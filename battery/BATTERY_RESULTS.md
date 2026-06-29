# GXemul est/ — Regression Battery Results & Post-Analysis (2026-06-28)

Final run of the full battery on the hardened `build/gxemul` (after #1–#117). All test-only; no codebase change.

## Results matrix
| # | Machine (`-E`/`-e`) | Arch / CPU | Guest OS | Boot result | Device-attach | Post-boot depth |
|---|---------------------|-----------|----------|-------------|---------------|-----------------|
| 1 | decstation `3max` | MIPS R3000 | OpenBSD 2.2 | ✅ BOOTED multiuser | sd0/scsibus | **root + NAT ping 0% + disk dd/cksum + syslogd + reboot-persistence PASS** |
| 2 | arc `pica` | MIPS R4000 | OpenBSD 2.3 | ✅ BOOTED (→`<pccngetc>`) | jazzio | (bootcheck) |
| 3 | arc `pica` | MIPS R4000 | NetBSD 8.2 | ✅ BOOTED | 22 lines | banner+probes |
| 4 | cats | ARM | NetBSD 8.2 | ✅ BOOTED | 2 lines | banner |
| 5 | hpcmips `mobilepro770` | MIPS VR4121 | NetBSD 8.2 | ✅ BOOTED | 11 lines | banner+probes |
| 6 | sgi `o2` (IP32) | MIPS R10000 | NetBSD 8.2 | ✅ BOOTED | 21 lines | banner+probes |
| 7 | landisk | SH4 | NetBSD 8.2 | ✅ BOOTED | 14 lines | banner+probes |
| 8 | **prep `ibm6050`** | **PPC (non-macppc)** | NetBSD 8.2 | ✅ **BOOTED** | 18 lines | banner+probes |
| 9 | **luna88k `luna-88k`** | **M88K** | OpenBSD 7.7 | ✅ **BOOTED** | 9 (M88100/CMMU/le0) | banner+probes |
| 10 | macppc `g4` (7400) | PPC | NetBSD 8.2 | ⚠️ early (OF) | 46 OF lines | inert — pre-existing |
| 11 | macppc `g4plus` (7455) | PPC | NetBSD 8.2 | ⚠️ early (BATs engage) | — | HID0 gate verified |
| 12 | evbmips `malta` | MIPS | Linux 3.2 | ✅ BOOTED | 6 lines | banner+probes |

**Totals:** 12 boot configs · **5 CPU arches** (MIPS/ARM/SH4/PPC/M88K) · **3 OS families** (NetBSD/OpenBSD/Linux) · **10 BOOTED + 2 macppc-early** · `emu-crash=0`, `panic/fatal/ASan=0`, device-attach confirmed everywhere.

## Correction → validation coverage
| Changed subsystem | Corrections | Exercised by |
|-------------------|-------------|--------------|
| MIPS dyntrans / nested delay-slot | #41 #47 #90 #29 | pmax, arc, hpcmips, sgimips, malta |
| memory_rw uninit zero-fill | #95 | every boot |
| PPC core + extended BATs | #30 #46 #116 #117 | **prep** + macppc g4/g4plus |
| M88K core | #36 #46 | **luna88k** |
| SH4 core | #47 | landisk |
| ARM (READ_WORD) | #45 | cats |
| SCSI / disk / overlay | #104 #113 #114 #115 | pmax (boot-from-SCSI + disk battery + persistence) |
| Network / NAT | #102 #103 | pmax NAT ping |
| File loaders + bootblocks | many | every boot loads ELF (+ one-time fuzz corpus) |

## Post-analysis — findings
1. **No regressions.** Every guest that booted on stock 0.7 still boots on the hardened build; all 5 arches + 3 OS families green. The M88K coverage gap (cpu_m88k had zero boot coverage) is **closed** by luna88k.
2. **macppc/NetBSD-8.2 = pre-existing, proven.** Identical on the pristine baseline; #116/#117 make the extended BATs *engage* on `g4plus` (gate verified) but the skeletal OpenFirmware is the next wall — out of scope, not a regression.
3. **Positive-path depth holds.** pmax exercises disk write/read, NAT, syslog, and **survives a reboot with the written file intact + no new FFS damage** — the disk-flush path is sound.
4. **Honest limit (critical):** this battery validates the **happy path**. The guest→host bounds-check fixes (#99/#101/#102/#103/#113/#114 …) only trigger on *malicious* input a normal boot never sends — so the battery does **not** prove those guards are effective; that needs a deterministic negative/exploit-path harness (deliberately deprioritized).
5. **Coverage the battery does NOT touch:** the built-in debugger/single-step, instruction tracing, snapshot/save-restore, GUI/framebuffer guests (cobalt/dreamcast couldn't be captured headless), cross-platform builds (only WSL-gcc verified; clang-21 since added), and the test-machines.

## Shell / userland exercise (2026-06-28) — depth beyond boot, per arch
Goal: exercise userland/syscalls/console interactively on more than just the pmax rig.
| Arch | ROM (kernel) | Depth reached | Exercised |
|------|--------------|---------------|-----------|
| MIPS | pmax rig (OpenBSD 2.2, installed) | **full multiuser** | root + disk I/O + NAT + daemons + reboot-persist |
| **M88K** | luna88k (OpenBSD 7.7 `bsd.rd`) | **full `#` shell** | `sysctl hw.model`→OMRON LUNA-88K, `dmesg`→M88100/2 CMMU/le0 |
| **SH4** | landisk (NetBSD 8.2 INSTALL → `sysinst`→Utility→Run /bin/sh) | **full `#` shell** | `sysctl`→SH7751R/physmem, `dmesg`→SH4 ITLB/UTLB, wdc0 |
| PPC | prep (NetBSD 8.2 INSTALL) | boot/banner only | stalls at "PCI detection not yet implemented for dec21143" (GXemul prep PCI gap) |
| PPC | macppc (OpenBSD 3.4 `bsd.rd`) | kernel+ramdisk boot; install userland HANGS | boots *past* the OF wall that stops NetBSD (cpu0 7400, rd0 mounted, install script starts) but wedges at "erase ^?…" before the `(S)hell?` prompt — GXemul macppc skeletal-OF userland limit |
| MIPS | sgi Indy/IP2x (NetBSD INSTALL) | won't boot | GXemul IP2x partial (only o2/IP32 GENERIC boots) |
| ARM | cats (NetBSD GENERIC only) | boot only — **no shell path** | NetBSD/cats ships no INSTALL ramdisk; no local OpenBSD/cats; other ARM (netwinder/hpcarm) broken/unfetchable in GXemul |
| Linux | malta | boot only | needs a rootfs/initrd |

**Net:** deep/interactive coverage on **3 of 5 arches** — MIPS (full rig), M88K (shell), SH4 (shell) — plus
all-arch boot+device-attach. **PPC/ARM shell push (2026-06-28): confirmed blocked by pre-existing GXemul
limits**, not regressions: PPC prep stalls at unimplemented prep-PCI; PPC macppc boots kernel+ramdisk further
than NetBSD but the OpenBSD install userland hangs before the shell prompt (skeletal OF); ARM cats has no
installer ramdisk anywhere reachable. So 3/5 deep is the ceiling GXemul's machine support currently permits.
Scripts: `luna_shell.sh`, `landisk_shell.sh`, `ppc_shell.sh`; INSTALL kernels fetched from the NetBSD 8.2
archive; OpenBSD/macppc bsd.rd from the OpenBSD 3.x release archive. NetBSD `sysinst`→shell: answer
"Terminal type? [vt100]", then English (a), Utility menu (e), Run /bin/sh (a).
