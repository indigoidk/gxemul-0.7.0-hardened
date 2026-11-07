# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `pmax3minslotnr` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `pmax3minslotnr`, state `open`)

**title:** machines/machine_pmax.c 3MIN arm -- option slots 1 and 2 are registered as slot 0 (feeds only a debug message) -- HYGIENE (cosmetic)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T152 (class HYGIENE; reach C, configuration, debugger, host environment or a non-default build; effort: one-line; report rows: A2-46).  Source URLs: https://github.com/rpajarola/gxemul/commit/042b61b040deedf4c1aafb361a563fdc4f9eedb9.  Our site at de8c7547: src/machines/machine_pmax.c:330, :338.  Portable fix: yes -- port rpajarola 042b61b.  Filing check (TRIAGE.md): 0 hits.  Reach C, not build-only (regress/artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md B).  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- 330, 338

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/machines/machine_pmax.c b/src/machines/machine_pmax.c
index 19d37605..d698b6b0 100644
--- a/src/machines/machine_pmax.c
+++ b/src/machines/machine_pmax.c
@@ -327,7 +327,7 @@ MACHINE_SETUP(pmax)
 
 		snprintf(tmpstr, sizeof(tmpstr), "%s.cpu[%i].%i",
 		    machine->path, machine->bootstrap_cpu, KMIN_INT_TC1);
-		dev_turbochannel_init(machine, mem, 0,
+		dev_turbochannel_init(machine, mem, 1,
 		    KMIN_PHYS_TC_1_START, KMIN_PHYS_TC_1_END,
 		    machine->n_gfx_cards >= 2?
 			turbochannel_default_gfx_card : "",
@@ -335,7 +335,7 @@ MACHINE_SETUP(pmax)
 
 		snprintf(tmpstr, sizeof(tmpstr), "%s.cpu[%i].%i",
 		    machine->path, machine->bootstrap_cpu, KMIN_INT_TC2);
-		dev_turbochannel_init(machine, mem, 0,
+		dev_turbochannel_init(machine, mem, 2,
 		    KMIN_PHYS_TC_2_START, KMIN_PHYS_TC_2_END,
 		    machine->n_gfx_cards >= 3?
 			turbochannel_default_gfx_card : "",
```

## Every edited function, after the fix

### `src/machines/machine_pmax.c` -- post-edit lines 57-951 (`+` marks a line the diff added or the point of a deletion)

```c
   57|  MACHINE_SETUP(pmax)
   58|  {
   59|  	const char *framebuffer_console_name, *serial_console_name;
   60|  	char bootpath[200];
   61|  	char *init_bootpath;
     | [... lines 62-219 not shown ...]
  220|  
  221|  		/*  TURBOchannel slot 5 is PMAZ-AA ("asc" SCSI).  */
  222|  		snprintf(tmpstr, sizeof(tmpstr), "%s.cpu[%i].2.kn02.%i",
  223|  		    machine->path, machine->bootstrap_cpu, 5);
  224|  		dev_turbochannel_init(machine, mem, 5,
  225|  		    KN02_PHYS_TC_5_START, KN02_PHYS_TC_5_END,
  226|  		    "PMAZ-AA", tmpstr);
  227|  
  228|  		/*  TURBOchannel slot 6 is PMAD-AA ("le" ethernet).  */
  229|  		snprintf(tmpstr, sizeof(tmpstr), "%s.cpu[%i].2.kn02.%i",
  230|  		    machine->path, machine->bootstrap_cpu, 6);
  231|  		dev_turbochannel_init(machine, mem, 6,
  232|  		    KN02_PHYS_TC_6_START, KN02_PHYS_TC_6_END,
  233|  		    "PMAD-AA", tmpstr);
  234|  
  235|  		/*  TURBOchannel slot 7 is system stuff.  */
  236|  		snprintf(tmpstr, sizeof(tmpstr), "%s.cpu[%i].2.kn02.%i",
  237|  		    machine->path, machine->bootstrap_cpu, 7);
  238|  		machine->main_console_handle =
  239|  		    dev_dc7085_init(machine, mem,
  240|  		    KN02_SYS_DZ, tmpstr, machine->x11_md.in_use);
  241|  
  242|  		snprintf(tmpstr, sizeof(tmpstr), "%s.cpu[%i].%i",
  243|  		    machine->path, machine->bootstrap_cpu, KN02_INT_CLOCK);
  244|  		dev_mc146818_init(machine, mem,
  245|  		    KN02_SYS_CLOCK, tmpstr, MC146818_DEC, 1);
  246|  
  247|  		framebuffer_console_name = "osconsole=0,7";
  248|  								/*  fb,keyb  */
  249|  		serial_console_name      = "osconsole=2";
  250|  		boot_scsi_boardnumber = 5;
  251|  		boot_net_boardnumber = 6;	/*  TODO: 3?  */
  252|  		break;
  253|  
  254|  	case MACHINE_DEC_3MIN_5000:		/*  type 3, KN02BA  */
  255|  		machine->machine_name = strdup("DECstation 5000/112, 125, or 145 (3MIN,"
  256|  		    " KN02BA)");
  257|  		if (machine->emulated_hz == 0)
  258|  			machine->emulated_hz = 33000000;
  259|  		if (machine->physical_ram_in_mb > 128)
  260|  			fprintf(stderr, "WARNING! Real 3MIN machines cannot "
  261|  			    "have more than 128MB RAM. Continuing anyway.\n");
  262|  
  263|  		/*  KN02BA "3min" TurboChannel interrupt controller:  */
  264|  		snprintf(tmpstr, sizeof(tmpstr), "kn02ba irq=%s.cpu[%i].%i",
  265|  		    machine->path, machine->bootstrap_cpu, KMIN_INT_TC3);
  266|  		device_add(machine, tmpstr);
  267|  
  268|  		/*
  269|  		 *  tc0 at mainbus0: 12.5 MHz clock  (0x10000000,slotsize=64MB)
  270|  		 *  tc slot 1:   0x14000000
  271|  		 *  tc slot 2:   0x18000000
  272|  		 *  ioasic0 at tc0 slot 3 offset 0x0	(0x1c000000) slot 0
  273|  		 *  asic regs				(0x1c040000) slot 1
  274|  		 *  station's ether address		(0x1c080000) slot 2
  275|  		 *  le0 at ioasic0 offset 0xc0000: address 00:00:00:00:00:00
  276|  		 *					(0x1c0c0000) slot 3
  277|  		 *  scc0 at ioasic0 offset 0x100000	(0x1c100000) slot 4
  278|  		 *  scc1 at ioasic0 offset 0x180000: console(0x1c180000) slot 6
  279|  		 *  mcclock0 at ioasic0 offset 0x200000: mc146818 or
  280|  		 *	compatible			(0x1c200000) slot 8
  281|  		 *  asc0 at ioasic0 offset 0x300000: NCR53C94, 25MHz,
  282|  		 *	SCSI ID 7			(0x1c300000) slot 12
  283|  		 *  dma for asc0			(0x1c380000) slot 14
  284|  		 */
  285|  
  286|  ////fatal("TODO: kmin dev_le_init.\n");
  287|  ////abort();
  288|  //		dev_le_init(machine, mem, 0x1c0c0000, 0, 0,
  289|  //		    KMIN_INTR_LANCE + 8, 4 * 65536);
  290|  
  291|  		snprintf(tmpstr, sizeof(tmpstr), "%s.cpu[%i].%i.kn02ba.0x%x",
  292|  		    machine->path, machine->bootstrap_cpu, KMIN_INT_TC3, KMIN_INTR_SCC_0);
  293|  		dev_scc_init(machine, mem, 0x1c100000, tmpstr,
  294|  		    machine->x11_md.in_use, 0, 1);
  295|  
  296|  		snprintf(tmpstr, sizeof(tmpstr), "%s.cpu[%i].%i.kn02ba.0x%x",
  297|  		    machine->path, machine->bootstrap_cpu, KMIN_INT_TC3, KMIN_INTR_SCC_1);
  298|  		dev_scc_init(machine, mem, 0x1c180000, tmpstr,
  299|  		    machine->x11_md.in_use, 1, 1);
  300|  
  301|  
  302|  		snprintf(tmpstr, sizeof(tmpstr), "%s.cpu[%i].%i.kn02ba.0x%x",
  303|  		    machine->path, machine->bootstrap_cpu, KMIN_INT_TC3, KMIN_INTR_CLOCK);
  304|  		dev_mc146818_init(machine, mem,
  305|  		    KMIN_SYS_CLOCK, tmpstr, MC146818_DEC, 1);
  306|  		    
  307|  		snprintf(tmpstr, sizeof(tmpstr), "%s.cpu[%i].%i.kn02ba.0x%x",
  308|  		    machine->path, machine->bootstrap_cpu, KMIN_INT_TC3, KMIN_INTR_SCSI);
  309|  		dev_asc_init(machine, mem, 0x1c300000, tmpstr,
  310|  		    NULL, DEV_ASC_DEC, NULL, NULL);
  311|  
  312|  		/*
  313|  		 *  TURBOchannel slots 0, 1, and 2 are free for
  314|  		 *  option cards.  These are by default filled with
  315|  		 *  zero or more graphics boards.
  316|  		 *
  317|  		 *  TODO: irqs 
  318|  		 */
  319|  
  320|  		snprintf(tmpstr, sizeof(tmpstr), "%s.cpu[%i].%i",
  321|  		    machine->path, machine->bootstrap_cpu, KMIN_INT_TC0);
  322|  		dev_turbochannel_init(machine, mem, 0,
  323|  		    KMIN_PHYS_TC_0_START, KMIN_PHYS_TC_0_END,
  324|  		    machine->n_gfx_cards >= 1?
  325|  			turbochannel_default_gfx_card : "",
  326|  		    tmpstr);
  327|  
  328|  		snprintf(tmpstr, sizeof(tmpstr), "%s.cpu[%i].%i",
  329|  		    machine->path, machine->bootstrap_cpu, KMIN_INT_TC1);
  330|+ 		dev_turbochannel_init(machine, mem, 1,
  331|  		    KMIN_PHYS_TC_1_START, KMIN_PHYS_TC_1_END,
  332|  		    machine->n_gfx_cards >= 2?
  333|  			turbochannel_default_gfx_card : "",
  334|  		    tmpstr);
  335|  
  336|  		snprintf(tmpstr, sizeof(tmpstr), "%s.cpu[%i].%i",
  337|  		    machine->path, machine->bootstrap_cpu, KMIN_INT_TC2);
  338|+ 		dev_turbochannel_init(machine, mem, 2,
  339|  		    KMIN_PHYS_TC_2_START, KMIN_PHYS_TC_2_END,
  340|  		    machine->n_gfx_cards >= 3?
  341|  			turbochannel_default_gfx_card : "",
  342|  		    tmpstr);
  343|  
  344|  		/*  (kmin shared irq numbers (IP) are offset by +8 in the
  345|  		    emulator)  */
  346|  		/*  kmin_csr = dev_kmin_init(cpu, mem, KMIN_REG_INTR);  */
  347|  
  348|  		framebuffer_console_name = "osconsole=0,3";	/* fb,keyb(?) */
  349|  		serial_console_name      = "osconsole=3";	/* ? */
  350|  		break;
  351|  
  352|  	case MACHINE_DEC_3MAXPLUS_5000:	/*  type 4, KN03  */
  353|  		machine->machine_name = strdup("DECsystem 5900 or 5000 (3MAX+) (KN03)");
  354|  
  355|  		/*  5000/240 (KN03-GA, R3000): 40 MHz  */
  356|  		/*  5000/260 (KN05-NB, R4000): 60 MHz  */
  357|  		/*  TODO: are both these type 4?  */
  358|  		if (machine->emulated_hz == 0)
  359|  			machine->emulated_hz = 40000000;
  360|  		if (machine->physical_ram_in_mb > 480)
  361|  			fprintf(stderr, "WARNING! Real KN03 machines cannot "
  362|  			    "have more than 480MB RAM. Continuing anyway.\n");
  363|  
  364|  		/*  KN03 interrupts:  */
  365|  fatal("TODO: Legacy rewrite\n");
  366|  abort();
  367|  //		machine->md_interrupt = kn03_interrupt;
  368|  
  369|  		/*
  370|  		 *  tc0 at mainbus0: 25 MHz clock (slot 0)	(0x1e000000)
  371|  		 *  tc0 slot 1					(0x1e800000)
  372|  		 *  tc0 slot 2					(0x1f000000)
  373|  		 *  ioasic0 at tc0 slot 3 offset 0x0		(0x1f800000)
  374|  		 *    something that has to do with interrupts? (?)(0x1f840000?)
  375|  		 *  le0 at ioasic0 offset 0xc0000		(0x1f8c0000)
  376|  		 *  scc0 at ioasic0 offset 0x100000		(0x1f900000)
  377|  		 *  scc1 at ioasic0 offset 0x180000: console	(0x1f980000)
  378|  		 *  mcclock0 at ioasic0 offset 0x200000: mc146818 or
  379|  		 *	compatible				(0x1fa00000)
  380|  		 *  asc0 at ioasic0 offset 0x300000: NCR53C94, 25MHz,
  381|  		 *	SCSI ID 7				(0x1fb00000)
  382|  		 */
  383|  fatal("TODO: dec_ioasic legacy rewrite\n");
  384|  abort();
  385|  //		machine->md_int.dec_ioasic_data = dev_dec_ioasic_init(cpu,
  386|  //		    mem, 0x1f800000, 0);
  387|  
  388|  fatal("TODO: kn03 dev_le_init rewrite\n");
  389|  abort();
  390|  //		dev_le_init(machine, mem, KN03_SYS_LANCE, 0, 0,
  391|  //		    KN03_INTR_LANCE +8, 4 * 65536);
  392|  
  393|  fatal("TODO: dec_ioasic legacy rewrite\n");
  394|  abort();
  395|  //		machine->md_int.dec_ioasic_data->dma_func[3] =
  396|  //		    dev_scc_dma_func;
  397|  //		machine->md_int.dec_ioasic_data->dma_func_extra[2] =
  398|  //		    dev_scc_init(machine, mem, KN03_SYS_SCC_0,
     | [... lines 399-921 not shown ...]
  922|  		snprintf(tmps, sizeof(tmps), "bitmap=0x%" PRIx32, (uint32_t)
  923|  		    ( (DEC_MEMMAP_ADDR + sizeof(uint32_t) /* skip the
  924|  			page size and point to the memmap */
  925|  		    ) & 0xffffffffULL) );
  926|  		tmps[sizeof(tmps)-1] = '\0';
  927|  		add_environment_string(cpu, tmps, &addr);
  928|  
  929|  		snprintf(tmps, sizeof(tmps), "bitmaplen=0x%" PRIx32, (uint32_t)
  930|  		    ( machine->physical_ram_in_mb * 1048576 / 4096 / 8) );
  931|  		tmps[sizeof(tmps)-1] = '\0';
  932|  		add_environment_string(cpu, tmps, &addr);
  933|  	}
  934|  
  935|  	add_environment_string(cpu, "scsiid0=7", &addr);
  936|  	add_environment_string(cpu, "bootmode=a", &addr);
  937|  	add_environment_string(cpu, "testaction=q", &addr);
  938|  	add_environment_string(cpu, "haltaction=h", &addr);
  939|  	add_environment_string(cpu, "more=24", &addr);
  940|  
  941|  	/*  Used in at least Ultrix on the 5100:  */
  942|  	add_environment_string(cpu, "scsiid=7", &addr);
  943|  	add_environment_string(cpu, "baud0=9600", &addr);
  944|  	add_environment_string(cpu, "baud1=9600", &addr);
  945|  	add_environment_string(cpu, "baud2=9600", &addr);
  946|  	add_environment_string(cpu, "baud3=9600", &addr);
  947|  	add_environment_string(cpu, "iooption=0x1", &addr);
  948|  
  949|  	/*  The end:  */
  950|  	add_environment_string(cpu, "", &addr);
  951|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_PMAX3MINSLOTNR: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_PMAX3MINSLOTNR: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
