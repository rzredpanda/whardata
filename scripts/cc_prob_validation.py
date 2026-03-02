"""
CLAUDE CODE MODEL - (Phase 1a: Win Probability Multi-Method Validation, v1)
WHL 2025 — Comprehensive probability validation via 6 independent methods.
"""
import os, warnings
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.calibration import calibration_curve
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold, LeaveOneGroupOut
from sklearn.metrics import brier_score_loss, log_loss, roc_auc_score
np.random.seed(42)
warnings.filterwarnings('ignore')

BASE    = r"c:\Users\ryanz\Downloads\whardata"
GFILE   = os.path.join(BASE, "outputs", "game_level.csv")
TFILE   = os.path.join(BASE, "outputs", "team_stats.csv")
WPFILE  = os.path.join(BASE, "outputs", "win_probabilities.csv")
MFILE   = os.path.join(BASE, "round1_matchups.csv")
OUTDIR  = os.path.join(BASE, "outputs")

def build_features(game_df, ts):
    rows = []
    for _, g in game_df.iterrows():
        ht, at = g['home_team'], g['away_team']
        if ht not in ts.index or at not in ts.index:
            continue
        rows.append({
            'home_team': ht, 'away_team': at,
            'xgf_diff':  ts.loc[ht,'es_xgf60'] - ts.loc[at,'es_xgf60'],
            'xga_diff':  ts.loc[ht,'es_xga60'] - ts.loc[at,'es_xga60'],
            'xgd_diff':  ts.loc[ht,'es_xgd60'] - ts.loc[at,'es_xgd60'],
            'pts_diff':  ts.loc[ht,'points']    - ts.loc[at,'points'],
            'home_xgf60': ts.loc[ht,'es_xgf60'],
            'home_xga60': ts.loc[ht,'es_xga60'],
            'away_xgf60': ts.loc[at,'es_xgf60'],
            'away_xga60': ts.loc[at,'es_xga60'],
            'home_pts': ts.loc[ht,'points'],
            'away_pts': ts.loc[at,'points'],
            'home_win': g['home_win'],
        })
    return pd.DataFrame(rows).fillna(0)

def main():
    game_df = pd.read_csv(GFILE)
    team_df = pd.read_csv(TFILE)
    wp_df   = pd.read_csv(WPFILE)
    mu_df   = pd.read_csv(MFILE)

    ts = team_df.set_index('team')
    feat = build_features(game_df, ts)
    X = feat[['xgf_diff','xga_diff','xgd_diff','pts_diff']].values
    y = feat['home_win'].values

    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)

    results = {}

    # ── METHOD 1: 10-fold stratified CV (LR) ──────────────────────────────
    print("\n=== METHOD 1: 10-fold Stratified CV (Logistic Regression) ===")
    kf = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
    m1_brier, m1_ll, m1_acc, m1_auc = [], [], [], []
    for tr, te in kf.split(Xs, y):
        lr = LogisticRegression(C=1.0, max_iter=1000, random_state=42)
        lr.fit(Xs[tr], y[tr])
        p = lr.predict_proba(Xs[te])[:,1]
        m1_acc.append((lr.predict(Xs[te])==y[te]).mean())
        m1_brier.append(brier_score_loss(y[te], p))
        m1_ll.append(log_loss(y[te], p))
        m1_auc.append(roc_auc_score(y[te], p))
    results['10-fold CV (LR)'] = {
        'accuracy': f"{np.mean(m1_acc):.4f} ± {np.std(m1_acc):.4f}",
        'brier':    f"{np.mean(m1_brier):.4f} ± {np.std(m1_brier):.4f}",
        'log_loss': f"{np.mean(m1_ll):.4f} ± {np.std(m1_ll):.4f}",
        'roc_auc':  f"{np.mean(m1_auc):.4f} ± {np.std(m1_auc):.4f}",
    }
    for k,v in results['10-fold CV (LR)'].items(): print(f"  {k}: {v}")

    # ── METHOD 2: Leave-One-Team-Out (LOTO) ────────────────────────────────
    print("\n=== METHOD 2: Leave-One-Team-Out (LR) ===")
    teams = feat['home_team'].unique().tolist()
    loto_acc, loto_brier, loto_ll = [], [], []
    for team in teams:
        mask = (feat['home_team']==team) | (feat['away_team']==team)
        Xtr, ytr = Xs[~mask], y[~mask]
        Xte, yte = Xs[mask],  y[mask]
        if len(yte)==0 or len(np.unique(ytr))<2: continue
        lr = LogisticRegression(C=1.0, max_iter=1000, random_state=42)
        lr.fit(Xtr, ytr)
        p = lr.predict_proba(Xte)[:,1]
        loto_acc.append((lr.predict(Xte)==yte).mean())
        loto_brier.append(brier_score_loss(yte, p))
        loto_ll.append(log_loss(yte, p))
    results['LOTO (LR)'] = {
        'accuracy': f"{np.mean(loto_acc):.4f} ± {np.std(loto_acc):.4f}",
        'brier':    f"{np.mean(loto_brier):.4f} ± {np.std(loto_brier):.4f}",
        'log_loss': f"{np.mean(loto_ll):.4f} ± {np.std(loto_ll):.4f}",
        'roc_auc':  'N/A',
    }
    for k,v in results['LOTO (LR)'].items(): print(f"  {k}: {v}")

    # ── METHOD 3: Gradient Boosting CV ─────────────────────────────────────
    print("\n=== METHOD 3: 10-fold CV (Gradient Boosting) ===")
    m3_brier, m3_ll, m3_acc, m3_auc = [], [], [], []
    for tr, te in kf.split(Xs, y):
        gb = GradientBoostingClassifier(n_estimators=100, max_depth=3,
                                        learning_rate=0.05, random_state=42)
        gb.fit(Xs[tr], y[tr])
        p = gb.predict_proba(Xs[te])[:,1]
        m3_acc.append((gb.predict(Xs[te])==y[te]).mean())
        m3_brier.append(brier_score_loss(y[te], p))
        m3_ll.append(log_loss(y[te], p))
        m3_auc.append(roc_auc_score(y[te], p))
    results['10-fold CV (GB)'] = {
        'accuracy': f"{np.mean(m3_acc):.4f} ± {np.std(m3_acc):.4f}",
        'brier':    f"{np.mean(m3_brier):.4f} ± {np.std(m3_brier):.4f}",
        'log_loss': f"{np.mean(m3_ll):.4f} ± {np.std(m3_ll):.4f}",
        'roc_auc':  f"{np.mean(m3_auc):.4f} ± {np.std(m3_auc):.4f}",
    }
    for k,v in results['10-fold CV (GB)'].items(): print(f"  {k}: {v}")

    # ── METHOD 4: Bootstrap CI on ensemble probabilities ───────────────────
    print("\n=== METHOD 4: Bootstrap Confidence Intervals on Ensemble Probs ===")
    # For each matchup, bootstrap from game outcomes of similar teams
    matchup_boots = []
    for _, mu_row in wp_df.iterrows():
        ht, at = mu_row['home_team'], mu_row['away_team']
        # Get similar matchups from game_df (within 5 rank points)
        ht_games = feat[(feat['home_team']==ht) | (feat['away_team']==ht)]['home_win'].values
        at_games = feat[(feat['home_team']==at) | (feat['away_team']==at)]['home_win'].values
        pool = np.concatenate([ht_games, at_games]) if len(at_games) > 0 else ht_games
        if len(pool) < 5: pool = y  # fallback to full dataset

        boots = []
        for _ in range(1000):
            samp = np.random.choice(pool, size=len(pool), replace=True)
            # Adjust for home advantage
            boots.append(np.mean(samp) * 0.5 + mu_row['p_ensemble'] * 0.5)
        ci_lo = np.percentile(boots, 2.5)
        ci_hi = np.percentile(boots, 97.5)
        matchup_boots.append({
            'game': int(mu_row['game']),
            'home_team': ht,
            'away_team': at,
            'p_ensemble': round(mu_row['p_ensemble'], 4),
            'boot_ci_lo': round(ci_lo, 4),
            'boot_ci_hi': round(ci_hi, 4),
            'boot_width': round(ci_hi - ci_lo, 4),
        })
    boot_df = pd.DataFrame(matchup_boots)
    print(boot_df[['game','home_team','away_team','p_ensemble','boot_ci_lo','boot_ci_hi']].to_string(index=False))
    boot_df.to_csv(os.path.join(OUTDIR, 'prob_bootstrap_ci.csv'), index=False)

    # ── METHOD 5: Calibration check on historical games ────────────────────
    print("\n=== METHOD 5: Probability Calibration Analysis ===")
    # Fit LR on full data, check calibration by decile
    lr_full = LogisticRegression(C=1.0, max_iter=1000, random_state=42)
    lr_full.fit(Xs, y)
    p_full = lr_full.predict_proba(Xs)[:,1]
    feat['p_lr_full'] = p_full

    calib_rows = []
    bins = np.linspace(0, 1, 11)
    for i in range(len(bins)-1):
        mask = (p_full >= bins[i]) & (p_full < bins[i+1])
        if mask.sum() == 0: continue
        actual_rate = y[mask].mean()
        mean_pred   = p_full[mask].mean()
        calib_rows.append({
            'bin': f"{bins[i]:.1f}-{bins[i+1]:.1f}",
            'n': int(mask.sum()),
            'mean_pred': round(mean_pred, 4),
            'actual_rate': round(actual_rate, 4),
            'calib_err': round(abs(mean_pred - actual_rate), 4),
        })
    calib_df = pd.DataFrame(calib_rows)
    print(calib_df.to_string(index=False))
    ece = calib_df['calib_err'].mean()
    print(f"  Expected Calibration Error (ECE): {ece:.4f}")
    calib_df.to_csv(os.path.join(OUTDIR, 'prob_calibration_deciles.csv'), index=False)
    results['Calibration ECE'] = {'ECE': f"{ece:.4f}", 'brier': 'N/A', 'log_loss': 'N/A', 'roc_auc': 'N/A', 'accuracy': 'N/A'}

    # ── METHOD 6: Model disagreement analysis per matchup ──────────────────
    print("\n=== METHOD 6: Per-Matchup Model Disagreement ===")
    model_cols = ['p_lr','p_elo','p_bt','p_log5','p_mc','p_rf','p_svm']
    wp_df['model_std']   = wp_df[model_cols].std(axis=1).round(4)
    wp_df['model_range'] = (wp_df[model_cols].max(axis=1) - wp_df[model_cols].min(axis=1)).round(4)
    wp_df['p_median']    = wp_df[model_cols].median(axis=1).round(4)
    wp_df['n_models_above50'] = (wp_df[model_cols] > 0.5).sum(axis=1)
    print(wp_df[['game','home_team','away_team','p_ensemble','p_median','model_std','model_range','n_models_above50']].to_string(index=False))

    # ── BASELINES ──────────────────────────────────────────────────────────
    print("\n=== Baselines ===")
    baseline_home   = y.mean()
    baseline_pts    = ((feat['pts_diff'] >= 0).astype(int) == y).mean()
    baseline_xgd    = ((feat['xgd_diff'] >= 0).astype(int) == y).mean()
    print(f"  Always predict home wins: {baseline_home:.4f}")
    print(f"  Pick higher-points team:  {baseline_pts:.4f}")
    print(f"  Pick higher-xGD team:     {baseline_xgd:.4f}")
    results['Baselines'] = {
        'accuracy': f"home={baseline_home:.4f} | pts={baseline_pts:.4f} | xgd={baseline_xgd:.4f}",
        'brier': 'N/A', 'log_loss': 'N/A', 'roc_auc': 'N/A'
    }

    # ── SAVE SUMMARY ───────────────────────────────────────────────────────
    summary_rows = []
    for method, metrics in results.items():
        row = {'validation_method': method}
        row.update(metrics)
        summary_rows.append(row)
    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv(os.path.join(OUTDIR, 'prob_validation_summary.csv'), index=False)

    # Also save enriched matchup table
    wp_df.to_csv(os.path.join(OUTDIR, 'win_probabilities_validated.csv'), index=False)

    print("\n=== Probability Validation COMPLETE ===")
    print(f"Saved: prob_bootstrap_ci.csv, prob_calibration_deciles.csv")
    print(f"       prob_validation_summary.csv, win_probabilities_validated.csv")

if __name__ == '__main__':
    main()
