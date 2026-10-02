# DERIVATION.md -- #529 closing pass 8, Opus MEASURING seat.  The DENOMINATOR, derived before any mutant was built.

Every number here comes from a script in `scripts/`, run against the SHIPPED probe
(`regress/crime_width_probe.py`, md5 `2818bd4ea28ac3b6347fec4e219cc4c9`) and the SHIPPED fix
(`src/devices/dev_sgi_ip32.c`, md5 `8c1d1545eeddd12fd49f52ccede60262`, the UNCOMMITTED #529 working set).
**Re-run the scripts; do not quote these literals.**

    scripts/cellmap8.py     the POST-latch half:  118 accepted CRIME accesses, 18 of 51 sessions
    scripts/cellmap8b.py    the same, per session, with each session's row names
    scripts/preclear8.py    the PRE-latch (latch-CLEAR) half:  102 accepted CRIME accesses
    scripts/sessrows.py     every session that drives a 4-byte access at a NAMED label with the latch CLEAR

## 1.  THE HANDLER'S OWN PARTITIONS, read off `DEVICE_ACCESS(crime)` at `dev_sgi_ip32.c:193-421`

The brief's inlined copy of the function is byte-accurate -- I checked it line by line against the source before
using it.  The accept path tests SIX partitions of guest-controlled input:

| what | where | in the enumeration? |
|---|---|---|
| `len` -> {8, 4, declined} | `:275`, `:280`, `:296` | **yes** -- axis 2 |
| `writeflag` -> {WRITE, READ} | `:276`, `:281`, `:356`, `:397`, `:419` | **yes** -- axis 3 |
| `relative_addr` as a LABEL -> 7 arms | `switch` at `:322` | **yes** -- axis 4 |
| `relative_addr` as a LANE -> `& 4` | `:282` **and** `:291` -- twice, inside the `len == 4` arm | **NO** |
| `cpu->pc` -> the PROM-probe window | `:344` | **NO** |
| `idata` -> DOG 0x200, HARD_RESET 0x800, leftover != 0 | `:361`, `:364`, `:377` | disclosed as clause-(e) joints |

The latch axis is sound: `d->warned` has **exactly one reader and one writer**, both inside the decline arm
(`:314`, `:315`), and `CRIME_W_LEN` appears nowhere else in `src/` -- so "pre-latch" is exactly "before this
session's first 1- or 2-byte CRIME access", which is what the maps compute.

## 2.  THE LANE AND THE WINDOW ARE UNNAMED AXES, AND THE LANE IS UNSATISFIABLE AT EVERY NAMED LABEL

CRIME_REV 0x00, CRIME_CONTROL 0x08, CRIME_INTSTAT 0x10, CRIME_INTMASK 0x18, CRIME_DOG 0x30, CRIME_TIME 0x38 are
all 8-ALIGNED, so `relative_addr == CRIME_X` implies `(relative_addr & 4) == 0`.  A mutant conditioned on
`relative_addr == CRIME_X && (relative_addr & 4)` is unsatisfiable, not merely unrowed.  The lane is a free axis
only at the `default` arm -- where `+0x04`, `+0x0c`, ... `+0x34`, `+0x3c` land.

`scripts/cellmap8.py` therefore reports 14 empty cells on the finer product and every one of them is one of those
unsatisfiable `lane=1 at a named label` cells.  **On the finer product `{latch set} x {len} x {dir} x {label} x
{lane} x {window}` every SATISFIABLE cell has at least one post-latch accepted access.**  Since a K-form mutant can
only act through a post-latch access at its own cell, occupancy is a NECESSARY condition for a kill, and it is met
everywhere.

## 3.  THE POST-LATCH HALF IS DENSE; THE PRE-LATCH HALF HAS A HOLE, AND IT IS `latch x5`

`scripts/preclear8.py` + `scripts/sessrows.py` give the complete latch-CLEAR table for the twelve
4-byte-at-a-named-label cells:

| cell | sessions driving it with the latch CLEAR | a row that can see a SILENT decline there |
|---|---|---|
| REV 4W in window | 40, **42** | `revP sw pc` |
| REV 4W out of window | **40 only** | none -- EQUIVALENT (the prelude rewrites reg[0] at `:229`) |
| REV 4R in window | 40, **1** | `rev pc ctl` -- its redirect needs the access ACCEPTED |
| REV 4R out of window | 40, **0** | `devsig hi` reads 0 either way -- blind, but EQUIVALENT |
| CTL 4W | 40, **2, 3** | `sw08 halts`, `sw08 msg ctl` |
| **CTL 4R** | **40 ONLY** | **NONE** |
| IST 4W | 40, **44** | `istw sw` |
| **IST 4R** | **40 ONLY** | **NONE** |
| IMK 4W | 40, **43** | `acc imask sw` |
| IMK 4R | 40, **20** | `gate line` -- the gate session's `lw +0x18` is what reasserts IP2 (`:723`, `:736`) |
| DOG 4W | 40, **4** | `acc4 whi` |
| DOG 4R | 40, **4** | `acc4 rhi` |
| **TIM 4W** | **40 ONLY** | **NONE** |
| **TIM 4R** | **40 ONLY** | **NONE** |

Session **40 is `latch x5`** (`crime_width_probe.py:1040-1080`).  It runs all 46 ACCEPTS entries as its prologue and
carries exactly THREE rows -- `latch x5` (an announce COUNT), `latch surv` (a RAM round trip) and `latch said` (the
announce TEXT of the `lh +0x06` that follows the prologue).  **A silent `goto crime_declined` in that prologue
touches none of the three:** it prints nothing, so no count moves; it does not set the latch, so the `lh` still
carries its own announce; and the host stays alive.

The 8-byte latch-clear cells are all covered -- every one has a second driving session with a value oracle -- so the
hole is exactly the 4-byte column, and exactly four of its twelve cells.

## 4.  WHY THIS IS THE K-CLASS'S OWN ARGUMENT, POINTED THE OTHER WAY

Closing pass 7 graded the K-class FLOOR because *"every value row this probe had was measured with the latch
CLEAR, so none of them could see a guard conditioned on it."*  Repair 13 answered by adding `p *` rows that run
with the latch SET.  **It did not add any row that runs with the latch CLEAR at a cell only `latch x5` reaches** --
and `latch x5`'s rows cannot see a silent decline in either state.  So the same sentence, with "CLEAR" and "SET"
exchanged, is true of repair 13.

The contract's own amended clause says a silent bypass is caught only where *"THE CATCHING ROW RUNS IN THE
BYPASS'S OWN LATCH STATE"*.  For these four cells no row runs in the CLEAR state at all.

## 5.  A SECOND, INDEPENDENT HOLE ON THE LATCH-**SET** SIDE: THE GENERATING SET AT CONTROL

The 2026-09-04 generating-set clause: *"At each floor cell, every idata bit the guarded body TESTS is written both
clear and set."*  The CONTROL arm tests three idata bits.  Derived from `scripts/cellmap8b.py`, the post-latch
CONTROL writes in the whole 188-row probe are:

    session 46 (P2)   sd +0x08 <- 0x01      sw +0x08 <- 0x0001      sw +0x08 <- 0x0201
    session 26 (rearm once, no value oracle)   the ACCEPTS values 0x0201, 0x0001, 0, 0x0200, 0x0100

**HARD_RESET (0x800) is CLEAR in every one of them.**  The only session that writes 0x800 at CONTROL is
`sw08 halts` (session #2) and it writes it BEFORE any refusal.  So at the latch-SET CONTROL-4W and CONTROL-8W floor
cells that bit is never driven -- which is what the codex seat named, and it is a breach of a DIFFERENT clause from
the latch-clear one.

## 6.  WHAT I BUILT AND RAN

Table A (`scripts/kill8.sh`, frozen as `kill8.run-200658.sh`), 13 mutants + base on the shipped 188-row probe:
the four DEFAULT-arm lane splits; the four REV window splits; three lane-FLIP shapes (INTSTAT, TIME, and an
all-labels negative control); a latch-keyed refused-store LANDING; a latch-keyed register RE-MAP.

Table B (`scripts/kill8b.sh`, frozen as `kill8b.run-202251.sh`), 8 mutants: `C_ctl4r` re-derived and cmp'd
byte-for-byte against killtable11's own diff; `G_lane_ctl` (the CONTROL-4R liveness control); the four latch-CLEAR
bypasses; the two CONTROL HARD_RESET generating-set cells.  Three purpose-built probes carry the owed rows --
`scripts/ctl4r.py`, `scripts/t4clear.py`, `scripts/ctlreset.py` -- each with its own liveness and device-signature
controls, and each measured on BASE as well as on its mutant.
