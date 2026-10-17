FABLE_M88KP14_20261016
# CHECKPOINT -- 2026-10-07 11:3x RUNNING (087a90 sections rewritten; the peer's sections below are untouched)
VERDICT: DO NOT CLOSE (repair 13 closed the delay-slot axis at ONE of the four sites this chain used for every other axis -- {label} x {SFRZ set} x {delay slot set} is unrowed at all seven labels, so `case <L>: implemented = !(cpu->delay_slot && (cr[PSR] & M88K_PSR_SFRZ));' at any instruction label, and `if (cpu->delay_slot && update_shadow_regs)' at :865, are PREDICTED 63/63 sweeps; the two MEASURED 63/63 sweeps at BOUNDS and ERROR (READ, table 16) are floor cells mis-filed as disclosed, because manual silence is not a floor criterion and `dslot' already pins a manual-CONTRADICTED cell; nine rows in ONE diff close {7 labels} x {SFRZ} x {delay slot} exhaustively.  F1 (mine) under-enumerated its own axis and F2 (mine) was wrong; m88ksfd1row KEEP stands)

Seat: Fable 5.1 (Agent, file-reading, read-only).  Pass 14 of `m88kexcdeliver' (#502), review of repair 13 (probe v20).

## 0. Evidence basis, and one disclosure

* Tree: HEAD 7b23b785 (committed 2026-10-16 17:13:55 -0500) plus the working tree, read 18:2x-18:4x while the main loop was
  still editing it -- `CHANGELOG.md' and `tools/pipeline/fable_queue.md' were unmodified at my first `git status' and
  modified at my second, so every working-tree line number below is as of 18:4x.
* Every score marked READ was read from a preserved log under `repair13_20261016/' or `delayslot_20261016/'; every score
  marked PREDICTED is reasoning from the committed source and the row table, and nothing was built or run.
* The other three pass-14 answers were not opened (both `grok_m88kp14.txt' and `codex_m88kp14.txt' were 0 bytes at my read
  time in any case).
* The only project file written is this one.  DISCLOSURE: one `git diff' output was spooled to `%TEMP%\ledger_diff.txt'
  (the Windows temp directory, outside every project tree and outside my scratchpad) in order to grep it, and deleted in the
  same minute; `ls' confirms it is gone.  That was outside the brief's "nothing else anywhere" and I record it rather than
  omit it.

## 1. The packet's facts, checked (all READ unless marked)

1. Table 16.  `run_table16.sh' (frozen 18:00:51) cmp's the clone's `cpu_m88k.c' against HEAD's before building and checks
   `[ gxemul -nt cpu_m88k.c ]' after every mutant build; `base.md5' 3593a8a5 / 20c69576.  BASE 63/63.  `implemented =
   !cpu->delay_slot' at MISALIGN / UNIMPL / PRIV / OVF / DIV0: 62/63 each, the true red set exactly its own row
   (dslotmisalign / dslotunimpl / dslotpriv / dslotovf / dslot, all HALT -- the eight expected-HALT rows the driver's naive
   filter also lists are accounted for in ANALYSIS.out).  The same at BOUNDS and at ERROR: 63/63, escapes.  Polarity twins
   55 / 58 / 57 / 54 of 63, the v19 red sets plus nothing.  Every log ends `M88KEXC_DONE'.
2. Table 16b.  Committed-form probe md5 4bc86466 (two asserts and comments over the table-16 copy ddffb55b); BASE 63/63;
   M_RRTRAPJOINT 62/63, red = trapfrozensfd1/STOP.  The PRETABLE addendum predicted "re-routed to ERROR 0x50 with the
   refatal diagnostic": the mechanism is as predicted; the row's breakpoint is at 0x38, so the re-routed trap sits at
   0x50's self-loop and the classifier reads STOP rather than BADREGS.  F7's measured warrant holds.
3. `delayslot_20261016/': BASE 59/59 md5 898eb0a7; the four `!cpu->delay_slot' logs are BYTE-IDENTICAL to BASE (I md5'd
   them: 898eb0a7 all four); twins 50 / 51 / 53 / 54 of 59.  The L2 grade stands.
4. `assert_controls.out': four negative controls fail with the named message, the unmodified import is clean.
5. The gate's new five-alternative regex: I ran it against `t16_BASE.out' with `grep -cE' and got 5.  No gate run on v20
   exists in the artifacts, so this grep is the only evidence that the check is satisfiable.  Note that `dslotpriv' is
   exactly nine characters, the width of the `%-9s' column: the regex's ` +' is satisfied only by the LITERAL space in the
   format string.  One character from the padded-column class; worth a comment beside the format.
6. X(br_n) (`cpu_m88k_instr.c:92-107'): sets delay_target, delay_slot = TO_BE_DELAYED (2), calls `ic[1].f', then
   `if (!(delay_slot & EXCEPTION_IN_DELAY_SLOT)) { delay_slot = NOT_DELAYED; pc = delay_target; quick_pc_to_pointers; }
   else delay_slot = NOT_DELAYED;'.  So the :865 write is CONSUMED by the branch: a slot fault whose EXCEPTION_IN_DELAY_SLOT
   (8) is not set has its delivery overridden by `pc = delay_target'.  That is the channel every (SFRZ set, slot set) row
   below reads, and it is guest-visible.
7. X(tb1) (`:2553-2563'): SYNCH_PC; user mode && vector < 128 -> PRIVILEGE_VIOLATION with is_trap 0 (premise 3 of
   section 2 verified); else `if (reg & bit) m88k_exception(vector, 1)'.  No delay-slot guard.  SYNCH_PC derives pc from
   `ic', which in a slot is ic+1, the slot's own address.  PSR_FRZSUP = 0x80000003, PSR_FRZUSER = 0x00000003, as stated.
8. `mc88100.txt' (775,987 bytes -- not an empty extraction): 3712-3728 and 9433-9440 read; every "delay slot" mention
   censused (3722-3726 fill advice, 9433 trace note 6, 10721-10725 scheduling advice, 11745-11764 and 12226 timing).  None
   speaks to a trap instruction IN a branch's slot.  The premise is right; what it LICENSES is Q3, and I rule the other way.

## 2. Q1 -- single-axis sweeps inside the floor

At the five instruction-reachable labels with SFRZ clear: none found, and I looked at the common tail.  Each
`implemented = !cpu->delay_slot' form is killed by its own row (READ) and its twin proves the edit lands (READ).  The
else-arm forms conditioned on one label (`SNIP := delay_target, SFIP := SNIP+4' for OVF alone; `SFIP := pc + 8'; XIP_E
set on a slot fault) are caught by that label's SNIP != SFIP pin (PREDICTED red at the label's dslot* row).  The tail:
`pc = VBR + 8*vector' or `m88k_pc_to_pointers' conditioned on delay_slot reads STOP at every dslot* row (PREDICTED); the
INSTRUCTION_ACCESS idiom copied into the seven-label arm (`if (delay_slot & EXCEPTION_IN_DELAY_SLOT) SNIP = SFIP = 0')
reds all five slot rows (PREDICTED); the DMT clears (:871-879) are written, never tested, and are 0 in every row because no
DATA_ACCESS row precedes -- an edit there is equivalent on this instrument, clause (e), not a cell.

The only single-axis sweeps are the two the repair MEASURED and filed as disclosed: `implemented = !cpu->delay_slot' at
BOUNDS (63/63 READ) and at ERROR (63/63 READ).  Whether those cells are inside the floor is Q3; I rule that they are.

Two-axis sweeps inside the floor as the RULE bounds it (Q2 says why they are floor):
* `case M88K_EXCEPTION_INTEGER_OVERFLOW: implemented = !(cpu->delay_slot && (cpu->cd.m88k.cr[M88K_CR_PSR] &
  M88K_PSR_SFRZ));' -- PREDICTED 63/63.  No row raises any class from a delay slot while SFRZ is set: every dslot* row is
  unfrozen and every err*/trapfrozen* second fault is outside a slot.  The same form at MISALIGN, UNIMPL, PRIV and DIV0:
  63/63 each, PREDICTED.  Canonical (d): the repair statement qualified by two fields the body reads.
* Site-level, `:865': `if (cpu->delay_slot && update_shadow_regs) cpu->delay_slot = EXCEPTION_IN_DELAY_SLOT; else
  cpu->delay_slot = NOT_DELAYED;' -- PREDICTED 63/63.  Under it a frozen handler's slot fault is re-routed to ERROR, pc is
  set to 0x50, and X(br_n) then overrides pc with delay_target: the ERROR delivery is LOST and the guest continues inside
  its handler with SFRZ set and the diagnostic already printed.

## 3. Q2 -- the other two sites: FLOOR at the re-route, clause (e) at the fallback

The floor (the flagship's pass-11 bound): the cross-product of the guard's dominating predicates -- the switch-1 labels --
with the STATE lvalues the fix's repair path reads that are jointly reachable.  The repair path reads PSR (tests SFRZ, :811)
and `cpu->delay_slot' (tests it at :840 and again at :865).  The body's own code distinguishes (SFRZ set, slot set) from
both of its neighbours: :834 skips the shadow update, :865 still writes EXCEPTION_IN_DELAY_SLOT, and X(br_n) consumes that
write.  Jointly reachable: a frozen handler is ordinary compiled code and compilers fill `.n' slots.  So the floor is
{label} x {SFRZ} x {delay_slot}, 28 cells, and the chain's own precedent agrees: killtable5 closed {SFRZ set, non-trap} x
{class} PER CLASS (errdiv0 / errpriv / errunimpl / error / errovf) against label-level conjuncts of exactly the shape
above.

F3 said "not in the floor as bounded here".  My bound was wrong.  I wrote "the same level at which the chain closed the PSR
bits" and then applied it to the arms alone -- but that level is {SITE} x {axis}, and the sites ARE the SFRZ x is_trap
cells (arms, fallback, non-trap re-route, trap exemption).  The repair crossed delay_slot with one of the four.  That is the
#499 shape: repaired at the address the mutant used, the symmetric cell left for the next pass.

The fallback (:799): predicate `vector < 128 && !implemented', body a halt that reads nothing.  By F5's own criterion (grade
by what the body TESTS) {fallback} x {delay slot} is clause (e).  The dependency, stated so it is not hidden: if D1 goes the
other way and the fallback's PSR-bit cells keep their recorded L2 grade, parity makes this cell floor too.  One unfrozen row
(`usfu1dslot', section 9) makes the dependency moot; I recommend it rides, not owed under F5.

The trap exemption (:816): is_trap is a per-raise-site argument, not a state lvalue, and the body tests it only inside the
SFRZ block.  At the two trap-only labels the trap route is the ONLY route to the (label, SFRZ set, slot set) cell, so those
two rows are the cell's rows and are floor.  At the five instruction labels the trap route is a second sub-cell of a cell
the fault row already holds: clause (e), disclosed by count with its mutant named (section 8).

## 4. Q3 -- BOUNDS / ERROR x {delay slot}: FLOOR, and the rows

The disclosure rests on "the manual does not settle whether a trap instruction may sit in a slot".  Three reasons that is
not a floor criterion:

(i) the carrier derives a cell's reachability from the WRITERS of each lvalue -- never from an invariant, and nowhere from
    architectural legality.  X(br_n) writes delay_slot = TO_BE_DELAYED before it calls the slot's handler; X(tb1) carries
    no slot guard.  The cell is reached by a two-word guest sequence the emulator executes.
(ii) the chain's own `dslot' row pins the else-arm, which the manual CONTRADICTS (m88kdslotshadow), AS IMPLEMENTED with a
    re-pin-first note.  Silence is a weaker ground than contradiction; a cell rowed under contradiction cannot be refused
    under silence.
(iii) the mutant that exempts the cell re-introduces this round's own defect -- every guest CPU stopped at the fallback --
    for a sequence the emulator accepts.  The fork's ethos does not condition a guest-drivable host kill on the guest being
    well-behaved.  What legality governs is what the row may CLAIM: it pins emulator policy (the ddi0406 precedent: policy
    "may not be described as architecture"), and its comment says so.

F2 was mine and it conflated "what the row may claim" with "whether the cell is owed".  The rows (names begin with `dslot'
so the shared scoring branch applies; the same +16 geometry as the five):

    ("dslotboundstb", [BR_N_PLUS16, TB1_0_R3_7],  {"r3": 1}, V_BOUNDS, 0x10008, PSR_RESET, None),
    ("dslotertb",     [BR_N_PLUS16, TB1_0_R3_10], {"r3": 1}, V_ERROR,  0x10008, PSR_RESET, None),

PREDICTED on HEAD (traced through X(br_n), X(tb1), :811-:868): RESULT=DELIVER pc=0x00000038 / 0x00000050,
sxip=0x0001000a snip=0x0001000e sfip=0x00010016 psr=0x8000000b epsr=0x80000002 r2=0xdeadbeef -- the shadow columns
byte-identical to `dslot'.  Under M_DSNOT_BOUNDS / M_DSNOT_ERROR: HALT (`unimplemented vector=0x007' / `0x00a' plus
`machines stopped') -> 64/65 each on a 65-row instrument.  If HEAD does NOT deliver one of them, that is a finding about the
decoder and the cell is reachable in a way this answer did not predict; either outcome is worth the two sessions.  Row
comment: "a trap instruction in a .n slot; the MC88100 manual (3.3.2, 6.7.2 note 6) does not define it; pinned AS
IMPLEMENTED (the else-arm shadows), re-pinned with every dslot* row when m88kdslotshadow lands".

## 5. Q4 -- D1: the F5 sentence is right, with one addition

Re-checked against the function, harder than before.  The only PSR mask the enclosing function performs is
`& M88K_PSR_SFRZ' at :811; :824 and :827 copy and OR the whole register; `m88k_stcr' is a callee, outside the DEPENDS-ON
bound.  By the 09-25 pin (TESTS = masks or compares as a case) and the 10-09 ruling (an input is graded by what the body
tests on it), {site} x {MODE, SFD1, IND, C, SER} is clause (e) at all four sites, and the L2 grades on v16/v17/v19 were given
under a reads-PSR criterion.  The three "moot" answers address row demand, which nobody disputes; the sentence is about the
precedent the recorded grades set.  The addition: the reads-PSR criterion came from clause (d)(2) ("swaps drawn ONLY from
fields the guarded BODY reads"), and (d)(2) enumerates MUTANTS TO BUILD, not CELLS TO ROW.  Say so in the sentence, or the
next de-fatalisation of a status-register path will read (d)(2) as a floor rule again.

## 6. Q5 -- D2: no licence wording; the ledger line carries the warrant

Unchanged from my close answer.  The two asserts are the structural answer; the ledger line cites F7's measured 62/63 and
Grok's shared-constant condition.  One consequence of section 10: at my read time the ledger's `m88ksfd1row' row carries
neither "57/58" nor "kept, not owed" (nor "58/58"), at HEAD or in the working tree -- so the protection the coordinator
describes ("cannot be copied bare") does not exist until the commit writes it.

## 7. Q6 -- which of the nine ACCEPTED dispositions is wrong

* F2 (disclosed): WRONG -- floor, section 4.  Mine.
* F1 (accepted, measured): the acceptance was right; what it accepted was under-enumerated BY ME -- the axis at one site of
  four.  The repair inherited that gap faithfully.
* F9 (deriver and census fixed): the new delay-slot census is single-site and prints DISCLOSED for BOUNDS/ERROR with the
  manual-silence reason -- it encodes the two dispositions this answer overturns.  It owes a {label} x {SFRZ} grid for
  delay_slot with the trap-only labels marked by route.
* F8 (L4, four records): READ in the probe (`:443'), `CHANGELOG.md:9307-9309' and `fable_queue.md:1507' in the working
  tree (HEAD still reads "at 58/58" at `CHANGELOG.md:9307').  NOT in the ledger at 18:4x: the `m88ksfd1row' row contains
  none of the strings "57/58", "58/58", "kept, not owed" at HEAD or in the tree, and `git diff -- ledger.json' carries no
  hunk for that row.  Not wrong; not yet true.  The commit message must not say four records unless the fourth is in it.
* F4: right.  One clause owed: the ROWS comment for the four says "scored like dslot (the else-arm, AS IMPLEMENTED)" and
  leans on dslot's `***' note for the re-pin-first obligation; write "re-pinned FIRST with dslot when m88kdslotshadow
  lands" once, in the shared scoring branch, where the re-pin will actually happen.
* F10: right about the chain; THIS pass's validity statement must read "breaches found and enumerated", not "zero with
  denominator".
* F11: verified at X(tb1) and the probe's constants.  F6 and F7: right; F7 measured (16b).

## 8. Q7 -- the denominator is not complete; the enumeration the closing pass must verify

The delay-slot axis of a TESTED lvalue crossed with the arms alone is "zero looked for" on the SFRZ slice.  The grid is
{7 labels} x {SFRZ} x {delay_slot}, 28 cells; cell = (SFRZ, delay_slot):

    label      (0,0)            (0,1)                (1,0)                            (1,1)
    MISALIGN   misalign         dslotmisalign        error / trapfrozen4              OWED  errdslotmisalign
    UNIMPL     unimpl           dslotunimpl          errunimpl / trapfrozen5          OWED  errdslotunimpl
    PRIV       priv             dslotpriv            errpriv / trapfrozen6            OWED  errdslotpriv
    BOUNDS     bounds (trap)    OWED dslotboundstb   trapfrozen (trap)                OWED  trapfrozen7dslot  (trap: only route)
    DIV0       div0             dslot                errdiv0 / trapfrozen8            OWED  errdslotdiv0
    OVF        ovf              dslotovf             errovf / trapfrozen9             OWED  errdslotovf
    ERROR      errortb (trap)   OWED dslotertb       error (re-route) / trapfrozen10  OWED  trapfrozen10dslot (trap: only route)

19 rowed, 9 owed; after the diff 28/28.  Disclosed, clause (e), each with its mutant:
* the trap route at (L in {4,5,6,8,9}, 1, 1): `if (!is_trap || (vector == L && cpu->delay_slot))' at :816, PREDICTED
  72/72 each.  Its label-free form `if (!is_trap || cpu->delay_slot)' IS caught: trapfrozen7dslot (STOP, re-routed to 0x50)
  and trapfrozen10dslot (refatal present -> BADREGS), PREDICTED 70/72;
* {fallback} x {delay slot} -- one optional row, section 9;
* {delay slot} x {any PSR bit}; three-or-more-axis joints; vectors 0..3 (m88kexchwtraps).
The trap/fault distinction at SFRZ clear is NOT a cell: the body tests is_trap only inside :811.

Denominator restated: PSR grid 40/40, fallback 6/6, non-trap re-route 5/5, trap exemption 5/5 (all clause (e) under F5,
closed voluntarily) + the delay-slot grid 14/14 label x SFRZ (5/14 today) = 70 cells.

## 9. The rows owed, in ONE diff (sketch rule observed: each traced through X(br_n), X(tb1) and m88k_exception; geometry
##    chosen so the lost-delivery channel is a planted self-loop, never a coincidence)

THE GEOMETRY TRAP, named so the copier does not fall into it: `br.n +16' must NOT be copied into a handler at 0x40.
0x40 + 16 = 0x50 is the ERROR entry, so under the :865 mutant the branch would land on the row's own breakpoint and read
DELIVER -- a clean-looking escape by coincidence of geometry.  Use BR_N_PLUS8 inside handlers: the branch target is then the
SELF word the probe plants at `8*handler_at + 4*len(handler)' (0x48 for a two-word handler, 0x4c for three), and a lost
delivery reads STOP.  Shadows are FROZEN in all seven, so none pins the else-arm and none inherits the m88kdslotshadow
re-pin -- a point in favour of closing this slice now.  Add the seven names to the frozen-scoring tuple and to
REFATAL_EXPECT (True for err*, False for trapfrozen*); none may begin with `dslot'.

    ("errdslotmisalign",  [DIVU_R2_R3_R0], {"r3": 0x10, "r5": DATA + 1},    V_ERROR,  0x10004, PSR_RESET,
                 [BR_N_PLUS8, 0x14000000 | (6 << 21) | (5 << 16)]),       # handler 0x40: br.n +8 (-> 0x48 SELF), ld r6,r5,0 odd IN THE SLOT
    ("errdslotovf",       [DIVU_R2_R3_R0], {"r3": 0x7fffffff, "r4": 1},     V_ERROR,  0x10004, PSR_RESET,
                 [BR_N_PLUS8, ADD_R2_R3_R4]),
    ("errdslotdiv0",      [DIVU_R2_R3_R0], {"r3": 0x10, "r5": PSR_FRZSUP},  V_ERROR,  0x10004, PSR_RESET,
                 [STCR_R5_CR1, BR_N_PLUS8, DIVU_R2_R3_R0]),              # br.n at 0x44 -> 0x4c SELF; divu at 0x48 in the slot
    ("errdslotpriv",      [DIVU_R2_R3_R0], {"r3": 0x10, "r5": PSR_FRZUSER}, V_ERROR,  0x10004, PSR_RESET,
                 [STCR_R5_CR1, BR_N_PLUS8, LDCR_R2_CR1]),
    ("errdslotunimpl",    [DIVU_R2_R3_R0], {"r3": 0x10, "r5": PSR_FRZUSER}, V_ERROR,  0x10004, PSR_RESET,
                 [STCR_R5_CR1, BR_N_PLUS8, PROM_CALL]),
    ("trapfrozen7dslot",  [DIVU_R2_R3_R0], {"r3": 0x11},                    V_BOUNDS, 0x10004, PSR_RESET,
                 [BR_N_PLUS8, TB1_0_R3_7]),
    ("trapfrozen10dslot", [DIVU_R2_R3_R0], {"r3": 0x11},                    V_ERROR,  0x10004, PSR_RESET,
                 [BR_N_PLUS8, TB1_0_R3_10]),

plus the two unfrozen trap rows of section 4.  Optional, recommended (the fallback cell, unfrozen, HALT expected,
EXPECT_VECTOR 0x072): ("usfu1dslot", [STCR_R5_CR1, BR_N_PLUS16, DIVU_R6_R5_R4], {"r5": PSR_USERSFD1, "r4": 0x10},
V_SFU1, 0x1000c, PSR_USERSFD1, None).

PREDICTED on HEAD, all seven frozen rows: DELIVER with the `error' / `trapfrozen' columns exactly -- pc 0x50 for the five
err* and trapfrozen10dslot, 0x38 for trapfrozen7dslot; sxip 0x10006 snip 0x1000a sfip 0x1000e psr 0x8000000b epsr
0x80000002.  Trace for errdslotpriv: divu at 0x10004 -> DIV0 unfrozen -> handler 0x40: stcr (MODE clear, SFRZ kept), br.n
at 0x44 (target 0x4c = planted SELF), ldcr at 0x48 IN THE SLOT -> PRIVILEGE with SFRZ set -> re-route to ERROR,
update_shadow_regs false, :865 writes EXCEPTION_IN_DELAY_SLOT, X(br_n) sees it and leaves pc at 0x50 -> breakpoint ->
DELIVER, refatal present.  The unfrozen stcr -> br.n -> ldcr sequence is already measured by dslotpriv (READ).

Table 17 (72 rows; 73 with the optional row), PREDICTED, PRETABLE17 in its OWN file before the build:
    BASE                                                   72/72
    M_DSNOT_BOUNDS / M_DSNOT_ERROR                         71/72 each   dslotboundstb / dslotertb HALT
    M_DSFRZ_<L>  (the label conjunct, seven builds)        71/72 each   errdslot<L> HALT at the five; trapfrozen7dslot / trapfrozen10dslot HALT at the two
    M_DS865      (`&& update_shadow_regs' at :865)         65/72        all seven frozen-slot rows STOP (pc = the planted SELF)
    M_RRDS       (`if (!is_trap || cpu->delay_slot)')      70/72        trapfrozen7dslot STOP, trapfrozen10dslot BADREGS(refatal)
    M_RRDS_<L>   (`|| (vector == L && cpu->delay_slot)'), L in {4,5,6,8,9}:  72/72 -- the disclosed remainder, measured so the disclosure states a measured escape
    M_FBDS       (`&& !cpu->delay_slot' at :799), if usfu1dslot rides:  72/73   usfu1dslot DELIVER at 0x390 instead of HALT
    the existing M_DSNOT at the five instruction labels and the four twins keep their red sets exactly.
The next pass VERIFIES THIS ENUMERATION (28 cells, 5 disclosed sub-cells by mutant) rather than hunting cells; the chain
closes on that pass if table 17 matches.

## 10. Records findings

1. The packet's "`repair13_20261016/PRETABLE.out' was written before table 16 ran (mtime order)" is no longer verifiable:
   PRETABLE.out is 18:10:15, `t16_BASE.out' 18:02:38, and eight of the eleven mutant logs predate 18:10.  The file's own 16b
   addendum says the mtime now orders 16b; the packet does not.  Not a reason to doubt the table -- the predictions match
   the measurements column for column -- but the ORDER proof the carrier asks for is spent, and an APPEND is what spent it.
   Practice: a later addendum goes in `PRETABLE16b.out', never appended; the order discriminator is the file's mtime and an
   append consumes it.
2. The gate check is unverified by a gate run (section 1.5): run gate 11 once on v20 before the commit, or record that the
   only verification is a grep.
3. F8's ledger half and F6's "kept, not owed" closure are not in the working-tree ledger at 18:4x (section 7).
4. `derive_cells.py' / `CELLCENSUS.out' (section 7, F9) encode the overturned dispositions.
5. The docstring entry for the four rows credits "predicted by Fable 5.1"; when the nine rows land, add "and
   under-enumerated by Fable 5.1 -- the SFRZ slice was left for pass 14", so the record carries the correction with the
   credit.

## 11. The shape question -- five rows pinned to an else-arm the manual calls wrong

The right shape for the round boundary.  A row pinning the manual's values would be RED on HEAD, and making it green is the
m88kdslotshadow code change -- a different round, under the oracle-correction order (re-pin first, measure HEAD red, then
fix).  What the five rows buy today is the SNIP != SFIP pin at every slot-reachable label, so a label-conditioned else-arm
edit cannot hide behind DIV0; what they cost is one shared re-pin in one scoring branch when that round lands -- and that
round gets a five-label HEAD-red witness for free.  The nine rows above pin FROZEN shadows and carry no such debt.

## 12. Not established here

No build, no run.  Every 63/63, 65/72, 70/72 and 72/72 above that is not in section 1 is PREDICTED from X(br_n), X(tb1),
m88k_exception and the row table.  The legality of a trap instruction in a `.n' slot on MC88100 silicon is unsettled from the
manual on disk and is not what this ruling turns on.  The ledger may phrase the F8 correction in words my grep did not use;
what I can say is that "57/58", "58/58" and "kept, not owed" are absent from the `m88ksfd1row' row in both HEAD and the
working tree.  The working tree was moving while I read it.
