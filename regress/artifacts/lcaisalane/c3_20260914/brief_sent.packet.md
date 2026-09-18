# CLOSING PASS 3 on the #530 REPAIR 3 -- `lcaisalane`: is the 93-row detector now complete for its contract?  Liveness token `LCA530_C3_20260914`.

VERDICT LINE FIRST: `CLOSES` (no floor gap in the 93-row detector) or `GAP: <exact source edit to dev_lca.c that scores 93/93
and changes a guest-visible outcome>`, then the token.

A routine mutation-testing review of an open-source hardware emulator (GXemul, a hardened fork).  Check premises, not only
reasoning; say what you could not check.  Tree: `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\` ONLY.  Packet-fed seats: all
facts are below; do not plan to read files.

## WHY THIS PASS EXISTS
Closing pass 2 (on the 77-row class closure) was NOT clean, and its measuring seat BUILT the two escapes it reported:
the split TAIL cells (len 3/5/6/7 at lane 0) were unrowed because the header said tails start only at the unmapped port
0x400 -- they start at every port 0 mod 0x20, and the 8042 sits at 0x60 -- and x_wfallthru (the write arm's `return'
deleted, a phantom read of the stored port) loses IIR_TXRDY on a store to 0x3fa and was never in the header's contract.
Two reading-seat mutants (an exact-port conjunct, a data-keyed index) were measured 77/77 and are now DISCLOSED BY
CLASS; grok's `h5 stq' premise was measured false (76/77).  Repair 3 rows the tail cells at 0x60 (sessions 4f `tailr' /
`tailw', each write phase resetting the 8042 command byte first so a DECLINED tail store is visible) and the phantom
read (4h `iir'), and rewrites THE CELL SPACE, the CONTRACT and the DISCLOSED list.  The closing pass VERIFIES THE
ENUMERATION: the chain closes on the first valid pass with zero floor breaches.

## SETTLED (re-stated because the questions depend on it)
* Disposition B (adjudicated 8 of 9, flagship last): the byte for ISA port P sits at buffer position `(P & 3) % len` on
  BOTH arms; `len == 0` refused first; no latch, no announce.  Every seat that walked the handler found the fix right in
  every (len 1..8, ofs 0..3, direction) cell: no exit, no out-of-range index, no divide by zero.
* On Alpha a handler `return 0` leaves a load's register unchanged and makes a store invisible except through the device.
* memory_rw pre-zeroes a device read buffer (#95), so the read arm's zero-fill of the other positions is EQUIVALENT.
* The 1 KB split (MRW_SPLIT_MASK 0x3ff) fires for any non-PHYSICAL access on a CPU with translate_v2p -- Alpha always --
  so every split has a HEAD of 1..7 bytes at a port 0x1f mod 0x20 (lane 3) and a TAIL of 8-h (LDQ/STQ) or 4-h
  (LDL/STL) bytes at the next port, 0 mod 0x20 (lane 0) -- measured; a declined tail fails a whole load, while a store
  forwards its head before its tail fails (tables 2 and 3).
* Kill-table targeting rule: repair 3 ADDS sessions and changes no existing session's commands, so no earlier kill moves;
  tables 1-3 stand, table 4 measures the new rows.

## THE FIX (`git diff`, verbatim -- the code is unchanged since pass 2; only its comment was corrected)

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

## THE PROBE HEADER'S CONTRACT (clause e), verbatim

```
*** #530: IT IS NOW THE WITNESS AND THE DETECTOR.  Sessions 1-3 are the witness below, unchanged but
#  for the sentinel; the #530 sessions at the end are the detector for the fix. ***
#
#  THE FIX (disposition B, regress/artifacts/lcaisalane/FABLE_F2_RULING_20260914.md): the byte for port
#  P sits at buffer position (P & 3) % len on BOTH arms; `len == 0' is refused first; no latch, no
#  announce (there is no event -- member 4, ACCEPT).  Table 1 (37 rows): HEAD 19/37, fix 37/37
#  (regress/artifacts/lcaisalane/fix530_20260914/HEAD_det.out, FIX_det.out); after the pass-2 repair
#  (51 rows) see that dir's table 2; after closing pass 1's class closure (77 rows) its table 3; after
#  closing pass 2's tail cells and phantom-read rows (93 rows) its table 4.
#
#  THE CELL SPACE, rowed WHOLE since closing pass 1 (pass 2 and closing pass 1 found the same class --
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
#  read of the stored port (x_wfallthru -- the `iir' rows, since closing pass 2: every port stored to
#  before then read back without a side effect, so it scored 77/77 and was called disclosed by table 3's
#  PRETABLE/POSTTABLE only, never here).  *** TABLE 1'S CONTRACT CLAIMED MOST OF THIS AT 37 ROWS AND WAS MEASURED FALSE: the Opus
#  pass-2 seat built ten mutants that scored 37/37, nine changing a guest outcome -- no row stored at len
#  4/8 -- and measured that the split heads it DISCLOSED as needing a translated access split on K0SEG. ***
#  DISCLOSED, not caught: the len-0 refusal (no producer); the zero-fill of the positions other than
#  `ofs' (p_nozero -- EQUIVALENT: memory_rw's #95 pre-zero already clears the buffer); an address-decode
#  edit above port 0x3ff (p_port10 -- not an edit of the fix; measured 51/51 by the Opus closing seat.
#  This said "every probed port is below 0x400", and the split TAILS reach port 0x400 -- grok and the
#  Opus seat, closing pass 1 -- so the premise was wrong and the scoping reason is the one that stands);
#  the size field a<4:3> (lcaisasize); the hardware QUADWORD ENCODING's route (lcaisaqword: on the
#  21066 a<6:5> = 11 with a<4:3> = 11 is a quadword at port P, which the model forwards to P|3 -- NOT the
#  len-8 lane this probe rows, which follows the same (P & 3) % len rule as every other width); the
#  missing PHYSICAL (lcaisaphys); the end-of-window clamp at port 0xffff (nothing is mapped there).
#  Disclosed BY CLASS (closing pass 2; each measured 77/77 by the Opus seat, regress/artifacts/lcaisalane/
#  opus_c2_20260914/): a decline or mis-decode keyed on an EXACT PORT VALUE (kimi-k3's `relative_addr ==
#  0x400 && len == 4' -- the p_port10 class: the body never tests the port against a constant); a
#  mis-decode keyed on the DATA (codex's `ofs == 2 && !data[2]', generally `data[ofs] ? data[ofs] :
#  data[0]' -- every store row carries a NONZERO correct byte, so "the correct byte is 0" is unrowed at
#  every store cell).  EQUIVALENT on alphabook1, named: the inner forward's return value honoured on the
#  read arm, or forced to success on the write arm -- no ISA device there fails an access, and an
#  unmapped forward returns success with a zero fill.
#  EQUIVALENT by construction, named so no table is spent on them (kimi-k3, pass 2): restoring the dead
#  `% len' on the write arm's index (`ofs' is already reduced), and reinstating `if (ofs > len) exit(1)'
#  AFTER the fold (unsatisfiable once ofs < len) -- the reinstated exit that matters is on the UNFOLDED
#  lane, which the table's m_exit builds.
#
#  *** ```

## THE REPAIR DIFF -- the 77-row instrument -> the 93-row instrument (`git diff --no-index`, verbatim; 6 hunks)

```diff
diff --git "a/C:\\DocumentNoSnc\\CC\\GXEMUL\\GXEMUL-SEC\\regress\\artifacts\\lcaisalane\\fix530_20260914\\table3\\lca_isalane_probe.table3.py" "b/C:\\DocumentNoSnc\\CC\\GXEMUL\\GXEMUL-SEC\\regress\\lca_isalane_probe.py"
index 7c75255..d68a417 100644
--- "a/C:\\DocumentNoSnc\\CC\\GXEMUL\\GXEMUL-SEC\\regress\\artifacts\\lcaisalane\\fix530_20260914\\table3\\lca_isalane_probe.table3.py"
+++ "b/C:\\DocumentNoSnc\\CC\\GXEMUL\\GXEMUL-SEC\\regress\\lca_isalane_probe.py"
@@ -68,3 +68,4 @@
 #  (regress/artifacts/lcaisalane/fix530_20260914/HEAD_det.out, FIX_det.out); after the pass-2 repair
-#  (51 rows) see that dir's table 2; after closing pass 1's class closure (77 rows) its table 3.
+#  (51 rows) see that dir's table 2; after closing pass 1's class closure (77 rows) its table 3; after
+#  closing pass 2's tail cells and phantom-read rows (93 rows) its table 4.
 #
@@ -74,5 +75,11 @@
 #  every cell rowed (the read side of len 4 at lanes 2/3 FULL-register, not only a single-lane mask);
-#  split HEADS len 1-7 at lane 3 (a head always ends at port 0x3ff) x R/W; split TAILS start at port
-#  0x400 (lane 0), where nothing is mapped, so a tail cell shows only as a whole-access failure -- seen
-#  by the split rows (table 2's p_lane0decl), not rowed per length.
+#  split HEADS len 1-7 at lane 3 x R/W (a head ends at a port 0x1f mod 0x20; this probe's is 0x3ff);
+#  split TAILS len 1-7 at lane 0 x R/W (a tail starts at the next port, 0 mod 0x20) -- tails of len 1,
+#  2 and 4 are the direct lane-0 cells, and tails of len 3, 5, 6 and 7 are rowed at the 8042 DATA port
+#  0x60 (sessions 4f `tailr' / `tailw', since closing pass 2).  *** THIS SAID "split TAILS start at port
+#  0x400, where nothing is mapped, so a tail cell shows only as a whole-access failure ... not rowed per
+#  length" UNTIL CLOSING PASS 2, AND IT WAS MEASURED FALSE: tails start at EVERY port 0 mod 0x20 (the
+#  8259 at 0x20/0xa0, the 8253 at 0x40, the 8042 at 0x60), and the Opus seat's tail mis-placement
+#  mutant scored 77/77 because the split rows' tails at the unmapped 0x400 can show a decline but never
+#  a position. ***
 #
@@ -88,3 +95,6 @@
 #  byte replicated into every position, at len 2, 4 or 8; the read arm's success return turned into a
-#  failure.  *** TABLE 1'S CONTRACT CLAIMED MOST OF THIS AT 37 ROWS AND WAS MEASURED FALSE: the Opus
+#  failure; the write arm's `return' removed, so a store falls into the read arm and makes a phantom
+#  read of the stored port (x_wfallthru -- the `iir' rows, since closing pass 2: every port stored to
+#  before then read back without a side effect, so it scored 77/77 and was called disclosed by table 3's
+#  PRETABLE/POSTTABLE only, never here).  *** TABLE 1'S CONTRACT CLAIMED MOST OF THIS AT 37 ROWS AND WAS MEASURED FALSE: the Opus
 #  pass-2 seat built ten mutants that scored 37/37, nine changing a guest outcome -- no row stored at len
@@ -100,2 +110,10 @@
 #  missing PHYSICAL (lcaisaphys); the end-of-window clamp at port 0xffff (nothing is mapped there).
+#  Disclosed BY CLASS (closing pass 2; each measured 77/77 by the Opus seat, regress/artifacts/lcaisalane/
+#  opus_c2_20260914/): a decline or mis-decode keyed on an EXACT PORT VALUE (kimi-k3's `relative_addr ==
+#  0x400 && len == 4' -- the p_port10 class: the body never tests the port against a constant); a
+#  mis-decode keyed on the DATA (codex's `ofs == 2 && !data[2]', generally `data[ofs] ? data[ofs] :
+#  data[0]' -- every store row carries a NONZERO correct byte, so "the correct byte is 0" is unrowed at
+#  every store cell).  EQUIVALENT on alphabook1, named: the inner forward's return value honoured on the
+#  read arm, or forced to success on the write arm -- no ISA device there fails an access, and an
+#  unmapped forward returns success with a zero fill.
 #  EQUIVALENT by construction, named so no table is spent on them (kimi-k3, pass 2): restoring the dead
@@ -650,3 +668,4 @@ print("")
 #  ---- SESSIONS 4e (#530 closing pass 1): the SPLIT heads at every length 1..7, both arms --------------------------
-#  A split head always ends at port 0x3ff (lane 3), so its cells are (len, 3) for len 1..7.  4c rowed len 3 (R, W) and
+#  A split head always ends at a port 0x1f mod 0x20 (lane 3 -- the lane is the invariant; this probe's boundary is port
+#  0x3ff), so its cells are (len, 3) for len 1..7.  4c rowed len 3 (R, W) and
 #  5 (R); deepseek found `len == 6' free.  Heads of len 6 and 7 (R) and 5-7 (W) never ended the host and share one
@@ -692,2 +711,69 @@ print("")
 
+#  ---- SESSIONS 4f (#530 closing pass 2): the split TAIL cells, at a MAPPED port ------------------------------------
+#  A 1 KB split (MRW_SPLIT_MASK 0x3ff on the VIRTUAL address = 32 sparse ports) puts its head at a port 0x1f mod 0x20
+#  (lane 3) and its TAIL at the next port, 0 mod 0x20 (lane 0), of length 8 - h (LDQ/STQ) or 4 - h (LDL/STL).  Tails of
+#  length 1, 2 and 4 are handler-identical to the direct lane-0 cells; tails of length 3, 5, 6 and 7 exist ONLY as tails.
+#  The split rows above put their tails on port 0x400, where nothing is mapped: a tail read there is zero-filled and a
+#  tail write goes nowhere, so they see a tail DECLINE and never a tail MIS-PLACEMENT (principle 2 -- zero readback alone
+#  proves nothing -- applied to the probe's own tails).  The Opus closing-pass-2 seat MEASURED
+#  `if ((relative_addr & 3) == 0 && len > 2 && (len & 3)) ofs = 1;' at 77/77 (regress/artifacts/lcaisalane/
+#  opus_c2_20260914/).  These two sessions are its discriminator, ported: an unaligned LDQ/STQ at SP(0x5f) + 0x1f / 0x1e
+#  / 0x1d / 0x1b is a head of 1 / 2 / 3 / 5 at port 0x5f (unmapped) and a tail of 7 / 6 / 5 / 3 at port 0x60, the 8042
+#  DATA port.  Read channel: the self-test reply 0x55 lands at register byte h.  Write channel: the 8042 command byte
+#  (0x60 to the command port, then the tail's forwarded byte; read back with 0x20 through the FLAT mapping).  The 1- and
+#  2-byte heads at 0x5f are (1,3) and (2,3) cells, so on HEAD each session ends the host at its first split.
+TAILHEADS = ((1, 0x1f), (2, 0x1e), (3, 0x1d), (5, 0x1b))   # (head length h, byte offset) -> tail 8 - h at port 0x60
+C4f = [k0(FLAT(KBC_CMD)), KBC_SELFTEST, k0(SP(KBC_DAT))] + [k0(SP(0x5f) + o) for _, o in TAILHEADS]
+def kbc_selftest(): return [LDQ(T1, 0, T0), LDQ(T2, 8, T0), STB(T2, 0, T1)]
+P4f = [(kbc_selftest() + [LDQ(T1, 16, T0)] + sent(T3) + [LDQ(T3, 0, T1)], "t3")]                  # control: (8,0)
+for i in range(len(TAILHEADS)):
+    P4f.append((kbc_selftest() + [LDQ(T1, 24 + 8 * i, T0)] + sent(T4) + [LDQ(T4, 0, T1)], "t4"))
+a4f, g4f = dsession("tailr", C4f, P4f, ["ctl"] + ["t%d" % (8 - h) for h, _ in TAILHEADS])
+row("tailr alive", "alive" if a4f else "dead", "alive", "CONTROL (1/2-byte heads at 0x5f were host deaths on HEAD)")
+row("tailr ctl", hx(g4f["ctl"]), hx(KBC_REPLY), "CONTROL: aligned LDQ at SP(0x60), the (8,0) cell, reads 0x55")
+for h, _ in TAILHEADS:
+    row("tailr t%d" % (8 - h), hx(g4f["t%d" % (8 - h)]), hx(KBC_REPLY << (8 * h)),
+        "(%d,0) LDQ TAIL at port 0x60: position 0 -> register byte %d" % (8 - h, h))
+print("")
+
+def tailv(h): return (0x44 << (8 * h)) | (0x21 << (8 * (h + 1)))   # tail position 0 = 0x44, position 1 = 0x21
+C4g = ([k0(FLAT(KBC_CMD)), 0x60, 0x20, k0(FLAT(KBC_DAT))] + [k0(SP(0x5f) + o) for _, o in TAILHEADS]
+       + [tailv(h) for h, _ in TAILHEADS])
+def kbc_ldcmd(): return [LDQ(T1, 0, T0), LDQ(T2, 8, T0), STB(T2, 0, T1)]
+def kbc_rdcmd(): return [LDQ(T1, 0, T0), LDQ(T2, 16, T0), STB(T2, 0, T1), LDQ(T1, 24, T0)]
+def kbc_reset(): return kbc_ldcmd() + load_const(T3, 0x04) + [LDQ(T1, 24, T0), STB(T3, 0, T1)]   # cmdbyte = 0x04 (flat)
+P4g = [(kbc_reset() + kbc_rdcmd() + sent(T4) + [LDBU(T4, 0, T1)], "t4")]                          # control: flat
+#  Each tail phase RESETS the command byte to 0x04 first: without it a DECLINED tail store would read back the previous
+#  phase's 0x44 and pass (the order is t7, t6, t5, t3), so these rows would see a mis-placement and never a decline.
+for i in range(len(TAILHEADS)):
+    P4g.append((kbc_reset() + kbc_ldcmd() + [LDQ(T3, 64 + 8 * i, T0), LDQ(T1, 32 + 8 * i, T0), STQ(T3, 0, T1)]
+                + kbc_rdcmd() + sent(T5) + [LDBU(T5, 0, T1)], "t5"))
+a4g, g4g = dsession("tailw", C4g, P4g, ["ctl"] + ["t%d" % (8 - h) for h, _ in TAILHEADS])
+row("tailw alive", "alive" if a4g else "dead", "alive", "CONTROL (1/2-byte heads at 0x5f were host deaths on HEAD)")
+row("tailw ctl", hx(g4g["ctl"]), hx(0x04), "CONTROL: flat command-byte round trip")
+for h, _ in TAILHEADS:
+    row("tailw t%d" % (8 - h), hx(g4g["t%d" % (8 - h)]), hx(0x44),
+        "(%d,0) STQ TAIL at port 0x60 forwards position 0 (0x44), not 1 (0x21)" % (8 - h))
+print("")
+
+#  ---- SESSION 4h (#530 closing pass 2): a store to a port whose READ has a side effect ---------------------------
+#  Every port the rows above store to reads back without a side effect, so deleting the write arm's `return' -- the
+#  store then FALLS INTO the read arm, a phantom 1-byte read of the same port -- scored 77/77 (x_wfallthru, table 3 and
+#  the Opus closing-pass-2 seat).  It is not equivalent for a guest: dev_ns16550.c's com_iir READ arm clears IIR_TXRDY
+#  (and com_data's calls console_readchar, so every THR store would eat a pending input character).  Channel: arm
+#  TXRDY (IER 0 -> ETXRDY), store 0 through lca_isa to ISA 0x3fa (FCR on a write, IIR on a read), flat IIR & 3.
+UART_IIR = 0x3fa                    # 2 mod 4 -> lane 2
+def iir_arm(): return load_const(T3, 0x02) + [LDQ(T1, 0, T0), STB(ZERO, 0, T1), STB(T3, 0, T1)]
+C4h = [k0(FLAT(UART_IER)), k0(FLAT(UART_IIR)), k0(SP(UART_IIR))]
+P4h = [(iir_arm() + [LDQ(T1, 8, T0)] + sent(T2) + [LDBU(T2, 0, T1)], "t2"),                     # control, no lca store
+       (iir_arm() + [LDQ(T1, 16, T0), STB(ZERO, 0, T1), LDQ(T1, 8, T0)] + sent(T4) + [LDBU(T4, 0, T1)], "t4"),  # (1,2)
+       (iir_arm() + [LDQ(T1, 16, T0), STL(ZERO, 0, T1), LDQ(T1, 8, T0)] + sent(T5) + [LDBU(T5, 0, T1)], "t5")]  # (4,2)
+a4h, g4h = dsession("iir", C4h, P4h, ["ctl", "stb", "stl"])
+iir3 = lambda v: None if v is None else v & 0x03
+row("iir alive", "alive" if a4h else "dead", "alive", "CONTROL")
+row("iir ctl", hx(iir3(g4h["ctl"])), hx(0x02), "CONTROL: IER 0 -> ETXRDY sets IIR_TXRDY; flat IIR & 3 = TXRDY")
+row("iir stb", hx(iir3(g4h["stb"])), hx(0x02), "(1,2) STB 0 -> SP(0x3fa): TXRDY survives the store (x_wfallthru)")
+row("iir stl", hx(iir3(g4h["stl"])), hx(0x02), "(4,2) STL 0 -> SP(0x3fa): TXRDY survives the store (x_wfallthru)")
+print("")
+
 #  ---- SESSIONS 5-10: the six cells that ENDED THE HOST on HEAD, one process each -------------
```

## THE MEASURING SEAT'S CLOSING-PASS-2 ANSWER (what repair 3 answers)

# VERDICT: GAP -- (1) `ofs = (relative_addr & 3) % len;` followed by the inserted line `if ((relative_addr & 3) == 0 && len > 2 && (len & 3)) ofs = 1;` scores 77/77 and moves the byte at the four split-TAIL cells (3,0) (5,0) (6,0) (7,0), both arms, at a MAPPED port. (2) x_wfallthru (delete the write arm's `return`) scores 77/77 and loses the ns16550's IIR_TXRDY on a store to port 0x3fa. BOTH MEASURED, each with a guest-visible discriminator run on base and mutant.

Liveness `LCA530_C2_OPUS_20260914`.  `_scratchpad/CHECKPOINT.md` line 1, verbatim, read at 05:1x:

    # CHECKPOINT -- 2026-09-14 ~05:0x   HEAD 9c91999 (records)   #529 TABLE 8 PROBES RUNNING; #530 CLOSING PASS 2 FIRED

(At the start of this seat, ~04:5x, line 1 read `# CHECKPOINT -- 2026-09-13 ~23:2x   HEAD 9c91999 (records)   crimewidthkill #529: TABLE 7 PROBES RUNNING; rung-3 seat out`. The file was overwritten while this seat ran.)

Seat: Opus 5, the Agent tool, MEASURING.  Tree: `GXEMUL-SEC/` only.  I wrote nothing into GXEMUL-SEC except this directory.

---

## HOW IT WAS MEASURED

* Clone `/tmp/gxopus530c2` = `cp -a build/`, plus GXEMUL-SEC's working-tree `src/devices/dev_lca.c` (md5 `dc49ebdd...`,
  the same before and after this seat).  `BASELINE_CMP CLEAN`.  `rm src/cpus/*.o` before the first build; every build
  checked with `[ gxemul -nt dev_lca.c ] && [ dev_lca.o -nt dev_lca.c ]`.  I dropped a clone-local `.MUTANT` sentinel,
  and both drivers restored the clone (`cmp` clean against SEC, the binary newer than the source, `restored == base
  (byte-identical)`).  No mutant binary was identical to base.
* Instrument: `regress/lca_isalane_probe.py` frozen as a scratch copy, **md5 `299645d6...`, identical to the shipped
  probe and to table 3's `lca_isalane_probe.table3.py`** (`logs/INSTRUMENT.md5`).
* Discriminators (NOT detectors): `instrument/opus_c2_demo.py` (16 rows) and `instrument/opus_c2_demo2.py` (6 rows).
  Both are the probe's own helpers, lines 157-337 and 467-494 copied verbatim, plus new sessions.  They run on
  unmodified `alphabook1`, and every access in them is a guest instruction.
* Drivers `instrument/opus530c2.run-050257.sh` and `opus530c2b.run-050845.sh` (frozen copies).  Two probe lanes each.
  **Every log below ends with its completion sentinel** (`LCAISALANE_DONE` / `OPUSC2_DONE`).  `RETRIED=none` on every
  leg.
* Durable logs: `logs/` (my sweep) and `logs_panel/` (the panel mutants relayed mid-run).

---

## Q1 -- DOES "THE CELL SPACE" ENUMERATE THE SPACE CORRECTLY?

**The axes are right.**  The handler reads `relative_addr` only through `(relative_addr >> 5)`:

* as the forwarded port P, which is the same on both arms, and
* through `P & 3` in `ofs`.

It reads `len` only through `len == 0`, `% len` and the fill-loop bound.  So (len, lane = P & 3, direction) is the
handler's own partition.

**The reachable len values are enumerated right: direct 1, 2, 4, 8 at any lane, plus split pieces.  The split pieces
are where the enumeration goes wrong.**  MRW_SPLIT_MASK is 0x3ff on the VIRTUAL address, which is 32 ports per 1 KB.
Every split therefore produces:

* a HEAD of length h = 1..7 at a port that is 0x1f mod 0x20 (lane 3), and
* a TAIL of length 8-h (LDQ/STQ) or 4-h (LDL/STL) at a port that is 0 mod 0x20 (lane 0).

**The header states both facts as if the probe's one boundary were every boundary:**

* "a head always ends at port 0x3ff" -- it ends at 0x1f, 0x3f, ... 0x3ff, ...  The lane (3) is the invariant, the
  port is not.  This does no harm by itself: a head cell is still (h, 3).
* **"split TAILS start at port 0x400 (lane 0), where nothing is mapped, so a tail cell shows only as a whole-access
  failure"**.  This one is false, and it is load-bearing.  Tails start at 0x20, 0x40, 0x60, 0xa0 ..., and bus_isa
  puts the 8259 at +0x20 and +0xa0, the 8253 at +0x40, and the 8042 at +0x60.

**OMITTED CELLS (should be rowed): (3,0), (5,0), (6,0), (7,0), for both R and W -- eight cells.**

* The tails of length 1, 2 and 4 are handler-identical to the direct lane-0 cells.  Those are rowed at 0x3fc, 0x60
  and 0x300.
* Tails of length 3, 5, 6 and 7 exist only as tails.
* At the probe's only tail port, 0x400, the position channel **cannot vary**:
  * a tail READ forwards to non-existent memory, and memory_rw zero-fills it (`memory_rw.c`, the physical_max arm:
    `memset(data, 0, len)`), so the tail contributes a zero at whichever position;
  * a tail WRITE goes nowhere.
* So the rows the header leans on (`h1/h2/h3 ldq`, `h3 ldl`, `h1/h2/h3 stq`, whose tails are (7,0) (6,0) (5,0) (1,0))
  see a tail **decline** (whole-access failure, e.g. table 3's x_len6 via `h2 ldq`) and never a tail **mis-placement**.
* This is the probe's own principle 2, *"zero readback alone proves nothing"*, applied to its own tails.

**MEASURED at port 0x60 (8042 data).**  An unaligned LDQ/STQ at `SP(0x5f) + 0x1f/0x1e/0x1d/0x1b` gives head 1/2/3/5
at port 0x5f (unmapped) and tail 7/6/5/3 at port 0x60.  `logs/demo_base.raw` is 16/16:

| row | cell | base | t_tails |
|---|---|---|---|
| tailr t7 | (7,0) R | 0x5500 | 0x550000 |
| tailr t6 | (6,0) R | 0x550000 | 0x55000000 |
| tailr t5 | (5,0) R | 0x55000000 | 0x5500000000 |
| tailr t3 | (3,0) R | 0x550000000000 | 0x55000000000000 |
| tailw t7/t6/t5/t3 | (7,0)..(3,0) W: 8042 command byte, flat readback | 0x44 | 0x21 |

**CELLS LISTED AS ROWED THAT NO ROW EXERCISES: NONE.  Verified in one run rather than argued:** `x_rot` =
`ofs = ((relative_addr & 3) + 1) % len;` rotates the position at every cell with len >= 2 and leaves every len-1 cell
alone.

* **Measured 38/77** (`logs/probe_x_rot.raw`).  Its 39 red rows match my written prediction **exactly**, with zero
  extra and zero missing.
* The prediction was every row of every len >= 2 cell: all 24 direct cells (len 2/4/8 x lane x R/W) and the 10
  head-only cells (len 2, 3, 5, 6, 7 at lane 3 x R/W; head len 4 is the direct (4,3) cell), across 39 rows.  No len-1 row reddened.
* So every len >= 2 cell the header lists as rowed has a row whose channel varies with the position there.
* The len-1 cells have only one position.  Their mis-decode (byte dropped) is HEAD's own shape, measured red on
  `r11/r12/r13/w12/w13` by table 1 and HEAD_r3.
* By construction, every store row's value carries a nonzero correct byte and different bytes at the other positions,
  and every read row compares the FULL register against a nonzero device byte.  So alternatives other than the
  rotation are also visible.  (That last point is argued, not measured.)

---

## Q2 -- FLOOR GAPS IN THE 77-ROW DETECTOR

### GAP 1 -- the split-tail cells (the SAME CLASS the class closure closed)

* **Edit:** insert after `ofs = (relative_addr & 3) % len;`
  `if ((relative_addr & 3) == 0 && len > 2 && (len & 3)) ofs = 1;`
* **Score:** 77/77 (`logs/probe_t_tails.raw`).  Discriminator: 8/16 (`logs/demo_t_tails.raw`), the eight tail rows
  above.
* **Rows expected to catch it, and why they cannot:** `h1 ldq`, `h2 ldq`, `h3 ldq`, `h3 ldl`, `h1 stq`, `h2 stq`,
  `h3 stq` all put a (7,0), (6,0), (5,0) or (1,0) tail through the handler.  But the tail lands on port 0x400.  There
  the forwarded byte is a zero-fill (read) or a write into nothing, so moving it changes nothing observable.
* **Guest-visible difference:** a guest LDQ that straddles a 1 KB sparse line onto the 8042 data port sees the device
  byte one register byte too high.  A STQ there hands the 8042 the next byte of the value instead of the right one.
  The command byte reads back 0x21 instead of 0x44.
* **Why it is in scope rather than disclosable:**
  * The header ENUMERATES these cells and declines to row them on a stated premise that is measured false.
  * The edit is a (len, lane) conjunct of the position rule.  That is exactly the shape of `c1_w1w`
    (`ofs == 1 && len > 2`), which the previous pass accepted as a gap and rowed.
  * `% len` distinguishes every len in the body, and the header's own axis is len 1..7.
  * My grading: the class the round claims closed, one sub-space over.  **L2 if the contract's "at every cell of that
    space" stands; at minimum an L4 wrong record** in THE CELL SPACE paragraph.
* **Cheapest closure:** two sessions (`tailr`, `tailw` in `instrument/opus_c2_demo.py`).  That is 8 value rows plus
  controls against the 8042 at 0x60, with no new port and no timer.
* Note for a detector: the (1,3) and (2,3) heads at 0x5f end the host on HEAD.  That is the expected HEAD-red, the same
  as `h1/h2` today.

### GAP 2 -- x_wfallthru (kimi-k3's shape; I re-measured it and dispute the "DISCLOSED")

* **Edit:** in the write arm, `return cpu->memory_rw(...)` becomes `cpu->memory_rw(...)`.  The store then falls into
  the read arm: a phantom 1-byte READ of the same port, a fill of the (store) buffer, then `return 1`.
* **Score:** 77/77 (`logs/probe_x_wfallthru.raw`; table 3 measured the same).  Discriminator: 14/16
  (`logs/demo_x_wfallthru.raw`):

| row | base | x_wfallthru |
|---|---|---|
| iir stb: (1,2) STB 0 to SP(0x3fa), then flat IIR & 3 | 0x2 (TXRDY) | 0x1 (NOPEND) |
| iir stl: (4,2) STL 0 to SP(0x3fa), same readback | 0x2 | 0x1 |

* **Why no row catches it:** every port the probe stores to (SCR, MCR, IER, MSR, the 8042 command port, the unmapped
  0x5f and 0x400) reads back without a side effect.
* **What it breaks in a guest:**
  * dev_ns16550.c's `com_iir` READ arm clears IIR_TXRDY, so an FCR store loses a pending transmit-ready interrupt.
  * The `com_data` READ arm calls `console_readchar`, so **every THR store (every console output byte) consumes one
    pending input character**.
  * The 8042 data READ pops the output buffer.
* **The "DISCLOSED" is wrong twice:**
  * The contract text (the probe header's clause (e) list) does not mention it.  `grep -i "fallthru\|phantom"` over
    `regress/lca_isalane_probe.py` returns nothing.  The disclosure lives only in table 3's PRETABLE and POSTTABLE,
    and PRETABLE itself names the ports that would see it ("RBR, IIR").
  * Its warrant, "no port it stores to has a read side effect", is a fact about the probe's port choice.  It is not a
    reason the edit is outside the contract.
* **Floor classification (for adjudication):** `if (writeflag == MEM_WRITE)` dominates the fix's edited line
  `byte = data[ofs]`.  Deleting the guarded body's `return` keeps the guard and nulls its routing, which is clause (d)'s
  "keep the guard, remove its effect".  I read it as floor-shaped.  At minimum the header must disclose it by name.
* **Cost to row it:** one session, 3 rows (`iir` in the demo).

### THE DENOMINATOR -- every shape built and swept (12 mutants: 6 of mine + the 6 relayed panel mutants; base measured twice)

| mutant | edit to the FIXED handler | 77-row | red rows | discriminator | disposition |
|---|---|---|---|---|---|
| base | -- | **77/77** (x2: `logs/`, `logs_panel/`) | -- | 16/16, 6/6 | |
| **t_tails** | insert `if ((relative_addr & 3) == 0 && len > 2 && (len & 3)) ofs = 1;` | **77/77** | none | **8/16** | **GAP 1** |
| **x_wfallthru** | delete the write arm's `return` | **77/77** | none | **14/16** | **GAP 2** |
| x_rot | `ofs = ((relative_addr & 3) + 1) % len;` | 38/77 | exactly the 39 predicted (every len >= 2 cell) | 7/16 | the channel check for the whole cross |
| swapmod | `ofs = (relative_addr % len) & 3;` | 75/77 | h7 ldq (0x5a00), h7 stq (0x96) | 12/16 (tailr/tailw t7, t5) | killed -- but see the caution below |
| r_fwdret | read arm: `if (!cpu->memory_rw(...)) return 0;` | 77/77 | none | 16/16 | EQUIVALENT on alphabook1 (below) |
| w_ret1 | write arm: `return 1 \| cpu->memory_rw(...)` | 77/77 | none | 16/16 | EQUIVALENT on alphabook1 (below) |
| G1..K2b | see PANEL MUTANTS | | | | |

**CAUTION on swapmod.  It is killed by two rows, and only because of a coincidence in the port.**  0x3ff = 1023, and
1023 is 0 mod 3, 3 mod 5 and 3 mod 6.  So at the probe's single head boundary, `(P % len) & 3` equals `(P & 3) % len`
for heads 3, 5 and 6.  Only h7 (1023 mod 7 = 1) sees it.  At any other boundary (port 0x1f: 31 mod 3/5/6 = 1) the h3,
h5 and h6 rows would also see it.  This is clause (f)'s layout caution in another coat: the head rows' kills of a
modulus edit depend on WHICH boundary was chosen.  The GAP-1 tail rows at 0x60 add kills for it too (0x60 mod 5 = 1,
0x60 mod 7 = 1, measured red).

**r_fwdret / w_ret1 are equivalent.  The reasoning, checked against the code:**

* No ISA device on alphabook1 fails an access.  I scanned `DEVICE_ACCESS` in dev_8259/8253/pccmos/lpt/wdc/fdc/pckbc/
  ns16550 for `return 0;`, and the only hit is ns16550's out-of-range arm, which the flat mapping cannot reach.
* An unmapped forward returns OK with a zero fill (`memory_warn_about_unimplemented_addr` returns false).  The
  exception is `halt_on_nonexistant_memaccess`, and there `cpu->running = 0` makes the OUTER memory_rw fail whatever
  the handler returns.
* So the forward's return value never differs.  Guest visibility would need a failing forward (a STx_C success flag, or
  a split store whose head fails before its tail), and nothing produces one.  Recommend: disclose as EQUIVALENT by
  name.

**Thought about, not built:**

* `i < len` -> `i <= len` in the fill loop: a 1-byte host write past the caller's `data[]` on direct reads.  ASAN-
  visible and host-only.  For split heads the tail overwrites it, so it is not guest-visible.
* `byte = data[ofs] ? data[ofs] : data[0]`: the generalisation of C1 below, a value-keyed forward.  It escapes by the
  same argument as C1.
* Mutants keyed on port bits other than `& 3` (address-decode, the p_port10 class).  Disclosed, and consistent with the
  joint-cell rule: the body never tests those bits.

---

## PANEL MUTANTS (relayed by the main loop mid-run; built in the same clone, `logs_panel/`)

| id | edit | 77-row | red rows (got vs want) | discriminator (base -> mutant) | note |
|---|---|---|---|---|---|
| G1 (grok) | write `byte = data[(len == 5 && ofs == 3) ? 0 : ofs];` | **76/77** | `h5 stq` 0x7e vs 0xc3 | -- | **grok's premise is false; the main loop's reading is right.**  C4e slot 4 is `k0(SP(UART_SCR) + 0x1b)`, a real 5-byte head |
| G2 (grok) | `if (len == 0 \|\| (len == 5 && writeflag == MEM_WRITE)) return 0;` | **76/77** | `h5 stq` 0x5a (SCR's prior value kept) vs 0xc3 | -- | `h3 stq` stays green: its head lands before its 5-byte tail is declined |
| K1 (kimi-k3) | after `relative_addr >>= 5;`: `if (relative_addr == 0x400 && len == 4) return 0;` | **77/77** | none | `demo2`: LDQ SP(SCR)+0x1c 0x5a000000 -> sentinel 0x0bad1d8a (whole load abandoned); LDL SP(0x400) 0x0 -> sentinel | guest-visible (a load's register kept); see below |
| C1 (codex) | write `byte = data[ofs == 2 && !data[2] ? 0 : ofs];` | **77/77** | none | `demo2`: STQ 0x04 via SP(MSR), flat MSR 0xb0 -> **0xb4**; STL 0x04 the same, 0xb0 -> 0xb4 | codex's discriminator is confirmed exactly |
| K2a (kimi CLI) | write `byte = data[(ofs == 3 && len == 4) ? 0 : ofs];` | **76/77** | `st4 lane3` 0x0 vs 0x7e | -- | confirmed |
| K2b (kimi CLI) | write `byte = data[(ofs == 3 && len == 8) ? 0 : ofs];` | **75/77** | `st8 lane3` 0x0 vs 0x6d; `ld8 lane3` 0x0 vs 0x6d000000 | -- | confirmed.  The read row reddens too, because it reads back the SCR value the bad store left |

**K1: disclose, but not under the tail paragraph's warrant.**

* The cell (4,0) is rowed (`st4 lane0`, `ld4 lane0` at 0x3fc).  K1 adds an exact-ADDRESS conjunct inside it.  The body
  never tests `relative_addr` against a constant, so under the joint-cell rule this is a clause-(e) value/address
  disclosure, the p_port10 class.  I agree with disclosing it.
* But the header's "a tail cell shows only as a whole-access failure -- seen by the split rows" is **not** why it is
  safe.  No row produces a len-4 tail.  The tail lengths the probe produces are 7 (h1), 6 (h2), 5 (h3 ldq/stq), 3 (h5),
  2 (h6), and 1 (h7 and h3 ldl).  It is also not a floor cell: a (4,0) decline keyed on len and lane, not address, is
  caught by the direct rows.

**C1: disclose by class, as intended.**  It is a value conjunct the body never tests.  Every store row carries a
NONZERO correct byte, so "the correct byte is 0" is an unrowed value class at every store cell.  Name the class in the
disclosure (with `data[ofs] ? data[ofs] : data[0]` as its general form), not only C1.

---

## Q3 -- WRONG STATEMENTS

1. **Probe header, THE CELL SPACE (and the brief's SETTLED bullet 4):**
   * "split TAILS start at port 0x400 (lane 0), where nothing is mapped, so a tail cell shows only as a whole-access
     failure".
   * False: tails start at every port that is 0 mod 0x20, including 0x20/0xa0 (8259), 0x40 (8253) and 0x60 (8042).
   * At 0x60 a tail's byte and its position are guest-visible (measured, GAP 1).
   * "not rowed per length" therefore leaves eight live cells unrowed on a false premise.
2. **Probe header and the session-4e comment:** "a head always ends at port 0x3ff" / "A split head always ends at port
   0x3ff (lane 3)".  A head ends at every port that is 0x1f mod 0x20.  Lane 3 is the invariant, 0x3ff is the probe's
   choice.  It is harmless for the cell, but it hides the swapmod coincidence above.
3. **POSTTABLE 3 (and PRETABLE 3):** "x_wfallthru 77 (PREDICTED EQUIVALENT on this probe ...) -- DISCLOSED".
   * "Equivalent on this probe" is accurate.
   * "DISCLOSED" is false: the probe header's contract has no such entry.
   * The edit is not equivalent for a guest (measured, GAP 2).  PRETABLE's own text names the ports that would catch it.
4. **Fix comment in dev_lca.c:** "or the 1- or 2-byte head of an unaligned LDL/LDQ that memory_rw splits at 1 KB".
   * It omits STL/STQ.  `fix530_20260914/HEAD_r3.out` records `h1 stq alive` and `h2 stq alive` = `dead` on HEAD.
   * The store heads ended the host too, and the probe's own row notes say so ("(1,3) STQ head ... was a host death on
     HEAD").
5. **Probe header CONTRACT, "at every cell of that space"**: this is false for the eight tail cells of item 1 while
   they stay unrowed.  It is true (x_rot, measured) for every direct and head cell.

POSTTABLE 3's per-mutant counts, re-derived from the diffs: c1_w2 75, c1_w1w 75, c1_r4 75, x_len6 74 (with the
`h2 stq` stays-green explanation), x_len8lane0 76, x_lane2clamp 72, x_w1drop 75.  I agree with all of them.  The base
77/77 and the head 49/77 = 20 + 8 are consistent with HEAD_r3.out.  I found nothing else wrong in it.

---

## CLONE

`/tmp/gxopus530c2` was restored by both drivers.  I re-checked it by hand before deleting: no `.MUTANT`,
`dev_lca.c` cmp-clean against GXEMUL-SEC, `gxemul -nt dev_lca.c`.  Then I **DELETED** it, together with
`/tmp/gxopus530c2_bins` and `/tmp/gxopus530c2_bins2`.  GXEMUL-SEC's `dev_lca.c` is unchanged: md5 `dc49ebdd...`
before and after.  The only project path written is `regress/artifacts/lcaisalane/opus_c2_20260914/`.


## KILL TABLE 4 on the 93-row instrument -- POSTTABLE

```
POSTTABLE -- #530 (lcaisalane) kill table 4, CLOSING PASS 2's REPAIR 3 (93 rows).  Written after the table (table4.out
ends KILL530D_DONE); PRETABLE.out 05:52:16 predates HEAD_r4/FIX_r4, the launch (kill530d.run-060752.sh) and every log.

DRIVER   kill530d.run-060752.sh (frozen), clone /tmp/gxlca530 (BASELINE_CMP CLEAN), own .MUTANT; 9 legs built; clone
         RESTORED (re-checked by hand: no .MUTANT, dev_lca.c cmp-clean vs GXEMUL-SEC, gxemul -nt source); `restored ==
         base (byte-identical)'; no mutant binary identical to base.
INSTRUMENT  lca_isalane_probe.table4.py BYTE-IDENTICAL to the shipped regress/lca_isalane_probe.py (cmp) and to the
         frozen copy HEAD_r4 / FIX_r4 ran (../lca_isalane_probe.r4.frozen.py): FIX_r4 93/93, HEAD_r4 52/93.
LOGS     9 logs/probe_*.raw, every one ends LCAISALANE_DONE; LCAISALANE_RETRIED=none on every leg.
LOAD     two probe lanes beside #529's kill table 8 (four lanes) and the #529 closing-pass-5 panel -- no retries.

check_pred.out:  CHECKPRED exact=9 differs=0 of 9 measured (9 predicted)
   base 93/93 · head 52/93 (41 red: table 3's 28 + the three new processes, each ending the host at its first (1,3) or
   (1,2) access after its control phase) · t_tails 85 (the Opus seat's 77/77 escape: all eight tail rows) · x_wfallthru 91
   (the Opus seat's 77/77 escape: iir stb, iir stl) · swapmod 87 (h7 ldq/stq and the t7/t5 tails -- 0x60 is 1 mod 5 and
   5 mod 7) · d_len3lane0 90 (h5 ldq via its 0x400 tail, tailr t3, tailw t3) · t_w7 92 · t_r6 92 · d_w6tail 92 (the
   per-phase command-byte RESET's own kill: without it tailw t6 reads t7's 0x44 and passes).
   Every leg DETECTED, every red set exactly as predicted.

*** THE CHECKER WAS CORRECTED AFTER THE RUN, AND ITS AS-RUN OUTPUT IS KEPT. ***  As run (check_pred.asrun.py ->
check_pred.asrun.out) it read `exact=8 differs=1', `head' DIFFERS with extra=['iir stl'] and a "missing" row made of
PRETABLE prose.  That was a PARSE defect, not a prediction miss: PRETABLE's head note is a NESTED parenthetical ("... a
(1,3) cell -- ... a (1,2) STB ..."), and the checker's `\(.*?\)' stopped at the first `)', leaving the tail of the note
glued to `iir stl'.  The fix strips innermost parentheticals until none remain; PRETABLE.out is untouched.  The measured
head set is the 41 rows PRETABLE lists, and 52/93 is its predicted score.  (Table 3's checker had the same regex and its
PRETABLE's notes were not nested; its exact=10 stands.)

FLOOR    (a) head 52/93; (d) the two DEPENDS-ON escapes closing pass 2 measured -- the tail mis-placement and the deleted
         write-arm `return' -- red; (e) THE CELL SPACE now includes the tail cells, the CONTRACT names x_wfallthru, and the
         DISCLOSED list names the address and data classes and the forward-return equivalents.
NOT RE-MEASURED  every table 1-3 kill: repair 3 ADDS sessions and changes no existing session's commands (the targeting
         rule), so none can move.
```

## QUESTIONS

1. **Does THE CELL SPACE now enumerate the whole space from the handler's own inputs** -- direct len 1/2/4/8 x lane 0-3 x
   R/W, heads len 1-7 at lane 3 x R/W, tails len 1-7 at lane 0 x R/W (1, 2, 4 = the direct lane-0 cells)?  Name any cell
   it omits, any cell listed as rowed whose row's channel cannot vary under the mutant it claims, and any DISCLOSED item
   (the address class, the data class, the forward-return equivalents) disclosed wrongly.
2. **Is there a floor gap in the 93-row detector?**  The smallest source edit to the FIXED `dev_lca.c` that changes a
   guest-visible outcome and still scores 93/93 -- as an exact edit, with the row you expected to catch it and why it
   cannot.
3. **Which statement in the header, the fix comment, or POSTTABLE 4 is wrong?**


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
