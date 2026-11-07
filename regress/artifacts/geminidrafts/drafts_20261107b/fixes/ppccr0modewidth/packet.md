# GXemul hardened fork -- DRAFT A FIX for one filed issue, `ppccr0modewidth` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at lines the coordinator LOCATED from names the row uses (the row cites none) (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `ppccr0modewidth`, state `open`, severity `MED`)

**title:** cpu_ppc.c update_cr0(): the comparison width is chosen from the CPU MODEL width (cpu->cd.ppc.bits) rather than from the current operating mode, so a 64-bit CPU running with SF=0 records 64-bit condition bits

**state_note (head):**

[2026-10-02] RE-GRADED low -> MED by #554 from the Astra review campaign (retro, DISPOSITIONS.md:163-164; the files are under regress/artifacts/astraretro_20260926/ and astraretro_harness_20260926/).

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- use current operating mode instead of CPU model width in update_cr0().

## The code at the cited lines

### `src/cpus/cpu_ppc.c` around line 1799 -- LOCATED BY THE COORDINATOR from the name `update_cr0` the row uses (the row cites no line; check this is the defect's site) (HEAD 8d9df658, lines 1679-1919)

```c
 1679| 			break;
 1680| 		default:rt = (iword >> 21) & 31;
 1681| 			ra = (iword >> 16) & 31;
 1682| 			rb = (iword >> 11) & 31;
 1683| 			rc = iword & 1;
 1684| 			switch (xo) {
 1685| 			case PPC_63_FCMPU:
 1686| 			case PPC_63_FRSP:
 1687| 			case PPC_63_FCTIWZ:
 1688| 			case PPC_63_FNEG:
 1689| 			case PPC_63_FMR:
 1690| 			case PPC_63_FNABS:
 1691| 			case PPC_63_FABS:
 1692| 				switch (xo) {
 1693| 				case PPC_63_FCMPU:	mnem = "fcmpu"; break;
 1694| 				case PPC_63_FCTIWZ:
 1695| 					mnem = power? "fcirz" : "fctiwz"; break;
 1696| 				case PPC_63_FRSP:	mnem = "frsp"; break;
 1697| 				case PPC_63_FNEG:	mnem = "fneg"; break;
 1698| 				case PPC_63_FMR:	mnem = "fmr"; break;
 1699| 				case PPC_63_FNABS:	mnem = "fnabs"; break;
 1700| 				case PPC_63_FABS:	mnem = "fabs"; break;
 1701| 				}
 1702| 				debug("%s%s\t", mnem, rc? "." : "");
 1703| 				switch (xo) {
 1704| 				case PPC_63_FCMPU:
 1705| 					debug("%i,f%i,f%i", rt >> 2, ra, rb);
 1706| 					break;
 1707| 				case PPC_63_FCTIWZ:
 1708| 				case PPC_63_FRSP:
 1709| 				case PPC_63_FNEG:
 1710| 				case PPC_63_FMR:
 1711| 				case PPC_63_FNABS:
 1712| 				case PPC_63_FABS:
 1713| 					debug("f%i,f%i", rt, rb);
 1714| 					break;
 1715| 				default:debug("f%i,f%i,f%i", rt, ra, rb);
 1716| 				}
 1717| 				break;
 1718| 			case PPC_63_MFFS:
 1719| 				debug("mffs%s\tf%i", rc?".":"", rt);
 1720| 				break;
 1721| 			case PPC_63_MTFSF:
 1722| 				ra = (iword >> 17) & 255;	/*  flm  */
 1723| 				debug("mtfsf%s\t0x%02x,f%i", rc?".":"", ra, rb);
 1724| 				break;
 1725| 			default:debug("unimplemented hi6_63, xo = 0x%x", xo);
 1726| 			}
 1727| 		}
 1728| 		break;
 1729| 	default:
 1730| 		/*  TODO  */
 1731| 		debug("unimplemented hi6 = 0x%02x", hi6);
 1732| 	}
 1733| 
 1734| 	debug("\n");
 1735| 	return sizeof(iword);
 1736| }
 1737| 
 1738| 
 1739| /*
 1740|  *  debug_spr_usage():
 1741|  *
 1742|  *  Helper function. To speed up overall development speed of the emulator,
 1743|  *  all SPR accesses are allowed. This function causes unknown/unimplemented
 1744|  *  SPRs to give a warning.
 1745|  */
 1746| static void debug_spr_usage(uint64_t pc, int spr)
 1747| {
 1748| 	static uint32_t spr_used[1024 / sizeof(uint32_t)];
 1749| 	static int initialized = 0;
 1750| 
 1751| 	if (!initialized) {
 1752| 		memset(spr_used, 0, sizeof(spr_used));
 1753| 		initialized = 1;
 1754| 	}
 1755| 
 1756| 	spr &= 1023;
 1757| 	if (spr_used[spr >> 2] & (1 << (spr & 3)))
 1758| 		return;
 1759| 
 1760| 	switch (spr) {
 1761| 	/*  Known/implemented SPRs:  */
 1762| 	case SPR_XER:
 1763| 	case SPR_LR:
 1764| 	case SPR_CTR:
 1765| 	case SPR_DSISR:
 1766| 	case SPR_DAR:
 1767| 	case SPR_DEC:
 1768| 	case SPR_SDR1:
 1769| 	case SPR_SRR0:
 1770| 	case SPR_SRR1:
 1771| 	case SPR_SPRG0:
 1772| 	case SPR_SPRG1:
 1773| 	case SPR_SPRG2:
 1774| 	case SPR_SPRG3:
 1775| 	case SPR_PVR:
 1776| 	case SPR_DMISS:
 1777| 	case SPR_DCMP:
 1778| 	case SPR_HASH1:
 1779| 	case SPR_HASH2:
 1780| 	case SPR_IMISS:
 1781| 	case SPR_ICMP:
 1782| 	case SPR_DBSR:
 1783| 	case SPR_PIR:
 1784| 		break;
 1785| 	default:if ((spr >= SPR_IBAT0U && spr <= SPR_DBAT3L) ||
 1786| 		    (spr >= SPR_IBAT4U && spr <= SPR_DBAT7L)) {	/* #116: extended BATs (7445/7455) */
 1787| 			break;
 1788| 		} else
 1789| 			fatal("[ using UNIMPLEMENTED spr %i (%s), pc = "
 1790| 			    "0x%" PRIx64" ]\n", spr, ppc_spr_names[spr] == NULL?
 1791| 			    "UNKNOWN" : ppc_spr_names[spr], (uint64_t) pc);
 1792| 	}
 1793| 
 1794| 	spr_used[spr >> 2] |= (1 << (spr & 3));
 1795| }
 1796| 
 1797| 
 1798| /*
 1799|  *  update_cr0():
 1800|  *
 1801|  *  Sets the top 4 bits of the CR register.
 1802|  */
 1803| void update_cr0(struct cpu *cpu, uint64_t value)
 1804| {
 1805| 	int c;
 1806| 
 1807| 	if (cpu->cd.ppc.bits == 64) {
 1808| 		if ((int64_t)value < 0)
 1809| 			c = 8;
 1810| 		else if ((int64_t)value > 0)
 1811| 			c = 4;
 1812| 		else
 1813| 			c = 2;
 1814| 	} else {
 1815| 		if ((int32_t)value < 0)
 1816| 			c = 8;
 1817| 		else if ((int32_t)value > 0)
 1818| 			c = 4;
 1819| 		else
 1820| 			c = 2;
 1821| 	}
 1822| 
 1823| 	/*  SO bit, copied from XER:  */
 1824| 	c |= ((cpu->cd.ppc.spr[SPR_XER] >> 31) & 1);
 1825| 
 1826| 	cpu->cd.ppc.cr &= ~((uint32_t)0xf << 28);
 1827| 	cpu->cd.ppc.cr |= ((uint32_t)c << 28);
 1828| }
 1829| 
 1830| 
 1831| /*
 1832|  *  update_cr1():  #326
 1833|  *
 1834|  *  Sets CR field 1 from the top four bits of the FPSCR, which is what every
 1835|  *  floating-point instruction with Rc=1 owes: Book I, "For all floating-point
 1836|  *  instructions in which Rc=1, CR Field 1 is a copy of the final state of
 1837|  *  FPSCR FX, FEX, VX, OX". Those are FPSCR bits 0:3, i.e. the register's top
 1838|  *  nibble, and CR field n lives at shift 28-4n -- so field 1 is shift 24. The
 1839|  *  same 28-4*BF convention is visible in the fcmpu translation.
 1840|  *
 1841|  *  This lives here, beside update_cr0, rather than as a static in
 1842|  *  cpu_ppc_instr.c: that file is compiled twice (DYNTRANS_DUALMODE_32), so a
 1843|  *  static helper there would be defined twice in one translation unit.
 1844|  *
 1845|  *  The copy is exact whatever the FPSCR contains. This fork does not model the
 1846|  *  FPU exception state fully, so FX/FEX/VX/OX are mostly zero -- but they are
 1847|  *  not always: frsp's signalling-NaN arm sets FX and VX, so `frsp.` after an
 1848|  *  sNaN reads back nonzero. Where the bits are zero, hardware with no pending
 1849|  *  exception delivers zero too, and a guest reading the same under-populated
 1850|  *  FPSCR through mffs already sees it. No new inaccuracy is introduced here;
 1851|  *  what is removed is a legal instruction halting the emulator.
 1852|  */
 1853| void update_cr1(struct cpu *cpu)
 1854| {
 1855| 	cpu->cd.ppc.cr &= ~((uint32_t)0xf << 24);
 1856| 	cpu->cd.ppc.cr |= ((uint32_t)((cpu->cd.ppc.fpscr >> 28) & 0xf) << 24);
 1857| }
 1858| 
 1859| 
 1860| /*
 1861|  *  ppc_fpscr_recompute():  #327
 1862|  *
 1863|  *  Re-derives the two FPSCR summary bits from the rest of the register.
 1864|  *
 1865|  *  Book I does not describe VX and FEX as storage. VX is "the OR of all the
 1866|  *  Invalid Operation exception bits" and FEX "the OR of all the floating-point
 1867|  *  exception bits masked by their respective enable bits", and no instruction
 1868|  *  may write either one: "mcrfs, mtfsfi, mtfsf, mtfsb0, and mtfsb1 cannot
 1869|  *  alter FPSCR VX / FEX explicitly." This fork stored them, so they went stale
 1870|  *  in BOTH directions, measured:
 1871|  *
 1872|  *      frsp(sNaN)              -> a1001000   FX|VX|VXSNAN, correct
 1873|  *      frsp(sNaN); mtfsb0 7    -> a0001000   cause cleared, VX STILL SET
 1874|  *      mtfsb1 10 (VXZDZ)       -> 80200000   cause set, VX NEVER ROSE
 1875|  *      mtfsb1 7; mtfsb1 24     -> 81000080   VXSNAN+VE, FEX NEVER ROSE
 1876|  *
 1877|  *  "VX set with no cause" is a state hardware cannot produce, and #326 is what
 1878|  *  made it reachable: three of the four instructions that may clear an
 1879|  *  exception bit did not exist before it. Every record form then copied the
 1880|  *  phantom into CR1.
 1881|  *
 1882|  *  FEX pairs the invalid-operation GROUP with the single VE enable -- there is
 1883|  *  no per-cause enable, so `VX & VE` is the whole invalid term. Pairing each
 1884|  *  VXxx bit with VE separately would be the same expression expanded.
 1885|  *
 1886|  *  This deliberately does NOT touch FX. FX is sticky and latches only when an
 1887|  *  exception bit goes 0->1; recomputing it here would re-set it after a guest
 1888|  *  had explicitly cleared it.
 1889|  */
 1890| void ppc_fpscr_recompute(struct cpu *cpu)
 1891| {
 1892| 	uint32_t f = cpu->cd.ppc.fpscr;
 1893| 	int fex = 0;
 1894| 
 1895| 	if (f & PPC_FPSCR_VX_CAUSES)
 1896| 		f |= PPC_FPSCR_VX;
 1897| 	else
 1898| 		f &= ~PPC_FPSCR_VX;
 1899| 
 1900| 	if ((f & PPC_FPSCR_VX) && (f & PPC_FPSCR_VE)) fex = 1;
 1901| 	if ((f & PPC_FPSCR_OX) && (f & PPC_FPSCR_OE)) fex = 1;
 1902| 	if ((f & PPC_FPSCR_UX) && (f & PPC_FPSCR_UE)) fex = 1;
 1903| 	if ((f & PPC_FPSCR_ZX) && (f & PPC_FPSCR_ZE)) fex = 1;
 1904| 	if ((f & PPC_FPSCR_XX) && (f & PPC_FPSCR_XE)) fex = 1;
 1905| 
 1906| 	if (fex)
 1907| 		f |= PPC_FPSCR_FEX;
 1908| 	else
 1909| 		f &= ~PPC_FPSCR_FEX;
 1910| 
 1911| 	cpu->cd.ppc.fpscr = f;
 1912| }
 1913| 
 1914| 
 1915| /*
 1916|  *  ppc_fpscr_raise():  #330
 1917|  *
 1918|  *  Raise one or more FPSCR exception CAUSES, apply the implicit-FX rule, and
 1919|  *  let the summaries follow. Every site that detects an exception goes through
```


RULES FOR THE EDITS: change ONLY text that appears in this packet; use ONLY fields, functions and macros that appear in it
(a draft that calls an undeclared function or a field that does not exist does not compile); make each `old` long enough to
occur exactly once in its file -- include a distinctive neighbouring line when a statement repeats.

## WHAT TO RETURN

1. One line: `STILL PRESENT: YES|NO|UNSETTLED -- <the line of code shown that shows it>`.  The cited line numbers may have
   moved since the row was written; judge from the code shown.  If NO, say what already fixed it and STOP (no edits).
2. If YES: EXACTLY ONE fenced ```json block -- a list of edits, the smallest fix that removes the defect without changing any
   other behaviour: [{"file": "src/...", "old": "<exact text from the code above, without the line-number prefix; it must occur
   EXACTLY ONCE in that file>", "new": "<replacement>", "why": "<one line>"}].  Use JSON escapes (\t, \n).  Tabs stay tabs;
   lines within 79 columns; tag a new comment `/* #NNN: ... */`.  Prefer the file's existing idioms (a decline, a once-per-
   device announce, a clamp) over new machinery.
3. After the block: what the fix deliberately does NOT change, and anything you could not settle from the code shown.

End with one line: `FIXDRAFT_PPCCR0MODEWIDTH: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.

## YOUR PREVIOUS DRAFT FAILED -- correct it

```text
NO EDITS: the draft returned an EMPTY edit list, so nothing was changed.  If the defect is present, write the
executable change; if the code shown cannot settle it -- the lines were LOCATED BY NAME, so they may not be the
defect's site -- say STILL PRESENT: UNSETTLED and name the function or definition you would need to see.
```

The previous edits:

```json
[]
```

Return a CORRECTED complete edit list in the same form, or `STILL PRESENT: UNSETTLED` naming what is missing; end with
the line `FIXDRAFT_PPCCR0MODEWIDTH: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
