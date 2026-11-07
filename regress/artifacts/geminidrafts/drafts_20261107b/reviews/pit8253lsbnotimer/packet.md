# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `pit8253lsbnotimer` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `pit8253lsbnotimer`, state `open`)

**title:** dev_8253.c one-byte formats: BOTH arms keep the other byte stale against the datasheet, and the LSB arm additionally installs no timer -- wrong host rate on counter 0

**state_note (head):** filed 2026-09-17 by the kimi-k3 seat, WIDENED the same day by Fable 5.1's adjudication from a datasheet passage I read past

**The drafter's own reading:** STILL PRESENT: YES -- `src/devices/dev_8253.c:188` (timer setup runs for invalid `rw` values).

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_8253.c b/src/devices/dev_8253.c
index 9e756933..59bb0988 100644
--- a/src/devices/dev_8253.c
+++ b/src/devices/dev_8253.c
@@ -172,12 +172,25 @@ DEVICE_ACCESS(8253)
 		if (writeflag == MEM_WRITE) {
 			switch (rw) {
 			case I8253_TIMER_LSB:
-				d->counter[relative_addr] &= 0xff00;
-				d->counter[relative_addr] |= (idata & 0xff);
+				if ((d->mode_byte & 0x30) == I8253_TIMER_LSB)
+					d->counter[relative_addr] = (idata & 0xff);
+				else
+					d->counter[relative_addr] = (d->counter[relative_addr] & 0xff00) | (idata & 0xff);
 				break;
 			case I8253_TIMER_MSB:
-				d->counter[relative_addr] &= 0x00ff;
-				d->counter[relative_addr] |= ((idata&0xff)<<8);
+				if ((d->mode_byte & 0x30) == I8253_TIMER_MSB)
+					d->counter[relative_addr] = ((idata & 0xff) << 8);
+				else
+					d->counter[relative_addr] = (d->counter[relative_addr] & 0x00ff) | ((idata & 0xff) << 8);
+				break;
+			default:fatal("[ 8253: huh? writing to counter"
+				    " %i but neither from msb nor lsb? ]\n",
+				    (int)relative_addr);
+				break;	/*  #223: (Codex/Fable) don't exit() the host  */
+			}
+
+			if (rw == I8253_TIMER_LSB || rw == I8253_TIMER_MSB) {
+				/* #442: Setup timer for all write formats */
 				if (d->counter[relative_addr] != 0)
 					d->hz[relative_addr] = (int) (
 					    I8253_TIMER_FREQ / (float)
@@ -200,11 +213,6 @@ DEVICE_ACCESS(8253)
 				case 2:	fatal("TODO: 8253 tone generation?\n");
 					break;
 				}
-				break;
-			default:fatal("[ 8253: huh? writing to counter"
-				    " %i but neither from msb nor lsb? ]\n",
-				    (int)relative_addr);
-				break;	/*  #223: (Codex/Fable) don't exit() the host  */
 			}
 		} else if (d->latched[relative_addr]) {
 			/*  #439: Reading a counter that the latch
```

## Every edited function, after the fix

### `src/devices/dev_8253.c` -- post-edit lines 132-372 (`+` marks a line the diff added or the point of a deletion)

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
  175|+ 				if ((d->mode_byte & 0x30) == I8253_TIMER_LSB)
  176|+ 					d->counter[relative_addr] = (idata & 0xff);
  177|+ 				else
  178|+ 					d->counter[relative_addr] = (d->counter[relative_addr] & 0xff00) | (idata & 0xff);
  179|  				break;
  180|  			case I8253_TIMER_MSB:
  181|+ 				if ((d->mode_byte & 0x30) == I8253_TIMER_MSB)
  182|+ 					d->counter[relative_addr] = ((idata & 0xff) << 8);
  183|+ 				else
  184|+ 					d->counter[relative_addr] = (d->counter[relative_addr] & 0x00ff) | ((idata & 0xff) << 8);
  185|+ 				break;
  186|+ 			default:fatal("[ 8253: huh? writing to counter"
  187|+ 				    " %i but neither from msb nor lsb? ]\n",
  188|+ 				    (int)relative_addr);
  189|+ 				break;	/*  #223: (Codex/Fable) don't exit() the host  */
  190|+ 			}
  191|+ 
  192|+ 			if (rw == I8253_TIMER_LSB || rw == I8253_TIMER_MSB) {
  193|+ 				/* #442: Setup timer for all write formats */
  194|  				if (d->counter[relative_addr] != 0)
  195|  					d->hz[relative_addr] = (int) (
  196|  					    I8253_TIMER_FREQ / (float)
  197|  					    d->counter[relative_addr] + 0.5);
  198|  				else
  199|  					d->hz[relative_addr] = 0;
  200|  				debug("[ 8253: counter %i set to %i (%i Hz) "
  201|  				    "]\n", (int)relative_addr, d->counter[
  202|  				    relative_addr], d->hz[relative_addr]);
  203|  				switch (relative_addr) {
  204|  				case 0:	if (d->timer0 == NULL)
  205|  						d->timer0 = timer_add(
  206|  						    d->hz[0], timer0_tick, d);
  207|  					else
  208|  						timer_update_frequency(
  209|  						    d->timer0, d->hz[0]);
  210|  					break;
  211|  				case 1:	fatal("TODO: DMA refresh?\n");
  212|  					break;	/*  #223: (Codex/Fable) warn+ignore, don't exit() the host  */
  213|  				case 2:	fatal("TODO: 8253 tone generation?\n");
  214|  					break;
  215|  				}
  216|+ 			}
  217|  		} else if (d->latched[relative_addr]) {
  218|  			/*  #439: Reading a counter that the latch
  219|  			    command latched.  gxemul models this timer's
  220|  			    RATE, not a count that decrements (see the
  221|  			    TODO at the top of this file), so there is no
  222|  			    captured count to hand back.  Return 0 to say
  223|  			    so, rather than returning the reload value,
  224|  			    which would look like a count that has not
  225|  			    started -- guests divide by (reload - this).  */
  226|  			odata = 0;
  227|  
  228|  			/*
  229|  			 *  #440: CONSUME the latch.  i8254 p. 8: "the count
  230|  			 *  must be read according to the programmed format
  231|  			 *  specifically if the Counter is programmed for two
  232|  			 *  byte counts two bytes must be read"; p. 7: the
  233|  			 *  count "is held in the latch until it is read by
  234|  			 *  the CPU (or until the Counter is reprogrammed)
  235|  			 *  The count is then unlatched automatically".
  236|  			 *
  237|  			 *  So the last byte the format calls for releases it.
  238|  			 *  #439 cleared the flag only on a mode write, which
  239|  			 *  left one latch command making EVERY later read of
  240|  			 *  that counter return 0.  This byte counts against
  241|  			 *  the format, so the flip-flop below advances for it
  242|  			 *  too.
  243|  			 *
  244|  			 *  #440 pass 2, and the sentence this replaces was
  245|  			 *  MEASURED FALSE: it claimed "#439's measured
  246|  			 *  behaviour is unchanged".  Two toggles preserve the
  247|  			 *  starting phase, so a gettick() entered at EVEN read
  248|  			 *  parity is indeed a no-op -- but at ODD parity the
  249|  			 *  first read already has rw == MSB, consumes the
  250|  			 *  latch, and the second returns the live counter LSB:
  251|  			 *  0x9c00 where #439 gave 0x0000.  That is a change,
  252|  			 *  and it is the shape closer to the hardware (the
  253|  			 *  first read takes the byte the format calls for and
  254|  			 *  unlatches).  #439's reason for existing survives
  255|  			 *  either way -- the divisor is non-zero in both.
  256|  			 *
  257|  			 *  Left as a KNOWN OPEN QUESTION, not settled here: a
  258|  			 *  byte read BEFORE the latch command cannot be a byte
  259|  			 *  of the newly latched value, so consuming the latch
  260|  			 *  after one post-latch read arguably contradicts
  261|  			 *  p. 8's "two bytes must be read".  The local i8254
  262|  			 *  text does not say whether a latch command rewinds
  263|  			 *  the read flip-flop, and with no other 8253/8254
  264|  			 *  source in the tree this is an honest UNKNOWN rather
  265|  			 *  than a defect either way.  Tracked as `pitlatch2`.
  266|  			 */
  267|  			if ((d->mode_byte & 0x30) != I8253_TIMER_16BIT ||
  268|  			    rw == I8253_TIMER_MSB)
  269|  				d->latched[relative_addr] = 0;
  270|  		} else {
  271|  			switch (rw) {
  272|  			case I8253_TIMER_LSB:
  273|  				odata = d->counter[relative_addr] & 0xff;
  274|  				break;
  275|  			case I8253_TIMER_MSB:
  276|  				odata = (d->counter[relative_addr] >> 8) & 0xff;
  277|  				break;
  278|  			default:fatal("[ 8253: huh? reading from counter"
  279|  				    " %i but neither from msb nor lsb? ]\n",
  280|  				    (int)relative_addr);
  281|  				break;	/*  #223: (Codex/Fable) don't exit() the host  */
  282|  			}
  283|  		}
  284|  
  285|  		/*  #440: advance the flip-flop -- ALTERNATE, never latch.  This
  286|  		    used to be `d->mode_byte &= ~I8253_TIMER_LSB', a one-way
  287|  		    clear that also destroyed the programmed format.  */
  288|  		if ((d->mode_byte & 0x30) == I8253_TIMER_16BIT) {
  289|  			if (writeflag == MEM_WRITE)
  290|  				d->wr_msb[relative_addr] ^= 1;
  291|  			else
  292|  				d->rd_msb[relative_addr] ^= 1;
  293|  		}
  294|  
  295|  		break;
  296|  
  297|  	case I8253_TIMER_MODE:
  298|  		if (writeflag == MEM_WRITE) {
  299|  			d->counter_select = (idata >> 6) & 3;
  300|  			if (d->counter_select > 2) {
  301|  				debug("[ 8253: attempt to select counter 3,"
  302|  				    " which doesn't exist. ]\n");
  303|  				d->counter_select = 0;
  304|  			}
  305|  
  306|  			/*  #439: The counter-latch command (RW == 00) latches a
  307|  			    counter so it can be read; it does NOT reprogram it, so
  308|  			    the RW format in mode_byte and the counting mode in
  309|  			    mode[] have to survive it.  Writing idata through here
  310|  			    unconditionally used to destroy both.  */
  311|  			if ((idata & 0x30) == I8253_TIMER_LATCH) {
  312|  				d->latched[d->counter_select] = 1;
  313|  				debug("[ 8253: latch counter %i ]\n",
  314|  				    d->counter_select);
  315|  				break;
  316|  			}
  317|  
  318|  			d->mode_byte = idata;
  319|  			d->latched[d->counter_select] = 0;
  320|  			d->mode[d->counter_select] = idata & 0x0e;
  321|  
  322|  			/*  #440: a Control Word programs "least significant
  323|  			    byte first then most significant byte" (i8254
  324|  			    Figure 7, RW1 RW0 = 1 1), so it rewinds this
  325|  			    counter's flip-flops.  Per counter, like the
  326|  			    hardware: Figure 8's sequences interleave control
  327|  			    words and count bytes across all three.  */
  328|  			d->rd_msb[d->counter_select] = 0;
  329|  			d->wr_msb[d->counter_select] = 0;
  330|  
  331|  			debug("[ 8253: select=%i mode=0x%x ",
  332|  			    d->counter_select, d->mode[d->counter_select]);
  333|  			if (idata & 0x30) {
  334|  				switch (idata & 0x30) {
  335|  				case I8253_TIMER_LSB:
  336|  					debug("LSB ");
  337|  					break;
  338|  				case I8253_TIMER_16BIT:
  339|  					debug("LSB+");
  340|  					// fall through
  341|  				case I8253_TIMER_MSB:
  342|  					debug("MSB ");
  343|  				}
  344|  			}
  345|  			debug("]\n");
  346|  
  347|  			if (idata & I8253_TIMER_BCD) {
  348|  				/*  #223: (Codex/Fable) warn+ignore BCD mode instead of
  349|  				    exit()ing the host.  */
  350|  				fatal("[ 8253: BCD not yet implemented ]\n");
  351|  			}
  352|  		} else {
  353|  			debug("[ 8253: read; can this actually happen? ]\n");
  354|  			odata = d->mode_byte;
  355|  		}
  356|  		break;
  357|  
  358|  	default:if (writeflag == MEM_WRITE) {
  359|  			fatal("[ 8253: unimplemented write to address 0x%x"
  360|  			    " data=0x%02x ]\n", (int)relative_addr, (int)idata);
  361|  		} else {
  362|  			fatal("[ 8253: unimplemented read from address 0x%x "
  363|  			    "]\n", (int)relative_addr);
  364|  		}
  365|  		break;	/*  #223: (Codex/Fable) warn+ignore, don't exit() the host  */
  366|  	}
  367|  
  368|  	if (writeflag == MEM_READ)
  369|  		memory_writemax64(cpu, data, len, odata);
  370|  
  371|  	return 1;
  372|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_PIT8253LSBNOTIMER: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_PIT8253LSBNOTIMER: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
