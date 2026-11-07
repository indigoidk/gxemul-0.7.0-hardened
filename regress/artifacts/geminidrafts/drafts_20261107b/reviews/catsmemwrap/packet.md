# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `catsmemwrap` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `catsmemwrap`, state `open`)

**title:** src/machines/machine_cats.c:59-61,110-111 -- physical_ram_in_mb * 1048576 is computed in 32 bits, so a -M of 4096 MB or more wraps the boot-info bt_memend; the > 256 test only warns -- WRAP (host -M option)

**state_note (head):** 

**The drafter's own reading:** STILL PRESENT: YES -- src/machines/machine_cats.c:59

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/machines/machine_cats.c b/src/machines/machine_cats.c
index 6fd5de57..ece5a5a9 100644
--- a/src/machines/machine_cats.c
+++ b/src/machines/machine_cats.c
@@ -56,9 +56,12 @@ MACHINE_SETUP(cats)
 	if (machine->emulated_hz == 0)
 		machine->emulated_hz = 50000000;
 
-	if (machine->physical_ram_in_mb > 256)
+	if (machine->physical_ram_in_mb > 256) {
 		fprintf(stderr, "WARNING! Real CATS machines cannot"
 		    " have more than 256 MB RAM. Continuing anyway.\n");
+		/* #001: clamp to avoid wrapping 32-bit boot info */
+		machine->physical_ram_in_mb = 256;
+	}
 
 	snprintf(tmpstr, sizeof(tmpstr), "footbridge irq=%s.cpu[%i].irq"
 	    " addr=0x42000000", machine->path, machine->bootstrap_cpu);
```

## Every edited function, after the fix

### `src/machines/machine_cats.c` -- post-edit lines 47-135 (`+` marks a line the diff added or the point of a deletion)

```c
   47|  MACHINE_SETUP(cats)
   48|  {
   49|  	struct ebsaboot ebsaboot;
   50|  	struct pci_data *pci_bus;
   51|  	char bs[300], tmpstr[400];
   52|  	int boot_id = machine->bootdev_id >= 0? machine->bootdev_id : 0;
   53|  
   54|  	machine->machine_name = strdup("CATS evaluation board");
   55|  
   56|  	if (machine->emulated_hz == 0)
   57|  		machine->emulated_hz = 50000000;
   58|  
   59|+ 	if (machine->physical_ram_in_mb > 256) {
   60|  		fprintf(stderr, "WARNING! Real CATS machines cannot"
   61|  		    " have more than 256 MB RAM. Continuing anyway.\n");
   62|+ 		/* #001: clamp to avoid wrapping 32-bit boot info */
   63|+ 		machine->physical_ram_in_mb = 256;
   64|+ 	}
   65|  
   66|  	snprintf(tmpstr, sizeof(tmpstr), "footbridge irq=%s.cpu[%i].irq"
   67|  	    " addr=0x42000000", machine->path, machine->bootstrap_cpu);
   68|  	pci_bus = (struct pci_data *) device_add(machine, tmpstr);
   69|  
   70|  	/*  DC21285_ROM_BASE (256 KB at 0x41000000)  */
   71|  	dev_ram_init(machine, 0x41000000, 256 * 1024, DEV_RAM_RAM, 0, NULL);
   72|  
   73|  	/*  NetBSD, OpenBSD, and Linux (?) clean their caches here:  */
   74|  	dev_ram_init(machine, 0x50000000, 0x10000, DEV_RAM_RAM, 0, NULL);
   75|  
   76|  	/*  Interrupt ack space?  */
   77|  	dev_ram_init(machine, 0x80000000, 0x1000, DEV_RAM_RAM, 0, NULL);
   78|  
   79|  	/*  Linux uses 0xc0000000 as phys.:  */
   80|  	dev_ram_init(machine, 0xc0000000, 0x20000000, DEV_RAM_MIRROR, 0x0, NULL);
   81|  
   82|  	/*  OpenBSD reboot needs 0xf??????? to be mapped to phys.:  */
   83|  	dev_ram_init(machine, 0xf0000000, 0x1000000, DEV_RAM_MIRROR, 0x0, NULL);
   84|  
   85|  	bus_pci_add(machine, pci_bus, machine->memory, 0xc0, 8, 0, "s3_virge");
   86|  
   87|  	if (!machine->prom_emulation)
   88|  		return;
   89|  
   90|  	/*  See cyclone_boot.h for details.  */
   91|  
   92|  	/*  DC21285_ROM_BASE "reboot" code:  (works with NetBSD)  */
   93|  	store_32bit_word(cpu, 0x41000008ULL, 0xef8c64ebUL);
   94|  
   95|  	cpu->cd.arm.r[0] = /* machine->physical_ram_in_mb */
   96|  	    7 * 1048576 - 0x1000;
   97|  
   98|  	memset(&ebsaboot, 0, sizeof(struct ebsaboot));
   99|  	store_32bit_word_in_host(cpu, (unsigned char *)
  100|  	    &(ebsaboot.bt_magic), BT_MAGIC_NUMBER_CATS);
  101|  	store_32bit_word_in_host(cpu, (unsigned char *)
  102|  	    &(ebsaboot.bt_vargp), 0);
  103|  	store_32bit_word_in_host(cpu, (unsigned char *)
  104|  	    &(ebsaboot.bt_pargp), 0);
  105|  	store_32bit_word_in_host(cpu, (unsigned char *)
  106|  	    &(ebsaboot.bt_args), cpu->cd.arm.r[0]
  107|  	    + sizeof(struct ebsaboot));
  108|  	store_32bit_word_in_host(cpu, (unsigned char *)
  109|  	    &(ebsaboot.bt_l1), 7 * 1048576 - 32768);
  110|  	store_32bit_word_in_host(cpu, (unsigned char *)
  111|  	    &(ebsaboot.bt_memstart), 0);
  112|  	store_32bit_word_in_host(cpu, (unsigned char *)
  113|  	    &(ebsaboot.bt_memend),
  114|  	    machine->physical_ram_in_mb * 1048576);
  115|  	store_32bit_word_in_host(cpu, (unsigned char *)
  116|  	    &(ebsaboot.bt_memavail), 7 * 1048576);
  117|  	store_32bit_word_in_host(cpu, (unsigned char *)
  118|  	    &(ebsaboot.bt_fclk), 50 * 1000000);
  119|  	store_32bit_word_in_host(cpu, (unsigned char *)
  120|  	    &(ebsaboot.bt_pciclk), 66 * 1000000);
  121|  	/*  TODO: bt_vers  */
  122|  	/*  TODO: bt_features  */
  123|  
  124|  	store_buf(cpu, cpu->cd.arm.r[0],
  125|  	    (char *)&ebsaboot, sizeof(struct ebsaboot));
  126|  
  127|  	snprintf(bs, sizeof(bs), "(hd%i)%s root=/dev/wd%i%s%s",
  128|  	    boot_id, machine->boot_kernel_filename, boot_id,
  129|  	    (machine->boot_string_argument[0])? " " : "",
  130|  	    machine->boot_string_argument);
  131|  
  132|  	store_string(cpu, cpu->cd.arm.r[0]+sizeof(struct ebsaboot), bs);
  133|  
  134|  	arm_setup_initial_translation_table(cpu, 7 * 1048576 - 32768);
  135|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_CATSMEMWRAP: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_CATSMEMWRAP: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
