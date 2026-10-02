# PANEL BRIEF -- three ARM findings graded HIGH by the retro-review

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

## H4 -- ARM: a control-register write that changes the byte-order bit ends the process

**The finding, as ruled:** a write to the CP15 control register (c1, opcode2 0) stores the guest's value; when its
byte-order bit differs from the byte order the machine was configured with, the handler calls `fatal()` + `exit(1)`.
A comment added by round #378 says the exit is load-bearing for decisions made at translation time.  Graded HIGH,
new.

`src/cpus/cpu_arm_coproc.c`, lines 131-178 at `db8b1a33`:

```
  131:         /*
  132:          *  Write to control:  Check each bit individually:
  133:          */
  134:         old_control = cpu->cd.arm.control;
  135:         cpu->cd.arm.control = cpu->cd.arm.r[rd];
  136:         if ((old_control & ARM_CONTROL_MMU) !=
  137:             (cpu->cd.arm.control & ARM_CONTROL_MMU)) {
  138:             debug("[ %s the MMU ]\n", cpu->cd.arm.control &
  139:                 ARM_CONTROL_MMU? "enabling" : "disabling");
  140:             cpu->translate_v2p =
  141:                 cpu->cd.arm.control & ARM_CONTROL_MMU?
  142:                 arm_translate_v2p_mmu : arm_translate_v2p;
  143:         }
  144:         if ((old_control & ARM_CONTROL_ALIGN) !=
  145:             (cpu->cd.arm.control & ARM_CONTROL_ALIGN))
  146:             debug("[ %s alignment checks ]\n", cpu->cd.arm.control &
  147:                 ARM_CONTROL_ALIGN? "enabling" : "disabling");
  148:         if ((old_control & ARM_CONTROL_CACHE) !=
  149:             (cpu->cd.arm.control & ARM_CONTROL_CACHE))
  150:             debug("[ %s the [data] cache ]\n", cpu->cd.arm.control &
  151:                 ARM_CONTROL_CACHE? "enabling" : "disabling");
  152:         if ((old_control & ARM_CONTROL_WBUFFER) !=
  153:             (cpu->cd.arm.control & ARM_CONTROL_WBUFFER))
  154:             debug("[ %s the write buffer ]\n", cpu->cd.arm.control &
  155:                 ARM_CONTROL_WBUFFER? "enabling" : "disabling");
  156: 
  157:         old_control &= ~ARM_CONTROL_BIG;
  158:         if (cpu->byte_order == EMUL_BIG_ENDIAN)
  159:             old_control |= ARM_CONTROL_BIG;
  160: 
  161:         if ((old_control & ARM_CONTROL_BIG) !=
  162:             (cpu->cd.arm.control & ARM_CONTROL_BIG)) {
  163:             /*  #378: this exit is LOAD-BEARING for translate-time
  164:                 byte-order decisions elsewhere: the LDM/STM fast-path
  165:                 install gate in cpu_arm_instr.c reads cpu->byte_order
  166:                 once, at translation, which is sound only because no
  167:                 route changes it afterwards (this one exits; SETEND
  168:                 is undecoded; every other write is machine setup).
  169:                 Implementing the switch therefore needs more than
  170:                 setting byte_order: invalidate_translation_caches(
  171:                 cpu, 0, INVALIDATE_ALL) so cached ic->f handlers are
  172:                 re-picked, AND re-translation of instruction words
  173:                 (the decoder itself reads byte_order), AND a revisit
  174:                 of that install gate.  */
  175:             fatal("ERROR: Trying to switch endianness. Not "
  176:                 "supported yet.\n");
  177:             exit(1);
  178:         }
```

Premises, as questions:
* Is this reachable only from a privileged guest mode, or can user code execute the `mcr`?  (The handler's caller is
  not shown; say if you cannot settle it.)
* The #378 comment says the alternative -- really switching byte order -- needs the translation caches invalidated,
  instruction words re-translated, and one install gate revisited.  So "delete the exit" is not an available option:
  it would leave a machine whose stored control bit disagrees with the byte order the translated code was built
  for.  Is "refuse the bit, keep the old byte order, announce once" sound -- and what does the guest then read back
  from the control register?
* **A wider question for the seats that can read the file.**  `grep -n 'exit(1)' src/cpus/cpu_arm_coproc.c` at
  `db8b1a33` prints thirteen lines, six of them commented out; the seven active ones are at lines 62, 177, 264, 322,
  331, 417 and 528.  H4 is the one at 177.  The one at 62 is `if (rd == ARM_PC)` -- a coprocessor instruction naming
  r15 -- at the top of the handler.  Which of the other six can a guest reach?

## H5 -- ARM: an exception whose vector cannot be translated re-enters the exception routine without bound

**The finding, as ruled:** this one is ALREADY in the queue, graded MED; the confirmation raised it to HIGH.  When an
instruction-address translation fails, the translator raises a prefetch abort itself; the exception routine sets the
program counter to the vector and asks for the vector's translation; if that fails too, the same thing happens
again, one stack frame deeper each time.  The host's stack runs out and the process ends.

`src/cpus/memory_arm.c`, lines 257-277 at `db8b1a33`:

```
  257: exception_return:
  258:     if (no_exceptions)
  259:         return 0;
  260: 
  261:     if (!quiet_mode) {
  262:         fatal("{ arm memory fault: vaddr=0x%08x domain=%i dav=%i ap=%i "
  263:             "access=%i user=%i", (int)vaddr, domain, dav, ap,
  264:             access, user);
  265:         fatal(" d=0x%08x d2=0x%08x pc=0x%08x }\n", d, d2, (int)cpu->pc);
  266:     }
  267: 
  268:     if (instr)
  269:         arm_exception(cpu, ARM_EXCEPTION_PREF_ABT);
  270:     else {
  271:         cpu->cd.arm.far = vaddr;
  272:         cpu->cd.arm.fsr = (domain << 4) | fs;
  273:         arm_exception(cpu, ARM_EXCEPTION_DATA_ABT);
  274:     }
  275: 
  276:     return 0;
  277: }
```

`src/cpus/cpu_arm.c`, lines 730-734 at `db8b1a33`:

```
  730:     cpu->cd.arm.r[ARM_LR] = retaddr;
  731:     cpu->pc = cpu->cd.arm.r[ARM_PC] = exception_nr * 4 +
  732:         ((cpu->cd.arm.control & ARM_CONTROL_V)? 0xffff0000 : 0);
  733:     quick_pc_to_pointers(cpu);
  734: }
```

`src/include/quick_pc_to_pointers.h`, lines 5-17 at `db8b1a33`:

```
    5: #ifdef MODE32
    6: #define    quick_pc_to_pointers(cpu) {                    \
    7:     uint32_t pc_tmp32 = cpu->pc;                    \
    8:     struct DYNTRANS_TC_PHYSPAGE *ppp_tmp;                \
    9:     ppp_tmp = cpu->cd.DYNTRANS_ARCH.phys_page[pc_tmp32 >> 12];    \
   10:     if (ppp_tmp != NULL) {                        \
   11:         cpu->cd.DYNTRANS_ARCH.cur_ic_page = &ppp_tmp->ics[0];    \
   12:         cpu->cd.DYNTRANS_ARCH.next_ic =                \
   13:             cpu->cd.DYNTRANS_ARCH.cur_ic_page +            \
   14:             DYNTRANS_PC_TO_IC_ENTRY(pc_tmp32);            \
   15:     } else                                \
   16:         DYNTRANS_PC_TO_POINTERS(cpu);                \
   17: }
```

`src/cpus/cpu_dyntrans.c`, lines 670-734 at `db8b1a33`:

```
  670:     if (!ok) {
  671:         uint64_t paddr;
  672:         if (cpu->translate_v2p != NULL) {
  673:             uint64_t vaddr =
  674: #if defined(MODE32) && defined(DYNTRANS_MIPS)
  675:             /*  32-bit MIPS is _sign_ extend, not zero.  */
  676:                 (int32_t)
  677: #endif
  678:                 cached_pc;
  679:             ok = cpu->translate_v2p(
  680:                 cpu, vaddr, &paddr, FLAG_INSTR);
  681:         } else {
  682:             paddr = cached_pc;
  683:             ok = 1;
  684:         }
  685:         if (!ok) {
       ...   [lines 686-694 elided: a comment: 'The PC is now set to the exception handler. Try to find the paddr in the translation arrays, or if that fails, call translate_v2p for the exception handler.']
  695: 
  696:             /*  If there was an exception, the PC has changed.
  697:                 Update cached_pc:  */
  698:             cached_pc = cpu->pc;
  699: 
  700: #ifdef MODE32
  701:             index = DYNTRANS_ADDR_TO_PAGENR(cached_pc);
  702:             if (cpu->cd.DYNTRANS_ARCH.host_load[index] != NULL) {
  703:                 paddr = cpu->cd.DYNTRANS_ARCH.phys_addr[index];
  704:                 ok = 1;
  705:             }
       ...   [lines 706-718 elided: the 64-bit (#else) arm of the same lookup]
  719: 
  720:             if (!ok) {
  721:                 ok = cpu->translate_v2p(cpu, cpu->pc, &paddr,
  722:                     FLAG_INSTR);
  723:             }
  724: 
       ...   [lines 725-727 elided: a commented-out printf]
  728: 
  729:             if (!ok) {
  730:                 fatal("FATAL: could not find physical"
  731:                     " address of the exception handler?");
  732:                 exit(1);
  733:             }
  734:         }
```

Premises, as questions:
* Walk the chain: `cpu_dyntrans.c:679` calls `translate_v2p(..., FLAG_INSTR)` -> on failure `memory_arm.c:269`
  calls `arm_exception(PREF_ABT)` -> `cpu_arm.c:733` `quick_pc_to_pointers` -> (no cached page) the generic
  pc-to-pointers routine -> line 679 again, now for the vector address.  Is there any point in that loop where a
  SECOND failure is detected and the recursion stops?  Note `cpu_dyntrans.c:729-733`: an `exit(1)` for "could not
  find physical address of the exception handler" -- is it ever reached on ARM, or does the recursion never return
  to it?
* What must the guest do to get here?  (My reading: turn the MMU on with page tables that do not map the vector
  page, then take any exception.)  Is that a guest a correct operating system would ever be, or only a faulty one?
* The queue row says the same shape exists on PowerPC and possibly SH and M88K.  Not shown here; say if you know.

## H6 -- ARM: a user-mode "load multiple with restore" stops the CPU

**The finding, as ruled:** found by the confirmation pass while checking another row.  `LDM` with the S bit set and
r15 in the register list restores the status register from the saved one for the current mode.  User and System
mode have no saved status register.  The handler clears its S flag in user mode but still marks the instruction as a
return; the return path then switches on the current mode, finds no case for user or system mode, and stops the CPU
(`cpu->running = 0`).  The architecture manual calls the instruction UNPREDICTABLE in those modes
(`ddi0100i.txt:8167-8168`, under "A4.1.22 LDM (3)": "This instruction is UNPREDICTABLE in User or System mode.").
Proposed HIGH; not yet a queue row.

`src/cpus/cpu_arm_instr.c`, lines 1604-1620 at `db8b1a33`:

```
 1604:     uint32_t addr = *np;
 1605:     unsigned char data[4];
 1606:     unsigned char *page;
 1607:     int i, return_flag = 0;
 1608:     uint32_t new_values[16];
 1609: 
 1610:     if (s_bit) {
 1611:         /*  Load to USR registers:  */
 1612:         if ((cpu->cd.arm.cpsr & ARM_FLAG_MODE) == ARM_MODE_USR32) {
 1613:             fatal("[ bdt_load: s-bit: in usermode? ]\n");
 1614:             s_bit = 0;
 1615:         }
 1616:         if (iw & 0x8000) {
 1617:             s_bit = 0;
 1618:             return_flag = 1;
 1619:         }
 1620:     }
```

`src/cpus/cpu_arm_instr.c`, lines 1780-1808 at `db8b1a33`:

```
 1780:     if (return_flag) {
 1781:         uint32_t new_cpsr;
 1782:         int switch_register_banks;
 1783: 
 1784:         switch (cpu->cd.arm.cpsr & ARM_FLAG_MODE) {
 1785:         case ARM_MODE_FIQ32:
 1786:             new_cpsr = cpu->cd.arm.spsr_fiq; break;
 1787:         case ARM_MODE_ABT32:
 1788:             new_cpsr = cpu->cd.arm.spsr_abt; break;
 1789:         case ARM_MODE_UND32:
 1790:             new_cpsr = cpu->cd.arm.spsr_und; break;
 1791:         case ARM_MODE_IRQ32:
 1792:             new_cpsr = cpu->cd.arm.spsr_irq; break;
 1793:         case ARM_MODE_SVC32:
 1794:             new_cpsr = cpu->cd.arm.spsr_svc; break;
 1795:         default:fatal("bdt_load: unimplemented mode %i\n",
 1796:                 cpu->cd.arm.cpsr & ARM_FLAG_MODE);
 1797:             cpu->running = 0;
 1798:             cpu->cd.arm.next_ic = &nothing_call;
 1799:             return;
 1800:         }
 1801: 
 1802:         switch_register_banks = (cpu->cd.arm.cpsr & ARM_FLAG_MODE) !=
 1803:             (new_cpsr & ARM_FLAG_MODE);
 1804: 
 1805:         if (switch_register_banks)
 1806:             arm_save_register_bank(cpu);
 1807: 
 1808:         cpu->cd.arm.cpsr = new_cpsr;
```

Premises, as questions:
* In USR32: line 1612 is true, so `s_bit = 0`; then line 1616 tests `iw & 0x8000` INSIDE the outer `if (s_bit)` --
  which was entered while `s_bit` was still set.  So is `return_flag` set for a user-mode instruction?  And in SYS32,
  where line 1612 is false?
* With `return_flag` set, does the `switch` at line 1784 reach `default:` for both USR32 and SYS32?
* This instruction is unprivileged.  If the premises hold, ONE word in an ordinary user program stops the emulated
  machine.  UNPREDICTABLE leaves the result open but an implementation must not let user code halt the system:
  what should the model do -- ignore the S bit and load the registers, or raise the undefined-instruction exception?

## THE QUESTIONS (please answer all; they are short)

Q1. **The premise audit.**  For each of H4, H5 and H6: is the path reachable from code running in the guest, as the
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
