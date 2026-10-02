HARNESS RECORD CORRECTIONS, part 02 -- find the text each correction replaces

FIRST line of your answer: `VERDICT: <s> of 18 still say it, <c> already corrected, <m> not found, <w> replacement does not fit`.
SECOND line: the token `AGY_HREC_02_ALIVE_1002`.  THIRD line: quote verbatim the first line of
`C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\CHECKPOINT.md`.

READ-ONLY, always: write no file, run nothing that changes a file, build nothing.  The tree under review is
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC` (git) at commit `7440e129`; read committed files
(`git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show 7440e129:<path>`), and ignore any other `src/` under the project root.

**Context.**  A review of this project's regression harness (its gate scripts, probes and checkers under `regress/`
and `tools/`) found comments and records that say something false or out of date.  Each such finding was ruled
RECORD: nothing is wrong with the code, the SENTENCE is wrong, and a replacement sentence was written.  The
corrections will be made in place, file by file, in later rounds.  Before a sentence can be replaced, somebody has to
find the text it replaces in the committed file and say whether it is still there.  That is this job.  The line
numbers in the dispositions are an older commit's (`db8b1a33`); the files have moved since, so find the text by what
it SAYS.

**For each disposition below, ONE line:**
`<key> | <path>:<first line>-<last line> at 7440e129 | STILL SAYS IT / ALREADY CORRECTED / NOT FOUND | CURRENT: "<the sentence or comment as it stands now, verbatim, at most 300 characters>" | FITS / DOES NOT FIT: <why>`
* `STILL SAYS IT`: the false or stale statement the disposition describes is present.  Quote it exactly as it stands
  (comment markers and all), so that a script can find it.
* `ALREADY CORRECTED`: the place now says what the replacement says, or the statement is gone.  Quote what stands there.
* `NOT FOUND`: you could not find the statement in the file the disposition names.  Say where you looked.
* `DOES NOT FIT`: the replacement sentence would itself be false at `7440e129`, or it describes another place.  Say
  which, with `path:line`.  Your agreement is not what is wanted: a replacement you cannot check against the source is
  `FITS: NOT CHECKED`, never a plain `FITS`.

End with `DENOMINATOR: <a> of 18 dispositions looked up in the committed file`.

**The dispositions** (key | the governing line, cut at 640 characters; where a replacement sentence is quoted in it,
that is the sentence that should stand):
1. regress23:F9 | regress23:F9 | RECORD | RIGHT | RECORD: "PTBR_VAL is 0x00000000aaaa1111 and the ptbr row expects it. apcb_flags is loaded from new_flags, and the flags row expects 0x00000000bbbb2222." | DROP: "the row expects already match the handler; the comments describe the old oracle" | regress/alpha_harness_probe.py:285,300-303,329,347-355; src/cpus/cpu_alpha_palcode.c:309
2. regress23:F10 | regress23:F10 | RECORD | RIGHT | RECORD: "The idle-path destination and flags rows compare with the literals 0 and 0x4. The -J sessions run the exit program and the alias program." | DROP: "the exit rows do have a -J session; the header over-claims that for the idle-path rows" | regress/arm_idle_probe.py:21,287-311,340
3. regress23:F11 | regress23:F11 | RECORD | RIGHT | RECORD: "When pclock is 0 the TCR write is ignored after a one-time fatal print. These rows require survived and quiet." | DROP: "the assertions already require survival; the death sentences describe the pre-fix host" | regress/sh_pclock_probe.py:228-248; src/devices/dev_sh4.c:2052-2054,2089-2095; src/core/debugmsg.c:384-390
4. regress24:F8 | regress24:F8 | RECORD | RIGHT | RECORD: "HEAD emits 57 rows." | DROP: "the score file under regress/artifacts was outside this read; the header is already false of the 57 row() sites" | regress/mk48_nvram_probe.py:10,186-324
5. regress24:F9 | regress24:F9 | RECORD | RIGHT | RECORD: "devsig reads 0x1ffc, 0x1ffd, 0x1ffe, and 0x1fff. 0x1ff9 is a survival row. 0x1ffa and 0x1ffb are not accessed." | DROP: "the four devsig expects already name 0x1ffc..0x1fff; the range in the table is the false part" | regress/mk48_nvram_probe.py:57,86,210-220,228-233,284
6. regress24:F10 | regress24:F10 | RECORD | RIGHT | RECORD: "cpu_mips.o lists cpu_mips_instr.c as a prerequisite in src/cpus/Makefile.skel." | DROP: "the prerequisite line is already in the makefile the header describes" | regress/gate_build.sh:11-13; src/cpus/Makefile.skel:146-148
7. regress24:F11 | regress24:F11 | RECORD | RIGHT | RECORD: "The fakes assert MARKER, BUDGET, STALLED, ABSENT, and EXITED. A timeout with no instruction records becomes ABSENT. No fake asserts BACKSTOP." | DROP: "the selftest checks already name those five tokens" | regress/gate_ab.sh:134,149-202; regress/lib.sh:287-315
8. hbundle_regress25:F2 | hbundle_regress25:F2 | RECORD | RIGHT | RECORD "The ftrc rows are mode-independent by architecture; discriminating counts static vector dictionary entries (len(set(v[4].values())) > 1) to ensure the table retains mode discriminators, but does not observe emulator execution or tripwire ftrc source changes." | regress/sh_rounding_probe.py:311-318
9. hbundle_regress25:F4 | hbundle_regress25:F4 | RECORD | RIGHT | RECORD "fcmpo, fmadds, fmsubs: no technical blocker -- these are a few dozen lines at the fidelity bar this file already ships (fnmadd/fnmsub were fixed in #344)." | regress/ppc_halt_probe.py:54-60, regress/ppc_halt_probe.py:270-276, src/cpus/cpu_ppc_instr.c:5263
10. hbundle_regress25:F6 | hbundle_regress25:F6 | RECORD | RIGHT | RECORD "2^32 and 0 are equal in their low 32 bits, so a comparator narrowed to int treats them as equal (failing to increment failures); the wide sentinel detects this narrowing, whereas the small sentinel (1 vs 2) cannot." | regress/diff_diskimage_parse.c:120-160
11. hbundle_regress26:F6 | hbundle_regress26:F6 | RECORD | RIGHT | RECORD "STRLEN_CONTROL requires only a positive cycle delta (_j[1] - _j[0] > 0); the subsequent reference band and end-address rows independently test that the delta is within [30000,60000] and that the walk ended at the NUL byte." | regress/arm_strlen_probe.py:230-246
12. hbundle_regress26:F7 | hbundle_regress26:F7 | RECORD | RIGHT | RECORD "Every row in this file goes through chk(), so unlike sh4_tmu (12 of 19) this sentinel covers the whole table." | regress/diff_rtc_range.c:147, regress/diff_sh4_tmu.c:530-536
13. hbundle_regress26:F8 | hbundle_regress26:F8 | RECORD | RIGHT | RECORD "The top of RAM is occupied -- a 12-byte halt stub at SP+32 with SP = R-4096, AND a PROM hook at R-8 written by arm_cpu_new(). CODE is planted low, at 0x8000." | regress/arm_bfx_width_probe.py:65-67, regress/arm_bfx_width_probe.py:114
14. hbundle_regress26:F9 | hbundle_regress26:F9 | RECORD | RIGHT | RECORD "NO SBFX ROW CHECKED PC AT ALL -- and s w32 is one whose expected failure value under the undefined shift is EXACTLY ZERO (like ubfx w32), which is precisely the case the pc control exists to disambiguate." | regress/arm_bfx_width_probe.py:265-272
15. hbundle_regress26:F10 | hbundle_regress26:F10 | draft said RECORD “…dev_sh4.c:731…jams the shift register at 8…” | should be RECORD “The caller resets sci_bits_outputed after sh4_sci_cmd returns. Moving that reset below the callee’s early returns leaves the counter at 8 after a decline; subsequent clocks increment it past 8, preventing later bytes in these sessions from reaching the command handler. R3 and X also detect this; J additionally checks a legal transfer after decline.” | `src/devices/dev_sh4.c:839,874,944–949`; `regress/sh4_sci_probe.py:173–193,285–291`. The counter does not remain at 8, and the reset is at line 949. Codex’s behavioral wordin...
16. hbundle_regress26:F11 | hbundle_regress26:F11 | draft said RECORD “dev_sh4.c:664 and :685. Match the full structured transfer format…” | should be RECORD “Match complete SCI transfer lines, including address and data. Decline lines contain ‘SCI: command byte’ and match neither ‘SCI: read’ nor ‘SCI: write’.” | The actual transfer messages are at `src/devices/dev_sh4.c:887–888,902–903`; declines are at `:837–838,870–873`. Lines 664 and 685 concern DMA. Codex’s replacement avoids the false coordinates. | confidence high
17. hbundle_regress26:F12 | hbundle_regress26:F12 | RECORD | RIGHT | RECORD "Clock every byte in seq through one session. Returns (started, alive, transfers, declines)." | regress/sh4_sci_probe.py:133-145
18. hbundle_regress27:F6 | hbundle_regress27:F6 | draft said RECORD “…for ceil.w and floor.w, non-zero FCSR.RM ensures directed modes differ from inherited modes.” | should be RECORD “Inheriting FCSR.RM=0 agrees with round.w’s forced nearest-even mode, but need not agree with ceil.w or floor.w. Each discriminating row chooses a nonzero FCSR.RM and input that produce a different inherited result.” | Nonzero alone is insufficient: RP=2 matches ceil’s forced mode; RM=3 matches floor’s. The actual fixtures deliberately choose differing modes and inputs. `regress/mips_fixedmode_probe.py:76,120–128`; `src/cpus/cpu_mips_coproc.c:1678–1679,1692–1693,1706–1707`. Co...
