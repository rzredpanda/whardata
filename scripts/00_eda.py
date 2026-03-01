"""
EDA Agent — WHL 2025 Data Science Competition
Phase 0: Independent Exploratory Data Analysis
"""
import os, sys, datetime
import pandas as pd
import numpy as np
from scipy import stats

random_seed = 42
np.random.seed(random_seed)

LOG_FILE = r"c:\Users\ryanz\Downloads\whardata\scratch\agent_log.txt"
OUT_DIR  = r"c:\Users\ryanz\Downloads\whardata\outputs"
EDA_DIR  = r"c:\Users\ryanz\Downloads\whardata\outputs\eda_tables"
DATA_FILE= r"c:\Users\ryanz\Downloads\whardata\whl_2025.csv"

VISUALIZATIONS_ENABLED = False  # Hold until green light

def log(msg):
    ts = datetime.datetime.now().isoformat()
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"[EDA] {ts} | {msg}\n")
    print(msg)

def main():
    log("=== EDA Agent STARTED ===")
    
    # ── Load data ──────────────────────────────────────
    df = pd.read_csv(DATA_FILE)
    log(f"Data loaded: {df.shape[0]} rows × {df.shape[1]} cols")

    report_lines = []
    def rline(x=""):
        report_lines.append(str(x))
    
    rline("# WHL 2025 — EDA Report")
    rline(f"Generated: {datetime.datetime.now().isoformat()}")
    rline()
    
    # ── 1. Basic structure ─────────────────────────────
    rline("## 1. Dataset Structure")
    rline(f"- Shape: {df.shape}")
    rline(f"- Columns: {df.columns.tolist()}")
    rline(f"- Unique games: {df['game_id'].nunique()}")
    rline(f"- Records per game (mean): {df.groupby('game_id').size().mean():.2f}")
    rline()

    # ── 2. Missing values ──────────────────────────────
    rline("## 2. Missing Values")
    mv = df.isnull().sum()
    for col, cnt in mv.items():
        if cnt > 0:
            rline(f"  - {col}: {cnt} missing ({cnt/len(df)*100:.2f}%)")
    if mv.sum() == 0:
        rline("  - No missing values found.")
    rline()

    # ── 3. Categorical value counts ────────────────────
    rline("## 3. Categorical Fields")
    cats = ['home_off_line','home_def_pairing','away_off_line','away_def_pairing','went_ot']
    for c in cats:
        vc = df[c].value_counts()
        rline(f"### {c}")
        rline(vc.to_markdown())
        vc.to_csv(os.path.join(EDA_DIR, f"vc_{c}.csv"))
        rline()

    # ── 4. Numeric distributions ────────────────────────
    rline("## 4. Numeric Summary Statistics")
    nums = ['toi','home_xg','away_xg','home_goals','away_goals',
            'home_shots','away_shots','home_max_xg','away_max_xg',
            'home_assists','away_assists',
            'home_penalties_committed','home_penalty_minutes',
            'away_penalties_committed','away_penalty_minutes']
    num_summary = df[nums].describe().T
    num_summary['skew'] = df[nums].skew()
    rline(num_summary.to_markdown())
    num_summary.to_csv(os.path.join(EDA_DIR, "numeric_summary.csv"))
    rline()

    # ── 5. Game-level aggregation ──────────────────────
    rline("## 5. Game-Level Aggregated Stats")
    game_agg = df.groupby('game_id').agg(
        home_team=('home_team','first'),
        away_team=('away_team','first'),
        went_ot=('went_ot','first'),
        total_toi=('toi','sum'),
        home_goals=('home_goals','sum'),
        away_goals=('away_goals','sum'),
        home_xg=('home_xg','sum'),
        away_xg=('away_xg','sum'),
        home_shots=('home_shots','sum'),
        away_shots=('away_shots','sum'),
    ).reset_index()
    game_agg['home_win'] = (game_agg['home_goals'] > game_agg['away_goals']).astype(int)
    game_agg['goal_diff'] = game_agg['home_goals'] - game_agg['away_goals']
    rline(f"Games aggregated: {len(game_agg)}")
    rline(f"Home win rate: {game_agg['home_win'].mean():.4f}")
    rline(f"OT/SO rate: {game_agg['went_ot'].mean():.4f}")
    game_agg.to_csv(os.path.join(EDA_DIR, "game_level_eda.csv"), index=False)
    rline()

    # ── 6. Home advantage breakdown ────────────────────
    rline("## 6. Home Advantage Analysis")
    reg = game_agg[game_agg['went_ot']==0]
    ot  = game_agg[game_agg['went_ot']==1]
    rline(f"Overall home win rate: {game_agg['home_win'].mean():.4f}")
    rline(f"Regulation home win rate: {reg['home_win'].mean():.4f} (n={len(reg)})")
    rline(f"OT/SO home win rate: {ot['home_win'].mean():.4f} (n={len(ot)})")
    rline(f"Goal margin distribution:")
    gd = game_agg['goal_diff'].value_counts().sort_index()
    rline(gd.to_markdown())
    gd.to_csv(os.path.join(EDA_DIR, "goal_diff_dist.csv"))
    rline()

    # ── 7. xG vs actual goals correlation ─────────────
    rline("## 7. xG vs Actual Goals Correlation")
    xg_corr_home = game_agg['home_xg'].corr(game_agg['home_goals'])
    xg_corr_away = game_agg['away_xg'].corr(game_agg['away_goals'])
    rline(f"Home xG vs Home Goals Pearson r: {xg_corr_home:.4f}")
    rline(f"Away xG vs Away Goals Pearson r: {xg_corr_away:.4f}")
    all_xg   = pd.concat([game_agg['home_xg'],   game_agg['away_xg']])
    all_goals= pd.concat([game_agg['home_goals'], game_agg['away_goals']])
    rline(f"Combined xG vs Goals Pearson r: {all_xg.corr(all_goals):.4f}")
    rline()

    # ── 8. xG Calibration ─────────────────────────────
    rline("## 8. xG Calibration (does xG=1.0 → ~1 goal)")
    all_df = pd.concat([
        df[['home_xg','home_goals']].rename(columns={'home_xg':'xg','home_goals':'goals'}),
        df[['away_xg','away_goals']].rename(columns={'away_xg':'xg','away_goals':'goals'})
    ], ignore_index=True)
    all_df['xg_bin'] = pd.cut(all_df['xg'], bins=np.arange(0,3.5,0.25))
    cal = all_df.groupby('xg_bin',observed=True).agg(mean_xg=('xg','mean'), mean_goals=('goals','mean'), n=('goals','count')).reset_index()
    rline(cal.to_markdown())
    cal.to_csv(os.path.join(EDA_DIR, "xg_calibration.csv"), index=False)
    rline()

    # ── 9. Power play vs even-strength xG rates ────────
    rline("## 9. Power Play vs Even-Strength xG Rates")
    es = df[df['home_off_line'].isin(['first_off','second_off'])]
    pp = df[df['home_off_line'].isin(['PP_up'])]
    pk = df[df['home_off_line'].isin(['PP_kill_dwn'])]
    
    def xg60(subset, side='home'):
        col = f'{side}_xg'
        toi_col = 'toi'
        total_xg  = subset[col].sum()
        total_toi = subset[toi_col].sum()
        return (total_xg / total_toi * 3600) if total_toi > 0 else np.nan
    
    rline(f"Even-strength home xG/60: {xg60(es,'home'):.4f}")
    rline(f"Even-strength away xG/60: {xg60(es,'away'):.4f}")
    rline(f"PP (home up) home xG/60: {xg60(pp,'home'):.4f}")
    rline(f"PP kill (home down) away xG/60: {xg60(pk,'away'):.4f}")
    rline()

    # ── 10. Goalie GSAx ───────────────────────────────
    rline("## 10. Goalie Goals Saved Above Expected (GSAx)")
    # For home goalie: faced away xG, allowed away goals
    home_goalie = df.groupby('home_goalie').agg(
        xga=('away_xg','sum'),
        ga=('away_goals','sum'),
        toi=('toi','sum')
    ).reset_index()
    home_goalie.columns = ['goalie','xga','ga','toi']
    home_goalie['gsax'] = home_goalie['xga'] - home_goalie['ga']
    home_goalie['gsax_per60'] = home_goalie['gsax'] / home_goalie['toi'] * 3600
    
    away_goalie = df.groupby('away_goalie').agg(
        xga=('home_xg','sum'),
        ga=('home_goals','sum'),
        toi=('toi','sum')
    ).reset_index()
    away_goalie.columns = ['goalie','xga','ga','toi']
    away_goalie['gsax'] = away_goalie['xga'] - away_goalie['ga']
    away_goalie['gsax_per60'] = away_goalie['gsax'] / away_goalie['toi'] * 3600
    
    goalie_all = pd.concat([home_goalie, away_goalie]).groupby('goalie').agg(
        xga=('xga','sum'), ga=('ga','sum'), toi=('toi','sum')
    ).reset_index()
    goalie_all['gsax'] = goalie_all['xga'] - goalie_all['ga']
    goalie_all['gsax_per60'] = goalie_all['gsax'] / goalie_all['toi'] * 3600
    goalie_all = goalie_all.sort_values('gsax', ascending=False)
    
    rline(f"Goalies analyzed: {len(goalie_all)}")
    rline("Top 5 GSAx:")
    rline(goalie_all.head(5)[['goalie','xga','ga','gsax','gsax_per60']].to_markdown())
    rline("Bottom 5 GSAx:")
    rline(goalie_all.tail(5)[['goalie','xga','ga','gsax','gsax_per60']].to_markdown())
    goalie_all.to_csv(os.path.join(EDA_DIR, "goalie_gsax.csv"), index=False)
    rline()

    # ── 11. Penalty analysis ───────────────────────────
    rline("## 11. Penalty Analysis")
    pen_game = df.groupby('game_id').agg(
        home_penalties=('home_penalty_minutes','sum'),
        away_penalties=('away_penalty_minutes','sum'),
        home_win=('home_goals', lambda x: (x.sum() > df.loc[x.index,'away_goals'].sum()).astype(int)),
    ).reset_index()
    pen_game = pen_game.merge(game_agg[['game_id','home_win','home_goals','away_goals']], on='game_id', suffixes=('_x',''))
    rline(f"Penalty min vs home win corr: {pen_game['home_penalties'].corr(pen_game['home_win']):.4f}")
    rline(f"Penalty min vs away pen corr: {pen_game['home_penalties'].corr(pen_game['away_penalties']):.4f}")
    pen_game.to_csv(os.path.join(EDA_DIR, "penalty_analysis.csv"), index=False)
    rline()

    # ── 12. Season trends (first half vs second half) ──
    rline("## 12. Season Trends — First vs Second Half Games")
    game_ids = sorted(df['game_id'].unique())
    mid = len(game_ids) // 2
    first_half_ids = set(game_ids[:mid])
    second_half_ids = set(game_ids[mid:])
    df['half'] = df['game_id'].apply(lambda g: 'first' if g in first_half_ids else 'second')
    
    for team in sorted(df['home_team'].unique()):
        # home appearances
        team_rows = df[(df['home_team']==team) | (df['away_team']==team)].copy()
        team_rows['team_xg'] = np.where(team_rows['home_team']==team, team_rows['home_xg'], team_rows['away_xg'])
        h1 = team_rows[team_rows['half']=='first']['team_xg'].sum()
        h2 = team_rows[team_rows['half']=='second']['team_xg'].sum()
    
    half_summary = []
    for team in sorted(game_agg['home_team'].unique()):
        games_h1 = game_agg[((game_agg['home_team']==team)|(game_agg['away_team']==team)) & (game_agg['game_id'].isin(first_half_ids))]
        games_h2 = game_agg[((game_agg['home_team']==team)|(game_agg['away_team']==team)) & (game_agg['game_id'].isin(second_half_ids))]
        
        def team_stats_from_games(g, team):
            wins = sum((g['home_team']==team) & (g['home_win']==1)) + sum((g['away_team']==team) & (g['home_win']==0))
            return wins, len(g)
        
        w1, n1 = team_stats_from_games(games_h1, team)
        w2, n2 = team_stats_from_games(games_h2, team)
        half_summary.append({'team': team, 'wins_h1': w1, 'games_h1': n1, 'wins_h2': w2, 'games_h2': n2,
                              'winpct_h1': w1/n1 if n1>0 else np.nan, 'winpct_h2': w2/n2 if n2>0 else np.nan})
    
    half_df = pd.DataFrame(half_summary)
    half_df['trend'] = half_df['winpct_h2'] - half_df['winpct_h1']
    rline("Top 5 improvers (second half win% - first half win%):")
    rline(half_df.nlargest(5,'trend')[['team','winpct_h1','winpct_h2','trend']].to_markdown())
    rline("Top 5 decliners:")
    rline(half_df.nsmallest(5,'trend')[['team','winpct_h1','winpct_h2','trend']].to_markdown())
    half_df.to_csv(os.path.join(EDA_DIR, "season_trends.csv"), index=False)
    rline()

    # ── 13. Outlier detection ──────────────────────────
    rline("## 13. Outlier Detection")
    outlier_rows = df[df['toi'] > df['toi'].mean() + 3*df['toi'].std()]
    rline(f"Rows with TOI 3+ std above mean: {len(outlier_rows)}")
    high_xg = df[(df['home_xg'] > df['home_xg'].mean() + 3*df['home_xg'].std()) | 
                 (df['away_xg'] > df['away_xg'].mean() + 3*df['away_xg'].std())]
    rline(f"Rows with xG 3+ std above mean: {len(high_xg)}")
    outlier_rows.to_csv(os.path.join(EDA_DIR, "outlier_toi.csv"), index=False)
    high_xg.to_csv(os.path.join(EDA_DIR, "outlier_xg.csv"), index=False)
    rline()

    # ── 14. Line matchup frequency ─────────────────────
    rline("## 14. Line Matchup Frequency")
    matchup_freq = df.groupby(['home_off_line','away_def_pairing']).size().reset_index(name='count')
    matchup_freq = matchup_freq.sort_values('count', ascending=False)
    rline(matchup_freq.to_markdown())
    matchup_freq.to_csv(os.path.join(EDA_DIR, "matchup_frequency.csv"), index=False)
    rline()

    # ── 15. TOI distribution by line type ─────────────
    rline("## 15. TOI by Line Type")
    toi_by_line = df.groupby('home_off_line')['toi'].describe()
    rline(toi_by_line.to_markdown())
    toi_by_line.to_csv(os.path.join(EDA_DIR, "toi_by_line.csv"))
    rline()

    # ── 16. Team clustering by xGF/60 and xGA/60 ──────
    rline("## 16. Team Clustering (xGF/60, xGA/60)")
    es_rows = df[df['home_off_line'].isin(['first_off','second_off'])]
    
    team_xg_list = []
    all_teams = set(df['home_team'].unique()) | set(df['away_team'].unique())
    for team in sorted(all_teams):
        h = es_rows[es_rows['home_team']==team]
        a = es_rows[es_rows['away_team']==team]
        xgf = (h['home_xg'].sum() + a['away_xg'].sum())
        xga = (h['away_xg'].sum() + a['home_xg'].sum())
        toi_ = h['toi'].sum() + a['toi'].sum()
        if toi_ > 0:
            team_xg_list.append({'team': team, 'xgf60': xgf/toi_*3600, 'xga60': xga/toi_*3600,
                                  'xgd60': (xgf-xga)/toi_*3600})
    
    team_xg_df = pd.DataFrame(team_xg_list)
    rline(team_xg_df.sort_values('xgd60', ascending=False).to_markdown())
    team_xg_df.to_csv(os.path.join(EDA_DIR, "team_es_xg_rates.csv"), index=False)
    rline()

    # ── Save report ────────────────────────────────────
    report_path = os.path.join(OUT_DIR, "eda_report.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(report_lines))
    log(f"EDA report saved to {report_path}")
    log("=== EDA Agent COMPLETED ===")

if __name__ == '__main__':
    main()
