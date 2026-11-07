# GXemul hardened fork -- DRAFT A FIX for one filed issue, `mpipimemmove` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `mpipimemmove`, state `open`, severity `MED`)

**title:** src/devices/dev_mp.c:225-228 -- the IPI queue shift passes an element count to memmove() where a byte count is needed, so with two or more IPIs pending the entries left in the queue are wrong -- WRONG-RESULT (test machines)

**state_note (head):**



**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- Direct calculation error in memmove sizing that breaks the IPI queue.

## The code at the cited lines

### `src/devices/dev_mp.c` around the row's cited line 225 (HEAD 2d25df65, lines 180-270)

```c
  180| 		 *
  181| 		 *		(IPI_nr << 16) | cpu_id
  182| 		 *
  183| 		 *  This will send an Inter-processor interrupt to a specific
  184| 		 *  CPU. (DEV_MP_IPI_MANY sends to all _except_ the specific
  185| 		 *  CPU.)
  186| 		 *
  187| 		 *  Sending an IPI means adding the IPI last in the list of
  188| 		 *  pending IPIs, and asserting the IPI "pin".
  189| 		 */
  190| 		which_cpu = (idata & 0xffff);
  191| 		for (i=0; i<cpu->machine->ncpus; i++) {
  192| 			int send_it = 0;
  193| 			if (relative_addr == DEV_MP_IPI_ONE && i == which_cpu)
  194| 				send_it = 1;
  195| 			if (relative_addr == DEV_MP_IPI_MANY && i != which_cpu)
  196| 				send_it = 1;
  197| 			if (send_it) {
  198| 				d->n_pending_ipis[i] ++;
  199| 				CHECK_ALLOCATION(d->ipi[i] = (int *) realloc(d->ipi[i],
  200| 				    d->n_pending_ipis[i] * sizeof(int)));
  201| 
  202| 				/*  Add the IPI last in the array:  */
  203| 				d->ipi[i][d->n_pending_ipis[i] - 1] =
  204| 				    idata >> 16;
  205| 
  206| 				INTERRUPT_ASSERT(d->ipi_irq[i]);
  207| 			}
  208| 		}
  209| 		break;
  210| 
  211| 	case DEV_MP_IPI_READ:
  212| 		/*
  213| 		 *  If the current CPU has any IPIs pending, accessing this
  214| 		 *  address reads the IPI value. (Writing to this address
  215| 		 *  discards _all_ pending IPIs.)  If there is no pending
  216| 		 *  IPI, then 0 is returned. Usage of the value 0 for real
  217| 		 *  IPIs should thus be avoided.
  218| 		 */
  219| 		if (writeflag == MEM_WRITE) {
  220| 			d->n_pending_ipis[cpu->cpu_id] = 0;
  221| 		}
  222| 		odata = 0;
  223| 		if (d->n_pending_ipis[cpu->cpu_id] > 0) {
  224| 			odata = d->ipi[cpu->cpu_id][0];
  225| 			if (d->n_pending_ipis[cpu->cpu_id]-- > 1)
  226| 				memmove(&d->ipi[cpu->cpu_id][0],
  227| 				    &d->ipi[cpu->cpu_id][1],
  228| 				    d->n_pending_ipis[cpu->cpu_id]);
  229| 		}
  230| 
  231| 		/*  Deassert the interrupt, if there are no pending IPIs:  */
  232| 		if (d->n_pending_ipis[cpu->cpu_id] == 0)
  233| 			INTERRUPT_DEASSERT(d->ipi_irq[cpu->cpu_id]);
  234| 		break;
  235| 
  236| 	case DEV_MP_NCYCLES:
  237| 		/*
  238| 		 *  Return _approximately_ the number of cycles executed
  239| 		 *  on this CPU.
  240| 		 *
  241| 		 *  (This value is not updated for each instruction.)
  242| 		 */
  243| 		odata = cpu->ninstrs;
  244| 		break;
  245| 
  246| 	default:
  247| 		fatal("[ dev_mp: unimplemented relative addr 0x%" PRIx64 " ]\n",
  248| 		    (uint64_t)relative_addr);
  249| 	}
  250| 
  251| 	if (writeflag == MEM_READ)
  252| 		memory_writemax64(cpu, data, len, odata);
  253| 
  254| 	return 1;
  255| }
  256| 
  257| 
  258| DEVINIT(mp)
  259| {
  260| 	struct mp_data *d;
  261| 	int n, i;
  262| 
  263| 	CHECK_ALLOCATION(d = (struct mp_data *) malloc(sizeof(struct mp_data)));
  264| 	memset(d, 0, sizeof(struct mp_data));
  265| 
  266| 	d->cpus = devinit->machine->cpus;
  267| 	d->startup_addr = INITIAL_PC;
  268| 	d->stack_addr = INITIAL_STACK_POINTER;
  269| 
  270| 	n = devinit->machine->ncpus;
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

End with one line: `FIXDRAFT_MPIPIMEMMOVE: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
