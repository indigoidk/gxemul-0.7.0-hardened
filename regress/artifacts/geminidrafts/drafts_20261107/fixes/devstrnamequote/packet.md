# GXemul hardened fork -- DRAFT A FIX for one filed issue, `devstrnamequote` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `devstrnamequote`, state `open`, severity `LOW`)

**title:** src/devices/device.c:342-357 -- a name2= value that is a lone quote makes len2 - 2 wrap to SIZE_MAX, so snprintf() is given size 0 and the new name buffer is left unterminated -- WRAP (host device strings only)

**state_note (head):**



**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- Subtracting 2 from length 1 causes underflow to SIZE_MAX and buffer issues.

## The code at the cited lines

### `src/devices/device.c` around the row's cited line 342 (HEAD 2d25df65, lines 297-387)

```c
  297| 			s2 ++;
  298| 
  299| 		if (*s2 == '\0')
  300| 			break;
  301| 
  302| 		/*  s2 now points to the next param. eg "addr=1234"  */
  303| 
  304| 		/*  Get a word (until there is a '=' sign):  */
  305| 		s3 = s2;
  306| 		while (*s3 != '=' && *s3 != '\0')
  307| 			s3 ++;
  308| 		if (s3 == s2) {
  309| 			fatal("weird param: %s\n", s2);
  310| 			if (device_exit_on_error)
  311| 				exit(1);
  312| 			else
  313| 				goto return_fail;
  314| 		}
  315| 		s3 ++;
  316| 		/*  s3 now points to the parameter value ("1234")  */
  317| 
  318| 		if (strncmp(s2, "addr=", 5) == 0) {
  319| 			devinit.addr = mystrtoull(s3, NULL, 0);
  320| 		} else if (strncmp(s2, "addr2=", 6) == 0) {
  321| 			devinit.addr2 = mystrtoull(s3, NULL, 0);
  322| 		} else if (strncmp(s2, "len=", 4) == 0) {
  323| 			devinit.len = mystrtoull(s3, NULL, 0);
  324| 		} else if (strncmp(s2, "addr_mult=", 10) == 0) {
  325| 			devinit.addr_mult = mystrtoull(s3, NULL, 0);
  326| 		} else if (strncmp(s2, "pci_little_endian=", 18) == 0) {
  327| 			devinit.pci_little_endian = mystrtoull(s3, NULL, 0);
  328| 			switch (devinit.pci_little_endian) {
  329| 			case 0:	break;
  330| 			case 1:	devinit.pci_little_endian =
  331| 				    MEM_PCI_LITTLE_ENDIAN;
  332| 				break;
  333| 			default:fatal("Bad pci_little_endian value.\n");
  334| 				exit(1);
  335| 			}
  336| 		} else if (strncmp(s2, "irq=", 4) == 0) {
  337| 			snprintf(devinit.interrupt_path, interrupt_path_len, "%s", s3);
  338| 			if (strchr(devinit.interrupt_path, ' ') != NULL)
  339| 				*strchr(devinit.interrupt_path, ' ') = '\0';
  340| 		} else if (strncmp(s2, "in_use=", 7) == 0) {
  341| 			devinit.in_use = mystrtoull(s3, NULL, 0);
  342| 		} else if (strncmp(s2, "name2=", 6) == 0) {
  343| 			const char *h = s2 + 6;
  344| 			size_t len2 = 0;
  345| 			quoted = 0;
  346| 			while (*h) {
  347| 				if (*h == '\'')
  348| 					quoted = !quoted;
  349| 				h++, len2++;
  350| 				if (!quoted && *h == ' ')
  351| 					break;
  352| 			}
  353| 			CHECK_ALLOCATION(devinit.name2 = (char *) malloc(len2 + 1));
  354| 			h = s2 + 6;
  355| 			if (*h == '\'')
  356| 				len2 -= 2, h++;
  357| 			snprintf(devinit.name2, len2 + 1, "%s", h);
  358| 		} else {
  359| 			fatal("unknown param: %s\n", s2);
  360| 			if (device_exit_on_error)
  361| 				exit(1);
  362| 			else
  363| 				goto return_fail;
  364| 		}
  365| 
  366| 		/*  skip to the next param:  */
  367| 		s2 = s3;
  368| 		quoted = 0;
  369| 		while (*s2 != '\0' && (*s2 != ' ' || quoted) &&
  370| 		    *s2 != ',' && *s2 != ';') {
  371| 			if (*s2 == '\'')
  372| 				quoted = !quoted;
  373| 			s2 ++;
  374| 		}
  375| 	}
  376| 
  377| 
  378| 	/*
  379| 	 *  Call the init function for this device:
  380| 	 */
  381| 
  382| 	devinit.return_ptr = NULL;
  383| 
  384| 	if (!p->initf(&devinit)) {
  385| 		fatal("error adding device (\"%s\")\n", name_and_params);
  386| 		if (device_exit_on_error)
  387| 			exit(1);
```

### `src/core/emul.c` around the row's cited line 533 (HEAD 2d25df65, lines 488-578)

```c
  488| 		machine_default_cputype(m);
  489| 	if (m->ncpus == 0)
  490| 		m->ncpus = 1;
  491| 
  492| 	CHECK_ALLOCATION(m->cpus = (struct cpu **) malloc(sizeof(struct cpu *) * m->ncpus));
  493| 	memset(m->cpus, 0, sizeof(struct cpu *) * m->ncpus);
  494| 
  495| 	char cpuname[200];
  496| 	if (m->ncpus == 1)
  497| 		snprintf(cpuname, sizeof(cpuname), "cpu0");
  498| 	else
  499| 		snprintf(cpuname, sizeof(cpuname), "cpu0 .. cpu%i", m->ncpus - 1);
  500| 
  501| 	for (i=0; i<m->ncpus; i++) {
  502| 		m->cpus[i] = cpu_new(m->memory, m, i, m->cpu_name);
  503| 		if (m->cpus[i] == NULL) {
  504| 			fprintf(stderr, "Unable to create CPU object. "
  505| 			    "Aborting.");
  506| 			return false;
  507| 		}
  508| 	}
  509| 
  510| 	if (m->use_random_bootstrap_cpu)
  511| 		m->bootstrap_cpu = random() % m->ncpus;
  512| 	else
  513| 		m->bootstrap_cpu = 0;
  514| 
  515| 	cpu = m->cpus[m->bootstrap_cpu];
  516| 
  517| 	if (m->x11_md.in_use)
  518| 		x11_init(m);
  519| 
  520| 	/*  Fill the directly addressable memory with random bytes:  */
  521| 	if (m->random_mem_contents) {
  522| 		for (i=0; i<(int)memory_amount; i+=256) {
  523| 			unsigned char data[256];
  524| 			unsigned int j;
  525| 			for (j=0; j<sizeof(data); j++)
  526| 				data[j] = random() & 255;
  527| 			cpu->memory_rw(cpu, m->memory, i, data, sizeof(data),
  528| 			    MEM_WRITE, CACHE_NONE | NO_EXCEPTIONS | PHYSICAL);
  529| 		}
  530| 	}
  531| 
  532| 	for (i=0; i<n_devices; i++)
  533| 		device_add(m, device_names[i]);
  534| 
  535| 	machine_setup(m);
  536| 
  537| 	cpu_dumpinfo(m, cpu, false);
  538| 	debugmsg(SUBSYS_MACHINE, "memory", VERBOSITY_INFO, "%s", meminfo);
  539| 	diskimage_dump_info(m);
  540| 	console_debug_dump(m);
  541| 
  542| 	/*  Load files (ROM code, boot code, ...) into memory:  */
  543| 	if (n_load == 0) {
  544| 		if (m->first_diskimage != NULL) {
  545| 			if (!load_bootblock(m, cpu, &n_load, &load_names)) {
  546| 				fprintf(stderr, "\nNo executable files were"
  547| 				    " specified, and booting directly from disk"
  548| 				    " failed.\n");
  549| 				return false;
  550| 			}
  551| 		} else {
  552| 			fprintf(stderr, "No executable file(s) loaded, and "
  553| 			    "we are not booting directly from a disk image."
  554| 			    "\nAborting.\n");
  555| 			return false;
  556| 		}
  557| 	}
  558| 
  559| 	while (n_load > 0) {
  560| 		FILE *tmp_f;
  561| 		char *name_to_load = *load_names;
  562| 		int remove_after_load = 0;
  563| 		char *gunzip_temp_name = NULL;
  564| 
  565| 		/*  Special hack for removing temporary files:  */
  566| 		if (name_to_load[0] == 8) {
  567| 			name_to_load ++;
  568| 			remove_after_load = 1;
  569| 		}
  570| 
  571| 		/*
  572| 		 *  gzipped files are automagically gunzipped, by running
  573| 		 *  gunzip via fork()/exec() (never via a shell) into a fresh
  574| 		 *  temporary file.
  575| 		 */
  576| 		tmp_f = fopen(name_to_load, "r");
  577| 		if (tmp_f != NULL) {
  578| 			unsigned char buf[2];		/*  gzip header  */
```

### `src/debugger/debugger_cmds.c` around the row's cited line 553 (HEAD 2d25df65, lines 508-598)

```c
  508| 		printf("syntax: continue\n");
  509| 		return;
  510| 	}
  511| 
  512| 	exit_debugger = true;
  513| }
  514| 
  515| 
  516| /*
  517|  *  debugger_cmd_device():
  518|  */
  519| static void debugger_cmd_device(struct machine *m, char *args)
  520| {
  521| 	int i;
  522| 	struct memory *mem;
  523| 	struct cpu *c;
  524| 
  525| 	if (args[0] == '\0')
  526| 		goto return_help;
  527| 
  528| 	if (m->cpus == NULL) {
  529| 		printf("No cpus (?)\n");
  530| 		return;
  531| 	}
  532| 	c = m->cpus[m->bootstrap_cpu];
  533| 	if (c == NULL) {
  534| 		printf("m->cpus[m->bootstrap_cpu] = NULL\n");
  535| 		return;
  536| 	}
  537| 	mem = m->cpus[m->bootstrap_cpu]->mem;
  538| 
  539| 	if (m->cpus == NULL) {
  540| 		printf("No cpus (?)\n");
  541| 		return;
  542| 	}
  543| 	c = m->cpus[m->bootstrap_cpu];
  544| 	if (c == NULL) {
  545| 		printf("m->cpus[m->bootstrap_cpu] = NULL\n");
  546| 		return;
  547| 	}
  548| 	mem = m->cpus[m->bootstrap_cpu]->mem;
  549| 
  550| 	if (strcmp(args, "all") == 0) {
  551| 		device_dumplist();
  552| 	} else if (strncmp(args, "add ", 4) == 0) {
  553| 		device_add(m, args+4);
  554| 	} else if (strcmp(args, "consoles") == 0) {
  555| 		console_debug_dump(m);
  556| 	} else if (strncmp(args, "remove ", 7) == 0) {
  557| 		i = atoi(args + 7);
  558| 		if (i==0 && args[7]!='0') {
  559| 			printf("Weird device number. Use 'device list'.\n");
  560| 		} else
  561| 			memory_device_remove(m->memory, i);
  562| 	} else if (strcmp(args, "list") == 0) {
  563| 		if (mem->n_mmapped_devices == 0)
  564| 			printf("No memory-mapped devices in this machine.\n");
  565| 
  566| 		for (i=0; i<mem->n_mmapped_devices; i++) {
  567| 			printf("%2i: %25s @ 0x%011" PRIx64", len = 0x%" PRIx64,
  568| 			    i, mem->devices[i].name,
  569| 			    (uint64_t) mem->devices[i].baseaddr,
  570| 			    (uint64_t) mem->devices[i].length);
  571| 
  572| 			if (mem->devices[i].flags) {
  573| 				printf(" (");
  574| 				if (mem->devices[i].flags & DM_DYNTRANS_OK)
  575| 					printf("DYNTRANS R");
  576| 				if (mem->devices[i].flags &DM_DYNTRANS_WRITE_OK)
  577| 					printf("+W");
  578| 				printf(")");
  579| 			}
  580| 			printf("\n");
  581| 		}
  582| 	} else
  583| 		goto return_help;
  584| 
  585| 	return;
  586| 
  587| return_help:
  588| 	printf("syntax: devices cmd [...]\n");
  589| 	printf("Available cmds are:\n");
  590| 	printf("  add name_and_params    add a device to the current "
  591| 	    "machine\n");
  592| 	printf("  all                    list all registered devices\n");
  593| 	printf("  consoles               list all slave consoles\n");
  594| 	printf("  list                   list memory-mapped devices in the"
  595| 	    " current machine\n");
  596| 	printf("  remove x               remove device nr x from the "
  597| 	    "current machine\n");
  598| }
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

End with one line: `FIXDRAFT_DEVSTRNAMEQUOTE: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
