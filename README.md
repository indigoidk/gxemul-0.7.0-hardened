# GXemul 0.7.0 — hardened fork

> **⚠️ Unofficial fork — this is _not_ the official GXemul repository.**
> The official GXemul is by Anders Gavare at <https://gxemul.sourceforge.net/>.
> This fork is **not affiliated with, nor endorsed by, the original author.**

A **security‑hardened fork of GXemul 0.7.0.** It began as a harness to
**automate booting and reviewing OpenBSD 2.2/2.3** — and other guest operating
systems — across the various CPU architectures GXemul emulates (ARM, MIPS,
Motorola 88K, PowerPC, SuperH), and has since grown a series of commits that
**increase the emulator's stability and security**: chiefly guest→host
memory‑safety and robustness fixes for running untrusted ROM / disk images.

GXemul is an educational/experimental emulator, **not a security boundary** —
these are robustness/hardening fixes, not a sandbox‑escape disclosure. The first
commit is the unmodified upstream 0.7.0 baseline; the diff against it *is* the
hardening.

## What's new — OpenBSD 2.2/arc: headless bring‑up + NE2000 networking

Stock **OpenBSD 2.2/arc** (Acer PICA‑61, "Microsoft Jazz", MIPS R4000) now installs and
runs **fully headless, with networking**, on this fork — previously it hung during init
and had no usable network card. Five source changes (new `dev_ne2000.c` + four touched
files), reviewed for correctness against the guest driver and for guest→host safety:

- **R4030 interrupt routing** (`dev_jazz.c`) — the Jazz `EXT_IMASK` register is now routed
  as CPU‑IP‑level interrupt enables (local‑bus → IP3, ISA bridge → IP4, interval‑timer →
  IP6) instead of being ANDed against Jazz device line numbers. That bit‑space mismatch
  left the hardclock and keyboard interrupts undelivered, hanging init in its idle loop.
- **Headless VGA text console** (`machine_arc.c`) — the PICA's on‑board S3 VGA console is
  always wired; without X11 it mirrors the 80×25 text screen to stdout and reads the PC
  keyboard from stdin, so the machine is fully drivable headless. The `-X` path is unchanged.
- **ARC firmware fixes** (`arcbios.c`) — advertise the video/keyboard console when headless,
  and emit the kernel boot path (`argv[0]`) in the value‑only, lowercase form OpenBSD's
  `makebootdev` expects, so the root device auto‑detects instead of dropping to a prompt.
- **NE2000 network card** (new `dev_ne2000.c`, attached on the ISA bus at port 0x280 / irq
  9) — a DP8390 / NE2000 (16‑bit) NIC that OpenBSD/arc's stock `ed0` driver drives. It is
  pure programmed‑I/O against a host‑private 16 KB ring buffer (no bus‑master DMA into guest
  RAM), and **every on‑card memory access is bounds‑clamped**, so guest‑programmable indices
  (remote‑DMA pointer, ring page pointers, transmit length) cannot escape the device's own
  buffer — consistent with this fork's guest→host safety charter. Result: `ed0` probes as
  NE2000, `ifconfig` brings it up, and it pings the emulated NAT gateway at **0% packet loss.**

The review found and fixed two real defects before merge: an RX ring page‑count off‑by‑one
(the received‑length reconstruction fails for certain frame sizes without reserving the
trailing FCS) and a lost‑interrupt race (the ISA bridge's EOI can clear a still‑pending
level, so the interrupt line is re‑asserted while the level is high rather than only on its
edge). Both are covered by a packet‑size ping sweep in the regression run.

## What's new — 2026 review rounds (#120–#154)

Two further rounds since the initial hardening publication:

**🔒 Security — a whole‑codebase multi‑model review (#130–#154).** A fresh review of the
*entire* core — the four CPU instruction cores, the dynamic‑translation engine, the
guest→host memory boundary, the file loaders, network, disk, debugger, and the
highest‑risk devices — using parallel Claude review agents, cross‑checked by three
independent cloud models (**GLM, DeepSeek‑V3, Qwen3‑Coder**), then adjudicated against
the source. **~23 confirmed fixes, every one pre‑existing in the baseline** (the earlier
pass simply had not reached them):
- **CRITICAL — MIPS `memset` combiner (#137).** A guest‑controlled `bzero`/`memset` loop
  with *end < start* underflowed an unsigned length **and** wrapped the page‑boundary
  clamp, driving a multi‑gigabyte `memset` straight into the host heap. Reachable from any
  MIPS guest (e.g. pmax). Fixed with a fall‑back to the safe path.
- **HIGH — PVR framebuffer (#145).** Oversized guest display geometry let the framebuffer
  refresh write past the fixed host framebuffer allocation — a guest→host heap overwrite.
  Now clamped to the host framebuffer.
- **HIGH — S‑record loader (#149).** A malformed `count` field drove a ~4 KB over‑read of
  the host stack into guest‑visible memory. Now clamped to the parsed record length.
- …plus a medium/low tail: an unbounded guest‑set SCSI transfer size (OOM‑exit DoS), a TCP
  timestamp‑option over‑read, several guest‑reachable `exit(1)` paths converted to
  warn‑and‑continue, `free()` on an `mmap`‑backed allocation, integer/format‑string
  hardening, and undefined‑behaviour cleanups. The dynamic‑translation engine, the memory
  boundary, and the prior loader hardening were **re‑confirmed sound** (no OOB).

**✨ Features (#120–#129).** SuperH unaligned‑access exceptions + 64‑bit `fmov` alignment;
multi‑track CUE/BIN CD‑image support; testmips RAM above 256 MB; subsystem‑level debug
breakpoints; and several debugger conveniences (step‑into‑call, expression fixes,
dump/disassemble spacing).

Every fix is regression‑gated — a multi‑architecture boot sweep plus the full OpenBSD/pmax
rig (boot, root shell, NAT, disk, clean halt) — and the tree still builds at **0 errors /
0 warnings.** Per‑fix detail: [`CHANGELOG.md`](CHANGELOG.md) ·
[`REVIEW_FINDINGS.md`](REVIEW_FINDINGS.md) · [`CHANGES.patch`](CHANGES.patch).

## Highlights

**🔒 Security — guest→host memory safety (most critical)**
An untrusted guest, ROM, or disk image could drive out‑of‑bounds writes into the
*host* process. Fixed across device, firmware, disk and network paths — e.g.:
- **GS** (`dev_ps2_gs`, #99) — 64‑bit OOB heap write past `reg[264]`
- **SCC serial** (`dev_scc`, #101) — ~8 KB OOB heap write past `scc_register_w[32]`
- **NAT/ARP** (`net.c`, #102) — ~65 KB guest frame overflowing a 74‑byte reply buffer
- **OpenFirmware `set-colors`** (`of.c`, #48) — unbounded palette index (reproduced SEGV)
- **SCSI DATA_OUT** (`dev_osiop`, #49) — unbounded DMA heap write
- **PixelStamp DMA** (`dev_px`, #89) — negative width → host stack overflow
- …plus ~20 more bounded device OOB writes (framebuffers, ADB, palettes, MEC, PVR, PCC2 …)

**✨ Feature — PowerPC 745x extended BATs**
New `MPC7455` CPU model and `-e g4plus` macppc subtype, with IBAT4‑7/DBAT4‑7
support (HID0[HIGH_BAT_EN]‑gated). Purely additive — `-e g4`/g3/g5 untouched.

**🐛 Robustness / bug fixes**
- **No guest‑triggered host crashes** — SCSI‑engine faults that reached `exit(1)`/NULL‑deref now warn and stop the local engine instead of killing the emulator (`dev_osiop`, #114/#118)
- **"Warn loudly, never silently mask, never crash"** — an emulator‑wide course‑correction so every security clamp is visible (rate‑limited `fatal()`), matching the author's error‑handling style while keeping all bounds
- **arc/Jazz interrupt mask (#69)** — correctness fix that lets OpenBSD/arc boot

## What's new — cross-model re-review (#182–#187): a framebuffer‑resize heap bug

A whole‑tree adversarial re‑review — **Codex GPT‑5.6‑sol/ultra** plus a four‑reviewer **Claude Fable** panel, each
finding source‑verified — turned up a **CRITICAL guest→host heap‑overwrite the earlier passes had missed:**

- **CRITICAL — framebuffer resize left a stale device length (#182).** On a framebuffer *shrink* (e.g. an SGI O2
  guest reprogramming the GBE resolution), `dev_fb_resize()` swapped the framebuffer pointer but left the
  memory‑mapped device's registered *length* at the old, larger value — so the dyntrans fast‑map path (added in
  #155) installed a writable host mapping past the end of the new, smaller allocation. Latent in pristine upstream.
  Fixed by keeping the device length in sync on resize.
- **HIGH — X11 image allocation overflow (#183).** On X11 builds a guest‑reachable resize could overflow the 32‑bit
  `int` used to size the XImage buffer (within the existing 16384/axis cap), under‑allocating it and then
  overrunning it on redraw. Widened to `size_t`.
- **guest‑reachable `exit(1)` DoS conversions (#184 / #186 / #187)** — framebuffer, MB89352 SCSI, and eight PowerVR
  MMIO register paths converted to log‑and‑continue, per this fork's #118/#119 ethos.

This round is notable methodologically: the four‑reviewer panel (partitioned by subsystem) independently judged the
memory‑safety surface clean, but #182 lives in the *seam* between two reviewers' areas — the holistic single‑context
Codex pass is what caught it. Remaining Codex medium/low findings (a CUE symlink‑follow, a cross‑memblock
invalidation gap, and others) are triaged in [`OUTSTANDING_BUGS.md`](OUTSTANDING_BUGS.md). Applied to both the `est/`
and `GXEMUL-SEC/` trees; gcc 15.2.1 at 0 errors / 0 warnings.

## Provenance — how this was built

Developed with an **agentic, multi‑model workflow.** Each change was drafted by
Claude (Opus 4.8), then put through **independent adversarial code review by two
other models — Codex (GPT‑5.5) and agy (Gemini 3.1 Pro) — to consensus** before
commit, and validated against a regression battery: boot across **5 CPU
architectures**, a full **OpenBSD/pmax** multiuser rig (root, NAT, disk, daemons,
reboot‑persistence), and **OpenBSD/luna88k** (M88K) + **NetBSD/landisk** (SH4)
interactive shells — with **gcc and clang both at 0 errors / 0 warnings.** The
full findings, severities, and review trail are in
[`REVIEW_FINDINGS.md`](REVIEW_FINDINGS.md).

---

Per‑fix detail: [`CHANGELOG.md`](CHANGELOG.md) · [`REVIEW_FINDINGS.md`](REVIEW_FINDINGS.md).
Upstream's original overview, build instructions and license are retained
unchanged in [`README`](README) and [`LICENSE`](LICENSE).
