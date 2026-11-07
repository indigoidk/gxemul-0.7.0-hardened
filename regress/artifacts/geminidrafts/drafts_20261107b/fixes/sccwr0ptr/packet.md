# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `sccwr0ptr` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `sccwr0ptr`, state `open`)

**title:** devices/dev_scc.c:DEVICE_ACCESS(scc) -- the WR0 register pointer is the whole byte & 15 and WR0 commands are not decoded -- WRONG-RESULT

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T68 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A2-29).  Source URLs: https://github.com/rpajarola/gxemul/commit/2dfd6ec32be07d7dd38a707f66742de3e2023ed3.  Our site at de8c7547: src/devices/dev_scc.c:402-405.  Portable fix: yes -- port rpajarola 2dfd6ec.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

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
  384|  				d->scc_register_r[port * N_SCC_REGS +
  385|  				    SCC_RR3] = 0;
  386|  
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
  403|* 				d->register_select_in_progress[port] = 1;
  404|* 				d->register_selected[port] = idata;
  405|* 				d->register_selected[port] &= (N_SCC_REGS-1);
  406|* 			} else {
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
  432|  			/*  TODO:  perhaps only clear the RX part of RR3?  */
  433|  			d->scc_register_r[N_SCC_REGS + SCC_RR3] = 0;
  434|  
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
  454|  			if (d->scc_register_w[port * N_SCC_REGS + SCC_WR9] &
  455|  			    SCC_WR9_MASTER_IE &&
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
    "old": "\t\t\tif (d->register_select_in_progress[port] == 0) {\n\t\t\t\td->register_select_in_progress[port] = 1;\n\t\t\t\td->register_selected[port] = idata;\n\t\t\t\td->register_selected[port] &= (N_SCC_REGS-1);\n\t\t\t} else {",
    "new": "\t\t\tif (d->register_select_in_progress[port] == 0) {\n\t\t\t\t/* #sccwr0ptr: extract register pointer, do not decode commands yet */\n\t\t\t\td->register_selected[port] = idata & 0x0f;\n\t\t\t\td->register_selected[port] &= (N_SCC_REGS-1);\n\t\t\t\td->register_select_in_progress[port] = (d->register_selected[port] != 0);\n\t\t\t} else {",
    "why": "Isolate the register pointer to the lower nibble and only enter register select mode if a non-zero register was selected, ignoring commands in upper bits."
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_SCCWR0PTR: DEFECT, 2 FINDINGS
1. Does the diff remove the defect the issue describes? No. The issue explicitly states "WR0 commands are not decoded", but the proposed fix still does not decode them, masking them away and explicitly commenting "do not decode commands yet".
2. CONTROL FLOW: No added `return`, `goto`, `break`, or early exit is introduced by this diff.
3. RETURN VALUE: No path returns something different. The function still returns 1.
4. What ELSE does the diff change? State left set: `d->register_select_in_progress[port]` is now cleared if `idata & 0x0f` is 0. This means the device will now expect another command/pointer write instead of a data write if register 0 was selected. 
5. House idioms: The new line 406 exceeds the 79-column limit (it is over 100 columns with its 4-tab indentation).
src/devices/dev_scc.c:404 DEFECT: Fails to decode WR0 commands as reported in the issue. Fix: Decode and execute the WR0 commands from `idata` instead of merely masking them out.
src/devices/dev_scc.c:406 STYLE: Line exceeds 79 columns. Fix: Break the expression onto a new line.
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

End with two lines: `REVISION_SCCWR0PTR: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_SCCWR0PTR: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
