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
23        serbia  2.729249  2.555705  0.173544
14   netherlands  2.061704  1.919532  0.142172
16          oman  2.518218  2.383663  0.134555
21        rwanda  2.250328  2.131230  0.119097
29            uk  2.561601  2.477957  0.083644
1         canada  2.371283  2.307699  0.063584
15   new_zealand  2.248975  2.215128  0.033847
13       morocco  2.349414  2.323011  0.026403
7        iceland  2.316934  2.316159  0.000775
18        panama  2.390459  2.398326 -0.007867
8          india  2.284762  2.328236 -0.043475
3       ethiopia  2.363288  2.501097 -0.137809
4         france  2.300075  2.445912 -0.145836
30           usa  2.422177  2.589498 -0.167321
22  saudi_arabia  1.979830  2.225834 -0.246004
26   switzerland  1.824277  2.077541 -0.253263
5        germany  2.259205  2.539662 -0.280457
24     singapore  2.374702  2.718955 -0.344253
31       vietnam  2.100056  2.449369 -0.349313
28           uae  1.804596  2.270135 -0.465539
20   philippines  1.881045  2.369175 -0.488130
10    kazakhstan  1.750543  2.324585 -0.574043
9      indonesia  1.861629  2.507587 -0.645957
12      mongolia  1.675981  2.622063 -0.946082
