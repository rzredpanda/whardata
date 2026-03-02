# WHL Competition Report Formatting Guide

## File Structure

```
reports/
├── README.md              # This file - explains the report structure
├── SUMMARY.md             # Executive summary (1-2 pages)
├── PHASE_1A_RANKINGS.md   # Power rankings only
├── PHASE_1A_PROBABILITIES.md  # Win probabilities only
├── PHASE_1B_DISPARITY.md  # Line disparity only
├── PHASE_1D_METHODS.md    # Detailed methodology
└── appendix/
    ├── individual_models.md   # All 13 model rankings
    └── validation_details.md  # Full validation tables
```

---

## Formatting Standards

### 1. Tables

**DO:** Use aligned columns with proper headers
```markdown
| Rank | Team    | Points | xGD/60 | Confidence |
|-----:|:--------|-------:|-------:|:-----------|
|    1 | Thailand|    107 |   0.89 | High       |
|    2 | Brazil  |    122 |   0.76 | High       |
```

**DON'T:** Use unaligned or unclear tables
```markdown
|Rank|Team|Points|xGD|Conf|
|1|Thailand|107|0.89|High|
|2|Brazil|122|0.76|High|
```

### 2. Probabilities

**Format:** Always show as percentage with 1 decimal place in reports
- In CSV: 0.625 (for calculations)
- In markdown: **62.5%** or 62.5% (depending on emphasis)

**Color coding (for rich displays):**
- High confidence (>65%): 🟢 Green
- Medium (55-65%): 🟡 Yellow
- Toss-up (45-55%): ⚪ Gray
- Away favored (<45%): 🔴 Red

### 3. Section Headers

Use consistent hierarchy:
```markdown
# Main Title

## Section (Phase 1a, 1b, etc.)

### Subsection (Methodology, Results, etc.)

#### Detail (Specific models)
```

### 4. Mathematical Notation

**Inline:** Use single `$` for simple equations
- $P(\text{home win}) = 0.564$
- $\text{xGD}_{/60} = 0.45$

**Block:** Use double `$$` for important formulas
```markdown
$$
P(\text{home wins}) = \frac{1}{1 + 10^{(R_{away} - R_{home})/400}}
$$
```

### 5. Confidence Levels

Standardized labels:
| Range | Label | Symbol |
|-------|-------|--------|
| >70% | Very High | ⭐⭐⭐ |
| 60-70% | High | ⭐⭐ |
| 55-60% | Medium | ⭐ |
| 50-55% | Low | ○ |
| <50% | Very Low | ⚠️ |

---

## Report Templates

### Template: Matchup Prediction Table

```markdown
| Game | Home Team | Away Team | Win Prob | Margin | Confidence | Models Agree |
|-----:|:----------|:----------|--------:|-------:|:-----------|:-------------|
| 1 | Brazil | Kazakhstan | **72.7%** | +22.7 | ⭐⭐⭐ High | 10/10 |
| 2 | Thailand | Oman | **66.7%** | +16.7 | ⭐⭐ Medium | 9/10 |
```

### Template: Power Rankings Summary

```markdown
| Rank | Team | Avg Rank | Best | Worst | Uncertainty |
|-----:|:-----|--------:|-----:|------:|:------------|
| 1 | Thailand | 3.2 | 1 | 8 | Low |
| 2 | Brazil | 3.5 | 1 | 15 | Medium |
```

### Template: Model Comparison

```markdown
| Model | Accuracy | Brier | Top-8 Hit | Grade |
|:------|--------:|------:|----------:|:------|
| Colley Matrix | 59.4% | 0.261 | 100% | A |
| Elo | 58.5% | 0.266 | 87.5% | B+ |
```

---

## Quick Reference: Markdown for Reports

### Emphasis
- **Bold** for important numbers: `**72.5%**`
- *Italic* for model names: `*Elo Rating*`
- `Code` for column names: `` `game_id` ``

### Lists
Use bullet points for explanations:
- **Finding:** Home teams win 56.4% of games
- **Implication:** All models must beat this baseline

Use numbered lists for steps:
1. Aggregate shift data to game level
2. Compute xG differentials
3. Fit Bradley-Terry model

### Callouts

**Important finding:**
> The top-3 teams (Thailand, Brazil, Pakistan) are consistent across all 13 models.

**Warning:**
> ⚠️ Low confidence matchup: Only 5/10 models agree on winner.

**Success:**
> ✅ Model achieves 100% Top-8 Hit Rate.

---

## Validation Summary Format

```markdown
## Model Validation Results

| Metric | Value | Threshold | Status |
|:-------|------:|----------:|:-------|
| 10-fold CV Accuracy | 60.8% | >56.4% | ✅ Pass |
| Brier Score | 0.234 | <0.250 | ✅ Pass |
| Top-8 Hit Rate | 100% | >75% | ✅ Pass |
| Calibration ECE | 0.029 | <0.050 | ✅ Pass |
```
