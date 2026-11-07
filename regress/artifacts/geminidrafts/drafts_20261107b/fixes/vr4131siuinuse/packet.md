# GXemul hardened fork -- DRAFT A FIX for one filed issue, `vr4131siuinuse` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `vr4131siuinuse`, state `open`, severity `MED`)

**title:** devices/dev_vr41xx.c:dev_vr41xx_init -- the VR4131 on-chip SIU is registered with the default in_use=1, so two ns16550 handles race for host stdin on the BE-300 -- WRONG-RESULT (lost console input)

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T114 (class WRONG-RESULT; reach C, configuration, debugger, host environment or a non-default build; effort: one-line; report rows: A3-11).  Source URLs: https://github.com/jroark/GXemul/commit/3c3d5cbfa23ce58718d6c1c348f44587b35c0911.  Our site at de8c7547: src/devices/dev_vr41xx.c:777-781; src/devices/device.c:266.  Portable fix: yes -- port jroark 3c3d5cb (embedded: the extra on-chip SIU registered as not in use).  Filing check (TRIAGE.md): 0 hits.  The extra SIU registered as not in use is a portable one-line fact (regress/artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md F).  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port jroark 3c3d5cb to register the extra SIU as not in use

## The code at the cited lines

### `src/devices/dev_vr41xx.c` around the row's cited line 777 (HEAD 2d25df65, lines 732-807)

```c
  732| 	INTERRUPT_CONNECT(tmps, d->giu_irq);
  733| 	snprintf(tmps, sizeof(tmps), "%s.cpu[%i].vrip.%i",
  734| 	    machine->path, machine->bootstrap_cpu, VRIP_INTR_KIU);
  735| 	INTERRUPT_CONNECT(tmps, d->kiu_irq);
  736| 
  737| 	if (machine->x11_md.in_use)
  738| 		machine->main_console_handle = d->kiu_console_handle;  
  739| 
  740| 	switch (cpumodel) {
  741| 	case 4101:
  742| 	case 4102:
  743| 	case 4111:
  744| 	case 4121:
  745| 		baseaddr = 0xb000000;
  746| 		break;
  747| 	case 4181:
  748| 		baseaddr = 0xa000000;
  749| 		dev_ram_init(machine, 0xb000000, 0x1000000, DEV_RAM_MIRROR,
  750| 		    0xa000000, NULL);
  751| 		break;
  752| 	case 4122:
  753| 	case 4131:
  754| 		baseaddr = 0xf000000;
  755| 		break;
  756| 	default:
  757| 		printf("Unimplemented VR cpu model\n");
  758| 		exit(1);
  759| 	}
  760| 
  761| 	if (d->cpumodel == 4121 || d->cpumodel == 4181)
  762| 		snprintf(tmps, sizeof(tmps), "%s.cpu[%i].3",
  763| 		    machine->path, machine->bootstrap_cpu);
  764| 	else
  765| 		snprintf(tmps, sizeof(tmps), "%s.cpu[%i].vrip.%i",
  766| 		    machine->path, machine->bootstrap_cpu, VRIP_INTR_ETIMER);
  767| 	INTERRUPT_CONNECT(tmps, d->timer_irq);
  768| 
  769| 	memory_device_register(mem, "vr41xx", baseaddr, DEV_VR41XX_LENGTH,
  770| 	    dev_vr41xx_access, (void *)d, DM_DEFAULT, NULL);
  771| 
  772| 	/*
  773| 	 *  TODO: Find out which controllers are at which addresses on
  774| 	 *  which chips.
  775| 	 */
  776| 	if (cpumodel == 4131) {
  777| 		snprintf(tmps, sizeof(tmps), "ns16550 irq=%s.cpu[%i].vrip.%i "
  778| 		    "addr=0x%" PRIx64" name2=siu", machine->path,
  779| 		    machine->bootstrap_cpu, VRIP_INTR_SIU,
  780| 		    (uint64_t) (baseaddr+0x800));
  781| 		device_add(machine, tmps);
  782| 	} else {
  783| 		/*  This is used by Linux and NetBSD:  */
  784| 		snprintf(tmps, sizeof(tmps), "ns16550 irq=%s.cpu[%i]."
  785| 		    "vrip.%i addr=0x%x name2=serial", machine->path,
  786| 		    machine->bootstrap_cpu, VRIP_INTR_SIU, 0xc000000);
  787| 		device_add(machine, tmps);
  788| 	}
  789| 
  790| 	/*  Hm... maybe this should not be here.  TODO  */
  791| 	snprintf(tmps, sizeof(tmps), "pcic irq=%s.cpu[%i].vrip.%i addr="
  792| 	    "0x140003e0", machine->path, machine->bootstrap_cpu,
  793| 	    VRIP_INTR_GIU);
  794| 	device_add(machine, tmps);
  795| 
  796| 	machine_add_tickfunction(machine, dev_vr41xx_tick, d,
  797| 	    DEV_VR41XX_TICKSHIFT);
  798| 
  799| 	/*  Some machines (?) use ISA space at 0x15000000 instead of
  800| 	    0x14000000, eg IBM WorkPad Z50.  */
  801| 	dev_ram_init(machine, 0x15000000, 0x1000000, DEV_RAM_MIRROR,
  802| 	    0x14000000, NULL);
  803| 
  804| 	return d;
  805| }
  806| 
  807| 
```

### `src/devices/device.c` around the row's cited line 266 (HEAD 2d25df65, lines 221-311)

```c
  221| 	i /= sizeof(struct device_entry);
  222| 
  223| 	free(device_entries[i].name);
  224| 	device_entries[i].name = NULL;
  225| 
  226| 	if (i == n_device_entries-1) {
  227| 		/*  Do nothing if we're removing the last array element.  */
  228| 	} else {
  229| 		/*  Remove array element i by copying the last element
  230| 		    to i's position:  */
  231| 		device_entries[i] = device_entries[n_device_entries-1];
  232| 
  233| 		/*  The array is not sorted anymore:  */
  234| 		device_entries_sorted = 0;
  235| 	}
  236| 
  237| 	n_device_entries --;
  238| 
  239| 	/*  TODO: realloc?  */
  240| 	return 1;
  241| }
  242| 
  243| 
  244| /*
  245|  *  device_add():
  246|  *
  247|  *  Add a device to a machine. For example: "kn210 addr=0x12340000" adds a
  248|  *  device called "kn210" at a specific address.
  249|  *
  250|  *  TODO: This function is quite ugly, and should be cleaned up.
  251|  */
  252| void *device_add(struct machine *machine, const char *name_and_params)
  253| {
  254| 	struct device_entry *p;
  255| 	struct devinit devinit;
  256| 	const char *s2;
  257| 	const char *s3;
  258| 	size_t len, interrupt_path_len = strlen(machine->path) + 100;
  259| 	int quoted;
  260| 
  261| 	memset(&devinit, 0, sizeof(struct devinit));
  262| 	devinit.machine = machine;
  263| 
  264| 	/*  Default values:  */
  265| 	devinit.addr_mult = 1;
  266| 	devinit.in_use = 1;
  267| 
  268| 	/*  Get the device name first:  */
  269| 	s2 = name_and_params;
  270| 	while (s2[0] != ',' && s2[0] != ' ' && s2[0] != '\0')
  271| 		s2 ++;
  272| 
  273| 	len = (size_t)s2 - (size_t)name_and_params;
  274| 	CHECK_ALLOCATION(devinit.name = (char *) malloc(len + 1));
  275| 	memcpy(devinit.name, name_and_params, len);
  276| 	devinit.name[len] = '\0';
  277| 
  278| 	/*  Allocate space for the default interrupt name:  */
  279| 	CHECK_ALLOCATION(devinit.interrupt_path = (char *)
  280| 	    malloc(interrupt_path_len + 1));
  281| 	snprintf(devinit.interrupt_path, interrupt_path_len,
  282| 	    "%s.cpu[%i]", machine->path, machine->bootstrap_cpu);
  283| 
  284| 	p = device_lookup(devinit.name);
  285| 	if (p == NULL) {
  286| 		fatal("no such device (\"%s\")\n", devinit.name);
  287| 		if (device_exit_on_error)
  288| 			exit(1);
  289| 		else
  290| 			goto return_fail;
  291| 	}
  292| 
  293| 	/*  Get params from name_and_params:  */
  294| 	while (*s2 != '\0') {
  295| 		/*  Skip spaces, commas, and semicolons:  */
  296| 		while (*s2 == ' ' || *s2 == ',' || *s2 == ';')
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

End with one line: `FIXDRAFT_VR4131SIUINUSE: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
