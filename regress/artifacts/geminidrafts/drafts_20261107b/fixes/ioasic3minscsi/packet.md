# GXemul hardened fork -- DRAFT A FIX for one filed issue, `ioasic3minscsi` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `ioasic3minscsi`, state `open`, severity `MED`)

**title:** machines/machine_pmax.c 3MIN arm + devices/dev_dec_ioasic.c -- the 3MIN 53C94 has no DMA path through the IOASIC, so DMA lands in the asc's private buffer -- WRONG-RESULT (3MIN SCSI; write direction not assessed)

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T64 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: medium; report rows: A2-23).  Source URLs: https://github.com/rpajarola/gxemul/commit/bee311c1f3107283beb0e577173a640f18968eab.  Our site at de8c7547: src/machines/machine_pmax.c:309-310; src/devices/dev_dec_ioasic.c:83-90.  Portable fix: yes -- port rpajarola bee311c.  Filing check (TRIAGE.md): 0 hits for IOASIC / 3MIN.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port rpajarola bee311c is available

## The code at the cited lines

### `src/machines/machine_pmax.c` around the row's cited line 309 (HEAD 8d9df658, lines 189-429)

```c
  189| 		 *  Let's put in zero or more graphics boards:
  190| 		 *
  191| 		 *  TODO: It's also possible to have larger graphics cards that
  192| 		 *  occupy several slots. How should this be solved nicely?
  193| 		 */
  194| 
  195| 		snprintf(tmpstr, sizeof(tmpstr), "%s.cpu[%i].2.kn02.%i",
  196| 		    machine->path, machine->bootstrap_cpu, 0);
  197| 		dev_turbochannel_init(machine, mem, 0,
  198| 		    KN02_PHYS_TC_0_START, KN02_PHYS_TC_0_END,
  199| 		    machine->n_gfx_cards >= 1?
  200| 			turbochannel_default_gfx_card : "",
  201| 		    tmpstr);
  202| 
  203| 		snprintf(tmpstr, sizeof(tmpstr), "%s.cpu[%i].2.kn02.%i",
  204| 		    machine->path, machine->bootstrap_cpu, 1);
  205| 		dev_turbochannel_init(machine, mem, 1,
  206| 		    KN02_PHYS_TC_1_START, KN02_PHYS_TC_1_END,
  207| 		    machine->n_gfx_cards >= 2?
  208| 			turbochannel_default_gfx_card : "",
  209| 		    tmpstr);
  210| 
  211| 		snprintf(tmpstr, sizeof(tmpstr), "%s.cpu[%i].2.kn02.%i",
  212| 		    machine->path, machine->bootstrap_cpu, 2);
  213| 		dev_turbochannel_init(machine, mem, 2,
  214| 		    KN02_PHYS_TC_2_START, KN02_PHYS_TC_2_END,
  215| 		    machine->n_gfx_cards >= 3?
  216| 			turbochannel_default_gfx_card : "",
  217| 		    tmpstr);
  218| 
  219| 		/*  TURBOchannel slots 3 and 4 are reserved.  */
  220| 
  221| 		/*  TURBOchannel slot 5 is PMAZ-AA ("asc" SCSI).  */
  222| 		snprintf(tmpstr, sizeof(tmpstr), "%s.cpu[%i].2.kn02.%i",
  223| 		    machine->path, machine->bootstrap_cpu, 5);
  224| 		dev_turbochannel_init(machine, mem, 5,
  225| 		    KN02_PHYS_TC_5_START, KN02_PHYS_TC_5_END,
  226| 		    "PMAZ-AA", tmpstr);
  227| 
  228| 		/*  TURBOchannel slot 6 is PMAD-AA ("le" ethernet).  */
  229| 		snprintf(tmpstr, sizeof(tmpstr), "%s.cpu[%i].2.kn02.%i",
  230| 		    machine->path, machine->bootstrap_cpu, 6);
  231| 		dev_turbochannel_init(machine, mem, 6,
  232| 		    KN02_PHYS_TC_6_START, KN02_PHYS_TC_6_END,
  233| 		    "PMAD-AA", tmpstr);
  234| 
  235| 		/*  TURBOchannel slot 7 is system stuff.  */
  236| 		snprintf(tmpstr, sizeof(tmpstr), "%s.cpu[%i].2.kn02.%i",
  237| 		    machine->path, machine->bootstrap_cpu, 7);
  238| 		machine->main_console_handle =
  239| 		    dev_dc7085_init(machine, mem,
  240| 		    KN02_SYS_DZ, tmpstr, machine->x11_md.in_use);
  241| 
  242| 		snprintf(tmpstr, sizeof(tmpstr), "%s.cpu[%i].%i",
  243| 		    machine->path, machine->bootstrap_cpu, KN02_INT_CLOCK);
  244| 		dev_mc146818_init(machine, mem,
  245| 		    KN02_SYS_CLOCK, tmpstr, MC146818_DEC, 1);
  246| 
  247| 		framebuffer_console_name = "osconsole=0,7";
  248| 								/*  fb,keyb  */
  249| 		serial_console_name      = "osconsole=2";
  250| 		boot_scsi_boardnumber = 5;
  251| 		boot_net_boardnumber = 6;	/*  TODO: 3?  */
  252| 		break;
  253| 
  254| 	case MACHINE_DEC_3MIN_5000:		/*  type 3, KN02BA  */
  255| 		machine->machine_name = strdup("DECstation 5000/112, 125, or 145 (3MIN,"
  256| 		    " KN02BA)");
  257| 		if (machine->emulated_hz == 0)
  258| 			machine->emulated_hz = 33000000;
  259| 		if (machine->physical_ram_in_mb > 128)
  260| 			fprintf(stderr, "WARNING! Real 3MIN machines cannot "
  261| 			    "have more than 128MB RAM. Continuing anyway.\n");
  262| 
  263| 		/*  KN02BA "3min" TurboChannel interrupt controller:  */
  264| 		snprintf(tmpstr, sizeof(tmpstr), "kn02ba irq=%s.cpu[%i].%i",
  265| 		    machine->path, machine->bootstrap_cpu, KMIN_INT_TC3);
  266| 		device_add(machine, tmpstr);
  267| 
  268| 		/*
  269| 		 *  tc0 at mainbus0: 12.5 MHz clock  (0x10000000,slotsize=64MB)
  270| 		 *  tc slot 1:   0x14000000
  271| 		 *  tc slot 2:   0x18000000
  272| 		 *  ioasic0 at tc0 slot 3 offset 0x0	(0x1c000000) slot 0
  273| 		 *  asic regs				(0x1c040000) slot 1
  274| 		 *  station's ether address		(0x1c080000) slot 2
  275| 		 *  le0 at ioasic0 offset 0xc0000: address 00:00:00:00:00:00
  276| 		 *					(0x1c0c0000) slot 3
  277| 		 *  scc0 at ioasic0 offset 0x100000	(0x1c100000) slot 4
  278| 		 *  scc1 at ioasic0 offset 0x180000: console(0x1c180000) slot 6
  279| 		 *  mcclock0 at ioasic0 offset 0x200000: mc146818 or
  280| 		 *	compatible			(0x1c200000) slot 8
  281| 		 *  asc0 at ioasic0 offset 0x300000: NCR53C94, 25MHz,
  282| 		 *	SCSI ID 7			(0x1c300000) slot 12
  283| 		 *  dma for asc0			(0x1c380000) slot 14
  284| 		 */
  285| 
  286| ////fatal("TODO: kmin dev_le_init.\n");
  287| ////abort();
  288| //		dev_le_init(machine, mem, 0x1c0c0000, 0, 0,
  289| //		    KMIN_INTR_LANCE + 8, 4 * 65536);
  290| 
  291| 		snprintf(tmpstr, sizeof(tmpstr), "%s.cpu[%i].%i.kn02ba.0x%x",
  292| 		    machine->path, machine->bootstrap_cpu, KMIN_INT_TC3, KMIN_INTR_SCC_0);
  293| 		dev_scc_init(machine, mem, 0x1c100000, tmpstr,
  294| 		    machine->x11_md.in_use, 0, 1);
  295| 
  296| 		snprintf(tmpstr, sizeof(tmpstr), "%s.cpu[%i].%i.kn02ba.0x%x",
  297| 		    machine->path, machine->bootstrap_cpu, KMIN_INT_TC3, KMIN_INTR_SCC_1);
  298| 		dev_scc_init(machine, mem, 0x1c180000, tmpstr,
  299| 		    machine->x11_md.in_use, 1, 1);
  300| 
  301| 
  302| 		snprintf(tmpstr, sizeof(tmpstr), "%s.cpu[%i].%i.kn02ba.0x%x",
  303| 		    machine->path, machine->bootstrap_cpu, KMIN_INT_TC3, KMIN_INTR_CLOCK);
  304| 		dev_mc146818_init(machine, mem,
  305| 		    KMIN_SYS_CLOCK, tmpstr, MC146818_DEC, 1);
  306| 		    
  307| 		snprintf(tmpstr, sizeof(tmpstr), "%s.cpu[%i].%i.kn02ba.0x%x",
  308| 		    machine->path, machine->bootstrap_cpu, KMIN_INT_TC3, KMIN_INTR_SCSI);
  309| 		dev_asc_init(machine, mem, 0x1c300000, tmpstr,
  310| 		    NULL, DEV_ASC_DEC, NULL, NULL);
  311| 
  312| 		/*
  313| 		 *  TURBOchannel slots 0, 1, and 2 are free for
  314| 		 *  option cards.  These are by default filled with
  315| 		 *  zero or more graphics boards.
  316| 		 *
  317| 		 *  TODO: irqs 
  318| 		 */
  319| 
  320| 		snprintf(tmpstr, sizeof(tmpstr), "%s.cpu[%i].%i",
  321| 		    machine->path, machine->bootstrap_cpu, KMIN_INT_TC0);
  322| 		dev_turbochannel_init(machine, mem, 0,
  323| 		    KMIN_PHYS_TC_0_START, KMIN_PHYS_TC_0_END,
  324| 		    machine->n_gfx_cards >= 1?
  325| 			turbochannel_default_gfx_card : "",
  326| 		    tmpstr);
  327| 
  328| 		snprintf(tmpstr, sizeof(tmpstr), "%s.cpu[%i].%i",
  329| 		    machine->path, machine->bootstrap_cpu, KMIN_INT_TC1);
  330| 		dev_turbochannel_init(machine, mem, 0,
  331| 		    KMIN_PHYS_TC_1_START, KMIN_PHYS_TC_1_END,
  332| 		    machine->n_gfx_cards >= 2?
  333| 			turbochannel_default_gfx_card : "",
  334| 		    tmpstr);
  335| 
  336| 		snprintf(tmpstr, sizeof(tmpstr), "%s.cpu[%i].%i",
  337| 		    machine->path, machine->bootstrap_cpu, KMIN_INT_TC2);
  338| 		dev_turbochannel_init(machine, mem, 0,
  339| 		    KMIN_PHYS_TC_2_START, KMIN_PHYS_TC_2_END,
  340| 		    machine->n_gfx_cards >= 3?
  341| 			turbochannel_default_gfx_card : "",
  342| 		    tmpstr);
  343| 
  344| 		/*  (kmin shared irq numbers (IP) are offset by +8 in the
  345| 		    emulator)  */
  346| 		/*  kmin_csr = dev_kmin_init(cpu, mem, KMIN_REG_INTR);  */
  347| 
  348| 		framebuffer_console_name = "osconsole=0,3";	/* fb,keyb(?) */
  349| 		serial_console_name      = "osconsole=3";	/* ? */
  350| 		break;
  351| 
  352| 	case MACHINE_DEC_3MAXPLUS_5000:	/*  type 4, KN03  */
  353| 		machine->machine_name = strdup("DECsystem 5900 or 5000 (3MAX+) (KN03)");
  354| 
  355| 		/*  5000/240 (KN03-GA, R3000): 40 MHz  */
  356| 		/*  5000/260 (KN05-NB, R4000): 60 MHz  */
  357| 		/*  TODO: are both these type 4?  */
  358| 		if (machine->emulated_hz == 0)
  359| 			machine->emulated_hz = 40000000;
  360| 		if (machine->physical_ram_in_mb > 480)
  361| 			fprintf(stderr, "WARNING! Real KN03 machines cannot "
  362| 			    "have more than 480MB RAM. Continuing anyway.\n");
  363| 
  364| 		/*  KN03 interrupts:  */
  365| fatal("TODO: Legacy rewrite\n");
  366| abort();
  367| //		machine->md_interrupt = kn03_interrupt;
  368| 
  369| 		/*
  370| 		 *  tc0 at mainbus0: 25 MHz clock (slot 0)	(0x1e000000)
  371| 		 *  tc0 slot 1					(0x1e800000)
  372| 		 *  tc0 slot 2					(0x1f000000)
  373| 		 *  ioasic0 at tc0 slot 3 offset 0x0		(0x1f800000)
  374| 		 *    something that has to do with interrupts? (?)(0x1f840000?)
  375| 		 *  le0 at ioasic0 offset 0xc0000		(0x1f8c0000)
  376| 		 *  scc0 at ioasic0 offset 0x100000		(0x1f900000)
  377| 		 *  scc1 at ioasic0 offset 0x180000: console	(0x1f980000)
  378| 		 *  mcclock0 at ioasic0 offset 0x200000: mc146818 or
  379| 		 *	compatible				(0x1fa00000)
  380| 		 *  asc0 at ioasic0 offset 0x300000: NCR53C94, 25MHz,
  381| 		 *	SCSI ID 7				(0x1fb00000)
  382| 		 */
  383| fatal("TODO: dec_ioasic legacy rewrite\n");
  384| abort();
  385| //		machine->md_int.dec_ioasic_data = dev_dec_ioasic_init(cpu,
  386| //		    mem, 0x1f800000, 0);
  387| 
  388| fatal("TODO: kn03 dev_le_init rewrite\n");
  389| abort();
  390| //		dev_le_init(machine, mem, KN03_SYS_LANCE, 0, 0,
  391| //		    KN03_INTR_LANCE +8, 4 * 65536);
  392| 
  393| fatal("TODO: dec_ioasic legacy rewrite\n");
  394| abort();
  395| //		machine->md_int.dec_ioasic_data->dma_func[3] =
  396| //		    dev_scc_dma_func;
  397| //		machine->md_int.dec_ioasic_data->dma_func_extra[2] =
  398| //		    dev_scc_init(machine, mem, KN03_SYS_SCC_0,
  399| //		    KN03_INTR_SCC_0 +8, machine->x11_md.in_use, 0, 1);
  400| //		machine->md_int.dec_ioasic_data->dma_func[2] =
  401| //		    dev_scc_dma_func;
  402| //		machine->md_int.dec_ioasic_data->dma_func_extra[3] =
  403| //		    dev_scc_init(machine, mem, KN03_SYS_SCC_1,
  404| //		    KN03_INTR_SCC_1 +8, machine->x11_md.in_use, 1, 1);
  405| 
  406| fatal("TODO: mc146818 irq\n");
  407| abort();
  408| //		dev_mc146818_init(machine, mem, KN03_SYS_CLOCK, KN03_INT_RTC,
  409| //		    MC146818_DEC, 1);
  410| fatal("TODO: asc init rewrite\n");
  411| abort();
  412| //		dev_asc_init(machine, mem, KN03_SYS_SCSI,
  413| //		    KN03_INTR_SCSI +8, NULL, DEV_ASC_DEC, NULL, NULL);
  414| 
  415| 		/*
  416| 		 *  TURBOchannel slots 0, 1, and 2 are free for
  417| 		 *  option cards.  These are by default filled with
  418| 		 *  zero or more graphics boards.
  419| 		 *
  420| 		 *  TODO: irqs 
  421| 		 */
  422| fatal("TODO: turbochannel rewrite init\n");
  423| abort();
  424| #if 0
  425| 		dev_turbochannel_init(machine, mem, 0,
  426| 		    KN03_PHYS_TC_0_START, KN03_PHYS_TC_0_END,
  427| 		    machine->n_gfx_cards >= 1?
  428| 			turbochannel_default_gfx_card : "",
  429| 		    KN03_INTR_TC_0 +8);
```

### `src/devices/dev_dec_ioasic.c` around the row's cited line 83 (HEAD 8d9df658, lines 1-203)

```c
    1| /*
    2|  *  Copyright (C) 2004-2018  Anders Gavare.  All rights reserved.
    3|  *
    4|  *  Redistribution and use in source and binary forms, with or without
    5|  *  modification, are permitted provided that the following conditions are met:
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
   28|  *  COMMENT: IOASIC device used in some DECstation machines
   29|  *
   30|  *  TODO:  Lots of stuff, such as DMA and all bits in the control registers.
   31|  */
   32| 
   33| #include <stdio.h>
   34| #include <stdlib.h>
   35| #include <string.h>
   36| 
   37| #include "cpu.h"
   38| #include "devices.h"
   39| #include "interrupt.h"
   40| #include "memory.h"
   41| #include "misc.h"
   42| 
   43| #include "thirdparty/dec_kn03.h"
   44| #include "thirdparty/tc_ioasicreg.h"
   45| 
   46| 
   47| #define IOASIC_DEBUG
   48| /* #define debug fatal */
   49| 
   50| 
   51| void dec_ioasic_reassert(struct dec_ioasic_data* d)
   52| {
   53| 	// printf("[ intr = 0x%08x, imsk = 0x%08x ]\n", d->intr, d->imsk);
   54| 
   55| 	if (d->intr & d->imsk && !d->int_asserted) {
   56| 		d->int_asserted = 1;
   57| 		d->irq->interrupt_assert(d->irq);
   58| 	}
   59| 	if (!(d->intr & d->imsk) && d->int_asserted) {
   60| 		d->int_asserted = 0;
   61| 		d->irq->interrupt_deassert(d->irq);
   62| 	}
   63| }
   64| 
   65| 
   66| DEVICE_ACCESS(dec_ioasic)
   67| {
   68| 	struct dec_ioasic_data *d = (struct dec_ioasic_data *) extra;
   69| 	uint64_t idata = 0, odata = 0;
   70| 	// uint64_t curptr;
   71| 	// uint32_t csr;
   72| 	// int dma_len, dma_res, regnr;
   73| 
   74| 	if (writeflag == MEM_WRITE)
   75| 		idata = memory_readmax64(cpu, data, len);
   76| 
   77| 	switch (relative_addr) {
   78| 	
   79| 	case 0:
   80| 		/*  NetBSD/pmax and OpenBSD/pmax read from this address.  */
   81| 		break;
   82| 
   83| 	case IOASIC_SCSI_DMAPTR:
   84| 		if (writeflag == MEM_WRITE)
   85| 			d->scsi_dmaptr = idata;
   86| 		else
   87| 			odata = d->scsi_dmaptr;
   88| 
   89| 		debug("[ dec_ioasic: %s SCSI_DMAPTR, data=0x%08" PRIx64 " ]\n",
   90| 			writeflag == MEM_WRITE ? "write to" : "read from",
   91| 			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
   92| 		break;
   93| 
   94| 	case IOASIC_SCSI_NEXTPTR:
   95| 		if (writeflag == MEM_WRITE)
   96| 			d->scsi_nextptr = idata;
   97| 		else
   98| 			odata = d->scsi_nextptr;
   99| 
  100| 		debug("[ dec_ioasic: %s SCSI_NEXTPTR, data=0x%08" PRIx64 " ]\n",
  101| 			writeflag == MEM_WRITE ? "write to" : "read from",
  102| 			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  103| 		break;
  104| 
  105| 	case IOASIC_LANCE_DMAPTR:
  106| 		if (writeflag == MEM_WRITE)
  107| 			d->lance_dmaptr = idata;
  108| 		else
  109| 			odata = d->lance_dmaptr;
  110| 
  111| 		debug("[ dec_ioasic: %s LANCE_DMAPTR, data=0x%08" PRIx64 " ]\n",
  112| 			writeflag == MEM_WRITE ? "write to" : "read from",
  113| 			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  114| 		break;
  115| 
  116| 	case IOASIC_FLOPPY_DMAPTR:
  117| 		if (writeflag == MEM_WRITE)
  118| 			d->floppy_dmaptr = idata;
  119| 		else
  120| 			odata = d->floppy_dmaptr;
  121| 
  122| 		debug("[ dec_ioasic: %s FLOPPY_DMAPTR, data=0x%08" PRIx64 " ]\n",
  123| 			writeflag == MEM_WRITE ? "write to" : "read from",
  124| 			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  125| 		break;
  126| 
  127| 	case IOASIC_ISDN_X_DMAPTR:
  128| 		if (writeflag == MEM_WRITE)
  129| 			d->isdn_x_dmaptr = idata;
  130| 		else
  131| 			odata = d->isdn_x_dmaptr;
  132| 
  133| 		debug("[ dec_ioasic: %s ISDN_X_DMAPTR, data=0x%08" PRIx64 " ]\n",
  134| 			writeflag == MEM_WRITE ? "write to" : "read from",
  135| 			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  136| 		break;
  137| 
  138| 	case IOASIC_ISDN_X_NEXTPTR:
  139| 		if (writeflag == MEM_WRITE)
  140| 			d->isdn_x_nextptr = idata;
  141| 		else
  142| 			odata = d->isdn_x_nextptr;
  143| 
  144| 		debug("[ dec_ioasic: %s ISDN_X_NEXTPTR, data=0x%08" PRIx64 " ]\n",
  145| 			writeflag == MEM_WRITE ? "write to" : "read from",
  146| 			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  147| 		break;
  148| 
  149| 	case IOASIC_ISDN_R_DMAPTR:
  150| 		if (writeflag == MEM_WRITE)
  151| 			d->isdn_r_dmaptr = idata;
  152| 		else
  153| 			odata = d->isdn_r_dmaptr;
  154| 
  155| 		debug("[ dec_ioasic: %s ISDN_R_DMAPTR, data=0x%08" PRIx64 " ]\n",
  156| 			writeflag == MEM_WRITE ? "write to" : "read from",
  157| 			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  158| 		break;
  159| 
  160| 	case IOASIC_ISDN_R_NEXTPTR:
  161| 		if (writeflag == MEM_WRITE)
  162| 			d->isdn_r_nextptr = idata;
  163| 		else
  164| 			odata = d->isdn_r_nextptr;
  165| 
  166| 		debug("[ dec_ioasic: %s ISDN_R_NEXTPTR, data=0x%08" PRIx64 " ]\n",
  167| 			writeflag == MEM_WRITE ? "write to" : "read from",
  168| 			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  169| 		break;
  170| 
  171| 	case IOASIC_CSR:
  172| 		if (writeflag == MEM_WRITE)
  173| 			d->csr = idata;
  174| 		else
  175| 			odata = d->csr;
  176| 
  177| 		debug("[ dec_ioasic: %s CSR, data=0x%08" PRIx64 " ]\n",
  178| 			writeflag == MEM_WRITE ? "write to" : "read from",
  179| 			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  180| #if 0
  181| 		if (writeflag == MEM_WRITE) {
  182| 			csr = d->reg[(IOASIC_CSR - IOASIC_SLOT_1_START) / 0x10];
  183| 
  184| 			d->reg[(IOASIC_INTR - IOASIC_SLOT_1_START) / 0x10] &=
  185| 			    ~IOASIC_INTR_T2_PAGE_END;
  186| 
  187| 			if (csr & IOASIC_CSR_DMAEN_T2) {
  188| 				/*  Transmit data:  */
  189| 				curptr = (d->reg[(IOASIC_SCC_T2_DMAPTR -
  190| 				    IOASIC_SLOT_1_START) / 0x10] >> 3)
  191| 				    | ((d->reg[(IOASIC_SCC_T2_DMAPTR -
  192| 				    IOASIC_SLOT_1_START) / 0x10] & 0x1f) << 29);
  193| 				dma_len = 0x1000 - (curptr & 0xffc);
  194| 
  195| 				if ((curptr & 0xfff) == 0)
  196| 					break;
  197| 
  198| 				if (d->dma_func[3] != NULL) {
  199| 					d->dma_func[3](cpu,
  200| 					    d->dma_func_extra[3], curptr,
  201| 					    dma_len, 1);
  202| 				} else
  203| 					fatal("[ dec_ioasic: DMA tx: data @ "
```

## The data structures those files define (every field that exists)

### `src/include/devices.h` -- `struct dec_ioasic_data` (HEAD lines 82-110)

```c
   82| struct dec_ioasic_data {
   83| 	uint32_t	scsi_dmaptr;		/*  0x000  */
   84| 	uint32_t	scsi_nextptr;		/*  0x010  */
   85| 	uint32_t	lance_dmaptr;		/*  0x020  */
   86| 	uint32_t	floppy_dmaptr;		/*  0x070  */
   87| 	uint32_t	isdn_x_dmaptr;		/*  0x080  */
   88| 	uint32_t	isdn_x_nextptr;		/*  0x090  */
   89| 	uint32_t	isdn_r_dmaptr;		/*  0x0a0  */
   90| 	uint32_t	isdn_r_nextptr;		/*  0x0b0  */
   91| 	uint32_t	csr;			/*  0x100  */
   92| 	uint32_t	intr;			/*  0x110  */
   93| 	uint32_t	imsk;			/*  0x120  */
   94| 	uint32_t	isdn_x_data;		/*  0x140  */
   95| 	uint32_t	isdn_r_data;		/*  0x150  */
   96| 	uint32_t	lance_decode;		/*  0x160  */
   97| 	uint32_t	scsi_decode;		/*  0x170  */
   98| 	uint32_t	scc0_decode;		/*  0x180  */
   99| 	uint32_t	scc1_decode;		/*  0x190  */
  100| 	uint32_t	floppy_decode;		/*  0x1a0  */
  101| 	uint32_t	scsi_scr;		/*  0x1b0  */
  102| 	uint32_t	scsi_sdr0;		/*  0x1c0  */
  103| 	uint32_t	scsi_sdr1;		/*  0x1d0  */
  104| 
  105| 	int		(*dma_func[MAX_IOASIC_DMA_FUNCTIONS])(struct cpu *, void *, uint64_t addr, size_t dma_len, int tx);
  106| 	void		*dma_func_extra[MAX_IOASIC_DMA_FUNCTIONS];
  107| 	int		rackmount_flag;
  108| 	struct interrupt *irq;
  109| 	int		int_asserted;
  110| };
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

End with one line: `FIXDRAFT_IOASIC3MINSCSI: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.

## YOUR PREVIOUS DRAFT SAID `STILL PRESENT: UNSETTLED` -- here is what it said was missing

```text
STILL PRESENT: UNSETTLED -- src/machines/machine_pmax.c:309
```json
[]
```
UNSETTLED: We need to see the declaration of `dev_asc_init` and the available `DEV_ASC_*` constants (likely in `src/include/devices.h` or `src/devices/dev_asc.h`) to determine how to configure the ASC to use the private DMA buffer at `0x1c380000` instead of the IOASIC DMA path. We also need to see how `dev_dec_ioasic` differentiates between 3MIN and 3MAX+ to conditionally handle `IOASIC_SCSI_DMAPTR`.
FIXDRAFT_IOASIC3MINSCSI: UNSETTLED PRESENT, 0 EDITS
```

## What you said was missing, from HEAD

### `src/devices/dev_asc.c` lines 1544-1560 (where HEAD defines `dev_asc_init`)

```c
 1544| }
 1545| 
 1546| 
 1547| /*
 1548|  *  dev_asc_init():
 1549|  *
 1550|  *  Register an 'asc' device.
 1551|  */
 1552| void dev_asc_init(struct machine *machine, struct memory *mem,
 1553| 	uint64_t baseaddr, const char *irq_path, void *turbochannel, int mode,
 1554| 	size_t (*dma_controller)(void *dma_controller_data,
 1555| 		unsigned char *data, size_t len, int writeflag),
 1556| 	void *dma_controller_data)
 1557| {
 1558| 	struct asc_data *d;
 1559| 
 1560| 	CHECK_ALLOCATION(d = (struct asc_data *) malloc(sizeof(struct asc_data)));
```

### `src/include/devices.h` lines 113-129 (where HEAD defines `dev_asc_init`)

```c
  113| struct dec_ioasic_data *dev_dec_ioasic_init(struct cpu *cpu, struct memory *mem, uint64_t baseaddr, int rackmount_flag, struct interrupt* irq);
  114| 
  115| /*  dev_asc.c:  */
  116| #define	DEV_ASC_DEC_LENGTH		0x40000
  117| #define	DEV_ASC_PICA_LENGTH		0x1000
  118| #define	DEV_ASC_DEC		1
  119| #define	DEV_ASC_PICA		2
  120| int dev_asc_access(struct cpu *cpu, struct memory *mem, uint64_t relative_addr, unsigned char *data, size_t len, int writeflag, void *);
  121| void dev_asc_init(struct machine *machine, struct memory *mem, uint64_t baseaddr,
  122| 	const char *irq_path, void *turbochannel, int mode,
  123| 	size_t (*dma_controller)(void *dma_controller_data,
  124| 		unsigned char *data, size_t len, int writeflag),
  125| 	void *dma_controller_data);
  126| 
  127| /*  dev_bt431.c:  */
  128| #define	DEV_BT431_LENGTH		0x20
  129| #define	DEV_BT431_NREGS			0x800	/*  ?  */
```

### `src/include/thirdparty/tc_ioasicreg.h` lines 88-104 (where HEAD defines `IOASIC_SCSI_DMAPTR`)

```c
   88| #define IOASIC_SLOT_14_START		0x380000
   89| #define IOASIC_SLOT_15_START		0x3c0000
   90| #define IOASIC_SLOTS_END		0x3fffff
   91| 
   92| /*
   93|  *  Register offsets (slot 1)
   94|  */
   95| 
   96| #define IOASIC_SCSI_DMAPTR		IOASIC_SLOT_1_START+0x000
   97| #define IOASIC_SCSI_NEXTPTR		IOASIC_SLOT_1_START+0x010
   98| #define IOASIC_LANCE_DMAPTR		IOASIC_SLOT_1_START+0x020
   99| #define IOASIC_SCC_T1_DMAPTR		IOASIC_SLOT_1_START+0x030
  100| #define IOASIC_SCC_R1_DMAPTR		IOASIC_SLOT_1_START+0x040
  101| #define IOASIC_SCC_T2_DMAPTR		IOASIC_SLOT_1_START+0x050
  102| #define IOASIC_SCC_R2_DMAPTR		IOASIC_SLOT_1_START+0x060
  103| #define IOASIC_FLOPPY_DMAPTR		IOASIC_SLOT_1_START+0x070
  104| #define IOASIC_ISDN_X_DMAPTR		IOASIC_SLOT_1_START+0x080
```


Now draft the fix, or -- if it still cannot be written from what is shown -- say `STILL PRESENT: UNSETTLED` and name the
exact definition or function still missing.  A name that appears in no section of this packet does not exist in HEAD; do
not use it.  Do not return an empty edit list, and do not return edits that change only comments.
