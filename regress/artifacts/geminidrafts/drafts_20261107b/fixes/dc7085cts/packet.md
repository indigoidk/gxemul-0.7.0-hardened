# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `dc7085cts` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `dc7085cts`, state `open`)

**title:** devices/dev_dc7085.c MSR read -- CTS is not reported on lines 2/3 -- WRONG-RESULT (OSF/1 console hangs up)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T79 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: one-line; report rows: A2-60, A(c)#13).  Source URLs: https://github.com/rpajarola/gxemul/commit/807d80bf5be49ec5ef4d2f590904bea23bd11966.  Our site at de8c7547: src/devices/dev_dc7085.c:261-262.  Portable fix: yes -- port rpajarola 807d80b.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/devices/dev_dc7085.c` -- AT HEAD, lines 165-291 (`*` marks a line your previous draft changed)

```c
  165|  DEVICE_ACCESS(dc7085)
  166|  {
  167|  	struct dc_data *d = (struct dc_data *) extra;
  168|  	uint64_t idata = 0, odata = 0;
  169|  	size_t i;
  170|  
  171|  	if (writeflag == MEM_WRITE)
  172|  		idata = memory_readmax64(cpu, data, len);
  173|  
  174|  	/*  Always clear:  */
  175|  	d->regs.dc_csr &= ~CSR_CLR;
  176|  
  177|  	switch (relative_addr) {
  178|  
  179|  	case 0x00:	/*  CSR:  Control and Status  */
  180|  		if (writeflag == MEM_WRITE) {
  181|  			debug("[ dc7085 write to CSR: 0x%04" PRIx64 " ]\n",
  182|  			    (uint64_t)idata);
  183|  			idata &= (CSR_TIE | CSR_RIE | CSR_MSE | CSR_CLR
  184|  			    | CSR_MAINT);
  185|  			d->regs.dc_csr &= ~(CSR_TIE | CSR_RIE | CSR_MSE
  186|  			    | CSR_CLR | CSR_MAINT);
  187|  			d->regs.dc_csr |= idata;
  188|  			if (!(d->regs.dc_csr & CSR_MSE))
  189|  				d->regs.dc_csr &= ~(CSR_TRDY | CSR_RDONE);
  190|  			goto do_return;
  191|  		} else {
  192|  			/*  read:  */
  193|  
  194|  			/*  fatal("[ dc7085 read from CSR: (csr = 0x%04x) ]\n",
  195|  			    d->regs.dc_csr);  */
  196|  			odata = d->regs.dc_csr;
  197|  		}
  198|  		break;
  199|  
  200|  	case 0x08:	/*  LPR:  */
  201|  		if (writeflag == MEM_WRITE) {
  202|  			debug("[ dc7085 write to LPR: 0x%04" PRIx64 " ]\n",
  203|  			    (uint64_t)idata);
  204|  			d->regs.dc_rbuf_lpr = idata;
  205|  			goto do_return;
  206|  		} else {
  207|  			/*  read:  */
  208|  			int avail = d->cur_rx_queue_pos_write !=
  209|  			    d->cur_rx_queue_pos_read;
  210|  			int ch = 0, lineno = 0;
  211|  			/*  debug("[ dc7085 read from RBUF: ");  */
  212|  			if (avail) {
  213|  				ch = d->rx_queue_char[d->cur_rx_queue_pos_read];
  214|  				lineno = d->rx_queue_lineno[
  215|  				    d->cur_rx_queue_pos_read];
  216|  				d->cur_rx_queue_pos_read++;
  217|  				if (d->cur_rx_queue_pos_read == MAX_QUEUE_LEN)
  218|  					d->cur_rx_queue_pos_read = 0;
  219|  				/*  if (ch >= ' ' && ch < 127)
  220|  					debug("'%c'", ch);
  221|  				else
  222|  					debug("0x%x", ch);
  223|  				debug(" for lineno %i ", lineno);  */
  224|  			}  /*  else
  225|  				debug("empty ");
  226|  			debug("]\n");  */
  227|  			odata = (avail? RBUF_DVAL:0) |
  228|  			    (lineno << RBUF_LINE_NUM_SHIFT) | ch;
  229|  
  230|  			d->regs.dc_csr &= ~CSR_RDONE;
  231|  			INTERRUPT_DEASSERT(d->irq);
  232|  		}
  233|  		break;
  234|  
  235|  	case 0x10:	/*  TCR:  */
  236|  		if (writeflag == MEM_WRITE) {
  237|  			/*  fatal("[ dc7085 write to TCR: 0x%04x) ]\n",
  238|  			    (int)idata);  */
  239|  			d->regs.dc_tcr = idata;
  240|  			d->regs.dc_csr &= ~CSR_TRDY;
  241|  			INTERRUPT_DEASSERT(d->irq);
  242|  			goto do_return;
  243|  		} else {
  244|  			/*  read:  */
  245|  			/*  debug("[ dc7085 read from TCR: (tcr = 0x%04x) ]\n",
  246|  			    d->regs.dc_tcr);  */
  247|  			odata = d->regs.dc_tcr;
  248|  		}
  249|  		break;
  250|  
  251|  	case 0x18:	/*  Modem status (R), transmit data (W)  */
  252|  		if (writeflag == MEM_WRITE) {
  253|  			int line_no = (d->regs.dc_csr >>
  254|  			    RBUF_LINE_NUM_SHIFT) & 0x3;
  255|  			idata &= 0xff;
  256|  
  257|  			lk201_tx_data(&d->lk201, line_no, idata);
  258|  
  259|  			d->regs.dc_csr &= ~CSR_TRDY;
  260|  			INTERRUPT_DEASSERT(d->irq);
  261|  		} else {
  262|  			/*  read:  */
  263|* 			d->regs.dc_msr_tdr |= MSR_DSR2 | MSR_CD2 |
  264|* 			    MSR_DSR3 | MSR_CD3;
  265|* 			debug("[ dc7085 read from MSR: (msr_tdr = 0x%04x) ]\n",
  266|  			    d->regs.dc_msr_tdr);
  267|  			odata = d->regs.dc_msr_tdr;
  268|  		}
  269|  		break;
  270|  
  271|  	default:
  272|  		if (writeflag==MEM_READ) {
  273|  			debug("[ dc7085 read from 0x%08lx ]\n",
  274|  			    (long)relative_addr);
  275|  		} else {
  276|  			debug("[ dc7085 write to 0x%08lx:",
  277|  			    (long)relative_addr);
  278|  			for (i=0; i<len; i++)
  279|  				debug(" %02x", data[i]);
  280|  			debug(" ]\n");
  281|  		}
  282|  	}
  283|  
  284|  	if (writeflag == MEM_READ)
  285|  		memory_writemax64(cpu, data, len, odata);
  286|  
  287|  do_return:
  288|  	dev_dc7085_tick(cpu, extra);
  289|  
  290|  	return 1;
  291|  }
```

## The data structures those files define (every field that exists)

### `src/devices/dev_dc7085.c` -- `struct dc_data {` (HEAD lines 49-65)

```c
   49| struct dc_data {
   50| 	struct dc7085regs	regs;
   51| 
   52| 	int			console_handle;
   53| 
   54| 	unsigned char		rx_queue_char[MAX_QUEUE_LEN];
   55| 	char			rx_queue_lineno[MAX_QUEUE_LEN];
   56| 	int			cur_rx_queue_pos_write;
   57| 	int			cur_rx_queue_pos_read;
   58| 
   59| 	int			tx_scanner;
   60| 
   61| 	struct interrupt	irq;
   62| 	int			use_fb;
   63| 
   64| 	struct lk201_data	lk201;
   65| };
```


## Your previous draft's edits

```json
[
  {
    "file": "src/devices/dev_dc7085.c",
    "old": "\t\t\td->regs.dc_msr_tdr |= MSR_DSR2 | MSR_CD2 |\n\t\t\t    MSR_DSR3 | MSR_CD3;",
    "new": "\t\t\td->regs.dc_msr_tdr |= MSR_DSR2 | MSR_CD2 | MSR_CTS2 |\n\t\t\t    MSR_DSR3 | MSR_CD3 | MSR_CTS3; /* #7085: Report CTS for lines 2/3 */",
    "why": "Add CTS signaling to lines 2 and 3 when reading MSR to prevent OSF/1 console hangs."
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_DC7085CTS: DEFECT, 1 FINDINGS.
1. **Defect Removal:** Yes, the diff removes the defect. The issue reports that CTS is not reported on lines 2/3 during an MSR read. The fix successfully adds `MSR_CTS2` and `MSR_CTS3` to the register value on the MSR read path (lines 263-264). It does not miss the named site.
2. **CONTROL FLOW:** No control flow statements (`return`, `goto`, `break`, or early exit) were added. The function's execution continues uninterrupted through the switch statement to the common tail (line 284: `if (writeflag == MEM_READ) memory_writemax64(...)`, then `do_return` and `return 1;`).
3. **RETURN VALUE:** No path now returns something different. The function continues to return `1` on line 290, which conventionally implies a successful handling of the memory access.
4. **State/Side Effects:** Beyond adding the required defect-fixing bits, the diff leaves the underlying pattern alone. Note that it permanently updates the emulator's saved state (`d->regs.dc_msr_tdr |= ...`) with the CTS bits upon a read, rather than just returning them via `odata`, but this perfectly mirrors the existing code's behavior for DSR and CD bits. The only newly introduced side effect is a source code comment.
5. **House Idioms:** The added comment successfully carries the required `/* #7085: ... */` tag. However, the line it was placed on exceeds the 79-column house limit. Assuming 8-space tabs, line 264 is 96 columns wide (3 tabs + 4 spaces + 68 characters).
`src/devices/dev_dc7085.c:264` STYLE Comment pushes line to 96 columns; place the comment on its own line above the statement.
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

End with two lines: `REVISION_DC7085CTS: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_DC7085CTS: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
