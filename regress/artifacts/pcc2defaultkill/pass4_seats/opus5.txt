# #501 `pcc2defaultkill` — PASS 4 — Opus 5 seat (the compile-and-measure seat)

`SEAT_501P4_20260905`

First line of `regress/artifacts/pcc2defaultkill/killtable4_20260905/PRETABLE_501c.out`, verbatim:

> PRE-TABLE BLOCK, #501 pcc2defaultkill PASS-3 REPAIR (table 4) -- written BEFORE the table (mtime against

---

## VERDICT: **NOT CLOSE.** I measured **four 46/46 clean sweeps** of the shipped 46-row composite — every one on an axis the pass-3 repair itself introduced (WIDTH, and the OFFSET LABEL) — and found **four L4s**, two of them present-tense claims that this defect still ends the host, one of those in the product file this round edits.

**The FIX is right and I say so without reservation.** I re-verified the guard bound (`%= 0x40` then
`1ULL << relative_addr`, shift 0..63), `break` reaching the handler's single `return 1`, both announce
operands, that no cased arm is perturbed, and both new comment sentences (against `timer.c` and the
end-span path). Nothing in the product needs changing.

**The DETECTOR's class closure is the problem.** Pass 3 enumerated the announce as `channel x arm`
(ten cells) and closed the tenth. But the axis it was *adding rows on* is WIDTH, so the space is
`channel x arm x width`. **Two of the six VALUE cells and one of the six WIDTH-LABEL cells are open,
and the OFFSET-LABEL channel is pinned at five points out of 43 offsets.** I swept the instrument
through all of them.

---

## WHAT I RAN, AND WHAT IT PRINTED

Scratch clone; nothing written to GXEMUL-SEC, build, est or build-asan.

```
cp -a /mnt/c/.../build /tmp/gxopus501p4                     CLONE_OK
GXEMUL-SEC/src/devices/dev_pcc2.c -> clone                  SRC_CMP_CLEAN_VS_SEC
rm -f src/devices/dev_pcc2.o ; make -j4                     MAKE_RC=0
ls: gxemul 11:26:53  >  dev_pcc2.c 11:26:31                 BINARY_NEWER_OK
frozen instrument PAIR in /tmp/gxinst501p4 (md5, both == the round's own frozen pair):
   pcc2_default_probe.py  b9b2fadcb1e5452ed494eb5fe442e756  == killtable4_20260905/frozen_probe.py
   pcc2_width_probe.py    a080e2bcdc6b4990d42786da17344f95
```

`/tmp/gxopus501p4/.MUTANT` dropped before mutant 1. Driver and edit-script frozen before launch and
not touched while running (my own pass-3 note). Restore verified against **SEC**, then rebuilt:
`RESTORED / MAKE_RC=0 / RESTORE_CMP_CLEAN_VS_SEC / RESTORE_BINARY_NEWER_OK / SENTINEL_CLEARED`.

| run | edit (diff lines) | measured | red rows |
|---|---|---|---|
| **BASE** | — | **46/46** | — |
| `CTL_LASTBYTE` (rig control) | `data[0]` -> `data[len-1]` (2) | **45/46** | `srvd half text` |
| **`MO1_RDWIDEBYTE`** | `data[0]` -> `data[len>>2]` (2) | **46/46 — CLEAN SWEEP** | none |
| **`MO2_WRHALFSILENT`** | `if (writeflag == MEM_WRITE)` -> `... && len != 2` (2) | **46/46 — CLEAN SWEEP** | none |
| **`MO3_RDOFFLABEL`** | read offset label -> `relative_addr < 0x14 ? relative_addr : 0` (2) | **46/46 — CLEAN SWEEP** | none |
| **`MO4_WRHALFVAL`** | write announce `idata` -> `len == 2 ? 0 : idata` (2) | **46/46 — CLEAN SWEEP** | none |

`CTL_LASTBYTE` reproduces table 4 exactly (45/46, sole red `srvd half text`) — the rig is validated
against the round's own measurement before any claim is drawn from it. Logs in `logs/`, each verified
by its `PCC2D_PROBE_DONE` sentinel before copying (the copier refused `MO4` while it was still
running, which is the sentinel rule doing its job).

---

## Q1 — IS THE REPAIR RIGHT? Mechanically, yes — all of it, and the disputed value is MEASURED.

* **Encoders correct.** `cpu_m88k_instr.c:3045` `case 0x02: /* ld.hu */`, `:3053` `case 0x0a: /* st.h */`;
  the size table at `:3063`/`:3071` gives both `opsize = 1` (2 bytes), `store = 1` only for `0x0a`.
  `cpu_m88k.c:995/1003/1012` agrees.
* **Alignment is enforced before `memory_rw`.** `cpu_m88k_instr_loadstore.c:168-172` raises
  `M88K_EXCEPTION_MISALIGNED_ACCESS` on `addr & (LS_SIZE-1)`. `0x06` (halfword) and `0x07`/`0x21`
  (bytes) are all legal. **This is load-bearing for Q3/Q4** — it is why a len-4 default read can only
  start at a word-aligned uncased offset.
* **`srvd wr latch` == 0x78: MEASURED** (BASE prints `srvd wr latch 0x78 ok`). The chain, verified step
  by step: `st.w 0x12345678` at the CASED `T1CMP` (0x04) fills 0x04..0x07 = `12 34 56 78`;
  `ld.bu 0x05` -> 0x34 and announces (bit 0x05 set); `ld.hu 0x06` -> 0x5678, announces
  `(len 2) served 0x56` (bit **0x06** set — a len-2 access sets only the bit of its own
  `relative_addr`); `st.h 0xaabb 0x06` -> silent, DECLINED; `ld.hu 0x06` -> 0x5678; `ld.bu 0x05` ->
  0x34, silent; `st.b 0xbb 0x07` -> **bit 0x07 was still clear**, so it announces and is declined,
  leaving the array byte 0x78; `ld.bu 0x07` -> **0x78**. Yes: the declined `st.b` leaves the byte the
  cased word store put there.
* **Text-anchor collisions: none.** The srvd session emits exactly three announces (0x5, 0x6, 0x7) and
  the two new anchors match one line each. The `0x6 (len 2)` write text the brief asks about is never
  emitted — **and that is the MO2/MO4 finding, not a reassurance.**
* **Gate anchors: sound, with zero margin.** I diffed the gate's `for v in ...` list against the
  probe's `row("...")` calls programmatically: sets equal, no name over the 14-char `%-16s`+two-space
  limit, and **zero prefix collisions** (`^srvd val  ` does not match `srvd val text`; `^wide wr  `
  does not match `wide wr msg`/`wide wr val`; `^inword rd  ` does not match `inword rdawr`).
  *Hazard, not a defect:* `srvd half text` is **exactly 14** characters. One character of drift and a
  row silently stops being counted — the padded-column trap this project has already paid for once.
* **Premise 1 re-derived exhaustively, not trusted.** The 21 `case` labels resolve to
  `{00,01,02,03,04,08,0c,10,15,16,17,1a,1b,1c,1d,1e,1f,27,2f,3e,3f}`; `set(NAMED18+INWORD+UNNAMED)`
  **equals** `set(range(0x40)) - cased` exactly. 43, nothing missing, nothing miscounted.
* **The tick really is signal-driven** (F2 #7's refutation of Fable holds): `timer.c:332`
  `saction.sa_handler = timer_tick`; `:219` `static void timer_tick(int signal_nr)`; `:284`
  `timer->timer_tick(timer, timer->extra)` called directly from the handler; `dev_pcc2.c:780`
  registers `pcc_timer_tick` via `timer_add`.

---

## Q2 — DOES EACH MUTANT DIE FOR THE REASON CLAIMED? Yes, and the table is honest.

I re-derived every score from the preserved artifacts rather than from the brief's transcription. For
all 34 `.out` files in `killtable4_20260905/`, **`PCC2D_RESULT` + `PCC2D_RED` count = 46 (or 36)
without a single exception**; `driver.log`'s per-mutant lines match the brief line for line; the three
gate logs give `PASS (844)` / `(857)` / `(867)` against 23 / 36 / 46 default rows — the arithmetic
844+13=857 and 857+10=867 holds, with 0 FAIL throughout.

Every new row carries a unique cell: `wr val text` (sole red under M_LEN4W), `wide wr val` (sole under
M_WRDATA0), **`srvd half text` (sole under M_LASTBYTE — I re-measured this myself at 45/46)**,
`srvd rd latch`/`srvd wr latch` (M_LATCHRD0), `inword rdawr` **but not** `unnamed rdawr` under
M_BACKEDLOW (the asymmetry is the point: 0x21 >= 0x14), and `inword msg`/`unnamed msg` (M_LATCHOFF).
**No mutant is killed only by a row not built for it.** The five safe misses are correctly diagnosed
as one class, and every predicted red went red.

*One observation, not a defect:* `srvd val text` is now a **hybrid** row — its anchor observes the
VALUE, its `== 1` observes the latch COUNT. Four of the five safe misses are that ambiguity showing.
It buys coverage and costs localisation; worth one sentence in the contract.

---

## Q3 — THE MIRRORS. Filling the grid the repair implied but never drew.

| channel | READ x1 | READ x2 | READ x4 | WRITE x1 | WRITE x2 | WRITE x4 |
|---|---|---|---|---|---|---|
| **VALUE** | `srvd val text` | `srvd half text` | **`wide rd srvd` — CANNOT VARY** | `wr val text` | **no announce exists** | `wide wr val` |
| **WIDTH label** | `srvd val text` | `srvd half text` | `wide rd srvd` | `wr val text` | **no announce exists** | `wide wr msg` |
| **direction** | `dir rd text` | (same line) | (same) | `dir wr text`, `wr declined` | **no announce exists** | (same) |
| **offset label** | 0x05 | 0x06 | **unpinned** | 0x30, 0x2a (`alias msg`) | **none** | 0x28 |
| **count** | `named rd msg`, `latch *` | — | — | `named wr msg`, `latch sameoff`, `inword/unnamed msg` | — | — |
| **fate** | rowed | srvd session | `wide rd` | rowed | `half wr rdawr` | `wide wr` |

Row by row, the mirror of each of the ten new rows:

1. **`wr val text`** — arm mirror `srvd val text` ROWED; width mirrors: len 4 `wide wr val` ROWED,
   **len 2 NEITHER**.
2. **`wide wr val`** — arm mirror is `wide rd srvd`, whose value is the constant `served 0x00`:
   **NEITHER** — and the contract *claims* it (L4-a).
3. **`srvd half text`** — arm mirror is the WRITE announce at len 2: **NEITHER**.
4. **`half wr rdawr`** — mirror is the len-2 read response, carried by the same row's `ld.hu`: ROWED.
5. **`srvd rd latch`** — setter mirror `srvd wr latch` ROWED. The (setter=READ, tester=WRITE) response
   cell is not separately rowed and **that is correct**: no enumerated mutant distinguishes it from
   `sameoff val`, and rows are owed per enumerated mutant, never per refusing state. I decline to
   manufacture a row demand against my own finding here.
6. **`srvd wr latch`** — mirror `sameoff val` (W,W response) ROWED.
7/9. **`inword msg` / `unnamed msg`** — named-class mirror `latch sameoff` ROWED. The READ-driven count
   in these two classes has no `msg` row (`inword rd`/`unnamed rd` are fate-only), but M_WRLATCH is
   caught at the named class and via `srvd val text`; no new row owed. Adequately covered.
8/10. **`inword rdawr` / `unnamed rdawr`** — named mirror `ieicr/ieerr rdawr` ROWED; the per-class
   asymmetry is measured under M_BACKEDLOW. Closed.

### (A) READ x len 4 x VALUE — `MO1`, **46/46 measured**

`data[0]` -> `data[len>>2]`: `data[0]` at len 1 and len 2, `data[1]` at len 4. Two tokens. It is the
M_LASTBYTE class narrowed to the one width whose row cannot see it, because `wide rd srvd` reads
PRTICR (0x30) whose four array bytes are 0. **Observed, not merely predicted:** in the MO1 log
`wide rd srvd got=1 want=1 ok` — the anchor `"(len 4) -- served 0x00"` still matches because PRTICR's
*second* byte is also 0x00.

**This is why the repair could not remove the blindness — it moved it.** Pass 3 found M_LASTBYTE swept
36/36 *because `wide rd srvd`'s value channel is constant*. The repair added a len-2 row whose two
bytes differ, killing the width-agnostic form, and left `wide rd srvd` exactly as constant as before.
That is clause (f)'s own correction verbatim — *"moving the rows from base to top swapped the
blindness rather than removing it"* — in a new coat.

**I checked whether the cell is UNROWABLE (my first reading) and refuted myself.** Exhaustive
enumeration of every writer of `pcctwo_reg[]` in the file: DEVINIT writes 0x00-0x03 and 0x15; the tick
`write32`s at 0x08 and 0x10; the cased arms write their own byte; and **`dev_pcc2.c:480`
`memcpy(d->pcctwo_reg + relative_addr, data, len)` is the only writer that reaches past its own
offset.** With `relative_addr` in {0x04,0x08,0x0c,0x10}, the only reach into a word-aligned uncased
offset is `0x10 + 8 = 0x18` — an **8-byte `st.d` at T2COUNT fills 0x14**, the sole guest-fillable
member of the ten word-aligned uncased offsets (0x14 0x18 0x20 0x24 0x28 0x2c 0x30 0x34 0x38 0x3c).
So the cell **is** rowable, at one offset, by one instruction — but only through the filed
`pcc2counter8` defect (`OUTSTANDING_BUGS.md:14603`, which names 0x14 explicitly). A row there would
couple this detector to an open defect that a later round must break.

### (B) WRITE x len 2 x the whole announce — `MO2` and `MO4`, both **46/46 measured**

The only `st.h` to the default arm in the entire instrument is `ST_H(7, 0x06)`, whose bit was set one
instruction earlier by the `ld.hu`. **The WRITE announce is never emitted at len 2 anywhere**, so its
existence, direction, width label, offset label and value are all unobserved at that width.
`half wr rdawr` pins the len-2 write's FATE and DISPOSITION; nothing pins its ANNOUNCE.

### (C) the announce's OFFSET LABEL — `MO3`, **46/46 measured**

The read announce's offset label is pinned only at 0x05 and 0x06. `named rd msg`, `named rd srvd`,
`dir rd text` and `wide rd srvd` all count phrases with no offset in them (verified green in the MO3
log at 18/18/1/1), and `alias msg` counts a **write** announce. Zeroing the label for
`relative_addr >= 0x14` mislabels **31 of the 43 offsets** and passes. The contract discloses
single-offset scoping of the *disposition* and the *count*; it says nothing about the announce's own
offset LABEL. On the write arm the label is pinned only at 0x28/0x2a/0x30 — nothing in the in-word class.

---

## Q4 — THE SMALLEST EDIT THAT BREAKS THE PROPERTY AND PASSES 46 ROWS

**`data[0]` -> `data[len>>2]` in the read announce.** One expression, two diff lines, **measured 46/46.**

The row I expected to stay green and why: **`wide rd srvd`**, anchor `"(len 4) -- served 0x00"` — the
mutant prints `data[1]`, PRTICR's second array byte is also 0x00, so the anchor is byte-identical;
every other value row is at len 1 or len 2, where `len>>2 == 0`. Measured: no red rows at all, and the
row's got/want printed exactly as predicted.

Runner-up, equally small and also measured: **`if (writeflag == MEM_WRITE)` -> `... && len != 2`** —
a len-2 default write becomes silent, 46/46.

---

## Q5 — IS THE RECORD HONEST? Four L4s.

**L4-a — the contract claims a class a measurement refutes.** `pcc2_default_probe.py:57-58`:

> *"the READ announce printing the wrong byte of a wide read (Opus M_LASTBYTE `data[len-1]`, MEASURED
> 36/36: `wide rd srvd` reads four ZERO bytes, so its channel could not vary) -> `srvd half text`"*

`srvd half text` is a **len-2** row. `MO1` **is** the read announce printing the wrong byte of a wide
read, and it sweeps 46/46. The sentence diagnoses the exact reason its own repair does not close the
cell, and then claims the class is caught. It is the same shape as the claim it replaced (*"a wrong OR
CONSTANT byte -> `srvd val text`"*): **corrected on the len-1/len-2 half and re-committed on the
len-4 half.**

**L4-b — a score claim naming a run that never existed.** `pcc2_default_probe.py:65-66` ships
*"Opus M_RELOAD, **MEASURED 44/44**"*. There has never been a 44-row instrument: I measured M_RELOAD at
**36/36** on the pass-3 instrument, and table 4 measured **46/46** on the repaired one. The number
matches no log and it sits in the shipped contract — the first artifact a future round reads. This is
the carrier's own *a score claim names its artifact* rule failing inside the detector it was written for.

**L4-c — a present-tense claim, in the product file this round edits, that the defect still kills.**
`src/devices/dev_pcc2.c:114-116`:

> *"NOT FIXED HERE, cited so "twelve kills removed" is not read as "file clean": pcc2c040kill (...) and
> **pcc2defaultkill (an unlisted offset still ends it)**."*

`git diff --stat` shows the round changing this file by 43/7 lines and leaving this sentence
**byte-identical to HEAD** (`git show HEAD:src/devices/dev_pcc2.c` line 116 == working copy line 116).
Its whole purpose is to stop a reader concluding the file is clean, so being wrong makes it actively
misleading, and the next round to read it will believe the arm still kills.

**L4-d — the same claim in a sibling detector's DOES-NOT-CATCH contract.**
`regress/pcc2_width_probe.py:402-403`: *"pcc2defaultkill -- an unlisted offset (0x06, 0x14, 0x18,
0x2c ...) **still ends the host** in `default:`"*. That file is not in the round's working set at all.
A DOES-NOT-CATCH list is exactly where a future round looks to decide whether a host exit is expected —
this one now says a **regression would be in-contract**. (`:1365`'s `NOROW pcc2defaultkill` is correct
and should stay.)

**L4-c and L4-d together are the carrier's mechanical rule 2 — *when correcting a claim, grep for its
siblings before calling it fixed* — going unrun. One `grep -rn "still ends"` finds both.**

**What I checked and found HONEST**, so the negatives are on the record too: the 46-row denominator and
its history (23+13+10); every table-4 score against its own `.out` file; the three gate check-counts;
`PASS (867 checks)` with 0 FAIL; the five safe misses and their single cause; the four pass-1 sentences
corrected **in their own sentences** with the original wording quoted; the late-recorded
`latch sameoff 3`; the M_EXIT 39-red set; the gate name list derived from the probe. **No fitted
number, and no correction hiding in a later paragraph.**

---

## Q6 — CLOSE?

**No — and the remaining work is small, bounded and terminates.**

**Grading precisely, without overclaiming.** `len` and `relative_addr` are **not** body-tested (the arm
has no `if` on either; only `writeflag` is tested), so the floor product is `writeflag x latch-state`,
and I verified all four of those cells are rowed on both the announce and the response channels.
**My four sweeps are therefore clause-(e) DEBT, not floor breaches.** But L4-a makes one of them a
WRONG RECORD, which is fix-in-round regardless; and (B) and (C) are debt that is **neither rowed nor
disclosed**, which is exactly what clause (e) exists to prevent.

**The repair I recommend, in ONE diff, per the repair-chain amendment's class-closure rule.** This is
the third consecutive pass to find the announce's VALUE channel open — pass 2 the read value, pass 3
the write value, pass 4 the read value at len 4 — so the next repair owes **the grid, not the cell**:

1. **Write the `channel x arm x width` grid into the contract**, cells marked rowed / disclosed. The
   closing pass then VERIFIES THE ENUMERATION instead of hunting cells. That is what ends the chain.
2. **Close WRITE x len 2 with one instruction and one row**, appended to an existing session (zero new
   sessions, the pass-3 shape): in the `dir wr text` session add `r7=0xaabb` and `ST_H(7, 0x2c)` —
   0x2c is uncased, halfword-aligned, and its bit is clear there — then
   `row("half wr text", t.count("0x2c (len 2): 0xaabb -- declined"), 1, ...)`. Twelve characters, no
   anchor collision. One row closes direction + width label + value at WRITE x 2, and `0xaabb`
   additionally separates `idata` from `data[0]` at that width (`data[0]` would print `0xaa`).
3. **DISCLOSE READ x len 4 x VALUE rather than row it**, with the derivation above: `wide rd srvd`'s
   value channel is constant because nothing in the file writes PRTICR, and the only word-aligned
   uncased offset a guest can fill is 0x14 via the 8-byte counter store that `pcc2counter8` describes.
   File the row as a rider on `pcc2counter8` rather than couple this detector to an open defect.
4. **Disclose the announce's OFFSET LABEL** as pinned at 0x05/0x06 (read) and 0x28/0x2a/0x30 (write).
5. **Fix L4-b, L4-c and L4-d in place.**

**The denominator I would then accept, with its exclusions stated:** twenty-two mutant shapes plus the
four I built; cells closed = the announce's six channels on both arms at widths 1 and 4, plus width 2
on the read arm and (after step 2) the write arm; the setter x tester direction product; accumulation
across offsets; disposition and read response on the latched path; all 43 uncased offsets driven once
in each direction, with one count and one read-back per class. **EXCLUDED and disclosed:** M_RELOAD —
I re-checked my own pass-3 finding and the disclosure holds, `data[0]` and a reload agree at every
offset a row can reach; **the READ announce's value at len 4**; **the announce's offset label outside
the five pinned points**; len 8; end-spanning reads; a member 6 or a latch scoped to a single unsampled
offset; per-instance latch scope; `debug()`-for-`fatal()` (the probe steps under `-V`, so both print —
a real limit, closable by a free-running breakpoint probe if it is ever worth it).

---

## SOMETHING ELSE, FOUND WHILE VERIFYING

* **`pcc2_width_probe.py:1365` prints `NOROW pcc2defaultkill`.** I checked whether gate 14's other 251
  rows form an additional net over this arm. **They do not — the 46 rows are this arm's entire
  coverage**, which raises the cost of every open cell above.
* **`dev_pcc2.c:104`'s alignment sentence is correct and load-bearing here** — *"every non-byte m88k
  access is alignment-checked BEFORE memory_rw"*, verified at `cpu_m88k_instr_loadstore.c:168-172`. It
  is what makes the len-4 read-value cell hard rather than merely unrowed, and the default arm's
  contract should cross-reference it.
* **Zero margin on the gate's row-name anchor**: `srvd half text` is exactly 14 characters.

## SEAT RECORD

Opus 5, pass 4. BUILT and MEASURED (not a reading): one BASE, one control and four mutants in
`/tmp/gxopus501p4`, instrument md5-verified equal to the round's frozen pair, sentinel dropped and
cleared after a `cmp`-clean restore **and** a rebuild. Four clean sweeps, all reproducible from
`logs/` and `mutate.py` beside this file.

---

## ADDENDUM — the len-4 read-value ROW is MEASURED to work (so option 3 above is a JUDGMENT, not a constraint)

I did not want to leave "the cell is rowable" as a derivation, so I built it. `len4_witness.py`, run
against the RESTORED BASE binary in the clone (`logs/len4wit_BASE.out`):

```
r6(ld.w at 0x14)=0x99887766   want 0x99887766 if the st.d filled 0x14..0x17
MSG: [ pcc2: unimplemented read from offset 0x14 (len 4) -- served 0x99.  (once) ]
```

Two instructions — `st.d r4,r2,0x10` with `r4=0x11223344 r5=0x99887766`, then `ld.w r6,r2,0x14` — give
a **len-4 default read whose announced first byte is a guest-chosen 0x99**. Under `MO1` the same line
would read `served 0x88` (`data[1]`), so a row counting `"0x14 (len 4) -- served 0x99"` kills my
headline sweep outright.

**So the choice at step 3 is a judgment the round must make explicitly, not a limitation:**

* **ROW it** — two instructions plus one row appended to an existing session, and the strongest of the
  four sweeps dies. **Cost: the row depends on the `pcc2counter8` behaviour** (the counter arm's raw
  `memcpy` of an 8-byte write, `OUTSTANDING_BUGS.md:14603`), so the round that fixes that defect must
  also rewrite this row — a detector coupled to an open defect.
* **DISCLOSE it** — no coupling, but the contract must stop claiming the class (L4-a) and must say
  plainly that `wide rd srvd`'s VALUE channel is constant and why.

**Either is defensible; silence is not.** What the round may not do is keep the present contract
sentence, which claims the class is caught while a two-token edit sweeps 46/46.
