# GXemul hardened fork -- DRAFT A FIX for one filed issue, `dec5800ncpushift` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `dec5800ncpushift`, state `open`, severity `LOW`)

**title:** src/devices/dev_dec5800.c:359-367 -- (1 << ncpus) - 1 is undefined for 31 or more CPUs, which -n allows (up to 256) -- WRONG-RESULT (host -n option)

**state_note (head):**



**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- Signed 32-bit shift overflows when ncpus >= 31, causing undefined behavior.

## The code at the cited lines

### `src/devices/dev_dec5800.c` around the row's cited line 359 (HEAD 2d25df65, lines 314-404)

```c
  314| 	struct decbi_data *d;
  315| 
  316| 	CHECK_ALLOCATION(d = (struct decbi_data *) malloc(sizeof(struct decbi_data)));
  317| 	memset(d, 0, sizeof(struct decbi_data));
  318| 
  319| 	memory_device_register(devinit->machine->memory, "decbi",
  320| 	    devinit->addr + 0x2000, DEV_DECBI_LENGTH - 0x2000,
  321| 	    dev_decbi_access, d, DM_DEFAULT, NULL);
  322| 
  323| 	return 1;
  324| }
  325| 
  326| 
  327| /*****************************************************************************/
  328| 
  329| 
  330| /*
  331|  *  CCA, "Console Communication Area" for a DEC 5800 SMP system.
  332|  */
  333| 
  334| struct deccca_data {
  335| 	int		dummy;
  336| };
  337| 
  338| 
  339| DEVICE_ACCESS(deccca)
  340| {
  341| 	uint64_t idata = 0, odata = 0;
  342| 	/*  struct deccca_data *d = extra;  */
  343| 
  344| 	if (writeflag == MEM_WRITE)
  345| 		idata = memory_readmax64(cpu, data, len);
  346| 
  347| 	switch (relative_addr) {
  348| 	case 6:
  349| 	case 7:
  350| 		/*  CCA "ID" bytes? These must be here, or Ultrix complains.  */
  351| 		if (writeflag == MEM_READ)
  352| 			odata = 67;
  353| 		break;
  354| 	case 8:
  355| 		if (writeflag == MEM_READ)
  356| 			odata = cpu->machine->ncpus;
  357| 		break;
  358| 	case 20:
  359| 		if (writeflag == MEM_READ)
  360| 			odata = (1 << cpu->machine->ncpus) - 1;
  361| 			    /*  one bit for each cpu  */
  362| 		break;
  363| 	case 28:
  364| 		if (writeflag == MEM_READ)
  365| 			odata = (1 << cpu->machine->ncpus) - 1;
  366| 			    /*  one bit for each enabled(?) cpu  */
  367| 		break;
  368| 	default:
  369| 		if (writeflag==MEM_READ) {
  370| 			debug("[ deccca: read from 0x%08lx ]\n",
  371| 			    (long)relative_addr);
  372| 		} else {
  373| 			debug("[ deccca: write to  0x%08lx: 0x%08x ]\n",
  374| 			    (long)relative_addr, (int)idata);
  375| 		}
  376| 	}
  377| 
  378| 	if (writeflag == MEM_READ)
  379| 		memory_writemax64(cpu, data, len, odata);
  380| 
  381| 	return 1;
  382| }
  383| 
  384| 
  385| /*
  386|  *  dev_deccca_init():
  387|  */
  388| void dev_deccca_init(struct memory *mem, uint64_t baseaddr)
  389| {
  390| 	struct deccca_data *d;
  391| 
  392| 	CHECK_ALLOCATION(d = (struct deccca_data *) malloc(sizeof(struct deccca_data)));
  393| 	memset(d, 0, sizeof(struct deccca_data));
  394| 
  395| 	memory_device_register(mem, "deccca", baseaddr, DEV_DECCCA_LENGTH,
  396| 	    dev_deccca_access, d, DM_DEFAULT, NULL);
  397| }
  398| 
  399| 
  400| /*****************************************************************************/
  401| 
  402| 
  403| /*
  404|  *  DEC 5800 XMI (this has to do with SMP...)
```

### `src/core/main.c` around the row's cited line 427 (HEAD 2d25df65, lines 382-472)

```c
  382| 			break;
  383| 		case 'J':
  384| 			m->allow_instruction_combinations = 0;
  385| 			machine_specific_options_used = true;
  386| 			break;
  387| 		case 'j':
  388| 			CHECK_ALLOCATION(m->boot_kernel_filename = strdup(optarg));
  389| 			machine_specific_options_used = true;
  390| 			break;
  391| 		case 'k':
  392| 			{
  393| 				/*  atoi() overflowed int before the old
  394| 				    "< 1" check ran; the value is multiplied
  395| 				    by 1 MB, so bound it by what fits in a
  396| 				    size_t (and 1 TB as a sanity cap).  */
  397| 				long long max_mb =
  398| 				    (long long) (SIZE_MAX / 1048576);
  399| 				if (max_mb > 1048576)
  400| 					max_mb = 1048576;
  401| 				dyntrans_cache_size = (size_t)
  402| 				    parse_int_option('k', optarg, 1, max_mb)
  403| 				    * 1048576;
  404| 			}
  405| 			break;
  406| 		case 'K':
  407| 			debugger_enter_at_end_of_run = true;
  408| 			break;
  409| 		case 'L':
  410| 			CHECK_ALLOCATION(*tap_devname = strdup(optarg));
  411| 			break;
  412| 		case 'M':
  413| 			/*  atoi() let negative/overflowed values through
  414| 			    to the uint32_t field.  */
  415| 			m->physical_ram_in_mb = (uint32_t)
  416| 			    parse_int_option('M', optarg, 1, 1048576);
  417| 			machine_specific_options_used = true;
  418| 			break;
  419| 		case 'N':
  420| 			m->show_nr_of_instructions = 1;
  421| 			machine_specific_options_used = true;
  422| 			break;
  423| 		case 'n':
  424| 			/*  atoi() accepted negative counts, which later
  425| 			    feed malloc()/memset() size calculations.  */
  426| 			m->ncpus = (int)
  427| 			    parse_int_option('n', optarg, 1, 256);
  428| 			machine_specific_options_used = true;
  429| 			break;
  430| 		case 'O':
  431| 			m->force_netboot = 1;
  432| 			machine_specific_options_used = true;
  433| 			break;
  434| 		case 'o':
  435| 			CHECK_ALLOCATION(m->boot_string_argument = strdup(optarg));
  436| 			machine_specific_options_used = true;
  437| 			break;
  438| 		case 'p':
  439| 			machine_add_breakpoint_string(m, optarg);
  440| 			machine_specific_options_used = true;
  441| 			break;
  442| 		case 'Q':
  443| 			m->prom_emulation = 0;
  444| 			machine_specific_options_used = true;
  445| 			break;
  446| 		case 'q':
  447| 			quiet_mode = 1;
  448| 			break;
  449| 		case 'R':
  450| 			m->use_random_bootstrap_cpu = 1;
  451| 			machine_specific_options_used = true;
  452| 			break;
  453| 		case 'r':
  454| 			m->register_dump = 1;
  455| 			machine_specific_options_used = true;
  456| 			break;
  457| 		case 'S':
  458| 			m->random_mem_contents = 1;
  459| 			machine_specific_options_used = true;
  460| 			break;
  461| 		case 's':
  462| 			machine_statistics_init(m, optarg);
  463| 			machine_specific_options_used = true;
  464| 			break;
  465| 		case 'T':
  466| 			m->halt_on_nonexistant_memaccess = 1;
  467| 			machine_specific_options_used = true;
  468| 			break;
  469| 		case 't':
  470| 			m->show_trace_tree = 1;
  471| 			machine_specific_options_used = true;
  472| 			break;
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

End with one line: `FIXDRAFT_DEC5800NCPUSHIFT: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
