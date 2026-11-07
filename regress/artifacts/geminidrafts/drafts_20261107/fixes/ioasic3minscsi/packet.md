# GXemul hardened fork -- DRAFT A FIX for one filed issue, `ioasic3minscsi` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `ioasic3minscsi`, state `open`, severity `MED`)

**title:** machines/machine_pmax.c 3MIN arm + devices/dev_dec_ioasic.c -- the 3MIN 53C94 has no DMA path through the IOASIC, so DMA lands in the asc's private buffer -- WRONG-RESULT (3MIN SCSI; write direction not assessed)

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T64 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: medium; report rows: A2-23).  Source URLs: https://github.com/rpajarola/gxemul/commit/bee311c1f3107283beb0e577173a640f18968eab.  Our site at de8c7547: src/machines/machine_pmax.c:309-310; src/devices/dev_dec_ioasic.c:83-90.  Portable fix: yes -- port rpajarola bee311c.  Filing check (TRIAGE.md): 0 hits for IOASIC / 3MIN.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port rpajarola bee311c is available

## The code at the cited lines

### `src/machines/machine_pmax.c` around the row's cited line 309 (HEAD 2d25df65, lines 264-354)

```c
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
```

### `src/devices/dev_dec_ioasic.c` around the row's cited line 83 (HEAD 2d25df65, lines 38-128)

```c
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
```

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
