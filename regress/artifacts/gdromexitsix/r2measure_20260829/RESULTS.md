# r2measure — the measured kill table for `gdrom_decline_probe.py` (20 rows)

**VERDICT: the detector DETECTS. Eleven mutants, ZERO escapes. All three previously
measured escapes are closed by the two rows added for them, and every one of the four
rows that had never been scored by anything now has a measured kill.**

Baseline `dev_dreamcast_gdrom.c` md5 `85846dc966d00efe511d2b5755364490`; baseline binary
md5 `8d473baa488b2aef3eabd3be569f2c9d`; instrument
`pinned/gdrom_decline_probe.py.FROZEN` md5 `188e92ebd8f9593664c294c63fed0d98`, used by
**all twelve runs** (verified: `grep PROBE_INSTRUMENT_MD5 | uniq -c` = 12 of one value).
Apparatus, and the concurrent-`git stash` hazard that nearly invalidated the table, are in
`METHOD.md`.

## Baseline

| run | score | control | log |
|---|---|---|---|
| base, pinned instrument | **20/20** | OK | `probe_base.log` |
| base, pre-stash instrument (04:46, corroboration) | **20/20** | OK | `probe_base_run1_prestash_instrument.log` |

Two independent baseline runs, two instrument copies, identical vectors
(`1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1`).

**A first-run pass was treated as suspicious, per the round's own history of six
construction defects.** What was checked before trusting it: `fmt stage` reads **0x98**, not
`0x0` — the row that catches the `load16` operand reversal; `devsig sh4` reads **0xda74**,
not `0x0` — the device-signature control is not failing open; `live` round-trips through
RAM; `GDROM_DECL_CONTROL=OK` is emitted over the three identity rows only, before any
product row; and the run took 10m24s across 15 real emulator sessions.

## The kill table

| mutant | edit | score | rows that REDDEN |
|---|---|---|---|
| `Ma_toclen` | Site A latch bit -> `GDROM_W_TOCLEN` | 19/20 | **`crossbit`** (`0,1`) |
| `Mb_toclen` | Site B latch bit -> `GDROM_W_TOCLEN` | 19/20 | **`crossbit`** (`1,0`) |
| `M_braceA` | Site A `break` moved INSIDE the latch `if` | 19/20 | **`latch cond`** (`1`, want `0`) |
| `M0_exitA` | floor (b): Site A `exit(1)` reinstated verbatim | 13/20 | `fmt surv`, `fmt says`, `fmt x2`, `fmt cnt`, `fmt event`, `both sites`, `crossbit` |
| `M1_exitB` | floor (b): Site B `exit(1)` reinstated verbatim | 13/20 | `unk surv`, `unk says`, `unk x2`, `unk cnt`, `unk event`, `both sites`, `crossbit` |
| `Md_nolatchA` | clause (d): Site A latch tested, never set | 19/20 | `fmt x2` (`2`, want `1`) |
| `Md_nolatchB` | clause (d): Site B latch tested, never set | 19/20 | `unk x2` (`2`, want `1`) |
| `M_growA` | `!= 0x20` -> `!= 0x21` (accept-set growth) | 13/20 | `fmt says`, `fmt x2`, `latch cond`, `both sites`, `crossbit`, `acceptA`, **`accept sil`** |
| `Md_hoistannounce` | announce hoisted to the head of `case 0x30` | 18/20 | `fmt 0x24`, **`accept sil`** — and **`acceptA` GREEN** |
| `M_retA` | Site A `break;` -> `return;` | 18/20 | `fmt cnt` (`0x98`), `fmt event` (`clear`) |
| `M_retB` | Site B `break;` -> `return;` | 18/20 | `unk cnt` (`0x98`), `unk event` (`clear`) |

`GDROM_DECL_CONTROL=OK` on every run — no result below is an apparatus failure.

**Every one of the eleven matched a prediction written down BEFORE the measure phase ran**
(`PREDICTIONS.md`, whose mtime precedes every log). Both the scores and the exact row sets
matched. That is worth stating plainly because it is unusual and because it is the
cheapest evidence that the table measures what it claims to.

## Per-row: which mutants each row killed

| row | killed |
|---|---|
| `live` | *(identity control — see below)* |
| `devsig sh4` | *(identity control)* |
| `gdrom map` | *(identity control)* |
| `fmt surv` | `M0_exitA` |
| `fmt says` | `M0_exitA`, `M_growA` |
| `fmt x2` | `M0_exitA`, `Md_nolatchA`, `M_growA` |
| `latch cond` | `M_braceA`, `M_growA` |
| `fmt stage` | *(apparatus control — see below)* |
| `fmt cnt` | `M0_exitA`, `M_retA` |
| `fmt event` | `M0_exitA`, `M_retA` |
| `fmt 0x24` | `Md_hoistannounce` |
| `unk surv` | `M1_exitB` |
| `unk says` | `M1_exitB` |
| `unk x2` | `M1_exitB`, `Md_nolatchB` |
| `unk cnt` | `M1_exitB`, `M_retB` |
| `unk event` | `M1_exitB`, `M_retB` |
| `both sites` | `M0_exitA`, `M1_exitB`, `M_growA` |
| `crossbit` | `Ma_toclen`, `Mb_toclen`, `M0_exitA`, `M1_exitB`, `M_growA` |
| `acceptA` | `M_growA` |
| `accept sil` | `M_growA`, `Md_hoistannounce` |

**All sixteen product rows have a measured kill. The four without one are the three
identity controls plus `fmt stage`, and that is by design rather than by omission** —
their job is to fail on a null medium or a broken helper, not on a product mutant. They
are graded by floor clause (c) below, not by this table.

## The three questions the round actually owed

### 1. `crossbit` closes BOTH cross-bit escapes — measured

`Ma_toclen` reads `0,1` and `Mb_toclen` reads `1,0` against a wanted `1,1`. A short TOC
sets `GDROM_W_TOCLEN` first; if either new latch aliases it, that site's decline prints
**nothing at all** and the guest gets a mute refusal. One row covers both bits.

### 2. `latch cond` closes the brace slip — and this was the one row that could not be trusted until it did

Under `M_braceA`, `fmt says` and `fmt x2` **both stay GREEN at 1** — which is exactly why
the mutant escaped the 13-row plan; "announces once" reads the same either way. Only
`latch cond` moves, `1` against a wanted `0`.

**This measurement was load-bearing for a second reason.** `latch cond` wants `0`, and a
regex that matches nothing also returns `0`. `REJ` is read by **no other row in the probe**,
and by no row at all with a non-zero wanted value — so before this run the row was formally
*indistinguishable from a dead regex*, exactly the shape the round's own
wanted-equals-failure rule was minted to catch. It has now been measured at `0` on the
baseline and `1` under the mutant, and at `2` under `M_growA`. The channel varies; the row
is a real oracle.

### 3. `accept sil` is failable AND non-redundant — measured, and the second half needed a purpose-built mutant

`M_growA` reddens it (`1`, want `0`), which discharges "never scored by anything". But
`M_growA` reddens `acceptA` too, so on its own it shows only that the row can fail — not
that it discriminates anything its neighbour does not.

`Md_hoistannounce` was built for that question: the announce is moved to the head of
`case 0x30`, so the guard is untouched and the decline still declines, but the message now
fires on **accepted** commands as well and stops meaning "declined". Measured:
**`accept sil` REDDENS while `acceptA` stays GREEN.** The legal command still reaches the
`Huh?` guard, so `acceptA` is satisfied; only `accept sil` sees the defect. The row earns
its place.

## The floor clauses, measured rather than argued

| clause | measurement | log |
|---|---|---|
| **(a)** fails on the pre-fix build | **8/20, CONTROL=OK**, 12 rows red | `probe_PREFIX.log` |
| **(b)** fails on a verbatim reinstatement at EVERY fixed site | `M0_exitA` 13/20 and `M1_exitB` 13/20 | `probe_M0_exitA.log`, `probe_M1_exitB.log` |
| **(c)** fails on a null medium | **4/20, CONTROL=DEAD** | `probe_NULLMEDIUM.log` |
| **(d)** fails when the guard is kept and its repair nulled | `Md_nolatchA`/`Md_nolatchB` 19/20; `M_braceA` 19/20; `Md_hoistannounce` 18/20 | as above |

### (a) — the pre-fix build, from the commit rather than from a reconstruction

Built from `git show HEAD:src/devices/dev_dreamcast_gdrom.c`, md5
`a1bd4373d4f4aa5e4dbf74103c051bfc`, 88 lines different from the pinned baseline; binary
md5 `f23d944ab72ff2cb76efbb8f1ba5fd02`.

**8/20 with `CONTROL=OK`** — and the control line is the point. Twelve product rows red
while all three identity controls stay green, so the failure is attributable to the
product and not to a rig that never reached the device. Both sites read `exit1` against a
wanted `exit0`: the host really does die on an ordinary guest store on the committed build.

`M0_exitA` and `M1_exitB` each reinstate ONE site, so between them clause (b) covers both
— but never in a single binary. This run is the pre-fix build itself, which is what
clause (a) actually asks for.

### (c) — the null medium, and it demonstrates the wanted-equals-failure class outright

The probe was run against **`/bin/true`** — a binary that is not gxemul at all. Result
**4/20 with `GDROM_DECL_CONTROL=DEAD`**. The three identity rows all fail, so the run is
condemned as an apparatus failure, which is exactly how the gate section reads it (controls
first and separately, before any score is believed).

**The four rows that pass against a program that does nothing are worth naming**, because
they are a live illustration of the rule this round minted:

```
fmt surv     exit0  exit0   ok      <- /bin/true exits 0, and exit0 IS the wanted value
unk surv     exit0  exit0   ok      <- same
latch cond   0      0       ok      <- wants 0; a regex matching nothing also gives 0
accept sil   0      0       ok      <- wants 0; likewise
```

*A row whose wanted value equals its failure value is not an oracle.* Four of twenty are in
that shape, and the detector survives it only because `GDROM_DECL_CONTROL` is computed over
the identity rows **alone** and goes DEAD here. That design decision is load-bearing, and
this run is the measurement that shows it.

Both `latch cond` and `accept sil` nevertheless have measured kills on real binaries
(above), so neither is vacuous in service — but neither is self-certifying, and a run whose
controls are dead must never be read as a product pass.

## Residual findings — filed, not fixed

**1. `unk cnt` has no same-session staging guard, while `fmt cnt` does.**
`fmt cnt` is preceded in its own session by `fmt stage`, which reads the staged `0x98`
back **before** the command and so proves the staging landed. The Site B session
(`store16 CNTLO/CNTHI` -> `packet(BAD_CMD)` -> `load16 CNTLO`) has no such read-back. Both
rows want `0x0`, which is also what a broken load helper returns.

*This is a sibling-parity asymmetry: the round's own newly-minted rule was applied at one
de-fatalised site and not at the other.* It is **not** vacuous today — `M_retB` measured
`unk cnt` at **`0x98`**, which proves the staging really does land in that session — but the
row's greenness is not self-certifying the way its sibling's is. One row (`unk stage`)
would close it. Filed rather than fixed: the detector is above the floor, so this is
coverage debt, and adding a row perturbs other mutants' scores and forces a re-table.

**2. `fmt stage` has no measured kill, and should be understood as an apparatus control
rather than a product row.** No product mutant reddens it — under `M_retA` it stays green
at `0x98` while `fmt cnt` moves. Its job is to catch a broken helper, and it has already
done that once historically (it is the row that exposed the `load16` operand reversal).
Worth a sentence in the probe header so a future reader does not mistake its permanent
greenness for a dead row.

**3. `crossbit` covers only the A x B x TOCLEN corner of a nine-writer field.**
`d->warned` now has nine writers sharing one field and six of the pre-existing bits are set
from inside `DEVICE_ACCESS` by ordinary guest register reads. `crossbit` builds one prior
state (`GDROM_W_TOCLEN`, via a short TOC) and checks both new sites against it. A collision
with, say, `GDROM_W_OVERREAD` — which a benign TOC-then-Mount-then-read sequence sets — is
not covered. Extending the same session to touch the other bits first would cover more of
the surface in one row rather than N². Filed as coverage debt.

## Companion record: an independent prediction that converged

`MAINLOOP_PREDICTION_acceptsil.md` in this directory was written by the main loop at ~05:40
— from reading only, before `M_growA` was scored — predicting that `accept sil` would redden
under `M_growA` and that `acceptA` would redden with it. Both predictions held.

It then inferred that `accept sil` was a candidate for COLLAPSE because "no mutant in the
table distinguishes them", and **self-refuted that inference once `Md_hoistannounce` landed**:
an enumerated mutant does separate them, so the KEEP/COLLAPSE question is settled as KEEP.
Its own diagnosis of the error is worth preserving — a universal quantifier written before its
population was complete, which is the frozen-number class in its inference form.

Two records, written independently and in different orders, reach the same conclusion about
`accept sil`. That is stated here so a future reader does not have to reconstruct the
agreement from two files that never reference each other.
