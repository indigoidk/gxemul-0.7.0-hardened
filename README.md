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

## What changed

**~268 numbered corrections** (each tagged `/* #NNN */` in the source) across ~39 review rounds,
in four themes:

1. **Guest→host memory safety & robustness** (the bulk, #1–~#154) — bound guest-controlled
   indices, lengths, and DMA in devices, file/disk loaders, the network stack, and the
   guest→host memory boundary, so an untrusted ROM, disk image, or guest cannot drive
   out-of-bounds writes into the host; guest-reachable `exit(1)`/`abort()`/host crashes become
   warn-and-continue.
2. **Hardware fidelity** (#155–#268) — accuracy to real silicon: MIPS fault-signature fidelity,
   guest-reachable host halts turned into hardware-plausible faults, R4000 FPU denormal traps,
   MIPS FPU result-correctness (div/sqrt/compare/NaN canonicalization, #254/#255), the R4030
   interval-timer rate (#257), LANCE RX-ring exhaustion signalling (#262), and a **deep NCR 53C94
   (ASC) SCSI + Jazz R4030 DMA audit** (#263–#268): DMA-accounting safety (count clamp,
   heap-disclosure), a guest-reachable `exit(1)` turned into a SCSI disconnect, FIFO-occupancy and
   chip-reset-IRQ hygiene, and R4030 translation-table / count-register bounds.
3. **Debuggability** — subsystem breakpoints, breakpoint hit-counts + "run N" (#248), data
   write-watchpoints (#250), verbosity gating, and debugger conveniences.
4. **New capabilities** — see [Feature highlights](#feature-highlights).

Every round is regression-gated: **0 errors / 0 warnings** under gcc and clang, a
multi-CPU-architecture boot sweep, and full OpenBSD 2.2 rigs on pmax (R3000) and arc (R4000)
booting to a root shell and halting cleanly. Built with an agentic multi-model workflow: each
change drafted by Claude, then adversarially reviewed to consensus by independent models (Codex
GPT-5.x, Fable, Gemini, and other cloud models) before commit.

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
| `deeb998` | Hardening / fidelity / debuggability rounds 17–25 (#155–#250) |
| `e56f54e` | Round 26 (#251/#252): console host-glue fidelity (output flush + stdin-EOF freeze) |
| `efb4eea` | CHANGES.patch: regenerate to match the SEC tree (recover missed files) |
| `4c3420b` | Round 27 (#253): `net_tap_init` — Linux tun/tap clone-device path |
| `cb85399` | README: reorganize for flow (GXemul intro, change summary, timeline, features) |
| `58ff040` | Round 28 (#254/#255): MIPS FPU result-correctness — div/sqrt via host IEEE, unified compare, NaN canonicalization |
| `7b53a4f` | Round 29 (#256): interactive-debugger MIPS breakpoint sign-extension |
| `7b53e46` | Round 30 (#257): R4030 interval timer honors the guest-programmed rate |
| `a138bd0` | Round 31 (#258): decoded STATUS/CAUSE/FCSR in the MIPS register dump |
| `eb7c406` | Round 32 (#259–#261): debugger/net QoL — implicit `-K`, net→`debugmsg`, opt-in break-on-error |
| `0b5b53e` | Round 33 (#262): LANCE RX-ring exhaustion → CSR0.MISS / descriptor BUFF + drain-fix |
| `fe3e2b6` | Round 34 (#263): ASC/R4030 DMA accounting — heap disclosure + count over-transfer |
| `2955644` | Round 35 (#264): ASC zero-length DATA_OUT host-abort → guest disconnect |
| `4c54c82` | Round 36 (#265/#266): ASC FIFO occupancy + chip-reset IRQ hygiene |
| `584c377` | Round 37 (#267): R4030 DMA translation-table limit |
| `accbcbc` | Round 38 (#268): R4030 DMA count-register width mask |
| `8758562` | Round 39: close the ASC/R4030 DMA audit — document known gaps |

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

## Documentation

- [`CHANGELOG.md`](CHANGELOG.md) — per-correction detail
- [`REVIEW_FINDINGS.md`](REVIEW_FINDINGS.md) — findings, severities, methodology
- [`CHANGES.patch`](CHANGES.patch) — full unified diff against upstream
- [`OUTSTANDING_BUGS.md`](OUTSTANDING_BUGS.md) — triaged / deferred items
- [`README`](README) / [`LICENSE`](LICENSE) — upstream's original overview, build instructions, and license, retained unchanged
