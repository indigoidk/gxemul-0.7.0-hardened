# CLOSING PASS 5 on the #530 REPAIR 5 -- `lcaisalane`: VERIFY THE ENUMERATION.  Liveness token `LCA530_C5_20260915`.

VERDICT LINE FIRST: `CLOSES` (the 185-row detector covers its enumerated class, and the enumeration is complete) or
`GAP: <exact source edit to the FIXED dev_lca.c that scores 185/185 and changes a guest-visible outcome>` or
`ENUMERATION WRONG: <the cell>`, then the token.

A routine mutation-testing review of an open-source hardware emulator (GXemul, a hardened fork).  Check premises, not only
reasoning; say what you could not check.  Tree: `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\` ONLY.  Packet-fed seats: all
facts are below; do not plan to read files.

## WHY THIS PASS EXISTS
Closing passes 2, 3 and 4 each found the FORWARD-COUNT class (a store's phantom read after its forward; a load's forward
duplicated) escaping one cell over, so by the repair-chain amendment repair 5 owed the CLASS CLOSURE: the whole class
enumerated from the handler's own arms x width kinds x lanes, every observable cell rowed in ONE diff, the rest classified
in the contract.  The flagship ruling (below, part B) fixed its shape: lanes 0-2 on ARCHITECTURAL channels; lane 3 on the
8042 PC-style stub's access counter (an emulator TODO) with a MANDATORY liveness row; tails on the 8042 queue; nonzero
stores.  **This pass VERIFIES THE ENUMERATION -- it does not hunt cells.**  A cell outside the enumeration, a row whose
channel cannot vary under its mutant, or a misclassified cell is the finding; a new mutant INSIDE a rowed cell that still
scores 185/185 is a GAP.

## SETTLED (re-stated because the questions depend on it)
* Disposition B: the byte for ISA port P sits at buffer position `(P & 3) % len` on BOTH arms; `len == 0` refused first;
  no latch, no announce.  The FIX is unchanged since pass 2 and every seat of six passes found it correct.
* memory_rw pre-zeroes a device read buffer (#95).  The 1 KB split fires on Alpha for every non-PHYSICAL access: a HEAD of
  1..7 bytes at a port 0x1f mod 0x20 (lane 3), a TAIL at the next port, 0 mod 0x20 (lane 0) -- measured.
* A head or tail is ONE handler call at ONE port, forwarding ONE byte (32 sparse bytes per port).
* The probe's machine: alphabook1 with a dummy 8-byte image -- no IDE image (so no wdc), no VGA without X11.
* Kill-table targeting: repair 5 ADDS sessions only, so no table 1-5 kill moves.

## THE FIX (`git diff`, verbatim)

```diff
diff --git a/src/devices/dev_lca.c b/src/devices/dev_lca.c
index 6873466..a7923f4 100644
--- a/src/devices/dev_lca.c
+++ b/src/devices/dev_lca.c
@@ -279,15 +279,25 @@ DEVICE_ACCESS(lca_isa)
 
 	relative_addr >>= 5;
 
-	ofs = relative_addr & 3;
-	if (ofs > len) {
-		fatal("[ ofs=%i len=%i in lca_isa access function. "
-		    "aborting ]\n", ofs, len);
-		exit(1);
-	}
+	/*
+	 *  #530: the byte for ISA port P sits at buffer position (P & 3) % len
+	 *  on BOTH arms -- the lane for the 21066's own len 4/8 accesses, and
+	 *  the rule the write arm already applied wherever the old guard let
+	 *  it run.  That guard's `ofs > len' exit(1) ended the host on a guest
+	 *  byte access to a port 2 or 3 mod 4 or a word access to a port 3 mod
+	 *  4 (ungated BWX; and at a port 3 mod 4 also the 1- or 2-byte head
+	 *  of an unaligned load or store that memory_rw splits at 1 KB),
+	 *  and the read arm discarded the
+	 *  fetched byte at ofs == len.
+	 *  One byte is forwarded whatever len is (the size field a<4:3> is
+	 *  not decoded here).  len 0 has no producer; refuse it before the %.
+	 */
+	if (len == 0)
+		return 0;
+	ofs = (relative_addr & 3) % len;
 
 	if (writeflag == MEM_WRITE) {
-		byte = data[ofs % len];
+		byte = data[ofs];
 		return cpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE +
 		    relative_addr, &byte, 1, writeflag, CACHE_NONE);
 	}
```

## THE WHOLE HANDLER

```c
DEVICE_ACCESS(lca_isa)
{
	unsigned int ofs, i;
	uint8_t byte;

	relative_addr >>= 5;

	/*
	 *  #530: the byte for ISA port P sits at buffer position (P & 3) % len
	 *  on BOTH arms -- the lane for the 21066's own len 4/8 accesses, and
	 *  the rule the write arm already applied wherever the old guard let
	 *  it run.  That guard's `ofs > len' exit(1) ended the host on a guest
	 *  byte access to a port 2 or 3 mod 4 or a word access to a port 3 mod
	 *  4 (ungated BWX; and at a port 3 mod 4 also the 1- or 2-byte head
	 *  of an unaligned load or store that memory_rw splits at 1 KB),
	 *  and the read arm discarded the
	 *  fetched byte at ofs == len.
	 *  One byte is forwarded whatever len is (the size field a<4:3> is
	 *  not decoded here).  len 0 has no producer; refuse it before the %.
	 */
	if (len == 0)
		return 0;
	ofs = (relative_addr & 3) % len;

	if (writeflag == MEM_WRITE) {
		byte = data[ofs];
		return cpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE +
		    relative_addr, &byte, 1, writeflag, CACHE_NONE);
	}

	cpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE + relative_addr,
	    &byte, 1, MEM_READ, CACHE_NONE);

	for (i=0; i<len; i++)
		data[i] = i == ofs? byte : 0x00;

	return 1;
}
```

## THE PROBE HEADER'S CONTRACT (clause e), verbatim -- re-derived by repair 5

```
*** #530: IT IS NOW THE WITNESS AND THE DETECTOR.  Sessions 1-3 are the witness below, unchanged but
#  for the sentinel; the #530 sessions at the end are the detector for the fix. ***
#
#  THE FIX (disposition B, regress/artifacts/lcaisalane/FABLE_F2_RULING_20260914.md): the byte for port
#  P sits at buffer position (P & 3) % len on BOTH arms; `len == 0' is refused first; no latch, no
#  announce (there is no event -- member 4, ACCEPT).  Table 1 (37 rows): HEAD 19/37, fix 37/37
#  (regress/artifacts/lcaisalane/fix530_20260914/HEAD_det.out, FIX_det.out); after the pass-2 repair
#  (51 rows) see that dir's table 2; after closing pass 1's class closure (77 rows) its table 3; after
#  closing pass 2's tail cells and phantom-read rows (93 rows) its table 4; after closing pass 3's
#  fallthrough rows (111 rows) its table 5; after closing pass 4's forward-count CLASS CLOSURE (185 rows) its table 6.
#
#  THE CELL SPACE, rowed WHOLE since closing pass 2 (the direct and head cells since closing pass 1, the
#  tail cells since closing pass 2; pass 2 and closing pass 1 found the same class --
#  a (len, lane, direction) cell of the position rule with no row -- one cell over each time, so the
#  repair rows the cross rather than the next cell): direct widths len 1, 2, 4, 8 x lane 0-3 x R/W,
#  every cell rowed (the read side of len 4 at lanes 2/3 FULL-register, not only a single-lane mask);
#  split HEADS len 1-7 at lane 3 x R/W (a head ends at a port 0x1f mod 0x20; this probe's is 0x3ff);
#  split TAILS len 1-7 at lane 0 x R/W (a tail starts at the next port, 0 mod 0x20) -- tails of len 1,
#  2 and 4 are the direct lane-0 cells, and tails of len 3, 5, 6 and 7 are rowed at the 8042 DATA port
#  0x60 (sessions 4f `tailr' / `tailw', since closing pass 2).  *** THIS SAID "split TAILS start at port
#  0x400, where nothing is mapped, so a tail cell shows only as a whole-access failure ... not rowed per
#  length" UNTIL CLOSING PASS 2, AND IT WAS MEASURED FALSE: tails start at EVERY port 0 mod 0x20 (the
#  8259 at 0x20/0xa0, the 8253 at 0x40, the 8042 at 0x60), and the Opus seat's tail mis-placement
#  mutant scored 77/77 because the split rows' tails at the unmapped 0x400 can show a decline but never
#  a position. ***
#
#  CONTRACT (clause e) -- the detector is DESIGNED to catch, on EITHER arm, at every cell of that space:
#  a byte placed at any position other than (P & 3) % len (a single-cell mis-decode included -- the
#  Opus closing seat's c1_w2, c1_w1w, c1_r4 each scored 51/51 before this repair); and, by name: the
#  removed exit reinstated at any of the six cells that ended the host (reads AND
#  writes at (1,2) (1,3) (2,3)); a decline beyond the width or at-and-beyond it, or of any lane-0 wide
#  access (a store dropped, a load's register kept); a store arm narrowed to len <= 2 or its stores
#  dropped or forwarded to another port; one arm folding and the other not; the byte placed at position 0
#  instead of (P & 3) % len (the clamp, anchored on (2,1) == (2,3)); a lane decode that drops bit 1 or
#  the `& 3', on the read arm or the write arm; `& (len - 1)' for `% len' (the len-3/5 split heads); a
#  byte replicated into every position, at len 2, 4 or 8; the read arm's success return turned into a
#  failure; the write arm's `return' removed, so a store falls into the read arm and makes a phantom
#  read of the stored port (x_wfallthru), and the read arm's forward DUPLICATED (RD2, a second read) -- together THE
#  FORWARD-COUNT CLASS, CLOSED BY ENUMERATION SINCE REPAIR 5 (flagship ruling, regress/artifacts/lcaisalane/
#  FABLE_C4_RULING_20260915.md, part B), in either form, unconditioned or gated on the width, the lane or the data:
#    DIRECT cells, 4 lanes x widths 1/2/4/8 x both arms -- every one rowed.  Lane 0: stores 4k `kbcq' (the 8042 data
#      port, one reply queued), loads 4l `rdq' (two replies queued).  Lane 1: both arms 4m `cmos' (CMOS REG C, whose
#      read clears it).  Lane 2: stores 4h `iir' / 4i `iirw', loads 4j `iirr' (len 1) and 4n `iirr2' (len 2/4/8) (IIR
#      0x3fa with TXRDY armed).  Lane 3: 4o `stub3' ALONE -- the 8042 PC-style stub at 0x63, an emulator-model oracle
#      (below).  4o `stub0'/`stub1'/`stub2' carry lanes 0-2 again as a strengthening, never as the sole carrier.
#    TAIL cells, widths 3/5/6/7 at lane 0 x both arms -- rowed at the 8042 data port 0x60 with the queue: 4p
#      `tailq_w' (one reply queued) and 4q `tailq_r' (two).  Tails of 1/2/4 are the direct lane-0 cells.
#    HEAD cells, widths 1-7 at lane 3 -- EQUIVALENT: the only mapped ports 0x1f mod 0x20 on this machine are 0x3ff and
#      0x2ff (ns16550 SCR, whose read returns d->reg[] with no side effect); 0x60-0x6f holds no 0x1f-mod-0x20 port.
#    DATA: every fallthrough row before repair 5 stored 0; the stub rows store 0x5a at every position and 4m stores 0x0f,
#      so the zero/nonzero partition is rowed on both sides (a strengthening, not floor -- the write body tests no bit
#      of the value); a fallthrough keyed on an EXACT value is disclosed by class.
#  SCOPE of that enumeration, stated because each is a premise: the machine AS PROBED (alphabook1, no IDE image so no
#  wdc at 0x1f0-0x1f7, no VGA without X11; the lpt read arm has no side effect -- checked by the flagship seat); the
#  width set is the memory_rw widths 1/2/4/8 plus the 1 KB split's heads (always lane 3) and tails (always lane 0);
#  `len == 0' is refused and DISCLOSED (no producer); a DIRECTION swap (a store forwarded as a read, or the reverse) is a
#  different class, caught by the value rows.  *** THE CHANNEL AT LANE 3 IS AN EMULATOR TODO: dev_pckbc.c's PC-style
#  branch answers 0x61-0x6f (but 0x64) from `static int x; x++;', bit 0x10 its parity.  If that port is ever implemented
#  the stub rows go green whatever the access count -- which is why every stub session opens with a LIVENESS row (two
#  flat reads must flip bit 0x10) that reds when the oracle disappears. ***
#  *** HISTORY, because each step was a wrong record in its turn: repair 4 SCOPED this entry to lane 2 and lane 0 at the
#  direct widths and DISCLOSED lane 1 and lane-3 direct; its lane-3 warrant ("no read-side-effect port is present on
#  this probe's machine") was MEASURED FALSE by the Opus closing-pass-4 seat (L3gate, the stub at 0x63), its RD2
#  sentence was unscoped while its one row was (1,2) (R2w escaped at len 2/4/8, 111/111), and it gave the tail cells no
#  disposition at all (WT6/WTsplit 111/111) -- grok had corrected the lane-1 and wdc halves hours earlier.  Before that,
#  "the write arm's `return' removed" stood here UNSCOPED while its rows sat at (1,2) and (4,2) only (W4, 93/93). ***
#  *** TABLE 1'S CONTRACT CLAIMED MOST OF THIS AT 37 ROWS AND WAS MEASURED FALSE: the Opus
#  pass-2 seat built ten mutants that scored 37/37, nine changing a guest outcome -- no row stored at len
#  4/8 -- and measured that the split heads it DISCLOSED as needing a translated access split on K0SEG. ***
#  DISCLOSED, not caught: the len-0 refusal (no producer); the zero-fill of the positions other than
#  `ofs' (p_nozero -- EQUIVALENT: memory_rw's #95 pre-zero already clears the buffer); an address-decode
#  edit above port 0x3ff (p_port10 -- not an edit of the fix; measured 51/51 by the Opus closing seat.
#  This said "every probed port is below 0x400", and the split TAILS reach port 0x400 -- grok and the
#  Opus seat, closing pass 1 -- so the premise was wrong and the scoping reason is the one that stands);
#  the DISCARDED sparse byte offset a<4:0> -- the size field a<4:3> included (lcaisasize) -- which the
#  handler shifts away, so an edit keyed on it (the Opus closing-pass-3 seat's H1b, keyed on a<4:0> =
#  0x1c: the 4-byte split head, 93/93; this said "a<4:2> = 0x1c", impossible for a 3-bit slice -- agy,
#  closing pass 4) is not seen [widened from "the size field a<4:3>" by the flagship
#  ruling, closing pass 3]; the hardware QUADWORD ENCODING's route (lcaisaqword: on the
#  21066 a<6:5> = 11 with a<4:3> = 11 is a quadword at port P, which the model forwards to P|3 -- NOT the
#  len-8 lane this probe rows, which follows the same (P & 3) % len rule as every other width); the
#  missing PHYSICAL (lcaisaphys); the end-of-window clamp at port 0xffff (nothing is mapped there).
#  Disclosed BY CLASS (closing pass 2; each measured 77/77 by the Opus seat, regress/artifacts/lcaisalane/
#  opus_c2_20260914/): a decline or mis-decode keyed on an EXACT PORT VALUE (kimi-k3's `relative_addr ==
#  0x400 && len == 4' -- the p_port10 class: the body never tests the port against a constant); a
#  mis-decode keyed on the DATA (codex's `ofs == 2 && !data[2]', generally `data[ofs] ? data[ofs] :
#  data[0]' -- every VALUE store row carries a NONZERO correct byte and the `iir', `iirw' and `kbcq' rows
#  store all-zero words, so no row distinguishes a zero correct byte from a nonzero byte beside it [the
#  `iirw'/`kbcq' zero stores added to this list 2026-09-15 from closing pass 4 (codex, kimi CLI); a sentence
#  "'the correct byte is 0' is unrowed" stood here and was dropped as imprecise by the flagship ruling]).  [Corrected 2026-09-14 from closing pass 3 (codex, grok, kimi-k3): this said
#  "every store row carries a NONZERO correct byte", false since session 4h stores zero.]  EQUIVALENT on alphabook1, named: the inner forward's return value honoured on the
#  read arm, or forced to success on the write arm -- no ISA device there fails an access, and an
#  unmapped forward returns success with a zero fill.
#  EQUIVALENT by construction, named so no table is spent on them (kimi-k3, pass 2): restoring the dead
#  `% len' on the write arm's index (`ofs' is already reduced), and reinstating `if (ofs > len) exit(1)'
#  AFTER the fold (unsatisfiable once ofs < len) -- the reinstated exit that matters is on the UNFOLDED
#  lane, which the table's m_exit builds.
#
#  *** ```

## THE REPAIR DIFF -- the 111-row instrument -> the 185-row instrument (`git diff --no-index`, verbatim; 5 hunks)

```diff
diff --git "a/C:\\DocumentNoSnc\\CC\\GXEMUL\\GXEMUL-SEC\\regress\\artifacts\\lcaisalane\\fix530_20260914\\table5\\lca_isalane_probe.table5.py" "b/C:\\DocumentNoSnc\\CC\\GXEMUL\\GXEMUL-SEC\\regress\\lca_isalane_probe.py"
index 0be08a1..6c0eca2 100644
--- "a/C:\\DocumentNoSnc\\CC\\GXEMUL\\GXEMUL-SEC\\regress\\artifacts\\lcaisalane\\fix530_20260914\\table5\\lca_isalane_probe.table5.py"
+++ "b/C:\\DocumentNoSnc\\CC\\GXEMUL\\GXEMUL-SEC\\regress\\lca_isalane_probe.py"
@@ -70,3 +70,3 @@
 #  closing pass 2's tail cells and phantom-read rows (93 rows) its table 4; after closing pass 3's
-#  fallthrough class closure (111 rows) its table 5.
+#  fallthrough rows (111 rows) its table 5; after closing pass 4's forward-count CLASS CLOSURE (185 rows) its table 6.
 #
@@ -98,15 +98,32 @@
 #  failure; the write arm's `return' removed, so a store falls into the read arm and makes a phantom
-#  read of the stored port (x_wfallthru -- the `iir' rows, since closing pass 2: every port stored to
-#  before then read back without a side effect, so it scored 77/77 and was called disclosed by table 3's
-#  PRETABLE/POSTTABLE only, never here) -- SCOPED since closing pass 3 (flagship ruling, option (c)): that
-#  edit, and the same edit gated on the width or the lane, is caught at LANE 2 at every direct width (4h
-#  `iir', 4i `iirw': IIR 0x3fa with TXRDY armed) and at LANE 0 at every direct width (4k `kbcq': the 8042
-#  data port with a reply queued); at the split-HEAD cells it is EQUIVALENT on alphabook1 (heads land on
-#  ports 0x1f mod 0x20 -- 0x3ff SCR, or unmapped -- none with a read side effect); at LANE 1 (no port
-#  with an armable read side effect is rowed) and at LANE-3 DIRECT (the wdc status port 0x1f7 would carry
-#  it with an IRQ pending; not rowed) it is DISCLOSED.  *** "The write arm's `return' removed" stood here
-#  UNSCOPED while its rows sat at (1,2) and (4,2) only, and the Opus closing-pass-3 seat MEASURED four
-#  gated forms at 93/93 -- W4 exempts exactly those two widths. ***  And the read arm's forward DUPLICATED
-#  (RD2 -- a second phantom read; outside the contract as first written, rowed since repair 4 at IIR,
-#  4j `iirr').  *** TABLE 1'S CONTRACT CLAIMED MOST OF THIS AT 37 ROWS AND WAS MEASURED FALSE: the Opus
+#  read of the stored port (x_wfallthru), and the read arm's forward DUPLICATED (RD2, a second read) -- together THE
+#  FORWARD-COUNT CLASS, CLOSED BY ENUMERATION SINCE REPAIR 5 (flagship ruling, regress/artifacts/lcaisalane/
+#  FABLE_C4_RULING_20260915.md, part B), in either form, unconditioned or gated on the width, the lane or the data:
+#    DIRECT cells, 4 lanes x widths 1/2/4/8 x both arms -- every one rowed.  Lane 0: stores 4k `kbcq' (the 8042 data
+#      port, one reply queued), loads 4l `rdq' (two replies queued).  Lane 1: both arms 4m `cmos' (CMOS REG C, whose
+#      read clears it).  Lane 2: stores 4h `iir' / 4i `iirw', loads 4j `iirr' (len 1) and 4n `iirr2' (len 2/4/8) (IIR
+#      0x3fa with TXRDY armed).  Lane 3: 4o `stub3' ALONE -- the 8042 PC-style stub at 0x63, an emulator-model oracle
+#      (below).  4o `stub0'/`stub1'/`stub2' carry lanes 0-2 again as a strengthening, never as the sole carrier.
+#    TAIL cells, widths 3/5/6/7 at lane 0 x both arms -- rowed at the 8042 data port 0x60 with the queue: 4p
+#      `tailq_w' (one reply queued) and 4q `tailq_r' (two).  Tails of 1/2/4 are the direct lane-0 cells.
+#    HEAD cells, widths 1-7 at lane 3 -- EQUIVALENT: the only mapped ports 0x1f mod 0x20 on this machine are 0x3ff and
+#      0x2ff (ns16550 SCR, whose read returns d->reg[] with no side effect); 0x60-0x6f holds no 0x1f-mod-0x20 port.
+#    DATA: every fallthrough row before repair 5 stored 0; the stub rows store 0x5a at every position and 4m stores 0x0f,
+#      so the zero/nonzero partition is rowed on both sides (a strengthening, not floor -- the write body tests no bit
+#      of the value); a fallthrough keyed on an EXACT value is disclosed by class.
+#  SCOPE of that enumeration, stated because each is a premise: the machine AS PROBED (alphabook1, no IDE image so no
+#  wdc at 0x1f0-0x1f7, no VGA without X11; the lpt read arm has no side effect -- checked by the flagship seat); the
+#  width set is the memory_rw widths 1/2/4/8 plus the 1 KB split's heads (always lane 3) and tails (always lane 0);
+#  `len == 0' is refused and DISCLOSED (no producer); a DIRECTION swap (a store forwarded as a read, or the reverse) is a
+#  different class, caught by the value rows.  *** THE CHANNEL AT LANE 3 IS AN EMULATOR TODO: dev_pckbc.c's PC-style
+#  branch answers 0x61-0x6f (but 0x64) from `static int x; x++;', bit 0x10 its parity.  If that port is ever implemented
+#  the stub rows go green whatever the access count -- which is why every stub session opens with a LIVENESS row (two
+#  flat reads must flip bit 0x10) that reds when the oracle disappears. ***
+#  *** HISTORY, because each step was a wrong record in its turn: repair 4 SCOPED this entry to lane 2 and lane 0 at the
+#  direct widths and DISCLOSED lane 1 and lane-3 direct; its lane-3 warrant ("no read-side-effect port is present on
+#  this probe's machine") was MEASURED FALSE by the Opus closing-pass-4 seat (L3gate, the stub at 0x63), its RD2
+#  sentence was unscoped while its one row was (1,2) (R2w escaped at len 2/4/8, 111/111), and it gave the tail cells no
+#  disposition at all (WT6/WTsplit 111/111) -- grok had corrected the lane-1 and wdc halves hours earlier.  Before that,
+#  "the write arm's `return' removed" stood here UNSCOPED while its rows sat at (1,2) and (4,2) only (W4, 93/93). ***
+#  *** TABLE 1'S CONTRACT CLAIMED MOST OF THIS AT 37 ROWS AND WAS MEASURED FALSE: the Opus
 #  pass-2 seat built ten mutants that scored 37/37, nine changing a guest outcome -- no row stored at len
@@ -119,4 +136,5 @@
 #  the DISCARDED sparse byte offset a<4:0> -- the size field a<4:3> included (lcaisasize) -- which the
-#  handler shifts away, so an edit keyed on it (the Opus closing-pass-3 seat's H1b, keyed on a<4:2> =
-#  0x1c: the 4-byte split head, 93/93) is not seen [widened from "the size field a<4:3>" by the flagship
+#  handler shifts away, so an edit keyed on it (the Opus closing-pass-3 seat's H1b, keyed on a<4:0> =
+#  0x1c: the 4-byte split head, 93/93; this said "a<4:2> = 0x1c", impossible for a 3-bit slice -- agy,
+#  closing pass 4) is not seen [widened from "the size field a<4:3>" by the flagship
 #  ruling, closing pass 3]; the hardware QUADWORD ENCODING's route (lcaisaqword: on the
@@ -129,5 +147,6 @@
 #  mis-decode keyed on the DATA (codex's `ofs == 2 && !data[2]', generally `data[ofs] ? data[ofs] :
-#  data[0]' -- every VALUE store row carries a NONZERO correct byte and the `iir' rows store all-zero
-#  words, so at no store cell does a row hold a zero correct byte beside a nonzero neighbour; "the correct
-#  byte is 0" is unrowed).  [Corrected 2026-09-14 from closing pass 3 (codex, grok, kimi-k3): this said
+#  data[0]' -- every VALUE store row carries a NONZERO correct byte and the `iir', `iirw' and `kbcq' rows
+#  store all-zero words, so no row distinguishes a zero correct byte from a nonzero byte beside it [the
+#  `iirw'/`kbcq' zero stores added to this list 2026-09-15 from closing pass 4 (codex, kimi CLI); a sentence
+#  "'the correct byte is 0' is unrowed" stood here and was dropped as imprecise by the flagship ruling]).  [Corrected 2026-09-14 from closing pass 3 (codex, grok, kimi-k3): this said
 #  "every store row carries a NONZERO correct byte", false since session 4h stores zero.]  EQUIVALENT on alphabook1, named: the inner forward's return value honoured on the
@@ -837,2 +856,136 @@ print("")
 
+#  ---- SESSIONS 4l-4q (#530 closing pass 4, REPAIR 5 -- the forward-count CLASS CLOSURE) --------------------------
+#  Closing pass 4 found the class a THIRD consecutive time, each escape guest-visible at 111/111 (the Opus seat,
+#  regress/artifacts/lcaisalane/opus_c4_20260914/): RD2 gated on the width (only (1,2) was rowed), the split-TAIL cells,
+#  lane-0 reads, lane-3 direct.  The flagship ruling (regress/artifacts/lcaisalane/FABLE_C4_RULING_20260915.md, part B)
+#  owes the enumeration DERIVED FROM THE HANDLER in one diff: its two arms (a store's phantom read after the forward; a
+#  load's forward duplicated) x every width kind x every lane.  Each observable cell below has a row, on an ARCHITECTURAL
+#  channel at lanes 0-2 and on the 8042 stub counter at lane 3 (the only lane-3 port with an access side effect on this
+#  machine); the stub also carries lanes 0-2 as a strengthening, never as the sole carrier.  Heads are EQUIVALENT (below).
+#
+#  4l `rdq': LANE-0 READS, direct widths 1/2/4/8.  Two self-test replies queued, one lca load of SP(0x60), then the flat
+#  status: DIB must still be 1 (a duplicated read pops both).  Each phase drains the survivor with a flat data read.  The
+#  control shows the channel counts pops: after two replies and ONE flat pop DIB is 1, after a second pop it is 0.
+def selftest(): return [LDQ(T1, 0, T0), LDQ(T2, 8, T0), STB(T2, 0, T1)]             # queue one 0x55 (slot 0 = cmd port)
+def kstatus(reg): return [LDQ(T1, 0, T0)] + sent(reg) + [LDBU(reg, 0, T1)]           # flat status (DIB = bit 0)
+def kpop(): return [LDQ(T1, 16, T0), LDBU(T5, 0, T1)]                                # flat data read (slot 2) pops one
+C4l = [k0(FLAT(KBC_CMD)), KBC_SELFTEST, k0(FLAT(KBC_DAT)), k0(SP(KBC_DAT))]
+P4l = [(selftest() + selftest() + kpop() + kstatus(T4), "t4"),                        # control: one of two left
+       (kpop() + kstatus(T4), "t4")]                                                  # control: none left
+for w, n, ld, _ in (("b", 1, LDBU, STB), ("w", 2, LDWU, STW), ("l", 4, LDL, STL), ("q", 8, LDQ, STQ)):
+    P4l.append((selftest() + selftest() + [LDQ(T1, 24, T0)] + sent(T3) + [ld(T3, 0, T1)] + kstatus(T4) + kpop(), "t4"))
+a4l, g4l = dsession("rdq", C4l, P4l, ["ctl1", "ctl0", "r1", "r2", "r4", "r8"])
+dibv = lambda v: None if v is None else v & 0x01
+row("rdq alive", "alive" if a4l else "dead", "alive", "CONTROL")
+row("rdq ctl1", hx(dibv(g4l["ctl1"])), hx(0x01), "CONTROL: two replies queued, one flat pop -> one left (DIB 1)")
+row("rdq ctl0", hx(dibv(g4l["ctl0"])), hx(0x00), "CONTROL: a second flat pop empties it (DIB 0): the channel counts pops")
+for n in (1, 2, 4, 8):
+    row("rdq r%d" % n, hx(dibv(g4l["r%d" % n])), hx(0x01),
+        "(%d,0) LOAD SP(0x60) pops ONE of two replies (RD2: the read forward duplicated)" % n)
+print("")
+
+#  4m `cmos': LANE 1, both arms, direct widths 1/2/4/8, on CMOS register C through the pccmos index/data pair (select
+#  0x0c at 0x70; 0x71 forwards to dev_mc146818.c, whose REG C read returns the register and then ZEROES it, and whose
+#  store sets it).  The stored value is 0x0f and every compare masks 0x0f: the mc146818 access path ORs UF/AF/PF/IRQF
+#  (0xf0) into REG C from the HOST CLOCK, so only the low nibble is deterministic.  Store rows: an lca store of 0x0f
+#  must still read back 0x0f (a phantom read after the store clears it).  Load rows: after a flat store of 0x0f the lca
+#  load must deliver 0x0f at lane position (1 % len) (a duplicated forward delivers the second, cleared, read).
+CMOS_VAL = 0x0f0f0f0f0f0f0f0f
+def csel(): return [LDQ(T1, 0, T0), LDQ(T2, 8, T0), STB(T2, 0, T1)]                   # select REG C (flat 0x70)
+def cset(): return csel() + [LDQ(T1, 24, T0), LDQ(T3, 32, T0), STB(T3, 0, T1)]        # flat store 0x0f -> REG C
+def cget(reg): return csel() + [LDQ(T1, 24, T0)] + sent(reg) + [LDBU(reg, 0, T1)]     # flat read REG C (clears it)
+C4m = [k0(FLAT(0x70)), 0x0c, k0(SP(0x71)), k0(FLAT(0x71)), CMOS_VAL]
+P4m = [(cset() + cget(T4), "t4"), (cget(T4), "t4")]                                   # controls: set, then cleared
+for w, n, ld, st in (("b", 1, LDBU, STB), ("w", 2, LDWU, STW), ("l", 4, LDL, STL), ("q", 8, LDQ, STQ)):
+    P4m.append((csel() + [LDQ(T1, 16, T0), LDQ(T3, 32, T0), st(T3, 0, T1)] + cget(T4), "t4"))       # lca STORE
+for w, n, ld, st in (("b", 1, LDBU, STB), ("w", 2, LDWU, STW), ("l", 4, LDL, STL), ("q", 8, LDQ, STQ)):
+    P4m.append((cset() + csel() + [LDQ(T1, 16, T0)] + sent(T4) + [ld(T4, 0, T1)], "t4"))           # lca LOAD
+a4m, g4m = dsession("cmos", C4m, P4m, ["set", "clr", "w1", "w2", "w4", "w8", "r1", "r2", "r4", "r8"])
+nib = lambda v, sh=0: None if v is None else (v >> sh) & 0x0f
+row("cmos alive", "alive" if a4m else "dead", "alive", "CONTROL")
+row("cmos set", hx(nib(g4m["set"])), hx(0x0f), "CONTROL: a flat store of 0x0f to REG C reads back 0x0f")
+row("cmos clr", hx(nib(g4m["clr"])), hx(0x00), "CONTROL: that read cleared it -- the channel sees ONE extra read")
+for n in (1, 2, 4, 8):
+    row("cmos w%d" % n, hx(nib(g4m["w%d" % n])), hx(0x0f),
+        "(%d,1) STORE 0x0f.. -> SP(0x71): REG C keeps it (x_wfallthru: a phantom read clears it)" % n)
+for n in (1, 2, 4, 8):
+    row("cmos r%d" % n, hx(nib(g4m["r%d" % n], 8 * (1 % n))), hx(0x0f),
+        "(%d,1) LOAD SP(0x71) delivers REG C = 0x0f at position %d (RD2: the second read is cleared)" % (n, 1 % n))
+print("")
+
+#  4n `iirr2': LANE-2 READS at widths 2/4/8 -- a NEW session, `iirr' (the (1,2) read) is left as it was.  Re-arm TXRDY
+#  before each load; the lane-2 byte of the loaded value must be IIR & 3 = TXRDY (a duplicated read clears it first).
+C4n = [k0(FLAT(UART_IER)), k0(SP(UART_IIR))]
+P4n = [(iir_arm() + [LDQ(T1, 8, T0)] + sent(T4) + [ld(T4, 0, T1)], "t4") for ld in (LDWU, LDL, LDQ)]
+a4n, g4n = dsession("iirr2", C4n, P4n, ["r2", "r4", "r8"])
+row("iirr2 alive", "alive" if a4n else "dead", "alive", "CONTROL")
+for n, sh in ((2, 0), (4, 16), (8, 16)):
+    v = g4n["r%d" % n]
+    row("iir lca rd%d" % n, hx(None if v is None else (v >> sh) & 0x03), hx(0x02),
+        "(%d,2) LOAD SP(0x3fa) after arming: TXRDY at position %d, read ONCE (R2w: RD2 gated on len)" % (n, 2 % n))
+print("")
+
+#  4o `stub0'-`stub3': the 8042 PC-style STUB.  dev_pckbc.c answers every port of 0x61-0x6f except 0x64 from a
+#  FUNCTION-STATIC counter (`static int x; x++;') bumped on EVERY access, read or write, with bit 0x10 its parity -- a
+#  "TODO (port 0x61)", an EMULATOR-MODEL oracle, not an architectural register (like the 0xffffffff absent-device
+#  signature).  Flat read, ONE lca access, flat read: the two flat answers agree in bit 0x10; an extra access flips it.
+#  The flats are chained, so each row brackets exactly one lca access.  Stores carry 0x5a at every byte position, so
+#  the data-keyed fallthrough (dataA: the fallthrough only on a NONZERO byte) is inside the rows.  Lane 3 (0x63) is the
+#  SOLE carrier of its cells; lanes 0-2 (0x68, 0x61, 0x62) are a strengthening beside 4k/4l/4m/4h-4j/4n.
+#  *** LIVENESS, and it is MANDATORY: if port 0x61 is ever implemented every stub row goes green whatever the access
+#  count.  Each session opens with two flat reads and NO lca access between them, which MUST flip bit 0x10. ***
+STUB_DATA = 0x5a5a5a5a5a5a5a5a
+for lane, port in ((3, 0x63), (0, 0x68), (1, 0x61), (2, 0x62)):
+    C = [k0(FLAT(port)), k0(SP(port)), STUB_DATA]
+    def sflat(): return [LDQ(T1, 0, T0)] + sent(T2) + [LDBU(T2, 0, T1)]
+    P = [(sflat(), "t2"), (sflat(), "t2")]
+    names = ["f0", "f1"]
+    for w, n, ld, st in (("b", 1, LDBU, STB), ("w", 2, LDWU, STW), ("l", 4, LDL, STL), ("q", 8, LDQ, STQ)):
+        P.append(([LDQ(T1, 8, T0)] + sent(T3) + [ld(T3, 0, T1)] + sflat(), "t2"))
+        names.append("r%d" % n)
+        P.append(([LDQ(T1, 8, T0), LDQ(T3, 16, T0), st(T3, 0, T1)] + sflat(), "t2"))
+        names.append("w%d" % n)
+    a, g = dsession("stub%d" % lane, C, P, names)
+    flip = lambda x, y: None if x is None or y is None else (x ^ y) & 0x10
+    row("stub%d alive" % lane, "alive" if a else "dead", "alive", "CONTROL")
+    row("stub%d live" % lane, hx(flip(g["f0"], g["f1"])), hx(0x10),
+        "LIVENESS: two flat reads of 0x%x flip bit 4 -- the stub's access counter is present" % port)
+    prev = "f1"
+    for nm in names[2:]:
+        n = int(nm[1:])
+        row("stub%d %s" % (lane, nm), hx(flip(g[prev], g[nm])), hx(0x00),
+            "(%d,%d) %s SP(0x%x): ONE access reaches the port (%s)"
+            % (n, lane, "LOAD" if nm[0] == "r" else "STORE 0x5a..", port,
+               "RD2" if nm[0] == "r" else "x_wfallthru, nonzero byte"))
+        prev = nm
+    print("")
+
+#  4p `tailq_w' / 4q `tailq_r': the split-TAIL cells, widths 3/5/6/7 at LANE 0 (a tail always starts at a port 0 mod
+#  0x20; here the 8042 data port 0x60).  `tailw' (4f) stores into an EMPTY queue, so a phantom read there changes nothing
+#  -- WT6/WTsplit scored 111/111.  WRITE tails: one reply queued, 0xd1 (the next data write goes to output_byte), the
+#  split STQ's tail forwards 0, and the flat status DIB must still be 1.  READ tails: two replies queued, the split LDQ's
+#  tail pops ONE, DIB must still be 1.  Each phase drains the survivor with a flat data read.
+C4p = [k0(FLAT(KBC_CMD)), KBC_SELFTEST, k0(FLAT(KBC_DAT)), KBC_WROUTPORT] + [k0(SP(0x5f) + o) for _, o in TAILHEADS]
+def wrout(): return [LDQ(T1, 0, T0), LDQ(T2, 24, T0), STB(T2, 0, T1)]                # 0xd1 -> the command port
+P4p = [(selftest() + kstatus(T4) + kpop(), "t4")]                                     # control: one reply queued
+for i in range(len(TAILHEADS)):
+    P4p.append((selftest() + wrout() + [LDQ(T1, 32 + 8 * i, T0), STQ(ZERO, 0, T1)] + kstatus(T4) + kpop(), "t4"))
+a4p, g4p = dsession("tailq_w", C4p, P4p, ["ctl"] + ["t%d" % (8 - h) for h, _ in TAILHEADS])
+row("tailq w alive", "alive" if a4p else "dead", "alive", "CONTROL")
+row("tailq w ctl", hx(dibv(g4p["ctl"])), hx(0x01), "CONTROL: a queued reply sets DIB")
+for h, _ in TAILHEADS:
+    row("tailq w t%d" % (8 - h), hx(dibv(g4p["t%d" % (8 - h)])), hx(0x01),
+        "(%d,0) STQ TAIL at 0x60: the queued reply survives the store (x_wfallthru at a tail width)" % (8 - h))
+P4q = [(selftest() + selftest() + kpop() + kstatus(T4) + kpop(), "t4")]               # control: one of two left
+for i in range(len(TAILHEADS)):
+    P4q.append((selftest() + selftest() + [LDQ(T1, 32 + 8 * i, T0)] + sent(T3) + [LDQ(T3, 0, T1)]
+                + kstatus(T4) + kpop(), "t4"))
+a4q, g4q = dsession("tailq_r", C4p, P4q, ["ctl"] + ["t%d" % (8 - h) for h, _ in TAILHEADS])
+row("tailq r alive", "alive" if a4q else "dead", "alive", "CONTROL")
+row("tailq r ctl", hx(dibv(g4q["ctl"])), hx(0x01), "CONTROL: two replies queued, one flat pop -> one left")
+for h, _ in TAILHEADS:
+    row("tailq r t%d" % (8 - h), hx(dibv(g4q["t%d" % (8 - h)])), hx(0x01),
+        "(%d,0) LDQ TAIL at 0x60 pops ONE of two replies (RD2 at a tail width pops both)" % (8 - h))
+print("")
+
 #  ---- SESSIONS 5-10: the six cells that ENDED THE HOST on HEAD, one process each -------------
```

## THE MEASURING SEAT'S ENUMERATION (closing pass 4, Q1) -- what repair 5 implements

## Q1 -- THE ENUMERATION, checked against alphabook1's ISA devices

### What is on the bus

This is from `bus_isa_init` with `BUS_ISA_IDE0 | BUS_ISA_IDE1` (`dev_lca.c`) and the device lengths.

| device | ports |
|---|---|
| 8259 | 0x20-0x21 and 0xa0-0xa1 |
| 8253 | 0x40-0x43 |
| 8042 (`pckbc`, `DEV_PCKBC_LENGTH` 0x10) | **0x60-0x6f** |
| pccmos | 0x70-0x71 |
| ns16550 | 0x3f8-0x3ff and 0x2f8-0x2ff |
| lpt | 0x378-0x37a |

* No FDC is present (flag not set), and no VGA without X11.
* **wdc0 and wdc1 are added ONLY `if (diskimage_exist(machine, n, DISKIMAGE_IDE))` (`bus_isa.c`).**  The probe loads `0x20000000:alpha_dummy.bin`, which is not a disk.  So **0x1f0-0x1f7 and 0x170-0x177 are UNMAPPED on the probe's machine.**  grok is right.

### Read (access) side effects, by lane

Each is read from the source; "MEASURED" means a discriminator channel shows it.

| lane | port(s) with an access side effect | status |
|---|---|---|
| 0 | 8042 data 0x60 (the pop; with TWO replies queued, a second read pops the second: **D, MEASURED**); **8042 PC-style stub 0x68/0x6c** (below); 8253 counter 0 at 0x40 (16-bit flip-flop); RBR 0x3f8/0x2f8 (`console_readchar`) | observable |
| 1 | **stub 0x61/0x65/0x69/0x6d (E, MEASURED)**; **8253 counter 1 at 0x41 after a LSB+MSB control word (F, MEASURED)**; **CMOS 0x71 with REG C selected, where a read clears it and a store sets it (G, MEASURED)** | observable, no arming needed at 0x61 |
| 2 | IIR 0x3fa/0x2fa (clears TXRDY: A/B, MEASURED); stub 0x62/0x66/0x6a/0x6e (E, MEASURED); 8253 counter 2 at 0x42 | observable |
| 3 direct | **stub 0x63/0x67/0x6b/0x6f (E, MEASURED)**.  wdc 0x1f7 only with an IDE image | observable, no arming needed |
| 3 split heads (P = 0x1f mod 0x20) | mapped head ports are **0x3ff and 0x2ff only**, both ns16550 SCR (the `default:` arm, inert).  0x1f..0x3df, 0x5f, 0x7f and so on are unmapped; the stub's 0x60-0x6f holds no 0x1f-mod-0x20 port | **EQUIVALENT**.  Still true with IDE images: wdc and altstatus add no 0x1f-mod-0x20 port |
| 0 split tails (P = 0 mod 0x20) | 0x20 and 0xa0 (8259: its read arm only reads irr/isr, inert); **0x40** (8253 counter 0); **0x60** (8042: C and D, MEASURED); 0x300 and 0x400 unmapped | observable at 0x40 and 0x60 |

**The stub.**

* `DEVICE_ACCESS(pckbc)`, PC-style branch, reads `if (relative_addr != 0 && relative_addr != 4) { /* TODO (port 0x61) */ odata = 0x21; { static int x = 0; x++; if (x&1) odata ^= 0x10; } ... return 1; }`.
* That is **a function-static counter bumped on EVERY access to 0x61-0x63 and 0x65-0x6f, read or write**, and bit 0x10 of the answer is its parity.
* So on base, a flat read, then ONE lca access, then a flat read leaves bit 4 unchanged.  One extra access flips it.
* The control channel (two plain reads flip 0x10) is live on every binary: `ctl=0x10` in all 11 discriminator logs.

### Answers to the Q1 sub-questions

**Heads EQUIVALENT: correct.**

**Lane-1 DISCLOSED: the classification is right, and the ORIGINAL warrant was false.**

* The original header said "no port with an armable read side effect".
* 0x61 needs no arming, and 0x41 and 0x71 need one store each.
* The coordinator's 00:19 correction states this accurately, and I measured all three.

**Lane-3 direct: the classification is DISCLOSED, and the CORRECTED warrant is FALSE.**

* The 00:19 header now says "LANE-3 DIRECT (no read-side-effect port is present on this probe's machine ...)".
* That is measured false.  L3gate flips E tog63.
* See Q3.3.

**The rows' channels vary under their named mutants.**

* `kbcq * pre` = 0x1 on base: one reply is queued, and Wpure pops it.
* `iirw ctl` / `iir ctl` = 0x2: TXRDY is armed, and Wpure clears it.
* No vacuous row was found.

### The complete (arm x width-kind x lane) enumeration of the forward-count class

"Observable" means observable on alphabook1 as the probe configures it.  "Rowed" means rowed in the 111-row instrument.

| arm | width-kind | lane | observable? | rowed? | cheapest channel (measured where noted) |
|---|---|---|---|---|---|
| write (phantom read after store) | direct 1/2/4/8 | 0 | yes | **yes** (`kbcq b/w/l/q`), ZERO data only | also stub 0x68 (E) |
| write | direct | 1 | **yes** | no, disclosed | stub 0x61 (E); 8253 0x41 (F); REG C (G) |
| write | direct | 2 | yes | **yes** (`iir`/`iirw` x4), ZERO data only | also stub 0x62 (E) |
| write | direct | 3 | **yes** | no, disclosed with a false warrant | stub 0x63 (E) |
| write | head 1..7 | 3 | no | -- | **EQUIVALENT** (0x3ff/0x2ff SCR) |
| write | **tail 3/5/6/7** (tails 1/2/4 are the direct lane-0 cells) | 0 | **yes** | **no -- UNCLASSIFIED** (not caught, not equivalent, not disclosed) | 8042 with one reply queued, then 0xd1, then a split store (C) |
| read (duplicated forward) | direct | 0 | **yes** | **no -- UNCLASSIFIED** | 8042 with TWO replies queued (D); stub 0x68 (E-load) |
| read | direct | 1 | **yes** | no, unclassified | stub 0x61 (E-load, via R2w) |
| read | direct | 2 | yes | **len 1 only** (`iir lca rd`); **2/4/8 NOT** | IIR (B); stub 0x62 |
| read | direct | 3 | **yes** | no, unclassified | stub 0x63 (E-load, via R2w) |
| read | head 1..7 | 3 | no | -- | **EQUIVALENT** (SCR) |
| read | **tail 3/5/6/7** | 0 | **yes** | **no -- UNCLASSIFIED** | 8042 with two replies (D, measured at tail 6) |

**Cheapest whole-class closure: one diff, new sessions only, so no earlier kill moves.**

* **Direct cells, 4 lanes x 4 widths x 2 arms = 32 cells.**
  * Use the stub at 0x68 / 0x61 / 0x62 / 0x63.
  * Each row is: flat read, then ONE lca access, then flat read; want `(a ^ b) & 0x10 == 0`.
  * Add one liveness row per session: two plain flat reads, want a flip of 0x10.
  * It needs no arming, does not care about the data value, and needs no queue.  About four sessions.
* **Tail cells, 4 widths x 2 arms = 8 cells.**
  * These are the C and D channels: 8042 queue plus a split access at SP(0x5f) + 0x1f / 0x1e / 0x1d / 0x1b.
  * Tails start at 0x60, the data port, not in the stub's range.  0x40 (8253) is the alternative.
* **Heads.**  Disclose EQUIVALENT with the mapped-port list: 0x3ff and 0x2ff SCR, and 0x60-0x6f contains no 0x1f-mod-0x20 port.
* **Store a NONZERO byte in the stub rows.**  The stub ignores store data.  The existing zero-store `iir`/`kbcq` rows then keep dataB red, and the nonzero stub stores red dataA.  So the data axis is closed for free.
* **Caution, and it is why the liveness row is mandatory.**
  * The stub is an emulator TODO.  If port 0x61 is ever implemented properly, every stub row goes vacuous silently, because `a == b` whatever the access count.
  * The liveness row reds when that happens.
  * The 8253 route (lanes 0-2) is architectural and survives such a change, but it cannot reach lane 3.  On this machine only the stub reaches lane 3.

---



## THE FLAGSHIP RULING, PART B (closing pass 4)

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


## KILL TABLE 6 on the 185-row instrument -- POSTTABLE

```
POSTTABLE -- #530 (lcaisalane) kill table 6, CLOSING PASS 4's REPAIR 5 -- the forward-count CLASS CLOSURE (185 rows).
Written after the table (table6.out ends KILL530F_DONE); PRETABLE.out 04:57:26 predates FIX_r6/HEAD_r6's analysis, the
launch (kill530f.run-051033.sh) and every log (probe_base.raw 05:30:25).

DRIVER   kill530f.run-051033.sh (frozen), clone /tmp/gxlca530 (BASELINE_CMP CLEAN), own .MUTANT; 14 legs built; clone
         RESTORED (re-checked by hand: no .MUTANT, dev_lca.c cmp-clean vs GXEMUL-SEC, gxemul -nt source); `restored ==
         base (byte-identical)'; no mutant binary identical to base.
INSTRUMENT  lca_isalane_probe.table6.py BYTE-IDENTICAL to the shipped regress/lca_isalane_probe.py (cmp, after the table)
         and to the frozen copy FIX_r6 / HEAD_r6 ran (../lca_isalane_probe.r6.frozen.py): FIX_r6 185/185, HEAD_r6 112/185
         -- EXACTLY the 30 new reds ../PREDICT_r6.out named before they ran (cmos r1, iir lca rd2, stub2 x9, stub3 x9,
         tailq w x5, tailq r x5), no retries.
LOGS     14 logs/probe_*.raw, every one ends LCAISALANE_DONE; LCAISALANE_RETRIED=none on every leg.
LOAD     two probe lanes beside #529's kill table 10 (four lanes) -- no retries.

check_pred.out:  CHECKPRED exact=14 differs=0 of 14 measured (14 predicted)
   base 185/185 · Wpure 153 · dataA 165 · dataB 173 · L1gate 177 · L3gate 181 · WT6 184 · WTsplit 181 · R2w 160 ·
   R2w2 178 · RD2L0 173 · RD2L1 177 · RD2L3 181 · RD2 153 -- every red set EXACTLY the PRETABLE's (check_pred.py holds
   them as Python sets).  The Opus closing-pass-4 seat's ten, each 111/111 on the 111-row probe except Wpure/dataB, are
   all DETECTED: R2w (the contract-named RD2 gated on width) on 25 rows, WT6 on `tailq w t6' alone, the tails, lane 0,
   lane 1 and lane 3 on their own sessions; dataA (the data-keyed fallthrough) on the 20 nonzero stores; RD2L1 and RD2L3,
   which the flagship ruling said "covered by construction is a prediction -- BUILD them", red on cmos r*/stub1 r* and
   stub3 r* as predicted.  Each chained stub row reds exactly ONE row per extra access, as the PRETABLE derived.

FLOOR    (a) HEAD_r6 112/185; the forward-count class CLOSED BY ENUMERATION (the contract's three-part table: DIRECT cells
         4 lanes x 4 widths x 2 arms, every one rowed; TAIL cells 3/5/6/7 x 2 arms, rowed at the 8042 queue; HEAD cells
         EQUIVALENT with the mapped-port derivation), lanes 0-2 on architectural channels and lane 3 on the stub with its
         LIVENESS row; the data axis's zero/nonzero partition rowed on both sides; four scope sentences.
NOT RE-MEASURED  every table 1-5 kill: repair 5 ADDS sessions and changes no existing session's commands (the targeting
         rule).
```

## QUESTIONS

1. **Is the enumeration complete and correctly classified?**  Arms {store's phantom read, load's duplicated forward} x
   width kinds {direct 1/2/4/8, split head 1-7 (lane 3), split tail 1-7 (lane 0)} x lanes 0-3.  Name any cell the contract
   does not dispose of (rowed / EQUIVALENT / out of scope), any head port that DOES have an access side effect, and any
   scope sentence that is false.
2. **Can each new row's channel vary under the mutant it names?**  stub rows need the counter to bump on EVERY access
   (and the liveness row to fail if it stops); cmos rows need REG C's read to clear it and its store to set it, with the
   0xf0 host-clock bits masked; rdq/tailq rows need exactly one or two replies queued; iirr2 needs TXRDY re-armed per phase.
3. **Is there a GAP -- an edit to the FIXED handler that scores 185/185 and changes a guest-visible outcome?**  As an exact
   edit, the row you expected to catch it and why it cannot.
4. **Which statement in the header, the fix comment, PREDICT_r6 or POSTTABLE 6 is wrong?**


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
