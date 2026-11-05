# pvrrenderexit -- test-variant TABLE 5 (repair 5: the swap body's statement-deletion closure, its right end from above, a negative span start; 148 rows), 2026-11-05 06:29:53-06:40:24 local (TABLE.log)

Driver `../table5_pvr.run.sh` (frozen copy of table5_pvr.sh), WSL scratch clone /tmp/gxpvr8 under a clone-local .MUTANT; restored,
cmp-clean against GXEMUL-SEC and against `../dev_pvr.c.fix5`, rebuilt fresh, sentinel cleared (TABLE.log).  Instrument
`probe148_frozen.py` (md5 84fe7386d80139de97ec7026bbe23e7f), cmp-identical to the in-tree probe when PRETABLE_5 was written; its md5 is
recorded in `../PRETABLE_5.out` and the driver checked it before the first leg.  Order: the frozen probe 06:28:22, PRETABLE_5.out
06:29:02, the first result (MD5.txt) 06:29:50 -- every prediction predates every result.  Scores: SCORES.txt; the driver's own
prediction check: CHECK.txt.  196 legs (190 variants and six apparatus legs), no build failed, no session timed out in any leg.

* Legs: base 148/148 CONTROL=OK SYMPTOM=ABSENT; HEAD (the pre-fix exit) 70/148 SYMPTOM=PRESENT CONTROL=OK on its predicted red set;
  null media /bin/true 9/148, an absent binary 0/148, /bin/false 1/148 -- each CONTROL=FAIL; restored 148/148.
* `TABLE5_CHECK hits=192 misses=0 not_predicted=4`: all six legs and all 186 predicted variants exactly as PRETABLE_5 recorded them.
  - 156 variants RED, each on exactly its predicted set -- among them the three FLOOR cells on their repair-5 rows and nothing else
    (DTs_z, simpleline's `tmpf = z1;` deleted: `ramp8hi r end` + twin; N1s: `negx n start` + twin; B2t: `texnegx n start` + twin),
    every one of the 24 swap-body deletion cells on its Z-on row AND its Z-off twin, and simpleline's seven depth compounds on the
    ramp8hi rows (five at the right end, `z1 += z2` and `z1 *= z2` at the left).
  - 30 variants GREEN, each predicted green and named: EQUIVALENT M17, L1s, L1t, It, H65, B1t, B13t, B14t; clause-(e) DEBT B3s, B11s,
    B12t; and the 19 compound substitutions that are debt -- texturedline's four depth members (the pass-5 ruling predicted these red
    on ramp8hi, which is untextured; green, as the candidate run had already measured) and the 15 colour and UV members.
  - Derivations PRETABLE_5 added beyond the ruling, all held: X1s also reddens the two left-end rows (COVERHI and RAMP8 both start at
    441, so nothing draws (440,60)); At reddens the negative-start textured rows (u 0.75: texel (6,0), never stored) while As and V5s
    clamp to red on `negx n start`; M13, M26, M3, M15, M6 and M7 red the Z-off ramp8hi rows, Ps only the right end; B2s reddens
    `negx n start` with N1s.
  - NOT PREDICTED (undefined behaviour, as in tables 2-4): Y2s, Y2t red their whole y-edges sessions and the Z-off twins; Y4s, Y4t red
    `b out` in both sessions -- the same sets as before.
  - EXCLUDED, not built: the thirteen compound forms that divide by an operand that is zero on a drawn swapped span (named in
    PRETABLE_5).
