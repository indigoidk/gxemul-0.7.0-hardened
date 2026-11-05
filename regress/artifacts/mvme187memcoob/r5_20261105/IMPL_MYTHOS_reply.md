MYTHOSIMPLMEMC5

VERDICT: REPAIR 5 IMPLEMENTED. 148 -> 206 rows, base on the fix 206/206, CONTROL OK, zero discrepancies, gate diff confined to the memc block.

- Rows before and after: 148 -> 206 (58 new: R16 27, R17 16, R5 2, R7 2, R9 3, R12 3, R13 3, R15 2; 10 re-wanted lines/pc rows), exactly the section 4 list of `p4_20261105/CONS_MYTHOS_local.md:56-77`.
- Base result line (`r5_20261105/base206/probe_base206.out:211-216`): `MVME187_MEMC_RESULT=206/206`, `MVME187_MEMC_CONTROL=OK`, `MVME187_MEMC_SYMPTOM=ABSENT`, `MVME187_MEMC_RED=none`, `MVME187_MEMC_ASAN=0`, elapsed 0.5s.
- Discrepancies (got != want): none. Every want came from the ruling's derivation; no row was pinned to the binary.
- Clearance (`r5_20261105/CLEARANCE.txt`): cmp of build vs GXEMUL-SEC dev_mvme187.c exit 0; build/gxemul newer than the source, exit 0.
- Probe edits (`regress/mvme187_memc_probe.py`): parser `range(4, 16)` -> `range(4, 32)` at the msession loop (cpu_m88k.c:289 prints `r%-2i = 0x%08x`, so r16..r27 parse with the existing regex); R16 timeout=120; new sessions R16 (45 words) and R17 (21 words); tails on R5, R7, R9, R12, R13, R15 with the listed init registers; docstring updated to fifteen sessions plus a REPAIR 5 paragraph. Probe diff: 34 lines removed, 163 added.
- Gate (`regress/gate_arm.sh`) diff stat vs backup: 5 lines changed (5 removed / 5 added), all inside the mvme187memcoob block: 2084-2085 (rows run / correct 148 -> 206), 2088 (names line, verified byte-equal to the base run's 206 names in order), 2091-2092 (rows emitted / green 148 -> 206). `bash -n` parses. The block's prose comment still says "148 rows ... R3 to R15"; left untouched per the names-and-pins-only brief, flagged in IMPL_NOTE.md.
- Files touched: `regress/mvme187_memc_probe.py`, `regress/gate_arm.sh`; written `regress/artifacts/mvme187memcoob/r5_20261105/` (mvme187_memc_probe.py.pre_r5, gate_arm.sh.pre_r5, CLEARANCE.txt, IMPL_NOTE.md, gate_arm.sh.r5.diff, mvme187_memc_probe.py.r5.diff, base206/probe206_run.py, base206/probe_base206.out, base206/rownames206.txt). No src/ edit, no build, no git command.
- Not done here: the L-walking script, PRETABLE_5 and table 5 (section 4's "order of work" after the rows) remain for the next step.
