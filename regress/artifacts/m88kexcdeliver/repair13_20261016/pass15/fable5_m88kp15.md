FABLE_M88KP15_20261016
# CHECKPOINT -- 2026-10-07 11:3x RUNNING (087a90 sections rewritten; the peer's sections below are untouched)
VERDICT: DO NOT CLOSE (the 28-cell state grid verifies 28/28 with no mis-credited cell, no vacuous row and no single-edit sweep INSIDE it -- but the enumeration is incomplete by the ONE INPUT the delivery path TESTS besides the two state values: `is_trap' at :816.  The carrier's generating-set clause owes that bit both ways at every floor cell, the chain already rows it both ways at every (label, SFRZ) cell with slot CLEAR (misaligntb..ovftb; trapfrozen4/5/6/8/9), and v23 rows it at the slot cells only where the trap is the ONLY route (7, 10).  So a TRAP in a slot at the five instruction labels is a floor obligation, not clause (e): frozen, the five M_RRDS_<L> 73/73 of table 19 (READ) are measured floor breaches mis-filed as disclosed -- L2, five rows; unfrozen, `case L: implemented = !(cpu->delay_slot && is_trap);' is a PREDICTED 73/73 sweep at each of the five arms -- five more rows.  Ten rows in ONE diff close {7 labels} x {SFRZ} x {delay_slot} x {is_trap}, 48 reachable obligations, after which m88k_exception() has no untested input left to enumerate -- that is the stop condition.  G6 was mine on pass 14 and it was wrong.)

Seat: Fable 5.1 (Agent, file-reading, read-only).  Pass 15 of `m88kexcdeliver' (#502), the verifying pass on repair 14
(probe v23).  Nothing built, nothing run; the only file written is this one.  Every score below is marked READ (a
preserved log under `repair13_20261016/') or PREDICTED (traced from the source and the row table).

## 0. Evidence basis, with three facts the packet does not state

1. **The frozen instrument and the committed probe are CODE-IDENTICAL; only records text moved after the freeze.**
   `cmp' says `m88k_exc_probe_v23.FROZEN.py' (md5 1d400b64, the md5 `probe_v23.md5' recorded for the working tree at
   18:51) and the working-tree `regress/m88k_exc_probe.py' (md5 e05ad051 now) differ; `diff' confines it to lines 41-52
   and 192-211, and the module docstring runs from line 2 to the closing `"""' at line 243 (`import' is line 244).  So
   table 19 measured the code the commit ships.  The commit message and the ledger should name BOTH md5s and say the
   delta is docstring-only, or a reader doing the two-md5 check will think table 19 measured something else.
2. **Gate 11 on v23 has FINISHED: PASS, 111 checks** (READ, `gate11_v23.out', 19:36; `M88KEXC_RESULT=73/73'; the two
   new checks `ok' at 7 and 8).  On a fresh HEAD build in the clone (`gate11v23_base.md5' = `base.md5', cpu_m88k.c
   3593a8a5 / gxemul 20c69576), two-part clearance in the runner.  The packet's "re-runs before the commit" is discharged.
3. **My pass-14 answer was WRONG about the v22 gate run.**  `gate11.out' is dated 18:23:47; my answer 18:47:38.  I wrote
   "no gate run on v20 exists in the artifacts" with the file twenty-four minutes old in the directory I was listing.
   A wrong record of mine; the packet's correction stands.

Also checked: `run_table19.sh' cmp's the clone's `cpu_m88k.c' against HEAD before the base build, drops `.MUTANT', requires
`MUT19_OK' + source-differs + `[ gxemul -nt cpu_m88k.c ]' per mutant, and restores with `cmp' before clearing the sentinel
(`driver19.out': all 23 `MUT19_OK', restore clean, `TABLE19_DONE 19:21:52').  Every t19 log ends `M88KEXC_DONE'.
`PRETABLE_19.out' (18:51) precedes `t19_BASE.out' (18:53); `PRETABLE_19b.out' (18:55) precedes `t19b_BASE.out' (19:23).

## 1. Q1 -- the 28 cells, each credited row checked against ROWS, the raise sites and a log.  NO MIS-CREDITED CELL.

How each state was verified, not assumed:
* LABEL: the only raise sites are `grep -n 'm88k_exception(' src/cpus/cpu_m88k_instr.c src/cpus/memory_m88k.c' --
  OVERFLOW from `add'/`add_imm'/`sub' (:585/:639/:697), DIV0 from the divides (:612/:624/:719/:731), PRIVILEGE from
  ldcr/stcr/fldcr/fstcr/rte and the user-mode trap filter (:816-:863, :2233/:2245, :2515/:2546/:2559), UNIMPLEMENTED
  from `prom_call' in user mode (:2450), MISALIGNED through `memory_m88k.c:417', and `ic->arg[2]' with is_trap 1 from
  tcnd/tb0/tb1 (:2529/:2551/:2564) -- the ONLY is_trap=1 sites, and the ONLY sites that can name 7 or 10.  There is no
  `tbnd' in this fork.  So "the trap route is the only route into BOUNDS and ERROR" is a sourced fact, and the frozen
  non-trap rows enter their OWN label (the re-route rewrites `vector' AFTER switch 1), which is what `derive_cells.py'
  records for them (e.g. `error' = DIV0 then MISALIGN, never ERROR).
* SLOT: unfrozen rows carry the else-arm shadows -- SFIP 0x10016 = delay_target|V against SNIP+4 = 0x10012 -- which only
  the `:840 if (cpu->delay_slot)' path produces (READ, t19_BASE: all seven dslot* rows).  Frozen rows skip the shadow
  update, so their slot evidence is M_DS865: each of the seven STOPs at the SELF planted after its handler (pc 0x48 for
  the two-word handlers, 0x4c for the three-word ones; READ, t19_M_DS865.out) -- X(br_n) only jumps there if it was
  mid-branch when m88k_exception ran, and on BASE the same rows DELIVER, so :865's write is what kept the vector.
* SFRZ: frozen rows show the first fault's shadows (SXIP 0x10006 = the divu at 0x10004) and the refatal diagnostic where
  expected; and each of the five frozen non-trap rows reds under exactly ITS label's M_DSFRZ_<L> and no other (READ,
  table 19 red lists) -- a mutant conditioned on `delay_slot && SFRZ' at label L halting the row proves label, slot and
  SFRZ in one observation.

Cell by cell (first row named; +N as the deriver prints it):
* (SFRZ 0, slot 0): misalign +2 (misaligntb, umisalign); unimpl +2; priv +3 (privtb = user tb1 naming 8 -> PRIVILEGE
  is_trap 0, privsuptb, privtbc); bounds +2 (vbrtb, boundstbc); div0 +34 (every two-fault row's first fault); indclr +6
  (ovf, ovfc, ovftb, uovf, ovftbser, trapfrozen8's first fault); errortb +1 (errortbc).  All at SFRZ clear, no slot.
* (0, slot 1): dslotmisalign / dslotunimpl / dslotpriv / dslotbounds / dslot / dslotovf / dsloterror -- each `br.n +16'
  immediately before the faulting word, PSR_RESET or PSR_USER (SFRZ clear), delivered at 0x20/0x28/0x30/0x38/0x40/0x48/0x50
  with SXIP 0x1000a|0x1000e, SNIP 0x1000e|0x10012, SFIP 0x10016|0x1001a (READ).  dslotbounds and dsloterror match my
  pass-14 prediction column for column.
* (1, slot 0): errc +4 (error, errind, errser, trapfrozen4); errunimpl +1 (trapfrozen5); errpriv +1 (trapfrozen6);
  trapfrozen +4 (trapfrozenind/c/ser/sfd1); errdiv0 +1 (trapfrozen8); errovf +1 (trapfrozen9); trapfrozen10.  Second
  faults, handlers at 0x40 (0x48 for trapfrozen8), SFRZ set by the first delivery.
* (1, slot 1): errdslotmisalign (ld r6,r5,0 with r5 = DATA+1 in a `br.n +8' slot), errdslotovf (add 7fffffff+1),
  errdslotdiv0 (stcr PSR_FRZSUP first so SFD1 is clear and the divu raises DIV0 -- the seat note's trace: without it
  the divu raises SFU1 at :609 before looking at the divisor), errdslotpriv (stcr PSR_FRZUSER, ldcr), errdslotunimpl
  (stcr PSR_FRZUSER, prom_call), trapfrozen7dslot and trapfrozen10dslot (tb1 naming 7 / 10, r3 = 0x11 so bit 0 is set).
  All SFRZ set (PSR 0x8000000b or the handler's FRZ* value, bit 0 set), all in the slot, all delivered where the grid
  says (READ).

One tooling note, not a defect: `derive_cells.py' does not parse ROWS; its FAULTS/INSLOT tables are hand transcriptions
of the probe.  I checked all 38 entries the delay-slot grid uses against ROWS and they agree.  A row added to the probe
and not to FAULTS prints OPEN (the safe direction); a row deleted from the probe and left in FAULTS prints ROWED (the
unsafe one).  Import ROWS, or assert the two name sets are equal, before the grid is cited as "derived from the rows".

## 2. Q2 -- none of the ten new rows is vacuous; the RIGHT row reds, through the PREDICTED channel (all READ)

I read the raw mutant logs rather than `analyze_t19.py''s summary (the analyzer is what I would otherwise be ratifying):
* M_DSNOT_BOUNDS / M_DSNOT_ERROR: dslotbounds / dsloterror HALT at pc 0x10014 -- the fallback halted, then X(br_n)
  jumped to delay_target because :865 never ran; plus trapfrozen7dslot / trapfrozen10dslot HALT at 0x48.  71/73 each.
* M_DSFRZ_<L>: exactly the frozen-slot row at L HALTs (errdslotdiv0 at pc 0x4c with psr 0x80000003 -- the handler's
  stcr value, i.e. the halt came AFTER the slot was entered).  72/73 each.  On v22 (table 19b) the same seven: 63/63 --
  my pass-14 prediction, measured.
* M_DS865: the seven frozen-slot rows STOP at their planted SELF (0x48 / 0x4c).  66/73.  On v22: 63/63 (table 19b).
* M_RRNTDS: the five errdslot* STOP at their OWN vectors 0x20/0x48/0x40/0x30/0x28 (not re-routed; the breakpoint is at
  0x50).  68/73.  Note errdslotdiv0's STOP is at 0x40, i.e. the handler re-ran and re-faulted until the grace expired --
  the classifier's `pc != entry' branch, correct.
* M_RRTDS: trapfrozen7dslot STOP at 0x50 (re-routed), trapfrozen10dslot BADREGS bad=refatal (same entry, wrong
  diagnostic) -- the refatal channel doing exactly what it was built for.  71/73.
* M_FBDS: usfu1dslot TAILHALT at pc 0x390 -- delivered to 114's entry, then switch 2's default stopped the cpu.  72/73.
  On BASE the row HALTs with pc 0x10018 = delay_target: the fallback returned without :865, X(br_n) jumped, the machine
  was already stopped.  So the fallback's halt is visibly slot-blind on HEAD, which is the measured warrant for rowing a
  clause-(e) cell.
* M_RRDS_<L>: 73/73 each -- real escapes, as the packet says.  Section 3 is about what they ARE.

The gate's two new regexes count 7 and 8 against `t19_BASE.out' (I ran `grep -cE' with the committed patterns) and the
v23 gate run confirms them live.  `dslotprivtb'/`dslotdiv0tb' style names (section 5) do not collide with the `dslot +'
and `dslotpriv +' alternatives, because the next character is a letter, not a space.

## 3. Q3 and Q4 -- the enumeration is INCOMPLETE, and the five "disclosed" M_RRDS_<L> escapes are floor breaches

**Inside the 28 state cells as enumerated: no single-edit sweep.**  Besides the 23 measured forms (every one killed
except the five M_RRDS_<L>, READ), I traced: `if ((PSR & SFRZ) && !cpu->delay_slot)' at :811 (errdslot* STOP at their
own vectors; the two frozen slot traps get a shadow UPDATE and read BADREGS) -- PREDICTED 66/73; `|| cpu->delay_slot' at
:811 (dslot* re-routed to 0x50 -> STOP; dsloterror's shadows not written -> BADREGS) -- PREDICTED 66/73; `:865 if
(cpu->delay_slot && !update_shadow_regs)' (the seven unfrozen slot rows lose the vector to X(br_n), landing on zeros at
0x10014/0x10018) -- PREDICTED 66/73; `:834 if (update_shadow_regs && !cpu->delay_slot)' (dslot* BADREGS) -- 66/73;
`:863 if (!cpu->delay_slot) cpu->pc = ...' (dslot* STOP) -- 66/73; `:865 ... && vector != ERROR' (the five errdslot*
and trapfrozen10dslot STOP) -- 67/73; the stcr at :827 conditioned on delay_slot (psr column) -- red at every slot row;
switch 2's seven-label arm zeroing SNIP/SFIP under `delay_slot && SFRZ' (frozen rows' snip pinned 0x1000a) -- 66/73.
Equivalent (not cells): :840's inner tests conditioned on SFRZ (never reached frozen) and the DMT clears.

**What the enumeration omits.**  `m88k_exception()' TESTS exactly four inputs: `vector' (switch 1, :799, :841/:844/:859,
:882, switch 2), `PSR & SFRZ' (:811), `cpu->delay_slot' (:840, :865; :902 is under the INSTRUCTION_ACCESS arm) -- and
`is_trap' at :816.  Pass 14 (mine) crossed the labels with the two STATE values and ruled the trap route at the five
instruction labels "a second sub-cell of a cell the fault row already holds".  Three things refute that:

(i) THE CARRIER.  The 2026-09-04 fix-review amendment: *"At each floor cell, every idata bit the guarded body TESTS is
    written both clear and set.  The bare state floor above does not catch M_ICLR -- an idata-bit x state joint -- and
    would grade the pass-11 escape as debt while the CHANGELOG grades it L2."*  `is_trap' is this function's one input
    bit, tested as a case; `if (!is_trap || (vector == L && cpu->delay_slot))' is a state x input-bit joint at a label --
    the M_ICLR shape exactly.  Filing it under "three-or-more-axis joints" is the bare-state-floor grading the carrier
    rejected; the carrier's own floors are three- and four-axis products (TxICR, #499), and its clause-(e) categories
    are cells outside the body-tested partitions and joints of MULTIPLE input bits -- m88k_exception() has one.
(ii) THE CHAIN'S OWN ROWS.  At every (label, SFRZ) cell with slot CLEAR the chain already writes is_trap both ways:
    misaligntb / unimpltb / privsuptb / div0tb / ovftb at SFRZ clear, trapfrozen4/5/6/8/9 at SFRZ set (killtable7), and
    the pass-5/pass-7 `!is_trap || vector == <class>' mutants were REPAIRED IN-ROUND (the v19 comment at probe :480-483
    cites them as precedent for grading the inner `if' L2).  The v23 mutant is that same mutant with `&& cpu->delay_slot'
    appended.  My "sub-cell" argument would have excused trapfrozen4..9 too, and the chain did not accept it there.
(iii) THE TELL.  v23 rows the slot-trap cell exactly where the trap is the only route (7, 10) and skips it where it is
    optional -- the is_trap=1 member was rowed when forced and dropped when not, which is the enumeration being built
    from the rows that happened to exist rather than from the function's inputs.

So the complete floor is **{7 labels} x {SFRZ} x {delay_slot} x {is_trap}: 56 cells, 8 unreachable** (is_trap 0 at
BOUNDS and ERROR in every (SFRZ, slot) state -- no non-trap raise site names 7 or 10; derive it with the grep above),
**48 reachable, 38 rowed by v23, 10 open**:

    label      (0,1,trap)          (1,1,trap)
    MISALIGN   OPEN                OPEN   M_RRDS_MISALIGNED_ACCESS      73/73 READ
    UNIMPL     OPEN                OPEN   M_RRDS_UNIMPLEMENTED_OPCODE   73/73 READ
    PRIV       OPEN                OPEN   M_RRDS_PRIVILEGE_VIOLATION    73/73 READ
    DIV0       OPEN                OPEN   M_RRDS_ILLEGAL_INTEGER_DIVIDE 73/73 READ
    OVF        OPEN                OPEN   M_RRDS_INTEGER_OVERFLOW       73/73 READ
    BOUNDS     dslotbounds         trapfrozen7dslot
    ERROR      dsloterror          trapfrozen10dslot

**Single edits that sweep, named with scores:**
* `if (!is_trap || (vector == L && cpu->delay_slot))' at :816, L in {4,5,6,8,9}: **73/73 READ** (table 19).  Five
  measured floor breaches -> L2.
* `case L: implemented = !(cpu->delay_slot && is_trap);' at the fix's own line, L in {4,5,6,8,9}: **73/73 PREDICTED** --
  no row raises L from a slot with is_trap 1 in either SFRZ state (dslot<L> and errdslot<L> are non-trap; the *tb and
  trapfrozen<L> rows are outside a slot).  The same edit at BOUNDS / ERROR: **71/73 PREDICTED** (dslotbounds/dsloterror and
  trapfrozen7dslot/10dslot HALT) -- the polarity control that the form lands.  This is the canonical clause-(d) shape,
  `if (X)' -> `if (X && Y)' with Y drawn from two body-TESTED values, i.e. the #488 E1 form the carrier calls a floor
  breach outright.  It conditions nothing the body does not test -- which is exactly why G7's PSR-bit cells are clause
  (e) and this is not.
* `if (cpu->delay_slot && (!is_trap || vector == 7 || vector == 10))' at :865: **73/73 PREDICTED** -- the same ten cells
  from the other side.

A NARROWER reading exists and I state it so the coordinator can rule: "the body tests is_trap only on the SFRZ path, so
the generating set applies only at the fourteen SFRZ-set cells" -> five owed (the frozen ones, all MEASURED), the
unfrozen five disclosed with the predicted arm mutant.  I rule for the BROAD reading on (ii): the chain's *tb rows
already treat the trap route as owed at SFRZ-clear cells, and the arm-level mutant above is in-rule under clause (d)
whatever the generating-set reading.  **Either reading forbids CLOSE**, because the five frozen cells hold measured
breaches under both.

**The disclosed remainder, re-classified (Q4):**
* the frozen trap route at the five instruction labels in a slot -- **WRONGLY classified**: floor, above.
* {delay slot} x {MODE, SER, C, SFD1, IND} -- clause (e), correctly (G7: copied or ORed, never tested).
* "three-or-more-axis joints" -- not a carrier category; here it names the is_trap cells and nothing else.  Replace with
  the carrier's terms.  Multi-axis INPUT joints are EMPTY for this function (one input bit).
* vectors 0..3's own delay-slot code -- correctly outside the fix's seven labels; `m88kexchwtraps'.
* NOT NAMED and should be, each clause (e) with its mutant so the disclosure is checkable:
  {user-trap labels 128 / 0x1c2 / MVMEPROM / 511} x {frozen slot}: `if (!is_trap || (vector >= 128 && cpu->delay_slot))'
  -- PREDICTED 73/73; outside the fix's labels (trapfrozen128/450/496/511 were voluntary closures of the exemption's
  label range), so disclose rather than row.  {fallback} x {SFRZ} x {slot}: `&& !(cpu->delay_slot && (PSR & SFRZ))' at
  :799 -- PREDICTED 73/73 (sfu1h is frozen outside a slot, usfu1dslot unfrozen inside one); clause (e) by G4's own
  criterion; an optional `sfu1hdslot' (sfu1h's handler as `[BR_N_PLUS8, DIVU_R6_R5_R4]', expected HALT naming 0x072)
  would row it for one session.

## 4. Q5 -- D3 and D4

* D3: FLOOR is right, and the reasoning does not stop where the coordinator stopped it.  GLM's point -- the :865 write
  is observable because X(br_n) reads it -- is measured (M_DS865 66/73 READ).  "Moot either way because the cells are
  rowed" is true of the non-trap side and FALSE of the trap side per label, which is the gap of section 3.  Grok's
  "disclosed joint" is the wording under which the five M_RRDS_<L> escapes were filed; it is wrong for the same reason it
  was wrong for M_RRNTDS.
* D4: FLOOR is right, and its principle -- reachability is derived from the writers of each value, never from legality;
  legality governs what the row may CLAIM -- is exactly what makes the ten slot-trap cells reachable: X(br_n) writes
  delay_slot before calling the slot's handler and X(tb1) has no slot guard (dslotbounds DELIVERED on HEAD, READ).

## 5. The repair that terminates the chain -- ten rows, ONE diff (sketch rule observed: each traced through X(br_n),
##    X(tb1) and m88k_exception; frozen geometry `br.n +8' so a lost delivery lands on a planted SELF, never on the row's
##    own breakpoint)

Frozen (add to the frozen-scoring tuple at probe :701-706 and to REFATAL_EXPECT as False; names must NOT begin `dslot'):

    ("trapfrozen4dslot", [DIVU_R2_R3_R0], {"r3": 0x11}, V_MISALIGN, 0x10004, PSR_RESET, [BR_N_PLUS8, TB1_0_R3_4]),
    ("trapfrozen5dslot", [DIVU_R2_R3_R0], {"r3": 0x11}, V_UNIMPL,   0x10004, PSR_RESET, [BR_N_PLUS8, TB1_0_R3_5]),
    ("trapfrozen6dslot", [DIVU_R2_R3_R0], {"r3": 0x11}, V_PRIV,     0x10004, PSR_RESET, [BR_N_PLUS8, TB1_0_R3_6]),
    ("trapfrozen8dslot", [ADD_R2_R3_R4], {"r3": 0x7fffffff, "r4": 1}, V_DIV0, 0x10004, PSR_RESET,
                 [BR_N_PLUS8, TB1_0_R3_8], V_OVF),   # first fault OVF, handler at 0x48 (trapfrozen8's shape): the
                 # breakpoint is 0x40, so the handler cannot live there.  br.n +8 from 0x48 targets 0x50 -- the ERROR
                 # entry's SELF -- which is safe HERE because this row's breakpoint is 0x40, not 0x50.  r3 keeps bit 0.
    ("trapfrozen9dslot", [DIVU_R2_R3_R0], {"r3": 0x11}, V_OVF,      0x10004, PSR_RESET, [BR_N_PLUS8, TB1_0_R3_9]),

PREDICTED on HEAD: DELIVER at 0x20 / 0x28 / 0x30 / 0x40 / 0x48, sxip 0x00010006 snip 0x0001000a sfip 0x0001000e psr
0x8000000b epsr 0x80000002 r2 0xdeadbeef, refatal absent -- the trapfrozen7dslot columns (READ) with the entry changed.
Trace for trapfrozen6dslot: divu at 0x10004 (PSR_RESET has SFD1 clear -> DIV0, not SFU1) -> 0x40 unfrozen, shadows
written; br.n +8 at 0x40 (delay_target 0x48 = planted SELF); tb1 0,r3,6 at 0x44 in the slot, supervisor so the user
filter at :2559 is skipped, r3 & 1 -> m88k_exception(6, 1): PRIV label implemented; SFRZ set, is_trap -> exempt,
update_shadow_regs false; pc = 0x30; :865 writes EXCEPTION_IN_DELAY_SLOT; X(br_n) leaves pc -> breakpoint -> DELIVER.

Unfrozen (names begin `dslot' so the shared else-arm branch scores them; they inherit the m88kdslotshadow re-pin like
the seven existing dslot* rows):

    ("dslotmisaligntb", [BR_N_PLUS16, TB1_0_R3_4], {"r3": 1}, V_MISALIGN, 0x10008, PSR_RESET, None),
    ("dslotunimpltb",   [BR_N_PLUS16, TB1_0_R3_5], {"r3": 1}, V_UNIMPL,   0x10008, PSR_RESET, None),
    ("dslotprivtb",     [BR_N_PLUS16, TB1_0_R3_6], {"r3": 1}, V_PRIV,     0x10008, PSR_RESET, None),
    ("dslotdiv0tb",     [BR_N_PLUS16, TB1_0_R3_8], {"r3": 1}, V_DIV0,     0x10008, PSR_RESET, None),
    ("dslotovftb",      [BR_N_PLUS16, TB1_0_R3_9], {"r3": 1}, V_OVF,      0x10008, PSR_RESET, None),

PREDICTED on HEAD: the dslotbounds columns (READ) with the entry changed -- sxip 0x0001000a snip 0x0001000e sfip
0x00010016 psr 0x8000000b epsr 0x80000002.  Under a lost delivery they land on the zeros at 0x10014, as dslotbounds
measurably does under M_DSNOT_BOUNDS (pc 0x10014, READ).

Gate: pin `M88KEXC_RESULT=83/83'; the unfrozen check gains the five names (count 12), the frozen check gains the five
trapfrozen<L>dslot names (count 13).  The existing `trapfrozen(4|5|...)? +RESULT' check at :380 stays at 16: the new
names are followed by a letter, so its alternatives do not match them (the same reason it ignored trapfrozen7dslot).

Table 20 (PRETABLE_20.out FIRST, its own file; 83 rows; the whole set re-run on ONE instrument so every score cites it):
    BASE                                   83/83
    M_RRDS_<L>, five                       82/83   trapfrozen<L>dslot STOP at 0x50 (refatal present)
    M_ARMTS_<L>  `!(delay_slot && is_trap)' at arm L, seven    81/83   dslot<L>tb HALT, trapfrozen<L>dslot HALT
    M_ARMTSU_<L> `... && !(PSR & SFRZ)', five                  82/83   dslot<L>tb HALT -- the unfrozen cell's own discriminator
    M_DSNOT_<L> at the five              79/83   dslot<L> errdslot<L> dslot<L>tb trapfrozen<L>dslot
    M_DSNOT_BOUNDS / ERROR               81/83   unchanged red sets
    M_DSFRZ_<L> at the five              81/83   errdslot<L> trapfrozen<L>dslot;  BOUNDS / ERROR 82/83
    M_DS865                              71/83   the twelve frozen-slot rows STOP
    M_RRTDS                              76/83   seven frozen slot traps (six STOP, trapfrozen10dslot BADREGS)
    M_RRNTDS                             78/83   the five errdslot*
    M_FBDS                               82/83   usfu1dslot TAILHALT
`mut19.py''s ARM mechanism takes the two new expressions unchanged (it rewrites the `implemented = true;' line under the
first `case' of the label).  Thirty-three builds, about 45 minutes at table 19's pace.

**Why this is terminal and not pass 16's #392:** the four tested inputs above are the function's complete tested set --
nothing else in :689-:981 is masked or compared as a case.  Pass 16 verifies that a 48-cell `derive_cells.py' grid (add
an ISTRAP column beside INSLOT) prints 48/48 with the eight unreachable cells NAMED with their reason, and that table 20
matches PRETABLE_20; there is no further input to enumerate, so a zero on that pass carries its denominator by
construction.

## 6. Q6 -- which ACCEPTED dispositions are wrong

* **G6 -- WRONG.  Mine.**  Floor, not clause (e); five measured breaches (L2) and five predicted.
* **G1 -- incomplete, mine.**  28/28 is true of the STATE grid and the state grid is not the whole floor.
* **G3 -- discharged only at the site level.**  Astra's pass-14 claim (I read `codex_m88kp14.txt') was the label-free
  `if (!is_trap || cpu->delay_slot)', killed by M_RRTDS 71/73 (READ).  The coordinator's "rowed per label" is true of the
  non-trap side and false of the trap side at five labels.
* **G12 -- incomplete.**  The deriver's grid needs the is_trap axis (28 -> 48).
* **G15 -- not this pass.**  Breaches found and enumerated; the validity statement is that, not "zero with denominator".
* **G13 -- not yet true, and more so than pass 14 found.**  The ledger's `m88kexcdeliver' row carries 87 entries, ALL
  dated 2026-09-05/06 -- nothing for the close adjudication, passes 13-15 or either repair; `m88ksfd1row' is `open'
  with zero entries and the hold question still in place; the working-tree ledger diff (29/29 lines) mentions none of
  v22/v23/repair 14/pass 15.  The commit's ledger write owes passes 12-15 with their four seats and the five deliberately
  unfired seats by name, both repairs with `detector:'/`probe:' witnesses, the F8 correction, and m88ksfd1row's closure.
  Until it does, G9's "corrected in place" is true only of OUTSTANDING_BUGS.md (verified, :15675-15786) and
  CHANGELOG.md's four added lines (the 57/58 correction; no repair-13/14 block exists yet).
* Verified right: G2, G4, G5 (every v23 handler `br.n +8', rows :376-:388), G7, G8, G9 (as above), G10
  (`PRETABLE_ORDER.txt' records Birth 17:59:43 < configure 18:00:57, Modify 18:10:15 = the append < 16b), G11 (all
  three in the working tree: :715-716, :747-748, :41-42 -- the docstring credit is in the working tree only, not the
  frozen instrument, which is the records-only delta of section 0), G14.
* A prediction of mine the coordinator corrected in PRETABLE_19: M_DSNOT_<L> on v23 also reds the frozen-slot row at L.
  Obviously so; written down here as my error so it is not read as the table's.

## 7. Q7 -- the denominator

Arithmetic and overlap as the packet states them are right: 7 labels x 5 untested bits = 35, less MODE at BOUNDS and
ERROR (unreachable: tcnd/tb0/tb1 all raise PRIVILEGE for a user-mode vector below 128, :2515/:2546/:2559, and nothing
else names 7 or 10) = 33; fallback 6; non-trap re-route 5; trap exemption 5; fallback x slot 1; and the PSR grid's SFRZ
column is not counted again because the slot-0 half of the delay-slot grid re-expresses it -- with ONE unit caveat to
write down: the PSR grid's cells are "the bit VARIES at this label" cells (7 for SFRZ) and the delay-slot grid's are
value cells (14 at slot 0); removing 7 and adding 14 double-counts nothing, but they are different units.

It is INCOMPLETE on the is_trap axis -- "zero looked for", not "zero found".  Restated: the delay-slot grid is 28 floor
cells carrying 48 reachable (cell, is_trap) obligations, 38 discharged, 10 open; with the 50 clause-(e) cells closed
voluntarily, 98 enumerated.  After the ten rows: 48/48, and the floor has no further axis to add.

## 8. Records to correct when the ruling is adopted (L4, each quoting what it refutes)

1. Probe docstring :209-211 ("Still disclosed, clause (e): a frozen TRAP in a slot at the five instruction labels ...
   three-or-more-axis joints") and the ROWS comment at :389-390 by implication.
2. `PRETABLE_19.out' :14-15 -- a dated prediction file; correct in PRETABLE_20, not by editing it.
3. `derive_cells.py' / `CELLCENSUS.out' -- the grid and its "28 of 28".
4. My pass-14 answer, sections 3 and 8 ("a second sub-cell ... clause (e)"; "the trap/fault distinction at SFRZ clear
   is NOT a cell") and section 1.5 (the gate run that existed).  This file is the correction.
5. The commit message: name both probe md5s (1d400b64 measured, e05ad051 committed, docstring-only delta); do not say
   "four records" for F8 or "ledger" for anything until the ledger write exists.

## 9. Not established here

No build, no run.  Every 73/73 above that is not in a t19/t19b/gate log is PREDICTED from X(br_n), X(tb1), m88k_exception
and the row table, including the ten-row scores of section 5.  The broad-versus-narrow reading of the generating-set
clause is a rule question I have ruled on with my reasons; the owner or the flagship adjudication may rule the other way,
and under the narrow reading the obligation is five rows, all with MEASURED escapes -- so the verdict does not depend on
which reading wins.  The legality of a trap instruction in a `.n' slot on MC88100 silicon remains unsettled from the
manual on disk and remains irrelevant to whether the cells are owed.
