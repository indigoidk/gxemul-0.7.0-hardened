# GXemul 0.7.0 — `est/` Change Log

Authoritative record of every change made to the `est/` working copy while
hardening GXemul 0.7.0. Companion documents:

- **`CHANGES.patch`** — precise unified diff (original `src/` → `est/src/`). 56 source files (now incl. `devices/makeautodev.sh`). (Generated/build files — `*.o`, `tmp_*.c`, `auto*.c`, `Makefile`, `font8x*.c`, `ppc_spr_strings.h` — are excluded; the `-fgnu89-inline` `configure` fix is in both trees so it no longer diffs.)
- **`REVIEW_FINDINGS.md`** — full findings table, severities, and the fuzzing/validation methodology.
- **`../build/BUILD_NOTES.md`** — how to build (native WSL ext4; `-fgnu89-inline`).

**Status:** 67 corrections + 1 performance optimization (#67); extended by #69 (arc/jazz), #70–#88 (outstanding-bug remediation), and #89–#94 (multi-model review). **Primary gcc build: 0 errors / 0 warnings.** No ASan/UBSan
reports across the 6,772-case audit (cases run to timeout — no sanitizer signature observed,
*not* a full behavioral pass; the ASan/UBSan/clang/`-fanalyzer` configs emit pre-existing
non-fatal warnings, mostly in generated dyntrans code). Guests boot across **5 CPU arches**
(MIPS / PPC / SH4 / ARM / M88K) and **3 OS families** (NetBSD, OpenBSD, Linux).

> Source changes are confined to `est/src/**`. The `-fgnu89-inline` `configure` build
> fix is also applied to the root (baseline) `configure` so both trees build cleanly;
> the original `src/` *code* is untouched (kept as the orig-vs-est reference).

---

## Changes by file (35 files)

| File | Corrections | What changed |
|------|-------------|--------------|
| `configure` | #9 | Auto-detect & add `-fgnu89-inline` (fixes modern-glibc link errors) |
| `devices/makeautodev.sh` | #61 | **#61** generate `autodev.c` via a PID-unique temp file + atomic `mv` (was a non-atomic append → concurrent recursive-make runs corrupted it → intermittent build failure) |
| `core/emul.c` | #3, #4, #42, #60 | `system()` gzip → `fork`/exec (no shell injection); `tmpstr[20]→[32]`; **#42** absolute-path `gunzip` (anti-`$PATH`) + `fd != STDOUT_FILENO` close guard + `--` option-injection guard; **#60** pass the `mkstemp` fd to the child & `dup2` it instead of reopening by name (closes the same-user temp race) |
| `core/misc.c` | #1, #2, #43 | `mystrlcpy`/`mystrlcat` bounded; `mymkstemp` hardened; **#43** suffix from `/dev/urandom` (unpredictable temp names) |
| `symbol/symbol.c` | #18 | `fscanf("%s")` → `%79s` (stack-overflow) |
| `file/file_aout.c` | #14, #17 | symbol `str_index` bounds; signed `symbsize`→`uint32_t` + file-size bound |
| `file/file.c` | #27 | **`unencode` macro** sign-extends via an unsigned accumulator (was `var=-1; var<<=8`, a signed-shift UB) — clears all 102 UBSan signatures across every file loader |
| `file/file_elf.c` | #15, #26, #28, #62 | symbol `st_name` bounds; reject `sh_size > file size`; tighten with `sh_offset` + symtab entry-size-multiple; **#62** also cap SYMTAB/STRTAB `sh_size` at `LOADER_MAX_TABLE_BYTES` (sparse-file OOM) |
| `file/file_ecoff.c` | #16, #59, #62, #66 | `es_strindex` bounds; **#59** bound `f_nsyms` (MS-COFF fallback), `issExtMax`, `iextMax` (offset + count*size ≤ file size) before `malloc`/`fread`, and check the previously-unchecked MS-COFF `fread`; **#62** + a 256 MB `LOADER_MAX_TABLE_BYTES` cap (sparse-file OOM); **#66** bound the MS-COFF long-name `altname` read + skip instead of `exit` |
| `file/file_macho.c` | #16, #19 | `n_strx` bounds + NUL-term; **load-command bounds + `cmd_len==0` guard** + zero-init `buf` & `pos+256>len` (truncated-thread uninit read) |
| `file/file_srec.c` | #6 | zero `bytes[]` (uninit leak) + negative-length guard |
| `disk/diskimage.c` | #7, #20 | free `overlay_basename` on error paths; temp files `fopen "wx"` + NULL-check |
| `devices/dev_fb.c` | #8, #21 | **guest OOB host write** guard (`x2<x1`); 24-bit fill bound (`linelen`, not `sizeof(ptr)`) |
| `devices/dev_osiop.c` | #10 | guard NULL `d->xferp` before SCSI phase switch |
| `devices/dev_pvr.c` | #12, #65, #67, #68 | `CHECK_ALLOCATION` on `ta_commands`; zero-init `wf_*`; **#65** bound STARTRENDER `fb_base`+frame against VRAM before the clear/render (guest→host OOB write, P1); **#67 (perf)** alt-VRAM dirty region extended once **per VRAM bank** (min/max) instead of once per byte; **#68** free the stale old-geometry Z buffer on a resolution change so `pvr_render` can't overflow an undersized `vram_z` (guest→host heap overflow), + `CHECK_ALLOCATION` on the Z alloc |
| `machines/machine_macppc.c` | #23 | **OOB heap read** — `store_buf(boot_string_argument, 256)` over a 1-byte `strdup("")` |
| `net/net_ip.c`, `net/net.c` | #22 | 6× signed-shift UB (`byte<<24`) in TCP/IP byte assembly |
| `promemul/arcbios.c` | #5, #25, #34, #44 | `malloc(0)`→`NULL`; `byte<<24` shift UB; **guest→host OOB** — bound the file handle in `Close`/`Seek`/`Read`/`Write`; **#44** `CHECK_ALLOCATION` on ~10 OOM-only boot-string setup mallocs |
| `promemul/of.c` | #48 | **Guest→host OOB write** in OpenFirmware `call-method` "set-colors" — `memcpy(rgb_palette + 3*color, …)` with `color` an unbounded guest arg (768-byte host palette); reject `color` outside `[0,256)`. Found by static audit + a new in-process OF harness (`of_fuzz.c`); reproduced (color=0x40000 → SEGV @ of.c:180), fixed build returns clean |
| `devices/dev_osiop.c`, `dev_asc.c`, `dev_sgi_mec.c`, `dev_dreamcast_maple.c`, `dev_mb8696x.c`, `dev_pvr.c` | #49–55 | **Device DMA guest→host OOB audit** (this session, 3 parallel audit agents + manual verification): osiop SCSI `DATA_OUT` unbounded heap **write** (#49, CRITICAL); asc DMA `memset` length (#50) and `memcpy` source (#51) bounds; sgi_mec TX length passed to `net_ethernet_tx` (#52); maple `device[port]` index (#53); mb8696x EEPROM index (#54); pvr VRAM texture read (#55) |
| `file/file_macho.c` | #16, #19, #56, #57, #58 | (earlier: symbol/load-command bounds) **#56** bound LC_SYMTAB `nsyms`/`strsize`/`symoff`/`stroff` against the file size before `malloc`/`calloc`/`fread` (was file-controlled → huge/overflowed sizes); corrected the load-command loop bound to `header_size + sizeofcmds`; **#57** replace the blanket `pos+256` load-command guard with **per-command bounds** (it rejected a valid compact `LC_UNIXTHREAD`); **#58** bound the LC_SYMTAB *products* `symoff+12*nsyms` / `stroff+strsize` (the #56 individual-value checks still let a crafted symtab hard-`exit`/OOM); **#62** 256 MB alloc cap (sparse-file OOM); **#63** require `cmd_len >= need`; **#64** size_t alloc/read arithmetic | 
| `cpus/generate_arm_r.c` | #13 | `1<<31` shift UB (build-time generator) |
| `cpus/cpu_dyntrans.c`, `cpu_mips_instr.c`, `cpu_sh_instr.c` | #25, #29, #41, #47 | `1<<(index&31)` + `1<<31` shift UBs; **[P1] dyntrans global-buffer-overflow root-caused & fixed** — a *branch in a branch's delay slot* wiped `EXCEPTION_IN_DELAY_SLOT`, so the outer branch over-advanced `next_ic` past `nothing_call`; detect the nested case at branch entry. **#47** the same bug existed in the **SH4** core (`bt/s`/`bf/s`, found by this session's completeness review, newly reproduced on `testsh`) — same fix applied. Verified: MIPS + SH reproducers no-crash; pmax/arc/sgimips + NetBSD/landisk(SH4) boot (holder removed) |
| `include/misc.h`, `cpus/cpu_{alpha,arm,arm_instr,i960,i960_instr}.c` | #45, #62 | `READ_WORD_LE/BE` macros (uint32_t-cast instruction-word assembly); 9 disassembler fetch sites converted; **#62** added the shared `LOADER_MAX_TABLE_BYTES` (256 MB) loader-allocation cap |
| `cpus/cpu_m88k.c`, `cpu_m88k_instr.c`, `cpu_ppc_instr.c`, `cpu_sh_instr.c` | #36–40, 46 | M88K/PPC/SH decode/execute **signed-shift, shift-by-32 (rotate sh=0), and negative-shift UBs** (6th/7th audit mutation fuzz) — casts/guards; **#46** M88K `ext` sign-extend via unsigned masks + PPC CR-compare `c<<bf_shift` cast (codex replay, 103 findings → 0) |
| `devices/dev_gc.c`, `dev_bebox.c`, `dev_cpc700.c`, `dev_footbridge.c`, `dev_i80321.c`, `dev_irqc.c`, `dev_kn02.c`, `dev_kn02ba.c`, `dev_kn230.c`, `dev_sgi_ip32.c`, `dev_luna88k.c` | #24, #25 | `1<<i` / `byte<<24` interrupt-controller & setup shift UBs → `(uint32_t)` |
| `include/thirdparty/bootblock.h`, `dp83932reg.h`, `pcireg.h`, `sgi_arcbios.h` | #11 | removed `#define __attribute__(x)` neutering (Debian root-cause for the link errors) |
| `cpus/cpu_ppc.c` | #30 | `byte<<24` shift UB in the PPC instruction disassembler |
| `devices/dev_disk.c` | #31 | **Guest→host OOB read/write** in `dev_disk_buf_access` — bound the data-buffer `memcpy` (found by the device-MMIO fuzzer) |
| `devices/dev_mp.c` | #33 | **Guest→host OOB** — `DEV_MP_STARTUPCPU` indexed `d->cpus[]` with a guest value; bound to `[0, ncpus)` (device-MMIO fuzzer) |
| `devices/dev_8253.c` | #35 | **Guest→host OOB** — negative `counter_select` bypassed the `>2` guard into `mode[3]`; mask `(idata>>6)&3` (device-MMIO fuzzer) |
| `core/emul_parse.c` | #32 | **OOB write**: device array sized `MAX_N_DISK`(10) but bounded by `MAX_N_DEVICE`(20) (found by cppcheck) |

## #89–#94 — multi-model review (Codex `gpt-5.5`/xhigh + agy `Gemini 3.1 Pro`/High + Claude)
Three-engine review of the full hardening diff, Claude source-verification, and a consensus rebuttal
loop (all 3 disputed verdicts conceded by both models). Clean rebuild 0/0. Full write-up in
`REVIEW_FINDINGS.md` ("Fifth round").

| File | Corr. | What changed |
|------|-------|--------------|
| `devices/dev_px.c` | #89 | **CRITICAL**, completes OB-3/#72: `if (x2 < x) x2 = x;` before the STAMP `memset(pixels,…,(x2-x)*bpp)` — guest DMA `x2<x` gave a negative→huge width → host stack overflow |
| `cpus/cpu_mips_instr.c` | #90 | Extend the nested-delay-slot guard (#41/#47) to the dyntrans **fused** handlers `beq/bne/b_samepage_addiu` + `beq/bne_samepage_nop` (they still corrupted `next_ic`) |
| `devices/dev_vga.c` | #91 | Completes OB-15/#81: set `modified` only when the in-bounds `memcpy` runs (else `vga_update_graphics` read OOB); `memset(data,0,len)` on out-of-range reads |
| `file/file_aout.c` | #92 | `malloc((size_t)strings_len + 1)` — `uint32_t strings_len==0xffffffff` wrapped `+1` to `malloc(0)` then wrote ~4 GB out |
| `devices/dev_pcc2.c` | #93 | Completes OB-11/#77: `memset(data,0,len)` on out-of-range read (was leaking uninitialized host memory) |
| `devices/dev_pmagja.c` | #94 | Completes OB-12/#78: zero `data[i]` on out-of-range read (uninitialized host-memory leak) |

False positives (rejected via the rebuttal loop, both models conceded): jazz timer mask (#69 is correct), px COPYSPANS `memmove` (`span_len` already clamped), m88k `ext` `o+w>32` (defined; low edge case). Deferred to `OUTSTANDING_BUGS.md` (OB-25/OB-26): diskimage reopen-by-name TOCTOU; osiop `exit(1)` DoS.

## #95 — central uninit-leak fix (Phase A) + #96–#100 (Phase B new-surface audit)
**#95 `cpus/memory_rw.c`** (root-cause): zero the caller's buffer on every device READ before the
len-clamp/dispatch, so a device handler that fills only part of `data` — or whose access is len-clamped —
can never return uninitialised host memory to the guest. Closes the whole class (cf. per-device #91/93/94).

| File | Corr. | What changed |
|------|-------|--------------|
| `devices/dev_kn01.c` | #96 | OB-8b: mask the overlay-palette *read* index `& 15` (16-entry array; the write index was masked in #75, read missed) — guest OOB palette read |
| `disk/bootblock_apple.c` | #97 | bound the partition loop (`ofs+0x40 <= sizeof(buf)`) + `%.32s` — `n_partitions=buf[0x207]` drove a ~130 KB OOB stack read on a malformed Apple-partition disk |
| `devices/dev_vga.c` | #98 | bound `vga_update_graphics` 8-bit/4-bit reads vs `gfx_mem_size` (OOB redraw read; complements #91) |
| `devices/dev_ps2_gs.c` | #99 | **CRITICAL**: reject `regnr (=relative_addr/16) >= N_GS_REGS` — guest 64-bit OOB heap **write** past `reg[264]` |
| `devices/dev_sgi_re.c` | #100 | `buf[4]`→`buf[8]` (bufdepth up to 8 stack overflow) + bound `tile_nr < 256` (re_tlb index) |

Phase B also ran a 3-agent fan-out (PROMs/framebuffers/disk-parsers): PROMs + config parser verified
CLEAN; 7 further agent candidates recorded in `OUTSTANDING_BUGS.md` (OB-27..33). scan-build clean.

## #101–#105 (Phase C deeper audit: network / SCSI / remaining devices)
| File | Corr. | What changed |
|------|-------|--------------|
| `devices/dev_scc.c` | #101 | **CRITICAL**: bound `port = (relative_addr/8) % N_SCC_PORTS` — guest 64-bit OOB heap **write** ~8 KB past `scc_register_w[32]` (0x1000 window → port 511) |
| `net/net.c` | #102 | **CRITICAL**: clamp the ARP/RARP reply `memcpy(lp->data+14, packet, len)` to the 60-byte body — `len` (guest ARP frame length, ~65 KB) overflowed the 74-byte reply buffer in the default NAT config |
| `net/net_ip.c` | #103 | **HIGH**: reject IP packets shorter than IP+L4 headers — a tiny guest IP length field shrank `len` so `net_ip_udp`'s `sendto(..., len-42, …)` underflowed to a huge `size_t` (and ICMP wrote its checksum past the reply) |
| `disk/diskimage_scsicmd.c` | #104 | READ_TOC: allocate `data_in` ≥ 12 (8 fixed header bytes are written) but report only `retlen` — guest alloc-len 0-7 caused an OOB heap write |
| `devices/dev_asc.c` | #105 | guard the never-allocated `incoming_data` in the unfinished non-DMA DATA_IN path (guest-triggerable NULL deref / DoS) |

Phase C also re-verified the dyntrans core + loadstore (nested-delay-slot family incl. #90) and the NIC/
storage controllers CLEAN; 1 candidate deferred (OB-34, SCSI short-CDB `cmd[]` over-read).

## #106–#113 — OB-27..34 remediation (deferred Phase-B/C candidates, all confirmed real)
| File | Corr. | OB | What changed |
|------|-------|----|--------------|
| `devices/dev_fb.c` | #106 | 27 | clip the source column `from_x` in `framebuffer_blockcopyfill` copy (memmove source over-read; via ps2_gif/igsfb) |
| `devices/dev_pvr.c` | #107 | 29 | 24-bit `pvr_fb_tick` copy: wrap start (size_t) + clamp span to `VRAM_SIZE-vo` (was reading past 8 MB VRAM) |
| `devices/dev_ps2_gif.c` | #108 | 28 | TA-putchar: `break` when `addr+3 > len` (`addr=(24+y*xsize)*4` over-read the host DMA buffer) |
| `disk/bootblock_iso9660.c` | #109 | 30 | dir-record walk: require the 8-byte header fits + clamp the name to the remaining `dirbuf` |
| `disk/bootblock_iso9660.c` | #110 | 31 | filename search: `i + strlen(filename) <= len` (was a `size_t` underflow) |
| `disk/bootblock.c` | #111 | 32 | cap disk-controlled `n_blocks` to [1,128] (`fatal()` doesn't exit → int-overflow/malloc-abort) |
| `disk/diskimage.c` | #112 | 33 | `%i`→`%s` for `diskimage_types[type]` in the not-found `fatal()` |
| `disk/diskimage_scsicmd.c` | #113 | 34 | validate `cmd_len` vs the CDB group length before reading fixed offsets (short-CDB `cmd[]` over-read) |

## #114–#115 — OB-25/OB-26 (the last two outstanding candidates → all OB-1..34 resolved)
| File | Corr. | OB | What changed |
|------|-------|----|--------------|
| `devices/dev_osiop.c` | #114 | 26 | skip the SCSI data phase (debug + `else`) when `xferp==NULL` instead of `exit(1)` — guest could halt the emulator |
| `disk/diskimage.c` | #115 | 25 | create the read-only-overlay temp files via `mymkstemp()` (unpredictable name, atomic O_EXCL) + exclusive `.map` — was a predictable-name reopen-by-name TOCTOU |

## #116 — PowerPC extended BAT (IBAT4-7 / DBAT4-7) support (capability add; Codex+agy+Claude consensus)
| File | Corr. | What changed |
|------|-------|--------------|
| `cpus/cpu_ppc.c` | #116a | widen the SPR known-register filter to `SPR_IBAT4U..SPR_DBAT7L` (store the extended BAT SPRs without the spurious `UNIMPLEMENTED` warning) |
| `cpus/memory_ppc.c` | #116b | factor `ppc_bat()` into `ppc_bat_block()` (faithful) + scan base BATs then the extended block at 0x230 — gated on `HID0[HIGH_BAT_EN]` (0x00800000) so non-745x cache-debug SPR writes can't spoof a BAT |

Process: design + HID0-gate resolution + final diff all passed through Codex (gpt-5.5/xhigh) and agy
(Gemini 3.1 Pro), unanimous APPROVE FOR COMMIT. Regression-safe (gate closed → byte-identical behavior);
build 0/0; OpenBSD 3.4/macppc + the full NetBSD/Linux multi-arch sweep all boot. NetBSD 8.2/macppc stays
inert on `-e g4` (advertises MPC7400, never sets HIGH_BAT_EN) — engaging it needs a 745x model (OB-35).

## #117 (OB-35) — MPC7455 CPU model + macppc `g4plus` subtype (engages #116's extended BATs; Codex+agy consensus)
| File | What changed |
|------|--------------|
| `include/cpu_ppc.h` | new `PPC_CPU_TYPE_DEFS` row `{ "MPC7455", 0x80010000, 32, 0, 15,5,8, 15,5,8, 18,5,8, 1 }` |
| `include/machine.h` | `#define MACHINE_MACPPC_G4PLUS 4` |
| `machines/machine_macppc.c` | `G4PLUS`→"MPC7455" in MACHINE_DEFAULT_CPU; register `-e g4plus` subtype |

Purely additive (`-e g4`/7400 + g3/g5 untouched). With `-e g4plus`, NetBSD 8.2/macppc sets HID0[HIGH_BAT_EN]
so #116's extended BATs engage (verified, gate-opened=1) and it advances past the MMU; it then stalls at
GXemul's skeletal OpenFirmware (separate, open-ended work). Both Codex (gpt-5.5/xhigh) + agy (Gemini 3.1
Pro) APPROVE FOR COMMIT; build 0/0; OpenBSD 3.4/macppc boots on g4 AND g4plus; full multi-arch sweep + pmax
+ arc regression-clean.

## #118 / #119 / #101 / #114 — course-correction: silent host-safety masks made LOUD (Codex+agy+Claude consensus)
Per the author's "warn-visibly-and-continue, never silently hide a fault" ethos (see REVIEW_FINDINGS "Twelfth
round") + the user's directive (keep ALL security bounds for unvalidated ROMs, add just-enough rate-limited
verbosity, never crash). No security bound removed.
| File | Corr. | What changed |
|------|-------|--------------|
| `devices/dev_osiop.c` | #118 | NULL guards in read_word/read_byte/write_byte + `osiop_hostpage_fault()` (warn-once + stop-script) + early-return in execute_scripts_instr — fixes a real host NULL-deref crash |
| `devices/dev_osiop.c` | #114 | NULL-`xferp` data phase: quiet skip+fake-completion → warn-once + stop-script + return (no fake, no exit) |
| `devices/dev_scc.c` | #101 | `% N_SCC_PORTS` alias → bounds-check + NO-OP out-of-range + warn-once (security kept, no aliasing) |
| `devices/dev_disk.c, dev_pcc2.c, dev_vga.c, dev_pmagja.c, dev_ps2_gs.c, dev_pvr.c`, `net/net.c` | #119 | loud-once `fatal()`/first-N on each previously-silent OOB skip/zero/clamp |

Rate-limited with `static` first-N guards (GXemul is single-threaded) so a hostile ROM cannot flood. `#95`
(generic memory_rw zero-fill) left unwarned by consensus (would flood benign boots). Regression: gcc 0/0 +
**clang 21 0/0 in all changed files**; full sweep + pmax deep (osiop/disk/net) + arc clean, 0 spurious
warnings in normal operation.

## How findings were produced
1. Manual review + `gcc -fanalyzer` over all 265 TUs.
2. ASan/UBSan mutation-fuzzing of the file loaders (a.out/ELF/Mach-O) and an in-process
   harness for the network stack (`net_ethernet_tx`).
3. "Run every machine under ASan" sweep (23 machine types) — found the macppc heap OOB.
4. Triage of five independent external fuzz audits (6,772-case corpus).
5. Functional validation: 10 guests across 5 CPU arches + 3 OS families; per-device
   runtime fuzz (real guests booted under ASan).
6. **In-process device-MMIO fuzzer** — sets up a real machine and drives every device's
   access handler with mutated register writes (found the dev_disk OOB, #31); plus an
   ARCBIOS PROM-call fuzzer.
7. **cppcheck** static analysis (found the emul_parse OOB, #32); **LeakSanitizer** +
   **Valgrind** on a guest boot (no leaks; 0 invalid reads/writes).
8. **Latest external-audit round (#57–#61)** — focused Mach-O/ECOFF/gzip regressions;
   every fix re-verified by replaying the audit's own focused cases against the rebuilt
   binary (see Validation) and by a fresh clean `make -j`.

## Validation results
- Loaders: fuzz-clean (420 ELF/a.out + 150 Mach-O cases); the external audit's 367→**12**
  ASan signatures on est, the last batch (ELF over-allocation) addressed by #26.
- Network: 500,000 mutated packets — 0 ASan / 0 UBSan.
- Machine setup: 23 machines ASan-clean (only macppc had a memory bug; fixed #23).
- Guest boot (5 CPU arches, 3 OS families): NetBSD/pmax (MIPS R3000) → sysinst; arc
  (R4000), hpcmips (VR4100), sgimips (R10000), algor (RM5200), macppc (PPC G4),
  landisk (SH4), cats (ARM SA-110); **OpenBSD/luna88k (M88K)**; and **Linux 3.2/Malta
  (MIPS 5Kc)** all boot — the fixes are behavior-preserving.
- Baseline now builds too: the `-fgnu89-inline` probe was propagated to the root
  `configure`, and `src/` + root `configure` compiles clean in WSL (verified).
- Per-device runtime fuzz: NetBSD booted under ASan on pmax/sgimips/cats/landisk —
  **0 device memory errors** (real drivers exercising asc/le/fb/mec/crime/footbridge/…).
- 3rd audit: est is **ASan-clean across 6,772 cases**; the 102 UBSan signatures all
  traced to the `unencode` macro (#27) and are now resolved.
- ELF fix #26 re-confirmed: the audit's 10 crashing ELF cases → 0 ASan crashes.
- **#57–#61 (latest round):** replayed the audit's focused PPC Mach-O + ECOFF cases on
  the rebuilt `build/gxemul`: the compact `LC_UNIXTHREAD` (204 B) now executes (was
  *"No entry point? Aborting"*); both symtab "extend past EOF" cases now skip the bad
  symtab and continue (were a hard `exit(1)`); ECOFF `huge`/`1000`-symbol cases report
  `[ ECOFF: bogus f_nsyms/f_symptr ]` and skip (was OOM); truly-truncated / `cmd_len==0`
  Mach-O cases are still rejected; a gzipped ELF loads identically to raw. The flaky
  `autodev.c` build race is gone (24 concurrent generator runs all correct; `make -j`
  reliable).
- **#62–#66 (this session):** primary build still **0/0**; the #62 cap rejects a 512 MB
  file with a 360 MB symtab in 46 ms (no 360 MB alloc); the full focused regression set
  is unchanged after #63/#64/#66 (no regressions); a real `-fsanitize=address,undefined`
  rebuild (103 MB) runs the loader cases with **0 memory errors** (only benign exit-time
  LeakSanitizer leaks). #65 (PVR P1) is verified by inspection + clean build/ASan;
  runtime trigger needs a Dreamcast guest. NB: `audit-results-20260627_current-review/`
  holds **pre-fix** snapshots whose recorded outputs predate these fixes.
- **#67 (perf, user-approved):** compiles 0/0 and the loader regression set is unchanged;
  the alt-VRAM render path needs a Dreamcast guest to exercise at runtime. Behavior-wise it
  marks the same dirty line range except for writes straddling the visible-FB edge (a few
  extra lines, redrawn identically). **#67 refined** to per-bank min/max so a write touching
  both 4 MB VRAM banks no longer dirties the gap between them.
- **#68 (PVR stale Z-buffer, external proposal):** compiles 0/0; the inverted
  `pvr_geometry_updated()` condition is fixed so a guest resolution change frees the
  old-geometry `vram_z` and `pvr_render` reallocates it (no overflow). Runtime trigger needs
  a Dreamcast guest (verified by inspection + clean build).
- **Mach-O #2 robustness (codex caveat):** the symtab `fseek`s now cast offsets
  `(long)(uint32_t)` (file_macho.c:269/278), so a *valid* large file with an offset
  ≥ 0x80000000 seeks correctly instead of negative (the compatibility gap codex flagged) —
  builds 0/0. The full `int32_t`→`uint32_t` *re-typing* of the fields was still NOT applied:
  it would make `for (i=0; i<nsyms; i++)` a `-Wextra -Wsign-compare` warning, regressing 0/0,
  and the memory-safety was already covered (#58 rejects bogus offsets/counts, #64 `size_t`
  alloc, #62 256 MB cap).
- **#69 (arc/Jazz interrupt-enable mask, correctness — enables OpenBSD/arc; found with Codex gpt-5.5/high):**
  `dev_jazz.c`'s R4030/PICA interrupt controller forwarded JAZZ interrupts to the MIPS IRQ lines *without*
  consulting `int_enable_mask`: `jazz_interrupt_assert()`/`deassert()` asserted `mips_irq_3` (JAZZ 0..14) and
  `mips_irq_6` (JAZZ 15 = the interval timer) unconditionally, and `DEVICE_TICK(jazz)` gated the timer on the
  wrong bit (`& 2` — the long-standing `/* Hm? */` "mask seems shifted" TODO) instead of JAZZ int 15 = `0x8000`.
  Effect: the free-running 100 Hz Jazz timer delivered a clock interrupt before the guest enabled it, so
  OpenBSD/arc 2.3 ran `hardclock` before `cpu_initclocks()` and faulted (null-deref at `[0]+0xb8`). Fix: add
  `PICA_TIMER_IRQ_MASK (1<<15)`, gate assert/deassert + DEVICE_TICK + the `EXT_IMASK` recompute on
  `int_asserted & int_enable_mask & {0x7fff, PICA_TIMER_IRQ_MASK}`, and route the pending-tick assert through
  `jazz_timer_irq`. **OpenBSD/arc 2.3 now boots to the kernel idle loop on 0.7.0** (previously only gxemul
  ≤0.3.6 worked — a regression introduced by the 0.3.7 dyntrans timer rewrite). **pmax-safe:** DECstation
  (pmax) instantiates `dev_mc146818`, not `dev_jazz`, and is R3000/EXC3K — re-verified pmax still boots
  multiuser with the same binary. Builds 0/0. (NB: edit est/build sources *from WSL* — Windows-side writes lag
  the WSL 9p view and `make` silently links stale `.o`; this masked the fix for many iterations.)

## Outstanding-bug remediation (#70–#88, dual Codex gpt-5.5 *xhigh* review + independent source audit)

A read-only Codex review (captured in `OUTSTANDING_BUGS.md`, OB-1..OB-24) surfaced 24 candidate
issues. Each was independently verified against the current source and triaged: **19 real bugs fixed
(#70–#88), 3 false positives left, 1 deferred, 1 intentionally skipped.** All build `gcc -O3 -Wall
-Wextra` 0/0; the pmax rig (boot→multiuser→root login→halt) and the arc rig (OpenBSD/arc 2.3 ELF +
ECOFF kernels load past the #69 hardclock point to the interactive console) were re-verified with the
fully-patched binary.

Two dominant root patterns: **(A) end-span** — a handler checks the *start* offset is in range, then
copies/indexes `len` bytes (`addr < size`, then `memcpy`/index `len`); **(B) window>backing** — a
device is registered with an MMIO window larger than its backing array, so `memory_rw.c`'s clamp to
the *window* still permits OOB into the smaller buffer. The high-severity class is guest→host OOB
*writes*. The canonical end-span guard used throughout is
`if (relative_addr >= SIZE || len > SIZE - relative_addr) return 0;` (cast deliberately to keep
`-Wsign-compare` clean).

- **#70 (OB-1, `dev_fb.c`, end-span, High):** `dev_fb_access()` checked `relative_addr >=
  framebuffer_size` but then indexed `framebuffer[relative_addr + i]` for `len` bytes. Added the span
  clause. Direct callers (DEC TGA `dev_dec21030`, `dev_sgi_mardigras`, `dev_pmagja`) call this
  *without* going through `memory_rw.c`'s clamp, so it is reachable. pmax uses dev_fb (serial-console
  rig unaffected) — re-verified.
- **#71 (OB-2, `dev_px.c` SRAM, window>backing, High):** the VDAC/SRAM aperture is registered as
  512 KiB (`0x200000..0x280000`) but `d->sram` is only 128 KiB; the write loop did
  `d->sram[relative_addr - 0x200000 + i] = data[i]` with no upper bound → guest→host heap OOB write.
  Bounded the per-byte index to `sizeof(d->sram)`.
- **#72 (OB-3, `dev_px.c` STAMP DMA, High):** the PixelStamp span-copy / fill (erasecols) / putchar
  paths build framebuffer pointers from guest-supplied, frequently signed-and-`%=`-negative
  coordinates (`span_dst*PX_XSIZE`, `(fb_y*PX_XSIZE+x)`, `(y+suby)*PX_XSIZE+x`). Guarded each of the
  three framebuffer `memmove`/`memcpy` writes with an explicit in-bounds row/column check (conservative
  — over-restrictive on bogus coordinates, never host-OOB; the `pixels[16]` source read is also
  bounded). PX is a TURBOchannel option (not pmax/arc); compile-verified, not runtime-fuzzed.
- **#73 (OB-6, `dev_adb.c`, unbounded append, High):** the VIA/ADB `DIR_OUTPUT` path did
  `output_buf[cur_output_offset++] = c` with no bound (the `DIR_INPUT` path *is* bounded), so a guest
  toggling the shift register past 100 bytes overruns the 100-byte buffer. Bounded against `MAX_BUF`.
- **#74 (OB-7, `dev_igsfb.c`, palette index, High):** `palette_write_index` is set directly from
  guest data and post-incremented, then used to index the 256-entry `rgb_palette[256*3]` → OOB. Masked
  the index (set + auto-increment) to `& 0xff`.
- **#75 (OB-8, `dev_kn01.c`, overlay palette, High):** the VDAC `OVERWA` register sets
  `cur_write_addr_overlay` from a guest byte (0–255), then `memcpy(rgb_palette_overlay + 3*addr, …, 3)`
  into a 16-entry overlay palette → OOB write. Masked the address to `& 15`.
- **#76 (OB-9, `dev_sgi_mardigras.c`, end-span, High):** the microcode-RAM subregion checked
  `relative_addr < MICROCODE_END` (start only) then `memcpy(microcode_ram ± relative_addr, …, len)`;
  `memory_rw.c` clamps to the *whole* device, which is larger than the subregion. Added
  `len <= MICROCODE_END - relative_addr` to the gate.
- **#77 (OB-11, `dev_pcc2.c`, end-span after modulo, High):** `relative_addr %= PCC2_SIZE` folds the
  *start* into the 0x40-entry `pcctwo_reg`, but `memcpy(…, len)` (read at the top, write in the
  T1/T2 timer cases) can still span past the array end. Bounded both copies to `relative_addr + len
  <= PCC2_SIZE`.
- **#78 (OB-12, `dev_pmagja.c`, window>backing, High):** the handler indexed `pixeldata[]`
  (`1280*1024`) from a guest offset `>= 0x200000` with no upper bound. Added `ofs < XSIZE*YSIZE`.
- **#79 (OB-13, `dev_sgi_gbe.c`, palette cache index, High):** `selected_palette[color_index]` used a
  `color_index` that ranges over 32 palettes (`cmap<<8`) to index the 256-entry cache. Masked to
  `& 0xff`.
- **#80 (OB-14, `dev_sgi_gbe.c`, tile over-read, High):** the per-line tile read length
  (`partial_pixels * bytes_per_pixel` for partial tiles) can exceed the `uint8_t fb_buf[512*3]`
  per-line size. Clamped the line length to 512 (the documented "up to 512 bytes from the tile").
- **#81 (OB-15, `dev_vga.c` 8-bit aperture, window>backing, High):** the GRAPHICS_MODE_8BIT
  `memcpy(gfx_mem ± relative_addr, …, len)` was bounded only by the 0x18000 aperture, not by
  `gfx_mem_size` (which is smaller in low resolutions). Bounded both copies to `gfx_mem_size`. arc/pica
  instantiates `dev_vga`; legitimate in-mode offsets still work.
- **#82 (OB-16, `dev_vga.c` CRTC textmode, High):** the guest-controlled CRTC start address
  (`VGA_CRTC_START_ADDR_*`) becomes `base`, then `vga_update_text()` and `vga_update_textmode()` index
  `charcells[base+i]` **and** `[base+i+1]` over `[start..end]` with no `base` bound → OOB read past the
  charcells heap on the next text redraw. Added `-Wsign-compare`-safe `base`/`end` clamps in both the
  caller (size_t) and the helper (int params, cast), fixing the `+1` off-by-one Codex's draft missed.
  arc/pica uses VGA — re-verified the arc boot.
- **#83 (OB-17, `dev_dec21143.c` Tulip TX, Medium):** a guest chaining TX descriptors without a
  final-segment flag grows `cur_tx_buf` via `realloc(cur_tx_buf_len + bufsize)` unboundedly (and
  overflows the `int` length). Capped the accumulated frame to 64 KiB in both the first-segment
  (`malloc`) and continuation (`realloc`) branches.
- **#84 (OB-18, `file_android.c` loader, Medium):** `page_size` is read from the boot.img header and
  used as a divisor (`kernel_size / page_size`) and seek multiplier with no validation — `page_size==0`
  is a div-by-zero, large values overflow the 32-bit page math. Reject non-power-of-two / out-of-range
  (`2048..65536`) page sizes up front.
- **#85 (OB-19, `file_elf.c` loader, Medium):** the PT_LOAD copy cursor `ofs` is `int` but compared
  against the file-controlled `uint64_t p_filesz` and advanced by up to 0x10000 per step — a segment
  ≥ 2 GiB overflows `ofs` to negative → infinite loop + wild `p_vaddr+ofs` writes. Widened `ofs` to
  `uint64_t` and made the tail-length clamp overflow-safe. Validated: the arc ELF kernel still loads
  (symbols resolve, runs to the console).
- **#86 (OB-20, `dev_dreamcast_gdrom.c`, Medium):** a guest GD-ROM read derives `d->cnt = 2048 *
  sector_count` (sector_count up to 0xffffff) which drives `alloc_data()` → multi-GiB allocation /
  overflow; the mismatch path also `exit(1)`s (guest-triggered abort). Reject `sector_count` outside
  `1..32` (64 KiB) and replaced `exit(1)` with `break`.
- **#87 (OB-21, `dev_dreamcast_g2.c`, subobject OOB, Medium):** the extdma register window is
  registered as 0x100 but `extdma_reg[]` is only 0x80 worth (32 words); accesses at 0x80..0xff index
  past it into the adjacent struct member. Added a parallel `extdma_high_reg[]` and route
  `relative_addr & 0x7f` to the correct array.
- **#88 (OB-23, `dev_sgi_re.c`, Low):** the zero-fill loop subtracted the full `sizeof(zerobuf)`
  (4096) from `dstlen` each iteration even when the actual `fill_len` was shorter (page/tail), so
  `dstlen` can wrap and the loop over-runs. Subtract the bytes actually filled.

### Triaged but NOT changed (this review)
- **OB-4 / OB-5 / OB-10 — false positives.** `cpus/memory_rw.c:288` clamps `len` to the remaining
  device bytes (`if (paddr+len > dev.length) len = dev.length - paddr`) *before* calling the handler,
  and `pvr_vram` / `asc_dma` / `ether_buf` are each registered with length == backing-buffer size and
  have no direct (non-`memory_rw`) callers — so the apparent end-spans in those handlers are
  unreachable. (Batch-2 speculatively added guards here; they were reverted once the clamp was
  confirmed, to keep the patch honest.) The window>backing bugs above are real precisely because their
  registered window is *larger* than the backing array.
- **OB-22 (`dev_jazz.c` jazzio vector read) — deferred.** Reading the interrupt-source register
  reports a vector but does not clear `int_asserted` and unconditionally `INTERRUPT_DEASSERT`s
  `mips_irq_3` ("needed by Windows NT during startup"). This is an emulation *correctness* issue, not a
  host memory-safety bug, it is medium-confidence, and it sits in the exact arc interrupt path just
  stabilized by #69 — deferred to avoid regressing the verified arc boot; revisit with dedicated arc
  interrupt testing.
- **OB-24 (signed `byte<<24` in CPU instruction cores) — skipped**, consistent with the existing
  decision below (UBSan-only, hottest path, no exploit path; the shared decoder is already fixed in #27).

## Not changed (assessed, intentionally left)
- ELF64 `st_name` "truncation" — **false positive**: gxemul's `exec_elf.h` defines
  `Elf64_Half = uint32_t` (32-bit), so it is not truncated.
- Signed `byte<<24` assembly in the **CPU instruction cores** (e.g. `cpu_arm_instr_loadstore.c`,
  found via the per-device runtime fuzz) — UBSan-only, deterministic, hottest code path. The
  shared file-decoder source (`unencode`) is now fixed (#27); the per-arch instruction load/store
  assembly is left (whack-a-mole across every core, no real bug).
- a.out timeout signature — the emulator *running* a loaded garbage program until timeout
  (expected behaviour, not a loader bug).
