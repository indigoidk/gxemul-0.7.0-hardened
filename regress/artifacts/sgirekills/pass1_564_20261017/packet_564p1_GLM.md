**Your token: `GLM_MTE564P1_20261017`** -- open your answer with it.

# `#564` sgirekills (MTE half) -- PASS 1 DESIGN BRIEF: five terminating calls in `dev_sgi_re.c`'s `do_mte_transfer()`

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly.  **Check the premises,
not just the derivations.**  Where I state something as fact, ask whether it is true.  A seat that re-derives a
premise from something this brief did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/` AT HEAD `2951694f`.**  There are THREE pristine-2021-upstream copies of
GXemul under the project root (`./src/` and two under `_archive/audit-results-*/builds/`).  They are NOT this fork.  If
your line numbers disagree with mine by hundreds you are reading one of them -- say so rather than reconciling.  The
working tree carries another session's uncommitted edits to OTHER files (`dev_lca.c`, `dev_pcc2.c`, `dev_sh4.c`,
`cpu_alpha_palcode.c`); `dev_sgi_re.c` is clean (md5 `60203f67`, identical to HEAD).

**If you cannot read files that is expected** -- every fact you need is inlined below.  Name any premise you cannot
settle from this packet rather than guessing at it.

**Where this brief states an ARITHMETIC claim -- a field width, a count of reachable values -- ENUMERATE it rather than
reasoning about it.**  And enumerate the right DOMAIN: ask what the producer of a value can actually emit.

**VERDICT LINE FIRST**, so your answer survives truncation.

---

## 1. The round

**Row `sgirekills` (HIGH, open).**  Its first half shipped as `#513` (the RE register read-back arms -- accept / decline,
2026-09-08).  That round's design deliberately EXCLUDED the transfer engine, and what remains of the row is exactly
this: **five guest-reachable terminating calls in `do_mte_transfer()`**, each `fatal(...); exit(1);`.  A sixth
`exit(1)` in the same file sits in `DEVICE_ACCESS(sgi_mte)`'s width chain under `if (len == 4) ... else if (len != 4)
... else { ... }` -- exact complements, so it is unreachable; it is out of scope here and already filed (`sgimtewidth`).

| site | guarding condition (verbatim) | where |
|---|---|---|
| S1 | `if (mode & MTE_MODE_STIPPLE)` | before the destination switch -- any destination |
| S2 | `if (src > MTE_TLB_C)` | before the destination switch -- any destination, fill or copy |
| S3 | `if (mode & MTE_MODE_COPY)` | inside `case MTE_TLB_LIN_A: case MTE_TLB_LIN_B:` only (tiled COPY is implemented) |
| S4 | `if (depth != 8)` | inside the linear cases only |
| S5 | `if (bytemask != 0xffffffff)` | inside the linear cases only, after S3 and S4 |

The census of `exit(` in `dev_sgi_re.c` at HEAD -- comments and string literals stripped, then a whole-word search --
finds six statements, at the five sites above plus the unreachable width arm.  **Check that census against section 3
rather than accepting it.**

## 2. The witness -- MEASURED on the committed build, BEFORE any edit (test-first)

A rung-3 cold-debugger probe on the UNMODIFIED `-E sgi -e ip32` machine: every MTE register is programmed by a REAL
GUEST STORE (`sw`) through real address decode and `memory_rw`, and the transfer is fired the way the device defines
it -- a write whose ADDRESS carries `CRIME_DE_START` (0x800), here `DST1 | START` written last.  One session per site,
because the process ends.  Each site row then performs a RAM store and load AFTER the transfer: `survived` means the
session lived and the later load returned its value.  **The site rows expect the post-fix behaviour, so they are RED
on HEAD.**  The binary is a scratch build of HEAD `2951694f` (`git archive`, configure, make, in WSL
`/tmp/gxsk_2951694f`; `[ gxemul -nt src/devices/dev_sgi_re.c ]` true, its `dev_sgi_re.c` md5 `60203f67` = HEAD's).

Instrument (frozen, for the file-reading seats): `regress/artifacts/sgirekills/witness_20261017/sgi_mte_exit_witness.py`
(md5 `dcbb328d`).  The values each site row writes (MODE field layout from `crmfbreg.h`, section 4):

| row | MODE written | BYTEMASK written | expected HEAD site |
|---|---|---|---|
| `stipple` | `0x600` = depth field 2 (32 bpp), STIPPLE 0x400, dst A, src A | not written | S1 |
| `src tex` | `0x260` = depth 32, src field 3 (`MTE_TLB_TEX`) | not written | S2 |
| `lin copy` | `0x810` = dst field 4 (`LIN_A`), COPY 0x800, depth 8 | `0xffffffff` | S3 |
| `lin depth` | `0x110` = dst LIN_A, depth field 1 (16 bpp) | `0xffffffff` | S4 |
| `bytemask` | `0x010` = dst LIN_A, depth 8 | `0x0000ffff` | S5 |
| `lin fill` (control) | `0x010` | `0xffffffff` | none -- every guarded value legal |

BG is `0x11223344`, DST0 = 0, DST1 = 0 (written with START).

**The run, verbatim** (`regress/artifacts/sgirekills/witness_20261017/witness_HEAD_2951694f.out`):

```
# witness md5 dcbb328d7077d43a14408bd94d57ba83; binary /tmp/gxsk_2951694f/gxemul (HEAD-2951694f); 2026-10-17 15:10:07
# sgirekills MTE exit witness, binary /tmp/gxsk_2951694f/gxemul, label HEAD-2951694f, 2026-10-17 15:10:07
row          got                    want       note                                                       
live         0x5a5a5a5a             0x5a5a5a5a RAM round-trip: the session and the CPU run                ok
devsig       0x1e000000             0x1e000000 CRIME_DE_STATUS: only the device answers this              ok
mode rt      0x600                  0x600      an MTE register through the sgi_mte decode; no START       ok
lin fill     survived               survived   LINEAR arm, every guarded value legal: the path itself lives ok
stipple      died                   survived   own text PRESENT; other sites' texts none                  FAIL
src tex      died                   survived   own text PRESENT; other sites' texts none                  FAIL
lin copy     died                   survived   own text PRESENT; other sites' texts none                  FAIL
lin depth    died                   survived   own text PRESENT; other sites' texts none                  FAIL
bytemask     died                   survived   own text PRESENT; other sites' texts none                  FAIL
MTEEXIT_RESULT=4/9
MTEEXIT_ATTRIBUTED_DEATHS=5/5 (died with ONLY that site's own fatal text)
MTEEXIT_DONE
```

## 3. The code, verbatim from HEAD 2951694f (`src/devices/dev_sgi_re.c`, md5 60203f67), real line numbers

### 3a. `do_mte_transfer()` -- WHOLE, every exit path (the function under edit)

```c
 1458  /****************************************************************************/
 1459  
 1460  /*
 1461   *  SGI "mte", NetBSD sources describes it as a "memory transfer engine".
 1462   *
 1463   *  If the relative address has the 0x0800 (CRIME_DE_START) flag set, it means
 1464   *  "go ahead with the transfer". Otherwise, it is just reads and writes of the
 1465   *  registers.
 1466   */
 1467  
 1468  void do_mte_transfer(struct cpu* cpu, struct sgi_re_data *d)
 1469  {
 1470  	uint32_t mode = d->mte_reg[(CRIME_MTE_MODE - 0x3000) / sizeof(uint32_t)];
 1471  	uint32_t src0 = d->mte_reg[(CRIME_MTE_SRC0 - 0x3000) / sizeof(uint32_t)];
 1472  	uint32_t src1 = d->mte_reg[(CRIME_MTE_SRC1 - 0x3000) / sizeof(uint32_t)];
 1473  	uint32_t dst0 = d->mte_reg[(CRIME_MTE_DST0 - 0x3000) / sizeof(uint32_t)];
 1474  	uint32_t dst1 = d->mte_reg[(CRIME_MTE_DST1 - 0x3000) / sizeof(uint32_t)];
 1475  	int32_t src_y_step = d->mte_reg[(CRIME_MTE_SRC_Y_STEP - 0x3000) / sizeof(uint32_t)];
 1476  	int32_t dst_y_step = d->mte_reg[(CRIME_MTE_DST_Y_STEP - 0x3000) / sizeof(uint32_t)];
 1477  	uint32_t dstlen = dst1 - dst0 + 1, fill_addr;
 1478  	unsigned char zerobuf[4096];
 1479  	int depth = 8 << ((mode & MTE_MODE_DEPTH_MASK) >> MTE_DEPTH_SHIFT);
 1480  	int src = (mode & MTE_MODE_SRC_BUF_MASK) >> MTE_SRC_TLB_SHIFT;
 1481  	uint32_t bytemask = d->mte_reg[(CRIME_MTE_BYTEMASK - 0x3000) / sizeof(uint32_t)];
 1482  	uint32_t bg = d->mte_reg[(CRIME_MTE_BG - 0x3000) / sizeof(uint32_t)];
 1483  
 1484  	debug("[ sgi_mte: STARTING: mode=0x%08x src0=0x%08x src1=0x%08x src_y_step=%i dst0=0x%08x,"
 1485  	    " dst1=0x%08x dst_y_step=%i bg=0x%x bytemask=0x%x ]\n",
 1486  	    mode,
 1487  	    src0, src1, src_y_step,
 1488  	    dst0, dst1, dst_y_step,
 1489  	    bg, bytemask);
 1490  
 1491  	if (dst_y_step != 0 && dst_y_step != 1 && dst_y_step != -1) {
 1492  		fatal("[ sgi_mte: TODO! unimplemented dst_y_step %i ]", dst_y_step);
 1493  		// exit(1);
 1494  	}
 1495  
 1496  	if (mode & MTE_MODE_STIPPLE) {
 1497  		fatal("[ sgi_mte: unimplemented MTE_MODE_STIPPLE ]");
 1498  		exit(1);
 1499  	}
 1500  
 1501  	int src_tlb = (mode & MTE_MODE_SRC_BUF_MASK) >> MTE_SRC_TLB_SHIFT;
 1502  	int dst_tlb = (mode & MTE_MODE_DST_BUF_MASK) >> MTE_DST_TLB_SHIFT;
 1503  	
 1504  	if (src > MTE_TLB_C) {
 1505  		fatal("[ sgi_mte: unimplemented SRC ]");
 1506  		exit(1);
 1507  	}
 1508  
 1509  	switch (dst_tlb) {
 1510  	case MTE_TLB_A:
 1511  	case MTE_TLB_B:
 1512  	case MTE_TLB_C:
 1513  		// Used by NetBSD's crmfb_fill_rect. It puts graphical
 1514  		// coordinates in dst0 and dst1.
 1515  		{
 1516  			int x1 = (dst0 >> 16) & 0xfff;
 1517  			int y1 = dst0 & 0xfff;
 1518  			int x2 = (dst1 >> 16) & 0xfff;
 1519  			int y2 = dst1 & 0xfff;
 1520  			x1 /= (depth / 8);
 1521  			x2 /= (depth / 8);
 1522  
 1523  			int src_x1 = (src0 >> 16) & 0xfff;
 1524  			int src_y1 = src0 & 0xfff;
 1525  			// int src_x2 = (src1 >> 16) & 0xfff;
 1526  			// int src_y2 = src1 & 0xfff;
 1527  			src_x1 /= (depth / 8);
 1528  			// src_x2 /= (depth / 8);
 1529  
 1530  			int dx = x1 > x2 ? -1 : 1;
 1531  			int dy = y1 > y2 ? -1 : 1;
 1532  			
 1533  			uint32_t src_mode = (src_tlb << 10) + (((mode & MTE_MODE_DEPTH_MASK) >> MTE_DEPTH_SHIFT) << 8);
 1534  			uint32_t dst_mode = (dst_tlb << 10) + (((mode & MTE_MODE_DEPTH_MASK) >> MTE_DEPTH_SHIFT) << 8);
 1535  
 1536  			// Hack. The MTE perhaps doesn't deal with colors per se,
 1537  			// but this makes sure that we copy 32 bits when doing 32-bit
 1538  			// transfers.
 1539  			/*  #509: was `depth == 4' -- UNREACHABLE.  `depth' is
 1540  			    a count of BITS (8 << a two-bit field, so 8/16/32/64
 1541  			    only); 4 is the corresponding BYTE count, which the
 1542  			    author used correctly in the `/ (depth / 8)' lines
 1543  			    just above.  So both assignments were dead, every
 1544  			    tiled transfer took the CI arm, and at 32 bits CI
 1545  			    assigns buf[0] alone while memory_rw copies four --
 1546  			    publishing three bytes of host stack into guest
 1547  			    memory.  The comment above states the intended
 1548  			    condition in words: 32-bit transfers.
 1549  
 1550  			    This repairs the 32-bit cell ONLY.  The 16-bit and
 1551  			    reserved-encoding-3 cells assign fewer bytes than
 1552  			    they copy for the same reason and are NOT closed
 1553  			    here -- see the uninitialised-buffer sibling.  */
 1554  			if (depth == 32) {	/*  #509  */
 1555  				src_mode |= DE_MODE_TYPE_RGBA;
 1556  				dst_mode |= DE_MODE_TYPE_RGBA;
 1557  			}
 1558  
 1559  			int src_y = src_y1;
 1560  			for (int y = y1; y != y2+dy; y += dy) {
 1561  				int src_x = src_x1;
 1562  				
 1563  				for  (int x = x1; x != x2+dx; x += dx) {
 1564  					if (mode & MTE_MODE_COPY) {
 1565  						horrible_getputpixel(0, cpu, d,
 1566  							src_x, src_y, &bg, src_mode);
 1567  						src_x += dx;
 1568  					}
 1569  
 1570  					horrible_getputpixel(1, cpu, d, x, y, &bg, dst_mode);
 1571  				}
 1572  				
 1573  				src_y += dy;
 1574  			}
 1575  		}
 1576  		break;
 1577  	case MTE_TLB_LIN_A:
 1578  	case MTE_TLB_LIN_B:
 1579  		// Used by the PROM to zero-fill memory (?).
 1580  		if (mode & MTE_MODE_COPY) {
 1581  			fatal("[ sgi_mte: unimplemented MTE_MODE_COPY ]");
 1582  			exit(1);
 1583  		}
 1584  
 1585  		if (depth != 8) {
 1586  			fatal("[ sgi_mte: unimplemented MTE_DEPTH_x ]");
 1587  			exit(1);
 1588  		}
 1589  
 1590  		debug("[ sgi_mte: LINEAR TRANSFER: mode=0x%08x dst0=0x%016llx,"
 1591  		    " dst1=0x%016llx (length 0x%llx), dst_y_step=%i bg=0x%x, bytemask=0x%x ]\n",
 1592  		    mode,
 1593  		    (long long)dst0, (long long)dst1,
 1594  		    (long long)dstlen, dst_y_step, (int)bg, (int)bytemask);
 1595  
 1596  		if (bytemask != 0xffffffff) {
 1597  			fatal("unimplemented MTE bytemask 0x%08x\n", (int)bytemask);
 1598  			exit(1);
 1599  		}
 1600  
 1601  		/*
 1602  		 *  Horrible hack:
 1603  		 *
 1604  		 *  During bootup, the PROM fills memory at 0x40000000 and
 1605  		 *  forward. This corresponds to the lowest possible RAM address.
 1606  		 *  However, these fills are not going via the CPU's cache,
 1607  		 *  which contains things such as the return address on the
 1608  		 *  stack. If we _really_ write this data in the emulator (which
 1609  		 *  doesn't emulate the cache), it would overwrite the stack.
 1610  		 *
 1611  		 *  So let's not.
 1612  		 *
 1613  		 *  (If some guest OS or firmware variant actually depends on
 1614  		 *  the ability to write to the start of memory this way,
 1615  		 *  it would not work in the emulator.)
 1616  		 */
 1617  		// if (dst0 >= 0x40000000 && dst0 < 0x40004000 && dst1 > 0x40004000) {
 1618  		//	dst0 += 0x4000;
 1619  		//	dstlen -= 0x4000;
 1620  		// }
 1621  
 1622  		/*
 1623  		 *  HUH?
 1624  		 *
 1625  		 *  Note that due to a bug (?) in the PROM firmware when it
 1626  		 *  is setting up the TLB entries, only every _second_ page is
 1627  		 *  actually put correctly in the TLB. This means that even
 1628  		 *  though it then tries to fill 0x40000000 .. 0x40007fff with
 1629  		 *  zeroes, it only fills 0x40001000 .. 0x40001fff,
 1630  		 *  0x40003000 .. 0x40003fff and so on!
 1631  		 *
 1632  		 *  So the Horrible hack above is not needed.
 1633  		 *
 1634  		 *  Ironic.
 1635  		 */
 1636  
 1637  		memset(zerobuf, bg, dstlen < sizeof(zerobuf) ? dstlen : sizeof(zerobuf));
 1638  		fill_addr = dst0;
 1639  		while (dstlen != 0) {
 1640  			uint64_t fill_len;
 1641  			if (dstlen > sizeof(zerobuf))
 1642  				fill_len = sizeof(zerobuf);
 1643  			else
 1644  				fill_len = dstlen;
 1645  
 1646  			uint64_t starting_page = fill_addr & ~0xfff;
 1647  			uint64_t ending_page = (fill_addr + fill_len - 1) & ~0xfff;
 1648  			if (starting_page != ending_page) {
 1649  				fill_len = starting_page + 4096 - fill_addr;
 1650  			}
 1651  
 1652  			// Find starting_page in the TLB in question.
 1653  			starting_page >>= 12;
 1654  			uint32_t *tlb = dst_tlb == MTE_TLB_LIN_A ? d->re_linear_a : d->re_linear_b;
 1655  			int match = 0;
 1656  			for (int i = 0; i < 32; ++i) {
 1657  				uint32_t entry = tlb[i];
 1658  				if (entry & 0x80000000) {
 1659  					entry &= ~0x80000000;
 1660  					if (entry == starting_page) {
 1661  						match = 1;
 1662  						break;
 1663  					}
 1664  				}
 1665  			}
 1666  			
 1667  			if (match) {
 1668  				cpu->memory_rw(cpu, cpu->mem, fill_addr, zerobuf, fill_len,
 1669  					MEM_WRITE, NO_EXCEPTIONS | PHYSICAL);
 1670  			} else {
 1671  				debug("[ sgi_mte: WARNING: address 0x%x not found in TLB? Ignoring fill. ]\n",
 1672  					(long long)fill_addr);
 1673  			}
 1674  
 1675  			fill_addr += fill_len;
 1676  			dstlen -= (uint32_t)fill_len;	/* OB-23: subtract bytes actually filled */
 1677  		}
 1678  		break;
 1679  	default:
 1680  		fatal("[ sgi_mte: TODO! unimplemented dst_tlb 0x%x ]", dst_tlb);
 1681  	}
 1682  }
```

### 3b. `DEVICE_ACCESS(sgi_mte)` -- WHOLE: its only caller, and the common tail a `return` in 3a cannot skip

```c
 1684  DEVICE_ACCESS(sgi_mte)
 1685  {
 1686  	struct sgi_re_data *d = (struct sgi_re_data *) extra;
 1687  	uint64_t idata = 0, odata = 0;
 1688  	int regnr;
 1689  	int startFlag = relative_addr & CRIME_DE_START;
 1690  
 1691  	relative_addr &= ~CRIME_DE_START;
 1692  
 1693  	idata = memory_readmax64(cpu, data, len);
 1694  	regnr = relative_addr / sizeof(uint32_t);
 1695  
 1696  	relative_addr += 0x3000;
 1697  
 1698  	/*
 1699  	 *  Treat all registers as read/write, by default.  Sometimes these
 1700  	 *  are accessed as 32-bit words, sometimes as 64-bit words.
 1701  	 *
 1702  	 *  NOTE: The lowest bits are internally stored in the "low" (+0)
 1703  	 *  register, and the higher bits are stored in the "+1" word.
 1704  	 */
 1705  	if (len == 4) {
 1706  		if (writeflag == MEM_WRITE)
 1707  			d->mte_reg[regnr] = idata;
 1708  		else
 1709  			odata = d->mte_reg[regnr];
 1710  	} else if (len != 4) {
 1711  		if (writeflag == MEM_WRITE) {
 1712  			d->mte_reg[regnr+1] = idata >> 32;
 1713  			d->mte_reg[regnr] = idata;
 1714  		} else {
 1715  			odata = ((uint64_t)d->mte_reg[regnr+1] << 32) +
 1716  			    d->mte_reg[regnr];
 1717  		}
 1718  	} else {
 1719  		fatal("[ sgi_mte: UNIMPLEMENTED read/write len %i ]\n", len);
 1720  		exit(1);
 1721  	}
 1722  
 1723  	switch (relative_addr) {
 1724  
 1725  	case CRIME_MTE_MODE:
 1726  		debug("[ sgi_mte: %s CRIME_MTE_MODE: 0x%016llx ]\n",
 1727  		    writeflag == MEM_WRITE ? "write to" : "read from",
 1728  		    writeflag == MEM_WRITE ? (long long)idata : (long long)odata);
 1729  		break;
 1730  
 1731  	case CRIME_MTE_BYTEMASK:
 1732  		debug("[ sgi_mte: %s CRIME_MTE_BYTEMASK: 0x%016llx ]\n",
 1733  		    writeflag == MEM_WRITE ? "write to" : "read from",
 1734  		    writeflag == MEM_WRITE ? (long long)idata : (long long)odata);
 1735  		break;
 1736  
 1737  	case CRIME_MTE_STIPPLEMASK:
 1738  		fatal("[ sgi_mte: %s CRIME_MTE_STIPPLEMASK: 0x%016llx ]\n",
 1739  		    writeflag == MEM_WRITE ? "write to" : "read from",
 1740  		    writeflag == MEM_WRITE ? (long long)idata : (long long)odata);
 1741  		break;
 1742  
 1743  	case CRIME_MTE_BG:
 1744  		debug("[ sgi_mte: %s CRIME_MTE_BG: 0x%016llx ]\n",
 1745  		    writeflag == MEM_WRITE ? "write to" : "read from",
 1746  		    writeflag == MEM_WRITE ? (long long)idata : (long long)odata);
 1747  		break;
 1748  
 1749  	case CRIME_MTE_SRC0:
 1750  		debug("[ sgi_mte: %s CRIME_MTE_SRC0: 0x%016llx ]\n",
 1751  		    writeflag == MEM_WRITE ? "write to" : "read from",
 1752  		    writeflag == MEM_WRITE ? (long long)idata : (long long)odata);
 1753  		break;
 1754  
 1755  	case CRIME_MTE_SRC1:
 1756  		debug("[ sgi_mte: %s CRIME_MTE_SRC1: 0x%016llx ]\n",
 1757  		    writeflag == MEM_WRITE ? "write to" : "read from",
 1758  		    writeflag == MEM_WRITE ? (long long)idata : (long long)odata);
 1759  		break;
 1760  
 1761  	case CRIME_MTE_DST0:
 1762  		debug("[ sgi_mte: %s CRIME_MTE_DST0: 0x%016llx ]\n",
 1763  		    writeflag == MEM_WRITE ? "write to" : "read from",
 1764  		    writeflag == MEM_WRITE ? (long long)idata : (long long)odata);
 1765  		break;
 1766  
 1767  	case CRIME_MTE_DST1:
 1768  		debug("[ sgi_mte: %s CRIME_MTE_DST1: 0x%016llx ]\n",
 1769  		    writeflag == MEM_WRITE ? "write to" : "read from",
 1770  		    writeflag == MEM_WRITE ? (long long)idata : (long long)odata);
 1771  		break;
 1772  
 1773  	case CRIME_MTE_SRC_Y_STEP:
 1774  		debug("[ sgi_mte: %s CRIME_MTE_SRC_Y_STEP: 0x%016llx ]\n",
 1775  		    writeflag == MEM_WRITE ? "write to" : "read from",
 1776  		    writeflag == MEM_WRITE ? (long long)idata : (long long)odata);
 1777  		break;
 1778  
 1779  	case CRIME_MTE_DST_Y_STEP:
 1780  		debug("[ sgi_mte: %s CRIME_MTE_DST_Y_STEP: 0x%016llx ]\n",
 1781  		    writeflag == MEM_WRITE ? "write to" : "read from",
 1782  		    writeflag == MEM_WRITE ? (long long)idata : (long long)odata);
 1783  		break;
 1784  
 1785  	case CRIME_MTE_NULL:
 1786  		fatal("[ sgi_mte: %s CRIME_MTE_NULL: 0x%016llx ]\n",
 1787  		    writeflag == MEM_WRITE ? "write to" : "read from",
 1788  		    writeflag == MEM_WRITE ? (long long)idata : (long long)odata);
 1789  		break;
 1790  
 1791  	case CRIME_MTE_FLUSH:
 1792  		fatal("[ sgi_mte: %s CRIME_MTE_FLUSH: 0x%016llx ]\n",
 1793  		    writeflag == MEM_WRITE ? "write to" : "read from",
 1794  		    writeflag == MEM_WRITE ? (long long)idata : (long long)odata);
 1795  		break;
 1796  
 1797  	default:
 1798  		if (writeflag == MEM_WRITE)
 1799  			fatal("[ sgi_mte: unimplemented write to "
 1800  			    "address 0x%llx, data=0x%016llx ]\n",
 1801  			    (long long)relative_addr, (long long)idata);
 1802  		else
 1803  			fatal("[ sgi_mte: unimplemented read from address"
 1804  			    " 0x%llx ]\n", (long long)relative_addr);
 1805  	}
 1806  
 1807  	if (startFlag)
 1808  		do_mte_transfer(cpu, d);
 1809  
 1810  	if (writeflag == MEM_READ)
 1811  		memory_writemax64(cpu, data, len, odata);
 1812  
 1813  	return 1;
 1814  }
```

### 3c. `DEVICE_ACCESS(sgi_de_status)` -- the status a guest polls (a constant)

```c
 1833  DEVICE_ACCESS(sgi_de_status)
 1834  {
 1835  	// struct sgi_re_data *d = (struct sgi_re_data *) extra;
 1836  	uint64_t idata = 0, odata = 0;
 1837  
 1838  	idata = memory_readmax64(cpu, data, len);
 1839  
 1840  	relative_addr += 0x4000;
 1841  
 1842  	switch (relative_addr) {
 1843  
 1844  	case CRIME_DE_STATUS:	// 0x4000
 1845  		odata = CRIME_DE_IDLE |
 1846  			CRIME_DE_SETUP_IDLE |
 1847  			CRIME_DE_PIXPIPE_IDLE |
 1848  			CRIME_DE_MTE_IDLE;
 1849  
 1850  		/*
 1851  		 *  TODO: Actually simulate pipeline of a number of commands?
 1852  		 */
 1853  		break;
 1854  
 1855  	case 0x4008:
 1856  		/*  Unknown. Ignore for now.  */
 1857  		break;
 1858  
 1859  	default:
 1860  		if (writeflag == MEM_WRITE)
 1861  			debug("[ sgi_de_status: unimplemented write to "
 1862  			    "address 0x%llx, data=0x%016llx ]\n",
 1863  			    (long long)relative_addr, (long long)idata);
 1864  		else
 1865  			debug("[ sgi_de_status: unimplemented read from address"
 1866  			    " 0x%llx ]\n", (long long)relative_addr);
 1867  	}
 1868  
 1869  	if (writeflag == MEM_READ)
 1870  		memory_writemax64(cpu, data, len, odata);
 1871  
 1872  	return 1;
 1873  }
```

### 3d. The house idiom in this file: the latch enum's head and tail, and one complete latched decline

```c
   58  /*
   59   *  #497: one latch bit per WIDTH-guard site in DEVICE_ACCESS(sgi_re).
   60   *
   61   *  SIX FLAGS, NOT ONE.  dev_wdc.c's own comment adjudicates this: sharing a
   62   *  latch is licensed only across sites that are MUTUALLY EXCLUSIVE at
   63   *  runtime.  These six are six different address windows, and any driver
   64   *  bringing up the rendering engine walks all of them in ONE session, so a
   65   *  shared latch would report the first odd-width access and silence the
   66   *  other five.
   67   */
   68  enum {
   69  	SGIRE_W_TLBA_LEN  = 1 << 0,
   70  	SGIRE_W_TLBB_LEN  = 1 << 1,
   71  	SGIRE_W_TLBC_LEN  = 1 << 2,
   72  	SGIRE_W_TEX_LEN   = 1 << 3,
   73  	SGIRE_W_LINA_LEN  = 1 << 4,
   74  	SGIRE_W_LINB_LEN  = 1 << 5,
   75  
  ...
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
  165  	    THE NEXT FREE BIT IS 1 << 13, AND THIS IS THE LAST ENUMERATOR --
  166  	    which is where that claim belongs, per the convention above.  A
  167  	    maintainer adding a bit BELOW this line must move this sentence
  168  	    with it and demote the copy here.  */
  169  	SGIRE_W_BADCOLOR  = 1 << 12,
  170  };
  ...
  257  	switch (tlb_mode) {
  258  	case 0:	tileptr = d->re_tlb_a[tile_nr] << 16;
  259  		break;
  260  	case 1:	tileptr = d->re_tlb_b[tile_nr] << 16;
  261  		break;
  262  	case 2:	tileptr = d->re_tlb_c[tile_nr] << 16;
  263  		break;
  264  	case 4:	tile_nr = x >> 12;
  265  		if (tile_nr >= 32)
  266  			return;
  267  		tileptr = 0x80000000 | (d->re_linear_a[tile_nr] << 12);
  268  		ofs = x & 4095;
  269  		// TODO... probably not correct!
  270  		// printf("tileptr = %08x x = %i y = %i tile_nr = %i ofs = %i\n", tileptr, x, y, tile_nr, ofs);
  271  		break;
  272  	default:/*  sgirandompixel: this arm used to assign `*color = random()' -- with
  273  		    its exit(1) commented out -- so a failed GET handed the CALLER a
  274  		    random value, and draw_primitive() then wrote it to the destination
  275  		    in the same loop iteration, since `color' is shared by the XFER GET
  276  		    and the PUT.  DE_MODE_LIN_B (0x1400) is one of the FIVE modes
  277  		    crmfbreg.h documents and extracts to tlb_mode 5, so this was
  278  		    reachable with a DOCUMENTED mode, not only with a junk one.
  279  		    MEASURED, rung 3: the destination received 0x4b1763a1, 0x2ee4b4df
  280  		    and 0x7433cdc1 on successive runs of
  281  		    regress/sgi_re_randompixel_probe.py.
  282  
  283  		    NOW DECLINED: `*color' is left alone, so the caller's own
  284  		    `uint32_t color = fg' stands and what lands is at least
  285  		    DETERMINISTIC.  The announce is latched because this helper is
  286  		    per-pixel.
  287  
  288  		    WHAT THIS DOES NOT DO, filed rather than silently omitted: the
  289  		    caller STILL PERFORMS its dependent PUT, so a declined GET still
  290  		    writes fg (row sgirandomskipput -- suppressing it needs a return
  291  		    value and every GET site changed, which is more than one site);
  292  		    LIN_B is still not implemented, and the panel refused to endorse
  293  		    implementing it as LIN_A-with-the-other-array on symmetry alone
  294  		    (row sgirelinb); and the COLOUR-mode switch below carries the same
  295  		    random() shape at its own default (row sgirandomcolour).  */
  296  		if (!(d->warned & SGIRE_W_BADMODE)) {
  297  			d->warned |= SGIRE_W_BADMODE;
  298  			/*  `dst_mode' is kept from the original text although the
  299  			    parameter is also passed as src_mode on a GET: the probe
  300  			    anchors on this literal, and rewording it here would be
  301  			    scope creep AND would move an oracle anchor mid-round,
  302  			    which is the laundering shape whatever the intent.
  303  			    Filed as sgirenamedstmode.  */
  304  			fatal("[ sgi_re: unimplemented dst_mode %i for "
  305  			    "horrible_getputpixel (%s), x=%i y=%i; declined "
  306  			    "(once) ]\n", mode, put ? "put" : "get", x, y);
  307  		}
  308  		return;
  309  	}
```

## 4. The constants (`src/include/thirdparty/crmfbreg.h` at HEAD)

```c
  238  
  239  /* memory transfer engine from 0x3000*/
  240  #define CRIME_MTE_MODE		0x3000
  241  #define CRIME_MTE_BYTEMASK	0x3008
  242  #define CRIME_MTE_STIPPLEMASK	0x3010
  243  #define CRIME_MTE_BG		0x3018
  244  #define CRIME_MTE_SRC0		0x3020	/* start */
  245  #define CRIME_MTE_SRC1		0x3028	/* end */
  246  #define CRIME_MTE_DST0		0x3030	/* start */
  247  #define CRIME_MTE_DST1		0x3038	/* end */
  248  #define CRIME_MTE_SRC_Y_STEP	0x3040
  249  #define CRIME_MTE_DST_Y_STEP	0x3048
  250  #define CRIME_MTE_NULL		0x3070
  251  #define CRIME_MTE_FLUSH		0x3078
  252  
  253  /* CRIME_MTE_MODE */
  254  #define MTE_MODE_DST_ECC	0x00000001	/* enable ECC in DST */
  255  #define MTE_MODE_SRC_ECC	0x00000002	/* enable ECC in SRC */
  256  #define MTE_MODE_DST_BUF_MASK	0x0000001c
  257  	#define MTE_TLB_A	0
  258  	#define MTE_TLB_B	1
  259  	#define MTE_TLB_C	2
  260  	#define MTE_TLB_TEX	3
  261  	#define MTE_TLB_LIN_A	4
  262  	#define MTE_TLB_LIN_B	5
  263  	#define MTE_TLB_CLIP	6
  264  	#define MTE_DST_TLB_SHIFT 2
  265  #define MTE_MODE_SRC_BUF_MASK	0x000000e0
  266  	#define MTE_SRC_TLB_SHIFT 5
  267  #define MTE_MODE_DEPTH_MASK	0x00000300
  268  	#define MTE_DEPTH_8	0
  269  	#define MTE_DEPTH_16	1
  270  	#define MTE_DEPTH_32	2
  271  	#define MTE_DEPTH_SHIFT 8
  272  #define MTE_MODE_STIPPLE	0x00000400
  273  #define MTE_MODE_COPY		0x00000800	/* 1 - copy, 0 - clear dst */
  274  
  275  /* drawing engine from 0x2000 */
  ...
  422  #define CRIME_DE_STATUS		0x4000
  423  #define CRIME_DE_IDLE		0x10000000
  424  #define CRIME_DE_SETUP_IDLE	0x08000000
  425  #define CRIME_DE_PIXPIPE_IDLE	0x04000000
  426  #define CRIME_DE_MTE_IDLE	0x02000000
```

## 5. The file's own idiom and the sibling dispositions (all quoted from HEAD in section 3 or below)

* **The house idiom in this file is a latched decline with a `(once)` marker**, one bit of `uint32_t warned` in
  `struct sgi_re_data` per site.  The enum's last enumerator at HEAD is `SGIRE_W_BADCOLOR = 1 << 12`, and its own
  comment says *"THE NEXT FREE BIT IS 1 << 13, AND THIS IS THE LAST ENUMERATOR"*.  Every entry above it records the
  rule *"a latch shared with any other site is silenced by that site's ordinary traffic"*, so each site gets its OWN
  bit.  A complete example, `horrible_getputpixel()`'s mode decline, is inlined in section 3d.
* **Census of suppression markers, run at brief-writing time against HEAD `2951694f`** (all `src/devices/*.c`, adjacent C
  string literals joined first): 92 markers in 13 spellings -- `(once)` 52, `(once per offset)` 12, `(once per offset
  per direction)` 5, `(further occurrences suppressed)` 5, `(once per bit)` 5, `(once per encoding)` 5, `(reported once)`
  2, and one each of `(once for each channel)`, `(once per direction)`, `(reported once per cpu)`, `(once per channel)`,
  `(reported once per register)`, `(once per timer)`.  (The raw scan printed a fourteenth spelling: one `(once per
  offset per direction)` torn across a COMMENT continuation, which the string-literal join does not repair.)
  `dev_sgi_re.c` carries 14 markers, all `(once)`.
* **The siblings inside `do_mte_transfer()` itself announce and CONTINUE, unlatched:** the `dst_y_step` check is
  `fatal(...); // exit(1);` (the call disabled by a comment), and the `switch (dst_tlb)` `default:` arm is a bare
  `fatal(...)`.  Both are guest-drivable and unlatched; both are FILED as their own rows (`mtetlbflood`,
  `sgimtetlbdefault`, LOW) and are NOT in this round.  The register arms `CRIME_MTE_STIPPLEMASK`, `CRIME_MTE_NULL` and
  `CRIME_MTE_FLUSH` in `DEVICE_ACCESS(sgi_mte)` are unlatched `fatal()`s too.
* **No completion status can hang the guest:** `CRIME_DE_STATUS` returns the constant `CRIME_DE_IDLE |
  CRIME_DE_SETUP_IDLE | CRIME_DE_PIXPIPE_IDLE | CRIME_DE_MTE_IDLE` whatever the transfer did (section 3c).

## 6. PREMISES ALREADY SETTLED, RE-INLINED SO NOBODY SPENDS AN ANSWER RE-DERIVING THEM

* **`fatal()` does not end the process** -- it prints and returns (`src/core/debugmsg.c`); only the `exit(1)` beside it
  terminates.  Settled repeatedly in this campaign; `debug()` has a verbosity early-out, `fatal()` has none.
* **`do_mte_transfer()` is called from exactly one place**: the end of `DEVICE_ACCESS(sgi_mte)`, `if (startFlag)
  do_mte_transfer(cpu, d);`, followed by that handler's common tail (`if (writeflag == MEM_READ)
  memory_writemax64(...); return 1;`) -- section 3b.  `do_mte_transfer()` returns `void` and has NO statements after its
  `switch`, so a `return` inside it skips nothing the caller depends on.
* **`mte_reg[]` is zeroed at device init** (`memset(d, 0, sizeof(struct sgi_re_data))` in `dev_sgi_re_init()`), so
  `BYTEMASK` reads 0 until a guest writes it: a LINEAR fill by a guest that never writes BYTEMASK reaches S5 today.
* **The sixth `exit(1)` is unreachable** (`if (len == 4) ... else if (len != 4) ... else`) -- GPT-6 Astra, 2026-09-09,
  re-derivable from section 3b; filed as `sgimtewidth`.
* **Grok 4.7's 2026-09-07 design answer already classed these five** as *"unimplemented transfer features (member 7 /
  decline-the-transfer, not member 4)"*, separate from the RE read arms by function, trigger, member and detector -- which
  is why `#513` excluded them.  It also noted that the `depth == 4` dead branch (`#509`, row `sgimtedepth4dead`) is on
  the TILED path and that declining linear `depth != 8` does not touch it.

## 7. The disposition -- my leaning, stated as QUESTIONS

The option set has SEVEN members: **1 DELETE** the terminating call only (announce and continue, the `dst_y_step`
shape) / **2 DECLINE silently** / **3 DECLINE + LATCHED ANNOUNCE** / **4 ACCEPT** (the model already computes the right
answer) / **5 FAULT** (model the space as unmapped -- `dev_unreadable.c`) / **6 BACKED ACCEPT** (fabricate storage) /
**7 IMPLEMENT** the feature.  Members 4 and 6 do not fit a TRANSFER (there is no value being read back), and member 5
does not fit an access to a mapped register whose only fault is the parameter it carries -- **say so if you disagree.**

**My leaning: member 3 at all five sites** -- `if (<guard>) { if (!(d->warned & SGIRE_W_MTE_<x>)) { d->warned |=
SGIRE_W_MTE_<x>; fatal("[ sgi_mte: ... -- transfer declined (once) ]\n", ...); } return; }`, five new bits `1 << 13`
.. `1 << 17`, the enum's "last enumerator" sentence moved with them.  The transfer is refused BEFORE any memory write:
S1 and S2 return before the destination switch, S3-S5 return before the fill loop (`memset(zerobuf, ...)` and the
`memory_rw` calls).  **Check each part of that:**

* **Q-a.** Is member 1 (delete only the `exit(1)`, keep going -- the file's own `dst_y_step` precedent) wrong here?
  My reason: at S3-S5 continuing runs the LINEAR fill with the unsupported parameter ignored -- at S4 the fill is
  `memset(zerobuf, bg, ...)`, which repeats only the LOW BYTE of `bg` at 16/32 bpp; at S5 it writes every byte the mask
  says to leave.  That is a silently wrong guest-visible result plus an unlatched message per transfer.  At S1 a
  stippled fill would become a solid fill.  Is "the destination is left untouched" actually better for a guest than
  "the destination is written approximately"?  Neither matches hardware.
* **Q-b. S2 refuses FILLS over a field a fill never reads.**  `src` is read only by S2's guard; `src_tlb` feeds only
  `src_mode`, which is used only under `if (mode & MTE_MODE_COPY)` in the tiled arm, and the linear arm reads no source
  at all (section 3a).  So today `src = 3..7` with COPY CLEAR ends the process for a transfer that would never touch
  the source.  Should S2 be scoped to COPY -- decline only `(mode & MTE_MODE_COPY) && src > MTE_TLB_C`, and let a fill
  with an unused source field proceed?  That would be a NARROWING of a guard, so it needs a warrant, not "cannot hurt":
  is there one (an SGI/NetBSD source, a manual) for what the hardware does with SRC_BUF on a fill?  If there is none,
  is the conservative answer to decline exactly what is refused today?
* **Q-c. Member 7 (implement) at S4 and S5.**  A depth-16/32 linear fill is a pattern-width change to an existing
  loop, and a byte mask is a read-merge-write per page.  The addition licence here requires a measured delta or a
  transferred warrant.  Is there one, or is IMPLEMENT a separate row?
* **Q-d. Latch granularity.**  One bit per SITE (five bits), or one per site AND destination label (S3-S5 sit in a block
  shared by `MTE_TLB_LIN_A` and `MTE_TLB_LIN_B`)?  A per-site bit means a LIN_B transfer is silent after a LIN_A one at
  the same site.
* **Q-e. Decline scope.**  The decline skips every remaining side effect and still answers through the caller's
  common exit (section 6).  Is anything between the top of `do_mte_transfer()` and S1-S5 a side effect that should not
  happen on a declined transfer?  (I see `debug()` calls and the `dst_y_step` `fatal()`; S5 sits after the linear arm's
  `debug(... LINEAR TRANSFER ...)`.)

## 8. The detector I propose (it ships WITH the fix; written before any table runs)

A new probe, `regress/sgi_mte_decline_probe.py`, grown from the witness (same session mechanics), wired into
`regress/gate_arm.sh` beside `sgi_re_width_probe.py` with its row counts pinned by equality.  Rows, each with the
mutant it is meant to catch and the observable that differs (the CHANNEL line):

| row(s) | what it drives | catches | channel |
|---|---|---|---|
| `<site> surv`, five | the witness's transfer | `exit(1)` reinstated (floor clause b) | the process ends |
| `<site> nowrite`, five | the same transfer at a destination the transfer WOULD write, pre-painted (tiled: the `TLBA_TILE` page `sgi_mte_fill_probe.py` uses; linear: a `re_linear_a/b` entry mapping the page) | member 1 -- `exit(1)` deleted, no `return` | the paint is overwritten |
| `<site> once`, five | two transfers in one session | a missing latch, a missing announce, a shared bit | the site's text appears exactly once |
| `lin b <site>`, three (S3-S5 at `MTE_TLB_LIN_B`) | the label the linear block also serves | a repair conditioned on `dst_tlb == MTE_TLB_LIN_A` | survival / paint at LIN_B |
| `src c fill` | a tiled fill with `src` field 2 (`MTE_TLB_C`, the bound) | `src > C` moved down one (`>= C`): the at-the-bound value would be refused | the fill lands |
| `src tex` / `src clip` | `src` 3 (B+1) and 6 | `src > C` moved up one (`> 3`): the first refused value would pass | decline |
| `lin fill`, `lin b fill` | every guarded value legal, at both labels | guard growth at S3-S5 (the de-escalation clause's accept side) | the fill lands |
| `bytemask lo`, `bytemask hi` | `0xfffffffe` and `0x7fffffff` | a narrowed mask compare (`(bytemask & 0xffff) != 0xffff`, `& 0xff...`) | decline vs fill |
| `depth 16/32/64` | fields 1, 2, 3 at LIN_A | `depth != 8` qualified to one value | decline |
| `live`, `devsig`, `mode rt` | as in the witness | -- | controls |

Clause (c), the null medium: an absent or non-emulator binary -- every session dies, so every `surv` and `nowrite` row
reds and the gate's equality pin on rows-green fails; I intend to MEASURE that leg rather than claim it by construction.
Clause (e), the contract, goes in the probe header.  A `PRETABLE.out` is written before table 1.

## 9. Questions

Answer in this order, each with its number.  Facts you checked carry `path:line` or a quoted line.

**Q1 -- PREMISE AUDIT.  These are the premises the design stands on; please test them, not ratify them:**
  1. the census -- six `exit(` statements in `dev_sgi_re.c` at HEAD, five reachable (S1-S5), the sixth unreachable;
  2. each witness row reached ITS OWN site -- the attribution in section 2 is "own fatal text present, the other four
     sites' texts absent".  Is that a sufficient answer to "did it end for the reason under test?"  Could two sites
     share a text, or a row pass an earlier guard it was meant to stop at?
  3. the decline returns before ANY memory write at every site (section 7, the paragraph after the leaning);
  4. Q-b's claim that a FILL never reads the source selector;
  5. the zeroed `BYTEMASK` (a linear fill that never wrote BYTEMASK reaches S5);
  6. no completion status can hang a guest after a declined transfer.

**Q2 -- THE SMALLEST EDIT.**  Against the fix in section 7 and the rows in section 8: what is the smallest edit to
`do_mte_transfer()` that brings back a guest-visible defect at one of S1-S5 (the process ending, a write the decline
should have prevented, a flood) while every proposed row stays green?  Name the row you expect to stay green.

**Q3 -- OPTION-SET COMPLETENESS.**  Is there a disposition this brief did not name?  Grep the fork for how other
transfer or DMA engines refuse an unsupported request (`grep -rn 'declined' src/devices/*.c` is a start) -- the
tree's own precedents are part of the design space.  And is any member I set aside (4, 5, 6) actually right at one
site?

**Q4 -- the round-specific questions Q-a to Q-e in section 7**, one answer each.

**Q5 -- ROUND SCOPE.**  This project's scope rule: a round takes ONE site; a second joins only if it is witnessed, in
the same device and the same semantic class (one fix design covers both), and covered by the same detector with no new
oracle.  Do all five meet that together?  If Q-b's answer is "scope S2 to COPY", is S2 still the same class?

**Q6 -- THE DETECTOR (section 8).**  For each proposed row: can its CHANNEL actually vary under the edit it is meant to
catch?  A row whose observable is the same with and without the defect is vacuous before any table runs.  Which floor
cell is missing -- in particular the destination-label axis (`LIN_A` / `LIN_B` share S3-S5's block, and the linear body
reads `dst_tlb` to pick `re_linear_a` or `re_linear_b`) and the bounds in S2 and S5?

If, while verifying a claim, you found something ELSE -- say so.

Format: open with your token, then ONE line `VERDICT: PROCEED AS PROPOSED / PROCEED WITH CHANGES (<n>) / REDESIGN
(<one line>)`, then Q1-Q6.
