# qhslowifetch -- REPAIR PASS 3 measurement of GPT-6 Astra's floor findings (p3_20261105/codex_qhs_p3.txt B1, B2), 2026-11-04 local

Instrument: table_p3/probe62_p3.py (the in-tree probe after the pass-3 records fixes; AST-equal to table 3's probe62_frozen.py).
Baseline: r3_20261105/cpu_ppc_instr.c.fix4 (== GXEMUL-SEC).  Driver: ../table_p3.run.sh (frozen copy of table_p3.sh), scratch clone
/tmp/gxqhs4 under a clone-local sentinel; restored, cmp-clean against GXEMUL-SEC, rebuilt fresh, sentinel cleared (../table_p3_run.log).
ORDER: ../PRETABLE_P3.out mtime 22:55:29.64 local; the driver's first output, build_base.log, 22:55:48.55.

base 62/62.  All four variants 62/62 -- EXACTLY as PRETABLE_P3 predicted (Astra's derivation).  Each edit was LIVE (sessions_*/):
  B1a_c_meclr    T_me and T_ra_me end with msr 0x00000000 (base 0x00001000); no row reads msr
  B1b_a_meclr    T_ra_me ends with msr 0x00000000 (base 0x00001000)
  B1c_c_meset    T_step, T_cont, again and T_ra end with msr 0x00001000 (base 0x00000000)  (corrected 2026-11-05: this line
                 named only T_step; the repair-pass-3 adjudication's P3 asked, and all four transcripts were read)
  B2_ra_chktext  T_ra prints the checkstop line once (base: none); T ra has no chkstop row (its sibling T ra me has one)
So both findings are MEASURED escapes of the 62-row detector.  Whether each is inside the floor's bound is the adjudication's
question (B1: a state write inserted in an arm; B2: a sibling-parity gap -- the chkstop channel is rowed on T ra me but not T ra).
