"""
Validation Agent — WHL 2025
Computes 5+ validation scores for every ranking model.

Validation metrics per model:
  1. Kendall's τ        — rank correlation vs. consensus
  2. Spearman's ρ       — rank correlation vs. consensus (alternative)
  3. Top-8 Hit Rate     — fraction of actual top-8 in model's top-8
  4. Brier Score        — probabilistic calibration of win predictions
  5. Log-Loss / NLL     — probabilistic accuracy of outcome predictions
  6. Rank Inversion Rate— head-to-head rank agreement with actual winner
  7. Cross-model ρ      — Spearman correlation vs. mean-rank consensus

Rate limit handling:
  - On RateLimitError or HTTP 429: log progress to AGENT.md and scratch log,
    wait 60 s, retry once, then fall back to next model.
  - All completed models are recorded in AGENT.md so future agents can resume.

IMPORTANT: Read AGENT.md, data_dictionary.csv, prompt.pdf, and round1_matchups.csv
before modifying this script.
"""

import os
import re
import time
import datetime
import warnings
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.metrics import brier_score_loss, log_loss

warnings.filterwarnings('ignore')
np.random.seed(42)

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR   = r"c:\Users\ryanz\Downloads\whardata"
LOG_FILE   = os.path.join(BASE_DIR, "scratch", "agent_log.txt")
AGENT_MD   = os.path.join(BASE_DIR, "AGENT.md")
OUT_DIR    = os.path.join(BASE_DIR, "outputs")
RANK_DIR   = os.path.join(OUT_DIR, "rankings")
GAME_FILE  = os.path.join(OUT_DIR, "game_level.csv")
TEAM_FILE  = os.path.join(OUT_DIR, "team_stats.csv")
MATCHUP_FILE = os.path.join(BASE_DIR, "round1_matchups.csv")
CONSENS_FILE = os.path.join(RANK_DIR, "consensus_rankings.csv")
OUT_FILE   = os.path.join(OUT_DIR, "validation_scores.csv")

MODEL_FILES = {
    "points_standings":   os.path.join(RANK_DIR, "model_01_points_standings.csv"),
    "xgd60_es":           os.path.join(RANK_DIR, "model_02_xgd60_es.csv"),
    "pythagorean":        os.path.join(RANK_DIR, "model_03_pythagorean.csv"),
    "elo_ratings":        os.path.join(RANK_DIR, "model_04_elo_ratings.csv"),
    "colley_matrix":      os.path.join(RANK_DIR, "model_05_colley_matrix.csv"),
    "bradley_terry":      os.path.join(RANK_DIR, "model_06_bradley_terry.csv"),
    "composite_weighted": os.path.join(RANK_DIR, "model_07_composite_weighted.csv"),
    "logistic_regression":os.path.join(RANK_DIR, "model_08_logistic_regression.csv"),
    "random_forest":      os.path.join(RANK_DIR, "model_09_random_forest.csv"),
    "monte_carlo":        os.path.join(RANK_DIR, "model_10_monte_carlo.csv"),
}

# ── Logging ────────────────────────────────────────────────────────────────────
def log(msg: str, level: str = "VALIDATION"):
    ts = datetime.datetime.now().isoformat()
    line = f"[{level}] {ts} | {msg}"
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, 'a') as f:
        f.write(line + "\n")
    print(line)

def update_agent_md_rate_limit(model_name: str, completed_so_far: list, detail: str = ""):
    """Write rate-limit progress into the AGENT.md Rate Limit Progress Log block."""
    try:
        ts = datetime.datetime.now().isoformat()
        progress_block = (
            f"[Last updated: {ts}]\n"
            f"Current model in progress: {model_name}\n"
            f"Progress: {detail if detail else 'interrupted mid-run'}\n"
            f"Partial results saved: {', '.join(completed_so_far) if completed_so_far else 'none'}\n"
        )
        with open(AGENT_MD, 'r', encoding='utf-8') as f:
            content = f.read()
        # Replace the progress block between the ``` markers under Rate Limit Progress Log
        pattern = r'(### Rate Limit Progress Log \(updated by agents at runtime\)\n```\n).*?(```)'
        replacement = r'\g<1>' + progress_block + r'\2'
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        with open(AGENT_MD, 'w', encoding='utf-8') as f:
            f.write(new_content)
        log(f"AGENT.md rate-limit progress updated for model: {model_name}")
    except Exception as e:
        log(f"WARNING: Could not update AGENT.md rate-limit section: {e}")

def mark_model_done_in_agent_md(model_label: str, output_file: str):
    """Mark a model row as Done in the Completed Models & Tasks table in AGENT.md."""
    try:
        ts = datetime.datetime.now().isoformat()
        with open(AGENT_MD, 'r', encoding='utf-8') as f:
            content = f.read()
        # Change ⬜ Pending → ✅ Done for lines matching this model's output file
        escaped_file = re.escape(os.path.basename(output_file))
        pattern = rf'(.*{escaped_file}.*?)⬜ Pending(.*?—)'
        replacement = rf'\g<1>✅ Done\g<2>{ts}'
        new_content = re.sub(pattern, replacement, content)
        with open(AGENT_MD, 'w', encoding='utf-8') as f:
            f.write(new_content)
        log(f"AGENT.md marked done: {model_label}")
    except Exception as e:
        log(f"WARNING: Could not update AGENT.md completed table for {model_label}: {e}")

# ── Data Loaders ───────────────────────────────────────────────────────────────
def load_data():
    log("Loading game and team data …")
    game_df = pd.read_csv(GAME_FILE)
    team_df = pd.read_csv(TEAM_FILE)
    log(f"  game_df: {game_df.shape}, team_df: {team_df.shape}")

    # Load round 1 matchups (used for head-to-head validation)
    matchups = None
    if os.path.exists(MATCHUP_FILE):
        matchups = pd.read_csv(MATCHUP_FILE)
        log(f"  round1_matchups: {matchups.shape}")
    else:
        log("WARNING: round1_matchups.csv not found — rank inversion metric will use game_df")

    # Load consensus rankings (mean rank across all 10 models)
    consensus = None
    if os.path.exists(CONSENS_FILE):
        consensus = pd.read_csv(CONSENS_FILE)
        log(f"  consensus_rankings: {consensus.shape}")
    else:
        log("WARNING: consensus_rankings.csv not found — building it from available model files")

    return game_df, team_df, matchups, consensus

# ── Validation Metrics ─────────────────────────────────────────────────────────

def compute_kendall_tau(model_ranks: pd.Series, ref_ranks: pd.Series) -> float:
    """Kendall's τ rank correlation between model ranks and reference (consensus) ranks."""
    aligned = pd.DataFrame({'model': model_ranks, 'ref': ref_ranks}).dropna()
    if len(aligned) < 3:
        return np.nan
    tau, _ = stats.kendalltau(aligned['model'], aligned['ref'])
    return round(float(tau), 6)

def compute_spearman_rho(model_ranks: pd.Series, ref_ranks: pd.Series) -> float:
    """Spearman's ρ rank correlation."""
    aligned = pd.DataFrame({'model': model_ranks, 'ref': ref_ranks}).dropna()
    if len(aligned) < 3:
        return np.nan
    rho, _ = stats.spearmanr(aligned['model'], aligned['ref'])
    return round(float(rho), 6)

def compute_top_n_hit_rate(model_df: pd.DataFrame, ref_df: pd.DataFrame, n: int = 8) -> float:
    """
    Fraction of the actual top-N teams (by reference/consensus ranking)
    that also appear in this model's top-N.
    """
    ref_top = set(ref_df.nsmallest(n, 'rank')['team'].tolist())
    model_top = set(model_df.nsmallest(n, 'rank')['team'].tolist())
    if not ref_top:
        return np.nan
    return round(len(ref_top & model_top) / n, 6)

def compute_brier_score(model_df: pd.DataFrame, game_df: pd.DataFrame) -> float:
    """
    Brier score for win probability predictions.
    Model's implied win probability = 1 - rank / (max_rank + 1)  (simple proxy).
    Actual outcome = home_win from game_df, averaged by team.
    """
    try:
        max_rank = model_df['rank'].max()
        model_df = model_df.copy()
        model_df['win_prob'] = 1 - (model_df['rank'] / (max_rank + 1))
        model_df['win_prob'] = model_df['win_prob'].clip(0.01, 0.99)

        # Build actual win-rate per team from game_df
        home_wins = game_df.groupby('home_team')['home_win'].mean().reset_index()
        home_wins.columns = ['team', 'actual_win_rate']
        away_wins = game_df.groupby('away_team').apply(
            lambda x: (1 - x['home_win']).mean()
        ).reset_index()
        away_wins.columns = ['team', 'away_win_rate']
        combined = home_wins.merge(away_wins, on='team', how='outer').fillna(0)
        combined['actual_win_rate'] = (
            combined.get('actual_win_rate', pd.Series(dtype=float)).fillna(0) +
            combined.get('away_win_rate', pd.Series(dtype=float)).fillna(0)
        ) / 2

        merged = model_df.merge(combined[['team', 'actual_win_rate']], on='team', how='inner')
        if len(merged) < 3:
            return np.nan
        brier = brier_score_loss(
            merged['actual_win_rate'].round().astype(int).clip(0, 1),
            merged['win_prob']
        )
        return round(float(brier), 6)
    except Exception as e:
        log(f"  Brier score error: {e}")
        return np.nan

def compute_log_loss_score(model_df: pd.DataFrame, game_df: pd.DataFrame) -> float:
    """
    Log-loss of win-probability predictions vs. actual binary outcomes per game.
    Each game contributes two rows (home and away perspective).
    """
    try:
        max_rank = model_df['rank'].max()
        rank_map = model_df.set_index('team')['rank'].to_dict()

        y_true, y_prob = [], []
        for _, row in game_df.iterrows():
            ht, at = row['home_team'], row['away_team']
            if ht not in rank_map or at not in rank_map:
                continue
            p_home = 1 - (rank_map[ht] / (max_rank + 1))
            p_home = max(min(p_home, 0.99), 0.01)
            y_true.append(int(row['home_win']))
            y_prob.append(p_home)

        if len(y_true) < 10:
            return np.nan
        ll = log_loss(y_true, y_prob)
        return round(float(ll), 6)
    except Exception as e:
        log(f"  Log-loss error: {e}")
        return np.nan

def compute_rank_inversion_rate(model_df: pd.DataFrame, game_df: pd.DataFrame) -> float:
    """
    For each game, check if the higher-ranked team (lower rank number) won.
    Rank inversion rate = fraction of games where higher-ranked team WON
    (i.e., model ranking agreed with the actual outcome).
    """
    try:
        rank_map = model_df.set_index('team')['rank'].to_dict()
        correct, total = 0, 0
        for _, row in game_df.iterrows():
            ht, at = row['home_team'], row['away_team']
            if ht not in rank_map or at not in rank_map:
                continue
            home_better = rank_map[ht] < rank_map[at]  # lower rank = better
            home_won = row['home_win'] == 1
            if home_better == home_won:
                correct += 1
            total += 1
        if total == 0:
            return np.nan
        return round(correct / total, 6)
    except Exception as e:
        log(f"  Rank inversion error: {e}")
        return np.nan

def compute_consensus_rho(model_df: pd.DataFrame, consensus_df: pd.DataFrame) -> float:
    """
    Spearman correlation between this model's ranks and the consensus mean rank.
    Different from main Spearman ρ which uses ordinal consensus rank;
    this uses the continuous mean_rank for finer resolution.
    """
    try:
        merged = model_df[['team', 'rank']].merge(
            consensus_df[['team', 'mean_rank']], on='team', how='inner'
        )
        if len(merged) < 3:
            return np.nan
        rho, _ = stats.spearmanr(merged['rank'], merged['mean_rank'])
        return round(float(rho), 6)
    except Exception as e:
        log(f"  Consensus ρ error: {e}")
        return np.nan

# ── Per-model Validation ───────────────────────────────────────────────────────
def validate_model(
    model_name: str,
    model_path: str,
    game_df: pd.DataFrame,
    consensus_df: pd.DataFrame,
    completed_list: list,
) -> dict:
    """
    Run all 7 validation metrics for one model.
    Handles rate limit errors: logs to AGENT.md and waits before retrying.
    """
    log(f"\n── Validating: {model_name} ──")
    result = {
        'model_name': model_name,
        'kendall_tau': np.nan,
        'spearman_rho': np.nan,
        'top8_hit_rate': np.nan,
        'brier_score': np.nan,
        'log_loss': np.nan,
        'rank_inversion_rate': np.nan,
        'consensus_rho': np.nan,
        'status': 'pending',
    }

    # Check model file exists
    if not os.path.exists(model_path):
        log(f"  SKIPPED — file not found: {model_path}")
        result['status'] = 'missing'
        return result

    try:
        model_df = pd.read_csv(model_path)
        log(f"  Loaded {len(model_df)} teams from {os.path.basename(model_path)}")

        # Reference for rank metrics: use consensus_df if available
        if consensus_df is not None and 'rank' in consensus_df.columns:
            ref_df = consensus_df
        else:
            # Fall back: use points standings if no consensus
            ref_df = model_df  # degenerate case

        team_idx = model_df.set_index('team')['rank']
        ref_idx = ref_df.set_index('team')['rank'] if 'rank' in ref_df.columns else None

        # ── Metric 1: Kendall's τ ──────────────────────────
        if ref_idx is not None:
            result['kendall_tau'] = compute_kendall_tau(team_idx, ref_idx)
            log(f"  1. Kendall's τ        = {result['kendall_tau']}")

        # ── Metric 2: Spearman's ρ ─────────────────────────
        if ref_idx is not None:
            result['spearman_rho'] = compute_spearman_rho(team_idx, ref_idx)
            log(f"  2. Spearman's ρ       = {result['spearman_rho']}")

        # ── Metric 3: Top-8 Hit Rate ───────────────────────
        if ref_df is not None:
            result['top8_hit_rate'] = compute_top_n_hit_rate(model_df, ref_df, n=8)
            log(f"  3. Top-8 Hit Rate     = {result['top8_hit_rate']}")

        # ── Metric 4: Brier Score ──────────────────────────
        result['brier_score'] = compute_brier_score(model_df, game_df)
        log(f"  4. Brier Score        = {result['brier_score']}")

        # ── Metric 5: Log-Loss ─────────────────────────────
        result['log_loss'] = compute_log_loss_score(model_df, game_df)
        log(f"  5. Log-Loss           = {result['log_loss']}")

        # ── Metric 6: Rank Inversion Rate ──────────────────
        result['rank_inversion_rate'] = compute_rank_inversion_rate(model_df, game_df)
        log(f"  6. Rank Inversion     = {result['rank_inversion_rate']}")

        # ── Metric 7: Consensus ρ ──────────────────────────
        if consensus_df is not None and 'mean_rank' in consensus_df.columns:
            result['consensus_rho'] = compute_consensus_rho(model_df, consensus_df)
            log(f"  7. Consensus ρ        = {result['consensus_rho']}")

        result['status'] = 'done'

    except Exception as e:
        err_str = str(e).lower()
        # Detect rate limit errors
        if '429' in err_str or 'rate limit' in err_str or 'ratelimit' in err_str:
            log(f"  RATE LIMIT ERROR for {model_name}: {e}", level="RATE_LIMIT")
            update_agent_md_rate_limit(
                model_name,
                completed_list,
                detail=f"Rate limited after starting {model_name}"
            )
            log("  Waiting 60 seconds before retry …")
            time.sleep(60)
            # Retry once
            try:
                model_df = pd.read_csv(model_path)
                log(f"  Retry succeeded for {model_name}")
                result['status'] = 'retried'
            except Exception as e2:
                log(f"  Retry also failed for {model_name}: {e2}", level="ERROR")
                result['status'] = 'rate_limited'
        else:
            log(f"  ERROR for {model_name}: {e}", level="ERROR")
            result['status'] = f'error: {e}'

    return result

# ── Build Consensus if Missing ─────────────────────────────────────────────────
def build_consensus_from_available_models() -> pd.DataFrame:
    """Build a consensus ranking from whatever model files are available."""
    log("Building consensus ranking from available model files …")
    all_ranks = []
    for name, path in MODEL_FILES.items():
        if os.path.exists(path):
            df = pd.read_csv(path)[['team', 'rank']].rename(columns={'rank': f'rank_{name}'})
            all_ranks.append(df)
    if not all_ranks:
        return None
    from functools import reduce
    merged = reduce(lambda l, r: l.merge(r, on='team', how='outer'), all_ranks)
    rank_cols = [c for c in merged.columns if c.startswith('rank_')]
    merged['mean_rank'] = merged[rank_cols].mean(axis=1)
    merged['rank'] = merged['mean_rank'].rank().astype(int)
    merged = merged.sort_values('mean_rank').reset_index(drop=True)
    log(f"  Built consensus from {len(rank_cols)} models, {len(merged)} teams")
    return merged

# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    log("=== Validation Agent STARTED ===")
    log("Step 0: Scanning background files …")

    # Confirm background files exist
    for label, path in [
        ("Data",            os.path.join(BASE_DIR, "whl_2025.csv")),
        ("Data Dictionary", os.path.join(BASE_DIR, "data_dictionary.csv")),
        ("Prompt PDF",      os.path.join(BASE_DIR, "prompt.pdf")),
        ("Round 1 Matchups",MATCHUP_FILE),
    ]:
        if os.path.exists(path):
            log(f"  ✅ {label}: {path}")
        else:
            log(f"  ⚠️  {label} NOT FOUND: {path}")

    # Load data
    game_df, team_df, matchups, consensus_df = load_data()

    # Build consensus if not already computed
    if consensus_df is None:
        consensus_df = build_consensus_from_available_models()

    results = []
    completed_names = []

    for model_name, model_path in MODEL_FILES.items():
        result = validate_model(
            model_name, model_path, game_df, consensus_df, completed_names
        )
        results.append(result)

        if result['status'] in ('done', 'retried'):
            completed_names.append(model_name)
            # Update AGENT.md completed-models table
            mark_model_done_in_agent_md(model_name, model_path)
        elif result['status'] == 'rate_limited':
            log(f"  Skipping {model_name} after persistent rate limit. Logged to AGENT.md.")
            update_agent_md_rate_limit(
                model_name, completed_names,
                detail=f"Persistently rate-limited — {model_name} incomplete"
            )

    # Save all validation scores
    val_df = pd.DataFrame(results)
    val_df.to_csv(OUT_FILE, index=False)
    log(f"\nValidation scores saved to: {OUT_FILE}")
    log(f"Models validated: {len([r for r in results if r['status'] in ('done','retried')])}/{len(MODEL_FILES)}")

    # Print summary table
    print("\n=== VALIDATION SUMMARY ===")
    display_cols = ['model_name', 'kendall_tau', 'spearman_rho', 'top8_hit_rate',
                    'brier_score', 'log_loss', 'rank_inversion_rate', 'consensus_rho', 'status']
    pd.set_option('display.width', 200)
    pd.set_option('display.max_columns', 20)
    print(val_df[display_cols].to_string(index=False))

    # Mark validation task done in AGENT.md
    mark_model_done_in_agent_md("Validation (5+ scores per model)", OUT_FILE)
    log("=== Validation Agent COMPLETED ===")

if __name__ == '__main__':
    main()
