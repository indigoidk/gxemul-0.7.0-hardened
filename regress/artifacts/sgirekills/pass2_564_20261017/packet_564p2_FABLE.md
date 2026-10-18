**Your token: `FABLE_MTE564P2_20261017`** -- open your answer with it.

# `#564` sgirekills (MTE half) -- PASS 2: the diff, the detector and its kill table

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly.  **Check the premises,
not just the derivations.**  A seat that re-derives a fact from something this brief did NOT give it is worth more than
a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/` AT HEAD `2951694f` PLUS THIS ROUND'S UNCOMMITTED WORKING-TREE CHANGES** to
`src/devices/dev_sgi_re.c`, `regress/gate_arm.sh` and the new `regress/sgi_mte_decline_probe.py` -- all three inlined
below.  The working tree also carries another session's uncommitted edits to OTHER files (`dev_lca.c`, `dev_pcc2.c`,
`dev_sh4.c`, `cpu_alpha_palcode.c`, some regress files); they are not this round's.  Ignore the pristine upstream
copies of GXemul under the project root (`./src/`, `_archive/...`).

**If you cannot read files that is expected** -- every fact you need is inlined.  Name any premise you cannot settle.

**VERDICT LINE FIRST.**

---

## 1. What pass 1 decided (three seats answered; full record `pass1_564_20261017/CONVERGENCE.md`)

GPT-6 Astra, Grok 4.7 and GLM 5.3 each answered PROCEED WITH CHANGES; Fable 5.1 was a SEAT FAILURE (HTTP 429, usage
limit), its stage held by owner ruling.  Unanimous design: **member 3 (decline the transfer, latched announcement) at
all five sites**, `return` OUTSIDE the latch, S2 kept as `src > MTE_TLB_C` for fills and copies, one latch bit per site
(`1 << 13` .. `1 << 17`), messages carrying the refused value and `-- transfer declined (once)` with each old key phrase
kept.  Detector rows were added for every hole the three seats named: BYTEMASK never written (the reset default), the
whole refused source domain {3,4,5,6,7}, S1/S2 at every destination kind, S3-S5 at both linear labels, all refused
depths at both labels, the 32 single-zero masks, a same-session five-site latch row and an existing-bit row, linear
fixtures that map the page in only the selected array, the PROM's own mode `0x11`, tiled transfers with a partial mask,
and a decline followed by a working transfer.  Declined: moving S5 above the linear arm's `debug()` (host-only, minimal
diff).  Filed for later rounds: S2 narrowed to COPY (needs a hardware warrant); IMPLEMENT at S4/S5; START honoured on a
READ of a START-tagged address (Astra).

**Settled premises -- each with its warrant, so no seat need re-derive them:**
* `fatal()` RETURNS.  `src/core/debugmsg.c:384-391` is `va_start; va_debug(argp, fmt); va_end;` and nothing else -- no
  `exit`, no early-out.  A declined site is `fatal()` once, then `return`.
* A transfer runs only on a WRITE whose address carries the START bit (`0x800`): `DEVICE_ACCESS(sgi_mte)` takes
  `startFlag = relative_addr & CRIME_DE_START` and masks it off before decoding (section 3c).  So the largest register
  index is `0x7ff / 4 = 511` and the 64-bit arm's `regnr + 1` stays inside the 1024-word `mte_reg[]`.
* `CRIME_DE_STATUS` is the constant `0x1e000000` (`DEVICE_ACCESS(sgi_de_status)`), which is why it is the probe's
  device-signature control.
* `BYTEMASK` is zero at init: `dev_sgi_re_init()` allocates ONE `struct sgi_re_data` and `memset`s it to zero
  (`dev_sgi_re.c:864-865`), and `dev_sgi_mte_init()` registers the MTE window over that same struct (`:871`, `:1873-1877`)
  without writing any register.  So a guest that never writes BYTEMASK reaches S5 with mask 0 -- the `mask unwritten`
  row.

## 2. The measurements (every number names its log, all under `regress/artifacts/sgirekills/`)

| what | HEAD `2951694f` (scratch build) | the fix (same tree, only `dev_sgi_re.c` replaced) | log |
|---|---|---|---|
| rung-3 witness `witness_20261017/sgi_mte_exit_witness.py` (md5 dcbb328d) | 4/9 -- five deaths, each with ONLY its own text | 9/9 -- five survivals, own text present | `witness_20261017/witness_HEAD_2951694f.out`, `witness_FIX_564.out` |
| detector as TABLED (md5 8d625289, 14-column names) | 8/53 -- controls 3 and ACCEPT 5 green, every decline row `died` | 53/53 | `detector_564_20261017/probe_HEAD_2951694f.out`, `probe_FIX_564.out` |
| detector as SHIPPED (16-column names, otherwise identical) | see section 6 | see section 6 | `detector_564_20261017/probe_*_shipped.out` |
| null medium (`/bin/true` as the binary) | -- | 0/53 | `killtable_564_20261017/raw/null.out` |
| kill table, 34 one-edit mutants of the fix | -- | **34/34 caught** | `killtable_564_20261017/KILLTABLE.txt` (section 5) |
| kill table 2: the two ACCEPT-side growth mutants table 1 lacked (S1 and S3), SHIPPED instrument | -- | **2/2 caught** -- `s1grow` 52/53, `s3growa` 50/53; base 53/53, null 0/53 | `killtable_564_20261017/KILLTABLE2.txt` (section 5d) |

**A CONSTRUCTION DEFECT OF MINE, CAUGHT BEFORE ANY TABLE (L1):** the detector's first draft (md5 ceed62be) compared the
`lw` result -- which SIGN-EXTENDS, so the paint `0x99999999` reads back as `0xffffffff99999999` -- against the 32-bit
literal.  Every `paint kept` row read "written" on the fixed build, and every `landed` row was vacuous (a surviving paint
also differed from the literal).  Fixed by masking each read to 32 bits; both builds re-run on the corrected instrument;
the flawed runs are kept as `detector_564_20261017/*.v1_signext.out`.  **Then a second, format-only change:** two row
names are exactly 14 characters, and the gate greps `^<name>  .*ok$` (two spaces), so the name field went 14 -> 16
columns.  The tabled instrument was reconstructed from the shipped file by reverting only that edit, and its md5
reproduces `8d625289` exactly (`killtable_564_20261017/sgi_mte_decline_probe.tabled.py`).

## 3. The files this round changes (`git diff --numstat`, each marked)

```
36	0	regress/gate_arm.sh    INLINED (section 3d)
65	12	src/devices/dev_sgi_re.c    INLINED (section 3a, and 3b-3c whole)
372	0	regress/sgi_mte_decline_probe.py    NEW FILE, INLINED WHOLE (section 4)
```

No other file is this round's.  Diff hunks inlined: `dev_sgi_re.c` 4, `gate_arm.sh` 1.

### 3a. `src/devices/dev_sgi_re.c` -- the whole diff against HEAD (working tree md5 1d65cdc1, HEAD 60203f67)

```diff
diff --git a/src/devices/dev_sgi_re.c b/src/devices/dev_sgi_re.c
index 2eff3075..d60df35d 100644
--- a/src/devices/dev_sgi_re.c
+++ b/src/devices/dev_sgi_re.c
@@ -162,11 +162,28 @@ enum {
 	    TLB/mode switch's decline in the same function and is a different
 	    event with a different text; sharing it would collapse the two.
 
-	    THE NEXT FREE BIT IS 1 << 13, AND THIS IS THE LAST ENUMERATOR --
+	    (This comment used to end "THE NEXT FREE BIT IS 1 << 13, AND THIS
+	    IS THE LAST ENUMERATOR".  #564 added SGIRE_W_MTE_STIPPLE ..
+	    SGIRE_W_MTE_BYTEMASK = 1 << 13 .. 1 << 17 BELOW this line and moved
+	    the sentence with them, as this comment itself instructed.  Demoted,
+	    not deleted, for the same reason as the demotions above it.)  */
+	SGIRE_W_BADCOLOR  = 1 << 12,
+
+	/*  #564 (sgirekills, MTE half): do_mte_transfer()'s five declines, ONE
+	    BIT PER SITE, for the reason every entry above records -- a latch
+	    shared with another site is silenced by that site's traffic.  LIN_A
+	    and LIN_B are two values of ONE guard at S3-S5, the shape of
+	    SGIRE_W_BADMODE (one bit, the value in the text).
+
+	    THE NEXT FREE BIT IS 1 << 18, AND THIS IS THE LAST ENUMERATOR --
 	    which is where that claim belongs, per the convention above.  A
 	    maintainer adding a bit BELOW this line must move this sentence
 	    with it and demote the copy here.  */
-	SGIRE_W_BADCOLOR  = 1 << 12,
+	SGIRE_W_MTE_STIPPLE  = 1 << 13,
+	SGIRE_W_MTE_SRC      = 1 << 14,
+	SGIRE_W_MTE_COPY     = 1 << 15,
+	SGIRE_W_MTE_DEPTH    = 1 << 16,
+	SGIRE_W_MTE_BYTEMASK = 1 << 17,
 };
 
 struct sgi_re_data {
@@ -1493,17 +1510,36 @@ void do_mte_transfer(struct cpu* cpu, struct sgi_re_data *d)
 		// exit(1);
 	}
 
+	/*  #564: S1-S5 below DECLINE an unsupported transfer, with a latched
+	    announcement; each used to end the process (fatal() + exit(1)).  The
+	    decline returns before any TRANSFER data is written -- the register
+	    store that carried START has already landed in the caller and stays,
+	    and the caller's common tail still answers.  Each site has its own
+	    latch bit (see the enum), and the `return' is OUTSIDE the latch, so
+	    every refused transfer is refused and only the announcement is once.
+	    Each old message's key phrase is kept in the new one.  */
 	if (mode & MTE_MODE_STIPPLE) {
-		fatal("[ sgi_mte: unimplemented MTE_MODE_STIPPLE ]");
-		exit(1);
+		if (!(d->warned & SGIRE_W_MTE_STIPPLE)) {
+			d->warned |= SGIRE_W_MTE_STIPPLE;
+			fatal("[ sgi_mte: unimplemented MTE_MODE_STIPPLE (mode "
+			    "0x%08x) -- transfer declined (once) ]\n", mode);
+		}
+		return;
 	}
 
 	int src_tlb = (mode & MTE_MODE_SRC_BUF_MASK) >> MTE_SRC_TLB_SHIFT;
 	int dst_tlb = (mode & MTE_MODE_DST_BUF_MASK) >> MTE_DST_TLB_SHIFT;
 	
 	if (src > MTE_TLB_C) {
-		fatal("[ sgi_mte: unimplemented SRC ]");
-		exit(1);
+		/*  #564: kept as `src > MTE_TLB_C' for fills AND copies.  A fill
+		    never reads the source, but nothing establishes what the
+		    hardware does with SRC_BUF on a fill (filed separately).  */
+		if (!(d->warned & SGIRE_W_MTE_SRC)) {
+			d->warned |= SGIRE_W_MTE_SRC;
+			fatal("[ sgi_mte: unimplemented SRC %i -- transfer "
+			    "declined (once) ]\n", src);
+		}
+		return;
 	}
 
 	switch (dst_tlb) {
@@ -1578,13 +1614,23 @@ void do_mte_transfer(struct cpu* cpu, struct sgi_re_data *d)
 	case MTE_TLB_LIN_B:
 		// Used by the PROM to zero-fill memory (?).
 		if (mode & MTE_MODE_COPY) {
-			fatal("[ sgi_mte: unimplemented MTE_MODE_COPY ]");
-			exit(1);
+			if (!(d->warned & SGIRE_W_MTE_COPY)) {
+				d->warned |= SGIRE_W_MTE_COPY;
+				fatal("[ sgi_mte: unimplemented MTE_MODE_COPY to "
+				    "linear dst_tlb %i -- transfer declined (once)"
+				    " ]\n", dst_tlb);
+			}
+			return;
 		}
 
 		if (depth != 8) {
-			fatal("[ sgi_mte: unimplemented MTE_DEPTH_x ]");
-			exit(1);
+			if (!(d->warned & SGIRE_W_MTE_DEPTH)) {
+				d->warned |= SGIRE_W_MTE_DEPTH;
+				fatal("[ sgi_mte: unimplemented MTE_DEPTH_x: depth "
+				    "%i to linear dst_tlb %i -- transfer declined "
+				    "(once) ]\n", depth, dst_tlb);
+			}
+			return;
 		}
 
 		debug("[ sgi_mte: LINEAR TRANSFER: mode=0x%08x dst0=0x%016llx,"
@@ -1594,8 +1640,15 @@ void do_mte_transfer(struct cpu* cpu, struct sgi_re_data *d)
 		    (long long)dstlen, dst_y_step, (int)bg, (int)bytemask);
 
 		if (bytemask != 0xffffffff) {
-			fatal("unimplemented MTE bytemask 0x%08x\n", (int)bytemask);
-			exit(1);
+			/*  #564: BYTEMASK is zeroed at init, so a guest that never
+			    stores it reaches this decline.  */
+			if (!(d->warned & SGIRE_W_MTE_BYTEMASK)) {
+				d->warned |= SGIRE_W_MTE_BYTEMASK;
+				fatal("[ sgi_mte: unimplemented MTE bytemask 0x%08x "
+				    "to linear dst_tlb %i -- transfer declined (once)"
+				    " ]\n", (int)bytemask, dst_tlb);
+			}
+			return;
 		}
 
 		/*
```

### 3b. `do_mte_transfer()` AFTER the fix -- WHOLE, every exit path, working-tree line numbers

```c
 1485  void do_mte_transfer(struct cpu* cpu, struct sgi_re_data *d)
 1486  {
 1487  	uint32_t mode = d->mte_reg[(CRIME_MTE_MODE - 0x3000) / sizeof(uint32_t)];
 1488  	uint32_t src0 = d->mte_reg[(CRIME_MTE_SRC0 - 0x3000) / sizeof(uint32_t)];
 1489  	uint32_t src1 = d->mte_reg[(CRIME_MTE_SRC1 - 0x3000) / sizeof(uint32_t)];
 1490  	uint32_t dst0 = d->mte_reg[(CRIME_MTE_DST0 - 0x3000) / sizeof(uint32_t)];
 1491  	uint32_t dst1 = d->mte_reg[(CRIME_MTE_DST1 - 0x3000) / sizeof(uint32_t)];
 1492  	int32_t src_y_step = d->mte_reg[(CRIME_MTE_SRC_Y_STEP - 0x3000) / sizeof(uint32_t)];
 1493  	int32_t dst_y_step = d->mte_reg[(CRIME_MTE_DST_Y_STEP - 0x3000) / sizeof(uint32_t)];
 1494  	uint32_t dstlen = dst1 - dst0 + 1, fill_addr;
 1495  	unsigned char zerobuf[4096];
 1496  	int depth = 8 << ((mode & MTE_MODE_DEPTH_MASK) >> MTE_DEPTH_SHIFT);
 1497  	int src = (mode & MTE_MODE_SRC_BUF_MASK) >> MTE_SRC_TLB_SHIFT;
 1498  	uint32_t bytemask = d->mte_reg[(CRIME_MTE_BYTEMASK - 0x3000) / sizeof(uint32_t)];
 1499  	uint32_t bg = d->mte_reg[(CRIME_MTE_BG - 0x3000) / sizeof(uint32_t)];
 1500  
 1501  	debug("[ sgi_mte: STARTING: mode=0x%08x src0=0x%08x src1=0x%08x src_y_step=%i dst0=0x%08x,"
 1502  	    " dst1=0x%08x dst_y_step=%i bg=0x%x bytemask=0x%x ]\n",
 1503  	    mode,
 1504  	    src0, src1, src_y_step,
 1505  	    dst0, dst1, dst_y_step,
 1506  	    bg, bytemask);
 1507  
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
 1560  			int src_y1 = src0 & 0xfff;
 1561  			// int src_x2 = (src1 >> 16) & 0xfff;
 1562  			// int src_y2 = src1 & 0xfff;
 1563  			src_x1 /= (depth / 8);
 1564  			// src_x2 /= (depth / 8);
 1565  
 1566  			int dx = x1 > x2 ? -1 : 1;
 1567  			int dy = y1 > y2 ? -1 : 1;
 1568  			
 1569  			uint32_t src_mode = (src_tlb << 10) + (((mode & MTE_MODE_DEPTH_MASK) >> MTE_DEPTH_SHIFT) << 8);
 1570  			uint32_t dst_mode = (dst_tlb << 10) + (((mode & MTE_MODE_DEPTH_MASK) >> MTE_DEPTH_SHIFT) << 8);
 1571  
 1572  			// Hack. The MTE perhaps doesn't deal with colors per se,
 1573  			// but this makes sure that we copy 32 bits when doing 32-bit
 1574  			// transfers.
 1575  			/*  #509: was `depth == 4' -- UNREACHABLE.  `depth' is
 1576  			    a count of BITS (8 << a two-bit field, so 8/16/32/64
 1577  			    only); 4 is the corresponding BYTE count, which the
 1578  			    author used correctly in the `/ (depth / 8)' lines
 1579  			    just above.  So both assignments were dead, every
 1580  			    tiled transfer took the CI arm, and at 32 bits CI
 1581  			    assigns buf[0] alone while memory_rw copies four --
 1582  			    publishing three bytes of host stack into guest
 1583  			    memory.  The comment above states the intended
 1584  			    condition in words: 32-bit transfers.
 1585  
 1586  			    This repairs the 32-bit cell ONLY.  The 16-bit and
 1587  			    reserved-encoding-3 cells assign fewer bytes than
 1588  			    they copy for the same reason and are NOT closed
 1589  			    here -- see the uninitialised-buffer sibling.  */
 1590  			if (depth == 32) {	/*  #509  */
 1591  				src_mode |= DE_MODE_TYPE_RGBA;
 1592  				dst_mode |= DE_MODE_TYPE_RGBA;
 1593  			}
 1594  
 1595  			int src_y = src_y1;
 1596  			for (int y = y1; y != y2+dy; y += dy) {
 1597  				int src_x = src_x1;
 1598  				
 1599  				for  (int x = x1; x != x2+dx; x += dx) {
 1600  					if (mode & MTE_MODE_COPY) {
 1601  						horrible_getputpixel(0, cpu, d,
 1602  							src_x, src_y, &bg, src_mode);
 1603  						src_x += dx;
 1604  					}
 1605  
 1606  					horrible_getputpixel(1, cpu, d, x, y, &bg, dst_mode);
 1607  				}
 1608  				
 1609  				src_y += dy;
 1610  			}
 1611  		}
 1612  		break;
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
 1656  		 *
 1657  		 *  During bootup, the PROM fills memory at 0x40000000 and
 1658  		 *  forward. This corresponds to the lowest possible RAM address.
 1659  		 *  However, these fills are not going via the CPU's cache,
 1660  		 *  which contains things such as the return address on the
 1661  		 *  stack. If we _really_ write this data in the emulator (which
 1662  		 *  doesn't emulate the cache), it would overwrite the stack.
 1663  		 *
 1664  		 *  So let's not.
 1665  		 *
 1666  		 *  (If some guest OS or firmware variant actually depends on
 1667  		 *  the ability to write to the start of memory this way,
 1668  		 *  it would not work in the emulator.)
 1669  		 */
 1670  		// if (dst0 >= 0x40000000 && dst0 < 0x40004000 && dst1 > 0x40004000) {
 1671  		//	dst0 += 0x4000;
 1672  		//	dstlen -= 0x4000;
 1673  		// }
 1674  
 1675  		/*
 1676  		 *  HUH?
 1677  		 *
 1678  		 *  Note that due to a bug (?) in the PROM firmware when it
 1679  		 *  is setting up the TLB entries, only every _second_ page is
 1680  		 *  actually put correctly in the TLB. This means that even
 1681  		 *  though it then tries to fill 0x40000000 .. 0x40007fff with
 1682  		 *  zeroes, it only fills 0x40001000 .. 0x40001fff,
 1683  		 *  0x40003000 .. 0x40003fff and so on!
 1684  		 *
 1685  		 *  So the Horrible hack above is not needed.
 1686  		 *
 1687  		 *  Ironic.
 1688  		 */
 1689  
 1690  		memset(zerobuf, bg, dstlen < sizeof(zerobuf) ? dstlen : sizeof(zerobuf));
 1691  		fill_addr = dst0;
 1692  		while (dstlen != 0) {
 1693  			uint64_t fill_len;
 1694  			if (dstlen > sizeof(zerobuf))
 1695  				fill_len = sizeof(zerobuf);
 1696  			else
 1697  				fill_len = dstlen;
 1698  
 1699  			uint64_t starting_page = fill_addr & ~0xfff;
 1700  			uint64_t ending_page = (fill_addr + fill_len - 1) & ~0xfff;
 1701  			if (starting_page != ending_page) {
 1702  				fill_len = starting_page + 4096 - fill_addr;
 1703  			}
 1704  
 1705  			// Find starting_page in the TLB in question.
 1706  			starting_page >>= 12;
 1707  			uint32_t *tlb = dst_tlb == MTE_TLB_LIN_A ? d->re_linear_a : d->re_linear_b;
 1708  			int match = 0;
 1709  			for (int i = 0; i < 32; ++i) {
 1710  				uint32_t entry = tlb[i];
 1711  				if (entry & 0x80000000) {
 1712  					entry &= ~0x80000000;
 1713  					if (entry == starting_page) {
 1714  						match = 1;
 1715  						break;
 1716  					}
 1717  				}
 1718  			}
 1719  			
 1720  			if (match) {
 1721  				cpu->memory_rw(cpu, cpu->mem, fill_addr, zerobuf, fill_len,
 1722  					MEM_WRITE, NO_EXCEPTIONS | PHYSICAL);
 1723  			} else {
 1724  				debug("[ sgi_mte: WARNING: address 0x%x not found in TLB? Ignoring fill. ]\n",
 1725  					(long long)fill_addr);
 1726  			}
 1727  
 1728  			fill_addr += fill_len;
 1729  			dstlen -= (uint32_t)fill_len;	/* OB-23: subtract bytes actually filled */
 1730  		}
 1731  		break;
 1732  	default:
 1733  		fatal("[ sgi_mte: TODO! unimplemented dst_tlb 0x%x ]", dst_tlb);
 1734  	}
 1735  }
```

### 3c. `DEVICE_ACCESS(sgi_mte)` -- WHOLE (unchanged): the only caller, and the common tail after `do_mte_transfer()` returns

```c
 1737  DEVICE_ACCESS(sgi_mte)
 1738  {
 1739  	struct sgi_re_data *d = (struct sgi_re_data *) extra;
 1740  	uint64_t idata = 0, odata = 0;
 1741  	int regnr;
 1742  	int startFlag = relative_addr & CRIME_DE_START;
 1743  
 1744  	relative_addr &= ~CRIME_DE_START;
 1745  
 1746  	idata = memory_readmax64(cpu, data, len);
 1747  	regnr = relative_addr / sizeof(uint32_t);
 1748  
 1749  	relative_addr += 0x3000;
 1750  
 1751  	/*
 1752  	 *  Treat all registers as read/write, by default.  Sometimes these
 1753  	 *  are accessed as 32-bit words, sometimes as 64-bit words.
 1754  	 *
 1755  	 *  NOTE: The lowest bits are internally stored in the "low" (+0)
 1756  	 *  register, and the higher bits are stored in the "+1" word.
 1757  	 */
 1758  	if (len == 4) {
 1759  		if (writeflag == MEM_WRITE)
 1760  			d->mte_reg[regnr] = idata;
 1761  		else
 1762  			odata = d->mte_reg[regnr];
 1763  	} else if (len != 4) {
 1764  		if (writeflag == MEM_WRITE) {
 1765  			d->mte_reg[regnr+1] = idata >> 32;
 1766  			d->mte_reg[regnr] = idata;
 1767  		} else {
 1768  			odata = ((uint64_t)d->mte_reg[regnr+1] << 32) +
 1769  			    d->mte_reg[regnr];
 1770  		}
 1771  	} else {
 1772  		fatal("[ sgi_mte: UNIMPLEMENTED read/write len %i ]\n", len);
 1773  		exit(1);
 1774  	}
 1775  
 1776  	switch (relative_addr) {
 1777  
 1778  	case CRIME_MTE_MODE:
 1779  		debug("[ sgi_mte: %s CRIME_MTE_MODE: 0x%016llx ]\n",
 1780  		    writeflag == MEM_WRITE ? "write to" : "read from",
 1781  		    writeflag == MEM_WRITE ? (long long)idata : (long long)odata);
 1782  		break;
 1783  
 1784  	case CRIME_MTE_BYTEMASK:
 1785  		debug("[ sgi_mte: %s CRIME_MTE_BYTEMASK: 0x%016llx ]\n",
 1786  		    writeflag == MEM_WRITE ? "write to" : "read from",
 1787  		    writeflag == MEM_WRITE ? (long long)idata : (long long)odata);
 1788  		break;
 1789  
 1790  	case CRIME_MTE_STIPPLEMASK:
 1791  		fatal("[ sgi_mte: %s CRIME_MTE_STIPPLEMASK: 0x%016llx ]\n",
 1792  		    writeflag == MEM_WRITE ? "write to" : "read from",
 1793  		    writeflag == MEM_WRITE ? (long long)idata : (long long)odata);
 1794  		break;
 1795  
 1796  	case CRIME_MTE_BG:
 1797  		debug("[ sgi_mte: %s CRIME_MTE_BG: 0x%016llx ]\n",
 1798  		    writeflag == MEM_WRITE ? "write to" : "read from",
 1799  		    writeflag == MEM_WRITE ? (long long)idata : (long long)odata);
 1800  		break;
 1801  
 1802  	case CRIME_MTE_SRC0:
 1803  		debug("[ sgi_mte: %s CRIME_MTE_SRC0: 0x%016llx ]\n",
 1804  		    writeflag == MEM_WRITE ? "write to" : "read from",
 1805  		    writeflag == MEM_WRITE ? (long long)idata : (long long)odata);
 1806  		break;
 1807  
 1808  	case CRIME_MTE_SRC1:
 1809  		debug("[ sgi_mte: %s CRIME_MTE_SRC1: 0x%016llx ]\n",
 1810  		    writeflag == MEM_WRITE ? "write to" : "read from",
 1811  		    writeflag == MEM_WRITE ? (long long)idata : (long long)odata);
 1812  		break;
 1813  
 1814  	case CRIME_MTE_DST0:
 1815  		debug("[ sgi_mte: %s CRIME_MTE_DST0: 0x%016llx ]\n",
 1816  		    writeflag == MEM_WRITE ? "write to" : "read from",
 1817  		    writeflag == MEM_WRITE ? (long long)idata : (long long)odata);
 1818  		break;
 1819  
 1820  	case CRIME_MTE_DST1:
 1821  		debug("[ sgi_mte: %s CRIME_MTE_DST1: 0x%016llx ]\n",
 1822  		    writeflag == MEM_WRITE ? "write to" : "read from",
 1823  		    writeflag == MEM_WRITE ? (long long)idata : (long long)odata);
 1824  		break;
 1825  
 1826  	case CRIME_MTE_SRC_Y_STEP:
 1827  		debug("[ sgi_mte: %s CRIME_MTE_SRC_Y_STEP: 0x%016llx ]\n",
 1828  		    writeflag == MEM_WRITE ? "write to" : "read from",
 1829  		    writeflag == MEM_WRITE ? (long long)idata : (long long)odata);
 1830  		break;
 1831  
 1832  	case CRIME_MTE_DST_Y_STEP:
 1833  		debug("[ sgi_mte: %s CRIME_MTE_DST_Y_STEP: 0x%016llx ]\n",
 1834  		    writeflag == MEM_WRITE ? "write to" : "read from",
 1835  		    writeflag == MEM_WRITE ? (long long)idata : (long long)odata);
 1836  		break;
 1837  
 1838  	case CRIME_MTE_NULL:
 1839  		fatal("[ sgi_mte: %s CRIME_MTE_NULL: 0x%016llx ]\n",
 1840  		    writeflag == MEM_WRITE ? "write to" : "read from",
 1841  		    writeflag == MEM_WRITE ? (long long)idata : (long long)odata);
 1842  		break;
 1843  
 1844  	case CRIME_MTE_FLUSH:
 1845  		fatal("[ sgi_mte: %s CRIME_MTE_FLUSH: 0x%016llx ]\n",
 1846  		    writeflag == MEM_WRITE ? "write to" : "read from",
 1847  		    writeflag == MEM_WRITE ? (long long)idata : (long long)odata);
 1848  		break;
 1849  
 1850  	default:
 1851  		if (writeflag == MEM_WRITE)
 1852  			fatal("[ sgi_mte: unimplemented write to "
 1853  			    "address 0x%llx, data=0x%016llx ]\n",
 1854  			    (long long)relative_addr, (long long)idata);
 1855  		else
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
 1867  }
```

### 3d. `regress/gate_arm.sh` -- the whole diff (the targeted gate's new block)

```diff
diff --git a/regress/gate_arm.sh b/regress/gate_arm.sh
index b0cdc001..b1b7b35f 100644
--- a/regress/gate_arm.sh
+++ b/regress/gate_arm.sh
@@ -1470,6 +1470,42 @@ else
 
 fi
 
+#  ---- #564 sgirekills (MTE half): do_mte_transfer()'s five refusals of an unsupported transfer parameter --
+#  ---- stipple, a source buffer past MTE_TLB_C, and COPY / depth != 8 / a partial BYTEMASK to a LINEAR
+#  ---- destination -- each DECLINE with a latched announcement, where each used to end the process.  Wired
+#  ---- IN THE SAME COMMIT as the fix.  Measured with one instrument: 8/53 on the pre-fix build (HEAD
+#  ---- 2951694f; only the controls and the five ACCEPT rows green) and 53/53 on the fix
+#  ---- (regress/artifacts/sgirekills/detector_564_20261017/).  Modelled on the sgi_re_width_probe block
+#  ---- (find it with `grep -n 'sgi_re_width_probe.py "$PMAX"' gate_arm.sh`), at depth 0 so a sibling
+#  ---- probe's missing sentinel cannot swallow it.
+MTELOG=$LOGDIR/sgi_mte_decline.log
+python3 sgi_mte_decline_probe.py "$PMAX" gate > "$MTELOG" 2>&1 || true
+
+if ! grep -q "MTEDECL_DONE" "$MTELOG"; then
+    note "sgi_mte decline probe did not reach its completion sentinel; last lines follow"
+    tail -5 "$MTELOG" | sed 's/^/       /'
+    check "sgi_mte decline probe completed" "no" "yes"
+else
+    grep -E " ok$| FAIL$" "$MTELOG" | sed 's/^/       /'
+
+    #  CONTROLS BY NAME: a run whose controls died is an APPARATUS failure, not 50 product failures.
+    for c in "live" "devsig" "mode rt"; do
+        check "sgi_mte control: $c" "$(count "$MTELOG" "^$c  .*ok$")" "1"
+    done
+
+    #  PER ROW, ONE LINE.  The probe prints a name of at most 14 characters in a 16-column field, so every
+    #  name is followed by TWO spaces and "^<name>  " cannot match a longer name that starts with it.
+    for v in "live" "devsig" "mode rt" "stip a" "stip b" "stip c" "stip copy" "stip lin a" "stip lin b" "stip surv" "stip once" "src 3" "src 4" "src 5" "src 6" "src 7" "src 3 copy" "src 3 lin" "src c fill" "src c copy" "src surv" "src once" "copy lin a" "copy lin b" "copy surv" "copy once" "depth a 16" "depth a 32" "depth a 64" "depth b 16" "depth b 32" "depth b 64" "depth surv" "depth once" "mask unwritten" "mask unw surv" "mask 0000ffff" "mask fffffffe" "mask 7fffffff" "mask sweep" "mask lin b" "mask surv" "mask once" "lin fill a" "lin fill b" "lin fill ecc" "tile mask" "tile copy mask" "latch paint" "latch texts" "latch old bit" "after fill" "after status"; do
+        check "sgi_mte row: $v" "$(count "$MTELOG" "^$v  .*ok$")" "1"
+    done
+
+    #  DENOMINATOR PINNED TO A LITERAL, summed arithmetically (count() is plain grep: a `|' would be literal).
+    check "sgi_mte rows emitted" \
+          "$(( $(count "$MTELOG" " ok$") + $(count "$MTELOG" " FAIL$") ))" "53"
+    check "sgi_mte rows green"   "$(count "$MTELOG" " ok$")"   "53"
+    check "sgi_mte rows red"     "$(count "$MTELOG" " FAIL$")" "0"
+fi
+
 #  ---- *** MOVED OUT ONE NESTING LEVEL, 2026-08-31.  It was pasted INSIDE the
 #  ---- sgi_re_width probe's success branch, so if THAT probe missed its sentinel this
 #  ---- block was never invoked at all -- 28 rows, three denominators and its own
```

## 4. The detector, WHOLE -- `regress/sgi_mte_decline_probe.py` as shipped (md5 86caed24, 372 lines)

The TABLED instrument (md5 8d625289) differs from this file in one place only: the row-name field is 14 columns
there and 16 here (section 2).

```python
   1  #!/usr/bin/env python3
   2  #
   3  #  #564 sgirekills (MTE half) -- DETECTOR: dev_sgi_re.c's do_mte_transfer() refuses five unsupported transfer
   4  #  parameters by DECLINING the transfer with a latched announcement, where it used to end the process:
   5  #
   6  #      S1  mode & MTE_MODE_STIPPLE              (before the destination switch: every destination)
   7  #      S2  src > MTE_TLB_C                      (before the switch: every destination, fill or copy)
   8  #      S3  mode & MTE_MODE_COPY                 (MTE_TLB_LIN_A / LIN_B only -- tiled COPY is implemented)
   9  #      S4  depth != 8                           (linear only)
  10  #      S5  bytemask != 0xffffffff               (linear only)
  11  #
  12  #  Every row is a REAL GUEST STORE or LOAD through real address decode and memory_rw on the unmodified
  13  #  `-E sgi -e ip32' machine (session mechanics from regress/sgi_mte_fill_probe.py, #509): the MTE is programmed
  14  #  with `sw', the RE TLBs with `sd', and a transfer fires on the write whose ADDRESS carries CRIME_DE_START.
  15  #
  16  #  ---------------------------------------------------------------------------------------------
  17  #  CONTRACT (vacuity-floor clause (e)) -- WHAT THIS DETECTOR IS DESIGNED TO CATCH.
  18  #
  19  #  * the terminating call put back at any site (every session ends at its first refused transfer);
  20  #  * the decline removed but the announcement kept -- the transfer proceeding with the refused parameter
  21  #    ignored (member 1): every refused transfer is aimed at a destination it WOULD write, pre-painted, and the
  22  #    row reads the paint back.  Tiled destinations use the #509 tile (re_tlb_[abc][0] = 0x8002 -> phys
  23  #    0x20000); linear ones map phys page 0x30 in ONLY the array the arm reads (`sd 0x8000003000000000' to
  24  #    CRIME_RE_LINEAR_A or _B), cleared again after use;
  25  #  * a guard scoped to fewer destinations, sources, depths or masks than today's: S1 at tiled A/B/C, tiled A
  26  #    COPY, LIN_A and LIN_B (at depth 8 with a full mask, so S4/S5 cannot hide the escape); S2 at every refused
  27  #    source value {3,4,5,6,7} on a tiled fill, at 3 on a tiled COPY and on a linear fill; S3 and S4 at both
  28  #    linear labels, S4 at every refused depth {16,32,64}; S5 at the reset default (BYTEMASK never written), at
  29  #    0x0000ffff, 0xfffffffe, 0x7fffffff, at LIN_B, and across all 32 single-zero masks (one row);
  30  #  * a guard grown to refuse legal transfers -- the ACCEPT side: a tiled fill and a tiled COPY at src C
  31  #    (the S2 bound), linear fills at both labels and at the PROM's own mode 0x11 (DST_ECC), and tiled
  32  #    fill/COPY with a non-full BYTEMASK (the linear restrictions must stay inside their branch);
  33  #  * the latch: a missing announcement, a missing suppression, a `return' moved INSIDE the latch (the paint is
  34  #    read after EVERY transfer, including the repeats), a bit shared between two new sites (one session drives
  35  #    S1..S5 then S1 again and wants five distinct texts once each), and an assignment that clears an EXISTING
  36  #    bit (SGIRE_W_TLBA_LEN, set first by one 4-byte store to CRIME_RE_TLB_A, must not announce again).
  37  #
  38  #  NOT CLAIMED: the rendering result of any ACCEPTED transfer beyond "it landed" (tiled fill: the word left the
  39  #  paint; tiled COPY: the source's first byte; linear fill: 0x44444444) -- #509's own detector owns the tiled
  40  #  colour channel; the `dst_y_step' and `default:' sibling arms (rows mtetlbflood, sgimtetlbdefault); START
  41  #  honoured on a READ (filed); destination labels 3, 6, 7 (they reach the default arm, which writes nothing,
  42  #  so a paint row there cannot see an S1/S2 escape -- disclosed, not rowed); masks with two or more zero bits
  43  #  beyond the four rowed ones (sampled, not exhausted).
  44  #
  45  #  Clause (c), the null medium: an absent or non-emulator binary -- every session dies, every row that reads a
  46  #  value or a survival reds (measured, not claimed: see the round's artifacts).
  47  #
  48  #  Usage:  sgi_mte_decline_probe.py <gxemul-binary> [label]
  49  import os, sys, pty, select, time, re, tempfile
  50  
  51  BIN   = sys.argv[1]
  52  LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"
  53  
  54  rows = []
  55  def row(name, got, want, note=""):
  56      ok = (got == want)
  57      rows.append((name, ok))
  58      #  16 columns for a name of at most 14: the gate greps "^<name>  .*ok$" (TWO spaces), and a name as long as
  59      #  its column leaves one -- the padded-column trap.  (The kill table ran the 14-column draft; only this
  60      #  width differs, see the round's artifacts.)
  61      print("%-16s %-22s %-12s %-56s %s" % (name, str(got), str(want), note, "ok" if ok else "FAIL"))
  62      return ok
  63  
  64  OP_SW_T0_A3 = 0xace80000          # sw   $t0, 0($a3)
  65  OP_SD_T0_A3 = 0xfce80000          # sd   $t0, 0($a3)
  66  OP_LW_V0_AT = 0x8c220000          # lw   $v0, 0($at)
  67  OP_B_SELF   = 0x1000ffff          # b    .
  68  OP_NOP      = 0x00000000
  69  
  70  CODE      = 0x80001000
  71  SCRATCH   = 0xa0001800
  72  LIVE_VAL  = 0x5a5a5a5a
  73  SENTINEL  = 0xdeadbeef
  74  DE_STATUS = 0xb5004000
  75  DE_STAT   = "0x1e000000"          # CRIME_DE_STATUS: IDLE|SETUP_IDLE|PIXPIPE_IDLE|MTE_IDLE; RAM reads 0
  76  
  77  DUMMY = os.path.join(tempfile.gettempdir(), "sgi_mte_decline_dummy.bin")
  78  if not os.path.exists(DUMMY):
  79      with open(DUMMY, "wb") as f:
  80          f.write(b"\0" * 8)
  81  
  82  #  CRIME base 0xb5000000 (KSEG1); offsets from src/include/thirdparty/crmfbreg.h.
  83  RE_TLB_A, RE_TLB_B, RE_TLB_C = 0xb5001000, 0xb5001200, 0xb5001400
  84  RE_LIN_A, RE_LIN_B           = 0xb5001700, 0xb5001780
  85  MTE_MODE       = 0xb5003000
  86  MTE_BYTEMASK   = 0xb5003008
  87  MTE_BG         = 0xb5003018
  88  MTE_SRC0       = 0xb5003020
  89  MTE_DST0       = 0xb5003030
  90  MTE_DST1_START = 0xb5003838       # CRIME_MTE_DST1 0x3038 | CRIME_DE_START 0x0800
  91  
  92  #  MTE_MODE: DST_BUF 0x1c >> 2, SRC_BUF 0xe0 >> 5, DEPTH 0x300 >> 8 (depth = 8 << field), STIPPLE 0x400, COPY 0x800.
  93  DST_A, DST_B, DST_C, DST_LA, DST_LB = 0 << 2, 1 << 2, 2 << 2, 4 << 2, 5 << 2
  94  D8, D16, D32, D64 = 0x000, 0x100, 0x200, 0x300
  95  STIPPLE, COPY, ECC = 0x400, 0x800, 0x001
  96  def SRC(v): return v << 5
  97  
  98  TILE      = 0x8002                # re_tlb_[abc][0]: bit 15 valid -> phys 0x20000 (the #509 tile)
  99  TDEST     = 0xa0020000            # tiled pixel (0,0), KSEG1
 100  LPAGE     = 0x80000030            # linear entry: valid | page 0x30
 101  LDEST     = 0xa0030000            # linear destination, KSEG1 of phys 0x30000
 102  LDST0, LDST1 = 0x00030000, 0x00030003
 103  PAINT     = 0x99999999
 104  BG_VAL    = 0x11223344
 105  SRC_WORD  = 0x1a2b3c4d            # first byte < 0x80 (sgirebufshiftub), four distinct bytes
 106  SRC_PIX   = 4 << 16               # SRC0: x = 4 bytes -> pixel 1 at depth 32
 107  
 108  #  Each site's announcement.  The key phrase is HEAD's own text (the witness attributes on it); the suffix is the
 109  #  decline's -- so a count of the SUFFIXED text counts declines, never a HEAD-style death message.
 110  DECL = "transfer declined (once)"
 111  KEY = {"S1": "unimplemented MTE_MODE_STIPPLE", "S2": "unimplemented SRC", "S3": "unimplemented MTE_MODE_COPY",
 112         "S4": "unimplemented MTE_DEPTH_x", "S5": "unimplemented MTE bytemask"}
 113  TLBA_LEN_TEXT = "for CRIME_RE_TLB_A -- declined.  (once)"
 114  
 115  def ntext(t, site):
 116      return len(re.findall(re.escape(KEY[site]) + r"[^\]\n]*" + re.escape(DECL), t))
 117  
 118  def session(cmds, settle=1.5, spin=1.8):
 119      pid, fd = pty.fork()
 120      if pid == 0:
 121          os.execv(BIN, [BIN, "-V", "-x", "-E", "sgi", "-e", "ip32", "-M", "64", "0x%x:" % CODE + DUMMY])
 122          os._exit(127)
 123      buf = ""
 124      def rd(t):
 125          nonlocal buf
 126          end = time.time() + t
 127          while time.time() < end:
 128              r, _, _ = select.select([fd], [], [], 0.1)
 129              if not r:
 130                  continue
 131              try:
 132                  d = os.read(fd, 65536)
 133                  if not d:
 134                      return False
 135                  buf += d.decode("latin-1", "replace")
 136              except OSError:
 137                  return False
 138          return True
 139      alive = rd(settle)
 140      for i, c in enumerate(cmds):
 141          try:
 142              os.write(fd, (c + "\n").encode("latin-1"))
 143          except OSError:
 144              alive = False; break
 145          if not rd(spin if i == len(cmds) - 1 else 0.22):
 146              alive = False; break
 147      try:
 148          os.write(fd, b"quit\n"); rd(0.4)
 149      except OSError:
 150          pass
 151      try:
 152          os.close(fd)
 153      except OSError:
 154          pass
 155      return buf.replace("\r", ""), alive
 156  
 157  class Sess(object):
 158      """One emulator session: a growing list of debugger commands, each check a labelled `lw' + `print v0'.
 159      Values come back IN ORDER; a check after the session ended reads 'died'."""
 160      def __init__(self):
 161          self.a = CODE; self.cmds = []; self.checks = []; self.reg = {}
 162      def _ops(self, ops):
 163          at = self.a; self.a += 4 * (len(ops) + 2) + 0x20
 164          put = ["put w 0x%x, 0x%08x" % (at + 4 * i, op) for i, op in enumerate(ops)]
 165          put += ["put w 0x%x, 0x%08x" % (at + 4 * len(ops), OP_B_SELF),
 166                  "put w 0x%x, 0x%08x" % (at + 4 * len(ops) + 4, OP_NOP)]
 167          self.cmds += put + ["pc=0x%x" % at, "step %d" % len(ops)]
 168      def sw(self, addr, val):
 169          self.cmds += ["a3=0x%x" % addr, "t0=0x%x" % val]; self._ops([OP_SW_T0_A3])
 170      def sd(self, addr, val):
 171          self.cmds += ["a3=0x%x" % addr, "t0=0x%x" % val]; self._ops([OP_SD_T0_A3])
 172      def mte(self, addr, val, force=False):
 173          """An MTE register store, skipped when the register already holds the value (the transfer reads the
 174          registers, so a skipped store is the same machine state)."""
 175          if force or self.reg.get(addr) != val:
 176              self.sw(addr, val); self.reg[addr] = val
 177      def check(self, addr, label):
 178          self.cmds += ["at=0x%x" % addr, "v0=0x%x" % SENTINEL]; self._ops([OP_LW_V0_AT])
 179          self.cmds += ["print v0"]; self.checks.append(label)
 180      def go(self, mode, linear=False, bytemask=None, src0=None):
 181          if bytemask is not None:
 182              self.mte(MTE_BYTEMASK, bytemask)
 183          self.mte(MTE_MODE, mode)
 184          self.mte(MTE_BG, BG_VAL)
 185          if src0 is not None:
 186              self.mte(MTE_SRC0, src0)
 187          self.mte(MTE_DST0, LDST0 if linear else 0)
 188          self.sw(MTE_DST1_START, LDST1 if linear else 0)        # START: always stored, never skipped
 189      def run(self):
 190          t, alive = session(self.cmds)
 191          vals = re.findall(r"print\s+v0\s*\n\s*(0x[0-9a-f]+)", t)
 192          res = {}
 193          for i, lab in enumerate(self.checks):
 194              #  `lw' SIGN-EXTENDS: the paint 0x99999999 reads back as 0xffffffff99999999.  Compare the 32 bits the
 195              #  guest loaded.  (The first draft compared the whole register, so every `paint kept' row read
 196              #  "written" on the fixed build and every `landed' row was vacuous -- a paint that survived also
 197              #  differed from the 32-bit literal.  Measured 2026-10-17, probe_FIX_564.v1_signext.out.)
 198              res[lab] = ("0x%x" % (int(vals[i], 16) & 0xffffffff)) if i < len(vals) else "died"
 199          return t, alive, res
 200  
 201  def tiles(s, a=True, b=False, c=False):
 202      if a: s.sd(RE_TLB_A, TILE << 48)
 203      if b: s.sd(RE_TLB_B, TILE << 48)
 204      if c: s.sd(RE_TLB_C, TILE << 48)
 205  
 206  def lin_map(s, which):
 207      """Map phys page 0x30 in ONLY the named linear array; clear the other."""
 208      s.sd(RE_LIN_A, (LPAGE << 32) if which == "a" else 0)
 209      s.sd(RE_LIN_B, (LPAGE << 32) if which == "b" else 0)
 210  
 211  P = "0x%x" % PAINT
 212  def top(v):
 213      return v if not v.startswith("0x") else "0x%02x" % ((int(v, 16) >> 24) & 0xff)
 214  def landed(v):
 215      return "died" if v == "died" else ("paint" if v == P else "landed")
 216  def kept(v):
 217      return "died" if v == "died" else ("paint kept" if v == P else "written")
 218  
 219  print("# sgi_mte_decline_probe -- binary=%s label=%s machine=sgi/ip32, %s" % (BIN, LABEL, time.strftime("%Y-%m-%d %H:%M:%S")))
 220  print("%-16s %-22s %-12s %-56s %s" % ("row", "got", "want", "note", ""))
 221  
 222  # ================================================================ controls
 223  s = Sess(); s.sw(SCRATCH, LIVE_VAL); s.check(SCRATCH, "v")
 224  t, alive, r = s.run()
 225  row("live", r["v"], "0x%x" % LIVE_VAL, "RAM round-trip: the session and the CPU run")
 226  
 227  s = Sess(); s.check(DE_STATUS, "v")
 228  t, alive, r = s.run()
 229  row("devsig", r["v"], DE_STAT, "CRIME_DE_STATUS: only the device answers this")
 230  
 231  s = Sess(); s.mte(MTE_MODE, STIPPLE | D32); s.check(MTE_MODE, "v")
 232  t, alive, r = s.run()
 233  row("mode rt", r["v"], "0x%x" % (STIPPLE | D32), "an MTE register through the sgi_mte decode; no START")
 234  
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
 272  
 273  # ================================================================ S3 linear COPY, both labels
 274  s = Sess()
 275  for lab in ("a", "b"):
 276      lin_map(s, lab); s.sw(LDEST, PAINT)
 277      s.go(COPY | (DST_LA if lab == "a" else DST_LB) | D8, linear=True, bytemask=0xffffffff); s.check(LDEST, lab)
 278  s.sw(SCRATCH, LIVE_VAL); s.check(SCRATCH, "live")
 279  t, alive, r = s.run()
 280  row("copy lin a", kept(r["a"]), "paint kept", "S3, LIN_A")
 281  row("copy lin b", kept(r["b"]), "paint kept", "S3, LIN_B")
 282  row("copy surv", "survived" if r["live"] == "0x%x" % LIVE_VAL else "died", "survived", "")
 283  row("copy once", ntext(t, "S3") if alive else "died", 1, "")
 284  
 285  # ================================================================ S4 linear depth != 8: {16,32,64} x both labels
 286  s = Sess()
 287  for lab in ("a", "b"):
 288      lin_map(s, lab)
 289      for dn, dv in (("16", D16), ("32", D32), ("64", D64)):
 290          s.sw(LDEST, PAINT); s.go((DST_LA if lab == "a" else DST_LB) | dv, linear=True, bytemask=0xffffffff)
 291          s.check(LDEST, lab + dn)
 292  s.sw(SCRATCH, LIVE_VAL); s.check(SCRATCH, "live")
 293  t, alive, r = s.run()
 294  for lab in ("a", "b"):
 295      for dn in ("16", "32", "64"):
 296          row("depth %s %s" % (lab, dn), kept(r[lab + dn]), "paint kept", "S4, LIN_%s depth %s" % (lab.upper(), dn))
 297  row("depth surv", "survived" if r["live"] == "0x%x" % LIVE_VAL else "died", "survived", "")
 298  row("depth once", ntext(t, "S4") if alive else "died", 1, "six refusals, one announcement")
 299  
 300  # ================================================================ S5 bytemask: the reset default, in a session that never stores it
 301  s = Sess(); lin_map(s, "a"); s.sw(LDEST, PAINT); s.go(DST_LA | D8, linear=True); s.check(LDEST, "v")
 302  s.sw(SCRATCH, LIVE_VAL); s.check(SCRATCH, "live")
 303  t, alive, r = s.run()
 304  row("mask unwritten", kept(r["v"]), "paint kept", "S5 at BYTEMASK's reset value 0, never stored")
 305  row("mask unw surv", "survived" if r["live"] == "0x%x" % LIVE_VAL else "died", "survived", "")
 306  
 307  # ================================================================ S5 bytemask: edges, LIN_B, and the 32 single-zero masks
 308  s = Sess(); lin_map(s, "a")
 309  for m in (0x0000ffff, 0xfffffffe, 0x7fffffff):
 310      s.sw(LDEST, PAINT); s.go(DST_LA | D8, linear=True, bytemask=m); s.check(LDEST, "m%08x" % m)
 311  s.sw(LDEST, PAINT)
 312  for b in range(32):
 313      s.mte(MTE_BYTEMASK, 0xffffffff ^ (1 << b)); s.sw(MTE_DST1_START, LDST1)
 314  s.check(LDEST, "sweep")
 315  lin_map(s, "b"); s.sw(LDEST, PAINT); s.go(DST_LB | D8, linear=True, bytemask=0x0000ffff); s.check(LDEST, "linb")
 316  s.sw(SCRATCH, LIVE_VAL); s.check(SCRATCH, "live")
 317  t, alive, r = s.run()
 318  for m in (0x0000ffff, 0xfffffffe, 0x7fffffff):
 319      row("mask %08x" % m, kept(r["m%08x" % m]), "paint kept", "S5, LIN_A")
 320  row("mask sweep", kept(r["sweep"]), "paint kept", "S5, all 32 single-zero masks, paint read once at the end")
 321  row("mask lin b", kept(r["linb"]), "paint kept", "S5, LIN_B")
 322  row("mask surv", "survived" if r["live"] == "0x%x" % LIVE_VAL else "died", "survived", "")
 323  row("mask once", ntext(t, "S5") if alive else "died", 1, "thirty-six refusals, one announcement")
 324  
 325  # ================================================================ ACCEPT: what must still land
 326  s = Sess(); tiles(s, a=True)
 327  lin_map(s, "a"); s.sw(LDEST, PAINT); s.go(DST_LA | D8, linear=True, bytemask=0xffffffff); s.check(LDEST, "la")
 328  lin_map(s, "b"); s.sw(LDEST, PAINT); s.go(DST_LB | D8, linear=True, bytemask=0xffffffff); s.check(LDEST, "lb")
 329  lin_map(s, "a"); s.sw(LDEST, PAINT); s.go(ECC | DST_LA | D8, linear=True, bytemask=0xffffffff); s.check(LDEST, "ecc")
 330  s.sw(TDEST, PAINT); s.go(DST_A | D32, bytemask=0x0000ffff); s.check(TDEST, "tmask")
 331  s.sw(TDEST + 4, SRC_WORD); s.sw(TDEST, PAINT); s.go(COPY | DST_A | D32, bytemask=0x0000ffff, src0=SRC_PIX); s.check(TDEST, "tcopy")
 332  t, alive, r = s.run()
 333  row("lin fill a", r["la"], "0x44444444", "ACCEPT: LIN_A, depth 8, full mask -- BG's low byte")
 334  row("lin fill b", r["lb"], "0x44444444", "ACCEPT: LIN_B")
 335  row("lin fill ecc", r["ecc"], "0x44444444", "ACCEPT: the PROM's own linear mode 0x11 (DST_ECC)")
 336  row("tile mask", landed(r["tmask"]), "landed", "ACCEPT: tiled fill with BYTEMASK 0x0000ffff")
 337  row("tile copy mask", top(r["tcopy"]), "0x1a", "ACCEPT: tiled COPY with BYTEMASK 0x0000ffff")
 338  
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
 360  
 361  # ================================================================ AFTER a decline: the engine still works and the status reads idle
 362  s = Sess(); tiles(s, a=True)
 363  s.sw(TDEST, PAINT); s.go(STIPPLE | DST_A | D32); s.check(TDEST, "decl")
 364  s.sw(TDEST, PAINT); s.go(DST_A | D32); s.check(TDEST, "fill")
 365  s.check(DE_STATUS, "stat")
 366  t, alive, r = s.run()
 367  row("after fill", landed(r["fill"]), "landed", "a legal fill after a declined one lands")
 368  row("after status", r["stat"], DE_STAT, "CRIME_DE_STATUS after a decline")
 369  
 370  ok = sum(1 for _, k in rows if k)
 371  print("MTEDECL_RESULT=%d/%d" % (ok, len(rows)))
 372  print("MTEDECL_DONE")
```

## 5. The kill tables

### 5a. `PRETABLE.out` -- written 2026-10-17 16:08:49, before table 1's first log (2026-10-17 16:09:49)

```
PRETABLE -- #564 sgirekills (MTE half), detector regress/sgi_mte_decline_probe.py, md5 8d625289: HEAD 8/53, the fix
53/53, one instrument for both (detector_564_20261017/probe_HEAD_2951694f.out, probe_FIX_564.out).  Its first draft,
md5 ceed62be, compared sign-extended `lw' results against the 32-bit paint and read every kept paint as written;
those runs are preserved as *.v1_signext.out.  This block was
written 2026-10-17 BEFORE kill table 1.  The fix: regress/../src/devices/dev_sgi_re.c md5 1d65cdc1 (HEAD 60203f67).
Mutant list: mutants_564.py beside this file (34 one-edit mutants of the fixed file, each with its predicted catchers).

== 1. SIBLING PARITY (each de-fatalised arm against its nearest sibling)
S1 vs S2: both sit before the destination switch and refuse for every destination; both carry the same three channels
  (survival, paint at a destination the transfer WOULD write, the announce count).  S1 is rowed at tiled A/B/C, tiled A
  COPY, LIN_A, LIN_B; S2 at tiled A fill for every refused src {3,4,5,6,7}, tiled A COPY (src 3), LIN_A (src 3).
  ASYMMETRY, deliberate: S2 is not rowed at tiled B/C -- its predicate reads `src', not the destination, and a
  destination-scoped S2 mutant is caught at LIN_A (`src 3 lin', mutant s2tiled); S1 at tiled B/C exists because the
  witness seats asked for the destination axis at the pre-switch sites.  OWED: none.
S3 vs S4 vs S5: all three sit in the block serving MTE_TLB_LIN_A and MTE_TLB_LIN_B; each is rowed at BOTH labels
  (copy lin a/b; depth a/b x 16/32/64; mask at LIN_A plus `mask lin b').  Parity holds.
The tree's own sibling disposition (`dst_y_step' fatal with the exit commented out; the `default:' dst arm) is NOT
  this round's (rows mtetlbflood, sgimtetlbdefault) and gets no rows.

== 2. CLAIM -> ROW (every ADDED comment sentence asserting an observable consequence)
"The decline returns before any TRANSFER data is written"          -> every `* paint kept' row, and `latch paint'.
"the register store that carried START has already landed ... and stays" -> no row: the MTE register file is not read
  back by any row after a START (a register round-trip WITHOUT START is `mode rt'); disclosed, not claimed.
"the caller's common tail still answers"                           -> `after status' (a read after a decline answers
  0x1e000000) and every `*surv' row (a RAM load after the decline returns its value).
"Each site has its own latch bit"                                  -> `latch texts' (five distinct texts once each).
"the `return' is OUTSIDE the latch, so every refused transfer is refused and only the announcement is once"
                                                                   -> `latch paint' (the repeat of S1), and each site
  session's second and later refusals (stip b/c/..., src 4..7, depth *, mask *).
"Each old message's key phrase is kept in the new one"            -> the HEAD witness re-run post-fix (its attribution
  needles are the old phrases) -- witness_FIX_564.out; no probe row.
"kept as `src > MTE_TLB_C' for fills AND copies"                  -> src 3..7 fill rows, `src 3 copy', `src c fill',
  `src c copy'.
"BYTEMASK is zeroed at init, so a guest that never stores it reaches this decline" -> `mask unwritten'.
The enum's "THE NEXT FREE BIT IS 1 << 18 ..." -> no row: a maintenance claim, not an observable.

== 3. GUARD FIELD vs BODY FIELD, and the partition each body induces
S1  guard reads `mode' (bit 0x400).  Body reads `d->warned' (bit SGIRE_W_MTE_STIPPLE) and `mode' (printed).
    Partition of mode at the guard: {STIPPLE clear, STIPPLE set}.  EXHAUSTED (both cells rowed: every accept row has it
    clear).  `dst_tlb' is NOT read by the guard; it is crossed anyway (tiled A/B/C, COPY, LIN_A/B) because a repair
    scoped by destination is the plausible one-token edit (s1tiled, s1copy).
S2  guard reads `src' = (mode & 0xe0) >> 5, domain {0..7}.  Partition: {0,1,2} accept / {3..7} refuse.  EXHAUSTED on
    the refuse side (3,4,5,6,7 each a row) and at the bound on the accept side (2 = MTE_TLB_C, fill and copy); 0 and 1
    are SAMPLED by every other row (src 0).  Edges per rule D2: 2 (at the bound, accepted) and 3 (one past).
S3  guard reads `mode' bit 0x800 inside the LIN block.  Partition: {COPY clear, set} x labels {LIN_A, LIN_B}.  EXHAUSTED.
S4  guard reads `depth' = 8 << field, domain {8,16,32,64}.  Partition {8} / {16,32,64}, x labels.  EXHAUSTED (all four
    values at LIN_A, all four at LIN_B: 8 via `lin fill b').
S5  guard reads `bytemask' (32 bits).  Partition {0xffffffff} / everything else, x labels.  The refused side is SAMPLED:
    0 (never stored), 0x0000ffff, 0xfffffffe, 0x7fffffff, and all 32 single-zero masks (one row, `mask sweep');
    multi-zero masks beyond those are disclosed (contract).
Latch field `d->warned': a SHARED bitfield.  Who else writes it?  `grep -c "d->warned |=" dev_sgi_re.c' at the fix:
    the 13 pre-existing sites plus the five new ones (MEASURED: HEAD 13, the fix 18); most pre-existing bits are set by ordinary RE register traffic
    (width declines), so the rows that read the latch drive one pre-existing bit (SGIRE_W_TLBA_LEN, by a 4-byte store
    to CRIME_RE_TLB_A) before the new sites and again after them (`latch old bit').

== 4. CHANNEL -- per row, the mutant it is meant to catch and the observable that differs under it
controls  live / devsig / mode rt                -- none (bootstrap); a dead session reds `live'.
stip a, b, c, copy, lin a, lin b                 -- b1 (session dies), d1 (paint written), r1 (b..lin b written: second
                                                    and later refusals), s1copy (copy), s1tiled (lin a/b).  Paint read
                                                    from a destination the transfer writes: tiled tile 0x8002 -> phys
                                                    0x20000; linear page 0x30 mapped in ONLY the array the arm reads.
stip surv                                        -- b1 (the RAM load after six refusals never returns).
stip once                                        -- a missing latch (count 6) or a missing announce (count 0).
src 3..7                                         -- b2, d2 (the tiled fill lands), s2up (3), s2no7 (7), s2copy (all).
src 3 copy                                       -- b2, d2 (the tiled COPY lands the source byte), s2up.
src 3 lin                                        -- d2, s2tiled, s2copy (the linear fill lands 0x44444444).
src c fill / src c copy (ACCEPT)                 -- s2down (the bound value refused: paint kept / 0x99 not 0x1a).
copy lin a / copy lin b                          -- b3, d3 (the linear arm runs as a fill: 0x44444444), s3laba (b only).
depth a/b 16/32/64                               -- b4, d4, s4one (32, 64), s4laba (b *).
mask unwritten                                   -- d5, b5, s5zero (the fill lands with BYTEMASK 0).
mask 0000ffff / fffffffe / 7fffffff / sweep / lin b -- d5, b5, r5 (later refusals), s5low (7fffffff, sweep),
                                                    s5hi (fffffffe, sweep), s5inner (sweep ONLY), s5laba (lin b).
lin fill a / b / ecc (ACCEPT)                    -- s4grow (lin fill b), eccgrow (lin fill ecc): the fill refused, so
                                                    the paint stays where 0x44444444 is wanted.
tile mask / tile copy mask (ACCEPT)              -- s5hoist (a bytemask refusal hoisted out of the linear branch
                                                    refuses the tiled transfers).
latch paint                                      -- r1 (the repeated S1 lands).
latch texts                                      -- shared (S2 silent after S1: 1/0/1/1/1), wrongbit (S5 silent after
                                                    S4), assign (S1 re-announces on the repeat: 2/...).
latch old bit                                    -- assign (`d->warned = X' clears SGIRE_W_TLBA_LEN, so the second
                                                    4-byte store announces again: 2).
after fill / after status                        -- b1 (the session ends at the decline); after fill also catches a
                                                    decline that leaves the engine refusing everything (no mutant
                                                    rowed for that shape -- disclosed).

CHANNEL check, asked by the carrier of the first mandated application: is each row's channel knowable at WRITING
time?  Yes for every row above EXCEPT one, stated before the table: `after status' cannot vary under any mutant in
the list (the status handler is a constant), so it is a CONTROL, not a detector row -- it pins the claim "a guest
polling after a decline is not held", and only a mutant of sgi_de_status (out of scope) could red it.

== 5. CLAUSE (c) -- the null medium
A non-emulator binary (`/bin/true') in place of gxemul: every session dies at once; predicted 0/53 (no row reads a
value from a dead session; the `once' rows require a live session).  MEASURED in this table as `null', not claimed.

== 6. THE (d) DEPENDS-ON enumeration (bounded to the enclosing function, do_mte_transfer)
Predicates dominating the edited lines: S1 (mode & STIPPLE); S2 (src > C); the switch labels LIN_A/LIN_B for S3-S5;
S3 (mode & COPY); S4 (depth != 8); S5 (bytemask != all ones).  Each is weakened in the list: s1copy, s1tiled; s2up,
s2down, s2no7, s2copy, s2tiled; s3laba; s4one, s4laba; s5zero, s5low, s5hi, s5inner, s5laba.  The decline body reads
`d->warned' only, so the operand-swap form is the latch mutants (shared, assign, nolatch, wrongbit).  The repair
itself (`return') is nulled in d1-d5 and moved in r1, r5.
```

### 5b. The mutants: `mutants_564.py` (table 1) and `mutants_564b.py` (table 2), whole

```python
#!/usr/bin/env python3
"""mutants_564.py <fixed dev_sgi_re.c> <out dir> -- write the #564 kill table's one-edit mutants of the FIXED file,
one <name>.c each.  Every edit is anchored on text that must occur EXACTLY ONCE in the fixed file; a missing or
ambiguous anchor is a FAIL (it would otherwise be a mutant that silently equals the fix).  Each entry names the rows
predicted to catch it -- predictions, checked against the table, never copied into a measured column."""
import io, os, sys

S1R = '"0x%08x) -- transfer declined (once) ]\\n", mode);\n\t\t}\n\t\treturn;'
S2R = '"declined (once) ]\\n", src);\n\t\t}\n\t\treturn;'
S3R = '" ]\\n", dst_tlb);\n\t\t\t}\n\t\t\treturn;'
S4R = '"(once) ]\\n", depth, dst_tlb);\n\t\t\t}\n\t\t\treturn;'
S5R = '" ]\\n", (int)bytemask, dst_tlb);\n\t\t\t}\n\t\t\treturn;'
G1 = 'if (mode & MTE_MODE_STIPPLE) {\n\t\tif (!(d->warned & SGIRE_W_MTE_STIPPLE))'
G2 = 'if (src > MTE_TLB_C) {'
G3 = 'if (mode & MTE_MODE_COPY) {\n\t\t\tif (!(d->warned & SGIRE_W_MTE_COPY))'
G4 = 'if (depth != 8) {'
G5 = 'if (bytemask != 0xffffffff) {'
DSTX = '((mode & MTE_MODE_DST_BUF_MASK) >> MTE_DST_TLB_SHIFT)'     # dst_tlb is declared AFTER S1

def sub(a, b):
    return [(a, b)]
def ret_to_exit(anchor):
    return sub(anchor, anchor.replace("return;", "exit(1);"))
def drop_ret(anchor, ind):
    return sub(anchor, anchor[:anchor.rindex("\n" + ind + "return;")])
def ret_inside(anchor, ind):
    inner = anchor[:anchor.rindex("\n" + ind[:-1] + "}")]       # up to the latch block's closing brace
    return sub(anchor, inner + "\n" + ind + "return;\n" + ind[:-1] + "}")

M = [
    # ---- floor clause (b): the terminating call put back, per site
    ("b1", ret_to_exit(S1R), "stip *"), ("b2", ret_to_exit(S2R), "src *"), ("b3", ret_to_exit(S3R), "copy *"),
    ("b4", ret_to_exit(S4R), "depth *"), ("b5", ret_to_exit(S5R), "mask *"),
    # ---- clause (d): the guard kept, the decline nulled -- announce and continue
    ("d1", drop_ret(S1R, "\t\t"), "stip a/b/c/copy/lin"), ("d2", drop_ret(S2R, "\t\t"), "src 3-7 (tiled fill lands), src 3 lin"),
    ("d3", drop_ret(S3R, "\t\t\t"), "copy lin a/b"), ("d4", drop_ret(S4R, "\t\t\t"), "depth a/b *"),
    ("d5", drop_ret(S5R, "\t\t\t"), "mask * incl. unwritten"),
    # ---- the return moved INSIDE the latch: the first refusal declines, the rest proceed
    ("r1", ret_inside(S1R, "\t\t\t"), "stip b (second refusal), latch paint"),
    ("r5", ret_inside(S5R, "\t\t\t\t"), "mask fffffffe etc. (second and later refusals)"),
    # ---- guards scoped to fewer cells than today's
    ("s1copy", sub(G1, G1.replace("(mode & MTE_MODE_STIPPLE)", "((mode & MTE_MODE_STIPPLE) && !(mode & MTE_MODE_COPY))")), "stip copy"),
    ("s1tiled", sub(G1, G1.replace("(mode & MTE_MODE_STIPPLE)", "((mode & MTE_MODE_STIPPLE) && %s <= MTE_TLB_C)" % DSTX)), "stip lin a/b"),
    ("s2up", sub(G2, "if (src > MTE_TLB_C + 1) {"), "src 3, src 3 copy, src 3 lin, latch texts"),
    ("s2down", sub(G2, "if (src >= MTE_TLB_C) {"), "src c fill, src c copy (ACCEPT)"),
    ("s2no7", sub(G2, "if (src > MTE_TLB_C && src != 7) {"), "src 7"),
    ("s2copy", sub(G2, "if (src > MTE_TLB_C && (mode & MTE_MODE_COPY)) {"), "src 3-7, src 3 lin"),
    ("s2tiled", sub(G2, "if (src > MTE_TLB_C && dst_tlb <= MTE_TLB_C) {"), "src 3 lin"),
    ("s3laba", sub(G3, G3.replace("(mode & MTE_MODE_COPY)", "((mode & MTE_MODE_COPY) && dst_tlb == MTE_TLB_LIN_A)")), "copy lin b"),
    ("s4one", sub(G4, "if (depth == 16) {"), "depth a/b 32, 64"),
    ("s4laba", sub(G4, "if (depth != 8 && dst_tlb == MTE_TLB_LIN_A) {"), "depth b *"),
    ("s5zero", sub(G5, "if (bytemask != 0xffffffff && bytemask != 0) {"), "mask unwritten"),
    ("s5low", sub(G5, "if ((bytemask & 0xffff) != 0xffff) {"), "mask 7fffffff, mask sweep"),
    ("s5hi", sub(G5, "if ((bytemask >> 16) != 0xffff) {"), "mask fffffffe, mask sweep"),
    ("s5inner", sub(G5, "if ((bytemask | 0x00ff0000) != 0xffffffff) {"), "mask sweep ONLY"),
    ("s5laba", sub(G5, "if (bytemask != 0xffffffff && dst_tlb == MTE_TLB_LIN_A) {"), "mask lin b"),
    # ---- the ACCEPT side: guards grown to refuse legal transfers
    ("eccgrow", sub(G5, "if (bytemask != 0xffffffff || (mode & MTE_MODE_DST_ECC)) {"), "lin fill ecc"),
    ("s4grow", sub(G4, "if (depth != 8 || dst_tlb == MTE_TLB_LIN_B) {"), "lin fill b"),
    ("s5hoist", sub("\tswitch (dst_tlb) {\n\tcase MTE_TLB_A:", "\tif (bytemask != 0xffffffff)\n\t\treturn;\n\tswitch (dst_tlb) {\n\tcase MTE_TLB_A:"),
     "tile mask, tile copy mask"),
    # ---- the latch
    ("shared", sub("SGIRE_W_MTE_SRC      = 1 << 14,", "SGIRE_W_MTE_SRC      = 1 << 13,"), "latch texts (S2 silenced by S1)"),
    ("assign", sub("d->warned |= SGIRE_W_MTE_COPY;", "d->warned = SGIRE_W_MTE_COPY;"), "latch old bit, latch texts"),
    ("nolatch", sub("if (!(d->warned & SGIRE_W_MTE_DEPTH)) {", "if (1) {"), "depth once"),
    ("wrongbit", sub("if (!(d->warned & SGIRE_W_MTE_BYTEMASK)) {", "if (!(d->warned & SGIRE_W_MTE_DEPTH)) {"), "mask once, latch texts"),
]

def main():
    src, out = sys.argv[1], sys.argv[2]
    t = io.open(src, encoding="utf-8", newline="").read()
    os.makedirs(out, exist_ok=True)
    names = []
    for name, edits, pred in M:
        m = t
        for a, b in edits:
            n = m.count(a)
            if n != 1:
                print("MUTANT ANCHOR FAIL %s: %d occurrences of %r" % (name, n, a[:70])); sys.exit(9)
            m = m.replace(a, b)
        assert m != t, name
        io.open(os.path.join(out, name + ".c"), "w", encoding="utf-8", newline="").write(m)
        names.append(name)
        print("%-9s predicted: %s" % (name, pred))
    print("mutants written: %d" % len(names))

if __name__ == "__main__":
    main()
```

```python
#!/usr/bin/env python3
"""mutants_564b.py <fixed dev_sgi_re.c> <out dir> -- TABLE 2 of #564's kill table: the two ACCEPT-side growth mutants
table 1 lacked.  Found by deriving, from table 1's raw logs, the rows that NO mutant had turned red: three controls and
`lin fill a'.  The accept-row rule says an accept row is discharged by a MEASURED kill, never by existing; and of the
five de-fatalised predicates, S1 and S3 had no growth mutant at all (S2: s2down, S4: s4grow, S5: eccgrow).
Table 1 (mutants_564.py, KILLTABLE.txt) is left as it ran."""
import io, os, sys

G1 = 'if (mode & MTE_MODE_STIPPLE) {\n\t\tif (!(d->warned & SGIRE_W_MTE_STIPPLE))'
G3 = 'if (mode & MTE_MODE_COPY) {\n\t\t\tif (!(d->warned & SGIRE_W_MTE_COPY))'
M = [
    #  S1's guard grown by the adjacent modelled bit the PROM itself sets (DST_ECC, mode 0x11): the least-observable
    #  growth -- it still reads as "the stipple check".
    ("s1grow", [(G1, G1.replace("(mode & MTE_MODE_STIPPLE)", "(mode & (MTE_MODE_STIPPLE | MTE_MODE_DST_ECC))"))],
     "lin fill ecc"),
    #  S3's guard grown to refuse every LIN_A transfer -- the mirror of table 1's s4grow (LIN_B), and the growth only
    #  `lin fill a' (and `lin fill ecc', also LIN_A) can see.
    ("s3growa", [(G3, G3.replace("(mode & MTE_MODE_COPY)", "((mode & MTE_MODE_COPY) || dst_tlb == MTE_TLB_LIN_A)"))],
     "lin fill a, lin fill ecc"),
]

def main():
    src, out = sys.argv[1], sys.argv[2]
    t = io.open(src, encoding="utf-8", newline="").read()
    os.makedirs(out, exist_ok=True)
    for name, edits, pred in M:
        m = t
        for a, b in edits:
            n = m.count(a)
            if n != 1:
                print("MUTANT ANCHOR FAIL %s: %d occurrences" % (name, n)); sys.exit(9)
            m = m.replace(a, b)
        io.open(os.path.join(out, name + ".c"), "w", encoding="utf-8", newline="").write(m)
        print("%-9s predicted: %s" % (name, pred))
    print("mutants written: %d" % len(M))

if __name__ == "__main__":
    main()
```

### 5c. `KILLTABLE.txt` -- table 1, the TABLED instrument (8d625289), 34 mutants

```
base      53/53
null      0/53
base all-green, null all-red: table valid

b1        40/53 KILLED   caught by: stip a, stip b, stip c, stip copy, stip lin a, stip lin b, stip surv, stip once, latch paint, latch texts, latch old bit, after fill, after status
                         predicted: stip *
b2        39/53 KILLED   caught by: src 3, src 4, src 5, src 6, src 7, src 3 copy, src 3 lin, src c fill, src c copy, src surv, src once, latch paint, latch texts, latch old bit
                         predicted: src *
b3        46/53 KILLED   caught by: copy lin a, copy lin b, copy surv, copy once, latch paint, latch texts, latch old bit
                         predicted: copy *
b4        42/53 KILLED   caught by: depth a 16, depth a 32, depth a 64, depth b 16, depth b 32, depth b 64, depth surv, depth once, latch paint, latch texts, latch old bit
                         predicted: depth *
b5        41/53 KILLED   caught by: mask unwritten, mask unw surv, mask 0000ffff, mask fffffffe, mask 7fffffff, mask sweep, mask lin b, mask surv, mask once, latch paint, latch texts, latch old bit
                         predicted: mask *
d1        46/53 KILLED   caught by: stip a, stip b, stip c, stip copy, stip lin a, stip lin b, latch paint
                         predicted: stip a/b/c/copy/lin
d2        45/53 KILLED   caught by: src 3, src 4, src 5, src 6, src 7, src 3 copy, src 3 lin, latch paint
                         predicted: src 3-7 (tiled fill lands), src 3 lin
d3        50/53 KILLED   caught by: copy lin a, copy lin b, latch paint
                         predicted: copy lin a/b
d4        46/53 KILLED   caught by: depth a 16, depth a 32, depth a 64, depth b 16, depth b 32, depth b 64, latch paint
                         predicted: depth a/b *
d5        46/53 KILLED   caught by: mask unwritten, mask 0000ffff, mask fffffffe, mask 7fffffff, mask sweep, mask lin b, latch paint
                         predicted: mask * incl. unwritten
r1        47/53 KILLED   caught by: stip b, stip c, stip copy, stip lin a, stip lin b, latch paint
                         predicted: stip b (second refusal), latch paint
r5        49/53 KILLED   caught by: mask fffffffe, mask 7fffffff, mask sweep, mask lin b
                         predicted: mask fffffffe etc. (second and later refusals)
s1copy    52/53 KILLED   caught by: stip copy
                         predicted: stip copy
s1tiled   51/53 KILLED   caught by: stip lin a, stip lin b
                         predicted: stip lin a/b
s2up      48/53 KILLED   caught by: src 3, src 3 copy, src 3 lin, latch paint, latch texts
                         predicted: src 3, src 3 copy, src 3 lin, latch texts
s2down    51/53 KILLED   caught by: src c fill, src c copy
                         predicted: src c fill, src c copy (ACCEPT)
s2no7     52/53 KILLED   caught by: src 7
                         predicted: src 7
s2copy    45/53 KILLED   caught by: src 3, src 4, src 5, src 6, src 7, src 3 lin, latch paint, latch texts
                         predicted: src 3-7, src 3 lin
s2tiled   52/53 KILLED   caught by: src 3 lin
                         predicted: src 3 lin
s3laba    52/53 KILLED   caught by: copy lin b
                         predicted: copy lin b
s4one     49/53 KILLED   caught by: depth a 32, depth a 64, depth b 32, depth b 64
                         predicted: depth a/b 32, 64
s4laba    50/53 KILLED   caught by: depth b 16, depth b 32, depth b 64
                         predicted: depth b *
s5zero    52/53 KILLED   caught by: mask unwritten
                         predicted: mask unwritten
s5low     47/53 KILLED   caught by: mask 0000ffff, mask 7fffffff, mask sweep, mask lin b, latch paint, latch texts
                         predicted: mask 7fffffff, mask sweep
s5hi      51/53 KILLED   caught by: mask fffffffe, mask sweep
                         predicted: mask fffffffe, mask sweep
s5inner   52/53 KILLED   caught by: mask sweep
                         predicted: mask sweep ONLY
s5laba    52/53 KILLED   caught by: mask lin b
                         predicted: mask lin b
eccgrow   52/53 KILLED   caught by: lin fill ecc
                         predicted: lin fill ecc
s4grow    52/53 KILLED   caught by: lin fill b
                         predicted: lin fill b
s5hoist   48/53 KILLED   caught by: mask once, tile mask, tile copy mask, latch texts, after fill
                         predicted: tile mask, tile copy mask
shared    52/53 KILLED   caught by: latch texts
                         predicted: latch texts (S2 silenced by S1)
assign    51/53 KILLED   caught by: latch texts, latch old bit
                         predicted: latch old bit, latch texts
nolatch   52/53 KILLED   caught by: depth once
                         predicted: depth once
wrongbit  51/53 KILLED   caught by: mask once, latch texts
                         predicted: mask once, latch texts

KILL TABLE: 34/34 killed
```

### 5d. `KILLTABLE2.txt` -- table 2, the SHIPPED instrument (86caed24): the two accept-side growth mutants table 1 lacked

```
base      53/53
null      0/53
base all-green, null all-red: table valid

s1grow    52/53 KILLED   caught by: lin fill ecc
                         predicted: lin fill ecc
s3growa   50/53 KILLED   caught by: lin fill a, lin fill ecc, latch texts
                         predicted: lin fill a, lin fill ecc

KILL TABLE 2: 2/2 killed
```

### 5e. Per row: how many mutants turned it red (computed from every raw log of both tables)

```
row              table 1   table 2   its catchers when 3 or fewer (table 2 marked *)
live             0         0         -- NONE --
devsig           0         0         -- NONE --
mode rt          0         0         -- NONE --
stip a           2         0         b1, d1
stip b           3         0         b1, d1, r1
stip c           3         0         b1, d1, r1
stip copy        4         0         
stip lin a       4         0         
stip lin b       4         0         
stip surv        1         0         b1
stip once        1         0         b1
src 3            4         0         
src 4            3         0         b2, d2, s2copy
src 5            3         0         b2, d2, s2copy
src 6            3         0         b2, d2, s2copy
src 7            4         0         
src 3 copy       3         0         b2, d2, s2up
src 3 lin        5         0         
src c fill       2         0         b2, s2down
src c copy       2         0         b2, s2down
src surv         1         0         b2
src once         1         0         b2
copy lin a       2         0         b3, d3
copy lin b       3         0         b3, d3, s3laba
copy surv        1         0         b3
copy once        1         0         b3
depth a 16       2         0         b4, d4
depth a 32       3         0         b4, d4, s4one
depth a 64       3         0         b4, d4, s4one
depth b 16       3         0         b4, d4, s4laba
depth b 32       4         0         
depth b 64       4         0         
depth surv       1         0         b4
depth once       2         0         b4, nolatch
mask unwritten   3         0         b5, d5, s5zero
mask unw surv    1         0         b5
mask 0000ffff    3         0         b5, d5, s5low
mask fffffffe    4         0         
mask 7fffffff    4         0         
mask sweep       6         0         
mask lin b       5         0         
mask surv        1         0         b5
mask once        3         0         b5, s5hoist, wrongbit
lin fill a       0         1         *s3growa
lin fill b       1         0         s4grow
lin fill ecc     1         2         eccgrow, *s1grow, *s3growa
tile mask        1         0         s5hoist
tile copy mask   1         0         s5hoist
latch paint      14        0         
latch texts      12        1         
latch old bit    6         0         
after fill       2         0         b1, s5hoist
after status     1         0         b1
rows red under NO mutant of either table (3 of 53): live, devsig, mode rt
rows red ONLY in table 2 (1): lin fill a
```

## 6. The SHIPPED instrument on both builds (md5 86caed24), row by row

```
row              HEAD 2951694f            fix (#564)              
live             0x5a5a5a5a ok            0x5a5a5a5a ok           
devsig           0x1e000000 ok            0x1e000000 ok           
mode rt          0x600 ok                 0x600 ok                
stip a           died FAIL                paint kept ok           
stip b           died FAIL                paint kept ok           
stip c           died FAIL                paint kept ok           
stip copy        died FAIL                paint kept ok           
stip lin a       died FAIL                paint kept ok           
stip lin b       died FAIL                paint kept ok           
stip surv        died FAIL                survived ok             
stip once        died FAIL                1 ok                    
src 3            died FAIL                paint kept ok           
src 4            died FAIL                paint kept ok           
src 5            died FAIL                paint kept ok           
src 6            died FAIL                paint kept ok           
src 7            died FAIL                paint kept ok           
src 3 copy       died FAIL                paint kept ok           
src 3 lin        died FAIL                paint kept ok           
src c fill       died FAIL                landed ok               
src c copy       died FAIL                0x1a ok                 
src surv         died FAIL                survived ok             
src once         died FAIL                1 ok                    
copy lin a       died FAIL                paint kept ok           
copy lin b       died FAIL                paint kept ok           
copy surv        died FAIL                survived ok             
copy once        died FAIL                1 ok                    
depth a 16       died FAIL                paint kept ok           
depth a 32       died FAIL                paint kept ok           
depth a 64       died FAIL                paint kept ok           
depth b 16       died FAIL                paint kept ok           
depth b 32       died FAIL                paint kept ok           
depth b 64       died FAIL                paint kept ok           
depth surv       died FAIL                survived ok             
depth once       died FAIL                1 ok                    
mask unwritten   died FAIL                paint kept ok           
mask unw surv    died FAIL                survived ok             
mask 0000ffff    died FAIL                paint kept ok           
mask fffffffe    died FAIL                paint kept ok           
mask 7fffffff    died FAIL                paint kept ok           
mask sweep       died FAIL                paint kept ok           
mask lin b       died FAIL                paint kept ok           
mask surv        died FAIL                survived ok             
mask once        died FAIL                1 ok                    
lin fill a       0x44444444 ok            0x44444444 ok           
lin fill b       0x44444444 ok            0x44444444 ok           
lin fill ecc     0x44444444 ok            0x44444444 ok           
tile mask        landed ok                landed ok               
tile copy mask   0x1a ok                  0x1a ok                 
latch paint      died FAIL                all kept ok             
latch texts      died FAIL                1/1/1/1/1 ok            
latch old bit    died FAIL                1 ok                    
after fill       died FAIL                landed ok               
after status     died FAIL                0x1e000000 ok           
HEAD MTEDECL_RESULT=8/53    fix MTEDECL_RESULT=53/53    (rows: 53)
```

## 7. Questions

Answer in this order, each with its number.  Facts you checked carry `path:line` or a quoted line.

**Q1 -- PREMISE AUDIT.  Test these; do not ratify them:**
  1. at all five sites the fix returns before any TRANSFER data is written, and the `return` is OUTSIDE the latch;
  2. the five new bits `1 << 13` .. `1 << 17` are distinct and collide with no existing `SGIRE_W_*` bit, and the
     demoted BADCOLOR sentence plus the new "next free bit is 1 << 18" sentence are true;
  3. each new message keeps its old key phrase (the witness attributes on those), and S5's new text gains the
     `[ sgi_mte:` prefix the old one lacked;
  4. the kill table is VALID -- base all green, the null medium all red, every log ends with its sentinel -- and each
     mutant in `mutants_564.py` / `mutants_564b.py` is the edit its name says;
  5. the gate block pins every row by name and both denominators by equality, and each `^<name>  .*ok$` pattern can
     match exactly one probe line (names of at most 14 characters in a 16-column field).

**Q2 -- THE SMALLEST EDIT, AND THE FLOOR QUESTION.**  Against the fixed `do_mte_transfer()` and the latch enum: what is
the smallest edit that brings back a guest-visible defect at one of S1-S5 (the process ending, a write the decline
should prevent, an unbounded or missing announcement) while all 53 rows stay green?  Name the row you expect to stay
green.  And the vacuity floor's clause (d), asked of the shipped composite: does a mutant in the DEPENDS-ON enumeration
(PRETABLE section 6 -- the predicates dominating the edits, walked only to the function boundary, plus the latch) sweep
the detector clean?

**Q3 -- ROW VALIDITY.**  Section 5 lists the rows that NO mutant turned red (three controls, and `lin fill a` in table
1 -- table 2 added the growth mutant for it).  Is any other row's channel unable to vary under the mutant PRETABLE
section 4 names for it?  Is any row a survival oracle at a site where the guarded and the unguarded code both survive?

**Q4 -- RECORDS.**  Every ADDED comment sentence in the diff that asserts an observable consequence: true of the code,
and carried by a row or by an explicit no-row sentence (PRETABLE section 2)?  Any claim in sections 1-2 of this brief
that the inlined material does not support?

If, while verifying a claim, you found something ELSE -- say so.

Format: open with your token, then ONE line `VERDICT: CLOSE / SHIP WITH CHANGES (<n>) / DO NOT SHIP (<one line>)`, then
Q1-Q4.
