#!/usr/bin/env python3
"""Every committed DETECTOR under regress/ is RUN by a gate, or carries a dated exemption.

*** SIXTY-SIX DETECTOR ROWS DEFENDED NOTHING BETWEEN BATTERIES, AND NO GATE, CHECK OR
    LEDGER FIELD COULD SAY SO. ***  Named by a batched flagship regress pass on 2026-08-21,
    which sorted every detector escape in this project into three shapes and found that two
    had mechanical guards and the third -- "nobody runs it" -- had none.  Its own census said
    24 rows across two rounds.  MEASURED at HEAD 3d752b4 it is FOUR rounds and 66:

        pit8253_latch_probe.py   #439/#440   18 rows   run by NO gate
        sh4_bsc_width_probe.py   #441        13 rows   run by NO gate
        fbpending_drain_probe.py #442        11 rows, REPORT-ONLY by default (EXPECT_CAP<0)
        hpcmips_ctor_probe.py    #444        24 rows   run by NO gate  (+4 emitted in loops;
                                            its round's own record audits 26 emitted rows)

    THE MEASURE IS NAMED BECAUSE THE FIRST ONE WAS WRONG.  These are `row()` CALL SITES WITH
    A LITERAL LABEL, counted through `ast`, not grepped.  A first pass used `grep -o 'row("R'`
    and reported 12/11/7/26 = 56 -- it silently dropped every control row that is not
    R-prefixed (pit8253's A1 A2 C1 C2 E T, fbpending's K P T).  Same shape as the padded-column
    grep trap: a number that looks right and counts the wrong set.  A count nobody can re-derive
    is not a fact, which is what run.sh's own GATE_MANIFEST comment says.  Re-derive with:
        python -c "import ast,io;t=ast.parse(io.open(F).read());print(sum(1 for n in ast.walk(t)
        if isinstance(n,ast.Call) and getattr(n.func,'id','')=='row'))"

WHY THE EXISTING GUARDS DO NOT COVER THIS.  gate_hygiene's EXPECT_CONVERTED pin is a CENSUS
PIN: it asserts that a new probe carries the three #392 pty constructs and that the count
moved.  It is a good guard and it has fired four times -- but its subject is the probe's
SOURCE TEXT, never its EXECUTION.  All four files above satisfy that pin today.  The pin says
"this probe is well formed"; nothing said "this probe runs".

THE TWO TRAPS THIS INHERITS FROM gate_offline.sh's SM_COVERED/SC_COVERED, both re-read before
a line of this was written:

  1. A PREFIX IS NOT A NAME.  SM_COVERED's loop compares whole stems ([ "$_c" = "$stem" ])
     precisely because a substring match would accept a stem that is merely a prefix of
     another.  Hours before this file was written, check_fable_queue.py matched round ids by
     SUBSTRING and reported a round as queued when the only occurrence was a parenthetical
     cross-reference.  So this file matches FULL BASENAMES, and it decides "is it run?" from
     COMMAND POSITION rather than from a name appearing somewhere on a line.
     THE LIVE INSTANCE, not a hypothetical: gate_sh_rounding.sh:185 and eight lines of
     gate_hygiene.sh MENTION the unwired probes -- one of them in order to COMPLAIN that they
     are unwired.  A grep-for-the-name check scores all four WIRED and prints green over the
     entire defect it exists to catch.

  2. THE MANIFEST MUST NOT VERIFY THE LEDGER INSTEAD OF THE WORK.  gate_offline's F3 note
     records a pass-2 seat measuring BOTH directions green: delete a selfmutant_one call and
     leave SM_COVERED intact -> GREEN.  The structural answer here is that THERE IS NO
     COVERED LIST.  The manifest below carries ONLY the one fact a machine cannot derive --
     what CLASS an artefact is -- and the wiring is DERIVED, every run, from the gate scripts
     named in run.sh's GATES array.  The manifest cannot lie about wiring because it never
     states it, and the derivation PRINTS ITS EVIDENCE (gate_arm.sh:97) so the derivation is
     auditable rather than trusted.

WITNESS vs DETECTOR -- THE LINE, AND WHY IT IS NOT SYNTACTIC.

    A DETECTOR asserts the REPAIRED property: it is GREEN once the defect is gone.
    A WITNESS   asserts the PRE-FIX SYMPTOM:  it is RED   once the defect is gone.

That is sharp, but no grep can evaluate it.  MEASURED, so this is not a preference:

  * pit8253_latch_probe.py opens "Rung-3 cold-debugger WITNESS for pitlatch / pitclobber"
    -- and its rows assert the FIXED behaviour ("R1/R2 fail on the PRE-FIX build"), so by the
    line above it is a DETECTOR.  A self-label grep classifies it wrongly and, worse, then
    stops asking for a gate.
  * hpcmips_ctor_probe.py and sh4_bsc_width_probe.py are DETECTORS whose docstrings both say
    "The pre-fix WITNESS ... asserts the SYMPTOM" in prose.  A self-label grep classifies
    BOTH as witnesses -- and would then demand they never be gated, which is backwards.

So the class is DECLARED here, by a human, one line each.  The file's own summary line is
cross-checked as an ADVISORY (SELFLABEL), never as a failure, for the measured reason above.

WHY GATING A WITNESS IS A FAILURE, not merely pointless -- the tooth in the other direction,
which the reading seat's recommendation did not name.  A witness goes RED the day its fix
lands.  Wiring one into the battery converts a successful repair into a red gate with a
bookkeeping cause: the phantom-regression class this project already names, manufactured on
purpose.  So witness entries are checked for the ABSENCE of a gate call.

RETROACTIVE IN DOMAIN, GREEN AT INTRODUCTION.  check_boilerplate.py and check_bugfile_sync.py
are forward-only BY DATE because retro-failing an archive of hundreds of ledger rows gets the
rule switched off, and a disabled rule is worse than no rule.  That argument does not carry
here: the domain is a few dozen files in ONE FLAT DIRECTORY, enumerable in full today, and an
unwired probe has no date to be forward-only about.  A date cutoff would also grandfather the
four files this check exists for, permanently.  So nothing is grandfathered -- and the check is
still green on the day it lands, because each existing gap is written down as a DATED
EXEMPTION naming the round that owes it.  Debt that expires, not debt that disappears.

DATES ARE VALIDATED, NEVER GUESSED.  gate_offline.sh records a malformed exemption date that
never expired AND still satisfied the coverage check ("ieee_store:2026-8-1", 19 days past,
sorted as FUTURE).  Here a missing or malformed date is RED and names itself; it is never
silently treated as unexpired.

WHAT THIS CANNOT DO, said plainly so a green line is not read as more than it is:
  * it cannot tell whether a gated probe's rows are any good.  gate_offline's selfmutant lane
    and the vacuity taxonomy are what answer that; this answers only "does anything run it".
  * it cannot stop a DETECTOR being misfiled as tool to silence the requirement.  The
    filename tooth below refuses *_probe.py/*_witness.py in that class, which closes the
    cheapest form; a rename defeats it.  What is left is a written lie in a tracked file, and
    that is the same footing every manifest in this harness stands on.  Said, not hidden.

*** --selftest IS PART OF THE CHECK, NOT A CONVENIENCE. ***  A gate that cannot be shown to
go RED is the vacuity class this project names first, and "I ran the mutants once" is a
remembered grep -- the mrwstore2 shape, where a round's witness left no artefact and a later
row had to re-cost the work.  `--selftest` applies 18 mutants to COPIES in a temp directory
(never the repo) and asserts the exit status of each.  It is re-runnable by someone who was
not there, which is the only kind of measurement that survives.

Usage:  python check_probe_wiring.py [-v] [--regress DIR] [--today YYYY-MM-DD]
        python check_probe_wiring.py --selftest [-v]
Exit 0 and print PROBEWIRING_PASS, or exit 1 and print PROBEWIRING_FAIL.
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_REGRESS = os.path.normpath(os.path.join(HERE, "..", "..", "regress"))

#  Scripts that are part of the battery but are not in the GATES array: run.sh drives it and
#  lib.sh is sourced by every gate, so an invocation placed in either really would run.
ALWAYS = ("run.sh", "lib.sh")

#  A script argument is only a REPO probe if its directory is the regress dir.  gate_offline
#  runs `python3 "$ACDIR/selftest_absorb.py"` on a MUTATED COPY in the log dir -- counting
#  that as "the repo file is gated" would be the absorb-control mutant vouching for the
#  artefact it was built to attack.  Anything else is reported under IGNORED rather than
#  dropped, so a legitimate new spelling shows up as a line to read instead of a silent red.
HERE_DIRS = ("", ".", "$HERE", "${HERE}")

CLASS_DETECTOR = "detector"
CLASS_WITNESS = "witness"
CLASS_TOOL = "tool"
CLASS_RESEARCH = "research"
#  #471: a NON-SHIPPING artefact preserved as EVIDENCE, not as a test.  It exists so a
#  measurement can be re-run or audited; it is not owed a gate and must not be read as
#  an unwired detector.
#
#  *** THIS CLASS EXISTS BECAUSE THE OBVIOUS FIX WOULD HAVE BROKEN SOMETHING. ***  Making
#  the scan recursive immediately pulls in the instruments preserved beside a kill table
#  under regress/artifacts/.  A `_probe.py` suffix trips the MISFILED rule if they are
#  called tools, while calling them detectors demands a gate they should never have --
#  a file with no honest class.  A farmed seat found this and said plainly: land the
#  complete path-aware fix WITH this classification, or do not land it at all.
CLASSES = (CLASS_DETECTOR, CLASS_WITNESS, CLASS_TOOL, CLASS_RESEARCH)

#  ---------------------------------------------------------------------------------------
#  THE MANIFEST.  One line per python artefact in regress/.  The CLASS is the only thing a
#  machine cannot derive; the wiring is derived below and printed with its file:line.
#
#  Adding a probe means adding a line here, deliberately -- the same idiom as run.sh's
#  GATE_MANIFEST and gate_offline's SM_COVERED.  An unlisted file is RED, so a new detector
#  cannot arrive unnoticed, which is exactly how all four debts below arrived.
MANIFEST = {
    # -- detectors a gate RUNS today (the evidence is derived, not asserted here) ---------
    "sgi_re_rgb_probe.py":         (CLASS_DETECTOR, "#505 RGB GET/PUT byte container"),
    #  *** TWO OF THESE THREE CARRIED STALE HEAD SCORES until 2026-09-07: 7/9 and 5/6 were the
    #  counts BEFORE each round added the row its own fix review demanded (`swpctx flags`,
    #  `walk vpn`).  Corrected to the measured values. ***
    "alpha_harness_probe.py":     (CLASS_WITNESS,  "alphaswpctxptbr: swpctx overwrites apcb_ptbr with the flags word -- HEAD 7/10, fix 10/10"),
    "lca_confwidth_probe.py":     (CLASS_WITNESS,  "lcaconfwidth: the IOC_CONF kill names a value the guard accepts -- HEAD 4/6, fix 6/6"),
    "lca_confbus_probe.py":       (CLASS_WITNESS,  "lcaconfbus1kill: an ACCEPTED stq 0x1 to IOC_CONF arms the bus!=0 kill in lca_pci_conf -- HEAD 3/4, the RED row is the defect; post-fix green PENDING"),
    "lca_irqstub_probe.py":       (CLASS_WITNESS,  "lcairqstubkill: ONE guest store to the 8042 command port reaches lca_interrupt_assert and ends the host -- HEAD 3/6, the RED row is the defect; post-fix green MEASURED 11/11 (#516, killtable_20260909).  *** STILL CLASS_WITNESS, and that is now a JUDGMENT rather than a description: #516 grew it from 6 rows to 11, five of which exist only to defend the repair, so it is detector-shaped and NO GATE RUNS IT.  Kept as WITNESS because it is the witness of record in the ledger, and re-classing it would demand a gate home this round has not designed.  FILED to wiringcliff, which is the row for exactly that question -- not left as a silent third state."),
    "pcc2_c040_probe.py":         (CLASS_WITNESS,  "pcc2c040kill: ONE legal guest st.b of 0x04 to PCC2 GENCTL runs reassert_interrupts() in the same access and ends the host -- HEAD 3/4, the RED row is the defect; post-fix green PENDING"),
    "alpha_pfnoffset_probe.py":   (CLASS_WITNESS,  "alphapfnoffset: the page-table walk drops the within-page offset -- HEAD 5/7, fix 7/7"),
    #  A SECOND, INDEPENDENT path to the same two stubs, through a DIFFERENT device.  The row's
    #  witness of record is `lca_irqstub_probe.py' above (8042, shipped 7c2f8e4); this one is a
    #  supplement.  Not gated -- there is no fix yet, so a gate row would be permanently red.
    "lca_irqstub_uart_probe.py":  (CLASS_WITNESS,  "lcairqstubkill (SECOND PATH): three guest byte stores to the ns16550 (IER, MCR, THR) reach lca_interrupt_assert() on IRQ 4 -- HEAD 2/4, with an identical-sequence-against-RAM control green"),
    "alpha_swpctx_v0_probe.py":   (CLASS_WITNESS,  "alphaswpctxreg (#514): swpctx published the old context into a0, the register the ABI wrapper calls clobbered, leaving v0 untouched -- HEAD 3/5, fix 5/5 after the pass-2 repair added the `v0 pair' apparatus row"),
    #  agy built this one as the measurement seat; I re-ran it against build/ and it reproduced
    #  5/7 with the identical two failing rows.  Preserved as the round's evidence, and it is a
    #  WITNESS -- red on the committed build, green with the fix -- not a gated detector.
    "artifacts/alphatbinegsel/witness_agy_20260908/alphatbi_probe.asrun.py":
        (CLASS_WITNESS, "alphatbinegsel: ALPHA_TBIA(-2) and ALPHA_TBIAP(-1) both misdispatch to INVALIDATE_VADDR(a1=0), so only cached page zero is flushed -- committed 5/7, fixed 7/7, with a positive-selector control green on both"),
    #  #509.  It began as a 6-row witness and grew to 14 rows across two kill tables; it is
    #  classified WITNESS because nothing gates it, which is the same footing as the three
    #  above.  Wiring it is a separate decision and a separate round.
    "sgi_mte_fill_probe.py":      (CLASS_WITNESS,  "sgimtedepth4dead: `depth == 4' is unreachable so tiled MTE always took CI -- HEAD 10/14, fix 14/14"),
    #  #510.  The entry and the file are added to the INDEX in the same action, deliberately:
    #  this checker reads TRACKED files, so a manifest naming an untracked probe is a GHOST,
    #  and a tracked probe with no entry is UNCLASSIFIED.  Both are red, in opposite
    #  directions, and `2956c7e' shipped the second one -- see [[gateworktree]].
    "arm_bfx_width_probe.py":     (CLASS_WITNESS,  "armbfxwidth32: ubfx/sbfx build their mask with `1 << width' where width reaches 32 -- HEAD 9/11"),
    "arm_endian_probe.py":         (CLASS_DETECTOR, "ARM LDR rotation / endianness"),
    "arm_flags_probe.py":          (CLASS_DETECTOR, "ARM flag semantics"),
    "arm_fold_marker_probe.py":    (CLASS_DETECTOR, "instruction-combination markers"),
    "arm_idle_probe.py":           (CLASS_DETECTOR, "ARM idle detection"),
    "arm_memcpy_probe.py":         (CLASS_DETECTOR, "memcpy fold"),
    "arm_strlen_probe.py":         (CLASS_DETECTOR, "strlen fold"),
    "arm_writeback_probe.py":      (CLASS_DETECTOR, "LDR/STR writeback"),
    "diag_div_sweep.py":           (CLASS_DETECTOR, "class ratchet: drivable divisions"),
    "footbridge_sites_probe.py":   (CLASS_DETECTOR, "footbridge reachability sites"),
    "luna_intmask_probe.py":       (CLASS_DETECTOR, "#438 luna88k interrupt mask"),
    "m8820x_sites_probe.py":       (CLASS_DETECTOR, "m8820x CMMU sites"),
    "m88k_idle_probe.py":          (CLASS_DETECTOR, "m88k idle detection"),
    "m88k_rounding_probe.py":      (CLASS_DETECTOR, "m88k FP rounding"),
    "mips_fixedmode_probe.py":     (CLASS_DETECTOR, "MIPS FS / fixed mode"),
    "mips_fold_probe.py":          (CLASS_DETECTOR, "MIPS instruction folds"),
    "mips_rounding_probe.py":      (CLASS_DETECTOR, "MIPS FP rounding"),
    "mips_subnorm_probe.py":       (CLASS_DETECTOR, "MIPS subnormal decode/encode"),
    "ppc_halt_probe.py":           (CLASS_DETECTOR, "PPC halt path"),
    "ppc_rounding_probe.py":       (CLASS_DETECTOR, "PPC FP rounding"),
    "readiness_predicate_test.py": (CLASS_DETECTOR, "#392 readiness truth table"),
    "selftest_absorb.py":          (CLASS_DETECTOR, "drive_guest.split_stream selftest"),
    "selftest_budget.py":          (CLASS_DETECTOR, "wall-clock budget selftest"),
    "selftest_logdir.py":          (CLASS_DETECTOR, "#422 $LOGDIR honouring selftest"),
    "selftest_inactivity.py":      (CLASS_DETECTOR, "#467 inactivity-deadline selftest"),
    #  #492: the wdcflood latch census -- a GATED tool, run by gate_sh_rounding.sh.
    #  It replaced a grep -c equality that counted comment text as a guard.
    "wdc_latch_census.py":         (CLASS_DETECTOR, "wdc warned_ latch SET/READ census"),
    #  #493: the wdcaltoffset rung-3 witness.  A DURABLE, RE-RUNNABLE artifact for a
    #  live sev-high defect whose two prior measurements could NOT be re-run -- #481
    #  preserved 201 bytes of OUTPUT with no driver, and a later /tmp run was deleted
    #  by its own script.  Preserved as EVIDENCE: it drives a real guest and is not
    #  wired into a gate, so it is CLASS_RESEARCH rather than a detector owing one.
    #  #494 ships TWO committed detectors.  The second is not a duplicate of the
    #  first: the main probe observes DRQ and the input ring, and a mutant that
    #  guards only the destructive call -- leaving `cur_command` clobbered --
    #  passes all 18 of its rows.  The SIGNATURE probe reads the ATAPI signature
    #  through cyl_lo/cyl_hi on a CD-ROM rig and is the ONLY instrument that sees
    #  it.  Measured: m3 scored 0 red on the main detector and DEFECT PRESENT on
    #  the signature one.
    "wdc_altoffset_probe.py":
        (CLASS_DETECTOR, "#494 wdc alt-ctrl offset decode -- DRQ/ring channels"),
    "wdc_altoffset_sig_probe.py":
        (CLASS_DETECTOR, "#494 wdc alt-ctrl offset decode -- ATAPI signature channel"),
    #  The THIRD is not redundant either, and it was added to repair a MEASURED
    #  floor breach found on pass 2.  The other two use only 0x06, 0x02 and 0x04 at
    #  offset 1 -- all three with WDCTL_4BIT clear -- so every offset-1 row they
    #  carry sits in ONE bit-3 equivalence class, and a guard reading
    #  `!(idata & WDCTL_4BIT)` escaped BOTH at 36/36 and declined.  That bit is
    #  libata's steady-state ap->ctl, so a mask guard re-opens the defect at exactly
    #  the values the commonest driver writes.
    "wdc_altoffset_4bit_probe.py":
        (CLASS_DETECTOR, "#494 wdc alt-ctrl -- the WDCTL_4BIT mask-guard escape"),
    #  #495.  THE FLOOR FORCED THIS ONE TO BE A DETECTOR RATHER THAN EVIDENCE: the
    #  shipped 128-row offline detector scores ZERO failures with the defect LIVE,
    #  so vacuity-floor clause (a) is unsatisfiable from any existing row.  This is
    #  the only instrument that observes the defect at all, and it is COMPLEMENTARY
    #  to diff_wdc_identify.c rather than a replacement -- each catches mutants the
    #  other misses, measured.
    "sgi_re_width_probe.py":
        (CLASS_DETECTOR, "#497 sgi_re six-site width decline -- 35 rows, wired into gate_arm.sh"),
    "wdc_addtoinbuf_probe.py":
        (CLASS_DETECTOR, "#495 wdc ATAPI data-port write during DATA-IN -- rung-3"),

    #  m88kexcdeliver (#502) and lunaabsentcpu (#503), 2026-09-06: every .py these rounds preserved under
    #  regress/artifacts/ is EVIDENCE -- frozen instruments beside their kill tables, the frozen mutant
    #  generators and fix scripts, and the two measuring seats' own drivers.  Generated from this checker's
    #  own UNCLASSIFIED list; one line per file, deliberately, as the pcc2 block above does.  The SHIPPED
    #  detector m88k_exc_probe.py is the one entry here that is NOT evidence and is classified as a detector,
    #  because the checker's own header warns that a detector misfiled as anything else silences the
    #  requirement; its gate wiring is DERIVED below, not asserted here.
    #  lcairqstubkill (2026-09-08): a WITNESS ATTEMPT, and it did NOT fire.  It is classified as
    #  evidence rather than as a detector because that is what it is -- three controls green, the
    #  assertion never reached the stub, and the round records it as an ATTEMPT rather than as a
    #  negative result, because whether a debugger `put' reaches DEVICE_ACCESS(ns16550) at all is
    #  still open.  A file that pins nothing must not be wired into a gate: it would be a green
    #  row that means nothing, which is the vacuity this whole layer exists to refuse.
    #  Not a probe of the emulator at all: it exercises the SHIPPED regex of
    #  alpha_swpctx_v0_probe.py -- extracted from that file, not retyped -- against the three
    #  synthetic transcripts a pass-3 seat used to measure three parser escapes.  Evidence that
    #  the repair works, which is why it is preserved; it runs no emulator and gates nothing.
    #  The ORDER half of the same evidence: anchoring fixed a response's SHAPE and could not fix
    #  its ORDER, so a pass-4 seat reported two variants that still swept.  This exercises the
    #  shipped `response_after' against both, and additionally shows the OLD count rule passing
    #  them -- which is what makes it evidence rather than a green row.
    #  The FULL escape corpus: all four variants reported across passes 4 and 5, run against the
    #  shipped composed rule.  It exists because neither the positional nor the binding rule alone
    #  was sufficient -- each let the other's escapes through -- so a test of either alone would
    #  have been the green row that means nothing.
    "artifacts/alphaswpctxreg/full_corpus.asrun.py":
        (CLASS_RESEARCH, "alphaswpctxreg (#514) pass 5: all four reported escapes plus the genuine shape, against the SHIPPED composed rule -- 5/5, each rejection naming its own reason"),
    "artifacts/alphaswpctxreg/order_attack.asrun.py":
        (CLASS_RESEARCH, "alphaswpctxreg (#514) pass 4: the two ORDER variants (read moved before the step; first response replayed as the second) re-run against the shipped step-binding -- 3/3, both rejected, and the old count rule shown passing both"),
    "artifacts/alphaswpctxreg/attack_parser.asrun.py":
        (CLASS_RESEARCH, "alphaswpctxreg (#514) pass 3: the seat's three synthetic parser attacks re-run against the SHIPPED regex -- 5/5, all rejected, both genuine shapes still parsed"),
    #  #515 lcaconfbus1kill: four FROZEN copies of `lca_confbus_probe.py', one per kill table,
    #  preserved so each table's scores can be re-read against the exact instrument that produced
    #  them.  They are EVIDENCE, not detectors -- the live probe is `regress/lca_confbus_probe.py'.
    #  Table 1 used a stale instrument and is explicitly NOT cited; tables 2-4 are.
    "artifacts/lcaconfbus1kill/killtable_20260908/table1_preliminary/lca_confbus_probe.asrun.py":
        (CLASS_RESEARCH, "lcaconfbus1kill (#515) table 1: the PRELIMINARY instrument, 14 rows before two oracle repairs -- preserved for comparison and deliberately not cited as a score claim"),
    "artifacts/lcaconfbus1kill/killtable_20260908/table2_shipped/lca_confbus_probe.asrun.py":
        (CLASS_RESEARCH, "lcaconfbus1kill (#515) table 2: the 14-row instrument, 10 variants zero escapes -- superseded by table 3 once the ask-again added four rows"),
    "artifacts/lcaconfbus1kill/killtable_20260908/table3_shipped/lca_confbus_probe.asrun.py":
        (CLASS_RESEARCH, "lcaconfbus1kill (#515) table 3: the SHIPPED 18-row instrument, 13 variants zero escapes -- code-identical to the live probe (verified by stripping comments)"),
    "artifacts/lcaconfbus1kill/killtable_20260908/table4_targeted/lca_confbus_probe.asrun.py":
        (CLASS_RESEARCH, "lcaconfbus1kill (#515) table 4: the same 18-row instrument for the targeted run -- grok's M13_regconj plus the 18-row PRE-FIX baseline, so the round's before/after uses one instrument"),
    "artifacts/lcairqstubkill/lcairq_probe.asrun.py":
        (CLASS_RESEARCH, "lcairqstubkill: the as-run witness ATTEMPT, preserved as evidence -- it did NOT fire, and it is not a detector"),
    "artifacts/sgimtedepth4dead/repair_20260909/sgi_mte_fill_probe.REPAIRED.py":
        (CLASS_RESEARCH, "sgimtelabelcells (#509 follow-up, 2026-09-09/10): the REPAIRED 16-row instrument as the Opus seat delivered it, identical to the shipped regress/sgi_mte_fill_probe.py after the loop applied it (md5 348f5312); the measured copy"),
    "artifacts/sgimtedepth4dead/repair_20260909/sgi_mte_fill_probe.AS_MEASURED.py":
        (CLASS_RESEARCH, "sgimtelabelcells: the frozen copy the table actually ran (differs from REPAIRED only in a comment correction proved static and empirical, BASE_corrected.raw); evidence"),
    "artifacts/sgimtedepth4dead/repair_20260909/drivers/mk_repaired_probe.py":
        (CLASS_RESEARCH, "sgimtelabelcells: the script that produced the REPAIRED probe from the shipped 14-row one (two label rows, fill_at helper, contract text); provenance"),
    "artifacts/sgimtedepth4dead/repair_20260909/drivers/mk_table.py":
        (CLASS_RESEARCH, "sgimtelabelcells: the table generator -- READS every log after its sentinel, transcribes nothing; its verdict lines are negative-controlled (verdict_negative_control.out) after a first draft printed YES unconditionally"),
    "artifacts/sgimtedepth4dead/repair_20260909/drivers/op7b_mutate.py":
        (CLASS_RESEARCH, "sgimtelabelcells: mutator for M_tlbA, M_tlbAB and the nine preserved M1..M9 (killtable2_20260907 edits re-applied); scratch clone only"),
    "artifacts/pcc2c040kill/ctlq_20260909/pcc2_c040_probe.REPAIRED.py":
        (CLASS_RESEARCH, "pcc2c040ctlq (#512 follow-up, 2026-09-09): the REPAIRED 16-row instrument as the Opus seat delivered it -- identical to the shipped regress/pcc2_c040_probe.py after the loop applied it; preserved as the measured copy (md5 cbe1945c)"),
    "artifacts/pcc2c040kill/ctlq_20260909/mutate.py":
        (CLASS_RESEARCH, "pcc2c040ctlq: the mutator (M_widen guard-only widening `& PCC2_C040' -> `& (PCC2_C040 | 0x10)', plus M_return / M_latchinside / M_d1_noassert re-built from killtable_20260908); scratch clone only"),
    "artifacts/pcc2c040kill/ctlq_20260909/make_repaired.py":
        (CLASS_RESEARCH, "pcc2c040ctlq: the script that produced the REPAIRED probe from the shipped one (the one-string re-key plus the SAYS hoist); evidence of the edit's provenance"),
    "artifacts/sgimtedepth4dead/killtable3_20260909/tlb_reach_control.py":
        (CLASS_RESEARCH, "sgimtedepth4dead 7g-1 (2026-09-09): the Opus seat's guest-only TLB REACHABILITY CONTROL (unmodified -E sgi -e ip32) -- separates BASE / M_tlbA / M_tlbAB by the RGBA-vs-CI outcome at each of the three labels, which the shipped detector cannot; the positive control behind the FLOOR ruling.  Evidence, not a detector"),
    #  #516 (2026-09-09): every instrument and mutator preserved beside the lcairqstubkill kill tables.
    #  Seventeen files, each described from its own header; the gate refused the commit until they had a class.
    "artifacts/lcairqstubkill/killtable_20260909/frozen_lca_irqstub_probe.py":
        (CLASS_RESEARCH, "lcairqstubkill (#516) tables D/E: the frozen 11-row instrument (the measuring seat's probe5 plus the loop's `kbc attrib' widening) that TABLE_D.out and TABLE_E.out measured -- superseded by table G once the twelfth row (`uart live') landed; preserved as evidence"),
    "artifacts/lcairqstubkill/killtable_20260909/frozen_mut516d.py":
        (CLASS_RESEARCH, "lcairqstubkill (#516) tables D/E: the frozen mutant-apply script (one named mutant per run by find/replace; MUTANT-TEXT-NOT-FOUND is a FAIL, so each find-text is a presence pin)"),
    "artifacts/lcairqstubkill/killtable_20260909/G/frozen_lca_irqstub_probe.py":
        (CLASS_RESEARCH, "lcairqstubkill (#516) TABLE G: the frozen 12-row SHIPPED instrument, byte-identical to regress/lca_irqstub_probe.py at commit time -- base 12/12, 14 of 16 cells killed, 2 measured equivalent (TABLE_G.out)"),
    "artifacts/lcairqstubkill/killtable_20260909/G/frozen_mut516d.py":
        (CLASS_RESEARCH, "lcairqstubkill (#516) TABLE G: the frozen mutant-apply script for the 2 sites x 8 edits enumeration plus the composites"),
    "artifacts/lcairqstubkill/killtable_20260909/H/frozen_lca_irqstub_probe.py":
        (CLASS_RESEARCH, "lcairqstubkill (#516) TABLE H: the same instrument, cmp-identical to G's frozen copy (the ONE-INSTRUMENT check in kill516h.sh), for the two assignment-bit-swap cells -- M14 8/12, M15 11/12 (TABLE_H.out)"),
    "artifacts/lcairqstubkill/killtable_20260909/H/frozen_mut516h.py":
        (CLASS_RESEARCH, "lcairqstubkill (#516) TABLE H: the frozen mutant-apply script for M14_assert_assignswap and M15_deassert_assignswap"),
    "artifacts/lcairqstubkill/killtable_opus_20260909/lca_irqstub_probe2.py":
        (CLASS_RESEARCH, "lcairqstubkill (#516) measuring seat, instrument 2 of its sequence: eight rows whose `irq honest' matched a bare `Alpha has no', present in BOTH announce texts -- M5_assertdishonest escaped it 8/8; the measured instance of the repair-reproduces-the-breach shape"),
    "artifacts/lcairqstubkill/killtable_opus_20260909/lca_irqstub_probe3.py":
        (CLASS_RESEARCH, "lcairqstubkill (#516) measuring seat, instrument 3 of its sequence (eight rows): intermediate, superseded by probe5; preserved so the adopted instrument's derivation can be audited"),
    "artifacts/lcairqstubkill/killtable_opus_20260909/lca_irqstub_probe4.py":
        (CLASS_RESEARCH, "lcairqstubkill (#516) measuring seat, instrument 4 of its sequence (nine rows): intermediate, superseded by probe5; preserved as evidence"),
    "artifacts/lcairqstubkill/killtable_opus_20260909/lca_irqstub_probe5.py":
        (CLASS_RESEARCH, "lcairqstubkill (#516) measuring seat, the 11-row instrument ADOPTED as the deliverable (drain sig, deassert ann/honest, assert once/deassert once, `irq honest' anchored to its own site); the shipped probe is this plus three corrections and the twelfth row"),
    "artifacts/lcairqstubkill/killtable_opus_20260909b/frozen_shipped_probe.py":
        (CLASS_RESEARCH, "lcairqstubkill (#516) pass-2 repair, measuring seat: the 11-row probe as it stood at that moment, frozen for the M12 reachability table"),
    "artifacts/lcairqstubkill/killtable_opus_20260909b/frozen_narrow_operand_probe.py":
        (CLASS_RESEARCH, "lcairqstubkill (#516) pass-2 repair, measuring seat: a frozen 11-row variant used by its Q3 comparison (the `kbc attrib' operand question, mut516r.py); evidence, not a detector"),
    "artifacts/lcairqstubkill/killtable_opus_20260909b/lca_assertassert_probe.py":
        (CLASS_RESEARCH, "lcairqstubkill (#516) pass-2 repair, measuring seat: six-row EDGE TRACE showing a second ASSERT edge with no intervening deassert is reachable on unmodified alphabook1 by ordinary stepped guest stores (the ns16550 on IRQ 4) -- the reachability measurement behind M12's L2 grading"),
    "artifacts/lcairqstubkill/killtable_opus_20260909b/lca_irqstub_probe_REPAIR.py":
        (CLASS_RESEARCH, "lcairqstubkill (#516) pass-2 repair, measuring seat: the PROPOSED 12-row repair (a second assert edge from a different ISA line between [B] and [C]); the shipped twelfth row `uart live' is the loop's implementation of it"),
    "artifacts/lcairqstubkill/killtable_opus_20260909b/mut516q.py":
        (CLASS_RESEARCH, "lcairqstubkill (#516) pass-2 repair, measuring seat: mutator for the M12 family (assert-guard latch-bit swap); scratch clone only"),
    "artifacts/lcairqstubkill/killtable_opus_20260909b/mut516r.py":
        (CLASS_RESEARCH, "lcairqstubkill (#516) pass-2 repair, measuring seat: the Q3 mutators (the `kbc attrib' widening question); scratch clone only"),
    "artifacts/lcairqstubkill/killtable_opus_20260909b/mut516s.py":
        (CLASS_RESEARCH, "lcairqstubkill (#516) pass-2 repair, measuring seat: re-builds of the round's own mutants so the proposed repair probe could be shown to lose none of their kills; scratch clone only"),
    #  #518 lcabadval and #519 sgirandomcolour (2026-09-10): both rounds are HELD -- #518 on three mutants
    #  that still escape its 67-row instrument, #519 on two clause-(d) operand swaps the measuring seat
    #  built itself after every planned mutant had died.  The evidence commit lands their ARTIFACTS while
    #  the fixes and the live probes stay out of the tree, so every file below is CLASS_RESEARCH and none
    #  is wired to a gate.  When a round ships, its live probe gets its own detector entry; these frozen
    #  copies stay evidence forever, because their whole purpose is that a table's scores can be re-read
    #  against the exact instrument that produced them.
    #  lcaisalane's is a WITNESS as-run copy, red on HEAD by design and not a green row anyone may wire.
    "artifacts/lcabadval/killtable_20260910/lca_badval_probe.asrun.py":
        (CLASS_RESEARCH, "lcabadval (#518) table 1: the as-run 40-row instrument, the measuring seat's first table -- superseded by the repaired 58-row copy, kept so table 1's scores stay re-readable"),
    "artifacts/lcabadval/killtable_20260910/lca_badval_probe.asrun2.py":
        (CLASS_RESEARCH, "lcabadval (#518) table 1 continuation: the same instrument after the round-one repair, preserved separately because the scores either side of it are not comparable"),
    "artifacts/lcabadval/killtable_20260910/lca_badval_probe.REPAIRED58.asrun.py":
        (CLASS_RESEARCH, "lcabadval (#518) table 2: the 58-row instrument, the round-two repair -- six of its own mutants swept it and exposed two vacuous and two absent rows, which is what round three was for"),
    "artifacts/lcabadval/killtable_20260910/t3/lca_badval_probe.REPAIRED64.asrun.py":
        (CLASS_RESEARCH, "lcabadval (#518) table 3: the 64-row instrument (t3/SCORES3.txt, BASE 64/64) -- M43/M44/M45/M47 escaped it and became round four's rows"),
    "artifacts/lcabadval/killtable_20260910/t4/lca_badval_probe.REPAIRED67.asrun.py":
        (CLASS_RESEARCH, "lcabadval (#518) table 4: the FINAL 67-row instrument (t4/SCORES4.txt, BASE 67/67) -- three mutants STILL escape it (M43, M44, M47), which is why the round is held"),
    "artifacts/lcabadval/killtable_20260910/gen_table1.py":
        (CLASS_RESEARCH, "lcabadval (#518): the measuring seat's table-1 driver -- reads every log after its LCABADVAL_DONE sentinel and transcribes nothing"),
    "artifacts/lcabadval/killtable_20260910/mutate518.py":
        (CLASS_RESEARCH, "lcabadval (#518): the table-1 mutator, one named find/replace per mutant; MUTANT-TEXT-NOT-FOUND is a hard failure, so every edit doubles as a presence pin"),
    "artifacts/lcabadval/killtable_20260910/mutate518b.py":
        (CLASS_RESEARCH, "lcabadval (#518): the table-1 mutator's second generation, for the mutants added after the round-one repair"),
    "artifacts/lcabadval/killtable_20260910/summarize518.py":
        (CLASS_RESEARCH, "lcabadval (#518): the table-1 summariser -- reads scores out of the .raw logs rather than accepting any typed number"),

    # -- #520 alphatbinegsel -----------------------------------------------------------
    #  The SHIPPED detector.  It is CLASS_DETECTOR and it is EXEMPT below rather than
    #  wired, for a reason that is a fact about the battery and not a preference: NO GATE
    #  IN THIS TREE RUNS AN ALPHA MACHINE.  `gate_crossfamily.sh' is the only gate that
    #  mentions alpha at all and is therefore the named home; giving it one is a gate
    #  change owing its own negative controls, which is a harness round, not a rider on a
    #  CPU fix.  Filed to `wiringcliff', the row for exactly that question -- not left as
    #  a silent third state.
    # -- #521 mk48nvramkill ------------------------------------------------------------
    #  CLASS_WITNESS, and correctly ungated: it is RED on the committed build by design
    #  (15/47, all 32 kill rows failing), so a gate row would be permanently red until the
    #  fix ships.  It is also NOT yet the round's detector -- its `msg census' row asserts
    #  the DEFECT'S OWN SIGNATURE and is green only while the defect is present, so the
    #  probe cannot score 47/47 on any build.  A shipped detector must drop or invert that
    #  row first; until then this stays a witness of record.
    "artifacts/mk48nvramkill/opus_mk48_nvram_witness_20260910.py":
        (CLASS_WITNESS, "mk48nvramkill (#521): eight offsets inside the device's own 8192-byte registration reach a default: arm that calls exit(1) -- rung 3 on unmodified -E mvme88k -e mvme187, SIXTEEN cells driven (8 offsets x read/write), committed 15/47 with all 15 controls green, fixed 46/47"),
    # -- #521 mk48nvramkill -------------------------------------------------------------
    #  CLASS_DETECTOR, and EXEMPT below rather than wired.  It is a fast (0.4 s) single-leg
    #  instrument that runs green on the fix today, so unlike a witness it COULD be gated --
    #  what it lacks is a home: gate_m88k_rounding.sh is the only gate on this CPU family and
    #  it drives luna88k, not mvme88k/mvme187.  Giving it an mvme187 leg is a gate change
    #  owing its own negative controls, i.e. a harness round, not a rider on a device fix.
    #  Filed to `wiringcliff'.
    # -- ppcrldiclzero + siblings ------------------------------------------------------
    #  CLASS_WITNESS and correctly ungated: RED on the committed build by design (19/27),
    #  so a gate row would be permanently red until the fix ships.  It is also a FAMILY
    #  instrument rather than a single-defect one -- it already reds on ppcrldimimask and
    #  ppcrlwimiwidth, two further measured defects in the same handler family -- so its
    #  contract needs stating carefully before any part of it is promoted to a detector.
    "artifacts/ppcrldiclzero/opus_ppc_rldicl_witness_20260910.py":
        (CLASS_WITNESS, "ppcrldiclzero: X(rldicl) writes ZERO on every execution -- rung 3 on unmodified -E bareppc / testppc / macppc -e g5, 190 of 190 census cells wrong on the committed build and 0 of 190 under the one-character repair (committed 19/27, fix 24/27).  Also carries a SECOND channel (the record form reports EQ always, so control flow is corrupted too) and rows for the two sibling defects it found"),
    # -- #522 ppcrldiclzero -------------------------------------------------------------
    #  CLASS_DETECTOR, EXEMPT below rather than wired.  It runs green on the fix in 0.2 s and
    #  COULD be gated -- what it needs is a gate that instantiates a 64-bit PowerPC CPU, and
    #  the two PowerPC gates both drive a 32-bit part, selected explicitly in their probes.
    #  (A gate DOES construct 64-bit PowerPC CPUs -- gate 9 enumerates every machine subtype
    #  -- but that is a CONSTRUCTION check with no result oracle.  Recorded because I had the
    #  stronger, false version of this claim in three rows before a seat checked it.)
    "ppc_rldicl_probe.py":
        (CLASS_DETECTOR, "ppcrldiclzero (#522): 24 rows on unmodified -E bareppc.  A 190-cell (SH,MB) census, value rows at SH 0/8/32/63, a record-form CR0 row, a deliberately-vacuous cell showing where the vacuity boundary is, a negative-apparatus control asserting its own liveness oracle CAN go red, and a disassembler cross-check of every placed word.  BASE 24/24, null medium 16/24, EIGHT mutants 16-23/24, ZERO ESCAPES (killtable_20260910/t2/SCORES.txt)"),

    #  The frozen copies are the instruments as-run.  t1 is the 19-row form that pass 2
    #  escaped TWICE; t2 is the 24-row closure; t0 is an apparatus failure kept on purpose.
    "artifacts/ppcrldiclzero/killtable_20260910/t1/ppc_rldicl_probe.frozen.py":
        (CLASS_RESEARCH, "ppcrldiclzero (#522) table 1: the as-run 19-row instrument -- pass 2 escaped it TWICE at 19/19 (a shift-decode mutant it was blind to BY CONSTRUCTION, and a CR0 mutant that is the sibling handler's own shipping token)"),
    "artifacts/ppcrldiclzero/killtable_20260910/t2/ppc_rldicl_probe.frozen.py":
        (CLASS_RESEARCH, "ppcrldiclzero (#522) table 2: the CLOSING 24-row instrument, byte-identical to the shipped regress/ppc_rldicl_probe.py"),
    "artifacts/ppcrldiclzero/killtable_20260910/t0_apparatus_failure/ppc_rldicl_probe.frozen.py":
        (CLASS_RESEARCH, "ppcrldiclzero (#522) table 0: an APPARATUS FAILURE preserved rather than deleted -- the driver was derived by substitution from #521 and called THAT round's mutator, which replied `unknown mutant'.  The hard-fail refused rather than measuring an unmutated tree, but the table looked HALF-HEALTHY because both mutators define BASE and answered it identically.  No number from it is cited anywhere"),

    "artifacts/ppcrldiclzero/killtable_20260910/mutate.py":
        (CLASS_TOOL, "ppcrldiclzero (#522): the mutator, nine mutants including the two that escaped pass 2.  Written with an editor rather than generated, because building it through a shell heredoc ate a backslash level and turned every escape into a real newline -- the carrier's documented trap, with its documented remedy"),

    #  The measuring seat's own apparatus, preserved with its answer.  Its mutator and mine
    #  were written independently and produced the SAME figures, which is why the literals
    #  were then reused verbatim -- so the legs stay comparable across the two tables.
    "artifacts/ppcrldiclzero/pass2_20260910/opus_mutate.py":
        (CLASS_TOOL, "ppcrldiclzero (#522) pass 2: the measuring seat's INDEPENDENT mutator -- six legs in its own clone, and the source of M_SH5 / M_MB5 / M_CR0"),
    "artifacts/ppcrldiclzero/pass2_20260910/opus_probe_plus3.py":
        (CLASS_RESEARCH, "ppcrldiclzero (#522) pass 2: the candidate probe with the three repair rows, MEASURED by the seat at 24/24 base, 22/24 M_SH5, 23/24 M_CR0 before I applied them"),
    #  Named `*_probe.py' but it is a PATCHER, not a probe -- it edits the probe rather than
    #  asserting anything.  The checker's filename tooth is right to refuse `tool' here and I
    #  am not renaming a seat's preserved artifact to satisfy it; RESEARCH is the honest class
    #  for a script kept as evidence of how the candidate rows were produced.
    "artifacts/ppcrldiclzero/pass2_20260910/opus_patch_probe.py":
        (CLASS_RESEARCH, "ppcrldiclzero (#522) pass 2: the seat's PATCHER for the candidate rows -- despite the name it asserts nothing; kept as evidence of how opus_probe_plus3.py was produced"),
    "artifacts/ppcrldiclzero/pass2_20260910/t0_backslash_apparatus_failure/probe_plus3.BROKEN.py":
        (CLASS_RESEARCH, "ppcrldiclzero (#522) pass 2: THE SEAT'S OWN APPARATUS FAILURE, preserved rather than deleted -- a regex built through a non-raw string turned a backslash-b into a literal BACKSPACE, so the pattern matched nothing and failed a row on EVERY leg including BASE.  Two documented traps stacked into a confident wrong answer; the corrected run added a negative control so the regex cannot silently match nothing again"),
    "mk48_nvram_probe.py":
        (CLASS_DETECTOR, "mk48nvramkill (#521): 57 rows on unmodified -E mvme88k -e mvme187.  Sixteen kill cells (eight offsets x read/write), nine round-trip rows closing the survive-only class, a CSR rising-edge row for the control case's side effect, four device-signature controls in two encodings, and a negative-apparatus control that asserts its own liveness oracle CAN go red.  BASE 57/57, null medium 16/57, five mutants 16-56/57, ZERO ESCAPES (killtable_20260910/t3/SCORES.txt)"),

    #  The three FROZEN copies are the instruments as-run, one per table.  Evidence, not live
    #  detectors: t1 is the 47-row form whose M_ICSR escape opened the floor breach, t2 the
    #  48-row repair, t3 the 57-row closure.
    "artifacts/mk48nvramkill/killtable_20260910/t1/mk48_nvram_probe.frozen.py":
        (CLASS_RESEARCH, "mk48nvramkill (#521) table 1: the as-run 47-row instrument -- M_ICSR escaped it 47/47, which is the floor breach the round was repaired for"),
    "artifacts/mk48nvramkill/killtable_20260910/t2/mk48_nvram_probe.frozen.py":
        (CLASS_RESEARCH, "mk48nvramkill (#521) table 2: the as-run 48-row instrument after the csr-rise repair -- zero escapes, but pass 2 then found the SAME survive-only class on the eight accepted offsets"),
    "artifacts/mk48nvramkill/killtable_20260910/t3/mk48_nvram_probe.frozen.py":
        (CLASS_RESEARCH, "mk48nvramkill (#521) table 3: the CLOSING 57-row instrument, byte-identical to the shipped regress/mk48_nvram_probe.py"),

    "artifacts/mk48nvramkill/killtable_20260910/mutate.py":
        (CLASS_TOOL, "mk48nvramkill (#521): the mutator -- one named literal find/replace per mutant with MUTANT-TEXT-NOT-FOUND a hard failure.  ITS OWN PRESENCE PIN CAUGHT TWO MISTAKES: an ambiguous anchor matching twice, and an M_NULL that replaced a statement with a COMMENT so `goto ret' became the if-body and the leg measured a different mutant than the record claimed"),
    "alpha_tbi_probe.py":
        (CLASS_DETECTOR, "alphatbinegsel (#520): 15 rows closing the tbi selector guard's NINE axes -- the window's four sides, the interior, the negative selectors, a1 zero-vs-nonzero, a1 magnitude and a0 magnitude.  BASE 15/15, null medium 11/15, nine mutants 12-14/15 (killtable_20260910/t3/SCORES.txt); every accept row carries a measured kill, checked by tally_kills.py"),

    #  The three FROZEN copies are the instruments as-run, one per table.  They are
    #  evidence, not live detectors: a citation into the live probe decays the moment the
    #  probe grows, which is exactly what happened here -- it went from 7 rows to 15 and a
    #  comment citing it for "5/7" came to CONTRADICT its own artifact.
    "artifacts/alphatbinegsel/killtable_20260910/t1/alpha_tbi_probe.frozen.py":
        (CLASS_RESEARCH, "alphatbinegsel (#520) table 1: the as-run 10-row instrument -- M_D and M_E swept it, which is what the bound rows were added for"),
    "artifacts/alphatbinegsel/killtable_20260910/t2/alpha_tbi_probe.frozen.py":
        (CLASS_RESEARCH, "alphatbinegsel (#520) table 2: the as-run 13-row instrument (probe_HEAD.raw 10/13, probe_BASE.raw 13/13) -- superseded when the pass-2 panel found the cast-width axis unrowed"),
    "artifacts/alphatbinegsel/killtable_20260910/t3/alpha_tbi_probe.frozen.py":
        (CLASS_RESEARCH, "alphatbinegsel (#520) table 3: the CLOSING 15-row instrument, byte-identical to the shipped regress/alpha_tbi_probe.py -- one instrument for all eleven legs"),

    #  Kill-table drivers.  CLASS_TOOL: they mutate and score, they assert nothing about
    #  the emulator, and no gate should ever run them.
    "artifacts/alphatbinegsel/killtable_20260910/mutate.py":
        (CLASS_TOOL, "alphatbinegsel (#520): the mutator -- one named find/replace per mutant, with MUTANT-TEXT-NOT-FOUND a hard failure, so every edit doubles as a presence pin on the fix's own text"),
    "artifacts/alphatbinegsel/killtable_20260910/t1/mutate.asrun.py":
        (CLASS_TOOL, "alphatbinegsel (#520): the table-1 mutator as run"),
    "artifacts/alphatbinegsel/killtable_20260910/t2/mutate.asrun.py":
        (CLASS_TOOL, "alphatbinegsel (#520): the table-2 mutator as run"),
    "artifacts/alphatbinegsel/killtable_20260910/t3/mutate.asrun.py":
        (CLASS_TOOL, "alphatbinegsel (#520): the table-3 mutator as run, carrying M_G/M_H/M_I -- the cast-width and a1-magnitude mutants the pass-2 panel demanded"),
    "artifacts/alphatbinegsel/killtable_20260910/tally_kills.py":
        (CLASS_TOOL, "alphatbinegsel (#520): computes the kill count FROM the logs and exits non-zero if any accept row lacks one -- so `every accept row carries a measured kill' is a check rather than a claim"),
    "artifacts/lcabadval/killtable_20260910/t2/gen_table2.py":
        (CLASS_RESEARCH, "lcabadval (#518): the table-2 driver, the second measuring seat's own, in its own scratch clone with its own sentinel"),
    "artifacts/lcabadval/killtable_20260910/t2/mutate518_t2.py":
        (CLASS_RESEARCH, "lcabadval (#518): the table-2 mutator (M1..M24, and M43..M47 re-used by table 4)"),
    "artifacts/lcabadval/killtable_20260910/t2/summarize_t2.py":
        (CLASS_RESEARCH, "lcabadval (#518): the table-2 summariser"),
    "artifacts/lcabadval/killtable_20260910/t4/mut518x.py":
        (CLASS_RESEARCH, "lcabadval (#518) table 4: the mutator for M48_wen_perreg (PRETABLE 4's own prescribed two-bit mutant, which neither seat's mutator had implemented) and M49_def_narrow -- both killed, 66/67"),
    "artifacts/lcabadval/witness_20260909/lca_badval_probe.asrun.py":
        (CLASS_RESEARCH, "lcabadval (#518): the as-run RUNG-3 WITNESS, 14/20 on the committed build 74daefd and 20/20 on the fix -- evidence, red on HEAD by design; the live probe is uncommitted with its held fix"),
    "artifacts/lcabadval/witness_20260909/lca_badval_probe.D9unsplit.asrun.py":
        (CLASS_RESEARCH, "lcabadval (#518): the D9-unsplit variant, preserved because the 63/64 score the records cite was re-measured against THIS copy and not against the split one"),
    "artifacts/lcaisalane/witness_20260910/lca_isalane_probe.asrun.py":
        (CLASS_RESEARCH, "lcaisalane: the as-run RUNG-3 WITNESS, 13/16 on HEAD 1ce8296 across two runs -- a WITNESS, red by design, and its `ofs1 zero' oracle is additionally known to alias its own sentinel (both Agent seats, pass 1), so it must never be wired to a gate"),
    "artifacts/sgirandomcolour/killtable_20260910/sgi_re_colourdefault_probe.FROZEN.py":
        (CLASS_RESEARCH, "sgirandomcolour (#519) table 1: the FROZEN 14-row instrument the measuring seat ran, BASE 14/14 -- the copy every table-1 score is re-readable against"),
    "artifacts/sgirandomcolour/killtable_20260910/sgi_re_colourdefault_probe.REPAIRED19.OPUSFROZEN.py":
        (CLASS_RESEARCH, "sgirandomcolour (#519): the measuring seat's own frozen copy of the repaired 19-row instrument, on which it re-ran its two escapes and measured them STILL escaping at 19/19"),
    "artifacts/sgirandomcolour/killtable_20260910/mut519.py":
        (CLASS_RESEARCH, "sgirandomcolour (#519) table 1: the mutator for M1..M12 (M11 copies the pre-fix file wholesale as the null medium); its M1/M7/M12 find-strings quote the pre-bracket literal and will not apply to the current source, which the round records rather than silently repairs"),
    "artifacts/sgirandomcolour/killtable_20260910/mut519b.py":
        (CLASS_RESEARCH, "sgirandomcolour (#519): the measuring seat's own mutator, for the two clause-(d) operand swaps it built after every planned mutant had died -- M13_widthdecline and M14_lineardecline, both TOTAL ESCAPES"),
    "artifacts/sgirandomcolour/killtable_20260910/t2/mut519x.py":
        (CLASS_RESEARCH, "sgirandomcolour (#519) tables 2/2b/2c: the mutator for the vertex-qualified guards (M13_okorx, M14_okory), the shared-latch-bit escapes (M15_texrd, M18_sharedbit_tlba) and the two drop-case growth mutants (M16, M17)"),
    "artifacts/sgirandomcolour/killtable_20260910/t2/sgi_re_colourdefault_probe.REPAIRED16.asrun.py":
        (CLASS_RESEARCH, "sgirandomcolour (#519) table 2: the 16-row instrument -- M15_texrd escaped it 16/16, the predicted escape that motivated the latch-collision class closure"),
    "artifacts/sgirandomcolour/killtable_20260910/t2/sgi_re_colourdefault_probe.REPAIRED16b.asrun.py":
        (CLASS_RESEARCH, "sgirandomcolour (#519) table 2b: the same 16 rows re-frozen against the bracket-edited source, so BASE_final's 19/19 is attributable to a named baseline"),
    "artifacts/sgirandomcolour/killtable_20260910/t2/sgi_re_colourdefault_probe.REPAIRED19.asrun.py":
        (CLASS_RESEARCH, "sgirandomcolour (#519) table 2c: the 19-row instrument carrying the class closure -- M15_texrd and M18_sharedbit_tlba both die 18/19 to `allbits announce'"),
    "artifacts/sgirandomcolour/witness_20260910/sgi_re_colourdefault_probe.asrun.py":
        (CLASS_RESEARCH, "sgirandomcolour (#519): the as-run RUNG-3 WITNESS agy built as the independent-transport fallback while both Anthropic seats were walled -- 2/5 on HEAD, 5/5 on the fix; evidence, red on HEAD by design"),
    "artifacts/lunaabsentcpu/killtable/fix_lunaabs.py":
        (CLASS_RESEARCH, "lunaabsentcpu (#503) table 1: the frozen fix script the baseline was derived from, preserved as evidence"),
    "artifacts/lunaabsentcpu/killtable/luna_absentcpu_probe.frozen.py":
        (CLASS_RESEARCH, "lunaabsentcpu (#503) table 1: the frozen instrument the table ran, preserved as evidence"),
    "artifacts/lunaabsentcpu/killtable/mut_lunaabs.py":
        (CLASS_RESEARCH, "lunaabsentcpu (#503) table 1: the frozen mutant generator, preserved as evidence"),
    "artifacts/lunaabsentcpu/killtable2/fix_lunaabs.v2.py":
        (CLASS_RESEARCH, "lunaabsentcpu (#503) table 2: the frozen fix script the baseline was derived from, preserved as evidence"),
    "artifacts/lunaabsentcpu/killtable2/luna_absentcpu_probe.frozen.py":
        (CLASS_RESEARCH, "lunaabsentcpu (#503) table 2: the frozen instrument the table ran, preserved as evidence"),
    "artifacts/lunaabsentcpu/killtable2/mut_lunaabs.v3.py":
        (CLASS_RESEARCH, "lunaabsentcpu (#503) table 2: the frozen mutant generator, preserved as evidence"),
    "artifacts/lunaabsentcpu/killtable3/fix_lunaabs.v2b.py":
        (CLASS_RESEARCH, "lunaabsentcpu (#503) table 3: the frozen fix script the baseline was derived from, preserved as evidence"),
    "artifacts/lunaabsentcpu/killtable3/luna_absentcpu_probe.frozen.py":
        (CLASS_RESEARCH, "lunaabsentcpu (#503) table 3: the frozen instrument the table ran, preserved as evidence"),
    "artifacts/lunaabsentcpu/killtable3/mut_lunaabs.v4.py":
        (CLASS_RESEARCH, "lunaabsentcpu (#503) table 3: the frozen mutant generator, preserved as evidence"),
    "artifacts/lunaabsentcpu/killtable4/luna_absentcpu_probe.frozen.py":
        (CLASS_RESEARCH, "lunaabsentcpu (#503) table 4: the frozen instrument the table ran, preserved as evidence"),
    "artifacts/lunaabsentcpu/killtable5/luna_absentcpu_probe.frozen.py":
        (CLASS_RESEARCH, "lunaabsentcpu (#503) table 5: the frozen instrument the table ran, preserved as evidence"),
    "artifacts/lunaabsentcpu/luna_absentcpu_probe.asrun.py":
        (CLASS_RESEARCH, "lunaabsentcpu (#503) the round's top-level evidence: the frozen instrument the table ran, preserved as evidence"),
    "artifacts/lunaabsentcpu/luna_absentcpu_probe.v2.py":
        (CLASS_RESEARCH, "lunaabsentcpu (#503) the round's top-level evidence: the frozen instrument the table ran, preserved as evidence"),
    "artifacts/lunaabsentcpu/luna_absentcpu_probe.v3.py":
        (CLASS_RESEARCH, "lunaabsentcpu (#503) the round's top-level evidence: the frozen instrument the table ran, preserved as evidence"),
    "artifacts/lunaabsentcpu/luna_absentcpu_probe.v4.py":
        (CLASS_RESEARCH, "lunaabsentcpu (#503) the round's top-level evidence: the frozen instrument the table ran, preserved as evidence"),
    "artifacts/lunaabsentcpu/luna_absentcpu_probe.v5.py":
        (CLASS_RESEARCH, "lunaabsentcpu (#503) the round's top-level evidence: the frozen instrument the table ran, preserved as evidence"),
    "artifacts/lunaabsentcpu/luna_absentcpu_probe.v6.frozen.py":
        (CLASS_RESEARCH, "lunaabsentcpu (#503) the round's top-level evidence: the frozen instrument the table ran, preserved as evidence"),
    "artifacts/lunaabsentcpu/luna_absentcpu_probe.v7.frozen.py":
        (CLASS_RESEARCH, "lunaabsentcpu (#503) the round's top-level evidence: the frozen instrument the table ran, preserved as evidence"),
    "artifacts/lunaabsentcpu/opus_p4_table/luna_absentcpu_probe.frozen.py":
        (CLASS_RESEARCH, "lunaabsentcpu (#503) the measuring seat's own pass-4 table: the frozen instrument the table ran, preserved as evidence"),
    "artifacts/lunaabsentcpu/opus_p4_table_v5/probe_v4.py":
        (CLASS_RESEARCH, "lunaabsentcpu (#503) the measuring seat's pass-4 cross-check against the frozen v5 instrument: preserved apparatus, preserved as evidence"),
    "artifacts/lunaabsentcpu/opus_p4_table_v5/probe_v5.py":
        (CLASS_RESEARCH, "lunaabsentcpu (#503) the measuring seat's pass-4 cross-check against the frozen v5 instrument: preserved apparatus, preserved as evidence"),
    "artifacts/m88kexcdeliver/agy_p5/mutate.py":
        (CLASS_RESEARCH, "m88kexcdeliver (#502) the agy seat's pass-5 measurement: preserved apparatus, preserved as evidence"),
    "artifacts/m88kexcdeliver/killtable/m88k_exc_probe.frozen.py":
        (CLASS_RESEARCH, "m88kexcdeliver (#502) table 1: the frozen instrument the table ran, preserved as evidence"),
    "artifacts/m88kexcdeliver/killtable10/m88k_exc_probe.frozen10.py":
        (CLASS_RESEARCH, "m88kexcdeliver (#502) table 10: the frozen instrument the table ran, preserved as evidence"),
    "artifacts/m88kexcdeliver/killtable10/mut_m88kexc.v10.py":
        (CLASS_RESEARCH, "m88kexcdeliver (#502) table 10: the frozen mutant generator, preserved as evidence"),
    "artifacts/m88kexcdeliver/killtable11/m88k_exc_probe.frozen11.py":
        (CLASS_RESEARCH, "m88kexcdeliver (#502) table 11: the frozen instrument the table ran, preserved as evidence"),
    "artifacts/m88kexcdeliver/killtable11/m88k_exc_probe.frozen11.v14.py":
        (CLASS_RESEARCH, "m88kexcdeliver (#502) table 11: the frozen instrument the table ran, preserved as evidence"),
    "artifacts/m88kexcdeliver/killtable11_attempt1_v13/m88k_exc_probe.frozen11.py":
        (CLASS_RESEARCH, "m88kexcdeliver (#502) table 11 run 1 (ABORTED at its BASE gate on a mis-cut row, preserved as the record of what ran): the frozen instrument the table ran, preserved as evidence"),
    "artifacts/m88kexcdeliver/killtable11_attempt1_v13/m88k_exc_probe.frozen11.v13.py":
        (CLASS_RESEARCH, "m88kexcdeliver (#502) table 11 run 1 (ABORTED at its BASE gate on a mis-cut row, preserved as the record of what ran): the frozen instrument the table ran, preserved as evidence"),
    "artifacts/m88kexcdeliver/killtable12/m88k_exc_probe.frozen12.py":
        (CLASS_RESEARCH, "m88kexcdeliver (#502) table 12: the frozen instrument the table ran, preserved as evidence"),
    "artifacts/m88kexcdeliver/killtable13/m88k_exc_probe.frozen13.py":
        (CLASS_RESEARCH, "m88kexcdeliver (#502) table 13: the frozen instrument the table ran, preserved as evidence"),
    "artifacts/m88kexcdeliver/killtable2/m88k_exc_probe.frozen2.py":
        (CLASS_RESEARCH, "m88kexcdeliver (#502) table 2: the frozen instrument the table ran, preserved as evidence"),
    "artifacts/m88kexcdeliver/killtable3/m88k_exc_probe.frozen3.py":
        (CLASS_RESEARCH, "m88kexcdeliver (#502) table 3: the frozen instrument the table ran, preserved as evidence"),
    "artifacts/m88kexcdeliver/killtable4/m88k_exc_probe.frozen4.py":
        (CLASS_RESEARCH, "m88kexcdeliver (#502) table 4: the frozen instrument the table ran, preserved as evidence"),
    "artifacts/m88kexcdeliver/killtable5/m88k_exc_probe.frozen5.py":
        (CLASS_RESEARCH, "m88kexcdeliver (#502) table 5: the frozen instrument the table ran, preserved as evidence"),
    "artifacts/m88kexcdeliver/killtable5/mut_m88kexc.v5.py":
        (CLASS_RESEARCH, "m88kexcdeliver (#502) table 5: the frozen mutant generator, preserved as evidence"),
    "artifacts/m88kexcdeliver/killtable6/m88k_exc_probe.frozen6.py":
        (CLASS_RESEARCH, "m88kexcdeliver (#502) table 6: the frozen instrument the table ran, preserved as evidence"),
    "artifacts/m88kexcdeliver/killtable6/mut_m88kexc.v6.py":
        (CLASS_RESEARCH, "m88kexcdeliver (#502) table 6: the frozen mutant generator, preserved as evidence"),
    "artifacts/m88kexcdeliver/killtable7/m88k_exc_probe.frozen7.py":
        (CLASS_RESEARCH, "m88kexcdeliver (#502) table 7: the frozen instrument the table ran, preserved as evidence"),
    "artifacts/m88kexcdeliver/killtable7/mut_m88kexc.v7.py":
        (CLASS_RESEARCH, "m88kexcdeliver (#502) table 7: the frozen mutant generator, preserved as evidence"),
    "artifacts/m88kexcdeliver/killtable8/m88k_exc_probe.frozen8.py":
        (CLASS_RESEARCH, "m88kexcdeliver (#502) table 8: the frozen instrument the table ran, preserved as evidence"),
    "artifacts/m88kexcdeliver/killtable8/mut_m88kexc.v8.py":
        (CLASS_RESEARCH, "m88kexcdeliver (#502) table 8: the frozen mutant generator, preserved as evidence"),
    "artifacts/m88kexcdeliver/killtable_opus_p8/m88k_exc_probe.censusP8.py":
        (CLASS_RESEARCH, "m88kexcdeliver (#502) the measuring seat's own pass-8 table: the frozen instrument the table ran, preserved as evidence"),
    "artifacts/m88kexcdeliver/killtable_opus_p8/m88k_exc_probe.frozenP8.py":
        (CLASS_RESEARCH, "m88kexcdeliver (#502) the measuring seat's own pass-8 table: the frozen instrument the table ran, preserved as evidence"),
    "artifacts/m88kexcdeliver/killtable_opus_p8/mutate_p8.py":
        (CLASS_RESEARCH, "m88kexcdeliver (#502) the measuring seat's own pass-8 table: preserved apparatus, preserved as evidence"),
    "artifacts/m88kexcdeliver/kimi_p5/m88k_exc_probe_v5p2.py":
        (CLASS_RESEARCH, "m88kexcdeliver (#502) the kimi seat's pass-5 measurement: the frozen instrument the table ran, preserved as evidence"),
    "artifacts/m88kexcdeliver/m88k_exc_probe.v16.frozen.py":
        (CLASS_RESEARCH, "m88kexcdeliver (#502) the round's top-level evidence: the frozen instrument the table ran, preserved as evidence"),
    "m88k_exc_probe.py":
        (CLASS_DETECTOR, "m88kexcdeliver detector (#502): the m88k exception-delivery path, 54 fault rows + 2 controls, run by gate_m88k_rounding.sh"),
    #  m88kexcdeliver (#502) and lunaabsentcpu (#503), 2026-09-06 evening: the pass-9..12 and pass-2
    #  additions.  One SHIPPED DETECTOR (luna_absentcpu_probe.py, gated in gate_m88k_rounding.sh);
    #  the rest are frozen instruments and one deriver, preserved beside the tables that ran them.
    "luna_absentcpu_probe.py":
        (CLASS_DETECTOR, "lunaabsentcpu detector (#503): dev_luna88k.c reassert_interrupts(), 37 rows + liveness and device-signature controls, run by gate_m88k_rounding.sh.  Also the round's rung-3 WITNESS."),
    "artifacts/lunaabsentcpu/luna_absentcpu_probe.v8.frozen.py":
        (CLASS_RESEARCH, "lunaabsentcpu (#503): the v8 instrument (contract updated with table 6's measured members), preserved as evidence"),
    "artifacts/m88kexcdeliver/derive_cells.py":
        (CLASS_RESEARCH, "m88kexcdeliver (#502): the {arm x settable-bit} cell census DERIVER, written after a bare total proved underivable on pass 10; prints the grid, not the count.  Evidence, not a detector"),
    "artifacts/m88kexcdeliver/killtable14/m88k_exc_probe.frozen14.py":
        (CLASS_RESEARCH, "m88kexcdeliver (#502) table 14: the frozen instrument that table ran, preserved as evidence"),
    "artifacts/m88kexcdeliver/m88k_exc_probe.v17.frozen.py":
        (CLASS_RESEARCH, "m88kexcdeliver (#502): the v17 instrument (grok's pass-9 SER closure), preserved as evidence"),
    "artifacts/m88kexcdeliver/m88k_exc_probe.v20.frozen.py":
        (CLASS_RESEARCH, "m88kexcdeliver (#502): the v20 instrument (records-only over v19), preserved as evidence"),
    "artifacts/m88kexcdeliver/m88k_exc_probe.v21.frozen.py":
        (CLASS_RESEARCH, "m88kexcdeliver (#502): the v21 instrument (the pass-12 ruling recorded in place), preserved as evidence"),
    "artifacts/wdcaltoffset/witness_20260829/wdcaltoff_rung3_probe.py":
        (CLASS_RESEARCH, "#493 wdcaltoffset rung-3 witness probe, preserved as evidence"),
    "artifacts/wdcaltoffset/witness_20260829/mkfixleg.py":
        (CLASS_RESEARCH, "#493 wdcaltoffset fix-leg builder, preserved as evidence"),
    #  pcc2widthkills (passes 3-13, 2026-09-03..05) and the pcc2defaultkill witness: every .py preserved under
    #  regress/artifacts/ by those rounds is EVIDENCE (#471 class) -- frozen instruments beside their kill
    #  tables, the measuring seats' drivers and discriminators, one rung-3 witness.  Generated 2026-09-05 from
    #  the hook's own UNCLASSIFIED list at the pass-13 commit; one line per file, deliberately.
    "pcc2_default_probe.py":
        (CLASS_DETECTOR, "pcc2defaultkill detector (#501): the default arm of DEVICE_ACCESS(pcc2), 46 rows, run by gate_arm.sh beside the width probe"),
    "artifacts/pcc2defaultkill/killtable_20260905/frozen_probe.py":
        (CLASS_RESEARCH, "#501 table 1/2: the frozen 23-row instrument, preserved beside its logs"),
    "artifacts/pcc2defaultkill/killtable_20260905/pcc2_width_probe.py":
        (CLASS_RESEARCH, "#501 table 1/2: the frozen session helper the instrument borrows, preserved beside it"),
    "artifacts/pcc2defaultkill/killtable_20260905/run1_oldrowformat/frozen_probe.py":
        (CLASS_RESEARCH, "#501 table run 1: the status-first instrument the gate could not count, preserved as the L1 record"),
    "artifacts/pcc2defaultkill/killtable_20260905/run1_oldrowformat/pcc2_width_probe.py":
        (CLASS_RESEARCH, "#501 table run 1: its frozen session helper"),
    "artifacts/pcc2defaultkill/killtable3_20260905/frozen_probe.py":
        (CLASS_RESEARCH, "#501 table 3: the frozen 36-row instrument, preserved beside its logs"),
    "artifacts/pcc2defaultkill/killtable3_20260905/pcc2_width_probe.py":
        (CLASS_RESEARCH, "#501 table 3: its frozen session helper"),
    "artifacts/pcc2defaultkill/killtable3_20260905/old23/frozen_probe.py":
        (CLASS_RESEARCH, "#501 table 3: the pass-2 (23-row) instrument the six escapes were re-measured on"),
    "artifacts/pcc2defaultkill/killtable3_20260905/old23/pcc2_width_probe.py":
        (CLASS_RESEARCH, "#501 table 3: the pass-2 instrument's session helper"),
    "artifacts/pcc2defaultkill/killtable4_20260905/frozen_probe.py":
        (CLASS_RESEARCH, "#501 table 4: the frozen 46-row instrument, preserved beside its logs"),
    "artifacts/pcc2defaultkill/killtable4_20260905/pcc2_width_probe.py":
        (CLASS_RESEARCH, "#501 table 4: its frozen session helper"),
    "artifacts/pcc2defaultkill/killtable4_20260905/old36/frozen_probe.py":
        (CLASS_RESEARCH, "#501 table 4: the pass-3 (36-row) instrument the ten escapes were re-measured on"),
    "artifacts/pcc2defaultkill/killtable4_20260905/old36/pcc2_width_probe.py":
        (CLASS_RESEARCH, "#501 table 4: the pass-3 instrument's session helper"),
    "artifacts/pcc2defaultkill/pass3_seats/opus_logs/edit_M_BACKEDLOW.py":
        (CLASS_RESEARCH, "#501 pass 3, Opus seat: the mutant edit script behind a measured 36/36 sweep, preserved as evidence"),
    "artifacts/pcc2defaultkill/pass3_seats/opus_logs/edit_M_LASTBYTE.py":
        (CLASS_RESEARCH, "#501 pass 3, Opus seat: mutant edit script, preserved as evidence"),
    "artifacts/pcc2defaultkill/pass3_seats/opus_logs/edit_M_LATCHOFF.py":
        (CLASS_RESEARCH, "#501 pass 3, Opus seat: mutant edit script, preserved as evidence"),
    "artifacts/pcc2defaultkill/pass3_seats/opus_logs/edit_M_RELOAD.py":
        (CLASS_RESEARCH, "#501 pass 3, Opus seat: mutant edit script, preserved as evidence"),
    "artifacts/pcc2defaultkill/pass3_seats/opus_logs/edit_M_WRDATA0.py":
        (CLASS_RESEARCH, "#501 pass 3, Opus seat: mutant edit script, preserved as evidence"),
    "artifacts/pcc2defaultkill/pass3_seats/opus_logs/edit_M_WRVAL0.py":
        (CLASS_RESEARCH, "#501 pass 3, Opus seat: mutant edit script, preserved as evidence"),
    "artifacts/pcc2defaultkill/pass4_seats/opus_logs/gatecheck.py":
        (CLASS_RESEARCH, "#501 pass 4, Opus seat: its gate-list vs probe-rows cross-check, preserved as evidence"),
    "artifacts/pcc2defaultkill/pass4_seats/opus_logs/len4_witness.py":
        (CLASS_RESEARCH, "#501 pass 4, Opus seat: the st.d-at-T2COUNT route to a nonzero len-4 read (the pcc2counter8 coupling), preserved"),
    "artifacts/pcc2defaultkill/pass4_seats/opus_logs/logs/len4_witness.py":
        (CLASS_RESEARCH, "#501 pass 4, Opus seat: a copy of the same witness beside its log"),
    "artifacts/pcc2defaultkill/pass4_seats/opus_logs/mutate.py":
        (CLASS_RESEARCH, "#501 pass 4, Opus seat: its mutant applier, preserved as evidence"),
    "artifacts/pcc2defaultkill/pass4_seats/opus_logs/offsets.py":
        (CLASS_RESEARCH, "#501 pass 4, Opus seat: its 43-offset census re-derivation, preserved as evidence"),
    "artifacts/pcc2defaultkill/witness_20260905/defaultkill_witness.py":
        (CLASS_RESEARCH, "pcc2defaultkill rung-3 witness (guest st.b/ld.bu at uncased offsets), preserved as evidence; not a gate"),
    "artifacts/pcc2widthkills/killtable2_20260903/part10/frozen_probe.py":
        (CLASS_RESEARCH, "pcc2widthkills: the frozen instrument a kill table measured, preserved beside its logs"),
    "artifacts/pcc2widthkills/killtable2_20260903/part10_aborted/frozen_probe.py":
        (CLASS_RESEARCH, "pcc2widthkills: the frozen instrument a kill table measured, preserved beside its logs"),
    "artifacts/pcc2widthkills/killtable2_20260903/part11/frozen_probe.py":
        (CLASS_RESEARCH, "pcc2widthkills: the frozen instrument a kill table measured, preserved beside its logs"),
    "artifacts/pcc2widthkills/killtable2_20260903/part12/frozen_probe.py":
        (CLASS_RESEARCH, "pcc2widthkills: the frozen instrument a kill table measured, preserved beside its logs"),
    "artifacts/pcc2widthkills/killtable2_20260903/part13/frozen_probe.py":
        (CLASS_RESEARCH, "pcc2widthkills: the frozen instrument a kill table measured, preserved beside its logs"),
    "artifacts/pcc2widthkills/killtable2_20260903/part13_aborted/frozen_probe.py":
        (CLASS_RESEARCH, "pcc2widthkills: the frozen instrument a kill table measured, preserved beside its logs"),
    "artifacts/pcc2widthkills/killtable2_20260903/part13_partial/frozen_probe.py":
        (CLASS_RESEARCH, "pcc2widthkills: the frozen instrument a kill table measured, preserved beside its logs"),
    "artifacts/pcc2widthkills/killtable2_20260903/part2/frozen_probe.py":
        (CLASS_RESEARCH, "pcc2widthkills: the frozen instrument a kill table measured, preserved beside its logs"),
    "artifacts/pcc2widthkills/killtable2_20260903/part3/frozen_probe.py":
        (CLASS_RESEARCH, "pcc2widthkills: the frozen instrument a kill table measured, preserved beside its logs"),
    "artifacts/pcc2widthkills/killtable2_20260903/part3b/frozen_probe.py":
        (CLASS_RESEARCH, "pcc2widthkills: the frozen instrument a kill table measured, preserved beside its logs"),
    "artifacts/pcc2widthkills/killtable2_20260903/part3c/frozen_probe.py":
        (CLASS_RESEARCH, "pcc2widthkills: the frozen instrument a kill table measured, preserved beside its logs"),
    "artifacts/pcc2widthkills/killtable2_20260903/part4/frozen_probe.py":
        (CLASS_RESEARCH, "pcc2widthkills: the frozen instrument a kill table measured, preserved beside its logs"),
    "artifacts/pcc2widthkills/killtable2_20260903/part5/frozen_probe.py":
        (CLASS_RESEARCH, "pcc2widthkills: the frozen instrument a kill table measured, preserved beside its logs"),
    "artifacts/pcc2widthkills/killtable2_20260903/part5b/frozen_probe.py":
        (CLASS_RESEARCH, "pcc2widthkills: the frozen instrument a kill table measured, preserved beside its logs"),
    "artifacts/pcc2widthkills/killtable2_20260903/part6/frozen_probe.py":
        (CLASS_RESEARCH, "pcc2widthkills: the frozen instrument a kill table measured, preserved beside its logs"),
    "artifacts/pcc2widthkills/killtable2_20260903/part6b/frozen_probe.py":
        (CLASS_RESEARCH, "pcc2widthkills: the frozen instrument a kill table measured, preserved beside its logs"),
    "artifacts/pcc2widthkills/killtable2_20260903/part7/frozen_probe.py":
        (CLASS_RESEARCH, "pcc2widthkills: the frozen instrument a kill table measured, preserved beside its logs"),
    "artifacts/pcc2widthkills/killtable2_20260903/part7b/frozen_probe.py":
        (CLASS_RESEARCH, "pcc2widthkills: the frozen instrument a kill table measured, preserved beside its logs"),
    "artifacts/pcc2widthkills/killtable2_20260903/part8/frozen_probe.py":
        (CLASS_RESEARCH, "pcc2widthkills: the frozen instrument a kill table measured, preserved beside its logs"),
    "artifacts/pcc2widthkills/killtable2_20260903/part9/frozen_probe.py":
        (CLASS_RESEARCH, "pcc2widthkills: the frozen instrument a kill table measured, preserved beside its logs"),
    "artifacts/pcc2widthkills/opus_pass3_20260903/pass3/probe.frozen.py":
        (CLASS_RESEARCH, "pcc2widthkills: a measuring seat's own script (mutant driver / discriminator / check), preserved as evidence"),
    "artifacts/pcc2widthkills/opus_pass3_20260903/pass3c/probe82.frozen.py":
        (CLASS_RESEARCH, "pcc2widthkills: a measuring seat's own script (mutant driver / discriminator / check), preserved as evidence"),
    "artifacts/pcc2widthkills/pass10_seats_20260904/opus/cmpnames.py":
        (CLASS_RESEARCH, "pcc2widthkills: a measuring seat's own script (mutant driver / discriminator / check), preserved as evidence"),
    "artifacts/pcc2widthkills/pass10_seats_20260904/opus/diffcheck.py":
        (CLASS_RESEARCH, "pcc2widthkills: a measuring seat's own script (mutant driver / discriminator / check), preserved as evidence"),
    "artifacts/pcc2widthkills/pass10_seats_20260904/opus/mutate.py":
        (CLASS_RESEARCH, "pcc2widthkills: a measuring seat's own script (mutant driver / discriminator / check), preserved as evidence"),
    "artifacts/pcc2widthkills/pass11_seats_20260904/opus/control_iclr.py":
        (CLASS_RESEARCH, "pcc2widthkills: a measuring seat's own script (mutant driver / discriminator / check), preserved as evidence"),
    "artifacts/pcc2widthkills/pass3_seats_20260903/opus_reader/mutate.py":
        (CLASS_RESEARCH, "pcc2widthkills: a measuring seat's own script (mutant driver / discriminator / check), preserved as evidence"),
    "artifacts/pcc2widthkills/pass3_seats_20260903/opus_reader/nonequiv_check.py":
        (CLASS_RESEARCH, "pcc2widthkills: a measuring seat's own script (mutant driver / discriminator / check), preserved as evidence"),
    "artifacts/pcc2widthkills/pass4_seats_20260903/fable/dump_names.py":
        (CLASS_RESEARCH, "pcc2widthkills: a measuring seat's own script (mutant driver / discriminator / check), preserved as evidence"),
    "artifacts/pcc2widthkills/pass4_seats_20260903/fable/probe_copy.py":
        (CLASS_RESEARCH, "pcc2widthkills: a measuring seat's own script (mutant driver / discriminator / check), preserved as evidence"),
    "artifacts/pcc2widthkills/pass4_seats_20260903/fable/probe_dry.py":
        (CLASS_RESEARCH, "pcc2widthkills: a measuring seat's own script (mutant driver / discriminator / check), preserved as evidence"),
    "artifacts/pcc2widthkills/pass4_seats_20260903/opus_reader/frozen_probe.py":
        (CLASS_RESEARCH, "pcc2widthkills: the frozen instrument a kill table measured, preserved beside its logs"),
    "artifacts/pcc2widthkills/pass5_seats_20260903/fable/frozen_probe.py":
        (CLASS_RESEARCH, "pcc2widthkills: the frozen instrument a kill table measured, preserved beside its logs"),
    "artifacts/pcc2widthkills/pass5_seats_20260903/fable/pty_ret0_probe.py":
        (CLASS_RESEARCH, "pcc2widthkills: a measuring seat's own script (mutant driver / discriminator / check), preserved as evidence"),
    "artifacts/pcc2widthkills/pass5_seats_20260903/opus_reader/artifacts/discriminator.py":
        (CLASS_RESEARCH, "pcc2widthkills: a measuring seat's own script (mutant driver / discriminator / check), preserved as evidence"),
    "artifacts/pcc2widthkills/pass5_seats_20260903/opus_reader/artifacts/gxopus_p5_disc.py":
        (CLASS_RESEARCH, "pcc2widthkills: a measuring seat's own script (mutant driver / discriminator / check), preserved as evidence"),
    "artifacts/pcc2widthkills/pass5_seats_20260903/opus_reader/discriminator.py":
        (CLASS_RESEARCH, "pcc2widthkills: a measuring seat's own script (mutant driver / discriminator / check), preserved as evidence"),
    "artifacts/pcc2widthkills/pass5_seats_20260903/opus_reader/mutate.py":
        (CLASS_RESEARCH, "pcc2widthkills: a measuring seat's own script (mutant driver / discriminator / check), preserved as evidence"),
    "artifacts/pcc2widthkills/pass5_seats_20260903/opus_reader/xcheck.py":
        (CLASS_RESEARCH, "pcc2widthkills: a measuring seat's own script (mutant driver / discriminator / check), preserved as evidence"),
    "artifacts/pcc2widthkills/pass6_seats_20260903/opus/mutate.py":
        (CLASS_RESEARCH, "pcc2widthkills: a measuring seat's own script (mutant driver / discriminator / check), preserved as evidence"),
    "artifacts/pcc2widthkills/pass7_seats_20260904/opus/gatecheck.py":
        (CLASS_RESEARCH, "pcc2widthkills: a measuring seat's own script (mutant driver / discriminator / check), preserved as evidence"),
    "artifacts/pcc2widthkills/pass8_seats_20260904/opus/mk_f1.py":
        (CLASS_RESEARCH, "pcc2widthkills: a measuring seat's own script (mutant driver / discriminator / check), preserved as evidence"),
    "artifacts/pcc2widthkills/pass8_seats_20260904/opus/mutate.py":
        (CLASS_RESEARCH, "pcc2widthkills: a measuring seat's own script (mutant driver / discriminator / check), preserved as evidence"),
    "artifacts/pcc2widthkills/pass9_seats_20260904/opus/audit_gate.py":
        (CLASS_RESEARCH, "pcc2widthkills: a measuring seat's own script (mutant driver / discriminator / check), preserved as evidence"),
    "artifacts/pcc2widthkills/pass9_seats_20260904/opus/cmp_names.py":
        (CLASS_RESEARCH, "pcc2widthkills: a measuring seat's own script (mutant driver / discriminator / check), preserved as evidence"),
    "artifacts/pcc2widthkills/pass9_seats_20260904/opus/frozen_probe.py":
        (CLASS_RESEARCH, "pcc2widthkills: the frozen instrument a kill table measured, preserved beside its logs"),
    "artifacts/pcc2widthkills/pass9_seats_20260904/opus/mutate.py":
        (CLASS_RESEARCH, "pcc2widthkills: a measuring seat's own script (mutant driver / discriminator / check), preserved as evidence"),

    #  wdcaltoffset PASS 1, 2026-08-30.  Four instruments from the measuring seat's
    #  six-binary table.  CLASS_RESEARCH on the precedent two entries down: they are
    #  EVIDENCE preserved so the numbers can be re-run rather than believed.
    #
    #  `table_a.py` is worth a note because it is the reason the table is credible:
    #  it IMPORTS witness_20260829/wdcaltoff_rung3_probe.py rather than
    #  re-implementing the encoder, so it cannot measure a fix of its own invention.
    #  Its fix leg was checked byte-identical to mkfixleg.py's output AND to the
    #  preserved fixleg.diff before any mutant was built.
    #  #494 PASS 2, the opus5 seat.  Instruments preserved so its measured floor
    #  breach can be re-run rather than believed.  `PROPOSED_...` is kept as the
    #  PROVENANCE of what the seat proposed: the shipped detector differs from it
    #  only by an added clause-(e) contract, and keeping both makes that checkable.
    #  wdcaddtoinbufbound RUNG-3 WITNESS, 2026-08-30.  The probe is the INSTRUMENT of
    #  a 20/20 two-leg measurement and is preserved so the numbers can be re-run
    #  rather than believed.  `frozen_wave_*` is the FROZEN COPY the run actually
    #  executed -- kept beside the live probe on purpose, because a comparison run
    #  owes ONE instrument and the frozen copy is the proof of which one it was.
    #  #497 widthkillclass, 2026-08-30.  The measuring seat's TWO-TABLE instrument set,
    #  preserved so a 22-mutant result can be RE-RUN rather than believed.  CLASS_RESEARCH
    #  on the precedent immediately below: these are EVIDENCE, not detectors the battery
    #  owes a run.
    #
    #  `sgi_re_width_probe.py` is the 35-row detector ITSELF, and it is filed here as
    #  research on purpose: the round's shipping copy will live in regress/ and be gated or
    #  dated-exempt.  Two copies with two classes is correct rather than untidy -- the
    #  artifacts one is the instrument that produced THESE numbers and must never change,
    #  while the regress/ one is live and will.
    #
    #  `mutate497.py` and `mutate497_v2.py` are BOTH kept, and the pair is the point: v1
    #  was re-read from the live scratchpad per mutant, which is the frozen-copy hole the
    #  seat caught before it bit.  v2 freezes the mutator and hard-exits if it is missing.
    #  Keeping only v2 would erase the evidence that table 1 and table 2 ran different
    #  drivers -- which is exactly what a reader comparing the two tables needs to know.
    "artifacts/widthkillclass/opus_impl_20260830/apply_fix497.py":
        (CLASS_RESEARCH, "#497 applies the six-site fix to a clone, preserved as evidence"),
    "artifacts/widthkillclass/opus_impl_20260830/move_warned.py":
        (CLASS_RESEARCH, "#497 moves the latch field last -- the edit that stopped the over-run aliasing the latch"),
    "artifacts/widthkillclass/opus_impl_20260830/mutate497.py":
        (CLASS_RESEARCH, "#497 table-1 mutator, kept to show v1 re-read itself per mutant"),
    "artifacts/widthkillclass/opus_impl_20260830/mutate497_v2.py":
        (CLASS_RESEARCH, "#497 table-2 mutator, frozen and hard-exiting if absent"),
    "artifacts/widthkillclass/opus_impl_20260830/sgi_re_width_probe.py":
        (CLASS_RESEARCH, "#497 the 35-row detector AS MEASURED -- the shipping copy is separate and gated"),
    #  #500 pass 6: the NEGATIVE CONTROL's mutated probe, frozen as evidence.  It is
    #  a MUTANT of the shipping detector, deliberately run by no gate -- its whole
    #  purpose is to reproduce a RED.  A seat built the mutant it carries; the
    #  control proved both that the hole existed and that the repair closes it.
    "artifacts/sgideprimop/killtable_20260902_table4/negctl_n25_rectset_probe.py":
        (CLASS_RESEARCH, "#500 the negative control AS RUN -- drawmode store neutered; reds n25 rectset alone, 38/39"),
    #  #500 pass 12: the FROZEN INSTRUMENT of the class-closure table.  A comparison
    #  run owes ONE instrument, so the driver copies the probe once and every cell
    #  scores against that copy -- a driver that re-reads the live probe between
    #  cells gives run 1 and run 2 different tools, which this project has measured
    #  (a 39/40 against a table of /39).  It is EVIDENCE, deliberately run by no gate;
    #  the shipping copy is regress/sgi_de_primop_probe.py and gate_arm.sh runs that.
    "artifacts/sgideprimop/killtable_20260903_table13_xfer/frozen_probe.py":
        (CLASS_RESEARCH, "#500 pass 15 frozen instrument for the eleven-register closure table (51 rows; six XFER cells closed, two declared limits measured)"),
    "artifacts/sgideprimop/gapB_20260903/frozen_probe.py":
        (CLASS_RESEARCH, "#500 pass 15 the 50-row instrument AS MEASURED against || step_x -- the gap, 50/50, before the repair"),
    "artifacts/sgideprimop/killtable_20260903_table12_regs/frozen_probe.py":
        (CLASS_RESEARCH, "#500 pass 14 frozen instrument for the register-family closure table (50 rows, dec regs set at want=1 -- the corrected live probe wants 2)"),
    "artifacts/sgideprimop/killtable_20260902_table11_closure/frozen_probe.py":
        (CLASS_RESEARCH, "#500 pass 12 frozen instrument for the class-closure table -- the 47-row probe AS MEASURED across B24/B27-B31 plus the B25/B26 controls"),

    "artifacts/widthkillclass/opus_impl_20260830/strengthen_comment.py":
        (CLASS_RESEARCH, "#497 applies the measured memory-safety wording at the two LINEAR sites only"),

    #  #498's SHIPPING detector -- gate-wired in gate_arm.sh, 25 rows, sentinel
    #  OPUS498T_DONE.  CLASS_DETECTOR rather than research: the battery owes it a run.
    #  Self-contained by deliberate choice -- every committed probe in this tree rolls its
    #  own pty rather than importing the untracked _scratchpad/gxprobe.py, and following
    #  that precedent avoids making a committed file depend on one outside the repo.
    "sgi_de_width_probe.py":
        (CLASS_DETECTOR, "#498 sgidewidth -- 25 rows, gate_arm.sh, every row from a measured mutant kill"),

    #  sgireunmapped #499: the SHIPPED detector.  Gate-run by gate_arm.sh -- invocation,
    #  OPUS499T_DONE sentinel check, controls by name, EVERY row named individually, and
    #  a SUMMED denominator that separates a LOST row from a FAILING one.
    #
    #  *** THE ROW COUNT IS NOT WRITTEN HERE.  It went 28 -> 34 -> 36 -> 48 across four
    #  passes in one day and this comment said 28 for all of them.  Derive it: ***
    #
    #      awk '/for v in "live"/{l=$0; getline n;
    #           if (n ~ /UNMLOG/) {print gsub(/"[^"]*"/,"",l)}}' regress/gate_arm.sh
    #
    #  The `getline'/UNMLOG pair is load-bearing and is not defensive clutter: several
    #  sections of gate_arm.sh open with the same `for v in "live" "devsig"' names, so
    #  the FIRST match is a different probe's list.  The log variable on the NEXT line
    #  is the only thing that identifies which section a row list belongs to.  (A first
    #  attempt here counted `check "sgi_re unmapped row:"' lines and returned 1 -- the
    #  rows are named in a LOOP, so there is one such line however many rows exist.
    #  It was caught by running it, which is the whole reason a deriver is written down
    #  instead of a number.)
    #
    #  (Demoted literals, kept as the record of what was measured and never as current
    #  claims: 18/28 pre-fix and 28/28 on the fix, the test-first evidence in this row's
    #  own artifacts dir; 30/34 and 33/34 for the two pass-2 mutants against the 34-row
    #  repair, where the 28-row version had scored both 28/28.)
    #  #500 sgideprimop: the SHIPPED detector.  Gate-run by gate_arm.sh -- invocation,
    #  OPUS500_DONE sentinel check, every row named individually, and a SUMMED denominator
    #  that separates a LOST row from a FAILING one.
    #
    #  ROW COUNT NOT WRITTEN HERE.  The sibling entry below said "28 rows" through four
    #  passes that took it to 50.  Derive it:
    #
    #      awk '/for v in "live"/{l=$0; getline n;
    #           if (n ~ /PRIMLOG/) {print gsub(/"[^"]*"/,"",l)}}' regress/gate_arm.sh
    #  pcc2widthkills: the WITNESS (rung 3, 4/10 on the committed build, preserved with its
    #  run under artifacts/pcc2widthkills/) and the DETECTOR it grew into.  The witness is
    #  deliberately run by no gate: its job was to exist BEFORE the edit.
    "artifacts/pcc2widthkills/pcc2_width_witness.asrun.py":
        (CLASS_RESEARCH, "pcc2widthkills the witness AS RUN for its 4/10 pre-fix measurement (before the docstring correction)"),
    "artifacts/pcc2widthkills/pcc2_operator_reach.asrun.py":
        (CLASS_RESEARCH, "pcc2widthkills the three-session probe that MEASURED the debugger reaching an odd-offset arm (put h 0xfff42003 -> exit1)"),
    "artifacts/pcc2widthkills/killtable_20260903/frozen_probe.py":
        (CLASS_RESEARCH, "pcc2widthkills frozen instrument for the kill table: PREFIX 14/60, BASE 60/60, seven mutants each killed by its designed rows"),
    "pcc2_width_witness.py":
        (CLASS_WITNESS, "pcc2widthkills rung-3 witness -- three aligned accesses (ld.h GENCTL, ld SCCERR, st.h T2CTL) each ended the host; four controls green"),
    "pcc2_width_probe.py":
        (CLASS_DETECTOR, "pcc2widthkills -- twelve width-guard blocks are a direction split (reads ACCEPT, writes DECLINE + per-instance latch); gate_arm.sh runs it, row count derived from the gate"),
    "sgi_de_primop_probe.py":
        (CLASS_DETECTOR, "#500 sgideprimop -- draw_primitive's default arm is a latched decline; every survival row is PAIRED with a positive post-draw observable, because exit status cannot distinguish declined-and-quit from died-with-status-0"),

    "sgi_re_unmapped_probe.py":
        (CLASS_DETECTOR, "#499 sgireunmapped -- the unmatched-address catch-all is a latched per-direction decline; wired into gate_arm.sh in the same commit as the fix, row count derived from the gate rather than restated here"),

    "sgi_re_randompixel_probe.py":
        (CLASS_DETECTOR, "#504 sgirandompixel -- horrible_getputpixel's unimplemented-mode arm is a "
                         "latched decline; 8 rows, wired into gate_arm.sh in the same commit as the "
                         "fix. It is BOTH the rung-3 witness and the detector. The `lin_b diag once' "
                         "row requires the probe's 1x4 rectangle: with a single pixel an UNLATCHED "
                         "announce also fires exactly once, the latch channel cannot vary, and "
                         "M_NOLATCH escaped 8/8 -- height not width, because LIN_A addressing is "
                         "`ofs = x & 4095' so y is ignored and four rows rewrite one byte, leaving "
                         "the value oracle intact"),

    #  #504's frozen evidence.  The killtable copy is the instrument the five-mutant table ran; the
    #  witness copy is the instrument that measured the COMMITTED build RED at 7/8 under the re-pinned
    #  oracle, which is this round's order proof.  Both are preserved rather than regenerated because a
    #  measurement cited in a durable record must live at a durable path.
    "artifacts/sgirandompixel/killtable/probe.frozen.py":
        (CLASS_RESEARCH, "sgirandompixel (#504) kill table: the frozen instrument the five-mutant "
                         "table ran, preserved as evidence"),
    "artifacts/sgirandompixel/witness_20260906/probe.frozen.py":
        (CLASS_RESEARCH, "sgirandompixel (#504) witness: the frozen instrument that measured the "
                         "committed pre-fix build RED at 7/8 under the re-pinned oracle -- the "
                         "oracle-correction order proof, preserved as evidence"),

    #  sgirebufuninit's two census scanners, preserved beside the brief that cites their OUTPUT.  They
    #  are ANALYSIS tools, not detectors: neither has an oracle and neither is wired to anything.  They
    #  are kept because the brief makes a claim about the whole device tree -- that only dev_sgi_re.c
    #  carries this defect -- and a reader must be able to re-run the search rather than trust the count.
    "artifacts/sgirebufuninit/scan_len.py":
        (CLASS_RESEARCH, "sgirebufuninit: scans src/devices for memory_rw calls whose transfer LENGTH "
                         "is not pinned to the stack buffer (6 sites). Blind by construction to a "
                         "partially-filled buffer passed as sizeof(buf) -- which is what scan_fill.py "
                         "exists to cover"),
    "artifacts/sgirebufuninit/scan_fill.py":
        (CLASS_RESEARCH, "sgirebufuninit: the companion scan -- every memory_rw that WRITES a stack "
                         "byte-buffer into guest-visible memory, with whether the buffer is ever "
                         "initialised wholesale (5 sites). Found dev_scc.c:305, which scan_len.py "
                         "excludes by construction. NOTE its known defect, recorded because it nearly "
                         "produced a wrong conclusion: the declaration map is keyed by NAME file-wide, "
                         "so two functions declaring the same buffer at different sizes collapse to the "
                         "last one parsed -- its `size' column reported 32 for a data[8]"),
    #  #499 pass 4's FROZEN MUTATOR, preserved because the E0/E0W measurement is cited in
    #  the round record and a citation into a session temp dir is not a citation.  It builds
    #  the announce-then-exit(0) mutants; it is EVIDENCE, not a detector the battery owes a
    #  run -- same disposition as the repin2 frozen copy below.
    #
    #  It also carries a lesson worth keeping next to the code: its FIRST version anchored on
    #  the handler's common tail, and `memory_writemax64(cpu, data, len, odata);' occurs FIVE
    #  times across FOUR handlers in dev_sgi_re.c.  The anchor matched twice and the run
    #  aborted.  This version anchors on SGIRE_W_UNMAP_* text and REFUSES unless the match
    #  count is exactly 1, so a wrong-handler mutation is impossible rather than unlikely.
    "artifacts/sgireunmapped/killtable_20260831/pass4/e0_mut.py":
        (CLASS_RESEARCH, "#499 pass 4 -- the frozen mutator for E0/E0W, the announce-then-exit(0) pair that measured the write-side floor breach.  Evidence, not a detector"),

    "artifacts/sgireunmapped/killtable_20260831/repin2/sgi_re_width_probe.repinned.py":
        (CLASS_RESEARCH, "sgireunmapped #499 REPIN2 -- the FROZEN re-pinned copy of #497's shipped probe, kept as the artifact the order proof was measured against.  The live file is regress/sgi_re_width_probe.py; this is evidence, not a second detector"),

    #  sgireunmapped #499 L2 REPAIR, 2026-08-31.  The mutator that rebuilt the two escapes
    #  the pass-2 seat found -- a verbatim reinstatement of the removed kill (floor clause
    #  (b)) and a one-hex-digit bound relaxation (clause (d)) -- against the REPAIRED
    #  34-row detector, which now scores them 30/34 and 33/34 where the 28-row version
    #  scored both 28/28.  CLASS_RESEARCH: evidence, not a detector the battery owes a run.
    #
    #  *** IT USES chr(92) FOR THE BACKSLASH ON PURPOSE AND SAYS SO IN ITS OWN HEADER. ***
    #  The first attempt hand-typed the escape and the C string literal was split by a REAL
    #  newline cooked in through the Bash -> heredoc -> Python path -- `error: missing
    #  terminating " character'.  Keeping this file is what stops the next round
    #  rediscovering that.
    "artifacts/sgireunmapped/killtable_20260831/l2repair/mkw.py":
        (CLASS_RESEARCH, "sgireunmapped #499 L2 -- rebuilds mutant W (the verbatim reinstatement) with chr(92) for the backslash, and asserts the emitted literal landed on ONE line rather than trusting that it did"),

    #  sgireunmapped #499 PORT + REPIN2, 2026-08-31.  CLASS_RESEARCH: the tooling that
    #  ported the detector and then measured the re-pin.  Kept because the round's two
    #  load-bearing negative results live in their output -- the proposed exit0+txt oracle
    #  ESCAPING an exit(0) mutant, and the measuring seat's own first-choice replacement
    #  escaping two more.  Neither is reconstructible from the shipped probe alone.

    "artifacts/sgireunmapped/killtable_20260831/port/mkvariant499.py":
        (CLASS_RESEARCH, "sgireunmapped #499 PORT -- the mutant generator for the ported detector's re-verification; supersedes the 08-30 one whose 1<<6 bit collided with #498"),
    "artifacts/sgireunmapped/killtable_20260831/port/patch_mk.py":
        (CLASS_RESEARCH, "sgireunmapped #499 PORT -- patch helper used to build the port's variants"),
    "artifacts/sgireunmapped/killtable_20260831/port/patch_mk2.py":
        (CLASS_RESEARCH, "sgireunmapped #499 PORT -- second patch helper, same run"),
    "artifacts/sgireunmapped/killtable_20260831/port/repin.py":
        (CLASS_RESEARCH, "sgireunmapped #499 PORT -- implements the CANDIDATE re-pin oracle ONLY and never edits the shipped probe, which is what let the order proof be measured without changing the artifact under test"),
    "artifacts/sgireunmapped/killtable_20260831/repin2/mk500.py":
        (CLASS_RESEARCH, "sgireunmapped #499 REPIN2 -- generator for the five variants that measured the exit0+txt ESCAPE; hard-fails on a duplicate enum bit and asserts the last enumerator is the highest, which is why the enum ordering defect cannot recur silently"),
    "artifacts/sgireunmapped/killtable_20260831/repin2/score500.py":
        (CLASS_RESEARCH, "sgireunmapped #499 REPIN2 -- scores four candidate oracles against five variants.  It EXTRACTS lines 66-197 of the shipped probe rather than reimplementing them, so session()/printed()/Addr/store/load are the shipped ones BY CONSTRUCTION and fidelity is diff-checkable"),
    "artifacts/sgireunmapped/killtable_20260831/repin2/score500b.py":
        (CLASS_RESEARCH, "sgireunmapped #499 REPIN2 -- the in-situ scorer that produced the 35-emitted / 35-green / 0-red denominators, i.e. the evidence that the repair FOLDS INTO the existing row rather than adding one"),

    #  sgireunmapped #499 KILL TABLE, 2026-08-31.  The table that discharged the three
    #  undischarged accept rows (accept tlba/tlbb/tlbc) by MEASURED KILL -- M1/M2/M3 each
    #  reddening exactly its own row -- and that found an L2 floor breach (M5) plus a
    #  duplicate latch-bit defect #498 had silently introduced into the 08-30 generator.
    #  CLASS_RESEARCH: evidence for a round, not detectors the battery owes a run.
    #
    #  *** `mkvariant499.py' REPLACES `opus_witness_20260830/mkvariant.py' AND THE REASON
    #  MUST NOT BE PRUNED. ***  The older generator inserts `SGIRE_W_UNMAP_WR = 1 << 6',
    #  and #498/cb28a6f added `SGIRE_W_DE_LEN = 1 << 6' to that same enum.  A duplicate
    #  enumerator is legal C and silent, and DEVICE_ACCESS(sgi_de) casts the same struct,
    #  so d->warned is SHARED -- measured as a 14/14 total escape.  This one uses 1<<7/1<<8
    #  and hard-fails on duplicates.
    #
    #  `base_slot_probe.py' is the CONTROL for M5 and is what makes it a result rather than
    #  a claim: it stores at the window BASE, reds on the mutant, and is serviced normally
    #  on the fix.  Without it, `accept lina' staying green is merely a green row.
    "artifacts/sgireunmapped/killtable_20260831/extra_rows.py":
        (CLASS_RESEARCH, "sgireunmapped #499 -- the four rows the shipped detector lacks: the M4 latch-collision kill (two NARROW accesses in one emu) and the fix6 duplicate-bit kill, each with its own green control"),
    "artifacts/sgireunmapped/killtable_20260831/base_slot_probe.py":
        (CLASS_RESEARCH, "sgireunmapped #499 -- the window-BASE control that proves M5's near-bound blindness is real and not an artifact of the oracle"),
    "artifacts/sgireunmapped/killtable_20260831/mkvariant499.py":
        (CLASS_RESEARCH, "sgireunmapped #499 mutant generator -- replaces the 08-30 one, whose 1<<6 latch bit collided with #498's SGIRE_W_DE_LEN"),

    #  sgidewidth PASS 2, 2026-08-31.  The measuring seat's nine-build re-measurement of a
    #  SHIPPED detector, which found two 25/25 escapes the round had missed.  CLASS_RESEARCH:
    #  evidence, not detectors the battery owes a run.
    #
    #  *** `probe_frozen.py` IS THE POINT OF THIS SET AND MUST NOT BE PRUNED. ***  The seat
    #  froze the shipped cb28a6f probe before mutant 1 -- and the repo copy WAS EDITED LIVE
    #  UNDER ITS RUN by the main loop (22 -> 25 -> 29 rows).  Without the frozen copy every
    #  score in that table would be against a moving instrument, which is exactly the hazard
    #  the frozen-copy rule exists for, observed rather than hypothesised.
    #
    #  `mutate4.py` builds the VERBATIM pre-fix arm -- floor clauses (a) and (b) -- and is
    #  kept because no earlier artifact showed that measurement: 14/25, eleven rows red.
    "artifacts/sgidewidth/opus_p2_20260831/probe_frozen.py":
        (CLASS_RESEARCH, "sgidewidth pass-2 FROZEN detector -- the shipped cb28a6f probe, held still while the worktree copy moved under the run"),
    "artifacts/sgidewidth/opus_p2_20260831/disc.py":
        (CLASS_RESEARCH, "sgidewidth pass-2 DISCRIMINATING rows -- how bracegoto and bit5collide were proven real, not merely predicted"),
    "artifacts/sgidewidth/opus_p2_20260831/mutate.py":
        (CLASS_RESEARCH, "sgidewidth pass-2 mutator (bit5collide)"),
    "artifacts/sgidewidth/opus_p2_20260831/mutate2.py":
        (CLASS_RESEARCH, "sgidewidth pass-2 mutator (bracegoto)"),
    "artifacts/sgidewidth/opus_p2_20260831/mutate3.py":
        (CLASS_RESEARCH, "sgidewidth pass-2 mutator (accept2 / skipans)"),
    "artifacts/sgidewidth/opus_p2_20260831/mutate4.py":
        (CLASS_RESEARCH, "sgidewidth pass-2 mutator (prefix -- the verbatim reinstatement, floor a+b, 14/25)"),

    #  sgidewidth, 2026-08-31.  The measuring seat's rung-3 witness, attribution probe and
    #  25-row / nine-build kill table, preserved because the seat reported them VOLATILE.
    #  CLASS_RESEARCH on the #497 precedent: EVIDENCE, not detectors the battery owes a run.
    #
    #  *** EVERY DRIVER HERE IS A `_frozen` COPY, AND THE NAMING IS THE POINT. ***  The
    #  carrier mandates a frozen copy for a comparison run -- editing a script a job is
    #  reading corrupts that run in bash, and re-reads it between runs in python.  These
    #  filenames make the obedience auditable rather than asserted.
    #
    #  `gxdew_mz_frozen.py` and `gxdew_mzp_frozen.py` are kept as a PAIR and must not be
    #  pruned to one: they differ only in the byte `#95` fills (0x00 vs 0xa5), and the pair
    #  is the control that showed a declined read returns a DETERMINISTIC value tracking
    #  that byte.  That is what retracted my claim that the early-return mutant's observable
    #  is nondeterministic -- keeping only one erases the attribution.
    "artifacts/sgidewidth/opus_witness_20260831/gxdew_probe_frozen.py":
        (CLASS_RESEARCH, "sgidewidth rung-3 WITNESS as measured -- 4/4 kills, liveness + device-signature controls"),
    "artifacts/sgidewidth/opus_witness_20260831/gxdew_probe2_frozen.py":
        (CLASS_RESEARCH, "sgidewidth attribution probe -- 24/24, offsets differing ONLY in bit 0x800"),
    "artifacts/sgidewidth/opus_witness_20260831/gxdew_kill_frozen.py":
        (CLASS_RESEARCH, "sgidewidth table-1 driver, frozen for the duration of the run"),
    "artifacts/sgidewidth/opus_witness_20260831/gxdew_kill2_frozen.py":
        (CLASS_RESEARCH, "sgidewidth table-2 driver (25 rows, 9 builds), frozen"),
    "artifacts/sgidewidth/opus_witness_20260831/gxdew_mutate2_frozen.py":
        (CLASS_RESEARCH, "sgidewidth mutator, frozen so a re-run cannot silently differ"),
    "artifacts/sgidewidth/opus_witness_20260831/gxdew_mr_frozen.py":
        (CLASS_RESEARCH, "sgidewidth mR variant builder -- the goto-to-common-exit shape, 25/25"),
    "artifacts/sgidewidth/opus_witness_20260831/gxdew_mz_frozen.py":
        (CLASS_RESEARCH, "sgidewidth #95 attribution builder -- fill 0x00, the control that refuted my retraction"),
    "artifacts/sgidewidth/opus_witness_20260831/gxdew_mzp_frozen.py":
        (CLASS_RESEARCH, "sgidewidth #95 attribution builder -- fill 0xa5, the paired control"),

    #  sgireunmapped, 2026-08-31.  The measuring seat's RUNG-3 WITNESS set, preserved
    #  because the seat reported its artifacts were in VOLATILE SCRATCH and would be lost.
    #  CLASS_RESEARCH on the #497 precedent above: EVIDENCE, not detectors the battery owes
    #  a run.
    #
    #  `sgi_re_unmapped_probe.py` is the WITNESS that licensed the fix -- 32/32 on an
    #  unmodified `-E sgi -e ip32`, with liveness, device-signature, neighbour-device and
    #  negative controls.  A witness exists BEFORE the edit and is graded by the witness
    #  clauses; a detector defends the fix afterwards and is graded by the vacuity floor.
    #  Filing this as research keeps that distinction rather than asking a gate to run a
    #  reproduction of a defect the round is about to remove.
    #
    #  `detector.py` is the seat's 14-row instrument AS MEASURED, and it is deliberately
    #  NOT the shipping detector: the round's own copy will live in regress/ and be gated.
    #  It is kept because a 9-variant table is worth nothing if the instrument that
    #  produced it can change underneath the numbers.
    #
    #  *** AND IT IS KEPT FOR A SECOND REASON THAT IS THE ROUND'S MOST TRANSFERABLE
    #  FINDING: this instrument contained a row that COULD NOT FAIL. ***  A latch mutant
    #  swept 14/14 against the row written to catch it, because gxprobe cached `pc` across
    #  `step` and the row's second access executed a nop.  The file as preserved is the
    #  BEFORE state, and `INSTRUMENT_FINDING.md` beside it is the diagnosis.  Deleting it
    #  would erase the only evidence of a vacuous row that eight of nine variants scored
    #  plausibly around.
    "artifacts/sgireunmapped/opus_witness_20260830/sgi_re_unmapped_probe.py":
        (CLASS_RESEARCH, "sgireunmapped RUNG-3 WITNESS as measured, 32/32 -- reproduction, not detector"),
    "artifacts/sgireunmapped/opus_witness_20260830/detector.py":
        (CLASS_RESEARCH, "sgireunmapped 14-row instrument AS MEASURED, incl. the row that could not fail"),
    "artifacts/sgireunmapped/opus_witness_20260830/mkvariant.py":
        (CLASS_RESEARCH, "sgireunmapped 9-variant mutator, preserved so the table can be re-run"),

    "artifacts/wdcaddtoinbufbound/rung3_20260830/addtoinbuf_rung3_probe.py":
        (CLASS_RESEARCH, "wdcaddtoinbufbound rung-3 witness probe, preserved as evidence"),
    "artifacts/wdcaddtoinbufbound/rung3_20260830/frozen_wave_20260830_102209.py":
        (CLASS_RESEARCH, "the FROZEN copy that run executed -- one instrument, provable"),
    "artifacts/wdcaddtoinbufbound/rung3_20260830/mkcd.py":
        (CLASS_RESEARCH, "builds the poisoned CD image the witness reads back"),
    "artifacts/wdcaddtoinbufbound/rung3_20260830/mkfix.py":
        (CLASS_RESEARCH, "applies the candidate fixes and clause-(d) mutants"),

    "artifacts/wdcaltoffset/opus_p2_20260830/mut494p2.py":
        (CLASS_RESEARCH, "#494 pass-2 mutant applier, preserved as evidence"),
    "artifacts/wdcaltoffset/opus_p2_20260830/q2_mechanism.py":
        (CLASS_RESEARCH, "#494 pass-2 return-0 mechanism measurement, evidence"),
    "artifacts/wdcaltoffset/opus_p2_20260830/PROPOSED_wdc_altoffset_4bit_probe.py":
        (CLASS_RESEARCH, "#494 pass-2 proposal for the shipped 4BIT detector"),

    "artifacts/wdcaltoffset/mutants_20260830/mkmutants.py":
        (CLASS_RESEARCH, "wdcaltoffset pass-1 mutant applier, preserved as evidence"),
    "artifacts/wdcaltoffset/mutants_20260830/table_a.py":
        (CLASS_RESEARCH, "wdcaltoffset pass-1 kill table (imports the witness probe)"),
    "artifacts/wdcaltoffset/mutants_20260830/table_b.py":
        (CLASS_RESEARCH, "wdcaltoffset read-side invariance table, preserved as evidence"),
    "artifacts/wdcaltoffset/mutants_20260830/table_c.py":
        (CLASS_RESEARCH, "wdcaltoffset ATAPI-signature table -- the only instrument that sees the m3 escape"),

    #  #471: THE NESTED FILES, now visible for the first time.  Keys are paths RELATIVE
    #  to regress/ -- top-level entries above stay bare basenames and are unaffected.
    #
    #  The detector is GATED (gate_sh_rounding.sh, #465).  The other two are the
    #  INSTRUMENTS preserved beside a kill table so its numbers can be re-run rather than
    #  merely believed -- the `preserveinstrument` rule.  They are EVIDENCE, not tests:
    #  owing them a gate would be demanding that an archive prove something.
    "artifacts/gdrompionull/gdrom_pio_null_probe.py":
        (CLASS_DETECTOR, "#465 gdrom PIO null-deref detector, run by gate_sh_rounding.sh"),
    "artifacts/gdrompionull/opus_p2_20260826/mism_probe.py":
        (CLASS_RESEARCH, "#465 pass-2 kill-table instrument, preserved as evidence"),
    "artifacts/gdrompionull/opus_p2_20260826/mutate.py":
        (CLASS_RESEARCH, "#465 pass-2 mutant applier, preserved as evidence"),
    "artifacts/wdccdbmidxfer/killtable2_20260827/mk477b.py":
        (CLASS_RESEARCH, "#477 pass-2 mutant applier, preserved as evidence"),
    "artifacts/wdcdataoutdrain/killtable_20260827/mk478.py":
        (CLASS_RESEARCH, "#478 mutant applier, preserved as evidence"),
    "artifacts/wdcdataoutdrain/killtable_20260827/drainvar.py":
        (CLASS_RESEARCH, "#478 fix-variant builder, preserved as evidence"),
    #  #490.  Four kill-table / measurement instruments and one HOOK CONTROL
    #  SUITE.  All five are EVIDENCE: they exist so a measurement can be
    #  re-run or audited, and none is owed a gate.
    #
    #  The seat that ran #490's supplementary pass predicted exactly this
    #  debt before the gate reported it, and noted it had renamed its own
    #  instrument off the `_probe.py` suffix -- which would otherwise have
    #  tripped the MISFILED rule.  Two of the five predate that seat.
    "artifacts/gdromexitsix/p2askagain_20260829/mut490p2.py":
        (CLASS_RESEARCH, "#490 ask-again mutant applier, preserved as evidence"),
    "artifacts/gdromexitsix/rot_20260829/probe.frozen.py":
        (CLASS_RESEARCH, "#490 rotted-packet instrument, frozen copy, evidence"),
    "artifacts/gdromexitsix/supp_p2_20260829/extend.py":
        (CLASS_RESEARCH, "#490 supplementary 22-row extender, evidence"),
    "artifacts/gdromexitsix/supp_p2_20260829/instrument_22row.frozen.py":
        (CLASS_RESEARCH, "#490 supplementary frozen instrument, evidence"),
    #  A control suite for a Claude-Code HOOK, not for emulator code -- so no
    #  emulator gate can run it.  Whether the harness should gate its own
    #  hook controls is FILED (`hookctlgate`), not answered here.
    "artifacts/makercfalse/hook_controls_20260829/hookctl.py":
        (CLASS_RESEARCH, "wsl-dollar hook control suite, 18 rows, evidence"),
    "artifacts/makercfalse/hook_controls_20260830/clusterctl.py":
        (CLASS_RESEARCH, "wsl-dollar hook CLUSTER controls, 11 rows -- 5 must fire, 6 must pass"),
    "artifacts/wdcdataoutdrain/killtable_20260827/addpkt.py":
        (CLASS_RESEARCH, "#478 detector row generator, preserved as evidence"),
    "artifacts/wdcdataoutdrain/killtable_20260827/addaccept.py":
        (CLASS_RESEARCH, "#478 accept-row generator, preserved as evidence"),
    "artifacts/wdcdataoutdrain/killtable_20260827/addlocal.py":
        (CLASS_RESEARCH, "#478 variant generator, preserved as evidence"),
    "artifacts/wdcdataoutdrain/killtable_20260827/addaltctl.py":
        (CLASS_RESEARCH, "#477 pass-2 accept-row generator, preserved as evidence"),
    "artifacts/wdcdataoutdrain/killtable_20260827/addannounce.py":
        (CLASS_RESEARCH, "#478 announce-row generator, preserved as evidence"),
    "artifacts/wdcdataoutdrain/killtable_20260827/addflush.py":
        (CLASS_RESEARCH, "#479 ring-flush repro generator, preserved as evidence"),
    "artifacts/wdcdataoutdrain/killtable_20260827/addp5.py":
        (CLASS_RESEARCH, "#479 premise-5 probe generator, preserved as evidence"),
    "artifacts/wdcdataoutdrain/killtable_20260827/addpartial.py":
        (CLASS_RESEARCH, "#478 partial-sector row generator, preserved as evidence"),
    "artifacts/wdcdataoutdrain/killtable_20260827/addphaserow.py":
        (CLASS_RESEARCH, "#477 pass-2 stale-phase row generator, preserved as evidence"),
    "artifacts/wdcdataoutdrain/killtable_20260827/wiprepro.py":
        (CLASS_RESEARCH, "#479 wdcwipclear repro generator, preserved as evidence"),
    "artifacts/wdccmdreset/killtable_20260827/mk479.py":
        (CLASS_RESEARCH, "#479 mutant applier, preserved as evidence"),
    "artifacts/wdccallsite/killtable_20260827/mk480.py":
        (CLASS_RESEARCH, "#480 call-site row generator, preserved as evidence"),
    "artifacts/wdcaltctrl/killtable_20260827/mkaltctrl.py":
        (CLASS_RESEARCH, "#481 ALT-CTRL reproduction generator, preserved as evidence"),
    "artifacts/wdcaltctrlcov/killtable_20260827/mk482.py":
        (CLASS_RESEARCH, "#482 tenant-isolation row generator, preserved as evidence"),
    "artifacts/wdcaltctrlfam/killtable_20260827/mk483.py":
        (CLASS_RESEARCH, "#483 orphan-ring/parity/sweep row generator, preserved as evidence"),
    "artifacts/wdcringambig/repro_20260827/author_repro484.py":
        (CLASS_RESEARCH, "#484 four-leg reproduction of the ring full/empty ambiguity, measured RED on ce75b1d before any edit"),
    "artifacts/wdcnoirq/repro_20260827/author_repro485.py":
        (CLASS_RESEARCH, "#485 256-opcode sweep of the ABRT-implies-assert invariant, measured RED on ed3f9cc before any edit"),
    "artifacts/wdcringambig/rung3_20260827/wdcring_rung3_probe.py":
        (CLASS_RESEARCH, "#484 rung-3 witness: a guest program on unmodified evbmips malta, both controls, 20/20 shipped-vs-fixed"),
    "artifacts/wdcfloodstale/measure_20260827/author_floodstale.py":
        (CLASS_RESEARCH, "three-leg measurement of wdcfloodstale: the death, a harness control, and the remedy"),
    "artifacts/wdcnoirq/killtable_20260827/author_mut485.py":
        (CLASS_RESEARCH, "#485 mutant applier: seven edits, four of which pass the sweep leg entirely"),
    "artifacts/wdcnoirq/killtable_20260827/author_rows485.py":
        (CLASS_RESEARCH, "#485 four-leg detector generator, each leg from a measured escape"),
    "artifacts/wdcnoirq/killtable_20260827/author_mut11.py":
        (CLASS_RESEARCH, "#485 pass-2: four representatives of the eleven measured escapes"),
    "artifacts/wdcnoirq/killtable_20260827/author_legs3.py":
        (CLASS_RESEARCH, "#485 pass-2: the three legs that close them -- task file, held level, ABRT"),
    "artifacts/wdcoddstep/overtaken_20260827/author_odd.py":
        (CLASS_RESEARCH, "the measurement that closed wdcoddstep as overtaken, with its clamp-removed control -- deliberately NOT shipped as a row"),
    "artifacts/wdcaltctrlfam/killtable_20260827/author_mut483.py":
        (CLASS_RESEARCH, "#483 mutant applier, author-prefixed after a seat overwrote an unprefixed one"),
    "artifacts/wdcaltctrlfam/killtable_20260827/author_fix483.py":
        (CLASS_RESEARCH, "#483 L1: the sweep's literal denominator, counted instead"),
    "artifacts/wdcaltctrlfam/killtable_20260827/author_fix483b.py":
        (CLASS_RESEARCH, "#483 L1: the orphan row's benign-control and small-ring legs"),
    "artifacts/wdcaltctrlfam/killtable_20260827/author_fix483c.py":
        (CLASS_RESEARCH, "#483 L1: the sweep asserts BOTH effects, not the latch alone"),
    "artifacts/wdcaltctrlcov/killtable_20260827/mut482_RECONSTRUCTED.py":
        (CLASS_RESEARCH, "#482 mutant applier, RECONSTRUCTED after a seat overwrote the original in the shared scratchpad; verified to reproduce the recorded table"),
    "artifacts/wdcaltctrl/killtable_20260827/fixaltctrl.py":
        (CLASS_RESEARCH, "#481 fix applier (A1+B4+C1), preserved as evidence"),
    "artifacts/wdcaltctrl/killtable_20260827/fixwarrant481.py":
        (CLASS_RESEARCH, "#481 L4: the B4 warrant corrected after measurement, evidence"),
    "artifacts/wdcaltctrl/killtable_20260827/rows481b.py":
        (CLASS_RESEARCH, "#481 post-panel row repairs, preserved as evidence"),
    "artifacts/wdcaltctrl/killtable_20260827/mutalt.py":
        (CLASS_RESEARCH, "#481 mutant applier, preserved as evidence"),
    "artifacts/wdcaltctrl/killtable_20260827/gatealt.py":
        (CLASS_RESEARCH, "#481 gate row-naming applier, preserved as evidence"),
    "artifacts/wdcaltctrl/killtable_20260827/gatealt2.py":
        (CLASS_RESEARCH, "#481 gate naming of the four missed rows, evidence"),
    "artifacts/wdccallsite/killtable_20260827/mk480b.py":
        (CLASS_RESEARCH, "#480 clause-(i)/(ii) row generator, preserved as evidence"),
    "artifacts/wdccallsite/killtable_20260827/mut480.py":
        (CLASS_RESEARCH, "#480 call-site mutant applier, preserved as evidence"),
    "artifacts/wdccallsite/killtable_20260827/mut480b.py":
        (CLASS_RESEARCH, "#480 full escape-set mutant applier, preserved as evidence"),
    "artifacts/wdccallsite/killtable_20260827/q3check.py":
        (CLASS_RESEARCH, "#480 fixture-liveness control, preserved as evidence"),
    "artifacts/wdccallsite/killtable_20260827/q4check.py":
        (CLASS_RESEARCH, "#480 detector-mutant applier (count-pin refutation), evidence"),
    "artifacts/wdccallsite/killtable_20260827/fixrows480.py":
        (CLASS_RESEARCH, "#480 row-construction repair, preserved as evidence"),
    "artifacts/wdccallsite/killtable_20260827/gatename480.py":
        (CLASS_RESEARCH, "#480 gate row-naming applier, preserved as evidence"),
    "artifacts/wdccmdreset/killtable_20260827/port479.py":
        (CLASS_RESEARCH, "#479 row-port generator, preserved as evidence"),
    "artifacts/wdccmdreset/killtable_20260827/add479rows.py":
        (CLASS_RESEARCH, "#479 mutant-required row generator, preserved as evidence"),
    "artifacts/wdccmdreset/killtable_20260827/fix479.py":
        (CLASS_RESEARCH, "#479 fix applier, preserved as evidence"),
    "artifacts/wdccmdreset/killtable_20260827/repin479.py":
        (CLASS_RESEARCH, "#479 oracle re-pin, preserved as evidence"),
    "artifacts/wdccmdreset/killtable_20260827/adddevctl.py":
        (CLASS_RESEARCH, "#479 devctl accept-row generator, preserved as evidence"),
    "artifacts/wdccmdreset/killtable_20260827/addle.py":
        (CLASS_RESEARCH, "#479 little-endian coverage generator, preserved as evidence"),
    "artifacts/wdccmdreset/killtable_20260827/addwm.py":
        (CLASS_RESEARCH, "#479 WRITEMULTI row generator, preserved as evidence"),
    "artifacts/wdccmdreset/killtable_20260827/addbadlencdb.py":
        (CLASS_RESEARCH, "#479 rejected-width row generator, preserved as evidence"),
    "artifacts/wdccmdreset/killtable_20260827/addmut479.py":
        (CLASS_RESEARCH, "#479 seat-named mutant generator, preserved as evidence"),
    #  CLASSIFIED WHILE ITS OWN ROUND WAS STILL IN THE INDEX, and that is the check working
    #  rather than an exception to it: this file was `git add`ed by a concurrent #446 round
    #  MINUTES after this checker was written, went straight into the domain, and was named
    #  UNCLASSIFIED on the first run.  Reading it settled both questions in under a minute --
    #  its own first line says "#446 DETECTOR", and gate_offline.sh:1815 really does run it,
    #  so it needs no exemption.  #446 wired its probe in the same commit as its fix.
    "sgi_eaddr_probe.py":          (CLASS_DETECTOR, "#446 SGI eaddr value oracle at arcbios_init"),
    "sh4_pcic_probe.py":           (CLASS_DETECTOR, "#443 sh4 PCIC exit sites"),
    "arcbios_shift_probe.py":      (CLASS_DETECTOR, "#450 arcbios exact-statement census"),
    "sh4_chcr_probe.py":           (CLASS_DETECTOR, "#448 sh4 CHCR field decoders"),
    "sh4_rtcsr_probe.py":          (CLASS_DETECTOR, "#449 sh4 RTCSR refresh-interrupt enables"),
    "sh4_rtcsr_witness.py":        (CLASS_WITNESS,  "#449 pre-fix symptom: a DELAYED host death"),
    "artifacts/shortread/round_20260827/shortread_witness.py": (CLASS_WITNESS,
                                    "#488 rung-3 on unmodified landisk: a guest READ SECTORS "
                                    "reads 0x0000 where the disk holds 'B','B' on the committed "
                                    "build AND on the rejected alternative, 0x4242 on the fix.  "
                                    "Not gated: it needs a hand-built truncated overlay (a "
                                    "200-byte data file plus a claiming .map) that no gate "
                                    "constructs, and a witness is checked for the ABSENCE of a "
                                    "gate call by design.  Preserved with all three transcripts."),
    "gdrom_toclen_probe.py":       (CLASS_DETECTOR,
                                    "#489 case 0x14 TOC length: a guest-supplied cnt is "
                                    "DECLINED with a latched (once) diagnostic instead of "
                                    "ending the host.  19 rows, gated in gate_sh_rounding.sh "
                                    "with a literal denominator pin.  Every value the guard "
                                    "refuses carries a DECLINE-CHANNEL row (bad/zero/over "
                                    "cond) and so does the latched STATE (latch cond) -- four "
                                    "measured escapes across three earlier row sets all had "
                                    "the same shape: a survive-only row is vacuous here."),
    "artifacts/wdcnoirq/witness_20260827/wdcnoirq_rung3_probe.py": (CLASS_WITNESS,
                                    "#485 rung-3 witness, PRESERVED INTO THE REPO 2026-08-28.  "
                                    "The ledger's witness field cited _scratchpad/witness485/ -- a "
                                    "volatile path -- and the files were still there, so this is a "
                                    "copy of a live witness rather than a reconstruction.  Its "
                                    "pre/post rows and transcripts sit beside it.  Ungated by "
                                    "design: a witness licenses a fix and is not a standing "
                                    "detector; #485's standing coverage is its kill table."),
    "artifacts/gdromexitsix/gdrom_toclen_witness.py": (CLASS_WITNESS,
                                    "gdromexitsix rung-3 on the unmodified dreamcast machine: "
                                    "nine guest accesses, cnt=407 and cnt=0 each end the host at "
                                    "the case 0x14 TOC length guard (exit1), while cnt=408 "
                                    "synthesizes a real TOC and survives.  MEASURED RED 8/8 on "
                                    "the committed build before any edit to the site.  Not "
                                    "gated, and a witness is checked for the ABSENCE of a gate "
                                    "call by design -- its badlen/zerolen rows INVERT the day "
                                    "the fix lands, so gating it manufactures a regression.  "
                                    "Preserved under artifacts/ because this row's previous TWO "
                                    "witnesses lived in a rotated scratchpad and no longer "
                                    "exist, which is why its witness field had to read `none`."),
    #  #496's DETECTOR, gated in gate_sh_rounding.sh.  It is the WITNESS's opposite number
    #  and the pair is worth reading together: the witness reads SURVIVAL and the detector is
    #  FORBIDDEN from reading it, because post-fix every one of these accesses exits 0.  Two
    #  files, opposite oracles, same defect -- which is why one is gated and one must not be.
    "gdrom_cond_probe.py":
        (CLASS_DETECTOR, "#496 GDROM_UNKNOWN_0x88 + GDROM_COND bad-value declines and the "
                         "d->cond store relocation -- 16 rows, keystone `R5 cond keep`"),

    #  gdromcondlies RUNG-3 WITNESS, 2026-08-30.  CLASS_WITNESS on the toclen precedent
    #  three entries up, and for the identical reason: its two kill rows INVERT the day
    #  the fix lands, so gating it would manufacture a regression.  The round's standing
    #  coverage is its own detector, which is a separate deliverable.
    "artifacts/gdromcondlies/witness_20260830/gdrom_cond_witness.py": (CLASS_WITNESS,
                                    "gdromcondlies rung-3 on the unmodified -E dreamcast: "
                                    "one guest mov.w per site ends the host at both live "
                                    "BADVAL exits (GDROM_UNKNOWN_0x88 != 0xb, GDROM_COND "
                                    "unmodelled), 15/15 on the committed build before any "
                                    "edit.  Carries BOTH mandatory controls plus two the "
                                    "ladder does not require and this result needs: a "
                                    "DEVICE-SIGNATURE row in the strong form (a "
                                    "TRANSFORMATION only the device performs -- the write "
                                    "arm masks to a byte, so 0x1234 to CNTLO reads back "
                                    "0x34, which RAM would not do), and ACCEPT rows.  The "
                                    "accept rows are what pin the defect to the VALUE and "
                                    "therefore to #443 BADVAL, rather than to the offset "
                                    "being unserviceable, which is the already-fixed #461 "
                                    "default-arm defect.  *** ITS ACCEPT ROWS MUST NOT BE "
                                    "CARRIED INTO THE DETECTOR UNCHANGED: they discriminate "
                                    "on SURVIVAL, and the fix makes survival universally "
                                    "green -- a survival oracle at a refusal-effect site is "
                                    "the CHANNEL check's canonical vacuous row.  Named by "
                                    "the fable5 seat on pass 1, before the detector existed."),
    #  #497 PASS 1, the opus5 seat, 2026-08-30.  CLASS_RESEARCH: these are EVIDENCE preserved
    #  so two measured escapes can be re-run rather than believed, not tests owed a gate.
    #
    #  They matter more than a usual artifacts drop because the seat DISCHARGED THE WITNESS
    #  OBLIGATION with them -- 26/26 across all six sites in both directions, where the round's
    #  original witness covered one site and stores only.  That settled a live scope
    #  disagreement between two seats by measurement instead of by argument.
    #
    #  `opus497_read_probe.py` is the re-aimed witness (its `lw` rows are the ones that expose
    #  the writeflag-conjunct escape); `latch_probe.py` drives two sites in ONE session, which
    #  is the only shape that can see a latch-bit collision; the three `apply_*.py` build the
    #  fix and the two mutants.
    "artifacts/widthkillclass/opus_p1_20260830/opus497_read_probe.py":
        (CLASS_RESEARCH, "#497 pass-1: the witness re-aimed to all six sites and BOTH "
                         "directions -- 26/26, discharging the per-site witness obligation"),
    "artifacts/widthkillclass/opus_p1_20260830/latch_probe.py":
        (CLASS_RESEARCH, "#497 pass-1: two sites in ONE session -- the only shape that can "
                         "observe a latch-bit collision"),
    "artifacts/widthkillclass/opus_p1_20260830/apply_fix.py":
        (CLASS_RESEARCH, "#497 pass-1: applies the candidate else-chained decline at all six "
                         "sites, preserved as evidence"),
    "artifacts/widthkillclass/opus_p1_20260830/apply_mutant.py":
        (CLASS_RESEARCH, "#497 pass-1: builds M1, the writeflag-conjunct escape"),
    "artifacts/widthkillclass/opus_p1_20260830/apply_m2.py":
        (CLASS_RESEARCH, "#497 pass-1: builds M2, the latch-bit collision"),

    #  widthkillclass RUNG-3 WITNESS, 2026-08-30, built by the agy seat -- a THIRD
    #  compile-and-measure front end, on a transport independent of the Agent tool.
    #  CLASS_WITNESS on the toclen/gdromcond precedent: its three kill rows INVERT the day
    #  that class is fixed, so gating it would manufacture a regression.
    #
    #  It matters beyond its own row because it is the FIRST witness this project has for
    #  the #337 class OUTSIDE dev_wdc.c: a guest choosing an ACCESS WIDTH ends the host, at
    #  three widths, on an unmodified `-E sgi -e ip32`, with an ACCEPT control (the legal
    #  8-byte store survives) pinning it to the WIDTH rather than to the offset being
    #  unserviceable.  `.earlier.py` is the prior draft, kept because two versions existed
    #  in /tmp and which one ran is a fact worth being able to check rather than recall.
    "artifacts/widthkillclass/witness_20260830/sgi_re_width_witness.py": (CLASS_WITNESS,
                                    "widthkillclass rung-3 on unmodified -E sgi -e ip32: a "
                                    "guest sw/sh/sb to CRIME_RE_TLB_A (0xb5001000) each ends "
                                    "the host at the len != 8 guard, 10/10, while the legal "
                                    "8-byte store survives.  Ungated by design -- its kill "
                                    "rows invert when the class is fixed."),
    "artifacts/widthkillclass/witness_20260830/sgi_re_width_witness.earlier.py":
        (CLASS_RESEARCH, "the earlier draft of that witness, preserved so which version ran "
                         "is checkable rather than remembered"),

    "artifacts/gdromcondlies/witness_20260830/gdrom_cond_extras.py": (CLASS_RESEARCH,
                                    "the flood measurement beside that witness, preserved as "
                                    "evidence: the two ALREADY-de-fatalised guest-drivable "
                                    "fatal() sites in the same device (the 0x88 READ arm, "
                                    "seven lines above site A in the same case, and the "
                                    "GDROM_STAT write arm) print 3 diagnostics on 3 accesses "
                                    "-- unlatched and unbounded.  Both Agent seats ruled on "
                                    "it independently on pass 1 and DISAGREED about scope, "
                                    "which is why the number is kept re-runnable rather than "
                                    "quoted: see the floodclass filing."),
    "sh4_sci_witness.py":          (CLASS_WITNESS,  "#451 pre-fix symptom: a clocked-in byte kills"),
    "sh4_sci_probe.py":            (CLASS_DETECTOR, "#451 SCI command byte declined, not fatal"),
    "sh4_tlbda2_witness.py":       (CLASS_WITNESS,  "#452 pre-fix symptom: one TLB da2 access kills"),
    "sh4_tlbda2_probe.py":         (CLASS_DETECTOR, "#452 TLB data array 2 declined, not fatal"),
    "sh4_chcr_witness.py":         (CLASS_WITNESS,  "#448 pre-fix symptom: TD=1 ends the host"),
    "sh4_val_probe.py":            (CLASS_DETECTOR, "#447 sh4 DEVICE_ACCESS value guards"),
    "sh4_val_witness.py":          (CLASS_WITNESS,  "#447 pre-fix symptom: the host dies"),
    "sh_halt_probe.py":            (CLASS_DETECTOR, "SH halt path"),
    "sh_intprio_probe.py":         (CLASS_DETECTOR, "#455 SH interrupt priority 0"),
    "sh_tlbmulti_probe.py":        (CLASS_DETECTOR, "#457 SH TLB multiple hit"),
    "sh_pclock_probe.py":          (CLASS_DETECTOR, "#459 SH pclock: declines instead of exit(1)"),
    "gdrom_data_probe.py":         (CLASS_DETECTOR, "#460 GDROM_DATA: four exits, no legal first touch"),
    "gdrom_default_probe.py":      (CLASS_DETECTOR, "#461 both default: arms + #462 the DMA+0x18 pair"),
    "asic_badaddr_probe.py":       (CLASS_DETECTOR, "#463 dreamcast_asic: one guest LOAD ended the host"),
    "wdc_flood_probe.py":          (CLASS_DETECTOR, "wdcflood dev_wdc.c: six unlatched fatal(), guest-drivable without bound"),
    "sh_iprbcd_probe.py":          (CLASS_DETECTOR, "#458 SH IPRB/IPRC/IPRA-RTC priority table"),
    "sh_rounding_probe.py":        (CLASS_DETECTOR, "SH FP rounding"),

    # -- detectors that NOTHING RUNS.  Each carries a dated exemption below. --------------
    #  pit8253's docstring line 1 calls it a "witness"; its rows assert the FIXED behaviour
    #  ("R1/R2 fail on the PRE-FIX build"), so by the green-once-fixed line it is a DETECTOR.
    #  This is the measured case that rules out classifying by self-label.
    "pit8253_latch_probe.py":      (CLASS_DETECTOR, "#439/#440 PIT latch + LSB/MSB selector"),
    "sh4_bsc_width_probe.py":      (CLASS_DETECTOR, "#441 BCR2/BCR3 non-16-bit access"),
    "fbpending_drain_probe.py":    (CLASS_DETECTOR, "#442 footbridge pending-tick backlog"),
    "hpcmips_ctor_probe.py":       (CLASS_DETECTOR, "#444 every hpcmips subtype constructs"),

    # -- witnesses.  RED once the fix lands, so gating one manufactures a regression. -----
    "fbpending_witness.py":        (CLASS_WITNESS, "#442 pre-fix: the clock stops 42.9s in 85.9s"),
    "hpcabort_witness.py":         (CLASS_WITNESS, "#444 pre-fix: 3 of 8 subtypes SIGABRT"),
    "sh4pcic_witness.py":          (CLASS_WITNESS, "#443 pre-fix: guest loads end the host"),

    # -- tools: apparatus and libraries, not assertions about the emulator ----------------
    "drive_guest.py":              (CLASS_TOOL, "the pty driver library every rig probe imports"),

    #  landiskaux's preserved census: MEASUREMENT INSTRUMENTS, not detectors and not
    #  witnesses.  They produced the twelve-write histogram the row's warrant rests on, and
    #  they are committed because that warrant previously lived in `_scratchpad/` -- the same
    #  volatile path that already destroyed BOTH of gdromexitsix's witnesses.  Preserving an
    #  instrument is not the same as gating it: none of these asserts anything, so gating one
    #  would pin nothing.
    #  #489's mutant applier, preserved beside its kill table.  A TOOL: it asserts nothing
    #  and pins nothing -- it edits one guard predicate into one of three named forms.  It is
    #  committed because the three mutants it applies FAILED to apply in table 4 (their
    #  anchors were built through a bash->heredoc->python chain and one backslash level was
    #  consumed), and this file is the repair: a real file with no shell in between, spelling
    #  its tabs as chr(9).  Preserving it makes the table re-runnable.
    "artifacts/gdromexitsix/killtable4_20260828/mut_common.py": (CLASS_TOOL, "#489 mutant applier: rewrites the case 0x14 guard predicate, no escaping chain"),
    "gdrom_decline_probe.py":      (CLASS_DETECTOR,
                                    "#490: the two de-fatalised sites in handle_command -- "
                                    "case 0x30's data-format guard and the default: arm.  20 "
                                    "rows in gate_sh_rounding.sh's gdromdecline section with "
                                    "its OWN denominator, deliberately not bolted onto the "
                                    "60-row gdrom_default list.  (This entry said 19 and 58; "
                                    "both were wrong -- 19 is the TOCLEN probe's count, copied "
                                    "in, and gdrom_default grew to 60 in this same round.  "
                                    "DERIVERS, because they differ per file: the decline probe "
                                    "is `grep -c '^row('` = 20, which agrees with its measured "
                                    "GDROM_DECL_RESULT=20/20.  **gdrom_default has NO sound "
                                    "static deriver** -- `^row(` gives 52 and any-`row(` gives "
                                    "55, because some rows are emitted from loops, so the "
                                    "MEASURED GDROM_DEF_RESULT=60/60 is the only authority.  "
                                    "A future reader counting row() by grep will get 52 and be "
                                    "wrong.)  Three of its rows exist "
                                    "because a measuring seat BUILT the escapes: `crossbit` "
                                    "(a latch bit aliasing one of the eight others sharing "
                                    "d->warned, six of which ordinary register reads set), "
                                    "`latch cond` (the break slipping inside the latch if, "
                                    "which the announce count cannot see), and `both sites` "
                                    "(one bit for two sites)."),
    "artifacts/gdromexitsix/opus_r2full_20260828/mkfix.py": (CLASS_TOOL,
                                    "#490 R2 pass 1: applies the candidate two-site fix to a "
                                    "scratch clone.  The baseline every escape below is "
                                    "measured RELATIVE TO."),
    "artifacts/gdromexitsix/opus_r2full_20260828/mkmut3.py": (CLASS_TOOL,
                                    "#490 R2 pass 1: builds M_retA / Ma_toclen / Mb_toclen / "
                                    "M_growA / M_growB over the fix, one minimal edit each.  "
                                    "Ma_toclen and Mb_toclen ESCAPED the committed 13-row "
                                    "plan -- a latch-bit collision with GDROM_W_TOCLEN that "
                                    "silences a whole site's diagnostic."),
    "artifacts/gdromexitsix/opus_r2full_20260828/mkmut_brace.py": (CLASS_TOOL,
                                    "#490 R2 pass 1: the brace slip -- Site A's `break` moved "
                                    "inside the latch `if`, so the SECOND identical bad format "
                                    "falls through into sector_nr.  ESCAPED the committed plan; "
                                    "`fmt x2` reads 1 either way.  Kept separate from mkmut3 "
                                    "because it is the mutant #489's own probe header records "
                                    "sweeping an 18-row detector clean at the sibling arm."),
    "artifacts/gdromexitsix/opus_r2full_20260828/tprobe3.py": (CLASS_TOOL,
                                    "#490 R2 pass 1: the measuring seat's probe -- eight "
                                    "sessions reading CNT / COND / EVT32 / rej / huh / the "
                                    "per-site decline counts, with session selection.  Ungated "
                                    "by design: a research instrument, not a standing detector; "
                                    "the rows it justifies land in the shipped probes."),
    "artifacts/gdromexitsix/asan_m0_20260828/apply_m0.py": (CLASS_TOOL,
                                    "#489 M0 applier: deletes the cnt!=408 guard for the ASAN "
                                    "run that turned the round's headline claim from DERIVED "
                                    "into MEASURED (7 heap-buffer-overflow WRITEs).  Preserved "
                                    "because the measurement is meaningless without the exact "
                                    "edit that produced it.  Written as a REAL FILE using "
                                    "chr(92) after a nested-heredoc chain ate the anchor's "
                                    "backslash -- it REFUSED with count=0 rather than mutating "
                                    "nothing, which is the failure mode worth keeping."),
    "artifacts/gdromexitsix/opus_r2table_20260828/mkfix.py": (CLASS_TOOL,
                                    "#490 R2: applies the CANDIDATE product fix (both sites "
                                    "de-fatalised) to a scratch clone.  Preserved because the "
                                    "measured table's every number is relative to the tree it "
                                    "builds -- without it the scores name no baseline."),
    "artifacts/gdromexitsix/opus_r2table_20260828/mkmut.py": (CLASS_TOOL,
                                    "#490 R2: builds the six mutants (M1ret, M2nolatch, "
                                    "M3shared, M4nobreakA, M5outerA, M6cond) as single minimal "
                                    "edits over the fix.  This is the file that makes the table "
                                    "REPRODUCIBLE rather than merely reported."),
    "artifacts/gdromexitsix/opus_r2table_20260828/tprobe2.py": (CLASS_TOOL,
                                    "#490 R2: the measuring seat's own probe -- eight sessions, "
                                    "reading COND / CNT / EVT32 / the two decline diagnostics, "
                                    "with SESSION SELECTION and negative controls in both "
                                    "directions (unknown token rc=2, bare prefix rc=2).  Ungated "
                                    "by design: it is a research instrument, not a standing "
                                    "detector, and the rows it justifies live in "
                                    "gdrom_default_probe.py."),
    "artifacts/landiskaux/census_20260827/census.py":       (CLASS_TOOL, "landiskaux census: tallies guest accesses per paddr from a hooked build"),
    "artifacts/landiskaux/census_20260827/analyse_hook.py": (CLASS_TOOL, "landiskaux census: reduces the hook log to the per-address table"),
    "artifacts/landiskaux/census_20260827/devlist.py":      (CLASS_TOOL, "landiskaux census: dumps the constructed machine's device list"),
    "artifacts/landiskaux/census_20260827/mk_censusB.py":   (CLASS_TOOL, "landiskaux census: builds the instrumented tree B"),
    "artifacts/landiskaux/census_20260827/watch_2c.py":     (CLASS_TOOL, "landiskaux census: write-watchpoint on 0x1400002c"),
    "selfmutant.py":               (CLASS_TOOL, "differential mutation harness; gate 2 drives it"),
    "absorb_census.py":            (CLASS_TOOL,
                                    "measures selftest_absorb.py's KILL RATE by hand over 22 "
                                    "rebuilt mutants. The gated artefact is selftest_absorb.py; "
                                    "this grades that detector and is not one itself."),
}

#  DATED, NAMED DEBT -- not a count and not a silent allowlist.  gate_offline.sh MEASURED that
#  a COUNT pin actively obstructs the shrink it claims to want ("6, shrinking not growing" went
#  RED at 5).  A date expires; shrinking is green by construction.
#
#  2026-09-20 matches the fbpending_bound:2026-09-20 deadline already standing in
#  gate_offline.sh's SM_EXEMPT, so #442's two debts fall due together.  IT IS A PROPOSAL: the
#  owner set the SM dates and set them TIGHTER than the ones proposed, and a deadline nobody
#  chose is a deadline nobody owns.
#
#  These are wiring jobs, not design ones -- each probe already prints a verdict token and
#  exits nonzero on failure.  What each needs is a gate that owns it, its rig preconditions,
#  and ONE clean gate run proving it green before it ships.  That last part is why they are
#  exempted here rather than wired here: gate_hygiene's own comments record FOUR probes that
#  shipped latently RED because the commit that added them never fired the gate.
EXEMPT = {
    #  pit8253_latch_probe.py's exemption is DISCHARGED, 2026-08-30 -- it is now wired into
    #  gate_arm.sh beside footbridge_sites_probe.py, which is the home gate_hygiene.sh's own
    #  bump note named for it ("wants an operator who can run that gate").  The entry is
    #  DELETED rather than dated forward, in the SAME edit that added the wiring, because a
    #  wired probe that keeps an exemption is a STALE EXEMPTION and this checker reds on it.
    #  Seven exemptions remain.
    #  sh4_bsc_width_probe.py's exemption is DISCHARGED, 2026-08-30 -- wired into
    #  gate_sh_rounding.sh, whose `-E landisk` machine it already used.  Deleted in the
    #  SAME edit as the wiring, because a wired probe that keeps an exemption is a
    #  STALE EXEMPTION.  Six exemptions remain.
    "fbpending_drain_probe.py": ("2026-09-20",
                                 "REPORT-ONLY by default: EXPECT_CAP must be set before a "
                                 "gate row can mean anything, so wiring is a design step first"),
    "hpcmips_ctor_probe.py":    ("2026-09-20",
                                 "rung 2, ~8 s, no rig image -- wants a construction gate"),
    #  Both #494 probes are TWO-LEG DIFFERENTIALS: they take a PRE-FIX binary and
    #  a post-fix one and compare.  No gate builds a second leg, so wiring them is
    #  a change to the instrument -- a single-leg mode asserting only the fix-side
    #  wants against the gate's own binary -- not a line in a gate script.
    "wdc_altoffset_probe.py":     ("2026-09-20",
                                   "two-leg differential; wants a single-leg mode "
                                   "before gate 10 can assert anything"),
    "wdc_altoffset_sig_probe.py": ("2026-09-20",
                                   "two-leg differential AND needs a ciR: CD-ROM rig "
                                   "the battery does not build today"),
    "wdc_altoffset_4bit_probe.py": ("2026-09-20",
                                    "two-leg differential; shares the single-leg-mode "
                                    "debt with its two siblings"),
    "wdc_addtoinbuf_probe.py":     ("2026-09-20",
                                    "two-leg differential AND needs a poisoned CD "
                                    "image the battery does not build"),
    #  #520's detector.  NOT a two-leg differential and not awaiting a design -- it is a
    #  single-leg 15-row instrument that runs green on the fix today.  What it lacks is a
    #  HOME: no gate in this tree runs an Alpha machine at all.  Dated to fall due with
    #  the others so the cliff stays one date rather than becoming a rolling excuse.
    #  #521's detector.  Single-leg, fast, green on the fix -- it lacks a HOME, not a design:
    #  the only gate on this CPU family drives luna88k, not mvme88k/mvme187.  Dated to fall
    #  due with the others so the cliff stays one date rather than a rolling excuse.
    #  #522's detector.  Single-leg, 0.2 s, green on the fix.  It lacks a gate that RUNS a
    #  64-bit PowerPC CPU: gate 9 constructs them but has no result oracle, and both PowerPC
    #  gates drive a 32-bit part.  Closing that is a harness round, filed to wiringcliff.
    "ppc_rldicl_probe.py":         ("2026-09-20",
                                    "no gate EXECUTES a 64-bit PowerPC CPU -- gate 9 "
                                    "constructs them with no result oracle; gate_ppc.sh "
                                    "is the named home, filed to wiringcliff"),
    "mk48_nvram_probe.py":         ("2026-09-20",
                                    "no gate drives mvme88k/mvme187; gate_m88k_rounding.sh "
                                    "is the named home and giving it an mvme187 leg is a "
                                    "harness round, filed to wiringcliff"),
    "alpha_tbi_probe.py":          ("2026-09-20",
                                    "no gate runs an Alpha machine; gate_crossfamily.sh "
                                    "is the named home and giving it one is a harness "
                                    "round, filed to wiringcliff"),
}

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


#  *** A PYTHON DICT LITERAL ACCEPTS A DUPLICATE KEY IN SILENCE, AND THE LAST ONE WINS.
#  MEASURED ON THIS FILE, HOURS AFTER IT WAS WRITTEN. ***
#
#  Two rounds added `sgi_eaddr_probe.py` to MANIFEST independently -- the author of this
#  checker, and the #446 round whose probe it was.  Both landed, four lines apart, and
#  `len(MANIFEST)` reported ONE entry.  Nothing complained, because nothing can: by the
#  time the module object exists the earlier entry is already gone.  Here the two agreed
#  on CLASS, so the behaviour was identical and the only damage was a stale line.  Had
#  they disagreed -- one DETECTOR, one TOOL -- the file would have carried a visible,
#  reviewed, *tracked* classification that the checker silently did not use, and the
#  filename tooth that refuses `*_probe.py` in class `tool` would have been reading the
#  wrong entry while looking correct in the diff.
#
#  It has to be caught by re-reading THIS FILE'S SOURCE TEXT, because the data structure
#  cannot represent the fault it suffers from.  A duplicate is a SETUP FAULT, not a
#  finding: it exits before any wiring is derived, so it can never be confused with a
#  probe that is genuinely unwired.
#  The open() is INLINE rather than a call to read() below: this guard runs at import time,
#  fifty lines before read() is defined, and the first draft died with a NameError proving it.
#  It failed loudly, which is luck -- a guard placed in a branch would have failed silently.
def _refuse_duplicate_keys():
    with open(os.path.abspath(__file__), "r", encoding="utf-8", errors="replace") as fh:
        src = fh.read()
    #  *** AN ANCHOR THAT NO LONGER MATCHES IS ITSELF A SETUP FAULT, NOT A REASON TO SKIP,
    #  AND THE FIRST VERSION OF THIS GUARD DID `continue`. ***  A flagship review MEASURED
    #  the consequence: `MANIFEST =  {` -- one extra space, valid Python, invisible to a
    #  reader -- makes a literal find() miss, the guard skips, and a planted duplicate key
    #  runs GREEN.  That is this file's own thesis turned on itself: a fault in a guard does
    #  not fail loudly, it stops guarding.  The regex tolerates whitespace, and a miss is
    #  now reported rather than shrugged at.
    for name in ("MANIFEST", "EXEMPT"):
        m = re.search(r"^%s\s*=\s*\{" % re.escape(name), src, re.M)
        if m is None:
            print("PROBEWIRING_SETUP_FAULT  the %s literal could not be located in this"
                  " file's own source." % name)
            print("  The duplicate-key guard cannot run, and a duplicate would pass"
                  " UNSEEN.  Fix the anchor, do not delete the check.")
            sys.exit(2)
        i = m.start()
        j = src.find("\n}", i)
        seen, dupes = set(), []
        for k in re.findall(r'^\s*"([^"]+)"\s*:', src[i:j], re.M):
            (dupes.append(k) if k in seen else None)
            seen.add(k)
        if dupes:
            print("PROBEWIRING_SETUP_FAULT  %s names the same key twice; a dict literal" % name)
            print("  keeps only the LAST and says nothing.  Delete the stale line(s):")
            for k in sorted(set(dupes)):
                print("    %s" % k)
            sys.exit(2)


_refuse_duplicate_keys()

#  A python interpreter token.  Bare python/python3, or the $PY-style indirections other
#  harnesses in this tree use.  Anchored so python3.12 and mypython do not match.
#  *** THE TRAILING BOUNDARY IS LOAD-BEARING AND THE FIRST VERSION LACKED IT. ***  A
#  flagship review MEASURED that `"$PYLINT" probe.py` scored as WIRING: the alternation
#  had no boundary after the group, so ANY $PY-prefixed variable read as an interpreter
#  and a linter invocation would have marked a probe wired.  That is the FALSE ACCEPT
#  direction -- the one that silently stops demanding a gate.  Latent rather than live:
#  no such variable exists in the battery today.  `$PYTHON` and `$PY` still match;
#  `$PYLINT` and `$PYTEST` no longer do.
INTERP_RE = re.compile(
    r'"?\$\{?(?:PY|PY3|PYTHON|PYTHON3)\}?"?(?![A-Za-z0-9_])'
    r'|(?<![\w./-])python3?(?![\w.-])'
)

#  COMMAND POSITION -- the whole defence against "a mention counts as wiring".  Everything
#  before the interpreter must be shell scaffolding: leading space, an assignment opening a
#  command substitution (out=$( ), control keywords, and environment-variable prefixes.
#
#  THE LINE THIS WAS BUILT AGAINST IS REAL AND LIVE, not invented:
#      gate_hygiene.sh:331   note "diag_div_sweep.py or python3 missing -- class ratchet NOT run"
#  It carries a probe basename AND the token python3 on one non-comment line, and it is a
#  message saying the probe DID NOT RUN.  A two-sided "name near python" regex scores it as
#  execution.  Here the interpreter's prefix is `note "diag_div_sweep.py or `, which is not
#  scaffolding, so the line is rejected.
CMDPOS_RE = re.compile(
    r"""^\s*
        (?: [A-Za-z_]\w* = (?:\$\()? \s* )?
        (?: (?: if | then | else | elif | while | until | do | ! | \$\( | \( ) \s* )*
        (?: [A-Za-z_]\w* = (?: "[^"]*" | '[^']*' | \S* ) \s+ )*
        $""",
    re.X,
)

VAR_RE = re.compile(r"^\$\{?([A-Za-z_]\w*)\}?$")
ASSIGN_RE = re.compile(r"^\s*([A-Za-z_]\w*)=(\S+)")


def read(path):
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


def unquote(tok):
    tok = tok.strip().rstrip(");,")
    if len(tok) >= 2 and tok[0] == tok[-1] and tok[0] in "\"'":
        tok = tok[1:-1]
    return tok.strip("\"'")


def gate_list(regress):
    """The battery's OWN array is the authority on which scripts run.

    Deriving from run.sh rather than from a gate_*.sh glob is deliberate, and carries a
    second-order property worth having: a gate script that exists but was dropped out of
    GATES does not run, so every probe it owned becomes unwired here and this goes RED.
    A glob would have called those probes gated forever.
    """
    run = os.path.join(regress, "run.sh")
    if not os.path.isfile(run):
        return None, "regress/run.sh is missing -- cannot tell which gates run"
    m = re.search(r"^GATES=\(([^)]*)\)", read(run), re.M)
    if not m:
        return None, "regress/run.sh has no GATES=( ... ) array -- cannot derive the battery"
    return [n + ".sh" for n in m.group(1).split()], None


def exec_sites(regress, scripts):
    """Return (hits, ignored, missing).

    hits[basename] = ["gate_arm.sh:97", ...]  -- a real invocation of the regress copy
    ignored        = ["gate_offline.sh:153  $ACDIR/selftest_absorb.py", ...]
    """
    hits, ignored, missing = {}, [], []
    for script in scripts:
        path = os.path.join(regress, script)
        if not os.path.isfile(path):
            missing.append(script)
            continue
        lines = read(path).splitlines()
        #  One-level variable map, from this file only.  gate_hygiene really does write
        #  DIVSWEEP=$HERE/diag_div_sweep.py and then run "$DIVSWEEP", so refusing to resolve
        #  one level would report a genuinely gated probe as unwired -- and a false red is
        #  how a rule gets switched off.
        varmap = {}
        for ln in lines:
            if ln.lstrip().startswith("#"):
                continue
            a = ASSIGN_RE.match(ln)
            if a and ".py" in a.group(2):
                varmap[a.group(1)] = unquote(a.group(2))
        #  *** HEREDOC BODIES ARE NOT CODE, AND COUNTING THEM IS A FALSE ACCEPT. ***  A
        #  flagship review MEASURED it: an invocation-shaped line inside a
        #  `cat <<'USAGE' ... USAGE` body scored as WIRING, so with the exemption removed
        #  the checker printed GREEN over a genuinely unwired detector.  Usage text quoting
        #  its own invocation is an entirely natural shape.  Latent rather than live -- every
        #  `<<` site in the battery today is a data table or a python program body, none
        #  carrying an interpreter plus a probe in body position -- but this is the
        #  dangerous direction: it does not fail loudly, it stops demanding a gate.
        #
        #  Skipping is the CONSERVATIVE choice and it has a cost worth naming: a heredoc
        #  that GENERATES a script the gate then runs is genuine wiring one level away, and
        #  skipping the body reports it UNWIRED -- a false red, which a human then reads.
        #  That is the right error to make.
        body = set()
        pend = None
        for no, ln in enumerate(lines, 1):
            if pend is not None:
                body.add(no)
                if ln.strip() == pend:
                    pend = None
                continue
            h = re.search(r"<<-?\s*[\"']?([A-Za-z_][A-Za-z0-9_]*)[\"']?", ln)
            if h and not ln.lstrip().startswith("#"):
                pend = h.group(1)

        for no, ln in enumerate(lines, 1):
            if ln.lstrip().startswith("#") or no in body:
                continue
            for m in INTERP_RE.finditer(ln):
                if not CMDPOS_RE.match(ln[: m.start()]):
                    continue
                toks = ln[m.end():].split()
                if toks and toks[0].startswith("-c"):
                    continue          # an inline program, not a script invocation
                for tok in toks:
                    t = unquote(tok)
                    v = VAR_RE.match(t)
                    if v:
                        t = varmap.get(v.group(1), "")
                    if not t.endswith(".py"):
                        continue
                    d, b = os.path.split(t)
                    if d in HERE_DIRS:
                        hits.setdefault(b, []).append("%s:%d" % (script, no))
                    else:
                        #  #471: a NESTED invocation is keyed by its RELATIVE PATH, not
                        #  its basename.  Before this, a gate invoking
                        #  `artifacts/.../gdrom_pio_null_probe.py` was filed as an
                        #  EXTERNAL reference and IGNORED -- so the detector #465 wired
                        #  by hand still reported UNWIRED once the scan could see it.
                        #
                        #  Path keys are also what makes the re-key SAFE: two detectors
                        #  sharing a basename in different directories stay distinct,
                        #  where basename keys would mark BOTH gated when only one is.
                        rel = os.path.normpath(os.path.join(d, b)).replace(os.sep, "/")
                        if os.path.isfile(os.path.join(regress, rel)):
                            hits.setdefault(rel, []).append("%s:%d" % (script, no))
                        else:
                            ignored.append("%s:%d  %s" % (script, no, t))
                    break             # the first .py argument is the script
    return hits, ignored, missing


#  STANDALONE WORDS ONLY.  The first draft used a plain substring and reported
#  mips_fold_probe.py as self-labelled "witness" -- its summary line reads "the MIPS
#  fold-witness COUNTERS", where the word names a counter, not the artefact.  That is the
#  substring trap in the one place in this file that was allowed to be a heuristic, and an
#  advisory that cries wolf is an advisory nobody reads.  MEASURED: with the hyphen guard
#  the noise line disappears and pit8253's real disagreement still fires.
_LBL_W = re.compile(r"(?<![\w-])witness(?![\w-])", re.I)
_LBL_D = re.compile(r"(?<![\w-])detector(?![\w-])", re.I)


def domain(regress):
    """The .py artefacts this check governs, and (mode, why) describing how it decided.

    *** COMMITTED-OR-STAGED, NOT "ON DISK", AND THE FIRST VERSION HAD IT WRONG. ***  The
    first draft enumerated the directory, and MINUTES AFTER IT WAS WRITTEN a concurrent
    round dropped `sgi_eaddr_probe.py` into regress/ as untracked in-flight work.  This
    check went red -- correctly identifying a real unwired detector, but firing at a
    file its author had not yet offered for commit, in someone else's working tree.

    `git ls-files` reads the INDEX, so a probe enters the domain the moment it is `git
    add`ed -- which is precisely when "every COMMITTED detector" starts to apply, and
    precisely when the author is present to classify it.  A scratch probe that is never
    staged defends nothing in a fresh clone either, so it is honestly out of scope.

    FALLBACK IS ANNOUNCED, NEVER SILENT.  Outside a work tree (the --selftest copies)
    git cannot answer, and a fallback that quietly changes what a check governs is the
    kind of silent scope change this harness keeps being bitten by.  So the mode is
    printed on the summary line.
    """
    try:
        p = subprocess.run(["git", "ls-files", "--", "*.py"], cwd=regress,
                           capture_output=True, text=True)
        if p.returncode == 0:
            #  #471: NO `"/" not in f` FILTER.  Its docstring always claimed "every
            #  committed DETECTOR under regress/", and the filter made that false --
            #  the checker could not see below top level, which is exactly where
            #  #465 shipped a detector that no gate ran.
            #
            #  `git ls-files` yields paths RELATIVE to regress/, so a top-level file
            #  still arrives as a bare basename and every existing MANIFEST key keeps
            #  matching unchanged.  Only nested files gain a path key.
            files = sorted(f for f in p.stdout.split()
                           if f.endswith(".py")
                           and os.path.isfile(os.path.join(regress, f)))
            if files:
                return files, "tracked-or-staged"
    except OSError:
        pass
    #  #471: the FALLBACK must descend too.  Leaving it flat would re-create the blind
    #  spot on any machine where git cannot answer -- a check whose coverage depends
    #  on which branch it took is the shape this file exists to refuse.
    found = []
    for dirpath, dirnames, filenames in os.walk(regress):
        dirnames[:] = [d for d in dirnames if d not in (".git", "__pycache__")]
        for f in filenames:
            if f.endswith(".py"):
                rel = os.path.relpath(os.path.join(dirpath, f), regress)
                found.append(rel.replace(os.sep, "/"))
    return sorted(found), "on-disk (git could not answer)"


def self_label(path):
    """The file's OWN summary line, for the SELFLABEL advisory only.  Never a verdict."""
    try:
        head = read(path).splitlines()[:6]
    except OSError:
        return None
    for ln in head:
        has_w, has_d = bool(_LBL_W.search(ln)), bool(_LBL_D.search(ln))
        if has_w and not has_d:
            return CLASS_WITNESS
        if has_d and not has_w:
            return CLASS_DETECTOR
        if has_w and has_d:
            return None
    return None


#  =======================================================================================
#  SELFTEST.  Mutants are applied to COPIES in a temp dir; nothing in the repository is
#  touched, so no .MUTANT sentinel is needed.  EXIT STATUS IS TAKEN FROM THE PROCESS: this
#  project lost a whole battery result to `cmd | tail`, which reports tail's status, so a
#  KILLED run read as exit 0.  subprocess.run(...).returncode cannot make that mistake.
#
#  A CHECKER-SOURCE MUTANT THAT DOES NOT APPLY EXACTLY ONCE IS A FAULT, NEVER A PASS --
#  absorb_census.py's rule, and it is what keeps this selftest from silently going vacuous
#  after someone reformats the manifest below.
#
#  *** AND IT FIRED ON ITS OWN AUTHOR, FIRST RUN. ***  The mutants below started life as
#  plain string literals, which meant the text they searched for existed TWICE in this file:
#  once in the manifest and once in the selftest.  _st_apply refused ("x2 ... want 1") rather
#  than mutating both, which would have silently mutated the selftest instead of the subject.
#  So every mutant target is BUILT from its parts and never written out whole.
def _lit(*parts):
    """Join fragments, so the assembled search string appears nowhere in this source."""
    return "".join(parts)


def _exline(key):
    """The EXEMPT entry for `key` AS IT APPEARS IN THE SOURCE, whole, however many lines.

    *** THIS USED TO REBUILD A ONE-LINE ENTRY FROM THE TABLE, AND THAT WAS WRONG FOR EVERY
    ENTRY THAT WRAPS. ***  Measured 2026-08-30, the day the second exemption was discharged:
    of the six then remaining, the reconstruction matched **zero** -- all six are written
    across two or more lines.  So the selftest's four exemption mutants had nothing to bite
    on and its SKIP arm fired, dropping 4 of 21 mutants.

    **That is the worse failure of the two, because the SKIP arm reads as "the EXEMPT table
    is empty, nothing to test" when the truth was "the reconstruction is too narrow".**  A
    check quietly getting weaker while reporting PASS is the shape this project names first,
    and here it would have arrived wearing the clothes of progress.

    Extracting the REAL text instead of rebuilding an idealised one removes the whole class:
    it cannot disagree with the source, because it IS the source.  Scans from the key to the
    line that closes the tuple, so single-line and wrapped entries are handled identically.
    *** AND THE SEARCH IS ANCHORED INSIDE THE EXEMPT BLOCK, WHICH IS NOT A DETAIL. ***
    `    "<name>":` appears in BOTH tables -- MANIFEST first, EXEMPT second -- so a bare
    `find()` returns the MANIFEST entry and the mutant deletes the wrong one.  Measured: M1
    and M2 then reported `UNCLASSIFIED ... is not in the MANIFEST` and `ORPHAN EXEMPTION`
    instead of the `UNWIRED DETECTOR` they exist to prove, i.e. the mutant reddened for a
    reason unrelated to the rule under test -- which would have looked like a working check.

    This is the wrong-section trap this project already records for gate row lists: anchor on
    something that identifies the SECTION, never on a pattern several sections share.
    """
    src = src_of_self()
    block = src.find("EXEMPT = {")
    if block < 0:
        raise RuntimeError("_exline: no EXEMPT block")
    start = src.find('    "%s":' % key, block)
    if start < 0:
        raise RuntimeError("_exline: %r not in EXEMPT" % key)
    i = start
    while i < len(src):
        nl = src.find("\n", i)
        if nl < 0:
            return ""
        line = src[i:nl + 1]
        if line.rstrip().endswith("),"):
            return src[start:nl + 1]
        i = nl + 1
    raise RuntimeError("_exline: unterminated entry for %r" % key)


def src_of_self():
    with open(__file__, encoding="utf-8", newline="") as _f:
        return _f.read()


def _pick_exempt_detector():
    """The selftest's exemplar is DERIVED, never hardcoded.

    *** THIS FUNCTION EXISTS BECAUSE THE SELFTEST BROKE THE DAY AN EXEMPTION WAS
    DISCHARGED, WHICH IS THE ONE EVENT IT SHOULD HAVE BEEN CELEBRATING. ***  Four of its
    mutants named `pit8253_latch_probe.py` literally.  When that probe was wired into
    gate_arm.sh and its exemption deleted -- exactly the outcome the EXEMPT table exists
    to drive toward -- three mutants raised KeyError on the missing entry and the fourth
    had its premise inverted.  `precommit_check.sh` reported THE PROBE-WIRING CHECKER CAN
    NO LONGER BE SHOWN TO FAIL, correctly.

    So the harness punished progress: doing the right thing to the tree broke the tool
    that asks for it.  A hardcoded exemplar is a frozen claim about a table designed to
    empty, and swapping in another name would only move the tripwire to the next
    discharge.

    Any exempt DETECTOR serves: exempt means unwired, which is the precondition all four
    mutants need.  Sorted for determinism, so a failure names the same probe twice.

    *** AND THE PICK IS VERIFIED, NOT MERELY CHOSEN -- BUT NOT FOR THE REASON THIS
    PARAGRAPH GAVE UNTIL 2026-08-30. ***  It said `_exline()` "reconstructs a ONE-LINE
    entry from the table", so entries wrapped across two source lines matched nothing.
    `_exline()` EXTRACTS the real source text now, however many lines it spans, and its
    own docstring says so -- so the two halves of one file contradicted each other, the
    stale half sitting in the function that consumes the fresh one.  Found by the pass-2
    seat reviewing the commit that made the change.

    **The `count == 1` guard is still load-bearing and its warrant has MOVED.**  It no
    longer defends against a formatting mismatch -- extraction cannot have one.  It
    defends the SELF-MATCH case: a doc comment in this file quoting an EXEMPT line makes
    the extracted text appear twice.  **The MECHANISM stated here was wrong until the
    adjudicating seat built the case: `_st_apply` does NOT silently edit the comment
    instead of the table -- it COUNTS and RAISES**, `MUTANT DID NOT APPLY: '...' x2
    (want 1)`.  So the guard prevents a selftest CRASH, not a silent wrong-edit, and
    `_st_apply`'s own raise is a second line of defence behind it.

    Two facts the seat measured that belong here: injecting a verbatim copy of one
    EXEMPT entry makes `src.count()` return 2, the guard skips that name and returns
    the next candidate -- so it is genuinely load-bearing.  And **it never fires
    today**: all six counts are 1.  It is a LATENT defence, which is worth saying
    plainly, because a guard that has never fired is the one most likely to be
    deleted as dead by someone who does not know what it is for.

    *A guard whose stated reason expires but whose behaviour is still needed is the
    hardest kind to audit: deleting it looks safe, because the case it cites is gone.*
    """
    src = src_of_self()
    for name in sorted(EXEMPT):
        cls = MANIFEST.get(name, (None,))[0]
        if cls != CLASS_DETECTOR:
            continue
        if src.count(_exline(name)) == 1:
            return name
    return None


PIT_RUN = '\npython3 pit8253_latch_probe.py "$PMAX" "$STUB" > "$PLOG" 2>&1 || true\n'
#  Four shapes of MENTION, none of which is an invocation.  The third is the live
#  gate_hygiene.sh:331 shape: one non-comment line carrying the basename AND `python3`,
#  whose message is that the probe did NOT run.
PIT_MENTIONS = (
    '\n#python3 pit8253_latch_probe.py "$PMAX" "$STUB" > "$PLOG" 2>&1 || true\n'
    '#  TODO: wire pit8253_latch_probe.py in\n'
    'note "pit8253_latch_probe.py or python3 missing -- PIT rows NOT run"\n'
    'echo "see pit8253_latch_probe.py"\n'
)


def _st_apply(path, old, new, want=1):
    src = read(path)
    n = src.count(old)
    if n != want:
        raise RuntimeError("MUTANT DID NOT APPLY: %r x%d in %s (want %d)"
                           % (old[:56], n, os.path.basename(path), want))
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(src.replace(old, new))


def _st_append(path, text):
    with open(path, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def selftest(verbose=False):
    import shutil
    import subprocess
    import tempfile

    src_regress = DEFAULT_REGRESS
    me = os.path.abspath(__file__)
    root = tempfile.mkdtemp(prefix="probewiring_selftest_")
    results = []

    #  *** THE BASELINE MUST BE GREEN BY CONSTRUCTION, AND THE FIRST VERSION WAS NOT. ***
    #  fresh() copied EVERY .py from the live tree, so when a concurrent round dropped an
    #  unclassified probe into regress/, M0/M2b/M5a all went red and the selftest announced
    #  "THE CHECKER CAN NO LONGER BE SHOWN TO FAIL".  Right colour, WRONG DIAGNOSIS: it
    #  blamed the checker for an APPARATUS state -- gate_offline's F5 shape, and the
    #  dangerous one, because it points the reader at the wrong file.
    #
    #  So the baseline copies exactly the MANIFEST set.  Live-tree content can no longer
    #  perturb a mutant, and M6 still tests the unclassified-arrival path by ADDING one.
    #  A MANIFEST entry with no source file is a SETUP FAULT here, never a mutant result --
    #  absorb_census.py's rule that a crash is a fault and never a detection.
    def fresh():
        work = tempfile.mkdtemp(dir=root)
        rg = os.path.join(work, "regress")
        os.makedirs(rg)
        #  #471: THE COPY MUST MIRROR THE TREE, NOT FLATTEN IT.  This loop was
        #  `os.listdir`, so once the checker could see nested detectors the selftest
        #  copy still could not -- and every nested MANIFEST entry became a GHOST in
        #  the copy, reddening the unmutated M0 control.
        #
        #  That is the SAME blind spot one level up, inside the harness that tests
        #  for it: a flat copy cannot exercise a recursive scan.
        for f in os.listdir(src_regress):
            if f.endswith(".sh"):
                shutil.copyfile(os.path.join(src_regress, f), os.path.join(rg, f))
        for rel in MANIFEST:
            if not rel.endswith(".py"):
                continue
            src = os.path.join(src_regress, rel.replace("/", os.sep))
            if not os.path.isfile(src):
                continue
            dst = os.path.join(rg, rel.replace("/", os.sep))
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(src, dst)
        chk = os.path.join(work, "check_probe_wiring.py")
        shutil.copyfile(me, chk)
        return rg, chk

    absent = [f for f in sorted(MANIFEST) if not os.path.isfile(os.path.join(src_regress, f))]
    if absent:
        print("PROBEWIRING_SELFTEST_SETUP  the MANIFEST names files regress/ does not have:")
        for f in absent:
            print("    %s" % f)
        print("  fix the manifest first; a selftest on a broken baseline proves nothing.")
        return 2

    def case(name, want_rc, want_text, chk, rg, extra=(), forbid=None):
        p = subprocess.run([sys.executable, chk, "--regress", rg] + list(extra),
                           capture_output=True, text=True)
        out = p.stdout + p.stderr
        ok = (p.returncode == want_rc) and (want_text in out)
        if forbid is not None and forbid in out:
            ok = False
        results.append(ok)
        print("  %s  %-48s rc=%d want=%d" % ("ok  " if ok else "FAIL", name,
                                             p.returncode, want_rc))
        if verbose or not ok:
            for l in out.splitlines():
                if want_text in l or l.startswith("PROBEWIRING"):
                    print("          %s" % l.strip()[:160])
        if not ok:
            print("      --- full output ---\n%s" % out)

    print("=" * 96)
    print("  check_probe_wiring --selftest   (mutants on copies; the repo is not touched)")
    print("=" * 96)

    rg, chk = fresh()
    case("M0  unmutated copy is GREEN", 0, "PROBEWIRING_PASS", chk, rg)

    #  THE EXEMPLAR IS DERIVED.  See _pick_exempt_detector(): naming one literally is what
    #  broke this selftest the day an exemption was discharged.
    EX = _pick_exempt_detector()
    if EX is None:
        #  *** A SKIPPED MUTATION IS A FAILURE.  The first version of this arm PRINTED
        #  A SKIP AND LET THE SELFTEST PASS, and a seat refuted it with a
        #  one-character proof: change the `== 1` in _pick_exempt_detector to `== 2`
        #  and no candidate matches, four cases vanish, and the run reports
        #  PROBEWIRING_SELFTEST_PASS 17/17.  **A check getting quietly weaker while
        #  still reporting PASS** -- the exact shape this project names first, and it
        #  was introduced BY the repair for a different instance of it. ***
        #
        #  The denominator is what makes the weakening visible, so the denominator is
        #  not allowed to move: a missing exemplar reds and says why.
        #  FOUR False results, so the DENOMINATOR STAYS 21 and the run FAILS.  Keeping
        #  the denominator is the whole point: it is what makes a shrinking check
        #  visible.  A skip that reduced 21 to 17 and still said PASS is the defect
        #  this arm now refuses to have.
        results.extend([False, False, False, False])
        print("  FAIL  M1/M2/M2b/M3 -- no exempt DETECTOR could be extracted.")
        print("        NOT the EXEMPT table doing its job.  Either _exline() cannot")
        print("        extract any entry, or every exemption is discharged -- and in")
        print("        both cases the checker is no longer shown to fail on these four")
        print("        rules.  Supply a synthetic fixture; do not let the count shrink.")
    else:
        _nl = chr(10)
        EX_RUN = ('%spython3 %s "$PMAX" "$STUB" > "$SELFTEST_LOG" 2>&1 || true%s'
                  % (_nl, EX, _nl))
        EX_MENTIONS = PIT_MENTIONS.replace("pit8253_latch_probe.py", EX)

        rg, chk = fresh(); _st_apply(chk, _exline(EX), "")
        case("M1  an unwired detector is NAMED", 1,
             "UNWIRED DETECTOR  %s" % EX, chk, rg)

        rg, chk = fresh(); _st_apply(chk, _exline(EX), "")
        _st_append(os.path.join(rg, "gate_arm.sh"), EX_MENTIONS)
        case("M2  4 MENTIONS do not count as wiring", 1,
             "UNWIRED DETECTOR  %s" % EX, chk, rg)

        rg, chk = fresh(); _st_apply(chk, _exline(EX), "")
        _st_append(os.path.join(rg, "gate_arm.sh"), EX_RUN)
        case("M2b SATISFIABLE: a real invocation turns it green", 0, "PROBEWIRING_PASS",
             chk, rg, forbid="UNWIRED")

        rg, chk = fresh(); _st_append(os.path.join(rg, "gate_arm.sh"), EX_RUN)
        case("M3  wired AND still exempt -> STALE EXEMPTION", 1,
             "STALE EXEMPTION  %s" % EX, chk, rg)

    rg, chk = fresh()
    _st_append(os.path.join(rg, "gate_sh_rounding.sh"),
               '\npython3 sh4pcic_witness.py "$PMAX" "$KERNEL" > "$WLOG" 2>&1 || true\n')
    case("M4  a WITNESS wired into a gate reddens", 1,
         "GATED WITNESS  sh4pcic_witness.py", chk, rg)

    rg, chk = fresh()
    case("M5a a live exemption is GREEN the day before", 0, "PROBEWIRING_PASS", chk, rg,
         extra=("--today", "2026-09-19"))
    case("M5b the same tree is RED the day after", 1, "EXPIRED EXEMPTION", chk, rg,
         extra=("--today", "2026-09-21"))

    for tag, bad in (("M5c unpadded (the ieee_store shape)", '"2026-9-20"'),
                     ("M5d empty", '""'),
                     ("M5e not a date at all", '"soon"')):
        if EX is None:
            #  NOT `continue`.  A bare continue drops the case from `results` and the
            #  DENOMINATOR SHRINKS -- which is the very defect this arm exists to
            #  refuse, surviving one level down from where it was first repaired.
            #  Measured: with the four M1-M3 cases fixed and this one still using
            #  `continue`, the run reported 13/18 rather than 13/21.
            results.append(False)
            print("  FAIL  %-44s -- no exempt DETECTOR (see above)." % tag)
            continue
        rg, chk = fresh()
        #  DERIVED, for the same reason M1-M3 are: this named a probe literally and
        #  broke the day that probe's exemption was discharged -- the SECOND time in
        #  one session, in a mutant group the first repair had not looked at.
        _st_apply(chk, _exline(EX), '    "%s":   (%s, "x"),\n' % (EX, bad))
        case("%-44s is RED, not unexpired" % tag, 1,
             "MALFORMED EXEMPTION  %s" % EX, chk, rg,
             extra=("--today", "2026-08-21"))

    #  ---------------------------------------------------------------- M5f
    #  *** THE DEFAULT CLOCK WAS COVERED BY NOTHING.  Measured 2026-08-30 by the pass-2
    #  seat, which asked the standing question -- what is the smallest edit that breaks
    #  this and still passes? -- and answered it in ONE LINE: ***
    #
    #      today = datetime.date.today().isoformat()   ->   today = "2020-01-01"
    #
    #  Production: PROBEWIRING_PASS, rc=0.  Selftest: SELFTEST_PASS 21/21, rc=0.  And it
    #  makes EVERY DATED EXEMPTION IMMORTAL -- the one thing the table exists to prevent.
    #
    #  **The blindness was structural, not an oversight about one line.**  M5a-M5e each
    #  pass `--today` EXPLICITLY, so between them they test the COMPARISON exhaustively
    #  and the CLOCK IT READS not at all.  The only mutant on the default path was M0,
    #  whose want is PASS -- so a frozen clock satisfies it.  *A parameter added to make
    #  a test deterministic removed the last coverage of the value it replaces.*
    #
    #  This row runs on the REAL clock, with one exemption dated YESTERDAY -- computed,
    #  never a literal, or the row rots into a permanent red the day it is written.
    #  Clean checker: rc=1, EXPIRED EXEMPTION.  Frozen clock: rc=0, PROBEWIRING_PASS.
    if EX is None:
        results.append(False)
        print("  FAIL  M5f -- no exempt DETECTOR (see above).")
    else:
        import datetime as _dt
        _yest = (_dt.date.today() - _dt.timedelta(days=1)).isoformat()
        rg, chk = fresh()
        _st_apply(chk, _exline(EX), '    "%s":   ("%s", "x"),%s' % (EX, _yest, chr(10)))
        case("M5f the DEFAULT clock is live (no --today)", 1,
             "EXPIRED EXEMPTION  %s" % EX, chk, rg)

    rg, chk = fresh()
    with open(os.path.join(rg, "zz_new_probe.py"), "w", encoding="utf-8",
              newline="\n") as fh:
        fh.write("#!/usr/bin/env python3\n")
    case("M6  a NEW probe arriving unclassified reddens", 1,
         "UNCLASSIFIED  zz_new_probe.py", chk, rg)

    rg, chk = fresh(); os.remove(os.path.join(rg, "pit8253_latch_probe.py"))
    case("M7  a MANIFEST entry whose file is gone reddens", 1,
         "GHOST  the MANIFEST names pit8253_latch_probe.py", chk, rg)

    rg, chk = fresh()
    _st_apply(chk, _lit('"pit8253_latch_probe.py"', ':      (CLASS_DETECTOR'),
              _lit('"pit8253_latch_probe.py"', ':      (CLASS_TOOL'))
    case("M8  hiding a detector in class 'tool' reddens", 1,
         "MISFILED  pit8253_latch_probe.py", chk, rg)

    rg, chk = fresh()
    _st_apply(os.path.join(rg, "run.sh"), " gate_arm gate_ppc_halt", " gate_ppc_halt")
    case("M9  dropping gate_arm from GATES unwires its 8", 1,
         "UNWIRED DETECTOR  arm_flags_probe.py", chk, rg)

    rg, chk = fresh(); os.remove(os.path.join(rg, "gate_ppc.sh"))
    case("M10 a gate named in GATES with no file reddens", 1,
         "run.sh names gate_ppc.sh", chk, rg)

    rg, chk = fresh(); _st_apply(os.path.join(rg, "run.sh"), "GATES=(", "GATESX=(")
    case("M11 an unparseable GATES array reddens", 1, "no GATES=( ... ) array", chk, rg)

    rg, chk = fresh()
    #  GUARDED, because a missing exemplar is ALREADY recorded as four failures above
    #  and a traceback here would bury that legible report under a stack trace.  The
    #  denominator is held the same way: one False, not one fewer case.
    if EX is None:
        results.append(False)
        print("  FAIL  M12 -- no exempt DETECTOR could be extracted (see above).")
    else:
        #  DERIVED.  This named `hpcmips_ctor_probe.py` literally and was the THIRD
        #  such literal in this selftest -- found by a seat AFTER two earlier repairs
        #  had each believed they were the last.  The tripwire was moved twice before
        #  it was removed, which is the argument for deriving rather than renaming.
        _st_apply(chk, _exline(EX),
                  _exline(EX).replace('"%s"' % EX, '"hpcabort_witness.py"', 1))
        case("M12 exempting a WITNESS reddens", 1,
             "ORPHAN EXEMPTION  hpcabort_witness.py", chk, rg)

    #  ---------------------------------------------------------------- #471
    #  THE RECURSIVE SCAN NEEDS ITS OWN MUTANTS, or a future edit reverts it and every
    #  mutant above stays green -- the vacuity this file exists to refuse.  The three
    #  below were specified by the farmed design that scoped this fix.

    #  M13: NESTED RED.  Delete the real invocation from the gate; the nested detector
    #  must be named by its FULL RELATIVE PATH, not its basename.
    rg, chk = fresh()
    _st_apply(os.path.join(rg, "gate_sh_rounding.sh"),
              'python3 -u "$GPNPROBE"', 'true "$GPNPROBE"')
    case("M13 a NESTED detector loses its gate and reddens", 1,
         "artifacts/gdrompionull/gdrom_pio_null_probe.py", chk, rg)

    #  M14: THE SCAN ITSELF.  Restore the `"/" not in f` filter and the nested detector
    #  becomes INVISIBLE -- which is exactly the #465 escape.  It reddens as a GHOST,
    #  because the MANIFEST still names a file the scan can no longer see.
    rg, chk = fresh()
    _st_apply(chk, _lit('rel = os.path.relpath(', 'os.path.join(dirpath, f), regress)'),
                   _lit('rel = ', 'f'))
    case("M14 the walk flattened (the #465 blind spot returns)", 1,
         "GHOST", chk, rg)

    #  M15: THE COLLISION CONTROL.  Re-key exec sites to the bare name again.  A gate
    #  invoking
    #  one nested detector would then mark EVERY like-named file gated -- the silent
    #  failure the path re-key exists to prevent.  (This comment deliberately avoids
    #  quoting the mutant's own find-text: _st_apply saw it TWICE and refused the
    #  edit, which is the harness correctly rejecting an ambiguous mutant.)
    #  It reddens because the ignored
    #  branch swallows the nested invocation instead.
    rg, chk = fresh()
    _st_apply(chk, _lit('hits.setdefault(', 'rel, []).append'),
                   _lit('hits.setdefault(', 'b, []).append'))
    case("M15 exec sites keyed by basename again (collision)", 1,
         "artifacts/gdrompionull/gdrom_pio_null_probe.py", chk, rg)

    shutil.rmtree(root, ignore_errors=True)
    n_ok = sum(1 for r in results if r)
    print()
    if n_ok != len(results):
        print("PROBEWIRING_SELFTEST_FAIL  %d/%d mutants behaved as specified"
              % (n_ok, len(results)))
        return 1
    print("PROBEWIRING_SELFTEST_PASS  %d/%d mutants behaved as specified"
          % (n_ok, len(results)))
    return 0


def main(argv):
    verbose = "-v" in argv or "--verbose" in argv
    if "--selftest" in argv:
        return selftest(verbose)
    regress = DEFAULT_REGRESS
    today = None
    for i, a in enumerate(argv):
        if a == "--regress" and i + 1 < len(argv):
            regress = os.path.abspath(argv[i + 1])
        if a == "--today" and i + 1 < len(argv):
            today = argv[i + 1]
    if today is None:
        import datetime
        today = datetime.date.today().isoformat()

    fails, notes = [], []

    if not os.path.isdir(regress):
        print("PROBEWIRING_FAIL  no regress dir at %s" % regress)
        return 1

    scripts, err = gate_list(regress)
    if err:
        print("  FAIL  %s" % err)
        print("PROBEWIRING_FAIL  the battery could not be derived")
        return 1
    scripts = scripts + [s for s in ALWAYS if s not in scripts]

    hits, ignored, missing = exec_sites(regress, scripts)
    for s in missing:
        fails.append("run.sh names %s and the file does not exist -- the battery is broken" % s)

    on_disk, mode = domain(regress)

    for f in on_disk:
        if f not in MANIFEST:
            fails.append("UNCLASSIFIED  %s is not in check_probe_wiring.py's MANIFEST.\n"
                         "                classify it detector (green once fixed), witness "
                         "(red once fixed) or tool." % f)
    for f in sorted(MANIFEST):
        if f not in on_disk:
            fails.append("GHOST  the MANIFEST names %s and regress/ has no such file -- "
                         "delete the entry" % f)

    rows = []
    for f in on_disk:
        if f not in MANIFEST:
            continue
        cls, why = MANIFEST[f]
        where = hits.get(f, [])
        if cls not in CLASSES:
            fails.append("BAD CLASS  %s is classified '%s'; want one of %s"
                         % (f, cls, "/".join(CLASSES)))
            continue

        if cls == CLASS_TOOL and (f.endswith("_probe.py") or f.endswith("_witness.py")):
            fails.append("MISFILED  %s is classified 'tool'. A file named *_probe.py or "
                         "*_witness.py asserts something; classify it detector or witness."
                         % f)

        if cls == CLASS_DETECTOR:
            if where:
                state = "RUN by " + ", ".join(where)
                if f in EXEMPT:
                    fails.append("STALE EXEMPTION  %s is RUN by %s and still carries an "
                                 "exemption dated %s -- the debt is paid, delete the line"
                                 % (f, where[0], EXEMPT[f][0]))
            elif f in EXEMPT:
                d = EXEMPT[f][0]
                if not DATE_RE.match(d or ""):
                    fails.append("MALFORMED EXEMPTION  %s:'%s' is not YYYY-MM-DD. A date "
                                 "nothing validates never expires -- refusing to guess."
                                 % (f, d))
                    state = "EXEMPT(BAD-DATE)"
                elif d < today:
                    fails.append("EXPIRED EXEMPTION  %s came due %s (today %s) and is still "
                                 "run by no gate" % (f, d, today))
                    state = "EXEMPT(EXPIRED %s)" % d
                else:
                    state = "EXEMPT until %s" % d
            else:
                fails.append("UNWIRED DETECTOR  %s is run by NO gate and has no dated "
                             "exemption.\n                wire it into a gate, or add a dated "
                             "line to EXEMPT naming the gate that owes it." % f)
                state = "UNWIRED"
        elif cls == CLASS_WITNESS:
            if where:
                fails.append("GATED WITNESS  %s is invoked at %s. A witness asserts the "
                             "PRE-FIX symptom, so it goes RED the day the fix lands -- "
                             "gating it manufactures a regression." % (f, where[0]))
                state = "GATED (must not be): " + ", ".join(where)
            else:
                state = "not run (correct)"
        else:
            state = ("RUN by " + ", ".join(where)) if where else "-"

        if cls in (CLASS_DETECTOR, CLASS_WITNESS):
            lbl = self_label(os.path.join(regress, f))
            if lbl and lbl != cls:
                notes.append("SELFLABEL  %s: manifest says %s, its own summary line says %s. "
                             "Advisory only -- self-labels are measurably unreliable in both "
                             "directions." % (f, cls, lbl))
        rows.append((cls, f, state, why))

    for f in sorted(EXEMPT):
        if f not in MANIFEST:
            fails.append("ORPHAN EXEMPTION  %s is exempted and is not in the MANIFEST" % f)
        elif MANIFEST[f][0] != CLASS_DETECTOR:
            fails.append("ORPHAN EXEMPTION  %s is classified '%s'; only a detector can be "
                         "exempted from being run" % (f, MANIFEST[f][0]))

    print("  check_probe_wiring: %d python artefacts in %s/ [%s], %d battery scripts "
          "from run.sh" % (len(on_disk), os.path.basename(regress), mode, len(scripts)))
    if verbose:
        for cls in CLASSES:
            for c, f, state, why in rows:
                if c == cls:
                    print("    %-8s %-28s %-38s %s" % (c, f, state, why))
        for line in ignored:
            print("    IGNORED  %s   (not the regress copy)" % line)
    for n in notes:
        print("  note  %s" % n)
    for f in fails:
        print("  FAIL  %s" % f)

    det = [r for r in rows if r[0] == CLASS_DETECTOR]
    run = [r for r in det if r[2].startswith("RUN")]
    ex = [r for r in det if r[2].startswith("EXEMPT")]
    wit = [r for r in rows if r[0] == CLASS_WITNESS]
    if fails:
        print("PROBEWIRING_FAIL  %d problem(s); %d/%d detectors run by a gate, %d dated-exempt"
              % (len(fails), len(run), len(det), len(ex)))
        return 1
    print("PROBEWIRING_PASS  %d/%d detectors run by a gate, %d dated-exempt, %d witnesses "
          "correctly ungated" % (len(run), len(det), len(ex), len(wit)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
