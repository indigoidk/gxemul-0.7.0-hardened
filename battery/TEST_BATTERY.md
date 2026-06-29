# GXemul est/ — Regression Test Battery

How the ~117 corrections + #116/#117 are validated against regression. Reviewed by Codex (gpt-5.5/xhigh)
+ agy (Gemini 3.1 Pro): boot battery = strong **regression** coverage (5 CPU arches × 3 OS families); the
guest→host bounds-checks themselves would additionally need negative/exploit-path tests (a separate, later
coverage frontier — current focus is regression protection of the 0.7 baseline).

## Boot battery (run on the rebuilt `build/gxemul` after every change)
| Point | Machine / guest | Arch | Validates |
|-------|-----------------|------|-----------|
| pmax rig | OpenBSD 2.2, full multiuser+root+NAT ping+halt (`reg_pmax.sh`) | MIPS R3000 | dyntrans, osiop SCSI, diskimage, net/NAT (arp/ip), dec_prom, console |
| arc | OpenBSD 2.3 → `<pccngetc>` (`arc_audit.sh bootcheck`) | MIPS R4000 | jazz ints (#69), arcbios |
| macppc | OpenBSD 3.4 (boots) + NetBSD 8.2 g4/g4plus (`reg_macppc_final.sh`) | PPC 7400/7455 | cpu_ppc, extended BATs #116/#117 |
| cats / arc / hpcmips / sgimips / landisk | NetBSD 8.2 (`reg_sweep.sh`) | ARM / MIPS×3 / SH4 | per-arch cores + machine/device setup |
| **prep** | **NetBSD 8.2 GENERIC** (`-E prep -e ibm6050`) | **PPC (non-macppc)** | **cpu_ppc on a 2nd PPC machine — #30/#46/#116/#117** |
| **luna88k** | **OpenBSD 7.7 RAMDISK** (`-e luna-88k`) | **M88K** | **cpu_m88k (#36/#46) — previously UNtested** |
| malta_lx | Linux 3.2 (mipsel) | MIPS | 3rd OS family |

`reg_sweep.sh` (8 ROMs) + the 3 OpenBSD rigs. Test kernels live in a local working dir (`<test-kernels>/`),
archived separately along with their source download URLs. macppc(NetBSD/g4) = expected
REVIEW (inert without g4plus; pre-existing OF limitation) — counts as a stable early-boot point, not a fail.

## 2026-06-28 battery expansion — candidate dispositions (Codex + agy + empirical)
Goal: add every LIVE, accessible guest on a GXemul-supported machine we did not yet test.
- **ADDED (BOOTED, wired into the sweep):** **luna88k** (OpenBSD 7.7, closes the M88K gap), **prep**
  (NetBSD 8.2, 2nd PPC machine — both engines' #1 pick for our PPC changes).
- **DEFERRED (documented-viable but no capturable output in the headless drive.py rig — their consoles are
  framebuffer/slave):** **cobalt** (MIPS; needs `-x` xterm or a disk+ISO install), **dreamcast** (SH4;
  GENERIC_MD reaches userland per docs but console is PVR/serial-not-on-stdio). Both need a framebuffer-
  console-capture rig improvement, not dead.
- **SKIP (dead / non-working in GXemul, confirmed by source + empirical + both engines):** netwinder
  (NetBSD 8.2 → endless `Exception caused no mode change pc=0xc`), mvmeppc ("mostly bogus" in
  machine_mvmeppc.c), hpcsh (skeletal, unimplemented SH opcode at 0xa0000000), sgi Indy/IP22 + Octane/IP30
  (fatal TODO paths; O2/IP32 is the supported SGI, already tested), PlayStation 2 (port removed 2009).

## Post-boot depth checks (2026-06-28, Codex + agy consensus)
Boot-to-banner alone doesn't exercise userland/disk/net. Added:
- **Device-attach assertions (in `reg_sweep.sh`):** each boot point now asserts machine-specific device
  lines (luna88k `M88100`/`CMMU`/`le0`, sgimips `crime`/`mace`, prep `pci`/`com0`, …) AND the absence of
  `panic`/`fatal error`/ASan/`Segmentation fault`/`cannot mount` — catching device-setup regressions and
  guest panics the banner-only check missed. macppc(g4) is classified `early` (OF milestone reached), not a
  fail. Validated: 8 BOOTED with device confirmation + macppc early, `bad=0` across the board.
- **pmax post-boot depth (`reg_pmax2.sh`):** beyond the original uname/id / NAT-ping / halt, now also:
  disk write+read path (`dd` 1 MB → `cksum` → read → `sync` → `cksum` stable → exercises osiop/SCSI/
  diskimage), and daemon health (`logger` → `/var/log/messages` → proves syslogd alive + a real disk
  write). Validated: root, 0% ping loss, disk cksum stable, syslogd ALIVE, clean halt, real-panic/fatal=0.

Consensus priority for FURTHER post-boot depth (not yet built): fsck-clean reboot persistence (2nd boot of
the same image); NAT TCP/UDP to host-side listeners (#102/#103 positive path); the pmax workload under ASan
(runtime memory-safety lane); RAMDISK shell smoke for luna88k/prep (`uname`/`dmesg`); snapshot save/restore
(lowest — complex, low value for the changed disk/net/device fixes). HONESTY: these catch POSITIVE-PATH
regressions; the malformed-input guards (#102/#103/#113/#114) still need the deterministic packet/device
harness — normal boot traffic never sends the bad values.

## Coverage gaps (acknowledged, lower priority than regression protection)
The bounds-check fixes for guest→host OOB (e.g. ps2_gs #99, scc #101, net_arp #102, pvr/gdrom/maple) are
only hit by a *malicious* input, which a normal boot never sends — so booting does not exercise them.
Closing that needs persistent ASan negative-corpus replay + targeted MMIO/exploit-path tests with
behavioral assertions (+ snapshot/save-restore fuzzing, CI enforcement). Tracked for future work.
