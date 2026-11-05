# qhslowifetch -- the rung-3 witness, measured 2026-11-04 01:09-01:10 (before any edit)

No fix exists yet: the design ruling is Fable's and is HELD (owner, 2026-11-04 ~00:4x "hold fable"; ~01:0x "keep going ... on the 5
oldest bugs").  This record is the reproduction step only, measured by the main loop (Opus 5.5).

**Instrument.**  `regress/ppc_ifetch_probe.py`, run as the frozen copy `probe_frozen.py` (md5 3826ecfb4816, equal to the source at run
time; `RUN.log`).  Machine: `-E pmppc`, UNMODIFIED in-tree (Artesyn PM/PPC, PPC750, 32 MB), a four-byte `ori r0,r0,0` loaded raw at 0x2000.
`-T` (halt on a non-existent memory access) is a command-line option of the same unmodified binary, not a change to the machine.

| run | binary | RESULT | CONTROL | SYMPTOM | red rows |
|---|---|---|---|---|---|
| `prefix_head.out` | the scratch clone /tmp/gx579 rebuilt with HEAD `ebe5af82`'s `cpu_ppc_instr.c`; `cpu_dyntrans.c`, `memory_rw.c`, `memory_ppc.c`, `core/memory.c`, `cpu_ppc.c`, `machine_pmppc.c` each checked `== HEAD` (`RUN.log`) | 11/17 | OK | PRESENT | the six `-T` rows |
| `prefix_build.out` | `build/gxemul` (HEAD plus the tree's six uncommitted product files; on this path only cpu_ppc_instr.c, whose diff is the three #579 X(llsc) hunks; part 1 (cpu_ppc_instr.c against SEC) CLEAN, part 2 FRESH) | 11/17 | OK | PRESENT | the six `-T` rows |
| `null.out` | `/bin/true` | 8/17 | FAIL | ABSENT | -- (the five exit-0 session rows and the three absent-text rows pass a non-emulator; neg apparatus fails) |
| `nobin.out` | a missing path | 3/17 | FAIL | ABSENT | -- |

The two `-T` transcripts (`prefix_head_sessions/T_cont.txt`, `T_step.txt`) end with
`memory READ: from non-existant paddr=0x02040000 len=4 pc=0x02040000` then `PPC to_be_translated(): read failed: TODO` and exit status 1;
under `step` the run loop's own pre-read for the disassembly first prints `XXX_run_instr(): could not read the instruction` and carries on,
and the translator's read then fails.  The clone was restored afterwards: `cmp` clean against SEC, rebuilt, binary newer, sentinel removed.

**Facts the ruling should weigh (measured unless marked READ):**

1. **The ordinary ISI route does NOT reach the exit.**  IR on, PC in a reset-BAT gap (0x20000000): the ISI is raised (READ, not measured: from the dyntrans PC lookup, cpu_dyntrans.c:670-680; the transcript's instr=4 is FLAG_INSTR, which both callers pass) (`[ memory_ppc: exception! ... ]`, `[ PPC Exception 0x4; pc=0x20000000 ]`), SRR0 = 0x20000000, and execution
   resumes at 0x400, where the zero word stops the CPU -- under `continue` (the `isi` rows) and under `step` (a smoke run on build/gxemul at 01:06; its output is preserved as `TRANSCRIPT_EXCERPT_isi_step.txt`, copied from the session transcript).
   This agrees with the bug-review answers of Astra ("an ordinary cold branch to an unmapped virtual page faults before reaching this
   slow-fetch site") and Grok, and it REFUTES the witness-brief answer's prediction (Grok, panel_20261103_111229_next5_qhslowifetch_witness/grok.txt:5) that `continue` reaches the exit after the ISI.  The bug-review brief's title (next5_panels/qhslowifetch/CODEX.md:47: "ends the emulator process after the ISI exception has already been raised") and the filing's reach note (ledger state_note: "memory_ppc.c:314-326 has already raised the ISI") are therefore not the measured route.
2. **The route that does reach it: `-T` and a real-mode fetch past the end of RAM plus the 256 KB slack above it, where accesses are silent** (0x02040000 on 32 MB, the first address core/memory.c:605 does not pass silently):
   `memory_rw` returns failure with no PowerPC exception, and the translator ends the process where `-T` asked for a halt.  Without `-T`
   the same fetch reads zeros and the CPU stops on the zero word (the `noT` rows, alive).
3. **Not established here:** a device whose access function fails an instruction-width read (a producer with no `-T`); IR-on fetches
   whose translation succeeds onto non-existent memory; 64-bit CPUs (bareppc/testppc PPC970); PPC603-class CPUs (exception 0x10, vector 0x1000).

**Owed when the design is ruled:** the post-fix rows (the PC after the `-T` halt -- MEASURED since by an Opus measuring seat, `_scratchpad/opus_qhs/answer.md`: the draft's bare return ends at 0x02040004 under `step` and 0x02048140 under `continue`, a park at 0x02040000; SRR0 keeps its sentinel under both, since that route raises no exception), the gate wiring, and the kill table.  The `-T` session rows and the absent-text rows are design-independent and are the
witness proper: the same script must go green on the fix.
