## A. Grammar shape: entropy at each end (lower = more predictable, endings-like)

Indus 'start' = stored position 0, inferred to be the reading END (jar-sign end).

| corpus | start+0 | start+1 | start+2 | end-0 | end-1 | end-2 |
|---|---|---|---|---|---|---|
| Indus | 4.71 b · top5 59% | 6.63 b · top5 24% | 6.31 b · top5 27% | 7.02 b · top5 24% | 6.18 b · top5 35% | 6.37 b · top5 28% |
| Sanskrit, whole words | 6.37 b · top5 28% | 8.03 b · top5 10% | 7.24 b · top5 18% | 8.20 b · top5 12% | 7.44 b · top5 15% | 7.76 b · top5 14% |
| Old Tamil, whole words | 5.47 b · top5 32% | 5.73 b · top5 29% | 6.44 b · top5 18% | 5.07 b · top5 46% | 6.39 b · top5 17% | 6.30 b · top5 22% |
| Chess openings | 2.34 b · top5 90% | 2.98 b · top5 83% | 3.30 b · top5 79% | 6.17 b · top5 24% | 5.48 b · top5 34% | 5.07 b · top5 40% |

Sanskrit, every word of ≥2 units: first-unit entropy 6.35 b, last-unit entropy 8.35 b

Old Tamil, every word of ≥2 units: first-unit entropy 5.64 b, last-unit entropy 5.01 b

## B. Sign groups by shared neighbours

Tamil check, 114 aksharas into 12 groups: purity by same vowel sign 0.32 vs random 0.28±0.02 (2.4 sd)
Tamil check, 114 aksharas into 12 groups: purity by same consonant 0.42 vs random 0.21±0.02 (11.8 sd)

Indus, 94 signs seen ≥15 times, 12 groups (largest first). Pos = share at stored start / at stored end:

G1  n=36  cohesion 0.07 · {'middle': 35, 'start': 1} · 220(233) 240(187) 520(167) 33(151) 235(145) 233(126) 590(117) 3(101) 803(88) 798(86) 176(83) 415(83) 760(77) 806(74) …
G2  n=11  cohesion 0.07 · {'middle': 11} · 2(505) 32(224) 60(165) 1(140) 741(140) 31(131) 61(46) 125(44) 892(36) 745(17) 13(15)
G3  n=8   cohesion 0.11 · {'middle': 8} · 705(99) 255(61) 706(53) 503(33) 440(29) 416(27) 832(19) 495(15)
G4  n=8   cohesion 0.08 · {'middle': 6, 'end': 2} · 820(152) 840(60) 692(46) 575(43) 350(31) 455(28) 413(19) 632(16)
G5  n=6   cohesion 0.12 · {'middle': 5, 'end': 1} · 817(118) 550(68) 388(30) 384(17) 555(17) 335(16)
G6  n=5   cohesion 0.09 · {'middle': 3, 'end': 1, 'start': 1} · 920(100) 100(75) 900(59) 690(46) 527(44)
G7  n=5   cohesion 0.14 · {'middle': 2, 'start': 2, 'end': 1} · 390(169) 861(155) 405(49) 407(46) 700(34)
G8  n=4   cohesion 0.12 · {'start': 3, 'middle': 1} · 740(953) 156(36) 154(31) 158(18)
G9  n=4   cohesion 0.08 · {'middle': 3, 'start': 1} · 90(85) 368(70) 595(27) 480(15)
G10 n=3   cohesion 0.13 · {'middle': 2, 'start': 1} · 226(25) 850(20) 165(17)
G11 n=2   cohesion 0.11 · {'start': 2} · 151(60) 617(44)
G12 n=2   cohesion 0.17 · {'start': 2} · 400(204) 621(19)

How far the groups just restate position: purity by start/middle/end 0.87 vs random 0.81±0.01

Nearest neighbours (cosine) of the 10 commonest signs:
   740: 154 0.12, 158 0.10, 151 0.10, 690 0.09, 415 0.09
     2: 60 0.15, 741 0.14, 1 0.13, 235 0.12, 13 0.11
   220: 233 0.23, 235 0.17, 803 0.14, 231 0.14, 240 0.14
    32: 233 0.13, 495 0.11, 140 0.08, 31 0.08, 705 0.08
   400: 621 0.17, 460 0.10, 151 0.09, 1 0.09, 61 0.07
   240: 235 0.31, 236 0.27, 233 0.27, 231 0.22, 798 0.18
   390: 405 0.30, 407 0.17, 700 0.15, 900 0.12, 413 0.09
   520: 923 0.22, 760 0.16, 555 0.13, 752 0.13, 151 0.11
    60: 2 0.15, 617 0.13, 742 0.12, 55 0.11, 455 0.11
   861: 390 0.09, 817 0.08, 700 0.08, 920 0.08, 255 0.07
