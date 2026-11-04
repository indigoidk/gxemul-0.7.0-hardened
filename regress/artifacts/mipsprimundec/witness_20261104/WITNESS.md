# mipsprimundec -- the rung-3 witness, measured 2026-11-04 01:14 (before any edit)

No fix exists: the design ruling (which words take Reserved Instruction and which Coprocessor Unusable, and with what CE) is
Fable's and is HELD (owner 2026-11-04 ~00:4x "hold fable"; ~01:0x "keep going ... on the 5 oldest bugs").  Measured by the main loop
(Opus 5.5).

**Instrument.**  `regress/mips_primundec_probe.py`, run as the frozen copy `probe_frozen.py` (md5 54c5c7ebac52, equal to the source at
run time; `RUN.log` 01:14:56).  Machine: `-E testmips`, UNMODIFIED in-tree, with `-C R4400` (ISA III, the 64-bit translator) and
`-C R3000` (ISA I, the MODE32 translator).  The binary is `build/gxemul`; the nine MIPS-path files in `build/` (`cpu_mips_instr.c`, `cpu_mips.c`, `cpu_dyntrans.c`, `memory_mips.c`, `memory_mips_v2p.c`, `memory_rw.c`, `machine_test.c`, `opcodes_mips.h`, `mips_cpu_types.h`) were checked `== HEAD` (RUN.log 01:14:56-57; HEAD ebe5af82 per the reflog), and cpu_mips_instr.c, cpu_mips.c and cpu_dyntrans.c were checked older than the binary (the driver tested only those three, although its RUN.log line says "every one of them").  The tree's only
uncommitted product deltas are in PowerPC, Alpha, SH, LCA and PCC2 files, none on this path.

| run | RESULT | CONTROL | SYMPTOM | red rows |
|---|---|---|---|---|
| `prefix_build.out` (build/gxemul, HEAD's MIPS path) | 16/80 | OK | PRESENT | all 64 witness rows: 8 words x 2 CPUs x {stop, exc, epc, pc} |
| `null.out` (`/bin/true`) | 16/80 | FAIL | ABSENT | -- (the 16 `stop` rows want absent text, which a non-emulator also gives) |
| `nobin.out` (a missing path) | 16/80 | FAIL | ABSENT | -- |

Every witness session (`prefix_build_sessions/<cpu>_<word>.txt`) steps the word, prints `UNIMPLEMENTED instruction` (0x1e first
prints `TODO: MDMX`, 0x33 `TODO: lwc3 not implemented yet`) and `All machines stopped`, with EPC = 0 and Cause = INT (exccode 0): no
exception is delivered.  The controls on the same CPUs show the apparatus does see one when it is raised: COP2 (0x48000000) gives
Coprocessor Unusable CE=2 with EPC = the planted PC and PC = the general vector (0xffffffff80000180 on the R4400, 0x80000080 on the
R3000), and LDC1 (0xd4000000) on the R3000 gives Reserved Instruction (exccode 10).  The null media score the same RESULT as the
pre-fix build and are rejected by CONTROL=FAIL; a gate pinning RESULT=80/80 by equality rejects all three.

**A fact for the ruling, measured in the first run (01:14:10, 17/80): that run's probe and outputs were overwritten and only its RUN.log count stands in this directory; the observation itself is preserved as `TRANSCRIPT_EXCERPT_5ke_pref.txt`, copied from the session transcript (01:14:27), and re-measured in `../draft_20261104/table_head.out` (5KE lwc3 = `pref`, PC +4):** that run's 64-bit leg used the DEFAULT testmips CPU, the MIPS64 5KE, and there 0xcc000000 executed as `pref 0x0,0(zr)` --
PC advanced, no exception.  On ISA IV and later opcode 0x33 is PREF, a legal prefetch, so a fix must leave it alone there (the
`HI6_LWC3` arm's TODO is reached only below ISA IV, as the filing says).  The probe's 64-bit leg was moved to the R4400 for that reason;
a PREF accept row on the 5KE is owed with the detector.

**Owed when the design is ruled:** the per-word ExcCode and CE rows (the `exc` rows here accept either 10 or 11), the R5900 arm, the
pmax and arc rig machines, user mode, a word in a branch delay slot, the gate wiring and the kill table.
