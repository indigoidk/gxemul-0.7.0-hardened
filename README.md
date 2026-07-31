# GXemul 0.7.0 — hardened fork

> **⚠️ Unofficial fork — this is _not_ the official GXemul repository.**
> The official GXemul is by Anders Gavare at <https://gxemul.sourceforge.net/>.
> This fork is **not affiliated with, nor endorsed by, the original author.**

[GXemul](https://gxemul.sourceforge.net/) (Anders Gavare, GPL) is a full-system
computer-architecture emulator: it runs real, unmodified operating systems on emulated
hardware, across several CPU families (MIPS, PowerPC, SuperH, ARM, Motorola 88K, …) and whole
machines (DECstation, Acer PICA/Jazz, SGI, macppc, Dreamcast, …) — CPU, MMU, interrupt
controllers, serial, framebuffers, SCSI/IDE disks, Ethernet NICs. It is educational/experimental
software, **not a security boundary.**

This fork starts from the final upstream release, **0.7.0 (2021)**: the first commit is the
untouched upstream tree, and everything after it is the change set summarized below.

## New here? Read this bit

**What it does:** runs old operating systems on emulated 1990s hardware — you can boot a
1997 copy of OpenBSD on a simulated DECstation and get a shell.

**What this fork adds:** about 290 bug fixes to that emulator, mostly memory-safety and
correctness issues. Each fix has a number like `#287`, marked in the source as
`/* #287: ... */` and written up in [`CHANGELOG.md`](CHANGELOG.md).

**Try it:**

```
./configure && make
./gxemul -H                    # list every machine it can emulate
```

**Check nothing is broken:**

```
regress/run.sh                 # runs all the automated checks
```

That prints one line per check and ends with `REGRESS_PASS` or `REGRESS_FAIL`. See
[`regress/README.md`](regress/README.md), which opens with a plain-language guide and a
glossary of the terms this project uses.

**A few terms you'll meet:** *pristine* means unmodified upstream 0.7.0; *rig* means a
setup that boots a real OS so we can check it still works; *pmax* and *arc* are the two
main test machines (a DECstation and an Acer PICA, both running OpenBSD 2.2).

## What changed

**~283 numbered corrections** (each tagged `/* #NNN */` in the source) across ~59 review rounds,
in four themes:

1. **Guest→host memory safety & robustness** (the bulk, #1–~#154) — bound guest-controlled
   indices, lengths, and DMA in devices, file/disk loaders, the network stack, and the
   guest→host memory boundary, so an untrusted ROM, disk image, or guest cannot drive
   out-of-bounds writes into the host; guest-reachable `exit(1)`/`abort()`/host crashes become
   warn-and-continue.
2. **Hardware fidelity** (#155–#294) — accuracy to real silicon: MIPS fault-signature fidelity,
   guest-reachable host halts turned into hardware-plausible faults, R4000 FPU denormal traps,
   MIPS FPU result-correctness (div/sqrt/compare/NaN canonicalization, #254/#255), the R4030
   interval-timer rate (#257), LANCE RX-ring exhaustion signalling (#262), and a **deep NCR 53C94
   (ASC) SCSI + Jazz R4030 DMA audit** (#263–#268): DMA-accounting safety (count clamp,
   heap-disclosure), a guest-reachable `exit(1)` turned into a SCSI disconnect, FIFO-occupancy and
   chip-reset-IRQ hygiene, and R4030 translation-table / count-register bounds. Rounds 40–46
   (#269–#279) add a pmax/arc **host-abort and diagnostic-hygiene sweep**: a guest-reachable VGA
   CRTC `exit(1)` (#271), LANCE descriptors held forever instead of dropped or failed (#274/#275),
   the FP→integer conversion of NaN/±Inf/out-of-range values pinned to the R3010/R4010 result
   instead of an undefined C cast whose answer depended on the build host (#273), and six
   guest-repeatable `fatal()` floods either verbosity-gated or latched once per device (#269,
   #272, #276–#279). Rounds 47–54 (#280–#290) pursue one theme — **an emulated device telling the
   guest a transfer succeeded when it did not**: the ASC reported short DATA\_IN and DATA\_OUT
   transfers as complete (#281–#284, and #286 for the count it still took from the *request*
   rather than the transfer), a MODE SELECT gate parsed a byte that was never sent (#285), the
   S-format store turned a floating-point overflow into a NaN encoding where hardware gives ±Inf
   (#287), the arc keyboard ring discarded its whole contents on overrun while its drain loop
   could starve the guest outright (#288), and the COP1 decoder admitted floating-point formats no
   ISA level in the machine actually defines (#290). Round 53 audited a sixth candidate and
   **shipped no code**, because the check it proposed would have been unreachable by construction.
3. **Debuggability** — subsystem breakpoints, breakpoint hit-counts + "run N" (#248), data
   write-watchpoints (#250), an honest `breakpoint subsystem` listing (#270), verbosity gating,
   and debugger conveniences.
4. **New capabilities** — see [Feature highlights](#feature-highlights).

Every round is regression-gated: **0 errors / 0 warnings** under gcc and clang, a
multi-CPU-architecture boot sweep, and full OpenBSD 2.2 rigs on pmax (R3000) and arc (R4000)
booting to a root shell and halting cleanly. Built with an agentic multi-model workflow: each
change drafted by Claude, then adversarially reviewed to consensus by independent models (Codex
GPT-5.x, Fable, Gemini, and other cloud models) before commit.

Two working rules do most of the load-bearing work. **Only change what can be tested for** — the
wrong behaviour is reproduced on the committed build *before* any edit, and a candidate that
cannot be reproduced is documented rather than patched; round 53 closed that way, and so did the
`dev_asc.c` PMAZ address register during the R4030 audit. And **the panel decides by measurement,
not by vote** — where seats disagreed, the tie was broken by fault injection or a probe on the
real rigs, which has now overturned the panel majority several times. Each round also records what
it did *not* prove: several corrections here are latent on the reference guests and say so.

## Commit timeline

Oldest first.

| Commit | Change |
|--------|--------|
| `39748e3` | Import GXemul 0.7.0 (unmodified upstream baseline) |
| `8dd86b5` | Security hardening: ~119 memory-safety & robustness corrections (#1–#119) |
| `b75e05d` | docs: hardened-fork notice, highlights, provenance |
| `3925954` | docs: changeset patch, regression battery, outstanding-bugs notes |
| `266aaaa` | battery: scrubbed regression harness + battery docs |
| `5ee491e` | Security review (#130–#154) + feature round (#120–#129): 23 fixes |
| `9d18d15` | arc: OpenBSD 2.2 headless bring-up + NE2000 networking |
| `8426be6` | README: document the OpenBSD 2.2/arc + NE2000 round |
| `de1398e` | Hardening / fidelity / debuggability rounds 17–25 (#155–#250) |
| `af0c73b` | Round 26 (#251/#252): console host-glue fidelity (output flush + stdin-EOF freeze) |
| `4975057` | CHANGES.patch: regenerate to match the SEC tree (recover missed files) |
| `dee8c1a` | Round 27 (#253): `net_tap_init` — Linux tun/tap clone-device path |
| `5af5422` | README: reorganize for flow (GXemul intro, change summary, timeline, features) |
| `9e4239e` | Round 28 (#254/#255): MIPS FPU result-correctness — div/sqrt via host IEEE, unified compare, NaN canonicalization |
| `bfd4a2c` | Round 29 (#256): interactive-debugger MIPS breakpoint sign-extension |
| `b679170` | Round 30 (#257): R4030 interval timer honors the guest-programmed rate |
| `f5d85ca` | Round 31 (#258): decoded STATUS/CAUSE/FCSR in the MIPS register dump |
| `962bf09` | Round 32 (#259–#261): debugger/net QoL — implicit `-K`, net→`debugmsg`, opt-in break-on-error |
| `24d6678` | Round 33 (#262): LANCE RX-ring exhaustion → CSR0.MISS / descriptor BUFF + drain-fix |
| `794c415` | Round 34 (#263): ASC/R4030 DMA accounting — heap disclosure + count over-transfer |
| `87c062a` | Round 35 (#264): ASC zero-length DATA_OUT host-abort → guest disconnect |
| `508ab23` | Round 36 (#265/#266): ASC FIFO occupancy + chip-reset IRQ hygiene |
| `938aa8b` | Round 37 (#267): R4030 DMA translation-table limit |
| `a749cbe` | Round 38 (#268): R4030 DMA count-register width mask |
| `4011246` | Round 39: close the ASC/R4030 DMA audit — document known gaps |
| `5bc4353` | README: document the FPU / debuggability / ASC-R4030 batch (rounds 28–39, #254–#268) |
| `2dfa3d4` | OUTSTANDING_BUGS: record two pmax/arc emulation-fidelity candidates (cross-arch trueness review) |
| `fc6e0b1` | OUTSTANDING_BUGS: test-first triage refutes both trueness candidates (no change) |
| `afd244d` | OUTSTANDING_BUGS: conclude the post-batch pmax/arc fidelity cluster (non-triaged remainder documented) |
| `4ad04c4` | README: refresh commit timeline (post-scrub hashes + recent doc commits) |
| `be95418` | Round 40 (#269/#270): self-review fixes — ASC FIFO diagnostic flood, breakpoint-listing honesty |
| `680cb56` | Round 41 (#271/#272): VGA CRTC — guest-reachable host abort → latched `fatal()`; unhandled-index flood → DEBUG gate |
| `79d04eb` | Round 42 (#273): FP→integer conversion — undefined C cast → the pinned R3010/R4010 result |
| `5bf592d` | Round 43 (#274/#275): LANCE — descriptors held forever instead of dropped or failed |
| `d917a66` | Round 44 (#276/#277): ASC — two guest-repeatable diagnostic floods, one gated and one latched |
| `b93b428` | Round 45 (#278): MIPS exception path — nine ungated `fatal()` calls per low-address guest access |
| `b38cc4f` | Round 46 (#279): `float_emul.c` — the reserved-format `fatal()` cluster, and a missing `return` |
| `895af34` | docs: close out rounds 41–46 (#271–#279) — timeline, and a real backlog |
| `18f81d2` | docs: backlog items 8 and 9 — S-format overflow, and the VGA stale length |
| `05488a1` | Round 47 (#280): `dev_fdc.c` — one host line per guest access to an unmodelled register |
| `a0d34f4` | Round 48 (#281/#282): ASC — a short DATA\_IN transfer reported as if the full count had moved |
| `2b52fca` | Round 49 (#283): ASC — a short DATA\_OUT DMA committed bytes the guest never supplied |
| `8522065` | Round 49 (#284): ASC — the COMMAND-phase DMA counter said "nothing moved" and "complete" at once |
| `2ffc91e` | Round 49 (#285): the MODE SELECT gate accepted a partial parameter list, and parsed a byte that was never sent |
| `26de880` | Round 50 (#286): the DATA\_IN counter still reported the count requested, not the count that moved |
| `0f95109` | Round 51 (#287): the S-format store turned an overflow into a NaN, and an underflow into +0 |
| `992bccb` | Round 52 (#288): the arc keyboard queue discarded itself, and its drain loop starved the guest |
| `84ee137` | Round 53: R4030 DMA delivery accounting — audited, **not** changed (no correction number) |
| `85a1d9e` | Round 54 (#290): the COP1 decoder enforced ISA level nowhere (#289 is void) |
| `120586c` | docs: bring the commit timeline current (rounds 47–54, #280–#290) |
| `2050c50` | Round 55: a regression harness, and the retirement of two gates that could not fail |
| `8cbc2bb` | regress: gate 1's divergence and sync checks were passing on an empty list |
| `ff57278` | regress: gate 8 — run upstream GXemul's own test suite, three-way |
| `218ab01` | regress: gate 9 — every machine started under AddressSanitizer, vs upstream |
| `db562cf` | docs: plainer words throughout (glossary; jargon explained inline) |
| `d961cac` | Round 56 (#291): the ARM cache-size fields shifted a negative number |
| `3eaaf3a` | Round 57 (#292): single-precision results were 1 ulp low half the time |
| `3ab1a40` | Round 58 (#293): typed input on SuperH was stolen before the serial port saw it |
| `6440006` | Round 59 (#294): cvt.w honours the FPU rounding mode; trunc.w provably does not |
| `e61badd` | Round 60 (#295): the fixed-rounding conversions, and a buffer declared full before it was filled |
| `f52c2fe` | Round 61 (#296): SuperH read the FPU rounding-mode field but never used it; gate 10 |
| `06445b5` | Round 62 (#297): ftrc converted with a raw C cast — the guest answer depended on the host |
| `85cc973` | Round 63 (#298): m88k stored its rounding register, read it back, used it nowhere; gate 11 |
| `51899d7` | Round 64 (#299): the single-precision sum was rounded twice — round-to-odd fixes all three families |
| `e644a30` | Round 65 (#300): D-format directed rounding via fma residuals — three panel passes, quantum bands |
| `4453ff2` | Round 66 (#301): cvt.d.l/cvt.s.l converted the integer before the rounding mode existed; gate 12 |
| `96b86a9` | Round 67 (#302): the m88k float→int triad — trnc cast raw, int/nint halted the emulator |
| `e3d972c` | Round 68 (#303): every subnormal decoded wrong on every architecture — pmax unmasked, five rigs measured |

## Feature highlights

- **OpenBSD 2.2/arc bring-up + NE2000 networking** — stock OpenBSD 2.2 on the Acer PICA-61 (MIPS
  R4000) runs fully headless, with networking: an R4030 `EXT_IMASK` interrupt-routing fix (init
  was hanging), a headless VGA-text console, ARC firmware console/boot-path fixes, and a new
  bounds-clamped DP8390/NE2000 NIC — `ed0` pings the NAT gateway at 0% loss.
- **PowerPC 745x extended BATs** — new MPC7455 CPU model + `-e g4plus` macppc subtype
  (IBAT4–7/DBAT4–7, HID0[HIGH_BAT_EN]-gated); purely additive.
- **SuperH** — unaligned-access exceptions + 64-bit `fmov` alignment.
- **Multi-track CUE/BIN** CD-image support.
- **testmips** — RAM above 256 MB.
- **Debugger** — subsystem/debugmsg breakpoints; hit-counts + "run N then break" (#248); data
  write-watchpoints (#250); step-into-call; `find`; `put s`/`put z`; per-subsystem verbosity;
  prefix-abbreviated subcommands; a `-f` disk fsync-on-write CLI option.
- **Console host-glue fidelity** (#251/#252) — an output-flush bookkeeping fix (no lost bursts on
  piped stdout) and a stdin-EOF freeze fix (the emulator no longer wedges when its stdin closes).
- **Linux tun/tap networking** (#253) — `net_tap_init` works on Linux (opens `/dev/net/tun` +
  `TUNSETIFF`), giving the guest a real layer-2 link that can receive unsolicited inbound traffic
  the userspace NAT can't deliver. Enable with `-e <machine> -L tap0` after
  `ip tuntap add dev tap0 mode tap`.
- **MIPS FPU result-correctness** (#254/#255) — `div.d`/`div.s` and `sqrt` now compute via the host
  IEEE unit (dropping an old approximation), all sixteen `c.cond` compare predicates go through one
  correct less/equal/unordered decode, and NaN results store the MIPS legacy quiet-NaN canonical
  form. Validated bit-for-bit on the host and, in-guest, by real `div.d`/`sqrt.d`/`c.lt.d` on
  OpenBSD/pmax.
- **NCR 53C94 (ASC) + Jazz R4030 DMA audit** (#263–#268) — a full fidelity pass over the SCSI
  controller shared by pmax and arc and the arc R4030 DMA engine: the DMA copy is bounded by the
  R4030 byte count (no over-transfer) and the DATA_OUT buffer is zero-filled (no uninitialized
  host heap reaching the guest disk); a zero-length DATA_OUT that used to `exit(1)` the emulator is
  now a guest-visible SCSI disconnect; the 16-byte FIFO no longer mis-reads a full ring as empty; a
  chip reset now releases the interrupt line; and the R4030 DMA honors its translation-table limit
  and 20-bit count-register width. The two boot-critical DMA bounds were gated on empirical arc
  boots (e.g. OpenBSD writes `TL_LIMIT=0x8000`, 0 would-break over ~2,600 transfers), and every
  reachable corrected branch was directly executed on the emulator and its postcondition verified.
  Remaining fidelity gaps (unreachable or needing new interrupt infrastructure) are documented in
  `REVIEW_FINDINGS.md`.

## Regression harness

`regress/run.sh` runs thirteen gates; `regress/run.sh 2 4` runs a subset. The governing rule is
that **a gate which cannot fail is worse than no gate**, because it reports green — and
this fork had been counting two such gates as evidence:

- a 20-machine `-V` smoke that booted each machine on a zero-filled blob and quit. It
  executed **zero** floating-point stores, so it would have passed identically whether
  #287 was right, wrong or absent;
- a 97-alias startup matrix that, with no kernel supplied, compared the three builds'
  **error strings**.

Both were retired and replaced by gates that either execute guest code or differentiate a
pure function in closed form.

| # | Gate | Proves |
|---|------|--------|
| 1 | `gate_build.sh` | Both trees rebuild clean from committed source — 223 objects (pmax), 224 (arc), zero warnings |
| 2 | `gate_offline.sh` | Closed-form differential of `ieee_store_float_value()` over 20,016,002 inputs + `ieee_interpret_float_value()` exhaustive over every subnormal, both signs, with an FTZ/DAZ runtime canary |
| 3 | `gate_mips.sh` | pmax 15/15 and arc 13/13 to `uid=0(root)` on OpenBSD 2.2 |
| 4 | `gate_crossfamily.sh` | m88k and SuperH cores execute guest code and return checked answers |
| 5 | `gate_hygiene.sh` | No distress markers in the raw pty logs |
| 6 | `gate_ab.sh` | Three-way A/B against pristine `39748e3` and pre-batch `2ffc91e` |
| 7 | `selftest_mutation.sh` | Five deliberate mutants prove gate 2 can actually fail |
| 8 | `gate_upstream.sh` | Upstream GXemul's own `test/` suite, run three-way |
| 9 | `gate_asan_sweep.sh` | Every machine started under AddressSanitizer, compared against upstream |
| 10 | `gate_sh_rounding.sh` | SuperH honours `FPSCR.RM` — 36 vector-mode pairs on real guest instructions, incl. two DN=0 subnormal rows |
| 11 | `gate_m88k_rounding.sh` | m88k rounding + the float→int triad + subnormal operands — 46 rows incl. swap tripwires, NaN-sign pins and a KNOWN-CHANGE flip pin |
| 12 | `gate_mips_rounding.sh` | MIPS cvt.d.l/cvt.s.l honour FCSR (arc, 11 rows) + #303 subnormal decode on BOTH rigs (pmax discriminators, arc trap control) |
| 13 | `gate_ppc.sh` | PowerPC single conversion — 54 rows on the macppc probe path: `frsp` under all four modes (each verified guest-visible through `mffs`), the ISA denormalization band, NaN payload/sign transport through both the base and indexed forms, sticky `VXSNAN`, and three pins where this fork deliberately differs from the letter |

**The strongest gate is the offline one.** `ieee_store_float_value()` is pure, so it can be
differentialled old-against-new over twenty million inputs in seconds — a stronger
instrument than any boot test, which can only observe whether a guest happened to notice.
It does not ask "did anything change"; it asserts a closed form for the change-set, which
is what makes an intended correction distinguishable from a regression.

**New in this round: the first non-MIPS rig that checks an answer.** `core/float_emul.c` is
called by the alpha, m88k, mips, ppc and sh cores, but only MIPS had ever executed it under
test. `cpus/cpu_m88k_instr.c` stores `IEEE_FMT_S` — the exact arm #287 changed — so the
OpenBSD 7.7 / luna88k rig drives the guest to a root shell and checks a computed value:
`1.5/3.0` and `sqrt(2)` must come back as `0.500000` and `1.414214`.

A SuperH rig (OpenBSD 7.6 / landisk) boots the SH4 core through a full kernel device probe
and checks a value the guest itself prints (`shpcic0 at mainbus0: HITACHI SH7751R`). It
sends **no** guest input, which is a measured decision rather than a shortcut: the emulated
SuperH console loses writes non-deterministically — on one boot, ten commands of increasing
length, and the 15, 23 and 33 byte lines ran while the 9, 17, 27 and 41 byte ones vanished
whole, with no echo and no output. That is now a bug candidate in its own right, written up
with its measurements in [`OUTSTANDING_BUGS.md`](OUTSTANDING_BUGS.md). An intermittent gate
is worse than a narrow one.

See [`regress/README.md`](regress/README.md) for the full coverage table, the gaps in the
harness itself, and what each gate does *not* prove.

## Documentation

- [`CHANGELOG.md`](CHANGELOG.md) — per-correction detail
- [`REVIEW_FINDINGS.md`](REVIEW_FINDINGS.md) — findings, severities, methodology
- [`CHANGES.patch`](CHANGES.patch) — full unified diff against upstream
- [`OUTSTANDING_BUGS.md`](OUTSTANDING_BUGS.md) — triaged / deferred items
- [`regress/README.md`](regress/README.md) — the regression harness, and what each gate does *not* prove
- [`regress/images.md`](regress/images.md) — guest images, provenance, and the per-family coverage table
- [`README`](README) / [`LICENSE`](LICENSE) — upstream's original overview, build instructions, and license, retained unchanged
