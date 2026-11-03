OPUS_SEAT_ALIVE_20261102_578P2

First line of the brief, verbatim:
`# PANEL PASS 2 -- `jazzvecdeassert` (#578): the real diff (a DELETION, not pass 1's conditional), the 22-row self-contained detector, its gate section, and TWO measured kill tables`

VERDICT: SHIP WITH CHANGES (5)

This seat argued for the deletion in pass 1, so I have pushed hardest on that ruling. The deletion is right, and I still hold it.
The changes are in the detector and the records, not in the product hunk. One of them (C1) is a contract sentence that is false
as written, and it is fixed with one row.

## What I checked, not judged (all read-only: HEAD 37b04798 via `git show`, est/ read in place, the artifacts read in place)

* **Scores in section 3 match the raws.** I counted `ok`/`FAIL` in every `.raw` and `.out`. Table 2: base_head 15, fixedb 22,
  M_c_absent 0, M_b 15, M_offs0 18 (after, vecw, com1, onevec), M_offsne0 18 (lbie, lbiew, dflt, com1), M_rd 17 (after, lbie, dflt,
  com1, onevec), M_wr 20 (vecw, lbiew), M_offs2 20 (lbie, lbiew), M_cond 22, M_uart 22. Table 1: base 11, fixed 13, absent 0,
  M_b/M_lowbits/M_ip6/M_timer/M_inv 11, M_del 13, M_nomask 13. probe2_head 15, probe2_fixed 22, probe2_fixedb 22. witness_head
  11/13 (after, com1), witness_fixed 13, witness_fixedb 13. **Every number in the brief is correct.**
* **Order proofs (mtime, full-iso).** PRETABLE.out 20:26:00.57 < base_head.raw 20:26:53.97. PRETABLE2.out 20:40:35.60 <
  base_head.raw (t2) 20:41:03.45. The corrections were written afterwards: PRETABLE_CORRECTION 20:33:35, PRETABLE2_CORRECTION
  20:44:17. witness_head.out 20:16:03 comes before apply_fix578.py 20:16:39 and product.diff 20:17:01. So test-first holds.
  Honest caveat, which PRETABLE2 itself states: the 22-row base/fixed scores (probe2_*, 20:39:39-44) were measured BEFORE
  PRETABLE2 was written. They are recorded as "measured already", not as predictions, so this is fine.
* **Instrument identity.** `_scratchpad/w578/jazz_vector_probe.py` is byte-identical (`cmp`) to `witness_20261102/jazz_vector_probe.py`
  and to `killtable2_20261102/jazz_vector_probe.ASRUN.py`. Each raw names md5 a1fbbc576ce0, so the shipped probe is the
  measured one.
* **Mutators build the texts named.** KILLTABLE2.log carries the `diff` for every mutant. Each one is exactly the two named lines,
  inserted after the #578 comment's last line (the presence pin, count 1) and before the `memory_writemax64` tail.
  `apply_fix578b.py` checks that OLD occurs once, and the resulting product_b.diff is the brief's hunk (+8 -2).
* **est twin.** The `DEVICE_ACCESS(jazz_jazzio)` bodies of HEAD SEC and est are identical (`diff` of the extracted functions is
  empty). est's tail is at :661-662 as the brief says, so the applier lands there.
* **The writer census, re-run.** At SEC HEAD, `mips_irq_3` appears at :83 (decl), :144 (assert), :154 (deassert), :467/:469 (mask
  arm), :697 (the tail) and :754 (connect), and nowhere else. `"%s.3"` is connected only by dev_jazz.c. `DEVICE_TICK(jazz)` never
  touches `mips_irq_3`. The MIPS `mtc0 Cause` arm (`cpu_mips_coproc.c:949-954`) writes only IP0/IP1, so a guest cannot write IP3
  directly. **Invariant I is genuinely closed over guest-reachable writers.** By induction, the deletion's line is EQUAL to
  `P && E` (not merely implied by it): the assert handler raises when the predicate holds, the deassert handler lowers when it
  fails, and the mask arm moves on predicate transitions of a line that already matched.
* **F5's healing mechanism.** `PICA_TIMER_IRQ` is 15, outside `0x7fff`, so the timer's own bit does not satisfy the IP3 test. The
  timer still heals because `jazz_interrupt_assert()` tests the WHOLE pending set (`int_asserted & 0x7fff`), not the new line.
  The timer assert therefore re-raises IRQ3 whenever any line 0-14 is pending. F5 holds, though for a less obvious reason than
  "the timer assert goes through jazz_interrupt_assert".

## Q1 -- the diff

**The deletion is right and complete.** No other site in `jazz_jazzio` or the file needs to change. Under I, nothing else
creates (IRQ3 low while P && E) once the tail is gone. HEAD's tail was the only writer that could produce that state, and the
mask arm's transition logic was correct all along given a line that matched the predicate.

**The comment over-narrows in two places and over-claims in one. Change C3:**
1. *"a vector read taken with a second JAZZ line still pending dropped a level interrupt"*. The table shows the drop on EVERY
   access to this register: a store to offset 0 (`jz ip vecw`), offset 2 read and write (`lbie`, `lbiew`), and the default arm
   (`dflt`). It also happens with ONE line pending (`jz ip onevec`). The second-line case is where the drop is HARMFUL, because
   servicing line 8 leaves line 9 pending and the deassert handler does nothing. It is not the condition for the drop.
2. *"until some line was asserted anew"*. **Widen it.** An EXT_IMASK TRANSITION of the IP3 term also healed it (`jz ip maskon`
   pins that arm), and F11 is right that a same-value rewrite does not. The timer tick and the UART tick are both "a line
   asserted anew", so they are covered by the existing words. The mask transition is not.
3. *"which recompute it from the pending lines and the enable mask on every change"*. The EXT_IMASK arm does not recompute. It
   acts on TRANSITIONS of the predicate (old_assert_3 vs new_assert_3), so a wrong line survives a same-value write. The truthful
   word is "keep it equal to". *"a read has no side effect"* is true for this register's reads, but an offset-2 write does store
   `jazz_timer_value`. The sentence should say that an access no longer touches the CPU line. *"as in the tree's other interrupt
   controllers"* is a universal claim about the tree, and its warrant is other seats' greps. Cite it or drop it.

Suggested text, still terse:

    /*  #578: no deassert here.  This tail used to deassert the CPU's IRQ3
        on every access ("needed by Windows NT during startup"), dropping
        a level interrupt while JAZZ lines were still pending until a line
        was asserted anew or EXT_IMASK re-enabled IP3 (OB-22).  The CPU line
        is kept equal to "a line 0-14 pending and EXT_IMASK.IP3 set" by
        jazz_interrupt_assert()/_deassert() and the EXT_IMASK arm; an
        access to this register no longer touches it.  */

Note that "every access" also makes the comment agree with the label rows that pin it.

## Q2 -- the ruling

**I still hold the deletion, and here is the hardest argument against it.** The conditional `if (!(P && E)) DEASSERT` can only
correct one polarity of desync: a line HIGH while nothing enabled is pending. That polarity is benign: `pica_iointr` reads vector
0 and returns. The defect this round closes is the OTHER polarity, a line LOW while P && E, and the conditional can never heal
that. So even the five seats' robustness case covers the harmless direction only. The one form with a robustness argument in both
directions is F14's recompute (`if (P && E) ASSERT else DEASSERT`). It too guards a state that I proves unreachable, so it is the
addition licence's "cannot hurt" with a better story. I find no argument for the conditional that does not reduce to guarding an
unreachable state.

**Two of the ruling's five warrants are weaker than written, and the record should say so:**
* **(ii) "equivalence is MEASURED"** is entailed by I and adds nothing independent. The rows cannot reach an I-violating state, so
  M_cond 22/22 and M_del 13/13 MUST come out equal on any correct reading. They corroborate I; they are not a second leg under it.
* **(iii) the est-compile fact** is a convenience warrant. est could take a conditional in ITS OWN predicate
  (`if (!(d->int_asserted & d->int_enable_mask & 0x7fff))`). What the deletion buys is byte-identity of a function that is
  identical today. That is real but not decisive. **(i) and (v) carry the ruling.**

**The record should also state the NT risk honestly, and it falls on both forms equally.** If NT's startup relied on the blanket
deassert as a crude stand-in for LB_IE masking (F4), with lines pending, LB_IE written to mask them, and the model ignoring
LB_IE, then removing it can leave IRQ3 asserted under an enabled IP3, which is a storm. The conditional NEVER fires either, so it
carries exactly the same risk. The only form that keeps that case is modelling LB_IE as a mask (`jazzlbmask`). So D1 does not turn
on NT, and the round should name `jazzlbmask` as the place that risk is carried.

## Q3 -- the floor

**The (d) enumeration over the function's own tests is NOT complete. Change C1, and the contract sentence is false as written.**
The body distinguishes `relative_addr` (switch: 0 / 2 / default) and `writeflag` (inside every arm, including the default arm's
read-vs-write `fatal()` texts). The cross-product is SIX cells. Five are rowed: (0,R) vec/after/onevec/com1, (0,W) vecw,
(2,R) lbie, (2,W) lbiew, (default,R) dflt. **(default, WRITE) has no row.** Yet the probe header and the brief both say *"every access
label of the enclosing function -- offsets 0 and 2 and the default arm, read and write -- is rowed with lines pending."* That is an
L4 wrong record. Under the 09-04 joint-cell reading it is also a floor cell, because the cell is guest-reachable (`sb` to
VEC+1/VEC+3) and the body tests both of its partitions. Smallest escape: `if (relative_addr != 0 && relative_addr != 2 &&
writeflag == MEM_WRITE) INTERRUPT_DEASSERT(...)`. I PREDICT it scores 22/22, because no row writes the default arm. That is a
prediction, not a measurement.

**Repair (one row, no new stub):** right after `jz ip dflt`:

    reheal(); st8(VEC + 1, 0)
    row("jz ip dfltw", ip3(), IP3)        # 11 chars; the default arm's write (one more unlatched fatal() line)

then add the name to the gate loop and change the EQUALITY pin to 23. Re-run table 2 plus that mutant. Expect `jz ip com1` to keep
inheriting the drop from whichever default-arm mutant precedes it, as PRETABLE2_CORRECTION already explains.

**Smallest re-introductions that keep the CURRENT 22 green and change a guest-visible IRQ3** (one line each, all predicted, none
measured):
* `if (idata != 0) DEASSERT`. Every row write stores 0 (`st32(VEC,0)`, `st8(VEC+2,0)`) and reads have `idata == 0`. OpenBSD's LB_IE
  writes in `pica_intr_establish` are nonzero and land with lines possibly pending (F13), so this is guest-visible.
* `if (d->jazz_timer_value != 0) DEASSERT`. The rows hold LB_IE at 0 for the whole run. After OpenBSD's first LB_IE write it is
  nonzero forever, so a booted guest would see exactly HEAD's defect again.
* `if (len == 2) DEASSERT`. No row uses a halfword. PICA_SYS_LB_IE is a 16-bit register, and I believe (not verified here) that the
  BSD drivers access it 16-bit.

None of these predicates is TESTED by the body (`idata` is stored, `len` is used only by readmax/writemax, `jazz_timer_value` is
not read in this function). So they are clause-(e) debt, not floor, and the contract's "a state the rows hold constant" covers
them only vaguely. **Change C2: either NAME all three in the contract, or (better, and nearly free) close the first two with a
one-constant change:** make `jz ip lbiew` store a NONZERO byte (e.g. `0x0f`). The reason the header gives for storing 0 (*"so the
Linux? tick arm stays unarmed"*) does not hold: that arm asserts only `if (d->pending_timer_interrupts > 0)`, and that count is
produced by a host-timer callback that the debugger stops during interaction, so the arm is inert under `step`. It only decrements
`jazz_timer_current`. With lbiew nonzero, `idata != 0` reds lbiew and `idata == 0` reds vecw and every read. `jazz_timer_value
!= 0` reds dflt/onevec/... and `== 0` reds vec/after/vecw/lbie. Both polarities of both families die with no new row. Making
lbiew an `sh` (stub `0xa4220000`) as well would put len 1/2/4 all in the rowed set (lbie/dflt = 1, lbiew = 2, vec = 4) at the cost
of one stub. If that is not wanted, disclose `len` by name. Any of these changes owes a re-run of table 2 (about 50 s) and a
check that M_uart and M_cond stay 22.

M_uart is correctly disclosed, and so is the mask-state family (`if (int_enable_mask != 0x2)`: the only jazzio access while the
mask is off is `jz vec masked`, with IP3 already 0).

## Q4 -- the vehicle

* **Padded column: clean.** `%-14s ` plus a 13-character name gives exactly two spaces. `^jz vec  .*ok$` cannot match `jz vec
  again/com1/masked/none`, and `^jz ip one  ` cannot match `jz ip onevec`. All 22 loop names equal the probe's names. The
  EQUALITY pin plus the `n/n` check fail loudly on any short run.
* **Parse.** The debugger prints bare `0x800` with no `cause =`. The regex therefore falls through to the fallback, which works
  only because the pty ECHOES `print cause` and the tail after the name holds the value (transcripts lines 99-138 confirm this).
  That is fragile but measured.
* **One false-pass direction (part of C4).** `exec_stub` ignores the return values of `set_reg`/`step`. If any of them times out
  (20 s), the guest store may not happen, and every IP3-wants-0x800 row after a skipped access PASSES, because a skipped access
  is what a fixed build looks like. A late reply then also shifts the next command's `wait()` by one prompt, and the loose
  fallback (`first 0x... after the name`) can pick up a stale value. On the gate the 22/22 equality makes an all-green
  desynchronised run very unlikely. In a kill table, though, a skipped store on a mutant's single red row is exactly a mutant
  scored as an escape. Cheap fix: keep a module-level `driver_ok` flag that any `send()` returning None clears, print
  `JAZZVEC_DRIVER=bad` at the end, and have the gate check it, or count a failed driver as an extra failing row.
* **Gate hygiene (also C4).** The gate does not set `JAZZVEC_LOG`, so each gate run leaves `/tmp/jazzvec_<pid>.log` behind and the
  transcript is not kept with the run. Set `JAZZVEC_LOG="$LOGDIR/gate_jazz_vector.pty"`. Also add the `JAZZVEC_DONE` sentinel to
  the "completed" check (a preserved log is verified by its sentinel). Nothing else is load-sensitive: no free-running, about 150
  commands, and table-2 legs took ~4-5 s each, well inside a 20 s per-command budget. `$HERE` and `$ARC_RIG` exist at HEAD
  (gate_mips.sh :21/:26). `$ARC_RIG/bsd` is not in the `need_file` list, but its absence gives 0/22, which is loud.
* No stale-translation hazard: the stubs are `put w` once before any execution, and `pc` is reset before every `step`.

## Q5 -- the records (change C5)

* **est's invariant is NOT invariant I.** est keeps the pre-#69 predicate `int_asserted & int_enable_mask & 0x7fff` (per-line enable
  bits) at :120/:130 and :424-440. F1's disposition ("the writer census ... in est: exactly those sites") and PRETABLE2's line
  numbers are SEC's. The deletion is equivalent in est by the same induction, over est's own predicate. Say so, and say that est's
  copy is UNMEASURED. The probe could not measure it as written anyway: with EXT_IMASK = 0x2, est's predicate masks lines 8/9 out,
  and `jz ip one` would read 0.
* **"M_b: the unconditional deassert reinstated verbatim"** (PRETABLE2, and floor (b)). The statement is verbatim but the comment
  is not: the mutator keeps the #578 comment and adds the bare line after it. That is behaviourally the reinstatement and
  sufficient for (b), but write "the removed statement reinstated" rather than "verbatim".
* **M_b's md5 differing from HEAD's (both tables).** A likelier cause than the line shift: the mutant is built in a DIFFERENT
  directory (`/tmp/gxmut578`, `/tmp/gxmut578b` vs `/tmp/gxdivw`), and debug info records the compilation directory. That can be
  checked by `strings`. Keep "cause not established" until someone runs that check.
* **F13 / section 5: "the fix is expected invisible to that guest".** Fine as an expectation. Do not write anything stronger until
  gate 4's boot with the fix has run.
* **Raw-header cosmetics.** `M_c_absent.raw` says "binary newer than dev_jazz.c: yes" for `/bin/true`, a `-nt` against a
  nonexistent file. It is harmless for a null medium, but a reader may take it as a freshness proof.
* **Section 0 dispositions.** F1 is right in substance, but its "in est" clause is wrong as above. F5 is right, though the healing
  works through the whole-set predicate (see above), not because the timer line is in 0x7fff. **The contract sentence in section
  2 and the probe header is the false one (C1).** I find no other of the 22 dispositions wrong. F17 (Linux? arm armed by any
  nonzero LB_IE write) is true, but it bears on C2 in the direction opposite to the header's caution: the arm is inert without
  host timers.

## Found while checking

* The jazzio `default:` arm's `fatal()` is UNLATCHED and guest-drivable: every byte access to VEC+1/VEC+3 prints a line, and the
  probe itself emits one (`transcript_fixedb.log:277`). That is out of scope here. File it under the flood class (house idiom
  `(once)` latch) if it is not already filed.
* `jazz_20` / `jazz_a0` default arms have the same unlatched shape.

## The five changes

C1. Add the (default, write) row `jz ip dfltw`; pin 23; correct the contract sentence; re-run table 2 with the default-write
    mutant. (L4 wrong record; a floor cell under the joint-cell reading.)
C2. Make `jz ip lbiew` store a nonzero byte (and optionally use `sh`), or name `idata`, `jazz_timer_value` and `len` in the contract
    as disclosed escapes. Correct the header's "Linux? tick arm" reason.
C3. Comment: "every access", "with lines pending", add the EXT_IMASK transition, "kept equal to", and cite or drop the
    other-controllers clause.
C4. Driver failure flag (a timed-out store must not be able to pass an IP3-high row). Gate sets `JAZZVEC_LOG` into `$LOGDIR` and
    checks `JAZZVEC_DONE`.
C5. Records: est's invariant and its unmeasured status; "reinstated" not "verbatim"; the md5 cause hypothesis; nothing beyond
    "expected" for OpenBSD until gate 4 runs.

VERDICT: SHIP WITH CHANGES (5)

## ADDENDUM (written later the same evening, while reviewing #577) -- my M_b md5 hypothesis above is REFUTED

In Q5 I wrote that M_b's md5 differs from HEAD's because the mutant was built in a different directory, and that debug info records the compilation directory. #577's table refutes that. Its M_b was built in `/tmp/gxmut577`, keeps a twelve-line added comment, and still has HEAD's md5 (b76a7799a3ea). The likelier cause here is `dev_jazz.c:712` `CHECK_ALLOCATION`, which expands `FAILURE()` (`misc.h:181-184`) and formats `__LINE__`. The #578 comment shifts that line, so a string constant in the binary changes. cpu_sh.c has no such use after its edited block. This is still a reading, not a measured cause; `strings` on the two binaries for `line 71` would settle it.

VERDICT: SHIP WITH CHANGES (5)
