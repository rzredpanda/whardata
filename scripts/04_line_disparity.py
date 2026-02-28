"""
Line Disparity Agent — WHL 2025
Phase 1b: 10 methods to rank teams by first-line vs second-line disparity
"""
import os, datetime
import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.formula.api as smf
import warnings
warnings.filterwarnings('ignore')

np.random.seed(42)
LOG_FILE  = r"c:\Users\ryanz\Downloads\whardata\scratch\agent_log.txt"
OUT_DIR   = r"c:\Users\ryanz\Downloads\whardata\outputs\disparity"
DATA_FILE = r"c:\Users\ryanz\Downloads\whardata\whl_2025.csv"

def log(msg):
    ts = datetime.datetime.now().isoformat()
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"[DISPARITY] {ts} | {msg}\n")
    print(msg)

def save_disparity(df, method_num, method_name):
    fp = os.path.join(OUT_DIR, f"method_{method_num:02d}_{method_name}.csv")
    df.to_csv(fp, index=False)
    log(f"  Saved: {fp}")
    return fp

def main():
    log("=== Line Disparity Agent STARTED ===")
    df = pd.read_csv(DATA_FILE)
    
    # Filter to first_off and second_off only
    es = df[df['home_off_line'].isin(['first_off','second_off'])].copy()
    log(f"Even-strength rows: {len(es)}")
    
    all_teams = sorted(set(df['home_team']) | set(df['away_team']))
    
    def get_team_line_stats(team):
        """Return per-row xG data for a team split by first/second line."""
        h = es[es['home_team']==team].copy()
        h['xg_for'] = h['home_xg']; h['xg_against'] = h['away_xg']
        h['shots_for'] = h['home_shots']
        h['goals_for'] = h['home_goals']
        h['line_type'] = h['home_off_line']
        h['def_opp'] = h['away_def_pairing']
        
        a = es[es['away_team']==team].copy()
        a['xg_for'] = a['away_xg']; a['xg_against'] = a['home_xg']
        a['shots_for'] = a['away_shots']
        a['goals_for'] = a['away_goals']
        a['line_type'] = a['away_off_line']
        a['def_opp'] = a['home_def_pairing']
        
        return pd.concat([h[['toi','xg_for','xg_against','shots_for','goals_for','line_type','def_opp']],
                          a[['toi','xg_for','xg_against','shots_for','goals_for','line_type','def_opp']]])

    # ── Method 1: Raw xG Ratio ─────────────────────────
    log("Method 1: Raw xG Ratio")
    m1_rows = []
    for team in all_teams:
        td = get_team_line_stats(team)
        f1_xg = td[td['line_type']=='first_off']['xg_for'].sum()
        f2_xg = td[td['line_type']=='second_off']['xg_for'].sum()
        ratio = f1_xg / f2_xg if f2_xg > 0 else np.nan
        m1_rows.append({'team': team, 'f1_xg': round(f1_xg,3), 'f2_xg': round(f2_xg,3), 'ratio': round(ratio,4) if not np.isnan(ratio) else np.nan})
    m1 = pd.DataFrame(m1_rows).sort_values('ratio', ascending=False).reset_index(drop=True)
    m1['rank'] = range(1, len(m1)+1)
    save_disparity(m1[['rank','team','ratio','f1_xg','f2_xg']], 1, 'raw_xg_ratio')
    
    # ── Method 2: xG per 60 Ratio ─────────────────────
    log("Method 2: xG per 60 Ratio")
    m2_rows = []
    for team in all_teams:
        td = get_team_line_stats(team)
        f1 = td[td['line_type']=='first_off']
        f2 = td[td['line_type']=='second_off']
        f1_xg60 = (f1['xg_for'].sum() / f1['toi'].sum() * 3600) if f1['toi'].sum() > 0 else np.nan
        f2_xg60 = (f2['xg_for'].sum() / f2['toi'].sum() * 3600) if f2['toi'].sum() > 0 else np.nan
        ratio = f1_xg60 / f2_xg60 if (f2_xg60 and f2_xg60 > 0) else np.nan
        m2_rows.append({'team': team, 'f1_xg60': round(f1_xg60,4) if not np.isnan(f1_xg60) else np.nan,
                        'f2_xg60': round(f2_xg60,4) if not np.isnan(f2_xg60) else np.nan,
                        'ratio': round(ratio,4) if not (ratio is None or np.isnan(ratio)) else np.nan})
    m2 = pd.DataFrame(m2_rows).sort_values('ratio', ascending=False).reset_index(drop=True)
    m2['rank'] = range(1, len(m2)+1)
    save_disparity(m2[['rank','team','ratio','f1_xg60','f2_xg60']], 2, 'xg_per60_ratio')
    
    # ── Method 3: Matchup-Adjusted xG per 60 ──────────
    log("Method 3: Matchup-Adjusted xG per 60")
    # League-average xGA/60 by defensive pairing type
    def_avg = {}
    for def_type in es['home_def_pairing'].unique():
        # When home_def_pairing is this type, how much xG does the away offense generate?
        sub = es[es['home_def_pairing']==def_type]
        toi_ = sub['toi'].sum()
        xga_ = sub['away_xg'].sum()
        def_avg[def_type] = xga_ / toi_ * 3600 if toi_ > 0 else np.nan
    league_avg_def = np.nanmean(list(def_avg.values()))
    log(f"  League avg def xGA/60: {league_avg_def:.4f}")
    
    m3_rows = []
    for team in all_teams:
        td = get_team_line_stats(team)
        adj_xg_list = {'first_off': [], 'second_off': []}
        toi_list    = {'first_off': [], 'second_off': []}
        for _, row in td.iterrows():
            lt = row['line_type']
            if lt not in ['first_off','second_off']:
                continue
            opp_def_xga60 = def_avg.get(row['def_opp'], league_avg_def) or league_avg_def
            adj_factor = league_avg_def / opp_def_xga60 if opp_def_xga60 > 0 else 1.0
            adj_xg = row['xg_for'] * adj_factor
            adj_xg_list[lt].append(adj_xg)
            toi_list[lt].append(row['toi'])
        
        f1_adj60 = sum(adj_xg_list['first_off'])  / sum(toi_list['first_off'])  * 3600 if sum(toi_list['first_off'])  > 0 else np.nan
        f2_adj60 = sum(adj_xg_list['second_off']) / sum(toi_list['second_off']) * 3600 if sum(toi_list['second_off']) > 0 else np.nan
        ratio = f1_adj60 / f2_adj60 if (f2_adj60 and f2_adj60 > 0) else np.nan
        m3_rows.append({'team': team, 'f1_adj_xg60': round(f1_adj60,4) if not np.isnan(f1_adj60) else np.nan,
                        'f2_adj_xg60': round(f2_adj60,4) if not np.isnan(f2_adj60) else np.nan,
                        'ratio': round(ratio,4) if not (ratio is None or np.isnan(ratio)) else np.nan})
    m3 = pd.DataFrame(m3_rows).sort_values('ratio', ascending=False).reset_index(drop=True)
    m3['rank'] = range(1, len(m3)+1)
    save_disparity(m3[['rank','team','ratio','f1_adj_xg60','f2_adj_xg60']], 3, 'matchup_adj_xg60')
    
    # ── Method 4: Goals per 60 Ratio ──────────────────
    log("Method 4: Goals per 60 Ratio")
    m4_rows = []
    for team in all_teams:
        td = get_team_line_stats(team)
        f1 = td[td['line_type']=='first_off']
        f2 = td[td['line_type']=='second_off']
        f1_g60 = (f1['goals_for'].sum() / f1['toi'].sum() * 3600) if f1['toi'].sum() > 0 else np.nan
        f2_g60 = (f2['goals_for'].sum() / f2['toi'].sum() * 3600) if f2['toi'].sum() > 0 else np.nan
        ratio = f1_g60 / f2_g60 if (f2_g60 and f2_g60 > 0) else np.nan
        m4_rows.append({'team': team, 'f1_g60': round(f1_g60,4) if not np.isnan(f1_g60) else np.nan,
                        'f2_g60': round(f2_g60,4) if not np.isnan(f2_g60) else np.nan,
                        'ratio': round(ratio,4) if not (ratio is None or np.isnan(ratio)) else np.nan})
    m4 = pd.DataFrame(m4_rows).sort_values('ratio', ascending=False).reset_index(drop=True)
    m4['rank'] = range(1, len(m4)+1)
    save_disparity(m4[['rank','team','ratio','f1_g60','f2_g60']], 4, 'goals_per60_ratio')
    
    # ── Method 5: Shots per 60 Ratio ──────────────────
    log("Method 5: Shots per 60 Ratio")
    m5_rows = []
    for team in all_teams:
        td = get_team_line_stats(team)
        f1 = td[td['line_type']=='first_off']
        f2 = td[td['line_type']=='second_off']
        f1_s60 = (f1['shots_for'].sum() / f1['toi'].sum() * 3600) if f1['toi'].sum() > 0 else np.nan
        f2_s60 = (f2['shots_for'].sum() / f2['toi'].sum() * 3600) if f2['toi'].sum() > 0 else np.nan
        ratio = f1_s60 / f2_s60 if (f2_s60 and f2_s60 > 0) else np.nan
        m5_rows.append({'team': team, 'f1_s60': round(f1_s60,4) if not np.isnan(f1_s60) else np.nan,
                        'f2_s60': round(f2_s60,4) if not np.isnan(f2_s60) else np.nan,
                        'ratio': round(ratio,4) if not (ratio is None or np.isnan(ratio)) else np.nan})
    m5 = pd.DataFrame(m5_rows).sort_values('ratio', ascending=False).reset_index(drop=True)
    m5['rank'] = range(1, len(m5)+1)
    save_disparity(m5[['rank','team','ratio','f1_s60','f2_s60']], 5, 'shots_per60_ratio')
    
    # ── Method 6: xG Share ─────────────────────────────
    log("Method 6: xG Share (Proportion Method)")
    m6_rows = []
    for team in all_teams:
        td = get_team_line_stats(team)
        f1_xg = td[td['line_type']=='first_off']['xg_for'].sum()
        f2_xg = td[td['line_type']=='second_off']['xg_for'].sum()
        total = f1_xg + f2_xg
        share = f1_xg / total if total > 0 else np.nan
        disparity = abs(share - 0.5) if not np.isnan(share) else np.nan  # distance from balanced
        m6_rows.append({'team': team, 'f1_xg_share': round(share,4) if not np.isnan(share) else np.nan,
                        'disparity_from_05': round(disparity,4) if not np.isnan(disparity) else np.nan})
    m6 = pd.DataFrame(m6_rows).sort_values('disparity_from_05', ascending=False).reset_index(drop=True)
    m6['rank'] = range(1, len(m6)+1)
    m6['ratio'] = m6['disparity_from_05']
    save_disparity(m6[['rank','team','ratio','f1_xg_share','disparity_from_05']], 6, 'xg_share_proportion')
    
    # ── Method 7: Z-Score Gap ─────────────────────────
    log("Method 7: Z-Score Gap")
    # Compute xG/60 for every team-line combination
    all_lines = []
    for team in all_teams:
        td = get_team_line_stats(team)
        for lt in ['first_off','second_off']:
            sub = td[td['line_type']==lt]
            if sub['toi'].sum() > 0:
                xg60 = sub['xg_for'].sum() / sub['toi'].sum() * 3600
                all_lines.append({'team': team, 'line': lt, 'xg60': xg60})
    all_lines_df = pd.DataFrame(all_lines)
    league_mean = all_lines_df['xg60'].mean()
    league_std  = all_lines_df['xg60'].std()
    all_lines_df['z'] = (all_lines_df['xg60'] - league_mean) / league_std
    
    m7_rows = []
    for team in all_teams:
        f1_z = all_lines_df[(all_lines_df['team']==team) & (all_lines_df['line']=='first_off')]['z']
        f2_z = all_lines_df[(all_lines_df['team']==team) & (all_lines_df['line']=='second_off')]['z']
        if len(f1_z) > 0 and len(f2_z) > 0:
            gap = float(f1_z.values[0]) - float(f2_z.values[0])
            m7_rows.append({'team': team, 'z_first': round(float(f1_z.values[0]),4),
                            'z_second': round(float(f2_z.values[0]),4), 'z_gap': round(gap,4)})
        else:
            m7_rows.append({'team': team, 'z_first': np.nan, 'z_second': np.nan, 'z_gap': np.nan})
    m7 = pd.DataFrame(m7_rows).sort_values('z_gap', ascending=False).reset_index(drop=True)
    m7['rank'] = range(1, len(m7)+1)
    m7['ratio'] = m7['z_gap']
    save_disparity(m7[['rank','team','ratio','z_first','z_second','z_gap']], 7, 'zscore_gap')
    
    # ── Method 8: Regression-Based Line Effect ─────────
    log("Method 8: Regression-Based Line Effect")
    # OLS: xg_per60 ~ line_type + team + opponent_def_quality
    reg_rows = []
    for team in all_teams:
        td = get_team_line_stats(team)
        for _, row in td.iterrows():
            opp_def_xga60 = def_avg.get(row['def_opp'], league_avg_def) or league_avg_def
            xg60 = row['xg_for'] / row['toi'] * 3600 if row['toi'] > 0 else np.nan
            if not np.isnan(xg60):
                reg_rows.append({
                    'team': team, 'line_type': row['line_type'],
                    'is_first_off': 1 if row['line_type']=='first_off' else 0,
                    'opp_def_xga60': opp_def_xga60, 'xg60': xg60
                })
    reg_df = pd.DataFrame(reg_rows)
    
    try:
        import statsmodels.formula.api as smf
        model = smf.ols("xg60 ~ is_first_off + opp_def_xga60 + C(team)", data=reg_df).fit()
        # Coefficient on is_first_off = effect of being first line vs second, controlling for team and def quality
        first_line_coef = model.params.get('is_first_off', np.nan)
        log(f"  Regression first_off coefficient: {first_line_coef:.4f}")
        
        # Team-specific effects (interaction): rerun with interaction
        model2 = smf.ols("xg60 ~ is_first_off * C(team) + opp_def_xga60", data=reg_df).fit(disp=0)
        
        m8_rows = []
        for team in all_teams:
            # Main effect + interaction
            main = model.params.get('is_first_off', 0)
            inter_key = f"is_first_off:C(team)[T.{team}]"
            inter = model2.params.get(inter_key, 0)
            gap = main + inter
            m8_rows.append({'team': team, 'reg_gap': round(gap, 4)})
        m8 = pd.DataFrame(m8_rows).sort_values('reg_gap', ascending=False).reset_index(drop=True)
        m8['rank'] = range(1, len(m8)+1)
        m8['ratio'] = m8['reg_gap']
        save_disparity(m8[['rank','team','ratio','reg_gap']], 8, 'regression_line_effect')
    except Exception as e:
        log(f"  Regression failed: {e}. Falling back to z-gap method.")
        m8 = m7.copy()
        m8.to_csv(os.path.join(OUT_DIR, "method_08_regression_line_effect.csv"), index=False)
    
    # ── Method 9: TOI-Weighted Line Quality ───────────
    log("Method 9: TOI-Weighted Line Quality")
    m9_rows = []
    for team in all_teams:
        td = get_team_line_stats(team)
        for_lines = {'first_off': [], 'second_off': []}
        for _, row in td.iterrows():
            lt = row['line_type']
            if lt in for_lines and row['toi'] > 0:
                per60 = row['xg_for'] / row['toi'] * 3600
                for_lines[lt].append((per60, row['toi']))
        
        def toi_weighted_avg(pairs):
            if not pairs: return np.nan
            vals, wts = zip(*pairs)
            return np.average(vals, weights=wts)
        
        f1_w = toi_weighted_avg(for_lines['first_off'])
        f2_w = toi_weighted_avg(for_lines['second_off'])
        ratio = f1_w / f2_w if (f2_w and f2_w > 0) else np.nan
        m9_rows.append({'team': team, 'f1_toi_wt_xg60': round(f1_w,4) if not np.isnan(f1_w) else np.nan,
                        'f2_toi_wt_xg60': round(f2_w,4) if not np.isnan(f2_w) else np.nan,
                        'ratio': round(ratio,4) if not (ratio is None or np.isnan(ratio)) else np.nan})
    m9 = pd.DataFrame(m9_rows).sort_values('ratio', ascending=False).reset_index(drop=True)
    m9['rank'] = range(1, len(m9)+1)
    save_disparity(m9[['rank','team','ratio','f1_toi_wt_xg60','f2_toi_wt_xg60']], 9, 'toi_weighted_quality')
    
    # ── Method 10: Bootstrap CI ───────────────────────
    log("Method 10: Bootstrap Confidence Interval")
    rng = np.random.RandomState(42)
    N_BOOT = 1000
    game_ids = sorted(df['game_id'].unique())
    m10_rows = []
    
    for team in all_teams:
        boot_ratios = []
        team_es = es[(es['home_team']==team) | (es['away_team']==team)].copy()
        team_games = list(set(team_es['game_id'].unique()))
        
        if len(team_games) < 5:
            m10_rows.append({'team': team, 'boot_mean': np.nan, 'boot_lo': np.nan,
                             'boot_hi': np.nan, 'boot_ci_width': np.nan})
            continue
        
        for _ in range(N_BOOT):
            sampled_games = rng.choice(team_games, size=len(team_games), replace=True)
            boot_es = team_es[team_es['game_id'].isin(sampled_games)]
            h = boot_es[boot_es['home_team']==team]
            a = boot_es[boot_es['away_team']==team]
            
            f1_xg  = h[h['home_off_line']=='first_off']['home_xg'].sum() + a[a['away_off_line']=='first_off']['away_xg'].sum()
            f2_xg  = h[h['home_off_line']=='second_off']['home_xg'].sum() + a[a['away_off_line']=='second_off']['away_xg'].sum()
            f1_toi = h[h['home_off_line']=='first_off']['toi'].sum() + a[a['away_off_line']=='first_off']['toi'].sum()
            f2_toi = h[h['home_off_line']=='second_off']['toi'].sum() + a[a['away_off_line']=='second_off']['toi'].sum()
            
            f1_60 = f1_xg/f1_toi*3600 if f1_toi > 0 else np.nan
            f2_60 = f2_xg/f2_toi*3600 if f2_toi > 0 else np.nan
            if f2_60 and f2_60 > 0 and not np.isnan(f1_60):
                boot_ratios.append(f1_60/f2_60)
        
        if boot_ratios:
            arr = np.array(boot_ratios)
            m10_rows.append({'team': team, 'boot_mean': round(arr.mean(),4),
                             'boot_lo': round(np.percentile(arr,2.5),4),
                             'boot_hi': round(np.percentile(arr,97.5),4),
                             'boot_ci_width': round(np.percentile(arr,97.5)-np.percentile(arr,2.5),4)})
        else:
            m10_rows.append({'team': team, 'boot_mean': np.nan, 'boot_lo': np.nan,
                             'boot_hi': np.nan, 'boot_ci_width': np.nan})
    
    m10 = pd.DataFrame(m10_rows).dropna(subset=['boot_mean']).sort_values('boot_mean', ascending=False).reset_index(drop=True)
    m10['rank'] = range(1, len(m10)+1)
    m10['ratio'] = m10['boot_mean']
    m10['flag_wide_ci'] = (m10['boot_ci_width'] > m10['boot_ci_width'].quantile(0.75)).map({True:'WIDE', False:''})
    save_disparity(m10[['rank','team','ratio','boot_mean','boot_lo','boot_hi','boot_ci_width','flag_wide_ci']], 10, 'bootstrap_ci_ratio')
    
    # ── Consensus Ranking ─────────────────────────────
    log("Computing consensus ranking...")
    all_methods = [m1, m2, m3, m4, m5, m6, m7, m8, m9]
    method_names = ['raw_xg','xg60','adj_xg60','goals60','shots60','xg_share','z_gap','regression','toi_wt']
    
    consensus = pd.DataFrame({'team': all_teams})
    for m, name in zip(all_methods, method_names):
        rank_map = m.set_index('team')['rank']
        consensus[f'rank_{name}'] = consensus['team'].map(rank_map)
    # Add method 10
    rank_m10 = m10.set_index('team')['rank']
    consensus['rank_bootstrap'] = consensus['team'].map(rank_m10)
    
    rank_cols = [f'rank_{n}' for n in method_names] + ['rank_bootstrap']
    consensus['mean_rank'] = consensus[rank_cols].mean(axis=1)
    consensus['rank_variance'] = consensus[rank_cols].var(axis=1)
    consensus['consensus_rank'] = consensus['mean_rank'].rank().astype(int)
    consensus = consensus.sort_values('mean_rank').reset_index(drop=True)
    
    top10 = consensus.head(10)
    log("\n=== TOP 10 TEAMS BY LINE DISPARITY (Consensus) ===")
    for _, r in top10.iterrows():
        log(f"  Rank {r['consensus_rank']:2d}: {r['team']} (mean rank={r['mean_rank']:.2f}, variance={r['rank_variance']:.1f})")
    
    consensus.to_csv(os.path.join(OUT_DIR, "consensus_disparity.csv"), index=False)
    top10.to_csv(os.path.join(OUT_DIR, "top10_disparity.csv"), index=False)
    log("Consensus disparity saved.")
    log("=== Line Disparity Agent COMPLETED ===")

if __name__ == '__main__':
    main()
