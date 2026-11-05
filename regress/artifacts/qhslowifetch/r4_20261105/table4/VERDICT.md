# qhslowifetch -- test-variant TABLE 4 verdict (repair 4, 69 rows), run 2026-11-04 local (-0600)

Instrument: table4/probe69_frozen.py.  Baseline: ../../r3_20261105/cpu_ppc_instr.c.fix4.  Driver: ../table4_qhs.run.sh (frozen copy),
scratch clone /tmp/gxqhs5 under a clone-local sentinel; restored, cmp-clean against GXEMUL-SEC, rebuilt fresh, sentinel cleared
(../table4_run.log).  ORDER: ../PRETABLE_4.out mtime 23:32:20.75 local; the driver's first output, build_base.log, 23:32:37.80.

LEGS: base 69/69 CONTROL=OK SYMPTOM=ABSENT; HEAD 37/69 SYMPTOM=PRESENT -- EXACTLY the predicted set (table 3's HEAD rows + the six
msr rows); /bin/true 32/69, an absent binary 22/69, /bin/false 23/69, each CONTROL=FAIL.

VARIANTS: 36.  26 red as predicted (the four repair-pass-3 variants on EXACTLY their named rows: B1a T_me_msr,T_ra_me_msr; B1b
T_ra_me_msr; B1c T_cont_msr,T_step_msr,again_msr,T_ra_msr; B2 T_ra_chkstop); 9 green, the predicted nine (D6, D9, D10, V4, V5, V6,
D11, V2, V3); V12 NOT PREDICTED (p3 ruling F4) -- it reddened T_ra_me_pc,T_ra_me_nonex here, the OPPOSITE leg from table 3
(T_ra_pc,T_ra_nonex,T_ra_addr), which is the ruling's point measured a second time.
ONE row-set prediction missed (D12 is still caught): D12 was predicted AT LEAST table 3's set (T_ra_nonex,T_ra_me_pc,T_ra_me_nonex) and
measured T_ra_pc,T_ra_nonex,T_ra_addr,T_ra_me_nonex (65/69): T_ra_me_pc stayed green.  D12 is build-dependent (PRETABLE_3.errata
item 1 said so and PRETABLE_4 did not carry the flag forward again -- PRETABLE_4.errata.md); across tables 2, 3 and 4 only
T_ra_nonex reddened every time.
Further catches on the new rows (not predicted, not defects): B1 reds the six msr rows (every -T session exits before `reg`); D1,
D2, D14, D15 and V7 red T_ra_chkstop (they send T ra's failure into the checkstop fallback).
