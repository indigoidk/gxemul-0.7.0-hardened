# PASS 6 -- `m88kexcdeliver` (#502): the closing pass on the PASS-5 REPAIR (probe v5 -> v8, 36 fault rows).  Tree `GXEMUL-SEC/src/`, HEAD `83df95c` + the uncommitted round.  2026-09-06, ~10:05.  SHORT BY DESIGN: one diff, two tables, one question.

## CONTEXT AND VOCABULARY
An ordinary correctness review of an open-source machine emulator's CPU model (GXemul 0.7.0, hardened fork): the MC88100
exception-delivery path in `cpu_m88k.c` and its detector `regress/m88k_exc_probe.py`.  The "guest" is the operating system inside the
emulator.  Plain engineering vocabulary.  **If you cannot read files that is expected -- every fact is inlined; name any premise you
cannot settle rather than guessing.**  Tree under review: `GXEMUL-SEC/src/` (three pristine-2021 copies under the project root are NOT
this fork).  **VERDICT LINE FIRST.**  Cite by grep anchor.  `python3` in git-bash is a Windows Store stub; a file-reading seat that
needs Python uses `C:\Users\User00\AppData\Local\Programs\Python\Python312\python.exe`.

## WHY A SIXTH PASS, AND WHAT CLOSES IT
The repair-chain rule: a repair made in response to a pass owes its own pass, scoped to THAT diff; the chain closes on the first VALID
pass that finds zero floor breaches surviving adjudication, with the denominator stated; when consecutive passes find breaches of one
CLASS the next repair closes the class, not the cell.  Pass 5 (v5, 29 rows) found THREE cells, all now closed in one repair:
* **the fallback window's FAR bound** -- deepseek and glm (packet-fed, independently): rows pinned only the interior (resid50 at 50,
  sfu1h at 114) and the outside (usertb at 128), so shrinking `vector < 128` to any N in (114, 128) escaped by construction.  agy, fired
  as the MEASURING seat with both Anthropic seats walled, built `vector < 127` and scored it 29/29 on v5.  Row `resid127` closes it.
* **frozen TRAPS per class** -- codex: `{SFRZ set, is_trap} x {class}` was rowed only for class 7 (trapfrozen); `if (!is_trap ||
  vector == <class>)` re-routed one frozen trap to ERROR unseen.  Rows trapfrozen4/5/6/8/9 close it; class 10 is observationally
  identical under both arms (its own vector IS the re-route target) and is disclosed.
* **the fallback's MODE cell** -- kimi, MEASURED in its own clone: `&& (PSR & MODE)` on the fallback predicate swept 29/29 because
  every fallback-reaching row was supervisor; one row (`usfu1`: user mode with SFD1 set, a legal divu -> SFU1 -> HALT) closes it.
Pass-5 roster: eight fired (agy as measuring seat), and the two Anthropic Agent seats -- Opus 5 and Fable 5 -- DIED on an Anthropic
session limit (HTTP 429, resets 12:50pm America/Chicago) before answering: SEAT FAILURES, recorded by name.  Every closure this
pass reaches is therefore PROVISIONAL on that roster gap; the two seats are re-fired when the wall lifts and adjudicate as any other
finding (closure changes the licence, never the truth-value).  Verdicts of the seats that answered:
* **deepseek** -- the fallback bound `vector < 128` -> `< 127` sweeps 29/29 because no row names vector 127; row owed: a supervisor tb1 naming 127 expecting HALT.  Found from the packet alone; measured true (killtable6: 29/29 on v5).  (panel.sh's seat check scored it CHECK (no verdict token): the answer opens 'ONE MORE REPAIR:' without the word VERDICT -- a format miss, not a failure.)
* **glm** -- the same class, stated exactly: the bound is pinned only on [115,128] (sfu1h at 114 is the upper interior pin), so a shrink into (114,128) escapes; row: tb0/tb1 naming 0x7f expecting HALT naming 0x07f.
* **minimax** -- called the fallback-threshold class a clean sweep by construction, not a floor breach.  WRONG on that point: the fallback predicate dominates the tail labels the diff added and its constant is a body-tested partition of `vector`; one row (resid127) kills the shrink, so it was a floor cell.
* **grok** -- every disposition holds; three records named: the gate check title still said 23 fault rows while the pin said 29/29 (fixed), OUTSTANDING_BUGS attributed the delay-slot shadow values to Table 6-3 (fixed), and the CHANGELOG folded m88ksfrzfatal into (vii)'s count of three (fixed).  Did not find the fallback-bound cell.
* **codex** -- {SFRZ set, is_trap} x {class} was rowed only for class 7 (trapfrozen); `if (!is_trap || vector == <class>)` re-routes one frozen trap unseen.  Prescribed trapfrozenovf and closure of the six cells.  Also: the m88ksfrzfatal filing said seven more classes reach the fatal(); five do (BOUNDS and ERROR are trap-only) -- corrected.  Verdicts held on the eleven dispositions otherwise.
* **agy** -- FIRED AS THE MEASURING SEAT (owner ruling: reserved for measurement) with both Anthropic seats walled -- MEASURED in a WSL scratch clone on the v5 probe: M_FALLBACK127 (`vector < 127`) 29/29 SWEEP, M_FALLBACK_NO_BOUND 28/29 (usertb), M_SFRZ_EPSR_SWAP 23/29, M_SFRZ_TRAP_UPDATE 28/29 (trapfrozen), M_TAIL_ERROR_DROP 23/29, M_TAIL_BOUNDS_DROP 26/29; BASE 29/29 both ends.  Verdict ONE MORE REPAIR: row resid127.
* **opus5** -- DIED before measuring on an Anthropic session limit (HTTP 429, resets 12:50pm America/Chicago), the shared-service class again; its clone /tmp/gxopus502p5 had built the baseline and no table ran.  agy took the measuring role (above).
* **fable5** -- DIED on the same 429 at the same minute (both Anthropic seats behind one service).  To be re-fired when the wall lifts; until then the main loop adjudicates (documented fallback) and every closure here is PROVISIONAL on that roster gap.
* **kimi** -- and it MEASURED (a WSL scratch clone of build/, the frozen v5 probe): M_SFRZTBMIS (`if (!is_trap || vector == MISALIGNED_ACCESS)`) 29/29 on v5 -- the trap hemisphere of {SFRZ set} x {is_trap} x {class}, the same class codex named and v7 closes (its own repair row trapfrzmis = trapfrozen4; it also noted class 8 needs a non-div0 first fault, which v7's handler_at does).  Second, disclosure-adjacent, measured 29/29: M_FBSUPONLY -- the fallback predicate conditioned on MODE; every fallback-reaching row was supervisor; one row closes it (user mode with SFD1 set, a legal divu -> SFU1 -> HALT naming 0x072; the mutant delivers to 0x390 and the #if 0'd SFU1 tail arm turns it into TAILHALT) -> v8 row usfu1.  Wrong disposition named: the contract implied the class-conditioned re-route family was settled while its trap side had one row.  Artifacts kimi_p5/.

Product code in this repair: NONE (the fix and its pass-4 comment corrections are unchanged; `cpu_m88k.c` is byte-identical to the
pass-5 packet's, two-part clearance CLEAN + FRESH on build/, build-asan/ and the WSL tree at 09:01).

## SETTLED PREMISES, RE-INLINED (each a QUESTION if you can check it)
1. `m88k_psl.h`: MODE 0x80000000, SFD1 0x00000008, MXM 0x00000004, IND 0x00000002, SFRZ 0x00000001.  Reset PSR 0x80000002.
2. Order inside `m88k_exception()`: switch 1 (class -> `implemented`); the FALLBACK `if (vector < M88K_EXCEPTION_USER_TRAPS_START &&
   !implemented)` (128) -> diagnostic `unimplemented vector=0x%03x`, every cpu stopped, `return`; THEN the SFRZ re-route
   `if (PSR & SFRZ) { if (!is_trap) { vector = ERROR; fatal(...); } update_shadow_regs = false; }`; then the common path (EPSR only when
   unfrozen; PSR |= SFRZ|IND|SFD1|MODE; shadows only when unfrozen; pc = VBR + 8*vector); then the tail switch (labels per class; its
   `default:` prints `internal error` and stops the cpu -- reachable by NO vector below 128 at HEAD-with-fix, since every class 0..10 has
   a label and 11..127 return at the fallback).
3. Because the fallback RETURNS, its predicate DOMINATES the tail labels the #502 diff added, and its constant 128 is a body-tested
   partition of `vector` -- which is why the far-bound shrink is a (d) floor cell and not clause-(e) debt (minimax read it the other way
   on pass 5).
4. A TRAP (tb0/tb1/tcnd, is_trap = 1) taken with SFRZ set is exempted from the ERROR re-route and delivered to ITS OWN vector with the
   shadows frozen (UM 6.10); `stcr` stores the PSR verbatim, so a handler may clear SFD1 or MODE while keeping SFRZ; `divu` tests SFD1
   before divisor == 0; `prom_call` raises UNIMPLEMENTED only in user mode; a user-mode tb1 naming a vector < 128 raises PRIVILEGE.
5. The probe plants `br .` at every entry of every vector in its VECTORS tuple (both tables when VBR is relocated), the row's handler
   words at `8 * handler_at` (default DIV0 = 0x40), a breakpoint at the expected entry, then `continue` with a 6 s grace; HALT = the
   fallback diagnostic naming the row's vector AND `All machines stopped.`; TAILHALT = `internal error` + stopped; STOP = anything else.

## THE REPAIR DIFF (probe v5 -> v8; shipped md5 e550e3fe == the table-8 frozen copy), VERBATIM
```diff
--- GXEMUL-SEC/regress/artifacts/m88kexcdeliver/killtable5/m88k_exc_probe.frozen5.py	2026-09-06 08:59:26.933375700 -0500
+++ GXEMUL-SEC/regress/m88k_exc_probe.py	2026-09-06 10:28:29.435906700 -0500
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
@@ -46,6 +47,11 @@
   trapfrozen div0 whose handler at 0x40 is tb1 0,r3,7 (r3=0x11): a TRAP with SFRZ already set is NOT
              re-routed to ERROR (UM :8633-8636, 6.10 :10613-10614) -- it delivers to 0x38 with the
              shadows still frozen.  `if (!is_trap)' -> `if (true)' was a 10/10 escape (Opus, pass 2)  0x38
+  trapfrozen4/5/6/9   the same shape naming 4, 5, 6, 9: the {SFRZ set, is_trap} x {class} closure -- with only class 7 rowed,
+             `if (!is_trap || vector == <class>)' re-routed that one frozen trap to ERROR unseen (codex, pass 5)  0x20/0x28/0x30/0x48
+  trapfrozen8 first fault add 7fffffff+1 (handler planted at 0x48), handler tb1 0,r3,8: the frozen trap naming DIV0
+             delivers to 0x40 -- observable only because the handler is NOT at 0x40 for this row.  Class 10 is not
+             rowed: a frozen trap naming ERROR lands on 0x50 whether exempted or re-routed (equivalent by construction)  0x40
   privsuptb  tb1 0,r3,6 (f003d806) in SUPERVISOR mode: the trap route into PRIVILEGE_VIOLATION.  privtb is
              NOT that route -- the user-mode filter in X(tb0) raises PRIVILEGE with is_trap == 0, so
              `implemented = !is_trap' on the PRIVILEGE arm left priv AND privtb green (codex, glm: pass 2)  0x30
@@ -53,6 +59,18 @@
              0x400.  Pins the tail switch's `< USER_TRAPS_START' guard: `<=' sends 128 into the tail
              default and stops the cpu (codex's one-character escape, pass 2)                       0x400
   resid50    tb1 0,r3,50 (f003d832): a residual vector.  EXPECTED RESULT = HALT (the fallback, by design).
+  resid127   tb1 0,r3,127 (f003d87f): the LAST residual vector -- pins the fallback window's FAR bound (`vector < 128').
+             The interior pins were resid50 (50) and sfu1h (114: its nested SFU1 halts at the fallback), so a shrink of the
+             bound to any N in (114, 128) escaped BY CONSTRUCTION (measured: `< 127' 29/29 on v5, `< 51' 28/29 -- sfu1h saw
+             that one), and usertb (128, just outside) pins only that 128 is not halted: the accept-row-at-the-LAST-slot
+             rule (deepseek and glm, pass 5, from the packet alone; glm named the interval exactly).  EXPECTED RESULT = HALT
+             naming 0x07f; a shrunk bound delivers 127 to 0x3f8
+             and the tail default stops the cpu instead (TAILHALT) -- mutants M_FALLBACK127, M_FALLBACK51.
+  usfu1      stcr r5,cr1 (r5=0x0000000a: USER mode, SFD1 set) then a LEGAL divu r6,r5,r4: SFU1 (114) raised from USER
+             mode reaches the fallback -- the only user-mode route to it (a user tb1 naming < 128 raises PRIVILEGE).
+             Every other fallback row is supervisor, so `&& (PSR & MODE)' on the fallback predicate swept 29/29 (kimi,
+             pass 5, MEASURED).  EXPECTED RESULT = HALT naming 0x072; the mutant delivers to 0x390 and the #if 0'd SFU1
+             tail arm makes that TAILHALT -- mutant M_FBSUPONLY                                                (0x390)
              Negative control: the shipped form must NOT deliver it (rejected D4 would)             (0x190)
   sfu1h      div0 whose handler at 0x40 is a LEGAL divu r6,r5,r4: with SFD1 set the divide raises
              SFU1_PRECISE (114), which halts at the FALLBACK (it runs before the SFRZ re-route).  EXPECTED
@@ -90,13 +108,13 @@
 RESULT per fault row (the classifier tests the STOP channel before pc, deliberately: the naive fix
 sets pc = entry and THEN stops, so pc alone cannot tell it from delivery):
   HALT       `unimplemented vector=` printed AND the machine stopped (both observed, pass 3); an
-             expected-HALT row (resid50, sfu1h) must also see ITS vector named in the diagnostic
+             expected-HALT row (resid50, resid127, sfu1h, usfu1) must also see ITS vector named in the diagnostic
   TAILHALT   `internal error` printed and the machine stopped (the naive fix's shape)
   STOP       the machine stopped for another reason (e.g. a wrong vector base landed in zeros)
   BADREGS    the entry breakpoint fired but a shadow-register/PSR/destination assert failed, or
              (bad=level) the transcript carried an `exception <CLASS>' line: the class printed at ERROR
              level, which the fork's default WARNING verbosity shows and INFO does not (kills M_LEVEL)
-  (rows resid50 and sfu1h EXPECT HALT: the fallback stopping the machine is the correct answer there)
+  (rows resid50, resid127, sfu1h and usfu1 EXPECT HALT: the fallback stopping the machine is the correct answer there)
   DELIVER    entry breakpoint fired, machine running, and every assert holds:
              pc == entry, SXIP == fault_pc|V, SNIP, SFIP, PSR == 0x8000000b (SFRZ|IND|SFD1|MODE),
              EPSR == the pre-fault PSR (0x80000002 supervisor rows; 0x00000002 user-mode rows),
@@ -108,7 +126,8 @@
 `M88KEXC_SELFTEST=OK|FAIL`, `M88KEXC_DONE`.  Set M88KEXC_VERBOSE=1 for transcripts.
 
 CONTRACT (clause e): catches a class returned to the fallback (HALT) by either route (instruction rows
-and the *tb trap rows); a class reaching the tail default (TAILHALT); a wrong vector SCALING (M_VEC4,
+and the *tb trap rows); a SHRUNK fallback window (resid127 pins the far bound: `< 128' -> `< 127' or `< 51' both deliver 127 to the
+tail default, TAILHALT; usertb pins that 128 is outside it, resid50 the interior); a class reaching the tail default (TAILHALT); a wrong vector SCALING (M_VEC4,
 M_VEC7: STOP) and a DROPPED vector base (vbrtb: STOP); a stale SXIP/SNIP/SFIP; a wrong PSR, including a
 cleared carry (ovfc); a dropped IND (indclr); the debugmsg LEVEL regression to ERROR/WARNING (bad=level on any
 delivered row: those print at the post-startup WARNING floor, INFO and DEBUG do not -- so exact INFO is NOT pinned,
@@ -116,11 +135,12 @@
 clear vs PSR MODE set); a MODE-conditioned `implemented' on any class that user mode can raise ({class} x
 {MODE} closure: DIV0 udiv0, PRIVILEGE priv/privtb, UNIMPLEMENTED unimpl, MISALIGNED umisalign, OVERFLOW uovf;
 BOUNDS and ERROR have no user-mode route -- a user tb1 naming them raises PRIVILEGE, and every handler runs
-supervisor); a class-conditioned SFRZ re-route ({SFRZ set, !is_trap} x {class}: MISALIGNED error, OVERFLOW errovf,
+supervisor; the FALLBACK predicate itself is pinned in user mode by usfu1, the one user-mode route to it); a class-conditioned SFRZ re-route ({SFRZ set, !is_trap} x {class}: MISALIGNED error, OVERFLOW errovf,
 DIV0 errdiv0 -- the handler clears SFD1 first, with it set the divu raises SFU1 instead (sfu1h) --, PRIVILEGE errpriv
 and UNIMPLEMENTED errunimpl -- the handler drops to user mode keeping SFRZ; BOUNDS and ERROR have no non-trap route,
 the frozen TRAP is trapfrozen); a wrong return address; the delay-slot else-arm's SFIP source (dslot, +16
-geometry); a trap re-routed to ERROR while frozen (trapfrozen); a written destination.  Does NOT catch:
+geometry); a trap re-routed to ERROR while frozen, per class ({SFRZ set, is_trap} x {class}: trapfrozen (7), trapfrozen4/5/6/8/9;
+class 10 is observationally identical under both arms -- disclosed; 0..3 are the hardware-event tails, m88kexchwtraps); a written destination.  Does NOT catch:
 fcr2/fcr4/fcr5; scoreboard (SSBR) bits; DMT contents; the post-delivery
 `cpu->delay_slot' write on the NON-delay path (M_DELAYALWAYS: needs a second UNFROZEN exception -- filed);
 vectors 0..3's tail arms (no row: M_TAILOFF -- filed); vectors 11..113 and 116..127 (fallback halts by
@@ -138,6 +158,7 @@
 PSR_USER = 0x00000002           # IND only: what the user-mode rows write via stcr
 PSR_FRZSUP = 0x80000003         # MODE | IND | SFRZ, SFD1 CLEAR: a frozen handler that wants its divu to raise DIV0, not SFU1
 PSR_FRZUSER = 0x00000003        # IND | SFRZ, MODE CLEAR: a frozen handler dropping to user mode (PRIVILEGE / UNIMPLEMENTED routes)
+PSR_USERSFD1 = 0x0000000a       # IND | SFD1, MODE CLEAR: user mode with the FPU disabled -- a legal divu raises SFU1 (kimi, pass 5)
 
 def tri(sub, d, s1, s2):
     return 0xf4000000 | (d << 21) | (s1 << 16) | (sub << 8) | s2
@@ -161,6 +182,8 @@
                                                  #   PRIVILEGE with is_trap == 0 (cpu_m88k_instr.c X(tb0)), so privtb is NOT the trap route
 TB1_0_R3_128 = 0xf003d880                        # tb1 0,r3,128 -- the first USER trap vector: delivered by the pre-existing code (entry 0x400)
 TB1_0_R3_50 = 0xf003d832                         # tb1 0,r3,50  -- a RESIDUAL vector (11..113): must still HALT (negative control vs D4)
+TB1_0_R3_127 = 0xf003d87f                        # tb1 0,r3,127 -- the LAST residual vector: pins the fallback window's FAR bound (< 128),
+                                                 #   which resid50 (interior) and usertb (128, outside) cannot see (deepseek, glm, pass 5)
 #  The four *tb rows are the TRAP ROUTE into switch 1 for the classes whose other rows arrive by INSTRUCTION
 #  (is_trap == 0).  Pass-2 seats (grok, deepseek, independently) predicted `if (!is_trap) implemented = true;'
 #  escapes the instruction rows for MISALIGNED/UNIMPL/DIV0/OVF; these rows are the ones that redden it (M_ISTRAP).
@@ -181,9 +204,12 @@
 V_SFU1 = 114
 V_USER0 = 128
 V_RESID = 50
-VECTORS = (V_MISALIGN, V_UNIMPL, V_PRIV, V_BOUNDS, V_DIV0, V_OVF, V_ERROR, V_SFU1, V_USER0, V_RESID)
+V_RESID2 = 127
+VECTORS = (V_MISALIGN, V_UNIMPL, V_PRIV, V_BOUNDS, V_DIV0, V_OVF, V_ERROR, V_SFU1, V_USER0, V_RESID, V_RESID2)
 
 # name, program words after MARK, regs, vector, fault_pc, epsr, handler words at the div0 entry (None = br .)
+# [, handler_at: the vector whose entry the handler is planted at -- only trapfrozen8 sets it, to OVF (0x48), because its frozen
+#  trap names DIV0 and a handler AT 0x40 would make the first fault's breakpoint mask the second event]
 ROWS = [
     ("div0",     [DIVU_R2_R3_R0],               {"r3": 0x10},                    V_DIV0,     0x10004, PSR_RESET, None),
     ("ovf",      [ADD_R2_R3_R4],                {"r3": 0x7fffffff, "r4": 1},     V_OVF,      0x10004, PSR_RESET, None),
@@ -203,6 +229,16 @@
     ("vbrtb",    [STCR_R5_CR7, TB1_0_R3_7],     {"r3": 1, "r5": VBR_TEST},       V_BOUNDS,   0x10008, PSR_RESET, None),
     ("trapfrozen", [DIVU_R2_R3_R0],             {"r3": 0x11},                    V_BOUNDS,   0x10004, PSR_RESET,
                  [TB1_0_R3_7]),                               # handler at 0x40: tb1 0,r3,7 with SFRZ set -> a TRAP is not re-routed to ERROR
+    ("trapfrozen4", [DIVU_R2_R3_R0],            {"r3": 0x11},                    V_MISALIGN, 0x10004, PSR_RESET,
+                 [TB1_0_R3_4]),                               # frozen tb1 naming 4 -> its own vector 0x20, shadows frozen (codex, pass 5)
+    ("trapfrozen5", [DIVU_R2_R3_R0],            {"r3": 0x11},                    V_UNIMPL,   0x10004, PSR_RESET,
+                 [TB1_0_R3_5]),                               # frozen tb1 naming 5 -> 0x28
+    ("trapfrozen6", [DIVU_R2_R3_R0],            {"r3": 0x11},                    V_PRIV,     0x10004, PSR_RESET,
+                 [TB1_0_R3_6]),                               # frozen tb1 naming 6 -> 0x30
+    ("trapfrozen8", [ADD_R2_R3_R4],             {"r3": 0x7fffffff, "r4": 1},     V_DIV0,     0x10004, PSR_RESET,
+                 [TB1_0_R3_8], V_OVF),                        # first fault OVF (handler at 0x48); frozen tb1 naming 8 -> 0x40, observable
+    ("trapfrozen9", [DIVU_R2_R3_R0],            {"r3": 0x11},                    V_OVF,      0x10004, PSR_RESET,
+                 [TB1_0_R3_9]),                               # frozen tb1 naming 9 -> 0x48.  Class 10: EQUIVALENT (0x50 either way), disclosed
     ("ovfc",     [STCR_R5_CR1, ADD_R2_R3_R4],   {"r3": 0x7fffffff, "r4": 1, "r5": PSR_CARRY}, V_OVF, 0x10008, PSR_CARRY, None),
     ("indclr",   [STCR_R5_CR1, ADD_R2_R3_R4],   {"r3": 0x7fffffff, "r4": 1, "r5": PSR_INDCLR}, V_OVF, 0x10008, PSR_INDCLR, None),
     ("umisalign", [STCR_R5_CR1, LD_R2_R3_0],    {"r3": DATA + 1, "r5": PSR_USER}, V_MISALIGN, 0x10008, PSR_USER,  None),
@@ -219,6 +255,8 @@
     ("udiv0",    [STCR_R3_CR1, DIVU_R2_R3_R0],  {"r3": PSR_USER},                V_DIV0,     0x10008, PSR_USER,  None),
     ("usertb",   [TB1_0_R3_128],                {"r3": 1},                       V_USER0,    0x10004, PSR_RESET, None),
     ("resid50",  [TB1_0_R3_50],                 {"r3": 1},                       V_RESID,    0x10004, PSR_RESET, None),
+    ("resid127", [TB1_0_R3_127],                {"r3": 1},                       V_RESID2,   0x10004, PSR_RESET, None),
+    ("usfu1",    [STCR_R5_CR1, DIVU_R6_R5_R4],  {"r5": PSR_USERSFD1, "r4": 0x10}, V_SFU1,    0x10008, PSR_USERSFD1, None),
     ("sfu1h",    [DIVU_R2_R3_R0],               {"r3": 0x10, "r5": 0x60, "r4": 0x10}, V_SFU1, 0x10004, PSR_RESET,
                  [DIVU_R6_R5_R4]),                             # handler at 0x40: a legal divu with SFD1 set -> SFU1 (114) -> fallback HALT
     ("live",     [DIVU_R2_R3_R4],               {"r3": 0x60, "r4": 0x10},        None,       None,    None,      None),
@@ -229,11 +267,11 @@
 #  NEGATIVE CONTROLS: rows whose CORRECT result is the fallback HALT.  They pin the boundary the diff keeps on purpose --
 #  vectors 11..113/116..127 and SFU1 (114/115) still stop the machine -- and separate the shipped D1 form from the rejected
 #  D4 (tail-default-delivers) and from delivering SFU1 (row m88kexcsfu1).  A mutant that delivers them turns these rows RED.
-EXPECT_RESULT = {"resid50": "HALT", "sfu1h": "HALT"}
+EXPECT_RESULT = {"resid50": "HALT", "resid127": "HALT", "sfu1h": "HALT", "usfu1": "HALT"}
 PSR_WANT = {"ovfc": 0x9000000b}                  # MODE | C | SFD1 | IND | SFRZ: carry PRESERVED through the exception path
 #  indclr wants the default PSR_EXC (0x8000000b): IND was CLEAR before the fault and must be SET by the exception path;
 #  EPSR keeps the pre-fault 0x80000000.  A write that drops `| M88K_PSR_IND' leaves 0x80000009 -> bad=psr.
-EXPECT_VECTOR = {"resid50": 0x032, "sfu1h": 0x072}   # the vector the fallback diagnostic must NAME for an expected-HALT row
+EXPECT_VECTOR = {"resid50": 0x032, "resid127": 0x07f, "sfu1h": 0x072, "usfu1": 0x072}   # the vector the fallback diagnostic must NAME for an expected-HALT row
 
 class Sess:
     def __init__(self):
@@ -293,7 +331,9 @@
 def fmt(v):
     return ("0x%08x" % v) if isinstance(v, int) else str(v)
 
-def run_row(name, prog, regs, vector, fault_pc, epsr_exp, handler, grace=6.0):
+def run_row(name, prog, regs, vector, fault_pc, epsr_exp, handler, grace=6.0, handler_at=None):
+    if handler_at is None:
+        handler_at = V_DIV0                              # the first fault of every two-fault row is DIV0 unless the row says otherwise
     s = Sess()
     if not s.wait_prompt(0, 60):
         s.close(); return dict(result="NOBOOT")
@@ -309,8 +349,8 @@
         s.send("put w 0x%x, 0x%08x" % (entry, SELF))
     if handler:
         for i, w in enumerate(handler):
-            s.send("put w 0x%x, 0x%08x" % (8 * V_DIV0 + 4 * i, w))
-        s.send("put w 0x%x, 0x%08x" % (8 * V_DIV0 + 4 * len(handler), SELF))
+            s.send("put w 0x%x, 0x%08x" % (8 * handler_at + 4 * i, w))
+        s.send("put w 0x%x, 0x%08x" % (8 * handler_at + 4 * len(handler), SELF))
     s.send("put w 0x%x, 0x%08x" % (DATA, 0x0badf00d))
     for r, v in regs.items():
         s.send("%s=0x%x" % (r, v))
@@ -364,7 +404,8 @@
         res["result"] = "STOP"          # ran past its grace without the entry breakpoint firing
     else:
         want = dict(sxip=(fault_pc | XIP_V), psr=PSR_WANT.get(name, PSR_EXC), epsr=epsr_exp, r2=0xdeadbeef)
-        if name in ("error", "trapfrozen", "errovf", "errdiv0", "errpriv", "errunimpl"):
+        if name in ("error", "trapfrozen", "errovf", "errdiv0", "errpriv", "errunimpl",
+                    "trapfrozen4", "trapfrozen5", "trapfrozen6", "trapfrozen8", "trapfrozen9"):
             # the second fault runs with SFRZ set: the shadows stay FROZEN at the first fault's values.  For
             # `trapfrozen' the second fault is a TRAP, which the manual (:8633-8636, 6.10 :10613-10614) exempts from
             # the ERROR re-route: it must deliver to ITS OWN vector (0x38), shadows still frozen.  M_SFRZTRAP sends it to 0x50.
@@ -395,8 +436,10 @@
     ok, psr = selftest()
     print("M88KEXC_SELFTEST=%s psr_at_reset=%s (want 0x80000002)" % ("OK" if ok else "FAIL", fmt(psr)), flush=True)
     delivered = 0; total = 0; controls_bad = []
-    for name, prog, regs, vector, fault_pc, epsr_exp, handler in ROWS:
-        res = run_row(name, prog, regs, vector, fault_pc, epsr_exp, handler)
+    for row in ROWS:
+        name, prog, regs, vector, fault_pc, epsr_exp, handler = row[:7]
+        handler_at = row[7] if len(row) > 7 else V_DIV0
+        res = run_row(name, prog, regs, vector, fault_pc, epsr_exp, handler, handler_at=handler_at)
         print("M88KEXC_ROW=%-9s RESULT=%-8s pc=%s sxip=%s snip=%s sfip=%s psr=%s epsr=%s r2=%s%s" % (
             name, res.get("result"), fmt(res.get("pc")), fmt(res.get("sxip")), fmt(res.get("snip")),
             fmt(res.get("sfip")), fmt(res.get("psr")), fmt(res.get("epsr")), fmt(res.get("r2")),
```

## THE GATE PINS (`regress/gate_m88k_rounding.sh`): `M88KEXC_RESULT=36/36`; resid50, resid127, sfu1h and usfu1 HALT; usertb's 128 outside the
## window is pinned by the existing `M_TAILLE`/`M_FALLBACKLE` shapes; six `trapfrozen*` rows DELIVER; the pass-5 pins unchanged.

## TABLE 6, MEASURED (`killtable6/`, frozen v6 md5 abfdf813; every mutant ALSO scored on the frozen v5 instrument to make the escape a
## measurement, not a prediction; BASE 30/30 before and after; clone re-baselined from SEC, sentinel clear)
| mutant (exact edit) | on v5 (29 rows) | on v6 (30 rows) | red rows on v6 |
|---|---|---|---|
| M_FALLBACK127: `vector < USER_TRAPS_START - 1` | **29/29 SWEEP** | 29/30 | resid127 TAILHALT (127 delivered to 0x3f8, the tail default stops the cpu) |
| M_FALLBACK51: `vector < 51` | 28/29 (sfu1h STOP: 114 no longer halted at the fallback, re-routed to ERROR) | 28/30 | resid127 TAILHALT, sfu1h STOP |
| M_FALLBACKLE: `vector <= USER_TRAPS_START` (control) | 28/29 (usertb HALT) | 29/30 | usertb HALT |
So the unpinned shrink interval on v5 was (114, 128), not (50, 128): sfu1h's nested SFU1 halting at the fallback is a second interior
pin -- glm's "[115,128]" was the exact statement; this brief's author first wrote (50, 128) and corrected it in place.

## TABLE 7, MEASURED (`killtable7/`, frozen v7 md5 b6eecc25 = shipped; every mutant also scored on the frozen v6 instrument; BASE 35/35
## before and after -- the `handler_at` extension left every old row's behaviour byte-identical)
| mutant (exact edit on the re-route: `if (!is_trap || vector == M88K_EXCEPTION_<class>)`) | on v6 (30 rows) | on v7 (35 rows) | red rows on v7 |
|---|---|---|---|
| M_SFRZTRAP4 (MISALIGNED_ACCESS) | **30/30 SWEEP** | 34/35 | trapfrozen4 STOP |
| M_SFRZTRAP5 (UNIMPLEMENTED_OPCODE) | **30/30** | 34/35 | trapfrozen5 STOP |
| M_SFRZTRAP6 (PRIVILEGE_VIOLATION) | **30/30** | 34/35 | trapfrozen6 STOP |
| M_SFRZTRAP8 (ILLEGAL_INTEGER_DIVIDE) | **30/30** | 34/35 | trapfrozen8 STOP |
| M_SFRZTRAP9 (INTEGER_OVERFLOW) | **30/30** | 34/35 | trapfrozen9 STOP |
| M_SFRZTRAP: `if (true)` (every trap re-routed; table 3's 21/22) | 29/30 | 29/35 | trapfrozen + the five above |
Each class-exemption mutant is killed by exactly its own row (single-killer cells, named in PRETABLE7 before the table).  HEAD with the
final instrument: **3/35** (`probe_v7_head.out`: usertb DELIVER, resid50 and resid127 HALT -- the fallback exists on HEAD; every other
class HALTs; sfu1h STOP).  The fix on the rebuilt build/: **35/35** (`probe_v7_fix_final.out`).
Records note: the driver logs of tables 6 and 7 print "RED resid127 HALT" under every mutant -- a stale expectation table in the DRIVER's
listing (`DRIVER_RED_LISTING_NOTE.txt`), not the probe; the M88KEXC_RESULT lines are the scores.  PRETABLE6 and PRETABLE7 were written
before their tables; both later had a dated correction APPENDED to the same file, which refreshed the mtime -- the order is asserted from
the session's sequence, and corrections go to separate files from now on.

## TABLE 8, MEASURED (`killtable8/`, frozen v8 md5 e550e3fe = shipped; each mutant also scored on the frozen v7 instrument; BASE 36/36)
| mutant | on v7 (35 rows) | on v8 (36 rows) | red row on v8 |
|---|---|---|---|
| M_FBSUPONLY: fallback `&& (PSR & MODE)` (kimi, pass 5, measured 29/29 on v5) | **35/35 SWEEP** | 35/36 | usfu1 TAILHALT (delivered to 0x390, the #if 0'd SFU1 tail arm falls to the default) |
| M_SFRZTRAP4 (= kimi's M_SFRZTBMIS; re-measured for the record) | 34/35 | 35/36 | trapfrozen4 STOP |
Row `usfu1`: `stcr r5,cr1` with r5 = 0x0000000a (USER mode, SFD1 set) then a LEGAL `divu r6,r5,r4` -> SFU1 (114) raised from user
mode reaches the fallback and HALTs naming 0x072 -- the only user-mode route to the fallback (a user tb1 naming < 128 raises
PRIVILEGE).  The {class} x {MODE} closure now names the FALLBACK predicate as well as the `implemented` arms.
HEAD with v8: **4/36** (`probe_v8_head.out`: usertb DELIVER; resid50, resid127 and usfu1 HALT -- the fallback exists on HEAD, so the
user-mode SFU1 halts there too; every other class HALTs).  The fix on the rebuilt build/: **36/36** (`probe_v8_fix_final.out`).

## THE CLOSURE, WRITTEN INTO THE CONTRACT (probe docstring)
* {class} x {PSR.MODE}: DIV0 udiv0; PRIVILEGE priv, privtb; UNIMPLEMENTED unimpl; MISALIGNED umisalign; OVERFLOW uovf.  BOUNDS/ERROR:
  no user route (a user tb1 naming them raises PRIVILEGE; every handler runs supervisor) -- disclosed.
* {SFRZ set, non-trap} x {class}: MISALIGNED error; OVERFLOW errovf; DIV0 errdiv0 (handler clears SFD1 first); PRIVILEGE errpriv and
  UNIMPLEMENTED errunimpl (handler drops to user mode keeping SFRZ).  BOUNDS/ERROR: no non-trap route -- disclosed.
* {SFRZ set, is_trap} x {class}: trapfrozen (7), trapfrozen4/5/6/8/9; class 10 observationally identical under both arms -- disclosed;
  0..3 are the hardware-event tails (m88kexchwtraps).
* the fallback window: resid50 (interior), sfu1h (114, interior via the nested SFU1), resid127 (the far bound), usertb (128, outside).
* still disclosed: {class} x {delay_slot} beyond DIV0 (m88kdslotshadow); M_DELAYALWAYS; vectors 0..3's tail arms; DMT contents;
  SSBR; fcr2/4/5; first-exception SFU1 (m88kexcsfu1); exact INFO; `implemented = is_trap` at BOUNDS/ERROR (equivalent today, m88ktbnd);
  the {MODE} x {SFRZ} x {class} triple for MISALIGNED/OVERFLOW/DIV0 (same re-route path as errpriv/errunimpl; MODE untested by the
  function -- clause (e)); an exemption of a single residual vector from the fallback (a value the body never tests as a case).

## THE DENOMINATOR THIS PASS CLAIMS CLOSED (tables 1-8)
12 reachable class x route cells; fallback predicate / off / stop / far bound / outside bound / user mode (M_REVERT 3/22, M_DELIVERALL
21/23, M_NOSTOP 21/23, M_FALLBACK127 29/30, M_FALLBACK51 28/30, M_FALLBACKLE 29/30, M_FALLBACK_NO_BOUND 28/29 by agy, M_FBSUPONLY 35/36); tail labels / bound /
return (M_NAIVE 3/22, M_TAILLE 21/22, M_TAILRETURN 2/23, M_TAIL_ERROR_DROP 23/29 and M_TAIL_BOUNDS_DROP 26/29 by agy); {SFRZ} x {is_trap}
four cells with frozen-shadow polarity both ways (M_SFRZTRAP 29/35, M_UPDSHADOWTRAP 22/23, M_ERRORDROP 21/22, M_SFRZ_TRAP_UPDATE 28/29 by
agy); {SFRZ, non-trap} x {class} five cells (table 5); {SFRZ, is_trap} x {class} six cells (table 7); {class} x {MODE} five cells (table 5
+ udiv0/priv/privtb/unimpl); the re-route's state source (M_SFRZ_EPSR_SWAP 23/29 by agy); VBR (M_NOVBR 21/22, vbrtb anchored); PSR bits
SFRZ/IND/SFD1/MODE/C each measured (M_NOSFRZ 2/23, M_NOIND 22/23, M_NOSFD1 1/29, M_NOMODE 19/23, M_CARRYCLR 22/23); EPSR (M_NOEPSR 2/23,
M_EPSRAFTER 2/23); shadows (M_NOSHADOW 3/23, M_SNIPX 3/23, M_DSLOT / M_SFIPNOTGT / M_DSLOTSWAP 21/22); LEVEL (M_LEVEL 3/23); vector
scaling (M_VEC4 1/23, M_VEC7).

## THE ONE QUESTION
**Does a clean-sweep mutant exist in the (d) DEPENDS-ON enumeration of the SHIPPED COMPOSITE (the #502 fix + probe v8)?**  The
enumeration: predicates dominating the diff's edited lines up to the function boundary (switch 1's class labels; the fallback's
`vector < 128 && !implemented`; the re-route's `PSR & SFRZ` and `is_trap`; the tail switch's labels), operand swaps drawn only from
fields the guarded bodies read, and joint cells where the body's own tests distinguish them (class x SFRZ x is_trap; the fallback
window's two bounds).  Review EFFORT is scoped to the v5 -> v8 diff above; the FLOOR question is asked of the composite.  If you find
one, give the exact edit and the row that should have caught it; if none, CLOSE with YOUR OWN denominator.  Second question, with the
count named: of the pass-6 dispositions (three class closures incl. the fallback's MODE cell, one harness extension, one disclosed
equivalent (class 10), one interval correction, one driver-listing note, one PRETABLE-order disclosure, one count correction (seven ->
five), three grok records), WHICH IS WRONG?

VERDICT LINE FIRST (CLOSE THE CHAIN / ONE MORE REPAIR: <which> / DO NOT SHIP), then the answer to the one question with its
denominator, then anything else, under a page.
