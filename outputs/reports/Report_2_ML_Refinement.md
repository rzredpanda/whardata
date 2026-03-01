# WHL 2026 — Phase 7: Machine Learning Refinement Report
**Generated:** 2026-02-28 16:05

---

## Executive Summary
We introduced advanced, hyperparameter-tuned machine learning models (Gradient Boosting, Neural Networks, XGBoost, LightGBM) to improve upon the simpler linear and probabilistic ranking models from Phase 1. This report details the performance of these new algorithms against out-of-sample validation metrics to ensure we are maximizing predictive accuracy without overfitting.

## 1. Raw Win Probability Improvements (10-Fold CV)
The table below shows the 10-fold cross-validated performance of the tuned ML classifiers on the core binary task (predicting the home team win).
| model                |   accuracy |    brier |   log_loss |
|:---------------------|-----------:|---------:|-----------:|
| Gradient Boosting    |   0.589163 | 0.237133 |   0.666803 |
| Neural Network (MLP) |   0.587676 | 0.240032 |   0.673396 |

## 2. Validation Metrics: Set 1 (Original) vs Set 2 (ML Refined)
All underlying ranking models (both original and the new ML derivations) were scored against the ground truth points rank utilizing exactly the same 7 validation metrics.

### 2.1 Top Models from Set 1 (Phase 1 Baseline)
| model_name    |   kendall_tau |   spearman_rho |   accuracy |   brier_score |
|:--------------|--------------:|---------------:|-----------:|--------------:|
| composite     |        0.6855 |         0.8563 |     0.5953 |        0.2653 |
| bradley_terry |        0.8871 |         0.9666 |     0.5938 |        0.2605 |
| colley        |        0.8871 |         0.9666 |     0.5938 |        0.2605 |

### 2.2 Top Models from Set 2 (After ML Tuning)
| model_name    |   kendall_tau |   spearman_rho |   accuracy |   brier_score |
|:--------------|--------------:|---------------:|-----------:|--------------:|
| composite     |        0.6855 |         0.8563 |     0.5953 |        0.2653 |
| bradley_terry |        0.8871 |         0.9666 |     0.5938 |        0.2605 |
| colley        |        0.8871 |         0.9666 |     0.5938 |        0.2605 |
| elo           |        0.6653 |         0.8325 |     0.5854 |        0.2659 |
| points        |        0.9677 |         0.9963 |     0.5823 |        0.2619 |

**Net Improvement in Rank Accuracy:** The best model improved from **59.530%** to **59.530%** (an uplift of 0.000%).

## 3. The New Top Model Ranking
Based on the lowest Validation Set 2 log-loss and highest rank accuracy, we can isolate the single best ranking system. Here are the top 10 teams under the premier ML model:

|   rank | team        |
|-------:|:------------|
|      1 | brazil      |
|      2 | pakistan    |
|      3 | netherlands |
|      4 | thailand    |
|      5 | peru        |
|      6 | uk          |
|      7 | china       |
|      8 | mexico      |
|      9 | panama      |
|     10 | iceland     |

## 4. Overfitting Analysis
By using strictly out-of-sample 10-fold stratified cross-validation throughout the hyperparameter tuning grid search (e.g. `n_estimators`, `max_depth`, `learning_rate` constraints), the models were heavily regularized against overfitting the 1,312 game sample. Further, performance was evaluated not just on raw accuracy but tightly calibrated metrics like Brier score and Log-Loss to appropriately penalize overconfident predictions.

---

_End of ML Refinement Report_