# pvrrenderexit -- test-variant TABLE 3 (repair 3 with the Z-off twins, 128 rows), 2026-11-05 ~10:4x-10:19Z (04:19 local)

Driver `../table3_pvr.run.sh` (frozen copy of table3_pvr.sh), WSL scratch clone /tmp/gxpvr4 under a clone-local .MUTANT; restored,
cmp-clean against GXEMUL-SEC, rebuilt fresh, sentinel cleared (TABLE.log).  Instrument `probe128_frozen.py`, cmp-identical to the
in-tree probe, its md5 recorded in `../PRETABLE_3.out` and checked by the driver before the first leg (the frozen copy predates the
rewritten PRETABLE_3; every table output postdates it).  Scores: SCORES.txt; the driver's own prediction check: CHECK.txt.  No session
timed out in any leg (TIMEOUT_SESSIONS=none throughout).

* base 128/128 CONTROL=OK SYMPTOM=ABSENT; HEAD 60/128 SYMPTOM=PRESENT on the predicted red set; null media /bin/true 9/128, an absent
  binary 0/128, /bin/false 1/128 -- each CONTROL=FAIL.
* `TABLE3_CHECK hits=129 misses=1 not_predicted=4`: every variant RED except the five predicted EQUIVALENT (green as predicted), and
  every red set exactly as predicted but ONE:
  - MISS `Vt_swap_nov` (texturedline's v-coordinate swap deleted): predicted `texramp_l_end`, measured `texramp_l_end` AND
    `ztramp_l_end`.  The variant is DETECTED; the prediction was wrong by one row, and wrong against PRETABLE_3's OWN stated rule ("a
    Z-off twin reds exactly when its Z-on row does", line 7) -- Vt is not one of the listed exceptions, so its twin was owed in the
    prediction.  Recorded in ../PRETABLE_3.errata.md; PRETABLE_3.out itself is not rewritten.
  - NOT PREDICTED (undefined behaviour, as in table 2): Y2s, Y2t (`y < -1`) red their whole y-edges sessions and the Z-off twins;
    Y4s, Y4t (`y > ysize`) red `b out` in both the Z-on and Z-off sessions.
