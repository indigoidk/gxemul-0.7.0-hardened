# Opus 5 measuring seat -- `sgimtedepth4dead` (#509, 2956c7e) -- rule question 7g-1

`OPUS_SEAT_ALIVE_20260909_7g1`

Line 3 of `regress/sgi_mte_fill_probe.py`, verbatim:

    #  sgimtedepth4dead -- RUNG-3 WITNESS: `if (depth == 4)' is dead, so MTE never selects RGBA.

---

## VERDICT LINE

**MEASURED TOTAL ESCAPE, TWICE.** `M_tlbA` (`depth == 32 && dst_tlb == MTE_TLB_A`) scores
**14/14** -- `killtable3_20260909/M_tlbA.raw` -- against the shipped detector's base **14/14**
(`killtable3_20260909/BASE.raw`), and the optional `M_tlbAB` (`&& dst_tlb != MTE_TLB_C`) also
scores **14/14** (`killtable3_20260909/M_tlbAB.raw`). Not merely equal scores: `diff` against
`BASE.raw` is EMPTY but for the label on line 1 -- every row returned the identical `got`.
**And the exempted cells are REACHABLE with the defect live in them, measured at rung 3**
(`reach_M_tlbA.raw`: A=RGBA, B=CI, C=CI; base `reach_BASE.raw`: A=RGBA, B=RGBA, C=RGBA).
**My answer to 7g-1 is FLOOR, not clause-(e) debt** -- `switch (dst_tlb)` is a dominating
predicate of the edited line inside the enclosing function, `if (X)` to `if (X && Y)` on a
dominating predicate is clause (d)'s canonical form, and the pass-11 floor sentence names
dominating predicates crossed with jointly-reachable repair-path state. **The shipped FIX is
correct at all three labels and is not in question; the shipped DETECTOR is blind at two of
three.** Closure costs **two rows**, already measured. Restore verified both parts, sentinel
cleared, no project tree mutated.

---

## TASK 1 -- THE MEASUREMENT

Full table, scores, binary MD5s and the restore record: `killtable3_20260909/TABLE.txt`.

| binary | edit at the `#509` line | detector | log |
|---|---|---|---|
| BASE | none (the shipped fix) | **14/14** | `killtable3_20260909/BASE.raw` |
| `M_tlbA` | `depth == 32 && dst_tlb == MTE_TLB_A` | **14/14** | `killtable3_20260909/M_tlbA.raw` |
| `M_tlbAB` | `depth == 32 && dst_tlb != MTE_TLB_C` | **14/14** | `killtable3_20260909/M_tlbAB.raw` |

Reachability control (`tlb_reach_control.py`, a CONTROL and not a proposed row set), same tiled
32-bit fill driven at each label, oracle `dest[0]` -- `0x11` = RGBA arm, `0x44` = CI arm:

| binary | MTE_TLB_A | MTE_TLB_B | MTE_TLB_C | log |
|---|---|---|---|---|
| BASE | RGBA | RGBA | RGBA | `reach_BASE.raw` |
| `M_tlbA` | RGBA | **CI** | **CI** | `reach_M_tlbA.raw` |
| `M_tlbAB` | RGBA | RGBA | **CI** | `reach_M_tlbAB.raw` |

The control separates all three binaries; the shipped detector separates none. That contrast is
the finding, and it is why the control was built: a blindness claim needs a positive control that
the difference is *there to be seen*, or it cannot be told from "the mutant does nothing".

Method, each item because this project has been burned by each: scratch clone `/tmp/gxopus7g1`
(`cp -a` of `build/`); **baseline NAMED** as `GXEMUL-SEC/src/devices/dev_sgi_re.c` at HEAD
`b4d4177` and `cmp`-verified clean before mutant 1 (md5 `8479c1ea...`); `.MUTANT` sentinel dropped
BEFORE each mutation and restored FROM SEC, never from a local backup; `rm -f
src/devices/dev_sgi_re.o` then `make -j4`, with `MAKE_RC` **not** trusted alone and
`[ gxemul -nt src/devices/dev_sgi_re.c ]` checked every time; each mutation verified as a
one-line edit by `diff` against SEC (exactly one `<` and one `>`); the probe FROZEN by copy
(md5 `dcada999...`) so all three runs share one instrument; no `set -e` anywhere, because the
probe exits 1 on a red row and a driver ending in a comparison is how a measurement silently
does not happen; every preserved log verified by its completion sentinel (`MTEFILL_DONE` /
`TLBREACH_DONE`) rather than by existence. **`build/` was never mutated and holds no sentinel.**

Restore: part 1 `cmp` CLEAN vs SEC, part 2 `[ binary -nt source ]` OK, and the rebuilt base
binary reproduced the stage-B md5 `e113ca7193a91b8953c4c10f37417ab2` bit-for-bit -- so the
restore is confirmed by the artifact, not only by the file compare. Sentinel then removed.

### What this settles, and what it does not

* **Settled: BLINDNESS.** The shipped 14-row detector cannot observe the `dst_tlb` label at all.
* **Settled: REACHABILITY of the exempted cells**, by an ordinary guest on an unmodified in-tree
  machine description -- the writer of `re_tlb_b`/`re_tlb_c` is the exact mirror of the TLB_A arm
  the probe already drives, and `horrible_getputpixel`'s `case 0/1/2` are the same code against a
  different array. This is the fact the floor rule keys on ("a mutant exempting a single cell
  whose reachability is MEASURED is a floor breach") and no prior artifact held it.
* **Settled: the shipped FIX is not defective.** BASE is RGBA at all three labels.
* **NOT settled, and it is the rule question itself:** whether that blindness is a FLOOR BREACH or
  DISCLOSED DEBT. A measurement cannot answer that; it is an adjudication, and mine is below.
* **NOT settled: whether any real driver travels B or C.** Reachability is rung 3; "is travelled"
  is rung 4 and I did not attempt it. The floor rule keys on reachability, so this does not change
  my answer -- but it bears on SEVERITY, and it is cheap for someone to check against a boot log.

---

## TASK 2 (a) -- THE ROWS, THEIR `dst_tlb`, AND THEIR OBSERVABLE

`fill()` writes `MTE_MODE = depth` and `copy()` writes `MODE_D32 | MODE_COPY` (0xa00).
`dst_tlb = (mode & MTE_MODE_DST_BUF_MASK 0x1c) >> 2`. **No mode value the probe writes has any
bit of 0x1c set, so `dst_tlb == MTE_TLB_A == 0` in every transfer it performs** -- and
`src_tlb = (mode & 0xe0) >> 5` is likewise 0 on the copy rows. This is true by construction, and
the measurement corroborates it: had any row driven B or C, `M_tlbA` could not have scored 14/14.

| # | row | dst_tlb | observable |
|---|---|---|---|
| 1 | `live` | *no transfer* | guest store then load through RAM at SCRATCH == `0x5a5a5a5a` |
| 2 | `devsig` | *no transfer* | `lw` from CRIME_DE_STATUS == `0x1e000000` (RAM would read 0) |
| 3 | `paint ok` | *no transfer* | `dest[0]` == `0x99` after a plain guest store to the oracle address |
| 4 | `fill alive` | **A** | process survival across a tiled 32-bit fill |
| 5 | `fill ran` | **A** | `dest[0]` is a byte the fill can produce at all (`0x44` or `0x11`) |
| 6 | `fill top` | **A** | `dest[0]` == `0x11` (bg>>24, RGBA) not `0x44` ((uint8_t)bg, CI) |
| 7 | `fill bot` | **A** | `dest[3]` == `0x44`; gated on `fill_top_ok` |
| 8 | `depth8 top` | **A** | `dest[0]` == `0x44` at 8bpp -- the branch must stay COLD |
| 9 | `depth16 top` | **A** | `dest[0]` == `0x44` at 16bpp |
| 10 | `depth64 top` | **A** | `dest[0]` == `0x44` at field value 3 |
| 11 | `copy alive` | **A** (src A) | process survival across a tiled 32-bit copy |
| 12 | `copy top` | **A** (src A) | `dest[0]` == `0x1a` -- pins COUPLING, invariant under both correct shapes |
| 13 | `copy 2nd` | **A** (src A) | `dest[1]` == `0x2b`; gated |
| 14 | `copy 4th` | **A** (src A) | `dest[3]` == `0x4d`; gated |

Three rows are identity/harness controls that perform no MTE transfer; **eleven perform one, and
all eleven use `MTE_TLB_A`.**

> **PREMISE AUDIT -- the brief I was given is wrong on this point.** Its premise 3 says the rows
> all drive A "except a `fill b top` row that pins packing on TLB_B". **There is no `fill b top`
> row in the shipped probe**, at 2956c7e or at HEAD; the string appears only in briefs and seat
> answers. The codex seat found the same thing independently
> (`codex_7g1_20260909.err`: *"The named detector has no `fill b top` row"*). This matters
> because the parenthetical is the strongest argument on the DEBT side -- "B is already covered,
> so only C is exposed" -- and it is an argument from a row that does not exist.

## TASK 2 (b) -- IS `switch (dst_tlb)` A DOMINATING PREDICATE? MY ANSWER TO 7g-1

**Yes, and not marginally.** In `do_mte_transfer()` at HEAD `b4d4177` the switch is at `:1474`
and the edited comparison at `:1519`, inside the block the switch's first three labels share.
Control reaches the edited line **only** when `dst_tlb` is one of `MTE_TLB_A`, `MTE_TLB_B`,
`MTE_TLB_C`. It is inside the enclosing function, so no callee or caller walk is needed and the
DEPENDS-ON bound is respected on its own terms.

**MY ANSWER: FLOOR. The three labels are floor cells, and the two unrowed ones are an L2 breach
of the shipped detector.** Four reasons, in descending strength:

1. **The mutant's SHAPE is clause (d)'s canonical form.** The carrier states it plainly when it
   corrects the ask-again cap: *"E1 was `if (X)` to `if (X && Y)` on the DOMINATING predicate --
   the canonical clause-(d) form, i.e. a floor breach"*. `M_tlbA` is exactly that, where `Y` is an
   operand of the dominating predicate. Nothing about the edit is exotic.
2. **The pass-11 FLOOR sentence names dominating predicates, not guard operands.** *"the FLOOR ...
   is the cross-product of the guard's dominating predicates with the device-STATE lvalues the
   fix's own repair path reads that are JOINTLY REACHABLE through its own data flow."* `switch
   (dst_tlb)` is a dominating predicate; its three admitted values are jointly reachable; I
   measured that.
3. **The `pcc2widthkills` precedent is structurally identical and ruled the other way from the
   PRETABLE.** There, one block served TWO case labels and the flagship adjudication made the
   LABEL a full axis of the closure -- *"at a block that serves TWO case labels the siblings are
   the LABELS"* -- with `{T2, T1}` appearing in the eight-cell cross-product. This is the same
   shape with three labels. A rule that made the label an axis at PCC2 and not here would be keyed
   to nothing the code distinguishes.
4. **The body is not label-independent, which is where the PRETABLE's reason is weakest.** Its
   warrant is *"the repaired comparison does not read `dst_tlb`"*. True -- and the comparison is
   not the whole of the DEPENDS-ON test. The guarded body is `src_mode |= ...; dst_mode |= ...`,
   and `dst_mode` is **computed from `dst_tlb`** four lines above
   (`dst_mode = (dst_tlb << 10) + ...`). So `dst_tlb` is inside the very lvalue the repair
   modifies. Calling that difference "PACKING, not the comparison under test" describes the
   CONSUMER of `dst_mode` correctly, but the floor asks which cells the repair's own observable
   can differ in -- and I measured it differing.

**THE STRONGEST CASE FOR THE OTHER SIDE, stated fairly, because it is the reading the round
adopted.** The pass-10 wording is *"the PARTITION the body's own tests induce"*, and the shared
block performs no `if` on `dst_tlb`; it uses it arithmetically. At PCC2 the body genuinely
*tested* its label (`relative_addr == PCCTWO_T1ICR`), so a strict reading distinguishes the cases,
and under it B and C are debt -- which is what `PRETABLE.out` section 1 concluded, on the grok
seat's reading, over the codex seat's contrary one. **So the two carrier sentences pull opposite
ways and this genuinely needs adjudicating rather than looking up.** My tiebreak is that a
`switch` with three written case labels IS the code's own test of that variable -- the labels are
not my partition, they are the author's -- and that the measured-reachability clause exists
precisely to settle ties like this one.

**WHAT WOULD CHANGE MY ANSWER:** a measurement showing B and C unreachable or unserviceable (the
opposite of `reach_M_tlbA.raw`), or a ruling that a `switch` label is not a "test" for pass-10
purposes -- in which case the same ruling retroactively unmakes PCC2's `{T1, T2}` axis, and that
consequence should be faced rather than left implicit.

**THE COST, because it is what usually decides these and here it is small.** Closure is **TWO
ROWS** -- `fill b top` and `fill c top`, the same fill at `dst_tlb` 1 and 2 reading `dest[0]`,
i.e. exactly the control I already ran and preserved. Two extra sessions. They kill `M_tlbA`,
`M_tlbAB` and every other single-label exemption.

> **AND THE DEMAND MUST NOT BE THE CROSS-PRODUCT, or the rule becomes the growth it forbids.**
> `depth` x `label` x `{fill, copy}` x `{src, dst}` is 48 cells. The floor here is the LABEL axis
> crossed with the ONE observable the repair controls at the depth the fix repairs -- three cells,
> of which one is already rowed. Everything else stays clause-(e) debt. I say this explicitly
> because "the labels are a floor axis" is one careless sentence away from demanding 48 rows.
>
> **A bound that falls out of the same reasoning, and it shows the rule does not explode:** the
> OTHER dominating predicate over a TLB variable, `if (src > MTE_TLB_C) { fatal; exit(1); }`,
> tests only a threshold, so the partition IT induces is two-valued and exactly one value reaches
> the edited line. It contributes **one** cell, already rowed -- not three. A predicate that names
> three cells owes three; one that names two owes the one that survives.

**CLASS-CLOSURE TRIGGER.** Pass 2 found `M9_ge32` sweeping the 13-row detector clean (an undriven
cell of the `depth` axis); this pass finds `M_tlbA` sweeping the 14-row detector clean (undriven
cells of the `dst_tlb` axis). **Two consecutive passes, one class: a dispatch axis of
`do_mte_transfer()` left single-valued by the row set.** The carrier's amendment applies -- close
the class in ONE diff and write into the contract which cells are covered and which are not, so a
third pass verifies an enumeration instead of hunting a third axis. The axes are enumerable by
reading the function's own inputs: `depth` (4 values, all now driven), `dst_tlb` (3 reachable
labels, 1 driven), `mode & MTE_MODE_COPY` (2, both driven), `src_tlb` (1 surviving cell, driven).

**DISPOSITION.** #509 is shipped, so the late-dissent rule governs: this is a *measured false pass
against the shipped detector's floor*, disposition 2 -- L2, repaired in a follow-up commit, not
amended under #509's number. If the adjudication lands on DEBT instead, then `PRETABLE.out`
section 5's disclosure already covers it and the only thing owed is that the CONTRACT in the probe
header say so **in the probe**, where a future row-writer will see it -- **it currently does not;
the disclosure lives only in `PRETABLE.out`.** That is a records gap under either ruling.

## TASK 2 (c) -- AN ADDED COMMENT ASSERTING AN OBSERVABLE CONSEQUENCE NO ROW PINS

**Yes.** The `#509` diff has one hunk and adds one comment. The sentence, verbatim:

    So both assignments were dead, every tiled transfer took the CI arm, and at 32 bits CI
    assigns buf[0] alone while memory_rw copies four -- publishing three bytes of host stack
    into guest memory.

**"every tiled transfer"** is a universal over the block's three case labels -- that is what
*tiled* means here, the A/B/C arm as against the LIN_A/LIN_B arm below it. The row set
instantiates that universal at **one label of three**. `PRETABLE.out` section 2 maps this
sentence to `fill top` and `copy 2nd`, and both drive `MTE_TLB_A` only; the quantifier gap is not
noted there, although section 1 of the same file discloses B and C two pages earlier. **The
disclosure was made and then not carried into the CLAIM to ROW mapping** -- which is that file's
own recorded failure mode (`#490`: rows prescribed in the block and lost when the row list was
rewritten), arriving one section apart inside a single document.

Two smaller notes on the same comment, both in the fix's favour:

* *"This repairs the 32-bit cell ONLY"* -- I can now confirm this is TRUE and, usefully, true
  across labels: BASE is RGBA at A, B and C, so the repair is uniform where it applies.
* *"depth is a count of BITS ... 8/16/32/64 only"* -- rowed at all four values since the `M9`
  repair added `depth64 top`. No gap.

**The honest summary of (c):** the comment is accurate; its SCOPE is three times the row set's, and
nothing in the probe says so. One sentence in the probe header's contract closes that half of it
whichever way 7g-1 is adjudicated.

---

## RESIDUALS FOR THE QUEUE (ranked; none of these is a claim that #509's fix is wrong)

1. **`sgimtedstlbrows`** -- add `fill b top` and `fill c top`. L2 if 7g-1 rules FLOOR; a cheap
   debt payment if it rules DEBT. Measured evidence already exists in `killtable3_20260909/`.
2. **The probe header's CONTRACT does not name the `dst_tlb` limitation.** Clause (e) requires the
   detector to say which edits it is designed to catch; a future row-writer reads the probe, not
   `PRETABLE.out`. Records-only, cheap, owed under either ruling.
3. **Rung-4 question, unattempted:** does NetBSD's `crmfb` (or the PROM) ever program `dst_tlb` to
   B or C? Bears on severity, not on the floor question.
4. **Observation, not a defect:** `do_mte_transfer()` computes the same quantity into two
   variables -- `src` (used only by the `> MTE_TLB_C` kill) and `src_tlb` (used to build
   `src_mode`). They agree today. Given `#515` shipped this week on *one variable meaning two
   things*, a note is worth more than the zero lines it currently has.

---

## ARTIFACTS

    regress/artifacts/sgimtedepth4dead/killtable3_20260909/
        TABLE.txt                  the full table, MD5s and the restore record
        BASE.raw  M_tlbA.raw  M_tlbAB.raw          shipped 14-row detector, all 14/14
        reach_BASE.raw  reach_M_tlbA.raw  reach_M_tlbAB.raw   the reachability control
        tlb_reach_control.py       the control instrument (NOT a proposed row set)
        gxopus7g1_M_tlbA.diff  gxopus7g1_M_tlbAB.diff   one-line edits, vs SEC
        drivers/                   every stage script A-H, and the build-log tails

Every preserved log carries its completion sentinel; verified after copying, not before.
