# Regression harness

## Start here

**What this is:** a set of automated checks you run before pushing, to make sure a bug fix
didn't break something that used to work. Run them all with:

```
./run.sh
```

It prints one line per check and a final `REGRESS_PASS` or `REGRESS_FAIL`. Nothing else is
required — no arguments, no configuration.

**What this project is:** GXemul is an emulator for old computers (1990s DECstations, SGI
workstations, Sun-era hardware and so on). This is a security-hardened fork of version
0.7.0, carrying about 290 numbered bug fixes. Each fix has a number like `#287`, and those
numbers appear throughout the code as comments and in `CHANGELOG.md`.

**Vocabulary used here**, because some of it is specific to this project:

| Term | Means |
|---|---|
| **gate** | one automated check, e.g. `gate_build.sh`. Passes or fails. |
| **rig** | a set-up that boots a real operating system inside the emulator, so we can see whether it still works |
| **pmax / arc** | the two main test machines — a DECstation 5000 and an Acer PICA, both running OpenBSD 2.2 from 1997 |
| **pristine** | unmodified upstream GXemul 0.7.0, used as the "before" picture |
| **pre-batch** | this fork as it stood before the most recent round of fixes |
| **HEAD** | the current code |
| **#287** etc. | a numbered bug fix; look it up in `CHANGELOG.md` |
| **a check that can't fail** | a test that reports success no matter what — worse than no test, because it looks like coverage. Several are described below as warnings. |
| **side-by-side comparison** | run the same thing on two builds and compare the results (elsewhere called a *differential*) |
| **nothing extra changed** | no difference appeared outside the ones we expected |
| **nothing was missed** | every difference we expected did in fact appear |
| **proof the check ran** | a check that the test itself did something, so an empty or skipped run can't look like success |

If you only read one thing: **a check that cannot fail is worse than no check**, because it
reports green. Most of the notes below exist because a check in this harness turned out to
be one, and the details are kept so the same mistake isn't repeated.

---

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
| 6 | `gate_hygiene.sh` | No error markers in the boot logs, plus a check that the logs are real, so empty ones can't pass. | ~5 s |
| 7 | `gate_ab.sh` | Three-way A/B against pristine 0.7.0 and the pre-batch fork. | ~15 min |
| 8 | `gate_upstream.sh` | **Upstream's own test suite**, run three-way. The only gate this project did not author. | ~30 s |
| 9 | `gate_asan_sweep.sh` | Every machine type built under AddressSanitizer and compared against upstream. The **breadth** gate. | ~6 min |

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

It is checked **both ways round**, and that matters more than it sounds.

Checking only that *nothing extra changed* is not enough on its own: a broken version that
fixes the overflow for negative numbers but not positive ones would pass it. Both groups
would be non-empty, nothing would look unexplained, and every positive overflow would still
be wrong. So the check also proves that *nothing was missed* — every input that should have
changed did change. Both halves together mean the rule above describes the difference
exactly, rather than merely allowing it.

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

## Gate 9 — every machine, under a memory-error detector

This is the **breadth** check. Every other gate runs four machines; the fork changed 117
source files, and 27 of those belong to architectures (Alpha, ARM, i960, PowerPC, SGI) that
none of the four ever touch. Gate 9 builds every machine type, attaches its devices, and
lets AddressSanitizer watch for memory errors.

**Setup** — it needs two instrumented builds, which take a few minutes:

```
./build_asan.sh          # builds current code and upstream 0.7.0 with ASan
```

Without them the gate reports `SKIP`, never a false pass.

**The comparison runs in one direction only, and that is deliberate.** The fork exists
partly to *fix* memory errors, so upstream being dirty where the current code is clean is
success, not failure:

| Upstream | Current | Meaning |
|---|---|---|
| clean | **dirty** | **regression — gate fails** |
| dirty | clean | the fork did its job |
| dirty | dirty | pre-existing upstream bug, reported but not failed |

**Measured result:** 40 machine types swept, 38 construct successfully, **13 machines where
the fork fixed real memory errors**, **2 still carrying pre-existing upstream bugs**, and
**0 regressions**. Among the 13 is `macppc`, where upstream throws an AddressSanitizer
heap-buffer-overflow that the current code no longer does — that is correction #23, found
by this same technique years ago and now guarded by a standing check rather than a one-off.

**A machine must be given a file or it never starts up.** `-E testmips` with no file prints
a usage message and quits *before attaching any device* — a sweep written that way would
test nothing and pass every time. Handing it a 500-byte dummy file makes it report
`model:`, `cpu:`, `memory:` and attach hardware. Machines with sub-models additionally need
`-e <subtype>`; without that, 13 of 37 never start.

**No ROM images are needed.** GXemul re-implements the firmware in software (`promemul/`:
ARCBIOS, DECstation PROM, Open Firmware, YAMON and others), so machines boot without
proprietary ROM dumps. Only `machine_pmax.c` references a real ROM at all.

## Upstream's own tests, and the intended-difference allowlist

Gate 8 runs the `test/` directory GXemul has shipped since 2021. It is the only gate here
this project did not write, which is exactly its value: every other instrument was
authored by the same process that made the ~290 corrections.

What it covers that nothing else did. The rigs do load kernels, so loader coverage was
never zero — but it was narrow: a.out, ELF32 LSB MIPS, ELF32 MSB PowerPC and gzip. Gate 8
adds **ELF64** (RISC-V LSB and SH5 MSB — a separate code path from ELF32), **b.out i960**,
**MIPS16**, and a **negative case** (`FileLoader_NonsenseFile`), which is precisely the
malformed-input handling the fork hardened. The fork changed seven files under
`src/file/`; ECOFF, Mach-O, SREC and Android still have no corpus.

**The allowlist is the part worth understanding.** With ~290 intended changes, "pristine
and HEAD differ" is not a finding — counting differences is meaningless when hundreds are
deliberate. So each difference is *classified*:

```
identical                       -> fine
differs, maps to correction #N  -> fine, and #N is named in the allowlist
differs, unexplained            -> REGRESSION
```

`intended_norm()` erases exactly one intended change per entry, so whatever survives is by
construction unexplained. Today it holds one entry — **#260**, which routed net
diagnostics through `debugmsg(SUBSYS_NET, …)` and so prefixes them with `net: `. Measured
result: **6 raw differences per case, 0 unexplained**. Adding an entry is a deliberate act
meaning "the fork changed this on purpose, under this number."

### What this gate got wrong on its first run

Both mistakes are the harness's recurring failure mode, so they are recorded rather than
quietly fixed:

1. It used `-e testmips`. That is the **subtype** flag; the machine flag is `-E`. Every
   invocation produced `Sorry, emulation "" (subtype "testmips") is unknown.` — and the
   gate compared that identical error across three builds and reported **22 checks
   passing**. Upstream's own `configure` comment still shows `-e`; it predates the change.
2. Its only guard was a 100-byte floor on output, which an error message clears easily.
   **A floor proves volume, not validity.** Every case now asserts a format-specific
   marker only the real loader can print — `ELF64 LSB`, `b.out`, `a.out` — so an error, a
   usage message or an empty run all fail.

### Deliberately not included

`test/floatingpoint/fptest.c` cross-compiles a guest binary that prints FP results as raw
hex against a golden file — genuinely the in-guest instrument for #287. It is **not** wired
in, because it needs a cross-toolchain, and gate 2 already makes a stronger claim about the
one function #287 changed (20M inputs, closed-form change-set in both directions, plus a
mutation self-test). It would add the end-to-end in-guest FP path: real value, highest
setup cost, least additive. Revisit when a cross-toolchain is available — and note that
#255's NaN canonicalisation will produce *intended* differences in the NaN rows, needing
allowlist entries.

## Guest disk images must be booted with `R:`

Any gate that boots the same disk image more than once — or boots it under more than one
build — has to use GXemul's `R:` prefix:

```
gxemul -e luna-88k -d R:liveimage-luna88k-raw-20250518.img boot
```

`R:` opens the base image **read-only** and routes every guest write into a temporary
overlay that is discarded at exit. Plain `-d` opens it **read/write**, so the guest's
writes land in the shared file and persist.

This is not theoretical. Gate 7 booted three builds sequentially against one writable 2 GB
image, so each build inherited whatever filesystem state the previous one left behind —
including an unclean unmount, because the 300 s budget kills a guest that has already
reached its login prompt. The result was a gate that failed non-deterministically: HEAD
returned `1:1:0` after passing `1:1:1` twice at the same commit with no code change in
between. The image's mtime settled it — it tracked the most recent boot, not the download.

Timing was ruled out by measurement rather than assumed: both builds reach `login:` in
about **100 s** against a 300 s budget, so it was never a marginal timeout.

One caveat worth stating. `R:` freezes the image *as it currently is* — the state many
earlier read/write boots left it in, not a fresh download. So every run now starts from the
same place, which is what a check needs; but that place isn't guaranteed clean.
Re-downloading the image would be needed for that.

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
`images.md` lists each one, where it came from, and the exact command to run it.
