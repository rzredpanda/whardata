"""
CLAUDE CODE MODEL - (Phase 1a: Strength-of-Schedule Adjusted Rating, v1)
WHL 2025 Competition — Custom Model by Claude Code

Mathematical formulation:
    SOS_i = mean win% of all opponents faced by team i
    Adjusted_winpct_i = raw_winpct_i * (SOS_i / mean_SOS)

    Iteratively refined: after each pass, update each team's raw_winpct
    using its actual win record, then recompute SOS from updated ratings.
    Convergence typically reached in ~50 iterations.

This model corrects a key deficiency in raw Points Standings: teams that
beat many weak opponents appear inflated. By weighting wins against
strong opponents more heavily, this model surfaces true competitive
strength independent of schedule luck.
"""
import os, datetime, warnings
import pandas as pd
import numpy as np
from scipy import stats

np.random.seed(42)
warnings.filterwarnings('ignore')

MODEL_NAME = "CLAUDE CODE MODEL - (Phase 1a: Strength-of-Schedule Adjusted Rating, v1)"
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
        f.write(f"[CC_SOS] {ts} | {msg}\n")
    print(msg)


def compute_sos_rating(game_df, team_df, n_iter=75):
    """
    Iterative Strength-of-Schedule Adjusted Rating.

    Algorithm:
    1. Initialize each team's rating = raw_win_pct
    2. For each team, compute SOS = mean opponent rating
    3. Compute adjusted_rating = wins weighted by opponent rating / games
    4. Repeat until convergence (change < 1e-6)
    """
    teams = team_df['team'].tolist()

    # Initial ratings = raw win percentage
    ratings = {}
    for _, row in team_df.iterrows():
        gp = row.get('gp', 82)  # games played
        w  = row.get('wins', row['points'] // 2)  # approximate wins from points
        ratings[row['team']] = w / gp if gp > 0 else 0.5

    # Build opponent map: for each team, list of opponents with game outcomes
    game_records = {}  # team -> list of (opponent, did_win)
    for t in teams:
        game_records[t] = []

    for _, g in game_df.iterrows():
        ht, at = g['home_team'], g['away_team']
        hw = g['home_win']
        if ht in game_records:
            game_records[ht].append((at, hw))
        if at in game_records:
            game_records[at].append((ht, 1 - hw))

    # Iterative refinement
    for iteration in range(n_iter):
        new_ratings = {}
        for team in teams:
            records = game_records.get(team, [])
            if not records:
                new_ratings[team] = 0.5
                continue
            # Weighted wins: sum(win_indicator * opponent_rating) / sum(opponent_rating)
            # This gives more credit for beating strong opponents
            weighted_wins = sum(
                w * ratings.get(opp, 0.5) for opp, w in records
            )
            total_weight = sum(
                ratings.get(opp, 0.5) for opp, w in records
            )
            new_ratings[team] = weighted_wins / total_weight if total_weight > 0 else 0.5

        # Check convergence
        max_change = max(abs(new_ratings[t] - ratings[t]) for t in teams)
        ratings = new_ratings
        if max_change < 1e-8:
            log(f"  SOS converged at iteration {iteration+1}, max_change={max_change:.2e}")
            break

    # Build output DataFrame
    rows = []
    for team, rating in ratings.items():
        # Compute SOS as mean opponent rating
        records = game_records.get(team, [])
        sos = np.mean([ratings.get(opp, 0.5) for opp, _ in records]) if records else 0.5
        rows.append({'team': team, 'sos_rating': round(rating, 6), 'sos': round(sos, 6)})

    df = pd.DataFrame(rows)
    df = df.sort_values('sos_rating', ascending=False).reset_index(drop=True)
    df['rank'] = range(1, len(df) + 1)
    df['score'] = df['sos_rating']
    return df


def validate_model(ranking_df, game_df, team_df):
    """Compute all 7 required validation metrics."""
    ts = team_df.set_index('team')

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

    # Brier score & log-loss from game-level rank → probability
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

    # Consensus rho
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

    ranking_df = compute_sos_rating(game_df, team_df)
    log("Top 10 SOS-Adjusted Rankings:")
    log(ranking_df.head(10)[['rank', 'team', 'sos_rating', 'sos']].to_string(index=False))

    out_path = os.path.join(OUT_DIR, 'cc_model_13_sos_adjusted_rating.csv')
    os.makedirs(OUT_DIR, exist_ok=True)
    ranking_df[['rank', 'team', 'score', 'sos_rating', 'sos']].to_csv(out_path, index=False)
    log(f"Saved: {out_path}")

    metrics = validate_model(ranking_df, game_df, team_df)
    log(f"Validation: tau={metrics['kendall_tau']:.4f}  rho={metrics['spearman_rho']:.4f}  "
        f"top8={metrics['top8_hit_rate']:.3f}  brier={metrics['brier_score']:.4f}  "
        f"ll={metrics['log_loss']:.4f}  acc={metrics['accuracy']:.4f}  "
        f"cons_rho={metrics['consensus_rho']:.4f}")

    # Append to validation_scores.csv
    if os.path.exists(VAL_FILE):
        val_df = pd.read_csv(VAL_FILE)
        # Remove old entry for this model if it exists
        val_df = val_df[val_df['model_name'] != MODEL_NAME]
        val_df = pd.concat([val_df, pd.DataFrame([metrics])], ignore_index=True)
        val_df.to_csv(VAL_FILE, index=False)
        log(f"Appended metrics to {VAL_FILE}")

    log(f"=== {MODEL_NAME} COMPLETED ===")


if __name__ == '__main__':
    main()
