# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `pit8253flood` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `pit8253flood`, state `open`)

**title:** pit8253flood  dev_8253.c: bound every unconditional emission in DEVICE_ACCESS(8253) -- LATCH :204/:270/:342, DELETE :198/:200, :351/:354 are dead code

**state_note (head):** pass 1 complete 2026-09-17, nine seats + Fable adjudication.  STAYS FIRST in the queue -- Fable ruled the panel's demotion wrong, on reach, with owner sequencing breaking a severity tie.

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/devices/dev_8253.c` -- AT HEAD, lines 132-364 (`*` marks a line your previous draft changed)

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
  198|* 				case 1:	fatal("TODO: DMA refresh?\n");
  199|* 					break;	/*  #223: (Codex/Fable) warn+ignore, don't exit() the host  */
  200|* 				case 2:	fatal("TODO: 8253 tone generation?\n");
  201|* 					break;
  202|  				}
  203|  				break;
  204|* 			default:fatal("[ 8253: huh? writing to counter"
  205|* 				    " %i but neither from msb nor lsb? ]\n",
  206|* 				    (int)relative_addr);
  207|* 				break;	/*  #223: (Codex/Fable) don't exit() the host  */
  208|  			}
  209|  		} else if (d->latched[relative_addr]) {
  210|  			/*  #439: Reading a counter that the latch
  211|  			    command latched.  gxemul models this timer's
  212|  			    RATE, not a count that decrements (see the
  213|  			    TODO at the top of this file), so there is no
  214|  			    captured count to hand back.  Return 0 to say
  215|  			    so, rather than returning the reload value,
  216|  			    which would look like a count that has not
  217|  			    started -- guests divide by (reload - this).  */
  218|  			odata = 0;
  219|  
  220|  			/*
  221|  			 *  #440: CONSUME the latch.  i8254 p. 8: "the count
  222|  			 *  must be read according to the programmed format
  223|  			 *  specifically if the Counter is programmed for two
  224|  			 *  byte counts two bytes must be read"; p. 7: the
  225|  			 *  count "is held in the latch until it is read by
  226|  			 *  the CPU (or until the Counter is reprogrammed)
  227|  			 *  The count is then unlatched automatically".
  228|  			 *
  229|  			 *  So the last byte the format calls for releases it.
  230|  			 *  #439 cleared the flag only on a mode write, which
  231|  			 *  left one latch command making EVERY later read of
  232|  			 *  that counter return 0.  This byte counts against
  233|  			 *  the format, so the flip-flop below advances for it
  234|  			 *  too.
  235|  			 *
  236|  			 *  #440 pass 2, and the sentence this replaces was
  237|  			 *  MEASURED FALSE: it claimed "#439's measured
  238|  			 *  behaviour is unchanged".  Two toggles preserve the
  239|  			 *  starting phase, so a gettick() entered at EVEN read
  240|  			 *  parity is indeed a no-op -- but at ODD parity the
  241|  			 *  first read already has rw == MSB, consumes the
  242|  			 *  latch, and the second returns the live counter LSB:
  243|  			 *  0x9c00 where #439 gave 0x0000.  That is a change,
  244|  			 *  and it is the shape closer to the hardware (the
  245|  			 *  first read takes the byte the format calls for and
  246|  			 *  unlatches).  #439's reason for existing survives
  247|  			 *  either way -- the divisor is non-zero in both.
  248|  			 *
  249|  			 *  Left as a KNOWN OPEN QUESTION, not settled here: a
  250|  			 *  byte read BEFORE the latch command cannot be a byte
  251|  			 *  of the newly latched value, so consuming the latch
  252|  			 *  after one post-latch read arguably contradicts
  253|  			 *  p. 8's "two bytes must be read".  The local i8254
  254|  			 *  text does not say whether a latch command rewinds
  255|  			 *  the read flip-flop, and with no other 8253/8254
  256|  			 *  source in the tree this is an honest UNKNOWN rather
  257|  			 *  than a defect either way.  Tracked as `pitlatch2`.
  258|  			 */
  259|  			if ((d->mode_byte & 0x30) != I8253_TIMER_16BIT ||
  260|  			    rw == I8253_TIMER_MSB)
  261|  				d->latched[relative_addr] = 0;
  262|  		} else {
  263|  			switch (rw) {
  264|  			case I8253_TIMER_LSB:
  265|  				odata = d->counter[relative_addr] & 0xff;
  266|  				break;
  267|  			case I8253_TIMER_MSB:
  268|  				odata = (d->counter[relative_addr] >> 8) & 0xff;
  269|  				break;
  270|  			default:fatal("[ 8253: huh? reading from counter"
  271|  				    " %i but neither from msb nor lsb? ]\n",
  272|  				    (int)relative_addr);
  273|  				break;	/*  #223: (Codex/Fable) don't exit() the host  */
  274|  			}
  275|  		}
  276|  
  277|  		/*  #440: advance the flip-flop -- ALTERNATE, never latch.  This
  278|  		    used to be `d->mode_byte &= ~I8253_TIMER_LSB', a one-way
  279|  		    clear that also destroyed the programmed format.  */
  280|  		if ((d->mode_byte & 0x30) == I8253_TIMER_16BIT) {
  281|  			if (writeflag == MEM_WRITE)
  282|  				d->wr_msb[relative_addr] ^= 1;
  283|  			else
  284|  				d->rd_msb[relative_addr] ^= 1;
  285|  		}
  286|  
  287|  		break;
  288|  
  289|  	case I8253_TIMER_MODE:
  290|  		if (writeflag == MEM_WRITE) {
  291|  			d->counter_select = (idata >> 6) & 3;
  292|  			if (d->counter_select > 2) {
  293|  				debug("[ 8253: attempt to select counter 3,"
  294|  				    " which doesn't exist. ]\n");
  295|  				d->counter_select = 0;
  296|  			}
  297|  
  298|  			/*  #439: The counter-latch command (RW == 00) latches a
  299|  			    counter so it can be read; it does NOT reprogram it, so
  300|  			    the RW format in mode_byte and the counting mode in
  301|  			    mode[] have to survive it.  Writing idata through here
  302|  			    unconditionally used to destroy both.  */
  303|  			if ((idata & 0x30) == I8253_TIMER_LATCH) {
  304|  				d->latched[d->counter_select] = 1;
  305|  				debug("[ 8253: latch counter %i ]\n",
  306|  				    d->counter_select);
  307|  				break;
  308|  			}
  309|  
  310|  			d->mode_byte = idata;
  311|  			d->latched[d->counter_select] = 0;
  312|  			d->mode[d->counter_select] = idata & 0x0e;
  313|  
  314|  			/*  #440: a Control Word programs "least significant
  315|  			    byte first then most significant byte" (i8254
  316|  			    Figure 7, RW1 RW0 = 1 1), so it rewinds this
  317|  			    counter's flip-flops.  Per counter, like the
  318|  			    hardware: Figure 8's sequences interleave control
  319|  			    words and count bytes across all three.  */
  320|  			d->rd_msb[d->counter_select] = 0;
  321|  			d->wr_msb[d->counter_select] = 0;
  322|  
  323|  			debug("[ 8253: select=%i mode=0x%x ",
  324|  			    d->counter_select, d->mode[d->counter_select]);
  325|  			if (idata & 0x30) {
  326|  				switch (idata & 0x30) {
  327|  				case I8253_TIMER_LSB:
  328|  					debug("LSB ");
  329|  					break;
  330|  				case I8253_TIMER_16BIT:
  331|  					debug("LSB+");
  332|  					// fall through
  333|  				case I8253_TIMER_MSB:
  334|  					debug("MSB ");
  335|  				}
  336|  			}
  337|  			debug("]\n");
  338|  
  339|  			if (idata & I8253_TIMER_BCD) {
  340|  				/*  #223: (Codex/Fable) warn+ignore BCD mode instead of
  341|  				    exit()ing the host.  */
  342|  				fatal("[ 8253: BCD not yet implemented ]\n");
  343|  			}
  344|  		} else {
  345|  			debug("[ 8253: read; can this actually happen? ]\n");
  346|  			odata = d->mode_byte;
  347|  		}
  348|  		break;
  349|  
  350|  	default:if (writeflag == MEM_WRITE) {
  351|  			fatal("[ 8253: unimplemented write to address 0x%x"
  352|  			    " data=0x%02x ]\n", (int)relative_addr, (int)idata);
  353|  		} else {
  354|  			fatal("[ 8253: unimplemented read from address 0x%x "
  355|  			    "]\n", (int)relative_addr);
  356|  		}
  357|  		break;	/*  #223: (Codex/Fable) warn+ignore, don't exit() the host  */
  358|  	}
  359|  
  360|  	if (writeflag == MEM_READ)
  361|  		memory_writemax64(cpu, data, len, odata);
  362|  
  363|  	return 1;
  364|  }
```

## The data structures those files define (every field that exists)

### `src/devices/dev_8253.c` -- `struct pit8253_data {` (HEAD lines 74-106)

```c
   74| struct pit8253_data {
   75| 	int		in_use;
   76| 
   77| 	int		counter_select;
   78| 	uint8_t		mode_byte;
   79| 
   80| 	int		mode[3];
   81| 	int		counter[3];
   82| 	int		latched[3];	/*  #439: latch command pending  */
   83| 
   84| 	/*
   85| 	 *  #440: the read/write flip-flops.  1 means "the MSB is the half the
   86| 	 *  next access refers to".  READS AND WRITES GET SEPARATE ONES -- and
   87| 	 *  that is INFERRED from an observable sequence, not quoted: the local
   88| 	 *  i8254 text never uses the phrase "read/write flip-flop" at all (its
   89| 	 *  only "flip-flop" hits are the GATE edge detector).  What it does
   90| 	 *  give, at _scratchpad/i8254.txt p. 8, is
   91| 	 *
   92| 	 *	1) Read least significant byte	2) Write new least significant byte
   93| 	 *	3) Read most significant byte	4) Write new most significant byte
   94| 	 *
   95| 	 *  as a valid sequence, and one shared flip-flop cannot produce it --
   96| 	 *  step 1 would advance it past step 2's LSB.
   97| 	 */
   98| 	int		rd_msb[3];
   99| 	int		wr_msb[3];
  100| 
  101| 	int		hz[3];
  102| 
  103| 	struct timer	*timer0;
  104| 	struct interrupt irq;
  105| 	int		pending_interrupts_timer0;
  106| };
```


## Your previous draft's edits

```json
[
  {
    "file": "src/devices/dev_8253.c",
    "old": "\t\t\t\tcase 1:\tfatal(\"TODO: DMA refresh?\\n\");\n\t\t\t\t\tbreak;\t/*  #223: (Codex/Fable) warn+ignore, don't exit() the host  */\n\t\t\t\tcase 2:\tfatal(\"TODO: 8253 tone generation?\\n\");\n\t\t\t\t\tbreak;",
    "new": "\t\t\t\tcase 1:\t/* TODO: DMA refresh? */\n\t\t\t\t\tbreak;\t/*  #223: (Codex/Fable) warn+ignore, don't exit() the host  */\n\t\t\t\tcase 2:\t/* TODO: 8253 tone generation? */\n\t\t\t\t\tbreak;",
    "why": "Delete unconditional emissions at 198 and 200."
  },
  {
    "file": "src/devices/dev_8253.c",
    "old": "\t\t\tdefault:fatal(\"[ 8253: huh? writing to counter\"\n\t\t\t\t    \" %i but neither from msb nor lsb? ]\\n\",\n\t\t\t\t    (int)relative_addr);\n\t\t\t\tbreak;\t/*  #223: (Codex/Fable) don't exit() the host  */",
    "new": "\t\t\tdefault:\n\t\t\t\tif (!d->latched[relative_addr]) { /* latched warning */\n\t\t\t\t\tfatal(\"[ 8253: huh? writing to counter\"\n\t\t\t\t\t    \" %i but neither from msb nor lsb? ]\\n\",\n\t\t\t\t\t    (int)relative_addr);\n\t\t\t\t}\n\t\t\t\tbreak;\t/*  #223: (Codex/Fable) don't exit() the host  */",
    "why": "Latch emission at 204."
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_PIT8253FLOOD: DEFECT, 4 FINDINGS
1. The diff fails to remove the defect at every site named in the issue. It successfully applies DELETE to :198 and :200, and applies LATCH to :204 (post-edit `src/devices/dev_8253.c:206`). However, it misses the LATCH bounds for :270 (post-edit `src/devices/dev_8253.c:273`) and :342 (post-edit `src/devices/dev_8253.c:345`), and misses the DELETE for :351/:354 (post-edit `src/devices/dev_8253.c:353` and `:356`).
2. CONTROL FLOW: No added `return`, `goto`, `break`, or early exit skips any code. The function will still safely reach its common tail at `src/devices/dev_8253.c:363` (`if (writeflag == MEM_READ) memory_writemax64(...)`) and return.
3. RETURN VALUE: No path returns a different value. Paths that previously called `fatal()` and exited the host now fall through and return `1` (which implies the access was successfully handled/ignored).
4. WHAT ELSE: Nothing else is functionally changed; bounding and removing `fatal()` calls simply prevents the emulator from crashing on these malformed guest inputs.
5. HOUSE IDIOMS: The added code violates house style by missing a ticket tag in the new comment, and by not implementing the `(once)` idiom for the retained `fatal` emission.
src/devices/dev_8253.c:273 DEFECT missed LATCH bounding on read default. Fix: `if (!d->latched[relative_addr]) fatal(...);`
src/devices/dev_8253.c:354 DEFECT missed DELETE of dead code. Fix: `/* deleted dead code */`
src/devices/dev_8253.c:205 STYLE missing issue tag in new comment. Fix: `/* #pit8253flood: latched warning */`
src/devices/dev_8253.c:206 STYLE diagnostic lacks `(once)`. Fix: `fatal("[ 8253: (once) huh? writing to counter...");`
```

## WHAT TO RETURN

1. For EACH review finding, one line: `ACCEPT` or `REJECT`, and why, citing the code shown.  A suggestion that uses a
   function, macro or field that appears nowhere in this packet does not exist in HEAD: reject it or replace it with an
   idiom the packet shows.
2. One line: `STILL PRESENT: YES|NO|UNSETTLED -- <the line of code that shows it>`.
3. If YES: EXACTLY ONE fenced ```json block -- the COMPLETE corrected edit list (not a delta), applying to the HEAD text
   above: [{"file": "src/...", "old": "<exact HEAD text, occurring EXACTLY ONCE in that file>", "new": "<replacement>",
   "why": "<one line>"}].  JSON escapes (\t, \n); tabs stay tabs; lines within 79 columns; a new comment carries
   `/* #NNN: ... */`.  Never an empty list and never comment-only edits for a defect in behaviour.  If every finding is
   rejected, return the previous edits unchanged.
4. After the block: what the fix deliberately does not change.

End with two lines: `REVISION_PIT8253FLOOD: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_PIT8253FLOOD: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
