#!/usr/bin/env python3
"""pcc2widthkills DETECTOR -- the twelve width-guard blocks in DEVICE_ACCESS(pcc2).

WHAT THE FIX DID.  Twelve `if (len != 1)' blocks -- TEN `fatal(); exit(1)' kills that ended the host on
a guest-chosen access width, and two #119 warn-once latches that refused it with a
process-global static.  The
tree's own header says PCC2 registers "can be accessed as bytes, two-bytes, or
four-bytes", so the width is LEGAL.  The fix is a DIRECTION SPLIT:

    READS   ACCEPT -- the memcpy above the switch already served them, raw bytes in
            address order, width-correct by construction.  The guard discarded a
            correct answer.
    WRITES  DECLINE + per-instance latched announce -- every STORING write arm uses `idata'
            (SCCERR stores a constant 0; PSCALEADJ and IPL store nothing and print),
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
      PSCALEADJ  S     S     W     S     C     M     C     A/C    op pscale noig  (message; acc pscale ign)
      TxCTL      S     M     W     S     C     M     C     A/C    rb t2ctl (FALL: part 3b, t2 and t1)
      TxICR      M     M     W     S     C     S     C     A/C    rb t2icr
      SCCERR     S     M     S     S     C     E     C     A/C    E: the arm stores 0 and nothing in
                                                                  the model ever stores a nonzero
                                                                  SCCERR (deriver: every writer of
                                                                  pcctwo_reg[], grep -F 'pcctwo_reg[';
                                                                  the counter memcpy's 8-byte span
                                                                  is pcc2counter8, disclosed)
      SCCICR     S     S     W     S     C     M     C     C      rb sccicr
      SCCTX      M     M     W     S     C     S     C     A/C    rb scctx
      SCCRX      S     S     W     S     C     M     C     C      rb sccrx
      SCSIICR    S     S     W     S     C     M     C     C      rb scsiicr
      IPL        S     S     W     M     C     M     C     A/C    hwr ipl noig    (pass-3 repair; acc ipl ro;
                                                                  the write body prints once)
      MASK       M     M     W     M     C     M     C     C      rb mask
      C  = the cardinality row `latch all' (twelve wide writes, twelve announces): ALIAS,
           any collision drops the count; SWAP: the bare swap drops the length test and every byte preset
           kills it (part 7, 95/171); a value-test QUALIFIER on the guard is caught only
           for the VALUES rows drive AT EVERY ARM -- 3 (`latch all'), 1 (`latch all
           one') and 0 (`latch all zero') -- and, per arm, for whatever that arm's own
           wide-write rows drive (0xaabb, 0xaab8, 0x0022 ...); any other constant is not
           (passes 7-8; Opus F13).
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
      DECL where zero is expected.  The six ODD blocks' WIDE-read cells are UNREACHABLE by
      construction -- a guest wide read at an odd offset alignment-faults before memory_rw
      (BYTE reads do reach them; see THE SECOND PREDICATE),
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
      announces 12 either way; `latch aba' DOES distinguish it (A=1, then the field is 3,
      and 3 == 1 is false, so A re-announces -- MEASURED 100/101 by a pass-5 seat).  An
      earlier version of this sentence called it indistinguishable; the instrument was
      stronger than its contract said.  `|=' -> `^=' or `+=' in the SET line is
      EQUIVALENT: the SET runs only under the TEST, i.e. only when the bit is clear.
      WIDTHS.  The debugger drives len 2 (`put h'), 4 (`put w') and 8 (`put d'); the
      guest drives 1, 2 and 4.  `latch all', `latch all w' and `latch all d' pin the
      ANNOUNCE at every block for each non-byte width, so a guard true on a subset of
      {2,4,8} drops one of the three counts; the REFUSAL per width is `rb *', `rb4 *'
      and `rb8 *' (see THE LANDING CHANNEL AT EVERY WIDTH).
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
      error.  At the six GUEST-reachable blocks the guest's store faults and the program
      never prints, so the block's `lv' row reds while its `hwr' row stays green -- the
      HOST survives (M_RET0_GENCTL, part 4: `hwr genctl lv' died, `hwr genctl' exit0; an
      earlier version of this sentence and PRETABLE_pass4 said the pair).  At
      the six OPERATOR-only blocks NOTHING above sees it -- MEASURED 101/101 at VECBASE
      by a pass-5 seat -- so `latch all fail' counts memory_rw's "failed ]" line at zero
      over the twelve-block session (M_RET0_VECBASE, part 5).
      THE FIX'S OWN STATE AS A GUARD INPUT (pass 5, MEASURED 101/101 at one arm and at all
      twelve by the Opus seat).  A guard qualified by its own latch bit -- `&& !(d->warned &
      (1u << bit))', the canonical clause-(d) conjunct -- declines and announces the FIRST
      wide write exactly as the fix does and lands the SECOND.  Every row above observed
      the device only while its latch was still armed.  Closed at every block by `rb2 *'
      (set, two wide writes, read back), `pscale noig2' and `ipl noig2' (the body's print,
      counted at zero after two writes); SCCERR is value-identical there too (E).
      THE SECOND PREDICATE.  Each arm's `if (writeflag == MEM_WRITE)' is now load-bearing
      for reads that fall through to it: WIDE reads at the even blocks since the split
      (the pre-fix guard killed them first), and BYTE reads at EVERY block, always (a byte
      access skips the alignment check and passes `len != 1').  Deleting it stores
      idata == 0 on a read while the readback in the same stream -- served by the memcpy
      before the switch -- still prints the old value; only a second read sees it.
      Pinned by `hrd * rb' (wide, four even storing blocks), `hrd ipl noro', and by
      `brd2 *' (byte, read twice, all nine storing blocks) with `brd pscale noig' /
      `brd ipl noro'; SCCERR is E.  It does not dominate the edited lines, so it sits
      outside the clause-(d) closure and is carried here as construction, not as a breach.
      THE LANDING CHANNEL AT EVERY WIDTH (pass 6, Opus seat, measured).  `latch all',
      `latch all w' and `latch all d' pin the ANNOUNCE at all twelve for len 2, 4, 8 --
      not the refusal: `break;' -> `if (len < 4) break;' at all twelve announced and
      LANDED every 4- and 8-byte write and scored 118/118.  The REFUSAL is pinned per
      width by `rb *' (len 2), `rb4 *' and `rb8 *' (nine storing blocks each, and the T1CTL /
      T1ICR labels), by
      `pscale noig4|8' / `ipl noig4|8' (the print-only bodies), and announce-once per
      width by `latch same' / `latch samew' / `latch samed'; SCCERR is E at every width.
      Landed lanes under a fall-through, len 4 / len 8: MASK 0xdd/0x44, VECBASE
      0xd0/0x40, TxCTL 0x01/0x00, TxICR 0x15/0x04, SCCICR and SCCTX (`& 0x1f') 0x1d/0x04,
      SCCRX and SCSIICR (`& 0xdf') 0xdd/0x44; GENCTL's own lanes 0xd9/0x40 -- none equals
      its preset, and none carries PCC2_C040 at GENCTL.
      The 8-byte pattern's low lane is 0x44 because 0x33 EQUALLED the TxCTL and TxICR
      presets through `& 3' and `& 0x17' -- measured in part 6, where `rb8 t2ctl' and
      `rb8 t2icr' stayed green under the fall-through; a readback row must choose a
      value whose landed lane differs from the preset under THAT arm's mask.
      The 4- and 8-byte rows are OPERATOR rows (`put w' / `put d'): only SCCERR is
      4-aligned, so a guest word store reaches no other block.
      THE GUARD'S OPERAND SPACE, CLOSED AS A CLASS (pass 6; RESTATED pass 7 after the same
      class was found a third time).  Clause (d) rule (2) draws a guard's extra operand from
      the LVALUES THE GUARDED BODY READS, walked to the enclosing function only -- never into
      callees -- so the closure is NON-TRANSITIVE BY DEFINITION.  Enumerated per arm, each
      lvalue with the bits a row CAN hold (dead bits -- set by no writer -- are named as
      such) and the row holding it non-initial at a wide write:
        TxCTL   reads d->pcctwo_reg[relative_addr] (RMW): bits 0-1 by the byte presets
                (`rb/rb4/rb8 t2ctl', `rb/rb4/rb8 t1ctl'); bits 4-7, the overflow count that
                ONLY pcc_timer_tick sets, held at 1 by `ovf1 *' / `ovf2 *' and at >= 8 (bit 7;
                the rows mask to bits 7 and 0, so 9-15 under host load read the same)
                by `ovfhi1 *' / `ovfhi2 *' (free-running, the count re-armed each iteration);
                a predicate true of 0, 1 and 8 alike is disclosed, not owed -- NAMED: the
                count at 2-7 and 9-15, bits 0-1 = 2 (COC alone), the byte 0xff; bits 2-3
                are set by NO model writer (the body stores `idata & 3', COVF only clears,
                the tick writes bits 4-7) except the counter arm's raw memcpy -- the filed
                pcc2counter8 path, which a guest `st.d' at the 8-aligned T2COUNT reaches --
                so they are held, all at once with bits 5-7, by `rb t2ctl b27' / `rb t1ctl
                b27' (measured: `&& !(reg & COVF)' 188/190).  Those two rows REST ON A FILED
                DEFECT and must be re-cut when it is fixed (bits 4-7 via overflows; bits 2-3
                then have no writer and become dead).  Pass 9 corrected the earlier sentence
                here that called the path operator-only and the bits E with no row.
        TxICR   reads the register (bits 0, 1 and 4 by the 0x13 presets, bit 2 by the 0x17
                presets; the combination 0x37 -- IL bit 2 with INT -- is held by no row and a
                guard exempting exactly it is a disclosed escape by name; continuing:
                presets of `rb t2icr il4' / `rb t1icr il4'; bit 5 INT, set ONLY by
                reassert_interrupts under a pending count, by `pend*'),
                d->pending_timer1/2_interrupts, held at 1 by `pend1 *' / `pend2 *' and at
                thousands by `pendn1 *' / `pendn2 *' (COC with compare 1; a predicate true of
                1 and ~9999 alike, `< 10000' say, is disclosed by name), and JOINTLY with
                each other, with the label and with idata's IEN bit (JOINT CELLS below), and relative_addr
                (the T1/T2 label: `rb t1icr', `op t1icr dcl', `pend1 *' hold the T1 value,
                every T2 row the other).
                TxCTL reads relative_addr too, as its RMW index: the same T1/T2 rows.
                BIT COVERAGE, the checkable form of the above (pass 9, Opus seat): reg[TxCTL]
                is held at {0x00, 0x03, 0x11, 0x81 (masked to bit 7 and CEN: the masked rows' KILL channel
                is CEN alone -- a landed write drives idata 0 and clears it -- bit 7 is arming, and
                bits 1-6 of that state are pinned only by `ovf*' at the exact 0x11, so the ovfhi wide
                writes must keep bit 0 clear; Opus, pass 10), 0xfc} -- all eight bits held SET and CLEAR;
                reg[TxICR] at {0x00, 0x13, 0x17, 0x31} -- every live bit (0, 1, 2, 4, 5) both
                ways, bits 3, 6, 7 dead by census.  That is why every single-bit predicate on
                either register is killed, and it is what a future edit must preserve; the
                pending counts are held at 0, 1 and thousands.
                JOINT CELLS (pass 10, adjudicated by the flagship seat; the rule now lives in
                CLAUDE.md clause (d)): a joint cell is in the closure exactly when the guarded
                BODY'S OWN CODE distinguishes it; the enumerated cells are the CROSS-PRODUCT of
                the body-tested partitions.  THE DENOMINATOR, read off the TxICR write body
                (dev_pcc2.c, the `if's between `writeflag == MEM_WRITE' and reassert): SEVEN
                partitions -- the label (== T1ICR / T2ICR), idata & IEN, idata & ICLR, the
                register's INT bit, pending1 > 0, pending2 > 0, idata & 0xe0 -- 128 cells.
                ROWED, all sixteen cells of {T2, T1} x {p1 = 0, > 0} x {p2 = 0, > 0} x {IEN
                clear, set} at a wide write: (label, 0, 0, *) by the plain rows (`latch all'
                drives 3, IEN clear; `rb t*icr' 0xaab8, IEN set); (T1, >0, 0, *) `pend1 rb' /
                `pend1 rbi'; (T2, >0, 0, *) `pend1 rb2' / `pend1 rb2i'; (T2, 0, >0, *) `pend2
                rb' / `pend2 rbi'; (T1, 0, >0, *) `pend2 rb1' / `pend2 rb1i'; (T2, >0, >0, *)
                `pendboth rb' / `pendboth rbi'; (T1, >0, >0, *) `pendboth rb1' / `pendboth
                rb1i'.  Pass 9 held one of these; pass 10 found its mirror open (Opus, predicted
                194/194 before the build) and the (T1, 0, >0) cell open (codex, Opus); the
                product closed in one diff.  NOT ROWED, DISCLOSED WITH THE COUNT: the ICLR, INT
                and 0xe0 partitions (the other 112 cells) -- they change what a landed write DOES
                to the counts, not whether it lands, and rowing them costs about thirty more wide
                writes; a guard exempting one of those cells is outside this contract as stated,
                and pass 11 is asked whether the rule demands them.  Partitions the body does NOT
                test are DISCLOSED under clause (e): both counts >= 2 at once (the body tests
                `> 0' only; grok read OpenBSD's clock.c as arming COC on both timers -- that
                source is not in this tree and is NOT independently verified; the in-tree
                warrant for the joint state is the MODEL's own: one pcc_timer_tick callback
                services both timers and reassert_interrupts reads both counts on every
                call -- Opus, pass 10), `idata == k' for any k no row drives, TxICR 0x37,
                TxCTL 0xff, the overflow count at 2-7 and 9-15.  The De Morgan form of the gap
                this closes (kimi substitute, pass 10): `!(p1 && p2)' is `p1 == 0 || p2 == 0'
                -- neither disjunct true of all its lvalue's held values, the disjunction true
                in every row, so a per-lvalue disclosure test could never fire on it.
                Bit 3 (ICLR, 0x08) is a WRITE STROBE: the body TESTS it (`idata & PCC2_TTIRQ_ICLR') and
                never stores it -- the store mask 0x17 is bits 0, 1, 2, 4 -- so the register bit is set by
                no writer (pass 10 accepted a sentence calling the mask a writer of it; pass 11 reverted
                that: 0x17 & 0x08 == 0).  Bits 6-7 of the TxICR byte are set by no writer at all (body `idata & 0x17',
                reassert bit 5, the counter memcpy cannot reach 0x1a): E, same warrant.
        IPL     reads the function-static `w' of its WRITE branch (its #119 print latch):
                `ipl wset'.  The READ branch has a second static of the same name; it is
                outside the closure (not the guarded write body) and `ipl rset' holds it
                set anyway.
        helper  reads d->warned: `rb2 *' holds each arm's OWN bit set; a guard naming
                ANOTHER arm's bit (the sibling round's foreign-bit cell, sgi_de pass 16,
                filed there as derived-not-measured) is held by `latch all' + `latch all
                rev' -- every ordered pair of blocks, measured in part 8.
        GENCTL, VECBASE, SCCICR, SCCTX, SCCRX, SCSIICR, MASK: pure stores (`= idata & m'),
                reading no PRIOR device state -- `idata' (the value under test, read by ten
                of the twelve bodies) is held by every wide-write row and pinned per arm by
                `latch all' / `latch all one' / `latch all zero'.  SCCERR: constant store.
                PSCALEADJ: reads only idata (print).  So a guard conditioned on those registers' bits
                (the SCC* INT bits included) is OUTSIDE the closure; the byte presets still
                pin their landing.
      OUT OF CLOSURE, disclosed not owed: d->pcctwo_reg[PCCTWO_IPL] is read by the IPL arm's
      READ branch and by the callee reassert_interrupts(), not by IPL's guarded write body --
      `&& reg[IPL] == 0' at the IPL guard escapes with a one-message consequence, and at any
      arm no row wide-writes with an interrupt pending; at TxICR the pend rows DO (reassert
      has raised IPL to the pending level), so the all-twelve form is killed there: MEASURED
      by the pass-7 Opus seat, 155/159, red pend1/pend2 decl+rb (pass7_seats_20260904/opus/).
      Likewise `&& pending_timer2 == 0' at all twelve: 157/159,
      the TxICR-only signature -- the conjunct is invisible at the other eleven arms, which
      is what the non-transitive closure predicts and discloses;
      cur_int_vec[] is WRITTEN by reassert_interrupts() and read only by the IACK handler.
      GATE 14 IS LOAD-SENSITIVE since pass 6: the pend*/ovf* rows need the host's 100 Hz
      SIGALRM to fire during a `continue' (20 s ceiling -- inert until pass 8: the tuple's
      third element was read after unpacking, so the wait returned at once), so a starved
      host reds them for a
      reason the row names (`no-breakpoint') -- run the gate alone.  Their poll loops also
      rely on GENCTL.MIEN being clear at init, so the guest never takes the interrupt.
      At GENCTL the 4-/8-byte lanes are 0xd9 / 0x40: 0xdd and 0x44 carry PCC2_C040 and a
      LANDED write there ends the host (pcc2c040kill) -- the row would still kill, by death
      instead of by value, and the NOROW line below would be false (pass 7, measured).
      reassert_interrupts() (a callee of seven bodies) reads GENCTL, the pending counts, the
      TxICR / SCC* IEN, INT and IL bits, MASK and IPL.  `latch all fail' rests on memory_rw's
      debug() line, which prints because this probe single-steps.
      pending_timer1/2_interrupts are INCREMENTED only by pcc_timer_tick (a SIGALRM callback
      that debugger.c stops during `step'); the TxICR body clears and decrements them.
      NOT PINNED, disclosed: the announce's `len=%i' value -- no row reads it (cosmetic,
      the NAME gap's sibling).  And the generic-DECL counts are over the WHOLE pty
      transcript: three other devices emit the same suffix, none instantiated on mvme187.
      OTHER DEVICE STATE AS A GUARD OPERAND (pass 6).  A guard conditioned on
      d->pcctwo_reg[], pending_timer*, the TxICR INT bit or reg[IPL] being NONZERO
      declines nothing in the init-state sessions (of the twelve guarded registers only
      VECBASE 0x0f and PSCALEADJ 0xdf are non-zero at init; CHIPID 0x20 is, and is not one
      of them), so `latch all' reads 0 -- killed.  One conditioned on them
      being ZERO is the shipped behaviour in every row that holds the field at its init
      value; MEASURED by both Agent seats at TxICR (`&& !d->pending_timer2_interrupts',
      `&& d->pending_timer1_interrupts == 0': 118/118 each) and closed as a class -- see
      THE GUARD'S OPERAND SPACE below.  The latch-set check (`rb2 *') is at width 2 only;
      the qualified-guard shape is width-agnostic, so its 4- and 8-byte repeats are
      coverage debt, FILED, not a floor cell.
      THE ODD BLOCKS FIRST.  Every guest-side channel at an odd block is absent by
      construction, and three consecutive passes found a shape with no channel there
      (fall-through x4, then at VECBASE and IPL, then FAULT x6).  A new shape is checked
      against the six operator-only blocks before anything else.
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
"""

import os, pty, re, select, sys, time

BIN = sys.argv[1] if len(sys.argv) > 1 else "build/gxemul"
LABEL = sys.argv[2] if len(sys.argv) > 2 else "local"

DUMMY = "/tmp/pcc2_dummy.bin"
open(DUMMY, "wb").write(b"\x00\x00\x00\x00")

CODE = 0x00010000
SCRATCH = 0x00020000
PCC2 = 0xfff42000
#  the SIX GUEST-reachable blocks (even offsets; IPL below is the sixth) and the six
#  OPERATOR-only ones (odd offsets; T1CTL/T1ICR are odd labels of the shared TxCTL/TxICR
#  blocks).  An earlier comment here said five and seven: a units slip, blocks vs labels.
GENCTL, T2CTL, T2ICR, SCCERR, SCCTX = 0x02, 0x16, 0x1a, 0x1c, 0x1e
VECBASE, PSCALEADJ, T1CTL, T1ICR, SCCICR, SCCRX, SCSIICR = 0x03, 0x15, 0x17, 0x1b, 0x1d, 0x1f, 0x2f
#  pcc2 pass 2: THE TWO FOLDED-IN ARMS HAD NO ROW AT ALL.  A seat found that the probe
#  touched no offset at 0x3e or 0x3f -- twelve blocks converted, ten given rows.  MASK
#  is GENCTL's byte-identical twin (store byte, reassert); GENCTL's null-repair was
#  caught by `rb genctl', MASK's by nothing, a 60/60 sweep.  AND IPL IS EVEN: it is the
#  SIXTH guest-reachable block, not a seventh operator one.
IPL, MASK = 0x3e, 0x3f
CHIPID = 0x00


def enc(op26, rd, rs1, imm):
    return (op26 << 26) | (rd << 21) | (rs1 << 16) | (imm & 0xffff)


#  r2 = PCC2 base, r3 = scratch, r4 = load target, r5 = store source, r6 = second source
#  ld.b / ld.h (0x07 / 0x06) SIGN-EXTEND: 0x82 would print as 0xffffff82.  Every row that
#  asserts a VALUE uses the unsigned forms ld.bu / ld.hu (0x03 / 0x02); the survival rows
#  only check exit status and keep the signed forms.
def LD_B(rd, off): return enc(0x07, rd, 2, off)
def LD_H(rd, off): return enc(0x06, rd, 2, off)
def LD_BU(rd, off): return enc(0x03, rd, 2, off)
def LD_HU(rd, off): return enc(0x02, rd, 2, off)
def LD_W(rd, off): return enc(0x05, rd, 2, off)
def ST_B(rs, off): return enc(0x0b, rs, 2, off)
def ST_H(rs, off): return enc(0x0a, rs, 2, off)
def ST_W(rs, off): return enc(0x09, rs, 2, off)
I_ST_SCR = enc(0x09, 5, 3, 0)          # st  r5,r3,0   scratch word
I_LD_SCR = enc(0x05, 4, 3, 0)          # ld  r4,r3,0
I_BR_SELF = 0xc0000000

SENTINEL = 0xdeadbeef
DEVSIG = "IGNORING write to read-only PCCTWO_CHIPID"
DECL = "-- declined.  (once) ]"
rows = []


def row(name, got, want, note=""):
    assert name not in [n for n, _ in rows], "DUPLICATE ROW NAME %r" % name
    assert len(name) <= 15, name    # load-bearing for gate_arm.sh: `%-16s' plus a literal space keep its `^$v  .*ok$' pattern satisfiable (pass 9, Opus)
    ok = (got == want)
    rows.append((name, ok))
    print("%-16s %-12s %-12s %-46s %s" % (name, str(got), str(want), note,
                                          "ok" if ok else "FAIL"))
    return ok


def session(cmds, settle=1.5, spin=1.2):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "mvme88k", "-e", "mvme187", "-M", "64",
                       "0x10000:" + DUMMY])
        os._exit(127)
    buf = ""

    def rd(t, until=None):
        #  drain the pty for t seconds; with `until', return as soon as that text has
        #  arrived (pass 7: a fixed drain after `continue' could send the next command to a
        #  guest that had not reached its breakpoint yet).
        nonlocal buf
        end = time.time() + t
        while time.time() < end:
            if until is not None and until in buf:
                return True
            r, _, _ = select.select([fd], [], [], 0.1)
            if not r:
                continue
            try:
                d = os.read(fd, 65536)
                if not d:
                    return False
                buf += d.decode("latin-1", "replace")
            except OSError:
                return False
        if until is not None and until in buf:    # pass 9 (codex): the token may land in the last read
            return True
        return "timeout" if until is not None else True

    alive = rd(settle)
    how = "nostatus"
    for i, c in enumerate(cmds):
        w = spin if i == len(cmds) - 1 else 0.25
        until = None
        if isinstance(c, tuple):    # (cmd, wait[, until]): `continue' waits for its breakpoint
            until = c[2] if len(c) > 2 else None    # read the tuple BEFORE unpacking it
            c, w = c[0], c[1]
        try:
            #  the one unbounded call left (pass 9, Opus): it blocks only if the pty input buffer fills
            #  while the guest free-runs -- tens of bytes per command against a kilobyte buffer.
            os.write(fd, (c + "\n").encode("latin-1"))
        except OSError:
            alive = False
            break
        r = rd(w, until)
        if r is False:
            alive = False
            break
        if r == "timeout":
            #  pass 8 (codex, grok): the guest never reached its breakpoint -- send it nothing
            #  more, and let every row of this session say so through cval().
            how = "no-breakpoint"
            break
    try:
        os.write(fd, b"quit\n")
        rd(0.4)
    except OSError:
        pass
    try:
        os.close(fd)
    except OSError:
        pass
    how = how if how == "no-breakpoint" else "nostatus"
    #  pass 7: a guest still running (no breakpoint reached) would block waitpid forever;
    #  give it a moment after the pty closed, then kill it -- the row says so, the gate
    #  does not hang.
    stat = None
    reaped = False
    for _ in range(30):
        try:
            p, stat = os.waitpid(pid, os.WNOHANG)
        except OSError:
            p, stat = pid, None
        if p:
            reaped = True
            break
        time.sleep(0.1)
    if not reaped:
        try:
            os.kill(pid, 9)
        except OSError:
            pass
        how = how if how == "no-breakpoint" else "killed"
        for _ in range(30):    # pass 8 (Opus F2): reap the killed child, bounded
            try:
                p, stat = os.waitpid(pid, os.WNOHANG)
            except OSError:
                p, stat = pid, None
            if p:
                reaped = True
                break
            time.sleep(0.1)
        if not reaped:
            how = how if how == "no-breakpoint" else "unreaped"
    try:
        if stat is None or not reaped or how in ("no-breakpoint", "unreaped", "killed"):
            pass
        elif os.WIFSIGNALED(stat):
            how = "sig%d" % os.WTERMSIG(stat)
        elif os.WIFEXITED(stat):
            how = "exit%d" % os.WEXITSTATUS(stat)
    except OSError:
        pass
    return buf.replace("\r", ""), alive, how


def printed(t, reg):
    m = re.search(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
    return "0x%x" % int(m.group(1), 16) if m else "absent"


def program(insns, at=CODE):
    #  `at' lets a session run TWO programs: a second sequence at the SAME address finds
    #  pc already there and the assignment is skipped (the Addr hazard, designed out in
    #  the sgi probes with Addr.take()).  Callers needing two pass at=CODE + 0x100.
    words = list(insns) + [I_BR_SELF, 0]
    cmds = ["put w 0x%x, 0x%08x" % (at + 4 * i, w) for i, w in enumerate(words)]
    return cmds + ["pc=0x%x" % at, "step %d" % len(insns)]


def setup(r5="0x5a5a5a5a", r6="0x0"):
    return ["r2=0x%x" % PCC2, "r3=0x%x" % SCRATCH, "r5=%s" % r5, "r6=%s" % r6,
            "r4=0x%x" % SENTINEL]


T1CMP, T1COUNT, T2CMP, T2COUNT = 0x04, 0x08, 0x0c, 0x10
def BB0(b5, rs, d16): return enc(0x34, b5, rs, d16)      # bb0 b5, rs, d16 (word displacement)
def program_free(insns, at=CODE):
    words = list(insns) + [I_BR_SELF, 0]
    cmds = ["put w 0x%x, 0x%08x" % (at + 4 * i, w) for i, w in enumerate(words)]
    return cmds + ["pc=0x%x" % at, "breakpoint add 0x%x" % (at + 4 * len(insns)), ("continue", 20.0, "BREAKPOINT")]
def pend_arm(cmp_off, cnt_off, icr_off, ctl_off):
    return [ST_W(5, cmp_off), ST_W(6, cnt_off), ST_B(7, icr_off), ST_B(8, ctl_off), LD_BU(4, icr_off), BB0(5, 4, -1)]
PEND_REGS = ["r5=0x1", "r6=0x0", "r7=0x11", "r8=0x1", "r9=0x0", "r10=0x13"]   # r10: the IEN-set wide-write value (pass 10)
def cval(alive, how, val):
    #  pass 8 (codex, grok): a decl/rb row graded after a missed breakpoint must say so;
    #  pass 9 (codex): so must one graded after the guest died under the session.
    if not alive: return "died (FAILED FOR SOME OTHER REASON)"
    return "no-breakpoint (FAILED FOR SOME OTHER REASON)" if how == "no-breakpoint" else val
def armval(t, alive, r4s):
    #  pass 7 (codex, grok): a row must fail for the reason under test or say otherwise.
    if not alive: return "died"
    if "BREAKPOINT" not in t: return "no-breakpoint (FAILED FOR SOME OTHER REASON)"
    return ("0x%x" % int(r4s[0], 16)) if r4s else "absent"

t, alive, how = session(setup() + ["r5=0x1", "r6=0x0", "r7=0x11", "r8=0x1", "r11=0x1b"]
                        + program_free(pend_arm(T2CMP, T2COUNT, T2ICR, T2CTL)) + ["print r4"]
                        + program([ST_H(11, T2ICR)], at=CODE + 0x100)
                        + program([LD_BU(4, T2ICR)], at=CODE + 0x200) + ["print r4"])
r4s = re.findall(r"print\s+r4\s*\n\s*(0x[0-9a-f]+)", t)
print("CONTROL alive=%s how=%s r4s=%s DECL=%d" % (alive, how, r4s, t.count(DECL)))
print("CONTROL_ARM=%s" % (r4s[0] if r4s else "absent"))
print("CONTROL_RB=%s" % (r4s[1] if len(r4s) > 1 else "absent"))
print("CONTROL_DONE")
