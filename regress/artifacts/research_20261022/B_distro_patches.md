# B — Patches that OS distributions apply to GXemul, cross-checked against the hardened fork

Survey date 2026-10-22. Read-only: nothing was written under `GXEMUL-SEC/` or the project root.

* **Fork reference:** `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\src\` at HEAD `de8c7547`. Every source file cited
  below was checked clean against HEAD (`git diff --quiet HEAD -- <file>`), so the line numbers are HEAD line
  numbers. Each one also has a grep anchor in quotes, because a line number goes stale after the next edit.
  Ledger and OUTSTANDING_BUGS states come from the **working tree**. `ledger.json` has uncommitted edits.
* **Pristine upstream 0.7.0:** `C:\DocumentNoSnc\CC\GXEMUL_upstream_2021\root_src\`
* **Downloads:** every patch, spec, ebuild, log and history file is saved under
  `C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-cc-GXEMUL\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\ghresearch\distro_patches\<distro>\`
  (`netbsd_pkgsrc`, `freebsd_ports`, `openbsd_ports`, `debian`, `fedora`, `gentoo`, `aur`, `homebrew`, `macports`,
  `nixpkgs`, `other\{void,dports,t2,yacp,rosa,openmandriva}`).
* **Helper (read-only):** `...\scratchpad\ghresearch\tools_distro\hunk_presence.py`. For each historical patch it
  reports how many of the added lines are present, and how many of the removed lines remain, in upstream 0.7.0 and
  in the fork. It was used only to triage which patches to read by hand.

Method limits are listed at the end. Nothing here was built or run. Every status below comes from reading the
fork's source and its records.

---

## Summary

* **Packaging trees checked directly: 18.** NetBSD pkgsrc, FreeBSD ports, DragonFly DPorts, OpenBSD ports, Debian,
  Ubuntu (Launchpad), Fedora, ROSA, OpenMandriva, Gentoo, Arch AUR, Homebrew, MacPorts, nixpkgs, Void, T2 SDE,
  Cygwin "yacp" and openSUSE. Repology (`repology.org/project/gxemul`) was used to confirm the list is complete. It
  shows 59 repository entries. The rest are Debian rebuilds (Kali, Parrot, Raspbian, PureOS, Devuan, Deepin,
  Pardus) and a Gentoo rebuild (Liguros), which carry the same patches as their parent distribution.
* **Patch files on current packages: 28.**
  * 24 are on 0.7.0 packages: pkgsrc 10, FreeBSD 2, OpenBSD 1, Debian 2, Fedora 4, ROSA 3, nixpkgs 1, T2 1.
  * 4 are on packages still at 0.6.x: Gentoo's legacy ebuild 2, Void 1, OpenMandriva 1.
  * DragonFly ships FreeBSD's 2 patches byte-for-byte.
  * Gentoo-0.7.0, AUR, yacp and MacPorts carry no patch files. The first three work around the same build failure
    with compiler or linker flags. Homebrew has never packaged GXemul.
* **Status of the 28 against the fork:** 12 ALREADY FIXED, 10 NOT APPLICABLE, 6 STILL OPEN. The 6 open rows are
  5 distinct issues, because the Fedora and ROSA rpath rows are the same thing:

  | Issue | Severity |
  |---|---|
  | FreeBSD's wdc LBA patch: LBA-mode requests are addressed as CHS | HIGH, guest data integrity |
  | pkgsrc's SYNCO-as-NOP: only the host halt is fixed; the instruction's behaviour is a design choice | MED |
  | pkgsrc's removal of the ARM OpenFirmware magic-word store | LOW |
  | pkgsrc's SYNCO disassembly | cosmetic |
  | Fedora/ROSA's removal of `-Wl,-rpath` | packaging policy |

* **Older patches and bug trackers:** about 95 removed patch files were read or hunk-checked. About 20 more (C++
  component and tap/networking patches) were accepted on the distribution's own "included upstream" note. 51
  bug-tracker entries were reviewed.
  Almost all were merged upstream before 0.7.0 and are present in the fork. 4 more items are **still open**:

  | Item | Notes |
  |---|---|
  | MIPS 4Kc/4KEc/5Kc/5KE have no FPU (pkgsrc 2017) | never merged upstream |
  | footbridge `exit(1)` on reads of the SDRAM base-address registers | introduced by a pkgsrc patch; already tracked as `fbsdrampair` |
  | SCSI unsupported opcode should return CHECK CONDITION (NetBSD PR 54114) | already tracked as `b120` |
  | GCC 16 `-Werror` breaks `--debug` builds (Gentoo bug 976428) | open |

---

## (a) Per-distribution summary

| Distribution | Version packaged | Patch files | Notes |
|---|---|---|---|
| NetBSD pkgsrc `emulators/gxemul` | 0.7.0nb3 | **10** | The richest source. Its history includes about 90 earlier patches, nearly all merged upstream. |
| FreeBSD ports `emulators/gxemul` | 0.7.0_1 | **2** | Includes the wdc LBA patch (Adrian Chadd, 2013). |
| DragonFly DPorts `emulators/gxemul` | 0.7.0_1 | 2 | Byte-identical copies of FreeBSD's two patches (checked with `cmp`). |
| OpenBSD ports `emulators/gxemul` | 0.7.0 (REVISION 0) | **1** | Removes the hard-coded `-O3`. |
| Debian `gxemul` (sid, forky, trixie) | 0.7.0+dfsg-2 | **2** | bookworm has 0.7.0+dfsg-1, which carries only `remove_defines`. |
| Ubuntu | 0.7.0+dfsg-1 for 22.04–24.04; 0.7.0+dfsg-2 for 25.04 onward | 1–2 | Synced from Debian. The `buildN` uploads are rebuilds with no changes. |
| Fedora `rpms/gxemul` (rawhide, f39–f45) | 0.7.0-14 | **4** | Two are 0.6.0.1-era patches still applied to 0.7.0. |
| ROSA 13 (`abf.io/import/gxemul`, branch rosa2023.1) | 0.7.0-1 | 3 | Two are Fedora's 0.7.0 patches; the rpath one is re-diffed with different headers. |
| OpenMandriva | 0.6.2-1 | 1 | `cstdlib` patch, identical to ROSA's. |
| Gentoo `app-emulation/gxemul` | 0.7.0 (+ 0.6.3.1 legacy) | 0 for 0.7.0; 2 for legacy | The 0.7.0 ebuild adds `-fgnu89-inline` and strips `-O3` with sed. Bug 976428 (GCC 16) is open. |
| Arch AUR `gxemul` | 0.7.0-1 | 0 | Builds with `CFLAGS=-std=gnu99 -fgnu89-inline`. |
| Homebrew | not packaged | – | No formula in homebrew-core or legacy-homebrew history (GitHub API: 0 commits). |
| MacPorts `emulators/gxemul` | 0.4.7.2 | 0 | Stale. |
| nixpkgs `pkgs/by-name/gx/gxemul` | 0.7.0 | **1** | `0001-fix-attributes.patch` |
| Void `srcpkgs/gxemul` | 0.6.2_2 | 1 | `refcount_ptr.h` include. |
| T2 SDE `package/emulators/gxemul` | 0.7.0 | **1** | `linux-tap.patch` |
| Cygwin "yacp" | 0.7.0-1bl1 | 0 | Links with `-Wl,--allow-multiple-definition`. |
| openSUSE | not in Factory or Emulators | – | `build.opensuse.org/public/source/...` returns `unknown_package`. |

---

## (b) Patch by patch

Status keys:

* **ALREADY FIXED** — the issue is fixed in the fork. Evidence is the fork's code and its round number.
* **NOT APPLICABLE** — the fork's code differs so the patch has no target, or the patch is packaging policy or
  documentation.
* **STILL OPEN** — the fork has the same code the patch changes.

### NetBSD pkgsrc (0.7.0nb3)

Base URL for the files below: `https://github.com/NetBSD/pkgsrc/blob/trunk/emulators/gxemul/patches/`.
CVS history is at `http://cvsweb.NetBSD.org/bsdweb.cgi/pkgsrc/emulators/gxemul/`.

| # | Patch | Files / functions | What it does | Category | Status in our fork |
|---|---|---|---|---|---|
| P1 | `patch-doc_machine__cats.html` (skrll, 2021-09-05) | `doc/machine_cats.html` | Updates the NetBSD/cats install guide from 8.1 to 9.2. Replaces the note that FTP installs fail with "ethernet timeouts" with "It may also be possible to install via FTP, but this is slow and sometimes unstable". This shipped in the same commit as the ARM carry and UDF fixes. Whether those fixes caused the improvement is not established. | OTHER (doc) | **NOT APPLICABLE** (documentation). |
| P2 | `patch-src_cpus_cpu__arm.c` (skrll, 2021-09-05; upstream SVN r6573) | `cpus/cpu_arm.c` `arm_cpu_new()` | Comments out the "ugly hack" that sets `of_emul_addr = RAM_MB*1MiB-8` and `store_32bit_word(cpu, of_emul_addr, 0xef8c64be)` while the CPU is being created. Upstream's log: *"Storing to memory is not allowed until the CPU has initialized completely; this code was for ARM OpenFirmware, which is not currently in use by any machine."* | CORRECTNESS (latent) | **STILL OPEN.** See the note below the table. |
| P3 | `patch-src_cpus_cpu__arm__instr.c` (skrll; upstream r6572, patch by Nick Hudson) | `cpus/cpu_arm_instr.c` `X(to_be_translated)`, the special non-loadstore space | Routes the ARM "permanently undefined" (UDF) pattern `(iword & 0x07f000f0) == 0x07f000f0` to `cond_instr(und)`. Previously it hit `fatal("unimplemented special non-loadstore encoding!")` and `goto bad`, which halts the emulator. | CRASH (emulator halt) + CORRECTNESS | **ALREADY FIXED, and more broadly: #312** (CHANGELOG "Seventy-first round (#311, #312, #313)"). `cpu_arm_instr.c:4690` "`#312: a word reaching here takes the`" through `:4747` "`ic->f = cond_instr(und);`" routes every unmatched encoding in that space to und, not only UDF, and warns once for non-UDF words. |
| P4 | `patch-src_cpus_cpu__arm__instr__dpi.c` (skrll; upstream r6576, Nick Hudson) | `cpus/cpu_arm_instr_dpi.c`, subtract-family carry | Replaces `(uint32_t)a >= (uint32_t)b` with `c32 == c64`, so SBC and RSC (which have a borrow-in) produce the right C flag. | CORRECTNESS | **ALREADY FIXED: #311.** `cpu_arm_instr_dpi.c:292` "`#311: the subtract carry-out is NOT-BORROW`", with `:302` `if ((uint64_t)c32 == c64)`. The fork also fixed ADCS's V flag (#313), which pkgsrc does not. |
| P5 | `patch-src_cpus_cpu__sh.c` (mrg, 2026-04-19) | `cpus/cpu_sh.c` `sh_cpu_disassemble_instr()` | Disassembles `0x00ab` as `synco`. | OTHER (disassembler) | **STILL OPEN, cosmetic.** `cpu_sh.c` has no `synco` (grep returns 0 matches). |
| P6 | `patch-src_cpus_cpu__sh__instr.c` (mrg, 2026-04-19) | `cpus/cpu_sh_instr.c` `X(to_be_translated)`, `main_opcode == 0` | Decodes SH-4A `SYNCO` (`0x00ab`) as `instr(nop)`. Commit message: *"fixes running landisk 'dig' from recent builds, which would cause the emulator to hard exit."* *"GCC 14 likes to emit it."* | CRASH (emulator exit) + CORRECTNESS (compatibility) | **PARTIAL.** The host exit is **ALREADY FIXED by #314** (CHANGELOG "Seventy-ninth round (#314)"; `cpu_sh_instr.c:242` `X(reserved)` raises `EXPEVT_RES_INST`, and the decoder sites carry "`instr(reserved);	/*  #314  */`"). The NOP behaviour was **deliberately not adopted**: #314 argued no SH-4A model is built, so `synco` is reserved on every core. **That leaves an open compatibility question:** under the fork, a NetBSD-current/landisk binary that uses `synco` takes a guest illegal-instruction exception rather than running. See recommendation 3. |
| P7–P10 | `patch-src_include_thirdparty_{bootblock.h, dp83932reg.h, pcireg.h, sgi__arcbios.h}` (jakllsch, 2024-10-27, "following upstream trunk") | 4 thirdparty headers | Removes `#define __attribute__(x)` / `#define __noreturn__` neutering. It strips `__gnu_inline__` from glibc headers, which gives duplicate `__cmsg_nxthdr` symbols at link time on Linux. | BUILD | **ALREADY FIXED: #11** (REVIEW_FINDINGS row 11; e.g. `include/thirdparty/pcireg.h:15` "`Removed historic "#define __attribute__(x) / __noreturn__" neutering`"). The fork's note adds that the neutering also silently discarded `__attribute__((packed))`. #9 (`configure:570` "`checking whether -fgnu89-inline can be used`") adds the belt-and-braces flag probe. |

**P2 detail.** `cpu_arm.c:181-188` ("`NOTE/TODO: Ugly hack for OpenFirmware emulation`") is unchanged from
upstream:

* `cpu->cd.arm.of_emul_addr` has **no reader** anywhere in `src/`. `grep -rn of_emul_addr` finds only the two
  assignment lines on ARM; the PowerPC copy is separate.
* So on every ARM machine with PROM emulation, this store plants the word `0xef8c64be` in the last 8 bytes of guest
  RAM before the CPU finishes initialising, and nothing ever uses it.
* The decoder maps that word to `X(openfirmware)` (`cpu_arm_instr.c:5034`), which calls `of_emul()`. That ends the
  process on every ARM machine, because `of_data` is NULL there. This is the fork's open row `ofemulnodata`.
* No ledger row covers the store itself.

### FreeBSD ports (0.7.0_1) — the same two patches ship in DragonFly DPorts

| # | Patch | Files / functions | What it does | Category | Status in our fork |
|---|---|---|---|---|---|
| F1 | [`files/patch-configure`](https://cgit.freebsd.org/ports/tree/emulators/gxemul/files/patch-configure) | `configure` | Replaces `/usr/X11R6` in the first X11 probe with `${LOCALBASE}`. Deletes the `-O3`/`-O` auto-optimisation block. | BUILD | **NOT APPLICABLE.** Packaging policy. The fork's `configure` already probes `/usr/local` (`:366`), and the `-O3` block (`:544`) is upstream behaviour, not a defect. |
| F2 | [`files/patch-src_devices_dev__wdc.c`](https://cgit.freebsd.org/ports/tree/emulators/gxemul/files/patch-src_devices_dev__wdc.c). Origin: ports commit `9d2b32a021a3`, Adrian Chadd, 2013-06-28, *"Enable LBA in GXEMUL. FreeBSD-10's ATA code requires LBA to be used. There's no code in the ATA stack to send CHS commands to the hardware these days."* Renamed `.cc` to `.c` in `9478a8c169cd` (PR 261874). | `devices/dev_wdc.c` `wdc__read()`, `wdc__write()` | Turns the `#if 0` LBA block on (`#if 1`), so `offset = 512*(((head&0xf)<<24) + (cyl<<8) + sector)` whenever `d->lba` is set. Turns the `printf` into `debug()`. | CORRECTNESS (guest disk data: wrong sector read and written) | **STILL OPEN** — the fork has the same `#if 0` in both functions. Both sites, the reason the patch cannot be taken as written, and the decision the fork's #407 record already made are in the note below. |

**F2 detail.**

* **Both sites are still disabled:** `dev_wdc.c:470` "`#if 0`" through `:476` in `wdc__read`, and `:562` through
  `:568` in `wdc__write`. A guest that sets the ATA LBA bit therefore gets its LBA bytes interpreted as
  cylinder/head/sector. Reads come from the wrong sector, and writes go to the wrong sector, so the disk image is
  corrupted. Host safety is unaffected because #416 bounds every disk access.
* **The FreeBSD patch is unsafe to copy as written.** The SDH decode at `dev_wdc.c:2015` ("`d->lba   = (idata >> 5) & 1;`")
  reads **bit 5**. ATA puts LBA in **bit 6** (0x40); bits 7 and 5 are obsolete and always written as 1.
  * NetBSD writes `WDSD_IBM (0xa0) | drive<<4 | head` for *CHS* requests. So with the FreeBSD patch, every NetBSD
    CHS request would be routed down the LBA formula. For example, block 0 (CHS sector 1) would read from offset 512.
  * **Verified against NetBSD trunk** (copies in `distro_patches\netbsd_pkgsrc\netbsd_src_refs\`):
    * `sys/dev/ic/wdc.c:1816` is the `wdccommand()` write above.
    * `sys/dev/ata/atareg.h:244-246` defines `WDSD_IBM 0xa0`, `WDSD_CHS 0x00` and `WDSD_LBA 0x40`.
    * `sys/dev/ata/ata_wdc.c:398-411` ORs in `WDSD_LBA` only in LBA mode.
    * `sys/dev/ata/wd.c:394-395` uses LBA only when IDENTIFY word 49 advertises it, and the fork leaves that word 0.
      So NetBSD guests on GXemul use CHS.
  * Adopt the *idea* (LBA28 addressing), but decode LBA from bit 6 and keep SDH readback byte-exact.
* **The fork already records the related decision.** IDENTIFY word 49 (LBA capability) is deliberately left 0, and
  #407 gates that zero (CHANGELOG #407, "Not touched, deliberately: word 49 (LBA support) stays zero"). Honouring
  LBA requests is independent of *advertising* LBA support. Advertising it would move NetBSD and Linux guests onto
  the new path.
* **Not filed.** No dedicated ledger row exists (searched `ledger.json` for "lba").

### OpenBSD ports (0.7.0)

| # | Patch | Files | What it does | Category | Status in our fork |
|---|---|---|---|---|---|
| O1 | [`patches/patch-configure`](https://github.com/openbsd/ports/blob/master/emulators/gxemul/patches/patch-configure), "remove hardcoded O3" | `configure` | Deletes the `-O3`/`-O` block so the package's CFLAGS are respected. | BUILD | **NOT APPLICABLE** (packaging policy; the fork's `configure:544` keeps it). |

### Debian 0.7.0+dfsg-2 (Ubuntu ≥ 25.04 and the Debian derivatives are identical)

| # | Patch | Files / functions | What it does | Category | Status in our fork |
|---|---|---|---|---|---|
| D1 | [`debian/patches/remove_defines`](https://sources.debian.org/src/gxemul/0.7.0+dfsg-2/debian/patches/remove_defines/), Göran Weinholt 2021-11-24, quoting upstream *"Removing weird defines, hopefully enabling build on Linux"* | Same 4 thirdparty headers, plus `doc/TODO.html` | Same as P7–P10. Upstream's explanation is in [gxemul-users 2021-04-28](https://sourceforge.net/p/gxemul/mailman/message/37270384/) (duplicate `__cmsg_nxthdr` at link time). | BUILD | **ALREADY FIXED (#11, #9).** |
| D2 | [`debian/patches/0002-Fix-tap-device-support-on-Linux.patch`](https://sources.debian.org/src/gxemul/0.7.0+dfsg-2/debian/patches/0002-Fix-tap-device-support-on-Linux.patch/), Jan-Benedict Glaw, Debian bug [#1032471](https://bugs.debian.org/1032471) | `net/net_tap.c` `net_tap_init()` | On Linux, opens `/dev/net/tun` and calls `TUNSETIFF` with `IFF_TAP\|IFF_NO_PI` and `ifr_name = tapdev`. Uses `strncpy(..., IFNAMSIZ)`. | PORTABILITY (host OS) | **ALREADY FIXED: #253** (REVIEW_FINDINGS row 253; `net_tap.c:178` "`#253: On Linux a tap is not opened via its own device node`"). The fork's version is stricter: it **rejects** names of `IFNAMSIZ` characters or more instead of truncating them without a terminating NUL, and it closes the fd on failure. Do not replace it with Debian's. |

### Fedora 0.7.0-14

[`gxemul.spec`](https://src.fedoraproject.org/rpms/gxemul/blob/rawhide/f/gxemul.spec). Patch files are in the same
directory.

| # | Patch | Files | What it does | Category | Status in our fork |
|---|---|---|---|---|---|
| R1 | `gxemul-0.6.0.1-Makefile-cleanup.patch` (Patch0) | `configure`, `Makefile.skel` | Adds a default `MANDIR=/usr/share/man` and an empty `DESTDIR=`. | BUILD | **NOT APPLICABLE.** 0.7.0's `configure` already handles `MANDIR` (`:1053`) and `DESTDIR` (`:1076`). |
| R2 | `gxemul-0.6.0.1-gcc47.patch` (Patch1) | `include/refcount_ptr.h` | Adds `#include <cstddef>`. | BUILD | **NOT APPLICABLE.** `refcount_ptr.h` is a leftover C++ header that no file in the fork includes (grep). |
| R3 | `gxemul-0.7.0-linux-fix.patch` (Patch2, cites the gxemul-users message) | `pcireg.h`, `sgi_arcbios.h` | Comments out the `__attribute__`/`__noreturn__` defines. | BUILD | **ALREADY FIXED (#11).** |
| R4 | `gxemul-0.7.0-no-rpath.patch` (Patch3) | `configure` X11 probes | Removes `-Wl,-rpath,/usr/X11R6/lib`, `.../X11R7/lib` and `/usr/local/lib`. | BUILD (packaging policy) | **STILL OPEN, low.** The fork's `configure:336`, `:351` and `:366` still add the rpaths. This is a distro-policy and hygiene item, not an emulator defect. |

### ROSA 13 and OpenMandriva

| # | Patch | Files | What it does | Category | Status in our fork |
|---|---|---|---|---|---|
| RO1 / OM1 | `gxemul-0.6.0.cstdlib.patch` ([ROSA raw](https://abf.io/import/gxemul/raw/rosa2023.1/gxemul-0.6.0.cstdlib.patch); identical in [OpenMandriva](https://github.com/OpenMandrivaAssociation/gxemul)) | `include/refcount_ptr.h` | Adds `<cstdlib>` and `<cstddef>`. | BUILD | **NOT APPLICABLE** (header unused). |
| RO2 | `gxemul-0.7.0-linux-fix.patch` | 2 headers | Identical to R3 (`cmp`). | BUILD | **ALREADY FIXED (#11).** |
| RO3 | `gxemul-0.7.0-no-rpath.patch` | `configure` | Same content as R4, different diff headers. | BUILD | **STILL OPEN** (same as R4). |

### nixpkgs, Gentoo, Void, T2

| # | Patch | Files | What it does | Category | Status in our fork |
|---|---|---|---|---|---|
| N1 | [`0001-fix-attributes.patch`](https://github.com/NixOS/nixpkgs/blob/master/pkgs/by-name/gx/gxemul/0001-fix-attributes.patch) | `pcireg.h`, `sgi_arcbios.h` | Deletes the two `#define`s, leaving the `#undef`s. | BUILD | **ALREADY FIXED (#11).** |
| G1 | [`files/gxemul-0.6.0-gcc46.patch`](https://github.com/gentoo/gentoo/tree/master/app-emulation/gxemul/files) (legacy 0.6.3.1 ebuild only) | `refcount_ptr.h` | Adds `<stddef.h>`. | BUILD | **NOT APPLICABLE.** |
| G2 | `files/gxemul-0.6.0-no-doxygen.patch` (legacy only) | `configure` | Skips the Doxygen probe. | BUILD | **NOT APPLICABLE.** 0.7.0's `configure` has no Doxygen probe. |
| V1 | [`patches/patch-src_include_refcount__ptr.h.patch`](https://github.com/void-linux/void-packages/tree/master/srcpkgs/gxemul/patches) (0.6.2; a copy of an old pkgsrc patch) | `refcount_ptr.h` | Adds `<stddef.h>`. | BUILD | **NOT APPLICABLE.** |
| T1 | [`linux-tap.patch`](https://svn.exactcode.de/t2/trunk/package/emulators/gxemul/linux-tap.patch) (T2 SDE, 2022) | `net/net_tap.c` | Linux tap through `/dev/net/tun`, `TUNGETFEATURES` and `TUNSETIFF`. | PORTABILITY | **ALREADY FIXED (#253).** **Do not import:** T2 copies the user-supplied name with **`strcpy(ifr.ifr_name, tapdev)`**, an unbounded copy into a 16-byte field. It also leaks the fd when the ioctl fails. |

### Build workarounds expressed as flags rather than patch files (no patch file to count)

| Distro | Workaround | Root cause | Fork status |
|---|---|---|---|
| Gentoo 0.7.0 | `append-cflags -fgnu89-inline`; `sed 's/-O3//'` on `configure` | attribute neutering (P7–P10) | ALREADY FIXED (#11 + #9) |
| AUR | `CFLAGS="... -std=gnu99 -fgnu89-inline"`; sed to fix the man path | same | ALREADY FIXED |
| Cygwin yacp | `OTHERLIBS="-Wl,--allow-multiple-definition"` | same | ALREADY FIXED |
| pkgsrc | `SUBST` rewriting `/usr/X11R6` in `configure` | X11 path probe | Packaging only |
| Debian `rules` | Strips `-Wl,-rpath`; replaces `COMPILE_DATE` (reproducible builds); empty `dh_auto_test` (the upstream test suite is broken) | rpath, reproducibility | Packaging only (same as R4) |

---

## Older patches (removed from the distro trees) and bug-tracker entries

The status column checks the claim of each distribution's update commit — for example *"All pkgsrc patches are
included by upstream"* in pkgsrc `0121c3706d` (0.6.3) and `4a9f1e5d6e` (0.6.2) — by reading upstream 0.7.0 and the
fork.

| Source | Item | Category | Status in our fork (evidence) |
|---|---|---|---|
| pkgsrc 2018–19 (gson, skrll) | MIPS `DIV`/`DDIV` divide overflow (`INT_MIN / -1` crashed the host) | CRASH | **Present** (upstream merged it): `cpu_mips_instr.c:1839` and `:1863` (`a == (int32_t)0x80000000U && b == -1`) |
| pkgsrc 2016/2019 (mrg) | MIPS32 trap-immediate instructions `tgei` … `tnei`, plus disassembly | CORRECTNESS | **Present**: `cpu_mips_instr.c:1631-1706`, `cpu_mips.c:1549` |
| pkgsrc 2019 (gson) | `SA_RESTART` on SIGALRM (console data loss) | CORRECTNESS | **Present**: `core/timer.c:333` |
| pkgsrc 2019, PR [pkg/54114](https://gnats.netbsd.org/54114) (christos) | Unimplemented SCSI command: change `exit(1)` to "ignore". In the PR, Frank Kardel quotes SPC-4 §2.4.1: an unsupported opcode *"shall terminate … with CHECK CONDITION … ILLEGAL REQUEST … INVALID COMMAND OPERATION CODE"*. The witness was NetBSD-current/pmax sending opcode `0xA3` while probing scsibus. | CRASH → CORRECTNESS | The exit is gone (`diskimage_scsicmd.c:1380-1384`, "`// exit(1);`"). The **standards-correct status is STILL OPEN** and tracked as ledger `b120` ("b120u SCSI: an unknown command is reported to the guest as success", **held**). The helper it needs already exists: `diskimage__return_check_condition()` at `:208` (#416). |
| pkgsrc 2017 (christos), "cosmetic (no/op) code for the SDRAM setup that cats does" | footbridge: always re-assert IRQs, and new `SDRAM_BA_MASK`/`SDRAM_BA_OFFSET` cases | CORRECTNESS / CRASH | The IRQ change is present. **The read arms the patch introduced call `exit(1)` and are STILL in the fork:** `dev_footbridge.c:732` "`case SDRAM_BA_MASK:`" (`exit(1)` at `:735`) and `:757` "`case SDRAM_BA_OFFSET:`" (`exit(1)` at `:760`). Tracked as `fbsdrampair` (HIGH, open; its "HEAD :712, :737" citation is stale against `de8c7547`). **Provenance learned here:** a distro patch introduced these guest-reachable host exits, and upstream inherited them. |
| pkgsrc 2017 (mrg) | MIPS 4Kc / 4KEc / 5Kc / 5KE marked `NOFPU` (real cores lack an FPU) | CORRECTNESS (CPU-model fidelity) | **STILL OPEN, never merged upstream.** `include/mips_cpu_types.h:101-104` still has flags `0`. The pkgsrc commit itself warned *"this will break the MALTA kernel in gxemul"*: evbmips defaults to `5Kc` (`machine_evbmips.c:165`), so the default CPU would have to change too. Low priority. |
| pkgsrc 2017 (christos) | `console_charavail()` returns a count; SCIF FDR reports it (landisk dropped characters) | CORRECTNESS | **Present** (`console_room_left_in_fifo`; `dev_sh4.c` SCIF_FDR) |
| pkgsrc 2017 / 2019 | pmax boot path `rz0`; hpcmips R4100 `tlbwri` hack | CORRECTNESS | **Superseded upstream** (`machine_pmax.c` builds `"X/rzY/"`; `coproc_tlbwri` checks the V bit per page) |
| pkgsrc 2021-01 (skrll) | MIPS address-error exception gets the correct ASID and VPN2 | CORRECTNESS | **Present**: `cpu_mips_instr_loadstore.c:61-76` |
| pkgsrc 2011–2013 (mrg, matt, christos) | SH `LDS Rm,MACH/MACL`; SH user→kernel-address exception; ARM `msr` any field mask; `blx` arg; `add ip,pc,#0` immediate | CORRECTNESS | **Present or reworked** (`cpu_sh_instr.c:4452`; `memory_sh.c:359`; the fork's #322 imm-rotate carry path) |
| pkgsrc 2012 (abs) | Dreamcast GD-ROM TOC | CORRECTNESS | **Present** (23 of 23 added lines found in `dev_dreamcast_gdrom.c`) |
| pkgsrc 2018 (kamil), about 60 patches | Clang / C++11 literal spacing, `void (*f)()` typedefs | BUILD | **NOT APPLICABLE** (0.7.0 is C) |
| FreeBSD 2008 (imp, from gonzo@) | piix IDE PCI config writes were not stored (FreeBSD panicked after probing IDE) | CORRECTNESS | **Present**: `bus_pci.c:781` `PCI_SET_DATA(reg, value);` |
| FreeBSD 2006 (bms) | YAMON `khz` environment variable for malta | CORRECTNESS | **Present**: `promemul/yamon.c:126` |
| Debian 0.4.6.6-3 / 0.4.6.3-1+lenny1; Launchpad [#301041](https://bugs.launchpad.net/ubuntu/+source/gxemul/+bug/301041) | `gxemul a` crashed with no machine type | CRASH | **Present**: `core/main.c:781-782` "`No machine type specified?`" |
| Debian [#574537](https://bugs.debian.org/574537); Gentoo bug 441558 | `mymkstemp()` opened without `O_CREAT`, so gxemul died at startup | CRASH | **ALREADY FIXED** (REVIEW_FINDINGS #2 and #43; `core/misc.c:211` uses `O_CREAT\|O_EXCL` and a `/dev/urandom` suffix) |
| Debian [#609082](https://bugs.debian.org/609082) | `memset(&si, sizeof(si), 0)`: arguments swapped | CORRECTNESS | **Present** (fixed upstream): `experiments/udp_snoop.c:75` |
| Gentoo bug [976428](https://bugs.gentoo.org/976428) (open, 2026-05-31) | GCC 16 with `--debug` (`-Werror`) fails on set-but-unused variables in `file_ecoff.c` (e.g. `s_nlnno`, `cbSsOffset`, `crfd`), `file_elf.c` (`p_align`, `sh_name`, `st_info`, `eflags`, …) and `file_macho.c` (`n_type`, `ncmds`, …) | BUILD | **STILL OPEN, debug builds only.** The variables are still set and never read (grep counts). The fork's trees build without `-Werror`; `configure:456` adds it only when `DEBUG=YES`. |
| NetBSD PRs [54252](https://gnats.netbsd.org/54252), [52242](https://gnats.netbsd.org/52242); FreeBSD [211172](https://bugs.freebsd.org/bugzilla/show_bug.cgi?id=211172); Red Hat bugs 197454, 199824, 1604301; the rest of the Debian archive (FTBFS on kfreebsd, hurd, mips, m68k) | 0.4.x–0.6.x regressions and build failures | – | All closed. Superseded in 0.7.0 or not about the emulator. |

---

## (c) Top 5 recommendations, ranked by value

1. **Honour ATA LBA28 addressing in `dev_wdc.c`, but not with FreeBSD's patch (F2).**
   * **Severity: HIGH, guest data integrity.** An LBA-mode guest gets wrong-sector reads, and writes that land in
     the wrong place in the disk image. FreeBSD ≥ 10 always uses LBA, as the port commit says, and any driver that
     ignores word 49 does too. FreeBSD and DragonFly have shipped this fix since 2013, which shows real guests need it.
   * **Why not the patch as written:** it keys on the existing `d->lba`, which is decoded from **bit 5** at
     `dev_wdc.c:2015`. NetBSD writes `0xa0` (bit 5 set) on *CHS* requests, so the patch would misroute every NetBSD
     CHS access. The fix needs three things:
     * decode LBA from bit 6 (0x40);
     * compute `((head&0xf)<<24)|(cyl_hi<<16)|(cyl_lo<<8)|sector` in `wdc__read` and `wdc__write`;
     * keep the SDH readback byte-exact.
   * **Keep word 49 = 0 as a separate decision** (#407 gates it). Advertising LBA would move NetBSD and Linux onto
     the new path.
   * **Witness:** a rung-3 probe on unmodified `-E evbmips -e malta` with a patterned disk image.
     * Test: the guest writes SDH=`0xE0` and issues READ SECTORS. Today it gets the CHS-decoded sector.
     * Liveness control: SDH=`0xA0` CHS reads must stay correct.
   * **Filing:** not yet a ledger row.
2. **Prioritise `fbsdrampair` (already filed HIGH): the footbridge `SDRAM_BA_MASK`/`SDRAM_BA_OFFSET` read arms
   `exit(1)`.**
   * **Provenance found here:** pkgsrc added these arms in 2017 as "cosmetic (no/op)" code for cats SDRAM setup
     (christos, `e975aa3484`), and upstream adopted them. Every distribution's GXemul now ships two guest-reachable
     process exits.
   * The row has already chosen DECLINE (member 3).
   * **Records fix:** the row's "HEAD :712, :737" citation is stale; at `de8c7547` the arms are at `:732` and
     `:757`.
3. **Re-adjudicate SYNCO (`0x00AB`) on landisk/SH-4 (P6).**
   * #314 chose "reserved instruction exception", because no SH-4A model exists.
   * **New evidence #314 did not have:**
     * pkgsrc (mrg, `d9851dcaeb`, 2026-04-19) reports that **NetBSD-current landisk userland built with GCC 14
       contains `synco`** ("dig").
     * The SH-4 manual (`_scratchpad/sh4_programming.txt:4508-4526`) guarantees the illegal-instruction exception
       only for `H'FFFD` and says *"Operation is not guaranteed if an undefined code other than H'FFFD is decoded"*.
     * So a NOP is within the architecture's latitude, and it is what makes that userland run.
   * The fork's choice also no longer halts the host. The open question is guest compatibility, and it is the
     owner's to decide.
   * **P5 (cosmetic):** the disassembler line `synco` is free to add either way.
4. **Close `b120` (unknown SCSI opcode reported as success) the SPC way.**
   * NetBSD PR 54114 gives both halves:
     * the standards text: CHECK CONDITION / ILLEGAL REQUEST / ASC 0x20 (INVALID COMMAND OPERATION CODE);
     * a real-guest witness: NetBSD-current/pmax issues `0xA3` while probing scsibus.
   * The `default:` arm at `diskimage_scsicmd.c:1380` still only prints a debug message. The
     `diskimage__return_check_condition()` helper (`:208`) is already in the file.
   * **Treat this as a sketch, not a fix.** Under the fork's sketch rule it must first be traced through each
     controller's status path: asc (#240 raises its own illegal-command IRQ), and the mb89352 path (`mb89352halt`,
     `mbcdbincomplete`).
5. **Remove the ARM OpenFirmware magic-word store from `arm_cpu_new()` (P2, upstream SVN r6573).**
   * Low severity, a few-line change.
   * It removes a word that every ARM boot plants in the last 8 bytes of RAM. Nothing reads its address
     (`of_emul_addr`), and the word itself routes to the `of_emul()` exit tracked as `ofemulnodata`.
   * It pairs naturally with that row and `armrebootmagic`.
   * **Witness:** after construction on `-E testarm` or `-E cats`, a debugger dump of `RAM_top-8` reads `0xef8c64be`.

**Lower priority, recorded for completeness:**

* MIPS 4Kc/4KEc/5Kc/5KE FPU flag. Fidelity only; it requires changing evbmips' default CPU first.
* GCC 16 `-Werror` in `--debug` builds (Gentoo 976428). Delete or `(void)` the dead locals.
* Fedora/ROSA/Debian `-Wl,-rpath` removal and OpenBSD/FreeBSD/Gentoo `-O3` removal. Packaging policy.

---

## Method and limits

* **Sources used:**

  | Distribution | Where the files came from |
  |---|---|
  | pkgsrc | `raw.githubusercontent.com/NetBSD/pkgsrc`. History through the GitHub commits API (103 commits on `emulators/gxemul`); `distinfo` snapshots at `14e6b39a43`, `af3b32097b`, `b4655617a5` and `d0940619d2`. |
  | FreeBSD | `cgit.freebsd.org` (tree, log, `/patch/?id=`) and the Bugzilla REST API. |
  | OpenBSD, Gentoo, nixpkgs, Void, DPorts, yacp, OpenMandriva | GitHub mirrors (contents and commits APIs). |
  | Debian | `sources.debian.org` API, `snapshot.debian.org` and the Debian bug tracker. |
  | Ubuntu | Launchpad API. |
  | Fedora | Pagure API at `src.fedoraproject.org`, and Red Hat Bugzilla. |
  | ROSA | `abf.io` raw files. The connection was intermittent; branch `rosa2023.1` is ROSA 13. |
  | T2 | `svn.exactcode.de`. |
  | Gentoo bugs | `bugs.gentoo.org` REST API. |
  | NetBSD bug reports | `gnats.netbsd.org`, searched by synopsis, plus the individual reports. |

* **Not done:**
  * Nothing was built, run or probed. Every "STILL OPEN" and "ALREADY FIXED" comes from reading the code.
  * The NetBSD CHS-encoding claim behind F2 was checked against NetBSD trunk source (citations in F2's note), not
    against a running guest.
  * FreeBSD's "LBA always" behaviour is taken from the port commit message; FreeBSD's ATA code was not re-read.
  * What real SH7751R silicon does with `0x00AB` is unknown. The manual leaves it unspecified.
* **The FreeBSD Bugzilla HTML front end is behind Anubis bot protection.** Its REST API worked and was used instead.
