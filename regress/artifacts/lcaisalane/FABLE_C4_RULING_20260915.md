# ADJUDICATION -- two closing passes, one ruling.  The Fable 5.1 seat, firing LAST.

```
MODEL: claude-fable-5-1
FABLE_ADJ_20260915_D
# CHECKPOINT -- 2026-09-15 ~07:xx   HEAD 9c91999 (records)   two rounds in flight, both UNCOMMITTED
```

**PART A (#529 crimewidthkill) VERDICT: `REPAIR 12` -- pass 6 does NOT close.  A1 is a FLOOR breach surviving
adjudication (six mutants at 141/141, four guest-visible, MEASURED).  Repair 12 = codex's `latch said` row (floor; it
closes the ANNOUNCED accept-guard-growth class over all 46 ACCEPTS cells by construction), the item-6 narrowing plus a
silent-bypass disclosure (REQUIRED), `free revP said` (licensed strengthening), value rows for the silent form (licensed;
if taken, from the ENUMERATION, not from the six mutants that happened to be built), and the A8 rewrites; then TARGETED
kill table 10 and CLOSING PASS 7, which VERIFIES the accept-side enumeration.**  Evidence basis: 8 of 9 mandated seats
(codex, agy, grok, kimi CLI, glm, deepseek, minimax, Opus measuring) plus kimi-k3:cloud as an extra transport, plus this
seat.  Every seat answered.

**PART B (#530 lcaisalane) VERDICT: `REPAIR 5` -- pass 4 does NOT close.  The forward-count class escaped for the THIRD
consecutive pass (R2w, WT6/WTsplit, RD2L0, L3gate, all 111/111, all guest-visible, MEASURED).  Repair 4 owed the class
closure and delivered the seat-named cells; repair 5 owes the closure DERIVED FROM THE HANDLER (the Opus Q1 table), every
observable cell in ONE diff, lanes 0-2 on ARCHITECTURAL channels and the 8042 stub -- with its liveness row -- for lane 3
only; then kill table 6 and CLOSING PASS 5, which VERIFIES the enumeration.**  Evidence basis: 8 of 9 mandated seats
(codex, agy, grok, kimi CLI, glm, deepseek, minimax, Opus measuring) plus kimi-k3:cloud, plus this seat.  Every seat
answered.

**Which of the coordinator's proposed dispositions is wrong -- answered first, in one place:**
1. **Part A, RA1's lean** ("(ii) for the four measured cells plus TIME 8W, (i) for the rest").  Not incoherent --
   UNDER-SPECIFIED, and wrong in one respect: (i) is not one horn of a choice, it is REQUIRED (item 6 is a false record
   however many value rows ship).  And a value-row set drawn from the mutants that were built, rather than from the
   derived per-cell table, reproduces the `#499` shape this chain has now met three times.  Ruled below.
2. **Part B, B1/B2/B3 graded "FLOOR".**  Disposition upheld (in-round, class closure owed); the GRADE LABEL is wrong by
   the letter and it matters for future passes: R2w, WT6 and RD2L0 are ROUTING edits, not weakenings of a predicate the
   fix depends on, so they are not clause-(d) floor.  They are CONTRACT breaches (L4) inside a claimed-whole cell space
   PLUS the repair-chain amendment's class-closure obligation.  Same outcome, different warrant; record the right one.
3. **Part B, repair 5's all-stub design** (32 direct cells on the 0x61-0x6f counter).  OVERTURNED in part: lanes 0-2 go
   on the architectural channels the seat already measured (8042 queue, IIR, CMOS REG C / 8253); the stub carries lane 3
   only, with the liveness row, and is recorded as an emulator-model oracle.  Reason in RB1.
4. **Part A, "the LATCH cross is complete" (A9)** -- upheld, with the sentence that was missing: the ACCEPT side of the
   same 46 cells was CLAIMED by item 6 and carried by nothing.  That is the L4 that makes A1 an L2 as well.

Everything else the coordinator proposed is upheld, with corrections of wording noted where they occur.

---

## PART A -- #529 crimewidthkill, closing pass 6, repair 11, 141 rows

### R1 -- A1 is a FLOOR breach, L2, and it is a CLASS.  Verified against the source, not taken from the seat.

The width arm (`dev_sgi_ip32.c:275-296`) branches on `len == 8`, `len == 4`, `writeflag` and `relative_addr & 4`; every
accepted access then reaches `switch (relative_addr)` (`:322`) and `d->reg[relative_addr / 8]` (`:277-290`).  So the
LABEL is a floor axis of the width guard under the JOIN clause (the selector flows into an lvalue the guarded body reads
and writes, and the switch re-tests it after the join).  A growth `len == 8 && relative_addr != CRIME_CONTROL` is the
canonical accept-row-failability mutant -- the joint guard-growth form -- and item 6 CLAIMS the accept side is pinned
"at any single cell".  Measured: C1, G1-G5 each 141/141, and G1/G2/G4/G5 change what the guest sees (an 8R of CONTROL
answers 0 not 0x100; an 8R of INTSTAT answers 0 with an interrupt pending; a 4W to REV from the window no longer
redirects; a 4W to INTMASK does not land).  All four of the seat's grounds hold on reading: the de-escalation clause
(pre-fix this edit ended the process at the first such access), the JOIN clause, item 6's own sentence, and the
`#499` shape (grok's `len == 8 && relative_addr != 0` was repaired at +0x00 by `acc8 near` and nowhere else).

**Why it is a class and not six cells:** `rearm once` and `latch x5` COUNT `-- declined.` (probe `:765`, `:949`).  A
wrongly declined accepted cell either comes after the first refusal (silenced) or IS the first refusal (takes the one
notice the lh +0x06 should have had).  Either way the count is 1.  So ACCEPTS carries the latch cross and carries nothing
about acceptance -- for any of its 46 cells.  Six seats read the enumeration and said CLOSES; none of the six engaged
with what the two ACCEPTS-fed rows can OBSERVE.  Counting arguments: one measured clean sweep outweighs seven readings
that did not look at the channel.

### R2 -- codex's row is the class closure for the ANNOUNCED form, and it is general by construction.

`row("latch said", said(t, 2, 0x06, clean), 1, ...)` in latch x5 (`said` at `:381` counts the exact announce text).  All
46 ACCEPTS accesses precede the lh +0x06 in that session (`:934-940`), so any guard growth at any of them sends that cell
into the announcing decline arm (`:314-319`) and the lh's own text is absent.  The window kinds are covered too: the
width arm declines BEFORE the pc test, so `swP/sdP/ldP/lwP` announce like any other (G4 measured red).  Base 149/149, red
on C1 and G1-G5, no shipped row moved, no command list changed.  **Take it as written; do not fold it into `latch x5`**
(a folded row loses the attribution of WHICH half failed).

### RA1 -- the SILENT bypass (G6).  (i) is REQUIRED; (ii) is LICENSED; the cell set is the ENUMERATION's or none.

G6 (`if (len == 8 && relative_addr == CRIME_CONTROL) goto crime_declined;` before the width test) is outside the
de-escalation class -- pre-fix an inserted `return 1;` was equally silent, so the deleted `exit(1)` never announced it --
and outside the DEPENDS-ON enumeration (it inserts a predicate; it weakens none).  So it is NOT floor, and no row can be
DEMANDED for it.  But item 6's literal "any single cell" is false of it, and a false record is L4 whatever the grade.

* **(i) REQUIRED:** narrow item 6 to "the ACCEPT SET shrunk at any single cell IN THE GUARD-GROWTH (announcing) FORM --
  carried by `latch said` over every ACCEPTS cell", and DISCLOSE the silent bypass BY CLASS, naming the cells where a
  value row catches it anyway (below) and the cells where it is EQUIVALENT at the guest (REV 8W/4W/4R out of the window,
  CONTROL 4R: the prelude rewrites or the high half is 0).
  *** THIS CLAUSE ALSO NAMED **TIME 4W/4R** AS EQUIVALENT, AND CLOSING PASS 7 MEASURED IT GUEST-VISIBLE -- mutant E2 at
  157/157, differing on four channels (`regress/artifacts/crimewidthkill/opus_close7_20260915/OPUS_REPORT.md', E2).
  The reason the ruling gave is wrong in the same place: a read takes `odata' BEFORE its own crime_update_crime_time(),
  so a skipped update ARRIVES ONE ACCESS LATE instead of accumulating.  Corrected here rather than only in the probe
  because item 6's wrong sentence was COPIED FROM THIS ONE, and correcting one of the two leaves the record
  inconsistent -- the seat that measured it said so explicitly.  The ruling's own disposition is otherwise untouched:
  TIME 4W/4R is now an unrowed single-axis FLOOR cell owed by repair 13. ***
  *** RA3 of this ruling -- "It is clause (e) by the DEPENDS-ON bound (`d->warned' is not a field the accept bodies
  read)" -- IS **OVERTURNED TO FLOOR** BY THE 2026-09-16 ADJUDICATION (FABLE_C5_RULING_20260915.md, S-A.7), ON FOUR
  INDEPENDENT GROUNDS, THE FIRST OF WHICH IS IN THE DIFF ITSELF: the fix's own decline arm READS `d->warned' at
  dev_sgi_ip32.c:314, in a hunk THIS DIFF ADDS, so the latch is a device-state lvalue the fix's own repair path reads --
  a floor axis by the pass-11 floor definition and the M_ICLR precedent, and by this round's own practice, since it
  built and measured the shrink.  Bounded, and not #392: the floor is the diff-closed 56-cell product, of which the
  ROWS OWED are the 23 open guest-visible cells.  *The measuring seat disputed this clause and was right; the ruling
  that adopted it was mine, and a ruling in one's own favour is the one least likely to be tested.* ***
* **(ii) LICENSED (measured delta: `dg ld ctl`, `dg ld istat`, `dg sw imask`, `dg swP pc` each red on its cell, green on
  base, new sessions only).**  If value rows are added -- and I RECOMMEND it, because at those cells the silent form has
  the SAME guest effect as the growth form and a detector that sees one and not the other is claiming more than it
  pins -- the set is the Opus per-cell table's guest-visible "no" cells, all of them, in ONE diff: REV window 4W/8W/8R
  (the redirect), CONTROL 8R/8W, INTSTAT 8W/8R/4W, INTMASK 4W, TIME 8W, default `sw/lw 0x40`.  Twelve cells, each with
  a CHANNEL line in `PRETABLE.out` naming the mutant and the observable.  A five-cell set drawn from the mutants the
  seat happened to build is licensed too, but then the record says "5 of 12 rowed, 7 disclosed" -- it may not say the
  silent class is closed.  What I reject is only the half-set presented as closure.
* The coordinator's worry about incoherence is answered: (i) states what the CONTRACT claims; (ii) states what the
  DETECTOR additionally pins.  Different questions, both answered, no contradiction.

### RA2 -- repair 12 owes TARGETED TABLE 10 and CLOSING PASS 7.  The seat's augmentation run does not discharge either.

* **Table 10, and why the run is not it:** the seat APPENDED rows to a frozen copy; repair 12 re-types them into the
  shipped probe.  A re-typed row is a new instrument and is measured, not assumed.  Legs: base; C1, G1-G6, C2 (the new
  rows' own kills, including G6 for any value rows); the 17 table-9 pre-set kills IF POSTTABLE 10 will state their new
  scores (the "they also red `latch said`" prediction is REASONED -- the seat says so -- and a predicted score in a
  measured column is the frozen-number class; run them or omit them from the record, ~17 legs, about an hour in four
  lanes).  The 12 re-arm kills and every kill outside the two sessions cannot move: no command list changed (the
  targeting rule), and I checked that `latch said` reads latch x5's existing transcript only.
* **Pass 7 is owed** because the first VALID pass with zero floor breaches surviving adjudication is not pass 6.  It is
  LIGHT and it VERIFIES rather than hunts: (a) for each of the 46 ACCEPTS cells, name the row that reds under an
  ANNOUNCED decline (`latch said`, by construction) and under a SILENT decline (a value row, or "equivalent", or
  "disclosed") -- 92 cells, derivable by reading; (b) confirm by reading latch x5's command list that every ACCEPTS
  access precedes the lh (the generality argument); (c) nothing else.  Full roster, per the every-stage rule.

### RA3 -- is there a further accept-side class?  Yes, and it is the one pass 7 enumerates; plus one thing to BUILD.

* The accept side of the 46-cell cross has exactly two forms a single edit can produce: ANNOUNCED decline (closed by
  `latch said`) and SILENT decline (RA1).  That is the enumeration pass 7 verifies: cell x {announced, silent}.
* **A `d->warned`-keyed shrink must be BUILT before it is disclosed.**  The seat reasoned it clause (e) and did not build
  it.  Two forms: keyed on 8R (`len == 8 && (writeflag == MEM_WRITE || !(d->warned & CRIME_W_LEN))`) -- I predict
  KILLED: `sb keeps`/`sh keeps`/`lo keeps`/`hi keeps`/`mid keeps` (`:691-842`) each read a seeded slot with an accepted ld
  AFTER a refusal, which such a shrink answers 0; and keyed on 8W -- may escape (the only accepted 8W after a refusal
  whose value is read back by an accepted read is unclear from the rows).  It is clause (e) by the DEPENDS-ON bound
  (`d->warned` is not a field the accept bodies read); if it escapes, DISCLOSE it by name.  "Reasoned, not built" is a
  prediction and this chain has had enough of those.
* Classes NOT to reopen: accepted-but-mishandled (landing, lane, re-map) are items 6/7's anchor rows and earlier tables'
  material, outside this chain's class.  Pass 7 is told so explicitly, or the chain does not terminate.

### A1-A9 dispositions
| # | ruling |
|---|---|
| A1 | **FLOOR breach, L2, a CLASS; also L4 (item 6).**  Coordinator upheld. |
| A2 | **REPAIR 12 takes codex's row as written.**  Upheld. |
| A3 | **RA1: (i) REQUIRED; (ii) licensed and recommended over the 12-cell derived set.**  Coordinator's lean corrected. |
| A4 | Clause (e) by the bound (the decline arm reads no `pc`); ADD `free revP said` as a licensed strengthening; item 5 gains a rowed line for pc at that one cell and a disclosed line for pc JOINTS.  Upheld. |
| A5 | Killed 139/141 both forms; premise true, conclusion refuted.  Upheld (none). |
| A6 | Killed 131/141; minimax's premise false (default-arm answer rows sit at unaligned offsets).  Upheld (none). |
| A7 | EQUIVALENT by construction (`idata` set only on writes, `odata` consumed only on reads); one DISCLOSED line.  Upheld. |
| A8 | All corrected in repair 12; two additions below (item 3 / `:495` "tested").  Upheld. |
| A9 | 40 floor + 2 clause-(e) strengthenings + 4 positional repeats = 46 (I recounted the tuple at `:731-743`).  deepseek's "six vs eight" is not an error: six KINDS, eight ENTRIES.  Upheld. |

### L4 wrong records in Part A (file: `regress/crime_width_probe.py` unless noted)
1. **Item 6, "the ACCEPT SET shrunk at any single cell"** -- false at every cell the Opus per-cell table marks "no".
2. **Item 3 (`:26-27`) "the arm's three TESTED idata bits (DOG 0x200, RESET 0x800, ENDIANESS 0x100)" and the comment at
   `:495` "ENDIANESS (0x0100) is the arm's third tested bit"** -- FALSE at both sites: `:375` is `idata &=
   ~CRIME_CONTROL_ENDIANESS;` with no `if`.  The header's own repair-11 note (`:728`) says the opposite correctly.  Two
   sites; the grep-for-siblings rule.
3. **DISCLOSED "ACCEPT cells at unrowed slots"** -- implies a touched slot is pinned; touching pins the LATCH, never the
   acceptance.
4. **DISCLOSED "an accepted WRITE at +0x00 or +0x08 shrunk away ... no round trip there can observe"** -- wrong twice: the
   window 4W redirects (G4 measured), and the 8-byte CONTROL write is unrowed (G1).
5. **Repair-11 comment (`:725-726`) "crossed the window with the DIRECTION on writes only"** -- the missing cell was the
   8-byte WIDTH on the READ side; say that.
6. **"the two label cells whose arms have NO body"** -- three: REV from OUTSIDE the window is a label cell with no body
   for that access.  Name it.
7. **`killtable9_20260914/POSTTABLE.out` FLOOR line** -- true for pre-set/re-arm; add the note "the ACCEPT side of the
   same cross is NOT closed by ACCEPTS (closing pass 6)" in the style it already uses.
8. **`panel_20260915_011138/brief_sent.md` "mutants of table 9, verbatim"** shows P3-P7; table 9 ran P1/P1b/P2/P2b only
   (`mutants529i.py` imports exactly those; codex and agy both caught it).  A frozen artifact; the ledger entry for this
   panel carries the correction.
9. **The adjudication brief itself:** "Six seats CLOSE (...)" lists SEVEN names.  Not a shipped record; noted so the
   ledger entry does not copy it.
10. `free_one` ignoring `clean` (codex): a truncated transcript can only produce a false RED there (count 0 against want
    1), never a false green -- not a vacuity, but fix it for consistency with `said`.

---

## PART B -- #530 lcaisalane, closing pass 4, repair 4, 111 rows

### R3 -- the forward-count class escaped a THIRD time; the class closure owed at repair 4 was not delivered.

Verified on the source: the write arm returns the forward (`dev_lca.c:299-303`); the read arm forwards once and fills
(`:305-311`).  R2w (`if (len != 1)` + a second forward) is the contract-named RD2 gated on the one width its row uses
(`iir lca rd`, LDBU, `:826`).  WT6/WTsplit gate the write fallthrough to the split-tail widths, which the header calls
part of THE CELL SPACE "rowed WHOLE" (`:73-81`) and the scoped x_wfallthru entry (`:101-109`) does not mention.  RD2L0
duplicates the read at lane 0.  All 111/111, each moving exactly its own discriminator channel (`DISC_SUMMARY.out`).

**Grade, precisely.**  None of these is a clause-(d) floor breach by the letter: the fix folded `ofs` and added the
`len == 0` refusal; RD2/WT insert routing, weakening nothing the fix depends on.  They are (1) L4 -- the RD2 sentence is
unscoped and POSTTABLE 5's "RD2 at lane 2" overclaims (both already carry 09-15 correction notes, verified), and the
tail cells are inside a space the header claims rowed whole with no disposition; and (2) the repair-chain amendment's
obligation: two consecutive passes of one class owe the class closure, and this is the third.  In-round either way.
The coordinator's "FLOOR" label is corrected so that no future pass cites this chain as precedent for enumerating
routing edits as (d) floor everywhere.

### RB1 -- the 0x61-0x6f stub as a floor oracle: acceptable for LANE 3 ONLY, with the liveness row, recorded as a model oracle.

The stub is real and I read it: `dev_pckbc.c:941-951`, PC-style (`bus_isa.c:308-310` passes `pc_style_flag = 1` unless
`BUS_ISA_PCKBC_NONPCSTYLE`), every access to `relative_addr` not in {0, 4} bumps a function-static `x` and bit 0x10 of
the answer is its parity, reads and writes alike.  As a channel it varies under every fallthrough/duplicate mutant and
is stable on base -- the vacuity floor is satisfied.  What it is NOT is durable: it is a `TODO`, shared by every pckbc
instance through one static, and its implementation would vacate every row resting on it in one edit.  The liveness row
turns that from silent to LOUD, which is the harness's own standard, so the stub is admissible.  But:

* **Lanes 0-2 use the architectural channels the seat MEASURED** -- lane 0 writes: `kbcq` (exists); lane 0 reads: the
  8042 with TWO replies queued (D, measured at (1,0), (8,0) and tail 6); lane 2 writes: `iir`/`iirw` (exist); lane 2
  reads at len 2/4/8: IIR with TXRDY armed (B, measured) in a NEW session -- do not extend `iirr`, or table 5's RD2 kill
  moves under the targeting rule; lane 1 R and W: CMOS REG C (G) or the 8253 at 0x41 (F), one arming store each.

  *** THIS BULLET IS **OVERTURNED** BY THE 2026-09-16 ADJUDICATION (FABLE_C5_RULING_20260915.md, S-B.4): CMOS REG C and
  ns16550 IIR ARE ONE-SHOT LATCHES, AND A LATCH CANNOT CARRY A FORWARD-COUNT CLASS.  `dev_mc146818.c:565` -- the read
  does `d->reg[MC_REGC*4] = 0x00;`, so a second read finds it already zero, and the write path is a plain assignment.
  `dev_ns16550.c:211-213` -- the read clears IIR_TXRDY once; the write path is `d->fcr = idata;`.  **A latch separates
  ZERO accesses from AT LEAST ONE; it can never separate ONE from TWO, which is exactly and only what this class asks.**
  Measured consequence: WWall 169/185 is sixteen stub rows and NOTHING else, RWall 167/185 is 16 stub + 2 tailr, and
  RD2post 161/185 has no architectural carrier at lanes 1-2 -- so the never-sole-carrier requirement in the very next
  bullet was breached at three cells BY THE CHANNELS THIS BULLET NAMED.  Repair 6 moves lanes 0-2 and the tails to the
  8253 per-counter rd_msb/wr_msb ALTERNATORS at 0x40/0x41/0x42, and keeps stub3 + its liveness row for lane 3 ONLY,
  where the 8253 is structurally blind (port 0x43 advances no flip-flop; cdxZL3 150/150, measured).

  *** AND THE CORRECTION ITSELF NEEDS CORRECTING, WHICH IS WHY IT IS WRITTEN OUT HERE RATHER THAN SUMMARISED.  The C5
  ruling's L4 item 2 quotes this bullet as naming CMOS and IIR, and it does -- but it names them **as one of two
  options**, "CMOS REG C (G) or the 8253 at 0x41 (F)".  The 8253 was on the table from the start and repair 5 took the
  other branch.  So the defect is NOT that the ruling named an unusable channel; it is that **it offered two channels
  as interchangeable when one of them is structurally incapable of the measurement, and gave no discriminator for
  choosing between them.**  The discriminator now exists and is checkable by reading, which is the part worth carrying
  forward: A FORWARD-COUNT ROW NEEDS A COUNTER OR AN ALTERNATOR, NEVER A LATCH.  The never-sole-carrier PRINCIPLE
  stands untouched; only the channel list under it was wrong. ***
* **Lane 3 direct, both arms, all four widths: the stub at 0x63/0x67/0x6b/0x6f**, plus the MANDATORY liveness row (two
  plain flat reads flip 0x10), plus a contract sentence: "an emulator-model oracle (a TODO counter), not a hardware
  contract; the liveness row reds when port 0x61 is implemented and these rows are then re-derived".  That is the
  `0xffffffff` precedent from the carrier -- an emulator-compatibility oracle, named as such.
* Stub rows at lanes 0-2 are permitted as ADDITIONAL strengthening (they close the data axis cheaply) but may not be the
  SOLE carrier of any lane 0-2 cell.  Cost: about three sessions more than the all-stub plan.  Benefit: the blast radius
  of the TODO being implemented is eight rows plus a liveness row, and 32 floor rows do not rest on one static.

### RB2 -- the enumeration is COMPLETE for the forward-count class on the stated scope; four scope sentences are owed.

The (arm x width-kind x lane) table in the brief is the right one and I re-derived its shape: heads are always lane 3
and tails always lane 0 because `memory_rw` splits at 1 KB and `(0x400k - h) >> 5 = 0x20k - 1`; direct widths are the
CPU's {1, 2, 4, 8}; `len == 0` has no producer.  Cells: direct 4 lanes x 4 widths x 2 arms = 32; tails 3/5/6/7 x 2 arms
= 8; heads EQUIVALENT (the only mapped 0x1f-mod-0x20 ports are 0x3ff/0x2ff = ns16550 SCR, whose `default:` arm at
`dev_ns16550.c:298-302` reads `d->reg[relative_addr]` with no side effect -- verified; 0x60-0x6f holds no such port).
The contract writes down: (1) the machine as probed -- alphabook1, no IDE image (so no wdc: `bus_isa.c:275-286`), no
X11 (no VGA); (2) the width set and the split derivation; (3) `len == 0` disclosed; (4) the DIRECTION swap (a read
routed through the write arm) is a different class and is caught by the existing value rows -- one sentence, predicted
(every 4-byte read row answers 0), not a row.  Two things the seat did not check, settled here: the lpt read arm
(`dev_lpt.c:79-88`) returns `d->data` or constants -- no side effect, so it is neither a channel nor a gap; IDE-attached
behaviour is OUT OF SCOPE and disclosed (wdc 0x1f7 lane 3, altstatus 0x3f6 lane 2 would add channels, not cells).

### RB3 -- repair 5 owes kill table 6 AND closing pass 5.  The "derived from the handler" argument is what pass 5 checks.

The chain rule closes on the first VALID pass with zero floor-bound breaches surviving adjudication; pass 4 found four.
Repair 5 is new floor-bound material and owes its pass.  That the enumeration is now derived from the arms rather than
from a seat's cells is exactly the claim pass 5 VERIFIES -- repair 4's scope was also "derived" and was short by the
tails.  Table 6 is light (new sessions only; no earlier kill moves): base; R2w, R2w2, WT6, WTsplit, RD2L0, L1gate,
L3gate, dataA (the new rows' own kills); PLUS two the seat did not build -- RD2 gated to lane 1 alone and to lane 3
alone ("covered by construction through R2w's E-load flips" is a prediction, and lane 3's carrier is the stub, whose
rows are the ones being introduced).  Pass 5: full roster, verifies the enumeration cell by cell, hunts nothing.

### RB4 -- dataA is clause (e); closed for free; the record says both.

The write body tests no bit of the value (`byte = data[ofs]` and forward, `:300-302`); by the pass-11 rule the written
value's bits are single-operand marginals, not floor.  The nonzero stores in the new rows close the {zero, nonzero}
partition of a data-keyed fallthrough (dataB is already red on the zero-store rows).  Record: "a fallthrough keyed on
the data's zero/nonzero partition: both sides rowed (licensed strengthening, not floor); keyed on an EXACT data value:
disclosed by class".  Coordinator upheld, with the exact-value residual added.

### B1-B9 dispositions
| # | ruling |
|---|---|
| B1 | **In-round: L4 (unscoped RD2 sentence; POSTTABLE 5 FLOOR line) + class closure (third pass).**  Grade label corrected from "FLOOR" to contract breach + amendment.  Rows: lane-2 reads at 2/4/8 on IIR (new session). |
| B2 | **In-round: L4 (tails inside a claimed-whole space, undisposed) + class closure.**  Rows: the 8042 with one reply queued, 0xd1, split store at SP(0x5f)+0x1f/0x1e/0x1d/0x1b, DIB after (C). |
| B3 | **In-round, same class.**  Rows: two replies queued, then the lane-0 read at each direct width and each tail (D). |
| B4 | **L4 against the 09-15 lane-3 correction** -- "no read-side-effect port is present" is false (the stub at 0x63/0x67/0x6b/0x6f, verified in source); a correction is not safer than what it corrects, third instance.  Cell moves to ROWED (stub + liveness). |
| B5 | Lane-1 correction VERIFIED (E tog61, F, G).  Cell moves to ROWED on an architectural channel (RB1). |
| B6 | Clause (e); closed free; record per RB4.  Upheld. |
| B7 | Heads EQUIVALENT: upheld and verified (ns16550 default arm; bus_isa device list); disclose WITH the port list and the premise so pass 5 re-derives it. |
| B8 | Corrected 09-15 (comment).  Upheld. |
| B9 | Refuted: a head is ONE handler call at ONE port (`relative_addr >>= 5`, `:280`); the model decodes no per-byte ports.  Upheld (none). |

### L4 wrong records in Part B (file: `regress/lca_isalane_probe.py` unless noted)
1. **Header, lane-3-direct warrant as corrected 2026-09-15 (`:108-109`)** -- false; see B4.
2. **Header, the RD2 sentence (`:113-115`)** -- unscoped while its only row is (1, 2, READ).
3. **Header, the scoped x_wfallthru entry (`:101-109`)** -- silent on the tail cells 3/5/6/7 and on RD2 at lanes 0/1/3
   and at tails, all inside its own CELL SPACE.
4. **Header (`:134-137`) "'the correct byte is 0' is unrowed"** -- imprecise (zero correct bytes ARE stored by
   `iir`/`iirw`/`kbcq`); the true limitation is the sentence beside it: no row distinguishes a zero correct byte from a
   nonzero byte at another position.  Keep that sentence, drop the other.
5. **`fix530_20260914/table5/POSTTABLE.out` FLOOR line** -- already carries the 09-15 correction note (verified); no
   further edit owed there.
6. **`c4_20260915/SEATS.txt`** records agy as "DELIBERATELY NOT FIRED" while `agy.txt` (15,936 b, 00:08, token present,
   CLOSES/GO) sits beside it.  The ledger entry records agy as ANSWERED with that file; the frozen SEATS.txt gets a note.
7. **The brief's "THIRD consecutive pass" framing is right**; note for the record that repair 4's scope was derived by
   the coordinator from the seat's cells, which is why the amendment now demands the derivation be VERIFIED by a pass
   rather than asserted by the author.

---

## SEAT LEDGER (this adjudication)
* **Part A** (`crimewidthkill/panel_20260915_011138/`, Opus `opus_close6_20260915/`): codex NO-GO (C1 + the row);
  agy CLOSES / GO-WITH-CHANGES; grok CLOSES; kimi CLI GO-WITH-CHANGES; glm CLOSES; deepseek CLOSES (1,157 b, no verdict
  token -- content read, a real answer); minimax CLOSES; kimi-k3:cloud CLOSES (extra transport); Opus GAP, MEASURING
  (22 legs, 13 binaries).  agy FIRED per the 2026-09-15 owner directive.  8 of 9 mandated + kimi-k3 + this seat.
  Counting arguments: the seven CLOSES are readings of the enumeration; none engaged with the ACCEPTS-fed rows' channel;
  the measured 141/141 sweep is unanswered by any of them.
* **Part B** (`lcaisalane/c4_20260915/`, Opus `opus_c4_20260914/`): codex NO-GO / GAP (R2w2, WT6); agy CLOSES / GO;
  grok GAP (R2w); kimi CLI NO-GO / GAP; glm GAP (WT3; no verdict token -- a full answer); deepseek GAP (dataA; 1,593 b, a
  real answer); minimax CLOSES with caveats; kimi-k3:cloud GAP; Opus GAP, MEASURING (11 binaries, 17 channels, 11/11 on
  prediction).  agy FIRED (the dir's SEATS.txt says otherwise -- L4 item 6).  8 of 9 mandated + kimi-k3 + this seat.

## WHAT RUNS NEXT
* **#529:** repair 12 (codex's `latch said`; item 6 narrowed + silent-bypass disclosure; `free revP said`; value rows
  from the 12-cell derived set or none, recorded as such; A8 rewrites incl. the two "tested ENDIANESS" sites; the
  `d->warned` shrink BUILT in both forms) -> table 10 (base, C1, G1-G6, C2, and the 17 pre-set kills if their scores are
  to be recorded) -> closing pass 7 (verifies cell x {announced, silent} over the 46 cells; hunts nothing).
* **#530:** repair 5 (the Q1 enumeration closed in ONE diff: lanes 0-2 architectural, lane 3 stub + liveness, tails on
  the 8042 queue, nonzero stores, contract re-scoped with the four scope sentences and the lane-3 warrant corrected
  again) -> table 6 (base + the ten mutants named in RB3) -> closing pass 5 (verifies the enumeration; hunts nothing).

The FIX in each round is correct and untouched -- every seat and both measuring reports agree; both repairs are to the
DETECTOR and its record only.
```
FABLE_ADJ_20260915_D
```
