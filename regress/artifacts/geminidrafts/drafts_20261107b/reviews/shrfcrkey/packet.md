# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `shrfcrkey` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `shrfcrkey`, state `open`)

**title:** src/devices/dev_sh4.c:2394-2397 -- the RFCR write stores idata & 0x03ff with no write-key test, where the SH7750 manual requires B'101001 in the six most significant bits of a write -- WRONG-RESULT

**state_note (head):** 

**The drafter's own reading:** STILL PRESENT: YES -- 2397

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_sh4.c b/src/devices/dev_sh4.c
index 2316288a..6a975740 100644
--- a/src/devices/dev_sh4.c
+++ b/src/devices/dev_sh4.c
@@ -2393,9 +2393,10 @@ DEVICE_ACCESS(sh4)
 
 	case SH4_RFCR:
 		/*  Refresh Count Register (10 bits):  */
-		if (writeflag == MEM_WRITE)
-			d->bsc_rfcr = idata & 0x03ff;
-		else
+		if (writeflag == MEM_WRITE) {
+			if ((idata >> 10) == 0x29)
+				d->bsc_rfcr = idata & 0x03ff;
+		} else
 			odata = d->bsc_rfcr & 0x03ff;
 		break;
```

## Every edited function, after the fix

### `src/devices/dev_sh4.c` -- post-edit lines 1738-2842 (`+` marks a line the diff added or the point of a deletion)

```c
 1738|  DEVICE_ACCESS(sh4)
 1739|  {
 1740|  	struct sh4_data *d = (struct sh4_data *) extra;
 1741|  	uint64_t idata = 0, odata = 0;
 1742|  	int timer_nr = 0, dma_channel = 0;
     | [... lines 1743-2285 not shown ...]
 2286|  			// Only some bits are writable:
 2287|  			idata &= (DMAOR_DDT | DMAOR_PR1 | DMAOR_PR0 | DMAOR_DME);
 2288|  			cpu->cd.sh.dmaor = idata;
 2289|  		}
 2290|  		break;
 2291|  
 2292|  	/*************************************************/
 2293|  	/*  BSC: Bus State Controller                    */
 2294|  
 2295|  	case SH4_BCR1:
 2296|  		if (writeflag == MEM_WRITE)
 2297|  			d->bsc_bcr1 = idata & 0x033efffd;
 2298|  		else {
 2299|  			odata = d->bsc_bcr1;
 2300|  			if (cpu->byte_order == EMUL_LITTLE_ENDIAN)
 2301|  				odata |= BCR1_LITTLE_ENDIAN;
 2302|  		}
 2303|  		break;
 2304|  
 2305|  	case SH4_BCR2:
 2306|  		if (!sh4_bsc16_report(d, 0, "BCR2", writeflag, len))
 2307|  			break;
 2308|  		if (writeflag == MEM_WRITE)
 2309|  			d->bsc_bcr2 = (idata >> sh4_bsc16_shift(cpu, len))
 2310|  			    & 0x3ffd;
 2311|  		else
 2312|  			odata = (uint64_t) d->bsc_bcr2
 2313|  			    << sh4_bsc16_shift(cpu, len);
 2314|  		break;
 2315|  
 2316|  	case SH4_BCR3:
 2317|  		if (!sh4_bsc16_report(d, 1, "BCR3", writeflag, len))
 2318|  			break;
 2319|  		if (writeflag == MEM_WRITE)
 2320|  			d->bsc_bcr3 = (idata >> sh4_bsc16_shift(cpu, len));
 2321|  		else
 2322|  			odata = (uint64_t) d->bsc_bcr3
 2323|  			    << sh4_bsc16_shift(cpu, len);
 2324|  		break;
 2325|  
 2326|  	case SH4_WCR1:
 2327|  		if (writeflag == MEM_WRITE)
 2328|  			d->bsc_wcr1 = idata & 0x77777777;
 2329|  		else
 2330|  			odata = d->bsc_wcr1;
 2331|  		break;
 2332|  
 2333|  	case SH4_WCR2:
 2334|  		if (writeflag == MEM_WRITE)
 2335|  			d->bsc_wcr2 = idata & 0xfffeefff;
 2336|  		else
 2337|  			odata = d->bsc_wcr2;
 2338|  		break;
 2339|  
 2340|  	case SH4_WCR3:
 2341|  		if (writeflag == MEM_WRITE)
 2342|  			d->bsc_wcr3 = idata & 0x77777777;
 2343|  		else
 2344|  			odata = d->bsc_wcr3;
 2345|  		break;
 2346|  
 2347|  	case SH4_MCR:
 2348|  		if (writeflag == MEM_WRITE)
 2349|  			d->bsc_mcr = idata & 0xf8bbffff;
 2350|  		else
 2351|  			odata = d->bsc_mcr;
 2352|  		break;
 2353|  
 2354|  	case SH4_PCR:
 2355|  		if (writeflag == MEM_WRITE)
 2356|  			d->bsc_pcr = idata;
 2357|  		else
 2358|  			odata = d->bsc_pcr;
 2359|  		break;
 2360|  
 2361|  	case SH4_RTCSR:
 2362|  		/*
 2363|  		 *  Refresh Timer Control/Status Register.
 2364|  		 *
 2365|  		 *  This comment used to ask whether the manual called it
 2366|  		 *  RTSCR while NetBSD called it RTCSR.  ANSWERED 2026-08-22
 2367|  		 *  against a real SH7750 Hardware Manual (Rev.7.00,
 2368|  		 *  REJ09B0366-0700), obtained by owner directive: the manual
 2369|  		 *  says RTCSR 32 times and RTSCR NOT ONCE.  Section 13.2.11
 2370|  		 *  is "Refresh Timer Control/Status Register (RTCSR)".  The
 2371|  		 *  two names never disagreed; the question rested on a false
 2372|  		 *  premise, which is what a question asked without the
 2373|  		 *  document tends to do.
 2374|  		 */
 2375|  		if (writeflag == MEM_WRITE) {
 2376|  			idata &= 0x00ff;
 2377|  			if (idata & RTCSR_CMF) {
 2378|  				idata = (idata & ~RTCSR_CMF)
 2379|  				    | (d->bsc_rtcsr & RTCSR_CMF);
 2380|  			}
 2381|  			d->bsc_rtcsr = idata & 0x00ff;
 2382|  		} else
 2383|  			odata = d->bsc_rtcsr;
 2384|  		break;
 2385|  
 2386|  	case SH4_RTCOR:
 2387|  		/*  Refresh Time Constant Register (8 bits):  */
 2388|  		if (writeflag == MEM_WRITE)
 2389|  			d->bsc_rtcor = idata & 0x00ff;
 2390|  		else
 2391|  			odata = d->bsc_rtcor & 0x00ff;
 2392|  		break;
 2393|  
 2394|  	case SH4_RFCR:
 2395|  		/*  Refresh Count Register (10 bits):  */
 2396|+ 		if (writeflag == MEM_WRITE) {
 2397|+ 			if ((idata >> 10) == 0x29)
 2398|+ 				d->bsc_rfcr = idata & 0x03ff;
 2399|+ 		} else
 2400|  			odata = d->bsc_rfcr & 0x03ff;
 2401|  		break;
 2402|  
 2403|  
 2404|  	/*******************************************/
 2405|  	/*  GPIO:  General-purpose I/O controller  */
 2406|  
 2407|  	case SH4_PCTRA:
 2408|  		if (writeflag == MEM_WRITE) {
 2409|  			d->pctra = idata;
 2410|  			
 2411|  			// Hack: Makes the Dreamcast BIOS pass "cable select"
 2412|  			// detection, it seems, without hanging in an endless
 2413|  			// loop.
 2414|  			d->pdtra |= 0x03;
 2415|  		} else {
 2416|  			odata = d->pctra;
 2417|  		}
 2418|  		break;
 2419|  
 2420|  	case SH4_PDTRA:
 2421|  		if (writeflag == MEM_WRITE) {
 2422|  			// debug("[ sh4: pdtra: write 0x%08x (while pctra = 0x%08x) ]\n", (int)idata, (int)d->pctra);
 2423|  			d->pdtra = idata;
 2424|  
 2425|  			// Hack: Makes the Dreamcast BIOS pass "cable select"
 2426|  			// detection, it seems, without hanging in an endless
 2427|  			// loop.
 2428|  			if ((idata & 1) == 0 || (idata & 2) == 0)
 2429|  				d->pdtra &= ~3;
 2430|  		} else {
 2431|  			// debug("[ sh4: pdtra: read ]\n");
 2432|  			odata = d->pdtra;
 2433|  
 2434|  			// bits 8..9 on Dreamcast mean:
 2435|  			//  00 = VGA, 10 = RGB, 11 = composite.
 2436|  			odata |= (0 << 8);
 2437|  		}
 2438|  		break;
 2439|  
 2440|  	case SH4_PCTRB:
 2441|  		if (writeflag == MEM_WRITE)
 2442|  			d->pctrb = idata;
 2443|  		else
 2444|  			odata = d->pctrb;
 2445|  		break;
 2446|  
 2447|  	case SH4_PDTRB:
 2448|  		if (writeflag == MEM_WRITE) {
 2449|  			debug("[ sh4: pdtrb: write: TODO ]\n");
 2450|  			d->pdtrb = idata;
 2451|  		} else {
 2452|  			debug("[ sh4: pdtrb: read: TODO ]\n");
 2453|  			odata = d->pdtrb;
 2454|  		}
 2455|  		break;
 2456|  
 2457|  	case SH4_GPIOIC:
 2458|  		if (writeflag == MEM_WRITE)
 2459|  			d->bsc_gpioic = idata;
     | [... lines 2460-2812 not shown ...]
 2813|  		else {
 2814|  			d->rtc_rcr2 = idata;
 2815|  			// bit 1 (i.e. idata == 0x02) means reset.
 2816|  			if (idata != 0x02) {
 2817|  				debug("[ SH4: TODO: RTC RCR2 value 0x%02x ignored. ]\n", (int)idata);
 2818|  			}
 2819|  		}
 2820|  		break;
 2821|  
 2822|  
 2823|  	/*************************************************/
 2824|  
 2825|  	default:if (writeflag == MEM_READ) {
 2826|  			fatal("[ sh4: read from addr 0x%x ]\n",
 2827|  			    (int)relative_addr);
 2828|  		} else {
 2829|  			fatal("[ sh4: write to addr 0x%x: 0x%x ]\n",
 2830|  			    (int)relative_addr, (int)idata);
 2831|  		}
 2832|  
 2833|  #ifdef SH4_DEBUG
 2834|  		exit(1);
 2835|  #endif
 2836|  	}
 2837|  
 2838|  	if (writeflag == MEM_READ)
 2839|  		memory_writemax64(cpu, data, len, odata);
 2840|  
 2841|  	return 1;
 2842|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_SHRFCRKEY: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

1. Does the diff remove the defect the issue describes, at every site the issue names?  Name any site it misses.
2. CONTROL FLOW: does any added `return`, `goto`, `break` or early exit skip code the function would otherwise run -- above
   all its COMMON TAIL (for example, code after a switch that writes a read's result to the guest, then `return 1;`)?
   Quote the tail line it skips.  An edit that skips the tail hands the guest an unwritten result.
3. RETURN VALUE: does any path now return something different?  Say what the shown code implies the value means.
4. What ELSE does the diff change -- state left set or cleared, a value the guest can now see, a message on a path that
   did not print one -- beyond removing the defect?
5. House idioms (low severity): a diagnostic a guest can trigger repeatedly should print ONCE per device instance (a latch
   field) with `(once)` in the message; a new comment carries a `/* #NNN: ... */` tag; lines stay within 79 columns.

Each finding: `file:line` in the POST-EDIT numbering shown above, severity DEFECT / QUESTION / STYLE, and the smallest fix
in ONE line.  When the excerpt does not show what a question needs, say UNSETTLED and name what is missing.

End with one line: `FIXREVIEW_SHRFCRKEY: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
