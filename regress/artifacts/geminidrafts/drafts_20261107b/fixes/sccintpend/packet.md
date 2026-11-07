# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `sccintpend` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `sccintpend`, state `open`)

**title:** devices/dev_scc.c -- RR3 and data reads clear all interrupt-pending bits, one WR1 governs both channels, special-condition-only mode interrupts per character, WR9 is stored per channel -- WRONG-RESULT

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T69 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: medium; report rows: A2-30).  Source URLs: https://github.com/rpajarola/gxemul/commit/2dfd6ec32be07d7dd38a707f66742de3e2023ed3, https://github.com/rpajarola/gxemul/commit/7aeae85458685ce7628f0ca5b6bcf9ebe611f393, https://github.com/rpajarola/gxemul/commit/a99af56307177bf32c0e789360fb36212b47225f.  Our site at de8c7547: src/devices/dev_scc.c:379-388, :432-435, :215-216, :201, :454.  Portable fix: yes -- port rpajarola 2dfd6ec, rpajarola 7aeae85, rpajarola a99af56.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/devices/dev_scc.c` -- AT HEAD, lines 319-487 (`*` marks a line your previous draft changed)

```c
  319|  DEVICE_ACCESS(scc)
  320|  {
  321|  	struct scc_data *d = (struct scc_data *) extra;
  322|  	uint64_t idata = 0, odata = 0;
  323|  	int port;
  324|  	int ultrix_mode = 0;
  325|  
  326|  	if (writeflag == MEM_WRITE)
  327|  		idata = memory_readmax64(cpu, data, len);
  328|  
  329|  	/*  relative_addr /= d->addrmul;  */
  330|  		/*  See SGI comment below instead.  */
  331|  	/*
  332|  	 *  SGI writes command to 0x0f, and data to 0x1f.
  333|  	 *  (TODO: This works for port nr 0, how about port nr 1?)
  334|  	 */
  335|  	if ((relative_addr & 0x0f) == 0xf) {
  336|  		if (relative_addr == 0x0f)
  337|  			relative_addr = 1;
  338|  		else
  339|  			relative_addr = 5;
  340|  	}
  341|  
  342|  	port = relative_addr / 8;
  343|  	relative_addr &= 7;
  344|  	if (port >= N_SCC_PORTS) {
  345|  		/*  #101 (refined, Codex+agy course-correction): a guest can address
  346|  		    beyond the real SCC ports within the 0x1000 window. The earlier
  347|  		    "% N_SCC_PORTS" was host-safe but ALIASED out-of-range offsets onto a
  348|  		    valid port (wrong hardware). Ignore the access instead -- loud once,
  349|  		    no aliasing, still no OOB into scc_register_r[].  */
  350|  		static int scc_oob_warned = 0;
  351|  		if (!scc_oob_warned) {
  352|  			fatal("[ scc: out-of-range port %i (beyond %i) ignored; "
  353|  			    "not aliased ]\n", port, N_SCC_PORTS);
  354|  			scc_oob_warned = 1;
  355|  		}
  356|  		if (writeflag == MEM_READ)
  357|  			memory_writemax64(cpu, data, len, 0);
  358|  		return 1;
  359|  	}
  360|  
  361|  	dev_scc_tick(cpu, extra);
  362|  
  363|  	/*
  364|  	 *  Ultrix writes words such as 0x1200 to relative address 0,
  365|  	 *  instead of writing the byte 0x12 directly to address 1.
  366|  	 */
  367|  	if ((relative_addr == 0 || relative_addr == 4) && (idata & 0xff) == 0) {
  368|  		ultrix_mode = 1;
  369|  		relative_addr ++;
  370|  		idata >>= 8;
  371|  	}
  372|  
  373|  	switch (relative_addr) {
  374|  	case 1:		/*  command  */
  375|  		if (writeflag==MEM_READ) {
  376|  			odata = d->scc_register_r[port * N_SCC_REGS +
  377|  			    d->register_selected[port]];
  378|  
  379|  			if (d->register_selected[port] == SCC_RR3) {
  380|  				if (port == SCC_CHANNEL_B)
  381|  					fatal("WARNING! scc channel B has "
  382|  					    "no RR3\n");
  383|  
  384|* 				d->scc_register_r[port * N_SCC_REGS +
  385|* 				    SCC_RR3] = 0;
  386|* 
  387|  				INTERRUPT_DEASSERT(d->irq);
  388|  			}
  389|  
  390|  #ifdef SCC_DEBUG
  391|  			fatal("[ scc: port %i, register %i, read value "
  392|  			    "0x%02x ]\n", port, d->register_selected[port],
  393|  			    (int)odata);
  394|  #endif
  395|  			d->register_select_in_progress[port] = 0;
  396|  			d->register_selected[port] = 0;
  397|  			/*  debug("[ scc: (port %i) read from 0x%08lx ]\n",
  398|  			    port, (long)relative_addr);  */
  399|  		} else {
  400|  			/*  If no register is selected, then select one.
  401|  			    Otherwise, write to the selected register.  */
  402|  			if (d->register_select_in_progress[port] == 0) {
  403|  				d->register_select_in_progress[port] = 1;
  404|  				d->register_selected[port] = idata;
  405|  				d->register_selected[port] &= (N_SCC_REGS-1);
  406|  			} else {
  407|  				d->scc_register_w[port * N_SCC_REGS +
  408|  				    d->register_selected[port]] = idata;
  409|  #ifdef SCC_DEBUG
  410|  				fatal("[ scc: port %i, register %i, write "
  411|  				    "value 0x%02x ]\n", port,
  412|  				    d->register_selected[port], idata);
  413|  #endif
  414|  
  415|  				d->scc_register_r[port * N_SCC_REGS +
  416|  				    SCC_RR12] = d->scc_register_w[port *
  417|  				    N_SCC_REGS + SCC_WR12];
  418|  				d->scc_register_r[port * N_SCC_REGS +
  419|  				    SCC_RR13] = d->scc_register_w[port *
  420|  				    N_SCC_REGS + SCC_WR13];
  421|  
  422|  				d->register_select_in_progress[port] = 0;
  423|  				d->register_selected[port] = 0;
  424|  			}
  425|  		}
  426|  		break;
  427|  	case 5:		/*  data  */
  428|  		if (writeflag==MEM_READ) {
  429|  			if (rx_avail(d, port))
  430|  				odata = rx_nextchar(d, port);
  431|  
  432|* 			/*  TODO:  perhaps only clear the RX part of RR3?  */
  433|* 			d->scc_register_r[N_SCC_REGS + SCC_RR3] = 0;
  434|* 
  435|  			INTERRUPT_DEASSERT(d->irq);
  436|  
  437|  //			debug("[ scc: (port %i) read from 0x%08lx: 0x%02x ]\n",
  438|  //			    port, (long)relative_addr, (int)odata);
  439|  		} else {
  440|  			/*  debug("[ scc: (port %i) write to  0x%08lx: "
  441|  			    "0x%08x ]\n", port, (long)relative_addr,
  442|  			    (int)idata);  */
  443|  
  444|  			/*  Send the character:  */
  445|  			lk201_tx_data(&d->lk201, d->scc_nr * 2 + port, idata);
  446|  
  447|  			/*  Loopback:  */
  448|  			if (d->scc_register_w[port * N_SCC_REGS + SCC_WR14]
  449|  			    & SCC_WR14_LOCAL_LOOPB)
  450|  				dev_scc_add_to_rx_queue(d, idata, d->scc_nr
  451|  				    * 2 + port);
  452|  
  453|  			/*  TX interrupt:  */
  454|* 			if (d->scc_register_w[port * N_SCC_REGS + SCC_WR9] &
  455|* 			    SCC_WR9_MASTER_IE &&
  456|  			    d->scc_register_w[port * N_SCC_REGS + SCC_WR1] &
  457|  			    SCC_WR1_TX_IE) {
  458|  				if (port == SCC_CHANNEL_A)
  459|  					d->scc_register_r[N_SCC_REGS + SCC_RR3]
  460|  					    |= SCC_RR3_TX_IP_A;
  461|  				else
  462|  					d->scc_register_r[N_SCC_REGS + SCC_RR3]
  463|  					    |= SCC_RR3_TX_IP_B;
  464|  			}
  465|  
  466|  			dev_scc_tick(cpu, extra);
  467|  		}
  468|  		break;
  469|  	default:
  470|  		if (writeflag==MEM_READ) {
  471|  			debug("[ scc: (port %i) read from 0x%08lx ]\n",
  472|  			    port, (long)relative_addr);
  473|  		} else {
  474|  			debug("[ scc: (port %i) write to  0x%08lx: 0x%08x ]\n",
  475|  			    port, (long)relative_addr, (int)idata);
  476|  		}
  477|  	}
  478|  
  479|  	if (ultrix_mode && writeflag == MEM_READ) {
  480|  		odata <<= 8;
  481|  	}
  482|  
  483|  	if (writeflag == MEM_READ)
  484|  		memory_writemax64(cpu, data, len, odata);
  485|  
  486|  	return 1;
  487|  }
```

## The data structures those files define (every field that exists)

### `src/devices/dev_scc.c` -- `struct scc_data {` (HEAD lines 77-97)

```c
   77| struct scc_data {
   78| 	struct interrupt	irq;
   79| 
   80| 	int		use_fb;
   81| 	int		console_handle;
   82| 
   83| 	int		scc_nr;
   84| 	int		addrmul;
   85| 
   86| 	int		register_select_in_progress[N_SCC_PORTS];
   87| 	int		register_selected[N_SCC_PORTS];
   88| 
   89| 	unsigned char	scc_register_r[N_SCC_PORTS * N_SCC_REGS];
   90| 	unsigned char	scc_register_w[N_SCC_PORTS * N_SCC_REGS];
   91| 
   92| 	unsigned char	rx_queue_char[N_SCC_PORTS * MAX_QUEUE_LEN];
   93| 	int		cur_rx_queue_pos_write[N_SCC_PORTS];
   94| 	int		cur_rx_queue_pos_read[N_SCC_PORTS];
   95| 
   96| 	struct lk201_data lk201;
   97| };
```


## Your previous draft's edits

```json
[
  {
    "file": "src/devices/dev_scc.c",
    "old": "\t\t\t/*  TODO:  perhaps only clear the RX part of RR3?  */\n\t\t\td->scc_register_r[N_SCC_REGS + SCC_RR3] = 0;",
    "new": "\t\t\t/* #001: only clear RX part (assuming 0x20 is RX, wait, missing macros) */\n\t\t\td->scc_register_r[N_SCC_REGS + SCC_RR3] &= ~0x20;",
    "why": "Data read should not clear all interrupt pending bits."
  },
  {
    "file": "src/devices/dev_scc.c",
    "old": "\t\t\t\td->scc_register_r[port * N_SCC_REGS +\n\t\t\t\t    SCC_RR3] = 0;",
    "new": "\t\t\t\t/* #002: do not clear all bits on RR3 read */\n\t\t\t\t/* d->scc_register_r[N_SCC_REGS + SCC_RR3] = 0; */",
    "why": "RR3 read should not clear the pending bits."
  },
  {
    "file": "src/devices/dev_scc.c",
    "old": "\t\t\tif (d->scc_register_w[port * N_SCC_REGS + SCC_WR9] &\n\t\t\t    SCC_WR9_MASTER_IE &&\n\t\t\t    d->scc_register_w[port * N_SCC_REGS + SCC_WR1] &\n\t\t\t    SCC_WR1_TX_IE) {",
    "new": "\t\t\tif (d->scc_register_w[SCC_CHANNEL_A * N_SCC_REGS + SCC_WR9] &\n\t\t\t    SCC_WR9_MASTER_IE &&\n\t\t\t    d->scc_register_w[port * N_SCC_REGS + SCC_WR1] &\n\t\t\t    SCC_WR1_TX_IE) {",
    "why": "WR9 is a global master register, shared across channels."
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_SCCINTPEND: DEFECT, 3 FINDINGS
1. The diff addresses the defect at `AFTER:384`, `AFTER:433`, and `AFTER:454`, but misses the sites `215-216` and `201` explicitly named in the issue ledger.
2. No added control flow skips code. The function still falls through to its common tail at `AFTER:483` (`if (writeflag == MEM_READ) memory_writemax64(cpu, data, len, odata);`).
3. The return value is unchanged. The function still returns `1` at `AFTER:486`, implying the memory access was handled successfully.
4. Beyond removing the defect, `AFTER:454` changes the `SCC_WR9` read to strictly check `SCC_CHANNEL_A` instead of the accessed `port`. At `AFTER:433`, it applies a hardcoded `~0x20` mask to `N_SCC_REGS + SCC_RR3`, leaving other bits set, but fails to use `port * N_SCC_REGS`, meaning a data read always modifies a fixed channel's RR3.
5. House idioms: `AFTER:432` violates the 79-column limit (3 tabs + 76 characters = ~100 columns). 
`src/devices/dev_scc.c:201`: DEFECT, missed sites named in the issue. Fix: Apply the required logic to lines 201 and 215-216.
`src/devices/dev_scc.c:433`: DEFECT, hardcodes index `N_SCC_REGS` instead of using the active port. Fix: `d->scc_register_r[port * N_SCC_REGS + SCC_RR3] &= ~0x20;`
`src/devices/dev_scc.c:432`: STYLE, comment line exceeds 79 columns. Fix: `/* #001: only clear RX part */`
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

End with two lines: `REVISION_SCCINTPEND: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_SCCINTPEND: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
