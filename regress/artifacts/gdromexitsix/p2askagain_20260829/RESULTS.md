# #490 pass 2 — the ASK-AGAIN, MEASURED

**VERDICT: the fix is correct and the detector is above the vacuity floor. But the capped
ask-again produced THREE mutants that ESCAPE all 20 rows — each built, each scored 20/20
with `GDROM_DECL_CONTROL=OK`, each row-block byte-identical to base. All three were
predicted in writing before any mutant score existed.**

Apparatus in `METHOD.md`. Predictions in `PREDICTIONS.md`. Drivers preserved beside them.

## The table

| run | edit | score | control | binary md5 | log |
|---|---|---|---|---|---|
| `base` | the round's pinned post-fix source | **20/20** | OK | `8d473baa…` | `probe_base.log` |
| `E1_aliasover` | `(1u << GDROM_W_FMT_B)` -> `(1u << GDROM_W_OVERREAD_B)` | **20/20 ESCAPE** | OK | `0582ccda…` | `probe_E1_aliasover.log` |
| `E2_assignA` | `d->warned \|= GDROM_W_FMT;` -> `d->warned = GDROM_W_FMT;` | **20/20 ESCAPE** | OK | `d97fd1e6…` | `probe_E2_assignA.log` |
| `E3_widenA` | `if (!(d->warned & GDROM_W_FMT))` -> `if (!(d->warned & (GDROM_W_FMT \| GDROM_W_CMD)))` | **20/20 ESCAPE** | OK | `e149e5b6…` | `probe_E3_widenA.log` |

**Every mutant binary is md5-DISTINCT from base and each `diff` of the 20-row block against
base is EMPTY — so these are total escapes, not score ties.** `base` rebuilt in an
independent clone to the r2measure table's own baseline binary md5 `8d473baa…`, which is the
apparatus control.

## What each escape costs

**`E1_aliasover` — the round PREDICTED this and did not measure it; this is the
measurement.** `crossbit` stages exactly one prior latch state (`GDROM_W_TOCLEN`, via a
short TOC), so it covers 1 of the 7 pre-existing bits. No probe session sets the other six:
none reads `GDROM_DATA` (so `NODATA`/`OVERREAD` never fire), every session writes `COND`
before its packet (so `NOTWAIT` never fires), every access is 16-bit (so `LEN` never fires),
and none arms DMA. **The contract was narrowed at 07:51 to name `GDROM_W_TOCLEN`
specifically and to predict "20/20" for exactly this mutant; the prediction is now measured
and correct.**

**`E2_assignA` — ONE CHARACTER, and the damage is at the OTHER eight latches.** Site A still
announces exactly once, so every Site-A row stays green. What breaks is that the latch
*assignment* clears every other bit in `d->warned`. `case 0x14`'s TOC-length decline is
guest-driven (`d->cnt != 408`, and `cnt` is two guest stores), so a guest alternating a
short TOC with a bad data format re-announces `#489`'s diagnostic **without bound** — and
`fatal()` cannot be silenced by `-q`. That is the guest-drivable flood class `#489` closed,
re-opened by deleting a `|`. **No row observes any latch bit across a Site-A decline**;
`crossbit` reads only whether the two NEW sites still speak, and they do.

**`E3_widenA` — the two-site rows fix ONE site order, and that gives ASYMMETRIC protection.**
`both sites` and `crossbit` both run Site A before Site B. Under this mutant Site A's guard
also tests `GDROM_W_CMD`, so on the probe's order nothing changes; reverse it — an unknown
COMMAND before an unknown FORMAT, the order a probing guest naturally walks — and Site A is
permanently silent. **Measured green: `both sites` `1,1`, `crossbit` `1,1`.**
*The same widening at SITE B would be CAUGHT* (`both sites` would read `1,0`), because Site A
runs first and sets `GDROM_W_FMT`. So the row set defends Site B against guard-widening and
does not defend Site A.

> **AND THE PASS-1 SESSION THAT DISCOVERED THE TWO-BIT REQUIREMENT USED THE OTHER ORDER.**
> `opus_r2table_20260828/tprobe2.py`'s `S3 both` is `stage_toc` -> `cmd12(W(0x31,0x20))` ->
> `cmd12(W(0x30,0x21))` — **CMD before FMT**. The shipped rows inverted it. For `M3shared`
> the inversion is harmless (either order loses a site); for an order-asymmetric guard edit
> it is the whole difference. Nothing in the round's records notes the inversion.

## A FOURTH candidate, REASONED AND THEN REFUTED — recorded because it was refuted

`E4`: delete `case 0x70:` so MOUNT (which NetBSD's `gdrom_mount_disk()` issues) falls into
the now-declining `default:`. Pre-fix that killed the host on the first mount; post-fix it is
a silent decline. **It does escape all 20 rows** — `0x70` appears once in
`gdrom_decline_probe.py` and that once is the *unused* `MOUNT` constant, and zero times in
`gdrom_data`, `gdrom_default` and `gdrom_toclen`.

**But it is CAUGHT, by a different gated probe.** `artifacts/gdrompionull/gdrom_pio_null_probe.py`
(13 rows, run by `gate_sh_rounding.sh`) has `staged quiet`, whose `NOISE` list contains a bare
`re.compile(r"unimplemented")`. The new `default:` decline text matches it, moving the row
from `1 of 8` to `2 of 8`. **So the prediction was wrong and is recorded as wrong.**

*The catch is incidental and rests on an unanchored pattern that this very round measured to
be too loose at its own site — `gdrom_decline_probe.py`'s header records that a bare
`unimplemented data format` matched two different messages and had to be anchored on
`-- declined`. `gdrompio`'s NOISE list still carries the unanchored form.*

## The one-declaration fix for the E1 class, CONTROLLED IN FIVE STATES

The round declined to close the alias class by rows, on addition-licence economics —
"DELIBERATELY NOT CLOSED BY BUILDING TWELVE MORE ALIAS MUTANTS". **That objection does not
apply to a compile-time bound, which closes the whole class in one declaration and costs no
rows and no object code.** The enum already makes the bit POSITIONS unique; each mask
`#define` then re-types its enumerator BY HAND, and that hand-written copy is the only place
an alias can enter — which is exactly what the round's own text identifies as "the realistic
edit ... a hand-written raw mask".

```c
typedef char gdrom_w_masks_disjoint[
    ((GDROM_W_LEN | GDROM_W_NODATA | GDROM_W_NOTWAIT | GDROM_W_OVERREAD
      | GDROM_W_DMANODATA | GDROM_W_DMAARM | GDROM_W_TOCLEN | GDROM_W_FMT
      | GDROM_W_CMD) == ((1u << GDROM_W_NBITS) - 1u)) ? 1 : -1];
```

Measured (`ASSERT_CONTROLS.out`, `assert_test.sh`), `gcc -std=c99 -pedantic-errors -Wall -Wextra`:

```
  s1_correct         COMPILES     the shipped masks
  s2_E1alias         REFUSED      my measured escape
  s3_Matoclen        REFUSED      the round's own Ma_toclen shape
  s4_M3shared        REFUSED      the round's own M3shared shape
  s5_E1_noassert     COMPILES     E1's alias WITHOUT the assert -- the negative control
                                  proving the assert is what refuses
```

**Warrant is transferred, not invented:** it is the identical negative-size-typedef idiom
already in this file at `gdrom_w_fits_its_carriers`, whose own licence sentence the file
quotes from `#388` — *"a static assertion costs nothing and covers the build the test cannot
reach."* This shape appears in exactly ONE file in the tree (`grep -l "1u << .*_B)" src/devices/*.c`),
so the change is scoped to one declaration in one file.

**It fails CLOSED when a tenth bit arrives:** a new enumerator raises `GDROM_W_NBITS`, and a
mask omitted from the OR list makes the equality fail — a compile error naming the author,
not a silent pass.

**And the three grounds on which the carrier records a disjointness assert being REJECTED for
`dev_sh4.c` each fail here**, checked rather than assumed: the bit domains are meant to be
pairwise disjoint (not "overlapping pervasively"); separation rests on the CONSTANTS (not on
array indices); and the values are internal latch bits that `Ma_toclen`/`Mb_toclen`/`E1`
prove can be written wrong (not immutable hardware layouts).

## Severity — and the precedent says FILE, not a floor breach

`#490`'s detector satisfies clauses (a)–(d) with measured mutants, and (e) exists. Under
`#464`'s precedent (`wdcperopcode`: *"Explicitly OUTSIDE `#464`'s contract, not a floor
breach"*; `wdcsectorreset`: a one-line latch-reset leaving all 26 rows green, dispositioned
*"coverage debt under the stopping rule and not a floor breach"*), these are **coverage
debt**.

* **`E1`** is now DISCLOSED in the contract, so it is outside it. My contribution is turning
  a prediction into a measurement.
* **`E2` and `E3` are disclosed NOWHERE.** Clause (e) says an escape is either outside the
  contract or a breach of it; these are currently neither. **The proportionate fix is one
  sentence each in the NOT-claimed list** — plus, for `E3`, one reversed-order two-site
  session, which is the cheapest row in the set and closes an asymmetry this round has
  already been bitten by once.

*`wdcsectorreset` is the direct structural analogue of `E2` and its record says "First job is
to build the mutant and score it." Mine arrives measured rather than source-proven.*
