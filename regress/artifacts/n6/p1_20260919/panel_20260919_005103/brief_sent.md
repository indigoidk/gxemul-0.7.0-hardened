# PASS 1 (DESIGN) -- `n6`, round 1 of the footbridge campaign: the +0x188 read (IRQEnable) is ACCEPTED

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated
wrongly.  **Check the premises, not just the derivations.**  Where I state something as
fact, ask whether it is true.  A seat that re-derives a premise from something this brief
did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/` (and `GXEMUL-SEC/regress/` for the probes).**  There are
THREE pristine-2021-upstream copies of GXemul under the project root (`./src/` and two under
`_archive/audit-results-*/builds/`).  They are NOT this fork.  If your line numbers disagree with mine by
hundreds you are reading one of them — say so rather than reconciling.  Every line number below was
generated from the tree at HEAD `408accf` when this brief was built.

**If you cannot read files that is expected** — every fact you need is inlined.  Name any
premise you cannot settle from this packet rather than guessing at it.

**Where this brief states an ARITHMETIC claim — an offset, an encoding, a count — ENUMERATE it rather than
reasoning about it.**  And ENUMERATE THE RIGHT DOMAIN: a domain is itself a premise.

**Scope your reading to `GXEMUL-SEC/src/` and `GXEMUL-SEC/regress/*.py`, `GXEMUL-SEC/regress/*.sh`.  Do not
read `regress/artifacts/` or `tools/pipeline/ledger.json`** -- everything from them that a question depends on
is inlined below.

**VERDICT LINE FIRST**, so your answer survives truncation.

---

## 1. THE DEFECT, AND WHY THIS ROUND TAKES ONE SITE

`DEVICE_ACCESS(footbridge)` (the DC21285 core-logic device of the `-E cats` ARM machine, mapped at physical
`0x42000000`) ends the emulator process with `exit(1)` at EIGHT guest-reachable sites.  Seven are accesses in a
direction the datasheet says the register does not have (a write to a read-only status register, a read of a
write-only register, a read of an SDRAM configuration register the model does not answer).  **One is
different: a READ of `+0x188`.**

The DC21285 datasheet (Intel 278115-001, `dc21285.txt`) gives, verbatim:

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

and for the register at `+0x188`:

 6910| 
 6911|         IRQEnable/FIQEnable Register--Offset 188h/288h
 6912| 
 6913|         This read-only register is used to mask the interrupt input sources and defines which active sources
 6914|         generate an interrupt request to the SA-110 on nIRQ/nFIQ. The value of this register can only be
 6915|         changed by writing to the EnableSet and EnableClear registers.
 6916| 
 6917|         Dword Bit  Name                R/W  Description
 6918|         31:0
 6919|                    IRQEnable/FIQEnable R    A 1 indicates that the associated interrupt source is
 6920|                                             enabled and allows an interrupt request.
 6921| 

So a read of `+0x188` is a DOCUMENTED, LEGAL read of a read-only register (IRQEnable).  The model already
computes the right answer -- `odata = d->irq_enable;` -- and then calls `fatal()` and `exit(1)`.  **The
disposition proposed is ACCEPT (option-set member 4): delete the `fatal()` and the `exit(1)`, keep the value, add
no message** -- there is no event to announce, and a bounded announce would print "unexpected" about a read that
is expected.

**One site per round** (this project's reopening rule): the seven invalid-direction sites are a different
semantic class and a different disposition (a DECLINE, members 2/3), and they are the NEXT round.

## 2. SETTLED PREMISES (the 2026-09-18 assess panel, all nine seats; re-derive any you doubt)

* **The census.**  `tools/pipeline/exit_census.py` at HEAD, comments stripped: `dev_footbridge.c` has TEN live
  `exit(1)`: eight inside `DEVICE_ACCESS(footbridge)` at 565 / 574 / 589 / 604 / 613 / 622 / 712 / 737, and two in
  its `DEVINIT` at 841 / 877 (construction-time; no guest reaches them).
* **`+0x188` reaches `case IRQ_ENABLE_SET` unmodified.**  The only rewrite of `relative_addr` before the switch
  is the timer fold, gated to `[TIMER_1_LOAD, TIMER_4_CLEAR]` = `[0x300, 0x36C]` (`dc21285reg.h`), which `0x188`
  is outside.  `IRQ_ENABLE_SET` is `0x188` (`dc21285reg.h:335`).
* **The machine.**  `machine_cats.c:63-64` attaches `footbridge ... addr=0x42000000`.  The probes turn the MMU off
  first: under the boot translation table only the low 256 MB is mapped, so an MMU-on access to `0x42000000`
  aliases to RAM and returns 0 -- the probes carry a negative control (arm T) for exactly that.
* **THREE probe arms use this read as their "something can still end the process" control, and all three must
  move in THE SAME COMMIT as the fix** (codex, assess): `footbridge_sites_probe.py` arm K (GATED in gate_arm.sh,
  row K1), `fbpending_drain_probe.py`'s kill arm, and `fbpending_witness.py` arm K.  **CORRECTED by a dedicated
  codex review (2026-09-18 22:06, `_scratchpad/n6/codex_dedicated_20260918/`): only the SITES probe checks both the
  `ENABLE SET` text and exit status 1 (`footbridge_sites_probe.py:291`).  The drain and witness probes RECORD the
  text for reporting and require only `HOST-DIED`; their close routines (`fbpending_drain_probe.py:403`,
  `fbpending_witness.py:342`) DISCARD the `waitpid` status, so neither can tell exit 1 from any other host death.**
  That is the same class the peer session found in `lca_isalane_probe.py` on #538's pass 2 (a host death AFTER the
  last observation passes); this round moves those two arms anyway, so it should also bind the status (Q1e).
* **The proposed temporary target is `+0x100`, SDRAM_BA_MASK, READ** -- `ldr r7,[r0,#256]`, encoding
  `0xE5907100` (grok, assess) -- which ends the process at line 711-712 with `footbridge read from sdram_ba_mask`.
  It is TEMPORARY: it is one of the seven DECLINE-class sites, so the next round must move the control again or
  replace it (see Q4).

## 3. THE CODE -- the FULL enclosing function, every exit path and the common tail

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
  586| 			odata = d->irq_enable;
  587| 			fatal("[ WARNING: footbridge read from "
  588| 			    "ENABLE SET? ]\n");
  589| 			exit(1);
  590| 		}
  591| 		break;
  592| 
  593| 	case IRQ_ENABLE_CLEAR:
  594| 		if (writeflag == MEM_WRITE) {
  595| 			d->irq_enable &= ~idata;
  596| 			if (d->irq_status & d->irq_enable)
  597| 				INTERRUPT_ASSERT(d->irq);
  598| 			else
  599| 				INTERRUPT_DEASSERT(d->irq);
  600| 		} else {
  601| 			odata = d->irq_enable;
  602| 			fatal("[ WARNING: footbridge read from "
  603| 			    "ENABLE CLEAR? ]\n");
  604| 			exit(1);
  605| 		}
  606| 		break;
  607| 
  608| 	case FIQ_STATUS:
  609| 		if (writeflag == MEM_READ)
  610| 			odata = d->fiq_status & d->fiq_enable;
  611| 		else {
  612| 			fatal("[ WARNING: footbridge write to fiq status? ]\n");
  613| 			exit(1);
  614| 		}
  615| 		break;
  616| 
  617| 	case FIQ_RAW_STATUS:
  618| 		if (writeflag == MEM_READ)
  619| 			odata = d->fiq_status;
  620| 		else {
  621| 			fatal("[ footbridge write to fiq_raw_status ]\n");
  622| 			exit(1);
  623| 		}
  624| 		break;
  625| 
  626| 	case FIQ_ENABLE_SET:
  627| 		if (writeflag == MEM_WRITE)
  628| 			d->fiq_enable |= idata;
  629| 		break;
  630| 
  631| 	case FIQ_ENABLE_CLEAR:
  632| 		if (writeflag == MEM_WRITE)
  633| 			d->fiq_enable &= ~idata;
  634| 		break;
  635| 
  636| 	case TIMER_1_LOAD:
  637| 		if (writeflag == MEM_READ)
  638| 			odata = d->timer_load[timer_nr];
  639| 		else {
  640| 			d->timer_load[timer_nr] = idata & TIMER_MAX_VAL;
  641| 			reload_timer_value(cpu, d, timer_nr);
  642| 			/*  debug("[ footbridge: timer %i (1-based), "
  643| 			    "value %i ]\n", timer_nr + 1,
  644| 			    (int)d->timer_value[timer_nr]);  */
  645| 			INTERRUPT_DEASSERT(d->timer_irq[timer_nr]);
  646| 		}
  647| 		break;
  648| 
  649| 	case TIMER_1_VALUE:
  650| 		if (writeflag == MEM_READ)
  651| 			odata = d->timer_value[timer_nr];
  652| 		else
  653| 			d->timer_value[timer_nr] = idata & TIMER_MAX_VAL;
  654| 		break;
  655| 
  656| 	case TIMER_1_CONTROL:
  657| 		if (writeflag == MEM_READ)
  658| 			odata = d->timer_control[timer_nr];
  659| 		else {
  660| 			d->timer_control[timer_nr] = idata;
  661| 			/*  #432: both prescaler bits set is TIMER_EXTERNAL
  662| 			    (0x0C, dc21285reg.h:364) -- a LEGAL named encoding,
  663| 			    and it used to reach fatal()+exit(1) right here, so a
  664| 			    guest selecting the external clock source KILLED THE
  665| 			    HOST.  Arguably likelier than the zero load, since it
  666| 			    is a documented mode rather than a malformed value.
  667| 			    The rate an external clock would actually give is
  668| 			    UNKNOWN and is NOT invented: footbridge_effective_cycles()
  669| 			    now gives the encoding a defined, survivable meaning
  670| 			    (the unprescaled period), and the real semantics are
  671| 			    filed for a round that has a datasheet.  */
  672| 			if (idata & TIMER_ENABLE) {
  673| 				reload_timer_value(cpu, d, timer_nr);
  674| 			} else {
  675| 				d->pending_timer_interrupts[timer_nr] = 0;
  676| 			}
  677| 			INTERRUPT_DEASSERT(d->timer_irq[timer_nr]);
  678| 		}
  679| 		break;
  680| 
  681| 	case TIMER_1_CLEAR:
  682| 		/*  #474: a READ must not perform the clear.  This case carried no
  683| 		    writeflag test at all, while TIMER_1_CONTROL immediately above it
  684| 		    does -- so a guest READ reloaded the counter, decremented the
  685| 		    pending count and DEASSERTED the interrupt.  A guest that merely
  686| 		    read the register silently acknowledged a pending timer interrupt;
  687| 		    the guest-visible consequence is a LOST interrupt, not a bad value.
  688| 
  689| 		    FOUR addresses, not one: the fold above normalises 0x30C/0x32C/
  690| 		    0x34C/0x36C onto this single case.
  691| 
  692| 		    GUARD THE BODY, KEEP THE break.  An early return here would skip
  693| 		    the function's common tail, which writes odata back on a read, and
  694| 		    would hand a guest an untouched buffer -- a defect this code does
  695| 		    not currently have.  */
  696| 		if (writeflag == MEM_WRITE) {
  697| 			if (d->timer_control[timer_nr] & TIMER_MODE_PERIODIC) {
  698| 				reload_timer_value(cpu, d, timer_nr);
  699| 			}
  700| 
  701| 			if (d->pending_timer_interrupts[timer_nr] > 0) {
  702| 				d->pending_timer_interrupts[timer_nr] --;
  703| 			}
  704| 
  705| 			INTERRUPT_DEASSERT(d->timer_irq[timer_nr]);
  706| 		}
  707| 		break;
  708| 
  709| 	case SDRAM_BA_MASK:
  710| 		if (writeflag == MEM_READ) {
  711| 			fatal("[ footbridge read from sdram_ba_mask ]\n");
  712| 			exit(1);
  713| 		} else {
  714| 			switch (idata) {
  715| 			case SDRAM_MASK_256KB:
  716| 			case SDRAM_MASK_512KB:
  717| 			case SDRAM_MASK_1MB:
  718| 			case SDRAM_MASK_2MB:
  719| 			case SDRAM_MASK_4MB:
  720| 			case SDRAM_MASK_8MB:
  721| 			case SDRAM_MASK_16MB:
  722| 			case SDRAM_MASK_32MB:
  723| 			case SDRAM_MASK_64MB:
  724| 			case SDRAM_MASK_128MB:
  725| 			case SDRAM_MASK_256MB:
  726| 				break;
  727| 			default:
  728| 				fatal("[ footbridge write to sdram_ba_mask "
  729| 				    "%#llx ]\n", (long long)idata);
  730| 				break;
  731| 			}
  732| 		}
  733| 		break;
  734| 	case SDRAM_BA_OFFSET:
  735| 		if (writeflag == MEM_READ) {
  736| 			fatal("[ footbridge read from sdram_ba_offset ]\n");
  737| 			exit(1);
  738| 		} else {
  739| 			if (idata != 0)
  740| 				fatal("[ footbridge write to sdram_ba_offset "
  741| 				    "%#llx ]\n", (long long)idata);
  742| 		}
  743| 		break;
  744| 
  745| 	default:if (writeflag == MEM_READ) {
  746| 			fatal("[ footbridge: read from 0x%x ]\n",
  747| 			    (int)relative_addr);
  748| 		} else {
  749| 			fatal("[ footbridge: write to 0x%x: 0x%llx ]\n",
  750| 			    (int)relative_addr, (long long)idata);
  751| 		}
  752| 	}
  753| 
  754| 	if (writeflag == MEM_READ)
  755| 		memory_writemax64(cpu, data, len, odata);
  756| 
  757| 	return 1;
  758| }

## 4. THE THREE CONTROLS THAT DEPEND ON THE +0x188 EXIT

`regress/footbridge_sites_probe.py` -- its header, the kill-arm word, and the K1 row:

   47| THE KILL PAIR, which is this probe's own failability control.  Arms L and K differ by
   48| EXACTLY ONE INSTRUCTION.  Arm K adds a guest read of IRQ_ENABLE_SET (base+0x188), which
   49| dev_footbridge.c:495-497 answers with fatal() then exit(1) -- an UNFIXED site, used here
   50| rather than repaired, because a probe that reports SURVIVED for every row is vacuous unless
   51| something in it can still die.  Arm L must live; arm K must exit 1 and say so.  If both
   52| survived, the guest instructions are not reaching the device at all and every SURVIVED
   53| verdict above is worthless; if both died, the probe is killing the host for its own reasons.
   54| The one-instruction delta is the entire argument.
   55| 

  102| KILL_NOP  = (0x2c, NOP,        NOPTXT,             "arm L: no kill site")
  103| KILL_LOAD = (0x2c, 0xE5907188, "ldr r7,[r0,#392]", "arm K: read IRQ_ENABLE_SET (0x188)")
  104| TAIL = [(0x30, NOP, NOPTXT, "landing pad -- planted, never stepped")]

  289| #  ---- the kill pair: this probe's own failability control. ----
  290| l_ok = L["status"] == "SURVIVED" and L["exit"] == 0 and not L["fatals"]
  291| k_ok = any("ENABLE SET" in f for f in K["fatals"]) and K["exit"] == 1
  292| print("%-4s %-40s %-30s %s"
  293|       % ("I1", "isolation arm SURVIVES untouched",
  294|          "status=%s exit=%s" % (L["status"], L["exit"]), "ok" if l_ok else "FAIL"))
  295| print("%-4s %-40s %-30s %s"
  296|       % ("K1", "kill arm dies at 0x188, exit 1",
  297|          "exit=%s" % K["exit"], "ok" if k_ok else "FAIL"))
  298| print("      kill arm said: %s" % ((K["fatals"] or ["(nothing)"])[-1]))
  299| results.append(l_ok)
  300| results.append(k_ok)

`regress/gate_arm.sh` grades it (this is the gated one):

 1098|     check "footbridge: the one-instruction kill arm still dies" \
 1099|           "$(grep -cE '^K1 .*ok$' "$FBLOG")" "1"

`regress/fbpending_drain_probe.py` (a DETECTOR, dated-exempt from gating):

  225|     if kill:
  226|         p.append((0x5c, 0xE5907188, "ldr r7,[r0,#392]",
  227|                   "arm K: IRQ_ENABLE_SET -> fatal()+exit(1)"))
  228|         emit(0x60, NOP, "")
  229|         return p

  552|     s = Session()
  553|     if not s.wait(timeout=120):
  554|         s.close()
  555|         return dict(status="NO-PROMPT", saw=False)
  556|     plant(s, prog)
  557|     step_and_check(s, prog, PROLOGUE_N + 3)
  558|     died = s.dead
  559|     if not died:
  560|         s.send("reg", timeout=10)
  561|         died = s.dead
  562|     saw = "ENABLE SET" in s.buf
  563|     s.close()
  564|     return dict(status="HOST-DIED" if died else "SURVIVED", saw=saw)
  565| 

`regress/fbpending_witness.py` (a WITNESS -- ungated by design; it reproduced #442's pre-fix symptom):

   72|   T  negative control.  MMU left on.  Must not return 0x1011 or 0x00345678.
   73|   K  failability control.  Arm A's prologue plus ONE instruction, a guest read of
   74|      IRQ_ENABLE_SET (footbridge+0x188), which dev_footbridge.c:486-499 answers with
   75|      fatal() then exit(1).  A probe in which nothing can die proves nothing by
   76|      surviving; K must kill the host and A must not.

  195| KILL    = (0x48, 0xE5907188, "ldr r7,[r0,#392]",
  196|            "arm K: read IRQ_ENABLE_SET -> fatal()+exit(1) at dev_footbridge.c:492-497")

  440|     died = s.dead
  441|     if not died:
  442|         #  The exit may land between the write and our read; one more poke settles it.
  443|         s.send("reg", timeout=10)
  444|         died = s.dead
  445|     seen = "ENABLE SET" in s.buf
  446|     s.close()
  447|     return dict(status="HOST-DIED" if died else "SURVIVED", saw_fatal=seen,
  448|                 badis=bad, nsteps=len(ex))
  449| 
  450| 

## 5. THE PROPOSED ROUND

1. **Fix.**  In `case IRQ_ENABLE_SET`, delete the `fatal("[ WARNING: footbridge read from ENABLE SET? ]\n")` and
   the `exit(1)`; keep `odata = d->irq_enable;`.  A `/* #NNN: */` comment quotes the datasheet line.
2. **Move the three controls to `+0x100`** (word `0xE5907100`, `ldr r7,[r0,#256]`), their text oracles from
   `ENABLE SET` to `sdram_ba_mask`, in the same commit, and re-run each.
3. **New ACCEPT rows in `footbridge_sites_probe.py`** (gated), all in the surviving arm:
   * `E0` read `+0x188` BEFORE any enable write, want `0` (the datasheet's reset value) -- the only row whose read
     sees `d->irq_enable == 0`, which is the field the read body reads (the operand-swap mutant Q2(g));
   * `E1` write a pattern P to `+0x188` (IRQEnableSet), read `+0x188` back, want exactly P;
   * `E2` write a second, DISJOINT pattern Q, read back, want exactly `P | Q` (pins the OR-accumulation --
     codex, assess: the read makes `|=` observable for the first time);
   * `E3` a BYTE read (`ldrb`) of `+0x188`, want `0x02`, P's low byte (the access width is a dominating input);
   * `E4` the surviving arm prints NO `ENABLE SET` diagnostic (a member-3 mutant -- keep the `fatal()`, drop only
     the `exit(1)` -- must red a row; `mk48_nvram_probe.py`'s `msg silent` row is the in-tree precedent).
   * `E5` (codex, dedicated review): after E2, write P to `+0x18c` (IRQEnableClear), then word-read `+0x188`, want
     exactly Q -- the other documented way the newly readable register changes, and preservation of uncleared bits.
   * `E6` (codex): an aligned HALFWORD read (`ldrh`) of `+0x188` after E2, want `0x2002` -- the handler passes `len`
     unchanged to `memory_writemax64` and no row held the 2-byte width.
   * and Q becomes `0x60000000` (bits 29 AND 30) so E2 wants `0x60002002`: a variant that keeps the diagnostic only
     for bits 30/31 (Q2(l)) is otherwise observed by nothing.
   P and Q use VALID source bits no source asserts during the run -- the DC21285 bit table reserves bits 0, 20,
   21 and 26; bits 4-7 are the four timers, which the DEVINIT connects locally; and on `cats` the ISA cascade is
   line 10 (`irq_path_isa` = `"%s.10"`).  Proposed: P = `0x00002002` (bits 1 and 13 -- soft interrupt, xcs_l[1];
   the LOW BYTE is nonzero so E3 cannot be satisfied by the 0 an absent device returns), Q = `0x20000000`
   (bit 29, received master abort).  **Is that choice safe on this machine?** (Q1c)
   E0's value alone is what an absent device returns; it is informative only beside the arm's device-signature
   rows (A1 VENDOR_ID `0x1011`, A2 the 24-bit TIMER_1_LOAD mask), which prove the device answered.
4. **A kill table before commit**, PRETABLE first: the mutants in Q2, each scored against the extended probe.
5. **Records**: the CHANGELOG round block; the #218-#223 summary that says the footbridge halts "were made
   graceful" is corrected in place (assess: codex, grok -- REVIEW_FINDINGS and the #220 row are already precise).

## 6. QUESTIONS

**Q1 -- premise audit.**
* (a) Is ACCEPT right, or does anything in the datasheet or the fork's own history make this read something the
  model should decline?  (Grep the fork for how the sibling `+0x288` read, FIQ_ENABLE_SET, is answered -- it is
  filed separately as `fiqenableread`, returning 0 rather than `d->fiq_enable`.  Should it join this round under
  the reopening rule -- same device, same semantic class, same detector -- or stay separate?)
* (b) Is `+0x100` a sound TEMPORARY control?  Does the MMU-off prologue, the word `0xE5907100`, and the
  `sdram_ba_mask` text give each of the three probes exactly what `+0x188` gave them?
* (c) Are P (bits 1, 13) and Q (bit 29) inert on `-E cats` during these probes -- nothing sets those bits of
  `d->irq_status`, so the enable write asserts nothing?  If a write DOES assert the interrupt, does that change
  any existing row's verdict under single-step?
* (d) Does anything else in the tree read or depend on this `fatal()` text (`ENABLE SET`) -- a gate grep, a
  hygiene list, a boot-log allowlist?  (codex scoped its search to src/ and regress/ and found only the four sites
  named above; the tree-wide claim is NOT CHECKED.)
* (e) Should the drain and witness kill arms, moved by this round, also BIND the `waitpid` status and require exit 1
  -- and does binding it change any existing row's verdict on the surviving arm (a host death after the last
  observation would then be visible)?

**Q2 -- candidate weakenings.  For each, say whether rows E1-E4 plus the existing rows catch it, and which row
reds first.**
  (a) delete `odata = d->irq_enable;` (the read returns 0)
  (b) `odata = d->irq_status;`             (c) `odata = d->irq_status & d->irq_enable;`
  (d) `odata = d->fiq_enable;`              (e) keep `fatal()`, delete only `exit(1)`
  (f) reinstate `fatal()`+`exit(1)` only when `len != 4`
  (g) reinstate them only when `d->irq_enable == 0`   (an operand swap onto a field the read body reads)
  (h) the write arm's `d->irq_enable |= idata;` becomes `d->irq_enable = idata;`
  (i) the fix lands, and the three controls are NOT moved
  (j) the write arm's assert condition becomes `d->irq_status | d->irq_enable` (codex: writing P then asserts the
      CPU IRQ with no pending source, and no listed row observes the IRQ line -- what row would?)
  (k) the same deletion is applied to `IRQ_ENABLE_CLEAR`'s read branch too (`+0x18c`, which the datasheet says is
      WRITE-ONLY) -- E5 reads `+0x188`, not `+0x18c`; is a row that expects the `+0x18c` read to STILL be refused
      owed, and in what form once the seven decline sites are de-fatalised next round?

**Q3 -- option-set completeness.**  The set is DELETE / DECLINE / DECLINE+LATCHED ANNOUNCE / ACCEPT / FAULT /
BACKED ACCEPT / IMPLEMENT.  ACCEPT is proposed.  Is there a member this brief did not weigh?  Is FAULT available
on ARM for this machine, and would it be RIGHT for a documented readable register (it would not be, if the
datasheet is right -- check)?

**Q4 -- the order of the campaign.**  The assess panel split: ACCEPT first (this brief; costs a TEMPORARY control
move now and another later) vs the seven-site DECLINE group first (no control move now, but the LAST remaining
exit is then this one, and removing it later needs a replacement control -- "a mutation failability leg before
the last kill goes").  Either way the three probes eventually need a failability control that does not depend on
the device ending the process.  What should that control be, and should THIS round build it instead of moving to
`+0x100`?

**Standing licence:** if, while verifying a claim, you found something ELSE — say so.


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
