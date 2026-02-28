"""
Win Probability Agent — WHL 2025
Phase 1a: 5 methods for all 16 Round 1 matchups
"""
import os, datetime, warnings
import pandas as pd
import numpy as np
from scipy import optimize, stats
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.calibration import CalibratedClassifierCV
import warnings
warnings.filterwarnings('ignore')

np.random.seed(42)
LOG_FILE      = r"c:\Users\ryanz\Downloads\whardata\scratch\agent_log.txt"
OUT_DIR       = r"c:\Users\ryanz\Downloads\whardata\outputs"
GAME_FILE     = r"c:\Users\ryanz\Downloads\whardata\outputs\game_level.csv"
TEAM_FILE     = r"c:\Users\ryanz\Downloads\whardata\outputs\team_stats.csv"
MATCHUPS_FILE = r"c:\Users\ryanz\Downloads\whardata\WHSDSC_Rnd1_matchups - matchups.csv"
RANKINGS_DIR  = r"c:\Users\ryanz\Downloads\whardata\outputs\rankings"

def log(msg):
    ts = datetime.datetime.now().isoformat()
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"[WIN_PROB] {ts} | {msg}\n")
    print(msg)

def main():
    log("=== Win Probability Agent STARTED ===")
    game_df = pd.read_csv(GAME_FILE)
    team_df = pd.read_csv(TEAM_FILE)
    matchups = pd.read_csv(MATCHUPS_FILE)
    ts = team_df.set_index('team')
    
    log(f"Games: {len(game_df)}, Teams: {len(team_df)}, Matchups: {len(matchups)}")

    # ── Prep features for each game ───────────────────
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
                'home_win': g['home_win']
            })
        return pd.DataFrame(rows).fillna(0)
    
    feat_df = build_features(game_df, ts)
    X_raw = feat_df[['home_xgf60','home_xga60','away_xgf60','away_xga60']].values
    y     = feat_df['home_win'].values

    # ── Method 1: Logistic Regression ─────────────────
    log("Method 1: Logistic Regression")
    scaler = StandardScaler()
    X_s = scaler.fit_transform(X_raw)
    lr = LogisticRegression(max_iter=1000, random_state=42)
    lr.fit(X_s, y)
    in_sample_acc = (lr.predict(X_s) == y).mean()
    log(f"  In-sample accuracy: {in_sample_acc:.4f}")

    # ── Method 2: Elo-based ────────────────────────────
    log("Method 2: Elo-based Probability")
    elo_file = os.path.join(RANKINGS_DIR, "model_04_elo_ratings.csv")
    elo_df = pd.read_csv(elo_file).set_index('team')
    HOME_ADV = 100

    # ── Method 3: Bradley-Terry ────────────────────────
    log("Method 3: Bradley-Terry Probability")
    bt_file = os.path.join(RANKINGS_DIR, "model_06_bradley_terry.csv")
    bt_df = pd.read_csv(bt_file).set_index('team')
    # Empirical home advantage multiplier
    home_wins = game_df['home_win'].sum()
    home_adv_mult = (home_wins / len(game_df)) / 0.5  # ratio vs coin flip
    
    # ── Method 4: Pythagorean Log5 ────────────────────
    log("Method 4: Pythagorean Log5")
    pyth_file = os.path.join(RANKINGS_DIR, "model_03_pythagorean.csv")
    pyth_df = pd.read_csv(pyth_file).set_index('team')

    # ── Method 5: Monte Carlo ──────────────────────────
    log("Method 5: Monte Carlo Matchup Simulation")
    # Per-team xGF/xGA distributions from game_df
    team_dist = {}
    all_teams = set(game_df['home_team']) | set(game_df['away_team'])
    for team in all_teams:
        h = game_df[game_df['home_team']==team][['home_xg','away_xg']].rename(columns={'home_xg':'xgf','away_xg':'xga'})
        a = game_df[game_df['away_team']==team][['away_xg','home_xg']].rename(columns={'away_xg':'xgf','home_xg':'xga'})
        g = pd.concat([h,a])
        team_dist[team] = {'lam_f': max(g['xgf'].mean(),0.01), 'lam_a': max(g['xga'].mean(),0.01)}

    def mc_prob(home_team, away_team, n=10000, seed=42):
        rng = np.random.RandomState(seed)
        h_lam = team_dist.get(home_team, {'lam_f':2})['lam_f']
        a_lam = team_dist.get(away_team, {'lam_f':2})['lam_f']
        h_goals = rng.poisson(h_lam, n)
        a_goals = rng.poisson(a_lam, n)
        home_wins = (h_goals > a_goals).sum() + 0.5*(h_goals==a_goals).sum()
        return home_wins / n

    # ── Compute probabilities for all 16 matchups ─────
    results = []
    for _, row in matchups.iterrows():
        ht, at = row['home_team'], row['away_team']
        log(f"  Matchup {row['game']}: {ht} vs {at}")
        
        # Method 1: LR
        if ht in ts.index and at in ts.index:
            x_q = np.array([[ts.loc[ht,'es_xgf60'] or 0, ts.loc[ht,'es_xga60'] or 0,
                             ts.loc[at,'es_xgf60'] or 0, ts.loc[at,'es_xga60'] or 0]])
            x_qs = scaler.transform(x_q)
            p_lr = lr.predict_proba(x_qs)[0][1]
        else:
            p_lr = 0.5

        # Method 2: Elo
        if ht in elo_df.index and at in elo_df.index:
            h_elo = elo_df.loc[ht,'elo']
            a_elo = elo_df.loc[at,'elo']
            p_elo = 1 / (1 + 10**((a_elo - h_elo - HOME_ADV)/400))
        else:
            p_elo = 0.5
        
        # Method 3: Bradley-Terry
        if ht in bt_df.index and at in bt_df.index:
            h_str = bt_df.loc[ht,'bt_strength'] * home_adv_mult
            a_str = bt_df.loc[at,'bt_strength']
            p_bt = h_str / (h_str + a_str)
        else:
            p_bt = 0.5
        
        # Method 4: Log5 Pythagorean
        if ht in pyth_df.index and at in pyth_df.index:
            A = pyth_df.loc[ht,'pyth_winpct']
            B = pyth_df.loc[at,'pyth_winpct']
            p_log5 = (A - A*B) / (A + B - 2*A*B) if (A + B - 2*A*B) != 0 else 0.5
        else:
            p_log5 = 0.5
        
        # Method 5: Monte Carlo
        p_mc = mc_prob(ht, at)
        
        # Ensemble
        probs = [p_lr, p_elo, p_bt, p_log5, p_mc]
        p_ensemble = np.mean(probs)
        disagreement = max(probs) - min(probs)
        
        results.append({
            'game': row['game'], 'home_team': ht, 'away_team': at,
            'p_lr': round(p_lr,4), 'p_elo': round(p_elo,4),
            'p_bt': round(p_bt,4), 'p_log5': round(p_log5,4),
            'p_mc': round(p_mc,4), 'p_ensemble': round(p_ensemble,4),
            'disagreement': round(disagreement,4),
            'flag_disagree': 'YES' if disagreement > 0.10 else ''
        })
    
    results_df = pd.DataFrame(results)
    out_path = os.path.join(OUT_DIR, "win_probabilities.csv")
    results_df.to_csv(out_path, index=False)
    log(f"Win probabilities saved: {out_path}")
    
    # Summary stats
    log("\n=== Win Probability Summary ===")
    for _, r in results_df.iterrows():
        log(f"  Game {r['game']:2d}: {r['home_team']:15s} vs {r['away_team']:15s} | "
            f"LR={r['p_lr']:.3f} Elo={r['p_elo']:.3f} BT={r['p_bt']:.3f} "
            f"Log5={r['p_log5']:.3f} MC={r['p_mc']:.3f} | Ens={r['p_ensemble']:.3f} "
            f"{'⚠️ DISAGREE' if r['flag_disagree'] else ''}")
    
    flagged = results_df[results_df['flag_disagree']=='YES']
    log(f"\n{len(flagged)} matchups with >10pp model disagreement: {flagged['home_team'].tolist()}")
    
    log("=== Win Probability Agent COMPLETED ===")

if __name__ == '__main__':
    main()
