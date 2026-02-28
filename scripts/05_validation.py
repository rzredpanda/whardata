"""
Validation Agent — WHL 2025
Phase 5: All validation routines for ranking and disparity models
"""
import os, datetime, glob, warnings
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import brier_score_loss, log_loss
import warnings
warnings.filterwarnings('ignore')

np.random.seed(42)
LOG_FILE  = r"c:\Users\ryanz\Downloads\whardata\scratch\agent_log.txt"
OUT_DIR   = r"c:\Users\ryanz\Downloads\whardata\outputs"
RANK_DIR  = r"c:\Users\ryanz\Downloads\whardata\outputs\rankings"
DISP_DIR  = r"c:\Users\ryanz\Downloads\whardata\outputs\disparity"
GAME_FILE = r"c:\Users\ryanz\Downloads\whardata\outputs\game_level.csv"
TEAM_FILE = r"c:\Users\ryanz\Downloads\whardata\outputs\team_stats.csv"

def log(msg):
    ts = datetime.datetime.now().isoformat()
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"[VALID] {ts} | {msg}\n")
    print(msg)

def build_features(game_df, ts):
    rows = []
    for _, g in game_df.iterrows():
        ht, at = g['home_team'], g['away_team']
        if ht not in ts.index or at not in ts.index:
            continue
        rows.append({
            'home_team': ht, 'away_team': at,
            'home_xgf60': ts.loc[ht,'es_xgf60'] or 0,
            'home_xga60': ts.loc[ht,'es_xga60'] or 0,
            'away_xgf60': ts.loc[at,'es_xgf60'] or 0,
            'away_xga60': ts.loc[at,'es_xga60'] or 0,
            'home_pts':   ts.loc[ht,'points'],
            'away_pts':   ts.loc[at,'points'],
            'home_xgd60': (ts.loc[ht,'es_xgf60'] or 0) - (ts.loc[ht,'es_xga60'] or 0),
            'away_xgd60': (ts.loc[at,'es_xgf60'] or 0) - (ts.loc[at,'es_xga60'] or 0),
            'home_win': g['home_win']
        })
    return pd.DataFrame(rows).fillna(0)

def validate_ranking_model(model_df, game_df, team_df, model_name, gt_col='rank_points'):
    """Compute all 7 validation metrics for a ranking model."""
    ts = team_df.set_index('team')
    feat_df = build_features(game_df, ts)
    baseline_pts = team_df.set_index('team')['rank_points']
    
    # Merge model ranks with ground truth (points rank)
    m_ranks = model_df.set_index('team')['rank']
    gt_ranks = team_df.set_index('team')['rank_points']
    
    common = m_ranks.index.intersection(gt_ranks.index)
    m_arr  = m_ranks[common].values.astype(float)
    gt_arr = gt_ranks[common].values.astype(float)
    
    # 1. Kendall's tau
    tau, p_tau = stats.kendalltau(m_arr, gt_arr)
    
    # 2. Spearman's rho
    rho, p_rho = stats.spearmanr(m_arr, gt_arr)
    
    # 3. Top-8 hit rate
    top8_m  = set(model_df.head(8)['team'])
    top8_gt = set(team_df.head(8)['team'])
    top8_hit = len(top8_m & top8_gt) / 8
    
    # 4. Brier Score — use model rank to estimate win probability
    # Prob(home wins) ≈ 1 / (1 + exp(away_rank - home_rank)) as a naive conversion
    brier_list, ll_list = [], []
    for _, g in feat_df.iterrows():
        ht, at = g['home_team'], g['away_team']
        if ht in m_ranks.index and at in m_ranks.index:
            r_h, r_a = m_ranks[ht], m_ranks[at]  # lower rank = better
            # Convert rank difference to probability (logistic)
            p_h = 1 / (1 + np.exp((r_h - r_a) / 10.0))
            p_h = np.clip(p_h, 1e-6, 1-1e-6)
            y = g['home_win']
            brier_list.append((y - p_h)**2)
            ll_list.append(y*np.log(p_h) + (1-y)*np.log(1-p_h))
    brier = np.mean(brier_list) if brier_list else np.nan
    logloss = -np.mean(ll_list) if ll_list else np.nan
    
    # 5. Rank Inversion Rate — check head-to-head: does higher-ranked team win more?
    inversions = 0; total_h2h = 0
    for _, g in feat_df.iterrows():
        ht, at = g['home_team'], g['away_team']
        if ht in m_ranks.index and at in m_ranks.index:
            r_h, r_a = m_ranks[ht], m_ranks[at]
            predicted_winner = ht if r_h < r_a else at
            actual_winner    = ht if g['home_win']==1 else at
            if predicted_winner != actual_winner:
                inversions += 1
            total_h2h += 1
    inversion_rate = inversions / total_h2h if total_h2h > 0 else np.nan
    accuracy = 1 - inversion_rate
    
    # 6. Consensus Rho — load consensus ranking
    cons_file = os.path.join(RANK_DIR, "consensus_rankings.csv")
    consensus_rho = np.nan
    if os.path.exists(cons_file):
        cons_df = pd.read_csv(cons_file).set_index('team')
        if 'mean_rank' in cons_df.columns:
            common2 = m_ranks.index.intersection(cons_df.index)
            cons_rho, _ = stats.spearmanr(m_ranks[common2], cons_df.loc[common2,'mean_rank'])
            consensus_rho = cons_rho
    
    return {
        'model_name': model_name,
        'kendall_tau': round(tau, 4),
        'spearman_rho': round(rho, 4),
        'top8_hit_rate': round(top8_hit, 4),
        'brier_score': round(brier, 4) if not np.isnan(brier) else np.nan,
        'log_loss': round(logloss, 4) if not np.isnan(logloss) else np.nan,
        'rank_inversion_rate': round(inversion_rate, 4) if not np.isnan(inversion_rate) else np.nan,
        'accuracy': round(accuracy, 4) if not np.isnan(accuracy) else np.nan,
        'consensus_rho': round(consensus_rho, 4) if not np.isnan(consensus_rho) else np.nan
    }

def validate_win_prob_model(game_df, team_df):
    """Logistic regression validation: in-sample + 10-fold CV + LOTO."""
    log("Validating win probability model (LR)...")
    ts = team_df.set_index('team')
    feat_df = build_features(game_df, ts)
    X = feat_df[['home_xgf60','home_xga60','away_xgf60','away_xga60']].values
    y = feat_df['home_win'].values
    
    scaler = StandardScaler()
    X_s = scaler.fit_transform(X)
    
    # In-sample
    lr = LogisticRegression(max_iter=1000, random_state=42)
    lr.fit(X_s, y)
    y_prob = lr.predict_proba(X_s)[:,1]
    in_acc = (lr.predict(X_s)==y).mean()
    in_brier = brier_score_loss(y, y_prob)
    in_ll = log_loss(y, y_prob)
    
    # 10-fold CV
    kf = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
    cv_accs, cv_briers, cv_lls = [], [], []
    for tr_idx, val_idx in kf.split(X_s, y):
        lr_cv = LogisticRegression(max_iter=1000, random_state=42)
        lr_cv.fit(X_s[tr_idx], y[tr_idx])
        p_val = lr_cv.predict_proba(X_s[val_idx])[:,1]
        cv_accs.append((lr_cv.predict(X_s[val_idx])==y[val_idx]).mean())
        cv_briers.append(brier_score_loss(y[val_idx], p_val))
        cv_lls.append(log_loss(y[val_idx], p_val))
    
    # LOTO (Leave-One-Team-Out)
    teams = team_df['team'].tolist()
    loto_accs = []
    feat_df_copy = feat_df.copy()
    for team in teams:
        mask_out = (feat_df_copy['home_team']==team) | (feat_df_copy['away_team']==team)
        X_tr = X_s[~mask_out]; y_tr = y[~mask_out]
        X_te = X_s[mask_out];  y_te = y[mask_out]
        if len(y_te) == 0 or len(np.unique(y_tr)) < 2:
            continue
        lr_l = LogisticRegression(max_iter=1000, random_state=42)
        lr_l.fit(X_tr, y_tr)
        loto_accs.append((lr_l.predict(X_te)==y_te).mean())
    
    # Baselines
    always_home = y.mean()  # always predict home wins
    higher_pts  = (feat_df['home_pts'] >= feat_df['away_pts']).astype(int)
    baseline_pts_acc = (higher_pts.values == y).mean()
    higher_xgd  = (feat_df['home_xgd60'] >= feat_df['away_xgd60']).astype(int)
    baseline_xgd_acc = (higher_xgd.values == y).mean()
    
    results = {
        'in_sample_accuracy': round(in_acc,4),
        'in_sample_brier': round(in_brier,4),
        'in_sample_logloss': round(in_ll,4),
        'cv10_acc_mean': round(np.mean(cv_accs),4),
        'cv10_acc_std': round(np.std(cv_accs),4),
        'cv10_brier_mean': round(np.mean(cv_briers),4),
        'cv10_logloss_mean': round(np.mean(cv_lls),4),
        'loto_acc_mean': round(np.mean(loto_accs),4),
        'loto_acc_std': round(np.std(loto_accs),4),
        'baseline_always_home': round(always_home,4),
        'baseline_higher_pts': round(baseline_pts_acc,4),
        'baseline_higher_xgd': round(baseline_xgd_acc,4),
    }
    log(f"  In-sample accuracy: {in_acc:.4f}")
    log(f"  10-fold CV accuracy: {np.mean(cv_accs):.4f} ± {np.std(cv_accs):.4f}")
    log(f"  LOTO accuracy: {np.mean(loto_accs):.4f}")
    log(f"  Baselines: always_home={always_home:.4f}, pts={baseline_pts_acc:.4f}, xgd={baseline_xgd_acc:.4f}")
    return results

def validate_disparity():
    """Validate line disparity methods."""
    log("Validating disparity methods...")
    
    disp_files = sorted(glob.glob(os.path.join(DISP_DIR, "method_*.csv")))
    team_df = pd.read_csv(TEAM_FILE)
    gt_pts = team_df.set_index('team')['rank_points']
    
    method_ranks = {}
    for fp in disp_files:
        name = os.path.basename(fp).replace('.csv','').replace('method_','')
        d = pd.read_csv(fp)
        if 'rank' in d.columns and 'team' in d.columns:
            method_ranks[name] = d.set_index('team')['rank']
    
    # Spearman correlation matrix between all disparity methods
    method_names = list(method_ranks.keys())
    n = len(method_names)
    corr_matrix = np.zeros((n,n))
    for i, m1 in enumerate(method_names):
        for j, m2 in enumerate(method_names):
            common = method_ranks[m1].index.intersection(method_ranks[m2].index)
            if len(common) > 3:
                rho, _ = stats.spearmanr(method_ranks[m1][common], method_ranks[m2][common])
                corr_matrix[i,j] = rho
    
    corr_df = pd.DataFrame(corr_matrix, index=method_names, columns=method_names)
    corr_df.to_csv(os.path.join(OUT_DIR, "disparity_method_correlation.csv"))
    log(f"  Disparity method correlation saved.")
    
    # Disparity vs standings correlation
    disp_vs_pts = []
    cons_file = os.path.join(DISP_DIR, "consensus_disparity.csv")
    if os.path.exists(cons_file):
        cons = pd.read_csv(cons_file)
        merged = cons.merge(team_df[['team','rank_points']], on='team')
        if 'mean_rank' in merged.columns:
            rho, p = stats.spearmanr(merged['mean_rank'], merged['rank_points'])
            log(f"  Disparity rank vs points rank Spearman rho={rho:.4f} p={p:.4f}")
            disp_vs_pts = {'rank_correlation': round(rho,4), 'p_value': round(p,4)}
    
    return corr_df, disp_vs_pts

def original_validation_1(game_df, team_df):
    """
    Original Validation 1: Elo Calibration Curve
    Check whether teams with higher Elo win at the rate the Elo system predicts.
    Bin games by predicted Elo win probability decile, compare vs actual win rate.
    """
    log("Original Validation 1: Elo Calibration Curve")
    elo_file = os.path.join(RANK_DIR, "model_04_elo_ratings.csv")
    if not os.path.exists(elo_file):
        return None
    elo_df = pd.read_csv(elo_file).set_index('team')
    HOME_ADV = 100
    
    probs, actuals = [], []
    for _, g in game_df.iterrows():
        ht, at = g['home_team'], g['away_team']
        if ht in elo_df.index and at in elo_df.index:
            p = 1 / (1 + 10**((elo_df.loc[at,'elo'] - elo_df.loc[ht,'elo'] - HOME_ADV)/400))
            probs.append(p)
            actuals.append(g['home_win'])
    
    calib_df = pd.DataFrame({'prob': probs, 'actual': actuals})
    calib_df['decile'] = pd.cut(calib_df['prob'], bins=10, labels=False)
    cal = calib_df.groupby('decile').agg(mean_pred=('prob','mean'), mean_actual=('actual','mean'), n=('actual','count'))
    cal['calibration_error'] = (cal['mean_pred'] - cal['mean_actual']).abs()
    log(f"  Elo ECE (Expected Calibration Error): {cal['calibration_error'].mean():.4f}")
    cal.to_csv(os.path.join(OUT_DIR, "elo_calibration_curve.csv"))
    return cal

def original_validation_2(game_df, team_df):
    """
    Original Validation 2: Score Confidence Interval Overlap
    For each pair of adjacent ranked teams, compute bootstrap CIs on their xGD/60.
    Flag pairs where CIs overlap — these rankings are not statistically distinguishable.
    """
    log("Original Validation 2: Score CI Overlap for Adjacent Rankings")
    team_df_sorted = team_df.sort_values('es_xgd60', ascending=False).reset_index(drop=True)
    
    rng = np.random.RandomState(42)
    ci_results = []
    
    for _, row in team_df_sorted.iterrows():
        team = row['team']
        # Get per-game xGD/60 from game_df
        h = game_df[game_df['home_team']==team]
        a = game_df[game_df['away_team']==team]
        # Daily xgd: using season total xg / total toi is single number; use per-game
        # We'll use the team's es_xgd60 as point estimate and bootstrap from game-level xg
        h_xgdf = h['home_xg']; a_xgdf = a['away_xg']
        h_xgda = h['away_xg']; a_xgda = a['home_xg']
        h_toi  = h['total_toi'] if 'total_toi' in h.columns else pd.Series([3600]*len(h))
        a_toi  = a['total_toi'] if 'total_toi' in a.columns else pd.Series([3600]*len(a))
        
        game_xgd = pd.concat([
            (h_xgdf.values - h_xgda.values),
            (a_xgdf.values - a_xgda.values)
        ])
        
        boots = []
        for _ in range(500):
            sample = rng.choice(game_xgd, size=len(game_xgd), replace=True)
            boots.append(sample.mean())
        ci_lo = np.percentile(boots, 2.5)
        ci_hi = np.percentile(boots, 97.5)
        ci_results.append({'team': team, 'mean_xgd': np.mean(game_xgd), 
                           'ci_lo': round(ci_lo,4), 'ci_hi': round(ci_hi,4)})
    
    ci_df = pd.DataFrame(ci_results).sort_values('mean_xgd', ascending=False).reset_index(drop=True)
    ci_df['rank'] = range(1, len(ci_df)+1)
    
    # Flag adjacent pairs with overlapping CIs
    overlaps = []
    for i in range(len(ci_df)-1):
        r1 = ci_df.iloc[i]; r2 = ci_df.iloc[i+1]
        overlap = r1['ci_hi'] > r2['ci_lo']
        overlaps.append({'team_upper': r1['team'], 'team_lower': r2['team'], 'ci_overlap': overlap})
    
    overlap_df = pd.DataFrame(overlaps)
    overlap_pct = overlap_df['ci_overlap'].mean()
    log(f"  Adjacent rank pairs with overlapping CIs: {overlap_pct:.1%}")
    ci_df.to_csv(os.path.join(OUT_DIR, "ranking_ci_overlap.csv"), index=False)
    return ci_df, overlap_df

def main():
    log("=== Validation Agent STARTED ===")
    game_df = pd.read_csv(GAME_FILE)
    team_df = pd.read_csv(TEAM_FILE)
    
    # ── Load all ranking models ────────────────────────
    model_files = {
        'points':         'model_01_points_standings.csv',
        'xgd60':          'model_02_xgd60_es.csv',
        'pythagorean':    'model_03_pythagorean.csv',
        'elo':            'model_04_elo_ratings.csv',
        'colley':         'model_05_colley_matrix.csv',
        'bradley_terry':  'model_06_bradley_terry.csv',
        'composite':      'model_07_composite_weighted.csv',
        'logistic':       'model_08_logistic_regression.csv',
        'random_forest':  'model_09_random_forest.csv',
        'monte_carlo':    'model_10_monte_carlo.csv',
    }
    
    validation_rows = []
    missing = []
    for name, fname in model_files.items():
        fp = os.path.join(RANK_DIR, fname)
        if os.path.exists(fp):
            try:
                mdf = pd.read_csv(fp)
                log(f"Validating model: {name}")
                row = validate_ranking_model(mdf, game_df, team_df, name)
                validation_rows.append(row)
                log(f"  τ={row['kendall_tau']:.3f}  ρ={row['spearman_rho']:.3f}  "
                    f"top8={row['top8_hit_rate']:.3f}  acc={row['accuracy']:.3f}  "
                    f"brier={row['brier_score']:.4f}  ll={row['log_loss']:.4f}  "
                    f"cons_ρ={row['consensus_rho']:.3f}")
            except Exception as e:
                log(f"  ERROR validating {name}: {e}")
        else:
            missing.append(fp)
            log(f"  SKIPPED (file not found): {fp}")
    
    if validation_rows:
        val_df = pd.DataFrame(validation_rows)
        val_df.to_csv(os.path.join(OUT_DIR, "validation_scores.csv"), index=False)
        log(f"Validation scores saved: {len(val_df)} models")
    
    # ── Win probability validation ─────────────────────
    wp_results = validate_win_prob_model(game_df, team_df)
    wp_df = pd.DataFrame([wp_results])
    wp_df.to_csv(os.path.join(OUT_DIR, "win_prob_validation.csv"), index=False)
    
    # ── Model agreement matrix ─────────────────────────
    log("Computing model agreement matrix...")
    model_dfs = {}
    for name, fname in model_files.items():
        fp = os.path.join(RANK_DIR, fname)
        if os.path.exists(fp):
            model_dfs[name] = pd.read_csv(fp).set_index('team')['rank']
    
    names = list(model_dfs.keys())
    agree_mat = np.zeros((len(names), len(names)))
    game_feat = build_features(game_df, team_df.set_index('team'))
    for i, n1 in enumerate(names):
        for j, n2 in enumerate(names):
            agrees = 0; total = 0
            for _, g in game_feat.iterrows():
                ht, at = g['home_team'], g['away_team']
                if (ht in model_dfs[n1].index and at in model_dfs[n1].index and
                    ht in model_dfs[n2].index and at in model_dfs[n2].index):
                    pred1 = ht if model_dfs[n1][ht] < model_dfs[n1][at] else at
                    pred2 = ht if model_dfs[n2][ht] < model_dfs[n2][at] else at
                    if pred1 == pred2: agrees += 1
                    total += 1
            agree_mat[i,j] = agrees/total if total > 0 else np.nan
    
    agree_df = pd.DataFrame(agree_mat, index=names, columns=names)
    agree_df.to_csv(os.path.join(OUT_DIR, "model_agreement_matrix.csv"))
    log("Model agreement matrix saved.")
    
    # ── Disparity validation ───────────────────────────
    disp_corr, disp_vs_pts = validate_disparity()
    
    # ── Original validations ───────────────────────────
    cal = original_validation_1(game_df, team_df)
    ci_df, overlap_df = original_validation_2(game_df, team_df)
    
    log("\n=== All Validation Complete ===")
    if validation_rows:
        val_df_show = pd.read_csv(os.path.join(OUT_DIR, "validation_scores.csv"))
        log("\nSummary Table:")
        log(val_df_show[['model_name','kendall_tau','spearman_rho','top8_hit_rate',
                         'brier_score','log_loss','accuracy','consensus_rho']].to_string(index=False))
    
    log("=== Validation Agent COMPLETED ===")

if __name__ == '__main__':
    main()
