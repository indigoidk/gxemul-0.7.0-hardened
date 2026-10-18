**Your token: `ASTRA_MTE564F2_20261017`** -- open your answer with it.

# `#564` sgirekills (MTE half) -- §F2: THE PANEL SHARES ITS PASS-2 FINDINGS

## READ THIS FIRST

This is the adjudication pass.  Pass 2 had three answering seats -- GPT-6 Astra, Grok 4.7, GLM 5.3 -- each SHIP WITH
CHANGES; Fable 5.1 was a SEAT FAILURE (HTTP 429), and its stage is held by owner ruling.  Every finding is below, with
the main loop's disposition on each.  **Please do not ratify.**  The load-bearing question is: **WHICH OF MY ELEVEN
DISPOSITIONS IS WRONG?**  A seat whose own finding is adopted is asked to be HARDER on it -- including whether the
proposed REPAIR is right, not merely whether the finding was.

**THE TREE IS `GXEMUL-SEC/` AT HEAD `2951694f` PLUS THIS ROUND'S UNCOMMITTED EDITS** to `src/devices/dev_sgi_re.c`,
`regress/gate_arm.sh` and the new `regress/sgi_mte_decline_probe.py`.  The repair proposed here is NOT applied yet: the
working tree is exactly what pass 2 reviewed.  Everything a packet-fed seat needs is inlined in section 3.

**VERDICT LINE FIRST.**

## 1. The findings and the main loop's dispositions

| # | seat(s) | finding | disposition |
|---|---|---|---|
| F1 | Astra, GLM, Grok | A START-tagged READ also runs the transfer: `if (startFlag) do_mte_transfer(cpu, d);` (3d, `:1860-1861`) has no `writeflag` test.  The pass-2 brief's settled premise "only on a WRITE" was false, and the fix's comment (3a, `:1515-1517`) says "the register store that carried START has already landed" -- true of a write only. | **ACCEPT, L4.**  The comment becomes: *"The decline returns before any TRANSFER data is written.  On a START-tagged write the register store has already landed in the caller and stays; a START-tagged READ reaches here too (filed separately), and either way the caller's common tail still answers."*  The index-bound conclusion (`regnr + 1 <= 512`) is unaffected. |
| F2 | Astra | The probe header says the paint "is read after EVERY transfer, including the repeats"; the 32-mask sweep reads it once at the end (its own row note says so). | **ACCEPT, L4.**  Header corrected; no oracle change. |
| F3 | Astra, GLM, Grok | PRETABLE errata: (a) "0 and 1 are SAMPLED" -- source 1 is never driven; (b) `after status` "cannot vary under any mutant" -- `b1` reddens it (session death); (c) `after fill` "(no mutant rowed for that shape)" -- `s5hoist` reddened it; (d) `src 3 copy` "lands the source byte" -- source mode 3 reaches the helper's default return and the PUT writes BG, still not the paint; (e) "S2 at B/C, owed: none" -- see F9. | **ACCEPT, L4.**  `PRETABLE.out` stays as written (its timestamp, before table 1, is the order proof); the corrections go in a dated `PRETABLE_ERRATA.txt` beside it, each quoting the text it corrects. |
| F4 | Astra | The enum comment promises each message carries "the value in the text"; no row checks the printed values (`ntext()` matches key phrase + suffix only). | **ACCEPT** as an explicit no-row sentence in the probe contract. |
| F5 | Grok | "`CRIME_DE_STATUS` is the constant 0x1e000000": the macro is the OFFSET 0x4000; the value read is `IDLE \| SETUP_IDLE \| PIXPIPE_IDLE \| MTE_IDLE` = 0x1e000000. | **ACCEPT**, records wording.  The probe's expected word is right. |
| F6 | GLM | "3a is not the whole diff": three hunks shown, numstat net +53, hunks net +46. | **REJECT, measured.**  The packet's section 3a carries FOUR hunks -- `@@ -162,11 +162,28`, `@@ -1493,17 +1510,36`, `@@ -1578,13 +1614,23`, `@@ -1594,8 +1640,15` -- net +17 +19 +10 +7 = +53, equal to the numstat.  The fourth (S5) was missed in reading. |
| F7 | GLM | `if (src > MTE_TLB_C \|\| src == 1)` (refuses a legal source 1) and `&& bytemask != 0x00ff00ff` (exempts one multi-zero mask) keep all 53 green. | **DISCLOSE (clause e), not floor.**  Both are equality cases at an interior value the guarded body never tests as a case; the joint-cell rule discloses those.  The two edges of `src > MTE_TLB_C` ARE rowed (`src 3` refused, `src c fill`/`src c copy` accepted at 2).  The contract will name source 1 as never driven beside the already-disclosed mask sampling. |
| F8 | GLM | A decline that also WRITES an MTE register before returning stays green: no row reads an MTE register after a declined START. | **DISCLOSE** -- PRETABLE section 2 already says so; the contract will too. |
| F9 | Grok (and the main loop, checking Astra's coverage remark) | `if (src > MTE_TLB_C && dst_tlb != MTE_TLB_B)` keeps all 53 green (likewise `MTE_TLB_C`, `MTE_TLB_LIN_B`): S2 is rowed only at A and LIN_A. | **ACCEPT, L2 -- and wider than the three labels.**  S1's and S2's `return` BYPASSES `switch (dst_tlb)` (3a), so the 2026-09-25 skipped-dispatch label clause applies (text in 3e): the floor for EACH of S1 and S2 is {A, B, C, LIN_A, LIN_B} x latch {CLEAR, SET} -- labels 3/6/7 reach `default:`, which writes nothing, so they are excluded as host-debug only.  Rowed today: S1 6 of 10 (A both; B, C, LIN_A, LIN_B SET only), S2 3 of 10 (A both; LIN_A SET).  REPAIR: rows for the 11 empty cells -- S2 SET at B, C, LIN_B appended to the S2 session AFTER its last existing check, and four new sessions each pairing one S1-CLEAR and one S2-CLEAR cell (S1 at B / S2 at C; S1 at C / S2 at B; S1 at LIN_A / S2 at LIN_B; S1 at LIN_B / S2 at LIN_A).  Kill table 3 MEASURES all 20 latch-conditioned label-swap variants, e.g. `if (src > MTE_TLB_C && !(dst_tlb == MTE_TLB_B && !(d->warned & SGIRE_W_MTE_SRC)))`; a plain label exemption exempts a superset of cells, so its detection follows from either conditioned variant's. |
| F10 | Grok | Aliasing a new latch bit onto a PRE-EXISTING one -- `SGIRE_W_MTE_STIPPLE = 1 << 10` (= `SGIRE_W_BADMODE`), `SGIRE_W_MTE_COPY = 1 << 11` (= `SGIRE_W_TEX_RD`) -- keeps all 53 green: the only pre-existing bit any session sets is `SGIRE_W_TLBA_LEN`. | **ACCEPT, L2.**  The `#490` precedent (a latch-bit collision that escaped was a clause-(d) breach) and this file's own crossbit rows (`sgi_re_width_probe.py` `tex xbit`, `sgi_re_colourdefault_probe.py` `allbits`).  REPAIR: one new session sets every pre-existing bit 0-12 FIRST, using the priming sequence the `allbits` row already proved (plus its colour decline, which sets bit 12), then drives S1-S5; rows: `xbit primed` (all 13 priming announcements seen -- the row proves its own setup) and `xbit texts` (each new site announces exactly once).  Kill table 3 measures one alias per new site (Grok's two, plus S2, S4 and S5 onto three other pre-existing bits); every other (site, bit) pair is covered BY CONSTRUCTION via `xbit primed` -- recorded in that form, not as a measurement. |
| F11 | Grok | The `*surv` rows and `after status` stay green under the d-mutants (return removed, the transfer runs). | **NO CHANGE.**  Their named mutants are the b-mutants (exit reinstated), under which they red; the paint rows catch the d-mutants.  Recorded in the errata so the channel split is explicit. |

## 2. Disagreements

* **F6:** GLM's missing-hunk reading against the packet itself -- settled by counting the packet's `@@` lines (above).
* **F9's width:** Grok asked for the three refuse-side labels (S2 at B, C, LIN_B).  The main loop reads the 2026-09-25
  clause as demanding labels x latch for BOTH S1 and S2 -- 20 cells, 11 rows, 20 measured variants.  **Is the latch
  cross owed here, or is that an over-reading?**  The clause says "the repair path tests the warning latch, so its CLEAR
  and SET states belong explicitly in the enumeration", and that "detection of the plain variant does not discharge the
  latch-conditioned variants".  It also says it was MINTED FROM ONE DEVICE and must be fit-checked on first reuse --
  this is that reuse.
* **F10's by-construction step:** is one measured alias per site plus a priming-proof row enough, or must every (site,
  pre-existing bit) pair be measured (5 x 13 = 65 builds)?
* **F7:** GLM calls the source-1 growth "outside the sample" and asks that the floor claim be scoped to the enumeration;
  the main loop agrees on the scoping and disposes it as clause (e).

## 3. The evidence, inlined

### 3a. `do_mte_transfer()` (working tree, md5 1d65cdc1): the sibling warning, S1, S2 and the destination dispatch they bypass

```c
 1508  	if (dst_y_step != 0 && dst_y_step != 1 && dst_y_step != -1) {
 1509  		fatal("[ sgi_mte: TODO! unimplemented dst_y_step %i ]", dst_y_step);
 1510  		// exit(1);
 1511  	}
 1512  
 1513  	/*  #564: S1-S5 below DECLINE an unsupported transfer, with a latched
 1514  	    announcement; each used to end the process (fatal() + exit(1)).  The
 1515  	    decline returns before any TRANSFER data is written -- the register
 1516  	    store that carried START has already landed in the caller and stays,
 1517  	    and the caller's common tail still answers.  Each site has its own
 1518  	    latch bit (see the enum), and the `return' is OUTSIDE the latch, so
 1519  	    every refused transfer is refused and only the announcement is once.
 1520  	    Each old message's key phrase is kept in the new one.  */
 1521  	if (mode & MTE_MODE_STIPPLE) {
 1522  		if (!(d->warned & SGIRE_W_MTE_STIPPLE)) {
 1523  			d->warned |= SGIRE_W_MTE_STIPPLE;
 1524  			fatal("[ sgi_mte: unimplemented MTE_MODE_STIPPLE (mode "
 1525  			    "0x%08x) -- transfer declined (once) ]\n", mode);
 1526  		}
 1527  		return;
 1528  	}
 1529  
 1530  	int src_tlb = (mode & MTE_MODE_SRC_BUF_MASK) >> MTE_SRC_TLB_SHIFT;
 1531  	int dst_tlb = (mode & MTE_MODE_DST_BUF_MASK) >> MTE_DST_TLB_SHIFT;
 1532  	
 1533  	if (src > MTE_TLB_C) {
 1534  		/*  #564: kept as `src > MTE_TLB_C' for fills AND copies.  A fill
 1535  		    never reads the source, but nothing establishes what the
 1536  		    hardware does with SRC_BUF on a fill (filed separately).  */
 1537  		if (!(d->warned & SGIRE_W_MTE_SRC)) {
 1538  			d->warned |= SGIRE_W_MTE_SRC;
 1539  			fatal("[ sgi_mte: unimplemented SRC %i -- transfer "
 1540  			    "declined (once) ]\n", src);
 1541  		}
 1542  		return;
 1543  	}
 1544  
 1545  	switch (dst_tlb) {
 1546  	case MTE_TLB_A:
 1547  	case MTE_TLB_B:
 1548  	case MTE_TLB_C:
 1549  		// Used by NetBSD's crmfb_fill_rect. It puts graphical
 1550  		// coordinates in dst0 and dst1.
 1551  		{
 1552  			int x1 = (dst0 >> 16) & 0xfff;
 1553  			int y1 = dst0 & 0xfff;
 1554  			int x2 = (dst1 >> 16) & 0xfff;
 1555  			int y2 = dst1 & 0xfff;
 1556  			x1 /= (depth / 8);
 1557  			x2 /= (depth / 8);
 1558  
 1559  			int src_x1 = (src0 >> 16) & 0xfff;
```

### 3b. The linear arm: S3, S4 and S5 sit INSIDE the dispatch (they bypass no dispatch)

```c
 1613  	case MTE_TLB_LIN_A:
 1614  	case MTE_TLB_LIN_B:
 1615  		// Used by the PROM to zero-fill memory (?).
 1616  		if (mode & MTE_MODE_COPY) {
 1617  			if (!(d->warned & SGIRE_W_MTE_COPY)) {
 1618  				d->warned |= SGIRE_W_MTE_COPY;
 1619  				fatal("[ sgi_mte: unimplemented MTE_MODE_COPY to "
 1620  				    "linear dst_tlb %i -- transfer declined (once)"
 1621  				    " ]\n", dst_tlb);
 1622  			}
 1623  			return;
 1624  		}
 1625  
 1626  		if (depth != 8) {
 1627  			if (!(d->warned & SGIRE_W_MTE_DEPTH)) {
 1628  				d->warned |= SGIRE_W_MTE_DEPTH;
 1629  				fatal("[ sgi_mte: unimplemented MTE_DEPTH_x: depth "
 1630  				    "%i to linear dst_tlb %i -- transfer declined "
 1631  				    "(once) ]\n", depth, dst_tlb);
 1632  			}
 1633  			return;
 1634  		}
 1635  
 1636  		debug("[ sgi_mte: LINEAR TRANSFER: mode=0x%08x dst0=0x%016llx,"
 1637  		    " dst1=0x%016llx (length 0x%llx), dst_y_step=%i bg=0x%x, bytemask=0x%x ]\n",
 1638  		    mode,
 1639  		    (long long)dst0, (long long)dst1,
 1640  		    (long long)dstlen, dst_y_step, (int)bg, (int)bytemask);
 1641  
 1642  		if (bytemask != 0xffffffff) {
 1643  			/*  #564: BYTEMASK is zeroed at init, so a guest that never
 1644  			    stores it reaches this decline.  */
 1645  			if (!(d->warned & SGIRE_W_MTE_BYTEMASK)) {
 1646  				d->warned |= SGIRE_W_MTE_BYTEMASK;
 1647  				fatal("[ sgi_mte: unimplemented MTE bytemask 0x%08x "
 1648  				    "to linear dst_tlb %i -- transfer declined (once)"
 1649  				    " ]\n", (int)bytemask, dst_tlb);
 1650  			}
 1651  			return;
 1652  		}
 1653  
 1654  		/*
 1655  		 *  Horrible hack:
```

### 3c. The latch enum's tail (the five new bits)

```c
  139  	SGIRE_W_BADMODE   = 1 << 10,
  140  
  141  	/*
  142  	    #513: THE TEX READ DECLINE GETS ITS OWN BIT, not SGIRE_W_TEX_LEN.
  143  	    Sharing one was measured at 23/25 for SGIRE_W_DE_LEN in #498: an
  144  	    ordinary narrow write fires the width latch, and the read decline is
  145  	    then silently suppressed for the life of the instance.  The detector
  146  	    has a row for exactly this (`tex xbit', which fires all six width
  147  	    latches before reading).
  148  
  149  	    (This comment used to end "THE NEXT FREE BIT IS 1 << 12, AND THIS
  150  	    IS THE LAST ENUMERATOR".  #519 added SGIRE_W_BADCOLOR = 1 << 12
  151  	    BELOW this line and moved the sentence with it, as this comment
  152  	    itself instructed.  Demoted, not deleted, for the same reason as
  153  	    the two demotions above it.)
  154  	 */
  155  	SGIRE_W_TEX_RD    = 1 << 11,
  156  
  157  	/*  #519 (sgirandomcolour): the colour-type PUT decline in
  158  	    horrible_getputpixel() gets its OWN bit, per the rule every entry
  159  	    above records: the helper is per-pixel, the struct is shared by
  160  	    four handlers, and a latch shared with any other site is silenced
  161  	    by that site's ordinary traffic.  SGIRE_W_BADMODE (1 << 10) is the
  162  	    TLB/mode switch's decline in the same function and is a different
  163  	    event with a different text; sharing it would collapse the two.
  164  
  165  	    (This comment used to end "THE NEXT FREE BIT IS 1 << 13, AND THIS
  166  	    IS THE LAST ENUMERATOR".  #564 added SGIRE_W_MTE_STIPPLE ..
  167  	    SGIRE_W_MTE_BYTEMASK = 1 << 13 .. 1 << 17 BELOW this line and moved
  168  	    the sentence with them, as this comment itself instructed.  Demoted,
  169  	    not deleted, for the same reason as the demotions above it.)  */
  170  	SGIRE_W_BADCOLOR  = 1 << 12,
  171  
  172  	/*  #564 (sgirekills, MTE half): do_mte_transfer()'s five declines, ONE
  173  	    BIT PER SITE, for the reason every entry above records -- a latch
  174  	    shared with another site is silenced by that site's traffic.  LIN_A
  175  	    and LIN_B are two values of ONE guard at S3-S5, the shape of
  176  	    SGIRE_W_BADMODE (one bit, the value in the text).
  177  
  178  	    THE NEXT FREE BIT IS 1 << 18, AND THIS IS THE LAST ENUMERATOR --
  179  	    which is where that claim belongs, per the convention above.  A
  180  	    maintainer adding a bit BELOW this line must move this sentence
  181  	    with it and demote the copy here.  */
  182  	SGIRE_W_MTE_STIPPLE  = 1 << 13,
  183  	SGIRE_W_MTE_SRC      = 1 << 14,
  184  	SGIRE_W_MTE_COPY     = 1 << 15,
  185  	SGIRE_W_MTE_DEPTH    = 1 << 16,
  186  	SGIRE_W_MTE_BYTEMASK = 1 << 17,
```

### 3d. `DEVICE_ACCESS(sgi_mte)`'s tail: START runs the transfer on a read or a write

```c
 1856  			fatal("[ sgi_mte: unimplemented read from address"
 1857  			    " 0x%llx ]\n", (long long)relative_addr);
 1858  	}
 1859  
 1860  	if (startFlag)
 1861  		do_mte_transfer(cpu, d);
 1862  
 1863  	if (writeflag == MEM_READ)
 1864  		memory_writemax64(cpu, data, len, odata);
 1865  
 1866  	return 1;
```

### 3e. The skipped-dispatch label clause, quoted from the project carrier (`CLAUDE.md`)

> **AND A GUARD THAT SUPPRESSES A DISPATCH ADDS A THIRD DISJUNCT TO THE 2026-09-09 LABEL CLAUSE, adjudicated 2026-09-25 on `#529` by the flagship's first-hand Q3 re-ruling, with GPT-6 Astra's amendments of 2026-09-26 (`crimewidthkill/rerule_20260925/`); this text is the codex seat's 2026-09-26 rewrite of the clause (`codexfarm_20260926/codex_carrierq3.txt`, "faithful with changes"), adopted with three corrections by the flagship's final ruling of 2026-09-30 (`crimewidthkill/final529r18_20260926/fable5_final.md`, item E): a dispatch LABEL is ALSO a floor axis when the edited guard's repair bypasses that dispatch in the enclosing function.  This is an alternative to selector data flow into the guarded body or re-testing after the join; absence of those two connections does not put a qualifying suppression label in clause (e).  At CRIME the repair is `goto crime_declined`, bypassing the register switch.  The jump omits the dispatch; that omission does not make the whole repair path empty of reads, writes or tests (it reads and writes the latch).  The added axis consists of the skipped dispatch's GUEST-OBSERVABLE labels.  Cross it with the applicable code-tested predicate and state partitions under the existing bounds: the guard's dominating predicates and the jointly reachable device-state lvalues read by the fix's own repair path, as defined by pass 11 above.  This does not make every test or state in the skipped arms a floor axis; the existing partition, reachability and generating-set bounds still apply.  At `#529` the repair path tests the warning latch, so its CLEAR and SET states belong explicitly in the enumeration.  TIME and REV with the latch SET were the demonstrated holes at repair 14 -- `M3_timelatch` and `M5_revlatch` escaped at 204/204 while `M4_timeplain` was detected at 200/204 and `M6_istlatch` at 201/204 (`repair14_20260916/POSTTABLE.out`) -- and were CLOSED by repair 15 (table 14: 214/218 both; table 16: 222/226 both, `table16_20260926/POSTTABLE16.out`).  Those holes were never the whole enumeration, and detection of the plain TIME variant does not discharge the latch-conditioned variants.  The INTMASK and CONTROL-write label-swaps were measured DETECTED: table 13a `M7_intmasklatch` / `M8_ctllatch` 201/204 each, table 16 223/226 each.  An OFFSET within one label is not an axis unless the body distinguishes it: `#529`'s entry 34 (`sd +0x40`, latch CLEAR) is unrowed while its label cell is held at +0x278 -- the unrowed-slot class, clause (e).  Include only labels whose skipped arms have guest-observable effects.  CRIME's DOG arm is a bare `break;` and its `default:` body is host-debug only, so neither contributes a floor label for THIS skipped-dispatch face.  This exclusion does not establish guest equivalence for ACCEPTED accesses at those labels: CRIME's width arm supplies `+0x0c`'s observable value before `default:` prints.  DISCHARGE requires measured DETECTION by the shipped instrument of each enumerated label-swap variant, including the relevant state-conditioned variants.  Existing rows may discharge them; predictions or aggregate detection do not substitute for the individual measurements.  Table 11's K2 PER-ROW prediction error is the recorded caution.  The added label enumeration is bounded to the ONE skipped dispatch in the enclosing function; it does not recurse into further dispatches or dispatches in callees.  MINTED FROM ONE DEVICE: on first reuse, check that the skipped-label enumeration and its bounded predicate/state product fit the new device.**

### 3f. The detector's S1 and S2 sessions (`regress/sgi_mte_decline_probe.py`, md5 86caed24) -- the rows F9 is about

```python
  235  # ================================================================ S1 STIPPLE: every destination
  236  s = Sess(); tiles(s, a=True, b=True, c=True)
  237  for lab, mode in (("a", DST_A | D32), ("b", DST_B | D32), ("c", DST_C | D32)):
  238      s.sw(TDEST, PAINT); s.go(STIPPLE | mode); s.check(TDEST, "t" + lab)
  239  s.sw(TDEST + 4, SRC_WORD); s.sw(TDEST, PAINT); s.go(STIPPLE | COPY | DST_A | SRC(0) | D32, src0=SRC_PIX); s.check(TDEST, "tcopy")
  240  for lab in ("a", "b"):
  241      lin_map(s, lab); s.sw(LDEST, PAINT)
  242      s.go(STIPPLE | (DST_LA if lab == "a" else DST_LB) | D8, linear=True, bytemask=0xffffffff); s.check(LDEST, "l" + lab)
  243  s.sw(SCRATCH, LIVE_VAL); s.check(SCRATCH, "live")
  244  t, alive, r = s.run()
  245  row("stip a", kept(r["ta"]), "paint kept", "S1, tiled A fill at depth 32")
  246  row("stip b", kept(r["tb"]), "paint kept", "S1, tiled B")
  247  row("stip c", kept(r["tc"]), "paint kept", "S1, tiled C")
  248  row("stip copy", kept(r["tcopy"]), "paint kept", "S1, tiled A COPY (the tiled COPY arm would run)")
  249  row("stip lin a", kept(r["la"]), "paint kept", "S1, LIN_A depth 8 full mask (S3-S5 all pass)")
  250  row("stip lin b", kept(r["lb"]), "paint kept", "S1, LIN_B depth 8 full mask")
  251  row("stip surv", "survived" if r["live"] == "0x%x" % LIVE_VAL else "died", "survived", "six refused transfers, then RAM")
  252  row("stip once", ntext(t, "S1") if alive else "died", 1, "six refusals, one announcement")
  253  
  254  # ================================================================ S2 src > MTE_TLB_C: the refused domain {3..7}
  255  s = Sess(); tiles(s, a=True, c=True)
  256  for v in (3, 4, 5, 6, 7):
  257      s.sw(TDEST, PAINT); s.go(SRC(v) | DST_A | D32); s.check(TDEST, "f%d" % v)
  258  s.sw(TDEST + 4, SRC_WORD); s.sw(TDEST, PAINT); s.go(COPY | SRC(3) | DST_A | D32, src0=SRC_PIX); s.check(TDEST, "copy3")
  259  lin_map(s, "a"); s.sw(LDEST, PAINT); s.go(SRC(3) | DST_LA | D8, linear=True, bytemask=0xffffffff); s.check(LDEST, "lin3")
  260  s.sw(TDEST, PAINT); s.go(SRC(2) | DST_A | D32); s.check(TDEST, "fillc")
  261  s.sw(TDEST + 4, SRC_WORD); s.sw(TDEST, PAINT); s.go(COPY | SRC(2) | DST_A | D32, src0=SRC_PIX); s.check(TDEST, "copyc")
  262  s.sw(SCRATCH, LIVE_VAL); s.check(SCRATCH, "live")
  263  t, alive, r = s.run()
  264  for v in (3, 4, 5, 6, 7):
  265      row("src %d" % v, kept(r["f%d" % v]), "paint kept", "S2, tiled A fill, src field %d" % v)
  266  row("src 3 copy", kept(r["copy3"]), "paint kept", "S2's active side: a COPY from src 3")
  267  row("src 3 lin", kept(r["lin3"]), "paint kept", "S2 at a linear destination")
  268  row("src c fill", landed(r["fillc"]), "landed", "ACCEPT: src 2 = MTE_TLB_C, the bound")
  269  row("src c copy", top(r["copyc"]), "0x1a", "ACCEPT: a COPY from TLB_C lands the source's first byte")
  270  row("src surv", "survived" if r["live"] == "0x%x" % LIVE_VAL else "died", "survived", "seven refused transfers, then RAM")
  271  row("src once", ntext(t, "S2") if alive else "died", 1, "seven refusals, one announcement")
```

### 3g. The detector's LATCH session -- the only one that sets a pre-existing bit (F10)

```python
  339  # ================================================================ LATCH: an existing bit first, then S1..S5 and S1 again, in one session
  340  s = Sess(); tiles(s, a=True)
  341  s.sw(RE_TLB_A, 0)                                       # a 4-byte store: SGIRE_W_TLBA_LEN, announced once
  342  s.sw(TDEST, PAINT); s.go(STIPPLE | DST_A | D32); s.check(TDEST, "s1")
  343  s.sw(TDEST, PAINT); s.go(SRC(3) | DST_A | D32); s.check(TDEST, "s2")
  344  lin_map(s, "a")
  345  s.sw(LDEST, PAINT); s.go(COPY | DST_LA | D8, linear=True, bytemask=0xffffffff); s.check(LDEST, "s3")
  346  s.sw(LDEST, PAINT); s.go(DST_LA | D16, linear=True, bytemask=0xffffffff); s.check(LDEST, "s4")
  347  s.sw(LDEST, PAINT); s.go(DST_LA | D8, linear=True, bytemask=0x0000ffff); s.check(LDEST, "s5")
  348  tiles(s, a=True)
  349  s.sw(TDEST, PAINT); s.go(STIPPLE | DST_A | D32); s.check(TDEST, "s1again")
  350  s.sw(RE_TLB_A, 0)                                       # the existing bit again: must NOT announce a second time
  351  s.sw(SCRATCH, LIVE_VAL); s.check(SCRATCH, "live")
  352  t, alive, r = s.run()
  353  paints = [r[k] for k in ("s1", "s2", "s3", "s4", "s5", "s1again")]
  354  row("latch paint", "all kept" if all(v == P for v in paints) else ("died" if "died" in paints else "written"),
  355      "all kept", "six refusals incl. a repeat of S1 after the latch is set")
  356  row("latch texts", "/".join(str(ntext(t, k)) for k in ("S1", "S2", "S3", "S4", "S5")) if alive else "died",
  357      "1/1/1/1/1", "five distinct sites in one session: five bits, not one")
  358  row("latch old bit", len(re.findall(re.escape(TLBA_LEN_TEXT), t)) if alive else "died", 1,
  359      "SGIRE_W_TLBA_LEN set before the new sites stays set after them")
```

### 3h. Kill table 1 rows the findings cite (`KILLTABLE.txt`)

```
d1        46/53 KILLED   caught by: stip a, stip b, stip c, stip copy, stip lin a, stip lin b, latch paint
                         predicted: stip a/b/c/copy/lin
d2        45/53 KILLED   caught by: src 3, src 4, src 5, src 6, src 7, src 3 copy, src 3 lin, latch paint
                         predicted: src 3-7 (tiled fill lands), src 3 lin
--
s2tiled   52/53 KILLED   caught by: src 3 lin
                         predicted: src 3 lin
--
shared    52/53 KILLED   caught by: latch texts
                         predicted: latch texts (S2 silenced by S1)
--
wrongbit  51/53 KILLED   caught by: mask once, latch texts
                         predicted: mask once, latch texts
```


## 4. Questions

Answer in this order, each with its number.  Facts you checked carry `path:line` or a quoted line.

**Q1 -- WHICH OF MY ELEVEN DISPOSITIONS IS WRONG?**  For each one you dispute: the finding number, why, and the
disposition you would give instead.  If your own finding was adopted, be harder on it -- is the proposed REPAIR right?

**Q2 -- F9.**  (a) Is the latch cross (labels x {CLEAR, SET}, for S1 AND S2) owed by the clause in 3e, or is it an
over-reading -- and if owed, is anything MISSING from the 20-cell set?  (b) Each CLEAR cell is the FIRST refusal of
its site in its session; does pairing one S1-CLEAR and one S2-CLEAR cell per session confound either cell?  (c) The
three S2-SET rows are appended after the S2 session's last existing check: can that change any existing row's
observable?

**Q3 -- F10.**  (a) Is priming bits 0-12 first, then S1-S5, the right shape?  (b) Is one measured alias per new site,
plus a row proving all 13 primings fired, enough -- or must more (site, bit) pairs be measured?

**Q4 -- ANYTHING MISSED.**  A finding none of the three seats raised, or a consequence of the repair (rows added to an
instrument perturb nothing already measured?) that the dispositions do not cover.

Format: open with your token, then ONE line `VERDICT: ALL UPHELD / <n> WRONG (<finding numbers>)`, then Q1-Q4.
