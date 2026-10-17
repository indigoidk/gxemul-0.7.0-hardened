# PASS 14 -- `m88kexcdeliver` (#502): review of REPAIR 13 (probe v20), with the close adjudication's findings shared

Four seats, by the owner's roster of 2026-10-16: Fable 5.1, GPT-6 Astra, Grok 4.7, GLM 5.3.  The other five (Opus, agy,
kimi, deepseek, minimax) are DELIBERATELY NOT FIRED under that roster.  This is an ordinary regression-detector coverage
review.  READ-ONLY: write nothing to any project tree.  The tree under review is `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC`
(HEAD 7b23b785 plus the uncommitted repair inlined below); ignore any other `src/` you find under the project root -- the
one at `C:/DocumentNoSnc/cc/GXEMUL/src/` is pristine 2021 upstream.  Everything a packet-fed seat needs is inlined; file-
reading seats may verify against `git show HEAD:<path>` and the working tree.

**Please do not simply ratify.**  Earlier today three of four seats ratified a 56-cell denominator, and the fourth showed it
omitted an axis the function TESTS; a measurement then confirmed it (section 1).  Check the premises, not just the arithmetic.

Open with your seat token -- `FABLE_M88KP14_20261016` / `ASTRA_M88KP14_20261016` / `GROK_M88KP14_20261016` /
`GLM_M88KP14_20261016` -- then ONE line: `VERDICT: CLOSE / DO NOT CLOSE (<one line>)`.

## 1. What happened since the close packet (each with its artifact under regress/artifacts/m88kexcdeliver/)

1. The close adjudication (`../adj_20261016/m88kexcdeliver/`): GPT-6 Astra, Grok 4.7 and GLM 5.3 ruled CLOSE on the 56-cell
   denominator; Fable 5.1 ruled DO NOT CLOSE -- the denominator omits `cpu->delay_slot`, which the delivery body tests, so
   {MISALIGN, UNIMPL, PRIV, OVF} x {delay slot set} were unrowed (only `dslot`, at DIV0, faulted in a slot).
2. MEASURED (`delayslot_20261016/`, scratch clone of HEAD 7b23b785): `implemented = !cpu->delay_slot;` at each of those four
   arms scored **59/59** on the shipped 59-row probe, every log byte-identical to BASE (md5 898eb0a7) -- a clean sweep at all
   four.  The polarity twins `implemented = cpu->delay_slot ? true : false;` scored OVF 50/59, MISALIGN 51/59, PRIV 53/59,
   UNIMPL 54/59 -- the per-arm row counts Fable had predicted from the row table.  Graded L2 (floor breach), repaired in-round.
3. REPAIR 13 = probe v20 (diff in section 3): four rows faulting IN A DELAY SLOT -- `dslotmisalign`, `dslotunimpl`, `dslotpriv`,
   `dslotovf`, each a `br.n +16` immediately before the faulting word, scored like `dslot` (the else-arm AS IMPLEMENTED); the
   gate pin 59/59 -> 63/63 plus a check that all five delay-slot rows deliver at their entries; the contract names the closure
   and discloses BOUNDS/ERROR x {delay slot}.  `repair13_20261016/PRETABLE.out` was written before table 16 ran (mtime order).
4. Records riding with it: two import-time asserts on `PSR_FRZUSER` / `PSR_FRZSUP` (negative-controlled: `assert_controls.out`);
   the probe comment's "58/58" corrected in place to 57/58; the m88ksfd1row ruling text; `derive_cells.py` taught the v19/v20
   rows and a delay-slot axis, `CELLCENSUS.out` regenerated (its v16 and v17/v18 grids are byte-identical to the old output).

## 2. Settled premises (warrants inline; challenge any of them)

* `m88k_exception(cpu, vector, is_trap)` (section 5, HEAD, untouched by this repair) TESTS, in its delivery path: `vector` (both
  switches), `!implemented` (the fallback, line 799), `PSR & SFRZ` (811), `is_trap` (816), and `cpu->delay_slot` (840 inside
  `if (update_shadow_regs)`, and 865 on every path that passes the fallback).  Every other PSR bit is copied to EPSR or ORed.
* In a delay slot every one of the seven trap-like arms takes the shadow branch's ELSE-arm (SNIP = pc+4, SFIP =
  delay_target): only DATA_ACCESS and INSTRUCTION_ACCESS have their own arms there.  `m88kdslotshadow` (filed) records that
  this else-arm returns wrong per the manual; the five `dslot*` rows pin it AS IMPLEMENTED and share ONE scoring branch, so
  that round re-pins all five in one place, before the code moves.
* MODE at BOUNDS/ERROR is unreachable (no instruction raises 7 or 10; a user `tb1` naming a vector below 128 raises
  PRIVILEGE with is_trap == 0; the re-route writes ERROR after switch 1) -- the warrant expires when `X(tbnd)` lands
  (row `m88ktbnd`).  SFRZ is invariant BY CONSTRUCTION inside both frozen sites (it is their guard).
* `trapfrozensfd1` runs its handler with `PSR_FRZSUP` = 0x80000003 (MODE set, SFD1 clear); `trapfrozenuser` with
  `PSR_FRZUSER` = 0x00000003 (MODE clear AND SFD1 clear), the constant `errpriv` / `errunimpl` also use.
* The probe launches `-E testm88k` with no `-C`, so every table measures an 88110 configuration; nothing in the exception path
  reads `cpu_type` (recorded since pass 8; pinning `-C 88100` is filed, not part of this repair).
* `mc88100.txt:3712-3728` (3.3.2 Delayed Branching) and `:9433-9440` (6.7.2 note 6, "instructions residing in the delay slot
  of a branch, jump, or a trap-taken instruction are never executed") are what the manual on disk says about delay slots;
  neither says whether a TRAP instruction may sit IN a delay slot.  `X(tb1)` carries no delay-slot guard, so the emulator
  reaches that case.

## 3. The repair -- `git diff` of the probe and the gate against HEAD 7b23b785 (9 hunks)

The records-only deriver change (`regress/artifacts/m88kexcdeliver/derive_cells.py`, +48/-4) is NOT inlined; its new
delay-slot output is in section 4.  File-reading seats: `git diff -- regress/artifacts/m88kexcdeliver/derive_cells.py`.

```diff
diff --git a/regress/gate_m88k_rounding.sh b/regress/gate_m88k_rounding.sh
index 31838d0c..5f829060 100644
--- a/regress/gate_m88k_rounding.sh
+++ b/regress/gate_m88k_rounding.sh
@@ -326,12 +326,12 @@ fi
 #  grew: every trap-like class stopped the machine.  With the final instrument the 7 are resid50, resid127,
 #  resid11, resid50ind, resid50c and usfu1, whose CORRECT answer is HALT, and the pre-existing user vector 128 (usertb); sfu1h reads STOP
 #  on HEAD because the FIRST divu halts on vector 0x008, not its own 0x072 -- probe10_head.out /
-#  probe_v3_head.out .. probe_v11_head.out) and the DETECTOR (59 fault rows + 2
+#  probe_v3_head.out .. probe_v11_head.out) and the DETECTOR (63 fault rows -- 59 until v20, 2026-10-16 -- + 2
 #  controls; kill tables killtable/, killtable2/, killtable3/, killtable4/ + killtable4b/
 #  (M_TAILRETURN), killtable5/ (the {class} x {MODE} and {SFRZ set, non-trap} x {class} closures), killtable6/ (the fallback far bound, resid127), killtable7/ (the frozen-TRAP rows per class), killtable8/ (the fallback in user mode, usfu1), killtable10/ (the frozen ERROR trap, the near bound, the fallback PSR-bit cells, the frozen user trap, the refatal channel; table 9 was folded into it), killtable11/ (the frozen traps naming the 0x1c2, MVMEPROM and 511 labels; the ERROR-arm-frozen and MISALIGNED-C representatives; the re-route x {IND, C} cells, errind/errc), killtable12/ (the re-route TRAP side x {IND, C}: both swept 46/46 before the rows existed), killtable13/ (the six previously-sweeping mutants, all killed), killtable14/ (grok's three predicted SER sweeps -- each 54/54 on the frozen v16 instrument and killed on v17 by its own row)
 #  under regress/artifacts/m88kexcdeliver/).  Only the detector half runs here.
 #
-#  The pins are NAMED so that deleting a row is visible: `M88KEXC_RESULT=59/59' pins the
+#  The pins are NAMED so that deleting a row is visible: `M88KEXC_RESULT=63/63' pins the
 #  denominator (a row that stops running shrinks it); resid50 and sfu1h are the two rows
 #  whose CORRECT answer is HALT -- they separate the shipped fix from a form that delivers
 #  every vector (the rejected D4) or SFU1 (row m88kexcsfu1); vbrtb is the one ANCHORED row
@@ -350,8 +350,14 @@ if ! grep -q "M88KEXC_DONE" "$EXCLOG"; then
 else
     check "m88k exc: CR parse self-test (PSR at reset == 0x80000002)" \
           "$(grep -c 'M88KEXC_SELFTEST=OK' "$EXCLOG")" "1"
-    check "m88k exc: 59 fault rows, all as expected (the denominator is the pin)" \
-          "$(grep -c 'M88KEXC_RESULT=59/59' "$EXCLOG")" "1"
+    check "m88k exc: 63 fault rows, all as expected (the denominator is the pin)" \
+          "$(grep -c 'M88KEXC_RESULT=63/63' "$EXCLOG")" "1"
+    #  v20, repair 13 (2026-10-16): {class} x {delay slot}.  Before it only DIV0 faulted in a delay slot, and the
+    #  form implemented = !cpu->delay_slot at MISALIGNED/UNIMPL/PRIV/OVF swept the 59-row probe clean at all four arms
+    #  (artifacts/m88kexcdeliver/delayslot_20261016/).  BOUNDS and ERROR in a slot need a trap instruction there,
+    #  which the manual does not settle -- disclosed in the probe's contract (repair13_20261016/, table 16).
+    check "m88k exc: a fault IN A DELAY SLOT is delivered at every class an instruction raises there (dslot 0x40, dslotmisalign 0x20, dslotunimpl 0x28, dslotpriv 0x30, dslotovf 0x48)" \
+          "$(grep -cE '^M88KEXC_ROW=(dslot +RESULT=DELIVER +pc=0x00000040|dslotmisalign +RESULT=DELIVER +pc=0x00000020|dslotunimpl +RESULT=DELIVER +pc=0x00000028|dslotpriv +RESULT=DELIVER +pc=0x00000030|dslotovf +RESULT=DELIVER +pc=0x00000048) ' "$EXCLOG")" "5"
     check "m88k exc: IND set by the exception path from a pre-fault PSR with IND clear (indclr)" \
           "$(grep -cE '^M88KEXC_ROW=indclr +RESULT=DELIVER .*psr=0x8000000b .*epsr=0x80000000' "$EXCLOG")" "1"
     check "m88k exc: user-mode MISALIGNED and OVERFLOW deliver (umisalign 0x20, uovf 0x48 -- the {class} x {MODE} closure)" \
diff --git a/regress/m88k_exc_probe.py b/regress/m88k_exc_probe.py
index ed843cdb..292083ce 100644
--- a/regress/m88k_exc_probe.py
+++ b/regress/m88k_exc_probe.py
@@ -35,6 +35,12 @@ rather than executing zeros, `breakpoint add <8*vector>`, `continue`, then `reg`
              `fip != nip + 4' arm say the else-arm returns WRONG (codex, grok, pass 2: the fallthrough executes
              before the target).  Pre-existing, out of this diff's scope, filed as m88kdslotshadow; when that round
              lands this row is RE-PINNED FIRST (oracle-correction rule: re-pin, measure HEAD red, then fix). ***
+  dslotmisalign/dslotunimpl/dslotpriv/dslotovf   v20 (repair 13, 2026-10-16): the same br.n +16 with the fault IN ITS
+             DELAY SLOT at the four other arms a guest INSTRUCTION can raise -- ld r2,r3,0 (r3 odd), prom_call and
+             ldcr r2,cr1 after stcr r3,cr1 (user mode), add 7fffffff+1.  `implemented = !cpu->delay_slot' at each of those
+             arms swept v19 59/59 (artifacts/m88kexcdeliver/delayslot_20261016/, predicted by Fable 5.1); each row
+             kills its own arm's form.  Scored like dslot (the else-arm, AS IMPLEMENTED): SNIP = fault+4,
+             SFIP = fault+12 = the branch's delay_target                                       0x20/0x28/0x30/0x48
   errortb    tb1  0,r3,10 (r3=1)      f003d80a  supervisor trap naming ERROR (10) directly -- the
              only route to switch 1's ERROR arm (the double-fault route enters at the re-route AFTER
              switch 1, so it cannot see that arm: M_ERRORDROP escaped the error row 9/9, table 1)  0x50
@@ -180,7 +186,14 @@ row is owed as its own revision with its own BASE run (codex, pass 8). ***) ({SF
 DIV0 errdiv0 -- the handler clears SFD1 first, with it set the divu raises SFU1 instead (sfu1h) --, PRIVILEGE errpriv
 and UNIMPLEMENTED errunimpl -- the handler drops to user mode keeping SFRZ; BOUNDS and ERROR have no non-trap route,
 the frozen TRAP is trapfrozen); a wrong return address; the delay-slot else-arm's SFIP source (dslot, +16
-geometry); a trap re-routed to ERROR while frozen, per class ({SFRZ set, is_trap} x {every switch-1 label a trap can NAME -- 0..3 are deliverable too and are unrowed, disclosed as
+geometry); a delay-slot-conditioned `implemented' on any class a guest INSTRUCTION can raise from a delay slot ({class} x
+{delay slot} closure, v20: DIV0 dslot, MISALIGNED dslotmisalign, UNIMPLEMENTED dslotunimpl, PRIVILEGE dslotpriv, OVERFLOW
+dslotovf -- `implemented = !cpu->delay_slot' at the four latter arms swept v19 59/59, delayslot_20261016/, and the body's own
+`if (cpu->delay_slot)' is what makes delay_slot a floor axis; BOUNDS and ERROR x {delay slot} need a TRAP INSTRUCTION IN A
+DELAY SLOT, which the MC88100 manual does not settle -- mc88100.txt:9433-9440 covers the slot OF a trap-taken instruction, not a
+trap in one -- so they are DISCLOSED with their measured escapes, M_DSNOT_BOUNDS and M_DSNOT_ERROR, table 16, and so is
+every trap instruction in a slot at the other five arms; multi-axis joints of delay slot with SFRZ, is_trap or a PSR bit stay
+clause (e)); a trap re-routed to ERROR while frozen, per class ({SFRZ set, is_trap} x {every switch-1 label a trap can NAME -- 0..3 are deliverable too and are unrowed, disclosed as
 m88kexchwtraps; the word EVERY overclaimed until v16}: trapfrozen (7),
 trapfrozen4/5/6/8/9/10/128/450/496/511 -- the ten labels 4..10, 128, 0x1c2, MVMEPROM_VECTOR, enumerated from switch 1's `case' list, plus
 the far edge of the user range (511) --
@@ -230,6 +243,14 @@ PSR_FRZUSER = 0x00000003        # IND | SFRZ: a frozen handler dropping to user
                                 # presents SFD1 clear as well.  A constant's comment that lists SOME of the bits it clears
                                 # reads like a complete decode and is not one.
 PSR_USERSFD1 = 0x0000000a       # IND | SFD1, MODE CLEAR: user mode with the FPU disabled -- a legal divu raises SFU1 (kimi, pass 5)
+#  v20 (Fable 5.1, 2026-10-16 four-seat adjudication of the close): the re-route's TRAP side has its SFD1-clear stimulus
+#  on TWO constants -- PSR_FRZUSER (trapfrozenuser: MODE clear AND SFD1 clear; shared with errpriv and errunimpl) and
+#  PSR_FRZSUP (trapfrozensfd1: MODE set, SFD1 clear; shared with errdiv0).  An edit such as PSR_FRZUSER 0x03 -> 0x0b
+#  keeps errpriv and errunimpl green and deletes one of those stimuli, and BASE alone would not notice.  A comment is
+#  memory; these fire at startup, before any session runs.
+PSR_BIT_MODE, PSR_BIT_SFD1 = 0x80000000, 0x00000008
+assert not (PSR_FRZUSER & (PSR_BIT_MODE | PSR_BIT_SFD1)), "PSR_FRZUSER must keep MODE and SFD1 clear (trapfrozenuser's cell)"
+assert (PSR_FRZSUP & PSR_BIT_MODE) and not (PSR_FRZSUP & PSR_BIT_SFD1), "PSR_FRZSUP must keep MODE set, SFD1 clear (trapfrozensfd1's cell)"
 PSR_FRZNOIND = 0x80000009       # MODE | SFD1 | SFRZ, IND CLEAR: a frozen handler that re-enables interrupts (grok, pass 7)
 PSR_FRZC = 0x9000000b           # C | MODE | SFD1 | IND | SFRZ: a frozen handler with the carry bit set (grok, pass 7)
 PSR_SUPCNOIND = 0xb0000000      # SER | MODE | C, IND CLEAR: supervisor, carry set, interrupts enabled, SERIAL MODE set.  ONE value
@@ -315,6 +336,13 @@ ROWS = [
     ("error",    [DIVU_R2_R3_R0],               {"r3": 0x10, "r5": DATA + 1},    V_ERROR,    0x10004, PSR_RESET,
                  [0x14000000 | (6 << 21) | (5 << 16)]),       # handler at 0x40: ld r6,r5,0 with r5 odd -> 2nd fault
     ("dslot",    [BR_N_PLUS16, DIVU_R2_R3_R0],  {"r3": 0x10},                    V_DIV0,     0x10008, PSR_RESET, None),
+    #  ---- v20, repair 13 (2026-10-16): {class} x {delay slot} at the four other arms an INSTRUCTION reaches from a slot.
+    #  `implemented = !cpu->delay_slot' at MISALIGNED/UNIMPL/PRIV/OVF swept v19 59/59 (delayslot_20261016/); dslot held
+    #  only DIV0.  BOUNDS and ERROR need a trap instruction IN a slot -- disclosed in the contract with measured escapes.
+    ("dslotmisalign", [BR_N_PLUS16, LD_R2_R3_0], {"r3": DATA + 1},               V_MISALIGN, 0x10008, PSR_RESET, None),
+    ("dslotunimpl", [STCR_R3_CR1, BR_N_PLUS16, PROM_CALL], {"r3": PSR_USER},      V_UNIMPL,   0x1000c, PSR_USER,  None),
+    ("dslotpriv", [STCR_R3_CR1, BR_N_PLUS16, LDCR_R2_CR1], {"r3": PSR_USER},      V_PRIV,     0x1000c, PSR_USER,  None),
+    ("dslotovf", [BR_N_PLUS16, ADD_R2_R3_R4],   {"r3": 0x7fffffff, "r4": 1},     V_OVF,      0x10008, PSR_RESET, None),
     ("errortb",  [TB1_0_R3_10],                 {"r3": 1},                       V_ERROR,    0x10004, PSR_RESET, None),
     ("misaligntb", [TB1_0_R3_4],                {"r3": 1},                       V_MISALIGN, 0x10004, PSR_RESET, None),
     ("unimpltb", [TB1_0_R3_5],                  {"r3": 1},                       V_UNIMPL,   0x10004, PSR_RESET, None),
@@ -411,7 +439,9 @@ ROWS = [
     #  under an SFD1-conditioned mutant too.  It is still the UNIQUE carrier of the MODE cell, and the polarity
     #  control proves that rather than asserting it: CTL_RRTRAPINV reddened all fifteen MODE-set trap rows and
     #  left this one alone.  trapfrozensfd1 below is the SINGLE-AXIS discriminator (MODE set, SFD1 clear): its
-    #  measured delta against its own mutant is ZERO -- trapfrozenuser alone catches M_RRTRAPSFD1 at 58/58.
+    #  measured delta against its own mutant is ZERO -- trapfrozenuser alone catches M_RRTRAPSFD1 at 57/58.
+    #  [CORRECTED 2026-10-16, GPT-6 Astra: this said "at 58/58", which is the score of a mutant NOT caught.  Table 15
+    #  measured 57/59 with two rows red; removing one leaves 57/58 -- arithmetic, not a preserved run.]
     #
     #  *** THE ATTRIBUTION WARRANT WAS RULED NOT TO TRANSFER, AND THE RULING IS RECORDED HERE RATHER THAN
     #  ARGUED WITH (codex/GPT-6 Astra at max, pass 12, the closing adjudication). ***  This round claimed the
@@ -421,6 +451,13 @@ ROWS = [
     #  demand "per enumerated mutant, never per attribution need".  Removing this row loses NONE of the 56
     #  closed cells and none of table 15's kills.
     #
+    #  *** RULED 2026-10-16: KEPT, NOT OWED -- all four seats (Fable 5.1, GPT-6 Astra, Grok 4.7, GLM 5.3) said KEEP. ***
+    #  Fable 5.1 added the stronger reason: the row's delta is NOT zero against every mutant -- the disclosed joint
+    #  `if (!is_trap || ((PSR & MODE) && !(PSR & SFD1)))' reds this row and no other (REASONED, not measured), so it
+    #  holds a third of the trap side's four {MODE} x {SFD1} cells; that is coverage, not attribution.  The asserts after
+    #  PSR_USERSFD1 are the structural answer to the shared-constant hazard below.  Grok 4.7 and GLM 5.3 also asked for
+    #  a sentence in the addition licence; Fable 5.1 and GPT-6 Astra said no wording -- carried to the owner as a rule
+    #  question, not settled here.  The text that follows is kept as it was written:
     #  IT IS KEPT PENDING THE 2026-09-09 ADJUDICATION, and the reason is the same seat's own next paragraph:
     #  after removal, SFD1 coverage rests entirely on trapfrozenuser, whose PSR_FRZUSER (0x03) is SHARED with
     #  errpriv and errunimpl -- so changing it to 0x0b would preserve THEIR routes while silently removing the
@@ -621,11 +658,13 @@ def run_row(name, prog, regs, vector, fault_pc, epsr_exp, handler, grace=6.0, ha
             # `trapfrozen' the second fault is a TRAP, which the manual (:8633-8636, 6.10 :10613-10614) exempts from
             # the ERROR re-route: it must deliver to ITS OWN vector (0x38), shadows still frozen.  M_SFRZTRAP sends it to 0x50.
             want.update(sxip=(0x10004 | XIP_V), snip=(0x10008 | XIP_V), sfip=(0x1000c | XIP_V), epsr=PSR_RESET)
-        elif name == "dslot":
+        elif name.startswith("dslot"):
             # the else-arm of the delay-slot branch: SNIP = (pc + 4) | V, SFIP = delay_target | V.  br.n +16 puts
             # delay_target at 0x10014 while slot_pc+4 is 0x1000c, so the two channels are DIFFERENT numbers (with
             # br.n +8 they were both 0x1000e and M_SFIPNOTGT / M_DSLOTSWAP escaped 10/10 -- Opus, pass 2).
-            want.update(snip=((fault_pc + 4) | XIP_V), sfip=((CODE + 4 + 16) | XIP_V))
+            # v20: every dslot* row puts the br.n +16 IMMEDIATELY before its faulting word, so delay_target is
+            # (fault_pc - 4) + 16 -- for dslot itself that is 0x10014, the CODE + 4 + 16 this line used to spell.
+            want.update(snip=((fault_pc + 4) | XIP_V), sfip=((fault_pc - 4 + 16) | XIP_V))
             assert want["snip"] != want["sfip"], "dslot geometry collapsed: SNIP and SFIP would be one number"
         else:
             want.update(snip=((fault_pc + 4) | XIP_V), sfip=((fault_pc + 8) | XIP_V))
```

## 4. Tables 16 and 16b (measured; logs t16_*.out / t16b_*.out in repair13_20261016/)

Table 16 ran the v20 probe as frozen BEFORE the records edits (`m88k_exc_probe_v20.FROZEN.py`); table 16b ran the
committed form (`m88k_exc_probe_v20final.FROZEN.py`: the same plus two asserts and comments).  "true red set" lists
the rows whose RESULT differs from what the probe expects (eight rows expect HALT by design).

```
log                              score    PREDICTED (PRETABLE.out)   true red set (row/RESULT where RESULT != expected)
BASE                             63/63    63/63                      (none)
M_DSNOT_MISALIGNED_ACCESS        62/63    62/63 dslotmisalign        dslotmisalign/HALT
M_DSNOT_UNIMPLEMENTED_OPCODE     62/63    62/63 dslotunimpl          dslotunimpl/HALT
M_DSNOT_PRIVILEGE_VIOLATION      62/63    62/63 dslotpriv            dslotpriv/HALT
M_DSNOT_INTEGER_OVERFLOW         62/63    62/63 dslotovf             dslotovf/HALT
M_DSNOT_ILLEGAL_INTEGER_DIVIDE   62/63    62/63 dslot                dslot/HALT
M_DSNOT_BOUNDS_CHECK_VIOLATION   63/63    63/63 (disclosed escape)   (none)
M_DSNOT_ERROR                    63/63    63/63 (disclosed escape)   (none)
M_DS_MISALIGNED_ACCESS           55/63    55/63                      misalign/HALT error/HALT misaligntb/HALT trapfrozen4/HALT umisalign/HALT errind/HALT errc/HALT errser/HALT
M_DS_UNIMPLEMENTED_OPCODE        58/63    58/63                      unimpl/HALT unimpltb/HALT trapfrozen5/HALT errunimpl/HALT unimpltbc/HALT
M_DS_PRIVILEGE_VIOLATION         57/63    57/63                      priv/HALT privtb/HALT trapfrozen6/HALT errpriv/HALT privsuptb/HALT privtbc/HALT
M_DS_INTEGER_OVERFLOW            54/63    54/63                      ovf/HALT ovftb/HALT trapfrozen8/HALT trapfrozen9/HALT ovfc/HALT indclr/HALT uovf/HALT errovf/HALT ovftbser/HALT
16b:BASE                         63/63    63/63 (committed form)     (none)
16b:M_RRTRAPJOINT                62/63    62/63 trapfrozensfd1       trapfrozensfd1/STOP
ANALYZE_T16_DONE

=== DELAY-SLOT axis -- v20, the SHIPPED instrument  (63 rows) ===
  MISALIGN  CLOSED     in a slot: dslotmisalign
  UNIMPL    CLOSED     in a slot: dslotunimpl
  PRIV      CLOSED     in a slot: dslotpriv
  BOUNDS    DISCLOSED  reachable in a slot only by a TRAP instruction there; the MC88100 manual does not settle its legality (mc88100.txt:9433-9440 covers the slot OF a trap-taken instruction)
  DIV0      CLOSED     in a slot: dslot
  OVF       CLOSED     in a slot: dslotovf
  ERROR     DISCLOSED  reachable in a slot only by a TRAP instruction there; the MC88100 manual does not settle its legality (mc88100.txt:9433-9440 covers the slot OF a trap-taken instruction)
closed 5 of 7 arms on the delay-slot axis (2 disclosed)
```

## 5. The enclosing function -- `m88k_exception()`, `src/cpus/cpu_m88k.c` at HEAD (lines 689-981, unchanged by this repair)

```c
 689  void m88k_exception(struct cpu *cpu, int vector, int is_trap)
 690  {
 691  	bool update_shadow_regs = true;
 692  	bool implemented = false;
 693  
 694  	// TODO: Use a const char * instead or something like that, inside the switch...
 695  
 696  	switch (vector) {
 697  
 698  	case M88K_EXCEPTION_RESET:
 699  		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "RESET", VERBOSITY_INFO, "");
 700  		implemented = true;
 701  		break;
 702  
 703  	case M88K_EXCEPTION_INTERRUPT:
 704  		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "INTERRUPT", VERBOSITY_INFO, "");
 705  		implemented = true;
 706  		break;
 707  
 708  	case M88K_EXCEPTION_INSTRUCTION_ACCESS:
 709  		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "INSTRUCTION_ACCESS", VERBOSITY_INFO, "");
 710  		implemented = true;
 711  		break;
 712  
 713  	case M88K_EXCEPTION_DATA_ACCESS:
 714  		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "DATA_ACCESS", VERBOSITY_INFO, "");
 715  		implemented = true;
 716  		break;
 717  
 718  	case M88K_EXCEPTION_MISALIGNED_ACCESS:
 719  		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "MISALIGNED_ACCESS", VERBOSITY_INFO, "");
 720  		implemented = true;	/*  m88kexcdeliver  */
 721  		break;
 722  
 723  	case M88K_EXCEPTION_UNIMPLEMENTED_OPCODE:
 724  		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "UNIMPLEMENTED_OPCODE", VERBOSITY_INFO, "");
 725  		implemented = true;	/*  m88kexcdeliver  */
 726  		break;
 727  
 728  	case M88K_EXCEPTION_PRIVILEGE_VIOLATION:
 729  		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "PRIVILEGE_VIOLATION", VERBOSITY_INFO, "");
 730  		implemented = true;	/*  m88kexcdeliver  */
 731  		break;
 732  
 733  	case M88K_EXCEPTION_BOUNDS_CHECK_VIOLATION:
 734  		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "BOUNDS_CHECK_VIOLATION", VERBOSITY_INFO, "");
 735  		implemented = true;	/*  m88kexcdeliver  */
 736  		break;
 737  
 738  	case M88K_EXCEPTION_ILLEGAL_INTEGER_DIVIDE:
 739  		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "ILLEGAL_INTEGER_DIVIDE", VERBOSITY_INFO, "");
 740  		implemented = true;	/*  m88kexcdeliver  */
 741  		break;
 742  
 743  	case M88K_EXCEPTION_INTEGER_OVERFLOW:
 744  		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "INTEGER_OVERFLOW", VERBOSITY_INFO, "");
 745  		implemented = true;	/*  m88kexcdeliver  */
 746  		break;
 747  
 748  	case M88K_EXCEPTION_ERROR:
 749  		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "ERROR", VERBOSITY_INFO, "");
 750  		implemented = true;	/*  m88kexcdeliver  */
 751  		break;
 752  
 753  	case M88K_EXCEPTION_SFU1_PRECISE:
 754  		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "SFU1_PRECISE", VERBOSITY_ERROR, "");
 755  		break;
 756  
 757  	case M88K_EXCEPTION_SFU1_IMPRECISE:
 758  		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "SFU1_IMPRECISE", VERBOSITY_ERROR, "");
 759  		break;
 760  
 761  	case 0x80:	/*  up to OpenBSD 5.2  */
 762  	case 0x1c2:	/*  from OpenBSD 5.3 and forward...  */
 763  		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "syscall", VERBOSITY_INFO,
 764  		    "r13=%i", cpu->cd.m88k.r[13]);
 765  #if 0
 766  		fatal("[ syscall %i(", cpu->cd.m88k.r[13]);
 767  		m88k_cpu_functioncall_trace(cpu, 8);
 768  		fatal(") ]\n");
 769  #endif
 770  		break;
 771  
 772  	case MVMEPROM_VECTOR:
 773  		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "MVMEPROM_VECTOR", VERBOSITY_INFO, "");
 774  		break;
 775  
 776  	default:
 777  		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "unknown vector",
 778  		    vector < M88K_EXCEPTION_USER_TRAPS_START ? VERBOSITY_ERROR
 779  		    : VERBOSITY_INFO, "0x%03x", vector);
 780  	}
 781  
 782  	/*
 783  	 *  m88kexcdeliver (2026-09-05): the seven trap-like classes above are
 784  	 *  DELIVERED (VBR + 8*vector, SXIP = the faulting instruction, SNIP = the
 785  	 *  next one, destination register unchanged -- MC88100 UM 6.4.3/6.5/6.6/
 786  	 *  6.8.3), like the four this fallback never covered.  Before, any of them
 787  	 *  stopped EVERY guest CPU here: one divu by zero, in either mode, ended
 788  	 *  the emulation (measured: regress/m88k_exc_probe.py rows div0/udiv0).
 789  	 *  Pre-existing upstream code (this fallback is the 0.7.0 import),
 790  	 *  surfaced by the 2026-09-05 retrospective of #380.  What still lands
 791  	 *  here, by design: SFU1_PRECISE/IMPRECISE (114/115; row m88kexcsfu1 --
 792  	 *  faithful delivery needs the rest of the SFU1 exception state, which
 793  	 *  the fork does not write) and vectors 11..113/116..127 (117 vectors
 794  	 *  with the two SFU1 ones), which no literal-constant raise site names
 795  	 *  but a supervisor tb0/tb1/tcnd can name directly (row
 796  	 *  m88kexctaildefault; the probe's resid50/sfu1h rows pin that they
 797  	 *  STILL halt).
 798  	 */
 799  	if (vector < M88K_EXCEPTION_USER_TRAPS_START && !implemented) {
 800  		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "unimplemented",
 801  		    VERBOSITY_ERROR, "vector=0x%03x pc=0x%08x",
 802  			vector,
 803  			(int)cpu->pc);
 804  		for (int j = 0; j < cpu->machine->ncpus; ++j)
 805  			cpu->machine->cpus[j]->running = false;
 806  		m88k_pc_to_pointers(cpu);
 807  		return;
 808  	}
 809  
 810  	/*  Stuff common for all exceptions:  */
 811  	if (cpu->cd.m88k.cr[M88K_CR_PSR] & M88K_PSR_SFRZ) {
 812  		/*
 813  		 *  Non-trap exceptions when the shadow freeze bit is already
 814  		 *  set result in an Error exception:
 815  		 */
 816  		if (!is_trap) {
 817  			vector = M88K_EXCEPTION_ERROR;
 818  			fatal("[ SFRZ already set in PSR => ERROR ]\n");
 819  		}
 820  
 821  		update_shadow_regs = false;
 822  	} else {
 823  		/*  Freeze shadow registers, and save the PSR:  */
 824  		cpu->cd.m88k.cr[M88K_CR_EPSR] = cpu->cd.m88k.cr[M88K_CR_PSR];
 825  	}
 826  
 827  	m88k_stcr(cpu, cpu->cd.m88k.cr[M88K_CR_PSR]
 828  	    | M88K_PSR_SFRZ	/*  Freeze shadow registers,          */
 829  	    | M88K_PSR_IND	/*  disable interrupts,               */
 830  	    | M88K_PSR_SFD1	/*  disable the floating point unit,  */
 831  	    | M88K_PSR_MODE,	/*  and switch to supervisor mode.    */
 832  	    M88K_CR_PSR, 0);
 833  
 834  	if (update_shadow_regs) {
 835  		cpu->cd.m88k.cr[M88K_CR_SSBR] = 0;
 836  
 837  		cpu->cd.m88k.cr[M88K_CR_SXIP] = cpu->pc | M88K_XIP_V;
 838  
 839  		/*  SNIP is the address to return to, when executing rte:  */
 840  		if (cpu->delay_slot) {
 841  			if (vector == M88K_EXCEPTION_DATA_ACCESS) {
 842  				cpu->cd.m88k.cr[M88K_CR_SNIP] = cpu->cd.m88k.delay_target | M88K_NIP_V;
 843  				cpu->cd.m88k.cr[M88K_CR_SFIP] = cpu->cd.m88k.cr[M88K_CR_SNIP]+4;
 844  			} else if (vector == M88K_EXCEPTION_INSTRUCTION_ACCESS) {
 845  				/*  If we are in a delay slot, then pc is
 846  				    something like 0xc6000 here (not 0xc5ffc).  */
 847  				cpu->cd.m88k.cr[M88K_CR_SNIP] = cpu->cd.m88k.delay_target | M88K_NIP_V;
 848  				cpu->cd.m88k.cr[M88K_CR_SFIP] = 0;
 849  			} else {
 850  				/*  Perhaps something like this could work:  */
 851  				cpu->cd.m88k.cr[M88K_CR_SNIP] = (cpu->pc + 4) | M88K_NIP_V;
 852  				cpu->cd.m88k.cr[M88K_CR_SFIP] = cpu->cd.m88k.delay_target | M88K_NIP_V;
 853  			}
 854  		} else {
 855  			cpu->cd.m88k.cr[M88K_CR_SNIP] = (cpu->pc + 4) | M88K_NIP_V;
 856  			cpu->cd.m88k.cr[M88K_CR_SFIP] = cpu->cd.m88k.cr[M88K_CR_SNIP]+4;
 857  		}
 858  
 859  		if (vector == M88K_EXCEPTION_INSTRUCTION_ACCESS)
 860  			cpu->cd.m88k.cr[M88K_CR_SXIP] |= M88K_XIP_E;
 861  	}
 862  
 863  	cpu->pc = cpu->cd.m88k.cr[M88K_CR_VBR] + 8 * vector;
 864  
 865  	if (cpu->delay_slot)
 866  		cpu->delay_slot = EXCEPTION_IN_DELAY_SLOT;
 867  	else
 868  		cpu->delay_slot = NOT_DELAYED;
 869  
 870  	/*  Default to no memory transactions:  */
 871  	cpu->cd.m88k.cr[M88K_CR_DMT0] = 0;
 872  	cpu->cd.m88k.cr[M88K_CR_DMD0] = 0;
 873  	cpu->cd.m88k.cr[M88K_CR_DMA0] = 0;
 874  	cpu->cd.m88k.cr[M88K_CR_DMT1] = 0;
 875  	cpu->cd.m88k.cr[M88K_CR_DMD1] = 0;
 876  	cpu->cd.m88k.cr[M88K_CR_DMA1] = 0;
 877  	cpu->cd.m88k.cr[M88K_CR_DMT2] = 0;
 878  	cpu->cd.m88k.cr[M88K_CR_DMD2] = 0;
 879  	cpu->cd.m88k.cr[M88K_CR_DMA2] = 0;
 880  
 881  	/*  Vector-specific handling:  */
 882  	if (vector < M88K_EXCEPTION_USER_TRAPS_START) {
 883  		switch (vector) {
 884  
 885  		case M88K_EXCEPTION_RESET:
 886  			fatal("[ m88k_exception: reset ]\n");
 887  			for (int j = 0; j < cpu->machine->ncpus; ++j)
 888  				cpu->machine->cpus[j]->running = false;
 889  			break;
 890  
 891  		case M88K_EXCEPTION_INTERRUPT:
 892  			/*  When returning with rte, we want to re-  */
 893  			/*  execute the interrupted instruction:  */
 894  			cpu->cd.m88k.cr[M88K_CR_SNIP] -= 4;
 895  			cpu->cd.m88k.cr[M88K_CR_SFIP] -= 4;
 896  			break;
 897  
 898  		case M88K_EXCEPTION_INSTRUCTION_ACCESS:
 899  			/*  When returning with rte, we want to re-  */
 900  			/*  execute the instruction in SXIP, not SNIP/SFIP,  */
 901  			/*  (unless the exception was in a delay-slot):  */
 902  			if (!(cpu->delay_slot & EXCEPTION_IN_DELAY_SLOT)) {
 903  				cpu->cd.m88k.cr[M88K_CR_SNIP] = 0;
 904  				cpu->cd.m88k.cr[M88K_CR_SFIP] = 0;
 905  			}
 906  			break;
 907  
 908  		case M88K_EXCEPTION_DATA_ACCESS:
 909  			/*  Update the memory transaction registers:  */
 910  			cpu->cd.m88k.cr[M88K_CR_DMT0] = cpu->cd.m88k.dmt[0];
 911  			cpu->cd.m88k.cr[M88K_CR_DMD0] = cpu->cd.m88k.dmd[0];
 912  			cpu->cd.m88k.cr[M88K_CR_DMA0] = cpu->cd.m88k.dma[0];
 913  			cpu->cd.m88k.cr[M88K_CR_DMT1] = cpu->cd.m88k.dmt[1];
 914  			cpu->cd.m88k.cr[M88K_CR_DMD1] = cpu->cd.m88k.dmd[1];
 915  			cpu->cd.m88k.cr[M88K_CR_DMA1] = cpu->cd.m88k.dma[1];
 916  			cpu->cd.m88k.cr[M88K_CR_DMT2] = 0;
 917  			cpu->cd.m88k.cr[M88K_CR_DMD2] = 0;
 918  			cpu->cd.m88k.cr[M88K_CR_DMA2] = 0;
 919  			m88k_memory_transaction_debug_dump(cpu, 0);
 920  			m88k_memory_transaction_debug_dump(cpu, 1);
 921  			break;
 922  
 923  		case M88K_EXCEPTION_MISALIGNED_ACCESS:
 924  		case M88K_EXCEPTION_UNIMPLEMENTED_OPCODE:
 925  		case M88K_EXCEPTION_PRIVILEGE_VIOLATION:
 926  		case M88K_EXCEPTION_BOUNDS_CHECK_VIOLATION:
 927  		case M88K_EXCEPTION_ILLEGAL_INTEGER_DIVIDE:
 928  		case M88K_EXCEPTION_INTEGER_OVERFLOW:
 929  		case M88K_EXCEPTION_ERROR:
 930  			/*  m88kexcdeliver: OUTSIDE A DELAY SLOT the common path above
 931  			    is already the architectural contract for these -- SXIP =
 932  			    the faulting instruction, SNIP = the next one, SFIP = SNIP+4,
 933  			    and rte resumes at SNIP (UM 6.4.3.1.4: "the processor
 934  			    hardware does not use the SXIP on return from an exception"),
 935  			    so the upstream doubt that sat here in an #if 0 ("should the
 936  			    PC be backed up one step?") is answered NO: 6.5.x/6.8.3 say
 937  			    the destination register is unchanged (6.6: and the carry
 938  			    bit, for the overflow case), and a handler that wants
 939  			    re-execution arranges SNIP/SFIP itself.  INSIDE a delay slot
 940  			    the else-arm above ("Perhaps something like this could
 941  			    work") is upstream's guess and the manual disagrees (Table
 942  			    6-3: the shadows copy XIP/NIP/FIP, and UM 6.2 defines FIP as
 943  			    the taken branch's target while the branch executes, so for
 944  			    a fault in its delay slot NIP = target, FIP = target+4) --
 945  			    pre-existing, now reachable by ordinary faults, row
 946  			    m88kdslotshadow.
 947  			    Without these labels the classes reached the default: below,
 948  			    which stops the cpu -- the one-site fix was measured to do
 949  			    exactly that; with them, nothing below 128 reaches that
 950  			    default any more (it is unreachable code kept as the
 951  			    tripwire for an eighth class).  ERROR arrives here by TWO
 952  			    routes: the SFRZ re-route above (a fault inside a handler,
 953  			    shadows deliberately frozen at the FIRST fault's values --
 954  			    SXIP then names that first fault, not this one) and a
 955  			    supervisor tb0/tb1/tcnd naming vector 10 directly (shadows
 956  			    updated normally when that trap is taken UNFROZEN; inside a
 957  			    handler it takes the is_trap exemption above and arrives
 958  			    here with the shadows frozen).  Not modelled, disclosed: scoreboard
 959  			    capture (the shadow-update path writes SSBR = 0; a frozen
 960  			    SSBR keeps its old value) and fcr2/fcr4/fcr5 for the divide.  */
 961  			break;
 962  
 963  #if 0
 964  		// TODO: Read up more about SFU1 exceptions and how the
 965  		// control registers look when they happen.
 966  		case M88K_EXCEPTION_SFU1_PRECISE:
 967  			cpu->cd.m88k.cr[M88K_CR_SNIP] = 0; //?
 968  			cpu->cd.m88k.cr[M88K_CR_SFIP] = 0;
 969  			//cpu->cd.m88k.cr[M88K_CR_SNIP] -= 4;
 970  			//cpu->cd.m88k.cr[M88K_CR_SFIP] -= 4;
 971  			break;
 972  #endif
 973  
 974  		default:debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "m88k",
 975  			    VERBOSITY_ERROR, "internal error");
 976  			cpu->running = false;
 977  		}
 978  	}
 979  
 980  	m88k_pc_to_pointers(cpu);
 981  }
```

## 6. The close adjudication's findings, consolidated -- with the coordinator's disposition on each

F1 (Fable 5.1) "the closing pass's 56-cell denominator omits `cpu->delay_slot` -- the one CPU-state lvalue `m88k_exception()`'s
   repair path TESTS -- and {MISALIGN, UNIMPL, PRIV, OVF} x {delay slot set} are unrowed".  **ACCEPTED, MEASURED** (section 1
   item 2); L2; repair 13 is the diff in section 3.  None of the three CLOSE answers enumerated `delay_slot`.
F2 (Fable 5.1) BOUNDS and ERROR x {delay slot}: "reachable in the emulator by a `tb1` in a `.n` slot ... whether the
   architecture permits a trap instruction in a slot I could NOT settle from `mc88100.txt` -- disclosed, not counted".
   **ACCEPTED**: disclosed in the contract, with both forms MEASURED as escapes in table 16 rather than predicted.
F3 (Fable 5.1) "a frozen handler with a `.n` slot fault (`errdslot`) is cheap and I recommend it ride with the repair, but it is
   not in the floor as bounded here".  **FILED** as clause-(e) coverage, not added: outside the bound by the recommending seat's
   own statement, and a row added after PRETABLE.out was written would have re-opened table 16.
F4 (Fable 5.1) "four more rows pinned to [the else-arm] must carry the same re-pin-first note".  **ACCEPTED**: one shared
   scoring branch (`name.startswith("dslot")`), and the docstring row table says so.
F5 (Fable 5.1) the deferred cut question is ANSWERED, not moot: by the carrier's 2026-09-25 pin ("tests" = masks or compares as
   a case) and its 2026-10-09 ruling (a derived input is graded by what the body tests on it), `m88k_exception()` tests ONE PSR
   bit, SFRZ, so {site} x {MODE, SFD1, IND, C, SER} is clause-(e) coverage at every site; v16/v17/v19 were graded L2 "under a
   reads-PSR criterion the carrier's 09-25 pin does not support"; one sentence in the closure note.  **ADOPTED AS A RECORDS
   SENTENCE ONLY -- no row, no code, no rule change.  Disputed: see D1.**
F6 (all four) `m88ksfd1row`: KEEP.  **ACCEPTED**: close the row "kept, not owed" (warrant in F7 and D2).
F7 (Fable 5.1) the row's delta is not zero against every mutant: the disclosed joint `if (!is_trap || ((PSR & MODE) &&
   !(PSR & SFD1)))` "reds `trapfrozensfd1` and no other row" (REASONED); and the shared-constant hazard's structural defence is
   "two import-time asserts in the probe ... named for the cells they carry".  **ACCEPTED**: the asserts are in the diff and
   negative-controlled; the joint mutant is MEASURED in table 16b (section 4) -- it is the stated warrant for keeping the row.
F8 (GPT-6 Astra) "Table 15 reports 57/59, with two failing rows.  Removing `trapfrozensfd1` would leave 57/58 ... not 58/58."
   **ACCEPTED, L4**: corrected in place in the probe comment (this diff), and in the same commit in `fable_queue.md`, the
   CHANGELOG #502 block and the `m88ksfd1row` ledger witness, each quoting what it corrects.
F9 (Grok 4.7) "`derive_cells.py` and `CELLCENSUS.out` still stop at the 57-row instrument and still print trap-side MODE and SFD1
   open ... a records defect".  **ACCEPTED**: fixed (section 1 item 4); the new delay-slot section of its output is in section 4.
F10 (GLM 5.3) "'this four-seat adjudication is the missing roster' overstates ... The record should read 'pass-12's measurement,
   ratified by three independent audits plus the author's self-review.'"  **ACCEPTED in substance, and overtaken**: that pass
   did not close the chain.  If this pass closes it, its validity is: the diff delivered (section 3); four of nine seats by owner
   ruling, the other five named as not fired; zero breaches stated WITH the denominator (Q7).
F11 (GLM 5.3) P1-P3 (the ground for the MODE exclusion; which bits vary at the frozen sites; `trapfrozensfd1`'s stimulus).
   **SETTLED from the committed probe text** -- the third and fourth bullets of section 2.
F12 (GPT-6 Astra) "I retract pass 12's rejection of retention; its rejection of attribution as a transferred warrant and its
   zero-floor finding stand."  **RECORDED**; the zero-floor finding is refuted by F1's measurement.

## 7. Disagreements, both sides in their own words

D1 -- the deferred cut question (F5).
   * Fable 5.1: "The question is answered by the carrier's own later pins, the answer re-grades three of this round's repairs from
     L2 to voluntary clause-(e) closure, and leaving it 'for a future round' leaves the over-grade standing as the precedent that
     future round will cite."
   * GPT-6 Astra: "moot for closure, unresolved generally ... This does not retrospectively endorse pass 7's classification."
   * Grok 4.7: "Moot as stated.  No remaining cell of this round is held out by 'the arm reads no PSR bit' ... Whether that test is
     the right DEPENDS-ON cut on a future round is a rule for the owner when a live cell still depends on it."
   * GLM 5.3: "moot as to rows, not as to the denominator" (conditional on its P1, which section 2 now settles as reachability).
   * Coordinator: no seat disputed Fable's premise (only SFRZ is TESTED); the three "moot" answers address row demand, which
     Fable agrees nothing depends on, and none addresses the precedent value of the recorded L2 grades.  So the sentence goes in
     the closure record, attributed, beside the three moot rulings.  Attack this if it is wrong.

D2 -- does the addition licence need a sentence for `m88ksfd1row`?
   * Grok 4.7 (yes): "A zero-delta row is licensed when it is the only stimulus for an enumerated cell that does not share a
     constant with rows whose oracles do not observe that bit, and a one-token edit of the shared constant preserves those rows
     and deletes the stimulus ... 'Kept, not owed' will be copied onto the next zero-delta row unless the ledger line cites the
     shared-constant condition above."
   * GLM 5.3 (yes): "a 'kept, not owed' record with no warrant is unstable -- the next zero-delta pass applying 'row demand bounded
     per enumerated mutant' removes it".
   * Fable 5.1 (no): "The addition licence governs PRODUCT code; it is the wrong instrument for a detector row.  Row demand ...
     bounds what is OWED, not what is PERMITTED.  Neither says delete ... One instance does not earn carrier prose."
   * GPT-6 Astra (no): "KEEP, with no licence or row-demand change ... the carrier explicitly extends the objection to
     attribution-only detector additions, so 'PRODUCT code' alone does not settle applicability.  But neither rule mandates
     pruning every redundant row."
   * Coordinator: no carrier wording in this round -- the carrier's own structure-first rule prefers the two asserts to a
     paragraph -- but the ledger line CITES the warrant (Grok's condition plus F7's measured delta), so it cannot be copied bare.
     The wording question goes to the owner as a rule question.

## 8. Questions (VERDICT LINE FIRST)

Q1. Does v20 close {arm} x {delay slot} at the five arms an instruction reaches from a slot?  Name any edit to
    `m88k_exception()` that sweeps the 63-row probe inside the floor -- a single-axis cell of a body-TESTED lvalue at a dominating
    predicate -- with its predicted score.  Section 5 is the whole function; mind its common tail.
Q2. The delay-slot axis at the OTHER two sites.  The fallback (799) halts without reading `delay_slot`; the frozen path sets
    `update_shadow_regs = false`, so the 840 test is not reached, but the 865 write is.  Coordinator: {fallback, SFRZ re-route} x
    {delay slot} is clause (e), and `errdslot` is filed.  Floor or clause (e)?
Q3. BOUNDS / ERROR x {delay slot}: disclosed, or floor?  If floor, give the row (a `tb1` naming 7 or 10 in a `.n` slot) and its
    expected shadows.
Q4. D1: is the F5 records sentence right?
Q5. D2: licence wording, or the ledger-line warrant?
Q6. Which of the coordinator's ACCEPTED dispositions is wrong?  There are nine: F1, F2, F4, F6, F7, F8, F9, F10, F11.  (F3 is
    filed, F5 adopted under dispute, F12 recorded.)
Q7. If nothing survives: CLOSE, with this denominator -- the PSR grid 40/40 at the seven arms, fallback 6/6, non-trap re-route
    5/5, trap exemption 5/5, and the delay-slot axis 5/5 at the instruction-reachable arms = 61 enumerated cells; disclosed:
    BOUNDS/ERROR x {delay slot}, trap instructions in a slot at any arm, {fallback, re-route} x {delay slot}, multi-axis joints,
    vectors 0..3 (`m88kexchwtraps`).  Is that denominator complete?

Seat notes: Fable 5.1 -- F1 and F7 were yours; be harder on the repair than on the finding, including whether five rows pinned
to an else-arm the manual calls wrong is the right shape.  GPT-6 Astra -- your pass 12 is what this overturned; check the
repair, not only the count.  Grok 4.7 -- passes 9 and 11 were yours.  GLM 5.3 -- you cannot read files; say "not checkable from
the packet" where that is true rather than guessing.
