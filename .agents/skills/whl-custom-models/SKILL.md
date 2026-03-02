---
name: WHL Custom Models
description: Patterns and templates for creating custom CLAUDE CODE MODEL scripts for the WHL competition. Covers all phases and model types.
---

# WHL Custom Model Creation Skill

This skill defines the standard patterns for creating new CLAUDE CODE MODEL scripts.

## Naming Convention (Mandatory)

```
CLAUDE CODE MODEL - (task: <Phase>, <Model Name / Iteration>)
```

Examples:
- `CLAUDE CODE MODEL - (Phase 1a: Strength-of-Schedule Adjusted Rating, v1)`
- `CLAUDE CODE MODEL - (Phase 1a: Dixon-Coles Bivariate Poisson)`
- `CLAUDE CODE MODEL - (Phase 1a: Ensemble Bayesian Rank Aggregation)`
- `CLAUDE CODE MODEL - (Phase 1b: Gini Line Disparity Index)`

## File Naming Convention
Scripts: `scripts/cc_<short_name>.py`
Output: `outputs/rankings/cc_model_<num>_<short_name>.csv`

## Script Template

```python
"""
CLAUDE CODE MODEL - (Phase 1a: <Model Name>)
WHL 2025 Competition — Custom Model by Claude Code
"""
import os, datetime, warnings
import pandas as pd
import numpy as np
from scipy import stats
np.random.seed(42)
warnings.filterwarnings('ignore')

MODEL_NAME = "CLAUDE CODE MODEL - (Phase 1a: <Name>)"
LOG_FILE   = r"c:\Users\ryanz\Downloads\whardata\scratch\agent_log.txt"
OUT_DIR    = r"c:\Users\ryanz\Downloads\whardata\outputs\rankings"
GAME_FILE  = r"c:\Users\ryanz\Downloads\whardata\outputs\game_level.csv"
TEAM_FILE  = r"c:\Users\ryanz\Downloads\whardata\outputs\team_stats.csv"
RANK_DIR   = r"c:\Users\ryanz\Downloads\whardata\outputs\rankings"

def log(msg):
    ts = datetime.datetime.now().isoformat()
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"[CC_MODEL] {ts} | {msg}\n")
    print(msg)

def compute_model(game_df, team_df):
    """
    Mathematical formulation: <describe formula here>
    """
    # ... model implementation ...
    pass

def validate_model(ranking_df, game_df, team_df):
    """Compute all 7 validation metrics."""
    from scipy import stats
    m_ranks = ranking_df.set_index('team')['rank']
    gt_ranks = team_df.set_index('team')['rank_points']
    common = m_ranks.index.intersection(gt_ranks.index)
    tau, _   = stats.kendalltau(m_ranks[common], gt_ranks[common])
    rho, _   = stats.spearmanr(m_ranks[common], gt_ranks[common])
    top8_m   = set(ranking_df.head(8)['team'])
    top8_gt  = set(team_df.sort_values('rank_points').head(8)['team'])
    top8_hit = len(top8_m & top8_gt) / 8
    # ... compute brier, logloss, inversion rate, consensus rho ...
    return {
        'model_name': MODEL_NAME,
        'kendall_tau': round(tau, 4),
        'spearman_rho': round(rho, 4),
        'top8_hit_rate': round(top8_hit, 4),
        # ... other metrics ...
    }

def main():
    log(f"=== {MODEL_NAME} STARTED ===")
    game_df = pd.read_csv(GAME_FILE)
    team_df = pd.read_csv(TEAM_FILE)

    ranking_df = compute_model(game_df, team_df)

    out_path = os.path.join(OUT_DIR, 'cc_model_XX_<name>.csv')
    ranking_df.to_csv(out_path, index=False)
    log(f"Saved: {out_path}")

    metrics = validate_model(ranking_df, game_df, team_df)
    log(f"Validation: {metrics}")

    # Append to validation_scores.csv
    val_path = r"c:\Users\ryanz\Downloads\whardata\outputs\validation_scores.csv"
    if os.path.exists(val_path):
        val_df = pd.read_csv(val_path)
        val_df = pd.concat([val_df, pd.DataFrame([metrics])], ignore_index=True)
        val_df.to_csv(val_path, index=False)

    log(f"=== {MODEL_NAME} COMPLETED ===")

if __name__ == '__main__':
    main()
```

## Currently Implemented CLAUDE CODE MODELS

| Model | File | Phase | Description |
|-------|------|-------|-------------|
| CC-01: SOS Adjusted Rating | `cc_sos_rating.py` | 1a | Win % adjusted for opponent strength via iterative schedule correction |
| CC-02: Dixon-Coles Poisson | `cc_dixon_coles.py` | 1a | Bivariate Poisson model with correlated home/away goals |
| CC-03: Bayesian Rank Aggregation | `cc_bayesian_agg.py` | 1a | Bayesian model averaging over all 12 existing model rankings |
| CC-04: Gini Line Disparity | `cc_gini_disparity.py` | 1b | Gini coefficient applied to line-level xG shares for each team |

## Model Design Principles

1. **Add genuine signal**: Each new model must use a different statistical mechanism than existing models
2. **Grounded in data only**: No external hockey knowledge or real-world data
3. **Interpretable**: The mathematical formulation must be documentable in the report
4. **Cross-validates**: Must pass the 7-metric validation suite
5. **Reproducible**: Fixed random seeds, deterministic outputs

## Good Model Ideas for Phase 1a
- Schedule strength index (opponents' win percentages)
- Margin-of-victory weighted Elo
- Time-decay Elo (recent games weighted more heavily)
- Regularized xG regression (shrinkage toward league mean)
- Negative binomial model for goal scoring variance
- Graphical model using head-to-head win network (PageRank-style)

## Good Model Ideas for Phase 1b
- Gini coefficient of line xG shares
- Herfindahl-Hirschman Index (HHI) applied to line minutes
- Opponent-adjusted first-to-second line ratio
- TOI-weighted coefficient of variation of line output
