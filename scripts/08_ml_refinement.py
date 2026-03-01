"""
ML Refinement Agent — WHL 2025
Phase 7: Advanced Machine Learning Models
Trains and tunes advanced models to improve upon Phase 1 win probability and ranking metrics.
"""
import os, datetime
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import brier_score_loss, log_loss
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import GradientBoostingClassifier
from scipy import stats

try:
    import xgboost as xgb
    HAS_XGB = True
except ImportError:
    HAS_XGB = False

try:
    import lightgbm as lgb
    HAS_LGB = True
except ImportError:
    HAS_LGB = False

np.random.seed(42)

LOG_FILE  = r"c:\Users\ryanz\Downloads\whardata\scratch\agent_log.txt"
OUT_DIR   = r"c:\Users\ryanz\Downloads\whardata\outputs"
GAME_FILE = r"c:\Users\ryanz\Downloads\whardata\outputs\game_level.csv"
TEAM_FILE = r"c:\Users\ryanz\Downloads\whardata\outputs\team_stats.csv"
VAL_DIR   = r"c:\Users\ryanz\Downloads\whardata\outputs\validation"
RANK_DIR  = r"c:\Users\ryanz\Downloads\whardata\outputs\rankings"

def log(msg):
    ts = datetime.datetime.now().isoformat()
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"[ML_AGENT] {ts} | {msg}\n")
    print(msg)

def build_features(game_df, ts):
    rows = []
    for _, g in game_df.iterrows():
        ht, at = g['home_team'], g['away_team']
        if ht not in ts.index or at not in ts.index:
            continue
        # Core rates
        h_xgf = ts.loc[ht,'es_xgf60'] or 0
        h_xga = ts.loc[ht,'es_xga60'] or 0
        a_xgf = ts.loc[at,'es_xgf60'] or 0
        a_xga = ts.loc[at,'es_xga60'] or 0
        
        # Advanced rates
        h_sh = ts.loc[ht,'points'] / 164.0  # approximate points percentage
        a_sh = ts.loc[at,'points'] / 164.0
        
        # Power Play / Penalty Kill indices if available
        # Using approximations if actual PP totals aren't in team_stats
        
        rows.append({
            'home_team': ht, 'away_team': at,
            'home_xgf60': h_xgf, 'home_xga60': h_xga,
            'away_xgf60': a_xgf, 'away_xga60': a_xga,
            'home_xgd60': h_xgf - h_xga,
            'away_xgd60': a_xgf - a_xga,
            'home_points_pct': h_sh,
            'away_points_pct': a_sh,
            'home_win': g['home_win']
        })
    return pd.DataFrame(rows).fillna(0)

def tune_and_evaluate(name, model, param_grid, X, y):
    log(f"Tuning {name}...")
    kf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    gs = GridSearchCV(model, param_grid, cv=kf, scoring='neg_log_loss', n_jobs=-1)
    gs.fit(X, y)
    
    best_model = gs.best_estimator_
    log(f"  Best params: {gs.best_params_}")
    
    # Evaluate with 10-fold CV on best model
    kf10 = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
    accs, briers, lls = [], [], []
    
    for tr_idx, val_idx in kf10.split(X, y):
        best_model.fit(X[tr_idx], y[tr_idx])
        p_val = best_model.predict_proba(X[val_idx])[:,1]
        preds = (p_val >= 0.5).astype(int)
        
        accs.append((preds == y[val_idx]).mean())
        briers.append(brier_score_loss(y[val_idx], p_val))
        lls.append(log_loss(y[val_idx], p_val))
        
    results = {
        'model': name,
        'accuracy': np.mean(accs),
        'brier': np.mean(briers),
        'log_loss': np.mean(lls)
    }
    log(f"  10-CV Acc: {np.mean(accs):.4f} | Brier: {np.mean(briers):.4f} | LogLoss: {np.mean(lls):.4f}")
    
    # Fit on all data to return the final model
    best_model.fit(X, y)
    return best_model, results

def derive_rankings_from_probs(model, scaler, team_df, features):
    """
    Simulate a full round-robin tournament using the trained model to rank teams.
    """
    teams = team_df['team'].tolist()
    ts = team_df.set_index('team')
    
    expected_wins = {t: 0.0 for t in teams}
    
    # Every team plays every other team once at home, once away
    for ht in teams:
        for at in teams:
            if ht == at: continue
            
            h_xgf = ts.loc[ht,'es_xgf60'] or 0; h_xga = ts.loc[ht,'es_xga60'] or 0
            a_xgf = ts.loc[at,'es_xgf60'] or 0; a_xga = ts.loc[at,'es_xga60'] or 0
            h_sh  = ts.loc[ht,'points'] / 164.0; a_sh  = ts.loc[at,'points'] / 164.0
            
            row = np.array([[
                h_xgf, h_xga, a_xgf, a_xga, 
                h_xgf-h_xga, a_xgf-a_xga, 
                h_sh, a_sh
            ]])
            
            row_scaled = scaler.transform(row)
            p_home_win = model.predict_proba(row_scaled)[0, 1]
            
            expected_wins[ht] += p_home_win
            expected_wins[at] += (1 - p_home_win)
            
    rank_df = pd.DataFrame(list(expected_wins.items()), columns=['team', 'expected_wins'])
    rank_df['rank'] = rank_df['expected_wins'].rank(ascending=False, method='min')
    return rank_df.sort_values('rank').reset_index(drop=True)

def main():
    log("=== ML Refinement Agent STARTED ===")
    
    game_df = pd.read_csv(GAME_FILE)
    team_df = pd.read_csv(TEAM_FILE)
    ts = team_df.set_index('team')
    
    feat_df = build_features(game_df, ts)
    features = [
        'home_xgf60', 'home_xga60', 'away_xgf60', 'away_xga60', 
        'home_xgd60', 'away_xgd60', 'home_points_pct', 'away_points_pct'
    ]
    
    X = feat_df[features].values
    y = feat_df['home_win'].values
    
    scaler = StandardScaler()
    X_s = scaler.fit_transform(X)
    
    models_to_try = []
    
    # 1. Gradient Boosting (sklearn)
    gbm = GradientBoostingClassifier(random_state=42)
    gbm_params = {
        'n_estimators': [50, 100, 200],
        'learning_rate': [0.01, 0.05, 0.1],
        'max_depth': [2, 3, 4],
        'subsample': [0.8, 1.0]
    }
    models_to_try.append(("Gradient Boosting", gbm, gbm_params))
    
    # 2. Multi-Layer Perceptron (Neural Net)
    mlp = MLPClassifier(random_state=42, max_iter=2000)
    mlp_params = {
        'hidden_layer_sizes': [(16,), (32, 16), (64, 32)],
        'alpha': [0.0001, 0.001, 0.01],
        'activation': ['relu', 'tanh']
    }
    models_to_try.append(("Neural Network (MLP)", mlp, mlp_params))
    
    # 3. XGBoost
    if HAS_XGB:
        xgb_model = xgb.XGBClassifier(random_state=42, use_label_encoder=False, eval_metric='logloss')
        xgb_params = {
            'n_estimators': [50, 100],
            'learning_rate': [0.01, 0.05, 0.1],
            'max_depth': [2, 3, 4],
            'colsample_bytree': [0.8, 1.0]
        }
        models_to_try.append(("XGBoost", xgb_model, xgb_params))
        
    # 4. LightGBM
    if HAS_LGB:
        lgb_model = lgb.LGBMClassifier(random_state=42)
        lgb_params = {
            'n_estimators': [50, 100],
            'learning_rate': [0.01, 0.05],
            'num_leaves': [7, 15, 31]
        }
        models_to_try.append(("LightGBM", lgb_model, lgb_params))

    # Evaluate all models
    results = []
    trained_models = {}
    
    for name, model, params in models_to_try:
        best_model, res = tune_and_evaluate(name, model, params, X_s, y)
        results.append(res)
        trained_models[name] = best_model
        
        # Generate new rankings based on this ML model
        log(f"Generating full round-robin rankings using {name}...")
        rank_df = derive_rankings_from_probs(best_model, scaler, team_df, features)
        
        # Save as model_11, model_12, etc depending on order
        idx = 11 + len(trained_models) - 1
        safe_name = name.replace(" ", "_").replace("(", "").replace(")", "").lower()
        rf_path = os.path.join(RANK_DIR, f"model_{idx}_{safe_name}.csv")
        rank_df.to_csv(rf_path, index=False)
        log(f"  Saved ML ranking to {rf_path}")
        
    res_df = pd.DataFrame(results)
    ml_val_path = os.path.join(VAL_DIR, "ml_models_validation.csv")
    res_df.to_csv(ml_val_path, index=False)
    log(f"ML evaluation results saved to {ml_val_path}")
    
    # Finally, run the main validation script again to generate validation_set2.csv
    log("Invoking 05_validation.py to validate the new ML rankings against ALL 7 metrics...")
    val_script = r"c:\Users\ryanz\Downloads\whardata\scripts\05_validation.py"
    
    # We must patch 05_validation.py briefly to save as validation_set2.csv
    # Or just let it run and then move the file. Let's just run it.
    os.system(f'python -X utf8 "{val_script}"')
    
    old_val = os.path.join(OUT_DIR, "validation_scores.csv")
    new_val = os.path.join(VAL_DIR, "validation_scores_set2.csv")
    if os.path.exists(old_val):
        import shutil
        shutil.move(old_val, new_val)
        log(f"Moved new validation results to {new_val}")
    
    log("=== ML Refinement Agent COMPLETED ===")

if __name__ == '__main__':
    main()
