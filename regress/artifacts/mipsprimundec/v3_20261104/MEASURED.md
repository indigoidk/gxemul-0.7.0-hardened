# mipsprimundec -- the v3, measured 2026-11-04 04:38-04:4x (main loop, Opus 5.5)

No ruling: the design ruling is Fable's (`_scratchpad/cloud_fable_20261103/web/4_mipsprimundec.md`, waiting on Claude Code Cloud).  The
v3 is the step before it, per the owner's 2026-11-04 roster ("keep going with opus, grok, gemini web, ollama glm5.3, astra"): the
measured draft plus ONLY the changes the four share-findings reviews agree on.

**What v3 is.**  `apply_v3.py` (md5 3a045be5c268) applied to HEAD's `src/cpus/cpu_mips_instr.c` (the working tree equals HEAD for this
file): the draft (`../draft_20261104/draft.diff`) plus grok 4.7's two consensus edits (`_scratchpad/v3_consol/grok_mipsprimundec_v3consol.txt`,
section 2; its end line: 2 CONSENSUS 2 DISPUTED 5 UNSETTLED):
* **V3-1** LDC2/SDC2 split off the coprocessor-2 case: below ISA II they decode as Reserved Instruction, the gate LDC1/SDC1 already use
  (HEAD lines 5527-5530); from ISA II up they stay Coprocessor Unusable with CE = 2.  LWC2/SWC2 stay CE = 2 on every CPU.
* **V3-2** the non-R5900 half of `0x1e` (HEAD lines 5571-5575) decodes as Reserved Instruction instead of `goto bad`; the R5900 half
  (5565-5568) is unchanged.
* **Not carried:** the draft's unrelated hunk that deleted a blank line after `switch (s6) {`.
The resulting diff is `v3.diff`: 53 added and 8 deleted lines (`grep -c -E '^\+([^+]|$)'` and `'^-([^-]|$)'`).  *This line first
said "56 changed lines" -- the count of NON-BLANK changed lines (`grep -c '^[-+][^-+]'`), with no method named; GLM 5.3's v3 review
(F1) caught it.*

**Build.**  `run_v3.run-043801.sh` (a frozen copy of `run_v3.sh`) in the main loop's own WSL clone `/tmp/gxmain_mpu3` (`cp -a` of
`build/`; its `cpu_mips_instr.c` checked equal to SEC before the edit; a `.MUTANT` sentinel inside; the clone removed afterwards): make
rc 0, 0 warnings, binary newer than the edited source (`RUN_V3.log`, `build_v3.log`).  `build/` itself was only READ: its
`cpu_mips_instr.c` equals SEC and its binary is newer (`RUN_V3.log`, part 1 CLEAN, part 2 FRESH).

**Instruments (frozen copies, one per run, in this directory).**  `probe_frozen.py` (md5 5cae041d040b: the repo's
`regress/mips_primundec_probe.py`, which differs from the witness's frozen copy 54c5c7ebac52 only in a docstring correction; the 80 rows
are identical); `main_table_frozen.py` (md5 cd68c0f97b64, the draft run's per-word table); `main_table_cpus.py` (md5 9020c370890d, the
same table with two more CPUs, R6000 and 24KEc).

## Results (all MEASURED)

| run | file | result |
|---|---|---|
| witness probe on v3 | `probe_v3.out` | **80/80**, CONTROL OK, SYMPTOM ABSENT, RED none (the draft scored 72/80: its MDMX rows still stopped the CPU) |
| per-word table, v3 vs the draft | `table_v3.out` vs `../draft_20261104/table_draft.out` | exactly five cells change, all as V3-1/V3-2 intend: `mdmx` on R4400, R3000 and 5KE goes from STOP (`INT/0`, EPC 0) to `RI/10/ce=0` with EPC = the planted PC and PC = the general vector; R3000 `ldc2` and `sdc2` go from `CPU/11/ce=2` to `RI/10/ce=0`.  Every other cell is unchanged. |
| 24KEc (MIPS32, the MODE32 translator), v3 | `table_v3_cpus.out` | jalx RI; mdmx RI; lwc2, ldc2, swc2, sdc2 CpU CE=2; swc3 RI (ISA >= 4); lwc3 is PREF (PC + 4) -- every word but PREF raises an exception, vector 0x80000180 |
| 24KEc, HEAD (`build/gxemul`) | `table_head_cpus.out` | every word STOPs the CPU except lwc3 (PREF) |
| delay slot, v3 (R4400) | `table_v3.out` | JALX in a branch delay slot: `RI/10/ce=0/BD`, EPC = the branch |
| R6000, HEAD and v3 | `table_head_cpus.out`, `table_v3_cpus.out`, `table_cpus_v3_sessions/v3_R6000_*.txt` | **the machine is not constructed**: `Internal error: No initialization code for config0? cpu rev = 0x3`, so no row runs |
| Allegrex, HEAD (one LDC2 session) | the main loop's console, 04:4x | not constructed either: `Internal error: No initialization code for config0? cpu rev = 0x0` |

## What the measurements settle for the ruling

1. **Grok's MODE32 catch row is measured:** on the 24KEc, LDC2 raises CpU CE=2, so a v3 that set `x64` for LDC2/SDC2 (which the
   MODE32 tail rewrites to Reserved Instruction) would show here.
2. **Grok's `<= 2` catch row is NOT measurable, and that is a finding:** the only ISA II CPUs in `mips_cpu_types.h` are the R6000 and
   the Allegrex (READ: its 46 CPU entries, 46 of 46 parsed, list ISA level 2 for exactly those two), and neither can be constructed
   on `-E testmips`.  So the ISA II side of the new gate has no constructible CPU here:
   a gate written `isa_level <= 2` gives the same result as `< 2` on every CPU this tree can build.  The detector must disclose that
   cell as unobservable rather than claim it.
3. Two CPU types listed in `mips_cpu_types.h` end the process at construction.  That is a command-line choice, not a guest action;
   recorded as a candidate filing, not worked here.

**Not measured:** the R5900 arm (0x1e's R5900 half is unchanged); user mode; the pmax and arc rig machines; the wrong versions of the
fix (the test-variant table owed after the ruling).  The DISPUTED and UNSETTLED items in grok's consolidation (sections 3-4) are the
ruling's, unchanged.
