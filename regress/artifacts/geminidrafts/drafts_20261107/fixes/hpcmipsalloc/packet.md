# GXemul hardened fork -- DRAFT A FIX for one filed issue, `hpcmipsalloc` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `hpcmipsalloc`, state `open`, severity `LOW`)

**title:** src/machines/machine_hpcmips.c:383,393-405 -- the Agenda VR3 boot-string buffer from malloc(1000) is written without a NULL test -- NULL (host out-of-memory only)

**state_note (head):**



**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- Unchecked malloc allows snprintf to write to a NULL pointer if allocation fails.

## The code at the cited lines

### `src/machines/machine_hpcmips.c` around the row's cited line 383 (HEAD 2d25df65, lines 338-428)

```c
  338| 
  339| 	store_32bit_word_in_host(cpu, (unsigned char *)&hpc_bootinfo.platid_cpu,
  340| 	      (hpc_platid_cpu_arch << 26) + (hpc_platid_cpu_series << 20)
  341| 	    + (hpc_platid_cpu_model << 14) + (hpc_platid_cpu_submodel <<  8)
  342| 	    + hpc_platid_flags);
  343| 	store_32bit_word_in_host(cpu, (unsigned char *)&hpc_bootinfo.
  344| 	    platid_machine, (hpc_platid_vendor << 22) + (hpc_platid_series<<16)
  345| 	    + (hpc_platid_model <<  8) + hpc_platid_submodel);
  346| 
  347| 	if (hpc_fb_addr != 0) {
  348| 		dev_fb_init(machine, machine->memory, hpc_fb_addr, VFB_HPC,
  349| 		    hpc_fb_xsize, hpc_fb_ysize,
  350| 		    hpc_fb_xsize_mem, hpc_fb_ysize_mem,
  351| 		    hpc_fb_bits, machine->machine_name);
  352| 
  353| 		/*  NetBSD/hpcmips uses framebuffer at physical
  354| 		    address 0x8.......:  */
  355| 		dev_ram_init(machine, 0x80000000, 0x20000000,
  356| 		    DEV_RAM_MIRROR | DEV_RAM_MIGHT_POINT_TO_DEVICES, 0x0, NULL);
  357| 	}
  358| 
  359| 	if (!machine->prom_emulation)
  360| 		return;
  361| 
  362| 
  363| 	/*  NetBSD/hpcmips and possibly others expects the following:  */
  364| 
  365| 	cpu->cd.mips.gpr[MIPS_GPR_A0] = 1;	/*  argc  */
  366| 	cpu->cd.mips.gpr[MIPS_GPR_A1] = machine->physical_ram_in_mb * 1048576
  367| 	    + 0xffffffff80000000ULL - 512;	/*  argv  */
  368| 	cpu->cd.mips.gpr[MIPS_GPR_A2] = machine->physical_ram_in_mb * 1048576
  369| 	    + 0xffffffff80000000ULL - 256;	/*  ptr to hpc_bootinfo  */
  370| 
  371| 	machine->bootstr = machine->boot_kernel_filename;
  372| 	store_32bit_word(cpu, 0x80000000ULL + (machine->physical_ram_in_mb <<
  373| 	    20) - 512, 0x80000000ULL + (machine->physical_ram_in_mb << 20)
  374| 	    - 512 + 16);
  375| 	store_32bit_word(cpu, 0x80000000ULL + (machine->physical_ram_in_mb <<
  376| 	    20) - 512 + 4, 0);
  377| 	store_string(cpu, 0x80000000ULL + (machine->physical_ram_in_mb <<
  378| 	    20) - 512 + 16, machine->bootstr);
  379| 
  380| 	/*  Special case for the Agenda VR3:  */
  381| 	if (machine->machine_subtype == MACHINE_HPCMIPS_AGENDA_VR3) {
  382| 		const int tmplen = 1000;
  383| 		char *tmp = (char *) malloc(tmplen);
  384| 
  385| 		cpu->cd.mips.gpr[MIPS_GPR_A0] = 2;	/*  argc  */
  386| 
  387| 		store_32bit_word(cpu, 0x80000000 + machine->physical_ram_in_mb
  388| 		    * 1048576-512 + 4, 0x80000000 + machine->physical_ram_in_mb
  389| 		    * 1048576 - 512 + 64);
  390| 		store_32bit_word(cpu, 0x80000000 + machine->physical_ram_in_mb
  391| 		    * 1048576 - 512 + 8, 0);
  392| 
  393| 		snprintf(tmp, tmplen, "root=/dev/rom video=vr4181fb:xres:160,y"
  394| 		    "res:240,bpp:4,gray,hpck:3084,inv ether=0,0x03fe0300,eth0");
  395| 		tmp[tmplen-1] = '\0';
  396| 
  397| 		if (!machine->x11_md.in_use)
  398| 			snprintf(tmp+strlen(tmp), tmplen-strlen(tmp),
  399| 			    " console=ttyS0,115200");
  400| 		tmp[tmplen-1] = '\0';
  401| 
  402| 		if (machine->boot_string_argument[0])
  403| 			snprintf(tmp+strlen(tmp), tmplen-strlen(tmp), " %s",
  404| 			    machine->boot_string_argument);
  405| 		tmp[tmplen-1] = '\0';
  406| 
  407| 		store_string(cpu, 0x80000000 + machine->physical_ram_in_mb
  408| 		    * 1048576 - 512 + 64, tmp);
  409| 
  410| 		machine->bootarg = tmp;
  411| 	} else if (machine->boot_string_argument[0]) {
  412| 		cpu->cd.mips.gpr[MIPS_GPR_A0] ++;	/*  argc  */
  413| 
  414| 		store_32bit_word(cpu, 0x80000000 + machine->physical_ram_in_mb
  415| 		    * 1048576-512 + 4, 0x80000000 + machine->physical_ram_in_mb
  416| 		    * 1048576 - 512 + 64);
  417| 		store_32bit_word(cpu, 0x80000000 + machine->physical_ram_in_mb
  418| 		    * 1048576 - 512 + 8, 0);
  419| 
  420| 		store_string(cpu, 0x80000000 + machine->physical_ram_in_mb *
  421| 		    1048576 - 512 + 64, machine->boot_string_argument);
  422| 
  423| 		machine->bootarg = machine->boot_string_argument;
  424| 	}
  425| 
  426| 	store_16bit_word_in_host(cpu, (unsigned char *)&hpc_bootinfo.length,
  427| 	    sizeof(hpc_bootinfo));
  428| 	store_32bit_word_in_host(cpu, (unsigned char *)&hpc_bootinfo.magic,
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

End with one line: `FIXDRAFT_HPCMIPSALLOC: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
