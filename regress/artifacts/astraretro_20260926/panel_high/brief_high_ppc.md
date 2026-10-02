# PANEL BRIEF -- three PowerPC findings graded HIGH by the retro-review

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

## H1 -- PowerPC: a block-translation (BAT) hit that denies the access ends the process

**The finding, as ruled:** with address translation on, a BAT entry that MATCHES the address but whose protection
bits deny the access makes `ppc_bat()` return 0, and `ppc_translate_v2p()` answers a 0 with `fatal()` + `exit(1)`.
The PowerPC architecture makes that case a DSI or ISI exception (a block memory-protection violation).  The reviewers
add that the test sits BEFORE the no-exceptions test, so a debugger memory dump of such a block reaches it too.
Graded HIGH, new.

`src/cpus/memory_ppc.c`, lines 43-80 at `db8b1a33`:

```
   43: static int ppc_bat_block(struct cpu *cpu, uint64_t vaddr, uint64_t *return_paddr,
   44:     int flags, int user, int istart, int iend, int base_spr)
   45: {
   46:     int i, pp;
   47: 
   48:     for (i=istart; i<iend; i++) {
   49:         int regnr = base_spr + i * 2;
   50:         uint32_t upper = cpu->cd.ppc.spr[regnr];
   51:         uint32_t lower = cpu->cd.ppc.spr[regnr + 1];
   52:         uint32_t phys = lower & BAT_RPN, ebs = upper & BAT_EPI;
   53:         uint32_t mask = ((upper & BAT_BL) << 15) | 0x1ffff;
   54: 
   55:         /*  Not valid in either supervisor or user mode?  */
   56:         if (user && !(upper & BAT_Vu))
   57:             continue;
   58:         if (!user && !(upper & BAT_Vs))
   59:             continue;
   60: 
   61:         /*  Virtual address mismatch? Then skip.  */
   62:         if ((vaddr & ~mask) != (ebs & ~mask))
   63:             continue;
   64: 
   65:         *return_paddr = (vaddr & mask) | (phys & ~mask);
   66: 
   67:         pp = lower & BAT_PP;
   68:         switch (pp) {
   69:         case BAT_PP_NONE:
   70:             return 0;
   71:         case BAT_PP_RO_S:
   72:         case BAT_PP_RO:
   73:             return (flags & FLAG_WRITEFLAG)? 0 : 1;
   74:         default:/*  BAT_PP_RW:  */
   75:             return 2;
   76:         }
   77:     }
   78: 
   79:     return -1;
   80: }
```

`src/cpus/memory_ppc.c`, lines 245-300 at `db8b1a33`:

```
  245: int ppc_translate_v2p(struct cpu *cpu, uint64_t vaddr,
  246:     uint64_t *return_paddr, int flags)
  247: {
  248:     int instr = flags & FLAG_INSTR, res = 0, match, user;
  249:     int writeflag = flags & FLAG_WRITEFLAG? 1 : 0;
  250:     uint64_t msr;
  251: 
  252:     reg_access_msr(cpu, &msr, 0, 0);
  253:     user = msr & PPC_MSR_PR? 1 : 0;
  254: 
  255:     if (cpu->cd.ppc.bits == 32)
  256:         vaddr &= 0xffffffff;
  257: 
  258:     if ((instr && !(msr & PPC_MSR_IR)) || (!instr && !(msr & PPC_MSR_DR))) {
  259:         *return_paddr = vaddr;
  260:         return 2;
  261:     }
  262: 
  263:     if (cpu->cd.ppc.cpu_type.flags & PPC_601) {
  264:         fatal("ppc_translate_v2p(): TODO: 601\n");
  265:         exit(1);
  266:     }
  267: 
  268:     /*  Try the BATs first:  */
  269:     if (cpu->cd.ppc.bits == 32) {
  270:         res = ppc_bat(cpu, vaddr, return_paddr, flags, user);
  271:         if (res > 0)
  272:             return res;
  273:         if (res == 0) {
  274:             fatal("[ TODO: BAT exception ]\n");
  275:             exit(1);
  276:         }
  277:     }
  278: 
  279:     /*  Virtual to physical translation:  */
  280:     if (cpu->cd.ppc.bits == 32) {
  281:         match = ppc_vtp32(cpu, vaddr, return_paddr, &res, msr,
  282:             writeflag, instr);
  283:         if (match && res > 0)
  284:             return res;
  285:     } else {
  286:         /*  htaborg = sdr1 & 0xfffffffffffc0000ULL;  */
  287:         fatal("TODO: ppc 64-bit translation\n");
  288:         exit(1);
  289:     }
  290: 
  291: 
  292:     /*
  293:      *  No match? Then cause an exception.
  294:      *
  295:      *  PPC603: cause a software TLB reload exception.
  296:      *  All others: cause a DSI or ISI.
  297:      */
  298: 
  299:     if (flags & FLAG_NOEXCEPTIONS)
  300:         return 0;
```

Premises, as questions:
* Does `ppc_bat_block()` return 0 in exactly two cases -- a matching entry with PP = 00, and a STORE through a
  matching read-only entry -- and -1 when nothing matches?
* Is line 273's `res == 0` arm reached before line 299's `FLAG_NOEXCEPTIONS` test, for every caller?
* The BAT registers are written by `mtspr` in supervisor state.  Can code in the guest's USER state reach this, or
  only its kernel?  Would an ordinary kernel program a PP = 00 block, or a read-only one that user code then stores to?
* The manual text I am relying on: `ppc_pem32_rev2_2001.txt:13503-13519` is Figure 7-9, "Memory Protection Violation
  Flow for Blocks", which ends in "ISI Exception" / "DSI Exception".  I read the figure's extracted text, not a prose
  statement -- say so if that matters.

## H2 -- PowerPC: the single-precision fused multiply-add family is not decoded, and stops the CPU

**The finding, as ruled:** primary opcode 59 decodes only `fdivs`, `fsubs`, `fadds` and `fmuls`.  Every other
opcode-59 word -- the four fused forms `fmadds`, `fmsubs`, `fnmadds`, `fnmsubs` and their record forms among them --
reaches `goto bad` (S2 above).  Graded HIGH, new for `fnmadds`/`fnmsubs`; `fmadds`/`fmsubs` are already recorded.

`src/cpus/cpu_ppc_instr.c`, lines 5195-5226 at `db8b1a33`:

```
 5195:         /*  NOTE: Some floating-point instructions are selected
 5196:             using only the lowest 5 bits, not all 10!  */
 5197:         switch (xo & 31) {
 5198:         case PPC_59_FDIVS:
 5199:         case PPC_59_FSUBS:
 5200:         case PPC_59_FADDS:
 5201:             switch (xo & 31) {
 5202:             case PPC_59_FDIVS: ic->f = instr(fdivs); rc_f = instr(fdivs_dot); break;
 5203:             case PPC_59_FSUBS: ic->f = instr(fsubs); rc_f = instr(fsubs_dot); break;
 5204:             case PPC_59_FADDS: ic->f = instr(fadds); rc_f = instr(fadds_dot); break;
 5205:             }
 5206:             ic->arg[0] = (size_t)(&cpu->cd.ppc.fpr[ra]);
 5207:             ic->arg[1] = (size_t)(&cpu->cd.ppc.fpr[rb]);
 5208:             ic->arg[2] = (size_t)(&cpu->cd.ppc.fpr[rt]);
 5209:             break;
 5210:         case PPC_59_FMULS:
 5211:             ic->f = instr(fmuls); rc_f = instr(fmuls_dot);
 5212:             ic->arg[0] = (size_t)(&cpu->cd.ppc.fpr[rt]);
 5213:             ic->arg[1] = (size_t)(&cpu->cd.ppc.fpr[ra]);
 5214:             ic->arg[2] = (size_t)(&cpu->cd.ppc.fpr[rs]); /* frc */
 5215:             break;
 5216:         default:/*  Use all 10 bits of xo:  */
 5217:             switch (xo) {
 5218:             default:goto bad;
 5219:             }
 5220:         }
 5221:         /*  #326: apply the record form, guarded.  */
 5222:         if (rc) {
 5223:             if (rc_f == NULL)
 5224:                 goto bad;
 5225:             ic->f = rc_f;
 5226:         }
```

`src/include/opcodes_ppc.h` at `db8b1a33` defines `PPC_59_FDIVS 18`, `PPC_59_FSUBS 20`, `PPC_59_FADDS 21`,
`PPC_59_FMULS 25`, `PPC_59_FMADDS 29` -- and no opcode-59 constant for 28, 30 or 31.

**What is ALREADY RECORDED, and it bears on the grade** -- `OUTSTANDING_BUGS.md` at `db8b1a33`, quoted verbatim:

```
 1705: > - **Twelve encodings still halt, deliberately, and gate 15 asserts that they do.** Split
 1706: >   by reason, because the reasons are not the same:
 1707: >   - `fctid`, `fctidz`, `fcfid`, `fsqrt`, `fsqrts` — **64-bit-only, or outside the G4's
 1708: >     instruction groups.** On a 32-bit G4 real silicon raises a program interrupt, so
 1709: >     implementing them unconditionally would make the model *less* faithful. These ride
 1710: >     on the missing exception model, not on decode work.
 1711: >   - `fres`, `frsqrte` — estimate instructions, accuracy implementation-defined.
 1712: >   - `fcmpo`, `fnmadd`, `fnmsub`, `fmadds`, `fmsubs` — **no technical blocker.** A few
 1713: >     dozen lines each at the fidelity bar already shipped (`fadds` and `fmuls` are
 1714: >     aliases of their double forms today). Out of #326 for round size alone. Do
 1715: >     `fmadds` first: gcc emits it for ordinary `float` arithmetic, so it is likely the
 1716: >     most frequently executed instruction still in this set.
```

(`fnmadd` and `fnmsub`, the DOUBLE forms, were decoded later by round #344; the rest of that list stands.)

Premises, as questions:
* Is stopping the CPU on these words a DEFECT, or the recorded policy working as designed?  The record calls the
  stop deliberate and says a test asserts it; the reviewers graded it HIGH by the "stops it making progress" clause.
  Both can be true.  Which should the queue show?
* The record says gcc emits `fmadds` for ordinary `float` arithmetic.  If so this is the finding an ordinary guest
  program is most likely to meet.  Do you know that to be true of the compilers these guests were built with, or
  is it a plausible claim nobody measured?

## H3 -- PowerPC: `lwarx`/`stwcx.` with the wrong record bit ends the process

**The finding, as ruled:** the decoder selects the load-and-reserve / store-conditional handler from the extended
opcode alone; the record bit (bit 0 of the word) is not part of the key.  The handler then calls `exit(1)` when a
load form has the bit set, or a store form has it clear.  Both are invalid forms of the instruction.  Round #216
removed the two memory-fault exits from this same function and left these two.  Graded HIGH, new.

`src/cpus/cpu_ppc_instr.c`, lines 4613-4615 at `db8b1a33`:

```
 4613:     case PPC_HI6_31:
 4614:         xo = (iword >> 1) & 1023;
 4615:         switch (xo) {
```

`src/cpus/cpu_ppc_instr.c`, lines 4866-4872 at `db8b1a33`:

```
 4866:         case PPC_31_LWARX:
 4867:         case PPC_31_LDARX:
 4868:         case PPC_31_STWCX_DOT:
 4869:         case PPC_31_STDCX_DOT:
 4870:             ic->arg[0] = iword;
 4871:             ic->f = instr(llsc);
 4872:             break;
```

`src/cpus/cpu_ppc_instr.c`, lines 2276-2335 at `db8b1a33`:

```
 2276: X(llsc)
 2277: {
 2278:     int iw = ic->arg[0], len = 4, load = 0, xo = (iw >> 1) & 1023;
 2279:     int i, rc = iw & 1, rt, ra, rb;
 2280:     uint64_t addr = 0, value;
 2281:     unsigned char d[8];
 2282: 
 2283:     switch (xo) {
 2284:     case PPC_31_LDARX:
 2285:         len = 8;
 2286:         // fall through
 2287:     case PPC_31_LWARX:
 2288:         load = 1;
 2289:         break;
 2290:     case PPC_31_STDCX_DOT:
 2291:         len = 8;
 2292:     case PPC_31_STWCX_DOT:
 2293:         break;
 2294:     }
 2295: 
 2296:     rt = (iw >> 21) & 31;
 2297:     ra = (iw >> 16) & 31;
 2298:     rb = (iw >> 11) & 31;
 2299: 
 2300:     if (ra != 0)
 2301:         addr = cpu->cd.ppc.gpr[ra];
 2302:     addr += cpu->cd.ppc.gpr[rb];
 2303: 
 2304:     if (load) {
 2305:         if (rc) {
 2306:             fatal("ll: rc-bit set?\n");
 2307:             exit(1);
 2308:         }
 2309:         if (cpu->memory_rw(cpu, cpu->mem, addr, d, len,
 2310:             MEM_READ, CACHE_DATA) != MEMORY_ACCESS_OK) {
 2311:             /*  #216: (Codex/Fable) memory_rw() raised a DSI on the
 2312:                 faulting lwarx address; let it proceed instead of
 2313:                 exit()ing the host.  */
 2314:             return;
 2315:         }
 2316: 
 2317:         value = 0;
 2318:         for (i=0; i<len; i++) {
 2319:             value <<= 8;
 2320:             if (cpu->byte_order == EMUL_BIG_ENDIAN)
 2321:                 value |= d[i];
 2322:             else
 2323:                 value |= d[len - 1 - i];
 2324:         }
 2325: 
 2326:         cpu->cd.ppc.gpr[rt] = value;
 2327:         cpu->cd.ppc.ll_addr = addr;
 2328:         cpu->cd.ppc.ll_bit = 1;
 2329:     } else {
 2330:         uint32_t old_so = cpu->cd.ppc.spr[SPR_XER] & PPC_XER_SO;
 2331:         if (!rc) {
 2332:             fatal("sc: rc-bit not set?\n");
 2333:             exit(1);
 2334:         }
 2335: 
```

Premises, as questions:
* `xo = (iword >> 1) & 1023` drops bit 0.  So do `lwarx` with Rc = 1 and `stwcx` with Rc = 0 both reach `X(llsc)`?
* These instructions are unprivileged.  Does that make this reachable from the guest's USER state -- one word in an
  ordinary user program ends the emulator?
* For an invalid instruction form the architecture leaves the result boundedly undefined or raises a program
  interrupt, depending on the implementation.  Which would you model, and does the fork deliver PowerPC program
  interrupts today (`ppc_exception()` exists in `cpu_ppc.c`)?

## THE QUESTIONS (please answer all; they are short)

Q1. **The premise audit.**  For each of H1, H2 and H3: is the path reachable from code running in the guest, as the
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
