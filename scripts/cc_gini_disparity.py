"""
CLAUDE CODE MODEL - (Phase 1b: Gini Line Disparity Index, v1)
WHL 2025 Competition — Custom Model by Claude Code

Mathematical formulation:
    The Gini coefficient measures inequality in a distribution.
    Applied to offensive line output:

        G = (2 * sum_i(i * x_i)) / (N * sum_i(x_i)) - (N+1)/N

    where x_i are line xG/60 values sorted in ascending order, N = number of lines.

    For a team with 2 offensive lines (first_off, second_off):
        G = |xG_per60_line1 - xG_per60_line2| / (xG_per60_line1 + xG_per60_line2)

    Gini = 0 → perfectly equal lines
    Gini → 1 → all output concentrated in one line

    This is superior to a simple ratio because:
    1. Bounded between 0 and 1 (interpretable inequality score)
    2. More numerically stable when a line has near-zero output
    3. Directly interpretable as a percent of "inequality"

    We also compute an opponent-adjusted version:
        adj_xG_per60 = raw_xG_per60 / mean_opponent_xGA_per60_vs_this_line_type

    This accounts for the fact that some lines face tougher defensive matchups.
"""
import os, datetime, warnings
import pandas as pd
import numpy as np
from scipy import stats

np.random.seed(42)
warnings.filterwarnings('ignore')

MODEL_NAME = "CLAUDE CODE MODEL - (Phase 1b: Gini Line Disparity Index, v1)"
LOG_FILE   = r"c:\Users\ryanz\Downloads\whardata\scratch\agent_log.txt"
OUT_DIR    = r"c:\Users\ryanz\Downloads\whardata\outputs\disparity"
DATA_FILE  = r"c:\Users\ryanz\Downloads\whardata\whl_2025.csv"
TEAM_FILE  = r"c:\Users\ryanz\Downloads\whardata\outputs\team_stats.csv"
RANK_DIR   = r"c:\Users\ryanz\Downloads\whardata\outputs\rankings"
VAL_FILE   = r"c:\Users\ryanz\Downloads\whardata\outputs\validation_scores.csv"


def log(msg):
    ts = datetime.datetime.now().isoformat()
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"[CC_GINI] {ts} | {msg}\n")
    print(msg)


def gini_two_values(x1, x2):
    """Gini coefficient for two values (offensive lines)."""
    total = x1 + x2
    if total <= 0:
        return 0.0
    return abs(x1 - x2) / total


def compute_line_xg_per60(df, team, is_home):
    """
    Compute TOI-normalized xG per 60 for each offensive line of a team.
    Only Even-Strength rows (home_off_line in [first_off, second_off]).
    """
    if is_home:
        team_df = df[df['home_team'] == team].copy()
        team_df = team_df[team_df['home_off_line'].isin(['first_off', 'second_off'])]
        first_df  = team_df[team_df['home_off_line'] == 'first_off']
        second_df = team_df[team_df['home_off_line'] == 'second_off']
        xg_col = 'home_xg'
    else:
        team_df = df[df['away_team'] == team].copy()
        team_df = team_df[team_df['away_off_line'].isin(['first_off', 'second_off'])]
        first_df  = team_df[team_df['away_off_line'] == 'first_off']
        second_df = team_df[team_df['away_off_line'] == 'second_off']
        xg_col = 'away_xg'

    def xg60(subset, col):
        toi = subset['toi'].sum()
        xg  = subset[col].sum()
        return (xg / toi * 3600) if toi > 0 else 0.0

    first_xg60  = xg60(first_df, xg_col)
    second_xg60 = xg60(second_df, xg_col)
    first_toi   = first_df['toi'].sum()
    second_toi  = second_df['toi'].sum()

    return first_xg60, second_xg60, first_toi, second_toi


def compute_opponent_adjusted_xg60(df, team, is_home):
    """
    Opponent-adjusted xG/60: scale each line's rate by the average
    defensive quality they faced (opponent's xGA/60 when facing that line type).
    """
    first_xg60_raw, second_xg60_raw, first_toi, second_toi = compute_line_xg_per60(df, team, is_home)

    if is_home:
        team_df = df[df['home_team'] == team].copy()
        team_df = team_df[team_df['home_off_line'].isin(['first_off', 'second_off'])]
        opp_xga_col = 'away_xg'  # opponent allowed
        line_col = 'home_off_line'
    else:
        team_df = df[df['away_team'] == team].copy()
        team_df = team_df[team_df['away_off_line'].isin(['first_off', 'second_off'])]
        opp_xga_col = 'home_xg'
        line_col = 'away_off_line'

    # Average opponent xGA/60 when this team's first line was on ice
    def opp_def_quality(subset, col):
        toi = subset['toi'].sum()
        xg  = subset[col].sum()
        return (xg / toi * 3600) if toi > 0 else 1.0  # default: league avg

    first_sub  = team_df[team_df[line_col] == 'first_off']
    second_sub = team_df[team_df[line_col] == 'second_off']

    opp_def_first  = opp_def_quality(first_sub, opp_xga_col)
    opp_def_second = opp_def_quality(second_sub, opp_xga_col)

    # League average xGA/60 for calibration
    league_avg_xga60 = 2.2  # approximate from team_stats

    # Adjusted = raw * (league_avg / opp_xga_against_this_line)
    # Teams that face better defenses get upward adjustments
    adj_first  = first_xg60_raw  * (league_avg_xga60 / opp_def_first)  if opp_def_first > 0 else first_xg60_raw
    adj_second = second_xg60_raw * (league_avg_xga60 / opp_def_second) if opp_def_second > 0 else second_xg60_raw

    return adj_first, adj_second


def compute_gini_disparity(raw_df):
    """
    Main computation: Gini line disparity for all teams.
    Returns DataFrame with raw Gini, adjusted Gini, and disparity rank.
    """
    teams = sorted(raw_df['home_team'].unique().tolist())
    rows = []

    for team in teams:
        # Home games
        h_f60, h_s60, h_f_toi, h_s_toi = compute_line_xg_per60(raw_df, team, is_home=True)
        # Away games
        a_f60, a_s60, a_f_toi, a_s_toi = compute_line_xg_per60(raw_df, team, is_home=False)

        # Combined (TOI-weighted average across home + away)
        total_f_toi = h_f_toi + a_f_toi
        total_s_toi = h_s_toi + a_s_toi

        comb_first  = (h_f60 * h_f_toi + a_f60 * a_f_toi) / total_f_toi if total_f_toi > 0 else 0
        comb_second = (h_s60 * h_s_toi + a_s60 * a_s_toi) / total_s_toi if total_s_toi > 0 else 0

        # Raw Gini
        gini_raw = gini_two_values(comb_first, comb_second)

        # Ratio (first / second) — per competition requirement
        ratio = comb_first / comb_second if comb_second > 0 else float('inf')

        # Adjusted xG/60
        ha_f60, ha_s60 = compute_opponent_adjusted_xg60(raw_df, team, is_home=True)
        aa_f60, aa_s60 = compute_opponent_adjusted_xg60(raw_df, team, is_home=False)

        adj_first  = (ha_f60 * h_f_toi + aa_f60 * a_f_toi) / total_f_toi if total_f_toi > 0 else 0
        adj_second = (ha_s60 * h_s_toi + aa_s60 * a_s_toi) / total_s_toi if total_s_toi > 0 else 0
        gini_adj   = gini_two_values(adj_first, adj_second)

        rows.append({
            'team': team,
            'first_line_xg60': round(comb_first, 4),
            'second_line_xg60': round(comb_second, 4),
            'gini_raw': round(gini_raw, 4),
            'gini_adj': round(gini_adj, 4),
            'disparity_ratio': round(ratio, 4),
        })

    df = pd.DataFrame(rows)
    # Rank by adjusted Gini (descending — higher Gini = more disparity)
    df = df.sort_values('gini_adj', ascending=False).reset_index(drop=True)
    df['rank'] = range(1, len(df) + 1)
    df['score'] = df['gini_adj']
    return df


def main():
    log(f"=== {MODEL_NAME} STARTED ===")

    if not os.path.exists(DATA_FILE):
        log("ERROR: whl_2025.csv not found")
        return

    raw_df  = pd.read_csv(DATA_FILE)
    team_df = pd.read_csv(TEAM_FILE)
    log(f"Loaded {len(raw_df)} shift rows, {len(team_df)} teams")

    disparity_df = compute_gini_disparity(raw_df)

    log("Top 10 Teams by Gini Line Disparity (highest = most top-heavy):")
    log(disparity_df.head(10)[['rank', 'team', 'gini_raw', 'gini_adj', 'disparity_ratio']].to_string(index=False))

    os.makedirs(OUT_DIR, exist_ok=True)
    out_path = os.path.join(OUT_DIR, 'cc_method_gini_disparity.csv')
    disparity_df.to_csv(out_path, index=False)
    log(f"Saved: {out_path}")

    # Compute Spearman correlation between Gini disparity rank and team power rank
    cons_file = os.path.join(RANK_DIR, 'consensus_rankings.csv')
    if os.path.exists(cons_file):
        cons_df = pd.read_csv(cons_file)
        merged = disparity_df.merge(cons_df[['team', 'consensus_rank']], on='team', how='inner')
        rho, p = stats.spearmanr(merged['rank'], merged['consensus_rank'])
        log(f"Gini disparity rank vs. power rank Spearman rho={rho:.4f}, p={p:.4f}")
        if p < 0.05:
            direction = "NEGATIVE" if rho < 0 else "POSITIVE"
            log(f"  Significant {direction} correlation: more disparity → {'weaker' if rho > 0 else 'stronger'} teams")
        else:
            log("  No significant correlation between disparity and power rank (p >= 0.05)")

    log(f"=== {MODEL_NAME} COMPLETED ===")


if __name__ == '__main__':
    main()
