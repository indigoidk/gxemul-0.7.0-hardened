# pvrrenderexit -- test-variant TABLE 4 (repair 4: rule D2-F's half-pixel rows and the swap body's far end; 140 rows), 2026-11-05 05:27:20-05:36:16 local (TABLE.log)

Driver `../table4_pvr.run.sh` (frozen copy of table4_pvr.sh), WSL scratch clone /tmp/gxpvr6 under a clone-local .MUTANT; restored,
cmp-clean against GXEMUL-SEC and against `../dev_pvr.c.fix4`, rebuilt fresh, sentinel cleared (TABLE.log).  Instrument
`probe140_frozen.py` (md5 790b5ac327b255eb7ff83a560076ec9e), cmp-identical to the in-tree probe when the driver started; its md5 is
recorded in `../PRETABLE_4.out` and the driver checked it before the first leg.  Order: the frozen probe 05:26:24.98, PRETABLE_4.out
05:26:25.40, the first result (MD5.txt) 05:27:16 -- every prediction predates every result.  Scores: SCORES.txt; the driver's own
prediction check: CHECK.txt.  152 legs, no build failed, no session timed out in any leg (TIMEOUT_SESSIONS=none on all 152).

* Legs: base 140/140 CONTROL=OK SYMPTOM=ABSENT; HEAD (the pre-fix exit) 66/140 SYMPTOM=PRESENT CONTROL=OK on its predicted red set;
  null media /bin/true 9/140, an absent binary 0/140, /bin/false 1/140 -- each CONTROL=FAIL; restored 140/140.
* `TABLE4_CHECK hits=148 misses=0 not_predicted=4`: all six legs and all 142 predicted variants exactly as PRETABLE_4 recorded them.
  - 130 variants RED, each on exactly its predicted set -- among them codex pass 4's eleven FLOOR edits (B1s, B2s, B4s-B10t, B13s,
    B14s), every one on its repair-4 row(s) and nothing else, and every swap-body exchange deletion, whole (Zs Rs Gs Bs_swap_nob; Zt
    Ut Vt) or half (B4s-B10t), on BOTH twins (ramp8 / zramp8, texramp8 / ztramp8) -- the table-3 Vt miss does not recur.
  - 12 variants GREEN, each predicted green and named: EQUIVALENT M17, L1s, L1t, It, H65 (tables 1-3); EQUIVALENT by rule D2-F (iv),
    texturedline's integer ends: B1t, B2t, B13t, B14t; clause-(e) DEBT by rule D2-F (ii)/(iii): B3s (`x <= x2 + 0.25`), B11s and B12t
    (`vram_z[ofs] <= z + 0.25`), SAMPLED and not claimed.
  - The two derivations PRETABLE_4 added beyond the ruling held: B2s (`int x = x1 + 0.5`) reddened the four half-r rows besides `swap
    s start` / `zswap s start`; As (`x1 - 1`) and V5s (Z-off `x1 - 2`) left the ramp8 rows green (column 448's colour clamps to
    magenta), held by `ramp l end` / `zramp l end` as before.
  - NOT PREDICTED (undefined behaviour, as in tables 2 and 3): Y2s, Y2t (`y < -1`) red their whole y-edges sessions and the Z-off
    twins; Y4s, Y4t (`y > ysize`) red `b out` in both the Z-on and Z-off sessions -- the same sets table 3 measured.
