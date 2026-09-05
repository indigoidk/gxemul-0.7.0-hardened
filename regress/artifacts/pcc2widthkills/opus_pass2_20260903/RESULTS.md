# pcc2widthkills -- OPUS SEAT pass-2 kill table

BASELINE, named before mutant 1: commit **b78bb0f**, `src/devices/dev_pcc2.c`
md5 `4c0cfc6d8e6cb099ebe7e92420e6b71e`.  Verified three ways -- `cmp` clean against
`GXEMUL-SEC` at clone time, identical to `git show b78bb0f:src/devices/dev_pcc2.c`,
and identical to the frozen copy `/tmp/pcc2_baseline.c` used for every restore.

RIG: `cp -a` of `build/` -> `/tmp/gxopus_pcc2` (WSL Gentoo).  `build/` cleared BOTH
parts before cloning (shared file, `cmp`-clean vs SEC; binary newer than source).
No project tree was written.  Detector unchanged throughout: `pcc2_width_probe.py`
md5 `678fc01000887e3626e8888b82004441` at start and at end.

| # | edit | size | score | verdict |
|---|---|---|---|---|
| BASE | none | - | **60/60** | baseline reproduced |
| M1 | SCCTX arm announces on `PCC2_W_SCCRX_LEN` | **one token** | **60/60** | **CLEAN SWEEP -- floor (d)** |
| M2 | MASK arm `len != 1` -> `len > 2` | **two chars** | **60/60** | **CLEAN SWEEP -- floor (d)** |
| M3 | `len != 1` -> `len > 2`, all twelve | - | 49/60 | KILLED (11 red) |
| M4 | `writeflag == MEM_WRITE` -> `!= MEM_READ` | - | 60/60 | **EQUIVALENT**, not an escape |
| M5 | latch test OR-ed -> floods | - | 59/60 | KILLED (`latch same`) |
| M6 | MASK arm announces then falls through | - | **60/60** | **CLEAN SWEEP** |
| M7 | verbatim `exit(1)` kill at IPL (0x3e) | - | (retried) | |
| M8 | guard deleted at SCCTX | - | (table 2) | |
| M9 | guard deleted at MASK | - | (table 2) | |
| M10 | latch made process-global | - | (table 2) | DISCLOSED blind spot |

M4 is a RESULT, not a hole: `src/include/memory.h` defines MEM_READ 0 / MEM_WRITE 1,
`memory_rw.c` documents the writeflag as exactly those two, and MEM_DOWNGRADE (128) is
used only in `cpu_dyntrans.c` for a different argument.  The two forms cannot differ.

THE HOLE, in one line: the probe reaches **twelve register LABELS across only TEN
BLOCKS** (T1CTL/T2CTL share one latch bit, T1ICR/T2ICR share another).  `PCC2_W_IPL_LEN`
and `PCC2_W_MASK_LEN` have **zero rows** -- gate 14 names all 60 and none touches
0x3e or 0x3f.  And `latch two` is the only session that writes two blocks, so it pins
ONE of the 66 possible bit collisions.

## CONFIRMED AS OF TABLE 2 / M8

M6 = 60/60 (MASK announces then falls through) -- THIRD clean sweep.
M8 = 60/60 (guard DELETED at SCCTX) -- FOURTH, and the worst: SCCTX (0x1e) is one of
the FIVE GUEST-REACHABLE arms the contract claims to cover.  Its only wide-write rows
are `hwr scctx' (exit status) and `hwr scctx lv' (liveness) -- survival-only.  Its arm
masks `& 0x1f', so a declined write and an accepted one store DIFFERENT values, and no
row reads the value back.

The round's own M_DELETE deleted ALL TWELVE guards and died on `rb genctl'.  Deleting
ONE dies nowhere.  The detector catches the global edit and not the local one -- the
"three cells of a two-by-two" shape the carrier names.

## THE ROOT CAUSE, in one sentence

The reachability census in the product comment MIXES UNITS: "the five EVEN-offset
BLOCKS (GENCTL, TxCTL, TxICR, SCCERR, SCCTX)" + "the seven odd ones" = twelve, which
READS as all twelve blocks but is five BLOCKS plus seven LABELS.  T1CTL/T1ICR are
labels of blocks already counted in the five, and PCCTWO_IPL (0x3e) and PCCTWO_MASK
(0x3f) appear in NEITHER list.  The probe was built from that census, which is exactly
why it has those twelve labels and no IPL/MASK rows.

## Q4 -- what would it take to know

The only consumer of `dev_pcc2.c` is MACHINE_MVME88K_187 (one `device_add`, in
`machine_mvme88k.c`).  `machine_luna88k.c` contains ZERO references to pcc2, and the
project's m88k boot rig is **luna88k** -- so **no mvme187 OS boot exists here at all**.

Consequence: the round's implicit warrant "no measured driver wide-writes these
registers" has NO measurement behind it in this project, because there is no execution
path on which such a write could have been observed.  That does not make DECLINE wrong
-- it makes it MORE clearly right, since COMPOSE would invent per-lane semantics that
nothing available here can validate.

The decline latch is, however, exactly the right instrument for the question: a real
mvme187 boot would print `-- declined.  (once) ]` the first time a driver wide-writes
any of the twelve.  So `pcc2widecompose` should record that its answer is one boot
away IF an image is ever obtained, and is otherwise a driver-SOURCE question
(OpenBSD `sys/arch/mvme88k/dev/pcctwo.c` and friends -- grep bus_space_write_2/_4
against the PCCTWO offsets).  No BSD driver source is on disk.

M9 = 60/60 (guard DELETED at MASK) -- FIFTH clean sweep.

## TABLE 2 + REPAIR VALIDATION (measured)

| # | edit | score |
|---|---|---|
| M8 | guard DELETED at SCCTX (GUEST-reachable) | **60/60 CLEAN SWEEP** |
| M9 | guard DELETED at MASK | **60/60 CLEAN SWEEP** |
| M10 | latch made process-global | 60/60 -- DISCLOSED by the contract, correctly |

PROPOSED REPAIR `latch all', validated in both directions:

    BASE  declines=12/12 ok    GENCTL,VECBASE,PSCALEADJ,TxCTL,TxICR,SCCERR,
                               SCCICR,SCCTX,SCCRX,SCSIICR,IPL,MASK
    M1    declines=11/12 FAIL  SILENT: SCCRX
    M9    declines=11/12 FAIL  SILENT: MASK

ONE row.  Green on the shipped fix, red on two clean-sweep mutants at two different
arms, and it NAMES the block that went silent.  It is also the only row that reaches
IPL and MASK at all -- note both appear in the BASE announce list.

## NON-EQUIVALENCE CONTROLS -- the two sweeps are REAL defects, not inert edits

A mutant that will not die has three explanations and one is "the mutant is mis-built".
Measured, on the same binaries:

    maskland  BASE  MASK after a wide write = 0x0     (declined -- shipped behaviour)
    maskland  M2    MASK after a wide write = 0xbb    (ACCEPTED: the lane belonging to
                                                       address 0x40, OUTSIDE the 0x40-byte
                                                       register file, stored into the
                                                       interrupt mask, then reassert)
    collide   BASE  SCCTX+SCCRX in one session = 2 declines
    collide   M1    SCCTX+SCCRX in one session = 1 decline   (one announce SILENCED)

So both 60/60 scores are DETECTOR HOLES, not equivalences.

## HYGIENE

FINAL CLEARANCE, against the b78bb0f BLOB (the correct oracle):
    clone   : 4c0cfc6d8e6cb099ebe7e92420e6b71e
    b78bb0f : 4c0cfc6d8e6cb099ebe7e92420e6b71e
    PART 1 OK (source == blob)   PART 2 OK (binary rebuilt, -nt source)   SENTINEL CLEARED

The in-table restore checker printed `restore: FAILED -- sentinel KEPT' from M5 onward.
That is a BROKEN CHECKER, not a bad restore: it compared against the SEC WORKTREE, which
the main loop moved mid-run (comment corrections + a `pcc2_w_fits_in_warned' typedef).
Predicted before it fired, and confirmed by md5.  Every restore copied the same frozen
immutable baseline, and the final clearance proves the clone ended byte-identical to
b78bb0f.  The sentinel outliving its mutant is the SAFE direction.

M7's first attempt died in the BUILD on the documented Bash -> heredoc -> Python
backslash trap: `\n' lost one level and became a REAL newline, splitting the C string
literal.  Rebuilt with chr(92) per the carrier's own remedy.  Recorded as apparatus
error, not as a result.

No project tree was written at any point.  Detector md5 identical at start and end
(678fc01000887e3626e8888b82004441), so all findings apply to the CURRENT worktree.

## WHY THE ROUND'S OWN TABLE DID NOT SEE THIS -- and it is visible in its own numbers

    M_OPKILL   58/60   red: op vecbase, op vecbase dcl        (kill reinstated at VECBASE)
    M_DELETE   56/60   red: rb genctl, rb genctl dcl, both latch rows
    M_SHARED   59/60   red: latch two   <-- ONE ROW, and only one

Every mutant in the round's table is either GLOBAL (all twelve arms) or aimed at GENCTL
or VECBASE -- the two arms with the richest rows.  None is scoped to an arm chosen for
having few rows.

`M_SHARED` collapsed ALL TWELVE blocks onto one bit -- the MAXIMAL collision -- and was
caught by `latch two` ALONE.  That single result should have prompted the question the
round did not ask: *what if the collision misses the one pair that row observes?*  It
escapes completely (M1, 60/60).

The round MEASURED the maximal case and INFERRED coverage of the class.

## M7 (retried correctly) AND THE Q1 MEASUREMENT

    M7   verbatim exit(1) kill reinstated at PCCTWO_IPL (0x3e)   60/60  CLEAN SWEEP

That is a GUEST-REACHABLE HOST KILL reinstated at an arm this round converted, and the
gate-enforced 60-row detector does not move.

Q1, measured on the restored BASE binary:

    byte  ld.bu IPL   IPL==0-diagnostic=True   old-"ignored"-msg=False   r4=0x0
    wide  ld.hu IPL   IPL==0-diagnostic=True   old-"ignored"-msg=False   r4=0x0

The read-side ACCEPT is CORRECT at IPL: a wide read now reaches the read-side
`IPL == 0' latch exactly as a byte read does, and the old "non-byte access ...
ignored" message -- which used to be printed ABOUT A READ THE MEMCPY HAD ALREADY
SERVED -- is gone.  The fix RESTORES a diagnostic the old guard suppressed.

## FINAL TALLY

    BASE  60/60          M4   60/60  EQUIVALENT (writeflag domain is {0,1})
    M1    60/60  SWEEP   M5   59/60  killed (latch same)
    M2    60/60  SWEEP   M6   60/60  SWEEP
    M3    49/60  killed  M7   60/60  SWEEP
    M8    60/60  SWEEP   M9   60/60  SWEEP
    M10   60/60          DISCLOSED blind spot, correctly

SIX CLEAN SWEEPS.  Smallest: ONE CHARACTER.
