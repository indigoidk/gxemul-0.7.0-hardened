# GXemul hardened fork -- DRAFT A FIX for one filed issue, `pit8253flood` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `pit8253flood`, state `open`, severity `MED`)

**title:** pit8253flood  dev_8253.c: bound every unconditional emission in DEVICE_ACCESS(8253) -- LATCH :204/:270/:342, DELETE :198/:200, :351/:354 are dead code

**state_note (head):**

pass 1 complete 2026-09-17, nine seats + Fable adjudication.  STAYS FIRST in the queue -- Fable ruled the panel's demotion wrong, on reach, with owner sequencing breaking a severity tie.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- Latch :342 to prevent unbounded fatal.

## The code at the cited lines

### `src/devices/dev_8253.c` around the row's cited line 198 (HEAD 2d25df65, lines 153-243)

```c
  153| 		 *  The old code cleared I8253_TIMER_LSB in mode_byte instead,
  154| 		 *  and nothing ever set it back, so the selector stuck at MSB
  155| 		 *  after one access and took the record of the programmed
  156| 		 *  format with it (the test below could then never match).  A
  157| 		 *  second 16-bit write pair therefore put BOTH of its bytes in
  158| 		 *  the high half: an extra, unasked-for reprogramming, and with
  159| 		 *  a low byte of 0x00 a transient count of ZERO from a guest
  160| 		 *  that never programmed one.
  161| 		 *
  162| 		 *  Resolving the half here means the switches below can no
  163| 		 *  longer see I8253_TIMER_16BIT; their default arms still catch
  164| 		 *  a counter touched before any control word (rw == LATCH == 0).
  165| 		 */
  166| 		rw = d->mode_byte & 0x30;
  167| 		if (rw == I8253_TIMER_16BIT)
  168| 			rw = (writeflag == MEM_WRITE ? d->wr_msb[relative_addr]
  169| 			    : d->rd_msb[relative_addr]) ?
  170| 			    I8253_TIMER_MSB : I8253_TIMER_LSB;
  171| 
  172| 		if (writeflag == MEM_WRITE) {
  173| 			switch (rw) {
  174| 			case I8253_TIMER_LSB:
  175| 				d->counter[relative_addr] &= 0xff00;
  176| 				d->counter[relative_addr] |= (idata & 0xff);
  177| 				break;
  178| 			case I8253_TIMER_MSB:
  179| 				d->counter[relative_addr] &= 0x00ff;
  180| 				d->counter[relative_addr] |= ((idata&0xff)<<8);
  181| 				if (d->counter[relative_addr] != 0)
  182| 					d->hz[relative_addr] = (int) (
  183| 					    I8253_TIMER_FREQ / (float)
  184| 					    d->counter[relative_addr] + 0.5);
  185| 				else
  186| 					d->hz[relative_addr] = 0;
  187| 				debug("[ 8253: counter %i set to %i (%i Hz) "
  188| 				    "]\n", (int)relative_addr, d->counter[
  189| 				    relative_addr], d->hz[relative_addr]);
  190| 				switch (relative_addr) {
  191| 				case 0:	if (d->timer0 == NULL)
  192| 						d->timer0 = timer_add(
  193| 						    d->hz[0], timer0_tick, d);
  194| 					else
  195| 						timer_update_frequency(
  196| 						    d->timer0, d->hz[0]);
  197| 					break;
  198| 				case 1:	fatal("TODO: DMA refresh?\n");
  199| 					break;	/*  #223: (Codex/Fable) warn+ignore, don't exit() the host  */
  200| 				case 2:	fatal("TODO: 8253 tone generation?\n");
  201| 					break;
  202| 				}
  203| 				break;
  204| 			default:fatal("[ 8253: huh? writing to counter"
  205| 				    " %i but neither from msb nor lsb? ]\n",
  206| 				    (int)relative_addr);
  207| 				break;	/*  #223: (Codex/Fable) don't exit() the host  */
  208| 			}
  209| 		} else if (d->latched[relative_addr]) {
  210| 			/*  #439: Reading a counter that the latch
  211| 			    command latched.  gxemul models this timer's
  212| 			    RATE, not a count that decrements (see the
  213| 			    TODO at the top of this file), so there is no
  214| 			    captured count to hand back.  Return 0 to say
  215| 			    so, rather than returning the reload value,
  216| 			    which would look like a count that has not
  217| 			    started -- guests divide by (reload - this).  */
  218| 			odata = 0;
  219| 
  220| 			/*
  221| 			 *  #440: CONSUME the latch.  i8254 p. 8: "the count
  222| 			 *  must be read according to the programmed format
  223| 			 *  specifically if the Counter is programmed for two
  224| 			 *  byte counts two bytes must be read"; p. 7: the
  225| 			 *  count "is held in the latch until it is read by
  226| 			 *  the CPU (or until the Counter is reprogrammed)
  227| 			 *  The count is then unlatched automatically".
  228| 			 *
  229| 			 *  So the last byte the format calls for releases it.
  230| 			 *  #439 cleared the flag only on a mode write, which
  231| 			 *  left one latch command making EVERY later read of
  232| 			 *  that counter return 0.  This byte counts against
  233| 			 *  the format, so the flip-flop below advances for it
  234| 			 *  too.
  235| 			 *
  236| 			 *  #440 pass 2, and the sentence this replaces was
  237| 			 *  MEASURED FALSE: it claimed "#439's measured
  238| 			 *  behaviour is unchanged".  Two toggles preserve the
  239| 			 *  starting phase, so a gettick() entered at EVEN read
  240| 			 *  parity is indeed a no-op -- but at ODD parity the
  241| 			 *  first read already has rw == MSB, consumes the
  242| 			 *  latch, and the second returns the live counter LSB:
  243| 			 *  0x9c00 where #439 gave 0x0000.  That is a change,
```

## WHAT TO RETURN

1. One line: `STILL PRESENT: YES|NO|UNSETTLED -- <the line of code shown that shows it>`.  The cited line numbers may have
   moved since the row was written; judge from the code shown.  If NO, say what already fixed it and STOP (no edits).
2. If YES: EXACTLY ONE fenced ```json block -- a list of edits, the smallest fix that removes the defect without changing any
   other behaviour: [{"file": "src/...", "old": "<exact text from the code above, without the line-number prefix; it must occur
   EXACTLY ONCE in that file>", "new": "<replacement>", "why": "<one line>"}].  Use JSON escapes (\t, \n).  Tabs stay tabs;
   lines within 79 columns; tag a new comment `/* #NNN: ... */`.  Prefer the file's existing idioms (a decline, a once-per-
   device announce, a clamp) over new machinery.
3. After the block: what the fix deliberately does NOT change, and anything you could not settle from the code shown.

End with one line: `FIXDRAFT_PIT8253FLOOD: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
