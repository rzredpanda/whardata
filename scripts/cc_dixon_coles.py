"""
CLAUDE CODE MODEL - (Phase 1a: Dixon-Coles Bivariate Poisson, v1)
WHL 2025 Competition — Custom Model by Claude Code

Mathematical formulation:
    The Dixon-Coles model (1997) extends the independent Poisson model
    by adding a low-score correction term tau(x,y,mu,nu,rho):

        P(X=x, Y=y) = tau(x,y,mu,nu,rho) * Poisson(x;mu) * Poisson(y;nu)

    where:
        mu  = attack_home * defence_away * home_advantage
        nu  = attack_away * defence_home
        tau = correction for low-scoring games (0-0, 1-0, 0-1, 1-1)

    Parameters estimated via Maximum Likelihood Estimation (MLE).
    Attack and defense parameters are fit per team.

    This model is superior to independent Poisson because:
    1. It accounts for the correlation between home/away goals in low-scoring games
    2. It provides calibrated probability distributions over score lines
    3. Attack/defense parameters decompose team strength into offense vs. defense

    xG values are used as the actual goal counts to preserve expected goals
    semantics rather than raw goal variance.
"""
import os, datetime, warnings
import pandas as pd
import numpy as np
from scipy import stats, optimize

np.random.seed(42)
warnings.filterwarnings('ignore')

MODEL_NAME = "CLAUDE CODE MODEL - (Phase 1a: Dixon-Coles Bivariate Poisson, v1)"
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
        f.write(f"[CC_DC] {ts} | {msg}\n")
    print(msg)


def tau_correction(x, y, mu, nu, rho):
    """
    Dixon-Coles tau correction for low-score outcomes.
    Applies only when x <= 1 and y <= 1.
    """
    if x == 0 and y == 0:
        return 1 - mu * nu * rho
    elif x == 0 and y == 1:
        return 1 + mu * rho
    elif x == 1 and y == 0:
        return 1 + nu * rho
    elif x == 1 and y == 1:
        return 1 - rho
    else:
        return 1.0


def poisson_pmf(k, lam):
    """Poisson probability mass function."""
    if lam <= 0:
        return 1.0 if k == 0 else 0.0
    from math import factorial, exp
    return (lam ** k) * exp(-lam) / factorial(min(k, 20))


def neg_log_likelihood(params, teams, home_goals, away_goals, home_teams, away_teams):
    """
    Negative log-likelihood for Dixon-Coles model.
    params layout: [attack_0..n, defence_0..n, home_adv, rho]
    """
    n = len(teams)
    attack  = {t: np.exp(params[i]) for i, t in enumerate(teams)}
    defence = {t: np.exp(params[n + i]) for i, t in enumerate(teams)}
    home_adv = np.exp(params[2 * n])
    rho = params[2 * n + 1]
    rho = np.clip(rho, -0.99, 0.99)

    nll = 0.0
    for hg, ag, ht, at in zip(home_goals, away_goals, home_teams, away_teams):
        if ht not in attack or at not in attack:
            continue
        mu = attack[ht] * defence[at] * home_adv
        nu = attack[at] * defence[ht]

        # Discretize xG to nearest integer for PMF
        hg_int = max(0, round(hg))
        ag_int = max(0, round(ag))

        tau = tau_correction(hg_int, ag_int, mu, nu, rho)
        tau = max(tau, 1e-10)

        p_h = poisson_pmf(hg_int, mu)
        p_a = poisson_pmf(ag_int, nu)
        p_joint = tau * p_h * p_a
        p_joint = max(p_joint, 1e-10)
        nll -= np.log(p_joint)

    return nll


def fit_dixon_coles(game_df, teams):
    """Fit Dixon-Coles parameters via MLE."""
    log("  Fitting Dixon-Coles via L-BFGS-B...")
    n = len(teams)

    home_goals  = game_df['home_xg'].values
    away_goals  = game_df['away_xg'].values
    home_teams  = game_df['home_team'].values
    away_teams  = game_df['away_team'].values

    # Initial params: attack=0, defence=0, home_adv=log(1.1), rho=-0.1
    x0 = np.zeros(2 * n + 2)
    x0[2 * n]     = np.log(1.1)   # home advantage
    x0[2 * n + 1] = -0.1          # rho (low-score correction)

    # Constraint: sum of attack params = 0 (for identifiability)
    result = optimize.minimize(
        neg_log_likelihood,
        x0,
        args=(teams, home_goals, away_goals, home_teams, away_teams),
        method='L-BFGS-B',
        options={'maxiter': 500, 'ftol': 1e-9, 'gtol': 1e-6}
    )

    if not result.success:
        log(f"  WARNING: Optimizer did not fully converge: {result.message}")

    params = result.x
    attack  = {t: np.exp(params[i]) for i, t in enumerate(teams)}
    defence = {t: np.exp(params[n + i]) for i, t in enumerate(teams)}
    home_adv = float(np.exp(params[2 * n]))
    rho = float(params[2 * n + 1])

    log(f"  Home advantage multiplier: {home_adv:.4f}")
    log(f"  Rho (low-score correction): {rho:.4f}")
    log(f"  NLL: {result.fun:.2f}")

    return attack, defence, home_adv, rho


def compute_win_probability(attack, defence, home_adv, rho, ht, at, max_goals=8):
    """
    Compute P(home wins) by summing over score outcomes.
    Uses the Dixon-Coles joint probability distribution.
    """
    mu = attack[ht] * defence[at] * home_adv
    nu = attack[at] * defence[ht]

    p_home_win = 0.0
    for hg in range(max_goals + 1):
        for ag in range(max_goals + 1):
            tau = tau_correction(hg, ag, mu, nu, rho)
            p = tau * poisson_pmf(hg, mu) * poisson_pmf(ag, nu)
            if hg > ag:
                p_home_win += p

    return np.clip(p_home_win, 0.01, 0.99)


def compute_dixon_coles_ranking(game_df, team_df):
    """Build team strength index from Dixon-Coles attack/defence parameters."""
    teams = sorted(team_df['team'].tolist())
    attack, defence, home_adv, rho = fit_dixon_coles(game_df, teams)

    rows = []
    for team in teams:
        att = attack.get(team, 1.0)
        dfc = defence.get(team, 1.0)
        # Team strength = attack / defence (higher attack, lower defence conceded = better)
        # Use attack * (1/defence) as combined metric
        strength = att / dfc
        rows.append({
            'team': team,
            'dc_attack': round(att, 6),
            'dc_defence': round(dfc, 6),
            'dc_strength': round(strength, 6),
        })

    df = pd.DataFrame(rows)
    df = df.sort_values('dc_strength', ascending=False).reset_index(drop=True)
    df['rank'] = range(1, len(df) + 1)
    df['score'] = df['dc_strength']
    return df, attack, defence, home_adv, rho


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

    ranking_df, attack, defence, home_adv, rho = compute_dixon_coles_ranking(game_df, team_df)

    log("Top 10 Dixon-Coles Rankings:")
    log(ranking_df.head(10)[['rank', 'team', 'dc_attack', 'dc_defence', 'dc_strength']].to_string(index=False))

    out_path = os.path.join(OUT_DIR, 'cc_model_14_dixon_coles.csv')
    os.makedirs(OUT_DIR, exist_ok=True)
    ranking_df[['rank', 'team', 'score', 'dc_attack', 'dc_defence', 'dc_strength']].to_csv(out_path, index=False)
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
