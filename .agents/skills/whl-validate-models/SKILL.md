---
name: WHL Validate Models
description: Validation pipeline for all WHL ranking models. Computes 7 required metrics per model and saves to outputs/validation_scores.csv. Use when models have been newly created or updated.
---

# WHL Model Validation Skill

This skill validates all ranking models using the 7 required competition metrics and produces a comprehensive validation summary.

## When to Use
- After creating any new ranking model
- After modifying existing model scripts
- When submitting the final competition deliverable
- To compare model performance and select the best ensemble weights

## Validation Metrics (Required for Each Model)

| # | Metric | Formula / Method | Good Value |
|---|--------|-----------------|------------|
| 1 | **Kendall's τ** | `scipy.stats.kendalltau(model_ranks, gt_ranks)` | > 0.5 |
| 2 | **Spearman's ρ** | `scipy.stats.spearmanr(model_ranks, gt_ranks)` | > 0.7 |
| 3 | **Top-8 Hit Rate** | `len(top8_model ∩ top8_gt) / 8` | > 0.6 |
| 4 | **Brier Score** | `mean((y_pred - y_actual)^2)` | < 0.28 |
| 5 | **Log-Loss** | `−mean(y*log(p) + (1−y)*log(1−p))` | < 0.76 |
| 6 | **Rank Inversion Rate** | `% head-to-head where lower-ranked team wins` | < 0.43 |
| 7 | **Consensus ρ** | `spearmanr(model_ranks, mean_rank_consensus)` | > 0.8 |

## Standard Validation Procedure

```python
# 1. Load ground truth
game_df = pd.read_csv('outputs/game_level.csv')
team_df = pd.read_csv('outputs/team_stats.csv')
cons_df = pd.read_csv('outputs/rankings/consensus_rankings.csv')

# 2. Build features for each game
features = []
for _, g in game_df.iterrows():
    ht, at = g['home_team'], g['away_team']
    features.append({
        'home_team': ht, 'away_team': at,
        'home_xgd60': ts.loc[ht,'es_xgd60'] - ts.loc[at,'es_xgd60'],
        'home_win': g['home_win']
    })

# 3. For each model: convert ranks to probabilities
# P(home wins) = 1 / (1 + exp((rank_home - rank_away) / 10))

# 4. Save results to outputs/validation_scores.csv
# Required columns: model_name, kendall_tau, spearman_rho, top8_hit_rate,
#                   brier_score, log_loss, rank_inversion_rate, consensus_rho
```

## Running Validation

```bash
# Run the full validation script
python scripts/05_validation.py

# Output files produced:
# outputs/validation_scores.csv         ← 7-metric table for all models
# outputs/win_prob_validation.csv       ← 10-fold CV results for win probability LR
# outputs/elo_calibration_curve.csv     ← Elo calibration by decile
# outputs/ranking_ci_overlap.csv        ← Bootstrap CI overlap for adjacent ranked teams
# outputs/model_agreement_matrix.csv   ← Pairwise model agreement rates
```

## Interpreting Results

### Best models (by validation accuracy, from current analysis):
1. **Colley Matrix / Bradley-Terry**: 59.38% accuracy — most stable, schedule-adjusted
2. **Composite Weighted**: 59.53% accuracy — best overall
3. **Elo**: 58.54% accuracy — good momentum capture

### Red flags to investigate:
- `kendall_tau < 0.3` → model ranking uncorrelated with ground truth
- `brier_score > 0.30` → worse than a naive "always predict home wins" baseline
- `top8_hit_rate < 0.5` → model cannot identify the top teams
- `accuracy < 0.54` → baseline beat by naive models

## Cross-Validation Protocol for Win Probability
1. **In-sample fit** on all 1,312 games
2. **10-fold stratified CV** → mean ± std accuracy
3. **Leave-One-Team-Out (LOTO)** → tests generalization to unseen teams
4. **Baselines**: always-home (56.4%), higher-points, higher-xGD/60

## Adding New Models to Validation
When a CLAUDE CODE MODEL is created:
1. Save its rankings CSV to `outputs/rankings/cc_model_XX_<name>.csv`
2. Ensure columns: `['rank', 'team', 'score']` at minimum
3. Run `python scripts/cc_validation_extension.py` to append its metrics to `validation_scores.csv`
4. Update AGENT.md Completed Models table
