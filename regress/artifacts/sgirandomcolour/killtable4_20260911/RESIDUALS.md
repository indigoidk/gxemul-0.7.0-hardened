# `#519` pass-4 residuals -- harvested from the read-only seats fired alongside kill table 4

*** EVERY ITEM BELOW IS A **READING**, NOT A MEASUREMENT. *** No mutant here was built and no
probe was run against it: the kill table held the clone and the seats were constrained read-only
so they could not contend with its wall-clock-sensitive sessions. Each names the mutant that
would settle it. Treat the scores as PREDICTIONS until a table says otherwise -- this project has
recorded a prediction written into a measured column as its own defect class.

---

## R1. THE SIBLING ARM HAS THE SAME BLIND SPOT, AND A WIDER ONE (candidate round, HIGH)

`horrible_getputpixel()`'s OTHER de-fatalised arm -- the `switch (tlb_mode)` `default:` at
`src/devices/dev_sgi_re.c:272-308`, shipped as `#504` (`sgirandompixel`) -- is guarded by
`regress/sgi_re_randompixel_probe.py`, **8 rows**, gate-wired at `regress/gate_arm.sh:1283`.

Read against `draw_primitive()`, that detector drives the arm at **one value of every free input
except `y`**: `mode` is 0x1620 tree-wide, `tile_nr`/`tile_nr_x`/`tile_nr_y` are all 0, `linear` is
always 1, `bufdepth` 4, `color_mode` RGBA, and `x` is 0x40 in the value-oracled rows.

**The pass-2 escape transfers verbatim:**

```c
default:  ... ;  if (tile_nr) *color = random();  return;
```

predicted **8/8 -- a clean sweep** -- restoring the `#504` defect for every pixel outside tile 0.
At bufdepth 4 that is the same 1.25%/98.75% severity inversion measured here for `M30`.

Three more predicted sweeps on the same arm, each a different axis:
`if (!linear) *color = random();` (tlb_mode 3 is reachable and never driven);
`if (tlb_mode != 5) *color = random();` (exempts the one documented label the round's warrant
rests on); `if (x != 0x40) *color = random();`.
And a latch-axis one, `if (!(d->warned & SGIRE_W_BADMODE) || tlb_mode != 5) {`, which restores a
guest-drivable per-pixel `fatal()` flood -- `fatal()` has no `-q` early-out, so a 2048x2048 XFER
rectangle is millions of unsuppressable lines.

**TWO CAUTIONS THE SEAT ESTABLISHED BY READING, AND BOTH MATTER BEFORE ANYONE BUILDS A TABLE:**

* **The `return;` at `:308` is DEAD.** `tileptr` is initialised 0 at `:250`, the default arm never
  assigns it, and `:312`'s `if (!(tileptr & 0x80000000)) return;` catches the fall-through with
  identical effect. So `return;` -> `if (X) return;` is an **EQUIVALENT mutant** -- it will come
  back 8/8 and be misread as detector blindness when the target is simply dead. The real repair
  is the DELETION of `*color = random();`, so the clause-(d) mutant re-introduces it under a
  predicate.
* **`if (put) *color = random();` is ALSO equivalent**, because on the PUT side `*color` is
  loop-local and dead after the store. The `put` axis is live for the LATCH mutant only. Building
  the value form keyed on `put`, reading 8/8, and concluding "blind" would be a wrong result.

Blast radius is bounded and worth knowing: the arm is reachable only from `draw_primitive()`,
where `color`/`oldcolor` are loop-local. `do_mte_transfer()` cannot reach it (`:1504` exits for
`src > MTE_TLB_C`) -- which matters, because that caller passes a FUNCTION-SCOPED `&bg`, so had it
been reachable the corruption would have persisted across a whole transfer.

## R2. THE GET-SIDE COLOUR `default:` HAS NO DETECTOR AT ALL (candidate, MEDIUM)

`dev_sgi_re.c:416-418`. `#519` explicitly scoped it out ("the GET default below is untouched").
It **accepts** a raw 32-bit read and carries an **unlatched, per-pixel, guest-drivable `fatal()`**
-- the `floodclass` shape -- reachable by the same twelve type nibbles.

Measured by grep, and this is the part worth acting on: `"get: color mode"` appears **0 times** in
`OUTSTANDING_BUGS.md`, `CHANGELOG.md` and `ledger.json`. Its buffer-contents half is filed as
`sgirebufuninit`; **the missing latch is filed nowhere.** It is the direct sibling-parity
counterpart of the arm `#519` just latched.

## R3. RECORDS THAT GO STALE THE MOMENT TABLE 4 LANDS

* `OUTSTANDING_BUGS.md:18751` -- headline reads `#519 DOES NOT CLOSE. PASS 2 MEASURED A FLOOR
  BREACH`. Overtaken: table 4 kills all six. **It cannot be corrected until the table finishes
  and its RESTORE leg closes** -- correcting it earlier would be a claim ahead of its evidence.
* `ledger.json` `sgirandomcolour.witness` calls a **19-row** instrument "the final instrument on
  the final source". It is 77 rows and two tables later.
* `sgirelatchenum` (OUTSTANDING_BUGS) says the latch enum holds "seven today, nine after #499 and
  #500". `#519` adds the 13th `1 << N` enumerator.
* The 2026-09-11 pass-2 panel is cited only at a project-root `_scratchpad/` path -- volatile --
  and its answering seats appear in **no ledger entry**, which is the unread-review shape section
  G exists to catch. Copy the panel dir under `regress/artifacts/sgirandomcolour/` BEFORE any
  durable record cites it.
* `tools/pipeline/check_probe_wiring.py`'s MANIFEST has no entry for
  `regress/sgi_re_colourdefault_probe.py`, nor for the scripts in `killtable3_20260910/`,
  `killtable4_20260911/` or `pass2_20260911/`. Unaddressed, the wiring gate reds on commit.

## R4. GATE WIRING IS OWED, NOT EXEMPT

`gate_arm.sh:1283` already runs the sibling `sgi_re_randompixel_probe.py` on `$PMAX`, with its
block at `:1267`. So the "no gate runs this family" warrant that justified recent exemptions does
not apply. Wire this probe beside its sibling and **pin 77 rows, not 59**. Corrected in this
directory's README, which first stated the absence in a way that read as an exemption.

---

## R5. FOUR ONE-TERM MUTANTS PREDICTED TO SWEEP THE 77-ROW INSTRUMENT (from the closure audit)

A read-only seat audited the pass-4 block against the source and found that its completeness
claim overreached. **DERIVED, NOT MEASURED — no table has run these.** Each is reachable by one
ordinary guest store. The probe's contract now discloses them; this is the filing it cites.

| mutant | why it escapes every driven cell | reachable by |
|---|---|---|
| `if (ok \|\| (tileptr & 0xfff00000))` | driven tileptr is only {0x1,0x2,0x3,0x4,0x5}0000 | `re_tlb_a[0] = 0x8010` |
| `if (ok \|\| (mode & 1))` | every mode word any row drives has low nibble 0; bits 0-3 and 13-31 are read by nothing in the function | `DE_MODE_DST = 0x12f1` |
| `if (ok \|\| (x & 1))` | driven x is {0, 4, 132} -- all even | vertex x = 1 |
| `if (ok \|\| (y & 2))` | driven masked y is {0, 1} | vertex y = 2 |

plus a mixed conjunction, `if (ok || (tile_nr_x && ofs == 0))`, true only at (x=128, y=0) --
a cell the pass-4 block explicitly considered and then did not drive.

**THE DISPOSITIONS ARE NOT ALL THE SAME, and the difference is the whole point:**

* **`tileptr` (the TLB array CONTENTS) is FLOOR-SHAPED and is the real gap.** The value flows
  into the store's ADDRESS operand, so by the 2026-09-09 flow test it is a floor axis exactly as
  `tlb_mode` is. The pass-4 enumeration NAMED it (`tileptr <- tlb_mode, tile_nr, array`) and then
  dropped it from its conclusion. Closing it is cheap -- one cell whose tile entry is programmed
  outside the 0x8001..0x8005 range -- and it is OWED.
* **`mode & 1` is clause-(e) debt by the same test that saved M28**: the unread bits flow into
  NOTHING the guarded body reads. That is the `mode & COPY` shape the ruling names explicitly.
* **`x & 1` and `y & 2` are within-class value slices.** They are not closable by any finite row
  set -- for any cells you drive, a predicate false on exactly those cells exists -- which is
  why the contract now separates EXHAUSTED axes (tlb_mode, bufdepth, color_mode) from SAMPLED
  ones (x, y, *color, tileptr, mode) instead of calling all of them "closed".

**AND THE UNRESOLVED TENSION, which is an adjudication question and not mine to settle:** this
round graded the tile-index and tiled-origin escapes as FLOOR breaches, and those are also value
slices of a store input. If value slices are floor, these are live floor breaches; if they are
debt, the earlier grading was wrong. **The round currently asserts the first and ships the
second.** It needs ONE ruling, not two. Recorded here rather than decided.

## R6. SMALLER ITEMS FROM THE SAME AUDIT, each verified before filing

* The pass-4 sessions are the two longest in the probe (~275 and ~200 debugger commands) and
  index their readbacks POSITIONALLY with no `MARK1`/`MARK2` split, unlike the tiled loop. A
  dropped response shifts every later cell. It fails LOUDLY (`absent`), so it is a false-red not
  a false-green -- but the row that reds is not the row that lost its meaning. One `t9` marker
  echo between the accept and decline phases would make each session self-locating.
* `xy anchor t0` may be a strict-subset row by the same criterion that deleted the four
  `ann cum` rows: any mutant redirecting C3 onto tile 0 reds `xy acc c3` first. Worth checking
  against the full table rather than deleting on a reading.
* Disclosure (iv) still cites `killtable3_20260910/PRETABLE.out` for "every cell", but that
  artifact predates the 14 new cells. Table 4 supplies them; the citation should be re-pointed.

**One audit claim was checked and is WRONG:** the seat reported that table 3's latch mutants
(M4/M5/M6/M7) "were not carried forward", leaving `xy ann` and `nib ann` unmeasurable. They ARE
in table 4's regression group. And `M38_acceptannounce` has since reddened BOTH new announce rows
along with all four `silent` rows and no `ann1` row -- so those rows carry measured kills.
