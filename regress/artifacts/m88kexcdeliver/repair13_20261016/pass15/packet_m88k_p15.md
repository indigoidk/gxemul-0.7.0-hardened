# PASS 15 -- `m88kexcdeliver` (#502): VERIFY THE ENUMERATION of repair 14 (probe v23), and adjudicate pass 14's findings

Four seats, by the owner's roster of 2026-10-16: Fable 5.1, GPT-6 Astra, Grok 4.7, GLM 5.3.  The other five (Opus, agy,
kimi, deepseek, minimax) are DELIBERATELY NOT FIRED under that roster.  An ordinary regression-detector coverage review.
READ-ONLY: write nothing to any project tree.  The tree under review is `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC` (HEAD
7b23b785 plus the uncommitted probe v22 + v23 in the working tree); ignore the pristine upstream copy at
`C:/DocumentNoSnc/cc/GXEMUL/src/`.  Everything a packet-fed seat needs is inlined.

**Please do not simply ratify, and do not hunt cells the enumeration already names.**  Passes 13 and 14 each found cells of
one class -- the delay-slot axis -- open, so by the carrier's class-closure rule this repair closes the WHOLE space in one
diff and states which cells it rows and which it deliberately does not.  This pass's job is to VERIFY THAT ENUMERATION:
is it complete, is every cell really reached by the row credited with it, and is every disclosure correctly classified.

**One correction to the naming, before anything else:** HEAD's probe is ALREADY v21 (`m88k_exc_probe.v20.frozen.py` and
`.v21.frozen.py` are earlier records-only revisions).  So the pass-14 packet's "v20" is **v22** (repair 13, the four
`dslot*` rows), and this repair is **v23**.  `repair13_20261016/NAMING.txt` maps every file.

Open with your seat token -- `FABLE_M88KP15_20261016` / `ASTRA_M88KP15_20261016` / `GROK_M88KP15_20261016` /
`GLM_M88KP15_20261016` -- then ONE line: `VERDICT: CLOSE / DO NOT CLOSE (<one line>)`.

## 1. What pass 14 found (all four answers are in `repair13_20261016/pass14/`)

* **Fable 5.1 -- DO NOT CLOSE.** The delivery path TESTS two state values, `PSR & SFRZ` (:811) and `cpu->delay_slot` (:840,
  and :865 whose write `X(br_n)` reads to keep the exception vector over the branch target).  By the carrier's floor bound --
  the guard's dominating predicates (the switch-1 labels) x the state values the repair path tests that are jointly reachable
  -- the floor for this axis is **{7 labels} x {SFRZ} x {delay_slot} = 28 cells**; v22 rowed 19.  It also overturned its own
  pass-13 F2: BOUNDS/ERROR in a slot are FLOOR ("manual silence decides what a row may CLAIM, not whether the cell is owed"),
  and named a geometry trap (below).
* **GPT-6 Astra -- DO NOT CLOSE.** The same BOUNDS/ERROR cells floor; the SFRZ re-route's non-trap and trap sides x {slot}
  floor; the fallback clause (e).  Predicted `if (!is_trap && !cpu->delay_slot)` and `if (!is_trap || cpu->delay_slot)` at
  :816 sweep v22 63/63.
* **Grok 4.7 -- CLOSE.** Fallback and frozen sites clause (e) ("`if (!is_trap && !cpu->delay_slot)` ... is the disclosed
  joint: it adds `delay_slot` to the `is_trap` test"); BOUNDS/ERROR disclosed.  Found `OUTSTANDING_BUGS.md` stale.
* **GLM 5.3 -- CLOSE**, with the frozen-site label "a guess" and the advice to MEASURE it: "Running the already-designed
  `errdslot` is the cheapest way to convert this guess into a warrant."

## 2. What was measured since (logs and PRETABLEs in `regress/artifacts/m88kexcdeliver/repair13_20261016/`)

* **Table 17 (v22):** Astra's two re-route mutants and GLM's fallback mutant each **63/63** -- all three escapes real.
* **Table 18 (a candidate, NOT shipped):** five rows covering ten site cells -- every mutant killed -- but two of its rows used
  `br.n +16` inside the handler at 0x40, whose target 0x50 IS the ERROR entry: a mutant that loses the ERROR delivery would
  land on the row's own breakpoint and read DELIVER.  Fable named the trap; v23 uses `br.n +8` in every handler.
* **Table 19 (v23, the shipped form)** and **table 19b (Fable's two predicted v22 sweeps, measured on v22):** section 4.
* **Gate 11 ran on v22**: PASS, 110 checks (`gate11.out`) -- Fable's pass-14 answer said no gate run existed; it did, in this
  directory.  Gate 11 re-runs on v23 before the commit.

## 3. Settled premises (warrants inline; challenge any of them)

* `m88k_exception()` (section 6, HEAD, untouched) TESTS `vector`, `!implemented` (799), `PSR & SFRZ` (811), `is_trap` (816,
  only inside the SFRZ block), and `cpu->delay_slot` (840 inside `if (update_shadow_regs)`; 865 on every path past the
  fallback).  No other PSR bit is masked or compared.
* `X(br_n)` (`cpu_m88k_instr.c:92-106`): sets `delay_target`, `delay_slot = TO_BE_DELAYED`, runs the slot's handler, then
  `if (!(cpu->delay_slot & EXCEPTION_IN_DELAY_SLOT)) { delay_slot = NOT_DELAYED; pc = delay_target; ... } else delay_slot =
  NOT_DELAYED;` -- so :865's write decides whether a slot fault keeps its vector.
* `X(tb1)` (`:2553-2565`): `SYNCH_PC`; a user-mode trap naming a vector below 128 raises PRIVILEGE with is_trap 0; otherwise
  `m88k_exception(vector, 1)`.  No delay-slot guard.
* The probe plants `br .` (SELF) at every listed vector entry, then a row's handler words at `8*handler_at`, then SELF after
  them -- so `br.n +8` at 0x40 targets the SELF at 0x48 (two-word handler) or, from 0x44, the SELF at 0x4c (three-word).
* The second fault of every two-fault row runs FROZEN (each handler keeps SFRZ set); EPSR keeps the first fault's PSR.

## 4. Tables 19 and 19b (measured; PRETABLE_19.out / PRETABLE_19b.out written first, each in its own file)

"red" lists the rows whose RESULT differs from what the probe expects (eight rows -- nine in v23 -- expect HALT by design).

```
== TABLE 19 (instrument m88k_exc_probe_v23.FROZEN.py)
BASE                               73/73  predicted 73/73  AS PREDICTED  red: (none)
M_DSNOT_MISALIGNED_ACCESS          71/73  predicted 71/73  AS PREDICTED  red: dslotmisalign/HALT errdslotmisalign/HALT
M_DSFRZ_MISALIGNED_ACCESS          72/73  predicted 72/73  AS PREDICTED  red: errdslotmisalign/HALT
M_DSNOT_UNIMPLEMENTED_OPCODE       71/73  predicted 71/73  AS PREDICTED  red: dslotunimpl/HALT errdslotunimpl/HALT
M_DSFRZ_UNIMPLEMENTED_OPCODE       72/73  predicted 72/73  AS PREDICTED  red: errdslotunimpl/HALT
M_DSNOT_PRIVILEGE_VIOLATION        71/73  predicted 71/73  AS PREDICTED  red: dslotpriv/HALT errdslotpriv/HALT
M_DSFRZ_PRIVILEGE_VIOLATION        72/73  predicted 72/73  AS PREDICTED  red: errdslotpriv/HALT
M_DSNOT_BOUNDS_CHECK_VIOLATION     71/73  predicted 71/73  AS PREDICTED  red: dslotbounds/HALT trapfrozen7dslot/HALT
M_DSFRZ_BOUNDS_CHECK_VIOLATION     72/73  predicted 72/73  AS PREDICTED  red: trapfrozen7dslot/HALT
M_DSNOT_ILLEGAL_INTEGER_DIVIDE     71/73  predicted 71/73  AS PREDICTED  red: dslot/HALT errdslotdiv0/HALT
M_DSFRZ_ILLEGAL_INTEGER_DIVIDE     72/73  predicted 72/73  AS PREDICTED  red: errdslotdiv0/HALT
M_DSNOT_INTEGER_OVERFLOW           71/73  predicted 71/73  AS PREDICTED  red: dslotovf/HALT errdslotovf/HALT
M_DSFRZ_INTEGER_OVERFLOW           72/73  predicted 72/73  AS PREDICTED  red: errdslotovf/HALT
M_DSNOT_ERROR                      71/73  predicted 71/73  AS PREDICTED  red: dsloterror/HALT trapfrozen10dslot/HALT
M_DSFRZ_ERROR                      72/73  predicted 72/73  AS PREDICTED  red: trapfrozen10dslot/HALT
M_DS865                            66/73  predicted 66/73  AS PREDICTED  red: errdslotmisalign/STOP errdslotovf/STOP errdslotdiv0/STOP errdslotpriv/STOP errdslotunimpl/STOP trapfrozen7dslot/STOP trapfrozen10dslot/STOP
M_RRTDS                            71/73  predicted 71/73  AS PREDICTED  red: trapfrozen7dslot/STOP trapfrozen10dslot/BADREGS
M_RRNTDS                           68/73  predicted 68/73  AS PREDICTED  red: errdslotmisalign/STOP errdslotovf/STOP errdslotdiv0/STOP errdslotpriv/STOP errdslotunimpl/STOP
M_RRDS_MISALIGNED_ACCESS           73/73  predicted 73/73  AS PREDICTED  red: (none)
M_RRDS_UNIMPLEMENTED_OPCODE        73/73  predicted 73/73  AS PREDICTED  red: (none)
M_RRDS_PRIVILEGE_VIOLATION         73/73  predicted 73/73  AS PREDICTED  red: (none)
M_RRDS_ILLEGAL_INTEGER_DIVIDE      73/73  predicted 73/73  AS PREDICTED  red: (none)
M_RRDS_INTEGER_OVERFLOW            73/73  predicted 73/73  AS PREDICTED  red: (none)
M_FBDS                             72/73  predicted 72/73  AS PREDICTED  red: usfu1dslot/TAILHALT
TABLE 19: ALL AS PREDICTED
== TABLE 19b (instrument m88k_exc_probe_v20final.FROZEN.py)
BASE                               63/63  predicted 63/63  AS PREDICTED  red: (none)
M_DSFRZ_MISALIGNED_ACCESS          63/63  predicted 63/63  AS PREDICTED  red: (none)
M_DSFRZ_UNIMPLEMENTED_OPCODE       63/63  predicted 63/63  AS PREDICTED  red: (none)
M_DSFRZ_PRIVILEGE_VIOLATION        63/63  predicted 63/63  AS PREDICTED  red: (none)
M_DSFRZ_BOUNDS_CHECK_VIOLATION     63/63  predicted 63/63  AS PREDICTED  red: (none)
M_DSFRZ_ILLEGAL_INTEGER_DIVIDE     63/63  predicted 63/63  AS PREDICTED  red: (none)
M_DSFRZ_INTEGER_OVERFLOW           63/63  predicted 63/63  AS PREDICTED  red: (none)
M_DSFRZ_ERROR                      63/63  predicted 63/63  AS PREDICTED  red: (none)
M_DS865                            63/63  predicted 63/63  AS PREDICTED  red: (none)
TABLE 19b: ALL AS PREDICTED
ANALYZE_T19_DONE ALL AS PREDICTED
```

The delay-slot grid, printed by `regress/artifacts/m88kexcdeliver/derive_cells.py` from the row definitions
(`CELLCENSUS.out`; a cell shows its first row alphabetically, +N more):

```
=== DELAY-SLOT GRID -- v23, the SHIPPED instrument  (73 rows) ===
label     (SFRZ 0, slot 0)       (0, slot 1)            (SFRZ 1, slot 0)       (1, slot 1)           
MISALIGN  misalign +2            dslotmisalign          errc +4                errdslotmisalign      
UNIMPL    unimpl +2              dslotunimpl            errunimpl +1           errdslotunimpl        
PRIV      priv +3                dslotpriv              errpriv +1             errdslotpriv          
BOUNDS    bounds +2              dslotbounds            trapfrozen +4          trapfrozen7dslot      
DIV0      div0 +34               dslot                  errdiv0 +1             errdslotdiv0          
OVF       indclr +6              dslotovf               errovf +1              errdslotovf           
ERROR     errortb +1             dsloterror             trapfrozen10           trapfrozen10dslot     
rowed 28 of 28 cells of {7 labels} x {SFRZ} x {delay_slot}

=== DELAY-SLOT GRID -- v22, history  (63 rows) ===
label     (SFRZ 0, slot 0)       (0, slot 1)            (SFRZ 1, slot 0)       (1, slot 1)           
MISALIGN  misalign +2            dslotmisalign          errc +4                OPEN                  
UNIMPL    unimpl +2              dslotunimpl            errunimpl +1           OPEN                  
PRIV      priv +3                dslotpriv              errpriv +1             OPEN                  
BOUNDS    bounds +2              OPEN                   trapfrozen +4          OPEN                  
DIV0      div0 +27               dslot                  errdiv0 +1             OPEN                  
OVF       indclr +6              dslotovf               errovf +1              OPEN                  
ERROR     errortb +1             OPEN                   trapfrozen10           OPEN                  
rowed 19 of 28 cells of {7 labels} x {SFRZ} x {delay_slot}

=== DELAY-SLOT GRID -- v21 (HEAD: v19's 59 rows), the instrument the close adjudication reviewed  (59 rows) ===
label     (SFRZ 0, slot 0)       (0, slot 1)            (SFRZ 1, slot 0)       (1, slot 1)           
MISALIGN  misalign +2            OPEN                   errc +4                OPEN                  
UNIMPL    unimpl +2              OPEN                   errunimpl +1           OPEN                  
PRIV      priv +3                OPEN                   errpriv +1             OPEN                  
BOUNDS    bounds +2              OPEN                   trapfrozen +4          OPEN                  
DIV0      div0 +27               dslot                  errdiv0 +1             OPEN                  
OVF       indclr +6              OPEN                   errovf +1              OPEN                  
ERROR     errortb +1             OPEN                   trapfrozen10           OPEN                  
rowed 15 of 28 cells of {7 labels} x {SFRZ} x {delay_slot}

=== the FALLBACK x {delay slot} -- v23 ===
  ROWED   usfu1dslot (SFU1 in a slot still HALTs, naming 0x072)
```

## 5. The repair -- v22 -> v23 (12 hunks: the probe, then gate 11)

v22 (repair 13: the four `dslot*` rows, the asserts, the records) was reviewed by pass 14 and is NOT re-inlined.  The
whole uncommitted change against HEAD, for file-reading seats:
`git -C C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC diff -- regress/m88k_exc_probe.py regress/gate_m88k_rounding.sh`.

```diff
diff --git a/C:/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/m88kv20/snap_v22/m88k_exc_probe.py b/C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/m88k_exc_probe.py
index 38471e6c..b8c67310 100644
--- a/C:/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/m88kv20/snap_v22/m88k_exc_probe.py
+++ b/C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/m88k_exc_probe.py
@@ -38,9 +38,18 @@ rather than executing zeros, `breakpoint add <8*vector>`, `continue`, then `reg`
   dslotmisalign/dslotunimpl/dslotpriv/dslotovf   v22 (repair 13, 2026-10-16): the same br.n +16 with the fault IN ITS
              DELAY SLOT at the four other arms a guest INSTRUCTION can raise -- ld r2,r3,0 (r3 odd), prom_call and
              ldcr r2,cr1 after stcr r3,cr1 (user mode), add 7fffffff+1.  `implemented = !cpu->delay_slot' at each of those
-             arms swept HEAD's v21 59/59 (artifacts/m88kexcdeliver/delayslot_20261016/, predicted by Fable 5.1); each row
+             arms swept HEAD's v21 59/59 (artifacts/m88kexcdeliver/delayslot_20261016/, predicted by Fable 5.1 -- who also
+             UNDER-ENUMERATED it: the SFRZ slice was left for pass 14, below); each row
              kills its own arm's form.  Scored like dslot (the else-arm, AS IMPLEMENTED): SNIP = fault+4,
              SFIP = fault+12 = the branch's delay_target                                       0x20/0x28/0x30/0x48
+  dslotbounds/dsloterror   v23 (repair 14, 2026-10-16): a TRAP instruction in a br.n +16 slot -- tb1 naming 7 / 10, the
+             only route into those two labels.  Pinned AS THIS EMULATOR BEHAVES (X(tb1) has no delay-slot guard); the
+             MC88100 manual does not define a trap in a slot                                                 0x38/0x50
+  errdslotmisalign/ovf/div0/priv/unimpl, trapfrozen7dslot/trapfrozen10dslot   v23: the frozen div0 handler re-faults
+             INSIDE a br.n +8 slot, one row per label -- the {SFRZ set} x {slot set} column of the grid.  A non-trap fault is
+             still re-routed to ERROR (0x50, refatal); a trap is still exempt (0x38 / 0x50, no refatal).  +8, never +16:
+             0x40 + 16 is the ERROR entry, so a lost delivery would land on the row's own breakpoint      0x50/0x38/0x50
+  usfu1dslot v23: SFU1 (114) raised in a delay slot still HALTs at the fallback, naming 0x072
   errortb    tb1  0,r3,10 (r3=1)      f003d80a  supervisor trap naming ERROR (10) directly -- the
              only route to switch 1's ERROR arm (the double-fault route enters at the re-route AFTER
              switch 1, so it cannot see that arm: M_ERRORDROP escaped the error row 9/9, table 1)  0x50
@@ -189,11 +198,17 @@ the frozen TRAP is trapfrozen); a wrong return address; the delay-slot else-arm'
 geometry); a delay-slot-conditioned `implemented' on any class a guest INSTRUCTION can raise from a delay slot ({class} x
 {delay slot} closure, v22: DIV0 dslot, MISALIGNED dslotmisalign, UNIMPLEMENTED dslotunimpl, PRIVILEGE dslotpriv, OVERFLOW
 dslotovf -- `implemented = !cpu->delay_slot' at the four latter arms swept v21 59/59, delayslot_20261016/, and the body's own
-`if (cpu->delay_slot)' is what makes delay_slot a floor axis; BOUNDS and ERROR x {delay slot} need a TRAP INSTRUCTION IN A
-DELAY SLOT, which the MC88100 manual does not settle -- mc88100.txt:9433-9440 covers the slot OF a trap-taken instruction, not a
-trap in one -- so they are DISCLOSED with their measured escapes, M_DSNOT_BOUNDS and M_DSNOT_ERROR, table 16, and so is
-every trap instruction in a slot at the other five arms; multi-axis joints of delay slot with SFRZ, is_trap or a PSR bit stay
-clause (e)); a trap re-routed to ERROR while frozen, per class ({SFRZ set, is_trap} x {every switch-1 label a trap can NAME -- 0..3 are deliverable too and are unrowed, disclosed as
+`if (cpu->delay_slot)' is what makes delay_slot a floor axis.  v23 then closed the whole CLASS, because passes 13 and 14
+each found cells of it open (repair 14, the class-closure rule), as Fable 5.1 enumerated it on pass 14: the delivery path
+TESTS PSR & SFRZ and cpu->delay_slot, so the floor is {7 labels} x {SFRZ} x {delay_slot}, 28 cells, all rowed -- the
+(SFRZ clear, slot) column by the five rows above plus dslotbounds and dsloterror (a tb1 naming 7 / 10 in a slot, pinned as
+this emulator behaves: the MC88100 manual does not define a trap in a slot, and manual silence decides what a row may
+CLAIM, not whether the cell is owed); the (SFRZ set, slot) column by errdslotmisalign, errdslotovf, errdslotdiv0,
+errdslotpriv, errdslotunimpl, trapfrozen7dslot and trapfrozen10dslot (line 865's write is what X(br_n) reads to keep the
+vector over the branch target); and the fallback, clause (e) but rowed on its measured escape, by usfu1dslot.  Table 19
+(artifacts/m88kexcdeliver/repair13_20261016/).  Still disclosed, clause (e): a frozen TRAP in a slot at the five instruction
+labels (`if (!is_trap || (vector == L && cpu->delay_slot))', measured as escapes in table 19), {delay slot} x {a PSR bit
+other than SFRZ}, three-or-more-axis joints, and vectors 0..3's own delay-slot code (upstream, m88kexchwtraps)); a trap re-routed to ERROR while frozen, per class ({SFRZ set, is_trap} x {every switch-1 label a trap can NAME -- 0..3 are deliverable too and are unrowed, disclosed as
 m88kexchwtraps; the word EVERY overclaimed until v16}: trapfrozen (7),
 trapfrozen4/5/6/8/9/10/128/450/496/511 -- the ten labels 4..10, 128, 0x1c2, MVMEPROM_VECTOR, enumerated from switch 1's `case' list, plus
 the far edge of the user range (511) --
@@ -277,6 +292,7 @@ DIVU_R6_R5_R4 = tri(0x68, 6, 5, 4)               # f4c56804 -- a LEGAL divide in
                                                  #   SFU1_PRECISE (114) before it looks at the divisor -> the fallback must still HALT
 ADD_R2_R3_R4 = tri(0x70, 2, 3, 4)                # f4437004
 LD_R2_R3_0 = 0x14000000 | (2 << 21) | (3 << 16)  # 14430000 (major opcode 5, ld)
+LD_R6_R5_0 = 0x14000000 | (6 << 21) | (5 << 16)  # 14c50000 -- the `error' row's handler load, named for errdslotmisalign (v23)
 TB1_0_R3_7 = 0xf003d807                          # tb1 0,r3,7   (computed vector 7, supervisor)
 TB1_0_R4_8 = 0xf004d808                          # tb1 0,r4,8
 TB1_0_R3_10 = 0xf003d80a
@@ -343,6 +359,36 @@ ROWS = [
     ("dslotunimpl", [STCR_R3_CR1, BR_N_PLUS16, PROM_CALL], {"r3": PSR_USER},      V_UNIMPL,   0x1000c, PSR_USER,  None),
     ("dslotpriv", [STCR_R3_CR1, BR_N_PLUS16, LDCR_R2_CR1], {"r3": PSR_USER},      V_PRIV,     0x1000c, PSR_USER,  None),
     ("dslotovf", [BR_N_PLUS16, ADD_R2_R3_R4],   {"r3": 0x7fffffff, "r4": 1},     V_OVF,      0x10008, PSR_RESET, None),
+    #  ---- v23, repair 14 (2026-10-16): THE DELAY-SLOT CLASS CLOSURE.  Passes 13 and 14 each found the axis open, so this
+    #  repair closes the whole space in one diff, as Fable 5.1 enumerated it on pass 14: the delivery path TESTS two state
+    #  values, PSR & SFRZ and cpu->delay_slot, so the grid is {7 labels} x {SFRZ} x {delay_slot} -- 28 cells, 19 rowed by
+    #  v22.  The nine below, plus the fallback row.
+    #  (a) the two TRAP-ONLY labels in a slot, unfrozen.  A tb1 in a .n slot: the MC88100 manual does not define it, X(tb1)
+    #  has no slot guard, so these pin THIS EMULATOR'S behaviour (the else-arm shadows, like every dslot* row).
+    ("dslotbounds", [BR_N_PLUS16, TB1_0_R3_7],  {"r3": 1},                       V_BOUNDS,   0x10008, PSR_RESET, None),
+    ("dsloterror", [BR_N_PLUS16, TB1_0_R3_10],  {"r3": 1},                       V_ERROR,    0x10008, PSR_RESET, None),
+    #  (b) the seven labels with SFRZ SET and the fault IN A SLOT: the div0 handler at 0x40 re-faults inside a br.n's slot.
+    #  *** br.n +8, NEVER +16, inside a handler: 0x40 + 16 = 0x50 is the ERROR entry, so a lost delivery (`:865' not
+    #  writing EXCEPTION_IN_DELAY_SLOT, after which X(br_n) jumps to delay_target) would land on the row's own breakpoint
+    #  and read DELIVER.  +8 targets the SELF word planted after the handler, so a lost delivery reads STOP (Fable 5.1). ***
+    #  Frozen shadows throughout, so none of these pins the else-arm or owes the m88kdslotshadow re-pin.
+    ("errdslotmisalign", [DIVU_R2_R3_R0],       {"r3": 0x10, "r5": DATA + 1},    V_ERROR,    0x10004, PSR_RESET,
+                 [BR_N_PLUS8, LD_R6_R5_0]),                   # ld r6,r5,0 (odd) in the slot -> MISALIGNED frozen -> ERROR
+    ("errdslotovf", [DIVU_R2_R3_R0],            {"r3": 0x7fffffff, "r4": 1},     V_ERROR,    0x10004, PSR_RESET,
+                 [BR_N_PLUS8, ADD_R2_R3_R4]),                 # add 7fffffff+1 in the slot -> OVERFLOW frozen -> ERROR
+    ("errdslotdiv0", [DIVU_R2_R3_R0],           {"r3": 0x10, "r5": PSR_FRZSUP},  V_ERROR,    0x10004, PSR_RESET,
+                 [STCR_R5_CR1, BR_N_PLUS8, DIVU_R2_R3_R0]),   # SFD1 cleared first (else SFU1), divu in the slot -> DIV0 frozen
+    ("errdslotpriv", [DIVU_R2_R3_R0],           {"r3": 0x10, "r5": PSR_FRZUSER}, V_ERROR,    0x10004, PSR_RESET,
+                 [STCR_R5_CR1, BR_N_PLUS8, LDCR_R2_CR1]),     # user mode, SFRZ kept, ldcr in the slot -> PRIVILEGE frozen
+    ("errdslotunimpl", [DIVU_R2_R3_R0],         {"r3": 0x10, "r5": PSR_FRZUSER}, V_ERROR,    0x10004, PSR_RESET,
+                 [STCR_R5_CR1, BR_N_PLUS8, PROM_CALL]),       # user mode, SFRZ kept, prom_call in the slot -> UNIMPL frozen
+    ("trapfrozen7dslot", [DIVU_R2_R3_R0],       {"r3": 0x11},                    V_BOUNDS,   0x10004, PSR_RESET,
+                 [BR_N_PLUS8, TB1_0_R3_7]),                   # a frozen TRAP in the slot is still exempt: 0x38, no refatal
+    ("trapfrozen10dslot", [DIVU_R2_R3_R0],      {"r3": 0x11},                    V_ERROR,    0x10004, PSR_RESET,
+                 [BR_N_PLUS8, TB1_0_R3_10]),                  # naming 10: exempt, 0x50, and NO refatal -- the channel
+    #  (c) the fallback, which is clause (e) by the carrier's tests-not-reads criterion (all four pass-14 seats), rowed
+    #  because its escape was measured (table 17: `&& !cpu->delay_slot' at the fallback swept v22 63/63).
+    ("usfu1dslot", [STCR_R5_CR1, BR_N_PLUS16, DIVU_R6_R5_R4], {"r5": PSR_USERSFD1, "r4": 0x10}, V_SFU1, 0x1000c, PSR_USERSFD1, None),
     ("errortb",  [TB1_0_R3_10],                 {"r3": 1},                       V_ERROR,    0x10004, PSR_RESET, None),
     ("misaligntb", [TB1_0_R3_4],                {"r3": 1},                       V_MISALIGN, 0x10004, PSR_RESET, None),
     ("unimpltb", [TB1_0_R3_5],                  {"r3": 1},                       V_UNIMPL,   0x10004, PSR_RESET, None),
@@ -486,7 +532,7 @@ VBR_OF = {"vbrtb": VBR_TEST}                     # rows that relocate the vector
 #  NEGATIVE CONTROLS: rows whose CORRECT result is the fallback HALT.  They pin the boundary the diff keeps on purpose --
 #  vectors 11..113/116..127 and SFU1 (114/115) still stop the machine -- and separate the shipped D1 form from the rejected
 #  D4 (tail-default-delivers) and from delivering SFU1 (row m88kexcsfu1).  A mutant that delivers them turns these rows RED.
-EXPECT_RESULT = {"resid50": "HALT", "resid127": "HALT", "resid11": "HALT", "resid50ind": "HALT", "resid50c": "HALT", "resid50ser": "HALT", "sfu1h": "HALT", "usfu1": "HALT"}
+EXPECT_RESULT = {"usfu1dslot": "HALT", "resid50": "HALT", "resid127": "HALT", "resid11": "HALT", "resid50ind": "HALT", "resid50c": "HALT", "resid50ser": "HALT", "sfu1h": "HALT", "usfu1": "HALT"}
 PSR_WANT = {"errc": 0x9000000b,   # v14: exception entry ORs MODE|SFRZ|IND|SFD1 and leaves C alone (mc88100 manual: "the shadow freeze,
                                   #      SFD1, and IND bits of the PSR are set"), so the C-set handler row keeps C -- table 11 BASE read
                                   #      45/46 bad=psr on this row before any mutant: a MIS-CUT ROW, not the fix (case 3)
@@ -499,7 +545,7 @@ PSR_WANT = {"errc": 0x9000000b,   # v14: exception entry ORs MODE|SFRZ|IND|SFD1
             "errser": 0xa000000b}                # v17: the non-trap re-route with SER set -- also the MISALIGNED x SER cell
 #  indclr wants the default PSR_EXC (0x8000000b): IND was CLEAR before the fault and must be SET by the exception path;
 #  EPSR keeps the pre-fault 0x80000000.  A write that drops `| M88K_PSR_IND' leaves 0x80000009 -> bad=psr.
-EXPECT_VECTOR = {"resid50": 0x032, "resid127": 0x07f, "resid11": 0x00b, "resid50ind": 0x032, "resid50c": 0x032, "resid50ser": 0x032, "sfu1h": 0x072, "usfu1": 0x072}
+EXPECT_VECTOR = {"usfu1dslot": 0x072, "resid50": 0x032, "resid127": 0x07f, "resid11": 0x00b, "resid50ind": 0x032, "resid50c": 0x032, "resid50ser": 0x032, "sfu1h": 0x072, "usfu1": 0x072}
 #  (the vector the fallback diagnostic must NAME for an expected-HALT row -- the comment that used to trail the dict above)
 #  refatal: the re-route prints `[ SFRZ already set in PSR => ERROR ]' (fatal() is a plain print in this fork); a re-routed non-trap row
 #  must SEE it, a frozen-trap row must NOT -- the channel that tells the exemption arm from the re-route arm when both land on 0x50
@@ -509,7 +555,9 @@ REFATAL_EXPECT = {"error": True, "errovf": True, "errdiv0": True, "errpriv": Tru
                   "trapfrozen": False, "trapfrozen4": False, "trapfrozen5": False, "trapfrozen6": False, "trapfrozen8": False,
                   "trapfrozen9": False, "trapfrozen10": False, "trapfrozen128": False, "trapfrozen450": False, "trapfrozen496": False, "trapfrozen511": False,
                   "trapfrozenind": False, "trapfrozenc": False, "trapfrozenser": False,
-                  "trapfrozenuser": False, "trapfrozensfd1": False}   # v19: the exemption must hold with MODE and
+                  "trapfrozenuser": False, "trapfrozensfd1": False,
+                  "errdslotmisalign": True, "errdslotovf": True, "errdslotdiv0": True, "errdslotpriv": True,
+                  "errdslotunimpl": True, "trapfrozen7dslot": False, "trapfrozen10dslot": False}   # v23   # v19: the exemption must hold with MODE and
                   #      SFD1 clear too -- and this is the CHANNEL that makes the two rows non-vacuous, because the
                   #      mutant re-routes the trap and the diagnostic then APPEARS where these expect none
 #  (v12 COPIED this dict's trailing comment up to EXPECT_VECTOR, where it belongs, and claimed to have REMOVED it here.
@@ -653,7 +701,9 @@ def run_row(name, prog, regs, vector, fault_pc, epsr_exp, handler, grace=6.0, ha
         if name in ("error", "trapfrozen", "errovf", "errdiv0", "errpriv", "errunimpl", "errind", "errc", "errser",
                     "trapfrozen4", "trapfrozen5", "trapfrozen6", "trapfrozen8", "trapfrozen9", "trapfrozen10", "trapfrozen128",
                     "trapfrozen450", "trapfrozen496", "trapfrozen511",
-                    "trapfrozenind", "trapfrozenc", "trapfrozenser", "trapfrozenuser", "trapfrozensfd1"):
+                    "trapfrozenind", "trapfrozenc", "trapfrozenser", "trapfrozenuser", "trapfrozensfd1",
+                    "errdslotmisalign", "errdslotovf", "errdslotdiv0", "errdslotpriv", "errdslotunimpl",
+                    "trapfrozen7dslot", "trapfrozen10dslot"):
             # the second fault runs with SFRZ set: the shadows stay FROZEN at the first fault's values.  For
             # `trapfrozen' the second fault is a TRAP, which the manual (:8633-8636, 6.10 :10613-10614) exempts from
             # the ERROR re-route: it must deliver to ITS OWN vector (0x38), shadows still frozen.  M_SFRZTRAP sends it to 0x50.
@@ -662,6 +712,8 @@ def run_row(name, prog, regs, vector, fault_pc, epsr_exp, handler, grace=6.0, ha
             # the else-arm of the delay-slot branch: SNIP = (pc + 4) | V, SFIP = delay_target | V.  br.n +16 puts
             # delay_target at 0x10014 while slot_pc+4 is 0x1000c, so the two channels are DIFFERENT numbers (with
             # br.n +8 they were both 0x1000e and M_SFIPNOTGT / M_DSLOTSWAP escaped 10/10 -- Opus, pass 2).
+            # *** RE-PIN THIS BRANCH FIRST when m88kdslotshadow lands: it serves all seven dslot* rows, and the manual
+            # says the else-arm returns WRONG (the oracle-correction order: re-pin, measure HEAD red, then fix). ***
             # v22: every dslot* row puts the br.n +16 IMMEDIATELY before its faulting word, so delay_target is
             # (fault_pc - 4) + 16 -- for dslot itself that is 0x10014, the CODE + 4 + 16 this line used to spell.
             want.update(snip=((fault_pc + 4) | XIP_V), sfip=((fault_pc - 4 + 16) | XIP_V))
@@ -692,6 +744,8 @@ def main():
         name, prog, regs, vector, fault_pc, epsr_exp, handler = row[:7]
         handler_at = row[7] if len(row) > 7 else V_DIV0
         res = run_row(name, prog, regs, vector, fault_pc, epsr_exp, handler, handler_at=handler_at)
+        #  NAME COLUMN: `%-9s' pads to nine and `dslotpriv' is exactly nine, so the ONE literal space after it is all the
+        #  gate's ` +RESULT' has to match on that row.  Never drop that space (the padded-column class; Fable 5.1, pass 14).
         print("M88KEXC_ROW=%-9s RESULT=%-8s pc=%s sxip=%s snip=%s sfip=%s psr=%s epsr=%s r2=%s%s" % (
             name, res.get("result"), fmt(res.get("pc")), fmt(res.get("sxip")), fmt(res.get("snip")),
             fmt(res.get("sfip")), fmt(res.get("psr")), fmt(res.get("epsr")), fmt(res.get("r2")),
diff --git a/C:/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/m88kv20/snap_v22/gate_m88k_rounding.sh b/C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/gate_m88k_rounding.sh
index 4098ef1a..063cb14d 100644
--- a/C:/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/m88kv20/snap_v22/gate_m88k_rounding.sh
+++ b/C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/gate_m88k_rounding.sh
@@ -326,12 +326,12 @@ fi
 #  grew: every trap-like class stopped the machine.  With the final instrument the 7 are resid50, resid127,
 #  resid11, resid50ind, resid50c and usfu1, whose CORRECT answer is HALT, and the pre-existing user vector 128 (usertb); sfu1h reads STOP
 #  on HEAD because the FIRST divu halts on vector 0x008, not its own 0x072 -- probe10_head.out /
-#  probe_v3_head.out .. probe_v11_head.out) and the DETECTOR (63 fault rows -- 59 until v22, 2026-10-16 -- + 2
+#  probe_v3_head.out .. probe_v11_head.out) and the DETECTOR (73 fault rows -- 59 until v22, 63 in v22, 2026-10-16 -- + 2
 #  controls; kill tables killtable/, killtable2/, killtable3/, killtable4/ + killtable4b/
 #  (M_TAILRETURN), killtable5/ (the {class} x {MODE} and {SFRZ set, non-trap} x {class} closures), killtable6/ (the fallback far bound, resid127), killtable7/ (the frozen-TRAP rows per class), killtable8/ (the fallback in user mode, usfu1), killtable10/ (the frozen ERROR trap, the near bound, the fallback PSR-bit cells, the frozen user trap, the refatal channel; table 9 was folded into it), killtable11/ (the frozen traps naming the 0x1c2, MVMEPROM and 511 labels; the ERROR-arm-frozen and MISALIGNED-C representatives; the re-route x {IND, C} cells, errind/errc), killtable12/ (the re-route TRAP side x {IND, C}: both swept 46/46 before the rows existed), killtable13/ (the six previously-sweeping mutants, all killed), killtable14/ (grok's three predicted SER sweeps -- each 54/54 on the frozen v16 instrument and killed on v17 by its own row)
 #  under regress/artifacts/m88kexcdeliver/).  Only the detector half runs here.
 #
-#  The pins are NAMED so that deleting a row is visible: `M88KEXC_RESULT=63/63' pins the
+#  The pins are NAMED so that deleting a row is visible: `M88KEXC_RESULT=73/73' pins the
 #  denominator (a row that stops running shrinks it); resid50 and sfu1h are the two rows
 #  whose CORRECT answer is HALT -- they separate the shipped fix from a form that delivers
 #  every vector (the rejected D4) or SFU1 (row m88kexcsfu1); vbrtb is the one ANCHORED row
@@ -350,14 +350,18 @@ if ! grep -q "M88KEXC_DONE" "$EXCLOG"; then
 else
     check "m88k exc: CR parse self-test (PSR at reset == 0x80000002)" \
           "$(grep -c 'M88KEXC_SELFTEST=OK' "$EXCLOG")" "1"
-    check "m88k exc: 63 fault rows, all as expected (the denominator is the pin)" \
-          "$(grep -c 'M88KEXC_RESULT=63/63' "$EXCLOG")" "1"
+    check "m88k exc: 73 fault rows, all as expected (the denominator is the pin)" \
+          "$(grep -c 'M88KEXC_RESULT=73/73' "$EXCLOG")" "1"
     #  v22, repair 13 (2026-10-16): {class} x {delay slot}.  Before it only DIV0 faulted in a delay slot, and the
     #  form implemented = !cpu->delay_slot at MISALIGNED/UNIMPL/PRIV/OVF swept the 59-row probe clean at all four arms
     #  (artifacts/m88kexcdeliver/delayslot_20261016/).  BOUNDS and ERROR in a slot need a trap instruction there,
     #  which the manual does not settle -- disclosed in the probe's contract (repair13_20261016/, table 16).
-    check "m88k exc: a fault IN A DELAY SLOT is delivered at every class an instruction raises there (dslot 0x40, dslotmisalign 0x20, dslotunimpl 0x28, dslotpriv 0x30, dslotovf 0x48)" \
-          "$(grep -cE '^M88KEXC_ROW=(dslot +RESULT=DELIVER +pc=0x00000040|dslotmisalign +RESULT=DELIVER +pc=0x00000020|dslotunimpl +RESULT=DELIVER +pc=0x00000028|dslotpriv +RESULT=DELIVER +pc=0x00000030|dslotovf +RESULT=DELIVER +pc=0x00000048) ' "$EXCLOG")" "5"
+    #  v23, repair 14: the delay-slot GRID, {7 labels} x {SFRZ} x {delay_slot} (table 19).  Unfrozen, all seven labels:
+    check "m88k exc: a fault IN A DELAY SLOT is delivered at all seven labels (dslot 0x40, dslotmisalign 0x20, dslotunimpl 0x28, dslotpriv 0x30, dslotovf 0x48, dslotbounds 0x38, dsloterror 0x50)" \
+          "$(grep -cE '^M88KEXC_ROW=(dslot +RESULT=DELIVER +pc=0x00000040|dslotmisalign +RESULT=DELIVER +pc=0x00000020|dslotunimpl +RESULT=DELIVER +pc=0x00000028|dslotpriv +RESULT=DELIVER +pc=0x00000030|dslotovf +RESULT=DELIVER +pc=0x00000048|dslotbounds +RESULT=DELIVER +pc=0x00000038|dsloterror +RESULT=DELIVER +pc=0x00000050) ' "$EXCLOG")" "7"
+    #  ... and FROZEN, all seven labels, plus the fallback row:
+    check "m88k exc: with SFRZ set, a slot fault is still re-routed (errdslot* at 0x50) and a slot trap still exempt (trapfrozen7dslot 0x38, trapfrozen10dslot 0x50); SFU1 in a slot still halts (usfu1dslot)" \
+          "$(grep -cE '^M88KEXC_ROW=(errdslot(misalign|ovf|div0|priv|unimpl) +RESULT=DELIVER +pc=0x00000050|trapfrozen7dslot +RESULT=DELIVER +pc=0x00000038|trapfrozen10dslot +RESULT=DELIVER +pc=0x00000050|usfu1dslot +RESULT=HALT) ' "$EXCLOG")" "8"
     check "m88k exc: IND set by the exception path from a pre-fault PSR with IND clear (indclr)" \
           "$(grep -cE '^M88KEXC_ROW=indclr +RESULT=DELIVER .*psr=0x8000000b .*epsr=0x80000000' "$EXCLOG")" "1"
     check "m88k exc: user-mode MISALIGNED and OVERFLOW deliver (umisalign 0x20, uovf 0x48 -- the {class} x {MODE} closure)" \
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

## 7. Pass 14's findings, consolidated -- with the coordinator's disposition on each

G1 (Fable 5.1) the floor is {7 labels} x {SFRZ} x {delay_slot}, 28 cells; v22 rowed 19.  **ACCEPTED** -- v23 rows all 28 (the
   grid in section 4 is printed by `derive_cells.py`, not hand-written).  The two shapes Fable PREDICTED to sweep v22 are
   MEASURED there in table 19b.
G2 (Fable 5.1 + GPT-6 Astra) BOUNDS/ERROR x {slot} are FLOOR, overturning pass 13's F2.  Fable: reachability is derived from
   the WRITERS of each value, never from architectural legality; "a cell rowed under contradiction [`dslot`, whose else-arm
   the manual contradicts] cannot be refused under silence"; and the exempting mutant re-introduces this round's own host
   stop.  **ACCEPTED**: `dslotbounds`, `dsloterror`, pinned as this emulator behaves and saying so.  Grok 4.7 and GLM 5.3
   held them disclosed -- D4.
G3 (GPT-6 Astra) the SFRZ re-route's two sides x {slot} are floor.  **ACCEPTED, MEASURED** (table 17: both 63/63 on v22) --
   they are the (SFRZ set, slot) column of G1's grid, rowed per label.  Grok held them a disclosed joint -- D3.
G4 (all four) {fallback} x {slot} is clause (e) by the tests-not-reads criterion.  **ACCEPTED** -- and rowed anyway
   (`usfu1dslot`) because its escape was measured (table 17, 63/63): a measured delta licenses a detector row whether or not
   it is owed.
G5 (Fable 5.1) `br.n +16` in a handler at 0x40 targets 0x50, the ERROR entry -- a lost delivery reads DELIVER.  **ACCEPTED**:
   every v23 handler uses `br.n +8`; the table-18 candidate that used +16 is not shipped (`NAMING.txt`).
G6 (Fable 5.1) the trap route at the five instruction labels x (SFRZ set, slot) is clause (e) -- a second sub-cell of a cell the
   fault row already holds.  **ACCEPTED**, disclosed by count with the mutant `if (!is_trap || (vector == L &&
   cpu->delay_slot))`, MEASURED as an escape at each of the five in table 19.
G7 (all four, Q4) the pass-13 F5 sentence is right: only SFRZ is TESTED, so {site} x {MODE, SFD1, IND, C, SER} is clause (e) at
   every site and the L2 grades on v16/v17/v19 were given under a reads-PSR criterion.  Fable added: that criterion came from
   clause (d)(2), which "enumerates MUTANTS TO BUILD, not CELLS TO ROW"; GLM asked that the record NAME the criterion; Astra
   limited it to the five named bits.  **ACCEPTED with all three**: the criterion is "a state value the delivery path
   TESTS", which is exactly why `delay_slot` is floor and the five PSR bits are not.
G8 (all four, Q5) `m88ksfd1row`: the ledger line carries the warrant (table 16b's measured 62/63 plus the two asserts); NO
   addition-licence wording.  Grok and GLM had asked for wording on the close pass and withdrew it on pass 14 once 16b
   measured the row's delta.  **ACCEPTED** -- the owner question is withdrawn with them.
G9 (Grok 4.7) `OUTSTANDING_BUGS.md` still called the row pending at 58/58.  **ACCEPTED**: corrected in place.
G10 (GPT-6 Astra, Fable 5.1) appending table 16b's prediction to `PRETABLE.out` spent its mtime as table 16's order proof.
   **ACCEPTED**: `PRETABLE_ORDER.txt` records the file's NTFS birth time (17:59:43, before table 16's configure at 18:00:57)
   and the append (18:10:15, before 16b); every later table has its own PRETABLE file.
G11 (Fable 5.1) state the `m88kdslotshadow` re-pin once, in the shared scoring branch; comment the `%-9s` name column
   (`dslotpriv` is exactly nine wide); credit the under-enumeration in the docstring.  **ACCEPTED**, all three in v23.
G12 (Fable 5.1) the deriver encoded the overturned dispositions.  **ACCEPTED**: its delay-slot section is now the 28-cell grid.
G13 (Fable 5.1) the F8 correction was not yet in the ledger.  **ACCEPTED**: it lands in this commit's ledger write.
G14 (GLM 5.3) name the trap-exemption site and arms 0..3 in the disclosures.  **ACCEPTED**: the contract names both.
G15 (GPT-6 Astra) the pass-14 roster cannot report zero breaches while candidates survive; (Fable 5.1) pass 14's validity
   statement is "breaches found and enumerated".  **ACCEPTED** -- this pass is the one that may close.

## 8. Disagreements, both sides in their own words

D3 -- is (SFRZ set, slot set) floor, or a disclosed joint?
   * Grok 4.7: "`if (!is_trap && !cpu->delay_slot)` at line 816 is a predicted 63/63, and it is the disclosed joint: it adds
     `delay_slot` to the `is_trap` test."
   * GPT-6 Astra: "SFRZ and non-trap status identify the existing site; varying `delay_slot` adds one tested axis there."
   * Fable 5.1: "the floor is {label} x {SFRZ} x {delay_slot}, 28 cells, and the chain's own precedent agrees: killtable5
     closed {SFRZ set, non-trap} x {class} PER CLASS ... against label-level conjuncts of exactly the shape above."
   * GLM 5.3: "clause (e) there rests on an unstated premise: that EXCEPTION_IN_DELAY_SLOT vs NOT_DELAYED is unobservable to
     the probe" -- it IS observable: `X(br_n)` reads it (section 3), and table 19's M_DS865 is the measurement.
   * Coordinator: floor, by Fable's grid; and moot for closure either way, because the cells are rowed.  Grok, attack it.
D4 -- BOUNDS/ERROR x {slot}: floor (Fable, Astra) or disclosed (Grok, GLM)?
   * GLM 5.3: "if traps in slots are illegal, no legitimate guest reaches the cell; if legal, the cell exists but its correct
     oracle is unknown."
   * Fable 5.1: "The fork's ethos does not condition a guest-drivable host kill on the guest being well-behaved.  What
     legality governs is what the row may CLAIM."
   * Coordinator: floor; the rows claim emulator policy only, and say so.

## 9. Questions (VERDICT LINE FIRST)

Q1. Verify the grid in section 4 against the rows in section 5: for each of the 28 cells, does the credited row really raise
    that label with that SFRZ state and that slot state?  Name any mis-credited cell.
Q2. Is any of the ten new rows vacuous -- its channel unable to vary under the mutant it is credited with?  (Table 19 measures
    each; check that the right row is the one that reds.)
Q3. Inside the enumerated floor, is there any single edit to `m88k_exception()` that sweeps the 73-row probe?  Name it with
    its predicted score.  Do not propose cells outside the enumeration unless you can show the enumeration is incomplete.
Q4. Is the disclosed remainder complete and correctly classified: the frozen trap route at the five instruction labels in a
    slot (measured escapes), {delay slot} x {a PSR bit other than SFRZ}, three-or-more-axis joints, vectors 0..3's own
    delay-slot code (upstream, `m88kexchwtraps`)?
Q5. D3 and D4: is either ruling wrong?
Q6. Which of the coordinator's ACCEPTED dispositions G1-G15 is wrong?  (All fifteen are marked ACCEPTED.)
Q7. If nothing survives: CLOSE, with the denominator -- the delay-slot grid 28/28 (floor); the five PSR bits other than SFRZ at
    the seven labels 33/33 (35 less MODE at BOUNDS/ERROR, unreachable; the PSR grid's SFRZ column is NOT counted again, because
    the delay-slot grid's slot-0 half re-expresses it); fallback x six bits 6/6; non-trap re-route 5/5; trap exemption 5/5;
    fallback x {slot} 1/1 -- 78 enumerated cells, 28 of them floor, the other 50 clause (e) by G7 and G4, closed
    voluntarily.  Is it complete, and is the overlap removal right?

Seat notes: Fable 5.1 -- the grid is yours; check it harder than anyone, including the frozen rows' traces (`errdslotdiv0`
clears SFD1 with `stcr` first so its `divu` raises DIV0 rather than SFU1).  GPT-6 Astra -- G3 was yours; check the rows that
discharge it.  Grok 4.7 -- D3 is your call to defend or withdraw.  GLM 5.3 -- you cannot read files; say "not checkable from
the packet" where that is true.
