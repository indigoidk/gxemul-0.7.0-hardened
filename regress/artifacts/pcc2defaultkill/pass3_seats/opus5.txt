# SEAT_501P3_20260905 -- Opus 5 seat, #501 pcc2defaultkill PASS 3 (the pass on the repair diff)

Liveness quote, first line of
GXEMUL-SEC/regress/artifacts/pcc2defaultkill/killtable3_20260905/PRETABLE_501b.out, VERBATIM:

> PRE-TABLE BLOCK, #501 pcc2defaultkill PASS-2 REPAIR (table 3) -- written BEFORE the table (mtime against

---

## VERDICT: NOT CLOSE.

**Six MEASURED clean sweeps of the 36-row detector, built and scored in my own scratch clone against
a BASE I rebuilt and re-verified at 36/36.  Two of them are the same floor cell: the exact MIRROR of
the cell this repair exists to close.**

| mutant | edit | 36-row score | disposition |
|---|---|---|---|
| M_WRVAL0 | write announce `(int) idata` -> `0` (one token) | **36/36 SWEEP** | **L2 floor breach** -- the mirror of my pass-2 M_O1, neither rowed nor disclosed |
| M_WRDATA0 | write announce `(int) idata` -> `data[0]` | **36/36 SWEEP** | same cell, a MORE plausible edit that the repair's own new comment invites |
| M_LASTBYTE | read announce `data[0]` -> `data[len-1]` | **36/36 SWEEP** | L4 (the contract asserts and disclaims one class) + cheap disclosed debt |
| M_RELOAD | read announce `data[0]` -> `d->pcctwo_reg[relative_addr]` | **36/36 SWEEP** | the pass-2 PRODUCT repair (disposition 7) is UNROWED and not disclosed as unrowed |
| M_BACKEDLOW | `if (writeflag == MEM_WRITE && relative_addr < 0x14) d->pcctwo_reg[relative_addr] = idata;` | **36/36 SWEEP** | member 6 conditioned off the two offsets that read back -- the #499 shape |
| M_LATCHOFF | latch SET restricted to IEICR/IEERR |  **36/36 SWEEP** | the same class on the latch axis |

**BASE reproduces at 36/36 in my clone**, so each sweep is a real escape and not a broken rig.
The round's own table 3 is SOUND: I re-read all nineteen artifact .out files and every one of the
twelve scores plus all seven old23 23/23 controls matches the record exactly.

---

## What I ran (every number names its log; scratch clone only)

GXEMUL-SEC, build, est and build-asan were never written.

```
wsl -d Gentoo -- bash <scratch>/base_build.sh
    cp -a /mnt/c/.../build /tmp/gxopus501p3
    CLONE_SRC_CMP_CLEAN_VS_SEC                       (clone src == GXEMUL-SEC src, byte-identical)
    rm -f src/devices/dev_pcc2.o gxemul ; make -j4    MAKE_RC=0
    gxemul 08:20:58  >  dev_pcc2.c 07:27:04          BINARY_NEWER_OK
    md5(GXEMUL-SEC/regress/pcc2_default_probe.py) = 10737375f192f22c7bae8d1efb9d54c1
        == the record's claimed live md5 AND == killtable3_20260905/frozen_probe.py  (both md5sum'd)

cd GXEMUL-SEC/regress && python3 -u pcc2_default_probe.py /tmp/gxopus501p3/gxemul opus_base
    -> PCC2D_RESULT=36/36                            (probe_base.out)

wsl -d Gentoo -- bash <scratch>/mutdrv.sh <names...>
    .MUTANT sentinel written BEFORE each mutation; each mutant restored from a frozen baseline copy,
    diff-line count printed (2 for every mutant here), rebuilt from a removed .o, binary-newer
    checked, probe run from the LIVE (unedited) instrument.
    RESTORE_CMP_CLEAN_VS_SEC ; RESTORE_MAKE_RC=0 ; SENTINEL_CLEARED (cmp clean AND binary newer).
```

*Apparatus defect of my own, disclosed:* M_WRVAL0's first attempt failed on a stale multi-line anchor
in my edit script -- I rewrote the script while the driver was already running, which is the
edit-a-file-underneath-a-running-job hazard in its python form.  Re-run separately; the single-line
anchor `(int) len, (int) idata);` is unique in the file, count == 1 verified from WSL python.

Logs beside this file: probe_base.out, probe_M_*.out, mutdrv*.log, edit_M_*.py, base_build.sh,
mutdrv.sh, runprobe.sh.

---

## 1.  THE WRITE ANNOUNCE'S VALUE IS UNPINNED -- the mirror of my own pass-2 finding, left open by the repair for it.  MEASURED 36/36, twice.

**The 2x5 product, derived from the arm's own body-read set** (writeflag, idata, len, data[0] -- the
PRETABLE's own GUARD-FIELD line names exactly these).  The announce has five observable channels;
writeflag partitions them into two arms:

| channel | WRITE arm | READ arm |
|---|---|---|
| FATE (host lives) | named/inword/unnamed/alias/wide wr | named/inword/unnamed rd, wide rd |
| COUNT (the latch) | named wr msg, latch sameoff/twooff/rw one/rd wr/aba | named rd msg, latch rd rd |
| DIRECTION text | dir wr text, wr declined | dir rd text |
| WIDTH text | wide wr msg | wide rd srvd |
| **VALUE text** | **NO ROW** | srvd val text  <- added by THIS repair, for my M_O1 |

Nine of ten cells are rowed.  The tenth is the WRITE arm's value -- the same cell type on the sibling
arm of the one this whole repair exists to close.  Nothing in the CONTRACT claims it; nothing in the
DISCLOSED list disclaims it.

M_WRVAL0 is `(int) idata` -> `0`, one token, inside the announce the diff itself edited.  Every row
that touches the write announce counts a PHRASE, never a value: named wr msg counts MSG, dir wr text
counts "unimplemented write to", wr declined counts "declined", wide wr msg counts
"offset 0x28 (len 4)" -- all still present.  wide wr / ieicr rdawr / ieerr rdawr / sameoff val read
the ARRAY, not the text.  **Measured 36/36, row for row identical to BASE.**

> **This is the #499 shape the repair-chain amendment names, reproduced inside its own repair:
> "the original breach, reproduced inside its own repair, by someone who had just spent an hour
> understanding it."  My M_O1 was *the announce's VALUE channel is unpinned*.  The repair pinned it on
> the arm the mutant happened to use and left the mirror open.**

M_WRDATA0 reaches the same cell by a MORE plausible edit and also measured 36/36: a future reader of
the repair's new comment ("data[0] is the byte actually SERVED") makes the two branches symmetric and
prints data[0] on the write side too -- which for a wide write emits only the most-significant byte
(0x5a for a stored 0x5a5a5a5a).  A wrong record in product code, invited by the repair's own comment.

**GRADE: L2, floor breach, repair in-round.**  Clause (d) DEPENDS-ON: idata is a body-read lvalue of
the guarded body and writeflag is the body-tested predicate that partitions it; the round itself
graded the READ half of this same joint cell a floor breach at pass 2.  An exemption keyed to which
arm the pass-2 mutant happened to use is exactly the provenance-keyed exemption the repair-chain
ruling rejects.

**THE ROW -- zero new sessions.**  dir wr text's session already stores 0x5a at PRTICR:

```python
row("wr val text", t.count("0x30 (len 1): 0x5a") if alive else "n/a", 1,
    "...and the announce prints the VALUE WRITTEN: idata->0, or ->data[0], is a wrong record (the WRITE mirror of `srvd val text')")
```

and in wide wr msg's existing session, `t.count("(len 4): 0x5a5a5a5a") == 1` additionally kills
M_WRDATA0, whose byte form prints 0x5a.

---

## 2.  M_LASTBYTE -- 36/36 MEASURED.  data[0] -> data[len-1]

Row for row identical to BASE, srvd val text, wide rd and wide rd srvd included.

**Why the row built for the width axis cannot see it.**  wide rd reads PRTICR (0x30..0x33), whose four
array bytes are all 0x00 and are unreachable by any guest write under member 3.  So wide rd srvd's
oracle -- `t.count("(len 4) -- served 0x00")` -- **cannot vary under a mutant that changes WHICH byte
is announced.**  That is the pre-table CHANNEL check's own failure mode, and the block says it is
knowable at writing time: "A row whose named channel cannot vary under its named mutant is VACUOUS BY
CONSTRUCTION."  The row is not vacuous for its named mutant (M_WIDEKILL, a host exit); it is vacuous
for the property its own note asserts -- "names the width and the FIRST served byte".

**The contract asserts and disclaims the same class, and a reader cannot tell which governs.**
CONTRACT: "the read announce printing **a wrong or constant byte** ... -> srvd val text" -- a wrong
byte includes data[len-1].  DISCLOSED: "the announce names the FIRST served byte of a wide read",
under a header reading "DISCLOSED, not caught".

**GRADE: L4 (reconcile the two sentences) + disclosed coverage debt -- NOT a floor breach**, because
the disclosure, however ambiguously, is present.  I am deliberately not promoting my own finding past
what the contract's own words support.

**THE ROW -- zero new sessions, and it retires the disclosed len-2 item at the same time.**  The
srvd val session already does ST_W(0x12345678, T1CMP), so the array holds 12 34 56 78 at 0x04..0x07
(srvd val measuring 0x34 proves it).  Append a half-word load into a register the row does not print:

```python
LD_HU = lambda rd, off: enc(0x02, rd, 2, off)      # the width probe's own encoding
... program([ST_W(5, T1CMP), LD_BU(4, 0x05), LD_HU(6, 0x06)]) + ["print r4"]
row("srvd half", t.count("0x6 (len 2) -- served 0x56") if alive else "n/a", 1,
    "a len-2 read at 0x06 announces its FIRST byte 0x56 (data[len-1] would say 0x78): pins WHICH byte, and drives len 2")
```

srvd val (prints r4 = 0x34) and srvd val text (counts "served 0x34") are untouched -- the new
announce reads "served 0x56".

---

## 3.  M_RELOAD -- 36/36 MEASURED.  The pass-2 PRODUCT repair has no row, and that is not disclosed.

data[0] -> d->pcctwo_reg[relative_addr] is **the exact pass-2 code**: a verbatim reinstatement of the
product defect codex found and disposition 7 fixed.  It sweeps.

**I am NOT calling this a floor breach, and the reason is a measurement rather than charity.**  The two
expressions differ only if something rewrites the array between the memcpy and the announce.
pcc_timer_tick() writes T1COUNT (0x0c) and T2COUNT (0x10) and nothing else; T1CMP (0x04), where
srvd val text reads, is **never** touched by the tick.  So the difference is an asynchronous race that
no deterministic row can pin -- the carrier's "a mutant that will not die is a result", case 2/3:
near-equivalence, which is a finding about the code.

**But the record does not say that.**  The CONTRACT files disposition 7's fix under "a wrong or
constant byte -> srvd val text", which is measurably false for the reload form.  **GRADE: L4.**  One
DISCLOSED sentence makes it honest and costs nothing:

> "a revert of data[0] to a reload of the array is NOT rowed: the two differ only when the tick
> rewrites the byte between the memcpy and the announce, a race no row can pin; the repair is a
> robustness fix, not a rowed one."

*A second, smaller thing found here, and it strengthens the repair rather than weakening it:* the
product comment's stated reason -- "the tick rewrites the counter interiors" -- overstates the
population.  Only T1COUNT's and T2COUNT's eight bytes are tick-written; the four T1CMP/T2CMP
interiors (0x05-0x07, 0x09-0x0b) are not.  data[0] is still the right expression -- it is what the
guest got, unconditionally, on both the memcpy and the zero-fill paths -- only the stated reason is
loose.

---

## 4.  M_BACKEDLOW -- 36/36 MEASURED.  Member 6, conditioned off the two offsets that read back.

```c
if (writeflag == MEM_WRITE && relative_addr < 0x14)
        d->pcctwo_reg[relative_addr] = idata;
```

This is the round's own M_BACKED with `if (X)` -> `if (X && Y)` -- the canonical clause-(d) weakening
-- and it restores precisely the surface the round's warrant says it is refusing: "a store from the
one arm 43 offsets reach would add a bounded-write surface."  It is highly plausible: "the twelve
in-word bytes are the interior of IMPLEMENTED counter/compare words, so a byte store there should
land" is pcc2widecompose's stated business, named in this very contract.

**Why every disposition row is blind.**  The DISPOSITION (declined vs backed) is read back at exactly
**two** of the 43 uncased offsets: 0x2a (ieicr rdawr, sameoff val) and 0x28 (ieerr rdawr, wide wr).
inword wr / inword rd and unnamed wr / unnamed rd are **separate sessions, i.e. separate processes**,
so a store in one cannot be observed by the read in the other.

> **The record's sentence "every one of the 43 uncased offsets is written once and read once" is TRUE
> and is doing work it cannot do.  It closes the FATE axis at 43 offsets.  It closes the DISPOSITION
> axis at 2.**

**GRADE: I do NOT call the 43-offset disposition product floor** -- 43 per-offset value rows is the
#392 shape the flagship bound exists to refuse.  **But it is undisclosed**, and it retires for one row
per offset CLASS, which is the partition the probe already uses:

```python
# inword wr's EXISTING session, after the twelve stores -- zero new sessions:
... program([ST_B(5, o) for o in INWORD] + [LD_BU(4, 0x05)]) + ["print r4"]
row("inword val", val(t, alive, how), "0x0",
    "a declined write at a COUNTER INTERIOR does not land (a class-conditioned member 6 reads 0x5a)")
# unnamed wr's existing session, likewise: LD_BU(4, 0x20) -> want 0x0
```

Three classes x one read-back closes the disposition axis per class, bounded and derivable.
M_BACKEDLOW reddens inword val at 0x5a.

**The LATCH-SET axis has the identical shape.**  Every row that revisits one offset uses 0x2a or 0x2b,
so a set restricted to IEICR and IEERR leaves the latch armed at 41 offsets.  (Restricting to IEICR
ALONE is RED on wide wr msg, whose session revisits 0x28 -- that one IS caught, which is why the pair
is the interesting form.)  M_LATCHOFF measured: **36/36, a sixth clean sweep**.  Cheapest closure, again zero new
sessions: make named wr msg's session write each of the 18 offsets **twice** -- the wanted count stays
18 and a per-offset set-exemption at any of them then prints 19 or more.

---

## Answers to the QUESTIONS

### Q1 -- IS THE REPAIR RIGHT?  Yes.  Every clause checked.

* **data[0] is the byte the guest received on BOTH paths.**  Memcpy path: the memcpy sits above the switch and nothing between it and the announce touches data.  End-span path (relative_addr + len > 0x40): memset(data, 0, len), so "served 0x00" is truthful.  **A third backstop the record does not name:** memory_rw.c's #95 pre-zeroes the caller's buffer on every read BEFORE device dispatch, so data[0] is defined even on a path that fills nothing.
* **WRITE arm: data is unused** -- it prints idata from memory_readmax64.  Correct.
* **(int) len fits** (len is at most 8 here; the explicit cast with %d is right).  data[0] is unsigned char, promoted; %02x correct.
* **No text anchor breaks:** I re-measured BASE at 36/36 on my own clone, and BASE.old23.out = 23/23 is in the artifacts.
* **The fold:** PCC2_SIZE == 0x0040 (mvme_pcctworeg.h:14), the %= is the handler's first statement, uint64_t shift of 0..63 -- defined.  warned_unimpl is a dedicated field used at exactly two sites; **no shared-bitfield collision** with the width latch field.  That is the hazard the #490 note says the guard-field check cannot see, so I checked it directly rather than assuming.
* **Census re-derived, not transcribed.**  The switch has **21** case labels; 0x40 minus 21 = **43** uncased; enumerating them against mvme_pcctworeg.h reproduces exactly the probe's NAMED18 (18) + INWORD (12) + UNNAMED (13).  The premise holds.
* **Gate/probe agreement checked mechanically:** 36 row() calls, 36 gate names, set difference empty in both directions, no duplicate names, longest name 13 chars (the padded-column anchor needs 14 or fewer).  The derived-list claim holds.

### Q2 -- DOES EACH MUTANT DIE FOR THE REASON CLAIMED?  Yes for all twelve; one prediction miss is unrecorded.

Checked mechanism-against-row for the six repair mutants; they are honest kills, not accidents.
M_WRLATCH reds latch rd rd and latch rd wr and correctly leaves latch rw one GREEN (the write still
sets the bit the read tests) -- **that green is the proof the two new cells were genuinely unreachable
before.**  M_ABA reds only latch aba (A,B,A is the only row that revisits an offset after another has
announced).  M_SRVD0 reds only srvd val text and correctly leaves wide rd srvd green (it IS 0x00
there).  M_BACKED2 reds only sameoff val, which requires the latch already set -- ieicr rdawr cannot
see it, exactly as claimed.  M_OFFKILL at 0x06 reds inword wr and inword rd, reachable only through
the 12-offset expansion.  M_WIDEKILL reds all four wide rows.

**One prediction miss, in the SAFE direction, and it is NOT recorded.**  PRETABLE_501b.out predicts
"M_UNLATCH ... latch sameoff 2".  M_UNLATCH.out measures **latch sameoff got=3** -- because this very
repair added a third access (the sameoff val read-back) to that session.  Score and red set are exact;
the per-row VALUE is not.  **The PRETABLE's own closing rule is "A miss in the SAFE direction is
recorded", and no such record exists.**  A number carried forward from pass 2 into the pass-3
prediction file: the frozen-number class, small, and in the safe direction.  **L4, one clause.**

### Q3 -- IS ANY CELL STILL OPEN?

Yes: (a) the WRITE arm's VALUE channel -- **floor**, section 1; (b) the byte-SELECTION sub-cell of the
read announce's value, section 2; (c) the DISPOSITION and LATCH-SET axes over the 41 offsets outside
0x28 and 0x2a, section 4.

**Nothing in the DISCLOSED list is floor by the "predicate the arm tests" criterion.**  The arm tests
exactly the latch bit and writeflag == MEM_WRITE.  len is printed, never tested, so the len-2 item is
correctly disclosed rather than owed; the body tests no bit of idata, so the flagship generating-set
clause raises nothing here.  (The len-2 item is nonetheless worth retiring, because the srvd half row
proposed in section 2 closes it and the byte-selection cell together, for one row.)

### Q4 -- THE SMALLEST EDIT THAT BREAKS THE PROPERTY AND PASSES 36 ROWS.

Six, all BUILT and MEASURED rather than derived: M_WRVAL0, M_WRDATA0, M_LASTBYTE, M_RELOAD,
M_BACKEDLOW, M_LATCHOFF -- every one 36/36.  The rows I expected to stay green, and why, are in each
section above; every expectation was confirmed by the run rather than asserted.

### Q5 -- IS THE RECORD HONEST?  Mostly.  Five sentences are refuted by a measurement.

1. **CHANGELOG.md line 6 -- "Detector: regress/pcc2_default_probe.py, 23 rows, run by gate 14."**  The
   shipped detector has **36** rows and gate14_501b.log pins 36.  This is the round block's headline
   bold summary, the sentence a future reader trusts first.  CHANGELOG.md line 59's heading
   "The detector (..., 23 rows; gate 14 pins them)" is the same defect one level down.  **L4.**
2. **CHANGELOG.md line 201 -- "875 checks ok"** against gate14_501b.log, which says PASS (857 checks);
   counting its ok lines gives **857**.  A transposed digit, refuted by the artifact the sentence
   itself cites.  857 is also the arithmetically right number: the pass-2 gate's 844 plus the 13 added
   rows.  **L4.**
3. **The CONTRACT's "a wrong or constant byte -> srvd val text"** -- measurably false for data[len-1]
   (section 2) and for the reload (section 3).  **L4.**
4. **The CHANGELOG's denominator sentence** -- "NOT closed, disclosed in the contract: len-2-only
   re-kills; an end-spanning wide read; per-instance latch scope" -- is a **strict subset** of the
   probe docstring's own DISCLOSED list.  It drops "the announce names the FIRST served byte of a wide
   read", which is exactly the cell M_LASTBYTE occupies.  A closing zero must carry ITS denominator;
   two denominators that disagree are not one.  **L4.**
5. The unrecorded safe-direction prediction miss (Q2).  **L4.**

**Counts with derivers -- checked, and these hold:** 43 uncased offsets (re-derived from the switch and
the header); 36 rows equal to 36 gate names (extracted and compared both ways); md5 10737375
frozen == live (both md5sum'd here); 21 case labels; witness 7/13 committed and 13/13 fixed (read from
witness_committed.out and witness_fixed_501.out); all twelve table-3 scores and all seven old23 23/23
controls (read from the nineteen .out files).  build/ passed the two-part clearance at the moment I
cloned it (source cmp-clean against SEC; gxemul 07:31:56 newer than dev_pcc2.c 07:27:04).

### Q6 -- CLOSE?  No.

Section 1 is a floor breach, and the floor says repair in-round however late it is found.  Sections 2,
3 and 4 are records defects with two-line, zero-new-session repairs.  What I would ship: four rows
(wr val text, srvd half, inword val, unnamed val) plus the doubled named-wr-msg writes; three
DISCLOSED sentences (the reload race; the disposition axis closed per CLASS not per offset; the
latch-set axis likewise); and the five L4 corrections.  That is ONE diff, and by the class-closure
amendment the next pass should VERIFY THE ENUMERATION (the 2x5 announce product and the three offset
classes) rather than hunt further cells.

**The denominator of MY zero, stated as the rule requires.**  I built and measured six mutants against
the repaired 36-row instrument, on a BASE I rebuilt and re-scored myself.  My sweep covers: the
announce's five channels crossed with writeflag; the byte-selection axis of the served value; the
data[0]-versus-array axis; member 6 conditioned on the offset; the latch set conditioned on the
offset.  It **EXCLUDES**: multi-clause composites; anything touching the eleven cased arms or the #119
end-span path; per-instance latch scope (no fixture exists -- pcc2latchinst); and any mutant of the
width-guard blocks, which are pcc2widthkills' business.

---

## Found while verifying something else

Chasing section 3 I read pcc_timer_tick().  Its two write32 stores into T1COUNT and T2COUNT are
**unconditional** -- they run on every tick whether or not PCC2_TCTL_CEN is set (the value is merely
unchanged when the timer is disabled).  Harmless today, but it means **eight of the twelve counter
interiors the default arm serves are written from a host-timer callback and four are not**, while the
product comment attributes the rewrite to all twelve.  Not this round's business; recorded because the
halves differ and the comment does not say so.
