No multiple-comparisons correction. P1–P5 are the only confirmatory tests, each on its own 95% CI; every other contrast is exploratory.
Source: 02_main_linear (commit 112e957, src e2ae83c2b53faf80, 20 seeds 200-219), 02_main_xor (commit 112e957, src e2ae83c2b53faf80, 20 seeds 200-219)

### Ticks alive and food (mean [95% bootstrap CI], per-arm CI)

| arm | linear ticks_alive | linear food | xor ticks_alive | xor food |
|---|---|---|---|---|
| random | 1175 [993, 1367] | 0.90 | 1175 [993, 1367] | 0.90 |
| tabular_q | 2882 [1963, 3827] | 5.51 | 3124 [2269, 3986] | 5.83 |
| ebm-nolearn | 1147 [989, 1310] | 0.92 | 1161 [1003, 1321] | 0.92 |
| ebm | 1102 [853, 1417] | 1.20 | 1185 [854, 1626] | 1.81 |
| ebm-dn | 1145 [865, 1496] | 1.39 | 1403 [970, 1910] | 1.94 |
| ebm-dn-sign | 1963 [1404, 2600] | 5.50 | 1966 [1322, 2641] | 4.55 |
| ebm-dn-greedy | 1127 [897, 1397] | 1.28 | 1354 [1076, 1650] | 1.72 |
| ebm-dn-critic | 1457 [1064, 1947] | 3.17 | 1296 [968, 1772] | 2.24 |
| ebm-td | 4113 [3210, 5014] | 9.08 | 3876 [2955, 4780] | 9.01 |
| ebm-all | 2076 [1437, 2771] | 2.67 | 2131 [1547, 2825] | 2.78 |
| tabular_q_next | 3919 [3025, 4803] | 9.82 | 4174 [3268, 4879] | 10.72 |

### Lives censored at the 15-day ceiling (ticks_alive == linear 5250, xor 5250), out of n seeds

| arm | linear | xor |
|---|---|---|
| random | 0/20 | 0/20 |
| tabular_q | 9/20 | 9/20 |
| ebm-nolearn | 0/20 | 0/20 |
| ebm | 0/20 | 0/20 |
| ebm-dn | 0/20 | 0/20 |
| ebm-dn-sign | 1/20 | 2/20 |
| ebm-dn-greedy | 0/20 | 0/20 |
| ebm-dn-critic | 1/20 | 1/20 |
| ebm-td | 15/20 | 14/20 |
| ebm-all | 2/20 | 2/20 |
| tabular_q_next | 14/20 | 15/20 |

### Gap fraction G = (arm - ebm-dn) / (tabular_q - ebm-dn), ticks_alive, paired bootstrap over seeds (5000 resamples), 95% CI

Denominator tabular_q - ebm-dn (linear): 1737 [739, 2744]
Denominator tabular_q - ebm-dn (xor): 1721 [518, 2892]

| arm | linear | xor |
|---|---|---|
| ebm-dn-sign | 0.47 [0.06, 1.31] | 0.33 [-0.28, 0.88] |
| ebm-dn-greedy | -0.01 [-0.50, 0.19] | -0.03 [-0.90, 0.22] |
| ebm-dn-critic | 0.18 [-0.18, 0.65] | -0.06 [-1.13, 0.35] |
| ebm-td | 1.71 [0.92, 4.13] | 1.44 [0.76, 4.06] |
| ebm-all | 0.54 [0.14, 1.15] | 0.42 [-0.16, 0.96] |

### Exploratory: G against the textbook target tabular_q_next (addendum item 10)

Denominator tabular_q_next - ebm-dn (linear): 2774 [1872, 3592]
Denominator tabular_q_next - ebm-dn (xor): 2771 [1569, 3801]

| arm | linear | xor |
|---|---|---|
| ebm-dn-sign | 0.30 [0.05, 0.63] | 0.20 [-0.13, 0.52] |
| ebm-dn-greedy | -0.01 [-0.20, 0.13] | -0.02 [-0.33, 0.15] |
| ebm-dn-critic | 0.11 [-0.09, 0.39] | -0.04 [-0.42, 0.18] |
| ebm-td | 1.07 [0.63, 1.84] | 0.89 [0.51, 1.58] |
| ebm-all | 0.34 [0.08, 0.70] | 0.26 [-0.07, 0.53] |

### Paired differences in ticks_alive (arm_a - arm_b, paired bootstrap; the honest companion to G near the ceiling)

| a - b | linear | xor |
|---|---|---|
| ebm-td - tabular_q | 1230 [-187, 2552] | 752 [-569, 2010] |
| ebm-td - tabular_q_next | 194 [-1200, 1698] | -298 [-1645, 1046] |
| ebm-all - ebm-td | -2037 [-2858, -1215] | -1745 [-2832, -590] |
| ebm-dn-sign - ebm-dn | 818 [121, 1561] | 563 [-273, 1431] |
| ebm-dn-critic - ebm-dn-greedy | 330 [-132, 944] | -58 [-543, 552] |
| tabular_q_next - tabular_q | 1036 [-77, 2175] | 1050 [100, 2003] |

## Confirmatory tests P1-P5 (prereg; linear world unless stated)

**P1 (ceiling)**: bar G(ebm-all) >= 0.75 with CI lower bound > 0.5
  G = 0.54 [0.14, 1.15];  point >= 0.75: no;  lo > 0.5: no

**P2 / P5 (ΔG = G(a) - G(b), paired; frac = share of replicates with G(a) > G(b))**
  G(ebm-dn-greedy) - G(ebm-dn-sign) = -0.481 [-1.599, -0.075];  frac_a_gt_b = 0.005;  CI excludes 0: yes
  G(ebm-dn-sign) - G(ebm-dn-critic) = 0.291 [0.015, 0.958];  frac_a_gt_b = 0.980;  CI excludes 0: yes
  G(ebm-td) - G(ebm-dn-greedy) = 1.719 [0.878, 4.554];  frac_a_gt_b = 1.000;  CI excludes 0: yes
  P2 bar G(ebm-dn-greedy) > 0.4: G = -0.01 [-0.50, 0.19]

**P3 (replication)**: `ebm` inside EXP-01's CI [806, 1167] and ebm - ebm-nolearn CI includes 0
  EXP-01 (01_main_linear) ebm: 973 [806, 1167]
  this run (02_main_linear) ebm mean = 1102.0 (own CI [853, 1417]);  inside EXP-01 CI [806, 1167]: in
  linear: ebm - ebm-nolearn = -45 [-309, 257];  CI includes 0: yes
  xor: ebm - ebm-nolearn = 24 [-354, 505];  CI includes 0: yes

**P4 (xor)**: G_xor(ebm-dn-sign) < G_linear(ebm-dn-sign); ΔG = G_linear - G_xor, joined by seed
  G_linear = 0.471, G_xor = 0.327;  ΔG = 0.144 [-0.507, 1.393];  CI > 0: no;  denominators defined: linear True, xor True
