# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `hpcmipsalloc` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `hpcmipsalloc`, state `open`)

**title:** src/machines/machine_hpcmips.c:383,393-405 -- the Agenda VR3 boot-string buffer from malloc(1000) is written without a NULL test -- NULL (host out-of-memory only)

**state_note (head):** 

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/machines/machine_hpcmips.c` -- AT HEAD, lines 46-450 (`*` marks a line your previous draft changed)

```c
   46|  MACHINE_SETUP(hpcmips)
   47|  {
   48|  	char tmpstr[1000];
   49|  	struct hpc_bootinfo hpc_bootinfo;
   50|  	int hpc_platid_flags = 0, hpc_platid_cpu_submodel = 0,
     | [... lines 51-273 not shown ...]
  274|  		dev_vr41xx_init(machine, machine->memory, 4181);
  275|  
  276|  		/*
  277|  		 *  #444: this arm's ORDER was already right, but "irq=%i" with
  278|  		 *  8+VRIP_INTR_SIU produced the bare name "17", which is not a
  279|  		 *  registered path, so INTERRUPT_CONNECT abort()ed here too.
  280|  		 *  The two halves of the old TODO named the SAME line under
  281|  		 *  different bases -- 8+9 is exactly the 17 it attributed to
  282|  		 *  Linux -- so vrip.VRIP_INTR_SIU is what is taken.  Still
  283|  		 *  JUDGED and not measured: there is no datasheet here; only
  284|  		 *  the path FORM was measured.  See the BE-300 arm above.
  285|  		 */
  286|  		{
  287|  			int x;
  288|  			snprintf(tmpstr, sizeof(tmpstr),
  289|  			    "ns16550 irq=%s.cpu[%i].vrip.%i addr=0x0c000010",
  290|  			    machine->path, machine->bootstrap_cpu,
  291|  			    VRIP_INTR_SIU);
  292|  			x = (size_t)device_add(machine, tmpstr);
  293|  
  294|  			if (!machine->x11_md.in_use)
  295|  				machine->main_console_handle = x;
  296|  		}
  297|  
  298|  		hpc_platid_cpu_arch = 1;	/*  MIPS  */
  299|  		hpc_platid_cpu_series = 1;	/*  VR  */
  300|  		hpc_platid_cpu_model = 1;	/*  VR41XX  */
  301|  		hpc_platid_cpu_submodel = 4;	/*  VR4181  */
  302|  		hpc_platid_vendor = 15;		/*  Agenda  */
  303|  		hpc_platid_series = 1;		/*  VR  */
  304|  		hpc_platid_model = 1;		/*  VR3  */
  305|  		hpc_platid_submodel = 0;	/*  -  */
  306|  
  307|  		dev_ram_init(machine, 0x0f000000, 0x01000000,
  308|  		    DEV_RAM_MIRROR | DEV_RAM_MIGHT_POINT_TO_DEVICES, 0x0, NULL);
  309|  		break;
  310|  
  311|  	case MACHINE_HPCMIPS_IBM_WORKPAD_Z50:
  312|  		/*  131 MHz VR4121  */
  313|  		machine->machine_name = strdup("IBM Workpad Z50");
  314|  		/*  TODO:  */
  315|  		hpc_fb_addr = 0xa000000;
  316|  		hpc_fb_xsize = 640;
  317|  		hpc_fb_ysize = 480;
  318|  		hpc_fb_xsize_mem = 640;
  319|  		hpc_fb_ysize_mem = 480;
  320|  		hpc_fb_bits = 16;
  321|  		hpc_fb_encoding = BIFB_D16_0000;
  322|  
  323|  		dev_vr41xx_init(machine, machine->memory, 4121);
  324|  
  325|  		hpc_platid_cpu_arch = 1;	/*  MIPS  */
  326|  		hpc_platid_cpu_series = 1;	/*  VR  */
  327|  		hpc_platid_cpu_model = 1;	/*  VR41XX  */
  328|  		hpc_platid_cpu_submodel = 3;	/*  VR4121  */
  329|  		hpc_platid_vendor = 9;		/*  IBM  */
  330|  		hpc_platid_series = 1;		/*  WorkPad  */
  331|  		hpc_platid_model = 1;		/*  Z50  */
  332|  		hpc_platid_submodel = 0;	/*  0  */
  333|  		break;
  334|  
  335|  	default:printf("Unimplemented hpcmips machine number.\n");
  336|  		exit(1);
  337|  	}
  338|  
  339|  	store_32bit_word_in_host(cpu, (unsigned char *)&hpc_bootinfo.platid_cpu,
  340|  	      (hpc_platid_cpu_arch << 26) + (hpc_platid_cpu_series << 20)
  341|  	    + (hpc_platid_cpu_model << 14) + (hpc_platid_cpu_submodel <<  8)
  342|  	    + hpc_platid_flags);
  343|  	store_32bit_word_in_host(cpu, (unsigned char *)&hpc_bootinfo.
  344|  	    platid_machine, (hpc_platid_vendor << 22) + (hpc_platid_series<<16)
  345|  	    + (hpc_platid_model <<  8) + hpc_platid_submodel);
  346|  
  347|  	if (hpc_fb_addr != 0) {
  348|  		dev_fb_init(machine, machine->memory, hpc_fb_addr, VFB_HPC,
  349|  		    hpc_fb_xsize, hpc_fb_ysize,
  350|  		    hpc_fb_xsize_mem, hpc_fb_ysize_mem,
  351|  		    hpc_fb_bits, machine->machine_name);
  352|  
  353|  		/*  NetBSD/hpcmips uses framebuffer at physical
  354|  		    address 0x8.......:  */
  355|  		dev_ram_init(machine, 0x80000000, 0x20000000,
  356|  		    DEV_RAM_MIRROR | DEV_RAM_MIGHT_POINT_TO_DEVICES, 0x0, NULL);
  357|  	}
  358|  
  359|  	if (!machine->prom_emulation)
  360|  		return;
  361|  
  362|  
  363|  	/*  NetBSD/hpcmips and possibly others expects the following:  */
  364|  
  365|  	cpu->cd.mips.gpr[MIPS_GPR_A0] = 1;	/*  argc  */
  366|  	cpu->cd.mips.gpr[MIPS_GPR_A1] = machine->physical_ram_in_mb * 1048576
  367|  	    + 0xffffffff80000000ULL - 512;	/*  argv  */
  368|  	cpu->cd.mips.gpr[MIPS_GPR_A2] = machine->physical_ram_in_mb * 1048576
  369|  	    + 0xffffffff80000000ULL - 256;	/*  ptr to hpc_bootinfo  */
  370|  
  371|  	machine->bootstr = machine->boot_kernel_filename;
  372|  	store_32bit_word(cpu, 0x80000000ULL + (machine->physical_ram_in_mb <<
  373|  	    20) - 512, 0x80000000ULL + (machine->physical_ram_in_mb << 20)
  374|  	    - 512 + 16);
  375|  	store_32bit_word(cpu, 0x80000000ULL + (machine->physical_ram_in_mb <<
  376|  	    20) - 512 + 4, 0);
  377|  	store_string(cpu, 0x80000000ULL + (machine->physical_ram_in_mb <<
  378|  	    20) - 512 + 16, machine->bootstr);
  379|  
  380|  	/*  Special case for the Agenda VR3:  */
  381|  	if (machine->machine_subtype == MACHINE_HPCMIPS_AGENDA_VR3) {
  382|  		const int tmplen = 1000;
  383|  		char *tmp = (char *) malloc(tmplen);
  384|* 
  385|  		cpu->cd.mips.gpr[MIPS_GPR_A0] = 2;	/*  argc  */
  386|  
  387|  		store_32bit_word(cpu, 0x80000000 + machine->physical_ram_in_mb
  388|  		    * 1048576-512 + 4, 0x80000000 + machine->physical_ram_in_mb
  389|  		    * 1048576 - 512 + 64);
  390|  		store_32bit_word(cpu, 0x80000000 + machine->physical_ram_in_mb
  391|  		    * 1048576 - 512 + 8, 0);
  392|  
  393|  		snprintf(tmp, tmplen, "root=/dev/rom video=vr4181fb:xres:160,y"
  394|  		    "res:240,bpp:4,gray,hpck:3084,inv ether=0,0x03fe0300,eth0");
  395|  		tmp[tmplen-1] = '\0';
  396|  
  397|  		if (!machine->x11_md.in_use)
  398|  			snprintf(tmp+strlen(tmp), tmplen-strlen(tmp),
  399|  			    " console=ttyS0,115200");
  400|  		tmp[tmplen-1] = '\0';
  401|  
  402|  		if (machine->boot_string_argument[0])
  403|  			snprintf(tmp+strlen(tmp), tmplen-strlen(tmp), " %s",
  404|  			    machine->boot_string_argument);
  405|  		tmp[tmplen-1] = '\0';
  406|  
  407|  		store_string(cpu, 0x80000000 + machine->physical_ram_in_mb
  408|  		    * 1048576 - 512 + 64, tmp);
  409|  
  410|  		machine->bootarg = tmp;
  411|  	} else if (machine->boot_string_argument[0]) {
  412|  		cpu->cd.mips.gpr[MIPS_GPR_A0] ++;	/*  argc  */
  413|  
  414|  		store_32bit_word(cpu, 0x80000000 + machine->physical_ram_in_mb
  415|  		    * 1048576-512 + 4, 0x80000000 + machine->physical_ram_in_mb
  416|  		    * 1048576 - 512 + 64);
  417|  		store_32bit_word(cpu, 0x80000000 + machine->physical_ram_in_mb
  418|  		    * 1048576 - 512 + 8, 0);
  419|  
  420|  		store_string(cpu, 0x80000000 + machine->physical_ram_in_mb *
  421|  		    1048576 - 512 + 64, machine->boot_string_argument);
  422|  
  423|  		machine->bootarg = machine->boot_string_argument;
  424|  	}
  425|  
  426|  	store_16bit_word_in_host(cpu, (unsigned char *)&hpc_bootinfo.length,
  427|  	    sizeof(hpc_bootinfo));
  428|  	store_32bit_word_in_host(cpu, (unsigned char *)&hpc_bootinfo.magic,
  429|  	    HPC_BOOTINFO_MAGIC);
  430|  	store_32bit_word_in_host(cpu, (unsigned char *)&hpc_bootinfo.fb_addr,
  431|  	    0x80000000 + hpc_fb_addr);
  432|  	store_16bit_word_in_host(cpu, (unsigned char *)&hpc_bootinfo.
  433|  	    fb_line_bytes, hpc_fb_xsize_mem * (((hpc_fb_bits-1)|7)+1) / 8);
  434|  	store_16bit_word_in_host(cpu, (unsigned char *)&hpc_bootinfo.fb_width,
  435|  	    hpc_fb_xsize);
  436|  	store_16bit_word_in_host(cpu, (unsigned char *)&hpc_bootinfo.fb_height,
  437|  	    hpc_fb_ysize);
  438|  	store_16bit_word_in_host(cpu, (unsigned char *)&hpc_bootinfo.fb_type,
  439|  	    hpc_fb_encoding);
  440|  	store_16bit_word_in_host(cpu, (unsigned char *)&hpc_bootinfo.bi_cnuse,
  441|  	    machine->x11_md.in_use? BI_CNUSE_BUILTIN : BI_CNUSE_SERIAL);
  442|  
  443|  	/*  printf("hpc_bootinfo.platid_cpu     = 0x%08x\n",
  444|  	    hpc_bootinfo.platid_cpu);
  445|  	    printf("hpc_bootinfo.platid_machine = 0x%08x\n",
  446|  	    hpc_bootinfo.platid_machine);  */
  447|  	store_32bit_word_in_host(cpu,(unsigned char *)&hpc_bootinfo.timezone,0);
  448|  	store_buf(cpu, 0x80000000 + machine->physical_ram_in_mb *
  449|  	    1048576 - 256, (char *)&hpc_bootinfo, sizeof(hpc_bootinfo));
  450|  }
```



## Your previous draft's edits

```json
[
  {
    "file": "src/machines/machine_hpcmips.c",
    "old": "\t\tconst int tmplen = 1000;\n\t\tchar *tmp = (char *) malloc(tmplen);",
    "new": "\t\tconst int tmplen = 1000;\n\t\tchar *tmp = (char *) malloc(tmplen);\n\t\tif (tmp == NULL)\n\t\t\treturn; /* #hpcmipsalloc: avoid snprintf to NULL */",
    "why": "Add missing NULL check after malloc."
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_HPCMIPSALLOC: DEFECT, 2 FINDINGS
1. Yes, the diff removes the defect described by the issue at the named sites. By verifying `tmp` is not NULL at line 384, it prevents the uncontrolled `snprintf` writes to a NULL pointer at lines 395, 400, and 405.
2. CONTROL FLOW: Yes, the added `return;` early exit skips code the function would otherwise run, specifically the common tail of the function that writes machine state to the guest memory. Skipped tail line: `store_16bit_word_in_host(cpu, (unsigned char *)&hpc_bootinfo.length, sizeof(hpc_bootinfo));` (line 428).
3. RETURN VALUE: No path returns a different value because the function `MACHINE_SETUP(hpcmips)` implicitly has a `void` return type.
4. What ELSE does the diff change: By bypassing the remainder of the function on malloc failure, it leaves the `hpc_bootinfo` structure and other framebuffer arguments unwritten to the guest RAM, meaning the guest machine starts with incomplete/uninitialized boot metadata. 
5. House idioms: The added comment `/* #hpcmipsalloc: avoid snprintf to NULL */` fails the idiom rule because it uses a string (`hpcmipsalloc`) instead of a numeric `#NNN` tag.
src/machines/machine_hpcmips.c:385 DEFECT early return skips the function's common tail, abandoning guest boot state. Smallest fix in ONE line: `if (tmp == NULL) exit(1);`
src/machines/machine_hpcmips.c:385 STYLE comment tag uses string instead of numeric NNN format. Smallest fix in ONE line: `return; /* #123: avoid snprintf to NULL */`
FIXREVIEW_HPCMIPSALLOC: DEFECT, 2 FINDINGS
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

End with two lines: `REVISION_HPCMIPSALLOC: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_HPCMIPSALLOC: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
