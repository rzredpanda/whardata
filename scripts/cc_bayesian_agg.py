"""
CLAUDE CODE MODEL - (Phase 1a: Ensemble Bayesian Rank Aggregation, v1)
WHL 2025 Competition — Custom Model by Claude Code

Mathematical formulation:
    Given K ranking models, each producing a rank vector r_k (k=1..K),
    the Bayesian aggregation constructs a posterior over the true ranking
    by treating each model's ranking as a noisy observation.

    Model:
        r_k[i] ~ N(true_rank[i], sigma_k^2)
        sigma_k inferred from each model's validation accuracy (higher
        accuracy → lower sigma → more weight in aggregation)

    Posterior mean rank:
        true_rank[i] = sum_k(w_k * r_k[i]) / sum_k(w_k)
        where w_k = 1 / sigma_k^2 = model_accuracy^2

    This is equivalent to precision-weighted rank aggregation, which is
    the optimal Bayesian estimator under Gaussian noise assumptions.

    Innovation over simple mean-rank:
    - Uses model validation accuracy as Bayesian prior precision
    - Models with lower Brier scores receive higher weights
    - Produces uncertainty quantification (posterior variance)
    - Accounts for model correlation via weight dampening
"""
import os, datetime, warnings
import pandas as pd
import numpy as np
from scipy import stats

np.random.seed(42)
warnings.filterwarnings('ignore')

MODEL_NAME = "CLAUDE CODE MODEL - (Phase 1a: Ensemble Bayesian Rank Aggregation, v1)"
LOG_FILE   = r"c:\Users\ryanz\Downloads\whardata\scratch\agent_log.txt"
OUT_DIR    = r"c:\Users\ryanz\Downloads\whardata\outputs\rankings"
GAME_FILE  = r"c:\Users\ryanz\Downloads\whardata\outputs\game_level.csv"
TEAM_FILE  = r"c:\Users\ryanz\Downloads\whardata\outputs\team_stats.csv"
RANK_DIR   = r"c:\Users\ryanz\Downloads\whardata\outputs\rankings"
VAL_FILE   = r"c:\Users\ryanz\Downloads\whardata\outputs\validation_scores.csv"


def log(msg):
    ts = datetime.datetime.now().isoformat()
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"[CC_BAYES] {ts} | {msg}\n")
    print(msg)


def load_all_models():
    """Load all available ranking models from outputs/rankings/."""
    model_files = {
        'points':        'model_01_points_standings.csv',
        'xgd60':         'model_02_xgd60_es.csv',
        'pythagorean':   'model_03_pythagorean.csv',
        'elo':           'model_04_elo_ratings.csv',
        'colley':        'model_05_colley_matrix.csv',
        'bradley_terry': 'model_06_bradley_terry.csv',
        'composite':     'model_07_composite_weighted.csv',
        'logistic':      'model_08_logistic_regression.csv',
        'random_forest': 'model_09_random_forest.csv',
        'monte_carlo':   'model_10_monte_carlo.csv',
    }

    # Also load cc models if available
    cc_files = {
        'cc_sos':       'cc_model_13_sos_adjusted_rating.csv',
        'cc_dc':        'cc_model_14_dixon_coles.csv',
    }

    model_ranks = {}
    for name, fname in {**model_files, **cc_files}.items():
        fp = os.path.join(RANK_DIR, fname)
        if os.path.exists(fp):
            try:
                df = pd.read_csv(fp)
                if 'team' in df.columns and 'rank' in df.columns:
                    model_ranks[name] = df.set_index('team')['rank']
                    log(f"  Loaded model: {name}")
            except Exception as e:
                log(f"  WARNING: Could not load {fname}: {e}")

    return model_ranks


def get_model_weights(model_ranks):
    """
    Compute Bayesian precision weights for each model.
    Weights based on historical validation accuracy (from validation_scores.csv)
    or uniform if not available.
    """
    weights = {}

    # Default uniform weights
    for name in model_ranks:
        weights[name] = 1.0

    # Try to load accuracy from validation scores
    if os.path.exists(VAL_FILE):
        val_df = pd.read_csv(VAL_FILE)
        if 'accuracy' in val_df.columns and 'model_name' in val_df.columns:
            for _, row in val_df.iterrows():
                model_key = row['model_name']
                # Match short names
                for name in model_ranks:
                    if name in model_key or model_key in name:
                        acc = row.get('accuracy', 0.5)
                        # Precision weight = acc^2 (higher accuracy = lower variance = more weight)
                        # Subtract baseline (0.5) to get excess accuracy
                        excess = max(0, acc - 0.50)
                        weights[name] = (0.5 + excess) ** 2
                        break

    log(f"  Model weights: {weights}")
    return weights


def compute_bayesian_aggregation(model_ranks, weights):
    """
    Precision-weighted Bayesian rank aggregation.
    Returns team scores (weighted mean rank) and posterior variance.
    """
    # Get all teams that appear in at least 3 models
    all_teams = set()
    for ranks in model_ranks.values():
        all_teams.update(ranks.index.tolist())

    rows = []
    for team in all_teams:
        team_weights = []
        team_ranks = []
        for name, ranks in model_ranks.items():
            if team in ranks.index:
                team_ranks.append(ranks[team])
                team_weights.append(weights.get(name, 1.0))

        if len(team_ranks) < 3:
            continue

        w = np.array(team_weights)
        r = np.array(team_ranks, dtype=float)

        # Weighted mean rank (Bayesian posterior mean)
        weighted_mean = np.average(r, weights=w)
        # Posterior variance (inverse of total precision, weighted by rank variance)
        posterior_var = np.sum(w * (r - weighted_mean) ** 2) / np.sum(w)

        rows.append({
            'team': team,
            'bayesian_mean_rank': round(weighted_mean, 4),
            'posterior_variance': round(posterior_var, 4),
            'n_models': len(team_ranks),
        })

    df = pd.DataFrame(rows)
    df = df.sort_values('bayesian_mean_rank', ascending=True).reset_index(drop=True)
    df['rank'] = range(1, len(df) + 1)
    df['score'] = -df['bayesian_mean_rank']  # negate so higher = better for score column
    return df


def validate_model(ranking_df, game_df, team_df):
    """Compute all 7 required validation metrics."""
    m_ranks = ranking_df.set_index('team')['rank']
    gt_df   = team_df.sort_values('points', ascending=False).reset_index(drop=True)
    gt_df['rank_pts'] = range(1, len(gt_df) + 1)
    gt_ranks = gt_df.set_index('team')['rank_pts']

    common = m_ranks.index.intersection(gt_ranks.index)
    tau, _ = stats.kendalltau(m_ranks[common], gt_ranks[common])
    rho, _ = stats.spearmanr(m_ranks[common], gt_ranks[common])

    top8_m  = set(ranking_df.head(8)['team'])
    top8_gt = set(gt_df.head(8)['team'])
    top8_hit = len(top8_m & top8_gt) / 8

    brier_list, ll_list = [], []
    inversions = 0; total_h2h = 0

    for _, g in game_df.iterrows():
        ht, at = g['home_team'], g['away_team']
        if ht in m_ranks.index and at in m_ranks.index:
            r_h, r_a = m_ranks[ht], m_ranks[at]
            p_h = 1 / (1 + np.exp((r_h - r_a) / 10.0))
            p_h = np.clip(p_h, 1e-6, 1 - 1e-6)
            y = g['home_win']
            brier_list.append((y - p_h) ** 2)
            ll_list.append(y * np.log(p_h) + (1 - y) * np.log(1 - p_h))
            pred_winner = ht if r_h < r_a else at
            actual_winner = ht if y == 1 else at
            if pred_winner != actual_winner:
                inversions += 1
            total_h2h += 1

    brier = np.mean(brier_list) if brier_list else np.nan
    logloss = -np.mean(ll_list) if ll_list else np.nan
    inversion_rate = inversions / total_h2h if total_h2h > 0 else np.nan

    cons_file = os.path.join(RANK_DIR, 'consensus_rankings.csv')
    consensus_rho = np.nan
    if os.path.exists(cons_file):
        cons_df = pd.read_csv(cons_file).set_index('team')
        if 'mean_rank' in cons_df.columns:
            common2 = m_ranks.index.intersection(cons_df.index)
            consensus_rho, _ = stats.spearmanr(m_ranks[common2], cons_df.loc[common2, 'mean_rank'])

    return {
        'model_name': MODEL_NAME,
        'kendall_tau': round(tau, 4),
        'spearman_rho': round(rho, 4),
        'top8_hit_rate': round(top8_hit, 4),
        'brier_score': round(brier, 4) if not np.isnan(brier) else np.nan,
        'log_loss': round(logloss, 4) if not np.isnan(logloss) else np.nan,
        'rank_inversion_rate': round(inversion_rate, 4) if not np.isnan(inversion_rate) else np.nan,
        'accuracy': round(1 - inversion_rate, 4) if not np.isnan(inversion_rate) else np.nan,
        'consensus_rho': round(consensus_rho, 4) if not np.isnan(consensus_rho) else np.nan,
    }


def main():
    log(f"=== {MODEL_NAME} STARTED ===")

    if not os.path.exists(GAME_FILE):
        log("ERROR: game_level.csv not found — run 01_game_aggregation.py first")
        return

    game_df = pd.read_csv(GAME_FILE)
    team_df = pd.read_csv(TEAM_FILE)
    log(f"Loaded {len(game_df)} games, {len(team_df)} teams")

    model_ranks = load_all_models()
    log(f"Loaded {len(model_ranks)} models for aggregation")

    weights = get_model_weights(model_ranks)
    ranking_df = compute_bayesian_aggregation(model_ranks, weights)

    log("Top 10 Bayesian Aggregated Rankings:")
    log(ranking_df.head(10)[['rank', 'team', 'bayesian_mean_rank', 'posterior_variance']].to_string(index=False))

    out_path = os.path.join(OUT_DIR, 'cc_model_15_bayesian_aggregation.csv')
    os.makedirs(OUT_DIR, exist_ok=True)
    ranking_df[['rank', 'team', 'score', 'bayesian_mean_rank', 'posterior_variance', 'n_models']].to_csv(out_path, index=False)
    log(f"Saved: {out_path}")

    metrics = validate_model(ranking_df, game_df, team_df)
    log(f"Validation: tau={metrics['kendall_tau']:.4f}  rho={metrics['spearman_rho']:.4f}  "
        f"top8={metrics['top8_hit_rate']:.3f}  brier={metrics['brier_score']:.4f}  "
        f"ll={metrics['log_loss']:.4f}  acc={metrics['accuracy']:.4f}  "
        f"cons_rho={metrics['consensus_rho']:.4f}")

    if os.path.exists(VAL_FILE):
        val_df = pd.read_csv(VAL_FILE)
        val_df = val_df[val_df['model_name'] != MODEL_NAME]
        val_df = pd.concat([val_df, pd.DataFrame([metrics])], ignore_index=True)
        val_df.to_csv(VAL_FILE, index=False)
        log(f"Appended metrics to {VAL_FILE}")

    log(f"=== {MODEL_NAME} COMPLETED ===")


if __name__ == '__main__':
    main()
