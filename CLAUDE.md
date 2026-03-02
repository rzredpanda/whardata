# CLAUDE.md — WHL 2025 Wharton Data Science Competition

## Project Overview
This is the **2026 Wharton High School Data Science Competition** project — an ice hockey analytics challenge using simulated WHL (World Hockey League) season data.

**Submission deadline:** March 2, 2026, 9:00 AM ET

**Competition phases:**
- **Phase 1a** — Team power rankings (all 32 teams) + win probabilities for 16 Round 1 matchups
- **Phase 1b** — Top-10 teams by offensive line quality disparity ratio
- **Phase 1c** — Data visualization (disparity vs. team strength)
- **Phase 1d** — Methodology summary for WHL commissioner

---

## Critical Files

| File | Purpose |
|------|---------|
| `whl_2025.csv` | Primary shift-level dataset (25,827 rows, 1,312 games) |
| `data_dictionary.csv` | Column definitions — check before using any field |
| `prompt_text.txt` | Official competition prompt (extracted from prompt.pdf) |
| `round1_matchups.csv` | 16 Round 1 games to predict |
| `AGENT.md` | Multi-agent orchestration rules |
| `FINAL_REPORT.md` | Master report — always update this, not WHL_Competition_Report.md |
| `outputs/win_probabilities.csv` | Final matchup predictions |
| `outputs/rankings/consensus_rankings.csv` | Final power rankings |

---

## Model Naming Convention

**Custom models created by Claude Code MUST follow this convention:**
```
CLAUDE CODE MODEL - (task: <Phase>, <Model Name / Iteration>)
```

Examples:
- `CLAUDE CODE MODEL - (Phase 1a: Strength-of-Schedule Adjusted Rating)`
- `CLAUDE CODE MODEL - (Phase 1a: Dixon-Coles Bivariate Poisson, v1)`
- `CLAUDE CODE MODEL - (Phase 1b: Gini Line Disparity Index)`
- `CLAUDE CODE MODEL - (Phase 1a: Ensemble Bayesian Rank Aggregation)`

---

## Directory Structure

```
whardata/
├── CLAUDE.md              ← this file
├── AGENT.md               ← multi-agent rules
├── FINAL_REPORT.md        ← master deliverable report
├── whl_2025.csv           ← raw data
├── round1_matchups.csv    ← matchups to predict
├── data_dictionary.csv    ← column definitions
├── run_pipeline.py        ← full pipeline runner
├── scripts/
│   ├── 00_eda.py
│   ├── 01_game_aggregation.py
│   ├── 02_ranking_models.py
│   ├── 03_win_probability.py
│   ├── 04_line_disparity.py
│   ├── 05_validation.py
│   ├── 11_final_report.py
│   └── cc_*.py            ← CLAUDE CODE MODEL scripts (cc_ prefix)
├── outputs/
│   ├── game_level.csv
│   ├── team_stats.csv
│   ├── win_probabilities.csv
│   ├── validation_scores.csv
│   ├── rankings/          ← all model ranking CSVs
│   └── disparity/         ← line disparity CSVs
└── scratch/               ← logs and temp files
```

---

## Workflow Rules

### Before writing any code:
1. Read `AGENT.md` for multi-agent rules
2. Check `outputs/` for already-completed work — never redo completed steps
3. Always set `np.random.seed(42)` for reproducibility
4. Check `data_dictionary.csv` for any column you use

### Code standards:
- Use `pandas`, `numpy`, `scipy`, `sklearn` as primary libraries
- All custom model scripts go in `scripts/` with `cc_` prefix
- Output CSVs go in `outputs/rankings/` (Phase 1a) or `outputs/disparity/` (Phase 1b)
- Every model needs ≥5 validation metrics (see AGENT.md Validation Requirements)
- No visualizations unless user says "green light on visualizations"

### Git:
- Never auto-commit — only commit when user explicitly requests
- Never push without confirmation
- Never use `--no-verify`

---

## Skills Available

Skills are in `.agents/skills/`. Use them by referencing their names:
- `hockey_analytics` — Hockey data normalization, xG modeling, ensemble ranking
- `phd_report_writing` — Formal academic report style guidelines
- `whl-validate-models` — Validation pipeline for ranking models
- `whl-run-pipeline` — Full pipeline execution guide
- `whl-update-report` — Report update and formatting procedures
- `whl-custom-models` — Custom CLAUDE CODE MODEL creation patterns

---

## Key Findings (from completed analysis)

### Top 3 Teams (consensus across all models):
1. **Thailand** — Best xG-based metrics, Pythagorean leader, Monte Carlo #1
2. **Brazil** — Points leader, Elo #1, Bradley-Terry #1
3. **Pakistan** — xGD/60 leader, consistent top-3 across all models

### Worst 3 Teams:
- **Mongolia** — Dead last in 7/10 models, lowest xGD/60
- **Kazakhstan** — Consistently bottom-3
- **Rwanda/Switzerland** — Bottom tier

### Home Ice Advantage:
- 56.4% home win rate overall, 57.6% regulation-only
- Statistically significant (p < 0.001)

### Model Performance (by accuracy):
1. Colley Matrix / Bradley-Terry: 59.38% accuracy
2. Composite: 59.53%
3. Elo: 58.54%
4. Points: 58.23%

### Top-10 Line Disparity (largest first-line dependence):
1. Saudi Arabia
2. Guatemala
3. France
4. USA
5. Iceland / Singapore (tied)
7. UAE
8. New Zealand
9. Peru
10. Serbia

---

## Validation Requirements (per model)

Every model must compute and save these 7 metrics:
1. Kendall's τ (rank correlation vs. points standings)
2. Spearman's ρ
3. Top-8 Hit Rate (% of actual top-8 correctly identified)
4. Brier Score
5. Log-Loss / NLL
6. Rank Inversion Rate
7. Cross-model Consensus ρ

Results saved to `outputs/validation_scores.csv`.

---

## Phase 1 Deliverables Summary

### 1a — Power Rankings (32 teams)
Use `outputs/rankings/consensus_rankings.csv` — final consensus_rank column.

### 1a — Win Probabilities (16 matchups)
Use `outputs/win_probabilities.csv` — p_ensemble column for home team win probability.

### 1b — Top-10 Line Disparity Teams
Use `outputs/disparity/consensus_disparity.csv` — top 10 by mean_rank (ascending).

### 1c — Visualization
Target: scatter plot of disparity rank vs. power rank, showing correlation.

### 1d — Methodology (word counts)
- Data cleaning/transform: ~50 words
- Additional variables: ~25 words
- Software tools: ~50 words
- Statistical methods: ~100 words
- Power rankings approach: ~50 words
- Disparity approach: ~50 words
- Visualization choices: ~50 words

---

## Competition Rules Reminders
- Use ONLY the provided WHL dataset — no external hockey data
- Teams are fictional — do not assume real-world identities
- Regular season IS representative of playoffs (per prompt)
- No changes in team/line quality over the season (per prompt)
