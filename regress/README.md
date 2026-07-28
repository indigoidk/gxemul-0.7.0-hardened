# Regression harness

This fork carries ~290 numbered corrections against GXemul 0.7.0. The harness exists to
answer one question before each push: *did a correction break something that used to
work?*

## The rule this harness is built around

> Only change what we can test for.

A gate that cannot fail is worse than no gate, because it reports green. Two gates in this
tree were retired for exactly that reason and are documented here so they are not
reintroduced:

* **The 20-machine `-V` smoke.** It booted twenty machines on a zero-filled blob and
  quit. Round 51 instrumented it and measured that it executed **zero** floating-point
  stores, so it would have passed identically whether #287 was right, wrong or absent.
* **The 97-alias startup matrix.** With no kernel, every machine prints
  `No filename given. Aborting.` (`core/main.c:583`), so the matrix compared *error
  strings* across builds. It found exactly one real signal (`g4plus`, a fork-added CPU
  subtype) and would not have caught a wrong answer anywhere.

What replaced them is below. Each gate states what it proves and, just as importantly,
what it does not.

## Gates

| # | Gate | Proves | Runtime |
|---|------|--------|---------|
| 1 | `gate_build.sh` | Both trees rebuild clean from committed source: exactly 223 objects (pmax) / 224 (arc), zero warnings, zero errors, and the source sync into each compile tree verified. | ~4 min |
| 2 | `gate_offline.sh` | Differentials the **real, linked** `src/core/float_emul.c` against upstream. Asserts a **closed form** for the change-set plus absolute answers. This is the only gate that covers #287. | ~25 s |
| 3 | `selftest_mutation.sh` | **Proves gate 2 can fail.** Reverts #287 in a scratch copy and requires the differential to go red. | ~50 s |
| 4 | `gate_mips.sh` | The two primary rigs boot OpenBSD 2.2 to `uid=0` — pmax 15/15, arc 13/13. | ~6 min |
| 5 | `gate_crossfamily.sh` | Non-MIPS CPU cores execute guest code and return checked answers: m88k to a root shell with a verified FP result, SuperH through a full kernel boot to a verified device-probe result. | ~12 min |
| 6 | `gate_hygiene.sh` | No distress markers in the boot logs, with a positive control so empty logs cannot pass. | ~5 s |
| 7 | `gate_ab.sh` | Three-way A/B against pristine 0.7.0 and the pre-batch fork. | ~15 min |

Gate 3 is the one that keeps the rest honest. Every other gate asserts something about the
emulator; that one asserts something about **the harness** — that its strongest check
responds to a broken subject. The first version of gate 2 did not, and no amount of green
output would have revealed it.

`./run.sh` runs all six and prints one verdict line per gate. `./run.sh 2 4` runs a subset;
out-of-range selectors are rejected rather than silently running nothing.

Verdicts are `PASS`, `FAIL` and `SKIP`, and **a `SKIP` is never counted as a `PASS`** — it
means coverage did not run, which is a gap, not evidence. A gate whose rigs partly ran is
downgraded to `SKIP` rather than passing on the remainder. The skip exit code is **77**,
not 2, because bash exits 2 on a syntax error: with 2 as the skip code, a typo in a gate
script was silently reported as a coverage gap and the run still exited 0.

## Why gate 2 is the strongest one here — and how it was nearly worthless

`ieee_store_float_value()` is pure. That means it can be differentialled offline over tens
of millions of inputs in seconds, old implementation against new, which is a far stronger
instrument than any boot test.

**But only because it links the real function.** The first version of this gate
transcribed *both* sides of the differential into its own C file and compared the copy
against itself. It never compiled, linked or executed `src/core/float_emul.c` at all — so
deleting #287 from the shipped source would have left all eight checks green. That is the
same defect as the 20-machine smoke this harness retired, one level of indirection further
back, and it was caught in review rather than by the gate. Two things now prevent a repeat:
the gate compiles and links the shipped `float_emul.c`, and it asserts that the file it
compiled is **byte-identical to the committed one**, so "the test passed" and "the
repository is correct" are the same statement.

The gate also checks **absolute answers**, not only agreement: a purely relative
differential passes when both sides are wrong in the same way. `1e300` must store as
`0x7f800000` (+Inf) and `-1e-40` as `0x80000000` (−0) — the values #287 exists to produce.

Beyond that, it does not merely check "did anything change" — it asserts that the set of
inputs where old and new disagree is *exactly*:

```
old(x) != new(x)  =>  (finite && |x| >= 2^128)          // S-format overflow
                  ||  (0 < |x| < 2^-126 && signbit(x))  // S-format negative underflow
```

and that for `IEEE_FMT_D` the change-set is **empty**.

It is checked as an **equivalence, in both directions**, and that matters more than it
sounds. Containment alone (nothing differs outside the classes) is satisfied by a mutant
that clears the overflow mantissa for negative values but not positive ones: both classes
are non-empty, nothing is unexplained, and every positive overflow is still broken. So the
gate also asserts **completeness** — every input inside the classes must differ.

The two extra predicates are load-bearing, not decoration. `x` must be an `isnormal`
double, because a host value below `2^-1022` takes the `FP_SUBNORMAL` arm where both
versions return signed zero; and `x` must not be an exact power of two, because there the
assembled fraction is already zero and #287's mantissa clear is a no-op. That second one
was found the hard way: a first-difference sweep over exact powers of two reported "no
difference anywhere".

Two thresholds live near each other here and must not be conflated — an earlier draft of
this file did conflate them:

* The **exponent reaches 255** at `|x| >= 2^128`, because the S-format bias is 127 and
  `e + 127 >= 255` means `e >= 128`. This is the bound that matters for the change-set:
  #287 clears the mantissa whenever the stored exponent is 255, so old and new can differ
  anywhere at or above `2^128`.
* The **clamp statement** `if (exponent >= 256) exponent = 255` only fires at
  `|x| >= 2^129`. Values in `[2^128, 2^129)` reach exponent 255 *without* the clamp — which
  is precisely why the old code emitted an Inf-with-garbage-mantissa there and the bug was
  not merely a clamping oversight.

A round-50 review brief asserted the clamp fired at `2^128`. Four seats caught it and a
probe confirmed the clamp is at `2^129`. The change-set bound, separately, is `2^128`.

## Why gate 4 exists

`float_emul.c` is shared by five CPU families, but until round 54 only MIPS ever executed
it under test. `cpu_m88k_instr.c` and `cpu_sh_instr.c` both store `IEEE_FMT_S` — the exact
arm #287 changed — and had **no execution coverage at all**.

Gate 4 closes that. The m88k rig drives OpenBSD/luna88k to a root shell and runs an FP
computation in-guest, checking the *answer*, not just that the guest survived:

```
awk 'BEGIN{printf "%.6f %.6f", 1.5/3.0, 2.0**0.5}'   ->   0.500000 1.414214
```

**What gate 4 does not prove, stated plainly because an earlier draft got this wrong.**
It does *not* cover #287. Both `0.5` and `1.41421356…` sit far inside the region where the
old and new implementations provably agree — gate 2's own closed form says they can only
differ at `|x| >= 2^128` or `|x| < 2^-126`. Reverting #287 would leave this gate green.
What gate 4 proves is that the m88k and SH4 **cores** execute guest code correctly and
call into the shared function; #287 itself is covered by gate 2, which links the real
`float_emul.c`. **The S-format overflow arm has no in-guest coverage on any rig**, MIPS
included. Closing that would need a staged guest binary computing something like
`1e30f * 1e30f`, not a double-precision `awk` one-liner.

## Known gaps in the harness itself

Stated here rather than left to be rediscovered. These are limits of the *instrument*, not
of the emulator.

1. **Gate 7 has no positive upstream-capability workload.** Its only cross-build comparison
   is luna88k — a machine upstream 0.7.0 *cannot* boot. So it proves the fork gained a
   capability, but it would not notice the fork *losing* one: a break in an alpha or
   PowerPC machine that upstream ran successfully is invisible to it. Closing this needs a
   guest image that pristine 0.7.0 can demonstrably boot, run under all three builds.
2. **No rig reaches #287's arm.** Covered above and in `images.md`. Gate 2 covers the
   function; nothing covers the S-format overflow path *in a guest*.
3. **`run_emu()` discards the emulator's exit status.** A build that crashed instantly and
   one that ran to the wall clock are distinguishable only by their markers. That is
   sufficient for how gate 7 grades today, but it is less information than is free.
4. **The MIPS step counts are weak assertions.** `completed 15/15 steps` is largely a sum
   of unconditional sends and sleeps; only one step is a real expect. The load-bearing
   evidence in gate 4 is the `uid=0(root)` and token greps, not the count — and on a
   heavily loaded host the count can come up short and fail a perfectly good boot.

## Rig requirements

The harness assumes the local layout documented in `RESUME.md`:

* Two build trees, no VPATH — `build/` compiles from `est/`, `/tmp/gxsec-build` from
  `GXEMUL-SEC/`. Edits must be propagated into both; the build gate re-syncs.
* Guest images under `_images/` and the OpenBSD 2.2 rigs where `RESUME.md` places them.
* Baseline builds at `/tmp/gx-pristine` and `/tmp/gx-prebatch`, produced by
  `gate_ab.sh --build`.

Gates skip with an explicit `SKIP` verdict when their inputs are absent. A skip is never
counted as a pass.

## Guest images

Gate 4 needs images that are not in this repository (they are between 2 MB and 2 GB).
`images.md` lists each one, its provenance and the exact invocation.
