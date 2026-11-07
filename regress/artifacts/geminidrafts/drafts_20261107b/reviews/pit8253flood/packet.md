# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `pit8253flood` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `pit8253flood`, state `open`)

**title:** pit8253flood  dev_8253.c: bound every unconditional emission in DEVICE_ACCESS(8253) -- LATCH :204/:270/:342, DELETE :198/:200, :351/:354 are dead code

**state_note (head):** pass 1 complete 2026-09-17, nine seats + Fable adjudication.  STAYS FIRST in the queue -- Fable ruled the panel's demotion wrong, on reach, with owner sequencing breaking a severity tie.

**The drafter's own reading:** STILL PRESENT: YES -- `src/devices/dev_8253.c:270`

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_8253.c b/src/devices/dev_8253.c
index 9e756933..7b01d4a6 100644
--- a/src/devices/dev_8253.c
+++ b/src/devices/dev_8253.c
@@ -195,15 +195,17 @@ DEVICE_ACCESS(8253)
 						timer_update_frequency(
 						    d->timer0, d->hz[0]);
 					break;
-				case 1:	fatal("TODO: DMA refresh?\n");
+				case 1:	/* #pit8253flood: deleted TODO: DMA refresh? */
 					break;	/*  #223: (Codex/Fable) warn+ignore, don't exit() the host  */
-				case 2:	fatal("TODO: 8253 tone generation?\n");
+				case 2:	/* #pit8253flood: deleted TODO: 8253 tone generation? */
 					break;
 				}
 				break;
-			default:fatal("[ 8253: huh? writing to counter"
-				    " %i but neither from msb nor lsb? ]\n",
-				    (int)relative_addr);
+			default:if (!d->latched[relative_addr]) {
+					fatal("[ 8253: huh? writing to counter"
+					    " %i but neither from msb nor lsb? ]\n",
+					    (int)relative_addr);
+				}
 				break;	/*  #223: (Codex/Fable) don't exit() the host  */
 			}
 		} else if (d->latched[relative_addr]) {
@@ -267,9 +269,11 @@ DEVICE_ACCESS(8253)
 			case I8253_TIMER_MSB:
 				odata = (d->counter[relative_addr] >> 8) & 0xff;
 				break;
-			default:fatal("[ 8253: huh? reading from counter"
-				    " %i but neither from msb nor lsb? ]\n",
-				    (int)relative_addr);
+			default:if (!d->latched[relative_addr]) {
+					fatal("[ 8253: huh? reading from counter"
+					    " %i but neither from msb nor lsb? ]\n",
+					    (int)relative_addr);
+				}
 				break;	/*  #223: (Codex/Fable) don't exit() the host  */
 			}
 		}
@@ -339,7 +343,9 @@ DEVICE_ACCESS(8253)
 			if (idata & I8253_TIMER_BCD) {
 				/*  #223: (Codex/Fable) warn+ignore BCD mode instead of
 				    exit()ing the host.  */
-				fatal("[ 8253: BCD not yet implemented ]\n");
+				if (!d->latched[d->counter_select]) {
+					fatal("[ 8253: BCD not yet implemented ]\n");
+				}
 			}
 		} else {
 			debug("[ 8253: read; can this actually happen? ]\n");
@@ -347,13 +353,7 @@ DEVICE_ACCESS(8253)
 		}
 		break;
 
-	default:if (writeflag == MEM_WRITE) {
-			fatal("[ 8253: unimplemented write to address 0x%x"
-			    " data=0x%02x ]\n", (int)relative_addr, (int)idata);
-		} else {
-			fatal("[ 8253: unimplemented read from address 0x%x "
-			    "]\n", (int)relative_addr);
-		}
+	default:/* #pit8253flood: deleted dead code */
 		break;	/*  #223: (Codex/Fable) warn+ignore, don't exit() the host  */
 	}
```

## Every edited function, after the fix

### `src/devices/dev_8253.c` -- post-edit lines 132-364 (`+` marks a line the diff added or the point of a deletion)

```c
  132|  DEVICE_ACCESS(8253)
  133|  {
  134|  	struct pit8253_data *d = (struct pit8253_data *) extra;
  135|  	uint64_t idata = 0, odata = 0;
  136|  	int rw = 0;		/*  #440: the half THIS access refers to  */
  137|  
  138|  	if (writeflag == MEM_WRITE)
  139|  		idata = memory_readmax64(cpu, data, len);
  140|  
  141|  	d->in_use = 1;
  142|  
  143|  	switch (relative_addr) {
  144|  
  145|  	case I8253_TIMER_CNTR0:
  146|  	case I8253_TIMER_CNTR1:
  147|  	case I8253_TIMER_CNTR2:
  148|  		/*
  149|  		 *  #440: in the 16-bit format it is the counter's read/write
  150|  		 *  flip-flop -- not mode_byte -- that says which half an access
  151|  		 *  refers to, and it ALTERNATES: LSB, MSB, LSB, ...
  152|  		 *
  153|  		 *  The old code cleared I8253_TIMER_LSB in mode_byte instead,
  154|  		 *  and nothing ever set it back, so the selector stuck at MSB
  155|  		 *  after one access and took the record of the programmed
  156|  		 *  format with it (the test below could then never match).  A
  157|  		 *  second 16-bit write pair therefore put BOTH of its bytes in
  158|  		 *  the high half: an extra, unasked-for reprogramming, and with
  159|  		 *  a low byte of 0x00 a transient count of ZERO from a guest
  160|  		 *  that never programmed one.
  161|  		 *
  162|  		 *  Resolving the half here means the switches below can no
  163|  		 *  longer see I8253_TIMER_16BIT; their default arms still catch
  164|  		 *  a counter touched before any control word (rw == LATCH == 0).
  165|  		 */
  166|  		rw = d->mode_byte & 0x30;
  167|  		if (rw == I8253_TIMER_16BIT)
  168|  			rw = (writeflag == MEM_WRITE ? d->wr_msb[relative_addr]
  169|  			    : d->rd_msb[relative_addr]) ?
  170|  			    I8253_TIMER_MSB : I8253_TIMER_LSB;
  171|  
  172|  		if (writeflag == MEM_WRITE) {
  173|  			switch (rw) {
  174|  			case I8253_TIMER_LSB:
  175|  				d->counter[relative_addr] &= 0xff00;
  176|  				d->counter[relative_addr] |= (idata & 0xff);
  177|  				break;
  178|  			case I8253_TIMER_MSB:
  179|  				d->counter[relative_addr] &= 0x00ff;
  180|  				d->counter[relative_addr] |= ((idata&0xff)<<8);
  181|  				if (d->counter[relative_addr] != 0)
  182|  					d->hz[relative_addr] = (int) (
  183|  					    I8253_TIMER_FREQ / (float)
  184|  					    d->counter[relative_addr] + 0.5);
  185|  				else
  186|  					d->hz[relative_addr] = 0;
  187|  				debug("[ 8253: counter %i set to %i (%i Hz) "
  188|  				    "]\n", (int)relative_addr, d->counter[
  189|  				    relative_addr], d->hz[relative_addr]);
  190|  				switch (relative_addr) {
  191|  				case 0:	if (d->timer0 == NULL)
  192|  						d->timer0 = timer_add(
  193|  						    d->hz[0], timer0_tick, d);
  194|  					else
  195|  						timer_update_frequency(
  196|  						    d->timer0, d->hz[0]);
  197|  					break;
  198|+ 				case 1:	/* #pit8253flood: deleted TODO: DMA refresh? */
  199|  					break;	/*  #223: (Codex/Fable) warn+ignore, don't exit() the host  */
  200|+ 				case 2:	/* #pit8253flood: deleted TODO: 8253 tone generation? */
  201|  					break;
  202|  				}
  203|  				break;
  204|+ 			default:if (!d->latched[relative_addr]) {
  205|+ 					fatal("[ 8253: huh? writing to counter"
  206|+ 					    " %i but neither from msb nor lsb? ]\n",
  207|+ 					    (int)relative_addr);
  208|+ 				}
  209|  				break;	/*  #223: (Codex/Fable) don't exit() the host  */
  210|  			}
  211|  		} else if (d->latched[relative_addr]) {
  212|  			/*  #439: Reading a counter that the latch
  213|  			    command latched.  gxemul models this timer's
  214|  			    RATE, not a count that decrements (see the
  215|  			    TODO at the top of this file), so there is no
  216|  			    captured count to hand back.  Return 0 to say
  217|  			    so, rather than returning the reload value,
  218|  			    which would look like a count that has not
  219|  			    started -- guests divide by (reload - this).  */
  220|  			odata = 0;
  221|  
  222|  			/*
  223|  			 *  #440: CONSUME the latch.  i8254 p. 8: "the count
  224|  			 *  must be read according to the programmed format
  225|  			 *  specifically if the Counter is programmed for two
  226|  			 *  byte counts two bytes must be read"; p. 7: the
  227|  			 *  count "is held in the latch until it is read by
  228|  			 *  the CPU (or until the Counter is reprogrammed)
  229|  			 *  The count is then unlatched automatically".
  230|  			 *
  231|  			 *  So the last byte the format calls for releases it.
  232|  			 *  #439 cleared the flag only on a mode write, which
  233|  			 *  left one latch command making EVERY later read of
  234|  			 *  that counter return 0.  This byte counts against
  235|  			 *  the format, so the flip-flop below advances for it
  236|  			 *  too.
  237|  			 *
  238|  			 *  #440 pass 2, and the sentence this replaces was
  239|  			 *  MEASURED FALSE: it claimed "#439's measured
  240|  			 *  behaviour is unchanged".  Two toggles preserve the
  241|  			 *  starting phase, so a gettick() entered at EVEN read
  242|  			 *  parity is indeed a no-op -- but at ODD parity the
  243|  			 *  first read already has rw == MSB, consumes the
  244|  			 *  latch, and the second returns the live counter LSB:
  245|  			 *  0x9c00 where #439 gave 0x0000.  That is a change,
  246|  			 *  and it is the shape closer to the hardware (the
  247|  			 *  first read takes the byte the format calls for and
  248|  			 *  unlatches).  #439's reason for existing survives
  249|  			 *  either way -- the divisor is non-zero in both.
  250|  			 *
  251|  			 *  Left as a KNOWN OPEN QUESTION, not settled here: a
  252|  			 *  byte read BEFORE the latch command cannot be a byte
  253|  			 *  of the newly latched value, so consuming the latch
  254|  			 *  after one post-latch read arguably contradicts
  255|  			 *  p. 8's "two bytes must be read".  The local i8254
  256|  			 *  text does not say whether a latch command rewinds
  257|  			 *  the read flip-flop, and with no other 8253/8254
  258|  			 *  source in the tree this is an honest UNKNOWN rather
  259|  			 *  than a defect either way.  Tracked as `pitlatch2`.
  260|  			 */
  261|  			if ((d->mode_byte & 0x30) != I8253_TIMER_16BIT ||
  262|  			    rw == I8253_TIMER_MSB)
  263|  				d->latched[relative_addr] = 0;
  264|  		} else {
  265|  			switch (rw) {
  266|  			case I8253_TIMER_LSB:
  267|  				odata = d->counter[relative_addr] & 0xff;
  268|  				break;
  269|  			case I8253_TIMER_MSB:
  270|  				odata = (d->counter[relative_addr] >> 8) & 0xff;
  271|  				break;
  272|+ 			default:if (!d->latched[relative_addr]) {
  273|+ 					fatal("[ 8253: huh? reading from counter"
  274|+ 					    " %i but neither from msb nor lsb? ]\n",
  275|+ 					    (int)relative_addr);
  276|+ 				}
  277|  				break;	/*  #223: (Codex/Fable) don't exit() the host  */
  278|  			}
  279|  		}
  280|  
  281|  		/*  #440: advance the flip-flop -- ALTERNATE, never latch.  This
  282|  		    used to be `d->mode_byte &= ~I8253_TIMER_LSB', a one-way
  283|  		    clear that also destroyed the programmed format.  */
  284|  		if ((d->mode_byte & 0x30) == I8253_TIMER_16BIT) {
  285|  			if (writeflag == MEM_WRITE)
  286|  				d->wr_msb[relative_addr] ^= 1;
  287|  			else
  288|  				d->rd_msb[relative_addr] ^= 1;
  289|  		}
  290|  
  291|  		break;
  292|  
  293|  	case I8253_TIMER_MODE:
  294|  		if (writeflag == MEM_WRITE) {
  295|  			d->counter_select = (idata >> 6) & 3;
  296|  			if (d->counter_select > 2) {
  297|  				debug("[ 8253: attempt to select counter 3,"
  298|  				    " which doesn't exist. ]\n");
  299|  				d->counter_select = 0;
  300|  			}
  301|  
  302|  			/*  #439: The counter-latch command (RW == 00) latches a
  303|  			    counter so it can be read; it does NOT reprogram it, so
  304|  			    the RW format in mode_byte and the counting mode in
  305|  			    mode[] have to survive it.  Writing idata through here
  306|  			    unconditionally used to destroy both.  */
  307|  			if ((idata & 0x30) == I8253_TIMER_LATCH) {
  308|  				d->latched[d->counter_select] = 1;
  309|  				debug("[ 8253: latch counter %i ]\n",
  310|  				    d->counter_select);
  311|  				break;
  312|  			}
  313|  
  314|  			d->mode_byte = idata;
  315|  			d->latched[d->counter_select] = 0;
  316|  			d->mode[d->counter_select] = idata & 0x0e;
  317|  
  318|  			/*  #440: a Control Word programs "least significant
  319|  			    byte first then most significant byte" (i8254
  320|  			    Figure 7, RW1 RW0 = 1 1), so it rewinds this
  321|  			    counter's flip-flops.  Per counter, like the
  322|  			    hardware: Figure 8's sequences interleave control
  323|  			    words and count bytes across all three.  */
  324|  			d->rd_msb[d->counter_select] = 0;
  325|  			d->wr_msb[d->counter_select] = 0;
  326|  
  327|  			debug("[ 8253: select=%i mode=0x%x ",
  328|  			    d->counter_select, d->mode[d->counter_select]);
  329|  			if (idata & 0x30) {
  330|  				switch (idata & 0x30) {
  331|  				case I8253_TIMER_LSB:
  332|  					debug("LSB ");
  333|  					break;
  334|  				case I8253_TIMER_16BIT:
  335|  					debug("LSB+");
  336|  					// fall through
  337|  				case I8253_TIMER_MSB:
  338|  					debug("MSB ");
  339|  				}
  340|  			}
  341|  			debug("]\n");
  342|  
  343|  			if (idata & I8253_TIMER_BCD) {
  344|  				/*  #223: (Codex/Fable) warn+ignore BCD mode instead of
  345|  				    exit()ing the host.  */
  346|+ 				if (!d->latched[d->counter_select]) {
  347|+ 					fatal("[ 8253: BCD not yet implemented ]\n");
  348|+ 				}
  349|  			}
  350|  		} else {
  351|  			debug("[ 8253: read; can this actually happen? ]\n");
  352|  			odata = d->mode_byte;
  353|  		}
  354|  		break;
  355|  
  356|+ 	default:/* #pit8253flood: deleted dead code */
  357|  		break;	/*  #223: (Codex/Fable) warn+ignore, don't exit() the host  */
  358|  	}
  359|  
  360|  	if (writeflag == MEM_READ)
  361|  		memory_writemax64(cpu, data, len, odata);
  362|  
  363|  	return 1;
  364|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_PIT8253FLOOD: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_PIT8253FLOOD: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
