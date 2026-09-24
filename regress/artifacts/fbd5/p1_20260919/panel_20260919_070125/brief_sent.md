# PASS 1 (DESIGN) -- `fbdeclinefive`, round 2 of the footbridge campaign: five register accesses in a direction the datasheet does not define stop ending the process; the #539 kill bridge retires; the durable harness controls land

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated
wrongly, and the previous round of THIS campaign found seven defects in its own pass-1 brief.
**Check the premises, not just the derivations.**  Where I state something as fact, ask
whether it is true.  A seat that re-derives a premise from something this brief did NOT give
it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\src\` at HEAD 9c28ca5 (#539 shipped).**  Copies of
`dev_footbridge.c` that are NOT this fork exist under the project root -- the live hazard is
`_scratchpad/r6pass2_fb/src/devices/dev_footbridge.c` (744 lines, a STALE FORK copy: lines off by tens, the dangerous
kind); the fork's file is 899 lines.  If your line numbers disagree with mine by tens or hundreds, say so rather than
reconciling.  Scope your reading to `GXEMUL-SEC/src/`, `GXEMUL-SEC/regress/*.py` and the named datasheet; do not read
`regress/artifacts/`, `tools/pipeline/ledger.json`, CHANGELOG.md or OUTSTANDING_BUGS.md.  Ordinary engineering
language: these are terminating calls, declines and error paths.

**If you cannot read files that is expected** — every fact you need is inlined.  Name any premise you cannot settle
from this packet rather than guessing at it.

**Where this brief states an ARITHMETIC claim — an offset, a count — ENUMERATE it rather than reasoning about it.**

**VERDICT LINE FIRST**, so your answer survives truncation.

## 1. THE DEFECT, AND WHY THIS ROUND TAKES FIVE SITES AS ONE
`DEVICE_ACCESS(footbridge)` (the DC21285 core-logic device of `-E cats`, at physical `0x42000000`) still ends the
emulator process at SEVEN guest-reachable sites after #539.  FIVE are accesses in a direction the datasheet does not
define for the register: a WRITE to a read-only status register (IRQ_STATUS +0x180, IRQ_RAW_STATUS +0x184, FIQ_STATUS
+0x280, FIQ_RAW_STATUS +0x284) and a READ of a write-only register (IRQ_ENABLE_CLEAR +0x18c).  The other two are READS
of SDRAM_BA_MASK/OFFSET (+0x100/+0x104), documented READ/WRITE registers whose write arms discard the value -- a
different class (a missing value, not an undefined direction) and a SEPARATE round (`fbsdrampair`).  The five are ONE
class under the reopening rule: same device, same semantic class (undefined direction -> the model refuses), same
detector (`regress/footbridge_sites_probe.py`), one fix design.

The datasheet, verbatim (`_scratchpad/dc21285.txt`, Intel 278115-001):
 6820| 
 6821| Table 7-10. Interrupt Controller Registers
 6822| 
 6823| Address                                         Read          Write
 6824| 180h                                            IRQStatus     --
 6825| 184h                                            IRQRawStatus  --
 6826| 188h                                            IRQEnable     IRQEnableSet
 6827| 18Ch                                            --            IRQEnableClear
 6828| 190h                                            --            IRQSoft
 6829| 280h                                            FIQStatus     --
 6830| 284h                                            FIQRawStatus  --
 6831| 288h                                            FIQEnable     FIQEnableSet
 6886| 7.3.29     IRQStatus/FIQStatus Register--Offset 180h/280h
 6887| 
 6888|            This read-only register is a bit-wise AND of RawStatus and IRQEnable/FIQEnable.
 6889| 
 6890|            Dword Bit Name                     R/W Description
 6891| 
 6892|            31:0   IRQStatus/ FIQStatus R      A 1 in a bit position indicates that the associated interrupt
 6893| 
 6894|                                               source is both active and enabled. The nIRQ/nFIQ output
 6895| 
 6896|                                               pin is the NOR of all of the bits in this register.
 6903|         The IRQRawStatus and FIQRawStatus read-only registers always contain identical data.
 6904| 7.3.32
 6905| 7.3.33  Dword Bit  Name                R/W Description
 6906|         31:0
 6907|                    IRQRawStatus/       R    A 1 in a bit position indicates that the associated interrupt
 6908|                    FIQRawStatus
 6909|                                             source is active.
 6936| 
 6937|         IRQEnableClear/FIQEnableClear Register--Offset
 6938|         18Ch/28Ch
 6939| 
 6940|         This write-only register is used to clear bits in the IRQEnable/FIQEnable register.
 6941| 
 6942|         Dword Bit  Name                R/W Description
 6943|         31:0
 6944|                    IRQEnableClear/     WO When writing to this location, each data bit that is high
 6945|                    FIQEnableClear                  causes the corresponding bit in the enable register to be
 6946|                                                    cleared. Data bits that are low have no effect on the
 6947|                                                    corresponding bit in the enable register.
and the CSR access rule:
 1651|        The selected CSR (the CSR with offset equal to SA-110 address A[10:2]) read data is driven onto
 1652|        D[31:0]. If a nonexistent CSR is selected within the CSR address range, zeros are read (no error
 1653|        action is taken). The SA-110 normally stalls for three cycles.

## 2. PREMISES ALREADY SETTLED, RE-INLINED SO NOBODY SPENDS AN ANSWER RE-DERIVING THEM
Settled by #539 (n6): pass 1 `panel_20260919_005103`, pass 2 `panel_20260919_021100`, F2 `panel_20260919_035324`, the
fable5 rulings `_scratchpad/n6/fable5_p1_20260919.md` / `fable5_f2_20260919.md`, the codex M1/M2/K4 readings:
* **#539's kill bridge is TEMPORARY and THIS round retires it** -- fable5 D1: the three probes' "the device can still
  end the process" control is a READ of +0x18c (`ldr r7,[r0,#396]` = 0xE590718C, complaint text `ENABLE CLEAR`, K rows
  require the complaint AND exit 1); the round that declines +0x18c builds the durable harness legs IN THE SAME COMMIT.
* **The durable legs (codex M1's oracle table, adopted by fable5 as the spec):** K1 startup-rejection -- launch with an
  unused `-E` name through each probe's OWN launcher; no prompt; the unknown-emulation diagnostic names that input;
  `WIFEXITED && WEXITSTATUS == 1`.  K2 death-after-execution -- the prologue verified complete and live by a fresh
  `reg` (MMU bit clear, RAM 0x11223344, VENDOR 0x1011, the timer-mask value), then `quit`; the next ordinary interaction
  fails with `dead` BEFORE cleanup; `WEXITSTATUS == 0`.  Every surviving arm reaps exit 0.  There are THREE separately
  implemented launchers (sites' nested helpers; drain's and witness's `Session` classes): the legs go in each.
* **Device reachability is carried by value rows, not by a kill** -- A1 (VENDOR_ID 0x1011), A2 (TIMER_1_LOAD masked
  to 24 bits), and #539's E rows (E1/E2 `|=` accumulation at +0x188).  `quit` exits 0 through normal shutdown
  (`debugger_cmds.c` sets `emul_shutdown`/`exit_debugger`; `main()` returns 0).
* **The teardown as shipped by #539** (all three probes): `quit`, drain the pty to EOF (bounded 20 s; `rd()` returns
  True on a select timeout and False only on EOF/EIO), close, bounded WNOHANG reap (10 s), SIGKILL only if still
  there and not already reaped, `exit`/`signal` on every session-return path, harness kills labelled
  `HARNESS-KILL(9)` / `HARNESS-CLOSE(<sig>)`.
* **+0x18c's decline must ALSO stop returning `d->irq_enable`** (codex M2, K4 D3): today the read branch computes it
  before terminating; a decline that keeps that assignment leaks the enable mask through a write-only address.
* **The VALUE warrant for a declined READ is 0** -- "nonexistent CSR ... zeros are read (no error action is taken)"
  (`:1652`); the diagnostic is emulator POLICY.  For a declined WRITE the datasheet defines no effect; the model must
  leave `irq_status`/`fiq_status`/the enables and the interrupt output UNCHANGED.
* **The house announce idiom** (censused 2026-09-17): a per-instance latch field + `fatal()` whose text carries an
  explicit suppression marker, `(once)` being the majority spelling; `fatal()` cannot be silenced by `-q`, which is why
  a guest-drivable diagnostic needs a latch and not a verbosity flag.  K4 proposed ONE `uint32_t warned_access`
  bit-field (bits 0-4 for these five) rather than five ints -- a proposal, not settled.
* **The default arm** (`default:` in the same switch) prints `[ footbridge: read from 0x%x ]` on every read that
  reaches it and returns 0 -- unlatched, per access, no exit.  Not this round's site; named so a decline is not
  modelled on it by accident.
* **Sub-word accesses**: the handler receives `len` and the unaligned `relative_addr`; word-aligned cases only.  The
  E3/E6 rows measured that a byte/halfword read at an aligned offset returns the low lanes.
* **What `exit_census.py` will count**: dev_footbridge.c carries ten live `exit(1)` at HEAD 9c28ca5 (HEAD lines 565,
  574, 606, 615, 624 -- this round; 714, 739 -- the SDRAM pair; 843 and 879 in DEVINIT, construction-time).

## 3. THE CODE -- the FULL enclosing function at HEAD 9c28ca5, every exit path and the common tail
  498| DEVICE_ACCESS(footbridge)
  499| {
  500| 	struct footbridge_data *d = (struct footbridge_data *) extra;
  501| 	uint64_t idata = 0, odata = 0;
  502| 	int timer_nr = 0;
  503| 
  504| 	if (writeflag == MEM_WRITE)
  505| 		idata = memory_readmax64(cpu, data, len);
  506| 
  507| 	if (relative_addr >= TIMER_1_LOAD && relative_addr <= TIMER_4_CLEAR) {
  508| 		timer_nr = (relative_addr >> 5) & (N_FOOTBRIDGE_TIMERS - 1);
  509| 		relative_addr &= ~0x060;
  510| 	}
  511| 
  512| 	switch (relative_addr) {
  513| 
  514| 	case VENDOR_ID:
  515| 		odata = 0x1011;  /*  DC21285_VENDOR_ID  */
  516| 		break;
  517| 
  518| 	case DEVICE_ID:
  519| 		odata = 0x1065;  /*  DC21285_DEVICE_ID  */
  520| 		break;
  521| 
  522| 	case 0x04:
  523| 	case 0x0c:
  524| 	case 0x10:
  525| 	case 0x14:
  526| 	case 0x18:
  527| 		/*  TODO. Written to by Linux.  */
  528| 		break;
  529| 
  530| 	case REVISION:
  531| 		odata = 3;  /*  footbridge revision number  */
  532| 		break;
  533| 
  534| 	case PCI_ADDRESS_EXTENSION:
  535| 		/*  TODO: Written to by Linux.  */
  536| 		if (writeflag == MEM_WRITE && idata != 0)
  537| 			fatal("[ footbridge: TODO: write to PCI_ADDRESS_"
  538| 			    "EXTENSION: 0x%llx ]\n", (long long)idata);
  539| 		break;
  540| 
  541| 	case SA_CONTROL:
  542| 		/*  Read by Linux:  */
  543| 		odata = PCI_CENTRAL_FUNCTION;
  544| 		break;
  545| 
  546| 	case UART_DATA:
  547| 		if (writeflag == MEM_WRITE)
  548| 			console_putchar(d->console_handle, idata);
  549| 		break;
  550| 
  551| 	case UART_RX_STAT:
  552| 		/*  TODO  */
  553| 		odata = 0;
  554| 		break;
  555| 
  556| 	case UART_FLAGS:
  557| 		odata = UART_TX_EMPTY;
  558| 		break;
  559| 
  560| 	case IRQ_STATUS:
  561| 		if (writeflag == MEM_READ)
  562| 			odata = d->irq_status & d->irq_enable;
  563| 		else {
  564| 			fatal("[ WARNING: footbridge write to irq status? ]\n");
  565| 			exit(1);
  566| 		}
  567| 		break;
  568| 
  569| 	case IRQ_RAW_STATUS:
  570| 		if (writeflag == MEM_READ)
  571| 			odata = d->irq_status;
  572| 		else {
  573| 			fatal("[ footbridge write to irq_raw_status ]\n");
  574| 			exit(1);
  575| 		}
  576| 		break;
  577| 
  578| 	case IRQ_ENABLE_SET:
  579| 		if (writeflag == MEM_WRITE) {
  580| 			d->irq_enable |= idata;
  581| 			if (d->irq_status & d->irq_enable)
  582| 				INTERRUPT_ASSERT(d->irq);
  583| 			else
  584| 				INTERRUPT_DEASSERT(d->irq);
  585| 		} else {
  586| 			/*  #539: a read of 188h is documented -- IRQEnable is
  587| 			    "read-only ... can only be changed by writing to
  588| 			    the EnableSet and EnableClear registers", reset 0
  589| 			    (DC21285 Table 7-10, 7.3.31).  The value below was
  590| 			    always right; the exit(1) that followed it is gone.  */
  591| 			odata = d->irq_enable;
  592| 		}
  593| 		break;
  594| 
  595| 	case IRQ_ENABLE_CLEAR:
  596| 		if (writeflag == MEM_WRITE) {
  597| 			d->irq_enable &= ~idata;
  598| 			if (d->irq_status & d->irq_enable)
  599| 				INTERRUPT_ASSERT(d->irq);
  600| 			else
  601| 				INTERRUPT_DEASSERT(d->irq);
  602| 		} else {
  603| 			odata = d->irq_enable;
  604| 			fatal("[ WARNING: footbridge read from "
  605| 			    "ENABLE CLEAR? ]\n");
  606| 			exit(1);
  607| 		}
  608| 		break;
  609| 
  610| 	case FIQ_STATUS:
  611| 		if (writeflag == MEM_READ)
  612| 			odata = d->fiq_status & d->fiq_enable;
  613| 		else {
  614| 			fatal("[ WARNING: footbridge write to fiq status? ]\n");
  615| 			exit(1);
  616| 		}
  617| 		break;
  618| 
  619| 	case FIQ_RAW_STATUS:
  620| 		if (writeflag == MEM_READ)
  621| 			odata = d->fiq_status;
  622| 		else {
  623| 			fatal("[ footbridge write to fiq_raw_status ]\n");
  624| 			exit(1);
  625| 		}
  626| 		break;
  627| 
  628| 	case FIQ_ENABLE_SET:
  629| 		if (writeflag == MEM_WRITE)
  630| 			d->fiq_enable |= idata;
  631| 		break;
  632| 
  633| 	case FIQ_ENABLE_CLEAR:
  634| 		if (writeflag == MEM_WRITE)
  635| 			d->fiq_enable &= ~idata;
  636| 		break;
  637| 
  638| 	case TIMER_1_LOAD:
  639| 		if (writeflag == MEM_READ)
  640| 			odata = d->timer_load[timer_nr];
  641| 		else {
  642| 			d->timer_load[timer_nr] = idata & TIMER_MAX_VAL;
  643| 			reload_timer_value(cpu, d, timer_nr);
  644| 			/*  debug("[ footbridge: timer %i (1-based), "
  645| 			    "value %i ]\n", timer_nr + 1,
  646| 			    (int)d->timer_value[timer_nr]);  */
  647| 			INTERRUPT_DEASSERT(d->timer_irq[timer_nr]);
  648| 		}
  649| 		break;
  650| 
  651| 	case TIMER_1_VALUE:
  652| 		if (writeflag == MEM_READ)
  653| 			odata = d->timer_value[timer_nr];
  654| 		else
  655| 			d->timer_value[timer_nr] = idata & TIMER_MAX_VAL;
  656| 		break;
  657| 
  658| 	case TIMER_1_CONTROL:
  659| 		if (writeflag == MEM_READ)
  660| 			odata = d->timer_control[timer_nr];
  661| 		else {
  662| 			d->timer_control[timer_nr] = idata;
  663| 			/*  #432: both prescaler bits set is TIMER_EXTERNAL
  664| 			    (0x0C, dc21285reg.h:364) -- a LEGAL named encoding,
  665| 			    and it used to reach fatal()+exit(1) right here, so a
  666| 			    guest selecting the external clock source KILLED THE
  667| 			    HOST.  Arguably likelier than the zero load, since it
  668| 			    is a documented mode rather than a malformed value.
  669| 			    The rate an external clock would actually give is
  670| 			    UNKNOWN and is NOT invented: footbridge_effective_cycles()
  671| 			    now gives the encoding a defined, survivable meaning
  672| 			    (the unprescaled period), and the real semantics are
  673| 			    filed for a round that has a datasheet.  */
  674| 			if (idata & TIMER_ENABLE) {
  675| 				reload_timer_value(cpu, d, timer_nr);
  676| 			} else {
  677| 				d->pending_timer_interrupts[timer_nr] = 0;
  678| 			}
  679| 			INTERRUPT_DEASSERT(d->timer_irq[timer_nr]);
  680| 		}
  681| 		break;
  682| 
  683| 	case TIMER_1_CLEAR:
  684| 		/*  #474: a READ must not perform the clear.  This case carried no
  685| 		    writeflag test at all, while TIMER_1_CONTROL immediately above it
  686| 		    does -- so a guest READ reloaded the counter, decremented the
  687| 		    pending count and DEASSERTED the interrupt.  A guest that merely
  688| 		    read the register silently acknowledged a pending timer interrupt;
  689| 		    the guest-visible consequence is a LOST interrupt, not a bad value.
  690| 
  691| 		    FOUR addresses, not one: the fold above normalises 0x30C/0x32C/
  692| 		    0x34C/0x36C onto this single case.
  693| 
  694| 		    GUARD THE BODY, KEEP THE break.  An early return here would skip
  695| 		    the function's common tail, which writes odata back on a read, and
  696| 		    would hand a guest an untouched buffer -- a defect this code does
  697| 		    not currently have.  */
  698| 		if (writeflag == MEM_WRITE) {
  699| 			if (d->timer_control[timer_nr] & TIMER_MODE_PERIODIC) {
  700| 				reload_timer_value(cpu, d, timer_nr);
  701| 			}
  702| 
  703| 			if (d->pending_timer_interrupts[timer_nr] > 0) {
  704| 				d->pending_timer_interrupts[timer_nr] --;
  705| 			}
  706| 
  707| 			INTERRUPT_DEASSERT(d->timer_irq[timer_nr]);
  708| 		}
  709| 		break;
  710| 
  711| 	case SDRAM_BA_MASK:
  712| 		if (writeflag == MEM_READ) {
  713| 			fatal("[ footbridge read from sdram_ba_mask ]\n");
  714| 			exit(1);
  715| 		} else {
  716| 			switch (idata) {
  717| 			case SDRAM_MASK_256KB:
  718| 			case SDRAM_MASK_512KB:
  719| 			case SDRAM_MASK_1MB:
  720| 			case SDRAM_MASK_2MB:
  721| 			case SDRAM_MASK_4MB:
  722| 			case SDRAM_MASK_8MB:
  723| 			case SDRAM_MASK_16MB:
  724| 			case SDRAM_MASK_32MB:
  725| 			case SDRAM_MASK_64MB:
  726| 			case SDRAM_MASK_128MB:
  727| 			case SDRAM_MASK_256MB:
  728| 				break;
  729| 			default:
  730| 				fatal("[ footbridge write to sdram_ba_mask "
  731| 				    "%#llx ]\n", (long long)idata);
  732| 				break;
  733| 			}
  734| 		}
  735| 		break;
  736| 	case SDRAM_BA_OFFSET:
  737| 		if (writeflag == MEM_READ) {
  738| 			fatal("[ footbridge read from sdram_ba_offset ]\n");
  739| 			exit(1);
  740| 		} else {
  741| 			if (idata != 0)
  742| 				fatal("[ footbridge write to sdram_ba_offset "
  743| 				    "%#llx ]\n", (long long)idata);
  744| 		}
  745| 		break;
  746| 
  747| 	default:if (writeflag == MEM_READ) {
  748| 			fatal("[ footbridge: read from 0x%x ]\n",
  749| 			    (int)relative_addr);
  750| 		} else {
  751| 			fatal("[ footbridge: write to 0x%x: 0x%llx ]\n",
  752| 			    (int)relative_addr, (long long)idata);
  753| 		}
  754| 	}
  755| 
  756| 	if (writeflag == MEM_READ)
  757| 		memory_writemax64(cpu, data, len, odata);
  758| 
  759| 	return 1;
  760| }
  761| 
  762| 

## 4. THE PROPOSED ROUND
**Fix (option-set member 3 for all five, DECLINE + LATCHED ANNOUNCE; member 2 silent decline is the alternative
per site):** each of the five arms stops calling `exit(1)`; the WRITE arms leave every field untouched; the +0x18c
READ arm returns 0 and no longer assigns `odata = d->irq_enable`; each arm announces ONCE per device instance with a
`(once)` marker.  Storage: K4's `uint32_t warned_access` (one bit per site, cleared by DEVINIT's memset) -- or five
`int` latches in the file's existing style; the panel chooses.  Texts (K4, verbatim):
  `[ WARNING: footbridge write to irq status? (once) ]`, `[ footbridge write to irq_raw_status (once) ]`,
  `[ WARNING: footbridge read from ENABLE CLEAR? (once) ]`, `[ WARNING: footbridge write to fiq status? (once) ]`,
  `[ footbridge write to fiq_raw_status (once) ]`.  0/5 share an exact message, so one aggregate boolean would let the
  first site suppress the other four -- one bit each.
**Detector rows (K4's A1-A5 / D1-D5, on `footbridge_sites_probe.py`; the SDRAM rows A6/A7/D6/D7 are NOT this round):**
  A1 IRQ_STATUS read +0x180 -> 0 with enable 0x30 (accept side; catches masked-AND -> OR: 0x30)
  D1 two writes of 0x10 to +0x180: state unchanged, the announce ONCE (catches a store into irq_status: raw/status 0x10)
  A2 IRQ_RAW_STATUS read +0x184 -> 0 (catches `odata = irq_enable`: 0x30)
  D2 two writes of 0x10 to +0x184: unchanged, announce once
  A3 IRQ_ENABLE_CLEAR write 0x10 with enable 0x30 -> enable 0x20; a zero write preserves 0x20 (catches a deleted clear)
  D3 two reads of +0x18c with enable 0x30 -> 0, 0; enables unchanged; announce once (catches the retained
     `odata = d->irq_enable`: 0x30 -- and a clear-on-read)
  A4/D4 FIQ_STATUS +0x280 with fiq enable 0xc0;  A5/D5 FIQ_RAW_STATUS +0x284 likewise
  Each D row's "once" is a COUNT of the announce text across two accesses (0 = silent decline, 2 = unlatched);
  every row also requires the arm to SURVIVE with exit 0 (a remaining terminating path shows as a missing continuation).
**The kill bridge retires and the harness legs land in the same commit:** arm K's +0x18c read (sites), the drain's and
the witness's K arms are REPLACED by the K1/K2 legs above (through each probe's own launcher), and `gate_arm.sh`'s
"the one-instruction kill arm still dies" check is replaced by two checks pinning the legs.  After this round NO
footbridge access reachable by these probes ends the process except the SDRAM pair.
**Witness (rung 3):** the new rows on HEAD 9c28ca5 -- D1..D5 and D3's read die at their first undefined-direction
access (exit 1 with the site's complaint) -- red pre-fix, green post-fix with the same script.
**Gate:** `gate_arm.sh`'s footbridge section gains count + value pins for the new rows (the same shape as the E pins).

## 5. THE THREE CONTROLS' CURRENT KILL ARMS (what this round removes), verbatim
  161| KILL_LOAD = (0x2c, 0xE590718C, "ldr r7,[r0,#396]", "arm K: read IRQ_ENABLE_CLEAR (0x18c)")
  347| K = run_arm("K  kill      (MMU off,+18c)", MMU_OFF + BODY + [KILL_LOAD] + TAIL)
  231|         p.append((0x5c, 0xE590718C, "ldr r7,[r0,#396]",
  200| KILL    = (0x48, 0xE590718C, "ldr r7,[r0,#396]",
and the sites probe's K row:
  402| k_ok = any("ENABLE CLEAR" in f for f in K["fatals"]) and K["exit"] == 1
  408|          "exit=%s" % K["exit"], "ok" if k_ok else "FAIL"))
  411| results.append(k_ok)

## 6. QUESTIONS
**Q1 -- premise audit, as questions.**
 (a) For each of the five sites: is the datasheet direction as stated (quote the section)?  Is member 3 right for it,
     or is there a site where member 2 (silent) or member 4/5 (the model already computes something; a fault) is
     the honest disposition?  Is FAULT even available on ARM for this machine (grep the fork: `dev_unreadable`,
     `memory_rw` exception dispatch for ARM)?
 (b) One `warned_access` bit-field vs five per-site `int` latches: which matches the file's existing idiom (grep its
     latch fields), and does the bit-field create a "who else writes this field" collision hazard?
 (c) The K1/K2 legs: do they establish what the old kill arm established (death detected; death detected AFTER guest
     steps) in each of the THREE launchers, and is "the next ordinary interaction fails with `dead` before cleanup"
     observable through each probe's `send()`/`wait()` as written?  Quote the helper you checked.
 (d) After this round, is the statement "no footbridge access these probes make ends the process" TRUE?  Enumerate
     every `exit(` in the function and say which guest access reaches it.
 (e) Does anything in the tree read or depend on the five complaint texts or on `ENABLE CLEAR` (a gate grep, a
     hygiene allowlist, `gate_hygiene.sh`'s boot-log rules)?
**Q2 -- candidate weakenings (which row reds first, or escapes).**
  (a) a decline that keeps `exit(1)` at ONE of the five sites   (b) the announce unlatched (fires every access)
  (c) one latch bit shared by two sites (the second never announces)   (d) +0x18c decline that keeps
  `odata = d->irq_enable`   (e) a WRITE decline that stores the written value into irq_status anyway
  (f) a decline that ALSO swallows the legal direction of the same register (IRQ_STATUS READ returns 0 always)
  (g) the announce text misnames the register   (h) K1's startup leg passing on ANY nonzero exit
  (i) K2's quit leg passing when the child died BEFORE the prologue completed   (j) the latch cleared by a read
  (k) the harness legs implemented in one launcher only
**Q3 -- option-set completeness.**  DELETE / DECLINE / DECLINE + LATCHED ANNOUNCE / ACCEPT / FAULT / BACKED ACCEPT /
  IMPLEMENT.  Member 3 is proposed for all five.  Is there a member this brief did not weigh for any site?  Grep the
  fork for the sibling handlers' dispositions (`dev_footbridge.c`'s other arms; `dev_unreadable.c`).
**Q4 -- the harness change's own risk.**  Replacing a kill arm with two legs in three launchers is the largest
  harness edit of the campaign.  What is the smallest edit to the LEGS that leaves them green while proving nothing?
  Name the row you expect to stay green.
If, while verifying a claim, you found something ELSE -- say so.
End with the seat record: model, what you read, what you ran (nothing).


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
