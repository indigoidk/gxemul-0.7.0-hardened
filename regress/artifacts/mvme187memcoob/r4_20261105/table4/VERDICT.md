# mvme187memcoob -- test-variant TABLE 4 verdict (repair 4, 148 rows), run 2026-11-04 local (-0600)

Instrument: table4/probe148_frozen.py.  Baseline: ../../det_20261104/dev_mvme187.c.fix2.  Driver: ../table4_memc.run.sh (frozen copy),
scratch clone /tmp/gxmemc5 under a clone-local sentinel; restored, cmp-clean against GXEMUL-SEC, rebuilt fresh, sentinel cleared
(../table4_run.log).  ORDER: ../PRETABLE_4.out mtime 23:36:24.05 local; the driver's first output, build_base.log, 23:36:57.29.

LEGS: base 148/148 CONTROL=OK SYMPTOM=ABSENT; HEAD 33/148 SYMPTOM=PRESENT; /bin/true 25/148, an absent binary 4/148, /bin/false
5/148, each CONTROL=FAIL.

VARIANTS: 112, ALL RED.  111 as PRETABLE_4 predicted: table 3's 63 red; the pass-3 seats' 33 in-bound families each red on the
repair-4 row named for it; the ruling's B1-B6 (15 cases) each red on the row named -- M_B3_chipid on R12_00_r2, R12_100_r10,
R12_w00_r6 and M_B3_chiprev on R12_04_r4, R12_104_r11, so served AND stays caught after change 3 (the ruling's freshness check).
ONE prediction missed, in the safe direction: G_2_dlen1 (ruled OUTSIDE the bound; no row added; predicted GREEN) reddened
R13_line_text and R13_lines -- R13's first default access is a WORD store, which G_2's byte-width gate silences.  Incidental, not
claimed (PRETABLE_4.errata.md).
