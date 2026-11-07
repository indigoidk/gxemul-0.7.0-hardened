# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `mpipimemmove` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `mpipimemmove`, state `open`)

**title:** src/devices/dev_mp.c:225-228 -- the IPI queue shift passes an element count to memmove() where a byte count is needed, so with two or more IPIs pending the entries left in the queue are wrong -- WRONG-RESULT (test machines)

**state_note (head):** 

**The drafter's own reading:** STILL PRESENT: YES -- 228| 				    d->n_pending_ipis[cpu->cpu_id]);

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_mp.c b/src/devices/dev_mp.c
index 1c06fe7e..23e346aa 100644
--- a/src/devices/dev_mp.c
+++ b/src/devices/dev_mp.c
@@ -225,7 +225,7 @@ DEVICE_ACCESS(mp)
 			if (d->n_pending_ipis[cpu->cpu_id]-- > 1)
 				memmove(&d->ipi[cpu->cpu_id][0],
 				    &d->ipi[cpu->cpu_id][1],
-				    d->n_pending_ipis[cpu->cpu_id]);
+				    d->n_pending_ipis[cpu->cpu_id] * sizeof(int));
 		}
 
 		/*  Deassert the interrupt, if there are no pending IPIs:  */
```

## Every edited function, after the fix

### `src/devices/dev_mp.c` -- post-edit lines 67-255 (`+` marks a line the diff added or the point of a deletion)

```c
   67|  DEVICE_ACCESS(mp)
   68|  {
   69|  	struct mp_data *d = (struct mp_data *) extra;
   70|  	int i, which_cpu;
   71|  	uint64_t idata = 0, odata = 0;
   72|  
   73|  	if (writeflag == MEM_WRITE)
   74|  	        idata = memory_readmax64(cpu, data, len);
   75|  
   76|  	/*
   77|  	 *  NOTE: It is up to the user of this device to read or write
   78|  	 *  correct addresses. (A write to NCPUS is pretty useless,
   79|  	 *  for example.)
   80|  	 */
   81|  
   82|  	switch (relative_addr) {
   83|  
   84|  	case DEV_MP_WHOAMI:
   85|  		odata = cpu->cpu_id;
   86|  		break;
   87|  
   88|  	case DEV_MP_NCPUS:
   89|  		odata = cpu->machine->ncpus;
   90|  		break;
   91|  
   92|  	case DEV_MP_STARTUPCPU:
   93|  		which_cpu = idata;
   94|  		/*  The CPU index comes from the guest; reject out-of-range
   95|  		    values instead of indexing d->cpus[] out of bounds.  */
   96|  		if (which_cpu < 0 || which_cpu >= cpu->machine->ncpus)
   97|  			break;
   98|  		d->cpus[which_cpu]->pc = d->startup_addr;
   99|  		switch (cpu->cpu_family->arch) {
  100|  		case ARCH_MIPS:
  101|  			d->cpus[which_cpu]->cd.mips.gpr[MIPS_GPR_SP] =
  102|  			    d->stack_addr;
  103|  			break;
  104|  		case ARCH_PPC:
  105|  			d->cpus[which_cpu]->cd.ppc.gpr[1] = d->stack_addr;
  106|  			break;
  107|  		default:
  108|  			/*  #221: (Codex/Fable) a guest STARTUPCPU on a test machine
  109|  			    of an arch without SP-init here: warn and start the CPU
  110|  			    anyway instead of exit()ing the host.  */
  111|  			fatal("dev_mp(): DEV_MP_STARTUPCPU: not for this"
  112|  			    " arch yet!\n");
  113|  			break;
  114|  		}
  115|  		d->cpus[which_cpu]->running = true;
  116|  		/*  debug("[ dev_mp: starting up cpu%i at 0x%llx ]\n", 
  117|  		    which_cpu, (long long)d->startup_addr);  */
  118|  		break;
  119|  
  120|  	case DEV_MP_STARTUPADDR:
  121|  		if (len==4 && (idata >> 32) == 0 && (idata & 0x80000000ULL))
  122|  			idata |= 0xffffffff00000000ULL;
  123|  		d->startup_addr = idata;
  124|  		break;
  125|  
  126|  	case DEV_MP_PAUSE_ADDR:
  127|  		d->pause_addr = idata;
  128|  		break;
  129|  
  130|  	case DEV_MP_PAUSE_CPU:
  131|  		/*  Pause all cpus except a specific CPU:  */
  132|  		which_cpu = idata;
  133|  
  134|  		for (i=0; i<cpu->machine->ncpus; i++)
  135|  			if (i != which_cpu)
  136|  				d->cpus[i]->running = false;
  137|  		break;
  138|  
  139|  	case DEV_MP_UNPAUSE_CPU:
  140|  		/*  Unpause a specific CPU:  */
  141|  		which_cpu = idata;
  142|  
  143|  		if (which_cpu >= 0 && which_cpu <cpu->machine->ncpus)
  144|  			d->cpus[which_cpu]->running = true;
  145|  		break;
  146|  
  147|  	case DEV_MP_STARTUPSTACK:
  148|  		if (len == 4 && (idata >> 32) == 0 && (idata & 0x80000000ULL))
  149|  			idata |= 0xffffffff00000000ULL;
  150|  		d->stack_addr = idata;
  151|  		break;
  152|  
  153|  	case DEV_MP_HARDWARE_RANDOM:
  154|  		/*
  155|  		 *  Return (up to) 64 bits of "hardware random":
  156|  		 *
  157|  		 *  NOTE: Remember that random() is (usually) 31 bits of
  158|  		 *        random data, _NOT_ 32, hence this construction.
  159|  		 */
  160|  		odata = random();
  161|  		odata = (odata << 31) ^ random();
  162|  		odata = (odata << 31) ^ random();
  163|  		break;
  164|  
  165|  	case DEV_MP_MEMORY:
  166|  		/*
  167|  		 *  Return the number of bytes of memory in the system.
  168|  		 *
  169|  		 *  (It is assumed to be located at physical address 0.
  170|  		 *  It is actually located at machine->memory_offset_in_mb
  171|  		 *  but that is only used for SGI emulation so far.)
  172|  		 */
  173|  		odata = cpu->machine->physical_ram_in_mb * 1048576ULL;
  174|  		break;
  175|  
  176|  	case DEV_MP_IPI_ONE:
  177|  	case DEV_MP_IPI_MANY:
  178|  		/*
  179|  		 *  idata should be of the form:
  180|  		 *
  181|  		 *		(IPI_nr << 16) | cpu_id
  182|  		 *
  183|  		 *  This will send an Inter-processor interrupt to a specific
  184|  		 *  CPU. (DEV_MP_IPI_MANY sends to all _except_ the specific
  185|  		 *  CPU.)
  186|  		 *
  187|  		 *  Sending an IPI means adding the IPI last in the list of
  188|  		 *  pending IPIs, and asserting the IPI "pin".
  189|  		 */
  190|  		which_cpu = (idata & 0xffff);
  191|  		for (i=0; i<cpu->machine->ncpus; i++) {
  192|  			int send_it = 0;
  193|  			if (relative_addr == DEV_MP_IPI_ONE && i == which_cpu)
  194|  				send_it = 1;
  195|  			if (relative_addr == DEV_MP_IPI_MANY && i != which_cpu)
  196|  				send_it = 1;
  197|  			if (send_it) {
  198|  				d->n_pending_ipis[i] ++;
  199|  				CHECK_ALLOCATION(d->ipi[i] = (int *) realloc(d->ipi[i],
  200|  				    d->n_pending_ipis[i] * sizeof(int)));
  201|  
  202|  				/*  Add the IPI last in the array:  */
  203|  				d->ipi[i][d->n_pending_ipis[i] - 1] =
  204|  				    idata >> 16;
  205|  
  206|  				INTERRUPT_ASSERT(d->ipi_irq[i]);
  207|  			}
  208|  		}
  209|  		break;
  210|  
  211|  	case DEV_MP_IPI_READ:
  212|  		/*
  213|  		 *  If the current CPU has any IPIs pending, accessing this
  214|  		 *  address reads the IPI value. (Writing to this address
  215|  		 *  discards _all_ pending IPIs.)  If there is no pending
  216|  		 *  IPI, then 0 is returned. Usage of the value 0 for real
  217|  		 *  IPIs should thus be avoided.
  218|  		 */
  219|  		if (writeflag == MEM_WRITE) {
  220|  			d->n_pending_ipis[cpu->cpu_id] = 0;
  221|  		}
  222|  		odata = 0;
  223|  		if (d->n_pending_ipis[cpu->cpu_id] > 0) {
  224|  			odata = d->ipi[cpu->cpu_id][0];
  225|  			if (d->n_pending_ipis[cpu->cpu_id]-- > 1)
  226|  				memmove(&d->ipi[cpu->cpu_id][0],
  227|  				    &d->ipi[cpu->cpu_id][1],
  228|+ 				    d->n_pending_ipis[cpu->cpu_id] * sizeof(int));
  229|  		}
  230|  
  231|  		/*  Deassert the interrupt, if there are no pending IPIs:  */
  232|  		if (d->n_pending_ipis[cpu->cpu_id] == 0)
  233|  			INTERRUPT_DEASSERT(d->ipi_irq[cpu->cpu_id]);
  234|  		break;
  235|  
  236|  	case DEV_MP_NCYCLES:
  237|  		/*
  238|  		 *  Return _approximately_ the number of cycles executed
  239|  		 *  on this CPU.
  240|  		 *
  241|  		 *  (This value is not updated for each instruction.)
  242|  		 */
  243|  		odata = cpu->ninstrs;
  244|  		break;
  245|  
  246|  	default:
  247|  		fatal("[ dev_mp: unimplemented relative addr 0x%" PRIx64 " ]\n",
  248|  		    (uint64_t)relative_addr);
  249|  	}
  250|  
  251|  	if (writeflag == MEM_READ)
  252|  		memory_writemax64(cpu, data, len, odata);
  253|  
  254|  	return 1;
  255|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_MPIPIMEMMOVE: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_MPIPIMEMMOVE: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
