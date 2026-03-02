---
name: Hockey Analytics Pipeline
description: End-to-end framework for parsing shift-level hockey data into actionable power rankings, expected goal modeling, and matchup probabilities.
---

# Hockey Analytics Pipeline

This skill document defines the standard operating procedures for analyzing granular hockey data (e.g., shift level xG events, line matchups, time-on-ice differentials).

## Workflow

### 1. Data Ingestion & Normalization
Start by ingesting raw shift-level events. Never use raw counting numbers for comparison—always normalize them to **Per-60-Minute Rates**.
- **Formula:** `Metric_per_60 = (Raw_Metric * 3600) / Time_on_Ice_Seconds`
- Segregate rates into tactical situations: Even Strength (ES), Powerplay (PP), and Penalty Kill (PK).

### 2. Isolate Team Talent vs. Goalie Talent
Utilize **Goals Saved Above Expected (GSAx)**. Goaltending is inherently volatile and masks structural skater weaknesses. Evaluate the team's xG Differential (xGD) completely separate from its actual goal variance to evaluate pure 5v5 dominance.

### 3. Model Ensembling (Ranking)
A single structural model is prone to bias. Utilize at least these primary models to derive a consensus power ranking:
- **Colley Matrix**: Accounts rigorously for schedule strength without considering goal margins.
- **Bradley-Terry Maximum Likelihood**: Provides log-odds of a team defeating another based entirely on binary win/loss history.
- **Elo Ratings**: Updates chronologically, capturing momentum and home-ice artificial barriers.
- **Pythagorean Expectation**: Evaluates generalized goal production (`xGF^2 / (xGF^2 + xGA^2)`).

### 4. Machine Learning & Predictive Probabilities
To forecast direct playoff matchups, employ probability ensembles:
- Generate independent match probabilities via Logistic Regression, Monte Carlo Simulation (Poisson distributions), Support Vector Machines (SVM), and Random Forests.
- Ensembling these distinct approaches strictly minimizes out-of-sample Brier Scores and cross-entropy loss. 
- Flag disparities: If models disagree wildly (e.g. `max(prob) - min(prob) > 10%`), manual review of those teams' localized variances (like line disparity drops) is mandated.

### 5. Line Disparity (Strategic Vulnerability)
Calculate the differential output between `first_off` and `second_off` lines. Teams with the biggest drop-offs are tactically fragile. Opponents can easily exploit them by matching their elite defensive shutdown pair solely against the opponent's first line, completely starving them of scoring equity.
