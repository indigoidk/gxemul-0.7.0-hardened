# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `ps2gmtime` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `ps2gmtime`, state `open`)

**title:** src/machines/machine_playstation2.c:141-145 -- the gmtime() result is used without a NULL test (the argument is time(NULL) + 9*3600) -- NULL (host only)

**state_note (head):** 

**The drafter's own reading:** STILL PRESENT: YES -- tm_ptr = gmtime(&timet);

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/machines/machine_playstation2.c b/src/machines/machine_playstation2.c
index cbe62d3b..24c71837 100644
--- a/src/machines/machine_playstation2.c
+++ b/src/machines/machine_playstation2.c
@@ -140,19 +140,21 @@ MACHINE_SETUP(playstation2)
 	/*  RTC data given by the BIOS:  */
 	timet = time(NULL) + 9*3600;	/*  PS2 uses Japanese time  */
 	tm_ptr = gmtime(&timet);
-	/*  TODO:  are these 0- or 1-based?  */
-	store_byte(cpu, 0xa0000000 + machine->physical_ram_in_mb
-	    * 1048576 - 0x1000 + 0x10 + 1, int_to_bcd(tm_ptr->tm_sec));
-	store_byte(cpu, 0xa0000000 + machine->physical_ram_in_mb
-	    * 1048576 - 0x1000 + 0x10 + 2, int_to_bcd(tm_ptr->tm_min));
-	store_byte(cpu, 0xa0000000 + machine->physical_ram_in_mb
-	    * 1048576 - 0x1000 + 0x10 + 3, int_to_bcd(tm_ptr->tm_hour));
-	store_byte(cpu, 0xa0000000 + machine->physical_ram_in_mb
-	    * 1048576 - 0x1000 + 0x10 + 5, int_to_bcd(tm_ptr->tm_mday));
-	store_byte(cpu, 0xa0000000 + machine->physical_ram_in_mb
-	    * 1048576 - 0x1000 + 0x10 + 6, int_to_bcd(tm_ptr->tm_mon+1));
-	store_byte(cpu, 0xa0000000 + machine->physical_ram_in_mb
-	    * 1048576 - 0x1000 + 0x10 + 7, int_to_bcd(tm_ptr->tm_year-100));
+	if (tm_ptr != NULL) {
+		/*  TODO:  are these 0- or 1-based?  */
+		store_byte(cpu, 0xa0000000 + machine->physical_ram_in_mb
+		    * 1048576 - 0x1000 + 0x10 + 1, int_to_bcd(tm_ptr->tm_sec));
+		store_byte(cpu, 0xa0000000 + machine->physical_ram_in_mb
+		    * 1048576 - 0x1000 + 0x10 + 2, int_to_bcd(tm_ptr->tm_min));
+		store_byte(cpu, 0xa0000000 + machine->physical_ram_in_mb
+		    * 1048576 - 0x1000 + 0x10 + 3, int_to_bcd(tm_ptr->tm_hour));
+		store_byte(cpu, 0xa0000000 + machine->physical_ram_in_mb
+		    * 1048576 - 0x1000 + 0x10 + 5, int_to_bcd(tm_ptr->tm_mday));
+		store_byte(cpu, 0xa0000000 + machine->physical_ram_in_mb
+		    * 1048576 - 0x1000 + 0x10 + 6, int_to_bcd(tm_ptr->tm_mon+1));
+		store_byte(cpu, 0xa0000000 + machine->physical_ram_in_mb
+		    * 1048576 - 0x1000 + 0x10 + 7, int_to_bcd(tm_ptr->tm_year-100));
+	}
 
 	/*  "BOOTINFO_PCMCIA_TYPE" in NetBSD's bootinfo.h. This
 	    contains the sbus controller type.  */
```

## Every edited function, after the fix

### `src/machines/machine_playstation2.c` -- post-edit lines 55-163 (`+` marks a line the diff added or the point of a deletion)

```c
   55|  MACHINE_SETUP(playstation2)
   56|  {
   57|  	char tmpstr[200];
   58|  	int tmplen;
   59|  	char *tmp;
   60|  	time_t timet;
   61|  	struct tm *tm_ptr;
   62|  
   63|  	machine->machine_name = strdup("Playstation 2");
   64|  	cpu->byte_order = EMUL_LITTLE_ENDIAN;
   65|  
   66|  	if (machine->physical_ram_in_mb != 32)
   67|  		fprintf(stderr, "WARNING! Playstation 2 machines are supposed "
   68|  		    "to have exactly 32 MB RAM. Continuing anyway.\n");
   69|  	if (!machine->x11_md.in_use)
   70|  		fprintf(stderr, "WARNING! Playstation 2 without -X is pretty "
   71|  		    "meaningless. Continuing anyway.\n");
   72|  
   73|  	/*
   74|  	 *  According to NetBSD:
   75|  	 *
   76|  	 *	Hardware irq 0 is timer/interrupt controller
   77|  	 *	Hardware irq 1 is dma controller
   78|  	 *
   79|  	 *  Some things are not yet emulated (at all), and hence are detected
   80|  	 *  incorrectly:
   81|  	 *
   82|  	 *	sbus0 at mainbus0: controller type 2
   83|  	 *	ohci0 at sbus0		(at 0x1f801600, according to linux)
   84|  	 *	ohci0: OHCI version 1.0
   85|  	 */
   86|  
   87|  	device_add(machine, "ps2 addr=0x10000000");
   88|  	device_add(machine, "ps2_gs addr=0x12000000");
   89|  	device_add(machine, "ps2_ether addr=0x14001000");
   90|  
   91|  	/*  TODO: how much?  */
   92|  	dev_ram_init(machine, 0x1c000000, 4 * 1048576, DEV_RAM_RAM, 0, NULL);
   93|  
   94|  	/*  OHCI at SBUS irq 1:  */
   95|  	snprintf(tmpstr, sizeof(tmpstr), "ohci addr=0x1f801600 irq="
   96|  	    "%s.cpu[%i].ps2_sbus.1", machine->path, machine->bootstrap_cpu);
   97|  	device_add(machine, tmpstr);
   98|  
   99|  	/*  Set the Harddisk controller present flag, if either
  100|  	    disk 0 or 1 is present:  */
  101|  	if (diskimage_exist(machine, 0, DISKIMAGE_IDE) ||
  102|  	    diskimage_exist(machine, 1, DISKIMAGE_IDE)) {
  103|  		if (machine->prom_emulation)
  104|  			store_32bit_word(cpu, 0xa0000000 + machine->
  105|  			    physical_ram_in_mb*1048576 - 0x1000 + 0x0, 0x100);
  106|  		device_add(machine, "ps2_spd addr=0x14000000");
  107|  	}
  108|  
  109|  	if (!machine->prom_emulation)
  110|  		return;
  111|  
  112|  
  113|  	tmplen = 1000;
  114|  	CHECK_ALLOCATION(tmp = (char *) malloc(tmplen));
  115|  
  116|  	add_symbol_name(&machine->symbol_context,
  117|  	    PLAYSTATION2_SIFBIOS, 0x10000, "[SIFBIOS entry]", 0, 0);
  118|  	store_32bit_word(cpu, PLAYSTATION2_BDA + 0,
  119|  	    PLAYSTATION2_SIFBIOS);
  120|  	store_buf(cpu, PLAYSTATION2_BDA + 4, "PS2b", 4);
  121|  
  122|  	/*  "Magic trap" instruction for software PROM emulation:  */
  123|  	store_32bit_word(cpu, PLAYSTATION2_SIFBIOS, 0x00c0de0c);
  124|  
  125|  	store_32bit_word(cpu, 0xa0000000 + machine->physical_ram_in_mb
  126|  	    * 1048576 - 0x1000 + 0x4, PLAYSTATION2_OPTARGS);
  127|  
  128|  	strlcpy(tmp, "root=/dev/hda1 crtmode=vesa0,60", tmplen);
  129|  
  130|  	if (machine->boot_string_argument[0])
  131|  		snprintf(tmp+strlen(tmp), tmplen-strlen(tmp),
  132|  		    " %s", machine->boot_string_argument);
  133|  	tmp[tmplen-1] = '\0';
  134|  
  135|  	machine->bootstr = tmp;
  136|  	store_string(cpu, PLAYSTATION2_OPTARGS, machine->bootstr);
  137|  
  138|  	/*  TODO:  netbsd's bootinfo.h, for symbolic names  */
  139|  
  140|  	/*  RTC data given by the BIOS:  */
  141|  	timet = time(NULL) + 9*3600;	/*  PS2 uses Japanese time  */
  142|  	tm_ptr = gmtime(&timet);
  143|+ 	if (tm_ptr != NULL) {
  144|+ 		/*  TODO:  are these 0- or 1-based?  */
  145|+ 		store_byte(cpu, 0xa0000000 + machine->physical_ram_in_mb
  146|+ 		    * 1048576 - 0x1000 + 0x10 + 1, int_to_bcd(tm_ptr->tm_sec));
  147|+ 		store_byte(cpu, 0xa0000000 + machine->physical_ram_in_mb
  148|+ 		    * 1048576 - 0x1000 + 0x10 + 2, int_to_bcd(tm_ptr->tm_min));
  149|+ 		store_byte(cpu, 0xa0000000 + machine->physical_ram_in_mb
  150|+ 		    * 1048576 - 0x1000 + 0x10 + 3, int_to_bcd(tm_ptr->tm_hour));
  151|+ 		store_byte(cpu, 0xa0000000 + machine->physical_ram_in_mb
  152|+ 		    * 1048576 - 0x1000 + 0x10 + 5, int_to_bcd(tm_ptr->tm_mday));
  153|+ 		store_byte(cpu, 0xa0000000 + machine->physical_ram_in_mb
  154|+ 		    * 1048576 - 0x1000 + 0x10 + 6, int_to_bcd(tm_ptr->tm_mon+1));
  155|+ 		store_byte(cpu, 0xa0000000 + machine->physical_ram_in_mb
  156|+ 		    * 1048576 - 0x1000 + 0x10 + 7, int_to_bcd(tm_ptr->tm_year-100));
  157|+ 	}
  158|  
  159|  	/*  "BOOTINFO_PCMCIA_TYPE" in NetBSD's bootinfo.h. This
  160|  	    contains the sbus controller type.  */
  161|  	store_32bit_word(cpu, 0xa0000000 + machine->physical_ram_in_mb
  162|  	    * 1048576 - 0x1000 + 0x1c, 2);
  163|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_PS2GMTIME: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_PS2GMTIME: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
