# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `mc146818uie` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `mc146818uie`, state `open`)

**title:** devices/dev_mc146818.c tick -- no once-a-second UF with a UIE interrupt (only a polled UF hack) -- WRONG-RESULT

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T57 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A2-36).  Source URLs: https://github.com/rpajarola/gxemul/commit/871e551340226bdc3ed3c3b1c9e0e1fea824aa70.  Our site at de8c7547: src/devices/dev_mc146818.c:357-379.  Portable fix: yes -- port rpajarola 871e551.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- 358| 	 *  but it is good enough... Sprite polls this, iirc.)

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_mc146818.c b/src/devices/dev_mc146818.c
index ec89e02b..73778772 100644
--- a/src/devices/dev_mc146818.c
+++ b/src/devices/dev_mc146818.c
@@ -376,6 +376,7 @@ DEVICE_ACCESS(mc146818)
 
 			d->reg[MC_REGC * 4] |= MC_REGC_UF;
 			d->reg[MC_REGC * 4] |= MC_REGC_IRQF;
+			d->pending_timer_interrupts++;
 
 			/*  For some reason, some Linux/DECstation KN04
 			    kernels want the PF (periodic flag) bit set,
```

## Every edited function, after the fix

### `src/devices/dev_mc146818.c` -- post-edit lines 280-581 (`+` marks a line the diff added or the point of a deletion)

```c
  280|  DEVICE_ACCESS(mc146818)
  281|  {
  282|  	struct mc_data *d = (struct mc_data *) extra;
  283|  	struct tm *tmp;
  284|  	time_t timet;
  285|  	size_t i;
  286|  
  287|  	/*  NOTE/TODO: This access function only handles 8-bit accesses!  */
  288|  
  289|  	relative_addr /= d->addrdiv;
  290|  
  291|  	/*  Different ways of accessing the registers:  */
  292|  	switch (d->access_style) {
  293|  	case MC146818_ALGOR:
  294|  	case MC146818_CATS:
  295|  	case MC146818_PC_CMOS:
  296|  		if ((relative_addr & 1) == 0x00) {
  297|  			if (writeflag == MEM_WRITE) {
  298|  				d->last_addr = data[0];
  299|  				return 1;
  300|  			} else {
  301|  				data[0] = d->last_addr;
  302|  				return 1;
  303|  			}
  304|  		} else
  305|  			relative_addr = d->last_addr * 4;
  306|  		break;
  307|  	case MC146818_ARC_NEC:
  308|  		if (relative_addr == 0x01) {
  309|  			if (writeflag == MEM_WRITE) {
  310|  				d->last_addr = data[0];
  311|  				return 1;
  312|  			} else {
  313|  				data[0] = d->last_addr;
  314|  				return 1;
  315|  			}
  316|  		} else if (relative_addr == 0x00)
  317|  			relative_addr = d->last_addr * 4;
  318|  		else {
  319|  			fatal("[ mc146818: not accessed as an "
  320|  			    "MC146818_ARC_NEC device! ]\n");
  321|  		}
  322|  		break;
  323|  	case MC146818_ARC_JAZZ:
  324|  		/*  See comment for dev_mc146818_jazz_access().  */
  325|  		relative_addr = d->last_addr * 4;
  326|  		break;
  327|  	case MC146818_DEC:
  328|  	case MC146818_SGI:
  329|  		/*
  330|  		 *  This device was originally written for DECstation
  331|  		 *  emulation, so no changes are necessary for that access
  332|  		 *  style.
  333|  		 *
  334|  		 *  SGI access bytes 0x0..0xd at offsets 0x0yz..0xdyz, where yz
  335|  		 *  should be ignored. It works _almost_ as DEC, if offsets are
  336|  		 *  divided by 0x40.
  337|  		 */
  338|  		break;
  339|  	case MC146818_PMPPC:
  340|  		relative_addr *= 4;
  341|  		break;
  342|  	default:
  343|  		;
  344|  	}
  345|  
  346|  #ifdef MC146818_DEBUG
  347|  	if (writeflag == MEM_WRITE) {
  348|  		fatal("[ mc146818: write to addr=0x%04x (len %i): ",
  349|  		    (int)relative_addr, (int)len);
  350|  		for (i=0; i<len; i++)
  351|  			fatal("0x%02x ", data[i]);
  352|  		fatal("]\n");
  353|  	}
  354|  #endif
  355|  
  356|  	/*
  357|  	 *  Sprite seems to wants UF interrupt status, once every second, or
  358|  	 *  it hangs forever during bootup.  (These do not cause interrupts,
  359|  	 *  but it is good enough... Sprite polls this, iirc.)
  360|  	 *
  361|  	 *  Linux on at least sgimips and evbmips (Malta) wants the UIP bit
  362|  	 *  in REGA to be updated once a second.
  363|  	 */
  364|  	if (relative_addr == MC_REGA*4 || relative_addr == MC_REGC*4) {
  365|  		timet = time(NULL);
  366|  		tmp = gmtime(&timet);
  367|  		d->reg[MC_REGC * 4] &= ~MC_REGC_UF;
  368|  		if (tmp->tm_sec != d->previous_second) {
  369|  			d->n_seconds_elapsed ++;
  370|  			d->previous_second = tmp->tm_sec;
  371|  		}
  372|  		if (d->n_seconds_elapsed > d->uip_threshold) {
  373|  			d->n_seconds_elapsed = 0;
  374|  
  375|  			d->reg[MC_REGA * 4] |= MC_REGA_UIP;
  376|  
  377|  			d->reg[MC_REGC * 4] |= MC_REGC_UF;
  378|  			d->reg[MC_REGC * 4] |= MC_REGC_IRQF;
  379|+ 			d->pending_timer_interrupts++;
  380|  
  381|  			/*  For some reason, some Linux/DECstation KN04
  382|  			    kernels want the PF (periodic flag) bit set,
  383|  			    even though interrupts are not enabled?  */
  384|  			d->reg[MC_REGC * 4] |= MC_REGC_PF;
  385|  		} else
  386|  			d->reg[MC_REGA * 4] &= ~MC_REGA_UIP;
  387|  	}
  388|  
  389|  	/*  RTC data is in either BCD format or binary:  */
  390|  	if (d->use_bcd)
  391|  		d->reg[MC_REGB * 4] &= ~(1 << 2);
  392|  	else
  393|  		d->reg[MC_REGB * 4] |= (1 << 2);
  394|  
  395|  	/*  RTC date/time is always Valid:  */
  396|  	d->reg[MC_REGD * 4] |= MC_REGD_VRT;
  397|  
  398|  	if (writeflag == MEM_WRITE) {
  399|  		/*  WRITE:  */
  400|  		switch (relative_addr) {
  401|  		case MC_REGA*4:
  402|  			if ((data[0] & MC_REGA_DVMASK) == MC_BASE_32_KHz)
  403|  				d->timebase_hz = 32000;
  404|  			if ((data[0] & MC_REGA_DVMASK) == MC_BASE_1_MHz)
  405|  				d->timebase_hz = 1000000;
  406|  			if ((data[0] & MC_REGA_DVMASK) == MC_BASE_4_MHz)
  407|  				d->timebase_hz = 4000000;
  408|  			switch (data[0] & MC_REGA_RSMASK) {
  409|  			case MC_RATE_NONE:
  410|  				d->interrupt_hz = 0;
  411|  				break;
  412|  			case MC_RATE_1:
  413|  				if (d->timebase_hz == 32000)
  414|  					d->interrupt_hz = 256;
  415|  				else
  416|  					d->interrupt_hz = 32768;
  417|  				break;
  418|  			case MC_RATE_2:
  419|  				if (d->timebase_hz == 32000)
  420|  					d->interrupt_hz = 128;
  421|  				else
  422|  					d->interrupt_hz = 16384;
  423|  				break;
  424|  			case MC_RATE_8192_Hz:	d->interrupt_hz = 8192;	break;
  425|  			case MC_RATE_4096_Hz:	d->interrupt_hz = 4096;	break;
  426|  			case MC_RATE_2048_Hz:	d->interrupt_hz = 2048;	break;
  427|  			case MC_RATE_1024_Hz:	d->interrupt_hz = 1024;	break;
  428|  			case MC_RATE_512_Hz:	d->interrupt_hz = 512;	break;
  429|  			case MC_RATE_256_Hz:	d->interrupt_hz = 256;	break;
  430|  			case MC_RATE_128_Hz:	d->interrupt_hz = 128;	break;
  431|  			case MC_RATE_64_Hz:	d->interrupt_hz = 64;	break;
  432|  			case MC_RATE_32_Hz:	d->interrupt_hz = 32;	break;
  433|  			case MC_RATE_16_Hz:	d->interrupt_hz = 16;	break;
  434|  			case MC_RATE_8_Hz:	d->interrupt_hz = 8;	break;
  435|  			case MC_RATE_4_Hz:	d->interrupt_hz = 4;	break;
  436|  			case MC_RATE_2_Hz:	d->interrupt_hz = 2;	break;
  437|  			default:/*  debug("[ mc146818: unimplemented "
  438|  				    "MC_REGA RS: %i ]\n",
  439|  				    data[0] & MC_REGA_RSMASK);  */
     | [... lines 440-551 not shown ...]
  552|  
  553|  		data[0] = d->reg[relative_addr];
  554|  
  555|  		if (relative_addr == MC_REGC*4) {
  556|  			INTERRUPT_DEASSERT(d->irq);
  557|  
  558|  			/*
  559|  			 *  Acknowledging an interrupt decreases the
  560|  			 *  number of pending "real world" timer ticks.
  561|  			 */
  562|  			if (d->reg[MC_REGC * 4] & MC_REGC_PF &&
  563|  			    d->pending_timer_interrupts > 0)
  564|  				d->pending_timer_interrupts --;
  565|  
  566|  			d->reg[MC_REGC * 4] = 0x00;
  567|  		}
  568|  	}
  569|  
  570|  #ifdef MC146818_DEBUG
  571|  	if (writeflag == MEM_READ) {
  572|  		fatal("[ mc146818: read from addr=0x%04x (len %i): ",
  573|  		    (int)relative_addr, (int)len);
  574|  		for (i=0; i<len; i++)
  575|  			fatal("0x%02x ", data[i]);
  576|  		fatal("]\n");
  577|  	}
  578|  #endif
  579|  
  580|  	return 1;
  581|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_MC146818UIE: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_MC146818UIE: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
