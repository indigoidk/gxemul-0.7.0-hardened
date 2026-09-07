# PASS-2 REVIEW BRIEF -- `m88kexcdeliver` (HIGH): the diff that makes the MC88100 model DELIVER seven trap-like exception classes instead of stopping the emulation.  Tree `GXEMUL-SEC/src/`, HEAD `83df95c` + the UNCOMMITTED diff below.  2026-09-05, ~21:30 (the diff is unchanged since 16:16; the detector gained the `errortb` row at 21:05).

## CONTEXT AND VOCABULARY
An ordinary correctness review of an open-source machine emulator's CPU model (GXemul 0.7.0, hardened fork).  The "guest" is
the operating system running inside the emulator.  Plain engineering vocabulary: "the emulation stops", "the exception is
delivered to the guest's handler".  Read the project's own records NARROWLY (grep anchors, a few lines of context; never whole
CHANGELOG blocks or the ledger) and paraphrase in neutral terms.

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY
A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly.  **Check the premises, not just the
derivations.**  Where I state something as fact, ask whether it is true.  **THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.**  Three
pristine-2021-upstream copies of GXemul sit under the project root (`./src/` and two under `_archive/`); they are NOT this fork.
**If you cannot read files that is expected** -- every fact you need is inlined.  Name any premise you cannot settle rather than
guessing.  **ENUMERATE arithmetic** (vector offsets, encodings, register values) rather than reasoning about it.  **VERDICT LINE
FIRST.**  Cite by grep anchor, not line number.

## 1. SETTLED PREMISES, RE-INLINED (each is a QUESTION if you can check it)
Settled by pass 1 (`_scratchpad/panel_20260905_143211/`, Opus measuring seat in `/tmp/gxopus_m88kexc`, logs preserved under
`_scratchpad/m88kexc/opus_logs/`):
* **Two sites in one function.**  `m88k_exception()` marks four vectors `implemented` in its first switch; a fallback stops EVERY
  guest CPU for any unimplemented vector < 128; the common path then sets EPSR/PSR/SXIP/SNIP/SFIP and `pc = VBR + 8*vector`; a
  TAIL switch's `default:` stops THIS cpu.  MEASURED: the one-site form (`implemented = true` alone) halts at the tail default
  with pc/SXIP/PSR already correct; only the machine-still-running bit distinguishes it from delivery.
* **The contract** (MC88100 UM, `_scratchpad/mc88100.txt`): rte resumes at SNIP, never SXIP (`:8983-8985`); SXIP = the faulting
  instruction; the destination register (and carry bit) unchanged -- 6.5.2 (`:9231-9240`), 6.5.3 (`:9248-9255`), 6.5.4
  (`:9257-9269`), 6.6 (`:9305-9308`), 6.8.3 (`:10300-10305`).  The common path's defaults (SNIP = pc+4 | V) are that contract.
* **Reachability.**  Literal-constant raise sites: PRIVILEGE 10, ILLEGAL_INTEGER_DIVIDE 4, INTEGER_OVERFLOW 3, MISALIGNED 1,
  UNIMPLEMENTED_OPCODE 1, SFU1_PRECISE 58.  BUT `tb0/tb1/tcnd` raise `m88k_exception(cpu, ic->arg[2], 1)` with a 9-bit
  guest-chosen vector, unfiltered in supervisor mode -- so BOUNDS_CHECK (7) IS reachable (MEASURED: supervisor `tb1 0,r3,7`
  halts HEAD), and so is every vector < 128.  ERROR (10) is reached by the SFRZ re-route when a handler faults (MEASURED on the
  five-class form: `internal error`, machine stopped).  Vector 0 named by a trap dies in the tail RESET arm (filed separately).
* **Reset PSR** = MODE|IND = 0x80000002 (SFD1 clear).  `X(divu)` tests SFD1 BEFORE the zero divisor, so INSIDE a handler (SFD1
  set by the common path) a divu raises SFU1_PRECISE, not vector 8 -- row m88kexcsfu1, out of scope here.
* **The house idiom is D1.**  `sh_exception()` has the same shape and #217/#315/#457 fixed it by adding bare `case ... break`
  arms; MIPS/PPC/ARM cores deliver everything they recognise.  Nine pass-1 seats' worth of option-set search found one unnamed
  member: D4 = make the tail `default:` deliver everything (filed `m88kexctaildefault`, not adopted: bigger blast radius).
* **Message level INFO**: no hygiene row keys on these lines (checked: `grep exception regress/gate_hygiene.sh` -> one unrelated
  comment); `#261`'s break-on-ERROR is opt-in.  The level change is DISCLOSED as unobservable (M_LEVEL).
* **Pass-1 roster** (record, not agreement): answered -- Opus 5 (measured), kimi 3 (282 KB), grok 4.6, deepseek, minimax
  (packet-fed, conditioned answers).  SEAT FAILURES -- codex GPT-6 Astra REFUSED twice (content filter; 466 KB reasoning stream
  then the refusal, then a 0-byte second attempt); glm-5.3 thinking BURN (0-byte response, 117 KB thinking; a mini packet
  re-fire then answered); Fable 5.1 WALLED (session limit, reset 4pm) -- re-fired at this pass.  agy DELIBERATELY NOT FIRED.

## 2. THE DIFF (uncommitted; `git -C GXEMUL-SEC diff -- src/cpus/cpu_m88k.c`, 47+ 12-), VERBATIM
```diff
@@ -716,31 +716,38 @@ void m88k_exception(struct cpu *cpu, int vector, int is_trap)
 	case M88K_EXCEPTION_MISALIGNED_ACCESS:
-		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "MISALIGNED_ACCESS", VERBOSITY_ERROR, "");
+		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "MISALIGNED_ACCESS", VERBOSITY_INFO, "");
+		implemented = true;	/*  m88kexcdeliver  */
 		break;
     ... the SAME two-line change at UNIMPLEMENTED_OPCODE, PRIVILEGE_VIOLATION, BOUNDS_CHECK_VIOLATION,
         ILLEGAL_INTEGER_DIVIDE, INTEGER_OVERFLOW and ERROR (seven arms; SFU1_PRECISE/IMPRECISE untouched) ...
@@ -772,6 +779,18 @@
+	/*
+	 *  m88kexcdeliver (2026-09-05): the seven trap-like classes above are
+	 *  DELIVERED (VBR + 8*vector, SXIP = the faulting instruction, SNIP = the
+	 *  next one, destination register unchanged -- MC88100 UM 6.4.3/6.5/6.6/
+	 *  6.8.3), like the four this fallback never covered.  Before, any of them
+	 *  stopped EVERY guest CPU here: one user-mode divu by zero ended the
+	 *  emulation.  Pre-existing upstream code, surfaced by the 2026-09-05
+	 *  retrospective of #380.  What still lands here: SFU1_PRECISE/IMPRECISE
+	 *  (row m88kexcsfu1 -- they need the FP exception registers the fork does
+	 *  not write) and vectors 11..113/116..127, which nothing raises by name
+	 *  but a supervisor tb0/tb1/tcnd can name directly (row m88kexctaildefault).
+	 */
 	if (vector < M88K_EXCEPTION_USER_TRAPS_START && !implemented) {
@@ -896,13 +915,29 @@
-#if 0
+		case M88K_EXCEPTION_MISALIGNED_ACCESS:
+		case M88K_EXCEPTION_UNIMPLEMENTED_OPCODE:
+		case M88K_EXCEPTION_PRIVILEGE_VIOLATION:
+		case M88K_EXCEPTION_BOUNDS_CHECK_VIOLATION:
 		case M88K_EXCEPTION_ILLEGAL_INTEGER_DIVIDE:
-			/*  TODO: Is it correct to continue on the instruction
-			    _after_ the division by zero? Or should the PC
-			    be backed up one step?  */
+		case M88K_EXCEPTION_INTEGER_OVERFLOW:
+		case M88K_EXCEPTION_ERROR:
+			/*  m88kexcdeliver: the common path above is already the
+			    architectural contract for these -- SXIP = the faulting
+			    instruction, SNIP = the next one, and rte resumes at SNIP
+			    (UM 6.4.3.1.4: "the processor hardware does not use the
+			    SXIP on return from an exception"), so the upstream doubt
+			    that sat here in an #if 0 ("should the PC be backed up one
+			    step?") is answered NO: 6.8.3 and 6.6 say the destination
+			    register (and carry bit) are unchanged and a handler that
+			    wants re-execution copies SXIP into SNIP itself.  Without
+			    these labels the classes reached the default: below, which
+			    stops the cpu -- the one-site fix was measured to do exactly
+			    that.  ERROR arrives here from the SFRZ re-route above with
+			    the shadows deliberately frozen (update_shadow_regs false).
+			    Not modelled, disclosed: the scoreboard bit (SSBR stays 0)
+			    and fcr2/fcr4/fcr5 for the divide.  */
 			break;
-#endif
```
The tail's `default:` (`internal error`, `cpu->running = false`) and the fallback are UNCHANGED.  The `#if 0` SFU1 block below
the new arms is unchanged.  A file-reading seat: `git -C GXEMUL-SEC diff -- src/cpus/cpu_m88k.c` shows the whole thing.

## 3. THE DETECTOR (v2, `_scratchpad/m88kexc/m88k_exc_probe.py`; ships as `regress/m88k_exc_probe.py` in gate 11)
Ten fault rows (nine + `errortb`, below) + two controls + a parse self-test, each a one-instruction program at 0x10000 after a liveness marker
(`addu r9,r0,r10`), a `br .` planted at every vector entry, `breakpoint add <8*vector>`, `continue`, then `reg` / `reg 0,0`:
    div0 (divu r2,r3,r0, f4436800 -> 0x40) | ovf (add r2,r3,r4 7fffffff+1 -> 0x48) | misalign (ld r2,r3,0 odd -> 0x20) |
    bounds (supervisor tb1 0,r3,7 f003d807 -> 0x38) | priv (stcr r3,cr1 80038023 clearing MODE, then ldcr r2,cr1 80404020 -> 0x30) |
    privtb (stcr then user-mode tb1 0,r4,8 f004d808 -> 0x30) | unimpl (stcr then prom_call f400fc92 -> 0x28) |
    error (div0 whose handler at 0x40 is a misaligned ld: 2nd fault, SFRZ set, re-route -> 0x50) |
    dslot (br.n +8 c4000002 with divu in its delay slot -> 0x40; the else-arm: SNIP = pc+4, SFIP = delay_target) |
    live (divu r2,r3,r4 = 0x60/0x10 -> r2 = 6) | attrib (same instruction, r3 = r4 = 0x10 -> r2 = 1) | selftest (PSR at reset == 0x80000002)
DELIVER requires ALL of: not stopped; pc == 8*vector; SXIP == fault_pc|2; SNIP == fault_pc+4|2 (dslot: slot_pc+4|2); SFIP ==
SNIP+4 (dslot: delay_target|2); PSR == 0x8000000b; EPSR == 0x80000002 (supervisor rows) / 0x00000002 (user-mode rows);
r2 == 0xdeadbeef.  The stop channel is tested BEFORE pc (the naive form sets pc = entry and then stops).  Other words:
HALT (`unimplemented vector=` + stopped), TAILHALT (`internal error` + stopped), STOP, BADREGS (+ the failing fields), NOSTART.

MEASURED, same script: HEAD 83df95c build/gxemul 14:54 -> **0/9** (all nine HALT; controls DONE; selftest OK)  [probe2_head.out]
                       fix build/gxemul 16:16:27          -> **9/9** DELIVER, every assert holding; controls DONE  [probe2_fix.out]
    fix values: div0 pc=0x40 sxip=0x10006 snip=0x1000a sfip=0x1000e psr=0x8000000b epsr=0x80000002 r2=0xdeadbeef
                priv pc=0x30 sxip=0x1000a snip=0x1000e sfip=0x10012 psr=0x8000000b epsr=0x00000002
                error pc=0x50 sxip=0x10006 snip=0x1000a sfip=0x1000e (frozen at the first fault) epsr=0x80000002
                dslot pc=0x40 sxip=0x1000a snip=0x1000e sfip=0x1000e (delay_target 0x1000c|2)
KILL TABLE 1, MEASURED (scratch clone of the fix build; frozen probe; `PRETABLE_m88kexc.out` written first; logs
`_scratchpad/m88kexc/killtable/`; BASE 9/9 before and after):
    M_REVERT (all seven back to the fallback)   0/9  killed (every row HALT)
    M_REVERT1 (BOUNDS_CHECK only)               8/9  killed (bounds row HALT)
    M_NAIVE (tail labels dropped)               0/9  killed (every row TAILHALT)
    M_VEC4 (+4*vector)                          0/9  killed (STOP)
    M_NOSHADOW / M_NOSFRZ / M_NOEPSR            0/9  killed (BADREGS: sxip / psr / epsr)
    M_SNIPX (SNIP = pc)                         1/9  killed (dslot survives BY DESIGN: its SNIP comes from the delay-slot arm)
    M_NOMODE (MODE dropped from the PSR write)  6/9  killed by exactly the three user-mode rows (supervisor rows cannot see it)
    M_TAILRETURN (break -> return)              0/9  killed (grok's mutant)
    M_DSLOT (else-arm SFIP wrong)               8/9  killed (dslot row)
    M_LEVEL (INFO -> ERROR)                     9/9  SURVIVED -- disclosed (no row can observe the level)
    ** M_ERRORDROP (ERROR's implemented=true dropped in switch 1)  9/9  ESCAPED **
THE ESCAPE, and its repair (L1, pre-ship construction): the `error` row reaches vector 10 through the SFRZ re-route, which runs
AFTER switch 1 -- so switch 1's ERROR arm is reachable ONLY by a trap instruction naming vector 10 directly.  Row `errortb`
(supervisor `tb1 0,r3,10` = f003d80a -> 0x50, normal unfrozen shadows) was added; a second mutant M_ERRORTAIL (drop ONLY the
ERROR tail label) was added to prove the `error` row pins the tail arm.  TABLE 2, MEASURED (`_scratchpad/m88kexc/killtable2/`, same clone, baseline rebuilt,
frozen probe md5 556aa357): BASE 10/10 before and after; M_ERRORDROP 9/10 (errortb HALT); M_ERRORTAIL 8/10 (error AND errortb
TAILHALT -- so the `error` row does pin the tail arm); M_REVERT1 9/10 (bounds HALT).  The table-1 escape is closed; clone clean.  QUESTION: is there any OTHER route
into switch 1's ERROR arm than a trap naming 10?  (`grep -n 'M88K_EXCEPTION_ERROR' src/cpus/*.c`: the re-route and the switch
cases only.)

## 4. THE F2 PACKET -- pass-1 findings, numbered, with the main loop's DISPOSITION on each (say which disposition is WRONG)
F1 (Opus, MEASURED) four value channels printed but not asserted -> ACCEPTED: v2 asserts SXIP/SNIP/SFIP/PSR/EPSR/r2.
F2 (Opus, MEASURED) M_NOMODE equivalent on supervisor rows -> ACCEPTED: three user-mode rows (EPSR MODE clear vs PSR MODE set).
F3 (Opus, MEASURED) BOUNDS_CHECK and ERROR reachable; include both -> ACCEPTED (seven classes).  Grok: "leave BOUNDS unimplemented,
   file ERROR" -> REJECTED by the measurement (both reached today; the SH precedent groups by architectural category).  D1.
F4 (Opus) tail RESET arm dies on a trap naming vector 0 -> FILED `m88kexcresetkill` (upstream; separate fix design).
F5 (Opus, kimi F4) `stcr` with MXM set stops the machine; the template never rounds down -> FILED `m88kmxmkill`.
F6 (Opus) D4 tail-default-delivers -> FILED `m88kexctaildefault` (named, not adopted).  glm: demote stop-all to stop-this-CPU for
   the residual 119 vectors -> folded into that row.
F7 (grok) M_TAILRETURN (break -> return skips m88k_pc_to_pointers) -> ACCEPTED as a table mutant (measuring).
F8 (grok) `br .` = c0000000, not c3ffffff (that was `br -1` = a two-instruction loop) -> ACCEPTED: v2 uses c0000000.
F9 (grok, kimi C1, Opus) "opcode 0x15" -> major opcode 5 -> ACCEPTED (docstring).
F10 (kimi C6) the v1 witness artefact had sxip=None psr=None: the CR parse used `reg 0,1` (the FP set) -> ACCEPTED: v2 uses `reg 0,0`
   + a parse self-test row; the artefact was re-captured (probe2_head.out).
F11 (kimi F1-F3, F5, F6) register-form sub/add.co undecoded (`goto bad` halt); tbnd undecoded; fxcr undecoded; X(div) does not
   raise on negative operands; m88k_ldcr stops the cpu on unimplemented CRs -> FILED as LOW rows (`m88ksubco`, `m88ktbnd`,
   `m88kfxcr`, `m88kdivneg`, `m88kldcrhalt`); none in this diff's function.
F12 (minimax) 6.6 not cited for INTEGER_OVERFLOW -> RESOLVED: `:9305-9308` quoted above (destination and carry unchanged).
F13 (minimax) is_trap at the raise sites -> CHECKED: all five literal-constant classes pass 0; the trap instructions pass 1.
F14 (glm mini) the carry bit is a second unasserted destination -> the exact PSR compare pins bit 28; ACCEPTED as covered.
F15 (glm mini) ERROR row: do the shadows update on the error exception? -> the fork freezes them (update_shadow_regs false when
   SFRZ set); the row asserts the frozen values; the manual's Figure 6-4 flow shows SFRZ=1 -> ERROR with no shadow update.
   CHECK this against `mc88100.txt` if you can (grep `ERROR EXCEPTION`).
F16 (deepseek) SNIP not in the row list -> ACCEPTED (v2 asserts SNIP).
D1 (disagreement) grok vs Opus on BOUNDS/ERROR inclusion -> ruled for Opus by measurement; the dissent is recorded.

## 5. QUESTIONS (VERDICT LINE FIRST)
1. **IS THE DIFF RIGHT?**  Every hunk; the seven; INFO; the comments' claims (each sentence asserting an observable maps to a row --
   say which does not).  Is anything in the tail arm's comment FALSE?  Is the fallback comment's residual list right (11..113,
   116..127)?
2. **THE SMALLEST EDIT that breaks this diff and still passes the 11-row probe.**  Name the row you expect to stay green.  The main
   loop expects M_LEVEL to survive (disclosed); what else?
3. **WHICH OF THE SIXTEEN DISPOSITIONS ABOVE IS WRONG?**  The count is named: sixteen accepted/resolved/filed, one rejected.  A round
   that accepted everything has either had a very good panel or stopped arguing.
4. **WHAT DID ALL OF US MISS?**  You now have the whole pass-1 panel's output.
5. **RECORDS.**  What the CHANGELOG block, the queue file and the ledger owe (provenance: upstream code, surfaced by the batch-2
   retrospective of #380; the split from m88kexcsfu1; the census correction -- the literal deriver is blind to computed vectors; the
   8-of-128 figure; the seat failures by name).

If, while verifying a claim, you found something ELSE -- say so.  agy is DELIBERATELY NOT FIRED (reserved for measurement).
