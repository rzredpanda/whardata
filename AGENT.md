# AGENT.md — WHL Competition Multi-Agent Rules

## Identity
Lead Orchestrator manages all subagents. **Every subagent MUST read this file before starting any work.**

---

## MANDATORY: Background File Scanning
Before writing a single line of code, every agent MUST read and internalize these files:

| File | Path | Purpose |
|------|------|---------|
| **Data** | `whl_2025.csv` | Primary dataset — scan column names, data types, sample rows |
| **Data Dictionary** | `data_dictionary.csv` | Column definitions — read every row before using any field |
| **Competition Prompt** | `prompt.pdf` | Official task requirements — read in full, note scoring criteria |
| **Round 1 Matchups** | `round1_matchups.csv` | Target matchups for predictions — these are the games to rank/predict |

**Scanning procedure for each file:**
1. Print shape/dtypes for CSV files (`df.shape`, `df.dtypes`, `df.head(5)`)
2. Log any unexpected nulls, data types, or outliers immediately
3. Cross-reference the data dictionary for every column you use
4. For the PDF prompt: extract and log the exact evaluation criteria and deliverable specifications

---

## File Structure
- `/outputs/`           → all final outputs
- `/outputs/rankings/`  → Phase 1a model outputs
- `/outputs/disparity/` → Phase 1b disparity outputs
- `/outputs/eda_tables/`→ EDA supporting tables
- `/outputs/plots/`     → all visualizations (held until green light)
- `/scratch/`           → intermediate/temp files, not final outputs

---

## API Key Safety — CRITICAL
- NEVER print, log, or write API keys or secrets to any file
- NEVER include API keys in code comments
- NEVER hardcode credentials anywhere
- Load all secrets from environment variables only: `os.environ.get('KEY_NAME')`
- If a key is accidentally printed, immediately flag it and do not proceed
- Do not commit or expose `.env` files

---

## Rate Limit Handling — CRITICAL
If any API call returns a rate limit error (HTTP 429 or RateLimitError):

1. **Log** the error with timestamp to `/scratch/agent_log.txt`
2. **Update AGENT.md** immediately with:
   - Current model being processed (name + model number)
   - Number of teams/rows completed so far
   - Any partial results already saved
   - Timestamp of interruption
3. Wait **60 seconds** and retry once
4. If still rate-limited, switch to the next available model in fallback order (below)
5. Log which model was switched to and why
6. **Never crash** the pipeline due to a rate limit — always recover gracefully

### Rate Limit Progress Log (updated by agents at runtime)
```
[Last updated: —]
Current model in progress: —
Progress: —
Partial results saved: —
```

---

## Completed Models & Tasks
> Agents: update this section upon completing each model. Subsequent agents read this to avoid re-running completed work.

| # | Model / Task | Status | Output File | Completed At |
|---|-------------|--------|-------------|-------------|
| 01 | Game Aggregation | ⬜ Pending | `outputs/game_level.csv`, `outputs/team_stats.csv` | — |
| 02-1 | Model 1: Raw Points Standings | ⬜ Pending | `outputs/rankings/model_01_points_standings.csv` | — |
| 02-2 | Model 2: xG Diff per 60 (ES) | ⬜ Pending | `outputs/rankings/model_02_xgd60_es.csv` | — |
| 02-3 | Model 3: Pythagorean Expectation | ⬜ Pending | `outputs/rankings/model_03_pythagorean.csv` | — |
| 02-4 | Model 4: Elo Rating System | ⬜ Pending | `outputs/rankings/model_04_elo_ratings.csv` | — |
| 02-5 | Model 5: Colley Matrix | ⬜ Pending | `outputs/rankings/model_05_colley_matrix.csv` | — |
| 02-6 | Model 6: Bradley-Terry | ⬜ Pending | `outputs/rankings/model_06_bradley_terry.csv` | — |
| 02-7 | Model 7: Composite Weighted | ⬜ Pending | `outputs/rankings/model_07_composite_weighted.csv` | — |
| 02-8 | Model 8: Logistic Regression | ⬜ Pending | `outputs/rankings/model_08_logistic_regression.csv` | — |
| 02-9 | Model 9: Random Forest | ⬜ Pending | `outputs/rankings/model_09_random_forest.csv` | — |
| 02-10 | Model 10: Monte Carlo | ⬜ Pending | `outputs/rankings/model_10_monte_carlo.csv` | — |
| 03 | Validation (5+ scores per model) | ⬜ Pending | `outputs/validation_scores.csv` | — |
| EDA | EDA Agent | ⬜ Pending | `outputs/eda_tables/` | — |

**How to mark complete:** Change `⬜ Pending` → `✅ Done` and fill in timestamp.

---

## Model Fallback Order
- Primary:  `claude-sonnet-4-6`
- Fallback: `claude-opus-4-6`
- Fallback: `claude-haiku-4-5-20251001`

---

## Validation Requirements — CRITICAL
**Every model must have AT LEAST 5 validation scores computed by `scripts/03_validation.py`:**

| # | Metric | Description |
|---|--------|-------------|
| 1 | **Kendall's τ** | Rank correlation against consensus ranking |
| 2 | **Spearman's ρ** | Rank correlation (alternative) |
| 3 | **Top-N Hit Rate** | % of actual top-8 teams correctly in model's top-8 |
| 4 | **Brier Score** | Calibration of win probability predictions |
| 5 | **Log-Loss / NLL** | Probabilistic accuracy of outcome predictions |
| 6 | **Rank Inversion Rate** | % of head-to-head matchups where model rank agrees with actual winner |
| 7 | **Cross-model Agreement (consensus ρ)** | Spearman correlation between this model's ranks and mean-rank consensus |

The validation results must be saved to `outputs/validation_scores.csv` with columns:
`model_name, kendall_tau, spearman_rho, top8_hit_rate, brier_score, log_loss, rank_inversion_rate, consensus_rho`

---

## Subagent Rules
- Each subagent must read **this file (AGENT.md)** before starting
- Each subagent must scan all four background files (see Mandatory Scanning section above)
- Subagents write outputs to `/outputs/` with clearly named files
- Subagents must not overwrite another agent's output files
- Subagents log their start time, end time, and completion status to `/scratch/agent_log.txt`
- If a subagent fails, it writes the error to `/scratch/agent_log.txt` and updates the Completed Models table above
- Subagents do not spawn their own subagents without Orchestrator approval

---

## Parallelization Rules
- EDA Agent runs immediately and in parallel with Game Aggregation Agent
- All ranking model agents wait for `/outputs/game_level.csv` and `/outputs/team_stats.csv` to exist
- Validation Agent (`03_validation.py`) waits for **all 10 model outputs** to exist before running
- PDF Report Agent runs last, after Validation Agent completes
- Use file existence as a synchronization primitive — check for output files before depending on them

---

## Code Standards
- All Python code must include try/except blocks for file I/O and API calls
- All data transformations must be reproducible — set random seeds (`random.seed(42)`, `np.random.seed(42)`)
- Print progress updates at each major step
- Save intermediate outputs frequently — do not rely on in-memory state across steps
- Use `pandas`, `numpy`, `scipy`, `sklearn`, `matplotlib`, `seaborn` as primary libraries
- Install any missing packages with `pip` before importing

---

## Visualization Hold
- Do NOT generate or save any visualization files until the user explicitly says "green light on visualizations"
- All visualization code should be written and ready but wrapped in a flag: `VISUALIZATIONS_ENABLED = False`
- When the green light is given, set `VISUALIZATIONS_ENABLED = True` and run all visualization code

---

## Competition Data Rules
- Use ONLY the provided WHL dataset — do not use external hockey data
- Do not assume real-world team identities from country names
- All findings must be grounded in the data, not hockey domain knowledge
- The prompt states: no changes in team quality over the season; regular season is representative of playoffs

---

## Quality Standards
- **Every model must have at least FIVE validation metrics** (see Validation Requirements above)
- Rankings must be deterministic — same input always produces same output
- All assumptions must be documented in code comments
- The PDF report must be self-contained and understandable without external context
