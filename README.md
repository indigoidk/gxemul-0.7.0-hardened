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
