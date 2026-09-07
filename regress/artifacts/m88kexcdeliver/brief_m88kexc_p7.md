# PASS 7 -- `m88kexcdeliver` (#502): the closing pass on the PASS-6 REPAIR (probe v8 -> v10, 41 fault rows).  Tree `GXEMUL-SEC/src/`, HEAD `83df95c` + the uncommitted round.  2026-09-06, ~11:35.  SHORT BY DESIGN: one diff, one table, one question.

## CONTEXT AND VOCABULARY
An ordinary correctness review of an open-source machine emulator's CPU model (GXemul 0.7.0, hardened fork): the MC88100
exception-delivery path in `cpu_m88k.c` and its detector `regress/m88k_exc_probe.py`.  The "guest" is the operating system inside the
emulator.  Plain engineering vocabulary.  **If you cannot read files that is expected -- every fact is inlined; name any premise you
cannot settle rather than guessing.**  Tree under review: `GXEMUL-SEC/src/` (three pristine-2021 copies under the project root are NOT
this fork).  **VERDICT LINE FIRST.**  Cite by grep anchor.  `python3` in git-bash is a Windows Store stub; a file-reading seat that
needs Python uses `C:\Users\User00\AppData\Local\Programs\Python\Python312\python.exe`.

## WHY A SEVENTH PASS, AND WHAT CLOSES IT
The repair-chain rule: a repair made in response to a pass owes its own pass, scoped to THAT diff; the chain closes on the first VALID
pass that finds zero floor breaches surviving adjudication, with the denominator stated; when consecutive passes find breaches of one
CLASS the next repair closes the class, not the cell.  Pass 6 (v8, 36 rows; codex, deepseek, minimax, grok, kimi answered; glm BURNED;
Opus 5 and Fable 5 walled until 12:50pm America/Chicago -- SEAT FAILURES, so every closure here is PROVISIONAL on their re-fire; agy
deliberately not fired) found FIVE cells, all measured as 36/36 sweeps of v8 in table 10 and all closed in one repair:
* **codex** -- switch 1's ERROR arm is its own predicate: a frozen tb1 naming 10 enters switch 1 AS ERROR (no row did; the err* rows enter
  under their original classes and become ERROR after the fallback), so `implemented = !(PSR & SFRZ)` there swept.  Row `trapfrozen10`.
  Also: **a gate regression of this round's own making** -- the three check lines added that morning carried a LITERAL backslash-n between
  arguments, so `check()` would have compared the wrong pair and failed on correct output.  Repaired before any gate ran.
* **kimi** -- the {fallback predicate} x {PSR bit} CLASS: pass 5 closed only the MODE cell; `&& (PSR & IND)` and `&& !(PSR & C)` swept because
  every fallback-reaching row had IND set and C clear -> rows `resid50ind`, `resid50c` (with usfu1 and sfu1h, every settable PSR bit now
  has both sides at the fallback; MXM and BO cannot be set by `stcr` without stopping the cpu -- disclosed).  The window's NEAR bound:
  `vector >= 12 &&` swept (no row named 11..49) -> row `resid11`.  No frozen USER trap rowed: `!is_trap || vector >= 128` swept -> row
  `trapfrozen128`.  And **the class-10 "observationally identical" disclosure was FALSE for the composite**: the re-route arm prints
  `[ SFRZ already set in PSR => ERROR ]` (a plain print in this fork) and the exempt arm does not -- into the very transcript the probe
  reads.  -> the **refatal channel**: the five err* rows must SEE that line and the eight trapfrozen* rows must NOT.
* **deepseek** -- vectors 0..3's switch-1 arms are unrowed: the disclosed hardware-event class (m88kexchwtraps), stays disclosed.  Its second
  point taken: glm's "[115,128]" was off by one at the top; the shrink VALUES are 115..127 -- wording corrected.
* **minimax, grok** -- CLOSE; grok's two L4s applied (the gate's HEAD narration; the working tree running ahead of the shipped probe mid-repair).
This pass closes if it finds zero floor breaches surviving adjudication in the (d) enumeration of the shipped composite.

## SETTLED PREMISES, RE-INLINED (each a QUESTION if you can check it)
1. `m88k_psl.h`: MODE 0x80000000, C 0x10000000, SFD1 0x00000008, MXM 0x00000004, IND 0x00000002, SFRZ 0x00000001.  Reset PSR 0x80000002.
2. Order inside `m88k_exception()`: switch 1 (class -> `implemented`); the FALLBACK `if (vector < M88K_EXCEPTION_USER_TRAPS_START (128) &&
   !implemented)` -> `unimplemented vector=0x%03x`, every cpu stopped, `return`; THEN the SFRZ re-route `if (PSR & SFRZ) { if (!is_trap) {
   vector = ERROR; fatal("[ SFRZ already set in PSR => ERROR ]\n"); } update_shadow_regs = false; }`; then the common path; then the tail switch
   (labels per class; its `default:` prints `internal error` and stops the cpu -- reachable by no vector below 128 at HEAD-with-fix).
3. `fatal()` in this fork is a plain print with no early-out (`debugmsg.c`, anchor `fatal(`); it cannot be silenced by `-q`.  The line lands in
   the pty transcript the probe reads alongside the debugger prompt.
4. A TRAP (tb0/tb1/tcnd, is_trap = 1) taken with SFRZ set is exempted from the re-route and delivered to ITS OWN vector with frozen shadows;
   `stcr` stores the PSR verbatim (MODE-clear prints a WARNING and continues; MXM set or a BO flip stops the cpu); `divu` tests SFD1 before
   divisor == 0; `prom_call` raises UNIMPLEMENTED only in user mode; a user tb1 naming a vector < 128 raises PRIVILEGE.
5. The probe plants `br .` at every entry of every vector in VECTORS (now incl. 11 and 127), the row's handler words at `8 * handler_at`
   (default 0x40), a breakpoint at the expected entry, then `continue`; HALT = the fallback diagnostic naming the row's vector AND
   `All machines stopped.`; TAILHALT = `internal error` + stopped; STOP = anything else; bad=refatal = the re-route's diagnostic present where
   the exemption should hold or absent where the re-route fired.

## THE REPAIR DIFF (probe v8 -> v10; shipped md5 ee2c78c2 == the table-10 frozen copy), VERBATIM
```diff
--- GXEMUL-SEC/regress/artifacts/m88kexcdeliver/killtable8/m88k_exc_probe.frozen8.py	2026-09-06 10:28:29.365814800 -0500
+++ GXEMUL-SEC/regress/m88k_exc_probe.py	2026-09-06 11:31:29.650590500 -0500
@@ -50,8 +50,11 @@
   trapfrozen4/5/6/9   the same shape naming 4, 5, 6, 9: the {SFRZ set, is_trap} x {class} closure -- with only class 7 rowed,
              `if (!is_trap || vector == <class>)' re-routed that one frozen trap to ERROR unseen (codex, pass 5)  0x20/0x28/0x30/0x48
   trapfrozen8 first fault add 7fffffff+1 (handler planted at 0x48), handler tb1 0,r3,8: the frozen trap naming DIV0
-             delivers to 0x40 -- observable only because the handler is NOT at 0x40 for this row.  Class 10 is not
-             rowed: a frozen trap naming ERROR lands on 0x50 whether exempted or re-routed (equivalent by construction)  0x40
+             delivers to 0x40 -- observable only because the handler is NOT at 0x40 for this row.                     0x40
+  trapfrozen10 the same shape naming 10: for the RE-ROUTE mutant it is equivalent (0x50 either way), but switch 1's ERROR
+             arm is a separate predicate -- a frozen trap naming 10 enters switch 1 AS ERROR, which no other row does
+             (the err* rows enter under their own classes and become ERROR after the fallback); `implemented =
+             !(PSR & SFRZ)' there sends it to the fallback -- M_ERRORFRZOFF (codex, pass 6).  Expect 0x50, shadows frozen 0x50
   privsuptb  tb1 0,r3,6 (f003d806) in SUPERVISOR mode: the trap route into PRIVILEGE_VIOLATION.  privtb is
              NOT that route -- the user-mode filter in X(tb0) raises PRIVILEGE with is_trap == 0, so
              `implemented = !is_trap' on the PRIVILEGE arm left priv AND privtb green (codex, glm: pass 2)  0x30
@@ -63,9 +66,19 @@
              The interior pins were resid50 (50) and sfu1h (114: its nested SFU1 halts at the fallback), so a shrink of the
              bound to any N in (114, 128) escaped BY CONSTRUCTION (measured: `< 127' 29/29 on v5, `< 51' 28/29 -- sfu1h saw
              that one), and usertb (128, just outside) pins only that 128 is not halted: the accept-row-at-the-LAST-slot
-             rule (deepseek and glm, pass 5, from the packet alone; glm named the interval exactly).  EXPECTED RESULT = HALT
+             rule (deepseek and glm, pass 5, from the packet alone; glm's [115,128] named it -- the shrink VALUES are
+             115..127, 128 being the bound itself: deepseek, pass 6).  EXPECTED RESULT = HALT
              naming 0x07f; a shrunk bound delivers 127 to 0x3f8
              and the tail default stops the cpu instead (TAILHALT) -- mutants M_FALLBACK127, M_FALLBACK51.
+  resid11    tb1 0,r3,11 (f003d80b): the FIRST residual vector -- the fallback window's NEAR bound.  `vector >= 12 &&' on the
+             fallback swept 36/36 because no row named 11..49 (kimi, pass 6).  EXPECTED RESULT = HALT naming 0x00b        (0x58)
+  resid50ind stcr r5,cr1 (r5=0x80000000: IND CLEAR) then tb1 0,r3,50: the fallback with IND clear -- `&& (PSR & IND)' on the
+             fallback swept 36/36 because every fallback row had IND set.  EXPECTED RESULT = HALT naming 0x032          (0x190)
+  resid50c   stcr r5,cr1 (r5=0x90000002: C SET) then tb1 0,r3,50: the fallback with C set -- `&& !(PSR & C)' swept likewise.
+             With usfu1 (MODE clear, SFD1 set) and sfu1h (SFRZ set) these give every settable PSR bit both sides at the
+             fallback; MXM and BO cannot be set by stcr without stopping the cpu -- disclosed.  EXPECTED RESULT = HALT    (0x190)
+  trapfrozen128 div0 whose handler is tb1 0,r3,128: a frozen USER trap is exempted from the re-route like any trap and
+             delivered to 0x400 with frozen shadows -- `!is_trap || vector >= 128' swept 36/36 (kimi, pass 6)              0x400
   usfu1      stcr r5,cr1 (r5=0x0000000a: USER mode, SFD1 set) then a LEGAL divu r6,r5,r4: SFU1 (114) raised from USER
              mode reaches the fallback -- the only user-mode route to it (a user tb1 naming < 128 raises PRIVILEGE).
              Every other fallback row is supervisor, so `&& (PSR & MODE)' on the fallback predicate swept 29/29 (kimi,
@@ -111,7 +124,9 @@
              expected-HALT row (resid50, resid127, sfu1h, usfu1) must also see ITS vector named in the diagnostic
   TAILHALT   `internal error` printed and the machine stopped (the naive fix's shape)
   STOP       the machine stopped for another reason (e.g. a wrong vector base landed in zeros)
-  BADREGS    the entry breakpoint fired but a shadow-register/PSR/destination assert failed, or
+  BADREGS    the entry breakpoint fired but a shadow-register/PSR/destination assert failed, or (bad=refatal) the re-route's
+             `[ SFRZ already set in PSR => ERROR ]' line was present on a frozen-TRAP row or absent on a re-routed err* row --
+             the channel that separates the exemption arm from the re-route arm when both deliver to 0x50 (kimi, pass 6), or
              (bad=level) the transcript carried an `exception <CLASS>' line: the class printed at ERROR
              level, which the fork's default WARNING verbosity shows and INFO does not (kills M_LEVEL)
   (rows resid50, resid127, sfu1h and usfu1 EXPECT HALT: the fallback stopping the machine is the correct answer there)
@@ -135,12 +150,15 @@
 clear vs PSR MODE set); a MODE-conditioned `implemented' on any class that user mode can raise ({class} x
 {MODE} closure: DIV0 udiv0, PRIVILEGE priv/privtb, UNIMPLEMENTED unimpl, MISALIGNED umisalign, OVERFLOW uovf;
 BOUNDS and ERROR have no user-mode route -- a user tb1 naming them raises PRIVILEGE, and every handler runs
-supervisor; the FALLBACK predicate itself is pinned in user mode by usfu1, the one user-mode route to it); a class-conditioned SFRZ re-route ({SFRZ set, !is_trap} x {class}: MISALIGNED error, OVERFLOW errovf,
+supervisor; the FALLBACK predicate itself is pinned in user mode by usfu1, the one user-mode route to it); a class-conditioned SFRZ re-route, its diagnostic pinned both ways by the refatal channel ({SFRZ set, !is_trap} x {class}: MISALIGNED error, OVERFLOW errovf,
 DIV0 errdiv0 -- the handler clears SFD1 first, with it set the divu raises SFU1 instead (sfu1h) --, PRIVILEGE errpriv
 and UNIMPLEMENTED errunimpl -- the handler drops to user mode keeping SFRZ; BOUNDS and ERROR have no non-trap route,
 the frozen TRAP is trapfrozen); a wrong return address; the delay-slot else-arm's SFIP source (dslot, +16
-geometry); a trap re-routed to ERROR while frozen, per class ({SFRZ set, is_trap} x {class}: trapfrozen (7), trapfrozen4/5/6/8/9;
-class 10 is observationally identical under both arms -- disclosed; 0..3 are the hardware-event tails, m88kexchwtraps); a written destination.  Does NOT catch:
+geometry); a trap re-routed to ERROR while frozen, per class ({SFRZ set, is_trap} x {class}: trapfrozen (7), trapfrozen4/5/6/8/9/10/128 --
+class 10's re-route exemption is told from the re-route by the refatal channel (the pass-6 packet called it equivalent; kimi refuted
+that: the re-route prints a diagnostic the exemption does not) and switch 1's ERROR eligibility under SFRZ by trapfrozen10's
+HALT/DELIVER; 0..3 are the hardware-event tails, m88kexchwtraps); the fallback window's NEAR bound (resid11) and the fallback predicate
+conditioned on any settable PSR bit (resid50ind, resid50c, usfu1, sfu1h); a written destination.  Does NOT catch:
 fcr2/fcr4/fcr5; scoreboard (SSBR) bits; DMT contents; the post-delivery
 `cpu->delay_slot' write on the NON-delay path (M_DELAYALWAYS: needs a second UNFROZEN exception -- filed);
 vectors 0..3's tail arms (no row: M_TAILOFF -- filed); vectors 11..113 and 116..127 (fallback halts by
@@ -182,6 +200,7 @@
                                                  #   PRIVILEGE with is_trap == 0 (cpu_m88k_instr.c X(tb0)), so privtb is NOT the trap route
 TB1_0_R3_128 = 0xf003d880                        # tb1 0,r3,128 -- the first USER trap vector: delivered by the pre-existing code (entry 0x400)
 TB1_0_R3_50 = 0xf003d832                         # tb1 0,r3,50  -- a RESIDUAL vector (11..113): must still HALT (negative control vs D4)
+TB1_0_R3_11 = 0xf003d80b                         # tb1 0,r3,11  -- the FIRST residual vector: the fallback window's NEAR bound (kimi, pass 6)
 TB1_0_R3_127 = 0xf003d87f                        # tb1 0,r3,127 -- the LAST residual vector: pins the fallback window's FAR bound (< 128),
                                                  #   which resid50 (interior) and usertb (128, outside) cannot see (deepseek, glm, pass 5)
 #  The four *tb rows are the TRAP ROUTE into switch 1 for the classes whose other rows arrive by INSTRUCTION
@@ -205,7 +224,8 @@
 V_USER0 = 128
 V_RESID = 50
 V_RESID2 = 127
-VECTORS = (V_MISALIGN, V_UNIMPL, V_PRIV, V_BOUNDS, V_DIV0, V_OVF, V_ERROR, V_SFU1, V_USER0, V_RESID, V_RESID2)
+V_RESID0 = 11
+VECTORS = (V_MISALIGN, V_UNIMPL, V_PRIV, V_BOUNDS, V_DIV0, V_OVF, V_ERROR, V_SFU1, V_USER0, V_RESID, V_RESID2, V_RESID0)
 
 # name, program words after MARK, regs, vector, fault_pc, epsr, handler words at the div0 entry (None = br .)
 # [, handler_at: the vector whose entry the handler is planted at -- only trapfrozen8 sets it, to OVF (0x48), because its frozen
@@ -238,7 +258,12 @@
     ("trapfrozen8", [ADD_R2_R3_R4],             {"r3": 0x7fffffff, "r4": 1},     V_DIV0,     0x10004, PSR_RESET,
                  [TB1_0_R3_8], V_OVF),                        # first fault OVF (handler at 0x48); frozen tb1 naming 8 -> 0x40, observable
     ("trapfrozen9", [DIVU_R2_R3_R0],            {"r3": 0x11},                    V_OVF,      0x10004, PSR_RESET,
-                 [TB1_0_R3_9]),                               # frozen tb1 naming 9 -> 0x48.  Class 10: EQUIVALENT (0x50 either way), disclosed
+                 [TB1_0_R3_9]),                               # frozen tb1 naming 9 -> 0x48
+    ("trapfrozen128", [DIVU_R2_R3_R0],          {"r3": 0x11},                    V_USER0,    0x10004, PSR_RESET,
+                 [TB1_0_R3_128]),                             # a frozen USER trap: exempted from the re-route, delivered to 0x400 with frozen shadows
+    ("trapfrozen10", [DIVU_R2_R3_R0],           {"r3": 0x11},                    V_ERROR,    0x10004, PSR_RESET,
+                 [TB1_0_R3_10]),                              # frozen tb1 naming 10 -> 0x50: the re-route cannot see it (same target) but
+                                                              # switch 1's ERROR arm can (M_ERRORFRZOFF: eligibility conditioned on SFRZ -- codex, pass 6)
     ("ovfc",     [STCR_R5_CR1, ADD_R2_R3_R4],   {"r3": 0x7fffffff, "r4": 1, "r5": PSR_CARRY}, V_OVF, 0x10008, PSR_CARRY, None),
     ("indclr",   [STCR_R5_CR1, ADD_R2_R3_R4],   {"r3": 0x7fffffff, "r4": 1, "r5": PSR_INDCLR}, V_OVF, 0x10008, PSR_INDCLR, None),
     ("umisalign", [STCR_R5_CR1, LD_R2_R3_0],    {"r3": DATA + 1, "r5": PSR_USER}, V_MISALIGN, 0x10008, PSR_USER,  None),
@@ -256,6 +281,9 @@
     ("usertb",   [TB1_0_R3_128],                {"r3": 1},                       V_USER0,    0x10004, PSR_RESET, None),
     ("resid50",  [TB1_0_R3_50],                 {"r3": 1},                       V_RESID,    0x10004, PSR_RESET, None),
     ("resid127", [TB1_0_R3_127],                {"r3": 1},                       V_RESID2,   0x10004, PSR_RESET, None),
+    ("resid11",  [TB1_0_R3_11],                 {"r3": 1},                       V_RESID0,   0x10004, PSR_RESET, None),
+    ("resid50ind", [STCR_R5_CR1, TB1_0_R3_50],  {"r3": 1, "r5": PSR_INDCLR},     V_RESID,    0x10008, PSR_INDCLR, None),
+    ("resid50c", [STCR_R5_CR1, TB1_0_R3_50],    {"r3": 1, "r5": PSR_CARRY},      V_RESID,    0x10008, PSR_CARRY, None),
     ("usfu1",    [STCR_R5_CR1, DIVU_R6_R5_R4],  {"r5": PSR_USERSFD1, "r4": 0x10}, V_SFU1,    0x10008, PSR_USERSFD1, None),
     ("sfu1h",    [DIVU_R2_R3_R0],               {"r3": 0x10, "r5": 0x60, "r4": 0x10}, V_SFU1, 0x10004, PSR_RESET,
                  [DIVU_R6_R5_R4]),                             # handler at 0x40: a legal divu with SFD1 set -> SFU1 (114) -> fallback HALT
@@ -267,11 +295,18 @@
 #  NEGATIVE CONTROLS: rows whose CORRECT result is the fallback HALT.  They pin the boundary the diff keeps on purpose --
 #  vectors 11..113/116..127 and SFU1 (114/115) still stop the machine -- and separate the shipped D1 form from the rejected
 #  D4 (tail-default-delivers) and from delivering SFU1 (row m88kexcsfu1).  A mutant that delivers them turns these rows RED.
-EXPECT_RESULT = {"resid50": "HALT", "resid127": "HALT", "sfu1h": "HALT", "usfu1": "HALT"}
+EXPECT_RESULT = {"resid50": "HALT", "resid127": "HALT", "resid11": "HALT", "resid50ind": "HALT", "resid50c": "HALT", "sfu1h": "HALT", "usfu1": "HALT"}
 PSR_WANT = {"ovfc": 0x9000000b}                  # MODE | C | SFD1 | IND | SFRZ: carry PRESERVED through the exception path
 #  indclr wants the default PSR_EXC (0x8000000b): IND was CLEAR before the fault and must be SET by the exception path;
 #  EPSR keeps the pre-fault 0x80000000.  A write that drops `| M88K_PSR_IND' leaves 0x80000009 -> bad=psr.
-EXPECT_VECTOR = {"resid50": 0x032, "resid127": 0x07f, "sfu1h": 0x072, "usfu1": 0x072}   # the vector the fallback diagnostic must NAME for an expected-HALT row
+EXPECT_VECTOR = {"resid50": 0x032, "resid127": 0x07f, "resid11": 0x00b, "resid50ind": 0x032, "resid50c": 0x032, "sfu1h": 0x072, "usfu1": 0x072}
+#  refatal: the re-route prints `[ SFRZ already set in PSR => ERROR ]' (fatal() is a plain print in this fork); a re-routed non-trap row
+#  must SEE it, a frozen-trap row must NOT -- the channel that tells the exemption arm from the re-route arm when both land on 0x50
+#  (kimi, pass 6: the class-10 "equivalent" disclosure was false for the composite).
+REFATAL = "SFRZ already set in PSR"
+REFATAL_EXPECT = {"error": True, "errovf": True, "errdiv0": True, "errpriv": True, "errunimpl": True,
+                  "trapfrozen": False, "trapfrozen4": False, "trapfrozen5": False, "trapfrozen6": False, "trapfrozen8": False,
+                  "trapfrozen9": False, "trapfrozen10": False, "trapfrozen128": False}   # the vector the fallback diagnostic must NAME for an expected-HALT row
 
 class Sess:
     def __init__(self):
@@ -405,7 +440,7 @@
     else:
         want = dict(sxip=(fault_pc | XIP_V), psr=PSR_WANT.get(name, PSR_EXC), epsr=epsr_exp, r2=0xdeadbeef)
         if name in ("error", "trapfrozen", "errovf", "errdiv0", "errpriv", "errunimpl",
-                    "trapfrozen4", "trapfrozen5", "trapfrozen6", "trapfrozen8", "trapfrozen9"):
+                    "trapfrozen4", "trapfrozen5", "trapfrozen6", "trapfrozen8", "trapfrozen9", "trapfrozen10", "trapfrozen128"):
             # the second fault runs with SFRZ set: the shadows stay FROZEN at the first fault's values.  For
             # `trapfrozen' the second fault is a TRAP, which the manual (:8633-8636, 6.10 :10613-10614) exempts from
             # the ERROR re-route: it must deliver to ITS OWN vector (0x38), shadows still frozen.  M_SFRZTRAP sends it to 0x50.
@@ -419,6 +454,8 @@
         else:
             want.update(snip=((fault_pc + 4) | XIP_V), sfip=((fault_pc + 8) | XIP_V))
         bad = [k for k, v in want.items() if res.get(k) != v]
+        if name in REFATAL_EXPECT and ((REFATAL in tr) != REFATAL_EXPECT[name]):
+            bad.append("refatal")                      # the re-route's diagnostic present where the exemption should hold, or absent where the re-route fired
         if levelmsg:
             bad.append("level")
         res["result"] = "DELIVER" if not bad else "BADREGS"
```

Product code in this repair: NONE.  The gate (`regress/gate_m88k_rounding.sh`) pins `M88KEXC_RESULT=41/41`, the seven HALT rows (resid50,
resid127, resid11, resid50ind, resid50c, sfu1h, usfu1), the eight frozen-trap rows `trapfrozen(4|5|6|8|9|10|128)?` DELIVER, the two
user-mode rows, the four frozen-handler rows at 0x50, `bad=refatal` absent, `bad=level` absent, indclr, vbrtb, ovfc, the controls -- and its
three malformed check lines are repaired (real continuations).

## TABLE 10, MEASURED (`killtable10/`, frozen v10 md5 ee2c78c2 = shipped; PRETABLE10 written before and untouched; every mutant ALSO scored on
## the frozen v8 instrument so each escape is a measurement; BASE 41/41 before and after; clone `cmp`-clean, sentinel clear)
| mutant (exact edit) | on v8 (36 rows) | on v10 (41 rows) | red row on v10 |
|---|---|---|---|
| M_ERRORFRZOFF: switch 1's ERROR arm `implemented = !(PSR & SFRZ)` | **36/36 SWEEP** | 40/41 | trapfrozen10 HALT (naming 0x00a) |
| M_SFRZTRAP10: re-route `if (!is_trap \|\| vector == ERROR)` | **36/36** | 40/41 | trapfrozen10 BADREGS bad=refatal (both arms land on 0x50; only one prints) |
| M_FB_LO: fallback `vector >= 12 && ...` | **36/36** | 40/41 | resid11 TAILHALT (11 delivered to 0x58, the tail default) |
| M_FBIND: fallback `&& (PSR & IND)` | **36/36** | 40/41 | resid50ind TAILHALT (50 delivered to 0x190) |
| M_FBNOC: fallback `&& !(PSR & C)` | **36/36** | 40/41 | resid50c TAILHALT |
| M_SFRZTRAPUSER: re-route `if (!is_trap \|\| vector >= 128)` | **36/36** | 40/41 | trapfrozen128 STOP (re-routed to 0x50 instead of 0x400) |
HEAD with the final instrument: **7/41** (`probe_v10_head.out`: usertb DELIVER; resid50, resid127, resid11, resid50ind, resid50c, usfu1 HALT --
the fallback exists on HEAD; every other class HALTs; sfu1h STOP).  The fix on the rebuilt build/: **41/41** (`probe_v10_fix_final.out`).

## THE CLOSURES NOW IN THE CONTRACT (probe docstring)
* {class} x {PSR.MODE}: DIV0 udiv0; PRIVILEGE priv/privtb; UNIMPLEMENTED unimpl; MISALIGNED umisalign; OVERFLOW uovf; BOUNDS/ERROR no user route.
* {SFRZ set, non-trap} x {class}: error, errovf, errdiv0, errpriv, errunimpl; BOUNDS/ERROR no non-trap route.  Each must SEE the re-route's line.
* {SFRZ set, is_trap} x {class}: trapfrozen (7), trapfrozen4/5/6/8/9/10/128 -- each must NOT see the line; class 10's switch-1 eligibility under
  SFRZ pinned by trapfrozen10's HALT/DELIVER and its re-route exemption by refatal.  0..3 are the hardware-event tails (m88kexchwtraps).
* the fallback window: resid11 (near bound), resid50 / resid50ind / resid50c (interior, PSR default / IND clear / C set), sfu1h (114, SFRZ set),
  usfu1 (114 from user mode, SFD1 set), resid127 (far bound), usertb (128, outside).  MXM/BO: not settable by stcr -- disclosed.
* still disclosed: {class} x {delay_slot} beyond DIV0 (m88kdslotshadow); M_DELAYALWAYS; vectors 0..3's switch-1 and tail arms (m88kexchwtraps);
  DMT contents; SSBR; fcr2/4/5; first-exception SFU1 (m88kexcsfu1; SFU1_IMPRECISE 115 likewise); exact INFO; `implemented = is_trap` at
  BOUNDS/ERROR (equivalent today, m88ktbnd); the {MODE} x {SFRZ} x {class} triple for MISALIGNED/OVERFLOW/DIV0 (clause e); an exemption of a
  single residual vector other than 11/50/127 from the fallback (a value the body never tests as a case).

## THE DENOMINATOR THIS PASS CLAIMS CLOSED (tables 1-10, every score in a named log under regress/artifacts/m88kexcdeliver/)
12 reachable class x route cells; the fallback -- predicate / off / stop / near bound / far bound / outside / user mode / IND / C (M_REVERT
3/22, M_DELIVERALL 21/23, M_NOSTOP 21/23, M_FB_LO 40/41, M_FALLBACK127 29/30, M_FALLBACK51 28/30, M_FALLBACKLE 29/30, M_FALLBACK_NO_BOUND
28/29 (agy), M_FBSUPONLY 35/36, M_FBIND 40/41, M_FBNOC 40/41); switch 1's eligibility per class incl. ERROR under SFRZ (M_ERRORFRZOFF 40/41)
and the {class} x {MODE} closure (M_OVFSUPONLY 28/29, M_MISSUPONLY 28/29, M_NOMODE 19/23); the re-route -- source (M_SFRZ_EPSR_SWAP 23/29,
agy), is_trap polarity (M_SFRZTRAP 29/35, M_SFRZ_TRAP_UPDATE 28/29 agy), per-class non-trap (table 5), per-class trap incl. 10 and the user
trap (tables 7, 10: M_SFRZTRAP10 40/41, M_SFRZTRAPUSER 40/41), the diagnostic both ways (refatal); tail labels / bound / return (M_NAIVE
3/22, M_TAILLE 21/22, M_TAILRETURN 2/23, M_TAIL_ERROR_DROP 23/29, M_TAIL_BOUNDS_DROP 26/29); VBR (M_NOVBR 21/22, vbrtb anchored); PSR bits
SFRZ/IND/SFD1/MODE/C each measured on the common path (M_NOSFRZ 2/23, M_NOIND 22/23, M_NOSFD1 1/29, M_NOMODE 19/23, M_CARRYCLR 22/23); EPSR
(M_NOEPSR 2/23, M_EPSRAFTER 2/23); shadows (M_NOSHADOW 3/23, M_SNIPX 3/23, M_DSLOT / M_SFIPNOTGT / M_DSLOTSWAP 21/22); LEVEL (M_LEVEL 3/23);
vector scaling (M_VEC4 1/23, M_VEC7).

## THE ONE QUESTION
**Does a clean-sweep mutant exist in the (d) DEPENDS-ON enumeration of the SHIPPED COMPOSITE (the #502 fix + probe v10)?**  The enumeration:
predicates dominating the diff's edited lines up to the function boundary (switch 1's class labels; the fallback's `vector < 128 &&
!implemented`; the re-route's `PSR & SFRZ` and `is_trap`; the tail switch's labels), operand swaps drawn only from fields the guarded bodies
read, and joint cells where the body's own tests distinguish them.  Review EFFORT is scoped to the v8 -> v10 diff above; the FLOOR question is
asked of the composite.  If you find one, give the exact edit and the row that should have caught it; if none, CLOSE with YOUR OWN
denominator.  Second question, with the count named: of the pass-7 dispositions (five row closures, one channel, one disclosure withdrawn
(class 10), one gate repair, one interval wording, the deepseek 0..3 class kept disclosed), WHICH IS WRONG?

VERDICT LINE FIRST (CLOSE THE CHAIN / ONE MORE REPAIR: <which> / DO NOT SHIP), then the answer to the one question with its denominator,
then anything else, under a page.
