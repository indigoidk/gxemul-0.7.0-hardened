# GXemul hardened fork -- DRAFT A FIX for one filed issue, `dc7085cts` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `dc7085cts`, state `open`, severity `MED`)

**title:** devices/dev_dc7085.c MSR read -- CTS is not reported on lines 2/3 -- WRONG-RESULT (OSF/1 console hangs up)

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T79 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: one-line; report rows: A2-60, A(c)#13).  Source URLs: https://github.com/rpajarola/gxemul/commit/807d80bf5be49ec5ef4d2f590904bea23bd11966.  Our site at de8c7547: src/devices/dev_dc7085.c:261-262.  Portable fix: yes -- port rpajarola 807d80b.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- Portable fix available upstream.

## The code at the cited lines

### `src/devices/dev_dc7085.c` around the row's cited line 261 (HEAD 2d25df65, lines 216-306)

```c
  216| 				d->cur_rx_queue_pos_read++;
  217| 				if (d->cur_rx_queue_pos_read == MAX_QUEUE_LEN)
  218| 					d->cur_rx_queue_pos_read = 0;
  219| 				/*  if (ch >= ' ' && ch < 127)
  220| 					debug("'%c'", ch);
  221| 				else
  222| 					debug("0x%x", ch);
  223| 				debug(" for lineno %i ", lineno);  */
  224| 			}  /*  else
  225| 				debug("empty ");
  226| 			debug("]\n");  */
  227| 			odata = (avail? RBUF_DVAL:0) |
  228| 			    (lineno << RBUF_LINE_NUM_SHIFT) | ch;
  229| 
  230| 			d->regs.dc_csr &= ~CSR_RDONE;
  231| 			INTERRUPT_DEASSERT(d->irq);
  232| 		}
  233| 		break;
  234| 
  235| 	case 0x10:	/*  TCR:  */
  236| 		if (writeflag == MEM_WRITE) {
  237| 			/*  fatal("[ dc7085 write to TCR: 0x%04x) ]\n",
  238| 			    (int)idata);  */
  239| 			d->regs.dc_tcr = idata;
  240| 			d->regs.dc_csr &= ~CSR_TRDY;
  241| 			INTERRUPT_DEASSERT(d->irq);
  242| 			goto do_return;
  243| 		} else {
  244| 			/*  read:  */
  245| 			/*  debug("[ dc7085 read from TCR: (tcr = 0x%04x) ]\n",
  246| 			    d->regs.dc_tcr);  */
  247| 			odata = d->regs.dc_tcr;
  248| 		}
  249| 		break;
  250| 
  251| 	case 0x18:	/*  Modem status (R), transmit data (W)  */
  252| 		if (writeflag == MEM_WRITE) {
  253| 			int line_no = (d->regs.dc_csr >>
  254| 			    RBUF_LINE_NUM_SHIFT) & 0x3;
  255| 			idata &= 0xff;
  256| 
  257| 			lk201_tx_data(&d->lk201, line_no, idata);
  258| 
  259| 			d->regs.dc_csr &= ~CSR_TRDY;
  260| 			INTERRUPT_DEASSERT(d->irq);
  261| 		} else {
  262| 			/*  read:  */
  263| 			d->regs.dc_msr_tdr |= MSR_DSR2 | MSR_CD2 |
  264| 			    MSR_DSR3 | MSR_CD3;
  265| 			debug("[ dc7085 read from MSR: (msr_tdr = 0x%04x) ]\n",
  266| 			    d->regs.dc_msr_tdr);
  267| 			odata = d->regs.dc_msr_tdr;
  268| 		}
  269| 		break;
  270| 
  271| 	default:
  272| 		if (writeflag==MEM_READ) {
  273| 			debug("[ dc7085 read from 0x%08lx ]\n",
  274| 			    (long)relative_addr);
  275| 		} else {
  276| 			debug("[ dc7085 write to 0x%08lx:",
  277| 			    (long)relative_addr);
  278| 			for (i=0; i<len; i++)
  279| 				debug(" %02x", data[i]);
  280| 			debug(" ]\n");
  281| 		}
  282| 	}
  283| 
  284| 	if (writeflag == MEM_READ)
  285| 		memory_writemax64(cpu, data, len, odata);
  286| 
  287| do_return:
  288| 	dev_dc7085_tick(cpu, extra);
  289| 
  290| 	return 1;
  291| }
  292| 
  293| 
  294| /*
  295|  *  dev_dc7085_init():
  296|  *
  297|  *  Initialize a dc7085 serial controller device. use_fb should be non-zero
  298|  *  if a framebuffer device is used. Channel 0 will then be treated as a
  299|  *  DECstation keyboard, instead of a plain serial console.
  300|  */
  301| int dev_dc7085_init(struct machine *machine, struct memory *mem,
  302| 	uint64_t baseaddr, char *irq_path, int use_fb)
  303| {
  304| 	struct dc_data *d;
  305| 
  306| 	CHECK_ALLOCATION(d = (struct dc_data *) malloc(sizeof(struct dc_data)));
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

End with one line: `FIXDRAFT_DC7085CTS: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
