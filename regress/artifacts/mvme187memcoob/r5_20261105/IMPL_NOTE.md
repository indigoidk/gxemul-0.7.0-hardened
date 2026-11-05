MYTHOSIMPLMEMC5 -- mvme187memcoob REPAIR 5, implementation note (2026-11-05)
model: claude-mythos-5-1 (Mythos 5.1; configured id, serving model may differ)
ruling implemented: p4_20261105/CONS_MYTHOS_local.md section 4 (row list), carrying section 3 (the closed enumeration).

RESULT: 148 -> 206 rows.  Base on the fix (base206/probe_base206.out):
  MVME187_MEMC_RESULT=206/206
  MVME187_MEMC_CONTROL=OK
  MVME187_MEMC_SYMPTOM=ABSENT
  MVME187_MEMC_RED=none
  MVME187_MEMC_ASAN=0
  elapsed 0.5s
DISCREPANCIES (got != want on the fix): none.  Every want below is the ruling's derivation (section 4); no row was pinned to the binary.
CLEARANCE: CLEARANCE.txt -- build/src/devices/dev_mvme187.c identical to GXEMUL-SEC's (cmp exit 0); build/gxemul newer than it (exit 0).

FILES TOUCHED
  regress/mvme187_memc_probe.py       (backup: mvme187_memc_probe.py.pre_r5; diff: mvme187_memc_probe.py.r5.diff, 34 lines removed, 163 added)
  regress/gate_arm.sh                 (backup: gate_arm.sh.pre_r5; diff: gate_arm.sh.r5.diff)
  this directory (CLEARANCE.txt, IMPL_NOTE.md, base206/probe206_run.py, base206/probe_base206.out, base206/rownames206.txt, the two diffs)
  NOT touched: src/, the build tree, git.

GATE DIFF STAT (gate_arm.sh.pre_r5 -> gate_arm.sh): 5 lines changed, 5 removed / 5 added, all inside the mvme187memcoob block:
  2084,2085c2084,2085   rows run 148 -> 206; rows correct "148" -> "206"   (the RESULT=N/N pins)
  2088c2088             the row-names line: 206 names, the base run's order, verified equal to base206/rownames206.txt
  2091,2092c2091,2092   rows emitted "148" -> "206"; rows green "148" -> "206"
  `bash -n gate_arm.sh` parses.  The block's prose comment (lines 2063-2075: "148 rows ... thirteen multi-access sessions -- R3 to R15")
  was left as it was, per the brief (names list and pins only); it is now stale by 58 rows and two sessions.

PROBE EDITS (section 4, "probe edit first")
  :223  msession parses r2 and r4..r31 (`range(4, 16)` -> `range(4, 32)`); cpu_m88k.c:289 prints every GPR as "r%-2i = 0x%08x", so
        the existing `\br%d\s*=` regex reads r16..r27 unchanged.  R16 is given timeout=120.
  docstring: "fifteen: R3 to R17", a REPAIR 5 paragraph naming the phase product and the tails.

NEW ROWS (58), each with its session and the section-4 item it implements
R16 NEW (27 rows; section 4 "R16 NEW", phases 00 -> 10 -> 11; 45 instructions exactly as listed, init r5=0xff r6=0x07 r9=0xffffffff,
  SENT in r2, r4, r7, r8, r10..r27):
  R16 session exit0 | R16 cnf line "memconf write 0x7 (controller 0) ignored, not modelled (once) ]" | R16 def line "unimplemented write
  to offset 0x1c (controller 1): 0xffffffff (once) ]" | R16 lines "2" | R16 pc 0x100b4 |
  R16 100 r2 0x80 | R16 00 r4 0x80 | R16 104 r7 0x1 | R16 04 r8 0x1 | R16 08 r10 0x3 | R16 108 r11 0x3            (phase 00; F5, F6)
  R16 100b r12 0x80 | R16 00b r13 0x80 | R16 104b r14 0x1 | R16 04b r15 0x1 | R16 08b r16 0x3 | R16 108b r17 0x3 (phase 10; F4 #13, F2/F5 #26-#27)
  R16 100c r18 0x80 | R16 00c r19 0x80 | R16 104c r20 0x1 | R16 04c r21 0x1 | R16 08c r22 0x3 | R16 108c r23 0x3 (phase 11; F6, F10)
  R16 83 r24 0x0 (#40: F8 complement of 0x7c, F10 phase 11) | R16 10c r25 0x0 | R16 1c r26 0x0 (#44: F9, F3) | R16 08d r27 0x3 (#43 readback)
R17 NEW (16 rows; section 4 "R17 NEW", default first at 0xf3, phase 01; 21 instructions exactly as listed, init r5=0xff r6=0x07
  r9=0xffffffff, SENT in r2, r4, r7, r8, r10..r16):
  R17 session exit0 | R17 def line "unimplemented read from offset 0xf3 (controller 0) (once) ]" (family B, F8 #1) | R17 cnf line
  "memconf write 0x7 (controller 0) ignored, not modelled (once) ]" (#18: F1, F4, F10 phase 01) | R17 lines "2" | R17 pc 0x10054 |
  R17 f3 r2 0x0 | R17 10c r4 0x0 | R17 100 r7 0x80 | R17 00 r8 0x80 | R17 104 r10 0x1 | R17 04 r11 0x1 (F6, D set) | R17 08 r12 0x3
  (family C) | R17 108 r13 0x3 | R17 7c r14 0x0 (#17) | R17 7d r15 0x0 (#20: F3) | R17 08b r16 0x3 (#19 readback)
R5 EXTENDED (2 rows; appended ST_B(10,3,0x08), LD_BU(11,3,0x08); init + r10=0x07, r11=SENT):
  R5 cnf line "memconf write 0x7 (controller 0) ignored, not modelled (once) ]" (F4 tail, F10 `if (D) M = 1`) | R5 08b r11 0x3
  re-wanted: R5 lines "2", R5 pc 0x10020
R7 EXTENDED (2 rows; appended ST_B(0,3,0x08), LD_BU(6,3,0x10c), LD_BU(7,3,0x108); init + r6, r7 SENT):
  R7 10c r6 0x0 (F3) | R7 108b r7 0x3 (F1 second store readback)
  re-wanted: R7 pc 0x10018 (lines stays 2)
R9 EXTENDED (3 rows; appended LD_BU(8,3,0x10c), ST_B(0,3,0x08), LD_BU(9,3,0x08); init + r8, r9 SENT):
  R9 def line "unimplemented read from offset 0xc (controller 1) (once) ]" (F2, F7) | R9 10c r8 0x0 | R9 08b r9 0x3
  re-wanted: R9 lines "2", R9 pc 0x10024 (R9 no wide unchanged)
R12 EXTENDED (3 rows; LD_BU(13,3,0x08) inserted after LD_BU(4,3,0x04); appended ST_B(0,3,0x108), LD_BU(14,3,0x0c), LD_BU(15,3,0x08);
  init + r13, r14, r15 SENT):
  R12 m08 r13 0x3 (family C) | R12 0cb r14 0x0 (family A, default) | R12 08b r15 0x3 (family A memconf second store; F5 tail)
  re-wanted: R12 pc 0x10054 (lines stays 2)
R13 EXTENDED (3 rows; appended ST_B(7,3,0x08), LD_BU(8,3,0x08), LD_BU(9,3,0x10c); init + r7=0x07, r8, r9 SENT):
  R13 cnf line "memconf write 0x7 (controller 0) ignored, not modelled (once) ]" (F10 W c1 word -> first memconf store) | R13 08b r8 0x3
  | R13 10c r9 0x0 (family A second default access)
  re-wanted: R13 lines "2", R13 pc 0x1001c
R15 EXTENDED (2 rows; appended ST_W(6,3,0x1c), ST_B(0,3,0x108), LD_BU(7,3,0x08); init + r6=0xffffffff, r7 SENT):
  R15 def line "unimplemented write to offset 0x1c (controller 0): 0xffffffff (once) ]" (first default write 0x1c, M set) | R15 08 r7 0x3
  re-wanted: R15 lines "2", R15 pc 0x10018
Count: 27 + 16 + 2 + 2 + 3 + 3 + 3 + 2 = 58 new, 10 re-wanted (R5 lines/pc, R7 pc, R9 lines/pc, R12 pc, R13 lines/pc, R15 lines/pc); 148 -> 206.
All row names <= 16 characters and unique (asserted by row(); the longest new name is "R16 100b r12", 12 characters).

NOT DONE HERE (section 4's "order of work"): the L-walking script / PRETABLE_5 and table 5 (the test-variant run) belong to the
next step; this run delivers only the detector rows and the gate pins.
