# ADJUDICATION -- two closing passes, one ruling.  The Fable 5.1 seat, firing LAST.

```
MODEL: claude-fable-5-1
FABLE_ADJ_20260914_C
# CHECKPOINT -- 2026-09-14 ~05:0x   HEAD 9c91999 (records)   #529 TABLE 8 PROBES RUNNING; #530 CLOSING PASS 2 FIRED
```

**PART A (#529 crimewidthkill) VERDICT: `REPAIR 11` -- add `("ldP",0x00,0)` to `ACCEPTS` (A1 is a FLOOR breach), close
the whole window x kind cross in one diff, rewrite item 9 and the "both directions" wording; then a TARGETED kill table
and CLOSING PASS 6.  Pass 5 does NOT close: it found one floor breach surviving adjudication.**  Evidence basis: 8 of 9
mandated seats (codex, grok, kimi CLI, glm, deepseek, kimi-k3:cloud, minimax [first fire timed out, re-fire 6027 b
answered], Opus measuring), agy deliberately not fired, plus this seat.

**PART B (#530 lcaisalane) VERDICT: `REPAIR 4` -- option (c): row the observable cells of the fallthrough class
(the 0x3fa STW/STQ pair + a lane-0 0x60 session + the RD2 read-IIR phase), SCOPE the contract to what is caught and
DISCLOSE the un-rowable rest by name; then its kill table and CLOSING PASS 4.  Pass 3 does NOT close: the contract names
x_wfallthru unscoped and a clean-sweep escape (W4, 93/93) makes that a wrong record that must be fixed in-round.**
Evidence basis: 8 of 9 mandated seats (codex, grok, kimi CLI, glm, deepseek, minimax, kimi-k3:cloud, Opus measuring),
agy deliberately not fired, plus this seat.

The load-bearing instruction from the brief -- *which of my proposed dispositions is wrong?* -- is answered directly in
each part.  Three coordinator dispositions are overturned: Part A's "close now with repair 11 as a clause-(e)
strengthening" and "DISCLOSE A1 and do not add", and Part B's option (a) "scope and close now".

---

## PART A -- #529 crimewidthkill, closing pass 5, repair 10, 141 rows

### R1(a) -- A1 is FLOOR; A2 is clause (e).  The two questions have different answers and must not be collapsed.

**A1 (window x 8R = `ldP`) is FLOOR, and the decisive fact is empirical, not a matter of reading.**  Repair 10 itself put
`lwP` (4R), `swP` (4W) and `sdP` (8W) into `ACCEPTS` (probe lines 712-713).  It thereby DECIDED that the REV PROM-probe
window is a floor axis to cross with the accepted-kind partition.  You cannot coherently grade three cells of one cross
as floor (rowed) and the symmetric fourth as clause-(e) debt.  The kind partition {8W,8R,4W,4R} is genuinely body-tested
-- the width arm at `dev_sgi_ip32.c:275-320` branches on `len == 8`, `len == 4` and, inside each, `writeflag == MEM_WRITE`
-- and the window `if (((uint32_t)cpu->pc & 0xffffff00) == 0xbfc05100)` (`:344`) is a dominating predicate.  The cross of a
dominating predicate with a body-tested partition IS the JOINT-CELLS floor.  Six seats read it as a floor gap / the same
cross pass 4 demanded (codex, grok, deepseek, glm, kimi-k3, minimax); counting arguments, the "repair 10 already rowed
3 of 4" argument is dispositive because it is a measured commitment of the round, not an opinion.  **The Opus seat's
clause-(e) grade is overturned on the grade -- and note it agrees on the action** ("VISIBLY ASYMMETRIC ... I recommend
it").  Grading it floor is what makes repair 11 owe a table and a pass; grading it a tidy would let it ship, and that is
the error.

This is precisely the pass-3 "sides taken somewhere, not crossed with the label" shape that pass 4 was minted to fix,
reproduced one axis over -- writes got both widths at the window, reads got only `lw`.  It is #499's shape: a class
repaired at the cells the earlier mutants used, leaving the symmetric cell open.

**A2 (a latch keyed on the CONTROL ENDIANESS bit 0x100) is clause (e), and here the Opus seat is right.**  `dev_sgi_ip32.c:375`
clears ENDIANESS UNCONDITIONALLY (`idata &= ~CRIME_CONTROL_ENDIANESS;`) -- there is no `if` on it.  The CONTROL write arm's
generating set is {DOG 0x200, HARD_RESET 0x800, leftover != 0}, and `ACCEPTS` already crosses CONTROL writes with exactly
those value partitions ({0x0201,0x0001,0,0x0200}).  0x100 is a value bit the body writes but never branches on -- the
"value or combination the body never tests is clause (e) DISCLOSED" rule, and the pass-11 generating-set discussion, put
it squarely in clause (e).  Disclosure is the floor for A2.

### R1(b) -- repair 11 owes BOTH a targeted table AND closing pass 6; the Opus augmentation run does NOT discharge it.

Adding `("ldP",0x00,0)` inserts one accepted access into the prologue of the two sessions that iterate `ACCEPTS` -- `rearm`
(probe `:740`) and `latch x5` (`:913`).  Their command lists therefore change.  By the tables' own targeting rule, **every
earlier kill whose red rows sit in those two sessions must be re-measured** against the augmented probe.  That is a large
set -- from `killtable8_20260914/logs`, the `latch x5` and `rearm once` reds cover `c2_pre_rev`, all five `c3_pre_*`,
`d2_pre_dog0200`, `d4_pre_wistat`, `o_ctl_collide`, `r_byp_rev`, four `r_pre_*`, three `x_pre_*`, the three `c2_rearm_*`,
`c4_kimicli`, `d1_rearm_dog0200`, `d3_rearm_wtime`, `d7_rearm_wrev`, three `r_rearm_*`, three `x_rearm_*`, `rearm`,
`nolatch` -- roughly twenty mutants.  The Opus augmentation run measured ONLY `aug_base` plus the four survivors
(P1/P1b/P2/P2b); it did not touch those twenty.  So it proves the new tuples close the survivors and disturb no row IN
THAT SET -- it does not prove the ~20 earlier kills still red their predicted rows once the prologue grows.  This is
exactly #462's lesson (a changed session perturbs other mutants' scores): *run it, do not assert it.*

And because pass 4 AND pass 5 have now each breached the accepted-kind-cross latch class, the repair-chain amendment
governs: repair 11 owes the CLASS closure -- enumerate the full (branch-side x kind) space from the function's own
branches, close every cell in ONE diff, and write into the CONTRACT which cells are floor and which are clause-(e)
disclosed.  Closing pass 6 then VERIFIES THE ENUMERATION rather than hunting cells, so it is light -- but it is owed,
because the first VALID pass with zero floor breaches surviving adjudication is not pass 5 (pass 5 found A1).

### R1(c) -- DISCLOSE-and-do-not-add is REJECTED for A1.  It is a floor breach; disclosure cannot discharge a floor cell.
DISCLOSE is the correct disposition for A2 (and for A3, A5).

### Repair 11, concretely
* **A1 -- ADD `("ldP",0x00,0)`** (required, floor).  `accept()` already routes `ldP` correctly (`:728-732`).
* **A2 -- DISCLOSE by name** (required).  Since repair 11 re-tables `ACCEPTS` anyway and the Opus run measured the two
  CONTROL-0x100 tuples killing P2/P2b with no row disturbed, folding them in is a LICENSED clause-(e) strengthening
  (measured delta, no cost) -- but the contract must record them as clause-(e) strengthening, NOT as floor, or a future
  pass will treat every value bit as floor.
* **A3 -- DISCLOSE** (multi-axis NOTICE-channel joint; the floor rows single axes).  Accepted.
* **A5 -- DISCLOSE machine-config lvalues by class AND REWRITE item 9.**  Item 9 is a WRONG RECORD (see below).
* **A7 -- already corrected in place** (the "addressed lanes" docstring; the header carries the 2026-09-14 glm note).
* **A8 -- reword** with repair 11.

### A1-A8 dispositions
| # | ruling |
|---|---|
| A1 | **FLOOR breach, L2. ADD in repair 11.** (coordinator's ADD upheld; its clause-(e) fallback overturned) |
| A2 | **clause (e). DISCLOSE required; adding the tuples licensed as clause-(e) strengthening.** |
| A3 | DISCLOSE (multi-axis channel joint). Accepted. |
| A4 | Killed (135/141). No gap. Accepted. |
| A5 | DISCLOSE machine-config lvalues; REWRITE item 9. Accepted. |
| A6 | Killed (P6 137, P7 137); minimax's warrant false. Accepted (none). |
| A7 | Corrected in place. Accepted. |
| A8 | Overstated; reword with repair 11. Accepted -- and it is an L4 record (below). |

### L4 wrong records in Part A (file: `regress/crime_width_probe.py` unless noted)
1. **Item 9: "every lvalue the function reads is nonzero where a refused answer is read, including HARDINT" is FALSE.**
   `d->use_fb` (`:229`, = 0 on a non-graphics ip32, giving REV 0x11), `flag_for_128MB` (`:262`, = 0 at `-M 64`) and
   `idata` (0 on reads) are all read where a refused answer is read and are all 0.  Opus P5 (`odata=d->use_fb`) surviving
   141/141 is the measurement.  Rewrite to the form Opus gives: every lvalue that is NONZERO at a rowed refused read is
   caught; machine-config lvalues 0 on the probed machine are DISCLOSED.
2. **The contract's "REV also from the PROM-probe window in both directions" (item 4/8) and "closes the cross" (A8) are
   FALSE** -- the window is crossed with 4R/4W/8W, not 8R, so it is neither "both directions" nor a closed cross.  Reword
   with repair 11.
3. **`killtable8_20260914/POSTTABLE.out` FLOOR line "(d) ... pre-set and re-arm at every ACCEPTS kind" is circular**
   (it certifies the list against itself, as grok noted) and asserts the cross closed while `ldP` is absent.  POSTTABLE 8
   is a frozen artifact; repair 11's new POSTTABLE carries the true statement, and POSTTABLE 8 should get a correction
   note in the style it already uses for the docstring change.

---

## PART B -- #530 lcaisalane, closing pass 3, repair 3, 93 rows

### R2 -- the gated fallthrough (B1) is NOT a (d)-floor breach, but it IS a CONTRACT breach; option (c), and it owes a table AND closing pass 4.

**Floor or (e)?  Precisely: neither of the two clean answers the split proposes.**  The Opus seat is right on the narrow
point that W1-W4 are not DEPENDS-ON (d) breaches of the FIX -- the fix folded `ofs = (relative_addr & 3) % len` and added
`if (len == 0) return 0`; it never touched the write arm's `return`, and the write body tests neither `len` nor the lane,
so a conjunct on them is a conjunct on an untested value.  And the c1_w1w precedent the other seats cite is weaker than
cited: its own measuring seat graded it clause-(e) COVERAGE DEBT (`opus_c1_20260914/OPUS_ANSWER.md:11`, verified), rowed
only inside the position-cell closure -- it was never "ruled floor".  So the packet's premise that c1_w1w was ruled
in-scope is itself an error (below).

**But the disposition does not turn on the (d) letter, because the CONTRACT names x_wfallthru with NO width or lane
scope** ("the write arm's `return' removed ... the `iir' rows") and rows it at exactly (1,2) and (4,2) at one port.
W4 (`len == 1 || len == 4`) exempts exactly the two widths those rows use and sweeps the 93-row table CLEAN.  A detector
that catches a contract-named edit only at the widths its rows happen to use has not caught the edit.  A clean-sweep of a
NAMED edit is the strongest possible signal that "shipped a detector with the fix" is false about that edit -- so this is
a WRONG RECORD (L4), and an L4 must be fixed in-round.  It rises to L2-in-spirit if the round keeps the claim unscoped.
Either the rows or the claim must change this pass; pass 3 cannot close over it.

**Which of (a)/(b)/(c)?  Option (c), and option (a) "scope and close now" is the coordinator disposition I overturn.**
Two considerations decide it against pure disclosure:
* This channel has escaped in TWO consecutive passes (closing pass 2, unconditioned; closing pass 3, gated W1-W4 + RD2).
  The repair-chain amendment's converge-in-one-diff / verify-the-enumeration discipline is exactly for a recurring class,
  and #499's ruling forbids disclosing away a reproduced breach that is cheaply catchable.
* The cost of (c) is genuinely low and the #462 hazard does not apply: repair 4 ADDS sessions only and changes no
  existing session's commands, so the targeting rule moves no earlier kill.  Opus measured the closure: the 0x3fa STW+STQ
  pair kills W1/W2/W4; a lane-0 0x60 session with a queued 8042 reply kills W3; one LDBU-IIR phase kills RD2.

Option (a) is defensible by the pure clause-(e) letter, and it is the retreat #499 was written to refuse; option (b)
leaves W3 and RD2 open.  So (c): row what is observable, and honestly scope + disclose what is not -- the class is NOT
fully rowable (split heads have no read-side-effect port; no lane-1 port is established; lane-3 direct wdc 0x1f7 is
unbuilt), which is precisely the "write into the contract which cells are covered and which are deliberately not" the
amendment demands.

**Does the repair owe a full closing pass or only its table?  BOTH.**  Repair 4 produces new floor-bound material
(the class-closure rows), so it owes closing pass 4 -- which, being a class-closure repair, VERIFIES the enumeration
(the 0x3fa pair + 0x60 session close every observable fallthrough cell, and the disclosed cells are genuinely
un-observable) rather than hunting further cells.  Its kill table is LIGHT because it adds sessions only: measure base,
W1-W4 red, RD2 red, and the new rows' own kill mutants; no earlier kill can move (targeting rule), so none re-runs.

**Is B2 (RD2) inside the contract at all?  No.**  RD2 duplicates the read arm's forward -- a ROUTING edit, not a position
edit.  The contract names "the read arm's success return turned into a failure" (a polarity edit) and does not name a
duplicated forward, so RD2 is clause-(e) debt OUTSIDE the contract as written.  It is, however, the most realistic escape
on the record (an interrupt handler reads IIR through this window) and costs one phase.  Since repair 4 re-tables anyway,
row it; at absolute minimum it must be DISCLOSED by name.

### B1-B7 dispositions
| # | ruling |
|---|---|
| B1 | **CONTRACT breach (L4 -> in-round). REPAIR, option (c).** (coordinator's option (a) overturned) |
| B2 | **Outside the contract as written; clause (e). ROW it in repair 4 (cheapest row) or DISCLOSE.** Recommend row. |
| B3 | DISCLOSE; widen `lcaisasize` a<4:3> -> a<4:0>. Accepted (H1a is EQUIVALENT-by-construction; H1b 93/93 keys a<4:2>=0x1c). |
| B4 | keep DISCLOSED (body never tests the data). Accepted; warrant already corrected in the header. |
| B5 | r_fwdret still EQUIVALENT (Opus re-measured and read `core/memory.c`). Accepted (none). |
| B6 | Corrected in place. Accepted. |
| B7 | kimi CLI's data-decline and forced `return 0` both 89/93 -- killed by the split head-failure abort. Refuted. Accepted. |

### L4 wrong records in Part B (file: `regress/lca_isalane_probe.py` unless noted)
1. **The CONTRACT's x_wfallthru entry is unscoped** while the rows deliver it at two cells.  Scope it in repair 4 to name
   the caught cells (lanes 0 and 2 at every direct width), the EQUIVALENT cells (head cells, no read-side-effect port),
   and the DISCLOSED cells (lane 1, lane-3 direct wdc).
2. **The `lcaisasize` disclosure "the size field a<4:3>" is too narrow.**  H1b keys on a<4:2> (0x1c); the class the
   handler discards is the whole pre-shift low five bits a<4:0>.  Name the class by a<4:0>.
3. **Also flag, from the panel's own premise:** the claim (glm/kimi CLI/codex) that "c1_w1w was ruled in-scope" is false
   -- it was graded clause-(e) debt.  This is a reasoning error in the panel packet, not a shipped-record error, but it
   should not be carried forward as precedent.
4. (No action -- already corrected in-tree: the data-class warrant, session 4h's "rows above", THE CELL SPACE opener, and
   POSTTABLE 4's "Every leg DETECTED"; each carries its 2026-09-14 correction note, verified.)

---

## SEAT LEDGER (this adjudication)
* **Part A:** answered -- codex, grok, kimi CLI, glm, deepseek, kimi-k3:cloud, minimax (first fire TimeoutError 44 b;
  re-fire 6027 b answered, its P6/P7 findings measured KILLED by Opus), Opus (measuring). **agy: DELIBERATELY NOT FIRED**
  (measurement reservation, owner ruling 2026-08-30) -- not a failure, not agreement.  8 of 9 mandated + this seat.
* **Part B:** answered -- codex, grok (verdict token absent from the file, content is a full CLOSES answer -- a parse
  miss, not a seat failure), kimi CLI, glm, deepseek, minimax, kimi-k3:cloud, Opus (measuring). **agy: DELIBERATELY NOT
  FIRED.**  8 of 9 mandated + this seat.

## SUMMARY OF WHAT RUNS NEXT
* **#529:** repair 11 (add `ldP`; fold the two CONTROL-0x100 tuples as disclosed strengthening; rewrite item 9 and the
  "both directions"/"closes the cross" wording; correct POSTTABLE 8's circular floor line in the new POSTTABLE) ->
  targeted kill table over the ~20 mutants that red the `rearm`/`latch x5` sessions plus P1/P1b/P2/P2b -> closing pass 6
  (enumeration verification).
* **#530:** repair 4 (option (c): add the 0x3fa STW+STQ phases, a lane-0 0x60 session with a queued reply, and the RD2
  read-IIR phase; scope the x_wfallthru contract entry; widen the `lcaisasize` disclosure to a<4:0>) -> its light kill
  table (adds-only, no earlier kill moves) -> closing pass 4 (enumeration verification).

The FIX in each round is correct and untouched; both repairs are to the DETECTOR only.
```
FABLE_ADJ_20260914_C
```
