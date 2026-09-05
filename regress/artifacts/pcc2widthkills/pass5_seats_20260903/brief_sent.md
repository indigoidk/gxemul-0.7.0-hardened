# pcc2widthkills -- PASS 5, the closing pass: the domain repaired one function outward (the helper's own lines, four widths).  Detector 96 -> 101 rows; product diff is comments plus the pass-2 typedef.

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly,
and THIS round's pass 3 found the author had (a) mis-credited a row in his own parity table,
(b) applied his own ruling to four arms when it convicted five, (c) never walked the one guard
input the fix itself introduced, and (d) claimed accept-side coverage carried by five rows.
**Check the premises, not just the derivations.**  Where I state something as fact, ask
whether it is true.  A seat that re-derives a premise from something this brief did NOT give
it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/` and `GXEMUL-SEC/regress/`, UNCOMMITTED on top of
`b78bb0f`.**  Three pristine-2021 copies under the project root are NOT this fork.  If your line
numbers disagree with mine by hundreds you are reading one of them -- say so.

**If you cannot read files that is expected** -- every fact you need is inlined.  Name any
premise you cannot settle from this packet rather than guessing at it.

**Where this brief states an ARITHMETIC claim -- a lane value under a mask, a count of blocks,
a latch-bit cardinality -- ENUMERATE it rather than reasoning about it.**  And ENUMERATE THE
RIGHT DOMAIN: the m88k core alignment-checks every non-byte access BEFORE memory_rw, and the
debugger's `put' path does not.

**VERDICT LINE FIRST**, so your answer survives truncation.

## WHY THIS PASS EXISTS, AND WHAT CLOSES THE CHAIN

Pass 4 verified every derivation in the 12 x 9 enumeration and found the DOMAIN one function
too small: the twelve guards all call `pcc2_width_decline()', whose TEST and SET lines every
block depends on, and nobody had mutated the helper.  A one-character edit to its SET line
(`|=' -> `=') swept the shipped 96 rows -- MEASURED by the Opus reader.  Pass 4 also named
the 8-byte width (rows drove {1,2,4}; `put d' reaches with 8) and the accept side reaching
the body at the two print-only arms.  This diff adds five rows and extends the contract's
domain to the helper's operations and the four widths; part 4 measures the five mutants.
**A closing zero must be VALID: the diff delivered (it is inlined), the roster complete or its
misses named, and the zero carried WITH its denominator -- which cells, which shapes.**


Pass 2 (60 rows) had six clean sweeps.  The 78-row repair killed them; pass 2's builder then
found four odd-arm fall-throughs sweeping 78; the 82-row repair killed those.  Pass 3 found
the SAME class a third time (VECBASE, IPL) and three shapes the six-shape list never named.
**Two consecutive passes on one class means the repair owes the CLASS, not the cell**: this
diff enumerates the full space from the guard's own inputs (len, writeflag, relative_addr ->
block, idata, d->warned), closes every cell in ONE diff, and writes into the contract which
cells are covered, which are argued same-channel, which are equivalent by construction with
their warrant, and which are unreachable.  **Your job is to VERIFY THAT ENUMERATION** -- is the
domain right, is every cell's status right, is any status a rationalisation -- and to name the
smallest edit that breaks the property and passes all 96 rows if one exists.  A closing zero
must carry its denominator: say which cells and shapes you swept.

## N. PREMISES ALREADY SETTLED, RE-INLINED

Settled by passes 1-3 (`panel_20260903_121558`, `panel_20260903_152458`, and the measurement
artifacts under `regress/artifacts/pcc2widthkills/`), warrants inline:

1. **The width is LEGAL** -- `mvme_pcctworeg.h`: "bytes, two-bytes, or four-bytes".
2. **`memory_readmax64` composes BIG-ENDIAN**: `(uint8_t) idata' is the HIGHEST-address lane;
   a bare deletion stores the neighbour's byte.  MEASURED (`M_DELETE' -> `rb genctl' 0xbb).
3. **Reachability:** every non-byte m88k access is alignment-checked before memory_rw
   (`#ifndef LS_1 ... m88k_exception(MISALIGNED)' then return) and `relative_addr %= 0x40'
   keeps parity.  SIX even blocks (GENCTL 0x02, TxCTL 0x16, TxICR 0x1a, SCCERR 0x1c, SCCTX
   0x1e, IPL 0x3e) are GUEST-reachable; EIGHT odd OFFSETS -- the six odd-only blocks VECBASE
   0x03, PSCALEADJ 0x15, SCCICR 0x1d, SCCRX 0x1f, SCSIICR 0x2f, MASK 0x3f, plus the T1CTL 0x17
   / T1ICR 0x1b labels of the shared TxCTL/TxICR blocks -- are OPERATOR-only.  Byte accesses
   (`st.b', `put b') are never alignment-checked.
4. **The operator path reaches the SAME guard**: `put h' warns, then `store_16bit_word' ->
   ONE `memory_rw(len 2)' -> the same arm.  `put w' / `put d' likewise give len 4 / 8.
   **A debugger READ does not reach the arm**: `memory_rw' dispatches a device only if
   `(!no_exceptions || (flags & DM_READS_HAVE_NO_SIDE_EFFECTS))' and pcc2 registers
   `DM_DEFAULT' -- so the six odd blocks' READ-side cells are unreachable by construction.
5. **Arm bodies** (inlined below): VECBASE stores `idata & 0xf0' (+ HUH print); SCCICR
   `& 0x1f'; SCCRX and SCSIICR `& 0xdf'; each of those four then (except VECBASE) calls
   `reassert_interrupts()'.  PSCALEADJ stores nothing, prints "ignored (value ...)".  IPL's
   write body stores nothing and prints "write to read-only PCCTWO_IPL; ignored" once per
   process (#119 static).  SCCERR's write body is `= 0' and nothing in the model stores a
   nonzero SCCERR.  TxCTL `& 3'; TxICR `&= ~0x17 |= idata & 0x17'.  GENCTL and MASK store the
   byte and reassert.  SCCRXIACK has NO width guard and never had one: its body ignores idata.
6. **`fatal()' returns**; the announce is once per block per instance via `d->warned', a
   32-bit field with twelve bits assigned, written ONLY inside `pcc2_width_decline()'.
   `reassert_interrupts()' exits the host only on `GENCTL & 0x04' (pcc2c040kill, filed);
   every GENCTL value in the probe keeps that bit clear.  Every probe session is a fresh
   `pty.fork'/`execv' of the emulator.
7. **The ruling, applied to all twelve now**: clause (d) is a FLOOR; a disclosed asymmetry
   cannot discharge it.  Announce-then-fall-through leaves every `dcl' row and `latch all'
   green by construction, so its only channel is a readback (storing arms) or the arm's own
   print (print-only arms).
8. **Pass-3 and pass-4 rosters**: eight answered each time (codex, kimi, grok, glm, deepseek,
   minimax, opus, fable5); agy DELIBERATELY NOT FIRED (reserved for measurement).  Pass 4's
   Opus reader measured; its fable5 seat ratified on an analytic sweep that omitted the helper
   edits and was overturned by that measurement.
9. **The debugger's `put b' never reaches the arms** (memory_rw with NO_EXCEPTIONS is not
   dispatched to a DM_DEFAULT device); `put h/w/d' go through store_Nbit_word and do; guest
   `st.b' reaches every offset.  MEASURED (part 3: a grown guard escaped the `put b' row twice
   with the mutation proven; part 3c: killed by the guest-store form).

## THE TABLES (every number names its log)

The Opus pass-4 reader, on the shipped 96-row instrument (md5 72759b4f) -- the breach this diff closes:
    BASE               96/96   -
    M_LATCHASSIGN      96/96   -
    M_BITSHIFT         96/96   -
    (M_LATCHASSIGN = the SET line assigned; M_BITSHIFT = the bit translated, EQUIVALENT by construction)

Pass-3 seats, on the 82-row instrument (md5 cd22f951) -- the breaches the pass-3 repair closed:
    fable5   M_FALL_VECBASE    82/82   (pass3_seats_20260903/fable/probe_mfall_vecbase.out)
    BASE               82/82   -
    MD                 80/82   rb genctl,rb genctl lo
    MA                 82/82   -
    MB                 82/82   -
    MC                 82/82   -
    (opus reader: MD = guard deleted at GENCTL, the control; MA = break removed at VECBASE;
     MB = at IPL; MC = `writeflag == MEM_WRITE' -> `<= MEM_WRITE' at all twelve)
    kimi     M_FALL_VECBASE 82/82, M_FALL_IPL 82/82, delete@VECBASE 80/82 (latch all, op vecbase dcl)

Part 3 -- `killtable2_20260903/part3/driver.log`, the 96-row instrument, fresh scratch clone,
BASE rebuilt in the clone:
    BASE               95/96   rb t1ctl
    M_FALL_VECBASE     94/96   rb vecbase own,rb t1ctl
    M_FALL_IPL         94/96   hwr ipl noig,rb t1ctl
    M_LEN2_VECBASE     94/96   latch all w,rb t1ctl
    M_GROW_PSCALEADJ   95/96   rb t1ctl
    M_RDDECL_ALL       88/96   hrd genctl nod,hrd t2ctl nod,hrd t2icr nod,hrd sccerr nod,hrd scctx nod,wrd sccerr nod,rb t1ctl,hrd ipl nod
    M_FALL_TXCTL       94/96   rb t2ctl,rb t1ctl
    -- part 3b --              (BASE re-run after the rb t1ctl string fix; the T1 cell)
    BASE               96/96   -
    M_GROW_PSCALEADJ   96/96   -
    M_FALL_TXCTL       94/96   rb t2ctl,rb t1ctl
    -- part 3c --              (acc all rewritten as guest st.b; the grown guard re-measured)
    BASE               96/96   -
    M_GROW_PSCALEADJ   95/96   acc all
    -- part 4 --               (the pass-4 repair: 101 rows)
    BASE               101/101 -
    M_LEN8_VECBASE     100/101 latch all d
    M_LATCH_ASSIGN     100/101 latch aba
    M_LATCH_BIT0       100/101 latch same2
    M_GROW_IPL         99/101  acc all,acc ipl ro
    M_RET0_GENCTL      96/101  hwr genctl lv,rb genctl,rb vecbase,rb genctl lo,latch two

Earlier tables, unchanged and still in force (adding rows cannot un-kill a mutant): part 1
(nine mutants at 78 rows), part 2 (`M_IDATA_GENCTL' 80/82), the pass-2 builder's pass 3 (six
sweeps killed at 78), 3b (four fall-throughs = four x 78/78) and 3c (the same four killed
81/82 each at 82).  `M_ALIAS_SCCTX' was measured at 78 rows (the builder's M1, 77/78 by
`latch all' alone) and TRANSFERS because `latch all' is byte-identical across the instruments;
it was never re-run at 82 or 96 -- stated so the record does not overclaim.

## QUESTIONS

1. **VERIFY THE ENUMERATION** in the contract below (12 blocks x 9 shapes, the two T1 labels,
   the helper's TEST and SET lines, and the widths {1,2,4,8}).  Is the DOMAIN now the whole
   of what the fix introduced -- the twelve guards, the helper, and nothing else?  Walk the
   helper's two lines token by token and say which edits the five new rows catch, which are
   equivalent (the bit translation is disclosed as such), and which, if any, escape.  (a) Is the DOMAIN right -- are there guard inputs or plausible one-token shapes
   the nine do not cover?  (b) For each cell marked S (same channel as a measured shape), does
   the mutant really land the write, or die, exactly as the measured one does at THAT arm?
   (c) For each cell marked E or UNREACHABLE, is the warrant true?  (d) Is any C/W/A cell
   resting on a cardinality row that a benign session event could inflate or a mutant could
   preserve?  Say which cells you re-derived from the source rather than from this packet.
2. **THE SMALLEST EDIT THAT BREAKS THIS AND STILL PASSES 101 ROWS.**  Name the row you expect
   to stay green.  Shapes NOT in the contract are the interesting ones.
3. **OPTION-SET COMPLETENESS: N/A** -- no disposition is chosen; say so if you disagree.
4. **IS THE RECORD HONEST?**  The contract, the PRETABLE amendments and the diff are inlined.
   Name any sentence a measurement refutes, any count without a deriver, and any claim of
   coverage no row carries.  PRETABLE.out was restored to Sections 0-4 and its amendments moved
   to a second file because appending had destroyed its mtime discriminator: is the split
   honest as written?

If, while verifying a claim, you found something ELSE -- say so.

## THE CONTRACT (the probe's docstring, VERBATIM, as it now stands)

```
pcc2widthkills DETECTOR -- the twelve width-guard blocks in DEVICE_ACCESS(pcc2).

WHAT THE FIX DID.  Twelve `if (len != 1)' blocks -- TEN `fatal(); exit(1)' kills that ended the host on
a guest-chosen access width, and two #119 warn-once latches that refused it with a
process-global static.  The
tree's own header says PCC2 registers "can be accessed as bytes, two-bytes, or
four-bytes", so the width is LEGAL.  The fix is a DIRECTION SPLIT:

    READS   ACCEPT -- the memcpy above the switch already served them, raw bytes in
            address order, width-correct by construction.  The guard discarded a
            correct answer.
    WRITES  DECLINE + per-instance latched announce -- every write arm uses `idata',
            the big-endian-composed value, which is "the addressed byte" ONLY at
            len==1.  Deleting the guard would store the NEIGHBOUR's lane.

CONTRACT (vacuity-floor clause (e)) -- what this detector is designed to catch:

  CATCHES
    * reinstatement of the kill at any of the SIX GUEST-reachable blocks (survival
      rows paired with a liveness observable, because exit status cannot tell
      "declined and quit" from "died with status 0");
    * *** pass 2: the two FOLDED-IN arms, IPL and MASK, had NO ROW -- twelve blocks
      converted, ten given rows, and the shipped contract did not say so.  A seat
      found it by sibling parity: MASK is GENCTL's twin and had none of GENCTL's rows.
      Repaired: IPL is EVEN and therefore the SIXTH guest-reachable block (survival +
      message rows); MASK is odd (operator rows) and gets GENCTL's readback. ***
    * reinstatement at any of the six OPERATOR-only blocks (VECBASE, PSCALEADJ, SCCICR,
      SCCRX, SCSIICR, MASK; the T1CTL/T1ICR labels are odd too but share TxCTL/TxICR's
      blocks), through the debugger's `put h' at an odd address -- MEASURED to warn
      and store and kill
      (artifacts/pcc2widthkills/operator_reach_20260903.out);
    * *** DELETE instead of decline on the write side -- the lane hazard.  `st.h
      0xAABB' to GENCTL must leave GENCTL unchanged; a bare deletion stores 0xBB,
      VECBASE's lane, because (uint8_t) idata is the HIGHEST-address byte ***;
    * an accidental per-lane compose (GENCTL would read 0xAA);
    * the value a wide READ composes -- lane order and width -- not merely survival;
    * loss of the latch in either direction: dropped `|=' floods (same site twice
      must announce ONCE), and one bit shared across blocks silences (two sites must
      announce TWICE);
    * the de-escalation clause: at the five even blocks with `acc' rows a legal byte write
      lands and reads back through the arm's own mask with NO decline message; at all
      twelve, `acc all' pins NO decline and survival (a guard grown to refuse bytes); at
      the two print-only arms the body's own print is the proof (`acc pscale ign',
      `acc ipl ro').  SCCERR's byte side is value-identical (always 0) and is disclosed,
      not claimed.

  THE ENUMERATION (pass 3 class closure, pass 4 domain repair).  Twelve blocks x NINE
  clause-(d) shapes, the helper's own two operations, and four access widths.  Two
  consecutive passes found breaches of ONE class -- a block with no channel for the
  ANNOUNCE-THEN-FALL-THROUGH shape (guard kept, announce kept, `break' removed, the
  halfword LANDS) -- at MASK, then at four odd arms, then (pass 3, MEASURED 82/82 by a
  seat) at VECBASE, whose `rb vecbase' row is GENCTL's neighbour-lane check and never
  writes wide to VECBASE's own arm.  So the space is written down, cell by cell.
  M = measured kill (log named in CHANGELOG/PRETABLE); S = same channel as a measured
  shape at that arm (the mutant lands the write exactly as the measured one does);
  E = equivalent by construction, with its warrant.  Shapes: DEL guard deleted; LEN
  `len != 1' -> `len > 2' (halfword lands, word declined); LEN2 its MIRROR, `len != 1' ->
  `len == 2' (halfword declined, WORD lands -- named by the codex seat on pass 3); KILL
  verbatim exit(1) reinstated; ALIAS one enum member for two blocks; FALL announce-then-
  fall-through; SWAP guard operand `len' -> `idata > 0xff'; GROW the guard widened to
  decline the LEGAL byte width too (`len != 1' -> `len != 0'), the de-escalation clause.

      block      DEL   LEN   LEN2  KILL  ALIAS FALL  SWAP  GROW   FALL channel
      GENCTL     M     S     W     S     C     M     M     A/C    rb genctl (table 1 M_NOBREAK)
      VECBASE    S     S     W     M     C     M     C     C      rb vecbase own  (pass-3 repair)
      PSCALEADJ  S     S     W     S     C     M     C     C      op pscale noig  (message)
      TxCTL      S     M     W     S     C     M     C     A/C    rb t2ctl (FALL: part 3b, t2 and t1)
      TxICR      M     M     W     S     C     S     C     A/C    rb t2icr
      SCCERR     S     M     S     S     C     E     C     A/C    E: the arm stores 0 and nothing in
                                                                  the model ever stores a nonzero
                                                                  SCCERR (deriver: every writer of
                                                                  pcctwo_reg[], grep 'pcctwo_reg\[';
                                                                  the counter memcpy's 8-byte span
                                                                  is pcc2counter8, disclosed)
      SCCICR     S     S     W     S     C     M     C     C      rb sccicr
      SCCTX      M     M     W     S     C     S     C     A/C    rb scctx
      SCCRX      S     S     W     S     C     M     C     C      rb sccrx
      SCSIICR    S     S     W     S     C     M     C     C      rb scsiicr
      IPL        S     S     W     M     C     M     C     C      hwr ipl noig    (pass-3 repair:
                                                                  the write body prints once)
      MASK       M     M     W     M     C     M     C     C      rb mask
      C  = the cardinality row `latch all' (twelve wide writes, twelve announces): ALIAS,
           any collision drops the count; SWAP, its value 0x0003 fits a byte, so a
           value-test guard at ANY arm lets it land and drops the count.
      W  = `latch all w' (twelve WORD writes via put w, twelve announces): a `len == 2'
           guard at ANY arm lets the word land silently and drops the count.  SCCERR's
           own word rows (wrd/wwr sccerr) are its S.
      A/C = the arm's own `acc' row, AND `acc all' (twelve legal GUEST byte stores, ZERO
           declines): a guard grown to refuse bytes at ANY arm announces and reds it.
           Blocks marked C alone have no per-arm acc row; `acc all' is their channel.
           NOT the debugger's `put b': it calls memory_rw with NO_EXCEPTIONS, which does not
           dispatch to a DM_DEFAULT device, so a `put b' row could not see the grown guard
           (MEASURED: 95/96 in part 3 and 96/96 in part 3b, the mutation proven in the binary).  `put h/w/d' go
           through the store_Nbit_word helpers and do reach the arms.
      DEL/LEN/KILL cells marked S land the write, or die, exactly as the measured shape at
      that arm does, and the arm's own dcl / survival
      / readback rows are the channel.  KILL cells' channel is the survival PAIR (exit
      status plus the liveness observable), which varies under a reinstated kill by
      construction; the CHANNEL rule's 'survival-only' names a survival oracle at a
      REFUSAL-effect site, which a kill is not.  `d->warned' is a 32-bit field with twelve bits assigned.

      A NINTH SHAPE, on the input the six-shape list named and never walked: RDDECL, the
      direction split's own conjunct nulled, `writeflag == MEM_WRITE' -> `<= MEM_WRITE'
      (ONE character; MEM_READ is 0).  The Opus seat MEASURED it 82/82 on pass 3: wide
      READS were declined, announced as writes, skipped the arm's read body and consumed
      the block's latch bit -- and no session holding a wide read carried a decline-count
      row.  Closed by `hrd <block> nod' / `wrd sccerr nod' on the SEVEN wide-read sessions
      that already existed (six even blocks by ld.h, SCCERR by ld): a declined read is a
      DECL where zero is expected.  The six ODD blocks' read-side cells are UNREACHABLE by
      construction -- a guest wide read at an odd offset alignment-faults before memory_rw,
      and a debugger read does not dispatch to a DM_DEFAULT device -- and are disclosed,
      not rowed.  One cosmetic gap, disclosed: the seven `op * dcl' rows count the GENERIC
      decline text, and for FIVE arms (VECBASE, PSCALEADJ, SCCICR, SCCRX, SCSIICR) no other
      row pins the name string, so a change of the NAME alone there is invisible; the
      T1 labels share TxCTL/TxICR's fatal() with the named `rb t2ctl dcl' / `rb t2icr dcl'
      rows, and `latch all' pins cardinality.

      THE SHARED BLOCKS.  TxCTL serves T1CTL (0x17, odd) and T2CTL (0x16, even); TxICR
      serves T1ICR (0x1b) and T2ICR (0x1a).  The blocks' readbacks above are at the T2
      offsets; a seat noted that a fall-through reaching only the T1 labels (the block
      split in two) would leave `op t1ctl dcl' at 1 with nothing reading T1CTL back.  So
      the T1 labels carry their own operator-path readbacks, `rb t1ctl' and `rb t1icr'.
      THE THIRTEENTH ARM.  SCCRXIACK has NO width guard and never had one: its body
      ignores `idata' (it clears a bit in SCCRX and reasserts), so its effect is
      width-invariant by construction and it is not a member of the twelve.  It is named
      here so the census is not read as an omission.
      SESSIONS.  Every session() is a fresh pty.fork/execv of the emulator, so no latch
      state survives from one row to the next; `latch all' counts one process.
      THE HELPER'S OWN OPERATIONS (pass 4).  pcc2_width_decline() has two lines that
      every block depends on: the TEST `!(d->warned & (1u << bit))' and the SET
      `d->warned |= (1u << bit)'.  One-token edits to the SET line escaped every row:
      `|=' -> `=' (assign: A, B clears A -- `latch aba' A,B,A = 2) and `(1u << bit)' ->
      `1' (bit 0 always: every other block announces every time -- `latch same2', MASK
      twice = 1).  The TEST line's operand swap (`&' -> `==') is caught by `latch all':
      with the field accumulating, equality fails from the second block on and it
      announces 12 either way -- DISCLOSED as not distinguishable by this instrument.
      WIDTHS.  The debugger drives len 2 (`put h'), 4 (`put w') and 8 (`put d'); the
      guest drives 1, 2 and 4.  `latch all', `latch all w' and `latch all d' pin the
      refusal at every block for each non-byte width, so a guard true on a subset of
      {2,4,8} drops one of the three counts.
      BIT IDENTITY.  `latch all' and `latch all w' are cardinality rows: they assert
      twelve announces, never WHICH bit.  A translation of the bit index
      (`1u << bit' -> `1u << (bit + 1)') is EQUIVALENT by construction -- no code
      outside pcc2_width_decline() reads d->warned's bits -- and was MEASURED 96/96 by a
      pass-4 seat as the clause-(f) control.  That warrant expires the day anything
      indexes or reports those bits.
      ANNOUNCE SEVERITY.  Every row counts TEXT on a pty run under -V; `fatal(' ->
      `debug(' in the helper changes no text these rows read.  NOT CAUGHT, disclosed;
      the fork's recorded warrant for fatal() over debug() is dev_asc.c's (-q makes a
      debug()-level line invisible to the boot-log hygiene grep).
      THE FAULT MEMBER.  `break' -> `return 0' at a guard turns the decline into a bus
      error: the guest's store faults, the program never prints, and the block's `hwr'
      / `lv' pair reds.  Measured as M_RET0_GENCTL in part 4.
      INSTRUMENTS.  Parts 3, 3b and 3c ran three frozen copies (md5 3dcf73de, 280d9ab3,
      72759b4f); the last is the shipped probe.  3 -> 3b changed only `rb t1ctl' /
      `rb t1icr's expected string, 3b -> 3c only `acc all's session; row-name sets are
      identical and no killing row was touched, so the part-3 kills TRANSFER.  `acc all'
      was REWRITTEN, not added: its warrant is that the session is self-contained and
      part 3c measured the rewrite (95/96, `acc all' alone).

  DOES NOT CATCH, stated so an escape is outside the contract rather than an argument
    * per-instance vs process-global latch state: mvme187 instantiates ONE pcc2, so no
      session can hold two instances.  The bitfield is per-instance by construction;
      nothing here measures it;
    * pcc2c040kill -- a LEGAL byte write of 0x04 to GENCTL still ends the host in
      reassert_interrupts().  Every GENCTL lane value here keeps bit 0x04 CLEAR so no
      row dies for that reason;
    * pcc2defaultkill -- an unlisted offset (0x06, 0x14, 0x18, 0x2c ...) still ends the
      host in `default:';
    * pcc2counter8 -- the counter arm's raw memcpy of an 8-byte write;
    * what real hardware does with the LANES of a wide write (not on disk);
    * the SCCERR word-write's stored value: the arm always stores 0, so a decline and
      an accept are value-identical there and the row's channel is the message.

Sentinel: PCC2W_PROBE_DONE

```

## THE ENCLOSING CODE (the helper by brace count; the arms whose rows are new)

```c
static void pcc2_width_decline(struct pcc2_data *d, int bit, const char *name, int len)
{
	if (!(d->warned & (1u << bit))) {
		d->warned |= (1u << bit);
		fatal("[ pcc2: unimplemented len=%i write to %s -- declined."
		    "  (once) ]\n", len, name);
	}
}

	case PCCTWO_VECBASE:
		if (len != 1 && writeflag == MEM_WRITE) {
			pcc2_width_decline(d, PCC2_W_VECBASE_LEN, "PCCTWO_VECBASE", len);
			break;
		}
		if (writeflag == MEM_WRITE) {
			d->pcctwo_reg[relative_addr] = idata & 0xf0;
			if (idata & ~0xf0)
				fatal("[ pcc2: HUH? write to PCCTWO_VECBASE"
				    " with value 0x%02x. ]\n", (int) idata);
		}
		break;

	case PCCTWO_T1CMP:
	case PCCTWO_T2CMP:
	case PCCTWO_T1COUNT:
	case PCCTWO_T2COUNT:
		if (writeflag == MEM_WRITE &&
		    relative_addr + len <= PCC2_SIZE)	/* OB-11: end-span */
			memcpy(d->pcctwo_reg + relative_addr, data, len);
		break;

	case PCCTWO_IPL:
		/*  pcc2widthkills: was a #119 `static int w' -- process-global, and it
		    said "ignored" about a READ the memcpy above had already served.
		    Now per-instance, write-only, like the ten blocks above.  */
		if (len != 1 && writeflag == MEM_WRITE) {
			pcc2_width_decline(d, PCC2_W_IPL_LEN, "PCCTWO_IPL", len);
			break;
		}
		if (writeflag == MEM_WRITE) {
			static int w = 0;	/* #119: was exit(1) (IPL is read-only) */
			if (!w) { fatal("[ pcc2: write to read-only PCCTWO_IPL; "
			    "ignored ]\n"); w = 1; }
		} else {
			if (d->pcctwo_reg[PCCTWO_IPL] == 0) {
				static int w = 0;	/* #119: was exit(1) */
				if (!w) { fatal("[ pcc2: IPL == 0 on read ]\n");
				    w = 1; }
			}
		}
		break;

	case PCCTWO_MASK:
		/*  pcc2widthkills: was a #119 `static int w' -- process-global, and it
		    said "ignored" about a READ the memcpy above had already served.
		    Now per-instance, write-only, like the ten blocks above.  */
		if (len != 1 && writeflag == MEM_WRITE) {
			pcc2_width_decline(d, PCC2_W_MASK_LEN, "PCCTWO_MASK", len);
			break;
		}
		if (writeflag == MEM_WRITE) {
			d->pcctwo_reg[relative_addr] = idata;
			reassert_interrupts(d);
		}
		break;

	case PCCTWO_T2CTL:
	case PCCTWO_T1CTL:
		if (len != 1 && writeflag == MEM_WRITE) {
			pcc2_width_decline(d, PCC2_W_TXCTL_LEN, "PCCTWO_TxCTL", len);
			break;
		}
		if (writeflag == MEM_WRITE) {
			/*  PCC2_TCTL_CEN and PCC2_TCTL_COC:  */
			d->pcctwo_reg[relative_addr] &= 0xfc;
			d->pcctwo_reg[relative_addr] |= (idata & 3);

			if (idata & PCC2_TCTL_COVF)
				d->pcctwo_reg[relative_addr] &=
				    ~(PCC2_TCTL_OVF | PCC2_TCTL_COVF);

			if (idata & ~7)
				fatal("[ pcc2: HUH? write to PCCTWO_TxCTL"
				    " with value 0x%02x. ]\n", (int) idata);
		}
		break;

	case PCCTWO_T2ICR:
	case PCCTWO_T1ICR:
		if (len != 1 && writeflag == MEM_WRITE) {
			pcc2_width_decline(d, PCC2_W_TXICR_LEN, "PCCTWO_TxICR", len);
			break;
		}
		if (writeflag == MEM_WRITE) {
			d->pcctwo_reg[relative_addr] &= ~0x17;
			d->pcctwo_reg[relative_addr] |= (idata & 0x17);

			if (relative_addr == PCCTWO_T1ICR &&
			    !(idata & PCC2_TTIRQ_IEN))
				d->pending_timer1_interrupts = 0;
			if (relative_addr == PCCTWO_T2ICR &&
			    !(idata & PCC2_TTIRQ_IEN))
				d->pending_timer2_interrupts = 0;

			if (relative_addr == PCCTWO_T1ICR && (idata & PCC2_TTIRQ_ICLR)
			    && d->pcctwo_reg[relative_addr] & PCC2_TTIRQ_INT
			    && d->pending_timer1_interrupts > 0)
				d->pending_timer1_interrupts --;

			if (relative_addr == PCCTWO_T2ICR && (idata & PCC2_TTIRQ_ICLR)
			    && d->pcctwo_reg[relative_addr] & PCC2_TTIRQ_INT
			    && d->pending_timer2_interrupts > 0)
				d->pending_timer2_interrupts --;

			if (idata & PCC2_TTIRQ_ICLR)
				d->pcctwo_reg[relative_addr] &= ~PCC2_TTIRQ_INT;

			if (idata & 0xe0)
				fatal("[ pcc2: HUH? write to PCCTWO_TxICR"
				    " with value 0x%02x. ]\n", (int) idata);

			reassert_interrupts(d);
		}
		break;
```

## THE DETECTOR DIFF (`regress/pcc2_width_probe.py`, 60 -> 101 rows, INLINED IN FULL)

```diff
diff --git a/regress/pcc2_width_probe.py b/regress/pcc2_width_probe.py
index bed9732..ae091a8 100644
--- a/regress/pcc2_width_probe.py
+++ b/regress/pcc2_width_probe.py
@@ -1,8 +1,9 @@
 #!/usr/bin/env python3
 """pcc2widthkills DETECTOR -- the twelve width-guard blocks in DEVICE_ACCESS(pcc2).
 
-WHAT THE FIX DID.  Twelve `if (len != 1) { fatal(...); exit(1); }' blocks (ten kills and
-two #119 function-static latches) ended the host on a guest-chosen access width.  The
+WHAT THE FIX DID.  Twelve `if (len != 1)' blocks -- TEN `fatal(); exit(1)' kills that ended the host on
+a guest-chosen access width, and two #119 warn-once latches that refused it with a
+process-global static.  The
 tree's own header says PCC2 registers "can be accessed as bytes, two-bytes, or
 four-bytes", so the width is LEGAL.  The fix is a DIRECTION SPLIT:
 
@@ -16,11 +17,18 @@ four-bytes", so the width is LEGAL.  The fix is a DIRECTION SPLIT:
 CONTRACT (vacuity-floor clause (e)) -- what this detector is designed to catch:
 
   CATCHES
-    * reinstatement of the kill at any of the five GUEST-reachable blocks (survival
+    * reinstatement of the kill at any of the SIX GUEST-reachable blocks (survival
       rows paired with a liveness observable, because exit status cannot tell
       "declined and quit" from "died with status 0");
-    * reinstatement at any of the seven OPERATOR-reachable blocks, through the
-      debugger's `put h' at an odd address -- MEASURED to warn and store and kill
+    * *** pass 2: the two FOLDED-IN arms, IPL and MASK, had NO ROW -- twelve blocks
+      converted, ten given rows, and the shipped contract did not say so.  A seat
+      found it by sibling parity: MASK is GENCTL's twin and had none of GENCTL's rows.
+      Repaired: IPL is EVEN and therefore the SIXTH guest-reachable block (survival +
+      message rows); MASK is odd (operator rows) and gets GENCTL's readback. ***
+    * reinstatement at any of the six OPERATOR-only blocks (VECBASE, PSCALEADJ, SCCICR,
+      SCCRX, SCSIICR, MASK; the T1CTL/T1ICR labels are odd too but share TxCTL/TxICR's
+      blocks), through the debugger's `put h' at an odd address -- MEASURED to warn
+      and store and kill
       (artifacts/pcc2widthkills/operator_reach_20260903.out);
     * *** DELETE instead of decline on the write side -- the lane hazard.  `st.h
       0xAABB' to GENCTL must leave GENCTL unchanged; a bare deletion stores 0xBB,
@@ -30,8 +38,126 @@ CONTRACT (vacuity-floor clause (e)) -- what this detector is designed to catch:
     * loss of the latch in either direction: dropped `|=' floods (same site twice
       must announce ONCE), and one bit shared across blocks silences (two sites must
       announce TWICE);
-    * the de-escalation clause: byte writes at the LEGAL width at every reachable
-      arm still land, read back through each arm's own mask, with NO decline message.
+    * the de-escalation clause: at the five even blocks with `acc' rows a legal byte write
+      lands and reads back through the arm's own mask with NO decline message; at all
+      twelve, `acc all' pins NO decline and survival (a guard grown to refuse bytes); at
+      the two print-only arms the body's own print is the proof (`acc pscale ign',
+      `acc ipl ro').  SCCERR's byte side is value-identical (always 0) and is disclosed,
+      not claimed.
+
+  THE ENUMERATION (pass 3 class closure, pass 4 domain repair).  Twelve blocks x NINE
+  clause-(d) shapes, the helper's own two operations, and four access widths.  Two
+  consecutive passes found breaches of ONE class -- a block with no channel for the
+  ANNOUNCE-THEN-FALL-THROUGH shape (guard kept, announce kept, `break' removed, the
+  halfword LANDS) -- at MASK, then at four odd arms, then (pass 3, MEASURED 82/82 by a
+  seat) at VECBASE, whose `rb vecbase' row is GENCTL's neighbour-lane check and never
+  writes wide to VECBASE's own arm.  So the space is written down, cell by cell.
+  M = measured kill (log named in CHANGELOG/PRETABLE); S = same channel as a measured
+  shape at that arm (the mutant lands the write exactly as the measured one does);
+  E = equivalent by construction, with its warrant.  Shapes: DEL guard deleted; LEN
+  `len != 1' -> `len > 2' (halfword lands, word declined); LEN2 its MIRROR, `len != 1' ->
+  `len == 2' (halfword declined, WORD lands -- named by the codex seat on pass 3); KILL
+  verbatim exit(1) reinstated; ALIAS one enum member for two blocks; FALL announce-then-
+  fall-through; SWAP guard operand `len' -> `idata > 0xff'; GROW the guard widened to
+  decline the LEGAL byte width too (`len != 1' -> `len != 0'), the de-escalation clause.
+
+      block      DEL   LEN   LEN2  KILL  ALIAS FALL  SWAP  GROW   FALL channel
+      GENCTL     M     S     W     S     C     M     M     A/C    rb genctl (table 1 M_NOBREAK)
+      VECBASE    S     S     W     M     C     M     C     C      rb vecbase own  (pass-3 repair)
+      PSCALEADJ  S     S     W     S     C     M     C     C      op pscale noig  (message)
+      TxCTL      S     M     W     S     C     M     C     A/C    rb t2ctl (FALL: part 3b, t2 and t1)
+      TxICR      M     M     W     S     C     S     C     A/C    rb t2icr
+      SCCERR     S     M     S     S     C     E     C     A/C    E: the arm stores 0 and nothing in
+                                                                  the model ever stores a nonzero
+                                                                  SCCERR (deriver: every writer of
+                                                                  pcctwo_reg[], grep 'pcctwo_reg\[';
+                                                                  the counter memcpy's 8-byte span
+                                                                  is pcc2counter8, disclosed)
+      SCCICR     S     S     W     S     C     M     C     C      rb sccicr
+      SCCTX      M     M     W     S     C     S     C     A/C    rb scctx
+      SCCRX      S     S     W     S     C     M     C     C      rb sccrx
+      SCSIICR    S     S     W     S     C     M     C     C      rb scsiicr
+      IPL        S     S     W     M     C     M     C     C      hwr ipl noig    (pass-3 repair:
+                                                                  the write body prints once)
+      MASK       M     M     W     M     C     M     C     C      rb mask
+      C  = the cardinality row `latch all' (twelve wide writes, twelve announces): ALIAS,
+           any collision drops the count; SWAP, its value 0x0003 fits a byte, so a
+           value-test guard at ANY arm lets it land and drops the count.
+      W  = `latch all w' (twelve WORD writes via put w, twelve announces): a `len == 2'
+           guard at ANY arm lets the word land silently and drops the count.  SCCERR's
+           own word rows (wrd/wwr sccerr) are its S.
+      A/C = the arm's own `acc' row, AND `acc all' (twelve legal GUEST byte stores, ZERO
+           declines): a guard grown to refuse bytes at ANY arm announces and reds it.
+           Blocks marked C alone have no per-arm acc row; `acc all' is their channel.
+           NOT the debugger's `put b': it calls memory_rw with NO_EXCEPTIONS, which does not
+           dispatch to a DM_DEFAULT device, so a `put b' row could not see the grown guard
+           (MEASURED: 95/96 in part 3 and 96/96 in part 3b, the mutation proven in the binary).  `put h/w/d' go
+           through the store_Nbit_word helpers and do reach the arms.
+      DEL/LEN/KILL cells marked S land the write, or die, exactly as the measured shape at
+      that arm does, and the arm's own dcl / survival
+      / readback rows are the channel.  KILL cells' channel is the survival PAIR (exit
+      status plus the liveness observable), which varies under a reinstated kill by
+      construction; the CHANNEL rule's 'survival-only' names a survival oracle at a
+      REFUSAL-effect site, which a kill is not.  `d->warned' is a 32-bit field with twelve bits assigned.
+
+      A NINTH SHAPE, on the input the six-shape list named and never walked: RDDECL, the
+      direction split's own conjunct nulled, `writeflag == MEM_WRITE' -> `<= MEM_WRITE'
+      (ONE character; MEM_READ is 0).  The Opus seat MEASURED it 82/82 on pass 3: wide
+      READS were declined, announced as writes, skipped the arm's read body and consumed
+      the block's latch bit -- and no session holding a wide read carried a decline-count
+      row.  Closed by `hrd <block> nod' / `wrd sccerr nod' on the SEVEN wide-read sessions
+      that already existed (six even blocks by ld.h, SCCERR by ld): a declined read is a
+      DECL where zero is expected.  The six ODD blocks' read-side cells are UNREACHABLE by
+      construction -- a guest wide read at an odd offset alignment-faults before memory_rw,
+      and a debugger read does not dispatch to a DM_DEFAULT device -- and are disclosed,
+      not rowed.  One cosmetic gap, disclosed: the seven `op * dcl' rows count the GENERIC
+      decline text, and for FIVE arms (VECBASE, PSCALEADJ, SCCICR, SCCRX, SCSIICR) no other
+      row pins the name string, so a change of the NAME alone there is invisible; the
+      T1 labels share TxCTL/TxICR's fatal() with the named `rb t2ctl dcl' / `rb t2icr dcl'
+      rows, and `latch all' pins cardinality.
+
+      THE SHARED BLOCKS.  TxCTL serves T1CTL (0x17, odd) and T2CTL (0x16, even); TxICR
+      serves T1ICR (0x1b) and T2ICR (0x1a).  The blocks' readbacks above are at the T2
+      offsets; a seat noted that a fall-through reaching only the T1 labels (the block
+      split in two) would leave `op t1ctl dcl' at 1 with nothing reading T1CTL back.  So
+      the T1 labels carry their own operator-path readbacks, `rb t1ctl' and `rb t1icr'.
+      THE THIRTEENTH ARM.  SCCRXIACK has NO width guard and never had one: its body
+      ignores `idata' (it clears a bit in SCCRX and reasserts), so its effect is
+      width-invariant by construction and it is not a member of the twelve.  It is named
+      here so the census is not read as an omission.
+      SESSIONS.  Every session() is a fresh pty.fork/execv of the emulator, so no latch
+      state survives from one row to the next; `latch all' counts one process.
+      THE HELPER'S OWN OPERATIONS (pass 4).  pcc2_width_decline() has two lines that
+      every block depends on: the TEST `!(d->warned & (1u << bit))' and the SET
+      `d->warned |= (1u << bit)'.  One-token edits to the SET line escaped every row:
+      `|=' -> `=' (assign: A, B clears A -- `latch aba' A,B,A = 2) and `(1u << bit)' ->
+      `1' (bit 0 always: every other block announces every time -- `latch same2', MASK
+      twice = 1).  The TEST line's operand swap (`&' -> `==') is caught by `latch all':
+      with the field accumulating, equality fails from the second block on and it
+      announces 12 either way -- DISCLOSED as not distinguishable by this instrument.
+      WIDTHS.  The debugger drives len 2 (`put h'), 4 (`put w') and 8 (`put d'); the
+      guest drives 1, 2 and 4.  `latch all', `latch all w' and `latch all d' pin the
+      refusal at every block for each non-byte width, so a guard true on a subset of
+      {2,4,8} drops one of the three counts.
+      BIT IDENTITY.  `latch all' and `latch all w' are cardinality rows: they assert
+      twelve announces, never WHICH bit.  A translation of the bit index
+      (`1u << bit' -> `1u << (bit + 1)') is EQUIVALENT by construction -- no code
+      outside pcc2_width_decline() reads d->warned's bits -- and was MEASURED 96/96 by a
+      pass-4 seat as the clause-(f) control.  That warrant expires the day anything
+      indexes or reports those bits.
+      ANNOUNCE SEVERITY.  Every row counts TEXT on a pty run under -V; `fatal(' ->
+      `debug(' in the helper changes no text these rows read.  NOT CAUGHT, disclosed;
+      the fork's recorded warrant for fatal() over debug() is dev_asc.c's (-q makes a
+      debug()-level line invisible to the boot-log hygiene grep).
+      THE FAULT MEMBER.  `break' -> `return 0' at a guard turns the decline into a bus
+      error: the guest's store faults, the program never prints, and the block's `hwr'
+      / `lv' pair reds.  Measured as M_RET0_GENCTL in part 4.
+      INSTRUMENTS.  Parts 3, 3b and 3c ran three frozen copies (md5 3dcf73de, 280d9ab3,
+      72759b4f); the last is the shipped probe.  3 -> 3b changed only `rb t1ctl' /
+      `rb t1icr's expected string, 3b -> 3c only `acc all's session; row-name sets are
+      identical and no killing row was touched, so the part-3 kills TRANSFER.  `acc all'
+      was REWRITTEN, not added: its warrant is that the session is self-contained and
+      part 3c measured the rewrite (95/96, `acc all' alone).
 
   DOES NOT CATCH, stated so an escape is outside the contract rather than an argument
     * per-instance vs process-global latch state: mvme187 instantiates ONE pcc2, so no
@@ -61,9 +187,17 @@ open(DUMMY, "wb").write(b"\x00\x00\x00\x00")
 CODE = 0x00010000
 SCRATCH = 0x00020000
 PCC2 = 0xfff42000
-#  the five GUEST-reachable blocks (even offsets) and the seven OPERATOR-reachable ones
+#  the SIX GUEST-reachable blocks (even offsets; IPL below is the sixth) and the six
+#  OPERATOR-only ones (odd offsets; T1CTL/T1ICR are odd labels of the shared TxCTL/TxICR
+#  blocks).  An earlier comment here said five and seven: a units slip, blocks vs labels.
 GENCTL, T2CTL, T2ICR, SCCERR, SCCTX = 0x02, 0x16, 0x1a, 0x1c, 0x1e
 VECBASE, PSCALEADJ, T1CTL, T1ICR, SCCICR, SCCRX, SCSIICR = 0x03, 0x15, 0x17, 0x1b, 0x1d, 0x1f, 0x2f
+#  pcc2 pass 2: THE TWO FOLDED-IN ARMS HAD NO ROW AT ALL.  A seat found that the probe
+#  touched no offset at 0x3e or 0x3f -- twelve blocks converted, ten given rows.  MASK
+#  is GENCTL's byte-identical twin (store byte, reassert); GENCTL's null-repair was
+#  caught by `rb genctl', MASK's by nothing, a 60/60 sweep.  AND IPL IS EVEN: it is the
+#  SIXTH guest-reachable block, not a seventh operator one.
+IPL, MASK = 0x3e, 0x3f
 CHIPID = 0x00
 
 
@@ -164,6 +298,9 @@ def printed(t, reg):
 
 
 def program(insns, at=CODE):
+    #  `at' lets a session run TWO programs: a second sequence at the SAME address finds
+    #  pc already there and the assignment is skipped (the Addr hazard, designed out in
+    #  the sgi probes with Addr.take()).  Callers needing two pass at=CODE + 0x100.
     words = list(insns) + [I_BR_SELF, 0]
     cmds = ["put w 0x%x, 0x%08x" % (at + 4 * i, w) for i, w in enumerate(words)]
     return cmds + ["pc=0x%x" % at, "step %d" % len(insns)]
@@ -194,6 +331,8 @@ for nm, off in (("genctl", GENCTL), ("t2ctl", T2CTL), ("t2icr", T2ICR),
     t, alive, how = session(setup() + program([I_ST_SCR, LD_H(4, off), I_LD_SCR]) + ["print r4"])
     row("hrd " + nm, how, "exit0", "ld.h %s (aligned halfword READ) survives" % nm.upper())
     row("hrd %s lv" % nm, printed(t, "r4") if alive else "died", "0x5a5a5a5a", "...and runs on")
+    row("hrd %s nod" % nm, t.count(DECL), 0,
+        "...and a wide READ is never declined (the direction split's own conjunct)")
     #  r6 = the halfword to store: both lanes keep GENCTL's bit 0x04 CLEAR (pcc2c040kill)
     t, alive, how = session(setup(r6="0xaabb") + program([I_ST_SCR, ST_H(6, off), I_LD_SCR]) + ["print r4"])
     row("hwr " + nm, how, "exit0", "st.h %s (aligned halfword WRITE) survives" % nm.upper())
@@ -202,6 +341,7 @@ for nm, off in (("genctl", GENCTL), ("t2ctl", T2CTL), ("t2icr", T2ICR),
 t, alive, how = session(setup() + program([I_ST_SCR, LD_W(4, SCCERR), I_LD_SCR]) + ["print r4"])
 row("wrd sccerr", how, "exit0", "ld SCCERR (the one 4-aligned block) survives")
 row("wrd sccerr lv", printed(t, "r4") if alive else "died", "0x5a5a5a5a", "...and runs on")
+row("wrd sccerr nod", t.count(DECL), 0, "...and the word READ is never declined")
 t, alive, how = session(setup(r6="0x00000000") + program([I_ST_SCR, ST_W(6, SCCERR), I_LD_SCR]) + ["print r4"])
 row("wwr sccerr", how, "exit0", "st SCCERR (word WRITE) survives")
 row("wwr sccerr lv", printed(t, "r4") if alive else "died", "0x5a5a5a5a", "...and runs on")
@@ -239,6 +379,56 @@ t, alive, how = session(setup(r5="0x50", r6="0xaabb")
 row("rb vecbase", printed(t, "r4") if alive else "died", "0x50",
     "VECBASE unchanged too -- the second lane of the declined halfword")
 
+# ---------------------------- per-arm channels (pass 2: sibling parity, arm by arm)
+#  A seat pointed out that only GENCTL had a readback: every other reachable arm's
+#  halfword-write row checked SURVIVAL alone, so a guard edited at ONE arm (`len > 2',
+#  or the guard deleted, at T2ICR only) left every row green.  Each arm now has its own
+#  channel, with a lane value its own mask turns into a different byte when it lands.
+for nm, off, pre, landed in (("t2ctl", T2CTL, "0x03", "0x3"), ("t2icr", T2ICR, "0x13", "0x13"),
+                             ("scctx", SCCTX, "0x1f", "0x1f")):
+    t, alive, how = session(setup(r5=pre, r6="0xaab8")
+                            + program([ST_B(5, off), ST_H(6, off), LD_BU(4, off)]) + ["print r4"])
+    row("rb " + nm, printed(t, "r4") if alive else "died", landed,
+        "%s unchanged after a declined st.h -- kills a guard edited at THIS arm" % nm.upper())
+    row("rb %s dcl" % nm, t.count("write to PCCTWO_%s " % ("TxCTL" if nm == "t2ctl" else "TxICR" if nm == "t2icr" else "SCCTX") + DECL), 1,
+        "...announced once at this arm")
+t, alive, how = session(setup(r6="0xaab8") + program([ST_H(6, SCCERR)]))
+row("hwr sccerr dcl", t.count("write to PCCTWO_SCCERR " + DECL), 1,
+    "halfword write to SCCERR declined once -- value-identical arm, message channel")
+
+#  PRE-TABLE BLOCK yield (section 1, guard field vs body field): the guard reads the access
+#  SHAPE (len) and the guarded body reads the VALUE (idata).  An operand swap to a value
+#  test -- `idata > 0xff', a plausible "does it fit a byte" reading -- accepts a halfword
+#  write whose value fits, and big-endian 0x0022 then stores 0x22, the NEIGHBOUR's lane,
+#  into GENCTL: the original defect, behind a guard that still reads like a width check.
+#  Every other wide-write row used a value above 0xff, so all 77 were green under it BY
+#  CONSTRUCTION.  Written before the repair table ran; the table says whether it kills.
+t, alive, how = session(setup(r5="0x11", r6="0x0022")
+                        + program([ST_B(5, GENCTL), ST_H(6, GENCTL), LD_BU(4, GENCTL)]) + ["print r4"])
+row("rb genctl lo", printed(t, "r4") if alive else "died", "0x11",
+    "st.h of a value that FITS a byte is still declined -- the guard is on len, not idata")
+
+# ------------------------- latch CARDINALITY (pass 2, the measuring seat's class closer)
+#  `latch same' and `latch two' pin ONE pair out of 66: every other session writes at most
+#  one BLOCK, so a bit shared by any other pair announces normally and no row moves.
+#  MEASURED by the builder: aliasing SCCTX onto SCCRX's bit -- a ONE-CHARACTER edit --
+#  left the 60-row detector at 60/60.  ONE OFFSET PER BLOCK: TxCTL serves T1CTL+T2CTL
+#  and TxICR serves T1ICR+T2ICR, so twelve LABELS would give only ten announces -- the
+#  same units slip that let "five even blocks + seven odd ones = twelve" read as all
+#  twelve blocks.  This row pins the CARDINALITY of the latch: any collision anywhere in
+#  the 12-bit space drops the count.  (Operator path for all twelve, so the odd ones are
+#  reachable; the guest-reachable halves have their own rows above.)
+BLOCKS12 = (("GENCTL", 0x02), ("VECBASE", 0x03), ("PSCALEADJ", 0x15), ("TxCTL", 0x16),
+            ("TxICR", 0x1a), ("SCCERR", 0x1c), ("SCCICR", 0x1d), ("SCCTX", 0x1e),
+            ("SCCRX", 0x1f), ("SCSIICR", 0x2f), ("IPL", 0x3e), ("MASK", 0x3f))
+#  VALUE 0x0003, not 0x0303: it fits a byte, so this row ALSO reds if any arm swaps its
+#  guard operand from len to a value test (see `rb genctl lo').  On the fix the value
+#  never lands, so the expectation is value-independent.
+t, alive, how = session(["put h 0x%x, 0x0003" % (PCC2 + o) for _, o in BLOCKS12])
+row("latch all", t.count(DECL), 12,
+    "one wide write per BLOCK -> TWELVE announces: bit CARDINALITY, not one pair")
+row("latch all lv", how, "exit0", "...and the host survived all twelve blocks")
+
 # ------------------------------------------------------------------ latch rows
 t, alive, how = session(setup(r6="0xaabb") + program([ST_H(6, GENCTL), ST_H(6, GENCTL)]))
 row("latch same", t.count("write to PCCTWO_GENCTL " + DECL), 1,
@@ -246,6 +436,20 @@ row("latch same", t.count("write to PCCTWO_GENCTL " + DECL), 1,
 t, alive, how = session(setup(r6="0x0303") + program([ST_H(6, GENCTL), ST_H(6, T2CTL)]))
 row("latch two", t.count(DECL), 2,
     "two blocks -> TWO announces -- kills a bit shared across blocks")
+#  PASS 4 (glm, kimi, codex): `latch same' sees only CONSECUTIVE repeats, so `|=' -> `=' in the
+#  helper -- the field ASSIGNED instead of accumulated, one character -- passed every row: A
+#  then B clears A's bit, and nothing wrote A again afterwards.  Interleave: A, B, A -> TWO.
+t, alive, how = session(setup(r6="0x0303") + program([ST_H(6, GENCTL)])
+                        + ["put h 0x%x, 0x0303" % (PCC2 + VECBASE)]
+                        + program([ST_H(6, GENCTL)], at=CODE + 0x100))
+row("latch aba", t.count(DECL), 2,
+    "A, B, A -> TWO announces: the latch ACCUMULATES (an assignment would give three)")
+#  PASS 4 (minimax): `(1u << bit)' -> `1' in the SET line latches bit 0 for every block, so
+#  every block but GENCTL announces on every write.  `latch same' is at GENCTL (bit 0) and
+#  stays green.  The same test at a non-zero bit:
+t, alive, how = session(["put h 0x%x, 0x0303" % (PCC2 + MASK)] * 2)
+row("latch same2", t.count("write to PCCTWO_MASK " + DECL), 1,
+    "MASK (bit 11) twice -> ONE announce: the SET line names the block's own bit")
 
 # --------------------------------------------- de-escalation ACCEPT rows (byte writes)
 #  Removing twelve exit(1)s destroys the tripwire that announced guard growth.  So the
@@ -270,6 +474,121 @@ for nm, off in (("vecbase", VECBASE), ("pscale", PSCALEADJ), ("t1ctl", T1CTL),
     row("op " + nm, how, "exit0", "debugger put h at odd %s survives" % nm.upper())
     row("op %s dcl" % nm, t.count(DECL), 1, "...and was declined once")
 
+#  --------- the odd arms' FALL-THROUGH channel (pass 3, ruled a floor breach, not a disclosure)
+#  The block above proves each odd arm ANNOUNCES; it cannot see a guard that announces AND
+#  then lets the halfword land (the M_FALL shape -- decline nulled, guard kept: clause (d)).
+#  PRETABLE Section 2 had disclosed that as "a sentence owed".  The measuring seat asked
+#  whether a disclosure can discharge a floor clause; it cannot, or every breach becomes a
+#  sentence.  So each of the four arms gets the channel its body offers:
+#    SCCICR/SCCRX/SCSIICR store `idata & mask' then reassert_interrupts(): set 0x1f by
+#      byte (legal under both masks), decline a wide 0xaab8, read the byte back -- a landed
+#      write leaves 0x18 (& 0x1f) or 0x98 (& 0xdf) in an INTERRUPT CONTROL register.
+#    PSCALEADJ stores nothing; its write body only prints "ignored (value ...)".  A landed
+#      wide write therefore prints that line -- the message is the only channel, and the
+#      row counts it at ZERO.
+for nm, off in (("sccicr", SCCICR), ("sccrx", SCCRX), ("scsiicr", SCSIICR)):
+    t, alive, how = session(setup(r5="0x1f") + program([ST_B(5, off)])
+                            + ["put h 0x%x, 0xaab8" % (PCC2 + off)]
+                            + program([LD_BU(4, off)], at=CODE + 0x100) + ["print r4"])
+    row("rb " + nm, printed(t, "r4") if alive else "died", "0x1f",
+        "%s unchanged after a declined put h -- a fall-through lands 0x18/0x98 and reasserts" % nm.upper())
+t, alive, how = session(["put h 0x%x, 0x0303" % (PCC2 + PSCALEADJ)])
+row("op pscale noig", t.count("PSCALEADJ ignored"), 0,
+    "a declined wide write never reaches the 'ignored' print -- fall-through would")
+
+#  PASS 3 (class closure).  `rb vecbase' above writes wide to GENCTL and reads VECBASE: it
+#  is GENCTL's neighbour-lane check and never exercises VECBASE's own guard.  A seat
+#  MEASURED announce-then-fall-through at VECBASE as 82/82 -- the halfword landed (& 0xf0)
+#  while `op vecbase dcl' and `latch all' stayed green by construction.  VECBASE is the
+#  interrupt vector base, so the landed lane mis-delivers every vector.  Its own readback:
+t, alive, how = session(setup(r5="0x50") + program([ST_B(5, VECBASE)])
+                        + ["put h 0x%x, 0xaab8" % (PCC2 + VECBASE)]
+                        + program([LD_BU(4, VECBASE)], at=CODE + 0x100) + ["print r4"])
+row("rb vecbase own", printed(t, "r4") if alive else "died", "0x50",
+    "VECBASE unchanged after a declined put h to ITS OWN arm -- a fall-through lands 0xb0")
+#  IPL's write body stores nothing and prints "write to read-only PCCTWO_IPL; ignored"
+#  once per process (#119 static).  A declined wide write never reaches it; a fall-through
+#  prints it -- PSCALEADJ's shape at the twelfth block.  The message is the channel.
+t, alive, how = session(setup(r6="0x0303") + program([ST_H(6, IPL)]))
+row("hwr ipl noig", t.count("write to read-only PCCTWO_IPL"), 0,
+    "a declined st.h to IPL never reaches the read-only print -- fall-through would")
+#  The codex seat, pass 3: the MIRROR of the measured width edit.  `len != 1' -> `len == 2'
+#  declines every halfword row here and lets a WORD write land -- every row above stayed
+#  green under it.  One cardinality row over WORD writes closes that at all twelve blocks.
+#  (Word writes to the counter arms are pcc2counter8's business and are not touched.)
+t, alive, how = session(["put w 0x%x, 0x00000003" % (PCC2 + o) for _, o in BLOCKS12])
+row("latch all w", t.count(DECL), 12,
+    "one WORD write per BLOCK -> TWELVE announces: a `len == 2' guard anywhere drops it")
+#  PASS 4 (glm, deepseek, codex): the rows drove widths {1,2,4} and the contract itself says
+#  `put d' reaches with len 8, so a guard true on {2,4} and false on 8 (`len & 6', or
+#  `len != 1 && len != 8') passed every row.  Twelve DWORD writes, twelve announces:
+t, alive, how = session(["put d 0x%x, 0x0000000000000003" % (PCC2 + o) for _, o in BLOCKS12])
+row("latch all d", t.count(DECL), 12,
+    "one DWORD write per BLOCK -> TWELVE announces: an 8-byte exemption anywhere drops it")
+#  And the de-escalation side, closed at all twelve: one LEGAL byte write per block must
+#  announce NOTHING.  A guard grown to refuse bytes (`len != 1' -> `len != 0') at any of
+#  the seven blocks without a per-arm `acc' row is visible only here.  Values: GENCTL keeps
+#  bit 0x04 clear (pcc2c040kill); VECBASE's mask is 0xf0; the rest accept any byte.
+#  *** MEASURED, part 3 and 3b: this row's first form used the debugger's `put b' and could
+#  NOT SEE a guard grown to refuse bytes at PSCALEADJ -- 96/96 with the mutation PROVEN in the
+#  source and the binary newer than it.  `put b' calls memory_rw directly with NO_EXCEPTIONS,
+#  and that flag does not dispatch to a DM_DEFAULT device; `put h/w/d' go through the
+#  store_Nbit_word helpers and do reach the arms.  So the operator path for BYTES is not a
+#  path at all, and the row was vacuous by construction -- the CHANNEL rule's own failure,
+#  caught by the table.  Guest `st.b' is legal at every offset (byte accesses skip the m88k
+#  alignment check; `rb mask' stores a byte at 0x3f this way), so the accept side is pinned
+#  from the GUEST at all twelve blocks, which is the stronger form anyway. ***
+t, alive, how = session(setup(r5="0x10") + program([ST_B(5, o) for _, o in BLOCKS12]))
+row("acc all", t.count(DECL), 0,
+    "twelve legal guest byte stores, ZERO declines -- the accept side at every block")
+row("acc all lv", how, "exit0", "...and the host survived all twelve byte stores")
+#  PASS 4 (codex): `acc all' proves no DECLINE and survival; it does not prove the byte
+#  reached the arm's BODY.  For the two print-only arms the body's own print is the proof:
+t, alive, how = session(setup(r5="0x10") + program([ST_B(5, PSCALEADJ)]))
+row("acc pscale ign", t.count("PSCALEADJ ignored"), 1,
+    "a legal byte write to PSCALEADJ reaches its body -- the ignored print fires once")
+t, alive, how = session(setup(r5="0x10") + program([ST_B(5, IPL)]))
+row("acc ipl ro", t.count("write to read-only PCCTWO_IPL"), 1,
+    "a legal byte write to IPL reaches its body -- the read-only print fires once")
+#  The T1 labels of the two SHARED blocks (deepseek, pass 3): their readbacks above are at
+#  the T2 offsets, so a fall-through reaching only the T1 half of a split block would leave
+#  `op t1ctl dcl' at 1 with nothing reading T1CTL back.  Operator path, own readbacks:
+#  (`want' is the value as the debugger PRINTS it -- 0x03 comes back as `0x3'.  The first
+#  part-3 BASE run reddened this row on the fix for exactly that string mismatch, 95/96;
+#  the value was right.  Re-measured in part 3b.)
+for nm, off, pre, want in (("t1ctl", T1CTL, "0x03", "0x3"), ("t1icr", T1ICR, "0x13", "0x13")):
+    t, alive, how = session(setup(r5=pre) + program([ST_B(5, off)])
+                            + ["put h 0x%x, 0xaab8" % (PCC2 + off)]
+                            + program([LD_BU(4, off)], at=CODE + 0x100) + ["print r4"])
+    row("rb " + nm, printed(t, "r4") if alive else "died", want,
+        "%s unchanged after a declined put h at the T1 label -- a fall-through lands 0xb8 & mask (RMW at TxCTL: 0)" % nm.upper())
+
+# --------------------------------- IPL (guest-reachable, EVEN) and MASK (operator, odd)
+#  IPL 0x3e: a halfword at 0x3e lands in the IPL arm.  Its write side is read-only (#119
+#  "ignored"), so a wide write is declined by the WIDTH latch first and a readback cannot
+#  tell the two refusals apart -- the channel is the message.
+t, alive, how = session(setup() + program([I_ST_SCR, LD_H(4, IPL), I_LD_SCR]) + ["print r4"])
+row("hrd ipl", how, "exit0", "ld.h IPL (EVEN, the SIXTH guest-reachable block) survives")
+row("hrd ipl lv", printed(t, "r4") if alive else "died", "0x5a5a5a5a", "...and runs on")
+row("hrd ipl nod", t.count(DECL), 0, "...and the wide READ of IPL is never declined")
+t, alive, how = session(setup(r6="0x1234") + program([I_ST_SCR, ST_H(6, IPL), I_LD_SCR]) + ["print r4"])
+row("hwr ipl", how, "exit0", "st.h IPL survives")
+row("hwr ipl lv", printed(t, "r4") if alive else "died", "0x5a5a5a5a", "...and runs on")
+row("hwr ipl dcl", t.count("write to PCCTWO_IPL " + DECL), 1,
+    "...declined by the WIDTH latch (not the read-only one) -- the message is the channel")
+#  MASK 0x3f: odd, operator path.  It is GENCTL's twin, so it gets GENCTL's readback: set
+#  MASK to a known byte at the legal width, decline a wide write through the debugger,
+#  then read the byte back through a program at a SECOND address.  A deleted guard stores
+#  the wrong lane (0xbb); an accidental compose stores 0xaa.  reassert_interrupts on a
+#  MASK byte write is harmless here: GENCTL's C040 bit is clear and nothing is pending.
+t, alive, how = session(setup(r5="0x12") + program([ST_B(5, MASK)])
+                        + ["put h 0x%x, 0xaabb" % (PCC2 + MASK)]
+                        + program([LD_BU(4, MASK)], at=CODE + 0x100) + ["print r4"])
+row("op mask", how, "exit0", "debugger put h at odd MASK survives")
+row("op mask dcl", t.count("write to PCCTWO_MASK " + DECL), 1, "...and was declined once")
+row("rb mask", printed(t, "r4") if alive else "died", "0x12",
+    "MASK unchanged after the declined wide write -- GENCTL's twin gets GENCTL's readback")
+
 # ---------------------------------------------------------------------- summary
 print("NOROW  two device instances               -- mvme187 has ONE pcc2; per-instance latch state"
       " is by construction, not measured")

```

## THE GATE DIFF (INLINED IN FULL)

```diff
diff --git a/regress/gate_arm.sh b/regress/gate_arm.sh
index a8359d0..fbb6f5f 100644
--- a/regress/gate_arm.sh
+++ b/regress/gate_arm.sh
@@ -1292,13 +1292,13 @@ if ! grep -q "PCC2W_PROBE_DONE" "$PCC2LOG"; then
     check "pcc2 width probe completed" "no" "yes"
 else
     check "pcc2 width probe completed" "yes" "yes"
-    for v in "live" "devsig" "byte rd" "byte rd liv" "hrd genctl" "hrd genctl lv" "hwr genctl" "hwr genctl lv" "hrd t2ctl" "hrd t2ctl lv" "hwr t2ctl" "hwr t2ctl lv" "hrd t2icr" "hrd t2icr lv" "hwr t2icr" "hwr t2icr lv" "hrd sccerr" "hrd sccerr lv" "hwr sccerr" "hwr sccerr lv" "hrd scctx" "hrd scctx lv" "hwr scctx" "hwr scctx lv" "wrd sccerr" "wrd sccerr lv" "wwr sccerr" "wwr sccerr lv" "wwr sccerr dcl" "val h genctl" "val w sccerr" "rb genctl" "rb genctl dcl" "rb vecbase" "latch same" "latch two" "acc genctl" "acc genctl nod" "acc t2ctl" "acc t2ctl nod" "acc t2icr" "acc t2icr nod" "acc scctx" "acc scctx nod" "acc sccerr" "acc sccerr nod" "op vecbase" "op vecbase dcl" "op pscale" "op pscale dcl" "op t1ctl" "op t1ctl dcl" "op t1icr" "op t1icr dcl" "op sccicr" "op sccicr dcl" "op sccrx" "op sccrx dcl" "op scsiicr" "op scsiicr dcl"; do
+    for v in "live" "devsig" "byte rd" "byte rd liv" "hrd genctl" "hrd genctl lv" "hrd genctl nod" "hwr genctl" "hwr genctl lv" "hrd t2ctl" "hrd t2ctl lv" "hrd t2ctl nod" "hwr t2ctl" "hwr t2ctl lv" "hrd t2icr" "hrd t2icr lv" "hrd t2icr nod" "hwr t2icr" "hwr t2icr lv" "hrd sccerr" "hrd sccerr lv" "hrd sccerr nod" "hwr sccerr" "hwr sccerr lv" "hrd scctx" "hrd scctx lv" "hrd scctx nod" "hwr scctx" "hwr scctx lv" "wrd sccerr" "wrd sccerr lv" "wrd sccerr nod" "wwr sccerr" "wwr sccerr lv" "wwr sccerr dcl" "val h genctl" "val w sccerr" "rb genctl" "rb genctl dcl" "rb vecbase" "rb t2ctl" "rb t2ctl dcl" "rb t2icr" "rb t2icr dcl" "rb scctx" "rb scctx dcl" "hwr sccerr dcl" "rb genctl lo" "latch same" "latch two" "latch aba" "latch same2" "latch all" "latch all lv" "acc genctl" "acc genctl nod" "acc t2ctl" "acc t2ctl nod" "acc t2icr" "acc t2icr nod" "acc scctx" "acc scctx nod" "acc sccerr" "acc sccerr nod" "op vecbase" "op vecbase dcl" "op pscale" "op pscale dcl" "op t1ctl" "op t1ctl dcl" "op t1icr" "op t1icr dcl" "op sccicr" "op sccicr dcl" "op sccrx" "op sccrx dcl" "op scsiicr" "op scsiicr dcl" "rb sccicr" "rb sccrx" "rb scsiicr" "op pscale noig" "rb vecbase own" "hwr ipl noig" "latch all w" "latch all d" "acc all" "acc all lv" "acc pscale ign" "acc ipl ro" "rb t1ctl" "rb t1icr" "hrd ipl" "hrd ipl lv" "hrd ipl nod" "hwr ipl" "hwr ipl lv" "hwr ipl dcl" "op mask" "op mask dcl" "rb mask"; do
         check "pcc2 width row: $v" "$(count "$PCC2LOG" "^$v  .*ok$")" "1"
     done
 
     #  DENOMINATOR, SUMMED -- a lost row and a failing row need different responses.
-    check "pcc2 width rows emitted"           "$(( $(count "$PCC2LOG" " ok$") + $(count "$PCC2LOG" " FAIL$") ))" "60"
-    check "pcc2 width rows green" "$(count "$PCC2LOG" " ok$")"   "60"
+    check "pcc2 width rows emitted"           "$(( $(count "$PCC2LOG" " ok$") + $(count "$PCC2LOG" " FAIL$") ))" "101"
+    check "pcc2 width rows green" "$(count "$PCC2LOG" " ok$")"   "101"
     check "pcc2 width rows red"   "$(count "$PCC2LOG" " FAIL$")" "0"
 fi
 

```

## THE PRODUCT DIFF (`src/devices/dev_pcc2.c`: comments + one typedef, INLINED IN FULL)

```diff
diff --git a/src/devices/dev_pcc2.c b/src/devices/dev_pcc2.c
index e795fe9..9def138 100644
--- a/src/devices/dev_pcc2.c
+++ b/src/devices/dev_pcc2.c
@@ -64,8 +64,9 @@
 
 // #define	debug fatal
 
-/*  pcc2widthkills: TWELVE width-guard blocks in DEVICE_ACCESS(pcc2) ended the host
-    on a guest-chosen access width -- an ordinary aligned halfword load of a documented
+/*  pcc2widthkills: TWELVE width-guard blocks in DEVICE_ACCESS(pcc2) -- TEN of them
+    `fatal(); exit(1)' kills that ended the host on a guest-chosen access width, and
+    two (IPL, MASK) #119 warn-once latches that declined it process-globally -- an ordinary aligned halfword load of a documented
     register.  Same class as #337 (dev_wdc.c) and #497 (dev_sgi_re.c).
 
     THE TREE ALREADY KNEW THE WIDTH IS LEGAL: mvme_pcctworeg.h says the PCCchip2
@@ -80,22 +81,30 @@
               byte" ONLY at len == 1: memory_readmax64 composes big-endian, so
               (uint8_t) idata is the HIGHEST-address lane.  Deleting the guard would
               store the neighbour's byte -- st.h 0xAABB to GENCTL would set GENCTL to
-              0xBB, VECBASE's lane.  And seven arms mask, read-modify-write or clear
-              on write, six of them calling reassert_interrupts().  Now: DECLINE +
+              0xBB, VECBASE's lane.  And eight arms mask, read-modify-write or clear
+              on write, and seven of the twelve blocks call reassert_interrupts()
+              (five of those eight; a seat measured the earlier "six" wrong).  Now: DECLINE +
               latched announce.  Per-lane composition through each arm (COMPOSE) is
               the faithful upgrade and is FILED as pcc2widecompose; not taken here
-              because the hardware's lane semantics are not on disk and no measured
-              driver wide-writes these registers.
+              because the hardware's lane semantics are not on disk and no driver
+              MEASUREMENT exists either way: the only consumer is mvme187, no mvme187
+              boot runs in this harness, and the one OS source in the tree (OpenBSD
+              2.2) declares these registers `volatile u_char' and byte-accesses them
+              -- a reading, not a measurement.
 
     ONE BIT PER BLOCK, twelve, per instance: a driver bringing up the chip touches
     several of these in one pass, and one latch would announce the first and silence
     the rest (#497's own reasoning).  Auto-incremented rather than `1 << N' literals,
-    which this fork records as collision-prone; PCC2_W_NBITS bounds it.
+    which this fork records as collision-prone; PCC2_W_NBITS names the count, and the
+    typedef after the enum makes the build fail if it ever exceeds the 32-bit field.
 
     REACHABILITY, verified: every non-byte m88k access is alignment-checked BEFORE
-    memory_rw, and `relative_addr %= PCC2_SIZE' keeps parity, so only the five
-    EVEN-offset blocks (GENCTL, TxCTL, TxICR, SCCERR, SCCTX) are GUEST-reachable; the
-    seven odd ones are OPERATOR-reachable -- the debugger's `put h' warns on a
+    memory_rw, and `relative_addr %= PCC2_SIZE' keeps parity, so only the SIX
+    EVEN-offset blocks (GENCTL, TxCTL, TxICR, SCCERR, SCCTX, IPL) are GUEST-reachable
+    (this said "five" until pass 2; IPL at 0x3e is even, and a seat counted); the
+    eight odd OFFSETS -- the six odd-only blocks VECBASE, PSCALEADJ, SCCICR, SCCRX,
+    SCSIICR, MASK, plus the T1CTL/T1ICR labels of the shared TxCTL/TxICR blocks --
+    are OPERATOR-reachable -- the debugger's `put h' warns on a
     misaligned address and stores anyway, MEASURED (artifacts/pcc2widthkills/
     operator_reach_20260903.out: `put h 0xfff42003' ended the host).  All twelve are
     converted; the detector reaches the odd ones through that path.
@@ -118,6 +127,9 @@ enum {
 	PCC2_W_MASK_LEN,	/*  was a #119 function-static: process-global  */
 	PCC2_W_NBITS
 };
+/*  A seat pointed out that NBITS "bounded" nothing.  Now it does: negative array
+    size is a compile-time error, C99, no assert.h.  */
+typedef char pcc2_w_fits_in_warned[PCC2_W_NBITS <= 32 ? 1 : -1];
 
 struct pcc2_data {
 	struct interrupt	cpu_irq;

```

## PRETABLE_amendments.out (Sections 5-7) and PRETABLE_pass4.out (Section 8)

```
PRETABLE AMENDMENTS -- pcc2widthkills, killtable2_20260903.  Split out of PRETABLE.out on pass 3.


SECTION 5 -- AMENDMENT, written after table-2 PART 1 (9 mutants + BASE, all killed) and
BEFORE PART 2.  Section 2's "sentence owed" was RULED A FLOOR BREACH, not a disclosure.
--------------------------------------------------------------------------------
The measuring seat, running its own pass 3 against the 78-row detector, asked whether the
disclosed asymmetry (PSCALEADJ/SCCICR/SCCRX/SCSIICR: no readback, so a guard that ANNOUNCES
and then lets the halfword land is invisible) can be discharged by clause (e).  Ruling: NO.
Clause (d) is a FLOOR -- "the guard kept, its effect removed" -- and the fall-through shape at
those arms is exactly that.  Clause (e) governs claims ABOVE the floor; a disclosure cannot
place a detector below it, or every floor breach becomes dischargeable by a sentence.  The
CHANNEL rule in Section 4 already said as much: a `dcl' row cannot vary under a mutant that
keeps announcing, so at those four arms it was the WRONG channel for this shape.

Rows added (part 2 measures them):
  rb sccicr / rb sccrx / rb scsiicr   set 0x1f by byte, decline put h 0xaab8, read back 0x1f
                                      M_FALL_* lands 0x18 (& 0x1f) / 0x98 (& 0xdf) and REASSERTS
  op pscale noig                      PSCALEADJ's body stores nothing and only prints; count of
                                      "PSCALEADJ ignored" in the wide-write session == 0.
                                      M_FALL_PSCALEADJ prints it once.
Blast radius is NOT uniform across the four (the seat's point): three of them put the
neighbour's lane into an INTERRUPT CONTROL register and reassert; one prints.  One sentence
had covered all four, which was too coarse as well as below the floor.


SECTION 6 -- PASS 3: THE CLASS CLOSURE.  Written after pass 3's seats landed and BEFORE
part 3 of the table.
--------------------------------------------------------------------------------
Pass 3 found the SAME class a third time: the fable5 seat MEASURED announce-then-fall-through
at VECBASE as 82/82 (its `pcc2p3_fable/probe_mfall_vecbase.out`).  `rb vecbase' is GENCTL's
neighbour-lane check (st.b VECBASE; st.h GENCTL; ld.bu VECBASE) and Section 2 above credited
it as VECBASE's own readback -- a wrong record that hid the cell.  Independently, glm and grok
named IPL: its write body prints "write to read-only PCCTWO_IPL; ignored" once per process and
stores nothing, so a fall-through has a MESSAGE channel exactly as PSCALEADJ does -- and the
fable5 seat had called that cell a no-op, the same direction the builder was wrong about
PSCALEADJ.  SCCERR's fall-through cell is EQUIVALENT BY CONSTRUCTION: the arm stores 0 and no
code in the model stores a nonzero SCCERR (grep), so decline and land are the same state.

The enumeration (12 blocks x 6 shapes) is now written into the probe's CONTRACT with a status
per cell; the two open cells get rows:
  rb vecbase own   st.b 0x50 at VECBASE; put h 0xaab8 at VECBASE; ld.bu -> 0x50.
                   M_FALL_VECBASE lands 0xb0 (0xaab8 & 0xf0) and also prints HUH.
  hwr ipl noig     st.h 0x0303 at IPL (guest-reachable); count of the read-only print == 0.
                   M_FALL_IPL prints it once.
The codex seat added two shapes the six-shape list did not have, both closable at all twelve
blocks by one cardinality row each:
  latch all w      `len != 1' -> `len == 2' (LEN's mirror) declines every halfword row and lets
                   a WORD land; twelve `put w' writes, twelve announces.  M_LEN2_VECBASE -> 11.
  acc all (+lv)    the contract claimed byte writes land "at every reachable arm" while acc
                   rows existed at five blocks.  Twelve legal `put b' writes, ZERO declines.
                   M_GROW_PSCALEADJ (`len != 1' -> `len != 0' at an arm with no acc row) -> 1.
The Opus reader seat MEASURED a ninth shape, 82/82, ONE character: `writeflag == MEM_WRITE'
-> `<= MEM_WRITE', the direction split's own conjunct nulled, so wide READS are declined,
announced as writes, skip the arm's read body and consume the latch bit.  No session holding
a wide read carried a decline-count row.  Closed with ZERO new sessions:
  hrd <block> nod  (six even blocks) and wrd sccerr nod: t.count(DECL) == 0 on the existing
                   wide-read sessions.  M_RDDECL_ALL (all twelve conjuncts) -> seven reds.
  The six odd blocks' read-side cells are UNREACHABLE by construction (guest wide reads at
  odd offsets alignment-fault before memory_rw; debugger reads do not dispatch to DM_DEFAULT
  devices) and are disclosed in the contract.
The T1 labels (deepseek): TxCTL/TxICR are SHARED blocks whose readbacks sat at the T2 offsets;
`rb t1ctl' / `rb t1icr' (operator path, own readbacks) close the T1 half.  M_FALL_TXCTL
(break removed at the shared block) -> rb t2ctl AND rb t1ctl both red.  SCCRXIACK (glm): the
thirteenth arm, never width-guarded, body ignores idata -- named in the contract as excluded.
Part 3 measures BASE 96/96, M_FALL_VECBASE, M_FALL_IPL, M_LEN2_VECBASE, M_GROW_PSCALEADJ,
M_RDDECL_ALL, M_FALL_TXCTL.  Every other cell keeps its measured or same-channel status from
parts 1-2 and the builder's pass 3/3b/3c: adding rows cannot un-kill a mutant.  A closing
pass 4 verifies THIS enumeration (12 x 9 plus the two T1 labels, written into the contract);
it does not hunt cells.


SECTION 7 -- PART 3 MEASURED (killtable2_20260903/part3/, part3b/), and what it corrected.
--------------------------------------------------------------------------------
Part 3 (96-row instrument): BASE 95/96 -- `rb t1ctl' red on the fix by a STRING mismatch (the
row wanted "0x03", the debugger prints "0x3"; the value was right).  Fixed; part 3b BASE 96/96.
Kills, each on exactly the row Section 6 named (the artifact row subtracted):
  M_FALL_VECBASE    rb vecbase own          M_FALL_IPL       hwr ipl noig
  M_LEN2_VECBASE    latch all w             M_RDDECL_ALL     all seven hrd/wrd * nod (88/96)
  M_FALL_TXCTL      rb t2ctl AND rb t1ctl   (part 3b, BASE full: the T1 cell measured)
ESCAPE: M_GROW_PSCALEADJ 95/96 (part 3) and 96/96 (part 3b) -- `acc all' did not move, WITH
the mutation PROVEN in the source (1 x `len != 0') and the binary newer than the source (3b's
proof lines).  So the row could not see the arm: the debugger's `put b' calls memory_rw with
NO_EXCEPTIONS, and memory_rw.c's device dispatch is `if (!no_exceptions || (flags &
DM_READS_HAVE_NO_SIDE_EFFECTS))'; pcc2 registers DM_DEFAULT, so a NO_EXCEPTIONS byte write is
never dispatched.  `put h/w/d' go through store_Nbit_word and do reach the arms (every other
cardinality row worked).  THE ROW WAS VACUOUS BY CONSTRUCTION -- the CHANNEL rule's failure
condition, caught by the table rather than at writing time.  `acc all' is now twelve GUEST
`st.b' stores (legal at every offset), and part 3c re-measures BASE + M_GROW_PSCALEADJ.
The contract now states the `put b' fact so no future row rests on it.


PRE-TABLE AMENDMENT, PASS 4 -- its own file so its mtime is its own order witness for part 4.
(PRETABLE_amendments.out holds Sections 5-7; appending Section 7 there had re-created the very
mtime defect Section 6 was split out to avoid -- a pass-4 seat caught it.)

SECTION 8 -- PASS 4 (panel_20260903_180648): the enumeration's DERIVATIONS verified by all nine
seats (fable5 ratified on an analytic sweep that omitted the helper edits -- overturned by
measurement), its DOMAIN found short.  Written BEFORE part 4.
--------------------------------------------------------------------------------
Every landing value, cardinality drop and red count in the contract was re-derived and held
(glm, grok, codex, kimi).  Two holes, both on axes the contract names and never walked:
  THE HELPER'S OWN OPERATIONS.  `d->warned |= (1u << bit)': `|=' -> `=' (glm, kimi, codex)
    -- A then B clears A's bit; `latch same' only ever sees consecutive repeats.  Row:
    `latch aba' (GENCTL st.h, VECBASE put h, GENCTL st.h -> TWO announces).  And
    `(1u << bit)' -> `1' (minimax) -- bit 0 always, every other block announces every time;
    `latch same' is at bit 0.  Row: `latch same2' (MASK put h twice -> ONE).
  WIDTH 8.  Rows drove {1,2,4}; `put d' gives 8 (glm, deepseek, codex).  A guard true on
    {2,4} and false on 8 (`len & 6') passed every row.  Row: `latch all d' (twelve put d ->
    twelve announces).
Accept side (codex): `acc all' proves no-decline and survival, not that the byte reached the
body; the two print-only arms get `acc pscale ign' / `acc ipl ro' (their prints, once).
Records corrected: TxCTL FALL cell S -> M (3b measured it; deepseek); "no S cell is
survival-only" restated for KILL cells (deepseek); "six shapes" -> nine (codex, deepseek);
the opening "twelve exit(1) blocks" -> ten kills + two latches (codex); the A/C note's
"96/96 part 3" -> 95/96 part 3, 96/96 part 3b (glm); the `rb t1ctl' comment for the RMW arm
(grok); "product diff is comments only" -> comments + the pass-2 typedef (codex).
THE OPUS READER MEASURED THE BREACH on the shipped 96 rows (frozen md5 72759b4f, own clone):
M_LATCHASSIGN (`|=' -> `=') 96/96 TOTAL SWEEP with the mutation proven and the binary newer;
M_BITSHIFT (`1u << bit' -> `1u << (bit + 1)') 96/96 and EQUIVALENT (bit identity has no
consumer) -- the clause-(f) control, now disclosed in the contract.  It also named: `break'
-> `return 0' (the FAULT member, unmeasured -- M_RET0_GENCTL added); announce SEVERITY
(`fatal(' -> `debug(') unobservable by text rows under -V -- disclosed; the SCCERR deriver
keyed on a correlate -- corrected; three instruments presented as one -- the transfer stated;
`acc all' REWRITTEN, so "adding rows cannot un-kill" was the wrong warrant -- corrected.
PREDICTIONS for part 4: BASE 101/101; M_LEN8_VECBASE -> `latch all d' 11; M_LATCH_ASSIGN ->
`latch aba' 3 (and `latch same' stays 1, `latch all' stays 12); M_LATCH_BIT0 -> `latch same2'
2 (and `latch aba' 2, `latch all' 12); M_GROW_IPL -> `acc ipl ro' 0 and `acc all' 1;
M_RET0_GENCTL -> `hwr genctl' / `hwr genctl lv' red (the guest store faults).

```

## DISCLOSURE -- `git diff --numstat` for the round's files

```
258	0	CHANGELOG.md
60	0	OUTSTANDING_BUGS.md
3	3	regress/gate_arm.sh
327	8	regress/pcc2_width_probe.py
20	6	regress/sgi_de_primop_probe.py
22	10	src/devices/dev_pcc2.c
464	5	tools/pipeline/ledger.json
3	3	tools/pipeline/matrix.html

```
    regress/pcc2_width_probe.py   INLINED
    regress/gate_arm.sh           INLINED
    src/devices/dev_pcc2.c        INLINED
    regress/sgi_de_primop_probe.py  NOT SHOWN -- a different round (#500 pass 16, comment-only)
    OUTSTANDING_BUGS.md           NOT SHOWN -- filings
    CHANGELOG.md                  NOT SHOWN -- the round blocks
    tools/pipeline/ledger.json    NOT SHOWN -- seat records
    tools/pipeline/matrix.html    NOT SHOWN -- generated


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
