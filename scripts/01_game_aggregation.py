"""
Game Aggregation Agent — WHL 2025
Builds canonical game-level and team-level summary tables
"""
import os, datetime
import pandas as pd
import numpy as np

np.random.seed(42)
LOG_FILE  = r"c:\Users\ryanz\Downloads\whardata\scratch\agent_log.txt"
OUT_DIR   = r"c:\Users\ryanz\Downloads\whardata\outputs"
DATA_FILE = r"c:\Users\ryanz\Downloads\whardata\whl_2025.csv"

def log(msg):
    ts = datetime.datetime.now().isoformat()
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"[GAME_AGG] {ts} | {msg}\n")
    print(msg)

def main():
    log("=== Game Aggregation Agent STARTED ===")
    df = pd.read_csv(DATA_FILE)
    log(f"Loaded {df.shape[0]} rows")

    # ── 1. Game-level table ───────────────────────────
    game_df = df.groupby('game_id').agg(
        home_team=('home_team','first'),
        away_team=('away_team','first'),
        went_ot=('went_ot','first'),
        home_goals=('home_goals','sum'),
        away_goals=('away_goals','sum'),
        home_xg=('home_xg','sum'),
        away_xg=('away_xg','sum'),
        home_shots=('home_shots','sum'),
        away_shots=('away_shots','sum'),
        home_assists=('home_assists','sum'),
        away_assists=('away_assists','sum'),
        home_penalties_min=('home_penalty_minutes','sum'),
        away_penalties_min=('away_penalty_minutes','sum'),
        home_penalties_committed=('home_penalties_committed','sum'),
        away_penalties_committed=('away_penalties_committed','sum'),
        total_toi=('toi','sum'),
    ).reset_index()

    # Sort by game_id numerically
    game_df['game_num'] = game_df['game_id'].str.extract(r'(\d+)').astype(int)
    game_df = game_df.sort_values('game_num').reset_index(drop=True)

    game_df['home_win']  = (game_df['home_goals'] > game_df['away_goals']).astype(int)
    game_df['goal_diff'] = game_df['home_goals'] - game_df['away_goals']
    game_df['xg_diff']   = game_df['home_xg']    - game_df['away_xg']
    log(f"Game-level table: {len(game_df)} games")

    # ── 2. Even-strength line data ────────────────────
    es = df[df['home_off_line'].isin(['first_off','second_off'])]
    es_home = es.groupby(['game_id','home_team']).agg(
        es_home_xg=('home_xg','sum'), es_home_shots=('home_shots','sum'),
        es_away_xg=('away_xg','sum'), es_away_shots=('away_shots','sum'),
        es_toi=('toi','sum')
    ).reset_index().rename(columns={'home_team':'team'})
    es_away = es.groupby(['game_id','away_team']).agg(
        es_away_xg_f=('away_xg','sum'), es_away_shots_f=('away_shots','sum'),
        es_home_xg_a=('home_xg','sum'), es_home_shots_a=('home_shots','sum'),
        es_toi_a=('toi','sum')
    ).reset_index().rename(columns={'away_team':'team'})

    # ── 3. PP/PK data ─────────────────────────────────
    pp_rows = df[df['home_off_line']=='PP_up']
    pk_rows = df[df['home_off_line']=='PP_kill_dwn']

    pp_home = pp_rows.groupby(['game_id','home_team']).agg(
        pp_xgf=('home_xg','sum'), pp_toi=('toi','sum')
    ).reset_index().rename(columns={'home_team':'team'})
    pk_home = pk_rows.groupby(['game_id','home_team']).agg(
        pk_xga=('away_xg','sum'), pk_toi=('toi','sum')
    ).reset_index().rename(columns={'home_team':'team'})

    # ── 4. Goalie GSAx per game ───────────────────────
    # home goalie faced away shots
    hg = df.groupby(['game_id','home_goalie']).agg(
        xga=('away_xg','sum'), ga=('away_goals','sum'), toi=('toi','sum')
    ).reset_index().rename(columns={'home_goalie':'goalie'})
    ag = df.groupby(['game_id','away_goalie']).agg(
        xga=('home_xg','sum'), ga=('home_goals','sum'), toi=('toi','sum')
    ).reset_index().rename(columns={'away_goalie':'goalie'})

    # ── 5. Team-season stats ──────────────────────────
    all_teams = sorted(set(game_df['home_team'].unique()) | set(game_df['away_team'].unique()))
    team_rows = []
    
    for team in all_teams:
        h_games = game_df[game_df['home_team']==team].copy()
        a_games = game_df[game_df['away_team']==team].copy()
        
        n_games = len(h_games) + len(a_games)
        wins  = h_games['home_win'].sum()      + (1 - a_games['home_win']).sum()
        losses_reg = ((h_games['home_win']==0) & (h_games['went_ot']==0)).sum() + \
                     ((a_games['home_win']==1) & (a_games['went_ot']==0)).sum()
        ot_loss = ((h_games['home_win']==0) & (h_games['went_ot']==1)).sum() + \
                  ((a_games['home_win']==1) & (a_games['went_ot']==1)).sum()
        points = 2*wins + ot_loss
        
        gf = h_games['home_goals'].sum() + a_games['away_goals'].sum()
        ga = h_games['away_goals'].sum() + a_games['home_goals'].sum()
        xgf = h_games['home_xg'].sum() + a_games['away_xg'].sum()
        xga = h_games['away_xg'].sum() + a_games['home_xg'].sum()
        sf  = h_games['home_shots'].sum() + a_games['away_shots'].sum()
        sa  = h_games['away_shots'].sum() + a_games['home_shots'].sum()
        pen_min = h_games['home_penalties_min'].sum() + a_games['away_penalties_min'].sum()
        
        # Even-strength per-60
        es_team_h = es[es['home_team']==team]
        es_team_a = es[es['away_team']==team]
        es_toi = es_team_h['toi'].sum() + es_team_a['toi'].sum()
        es_xgf = es_team_h['home_xg'].sum() + es_team_a['away_xg'].sum()
        es_xga = es_team_h['away_xg'].sum() + es_team_a['home_xg'].sum()
        es_xgf60 = (es_xgf / es_toi * 3600) if es_toi > 0 else np.nan
        es_xga60 = (es_xga / es_toi * 3600) if es_toi > 0 else np.nan
        
        # PP
        pp_team_h = pp_rows[pp_rows['home_team']==team]
        pp_team_a = pp_rows[pp_rows['away_team']==team]  # when away and PP_up would be away_off_line
        pp_toi = pp_team_h['toi'].sum()
        pp_xgf = pp_team_h['home_xg'].sum()
        pp_xgf60 = (pp_xgf / pp_toi * 3600) if pp_toi > 0 else np.nan
        
        # PK — home team killing penalty (PP_kill_dwn)
        pk_team_h = pk_rows[pk_rows['home_team']==team]
        pk_toi = pk_team_h['toi'].sum()
        pk_xga_val = pk_team_h['away_xg'].sum()  # opposition xg while team kills
        pk_xga60 = (pk_xga_val / pk_toi * 3600) if pk_toi > 0 else np.nan
        
        # Goalie GSAx for team's goalie
        team_goalie_h = hg[hg['game_id'].isin(h_games['game_id'])]
        team_goalie_a = ag[ag['game_id'].isin(a_games['game_id'])]
        gsax = (team_goalie_h['xga'].sum() - team_goalie_h['ga'].sum() +
                team_goalie_a['xga'].sum() - team_goalie_a['ga'].sum())
        goalie_toi = team_goalie_h['toi'].sum() + team_goalie_a['toi'].sum()
        gsax60 = (gsax / goalie_toi * 3600) if goalie_toi > 0 else np.nan
        
        # Save%
        sav = sa - ga
        save_pct = sav / sa if sa > 0 else np.nan
        
        team_rows.append({
            'team': team, 'games': n_games, 'wins': int(wins), 'losses_reg': int(losses_reg),
            'ot_losses': int(ot_loss), 'points': int(points),
            'gf': int(gf), 'ga': int(ga), 'gd': int(gf-ga),
            'xgf': round(xgf,3), 'xga': round(xga,3), 'xgd': round(xgf-xga,3),
            'xgf_per_game': round(xgf/n_games,3) if n_games>0 else np.nan,
            'xga_per_game': round(xga/n_games,3) if n_games>0 else np.nan,
            'shots_for': int(sf), 'shots_against': int(sa),
            'save_pct': round(save_pct,4) if not np.isnan(save_pct) else np.nan,
            'es_toi': round(es_toi,1), 'es_xgf': round(es_xgf,3), 'es_xga': round(es_xga,3),
            'es_xgf60': round(es_xgf60,4) if not np.isnan(es_xgf60) else np.nan,
            'es_xga60': round(es_xga60,4) if not np.isnan(es_xga60) else np.nan,
            'es_xgd60': round(es_xgf60-es_xga60,4) if not (np.isnan(es_xgf60) or np.isnan(es_xga60)) else np.nan,
            'pp_xgf60': round(pp_xgf60,4) if not np.isnan(pp_xgf60) else np.nan,
            'pk_xga60': round(pk_xga60,4) if not np.isnan(pk_xga60) else np.nan,
            'gsax': round(gsax,3), 'gsax60': round(gsax60,4) if not np.isnan(gsax60) else np.nan,
            'pen_min': int(pen_min),
            'win_pct': round(wins/n_games,4) if n_games>0 else np.nan,
        })
    
    team_df = pd.DataFrame(team_rows).sort_values('points', ascending=False).reset_index(drop=True)
    team_df['rank_points'] = range(1, len(team_df)+1)
    
    # Save outputs
    game_df.to_csv(os.path.join(OUT_DIR, "game_level.csv"), index=False)
    team_df.to_csv(os.path.join(OUT_DIR, "team_stats.csv"), index=False)
    log(f"game_level.csv saved: {len(game_df)} rows")
    log(f"team_stats.csv saved: {len(team_df)} teams")
    log("=== Game Aggregation Agent COMPLETED ===")

if __name__ == '__main__':
    main()
