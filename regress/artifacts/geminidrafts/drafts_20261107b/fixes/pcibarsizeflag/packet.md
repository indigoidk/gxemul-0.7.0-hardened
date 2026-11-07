# GXemul hardened fork -- DRAFT A FIX for one filed issue, `pcibarsizeflag` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `pcibarsizeflag`, state `open`, severity `LOW`)

**title:** src/devices/bus_pci.c:126-131,145-150,178,192-203 -- the BAR-sizing flag (set when the guest writes 0xffffffff to a base address register) is one per bus and is cleared only by a config read, so when the guest selects a different device or BAR before reading, that target's next BAR read returns its size mask instead of its value -- WRONG-RESULT

**state_note (head):**



**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- clear flag on target change

## The code at the cited lines

### `src/devices/bus_pci.c` around the row's cited line 126 (HEAD 8d9df658, lines 6-246)

```c
    6|  *
    7|  *  1. Redistributions of source code must retain the above copyright
    8|  *     notice, this list of conditions and the following disclaimer.
    9|  *  2. Redistributions in binary form must reproduce the above copyright  
   10|  *     notice, this list of conditions and the following disclaimer in the 
   11|  *     documentation and/or other materials provided with the distribution.
   12|  *  3. The name of the author may not be used to endorse or promote products
   13|  *     derived from this software without specific prior written permission.
   14|  *
   15|  *  THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
   16|  *  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
   17|  *  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
   18|  *  ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE   
   19|  *  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
   20|  *  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
   21|  *  OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
   22|  *  HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
   23|  *  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
   24|  *  OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
   25|  *  SUCH DAMAGE.
   26|  *   
   27|  *
   28|  *  COMMENT: Generic PCI bus framework
   29|  *
   30|  *  This is not a normal "device", but is used by individual PCI controllers
   31|  *  and devices.
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
  123| 	}
  124| 
  125| 	/*  Return normal config data, or length data?  */
  126| 	if (pci_data->last_was_write_ffffffff &&
  127| 	    pci_data->cur_reg >= PCI_MAPREG_START &&
  128| 	    pci_data->cur_reg <= PCI_MAPREG_END - 4)
  129| 		cfg_base = dev->cfg_mem_size;
  130| 	else
  131| 		cfg_base = dev->cfg_mem;
  132| 
  133| 	/*  Read data as little-endian:  */
  134| 	x = 0;
  135| 	for (i=len-1; i>=0; i--) {
  136| 		int ofs = pci_data->cur_reg + i;
  137| 		x <<= 8;
  138| 		x |= cfg_base[ofs & (PCI_CFG_MEM_SIZE - 1)];
  139| 	}
  140| 
  141| 	/*  Register write:  */
  142| 	if (writeflag == MEM_WRITE) {
  143| 		debug("[ bus_pci: write to PCI DATA: data = 0x%08llx ]\n",
  144| 		    (long long)idata);
  145| 		if (idata == 0xffffffffULL &&
  146| 		    pci_data->cur_reg >= PCI_MAPREG_START &&
  147| 		    pci_data->cur_reg <= PCI_MAPREG_END - 4) {
  148| 			pci_data->last_was_write_ffffffff = 1;
  149| 			return;
  150| 		}
  151| 
  152| 		if (dev->cfg_reg_write == NULL ||
  153| 		    dev->cfg_reg_write(dev, pci_data->cur_reg, *data) == 0) {
  154| 			/*  Print a warning for unhandled writes:  */
  155| 			debug("[ bus_pci: write to PCI DATA: data = 0x%08llx"
  156| 			    " (current value = 0x%08llx); NOT YET"
  157| 			    " SUPPORTED. bus %i, device %i, function %i (%s)"
  158| 			    " register 0x%02x ]\n", (long long)idata,
  159| 			    (long long)x, pci_data->cur_bus,
  160| 			    pci_data->cur_device, pci_data->cur_func,
  161| 			    dev->name, pci_data->cur_reg);
  162| 
  163| 			/*  Special warning, to detect if NetBSD's special
  164| 			    detection of PCI devices fails:  */
  165| 			if (pci_data->cur_reg == PCI_COMMAND_STATUS_REG
  166| 			    && !((*data) & PCI_COMMAND_IO_ENABLE)) {
  167| 				fatal("\n[ NetBSD PCI detection stuff not"
  168| 				    " yet implemented for device '%s' ]\n",
  169| 				    dev->name);
  170| 			}
  171| 		}
  172| 		return;
  173| 	}
  174| 
  175| 	/*  Register read:  */
  176| 	*data = x;
  177| 
  178| 	pci_data->last_was_write_ffffffff = 0;
  179| 
  180| 	debug("[ bus_pci: read from PCI DATA, bus %i, device "
  181| 	    "%i, function %i (%s) register 0x%02x: (len=%i) 0x%08lx ]\n",
  182| 	    pci_data->cur_bus, pci_data->cur_device, pci_data->cur_func,
  183| 	    dev->name, pci_data->cur_reg, len, (long)*data);
  184| }
  185| 
  186| 
  187| /*
  188|  *  bus_pci_setaddr():
  189|  *
  190|  *  Sets the address in preparation for a PCI register transfer.
  191|  */
  192| void bus_pci_setaddr(struct cpu *cpu, struct pci_data *pci_data,
  193| 	int bus, int device, int function, int reg)
  194| {
  195| 	if (cpu == NULL || pci_data == NULL) {
  196| 		fatal("bus_pci_setaddr(): NULL ptr\n");
  197| 		exit(1);
  198| 	}
  199| 
  200| 	pci_data->cur_bus = bus;
  201| 	pci_data->cur_device = device;
  202| 	pci_data->cur_func = function;
  203| 	pci_data->cur_reg = reg;
  204| }
  205| 
  206| 
  207| /*
  208|  *  bus_pci_add():
  209|  *
  210|  *  Add a PCI device to a bus_pci device.
  211|  */
  212| void bus_pci_add(struct machine *machine, struct pci_data *pci_data,
  213| 	struct memory *mem, int bus, int device, int function,
  214| 	const char *name)
  215| {
  216| 	struct pci_device *pd;
  217| 	int ofs;
  218| 	void (*init)(struct machine *, struct memory *, struct pci_device *);
  219| 
  220| 	if (pci_data == NULL) {
  221| 		fatal("bus_pci_add(): pci_data == NULL!\n");
  222| 		abort();
  223| 	}
  224| 
  225| 	/*  Find the PCI device:  */
  226| 	init = pci_lookup_initf(name);
  227| 
  228| 	/*  Make sure this bus/device/function number isn't already in use:  */
  229| 	pd = pci_data->first_device;
  230| 	while (pd != NULL) {
  231| 		if (pd->bus == bus && pd->device == device &&
  232| 		    pd->function == function) {
  233| 			fatal("bus_pci_add(): (bus %i, device %i, function"
  234| 			    " %i) already in use\n", bus, device, function);
  235| 			exit(1);
  236| 		}
  237| 		pd = pd->next;
  238| 	}
  239| 
  240| 	CHECK_ALLOCATION(pd = (struct pci_device *) malloc(sizeof(struct pci_device)));
  241| 	memset(pd, 0, sizeof(struct pci_device));
  242| 
  243| 	/*  Add the new device first in the PCI bus' chain:  */
  244| 	pd->next = pci_data->first_device;
  245| 	pci_data->first_device = pd;
  246| 
```

### `src/include/bus_pci.h` around the row's cited line 85 (HEAD 8d9df658, lines 1-166)

```c
    1| #ifndef	BUS_PCI_H
    2| #define	BUS_PCI_H
    3| 
    4| /*
    5|  *  Copyright (C) 2004-2010  Anders Gavare.  All rights reserved.
    6|  *
    7|  *  Redistribution and use in source and binary forms, with or without
    8|  *  modification, are permitted provided that the following conditions are met:
    9|  *
   10|  *  1. Redistributions of source code must retain the above copyright
   11|  *     notice, this list of conditions and the following disclaimer.
   12|  *  2. Redistributions in binary form must reproduce the above copyright  
   13|  *     notice, this list of conditions and the following disclaimer in the 
   14|  *     documentation and/or other materials provided with the distribution.
   15|  *  3. The name of the author may not be used to endorse or promote products
   16|  *     derived from this software without specific prior written permission.
   17|  *
   18|  *  THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
   19|  *  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
   20|  *  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
   21|  *  ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE   
   22|  *  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
   23|  *  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
   24|  *  OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
   25|  *  HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
   26|  *  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
   27|  *  OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
   28|  *  SUCH DAMAGE.
   29|  *
   30|  *
   31|  *  PCI bus.
   32|  */
   33| 
   34| #include "misc.h"
   35| 
   36| #include "thirdparty/pcireg.h"
   37| 
   38| struct machine;
   39| struct memory;
   40| 
   41| struct pci_device;
   42| 
   43| 
   44| #ifndef BUS_PCI_C
   45| 
   46| struct pci_data;
   47| 
   48| #else
   49| 
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
   89| 
   90| #define	PCI_CFG_MEM_SIZE	0x100
   91| 
   92| struct pci_device {
   93| 	/*  Pointer to the next PCI device on this bus:  */
   94| 	struct pci_device	*next;
   95| 
   96| 	/*  Pointer back to the bus this device is connected to:  */
   97| 	struct pci_data		*pcibus;
   98| 
   99| 	/*  Short device name, and bus/device/function value:  */
  100| 	char			*name;
  101| 	int			bus, device, function;
  102| 
  103| 	/*  Configuration memory:  */
  104| 	unsigned char		cfg_mem[PCI_CFG_MEM_SIZE];
  105| 	unsigned char		cfg_mem_size[PCI_CFG_MEM_SIZE];
  106| 
  107| 	/*  Used when setting up the configuration registers:  */
  108| 	int			cur_mapreg_offset;
  109| 
  110| 	/*  Function to handle device-specific cfg register writes:  */
  111| 	int			(*cfg_reg_write)(struct pci_device *pd,
  112| 				    int reg, uint32_t value);
  113| 	void			*extra;
  114| };
  115| 
  116| #define	PCIINIT(name)	void pciinit_ ## name(struct machine *machine,	\
  117| 	struct memory *mem, struct pci_device *pd)
  118| 
  119| /*
  120|  *  Store little-endian config data in the pci_data struct's cfg_mem[]
  121|  *  or cfg_mem_size[], respectively.
  122|  */
  123| #define PCI_SET_DATA(ofs,value)	{					\
  124| 	pd->cfg_mem[(ofs)]     = (value) & 255;				\
  125| 	pd->cfg_mem[(ofs) + 1] = ((value) >> 8) & 255;			\
  126| 	pd->cfg_mem[(ofs) + 2] = ((value) >> 16) & 255;			\
  127| 	pd->cfg_mem[(ofs) + 3] = ((value) >> 24) & 255;			\
  128| 	}
  129| #define PCI_SET_DATA_SIZE(ofs,value)	{				\
  130| 	pd->cfg_mem_size[(ofs)]     = (value) & 255;			\
  131| 	pd->cfg_mem_size[(ofs) + 1] = ((value) >> 8) & 255;		\
  132| 	pd->cfg_mem_size[(ofs) + 2] = ((value) >> 16) & 255;		\
  133| 	pd->cfg_mem_size[(ofs) + 3] = ((value) >> 24) & 255;		\
  134| 	}
  135| 
  136| #endif
  137| 
  138| #define	BUS_PCI_ADDR	0xcf8
  139| #define	BUS_PCI_DATA	0xcfc
  140| 
  141| 
  142| /*
  143|  *  bus_pci.c:
  144|  */
  145| 
  146| /*  Run-time access:  */
  147| void bus_pci_decompose_1(uint32_t t, int *bus, int *dev, int *func, int *reg);
  148| void bus_pci_setaddr(struct cpu *cpu, struct pci_data *pci_data,
  149| 	int bus, int device, int function, int reg);
  150| void bus_pci_data_access(struct cpu *cpu, struct pci_data *pci_data,
  151| 	uint64_t *data, int len, int writeflag);
  152| 
  153| /*  Initialization:  */
  154| struct pci_data *bus_pci_init(struct machine *machine, const char *irq_path,
  155| 	uint64_t pci_actual_io_offset, uint64_t pci_actual_mem_offset,
  156| 	uint64_t pci_portbase, uint64_t pci_membase, const char *pci_irqbase,
  157| 	uint64_t isa_portbase, uint64_t isa_membase, const char *isa_irqbase);
  158| 
  159| /*  Add a PCI device to a PCI bus:  */
  160| void bus_pci_add(struct machine *machine, struct pci_data *pci_data,
  161| 	struct memory *mem, int bus, int device, int function,
  162| 	const char *name);
  163| 
  164| 
  165| #endif	/*  BUS_PCI_H  */
  166| 
```

## The data structures those files define (every field that exists)

### `src/include/bus_pci.h` -- `struct pci_data {` (HEAD lines 50-88)

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

End with one line: `FIXDRAFT_PCIBARSIZEFLAG: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
