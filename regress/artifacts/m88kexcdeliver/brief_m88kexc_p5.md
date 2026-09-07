# PASS 5 -- `m88kexcdeliver` (#502): the closing pass on the PASS-4 REPAIR (probe v5, 29 fault rows).  Tree `GXEMUL-SEC/src/`, HEAD `83df95c` + the uncommitted round.  2026-09-06, ~09:20.  SHORT BY DESIGN: one diff, one table, one question.

## CONTEXT AND VOCABULARY
An ordinary correctness review of an open-source machine emulator's CPU model (GXemul 0.7.0, hardened fork): the MC88100
exception-delivery path in `cpu_m88k.c` and its detector `regress/m88k_exc_probe.py`.  The "guest" is the operating system
inside the emulator.  Plain engineering vocabulary.  **If you cannot read files that is expected -- every fact is inlined; name
any premise you cannot settle rather than guessing.**  Tree under review: `GXEMUL-SEC/src/` (three pristine-2021 copies under the
project root are NOT this fork).  **VERDICT LINE FIRST.**  Cite by grep anchor.  `python3` in git-bash is a Windows Store stub;
a file-reading seat that needs Python uses `C:\Users\User00\AppData\Local\Programs\Python\Python312\python.exe`.

## WHY A FIFTH PASS
The repair-chain rule: a repair made in response to a pass owes its own pass, scoped to THAT diff, and the chain closes on the first
VALID pass that finds zero floor breaches surviving adjudication, with the denominator stated.  **Pass 4 did not close**: six of
eight fired seats said CLOSE, but the two measuring/flagship seats each built a REAL 23/23 sweep on v4 -- Opus: `M_OVFSUPONLY`
(`implemented = (PSR & MODE) != 0` at the OVERFLOW arm; a user-mode overflow ended the emulation again and no row noticed);
Opus and Fable: `M_SFRZMIS` (`if (!is_trap)` -> `if (!is_trap && vector == MISALIGNED)` on the SFRZ re-route; `error` was the
only frozen non-trap row).  Fable graded the second an L2 floor breach ({SFRZ set, non-trap} x {class} is a body-tested joint
cell of two predicates dominating the diff's tail labels) and the first clause-(e) debt; Opus the reverse.  **Both CLASSES were
closed in ONE diff** per the repair-chain amendment (two consecutive passes finding one class -> close the class, not the cell).
minimax's ONE MORE rested on SFD1 being bit 1: `m88k_psl.h` defines `M88K_PSR_SFD1 0x00000008` (bit 3), so that reading is
answered by the tree.  agy DELIBERATELY NOT FIRED (reserved for measurement).

## SETTLED PREMISES, RE-INLINED (each a QUESTION if you can check it)
1. `m88k_psl.h`: MODE 0x80000000, SFD1 0x00000008, MXM 0x00000004, IND 0x00000002, SFRZ 0x00000001.  Reset PSR 0x80000002.
2. The exception path's PSR write is ONE site, an OR-in: `m88k_stcr(cpu, cpu->cd.m88k.cr[M88K_CR_PSR] | SFRZ | IND | SFD1 | MODE, ...)`
   -> post-exception PSR 0x8000000b from every pre-fault value in the table (0x9000000b for ovfc).  EPSR is written only on the
   unfrozen path (a frozen second fault keeps the first fault's EPSR; the rows expect 0x80000002 there).
3. Order inside `m88k_exception()`: switch 1 (class -> `implemented`, INFO diagnostic); the FALLBACK (`vector < 128 &&
   !implemented` -> `unimplemented ... vector=0x%03x` + every cpu stopped); THEN the SFRZ re-route (`if (PSR & SFRZ) { if (!is_trap)
   { vector = ERROR; } update_shadow_regs = false; }`); then the common path (EPSR/PSR/shadows/pc = VBR + 8*vector); then the tail switch.
4. `m88k_stcr` case PSR: stores the value verbatim (MODE-clear by stcr prints a WARNING and continues; MXM set stops the cpu; a
   byte-order flip stops the cpu).  So a handler may write SFRZ=1 / SFD1=0 / MODE=0 itself.
5. `divu`/`divu_imm`/`mulu`...: `if (PSR & SFD1) -> SFU1_PRECISE` is tested BEFORE `divisor == 0 -> ILLEGAL_INTEGER_DIVIDE`
   (`cpu_m88k_instr.c` anchor `M88K_FPECR_FUNIMP`).  `prom_call` raises UNIMPLEMENTED_OPCODE only when MODE is clear (anchor
   `If executed from user mode, then cause an exception`).  `X(tb0)`/tb1: a user-mode trap naming a vector < 128 raises PRIVILEGE.
6. `All machines stopped.` (emul.c) is the ONLY stop emission; the probe's `stopped` is that substring and `halted` = fallback
   diagnostic AND stopped AND (for the two expected-HALT rows) the named vector.
7. The probe program: MARK, the row's words, then `br .` at CODE=0x10000; every vector entry holds `br .`; the row's handler words are
   planted at 0x40 (the DIV0 entry) followed by `br .`; breakpoint at the expected entry; `continue`; 6 s grace.

## THE REPAIR DIFF, VERBATIM (`regress/m88k_exc_probe.py` v4 -> v5; frozen table copy md5 c83b1f38, shipped md5 96ab47a0 -- the
## shipped file differs from the frozen copy by the five docstring lines shown after the diff)
```diff
--- GXEMUL-SEC/regress/artifacts/m88kexcdeliver/killtable4/m88k_exc_probe.frozen4.py	2026-09-06 08:20:13.915977600 -0500
+++ GXEMUL-SEC/regress/m88k_exc_probe.py	2026-09-06 08:59:28.459997100 -0500
@@ -29,8 +29,9 @@
   dslot      br.n +16 (c4000004) with divu r2,r3,r0 in its delay slot -> the else-arm of the
              delay-slot branch (SNIP = pc+4 = 0x1000c, SFIP = delay_target = 0x10014 -- two
              DIFFERENT numbers; with br.n +8 both were 0x1000e and the SFIP channel was vacuous)  ILLEGAL_INTEGER_DIVIDE 0x40
-             *** THIS ROW PINS THE ELSE-ARM AS IMPLEMENTED, NOT AS THE MANUAL'S CONTRACT.  Table 6-3 (shadows copy
-             XIP/NIP/FIP: for a fault in the delay slot of a taken br.n, NIP = target, FIP = target+4) and X(rte)'s
+             *** THIS ROW PINS THE ELSE-ARM AS IMPLEMENTED, NOT AS THE MANUAL'S CONTRACT.  Table 6-3 (the shadows copy
+             XIP/NIP/FIP) with the pointer definitions at UM 6.2 (mc88100.txt:2093-2104: FIP is the taken branch's
+             target while the branch executes, so for a fault in its delay slot NIP = target, FIP = target+4) and X(rte)'s
              `fip != nip + 4' arm say the else-arm returns WRONG (codex, grok, pass 2: the fallthrough executes
              before the target).  Pre-existing, out of this diff's scope, filed as m88kdslotshadow; when that round
              lands this row is RE-PINNED FIRST (oracle-correction rule: re-pin, measure HEAD red, then fix). ***
@@ -57,7 +58,7 @@
   sfu1h      div0 whose handler at 0x40 is a LEGAL divu r6,r5,r4: with SFD1 set the divide raises
              SFU1_PRECISE (114), which halts at the FALLBACK (it runs before the SFRZ re-route).  EXPECTED
              RESULT = HALT naming vector 0x072, with pc == 0x40 (the first delivery happened -- on HEAD the
-             first divu halts and this row reads BADREGS stage1).  With the fallback off (M_DELIVERALL) the
+             first divu halts on vector 0x008, not this row's 0x072, and it reads STOP).  With the fallback off (M_DELIVERALL) the
              nested SFU1 is RE-ROUTED TO ERROR (0x50), not delivered to 0x390: the row reds as STOP.  So it
              pins 'SFU1 inside a handler still halts', NOT 'SFU1 is not delivered to its vector' -- the
              first-exception SFU1 route is row m88kexcsfu1's (grok, kimi, pass 3)                    (0x390)
@@ -67,6 +68,19 @@
   indclr     stcr r5,cr1 (r5=0x80000000: MODE only, IND CLEAR) then add 7fffffff+1: the exception path must
              SET IND (PSR 0x8000000b from 0x80000000; EPSR 0x80000000).  Every other row's pre-fault PSR already
              has IND, so `| M88K_PSR_IND' was unobservable -- the carry shape again (grok, codex, pass 3)     0x48
+  umisalign  stcr r5,cr1 (r5=0x2: user mode) then ld r2,r3,0 with r3 odd: MISALIGNED from USER mode
+             (a MODE-conditioned `implemented' on that arm swept 23/23 -- Opus, pass 4)                    0x20
+  uovf       stcr r5,cr1 (user mode) then add 7fffffff+1: OVERFLOW from USER mode -- the measured
+             M_OVFSUPONLY escape (a user-mode overflow ended the emulation again, 23/23)               0x48
+  errovf     div0 whose handler at 0x40 is add 7fffffff+1: a NON-TRAP fault of a SECOND class with
+             SFRZ set -> re-routed to ERROR with frozen shadows (M_SFRZMIS -- `!is_trap && vector ==
+             MISALIGNED' on the re-route -- swept 23/23 because `error' was that cell's only row)      0x50
+  errdiv0    div0 whose handler is stcr r5,cr1 (r5=0x80000003: SFD1 CLEAR, SFRZ kept) then divu by zero:
+             a frozen non-trap DIV0 -> ERROR (with SFD1 set the same divu raises SFU1 instead: sfu1h)     0x50
+  errpriv    div0 whose handler is stcr r5,cr1 (r5=0x00000003: USER mode, SFRZ kept) then ldcr: a frozen
+             non-trap PRIVILEGE -> ERROR (Fable, pass 4: the {SFRZ, !is_trap} x {class} closure)        0x50
+  errunimpl  div0 whose handler is stcr r5,cr1 (user mode, SFRZ kept) then prom_call: a frozen non-trap
+             UNIMPLEMENTED -> ERROR.  BOUNDS and ERROR have no non-trap route (trapfrozen covers the trap)  0x50
   ovfc       stcr r5,cr1 (80058025, r5=0x90000002: C set) then add 7fffffff+1: the carry bit must
              SURVIVE the exception path (UM 6.6) -> PSR 0x9000000b, EPSR 0x90000002.  Every other
              row's pre-fault C is 0, so PSR == 0x8000000b pinned 'C not set', never 'C unchanged'  0x48
@@ -100,7 +114,13 @@
 cleared carry (ovfc); a dropped IND (indclr); the debugmsg LEVEL regression to ERROR/WARNING (bad=level on any
 delivered row: those print at the post-startup WARNING floor, INFO and DEBUG do not -- so exact INFO is NOT pinned,
 only 'not ERROR/WARNING' -- M_LEVEL; codex, pass 3); a skipped EPSR save; a skipped supervisor switch (the user-mode rows: EPSR MODE
-clear vs PSR MODE set); a wrong return address; the delay-slot else-arm's SFIP source (dslot, +16
+clear vs PSR MODE set); a MODE-conditioned `implemented' on any class that user mode can raise ({class} x
+{MODE} closure: DIV0 udiv0, PRIVILEGE priv/privtb, UNIMPLEMENTED unimpl, MISALIGNED umisalign, OVERFLOW uovf;
+BOUNDS and ERROR have no user-mode route -- a user tb1 naming them raises PRIVILEGE, and every handler runs
+supervisor); a class-conditioned SFRZ re-route ({SFRZ set, !is_trap} x {class}: MISALIGNED error, OVERFLOW errovf,
+DIV0 errdiv0 -- the handler clears SFD1 first, with it set the divu raises SFU1 instead (sfu1h) --, PRIVILEGE errpriv
+and UNIMPLEMENTED errunimpl -- the handler drops to user mode keeping SFRZ; BOUNDS and ERROR have no non-trap route,
+the frozen TRAP is trapfrozen); a wrong return address; the delay-slot else-arm's SFIP source (dslot, +16
 geometry); a trap re-routed to ERROR while frozen (trapfrozen); a written destination.  Does NOT catch:
 fcr2/fcr4/fcr5; scoreboard (SSBR) bits; DMT contents; the post-delivery
 `cpu->delay_slot' write on the NON-delay path (M_DELAYALWAYS: needs a second UNFROZEN exception -- filed);
@@ -117,6 +137,8 @@
 PSR_RESET = 0x80000002          # MODE | IND (cpu_m88k.c: cr[PSR] = M88K_PSR_MODE | M88K_PSR_IND)
 PSR_EXC = 0x8000000b            # MODE | SFD1 | IND | SFRZ after the common path
 PSR_USER = 0x00000002           # IND only: what the user-mode rows write via stcr
+PSR_FRZSUP = 0x80000003         # MODE | IND | SFRZ, SFD1 CLEAR: a frozen handler that wants its divu to raise DIV0, not SFU1
+PSR_FRZUSER = 0x00000003        # IND | SFRZ, MODE CLEAR: a frozen handler dropping to user mode (PRIVILEGE / UNIMPLEMENTED routes)
 
 def tri(sub, d, s1, s2):
     return 0xf4000000 | (d << 21) | (s1 << 16) | (sub << 8) | s2
@@ -184,6 +206,16 @@
                  [TB1_0_R3_7]),                               # handler at 0x40: tb1 0,r3,7 with SFRZ set -> a TRAP is not re-routed to ERROR
     ("ovfc",     [STCR_R5_CR1, ADD_R2_R3_R4],   {"r3": 0x7fffffff, "r4": 1, "r5": PSR_CARRY}, V_OVF, 0x10008, PSR_CARRY, None),
     ("indclr",   [STCR_R5_CR1, ADD_R2_R3_R4],   {"r3": 0x7fffffff, "r4": 1, "r5": PSR_INDCLR}, V_OVF, 0x10008, PSR_INDCLR, None),
+    ("umisalign", [STCR_R5_CR1, LD_R2_R3_0],    {"r3": DATA + 1, "r5": PSR_USER}, V_MISALIGN, 0x10008, PSR_USER,  None),
+    ("uovf",     [STCR_R5_CR1, ADD_R2_R3_R4],   {"r3": 0x7fffffff, "r4": 1, "r5": PSR_USER}, V_OVF, 0x10008, PSR_USER,  None),
+    ("errovf",   [DIVU_R2_R3_R0],               {"r3": 0x7fffffff, "r4": 1},     V_ERROR,    0x10004, PSR_RESET,
+                 [ADD_R2_R3_R4]),                             # handler at 0x40: an OVERFLOW (non-trap) with SFRZ set -> re-routed to ERROR
+    ("errdiv0",  [DIVU_R2_R3_R0],               {"r3": 0x10, "r5": PSR_FRZSUP},  V_ERROR,    0x10004, PSR_RESET,
+                 [STCR_R5_CR1, DIVU_R2_R3_R0]),               # handler: clear SFD1 (SFRZ kept), divu by zero -> DIV0 frozen -> ERROR
+    ("errpriv",  [DIVU_R2_R3_R0],               {"r3": 0x10, "r5": PSR_FRZUSER}, V_ERROR,    0x10004, PSR_RESET,
+                 [STCR_R5_CR1, LDCR_R2_CR1]),                 # handler: drop to USER mode (SFRZ kept), ldcr -> PRIVILEGE frozen -> ERROR
+    ("errunimpl", [DIVU_R2_R3_R0],              {"r3": 0x10, "r5": PSR_FRZUSER}, V_ERROR,    0x10004, PSR_RESET,
+                 [STCR_R5_CR1, PROM_CALL]),                   # handler: drop to USER mode (SFRZ kept), prom_call -> UNIMPLEMENTED frozen -> ERROR
     ("privsuptb", [TB1_0_R3_6],                 {"r3": 1},                       V_PRIV,     0x10004, PSR_RESET, None),
     ("udiv0",    [STCR_R3_CR1, DIVU_R2_R3_R0],  {"r3": PSR_USER},                V_DIV0,     0x10008, PSR_USER,  None),
     ("usertb",   [TB1_0_R3_128],                {"r3": 1},                       V_USER0,    0x10004, PSR_RESET, None),
@@ -300,7 +332,8 @@
     #  HALT is the fallback's diagnostic AND the machine-stopped observation (codex, pass 3: a mutant that keeps the
     #  message and drops the stop would otherwise classify as HALT); an expected-HALT row must also see ITS vector named.
     diag = re.search(r"unimplemented[^\r\n]*vector=0x([0-9a-f]+)", tr)
-    halted = diag is not None and ("machines stopped" in tr or "stopped" in tr)
+    stopped = "machines stopped" in tr           # emul.c's `All machines stopped.' -- the ONE stop observation (pass 4:
+    halted = diag is not None and stopped        # an `or "stopped" in tr' disjunct had made the exact term dead code)
     if halted and name in EXPECT_VECTOR and int(diag.group(1), 16) != EXPECT_VECTOR[name]:
         halted = False                              # halted on some OTHER vector: not the row's answer
     #  LEVEL channel (Fable review seat, pass 2): main.c lowers every subsystem to WARNING after startup, so a
@@ -310,7 +343,6 @@
     levelmsg = re.search(r"exception (MISALIGNED_ACCESS|UNIMPLEMENTED_OPCODE|PRIVILEGE_VIOLATION|"
                          r"BOUNDS_CHECK_VIOLATION|ILLEGAL_INTEGER_DIVIDE|INTEGER_OVERFLOW|ERROR)", tr) is not None
     tailhalt = "internal error" in tr
-    stopped = "machines stopped" in tr
     pc = s.pc(); r2 = s.gpr(2); r9 = s.gpr(9)
     sxip, snip, sfip, psr, epsr = s.cr("SXIP"), s.cr("SNIP"), s.cr("SFIP"), s.cr("PSR"), s.cr("EPSR")
     s.close()
@@ -333,7 +365,7 @@
         res["result"] = "STOP"          # ran past its grace without the entry breakpoint firing
     else:
         want = dict(sxip=(fault_pc | XIP_V), psr=PSR_WANT.get(name, PSR_EXC), epsr=epsr_exp, r2=0xdeadbeef)
-        if name in ("error", "trapfrozen"):
+        if name in ("error", "trapfrozen", "errovf", "errdiv0", "errpriv", "errunimpl"):
             # the second fault runs with SFRZ set: the shadows stay FROZEN at the first fault's values.  For
             # `trapfrozen' the second fault is a TRAP, which the manual (:8633-8636, 6.10 :10613-10614) exempts from
             # the ERROR re-route: it must deliver to ITS OWN vector (0x38), shadows still frozen.  M_SFRZTRAP sends it to 0x50.
```

Frozen-copy vs shipped (docstring only; the Table 6-3 attribution correction from pass 4):
```
32,33c32,34
<              *** THIS ROW PINS THE ELSE-ARM AS IMPLEMENTED, NOT AS THE MANUAL'S CONTRACT.  Table 6-3 (shadows copy
<              XIP/NIP/FIP: for a fault in the delay slot of a taken br.n, NIP = target, FIP = target+4) and X(rte)'s
---
>              *** THIS ROW PINS THE ELSE-ARM AS IMPLEMENTED, NOT AS THE MANUAL'S CONTRACT.  Table 6-3 (the shadows copy
>              XIP/NIP/FIP) with the pointer definitions at UM 6.2 (mc88100.txt:2093-2104: FIP is the taken branch's
>              target while the branch executes, so for a fault in its delay slot NIP = target, FIP = target+4) and X(rte)'s
```

Product code in this repair: COMMENT-ONLY, two passages in `cpu_m88k.c` (grep anchors `6-3: the shadows copy XIP/NIP/FIP` and
`updated normally when that trap is taken UNFROZEN`):
* "the manual disagrees (Table 6-3: NIP = the branch target, FIP = target+4)" -> "(Table 6-3: the shadows copy XIP/NIP/FIP, and UM 6.2
  defines FIP as the taken branch's target while the branch executes, so for a fault in its delay slot NIP = target, FIP = target+4)".
* "a supervisor tb0/tb1/tcnd naming vector 10 directly (shadows updated normally)" -> "(shadows updated normally when that trap is
  taken UNFROZEN; inside a handler it takes the is_trap exemption above and arrives here with the shadows frozen)".
Propagated to est/build/build-asan/WSL; the three build trees rebuilt; two-part clearance CLEAN + FRESH on all three (`rebuild_fix2.log`).

## THE GATE PINS ADDED (`regress/gate_m88k_rounding.sh`, verbatim)
```
    check "m88k exc: user-mode MISALIGNED and OVERFLOW deliver (umisalign 0x20, uovf 0x48 -- the {class} x {MODE} closure)" \
          "$(grep -cE '^M88KEXC_ROW=(umisalign +RESULT=DELIVER +pc=0x00000020|uovf +RESULT=DELIVER +pc=0x00000048) .*psr=0x8000000b .*epsr=0x00000002' "$EXCLOG")" "2"
    check "m88k exc: a frozen handler's non-trap fault of every class re-routes to ERROR (errovf errdiv0 errpriv errunimpl at 0x50)" \
          "$(grep -cE '^M88KEXC_ROW=err(ovf|div0|priv|unimpl) +RESULT=DELIVER +pc=0x00000050' "$EXCLOG")" "4"
```
plus `M88KEXC_RESULT=23/23` -> `29/29`.

## TABLE 5, MEASURED (`regress/artifacts/m88kexcdeliver/killtable5/`, frozen v5 md5 c83b1f38, scratch clone of the fix build
## `cmp`-clean against SEC, BASE 29/29 before and after, sentinel clear; `PRETABLE5_m88kexc.out` written 08:47, table start 08:48)
| mutant (exact edit) | score | red rows |
|---|---|---|
| M_OVFSUPONLY: OVERFLOW arm `implemented = (PSR & MODE) != 0` | 28/29 | uovf HALT |
| M_MISSUPONLY: MISALIGNED arm, same edit | 28/29 | umisalign HALT |
| M_SFRZMIS: `if (!is_trap && vector == MISALIGNED_ACCESS)` on the re-route | 25/29 | errovf, errdiv0, errpriv, errunimpl STOP |
| M_SFRZNOOVF: `!is_trap && vector != INTEGER_OVERFLOW` | 28/29 | errovf STOP |
| M_SFRZNODIV0: `!is_trap && vector != ILLEGAL_INTEGER_DIVIDE` | 28/29 | errdiv0 STOP |
| M_SFRZNOPRIV: `!is_trap && vector != PRIVILEGE_VIOLATION` | 28/29 | errpriv STOP |
| M_SFRZNOUNIMPL: `!is_trap && vector != UNIMPLEMENTED_OPCODE` | 28/29 | errunimpl STOP |
| M_NOSFD1: `| M88K_PSR_SFD1` -> `| 0` in the exception-path PSR write | 1/29 | 27 rows bad=psr (0x80000003), sfu1h STOP (its handler's divu ran instead of raising SFU1); resid50 survives (a HALT row never compares PSR) |
Every kill is by exactly the rows PRETABLE5 named before the table ran.  HEAD with the final instrument (`probe_v5_head.out`, the
/tmp/gxopus501p4 clone whose cpu_m88k.c `cmp`s equal to HEAD): **2/29** -- usertb DELIVER, resid50 HALT, sfu1h STOP (the first divu
halts on 0x008), every other class HALT.  The fix on the rebuilt build/: **29/29** (`probe_v5_fix_final.out`).

## THE CLOSURE, WRITTEN INTO THE CONTRACT (probe docstring, CONTRACT paragraph)
* {class} x {PSR.MODE at fault}: DIV0 udiv0; PRIVILEGE priv, privtb; UNIMPLEMENTED unimpl; MISALIGNED umisalign; OVERFLOW uovf.
  BOUNDS and ERROR: no user-mode route (a user tb1 naming them raises PRIVILEGE -- privtb; every handler runs supervisor).  DISCLOSED.
  Note MODE is tested by the CALLERS (`X(tb0)`, `m88k_stcr`) and never by `m88k_exception` itself, which is why one seat graded this
  axis clause-(e) rather than floor; it is closed either way.
* {SFRZ set, non-trap} x {class}: MISALIGNED error; OVERFLOW errovf; DIV0 errdiv0 (the handler clears SFD1 first -- with it set the
  same divu is sfu1h's SFU1); PRIVILEGE errpriv and UNIMPLEMENTED errunimpl (the handler drops to user mode keeping SFRZ).  BOUNDS and
  ERROR: no non-trap route; the frozen TRAP is trapfrozen (is_trap exemption, own vector, shadows frozen).  DISCLOSED.
* Still disclosed, unchanged: {class} x {delay_slot} beyond DIV0 (deferred to m88kdslotshadow: the arm is known wrong, more pins are
  more re-pins); M_DELAYALWAYS; vectors 0..3's tail arms; DMT contents (the common-path zeroing) and the frozen-trap DMT defect
  (m88kexcfrozendmt); SSBR; fcr2/4/5; first-exception SFU1 (m88kexcsfu1); exact INFO (only 'not ERROR/WARNING' is pinned);
  `implemented = is_trap` at BOUNDS/ERROR (equivalent today, m88ktbnd); a user-mode fault INSIDE a frozen handler for
  MISALIGNED/OVERFLOW/DIV0 (the {MODE} x {SFRZ} x {class} triple: same re-route code path as errpriv/errunimpl, MODE untested by
  the function -- clause (e)).

## THE DENOMINATOR THIS PASS CLAIMS CLOSED (tables 1-5; every score in a named log under regress/artifacts/m88kexcdeliver/)
12 reachable class x route cells (instruction and *tb rows; 7-insn and 10-insn disclosed); fallback predicate / off / stop (M_REVERT
3/22, M_DELIVERALL 21/23, M_NOSTOP 21/23); tail labels / bound / return (M_NAIVE 3/22, M_TAILLE 21/22, M_TAILRETURN 2/23); {SFRZ} x
{is_trap} four cells with frozen-shadow polarity both ways (M_SFRZTRAP 21/22, M_UPDSHADOWTRAP 22/23, M_ERRORDROP 21/22); {SFRZ
set, non-trap} x {class} five cells (table 5); {class} x {MODE} five cells (table 5 + udiv0/priv/privtb/unimpl); VBR (M_NOVBR
21/22, vbrtb anchored); PSR bits SFRZ/IND/SFD1/MODE/C each measured (M_NOSFRZ 2/23, M_NOIND 22/23, M_NOSFD1 1/29, M_NOMODE 19/23,
M_CARRYCLR 22/23); EPSR (M_NOEPSR 2/23, M_EPSRAFTER 2/23); shadows (M_NOSHADOW 3/23, M_SNIPX 3/23, M_DSLOT / M_SFIPNOTGT /
M_DSLOTSWAP 21/22); LEVEL (M_LEVEL 3/23); vector scaling (M_VEC4 1/23, M_VEC7).

## THE ONE QUESTION
**Does a clean-sweep mutant exist in the (d) DEPENDS-ON enumeration of the SHIPPED COMPOSITE (the #502 fix + probe v5)?**  The
enumeration is: predicates dominating the diff's edited lines up to the function boundary (switch 1's class labels; the fallback
`vector < 128 && !implemented`; the re-route's `PSR & SFRZ` and `is_trap`; the tail switch's labels), and for operand swaps only
fields the guarded bodies read; joint cells where the body's own tests distinguish them (class x SFRZ x is_trap).  Review EFFORT is
scoped to the v5 repair diff above; the FLOOR question is asked of the composite.  If you find one, give the exact edit and the
row that should have caught it; if you find none, CLOSE with YOUR OWN denominator, not by repeating mine.  Second question, with the
count named: of the eleven dispositions this pass applied (two class closures, one classifier refine, six L4 records, one filing,
one carried-wording ruling), WHICH IS WRONG?

VERDICT LINE FIRST (CLOSE THE CHAIN / ONE MORE REPAIR: <which> / DO NOT SHIP), then the answer to the one question with its
denominator, then anything else, under a page.
