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

**~253 numbered corrections** (each tagged `/* #NNN */` in the source) across ~27 review rounds,
in four themes:

1. **Guest→host memory safety & robustness** (the bulk, #1–~#154) — bound guest-controlled
   indices, lengths, and DMA in devices, file/disk loaders, the network stack, and the
   guest→host memory boundary, so an untrusted ROM, disk image, or guest cannot drive
   out-of-bounds writes into the host; guest-reachable `exit(1)`/`abort()`/host crashes become
   warn-and-continue.
2. **Hardware fidelity** (#155–~#250) — accuracy to real silicon: MIPS fault-signature fidelity,
   guest-reachable host halts turned into hardware-plausible faults, R4000 FPU denormal traps.
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

## Documentation

- [`CHANGELOG.md`](CHANGELOG.md) — per-correction detail
- [`REVIEW_FINDINGS.md`](REVIEW_FINDINGS.md) — findings, severities, methodology
- [`CHANGES.patch`](CHANGES.patch) — full unified diff against upstream
- [`OUTSTANDING_BUGS.md`](OUTSTANDING_BUGS.md) — triaged / deferred items
- [`README`](README) / [`LICENSE`](LICENSE) — upstream's original overview, build instructions, and license, retained unchanged
