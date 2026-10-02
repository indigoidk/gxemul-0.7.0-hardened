#!/usr/bin/env python3
"""
crime_width_probe.py BIN [LABEL] -- #529 crimewidthkill DETECTOR, rung 3, cold debugger, UNMODIFIED `-E sgi -e ip32'.

src/devices/dev_sgi_ip32.c, DEVICE_ACCESS(crime): an access whose length is neither 8 nor 4 used to reach

        fatal("crime access len = %i!\n", len);
        exit(1);

so one guest lb/lbu/lh/lhu/sb/sh anywhere in CRIME (physical 0x14000000, KSEG1 0xb4000000) ended the emulator
(witnessed for all six widths at rung 3: regress/artifacts/crimewidthkill/crime_width_witness_20260913.py).  #529 DECLINES the width
with one latched `(once)' announce and a `goto' to the function's common tail, skipping the register switch -- the
#498 sgi_de shape.  A read is answered 0 by the tail, a write is dropped, the PC advances, no exception is raised.

Every access here is a real MIPS guest instruction through real address decode and memory_rw, one `step' at a time.

CONTRACT -- the edits this detector is designed to catch (clause (e)), each MEASURED in a kill table under
artifacts/crimewidthkill/ (killtable_20260913/ through killtable10_20260915/):
  1. the kill reinstated verbatim, or any other host death at the width arm, before or after the announce
                                                       <op> surv (six widths), hi surv, latch surv, sb08 run
  2. FAULT: the width arm returning 0 (a guest data bus error, EXCEPTION_DBE)   lb/lh/sb/sh pc and exc, lb/lh/lbu/lhu v0
  3. the refused access FALLING INTO THE REGISTER SWITCH -- the goto lost, or narrowed by width, direction, or ADDRESS.
     The switch's observable arms, per refusal cell:
        CRIME_CONTROL (+0x08), writes     sb 0x01 prints the unimplemented-control fatal    sb08 msg
                                          sh 0x0800 stops every CPU (HARD_RESET)            sh08 run, sh08 pc
                                          and the arm's two TESTED idata bits (DOG 0x200, RESET 0x800) each
                                          both ways at 2W, plus ENDIANESS 0x100, which the arm CLEARS
                                          UNCONDITIONALLY and never branches on (written anyway): sh 0x0201,
                                          0x0900, 0x0a00 with sh08 0x0800       sh08b msg, sh08b run
                                          [This said "three TESTED idata bits (... ENDIANESS 0x100)" until
                                          repair 12 -- false; agy, grok, closing pass 6.]
                                          plus ALL-ONES refused writes, sb 0xff and sh 0xffff (kimi CLI,
                                          closing pass), so a fall-through keyed on any bit a 1- or 2-byte
                                          store can carry shows (bits above 15 never reach a refused access,
                                          so a conjunct on them is equivalent)  sb08 msg, sh08b msg/run
        and the refused stores at INTSTAT, INTMASK and TIME carry all-ones (0xff / 0xffff) for the same reason
        CRIME_REV (+0x00), reads AND writes, from pc 0xbfc05180: the PROM-probe hack sets pc = ra (it does not test
                                          the direction)                                    lb/lh/sb/sh rev pc
        CRIME_INTMASK (+0x18), CRIME_INTSTAT (+0x10), all four cells: the arm calls crime_interrupt_reassert(),
                                          which raises cause.IP2 after a SOFTINT store   imask/istat lb, sb, lh, sh
        CRIME_TIME (+0x38), all four cells: the arm advances TIME, which the NEXT read shows   time lb, sb, lh, sh
        the default arm (any unlabelled offset): a debug() line, printed while stepping      lb/lh/sb/sh nodflt,
                                          at +0x07, +0x06, +0x1f, +0x1e, +0x27f  hi nodflt, and
                                          +0x1ff, +0x1fe, +0x1fc                 mid nodflt
     Each channel carries a LIVE control on an accepted width that shows it can vary:
        rev pc ctl (lw redirects), sw08 halts (sw 0x800 stops the CPUs), sw08 msg ctl (sw 0x01 prints the text),
        imask/istat pre + ctl (IP2 low after the setup; an accepted lw sets it), time lb/sb/lh/sh ctl (an accepted ld
        moves TIME), dflt ctl (lw +0x04 prints the default-arm line).
     The INTSTAT/INTMASK/TIME rows came from the pass-2 Opus seat, which MEASURED a decline narrowed to skip those
     labels passing the 40-row version of this detector 40/40 (opus_pass2_20260913/OPUS_REPORT.md); their 2-byte cells
     from the F2 pass (grok, glm): `len != 2 || relative_addr != CRIME_INTSTAT' passed the 71-row version.  So every
     observable label carries the whole {1,2} x {R,W} refusal floor (CONTROL's reads and DOG have no body: below).
     *** THE sh08 AND sw08 CHANNELS EXIST BECAUSE OF A SEPARATE DEFECT, `crimectllane' (filed): the switch matches
     CRIME_CONTROL by its exact label 0x08 and reads the RAW idata, so a 32-bit write to the high half, or a halfword at
     +0x08, carries bit 11 into HARD_RESET, while NetBSD's +0x0c write does nothing.  A round that fixes that lane
     removes or moves these channels and owes their re-derivation -- the sw08 controls will go red to say so. ***
  4. the latch removed, never set, or KEYED ON THE ACCESS -- the class closed on its single axes after two passes
     found members (F2: `|= len', `|= relative_addr', `<< writeflag'; closing pass: keyed on CRIME_CONTROL, on
     `relative_addr >= 0x40', on address parity).  A keyed latch shows only when the first refusal in a session falls
     where it does not set, so every axis value is a FIRST refusal followed by another, with an announce count:
        width 1 or 2 and direction R or W  warm once (sb, write, odd), latch x5 (lh, read, even)
        each label first                   rev once, sh08b once (CONTROL), istat once, imask once, dog once,
                                           time once, latch x5 (default-arm, low), hi once (the far block,
                                           followed by refusals there and one below 0x40), mid once
     and every label-first session refuses again at ANOTHER label (codex, second closing pass: a latch whose bit is
     keyed on one label, `CRIME_W_LEN << (relative_addr == CRIME_INTMASK)', passed the 111-row version: the imask,
     istat and sh08b sessions refused only at their own label; codex, third closing pass: the middle block likewise
     for address bits 7 and 8 -- mid once now refuses at +0x07 as well)
     and the FIRST refusal's own TEXT in every label-first session (codex, third closing pass: a notice SUPPRESSED at
     one label, or at one address-bit value, and printed by the follow-up instead, still counted one; every said row
     sat at an offset with bit 1 set -- rev said is at +0x00, every address bit clear)
                                            rev said, sh08b said, imask said, istat said, time said, dog said
     and the latch TEST that lets one label through (`|| relative_addr == L'): every label is refused again AFTER the
     latch is set somewhere -- REV and TIME in latch x5's tail (the Opus third-closing seat, measured: they were each
     refused once per session, first, so `|| == CRIME_REV' and `|| == CRIME_TIME' passed)
     and the latch PRE-SET before any refusal, over the KIND x LABEL CROSS (`ACCEPTS'): {8W, 8R, 4W, 4R} at every
     case label, REV also from the PROM-probe window at all four kinds (`ldP' since repair 11 -- this said "in both
     directions" and the window had no 8R; the flagship ruling, closing pass 5), CONTROL's writes at both widths x
     {0x0201, 0x0001, 0, 0x0200} (DOG x leftover, all four; plus 0x0100 ENDIANESS at both widths, a clause-(e)
     strengthening -- the arm never branches on it), and the default arm's six kinds in both 4-byte lanes -- all in
     latch x5's prologue, before its first refusal; also warm once (sd first) and time once (ld first).  HARD_RESET's
     true side: disclosed (it stops the CPUs).  *** This said "DERIVED FROM THE FUNCTION'S OWN BRANCHES ... both sides
     of every `if'" after repair 9, and the fourth closing pass measured it short: each branch's sides were taken
     SOMEWHERE, not crossed with the label -- a pre-set on an accepted 8-byte WRITE at +0x10 and on CONTROL's 0x0200 cell
     each scored 131/131 on the 131-row test (the Opus seat; deepseek, kimi CLI by reading). ***
  5. the announce: its text (`unimplemented len=N at 0xA -- declined.  (once) ]' exactly once in each width's own
     session: lb/lh/sb/sh said, hi said), and its CHANNEL -- fatal(), which prints when the guest free-runs, where a
     debug() would not -- on EVERY axis of the refusal: bits 0-2 (free said, +0x07), bits 3-8 and len 2 (free 2r said,
     +0x1f8), bit 9 and a write (free 1w said, +0x27f), a 2-byte write at a label (free 2w said, CONTROL), and each
     remaining label (free rev/istat/imask/dog/time said), and the ISSUING PC -- a refusal from the PROM-probe window
     (free revP said, repair 12; glm, closing pass 6: `(pc in the window ? debug : fatal)(' scored 141/141 on the 141-row
     test -- clause (e)
     by the DEPENDS-ON bound, rowed as a strengthening).  *** Until repair 10 the channel was pinned at ONE cell (+0x07):
     `(relative_addr & 8 ? debug : fatal)(' and `(len == 2 ? debug : fatal)(' each scored 131/131 on the 131-row test (codex, the Opus
     seat, fourth closing pass).  One refusal per free-running session -- the latch silences any second one. ***
  6. the ACCEPT SET shrunk at any single cell IN THE GUARD-GROWTH FORM -- an accept guard grown by a conjunct, so the
     cell falls into the announcing decline arm (the de-escalation clause: the deleted exit(1) used to announce exactly
     this) -- at EVERY ACCEPTS cell by `latch said': latch x5 runs all 46 ACCEPTS accesses before the lh +0x06, so a
     wrongly declined accepted cell steals that lh's own announce (repair 12; codex's C1 and the Opus seat's G1-G5 each
     scored 141/141 on the 141-row test, because `latch x5' and `rearm once' COUNT notices and a stolen notice keeps the
     count at 1).  *** This item said "the ACCEPT SET shrunk at any single cell" with no form, and it was false at
     CONTROL 4R/8R/8W, INTSTAT 8, TIME 4, INTMASK 4W and the REV window 4W (closing pass 6, measured). ***
     The SILENT form -- a bypass inserted before the width test that declines an accepted cell with NO announce (the
     Opus seat's G6) -- is outside the de-escalation class and DISCLOSED by class; it is CAUGHT where a bypassed cell is
     guest-visible AND THE CATCHING ROW RUNS IN THE BYPASS'S OWN LATCH STATE, by the value rows derived per cell
     (repair 12): REV window 4W/8W/8R (revP sw/sd/ld pc), CONTROL 8R
     (acc ctl ld) and 8W (acc ctl sd), INTSTAT 8R (acc istat ld), 8W and 4W (istw sd, istw sw), INTMASK 4W (acc imask
     sw), TIME 8W (acc time sd), the default arm's 4W/4R at +0x40 (acc 40 sw, acc 40 lw); and it is EQUIVALENT at REV
     8W/4W/4R outside the window (the prelude rewrites REV; its high half is 0) and CONTROL 4R (reads 0 either way).
     *** THIS SENTENCE ALSO LISTED "TIME 4W/4R (the high half is 0; updates accumulate)" AS EQUIVALENT, AND BOTH THE
     CLAIM AND ITS STATED REASON ARE MEASURED FALSE -- closing pass 7, artifacts/crimewidthkill/opus_close7_20260915/
     OPUS_REPORT.md, mutant E2 at 157/157 on the 157-row test, with the difference on FOUR channels.  A read takes `odata' BEFORE its own
     crime_update_crime_time(), so an update skipped at the 4-byte access ARRIVES ONE ACCESS LATE rather than
     accumulating: free-running ld;sw;ld reads 0xc6 then 0x108 on base and 0x0 under the bypass, six times out of six
     each way.  TIME 4W/4R is
     GUEST-VISIBLE AND UNROWED -- a single-axis floor cell, owed by repair 13 in the GAPPED step shape
     (opus_close7_20260915/scripts2/post7c.py; the two obvious shapes were measured VACUOUS by the seat that wrote
     them, which is why the CHANNEL line has to be CHECKED against its mutant and not merely written). ***
     *** AND THE "CAUGHT" CLAUSE ABOVE CARRIED NO LATCH QUALIFIER UNTIL THAT SAME PASS, WHICH MADE IT FALSE OF A
     LATCH-CONDITIONED BYPASS.  K1/K2/K3 -- `&& !(<cell> && (d->warned & CRIME_W_LEN))' at INTMASK 4W, at the REV
     4-byte cell and at CONTROL 8R -- EACH SCORE 157/157 on the 157-row test, because the value row for each cell is measured
     only while the latch is CLEAR.  Eight of the guest-visible cells ARE already pinned post-latch and the rest are
     not; the map is derived in opus_close7_20260915/scripts2/session_map2.py, not asserted here. ***
     *** AND "The remaining ACCEPTS cells' accept side is pinned by the rows below" IS FALSE IN THREE PLACES, all
     measured in the same pass, all on the 157-row test: sw +0x04 (F3, 157/157 -- guest-equivalent, a host WRITE line nothing
     counts), CONTROL 0x0201 at BOTH widths (F1/F1b, 157/157 on the 157-row test -- host-log only, a multi-axis idata joint, so clause-(e)
     debt rather than floor), and EIGHT cells whose only pin is an INCIDENTAL access in another session that no
     enumeration names.  The honest statement: the cells enumerated above are ROWED; the others are pinned where a row
     happens to touch them, and which those are is a derivation, not a claim. ***  The ACCEPT set also at BOTH ends of the window:  the FIRST slot +0x00 -- acc8 near (8R, anchored to CRIME_REV's 0x11, which the
     prelude writes; grok, closing pass: `len == 8 && relative_addr != 0' passed the 85-row version, whose rows sat at
     +0x30 -- an interior slot, not an end), with devsig the 4R-low cell there and `rev pc ctl' the 4R-high one (its
     redirect needs the access ACCEPTED; `devsig hi' reads 0 either way -- grok, codex, second closing pass, correcting
     this sentence, which credited devsig hi); CRIME_DOG +0x30 -- acc8 st+ld
     (8W, 8R), acc4 rhi, acc4 rlo, acc4 wlo, acc4 whi; the last slot +0x278 -- top8 st+ld, top4 rhi, top4 rlo, top4 w.  Those rows are ROUND TRIPS and cannot see an
     accept arm that re-maps its register index (kimi-k3:cloud, F2: `d->reg[(relative_addr & 0x3f) / 8]' passed the
     71-row version), so one row is ANCHORED: `top8 anchor' reads bank-1 control at +0x210, a value the PRELUDE writes
     by bank index (1 for -M 64), not by the decode under test; `top4 anchor' reads its low half with a 4R.  The 4R
     of its HIGH half answers 0 accepted or refused, so that cell is pinned by the ANNOUNCE instead (Opus closing:
     `len == 4 && relative_addr != 0x210' passed the 85-row version): every accept cell the top session touches
     before its one refusal is pinned the same way                                                      top said
     *** It pins the model's CURRENT bank layout, which the
     filed `crimebankorder' disputes; a round that re-orders the banks owes this row's re-derivation. ***
  7. a refused store that LANDS: CRIME_DOG seeded by an accepted sd survives a refused sb and sh     sb keeps, sh keeps;
     and a seeded slot with address bit 4 CLEAR (+0x40; the Opus third-closing seat, measured: every read-back refused
     store had bit 4 set, so a landing keyed on bit 4 clear passed), including a refused HALFWORD with address bit 1
     SET at +0x42 (codex, the Opus seat, fourth closing pass: every read-back refused 2-byte store cleared bit 1, and a
     2W landing keyed on it scored 131/131 on the 131-row test)                                                             lo keeps
     and at the far block, a refused sb +0x27f and sh +0x27c leave the SEEDED +0x278 as seeded (Opus, F2 and closing: a
     store landing only >= 0x200, of either width; this said "reading 0" until the fourth closing pass -- repair 8
     seeded the slot)                                                                                   hi keeps
     and in the middle of the window (+0x1ff / +0x1fc, every address bit 0-8 set)                       mid keeps
     and at INTMASK, read back by an accepted ld (kimi CLI, second closing pass: a landing that ORs into INTMASK kept
     bit 28, so imask ctl could not see it)                                                             imask keeps
  8. state carried ACROSS calls: a declined read after accepted reads of a nonzero register still answers 0 (an
     `odata' made static), and an accepted access between two refusals does not re-arm the announce    warm v0,
     warm once  (the codex seat, F2) -- closed over every place an accepted access can go after codex found the
     4-byte arm's re-arm open on the closing pass -- now the KIND x LABEL CROSS, the SAME list as item 4's pre-set
     (`ACCEPTS', 46 ENTRIES since repair 11 (SIX kinds -- see the repair-12 bullet; this said `46 kinds' and the same header said `46 ENTRIES, not 46 kinds' twenty lines down: grok's nit, confirmed and corrected at BOTH sites) -- 43 before `ldP' and the two ENDIANESS writes; codex, second closing pass: `d->warned = 0;' inside DOG_ENABLE; the Opus third-closing seat:
     CONTROL's read, DOG-clear and zero-leftover sides; the fourth closing pass: a re-arm on an accepted WRITE at
     INTSTAT/INTMASK or REV and on CONTROL's 0x0200 cell, each 131/131 on the 131-row test) -- each accepted kind between two refusals
                                                                                            rearm once, rearm surv
     and in the middle block (an accepted sd between two refusals there)                                mid once
  9. the ANSWER at each named label: a refused read at CRIME_REV, CONTROL, INTSTAT, INTMASK, DOG and TIME answers 0
     (codex, closing pass: `if (relative_addr == CRIME_REV) odata = 1;' passed the 85-row version -- the REV rows
     checked only the pc)          lb/lh rev v0, ctl v0, ctl lb v0, istat/imask lb/lh v0, dog v0, dog lh v0, time lb/lh v0
     every one at 2 bytes (lh sees every value lb sees) and over a register whose LOW BYTES ARE NONZERO, so a decline
     that answers the register shows (kimi CLI, second closing pass: INTSTAT, INTMASK and DOG held 0 in their low
     bytes and `odata = d->reg[relative_addr / 8]' there passed; codex: `odata = 0x100' at DOG passed the lb-only row)
     -- REV 0x11, CONTROL 0x100, TIME 66-990 (low bytes); INTSTAT/INTMASK 0x0101010111010101 and DOG
     0x0123456789abcdef, nonzero in EVERY byte, so any SHIFT of the register's bytes into the answer shows (Opus, second
     closing pass: the ADDRESSED lanes passed the 0x10000001 seed 121/121 on the 121-row test; glm, third closing pass:
     the 4-byte path's half, `reg >> 32', passed the 0x0101000010000001 one).  [A selection CONFINED above byte 1 --
     `& 0xffff0000' -- answers 0 to every lb/lh by construction and is EQUIVALENT; this said "ANY selection ... shows"
     until the kimi CLI seat, fourth closing pass.]  And the answer SOURCE other than the addressed register: every
     lvalue the function reads that is NONZERO in some session is nonzero where a refused answer is read in that
     session, HARDINT included -- latched only in the gate session, where refused lb/lh now read it -- and SOFTINT
     (nonzero in the imask/istat/gate sessions; the Opus fifth-closing seat measured `odata = SOFTINT' red there).
     [Corrected 2026-09-14, flagship ruling on closing pass 5: this said "every lvalue the function reads is nonzero
     where a refused answer is read" -- FALSE: `d->use_fb', `flag_for_128MB' and `idata' are 0 at every refused read,
     and `odata = d->use_fb' scored 141/141 on the 141-row test (the Opus seat).  Those are DISCLOSED below.]  The HARDINT source (kimi-k3:cloud, the Opus seat, fourth closing pass: a decline answering
     `d->reg[CRIME_HARDINT / 8]' scored 131/131 on the 131-row test)                                          gate lb v0, gate lh v0.
     CONTROL is answered at both widths (ctl lb v0, ctl v0; the Opus
     third-closing seat, measured: `odata = 1' keyed on len 1 at CONTROL passed the lh-only row); its low byte is 0, so
     only a CONSTANT answer can show at lb there.  TIME: at the time rows' refused reads TIME is a multiple of 66 and is
     0 in 42 of 800 logged cells (the same seat -- this said "0.3% of runs, 66-990 includes 256, 512, 768", and those
     are not multiples of 66), so the register cell is pinned by a SEEDED odd TIME instead     time sd lb v0, time sd lh v0
     and in the far block and the middle block over a NONZERO slot, at both widths (Opus closing: a refused read
     >= 0x200 answering the register; Opus, second closing pass: the 2-byte cell there)
                                                                   top rd v0, top rd2 v0, mid lb v0, mid lh v0
  10. the decline HOLDS WHILE AN INTERRUPT IS LATCHED: HARDINT set by the guest through MACE and the CRIME line
      asserted, a refused sh 0x0800 at CONTROL still does not stop the CPUs (the Opus closing seat: `if
      (!d->reg[CRIME_HARDINT / 8])' -- a field the tail reads -- and `if (!d->prev_asserted)' passed the 85-row
      version)                                        gate run, with gate hardint and gate line as its controls
      and a refused READ answers 0 while HARDINT is latched -- the answer SOURCE item 9 names (fourth closing pass)
                                                                                                 gate lb v0, gate lh v0

*** THE LATCH-KEYED ACCEPT SHRINK (the K-CLASS) AND ITS CLOSURE -- repair 13, and it is the reason this probe grew
from 157 rows to 188. ***

An accept guard grown with a conjunct on THIS FIX'S OWN LATCH -- `&& !(<cell> && (d->warned & CRIME_W_LEN))' -- declines
SILENTLY at that cell once any refusal has happened, because the latch is exactly what suppresses the announce.  Three
instances were MEASURED at 157/157 with a guest loss on the 157-row instrument (closing pass 7, opus_close7_20260915/
OPUS_REPORT.md): K1 at INTMASK 4W, K2 at the REV 4-byte cell, K3 at CONTROL 8R.  The value rows at THOSE THREE
CELLS are measured with the latch CLEAR, so none of them could see it.
*** THIS SENTENCE READ "EVERY value row this probe had was measured with the latch CLEAR" AND IS FALSE -- codex,
closing pass 8, naming `imask keeps', `sb keeps', `sh keeps' and the TIME controls as rows that already operate
AFTER a refusal.  IT IS THE SECOND TIME I HAVE WRITTEN IT: the close-7 seat corrected the same over-generalisation
in MAINLOOP_HARVEST.md (45 sessions, 72 post-refusal accepted accesses in eleven of them), and I reintroduced it
here while writing repair 13's contract.  The true statement is the narrow one above, plus the derived bucket: of
the 31 guest-visible ACCEPTS entries, EIGHT are already pinned post-latch (session_map2.py).  A sentence corrected
once and rewritten later is worse than one never corrected, because the correction is on record and looks applied. ***

*** THE GRADE IS FLOOR, NOT CLAUSE (e), and that OVERTURNED THE PRIOR RULING (FABLE_C5_RULING_20260915.md, S-A.7;
FABLE_C4_RULING's RA3 corrected in place).  The reason is in the fix's own diff: the width dispatch's `else' arm READS
`d->warned', in a hunk this diff ADDS -- so the latch is a device-state lvalue the fix's own repair path reads, which
the pass-11 floor definition and the M_ICLR precedent make a floor axis. ***

THE ENUMERATION is the four-axis product {latch clear, set} x {len 4, 8} x {read, write} x {the 7 labels the switch
distinguishes: REV, CONTROL, INTSTAT, INTMASK, DOG, TIME, default} = 56 cells.
*** THIS SENTENCE READ "The latch-CLEAR half is table 10's twelve S_* silent bypasses" AND IS FALSE TWICE -- the glm
seat, closing pass 8, and it is the sharpest finding of that pass.  (i) THE LATCH-CLEAR HALF IS 28 CELLS AND TWELVE IS
TWELVE.  (ii) Materially, and by this round's OWN evidence: close-7's E2 proved TIME 4W/4R guest-visible on a
LATCH-CLEAR observation ("free-running ld;sw;ld reads 0xc6 then 0x108 on base and 0x0 under the bypass" -- no refusal
in that sequence), and TIME 4W/4R are NOT among the twelve, whose only TIME cell is 8W.  So the half provably contains
a guest-visible cell outside the set that was said to close it. ***
*** AND THE CONSEQUENCE IS A CANDIDATE ESCAPE, THE MIRROR OF THE K-CLASS: repair 13 rows TIME 4W/4R ONLY POST-LATCH --
every `p *' session opens with a refused lb, which is the whole point of them -- so a bypass conditioned on the latch
being CLEAR has NO row running in its state at that cell.  The amended catching clause above ("CAUGHT ... AND THE
CATCHING ROW RUNS IN THE BYPASS'S OWN LATCH STATE") therefore fails for it by its own words.  The owed row is the same
GAPPED shape MINUS the opening refused lb.  Under measurement by the closing-pass-8 measuring seat; if it escapes, it
is an L2 floor cell and repair 14 owes the latch-CLEAR half the same treatment the latch-SET half got. ***  **THE ROWS OWED ARE NOT ALL 28 LATCH-SET MUTANTS AND NOT ALL 56 CELLS**: a mutant at an
equivalent or already-pinned cell teaches nothing and a row at a cell no mutant reaches is unfalsifiable, so the FLOOR
is the INTERSECTION.  Over the 46 ACCEPTS entries:

    23  ROWED HERE, post-latch, by the `p *' sessions below (the REV window, the value session, the INTSTAT reassert
        channel, the TIME pair, and the residual ACCEPT cells).  Every one runs AFTER a refused lb at +0x07, so the
        latch is SET while the row is measured -- which is the whole point.
     8  ALREADY PINNED post-latch by an incidental access in an existing session.  Derived, not asserted:
        opus_close7_20260915/scripts2/session_map2.py (static, no emulator) maps all 45 sessions and finds 72 accepted
        accesses after their session's first refusal, in 11 sessions, 10 carrying an oracle.
    10  EQUIVALENT at the guest -- nothing to observe, so no row is owed or possible.
     5  HOST-DIAGNOSTIC ONLY: clause-(e) debt.  *** THIS ENTRY SAID "DISCLOSED with its measurements RATHER THAN
        ROWED" AND THEN NAMED ONLY THREE CELLS AGAINST A COUNT OF FIVE -- grok, closing pass 8, and both halves are
        wrong.  (i) The parenthetical names CONTROL 0x0201 at two widths and the `sw +0x04' write line = THREE; the
        bucket says FIVE, and the missing two are not named anywhere.  (ii) "rather than rowed" is STALE: repair 13's
        `p acc ctl msg' COUNTS the three accepted CONTROL writes, so the 0x0201 cells now have a row that moves on
        them, whatever the bucket calls them. ***  NAMED, with what is measured about each:
          CONTROL 0x0201 4W and 8W (F1/F1b, 157/157 on the 157-row test): host-log only -- the `unimplemented' count
            drops to one, `CTL after ld' is 0x100 either way; a MULTI-AXIS idata joint, which the 2026-09-04 pass-11
            amendment puts in debt.  NOW ALSO COUNTED by `p acc ctl msg'.
          `sw +0x04' write line (F3, 157/157 on the 157-row test): guest-equivalent; `dflt ctl' counts READS at +0x04
            and nothing counts writes there.
          THE REMAINING TWO ARE UNNAMED IN THIS RECORD AND THAT IS THE DEFECT, not a rounding: a bucket whose members
            cannot be listed cannot be audited, and minimax independently reported it could not check them from the
            packet ("4 are named; 6 are not" of the EQUIVALENT bucket, the same shape of hole).  OWED: enumerate both
            buckets member by member from session_map2.py's output, or state that the counts are derived and the
            members unlisted.
    --
    46  = the ACCEPTS entry count (46 ENTRIES, six KINDS).

*** THE TIME 4W/4R PAIR IS A FLOOR CELL AND ITS ROWS NEEDED A PARTICULAR SHAPE, which is this repair's own evidence
that a CHANNEL line must be RUN against its mutant and not merely written.  The seat that proposed the rows measured
its own first two shapes VACUOUS, and one gave a FALSE RED on a control.  Only the GAPPED form discriminates: the
refused lb and the first 8R in one `step 2', the 4-byte cell in its own `step 1', the final 8R in another -- the
debugger's pause BETWEEN steps is the gap, so an update that happens lands before the final read and one that is
skipped arrives after it.  ~13,000x separation (base 0x13414f8 against the bypass's 0x5ee), reproduced here. ***

*** REPAIR 14 (2026-09-17).  WHAT THIS DETECTOR NOW COVERS ON THE **ACCEPT** SIDE, AND WHAT IT DOES NOT. ***
  Repair 13 closed the latch-SET half of the accept product.  Closing pass 8 then measured FIVE mutants at
  188/188, and the repair-14 panel measured TWO more on a face the enumeration never named.  This block says  [188-row]
  which cells are now rowed and which are deliberately not, per clause (e).

  NOW ROWED (each with its channel named at the row, and each shape MEASURED before it was shipped):
    entry 14  sd +0x08 = 0x0201   `p acc ctl msg' count 3 -> 4.  The row counted the `sw' twin and not the
                                  `sd': same address, same value, OTHER WIDTH.  The #499 shape reproduced
                                  inside the row that closed the #499 family.  L2.
    entry 21  lw +0x10            BOTH latch states (`acc istat lw', `p acc istat lw').  The twins already
                                  read INTSTAT at EIGHT bytes and neither read it at FOUR.
                                  *** THE SEED IS LOAD-BEARING: a 4-byte read at +0x10 answers the HIGH 32
                                  bits, so the interrupt state must be seeded ABOVE BIT 31 or the row answers
                                  0 -- which is what a DECLINE answers, making it green under its own
                                  mutant. ***
    entries 32 and 33  sw/lw +0x38    latch CLEAR, via the GAPPED clock-advance channel (`c t4w gap',
                                  `c t4r gap', control `c t gap once' wanting [0, 0] -- the OPPOSITE of its
                                  POST twin, because a session that announces has set the latch).
    entry 46  ld +0x278           latch CLEAR (`top8 clear').  It was already rowed post-refusal; this is the
                                  same read in the session's accepted-only prefix.
    CONTROL 4R                    AS A PAIR (`acc ctl4r'/`acc ctl0c' and the POST twins), NEVER `lw +0x08'
                                  alone: +0x08 takes the HIGH lane of 0x100 and answers 0, and so does a
                                  decline, so that row alone is 0 == 0.  +0x0c takes the LOW lane and answers
                                  0x100.

  EQUIVALENT, WITH THE DERIVATION RATHER THAN THE ASSERTION (no row owed, and this is why):
    entries 1, 3   sd/sw +0x00    the prelude re-forces CRIME_REV at :229 on EVERY access, and REV is read
                                  nowhere else in the file.  Outside the PROM window the arm body is empty.
    entries 4, 8   lw +0x00/+0x08 the 4-byte read takes the HIGH lane (:293-294) and answers 0; a declined
                                  read answers 0.  No channel can separate them, which is exactly why the
                                  CONTROL cell is rowed as a PAIR above instead.

  HOST-DIAGNOSTIC, not guest-visible:
    entry 40  sw +0x04            host log only; already so recorded in this header.

   *** CORRECTION 2026-09-17, from the OWED pass 2 (grok).  VERIFIED IN dev_sgi_ip32.c BEFORE
       BEING WRITTEN HERE.  Full working: artifacts/crimewidthkill/repair14_20260916/
       L4_CORRECTIONS_20260917.md.  PRETABLE.out is deliberately NOT edited -- its mtime is the
       proof that it preceded table 1, and an edit would destroy that. ***

     DO NOT READ THE `default:' ARM AS HOST-LOG-ONLY IN GENERAL.  It is not, for `acc ctl0c'.
     THE WIDTH ARM RUNS BEFORE THE SWITCH -- `} else if (len == 4) {' then
     `odata = d->reg[relative_addr / 8]' -- and `0x0c / 8 == 0x08 / 8 == 1'.  So a 4-byte read at
     +0x0c takes CONTROL's LOW half (0x100) out of the width arm and only THEN falls to `default:'
     for a debug print.  A DECLINE skips the width arm and answers 0.
     **That is a GUEST-VISIBLE difference, not a host-log one** -- so +0x0c IS separable, where
     +0x00/+0x08 (HIGH lane, 0 either way -- the entries-4/8 note above) are not.

     AND THE CONSEQUENCE, which is the finding rather than the correction:
     *** `acc ctl0c' NEVER REDS UNDER ANY OF THE FIFTEEN LEGS OF TABLE 12 *** -- including
     `G_clr_ctl4r', the equivalent-cell decline the PAIR was added to make observable.  That
     mutant is `relative_addr == CRIME_CONTROL' (0x08); +0x0c is a DIFFERENT switch label.  Same
     storage, different switch.  So the DISCRIMINATING half of the pair carries no measured kill.
     Accept-row failability says a row is not discharged by EXISTING.  **Do NOT add a row -- the
     rows already exist.**  Either run a decline that actually reaches 0x0c, or stop claiming
     `ctl0c' as `G_lane_ctl''s channel.

*** AND THE FACE THIS DETECTOR DOES **NOT** YET CLOSE, STATED PLAINLY BECAUSE A CONTRACT THAT HIDES ITS
    HOLES IS WORSE THAN NONE. ***
  THE DECLINE-SUPPRESSION FACE.  The `goto crime_declined' SKIPS the register switch, and what it skips is
  an OMISSION -- it reads, writes and tests nothing -- so every floor clause in this project enumerates the
  EMPTY SET over it.  Two mutants that condition the `goto' on a LABEL score 188/188 against this probe:  [188-row]
      M3_timelatch   the goto moved inside the latch block, exempting CRIME_TIME  -- 188/188  [188-row]
      M5_revlatch    the same at CRIME_REV                                        -- 188/188  [188-row]
  with M4_timeplain (the same edit WITHOUT the latch conjunct) killed at 184/188 and M6_istlatch (the same  [188-row]
  edit at INTSTAT) killed at 185/188 -- the controls that make those two escapes mean `no row looked'.  [188-row]
  *** OF THE FIVE GUEST-OBSERVABLE LABELS ON THAT FACE, THREE HAVE BEEN SWEPT (INTSTAT killed, TIME and REV
  escaping) AND **INTMASK AND CONTROL-WRITE ARE COVERED ONLY BY READING, NEVER MEASURED**.  Deriving them
  covered is the same move that M5_revlatch was built to punish: REV was DERIVED open and then MEASURED
  open. ***  Carriers for TIME and REV, and label-swap mutants for INTMASK and CONTROL-write, are OWED and
  are not in this file yet.

DISCLOSED, not rowed:
  * `goto crime_declined' -> `return 1' is EQUIVALENT on every channel: memory_rw pre-zeroes a device read buffer
    (#95, src/cpus/memory_rw.c -- `if (writeflag == MEM_READ)' then `memset(data, 0, len);', immediately above
    `paddr -= mem->devices[i].baseaddr;'), and on a declined access nothing between the entry and the tail writes
    HARDINT or SOFTINT, so the tail's restore and recompute are identities.  Measured 40/40 (the then 40-row test) in kill table 1.
  * a fall-through confined to the THREE label cells whose arms have NO body for that access, all EQUIVALENT:
      CRIME_DOG (0x30)          `No warning.' -- the arm is `break;'
      CRIME_CONTROL, reads      the arm acts only on MEM_WRITE
      CRIME_REV, outside the PROM-probe window   the arm acts only when the pc is in the window
    The first two measured as survivors in kill table 2 (`!= CRIME_DOG', the CONTROL-read-only fall-through); the REV
    cell is the `lb/lh rev pc' rows' converse, read from the arm.  [This said "the two label cells" until repair 12 --
    kimi CLI, closing pass 6.]
  * ACCEPT cells at unrowed slots: the rows touch accepted accesses at +0x00, +0x04, +0x08, +0x10, +0x18, +0x30,
    +0x34, +0x38, +0x40, +0x210, +0x214, +0x1f8 and +0x278 (not an exhaustive list of what the window accepts); an
    accept arm narrowed by an address strictly INSIDE the window at an unrowed slot (e.g. `len == 8 && relative_addr !=
    0x100', kill table 2's acc8mid, 71/71 on the 71-row test) is not seen.  TOUCHING a slot in ACCEPTS pins its LATCH
    behaviour, never its acceptance -- what pins acceptance is item 6 (`latch said' for the announced form, the value
    rows for the silent form).  [This bullet implied a touched slot was pinned until repair 12 -- the Opus seat, closing
    pass 6.]
  * an effect ADDED to the decline arm and keyed on ONE UNNAMED offset (item 9 rows the READ answer at every named
    label) -- a refused store that lands only at
    +0x31, a declined read answering nonzero only at +0x20, a silent decline only at +0x100, a fall-through only at
    +0x40 (kimi CLI, glm, F2).  The rows pin the refusal floor at every observable LABEL and at eight default-arm
    offsets; the keeps rows catch a landing at CRIME_DOG, INTMASK, the far block and the middle block.  An effect
    keyed on a single ADDRESS BIT is NOT in this class: every bit 0-9 is carried both ways by a refused access of each
    kind that can carry it (the mid session sets bits 0-8, the far block bit 9; an aligned 2-byte access never sets
    bit 0; kimi-k3:cloud, second closing pass, found bits 7 and 8 carried by no refusal at all; codex and the Opus seat,
    fourth closing pass, found 2W LANDING at bit 1 set carried by no read-back store -- now +0x42, `lo keeps').  Note
    `relative_addr / 8': a refused halfword at +0x1e would land on INTMASK's slot, not at +0x1e; the 2W session's
    +0x1e store is not read back, and the INTMASK landing is carried by `imask keeps'.  A landing at
    CRIME_SOFTINT (0x20, not a switch label) is in this class (deepseek, third closing pass).  ONE NAMED CELL IS
    OPEN AND SAID SO (kimi-k3:cloud, closing pass): a refused sb/sh that LANDS only at CRIME_TIME stores <= 0xffff,
    which the time rows' 0.1 s threshold cannot tell from the 66-990 the first tick adds -- clause (e) debt.  At INTSTAT
    (the tail recomputes it), CONTROL and REV (the prelude rewrites them) such a landing is EQUIVALENT.
  * a ROUND TRIP cannot observe an accepted WRITE at +0x00 or +0x08 (the prelude rewrites CRIME_REV and CRIME_CONTROL
    on every access) -- but the write's EFFECTS can, and are rowed: from the PROM-probe window an accepted write
    REDIRECTS the pc (revP sw pc, revP sd pc), and at CONTROL the arm's effects (sw08 halts, sw08 msg ctl at 4 bytes;
    acc ctl sd at 8).  [This bullet said "no round trip there can observe whether the store was accepted" as though
    nothing could, and it was wrong twice: the window redirect (measured by the Opus seat, G4) and the 8-byte CONTROL
    write, which no row carried until repair 12 -- closing pass 6.]  The 4R-high cell at +0x00 is carried by `rev pc
    ctl' (its redirect needs the access ACCEPTED), not by `devsig hi', whose 0 a refused read also returns.
  * `odata = idata' in the decline arm: EQUIVALENT by construction -- `idata' is set only under MEM_WRITE and `odata' is
    consumed only under MEM_READ (measured 141/141 on the 141-row test by the Opus seat, closing pass 6).  `cpu->is_32bit' (the REV arm's
    pc-pointer refresh) holds one value per machine, like the configuration lvalues above.  Accepted-side address bits 7
    and 8: the mid session's accepted sd +0x1f8 carries both, before and between its refusals (a latch keyed on them is
    killed -- kimi-k3's C3, 139/141 on the 141-row test); an ACCEPT arm keyed on them is the unrowed-slot class above.
  * ACCEPTS has 46 ENTRIES, not 46 kinds: the 40-cell pre-set/re-arm floor, the two ENDIANESS strengthenings, and four
    positional repeats of default-arm kinds (`sw/lw 0x04' repeat 0x34's low lane; `sd/ld 0x278' repeat 0x40's 8-byte
    kinds, and are the prologue's only accepted access with address bit 9 set -- an unrecorded strengthening until
    repair 12; kimi CLI, closing pass 6).
  * a decline answering a selection of the register's bytes at CRIME_REV, CRIME_CONTROL or CRIME_TIME CONFINED to
    bytes the model holds at 0 there -- REV = 0x11: bytes 1-7; CONTROL = 0x100: byte 0 and bytes 2-7; TIME: the 4-byte
    half above the low word -- is EQUIVALENT (the prelude rewrites REV and CONTROL on every access; TIME is kept to 32
    bits).  [Corrected 2026-09-14 from closing pass 5 (glm): this read "the ADDRESSED lanes (bytes 0-1 at a label)",
    which at REV and CONTROL include a NONZERO byte -- item 9's v0 rows exist to catch exactly that selection.]  At
    INTSTAT, INTMASK and DOG every byte is seeded nonzero, so any selection shows (Opus, second closing pass; glm, third).
  * a latch keyed on a JOINT predicate (e.g. only 2-byte refusals at CRIME_TIME), or on one unnamed offset other than the
    default-arm cells the latch rows refuse at: clause (e), the single-axis generating set being the floor.
  * (closing pass 5; the Opus seat measured each at 141/141 on the 141-row test; the flagship ruling graded each clause
    (e)) a latch re-armed or pre-set by a CONTROL write's ENDIANESS bit (0x100) -- the arm clears it unconditionally and
    never branches on it; the two ENDIANESS writes in ACCEPTS since repair 11 are a strengthening, not a floor claim
    over value bits; the announce CHANNEL keyed on a JOINT of axes (e.g. `(relative_addr == CRIME_INTSTAT && len == 2 ?
    debug : fatal)(') -- item 5 rows the channel on each SINGLE axis; and a decline answering a MACHINE-CONFIGURATION
    lvalue (`d->use_fb', `flag_for_128MB'), which holds one value per machine and is 0 on this probe's -M 64 non-graphics
    ip32 -- a graphics O2 (use_fb = 1) would see `odata = d->use_fb' answer 1.  Unrowable on one machine, like the
    function-static latch below.
  * a re-arm or pre-set inside the HARD_RESET branch of the CONTROL arm: an accepted write that takes it stops every
    CPU, so nothing can follow it in the session.  Unrowable, not merely unrowed.
  * a fall-through only at CRIME_SOFTINT (0x20), which the switch does not name -- measured 71/71 (the 71-row test) by the Opus seat
    (F2, `sft'); it is the single-unnamed-offset class of the bullet above.
  * a FUNCTION-STATIC latch in place of `d->warned' is NOT equivalent in general -- two IP32 machines in one gxemul
    process would share it -- and this single-machine probe cannot see it (kimi-k3:cloud, F2; the pass-2 Opus seat had
    recorded it "equivalent", which holds only for one machine per process).
  * widths 3, 5, 6, 7 (no MIPS load/store issues them); the unaligned-pair instructions (lwl/lwr/swl/swr, ldl/ldr) are
    not rowed.  The RAM-size checks ABOVE the width arm (`-M 48' exits at the first CRIME access) are filed, not here.
  * independence between two CRIME instances (the latch is per instance by construction; IP32 has one CRIME).

Sentinel: CRIMEP_DONE (plus CRIMEP_RESULT=n/N and CRIMEP_CONTROL=OK|FAIL).
"""
import os, pty, re, select, signal, sys, time

BIN = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"
DUMMY = "/tmp/dummy_crimep.bin"
if not os.path.exists(DUMMY):
    with open(DUMMY, "wb") as f:
        f.write(b"\0" * 16)

CODE = 0x80001000
SCRATCH_RAM = 0xa0001800
LIVE_VAL = 0x12345678
CRIME = 0xb4000000
SENT = 0xdeadbeef
RA = 0x80004000
PROBE_PC = 0xbfc05180           # inside the CRIME_REV hack's window, (pc & 0xffffff00) == 0xbfc05100

R = {"zero": 0, "at": 1, "v0": 2, "v1": 3, "a0": 4, "a1": 5, "a2": 6, "a3": 7, "t0": 8, "t1": 9,
     "s0": 16, "s1": 17, "s2": 18, "s3": 19, "s4": 20, "ra": 31}
OPC = {"lb": 0x20, "lh": 0x21, "lw": 0x23, "lbu": 0x24, "lhu": 0x25, "ld": 0x37,
       "sb": 0x28, "sh": 0x29, "sw": 0x2b, "sd": 0x3f}
OP_B_SELF = 0x1000ffff
OP_NOP = 0


def enc(op, rs, rt, imm=0):
    return (OPC[op] << 26) | (R[rs] << 21) | (R[rt] << 16) | (imm & 0xffff)


#  hand-assembled encodings checked against the committed witness's constants (a wrong register field reads 0, which
#  a decline's own answer would accept by accident -- so the accept rows carry nonzero wants)
assert enc("lb", "at", "v0") == 0x80220000 and enc("lhu", "at", "v0") == 0x94220000
assert enc("sb", "a3", "t0") == 0xa0e80000 and enc("sh", "a3", "t0") == 0xa4e80000
assert enc("sw", "a3", "t0") == 0xace80000 and enc("lw", "at", "v0") == 0x8c220000
#  #529 repair 14 (L1 fix): s4 is register 20 and was added for the CONTROL-pair rows, whose first form read
#  a3 -- the register st() uses to hold its ADDRESS -- so six later stores clobbered it and the base leg
#  scored 202/204.  A wrong register field reads 0, and 0 is what a DECLINE answers, so the encoding is
#  pinned here rather than trusted.
assert enc("lw", "at", "s4") == 0x8c340000

rows = []


def row(name, got, want, note=""):
    ok = (got == want)
    rows.append((name, ok))
    print("%-16s %-20s %-20s %-40s %s" % (name, str(got), str(want), note, "ok" if ok else "FAIL"))
    sys.stdout.flush()


def session(cmds, settle=1.5, spin=1.2):
    """one emulator, read to the pty's EOF after `quit'.  Returns (text, clean): clean = EOF reached AND exit 0."""
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "sgi", "-e", "ip32", "-M", "64", "0x80001000:" + DUMMY])
        os._exit(127)
    buf = ""

    def rd(t):
        nonlocal buf
        end = time.time() + t
        while time.time() < end:
            r, _, _ = select.select([fd], [], [], 0.1)
            if not r:
                continue
            try:
                d = os.read(fd, 65536)
            except OSError:
                return False
            if not d:
                return False
            buf += d.decode("latin-1", "replace")
        return True

    rd(settle)
    for i, c in enumerate(cmds):
        try:
            if c == "<RUN>":        # free-run: `continue', let the guest run, then break back in with CTRL-C
                os.write(fd, b"continue\n")
                ok = rd(2.0)
                os.write(fd, b"\x03")
                ok = ok and rd(1.5)
            else:
                os.write(fd, (c + "\n").encode("latin-1"))
                ok = rd(spin if i == len(cmds) - 1 else 0.25)
        except OSError:
            break
        if not ok:
            break
    eof = True                      # a process already gone before `quit' has closed the pty; its status says how
    try:
        os.write(fd, b"quit\n")
        eof = not rd(10.0)          # to EOF, so anything printed on the way out is in the transcript
    except OSError:
        pass
    if not eof:
        try:
            os.kill(pid, signal.SIGKILL)    # a session that never reached EOF is ended, never waited on forever
        except OSError:
            pass
    try:
        os.close(fd)
    except OSError:
        pass
    how = "nostatus"
    try:
        _, stat = os.waitpid(pid, 0)
        how = ("sig%d" % os.WTERMSIG(stat)) if os.WIFSIGNALED(stat) else ("exit%d" % os.WEXITSTATUS(stat))
    except OSError:
        pass
    return buf.replace("\r", ""), (eof and how == "exit0")


def pr(t, reg):
    m = re.search(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
    return ("0x%x" % int(m.group(1), 16)) if m else "absent"


def exc(t):
    c = pr(t, "cause")
    return ("%d" % ((int(c, 16) >> 2) & 0x1f)) if c != "absent" else "absent"


def count(t, s, clean):
    """a text count is evidence only from a whole transcript: an unclean session reads `unclean', never a number"""
    return t.count(s) if clean else "unclean"


class Addr(object):
    def __init__(self, base):
        self.a = base

    def take(self, n):
        got = self.a
        self.a += 4 * (n + 2) + 0x20
        return got


def run_ops(ops, at):
    put = ["put w 0x%x, 0x%08x" % (at + 4 * i, op) for i, op in enumerate(ops)]
    put += ["put w 0x%x, 0x%08x" % (at + 4 * len(ops), OP_B_SELF),
            "put w 0x%x, 0x%08x" % (at + 4 * len(ops) + 4, OP_NOP)]
    return put + ["pc=0x%x" % at, "step %d" % len(ops)]


def ld(A, op, addr, rt, at=None):
    """one load `op rt, 0(at)', rt seeded with SENT; returns (cmds, code address)"""
    here = A.take(1) if at is None else at
    return ["at=0x%x" % addr, "%s=0x%x" % (rt, SENT)] + run_ops([enc(op, "at", rt)], here), here


def st(A, op, addr, val, at=None):
    here = A.take(1) if at is None else at
    return ["a3=0x%x" % addr, "t0=0x%x" % val] + run_ops([enc(op, "a3", "t0")], here), here


AFTER = ["print pc", "print cause"]


def roundtrip(A):
    """a RAM round trip printed in v1: absent if the host died, the sentinel if the CPU was stopped"""
    c1, _ = st(A, "sw", SCRATCH_RAM, LIVE_VAL)
    c2, _ = ld(A, "lw", SCRATCH_RAM, "v1")
    return c1 + c2 + ["print v1"]


def said(t, ln, off, clean):
    """the whole announce, `(once)' marker included -- a reworded or unmarked announce reads 0"""
    return count(t, "unimplemented len=%d at 0x%x -- declined.  (once) ]" % (ln, off), clean)


def dflt(t, clean, off, write):
    """the register switch's default-arm debug() line FOR THIS REFUSED ACCESS -- `[ crime: read from 0xOFF,' or
    `[ crime: write to 0xOFF:' -- printed while stepping, so a refused access that falls into the switch at an
    unlabelled offset says so here.  Keyed on the access's own offset and direction, because an ACCEPTED access at a
    default-arm offset in the same session prints the same kind of line (hi keeps' ld +0x278 does)."""
    if not clean:
        return "unclean"
    return t.count(("[ crime: write to 0x%x:" if write else "[ crime: read from 0x%x,") % off)


print("CRIME WIDTH PROBE (#529) -- rung 3, unmodified -E sgi -e ip32   binary=%s  label=%s" % (BIN, LABEL))
print("%-16s %-20s %-20s %-40s %s" % ("row", "got", "want", "note", ""))

# ---- CONTROLS: liveness + device signature, one session ----
A = Addr(CODE)
c = roundtrip(A)
x, _ = ld(A, "lw", CRIME + 4, "s1"); c += x
x, _ = ld(A, "lw", CRIME + 0, "s2"); c += x
x, _ = ld(A, "ld", CRIME + 0, "s3"); c += x
t, clean = session(c + ["print s1", "print s2", "print s3"])
row("live", pr(t, "v1"), "0x%x" % LIVE_VAL, "LIVENESS: RAM round trip, same apparatus")
row("devsig", pr(t, "s1"), "0x11", "CRIME_REV low half = rev 0x11: a device")
row("devsig hi", pr(t, "s2"), "0x0", "CRIME_REV high half reads 0")
row("dflt ctl", count(t, "[ crime: read from 0x4,", clean), 1, "CONTROL: default-arm text prints when stepped")
#  grok, closing pass: the NEAR end of the 8-byte accept window is +0x00, not CRIME_DOG -- `len == 8 && relative_addr
#  != 0' passed the 85-row version.  Anchored: the prelude writes CRIME_REV's revision on every access, so an 8R there
#  reads 0x11 from a channel outside the decode (an 8W round trip there is impossible for the same reason: disclosed).
row("acc8 near", pr(t, "s3"), "0x11", "8R at +0x00 (the window's first slot): CRIME_REV")

# ---- the switch channels are LIVE on an accepted width (else rows 3.x could not vary) ----
A = Addr(CODE)
x, _ = ld(A, "lw", CRIME + 0, "v0", at=PROBE_PC)
t, clean = session(["ra=0x%x" % RA] + x + AFTER)
row("rev pc ctl", pr(t, "pc"), "0x%x" % RA, "CONTROL: lw CRIME_REV from 0xbfc051xx -> ra")

A = Addr(CODE)
x, _ = st(A, "sw", CRIME + 0x08, 0x0800)
t, clean = session(x + AFTER + roundtrip(A))
row("sw08 halts", pr(t, "v1"), "0x%x" % SENT, "CONTROL: sw 0x800 +0x08 stops CPUs (crimectllane)")

A = Addr(CODE)
x, _ = st(A, "sw", CRIME + 0x08, 0x01)
t, clean = session(x + AFTER + roundtrip(A))
row("sw08 msg ctl", count(t, "CRIME_CONTROL: unimplemented", clean), 1, "CONTROL: sw 0x01 +0x08 prints the text")

# ---- ACCEPT cells on CRIME_DOG (0x030): 8W, 8R, 4R hi/lo, 4W lo/hi -- nonzero wants ----
A = Addr(CODE)
c = []
x, _ = st(A, "sd", CRIME + 0x30, 0x1122334455667788); c += x   # 8W
x, _ = ld(A, "ld", CRIME + 0x30, "a0"); c += x                  # 8R
x, _ = ld(A, "lw", CRIME + 0x30, "a1"); c += x                  # 4R high half
x, _ = ld(A, "lw", CRIME + 0x34, "a2"); c += x                  # 4R low half
x, _ = st(A, "sw", CRIME + 0x34, 0x0badcafe); c += x            # 4W low half
x, _ = ld(A, "ld", CRIME + 0x30, "s0"); c += x
x, _ = st(A, "sw", CRIME + 0x30, 0x0defaced); c += x            # 4W high half
x, _ = ld(A, "ld", CRIME + 0x30, "s3"); c += x
t, clean = session(c + ["print a0", "print a1", "print a2", "print s0", "print s3"])
row("acc8 st+ld", pr(t, "a0"), "0x1122334455667788", "8W then 8R at CRIME_DOG")
row("acc4 rhi", pr(t, "a1"), "0x11223344", "4R of the high half (+0x30)")
row("acc4 rlo", pr(t, "a2"), "0x55667788", "4R of the low half (+0x34)")
row("acc4 wlo", pr(t, "s0"), "0x112233440badcafe", "4W low half lands, high half kept")
row("acc4 whi", pr(t, "s3"), "0xdefaced0badcafe", "4W high half lands, low half kept")

# ---- REFUSED widths, one session each: value, pc, exccode, survival, own announce ----
for op, off, full in (("lb", 7, True), ("lh", 6, True), ("lbu", 7, False), ("lhu", 6, False)):
    A = Addr(CODE)
    x, here = ld(A, op, CRIME + off, "v0")
    t, clean = session(x + AFTER + ["print v0"] + roundtrip(A))
    ln = 1 if op in ("lb", "lbu") else 2
    row("%s v0" % op, pr(t, "v0"), "0x0", "declined read answers 0 (dest seeded 0x%x)" % SENT)
    if full:
        row("%s pc" % op, pr(t, "pc"), "0x%x" % (here + 4), "pc advances, no vector")
        row("%s exc" % op, exc(t), "0", "cause.ExcCode 0 (a bus error is 7)")
        row("%s said" % op, said(t, ln, off, clean), 1, "own announce, len=%d at 0x%x, once" % (ln, off))
        row("%s nodflt" % op, dflt(t, clean, off, False), 0, "switch default arm NOT reached at 0x%x" % off)
    row("%s surv" % op, pr(t, "v1"), "0x%x" % LIVE_VAL, "host survives, then a RAM trip")

for op, off, val in (("sb", 0x1f, 0xff), ("sh", 0x1e, 0xffff)):
    A = Addr(CODE)
    x, here = st(A, op, CRIME + off, val)
    t, clean = session(x + AFTER + roundtrip(A))
    ln = 1 if op == "sb" else 2
    row("%s pc" % op, pr(t, "pc"), "0x%x" % (here + 4), "pc advances, no vector")
    row("%s exc" % op, exc(t), "0", "cause.ExcCode 0 (a bus error is 7)")
    row("%s said" % op, said(t, ln, off, clean), 1, "own announce, len=%d at 0x%x, once" % (ln, off))
    row("%s nodflt" % op, dflt(t, clean, off, True), 0, "switch default arm NOT reached at 0x%x" % off)
    row("%s surv" % op, pr(t, "v1"), "0x%x" % LIVE_VAL, "host survives, then a RAM trip")

# ---- the switch is NOT entered by a refused width, per cell (contract 3) ----
A = Addr(CODE)
x, here = st(A, "sh", CRIME + 0x08, 0x0800)
t, clean = session(x + AFTER + roundtrip(A))
row("sh08 pc", pr(t, "pc"), "0x%x" % (here + 4), "2W sh 0x800 +0x08: pc advances")
row("sh08 run", pr(t, "v1"), "0x%x" % LIVE_VAL, "2W: CPUs NOT stopped (RAM trip runs)")

A = Addr(CODE)
x, here = st(A, "sb", CRIME + 0x08, 0x01)
f, _ = st(A, "sb", CRIME + 0x08, 0xff)          # all-ones (kimi CLI, closing pass): a fall-through keyed on ANY bit
t, clean = session(x + f + AFTER + roundtrip(A))
row("sb08 msg", count(t, "CRIME_CONTROL: unimplemented", clean), 0, "1W sb 0x01, 0xff +0x08: no CONTROL text")
row("sb08 run", pr(t, "v1"), "0x%x" % LIVE_VAL, "1W: the session completes (a RAM trip)")

#  THE CONTROL ARM TESTS BITS OF idata, so the 2-byte write cell owes each tested bit written both clear and set (the
#  generating-set clause; the Opus seat, F2: `relative_addr != CRIME_CONTROL || !(idata & CRIME_CONTROL_DOG_ENABLE)'
#  passed the 71-row version because no refused row carried DOG_ENABLE).  sh08 above writes HARD_RESET set / DOG clear;
#  here 0x0201 writes HARD_RESET clear / DOG set / bit 0 (the arm would print its unimplemented-control text) and 0x0a00
#  writes both set (the arm would stop every CPU).  A 1-byte write cannot carry either bit.
A = Addr(CODE)
x, _ = st(A, "sh", CRIME + 0x08, 0x0201)
e, _ = st(A, "sh", CRIME + 0x08, 0x0900)       # glm, closing pass: ENDIANESS (0x0100) -- CLEARED by the arm, never
                                               # branched on (this said "the arm's third tested bit" until repair 12)
y, _ = st(A, "sh", CRIME + 0x08, 0x0a00)
f, _ = st(A, "sh", CRIME + 0x08, 0xffff)        # all-ones: every bit a data-keyed narrowing could key on, set
#  and a follow-up refusal at ANOTHER label (the codex seat, second closing pass: a latch whose bit is keyed on one label,
#  `CRIME_W_LEN << (relative_addr == L)', is invisible to a session that refuses only at L)
g, _ = ld(A, "lb", CRIME + 0x07, "t1")
t, clean = session(x + e + y + f + AFTER + roundtrip(A) + g)
row("sh08b msg", count(t, "CRIME_CONTROL: unimplemented", clean), 0, "2W sh 0x0201 +0x08 (DOG set): no CONTROL text")
row("sh08b run", pr(t, "v1"), "0x%x" % LIVE_VAL, "2W sh 0x0900, 0x0a00 +0x08 (E/DOG+RESET): CPUs NOT stopped")
row("sh08b once", count(t, "-- declined.", clean), 1, "4 refusals at CONTROL, then +0x07: one notice")
#  the FIRST refusal's own text (codex, third closing pass: a notice suppressed at one label -- or at one address-bit
#  value -- and printed instead by the +0x07 follow-up still counts one; every said row sat at an offset with bit 1 set)
row("sh08b said", said(t, 2, 0x8, clean), 1, "sh +0x08 (first refusal): its own announce")

for op in ("lb", "lh"):
    A = Addr(CODE)
    x, _ = ld(A, op, CRIME + 0, "v0", at=PROBE_PC)
    more = ld(A, "lb", CRIME + 0x07, "v1")[0] if op == "lb" else []     # a second refusal: the REV-first latch cell
    t, clean = session(["ra=0x%x" % RA] + x + AFTER + ["print v0"] + more)
    row("%s rev pc" % op, pr(t, "pc"), "0x%x" % (PROBE_PC + 4), "%dR at CRIME_REV from 0xbfc05180: pc NOT ra"
        % (1 if op == "lb" else 2))
    row("%s rev v0" % op, pr(t, "v0"), "0x0", "refused %s at CRIME_REV answers 0" % op)
    if op == "lb":
        row("rev once", count(t, "-- declined.", clean), 1, "first refusal at CRIME_REV, then +0x07: one notice")
        row("rev said", said(t, 1, 0x0, clean), 1, "lb +0x00 (first refusal, every address bit clear): its own announce")

#  the CRIME_REV arm's PROM-probe hack does not test writeflag, so the WRITE cells at +0 are side-effect cells too
for op, val in (("sb", 0xa5), ("sh", 0xa5a5)):
    A = Addr(CODE)
    x, _ = st(A, op, CRIME + 0, val, at=PROBE_PC)
    t, clean = session(["ra=0x%x" % RA] + x + AFTER)
    row("%s rev pc" % op, pr(t, "pc"), "0x%x" % (PROBE_PC + 4), "%dW at CRIME_REV from 0xbfc05180: pc NOT ra"
        % (1 if op == "sb" else 2))

# ---- the INTSTAT / INTMASK labels: their arm calls crime_interrupt_reassert(), which is NOT idempotent -- ----
#  INTMASK = bit 28 and SOFTINT = bit 28 are stored with 8-byte writes; SOFTINT's store goes to the default arm and does
#  NOT reassert, so the CPU's IP2 (cause bit 0x400) stays low until something reasserts.  A refused access at the label
#  must leave it low; the accepted `lw' that follows is the CONTROL that the arm reasserts at once.  (Measured by the
#  pass-2 Opus seat, opus_pass2_20260913/scripts/crime_p2_escape.py E1/E2: a fall-through at the label sets IP2.)
#  BIT carries bit 0 as well (the kimi CLI seat, second closing pass): a refused read answers the low bytes of whatever
#  the decline hands the tail, so with a register whose low bytes were 0 a decline that answered THE REGISTER
#  (`odata = d->reg[relative_addr / 8]' at INTSTAT or INTMASK) read back 0 and passed.  AND in its TOP lanes (the Opus
#  second-closing seat, measured 121/121 on the 0x10000001 seed): a decline that answers the bytes the ADDRESS names --
#  `odata = d->reg[relative_addr / 8] >> (8 * (8 - len - (relative_addr & 7)))', the lane the model's own 4-byte read
#  path uses -- reads bytes 0-1 at the label, which the 0x10000001 seed left 0.  So the seed is nonzero in byte 0, byte 1
#  and the low byte; INTSTAT = SOFTINT | HARDINT and INTMASK both carry it; the reassert still sees bit 28.
#  And glm (third closing pass) found a THIRD byte selection -- the 4-byte path's half, `reg >> 32' -- whose low bytes
#  that seed left 0.  So the seed is now nonzero in EVERY byte: no selection of the register's bytes can answer 0.  (DOG,
#  the far slot and the middle slot are seeded every-byte-nonzero already.)
BIT = 0x0101010111010101


def nth(t, reg, n):
    ms = re.findall(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
    return int(ms[n], 16) if len(ms) > n else None


def ip2(v):
    return "absent" if v is None else ("set" if v & 0x400 else "clear")


for lbl, off in (("imask", 0x18), ("istat", 0x10)):
    A = Addr(CODE)
    c = []
    x, _ = st(A, "sd", CRIME + 0x18, BIT); c += x
    x, _ = st(A, "sd", CRIME + 0x20, BIT); c += x
    c += ["print cause"]
    x, _ = ld(A, "lb", CRIME + off, "a0"); c += x
    c += ["print cause"]
    x, _ = st(A, "sb", CRIME + off, 0xff); c += x
    c += ["print cause"]
    x, _ = ld(A, "lh", CRIME + off, "a1"); c += x
    c += ["print cause"]
    x, _ = st(A, "sh", CRIME + off, 0xffff); c += x
    c += ["print cause"]
    x, _ = ld(A, "lw", CRIME + off, "v0"); c += x
    c += ["print cause", "print a0", "print a1"]
    #  INTMASK read back by an accepted ld after the refused stores (kimi CLI, second closing pass: a landing that ORs
    #  into INTMASK keeps bit 28, so the reassert rows cannot see it), then a follow-up refusal at ANOTHER label (codex:
    #  a latch keyed on this one label is invisible to a session that refuses only here)
    x, _ = ld(A, "ld", CRIME + 0x18, "s2"); c += x
    x, _ = ld(A, "lb", CRIME + 0x07, "t1"); c += x
    c += ["print s2"]
    t, clean = session(c)
    row("%s pre" % lbl, ip2(nth(t, "cause", 0)), "clear", "IP2 low after SOFTINT's default-arm store")
    row("%s lb" % lbl, ip2(nth(t, "cause", 1)), "clear", "refused lb +0x%x: no reassert" % off)
    row("%s sb" % lbl, ip2(nth(t, "cause", 2)), "clear", "refused sb +0x%x: no reassert" % off)
    row("%s lh" % lbl, ip2(nth(t, "cause", 3)), "clear", "refused lh +0x%x: no reassert" % off)
    row("%s sh" % lbl, ip2(nth(t, "cause", 4)), "clear", "refused sh +0x%x: no reassert" % off)
    row("%s ctl" % lbl, ip2(nth(t, "cause", 5)), "set", "CONTROL: accepted lw +0x%x reasserts" % off)
    row("%s once" % lbl, count(t, "-- declined.", clean), 1, "4 refusals at +0x%x, then +0x07: one notice" % off)
    row("%s said" % lbl, said(t, 1, off, clean), 1, "lb +0x%x (first refusal): its own announce" % off)
    row("%s lb v0" % lbl, pr(t, "a0"), "0x0", "refused lb +0x%x answers 0 (register 0x0101..01)" % off)
    row("%s lh v0" % lbl, pr(t, "a1"), "0x0", "refused lh +0x%x answers 0 (register 0x0101..01)" % off)
    if lbl == "imask":
        row("imask keeps", pr(t, "s2"), "0x%x" % BIT, "refused sb/sh +0x18 leave INTMASK as stored (ld +0x18)")

# ---- THE DECLINE HOLDS WHILE AN INTERRUPT IS LATCHED (the Opus closing seat: `if (!d->reg[CRIME_HARDINT / 8]) goto
#  crime_declined;' passed the 85-row version -- every refusal in it ran with HARDINT == 0, and the tail the goto jumps
#  to READS HARDINT, so the field is a DEPENDS-ON operand; `if (!d->prev_asserted)' passed too).  The guest latches a
#  hardware interrupt by two MACE stores (ISA interrupt status, then mask -> crime_interrupt_assert -> HARDINT), and
#  -- INDEPENDENTLY, not as a consequence (grok, second closing pass: HARDINT's bit is not in the mask used here) --
#  asserts the CRIME line (INTMASK and SOFTINT = BIT, reasserted by an accepted lw), then a refused sh 0x0800 at
#  CRIME_CONTROL: falling into the switch there would stop every CPU.  Both states are rowed as controls: HARDINT reads
#  nonzero, and IP2 is set.
MACE = 0xbf310000                                   # KSEG1 of the `mace addr=0x1f310000' device (dev_sgi_ip32.c)
A = Addr(CODE)
c = []
for off, val in ((0x10, 0x01), (0x18, 0x01)):
    x, _ = st(A, "sd", MACE + off, val); c += x
x, _ = st(A, "sd", CRIME + 0x18, BIT); c += x
x, _ = st(A, "sd", CRIME + 0x20, BIT); c += x
x, _ = ld(A, "lw", CRIME + 0x18, "a0"); c += x
x, _ = ld(A, "ld", CRIME + 0x28, "s2"); c += x
c += ["print s2", "print cause"]
#  refused READS while HARDINT is nonzero (kimi-k3:cloud, fourth closing pass; the Opus seat measured it: a decline
#  answering `d->reg[CRIME_HARDINT / 8]' scored 131/131 -- HARDINT is nonzero ONLY in this session, which read no refused
#  answer; it answered 0x20 at both widths here).  The one answer SOURCE every other session left at 0.
x, _ = ld(A, "lb", CRIME + 0x08, "t1"); c += x
x, _ = ld(A, "lh", CRIME + 0x08, "s3"); c += x
x, _ = st(A, "sh", CRIME + 0x08, 0x0800); c += x
t, clean = session(c + ["print t1", "print s3"] + roundtrip(A))
hint = nth(t, "s2", 0)
row("gate hardint", "set" if hint else ("absent" if hint is None else "clear"), "set",
    "CONTROL: two MACE stores latch HARDINT (raw %s)" % hint)
row("gate line", ip2(nth(t, "cause", 0)), "set", "CONTROL: the CRIME line is asserted")
row("gate run", pr(t, "v1"), "0x%x" % LIVE_VAL, "refused sh 0x800 +0x08 with an irq latched: CPUs run")
row("gate lb v0", pr(t, "t1"), "0x0", "refused lb +0x08 with HARDINT nonzero answers 0")
row("gate lh v0", pr(t, "s3"), "0x0", "refused lh +0x08 with HARDINT nonzero answers 0")

# ---- the TIME label: an accepted read returns the value of the PREVIOUS update, then updates -- so a refused access
#  that reached crime_update_crime_time() would show in the NEXT read.  The first `ld' latches last_microseconds; on the
#  fixed build the only other update before the next `ld' is the device tick's FIRST firing -- ticks_till_next starts at
#  0, so it fires right after the session's first `ld' (the Opus closing seat; this said "nothing else updates TIME"
#  until then), and it adds the few microseconds since the latch: the 66-990 the rows print (measured across 52 cells
#  against SMALL = 6.6e6).  Later ticks are 2^14 cycles apart and a session steps a few dozen instructions; a fall-through at 0x38
#  makes it the wall-clock interval of the intervening debugger commands, ~1e8.  The third `ld' is the CONTROL that the
#  channel moves.  (Opus pass 2, E3; the tick-spacing wording corrected by the kimi CLI seat on the F2 pass.)
#  ASSUMPTION, disclosed: after that FIRST tick, no further tick falls between the first `ld' and the `ld' that samples
#  s1 (codex, closing pass: the window runs THROUGH the sampling read, not only to the refused access; deepseek and
#  codex, second closing pass: this sentence said "no tick boundary" while the one above names the first tick).  The IRQ rows carry the same assumption:
#  dev_crime_tick also calls crime_interrupt_reassert(), so a tick inside a session could raise IP2 on the fixed build
#  (kimi CLI, closing pass) -- a false red, never a false green; measured stable so far.
SMALL = 66 * 100000


def mag(v):
    return "absent" if v is None else ("small" if v < SMALL else "large")


for op in ("lb", "sb", "lh", "sh"):
    A = Addr(CODE)
    c = []
    x, _ = ld(A, "ld", CRIME + 0x38, "s0"); c += x
    if op in ("lb", "lh"):
        x, _ = ld(A, op, CRIME + 0x38, "v0"); c += x
    else:
        x, _ = st(A, op, CRIME + 0x38, 0xff if op == "sb" else 0xffff); c += x
    x, _ = ld(A, "ld", CRIME + 0x38, "s1"); c += x
    x, _ = ld(A, "ld", CRIME + 0x38, "s2"); c += x
    if op == "lb":                                  # a second refusal: the TIME-first latch cell
        x, _ = ld(A, "lb", CRIME + 0x07, "v1"); c += x
    t, clean = session(c + ["print s1", "print s2", "print v0"])
    s1, s2 = nth(t, "s1", 0), nth(t, "s2", 0)
    row("time %s" % op, mag(s1), "small", "after refused %s +0x38 (raw %s)" % (op, s1))
    row("time %s ctl" % op, mag(s2), "large", "CONTROL: accepted ld moved TIME (raw %s)" % s2)
    if op in ("lb", "lh"):
        row("time %s v0" % op, pr(t, "v0"), "0x0", "refused %s +0x38 answers 0" % op)
    if op == "lb":
        row("time once", count(t, "-- declined.", clean), 1, "first refusal at CRIME_TIME, then +0x07: one notice")
        row("time said", said(t, 1, 0x38, clean), 1, "lb +0x38 (first refusal): its own announce")

# ---- a refused store leaves the register it names untouched (CRIME_DOG seeded by an accepted sd) ----
A = Addr(CODE)
c = []
x, _ = st(A, "sd", CRIME + 0x30, 0x0123456789abcdef); c += x
x, _ = st(A, "sb", CRIME + 0x37, 0xa5); c += x
x, _ = ld(A, "ld", CRIME + 0x30, "a0"); c += x
x, _ = st(A, "sh", CRIME + 0x30, 0x5a5a); c += x
x, _ = ld(A, "ld", CRIME + 0x30, "a1"); c += x
#  the codex seat, F2: every other refused read runs in a COLD session, so an `odata' that survived from the previous
#  call (`static uint64_t idata = 0, odata = 0;') answered 0 there by luck.  Here a refused lbu follows accepted reads
#  of a nonzero register; and the announce count across refused-accepted-refused catches a latch re-armed by an
#  accepted access (`d->warned = 0;' in an accept arm), which `latch x5' -- no accepted access -- cannot.
x, _ = ld(A, "lbu", CRIME + 0x07, "v0"); c += x
#  a SEEDED slot with address bit 4 CLEAR (the Opus third-closing seat, measured: every refused store the rows read back
#  had bit 4 set, so a landing keyed on bit 4 clear passed); +0x40 reaches the default arm
x, _ = st(A, "sd", CRIME + 0x40, 0x0123456789abcdef); c += x
x, _ = st(A, "sb", CRIME + 0x47, 0xff); c += x
x, _ = st(A, "sh", CRIME + 0x44, 0xffff); c += x
#  and a refused HALFWORD with address bit 1 SET (codex, fourth closing pass; the Opus seat measured it: every read-back
#  refused 2-byte store cleared bit 1 -- +0x18, +0x30, +0x44, +0x1fc, +0x27c -- so a 2W landing keyed on bit 1 scored
#  131/131).  +0x42 / 8 is the +0x40 slot, which `lo keeps' reads back.
x, _ = st(A, "sh", CRIME + 0x42, 0xffff); c += x
x, _ = ld(A, "ld", CRIME + 0x40, "s2"); c += x
t, clean = session(c + ["print a0", "print a1", "print v0", "print s2"])
row("sb keeps", pr(t, "a0"), "0x123456789abcdef", "refused sb +0x37 leaves CRIME_DOG as seeded")
row("sh keeps", pr(t, "a1"), "0x123456789abcdef", "refused sh +0x30 leaves CRIME_DOG as seeded")
row("warm v0", pr(t, "v0"), "0x0", "refused lbu AFTER accepted reads of 0x0123..: still 0")
row("warm once", count(t, "-- declined.", clean), 1, "refused, accepted, refused: still one announce")
row("lo keeps", pr(t, "s2"), "0x123456789abcdef", "refused sb +0x47, sh +0x44/+0x42 (bit 4 clear) leave +0x40")

#  RE-ARM, closed over every place an accepted access can go (codex, closing pass: `d->warned = 0;' in the 4-byte arm
#  passed the 85-row version -- `warm once' interleaves only 8-byte accesses; the Opus seat measured it 85/85).  One
#  refusal latches; then each ACCEPTED kind -- 8W, 8R, 4W and 4R in both lanes, and an accepted access into each switch
#  arm (DOG, TIME, INTMASK, INTSTAT, REV, CONTROL, the default arm low and in the far block) -- is followed by a refusal.
#  A re-arm anywhere an accepted access reaches shows as a second notice.  (A re-arm in the common tail, which refusals
#  also reach, shows in latch x5.)
#  The second closing pass (codex) found the arm's BRANCHES were not all reached: an accepted CONTROL write carried only
#  0, 1 or 0x800, so a re-arm inside the DOG_ENABLE branch passed.  So the CONTROL write here is 0x0201 (the DOG branch
#  and the unimplemented-control branch), the REV read runs from the PROM-probe window (its pc-redirect branch), and the
#  default arm takes a 4-byte write too.  The HARD_RESET branch cannot be followed by anything (it stops every CPU):
#  a re-arm there is DISCLOSED.
A = Addr(CODE)
c = ["ra=0x%x" % RA]
x, _ = ld(A, "lb", CRIME + 0x07, "v0"); c += x
#  The THIRD closing pass (the Opus seat, measured) found the list still built from the members earlier passes had
#  found rather than from the function: a CONTROL READ, a CONTROL write with DOG clear, and one whose leftover bits are
#  zero each re-armed at 121/121.  So the kinds are now DERIVED FROM DEVICE_ACCESS(crime)'s OWN BRANCHES -- both sides
#  of every `if' an accepted access can take and come back from: len 8 (W, R), len 4 (W, R) x (relative_addr & 4),
#  every case label, the REV pc-window test (in, out), CONTROL's writeflag test (R, W) x its DOG test (set, clear) x
#  its leftover test (nonzero, zero), the default arm (R, W).  HARD_RESET's true side stops the CPUs: disclosed.
#  *** And the FOURTH closing pass (the Opus seat, measured; kimi CLI, deepseek by reading) found that list had each
#  branch's two sides SOMEWHERE -- the marginals -- but not the KIND crossed with the LABEL the contract promises: a
#  re-arm on an accepted WRITE at INTSTAT/INTMASK or REV, a pre-set on a write at +0x10, and CONTROL's (DOG set,
#  leftover 0) cell (0x0200) each scored 131/131 while changing the announce count.  So the list is now the CROSS:
#  {8W, 8R, 4W, 4R} at every label (a label is 8-aligned, so its 4-byte access is the high lane), REV also from the
#  PROM-probe window, CONTROL's writes at both widths x {0x0201, 0x0001, 0, 0x0200}, and the default arm's six kinds
#  in both 4-byte lanes.  ONE list, used here (re-arm) AND as latch x5's prologue (pre-set). ***
#  *** REPAIR 11 (closing pass 5; flagship ruling regress/artifacts/lcaisalane/FABLE_C3_RULING_20260914.md, part A):
#  the window was crossed with 4R/4W/8W and NOT 8R -- this said "in both directions (the pc test ignores the
#  direction)", and the missing cell was the 8-byte WIDTH on reads [this read "the DIRECTION on writes only" until
#  repair 12 -- kimi-k3:cloud, closing pass 6]; five seats and the Opus seat's measurement
#  (a re-arm/pre-set keyed on an accepted 8R from the window, 141/141) put `ldP' in, as a FLOOR cell.  The two CONTROL
#  0x0100 (ENDIANESS) writes are a CLAUSE-(e) STRENGTHENING, not floor: the arm clears ENDIANESS unconditionally and
#  never branches on it, so it is outside CONTROL's generating set {DOG, HARD_RESET, leftover}; they are here only
#  because the Opus seat measured them killing an ENDIANESS-keyed latch with no row disturbed.  46 ENTRIES, six
#  KINDS -- this line said `46 kinds', the second of the two sites grok's nit named. ***
ACCEPTS = (("sd", 0x00, 0), ("ld", 0x00, 0), ("sw", 0x00, 0), ("lw", 0x00, 0),
           ("lwP", 0x00, 0), ("swP", 0x00, 0), ("sdP", 0x00, 0),
           ("lw", 0x08, 0), ("ld", 0x08, 0),
           ("sw", 0x08, 0x0201), ("sw", 0x08, 0x0001), ("sw", 0x08, 0), ("sw", 0x08, 0x0200),
           ("sd", 0x08, 0x0201), ("sd", 0x08, 0x0001), ("sd", 0x08, 0), ("sd", 0x08, 0x0200),
           ("sd", 0x10, 0), ("ld", 0x10, 0), ("sw", 0x10, 0), ("lw", 0x10, 0),
           ("sd", 0x18, 0), ("ld", 0x18, 0), ("sw", 0x18, 0), ("lw", 0x18, 0),
           ("sd", 0x30, 0), ("ld", 0x30, 0), ("sw", 0x30, 0), ("lw", 0x30, 0),
           ("sd", 0x38, 0), ("ld", 0x38, 0), ("sw", 0x38, 0), ("lw", 0x38, 0),
           ("sd", 0x40, 0), ("ld", 0x40, 0), ("sw", 0x40, 0), ("lw", 0x40, 0),
           ("sw", 0x34, 0x0badcafe), ("lw", 0x34, 0), ("sw", 0x04, 0), ("lw", 0x04, 0),
           ("ldP", 0x00, 0), ("sw", 0x08, 0x0100), ("sd", 0x08, 0x0100),
           ("sd", 0x278, 0), ("ld", 0x278, 0))
KINDS = ACCEPTS


def accept(A, op, off, val, reg="a0"):
    """one ACCEPTED access of ACCEPTS; the `P' kinds run from pc 0xbfc05180, the REV arm's redirect window (pc = ra)"""
    #  hygienecensus (2026-09-23, owner ruling): spelled `op[-1:] == "P"', not with the str method -- identical over the
    #  eight op strings ACCEPTS produces (and on ""), but gate_hygiene's spelling census counts every literal call of
    #  that method on a code line and reads one it does not recognise as a readiness predicate it cannot classify; it
    #  read got=1 want=0 on this line at the 2026-09-20 battery.  (It sees only literal spellings: a space before the
    #  paren passes it -- filed as hygienecensusholes.)  This probe has NO prompt predicate -- session() reads by timed
    #  drains -- so it is grandfathered by name as promptless; pass 2 found that an earlier wording of THIS comment
    #  had hidden that.
    if op[-1:] == "P":
        if op[0] == "s":
            x, _ = st(A, op[:2], CRIME + off, val, at=PROBE_PC)
        else:
            x, _ = ld(A, op[:2], CRIME + off, reg, at=PROBE_PC)
    elif op[0] == "s":
        x, _ = st(A, op, CRIME + off, val)
    else:
        x, _ = ld(A, op, CRIME + off, reg)
    return x


for op, off, val in KINDS:
    c += accept(A, op, off, val)
    x, _ = ld(A, "lb", CRIME + 0x06, "v0"); c += x
t, clean = session(c + roundtrip(A))
row("rearm once", count(t, "-- declined.", clean), 1, "%d refusals, %d accepted kinds between: one notice"
    % (len(KINDS) + 1, len(KINDS)))
row("rearm surv", pr(t, "v1"), "0x%x" % LIVE_VAL, "the whole interleave completes (a RAM trip)")

# ---- ACCEPT cells at the window's LAST 8-byte slot (+0x278; no case label, no prelude write) -- the far bound ----
A = Addr(CODE)
c = []
x, _ = ld(A, "ld", CRIME + 0x210, "s2"); c += x
x, _ = ld(A, "lw", CRIME + 0x214, "s1"); c += x      # 4R of the anchored slot's low half
#  4R of its HIGH half (the Opus closing seat: `len == 4 && relative_addr != 0x210' passed the 85-row version).  Its
#  value is 0 accepted or refused -- the prelude rewrites the slot on every access -- so the row is the ANNOUNCE: a
#  refused accept cell here takes the session's one notice, and `top said' below reads 0.
x, _ = ld(A, "lw", CRIME + 0x210, "t1"); c += x
x, _ = st(A, "sd", CRIME + 0x278, 0x0102030405060708); c += x
x, _ = ld(A, "ld", CRIME + 0x278, "v1"); c += x      # #529 repair 14: ACCEPTS entry 46, BEFORE the first refusal -- latch CLEAR
x, _ = ld(A, "lb", CRIME + 0x27b, "v0"); c += x      # a REFUSED read while the far slot is nonzero (Opus: rd_hi)
x, _ = ld(A, "lh", CRIME + 0x27a, "s3"); c += x      # and a refused 2-byte read there (Opus, second closing pass)
x, _ = ld(A, "ld", CRIME + 0x278, "a0"); c += x
x, _ = ld(A, "lw", CRIME + 0x278, "a1"); c += x
x, _ = ld(A, "lw", CRIME + 0x27c, "a2"); c += x
x, _ = st(A, "sw", CRIME + 0x27c, 0x0a0b0c0d); c += x
x, _ = st(A, "sw", CRIME + 0x278, 0x11112222); c += x
x, _ = ld(A, "ld", CRIME + 0x278, "s0"); c += x
t, clean = session(c + ["print s2", "print a0", "print a1", "print a2", "print s0", "print s1", "print v0",
                        "print s3", "print v1"])
row("top8 anchor", pr(t, "s2"), "0x1", "8R +0x210: bank-1 ctrl the PRELUDE wrote (-M 64)")
row("top4 anchor", pr(t, "s1"), "0x1", "4R +0x214: the anchored slot's low half")
row("top rd v0", pr(t, "v0"), "0x0", "refused lb +0x27b over a nonzero slot answers 0")
row("top rd2 v0", pr(t, "s3"), "0x0", "refused lh +0x27a over a nonzero slot answers 0")
row("top said", said(t, 1, 0x27b, clean), 1, "lb +0x27b is the first refusal: every access before it accepted")
row("top8 st+ld", pr(t, "a0"), "0x102030405060708", "8W then 8R at +0x278")
row("top8 clear", pr(t, "v1"), "0x102030405060708",
    "8R at +0x278 BEFORE this session's first refusal -- ACCEPTS entry 46, latch CLEAR")
#  *** #529 repair 14.  `M2_ld278clr' (the Opus seat's fifth escape) scores 188/188 against the shipped
#  probe.  Entry 46 WAS driven with an oracle -- the row directly above -- but only AFTER the refused
#  lb +0x27b, so the latch was SET; BUCKETS8_rerun.out names session 40, which has no value oracle, as its
#  only latch-CLEAR driver.  This row is the same read in the session's ACCEPTED-ONLY PREFIX. ***
#  The pair is the point: `top8 st+ld' and `top8 clear' read the SAME slot for the SAME value in the TWO
#  latch states, so a decline keyed on either state moves exactly one of them.
#  CONTROL: `top said' below already asserts that lb +0x27b is this session's FIRST refusal, so it is the
#  row that reds if the access added here ever stops being accepted -- no new control is owed.
row("top4 rhi", pr(t, "a1"), "0x1020304", "4R high half at +0x278")
row("top4 rlo", pr(t, "a2"), "0x5060708", "4R low half at +0x27c")
row("top4 w", pr(t, "s0"), "0x111122220a0b0c0d", "4W both halves at +0x278/+0x27c")

# ---- a refused width at the window's LAST byte: declined, announced, default arm not reached ----
#  The far slot is SEEDED first (codex, third closing pass: a refused store that CLEARS -- `&= idata' -- left the unseeded
#  slot at 0, which `hi keeps' wanted).
A = Addr(CODE)
sf, _ = st(A, "sd", CRIME + 0x278, 0x0123456789abcdef)
x, here = st(A, "sb", CRIME + 0x27f, 0xff)
w, _ = st(A, "sh", CRIME + 0x27c, 0xffff)      # a refused 2-byte store in the far block too (Opus closing: wst_mc2)
y, _ = ld(A, "ld", CRIME + 0x278, "a0")        # the refused stores' register, read back by an ACCEPTED ld
z, _ = st(A, "sb", CRIME + 0x27e, 0xee)        # follow-up refusals: one in the high block (a latch keyed on >= 0x40)
z2, _ = ld(A, "lb", CRIME + 0x07, "v0")        #   and one low (a latch whose bit depends on the block, `lt_blk')
t, clean = session(sf + x + AFTER + roundtrip(A) + w + y + ["print a0"] + z + z2)
row("hi said", said(t, 1, 0x27f, clean), 1, "sb +0x27f: own announce, once")
row("hi nodflt", dflt(t, clean, 0x27f, True), 0, "switch default arm NOT reached at 0x27f")
row("hi surv", pr(t, "v1"), "0x%x" % LIVE_VAL, "host survives, then a RAM trip")
row("hi keeps", pr(t, "a0"), "0x123456789abcdef", "refused sb +0x27f, sh +0x27c leave the seeded slot (ld +0x278)")
row("hi once", count(t, "-- declined.", clean), 1, "first refusal +0x27f, then 0x27c/0x27e/0x07: one notice")

# ---- THE MIDDLE OF THE WINDOW, where EVERY address bit 0-8 is set (kimi-k3:cloud, second closing pass: no refused access
#  set bit 7 or bit 8, so a decline effect keyed on `relative_addr & 0x80' -- `odata = relative_addr & 0x80' -- passed).
#  Together with the low cells (bits clear) and the far block (bit 9), every address bit is now carried both ways by a
#  refused access of each kind: the ANSWER (1R, 2R), a LANDING (1W, 2W, read back by an accepted ld), the NOTICE (its
#  text here, and one count across the session), the DEFAULT ARM not reached, and a RE-ARM by an accepted access in
#  this block (the sd between the refusals).  +0x1f8 is inside DEV_CRIME_LENGTH (0x280) and reaches the default arm.
A = Addr(CODE)
c = []
x, _ = st(A, "sd", CRIME + 0x1f8, 0x0123456789abcdef); c += x
x, _ = ld(A, "lb", CRIME + 0x1ff, "v0"); c += x
x, _ = ld(A, "lh", CRIME + 0x1fe, "a1"); c += x
x, _ = st(A, "sb", CRIME + 0x1ff, 0xff); c += x
x, _ = st(A, "sh", CRIME + 0x1fc, 0xffff); c += x
x, _ = ld(A, "ld", CRIME + 0x1f8, "a0"); c += x
x, _ = st(A, "sd", CRIME + 0x1f8, 0x0123456789abcdef); c += x
x, _ = ld(A, "lb", CRIME + 0x1ff, "t1"); c += x
#  and a follow-up refusal with bits 7 and 8 CLEAR (codex, third closing pass: a latch whose bit is keyed on address bit 7
#  or 8 was invisible -- the middle block's refusals all set them, every other session's all clear them)
x, _ = ld(A, "lb", CRIME + 0x07, "s3"); c += x
t, clean = session(c + ["print v0", "print a1", "print a0"] + roundtrip(A))
mid_dflt = (dflt(t, clean, 0x1ff, False) + dflt(t, clean, 0x1fe, False) + dflt(t, clean, 0x1ff, True) +
            dflt(t, clean, 0x1fc, True)) if clean else "unclean"
row("mid said", said(t, 1, 0x1ff, clean), 1, "lb +0x1ff (bits 0-8 set): own announce, once")
row("mid nodflt", mid_dflt, 0, "switch default arm NOT reached at 0x1ff/0x1fe/0x1fc")
row("mid lb v0", pr(t, "v0"), "0x0", "refused lb +0x1ff over a seeded slot answers 0")
row("mid lh v0", pr(t, "a1"), "0x0", "refused lh +0x1fe over a seeded slot answers 0")
row("mid keeps", pr(t, "a0"), "0x123456789abcdef", "refused sb +0x1ff, sh +0x1fc do not land (ld +0x1f8)")
row("mid once", count(t, "-- declined.", clean), 1, "5 refusals, an accepted sd between, then +0x07: one notice")
row("mid surv", pr(t, "v1"), "0x%x" % LIVE_VAL, "the session completes (a RAM trip)")

# ---- the latch, first refusal at CRIME_DOG (the one named label with no session whose FIRST refusal is there) ----
#  CRIME_DOG is SEEDED first (kimi CLI, second closing pass: with DOG at 0 a decline answering the register read 0), and
#  read refused at BOTH widths (codex: `odata = 0x100' at DOG left the lb's low byte 0 and passed).
A = Addr(CODE)
s, _ = st(A, "sd", CRIME + 0x30, 0x0123456789abcdef)
x, _ = ld(A, "lb", CRIME + 0x30, "v0")
y, _ = ld(A, "lb", CRIME + 0x07, "v1")
z, _ = ld(A, "lh", CRIME + 0x08, "a0")        # a refused read at CRIME_CONTROL (codex, closing pass: answers at labels)
w, _ = ld(A, "lh", CRIME + 0x30, "t1")
#  CONTROL's 1-byte answer cell (the Opus third-closing seat, measured: `odata = 1' keyed on len 1 at CONTROL passed --
#  the only refused read there was an lh), and TIME's answer over a SEEDED register: at the TIME rows' refused reads
#  TIME is whatever the first tick added, a multiple of 66, and it is 0 in 42 of 800 logged cells (the same seat), so
#  a decline answering the register there was invisible in those runs.  Seeded ODD by an accepted sd, TIME stays odd
#  (every update adds a multiple of 66), so its low byte and low halfword are never 0.
w2, _ = ld(A, "lb", CRIME + 0x08, "a1")
ts, _ = st(A, "sd", CRIME + 0x38, 0x11111111)
tb, _ = ld(A, "lb", CRIME + 0x38, "s0")
th, _ = ld(A, "lh", CRIME + 0x38, "s1")
t, clean = session(s + x + y + z + w + w2 + ts + tb + th + ["print v0", "print a0", "print t1", "print a1", "print s0",
                                                              "print s1"])
row("dog once", count(t, "-- declined.", clean), 1, "first refusal at CRIME_DOG, then +0x07: one notice")
row("dog said", said(t, 1, 0x30, clean), 1, "lb +0x30 (first refusal): its own announce")
row("dog v0", pr(t, "v0"), "0x0", "refused lb at CRIME_DOG (seeded 0x0123..ef) answers 0")
row("dog lh v0", pr(t, "t1"), "0x0", "refused lh at CRIME_DOG (seeded) answers 0")
row("ctl v0", pr(t, "a0"), "0x0", "refused lh at CRIME_CONTROL (holds 0x100) answers 0")
row("ctl lb v0", pr(t, "a1"), "0x0", "refused lb at CRIME_CONTROL answers 0")
row("time sd lb v0", pr(t, "s0"), "0x0", "refused lb at CRIME_TIME (seeded odd) answers 0")
row("time sd lh v0", pr(t, "s1"), "0x0", "refused lh at CRIME_TIME (seeded odd) answers 0")

# ---- FREE-RUNNING: the announce is a fatal(), so it prints when the guest is NOT single-stepped (a debug() would not) ----
A = Addr(CODE)
here = A.take(2)
c = ["at=0x%x" % (CRIME + 7), "v0=0x%x" % SENT,
     "put w 0x%x, 0x%08x" % (here, enc("lb", "at", "v0")),
     "put w 0x%x, 0x%08x" % (here + 4, OP_NOP),
     "put w 0x%x, 0x%08x" % (here + 8, OP_B_SELF),
     "put w 0x%x, 0x%08x" % (here + 12, OP_NOP),
     "pc=0x%x" % here, "<RUN>", "print v0"]
t, clean = session(c)
ran = t.split("continue", 1)[1] if "continue" in t else ""
row("free said", ran.count("unimplemented len=1 at 0x7 -- declined.  (once) ]"), 1, "free-running lb +7: announce printed")
row("free v0", pr(t, "v0"), "0x0", "free-running lb +7: declined read answers 0")

#  THE CHANNEL across its axes (codex, fourth closing pass; the Opus seat measured it: `(relative_addr & 8 ? debug :
#  fatal)(' and `(len == 2 ? debug : fatal)(' each scored 131/131 -- stepped rows cannot tell debug() from fatal(), and
#  the ONE free-running refusal above sits at +0x07, bits 3-9 clear, len 1, a read, the default arm).  Each session below
#  is ONE free-running refusal -- the latch silences any second one -- chosen to carry the other side of an axis: 2R at
#  +0x1f8 (bits 3-8 set), 1W at +0x27f (bit 9, a write), 2W at CONTROL; and one per remaining label.
def free_one(op, off, val):
    A = Addr(CODE)
    here = A.take(2)
    if op[0] == "l":
        setup, ins = ["at=0x%x" % (CRIME + off), "v0=0x%x" % SENT], enc(op, "at", "v0")
    else:
        setup, ins = ["a3=0x%x" % (CRIME + off), "t0=0x%x" % val], enc(op, "a3", "t0")
    c = setup + ["put w 0x%x, 0x%08x" % (here, ins), "put w 0x%x, 0x%08x" % (here + 4, OP_NOP),
                 "put w 0x%x, 0x%08x" % (here + 8, OP_B_SELF), "put w 0x%x, 0x%08x" % (here + 12, OP_NOP),
                 "pc=0x%x" % here, "<RUN>"]
    t, clean = session(c)
    ran = t.split("continue", 1)[1] if "continue" in t else ""
    ln = 1 if op in ("lb", "lbu", "sb") else 2
    #  `clean' honoured since repair 12 (the flagship ruling, closing pass 6: a count from an unclean transcript is not
    #  evidence -- ignoring it could only false-RED, but every other count row already said `unclean')
    if not clean:
        return "unclean"
    return ran.count("unimplemented len=%d at 0x%x -- declined.  (once) ]" % (ln, off))


for op, off, val, nm in (("lh", 0x1f8, 0, "free 2r said"), ("sb", 0x27f, 0xff, "free 1w said"),
                         ("sh", 0x08, 0, "free 2w said"), ("lb", 0x00, 0, "free rev said"),
                         ("lb", 0x10, 0, "free istat said"), ("lb", 0x18, 0, "free imask said"),
                         ("lb", 0x30, 0, "free dog said"), ("lb", 0x38, 0, "free time said")):
    row(nm, free_one(op, off, val), 1, "free-running %s +0x%x: the fatal() announce printed" % (op, off))

# ---- the latch: five refused accesses, one session, exactly one announce ----
A = Addr(CODE)
c = ["ra=0x%x" % RA]
#  PROLOGUE (the Opus closing seat): accepted accesses BEFORE the first refusal -- a notice PRE-SILENCED by an accepted
#  access (`d->warned |= CRIME_W_LEN;' in an accept arm, `pre4') shows as zero notices; and an accepted CONTROL write
#  whose unmodelled bit prints the CONTROL text, so a future second latch on THAT message reusing bit 0 (`ctl_collide')
#  shows the same way.  CLOSED OVER EVERY ARM AND EVERY BRANCH an accepted access can take and come back from (glm,
#  second closing pass: the REV arm; codex, grok, kimi, third closing pass: CONTROL's DOG_ENABLE branch -- the 0x01 write
#  here skipped it -- the REV redirect branch, and the INTSTAT case alone -- each reached only AFTER some session's
#  first refusal, where a pre-set is invisible):
#      CONTROL  sw 0x0201 (DOG set, leftover nonzero), sw 0x0001 (DOG clear, leftover nonzero), sw 0 (DOG clear,
#               leftover zero), lw (CONTROL's read side) -- the Opus third-closing seat, measured: a pre-set on the
#               read side, and (by reading) on the zero-leftover side, passed; HARD_RESET is disclosed (it stops the CPUs)
#      REV      lw from the PROM-probe window (the redirect branch) AND from ordinary code (the branch not taken)
#      INTSTAT, INTMASK   lw +0x10, lw +0x18        DOG  ld +0x30        TIME  ld +0x38
#      default  sw/lw +0x34 (4-byte, low lane), sd +0x278 (8-byte, far block)
#  *** Since the fourth closing pass the prologue IS the re-arm list, ACCEPTS (the kind x label cross): the Opus seat
#  measured a pre-set on an accepted 8-byte WRITE at +0x10, and one on CONTROL's 0x0200 cell, each 131/131. ***
for op, off, val in ACCEPTS:
    c += accept(A, op, off, val, reg="a2")
#  lh FIRST (Opus seat, F2): a latch whose bit is taken from the access -- `d->warned |= len' or `|= relative_addr' --
#  sets bit 0 only for a 1-byte access or an odd address, so the lh at +0x06 would leave it clear and the lb after it
#  would announce again.  With lb first, both shapes passed.
for op, off in (("lh", 6), ("lb", 7), ("lbu", 0x3f)):
    x, _ = ld(A, op, CRIME + off, "v0"); c += x
for op, off, val in (("sb", 0x37, 0xab), ("sh", 0x36, 0xabcd)):
    x, _ = st(A, op, CRIME + off, val); c += x
#  and refusals at CRIME_REV and CRIME_TIME AFTER the latch is set (the Opus third-closing seat, measured: a latch TEST
#  that lets one label through -- `|| relative_addr == CRIME_REV' -- passed, because REV and TIME were each refused only
#  once per session, first; every other label is refused again after the latch is set somewhere)
for off in (0x00, 0x38):
    x, _ = ld(A, "lb", CRIME + off, "v0"); c += x
t, clean = session(c + roundtrip(A))
row("latch x5", count(t, "-- declined.", clean), 1, "5 refused accesses, then +0x00, +0x38 -> one (once)")
row("latch surv", pr(t, "v1"), "0x%x" % LIVE_VAL, "host survives all five")
#  REPAIR 12 (closing pass 6; flagship ruling regress/artifacts/lcaisalane/FABLE_C4_RULING_20260915.md, part A): the two
#  rows ACCEPTS feeds COUNT notices, so an ACCEPTED cell wrongly declined -- an accept guard GROWN by one conjunct, the
#  de-escalation clause's own shape -- takes the session's one notice itself and the count stays 1: codex's C1 (CONTROL
#  4R) and the Opus seat's G1-G5 (CONTROL 8R/8W, INTSTAT 8, TIME 4, REV window 4W, INTMASK 4W) each scored 141/141
#  (regress/artifacts/crimewidthkill/opus_close6_20260915/).  All 46 ACCEPTS accesses run BEFORE the lh +0x06 here, and
#  the width arm declines before the REV pc test, so that lh must still carry its OWN announce: any grown accept guard
#  at any ACCEPTS cell steals it.  CHANNEL: the announce text of the session's first GENUINE refusal (codex's row).
row("latch said", said(t, 2, 0x6, clean), 1, "lh +0x06, after all 46 ACCEPTS cells: ITS OWN announce")

#  The same announce, FREE-RUNNING from the PROM window (glm, closing pass 6: `(pc in the window ? debug : fatal)('
#  scored 141/141 -- every free-running refusal ran from CODE).  Clause (e) by the DEPENDS-ON bound (the decline arm does
#  not read the pc); rowed as a licensed strengthening because the PROM's probe loop is the one real caller that issues
#  CRIME accesses from that window.  CHANNEL: the fatal() text, which a debug() would not print while free-running.
A = Addr(CODE)
c = ["ra=0x%x" % RA, "at=0x%x" % CRIME, "v0=0x%x" % SENT,
     "put w 0x%x, 0x%08x" % (PROBE_PC, enc("lb", "at", "v0")),
     "put w 0x%x, 0x%08x" % (PROBE_PC + 4, OP_NOP),
     "put w 0x%x, 0x%08x" % (PROBE_PC + 8, OP_B_SELF),
     "put w 0x%x, 0x%08x" % (PROBE_PC + 12, OP_NOP),
     "pc=0x%x" % PROBE_PC, "<RUN>", "print v0"]
t, clean = session(c)
ran = t.split("continue", 1)[1] if "continue" in t else ""
row("free revP said", ran.count("unimplemented len=1 at 0x0 -- declined.  (once) ]") if clean else "unclean", 1,
    "free-running lb +0x00 FROM the PROM window")

#  THE SILENT FORM (repair 12, licensed): an accepted cell bypassed with NO announce -- `if (len == 8 && relative_addr ==
#  CRIME_CONTROL) goto crime_declined;' before the width test (the Opus seat's G6, 141/141 with `latch said' green) --
#  is outside the de-escalation class (the deleted exit(1) would not have announced it either) and is DISCLOSED by class
#  in item 6; these VALUE rows carry the cells where such a bypass is GUEST-VISIBLE, derived per cell from the switch and
#  the width arm (the flagship ruling: from the enumeration, never from the mutants that happened to be built):
#    REV window 4W/8W/8R, CONTROL 8R/8W, INTSTAT 8W/8R/4W, INTMASK 4W, TIME 8W, the default arm's 4W/4R at +0x40.
#  The other ACCEPTS cells are either pinned elsewhere or EQUIVALENT when bypassed (item 6).
#  REV window: CHANNEL = the PROM-probe redirect (pc = ra), which only an ACCEPTED access reaches.
A = Addr(CODE)
c = ["ra=0x%x" % RA]
x, _ = st(A, "sw", CRIME + 0, 0, at=PROBE_PC); c += x + ["print pc"]
x, _ = st(A, "sd", CRIME + 0, 0, at=PROBE_PC); c += x + ["print pc"]
x, _ = ld(A, "ld", CRIME + 0, "s0", at=PROBE_PC); c += x + ["print pc"]
t, clean = session(c)
for i, k in enumerate(("sw", "sd", "ld")):
    v = nth(t, "pc", i)
    row("revP %s pc" % k, "absent" if v is None else "0x%x" % v, "0x%x" % RA,
        "accepted %s CRIME_REV from 0xbfc05180: pc = ra" % k)
#  CONTROL 8R: CHANNEL = its value, 0x100 (the prelude's ENDIANESS; a declined read answers 0).  INTSTAT 8R: its value
#  SOFTINT | HARDINT, recomputed by every access's tail.  INTMASK 4W: the high half lands (ld +0x18).  TIME 8W: an ODD
#  seed stays odd (every update adds a multiple of 66), and the register is even before it -- so parity says whether
#  the store landed, whatever the host clock added.  Default arm +0x40 4W (the high lane) and 4R: the value round trip.
#  CONTROL 8W: its arm prints the unimplemented-control text for a leftover bit (0x01), which a declined store cannot.
A = Addr(CODE)
c = []
x, _ = ld(A, "ld", CRIME + 0x08, "s0"); c += x
x, _ = ld(A, "lw", CRIME + 0x08, "a0"); c += x                     # #529 repair 14: CONTROL 4R, HIGH lane (0 -- pairs with +0x0c)
x, _ = ld(A, "lw", CRIME + 0x0c, "s4"); c += x                     # #529 repair 14: CONTROL 4R, LOW lane (0x100 -- the discriminating half)
x, _ = st(A, "sd", CRIME + 0x20, BIT); c += x
x, _ = ld(A, "ld", CRIME + 0x10, "s1"); c += x
x, _ = ld(A, "lw", CRIME + 0x10, "v1"); c += x                     # #529 repair 14: ACCEPTS entry 21, the 4-BYTE twin
x, _ = st(A, "sw", CRIME + 0x18, 0x10000000); c += x
x, _ = ld(A, "ld", CRIME + 0x18, "s2"); c += x
x, _ = st(A, "sd", CRIME + 0x38, 0x11111111); c += x
x, _ = ld(A, "ld", CRIME + 0x38, "s3"); c += x
x, _ = st(A, "sd", CRIME + 0x40, 0); c += x
x, _ = st(A, "sw", CRIME + 0x40, 0x0a0b0c0d); c += x
x, _ = ld(A, "lw", CRIME + 0x40, "a1"); c += x
x, _ = ld(A, "ld", CRIME + 0x40, "a2"); c += x
x, _ = st(A, "sd", CRIME + 0x08, 0x01); c += x
t, clean = session(c + ["print s0", "print s1", "print s2", "print s3", "print a1", "print a2", "print v1",
                        "print a0", "print s4"])
tv = nth(t, "s3", 0)
row("acc ctl ld", pr(t, "s0"), "0x100", "accepted ld +0x08 answers CONTROL (0x100)")
row("acc ctl4r", pr(t, "a0"), "0x0",
    "accepted lw +0x08: CONTROL's HIGH lane is 0 -- VACUOUS ALONE, paired with acc ctl0c below")
row("acc ctl0c", pr(t, "s4"), "0x100",
    "accepted lw +0x0c: the LOW lane is 0x100 -- the half that discriminates, latch CLEAR")
row("acc istat ld", pr(t, "s1"), "0x%x" % BIT, "accepted ld +0x10 answers INTSTAT = SOFTINT")
row("acc istat lw", pr(t, "v1"), "0x%x" % (BIT >> 32),
    "accepted lw +0x10 answers INTSTAT's HIGH lane -- ACCEPTS entry 21, latch CLEAR")
row("acc imask sw", pr(t, "s2"), "0x1000000000000000", "accepted sw +0x18 lands in the high half")
row("acc time sd", "absent" if tv is None else ("odd" if tv & 1 else "even"), "odd",
    "accepted sd +0x38 of an odd seed: TIME stays odd (raw %s)" % tv)
row("acc 40 lw", pr(t, "a1"), "0xa0b0c0d", "accepted lw +0x40 answers the high half the sw stored")
row("acc 40 sw", pr(t, "a2"), "0xa0b0c0d00000000", "accepted sw +0x40 lands in the high half (ld)")
row("acc ctl sd", count(t, "CRIME_CONTROL: unimplemented", clean), 1, "accepted sd 0x01 +0x08 prints the text")
#  INTSTAT 8W and 4W: CHANNEL = cause.IP2.  With INTMASK = SOFTINT = BIT and the line low (SOFTINT's store goes to the
#  default arm, which does not reassert), an ACCEPTED store at +0x10 reasserts and raises IP2; a declined one reaches the
#  tail, which recomputes INTSTAT but does NOT touch the line.  Between the two, SOFTINT = 0 and an INTMASK store lower it.
A = Addr(CODE)
c = []
x, _ = st(A, "sd", CRIME + 0x18, BIT); c += x
x, _ = st(A, "sd", CRIME + 0x20, BIT); c += x
c += ["print cause"]
x, _ = st(A, "sd", CRIME + 0x10, 0); c += x
c += ["print cause"]
x, _ = st(A, "sd", CRIME + 0x20, 0); c += x
x, _ = st(A, "sd", CRIME + 0x18, BIT); c += x
x, _ = st(A, "sd", CRIME + 0x20, BIT); c += x
c += ["print cause"]                                # immediately before the sw, as `pre' is before the sd
x, _ = st(A, "sw", CRIME + 0x10, 0); c += x
c += ["print cause"]
t, clean = session(c)
row("istw pre", ip2(nth(t, "cause", 0)), "clear", "CONTROL: IP2 low after SOFTINT's default-arm store")
row("istw sd", ip2(nth(t, "cause", 1)), "set", "accepted sd +0x10 reasserts: IP2 set")
row("istw mid", ip2(nth(t, "cause", 2)), "clear", "CONTROL: lowered again (SOFTINT 0, INTMASK store), SOFTINT set")
row("istw sw", ip2(nth(t, "cause", 3)), "set", "accepted sw +0x10 reasserts: IP2 set")

# ============================================================================================
#  REPAIR 13 -- APPLIED 2026-09-16, 157 -> 188 rows, measured 188/188 CONTROL=OK on the committed
#  build (killtable11_20260916/probe_repair13_fix.out) and verified by kill table 11.
#  *** THIS HEADER READ "DRAFT -- NOT APPLIED" IN THE SHIPPED PROBE UNTIL 2026-09-16 19:5x, WHEN
#  THE GROK SEAT READ THE FILE AND SAID SO.  It was true of the scratchpad draft and false the
#  moment the block was spliced -- a wrong record sitting in product-adjacent code, of exactly
#  the class this project grades L4.  Corrected in place. ***  Every session below is owed: they
#  are the rows that catch the K-class at the cells the close-7 seat MEASURED, in the shapes it
#  measured them in (opus_close7_20260915/scripts2/post7.py, post7c.py -- base 29/29, K1 28/29,
#  K2 27/29, K3 28/29, four negative controls 29/29).  What Fable's answer changes is how many
#  MORE cells the closure product adds, not whether these belong.
#
#  THE ONE STRUCTURAL IDEA, and it is the whole repair: every existing value row is measured
#  with `d->warned & CRIME_W_LEN' CLEAR, so a guard grown with a conjunct on that latch is
#  invisible to all of them.  `POST()' below opens each session with a REFUSED lb at +0x07, so
#  every access after it is measured with the LATCH SET.  New sessions only -- the targeting
#  rule therefore selects no earlier kill for re-running (no existing session's command list
#  changes).
#
#  CHANNEL lines: each row names its mutant and the observable, and EVERY ONE WAS CHECKED
#  AGAINST ITS MUTANT rather than merely written -- the seat's first two TIME shapes were
#  measured VACUOUS and one gave a FALSE RED on a control, which is this block's own evidence
#  for why the PRETABLE CHANNEL line has to be run, not asserted.
# ============================================================================================


def POST(A):
    """A refused lb at +0x07 sets d->warned & CRIME_W_LEN before anything else in the session."""
    x, _ = ld(A, "lb", CRIME + 0x07, "v0")
    return x


# ---- P1: the REV PROM-probe window, POST.  CHANNEL: pc = ra, which only an ACCEPTED access
#      reaches.  KILLS K2 (the REV 4-byte cell conjoined with the latch). ----
A = Addr(CODE)
c = ["ra=0x%x" % RA] + POST(A)
for op in ("sw", "sd", "ld", "lw"):
    if op[0] == "s":
        x, _ = st(A, op, CRIME + 0, 0, at=PROBE_PC)
    else:
        x, _ = ld(A, op, CRIME + 0, "s0", at=PROBE_PC)
    c += x + ["print pc"]
t, clean = session(c)
for i, k in enumerate(("sw", "sd", "ld", "lw")):
    v = nth(t, "pc", i)
    row("p revP %s pc" % k, "absent" if v is None else "0x%x" % v, "0x%x" % RA,
        "POST: accepted %s CRIME_REV from the window -> ra" % k)
row("p revP once", count(t, "-- declined.", clean), 1, "CONTROL: the session refused exactly once (the lb)")

# ---- P2: the twelve-cell value session, POST.  KILLS K1 (INTMASK 4W) and K3 (CONTROL 8R).
#      The two CONTROL writes at the end drive the clause-(e) 0x0001 and 0x0201 cells into the
#      `unimplemented' count row, so one count row covers three accesses. ----
A = Addr(CODE)
c = POST(A)
x, _ = ld(A, "ld", CRIME + 0x08, "s0"); c += x
x, _ = ld(A, "lw", CRIME + 0x08, "a0"); c += x                     # #529 repair 14: CONTROL 4R, HIGH lane (0 -- pairs with +0x0c)
x, _ = ld(A, "lw", CRIME + 0x0c, "s4"); c += x                     # #529 repair 14: CONTROL 4R, LOW lane (0x100 -- the discriminating half)
x, _ = st(A, "sd", CRIME + 0x20, BIT); c += x
x, _ = ld(A, "ld", CRIME + 0x10, "s1"); c += x
x, _ = ld(A, "lw", CRIME + 0x10, "v1"); c += x                     # #529 repair 14: ACCEPTS entry 21, the 4-BYTE twin
x, _ = st(A, "sw", CRIME + 0x18, 0x10000000); c += x
x, _ = ld(A, "ld", CRIME + 0x18, "s2"); c += x
x, _ = st(A, "sd", CRIME + 0x38, 0x11111111); c += x
x, _ = ld(A, "ld", CRIME + 0x38, "s3"); c += x
x, _ = st(A, "sd", CRIME + 0x40, 0); c += x
x, _ = st(A, "sw", CRIME + 0x40, 0x0a0b0c0d); c += x
x, _ = ld(A, "lw", CRIME + 0x40, "a1"); c += x
x, _ = ld(A, "ld", CRIME + 0x40, "a2"); c += x
x, _ = st(A, "sd", CRIME + 0x08, 0x01); c += x
x, _ = st(A, "sw", CRIME + 0x08, 0x0001); c += x          # EXTRA: CONTROL 4W 0x0001
x, _ = st(A, "sw", CRIME + 0x08, 0x0201); c += x          # EXTRA: CONTROL 4W 0x0201 (clause-(e) cell)
x, _ = st(A, "sd", CRIME + 0x08, 0x0201); c += x          # #529 repair 14: ACCEPTS entry 14, the 8-BYTE TWIN of the line above
t, clean = session(c + ["print s0", "print s1", "print s2", "print s3", "print a1", "print a2", "print v1",
                        "print a0", "print s4"])
tv = nth(t, "s3", 0)
row("p acc ctl ld", pr(t, "s0"), "0x100", "POST: accepted ld +0x08 answers CONTROL")
row("p acc ctl4r", pr(t, "a0"), "0x0",
    "POST: accepted lw +0x08: CONTROL's HIGH lane is 0 -- VACUOUS ALONE, paired with p acc ctl0c")
row("p acc ctl0c", pr(t, "s4"), "0x100",
    "POST: accepted lw +0x0c: the LOW lane is 0x100 -- the discriminating half, latch SET")
#  *** #529 REPAIR 14, Fable item D: THE CONTROL 4R CELL IS A **PAIR**, NEVER `lw +0x08' ALONE. ***
#  `lw +0x08' has (relative_addr & 4) == 0, so :293-294 answers the HIGH 32 bits of CONTROL -- and
#  CONTROL is 0x100 (the prelude at :231), whose high half is ZERO.  A DECLINED read answers 0 too, so a
#  row asserting 0 there is GREEN UNDER ITS OWN MUTANT: 0 == 0.  That is the vacuity codex found in the
#  shipped probe and the reason table 11's `C_ctl4r' leg proved nothing.
#  `lw +0x0c' has (relative_addr & 4) == 4, takes the LOW lane, and answers 0x100.  The two together say
#  "the lane decode is alive AND this lane is zero", which neither says alone.
#  MEASURED before being shipped, by opus_close8_20260916/scripts/ctl4r.py: base 9/9; `C_ctl4r' 9/9, so
#  the cell really IS equivalent; and `G_lane_ctl' 8/9 reddening `post ctl4r' -- the LIVENESS CONTROL
#  that makes those 9/9 mean EQUIVALENCE rather than "nothing looked".
row("p acc istat ld", pr(t, "s1"), "0x%x" % BIT, "POST: accepted ld +0x10 answers INTSTAT")
row("p acc istat lw", pr(t, "v1"), "0x%x" % (BIT >> 32),
    "POST: accepted lw +0x10 answers INTSTAT's HIGH lane -- ACCEPTS entry 21, latch SET")
#  *** #529 REPAIR 14, ACCEPTS ENTRY 21 -- THE CELL NO INSTRUMENT IN THIS CAMPAIGN OBSERVED.
#  `G_clr_ist4r' scores 188/188 against the shipped probe AND 5/5 against t4clear.py. ***
#  IT WAS BLIND IN **BOTH** LATCH STATES, and the reason is the WIDTH AXIS, not the latch: these two twin
#  sessions already seeded SOFTINT = BIT and read INTSTAT at EIGHT bytes, and NEITHER read it at FOUR.
#  The buckets derivation says the same thing from the other side -- CLEAR driven only by session 40, SET
#  only by sessions 19 and 26, and all three are oracle-less for this cell.
#  CHANNEL: (relative_addr & 4) == 0 at +0x10, so dev_sgi_ip32.c:293-294 answers the HIGH 32 bits.
#  *** THE SEED IS LOAD-BEARING: BIT's high word is 0x01010101, so the row reads 0x1010101 where a
#  DECLINED read answers 0.  Seeding the interrupt state in the LOW half would make the row answer 0 --
#  the same value a decline gives -- and it would be GREEN UNDER ITS OWN MUTANT.  That vacuity is what
#  this repair exists to remove, and it is one masking line away from reproducing it. ***
row("p acc imask sw", pr(t, "s2"), "0x1000000000000000", "POST: accepted sw +0x18 lands high")
row("p acc time sd", "absent" if tv is None else ("odd" if tv & 1 else "even"), "odd",
    "POST: accepted sd +0x38 odd seed stays odd (raw %s)" % tv)
row("p acc 40 lw", pr(t, "a1"), "0xa0b0c0d", "POST: accepted lw +0x40 answers the stored half")
row("p acc 40 sw", pr(t, "a2"), "0xa0b0c0d00000000", "POST: accepted sw +0x40 lands high")
row("p acc ctl msg", count(t, "CRIME_CONTROL: unimplemented", clean), 4,
    "POST: the FOUR accepted CONTROL writes (0x01 sd, 0x0001 sw, 0x0201 sw, 0x0201 sd) each print")
#  *** #529 repair 14, ACCEPTS entry 14.  THIS ROW WANTED 3 AND DROVE ONLY THE `sw' FORM OF 0x0201,
#  while entry 14 is the `sd' form: SAME ADDRESS, SAME VALUE, OTHER WIDTH, no row.  That is the #499
#  width-axis shape reproduced INSIDE the row added to close the #499 family, and it was found by the
#  Opus measuring seat's value-aware bucket derivation (repair-14 adjudication) and graded L2 -- a floor
#  breach, not debt -- by the flagship ruling FABLE_RULING_20260917.md.
#  *** THE COUNT IS THE ONLY CHANNEL THAT CAN SEPARATE THE TWO WIDTHS, and that is checked rather than
#  assumed: `sd 0x0201' masks DOG at dev_sgi_ip32.c:361-363, leaves 0x001 past the ENDIANESS mask at
#  :375, and prints at :377-379 -- TEXT-IDENTICAL to the `sw' twin, because the arm prints the MASKED
#  idata.  A text row cannot tell them apart; only the count can.  A mutant declining the 8-byte form at
#  CONTROL takes this to 3 and reds it. ***
row("p acc once", count(t, "-- declined.", clean), 1, "CONTROL: exactly one refusal (the lb)")

# ---- P3: INTSTAT's reassert channel (cause.IP2), POST.  The reassert is an EFFECT channel a
#      value row cannot see, which is why this session exists separately. ----
A = Addr(CODE)
c = POST(A)
x, _ = st(A, "sd", CRIME + 0x18, BIT); c += x
x, _ = st(A, "sd", CRIME + 0x20, BIT); c += x
c += ["print cause"]
x, _ = st(A, "sd", CRIME + 0x10, 0); c += x
c += ["print cause"]
x, _ = st(A, "sd", CRIME + 0x20, 0); c += x
x, _ = st(A, "sd", CRIME + 0x18, BIT); c += x
x, _ = st(A, "sd", CRIME + 0x20, BIT); c += x
c += ["print cause"]
x, _ = st(A, "sw", CRIME + 0x10, 0); c += x
c += ["print cause"]
t, clean = session(c)
row("p istw pre", ip2(nth(t, "cause", 0)), "clear", "CONTROL: IP2 low after SOFTINT default-arm store")
row("p istw sd", ip2(nth(t, "cause", 1)), "set", "POST: accepted sd +0x10 reasserts")
row("p istw mid", ip2(nth(t, "cause", 2)), "clear", "CONTROL: lowered again")
row("p istw sw", ip2(nth(t, "cause", 3)), "set", "POST: accepted sw +0x10 reasserts")

# ---- P4/P5: THE TIME 4-BYTE CELLS, POST, IN THE **GAPPED** SHAPE.  *** THE TWO OBVIOUS SHAPES
#      WERE MEASURED VACUOUS (post7b.py) and one gave a FALSE RED on a control; only this one
#      discriminates, at ~13,000x (base 0x13414f8 vs the bypass's 0x5ee). ***  The gap is the
#      debugger's own pause BETWEEN steps: host time passes, so an update that is performed
#      arrives before the final 8R and one that is skipped arrives after it.  CHANNEL: a read
#      takes odata BEFORE its own crime_update_crime_time(). ----
def gapped_post(kind):
    ops = [enc("lb", "a3", "t1"),                                            # REFUSED lb -- sets the latch
           enc("ld", "at", "v1"),                                            # TIME 8R, TIME still ~0
           enc("sw", "at", "t0") if kind == "w" else enc("lw", "at", "a0"),  # the cell under test
           enc("ld", "at", "v0")]                                            # what it left behind
    c = ["at=0x%x" % (CRIME + 0x38), "a3=0x%x" % (CRIME + 0x07), "t0=0x0a0b0c0d",
         "v0=0x%x" % SENT, "v1=0x%x" % SENT, "a0=0x%x" % SENT, "t1=0x%x" % SENT]
    for i, op in enumerate(ops):
        c.append("put w 0x%x, 0x%08x" % (CODE + 4 * i, op))
    c += ["put w 0x%x, 0x%08x" % (CODE + 4 * len(ops), OP_B_SELF),
          "put w 0x%x, 0x%08x" % (CODE + 4 * len(ops) + 4, OP_NOP), "pc=0x%x" % CODE]
    c += ["step 2", "step 1", "step 1", "print v0", "print v1"]
    t, clean = session(c)
    return nth(t, "v0", 0), nth(t, "v1", 0), (t.count("-- declined.") if clean else "unclean")


_gapnote = []
for kind in ("w", "r"):
    v0, v1, n = gapped_post(kind)
    _gapnote.append(n)
    row("p t4%s gap" % kind, mag(v0), "large",
        "step2[lb,ld] step1[%s] step1[ld] (raw %s, first ld %s)"
        % ("sw" if kind == "w" else "lw", None if v0 is None else hex(v0), None if v1 is None else hex(v1)))
row("p t gap once", _gapnote, [1, 1], "CONTROL: each gapped session announced its one refusal")

# ---- #529 REPAIR 14: THE SAME TWO TIME CELLS WITH THE LATCH **CLEAR** -- ACCEPTS entries 32 and 33. ----
#  *** WHY THIS EXISTS: every row repair 13 added opens with POST(), a REFUSED lb that sets the latch before
#  anything else in the session.  So the whole latch-CLEAR half of the product was driven by session 40
#  (`latch x5') ALONE, whose only three rows are two announce COUNTS and a RAM round trip -- all blind to a
#  silent decline.  BUCKETS8_rerun.out names the eight entries in that state; 32 and 33 are two of them, and
#  `G_glm_tim4clear' (the latch-CLEAR bypass at TIME) scored 188/188 against the shipped probe. ***
#  THE SHAPE IS NOT NEW AND THAT IS DELIBERATE: it is gapped_post() MINUS the opening refusal, built and
#  MEASURED by the closing-pass-8 seat as artifacts/crimewidthkill/opus_close8_20260916/scripts/t4clear.py --
#  3/5 against G_glm_tim4clear (both gap rows red) and 5/5 against three OFF-CELL mutants, so it
#  discriminates rather than sweeping.  Transplanted rather than re-derived.
#  CHANNEL: identical to the POST twin -- the gap is the debugger's own pause BETWEEN steps, so an update
#  that is performed lands before the final 8-byte read and one that is skipped arrives after it.
#  *** AND THE CONTROL ROW IS THE OPPOSITE OF ITS TWIN'S: `c t gap once' wants [0, 0], because a session
#  that announces ANYTHING has set the latch and is no longer testing the CLEAR state at all. ***
def gapped_clear(kind):
    ops = [enc("ld", "at", "v1"),                                            # TIME 8R, TIME still ~0
           enc("sw", "at", "t0") if kind == "w" else enc("lw", "at", "a0"),  # the cell under test
           enc("ld", "at", "v0")]                                            # what it left behind
    c = ["at=0x%x" % (CRIME + 0x38), "t0=0x0a0b0c0d",
         "v0=0x%x" % SENT, "v1=0x%x" % SENT, "a0=0x%x" % SENT]
    for i, op in enumerate(ops):
        c.append("put w 0x%x, 0x%08x" % (CODE + 4 * i, op))
    c += ["put w 0x%x, 0x%08x" % (CODE + 4 * len(ops), OP_B_SELF),
          "put w 0x%x, 0x%08x" % (CODE + 4 * len(ops) + 4, OP_NOP), "pc=0x%x" % CODE]
    c += ["step 1", "step 1", "step 1", "print v0", "print v1", "print a0"]
    t, clean = session(c)
    return nth(t, "v0", 0), nth(t, "v1", 0), nth(t, "a0", 0), (t.count("-- declined.") if clean else "unclean")


_clearnote = []
for kind in ("w", "r"):
    v0, v1, a0, n = gapped_clear(kind)
    _clearnote.append(n)
    row("c t4%s gap" % kind, mag(v0), "large",
        "step1[ld] step1[%s] step1[ld] LATCH CLEAR (raw %s, first ld %s, cell %s)"
        % ("sw" if kind == "w" else "lw", None if v0 is None else hex(v0),
           None if v1 is None else hex(v1), None if a0 is None else hex(a0)))
row("c t gap once", _clearnote, [0, 0],
    "CONTROL: NEITHER session announced -- the latch stayed CLEAR, so these two rows really test that state")

# ---- #529 REPAIR 14, Fable item B: THE HARD_RESET GENERATING-SET CELLS. ----
#  *** THE 2026-09-04 CLAUSE: at each floor cell, every idata bit the guarded body TESTS is written both
#  CLEAR and SET.  The CONTROL arm tests DOG 0x200 and HARD_RESET 0x800 -- and EVERY accepted CONTROL write
#  in this probe carried 0x800 CLEAR (0x01, 0x0001, 0x0201), so the (HARD_RESET set x post-latch) cell was
#  driven by nothing.  K_ctl4w_reset_post and K_ctl8w_reset_post both score 188/188. ***
#  *** FOUND BY WRITING THE PRE-TABLE CHECK FOR REPAIR 14'S OWN TABLE, not by measuring: listing the
#  predicted red rows showed nothing written so far moves under either K mutant.  That is what the
#  pre-table block is for -- a detector arriving with visible holes wastes the one ask-again. ***
#  CHANNEL: THE HALT ITSELF.  An accepted 0x800 at CONTROL runs :364-373 and clears `running' on every CPU,
#  so the write MUST BE THE SESSION'S LAST ACCESS -- Fable named that cost in advance -- and the oracle is a
#  RAM round trip placed AFTER it.
#  *** AND THE TWO OUTCOMES ARE NOT THE SAME, WHICH IS THE WHOLE POINT OF THIS ROUND: roundtrip()'s own
#  docstring distinguishes them -- ABSENT if the HOST DIED, the SENTINEL if the CPU WAS STOPPED.  These rows
#  want the SENTINEL.  A row wanting `absent' would assert that the host died, which is the defect #529
#  REMOVED, and it would go green exactly when the fix was reverted. ***
#  MEASURED BEFORE TRANSPLANTING (opus_close8_20260916/scripts/ctlreset.py): base 6/6; K_ctl4w_reset_post
#  5/6 on its 4-byte row; K_ctl8w_reset_post 5/6 on its 8-byte row; G_glm_tim4clear 6/6 OFF-CELL.
def rst_session(op):
    """a refused lb sets the latch; then an accepted `op' of 0x800 at CONTROL stops every CPU (or does not)"""
    A = Addr(CODE)
    c, _ = ld(A, "lb", CRIME + 0x07, "v0")
    if op is not None:
        x, _ = st(A, op, CRIME + 0x08, 0x800)
        c += x
    c += roundtrip(A)
    t, clean = session(c)
    return pr(t, "v1"), (t.count("-- declined.") if clean else "unclean")


_rv, _rn = rst_session(None)
row("rst alive", _rv, "0x%x" % LIVE_VAL,
    "CONTROL: with NO 0x800 write the RAM round trip completes -- the halt oracle is live, not stuck")
row("rst alive once", _rn, 1, "CONTROL: the control session refused exactly once")
for _op, _w in (("sw", 4), ("sd", 8)):
    _rv, _rn = rst_session(_op)
    row("rst %dw" % _w, _rv, "0x%x" % SENT,
        "*** accepted %s 0x800 at CONTROL with the latch SET stops every CPU: the round trip after it does "
        "not run, so v1 keeps the SENTINEL (absent would mean the HOST died -- a different outcome) ***"
        % _op)
    row("rst %dw once" % _w, _rn, 1, "CONTROL: exactly one refusal announced in this session")

# ---- P6: the remaining post-latch ACCEPT cells that carry a value, plus the two EXTRA accesses
#      (DOG 4W high, the +0x04 write line). ----
A = Addr(CODE)
c = POST(A)
x, _ = ld(A, "ld", CRIME + 0x00, "s0"); c += x                      # REV 8R from CODE
x, _ = ld(A, "lw", CRIME + 0x04, "s1"); c += x                      # REV 4R low lane (devsig cell)
x, _ = st(A, "sw", CRIME + 0x04, 0x0c0ffee0); c += x                # EXTRA: the +0x04 WRITE line
x, _ = st(A, "sd", CRIME + 0x30, 0x1122334455667788); c += x        # DOG 8W
x, _ = ld(A, "ld", CRIME + 0x30, "s2"); c += x                      # DOG 8R
x, _ = ld(A, "lw", CRIME + 0x30, "a0"); c += x                      # DOG 4R high
x, _ = ld(A, "lw", CRIME + 0x34, "a1"); c += x                      # DOG 4R low
x, _ = st(A, "sw", CRIME + 0x34, 0x0badcafe); c += x                # DOG 4W low
x, _ = ld(A, "ld", CRIME + 0x30, "s3"); c += x
x, _ = st(A, "sw", CRIME + 0x30, 0x0feedbac); c += x                # EXTRA: DOG 4W HIGH
x, _ = ld(A, "ld", CRIME + 0x30, "ra"); c += x
x, _ = st(A, "sd", CRIME + 0x18, BIT); c += x                       # INTMASK 8W
x, _ = ld(A, "ld", CRIME + 0x18, "a2"); c += x                      # INTMASK 8R
x, _ = st(A, "sd", CRIME + 0x278, 0x0102030405060708); c += x       # far block 8W
x, _ = ld(A, "ld", CRIME + 0x278, "t1"); c += x
t, clean = session(c + ["print s0", "print s1", "print s2", "print a0", "print a1", "print s3",
                        "print ra", "print a2", "print t1"] + roundtrip(A))
row("p rev ld", pr(t, "s0"), "0x11", "POST: accepted ld +0x00 answers CRIME_REV")
row("p rev lw4", pr(t, "s1"), "0x11", "POST: accepted lw +0x04 answers REV low lane")
row("p dog st+ld", pr(t, "s2"), "0x1122334455667788", "POST: 8W then 8R at CRIME_DOG")
row("p dog rhi", pr(t, "a0"), "0x11223344", "POST: 4R of the high half (+0x30)")
row("p dog rlo", pr(t, "a1"), "0x55667788", "POST: 4R of the low half (+0x34)")
row("p dog wlo", pr(t, "s3"), "0x112233440badcafe", "POST: 4W low half lands, high half kept")
row("p dog whi", pr(t, "ra"), "0xfeedbac0badcafe", "POST: 4W HIGH half lands, low half kept")
row("p imask st+ld", pr(t, "a2"), "0x%x" % BIT, "POST: 8W then 8R at CRIME_INTMASK")
row("p top st+ld", pr(t, "t1"), "0x102030405060708", "POST: 8W then 8R at +0x278")
row("p resid once", count(t, "-- declined.", clean), 1, "CONTROL: exactly one refusal (the lb)")
row("p resid surv", pr(t, "v1"), "0x%x" % LIVE_VAL, "CONTROL: the host survives (a RAM trip)")

#  *** REGISTER COLLISION, CAUGHT WHILE DRAFTING AND RECORDED RATHER THAN SILENTLY FIXED: the
#  prototype's residual-survival row reads `v1', which roundtrip() writes.  The DOG 4W-high
#  readback added here therefore CANNOT use v1 -- it would make one of the two rows read the
#  other's register and go green for the wrong reason, which is exactly the vacuity this repair
#  exists to close.  It is parked in `ra' above.  *** THIS NOTE SAID `t2' UNTIL 2026-09-16 20:0x, AND THE CODE SAID
#  `ra' -- I repointed the CODE when the first run died on `KeyError: t2' (t2 is not in this probe's fifteen-name
#  register map) and left the PROSE describing the register I had abandoned.  The glm seat read the two against each
#  other and caught it.  Worse than untidy: the note's own liveness checklist (a3/t0, at, t1) does not cover `ra', so
#  the audit AS WRITTEN could not discharge the collision it exists to catch. ***  `ra' IS free in this session --
#  P1 sets it, P6 does not, and the deriver that found it is recorded: the only R-map names absent from the P6 block
#  are `ra' and `v0', and `v0' is a FALSE POSITIVE because POST() writes it through a CALL the block's text never
#  shows.  The row does vary (base green; C_dog4w reds it), so the ROW is sound and it was the RECORD that was wrong.


npass = sum(1 for _, ok in rows if ok)
st_ = dict(rows)
control = all(st_.get(n, False) for n in ("live", "devsig", "devsig hi", "dflt ctl", "rev pc ctl", "sw08 halts",
                                          "gate hardint", "gate line",
                                          "sw08 msg ctl", "imask pre", "imask ctl", "istat pre", "istat ctl",
                                          "time lb ctl", "time sb ctl", "time lh ctl", "time sh ctl"))
print("")
print("FAILING: " + ", ".join(n for n, ok in rows if not ok))
print("CRIMEP_RESULT=%d/%d" % (npass, len(rows)))
print("CRIMEP_CONTROL=%s" % ("OK" if control else "FAIL"))
print("CRIMEP_DONE")
