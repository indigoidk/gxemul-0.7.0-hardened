# GXemul hardened fork -- DRAFT A FIX for one filed issue, `pcicfgaddrlow` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD d2a6f233).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `pcicfgaddrlow`, state `open`, severity `MED`)

**title:** devices/bus_pci.c:bus_pci_decompose_1 -- CONFIG_ADDRESS keeps bits 1:0 in the register number and every unaligned select prints an unlatched `fatal()` -- WRONG-RESULT

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T100 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: one-line; report rows: A5-30).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/eb4c571747357b394ec15fc2b9f9a31efb999ef5.  Our site at de8c7547: src/devices/bus_pci.c:77-82.  Portable fix: yes -- port rs6000 eb4c571.  Filing check (TRIAGE.md): `pciaddrreadclobber` is a different 0xcf8 defect.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port rs6000 eb4c571

## The code at the cited lines

### `src/devices/bus_pci.c` around the row's cited line 77 (HEAD d2a6f233, lines 32-122)

```c
   32|  *
   33|  *  See NetBSD's pcidevs.h for more PCI vendor and device identifiers.
   34|  *
   35|  *  TODO:
   36|  *
   37|  *	x) Allow guest OSes to do runtime address fixups (i.e. actually
   38|  *	   move a device from one address to another).
   39|  *
   40|  *	x) Generalize the PCI and legacy ISA interrupt routing stuff.
   41|  *
   42|  *	x) Make sure that pci_little_endian is used correctly everywhere.
   43|  */
   44| 
   45| #include <stdio.h>
   46| #include <stdlib.h>
   47| #include <string.h>
   48| 
   49| #define BUS_PCI_C
   50| 
   51| #include "bus_isa.h"
   52| #include "bus_pci.h"
   53| #include "cpu.h"
   54| #include "device.h"
   55| #include "devices.h"
   56| #include "diskimage.h"
   57| #include "machine.h"
   58| #include "memory.h"
   59| #include "misc.h"
   60| #include "wdc.h"
   61| 
   62| #include "thirdparty/cpc700reg.h"
   63| 
   64| extern int verbose;
   65| 
   66| 
   67| /*
   68|  *  bus_pci_decompose_1():
   69|  *
   70|  *  Helper function for decomposing Mechanism 1 tags.
   71|  */
   72| void bus_pci_decompose_1(uint32_t t, int *bus, int *dev, int *func, int *reg)
   73| {
   74| 	*bus  = (t >> 16) & 0xff;
   75| 	*dev  = (t >> 11) & 0x1f;
   76| 	*func = (t >>  8) &  0x7;
   77| 	*reg  =  t        & 0xff;
   78| 
   79| 	/*  Warn about unaligned register access:  */
   80| 	if (t & 3)
   81| 		fatal("[ bus_pci_decompose_1: WARNING: reg = 0x%02x ]\n",
   82| 		    t & 0xff);
   83| }
   84| 
   85| 
   86| /*
   87|  *  bus_pci_data_access():
   88|  *
   89|  *  Reads from or writes to the PCI configuration registers of a device.
   90|  */
   91| void bus_pci_data_access(struct cpu *cpu, struct pci_data *pci_data,
   92| 	uint64_t *data, int len, int writeflag)
   93| {
   94| 	struct pci_device *dev;
   95| 	unsigned char *cfg_base;
   96| 	uint64_t x, idata = *data;
   97| 	int i;
   98| 
   99| 	/*  Scan through the list of pci_device entries.  */
  100| 	dev = pci_data->first_device;
  101| 	while (dev != NULL) {
  102| 		if (dev->bus      == pci_data->cur_bus &&
  103| 		    dev->function == pci_data->cur_func &&
  104| 		    dev->device   == pci_data->cur_device)
  105| 			break;
  106| 		dev = dev->next;
  107| 	}
  108| 
  109| 	/*  No device? Then return emptiness.  */
  110| 	if (dev == NULL) {
  111| 		if (writeflag == MEM_READ) {
  112| 			if (pci_data->cur_reg == 0)
  113| 				*data = (uint64_t) -1;
  114| 			else
  115| 				*data = 0;
  116| 		} else {
  117| 			fatal("[ bus_pci_data_access(): write to non-existant"
  118| 			    " device, bus %i func %i device %i ]\n",
  119| 			    pci_data->cur_bus, pci_data->cur_func,
  120| 			    pci_data->cur_device);
  121| 		}
  122| 		return;
```

## The data structures those files define (every field that exists)

### `src/include/bus_pci.h` -- `struct pci_data` (HEAD lines 50-88)

```c
   50| struct pci_data {
   51| 	/*
   52| 	 *  IRQ paths:
   53| 	 *
   54| 	 *  irq_path		Path of the controller itself.
   55| 	 *  irq_path_isa	Path base of ISA interrupts.
   56| 	 *  irq_path_pci	Path base of PCI interrupts.
   57| 	 */
   58| 	char		*irq_path;
   59| 	char		*irq_path_isa;
   60| 	char		*irq_path_pci;
   61| 
   62| 	/*
   63| 	 *  Default I/O port, memory, and irq bases for PCI and legacy ISA
   64| 	 *  devices, and the base address for actual (emulated) devices:
   65| 	 *
   66| 	 *  pci_portbase etc are what is stored in the device configuration
   67| 	 *  registers. This address + pci_actual_{io,mem}_offset is where the
   68| 	 *  emulated device should be registered.
   69| 	 */
   70| 	uint64_t	pci_actual_io_offset;
   71| 	uint64_t	pci_actual_mem_offset;
   72| 
   73| 	uint64_t	pci_portbase;
   74| 	uint64_t	pci_membase;
   75| 
   76| 	uint64_t	isa_portbase;
   77| 	uint64_t	isa_membase;
   78| 
   79| 	/*  Current base when allocating space for PCI devices:  */
   80| 	uint64_t	cur_pci_portbase;
   81| 	uint64_t	cur_pci_membase;
   82| 
   83| 	/*  Current register access:  */
   84| 	int		cur_bus, cur_device, cur_func, cur_reg;
   85| 	int		last_was_write_ffffffff;
   86| 
   87| 	struct pci_device *first_device;
   88| };
```

RULES FOR THE EDITS: change ONLY text that appears in this packet; use ONLY fields, functions and macros that appear in it
(a draft that calls an undeclared function or a field that does not exist does not compile); make each `old` long enough to
occur exactly once in its file -- include a distinctive neighbouring line when a statement repeats.

## WHAT TO RETURN

1. One line: `STILL PRESENT: YES|NO|UNSETTLED -- <the line of code shown that shows it>`.  The cited line numbers may have
   moved since the row was written; judge from the code shown.  If NO, say what already fixed it and STOP (no edits).
2. If YES: EXACTLY ONE fenced ```json block -- a list of edits, the smallest fix that removes the defect without changing any
   other behaviour: [{"file": "src/...", "old": "<exact text from the code above, without the line-number prefix; it must occur
   EXACTLY ONCE in that file>", "new": "<replacement>", "why": "<one line>"}].  Use JSON escapes (\t, \n).  Tabs stay tabs;
   lines within 79 columns; tag a new comment `/* #NNN: ... */`.  Prefer the file's existing idioms (a decline, a once-per-
   device announce, a clamp) over new machinery.
3. After the block: what the fix deliberately does NOT change, and anything you could not settle from the code shown.

End with one line: `FIXDRAFT_PCICFGADDRLOW: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
