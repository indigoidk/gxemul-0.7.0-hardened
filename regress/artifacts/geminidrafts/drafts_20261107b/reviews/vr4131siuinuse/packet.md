# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `vr4131siuinuse` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `vr4131siuinuse`, state `open`)

**title:** devices/dev_vr41xx.c:dev_vr41xx_init -- the VR4131 on-chip SIU is registered with the default in_use=1, so two ns16550 handles race for host stdin on the BE-300 -- WRONG-RESULT (lost console input)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T114 (class WRONG-RESULT; reach C, configuration, debugger, host environment or a non-default build; effort: one-line; report rows: A3-11).  Source URLs: https://github.com/jroark/GXemul/commit/3c3d5cbfa23ce58718d6c1c348f44587b35c0911.  Our site at de8c7547: src/devices/dev_vr41xx.c:777-781; src/devices/device.c:266.  Portable fix: yes -- port jroark 3c3d5cb (embedded: the extra on-chip SIU registered as not in use).  Filing check (TRIAGE.md): 0 hits.  The extra SIU registered as not in use is a portable one-line fact (regress/artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md F).  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- `if (cpumodel == 4131) { snprintf(tmps, sizeof(tmps), "ns16550 irq=%s.cpu[%i].vrip.%i " "addr=0x%" PRIx64" name2=siu", machine->path,` at `src/devices/dev_vr41xx.c:776`

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_vr41xx.c b/src/devices/dev_vr41xx.c
index e0108e3d..4c26bf33 100644
--- a/src/devices/dev_vr41xx.c
+++ b/src/devices/dev_vr41xx.c
@@ -775,7 +775,7 @@ struct vr41xx_data *dev_vr41xx_init(struct machine *machine,
 	 */
 	if (cpumodel == 4131) {
 		snprintf(tmps, sizeof(tmps), "ns16550 irq=%s.cpu[%i].vrip.%i "
-		    "addr=0x%" PRIx64" name2=siu", machine->path,
+		    "addr=0x%" PRIx64" name2=siu in_use=0", machine->path,
 		    machine->bootstrap_cpu, VRIP_INTR_SIU,
 		    (uint64_t) (baseaddr+0x800));
 		device_add(machine, tmps);
```

## Every edited function, after the fix

### `src/devices/dev_vr41xx.c` -- post-edit lines 674-805 (`+` marks a line the diff added or the point of a deletion)

```c
  674|  {
  675|  	struct vr41xx_data *d;
  676|  	uint64_t baseaddr = 0;
  677|  	char tmps[300];
  678|  	int i;
  679|  
  680|  	CHECK_ALLOCATION(d = (struct vr41xx_data *) malloc(sizeof(struct vr41xx_data)));
  681|  	memset(d, 0, sizeof(struct vr41xx_data));
  682|  
  683|  	/*  Connect to MIPS irq 2:  */
  684|  	snprintf(tmps, sizeof(tmps), "%s.cpu[%i].2",
  685|  	    machine->path, machine->bootstrap_cpu);
  686|  	INTERRUPT_CONNECT(tmps, d->cpu_irq);
  687|  
  688|  	/*
  689|  	 *  Register VRIP interrupt lines 0..25:
  690|  	 */
  691|  	for (i=0; i<=25; i++) {
  692|  		struct interrupt templ;
  693|  		snprintf(tmps, sizeof(tmps), "%s.cpu[%i].vrip.%i",
  694|  		    machine->path, machine->bootstrap_cpu, i);
  695|  		memset(&templ, 0, sizeof(templ));
  696|  		templ.line = i;
  697|  		templ.name = tmps;
  698|  		templ.extra = d;
  699|  		templ.interrupt_assert = vr41xx_vrip_interrupt_assert;
  700|  		templ.interrupt_deassert = vr41xx_vrip_interrupt_deassert;
  701|  		interrupt_handler_register(&templ);
  702|  	}
  703|  
  704|  	/*
  705|  	 *  Register GIU interrupt lines 0..31:
  706|  	 */
  707|  	for (i=0; i<32; i++) {
  708|  		struct interrupt templ;
  709|  		snprintf(tmps, sizeof(tmps), "%s.cpu[%i].vrip.%i.giu.%i",
  710|  		    machine->path, machine->bootstrap_cpu, VRIP_INTR_GIU, i);
  711|  		memset(&templ, 0, sizeof(templ));
  712|  		templ.line = i;
  713|  		templ.name = tmps;
  714|  		templ.extra = d;
  715|  		templ.interrupt_assert = vr41xx_giu_interrupt_assert;
  716|  		templ.interrupt_deassert = vr41xx_giu_interrupt_deassert;
  717|  		interrupt_handler_register(&templ);
  718|  	}
  719|  
  720|  	d->cpumodel = cpumodel;
  721|  
  722|  	/*  TODO: VRC4173 has the KIU at offset 0x100?  */
  723|  	d->kiu_offset = 0x180;
  724|  	d->kiu_console_handle = -1;
  725|  	if (machine->x11_md.in_use)
  726|  		d->kiu_console_handle = console_start_slave_inputonly(
  727|  		    machine, "kiu", 1);
  728|  
  729|  	/*  Connect to the KIU and GIU interrupts:  */
  730|  	snprintf(tmps, sizeof(tmps), "%s.cpu[%i].vrip.%i",
  731|  	    machine->path, machine->bootstrap_cpu, VRIP_INTR_GIU);
  732|  	INTERRUPT_CONNECT(tmps, d->giu_irq);
  733|  	snprintf(tmps, sizeof(tmps), "%s.cpu[%i].vrip.%i",
  734|  	    machine->path, machine->bootstrap_cpu, VRIP_INTR_KIU);
  735|  	INTERRUPT_CONNECT(tmps, d->kiu_irq);
  736|  
  737|  	if (machine->x11_md.in_use)
  738|  		machine->main_console_handle = d->kiu_console_handle;  
  739|  
  740|  	switch (cpumodel) {
  741|  	case 4101:
  742|  	case 4102:
  743|  	case 4111:
  744|  	case 4121:
  745|  		baseaddr = 0xb000000;
  746|  		break;
  747|  	case 4181:
  748|  		baseaddr = 0xa000000;
  749|  		dev_ram_init(machine, 0xb000000, 0x1000000, DEV_RAM_MIRROR,
  750|  		    0xa000000, NULL);
  751|  		break;
  752|  	case 4122:
  753|  	case 4131:
  754|  		baseaddr = 0xf000000;
  755|  		break;
  756|  	default:
  757|  		printf("Unimplemented VR cpu model\n");
  758|  		exit(1);
  759|  	}
  760|  
  761|  	if (d->cpumodel == 4121 || d->cpumodel == 4181)
  762|  		snprintf(tmps, sizeof(tmps), "%s.cpu[%i].3",
  763|  		    machine->path, machine->bootstrap_cpu);
  764|  	else
  765|  		snprintf(tmps, sizeof(tmps), "%s.cpu[%i].vrip.%i",
  766|  		    machine->path, machine->bootstrap_cpu, VRIP_INTR_ETIMER);
  767|  	INTERRUPT_CONNECT(tmps, d->timer_irq);
  768|  
  769|  	memory_device_register(mem, "vr41xx", baseaddr, DEV_VR41XX_LENGTH,
  770|  	    dev_vr41xx_access, (void *)d, DM_DEFAULT, NULL);
  771|  
  772|  	/*
  773|  	 *  TODO: Find out which controllers are at which addresses on
  774|  	 *  which chips.
  775|  	 */
  776|  	if (cpumodel == 4131) {
  777|  		snprintf(tmps, sizeof(tmps), "ns16550 irq=%s.cpu[%i].vrip.%i "
  778|+ 		    "addr=0x%" PRIx64" name2=siu in_use=0", machine->path,
  779|  		    machine->bootstrap_cpu, VRIP_INTR_SIU,
  780|  		    (uint64_t) (baseaddr+0x800));
  781|  		device_add(machine, tmps);
  782|  	} else {
  783|  		/*  This is used by Linux and NetBSD:  */
  784|  		snprintf(tmps, sizeof(tmps), "ns16550 irq=%s.cpu[%i]."
  785|  		    "vrip.%i addr=0x%x name2=serial", machine->path,
  786|  		    machine->bootstrap_cpu, VRIP_INTR_SIU, 0xc000000);
  787|  		device_add(machine, tmps);
  788|  	}
  789|  
  790|  	/*  Hm... maybe this should not be here.  TODO  */
  791|  	snprintf(tmps, sizeof(tmps), "pcic irq=%s.cpu[%i].vrip.%i addr="
  792|  	    "0x140003e0", machine->path, machine->bootstrap_cpu,
  793|  	    VRIP_INTR_GIU);
  794|  	device_add(machine, tmps);
  795|  
  796|  	machine_add_tickfunction(machine, dev_vr41xx_tick, d,
  797|  	    DEV_VR41XX_TICKSHIFT);
  798|  
  799|  	/*  Some machines (?) use ISA space at 0x15000000 instead of
  800|  	    0x14000000, eg IBM WorkPad Z50.  */
  801|  	dev_ram_init(machine, 0x15000000, 0x1000000, DEV_RAM_MIRROR,
  802|  	    0x14000000, NULL);
  803|  
  804|  	return d;
  805|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_VR4131SIUINUSE: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_VR4131SIUINUSE: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

## YOUR PREVIOUS REVIEW OF THIS DRAFT SAID UNSETTLED -- here is what it said, and the definitions it named

```text
FIXREVIEW_VR4131SIUINUSE: UNSETTLED, 1 FINDINGS
1. The diff removes the defect at `src/devices/dev_vr41xx.c:777-781` by explicitly setting `in_use=0` in the device argument string. However, the issue also names `src/devices/device.c:266` which is not edited by this diff. It is UNSETTLED whether a change is also required there without reading `src/devices/device.c`.
2. No. The diff adds no control flow statements.
3. No. The function continues to return `d`, representing the allocated and initialized `vr41xx_data` structure. 
4. Nothing else. The diff only alters the device creation string passed to `device_add` for the SIU.
5. The edited line stays within 79 columns. No new diagnostics or comments were added.
src/devices/device.c:266: QUESTION: File not included in diff; UNSETTLED if changes are needed here to fully clear the issue.
```

### `src/devices/dev_vr41xx.c` lines 52-68 (where HEAD defines `vr41xx_data`)

```c
   52| #include "thirdparty/vr_rtcreg.h"
   53| 
   54| 
   55| /*  #define debug fatal  */
   56| 
   57| #define	DEV_VR41XX_TICKSHIFT		14
   58| 
   59| #define	DEV_VR41XX_LENGTH		0x800	/*  TODO?  */
   60| struct vr41xx_data {
   61| 	struct interrupt cpu_irq;		/*  Connected to MIPS irq 2  */
   62| 	int		cpumodel;		/*  Model nr, e.g. 4121  */
   63| 
   64| 	/*  KIU:  */
   65| 	int		kiu_console_handle;
   66| 	uint32_t	kiu_offset;
   67| 	struct interrupt kiu_irq;
   68| 	int		kiu_int_assert;
```

### `src/devices/dev_vr41xx.c` lines 664-680 (where HEAD defines `vr41xx_data`)

```c
  664| }
  665| 
  666| 
  667| /*
  668|  *  dev_vr41xx_init():
  669|  *
  670|  *  machine->path is something like "machine[0]".
  671|  */
  672| struct vr41xx_data *dev_vr41xx_init(struct machine *machine,
  673| 	struct memory *mem, int cpumodel)
  674| {
  675| 	struct vr41xx_data *d;
  676| 	uint64_t baseaddr = 0;
  677| 	char tmps[300];
  678| 	int i;
  679| 
  680| 	CHECK_ALLOCATION(d = (struct vr41xx_data *) malloc(sizeof(struct vr41xx_data)));
```

### `src/devices/device.c` lines 244-260 (where HEAD defines `device_add`)

```c
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
```

### `src/include/device.h` lines 71-87 (where HEAD defines `device_add`)

```c
   71| 
   72| /*  autodev.c: (built automatically in the devices/ directory):  */
   73| void autodev_init(void);
   74| 
   75| /*  device.c:  */
   76| int device_register(const char *name, int (*initf)(struct devinit *));
   77| struct device_entry *device_lookup(char *name);
   78| int device_unregister(char *name);
   79| void *device_add(struct machine *machine, const char *name_and_params);
   80| void device_dumplist(void);
   81| void device_set_exit_on_error(int exit_on_error);
   82| void device_init(void);
   83| 
   84| /*  PCI stuff:  (TODO: move somewhere else?)  */
   85| int pci_register(const char *name, void (*initf)(struct machine *, struct memory *,
   86| 	struct pci_device *));
   87| void (*pci_lookup_initf(const char *name))(struct machine *machine,
```

Review the draft again with these in view.  If it still cannot be settled, say UNSETTLED and name the exact function or
definition still missing.
