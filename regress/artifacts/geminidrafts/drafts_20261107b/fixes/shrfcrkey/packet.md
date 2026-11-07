# GXemul hardened fork -- DRAFT A FIX for one filed issue, `shrfcrkey` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `shrfcrkey`, state `open`, severity `MED`)

**title:** src/devices/dev_sh4.c:2394-2397 -- the RFCR write stores idata & 0x03ff with no write-key test, where the SH7750 manual requires B'101001 in the six most significant bits of a write -- WRONG-RESULT

**state_note (head):**



**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- require B'101001 in upper 6 bits of idata for RFCR writes

## The code at the cited lines

### `src/devices/dev_sh4.c` around the row's cited line 2394 (HEAD 8d9df658, lines 2274-2514)

```c
 2274| 			cpu->cd.sh.dmac_chcr[dma_channel] = idata;
 2275| 
 2276| 			/*  Perform a transfer?  */
 2277| 			if (idata & CHCR_TD)
 2278| 				sh4_dmac_transfer(cpu, d, dma_channel);
 2279| 		}
 2280| 		break;
 2281| 
 2282| 	case SH4_DMAOR:
 2283| 		if (writeflag == MEM_READ) {
 2284| 			odata = cpu->cd.sh.dmaor;
 2285| 		} else {
 2286| 			// Only some bits are writable:
 2287| 			idata &= (DMAOR_DDT | DMAOR_PR1 | DMAOR_PR0 | DMAOR_DME);
 2288| 			cpu->cd.sh.dmaor = idata;
 2289| 		}
 2290| 		break;
 2291| 
 2292| 	/*************************************************/
 2293| 	/*  BSC: Bus State Controller                    */
 2294| 
 2295| 	case SH4_BCR1:
 2296| 		if (writeflag == MEM_WRITE)
 2297| 			d->bsc_bcr1 = idata & 0x033efffd;
 2298| 		else {
 2299| 			odata = d->bsc_bcr1;
 2300| 			if (cpu->byte_order == EMUL_LITTLE_ENDIAN)
 2301| 				odata |= BCR1_LITTLE_ENDIAN;
 2302| 		}
 2303| 		break;
 2304| 
 2305| 	case SH4_BCR2:
 2306| 		if (!sh4_bsc16_report(d, 0, "BCR2", writeflag, len))
 2307| 			break;
 2308| 		if (writeflag == MEM_WRITE)
 2309| 			d->bsc_bcr2 = (idata >> sh4_bsc16_shift(cpu, len))
 2310| 			    & 0x3ffd;
 2311| 		else
 2312| 			odata = (uint64_t) d->bsc_bcr2
 2313| 			    << sh4_bsc16_shift(cpu, len);
 2314| 		break;
 2315| 
 2316| 	case SH4_BCR3:
 2317| 		if (!sh4_bsc16_report(d, 1, "BCR3", writeflag, len))
 2318| 			break;
 2319| 		if (writeflag == MEM_WRITE)
 2320| 			d->bsc_bcr3 = (idata >> sh4_bsc16_shift(cpu, len));
 2321| 		else
 2322| 			odata = (uint64_t) d->bsc_bcr3
 2323| 			    << sh4_bsc16_shift(cpu, len);
 2324| 		break;
 2325| 
 2326| 	case SH4_WCR1:
 2327| 		if (writeflag == MEM_WRITE)
 2328| 			d->bsc_wcr1 = idata & 0x77777777;
 2329| 		else
 2330| 			odata = d->bsc_wcr1;
 2331| 		break;
 2332| 
 2333| 	case SH4_WCR2:
 2334| 		if (writeflag == MEM_WRITE)
 2335| 			d->bsc_wcr2 = idata & 0xfffeefff;
 2336| 		else
 2337| 			odata = d->bsc_wcr2;
 2338| 		break;
 2339| 
 2340| 	case SH4_WCR3:
 2341| 		if (writeflag == MEM_WRITE)
 2342| 			d->bsc_wcr3 = idata & 0x77777777;
 2343| 		else
 2344| 			odata = d->bsc_wcr3;
 2345| 		break;
 2346| 
 2347| 	case SH4_MCR:
 2348| 		if (writeflag == MEM_WRITE)
 2349| 			d->bsc_mcr = idata & 0xf8bbffff;
 2350| 		else
 2351| 			odata = d->bsc_mcr;
 2352| 		break;
 2353| 
 2354| 	case SH4_PCR:
 2355| 		if (writeflag == MEM_WRITE)
 2356| 			d->bsc_pcr = idata;
 2357| 		else
 2358| 			odata = d->bsc_pcr;
 2359| 		break;
 2360| 
 2361| 	case SH4_RTCSR:
 2362| 		/*
 2363| 		 *  Refresh Timer Control/Status Register.
 2364| 		 *
 2365| 		 *  This comment used to ask whether the manual called it
 2366| 		 *  RTSCR while NetBSD called it RTCSR.  ANSWERED 2026-08-22
 2367| 		 *  against a real SH7750 Hardware Manual (Rev.7.00,
 2368| 		 *  REJ09B0366-0700), obtained by owner directive: the manual
 2369| 		 *  says RTCSR 32 times and RTSCR NOT ONCE.  Section 13.2.11
 2370| 		 *  is "Refresh Timer Control/Status Register (RTCSR)".  The
 2371| 		 *  two names never disagreed; the question rested on a false
 2372| 		 *  premise, which is what a question asked without the
 2373| 		 *  document tends to do.
 2374| 		 */
 2375| 		if (writeflag == MEM_WRITE) {
 2376| 			idata &= 0x00ff;
 2377| 			if (idata & RTCSR_CMF) {
 2378| 				idata = (idata & ~RTCSR_CMF)
 2379| 				    | (d->bsc_rtcsr & RTCSR_CMF);
 2380| 			}
 2381| 			d->bsc_rtcsr = idata & 0x00ff;
 2382| 		} else
 2383| 			odata = d->bsc_rtcsr;
 2384| 		break;
 2385| 
 2386| 	case SH4_RTCOR:
 2387| 		/*  Refresh Time Constant Register (8 bits):  */
 2388| 		if (writeflag == MEM_WRITE)
 2389| 			d->bsc_rtcor = idata & 0x00ff;
 2390| 		else
 2391| 			odata = d->bsc_rtcor & 0x00ff;
 2392| 		break;
 2393| 
 2394| 	case SH4_RFCR:
 2395| 		/*  Refresh Count Register (10 bits):  */
 2396| 		if (writeflag == MEM_WRITE)
 2397| 			d->bsc_rfcr = idata & 0x03ff;
 2398| 		else
 2399| 			odata = d->bsc_rfcr & 0x03ff;
 2400| 		break;
 2401| 
 2402| 
 2403| 	/*******************************************/
 2404| 	/*  GPIO:  General-purpose I/O controller  */
 2405| 
 2406| 	case SH4_PCTRA:
 2407| 		if (writeflag == MEM_WRITE) {
 2408| 			d->pctra = idata;
 2409| 			
 2410| 			// Hack: Makes the Dreamcast BIOS pass "cable select"
 2411| 			// detection, it seems, without hanging in an endless
 2412| 			// loop.
 2413| 			d->pdtra |= 0x03;
 2414| 		} else {
 2415| 			odata = d->pctra;
 2416| 		}
 2417| 		break;
 2418| 
 2419| 	case SH4_PDTRA:
 2420| 		if (writeflag == MEM_WRITE) {
 2421| 			// debug("[ sh4: pdtra: write 0x%08x (while pctra = 0x%08x) ]\n", (int)idata, (int)d->pctra);
 2422| 			d->pdtra = idata;
 2423| 
 2424| 			// Hack: Makes the Dreamcast BIOS pass "cable select"
 2425| 			// detection, it seems, without hanging in an endless
 2426| 			// loop.
 2427| 			if ((idata & 1) == 0 || (idata & 2) == 0)
 2428| 				d->pdtra &= ~3;
 2429| 		} else {
 2430| 			// debug("[ sh4: pdtra: read ]\n");
 2431| 			odata = d->pdtra;
 2432| 
 2433| 			// bits 8..9 on Dreamcast mean:
 2434| 			//  00 = VGA, 10 = RGB, 11 = composite.
 2435| 			odata |= (0 << 8);
 2436| 		}
 2437| 		break;
 2438| 
 2439| 	case SH4_PCTRB:
 2440| 		if (writeflag == MEM_WRITE)
 2441| 			d->pctrb = idata;
 2442| 		else
 2443| 			odata = d->pctrb;
 2444| 		break;
 2445| 
 2446| 	case SH4_PDTRB:
 2447| 		if (writeflag == MEM_WRITE) {
 2448| 			debug("[ sh4: pdtrb: write: TODO ]\n");
 2449| 			d->pdtrb = idata;
 2450| 		} else {
 2451| 			debug("[ sh4: pdtrb: read: TODO ]\n");
 2452| 			odata = d->pdtrb;
 2453| 		}
 2454| 		break;
 2455| 
 2456| 	case SH4_GPIOIC:
 2457| 		if (writeflag == MEM_WRITE)
 2458| 			d->bsc_gpioic = idata;
 2459| 		else
 2460| 			odata = d->bsc_gpioic;
 2461| 		break;
 2462| 
 2463| 
 2464| 	/****************************/
 2465| 	/*  SCI:  Serial Interface  */
 2466| 
 2467| 	case SHREG_SCSPTR:
 2468| 		odata = sh4_sci_access(d, cpu,
 2469| 		    writeflag == MEM_WRITE? 1 : 0, idata);
 2470| 
 2471| 		/*
 2472| 		 *  TODO
 2473| 		 *
 2474| 		 *  Find out the REAL way to make OpenBSD/landisk 4.1 run
 2475| 		 *  in a stable manner! This is a SUPER-UGLY HACK which
 2476| 		 *  just side-steps the real bug.
 2477| 		 *
 2478| 		 *  NOTE:  Snapshots of OpenBSD/landisk _after_ 4.1 seem
 2479| 		 *  to work WITHOUT this hack, but NOT with it!
 2480| 		 */
 2481| 		cpu->invalidate_translation_caches(cpu, 0, INVALIDATE_ALL);
 2482| 
 2483| 		break;
 2484| 
 2485| 
 2486| 	/*********************************/
 2487| 	/*  INTC:  Interrupt Controller  */
 2488| 
 2489| 	case SH4_ICR:
 2490| 		/*
 2491| 		 *  #447: ICR is not modelled on ANY path -- no arm of this case
 2492| 		 *  stores anything, and a read answers the odata this function was
 2493| 		 *  entered with, i.e. 0.  So there is no state to corrupt and none
 2494| 		 *  to restore, and a detector row that writes ICR and reads it back
 2495| 		 *  is VACUOUS here by construction: it answers 0 before the fix,
 2496| 		 *  after it, and under every mutant.  The diagnostic is the only
 2497| 		 *  observable this arm has.
 2498| 		 *
 2499| 		 *  #458: THIS REFUSAL IS WHY cpu_sh.c DECLINES TO READ IPRD.  The two
 2500| 		 *  decisions are one decision, and they sit in different files, so a
 2501| 		 *  future change that accepts IRLM=1 here makes the other one wrong on
 2502| 		 *  the same day -- IPRD would then have to be applied, gated on the live
 2503| 		 *  IRLM bit, with an explicit policy for the IRQ2/5/8/11 aliasing.  See
 2504| 		 *  sh_update_interrupt_priorities().
 2505| 		 */
 2506| 		if (writeflag == MEM_WRITE && (idata & 0x80)) {
 2507| 			if (sh4_val_first(d, SH4_VAL_ICRIRLM, 0,
 2508| 			    (uint32_t) (idata & 0x80)))
 2509| 				fatal("[ sh4: INTC: ICR IRLM bit 0x%04x not"
 2510| 				    " implemented -- write ignored."
 2511| 				    "  (once per bit) ]\n", (int) (idata & 0x80));
 2512| 		}
 2513| 		break;
 2514| 
```

## The data structures those files define (every field that exists)

### `src/devices/dev_sh4.c` -- `struct sh4_data {` (HEAD lines 292-372)

```c
  292| struct sh4_data {
  293| 	/*  Store Queues:  */
  294| 	uint8_t		sq[32 * 2];
  295| 
  296| 	/*  SCIF (Serial controller):  */
  297| 	uint16_t	scif_smr;
  298| 	uint8_t		scif_brr;
  299| 	uint16_t	scif_scr;
  300| 	uint16_t	scif_ssr;
  301| 	uint16_t	scif_fcr;
  302| 	uint16_t	scif_lsr;
  303| 	int		scif_delayed_tx;
  304| 	int		scif_console_handle;
  305| 	uint8_t		scif_tx_fifo[SCIF_TX_FIFO_SIZE + 1];
  306| 	size_t		scif_tx_fifo_cursize;
  307| 	struct interrupt scif_tx_irq;
  308| 	struct interrupt scif_rx_irq;
  309| 	int		scif_tx_irq_asserted;
  310| 	int		scif_rx_irq_asserted;
  311| 
  312| 	/*  Bus State Controller:  */
  313| 	uint32_t	bsc_bcr1;
  314| 	uint16_t	bsc_bcr2;
  315| 	uint16_t	bsc_bcr3;	/*  SH7751R  */
  316| 	/*  #441: has the non-16-bit diagnostic been given for BCR2 / BCR3?
  317| 	    PER SITE, NOT SHARED: a shared flag demotes the second register's
  318| 	    FIRST report, which is #438's "1 of 4 kinds" hazard.  A two-character
  319| 	    mutant ([site] -> [0]) passed a 13-row detector until the oracle was
  320| 	    corrected -- see the comment on sh4_bsc16_report().  */
  321| 	int		bsc16_reported[2];
  322| 	uint32_t	bsc_wcr1;
  323| 	uint32_t	bsc_wcr2;
  324| 	uint32_t	bsc_wcr3;
  325| 	uint32_t	bsc_mcr;
  326| 	uint16_t	bsc_pcr;
  327| 	uint16_t	bsc_rtcsr;
  328| 	uint16_t	bsc_rtcor;
  329| 	uint16_t	bsc_rfcr;
  330| 
  331| 	/*  CPG:  */
  332| 	uint16_t	cpg_frqcr;
  333| 	uint8_t		cpg_stbcr;
  334| 	uint16_t	cpg_wtcnt;
  335| 	uint16_t	cpg_wtcsr;
  336| 	uint8_t		cpg_stbcr2;
  337| 
  338| 	/*  GPIO:  */
  339| 	uint32_t	pctra;		/*  Port Control Register A  */
  340| 	uint32_t	pdtra;		/*  Port Data Register A  */
  341| 	uint32_t	pctrb;		/*  Port Control Register B  */
  342| 	uint32_t	pdtrb;		/*  Port Data Register B  */
  343| 	uint16_t	bsc_gpioic;
  344| 
  345| 	/*  PCIC (PCI controller):  */
  346| 	struct pci_data	*pci_data;
  347| 	struct interrupt cpu_pcic_interrupt[N_PCIC_IRQS];
  348| 	uint32_t	pcic_reg[N_PCIC_REGS];
  349| 	/*  #443: one bit per word offset, so each unsupported transaction is reported
  350| 	    ONCE and a second, DIFFERENT one is not hidden behind the first.  A
  351| 	    per-device flag would hide it (the "1 of 4 kinds" hazard #438 recorded);
  352| 	    137 named flags would be absurd.  This is five words.  */
  353| 	/*  #443 pass 2: [fault class][word].  THREE classes -- UNIMPL, BADVAL and
  354| 	    NOCPU; see sh4_pcic_first().  (This comment said TWO for months, beside
  355| 	    an array dimensioned SH4_PCIC_NCLASS == 3.  A seat reading it for the
  356| 	    gdromdefault round caught the mismatch: the third class was added and
  357| 	    the count in the comment was not.)  */
  358| 	uint32_t	pcic_reported[SH4_PCIC_NCLASS][(N_PCIC_REGS + 31) / 32];
  359| 
  360| 	/*  SCI (serial interface):  */
  361| 	int		sci_bits_outputed;
  362| 	int		sci_bits_read;
  363| 	uint8_t		sci_scsptr;
  364| 	uint8_t		sci_curbyte;
  365| 	uint8_t		sci_cur_addr;
  366| 
  367| 	/*  SD-RAM:  */
  368| 	uint16_t	sdmr2;
  369| 	uint16_t	sdmr3;
  370| 
  371| 	/*  Timer Management Unit:  */
  372| 	struct timer	*sh4_timer;
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

End with one line: `FIXDRAFT_SHRFCRKEY: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
