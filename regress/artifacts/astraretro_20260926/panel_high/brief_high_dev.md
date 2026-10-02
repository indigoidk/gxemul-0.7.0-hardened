# PANEL BRIEF -- one device finding graded HIGH, and two severity disputes, from the retro-review

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly.  **Check the premises,
not just the derivations.**  Where I state something as fact, ask whether it is true.  A seat that re-derives a
premise from something this brief did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`**, at commit `db8b1a33`.  There are THREE pristine-2021-upstream copies of
GXemul under the project root (`./src/` and two under `_archive/audit-results-*/builds/`).  They are NOT this fork.
If your line numbers disagree with mine by hundreds you are reading one of them -- say so rather than reconciling.
Seats that read files: scope your reading to `GXEMUL-SEC/src/` and `GXEMUL-SEC/regress/*.py`; do not read
`regress/artifacts/` or `tools/pipeline/ledger.json`.

**If you cannot read files that is expected** -- every fact you need is inlined.  Name any premise you cannot settle
from this packet rather than guessing at it.

**Where this brief states an ARITHMETIC claim -- an index range, an offset, a count of reachable addresses --
ENUMERATE it rather than reasoning about it.**  And enumerate the right DOMAIN: ask what the producer of these values
can actually emit before you walk them.

**VERDICT LINE FIRST**, so your answer survives truncation: `VERDICT: <n> of 3 findings hold as stated -- <one clause>`.

## WHAT THIS IS

This fork's old changes are being re-read, file by file, by one reviewing model (62 source files and bundles, 403
findings).  Each finding is then ruled on by a second model (the adjudicator) and checked by the first again (the
confirmation).  This packet puts THREE of the findings graded HIGH in front of the whole panel, with the source
inlined, so that every seat can check the evidence for itself.  **Nothing has been changed and no change is proposed
here**: a finding that survives becomes a correction round of its own, with its own design review.

The severity rule both reviewers applied: **HIGH** -- input under the guest's control makes the emulator process end,
makes one of its memory accesses leave a buffer's bounds, or stops it making progress.  **MED** -- guest-visible
behaviour differs from the hardware documentation.  **LOW** -- diagnostics, latent code, test coverage.

## SETTLED PREMISES (re-inlined so nobody spends an answer re-deriving them; each is checkable below)

S1. `fatal()` PRINTS and RETURNS.  It does not end the process; `exit(1)` does.
`src/core/debugmsg.c`, lines 384-391 at `db8b1a33`:

```
  384: void fatal(const char *fmt, ...)
  385: {
  386:     va_list argp;
  387: 
  388:     va_start(argp, fmt);
  389:     va_debug(argp, fmt);
  390:     va_end(argp);
  391: }
```

S2. An instruction word the decoder cannot translate reaches the shared `bad:` label, which reports, sets
`cpu->running = 0`, and redirects execution to a do-nothing instruction.  It stops that virtual CPU; it does not call
`exit()`.
`src/cpus/cpu_dyntrans.c`, lines 1983-2024 at `db8b1a33`:

```
 1983: bad:    /*
 1984:      *  Nothing was translated. (Unimplemented or illegal instruction.)
 1985:      */
 1986: 
 1987:     /*  Clear the translation, in case it was "half-way" done:  */
 1988:     ic->f = TO_BE_TRANSLATED;
 1989: 
 1990:     if (cpu->translation_readahead)
 1991:         return;
 1992: 
 1993: 
       ...   [lines 1994-2000 elided: a comment: 'Abort the emulation ... this is an unimplemented instruction that should be implemented for real']
 2001: 
 2002:     about_to_enter_single_step = true;
 2003: 
 2004:     if (cpu->is_32bit)
 2005:         debugmsg_cpu(cpu, SUBSYS_CPU, "", VERBOSITY_ERROR,
 2006:             "UNIMPLEMENTED instruction at 0x%" PRIx32, (uint32_t)cpu->pc);
 2007:     else
 2008:         debugmsg_cpu(cpu, SUBSYS_CPU, "", VERBOSITY_ERROR,
 2009:             "UNIMPLEMENTED instruction at 0x%" PRIx64, (uint64_t)cpu->pc);
 2010: 
 2011:     if (!(single_step || cpu->machine->instruction_trace))
 2012:         DISASSEMBLE(cpu, ib, 1, 0);
 2013: 
 2014:     cpu->running = 0;
 2015: 
 2016:     /*  Note: Single-stepping can jump here.  */
 2017: stop_running_translated:
 2018: 
 2019:     // This makes sure that we stop in the debugger, even if e.g.
 2020:     // "step 100" was executing and 50 steps remained.
 2021:     debugger_reset();
 2022: 
 2023:     ic = cpu->cd.DYNTRANS_ARCH.next_ic = &nothing_call;
 2024:     cpu->cd.DYNTRANS_ARCH.next_ic ++;
```

S3. When no machine is still running, the run loop ends (unless the debugger was asked to take over at the end of the
run), and `main()` returns 0.  So on a single-CPU machine "every CPU stopped" ends the emulation and the process.
`src/core/emul.c`, lines 1048-1060 at `db8b1a33`:

```
 1048:             any_machine_still_running |= machine_run(emul->machines[i]);
 1049: 
 1050:         emul_executing = false;
 1051: 
 1052:         if (!any_machine_still_running) {
 1053:             if (debugger_enter_at_end_of_run) {
 1054:                 debugmsg(SUBSYS_EMUL, NULL, VERBOSITY_WARNING, "All machines stopped.");
 1055:                 debugger_reset();
 1056:                 single_step = true;
 1057:             } else {
 1058:                 break;
 1059:             }
 1060:         }
```

`src/core/main.c`, lines 806-821 at `db8b1a33`:

```
  806:     /*  Run the emulation:  */
  807:     emul_run(emul);
  808: 
  809: 
  810:     /*
  811:      *  Deinitialize everything:
  812:      */
  813: 
  814:     console_deinit();
  815: 
  816:     emul_destroy(emul);
  817: 
  818:     settings_remove_all(global_settings);
  819:     settings_destroy(global_settings);
  820: 
  821:     return 0;
```

## H7 -- Dreamcast GD-ROM: a DMA transfer aimed at its own start register re-enters the handler without bound

**The finding, as ruled:** the DMA start arm copies the staged data to a guest-chosen physical address with
`memory_rw()`.  If that address is the DMA device's own start register, `memory_rw()` dispatches the write back into
the same handler, with the arming registers and the staged data unchanged -- so the start arm runs again, and again.
There is no in-flight guard.  The host's stack runs out and the process ends.  Graded HIGH, new.

`src/devices/dev_dreamcast_gdrom.c`, lines 1367-1395 at `db8b1a33`:

```
 1367: DEVICE_ACCESS(dreamcast_gdrom_dma)
 1368: {
 1369:     struct dreamcast_gdrom_data *d = (struct dreamcast_gdrom_data *) extra;
 1370:     uint64_t idata = 0, odata = 0;
 1371: 
 1372:     if (writeflag == MEM_WRITE)
 1373:         idata = memory_readmax64(cpu, data, len);
 1374: 
 1375:     /*  Default read:  */
 1376:     if (writeflag == MEM_READ)
 1377:         odata = d->dma_reg[relative_addr / sizeof(uint32_t)];
 1378: 
 1379:     switch (relative_addr) {
 1380: 
 1381:     case 0x04:    // destination address? e.g. 0x8c008000
 1382:     case 0x08:    // DMA length in bytes? e.g. 0x3800
 1383:     case 0x0c:    // count? e.g. 1
 1384:     case 0x14:    // "enable"?
 1385:         break;
 1386: 
 1387:     case 0x18:
 1388:         // GDROM DMA start?
 1389:         if (idata != 0) {
 1390:             if (d->dma_reg[0x0c / sizeof(uint32_t)] == 1 &&
 1391:                 d->dma_reg[0x14 / sizeof(uint32_t)] == 1) {
 1392:                 // GDROM DMA transfer.
 1393:                 uint32_t dst = d->dma_reg[0x04 / sizeof(uint32_t)];
 1394:                 int length = d->dma_reg[0x08 / sizeof(uint32_t)];
 1395:                 if (d->data == NULL) {
```

`src/devices/dev_dreamcast_gdrom.c`, lines 1497-1508 at `db8b1a33`:

```
 1497:                 fatal("[ dreamcast_gdrom_dma: Transfering %i bytes to 0x%08"
 1498:                     PRIx32 " (guest asked for %i) ]\n",
 1499:                     (int) d->data_len, dst, length);
 1500: 
 1501:                 dst &= 0x0fffffff;    // 0x8c008000 => 0x0c008000
 1502:                 cpu->memory_rw(cpu, cpu->mem, dst,
 1503:                     d->data, d->data_len, MEM_WRITE, PHYSICAL);
 1504: 
 1505:                 SYSASIC_TRIGGER_EVENT(SYSASIC_EVENT_GDROM_DMA);
 1506: 
 1507:                 idata = 0;
 1508:             } else {
```

`src/devices/dev_dreamcast_gdrom.c`, lines 1675-1682 at `db8b1a33`:

```
 1675:     if (writeflag == MEM_WRITE)
 1676:         d->dma_reg[relative_addr / sizeof(uint32_t)] = idata;
 1677: 
 1678:     if (writeflag == MEM_READ)
 1679:         memory_writemax64(cpu, data, len, odata);
 1680: 
 1681:     return 1;
 1682: }
```

`src/devices/dev_dreamcast_gdrom.c`, lines 1696-1697 at `db8b1a33`:

```
 1696:     memory_device_register(devinit->machine->memory, "gdrom_dma", 0x005f7400,
 1697:         0x80, dev_dreamcast_gdrom_dma_access, d, DM_DEFAULT, NULL);
```

How `memory_rw()` dispatches a physical write that lands in a device, and how the handler reads its operand:

`src/cpus/memory_rw.c`, lines 478-495 at `db8b1a33`:

```
  478:         /*  Scan through all devices:  */
  479:         do {
  480:             if (paddr >= mem->devices[i].baseaddr &&
  481:                 paddr < mem->devices[i].endaddr) {
  482:                 /*  Found a device, let's access it:  */
  483:                 mem->last_accessed_device = i;
  484: 
       ...   [lines 485-490 elided: a comment on zeroing the caller's buffer before a read]
  491:                 if (writeflag == MEM_READ)
  492:                     memset(data, 0, len);
  493: 
  494:                 paddr -= mem->devices[i].baseaddr;
  495:                 if (paddr + len > mem->devices[i].length) {
```

`src/cpus/memory_rw.c`, lines 523-524 at `db8b1a33`:

```
  523:                     len = mem->devices[i].length - paddr;
  524:                 }
```

`src/cpus/memory_rw.c`, lines 583-593 at `db8b1a33`:

```
  583:                 res = 0;
  584:                 if (!no_exceptions || (mem->devices[i].flags &
  585:                     DM_READS_HAVE_NO_SIDE_EFFECTS)) {
  586:                     bool running_before_device_access = cpu->running;
  587:                     res = mem->devices[i].f(cpu, mem, paddr,
  588:                         data, len, writeflag,
  589:                         mem->devices[i].extra);
  590: 
  591:                     if (running_before_device_access && !cpu->running)
  592:                         return MEMORY_ACCESS_FAILED;
  593:                 }
```

`src/core/memory.c`, lines 55-78 at `db8b1a33`:

```
   55: uint64_t memory_readmax64(struct cpu *cpu, unsigned char *buf, int len)
   56: {
   57:     int i, byte_order = cpu->byte_order;
   58:     uint64_t x = 0;
   59: 
   60:     if (len & MEM_PCI_LITTLE_ENDIAN) {
   61:         len &= ~MEM_PCI_LITTLE_ENDIAN;
   62:         byte_order = EMUL_LITTLE_ENDIAN;
   63:     }
   64: 
   65:     /*  Switch byte order for incoming data, if necessary:  */
   66:     if (byte_order == EMUL_BIG_ENDIAN)
   67:         for (i=0; i<len; i++) {
   68:             x <<= 8;
   69:             x |= buf[i];
   70:         }
   71:     else
   72:         for (i=len-1; i>=0; i--) {
   73:             x <<= 8;
   74:             x |= buf[i];
   75:         }
   76: 
   77:     return x;
   78: }
```

Premises, as questions -- ENUMERATE, do not reason:
* The guest writes 0x005f7418 (or an alias of it: line 1501 masks with 0x0fffffff) to `+0x04`, 1 to `+0x0c`, 1 to
  `+0x14`, stages data, and writes nonzero to `+0x18`.  The inner `memory_rw()` finds the device at base 0x005f7400,
  length 0x80; the relative address is 0x18; `len` is `data_len` clamped to 0x80 - 0x18 = 0x68.  Is that right?
* `memory_readmax64(cpu, data, 0x68)` on this little-endian CPU: which bytes of the staged data end up in `idata`
  after 104 shift-and-or steps into a 64-bit value -- and is the recursion therefore conditional on those bytes
  being nonzero?
* The register store at line 1676 runs AFTER the switch.  So during the recursion `dma_reg[0x0c/4]` and
  `dma_reg[0x14/4]` still hold 1.  Is anything else changed between one entry and the next that could end it?
* A destination of 0x005f7404 instead would overwrite the destination register itself on the way.  Does any other
  self-aimed destination recurse, or only ones that hit `+0x18` first?

## H8 -- SGI O2 (IP32) CRIME: a SEVERITY dispute.  MED or HIGH?

**The finding, as ruled:** the CRIME control register is 64 bits wide at offset 0x08, and every defined bit is in its
low 14 bits.  The register switch matches the offset 0x08 exactly and acts on the raw value of whatever access
reached it.  On this big-endian machine a 32-bit store to `+0x08` is the HIGH half of the register -- bits the header
reserves -- yet a value of 0x800 there is read as the hard-reset bit and stops every CPU.  (A 32-bit store to
`+0x0c`, the low half, where the bit really lives, does not reach this arm at all.)

`src/devices/dev_sgi_ip32.c`, lines 269-292 at `db8b1a33`:

```
  269:     if (len == 8) {
  270:         if (writeflag == MEM_WRITE)
  271:             d->reg[relative_addr / 8] = idata;
  272:         else
  273:             odata = d->reg[relative_addr / 8];
  274:     } else if (len == 4) {
  275:         if (writeflag == MEM_WRITE) {
  276:             if (relative_addr & 4) {
  277:                 d->reg[relative_addr / 8] &= ~0xffffffffULL;
  278:                 d->reg[relative_addr / 8] |= (uint32_t)idata;
  279:             } else {
  280:                 d->reg[relative_addr / 8] &= 0xffffffffULL;
  281:                 d->reg[relative_addr / 8] |= (uint64_t)(idata << 32ULL);
  282:             }
  283:         } else {
  284:             odata = d->reg[relative_addr / 8];
  285:             if (relative_addr & 4)
  286:                 odata = (int32_t)odata;
  287:             else
  288:                 odata = (int32_t)(odata >> 32);
  289:         }
  290:     } else {
  291:         fatal("crime access len = %i!\n", len);
  292:         exit(1);
```

`src/devices/dev_sgi_ip32.c`, lines 326-350 at `db8b1a33`:

```
  326:     case CRIME_CONTROL:    /*  0x008  */
  327:         /*  TODO: 64-bit write to CRIME_CONTROL, but some things
  328:             (such as NetBSD 1.6.2) write to 0x00c!  */
  329:         if (writeflag == MEM_WRITE) {
  330:             /*
  331:              *  0x200 = watchdog timer (according to NetBSD)
  332:              *  0x800 = "reboot" used by the IP32 PROM
  333:              */
  334:             if (idata & CRIME_CONTROL_DOG_ENABLE) {
  335:                 idata &= ~CRIME_CONTROL_DOG_ENABLE;
  336:             }
  337:             if (idata & CRIME_CONTROL_HARD_RESET) {
  338:                 int j;
  339: 
  340:                 /*  This is used by the IP32 PROM's
  341:                     "reboot" command:  */
  342:                 for (j=0; j<cpu->machine->ncpus; j++)
  343:                     cpu->machine->cpus[j]->running = 0;
  344: 
  345:                 idata &= ~CRIME_CONTROL_HARD_RESET;
  346:             }
  347: 
  348:             idata &= ~CRIME_CONTROL_ENDIANESS;
  349: 
  350:             if (idata != 0)
```

**The two positions, each in its own words:**
* The adjudicator, MED: "the lane defect grants a guest no capability it lacks through the modelled 64-bit HARD_RESET
  (a reset the guest may legitimately request); what it produces is guest-visible behaviour contrary to the header".
* The confirmation, HIGH: the action "stops all CPUs", after which the emulation ends and the process returns (S3
  above); "Existing legitimate reset capability does not exempt this unintended termination."

Premises, as questions:
* Is the behaviour as described -- `sw 0x800` to `+0x08` stops every CPU, `sw 0x800` to `+0x0c` does not?
  (Measured on 2026-09-13 by a seat that built and ran it; shown here only by the source.)
* **The rule question.**  A guest that writes the hard-reset bit correctly ALSO ends the emulation -- that is what the
  model does for a reset.  So is a second, incorrect way to reach the same outcome HIGH (the process ends on input
  the hardware would ignore) or MED (the guest gains nothing it could not already do)?  Say which and why; this
  ruling will be applied to other rows.

## H9 -- SuperH: a SEVERITY dispute.  An index one past an array that lands in the next field of the same struct

**The finding, as ruled:** with the double-precision mode bit set, the floating-point arithmetic handlers treat their
operand as a PAIR of 32-bit registers, `fr[n]` and `fr[n+1]`.  The decoder accepts any register field 0..15.  For
field 15 the second word is `fr[16]` -- one past the end of `fr[16]`, which is `xf[0]`, the first element of the
array declared immediately after it.  The manual's encoding for the double-precision form uses even fields only; an
odd field is a reserved combination.

`src/include/cpu_sh.h`, lines 100-107 at `db8b1a33`:

```
  100:     uint32_t    r[SH_N_GPRS];
  101:     uint32_t    r_bank[SH_N_GPRS_BANKED];
  102: 
  103:     /*  Floating-Point Registers:  */
  104:     uint32_t    fr[SH_N_FPRS];
  105:     uint32_t    xf[SH_N_FPRS];    /*  "Other bank."  */
  106: 
  107:     uint32_t    mach;        /*  Multiply-Accumulate High  */
```

`src/cpus/cpu_sh_instr.c`, lines 4951-4956 at `db8b1a33`:

```
 4951:     case 0xf:
 4952:         if (lo4 == 0x0) {
 4953:             /*  FADD FRm,FRn  */
 4954:             ic->f = instr(fadd_frm_frn);
 4955:             ic->arg[0] = (size_t)&cpu->cd.sh.fr[r4];
 4956:             ic->arg[1] = (size_t)&cpu->cd.sh.fr[r8];
```

`src/cpus/cpu_sh_instr.c`, lines 3371-3387 at `db8b1a33`:

```
 3371:     if (cpu->cd.sh.fpscr & SH_FPSCR_PR) {
 3372:         /*  Double-precision, using a pair of registers:  */
 3373:         int64_t r1, r2, ieee;
 3374:         double result;
 3375: 
 3376:         r1 = reg(ic->arg[0] + sizeof(uint32_t)) +
 3377:             ((uint64_t)reg(ic->arg[0]) << 32);
 3378:         r2 = reg(ic->arg[1] + sizeof(uint32_t)) +
 3379:             ((uint64_t)reg(ic->arg[1]) << 32);
 3380:         ieee_interpret_float_value(r1, &op1, IEEE_FMT_D);
 3381:         ieee_interpret_float_value(r2, &op2, IEEE_FMT_D);
 3382: 
 3383:         /*  #300: directed rounding via the 2Sum helper  */
 3384:         result = ieee_add_round_rm(op2.f, op1.f, sh_fp_rm(cpu));
 3385:         ieee = ieee_store_float_value(result, IEEE_FMT_D);
 3386:         reg(ic->arg[1]) = (uint32_t) (ieee >> 32);
 3387:         reg(ic->arg[1] + sizeof(uint32_t)) = (uint32_t) ieee;
```

**The two positions, each in its own words:**
* The adjudicator, LOW: "an out-of-ARRAY index that stays inside the cpu struct; no host-memory hazard ... an odd
  field under PR=1 is a reserved combination whose hardware behaviour is 'not guaranteed'".
* The confirmation, HIGH: "Remaining inside the containing structure does not keep the access inside that array" --
  the severity rule's clause "makes one of its memory accesses leave a buffer's bounds", by its letter.

Premises, as questions:
* Is `fr[16]` (field 15, second word) really `xf[0]`, with no padding between two `uint32_t` arrays?  Both are
  `uint32_t[SH_N_FPRS]`; the claim is that they are adjacent members.
* **The rule question.**  The access leaves the ARRAY and stays in the STRUCT; what it reads and writes is the
  guest's own other-bank register.  Does the HIGH clause mean "leaves the C object the index was computed for" (then
  HIGH) or "reaches memory the guest has no business touching" (then not)?  This project has reduced a finding on
  exactly this ground before ("load-bearing host memory safety" became "intra-struct corruption" once `offsetof` was
  measured).  Say which reading you would adopt and why; this ruling will be applied to other rows.

## THE QUESTIONS (please answer all; they are short)

Q1. **The premise audit.**  For each of H7, H8 and H9: is the path reachable from code running in the guest, as the
reviewers describe?  Name the ONE premise that would make the finding false if it failed, and say whether you could
check it.

Q2. **WHICH OF THESE THREE DISPOSITIONS IS WRONG?**  Name the count.  A finding can be wrong in its reachability, in
its severity, or in being a duplicate of something already recorded.

Q3. **What should a correction round do -- and is that option available here?**  This project's set of dispositions
for an access the model cannot service: (1) delete the terminating call; (2) decline silently; (3) decline and
announce once per device or CPU; (4) accept -- the model already computes the right value; (5) fault -- deliver the
architecture's exception; (6) accept into invented backing store; (7) implement the missing behaviour.  For each
finding name the member you would choose and say whether the machinery it needs exists on THIS CPU (option 5 needs
the architecture's exception delivery to be modelled).  Is there a member this list does not name?

Q4. **Rank the three** by what an operating system in ordinary operation would actually meet, most likely first, and
say what you based the ranking on.

**The standing license:** if, while verifying a claim, you found something ELSE -- say so.
