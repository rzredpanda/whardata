---
name: WHL Run Pipeline
description: Full end-to-end pipeline execution guide for the WHL competition. Covers correct script order, dependency checking, and error recovery.
---

# WHL Pipeline Execution Skill

This skill governs how to correctly execute the full WHL analysis pipeline, including dependency management and error recovery.

## Script Execution Order (Strict)

```
Phase 0:  00_eda.py               ← EDA (parallel with Phase 1)
Phase 1:  01_game_aggregation.py  ← REQUIRED FIRST — produces game_level.csv + team_stats.csv
Phase 2:  02_ranking_models.py    ← All 10 baseline ranking models
Phase 3:  03_win_probability.py   ← Win probability ensemble (7 models)
Phase 4:  04_line_disparity.py    ← 10 disparity metrics
Phase 5:  05_validation.py        ← Validation of all ranking models
Phase CC: cc_*.py                 ← CLAUDE CODE MODEL custom scripts (after Phase 1)
Phase R:  11_final_report.py      ← Final report generation
```

## Quick Start

```bash
# Full pipeline (all phases)
cd C:\Users\ryanz\Downloads\whardata
python run_pipeline.py

# Individual script
python -X utf8 scripts/01_game_aggregation.py
python -X utf8 scripts/02_ranking_models.py
python -X utf8 scripts/05_validation.py
```

## Dependency Checks Before Each Phase

### Before Phase 2 (ranking models):
```python
assert os.path.exists('outputs/game_level.csv'), "Run Phase 1 first"
assert os.path.exists('outputs/team_stats.csv'), "Run Phase 1 first"
```

### Before Phase 5 (validation):
```python
required = [f'outputs/rankings/model_{i:02d}_*.csv' for i in range(1, 11)]
# All 10 model files must exist
```

### Before final report:
```python
assert os.path.exists('outputs/validation_scores.csv'), "Run validation first"
assert os.path.exists('outputs/win_probabilities.csv'), "Run win probability first"
```

## Output File Map

| Script | Primary Output | Secondary Outputs |
|--------|---------------|------------------|
| `01_game_aggregation.py` | `outputs/game_level.csv` | `outputs/team_stats.csv` |
| `02_ranking_models.py` | `outputs/rankings/model_01-10_*.csv` | `outputs/rankings/consensus_rankings.csv` |
| `03_win_probability.py` | `outputs/win_probabilities.csv` | `outputs/win_prob_validation.csv` |
| `04_line_disparity.py` | `outputs/disparity/method_*.csv` | `outputs/disparity/consensus_disparity.csv` |
| `05_validation.py` | `outputs/validation_scores.csv` | `outputs/model_agreement_matrix.csv` |
| `cc_custom_models.py` | `outputs/rankings/cc_model_*.csv` | appended to `validation_scores.csv` |

## Error Recovery

### If a script fails:
1. Check `scratch/pipeline_run.log` for the error
2. Check `scratch/agent_log.txt` for detailed logs
3. Common fixes:
   - `ModuleNotFoundError` → `pip install <package>`
   - `FileNotFoundError` → run the prerequisite script first
   - `KeyError: 'column'` → check `data_dictionary.csv` for correct column name
   - Unicode errors → run with `python -X utf8 script.py`

### If rate-limited (API calls):
1. Log to `scratch/agent_log.txt` with timestamp
2. Wait 60s, retry once
3. If still blocked, skip and note in AGENT.md

## Environment Variables
```bash
# Required for Python on Windows
PYTHONIOENCODING=utf-8
PYTHONUTF8=1
```

## Random Seeds (for reproducibility)
Every script must set at the top:
```python
np.random.seed(42)
random.seed(42)  # if random module used
```
