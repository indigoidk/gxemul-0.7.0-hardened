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

## #120–#129 — feature round (TODO items) + SuperH alignment
Additive capability work drawn from upstream's `doc/TODO.html`, each regression‑gated:
- **SuperH unaligned‑access exceptions (#124)** and **64‑bit `fmov` 8‑byte alignment (#129)** — the SH4
  now raises the correct address‑error exception for misaligned loads/stores (parity with the other cores).
- **Multi‑track CUE/BIN CD images (#127)** — real per‑track sector mapping (MODE1/MODE2, 2048/2352/2336),
  read‑only, with per‑sector raw‑header stripping.
- **testmips RAM above 256 MB (#120)** — a 32‑bit guest can use up to ~3 GB via a high‑RAM/mirror map.
- **Subsystem debug breakpoints (#128)** — `debugmsg` can drop into the debugger when a chosen subsystem
  emits at/above a verbosity level.
- **Debugger conveniences (#122/#125/#126)** — step‑into‑call, `find`/`put`, expression‑parser and
  dump/disassemble‑range fixes.

## #130–#154 — full‑project multi‑model review + remediation
A whole‑codebase (not just recent‑changes) adversarial review of the core‑critical subset — the four CPU
instruction cores, the shared dynamic‑translation engine, the guest→host memory boundary + main loop, the
file loaders, network, disk, debugger, and the highest‑risk devices — explicitly weighing the original
author's *warn‑loudly / never‑silently‑mask / never‑crash‑on‑untrusted‑guest* ethos and the `doc/TODO.html`
wishlist. **Method:** parallel per‑subsystem Claude review agents → three independent cloud models
(GLM / DeepSeek‑V3 / Qwen3‑Coder) cross‑checking the top findings against the code → a Claude adjudicator
ruling every finding against the actual source and the pristine baseline. **~23 confirmed fixes; no false
positives survived; every confirmed bug is pre‑existing in the baseline** (the ~119‑item pass had not
reached them). The cores it *had* hardened — the dyntrans engine, the `memory_rw` boundary, and the
ELF/ECOFF/Mach‑O/a.out loaders — were re‑confirmed sound.

- **#137 (CRITICAL) — `cpus/cpu_mips_instr.c` `memset_addiu_bne_sw`.** `bytes_to_write = rY - rX` (unsigned)
  underflowed when a guest set *end < start*, and the page‑boundary clamp `(rX&0xfff)+bytes_to_write > 0x1000`
  itself wrapped mod 2^N → a **direct multi‑gigabyte `memset` into the host page** (bypassing the `memory_rw`
  clamp). Guest‑triggerable on pmax. **Fix:** fall back to the slow path when `rY < rX`.
- **#145 (HIGH) — `devices/dev_pvr.c`.** The framebuffer‑refresh copy was clamped to guest DIWSIZE geometry
  but not to the fixed 672×512 host framebuffer → guest→host heap **write**. **Fix:** also clamp to the host
  framebuffer's inner drawable area (proven bound).
- **#149 (HIGH) — `file/file_srec.c`.** A non‑hex byte survives (the loader warns but continues), so a record
  `count` reached 4335 against a 270‑byte buffer → ~4 KB host‑stack **over‑read** into guest RAM. **Fix:**
  clamp `count` to the actual parsed length (the parse loop is provably bounded).
- **Medium:** `#133` guest‑set SCSI `logical_block_size` overflow → OOM‑`exit(1)` (validate + 64‑bit math);
  `#130` TCP timestamp‑option over‑read echoed to the guest (length‑gate); `#141` PPC Time‑Base‑Upper never
  incremented (mask like DEC); `#146` five recoverable `dev_osiop` `exit(1)`s → warn‑once + stop the local
  engine; `#150` `free()` on an `mmap`‑backed `cpu` → `munmap`; `#136` uncapped boot‑image sizes → capped.
- **Low / hardening:** a `%s`‑with‑no‑argument trace format; two more small guest→host over‑reads (odd‑length
  ICMP checksum, short ARP); a NULL‑deref idle path; two missing nested‑delay‑slot guards; the inverted SH4
  store‑queue privilege test; SH FDIV‑by‑zero now yields the IEEE result; a debugger divide‑by‑zero guard;
  `strtoll`+range validation for numeric CLI options; a gzip temp‑file leak; residual signed‑shift UB casts;
  and a rate‑limited note on the device length‑clamp.

**Deferred (confirmed, but neither is a host‑safety issue and each fix's risk outweighs its low severity):**
a double‑precision op on an *odd* FP register (stays within the FP register union — not a host OOB), and the
nested‑delay‑slot guard being silent (already host‑safe; raising the architectural slot‑exception would be a
guest‑visible behaviour change across ~18 hot handlers).

**Verification:** build 0 errors / 0 warnings; a 9‑machine multi‑architecture boot sweep (all boot, no
regressions); the OpenBSD/pmax rig (full boot + root shell + NAT ping + clean halt); and a positive test
showing the S‑record loader now clamps the crafted over‑long record while a valid record still loads cleanly.

## Fifteenth round (#155–#177) — Codex 5.6-Sol-Ultra review, Fable-verified (ported from est/)
A whole-tree security review by **Codex CLI `gpt-5.6-sol`/ultra** (report
`../harness/codex_sol_ultra_to_fable.md`) raised **21 findings**; **4 parallel Fable verifiers** independently
confirmed **all 21 REAL, 0 false positives** against the real code + the pristine baseline; **4 Fable fixers**
applied minimal, ethos-matched corrections, plus **2 same-class companions** (#176/#177). These were developed and
build-verified in `est/` and **ported here byte-identically** — the full per-correction table is in
`../est/CHANGELOG.md` (Fifteenth round). `Cdx.N` = finding N in the Codex report.

Headlines — **3 CRITICAL:** #155 (`memory_rw.c`: a partial device page got a full-page dyntrans fast-mapping →
guest OOB r/w, bypassing #70), #156 (`dev_fb.c`: `dev_fb_resize` int-overflow → undersized `malloc` then OOB
write), #157 (`dev_fb.c`: fb realloc left stale dyntrans pointers → UAF; fixed centrally in `dev_fb_resize`).
**2 HIGH:** #158 (CUE `FILE "../.."` → arbitrary host-file read, new authority from #127), #159 (tape READ
uninitialized-heap disclosure to the guest). Then a MEDIUM tier (#160–#171, #176: PVR OOB read, short-IPv4
over-read, uncapped SCSI alloc, overlay `abort()`, GD-ROM/PVR guest-`exit(1)`, SCSI-phase NULL deref, cyclic-EBR
hang, fused-MIPS starvation, a.out/android loader OOM) and a LOW tail (#172/#174/#175/#177: PS2-GIF stack
over-read, PPC extended-BAT fidelity gate — no host escape, `mmap` vs `MAP_FAILED`, DHCP debug over-read).
Guest-reachable `exit(1)`/`abort()` were converted to log-and-continue per the #118/#119 ethos. **Deferred:** #173
(overlay reopen-by-name TOCTOU) — assessed, not a cross-user hole.

**Build & regression (this fork):** `GXEMUL-SEC/src` builds **0 errors / 0 warnings** (`make -j12`, WSL Gentoo /
gcc 15.2.1, 2026-07-09); the rebuilt binary is installed as the **arc and pmax rigs' `gxsec-gxemul`**; the pmax
OpenBSD-2.2 rig boots multiuser on it — root login, `le0` NAT ping 0% loss (3/3), clean halt — **no regression**.

## Sixteenth round (#178–#181) — NE2000 / NAT hardening (Codex 5.6-Sol-Ultra NE2000 review, Fable-verified)
Codex `gpt-5.6-sol`/ultra reviewed the new arc NE2000 NIC (`src/devices/dev_ne2000.c`, 662 lines) plus its NAT and
Jazz-interrupt surface (report `../harness/codex_ne2000_to_fable.md`): 4 findings, **all confirmed REAL by a Fable
verifier (0 false positives), 0 CRITICAL** — the device's earlier panel fixes (RX FCS page-count, lost-interrupt
race, every card-memory access bounds-checked via `ne_mem_readb/writeb`) were re-confirmed sound.

| # | ID | Sev | File — fix |
|---|-----|-----|------------|
| **#178** | Cdx-NE.1 | **HIGH** | `net/net.c`+`net/net.h`, `devices/dev_ne2000.c`: unbounded NAT reply queue — a guest whose NE2000 receiver is disabled (`STP` / `RCR.MON`) enqueues replies that never drain → host OOM / `exit(1)`. **Fix:** per-`net` queued-packet counter + `NET_MAX_QUEUED_PACKETS` (256) drop-oldest cap; **and** the NE2000 drains its queue per-tick while stopped/monitor and makes CR `STP` dominate `STA` (rejects TXP while stopped) — closing both trigger variants. |
| **#179** | Cdx-NE.2 | MED | `devices/dev_jazz.c`: guest-reachable unconditional char-by-char `fatal()` on `R4030_SYS_CONFIG` / undefined offsets (host-output stall / log-fill DoS). **Fix:** ignore / return-0 + a once-only `debugmsg` (#119 idiom). |
| **#180** | Cdx-NE.3 | LOW | `devices/dev_ne2000.c`: `TPSR=0xff` TX source span aliases (16-bit wrap) into the station PROM, emitting card-private bytes as a valid frame. **Fix:** wide-arithmetic span check (`NE_RAM_START..NE_RAM_END`, `len ≤ NE_MAX_TX`) → set `TXE`, clear `TXP`, do not transmit. |
| **#181** | Cdx-NE.4 | LOW | `devices/dev_ne2000.c`: remote DMA kept accessing card RAM after `RBCR` reached 0 (a wide data-port access over-wrote past the count). **Fix:** early-out in `ne_dma_readb/writeb` when `rbcr==0` (no access, no `rsar++`; reads 0xff; RDC latch kept). |

Severity note: #180/#181 are hardware-fidelity / hardening — **no host OOB** (the aliased bytes are the
already-guest-readable PROM; the DMA over-write lands in RAM the guest already owns). **Build & regression:** builds
**0 errors / 0 warnings** (gcc 15.2.1, 2026-07-10); the rebuilt binary is the rigs' `gxsec-gxemul`; **both rigs
regression-pass** — pmax `le0` and arc NE2000 `ed0` each ping 0% loss + clean halt (the queue cap does not perturb
normal networking).

## Seventeenth round (#182–#187) — full-tree Codex 5.6-Sol-Ultra review + Fable panel (fb-resize CRITICAL)
A whole-tree adversarial re-review: **Codex `gpt-5.6-sol`/ultra** returned 17 findings, cross-checked against a
4-reviewer **Fable panel**, each finding source-verified by Fable. The panel had independently cleared the
memory-safety surface, so the headline is a **seam bug the area-partitioned panel missed and the holistic Codex pass
caught**: on a framebuffer *shrink*, `dev_fb_resize()` swaps the data pointer but leaves the device's registered
`length` stale, so the #155 dyntrans fast-map gate maps past the new, smaller allocation. This round fixes the
CRITICAL + the HIGH + the clean part of the guest-`exit(1)` cluster; the render-loop `exit(1)`s and the remaining
Codex medium/lows are triaged in `OUTSTANDING_BUGS.md`.

| # | ID | Sev | File — fix |
|---|-----|-----|------------|
| **#182** | Cdx.1 | **CRITICAL** | `core/memory.c`+`include/memory.h`, `devices/dev_fb.c`: `dev_fb_resize()` called `memory_device_update_data()` (swaps only the dyntrans data pointer) but never shrank the device's registered `length`; the #155 fast-map gate `(paddr|mask) < length` then trusted the OLD length and installed a writable host mapping past the end of the new, smaller framebuffer → guest-controlled OOB host write (e.g. SGI O2/GBE `HCMAP` shrink 1280→640, then touch offset 0x200000). Latent in pristine upstream. **Fix:** new `memory_device_update_length()` keeps `length`/`endaddr`/`mmap_dev_maxaddr` in sync on resize; the existing #157 cache-invalidate then drops stale fast-path pointers. |
| **#183** | Cdx.2 | **HIGH** | `console/x11.c`: `x11_fb_resize()` computed the XImage allocation `new_xsize*new_ysize*alloc_depth/8` in 32-bit `int`; a guest-reachable resize within #156's 16384/axis cap (e.g. 12000×12000×32bpp) overflows `int`, under-allocates, then `XPutPixel` overruns the buffer → host heap corruption on X11 builds. **Fix:** widen the arithmetic to `size_t`. |
| **#184** | Cdx.4 | MED | `devices/dev_fb.c`: the `dev_fb_resize()` too-small (`<10`) branch still did `exit(1)`; guest-reachable via GBE `HCMAP`/`VCMAP` written with a tiny/zero dimension → emulator-abort DoS. **Fix:** reject and keep the old framebuffer (return), matching the sibling `>16384` branch (#156 idiom). |
| **#186** | Cdx.6 | MED | `devices/dev_mb89352.c`: a valid guest `SCMD_XFR` with an unimplemented `PCTL` phase (4/5/6) hit `exit(1)`. **Fix:** log + `break` (#119 idiom). |
| **#187** | Cdx.7 | MED | `devices/dev_pvr.c`: eight guest-reachable PVR **MMIO register-write** `exit(1)`s (STARTRENDER read; OB_ADDR / TILEBUF_ADDR / TA_OPB_START / TA_OB_START unknown-bit; DIWCONF magic; TA access-len; and the default unhandled-register case). **Fix:** log-and-continue (mask-and-`DEFAULT_WRITE` / `break`), matching #166/#176. |

Provenance/severity: **#182 CRITICAL** overturns the Fable-panel-only "memory-safety clean" read — a genuine
guest→host heap-overwrite, latent in pristine upstream, exposed by any framebuffer that shrinks (SGI GBE, or
`fbctrl`). **#183 HIGH** is X11-build-only. #184/#186/#187 are availability (`exit(1)`) DoS, converted per the fork's
#118/#119 log-and-continue ethos. **Deferred (documented in `OUTSTANDING_BUGS.md`, not silently dropped):** the ASC
`data_out_len==0` `exit(1)` (#185 — needs a structural transfer-skip), the four PVR render/texture-loop `exit(1)`s
(dev_pvr.c 868/1084/1245/1419), and Codex's remaining medium/lows (CUE symlink-follow, cross-memblock invalidation,
overlay silent-fail, Jazz LB_IE / dual-pending IRQ, ARC partition signed-`*512`, TCP-debug over-read, NE2000 TX
log-flood, `dev_ram` MAP_FAILED). **Build:** incremental **0 errors / 0 warnings** (gcc 15.2.1, `-Wall -Wextra`);
applied byte-identically to `est/` and `GXEMUL-SEC/`. Rig regression run (pmax/arc boot) pending.


## Eighteenth round (#188–#209) — accuracy/debuggability pass: Codex 5.6-Sol-Ultra + Fable panel
A fresh full-tree adversarial re-review (**Codex `gpt-5.6-sol`/ultra**, 17 findings, cross-checked by a
4-reviewer **Fable panel** + this session's per-site source verification) against a narrowed brief: *not* new
hardening for its own sake, but changes that make the emulator behave more like real silicon **and** stay
debuggable, in the fork's `exit()`→graceful ethos. Every correction converts a guest-reachable
`exit()`/`abort()`/host-crash on guest-controlled state into a hardware-plausible fault or a bound, or fixes a
guest→host OOB. All 21 tags (#188–#208) + the #209 add/sub cleanup verified present+matched in **both** `est/` and `GXEMUL-SEC/`; the shared code is
byte-identical, and the `arcbios.c`/`diskimage.c` edits land in the two trees' shared regions (the SEC
ARC-enablement layer is untouched). **Build: incremental 0 errors / 0 warnings** (gcc 15.2.1, `-Wall -Wextra`).
Cross-model convergence: the **ARC PROM `Read`/`Write` unbounded-`malloc` DoS (#192)** was found independently by
Codex (F12), the Fable SEC-surface reviewer, and this session; the **R4000 PageMask host-exit** came from both
sides — Codex's write-path root cause (#188) and Fable's translate-path (#189).

### MIPS / CP0 + PROM (the pmax + arc audit path)
| # | Sev | File — fix |
|---|-----|------------|
| **#188** | MED | `cpus/cpu_mips_coproc.c`: an invalid, non-contiguous `COP0_PAGEMASK` was only *warned* on write, then stored; `tlbwi` copied it into the TLB and the walker's mask `switch` hit `default: exit(1)` — guest-reachable host DoS. **Fix:** canonicalize the invalid mask to the minimum page size on write (real R4000 latches only defined mask bits). |
| **#189** | MED | `cpus/memory_mips_v2p.c`: the same walker `default: exit(1)` on a non-standard mask (also reachable on R4100, which #188 does not canonicalize). **Fix:** `goto exception` → a normal TLB refill so the guest faults and the emulator stays alive/debuggable. |
| **#190** | MED | `cpus/cpu_mips_coproc.c`: `TLBWR` computed `random() % (nr_of_tlbs - COP0_WIRED)`; guest-writable `WIRED >= nr_of_tlbs` → divide-by-zero (host SIGFPE). **Fix:** pin `Random` at the top entry like hardware when `WIRED` is out of range. |
| **#191** | MED | `promemul/dec_prom.c`: DEC PROM `read()`/`bootread()` did `malloc(A2)` with a guest length checked only `> 0` → up to 2 GB → `CHECK_ALLOCATION`→`exit()`. **Fix:** cap at 64 MB. |
| **#192** | MED | `promemul/arcbios.c`: ARC PROM `Read`/`Write` `malloc(A2)` unbounded (same class) → `exit()`; and `Write` unconditionally set `V0=0` at the end, clobbering the disk-path `ARCBIOS_EIO` (a failed disk write reported to the guest as success). **Fix:** cap `A2` at 64 MB + graceful `EIO`; move the success store into the STDOUT branch only. |

### Other-arch fidelity (host-crash → guest fault)
| # | Sev | File — fix |
|---|-----|------------|
| **#193** | MED | `cpus/memory_arm.c`: an L2 page-table page outside mapped RAM did a debug `printf` + `exit(1)`. **Fix:** `fs = FAULT_TRANS_P; goto exception_return;` (the file's own translation-fault idiom). |
| **#194** | MED | `cpus/memory_alpha.c`: a failed 3-level page-table walk did `abort(); exit(1);`. **Fix:** `return 0` (no-translation) so the caller faults; keeps the fatal() for debugging. (Reachability low — Alpha MMU is incomplete scaffolding.) |
| **#195** | MED | `cpus/cpu_m88k_instr.c`: signed `div` handled divide-by-zero but not `INT_MIN / -1` → C UB / host SIGFPE. **Fix:** special-case it to the wrapped 2's-complement result `0x80000000`. |
| **#196** | MED | `devices/dev_sgi_gbe.c`: `get_rgb()` `exit(1)` on a guest-controlled unimplemented WID color mode (per-pixel, so also a fatal()-flood risk). **Fix:** render black + `break`. |

### Guest→host DoS (unbounded alloc / counter)
| # | Sev | File — fix |
|---|-----|------------|
| **#197** | MED | `devices/dev_asc.c`: reading an empty FIFO drove `n_bytes_in_fifo` below zero (and writes past full grew it); a later non-DMA selection turned the negative count into a huge `size_t` alloc → `exit()`. **Fix:** guard the read-underflow and write-overflow. |
| **#198** | MED | `devices/dev_ps2_stuff.c`: the DMAC transfer length used the full guest-written QWC register, not its 16-bit field → multi-GB `malloc`. **Fix:** mask `& 0xffff` before `*16`. |
| **#199** | MED | `devices/dev_le.c`: multi-fragment LANCE TX `realloc`-appended without an aggregate cap; a guest rearming a non-ENP descriptor grew host memory without bound. **Fix:** cap the aggregate at 64 KB. |
| **#200** | MED | `devices/dev_pvr.c`: every completed TA command appended 64 bytes and doubled the buffer indefinitely if the guest withheld render/reset. **Fix:** cap queued commands at `VRAM_SIZE/64`. |
| **#201** | MED | `promemul/of.c`: OpenFirmware used guest `nargs` as a signed loop bound (values above `OF_N_MAX_ARGS` only warned, then looped) → ~2^31 iterations / log flood. **Fix:** clamp `nargs` to `OF_N_MAX_ARGS`. |

### Guest→host OOB (memory-safety; Codex HIGH)
| # | Sev | File — fix |
|---|-----|------------|
| **#202** | HIGH | `devices/dev_sii.c`: the SII MMIO window is larger than the `SIIRegs` block that `d->regs` (a `uint16_t*`) points into; `regnr = relative_addr/2` then indexed `d->regs[]` out of range → guest OOB host read (and OOB write in the register switch). **Fix:** reject `relative_addr >= sizeof(d->siiregs)`. |
| **#203** | HIGH | `devices/dev_sgi_mec.c`: the per-fragment "packet too large" `break` stopped only the inner copy; the outer DMA-fragment loop kept writing past `cur_tx_packet[MAX_TX_PACKET_LEN]` → host heap overflow. **Fix:** also break the outer loop when full. |
| **#204** | HIGH | `disk/diskimage.c`: `diskimage_access__cdrom()` accepted a negative `offset` (a guest seeks an opened flat CD/ISO handle to 0xffffffff); `offset/SECTOR*SECTOR` truncates to 0 → `buf_ofs` negative → `cdrom_buf[-1]` OOB stack read. **Fix:** reject `offset < 0`. |
| **#205** | HIGH | `disk/diskimage_scsicmd.c`: MODE SELECT read fixed offsets up to byte 11 after checking only that some DATA OUT occurred; a controller supplying a shorter buffer → heap over-read. **Fix:** require `data_out != NULL && data_out_len >= 12`. |
| **#206** | MED | `disk/diskimage.c`: a legal zero-length access (SCSI WRITE(10) transfer length 0) arrives with `buf==NULL`, which the `buf==NULL` check `exit()`ed before the `len==0` no-op. **Fix:** the `len==0` no-op first. |
| **#207** | HIGH | `devices/dev_px.c`: the PX/PXG `copyspans` re-read `memmove(dma_buf, &sram[sys_addr&0x1ffff], dma_len)` with a guest-forced `dma_len` up to 3080 and offset up to 0x1f800 → ~1 KB read past the 128 KiB `sram[]` into adjacent host heap. **Fix:** clamp the source span to the SRAM size. (Fable-found; the initial 224-byte read is provably in-bounds, left as-is.) |
| **#208** | LOW | `devices/dev_ram.c`: `mmap()` failure was tested `== NULL` but returns `MAP_FAILED`; on failure it skipped the malloc fallback and registered RAM backed by `(void*)-1` (the #175 straggler). **Fix:** test `== MAP_FAILED`. |

**#209 (`cpu_mips_instr.c`, MIPS integer add/sub — audit follow-up):** the MIPS Integer-Overflow *trap* turned out
to be **already correctly implemented** — `add`/`addi`/`sub`/`dadd`/`daddi`/`dsub` raise `EXCEPTION_OV` on overflow
(and OpenBSD boots with it). The audit's UBSan hit was the overflow-*detection* code itself computing `rs+rt` in
signed types (UB on the very overflow it detects); #209 recomputes the sum (and the `sub`/`dsub` negation) in
unsigned at all six sites — bit-identical 2's-complement result, trap behavior unchanged, UBSan signature cleared.
Verified: build 0/0 + OpenBSD 2.2/pmax boots to multiuser.

**Not changed (assessed, intentionally left):** the `dev_px` initial 224-byte SRAM read (line 155) is provably
in-bounds. Codex's remaining items and prior deferrals stay in `OUTSTANDING_BUGS.md`.

**Provenance:** Codex `gpt-5.6-sol`/ultra (holistic, 17 findings) + a 4-reviewer Fable panel (seam /
framebuffer-DMA / storage-net-loaders / SEC-ARC-surface) + this session's per-site source verification and
dual-tree 0/0 build. Corroborated by the audit's ASan cross-check (emulator memory-clean during the #54/#82
fires). **pmax boot regression PASS** (OpenBSD 2.2/pmax to multiuser on the corrected binary; arc boot pending — needs a SEC rebuild).


## Nineteenth round (#210–#223) — MIPS exception fidelity + debuggability + host-halt sweep (Codex 5.6-Sol-Ultra + Fable panel)
A follow-up on the same accuracy/debuggability brief: a fresh Codex `gpt-5.6-sol`/ultra pass + a 2-agent Fable
panel (remaining guest-reachable host-halts; MIPS exception fidelity). **14 corrections (#210–#223)** — mostly
converting a guest-reachable `exit()`/`abort()` on guest-controlled state into a hardware-plausible fault or
graceful return, plus one debuggability hook and one CP0-fingerprint fidelity fix. Applied to both trees (all
tags matched); **build 0/0** (gcc 15.2.1); **OpenBSD 2.2/pmax boots to multiuser** with the MIPS exception-path
changes live.

### MIPS — the audit path (★)
| # | File — change |
|---|---------------|
| **#210** | `cpus/cpu_mips.c`: emit every MIPS exception on the trappable `SUBSYS_EXCEPTION` channel (MIPS was the only major CPU not doing so) with the fault signature fully set. Lets `break exception` stop inside the TLB-miss path that the `-p` PC breakpoint structurally cannot reach — the key hook for tracing a controlled-PC-into-unmapped chain. Cheap when no breakpoint/verbosity is armed. |
| **#211** | `cpus/cpu_mips.c`: an Address Error (AdEL/AdES) or VCE now updates **only BadVAddr**, not Context/EntryHi/XContext — real R3000/R4000 write those only on TLB Mod/Refill/Invalid. Stops the emulator polluting the CP0 fault fingerprint on the misalignment / kernel-touch faults an exploit hits. |
| **#212** | `cpus/cpu_mips_instr.c`: unaligned `LL/LLD` raise AdEL and `SC/SCD` raise AdES (were `exit(1)`), matching silicon and keeping the emulator alive/debuggable on a guest RMW. |
| **#213** | `cpus/cpu_mips_coproc.c`: `mfc0`/`mtc0` to an unimplemented CONFIG select (Config2..7) returns a defined 0 / ignores the write (was `exit(1)`) — any guest can reach it by probing. |
| **#214** | `cpus/cpu_mips_coproc.c`: `mtc0 ENTRYLO1` on an R3000 (reg 3 undefined) warns and ignores instead of `exit(1)`. |

### Other-arch host-crash → guest fault
| # | File — change |
|---|---------------|
| **#215** | `cpus/cpu_alpha_instr_loadstore.c`: the generic load/store path `return`s on a failed `memory_rw()` (the translator already signalled the fault per #194) instead of `exit(1)` (was mislabeled "store failed"). |
| **#216** | `cpus/cpu_ppc_instr.c`: `lwarx`/`stwcx.` to a faulting address let the raised DSI proceed instead of `exit(1)`. |
| **#217** | `cpus/cpu_sh.c`: a guest reserved SuperH instruction takes the illegal-instruction exception (general vector already set above) instead of `exit(1)`. |

### Guest-reachable device / PROM host-halts (the round-18 pattern, more sites)
| # | File — change |
|---|---------------|
| **#218** | `promemul/of.c`: OF `getprop`/`read`/`write` copy to a **guest** buffer pointer via `memory_rw(NO_EXCEPTIONS)`; a bad pointer now stops the copy / returns instead of `exit(1)`. |
| **#219** | `promemul/of.c`: an unknown guest OF service keeps the clean `cpu->running=0` halt but drops the `exit(1)` that defeated the debugger. |
| **#220** | `devices/dev_footbridge.c`: the reset port's col-0 `exit(1)` debug hack removed (`cpu->running=0` already halts); a PCI-config access decoding to bus 255 reads as no-device instead of `exit(1)`. |
| **#221** | `devices/dev_mp.c`: a guest `STARTUPCPU` on an arch without SP-init here starts the CPU anyway (warn) instead of `exit(1)`. |
| **#222** | `devices/dev_kn02ba.c`: a guest MMIO access to an unimplemented DECstation 5000/1xx MER/MSR offset warns and ignores instead of `exit(1)`. |
| **#223** | `devices/dev_8253.c`: five guest-writable i8253-timer paths (DMA-refresh TODO, latch-mode msb/lsb, BCD-mode, unimplemented offset) warn and continue instead of `exit(1)`. |

**Fidelity baseline confirmed (not changed):** GXemul already raises AdEL/AdES (not TLBL) for unaligned *mapped*
targets with correct ExcCode/CE/BadVAddr/EPC/Cause.BD — the general "exception-ordering" caveat is not a gap.
Two document-only items: the R3000 BEV=1 bootstrap-vector base (`0xbfc00200` vs `0xbfc00100`; off the exploit
window — OpenBSD clears BEV early) and `mtc0`-writable `BADVADDR` (Irix compat). The broad tail of remaining
`fatal();exit(1)` in other device handlers (adb, clmpcc, igsfb, lca, m8820x, pcc2, …) is recorded in
`OUTSTANDING_BUGS.md` for a future sweep.

**Provenance:** Codex `gpt-5.6-sol`/ultra + a 2-agent Fable panel (host-halt sweep; MIPS exception fidelity) +
per-site verification. Build **0/0** both trees; all #210–#223 tags matched; **pmax boot regression PASS**.
Both **pmax (R3000) and arc (R4000) boot to multiuser** on the corrected binaries.


## Twentieth round (#224–#226) — MIPS FPU memory-safety (Codex 5.6-Sol-Ultra)
Three **HIGH guest→host memory-safety** bugs on the MIPS FPU path, from the Codex `gpt-5.6-sol`/ultra round-19
pass, per-site verified. Applied to both trees; **build 0/0**; **pmax boots to multiuser**.
- **#224** `cpus/cpu_mips_instr.c` (`ldc1`/`sdc1`): in FR=0, `ft=31` indexed `reg[32]` — one past the 32-entry
  FPR file, into the adjacent `mips_coproc::tlbs` pointer (LDC1 corrupts it → wild pointer; SDC1 discloses it).
  Odd `ft` is architecturally undefined → now raises RI before the OOB access.
- **#225** `cpus/cpu_mips_instr.c` (`ldc1`): the 64-bit load target `fpr` was uninitialized; a **faulting** LDC1
  then copied host-stack garbage into the guest FPR (info leak). Now seeded from the current register so a fault
  leaves the FPR unchanged.
- **#226** `cpus/cpu_mips_coproc.c`: the paired double/long-store **sign-extension** used raw `cp->reg[fd+1]`
  (the write just above already masks `(fd+1)&31`), so `fd=31` sign-extended `reg[32]` — OOB into `tlbs`. Now
  masked at both `FPU_OP` store and `FPU_OP_MOV`.

**Remaining Codex round-19 backlog (22 items) is recorded in `OUTSTANDING_BUGS.md`** for future rounds —
notably the fault-signature fidelity trio (misaligned `JR/JALR` silent round-down → should AdEL; `SWL/SWR`
exception mislabel; `mtc0`-writable `BadVAddr`) and more guest-reachable host-halts (`goto bad`, `malloc(0)`,
PPC/Thumb/m88k slow-path).


## Twenty-first round (#227–#229) — fault-signature fidelity trio (multi-model panel)
The three fault-signature-fidelity items promoted from the Codex round-19 backlog, taken through a **multi-model
advisory panel**: Codex `gpt-5.6-sol`/ultra + agy `Gemini` + Fable (Ollama cloud was unavailable on this host).
**Panel verdict: unanimous FIX-AS-PROPOSED on all three (3-0)**, with the Fable/Codex implementation corrections
baked in. Applied to both trees; **build 0/0**; **pmax + arc boot**. These directly protect the integrity of a
controlled-PC / BADVADDR finding.
- **#227** `cpus/cpu_mips_instr_unaligned.c` (`SWL/SWR` store): the store path pre-reads with `MEM_READ` and then
  *unconditionally* rewrote the fault as `TLBS`; an AdEL (user store to a kernel/misaligned address) or a DBE was
  mislabeled. **Fix:** map only load-side codes to their store counterparts (`TLBL→TLBS`, `AdEL→AdES`), leaving
  the rest (DBE is a shared load/store code; Mod can't arise from a read). Uses the full CP0 accessor (no local
  `reg` alias exists there — Fable correction).
- **#228** `cpus/cpu_mips_instr.c` (6 register-jump handlers): a **misaligned `jr`/`jalr` target** was silently
  rounded down to the IC index instead of raising instruction-fetch AdEL — so a controlled-PC exploit that landed
  an odd target mis-signaled (executed aligned-down rather than faulting). **Fix:** in each of
  `jr`/`jr_ra`/`jr_ra_addiu`/`jr_ra_trace`/`jalr`/`jalr_trace`, after setting `pc` and clearing the delay state,
  `if (pc & 3)` raise AdEL (BadVAddr=EPC=rs, BD=0) and return — *before* the trace hooks; `jr_ra_addiu` counts its
  fused delay-slot addiu first (Codex correction). The panel rejected hoisting into the hotter
  `quick_pc_to_pointers` (~40 already-aligned call sites) and a `return`-hiding macro (foreign pattern).
- **#229** `cpus/cpu_mips_coproc.c` (`mtc0 $8`): `BadVAddr` was guest-**writable** (an old Irix-compat note), so a
  payload could erase the fault address an auditor snapshots. **Fix:** `readonly=1` (ignore guest writes) —
  read-only on R3000/R4000. The panel resolved the prior reviewer disagreement **3-0 to FIX**, and Codex
  empirically confirmed OpenBSD 2.2 pmax/arc only `mfc0`-reads CP0 $8 (no `mtc0 $8` in its kernel source), so no
  regression; the emulator sets BadVAddr directly, not via this write path.

**Provenance:** multi-model advisory panel (Codex `gpt-5.6-sol` + agy Gemini + Fable), each verifying against the
source; unanimous 3-0. Build **0/0** both trees; **pmax + arc boot regression PASS**. The remaining Codex
round-19 backlog (~19 items) stays in `OUTSTANDING_BUGS.md` for #230+.


## Twenty-second round (#230–#233) — MIPS fault-signature fidelity (full 4-model panel)
Four more fault-signature-fidelity items from the Codex round-19 backlog, taken through a **full 4-model advisory
panel**: Codex `gpt-5.6-sol`/ultra + agy `Gemini` + **Ollama** (`gpt-oss:20b`; the `qwen3-coder:480b-cloud` model
returned HTTP 410 Gone) + Fable. Applied to both trees; **build 0/0**; **pmax + arc boot**.
- **#230** `cpus/cpu_mips_instr.c` `X(rfe)`: R3000 RFE must pop the KU/IE stack (`bits[3:0]<-[5:2]`) and leave
  `bits[5:4]` (KUo/IEo) **unchanged**; the old `~0x3f` cleared `[5:4]`, losing the outer privilege/interrupt level
  across nested exceptions. **Fix:** `~0x0f`. (Panel 4-0 CONFIRM.)
- **#231** `cpus/cpu_mips_instr.c` (ERET decode): ERET is MIPS-III+; on an R3000 (EXC3K) it is a reserved encoding
  that must raise RI. **Fix:** decode-gate — `ic->f = (exc_model==EXC3K)? instr(reserved) : instr(eret)` (mirrors
  the WAIT/STANDBY→reserved pattern; `X(reserved)` does the PC-sync). (4-0 FIX; decode-gate 3-1 over a runtime
  guard.) arc (R4000) keeps ERET.
- **#232** `cpus/cpu_mips_instr.c` `X(j)`/`X(jal)`/`X(jal_trace)`: the J/JAL target region used the *branch's*
  page-base region and `~0x03ffffff` (which kept `[27:26]`, double-counting the 28-bit target). MIPS defines the
  region as the **delay-slot PC's** top nibble `(branch+4)[31:28]`. **Fix:** `(page_base + arg[1] - 4)`
  reconstructs branch+4 (`arg[1]=(addr&0xffc)+8`), masked `~0x0fffffff` (correct on 64-bit too). Live for kseg1
  device code (`0xBC…`); the boot escapes it only because kernel text sits at `0x800xxxxx`. (4-0 FIX.)
- **#233** `cpus/cpu_mips_instr.c` `X(mtc0)`/`X(dmtc0)`: the CP0 **write** handlers omitted
  `cop0_availability_check`, so a user-mode `mtc0`/`dmtc0` with Status.CU0 clear silently mutated CP0 state
  instead of raising CpU (a privilege / fault-signature divergence). **Fix:** add the check (writes only). The
  panel **narrowed** this from the broader Codex/Ollama proposal — the mfc0 read fast-paths and the EXC3K
  user-from-PC heuristic are **deferred** (that heuristic is load-bearing; an in-code comment notes forcing KUc
  "crashes Linux").

**Deferred by panel ruling (in `OUTSTANDING_BUGS.md`):** the **privilege-transition fast-map bleed** (Codex #17)
— agy+Fable ruled DEFER (invalidating the fast map on every R3000 RFE/Status-write would hang the boot; the only
correct fix is a structural fast-map privilege-tag refactor the ethos forbids); Codex+Ollama conceded HIGH risk.
Plus the read-side / `$zero`-fold / EXC3K-KUc remainder of #233.

**Provenance:** full 4-model advisory panel (Codex `gpt-5.6-sol` + agy Gemini + Ollama gpt-oss:20b + Fable),
ruling on 3 fixes + 2 fix-or-defer items; Fable and Codex verified against source. Build **0/0** both trees;
**pmax + arc boot regression PASS**.


## Twenty-third round (#234–#244) — guest-reachable host-halt tail → hardware-plausible faults (Fable + agy panel)
The remaining guest-reachable **host-halt** tail from the Codex round-19 backlog (~13 candidates — each a place a
guest can drive GXemul into `exit(1)` / `cpu->running = 0` on guest-controlled state). A **Fable (source-verified)
+ agy** panel triaged them: **10 DO-NOW** — all on the MIPS / pmax(R3000) / arc(R4000) audit path — were converted
to the hardware-plausible fault or graceful error-return; **3 off-path** (PPC/ARM/m88k) were deferred. This makes
the instrument observable exactly where a controlled-PC / bad-descriptor probe used to freeze the rig. Applied to
both trees; **build 0/0**; **pmax + arc boot**.
- **#234** `cpus/cpu_mips_instr.c` `to_be_translated` ifetch: a failed instruction fetch already installs the MIPS
  exception and redirects the PC to the vector (`mips_cpu_exception`→`pc_to_pointers`; also logged by #210), then
  `goto bad` set `cpu->running = 0`. **Fix:** `return` (take the pending exception), matching the faulting-load
  idiom. Trigger: jump to a VA whose ifetch bus/TLB-errors (e.g. a TLB entry mapping to a non-memory paddr).
- **#235** `cpus/cpu_mips_instr.c` `SPECIAL_BREAK`: `break 0x30378` was treated as the GXemul reboot sentinel at
  *any* PC. **Fix:** gate the reboot to the injected reset stub (`(addr & 0x1fffffff)==0x1fc00000`); a guest that
  executes that encoding from ordinary RAM now takes a real **BP** exception, as on hardware.
- **#236** `cpus/cpu_mips_instr.c` reserved COP0 function: an unimplemented `cop0` CO function did `goto bad`
  (halt). **Fix:** `instr(reserved)` → **RI**.
- **#237** `cpus/cpu_mips_instr.c` COP0 `STANDBY`/`SUSPEND`/`HIBERNATE`: HIBERNATE did `goto bad` (halt) and SUSPEND
  did an unconditional reboot at any PC. **Fix:** fold all three onto the STANDBY idiom — idle (`wait`) on R4100,
  **RI** on every other CPU (incl. the R3000/R4000 targets). (Fable folded in the HIBERNATE sibling.)
- **#238** `cpus/memory_mips_v2p.c` (R4000+): a guest entering **supervisor** (KSU=1) or reserved KSU=3 fell through
  to `exit(1)`. **Fix:** supervisor takes Status.SX and joins the normal (kernel-style) TLB walk; reserved KSU does
  a best-effort 32-bit walk — both **fault** instead of halting. Not hit by normal kernel/user boots.
- **#239** `cpus/cpu_mips_coproc.c` (R3000 `tlbw*` under Status.IsC): the architectural TLB entry was already
  written, then `exit(1)` only because the host fast-map add is unsupported. **Fix:** `return` (skip just the
  fast-map add), as the in-code TODO intended.
- **#240** `devices/dev_asc.c` unimplemented SCSI command: set the illegal-command IRQ (`NCRSTAT_INT|NCRINTR_ILL`)
  then `exit(1)`. **Fix:** drop the exit — `dev_asc_tick` delivers the illegal-command interrupt to the guest, as
  on real hardware (distinct from the deferred #185 DATA_OUT).
- **#241** `promemul/dec_prom.c` unsupported DEC-PROM services (2nd `open`, unimplemented jump-table vector, unknown
  `rex()`, unimplemented callback vector): each `cpu->running = 0`. **Fix:** bounded diagnostic + `V0 = -1` +
  return; the intentional halt/reboot services (`rex('h')`/`rex('b')`) are left untouched.
- **#242** `promemul/arcbios.c` unsupported ARC services (non-SGI private call `exit(1)`; the `0x888` "exception,
  no handler" and the unimplemented-vector default `cpu->running = 0`). **Fix:** dump state for debugging, then
  `V0 = ARCBIOS_EINVAL` + return. (Fable flagged the `0x888` sibling; folded in here.)
- **#243** `disk/diskimage_scsicmd.c` `scsi_transfer_allocbuf`: a legal zero-length transfer reached `malloc(0)`,
  which C99 may return NULL → the out-of-memory `exit(1)`. **Fix:** `malloc(want_len ? want_len : 1)`.
- **#244** `cpus/memory_rw.c` (whole class): a failed / `NO_EXCEPTIONS` translation returned `MEMORY_ACCESS_FAILED`
  leaving the caller's read buffer untouched; callers that ignore the return (the DEC-PROM string helpers) consumed
  uninitialised host stack — nondeterminism / unbounded string scans (backlog #22). **Fix:** zero-fill the read
  buffer on failure (same ethos as the failed-device-read zero-fill #95).

**Deferred (off the MIPS audit path; source + 2-model agreement):** #10 PPC/ARM slow-path ifetch `exit` (the data
side is already #216), #11 PPC `MSR.IP` reboot hack, #12 m88k CMMU / `dev_mb89352` fatal errors. Also **not
reachable** on pmax/arc: the SPECIAL3 **RDHWR** selector halt — Fable verified SPECIAL3 is ISA-gated to RI on
R3000/R4000, so the halt only exists on emulated MIPS32r2 (off-path); the RDHWR `HWREna` gate is the same class.
Logged for a future round.

**Provenance:** Fable (source-verified — located every site, confirmed guest-reachability, wrote each minimal fix,
and found the HIBERNATE→#237 and ARCBIOS-`0x888`→#242 siblings) + agy (independent DO-NOW/DEFER triage). Applied to
both trees; **build 0/0**; **pmax + arc boot regression PASS** (pmax R3000 15/15 steps → `uid=0(root)`, OpenBSD 2.2,
clean halt; arc R4000 13/13 → `uid=0(root)`, clean halt).


## Twenty-fourth round (#245–#246) — debuggability logging + FPU denormal fidelity (5-model panel)
The round-23 Part-B suggestions, taken through a **5-model panel** — Codex `gpt-5.6-sol` + Fable + agy `Gemini` +
Ollama (`gpt-oss:120b-cloud`) + **Kimi** (`kimi-k2.5:cloud`). The panel **cleared all four hardware-accuracy
candidates** (C1 R3000 IsC cache, C2 R4000 TLB-Shutdown, C3 FPU denormal-trap, C4 R3000 IE-hazard); on a follow-up
physical-fidelity pass only **C3** survived as genuinely more-faithful, and **C5** (debuggability) was unanimous.
Applied to both trees; **build 0/0**; **pmax + arc boot**.
- **#245 (C5)** `devices/dev_asc.c`, `promemul/dec_prom.c`, `promemul/arcbios.c` — the guest-reachable
  fault-conversion diagnostics from rounds 18–23 (`fatal()` on every guest MMIO / PROM / ARC invocation) now route
  through the verbosity-gated `debugmsg` / `ENOUGH_VERBOSITY` channel at `VERBOSITY_DEBUG` (SUBSYS_DEVICE /
  SUBSYS_PROMEMUL), so a guest or fuzzer hammering an unimplemented ASC command / PROM service can no longer flood
  the host log; full state stays available at `-v` or `break device` / `break promemul`. No new machinery (reuses
  the #210 channel). 8 sites; the 4 PROM/ARC vector sites' unconditional register-dump + a0-string scaffolding is
  folded behind the same gate.
- **#246 (C3)** `cpus/cpu_mips_coproc.c` (FPU denormals → real Unimplemented-Operation trap): the R3010/R4000 FPUs
  do not compute denormalized (IEEE subnormal) values in hardware — they set FCSR cause bit **E** (which, unlike
  V/Z/O/U/I, has **no enable bit** and always traps) and abort so the kernel softfloat completes the op. GXemul
  instead produced **wrong values** (`float_emul.c` always adds the implicit 1-bit, misreading denormal operands,
  and flushes denormal results to ±0 — "FP_SUBNORMAL: TODO"; a denormal divisor even hit the "DIV by zero" fatal).
  Now a denormal S/D operand — or a denormal result with FCSR.FS clear — sets cause E and raises `EXCEPTION_FPE`
  (ExcCode 15) with no result / condition-code written. **Gated to EXC4K+ (R4000/arc)**: MIPS-I (R3000/pmax) has
  no ExcCode 15 (the R3010 signals via the unwired "irq5 fpu" pin), so EXC3K is **bit-identical to before** — pmax
  boot risk **zero by construction**; arc risk negligible (no denormals in the boot path; real R4000 mandates
  kernel softfloat completion if it ever fires). FCSR flag bits + CTC1-cause trapping remain pre-existing TODOs
  (out of scope). Verified: arc boots to multiuser with the trap active and no spurious FP exception.

**Assessed, intentionally left (panel ruling; #247 unconsumed):**
- **C1 (R3000 IsC cache isolation) — already correct:** GXemul allocates real per-cache buffers
  (`cpu_mips.c`: `cpu->cd.mips.cache[i] = malloc(...)`) and `memory_cache_R3000()` routes isolated-cache data
  accesses to them — the "invisible cache stash" is already faithfully modeled. Not inaccurate.
- **C2 (R4000 TLB-Shutdown on overlapping entries) — DO-NOT:** no machine-check delivery exists
  (`EXCEPTION_MCHECK` is never raised; no `STATUS_TS`/DS state is modeled), R4000-true multiple-match is
  architecturally **undefined** (a reset-latched wedge, not an exception), and a MIPS32-style ExcCode 24 would be
  anachronistic + panic-prone on OpenBSD 2.2. Upstream's own duplicate detector is `#if 0`'d as unreliable.
  First-match is a legitimate concretization of UNDEFINED that no correct guest can distinguish from silicon.
- **C4 (R3000 delayed-IE / interrupt-in-delay-slot) — already correct where it matters:** the delay-slot
  `Cause.BD` + `EPC=branch` fault signature is textbook (`cpu_mips.c`); only the 1–2-instruction IE cycle-timing
  hazard is unmodeled, which no OpenBSD path depends on (a functional emulator has no cycle timing). Left.

**Provenance:** 5-model panel (Codex + Fable + agy + Ollama gpt-oss:120b + Kimi-k2.5) on 5 candidates; Fable
source-verified C1/C4 already-correct and designed the #246 patch + the C2 DO-NOT rationale. Build **0/0** both
trees; **pmax + arc boot regression PASS** (pmax R3000 15/15 → `uid=0(root)`, OpenBSD 2.2, clean halt; arc R4000
13/13 → `uid=0(root)`, clean halt, FPU trap active + no misfire).


## Twenty-fifth round (#248, #250) — debugger QoL for the audit: breakpoint hit-counts + data write-watchpoints (4-model panel)
A scoping pass over the author's own `doc/TODO.html`, filtered to items that improve **debuggability** for the
OpenBSD 2.2 pmax/arc exploitation audit. Recon found the fork already implements most of the TODO debugger wishlist
(`find`, `put s/z`, `step call`, `verbosity`, subsystem/`debugmsg` breakpoints, prefix-abbrev subcmds — the
#120–#128 round) **and** the `-f` fsync option (so the panel's "C3 fsync CLI toggle" candidate, tentatively
**#249**, was **already done — #249 is VOID / unconsumed**). A **4-model panel** (Codex `gpt-5.6-sol` + agy `Gemini`
+ Ollama `gpt-oss:120b-cloud` + Kimi `kimi-k2.5:cloud`; the Fable seat was down on credits) ranked the two
remaining verified-undone items DO-NOW. Both are **opt-in and guest-invisible** — with none set, each is a single
`n != 0` early-out, so a run without them is behaviourally identical (both boot regressions confirm this). Applied
to both trees; **build 0/0**; **pmax + arc boot regression PASS**.
- **#248** `include/machine.h`, `machines/machine.c`, `debugger/debugger_cmds.c`, `debugger/debugger.c`,
  `cpus/cpu_dyntrans.c` (**breakpoint hit-counts + "run N then break"**): `struct breakpoints` gains parallel
  `hitcount` / `ignore_left` arrays. The dyntrans breakpoint check (`TO_BE_TRANSLATED_HEAD`) counts every hit, and
  while `ignore_left > 0` it decrements and **keeps running** instead of stopping — reusing the existing
  `single_step_breakpoint` re-translation path so the check re-fires on the next hit (the instruction-combination
  gate also now excludes `single_step_breakpoint`, so a merged predecessor can't bypass counting). Syntax:
  `breakpoint add addr[, N]` = skip the first N hits; `breakpoint show` and CTRL-T display live hit counts. Verified:
  ignore-5 on a 64-iteration TLB-init loop first stops at `hits=6`, next continue `hits=7`.
- **#250** `include/machine.h`, `machines/machine.c`, `debugger/debugger_cmds.c`, `cpus/cpu_dyntrans.c`,
  `cpus/memory_rw.c` (**data write-watchpoints**): `watchpoint add addr[, len]` breaks into the debugger on a guest
  **store** into the range, reporting writer PC, width, value, and both vaddr/paddr. (a) `update_translation_table()`
  keeps a watched page **out of the fast store table** (`host_store = NULL`) so its writes trap to `memory_rw`;
  add/delete calls `invalidate_translation_caches(…, INVALIDATE_ALL)` (not `cpu_create_or_reset_tc`, which only
  clears *code* translations) so the data fast-map is rebuilt. (b) The check sits **early in `memory_rw`, before the
  device/cache/RAM dispatch** — before the R3000 `memory_cache_R3000()` early-return that would otherwise hide every
  cached kseg0 store. Matching is on the **physical** address (typed vaddr → paddr via `translate_v2p` at add-time):
  defeats 32-bit vaddr sign-extension and kseg0/kseg1 aliasing. Verified on pmax: `watchpoint add 0x80000000`
  (→ paddr 0x0) caught the kernel installing exception vectors via `_bcopy`, reporting `pc=0x…80122c00` + the bytes.

**Not consumed:** **#249 is VOID** (its candidate — a disk fsync-on-write CLI toggle — is already the shipped `-f`
option). Panel DEFER/DO-NOT (documented in `OUTSTANDING_BUGS.md`): CTRL-T in the main run loop; PC/execution
statistics.

**Provenance:** 4-model panel (Codex + agy + Ollama gpt-oss:120b + Kimi-k2.5; Fable seat down on credits). Build
**0/0** both trees; **pmax + arc boot regression PASS** (pmax R3000 → `uid=0(root)`, OpenBSD 2.2; arc R4000 →
`uid=0(root)`, clean halt) — both with nothing set, confirming zero behavioural change; features then functionally
verified live (C1 ignore-count, C6 watchpoint fire).


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
