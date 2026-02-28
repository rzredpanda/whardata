"""
Ranking Models Agent — WHL 2025
All 10 Power Ranking Models (Phase 1a)
"""
import os, datetime, warnings
import pandas as pd
import numpy as np
from scipy import stats, optimize
from scipy.linalg import solve
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

np.random.seed(42)
LOG_FILE  = r"c:\Users\ryanz\Downloads\whardata\scratch\agent_log.txt"
OUT_DIR   = r"c:\Users\ryanz\Downloads\whardata\outputs\rankings"
DATA_FILE = r"c:\Users\ryanz\Downloads\whardata\whl_2025.csv"
GAME_FILE = r"c:\Users\ryanz\Downloads\whardata\outputs\game_level.csv"
TEAM_FILE = r"c:\Users\ryanz\Downloads\whardata\outputs\team_stats.csv"

def log(msg):
    ts = datetime.datetime.now().isoformat()
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"[RANKING] {ts} | {msg}\n")
    print(msg)

def save_ranking(df, model_num, model_name, extra_cols=None):
    cols = ['rank', 'team', 'score'] + (extra_cols or [])
    fp = os.path.join(OUT_DIR, f"model_{model_num:02d}_{model_name}.csv")
    df.to_csv(fp, index=False)
    log(f"Saved: {fp}")
    return fp

# ── MODEL 1: Raw Points Standings ─────────────────────────────────────────────
def model1_points(game_df, team_df):
    log("Model 1: Raw Points Standings")
    df = team_df[['team','points','gd','xgd']].copy()
    df = df.sort_values(['points','gd','xgd'], ascending=[False,False,False]).reset_index(drop=True)
    df['rank'] = range(1, len(df)+1)
    df['score'] = df['points']
    save_ranking(df[['rank','team','score','points','gd','xgd']], 1, 'points_standings', ['points','gd','xgd'])
    return df

# ── MODEL 2: xG Differential per 60 (ES) ──────────────────────────────────────
def model2_xgd60(team_df):
    log("Model 2: xG Differential per 60")
    df = team_df[['team','es_xgf60','es_xga60','es_xgd60']].copy()
    df = df.sort_values('es_xgd60', ascending=False).reset_index(drop=True)
    df['rank'] = range(1, len(df)+1)
    df['score'] = df['es_xgd60']
    save_ranking(df[['rank','team','score','es_xgf60','es_xga60','es_xgd60']], 2, 'xgd60_es', ['es_xgf60','es_xga60','es_xgd60'])
    return df

# ── MODEL 3: Pythagorean Expectation ──────────────────────────────────────────
def model3_pythagorean(team_df):
    log("Model 3: Pythagorean Expectation")
    df = team_df[['team','xgf','xga','win_pct']].copy()
    
    # Tune k
    best_k, best_r = 2.0, -999
    for k in np.arange(1.5, 3.1, 0.1):
        pyth = df['xgf']**k / (df['xgf']**k + df['xga']**k)
        r = pyth.corr(df['win_pct'])
        if r > best_r:
            best_r = r
            best_k = round(k, 1)
    
    log(f"  Optimal k={best_k}, r={best_r:.4f}")
    df['pyth_winpct'] = df['xgf']**best_k / (df['xgf']**best_k + df['xga']**best_k)
    df['score'] = df['pyth_winpct']
    df['optimal_k'] = best_k
    df = df.sort_values('score', ascending=False).reset_index(drop=True)
    df['rank'] = range(1, len(df)+1)
    save_ranking(df[['rank','team','score','pyth_winpct','xgf','xga','optimal_k']], 3, 'pythagorean', ['pyth_winpct','xgf','xga','optimal_k'])
    return df, best_k

# ── MODEL 4: Elo Rating System ────────────────────────────────────────────────
def model4_elo(game_df):
    log("Model 4: Elo Rating System")
    teams = sorted(set(game_df['home_team'].unique()) | set(game_df['away_team'].unique()))
    elo = {t: 1500 for t in teams}
    K = 20
    HOME_ADV = 100
    
    history = []
    for _, row in game_df.sort_values('game_num').iterrows():
        ht, at = row['home_team'], row['away_team']
        e_home = 1 / (1 + 10**((elo[at] - elo[ht] - HOME_ADV)/400))
        e_away = 1 - e_home
        
        if row['went_ot'] == 0:
            # Regulation: winner gets 1, loser gets 0
            s_home = 1 if row['home_win'] == 1 else 0
        else:
            # OT: winner gets 0.5 extra? Use standard: home win=1, away win=0
            s_home = 1 if row['home_win'] == 1 else 0
        s_away = 1 - s_home
        
        elo[ht] += K * (s_home - e_home)
        elo[at] += K * (s_away - e_away)
        history.append({'game_id': row['game_id'], 'home': ht, 'away': at, 
                        'home_elo_after': elo[ht], 'away_elo_after': elo[at]})
    
    df = pd.DataFrame([{'team': t, 'score': round(v,2), 'elo': round(v,2)} for t,v in elo.items()])
    df = df.sort_values('score', ascending=False).reset_index(drop=True)
    df['rank'] = range(1, len(df)+1)
    save_ranking(df[['rank','team','score','elo']], 4, 'elo_ratings', ['elo'])
    return df

# ── MODEL 5: Colley Matrix Method ─────────────────────────────────────────────
def model5_colley(game_df):
    log("Model 5: Colley Matrix Method")
    teams = sorted(set(game_df['home_team'].unique()) | set(game_df['away_team'].unique()))
    n = len(teams)
    idx = {t: i for i,t in enumerate(teams)}
    
    C = np.eye(n) * 2  # diagonal starts at 2
    b = np.ones(n) / 2  # starts at 0.5 (prior)
    
    for _, row in game_df.iterrows():
        i, j = idx[row['home_team']], idx[row['away_team']]
        C[i,i] += 1; C[j,j] += 1
        C[i,j] -= 1; C[j,i] -= 1
        if row['home_win'] == 1:
            b[i] += 0.5; b[j] -= 0.5
        else:
            b[j] += 0.5; b[i] -= 0.5
    
    r = solve(C, b)
    df = pd.DataFrame([{'team': t, 'score': round(r[idx[t]],5), 'colley_rating': round(r[idx[t]],5)} for t in teams])
    df = df.sort_values('score', ascending=False).reset_index(drop=True)
    df['rank'] = range(1, len(df)+1)
    save_ranking(df[['rank','team','score','colley_rating']], 5, 'colley_matrix', ['colley_rating'])
    return df

# ── MODEL 6: Bradley-Terry ─────────────────────────────────────────────────────
def model6_bradley_terry(game_df):
    log("Model 6: Bradley-Terry Pairwise")
    teams = sorted(set(game_df['home_team'].unique()) | set(game_df['away_team'].unique()))
    n = len(teams)
    idx = {t: i for i,t in enumerate(teams)}
    
    wins = np.zeros(n)
    games_played = [{} for _ in range(n)]
    
    for _, row in game_df.iterrows():
        i, j = idx[row['home_team']], idx[row['away_team']]
        games_played[i][j] = games_played[i].get(j,0) + 1
        games_played[j][i] = games_played[j].get(i,0) + 1
        if row['home_win']==1:
            wins[i] += 1
        else:
            wins[j] += 1
    
    # Log-likelihood maximization
    def neg_log_likelihood(log_s):
        s = np.exp(log_s)
        ll = 0
        for _, row in game_df.iterrows():
            i, j = idx[row['home_team']], idx[row['away_team']]
            if row['home_win']==1:
                ll += np.log(s[i]/(s[i]+s[j]) + 1e-10)
            else:
                ll += np.log(s[j]/(s[i]+s[j]) + 1e-10)
        return -ll
    
    init = np.zeros(n)
    res = optimize.minimize(neg_log_likelihood, init, method='L-BFGS-B', 
                            options={'maxiter':1000,'ftol':1e-10})
    strengths = np.exp(res.x)
    
    df = pd.DataFrame([{'team': t, 'score': round(strengths[idx[t]],5), 
                        'bt_strength': round(strengths[idx[t]],5)} for t in teams])
    df = df.sort_values('score', ascending=False).reset_index(drop=True)
    df['rank'] = range(1, len(df)+1)
    save_ranking(df[['rank','team','score','bt_strength']], 6, 'bradley_terry', ['bt_strength'])
    return df

# ── MODEL 7: Composite Weighted Score ──────────────────────────────────────────
def model7_composite(team_df, goalie_df=None):
    log("Model 7: Composite Weighted Score")
    df = team_df[['team','es_xgd60','gd','pp_xgf60','pk_xga60','gsax60']].copy()
    
    # Fill missing values with median
    for col in ['es_xgd60','gd','pp_xgf60','pk_xga60','gsax60']:
        df[col] = df[col].fillna(df[col].median())
    
    # Z-score each metric
    df['z_xgd60']  = stats.zscore(df['es_xgd60'])
    df['z_gd']     = stats.zscore(df['gd'] / team_df['games'])
    df['z_gsax60'] = stats.zscore(df['gsax60'])
    df['z_pp']     = stats.zscore(df['pp_xgf60'])
    # PK: lower xGA is better, invert
    df['z_pk']     = stats.zscore(-df['pk_xga60'])
    
    # Weighted sum: xGD(0.35) + GD(0.15) + GSAx(0.20) + PP(0.15) + PK(0.15)
    df['composite'] = (0.35*df['z_xgd60'] + 0.15*df['z_gd'] + 0.20*df['z_gsax60'] +
                       0.15*df['z_pp']    + 0.15*df['z_pk'])
    df['score'] = df['composite']
    df = df.sort_values('score', ascending=False).reset_index(drop=True)
    df['rank'] = range(1, len(df)+1)
    save_ranking(df[['rank','team','score','composite','z_xgd60','z_gd','z_gsax60','z_pp','z_pk']], 
                 7, 'composite_weighted', ['composite','z_xgd60','z_gd','z_gsax60','z_pp','z_pk'])
    return df

# ── MODEL 8: Logistic Regression Strength ──────────────────────────────────────
def model8_logistic(game_df, team_df):
    log("Model 8: Logistic Regression Strength")
    ts = team_df.set_index('team')
    
    rows = []
    for _, g in game_df.iterrows():
        ht, at = g['home_team'], g['away_team']
        rows.append({
            'home_xgf60': ts.loc[ht,'es_xgf60'], 'home_xga60': ts.loc[ht,'es_xga60'],
            'away_xgf60': ts.loc[at,'es_xgf60'], 'away_xga60': ts.loc[at,'es_xga60'],
            'home_win': g['home_win']
        })
    X_df = pd.DataFrame(rows).fillna(0)
    X = X_df[['home_xgf60','home_xga60','away_xgf60','away_xga60']].values
    y = X_df['home_win'].values
    
    scaler = StandardScaler()
    X_s = scaler.fit_transform(X)
    
    lr = LogisticRegression(max_iter=1000, random_state=42)
    lr.fit(X_s, y)
    
    # Team strength: home xgf coef - away xgf coef for offensive, reverse for defensive
    coefs = lr.coef_[0]  # [h_xgf60, h_xga60, a_xgf60, a_xga60]
    log(f"  Coefficients: h_xgf60={coefs[0]:.4f}, h_xga60={coefs[1]:.4f}, a_xgf60={coefs[2]:.4f}, a_xga60={coefs[3]:.4f}")
    
    # Score each team: offensive contribution (xgf) + defensive contribution (negating xga)
    scores = []
    for _, row in team_df.iterrows():
        off = (row['es_xgf60'] or 0) * (coefs[0] - coefs[2]) / 2
        dff = (row['es_xga60'] or 0) * (coefs[1] - coefs[3]) / 2
        scores.append({'team': row['team'], 'lr_score': off - dff, 
                       'es_xgf60': row['es_xgf60'], 'es_xga60': row['es_xga60']})
    
    df = pd.DataFrame(scores)
    df['score'] = df['lr_score']
    df = df.sort_values('score', ascending=False).reset_index(drop=True)
    df['rank'] = range(1, len(df)+1)
    save_ranking(df[['rank','team','score','lr_score','es_xgf60','es_xga60']], 
                 8, 'logistic_regression', ['lr_score','es_xgf60','es_xga60'])
    return df, lr, scaler, coefs

# ── MODEL 9: Random Forest ──────────────────────────────────────────────────────
def model9_random_forest(game_df, team_df):
    log("Model 9: Random Forest Feature Importance")
    ts = team_df.set_index('team')
    
    feat_cols = ['home_xgf60','home_xga60','away_xgf60','away_xga60',
                 'home_gsax60','away_gsax60','home_pp','away_pp']
    rows = []
    for _, g in game_df.iterrows():
        ht, at = g['home_team'], g['away_team']
        rows.append({
            'home_xgf60': ts.loc[ht,'es_xgf60'] or 0,
            'home_xga60': ts.loc[ht,'es_xga60'] or 0,
            'away_xgf60': ts.loc[at,'es_xgf60'] or 0,
            'away_xga60': ts.loc[at,'es_xga60'] or 0,
            'home_gsax60': ts.loc[ht,'gsax60'] or 0,
            'away_gsax60': ts.loc[at,'gsax60'] or 0,
            'home_pp': ts.loc[ht,'pp_xgf60'] or 0,
            'away_pp': ts.loc[at,'pp_xgf60'] or 0,
            'home_win': g['home_win']
        })
    X_df = pd.DataFrame(rows).fillna(0)
    X = X_df[feat_cols].values
    y = X_df['home_win'].values
    
    rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf.fit(X, y)
    
    import_scores = rf.feature_importances_
    feat_importance = dict(zip(feat_cols, import_scores))
    log(f"  Feature importances: {feat_importance}")
    
    # Rank teams by linear combination of their top-feature values weighted by importance
    scores = []
    for _, row in team_df.iterrows():
        team_vals = {
            'home_xgf60': row.get('es_xgf60', 0) or 0,
            'home_xga60': -(row.get('es_xga60', 0) or 0),  # invert: lower is better
            'away_xgf60': -(row.get('es_xgf60', 0) or 0),   # when opponent, higher hurts
            'away_xga60': row.get('es_xga60', 0) or 0,
            'home_gsax60': row.get('gsax60', 0) or 0,
            'away_gsax60': -(row.get('gsax60', 0) or 0),
            'home_pp': row.get('pp_xgf60', 0) or 0,
            'away_pp': -(row.get('pp_xgf60', 0) or 0),
        }
        score = sum(feat_importance[f] * team_vals[f] for f in feat_cols)
        scores.append({'team': row['team'], 'rf_score': score})
    
    df = pd.DataFrame(scores)
    df['score'] = df['rf_score']
    df = df.sort_values('score', ascending=False).reset_index(drop=True)
    df['rank'] = range(1, len(df)+1)
    
    fi_df = pd.DataFrame([{'feature': k, 'importance': v} for k,v in feat_importance.items()])
    fi_path = os.path.join(OUT_DIR, "model_09_rf_feature_importance.csv")
    fi_df.sort_values('importance', ascending=False).to_csv(fi_path, index=False)
    
    save_ranking(df[['rank','team','score','rf_score']], 9, 'random_forest', ['rf_score'])
    return df

# ── MODEL 10: Monte Carlo Simulation ───────────────────────────────────────────
def model10_monte_carlo(game_df, team_df, n_simulations=1000):
    log("Model 10: Monte Carlo Simulation")
    teams = sorted(team_df['team'].unique())
    
    # For each team, model per-game xGF and xGA distributions
    team_dist = {}
    for team in teams:
        h = game_df[game_df['home_team']==team][['home_xg','away_xg']].copy()
        h.columns = ['xgf','xga']
        a = game_df[game_df['away_team']==team][['away_xg','home_xg']].copy()
        a.columns = ['xgf','xga']
        all_g = pd.concat([h, a], ignore_index=True)
        # Use mean as Poisson lambda (non-negative, discrete count-like data)
        lam_f = max(all_g['xgf'].mean(), 0.01)
        lam_a = max(all_g['xga'].mean(), 0.01)
        team_dist[team] = {'lambda_xgf': lam_f, 'lambda_xga': lam_a,
                           'std_xgf': all_g['xgf'].std(), 'std_xga': all_g['xga'].std()}
    
    rng = np.random.RandomState(42)
    unique_matchups = game_df[['home_team','away_team']].drop_duplicates().values
    
    sim_points = {t: [] for t in teams}
    
    for sim in range(n_simulations):
        season_pts = {t: 0 for t in teams}
        # Simulate all games for all teams
        for _, row in game_df.iterrows():
            ht, at = row['home_team'], row['away_team']
            # Sample xGF for each team from Poisson
            h_xgf = rng.poisson(max(team_dist[ht]['lambda_xgf'], 0.01))
            a_xgf = rng.poisson(max(team_dist[at]['lambda_xgf'], 0.01))
            
            if h_xgf > a_xgf:
                season_pts[ht] += 2
            elif a_xgf > h_xgf:
                season_pts[at] += 2
            else:
                # Tie → OT → 50/50
                if rng.random() < 0.5:
                    season_pts[ht] += 2; season_pts[at] += 1
                else:
                    season_pts[at] += 2; season_pts[ht] += 1
        
        for t in teams:
            sim_points[t].append(season_pts[t])
        
        if (sim+1) % 200 == 0:
            log(f"  Simulation {sim+1}/{n_simulations}")
    
    results = []
    for team in teams:
        pts_arr = np.array(sim_points[team])
        results.append({'team': team, 'mean_pts': round(pts_arr.mean(),2),
                        'std_pts': round(pts_arr.std(),2),
                        'score': round(pts_arr.mean(),2)})
    
    df = pd.DataFrame(results)
    df = df.sort_values('score', ascending=False).reset_index(drop=True)
    df['rank'] = range(1, len(df)+1)
    save_ranking(df[['rank','team','score','mean_pts','std_pts']], 10, 'monte_carlo', ['mean_pts','std_pts'])
    return df

# ── MAIN ───────────────────────────────────────────────────────────────────────
def main():
    log("=== Ranking Models Agent STARTED ===")
    
    game_df = pd.read_csv(GAME_FILE)
    team_df = pd.read_csv(TEAM_FILE)
    
    log(f"Games: {len(game_df)}, Teams: {len(team_df)}")
    
    m1  = model1_points(game_df, team_df)
    m2  = model2_xgd60(team_df)
    m3, best_k = model3_pythagorean(team_df)
    m4  = model4_elo(game_df)
    m5  = model5_colley(game_df)
    m6  = model6_bradley_terry(game_df)
    m7  = model7_composite(team_df)
    m8, lr, scaler, coefs = model8_logistic(game_df, team_df)
    m9  = model9_random_forest(game_df, team_df)
    m10 = model10_monte_carlo(game_df, team_df, n_simulations=1000)
    
    # Consensus ranking (mean rank across all 10 models)
    models = [m1, m2, m3, m4, m5, m6, m7, m8, m9, m10]
    model_names = ['points','xgd60','pythagorean','elo','colley','bt','composite','logistic','rf','montecarlo']
    
    all_teams = team_df['team'].tolist()
    consensus = pd.DataFrame({'team': all_teams})
    for m, name in zip(models, model_names):
        rank_map = m.set_index('team')['rank']
        consensus[f'rank_{name}'] = consensus['team'].map(rank_map)
    
    rank_cols = [f'rank_{n}' for n in model_names]
    consensus['mean_rank'] = consensus[rank_cols].mean(axis=1)
    consensus['rank_variance'] = consensus[rank_cols].var(axis=1)
    consensus['consensus_rank'] = consensus['mean_rank'].rank().astype(int)
    consensus = consensus.sort_values('mean_rank').reset_index(drop=True)
    consensus.to_csv(os.path.join(OUT_DIR, "consensus_rankings.csv"), index=False)
    
    log("Consensus rankings saved.")
    log("=== Ranking Models Agent COMPLETED ===")

if __name__ == '__main__':
    main()
