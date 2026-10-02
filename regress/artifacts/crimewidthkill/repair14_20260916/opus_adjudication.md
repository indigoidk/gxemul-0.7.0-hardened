# OPUS 5 — THE ADJUDICATION PASS.  Attacking the dispositions.

**OPUS_ADJ_20260917**

First line of `_scratchpad/CHECKPOINT.md`, verbatim:

> `# CHECKPOINT -- 2026-09-16 ~22:2x   HEAD 9c91999 (records)   two rounds in flight, both UNCOMMITTED, ONE MEASURING`

---

## VERDICT

**FIVE OF THE TWELVE ACCEPTED DISPOSITIONS DO NOT SURVIVE, AND THE WORST OF THEM IS MINE.**

* **MY O1 IS WRONG AS DERIVED.**  The decline arm is **not** a second 56-cell product.  It has no
  switch; `relative_addr` is read at exactly one place and flows into no lvalue and no test.  Settled
  by reading `DEVICE_ACCESS(crime)`.  The conclusion O1 was accepted for survives on a different and
  better warrant; the number 112 should not be written down anywhere.
* **SECTION 4b's NINE IS WRONG IN BOTH DIRECTIONS AT ONCE**, and "complete" is false.  Nine ENTRIES is
  **twelve** carrier obligations; **four of the nine can carry no row at all**; and the list is
  simultaneously too small, because `buckets8.py` drops the VALUE axis at its line 88.
* **A11 IS ACCEPTED AND ITS REMEDY IS MEASURABLY VACUOUS** — and the probe's own contract already
  corrected this exact vacuity at a different offset two closing passes ago.
* **A13 WAS ACCEPTED AND NOT APPLIED TO SECTION 5.**  My "predictions matched 6 of 6" is precisely the
  outcome-class metric A13 condemns.  Audited: **5 of 6 on row content, and 1 of 2 on the legs that
  were genuine forward row predictions.**
* **"O1 SUPERSEDES D1 ENTIRELY" IS FALSE.**  D1 sizes the `len` domain, which is an INPUT to the
  decline arm, not a question O1 replaces.

**AND I MEASURED THE ONE THING O4 ONLY DERIVED.**  Two mutants, built in a scratch clone, both logs
ending `CRIMEP_DONE`:

    M5_revlatch    188/188   TOTAL ESCAPE      -- O4's REV cell, no longer a derivation
    M6_istlatch    185/188   istat sb/lh/sh    -- NEGATIVE CONTROL, killed

The control is what makes the escape mean anything: **the identical edit at INTSTAT reds three rows**,
so the detector can see this shape and simply cannot see it at REV.  The decline x latch-SET face now
has **two measured open cells**, which settles §1's question — the mandate is earned on the decline
side too, not merely inherited from the framing.

---

## 1. WHICH ACCEPTED DISPOSITIONS ARE WRONG

Ranked by what they cost the repair.  Each is settled by reading the tree or by a measurement, not
by argument.

---

### 1.1 — SECTION 4b: "NINE TARGETED CARRIERS IS BOTH SMALLER AND COMPLETE."  **WRONG THREE WAYS.**

#### (a) NINE ENTRIES IS TWELVE OBLIGATIONS.  This is A1's own error, one section later.

`buckets8.py` reports `N_PRE_BLIND=8` (entries 1, 3, 8, 21, 32, 33, 40, 46) and `N_POST_BLIND=4`
(1, 3, 4, 8).  The union is nine.  **But entries 1, 3 and 8 are blind in BOTH latch states and owe a
carrier in each**, so the row demand is `8 + 4 = 12`, not 9.

The packet calls nine "a count whose members are listed, which is what §C4 demands."  It is a count of
ENTRIES presented as a count of ROWS — **the exact substitution A1 was accepted for four sections
earlier** (*"23 is a count of ACCEPTS ENTRIES rowed post-latch, not of product cells"*).

#### (b) FOUR OF THE NINE CAN CARRY NO ROW AT ALL.  The prelude forecloses them.

`DEVICE_ACCESS(crime)` runs an unconditional prelude before the width test:

```
:229   d->reg[CRIME_REV / 8]     = d->use_fb? 0xa1 : 0x11;
:231   d->reg[CRIME_CONTROL / 8] = CRIME_CONTROL_ENDIANESS;      /* 0x100 */
:233   d->reg[CRIME_INTSTAT / 8] = SOFTINT | HARDINT;
:264   d->reg[CRIME_MEM_BANK_CTRL0 / 8 + bank] = ...             /* 8 banks */
```

and a common tail that re-forces two more (`:414` HARDINT restored from the value preserved at `:213`,
`:415` INTSTAT recomputed).  **`CRIME_REV` is read NOWHERE else in the file** — verified: the only
occurrences of the symbol are `:229`, the case label and three comments; no tick function and no
interrupt path touches it.  So a value written to `+0x00` is consumed by nothing and overwritten by the
next access's prelude.

| entry | why it cannot carry a row |
|---|---|
| **1** `sd +0x00` | write to REV: prelude re-forces it; entry is NON-window so the REV arm's body is empty.  No channel at all. |
| **3** `sw +0x00` | same |
| **4** `lw +0x00` | 4R **high lane** (`relative_addr & 4 == 0` -> `odata = (int32_t)(odata >> 32)`), so it answers **0** — and a declined read answers 0 too. |
| **8** `lw +0x08` | identical: high lane of `0x100` answers **0**, and so does a decline. |
| **40** `sw +0x04` | low lane of the same forced REV slot; reaches `default:`, host log only.  **Already filed HOST-DIAGNOSTIC** by the probe's own contract at `:251-252`. |

**The probe already made this correction once, at the other offset.**
`crime_width_probe.py:132-133`: *"`devsig hi' reads 0 either way -- grok, codex, second closing pass,
correcting this sentence, which credited devsig hi"*, and again at `:308`: *"not by `devsig hi', whose
0 a refused read also returns."*

So the genuinely carriable members are **21, 32, 33, 46** — four, not nine.

#### (c) AND IT IS ALSO TOO SMALL: `buckets8.py` DROPS THE VALUE AXIS.

`buckets8.py:88` is `for n, (op, off, val) in enumerate(ACCEPTS, 1):` and `:89` is `key = (op, off)`.
**`val` is unpacked and never used again** — one occurrence in the file, the unpack.  `ACCEPTS` carries
five distinct CONTROL write values at `sw +0x08` and again at `sd +0x08`:

```
  ("sw", 0x08, 0x0201) ("sw", 0x08, 0x0001) ("sw", 0x08, 0) ("sw", 0x08, 0x0200) ("sw", 0x08, 0x0100)
  ("sd", 0x08, 0x0201) ("sd", 0x08, 0x0001) ("sd", 0x08, 0) ("sd", 0x08, 0x0200) ("sd", 0x08, 0x0100)
```

Ten entries collapse onto **two** keys (38 keys for 46 entries), and every one of the ten is reported
with the UNION of the five values' drivers.  The CONTROL arm **does** test the value —
`if (idata & CRIME_CONTROL_DOG_ENABLE)`, `if (idata & CRIME_CONTROL_HARD_RESET)`, `if (idata != 0)` —
so at this one label the value is a body-tested partition and merging it is wrong.

**Measured** (`b12.py`, key = `(op, off, val)` at `+0x08` only, `(op, off)` elsewhere — value-aware
exactly where the handler branches):

```
buckets8 (op,off)    PRE-BLIND  8   POST-BLIND  4   UNION  9   OBLIGATIONS 12
CONTROL-value-aware  PRE-BLIND 16   POST-BLIND 11   UNION 17   OBLIGATIONS 27
buckets8 SCORES COVERED BUT BLIND AT ITS OWN VALUE: PRE {10,12,13,14,16,17,43,44}  POST {12,13,14,16,17,43,44}
```

**Pushed harder, most of those shrink, and the residue is the interesting part.**  Applying the arm's
own branches: `0x0000` and `0x0100` clear to a zero residue and produce nothing (and `:327-328` of the
contract already files the ENDIANESS writes as "a strengthening, not a floor claim over value bits");
`0x0201` / `0x0001` leave residue `0x001` and are counted by `p acc ctl msg` (`:1256`, want 3).
**What is left is three cells, and one of them is the sharpest thing in this section.**
`crime_width_probe.py:1256-1257` — `p acc ctl msg`, want **3** — names the writes it counts, in its own
comment: *"the three accepted CONTROL writes (`0x01` sd, `0x0001` sw, `0x0201` sw) each print"*.

* **entry 14, `sd +0x08 = 0x0201` — UNCOVERED, and with a direct oracle.**  That row counts the **`sw`**
  form at `0x0201` and not its **`sd`** twin.  Same address, same value, other width, no row.  **That is
  the `#499` width-axis shape exactly** — a repair made at the width the mutant used with the symmetric
  cell left open — sitting inside the row that was added to close this very family.
* **entries 13 and 17, `sw`/`sd +0x08 = 0x0200` — the DOG_ENABLE MASK cell.**  The arm clears the bit,
  so the residue test sees 0 and nothing prints; the discriminating observation is the message count
  being **0** where `0x0201` gives 1, which needs a paired row rather than a bare one.

All three are driver-blind in both latch states and scored covered by `buckets8`.  **And the value-aware
derivation predicted the `sw`/`sd` split before I read `:1256`**: it reported entry 10 (`sw` 0x0201)
POST-covered by session 46 and entry 14 (`sd` 0x0201) POST-blind — which is exactly what that comment
says session 46 does.  Two roads, same cell.

> **NET: the nine becomes {21, 32, 33, 46} carriable + {13, 17} newly found — SIX — plus 40 on the
> host channel only, and {1, 3, 4, 8} disposed as EQUIVALENT rather than owed.**  Neither the count
> nor the membership of section 4b's list survives.

#### CONTROL: the value recovery was verified before any of this was believed

`b11.py` recovers each store's datum from the rt register the probe loads before the `put w`
(166 of 166 stores resolved, no silent misses).  The control: **session 40 matches 46 of 46
value-aware keys pre-latch and session 26 matches 46 of 46 post-latch** — which is exactly what
`buckets8.py`'s own docstring says those two sessions do.  A broken value recovery could not produce
46/46 against five distinct CONTROL values.  Separately, `enc(op, rs, rt, imm=0)` is called with
**zero** 4-argument forms in the probe, so every immediate is 0 and `off = base - CRIME` is sound —
a defect ruled out by checking rather than left unexamined.

---

### 1.2 — A11 IS ACCEPTED AND ITS REMEDY IS VACUOUS.  **Fold it into A12.**

A11: *"the shipped probe has NO direct value assertion for accepted CONTROL `lw +0x08`."*  True.
**But the value is 0 and a declined read also answers 0**, so the row A11 asks for is green under its
own mutant — the CHANNEL line's vacuity, in a row the packet has just committed to adding.

The non-vacuous form **already exists and is unshipped**, in the very script A12 says Parts A/B/C never
name.  `opus_close8_20260916/scripts/ctl4r.py` rows the cell as a **pair**:

```
    pre ctl4r    lw +0x08 BEFORE any refusal        the cell with the latch CLEAR      -> 0
    pre ctl0c    lw +0x0c BEFORE any refusal        the OTHER lane of the register     -> 0x100
    post ctl4r   lw +0x08 AFTER a refused lb +0x07  *** THE CELL UNDER TEST, latch SET ***
    post ctl0c   lw +0x0c after the refusal
    post ctl8r   ld +0x08 after the refusal         CONTROL is live post-latch, answers 0x100
```

> **A11 and A12 are one finding from two ends, and the packet accepted them as two.**  The row A11
> wants is `ctl4r`+`ctl0c`; shipping A11's half alone reintroduces at `+0x08` the vacuity the contract
> corrected at `+0x00`.

---

### 1.3 — A13 WAS ACCEPTED AND NOT APPLIED TO SECTION 5.  My own 6-of-6 is the metric it condemns.

A13: *"`MATCHED N, WRONG 0` certifies OUTCOME CLASSES, not row content."*  Accepted, corrected in the
legs — and then section 5 prints *"predictions matched 6 of 6"* without the same audit.  Applying it to
my own report:

| leg | predicted | measured | row content |
|---|---|---|---|
| `base` | 188/188 | 188/188 | exact (no rows) |
| `PC_imk4r` | 187/188, `gate line` | 187/188, `gate line` | exact — but a **re-run of an already-built binary** |
| `M1_gotolatch` | KILLED; **`sh08b run`** reds, `sh08b msg` may move | 178/188, **TEN rows** | **MISS.**  `sh08b run` ✓; `sh08b msg` **did not red** — `sb08 msg` did, a different session's row.  8 further rows unpredicted |
| `M2_ld278clr` | 188/188 ESCAPE | 188/188 | exact (no rows) |
| `M4_timeplain` | KILLED; `time lb/sb/lh/sh` | 184/188; `time lb, time sb, time lh, time sh` | **exact, row for row** |
| `M3_timelatch` | 188/188 ESCAPE | 188/188 | exact (no rows) |

> **6 of 6 on outcome class.  5 of 6 on row content.  And of the six, three are escapes (vacuously
> exact — there are no rows to name), one is a control re-run of a binary whose score was already
> known.  THE FORWARD ROW-CONTENT RECORD IS 1 OF 2.**

That is the honest number and it should replace "6 of 6" in the round record.  A metric that counts
escapes as prediction successes is the same shape as counting a seat that did not answer as agreement.

---

### 1.4 — "O1 SUPERSEDES D1 ENTIRELY" IS FALSE

D1 asks what the domain of `len` and the lane/window tuples actually is.  That is an **input** to the
decline arm's own axis, not a question the decline arm replaces.  The answer, which my O8 gave and
which I re-verified here:

`src/cpus/memory_rw.c:495-523` clamps `len = mem->devices[i].length - paddr` when an access runs past a
device's end.  `DEV_CRIME_LENGTH` is `0x280` = 640 = 8 x 80, and MIPS requires natural alignment, so
`0x280 - paddr` is always a multiple of the access width and **3/5/6/7 are unreachable**.  The decline
arm's reachable `len` domain is therefore `{1, 2}` — codex's reachability argument holds, **conditional
on a constant**.  Declaring D1 superseded discards the one premise that sizes the axis, and it is a
premise that a one-token edit to `DEV_CRIME_LENGTH` would falsify.

---

### 1.5 — A9's EXTENT IS UNDERSTATED, AND THE OMITTED PART CONTAINS TWO MORE `exit(1)`

A9 is accepted as "the omitted prelude at `229-235`".  The prelude runs to **`:273`**, and the omitted
remainder contains **two surviving host kills in the function the round is de-fatalising**:

```
:244   if (cpu->machine->physical_ram_in_mb > 1024) { fatal(...); exit(1); }
:255   if (cpu->machine->physical_ram_in_mb % mb_per_bank) { fatal(...); exit(1); }
```

Neither is guest-drivable — they gate on a machine-configuration value — which is exactly why my own O8
listed `physical_ram_in_mb` as a "collapsing axis" and said nothing about the two `exit(1)` it gates.
**The sketch rule exists so a reviewer sees every exit path in the enclosing function**, and a brief
that stops at `:235` hides two of the three in this one.

---

### 1.6 — A4's REJECTION IS RIGHT AND THE SENTENCE IT SAVED IS THE ONE TO CHALLENGE

There is no `CRIME_HARDINT` case — verified: the labels are `CRIME_REV`, `CRIME_CONTROL`,
`CRIME_INTSTAT`, `CRIME_INTMASK`, `CRIME_DOG`, `CRIME_TIME`, `default`.  Seven.  So the rejection is
correct on the question as put.

**But minimax was pointing at something real and it was closed off with the question.**  `CRIME_HARDINT`
*is* specially treated — outside the switch, in the common tail: `:213` preserves it on entry and `:414`
restores it, so **an accepted 8-byte write to `+0x28` is reverted inside the same access**.  That is a
label with distinguished behaviour implemented by the tail rather than by a case, and `ACCEPTS` contains
no `+0x28` entry at all.

**And "seven labels stands" is false as a SUPPRESSION axis**, which is what the decline arm needs
(§2):  `CRIME_DOG`'s arm is `break;` — null; `CRIME_CONTROL`'s arm is `if (writeflag == MEM_WRITE)` —
null on READ; `CRIME_INTSTAT` and `CRIME_INTMASK` **share one body** (`:383-386` fall through).  The
non-null (label, direction) count is **11**, not 14.

---

### 1.7 — A8 IS RIGHT AND UNDER-AMBITIOUS

`G_clr_imk4r` scores 187/188 and reds exactly **one** row, `gate line` (`:748`).  So the detector's
entire latch-CLEAR positive control rests on a single row, and the carrier's own "a mutant that will
not die" case 3 — the mis-cut row — would remove it silently.  Preserving one row is not the same as
having a control.  Entry **21** from 4b's own list (INTSTAT 4R, latch-CLEAR, seeded) would give a
second on a different channel, which is A7 doing double duty.

---

### 1.8 — WHAT SURVIVES

**A2, A3, A5, A7, A10, A12 survive**, and two are stronger than their dispositions say.

* **A2 verified by reading**: `:735` is `ld(A, "lw", CRIME + 0x18, "a0")` — INTMASK 4R — and the
  session's first refusal is `:741` `ld(A, "lb", CRIME + 0x08, "t1")`.  The 4R precedes the refusal, so
  the latch is CLEAR.  P4 is false, exactly as recorded.
* **A3 survives, and on its derivation rather than on its measurement.**  The `goto` -> `return 1`
  equivalence is sound because nothing between entry and tail writes HARDINT or SOFTINT on a declined
  access — I checked: the prelude touches `reg[0]`, `reg[1]`, `reg[2]` and `reg[65..72]` only — so the
  tail's restore and recompute are identities, and `memory_writemax64(..., odata = 0)` over a buffer
  `memory_rw.c` has already `memset` to zero is a second identity.  **The "measured 40/40" half is the
  weak half** — an equivalence asserted from "no row reddened" on a 40-row instrument is the
  will-not-die shape; the derivation is what carries it.
* **A7 IS THE BEST FINDING IN THE PACKET AND THE DISPOSITION UNDERSTATES IT.**  The packet says it is
  "sharper than my own criterion".  It is more than that: **A7 is the only finding that names the
  condition which makes its cell non-vacuous** — INTSTAT 4R reads the HIGH lane
  (`relative_addr & 4 == 0`), which is 0 unless `SOFTINT|HARDINT` is seeded above bit 31, and without
  the seed the row is `devsig hi` all over again.  Entries 4 and 8 needed exactly that treatment and
  did not get it.  **A7 is the template for the whole carrier set, not one cell of it.**

---

## 2. O1, ATTACKED BY ITS AUTHOR.  **THE DECLINE ARM IS NOT A 56-CELL PRODUCT.**

The packet has made O1 load-bearing for the whole repair.  It should not be, in the form I wrote it.

### 2.1 — WHAT I DID WRONG, NAMED PLAINLY

I wrote `{len 1,2} x {R,W} x {7 labels} x {latch}` = 56 **by analogy with the accept side**.  I did not
derive it from the decline arm.  That is the same move the panel has spent this whole round attacking
on the accept side — and worse, **the analogy's source is the very product A1 was accepted for
refuting.**  I copied a disputed enumeration into a new arm and multiplied it out.

### 2.2 — WHAT THE CODE SAYS.  `DEVICE_ACCESS(crime)`, `dev_sgi_ip32.c:296-320` and the tail at `:411-422`

```c
	} else {                                     /* len not in {4, 8} */
		if (!(d->warned & CRIME_W_LEN)) {
			d->warned |= CRIME_W_LEN;
			fatal("[ crime: unimplemented len=%i at 0x%x -- declined.  (once) ]\n",
			    (int) len, (int) relative_addr);
		}
		goto crime_declined;
	}
	switch (relative_addr) { ... }
 crime_declined:
	d->reg[CRIME_HARDINT / 8] = preserved_CRIME_HARDINT;
	d->reg[CRIME_INTSTAT / 8] = d->reg[CRIME_SOFTINT / 8] | d->reg[CRIME_HARDINT / 8];
	if (writeflag == MEM_READ)
		memory_writemax64(cpu, data, len, odata);       /* odata is still 0 */
	return 1;
```

**There is exactly ONE test in the arm: `d->warned & CRIME_W_LEN`.**  `warned` is `int warned;` at
`:88` with one bit defined, `CRIME_W_LEN (1 << 0)` at `:91`, read at `:314` and set at `:315` — two
uses in the file.  It is per-instance and device-wide: not per-label, not per-width.

**`relative_addr` is read at exactly one place — the `fatal()` format at `:316-317`.**  It flows into no
lvalue, selects no code, and is not re-tested after the join.  **`len` likewise** is printed and passed
as a width to `memory_writemax64`; the arm does not branch on it.

Applying the floor clauses as written:

* **DEPENDS-ON clause (1)**, predicates dominating the edited lines up to the function boundary:
  the `len == 8 / len == 4 / else` chain, and `!(d->warned & CRIME_W_LEN)`.
* **DEPENDS-ON clause (2)**, operand swaps drawn from fields the guarded body reads: `len`,
  `relative_addr`, `writeflag`, `odata`, SOFTINT/HARDINT.
* **The body-tested partition**: `{latch clear, latch set}` x `{R, W}` (the tail tests `writeflag`) x
  `{the decline len class as ONE cell}`.

> ### **FOUR CELLS, NOT FIFTY-SIX.  And the label is NOT a floor axis of the decline arm** — it fails
> ### both disjuncts of the 2026-09-09 `sgimtedepth4dead` label clause: the selector flows into no
> ### lvalue the body reads or writes, and the body does not re-test it after the join.  It is the
> ### `mode & COPY` shape, i.e. clause (e).

### 2.3 — SO WHY DOES `M3_timelatch` ESCAPE?  **THE RULES HAVE A GAP, AND THIS IS IT.**

A derivation that grades a measured 188/188 total escape as mere debt is producing the wrong answer on
the round's own best evidence.  The reason is structural, and it is worth more than the number:

> **A SUPPRESSING GUARD'S FLOOR AXES ARE THE AXES OF WHAT IT SUPPRESSES, NOT OF WHAT IT DOES.**
>
> Every floor clause enumerates from what the guarded body READS, WRITES or TESTS.  The `goto`'s entire
> semantic content is an **OMISSION** — it prevents a label-dispatched body from running — and an
> omission reads nothing, writes nothing and tests nothing.  DEPENDS-ON (1), DEPENDS-ON (2) and the
> label clause are all structurally blind to it.

The bounded repair to the rule, derivable by reading and diff-closed:

> **For a guard whose repair is a JUMP OVER a dispatch, the floor axes include the LABELS OF THE SKIPPED
> DISPATCH, restricted to labels whose arm has a non-null body for that access direction.**

That is finite (read off the switch), closed over the diff (it is the switch the `goto` skips), and it
would have predicted `M3_timelatch` before it was built.

### 2.4 — THE SUPPRESSION FACE, COUNTED FROM THE SWITCH RATHER THAN ASSUMED

| label | arm body | R | W |
|---|---|---|---|
| `CRIME_REV` 0x000 | pc-window redirect, no `writeflag` test | 1 (window only) | 1 (window only) |
| `CRIME_CONTROL` 0x008 | `if (writeflag == MEM_WRITE) {...}` | **0 — null on read** | 1 |
| `CRIME_INTSTAT` 0x010 | `crime_interrupt_reassert(d)` — **shared body**, `:383-386` falls through | 1 | 1 |
| `CRIME_INTMASK` 0x018 | same shared body | 1 | 1 |
| `CRIME_DOG` 0x030 | `break;` — **null** | 0 | 0 |
| `CRIME_TIME` 0x038 | `crime_update_crime_time(d)` | 1 | 1 |
| `default` | `debug(...)` only | 1* | 1* |

**11 non-null (label, direction) cells; 9 guest-observable** (`default`'s two are host-log only).
Not 14, and not 7.

**MY OWN O4 SAID "7 cells, 2 OPEN".  That is a count of LABELS presented as a count of CELLS** — the
same entries-vs-cells substitution I am criticising in §1.1, in my own pass-1 report.  The latch-SET
suppression face has 9 guest-observable cells, not 7.

### 2.5 — THE ASYMMETRY THAT ACTUALLY EXPLAINS THE ESCAPE, AND IT CHANGES WHAT THE REPAIR MUST BUILD

**The decline arm is asymmetric in the latch, and no product captures that.**

* **Latch CLEAR** — the `fatal()` fires and its TEXT carries both `len` and `relative_addr`.  So in the
  clear state the arm has a genuine `{len} x {dir} x {label}` observable, **and the probe already rows
  it**: `lb/lh/sb/sh said` for width and direction, and the per-label family at `:1044-1047` —
  `free rev said`, `free istat said`, `free imask said`, `free dog said`, `free time said`, plus
  `free 2r/1w/2w said` and `free revP said`, each a fresh single-refusal session.
* **Latch SET** — the announce does not fire.  What remains is the tail: a `writeflag` test and a
  `len`-wide store of a **constant zero**.  **There is no label channel and no width channel in the
  set state at all.**

> ### **SO `M3_timelatch` DOES NOT ESCAPE FOR WANT OF A ROW.  IT ESCAPES BECAUSE THE DECLINE ARM EMITS
> ### NOTHING AT (label, latch-SET) TO OBSERVE.**  Adding decline-side carriers there is impossible by
> ### construction.  **The rows that can catch it must observe the SUPPRESSED ARM'S SIDE EFFECT** — the
> ### clock advancing, the line re-asserting, the CPUs stopping — **in a session whose latch is already
> ### set.**  That is exactly what `M4_timeplain`'s four killed rows (`time lb/sb/lh/sh`) do in the
> ### CLEAR state, and the repair's job is to replay that shape after a prior refusal.

**This supersedes my own O2 framing as well.**  O2 said the K-form "is loud, not silent — the announce
is STOLEN".  True for the K-form.  For the latch-SET decline there is no announce to steal: the channel
does not exist rather than being pre-empted.

### 2.6 — THE ANSWER TO THE PACKET'S QUESTION

> *"Is O1 right that the decline arm is a SECOND 56-cell product, or is it smaller?"*

**Smaller, and not a product.**  Its own floor is `{latch} x {R,W}` = 4 cells with the `len` domain
`{1,2}` disclosed.  Its suppression face is 11 (label, direction) cells x `{latch}` = 22, of which 18
are guest-observable — and that face is **not covered by any existing floor clause**, which is the
finding.  **112 is wrong and should not be written into the round record.**  O1's CONCLUSION — that
Parts A/B/C are accept-side and cannot reach this — stands, on the warrant in §2.3 rather than on a
product.

---

## 3. THE NINE-ENTRY LIST AND `buckets8.py`'s BLINDNESS TEST

### 3.1 — IS THE NINE EVEN WELL-FORMED, GIVEN O7?

**The arithmetic is well-formed; the list is not.**  `{1,3,8,21,32,33,40,46} u {1,3,4,8}` is nine, and
`{1,3,8}` is correctly identified as the both-states intersection.  What is not well-formed:

1. **it counts ENTRIES and is spent as ROWS** (12 obligations, §1.1a);
2. **four members cannot carry a row at all** (§1.1b);
3. **it is computed with the value axis dropped** (§1.1c).

**And O7's objection and this one are DIFFERENT and both live.**  O7 says the *bucket* counts (23/8/
10/5) cannot be audited because 8 of 46 members are unlisted.  §1.1 says the *driver* derivation is
wrong.  They do not overlap, and the second was not addressed by the rerun.

> ### **THE SHARPER POINT, AND IT UNDOES 4b's CLAIM TO HAVE ANSWERED K2: `buckets8.py` DOES NOT
> ### RE-DERIVE THE BUCKETS.  IT CANNOT.**
>
> There is no machine-readable bucket assignment anywhere in the probe — the 23/8/10/5 live only in
> prose at `crime_width_probe.py:235-259`, and `buckets8.py` reads `ACCEPTS` and nothing else.  It
> derives **driver lists**, which is a different quantity.  kimi's K2 asked for the buckets to be
> re-derived; the tool answers a neighbouring question; the packet reports K2 as done.
>
> **So K2 is still open, and O7's 8-of-46 is untouched by `BUCKETS8_rerun.out`.**

**So: nine is neither a floor nor a ceiling.**  It is simultaneously too large (4 uncarriable members)
and too small (the value axis, and the whole decline arm).  Calling it "complete" is the error; calling
it a floor, as O7 did, is also not right, because a floor cannot contain members that are impossible.

### 3.2 — IS THE BLINDNESS TEST SUFFICIENT?  **NO — AND IT IS A CHECK THAT CANNOT FAIL.**

`buckets8.py`'s test is `p_other = [s for s in p if s not in BLIND]` where `BLIND = {26, 40}` is a
**hardcoded two-element set**, hand-derived.  The test asks *"is the driver one of the two sessions I
already knew were blind?"*  It consults **no oracle information whatsoever**.

**And it demonstrably had the oracle information and threw it away.**  The recorder collects each
session's row list into `PEND` and stores it at `S[i][1]` (lines 30, 34, 52, 53, 64 — all writes).
**`S[i][1]` is never read.**  The analysis loop uses `S[i][0]`, the access list, only.

> That is this project's own check-that-cannot-fail shape, exactly: **a cheap substitute (driver
> identity) standing in for an expensive question (does any row move when this cell changes), which
> returns a plausible-looking answer in both states.**  Ask of it what the carrier says to ask: *what
> does it print when the thing is FALSE?*  A third blind session drives a cell -> it prints the session
> number in the "other drivers" column and the cell reads COVERED.

**DOES SUCH A SESSION EXIST?  YES — SESSION 19, AT ENTRY 21, AND IT IS THE PACKET'S OWN BEST CELL.**

`buckets8` reports entry 21 (`lw +0x10`, INTSTAT 4R) as **PRE-BLIND only**, because its POST drivers are
`[19, 26]` and 19 is not in the hardcoded set.  Session 19's rows are:

```
  istat pre / istat lb / istat sb / istat lh / istat sh    the interrupt LINE state (clear/set)
  istat ctl                                                the line after a control access
  istat once / istat said                                  announce COUNTS
  istat lb v0 / istat lh v0                                the REFUSED read's answer (0x0)
```

**Not one of them reads back the value the accepted `lw +0x10` returns.**  The line-state rows observe
`crime_interrupt_reassert()`; the `v0` rows observe the *refused* accesses.  So session 19 drives the
cell and has no oracle for that channel — **entry 21 is blind POST-latch as well as PRE, and
`buckets8` scores the POST half covered.**

That is precisely the state the question hypothesised, and it lands on **A7's cell** — the finding the
packet singled out as sharper than its own criterion.  A7 asked for the latch-CLEAR half seeded; the
same argument gives the SET half, and `buckets8` hid it.

**A second, independent instance is the VALUE axis:** sessions 2 and 3 drive `sw +0x08` with `0x800`
and `0x01` (`crime_width_probe.py:551`, `:556`), so they appear as sighted "other" drivers for **all
five** `sw +0x08` entries — including `0x0200`, which neither ever writes.

### 3.3 — AND THE THIRD STATE THE TEST CANNOT SEE, WHICH IS THE ONE THAT MATTERS MOST

A cell can be in **three** states and `buckets8` renders two of them identically:

| state | correct disposition | buckets8 |
|---|---|---|
| no session with an oracle drives it | **OWES A CARRIER** | flags it |
| **no oracle is POSSIBLE — the channel does not exist** | **EQUIVALENT, owes nothing** | flags it identically |
| driven by a sighted session **at a different value** | owes a carrier iff the value is body-tested and has a channel | **scores it covered** |

Entries 1, 3, 4, 8 and 40 are in row 2 and were flagged as row 1.  Entries 13 and 17 are in row 3 and
were scored covered.  **The nine-entry list is the union of one real class and one impossible one, with
a third class missing.**

### 3.4 — AND NO STATIC SUCCESSOR CAN FIX IT.  This is the honest limit.

*"Has an oracle for this channel"* is the CHANNEL line's question — *name the mutant this row kills and
the observable that differs under it* — and the CHANNEL line is settled by **building the mutant**.  A
static tool can derive who DRIVES a cell; it cannot derive whether anything MOVES.

> **So the right successor to `buckets8.py` is not a better classifier.  It is: use the driver
> derivation to PROPOSE candidate cells, then settle each one the way `M2_ld278clr` settled entry 46 —
> with a mutant.**  Entry 46 is the proof that the loop closes: the deriver reached it by reading
> sessions, I reached it by building a mutant, and both landed on the same cell.  That agreement is
> what licenses the method, not the tool's output on its own.

**A caution from my own apparatus, recorded because it is the same failure one level up.**  I built two
classifiers before I trusted either, and **both keyed on a correlate rather than on what defines the
class** — the carrier's `staticlatchscope` lesson, met twice in one hour:

* `b9.py` treated string `want` values as non-oracles.  In this probe the DEVICE-VALUE rows are the hex
  **string** wants and the announce counts are the **int** wants — inverted.  It reported 49 of 50
  sessions blind, a number so large it was obviously an artifact.
* `b9.py` also attributed rows to the wrong session: `row()` fires **after** `session()` returns, so
  `PEND` at the moment session *i* is called holds session *i-1*'s rows.  Rows of session *i* are at
  `S[i+1][1]` — verified against the packet's own naming (`S[27][1]` is `rearm once`/`rearm surv`, which
  the packet calls session 26's).  **This is the row-to-session off-by-one my own O9 recorded in pass 1,
  reproduced in the tool written to audit it.**  `buckets8.py` is unaffected, because it never reads the
  row list at all.
* `b10.py`, with both fixed, still over-classified: it counted `small`/`large` as liveness tokens when
  they are **magnitude oracles on the TIME channel**, and it called sessions 2 and 3 blind when
  `sw08 halts` (the guest stops) and `sw08 msg ctl` (the arm's message) are genuine CONTROL-arm oracles.

**Only the VALUE-axis finding survived all three rounds of self-correction**, because it does not rest
on classifying oracles at all — it rests on `val` being unpacked at `:88` and never used, which is a
fact about the source.  I am reporting it and discarding the rest.

---

## 4. THE MEASUREMENT THIS PASS ADDED — O4's REV CELL IS NO LONGER DERIVED

O4 asserted, **without a run**, that the decline x latch-SET axis has two open cells, REV and TIME.
TIME was measured (`M3_timelatch`, 188/188).  **REV was a derivation, and a derivation that has been
right once is still a derivation.**  Two mutants settle it.

Predictions written to `opus_adj_work/PREDICT_adj.md` at **00:52:24**, builds at **00:53**, probe logs
complete at **01:2x** — the mtime ordering is the order discriminator.

```
base           188/188   (opus_pass1_work/logs/probe_base.raw, CRIMEP_DONE)   harness validated
M5_revlatch    188/188   --                        *** TOTAL ESCAPE -- O4's REV cell, MEASURED
M6_istlatch    185/188   istat sb, istat lh, istat sh   NEGATIVE CONTROL -- KILLED
```

Both logs end `CRIMEP_DONE` (`opus_adj_work/logs/probe_M5_revlatch.raw`, `probe_M6_istlatch.raw`;
scores in `logs/tableadj.out`, driver `KILLADJ_DONE`).  The two mutants are **byte-identical in shape**
— `M3_timelatch` with the label swapped — generated by one `latch_label()` helper so the edits cannot
drift apart.

### WHY THE CONTROL WAS NOT OPTIONAL

Without `M6`, an `M5` escape is ambiguous between

* **(a)** REV is an open cell of the label x latch face — the claim, and
* **(b)** a single-label latch-conditional `goto` is invisible to this detector **per se**, in which
  case `M3_timelatch` is a far larger finding than the round has recorded and the cell count is beside
  the point.

**(b) is refuted: the identical edit at INTSTAT reds three rows.**  The detector can see this shape.
It cannot see it at REV.

### AND THE CONTROL'S OWN ROW SET CONFIRMS THE MECHANISM

`M6` reds `istat sb`, `istat lh`, `istat sh` — **and not `istat lb`.**  That is exactly what the edit
predicts: the `goto` moves inside the latch block, so a session's **FIRST** refusal still declines
correctly, and in session 19 (`crime_width_probe.py`, the `istat *` block) the `lb` is that first
refusal while `sb`/`lh`/`sh` follow it.  The mutant is invisible to the row that measures it first and
visible to the three that measure it after.  **The kill pattern is the latch asymmetry itself.**

> ### **SO THE DECLINE x LATCH-SET FACE HAS TWO MEASURED OPEN CELLS, NOT ONE DERIVED AND ONE MEASURED.
> ### That is a second consecutive instance of one class, which is what the class-closure rule is FOR —
> ### and it converts §1's mandate from "inherited from the framing" to "earned on the decline side as
> ### well as the accept side."**

Closing TIME alone would be the `#499` shape precisely: repair at the address the mutant used, the
symmetric cell left open for the next pass.

### PREDICTION AUDIT, under A13's own criterion (§1.3)

| leg | predicted | measured | row content |
|---|---|---|---|
| `M5_revlatch` | 188/188 ESCAPE | 188/188 | exact — no rows to name |
| `M6_istlatch` | KILLED | 185/188 | **no row-level prediction was made**, so there is nothing to score |

**2 of 2 on outcome class; one leg carries no row claim and I am not counting it as a row-content
success.**  I should have predicted M6's rows — the `first-refusal-declines` reasoning above was
available before the build and would have named `istat lb` as the one that stays green.  Recording the
miss rather than rounding it up is the whole point of §1.3.

### FOOTPRINT

Clean.  No project tree written but this round's own artifacts dir.  Clone `/tmp/gxopus_r14`:
`.MUTANT` absent, source `cmp`-clean against `GXEMUL-SEC`, binary `-nt` source, `restored` binary
byte-identical to `base`.  All four fork copies of `dev_sgi_ip32.c` still md5 `8c1d1545`.  My analysis
tools (`b9`/`b10`/`b11`/`b12`) ran read-only out of the session scratchpad and wrote nothing anywhere
else.

---

## 5. §1 — IS THE MANDATE RIGHT, OR DID NINE SEATS INHERIT IT FROM THE FRAMING?

You were right to ask, and the answer is **partly inherited**.

The class-closure rule fires when **two consecutive passes find breaches of ONE class**.  Check whether
this chain has that:

* `t4clear.py` killing the TIME cell at 3/5 while INTSTAT scores 5/5, and `M2_ld278clr` (entry 46) — are
  **the same class**: *an accept cell whose only driver is an oracle-less session*.  Two instances, so
  the class-closure demand is earned **for the accept side**, and the members are enumerable
  (§1.1's corrected list).
* `M3_timelatch` is **a different class** — the suppression face of the decline arm.  When I drafted
  this section it was a *first* instance, and under the letter of the rule a first instance is not yet a
  closure trigger.  **`M5_revlatch` (§4) is the second, measured.**

> **So the mandate is right on the accept side on two instances, and right on the DECLINE side on two
> instances as well — TIME measured in pass 1, REV measured in this pass.**  It is not inherited from
> the framing; it is earned twice over, and the second half was not available to the nine seats because
> nobody had built the mutant.
>
> Closing TIME alone would be the `#499` shape — repair at the address the mutant used, symmetric cell
> left open for the next pass — and §2.4 says how many cells the face has, so the enumeration the
> closing pass must VERIFY is available rather than hunted.

**And the unanimity in §1 is worth exactly what the carrier says it is worth: nothing, on its own.**
Every seat that upheld the mandate was reasoning from the packet's framing of it.  What makes it
defensible is the two-instance count above, which is checkable, not the count of seats.

---

## 6. WHAT REPAIR 14 SHOULD ACTUALLY BUILD — the net of all of the above

Not nine carriers.  Three things:

1. **FOUR accept-side carriers from the nine, not nine — and entry 21 needs TWO**: entry **21**
   (INTSTAT 4R, **with `SOFTINT|HARDINT` seeded above bit 31** — A7's condition is what makes it
   non-vacuous — in **both** latch states, because §3.2 shows the POST half is blind too), **32/33**
   (TIME 4W/4R, via the clock-advance channel, the GAPPED shape — not a readback), **46**
   (`ld +0x278`, the one cell of the nine a plain value row can carry).
2. **THREE newly-derived carriers at CONTROL**: entry **14** (`sd +0x08 = 0x0201` — the `sd` twin of
   the `sw` cell `p acc ctl msg` already counts; direct oracle, the message count) and entries
   **13/17** (`sw`/`sd +0x08 = 0x0200`, the DOG_ENABLE mask — oracle is the count being **0** where
   `0x0201` gives 1, so it needs the pair).
3. **TWO decline-side carriers that observe the SUPPRESSED ARM, not the decline arm** — and both cells
   are now MEASURED open, not derived: replay the `time lb/sb/lh/sh` shape **after a prior refusal in
   the same session** (`M3_timelatch`), and the REV-window equivalent (`M5_revlatch`).  §2.5 is why no
   decline-side row can work here, and §4's `M6` control is why these two are the right cells.

**Dispose, do not carry**: entries **1, 3, 4, 8** as EQUIVALENT with the derivation written down
(the prelude at `:229`/`:231` re-forces the register and the 4R high lane answers 0 either way), and
**40** as HOST-DIAGNOSTIC, which the contract already says at `:251-252`.

**Fold A11 into A12**: the CONTROL 4R row is the `ctl4r`+`ctl0c` **pair** from
`opus_close8_20260916/scripts/ctl4r.py`, never `lw +0x08` alone.

**And write the EQUIVALENCE derivations into the contract**, because that is what converts the next
escape from "another breach" into "outside the contract, as stated" — which a cell-by-cell chain can
never reach.

---

## 7. THINGS I FOUND WHILE VERIFYING SOMETHING ELSE

* **A stale citation, and it is not the one O8 reported.**  O8 flagged `OUTSTANDING_BUGS.md:5574`
  citing `dev_sgi_ip32.c:698` where the target is now `:728`.  Separately, `ACCEPTS` is consumed at only
  **two** call sites (`:892` and `:1069`), both inside the two oracle-less sessions — so the enumeration
  that the whole bucket analysis rests on is driven in full **only** by sessions that can observe none of
  it.  That is the structural reason `buckets8.py` had to ask its question at all, and it is worth
  stating in the contract rather than leaving as a property of the code.
* **`ACCEPTS` contains no `CRIME_CONTROL` HARD_RESET (`0x800`) write**, although the arm branches on
  that bit and the effect is the loudest one in the device.  It cannot be in `ACCEPTS`: an accepted
  HARD_RESET write terminates its session — my own O8 rider.  So it is covered only by session 2
  (`sw08 halts`) as a one-off, and the gate session drives it only as a **refused** halfword
  (`:743`, `sh +0x08 = 0x0800`), which is what `gate run` observes under `M1_gotolatch`.
* **The `warned` bitfield collision hazard is currently nil here.**  `#490`'s lesson is *"who else writes
  this field, and can they set my bit?"*  In `dev_sgi_ip32.c` the answer is nobody: `CRIME_W_LEN` is the
  only bit defined and `d->warned` has exactly two uses.  Worth recording as a CHECKED-and-clean rather
  than left unexamined — it will stop being true the moment a second latch lands in this device.

* **§1's OWN EVIDENCE IS UNDERSTATED, and this is the one place a disposition is too WEAK rather than
  too strong.**  §1 cites `t4clear.py` as *"kills the TIME cell at 3/5 and scores the INTSTAT cell at
  5/5"* — two measurements.  The artifact set (`opus_close8_20260916/logs2/`, every file ending
  `T4CLEAR_DONE`) holds six:

  ```
      t4clear_base.out             5/5     baseline
      t4clear_G_glm_tim4clear.out  3/5     TIME        -- the only KILL
      t4clear_G_clr_ist4r.out      5/5     INTSTAT     -- ESCAPE
      t4clear_G_clr_imk4r.out      5/5     INTMASK     -- ESCAPE
      t4clear_G_clr_ctl4r.out      5/5     CONTROL     -- ESCAPE
      t4clear_C_ctl4r.out          5/5     CONTROL     -- ESCAPE
  ```

  **`t4clear.py` kills ONE of five mutants and escapes FOUR**, across three different labels.  Quoting
  two of the six makes the mandate look like a one-cell gap when the measurement says the instrument is
  label-blind in general — which is independent support for §2.4's suppression face, arrived at from an
  artifact rather than from the handler.
