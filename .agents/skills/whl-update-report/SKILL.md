---
name: WHL Update Report
description: Procedures for updating and formatting FINAL_REPORT.md. Covers all Phase 1 competition deliverables and academic writing standards.
---

# WHL Report Update Skill

This skill governs the update and formatting of `FINAL_REPORT.md` — the primary competition deliverable.

## Report Structure (Required)

```
FINAL_REPORT.md
├── Header (Title, Date, Team)
├── Abstract (dataset size, tools, key outcomes)
├── Section 1: Introduction & Epistemological Framework
├── Section 2: Data Provenance & Exploratory Diagnostics
│   ├── 2.1 Environmental Calibration (home ice advantage)
│   └── 2.2 Data Quality & EDA Findings
├── Section 3: Mathematical Architectures
│   ├── 3.1 Baseline Models (Colley, BT, Elo, Pythagorean, etc.)
│   └── 3.2 CLAUDE CODE MODELS (new custom models — document with full math)
├── Section 4: Validation & Out-of-Sample Testing
│   ├── 4.1 Validation Metrics Table (all models)
│   └── 4.2 Win Probability Cross-Validation
├── Section 5: Model-Specific Results (all 10+ models)
├── Section 6: CLAUDE CODE MODEL Results (custom models)
├── Section 7: Final Power Rankings (consensus, 32 teams)
├── Section 8: Playoff Matchup Predictions (16 games)
├── Section 9: Line Disparity Analysis
│   ├── 9.1 Top-10 Teams by Disparity
│   └── 9.2 Disparity vs. Team Strength Relationship
└── Section 10: Phase 1d Methodology Summary (competition submission text)
    ├── 10.1 Process (~50 words)
    ├── 10.2 Tools and Techniques (~100 words)
    ├── 10.3 Predictions methodology (~50 words each 1a, 1b, 1c)
    └── 10.4 Insights (model performance + AI usage)
```

## Formatting Standards

### Tables
Always use GitHub-flavored markdown tables with column alignment:
```markdown
| Rank | Team     | Score  | Metric_1 | Metric_2 |
|-----:|:---------|-------:|---------:|---------:|
|    1 | Thailand | 0.6053 |  294.737 |  221.662 |
```

### Math notation
Use LaTeX-style inline notation for equations:
- `$P(i > j) = p_i / (p_i + p_j)$`
- `$xGD/60 = (xGF - xGA) \times 3600 / TOI$`

### Section headers
Use `##` for top-level sections, `###` for subsections, `####` for sub-subsections.

### CLAUDE CODE MODEL documentation
Each custom model must be documented with:
1. Full model name following naming convention
2. Mathematical formulation
3. Motivation (why this adds value beyond existing models)
4. Results table
5. Validation metrics (at least 7)
6. Key findings / interpretation

## Data Sources for Report Updates

Pull from these files to update report tables:

```python
# Power rankings
consensus = pd.read_csv('outputs/rankings/consensus_rankings.csv')
# Columns: team, consensus_rank, mean_rank, rank_variance

# Win probabilities
win_probs = pd.read_csv('outputs/win_probabilities.csv')
# Columns: game, home_team, away_team, p_lr, p_elo, p_bt, p_log5, p_mc, p_rf, p_svm, p_ensemble

# Validation scores
validation = pd.read_csv('outputs/validation_scores.csv')
# Columns: model_name, kendall_tau, spearman_rho, top8_hit_rate, brier_score, log_loss, rank_inversion_rate, consensus_rho

# Line disparity
disparity = pd.read_csv('outputs/disparity/consensus_disparity.csv')
# Columns: team, mean_rank, consensus_rank
```

## Phase 1d Methodology Text Template

### Process (~50 words):
"Raw shift-level data (25,827 rows) was aggregated to game-level and team-level summaries. All counting metrics were normalized to per-60-minute rates to control for time-on-ice variation. Even-strength and special-teams situations were isolated. Additional derived variables included xG Differential/60, Pythagorean win percentage, game-by-game Elo trajectories, and line-level disparity ratios."

### Tools (~50 words):
"Python (pandas, numpy, scipy, sklearn) was used for all analysis. Claude Code (Anthropic) served as the primary AI orchestration layer, spawning and coordinating subagents for parallel model development, validation, and report generation. All code is reproducible with fixed random seeds."

### Statistical Methods (~100 words):
"We employed ten distinct statistical architectures: (1) raw points standings, (2) xG differential per 60, (3) Pythagorean expectation with optimal-k tuning, (4) chronological Elo ratings with K=20, (5) Colley Matrix schedule adjustment, (6) Bradley-Terry maximum likelihood, (7) composite weighted ensemble, (8) logistic regression, (9) Random Forest, and (10) Monte Carlo Poisson simulation. Additionally, three CLAUDE CODE MODELS extended this suite: a Strength-of-Schedule adjusted win percentage, a Dixon-Coles bivariate Poisson model, and a Bayesian rank aggregation. Validation used Kendall's τ, Spearman's ρ, Brier scores, log-loss, and 10-fold cross-validation."

## Report Update Checklist

Before finalizing FINAL_REPORT.md:
- [ ] All 32 teams appear in power rankings
- [ ] All 16 Round 1 matchups have win probabilities
- [ ] At least 10 models documented with validation metrics
- [ ] CLAUDE CODE MODELS documented with full math and results
- [ ] Top-10 disparity teams listed correctly
- [ ] Phase 1d methodology text meets word count targets
- [ ] All tables properly formatted with alignment
- [ ] No raw Python output or error messages in report
- [ ] Abstract mentions data size (25,827 rows, 1,312 games, 32 teams)
