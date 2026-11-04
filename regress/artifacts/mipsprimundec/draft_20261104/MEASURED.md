# mipsprimundec -- the per-word exception table, HEAD and the fix DRAFT, measured 2026-11-04 02:4x by the main loop (Opus 5.5)

Measured after the Opus measuring seat for this question (`answer.md` here) applied and built the draft but stopped on a safety-classifier
refusal before measuring.  NO RULING: which exception each word owes is Fable's and is HELD.  The draft is the seat's `draft.diff` (the
pass-1 fix draft, `_scratchpad/cloud_fable_20261103/mipsprimundec/11_packet_fixdraft.md`, checked against the packet's AFTER image in
`check2.out`), applied with `patch` in the main loop's own clone `/tmp/gxmain_mpu` (a `cp -a` of `build/`; `cpu_mips_instr.c` checked CLEAN
against SEC first; 38 changed lines; removed afterwards).  `main_table.py`: one cold `-E testmips` session per word and CPU -- the word at
0xffffffff80020000 by `put w`, one `step`, then `reg` and `reg ,0`.

| word | HEAD (all three CPUs) | draft, R4400 (ISA III) | draft, R3000 (ISA I) | draft, 5KE (MIPS64, the default) |
|---|---|---|---|---|
| 0x74000000 jalx (0x1d) | CPU STOP, EPC 0 | RI (10) | RI (10) | RI (10) |
| 0x78000000 mdmx (0x1e) | CPU STOP | **CPU STOP** | **CPU STOP** | **CPU STOP** |
| 0xc8000000 lwc2 (0x32) | CPU STOP | CpU (11) CE=2 | CpU CE=2 | CpU CE=2 |
| 0xcc000000 lwc3 (0x33) | CPU STOP (R4400, R3000); PREF executes (5KE) | CpU CE=3 | CpU CE=3 | PREF executes (PC +4) |
| 0xd8000000 ldc2 (0x36) | CPU STOP | CpU CE=2 | CpU CE=2 | CpU CE=2 |
| 0xe8000000 swc2 (0x3a) | CPU STOP | CpU CE=2 | CpU CE=2 | CpU CE=2 |
| 0xec000000 swc3 (0x3b) | CPU STOP | CpU CE=3 | CpU CE=3 | RI (10) |
| 0xf8000000 sdc2 (0x3e) | CPU STOP | CpU CE=2 | CpU CE=2 | CpU CE=2 |
| jalx in the delay slot of `beq zero,zero` (R4400) | CPU STOP | RI, **BD set, EPC = the branch** | -- | -- |

Every trapping row has EPC = the word's PC and PC = the general vector (0xffffffff80000180; 0x80000080 on the R3000)
(`table_draft.out`, sessions under `main_sessions/`).  The witness probe on the draft: `probe_draft.out` **72/80**, CONTROL=OK,
SYMPTOM=PRESENT -- the eight red rows are exactly the 0x1e (`mdmx`) rows on both CPUs: the draft leaves the MDMX/LQ arm going to `bad`.

**Facts the ruling should weigh (measured unless marked):**
1. The draft does not cover 0x1e, which the filing names ("0x1e off R5900"); the witness keeps it red.
2. LDC2/SDC2 (MIPS II instructions) take CpU CE=2 on the ISA-I R3000, where the fork's own LDC1/SDC1 arm raises RI below ISA II
   (`cpu_mips_instr.c:5527-5531`, READ by the seat) -- the draft does not gate them by ISA level.
3. LWC3/SWC3 take CpU CE=3 on the R4400; the seat READ the R4000 manual's opcode table (`_scratchpad/mips_r4000.txt:5823`, a
   run-together line) as possibly marking 0x33 and 0x3b reserved on the R4000, which would mean RI -- UNSETTLED.
4. The delay-slot case is architecturally right on the draft (BD set, EPC = the branch).  The witness probe's cause regex would not
   parse a ` bd` line (the seat's READ note); `main_table.py` does.

**A reading seat's manual table agrees with these cells (a READ, cross-checked here against this MEASURED table; no ruling).**  `_scratchpad/cloud_fable_20261103/mipsprimundec/26_answer_bugreview_fixdraft_opus_b.txt` reads the local extracts as requiring: 0x1e off the R5900 -> RI at every level; LDC2/SDC2 on ISA I -> RI (MIPS II instructions; `mips-iv.txt:1372`, `:1415`; no LDCz in the R30xx manual); LWC3/SWC3 on ISA III -> RI (COP3 removed at MIPS III, `mips-iv.txt:1369`, `:1426`, asterisk key `:1447`; R4000 map `mips_r4000.txt:5823`/`:5834`). So the draft's measured cells R3000 ldc2/sdc2 (CpU CE=2), R4400 lwc3/swc3 (CpU CE=3) and mdmx (CPU STOP) are the ones that seat calls wrong; it predicted 72/80 for the draft on the witness probe before this measurement, which measured 72/80.  A second, independent manual reading is running.
