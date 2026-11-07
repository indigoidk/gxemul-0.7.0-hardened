# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `ctorabortclass` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `ctorabortclass`, state `held`)

**title:** ctorabortclass  The same construction abort fires on NINE subtypes across FIVE machines -- the alpha instance was recorded as LATENT and UNADVERTISED, and MEASURED 2026-09-07 as both advertised and aborting

**state_note (head):** *** CENSUS CORRECTED 2026-09-07 BY MEASUREMENT.  EIGHT/FOUR -> NINE/FIVE. ***

The record distinguished `machine_alpha.c:71`'s `z8530 irq=0` from the eight as *"one genuinely LATENT
instance ... which `-H` never advertises, and all three alpha subtypes construct."*  **Both halves are
false and the instance is live.**

    -H lists FOUR alpha subtypes and names DEC 3000/300 among them (registered at machine_alpha.c:248)

    alphabook1         rc=124   CONSTRUCTED and RUNNING
    alphaserver4100    rc=124   CONSTRUCTED and RUNNING
    3000/300           rc=134   ABORT (SIGABRT): interrupt_handler_lookup("0") failed.
    eb164              rc=124   CONSTRUCTED and RUNNING

Evidence: `regress/artifacts/ctorabortclass/alpha_census_20260907.txt`.  The abort precedes the `model:`
line and `file: loading`, so it is machine CONSTRUCTION -- a rung-2 witness -- and reproduces with and
without `-x`.

**It is this class's own named mechanism on a fifth machine.**  `machine_sgi.c:142` already records ip27
dying *"inside its own device_add(), at interrupt_handler_lookup() <- devinit_z8530(), on its irq=0"*.

**The likely cause of the wrong record, and it is the more useful half:** the SGI census was MEASURED by
sweeping every advertised subtype; the Alpha sentence beside it reads as though it shares that
measurement and was almost certainly inferred from the arm's shape -- a bare `device_add` with no
`abort()` in it.  `machine_sgi.c`'s own comment warns of exactly that: *"reading for abort() misses an
abort raised by a callee."*  **A measured census with an unmeasured sentence appended inherits the
census's authority.**

*Found while establishing whether the Alpha family is reachable at all, for [[alphaswpctxptbr]] and
[[alphapfnoffset]] -- whose own reachability verdict was UNSETTLED.  That question now has a partial
answer worth carrying: THREE of four alpha subtypes construct and execute, so the Alpha rows are not
a dead family, and the fourth is this abort.*

**The drafter's own reading:** STILL PRESENT: YES -- `src/machines/machine_sgi.c` lines 170-171, 227-228, 231-234.

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/machines/machine_sgi.c b/src/machines/machine_sgi.c
index e1e0fcfa..30eecd2e 100644
--- a/src/machines/machine_sgi.c
+++ b/src/machines/machine_sgi.c
@@ -168,7 +168,7 @@ MACHINE_SETUP(sgi)
 		strlcat(machineName,
 		    " (Everest IP19)", MACHINE_NAME_MAXBUF);
 		machine->main_console_handle = (size_t)device_add(machine,
-		    "z8530 addr=0x1fbd9830 irq=0 addr_mult=4");
+		    "z8530 addr=0x1fbd9830 addr_mult=4");
 
 		fatal("TODO ip19 interrupt rewrite\n");
 		abort();
@@ -225,13 +225,13 @@ abort();
 		    TODO (or in dev_sgi_ip20?)  */
 
 		machine->main_console_handle = (size_t)device_add(machine,
-		    "z8530 addr=0x1fbd9830 irq=0 addr_mult=4");
+		    "z8530 addr=0x1fbd9830 addr_mult=4");
 
 		/*  This is the zsc0 reported by NetBSD:  TODO: irqs  */
 		machine->main_console_handle = (size_t)device_add(machine,
-		    "z8530 addr=0x1fb80d10 irq=0 addr_mult=4");
+		    "z8530 addr=0x1fb80d10 addr_mult=4");
 		machine->main_console_handle = (size_t)device_add(machine,
-		    "z8530 addr=0x1fb80d00 irq=0 addr_mult=4");
+		    "z8530 addr=0x1fb80d00 addr_mult=4");
 
 		/*  WDSC SCSI controller:  */
 /*		dev_wdsc_init(machine, mem, 0x1fb8011f, 0, 0);  */
```

## Every edited function, after the fix

### `src/machines/machine_sgi.c` -- post-edit lines 59-684 (`+` marks a line the diff added or the point of a deletion)

```c
   59|  MACHINE_SETUP(sgi)
   60|  {
   61|  	uint64_t sgi_ram_offset = 0;
   62|  	int arc_wordlen = sizeof(uint32_t);
   63|  	struct memory *mem = machine->memory;
   64|  	char tmpstr[1000];
   65|  	int i, j;
   66|  	unsigned char macaddr[6];
   67|  	char *machineName;
   68|  
   69|  	struct pci_data *pci_data = NULL;
   70|  
   71|  	CHECK_ALLOCATION(machineName = (char *) malloc(MACHINE_NAME_MAXBUF));
   72|  	machine->machine_name = machineName;
   73|  
   74|  	cpu->byte_order = EMUL_BIG_ENDIAN;
   75|  	snprintf(machineName, MACHINE_NAME_MAXBUF,
   76|  	    "SGI-IP%i", machine->machine_subtype);
   77|  
   78|  	sgi_ram_offset = 1048576 * machine->memory_offset_in_mb;
   79|  
   80|  	/*  Special cases for IP20,22,24,26 memory offset:  */
   81|  	if (machine->machine_subtype == 20 || machine->machine_subtype == 22 ||
   82|  	    machine->machine_subtype == 24 || machine->machine_subtype == 26) {
   83|  		dev_ram_init(machine, 0x00000000, 0x10000, DEV_RAM_MIRROR
   84|  		    | DEV_RAM_MIGHT_POINT_TO_DEVICES, sgi_ram_offset, NULL);
   85|  		dev_ram_init(machine, 0x00050000, sgi_ram_offset-0x50000,
   86|  		    DEV_RAM_MIRROR | DEV_RAM_MIGHT_POINT_TO_DEVICES,
   87|  		    sgi_ram_offset + 0x50000, NULL);
   88|  	}
   89|  
   90|  	/*  Special cases for IP28,30 memory offset:  */
   91|  	if (machine->machine_subtype == 28 || machine->machine_subtype == 30) {
   92|  		/*  TODO: length below should maybe not be 128MB?  */
   93|  		dev_ram_init(machine, 0x00000000, 128*1048576, DEV_RAM_MIRROR
   94|  		    | DEV_RAM_MIGHT_POINT_TO_DEVICES, sgi_ram_offset, NULL);
   95|  	}
   96|  
   97|  	net_generate_unique_mac(machine, macaddr);
   98|  
   99|  	char *eaddr_string;
  100|  	CHECK_ALLOCATION(eaddr_string = (char *) malloc(ETHERNET_STRING_MAXLEN));
  101|  
  102|  	/*
  103|  	 *  #446: FILL IT HERE, not only in the ip32 arm.
  104|  	 *
  105|  	 *  This buffer was malloc'ed and left UNINITIALISED, and only ONE subtype
  106|  	 *  arm (ip32, below) ever wrote to it -- yet the arcbios_init() call after
  107|  	 *  the switch is handed it unconditionally, and there set_env() ->
  108|  	 *  strdup() scans for a NUL that is not there.  MEASURED under ASan: a
  109|  	 *  41-byte READ past a 40-byte allocation, on ip12, ip28, ip30 and ip35;
  110|  	 *  reading the 40 in-bounds bytes at the point of use finds NO terminator
  111|  	 *  anywhere in the region.  ip32 is correct today only because its own arm
  112|  	 *  fills it.
  113|  	 *
  114|  	 *  *** THE OVERFLOW IS IN THE CALLEE'S strdup AND THE DEFECT IS HERE. ***
  115|  	 *  set_env() is correct code: it cannot detect a missing terminator
  116|  	 *  through the `const char *` it is given, so there is no callee-side
  117|  	 *  hardening to prefer at that signature.  (A review seat rightly noted
  118|  	 *  that this is not a categorical impossibility -- an interface taking a
  119|  	 *  LENGTH could check -- but changing set_env()'s signature to repair one
  120|  	 *  caller is not the minimal fix.)
  121|  	 *
  122|  	 *  A CALL-SITE AUDIT FOUND THIS THE ONLY DEFECTIVE CALLER, and the reason
  123|  	 *  is the two-caller grep, not the argument an earlier draft gave here.
  124|  	 *  arcbios_init() has exactly two callers: this one, and machine_arc.c,
  125|  	 *  which passes the string literal "10:20:30:40:50:60".  (That draft said
  126|  	 *  "machine.c forces machine->bootarg non-NULL"; machine.c:559 is a DEBUG
  127|  	 *  PRINT whose local `has_bootarg` only selects which message is emitted.
  128|  	 *  It forces nothing, and bootarg is not on this path at all.  The
  129|  	 *  conclusion survived; the argument for it did not.)
  130|  	 *
  131|  	 *  FIVE OTHER SUBTYPES WERE MASKING THIS -- ip19, ip20, ip22, ip24 and
  132|  	 *  ip27 -- and if their aborts are fixed first the overflow grows from
  133|  	 *  four subtypes to nine.  The coupling runs one way; recorded on
  134|  	 *  `ctorabortclass`.
  135|  	 *
  136|  	 *  *** THEY DO NOT ALL ABORT THE SAME WAY, AND AN EARLIER DRAFT OF THIS
  137|  	 *  COMMENT SAID THEY DID.  ***  A seat read the arms, found no abort() in
  138|  	 *  ip22's or ip27's, and challenged the claim.  MEASURED instead, over all
  139|  	 *  ten advertised subtypes: ip19/20/22/24/27 return 134 (SIGABRT) and
  140|  	 *  ip12/28/30/32/35 return 1.  The five are the five -- but ip22 has no
  141|  	 *  body of its own and FALLS THROUGH into case 24, and ip27 dies inside
  142|  	 *  its own device_add(), at interrupt_handler_lookup() <- devinit_z8530(),
  143|  	 *  on its `irq=0`.  A token search of a switch cannot see fall-through,
  144|  	 *  and reading for abort() misses an abort raised by a callee.
  145|  	 */
  146|  	snprintf(eaddr_string, ETHERNET_STRING_MAXLEN,
  147|  	    "%02x:%02x:%02x:%02x:%02x:%02x",
  148|  	    macaddr[0], macaddr[1], macaddr[2],
  149|  	    macaddr[3], macaddr[4], macaddr[5]);
  150|  
  151|  	switch (machine->machine_subtype) {
  152|  
  153|  	case 10:
  154|  		strlcat(machineName, " (4D/25)", MACHINE_NAME_MAXBUF);
  155|  		/*  TODO  */
  156|  		break;
  157|  
  158|  	case 12:
  159|  		strlcat(machineName, " (Iris Indigo IP12)", MACHINE_NAME_MAXBUF);
  160|  
  161|  		/*  TODO  */
  162|  		/*  33 MHz R3000, according to http://www.irisindigo.com/  */
  163|  		/*  "capable of addressing up to 96MB of memory."  */
  164|  
  165|  		break;
  166|  
  167|  	case 19:
  168|  		strlcat(machineName,
  169|  		    " (Everest IP19)", MACHINE_NAME_MAXBUF);
  170|  		machine->main_console_handle = (size_t)device_add(machine,
  171|+ 		    "z8530 addr=0x1fbd9830 addr_mult=4");
  172|  
  173|  		fatal("TODO ip19 interrupt rewrite\n");
  174|  		abort();
  175|  		//dev_scc_init(machine, mem, 0x10086000, 0,
  176|  		//    machine->x11_md.in_use, 0, 8);	/*  serial? irix?  */
  177|  
  178|  		device_add(machine, "sgi_ip19 addr=0x18000000");
  179|  
  180|  		/*  Irix' <everest_du_init+0x130> reads this device:  */
  181|  		device_add(machine, "random addr=0x10006000 len=16");
  182|  
  183|  		/*  Irix' get_mpconf() looks for this:  (TODO)  */
  184|  		store_32bit_word(cpu, 0xa0000000 + 0x3000,
  185|  		    0xbaddeed2);
  186|  
  187|  		/*  Memory size, not 4096 byte pages, but 256 bytes?
  188|  		    (16 is size of kernel... approx)  */
  189|  		store_32bit_word(cpu, 0xa0000000 + 0x26d0, 30000);
  190|  		  /* (machine->physical_ram_in_mb - 16) * (1048576 / 256));  */
  191|  
  192|  		break;
  193|  
  194|  	case 20:
  195|  		strlcat(machineName, " (Indigo)", MACHINE_NAME_MAXBUF);
  196|  
  197|  		/*
  198|  		 *  Guesses based on NetBSD 2.0 beta, 20040606.
  199|  		 *
  200|  		 *  int0 at mainbus0 addr 0x1fb801c0: bus 1MHz, CPU 2MHz
  201|  		 *  imc0 at mainbus0 addr 0x1fa00000: revision 0
  202|  		 *  gio0 at imc0
  203|  		 *  unknown GIO card (product 0x00 revision 0x00)
  204|  		 *	at gio0 slot 0 addr 0x1f400000 not configured
  205|  		 *  unknown GIO card (product 0x00 revision 0x00)
  206|  		 *	at gio0 slot 1 addr 0x1f600000 not configured
  207|  		 *  unknown GIO card (product 0x00 revision 0x00)
  208|  		 *	at gio0 slot 2 addr 0x1f000000 not configured
  209|  		 *  hpc0 at gio0 addr 0x1fb80000: SGI HPC1
  210|  		 *  zsc0 at hpc0 offset 0xd10   (channels 0 and 1,
  211|  		 *				 channel 1 for console)
  212|  		 *  zsc1 at hpc0 offset 0xd00   (2 channels)
  213|  		 *  sq0 at hpc0 offset 0x100: SGI Seeq 80c03
  214|  		 *  wdsc0 at hpc0 offset 0x11f
  215|  		 *  dpclock0 at hpc0 offset 0xe00
  216|  		 */
  217|  
  218|  		/*  int0 at mainbus0 addr 0x1fb801c0  */
  219|  fatal("TODO: SGI legacy interrupt system rewrite!\n");
  220|  abort();
  221|  //		machine->md_int.sgi_ip20_data = dev_sgi_ip20_init(cpu, mem,
  222|  //		    DEV_SGI_IP20_BASE);
  223|  
  224|  		/*  imc0 at mainbus0 addr 0x1fa00000: revision 0:
  225|  		    TODO (or in dev_sgi_ip20?)  */
  226|  
  227|  		machine->main_console_handle = (size_t)device_add(machine,
  228|+ 		    "z8530 addr=0x1fbd9830 addr_mult=4");
  229|  
  230|  		/*  This is the zsc0 reported by NetBSD:  TODO: irqs  */
  231|  		machine->main_console_handle = (size_t)device_add(machine,
  232|+ 		    "z8530 addr=0x1fb80d10 addr_mult=4");
  233|  		machine->main_console_handle = (size_t)device_add(machine,
  234|+ 		    "z8530 addr=0x1fb80d00 addr_mult=4");
  235|  
  236|  		/*  WDSC SCSI controller:  */
  237|  /*		dev_wdsc_init(machine, mem, 0x1fb8011f, 0, 0);  */
  238|  
  239|  		/*  Return memory read errors so that hpc1
  240|  		    and hpc2 are not detected:  */
  241|  		device_add(machine, "unreadable addr=0x1fb00000 len=0x10000");
  242|  		device_add(machine, "unreadable addr=0x1f980000 len=0x10000");
  243|  
  244|  		/*  Return nothing for gio slots 0, 1, and 2: */
  245|  		device_add(machine, "unreadable addr=0x1f400000 len=0x1000");
  246|  		device_add(machine, "unreadable addr=0x1f600000 len=0x1000");
  247|  		device_add(machine, "unreadable addr=0x1f000000 len=0x1000");
  248|  
  249|  		break;
  250|  
  251|  	case 21:
  252|  		strlcat(machineName,	/*  TODO  */
  253|  		    " (uknown SGI-IP21 ?)", MACHINE_NAME_MAXBUF);
  254|  		/*  NOTE:  Special case for arc_wordlen:  */
  255|  		arc_wordlen = sizeof(uint64_t);
  256|  
  257|  		device_add(machine, "random addr=0x418000200, len=0x20000");
  258|  
  259|  		break;
  260|  
  261|  	case 22:
  262|  	case 24:
  263|  		if (machine->machine_subtype == 22) {
  264|  			strlcat(machineName,
  265|  			    " (Indy, Indigo2, Challenge S; Full-house)",
  266|  			    MACHINE_NAME_MAXBUF);
  267|  fatal("TODO: SGI legacy interrupt system rewrite!\n");
  268|  abort();
  269|  //			machine->md_int.sgi_ip22_data =
  270|  //			    dev_sgi_ip22_init(machine, mem, 0x1fbd9000, 0);
  271|  		} else {
  272|  			strlcat(machineName,
  273|  			    " (Indy, Indigo2, Challenge S; Guiness)",
  274|  			    MACHINE_NAME_MAXBUF);
  275|  fatal("TODO: SGI legacy interrupt system rewrite!\n");
  276|  abort();
  277|  //			machine->md_int.sgi_ip22_data =
  278|  //			    dev_sgi_ip22_init(machine, mem, 0x1fbd9880, 1);
  279|  		}
  280|  
  281|  /*
  282|  Why is this here? TODO
  283|  		dev_ram_init(machine, 0x88000000ULL,
  284|  		    128 * 1048576, DEV_RAM_MIRROR, 0x08000000, NULL);
  285|  */
  286|  
  287|  fatal("TODO: Legacy rewrite\n");
  288|  abort();
  289|  //		machine->md_interrupt = sgi_ip22_interrupt;
  290|  
  291|  		/*
  292|  		 *  According to NetBSD 1.6.2:
  293|  		 *
  294|  		 *  imc0 at mainbus0 addr 0x1fa00000, Revision 0
     | [... lines 295-654 not shown ...]
  655|  
  656|  		// TODO: Correct Interrupt!
  657|  		snprintf(tmpstr, sizeof(tmpstr), "z8530 addr=0x1fbd9830 irq=%s.cpu[%i].2",
  658|  		    machine->path, machine->bootstrap_cpu);
  659|  		machine->main_console_handle = (size_t)device_add(machine, tmpstr);
  660|  
  661|  		break;
  662|  
  663|  	case 53:
  664|  		strlcat(machineName, " (Origin 350)",
  665|  		    MACHINE_NAME_MAXBUF);
  666|  
  667|  		/*
  668|  		 *  According to http://kumba.drachentekh.net/xml/myguide.html
  669|  		 *  Origin 350, Tezro IP53 R16000
  670|  		 */
  671|  		break;
  672|  
  673|  	default:
  674|  		fatal("unimplemented SGI machine type IP%i\n",
  675|  		    machine->machine_subtype);
  676|  		exit(1);
  677|  	}
  678|  
  679|  	if (!machine->prom_emulation)
  680|  		return;
  681|  
  682|  	arcbios_init(machine, arc_wordlen == sizeof(uint64_t), sgi_ram_offset,
  683|  	    eaddr_string, macaddr);
  684|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_CTORABORTCLASS: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_CTORABORTCLASS: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
