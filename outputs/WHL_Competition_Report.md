# WHL 2026 — Wharton High School Data Science Competition
## World Hockey League Performance Analysis Report
**Generated:** 2026-02-28 16:42  |  **Prepared by:** Multi-Agent Analytics Pipeline

---

# Section 1: Data Overview & EDA Findings

## 1.1 Dataset Description

The WHL 2025 dataset contains **25,827 rows** representing line-pairing matchup records across
one fictional season of the World Hockey League. There are **1,312 games** across **32 teams**,
with each game containing approximately 18–20 rows capturing different offensive line / defensive
pairing combinations on ice simultaneously.

**Key structural facts:**
- Each row is a line-level matchup summary (not a full game)
- `toi` = time on ice in seconds for that specific pairing
- `home_off_line` / `away_off_line`: `first_off`, `second_off`, `PP_up`, `PP_kill_dwn`, `empty_net_line`
- All analysis filters to `first_off` + `second_off` for even-strength work; PP rows analyzed separately

**Important confounders addressed:**
1. **TOI differences** — all rates computed per 60 minutes (×3600/toi) rather than raw totals
2. **Defensive matchup quality** — Method 3 (disparity) explicitly adjusts for opponent defensive strength


## 1.2 Key Numeric Statistics
| Unnamed: 0               |   count |    mean |     std |   min |    25% |     50% |     75% |      max |   skew |
|:-------------------------|--------:|--------:|--------:|------:|-------:|--------:|--------:|---------:|-------:|
| toi                      |   25827 | 190.195 | 153.702 |  0.01 | 92.645 | 156.19  | 237.985 | 1559.67  |  2.267 |
| home_xg                  |   25827 |   0.159 |   0.306 |  0    |  0     |   0.09  |   0.188 |    5.544 |  5.26  |
| away_xg                  |   25827 |   0.143 |   0.264 |  0    |  0     |   0.082 |   0.175 |    4.412 |  5.038 |
| home_goals               |   25827 |   0.157 |   0.477 |  0    |  0     |   0     |   0     |    7     |  4.274 |
| away_goals               |   25827 |   0.135 |   0.428 |  0    |  0     |   0     |   0     |    7     |  4.189 |
| home_shots               |   25827 |   1.4   |   2.046 |  0    |  0     |   1     |   2     |   28     |  3.521 |
| away_shots               |   25827 |   1.329 |   1.875 |  0    |  0     |   1     |   2     |   23     |  3.271 |
| home_max_xg              |   25827 |   0.066 |   0.06  |  0    |  0     |   0.08  |   0.105 |    0.271 |  0.417 |
| away_max_xg              |   25827 |   0.062 |   0.058 |  0    |  0     |   0.074 |   0.1   |    0.262 |  0.467 |
| home_assists             |   25827 |   0.245 |   0.799 |  0    |  0     |   0     |   0     |   13     |  4.616 |
| away_assists             |   25827 |   0.211 |   0.714 |  0    |  0     |   0     |   0     |   13     |  4.494 |
| home_penalties_committed |   25827 |   0.316 |   1.314 |  0    |  0     |   0     |   0     |   16     |  5.119 |
| home_penalty_minutes     |   25827 |   0.646 |   2.695 |  0    |  0     |   0     |   0     |   34     |  5.162 |
| away_penalties_committed |   25827 |   0.345 |   1.437 |  0    |  0     |   0     |   0     |   19     |  5.2   |
| away_penalty_minutes     |   25827 |   0.704 |   2.94  |  0    |  0     |   0     |   0     |   38     |  5.253 |

## 1.3 Home Advantage
- **Overall home win rate:** 0.564 (56.4%)
- **OT/SO rate:** 0.220 (22.0%)
- **Regulation home win rate:** 0.576
- **OT/SO home win rate:** 0.521

## 1.4 Full EDA Findings
# WHL 2025 — EDA Report
Generated: 2026-02-28T16:40:02.451181

## 1. Dataset Structure
- Shape: (25827, 26)
- Columns: ['game_id', 'record_id', 'home_team', 'away_team', 'went_ot', 'home_off_line', 'home_def_pairing', 'away_off_line', 'away_def_pairing', 'home_goalie', 'away_goalie', 'toi', 'home_assists', 'home_shots', 'home_xg', 'home_max_xg', 'home_goals', 'away_assists', 'away_shots', 'away_xg', 'away_max_xg', 'away_goals', 'home_penalties_committed', 'home_penalty_minutes', 'away_penalties_committed', 'away_penalty_minutes']
- Unique games: 1312
- Records per game (mean): 19.69

## 2. Missing Values
  - No missing values found.

## 3. Categorical Fields
### home_off_line
| home_off_line   |   count |
|:----------------|--------:|
| first_off       |   11062 |
| second_off      |   11038 |
| PP_kill_dwn     |    1434 |
| PP_up           |    1305 |
| empty_net_line  |     988 |

### home_def_pairing
| home_def_pairing   |   count |
|:-------------------|--------:|
| second_def         |   11067 |
| first_def          |   11033 |
| PP_kill_dwn        |    1434 |
| PP_up              |    1305 |
| empty_net_line     |     988 |

### away_off_line
| away_off_line   |   count |
|:----------------|--------:|
| second_off      |   10960 |
| first_off       |   10935 |
| PP_kill_dwn     |    1389 |
| PP_up           |    1302 |
| empty_net_line  |    1241 |

### away_def_pairing
| away_def_pairing   |   count |
|:-------------------|--------:|
| second_def         |   10950 |
| first_def          |   10945 |
| PP_kill_dwn        |    1389 |
| PP_up              |    1302 |
| empty_net_line     |    1241 |

### went_ot
|   went_ot |   count |
|----------:|--------:|
|         0 |   20379 |
|         1 |    5448 |

## 4. Numeric Summary Statistics
|                          |   count |        mean |         std |   min |    25% |      50% |      75% |       max |     skew |
|:-------------------------|--------:|------------:|------------:|------:|-------:|---------:|---------:|----------:|---------:|
| toi                      |   25827 | 190.195     | 153.702     |  0.01 | 92.645 | 156.19   | 237.985  | 1559.67   | 2.26691  |
| home_xg                  |   25827 |   0.158953  |   0.305636  |  0    |  0     |   0.0898 |   0.1878 |    5.5435 | 5.2604   |
| away_xg                  |   25827 |   0.142801  |   0.264191  |  0    |  0     |   0.0825 |   0.1752 |    4.4123 | 5.03795  |
| home_goals               |   25827 |   0.157045  |   0.476548  |  0    |  0     |   0      |   0      |    7      | 4.274    |
| away_goals               |   25827 |   0.13544   |   0.427517  |  0    |  0     |   0      |   0      |    7      | 4.18863  |
| home_shots               |   25827 |   1.40024   |   2.04626   |  0    |  0     |   1      |   2      |   28      | 3.5212   |
| away_shots               |   25827 |   1.32911   |   1.87525   |  0    |  0     |   1      |   2      |   23      | 3.2712   |
| home_max_xg              |   25827 |   0.0663317 |   0.0604896 |  0    |  0     |   0.0801 |   0.105  |    0.2707 | 0.417094 |
| away_max_xg              |   25827 |   0.0624551 |   0.0580029 |  0    |  0     |   0.0745 |   0.0996 |    0.2622 | 0.466749 |
| home_assists             |   25827 |   0.245054  |   0.798532  |  0    |  0     |   0      |   0      |   13      | 4.61579  |
| away_assists             |   25827 |   0.211445  |   0.714388  |  0    |  0     |   0      |   0      |   13      | 4.49406  |
| home_penalties_committed |   25827 |   0.31649   |   1.31447   |  0    |  0     |   0      |   0      |   16      | 5.11904  |
| home_penalty_minutes     |   25827 |   0.646494  |   2.69504   |  0    |  0     |   0      |   0      |   34      | 5.16174  |
| away_penalties_committed |   25827 |   0.34491   |   1.43678   |  0    |  0     |   0      |   0      |   19      | 5.20004  |
| away_penalty_minutes     |   25827 |   0.703605  |   2.9404    |  0    |  0     |   0      |   0      |   38      | 5.25347  |

## 5. Game-Level Aggregated Stats
Games aggregated: 1312
Home win rate: 0.5640
OT/SO rate: 0.2195

## 6. Home Advantage Analysis
Overall home win rate: 0.5640
Regulation home win rate: 0.5762 (n=1024)
OT/SO home win rate: 0.5208 (n=288)
Goal margin distribution:
|   goal_diff |   count |
|------------:|--------:|
|          -9 |       1 |
|          -7 |       2 |
|          -6 |       7 |
|          -5 |      21 |
|          -4 |      43 |
|          -3 |      72 |
|          -2 |      82 |
|          -1 |     344 |
|           1 |     367 |
|           2 |     127 |
|           3 |      89 |
|           4 |      88 |
|           5 |      42 |
|           6 |      18 |
|           7 |       6 |
|           8 |       3 |

## 7. xG vs Actual Goals Correlation
Home xG vs Home Goals Pearson r: 0.4560
Away xG vs Away Goals Pearson r: 0.4381
Combined xG vs Goals Pearson r: 0.4586

## 8. xG Calibration (does xG=1.0 → ~1 goal)
|    | xg_bin      |   mean_xg |   mean_goals |     n |
|---:|:------------|----------:|-------------:|------:|
|  0 | (0.0, 0.25] |  0.128949 |     0.121828 | 23410 |
|  1 | (0.25, 0.5] |  0.33522  |     0.342544 |  5284 |
|  2 | (0.5, 0.75] |  0.606168 |     0.580989 |  1031 |
|  3 | (0.75, 1.0] |  0.86052  |     0.802935 |   477 |
|  4 | (1.0, 1.25] |  1.11718  |     1.02362  |   381 |
|  5 | (1.25, 1.5] |  1.37018  |     1.43609  |   266 |
|  6 | (1.5, 1.75] |  1.62024  |     1.58421  |   190 |
|  7 | (1.75, 2.0] |  1.87375  |     1.65972  |   144 |
|  8 | (2.0, 2.25] |  2.11943  |     2.11458  |    96 |
|  9 | (2.25, 2.5] |  2.36996  |     2.52     |    50 |
| 10 | (2.5, 2.75] |  2.61499  |     2.75     |    24 |
| 11 | (2.75, 3.0] |  2.84306  |     2.92308  |    26 |
| 12 | (3.0, 3.25] |  3.13571  |     2.93333  |    15 |

## 9. Power Play vs Even-Strength xG Rates
Even-strength home xG/60: 2.3471
Even-strength away xG/60: 2.2438
PP (home up) home xG/60: 7.7306
PP kill (home down) away xG/60: 7.0933

## 10. Goalie Goals Saved Above Expected (GSAx)
Goalies analyzed: 33
Top 5 GSAx:
|    | goalie        |     xga |   ga |    gsax |   gsax_per60 |
|---:|:--------------|--------:|-----:|--------:|-------------:|
| 25 | player_id_38  | 235.358 |  185 | 50.3583 |     0.583574 |
| 19 | player_id_257 | 237.305 |  192 | 45.3053 |     0.532898 |
| 10 | player_id_16  | 246.944 |  205 | 41.9443 |     0.500609 |
| 15 | player_id_218 | 213.931 |  176 | 37.9307 |     0.441233 |
|  4 | player_id_123 | 298.675 |  265 | 33.6754 |     0.393066 |
Bottom 5 GSAx:
|    | goalie        |      xga |   ga |     gsax |   gsax_per60 |
|---:|:--------------|---------:|-----:|---------:|-------------:|
| 12 | player_id_208 | 232.285  |  262 | -29.7147 |    -0.349771 |
|  1 | player_id_103 | 222.081  |  252 | -29.9186 |    -0.3516   |
| 17 | player_id_232 | 232.813  |  263 | -30.1872 |    -0.358802 |
|  0 | empty_net     |  38.7571 |   76 | -37.2429 |    -1.41638  |
| 30 | player_id_80  | 249.482  |  296 | -46.5176 |    -0.554099 |

## 11. Penalty Analysis
Penalty min vs home win corr: -0.1800
Penalty min vs away pen corr: 0.0563

## 12. Season Trends — First vs Second Half Games
Top 5 improvers (second half win% - first half win%):
|    | team        |   winpct_h1 |   winpct_h2 |    trend |
|---:|:------------|------------:|------------:|---------:|
| 30 | usa         |    0.3      |    0.547619 | 0.247619 |
| 19 | peru        |    0.512195 |    0.756098 | 0.243902 |
| 21 | rwanda      |    0.268293 |    0.463415 | 0.195122 |
| 16 | oman        |    0.341463 |    0.512195 | 0.170732 |
| 20 | philippines |    0.439024 |    0.609756 | 0.170732 |
Top 5 decliners:
|    | team      |   winpct_h1 |   winpct_h2 |     trend |
|---:|:----------|------------:|------------:|----------:|
|  0 | brazil    |    0.809524 |    0.6      | -0.209524 |
| 13 | morocco   |    0.547619 |    0.35     | -0.197619 |
| 17 | pakistan  |    0.682927 |    0.512195 | -0.170732 |
|  2 | china     |    0.657895 |    0.5      | -0.157895 |
|  6 | guatemala |    0.575    |    0.452381 | -0.122619 |

#

---

# Section 2: Phase 1a — Team Power Rankings

## 2.1 Model 1: Raw Points Standings
_Standard NHL-style: 2pts win, 1pt OT loss. Baseline model._

|   rank | team         |   score |   points |   gd |     xgd |
|-------:|:-------------|--------:|---------:|-----:|--------:|
|      1 | brazil       |     122 |      122 |   87 |  50.653 |
|      2 | netherlands  |     114 |      114 |   69 |  40.695 |
|      3 | peru         |     112 |      112 |   78 |  29.616 |
|      4 | thailand     |     107 |      107 |   46 |  73.075 |
|      5 | pakistan     |     106 |      106 |   51 |  51.241 |
|      6 | india        |     104 |      104 |   28 |   1.404 |
|      7 | china        |     101 |      101 |   46 |  34.938 |
|      8 | panama       |     101 |      101 |   42 |  16.061 |
|      9 | iceland      |     101 |      101 |   29 | -18.611 |
|     10 | philippines  |      99 |       99 |   12 | -22.549 |
|     11 | ethiopia     |      98 |       98 |   20 | -23.268 |
|     12 | singapore    |      94 |       94 |  -14 | -42.964 |
|     13 | guatemala    |      92 |       92 |   -5 |  22.878 |
|     14 | uk           |      91 |       91 |   33 |  36.311 |
|     15 | indonesia    |      90 |       90 |   11 | -22.437 |
|     16 | vietnam      |      90 |       90 |  -34 | -46.238 |
|     17 | serbia       |      88 |       88 |    5 |  13.114 |
|     18 | uae          |      88 |       88 |  -48 | -30.969 |
|     19 | mexico       |      87 |       87 |  -17 |  41.193 |
|     20 | new_zealand  |      86 |       86 |   -7 |   2.933 |
|     21 | south_korea  |      86 |       86 |  -14 |   8.656 |
|     22 | saudi_arabia |      85 |       85 |  -10 | -12.003 |
|     23 | morocco      |      85 |       85 |  -20 |   5.879 |
|     24 | france       |      85 |       85 |  -24 |  32.513 |
|     25 | canada       |      83 |       83 |  -43 |   7.55  |
|     26 | switzerland  |      81 |       81 |  -28 | -32.09  |
|     27 | usa          |      80 |       80 |  -47 | -34.305 |
|     28 | germany      |      78 |       78 |  -21 | -13.895 |
|     29 | oman         |      77 |       77 |  -42 | -34.555 |
|     30 | rwanda       |      68 |       68 |  -63 | -32.312 |
|     31 | mongolia     |      67 |       67 |  -65 | -80.898 |
|     32 | kazakhstan   |      66 |       66 |  -55 | -21.616 |

## 2.2 Model 2: xG Differential/60 (ES)
_Even-strength xGF/60 minus xGA/60. Adjusts for TOI._

|   rank | team         |   score |   es_xgf60 |   es_xga60 |   es_xgd60 |
|-------:|:-------------|--------:|-----------:|-----------:|-----------:|
|      1 | pakistan     |   0.876 |      2.967 |      2.091 |      0.876 |
|      2 | thailand     |   0.847 |      2.9   |      2.053 |      0.847 |
|      3 | brazil       |   0.789 |      2.751 |      1.963 |      0.789 |
|      4 | mexico       |   0.553 |      2.525 |      1.972 |      0.553 |
|      5 | south_korea  |   0.476 |      2.624 |      2.149 |      0.476 |
|      6 | china        |   0.374 |      2.464 |      2.09  |      0.374 |
|      7 | guatemala    |   0.348 |      2.487 |      2.139 |      0.348 |
|      8 | peru         |   0.241 |      2.229 |      1.988 |      0.241 |
|      9 | serbia       |   0.174 |      2.729 |      2.556 |      0.174 |
|     10 | netherlands  |   0.142 |      2.062 |      1.92  |      0.142 |
|     11 | oman         |   0.135 |      2.518 |      2.384 |      0.135 |
|     12 | rwanda       |   0.119 |      2.25  |      2.131 |      0.119 |
|     13 | uk           |   0.084 |      2.562 |      2.478 |      0.084 |
|     14 | canada       |   0.064 |      2.371 |      2.308 |      0.064 |
|     15 | new_zealand  |   0.034 |      2.249 |      2.215 |      0.034 |
|     16 | morocco      |   0.026 |      2.349 |      2.323 |      0.026 |
|     17 | iceland      |   0.001 |      2.317 |      2.316 |      0.001 |
|     18 | panama       |  -0.008 |      2.39  |      2.398 |     -0.008 |
|     19 | india        |  -0.044 |      2.285 |      2.328 |     -0.044 |
|     20 | ethiopia     |  -0.138 |      2.363 |      2.501 |     -0.138 |
|     21 | france       |  -0.146 |      2.3   |      2.446 |     -0.146 |
|     22 | usa          |  -0.167 |      2.422 |      2.59  |     -0.167 |
|     23 | saudi_arabia |  -0.246 |      1.98  |      2.226 |     -0.246 |
|     24 | switzerland  |  -0.253 |      1.824 |      2.078 |     -0.253 |
|     25 | germany      |  -0.28  |      2.259 |      2.54  |     -0.28  |
|     26 | singapore    |  -0.344 |      2.375 |      2.719 |     -0.344 |
|     27 | vietnam      |  -0.349 |      2.1   |      2.449 |     -0.349 |
|     28 | uae          |  -0.466 |      1.805 |      2.27  |     -0.466 |
|     29 | philippines  |  -0.488 |      1.881 |      2.369 |     -0.488 |
|     30 | kazakhstan   |  -0.574 |      1.75  |      2.325 |     -0.574 |
|     31 | indonesia    |  -0.646 |      1.862 |      2.508 |     -0.646 |
|     32 | mongolia     |  -0.946 |      1.676 |      2.622 |     -0.946 |

## 2.3 Model 3: Pythagorean Expectation
_xGF^k / (xGF^k + xGA^k). Optimal k tuned empirically._

|   rank | team         |   score |   pyth_winpct |     xgf |     xga |   optimal_k |
|-------:|:-------------|--------:|--------------:|--------:|--------:|------------:|
|      1 | thailand     |   0.605 |         0.605 | 294.737 | 221.662 |         1.5 |
|      2 | brazil       |   0.577 |         0.577 | 272.479 | 221.827 |         1.5 |
|      3 | pakistan     |   0.574 |         0.574 | 284.703 | 233.462 |         1.5 |
|      4 | netherlands  |   0.568 |         0.568 | 242.499 | 201.803 |         1.5 |
|      5 | mexico       |   0.563 |         0.563 | 263.958 | 222.765 |         1.5 |
|      6 | china        |   0.555 |         0.555 | 255.917 | 220.979 |         1.5 |
|      7 | uk           |   0.553 |         0.553 | 276.312 | 240.001 |         1.5 |
|      8 | france       |   0.549 |         0.549 | 266.652 | 234.14  |         1.5 |
|      9 | peru         |   0.548 |         0.548 | 244.55  | 214.934 |         1.5 |
|     10 | guatemala    |   0.535 |         0.535 | 255.688 | 232.81  |         1.5 |
|     11 | panama       |   0.524 |         0.524 | 257.455 | 241.394 |         1.5 |
|     12 | serbia       |   0.518 |         0.518 | 277.288 | 264.174 |         1.5 |
|     13 | south_korea  |   0.513 |         0.513 | 259.857 | 251.201 |         1.5 |
|     14 | canada       |   0.512 |         0.512 | 241.134 | 233.584 |         1.5 |
|     15 | morocco      |   0.509 |         0.509 | 249.503 | 243.625 |         1.5 |
|     16 | new_zealand  |   0.505 |         0.505 | 241.265 | 238.331 |         1.5 |
|     17 | india        |   0.502 |         0.502 | 239.336 | 237.932 |         1.5 |
|     18 | saudi_arabia |   0.48  |         0.48  | 218.965 | 230.968 |         1.5 |
|     19 | germany      |   0.479 |         0.479 | 239.107 | 253.002 |         1.5 |
|     20 | iceland      |   0.471 |         0.471 | 230.062 | 248.674 |         1.5 |
|     21 | ethiopia     |   0.465 |         0.465 | 239.42  | 262.688 |         1.5 |
|     22 | kazakhstan   |   0.463 |         0.463 | 209.805 | 231.421 |         1.5 |
|     23 | indonesia    |   0.463 |         0.463 | 215.9   | 238.338 |         1.5 |
|     24 | philippines  |   0.462 |         0.462 | 213.585 | 236.134 |         1.5 |
|     25 | usa          |   0.451 |         0.451 | 247.393 | 281.697 |         1.5 |
|     26 | oman         |   0.451 |         0.451 | 244.937 | 279.493 |         1.5 |
|     27 | rwanda       |   0.45  |         0.45  | 223.809 | 256.122 |         1.5 |
|     28 | uae          |   0.449 |         0.449 | 211.395 | 242.364 |         1.5 |
|     29 | switzerland  |   0.446 |         0.446 | 205.292 | 237.382 |         1.5 |
|     30 | singapore    |   0.442 |         0.442 | 257.021 | 299.984 |         1.5 |
|     31 | vietnam      |   0.431 |         0.431 | 225.778 | 272.016 |         1.5 |
|     32 | mongolia     |   0.369 |         0.369 | 187.599 | 268.497 |         1.5 |

## 2.4 Model 4: Elo Rating System
_K=20, 1500 base, +100 home advantage. Chronological game processing._

|   rank | team         |   score |     elo |
|-------:|:-------------|--------:|--------:|
|      1 | brazil       | 1633.08 | 1633.08 |
|      2 | netherlands  | 1598.38 | 1598.38 |
|      3 | thailand     | 1585.08 | 1585.08 |
|      4 | iceland      | 1569.99 | 1569.99 |
|      5 | china        | 1557.44 | 1557.44 |
|      6 | peru         | 1556.68 | 1556.68 |
|      7 | pakistan     | 1552.51 | 1552.51 |
|      8 | new_zealand  | 1552.47 | 1552.47 |
|      9 | ethiopia     | 1541.54 | 1541.54 |
|     10 | india        | 1535.28 | 1535.28 |
|     11 | serbia       | 1523.17 | 1523.17 |
|     12 | guatemala    | 1522.22 | 1522.22 |
|     13 | philippines  | 1512.63 | 1512.63 |
|     14 | indonesia    | 1511.06 | 1511.06 |
|     15 | morocco      | 1502.64 | 1502.64 |
|     16 | south_korea  | 1489.62 | 1489.62 |
|     17 | singapore    | 1484.74 | 1484.74 |
|     18 | uae          | 1476.94 | 1476.94 |
|     19 | saudi_arabia | 1472.48 | 1472.48 |
|     20 | switzerland  | 1472.28 | 1472.28 |
|     21 | canada       | 1471.25 | 1471.25 |
|     22 | panama       | 1470.98 | 1470.98 |
|     23 | vietnam      | 1469.8  | 1469.8  |
|     24 | uk           | 1467.06 | 1467.06 |
|     25 | oman         | 1463.33 | 1463.33 |
|     26 | mexico       | 1458.85 | 1458.85 |
|     27 | germany      | 1456.1  | 1456.1  |
|     28 | france       | 1437.14 | 1437.14 |
|     29 | usa          | 1429.08 | 1429.08 |
|     30 | kazakhstan   | 1428.85 | 1428.85 |
|     31 | mongolia     | 1401.17 | 1401.17 |
|     32 | rwanda       | 1396.15 | 1396.15 |

## 2.5 Model 5: Colley Matrix
_Linear system solving for strength-of-schedule-adjusted ratings._

|   rank | team         |   score |   colley_rating |
|-------:|:-------------|--------:|----------------:|
|      1 | brazil       |   0.442 |           0.442 |
|      2 | netherlands  |   0.399 |           0.399 |
|      3 | peru         |   0.376 |           0.376 |
|      4 | thailand     |   0.35  |           0.35  |
|      5 | pakistan     |   0.34  |           0.34  |
|      6 | india        |   0.34  |           0.34  |
|      7 | china        |   0.319 |           0.319 |
|      8 | iceland      |   0.309 |           0.309 |
|      9 | panama       |   0.306 |           0.306 |
|     10 | ethiopia     |   0.273 |           0.273 |
|     11 | philippines  |   0.272 |           0.272 |
|     12 | guatemala    |   0.261 |           0.261 |
|     13 | indonesia    |   0.254 |           0.254 |
|     14 | serbia       |   0.248 |           0.248 |
|     15 | new_zealand  |   0.239 |           0.239 |
|     16 | singapore    |   0.235 |           0.235 |
|     17 | uk           |   0.229 |           0.229 |
|     18 | saudi_arabia |   0.227 |           0.227 |
|     19 | vietnam      |   0.227 |           0.227 |
|     20 | south_korea  |   0.226 |           0.226 |
|     21 | mexico       |   0.216 |           0.216 |
|     22 | uae          |   0.212 |           0.212 |
|     23 | france       |   0.203 |           0.203 |
|     24 | morocco      |   0.2   |           0.2   |
|     25 | canada       |   0.197 |           0.197 |
|     26 | switzerland  |   0.196 |           0.196 |
|     27 | germany      |   0.194 |           0.194 |
|     28 | oman         |   0.186 |           0.186 |
|     29 | usa          |   0.182 |           0.182 |
|     30 | rwanda       |   0.129 |           0.129 |
|     31 | kazakhstan   |   0.121 |           0.121 |
|     32 | mongolia     |   0.092 |           0.092 |

## 2.6 Model 6: Bradley-Terry Pairwise
_MLE pairwise model: P(i beats j) = s_i/(s_i+s_j)._

|   rank | team         |   score |   bt_strength |
|-------:|:-------------|--------:|--------------:|
|      1 | brazil       |   2.351 |         2.351 |
|      2 | netherlands  |   1.906 |         1.906 |
|      3 | peru         |   1.719 |         1.719 |
|      4 | thailand     |   1.534 |         1.534 |
|      5 | pakistan     |   1.462 |         1.462 |
|      6 | india        |   1.461 |         1.461 |
|      7 | china        |   1.339 |         1.339 |
|      8 | iceland      |   1.283 |         1.283 |
|      9 | panama       |   1.264 |         1.264 |
|     10 | ethiopia     |   1.103 |         1.103 |
|     11 | philippines  |   1.098 |         1.098 |
|     12 | guatemala    |   1.047 |         1.047 |
|     13 | indonesia    |   1.018 |         1.018 |
|     14 | serbia       |   0.99  |         0.99  |
|     15 | new_zealand  |   0.952 |         0.952 |
|     16 | singapore    |   0.937 |         0.937 |
|     17 | uk           |   0.913 |         0.913 |
|     18 | saudi_arabia |   0.907 |         0.907 |
|     19 | vietnam      |   0.907 |         0.907 |
|     20 | south_korea  |   0.902 |         0.902 |
|     21 | mexico       |   0.867 |         0.867 |
|     22 | uae          |   0.849 |         0.849 |
|     23 | france       |   0.82  |         0.82  |
|     24 | morocco      |   0.809 |         0.809 |
|     25 | canada       |   0.798 |         0.798 |
|     26 | switzerland  |   0.794 |         0.794 |
|     27 | germany      |   0.787 |         0.787 |
|     28 | oman         |   0.762 |         0.762 |
|     29 | usa          |   0.749 |         0.749 |
|     30 | rwanda       |   0.592 |         0.592 |
|     31 | kazakhstan   |   0.575 |         0.575 |
|     32 | mongolia     |   0.5   |         0.5   |

## 2.7 Model 7: Composite Weighted Score
_Z-score weighted sum: xGD(0.35)+GD(0.15)+GSAx(0.20)+PP(0.15)+PK(0.15)._

|   rank | team         |   score |   composite |   z_xgd60 |   z_gd |   z_gsax60 |   z_pp |   z_pk |
|-------:|:-------------|--------:|------------:|----------:|-------:|-----------:|-------:|-------:|
|      1 | brazil       |   1.344 |       1.344 |     1.861 |  2.118 |      0.986 | -0.202 |  1.387 |
|      2 | pakistan     |   1.21  |       1.21  |     2.068 |  1.242 |      0.552 |  0.459 |  0.805 |
|      3 | netherlands  |   1.079 |       1.079 |     0.324 |  1.68  |      0.77  |  2.216 |  1.515 |
|      4 | thailand     |   0.983 |       0.983 |     1.999 |  1.12  |     -1.304 |  1.466 |  1.043 |
|      5 | peru         |   0.813 |       0.813 |     0.56  |  1.899 |      1.104 | -0.022 |  0.763 |
|      6 | uk           |   0.596 |       0.596 |     0.185 |  0.804 |      0.824 |  1.458 |  0.181 |
|      7 | china        |   0.533 |       0.533 |     0.874 |  1.12  |      0.791 | -0.23  | -0.435 |
|      8 | mexico       |   0.388 |       0.388 |     1.302 | -0.414 |     -1.437 |  0.366 |  1.513 |
|      9 | panama       |   0.382 |       0.382 |    -0.033 |  1.023 |      0.813 |  0.711 | -0.195 |
|     10 | iceland      |   0.362 |       0.362 |    -0.012 |  0.706 |      1.245 | -1.126 |  1.203 |
|     11 | guatemala    |   0.332 |       0.332 |     0.812 | -0.122 |     -0.408 |  0.682 |  0.3   |
|     12 | india        |   0.154 |       0.154 |    -0.117 |  0.682 |      1.435 | -1.21  | -0.083 |
|     13 | philippines  |   0.072 |       0.072 |    -1.174 |  0.292 |      1.603 |  0.339 |  0.45  |
|     14 | serbia       |   0.045 |       0.045 |     0.399 |  0.122 |     -0.278 |  0.508 | -0.891 |
|     15 | saudi_arabia |  -0.013 |      -0.013 |    -0.599 | -0.243 |      0.697 | -1.015 |  1.64  |
|     16 | ethiopia     |  -0.042 |      -0.042 |    -0.341 |  0.487 |      0.325 |  0.696 | -1.104 |
|     17 | new_zealand  |  -0.1   |      -0.1   |     0.067 | -0.17  |      0.194 | -0.146 | -0.767 |
|     18 | singapore    |  -0.151 |      -0.151 |    -0.832 | -0.341 |      0.893 |  1.761 | -1.674 |
|     19 | south_korea  |  -0.169 |      -0.169 |     1.117 | -0.341 |     -2.244 |  0.337 | -0.739 |
|     20 | france       |  -0.171 |      -0.171 |    -0.36  | -0.584 |     -1.454 |  0.764 |  1.463 |
|     21 | indonesia    |  -0.37  |      -0.37  |    -1.549 |  0.268 |      0.802 | -1.049 |  0.858 |
|     22 | morocco      |  -0.425 |      -0.425 |     0.049 | -0.487 |     -1.248 | -0.724 | -0.071 |
|     23 | rwanda       |  -0.453 |      -0.453 |     0.269 | -1.534 |     -0.626 | -0.93  | -0.353 |
|     24 | canada       |  -0.473 |      -0.473 |     0.137 | -1.047 |     -1.502 | -0.562 |  0.138 |
|     25 | vietnam      |  -0.56  |      -0.56  |    -0.844 | -0.828 |      0.287 |  0.077 | -1.395 |
|     26 | germany      |  -0.591 |      -0.591 |    -0.681 | -0.511 |     -1.104 |  1.003 | -1.37  |
|     27 | oman         |  -0.616 |      -0.616 |     0.306 | -1.023 |     -0.42  | -1.694 | -1.542 |
|     28 | usa          |  -0.633 |      -0.633 |    -0.411 | -1.144 |     -0.489 | -0.88  | -0.586 |
|     29 | uae          |  -0.749 |      -0.749 |    -1.12  | -1.169 |     -0.571 | -0.096 | -0.356 |
|     30 | switzerland  |  -0.756 |      -0.756 |    -0.616 | -0.682 |      0.032 | -1.624 | -1.338 |
|     31 | kazakhstan   |  -0.951 |      -0.951 |    -1.378 | -1.339 |     -0.924 |  0.324 | -0.88  |
|     32 | mongolia     |  -1.07  |      -1.07  |    -2.263 | -1.583 |      0.655 | -1.658 |  0.518 |

## 2.8 Model 8: Logistic Regression
_LR on xGF/60, xGA/60 features. Team strength from coefficients._

|   rank | team         |   score |   lr_score |   es_xgf60 |   es_xga60 |
|-------:|:-------------|--------:|-----------:|-----------:|-----------:|
|      1 | serbia       |   0.695 |      0.695 |      2.729 |      2.556 |
|      2 | singapore    |   0.676 |      0.676 |      2.375 |      2.719 |
|      3 | uk           |   0.664 |      0.664 |      2.562 |      2.478 |
|      4 | usa          |   0.663 |      0.663 |      2.422 |      2.59  |
|      5 | pakistan     |   0.657 |      0.657 |      2.967 |      2.091 |
|      6 | oman         |   0.645 |      0.645 |      2.518 |      2.384 |
|      7 | ethiopia     |   0.643 |      0.643 |      2.363 |      2.501 |
|      8 | thailand     |   0.643 |      0.643 |      2.9   |      2.053 |
|      9 | germany      |   0.636 |      0.636 |      2.259 |      2.54  |
|     10 | panama       |   0.632 |      0.632 |      2.39  |      2.398 |
|     11 | france       |   0.628 |      0.628 |      2.3   |      2.446 |
|     12 | south_korea  |   0.624 |      0.624 |      2.624 |      2.149 |
|     13 | canada       |   0.616 |      0.616 |      2.371 |      2.308 |
|     14 | morocco      |   0.616 |      0.616 |      2.349 |      2.323 |
|     15 | brazil       |   0.612 |      0.612 |      2.751 |      1.963 |
|     16 | iceland      |   0.611 |      0.611 |      2.317 |      2.316 |
|     17 | india        |   0.609 |      0.609 |      2.285 |      2.328 |
|     18 | guatemala    |   0.606 |      0.606 |      2.487 |      2.139 |
|     19 | vietnam      |   0.604 |      0.604 |      2.1   |      2.449 |
|     20 | china        |   0.596 |      0.596 |      2.464 |      2.09  |
|     21 | new_zealand  |   0.588 |      0.588 |      2.249 |      2.215 |
|     22 | mexico       |   0.586 |      0.586 |      2.525 |      1.972 |
|     23 | indonesia    |   0.584 |      0.584 |      1.862 |      2.508 |
|     24 | mongolia     |   0.578 |      0.578 |      1.676 |      2.622 |
|     25 | rwanda       |   0.576 |      0.576 |      2.25  |      2.131 |
|     26 | philippines  |   0.566 |      0.566 |      1.881 |      2.369 |
|     27 | saudi_arabia |   0.558 |      0.558 |      1.98  |      2.226 |
|     28 | peru         |   0.553 |      0.553 |      2.229 |      1.988 |
|     29 | kazakhstan   |   0.544 |      0.544 |      1.75  |      2.325 |
|     30 | uae          |   0.543 |      0.543 |      1.805 |      2.27  |
|     31 | netherlands  |   0.523 |      0.523 |      2.062 |      1.92  |
|     32 | switzerland  |   0.518 |      0.518 |      1.824 |      2.078 |

## 2.9 Model 9: Random Forest
_RF with permutation importance. Teams ranked by weighted feature score._

|   rank | team         |   score |   rf_score |
|-------:|:-------------|--------:|-----------:|
|      1 | thailand     |   0.162 |      0.162 |
|      2 | netherlands  |   0.158 |      0.158 |
|      3 | pakistan     |   0.153 |      0.153 |
|      4 | uk           |   0.148 |      0.148 |
|      5 | brazil       |   0.144 |      0.144 |
|      6 | guatemala    |   0.144 |      0.144 |
|      7 | mexico       |   0.143 |      0.143 |
|      8 | singapore    |   0.143 |      0.143 |
|      9 | south_korea  |   0.14  |      0.14  |
|     10 | serbia       |   0.138 |      0.138 |
|     11 | panama       |   0.138 |      0.138 |
|     12 | china        |   0.135 |      0.135 |
|     13 | peru         |   0.135 |      0.135 |
|     14 | ethiopia     |   0.134 |      0.134 |
|     15 | germany      |   0.133 |      0.133 |
|     16 | france       |   0.133 |      0.133 |
|     17 | new_zealand  |   0.128 |      0.128 |
|     18 | philippines  |   0.124 |      0.124 |
|     19 | vietnam      |   0.122 |      0.122 |
|     20 | canada       |   0.122 |      0.122 |
|     21 | rwanda       |   0.12  |      0.12  |
|     22 | morocco      |   0.119 |      0.119 |
|     23 | kazakhstan   |   0.119 |      0.119 |
|     24 | iceland      |   0.117 |      0.117 |
|     25 | uae          |   0.117 |      0.117 |
|     26 | india        |   0.115 |      0.115 |
|     27 | usa          |   0.114 |      0.114 |
|     28 | saudi_arabia |   0.112 |      0.112 |
|     29 | oman         |   0.111 |      0.111 |
|     30 | switzerland  |   0.104 |      0.104 |
|     31 | indonesia    |   0.103 |      0.103 |
|     32 | mongolia     |   0.09  |      0.09  |

## 2.10 Model 10: Monte Carlo Simulation
_Poisson xGF sampling, 1,000 season simulations. Mean±SD points shown._

|   rank | team         |   score |   mean_pts |   std_pts |
|-------:|:-------------|--------:|-----------:|----------:|
|      1 | thailand     |  104.7  |     104.7  |      7.85 |
|      2 | pakistan     |  101.33 |     101.33 |      8.41 |
|      3 | serbia       |   99.6  |      99.6  |      8.25 |
|      4 | uk           |   99.42 |      99.42 |      8.14 |
|      5 | brazil       |   98.37 |      98.37 |      8.78 |
|      6 | france       |   96.75 |      96.75 |      8.42 |
|      7 | mexico       |   94.84 |      94.84 |      8.76 |
|      8 | south_korea  |   93.66 |      93.66 |      8.42 |
|      9 | singapore    |   93.39 |      93.39 |      8.34 |
|     10 | panama       |   93.14 |      93.14 |      8.84 |
|     11 | guatemala    |   92.99 |      92.99 |      8.62 |
|     12 | china        |   92.97 |      92.97 |      8.23 |
|     13 | morocco      |   91.58 |      91.58 |      8.82 |
|     14 | peru         |   90.34 |      90.34 |      8.82 |
|     15 | usa          |   89.92 |      89.92 |      8.7  |
|     16 | oman         |   89.47 |      89.47 |      8.74 |
|     17 | netherlands  |   88.81 |      88.81 |      8.53 |
|     18 | new_zealand  |   88.8  |      88.8  |      8.75 |
|     19 | canada       |   87.6  |      87.6  |      8.73 |
|     20 | india        |   87.4  |      87.4  |      8.94 |
|     21 | ethiopia     |   87.38 |      87.38 |      8.2  |
|     22 | germany      |   87.05 |      87.05 |      8.45 |
|     23 | iceland      |   85.06 |      85.06 |      8.43 |
|     24 | vietnam      |   83.06 |      83.06 |      8.56 |
|     25 | rwanda       |   81.63 |      81.63 |      8.94 |
|     26 | saudi_arabia |   81.07 |      81.07 |      8.69 |
|     27 | indonesia    |   80.02 |      80.02 |      8.34 |
|     28 | philippines  |   79.19 |      79.19 |      8.7  |
|     29 | uae          |   78.8  |      78.8  |      8.53 |
|     30 | kazakhstan   |   77.98 |      77.98 |      8.39 |
|     31 | switzerland  |   75.93 |      75.93 |      8.53 |
|     32 | mongolia     |   68.9  |      68.9  |      8.62 |

## 2.11 Side-by-Side Ranking Comparison (All 10 Models)
| team         |   rank_points |   rank_xgd60 |   rank_pythagorean |   rank_elo |   rank_colley |   rank_bt |   rank_composite |   rank_logistic |   rank_rf |   rank_montecarlo |   mean_rank |   rank_variance |   consensus_rank |
|:-------------|--------------:|-------------:|-------------------:|-----------:|--------------:|----------:|-----------------:|----------------:|----------:|------------------:|------------:|----------------:|-----------------:|
| thailand     |             4 |            2 |                  1 |          3 |             4 |         4 |                4 |               8 |         1 |                 1 |         3.2 |           4.622 |                1 |
| brazil       |             1 |            3 |                  2 |          1 |             1 |         1 |                1 |              15 |         5 |                 5 |         3.5 |          18.944 |                2 |
| pakistan     |             5 |            1 |                  3 |          7 |             5 |         5 |                2 |               5 |         3 |                 2 |         3.8 |           3.511 |                3 |
| netherlands  |             2 |           10 |                  4 |          2 |             2 |         2 |                3 |              31 |         2 |                17 |         7.5 |          92.5   |                4 |
| china        |             7 |            6 |                  6 |          5 |             7 |         7 |                7 |              20 |        12 |                12 |         8.9 |          20.989 |                5 |
| peru         |             3 |            8 |                  9 |          6 |             3 |         3 |                5 |              28 |        13 |                14 |         9.2 |          59.511 |                6 |
| serbia       |            17 |            9 |                 12 |         11 |            14 |        14 |               14 |               1 |        10 |                 3 |        10.5 |          25.611 |                7 |
| uk           |            14 |           13 |                  7 |         24 |            17 |        17 |                6 |               3 |         4 |                 4 |        10.9 |          50.767 |                8 |
| guatemala    |            13 |            7 |                 10 |         12 |            12 |        12 |               11 |              18 |         6 |                11 |        11.2 |          10.844 |                9 |
| panama       |             8 |           18 |                 11 |         22 |             9 |         9 |                9 |              10 |        11 |                10 |        11.7 |          20.9   |               10 |
| iceland      |             9 |           17 |                 20 |          4 |             8 |         8 |               10 |              16 |        24 |                23 |        13.9 |          49.211 |               12 |
| india        |             6 |           19 |                 17 |         10 |             6 |         6 |               12 |              17 |        26 |                20 |        13.9 |          48.322 |               12 |
| ethiopia     |            11 |           20 |                 21 |          9 |            10 |        10 |               16 |               7 |        14 |                21 |        13.9 |          28.1   |               12 |
| mexico       |            19 |            4 |                  5 |         26 |            21 |        21 |                8 |              22 |         7 |                 7 |        14   |          71.778 |               14 |
| south_korea  |            21 |            5 |                 13 |         16 |            20 |        20 |               19 |              12 |         9 |                 8 |        14.3 |          32.9   |               15 |
| singapore    |            12 |           26 |                 30 |         17 |            16 |        16 |               18 |               2 |         8 |                 9 |        15.4 |          69.156 |               16 |
| new_zealand  |            20 |           15 |                 16 |          8 |            15 |        15 |               17 |              21 |        17 |                18 |        16.2 |          12.622 |               17 |
| france       |            24 |           21 |                  8 |         28 |            23 |        23 |               20 |              11 |        16 |                 6 |        18   |          55.111 |               18 |
| philippines  |            10 |           29 |                 24 |         13 |            11 |        11 |               13 |              26 |        18 |                28 |        18.3 |          59.122 |               19 |
| morocco      |            23 |           16 |                 15 |         15 |            24 |        24 |               22 |              14 |        22 |                13 |        18.8 |          20.622 |               20 |
| canada       |            25 |           14 |                 14 |         21 |            25 |        25 |               24 |              13 |        20 |                19 |        20   |          23.778 |               21 |
| indonesia    |            15 |           31 |                 23 |         14 |            13 |        13 |               21 |              23 |        31 |                27 |        21.1 |          50.767 |               22 |
| saudi_arabia |            22 |           23 |                 18 |         19 |            18 |        18 |               15 |              27 |        28 |                26 |        21.4 |          20.044 |               23 |
| vietnam      |            16 |           27 |                 31 |         23 |            19 |        19 |               25 |              19 |        19 |                24 |        22.2 |          21.289 |               24 |
| oman         |            29 |           11 |                 26 |         25 |            28 |        28 |               27 |               6 |        29 |                16 |        22.5 |          70.056 |               25 |
| germany      |            28 |           25 |                 19 |         27 |            27 |        27 |               26 |               9 |        15 |                22 |        22.5 |          40.056 |               25 |
| usa          |            27 |           22 |                 25 |         29 |            29 |        29 |               28 |               4 |        27 |                15 |        23.5 |          65.833 |               27 |
| uae          |            18 |           28 |                 28 |         18 |            22 |        22 |               29 |              30 |        25 |                29 |        24.9 |          21.211 |               28 |
| rwanda       |            30 |           12 |                 27 |         32 |            30 |        30 |               23 |              25 |        21 |                25 |        25.5 |          34.944 |               29 |
| switzerland  |            26 |           24 |                 29 |         20 |            26 |        26 |               30 |              32 |        30 |                31 |        27.4 |          13.6   |               30 |
| kazakhstan   |            32 |           30 |                 22 |         30 |            31 |        31 |               31 |              29 |        23 |                30 |        28.9 |          12.1   |               31 |
| mongolia     |            31 |           32 |                 32 |         31 |            32 |        32 |               32 |              24 |        32 |                32 |        31   |           6.222 |               32 |

## 2.12 Recommended Final Power Ranking
The **consensus ranking** (mean rank across all 10 models) is our recommended final ranking.
Teams with low rank variance are robustly ranked; those with high variance should be scrutinized.

| team         |   mean_rank |   rank_variance |   recommended_rank |
|:-------------|------------:|----------------:|-------------------:|
| thailand     |         3.2 |           4.622 |                  1 |
| brazil       |         3.5 |          18.944 |                  2 |
| pakistan     |         3.8 |           3.511 |                  3 |
| netherlands  |         7.5 |          92.5   |                  4 |
| china        |         8.9 |          20.989 |                  5 |
| peru         |         9.2 |          59.511 |                  6 |
| serbia       |        10.5 |          25.611 |                  7 |
| uk           |        10.9 |          50.767 |                  8 |
| guatemala    |        11.2 |          10.844 |                  9 |
| panama       |        11.7 |          20.9   |                 10 |
| iceland      |        13.9 |          49.211 |                 11 |
| india        |        13.9 |          48.322 |                 12 |
| ethiopia     |        13.9 |          28.1   |                 13 |
| mexico       |        14   |          71.778 |                 14 |
| south_korea  |        14.3 |          32.9   |                 15 |
| singapore    |        15.4 |          69.156 |                 16 |
| new_zealand  |        16.2 |          12.622 |                 17 |
| france       |        18   |          55.111 |                 18 |
| philippines  |        18.3 |          59.122 |                 19 |
| morocco      |        18.8 |          20.622 |                 20 |
| canada       |        20   |          23.778 |                 21 |
| indonesia    |        21.1 |          50.767 |                 22 |
| saudi_arabia |        21.4 |          20.044 |                 23 |
| vietnam      |        22.2 |          21.289 |                 24 |
| oman         |        22.5 |          70.056 |                 25 |
| germany      |        22.5 |          40.056 |                 26 |
| usa          |        23.5 |          65.833 |                 27 |
| uae          |        24.9 |          21.211 |                 28 |
| rwanda       |        25.5 |          34.944 |                 29 |
| switzerland  |        27.4 |          13.6   |                 30 |
| kazakhstan   |        28.9 |          12.1   |                 31 |
| mongolia     |        31   |           6.222 |                 32 |

---

# Section 3: Phase 1a — Win Probabilities (Round 1 Matchups)

## 3.1 All 16 Matchup Probabilities (Five Methods + Ensemble)
|   game | home_team   | away_team    |   p_lr |   p_elo |   p_bt |   p_log5 |   p_mc |   p_ensemble |   disagreement | flag_disagree   |
|-------:|:------------|:-------------|-------:|--------:|-------:|---------:|-------:|-------------:|---------------:|:----------------|
|      1 | brazil      | kazakhstan   |  0.708 |   0.852 |  0.822 |    0.612 |  0.62  |        0.723 |          0.24  | YES             |
|      2 | netherlands | mongolia     |  0.704 |   0.847 |  0.811 |    0.693 |  0.612 |        0.733 |          0.235 | YES             |
|      3 | peru        | rwanda       |  0.588 |   0.818 |  0.766 |    0.598 |  0.54  |        0.662 |          0.277 | YES             |
|      4 | thailand    | oman         |  0.658 |   0.782 |  0.694 |    0.651 |  0.59  |        0.675 |          0.191 | YES             |
|      5 | pakistan    | germany      |  0.7   |   0.756 |  0.677 |    0.594 |  0.582 |        0.662 |          0.174 | YES             |
|      6 | india       | usa          |  0.596 |   0.766 |  0.688 |    0.551 |  0.487 |        0.618 |          0.279 | YES             |
|      7 | panama      | switzerland  |  0.561 |   0.638 |  0.642 |    0.578 |  0.601 |        0.604 |          0.081 | nan             |
|      8 | iceland     | canada       |  0.559 |   0.758 |  0.645 |    0.459 |  0.476 |        0.579 |          0.299 | YES             |
|      9 | china       | france       |  0.639 |   0.78  |  0.648 |    0.506 |  0.478 |        0.61  |          0.302 | YES             |
|     10 | philippines | morocco      |  0.511 |   0.653 |  0.605 |    0.454 |  0.428 |        0.53  |          0.225 | YES             |
|     11 | ethiopia    | saudi_arabia |  0.552 |   0.726 |  0.578 |    0.485 |  0.543 |        0.577 |          0.24  | YES             |
|     12 | singapore   | new_zealand  |  0.49  |   0.546 |  0.526 |    0.438 |  0.528 |        0.506 |          0.108 | YES             |
|     13 | guatemala   | south_korea  |  0.559 |   0.682 |  0.567 |    0.522 |  0.491 |        0.564 |          0.191 | YES             |
|     14 | uk          | mexico       |  0.486 |   0.651 |  0.543 |    0.489 |  0.522 |        0.538 |          0.164 | YES             |
|     15 | vietnam     | serbia       |  0.525 |   0.567 |  0.508 |    0.413 |  0.4   |        0.482 |          0.167 | YES             |
|     16 | indonesia   | uae          |  0.524 |   0.684 |  0.575 |    0.514 |  0.51  |        0.561 |          0.174 | YES             |

### ⚠️ 15 Matchups with >10pp Model Disagreement (warrant extra scrutiny):
|   game | home_team   | away_team    |   p_lr |   p_elo |   p_bt |   p_log5 |   p_mc |   p_ensemble |   disagreement | flag_disagree   |
|-------:|:------------|:-------------|-------:|--------:|-------:|---------:|-------:|-------------:|---------------:|:----------------|
|      1 | brazil      | kazakhstan   |  0.708 |   0.852 |  0.822 |    0.612 |  0.62  |        0.723 |          0.24  | YES             |
|      2 | netherlands | mongolia     |  0.704 |   0.847 |  0.811 |    0.693 |  0.612 |        0.733 |          0.235 | YES             |
|      3 | peru        | rwanda       |  0.588 |   0.818 |  0.766 |    0.598 |  0.54  |        0.662 |          0.277 | YES             |
|      4 | thailand    | oman         |  0.658 |   0.782 |  0.694 |    0.651 |  0.59  |        0.675 |          0.191 | YES             |
|      5 | pakistan    | germany      |  0.7   |   0.756 |  0.677 |    0.594 |  0.582 |        0.662 |          0.174 | YES             |
|      6 | india       | usa          |  0.596 |   0.766 |  0.688 |    0.551 |  0.487 |        0.618 |          0.279 | YES             |
|      8 | iceland     | canada       |  0.559 |   0.758 |  0.645 |    0.459 |  0.476 |        0.579 |          0.299 | YES             |
|      9 | china       | france       |  0.639 |   0.78  |  0.648 |    0.506 |  0.478 |        0.61  |          0.302 | YES             |
|     10 | philippines | morocco      |  0.511 |   0.653 |  0.605 |    0.454 |  0.428 |        0.53  |          0.225 | YES             |
|     11 | ethiopia    | saudi_arabia |  0.552 |   0.726 |  0.578 |    0.485 |  0.543 |        0.577 |          0.24  | YES             |
|     12 | singapore   | new_zealand  |  0.49  |   0.546 |  0.526 |    0.438 |  0.528 |        0.506 |          0.108 | YES             |
|     13 | guatemala   | south_korea  |  0.559 |   0.682 |  0.567 |    0.522 |  0.491 |        0.564 |          0.191 | YES             |
|     14 | uk          | mexico       |  0.486 |   0.651 |  0.543 |    0.489 |  0.522 |        0.538 |          0.164 | YES             |
|     15 | vietnam     | serbia       |  0.525 |   0.567 |  0.508 |    0.413 |  0.4   |        0.482 |          0.167 | YES             |
|     16 | indonesia   | uae          |  0.524 |   0.684 |  0.575 |    0.514 |  0.51  |        0.561 |          0.174 | YES             |

## 3.2 Win Probability Model Calibration (LR)
| metric               |   value |
|:---------------------|--------:|
| in_sample_accuracy   |   0.585 |
| in_sample_brier      |   0.241 |
| in_sample_logloss    |   0.674 |
| cv10_acc_mean        |   0.582 |
| cv10_acc_std         |   0.028 |
| cv10_brier_mean      |   0.242 |
| cv10_logloss_mean    |   0.677 |
| loto_acc_mean        |   0.574 |
| loto_acc_std         |   0.052 |
| baseline_always_home |   0.564 |
| baseline_higher_pts  |   0.582 |
| baseline_higher_xgd  |   0.546 |

---

# Section 4: Phase 1b — Line Disparity Analysis

## 4.1 Method 1: Raw xG ratio (sum first_off / sum second_off). No adjustments.
|   rank | team         |   ratio |   f1_xg |   f2_xg |
|-------:|:-------------|--------:|--------:|--------:|
|      1 | usa          |   1.405 |  81.27  |  57.858 |
|      2 | guatemala    |   1.375 |  85.135 |  61.91  |
|      3 | saudi_arabia |   1.372 |  70.256 |  51.192 |
|      4 | uae          |   1.372 |  62.693 |  45.696 |
|      5 | france       |   1.36  |  78.88  |  57.994 |
|      6 | iceland      |   1.344 |  77.545 |  57.685 |
|      7 | singapore    |   1.262 |  80.333 |  63.681 |
|      8 | new_zealand  |   1.244 |  72.189 |  58.049 |
|      9 | panama       |   1.217 |  78.587 |  64.578 |
|     10 | rwanda       |   1.214 |  68.895 |  56.746 |
|     11 | peru         |   1.208 |  75.46  |  62.441 |
|     12 | uk           |   1.204 |  86.9   |  72.196 |
|     13 | india        |   1.177 |  75.36  |  64.014 |
|     14 | serbia       |   1.149 |  84.046 |  73.168 |
|     15 | south_korea  |   1.14  |  80.456 |  70.586 |
|     16 | netherlands  |   1.123 |  67.179 |  59.842 |
|     17 | mongolia     |   1.082 |  50.699 |  46.844 |
|     18 | china        |   1.07  |  79.406 |  74.236 |
|     19 | mexico       |   1.068 |  77.936 |  72.953 |
|     20 | canada       |   1.051 |  73.939 |  70.36  |
|     21 | pakistan     |   1.041 |  86.865 |  83.437 |
|     22 | philippines  |   1.03  |  61.014 |  59.262 |
|     23 | morocco      |   1.024 |  73.205 |  71.482 |
|     24 | kazakhstan   |   1.017 |  52.787 |  51.894 |
|     25 | oman         |   0.998 |  72.123 |  72.239 |
|     26 | thailand     |   0.994 |  85.518 |  86.054 |
|     27 | brazil       |   0.992 |  80.83  |  81.457 |
|     28 | indonesia    |   0.988 |  57.101 |  57.767 |
|     29 | germany      |   0.979 |  67.378 |  68.826 |
|     30 | vietnam      |   0.953 |  61.713 |  64.773 |
|     31 | ethiopia     |   0.938 |  68.039 |  72.521 |
|     32 | switzerland  |   0.899 |  52.475 |  58.358 |

## 4.2 Method 2: xG/60 ratio. Fixes TOI confounding.
|   rank | team         |   ratio |   f1_xg60 |   f2_xg60 |
|-------:|:-------------|--------:|----------:|----------:|
|      1 | usa          |   1.369 |     2.727 |     1.992 |
|      2 | saudi_arabia |   1.359 |     2.238 |     1.647 |
|      3 | guatemala    |   1.356 |     2.802 |     2.066 |
|      4 | uae          |   1.354 |     1.989 |     1.469 |
|      5 | france       |   1.341 |     2.548 |     1.9   |
|      6 | iceland      |   1.322 |     2.584 |     1.955 |
|      7 | singapore    |   1.256 |     2.622 |     2.088 |
|      8 | new_zealand  |   1.229 |     2.427 |     1.974 |
|      9 | peru         |   1.199 |     2.38  |     1.985 |
|     10 | panama       |   1.199 |     2.545 |     2.122 |
|     11 | rwanda       |   1.195 |     2.331 |     1.951 |
|     12 | uk           |   1.168 |     2.71  |     2.321 |
|     13 | india        |   1.166 |     2.422 |     2.077 |
|     14 | serbia       |   1.117 |     2.81  |     2.515 |
|     15 | netherlands  |   1.111 |     2.138 |     1.924 |
|     16 | south_korea  |   1.103 |     2.711 |     2.458 |
|     17 | mexico       |   1.056 |     2.556 |     2.42  |
|     18 | china        |   1.047 |     2.498 |     2.385 |
|     19 | mongolia     |   1.046 |     1.641 |     1.569 |
|     20 | pakistan     |   1.034 |     2.977 |     2.881 |
|     21 | canada       |   1.012 |     2.37  |     2.342 |
|     22 | kazakhstan   |   1.001 |     1.668 |     1.667 |
|     23 | philippines  |   1     |     1.84  |     1.84  |
|     24 | morocco      |   0.997 |     2.312 |     2.318 |
|     25 | oman         |   0.99  |     2.474 |     2.5   |
|     26 | brazil       |   0.982 |     2.702 |     2.753 |
|     27 | thailand     |   0.97  |     2.822 |     2.911 |
|     28 | indonesia    |   0.961 |     1.805 |     1.878 |
|     29 | germany      |   0.96  |     2.172 |     2.263 |
|     30 | vietnam      |   0.946 |     2.014 |     2.128 |
|     31 | ethiopia     |   0.905 |     2.223 |     2.457 |
|     32 | switzerland  |   0.889 |     1.709 |     1.923 |

## 4.3 Method 3: Matchup-adjusted xG/60. Scales for opponent defensive quality.
|   rank | team         |   ratio |   f1_adj_xg60 |   f2_adj_xg60 |
|-------:|:-------------|--------:|--------------:|--------------:|
|      1 | usa          |   1.38  |         2.737 |         1.983 |
|      2 | saudi_arabia |   1.36  |         2.237 |         1.645 |
|      3 | guatemala    |   1.358 |         2.805 |         2.066 |
|      4 | uae          |   1.357 |         1.993 |         1.468 |
|      5 | france       |   1.345 |         2.553 |         1.898 |
|      6 | iceland      |   1.327 |         2.593 |         1.954 |
|      7 | singapore    |   1.255 |         2.626 |         2.092 |
|      8 | new_zealand  |   1.233 |         2.431 |         1.971 |
|      9 | peru         |   1.204 |         2.385 |         1.981 |
|     10 | panama       |   1.201 |         2.548 |         2.122 |
|     11 | rwanda       |   1.197 |         2.337 |         1.952 |
|     12 | uk           |   1.169 |         2.714 |         2.322 |
|     13 | india        |   1.166 |         2.421 |         2.076 |
|     14 | serbia       |   1.117 |         2.813 |         2.518 |
|     15 | netherlands  |   1.114 |         2.143 |         1.924 |
|     16 | south_korea  |   1.101 |         2.711 |         2.463 |
|     17 | mexico       |   1.059 |         2.562 |         2.419 |
|     18 | china        |   1.051 |         2.502 |         2.381 |
|     19 | mongolia     |   1.05  |         1.643 |         1.565 |
|     20 | pakistan     |   1.03  |         2.968 |         2.88  |
|     21 | canada       |   1.014 |         2.375 |         2.342 |
|     22 | kazakhstan   |   1.007 |         1.675 |         1.664 |
|     23 | philippines  |   1.007 |         1.848 |         1.835 |
|     24 | morocco      |   0.996 |         2.306 |         2.316 |
|     25 | oman         |   0.991 |         2.481 |         2.503 |
|     26 | brazil       |   0.987 |         2.714 |         2.749 |
|     27 | thailand     |   0.972 |         2.83  |         2.912 |
|     28 | germany      |   0.961 |         2.175 |         2.263 |
|     29 | indonesia    |   0.961 |         1.806 |         1.88  |
|     30 | vietnam      |   0.947 |         2.013 |         2.125 |
|     31 | ethiopia     |   0.906 |         2.229 |         2.459 |
|     32 | switzerland  |   0.887 |         1.706 |         1.924 |

## 4.4 Method 4: Goals/60 ratio. Noisier but direct.
|   rank | team         |   ratio |   f1_g60 |   f2_g60 |
|-------:|:-------------|--------:|---------:|---------:|
|      1 | brazil       |   1.413 |    3.343 |    2.366 |
|      2 | serbia       |   1.269 |    3.009 |    2.372 |
|      3 | germany      |   1.148 |    2.643 |    2.302 |
|      4 | singapore    |   1.093 |    2.187 |    2     |
|      5 | ethiopia     |   1.037 |    2.81  |    2.71  |
|      6 | mongolia     |   1.024 |    1.716 |    1.675 |
|      7 | thailand     |   1.021 |    2.97  |    2.909 |
|      8 | france       |   0.986 |    2.035 |    2.064 |
|      9 | kazakhstan   |   0.965 |    1.612 |    1.67  |
|     10 | china        |   0.939 |    2.202 |    2.345 |
|     11 | india        |   0.936 |    2.217 |    2.368 |
|     12 | morocco      |   0.874 |    1.927 |    2.206 |
|     13 | oman         |   0.85  |    2.264 |    2.665 |
|     14 | canada       |   0.824 |    1.891 |    2.297 |
|     15 | netherlands  |   0.815 |    1.782 |    2.186 |
|     16 | mexico       |   0.815 |    2.001 |    2.455 |
|     17 | rwanda       |   0.81  |    1.725 |    2.131 |
|     18 | saudi_arabia |   0.792 |    1.529 |    1.93  |
|     19 | iceland      |   0.761 |    2.166 |    2.847 |
|     20 | uae          |   0.757 |    1.46  |    1.929 |
|     21 | guatemala    |   0.756 |    1.942 |    2.57  |
|     22 | panama       |   0.755 |    1.911 |    2.53  |
|     23 | peru         |   0.729 |    1.924 |    2.638 |
|     24 | indonesia    |   0.726 |    1.676 |    2.308 |
|     25 | uk           |   0.725 |    1.84  |    2.539 |
|     26 | vietnam      |   0.722 |    1.566 |    2.168 |
|     27 | new_zealand  |   0.716 |    1.681 |    2.347 |
|     28 | south_korea  |   0.697 |    2.426 |    3.483 |
|     29 | philippines  |   0.687 |    1.387 |    2.019 |
|     30 | usa          |   0.684 |    2.047 |    2.995 |
|     31 | switzerland  |   0.669 |    1.498 |    2.24  |
|     32 | pakistan     |   0.644 |    2.399 |    3.729 |

## 4.5 Method 5: Shots/60 ratio. Volume-based measure.
|   rank | team         |   ratio |   f1_s60 |   f2_s60 |
|-------:|:-------------|--------:|---------:|---------:|
|      1 | guatemala    |   1.313 |   29.228 |   22.259 |
|      2 | saudi_arabia |   1.27  |   22.429 |   17.662 |
|      3 | serbia       |   1.263 |   29.991 |   23.75  |
|      4 | rwanda       |   1.25  |   26.22  |   20.97  |
|      5 | iceland      |   1.238 |   25.593 |   20.673 |
|      6 | uae          |   1.213 |   21.26  |   17.523 |
|      7 | france       |   1.198 |   24.58  |   20.512 |
|      8 | south_korea  |   1.112 |   29.517 |   26.539 |
|      9 | singapore    |   1.09  |   26.307 |   24.136 |
|     10 | usa          |   1.086 |   24.966 |   22.996 |
|     11 | uk           |   1.068 |   24.792 |   23.208 |
|     12 | morocco      |   1.061 |   25.836 |   24.358 |
|     13 | thailand     |   1.052 |   25.773 |   24.49  |
|     14 | peru         |   1.033 |   24.889 |   24.093 |
|     15 | new_zealand  |   1.03  |   23.967 |   23.265 |
|     16 | china        |   1.022 |   23.311 |   22.811 |
|     17 | kazakhstan   |   1.011 |   20.224 |   20.012 |
|     18 | oman         |   0.991 |   24.599 |   24.818 |
|     19 | switzerland  |   0.986 |   21.887 |   22.208 |
|     20 | india        |   0.983 |   26.253 |   26.7   |
|     21 | philippines  |   0.962 |   21.171 |   22.018 |
|     22 | netherlands  |   0.961 |   21.098 |   21.957 |
|     23 | ethiopia     |   0.953 |   24.078 |   25.275 |
|     24 | brazil       |   0.94  |   23.401 |   24.905 |
|     25 | pakistan     |   0.929 |   27.386 |   29.485 |
|     26 | mongolia     |   0.923 |   20.522 |   22.244 |
|     27 | panama       |   0.915 |   22.605 |   24.713 |
|     28 | canada       |   0.914 |   23.785 |   26.028 |
|     29 | germany      |   0.91  |   20.954 |   23.016 |
|     30 | mexico       |   0.906 |   25.387 |   28.035 |
|     31 | vietnam      |   0.898 |   20.981 |   23.359 |
|     32 | indonesia    |   0.851 |   20.833 |   24.48  |

## 4.6 Method 6: xG share (distance from 50/50 balance).
|   rank | team         |   ratio |   f1_xg_share |   disparity_from_05 |
|-------:|:-------------|--------:|--------------:|--------------------:|
|      1 | usa          |   0.084 |         0.584 |               0.084 |
|      2 | guatemala    |   0.079 |         0.579 |               0.079 |
|      3 | saudi_arabia |   0.078 |         0.578 |               0.078 |
|      4 | uae          |   0.078 |         0.578 |               0.078 |
|      5 | france       |   0.076 |         0.576 |               0.076 |
|      6 | iceland      |   0.073 |         0.573 |               0.073 |
|      7 | singapore    |   0.058 |         0.558 |               0.058 |
|      8 | new_zealand  |   0.054 |         0.554 |               0.054 |
|      9 | panama       |   0.049 |         0.549 |               0.049 |
|     10 | rwanda       |   0.048 |         0.548 |               0.048 |
|     11 | peru         |   0.047 |         0.547 |               0.047 |
|     12 | uk           |   0.046 |         0.546 |               0.046 |
|     13 | india        |   0.041 |         0.541 |               0.041 |
|     14 | serbia       |   0.035 |         0.535 |               0.035 |
|     15 | south_korea  |   0.033 |         0.533 |               0.033 |
|     16 | netherlands  |   0.029 |         0.529 |               0.029 |
|     17 | switzerland  |   0.026 |         0.474 |               0.026 |
|     18 | mongolia     |   0.02  |         0.52  |               0.02  |
|     19 | china        |   0.017 |         0.517 |               0.017 |
|     20 | mexico       |   0.016 |         0.516 |               0.016 |
|     21 | ethiopia     |   0.016 |         0.484 |               0.016 |
|     22 | canada       |   0.012 |         0.512 |               0.012 |
|     23 | vietnam      |   0.012 |         0.488 |               0.012 |
|     24 | pakistan     |   0.01  |         0.51  |               0.01  |
|     25 | philippines  |   0.007 |         0.507 |               0.007 |
|     26 | morocco      |   0.006 |         0.506 |               0.006 |
|     27 | germany      |   0.005 |         0.495 |               0.005 |
|     28 | kazakhstan   |   0.004 |         0.504 |               0.004 |
|     29 | indonesia    |   0.003 |         0.497 |               0.003 |
|     30 | brazil       |   0.002 |         0.498 |               0.002 |
|     31 | thailand     |   0.002 |         0.498 |               0.002 |
|     32 | oman         |   0     |         0.5   |               0     |

## 4.7 Method 7: Z-score gap. League-standardized first vs second line xG/60.
|   rank | team         |   ratio |   z_first |   z_second |   z_gap |
|-------:|:-------------|--------:|----------:|-----------:|--------:|
|      1 | guatemala    |   1.962 |     1.453 |     -0.509 |   1.962 |
|      2 | usa          |   1.96  |     1.253 |     -0.707 |   1.96  |
|      3 | france       |   1.726 |     0.775 |     -0.95  |   1.726 |
|      4 | iceland      |   1.676 |     0.872 |     -0.805 |   1.676 |
|      5 | saudi_arabia |   1.576 |    -0.05  |     -1.626 |   1.576 |
|      6 | singapore    |   1.422 |     0.972 |     -0.449 |   1.422 |
|      7 | uae          |   1.386 |    -0.713 |     -2.099 |   1.386 |
|      8 | new_zealand  |   1.205 |     0.452 |     -0.753 |   1.205 |
|      9 | panama       |   1.127 |     0.767 |     -0.359 |   1.127 |
|     10 | peru         |   1.054 |     0.329 |     -0.726 |   1.054 |
|     11 | uk           |   1.037 |     1.207 |      0.17  |   1.037 |
|     12 | rwanda       |   1.013 |     0.197 |     -0.816 |   1.013 |
|     13 | india        |   0.919 |     0.439 |     -0.48  |   0.919 |
|     14 | serbia       |   0.787 |     1.474 |      0.687 |   0.787 |
|     15 | south_korea  |   0.673 |     1.21  |      0.537 |   0.673 |
|     16 | netherlands  |   0.57  |    -0.318 |     -0.888 |   0.57  |
|     17 | mexico       |   0.362 |     0.797 |      0.435 |   0.362 |
|     18 | china        |   0.301 |     0.642 |      0.341 |   0.301 |
|     19 | pakistan     |   0.257 |     1.919 |      1.662 |   0.257 |
|     20 | mongolia     |   0.191 |    -1.641 |     -1.832 |   0.191 |
|     21 | canada       |   0.075 |     0.302 |      0.226 |   0.075 |
|     22 | kazakhstan   |   0.003 |    -1.569 |     -1.572 |   0.003 |
|     23 | philippines  |  -0.001 |    -1.111 |     -1.11  |  -0.001 |
|     24 | morocco      |  -0.017 |     0.147 |      0.164 |  -0.017 |
|     25 | oman         |  -0.07  |     0.579 |      0.649 |  -0.07  |
|     26 | brazil       |  -0.135 |     1.186 |      1.321 |  -0.135 |
|     27 | indonesia    |  -0.194 |    -1.204 |     -1.01  |  -0.194 |
|     28 | thailand     |  -0.236 |     1.506 |      1.742 |  -0.236 |
|     29 | germany      |  -0.242 |    -0.226 |      0.016 |  -0.242 |
|     30 | vietnam      |  -0.305 |    -0.648 |     -0.344 |  -0.305 |
|     31 | switzerland  |  -0.57  |    -1.46  |     -0.89  |  -0.57  |
|     32 | ethiopia     |  -0.624 |    -0.091 |      0.533 |  -0.624 |

## 4.8 Method 8: OLS regression controlling for team and defensive quality.
|   rank | team         |   ratio |   reg_gap |
|-------:|:-------------|--------:|----------:|
|      1 | iceland      |   0.611 |     0.611 |
|      2 | saudi_arabia |   0.49  |     0.49  |
|      3 | guatemala    |   0.439 |     0.439 |
|      4 | singapore    |   0.429 |     0.429 |
|      5 | france       |   0.386 |     0.386 |
|      6 | new_zealand  |   0.322 |     0.322 |
|      7 | uk           |   0.268 |     0.268 |
|      8 | usa          |   0.259 |     0.259 |
|      9 | netherlands  |   0.227 |     0.227 |
|     10 | uae          |   0.212 |     0.212 |
|     11 | india        |   0.208 |     0.208 |
|     12 | south_korea  |   0.15  |     0.15  |
|     13 | peru         |   0.075 |     0.075 |
|     14 | china        |   0.07  |     0.07  |
|     15 | thailand     |   0.035 |     0.035 |
|     16 | pakistan     |  -0.01  |    -0.01  |
|     17 | canada       |  -0.078 |    -0.078 |
|     18 | serbia       |  -0.101 |    -0.101 |
|     19 | brazil       |  -0.107 |    -0.107 |
|     20 | mexico       |  -0.118 |    -0.118 |
|     21 | panama       |  -0.12  |    -0.12  |
|     22 | mongolia     |  -0.171 |    -0.171 |
|     23 | switzerland  |  -0.172 |    -0.172 |
|     24 | ethiopia     |  -0.203 |    -0.203 |
|     25 | indonesia    |  -0.208 |    -0.208 |
|     26 | rwanda       |  -0.234 |    -0.234 |
|     27 | philippines  |  -0.242 |    -0.242 |
|     28 | vietnam      |  -0.251 |    -0.251 |
|     29 | morocco      |  -0.272 |    -0.272 |
|     30 | oman         |  -0.318 |    -0.318 |
|     31 | germany      |  -0.345 |    -0.345 |
|     32 | kazakhstan   |  -0.673 |    -0.673 |

## 4.9 Method 9: TOI-weighted average xG/60 per line.
|   rank | team         |   ratio |   f1_toi_wt_xg60 |   f2_toi_wt_xg60 |
|-------:|:-------------|--------:|-----------------:|-----------------:|
|      1 | usa          |   1.369 |            2.727 |            1.992 |
|      2 | saudi_arabia |   1.359 |            2.238 |            1.647 |
|      3 | guatemala    |   1.356 |            2.802 |            2.066 |
|      4 | uae          |   1.354 |            1.989 |            1.469 |
|      5 | france       |   1.341 |            2.548 |            1.9   |
|      6 | iceland      |   1.322 |            2.584 |            1.955 |
|      7 | singapore    |   1.256 |            2.622 |            2.088 |
|      8 | new_zealand  |   1.229 |            2.427 |            1.974 |
|      9 | peru         |   1.199 |            2.38  |            1.985 |
|     10 | panama       |   1.199 |            2.545 |            2.122 |
|     11 | rwanda       |   1.195 |            2.331 |            1.951 |
|     12 | uk           |   1.168 |            2.71  |            2.321 |
|     13 | india        |   1.166 |            2.422 |            2.077 |
|     14 | serbia       |   1.117 |            2.81  |            2.515 |
|     15 | netherlands  |   1.111 |            2.138 |            1.924 |
|     16 | south_korea  |   1.103 |            2.711 |            2.458 |
|     17 | mexico       |   1.056 |            2.556 |            2.42  |
|     18 | china        |   1.047 |            2.498 |            2.385 |
|     19 | mongolia     |   1.046 |            1.641 |            1.569 |
|     20 | pakistan     |   1.034 |            2.977 |            2.881 |
|     21 | canada       |   1.012 |            2.37  |            2.342 |
|     22 | kazakhstan   |   1.001 |            1.668 |            1.667 |
|     23 | philippines  |   1     |            1.84  |            1.84  |
|     24 | morocco      |   0.997 |            2.312 |            2.318 |
|     25 | oman         |   0.99  |            2.474 |            2.5   |
|     26 | brazil       |   0.982 |            2.702 |            2.753 |
|     27 | thailand     |   0.97  |            2.822 |            2.911 |
|     28 | indonesia    |   0.961 |            1.805 |            1.878 |
|     29 | germany      |   0.96  |            2.172 |            2.263 |
|     30 | vietnam      |   0.946 |            2.014 |            2.128 |
|     31 | ethiopia     |   0.905 |            2.223 |            2.457 |
|     32 | switzerland  |   0.889 |            1.709 |            1.923 |

## 4.10 Method 10: Bootstrap CI (n=1,000). Reports mean ± 95% CI.
|   rank | team         |   ratio |   boot_mean |   boot_lo |   boot_hi |   boot_ci_width | flag_wide_ci   |
|-------:|:-------------|--------:|------------:|----------:|----------:|----------------:|:---------------|
|      1 | usa          |   1.37  |       1.37  |     1.264 |     1.487 |           0.224 | WIDE           |
|      2 | saudi_arabia |   1.362 |       1.362 |     1.265 |     1.471 |           0.206 | WIDE           |
|      3 | guatemala    |   1.357 |       1.357 |     1.256 |     1.472 |           0.216 | WIDE           |
|      4 | uae          |   1.355 |       1.355 |     1.242 |     1.473 |           0.23  | WIDE           |
|      5 | france       |   1.342 |       1.342 |     1.24  |     1.455 |           0.216 | WIDE           |
|      6 | iceland      |   1.324 |       1.324 |     1.223 |     1.435 |           0.212 | WIDE           |
|      7 | singapore    |   1.257 |       1.257 |     1.161 |     1.359 |           0.198 | nan            |
|      8 | new_zealand  |   1.229 |       1.229 |     1.148 |     1.317 |           0.169 | nan            |
|      9 | peru         |   1.199 |       1.199 |     1.107 |     1.291 |           0.185 | nan            |
|     10 | panama       |   1.198 |       1.198 |     1.102 |     1.305 |           0.203 | WIDE           |
|     11 | rwanda       |   1.197 |       1.197 |     1.103 |     1.3   |           0.197 | nan            |
|     12 | uk           |   1.168 |       1.168 |     1.081 |     1.269 |           0.188 | nan            |
|     13 | india        |   1.167 |       1.167 |     1.091 |     1.242 |           0.151 | nan            |
|     14 | serbia       |   1.118 |       1.118 |     1.043 |     1.2   |           0.157 | nan            |
|     15 | netherlands  |   1.11  |       1.11  |     1.01  |     1.213 |           0.202 | WIDE           |
|     16 | south_korea  |   1.103 |       1.103 |     1.015 |     1.198 |           0.183 | nan            |
|     17 | mexico       |   1.057 |       1.057 |     0.975 |     1.147 |           0.172 | nan            |
|     18 | mongolia     |   1.048 |       1.048 |     0.958 |     1.138 |           0.18  | nan            |
|     19 | china        |   1.048 |       1.048 |     0.956 |     1.136 |           0.18  | nan            |
|     20 | pakistan     |   1.034 |       1.034 |     0.958 |     1.111 |           0.153 | nan            |
|     21 | canada       |   1.012 |       1.012 |     0.935 |     1.098 |           0.163 | nan            |
|     22 | kazakhstan   |   1.002 |       1.002 |     0.916 |     1.1   |           0.184 | nan            |
|     23 | philippines  |   1.002 |       1.002 |     0.924 |     1.082 |           0.158 | nan            |
|     24 | morocco      |   0.996 |       0.996 |     0.916 |     1.079 |           0.163 | nan            |
|     25 | oman         |   0.993 |       0.993 |     0.914 |     1.073 |           0.16  | nan            |
|     26 | brazil       |   0.983 |       0.983 |     0.901 |     1.068 |           0.167 | nan            |
|     27 | thailand     |   0.97  |       0.97  |     0.886 |     1.058 |           0.172 | nan            |
|     28 | germany      |   0.963 |       0.963 |     0.882 |     1.051 |           0.17  | nan            |
|     29 | indonesia    |   0.962 |       0.962 |     0.883 |     1.051 |           0.168 | nan            |
|     30 | vietnam      |   0.947 |       0.947 |     0.861 |     1.039 |           0.178 | nan            |
|     31 | ethiopia     |   0.906 |       0.906 |     0.837 |     0.985 |           0.148 | nan            |
|     32 | switzerland  |   0.889 |       0.889 |     0.834 |     0.954 |           0.12  | nan            |

## 4.11 Consensus Top 10 Teams by Line Disparity
**This is the final Phase 1b submission answer.**

|   consensus_rank | team         |   mean_rank |   rank_variance |
|-----------------:|:-------------|------------:|----------------:|
|                1 | saudi_arabia |         4.1 |          24.767 |
|                2 | guatemala    |         4.2 |          35.511 |
|                3 | france       |         5.3 |           1.789 |
|                4 | usa          |         5.6 |          84.489 |
|                5 | iceland      |         6.5 |          21.833 |
|                5 | singapore    |         6.5 |           2.278 |
|                7 | uae          |         6.7 |          25.789 |
|                8 | new_zealand  |        10.4 |          39.6   |
|                9 | peru         |        11.8 |          18.622 |
|               10 | serbia       |        12.1 |          27.211 |

## 4.12 Method Correlation Matrix (Spearman ρ)
| Unnamed: 0                |   01_raw_xg_ratio |   02_xg_per60_ratio |   03_matchup_adj_xg60 |   04_goals_per60_ratio |   05_shots_per60_ratio |   06_xg_share_proportion |   07_zscore_gap |   08_regression_line_effect |   09_toi_weighted_quality |   10_bootstrap_ci_ratio |
|:--------------------------|------------------:|--------------------:|----------------------:|-----------------------:|-----------------------:|-------------------------:|----------------:|----------------------------:|--------------------------:|------------------------:|
| 01_raw_xg_ratio           |             1     |               0.995 |                 0.995 |                 -0.172 |                  0.688 |                    0.906 |           0.989 |                       0.782 |                     0.995 |                   0.995 |
| 02_xg_per60_ratio         |             0.995 |               1     |                 1     |                 -0.172 |                  0.677 |                    0.901 |           0.992 |                       0.788 |                     1     |                   0.999 |
| 03_matchup_adj_xg60       |             0.995 |               1     |                 1     |                 -0.164 |                  0.678 |                    0.901 |           0.991 |                       0.786 |                     1     |                   1     |
| 04_goals_per60_ratio      |            -0.172 |              -0.172 |                -0.164 |                  1     |                  0.001 |                   -0.258 |          -0.188 |                      -0.147 |                    -0.172 |                  -0.162 |
| 05_shots_per60_ratio      |             0.688 |               0.677 |                 0.678 |                  0.001 |                  1     |                    0.642 |           0.669 |                       0.578 |                     0.677 |                   0.674 |
| 06_xg_share_proportion    |             0.906 |               0.901 |                 0.901 |                 -0.258 |                  0.642 |                    1     |           0.897 |                       0.766 |                     0.901 |                   0.902 |
| 07_zscore_gap             |             0.989 |               0.992 |                 0.991 |                 -0.188 |                  0.669 |                    0.897 |           1     |                       0.798 |                     0.992 |                   0.99  |
| 08_regression_line_effect |             0.782 |               0.788 |                 0.786 |                 -0.147 |                  0.578 |                    0.766 |           0.798 |                       1     |                     0.788 |                   0.783 |
| 09_toi_weighted_quality   |             0.995 |               1     |                 1     |                 -0.172 |                  0.677 |                    0.901 |           0.992 |                       0.788 |                     1     |                   0.999 |
| 10_bootstrap_ci_ratio     |             0.995 |               0.999 |                 1     |                 -0.162 |                  0.674 |                    0.902 |           0.99  |                       0.783 |                     0.999 |                   1     |

---

# Section 5: Validation Summary

## 5.2 Model Agreement Matrix (% games where models agree on predicted winner)
| index         |   points |   xgd60 |   pythagorean |   elo |   colley |   bradley_terry |   composite |   logistic |   random_forest |   monte_carlo |
|:--------------|---------:|--------:|--------------:|------:|---------:|----------------:|------------:|-----------:|----------------:|--------------:|
| points        |    1     |   0.657 |         0.713 | 0.834 |    0.95  |           0.95  |       0.854 |      0.521 |           0.718 |         0.657 |
| xgd60         |    0.657 |   1     |         0.811 | 0.669 |    0.665 |           0.665 |       0.769 |      0.581 |           0.767 |         0.799 |
| pythagorean   |    0.713 |   0.811 |         1     | 0.688 |    0.723 |           0.723 |       0.816 |      0.569 |           0.805 |         0.799 |
| elo           |    0.834 |   0.669 |         0.688 | 1     |    0.868 |           0.868 |       0.778 |      0.503 |           0.665 |         0.61  |
| colley        |    0.95  |   0.665 |         0.723 | 0.868 |    1     |           1     |       0.864 |      0.516 |           0.705 |         0.647 |
| bradley_terry |    0.95  |   0.665 |         0.723 | 0.868 |    1     |           1     |       0.864 |      0.516 |           0.705 |         0.647 |
| composite     |    0.854 |   0.769 |         0.816 | 0.778 |    0.864 |           0.864 |       1     |      0.55  |           0.781 |         0.729 |
| logistic      |    0.521 |   0.581 |         0.569 | 0.503 |    0.516 |           0.516 |       0.55  |      1     |           0.634 |         0.748 |
| random_forest |    0.718 |   0.767 |         0.805 | 0.665 |    0.705 |           0.705 |       0.781 |      0.634 |           1     |         0.814 |
| monte_carlo   |    0.657 |   0.799 |         0.799 | 0.61  |    0.647 |           0.647 |       0.729 |      0.748 |           0.814 |         1     |

## 5.3 Original Validation 1: Elo Calibration Curve
Checks whether Elo-predicted win probabilities match actual win rates when binned by decile.
|   decile |   mean_pred |   mean_actual |   n |   calibration_error |
|---------:|------------:|--------------:|----:|--------------------:|
|        0 |       0.337 |         0.5   |  10 |               0.163 |
|        1 |       0.406 |         0.258 |  31 |               0.148 |
|        2 |       0.46  |         0.351 |  74 |               0.109 |
|        3 |       0.514 |         0.464 | 140 |               0.05  |
|        4 |       0.566 |         0.51  | 198 |               0.056 |
|        5 |       0.623 |         0.544 | 250 |               0.079 |
|        6 |       0.679 |         0.607 | 262 |               0.072 |
|        7 |       0.734 |         0.638 | 210 |               0.096 |
|        8 |       0.787 |         0.771 | 105 |               0.015 |
|        9 |       0.834 |         0.781 |  32 |               0.053 |

## 5.4 Original Validation 2: Bootstrap CI Overlap for Adjacent Rankings
Flags whether adjacent-ranked teams are statistically distinguishable via 95% bootstrap CIs on xGD/60.
| team         |   mean_xgd |   ci_lo |   ci_hi |   rank |
|:-------------|-----------:|--------:|--------:|-------:|
| thailand     |      0.891 |   0.579 |   1.186 |      1 |
| pakistan     |      0.625 |   0.37  |   0.86  |      2 |
| brazil       |      0.618 |   0.299 |   0.9   |      3 |
| mexico       |      0.502 |   0.274 |   0.746 |      4 |
| netherlands  |      0.496 |   0.271 |   0.745 |      5 |
| uk           |      0.443 |   0.159 |   0.728 |      6 |
| china        |      0.426 |   0.194 |   0.677 |      7 |
| france       |      0.396 |   0.163 |   0.619 |      8 |
| peru         |      0.361 |   0.134 |   0.6   |      9 |
| guatemala    |      0.279 |  -0.004 |   0.557 |     10 |
| panama       |      0.196 |  -0.074 |   0.446 |     11 |
| serbia       |      0.16  |  -0.141 |   0.436 |     12 |
| south_korea  |      0.106 |  -0.236 |   0.39  |     13 |
| canada       |      0.092 |  -0.164 |   0.349 |     14 |
| morocco      |      0.072 |  -0.185 |   0.338 |     15 |
| new_zealand  |      0.036 |  -0.227 |   0.336 |     16 |
| india        |      0.017 |  -0.248 |   0.283 |     17 |
| saudi_arabia |     -0.146 |  -0.422 |   0.094 |     18 |
| germany      |     -0.169 |  -0.389 |   0.067 |     19 |
| iceland      |     -0.227 |  -0.501 |   0.066 |     20 |
| kazakhstan   |     -0.264 |  -0.509 |   0.036 |     21 |
| indonesia    |     -0.274 |  -0.499 |  -0.033 |     22 |
| philippines  |     -0.275 |  -0.529 |  -0.047 |     23 |
| ethiopia     |     -0.284 |  -0.529 |  -0.013 |     24 |
| uae          |     -0.378 |  -0.683 |  -0.09  |     25 |
| switzerland  |     -0.391 |  -0.667 |  -0.131 |     26 |
| rwanda       |     -0.394 |  -0.604 |  -0.146 |     27 |
| usa          |     -0.418 |  -0.703 |  -0.108 |     28 |
| oman         |     -0.421 |  -0.7   |  -0.164 |     29 |
| singapore    |     -0.524 |  -0.855 |  -0.217 |     30 |
| vietnam      |     -0.564 |  -0.846 |  -0.281 |     31 |
| mongolia     |     -0.987 |  -1.263 |  -0.737 |     32 |

## 5.5 Baseline Comparisons
| Baseline | Accuracy |
|----------|----------|
| Always pick home team | 0.5640 |
| Always pick higher-points team | 0.5816 |
| Always pick higher xGD/60 team | 0.5457 |
| **Logistic Regression (our model)** | **0.5846** |
| LR 10-fold CV accuracy | 0.5823 ± 0.0285 |

---

# Section 6: Methodology Narrative (Phase 1d)

## 6.1 Data Cleaning & Preparation (~75 words)

The WHL 2025 dataset (25,827 rows, 26 columns) was loaded and audited for missing values — none
were found. Game-level aggregates were built by summing all row-level statistics within each
`game_id`. Even-strength analysis strictly filtered to `home_off_line ∈ {first_off, second_off}`,
while power play and penalty kill situations were handled separately. All rate statistics were
normalized to per-60-minute rates using the formula `stat × (3600 / toi)` to eliminate
confounding from unequal time-on-ice across line types.


## 6.2 Variable Creation (~75 words)

Key derived variables include: **xGD/60** (xGF/60 − xGA/60, even-strength), **GSAx** (Goals
Saved Above Expected: xGA − actual GA per goalie), **Pythagorean win%** (xGF^k / (xGF^k + xGA^k),
k tuned empirically), **Elo ratings** (initialized at 1500, K=20, +100 home advantage), and
**line disparity metrics** (10 variants from raw xG ratio to bootstrap-adjusted xG/60 ratios).
Matchup-adjusted xG scales raw xG by the ratio of league-average defensive quality to the
specific opponent's defensive quality.


## 6.3 Tools Used (~50 words)

All analysis was conducted in Python using `pandas` (data manipulation), `numpy` (numerical
computation), `scipy` (statistical tests, optimization), `scikit-learn` (logistic regression,
random forest, cross-validation), and `statsmodels` (OLS regression). A custom multi-agent
architecture orchestrated parallel execution of EDA, aggregation, modeling, validation, and
report generation pipelines.


## 6.4 Statistical Methods (~100 words)

Ten power ranking models were built ranging from simple point totals (Model 1) to sophisticated
approaches: **Elo ratings** (sequential Bayesian updating), **Colley matrix** (strength-of-schedule
via linear systems), **Bradley-Terry** (maximum likelihood pairwise competition model), **Pythagorean
expectation** (empirically tuned exponent), **composite weighted z-scores**, **logistic regression**,
**random forest with permutation importance**, and **Monte Carlo simulation** (1,000 full-season
replications). Win probabilities used five independent methods and ensemble averaging. Line disparity
employed 10 complementary techniques including bootstrap confidence intervals and regression control
for opponent defensive quality.


## 6.5 Model Assessment (~75 words)

Every ranking model was evaluated using seven metrics: Kendall's τ and Spearman ρ (rank correlation
vs points-based ground truth), Top-8 hit rate (proportion of true top-8 in model's top-8), Brier
score and log-loss (probability calibration), rank inversion rate (head-to-head prediction accuracy),
and consensus ρ (agreement with mean ranking). The win probability model was further validated via
10-fold cross-validation and leave-one-team-out validation, and compared against three naive baselines.


## 6.6 AI Tool Usage (~50 words)

All code, analysis, and report generation were produced by an AI multi-agent pipeline (Antigravity /
Google DeepMind). The Orchestrator spawned specialized subagents for EDA, game aggregation, ten
ranking models, five win probability models, ten disparity methods, validation, and report compilation.
Human oversight validated the pipeline architecture; all data analysis and statistical modeling was
AI-generated.


---

# 🏆 Submission-Ready Summary

## Phase 1a: Recommended Power Ranking (Consensus)
|   rank | team         |   mean_rank |
|-------:|:-------------|------------:|
|      1 | thailand     |         3.2 |
|      2 | brazil       |         3.5 |
|      3 | pakistan     |         3.8 |
|      4 | netherlands  |         7.5 |
|      5 | china        |         8.9 |
|      6 | peru         |         9.2 |
|      7 | serbia       |        10.5 |
|      8 | uk           |        10.9 |
|      9 | guatemala    |        11.2 |
|     10 | panama       |        11.7 |
|     11 | iceland      |        13.9 |
|     12 | india        |        13.9 |
|     13 | ethiopia     |        13.9 |
|     14 | mexico       |        14   |
|     15 | south_korea  |        14.3 |
|     16 | singapore    |        15.4 |
|     17 | new_zealand  |        16.2 |
|     18 | france       |        18   |
|     19 | philippines  |        18.3 |
|     20 | morocco      |        18.8 |
|     21 | canada       |        20   |
|     22 | indonesia    |        21.1 |
|     23 | saudi_arabia |        21.4 |
|     24 | vietnam      |        22.2 |
|     25 | oman         |        22.5 |
|     26 | germany      |        22.5 |
|     27 | usa          |        23.5 |
|     28 | uae          |        24.9 |
|     29 | rwanda       |        25.5 |
|     30 | switzerland  |        27.4 |
|     31 | kazakhstan   |        28.9 |
|     32 | mongolia     |        31   |

## Phase 1a: Win Probabilities for Round 1 Matchups
|   game | home_team   | away_team    |   home_win_prob |
|-------:|:------------|:-------------|----------------:|
|      1 | brazil      | kazakhstan   |           0.723 |
|      2 | netherlands | mongolia     |           0.733 |
|      3 | peru        | rwanda       |           0.662 |
|      4 | thailand    | oman         |           0.675 |
|      5 | pakistan    | germany      |           0.662 |
|      6 | india       | usa          |           0.618 |
|      7 | panama      | switzerland  |           0.604 |
|      8 | iceland     | canada       |           0.579 |
|      9 | china       | france       |           0.61  |
|     10 | philippines | morocco      |           0.53  |
|     11 | ethiopia    | saudi_arabia |           0.577 |
|     12 | singapore   | new_zealand  |           0.506 |
|     13 | guatemala   | south_korea  |           0.564 |
|     14 | uk          | mexico       |           0.538 |
|     15 | vietnam     | serbia       |           0.482 |
|     16 | indonesia   | uae          |           0.561 |

## Phase 1b: Top 10 Teams by First-to-Second Line Disparity
|   rank | team         |   avg_disparity_rank |
|-------:|:-------------|---------------------:|
|      1 | saudi_arabia |                  4.1 |
|      2 | guatemala    |                  4.2 |
|      3 | france       |                  5.3 |
|      4 | usa          |                  5.6 |
|      5 | iceland      |                  6.5 |
|      5 | singapore    |                  6.5 |
|      7 | uae          |                  6.7 |
|      8 | new_zealand  |                 10.4 |
|      9 | peru         |                 11.8 |
|     10 | serbia       |                 12.1 |

---
_End of Report_