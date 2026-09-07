# PASS 8 -- `m88kexcdeliver` (#502): the closing pass on the PASS-7 REPAIR (probe v10 -> v14, 46 fault rows).  Tree `GXEMUL-SEC/src/`, HEAD `83df95c` + the uncommitted round.  2026-09-06, ~12:55.  SHORT BY DESIGN: one diff, one table, one question.

## CONTEXT AND VOCABULARY
An ordinary correctness review of an open-source machine emulator's CPU model (GXemul 0.7.0, hardened fork): the MC88100
exception-delivery path in `cpu_m88k.c` and its detector `regress/m88k_exc_probe.py`.  The "guest" is the operating system inside the
emulator.  Plain engineering vocabulary.  **If you cannot read files that is expected -- every fact is inlined; name any premise you
cannot settle rather than guessing.**  Tree under review: `GXEMUL-SEC/src/` (three pristine-2021 copies under the project root are NOT
this fork).  **VERDICT LINE FIRST.**  Cite by grep anchor.  `python3` in git-bash is a Windows Store stub; a file-reading seat that
needs Python uses `C:\Users\User00\AppData\Local\Programs\Python\Python312\python.exe`.

## WHY AN EIGHTH PASS, AND WHAT CLOSES IT
The repair-chain rule: a repair made in response to a pass owes its own pass, scoped to THAT diff; the chain closes on the first VALID
pass that finds zero floor breaches surviving adjudication, with the denominator stated; when consecutive passes find breaches of one
CLASS the next repair closes the class.  Pass 7 (v10, 41 rows; codex, kimi, grok, deepseek, minimax answered; glm BURNED for the second
consecutive pass; Opus 5 and Fable 5 walled until 12:50pm America/Chicago -- SEAT FAILURES, so every closure here is PROVISIONAL on their
re-fire; agy deliberately not fired) found these, each measured as a sweep of the v10 instrument in table 11 and all closed in one repair:
* **codex** -- switch 1 has TEN deliverable labels (4..10, 128 = USER_TRAPS_START, 0x1c2 = 450 the OpenBSD >= 5.3 syscall vector,
  MVMEPROM_VECTOR = 496) and the frozen-trap rows covered eight: `!is_trap || vector == 0x1c2` and `|| vector == MVMEPROM_VECTOR` on the
  re-route sweep -> rows `trapfrozen450` (entry 0xe10), `trapfrozen496` (0xf80).  The frozen-trap class is now closed over EVERY label.
* **kimi** -- (i) the exemption's FAR edge: `trapfrozen128` pinned 128 only, `!is_trap || vector >= 129` sweeps; tb1's vector field is 9
  bits, so 511 is the last nameable trap -> row `trapfrozen511` (0xff8): the accept-row-at-the-LAST-slot rule.  (ii) It CLAIMED `case ERROR:
  implemented = (PSR & SFRZ)` sweeps -- REFUTED by existing rows (errortb and bounds enter those arms UNFROZEN and would HALT), measured
  anyway (M_ERRORFRZON) so the record carries a measurement.  (iii) the {switch-1 arm} x {PSR bit} surface: the `implemented` arms read
  no PSR bit, so {arm} x {C, IND, SFD1} is clause-(e) debt by the joint-cell rule -- DISCLOSED in the contract, one representative
  MEASURED (M_MISNOC).  (iv) a stale REFATAL_EXPECT trailing comment -- removed (L4).
* **grok** -- the RE-ROUTE x {IND, C}: the re-route predicate READS PSR (`if (PSR & SFRZ)`), so a PSR-bit conjunct THERE is a narrowing on
  a body-read lvalue -- clause (d) floor, unlike the switch-1 arms.  Every SFRZ-set row reached it with IND set and C clear (0x8000000b
  after the first delivery; 0x80000003 / 0x00000003 from the handler-stcr rows), so `(PSR & SFRZ) && (PSR & IND)` and `&& !(PSR & C)`
  sweep by construction.  Rows `errind` (a frozen handler that CLEARS IND -- `stcr` 0x80000009 -- then faults MISALIGNED) and `errc`
  (C set, 0x9000000b); the quieter INNER form of the mutant is the one built (M_RRIND, M_RRNOC).  MODE (errpriv) and SFD1 (errdiv0)
  already varied at the re-route; MXM/BO cannot be set by `stcr`; the 88110-only bits are 88100 here -- disclosed.  Also: vector 11 is
  `M88K_EXCEPTION_NMI` in `cpu_m88k.h`, unimplemented in switch 1 -- the resid11 pin stands, the name is now in the docstring.
* **deepseek, minimax** -- CLOSE THE CHAIN; no breach named.
* **A MIS-CUT ROW CAUGHT BY THE TABLE'S OWN BASE GATE**: v13's `errc` wanted PSR 0x8000000b after delivery; exception entry ORs
  MODE|SFRZ|IND|SFD1 and leaves C alone (mc88100 manual, anchor `the shadow freeze, SFD1, and IND bits of the PSR are set`), so the
  C-set handler row keeps C.  BASE read 45/46 `bad=psr` before any mutant and the driver aborted; repaired in the instrument only
  (`PSR_WANT["errc"] = 0x9000000b`, v14); attempt 1 preserved; no product code touched, no mutant re-aimed.  A mutant-that-will-not-die
  case 3 in its BASE form.
This pass closes if it finds zero floor breaches surviving adjudication in the (d) enumeration of the shipped composite.

## SETTLED PREMISES, RE-INLINED (each a QUESTION if you can check it)
1. `m88k_psl.h`: MODE 0x80000000, C 0x10000000, SFD1 0x00000008, MXM 0x00000004, IND 0x00000002, SFRZ 0x00000001.  Reset PSR 0x80000002.
2. Order inside `m88k_exception()`: switch 1 (class -> `implemented`); the FALLBACK `if (vector < M88K_EXCEPTION_USER_TRAPS_START (128) &&
   !implemented)` -> `unimplemented vector=0x%03x`, every cpu stopped, `return`; THEN the SFRZ re-route `if (PSR & SFRZ) { if (!is_trap) {
   vector = ERROR; fatal("[ SFRZ already set in PSR => ERROR ]\n"); } update_shadow_regs = false; }`; then the common path (EPSR only when
   unfrozen; PSR |= SFRZ|IND|SFD1|MODE, other bits untouched; shadows only when unfrozen; pc = VBR + 8*vector); then the tail switch (labels
   per class; its `default:` prints `internal error` and stops the cpu -- reachable by no vector below 128 at HEAD-with-fix).
3. `fatal()` in this fork is a plain print with no early-out (`debugmsg.c`, anchor `fatal(`); it cannot be silenced by `-q`.  The line lands in
   the pty transcript the probe reads alongside the debugger prompt -- the refatal channel.
4. A TRAP (tb0/tb1/tcnd, is_trap = 1) taken with SFRZ set is exempted from the re-route and delivered to ITS OWN vector with frozen shadows;
   `stcr` stores the PSR verbatim (MODE-clear prints a WARNING and continues; MXM set or a BO flip stops the cpu); `divu` tests SFD1 before
   divisor == 0; `prom_call` raises UNIMPLEMENTED only in user mode; a user tb1 naming a vector < 128 raises PRIVILEGE.
5. The probe plants `br .` at every entry of every vector in VECTORS (incl. 11, 127, 450, 496, 511), the row's handler words at
   `8 * handler_at` (default 0x40), a breakpoint at the expected entry, then `continue`; HALT = the fallback diagnostic naming the row's
   vector AND `All machines stopped.`; TAILHALT = `internal error` + stopped; STOP = anything else; bad=refatal = the re-route's diagnostic
   present where the exemption should hold or absent where the re-route fired; bad=psr = PSR after delivery differs from PSR_WANT (default
   0x8000000b; 0x9000000b for the two C-set rows ovfc and errc).

## THE REPAIR DIFF (probe v10 -> v14; shipped md5 ee2c78c2 -> frozen v14 md5 99eb9c00), VERBATIM
```diff
--- GXEMUL-SEC/regress/artifacts/m88kexcdeliver/killtable10/m88k_exc_probe.frozen10.py	2026-09-06 11:31:29.570664300 -0500
+++ _scratchpad/m88kexc/m88k_exc_probe.v14.frozen.py	2026-09-06 12:16:43.035131900 -0500
@@ -70,13 +70,19 @@
              115..127, 128 being the bound itself: deepseek, pass 6).  EXPECTED RESULT = HALT
              naming 0x07f; a shrunk bound delivers 127 to 0x3f8
              and the tail default stops the cpu instead (TAILHALT) -- mutants M_FALLBACK127, M_FALLBACK51.
-  resid11    tb1 0,r3,11 (f003d80b): the FIRST residual vector -- the fallback window's NEAR bound.  `vector >= 12 &&' on the
+  resid11    tb1 0,r3,11 (f003d80b): the FIRST residual vector (M88K_EXCEPTION_NMI in cpu_m88k.h, unimplemented in switch 1 --
+             grok, pass 7) -- the fallback window's NEAR bound.  `vector >= 12 &&' on the
              fallback swept 36/36 because no row named 11..49 (kimi, pass 6).  EXPECTED RESULT = HALT naming 0x00b        (0x58)
   resid50ind stcr r5,cr1 (r5=0x80000000: IND CLEAR) then tb1 0,r3,50: the fallback with IND clear -- `&& (PSR & IND)' on the
              fallback swept 36/36 because every fallback row had IND set.  EXPECTED RESULT = HALT naming 0x032          (0x190)
   resid50c   stcr r5,cr1 (r5=0x90000002: C SET) then tb1 0,r3,50: the fallback with C set -- `&& !(PSR & C)' swept likewise.
              With usfu1 (MODE clear, SFD1 set) and sfu1h (SFRZ set) these give every settable PSR bit both sides at the
              fallback; MXM and BO cannot be set by stcr without stopping the cpu -- disclosed.  EXPECTED RESULT = HALT    (0x190)
+  trapfrozen450 / trapfrozen496  the same shape naming 0x1c2 (the OpenBSD >= 5.3 syscall vector) and MVMEPROM_VECTOR: the LAST
+             two switch-1 labels.  Switch 1 has TEN deliverable labels -- 4..10, 128, 450, 496 -- and the frozen-trap rows now
+             cover all ten; `!is_trap || vector == 0x1c2' swept 41/41 before these (codex, pass 7)                  0xe10 / 0xf80
+  trapfrozen511 the same shape naming 511, the LAST nameable trap vector (tb1's field is 9 bits): trapfrozen128 pinned only the
+             near edge of the user range -- `!is_trap || vector >= 129' swept (kimi, pass 7; the last-slot rule again)          0xff8
   trapfrozen128 div0 whose handler is tb1 0,r3,128: a frozen USER trap is exempted from the re-route like any trap and
              delivered to 0x400 with frozen shadows -- `!is_trap || vector >= 128' swept 36/36 (kimi, pass 6)              0x400
   usfu1      stcr r5,cr1 (r5=0x0000000a: USER mode, SFD1 set) then a LEGAL divu r6,r5,r4: SFU1 (114) raised from USER
@@ -105,6 +111,12 @@
   errovf     div0 whose handler at 0x40 is add 7fffffff+1: a NON-TRAP fault of a SECOND class with
              SFRZ set -> re-routed to ERROR with frozen shadows (M_SFRZMIS -- `!is_trap && vector ==
              MISALIGNED' on the re-route -- swept 23/23 because `error' was that cell's only row)      0x50
+  errind     div0 whose handler is stcr r4,cr1 (r4=0x80000009: SFRZ kept, IND CLEAR) then the odd ld: the re-route with
+             interrupts enabled -- every SFRZ-set row had reached it with IND set, so `(PSR & SFRZ) && (PSR & IND)'
+             swept (grok, pass 7).  Expect ERROR at 0x50, frozen shadows, the diagnostic present                     0x50
+  errc       the same with r4=0x9000000b (C SET): `&& !(PSR & C)' on the re-route swept likewise; expects PSR 0x9000000b after
+             delivery (C survives exception entry -- the row first shipped wanting 0x8000000b and BASE caught it).  MODE (errpriv) and SFD1
+             (errdiv0) already vary at the re-route; MXM/BO cannot be set by stcr; the 88110-only PSR bits are 88100 here  0x50
   errdiv0    div0 whose handler is stcr r5,cr1 (r5=0x80000003: SFD1 CLEAR, SFRZ kept) then divu by zero:
              a frozen non-trap DIV0 -> ERROR (with SFD1 set the same divu raises SFU1 instead: sfu1h)     0x50
   errpriv    div0 whose handler is stcr r5,cr1 (r5=0x00000003: USER mode, SFRZ kept) then ldcr: a frozen
@@ -150,11 +162,15 @@
 clear vs PSR MODE set); a MODE-conditioned `implemented' on any class that user mode can raise ({class} x
 {MODE} closure: DIV0 udiv0, PRIVILEGE priv/privtb, UNIMPLEMENTED unimpl, MISALIGNED umisalign, OVERFLOW uovf;
 BOUNDS and ERROR have no user-mode route -- a user tb1 naming them raises PRIVILEGE, and every handler runs
-supervisor; the FALLBACK predicate itself is pinned in user mode by usfu1, the one user-mode route to it); a class-conditioned SFRZ re-route, its diagnostic pinned both ways by the refatal channel ({SFRZ set, !is_trap} x {class}: MISALIGNED error, OVERFLOW errovf,
+supervisor; the FALLBACK predicate itself is pinned in user mode by usfu1, the one user-mode route to it); a class-conditioned SFRZ re-route, its diagnostic pinned both ways by the refatal channel, and a PSR-bit conjunct on the re-route (the
+predicate reads PSR: every stcr-settable 88100 bit now varies there -- MODE errpriv, SFD1 errdiv0, IND errind, C errc; MXM/BO cannot be
+set by stcr and the 88110-only bits are 88100 here -- disclosed) ({SFRZ set, !is_trap} x {class}: MISALIGNED error, OVERFLOW errovf,
 DIV0 errdiv0 -- the handler clears SFD1 first, with it set the divu raises SFU1 instead (sfu1h) --, PRIVILEGE errpriv
 and UNIMPLEMENTED errunimpl -- the handler drops to user mode keeping SFRZ; BOUNDS and ERROR have no non-trap route,
 the frozen TRAP is trapfrozen); a wrong return address; the delay-slot else-arm's SFIP source (dslot, +16
-geometry); a trap re-routed to ERROR while frozen, per class ({SFRZ set, is_trap} x {class}: trapfrozen (7), trapfrozen4/5/6/8/9/10/128 --
+geometry); a trap re-routed to ERROR while frozen, per class ({SFRZ set, is_trap} x {EVERY deliverable switch-1 label}: trapfrozen (7),
+trapfrozen4/5/6/8/9/10/128/450/496/511 -- the ten labels 4..10, 128, 0x1c2, MVMEPROM_VECTOR, enumerated from switch 1's `case' list, plus
+the far edge of the user range (511) --
 class 10's re-route exemption is told from the re-route by the refatal channel (the pass-6 packet called it equivalent; kimi refuted
 that: the re-route prints a diagnostic the exemption does not) and switch 1's ERROR eligibility under SFRZ by trapfrozen10's
 HALT/DELIVER; 0..3 are the hardware-event tails, m88kexchwtraps); the fallback window's NEAR bound (resid11) and the fallback predicate
@@ -163,7 +179,10 @@
 `cpu->delay_slot' write on the NON-delay path (M_DELAYALWAYS: needs a second UNFROZEN exception -- filed);
 vectors 0..3's tail arms (no row: M_TAILOFF -- filed); vectors 11..113 and 116..127 (fallback halts by
 design); SFU1 (114/115, row m88kexcsfu1); `implemented = is_trap' on BOUNDS/ERROR (EQUIVALENT today: no
-instruction raises 7 or 10 -- becomes live when tbnd lands, row m88ktbnd).
+instruction raises 7 or 10 -- becomes live when tbnd lands, row m88ktbnd); a PSR-bit conjunct on a switch-1 `implemented' arm
+OTHER than MODE (closed for every class) and SFRZ at ERROR (both polarities: errortb unfrozen, trapfrozen10 frozen) -- the arms read no PSR
+bit, so {arm} x {C, IND, SFD1} is clause-(e) debt, not floor; one representative (MISALIGNED with `!(PSR & C)', M_MISNOC) is MEASURED to
+record the escape rather than assert it (kimi, pass 7).
 """
 import os, pty, re, select, struct, sys, time
 
@@ -177,6 +196,8 @@
 PSR_FRZSUP = 0x80000003         # MODE | IND | SFRZ, SFD1 CLEAR: a frozen handler that wants its divu to raise DIV0, not SFU1
 PSR_FRZUSER = 0x00000003        # IND | SFRZ, MODE CLEAR: a frozen handler dropping to user mode (PRIVILEGE / UNIMPLEMENTED routes)
 PSR_USERSFD1 = 0x0000000a       # IND | SFD1, MODE CLEAR: user mode with the FPU disabled -- a legal divu raises SFU1 (kimi, pass 5)
+PSR_FRZNOIND = 0x80000009       # MODE | SFD1 | SFRZ, IND CLEAR: a frozen handler that re-enables interrupts (grok, pass 7)
+PSR_FRZC = 0x9000000b           # C | MODE | SFD1 | IND | SFRZ: a frozen handler with the carry bit set (grok, pass 7)
 
 def tri(sub, d, s1, s2):
     return 0xf4000000 | (d << 21) | (s1 << 16) | (sub << 8) | s2
@@ -198,6 +219,9 @@
 TB1_0_R3_9 = 0xf003d809                          # tb1 0,r3,9   -- naming INTEGER_OVERFLOW (9)
 TB1_0_R3_6 = 0xf003d806                          # tb1 0,r3,6   -- naming PRIVILEGE_VIOLATION (6): the user-mode tb1 filter raises
                                                  #   PRIVILEGE with is_trap == 0 (cpu_m88k_instr.c X(tb0)), so privtb is NOT the trap route
+TB1_0_R3_450 = 0xf003d9c2                        # tb1 0,r3,450 -- the 0x1c2 syscall vector (OpenBSD >= 5.3): a switch-1 label of its own
+TB1_0_R3_496 = 0xf003d9f0                        # tb1 0,r3,496 -- MVMEPROM_VECTOR: likewise
+TB1_0_R3_511 = 0xf003d9ff                        # tb1 0,r3,511 -- the LAST nameable trap vector (9-bit field): the far edge of the user-trap range
 TB1_0_R3_128 = 0xf003d880                        # tb1 0,r3,128 -- the first USER trap vector: delivered by the pre-existing code (entry 0x400)
 TB1_0_R3_50 = 0xf003d832                         # tb1 0,r3,50  -- a RESIDUAL vector (11..113): must still HALT (negative control vs D4)
 TB1_0_R3_11 = 0xf003d80b                         # tb1 0,r3,11  -- the FIRST residual vector: the fallback window's NEAR bound (kimi, pass 6)
@@ -208,6 +232,7 @@
 #  escapes the instruction rows for MISALIGNED/UNIMPL/DIV0/OVF; these rows are the ones that redden it (M_ISTRAP).
                          # tb1 0,r3,10  (a supervisor trap naming vector 10 = ERROR directly)
 STCR_R3_CR1 = 0x80038023                         # stcr r3,cr1 (PSR)
+STCR_R4_CR1 = 0x80048024                         # stcr r4,cr1 (PSR) -- for handlers whose r5 is the odd load address
 STCR_R5_CR1 = 0x80058025                         # stcr r5,cr1 (PSR)  -- same format: 0x80000000 | S1<<16 | 0x8000 | CR<<5 | S1
 STCR_R5_CR7 = 0x800580e5                         # stcr r5,cr7 (VBR)
 PSR_CARRY = 0x90000002                           # MODE | C | IND: the ovfc row's pre-fault PSR (C = bit 28, UM 6.6 'carry bit unchanged')
@@ -225,7 +250,10 @@
 V_RESID = 50
 V_RESID2 = 127
 V_RESID0 = 11
-VECTORS = (V_MISALIGN, V_UNIMPL, V_PRIV, V_BOUNDS, V_DIV0, V_OVF, V_ERROR, V_SFU1, V_USER0, V_RESID, V_RESID2, V_RESID0)
+V_SYSCALL = 450
+V_MVMEPROM = 496
+V_USERLAST = 511
+VECTORS = (V_MISALIGN, V_UNIMPL, V_PRIV, V_BOUNDS, V_DIV0, V_OVF, V_ERROR, V_SFU1, V_USER0, V_RESID, V_RESID2, V_RESID0, V_SYSCALL, V_MVMEPROM, V_USERLAST)
 
 # name, program words after MARK, regs, vector, fault_pc, epsr, handler words at the div0 entry (None = br .)
 # [, handler_at: the vector whose entry the handler is planted at -- only trapfrozen8 sets it, to OVF (0x48), because its frozen
@@ -259,6 +287,12 @@
                  [TB1_0_R3_8], V_OVF),                        # first fault OVF (handler at 0x48); frozen tb1 naming 8 -> 0x40, observable
     ("trapfrozen9", [DIVU_R2_R3_R0],            {"r3": 0x11},                    V_OVF,      0x10004, PSR_RESET,
                  [TB1_0_R3_9]),                               # frozen tb1 naming 9 -> 0x48
+    ("trapfrozen450", [DIVU_R2_R3_R0],          {"r3": 0x11},                    V_SYSCALL,  0x10004, PSR_RESET,
+                 [TB1_0_R3_450]),                             # a frozen trap naming the 0x1c2 syscall label -> its own entry 0xe10 (codex, pass 7)
+    ("trapfrozen496", [DIVU_R2_R3_R0],          {"r3": 0x11},                    V_MVMEPROM, 0x10004, PSR_RESET,
+                 [TB1_0_R3_496]),                             # a frozen trap naming MVMEPROM_VECTOR -> its own entry 0xf80
+    ("trapfrozen511", [DIVU_R2_R3_R0],          {"r3": 0x11},                    V_USERLAST, 0x10004, PSR_RESET,
+                 [TB1_0_R3_511]),                             # the LAST user trap vector, frozen: exempted like 128 (kimi, pass 7: 128 pinned only the near edge)
     ("trapfrozen128", [DIVU_R2_R3_R0],          {"r3": 0x11},                    V_USER0,    0x10004, PSR_RESET,
                  [TB1_0_R3_128]),                             # a frozen USER trap: exempted from the re-route, delivered to 0x400 with frozen shadows
     ("trapfrozen10", [DIVU_R2_R3_R0],           {"r3": 0x11},                    V_ERROR,    0x10004, PSR_RESET,
@@ -270,6 +304,10 @@
     ("uovf",     [STCR_R5_CR1, ADD_R2_R3_R4],   {"r3": 0x7fffffff, "r4": 1, "r5": PSR_USER}, V_OVF, 0x10008, PSR_USER,  None),
     ("errovf",   [DIVU_R2_R3_R0],               {"r3": 0x7fffffff, "r4": 1},     V_ERROR,    0x10004, PSR_RESET,
                  [ADD_R2_R3_R4]),                             # handler at 0x40: an OVERFLOW (non-trap) with SFRZ set -> re-routed to ERROR
+    ("errind",   [DIVU_R2_R3_R0],               {"r3": 0x10, "r4": PSR_FRZNOIND, "r5": DATA + 1}, V_ERROR, 0x10004, PSR_RESET,
+                 [STCR_R4_CR1, 0x14000000 | (6 << 21) | (5 << 16)]),   # handler: keep SFRZ, clear IND, then the odd ld -> re-route with IND clear
+    ("errc",     [DIVU_R2_R3_R0],               {"r3": 0x10, "r4": PSR_FRZC, "r5": DATA + 1},     V_ERROR, 0x10004, PSR_RESET,
+                 [STCR_R4_CR1, 0x14000000 | (6 << 21) | (5 << 16)]),   # handler: keep SFRZ, set C, then the odd ld -> re-route with C set
     ("errdiv0",  [DIVU_R2_R3_R0],               {"r3": 0x10, "r5": PSR_FRZSUP},  V_ERROR,    0x10004, PSR_RESET,
                  [STCR_R5_CR1, DIVU_R2_R3_R0]),               # handler: clear SFD1 (SFRZ kept), divu by zero -> DIV0 frozen -> ERROR
     ("errpriv",  [DIVU_R2_R3_R0],               {"r3": 0x10, "r5": PSR_FRZUSER}, V_ERROR,    0x10004, PSR_RESET,
@@ -296,17 +334,21 @@
 #  vectors 11..113/116..127 and SFU1 (114/115) still stop the machine -- and separate the shipped D1 form from the rejected
 #  D4 (tail-default-delivers) and from delivering SFU1 (row m88kexcsfu1).  A mutant that delivers them turns these rows RED.
 EXPECT_RESULT = {"resid50": "HALT", "resid127": "HALT", "resid11": "HALT", "resid50ind": "HALT", "resid50c": "HALT", "sfu1h": "HALT", "usfu1": "HALT"}
-PSR_WANT = {"ovfc": 0x9000000b}                  # MODE | C | SFD1 | IND | SFRZ: carry PRESERVED through the exception path
+PSR_WANT = {"errc": 0x9000000b,   # v14: exception entry ORs MODE|SFRZ|IND|SFD1 and leaves C alone (mc88100 manual: "the shadow freeze,
+                                  #      SFD1, and IND bits of the PSR are set"), so the C-set handler row keeps C -- table 11 BASE read
+                                  #      45/46 bad=psr on this row before any mutant: a MIS-CUT ROW, not the fix (case 3)
+            "ovfc": 0x9000000b}                  # MODE | C | SFD1 | IND | SFRZ: carry PRESERVED through the exception path
 #  indclr wants the default PSR_EXC (0x8000000b): IND was CLEAR before the fault and must be SET by the exception path;
 #  EPSR keeps the pre-fault 0x80000000.  A write that drops `| M88K_PSR_IND' leaves 0x80000009 -> bad=psr.
 EXPECT_VECTOR = {"resid50": 0x032, "resid127": 0x07f, "resid11": 0x00b, "resid50ind": 0x032, "resid50c": 0x032, "sfu1h": 0x072, "usfu1": 0x072}
+#  (the vector the fallback diagnostic must NAME for an expected-HALT row -- the comment that used to trail the dict above)
 #  refatal: the re-route prints `[ SFRZ already set in PSR => ERROR ]' (fatal() is a plain print in this fork); a re-routed non-trap row
 #  must SEE it, a frozen-trap row must NOT -- the channel that tells the exemption arm from the re-route arm when both land on 0x50
 #  (kimi, pass 6: the class-10 "equivalent" disclosure was false for the composite).
 REFATAL = "SFRZ already set in PSR"
-REFATAL_EXPECT = {"error": True, "errovf": True, "errdiv0": True, "errpriv": True, "errunimpl": True,
+REFATAL_EXPECT = {"error": True, "errovf": True, "errdiv0": True, "errpriv": True, "errunimpl": True, "errind": True, "errc": True,
                   "trapfrozen": False, "trapfrozen4": False, "trapfrozen5": False, "trapfrozen6": False, "trapfrozen8": False,
-                  "trapfrozen9": False, "trapfrozen10": False, "trapfrozen128": False}   # the vector the fallback diagnostic must NAME for an expected-HALT row
+                  "trapfrozen9": False, "trapfrozen10": False, "trapfrozen128": False, "trapfrozen450": False, "trapfrozen496": False, "trapfrozen511": False}   # the vector the fallback diagnostic must NAME for an expected-HALT row
 
 class Sess:
     def __init__(self):
@@ -439,8 +481,9 @@
         res["result"] = "STOP"          # ran past its grace without the entry breakpoint firing
     else:
         want = dict(sxip=(fault_pc | XIP_V), psr=PSR_WANT.get(name, PSR_EXC), epsr=epsr_exp, r2=0xdeadbeef)
-        if name in ("error", "trapfrozen", "errovf", "errdiv0", "errpriv", "errunimpl",
-                    "trapfrozen4", "trapfrozen5", "trapfrozen6", "trapfrozen8", "trapfrozen9", "trapfrozen10", "trapfrozen128"):
+        if name in ("error", "trapfrozen", "errovf", "errdiv0", "errpriv", "errunimpl", "errind", "errc",
+                    "trapfrozen4", "trapfrozen5", "trapfrozen6", "trapfrozen8", "trapfrozen9", "trapfrozen10", "trapfrozen128",
+                    "trapfrozen450", "trapfrozen496", "trapfrozen511"):
             # the second fault runs with SFRZ set: the shadows stay FROZEN at the first fault's values.  For
             # `trapfrozen' the second fault is a TRAP, which the manual (:8633-8636, 6.10 :10613-10614) exempts from
             # the ERROR re-route: it must deliver to ITS OWN vector (0x38), shadows still frozen.  M_SFRZTRAP sends it to 0x50.
```
Product code in this repair: NONE.  The gate (`regress/gate_m88k_rounding.sh`) pins `M88KEXC_RESULT=46/46`, the six frozen-handler rows at
0x50 (`err(ovf|div0|priv|unimpl|ind|c)`), the eleven frozen-trap rows `trapfrozen(4|5|6|8|9|10|128|450|496|511)?` DELIVER, the seven HALT
rows, `bad=refatal` absent, `bad=level` absent, indclr, vbrtb, ovfc, the controls.

## TABLE 11, MEASURED
| mutant (exact edit) | on frozen v10 (41 rows) | on frozen v14 (46 rows) | red row on v14 |
|---|---|---|---|
| M_SFRZTRAP450: re-route `if (!is_trap \|\| vector == 0x1c2)` | **41/41 SWEEP** | 45/46 | trapfrozen450 STOP |
| M_SFRZTRAP496: `\|\| vector == MVMEPROM_VECTOR` | **41/41 SWEEP** | 45/46 | trapfrozen496 STOP |
| M_SFRZTRAPHI: `\|\| vector >= USER_TRAPS_START + 1` | **41/41 SWEEP** | 43/46 | trapfrozen450, trapfrozen496, trapfrozen511 STOP |
| M_ERRORFRZON: switch 1's ERROR arm `implemented = (PSR & SFRZ) != 0` | **40/41 -- NOT a sweep** | 45/46 | errortb HALT on both (kimi's sweep claim REFUTED by measurement, exactly as the existing errortb/bounds rows predicted) |
| M_MISNOC: MISALIGNED arm `implemented = !(PSR & C)` | 41/41 (the disclosed clause-(e) escape) | 45/46 | **errc HALT** -- the new re-route row kills the disclosed representative as a side effect |
| M_RRIND: re-route inner `if (!is_trap && (PSR & IND))` | **41/41 SWEEP** | 45/46 | errind STOP |
| M_RRNOC: re-route inner `if (!is_trap && !(PSR & C))` | **41/41 SWEEP** | 45/46 | errc STOP |

BASE 46/46 before the table and 46/46 after it; the clone `cmp`s clean against SEC and its sentinel is clear.  Five of the seven
mutants are MEASURED SWEEPS of the probe that shipped before this repair, each killed by exactly the row the PRETABLE named.  Two are
results of a different kind and both are recorded rather than tidied away: M_ERRORFRZON was CLAIMED to be a sweep by the seat that
proposed it and measured 40/41, refuted by rows that already existed; M_MISNOC was DISCLOSED as clause-(e) debt and turns out to be
killed by the repair's own new row, so the disclosure is narrowed in the shipped docstring (probe v15) rather than left overclaiming.

HEAD `83df95c` (`/tmp/gxopus501p4`, `cmp`-checked against `git show HEAD:src/cpus/cpu_m88k.c`) with the final instrument: **7/46**
(`probe_v14_head.out`; usertb DELIVER, and resid50 / resid127 / resid11 / resid50ind / resid50c / usfu1 HALT -- the fallback exists on
HEAD, every other class HALTs, sfu1h STOP).  The fix on the rebuilt `build/`: **46/46** (`probe_v14_fix_final.out`).

A MIS-CUT ROW, CAUGHT BY THE DRIVER'S OWN BASE GATE, is recorded here because it is the kind of thing a packet usually hides
(`killtable11_attempt1_v13/`, preserved in full with its own driver log): probe v13's `errc` expected PSR 0x8000000b after delivery.
BASE read **45/46 `bad=psr`** before a single mutant was built and the driver aborted.  Exception entry ORs MODE|SFRZ|IND|SFD1 and
leaves C alone, so a handler that set C keeps it -- the sibling `ovfc` row states the same fact from the other side.  Repaired in the
INSTRUMENT only (`PSR_WANT["errc"] = 0x9000000b`, v14); no product code was touched and no mutant was re-aimed.

## THE CLOSURES NOW IN THE CONTRACT (probe docstring)
* {class} x {PSR.MODE}: DIV0 udiv0; PRIVILEGE priv/privtb; UNIMPLEMENTED unimpl; MISALIGNED umisalign; OVERFLOW uovf; BOUNDS/ERROR no user route.
* {SFRZ set, non-trap} x {class}: error, errovf, errdiv0, errpriv, errunimpl; BOUNDS/ERROR no non-trap route.  Each must SEE the re-route's line.
* {SFRZ set, is_trap} x {EVERY deliverable switch-1 label}: trapfrozen (7), trapfrozen4/5/6/8/9/10/128/450/496 + the far edge 511 -- each must
  NOT see the line; class 10's eligibility under SFRZ pinned both ways (trapfrozen10 HALT/DELIVER + refatal; M_ERRORFRZON measured).
* the re-route x {every stcr-settable 88100 PSR bit}: MODE errpriv, SFD1 errdiv0, IND errind, C errc; MXM/BO not settable; 88110 bits are 88100 here.
* the fallback window: resid11 (near bound, = M88K_EXCEPTION_NMI), resid50 / resid50ind / resid50c (interior; PSR default / IND clear / C set),
  sfu1h (114, SFRZ set), usfu1 (114 from user mode, SFD1 set), resid127 (far bound), usertb (128, outside).
* still disclosed: {switch-1 arm} x {C, IND, SFD1} (the arms read no PSR bit; M_MISNOC measured as the representative); {class} x {delay_slot}
  beyond DIV0 (m88kdslotshadow); M_DELAYALWAYS; vectors 0..3 (m88kexchwtraps); DMT contents; SSBR; fcr2/4/5; first-exception SFU1
  (m88kexcsfu1; 115 likewise); exact INFO; `implemented = is_trap` at BOUNDS/ERROR (equivalent today, m88ktbnd); the {MODE} x {SFRZ} x {class}
  triple for MISALIGNED/OVERFLOW/DIV0 (clause e); an exemption of a single residual vector other than 11/50/127 from the fallback.

## THE DENOMINATOR THIS PASS CLAIMS CLOSED (tables 1-11, every score in a named log under regress/artifacts/m88kexcdeliver/)
Pass 7's denominator (12 class x route cells; the fallback predicate/off/stop/near/far/outside/user/IND/C; switch 1's eligibility per class
incl. ERROR under SFRZ; the {class} x {MODE} closure; the re-route's source, is_trap polarity, per-class non-trap and trap incl. 10 and 128, the
diagnostic both ways; tail labels/bound/return; VBR; the five PSR bits on the common path; EPSR; shadows; LEVEL; vector scaling) PLUS table 11:
the frozen traps at the last three labels and the far edge (M_SFRZTRAP450, M_SFRZTRAP496, M_SFRZTRAPHI), the ERROR arm eligible only when
frozen (M_ERRORFRZON), the MISALIGNED-C representative (M_MISNOC), and the re-route x {IND, C} (M_RRIND, M_RRNOC).

## THE ONE QUESTION
**Does a clean-sweep mutant exist in the (d) DEPENDS-ON enumeration of the SHIPPED COMPOSITE (the #502 fix + probe v14)?**  The enumeration:
predicates dominating the diff's edited lines up to the function boundary (switch 1's class labels; the fallback's `vector < 128 &&
!implemented`; the re-route's `PSR & SFRZ` and `is_trap`; the tail switch's labels), operand swaps drawn only from fields the guarded bodies
read (the re-route reads PSR -- so PSR bits are in scope THERE and not at the switch-1 arms), and joint cells where the body's own tests
distinguish them.  Review EFFORT is scoped to the v10 -> v14 diff above; the FLOOR question is asked of the composite.  If you find one, give
the exact edit and the row that should have caught it; if none, CLOSE with YOUR OWN denominator.  Second question, with the count named: of the
pass-7 dispositions (FIVE row closures -- trapfrozen450, trapfrozen496, trapfrozen511, errind, errc; ONE claim refuted by existing rows and
measured anyway (M_ERRORFRZON); ONE surface disclosed with a measured representative ({arm} x {C, IND, SFD1}, M_MISNOC); ONE mis-cut row
repaired from the BASE gate (errc's PSR); ONE records note (vector 11 = NMI); ONE L4 (the stale comment)), WHICH IS WRONG?

VERDICT LINE FIRST (CLOSE THE CHAIN / ONE MORE REPAIR: <which> / DO NOT SHIP), then the answer to the one question with its denominator,
then anything else, under a page.
