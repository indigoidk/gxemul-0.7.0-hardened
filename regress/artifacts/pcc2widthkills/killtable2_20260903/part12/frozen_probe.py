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
                each other, with the label and with the tested bits of idata (JOINT CELLS below), and relative_addr
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
                JOINT CELLS.  The rule (pass 10, the flagship seat; BOUNDED on pass 11 by the same
                seat against its own letter; CLAUDE.md clause (d)): a joint cell is ENUMERATED when
                the guarded body's own code distinguishes it, and the FLOOR -- the cells a row is
                OWED for -- is the cross-product of the guard's dominating predicates with the
                device-STATE lvalues the fix's own repair path reads that are jointly reachable
                through its own data flow.  Here that is {T2, T1} x {p1 = 0, > 0} x {p2 = 0, > 0}:
                one pcc_timer_tick callback increments both counts and reassert_interrupts reads
                both, so (p1, p2) is a joint input of the model.  EIGHT floor cells, every one held
                at a wide write: (T2, 0, 0) by `latch all' (0x0003) and `rb t2icr' (0xaab8), (T1, 0, 0) by `op t1icr dcl' (0x0303) and `rb t1icr' -- NOT `latch all', which iterates BLOCKS12 at 0x1a and never writes T1ICR (Opus, pass 11); (T1, >0, 0) `pend1 rb'; (T2, >0,
                0) `pend1 rb2'; (T2, 0, >0) `pend2 rb'; (T1, 0, >0) `pend2 rb1'; (T2, >0, >0)
                `pendboth rb'; (T1, >0, >0) `pendboth rb1'.  BEYOND THE FLOOR, HELD AS A GENERATING
                SET (grok, pass 11): the bits of the written idata that the body tests -- IEN (0x10),
                ICLR (0x08, a write strobe), the HUH? bits 0xe0 -- are single-operand MARGINALS of
                the value, not floor; yet at EVERY pending cell each is written both clear and set
                (0x0000; 0x0013; 0x0018; 0x0020 -- the `*i', `*c', `*h' readbacks, with a `huh' row
                per session as the HUH? print channel), so any single-axis extra conjunct on one of
                them at a pending cell lands a write and reds a readback (M_P2IEN, M_ICLR, M_HI,
                M_P1IEN).  The idle rows drive 0xaab8 (IEN|ICLR|INT|0x80) at both labels and 0x0003 / 0x0303, so the same
                holds at the (0, 0) cells.  DISCLOSED, with the derivation: multi-axis idata joints at
                a pending cell (`!(p2 && (idata & ICLR) && (idata & 0xe0))' and the like -- every held
                write sets at most one of the three); INT clear with a count pending -- UNREACHABLE on
                the model (the tick increments only under IEN and reassert sets INT before any guard
                runs; grok); pending counts >= 2 at once (the body tests `> 0' only; grok read OpenBSD's
                clock.c as arming COC on both timers -- not in this tree, NOT independently verified;
                the in-tree warrant is the model's joint handling); `idata == k' for any k no row
                drives; TxICR 0x37; TxCTL 0xff; the overflow count at 2-7 and 9-15.  Pass 9 held one
                floor cell; pass 10 the label mirror and its neighbours (Opus, codex); pass 11 found
                the ICLR x pending cell open (three seats, the Opus seat measured it) and the rule's
                letter over-demanding (its own author).  The De Morgan form of the original gap (kimi
                substitute): `!(p1 && p2)' is `p1 == 0 || p2 == 0' -- neither disjunct true of all its
                lvalue's held values, the disjunction true in every row, so a per-lvalue disclosure
                test could never fire on it.
                THE ENUMERATION ACROSS THE ARMS (pass 11 batch two; the class-closure amendment: three
                passes found one class -- an unvaried axis crossed with a varied one -- so the repair
                owes the enumeration, not another cell).  Read off each guarded write body, the axes its
                code makes DECISIVE (tested in an `if', or used as an index), and what the rows hold:
                  GENCTL, VECBASE, SCCICR, SCCTX, SCCRX, SCSIICR, SCCERR, PSCALEADJ, MASK -- stores,
                     masks or a print with NO `if' on state or idata: no axis beyond the label; the
                     plain rows hold every label.  (Their callee reassert_interrupts tests C040/MIEN --
                     out of the closure: non-transitive.)
                  IPL -- one function-static latch `w': held clear (`ipl noig2') and set (`ipl wset').
                  TxCTL -- the label (an RMW index), the register's overflow-count class {0, 1, >= 8,
                     0xfc-via-memcpy} and two tested idata bits, COVF (`if (idata & PCC2_TCTL_COVF)')
                     and the HUH? bits (`if (idata & ~7)').  Generating set: in the four overflow
                     sessions COVF-set (0x0004) and HUH?-bit-set (0x0008) writes at the ARMED label,
                     then the IDLE label preset to 0x02 (COC without CEN) with 0x0000 / 0x0004 /
                     0x0008 -- the `ovf* rbv/rbx/rb1/rb1v/rb1x' and `ovf1/ovfhi1 rb2*' readbacks and an
                     `ovf* huh' row per session.  Landed values never equal a preset: count 1 -> 0x00
                     (COVF clears the count and itself) / 0x10 (+ HUH?); count >= 8 -> 0x00 / 0x80
                     masked; idle 0x02 -> 0x00.  Disclosed: COVF at the 0xfc cell (rests on the filed
                     pcc2counter8 path) and at the plain 0x03 cell (a preset of 0x03 would start the
                     idle timer); the HUH? bits are held at the plain cell by 0xaab8 (lane 0xb8).
                  TxICR -- passes 9 to 11 above.
                A future arm added to the guard set owes this paragraph one line before its rows.
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


print("pcc2widthkills DETECTOR -- binary=%s label=%s" % (BIN, LABEL))
print("%-16s %-12s %-12s %-46s %s" % ("row", "got", "want", "note", ""))

# ------------------------------------------------------------------ controls
t, alive, how = session(setup() + program([I_ST_SCR, I_LD_SCR]) + ["print r4"])
row("live", printed(t, "r4") if alive else "died", "0x5a5a5a5a",
    "RAM word round-trips through the same decode")
t, alive, how = session(setup() + program([ST_B(5, CHIPID)]))
row("devsig", t.count(DEVSIG), 1, "a byte write to CHIPID makes the DEVICE speak")
t, alive, how = session(setup() + program([I_ST_SCR, LD_B(4, GENCTL), I_LD_SCR]) + ["print r4"])
row("byte rd", how, "exit0", "ld.b GENCTL: the legal width, serviced on both builds")
row("byte rd liv", printed(t, "r4") if alive else "died", "0x5a5a5a5a", "...and runs on")

# --------------------------------------- survival pairs at the five reachable blocks
#  Each kill row is PAIRED with a positive post-access observable.
for nm, off in (("genctl", GENCTL), ("t2ctl", T2CTL), ("t2icr", T2ICR),
                ("sccerr", SCCERR), ("scctx", SCCTX)):
    t, alive, how = session(setup() + program([I_ST_SCR, LD_H(4, off), I_LD_SCR]) + ["print r4"])
    row("hrd " + nm, how, "exit0", "ld.h %s (aligned halfword READ) survives" % nm.upper())
    row("hrd %s lv" % nm, printed(t, "r4") if alive else "died", "0x5a5a5a5a", "...and runs on")
    row("hrd %s nod" % nm, t.count(DECL), 0,
        "...and a wide READ is never declined (the direction split's own conjunct)")
    #  r6 = the halfword to store: both lanes keep GENCTL's bit 0x04 CLEAR (pcc2c040kill)
    t, alive, how = session(setup(r6="0xaabb") + program([I_ST_SCR, ST_H(6, off), I_LD_SCR]) + ["print r4"])
    row("hwr " + nm, how, "exit0", "st.h %s (aligned halfword WRITE) survives" % nm.upper())
    row("hwr %s lv" % nm, printed(t, "r4") if alive else "died", "0x5a5a5a5a", "...and runs on")
#  SCCERR is the one 4-aligned block: word read AND write
t, alive, how = session(setup() + program([I_ST_SCR, LD_W(4, SCCERR), I_LD_SCR]) + ["print r4"])
row("wrd sccerr", how, "exit0", "ld SCCERR (the one 4-aligned block) survives")
row("wrd sccerr lv", printed(t, "r4") if alive else "died", "0x5a5a5a5a", "...and runs on")
row("wrd sccerr nod", t.count(DECL), 0, "...and the word READ is never declined")
t, alive, how = session(setup(r6="0x00000000") + program([I_ST_SCR, ST_W(6, SCCERR), I_LD_SCR]) + ["print r4"])
row("wwr sccerr", how, "exit0", "st SCCERR (word WRITE) survives")
row("wwr sccerr lv", printed(t, "r4") if alive else "died", "0x5a5a5a5a", "...and runs on")
#  SCCERR's arm always stores 0, so decline and accept are VALUE-identical there: the
#  only channel that varies is the announcement.
row("wwr sccerr dcl", t.count("write to PCCTWO_SCCERR " + DECL), 1,
    "...and it was DECLINED once -- the message is the only channel here")

# ---------------------------------------------------------- VALUE rows (reads)
#  A wide read must compose the lanes in ADDRESS order.  VECBASE's arm masks & 0xf0
#  and GENCTL's stores the byte, so the halfword at 0x02 is GENCTL<<8 | VECBASE.
#  0x82 keeps bit 0x04 clear.
t, alive, how = session(setup(r5="0x82", r6="0x50")
                        + program([ST_B(5, GENCTL), ST_B(6, VECBASE), LD_HU(4, GENCTL)]) + ["print r4"])
row("val h genctl", printed(t, "r4") if alive else "died", "0x8250",
    "ld.h at GENCTL composes GENCTL:VECBASE in address order -- kills lane-order / zero-fill")
#  word at SCCERR: SCCERR always 0; SCCICR & 0x1f; SCCTX & 0x1f; SCCRX & 0xdf.
t, alive, how = session(setup(r5="0x15", r6="0x1f")
                        + program([ST_B(5, SCCICR), ST_B(6, SCCTX), ST_B(6, SCCRX), LD_W(4, SCCERR)]) + ["print r4"])
row("val w sccerr", printed(t, "r4") if alive else "died", "0x151f1f",
    "ld at SCCERR composes 00:SCCICR:SCCTX:SCCRX -- four lanes, right order")

# ------------------------------------------------ READBACK rows (the DELETE killer)
#  After a declined st.h 0xAABB to GENCTL, BOTH lanes must be unchanged.  Under a bare
#  deletion GENCTL reads 0xBB (the neighbour's lane); under an accidental compose it
#  reads 0xAA and VECBASE 0xB0.  Both lanes of 0xAABB keep bit 0x04 clear.
t, alive, how = session(setup(r5="0x82", r6="0xaabb")
                        + program([ST_B(5, GENCTL), ST_H(6, GENCTL), LD_BU(4, GENCTL)]) + ["print r4"])
row("rb genctl", printed(t, "r4") if alive else "died", "0x82",
    "GENCTL unchanged after a declined st.h -- kills DELETE (0xbb) and compose (0xaa)")
row("rb genctl dcl", t.count("write to PCCTWO_GENCTL " + DECL), 1,
    "...and the decline was announced ONCE")
t, alive, how = session(setup(r5="0x50", r6="0xaabb")
                        + program([ST_B(5, VECBASE), ST_H(6, GENCTL), LD_BU(4, VECBASE)]) + ["print r4"])
row("rb vecbase", printed(t, "r4") if alive else "died", "0x50",
    "VECBASE unchanged too -- the second lane of the declined halfword")

# ---------------------------- per-arm channels (pass 2: sibling parity, arm by arm)
#  A seat pointed out that only GENCTL had a readback: every other reachable arm's
#  halfword-write row checked SURVIVAL alone, so a guard edited at ONE arm (`len > 2',
#  or the guard deleted, at T2ICR only) left every row green.  Each arm now has its own
#  channel, with a lane value its own mask turns into a different byte when it lands.
for nm, off, pre, landed in (("t2ctl", T2CTL, "0x03", "0x3"), ("t2icr", T2ICR, "0x13", "0x13"),
                             ("scctx", SCCTX, "0x1f", "0x1f")):
    t, alive, how = session(setup(r5=pre, r6="0xaab8")
                            + program([ST_B(5, off), ST_H(6, off), LD_BU(4, off)]) + ["print r4"])
    row("rb " + nm, printed(t, "r4") if alive else "died", landed,
        "%s unchanged after a declined st.h -- kills a guard edited at THIS arm" % nm.upper())
    row("rb %s dcl" % nm, t.count("write to PCCTWO_%s " % ("TxCTL" if nm == "t2ctl" else "TxICR" if nm == "t2icr" else "SCCTX") + DECL), 1,
        "...announced once at this arm")
t, alive, how = session(setup(r6="0xaab8") + program([ST_H(6, SCCERR)]))
row("hwr sccerr dcl", t.count("write to PCCTWO_SCCERR " + DECL), 1,
    "halfword write to SCCERR declined once -- value-identical arm, message channel")

#  PRE-TABLE BLOCK yield (section 1, guard field vs body field): the guard reads the access
#  SHAPE (len) and the guarded body reads the VALUE (idata).  An operand swap to a value
#  test -- `idata > 0xff', a plausible "does it fit a byte" reading -- accepts a halfword
#  write whose value fits, and big-endian 0x0022 then stores 0x22, the NEIGHBOUR's lane,
#  into GENCTL: the original defect, behind a guard that still reads like a width check.
#  Every other wide-write row used a value above 0xff, so all 77 were green under it BY
#  CONSTRUCTION.  Written before the repair table ran; the table says whether it kills.
t, alive, how = session(setup(r5="0x11", r6="0x0022")
                        + program([ST_B(5, GENCTL), ST_H(6, GENCTL), LD_BU(4, GENCTL)]) + ["print r4"])
row("rb genctl lo", printed(t, "r4") if alive else "died", "0x11",
    "st.h of a value that FITS a byte is still declined -- the guard is on len, not idata")

# ------------------------- latch CARDINALITY (pass 2, the measuring seat's class closer)
#  `latch same' and `latch two' pin ONE pair out of 66: every other session writes at most
#  one BLOCK, so a bit shared by any other pair announces normally and no row moves.
#  MEASURED by the builder: aliasing SCCTX onto SCCRX's bit -- a ONE-CHARACTER edit --
#  left the 60-row detector at 60/60.  ONE OFFSET PER BLOCK: TxCTL serves T1CTL+T2CTL
#  and TxICR serves T1ICR+T2ICR, so twelve LABELS would give only ten announces -- the
#  same units slip that let "five even blocks + seven odd ones = twelve" read as all
#  twelve blocks.  This row pins the CARDINALITY of the latch: any collision anywhere in
#  the 12-bit space drops the count.  (Operator path for all twelve, so the odd ones are
#  reachable; the guest-reachable halves have their own rows above.)
BLOCKS12 = (("GENCTL", 0x02), ("VECBASE", 0x03), ("PSCALEADJ", 0x15), ("TxCTL", 0x16),
            ("TxICR", 0x1a), ("SCCERR", 0x1c), ("SCCICR", 0x1d), ("SCCTX", 0x1e),
            ("SCCRX", 0x1f), ("SCSIICR", 0x2f), ("IPL", 0x3e), ("MASK", 0x3f))
#  VALUE 0x0003, not 0x0303: it fits a byte, so this row ALSO reds if any arm swaps its
#  guard operand from len to a value test (see `rb genctl lo').  On the fix the value
#  never lands, so the expectation is value-independent.
t, alive, how = session(["put h 0x%x, 0x0003" % (PCC2 + o) for _, o in BLOCKS12])
row("latch all", t.count(DECL), 12,
    "one wide write per BLOCK -> TWELVE announces: bit CARDINALITY, not one pair")
row("latch all lv", how, "exit0", "...and the host survived all twelve blocks")
#  PASS 5 (fable5, MEASURED): `break' -> `return 0' at an OPERATOR-only block is a total escape
#  of the rows above -- the announce precedes the return, the body is skipped either way,
#  and a failed debugger put does not threaten the host.  What the pty DOES carry is
#  memory_rw's own line, "[ writing to device 'pcc2' addr ... failed ]", once per block
#  whose guard returned 0.  Counted at ZERO over this session, it pins the FAULT member at
#  all twelve blocks with no new session.  (At the six guest-reachable blocks the guest's
#  own store faults and the hwr/lv pair reds as well -- part 4, M_RET0_GENCTL.)
row("latch all fail", t.count("failed ]"), 0,
    "twelve declined wide writes, ZERO device-write failures: DECLINE, not FAULT, at every block")

# ------------------------------------------------------------------ latch rows
t, alive, how = session(setup(r6="0xaabb") + program([ST_H(6, GENCTL), ST_H(6, GENCTL)]))
row("latch same", t.count("write to PCCTWO_GENCTL " + DECL), 1,
    "same block twice -> ONE announce -- kills a dropped |= (flood)")
t, alive, how = session(setup(r6="0x0303") + program([ST_H(6, GENCTL), ST_H(6, T2CTL)]))
row("latch two", t.count(DECL), 2,
    "two blocks -> TWO announces -- kills a bit shared across blocks")
#  PASS 4 (glm, kimi, codex): `latch same' sees only CONSECUTIVE repeats, so `|=' -> `=' in the
#  helper -- the field ASSIGNED instead of accumulated, one character -- passed every row: A
#  then B clears A's bit, and nothing wrote A again afterwards.  Interleave: A, B, A -> TWO.
t, alive, how = session(setup(r6="0x0303") + program([ST_H(6, GENCTL)])
                        + ["put h 0x%x, 0x0303" % (PCC2 + VECBASE)]
                        + program([ST_H(6, GENCTL)], at=CODE + 0x100))
row("latch aba", t.count(DECL), 2,
    "A, B, A -> TWO announces: the latch ACCUMULATES (an assignment would give three)")
#  PASS 4 (minimax): `(1u << bit)' -> `1' in the SET line latches bit 0 for every block, so
#  every block but GENCTL announces on every write.  `latch same' is at GENCTL (bit 0) and
#  stays green.  The same test at a non-zero bit:
t, alive, how = session(["put h 0x%x, 0x0303" % (PCC2 + MASK)] * 2)
row("latch same2", t.count("write to PCCTWO_MASK " + DECL), 1,
    "MASK (bit 11) twice -> ONE announce: the SET line names the block's own bit")

# ------------- PASS 5: the guard reading the FIX'S OWN STATE (MEASURED 101/101 by the Opus seat)
#  `if (len != 1 && writeflag == MEM_WRITE && !(d->warned & (1u << bit)))' -- the canonical
#  clause-(d) "condition qualified" form, at one arm or at all twelve -- swept every row above:
#  the FIRST wide write is declined and announced exactly as before, and the SECOND lands the
#  neighbour's lane.  `latch same' does two wide writes and reads only the count; every `rb'
#  row reads back after exactly ONE.  No row ever observed the device at a decision point with
#  its latch already set.  So, at every block: set a byte, write wide TWICE, then read back
#  (or count the body's own print where the body stores nothing).  Even blocks by guest st.h,
#  odd blocks by the operator's put h.  SCCERR stores 0 and is value-identical (E, disclosed).
for nm, off, pre, want, guest in (("genctl", GENCTL, "0x82", "0x82", True), ("t2ctl", T2CTL, "0x03", "0x3", True),
                                  ("t2icr", T2ICR, "0x13", "0x13", True), ("scctx", SCCTX, "0x1f", "0x1f", True),
                                  ("vecbase", VECBASE, "0x50", "0x50", False), ("sccicr", SCCICR, "0x1f", "0x1f", False),
                                  ("sccrx", SCCRX, "0x1f", "0x1f", False), ("scsiicr", SCSIICR, "0x1f", "0x1f", False),
                                  ("mask", MASK, "0x12", "0x12", False)):
    if guest:
        t, alive, how = session(setup(r5=pre, r6="0xaab8") + program([ST_B(5, off), ST_H(6, off), ST_H(6, off), LD_BU(4, off)])
                                + ["print r4"])
    else:
        t, alive, how = session(setup(r5=pre) + program([ST_B(5, off)])
                                + ["put h 0x%x, 0xaab8" % (PCC2 + off)] * 2
                                + program([LD_BU(4, off)], at=CODE + 0x100) + ["print r4"])
    row("rb2 " + nm, printed(t, "r4") if alive else "died", want,
        "%s unchanged after TWO declined wide writes -- the second is refused with the latch SET" % nm.upper())
t, alive, how = session(["put h 0x%x, 0x0303" % (PCC2 + PSCALEADJ)] * 2)
row("pscale noig2", t.count("PSCALEADJ ignored"), 0,
    "two declined wide writes never reach the 'ignored' print -- the second one would, unlatched")
t, alive, how = session(setup(r6="0x0303") + program([ST_H(6, IPL), ST_H(6, IPL)]))
row("ipl noig2", t.count("write to read-only PCCTWO_IPL"), 0,
    "two declined st.h to IPL never reach the read-only print -- the second one would, unlatched")

#  And the wide READ that now falls through to each arm's SECOND predicate, `if (writeflag ==
#  MEM_WRITE)' (the pre-fix guard killed reads before it was reached; the Opus seat flagged it).
#  Delete that predicate at an even block and a wide READ stores idata == 0 into the register.
for nm, off, pre, want in (("genctl", GENCTL, "0x82", "0x82"), ("t2ctl", T2CTL, "0x03", "0x3"),
                           ("t2icr", T2ICR, "0x13", "0x13"), ("scctx", SCCTX, "0x1f", "0x1f")):
    t, alive, how = session(setup(r5=pre) + program([ST_B(5, off), LD_H(4, off), LD_BU(4, off)]) + ["print r4"])
    row("hrd %s rb" % nm, printed(t, "r4") if alive else "died", want,
        "%s unchanged after a wide READ -- the arm's write-side body must not run on a read" % nm.upper())
t, alive, how = session(setup() + program([I_ST_SCR, LD_H(4, IPL), I_LD_SCR]))
row("hrd ipl noro", t.count("write to read-only PCCTWO_IPL"), 0,
    "a wide READ of IPL never reaches the write body's read-only print")

#  PASS 6 (grok named it; both Agent seats measured the neighbouring cells): BYTE reads reach
#  EVERY arm -- the six odd blocks too, since a byte access skips the alignment check -- and
#  fall through the width guard to the arm's second predicate.  Delete it at a storing block
#  and a byte READ stores idata == 0; the readback in the same instruction stream is served by
#  the memcpy before the switch and still prints the old value.  So: set a byte, read it, read
#  it AGAIN.  Guest path at every block, even and odd alike.
for nm, off, pre, want in (("genctl", GENCTL, "0x82", "0x82"), ("vecbase", VECBASE, "0x50", "0x50"),
                           ("t2ctl", T2CTL, "0x03", "0x3"), ("t2icr", T2ICR, "0x13", "0x13"),
                           ("sccicr", SCCICR, "0x1f", "0x1f"), ("scctx", SCCTX, "0x1f", "0x1f"),
                           ("sccrx", SCCRX, "0x1f", "0x1f"), ("scsiicr", SCSIICR, "0x1f", "0x1f"),
                           ("mask", MASK, "0x12", "0x12")):
    t, alive, how = session(setup(r5=pre) + program([ST_B(5, off), LD_BU(4, off), LD_BU(4, off)]) + ["print r4"])
    row("brd2 " + nm, printed(t, "r4") if alive else "died", want,
        "%s unchanged after TWO byte READS -- the arm's write body must not run on a byte read" % nm.upper())
t, alive, how = session(setup() + program([LD_BU(4, PSCALEADJ), LD_BU(4, PSCALEADJ)]))
row("brd pscale noig", t.count("PSCALEADJ ignored"), 0, "byte READS of PSCALEADJ never reach the write body's print")
t, alive, how = session(setup() + program([LD_BU(4, IPL), LD_BU(4, IPL)]))
row("brd ipl noro", t.count("write to read-only PCCTWO_IPL"), 0, "byte READS of IPL never reach the write body's read-only print")

def c040ok(v):
    #  pass 8 (Opus F16): a value whose landing lane carries PCC2_C040 (0x04) would kill the
    #  host through reassert_interrupts() instead of landing -- the row would still red, by
    #  death, and the NOROW line below would be false.  Refuse such a lane at authoring time.
    assert (int(v, 16) & 0xff) & 0x04 == 0, "GENCTL lane %s carries PCC2_C040" % v
    return v
#  PASS 6, the LANDING channel at len 4 and len 8 (Opus seat, M1_W4FALL_ALL: `break;' ->
#  `if (len < 4) break;' at all twelve scored 118/118).  `latch all w' and `latch all d' count
#  the ANNOUNCE; nothing read the register back after a 4- or 8-byte write, so a guard that
#  announces and then lets the wide value land was invisible.  One readback per storing block
#  per width; the two print-only bodies counted at zero; SCCERR is E.
for nm, off, pre, want in (("genctl", GENCTL, "0x82", "0x82"), ("vecbase", VECBASE, "0x50", "0x50"),
                           ("t2ctl", T2CTL, "0x03", "0x3"), ("t2icr", T2ICR, "0x13", "0x13"),
                           ("sccicr", SCCICR, "0x1f", "0x1f"), ("scctx", SCCTX, "0x1f", "0x1f"),
                           ("sccrx", SCCRX, "0x1f", "0x1f"), ("scsiicr", SCSIICR, "0x1f", "0x1f"),
                           ("mask", MASK, "0x12", "0x12")):
    #  pass 7 (Opus seat, measured in part6b/M_W4FALL_ALL.out): at GENCTL the lanes 0xdd and
    #  0x44 carry bit 0x04 = PCC2_C040, so a LANDED write there ends the host (pcc2c040kill)
    #  and the row killed by death, not by value.  GENCTL gets lanes with bit 2 clear.
    w4 = c040ok("0xaab8ccd9") if off == GENCTL else "0xaab8ccdd"
    w8 = c040ok("0xaab8ccdd00112240") if off == GENCTL else "0xaab8ccdd00112244"
    t, alive, how = session(setup(r5=pre) + program([ST_B(5, off)]) + ["put w 0x%x, %s" % (PCC2 + off, w4)]
                            + program([LD_BU(4, off)], at=CODE + 0x100) + ["print r4"])
    row("rb4 " + nm, printed(t, "r4") if alive else "died", want,
        "%s unchanged after a declined 4-byte write -- the refusal, not the announce" % nm.upper())
    t, alive, how = session(setup(r5=pre) + program([ST_B(5, off)]) + ["put d 0x%x, %s" % (PCC2 + off, w8)]
                            + program([LD_BU(4, off)], at=CODE + 0x100) + ["print r4"])
    row("rb8 " + nm, printed(t, "r4") if alive else "died", want,
        "%s unchanged after a declined 8-byte write" % nm.upper())
t, alive, how = session(["put w 0x%x, 0xaab8ccdd" % (PCC2 + PSCALEADJ)])
row("pscale noig4", t.count("PSCALEADJ ignored"), 0, "a declined 4-byte write never reaches the PSCALEADJ print")
t, alive, how = session(["put d 0x%x, 0xaab8ccdd00112244" % (PCC2 + PSCALEADJ)])
row("pscale noig8", t.count("PSCALEADJ ignored"), 0, "a declined 8-byte write never reaches the PSCALEADJ print")
t, alive, how = session(["put w 0x%x, 0xaab8ccdd" % (PCC2 + IPL)])
row("ipl noig4", t.count("write to read-only PCCTWO_IPL"), 0, "a declined 4-byte write never reaches the IPL print")
t, alive, how = session(["put d 0x%x, 0xaab8ccdd00112244" % (PCC2 + IPL)])
row("ipl noig8", t.count("write to read-only PCCTWO_IPL"), 0, "a declined 8-byte write never reaches the IPL print")
t, alive, how = session(["put w 0x%x, 0xaab8ccdd" % (PCC2 + MASK)] * 2)
row("latch samew", t.count(DECL), 1, "two 4-byte writes to MASK announce ONCE -- the latch is not keyed by width")
t, alive, how = session(["put d 0x%x, 0xaab8ccdd00112244" % (PCC2 + MASK)] * 2)
row("latch samed", t.count(DECL), 1, "two 8-byte writes to MASK announce ONCE")
#  pass 7 (Opus seat): a value-test QUALIFIER `&& idata != 1' on the guard lets wide writes of
#  the value 1 land, and no row wide-wrote that value -- every value-test guard is caught only
#  for the values rows drive.  (The bare SWAP `len != 1' -> `idata != 1' drops the length test
#  and is killed by every byte preset: MEASURED 95/171 in part 7.)  Twelve 2-byte writes of
#  0x0001: any arm whose guard exempts that value lands one.
t, alive, how = session(["put h 0x%x, 0x0001" % (PCC2 + o) for _, o in BLOCKS12])
row("latch all one", t.count(DECL), 12, "twelve 2-byte writes of the VALUE 1 -- an `idata != 1' guard lands one and drops the count")

#  PASS 6, the fix's guard qualified by a TIMER PENDING COUNT (both Agent seats measured it:
#  `&& !d->pending_timer2_interrupts' and `&& d->pending_timer1_interrupts == 0' at the TxICR
#  guard each scored 118/118).  pending_timer* is INCREMENTED only by pcc_timer_tick, a
#  timer_add/SIGALRM callback -- which debugger.c stops for the whole of every `step' -- so no
#  stepping row can ever hold it non-zero.  These rows ARM a timer (compare 1, count 0, IEN,
#  CEN) and FREE-RUN to a breakpoint: the guest polls TxICR with `bb0 5, r4, -1' until
#  reassert_interrupts() sets the INT bit, which happens ONLY under pending > 0 -- so the 0x31
#  read after the loop is both the liveness control (the loop exited) and the device signature
#  (a mis-encoded bb0 would read 0x11).  Then the wide write, with the count non-zero.
T1CMP, T1COUNT, T2CMP, T2COUNT = 0x04, 0x08, 0x0c, 0x10
def BB0(b5, rs, d16): return enc(0x34, b5, rs, d16)      # bb0 b5, rs, d16 (word displacement)
def program_free(insns, at=CODE):
    words = list(insns) + [I_BR_SELF, 0]
    cmds = ["put w 0x%x, 0x%08x" % (at + 4 * i, w) for i, w in enumerate(words)]
    return cmds + ["pc=0x%x" % at, "breakpoint add 0x%x" % (at + 4 * len(insns)), ("continue", 20.0, "BREAKPOINT")]
def pend_arm(cmp_off, cnt_off, icr_off, ctl_off):
    return [ST_W(5, cmp_off), ST_W(6, cnt_off), ST_B(7, icr_off), ST_B(8, ctl_off), LD_BU(4, icr_off), BB0(5, 4, -1)]
PEND_REGS = ["r5=0x1", "r6=0x0", "r7=0x11", "r8=0x1", "r9=0x0", "r10=0x13", "r11=0x18", "r12=0x20"]   # r10/r11/r12: the IEN-set, ICLR-set and HUH-bit wide-write values (passes 10, 11)
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
t, alive, how = session(setup() + PEND_REGS + program_free(pend_arm(T2CMP, T2COUNT, T2ICR, T2CTL)) + ["print r4"]
                        + program([ST_H(9, T2ICR)], at=CODE + 0x100) + program([LD_BU(4, T2ICR)], at=CODE + 0x200) + ["print r4"]
                        #  pass 10: the (label, p1, p2, idata & IEN) product -- IEN set at T2, then the T1 label with timer 1 idle
                        + program([ST_H(10, T2ICR)], at=CODE + 0x300) + program([LD_BU(4, T2ICR)], at=CODE + 0x400) + ["print r4"]
                        + program([ST_B(7, T1ICR)], at=CODE + 0x500) + ["put h 0x%x, 0x0000" % (PCC2 + T1ICR)]
                        + program([LD_BU(4, T1ICR)], at=CODE + 0x600) + ["print r4", "put h 0x%x, 0x0013" % (PCC2 + T1ICR)]
                        + program([LD_BU(4, T1ICR)], at=CODE + 0x700) + ["print r4"]
                        #  pass 11: the ICLR and HUH-bit generating writes at both labels (appended: the indices above stay)
                        + program([ST_H(11, T2ICR)], at=CODE + 0x800) + program([LD_BU(4, T2ICR)], at=CODE + 0x900) + ["print r4"]
                        + program([ST_H(12, T2ICR)], at=CODE + 0xa00) + program([LD_BU(4, T2ICR)], at=CODE + 0xb00) + ["print r4",
                           "put h 0x%x, 0x0018" % (PCC2 + T1ICR)] + program([LD_BU(4, T1ICR)], at=CODE + 0xc00) + ["print r4",
                           "put h 0x%x, 0x0020" % (PCC2 + T1ICR)] + program([LD_BU(4, T1ICR)], at=CODE + 0xd00) + ["print r4"])
r4s = re.findall(r"print\s+r4\s*\n\s*(0x[0-9a-f]+)", t)
row("pend2 arm", armval(t, alive, r4s), "0x31",
    "timer 2 pending: INT|IEN|IL1 after the poll loop -- the state pass 6 found unreached")
row("pend2 decl", cval(alive, how, t.count(DECL)), 1, "timer 2 PENDING: the first of four wide writes (T2ICR guest 0x0000) is announced; the announce is latched once per block, the readbacks are the per-write channel")
row("pend2 rb", cval(alive, how, ("0x%x" % int(r4s[1], 16)) if alive and len(r4s) > 1 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x31",
    "T2ICR unchanged -- a `&& !pending_timer2' guard would land 0x20 and drop the pending count")
row("pend2 rbi", cval(alive, how, ("0x%x" % int(r4s[2], 16)) if alive and len(r4s) > 2 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x31",
    "T2ICR unchanged after an IEN-set (0x0013) wide write with timer 2 pending -- `&& !(p2 && (idata & IEN))' would land 0x33")
row("pend2 rb1", cval(alive, how, ("0x%x" % int(r4s[3], 16)) if alive and len(r4s) > 3 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x11",
    "T1ICR (preset IEN|IL1, timer 1 idle) unchanged with timer 2 pending -- `&& !(p2 && relative_addr == T1ICR)' (pass 10) would land 0x00")
row("pend2 rb1i", cval(alive, how, ("0x%x" % int(r4s[4], 16)) if alive and len(r4s) > 4 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x11",
    "T1ICR unchanged after the IEN-set write there -- the (T1, 0, >0, IEN) cell; a landed write reads 0x13")
row("pend2 rbc", cval(alive, how, ("0x%x" % int(r4s[5], 16)) if alive and len(r4s) > 5 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x31",
    "T2ICR unchanged after an ICLR-set (0x0018) guest write with timer 2 pending -- `&& !(p2 && (idata & ICLR))' (pass 11, measured) would land 0x10")
row("pend2 rbh", cval(alive, how, ("0x%x" % int(r4s[6], 16)) if alive and len(r4s) > 6 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x31",
    "T2ICR unchanged after a HUH-bit (0x0020) guest write with timer 2 pending -- `&& !(p2 && (idata & 0xe0))' would land 0x20")
row("pend2 rb1c", cval(alive, how, ("0x%x" % int(r4s[7], 16)) if alive and len(r4s) > 7 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x11",
    "T1ICR (idle) unchanged after an ICLR-set operator write with timer 2 pending -- a landed write reads 0x10")
row("pend2 rb1h", cval(alive, how, ("0x%x" % int(r4s[8], 16)) if alive and len(r4s) > 8 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x11",
    "T1ICR (idle) unchanged after a HUH-bit operator write with timer 2 pending -- a landed write reads 0x00")
row("pend2 huh", cval(alive, how, t.count("HUH? write to PCCTWO_TxICR")), 0, "no HUH? line: every 0x0020 wide write in this session was declined before the body could print it")
t, alive, how = session(setup() + PEND_REGS + program_free(pend_arm(T1CMP, T1COUNT, T1ICR, T1CTL)) + ["print r4",
                        "put h 0x%x, 0x0000" % (PCC2 + T1ICR)] + program([LD_BU(4, T1ICR)], at=CODE + 0x200) + ["print r4",
                        #  pass 10: the (label, p1, p2, idata & IEN) product -- IEN set at T1, then the T2 label with timer 2 idle
                        "put h 0x%x, 0x0013" % (PCC2 + T1ICR)] + program([LD_BU(4, T1ICR)], at=CODE + 0x300) + ["print r4"]
                        + program([ST_B(7, T2ICR), ST_H(9, T2ICR)], at=CODE + 0x400) + program([LD_BU(4, T2ICR)], at=CODE + 0x500) + ["print r4"]
                        + program([ST_H(10, T2ICR)], at=CODE + 0x600) + program([LD_BU(4, T2ICR)], at=CODE + 0x700) + ["print r4",
                        #  pass 11: the ICLR and HUH-bit generating writes at both labels (appended)
                        "put h 0x%x, 0x0018" % (PCC2 + T1ICR)] + program([LD_BU(4, T1ICR)], at=CODE + 0x800) + ["print r4",
                        "put h 0x%x, 0x0020" % (PCC2 + T1ICR)] + program([LD_BU(4, T1ICR)], at=CODE + 0x900) + ["print r4"]
                        + program([ST_H(11, T2ICR)], at=CODE + 0xa00) + program([LD_BU(4, T2ICR)], at=CODE + 0xb00) + ["print r4"]
                        + program([ST_H(12, T2ICR)], at=CODE + 0xc00) + program([LD_BU(4, T2ICR)], at=CODE + 0xd00) + ["print r4"])
r4s = re.findall(r"print\s+r4\s*\n\s*(0x[0-9a-f]+)", t)
row("pend1 arm", armval(t, alive, r4s), "0x31",
    "timer 1 pending: INT|IEN|IL1 after the poll loop")
row("pend1 decl", cval(alive, how, t.count(DECL)), 1, "timer 1 PENDING: the first of four wide writes (T1ICR operator 0x0000) is announced; latched once per block, the readbacks are the per-write channel")
row("pend1 rb", cval(alive, how, ("0x%x" % int(r4s[1], 16)) if alive and len(r4s) > 1 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x31",
    "T1ICR unchanged -- a `&& pending_timer1 == 0' guard would land 0x20")
row("pend1 rbi", cval(alive, how, ("0x%x" % int(r4s[2], 16)) if alive and len(r4s) > 2 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x31",
    "T1ICR unchanged after an IEN-set (0x0013) operator wide write with timer 1 pending -- a landed write reads 0x33")
row("pend1 rb2", cval(alive, how, ("0x%x" % int(r4s[3], 16)) if alive and len(r4s) > 3 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x11",
    "T2ICR (preset IEN|IL1, timer 2 idle) unchanged with timer 1 pending -- `&& !(p1 && !p2 && relative_addr == T2ICR)' would land 0x00")
row("pend1 rb2i", cval(alive, how, ("0x%x" % int(r4s[4], 16)) if alive and len(r4s) > 4 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x11",
    "T2ICR unchanged after the IEN-set guest write there -- the (T2, >0, 0, IEN) cell; a landed write reads 0x13")
row("pend1 rbc", cval(alive, how, ("0x%x" % int(r4s[5], 16)) if alive and len(r4s) > 5 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x31",
    "T1ICR unchanged after an ICLR-set (0x0018) operator write with timer 1 pending -- a landed write reads 0x10")
row("pend1 rbh", cval(alive, how, ("0x%x" % int(r4s[6], 16)) if alive and len(r4s) > 6 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x31",
    "T1ICR unchanged after a HUH-bit (0x0020) operator write with timer 1 pending -- a landed write reads 0x20")
row("pend1 rb2c", cval(alive, how, ("0x%x" % int(r4s[7], 16)) if alive and len(r4s) > 7 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x11",
    "T2ICR (idle) unchanged after an ICLR-set guest write with timer 1 pending -- a landed write reads 0x10")
row("pend1 rb2h", cval(alive, how, ("0x%x" % int(r4s[8], 16)) if alive and len(r4s) > 8 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x11",
    "T2ICR (idle) unchanged after a HUH-bit guest write with timer 1 pending -- a landed write reads 0x00")
row("pend1 huh", cval(alive, how, t.count("HUH? write to PCCTWO_TxICR")), 0, "no HUH? line: every 0x0020 wide write in this session was declined")

#  PASS 7 (codex): the TxCTL body is an RMW that PRESERVES the byte's upper nibble -- the
#  overflow count, set ONLY by pcc_timer_tick when the counter crosses 2^31 -- and every TxCTL
#  preset had that nibble zero, so `&& !(d->pcctwo_reg[relative_addr] & PCC2_TCTL_OVF)' on the
#  TxCTL guard was invisible.  Same shape as pend*: count near 2^31, CEN, free-run polling bit 4
#  (0x10, the overflow count's LSB, which no guest write can set), then the wide write.
def ovf_arm(cnt_off, ctl_off):
    return [ST_W(6, cnt_off), ST_B(8, ctl_off), LD_BU(4, ctl_off), BB0(4, 4, -1)]
OVF_REGS = ["r6=0x7fffff00", "r8=0x1", "r9=0x0", "r13=0x4", "r14=0x8", "r15=0x2"]   # r13 COVF, r14 a HUH? bit, r15 the idle label's preset (COC, no CEN) -- pass 11 batch two
t, alive, how = session(setup() + OVF_REGS + program_free(ovf_arm(T2COUNT, T2CTL)) + ["print r4"]
                        + program([ST_H(9, T2CTL)], at=CODE + 0x100) + program([LD_BU(4, T2CTL)], at=CODE + 0x200) + ["print r4"]
                        #  pass 11 batch two: the TxCTL generating set -- COVF and a HUH? bit at the armed label, then the idle label (preset COC)
                        + program([ST_H(13, T2CTL)], at=CODE + 0x300) + program([LD_BU(4, T2CTL)], at=CODE + 0x400) + ["print r4"]
                        + program([ST_H(14, T2CTL)], at=CODE + 0x500) + program([LD_BU(4, T2CTL)], at=CODE + 0x600) + ["print r4"]
                        + program([ST_B(15, T1CTL)], at=CODE + 0x700) + ["put h 0x%x, 0x0000" % (PCC2 + T1CTL)] + program([LD_BU(4, T1CTL)], at=CODE + 0x800) + ["print r4",
                           "put h 0x%x, 0x0004" % (PCC2 + T1CTL)] + program([LD_BU(4, T1CTL)], at=CODE + 0x900) + ["print r4",
                           "put h 0x%x, 0x0008" % (PCC2 + T1CTL)] + program([LD_BU(4, T1CTL)], at=CODE + 0xa00) + ["print r4"])
r4s = re.findall(r"print\s+r4\s*\n\s*(0x[0-9a-f]+)", t)
row("ovf2 arm", armval(t, alive, r4s), "0x11", "timer 2 overflowed: OVF count 1 | CEN -- a nibble only the tick can set")
row("ovf2 decl", cval(alive, how, t.count(DECL)), 1, "a guest wide write to T2CTL with the overflow nibble SET is declined")
row("ovf2 rb", cval(alive, how, ("0x%x" % int(r4s[1], 16)) if alive and len(r4s) > 1 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x11",
    "T2CTL unchanged -- a `&& !(reg & OVF)' guard would land 0x10 (CEN cleared)")
row("ovf2 rbv", cval(alive, how, ("0x%x" % int(r4s[2], 16)) if alive and len(r4s) > 2 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x11",
    "T2CTL unchanged after a COVF-set (0x0004) guest write with the count at 1 -- `&& !((idata & COVF) && (reg & OVF))' would land 0x00")
row("ovf2 rbx", cval(alive, how, ("0x%x" % int(r4s[3], 16)) if alive and len(r4s) > 3 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x11",
    "T2CTL unchanged after a HUH?-bit (0x0008) guest write with the count at 1 -- a landed write reads 0x10 and prints HUH?")
row("ovf2 rb1", cval(alive, how, ("0x%x" % int(r4s[4], 16)) if alive and len(r4s) > 4 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x2",
    "T1CTL (idle, preset COC) unchanged after an operator 0x0000 write while timer 2 holds a count -- the T1 label of this state")
row("ovf2 rb1v", cval(alive, how, ("0x%x" % int(r4s[5], 16)) if alive and len(r4s) > 5 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x2",
    "T1CTL (idle) unchanged after a COVF-set operator write -- a landed write reads 0x00")
row("ovf2 rb1x", cval(alive, how, ("0x%x" % int(r4s[6], 16)) if alive and len(r4s) > 6 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x2",
    "T1CTL (idle) unchanged after a HUH?-bit operator write -- a landed write reads 0x00 and prints HUH?")
row("ovf2 huh", cval(alive, how, t.count("HUH? write to PCCTWO_TxCTL")), 0, "no TxCTL HUH? line: every 0x0008 wide write in this session was declined")
t, alive, how = session(setup() + OVF_REGS + program_free(ovf_arm(T1COUNT, T1CTL)) + ["print r4",
                        "put h 0x%x, 0x0000" % (PCC2 + T1CTL)] + program([LD_BU(4, T1CTL)], at=CODE + 0x200) + ["print r4",
                        #  pass 11 batch two: the TxCTL generating set (the mirror)
                        "put h 0x%x, 0x0004" % (PCC2 + T1CTL)] + program([LD_BU(4, T1CTL)], at=CODE + 0x300) + ["print r4",
                        "put h 0x%x, 0x0008" % (PCC2 + T1CTL)] + program([LD_BU(4, T1CTL)], at=CODE + 0x400) + ["print r4"]
                        + program([ST_B(15, T2CTL), ST_H(9, T2CTL)], at=CODE + 0x500) + program([LD_BU(4, T2CTL)], at=CODE + 0x600) + ["print r4"]
                        + program([ST_H(13, T2CTL)], at=CODE + 0x700) + program([LD_BU(4, T2CTL)], at=CODE + 0x800) + ["print r4"]
                        + program([ST_H(14, T2CTL)], at=CODE + 0x900) + program([LD_BU(4, T2CTL)], at=CODE + 0xa00) + ["print r4"])
r4s = re.findall(r"print\s+r4\s*\n\s*(0x[0-9a-f]+)", t)
row("ovf1 arm", armval(t, alive, r4s), "0x11", "timer 1 overflowed: OVF count 1 | CEN")
row("ovf1 decl", cval(alive, how, t.count(DECL)), 1, "an operator wide write to T1CTL (odd) with the overflow nibble SET is declined")
row("ovf1 rb", cval(alive, how, ("0x%x" % int(r4s[1], 16)) if alive and len(r4s) > 1 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x11",
    "T1CTL unchanged -- the T1-only form of the same guard would land 0x10")
row("ovf1 rbv", cval(alive, how, ("0x%x" % int(r4s[2], 16)) if alive and len(r4s) > 2 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x11",
    "T1CTL unchanged after a COVF-set operator write with the count at 1 -- a landed write reads 0x00")
row("ovf1 rbx", cval(alive, how, ("0x%x" % int(r4s[3], 16)) if alive and len(r4s) > 3 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x11",
    "T1CTL unchanged after a HUH?-bit operator write with the count at 1 -- a landed write reads 0x10")
row("ovf1 rb2", cval(alive, how, ("0x%x" % int(r4s[4], 16)) if alive and len(r4s) > 4 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x2",
    "T2CTL (idle, preset COC) unchanged after a guest 0x0000 write while timer 1 holds a count")
row("ovf1 rb2v", cval(alive, how, ("0x%x" % int(r4s[5], 16)) if alive and len(r4s) > 5 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x2",
    "T2CTL (idle) unchanged after a COVF-set guest write -- a landed write reads 0x00")
row("ovf1 rb2x", cval(alive, how, ("0x%x" % int(r4s[6], 16)) if alive and len(r4s) > 6 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x2",
    "T2CTL (idle) unchanged after a HUH?-bit guest write -- a landed write reads 0x00")
row("ovf1 huh", cval(alive, how, t.count("HUH? write to PCCTWO_TxCTL")), 0, "no TxCTL HUH? line in the timer-1 overflow session")

#  PASS 7 (grok): the IPL write body reads a FUNCTION-STATIC `w' (its #119 print-once latch), not
#  a `d->' field -- the pass-6 enumeration walked fields and missed it.  No row held it SET at a
#  wide write: `acc ipl ro' sets it on a byte write and never wide-writes; `ipl noig2' wide-writes
#  with it still 0.  One session: the byte write first (w = 1), then the wide write -> declined.
t, alive, how = session(setup(r5="0x0", r6="0x0000") + program([ST_B(5, IPL), ST_H(6, IPL)]))
row("ipl wset", t.count(DECL), 1, "a wide write to IPL with the body's print latch already SET is still declined")

#  PASS 8 (kimi substitute, packet-fed): a lvalue held at ONE non-initial value pins only the
#  predicates that value breaks.  The overflow COUNT: `ovf*' hold it at 1 (bit 4), so a guard
#  `&& !(reg & 0xe0)' passed every row.  Re-arming the count every loop iteration overflows once
#  per host callback; exit when bit 7 sets (count 8): 0x81 = count 8 | CEN.
def ovfhi_arm(cnt_off, ctl_off):
    return [ST_B(8, ctl_off), ST_W(6, cnt_off), LD_BU(4, ctl_off), BB0(7, 4, -2)]
t, alive, how = session(setup() + OVF_REGS + program_free(ovfhi_arm(T2COUNT, T2CTL)) + ["print r4"]
                        + program([ST_H(9, T2CTL)], at=CODE + 0x100) + program([LD_BU(4, T2CTL)], at=CODE + 0x200) + ["print r4"]
                        #  pass 11 batch two: the TxCTL generating set at the count >= 8 cell
                        + program([ST_H(13, T2CTL)], at=CODE + 0x300) + program([LD_BU(4, T2CTL)], at=CODE + 0x400) + ["print r4"]
                        + program([ST_H(14, T2CTL)], at=CODE + 0x500) + program([LD_BU(4, T2CTL)], at=CODE + 0x600) + ["print r4"]
                        + program([ST_B(15, T1CTL)], at=CODE + 0x700) + ["put h 0x%x, 0x0000" % (PCC2 + T1CTL)] + program([LD_BU(4, T1CTL)], at=CODE + 0x800) + ["print r4",
                           "put h 0x%x, 0x0004" % (PCC2 + T1CTL)] + program([LD_BU(4, T1CTL)], at=CODE + 0x900) + ["print r4",
                           "put h 0x%x, 0x0008" % (PCC2 + T1CTL)] + program([LD_BU(4, T1CTL)], at=CODE + 0xa00) + ["print r4"])
r4s = re.findall(r"print\s+r4\s*\n\s*(0x[0-9a-f]+)", t)
#  pass 9 (Opus): the count advances one per DELIVERED callback, so under host load the poll can
#  exit at 9 (0x91); the rows mask to bits 7 and 0 -- count >= 8 AND CEN -- and the mutant's 0x80
#  (CEN cleared by the landed write) still reds.  Re-measured as a control in part 9.
def ovfmask(x):
    return ("0x%x" % (int(x, 16) & 0x81)) if isinstance(x, str) and x.startswith("0x") else x
row("ovfhi2 arm", ovfmask(armval(t, alive, r4s)), "0x81", "timer 2 overflowed >= EIGHT times: count 8 | CEN, masked to bits 7,0")
row("ovfhi2 decl", cval(alive, how, t.count(DECL)), 1, "a guest wide write to T2CTL with the overflow count >= 8 is declined")
row("ovfhi2 rb", cval(alive, how, ("0x%x" % (int(r4s[1], 16) & 0x81)) if alive and len(r4s) > 1 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x81",
    "T2CTL unchanged (bits 7,0) -- a `&& !(reg & 0xe0)' guard would land 0x80")
row("ovfhi2 rbv", cval(alive, how, ("0x%x" % (int(r4s[2], 16) & 0x81)) if alive and len(r4s) > 2 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x81",
    "T2CTL unchanged (bits 7,0) after a COVF-set guest write with the count >= 8 -- a landed write reads 0x00")
row("ovfhi2 rbx", cval(alive, how, ("0x%x" % (int(r4s[3], 16) & 0x81)) if alive and len(r4s) > 3 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x81",
    "T2CTL unchanged (bits 7,0) after a HUH?-bit guest write with the count >= 8 -- a landed write reads 0x80")
row("ovfhi2 rb1", cval(alive, how, ("0x%x" % int(r4s[4], 16)) if alive and len(r4s) > 4 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x2",
    "T1CTL (idle, preset COC) unchanged after an operator 0x0000 write while timer 2 holds a high count")
row("ovfhi2 rb1v", cval(alive, how, ("0x%x" % int(r4s[5], 16)) if alive and len(r4s) > 5 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x2",
    "T1CTL (idle) unchanged after a COVF-set operator write")
row("ovfhi2 rb1x", cval(alive, how, ("0x%x" % int(r4s[6], 16)) if alive and len(r4s) > 6 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x2",
    "T1CTL (idle) unchanged after a HUH?-bit operator write")
row("ovfhi2 huh", cval(alive, how, t.count("HUH? write to PCCTWO_TxCTL")), 0, "no TxCTL HUH? line in the timer-2 high-count session")
t, alive, how = session(setup() + OVF_REGS + program_free(ovfhi_arm(T1COUNT, T1CTL)) + ["print r4",
                        "put h 0x%x, 0x0000" % (PCC2 + T1CTL)] + program([LD_BU(4, T1CTL)], at=CODE + 0x200) + ["print r4",
                        #  pass 11 batch two: the TxCTL generating set at the count >= 8 cell (the mirror)
                        "put h 0x%x, 0x0004" % (PCC2 + T1CTL)] + program([LD_BU(4, T1CTL)], at=CODE + 0x300) + ["print r4",
                        "put h 0x%x, 0x0008" % (PCC2 + T1CTL)] + program([LD_BU(4, T1CTL)], at=CODE + 0x400) + ["print r4"]
                        + program([ST_B(15, T2CTL), ST_H(9, T2CTL)], at=CODE + 0x500) + program([LD_BU(4, T2CTL)], at=CODE + 0x600) + ["print r4"]
                        + program([ST_H(13, T2CTL)], at=CODE + 0x700) + program([LD_BU(4, T2CTL)], at=CODE + 0x800) + ["print r4"]
                        + program([ST_H(14, T2CTL)], at=CODE + 0x900) + program([LD_BU(4, T2CTL)], at=CODE + 0xa00) + ["print r4"])
r4s = re.findall(r"print\s+r4\s*\n\s*(0x[0-9a-f]+)", t)
row("ovfhi1 arm", ovfmask(armval(t, alive, r4s)), "0x81", "timer 1 overflowed >= eight times, masked to bits 7,0")
row("ovfhi1 decl", cval(alive, how, t.count(DECL)), 1, "an operator wide write to T1CTL with the overflow count >= 8 is declined")
row("ovfhi1 rb", cval(alive, how, ("0x%x" % (int(r4s[1], 16) & 0x81)) if alive and len(r4s) > 1 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x81", "T1CTL unchanged (bits 7,0)")
row("ovfhi1 rbv", cval(alive, how, ("0x%x" % (int(r4s[2], 16) & 0x81)) if alive and len(r4s) > 2 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x81",
    "T1CTL unchanged (bits 7,0) after a COVF-set operator write with the count >= 8")
row("ovfhi1 rbx", cval(alive, how, ("0x%x" % (int(r4s[3], 16) & 0x81)) if alive and len(r4s) > 3 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x81",
    "T1CTL unchanged (bits 7,0) after a HUH?-bit operator write with the count >= 8")
row("ovfhi1 rb2", cval(alive, how, ("0x%x" % int(r4s[4], 16)) if alive and len(r4s) > 4 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x2",
    "T2CTL (idle, preset COC) unchanged after a guest 0x0000 write while timer 1 holds a high count")
row("ovfhi1 rb2v", cval(alive, how, ("0x%x" % int(r4s[5], 16)) if alive and len(r4s) > 5 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x2",
    "T2CTL (idle) unchanged after a COVF-set guest write")
row("ovfhi1 rb2x", cval(alive, how, ("0x%x" % int(r4s[6], 16)) if alive and len(r4s) > 6 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x2",
    "T2CTL (idle) unchanged after a HUH?-bit guest write")
row("ovfhi1 huh", cval(alive, how, t.count("HUH? write to PCCTWO_TxCTL")), 0, "no TxCTL HUH? line in the timer-1 high-count session")

#  The pending COUNTS: `pend*' hold them at 1, so `&& pending < 2' passed every row.  With COC set
#  and compare 1, one callback adds thousands of interrupts (pcc_timer_tick:231-236).
PENDN_REGS = ["r5=0x1", "r6=0x0", "r7=0x11", "r8=0x3", "r9=0x0"]
t, alive, how = session(setup() + PENDN_REGS + program_free(pend_arm(T2CMP, T2COUNT, T2ICR, T2CTL)) + ["print r4"]
                        + program([ST_H(9, T2ICR)], at=CODE + 0x100) + program([LD_BU(4, T2ICR)], at=CODE + 0x200) + ["print r4"])
r4s = re.findall(r"print\s+r4\s*\n\s*(0x[0-9a-f]+)", t)
row("pendn2 arm", armval(t, alive, r4s), "0x31", "timer 2 pending MANY times (COC, compare 1): INT|IEN|IL1")
row("pendn2 decl", cval(alive, how, t.count(DECL)), 1, "a guest wide write to T2ICR with thousands pending is declined")
row("pendn2 rb", cval(alive, how, ("0x%x" % int(r4s[1], 16)) if alive and len(r4s) > 1 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x31",
    "T2ICR unchanged -- a `&& pending_timer2 < 2' guard would land 0x20")
t, alive, how = session(setup() + PENDN_REGS + program_free(pend_arm(T1CMP, T1COUNT, T1ICR, T1CTL)) + ["print r4",
                        "put h 0x%x, 0x0000" % (PCC2 + T1ICR)] + program([LD_BU(4, T1ICR)], at=CODE + 0x200) + ["print r4"])
r4s = re.findall(r"print\s+r4\s*\n\s*(0x[0-9a-f]+)", t)
row("pendn1 arm", armval(t, alive, r4s), "0x31", "timer 1 pending many times")
row("pendn1 decl", cval(alive, how, t.count(DECL)), 1, "an operator wide write to T1ICR with thousands pending is declined")
row("pendn1 rb", cval(alive, how, ("0x%x" % int(r4s[1], 16)) if alive and len(r4s) > 1 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x31", "T1ICR unchanged")

#  The value 0 was driven at SCCERR and T1ICR only: a per-arm `&& idata != 0' escaped elsewhere.
t, alive, how = session(["put h 0x%x, 0x0000" % (PCC2 + o) for _, o in BLOCKS12])
row("latch all zero", t.count(DECL), 12, "twelve 2-byte writes of the VALUE 0 -- an `idata != 0' qualifier lands one and drops the count")

#  PASS 8 (codex): the TxICR presets 0x13 / 0x31 leave bit 2 -- an interrupt-level bit -- clear,
#  a legal byte write 0x14 sets it, and `&& !(reg & 0x04)' on the TxICR guard passed every row.
#  One preset with the bit set, at both labels.
t, alive, how = session(setup(r5="0x17", r6="0xaab8") + program([ST_B(5, T2ICR), ST_H(6, T2ICR), LD_BU(4, T2ICR)]) + ["print r4"])
row("rb t2icr il4", printed(t, "r4") if alive else "died", "0x17", "T2ICR with IL bit 2 set is unchanged after a declined 2-byte write")
t, alive, how = session(setup(r5="0x17") + program([ST_B(5, T1ICR)]) + ["put h 0x%x, 0xaab8" % (PCC2 + T1ICR)]
                        + program([LD_BU(4, T1ICR)], at=CODE + 0x100) + ["print r4"])
row("rb t1icr il4", printed(t, "r4") if alive else "died", "0x17", "T1ICR with IL bit 2 set is unchanged after a declined put h")

#  PASS 8 (Opus F5): the IPL arm has a SECOND function-static, in its READ branch (the "IPL == 0
#  on read" print latch).  It is outside the closure -- the read branch is not the guarded write
#  body -- but one session holds it set and then wide-writes, so a guard reading it is pinned anyway.
t, alive, how = session(setup(r6="0x0000") + program([LD_BU(4, IPL), ST_H(6, IPL)]))
row("ipl rset", t.count(DECL), 1, "a wide write to IPL after a READ of IPL (the read branch's own latch set) is still declined")

#  PASS 8 (Opus seat): a guard at arm A qualified by arm B's latch bit -- `&& !(d->warned &
#  (1u << B))', the helper's own operand with the wrong index -- is killed by `latch all' only
#  when B is written BEFORE A (B's bit is then set and A's write lands).  The forward order
#  leaves every pair with B after A uncovered, GENCTL first of all.  The same twelve writes in
#  REVERSE order cover the other half: together, all 132 ordered pairs.
t, alive, how = session(["put h 0x%x, 0x0003" % (PCC2 + o) for _, o in reversed(BLOCKS12)])
row("latch all rev", t.count(DECL), 12, "the twelve wide writes in reverse block order -- with `latch all', every cross-bit qualifier lands one")

#  PASS 9 (Opus seat): a guard conditioned on BOTH pending counts -- `&& !(pending1 && pending2)' --
#  passed every row, because each count was held non-zero in its own session and never together.
#  Both timers armed (compare 1, count 0, IEN|IL1, CEN), free-run until T2's INT, read T1's too.
def pendboth_arm():
    return [ST_W(5, T1CMP), ST_W(6, T1COUNT), ST_B(7, T1ICR), ST_B(8, T1CTL),
            ST_W(5, T2CMP), ST_W(6, T2COUNT), ST_B(7, T2ICR), ST_B(8, T2CTL), LD_BU(4, T2ICR), BB0(5, 4, -1)]
t, alive, how = session(setup() + PEND_REGS + program_free(pendboth_arm()) + ["print r4"]
                        + program([LD_BU(4, T1ICR)], at=CODE + 0x100) + ["print r4"]
                        + program([ST_H(9, T2ICR)], at=CODE + 0x200) + program([LD_BU(4, T2ICR)], at=CODE + 0x300) + ["print r4"]
                        + program([ST_H(10, T2ICR)], at=CODE + 0x400) + program([LD_BU(4, T2ICR)], at=CODE + 0x500) + ["print r4",
                           "put h 0x%x, 0x0000" % (PCC2 + T1ICR)] + program([LD_BU(4, T1ICR)], at=CODE + 0x600) + ["print r4",
                           "put h 0x%x, 0x0013" % (PCC2 + T1ICR)] + program([LD_BU(4, T1ICR)], at=CODE + 0x700) + ["print r4"]
                        #  pass 11: the ICLR and HUH-bit generating writes at both labels (appended)
                        + program([ST_H(11, T2ICR)], at=CODE + 0x800) + program([LD_BU(4, T2ICR)], at=CODE + 0x900) + ["print r4"]
                        + program([ST_H(12, T2ICR)], at=CODE + 0xa00) + program([LD_BU(4, T2ICR)], at=CODE + 0xb00) + ["print r4",
                           "put h 0x%x, 0x0018" % (PCC2 + T1ICR)] + program([LD_BU(4, T1ICR)], at=CODE + 0xc00) + ["print r4",
                           "put h 0x%x, 0x0020" % (PCC2 + T1ICR)] + program([LD_BU(4, T1ICR)], at=CODE + 0xd00) + ["print r4"])
r4s = re.findall(r"print\s+r4\s*\n\s*(0x[0-9a-f]+)", t)
#  pass 10 (Opus, predicted before its build; codex by reading): the joint cell was closed at the T2
#  LABEL only and with IEN clear only; `&& !(p1 && p2 && relative_addr == PCCTWO_T1ICR)' passed every
#  row -- the #499 shape (one side of a symmetry closed, its mirror open) inside the repair for it.
#  The same session now wide-writes at BOTH labels with BOTH IEN values; with the pend1/pend2
#  extensions the whole (label, p1, p2, IEN) product is held.
row("pendboth arm", armval(t, alive, r4s), "0x31", "timer 2 pending with timer 1 ALSO armed: INT|IEN|IL1")
row("pendboth arm1", cval(alive, how, ("0x%x" % int(r4s[1], 16)) if alive and len(r4s) > 1 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x31",
    "timer 1's INT set in the same session (sticky: |= in reassert, cleared only by ICLR); the proof that BOTH counts are non-zero at the guard is M_PENDBOTH reddening the rb/rbi readbacks, not this readback")
row("pendboth decl", cval(alive, how, t.count(DECL)), 1, "BOTH timers pending: the first of four wide writes (T2ICR guest 0x0000) is announced; latched once per block, the readbacks are the per-write channel")
row("pendboth rb", cval(alive, how, ("0x%x" % int(r4s[2], 16)) if alive and len(r4s) > 2 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x31",
    "T2ICR unchanged -- a `&& !(pending1 && pending2)' guard would land 0x20")
row("pendboth rbi", cval(alive, how, ("0x%x" % int(r4s[3], 16)) if alive and len(r4s) > 3 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x31",
    "T2ICR unchanged after the IEN-set guest write with both pending -- a landed write reads 0x33")
row("pendboth rb1", cval(alive, how, ("0x%x" % int(r4s[4], 16)) if alive and len(r4s) > 4 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x31",
    "T1ICR unchanged -- the T1-label joint form `&& !(p1 && p2 && relative_addr == T1ICR)' would land 0x20")
row("pendboth rb1i", cval(alive, how, ("0x%x" % int(r4s[5], 16)) if alive and len(r4s) > 5 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x31",
    "T1ICR unchanged after the IEN-set operator write with both pending -- the (T1, >0, >0, IEN) cell; a landed write reads 0x33")
row("pendboth rbc", cval(alive, how, ("0x%x" % int(r4s[6], 16)) if alive and len(r4s) > 6 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x31",
    "T2ICR unchanged after an ICLR-set guest write with both pending -- a landed write reads 0x10 and decrements timer 2's count")
row("pendboth rbh", cval(alive, how, ("0x%x" % int(r4s[7], 16)) if alive and len(r4s) > 7 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x31",
    "T2ICR unchanged after a HUH-bit guest write with both pending -- a landed write reads 0x20 and prints HUH?")
row("pendboth rb1c", cval(alive, how, ("0x%x" % int(r4s[8], 16)) if alive and len(r4s) > 8 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x31",
    "T1ICR unchanged after an ICLR-set operator write with both pending -- a landed write reads 0x10")
row("pendboth rb1h", cval(alive, how, ("0x%x" % int(r4s[9], 16)) if alive and len(r4s) > 9 else "short-transcript (FAILED FOR SOME OTHER REASON)"), "0x31",
    "T1ICR unchanged after a HUH-bit operator write with both pending -- a landed write reads 0x20")
row("pendboth huh", cval(alive, how, t.count("HUH? write to PCCTWO_TxICR")), 0, "no HUH? line in the both-timers session")

#  PASS 8 (Opus seat): the TxCTL byte's THIRD writer is the counter arm's raw memcpy -- an 8-byte
#  write at T2COUNT (0x10, 8-aligned, so a guest st.d reaches it) copies 0x10..0x17 and lands
#  arbitrary bytes on T2CTL (0x16) and T1CTL (0x17).  That is the filed pcc2counter8 defect, and
#  it is the ONLY way bits 2-3 (and, in one step, 5-7) of TxCTL become non-initial.  One session
#  holds bits 2-7 SET at a wide write.  *** THIS ROW RESTS ON A FILED DEFECT: when pcc2counter8
#  is fixed the preset path vanishes and the row must be re-cut (bits 4-7 via the tick's
#  overflows; bits 2-3 then have no writer and become dead). ***
t, alive, how = session(setup() + ["put d 0x%x, 0x000000000000fcfc" % (PCC2 + T2COUNT)] + program([LD_BU(4, T2CTL)]) + ["print r4",
                        "put h 0x%x, 0x0303" % (PCC2 + T2CTL)] + program([LD_BU(4, T2CTL)], at=CODE + 0x100) + ["print r4"])
r4s = re.findall(r"print\s+r4\s*\n\s*(0x[0-9a-f]+)", t)
row("rb t2ctl b27", ("0x%x" % int(r4s[1], 16)) if alive and len(r4s) > 1 else "died", "0xfc",
    "T2CTL with bits 2-7 set (via the pcc2counter8 raw copy) unchanged after a declined put h -- a `&& !(reg & COVF)' guard would land 0xff")
t, alive, how = session(setup() + ["put d 0x%x, 0x000000000000fcfc" % (PCC2 + T2COUNT)] + program([LD_BU(4, T1CTL)]) + ["print r4",
                        "put h 0x%x, 0x0303" % (PCC2 + T1CTL)] + program([LD_BU(4, T1CTL)], at=CODE + 0x100) + ["print r4"])
r4s = re.findall(r"print\s+r4\s*\n\s*(0x[0-9a-f]+)", t)
row("rb t1ctl b27", ("0x%x" % int(r4s[1], 16)) if alive and len(r4s) > 1 else "died", "0xfc",
    "T1CTL with bits 2-7 set (same raw copy) unchanged after a declined put h")

#  PASS 7 (codex): the T1CTL / T1ICR labels share the TxCTL / TxICR guards and had len-2 rows only;
#  a `len < 4 || relative_addr == PCCTWO_T2CTL' fall-through lands 4-/8-byte writes at T1CTL alone.
#  The width cross-product at the two labels (operator rows: the offsets are odd).
for nm, off, pre, want in (("t1ctl", T1CTL, "0x03", "0x3"), ("t1icr", T1ICR, "0x13", "0x13")):
    t, alive, how = session(setup(r5=pre) + program([ST_B(5, off)]) + ["put w 0x%x, 0xaab8ccdd" % (PCC2 + off)]
                            + program([LD_BU(4, off)], at=CODE + 0x100) + ["print r4"])
    row("rb4 " + nm, printed(t, "r4") if alive else "died", want, "%s unchanged after a declined 4-byte write" % nm.upper())
    t, alive, how = session(setup(r5=pre) + program([ST_B(5, off)]) + ["put d 0x%x, 0xaab8ccdd00112244" % (PCC2 + off)]
                            + program([LD_BU(4, off)], at=CODE + 0x100) + ["print r4"])
    row("rb8 " + nm, printed(t, "r4") if alive else "died", want, "%s unchanged after a declined 8-byte write" % nm.upper())

# --------------------------------------------- de-escalation ACCEPT rows (byte writes)
#  Removing twelve exit(1)s destroys the tripwire that announced guard growth.  So the
#  legal width must still LAND at each reachable arm, through its own mask, with no
#  decline message.  Expected values from the arms' own semantics.
for nm, off, wr, rdv in (("genctl", GENCTL, "0x82", "0x82"),     # stores the byte; bit 0x04 clear
                          ("t2ctl", T2CTL, "0x03", "0x3"),       # &= 0xfc; |= (v & 3)
                          ("t2icr", T2ICR, "0x13", "0x13"),      # &= ~0x17; |= (v & 0x17)
                          ("scctx", SCCTX, "0x1f", "0x1f"),      # = v & 0x1f
                          ("sccerr", SCCERR, "0x5a", "0x0")):    # any write clears to 0
    t, alive, how = session(setup(r5=wr) + program([ST_B(5, off), LD_BU(4, off)]) + ["print r4"])
    row("acc " + nm, printed(t, "r4") if alive else "died", rdv,
        "st.b %s at the legal width lands through its own mask" % nm.upper())
    row("acc %s nod" % nm, t.count(DECL), 0, "...with NO decline message")

# ------------------------------- OPERATOR path: the seven odd blocks via `put h'
#  The m88k alignment check makes these guest-unreachable; the debugger warns on a
#  misaligned put and stores anyway, straight to the handler (MEASURED pre-fix: exit1).
for nm, off in (("vecbase", VECBASE), ("pscale", PSCALEADJ), ("t1ctl", T1CTL),
                ("t1icr", T1ICR), ("sccicr", SCCICR), ("sccrx", SCCRX), ("scsiicr", SCSIICR)):
    t, alive, how = session(["put h 0x%x, 0x0303" % (PCC2 + off)])
    row("op " + nm, how, "exit0", "debugger put h at odd %s survives" % nm.upper())
    row("op %s dcl" % nm, t.count(DECL), 1, "...and was declined once")

#  --------- the odd arms' FALL-THROUGH channel (pass 3, ruled a floor breach, not a disclosure)
#  The block above proves each odd arm ANNOUNCES; it cannot see a guard that announces AND
#  then lets the halfword land (the M_FALL shape -- decline nulled, guard kept: clause (d)).
#  PRETABLE Section 2 had disclosed that as "a sentence owed".  The measuring seat asked
#  whether a disclosure can discharge a floor clause; it cannot, or every breach becomes a
#  sentence.  So each of the four arms gets the channel its body offers:
#    SCCICR/SCCRX/SCSIICR store `idata & mask' then reassert_interrupts(): set 0x1f by
#      byte (legal under both masks), decline a wide 0xaab8, read the byte back -- a landed
#      write leaves 0x18 (& 0x1f) or 0x98 (& 0xdf) in an INTERRUPT CONTROL register.
#    PSCALEADJ stores nothing; its write body only prints "ignored (value ...)".  A landed
#      wide write therefore prints that line -- the message is the only channel, and the
#      row counts it at ZERO.
for nm, off in (("sccicr", SCCICR), ("sccrx", SCCRX), ("scsiicr", SCSIICR)):
    t, alive, how = session(setup(r5="0x1f") + program([ST_B(5, off)])
                            + ["put h 0x%x, 0xaab8" % (PCC2 + off)]
                            + program([LD_BU(4, off)], at=CODE + 0x100) + ["print r4"])
    row("rb " + nm, printed(t, "r4") if alive else "died", "0x1f",
        "%s unchanged after a declined put h -- a fall-through lands 0x18/0x98 and reasserts" % nm.upper())
t, alive, how = session(["put h 0x%x, 0x0303" % (PCC2 + PSCALEADJ)])
row("op pscale noig", t.count("PSCALEADJ ignored"), 0,
    "a declined wide write never reaches the 'ignored' print -- fall-through would")

#  PASS 3 (class closure).  `rb vecbase' above writes wide to GENCTL and reads VECBASE: it
#  is GENCTL's neighbour-lane check and never exercises VECBASE's own guard.  A seat
#  MEASURED announce-then-fall-through at VECBASE as 82/82 -- the halfword landed (& 0xf0)
#  while `op vecbase dcl' and `latch all' stayed green by construction.  VECBASE is the
#  interrupt vector base, so the landed lane mis-delivers every vector.  Its own readback:
t, alive, how = session(setup(r5="0x50") + program([ST_B(5, VECBASE)])
                        + ["put h 0x%x, 0xaab8" % (PCC2 + VECBASE)]
                        + program([LD_BU(4, VECBASE)], at=CODE + 0x100) + ["print r4"])
row("rb vecbase own", printed(t, "r4") if alive else "died", "0x50",
    "VECBASE unchanged after a declined put h to ITS OWN arm -- a fall-through lands 0xb0")
#  IPL's write body stores nothing and prints "write to read-only PCCTWO_IPL; ignored"
#  once per process (#119 static).  A declined wide write never reaches it; a fall-through
#  prints it -- PSCALEADJ's shape at the twelfth block.  The message is the channel.
t, alive, how = session(setup(r6="0x0303") + program([ST_H(6, IPL)]))
row("hwr ipl noig", t.count("write to read-only PCCTWO_IPL"), 0,
    "a declined st.h to IPL never reaches the read-only print -- fall-through would")
#  The codex seat, pass 3: the MIRROR of the measured width edit.  `len != 1' -> `len == 2'
#  declines every halfword row here and lets a WORD write land -- every row above stayed
#  green under it.  One cardinality row over WORD writes closes that at all twelve blocks.
#  (Word writes to the counter arms are pcc2counter8's business and are not touched.)
t, alive, how = session(["put w 0x%x, 0x00000003" % (PCC2 + o) for _, o in BLOCKS12])
row("latch all w", t.count(DECL), 12,
    "one WORD write per BLOCK -> TWELVE announces: a `len == 2' guard anywhere drops it")
#  PASS 4 (glm, deepseek, codex): the rows drove widths {1,2,4} and the contract itself says
#  `put d' reaches with len 8, so a guard true on {2,4} and false on 8 (`len & 6', or
#  `len != 1 && len != 8') passed every row.  Twelve DWORD writes, twelve announces:
t, alive, how = session(["put d 0x%x, 0x0000000000000003" % (PCC2 + o) for _, o in BLOCKS12])
row("latch all d", t.count(DECL), 12,
    "one DWORD write per BLOCK -> TWELVE announces: an 8-byte exemption anywhere drops it")
#  And the de-escalation side, closed at all twelve: one LEGAL byte write per block must
#  announce NOTHING.  A guard grown to refuse bytes (`len != 1' -> `len != 0') at any of
#  the seven blocks without a per-arm `acc' row is visible only here.  Values: GENCTL keeps
#  bit 0x04 clear (pcc2c040kill); VECBASE's mask is 0xf0; the rest accept any byte.
#  *** MEASURED, part 3 and 3b: this row's first form used the debugger's `put b' and could
#  NOT SEE a guard grown to refuse bytes at PSCALEADJ -- 96/96 with the mutation PROVEN in the
#  source and the binary newer than it.  `put b' calls memory_rw directly with NO_EXCEPTIONS,
#  and that flag does not dispatch to a DM_DEFAULT device; `put h/w/d' go through the
#  store_Nbit_word helpers and do reach the arms.  So the operator path for BYTES is not a
#  path at all, and the row was vacuous by construction -- the CHANNEL rule's own failure,
#  caught by the table.  Guest `st.b' is legal at every offset (byte accesses skip the m88k
#  alignment check; `rb mask' stores a byte at 0x3f this way), so the accept side is pinned
#  from the GUEST at all twelve blocks, which is the stronger form anyway. ***
t, alive, how = session(setup(r5="0x10") + program([ST_B(5, o) for _, o in BLOCKS12]))
row("acc all", t.count(DECL), 0,
    "twelve legal guest byte stores, ZERO declines -- the accept side at every block")
row("acc all lv", how, "exit0", "...and the host survived all twelve byte stores")
#  PASS 4 (codex): `acc all' proves no DECLINE and survival; it does not prove the byte
#  reached the arm's BODY.  For the two print-only arms the body's own print is the proof:
t, alive, how = session(setup(r5="0x10") + program([ST_B(5, PSCALEADJ)]))
row("acc pscale ign", t.count("PSCALEADJ ignored"), 1,
    "a legal byte write to PSCALEADJ reaches its body -- the ignored print fires once")
t, alive, how = session(setup(r5="0x10") + program([ST_B(5, IPL)]))
row("acc ipl ro", t.count("write to read-only PCCTWO_IPL"), 1,
    "a legal byte write to IPL reaches its body -- the read-only print fires once")
#  The T1 labels of the two SHARED blocks (deepseek, pass 3): their readbacks above are at
#  the T2 offsets, so a fall-through reaching only the T1 half of a split block would leave
#  `op t1ctl dcl' at 1 with nothing reading T1CTL back.  Operator path, own readbacks:
#  (`want' is the value as the debugger PRINTS it -- 0x03 comes back as `0x3'.  The first
#  part-3 BASE run reddened this row on the fix for exactly that string mismatch, 95/96;
#  the value was right.  Re-measured in part 3b.)
for nm, off, pre, want in (("t1ctl", T1CTL, "0x03", "0x3"), ("t1icr", T1ICR, "0x13", "0x13")):
    t, alive, how = session(setup(r5=pre) + program([ST_B(5, off)])
                            + ["put h 0x%x, 0xaab8" % (PCC2 + off)]
                            + program([LD_BU(4, off)], at=CODE + 0x100) + ["print r4"])
    row("rb " + nm, printed(t, "r4") if alive else "died", want,
        "%s unchanged after a declined put h at the T1 label -- a fall-through lands 0xb8 & mask (RMW at TxCTL: 0)" % nm.upper())

# --------------------------------- IPL (guest-reachable, EVEN) and MASK (operator, odd)
#  IPL 0x3e: a halfword at 0x3e lands in the IPL arm.  Its write side is read-only (#119
#  "ignored"), so a wide write is declined by the WIDTH latch first and a readback cannot
#  tell the two refusals apart -- the channel is the message.
t, alive, how = session(setup() + program([I_ST_SCR, LD_H(4, IPL), I_LD_SCR]) + ["print r4"])
row("hrd ipl", how, "exit0", "ld.h IPL (EVEN, the SIXTH guest-reachable block) survives")
row("hrd ipl lv", printed(t, "r4") if alive else "died", "0x5a5a5a5a", "...and runs on")
row("hrd ipl nod", t.count(DECL), 0, "...and the wide READ of IPL is never declined")
t, alive, how = session(setup(r6="0x1234") + program([I_ST_SCR, ST_H(6, IPL), I_LD_SCR]) + ["print r4"])
row("hwr ipl", how, "exit0", "st.h IPL survives")
row("hwr ipl lv", printed(t, "r4") if alive else "died", "0x5a5a5a5a", "...and runs on")
row("hwr ipl dcl", t.count("write to PCCTWO_IPL " + DECL), 1,
    "...declined by the WIDTH latch (not the read-only one) -- the message is the channel")
#  MASK 0x3f: odd, operator path.  It is GENCTL's twin, so it gets GENCTL's readback: set
#  MASK to a known byte at the legal width, decline a wide write through the debugger,
#  then read the byte back through a program at a SECOND address.  A deleted guard stores
#  the wrong lane (0xbb); an accidental compose stores 0xaa.  reassert_interrupts on a
#  MASK byte write is harmless here: GENCTL's C040 bit is clear and nothing is pending.
t, alive, how = session(setup(r5="0x12") + program([ST_B(5, MASK)])
                        + ["put h 0x%x, 0xaabb" % (PCC2 + MASK)]
                        + program([LD_BU(4, MASK)], at=CODE + 0x100) + ["print r4"])
row("op mask", how, "exit0", "debugger put h at odd MASK survives")
row("op mask dcl", t.count("write to PCCTWO_MASK " + DECL), 1, "...and was declined once")
row("rb mask", printed(t, "r4") if alive else "died", "0x12",
    "MASK unchanged after the declined wide write -- GENCTL's twin gets GENCTL's readback")

# ---------------------------------------------------------------------- summary
print("NOROW  two device instances               -- mvme187 has ONE pcc2; per-instance latch state"
      " is by construction, not measured")
print("NOROW  pcc2c040kill                        -- a LEGAL byte write of 0x04 to GENCTL still ends"
      " the host; every GENCTL lane here keeps that bit clear")
print("NOROW  pcc2defaultkill / pcc2counter8      -- other arms, other rounds")
bad = [n for n, ok in rows if not ok]
print("PCC2W_RESULT=%d/%d" % (len(rows) - len(bad), len(rows)))
print("PCC2W_LABEL=%s" % LABEL)
if bad:
    print("PCC2W_RED=%s" % ",".join(bad))
print("PCC2W_PROBE_DONE")
