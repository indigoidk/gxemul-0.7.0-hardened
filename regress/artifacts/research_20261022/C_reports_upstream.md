# GXemul: what was published upstream and in bug reports, checked against our fork

**Scope.** Published bug reports, advisories and upstream development for GXemul. GitHub forks and distro patch sets are left to the other agents; they come up here only where a bug report points at them.
**Date:** 2026-10-22. **Fork baseline:** `GXEMUL-SEC` HEAD `de8c7547`, with source read from `GXEMUL-SEC/src/`. **Pristine reference:** the upstream 0.7.0 tarball, downloaded and checked against the published SHA256 (`79c4437c…8e83`).
**Method.** Every web source listed below was fetched. Every defect claimed to affect our fork was checked by reading the fork's source at the cited `file:line`. Nothing under `GXEMUL-SEC/` or the project root was written.

Downloaded material is in `C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-cc-GXEMUL\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\ghresearch\reports\`:

| File or folder | Contents |
|---|---|
| `dl_trunk\gxemul-trunk.tar.gz` | The trunk snapshot |
| `dl_070\gxemul-0.7.0.tar.gz` | The 0.7.0 release |
| `x_trunk\`, `x_070\` | Both, unpacked |
| `trunk_src.diff` | Full source diff from 0.7.0 to trunk (7,724 lines) |
| `trunk_HISTORY.diff` | Upstream changelog diff |
| `sf\diffs\r6519.diff` … `r6577.diff` | One diff per SVN commit, taken from SourceForge's per-commit diff view |
| `sf\all_msgs.txt`, `sf\ml_index.txt` | All 161 mailing-list messages, plus an index |
| `netbsd\` | NetBSD bug reports (GNATS PRs) and pkgsrc patches |
| `distro_bugs\`, `other_emus\`, `upstream_site\` | Supporting pages |

---

## Headline

1. **There is no CVE, OSV or NVD record for GXemul.** NVD returns 0 results for `gxemul`, `GXemul`, `mips64emul` and `gavare`; OSV returns nothing for Debian, Ubuntu or Alpine. I found no academic paper that fuzzed or audited GXemul, and no Stack Exchange or OSDev forum threads.
2. **Upstream development did continue after 0.7.0, but it was never released.**
   - SourceForge's "Code2" SVN repository has **56 commits after the release (r6522–r6577, 2021-04-26 → 2023-04-10)**.
   - The homepage's file listing has an unreleased snapshot, `src/gxemul-trunk.tar.gz`. It was last modified **2025-11-19** (6,001,434 bytes) and its newest source files are dated 2023-08-05.
   - The snapshot's own release notes call it **"0.7.0.1"** ("Updated installation guides…", "Some minor 88K specific fixes").
   - The marker file `LATEST_IS_0.7.0` is still present.
   - The commit pages for r6532 and r6577 list only 25 changed files each (SourceForge truncates the list), and the tarball also carries cleanup edits from July 2023. So the full tarball diff is the authoritative record, and the SVN commits are used only to say *why* each change was made.
3. **Our fork already knew of two upstream post-0.7.0 changes, and has improved on both:** `tcnd` (#307) and REGIMM (#309). Both CHANGELOG entries mention "the abandoned 0.7.1 line". Nothing in the fork records a full triage of the post-0.7.0 commits; this report is that triage.
4. **Totals.**

   | Group | Count |
   |---|---|
   | Rows in the findings tables | 61 (30 from upstream code, 31 from bug reports) |
   | **Still open in our fork** | **19** |
   | — of those, already recorded by the fork | 5 (`lunadefaultstop`, `pvrrenderexit`, `ctorabortclass`, `m88kpsrmxm`, `b120`) |
   | — of those, new to the fork's records | 14 |
   | Unverified | 2 |
   | Already fixed, not applicable, or feature notes | the rest |

---

## (a) Sources checked

| # | Source | URL | Coverage | Result |
|---|---|---|---|---|
| S1 | Upstream homepage | https://gavare.se/gxemul/ | current | No news section. Says "only occasionally updated". Links a mail with a workaround for the 0.7.0 Linux build |
| S2 | Upstream download listing | https://gavare.se/gxemul/src/ | to 2025-11-19 | **`gxemul-trunk.tar.gz`** (Last-Modified 2025-11-19) and `LATEST_IS_0.7.0`. The 0.7.0 SHA256 matches. No 0.7.0.1 or 0.7.1 tarball exists |
| S3 | Upstream trunk documentation online | https://gavare.se/gxemul/gxemul-trunk/doc/RELEASE.html, …/HISTORY.html, …/doc/TODO.html | 2025-11-19 | Calls itself "0.7.0.1". Identical to the tarball |
| S4 | SourceForge SVN "Code2" commit log, with per-commit diffs | https://sourceforge.net/p/gxemul/code2/HEAD/log/ | r6519–r6577 (2021-04-22 → 2023-04-10) | Fully triaged. The older "Code" repository and raw file views are behind a Cloudflare challenge; the per-commit diff view was not |
| S5 | SourceForge mailing lists `gxemul-users` and `gxemul-devel` | https://sourceforge.net/p/gxemul/mailman/ | 2008-03 → 2023-03 (64 monthly pages, 161 messages) | Every defect thread was read; see the R rows |
| S6 | NVD API | `services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch=` | all | **0 CVEs** for all four keywords |
| S7 | OSV.dev API | `api.osv.dev/v1/query` | Debian, Ubuntu, Alpine | **No records** |
| S8 | cve.org | `cveawg.mitre.org` | — | The API requires authentication. NVD mirrors every CVE ID, so this is covered by S6 |
| S9 | NetBSD bug database (GNATS), "gxemul" | `gnats.netbsd.org/cgi-bin/query-pr-list.pl?text=gxemul` | 2006–2021, 18 PRs | PR 54114 and PR 54252 are about GXemul; the others are guest-side NetBSD bugs |
| S10 | NetBSD wiki page for cats under GXemul, and the NetBSD emulator matrix | https://wiki.netbsd.org/ports/cats/gxemul_cats/, https://www.netbsd.org/ports/emulators.html | to 2026 | 0.7.0 cannot boot NetBSD/cats builds made with GCC ≥ 10 without a pkgsrc patch. The matrix also carries stale notes for evbarm, prep and dreamcast |
| S11 | pkgsrc patch files (opened only to compare with the bug reports) | https://ftp.netbsd.org/pub/pkgsrc/current/pkgsrc/emulators/gxemul/patches/ | 2021–2026 | Patches for the ARM carry flag, ARM `udf`, removing the ARM OpenFirmware word, and SH4-A `synco` (2026-04). Distro patch sets belong to another agent |
| S12 | Debian bug tracker, `src:gxemul` | https://bugs.debian.org/cgi-bin/pkgreport.cgi?src=gxemul;archive=both | 2006–2023, 14 bugs | All archived. #609082, #574537 and #1032471 are covered in the R rows |
| S13 | Ubuntu Launchpad | https://bugs.launchpad.net/ubuntu/+source/gxemul/+bugs | 4 bugs | #301041 (`gxemul a` segfault, 2008) |
| S14 | Gentoo Bugzilla | https://bugs.gentoo.org/976428 | 2026-05-31 | Build fails under GCC 16 (`s_nlnno`) |
| S15 | FreeBSD Bugzilla | bugs.freebsd.org | — | Blocked by a bot challenge. Web search found only port-update PRs (81048, 123870) |
| S16 | HelenOS bug tracker | https://www.helenos.org/query?summary=~gxemul and ticket #362 | 2009–2012 | Tickets #24, #161, #347 and #454 are HelenOS-side bugs. **#362 records a GXemul interrupt-delivery problem** |
| S17 | virtuallyfun blog, "GXemul for Win32" | https://virtuallyfun.com/2019/08/05/gxemul-for-win32/ | 2019 → 2025 comments | Portability and mouse-tracking issues only (features) |
| S18 | barebox mailing list; FreeBSD wiki page on MIPS emulation | https://lists.infradead.org/pipermail/barebox/2015-February/022410.html, https://wiki.freebsd.org/MipsEmulation | 2015–2018 | Malta: PCI-enabled barebox hangs; big-endian Malta and a Malta NIC are unsupported (features) |
| S19 | Academic and fuzzing literature (web searches) | — | — | **Nothing GXemul-specific** |
| S20 | Stack Overflow, Stack Exchange, OSDev forum (web searches) | — | — | **Nothing found** |
| S21 | Other emulators reusing GXemul code: MAME `omron/luna_88k.cpp` and `sega/dccons.cpp` (raw source), nono (the LUNA emulator), QEMU mailing lists | raw.githubusercontent.com/mamedev/mame, web searches | — | **No reuse found.** MAME's drivers do not mention GXemul, and nono is an independent implementation. HelenOS and NetBSD's automated test runs *use* GXemul but carry no device code |
| S22 | OpenBSD lists (marc.info), port-pmax / port-hpcmips / port-landisk lists | web searches | — | Nothing GXemul-defect-specific. The only port-pmax hit, "Crashing 5000/240" (2017), concerns real hardware |

---

## (b) Findings

Status key:

| Status | Meaning |
|---|---|
| **FIXED** | Already fixed in our fork; the evidence is cited |
| **OPEN** | Still open in our fork and not in its records |
| **OPEN (filed `x`)** | Still open, and already recorded in the fork's bug file or ledger under `x` |
| **N/A** | Not applicable |
| **UNVERIFIED** | Could not be decided by reading the source |

Unless a row says otherwise, fork citations are to `GXEMUL-SEC/src/`.

### B1. Upstream code after 0.7.0 (SVN r6522–r6577, plus the 2023 cleanup in the tarball)

| ID | Commit and date | What changed upstream | Category | Status in our fork, with evidence |
|---|---|---|---|---|
| U1 | r6557 (2021-05-08), r6562 (2021-05-09) | When memory is written, or a page is mapped writable, upstream now discards the cached translated code for that page on **all** CPUs, not just the CPU that wrote. HISTORY: "Improved SMP stability" (LUNA-88K with 4 CPUs). r6562 also null-checks each CPU's discard routine | CORRECTNESS | **OPEN.** `cpus/memory_rw.c:752-760` discards only the writing CPU's translations (`cpu->invalidate_code_translation(cpu, …)`). **Two caveats before porting.** (1) The upstream loop dereferences `machine->cpus[ci]`. In our fork `cpus[]` is filled only *after* each CPU constructor returns (`core/emul.c:492-503`), so the three stores made inside constructors would dereference NULL: `cpus/cpu_alpha.c:101`, `cpus/cpu_arm.c:184-188`, `cpus/cpu_mips.c:294-304`. That is why upstream removed or moved exactly those three (r6564, r6573, r6577). (2) The fix is partial. When a CPU translates a page, it revokes fast-path write access only in its own tables (`cpus/cpu_dyntrans.c:820-828`, the same in trunk). Another CPU that already holds a writable fast-path mapping still bypasses `memory_rw`. A complete fix also has to broadcast that revocation to all CPUs |
| U2 | r6564 (MIPS), r6573 (ARM, = pkgsrc `patch-src_cpus_cpu__arm.c`, 2021-09-05), r6577 (Alpha) | Removed or relocated guest-memory stores made inside the CPU constructors ("Storing to memory is not allowed until the CPU has initialized completely"; the ARM OpenFirmware code "is not currently in use by any machine") | CORRECTNESS / prerequisite for U1 | **OPEN.** All three stores remain (lines as in U1). The ARM one writes the word `0xef8c64be` at top-of-RAM−8 on every ARM machine with PROM emulation. That word is the "magic" software-interrupt instruction (SWI) that routes to `of_emul()` and its `exit(1)` (`promemul/of.c:1098-1101`; our fork filed this as `ofemulnodata` on 2026-10-21). Upstream's own statement that ARM OpenFirmware is unused supports our fork's planned fix of gating the magic SWI in the instruction decoder |
| U3 | r6568 (2021-05-24) | An unimplemented MIPS REGIMM instruction now raises a Reserved Instruction exception instead of stopping the emulator | CRASH (emulator stop) | **FIXED** #309, `cpus/cpu_mips_instr.c:5372-5412`. The comment there cites "the 0.7.1 line it never released" |
| U4 | r6572 (2021-08-29, Nick Hudson) | ARM `udf` (permanently undefined) now raises the undefined-instruction exception | CRASH (emulator stop) | **FIXED, more generally**: #312, `cpus/cpu_arm_instr.c:4690-4749` routes *all* undecodable encodings in that space to the undefined-instruction exception, including when the condition fails. Disassembly of `udf` was not added; cosmetic only |
| U5 | r6576 (2021-08-30, Nick Hudson); the same patch is pkgsrc `patch-src_cpus_cpu__arm__instr__dpi.c`. The NetBSD wiki says 0.7.0 cannot boot NetBSD/cats ≥ 10.0 (GCC ≥ 10) without it | ARM carry flag for CMP, RSB, SUB, RSC and SBC: `a >= b` replaced by `c32 == c64` | CORRECTNESS | **FIXED** #311, `cpus/cpu_arm_instr_dpi.c:289-303` (the same expression). Our fork also fixed the ADC overflow flag (#313) |
| U6 | r6523, r6541 (2021-04-26/28) | 88K `tcnd ne0,r0,x` treated as a no-op; typo fix | CRASH (emulator stop) | **FIXED, more completely** #307, `cpus/cpu_m88k_instr.c:2483-2520` (the full condition mask; the upstream special case was rejected as insufficient) |
| U7 | r6577 (2023-04-10) | Adds the 88K register-form **signed `sub`** (opcode 0x74, with an integer-overflow trap; `X(sub)`, trunk `cpu_m88k_instr.c:695-710`) | CRASH (emulator stop on a legal instruction) / CORRECTNESS | **OPEN.** The fork's register-form decoder (`cpus/cpu_m88k_instr.c:3660-3716`) handles 0x70 `add` but not 0x74. It falls to `default: goto bad` (`:3815`), and the shared `bad` label clears `cpu->running`. **The carry variants `add.ci/.co/.cio` (0x71–0x73) and `sub.ci/.co/.cio` (0x75–0x77) are missing in both trunk and our fork**, although our fork's own comment at `:3735-3738` names them. All are documented MC88100 instructions, usable at any privilege level (`_scratchpad/mc88100.txt:6021-6069` for `sub`, `:3844` for `add.cio`) |
| U8 | r6542 (2021-04-29), r6547 (2021-05-02) | 88K bus-error reporting. When a device refuses an access, `memory_rw` now sets the memory-management unit's fault status register to "bus error" (`PFSR = BERROR<<16`) and its fault address register (`PFAR = paddr`), with a NULL check, before raising the exception. The LUNA probe address 0x3ffffff0 also sets PFAR, then becomes a `DEV_RAM_FAIL` device that raises a real data-access exception | CORRECTNESS | **OPEN.** `cpus/memory_rw.c:603-624` raises `m88k_exception(DATA/INSTRUCTION_ACCESS)` without writing PFSR or PFAR. `devices/dev_luna88k.c:624-627` sets PFSR only, writes no PFAR, and returns success with no exception. **Our fork has already measured the consequence**: `regress/artifacts/vmedefaultkill/measure_20261009/` (CHANGELOG `7n-4`) shows a fault delivered to the OpenBSD 2.2/mvme88k guest arrives "with … the data CMMU's PFSR still 0 … so `trap.c` … reaches `panictrap()`". Every FAULT disposition our fork uses on 88K therefore delivers a bus error that is not well formed. This includes #568 `vmedefaultkill`, population 1 |
| U9 | r6544, r6546, r6550 + 2021-05-03 (`dev_mb89352.c`, the LUNA-88K SCSI controller) | (a) The bus-free interrupt (`PCTL_BFINT_ENAB`) is implemented. (b) The command byte (SCMD) is decoded from bits 7:5, which adds `RST_ATN`/`SET_ATN` and accepts transfers without `PROG_XFR`. (c) Writes to PSNS now go to the diagnostics register (SDGC) instead of being stored. (d) 32-bit reads at offset 0 are accepted (the OMRON MACH OS probes this way). (e) Nine `cpu->running = 0` stops removed | CORRECTNESS + CRASH (emulator stop) | **OPEN (partly filed).** (a) `devices/dev_mb89352.c:107` is still a TODO and is not in the fork's records. (b) `:364` still does `switch (idata)` on the whole byte, and `:409-410` accept only transfers with `PROG_XFR`. The fork filed only the *halting* half (`qhmbunimplstops`), not the decoding fault. (e) is filed as `qhm88kstops` / `qhmbphasestops` / `qhmbunimplstops` / `qhmbbufendstops`. **Warning: trunk did not stop halting here.** Trunk's `debugmsg()` now stops the CPU on *every* error-level message by default: the `skip_print` block, breakpoint level `VERBOSITY_ERROR` for every subsystem. Our fork deliberately rejected that design in #261 (opt-in, off by default). So upstream's (b), (c) and (d) are valid evidence for correct decoding, but its (e) is not evidence that the stops can simply be removed |
| U10 | r6542, r6552 (`dev_luna88k.c`, 2021-05-04) | Per-CPU resets `RESET_CPU0..3` (0x6d000000–0x6d00000c) are modelled, limited by `ncpus`. The default case no longer stops the CPU. The interrupt-mask `exit(1)` became a message. Absent CPUs' memory-management-unit windows are mapped as plain RAM | CRASH (emulator stop) | **OPEN (filed `lunadefaultstop`, MED).** A write to `RESET_CPU0..3` falls into the default case at `devices/dev_luna88k.c:909-924` and stops the CPU; only `RESET_CPU_ALL` is handled (`:904-907`). The registers are already defined in `include/thirdparty/luna88k_board.h:113-116`. The `exit(1)` on low interrupt-mask bits is **FIXED** (#438). **Do not copy the plain-RAM mapping for absent CPUs**: a guest probing for a memory-management unit would then find one that does not exist |
| U11 | r6577 (2023-04-10, `dev_pvr.c`) | The "no zwrite? not implemented" `exit(1)` is commented out; rendering continues with Z writes enabled | CRASH (host process exit) | **OPEN (filed `pvrrenderexit`, HIGH).** `devices/dev_pvr.c:1243-1246`. The `zwrite` bit comes from a guest-written graphics display-list word (bit 26, `:1225`). Upstream's choice is a tested fix shape for one of the four sites |
| U12 | r6577 (`promemul/dreamcast.c`) | GD-ROM BIOS call `r7 = 8` (`GDROM_ABORT_COMMAND`) is accepted as a no-op | CRASH (emulator stop) | **OPEN, not filed.** `promemul/dreamcast.c:303-323`: any `r7` other than 0–4 does `goto bad`, which clears `cpu->running` at `:382-388`. A legitimate Dreamcast BIOS call stops the emulated CPU. The sibling syscall groups at `:268` and `:295` stop it the same way |
| U13 | r6577 (`dev_dreamcast_gdrom.c`) | GD-ROM register offset 0x98 silently ignored | CORRECTNESS | **FIXED, more generally** (#461): `devices/dev_dreamcast_gdrom.c:1341-1357` declines every unimplemented offset, reading 0, with one message per offset and direction |
| U14 | r6577 (`machine_alpha.c`) | DEC 3000/300: the serial controller's interrupt changes from `irq=0` to `irq=machine[0].cpu[0]` | CRASH (host process abort at machine construction) | **OPEN (filed `ctorabortclass`; ASAN-sweep exemption until 2026-11-30, `regress/gate_asan_sweep.sh:176`).** `machines/machine_alpha.c:70-71`. Upstream's string names the interrupt the Alpha CPU registers under `cpu->path` (`cpus/cpu_alpha.c:114-125`; `cpus/cpu.c:74-75` builds it as `"%s.cpu[%i]"`). Build it as `"… irq=%s …"` from `cpu->path` rather than the literal, so it still works when the 3000/300 is not machine 0 in a configuration file |
| U15 | July 2023 (`cpu_mips_coproc.c`) | (a) Out-of-bounds index `reg[fd+1]` → `reg[(fd+1)&31]`. (b) Floating-point divide by zero: `fabs > 1e-11` → `!= 0`, now raising a floating-point exception. (c) `trunc.l/.w` really truncate. (d) `memset(float_value)`. (e) COP0 RANDOM uses a deterministic pseudo-random generator | BOUNDS / CORRECTNESS | **FIXED.** (a) #226 (`cpus/cpu_mips_coproc.c:1220-1228`, `:1426-1433`). (b) #254 (`:1345-1362`). Our fork's plain IEEE result is better than trunk's *unconditional* floating-point exception, which is only correct when the divide-by-zero trap is enabled; do not copy that. (c) Truncation toward zero (`:1613-1633`). (d) Our fork reads `float_value[1]` only on two-operand paths: N/A. (e) See U25. **Trunk still divides by zero when the guest sets WIRED ≥ the TLB size, which our fork fixed in #190 (`:1941-1950`)** |
| U16 | r6532 (2021-04-27, `cpu_alpha_instr_loadstore.c`) | A failed Alpha load or store no longer calls `exit(1)` | CRASH (host process exit) | **FIXED** #215 (`cpus/cpu_alpha_instr_loadstore.c:68-74`, `:112-118`) |
| U17 | July 2023 (`cpu_m88k.c`) | Setting PSR.MXM (misaligned-access mode) still stops the CPU (`#if 1`), with a clearer message | CRASH (emulator stop) | **OPEN (filed `m88kpsrmxm`, MED).** `cpus/cpu_m88k.c:542-547`. **Upstream offers no fix** |
| U18 | r6531 (2021-04-27) | Build rule: `cpu_alpha.o` now depends on the generated `tmp_alpha_misc.c` | OTHER (build correctness) | **OPEN.** `cpus/Makefile.skel:24-25` lacks the dependency (the generated file is included at `cpus/cpu_alpha_instr.c:742`). This is direct evidence for the fork's filed question `depsrm`, whose filing names generated `tmp_*.c` files as "the case most likely to still need" the `rm` |
| U19 | r6533, r6535 (2021-04-27/28); mail of 2021-04-28 | Removed the `#define __attribute__(x)` / `__noreturn__` overrides from the third-party headers. They broke the 0.7.0 link on Linux (`__cmsg_nxthdr` multiple definition) | OTHER (build) | **FIXED** (`include/thirdparty/bootblock.h:132`, `dp83932reg.h:15`, `pcireg.h:15`, `sgi_arcbios.h:17`) |
| U20 | r6575 (2021-08-30) | The ARM memory-fault message moved to debug verbosity | OTHER (log flood / throughput) | **OPEN.** `cpus/memory_arm.c:261-266` prints two lines for *every* guest page fault unless `-q` is given. Our fork's own measurement of the equivalent MIPS flood in #278 found a 70–140× throughput loss. Compare also `armvecrecurse`: 47,591 such lines before the host crashed |
| U21 | r6532 (`cpu_ppc.c`) | The "PPC Exception" print became an info-level debug message that can be filtered per subsystem | OTHER (log flood) | **OPEN.** `cpus/cpu_ppc.c:329-331` prints one line per guest exception, decrementer ticks included, unless `-q` is given |
| U22 | r6532/r6555 (`emul.c`) | Console and X11 output are flushed every 50 ms of wall-clock time instead of every 2^19 instructions executed by the boot CPU | CORRECTNESS (low) | **OPEN.** `core/emul.c:1019-1024`. If the boot CPU stops while other CPUs keep running, console and X11 polling stops; the idle path at `:999-1017` covers only the case where every CPU is idle |
| U23 | r6537 (2021-04-28) | A just-translated instruction is not executed if a debug message has requested single-stepping | OTHER (debugger) | **N/A.** Our fork's subsystem breakpoints are an independent design (#259–#261, #270). Low |
| U24 | r6532, r6555, r6570 | Breakpoint refactor: hit counting, print-instead-of-break, `-T` as a memory-subsystem breakpoint | FEATURE | **N/A.** Our fork has its own equivalent: #248 (hit and ignore counts), #259–#261. Trunk's abort-on-error-by-default policy is the one our fork rejected |
| U25 | r6563 (2021-05-09) | COP0 RANDOM uses a seeded xorshift64* generator instead of host `random()` (fixes an OpenBSD linker warning and gives determinism) | OTHER | **OPEN** (low): `cpus/cpu_mips_coproc.c:1949` |
| U26 | r6569 | `strlcpy(..., sizeof field)` in the Alpha HWRPB setup | OTHER | **N/A**: the fields are `rpb_magic[8]` and `rpb_ssn[16]` (`include/thirdparty/alpha_rpb.h:55`, `:63`), so the existing sizes 8 and 10 are in bounds |
| U27 | trunk `TODO.html` (Juli Mallett) | "diskimage__internal_access now always returns success, even if trying to read past end of image", so a disk-size binary search on testmips never ends | CORRECTNESS | **FIXED** #416. `disk/diskimage.c:1591-1601` rejects reads past the advertised capacity, and testmips propagates the status (`devices/dev_disk.c:151-157`) |
| U28 | r6559 (`dev_m8820x.c`) | Memory-management-unit flush commands discard only the affected pages; SAPR/UAPR writes discard translations only when the value changes | OTHER (performance) | **N/A, by design.** Our fork's #434/#435 made measured, deliberate choices here. Trunk's "only when changed" guard is the very mutant shape the fork's detector is built to catch |
| U29 | r6541, r6549, r6556 | 88K memset/memcpy loop fast paths (claimed ~200× on memset-heavy code) | FEATURE (performance) | Not in our fork. See C3 for the hazards in porting them |
| U30 | r6532 (`console.c`) | `fflush(stdout)` in `console_deinit_main()`; Ctrl-T prints a status summary | OTHER | `console/console.c:141-149` has no flush. Normal `exit()` flushes anyway; this matters only on abnormal termination. Low |

### B2. Published bug reports: mailing lists, NetBSD PRs, trackers, blogs

| ID | Source and date | Defect | Area of GXemul | Category | Status in our fork, with evidence |
|---|---|---|---|---|---|
| R1 | gxemul-devel, 2018-08-08 (Andreas Gustafsson), msg 36392903 | MIPS `DIV`/`DDIV` with INT_MIN / −1 crashes the host with SIGFPE | `cpu_mips_instr` div/ddiv | CRASH | **FIXED** upstream 2018-08-19, inherited: `cpus/cpu_mips_instr.c:1839`, `:1863` |
| R2 | gxemul-devel, 2019-03-03 (Gustafsson), msg 36604666 | Console output lost because SIGALRM interrupts `write()`; fix is `SA_RESTART` | `timer.c` | CORRECTNESS | **FIXED** (`core/timer.c:333`) |
| R3 | gxemul-devel, 2019-03-21 (J. Nilsson), msg 36618359 | ARM `SBCS` does not set the overflow flag (carry-in sense inverted) | `cpu_arm_instr_dpi` | CORRECTNESS | **FIXED** upstream 2019 (`cpus/cpu_arm_instr_dpi.c:187-188`); further work in #311 and #313 |
| R4 | gxemul-devel, 2016-09-10 / 2018-11-22 (Maya Rashish) | Floating-point 0.0 decoded as 2.22507e-308 on `-e 3max` | MIPS FPU | CORRECTNESS | **FIXED** upstream 2018-11-22; our fork later reworked the FPU further (#246 and others) |
| R5 | NetBSD PR **pkg/54114** (2019-04-11, Gustafsson; reply from Frank Kardel) | An unimplemented SCSI command (0xa3) hit `exit(1)`. pkgsrc's fix: ignore it. Kardel quotes SPC-4 §2.4.1: the device must return CHECK CONDITION, sense key ILLEGAL REQUEST, "INVALID COMMAND OPERATION CODE" | `disk/diskimage_scsicmd.c` | CRASH → CORRECTNESS | `exit` **FIXED** (`disk/diskimage_scsicmd.c:1380-1388` logs and returns). **The standards-compliant answer is still OPEN (filed `b120`/`b120u`, held):** an unknown command is reported to the guest as success. PR 54114 gives a real-guest witness (NetBSD-current/pmax probing with 0xa3) and the clause from the standard |
| R6 | NetBSD PR **pkg/54252** and gxemul-devel 2019-05-31 → 06-06 | NetBSD/hpcmips install fails on 0.6.1 (r5906, discarding translations for pages smaller than 4 KB); pmax boot-path bug | MIPS TLB, `machine_pmax` | CORRECTNESS | **FIXED** upstream 0.6.2 and inherited. Upstream also says it did not apply pkgsrc's "NOFPU CPU models" patch. Our fork has NOFPU for VR41xx (`include/mips_cpu_types.h:79-83`); comparing the full list belongs to the distro-patch agent |
| R7 | gxemul-devel, 2019-06-27 (Gustafsson; also Chris H. for Ultrix/3max on Ubuntu), msg 36704630 | Serial output stops until a key is pressed (NetBSD/hpcmips 8.1 install kernel, `-e mobilepro880`, Linux hosts only). A reproduction script is in the mail | console, ns16550/hpcmips serial, idle | CORRECTNESS | **UNVERIFIED.** No fork record. #251/#252 fixed *different* console-glue bugs. pmax and arc boots on WSL Linux pass, but hpcmips was never measured. The reproduction script is a cheap boot-level (rung-4) witness attempt |
| R8 | gxemul-devel, 2019-09-16 (Gustafsson), msg 36764010 | NetBSD/landisk: the guest clock stops advancing after a few minutes | `dev_sh4` TMU timer | CORRECTNESS | **FIXED** #400: the SH-4 timer underflow clamp pinned the counter at 0 (OpenBSD/landisk froze at ~515 s). **Never fixed upstream** (`dev_sh4.c` is unchanged in trunk) |
| R9 | gxemul-devel, 2023-03-30 (Jan-Benedict Glaw), msg 37797910 | With stdin redirected from `/dev/null`, the emulator spins forever in `console_charavail()` → `d_avail()` (backtrace in the mail) | `console/console.c` | CORRECTNESS / hang | **FIXED** #252 (stdin end-of-file now ends the read loop) |
| R10 | gxemul-devel, 2023-03-25 → 03-28 (Glaw, with a PATCH) | MAC addresses cannot be configured, and two GXemul processes generate the same MAC (bad when bridged over tap). The patch adds `-l` and `mac_list()` | `net/net_misc.c` | FEATURE / CORRECTNESS | **OPEN.** `net/net_misc.c:98-124`: `macbuf[5] = (serial_nr<<4) + (nr_of_nics<<1)`, so MACs repeat across processes and wrap after 8 NICs or 16 serial numbers. **The patch has a defect of its own:** its debug `fprintf` dereferences `m->mac_list` before its NULL check |
| R11 | gxemul-devel, 2023-03-28 (Glaw, PATCH); Debian #1032471 (2023-03-07); trunk TODO ("Chris Berry's patch") | Tap networking does not work on Linux hosts (`/dev/net/tun`, `TUNSETIFF`) | `net/net_tap.c` | FEATURE | **FIXED** #253 (`net/net_tap.c:48-50`, `:177-205`) |
| R12 | gxemul-users, 2013-04-07 (Mikael P.; reply from George Koehler) | OpenBSD/mvme88k 5.2 on 0.4.7.2: glibc reports "malloc(): memory corruption" during SCSI probing, after MODE_SENSE page 8 and a MODE_SELECT | osiop SCSI controller, MODE SELECT | CRASH / BOUNDS | **Likely FIXED:** #49 (osiop DATA_OUT unbounded heap **write**, CRITICAL), #205 (MODE SELECT over-read), #285 (partial MODE SELECT). Not re-witnessed on MVME187 |
| R13 | gxemul-devel, 2011-04-07 (Fausto S.) | Ultrix 4.5: "UNIMPLEMENTED cop0 (func 0x00)" stopped the emulator; gmp's `mpn_get_d` overflow test got +Inf instead of DBL_MAX | MIPS COP0 decode, FPU rounding | CRASH / CORRECTNESS | **FIXED** #236 (Reserved Instruction exception, `cpus/cpu_mips_instr.c:4930-4938`). The rounding side is covered by the FPU rounding rounds (#292, #294, #300); the gmp case itself was not re-run |
| R14 | gxemul-devel, 2012-06-12 (James Peacock, patch) | ARM `MSR` with the `s` or `x` field masks; the CPSR mask in user mode | `cpu_arm_instr` msr | CORRECTNESS | **FIXED** upstream r5800 (`cpus/cpu_arm_instr.c:822-828`) |
| R15 | gxemul-devel, 2012-09-05 (George Koehler, patch) | DHCP replies had a bad UDP checksum and lacked options, so `dhcpcd` rejected them | `net/net_ip.c` | CORRECTNESS | **FIXED** upstream r5803 (`net/net_ip.c:1074-1086`) |
| R16 | gxemul-devel, 2012-09-27 (Jeff R.); Debian #574537 (2010) | `mymkstemp()` without `O_CREAT`; failure to create the temporary file at startup | `core/misc.c` | OTHER | **FIXED** upstream r5722 and r5801 |
| R17 | gxemul-devel, 2010-01-25 (Yana, patch) | testarm aborted or segfaulted in the `dev_ether` receive path | `devices/dev_ether.c` | CRASH | **FIXED** upstream r5637 (`devices/dev_ether.c:151-157`) |
| R18 | gxemul-devel, 2008-06-10 (Jiri Svoboda) | ARM `bkpt` should raise a prefetch abort | `cpu_arm_instr` | CORRECTNESS | **FIXED** (`cpus/cpu_arm_instr.c:1026-1033`) |
| R19 | HelenOS ticket **#362** (2011–2012), quoting a 2010 GXemul thread (Jermář / Gavare) | arm32 on testarm "after about 20 seconds … does not receive any more interrupts". Gavare: GXemul checks for interrupts only "now and then", which "may be unreliable". HelenOS worked around it by randomising GXemul's check interval | interrupt delivery in the core execution loop | CORRECTNESS (lost interrupts) | **OPEN, and never fixed upstream.** A pending interrupt is delivered only when a block of instructions starts (`cpus/cpu_dyntrans.c:206-215`). ARM `msr` (`cpus/cpu_arm_instr.c:822-867`) and 88K `stcr` writing the PSR (`cpus/cpu_m88k_instr.c:839-850`, `cpus/cpu_m88k.c:522-554`) re-enable interrupts without checking for a pending one. So a short window of enabled interrupts inside one block loses the interrupt. MIPS `mtc0 Status` (`cpus/cpu_mips_instr.c:2468-2489`) and SH `ldc …,sr` (`cpus/cpu_sh_instr.c` near `:2835`) already deliver immediately, which is the fork's own model for the fix |
| R20 | Debian #609082 (2011, Silvio Cesare) | `memset` arguments swapped in `experiments/udp_snoop.c` | experiments | OTHER | **FIXED** (`experiments/udp_snoop.c:75`) |
| R21 | Launchpad #301041 (2008) | `gxemul a` segfaults | command-line loader | CRASH (command line) | **FIXED:** a missing file goes to `file_load_raw`, which calls `perror` and exits cleanly (`file/file_raw.c:58-63`) |
| R22 | Gentoo #976428 (2026-05-31, GCC 16 build farm) | `file_ecoff.c:197:40: error: variable 's_nlnno' set but not used [-Werror=unused-but-set-variable=]` | `file/file_ecoff.c` | OTHER (build) | **OPEN.** `file/file_ecoff.c:197` and `:483` (the second copy was not reported). `-Werror` is added only under `--debug` (`configure:455-461`), but `-Wall` alone will break the fork's zero-warnings build policy once it moves to GCC 16 |
| R23 | NetBSD wiki, cats page (edited 2026-08-02) | 0.7.0 cannot boot NetBSD/cats ≥ 10.0 (GCC ≥ 10) without the pkgsrc carry-flag patch | ARM | CORRECTNESS | **FIXED** (= U5, #311) |
| R24 | gxemul-users, 2008 | `bootblock_iso9660.c` freed `tmpfname` before it was used | ISO9660 boot | CRASH | **FIXED** upstream 0.4.6.6 (`disk/bootblock_iso9660.c:413`, then `:427`) |
| R25 | NetBSD PR **port-pmax/53611** (2018) | "PROM emulation: unimplemented JUMP TABLE vector" halted the 3MIN emulation (0.3.6.2) | `promemul/dec_prom.c` | CRASH (emulator stop) | **FIXED** #241/#245 (returns an error; message only at debug level; `promemul/dec_prom.c:184-194`) |
| R26 | gxemul-users, 2021-04-27/28 | 0.7.0 does not link on Linux | build | OTHER | **FIXED** (= U19) |
| R27 | NetBSD PRs 52242, 51315, 53202, 56466, 42934, 52238; HelenOS #24, #161, #347, #454 | Guest-OS bugs found while running under GXemul | — | — | **N/A** (fixed in NetBSD or HelenOS) |
| R28 | NetBSD emulator matrix | evbarm "latest working 2.1; problem is in GXemul's ARM emulation"; prep "NetBSD 3.x failed with disk controller problems"; dreamcast "root-on-NFS not possible" | ARM, PReP disk, Dreamcast network | CORRECTNESS / FEATURE | **UNVERIFIED.** The notes are stale (the cats page says all NetBSD/cats versions now run) and too vague to act on |
| R29 | barebox (2015); FreeBSD MIPS-emulation wiki | Malta: PCI-enabled barebox hangs; big-endian unsupported (incomplete PCI controller); no Malta network card | `machine_evbmips`, GT-64120 | FEATURE | Not assessed; feature gaps |
| R30 | virtuallyfun (2019–2025 comments) | Win32/Cygwin port; X11 mouse grab and tracking mismatch; a request for SGI O2 SCSI | portability, `x11.c` | FEATURE | Not in scope for the fork; trunk r6548 has a heuristic for mouse wrap-around |
| R31 | Fixed in trunk r6555 (the defect existed in 0.7.0 at `debugger/debugger_cmds.c:77`, `x > m->breakpoints.n`) | `breakpoint delete n`, where n equals the breakpoint count, frees memory out of bounds | debugger | BOUNDS (input from the debugger user) | **FIXED** (`debugger/debugger_cmds.c:129`, `x >= m->breakpoints.n`, commit `5ee491e7`) |

**Found while cross-checking; not reported anywhere upstream.**

- `machines/machine.c:281-282`: `machine_add_breakpoint_string(m, str)` ignores its `str` argument and duplicates `optarg` instead. This is latent today, because the only caller passes `optarg` (`core/main.c:439`). Trunk deleted the function.
- `core/memory.c:507-512`: the debugger's `device remove n` with an invalid number calls `exit(1)`. The input comes from the debugger user, not the guest. Low.

### B3. Things in trunk not to copy blindly

1. **Trunk stops the CPU on every error-level message by default** (`debugmsg.c`'s `skip_print` block; breakpoint level `VERBOSITY_ERROR` for all subsystems). Most of trunk's removals of `cpu->running = 0` (in `dev_mb89352`, `dev_luna88k` and `m88k`) exist *because of* this design. Read in isolation, they look like crash fixes, and they are not.
2. **Trunk's floating-point divide by zero always raises an exception** (`cpu_mips_coproc.c`). That is wrong unless the guest has enabled the divide-by-zero trap. Our fork's #254 is correct.
3. **The 88K loop fast paths (U29).** `fourword_copy_loop` calls `memcpy` on guest ranges that may overlap, which is undefined behaviour on the host; the real loop copies forward 16 bytes at a time. `byte_fill_loop` and `word_fill_loop` with a count of 0 exit at once, whereas the real loop wraps 2^32 times. Each needs a detector before it can be adopted.
4. **Trunk's error message for unimplemented addresses** (`memory_warn_about_unimplemented_addr`) adds a buffer with an inconsistent size argument (`sizeof(datastr) - i*3` beside offset `i*5`). It is harmless at the current sizes, but would be a latent defect if copied.
5. **The memory-management-unit equality guard (U28)** and **plain RAM for absent CPUs' memory-management units (U10)**: both contradict the fork's measured decisions or its option set.
6. **U1's loop in its upstream form** crashes on our fork's constructor-time stores. See U1/U2.
7. **Upstream's interrupt string for the 3000/300 (U14)** hard-codes `machine[0]`. Build it from `cpu->path` instead.

---

## (c) Features worth considering, with effort

| Feature | Origin | Effort and notes |
|---|---|---|
| Configurable MAC addresses (`-l` and `mac_list()`), with uniqueness across processes | Glaw patch 2023-03-28 (R10) | Small, about 80 lines. Validate the input, fix the patch's NULL dereference, and decide what happens beyond 8 NICs or 16 serial numbers (the current scheme wraps) |
| 88K memset/memcpy loop fast paths | trunk r6541/r6549/r6556 | Medium. Large speed-up for OpenBSD/luna88k. Needs the hazards in B3.3 fixed, plus a differential detector |
| OMRON MACH support on LUNA-88K: FUSE ROM checksum (Kenji Aoyama), the PROM `getxargs` vector, PFAR on the 0x3ffffff0 probe | trunk r6543, r6545, r6542 | Small. A further guest OS; overlaps with U8 |
| Loading 88K BCS COFF files and the `00 04 01 07` a.out variant | trunk r6524, r6577 | Small. **Host-side input parsing:** the trunk version seeks to fixed offsets (0x30, and a 0x2c section stride) without validation, so add bounds checks |
| NCD 88K X-terminal machine (`machine_ncd88k`, `dev_ncdserial`, `ncd88kprom`) | trunk r6577 | Medium to high. The author calls it experimental ("perhaps do not actually work") |
| Console and X11 flushing by wall-clock time | trunk r6532/r6555 (U22) | Small; also helps runs with several CPUs |
| Ctrl-T status line / `-N` periodic status | trunk r6532/r6555 | Small; usability |
| Seeded, deterministic pseudo-random generator for TLB random replacement | trunk r6563 (U25) | Small; makes runs reproducible |
| X11 mouse wrap-around heuristic | trunk r6548; virtuallyfun complaints | Small; usability |
| Malta PCI (GT-64120) completeness, big-endian Malta, a Malta NIC | barebox 2015, FreeBSD wiki | Medium to high |
| Newer NetBSD on macppc ("trigger unimplemented cases", trunk docs) | trunk `machine_macppc.html` | Unknown; needs a boot-level survey |
| SH4-A `synco` treated as a no-op (GCC 14 emits it) | pkgsrc 2026-04 (patch; for the distro agent) | Trivial; included here only as a cross-reference |

---

## (d) Top 5 recommendations, ranked by value

1. **Make 88K bus errors well formed: set the memory-management unit's fault status (`PFSR = BERROR<<16`) and fault address (`PFAR`) when a device refuses an access** (U8; upstream r6542/r6547; a few lines, with upstream's NULL check). This goes in `cpus/memory_rw.c`'s 88K device-failure branch (`:614-623`). Our fork's own artifact, `regress/artifacts/vmedefaultkill/measure_20261009/`, already shows that the current fault reaches OpenBSD's `trap.c` with PFSR = 0 and panics. Every FAULT disposition our fork uses on 88K (#568 `vmedefaultkill`, population 1, and any future FAULT on LUNA or MVME devices) depends on this. A guarded `badaddr()` probe of a population-1 offset should be predicted from source and then **measured**, using the existing VME probe, before and after the change.

2. **Make translated code coherent across CPUs** (U1, plus the U2 prerequisites). Port r6557/r6562's all-CPU discard in `memory_rw`. First relocate the three constructor-time stores (`cpus/cpu_alpha.c:101`, `cpus/cpu_arm.c:187`, `cpus/cpu_mips.c:303`), or guard `c != NULL`. Then extend the translate-time write revocation (`cpus/cpu_dyntrans.c:825-828`) to every CPU, which closes the part upstream left open. Witness first: a cold-debugger probe (rung 3) with `-n 2` on an unmodified luna88k or testm88k, where CPU 1 overwrites an instruction on a page CPU 0 has already executed, and CPU 0 then runs the stale instruction.

3. **Decode the 88K register-form signed `add`/`sub` family** (U7): `sub` (0x74, as in trunk's `X(sub)`), plus `add.ci/.co/.cio` and `sub.ci/.co/.cio` (0x71–0x73, 0x75–0x77). The semantics are in `_scratchpad/mc88100.txt:6021-6069`. Today these legal instructions, usable at any privilege level, stop the emulated CPU through `goto bad`. The witness is cheap: one instruction stored with the cold debugger. Check the encoding against the fork's disassembler first, because of the hand-assembled-encoding trap.

4. **Deliver a pending interrupt as soon as the guest re-enables interrupts on ARM and 88K** (R19; HelenOS #362 and the 2010 GXemul thread; never fixed upstream). `msr` and `stcr PSR` should check for a pending interrupt and, if there is one, end the current block of instructions or raise the interrupt immediately, as MIPS `mtc0` and SH `ldc sr` already do. Witness: free-running (not single-stepping) on testarm, with a timer interrupt pending and a tight loop that enables interrupts for one instruction then disables them.

5. **Adopt upstream's tested fix shapes for crash rows the fork has already filed, and close the cheap new ones.**
   - DEC 3000/300 interrupt string (U14, `ctorabortclass`). The host aborts at machine construction; build the string from `cpu->path`.
   - PVR `zwrite` (U11, `pvrrenderexit`): ignore the bit and keep rendering.
   - Dreamcast GD-ROM BIOS call `r7 = 8` (U12, new): return without stopping the CPU.
   - Model `RESET_CPU0..3` (U10) inside `lunadefaultstop`'s fix.
   - Decode the MB89352 command byte by bits 7:5 and add the bus-free interrupt (U9) as the design for `qhmbunimplstops`.
   - Each of these has an upstream precedent, but the caution in B3.1 applies: none of trunk's *halt removals* counts as evidence. Each row still owes its own witness and detector.
   - Cheap hygiene to batch alongside: the ARM and PPC log floods (U20, U21), GCC 16's `s_nlnno` (R22), and the missing `tmp_alpha_misc.c` dependency (U18).

**How I ranked them.** Items 1–4 are silent-wrong-behaviour or guest-drivable-stop defects that are new to the fork's records and have cheap rung-3 witnesses. Item 1 ranks first because our fork already holds a measurement of its consequence. Item 5 converts already-filed crash rows into quick, warranted fixes.
