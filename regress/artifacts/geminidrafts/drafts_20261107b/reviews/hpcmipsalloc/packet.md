# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `hpcmipsalloc` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `hpcmipsalloc`, state `open`)

**title:** src/machines/machine_hpcmips.c:383,393-405 -- the Agenda VR3 boot-string buffer from malloc(1000) is written without a NULL test -- NULL (host out-of-memory only)

**state_note (head):** 

**The drafter's own reading:** STILL PRESENT: YES -- src/machines/machine_hpcmips.c:383

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/machines/machine_hpcmips.c b/src/machines/machine_hpcmips.c
index 3d8eee77..2a90626b 100644
--- a/src/machines/machine_hpcmips.c
+++ b/src/machines/machine_hpcmips.c
@@ -381,6 +381,8 @@ MACHINE_SETUP(hpcmips)
 	if (machine->machine_subtype == MACHINE_HPCMIPS_AGENDA_VR3) {
 		const int tmplen = 1000;
 		char *tmp = (char *) malloc(tmplen);
+		if (tmp == NULL)
+			exit(1); /* #124: avoid snprintf to NULL */
 
 		cpu->cd.mips.gpr[MIPS_GPR_A0] = 2;	/*  argc  */
```

## Every edited function, after the fix

### `src/machines/machine_hpcmips.c` -- post-edit lines 46-452 (`+` marks a line the diff added or the point of a deletion)

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
  384|+ 		if (tmp == NULL)
  385|+ 			exit(1); /* #124: avoid snprintf to NULL */
  386|  
  387|  		cpu->cd.mips.gpr[MIPS_GPR_A0] = 2;	/*  argc  */
  388|  
  389|  		store_32bit_word(cpu, 0x80000000 + machine->physical_ram_in_mb
  390|  		    * 1048576-512 + 4, 0x80000000 + machine->physical_ram_in_mb
  391|  		    * 1048576 - 512 + 64);
  392|  		store_32bit_word(cpu, 0x80000000 + machine->physical_ram_in_mb
  393|  		    * 1048576 - 512 + 8, 0);
  394|  
  395|  		snprintf(tmp, tmplen, "root=/dev/rom video=vr4181fb:xres:160,y"
  396|  		    "res:240,bpp:4,gray,hpck:3084,inv ether=0,0x03fe0300,eth0");
  397|  		tmp[tmplen-1] = '\0';
  398|  
  399|  		if (!machine->x11_md.in_use)
  400|  			snprintf(tmp+strlen(tmp), tmplen-strlen(tmp),
  401|  			    " console=ttyS0,115200");
  402|  		tmp[tmplen-1] = '\0';
  403|  
  404|  		if (machine->boot_string_argument[0])
  405|  			snprintf(tmp+strlen(tmp), tmplen-strlen(tmp), " %s",
  406|  			    machine->boot_string_argument);
  407|  		tmp[tmplen-1] = '\0';
  408|  
  409|  		store_string(cpu, 0x80000000 + machine->physical_ram_in_mb
  410|  		    * 1048576 - 512 + 64, tmp);
  411|  
  412|  		machine->bootarg = tmp;
  413|  	} else if (machine->boot_string_argument[0]) {
  414|  		cpu->cd.mips.gpr[MIPS_GPR_A0] ++;	/*  argc  */
  415|  
  416|  		store_32bit_word(cpu, 0x80000000 + machine->physical_ram_in_mb
  417|  		    * 1048576-512 + 4, 0x80000000 + machine->physical_ram_in_mb
  418|  		    * 1048576 - 512 + 64);
  419|  		store_32bit_word(cpu, 0x80000000 + machine->physical_ram_in_mb
  420|  		    * 1048576 - 512 + 8, 0);
  421|  
  422|  		store_string(cpu, 0x80000000 + machine->physical_ram_in_mb *
  423|  		    1048576 - 512 + 64, machine->boot_string_argument);
  424|  
  425|  		machine->bootarg = machine->boot_string_argument;
  426|  	}
  427|  
  428|  	store_16bit_word_in_host(cpu, (unsigned char *)&hpc_bootinfo.length,
  429|  	    sizeof(hpc_bootinfo));
  430|  	store_32bit_word_in_host(cpu, (unsigned char *)&hpc_bootinfo.magic,
  431|  	    HPC_BOOTINFO_MAGIC);
  432|  	store_32bit_word_in_host(cpu, (unsigned char *)&hpc_bootinfo.fb_addr,
  433|  	    0x80000000 + hpc_fb_addr);
  434|  	store_16bit_word_in_host(cpu, (unsigned char *)&hpc_bootinfo.
  435|  	    fb_line_bytes, hpc_fb_xsize_mem * (((hpc_fb_bits-1)|7)+1) / 8);
  436|  	store_16bit_word_in_host(cpu, (unsigned char *)&hpc_bootinfo.fb_width,
  437|  	    hpc_fb_xsize);
  438|  	store_16bit_word_in_host(cpu, (unsigned char *)&hpc_bootinfo.fb_height,
  439|  	    hpc_fb_ysize);
  440|  	store_16bit_word_in_host(cpu, (unsigned char *)&hpc_bootinfo.fb_type,
  441|  	    hpc_fb_encoding);
  442|  	store_16bit_word_in_host(cpu, (unsigned char *)&hpc_bootinfo.bi_cnuse,
  443|  	    machine->x11_md.in_use? BI_CNUSE_BUILTIN : BI_CNUSE_SERIAL);
  444|  
  445|  	/*  printf("hpc_bootinfo.platid_cpu     = 0x%08x\n",
  446|  	    hpc_bootinfo.platid_cpu);
  447|  	    printf("hpc_bootinfo.platid_machine = 0x%08x\n",
  448|  	    hpc_bootinfo.platid_machine);  */
  449|  	store_32bit_word_in_host(cpu,(unsigned char *)&hpc_bootinfo.timezone,0);
  450|  	store_buf(cpu, 0x80000000 + machine->physical_ram_in_mb *
  451|  	    1048576 - 256, (char *)&hpc_bootinfo, sizeof(hpc_bootinfo));
  452|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_HPCMIPSALLOC: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_HPCMIPSALLOC: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
