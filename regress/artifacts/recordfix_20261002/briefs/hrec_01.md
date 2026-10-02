HARNESS RECORD CORRECTIONS, part 01 -- find the text each correction replaces

FIRST line of your answer: `VERDICT: <s> of 18 still say it, <c> already corrected, <m> not found, <w> replacement does not fit`.
SECOND line: the token `AGY_HREC_01_ALIVE_1002`.  THIRD line: quote verbatim the first line of
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
1. hbundle_regress13:F9 | hbundle_regress13:F9 | draft said NEW LOW alphabndmid | should be RECORD under the existing retro correction, without a new alphabndmid ID | `RETRO:755` already records this exact erroneous two-row ITB/DTB claim and its correction. `regress/alpha_tbi_probe.py:532-533,552-555,571-574` confirms that the data observations leave `bnd mid` green under a correct DTB flush. Retain the draft replacement text. | confidence HIGH
2. hbundle_regress15:F7 | hbundle_regress15:F7 | draft said `NEW LOW rldicldisasmgap`, “five sessions discard the disassembly” | should be the same disposition with “four session calls discard the returned disassembly”; retain the proposed RECORD text | `regress/ppc_rldicl_probe.py:340,348,362,472` are the four calls: negative apparatus, PPC603, vacuity and candidate. | confidence high
3. hbundle_regress18:F6 | hbundle_regress18:F6 | draft said FILED-BY-PROSE asicoffsetkill | should be RECORD “The probe sweeps all 256 offsets and checks a post-sweep marker; the per-offset coverage gap has been addressed.” | `OUTSTANDING_BUGS.md:11359–11360` files the original uncovered-offset defect, not the stale header. `regress/asic_badaddr_probe.py:379–387` implements the sweep; `:109–130` retains the obsolete inventory and filing status. | confidence high
4. hbundle_regress18:F16 | hbundle_regress18:F16 | draft said FILED-BY-PROSE rtcgate | should be RECORD “diff_rtc_range.c directly includes the RTC device with stubs; covering narrowing does not require moving it into the timer core.” | `OUTSTANDING_BUGS.md:6759–6760` closes the missing-detector work; it does not file this stale explanation. Compare `regress/diff_timer.c:35–38` with `regress/diff_rtc_range.c:101`. | confidence high
5. hbundle_regress18:F18 | hbundle_regress18:F18 | draft said FILED-BY-PROSE fbtimercomments already covers this occurrence | should be EXTEND fbtimercomments to diff_timer.c; RECORD “This file compares both numeric strings and symbolic results.” | `OUTSTANDING_BUGS.md:22155–22161` records the copied false sentence in `diff_footbridge.c`, with the entry scoped to that file and `gate_offline.sh`. The additional occurrence is `regress/diff_timer.c:187–188`; symbolic comparisons appear at `:280,335,379,396`. This is a scope amendment to the existing records entry. | confidence high
6. regress21:F6 | regress21:F6 | RECORD | RIGHT | RECORD: "D7a and D7b run in this file, both through a big-endian config." | DROP: "the scored rows already run; only the header sentence is stale" | regress/sh4_bsc_width_probe.py:25,355,372
7. regress21:F7 | regress21:F7 | RECORD | RIGHT | RECORD: "A 1-byte access returns 0 from sh4_bsc16_report and breaks before sh4_bsc16_shift, so this row does not reach that helper's length guard." | DROP: "false comment; the row still checks the ignored-byte diagnostic" | regress/sh4_bsc_width_probe.py:247; src/devices/dev_sh4.c:1633-1641,1676-1679
8. regress21:F8 | regress21:F8 | RECORD | RIGHT | RECORD: "Unmasked 0xc003 sign-extends to 0xffffc003 and dumps 03c0ffff. The store is 0x89abc003." | DROP: "the scored masked expectation is already right" | regress/sh4_bsc_width_probe.py:205,219
9. regress21:F9 | regress21:F9 | RECORD | RIGHT | RECORD: "fadd toward +Inf/+Inf-opposite at m88k_rounding_probe.py:68-69 and flt toward +Inf at :96 also fail a missing 2-for-3 swap." | DROP: "those rows already fail the swap; the 'only defence' sentence is the defect" | regress/gate_m88k_rounding.sh:16; regress/m88k_rounding_probe.py:68-69,95-96
10. regress21:F10 | regress21:F10 | RECORD | RIGHT | RECORD: "Seven truncation rows (three SS and four SD). 25+7+8+6=46." | DROP: "the running denominator 80 already matches the tuple count" | regress/gate_m88k_rounding.sh:55; regress/m88k_rounding_probe.py:134-146,158-169,287-322
11. regress21:F11 | regress21:F11 | RECORD | RIGHT | RECORD: "Eight expected-HALT rows: resid50, resid127, resid11, resid50ind, resid50c, resid50ser, sfu1h, usfu1." | DROP: "the checks already name the eight; the comment under-counts them" | regress/gate_m88k_rounding.sh:329,357-373; regress/m88k_exc_probe.py:452
12. regress21:F12 | regress21:F12 | RECORD | RIGHT | RECORD: "On pmax the negative tiny result is fpu_subst_tiny after the subnormal encoder. The expected word remains 80000000." | DROP: "the expected word is already the HEAD result" | regress/mips_subnorm_probe.py:20,379; src/core/float_emul.c:645,663-677; src/cpus/cpu_mips_coproc.c:1137,1192-1197
13. regress22:F6 | regress22:F6 | RECORD | RIGHT | RECORD: "A wrong argument count prints usage and returns 2. SystemExit is re-raised, so SELFMUTANT_SETUP is not printed." | DROP: "usage plus exit 2 is already what the wrapper does" | regress/selfmutant.py:185-187,395-408
14. regress22:F7 | regress22:F7 | RECORD | RIGHT | RECORD: "a0 obs checks that a0 was read, so v0=C with a0=C scores 6/6. The line 399 note fires on that permitted pair." | DROP: "the six row predicates already implement presence-only a0" | regress/alpha_swpctx_v0_probe.py:35-36,80-87,397-399
15. regress22:F8 | regress22:F8 | RECORD | RIGHT | RECORD: "The first swpctx returns the initial context 0x10100. The second returns 0x1000000." | DROP: "v0 ctx already distinguishes the two values" | regress/alpha_swpctx_v0_probe.py:76-77; src/cpus/cpu_alpha.c:107; src/cpus/cpu_alpha_palcode.c:269,273
16. regress22:F9 | regress22:F9 | RECORD | RIGHT | RECORD: "A third swpctx still returns N when ctx=a0 is kept and the PCB loads are omitted, which is also what correct code returns." | DROP: "the proposed third call matches both the hole and the correct handler" | regress/alpha_swpctx_v0_probe.py:40-48; src/cpus/cpu_alpha_palcode.c:269,273
17. regress22:F10 | regress22:F10 | draft said RECORD “Writing SCIF SCR=0x40 or SSR=1 also asserts RXI through scif_reassert_interrupts.” | should be RECORD “RXI also asserts synchronously when guest writes leave SCR.RIE and SSR.DR both set and RXI was previously deasserted; for example, set SCR=0x40, then SSR=1.” | `src/devices/dev_sh4.c:550-554` requires both bits and the assertion transition; either register write recomputes the condition at `:2635-2638,2658-2663`. The unqualified “or” is false. | confidence high
18. regress22:F11 | regress22:F11 | RECORD | RIGHT | RECORD: "Eight of the first ten rows drive TXI. live stores to RAM and devsig reads IPRD." | DROP: "the row calls already separate those two" | regress/sh_iprbcd_probe.py:375
