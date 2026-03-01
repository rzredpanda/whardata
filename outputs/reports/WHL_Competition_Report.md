# WHL 2026 — Wharton High School Data Science Competition
## World Hockey League Performance Analysis Report
**Generated:** 2026-02-28 14:57  |  **Prepared by:** Multi-Agent Analytics Pipeline

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
| Unnamed: 0               |   count |        mean |         std |   min |    25% |      50% |      75% |       max |     skew |
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

## 1.3 Home Advantage
- **Overall home win rate:** 0.564 (56.4%)
- **OT/SO rate:** 0.220 (22.0%)
- **Regulation home win rate:** 0.576
- **OT/SO home win rate:** 0.521

## 1.4 Full EDA Findings
# WHL 2025 — EDA Report
Generated: 2026-02-28T13:13:54.617378

## 1. Dataset Structure
- Shape: (25827, 26)
- Columns: ['game_id', 'record_id', 'home_team', 'away_team', 'went_ot', 'home_off_line', 'home_def_pairing', 'away_off_line', 'away_def_pairing', 'home_goalie', 'away_goalie', 'toi', 'home_assists', 'home_shots', 'home_xg', 'home_max_xg', 'home_goals', 'away_assists', 'away_shots', 'away_xg', 'away_max_xg', 'away_goals', 'home_penalties_committed', 'home_penalty_minutes', 'away_penalties_committed', 'away_penalty_minutes']
- Unique games: 1312
- Records per game (mean): 19.69

## 2. Missing Values
  - No missing values found.

## 3. Categorical Fields
### home_off_line
home_off_line
first_off         11062
second_off        11038
PP_kill_dwn        1434
PP_up              1305
empty_net_line      988

### home_def_pairing
home_def_pairing
second_def        11067
first_def         11033
PP_kill_dwn        1434
PP_up              1305
empty_net_line      988

### away_off_line
away_off_line
second_off        10960
first_off         10935
PP_kill_dwn        1389
PP_up              1302
empty_net_line     1241

### away_def_pairing
away_def_pairing
second_def        10950
first_def         10945
PP_kill_dwn        1389
PP_up              1302
empty_net_line     1241

### went_ot
went_ot
0    20379
1     5448

## 4. Numeric Summary Statistics
                            count        mean         std   min     25%       50%       75%        max      skew
toi                       25827.0  190.194902  153.702230  0.01  92.645  156.1900  237.9850  1559.6700  2.266910
home_xg                   25827.0    0.158953    0.305636  0.00   0.000    0.0898    0.1878     5.5435  5.260399
away_xg                   25827.0    0.142801    0.264191  0.00   0.000    0.0825    0.1752     4.4123  5.037954
home_goals                25827.0    0.157045    0.476548  0.00   0.000    0.0000    0.0000     7.0000  4.273998
away_goals                25827.0    0.135440    0.427517  0.00   0.000    0.0000    0.0000     7.0000  4.188632
home_shots                25827.0    1.400240    2.046256  0.00   0.000    1.0000    2.0000    28.0000  3.521200
away_shots                25827.0    1.329113    1.875248  0.00   0.000    1.0000    2.0000    23.0000  3.271204
home_max_xg               25827.0    0.066332    0.060490  0.00   0.000    0.0801    0.1050     0.2707  0.417094
away_max_xg               25827.0    0.062455    0.058003  0.00   0.000    0.0745    0.0996     0.2622  0.466749
home_assists              25827.0    0.245054    0.798532  0.00   0.000    0.0000    0.0000    13.0000  4.615794
away_assists              25827.0    0.211445    0.714388  0.00   0.000    0.0000    0.0000    13.0000  4.494062
home_penalties_committed  25827.0    0.316490    1.314470  0.00   0.000    0.0000    0.0000    16.0000  5.119035
home_penalty_minutes      25827.0    0.646494    2.695040  0.00   0.000    0.0000    0.0000    34.0000  5.161742
away_penalties_committed  25827.0    0.344910    1.436780  0.00   0.000    0.0000    0.0000    19.0000  5.200038
away_penalty_minutes      25827.0    0.703605    2.940398  0.00   0.000    0.0000    0.0000    38.0000  5.253475

## 5. Game-Level Aggregated Stats
Games aggregated: 1312
Home win rate: 0.5640
OT/SO rate: 0.2195

## 6. Home Advantage Analysis
Overall home win rate: 0.5640
Regulation home win rate: 0.5762 (n=1024)
OT/SO home win rate: 0.5208 (n=288)
Goal margin distribution:
goal_diff
-9      1
-7      2
-6      7
-5     21
-4     43
-3     72
-2     82
-1    344
 1    367
 2    127
 3     89
 4     88
 5     42
 6     18
 7      6
 8      3

## 7. xG vs Actual Goals Correlation
Home xG vs Home Goals Pearson r: 0.4560
Away xG vs Away Goals Pearson r: 0.4381
Combined xG vs Goals Pearson r: 0.4586

## 8. xG Calibration (does xG=1.0 → ~1 goal)
         xg_bin   mean_xg  mean_goals      n
0   (0.0, 0.25]  0.128949    0.121828  23410
1   (0.25, 0.5]  0.335220    0.342544   5284
2   (0.5, 0.75]  0.606168    0.580989   1031
3   (0.75, 1.0]  0.860520    0.802935    477
4   (1.0, 1.25]  1.117180    1.023622    381
5   (1.25, 1.5]  1.370179    1.436090    266
6   (1.5, 1.75]  1.620242    1.584211    190
7   (1.75, 2.0]  1.873745    1.659722    144
8   (2.0, 2.25]  2.119429    2.114583     96
9   (2.25, 2.5]  2.369964    2.520000     50
10  (2.5, 2.75]  2.614988    2.750000     24
11  (2.75, 3.0]  2.843058    2.923077     26
12  (3.0, 3.25]  3.135707    2.933333     15

## 9. Power Play vs Even-Strength xG Rates
Even-strength home xG/60: 2.3471
Even-strength away xG/60: 2.2438
PP (home up) home xG/60: 7.7306
PP kill (home down) away xG/60: 7.0933

## 10. Goalie Goals Saved Above Expected (GSAx)
Goalies analyzed: 33
Top 5 GSAx:
           goalie       xga   ga     gsax  gsax_per60
25   player_id_38  235.3583  185  50.3583    0.583574
19  player_id_257  237.3053  192  45.3053    0.532898
10   player_id_16  246.9443  205  41.9443    0.500609
15  player_id_218  213.9307  176  37.9307    0.441233
4   player_id_123  298.6754  265  33.6754    0.393066
Bottom 5 GSAx:
           goalie       xga   ga     gsax  gsax_per60
12  player_id_208  232.2853  262 -29.7147   -0.349771
1   player_id_103  222.0814  252 -29.9186   -0.351600
17  player_id_232  232.8128  263 -30.1872   -0.358802
0       empty_net   38.7571   76 -37.2429   -1.416384
30   player_id_80  249.4824  296 -46.5176   -0.554099

## 11. Penalty Analysis
Penalty min vs home win corr: -0.1800
Penalty min vs away pen corr: 0.0563

## 12. Season Trends — First vs Second Half Games
Top 5 improvers (second half win% - first half win%):
           team  winpct_h1  winpct_h2     trend
30          usa   0.300000   0.547619  0.247619
19         peru   0.512195   0.756098  0.243902
21       rwanda   0.268293   0.463415  0.195122
16         oman   0.341463   0.512195  0.170732
20  philippines   0.439024   0.609756  0.170732
Top 5 decliners:
         team  winpct_h1  winpct_h2     trend
0      brazil   0.809524   0.600000 -0.209524
13    morocco   0.547619   0.350000 -0.197619
17   pakistan   0.682927   0.512195 -0.170732
2       china   0.657895   0.500000 -0.157895
6   guatemala   0.575000   0.452381 -0.122619

## 13. Outlier Detection
Rows with TOI 3+ std above mean: 658
Rows with xG 3+ std above mean: 1196

## 14. Line Matchup Frequency
     home_off_line away_def_pairing  count
8        first_off       second_def   5248
10      second_off        first_def   5248
7        first_off        first_def   5248
11      second_off       second_def   5247
2            PP_up      PP_kill_dwn   1305
0      PP_kill_dwn            PP_up   1302
6        first_off   empty_net_line    566
9       second_off   empty_net_line    543
5   empty_net_line       second_def    455
4   empty_net_line        first_def    449
1      PP_kill_dwn   empty_net_line    132
3   empty_net_line      PP_kill_dwn     84

## 15. TOI by Line Type
                  count        mean         std    min      25%      50%       75%      max
home_off_line                                                                              
PP_kill_dwn      1434.0  450.379505  240.936029   2.20  252.120  473.960  600.0000  1330.27
PP_up            1305.0  527.945939  228.034882  28.70  360.000  493.500  673.4900  1559.67
empty_net_line    988.0   42.453077   25.726999   0.01   19.680   46.365   58.6025   155.56
first_off       11062.0  161.042208   88.572137   0.15   94.295  150.190  216.0650   598.36
second_off      11038.0  158.901752   87.229890   0.21   94.045  148.810  211.2950   584.25

## 16. Team Clustering (xGF/60, xGA/60)
            team     xgf60     xga60     xgd60
17      pakistan  2.966984  2.091055  0.875930
27      thailand  2.899978  2.053101  0.846876
0         brazil  2.751404  1.962812  0.788592
11        mexico  2.525331  1.971933  0.553397
25   south_korea  2.624278  2.148714  0.475564
2          china  2.463716  2.090096  0.373620
6      guatemala  2.486605  2.139139  0.347466
19          peru  2.229403  1.988145  0.241257
23        serbia  2.729

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
|      1 | pakistan     |  0.8759 |     2.967  |     2.0911 |     0.8759 |
|      2 | thailand     |  0.8469 |     2.9    |     2.0531 |     0.8469 |
|      3 | brazil       |  0.7886 |     2.7514 |     1.9628 |     0.7886 |
|      4 | mexico       |  0.5534 |     2.5253 |     1.9719 |     0.5534 |
|      5 | south_korea  |  0.4756 |     2.6243 |     2.1487 |     0.4756 |
|      6 | china        |  0.3736 |     2.4637 |     2.0901 |     0.3736 |
|      7 | guatemala    |  0.3475 |     2.4866 |     2.1391 |     0.3475 |
|      8 | peru         |  0.2413 |     2.2294 |     1.9881 |     0.2413 |
|      9 | serbia       |  0.1735 |     2.7292 |     2.5557 |     0.1735 |
|     10 | netherlands  |  0.1422 |     2.0617 |     1.9195 |     0.1422 |
|     11 | oman         |  0.1346 |     2.5182 |     2.3837 |     0.1346 |
|     12 | rwanda       |  0.1191 |     2.2503 |     2.1312 |     0.1191 |
|     13 | uk           |  0.0836 |     2.5616 |     2.478  |     0.0836 |
|     14 | canada       |  0.0636 |     2.3713 |     2.3077 |     0.0636 |
|     15 | new_zealand  |  0.0338 |     2.249  |     2.2151 |     0.0338 |
|     16 | morocco      |  0.0264 |     2.3494 |     2.323  |     0.0264 |
|     17 | iceland      |  0.0008 |     2.3169 |     2.3162 |     0.0008 |
|     18 | panama       | -0.0079 |     2.3905 |     2.3983 |    -0.0079 |
|     19 | india        | -0.0435 |     2.2848 |     2.3282 |    -0.0435 |
|     20 | ethiopia     | -0.1378 |     2.3633 |     2.5011 |    -0.1378 |
|     21 | france       | -0.1458 |     2.3001 |     2.4459 |    -0.1458 |
|     22 | usa          | -0.1673 |     2.4222 |     2.5895 |    -0.1673 |
|     23 | saudi_arabia | -0.246  |     1.9798 |     2.2258 |    -0.246  |
|     24 | switzerland  | -0.2533 |     1.8243 |     2.0775 |    -0.2533 |
|     25 | germany      | -0.2805 |     2.2592 |     2.5397 |    -0.2805 |
|     26 | singapore    | -0.3443 |     2.3747 |     2.719  |    -0.3443 |
|     27 | vietnam      | -0.3493 |     2.1001 |     2.4494 |    -0.3493 |
|     28 | uae          | -0.4655 |     1.8046 |     2.2701 |    -0.4655 |
|     29 | philippines  | -0.4881 |     1.881  |     2.3692 |    -0.4881 |
|     30 | kazakhstan   | -0.574  |     1.7505 |     2.3246 |    -0.574  |
|     31 | indonesia    | -0.646  |     1.8616 |     2.5076 |    -0.646  |
|     32 | mongolia     | -0.9461 |     1.676  |     2.6221 |    -0.9461 |

## 2.3 Model 3: Pythagorean Expectation
_xGF^k / (xGF^k + xGA^k). Optimal k tuned empirically._

|   rank | team         |    score |   pyth_winpct |     xgf |     xga |   optimal_k |
|-------:|:-------------|---------:|--------------:|--------:|--------:|------------:|
|      1 | thailand     | 0.605251 |      0.605251 | 294.737 | 221.662 |         1.5 |
|      2 | brazil       | 0.576518 |      0.576518 | 272.479 | 221.827 |         1.5 |
|      3 | pakistan     | 0.573866 |      0.573866 | 284.703 | 233.462 |         1.5 |
|      4 | netherlands  | 0.568457 |      0.568457 | 242.499 | 201.803 |         1.5 |
|      5 | mexico       | 0.563286 |      0.563286 | 263.958 | 222.765 |         1.5 |
|      6 | china        | 0.554823 |      0.554823 | 255.917 | 220.979 |         1.5 |
|      7 | uk           | 0.552637 |      0.552637 | 276.312 | 240.001 |         1.5 |
|      8 | france       | 0.548605 |      0.548605 | 266.652 | 234.14  |         1.5 |
|      9 | peru         | 0.548258 |      0.548258 | 244.55  | 214.934 |         1.5 |
|     10 | guatemala    | 0.535093 |      0.535093 | 255.688 | 232.81  |         1.5 |
|     11 | panama       | 0.524137 |      0.524137 | 257.455 | 241.394 |         1.5 |
|     12 | serbia       | 0.51816  |      0.51816  | 277.288 | 264.174 |         1.5 |
|     13 | south_korea  | 0.512702 |      0.512702 | 259.857 | 251.201 |         1.5 |
|     14 | canada       | 0.511927 |      0.511927 | 241.134 | 233.584 |         1.5 |
|     15 | morocco      | 0.508939 |      0.508939 | 249.503 | 243.625 |         1.5 |
|     16 | new_zealand  | 0.504588 |      0.504588 | 241.265 | 238.331 |         1.5 |
|     17 | india        | 0.502206 |      0.502206 | 239.336 | 237.932 |         1.5 |
|     18 | saudi_arabia | 0.479998 |      0.479998 | 218.965 | 230.968 |         1.5 |
|     19 | germany      | 0.47883  |      0.47883  | 239.107 | 253.002 |         1.5 |
|     20 | iceland      | 0.47086  |      0.47086  | 230.062 | 248.674 |         1.5 |
|     21 | ethiopia     | 0.465276 |      0.465276 | 239.42  | 262.688 |         1.5 |
|     22 | kazakhstan   | 0.463294 |      0.463294 | 209.805 | 231.421 |         1.5 |
|     23 | indonesia    | 0.46299  |      0.46299  | 215.9   | 238.338 |         1.5 |
|     24 | philippines  | 0.462434 |      0.462434 | 213.585 | 236.134 |         1.5 |
|     25 | usa          | 0.451458 |      0.451458 | 247.393 | 281.697 |         1.5 |
|     26 | oman         | 0.45067  |      0.45067  | 244.937 | 279.493 |         1.5 |
|     27 | rwanda       | 0.449599 |      0.449599 | 223.809 | 256.122 |         1.5 |
|     28 | uae          | 0.448912 |      0.448912 | 211.395 | 242.364 |         1.5 |
|     29 | switzerland  | 0.44575  |      0.44575  | 205.292 | 237.382 |         1.5 |
|     30 | singapore    | 0.442294 |      0.442294 | 257.021 | 299.984 |         1.5 |
|     31 | vietnam      | 0.430585 |      0.430585 | 225.778 | 272.016 |         1.5 |
|     32 | mongolia     | 0.3687   |      0.3687   | 187.599 | 268.497 |         1.5 |

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
|      1 | brazil       | 0.44203 |         0.44203 |
|      2 | netherlands  | 0.39885 |         0.39885 |
|      3 | peru         | 0.3763  |         0.3763  |
|      4 | thailand     | 0.35032 |         0.35032 |
|      5 | pakistan     | 0.33961 |         0.33961 |
|      6 | india        | 0.33959 |         0.33959 |
|      7 | china        | 0.31931 |         0.31931 |
|      8 | iceland      | 0.30926 |         0.30926 |
|      9 | panama       | 0.30567 |         0.30567 |
|     10 | ethiopia     | 0.27343 |         0.27343 |
|     11 | philippines  | 0.27246 |         0.27246 |
|     12 | guatemala    | 0.26122 |         0.26122 |
|     13 | indonesia    | 0.25428 |         0.25428 |
|     14 | serbia       | 0.24805 |         0.24805 |
|     15 | new_zealand  | 0.23871 |         0.23871 |
|     16 | singapore    | 0.235   |         0.235   |
|     17 | uk           | 0.22858 |         0.22858 |
|     18 | saudi_arabia | 0.22713 |         0.22713 |
|     19 | vietnam      | 0.227   |         0.227   |
|     20 | south_korea  | 0.22597 |         0.22597 |
|     21 | mexico       | 0.21638 |         0.21638 |
|     22 | uae          | 0.21164 |         0.21164 |
|     23 | france       | 0.20323 |         0.20323 |
|     24 | morocco      | 0.20028 |         0.20028 |
|     25 | canada       | 0.19683 |         0.19683 |
|     26 | switzerland  | 0.19562 |         0.19562 |
|     27 | germany      | 0.19365 |         0.19365 |
|     28 | oman         | 0.1861  |         0.1861  |
|     29 | usa          | 0.18189 |         0.18189 |
|     30 | rwanda       | 0.12865 |         0.12865 |
|     31 | kazakhstan   | 0.12137 |         0.12137 |
|     32 | mongolia     | 0.09161 |         0.09161 |

## 2.6 Model 6: Bradley-Terry Pairwise
_MLE pairwise model: P(i beats j) = s_i/(s_i+s_j)._

|   rank | team         |   score |   bt_strength |
|-------:|:-------------|--------:|--------------:|
|      1 | brazil       | 2.35101 |       2.35101 |
|      2 | netherlands  | 1.90555 |       1.90555 |
|      3 | peru         | 1.7191  |       1.7191  |
|      4 | thailand     | 1.5335  |       1.5335  |
|      5 | pakistan     | 1.46191 |       1.46191 |
|      6 | india        | 1.46133 |       1.46133 |
|      7 | china        | 1.33947 |       1.33947 |
|      8 | iceland      | 1.28342 |       1.28342 |
|      9 | panama       | 1.26405 |       1.26405 |
|     10 | ethiopia     | 1.10251 |       1.10251 |
|     11 | philippines  | 1.0975  |       1.0975  |
|     12 | guatemala    | 1.04684 |       1.04684 |
|     13 | indonesia    | 1.01774 |       1.01774 |
|     14 | serbia       | 0.99011 |       0.99011 |
|     15 | new_zealand  | 0.95236 |       0.95236 |
|     16 | singapore    | 0.9369  |       0.9369  |
|     17 | uk           | 0.91286 |       0.91286 |
|     18 | saudi_arabia | 0.90707 |       0.90707 |
|     19 | vietnam      | 0.90656 |       0.90656 |
|     20 | south_korea  | 0.90238 |       0.90238 |
|     21 | mexico       | 0.86685 |       0.86685 |
|     22 | uae          | 0.84895 |       0.84895 |
|     23 | france       | 0.81984 |       0.81984 |
|     24 | morocco      | 0.80909 |       0.80909 |
|     25 | canada       | 0.79764 |       0.79764 |
|     26 | switzerland  | 0.7941  |       0.7941  |
|     27 | germany      | 0.7872  |       0.7872  |
|     28 | oman         | 0.76245 |       0.76245 |
|     29 | usa          | 0.74874 |       0.74874 |
|     30 | rwanda       | 0.59193 |       0.59193 |
|     31 | kazakhstan   | 0.5746  |       0.5746  |
|     32 | mongolia     | 0.50028 |       0.50028 |

## 2.7 Model 7: Composite Weighted Score
_Z-score weighted sum: xGD(0.35)+GD(0.15)+GSAx(0.20)+PP(0.15)+PK(0.15)._

|   rank | team         |      score |   composite |    z_xgd60 |      z_gd |   z_gsax60 |       z_pp |       z_pk |
|-------:|:-------------|-----------:|------------:|-----------:|----------:|-----------:|-----------:|-----------:|
|      1 | brazil       |  1.34411   |   1.34411   |  1.86091   |  2.11841  |  0.985799  | -0.20166   |  1.38748   |
|      2 | pakistan     |  1.21031   |   1.21031   |  2.06844   |  1.24183  |  0.552427  |  0.45872   |  0.805249  |
|      3 | netherlands  |  1.07916   |   1.07916   |  0.324293  |  1.68012  |  0.770258  |  2.21599   |  1.51462   |
|      4 | thailand     |  0.983379  |   0.983379  |  1.9995    |  1.12008  | -1.30437   |  1.46647   |  1.04297   |
|      5 | peru         |  0.812755  |   0.812755  |  0.559872  |  1.89926  |  1.10387   | -0.0220792 |  0.762984  |
|      6 | uk           |  0.596009  |   0.596009  |  0.18499   |  0.803535 |  0.823898  |  1.45842   |  0.181268  |
|      7 | china        |  0.532527  |   0.532527  |  0.874374  |  1.12008  |  0.790864  | -0.229984  | -0.434604  |
|      8 | mexico       |  0.388005  |   0.388005  |  1.30179   | -0.413942 | -1.43716   |  0.36627   |  1.51307   |
|      9 | panama       |  0.382064  |   0.382064  | -0.0325229 |  1.02268  |  0.813432  |  0.711053  | -0.195328  |
|     10 | iceland      |  0.362393  |   0.362393  | -0.0118414 |  0.706137 |  1.2455    | -1.12645   |  1.20324   |
|     11 | guatemala    |  0.331811  |   0.331811  |  0.812329  | -0.121748 | -0.407533  |  0.682153  |  0.299613  |
|     12 | india        |  0.154315  |   0.154315  | -0.117151  |  0.681787 |  1.4352    | -1.21042   | -0.0828496 |
|     13 | philippines  |  0.071859  |   0.071859  | -1.17405   |  0.292194 |  1.60299   |  0.338951  |  0.450044  |
|     14 | serbia       |  0.04487   |   0.04487   |  0.398699  |  0.121748 | -0.277685  |  0.507893  | -0.890557  |
|     15 | saudi_arabia | -0.0127973 |  -0.0127973 | -0.598531  | -0.243495 |  0.697321  | -1.01488   |  1.63987   |
|     16 | ethiopia     | -0.0424307 |  -0.0424307 | -0.34132   |  0.486991 |  0.325438  |  0.696244  | -1.10361   |
|     17 | new_zealand  | -0.100487  |  -0.100487  |  0.0666058 | -0.170447 |  0.193955  | -0.146449  | -0.767038  |
|     18 | singapore    | -0.150815  |  -0.150815  | -0.832209  | -0.340894 |  0.89291   |  1.7605    | -1.67377   |
|     19 | south_korea  | -0.169457  |  -0.169457  |  1.11685   | -0.340894 | -2.24438   |  0.336795  | -0.739091  |
|     20 | france       | -0.170508  |  -0.170508  | -0.360337  | -0.584389 | -1.4545    |  0.764395  |  1.46339   |
|     21 | indonesia    | -0.370243  |  -0.370243  | -1.54941   |  0.267845 |  0.802311  | -1.04881   |  0.858211  |
|     22 | morocco      | -0.424786  |  -0.424786  |  0.0490146 | -0.486991 | -1.24844   | -0.72358   | -0.0711186 |
|     23 | rwanda       | -0.453413  |  -0.453413  |  0.26938   | -1.53402  | -0.626019  | -0.92976   | -0.352833  |
|     24 | canada       | -0.472864  |  -0.472864  |  0.137446  | -1.04703  | -1.50192   | -0.561684  |  0.13814   |
|     25 | vietnam      | -0.559987  |  -0.559987  | -0.844095  | -0.827884 |  0.286516  |  0.076985  | -1.39481   |
|     26 | germany      | -0.590727  |  -0.590727  | -0.680544  | -0.51134  | -1.10355   |  1.00264   | -1.37014   |
|     27 | oman         | -0.615642  |  -0.615642  |  0.306226  | -1.02268  | -0.419962  | -1.69438   | -1.5418    |
|     28 | usa          | -0.633313  |  -0.633313  | -0.411447  | -1.14443  | -0.488975  | -0.879581  | -0.586071  |
|     29 | uae          | -0.749459  |  -0.749459  | -1.12032   | -1.16878  | -0.571397  | -0.0955505 | -0.356111  |
|     30 | switzerland  | -0.755784  |  -0.755784  | -0.615885  | -0.681787 |  0.0320532 | -1.62422   | -1.33823   |
|     31 | kazakhstan   | -0.951317  |  -0.951317  | -1.37825   | -1.33922  | -0.923655  |  0.32443   | -0.879861  |
|     32 | mongolia     | -1.06954   |  -1.06954   | -2.2628    | -1.58272  |  0.654801  | -1.65843   |  0.51767   |

## 2.8 Model 8: Logistic Regression
_LR on xGF/60, xGA/60 features. Team strength from coefficients._

|   rank | team         |    score |   lr_score |   es_xgf60 |   es_xga60 |
|-------:|:-------------|---------:|-----------:|-----------:|-----------:|
|      1 | serbia       | 0.694847 |   0.694847 |     2.7292 |     2.5557 |
|      2 | singapore    | 0.675785 |   0.675785 |     2.3747 |     2.719  |
|      3 | uk           | 0.663568 |   0.663568 |     2.5616 |     2.478  |
|      4 | usa          | 0.662869 |   0.662869 |     2.4222 |     2.5895 |
|      5 | pakistan     | 0.656595 |   0.656595 |     2.967  |     2.0911 |
|      6 | oman         | 0.644805 |   0.644805 |     2.5182 |     2.3837 |
|      7 | ethiopia     | 0.643095 |   0.643095 |     2.3633 |     2.5011 |
|      8 | thailand     | 0.643093 |   0.643093 |     2.9    |     2.0531 |
|      9 | germany      | 0.636153 |   0.636153 |     2.2592 |     2.5397 |
|     10 | panama       | 0.631581 |   0.631581 |     2.3905 |     2.3983 |
|     11 | france       | 0.627577 |   0.627577 |     2.3001 |     2.4459 |
|     12 | south_korea  | 0.623755 |   0.623755 |     2.6243 |     2.1487 |
|     13 | canada       | 0.616254 |   0.616254 |     2.3713 |     2.3077 |
|     14 | morocco      | 0.615825 |   0.615825 |     2.3494 |     2.323  |
|     15 | brazil       | 0.612283 |   0.612283 |     2.7514 |     1.9628 |
|     16 | iceland      | 0.610948 |   0.610948 |     2.3169 |     2.3162 |
|     17 | india        | 0.608822 |   0.608822 |     2.2848 |     2.3282 |
|     18 | guatemala    | 0.605853 |   0.605853 |     2.4866 |     2.1391 |
|     19 | vietnam      | 0.604082 |   0.604082 |     2.1001 |     2.4494 |
|     20 | china        | 0.596061 |   0.596061 |     2.4637 |     2.0901 |
|     21 | new_zealand  | 0.588268 |   0.588268 |     2.249  |     2.2151 |
|     22 | mexico       | 0.586462 |   0.586462 |     2.5253 |     1.9719 |
|     23 | indonesia    | 0.583831 |   0.583831 |     1.8616 |     2.5076 |
|     24 | mongolia     | 0.57802  |   0.57802  |     1.676  |     2.6221 |
|     25 | rwanda       | 0.576364 |   0.576364 |     2.2503 |     2.1312 |
|     26 | philippines  | 0.566264 |   0.566264 |     1.881  |     2.3692 |
|     27 | saudi_arabia | 0.557506 |   0.557506 |     1.9798 |     2.2258 |
|     28 | peru         | 0.553286 |   0.553286 |     2.2294 |     1.9881 |
|     29 | kazakhstan   | 0.544195 |   0.544195 |     1.7505 |     2.3246 |
|     30 | uae          | 0.542852 |   0.542852 |     1.8046 |     2.2701 |
|     31 | netherlands  | 0.523303 |   0.523303 |     2.0617 |     1.9195 |
|     32 | switzerland  | 0.51753  |   0.51753  |     1.8243 |     2.0775 |

## 2.9 Model 9: Random Forest
_RF with permutation importance. Teams ranked by weighted feature score._

|   rank | team         |     score |   rf_score |
|-------:|:-------------|----------:|-----------:|
|      1 | thailand     | 0.162337  |  0.162337  |
|      2 | netherlands  | 0.158133  |  0.158133  |
|      3 | pakistan     | 0.153433  |  0.153433  |
|      4 | uk           | 0.148177  |  0.148177  |
|      5 | brazil       | 0.144421  |  0.144421  |
|      6 | guatemala    | 0.143525  |  0.143525  |
|      7 | mexico       | 0.143159  |  0.143159  |
|      8 | singapore    | 0.142505  |  0.142505  |
|      9 | south_korea  | 0.140224  |  0.140224  |
|     10 | serbia       | 0.137899  |  0.137899  |
|     11 | panama       | 0.13757   |  0.13757   |
|     12 | china        | 0.134918  |  0.134918  |
|     13 | peru         | 0.134819  |  0.134819  |
|     14 | ethiopia     | 0.13404   |  0.13404   |
|     15 | germany      | 0.13288   |  0.13288   |
|     16 | france       | 0.132641  |  0.132641  |
|     17 | new_zealand  | 0.127876  |  0.127876  |
|     18 | philippines  | 0.123805  |  0.123805  |
|     19 | vietnam      | 0.122287  |  0.122287  |
|     20 | canada       | 0.121804  |  0.121804  |
|     21 | rwanda       | 0.119748  |  0.119748  |
|     22 | morocco      | 0.119419  |  0.119419  |
|     23 | kazakhstan   | 0.118926  |  0.118926  |
|     24 | iceland      | 0.117038  |  0.117038  |
|     25 | uae          | 0.116821  |  0.116821  |
|     26 | india        | 0.115332  |  0.115332  |
|     27 | usa          | 0.114295  |  0.114295  |
|     28 | saudi_arabia | 0.112384  |  0.112384  |
|     29 | oman         | 0.111485  |  0.111485  |
|     30 | switzerland  | 0.104446  |  0.104446  |
|     31 | indonesia    | 0.103477  |  0.103477  |
|     32 | mongolia     | 0.0897977 |  0.0897977 |

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
| thailand     |             4 |            2 |                  1 |          3 |             4 |         4 |                4 |               8 |         1 |                 1 |         3.2 |         4.62222 |                1 |
| brazil       |             1 |            3 |                  2 |          1 |             1 |         1 |                1 |              15 |         5 |                 5 |         3.5 |        18.9444  |                2 |
| pakistan     |             5 |            1 |                  3 |          7 |             5 |         5 |                2 |               5 |         3 |                 2 |         3.8 |         3.51111 |                3 |
| netherlands  |             2 |           10 |                  4 |          2 |             2 |         2 |                3 |              31 |         2 |                17 |         7.5 |        92.5     |                4 |
| china        |             7 |            6 |                  6 |          5 |             7 |         7 |                7 |              20 |        12 |                12 |         8.9 |        20.9889  |                5 |
| peru         |             3 |            8 |                  9 |          6 |             3 |         3 |                5 |              28 |        13 |                14 |         9.2 |        59.5111  |                6 |
| serbia       |            17 |            9 |                 12 |         11 |            14 |        14 |               14 |               1 |        10 |                 3 |        10.5 |        25.6111  |                7 |
| uk           |            14 |           13 |                  7 |         24 |            17 |        17 |                6 |               3 |         4 |                 4 |        10.9 |        50.7667  |                8 |
| guatemala    |            13 |            7 |                 10 |         12 |            12 |        12 |               11 |              18 |         6 |                11 |        11.2 |        10.8444  |                9 |
| panama       |             8 |           18 |                 11 |         22 |             9 |         9 |                9 |              10 |        11 |                10 |        11.7 |        20.9     |               10 |
| iceland      |             9 |           17 |                 20 |          4 |             8 |         8 |               10 |              16 |        24 |                23 |        13.9 |        49.2111  |               12 |
| india        |             6 |           19 |                 17 |         10 |             6 |         6 |               12 |              17 |        26 |                20 |        13.9 |        48.3222  |               12 |
| ethiopia     |            11 |           20 |                 21 |          9 |            10 |        10 |               16 |               7 |        14 |                21 |        13.9 |        28.1     |               12 |
| mexico       |            19 |            4 |                  5 |         26 |            21 |        21 |                8 |              22 |         7 |                 7 |        14   |        71.7778  |               14 |
| south_korea  |            21 |            5 |                 13 |         16 |            20 |        20 |               19 |              12 |         9 |                 8 |        14.3 |        32.9     |               15 |
| singapore    |            12 |           26 |                 30 |         17 |            16 |        16 |               18 |               2 |         8 |                 9 |        15.4 |        69.1556  |               16 |
| new_zealand  |            20 |           15 |                 16 |          8 |            15 |        15 |               17 |              21 |        17 |                18 |        16.2 |        12.6222  |               17 |
| france       |            24 |           21 |                  8 |         28 |            23 |        23 |               20 |              11 |        16 |                 6 |        18   |        55.1111  |               18 |
| philippines  |            10 |           29 |                 24 |         13 |            11 |        11 |               13 |              26 |        18 |                28 |        18.3 |        59.1222  |               19 |
| morocco      |            23 |           16 |                 15 |         15 |            24 |        24 |               22 |              14 |        22 |                13 |        18.8 |        20.6222  |               20 |
| canada       |            25 |           14 |                 14 |         21 |            25 |        25 |               24 |              13 |        20 |                19 |        20   |        23.7778  |               21 |
| indonesia    |            15 |           31 |                 23 |         14 |            13 |        13 |               21 |              23 |        31 |                27 |        21.1 |        50.7667  |               22 |
| saudi_arabia |            22 |           23 |                 18 |         19 |            18 |        18 |               15 |              27 |        28 |                26 |        21.4 |        20.0444  |               23 |
| vietnam      |            16 |           27 |                 31 |         23 |            19 |        19 |               25 |              19 |        19 |                24 |        22.2 |        21.2889  |               24 |
| oman         |            29 |           11 |                 26 |         25 |            28 |        28 |               27 |               6 |        29 |                16 |        22.5 |        70.0556  |               25 |
| germany      |            28 |           25 |                 19 |         27 |            27 |        27 |               26 |               9 |        15 |                22 |        22.5 |        40.0556  |               25 |
| usa          |            27 |           22 |                 25 |         29 |            29 |        29 |               28 |               4 |        27 |                15 |        23.5 |        65.8333  |               27 |
| uae          |            18 |           28 |                 28 |         18 |            22 |        22 |               29 |              30 |        25 |                29 |        24.9 |        21.2111  |               28 |
| rwanda       |            30 |           12 |                 27 |         32 |            30 |        30 |               23 |              25 |        21 |                25 |        25.5 |        34.9444  |               29 |
| switzerland  |            26 |           24 |                 29 |         20 |            26 |        26 |               30 |              32 |        30 |                31 |        27.4 |        13.6     |               30 |
| kazakhstan   |            32 |           30 |                 22 |         30 |            31 |        31 |               31 |              29 |        23 |                30 |        28.9 |        12.1     |               31 |
| mongolia     |            31 |           32 |                 32 |         31 |            32 |        32 |               32 |              24 |        32 |                32 |        31   |         6.22222 |               32 |

## 2.12 Recommended Final Power Ranking
The **consensus ranking** (mean rank across all 10 models) is our recommended final ranking.
Teams with low rank variance are robustly ranked; those with high variance should be scrutinized.

| team         |   mean_rank |   rank_variance |   recommended_rank |
|:-------------|------------:|----------------:|-------------------:|
| thailand     |         3.2 |         4.62222 |                  1 |
| brazil       |         3.5 |        18.9444  |                  2 |
| pakistan     |         3.8 |         3.51111 |                  3 |
| netherlands  |         7.5 |        92.5     |                  4 |
| china        |         8.9 |        20.9889  |                  5 |
| peru         |         9.2 |        59.5111  |                  6 |
| serbia       |        10.5 |        25.6111  |                  7 |
| uk           |        10.9 |        50.7667  |                  8 |
| guatemala    |        11.2 |        10.8444  |                  9 |
| panama       |        11.7 |        20.9     |                 10 |
| iceland      |        13.9 |        49.2111  |                 11 |
| india        |        13.9 |        48.3222  |                 12 |
| ethiopia     |        13.9 |        28.1     |                 13 |
| mexico       |        14   |        71.7778  |                 14 |
| south_korea  |        14.3 |        32.9     |                 15 |
| singapore    |        15.4 |        69.1556  |                 16 |
| new_zealand  |        16.2 |        12.6222  |                 17 |
| france       |        18   |        55.1111  |                 18 |
| philippines  |        18.3 |        59.1222  |                 19 |
| morocco      |        18.8 |        20.6222  |                 20 |
| canada       |        20   |        23.7778  |                 21 |
| indonesia    |        21.1 |        50.7667  |                 22 |
| saudi_arabia |        21.4 |        20.0444  |                 23 |
| vietnam      |        22.2 |        21.2889  |                 24 |
| oman         |        22.5 |        70.0556  |                 25 |
| germany      |        22.5 |        40.0556  |                 26 |
| usa          |        23.5 |        65.8333  |                 27 |
| uae          |        24.9 |        21.2111  |                 28 |
| rwanda       |        25.5 |        34.9444  |                 29 |
| switzerland  |        27.4 |        13.6     |                 30 |
| kazakhstan   |        28.9 |        12.1     |                 31 |
| mongolia     |        31   |         6.22222 |                 32 |

---

# Section 3: Phase 1a — Win Probabilities (Round 1 Matchups)

## 3.1 All 16 Matchup Probabilities (Five Methods + Ensemble)
|   game | home_team   | away_team    |   p_lr |   p_elo |   p_bt |   p_log5 |   p_mc |   p_ensemble |   disagreement | flag_disagree   |
|-------:|:------------|:-------------|-------:|--------:|-------:|---------:|-------:|-------------:|---------------:|:----------------|
|      1 | brazil      | kazakhstan   | 0.7079 |  0.8521 | 0.8219 |   0.612  | 0.6204 |       0.7228 |         0.2401 | YES             |
|      2 | netherlands | mongolia     | 0.7036 |  0.847  | 0.8112 |   0.6928 | 0.6119 |       0.7333 |         0.2351 | YES             |
|      3 | peru        | rwanda       | 0.5881 |  0.8175 | 0.7661 |   0.5977 | 0.5403 |       0.662  |         0.2772 | YES             |
|      4 | thailand    | oman         | 0.6581 |  0.7819 | 0.6941 |   0.6514 | 0.5905 |       0.6752 |         0.1914 | YES             |
|      5 | pakistan    | germany      | 0.7004 |  0.756  | 0.6769 |   0.5944 | 0.5817 |       0.6619 |         0.1743 | YES             |
|      6 | india       | usa          | 0.5959 |  0.7662 | 0.6877 |   0.5507 | 0.487  |       0.6175 |         0.2792 | YES             |
|      7 | panama      | switzerland  | 0.5614 |  0.6383 | 0.6423 |   0.578  | 0.6012 |       0.6042 |         0.0809 | nan             |
|      8 | iceland     | canada       | 0.5594 |  0.7584 | 0.6448 |   0.459  | 0.4755 |       0.5794 |         0.2994 | YES             |
|      9 | china       | france       | 0.6392 |  0.7804 | 0.6483 |   0.5063 | 0.4782 |       0.6105 |         0.3023 | YES             |
|     10 | philippines | morocco      | 0.5114 |  0.6532 | 0.6048 |   0.4536 | 0.4283 |       0.5302 |         0.2249 | YES             |
|     11 | ethiopia    | saudi_arabia | 0.5522 |  0.7258 | 0.5783 |   0.4852 | 0.5426 |       0.5768 |         0.2405 | YES             |
|     12 | singapore   | new_zealand  | 0.4905 |  0.5463 | 0.526  |   0.4378 | 0.5276 |       0.5056 |         0.1085 | YES             |
|     13 | guatemala   | south_korea  | 0.5587 |  0.6821 | 0.5668 |   0.5224 | 0.4912 |       0.5643 |         0.1908 | YES             |
|     14 | uk          | mexico       | 0.4865 |  0.6509 | 0.5429 |   0.4892 | 0.5218 |       0.5383 |         0.1644 | YES             |
|     15 | vietnam     | serbia       | 0.5253 |  0.5667 | 0.5081 |   0.4129 | 0.3996 |       0.4825 |         0.1671 | YES             |
|     16 | indonesia   | uae          | 0.5238 |  0.684  | 0.5749 |   0.5142 | 0.51   |       0.5614 |         0.1739 | YES             |

### ⚠️ 15 Matchups with >10pp Model Disagreement (warrant extra scrutiny):
|   game | home_team   | away_team    |   p_lr |   p_elo |   p_bt |   p_log5 |   p_mc |   p_ensemble |   disagreement | flag_disagree   |
|-------:|:------------|:-------------|-------:|--------:|-------:|---------:|-------:|-------------:|---------------:|:----------------|
|      1 | brazil      | kazakhstan   | 0.7079 |  0.8521 | 0.8219 |   0.612  | 0.6204 |       0.7228 |         0.2401 | YES             |
|      2 | netherlands | mongolia     | 0.7036 |  0.847  | 0.8112 |   0.6928 | 0.6119 |       0.7333 |         0.2351 | YES             |
|      3 | peru        | rwanda       | 0.5881 |  0.8175 | 0.7661 |   0.5977 | 0.5403 |       0.662  |         0.2772 | YES             |
|      4 | thailand    | oman         | 0.6581 |  0.7819 | 0.6941 |   0.6514 | 0.5905 |       0.6752 |         0.1914 | YES             |
|      5 | pakistan    | germany      | 0.7004 |  0.756  | 0.6769 |   0.5944 | 0.5817 |       0.6619 |         0.1743 | YES             |
|      6 | india       | usa          | 0.5959 |  0.7662 | 0.6877 |   0.5507 | 0.487  |       0.6175 |         0.2792 | YES             |
|      8 | iceland     | canada       | 0.5594 |  0.7584 | 0.6448 |   0.459  | 0.4755 |       0.5794 |         0.2994 | YES             |
|      9 | china       | france       | 0.6392 |  0.7804 | 0.6483 |   0.5063 | 0.4782 |       0.6105 |         0.3023 | YES             |
|     10 | philippines | morocco      | 0.5114 |  0.6532 | 0.6048 |   0.4536 | 0.4283 |       0.5302 |         0.2249 | YES             |
|     11 | ethiopia    | saudi_arabia | 0.5522 |  0.7258 | 0.5783 |   0.4852 | 0.5426 |       0.5768 |         0.2405 | YES             |
|     12 | singapore   | new_zealand  | 0.4905 |  0.5463 | 0.526  |   0.4378 | 0.5276 |       0.5056 |         0.1085 | YES             |
|     13 | guatemala   | south_korea  | 0.5587 |  0.6821 | 0.5668 |   0.5224 | 0.4912 |       0.5643 |         0.1908 | YES             |
|     14 | uk          | mexico       | 0.4865 |  0.6509 | 0.5429 |   0.4892 | 0.5218 |       0.5383 |         0.1644 | YES             |
|     15 | vietnam     | serbia       | 0.5253 |  0.5667 | 0.5081 |   0.4129 | 0.3996 |       0.4825 |         0.1671 | YES             |
|     16 | indonesia   | uae          | 0.5238 |  0.684  | 0.5749 |   0.5142 | 0.51   |       0.5614 |         0.1739 | YES             |

## 3.2 Win Probability Model Calibration (LR)
| metric               |   value |
|:---------------------|--------:|
| in_sample_accuracy   |  0.5846 |
| in_sample_brier      |  0.2407 |
| in_sample_logloss    |  0.6744 |
| cv10_acc_mean        |  0.5823 |
| cv10_acc_std         |  0.0285 |
| cv10_brier_mean      |  0.242  |
| cv10_logloss_mean    |  0.677  |
| loto_acc_mean        |  0.5739 |
| loto_acc_std         |  0.052  |
| baseline_always_home |  0.564  |
| baseline_higher_pts  |  0.5816 |
| baseline_higher_xgd  |  0.5457 |

---

# Section 4: Phase 1b — Line Disparity Analysis

## 4.1 Method 1: Raw xG ratio (sum first_off / sum second_off). No adjustments.
|   rank | team         |   ratio |   f1_xg |   f2_xg |
|-------:|:-------------|--------:|--------:|--------:|
|      1 | usa          |  1.4046 |  81.27  |  57.858 |
|      2 | guatemala    |  1.3751 |  85.135 |  61.91  |
|      3 | saudi_arabia |  1.3724 |  70.256 |  51.192 |
|      4 | uae          |  1.372  |  62.693 |  45.696 |
|      5 | france       |  1.3602 |  78.88  |  57.994 |
|      6 | iceland      |  1.3443 |  77.545 |  57.685 |
|      7 | singapore    |  1.2615 |  80.333 |  63.681 |
|      8 | new_zealand  |  1.2436 |  72.189 |  58.049 |
|      9 | panama       |  1.2169 |  78.587 |  64.578 |
|     10 | rwanda       |  1.2141 |  68.895 |  56.746 |
|     11 | peru         |  1.2085 |  75.46  |  62.441 |
|     12 | uk           |  1.2037 |  86.9   |  72.196 |
|     13 | india        |  1.1772 |  75.36  |  64.014 |
|     14 | serbia       |  1.1487 |  84.046 |  73.168 |
|     15 | south_korea  |  1.1398 |  80.456 |  70.586 |
|     16 | netherlands  |  1.1226 |  67.179 |  59.842 |
|     17 | mongolia     |  1.0823 |  50.699 |  46.844 |
|     18 | china        |  1.0696 |  79.406 |  74.236 |
|     19 | mexico       |  1.0683 |  77.936 |  72.953 |
|     20 | canada       |  1.0509 |  73.939 |  70.36  |
|     21 | pakistan     |  1.0411 |  86.865 |  83.437 |
|     22 | philippines  |  1.0296 |  61.014 |  59.262 |
|     23 | morocco      |  1.0241 |  73.205 |  71.482 |
|     24 | kazakhstan   |  1.0172 |  52.787 |  51.894 |
|     25 | oman         |  0.9984 |  72.123 |  72.239 |
|     26 | thailand     |  0.9938 |  85.518 |  86.054 |
|     27 | brazil       |  0.9923 |  80.83  |  81.457 |
|     28 | indonesia    |  0.9885 |  57.101 |  57.767 |
|     29 | germany      |  0.979  |  67.378 |  68.826 |
|     30 | vietnam      |  0.9528 |  61.713 |  64.773 |
|     31 | ethiopia     |  0.9382 |  68.039 |  72.521 |
|     32 | switzerland  |  0.8992 |  52.475 |  58.358 |

## 4.2 Method 2: xG/60 ratio. Fixes TOI confounding.
|   rank | team         |   ratio |   f1_xg60 |   f2_xg60 |
|-------:|:-------------|--------:|----------:|----------:|
|      1 | usa          |  1.3692 |    2.7272 |    1.9918 |
|      2 | saudi_arabia |  1.3591 |    2.2384 |    1.6469 |
|      3 | guatemala    |  1.3563 |    2.8022 |    2.066  |
|      4 | uae          |  1.354  |    1.9893 |    1.4693 |
|      5 | france       |  1.3408 |    2.5479 |    1.9003 |
|      6 | iceland      |  1.3218 |    2.5841 |    1.955  |
|      7 | singapore    |  1.2555 |    2.622  |    2.0883 |
|      8 | new_zealand  |  1.229  |    2.4266 |    1.9744 |
|      9 | peru         |  1.1993 |    2.3803 |    1.9847 |
|     10 | panama       |  1.1992 |    2.545  |    2.1222 |
|     11 | rwanda       |  1.1949 |    2.3308 |    1.9507 |
|     12 | uk           |  1.1678 |    2.7099 |    2.3206 |
|     13 | india        |  1.1661 |    2.4216 |    2.0767 |
|     14 | serbia       |  1.1174 |    2.8101 |    2.5148 |
|     15 | netherlands  |  1.1113 |    2.1378 |    1.9238 |
|     16 | south_korea  |  1.1027 |    2.7109 |    2.4584 |
|     17 | mexico       |  1.0561 |    2.5563 |    2.4204 |
|     18 | china        |  1.0474 |    2.498  |    2.385  |
|     19 | mongolia     |  1.0458 |    1.6411 |    1.5693 |
|     20 | pakistan     |  1.0335 |    2.9773 |    2.8807 |
|     21 | canada       |  1.0121 |    2.3702 |    2.3419 |
|     22 | kazakhstan   |  1.0007 |    1.6681 |    1.6669 |
|     23 | philippines  |  0.9998 |    1.8401 |    1.8404 |
|     24 | morocco      |  0.9973 |    2.3122 |    2.3184 |
|     25 | oman         |  0.9896 |    2.4744 |    2.5005 |
|     26 | brazil       |  0.9816 |    2.7021 |    2.7527 |
|     27 | thailand     |  0.9695 |    2.8221 |    2.9108 |
|     28 | indonesia    |  0.9612 |    1.8051 |    1.8781 |
|     29 | germany      |  0.9598 |    2.172  |    2.263  |
|     30 | vietnam      |  0.9463 |    2.0137 |    2.1281 |
|     31 | ethiopia     |  0.9047 |    2.2229 |    2.457  |
|     32 | switzerland  |  0.8888 |    1.7091 |    1.9229 |

## 4.3 Method 3: Matchup-adjusted xG/60. Scales for opponent defensive quality.
|   rank | team         |   ratio |   f1_adj_xg60 |   f2_adj_xg60 |
|-------:|:-------------|--------:|--------------:|--------------:|
|      1 | usa          |  1.3803 |        2.7372 |        1.9831 |
|      2 | saudi_arabia |  1.36   |        2.2371 |        1.6449 |
|      3 | guatemala    |  1.3575 |        2.8053 |        2.0665 |
|      4 | uae          |  1.3573 |        1.9928 |        1.4682 |
|      5 | france       |  1.3451 |        2.5526 |        1.8977 |
|      6 | iceland      |  1.3266 |        2.5926 |        1.9543 |
|      7 | singapore    |  1.2553 |        2.6258 |        2.0917 |
|      8 | new_zealand  |  1.2332 |        2.431  |        1.9713 |
|      9 | peru         |  1.2038 |        2.3851 |        1.9813 |
|     10 | panama       |  1.2006 |        2.5479 |        2.1221 |
|     11 | rwanda       |  1.1972 |        2.3368 |        1.9518 |
|     12 | uk           |  1.1688 |        2.7139 |        2.322  |
|     13 | india        |  1.1662 |        2.4208 |        2.0758 |
|     14 | serbia       |  1.1174 |        2.8134 |        2.5178 |
|     15 | netherlands  |  1.1142 |        2.1432 |        1.9236 |
|     16 | south_korea  |  1.1009 |        2.7114 |        2.4629 |
|     17 | mexico       |  1.0592 |        2.562  |        2.4188 |
|     18 | china        |  1.0508 |        2.5024 |        2.3813 |
|     19 | mongolia     |  1.0495 |        1.6429 |        1.5654 |
|     20 | pakistan     |  1.0305 |        2.9683 |        2.8805 |
|     21 | canada       |  1.014  |        2.3751 |        2.3424 |
|     22 | kazakhstan   |  1.0069 |        1.6752 |        1.6637 |
|     23 | philippines  |  1.0068 |        1.8476 |        1.8352 |
|     24 | morocco      |  0.9957 |        2.3061 |        2.3162 |
|     25 | oman         |  0.9913 |        2.4813 |        2.503  |
|     26 | brazil       |  0.9872 |        2.7141 |        2.7494 |
|     27 | thailand     |  0.9718 |        2.83   |        2.912  |
|     28 | germany      |  0.9612 |        2.175  |        2.2628 |
|     29 | indonesia    |  0.9609 |        1.806  |        1.8795 |
|     30 | vietnam      |  0.9474 |        2.0131 |        2.125  |
|     31 | ethiopia     |  0.9062 |        2.2288 |        2.4594 |
|     32 | switzerland  |  0.8866 |        1.706  |        1.9243 |

## 4.4 Method 4: Goals/60 ratio. Noisier but direct.
|   rank | team         |   ratio |   f1_g60 |   f2_g60 |
|-------:|:-------------|--------:|---------:|---------:|
|      1 | brazil       |  1.4132 |   3.343  |   2.3655 |
|      2 | serbia       |  1.2689 |   3.0092 |   2.3715 |
|      3 | germany      |  1.1485 |   2.6434 |   2.3016 |
|      4 | singapore    |  1.0932 |   2.1868 |   2.0004 |
|      5 | ethiopia     |  1.0366 |   2.8097 |   2.7104 |
|      6 | mongolia     |  1.0242 |   1.7155 |   1.675  |
|      7 | thailand     |  1.021  |   2.97   |   2.909  |
|      8 | france       |  0.9858 |   2.0349 |   2.0643 |
|      9 | kazakhstan   |  0.9649 |   1.6116 |   1.6703 |
|     10 | china        |  0.939  |   2.2021 |   2.3453 |
|     11 | india        |  0.9362 |   2.2172 |   2.3682 |
|     12 | morocco      |  0.8736 |   1.9267 |   2.2055 |
|     13 | oman         |  0.8496 |   2.2643 |   2.6653 |
|     14 | canada       |  0.8235 |   1.8913 |   2.2966 |
|     15 | netherlands  |  0.8152 |   1.7821 |   2.186  |
|     16 | mexico       |  0.8149 |   2.0008 |   2.4551 |
|     17 | rwanda       |  0.8096 |   1.7254 |   2.1313 |
|     18 | saudi_arabia |  0.7923 |   1.5293 |   1.9303 |
|     19 | iceland      |  0.7609 |   2.1661 |   2.8468 |
|     20 | uae          |  0.7566 |   1.4596 |   1.9292 |
|     21 | guatemala    |  0.7557 |   1.942  |   2.5696 |
|     22 | panama       |  0.7551 |   1.9107 |   2.5305 |
|     23 | peru         |  0.7294 |   1.9242 |   2.6382 |
|     24 | indonesia    |  0.7259 |   1.6755 |   2.3083 |
|     25 | uk           |  0.7246 |   1.8399 |   2.5393 |
|     26 | vietnam      |  0.7223 |   1.5662 |   2.1684 |
|     27 | new_zealand  |  0.7161 |   1.6807 |   2.3469 |
|     28 | south_korea  |  0.6966 |   2.426  |   3.4828 |
|     29 | philippines  |  0.6873 |   1.3873 |   2.0186 |
|     30 | usa          |  0.6835 |   2.047  |   2.995  |
|     31 | switzerland  |  0.6687 |   1.4982 |   2.2405 |
|     32 | pakistan     |  0.6435 |   2.3993 |   3.7288 |

## 4.5 Method 5: Shots/60 ratio. Volume-based measure.
|   rank | team         |   ratio |   f1_s60 |   f2_s60 |
|-------:|:-------------|--------:|---------:|---------:|
|      1 | guatemala    |  1.3131 |  29.2282 |  22.2587 |
|      2 | saudi_arabia |  1.2699 |  22.4294 |  17.662  |
|      3 | serbia       |  1.2628 |  29.9912 |  23.7496 |
|      4 | rwanda       |  1.2504 |  26.2197 |  20.9696 |
|      5 | iceland      |  1.238  |  25.5928 |  20.6734 |
|      6 | uae          |  1.2132 |  21.2598 |  17.5233 |
|      7 | france       |  1.1984 |  24.5805 |  20.512  |
|      8 | south_korea  |  1.1122 |  29.5166 |  26.539  |
|      9 | singapore    |  1.0899 |  26.3069 |  24.1361 |
|     10 | usa          |  1.0857 |  24.9665 |  22.9958 |
|     11 | uk           |  1.0683 |  24.7918 |  23.2076 |
|     12 | morocco      |  1.0607 |  25.8362 |  24.3575 |
|     13 | thailand     |  1.0524 |  25.7729 |  24.4898 |
|     14 | peru         |  1.033  |  24.8886 |  24.0931 |
|     15 | new_zealand  |  1.0302 |  23.9669 |  23.2647 |
|     16 | china        |  1.0219 |  23.3113 |  22.8107 |
|     17 | kazakhstan   |  1.0106 |  20.2244 |  20.0116 |
|     18 | oman         |  0.9912 |  24.5988 |  24.8183 |
|     19 | switzerland  |  0.9855 |  21.8868 |  22.2077 |
|     20 | india        |  0.9833 |  26.2533 |  26.6995 |
|     21 | philippines  |  0.9615 |  21.171  |  22.018  |
|     22 | netherlands  |  0.9609 |  21.0985 |  21.9567 |
|     23 | ethiopia     |  0.9527 |  24.0783 |  25.2747 |
|     24 | brazil       |  0.9396 |  23.4007 |  24.9053 |
|     25 | pakistan     |  0.9288 |  27.386  |  29.4848 |
|     26 | mongolia     |  0.9226 |  20.5218 |  22.2437 |
|     27 | panama       |  0.9147 |  22.6048 |  24.7131 |
|     28 | canada       |  0.9138 |  23.7852 |  26.0284 |
|     29 | germany      |  0.9104 |  20.9535 |  23.0162 |
|     30 | mexico       |  0.9055 |  25.3868 |  28.0351 |
|     31 | vietnam      |  0.8982 |  20.981  |  23.3594 |
|     32 | indonesia    |  0.851  |  20.8331 |  24.4805 |

## 4.6 Method 6: xG share (distance from 50/50 balance).
|   rank | team         |   ratio |   f1_xg_share |   disparity_from_05 |
|-------:|:-------------|--------:|--------------:|--------------------:|
|      1 | usa          |  0.0841 |        0.5841 |              0.0841 |
|      2 | guatemala    |  0.079  |        0.579  |              0.079  |
|      3 | saudi_arabia |  0.0785 |        0.5785 |              0.0785 |
|      4 | uae          |  0.0784 |        0.5784 |              0.0784 |
|      5 | france       |  0.0763 |        0.5763 |              0.0763 |
|      6 | iceland      |  0.0734 |        0.5734 |              0.0734 |
|      7 | singapore    |  0.0578 |        0.5578 |              0.0578 |
|      8 | new_zealand  |  0.0543 |        0.5543 |              0.0543 |
|      9 | panama       |  0.0489 |        0.5489 |              0.0489 |
|     10 | rwanda       |  0.0483 |        0.5483 |              0.0483 |
|     11 | peru         |  0.0472 |        0.5472 |              0.0472 |
|     12 | uk           |  0.0462 |        0.5462 |              0.0462 |
|     13 | india        |  0.0407 |        0.5407 |              0.0407 |
|     14 | serbia       |  0.0346 |        0.5346 |              0.0346 |
|     15 | south_korea  |  0.0327 |        0.5327 |              0.0327 |
|     16 | netherlands  |  0.0289 |        0.5289 |              0.0289 |
|     17 | switzerland  |  0.0265 |        0.4735 |              0.0265 |
|     18 | mongolia     |  0.0198 |        0.5198 |              0.0198 |
|     19 | china        |  0.0168 |        0.5168 |              0.0168 |
|     20 | mexico       |  0.0165 |        0.5165 |              0.0165 |
|     21 | ethiopia     |  0.0159 |        0.4841 |              0.0159 |
|     22 | canada       |  0.0124 |        0.5124 |              0.0124 |
|     23 | vietnam      |  0.0121 |        0.4879 |              0.0121 |
|     24 | pakistan     |  0.0101 |        0.5101 |              0.0101 |
|     25 | philippines  |  0.0073 |        0.5073 |              0.0073 |
|     26 | morocco      |  0.006  |        0.506  |              0.006  |
|     27 | germany      |  0.0053 |        0.4947 |              0.0053 |
|     28 | kazakhstan   |  0.0043 |        0.5043 |              0.0043 |
|     29 | indonesia    |  0.0029 |        0.4971 |              0.0029 |
|     30 | brazil       |  0.0019 |        0.4981 |              0.0019 |
|     31 | thailand     |  0.0016 |        0.4984 |              0.0016 |
|     32 | oman         |  0.0004 |        0.4996 |              0.0004 |

## 4.7 Method 7: Z-score gap. League-standardized first vs second line xG/60.
|   rank | team         |   ratio |   z_first |   z_second |   z_gap |
|-------:|:-------------|--------:|----------:|-----------:|--------:|
|      1 | guatemala    |  1.9615 |    1.4526 |    -0.5089 |  1.9615 |
|      2 | usa          |  1.9595 |    1.2528 |    -0.7067 |  1.9595 |
|      3 | france       |  1.7255 |    0.7749 |    -0.9505 |  1.7255 |
|      4 | iceland      |  1.6763 |    0.8715 |    -0.8047 |  1.6763 |
|      5 | saudi_arabia |  1.5758 |   -0.0497 |    -1.6255 |  1.5758 |
|      6 | singapore    |  1.4218 |    0.9724 |    -0.4494 |  1.4218 |
|      7 | uae          |  1.3857 |   -0.7132 |    -2.0989 |  1.3857 |
|      8 | new_zealand  |  1.2048 |    0.4518 |    -0.753  |  1.2048 |
|      9 | panama       |  1.1266 |    0.7674 |    -0.3591 |  1.1266 |
|     10 | peru         |  1.0542 |    0.3286 |    -0.7256 |  1.0542 |
|     11 | uk           |  1.0373 |    1.2068 |     0.1695 |  1.0373 |
|     12 | rwanda       |  1.0128 |    0.1967 |    -0.8161 |  1.0128 |
|     13 | india        |  0.9189 |    0.4386 |    -0.4803 |  0.9189 |
|     14 | serbia       |  0.7868 |    1.4736 |     0.6868 |  0.7868 |
|     15 | south_korea  |  0.6729 |    1.2095 |     0.5366 |  0.6729 |
|     16 | netherlands  |  0.5704 |   -0.3176 |    -0.8879 |  0.5704 |
|     17 | mexico       |  0.362  |    0.7974 |     0.4354 |  0.362  |
|     18 | china        |  0.3011 |    0.6422 |     0.3411 |  0.3011 |
|     19 | pakistan     |  0.2574 |    1.9192 |     1.6618 |  0.2574 |
|     20 | mongolia     |  0.1913 |   -1.6411 |    -1.8324 |  0.1913 |
|     21 | canada       |  0.0754 |    0.3015 |     0.2261 |  0.0754 |
|     22 | kazakhstan   |  0.0031 |   -1.5691 |    -1.5723 |  0.0031 |
|     23 | philippines  | -0.0009 |   -1.1109 |    -1.1101 | -0.0009 |
|     24 | morocco      | -0.0166 |    0.1469 |     0.1635 | -0.0166 |
|     25 | oman         | -0.0695 |    0.5792 |     0.6487 | -0.0695 |
|     26 | brazil       | -0.1347 |    1.1859 |     1.3206 | -0.1347 |
|     27 | indonesia    | -0.1943 |   -1.204  |    -1.0097 | -0.1943 |
|     28 | thailand     | -0.2365 |    1.5056 |     1.7421 | -0.2365 |
|     29 | germany      | -0.2425 |   -0.2265 |     0.016  | -0.2425 |
|     30 | vietnam      | -0.3047 |   -0.6483 |    -0.3435 | -0.3047 |
|     31 | switzerland  | -0.5696 |   -1.4599 |    -0.8903 | -0.5696 |
|     32 | ethiopia     | -0.6239 |   -0.0909 |     0.533  | -0.6239 |

## 4.8 Method 8: OLS regression controlling for team and defensive quality.
|   rank | team         |   ratio |   reg_gap |
|-------:|:-------------|--------:|----------:|
|      1 | iceland      |  0.6109 |    0.6109 |
|      2 | saudi_arabia |  0.4905 |    0.4905 |
|      3 | guatemala    |  0.4387 |    0.4387 |
|      4 | singapore    |  0.4294 |    0.4294 |
|      5 | france       |  0.3859 |    0.3859 |
|      6 | new_zealand  |  0.322  |    0.322  |
|      7 | uk           |  0.2685 |    0.2685 |
|      8 | usa          |  0.259  |    0.259  |
|      9 | netherlands  |  0.227  |    0.227  |
|     10 | uae          |  0.2125 |    0.2125 |
|     11 | india        |  0.2077 |    0.2077 |
|     12 | south_korea  |  0.1498 |    0.1498 |
|     13 | peru         |  0.0746 |    0.0746 |
|     14 | china        |  0.0705 |    0.0705 |
|     15 | thailand     |  0.0351 |    0.0351 |
|     16 | pakistan     | -0.0103 |   -0.0103 |
|     17 | canada       | -0.0782 |   -0.0782 |
|     18 | serbia       | -0.1013 |   -0.1013 |
|     19 | brazil       | -0.107  |   -0.107  |
|     20 | mexico       | -0.1176 |   -0.1176 |
|     21 | panama       | -0.1204 |   -0.1204 |
|     22 | mongolia     | -0.171  |   -0.171  |
|     23 | switzerland  | -0.1717 |   -0.1717 |
|     24 | ethiopia     | -0.2027 |   -0.2027 |
|     25 | indonesia    | -0.2081 |   -0.2081 |
|     26 | rwanda       | -0.2337 |   -0.2337 |
|     27 | philippines  | -0.2425 |   -0.2425 |
|     28 | vietnam      | -0.2506 |   -0.2506 |
|     29 | morocco      | -0.2718 |   -0.2718 |
|     30 | oman         | -0.3183 |   -0.3183 |
|     31 | germany      | -0.3453 |   -0.3453 |
|     32 | kazakhstan   | -0.6729 |   -0.6729 |

## 4.9 Method 9: TOI-weighted average xG/60 per line.
|   rank | team         |   ratio |   f1_toi_wt_xg60 |   f2_toi_wt_xg60 |
|-------:|:-------------|--------:|-----------------:|-----------------:|
|      1 | usa          |  1.3692 |           2.7272 |           1.9918 |
|      2 | saudi_arabia |  1.3591 |           2.2384 |           1.6469 |
|      3 | guatemala    |  1.3563 |           2.8022 |           2.066  |
|      4 | uae          |  1.354  |           1.9893 |           1.4693 |
|      5 | france       |  1.3408 |           2.5479 |           1.9003 |
|      6 | iceland      |  1.3218 |           2.5841 |           1.955  |
|      7 | singapore    |  1.2555 |           2.622  |           2.0883 |
|      8 | new_zealand  |  1.229  |           2.4266 |           1.9744 |
|      9 | peru         |  1.1993 |           2.3803 |           1.9847 |
|     10 | panama       |  1.1992 |           2.545  |           2.1222 |
|     11 | rwanda       |  1.1949 |           2.3308 |           1.9507 |
|     12 | uk           |  1.1678 |           2.7099 |           2.3206 |
|     13 | india        |  1.1661 |           2.4216 |           2.0767 |
|     14 | serbia       |  1.1174 |           2.8101 |           2.5148 |
|     15 | netherlands  |  1.1113 |           2.1378 |           1.9238 |
|     16 | south_korea  |  1.1027 |           2.7109 |           2.4584 |
|     17 | mexico       |  1.0561 |           2.5563 |           2.4204 |
|     18 | china        |  1.0474 |           2.498  |           2.385  |
|     19 | mongolia     |  1.0458 |           1.6411 |           1.5693 |
|     20 | pakistan     |  1.0335 |           2.9773 |           2.8807 |
|     21 | canada       |  1.0121 |           2.3702 |           2.3419 |
|     22 | kazakhstan   |  1.0007 |           1.6681 |           1.6669 |
|     23 | philippines  |  0.9998 |           1.8401 |           1.8404 |
|     24 | morocco      |  0.9973 |           2.3122 |           2.3184 |
|     25 | oman         |  0.9896 |           2.4744 |           2.5005 |
|     26 | brazil       |  0.9816 |           2.7021 |           2.7527 |
|     27 | thailand     |  0.9695 |           2.8221 |           2.9108 |
|     28 | indonesia    |  0.9612 |           1.8051 |           1.8781 |
|     29 | germany      |  0.9598 |           2.172  |           2.263  |
|     30 | vietnam      |  0.9463 |           2.0137 |           2.1281 |
|     31 | ethiopia     |  0.9047 |           2.2229 |           2.457  |
|     32 | switzerland  |  0.8888 |           1.7091 |           1.9229 |

## 4.10 Method 10: Bootstrap CI (n=1,000). Reports mean ± 95% CI.
|   rank | team         |   ratio |   boot_mean |   boot_lo |   boot_hi |   boot_ci_width | flag_wide_ci   |
|-------:|:-------------|--------:|------------:|----------:|----------:|----------------:|:---------------|
|      1 | usa          |  1.3703 |      1.3703 |    1.2638 |    1.4872 |          0.2235 | WIDE           |
|      2 | saudi_arabia |  1.3617 |      1.3617 |    1.2647 |    1.4707 |          0.2061 | WIDE           |
|      3 | guatemala    |  1.357  |      1.357  |    1.2559 |    1.4719 |          0.216  | WIDE           |
|      4 | uae          |  1.3553 |      1.3553 |    1.2423 |    1.4728 |          0.2305 | WIDE           |
|      5 | france       |  1.3424 |      1.3424 |    1.2397 |    1.4554 |          0.2158 | WIDE           |
|      6 | iceland      |  1.3244 |      1.3244 |    1.2228 |    1.435  |          0.2122 | WIDE           |
|      7 | singapore    |  1.2572 |      1.2572 |    1.1612 |    1.3591 |          0.1978 | nan            |
|      8 | new_zealand  |  1.2291 |      1.2291 |    1.1476 |    1.317  |          0.1694 | nan            |
|      9 | peru         |  1.1989 |      1.1989 |    1.1066 |    1.2913 |          0.1847 | nan            |
|     10 | panama       |  1.1983 |      1.1983 |    1.102  |    1.3051 |          0.2031 | WIDE           |
|     11 | rwanda       |  1.1974 |      1.1974 |    1.1032 |    1.3002 |          0.197  | nan            |
|     12 | uk           |  1.1683 |      1.1683 |    1.0807 |    1.269  |          0.1884 | nan            |
|     13 | india        |  1.1667 |      1.1667 |    1.0911 |    1.2422 |          0.1511 | nan            |
|     14 | serbia       |  1.1178 |      1.1178 |    1.0432 |    1.2004 |          0.1572 | nan            |
|     15 | netherlands  |  1.1098 |      1.1098 |    1.0105 |    1.2128 |          0.2023 | WIDE           |
|     16 | south_korea  |  1.1031 |      1.1031 |    1.0154 |    1.1979 |          0.1826 | nan            |
|     17 | mexico       |  1.0567 |      1.0567 |    0.9749 |    1.1466 |          0.1717 | nan            |
|     18 | mongolia     |  1.0481 |      1.0481 |    0.9583 |    1.138  |          0.1797 | nan            |
|     19 | china        |  1.0477 |      1.0477 |    0.9563 |    1.1364 |          0.1801 | nan            |
|     20 | pakistan     |  1.034  |      1.034  |    0.9581 |    1.1111 |          0.153  | nan            |
|     21 | canada       |  1.0124 |      1.0124 |    0.9353 |    1.0985 |          0.1632 | nan            |
|     22 | kazakhstan   |  1.0022 |      1.0022 |    0.9159 |    1.0997 |          0.1838 | nan            |
|     23 | philippines  |  1.0015 |      1.0015 |    0.9235 |    1.0818 |          0.1583 | nan            |
|     24 | morocco      |  0.9957 |      0.9957 |    0.9163 |    1.0793 |          0.163  | nan            |
|     25 | oman         |  0.9926 |      0.9926 |    0.9136 |    1.0734 |          0.1598 | nan            |
|     26 | brazil       |  0.9829 |      0.9829 |    0.9014 |    1.068  |          0.1666 | nan            |
|     27 | thailand     |  0.9698 |      0.9698 |    0.8861 |    1.0583 |          0.1722 | nan            |
|     28 | germany      |  0.9628 |      0.9628 |    0.8817 |    1.0514 |          0.1697 | nan            |
|     29 | indonesia    |  0.9622 |      0.9622 |    0.8829 |    1.0513 |          0.1684 | nan            |
|     30 | vietnam      |  0.9472 |      0.9472 |    0.8607 |    1.0389 |          0.1782 | nan            |
|     31 | ethiopia     |  0.9061 |      0.9061 |    0.8367 |    0.9851 |          0.1484 | nan            |
|     32 | switzerland  |  0.8893 |      0.8893 |    0.834  |    0.9544 |          0.1204 | nan            |

## 4.11 Consensus Top 10 Teams by Line Disparity
**This is the final Phase 1b submission answer.**

|   consensus_rank | team         |   mean_rank |   rank_variance |
|-----------------:|:-------------|------------:|----------------:|
|                1 | saudi_arabia |         4.1 |        24.7667  |
|                2 | guatemala    |         4.2 |        35.5111  |
|                3 | france       |         5.3 |         1.78889 |
|                4 | usa          |         5.6 |        84.4889  |
|                5 | iceland      |         6.5 |        21.8333  |
|                5 | singapore    |         6.5 |         2.27778 |
|                7 | uae          |         6.7 |        25.7889  |
|                8 | new_zealand  |        10.4 |        39.6     |
|                9 | peru         |        11.8 |        18.6222  |
|               10 | serbia       |        12.1 |        27.2111  |

## 4.12 Method Correlation Matrix (Spearman ρ)
| Unnamed: 0                |   01_raw_xg_ratio |   02_xg_per60_ratio |   03_matchup_adj_xg60 |   04_goals_per60_ratio |   05_shots_per60_ratio |   06_xg_share_proportion |   07_zscore_gap |   08_regression_line_effect |   09_toi_weighted_quality |   10_bootstrap_ci_ratio |
|:--------------------------|------------------:|--------------------:|----------------------:|-----------------------:|-----------------------:|-------------------------:|----------------:|----------------------------:|--------------------------:|------------------------:|
| 01_raw_xg_ratio           |          1        |            0.994868 |              0.994501 |            -0.171554   |             0.687683   |                 0.906158 |        0.988636 |                    0.781891 |                  0.994868 |                0.994868 |
| 02_xg_per60_ratio         |          0.994868 |            1        |              0.999633 |            -0.171554   |             0.677053   |                 0.90066  |        0.991935 |                    0.78849  |                  1        |                0.999267 |
| 03_matchup_adj_xg60       |          0.994501 |            0.999633 |              1        |            -0.163856   |             0.678152   |                 0.901393 |        0.991202 |                    0.78629  |                  0.999633 |                0.999633 |
| 04_goals_per60_ratio      |         -0.171554 |           -0.171554 |             -0.163856 |             1          |             0.00146628 |                -0.257698 |       -0.18805  |                   -0.146994 |                 -0.171554 |               -0.16239  |
| 05_shots_per60_ratio      |          0.687683 |            0.677053 |              0.678152 |             0.00146628 |             1          |                 0.641862 |        0.669355 |                    0.578079 |                  0.677053 |                0.674487 |
| 06_xg_share_proportion    |          0.906158 |            0.90066  |              0.901393 |            -0.257698   |             0.641862   |                 1        |        0.896994 |                    0.766496 |                  0.90066  |                0.90176  |
| 07_zscore_gap             |          0.988636 |            0.991935 |              0.991202 |            -0.18805    |             0.669355   |                 0.896994 |        1        |                    0.798387 |                  0.991935 |                0.990469 |
| 08_regression_line_effect |          0.781891 |            0.78849  |              0.78629  |            -0.146994   |             0.578079   |                 0.766496 |        0.798387 |                    1        |                  0.78849  |                0.783358 |
| 09_toi_weighted_quality   |          0.994868 |            1        |              0.999633 |            -0.171554   |             0.677053   |                 0.90066  |        0.991935 |                    0.78849  |                  1        |                0.999267 |
| 10_bootstrap_ci_ratio     |          0.994868 |            0.999267 |              0.999633 |            -0.16239    |             0.674487   |                 0.90176  |        0.990469 |                    0.783358 |                  0.999267 |                1        |

---

# Section 5: Validation Summary

## 5.1 Ranking Model Validation Metrics
| model_name    |   kendall_tau |   spearman_rho |   top8_hit_rate |   brier_score |   log_loss |   rank_inversion_rate |   accuracy |   consensus_rho |
|:--------------|--------------:|---------------:|----------------:|--------------:|-----------:|----------------------:|-----------:|----------------:|
| points        |        0.9677 |         0.9963 |           0.875 |        0.2619 |     0.7408 |                0.4177 |     0.5823 |          0.8694 |
| xgd60         |        0.3105 |         0.4388 |           0.625 |        0.2854 |     0.8017 |                0.4543 |     0.5457 |          0.7412 |
| pythagorean   |        0.4274 |         0.5616 |           0.625 |        0.2788 |     0.7859 |                0.4466 |     0.5534 |          0.8356 |
| elo           |        0.6653 |         0.8325 |           0.875 |        0.2659 |     0.7519 |                0.4146 |     0.5854 |          0.7775 |
| colley        |        0.8871 |         0.9666 |           1     |        0.2605 |     0.7382 |                0.4062 |     0.5938 |          0.8859 |
| bradley_terry |        0.8871 |         0.9666 |           1     |        0.2605 |     0.7382 |                0.4062 |     0.5938 |          0.8859 |
| composite     |        0.6855 |         0.8563 |           0.75  |        0.2653 |     0.7537 |                0.4047 |     0.5953 |          0.9431 |
| logistic      |        0.0565 |         0.0777 |           0.25  |        0.3129 |     0.8765 |                0.4939 |     0.5061 |          0.3277 |
| random_forest |        0.4274 |         0.6056 |           0.5   |        0.282  |     0.7952 |                0.4375 |     0.5625 |          0.8094 |
| monte_carlo   |        0.3145 |         0.4402 |           0.375 |        0.2904 |     0.8155 |                0.4619 |     0.5381 |          0.758  |

## 5.2 Model Agreement Matrix (% games where models agree on predicted winner)
| index         |   points |    xgd60 |   pythagorean |      elo |   colley |   bradley_terry |   composite |   logistic |   random_forest |   monte_carlo |
|:--------------|---------:|---------:|--------------:|---------:|---------:|----------------:|------------:|-----------:|----------------:|--------------:|
| points        | 1        | 0.657012 |      0.713415 | 0.833841 | 0.950457 |        0.950457 |    0.854421 |   0.521341 |        0.717988 |      0.657012 |
| xgd60         | 0.657012 | 1        |      0.810976 | 0.669207 | 0.665396 |        0.665396 |    0.769055 |   0.580793 |        0.766768 |      0.79878  |
| pythagorean   | 0.713415 | 0.810976 |      1        | 0.6875   | 0.723323 |        0.723323 |    0.816311 |   0.568598 |        0.804878 |      0.79878  |
| elo           | 0.833841 | 0.669207 |      0.6875   | 1        | 0.86814  |        0.86814  |    0.778201 |   0.503049 |        0.664634 |      0.609756 |
| colley        | 0.950457 | 0.665396 |      0.723323 | 0.86814  | 1        |        1        |    0.864329 |   0.516006 |        0.70503  |      0.647104 |
| bradley_terry | 0.950457 | 0.665396 |      0.723323 | 0.86814  | 1        |        1        |    0.864329 |   0.516006 |        0.70503  |      0.647104 |
| composite     | 0.854421 | 0.769055 |      0.816311 | 0.778201 | 0.864329 |        0.864329 |    1        |   0.549543 |        0.78125  |      0.729421 |
| logistic      | 0.521341 | 0.580793 |      0.568598 | 0.503049 | 0.516006 |        0.516006 |    0.549543 |   1        |        0.634146 |      0.748476 |
| random_forest | 0.717988 | 0.766768 |      0.804878 | 0.664634 | 0.70503  |        0.70503  |    0.78125  |   0.634146 |        1        |      0.814024 |
| monte_carlo   | 0.657012 | 0.79878  |      0.79878  | 0.609756 | 0.647104 |        0.647104 |    0.729421 |   0.748476 |        0.814024 |      1        |

## 5.3 Original Validation 1: Elo Calibration Curve
Checks whether Elo-predicted win probabilities match actual win rates when binned by decile.
|   decile |   mean_pred |   mean_actual |   n |   calibration_error |
|---------:|------------:|--------------:|----:|--------------------:|
|        0 |    0.337018 |      0.5      |  10 |           0.162982  |
|        1 |    0.405696 |      0.258065 |  31 |           0.147631  |
|        2 |    0.460228 |      0.351351 |  74 |           0.108877  |
|        3 |    0.514082 |      0.464286 | 140 |           0.0497962 |
|        4 |    0.565973 |      0.510101 | 198 |           0.0558716 |
|        5 |    0.623245 |      0.544    | 250 |           0.0792453 |
|        6 |    0.679223 |      0.60687  | 262 |           0.0723528 |
|        7 |    0.733881 |      0.638095 | 210 |           0.0957855 |
|        8 |    0.786655 |      0.771429 | 105 |           0.0152269 |
|        9 |    0.83377  |      0.78125  |  32 |           0.0525198 |

## 5.4 Original Validation 2: Bootstrap CI Overlap for Adjacent Rankings
Flags whether adjacent-ranked teams are statistically distinguishable via 95% bootstrap CIs on xGD/60.
| team         |   mean_xgd |   ci_lo |   ci_hi |   rank |
|:-------------|-----------:|--------:|--------:|-------:|
| thailand     |  0.891161  |  0.5792 |  1.1865 |      1 |
| pakistan     |  0.624895  |  0.3695 |  0.8604 |      2 |
| brazil       |  0.617716  |  0.2989 |  0.8998 |      3 |
| mexico       |  0.502351  |  0.274  |  0.7457 |      4 |
| netherlands  |  0.496285  |  0.2709 |  0.7453 |      5 |
| uk           |  0.442818  |  0.1587 |  0.7277 |      6 |
| china        |  0.426078  |  0.1944 |  0.6769 |      7 |
| france       |  0.396499  |  0.1628 |  0.6192 |      8 |
| peru         |  0.361174  |  0.1345 |  0.5998 |      9 |
| guatemala    |  0.279     | -0.0041 |  0.557  |     10 |
| panama       |  0.195872  | -0.0738 |  0.4457 |     11 |
| serbia       |  0.159926  | -0.1412 |  0.4356 |     12 |
| south_korea  |  0.10556   | -0.2355 |  0.3903 |     13 |
| canada       |  0.0920695 | -0.1638 |  0.349  |     14 |
| morocco      |  0.071689  | -0.1848 |  0.3384 |     15 |
| new_zealand  |  0.035772  | -0.2274 |  0.3361 |     16 |
| india        |  0.0171171 | -0.2481 |  0.283  |     17 |
| saudi_arabia | -0.146377  | -0.4219 |  0.0937 |     18 |
| germany      | -0.16945   | -0.3894 |  0.0672 |     19 |
| iceland      | -0.226967  | -0.5014 |  0.0657 |     20 |
| kazakhstan   | -0.263612  | -0.5093 |  0.0358 |     21 |
| indonesia    | -0.273626  | -0.4988 | -0.0331 |     22 |
| philippines  | -0.274989  | -0.5287 | -0.0473 |     23 |
| ethiopia     | -0.283759  | -0.5286 | -0.013  |     24 |
| uae          | -0.377667  | -0.6832 | -0.0898 |     25 |
| switzerland  | -0.391341  | -0.6672 | -0.1306 |     26 |
| rwanda       | -0.394054  | -0.6035 | -0.1461 |     27 |
| usa          | -0.418348  | -0.7028 | -0.1083 |     28 |
| oman         | -0.421409  | -0.6996 | -0.1635 |     29 |
| singapore    | -0.523949  | -0.8552 | -0.2166 |     30 |
| vietnam      | -0.563876  | -0.8456 | -0.2813 |     31 |
| mongolia     | -0.986561  | -1.2627 | -0.7373 |     32 |

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
|      1 | brazil      | kazakhstan   |          0.7228 |
|      2 | netherlands | mongolia     |          0.7333 |
|      3 | peru        | rwanda       |          0.662  |
|      4 | thailand    | oman         |          0.6752 |
|      5 | pakistan    | germany      |          0.6619 |
|      6 | india       | usa          |          0.6175 |
|      7 | panama      | switzerland  |          0.6042 |
|      8 | iceland     | canada       |          0.5794 |
|      9 | china       | france       |          0.6105 |
|     10 | philippines | morocco      |          0.5302 |
|     11 | ethiopia    | saudi_arabia |          0.5768 |
|     12 | singapore   | new_zealand  |          0.5056 |
|     13 | guatemala   | south_korea  |          0.5643 |
|     14 | uk          | mexico       |          0.5383 |
|     15 | vietnam     | serbia       |          0.4825 |
|     16 | indonesia   | uae          |          0.5614 |

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