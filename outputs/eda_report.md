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

## 13. Outlier Detection
Rows with TOI 3+ std above mean: 658
Rows with xG 3+ std above mean: 1196

## 14. Line Matchup Frequency
|    | home_off_line   | away_def_pairing   |   count |
|---:|:----------------|:-------------------|--------:|
|  8 | first_off       | second_def         |    5248 |
| 10 | second_off      | first_def          |    5248 |
|  7 | first_off       | first_def          |    5248 |
| 11 | second_off      | second_def         |    5247 |
|  2 | PP_up           | PP_kill_dwn        |    1305 |
|  0 | PP_kill_dwn     | PP_up              |    1302 |
|  6 | first_off       | empty_net_line     |     566 |
|  9 | second_off      | empty_net_line     |     543 |
|  5 | empty_net_line  | second_def         |     455 |
|  4 | empty_net_line  | first_def          |     449 |
|  1 | PP_kill_dwn     | empty_net_line     |     132 |
|  3 | empty_net_line  | PP_kill_dwn        |      84 |

## 15. TOI by Line Type
| home_off_line   |   count |     mean |      std |   min |     25% |     50% |      75% |     max |
|:----------------|--------:|---------:|---------:|------:|--------:|--------:|---------:|--------:|
| PP_kill_dwn     |    1434 | 450.38   | 240.936  |  2.2  | 252.12  | 473.96  | 600      | 1330.27 |
| PP_up           |    1305 | 527.946  | 228.035  | 28.7  | 360     | 493.5   | 673.49   | 1559.67 |
| empty_net_line  |     988 |  42.4531 |  25.727  |  0.01 |  19.68  |  46.365 |  58.6025 |  155.56 |
| first_off       |   11062 | 161.042  |  88.5721 |  0.15 |  94.295 | 150.19  | 216.065  |  598.36 |
| second_off      |   11038 | 158.902  |  87.2299 |  0.21 |  94.045 | 148.81  | 211.295  |  584.25 |

## 16. Team Clustering (xGF/60, xGA/60)
|    | team         |   xgf60 |   xga60 |        xgd60 |
|---:|:-------------|--------:|--------:|-------------:|
| 17 | pakistan     | 2.96698 | 2.09105 |  0.87593     |
| 27 | thailand     | 2.89998 | 2.0531  |  0.846876    |
|  0 | brazil       | 2.7514  | 1.96281 |  0.788592    |
| 11 | mexico       | 2.52533 | 1.97193 |  0.553397    |
| 25 | south_korea  | 2.62428 | 2.14871 |  0.475564    |
|  2 | china        | 2.46372 | 2.0901  |  0.37362     |
|  6 | guatemala    | 2.4866  | 2.13914 |  0.347466    |
| 19 | peru         | 2.2294  | 1.98815 |  0.241257    |
| 23 | serbia       | 2.72925 | 2.5557  |  0.173544    |
| 14 | netherlands  | 2.0617  | 1.91953 |  0.142172    |
| 16 | oman         | 2.51822 | 2.38366 |  0.134555    |
| 21 | rwanda       | 2.25033 | 2.13123 |  0.119097    |
| 29 | uk           | 2.5616  | 2.47796 |  0.0836439   |
|  1 | canada       | 2.37128 | 2.3077  |  0.0635839   |
| 15 | new_zealand  | 2.24897 | 2.21513 |  0.0338473   |
| 13 | morocco      | 2.34941 | 2.32301 |  0.0264034   |
|  7 | iceland      | 2.31693 | 2.31616 |  0.000775131 |
| 18 | panama       | 2.39046 | 2.39833 | -0.00786654  |
|  8 | india        | 2.28476 | 2.32824 | -0.0434747   |
|  3 | ethiopia     | 2.36329 | 2.5011  | -0.137809    |
|  4 | france       | 2.30008 | 2.44591 | -0.145836    |
| 30 | usa          | 2.42218 | 2.5895  | -0.167321    |
| 22 | saudi_arabia | 1.97983 | 2.22583 | -0.246004    |
| 26 | switzerland  | 1.82428 | 2.07754 | -0.253263    |
|  5 | germany      | 2.2592  | 2.53966 | -0.280457    |
| 24 | singapore    | 2.3747  | 2.71895 | -0.344253    |
| 31 | vietnam      | 2.10006 | 2.44937 | -0.349313    |
| 28 | uae          | 1.8046  | 2.27013 | -0.465539    |
| 20 | philippines  | 1.88105 | 2.36918 | -0.48813     |
| 10 | kazakhstan   | 1.75054 | 2.32459 | -0.574043    |
|  9 | indonesia    | 1.86163 | 2.50759 | -0.645957    |
| 12 | mongolia     | 1.67598 | 2.62206 | -0.946082    |
