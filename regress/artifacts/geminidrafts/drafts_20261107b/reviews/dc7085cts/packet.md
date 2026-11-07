# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `dc7085cts` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `dc7085cts`, state `open`)

**title:** devices/dev_dc7085.c MSR read -- CTS is not reported on lines 2/3 -- WRONG-RESULT (OSF/1 console hangs up)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T79 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: one-line; report rows: A2-60, A(c)#13).  Source URLs: https://github.com/rpajarola/gxemul/commit/807d80bf5be49ec5ef4d2f590904bea23bd11966.  Our site at de8c7547: src/devices/dev_dc7085.c:261-262.  Portable fix: yes -- port rpajarola 807d80b.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- dev_dc7085.c:263-264

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_dc7085.c b/src/devices/dev_dc7085.c
index 08396f18..29b475b8 100644
--- a/src/devices/dev_dc7085.c
+++ b/src/devices/dev_dc7085.c
@@ -260,8 +260,9 @@ DEVICE_ACCESS(dc7085)
 			INTERRUPT_DEASSERT(d->irq);
 		} else {
 			/*  read:  */
-			d->regs.dc_msr_tdr |= MSR_DSR2 | MSR_CD2 |
-			    MSR_DSR3 | MSR_CD3;
+			/* #7085: Report CTS for lines 2/3 */
+			d->regs.dc_msr_tdr |= MSR_DSR2 | MSR_CD2 | MSR_CTS2 |
+			    MSR_DSR3 | MSR_CD3 | MSR_CTS3;
 			debug("[ dc7085 read from MSR: (msr_tdr = 0x%04x) ]\n",
 			    d->regs.dc_msr_tdr);
 			odata = d->regs.dc_msr_tdr;
```

## Every edited function, after the fix

### `src/devices/dev_dc7085.c` -- post-edit lines 165-292 (`+` marks a line the diff added or the point of a deletion)

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
  263|+ 			/* #7085: Report CTS for lines 2/3 */
  264|+ 			d->regs.dc_msr_tdr |= MSR_DSR2 | MSR_CD2 | MSR_CTS2 |
  265|+ 			    MSR_DSR3 | MSR_CD3 | MSR_CTS3;
  266|  			debug("[ dc7085 read from MSR: (msr_tdr = 0x%04x) ]\n",
  267|  			    d->regs.dc_msr_tdr);
  268|  			odata = d->regs.dc_msr_tdr;
  269|  		}
  270|  		break;
  271|  
  272|  	default:
  273|  		if (writeflag==MEM_READ) {
  274|  			debug("[ dc7085 read from 0x%08lx ]\n",
  275|  			    (long)relative_addr);
  276|  		} else {
  277|  			debug("[ dc7085 write to 0x%08lx:",
  278|  			    (long)relative_addr);
  279|  			for (i=0; i<len; i++)
  280|  				debug(" %02x", data[i]);
  281|  			debug(" ]\n");
  282|  		}
  283|  	}
  284|  
  285|  	if (writeflag == MEM_READ)
  286|  		memory_writemax64(cpu, data, len, odata);
  287|  
  288|  do_return:
  289|  	dev_dc7085_tick(cpu, extra);
  290|  
  291|  	return 1;
  292|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_DC7085CTS: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_DC7085CTS: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
