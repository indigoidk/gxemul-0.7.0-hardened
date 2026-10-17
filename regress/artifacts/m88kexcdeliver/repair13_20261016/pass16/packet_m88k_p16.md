# PASS 16 -- `m88kexcdeliver` (#502): VERIFY THE ENUMERATION of repair 15 (probe v24), and adjudicate pass 15's findings

Four seats, by the owner's roster of 2026-10-16: Fable 5.1, GPT-6 Astra, Grok 4.7, GLM 5.3.  Opus, agy, kimi, deepseek and
minimax are DELIBERATELY NOT FIRED under that roster.  An ordinary regression-detector coverage review.  READ-ONLY: write
nothing to any project tree.  The tree under review is `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC` -- HEAD c64445fa (v23 is
committed: 16512e9c) plus the uncommitted probe v24 in the working tree; ignore the pristine upstream copy at
`C:/DocumentNoSnc/cc/GXEMUL/src/`.  Everything a packet-fed seat needs is inlined.

**Please do not simply ratify, and do not hunt cells the enumeration already names.**  This repair claims to complete the
class: `m88k_exception()` TESTS exactly four inputs (section 3), the floor is their product over the seven labels, and every
reachable cell is now rowed.  Your job is to check that claim -- the input set, the reachability rule, each row's credit, and
each disclosure -- not to re-open settled cells.

Open with your seat token -- `FABLE_M88KP16_20261016` / `ASTRA_M88KP16_20261016` / `GROK_M88KP16_20261016` /
`GLM_M88KP16_20261016` -- then ONE line: `VERDICT: CLOSE / DO NOT CLOSE (<one line>)`.

## 1. What pass 15 found, and how it was ruled (answers in `repair13_20261016/pass15/`)

* **GPT-6 Astra -- CLOSE**: all 28 state cells verified against the row definitions; no vacuous row; 78/78.
* **Grok 4.7 -- CLOSE**: 28/28 verified; withdrew its pass-14 positions D3 and D4; held `is_trap` a per-raise PARAMETER
  outside the floor's device-state axes, so the five frozen trap-in-slot cells clause (e).  Corrected the contract's
  vectors-0..3 pointer (`m88kexcdebt`, not `m88kexchwtraps`) -- applied in 16512e9c.
* **Fable 5.1 -- DO NOT CLOSE**: the enumeration omits `is_trap` (:816), the fourth input the delivery path tests.  By the
  carrier's generating-set clause and this chain's own `*tb` / `trapfrozen<L>` rows, a TRAP in a slot at the five instruction
  labels is floor; the five `!is_trap || (vector == L && cpu->delay_slot)` 73/73 escapes of table 19 were measured floor
  breaches.  Ten rows close it, "after which m88k_exception() has no untested input left".
* **GLM 5.3 -- DO NOT CLOSE**: the user-trap labels (0x80, 0x1c2, MVMEPROM_VECTOR, the default) reach the same delay-slot code
  and were neither rowed nor disclosed.
* **RULED (the argument, not the 2-2 count):** Fable's -- the carrier added the generating-set clause precisely because a bare
  state floor graded an input-bit escape as debt, and this chain repaired the identical shape in-round on passes 5 and 7.
  GLM's user-trap labels: DISCLOSED (Fable: outside the fix's seven labels; their delivery predates #502), with their escapes
  now MEASURED (table 20).  v23 was committed as 16512e9c with the chain recorded OPEN; repair 15 is this diff.

## 2. Settled premises (warrants inline; challenge any of them)

* The function TESTS exactly four inputs: `vector` (switch 1, :799, the shadow branch's DATA/INSTRUCTION_ACCESS tests,
  switch 2), `PSR & SFRZ` (:811, the only PSR bit masked or compared), `cpu->delay_slot` (:840 inside `if
  (update_shadow_regs)`, :865 on every path past the fallback -- and `X(br_n)` reads :865's write to keep the vector over the
  branch target), and `is_trap` (:816, inside the SFRZ block).  Everything else is copied, ORed or written.
* `is_trap = 1` comes only from `tcnd` / `tb0` / `tb1` (`cpu_m88k_instr.c:2529/:2551/:2564`); a user-mode trap naming a vector
  below 128 raises PRIVILEGE with is_trap 0; no instruction raises 7 or 10 any other way (there is no `tbnd`).  So the 8
  cells (BOUNDS or ERROR) x (any SFRZ, any slot) x (is_trap 0) are UNREACHABLE, and the grid has 48 reachable cells.
* Frozen rows put their slot fault in the div0 handler at 0x40 behind `br.n +8`, whose target is the SELF word planted after
  the handler -- never the row's own breakpoint (the `br.n +16` -> 0x50 trap of pass 14).  **One exception, found by table
  20 itself:** `trapfrozen9dslot` traps to OVERFLOW, whose entry IS 0x48 = the +8 target, so under the `:865` mutant it read
  DELIVER (73/84 against a predicted 72/84).  It now uses `br.n +16` (target 0x50; its breakpoint is 0x48); table 20b
  re-measured every mutant that touches it.  Every other frozen row's target differs from its breakpoint (checked).  `trapfrozen8dslot` follows
  `trapfrozen8`'s shape (first fault OVERFLOW, handler at 0x48, breakpoint 0x40), so its +8 target is 0x50's SELF, which is
  safe because its breakpoint is 0x40.
* The probe's code is the frozen instrument table 20 scored (AST-identical; the committed v24 differs only in the docstring).

## 3. Table 20 (measured; PRETABLE_20.out written first, in its own file)

"red" lists the rows whose RESULT differs from what the probe expects (ten v24 rows expect HALT by design).

```
BASE                               84/84  predicted 84/84  AS PREDICTED  red: (none)
M_RRDS_MISALIGNED_ACCESS           83/84  predicted 83/84  AS PREDICTED  red: trapfrozen4dslot/STOP
M_ARMTSU_MISALIGNED_ACCESS         83/84  predicted 83/84  AS PREDICTED  red: dslotmisaligntb/HALT
M_RRDS_UNIMPLEMENTED_OPCODE        83/84  predicted 83/84  AS PREDICTED  red: trapfrozen5dslot/STOP
M_ARMTSU_UNIMPLEMENTED_OPCODE      83/84  predicted 83/84  AS PREDICTED  red: dslotunimpltb/HALT
M_RRDS_PRIVILEGE_VIOLATION         83/84  predicted 83/84  AS PREDICTED  red: trapfrozen6dslot/STOP
M_ARMTSU_PRIVILEGE_VIOLATION       83/84  predicted 83/84  AS PREDICTED  red: dslotprivtb/HALT
M_RRDS_ILLEGAL_INTEGER_DIVIDE      83/84  predicted 83/84  AS PREDICTED  red: trapfrozen8dslot/STOP
M_ARMTSU_ILLEGAL_INTEGER_DIVIDE    83/84  predicted 83/84  AS PREDICTED  red: dslotdiv0tb/HALT
M_RRDS_INTEGER_OVERFLOW            83/84  predicted 83/84  AS PREDICTED  red: trapfrozen9dslot/STOP
M_ARMTSU_INTEGER_OVERFLOW          83/84  predicted 83/84  AS PREDICTED  red: dslotovftb/HALT
M_ARMTS_MISALIGNED_ACCESS          82/84  predicted 82/84  AS PREDICTED  red: dslotmisaligntb/HALT trapfrozen4dslot/HALT
M_DSNOT_MISALIGNED_ACCESS          80/84  predicted 80/84  AS PREDICTED  red: dslotmisalign/HALT errdslotmisalign/HALT dslotmisaligntb/HALT trapfrozen4dslot/HALT
M_DSFRZ_MISALIGNED_ACCESS          82/84  predicted 82/84  AS PREDICTED  red: errdslotmisalign/HALT trapfrozen4dslot/HALT
M_ARMTS_UNIMPLEMENTED_OPCODE       82/84  predicted 82/84  AS PREDICTED  red: dslotunimpltb/HALT trapfrozen5dslot/HALT
M_DSNOT_UNIMPLEMENTED_OPCODE       80/84  predicted 80/84  AS PREDICTED  red: dslotunimpl/HALT errdslotunimpl/HALT dslotunimpltb/HALT trapfrozen5dslot/HALT
M_DSFRZ_UNIMPLEMENTED_OPCODE       82/84  predicted 82/84  AS PREDICTED  red: errdslotunimpl/HALT trapfrozen5dslot/HALT
M_ARMTS_PRIVILEGE_VIOLATION        82/84  predicted 82/84  AS PREDICTED  red: dslotprivtb/HALT trapfrozen6dslot/HALT
M_DSNOT_PRIVILEGE_VIOLATION        80/84  predicted 80/84  AS PREDICTED  red: dslotpriv/HALT errdslotpriv/HALT dslotprivtb/HALT trapfrozen6dslot/HALT
M_DSFRZ_PRIVILEGE_VIOLATION        82/84  predicted 82/84  AS PREDICTED  red: errdslotpriv/HALT trapfrozen6dslot/HALT
M_ARMTS_BOUNDS_CHECK_VIOLATION     82/84  predicted 82/84  AS PREDICTED  red: dslotbounds/HALT trapfrozen7dslot/HALT
M_DSNOT_BOUNDS_CHECK_VIOLATION     82/84  predicted 82/84  AS PREDICTED  red: dslotbounds/HALT trapfrozen7dslot/HALT
M_DSFRZ_BOUNDS_CHECK_VIOLATION     83/84  predicted 83/84  AS PREDICTED  red: trapfrozen7dslot/HALT
M_ARMTS_ILLEGAL_INTEGER_DIVIDE     82/84  predicted 82/84  AS PREDICTED  red: dslotdiv0tb/HALT trapfrozen8dslot/HALT
M_DSNOT_ILLEGAL_INTEGER_DIVIDE     80/84  predicted 80/84  AS PREDICTED  red: dslot/HALT errdslotdiv0/HALT dslotdiv0tb/HALT trapfrozen8dslot/HALT
M_DSFRZ_ILLEGAL_INTEGER_DIVIDE     82/84  predicted 82/84  AS PREDICTED  red: errdslotdiv0/HALT trapfrozen8dslot/HALT
M_ARMTS_INTEGER_OVERFLOW           82/84  predicted 82/84  AS PREDICTED  red: dslotovftb/HALT trapfrozen9dslot/HALT
M_DSNOT_INTEGER_OVERFLOW           80/84  predicted 80/84  AS PREDICTED  red: dslotovf/HALT errdslotovf/HALT dslotovftb/HALT trapfrozen9dslot/HALT
M_DSFRZ_INTEGER_OVERFLOW           82/84  predicted 82/84  AS PREDICTED  red: errdslotovf/HALT trapfrozen9dslot/HALT
M_ARMTS_ERROR                      82/84  predicted 82/84  AS PREDICTED  red: dsloterror/HALT trapfrozen10dslot/HALT
M_DSNOT_ERROR                      82/84  predicted 82/84  AS PREDICTED  red: dsloterror/HALT trapfrozen10dslot/HALT
M_DSFRZ_ERROR                      83/84  predicted 83/84  AS PREDICTED  red: trapfrozen10dslot/HALT
M_DS865                            73/84  predicted 72/84  *** DIFFERS ***  red: errdslotmisalign/STOP errdslotovf/STOP errdslotdiv0/STOP errdslotpriv/STOP errdslotunimpl/STOP trapfrozen7dslot/STOP trapfrozen10dslot/STOP trapfrozen4dslot/STOP trapfrozen5dslot/STOP trapfrozen6dslot/STOP trapfrozen8dslot/STOP
M_RRTDS                            77/84  predicted 77/84  AS PREDICTED  red: trapfrozen7dslot/STOP trapfrozen10dslot/BADREGS trapfrozen4dslot/STOP trapfrozen5dslot/STOP trapfrozen6dslot/STOP trapfrozen8dslot/STOP trapfrozen9dslot/STOP
M_RRNTDS                           79/84  predicted 79/84  AS PREDICTED  red: errdslotmisalign/STOP errdslotovf/STOP errdslotdiv0/STOP errdslotpriv/STOP errdslotunimpl/STOP
M_FBDS                             82/84  predicted 82/84  AS PREDICTED  red: usfu1dslot/TAILHALT sfu1hdslot/STOP
M_FBFRZDS                          83/84  predicted 83/84  AS PREDICTED  red: sfu1hdslot/STOP
M_RRUT                             84/84  predicted 84/84  AS PREDICTED  red: (none)
M_DS840UT                          84/84  predicted 84/84  AS PREDICTED  red: (none)
TABLE 20: SOME DIFFER
```

Table 20b, the corrected v24 (trapfrozen9dslot at br.n +16), the mutants that touch that row (PRETABLE_20b.out):

```
BASE                           84/84  predicted 84/84  AS PREDICTED  red: (none)
M_DS865                        72/84  predicted 72/84  AS PREDICTED  red: errdslotmisalign/STOP errdslotovf/STOP errdslotdiv0/STOP errdslotpriv/STOP errdslotunimpl/STOP trapfrozen7dslot/STOP trapfrozen10dslot/STOP trapfrozen4dslot/STOP trapfrozen5dslot/STOP trapfrozen6dslot/STOP trapfrozen8dslot/STOP trapfrozen9dslot/STOP
M_RRDS_INTEGER_OVERFLOW        83/84  predicted 83/84  AS PREDICTED  red: trapfrozen9dslot/STOP
M_ARMTS_INTEGER_OVERFLOW       82/84  predicted 82/84  AS PREDICTED  red: dslotovftb/HALT trapfrozen9dslot/HALT
M_DSNOT_INTEGER_OVERFLOW       80/84  predicted 80/84  AS PREDICTED  red: dslotovf/HALT errdslotovf/HALT dslotovftb/HALT trapfrozen9dslot/HALT
M_DSFRZ_INTEGER_OVERFLOW       82/84  predicted 82/84  AS PREDICTED  red: errdslotovf/HALT trapfrozen9dslot/HALT
M_RRTDS                        77/84  predicted 77/84  AS PREDICTED  red: trapfrozen7dslot/STOP trapfrozen10dslot/BADREGS trapfrozen4dslot/STOP trapfrozen5dslot/STOP trapfrozen6dslot/STOP trapfrozen8dslot/STOP trapfrozen9dslot/STOP
TABLE 20b: ALL AS PREDICTED
```

## 4. The grid, printed by `regress/artifacts/m88kexcdeliver/derive_cells.py` from its (hand-transcribed) row table

```
=== DELAY-SLOT x is_trap GRID -- v24, the SHIPPED instrument  (84 rows) ===
label     S0 D0 fault   S0 D0 trap    S0 D1 fault   S0 D1 trap    S1 D0 fault   S1 D0 trap    S1 D1 fault   S1 D1 trap   
MISALIGN  misalign +1   misaligntb    dslotmisalign dslotmisalign errc +3       trapfrozen4   errdslotmisal trapfrozen4ds
UNIMPL    unimpl        unimpltb +1   dslotunimpl   dslotunimpltb errunimpl     trapfrozen5   errdslotunimp trapfrozen5ds
PRIV      priv +1       privsuptb +1  dslotpriv     dslotprivtb   errpriv       trapfrozen6   errdslotpriv  trapfrozen6ds
BOUNDS    unreachable   bounds +2     unreachable   dslotbounds   unreachable   trapfrozen +4 unreachable   trapfrozen7ds
DIV0      div0 +37      div0tb +1     dslot         dslotdiv0tb   errdiv0       trapfrozen8   errdslotdiv0  trapfrozen8ds
OVF       indclr +5     ovftb +1      dslotovf      dslotovftb    errovf        trapfrozen9   errdslotovf   trapfrozen9ds
ERROR     unreachable   errortb +1    unreachable   dsloterror    unreachable   trapfrozen10  unreachable   trapfrozen10d
rowed 48 of 48 reachable cells of {7 labels} x {SFRZ} x {delay_slot} x {is_trap} (8 unreachable: is_trap 0 at BOUNDS/ERROR)

=== DELAY-SLOT x is_trap GRID -- v23, history  (73 rows) ===
label     S0 D0 fault   S0 D0 trap    S0 D1 fault   S0 D1 trap    S1 D0 fault   S1 D0 trap    S1 D1 fault   S1 D1 trap   
MISALIGN  misalign +1   misaligntb    dslotmisalign OPEN          errc +3       trapfrozen4   errdslotmisal OPEN         
UNIMPL    unimpl        unimpltb +1   dslotunimpl   OPEN          errunimpl     trapfrozen5   errdslotunimp OPEN         
PRIV      priv +1       privsuptb +1  dslotpriv     OPEN          errpriv       trapfrozen6   errdslotpriv  OPEN         
BOUNDS    unreachable   bounds +2     unreachable   dslotbounds   unreachable   trapfrozen +4 unreachable   trapfrozen7ds
DIV0      div0 +32      div0tb +1     dslot         OPEN          errdiv0       trapfrozen8   errdslotdiv0  OPEN         
OVF       indclr +4     ovftb +1      dslotovf      OPEN          errovf        trapfrozen9   errdslotovf   OPEN         
ERROR     unreachable   errortb +1    unreachable   dsloterror    unreachable   trapfrozen10  unreachable   trapfrozen10d
rowed 38 of 48 reachable cells of {7 labels} x {SFRZ} x {delay_slot} x {is_trap} (8 unreachable: is_trap 0 at BOUNDS/ERROR)

=== DELAY-SLOT x is_trap GRID -- v22, history  (63 rows) ===
label     S0 D0 fault   S0 D0 trap    S0 D1 fault   S0 D1 trap    S1 D0 fault   S1 D0 trap    S1 D1 fault   S1 D1 trap   
MISALIGN  misalign +1   misaligntb    dslotmisalign OPEN          errc +3       trapfrozen4   OPEN          OPEN         
UNIMPL    unimpl        unimpltb +1   dslotunimpl   OPEN          errunimpl     trapfrozen5   OPEN          OPEN         
PRIV      priv +1       privsuptb +1  dslotpriv     OPEN          errpriv       trapfrozen6   OPEN          OPEN         
BOUNDS    unreachable   bounds +2     unreachable   OPEN          unreachable   trapfrozen +4 unreachable   OPEN         
DIV0      div0 +25      div0tb +1     dslot         OPEN          errdiv0       trapfrozen8   OPEN          OPEN         
OVF       indclr +4     ovftb +1      dslotovf      OPEN          errovf        trapfrozen9   OPEN          OPEN         
ERROR     unreachable   errortb +1    unreachable   OPEN          unreachable   trapfrozen10  unreachable   OPEN         
rowed 29 of 48 reachable cells of {7 labels} x {SFRZ} x {delay_slot} x {is_trap} (8 unreachable: is_trap 0 at BOUNDS/ERROR)

=== DELAY-SLOT x is_trap GRID -- v21 (HEAD before 2026-10-16: v19's 59 rows)  (59 rows) ===
label     S0 D0 fault   S0 D0 trap    S0 D1 fault   S0 D1 trap    S1 D0 fault   S1 D0 trap    S1 D1 fault   S1 D1 trap   
MISALIGN  misalign +1   misaligntb    OPEN          OPEN          errc +3       trapfrozen4   OPEN          OPEN         
UNIMPL    unimpl        unimpltb +1   OPEN          OPEN          errunimpl     trapfrozen5   OPEN          OPEN         
PRIV      priv +1       privsuptb +1  OPEN          OPEN          errpriv       trapfrozen6   OPEN          OPEN         
BOUNDS    unreachable   bounds +2     unreachable   OPEN          unreachable   trapfrozen +4 unreachable   OPEN         
DIV0      div0 +25      div0tb +1     dslot         OPEN          errdiv0       trapfrozen8   OPEN          OPEN         
OVF       indclr +4     ovftb +1      OPEN          OPEN          errovf        trapfrozen9   OPEN          OPEN         
ERROR     unreachable   errortb +1    unreachable   OPEN          unreachable   trapfrozen10  unreachable   OPEN         
rowed 25 of 48 reachable cells of {7 labels} x {SFRZ} x {delay_slot} x {is_trap} (8 unreachable: is_trap 0 at BOUNDS/ERROR)

=== the FALLBACK x {SFRZ} x {delay slot} -- v24 ===
  usfu1dslot  ROWED  (SFRZ clear, in a slot): SFU1 must still HALT naming 0x072
  sfu1hdslot  ROWED  (SFRZ set, in a slot): SFU1 must still HALT naming 0x072
```

## 5. The repair -- `git diff` of the probe and gate 11 against HEAD c64445fa (v23) (9 hunks)

```diff
diff --git a/regress/gate_m88k_rounding.sh b/regress/gate_m88k_rounding.sh
index 063cb14d..810309fc 100644
--- a/regress/gate_m88k_rounding.sh
+++ b/regress/gate_m88k_rounding.sh
@@ -326,12 +326,12 @@ fi
 #  grew: every trap-like class stopped the machine.  With the final instrument the 7 are resid50, resid127,
 #  resid11, resid50ind, resid50c and usfu1, whose CORRECT answer is HALT, and the pre-existing user vector 128 (usertb); sfu1h reads STOP
 #  on HEAD because the FIRST divu halts on vector 0x008, not its own 0x072 -- probe10_head.out /
-#  probe_v3_head.out .. probe_v11_head.out) and the DETECTOR (73 fault rows -- 59 until v22, 63 in v22, 2026-10-16 -- + 2
+#  probe_v3_head.out .. probe_v11_head.out) and the DETECTOR (84 fault rows -- 59 until v22, 63 in v22, 73 in v23, 2026-10-16 -- + 2
 #  controls; kill tables killtable/, killtable2/, killtable3/, killtable4/ + killtable4b/
 #  (M_TAILRETURN), killtable5/ (the {class} x {MODE} and {SFRZ set, non-trap} x {class} closures), killtable6/ (the fallback far bound, resid127), killtable7/ (the frozen-TRAP rows per class), killtable8/ (the fallback in user mode, usfu1), killtable10/ (the frozen ERROR trap, the near bound, the fallback PSR-bit cells, the frozen user trap, the refatal channel; table 9 was folded into it), killtable11/ (the frozen traps naming the 0x1c2, MVMEPROM and 511 labels; the ERROR-arm-frozen and MISALIGNED-C representatives; the re-route x {IND, C} cells, errind/errc), killtable12/ (the re-route TRAP side x {IND, C}: both swept 46/46 before the rows existed), killtable13/ (the six previously-sweeping mutants, all killed), killtable14/ (grok's three predicted SER sweeps -- each 54/54 on the frozen v16 instrument and killed on v17 by its own row)
 #  under regress/artifacts/m88kexcdeliver/).  Only the detector half runs here.
 #
-#  The pins are NAMED so that deleting a row is visible: `M88KEXC_RESULT=73/73' pins the
+#  The pins are NAMED so that deleting a row is visible: `M88KEXC_RESULT=84/84' pins the
 #  denominator (a row that stops running shrinks it); resid50 and sfu1h are the two rows
 #  whose CORRECT answer is HALT -- they separate the shipped fix from a form that delivers
 #  every vector (the rejected D4) or SFU1 (row m88kexcsfu1); vbrtb is the one ANCHORED row
@@ -350,18 +350,18 @@ if ! grep -q "M88KEXC_DONE" "$EXCLOG"; then
 else
     check "m88k exc: CR parse self-test (PSR at reset == 0x80000002)" \
           "$(grep -c 'M88KEXC_SELFTEST=OK' "$EXCLOG")" "1"
-    check "m88k exc: 73 fault rows, all as expected (the denominator is the pin)" \
-          "$(grep -c 'M88KEXC_RESULT=73/73' "$EXCLOG")" "1"
+    check "m88k exc: 84 fault rows, all as expected (the denominator is the pin)" \
+          "$(grep -c 'M88KEXC_RESULT=84/84' "$EXCLOG")" "1"
     #  v22, repair 13 (2026-10-16): {class} x {delay slot}.  Before it only DIV0 faulted in a delay slot, and the
     #  form implemented = !cpu->delay_slot at MISALIGNED/UNIMPL/PRIV/OVF swept the 59-row probe clean at all four arms
     #  (artifacts/m88kexcdeliver/delayslot_20261016/).  BOUNDS and ERROR in a slot need a trap instruction there,
     #  which the manual does not settle -- disclosed in the probe's contract (repair13_20261016/, table 16).
     #  v23, repair 14: the delay-slot GRID, {7 labels} x {SFRZ} x {delay_slot} (table 19).  Unfrozen, all seven labels:
-    check "m88k exc: a fault IN A DELAY SLOT is delivered at all seven labels (dslot 0x40, dslotmisalign 0x20, dslotunimpl 0x28, dslotpriv 0x30, dslotovf 0x48, dslotbounds 0x38, dsloterror 0x50)" \
-          "$(grep -cE '^M88KEXC_ROW=(dslot +RESULT=DELIVER +pc=0x00000040|dslotmisalign +RESULT=DELIVER +pc=0x00000020|dslotunimpl +RESULT=DELIVER +pc=0x00000028|dslotpriv +RESULT=DELIVER +pc=0x00000030|dslotovf +RESULT=DELIVER +pc=0x00000048|dslotbounds +RESULT=DELIVER +pc=0x00000038|dsloterror +RESULT=DELIVER +pc=0x00000050) ' "$EXCLOG")" "7"
+    check "m88k exc: a fault or a TRAP in a delay slot is delivered at all seven labels (the seven dslot<L> fault rows and, v24, the five dslot<L>tb trap rows)" \
+          "$(grep -cE '^M88KEXC_ROW=(dslot +RESULT=DELIVER +pc=0x00000040|dslotmisalign +RESULT=DELIVER +pc=0x00000020|dslotunimpl +RESULT=DELIVER +pc=0x00000028|dslotpriv +RESULT=DELIVER +pc=0x00000030|dslotovf +RESULT=DELIVER +pc=0x00000048|dslotbounds +RESULT=DELIVER +pc=0x00000038|dsloterror +RESULT=DELIVER +pc=0x00000050|dslotmisaligntb +RESULT=DELIVER +pc=0x00000020|dslotunimpltb +RESULT=DELIVER +pc=0x00000028|dslotprivtb +RESULT=DELIVER +pc=0x00000030|dslotdiv0tb +RESULT=DELIVER +pc=0x00000040|dslotovftb +RESULT=DELIVER +pc=0x00000048) ' "$EXCLOG")" "12"
     #  ... and FROZEN, all seven labels, plus the fallback row:
-    check "m88k exc: with SFRZ set, a slot fault is still re-routed (errdslot* at 0x50) and a slot trap still exempt (trapfrozen7dslot 0x38, trapfrozen10dslot 0x50); SFU1 in a slot still halts (usfu1dslot)" \
-          "$(grep -cE '^M88KEXC_ROW=(errdslot(misalign|ovf|div0|priv|unimpl) +RESULT=DELIVER +pc=0x00000050|trapfrozen7dslot +RESULT=DELIVER +pc=0x00000038|trapfrozen10dslot +RESULT=DELIVER +pc=0x00000050|usfu1dslot +RESULT=HALT) ' "$EXCLOG")" "8"
+    check "m88k exc: with SFRZ set, a slot fault is still re-routed (errdslot* at 0x50) and a slot trap still exempt at all seven labels (trapfrozen<L>dslot); SFU1 in a slot still halts, frozen or not (usfu1dslot, sfu1hdslot)" \
+          "$(grep -cE '^M88KEXC_ROW=(errdslot(misalign|ovf|div0|priv|unimpl) +RESULT=DELIVER +pc=0x00000050|trapfrozen7dslot +RESULT=DELIVER +pc=0x00000038|trapfrozen10dslot +RESULT=DELIVER +pc=0x00000050|usfu1dslot +RESULT=HALT|trapfrozen4dslot +RESULT=DELIVER +pc=0x00000020|trapfrozen5dslot +RESULT=DELIVER +pc=0x00000028|trapfrozen6dslot +RESULT=DELIVER +pc=0x00000030|trapfrozen8dslot +RESULT=DELIVER +pc=0x00000040|trapfrozen9dslot +RESULT=DELIVER +pc=0x00000048|sfu1hdslot +RESULT=HALT) ' "$EXCLOG")" "14"
     check "m88k exc: IND set by the exception path from a pre-fault PSR with IND clear (indclr)" \
           "$(grep -cE '^M88KEXC_ROW=indclr +RESULT=DELIVER .*psr=0x8000000b .*epsr=0x80000000' "$EXCLOG")" "1"
     check "m88k exc: user-mode MISALIGNED and OVERFLOW deliver (umisalign 0x20, uovf 0x48 -- the {class} x {MODE} closure)" \
diff --git a/regress/m88k_exc_probe.py b/regress/m88k_exc_probe.py
index 4db06b5b..5b20e719 100644
--- a/regress/m88k_exc_probe.py
+++ b/regress/m88k_exc_probe.py
@@ -50,6 +50,11 @@ rather than executing zeros, `breakpoint add <8*vector>`, `continue`, then `reg`
              still re-routed to ERROR (0x50, refatal); a trap is still exempt (0x38 / 0x50, no refatal).  +8, never +16:
              0x40 + 16 is the ERROR entry, so a lost delivery would land on the row's own breakpoint      0x50/0x38/0x50
   usfu1dslot v23: SFU1 (114) raised in a delay slot still HALTs at the fallback, naming 0x072
+  dslotmisaligntb/unimpltb/privtb/div0tb/ovftb, trapfrozen4/5/6/8/9dslot   v24 (repair 15): a TRAP instruction (tb1
+             naming the label) in a slot at the five instruction labels, unfrozen (br.n +16, else-arm shadows) and frozen
+             (br.n +8 in the handler, exempt, frozen shadows -- +16 for trapfrozen9dslot, whose +8 target would be its own
+             OVERFLOW breakpoint 0x48: table 20 measured that, table 20b the fix) -- the is_trap axis  0x20/0x28/0x30/0x40/0x48
+  sfu1hdslot v24: SFU1 in a slot with SFRZ set (the frozen handler's legal divu) still HALTs, naming 0x072
   errortb    tb1  0,r3,10 (r3=1)      f003d80a  supervisor trap naming ERROR (10) directly -- the
              only route to switch 1's ERROR arm (the double-fault route enters at the re-route AFTER
              switch 1, so it cannot see that arm: M_ERRORDROP escaped the error row 9/9, table 1)  0x50
@@ -206,13 +211,16 @@ this emulator behaves: the MC88100 manual does not define a trap in a slot, and
 CLAIM, not whether the cell is owed); the (SFRZ set, slot) column by errdslotmisalign, errdslotovf, errdslotdiv0,
 errdslotpriv, errdslotunimpl, trapfrozen7dslot and trapfrozen10dslot (line 865's write is what X(br_n) reads to keep the
 vector over the branch target); and the fallback, clause (e) but rowed on its measured escape, by usfu1dslot.  Table 19
-(artifacts/m88kexcdeliver/repair13_20261016/).  OPEN, NOT DISCLOSED -- pass 15 (Fable 5.1, GLM 5.3) overturned that filing:
-the delivery path also TESTS is_trap (:816), so a TRAP in a slot at the five instruction labels is floor (the carrier's
-generating-set clause; the chain's own *tb and trapfrozen<L> rows already write is_trap both ways at every slot-0 cell), and
-`if (!is_trap || (vector == L && cpu->delay_slot))' swept this instrument 73/73 at each of the five (table 19) -- repair
-15 owes ten rows.  Disclosed, clause (e): {delay slot} x {a PSR bit other than SFRZ} (copied or ORed, never tested); the
+(artifacts/m88kexcdeliver/repair13_20261016/).  Pass 15 (Fable 5.1, GLM 5.3) then found the fourth tested input: is_trap
+(:816).  By the carrier's generating-set clause and the chain's own *tb and trapfrozen<L> rows, a TRAP in a slot at the five
+instruction labels is floor, and `if (!is_trap || (vector == L && cpu->delay_slot))' had swept v23 73/73 at each of the five
+(table 19).  v24 (repair 15) rows them: dslot<L>tb unfrozen and trapfrozen<L>dslot frozen, so the grid is {7 labels} x
+{SFRZ} x {slot} x {is_trap} -- 56 cells, 8 unreachable (no non-trap raise site names 7 or 10), 48 reachable, ALL ROWED;
+the function has no fifth tested input.  sfu1hdslot rows the fallback's frozen slot cell (clause (e)).  Table 20.
+Disclosed, clause (e): {delay slot} x {a PSR bit other than SFRZ} (copied or ORed, never tested); the
 user-trap labels (128, 0x1c2, MVMEPROM_VECTOR, the default) x {slot}, outside the fix's seven labels -- their delivery
-predates #502 (named by GLM 5.3 on pass 15); and vectors 0..3's own delay-slot code (upstream; its coverage debt is
+predates #502 (named by GLM 5.3 on pass 15; MEASURED escapes in table 20, `!is_trap || (vector >= USER_TRAPS_START &&
+cpu->delay_slot)' at :816 and `cpu->delay_slot && vector < USER_TRAPS_START' at :840, 84/84 each); and vectors 0..3's own delay-slot code (upstream; its coverage debt is
 m88kexcdebt -- the tail arms themselves are m88kexchwtraps, a different defect; Grok 4.7, pass 15)); a trap re-routed to ERROR while frozen, per class ({SFRZ set, is_trap} x {every switch-1 label a trap can NAME -- 0..3 are deliverable too and are unrowed, disclosed as
 m88kexchwtraps; the word EVERY overclaimed until v16}: trapfrozen (7),
 trapfrozen4/5/6/8/9/10/128/450/496/511 -- the ten labels 4..10, 128, 0x1c2, MVMEPROM_VECTOR, enumerated from switch 1's `case' list, plus
@@ -394,6 +402,40 @@ ROWS = [
     #  (c) the fallback, which is clause (e) by the carrier's tests-not-reads criterion (all four pass-14 seats), rowed
     #  because its escape was measured (table 17: `&& !cpu->delay_slot' at the fallback swept v22 63/63).
     ("usfu1dslot", [STCR_R5_CR1, BR_N_PLUS16, DIVU_R6_R5_R4], {"r5": PSR_USERSFD1, "r4": 0x10}, V_SFU1, 0x1000c, PSR_USERSFD1, None),
+    #  ---- v24, repair 15 (2026-10-16): THE is_trap AXIS.  m88k_exception() tests FOUR inputs -- vector, PSR & SFRZ,
+    #  cpu->delay_slot and is_trap (:816) -- and v23 crossed the labels with the first three only, rowing a TRAP in a slot
+    #  just where the trap is the only route (7, 10).  `if (!is_trap || (vector == L && cpu->delay_slot))' then swept v23
+    #  73/73 at each of the five instruction labels (table 19) -- floor breaches, by the carrier's generating-set clause
+    #  and the chain's own *tb / trapfrozen<L> rows, which already write is_trap both ways at every slot-0 cell (Fable
+    #  5.1, pass 15, against its own pass-14 ruling).  The grid is now {7 labels} x {SFRZ} x {slot} x {is_trap}, 48
+    #  reachable cells, and the function has no fifth tested input to enumerate.
+    #  (a) a TRAP in a slot, unfrozen, at the five instruction labels (else-arm shadows, as every dslot* row):
+    ("dslotmisaligntb", [BR_N_PLUS16, TB1_0_R3_4], {"r3": 1},                    V_MISALIGN, 0x10008, PSR_RESET, None),
+    ("dslotunimpltb", [BR_N_PLUS16, TB1_0_R3_5], {"r3": 1},                      V_UNIMPL,   0x10008, PSR_RESET, None),
+    ("dslotprivtb", [BR_N_PLUS16, TB1_0_R3_6],  {"r3": 1},                       V_PRIV,     0x10008, PSR_RESET, None),
+    ("dslotdiv0tb", [BR_N_PLUS16, TB1_0_R3_8],  {"r3": 1},                       V_DIV0,     0x10008, PSR_RESET, None),
+    ("dslotovftb", [BR_N_PLUS16, TB1_0_R3_9],   {"r3": 1},                       V_OVF,      0x10008, PSR_RESET, None),
+    #  (b) a FROZEN trap in a br.n +8 slot at the same five: still exempt, delivered to its own vector, no refatal.
+    ("trapfrozen4dslot", [DIVU_R2_R3_R0],       {"r3": 0x11},                    V_MISALIGN, 0x10004, PSR_RESET,
+                 [BR_N_PLUS8, TB1_0_R3_4]),
+    ("trapfrozen5dslot", [DIVU_R2_R3_R0],       {"r3": 0x11},                    V_UNIMPL,   0x10004, PSR_RESET,
+                 [BR_N_PLUS8, TB1_0_R3_5]),
+    ("trapfrozen6dslot", [DIVU_R2_R3_R0],       {"r3": 0x11},                    V_PRIV,     0x10004, PSR_RESET,
+                 [BR_N_PLUS8, TB1_0_R3_6]),
+    ("trapfrozen8dslot", [ADD_R2_R3_R4],        {"r3": 0x7fffffff, "r4": 1},     V_DIV0,     0x10004, PSR_RESET,
+                 [BR_N_PLUS8, TB1_0_R3_8], V_OVF),            # trapfrozen8's shape: first fault OVERFLOW, handler at
+                                                              # 0x48 because the row's breakpoint is 0x40; br.n +8 from 0x48
+                                                              # targets 0x50's SELF, safe HERE since the breakpoint is 0x40
+    ("trapfrozen9dslot", [DIVU_R2_R3_R0],       {"r3": 0x11},                    V_OVF,      0x10004, PSR_RESET,
+                 [BR_N_PLUS16, TB1_0_R3_9]),                  # +16, NOT +8: from 0x40, +8 targets 0x48 -- the OVERFLOW
+                                                              # entry, THIS row's own breakpoint -- so a lost delivery read
+                                                              # DELIVER (table 20: `:865' unconditioned on the frozen path
+                                                              # left this row green, 73/84).  +16 targets 0x50's SELF,
+                                                              # safe here because this row's breakpoint is 0x48
+    #  (c) the fallback's (SFRZ set, slot) cell -- clause (e) like usfu1dslot, rowed on its measured escape: a frozen
+    #  handler's legal divu with SFD1 set, in a slot, raises SFU1 and must still HALT naming 0x072.
+    ("sfu1hdslot", [DIVU_R2_R3_R0],             {"r3": 0x10, "r5": 0x60, "r4": 0x10}, V_SFU1, 0x10004, PSR_RESET,
+                 [BR_N_PLUS8, DIVU_R6_R5_R4]),
     ("errortb",  [TB1_0_R3_10],                 {"r3": 1},                       V_ERROR,    0x10004, PSR_RESET, None),
     ("misaligntb", [TB1_0_R3_4],                {"r3": 1},                       V_MISALIGN, 0x10004, PSR_RESET, None),
     ("unimpltb", [TB1_0_R3_5],                  {"r3": 1},                       V_UNIMPL,   0x10004, PSR_RESET, None),
@@ -537,7 +579,7 @@ VBR_OF = {"vbrtb": VBR_TEST}                     # rows that relocate the vector
 #  NEGATIVE CONTROLS: rows whose CORRECT result is the fallback HALT.  They pin the boundary the diff keeps on purpose --
 #  vectors 11..113/116..127 and SFU1 (114/115) still stop the machine -- and separate the shipped D1 form from the rejected
 #  D4 (tail-default-delivers) and from delivering SFU1 (row m88kexcsfu1).  A mutant that delivers them turns these rows RED.
-EXPECT_RESULT = {"usfu1dslot": "HALT", "resid50": "HALT", "resid127": "HALT", "resid11": "HALT", "resid50ind": "HALT", "resid50c": "HALT", "resid50ser": "HALT", "sfu1h": "HALT", "usfu1": "HALT"}
+EXPECT_RESULT = {"sfu1hdslot": "HALT", "usfu1dslot": "HALT", "resid50": "HALT", "resid127": "HALT", "resid11": "HALT", "resid50ind": "HALT", "resid50c": "HALT", "resid50ser": "HALT", "sfu1h": "HALT", "usfu1": "HALT"}
 PSR_WANT = {"errc": 0x9000000b,   # v14: exception entry ORs MODE|SFRZ|IND|SFD1 and leaves C alone (mc88100 manual: "the shadow freeze,
                                   #      SFD1, and IND bits of the PSR are set"), so the C-set handler row keeps C -- table 11 BASE read
                                   #      45/46 bad=psr on this row before any mutant: a MIS-CUT ROW, not the fix (case 3)
@@ -550,7 +592,7 @@ PSR_WANT = {"errc": 0x9000000b,   # v14: exception entry ORs MODE|SFRZ|IND|SFD1
             "errser": 0xa000000b}                # v17: the non-trap re-route with SER set -- also the MISALIGNED x SER cell
 #  indclr wants the default PSR_EXC (0x8000000b): IND was CLEAR before the fault and must be SET by the exception path;
 #  EPSR keeps the pre-fault 0x80000000.  A write that drops `| M88K_PSR_IND' leaves 0x80000009 -> bad=psr.
-EXPECT_VECTOR = {"usfu1dslot": 0x072, "resid50": 0x032, "resid127": 0x07f, "resid11": 0x00b, "resid50ind": 0x032, "resid50c": 0x032, "resid50ser": 0x032, "sfu1h": 0x072, "usfu1": 0x072}
+EXPECT_VECTOR = {"sfu1hdslot": 0x072, "usfu1dslot": 0x072, "resid50": 0x032, "resid127": 0x07f, "resid11": 0x00b, "resid50ind": 0x032, "resid50c": 0x032, "resid50ser": 0x032, "sfu1h": 0x072, "usfu1": 0x072}
 #  (the vector the fallback diagnostic must NAME for an expected-HALT row -- the comment that used to trail the dict above)
 #  refatal: the re-route prints `[ SFRZ already set in PSR => ERROR ]' (fatal() is a plain print in this fork); a re-routed non-trap row
 #  must SEE it, a frozen-trap row must NOT -- the channel that tells the exemption arm from the re-route arm when both land on 0x50
@@ -562,7 +604,9 @@ REFATAL_EXPECT = {"error": True, "errovf": True, "errdiv0": True, "errpriv": Tru
                   "trapfrozenind": False, "trapfrozenc": False, "trapfrozenser": False,
                   "trapfrozenuser": False, "trapfrozensfd1": False,
                   "errdslotmisalign": True, "errdslotovf": True, "errdslotdiv0": True, "errdslotpriv": True,
-                  "errdslotunimpl": True, "trapfrozen7dslot": False, "trapfrozen10dslot": False}   # v23   # v19: the exemption must hold with MODE and
+                  "errdslotunimpl": True, "trapfrozen7dslot": False, "trapfrozen10dslot": False,   # v23
+                  "trapfrozen4dslot": False, "trapfrozen5dslot": False, "trapfrozen6dslot": False,
+                  "trapfrozen8dslot": False, "trapfrozen9dslot": False}                             # v24   # v19: the exemption must hold with MODE and
                   #      SFD1 clear too -- and this is the CHANNEL that makes the two rows non-vacuous, because the
                   #      mutant re-routes the trap and the diagnostic then APPEARS where these expect none
 #  (v12 COPIED this dict's trailing comment up to EXPECT_VECTOR, where it belongs, and claimed to have REMOVED it here.
@@ -708,7 +752,8 @@ def run_row(name, prog, regs, vector, fault_pc, epsr_exp, handler, grace=6.0, ha
                     "trapfrozen450", "trapfrozen496", "trapfrozen511",
                     "trapfrozenind", "trapfrozenc", "trapfrozenser", "trapfrozenuser", "trapfrozensfd1",
                     "errdslotmisalign", "errdslotovf", "errdslotdiv0", "errdslotpriv", "errdslotunimpl",
-                    "trapfrozen7dslot", "trapfrozen10dslot"):
+                    "trapfrozen7dslot", "trapfrozen10dslot",
+                    "trapfrozen4dslot", "trapfrozen5dslot", "trapfrozen6dslot", "trapfrozen8dslot", "trapfrozen9dslot"):
             # the second fault runs with SFRZ set: the shadows stay FROZEN at the first fault's values.  For
             # `trapfrozen' the second fault is a TRAP, which the manual (:8633-8636, 6.10 :10613-10614) exempts from
             # the ERROR re-route: it must deliver to ITS OWN vector (0x38), shadows still frozen.  M_SFRZTRAP sends it to 0x50.
```

## 6. The enclosing function -- `m88k_exception()`, `src/cpus/cpu_m88k.c` at HEAD (lines 689-981, unchanged)

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

## 7. Pass 15's findings, consolidated -- with the coordinator's disposition on each

K1 (Fable 5.1) `is_trap` is the fourth tested input; the ten trap-in-slot cells at the five instruction labels are floor; table
   19's five 73/73 are L2.  **ACCEPTED** -- the ten rows are this diff (`dslot<L>tb`, `trapfrozen<L>dslot`); table 20.
K2 (Fable 5.1) the arm-level `implemented = !(cpu->delay_slot && is_trap)` at the five labels is a PREDICTED 73/73 sweep of v23.
   **ACCEPTED** -- MEASURED on v24 in table 20 (M_ARMTS_<L>) and killed; its SFRZ-clear-only twin M_ARMTSU_<L> isolates the
   unfrozen cell's own row.
K3 (GLM 5.3) the user-trap labels x {slot} were unnamed.  **ACCEPTED as a DISCLOSURE** (Fable's classification), with the two
   escapes MEASURED in table 20 (`!is_trap || (vector >= USER_TRAPS_START && cpu->delay_slot)` at :816;
   `cpu->delay_slot && vector < USER_TRAPS_START` at :840).  GLM's alternative -- two representative rows -- is D6.
K4 (Fable 5.1) {fallback} x {SFRZ} x {slot} should be named.  **ACCEPTED, ROWED**: `sfu1hdslot` (clause (e), rowed on its
   measured escape M_FBFRZDS).
K5 (Grok 4.7) the vectors-0..3 pointer.  **ACCEPTED, committed** (16512e9c).
K6 (Fable 5.1) name both probe md5s; (Astra) the deriver's grid is hand-transcribed, not a reachability proof.  **ACCEPTED**:
   the commit names the md5s; the grid's credits are re-checked against the row definitions by this pass (Q1).
K7 (Grok 4.7, GLM 5.3) Q7's 78 double-counted or mis-attributed the re-route buckets.  **ACCEPTED in part**: the 5+5 re-route
   buckets are PSR-bit cells at the re-route (CELLCENSUS "SFRZ RE-ROUTE" sections), not the grid's (SFRZ set, slot clear)
   cells, so they are not double-counted -- but they are clause (e) by G7 (untested PSR bits), and Q7 below drops the 78 in
   favour of naming the floor alone.
K8 (all) the ledger write must land.  **DONE**: 16512e9c's ledger carries the close adjudication, passes 14 and 15, the five
   unfired seats by name, both repairs and the m88ksfd1row closure.

## 8. Disagreements, both sides in their own words

D5 -- is `is_trap` a floor axis?
   * Grok 4.7: "Pass 11's owed floor is the switch-1 labels crossed with the device-state lvalues the repair path tests ...
     `is_trap` is a parameter, tested only inside the SFRZ block.  A joint the body distinguishes and that product does not
     owe is clause (e)."
   * GPT-6 Astra: "Under the carrier's device-state bound, `is_trap` is a per-raise selector rather than another persistent
     state axis.  Their disclosure as clause-(e) debt is therefore defensible."
   * Fable 5.1: "`is_trap` is this function's one input bit, tested as a case; `if (!is_trap || (vector == L &&
     cpu->delay_slot))` is a state x input-bit joint at a label -- the M_ICLR shape exactly ... The v23 mutant is that same
     mutant with `&& cpu->delay_slot` appended.  My 'sub-cell' argument would have excused trapfrozen4..9 too, and the chain
     did not accept it there."
   * Coordinator: Fable's, as section 1 says.  Grok and Astra -- if this is wrong, name the carrier text that excludes an input
     bit the body tests from the generating set, and say what grade the pass-5/7 repairs should then have had.
D6 -- the user-trap labels: rows (GLM) or disclosure (Fable)?
   * GLM 5.3: "Remedy: two representative rows (`usertbdslot`, a frozen 128-in-slot) or a disclosure line naming the family
     with a tracker, like the 0..3 line."
   * Fable 5.1: "outside the fix's labels (trapfrozen128/450/496/511 were voluntary closures of the exemption's label range),
     so disclose rather than row."
   * Coordinator: disclosure, with both escapes measured; the rows would pin pre-#502 behaviour the fix never touched.

## 9. Questions (VERDICT LINE FIRST)

Q1. Verify the grid in section 4 against the rows in section 5: for each of the 48 reachable cells, does the credited row raise
    that label with that SFRZ state, slot state and is_trap value?  Are the 8 unreachable cells really unreachable?
Q2. Is any of the eleven new rows vacuous -- unable to red under the mutant it is credited with?  (Table 20 measures each.)
Q3. Is the four-input claim of section 2 right?  If the function tests a fifth input, name it with a reachable cell and a
    single edit that sweeps the 84-row probe.  Otherwise: inside the 48 cells, any sweeping single edit?
Q4. Are the disclosures complete and correctly classified: user-trap labels x {slot} (measured escapes), {slot} x {PSR bits
    other than SFRZ}, vectors 0..3's own delay-slot code (`m88kexcdebt`)?
Q5. D5 and D6.
Q6. Which of the coordinator's ACCEPTED dispositions K1-K8 is wrong?
Q7. If nothing survives: CLOSE, with the denominator -- the floor is the 48 reachable cells of {7 labels} x {SFRZ} x
    {delay_slot} x {is_trap}, all rowed and each killed under its own mutant in table 20; everything else enumerated is
    clause (e) (closed voluntarily or disclosed with a measured escape).  Is that complete?

Seat notes: Fable 5.1 -- the is_trap axis was yours; check the ten rows' traces and the unreachable-cell claim harder than
anyone.  GPT-6 Astra and Grok 4.7 -- D5 was ruled against you; answer it on the carrier's text.  GLM 5.3 -- D6 is yours;
say "not checkable from the packet" where that is true.
