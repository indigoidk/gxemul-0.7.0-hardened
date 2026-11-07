# GXemul hardened fork -- DRAFT A FIX for one filed issue, `pit8253lsbnotimer` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `pit8253lsbnotimer`, state `open`, severity `MED-HIGH`)

**title:** dev_8253.c one-byte formats: BOTH arms keep the other byte stale against the datasheet, and the LSB arm additionally installs no timer -- wrong host rate on counter 0

**state_note (head):**

filed 2026-09-17 by the kimi-k3 seat, WIDENED the same day by Fable 5.1's adjudication from a datasheet passage I read past

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- The model incorrectly keeps stale bytes in both one-byte arms against the datasheet.

## The code at the cited lines

### `src/devices/dev_8253.c` around the row's cited line 175 (HEAD 2d25df65, lines 130-220)

```c
  130| 
  131| 
  132| DEVICE_ACCESS(8253)
  133| {
  134| 	struct pit8253_data *d = (struct pit8253_data *) extra;
  135| 	uint64_t idata = 0, odata = 0;
  136| 	int rw = 0;		/*  #440: the half THIS access refers to  */
  137| 
  138| 	if (writeflag == MEM_WRITE)
  139| 		idata = memory_readmax64(cpu, data, len);
  140| 
  141| 	d->in_use = 1;
  142| 
  143| 	switch (relative_addr) {
  144| 
  145| 	case I8253_TIMER_CNTR0:
  146| 	case I8253_TIMER_CNTR1:
  147| 	case I8253_TIMER_CNTR2:
  148| 		/*
  149| 		 *  #440: in the 16-bit format it is the counter's read/write
  150| 		 *  flip-flop -- not mode_byte -- that says which half an access
  151| 		 *  refers to, and it ALTERNATES: LSB, MSB, LSB, ...
  152| 		 *
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

End with one line: `FIXDRAFT_PIT8253LSBNOTIMER: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
