HARNESS RECORD CORRECTIONS, part 03 -- find the text each correction replaces

FIRST line of your answer: `VERDICT: <s> of 18 still say it, <c> already corrected, <m> not found, <w> replacement does not fit`.
SECOND line: the token `AGY_HREC_03_ALIVE_1002`.  THIRD line: quote verbatim the first line of
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
1. hbundle_regress27:F7 | hbundle_regress27:F7 | RECORD | RIGHT | RECORD "Guarded write rows D1/D2 use bits in 25..8 to produce distinct as-is, masked, and no-store readbacks; D3 exercises bits in 7..0 against narrowed guards, and device readbacks mask with 0x00ffffff." | regress/luna_intmask_probe.py:11-17, regress/luna_intmask_probe.py:188, 231
2. hbundle_regress27:F8 | hbundle_regress27:F8 | RECORD | RIGHT | RECORD "Post-fix detector for alphapfnoffset: the page-table walk now preserves within-page offset at src/cpus/memory_alpha.c:186; expected rows pass on HEAD." | regress/alpha_pfnoffset_probe.py:11-14, src/cpus/memory_alpha.c:186
3. hbundle_regress27:F9 | hbundle_regress27:F9 | RECORD | RIGHT | RECORD "dev_lca.c:119,140 implement per-instance warning latches and return without exit(1); the committed build survives the interrupt and passes." | regress/lca_irqstub_uart_probe.py:18-20, 43-46, src/devices/dev_lca.c:115-145
4. hbundle_regress27:F10 | hbundle_regress27:F10 | RECORD | RIGHT | RECORD "Historical note: lines 181-189 originally claimed the session repeatedly entered the assert callback; as explained at :195-231, edge-triggering enters it once regardless of latching." | regress/lca_irqstub_uart_probe.py:181-189, 195-231
5. hbundle_regress27:F11 | hbundle_regress27:F11 | RECORD | RIGHT | RECORD "The DISC classification includes 7 negative controls in CAUSE_ROWS that verify non-raising of exception flags (yielding identical values before and after #330), contrary to :32 defining DISC as values that flip with the fix." | regress/gate_ppc.sh:32-33, 205, regress/ppc_rounding_probe.py:372-385, 1232
6. hbundle_regress27:F12 | hbundle_regress27:F12 | draft said RECORD “…missing completion tokens skip…” | should be RECORD “Absence of PPC_CONV_RESULT= invokes gate_skip, preserving earlier failures. With a result present, missing control or mode-readback tokens fail their assertions; PPC_CONV_CONTROL=DEAD also fails. FPSCR writes are verified in four separate sessions, once per rounding mode.” | `regress/gate_ppc.sh:162–185`; `regress/lib.sh:137–144`; `regress/ppc_rounding_probe.py:676–715`. The skip condition tests one specific result marker. Codex’s narrower replacement is supported. | confidence high
7. hbundle_regress28:F10 | hbundle_regress28:F10 | RECORD | RIGHT | RECORD "In THE ANNOUNCE GRID, direction text is marked R for READ len2, READ len4, and WRITE len4, but their checks only match width/value/offset substrings without asserting 'read from' or 'write to' (which are rowed only for len1)." | regress/pcc2_default_probe.py:63-67, 224-235
8. hbundle_regress28:F11 | hbundle_regress28:F11 | RECORD | RIGHT | RECORD "In CONTRACT: the rows are lin_b not src and lin_b is fg (requiring FG, not an inequality); restoring exit(1) terminates the LIN_B session only, not controls in earlier independent sessions." | regress/sgi_re_randompixel_probe.py:22-29, 207-250
9. hbundle_regress28:F13 | hbundle_regress28:F13 | RECORD | RIGHT | RECORD "check(\"a 401-char '[' run is released, not held (HOLD_MAX must stay sane)\", tail, \"\")" | regress/selftest_absorb.py:156-157
10. hbundle_regress28:F14 | hbundle_regress28:F14 | RECORD | RIGHT | RECORD "and the shipped detector is blind to it because its four defect rows (P2 s4/s5, P4 t5/t6) observe DRQ and the ring." | regress/wdc_altoffset_sig_probe.py:259, regress/wdc_altoffset_probe.py:377, 379, 389, 391
11. hbundle_regress29:F6 | hbundle_regress29:F6 | draft said DROP “the flag overclaim is sh4rtcflags” | should be RECORD, extending retro sh4:F2: “The timer generates neither CMF nor OVF. OVF is guest-writable: writing 0x04 stores it.” | `OUTSTANDING_BUGS.md:8534-8538` files missing timer functionality and **repeats** the false premise; it does not file its correction. `src/devices/dev_sh4.c:2376-2381` establishes guest-writable OVF. `retro:106` already assigns the corresponding records correction; extend it to `regress/sh4_rtcsr_probe.py:34-38` and the queue sentence. | confidence HIGH
12. hbundle_regress30:F9 | hbundle_regress30:F9 | draft said DROP “filed as ctorabortclass” | should be RECORD “Both ip19 and ip27 abort during z8530 construction through interrupt_handler_lookup; ip19’s later literal abort is not reached.” | `ctorabortclass` (`OUTSTANDING_BUGS.md:6997-7002,7033-7035`) files the actual construction failure, not correction of the contradictory “DIFFERENT MECHANISMS” claim at `regress/sgi_eaddr_probe.py:79-83`. The ordering is established by `src/machines/machine_sgi.c:170-174,394-396`, `src/devices/dev_z8530.c:212`, and `src/core/interrupt.c:190-198`. Preserve the records repair as the operative disposition. | confidence HIGH
13. hbundle_regress31:F11 | hbundle_regress31:F11 | draft said NEW LOW sctrcensus, with RECORD “No code reads reg[CMMU_SCTR]” | should be RECORD, extending retro devm8820x:F8: “SCTR has register and bit definitions; its value is stored and read back through the generic register accessor. No translation consumer reads SCTR.” | `src/devices/dev_m8820x.c:251,257-258,459-460` establishes guest readback and storage, making the proposed replacement overbroad. `retro:670` already supplies the precise correction, and `:702` includes the queue wording as a records rider. Extend that correction to `regress/repro_m8sarpurge.c:16`; do not mint another ID. | confidence ...
14. hbundle_regress32:F10 | hbundle_regress32:F10 | RECORD | RIGHT | RECORD "the NaN/cvt/cfc1 controls, which CANNOT flip by construction (trunc controls flip only under the trunc mutant)" | regress/selftest_mutation_295.sh:15-18,92-101,148-154
15. hbundle_regress32:F11 | hbundle_regress32:F11 | RECORD | RIGHT | RECORD "Both rigs run the rt=0x15 and BGEZ rows; pmax also runs rt=0x1e." | regress/gate_mips_rounding.sh:94-96,112-117; regress/mips_subnorm_probe.py:352-360
16. hbundle_regress32:F12 | hbundle_regress32:F12 | RECORD | RIGHT | RECORD "for round.w (which forces RN), the likeliest revert (cvt.w's FPU_RM_FROM_FCSR copy-pasted back) EQUALS correct code under the default FCSR.RM=0; for ceil.w/floor.w (which force RP/RM), discriminating rows set a non-zero mode to test directed behavior." | regress/gate_mips_rounding.sh:121-126
17. hbundle_regress32:F13 | hbundle_regress32:F13 | RECORD | RIGHT | RECORD "FLUSH_SUPER_LINE: DEFINED in m8820x.h:112, handled (#433 fold)" | regress/m8820x_sites_probe.py:158; src/devices/dev_m8820x.c:138-145; regress/gate_m88k_rounding.sh:264-266
18. hbundle_regress32:F14 | hbundle_regress32:F14 | RECORD | RIGHT | RECORD "fire == passes-1 for loop folds; memset expects fire=1 and device-bail expects fire=0" | regress/gate_mips_folds.sh:13-17; regress/mips_fold_probe.py:20-25,418-427
