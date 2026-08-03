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


## Twenty-sixth round (#251, #252) — console host-glue fidelity: output flush + input-EOF freeze (3-view panel)
An OpenBSD 2.2 pmax/arc audit reported three "emulation-layer" defects: (L12) the serial console **drops**
long/rapid multi-line output, (L5) any path behind a `forkpty()`/pty **hangs**, and (L13) an `inetd`-spawned
UDP `dgram/wait` service never receives its datagram. A 3-view source-verified panel (Codex `gpt-5.6-sol`/high +
Fable + this reviewer's holistic pass) traced each to root and **converged**: the audit mis-attributed the
subsystem in every case. The two real, fixable emulator defects live in the shared **host-console glue**
(`console/console.c`, byte-identical to pristine 0.7.0 — these are upstream-latent, not est/SEC regressions),
*not* in the DZ/ns16550 UART, the NIC, or any "syscall timing". Both fixes are guest-invisible and change only
host-side I/O behaviour; **build 0/0 both trees; pmax 15/15 + arc 13/13 boot regression PASS**.
- **#251** `console/console.c` `console_putchar()` (**serial output loss — L12**): the newline branch cleared
  `console_stdout_pending` on `'\n'` assuming libc line-flushes. That holds only for a **tty**; when GXemul's
  stdout is a pipe/file (any scripted/headless capture) stdio is **fully buffered**, so `'\n'` does *not* flush
  *and* the cleared flag makes the periodic `console_flush()` a no-op — a newline-terminated burst then sits in
  the host stdio buffer and is lost outright if the process is killed or wedges before the next flush. Fix: drop
  the newline special-case and **always** mark output pending (3 lines → 1). On a tty nothing changes; on a pipe
  every burst now drains within the existing ≤2¹⁹-instruction `console_flush()` cadence. Not the UART — the DZ
  (`dev_dc7085`) and ns16550 TX paths are lossless by construction (every byte reaches `console_putchar`).
- **#252** `console/console.c` `console_charavail()` (**pty/console "hang" — L5**): the input-drain loop is
  `while (console_stdin_avail(handle)) { … read() … }`. On stdin **EOF** (harness closes GXemul's stdin, or
  stdin is `/dev/null`) `select()` reports the descriptor readable forever while `read()` returns 0, nothing
  enters the FIFO, and the `while` never exits — an **infinite spin inside a device tick**, so `machine_run()`
  never returns and the *entire emulator* freezes (no instructions, no IRQs, no flush; even CTRL-C is dead). A
  real serial line has no EOF. Fix: `if (len < 1) break;` after the `read()` (one line). *Not* clearing
  `in_use_for_input` — `console_putchar()` re-arms it on the next output char, silently undoing that variant.
- **Reproduced + verified on the pmax rig (before → after):** `gxemul -e 3max -d 1:disk bsd.pmax < /dev/null`
  (stdin at EOF) froze at **0 bytes** (killed at timeout); the *only* changed variable, an open stdin, booted
  normally to `root device?`. After #251/#252 the same `< /dev/null` invocation boots to `root device?`
  (979 bytes) identically to the open-stdin control — the freeze is gone and the output flushes.

**Triaged but NOT changed (this round):**
- **L13 inetd UDP `dgram/wait` — not an emulator/device bug.** GXemul's userspace NAT (`net/net_ip.c`
  `net_ip_udp` / `net_udp_rx_avail`) creates mappings **only** from guest-*outbound* datagrams and has no
  unsolicited-inbound path at all; an `inetd dgram wait` service waits on purely unsolicited inbound, so the
  datagram never enters the guest (nothing is "lost during fork+exec" — once `inetd`'s `select()` is readable the
  datagram is already in the guest socket buffer, past the NIC). The real axis is *solicited vs unsolicited*, not
  inetd-vs-standalone. Resolutions are configuration (tap networking, `net/net_tap.c`, already implemented) or a
  one-datagram outbound "hole-punch" in the test — **not** a `dev_le`/`dev_sn`/`net.c` change. True inbound
  port-forwarding would be a new feature with new state/options, outside the minimal-surgical ethos.
- **L12 UART model — not a bug** (lossless; see #251). The permanently-ready TX status is a fidelity
  simplification, not a data-loss source; adding baud-rate timing is unwarranted.
- **`dev_jazz.c` R4030 `EXT_IMASK` IP3/4/6 namespace gating** — the est/ copy ANDs CPU-IP funnel enables directly
  against Jazz device-line bits (arc-only; suppresses com0/timer/ISA IRQs). Real, but **SEC's `dev_jazz.c`
  already carries the corrected split** (this is the SEC-only jazz boot-enablement layer the arc rig runs), and
  pmax uses no jazzio — so it affects neither rig and is not the L5 hang. Companion OB-22 (`dev_jazz.c` vector-read
  blanket deassert) remains deferred (self-healing; touches the verified arc boot).

**Provenance:** 3-view source-verified panel (Codex `gpt-5.6-sol` high-reasoning + Fable, each cross-checked
against pristine `src/` by `diff`; + reviewer holistic pass). Build **0/0** both trees; **pmax + arc boot
regression PASS** (pmax R3000 15/15 → `uid=0(root)`, OpenBSD 2.2; arc R4000 13/13 → `uid=0(root)`, clean halt).


## Twenty-seventh round (#253) — Linux tun/tap enablement (net_tap.c) + inbound-delivery recipe (Codex + Fable)
Follow-up to round 26's L13 disposition (the userspace NAT has no unsolicited-inbound path, so an `inetd` UDP
`dgram/wait` service cannot receive its datagram). GXemul already ships a complete Ethernet **tap** backend
(`net/net_tap.c`, wired in `net/net.c`, selected by a `net( tapdev(...) )` config block or the `-L` CLI option),
but `net_tap_init()` opened the device BSD-style (`open(tapdev)`, a `/dev/tapN` node) — which does not work on
Linux. A Codex `gpt-5.6-sol` + Fable panel designed the minimal Linux path; applied:
- **#253** `net/net_tap.c` `net_tap_init()`: on `#if defined(__linux__)`, open the clone device `/dev/net/tun`
  and `ioctl(TUNSETIFF, { IFF_TAP | IFF_NO_PI, ifr_name = tapdev })` — so on Linux `tapdev` is the tap **interface
  name** (`tap0`), which the user pre-creates (`ip tuntap add dev tap0 mode tap user $USER`); the BSD device-path
  `open()` is preserved verbatim in the `#else`. `IFF_NO_PI` because the switch code (`net_tap_rx_avail`/`_tx`)
  expects bare Ethernet frames with no 4-byte packet-info header. The shared `FIONBIO` + `strdup`/`tap_fd` tail is
  untouched, so **non-Linux hosts compile byte-identical** and the NAT path (only reached when `tapdev == NULL`) is
  entirely unaffected. Gated includes `#if defined(__linux__)`: `<net/if.h>` (glibc `struct ifreq`) +
  `<linux/if_tun.h>` — **not** `<linux/if.h>`, which redefines `struct ifreq`/`IFF_*` against `<net/if.h>` on older
  glibc; the two seats split on the header and it was resolved by test-compiling all three variants under the build's
  `-Wall -Wextra -Wshadow`.

**Verification.** Build **0/0** both trees; both NAT boot regressions still pass (pmax 15/15 + arc 13/13 →
`uid=0(root)`), confirming zero NAT-path impact. **Live tap test (pmax rig, R3000):** `gxemul -e 3max -L tap0 -d
1:/tmp/rig.img /tmp/bsd.pmax` attaches (host `tap0` → `UP,LOWER_UP`, 0 errors; guest `le0` on the tap). With the
guest `ifconfig le0 inet 10.0.0.10 netmask 255.0.0.0 up`, an **unsolicited inbound** `ping` from the WSL host got
**4/4 replies** (guest ttl=255) and a host UDP datagram to a closed guest port drew an **ICMP port-unreachable** —
i.e. the datagram reached the guest kernel with no prior NAT mapping, the delivery the userspace NAT structurally
cannot do (closes the L13 class). The guest also learned the host MAC (`arp: (10.0.0.1) at …`), confirming
bidirectional L2. **Use the pmax rig for tap:** the arc/pica SONIC (`dev_sn.c`) is a register stub (no RX/TX),
whereas 3max LANCE (`dev_le.c`) is complete. Invocation: `-e 3max -L tap0` (the `-L` flag feeds `tapdev` via
`emul_simple_init`→`net_init`), or a `@config` with `net( tapdev("tap0") )` **before** `machine(...)` (a NIC joins
`emul->net` at machine-setup time, so net-first ordering is required). Under WSL2 the tap is host↔guest only (the VM's
NAT network isn't bridged to the LAN) — sufficient for the unsolicited-inbound proof.


## Twenty-eighth round (#254, #255) — MIPS FPU result-correctness (4-model panel)
Item #1 of an 8-item TODO-triage batch. `fpu_op()` (`cpus/cpu_mips_coproc.c`) had three verified IEEE-754 result
bugs on the pmax (R3010) / arc (R4010) FP path. A full 4-model panel (Codex `gpt-5.6-sol`/xhigh + agy Gemini Pro +
Fable + Ollama `gpt-oss:120b-cloud`) designed and reviewed the fix; scope kept to result-correctness (FCSR
flag/trap machinery deferred — see `OUTSTANDING_BUGS.md`).
- **#254** `cpus/cpu_mips_coproc.c` `fpu_op()`: (a) **DIV** — replace the `fabs(divisor) > 1e-11` hack (which sent
  valid small divisors like 1e-12, and every NaN divisor, into a `fatal("DIV by zero")` branch that returned
  WITHOUT writing fd → stale guest register) with unconditional host IEEE division (x/0→±Inf, 0/0→NaN; GXemul never
  unmasks host FP exceptions). (b) **SQRT** — `sqrt(neg)` is a quiet NaN, not `fatal()`+0.0. (c) **COMPARE** —
  replace the whole `switch(cond)` (which made c.olt/c.ole true for ANY ordered pair via `|| !unordered`, and
  `fatal()`'d on nine `#if 0`'d conditions) with the unified truth-table formula
  `((cond&4)&&less)||((cond&2)&&equal)||((cond&1)&&unordered)` — correct for all 16 c.cond.fmt predicates. Dropped
  the now-dead `nan` local.
- **#255** `cpus/cpu_mips_coproc.c` `fpu_store_float_value()`: canonicalize a NaN arithmetic result to the
  legacy-MIPS **quiet** NaN (S `0x7fbfffff`, D `0x7ff7ffffffffffff`; fraction MSB clear) — `ieee_store_float_value`
  emits all-ones, a *signaling* pattern. MOV copies raw bits and is unaffected; W/L integer formats untouched.

Build **0/0** both trees (Fable compiled the TU clean under the exact flags); **pmax 15/15 + arc 13/13 boot →
`uid=0(root)`**; the boot logs show **0 hits** of the removed `fatal()` strings (those paths were never exercised).
FP microtest: the OpenBSD 2.2 rig image has no in-guest C compiler (broken dynamic linker), so the panel's
16-condition / div / sqrt vectors were validated host-side against the exact new algorithm — **11/11 PASS** (incl.
compare mask (2.0,1.0)=0x0000 vs the old 0x0050, 0/0→qNaN `0x7ff7…`, `sqrt(2.0)`=`0x3ff6a09e667f3bcd`). Diff
4-seat-reviewed faithful + safe.


## Twenty-ninth round (#256) — interactive debugger MIPS breakpoint sign-extension (Codex + Fable + Ollama)
Item #2 of the 8-item TODO-triage batch. `breakpoint add <kseg0 addr>` typed interactively never fired on the **arc rig (R4000)**: the add path (`debugger/debugger_cmds.c`) parses the address with `writeflag=0`, so `debugger_parse_name()` skips the MIPS 32→64-bit sign-extension, and the stored `0x0000000080…` never equals the sign-extended pc `0xffffffff80…` in the 64-bit dyntrans compare. R3000/pmax was unaffected — its `mips32` compare truncates both sides. Config-file breakpoints already applied the fixup (`core/emul.c add_breakpoints` ~170-173); symbol-derived addresses were already sign-extended at load (`symbol.c`). A 3-seat panel (Codex `gpt-5.6-sol`/xhigh + Fable + Ollama `gpt-oss:120b-cloud`; agy dropped on a headless file-read limit) gave the identical minimal fix.
- **#256** `debugger/debugger_cmds.c` (`breakpoint add`): after the parse, mirror `emul.c`'s normalization verbatim — `if (arch==ARCH_MIPS && (tmp>>32)==0 && ((tmp>>31)&1)) tmp |= 0xffffffff00000000`. Guard is **ARCH_MIPS only** (an `is_32bit` guard would no-op it on R4000, the exact machine that needs it). Numeric input only; symbol breakpoints already worked.
Build **0/0** both trees; verified on the arc rig — `breakpoint add 0x80100000` now shows `0xffffffff80100000` (was `0x0000000080100000`); pmax + arc boot regressions unaffected (15/15 + 13/13 → `uid=0(root)`).


## Thirtieth round (#257) — R4030 interval timer honors the guest-programmed rate (dev_jazz.c, both trees)
Item #5 of the 8-item TODO-triage batch. The arc (Acer PICA/Jazz, R4000) R4030 interval timer was created at a hardcoded 100 Hz (`dev_jazz.c timer_add(100.0, …)`, with the author's own "TODO: Don't hardcode!"); guest writes to `R4030_SYS_IT_VALUE` (the arc OS clock rate) were stored but never propagated, so any non-100 rate was silently ignored. A 3-model panel (Codex `gpt-5.6-sol`/xhigh + Fable + Ollama; agy dropped on a headless file-read limit) split on the R4030 base clock (1 kHz vs 1 MHz); resolved **empirically** by instrumenting the IT_VALUE write and booting arc — OpenBSD 2.2 writes exactly **9** at clock init, which is 100 Hz only under a **1 kHz** base (`1000/(9+1)`), not 1 MHz.
- **#257** `devices/dev_jazz.c` (both trees, hand-applied — the file diverges between est/ and SEC): on a guest write to `R4030_SYS_IT_VALUE`, `timer_update_frequency(d->timer, 1000.0/((double)idata + 1.0))` — the R4030 counts down at 1 kHz and reloads N, interrupting every (N+1) ms. Computed from the **unsigned** `idata` (the `int interval_start` would give −1 on 0xffffffff → −1+1 div-by-zero); N ≥ 0 bounds the rate to (0, 1000] Hz. The 100 Hz `timer_add` stays the power-on default. Precedent: `dev_8253`/`dev_mc146818`/`dev_vr41xx` all retune via `timer_update_frequency` from their write handlers.
OpenBSD 2.2/arc writes 9 → exactly 100.0 Hz → `timer_update_frequency` early-returns, so the fix is a **no-op on the verified boot**. Build **0/0** both trees; **arc 13/13 + pmax 15/15 boot → `uid=0(root)`**.


## Thirty-first round (#258) — decoded STATUS/CAUSE/FCSR in the MIPS register dump (Codex + Fable + Ollama)
Item #6 of the 8-item TODO-triage batch — a display-only debuggability aid for the fault-signature workflow. `mips_cpu_register_dump()` (`cpus/cpu_mips.c`) printed COP0 STATUS/CAUSE and the FPU FCSR as raw hex only.
- **#258** `cpus/cpu_mips.c` (both trees): two static helpers decode, under the existing raw-hex rows, STATUS (R2000/R3000 EXC3K keeps the 3-deep KU/IE stack + cache-diag bits; R4000+ EXC4K has KSU/ERL/EXL/KX/SX/UX), CAUSE (`exception_names[]` mnemonic + exccode/BD/CE/IV/IP; 4-bit exccode on EXC3K vs 5-bit on EXC4K), and FCSR (FCC byte, FS, cause/enables/flags E-V-Z-O-U-I groups, rounding mode). Reuses existing bit `#define`s; the R5900's nonstandard FCSR layout is skipped. **Display-only — reads `reg[]`/`fcr[]` and calls `debug()`, no state change.**
Build **0/0** both trees; **pmax 15/15 + arc 13/13 boot → `uid=0(root)`** (output byte-identical outside the debugger dump).


---
## Thirty-second round (#259, #260, #261) — debugger/net QoL (Codex + Fable + Ollama)
Items #8a, #8b, #7 of the 8-item TODO-triage batch — three small, low-risk debuggability/housekeeping wins.
- **#259** `core/emul.c` + `debugger/debugger_cmds.c`: make `-K` (drop into the debugger at machine halt) implicit and **sticky** when any breakpoint is configured — set `debugger_enter_at_end_of_run` at the config/`-p`, interactive `breakpoint add`, and `breakpoint subsystem` sites. (Breakpoints already *fire* without `-K`; this only affects end-of-run.)
- **#260** `net/net.c`: route the four remaining `net_init()` diagnostics (bad IPv4 address / prefix length / unresolved remote / malformed `host:port`) through `debugmsg(SUBSYS_NET, …, VERBOSITY_ERROR)`, matching the existing net conversions; the `net_add_nic()` NULL programmer-error `exit(1)` is left as-is.
- **#261** `core/debugmsg.c` + `include/misc.h`: an **opt-in, default-OFF** global "break on any ERROR-level debugmsg" — a `debugmsg_break_on_error` flag checked in `debugmsg_va()` alongside the per-subsystem levels, toggled by `breakpoint subsystem all error` / `… all off`. (The panel rejected the TODO's literal "always break" as boot-fragile; the existing `all error` already covers registered subsystems, so this is a small robustness upgrade.) Default OFF = single false test = no-op.
Build **0/0** both trees; **pmax 15/15 + arc 13/13 boot → `uid=0(root)`** (all three inert on a normal boot).
---
## Thirty-third round (#262) — LANCE RX-ring exhaustion (CSR0.MISS) (Codex + agy + Fable + Ollama)
Item #4 of the 8-item TODO-triage batch — a fidelity correction to the emulated Am7990 (LANCE) receive path; the design was 4-model-panel-locked (a DESIGN review + a DIFF review of Codex's patch).
- **#262** `devices/dev_le.c` (both trees): `le_rx()` previously **held an incoming frame in `d->rx_packet` indefinitely** when the chip reached a receive descriptor it did not own (ring full), so the guest never observed the loss. Real Am7990 hardware drops it: **first-buffer** exhaustion now sets **`CSR0.MISS`**; **mid-frame** (chained-buffer) exhaustion is detected by **looking ahead while the current descriptor is still chip-owned** and terminates that descriptor with **`ERR`+`BUFF`** error bits plus **`RINT`** (no ENP) — the correct ownership transition (writing the *previous*, already-released descriptor was rejected as a DMA-contract violation). `le_register_fix()` now **drains only the already-resident receive queue** on exhaustion instead of re-polling `net_ethernet_rx_avail()` (which imports TAP/UDP/TCP traffic and could livelock a tick under a flood). `le_rx()` becomes `int` (its only caller is `le_register_fix`; no prototype). The stale "not emulated yet" TODO is updated.
Build **0/0** both trees; **pmax 15/15 + arc 13/13 boot → `uid=0(root)`**; instrumented boot shows **0** exhaustion hits (branches inert on a normal console-login boot).
---
## Thirty-fourth round (#263) — ASC/R4030 DMA accounting (host-heap disclosure + count over-transfer) (Codex + agy + Fable + Ollama)
Item #3 of the 8-item TODO-triage batch — a deep ASC (NCR 53C94) + R4030 DMA-seam audit; the design was 4-model-panel-locked at **scope (a)** (safety guards only), unanimous, with the residual/TC-suppression fidelity (**A4**) deferred to **#264**. Both bugs were found by the Codex xhigh audit (Fable's parallel audit missed them), adjudicated real against source, and tempered from Codex's CRITICAL to **HIGH** (guest-memory / host→guest-disk, not a host overrun).
- **#263 A2** `devices/dev_jazz.c` (both trees): `dev_jazz_dma_controller()` bounded its 1/15/255-byte copy quantum only by the ASC-requested `len`, never by the R4030 programmed byte count (`dma0_count`) — a short R4030 count against a larger ASC length could **over-read/over-write up to 254 bytes of guest memory**. The quantum is now **clamped to the remaining R4030 count**, and the callback **returns the actual bytes moved** (`return (size_t) i`) rather than the requested `len`. `dma0_count = 0` is left unchanged (panel-unanimous; the residual is A4/#264).
- **#263 A1** `devices/dev_asc.c` (both trees): the DATA_OUT first-transfer path allocated its transfer buffer **without zeroing** (`scsi_transfer_allocbuf(..., clearflag=0)`) and could advance the offset / set Terminal Count even when the DMA callback moved nothing (wrong-direction), so **uninitialized host heap could be written into the guest disk image**. The buffer is now **zero-filled** (`clearflag=1`), neutralizing the disclosure regardless of the residual A4 offset/TC fidelity.
On matched ASC/R4030 counts and correct direction (the arc/pmax SCSI-root boot path) the clamp never fires and the zero-fill is overwritten by real data → behavior byte-for-byte unchanged.
Build **0/0** both trees; **pmax 15/15 + arc 13/13 boot → `uid=0(root)`**; instrumented boot shows **0** clamp/short-DMA hits (guards inert on a normal SCSI-root boot).
---
## Thirty-fifth round (#264) — ASC zero-length DATA_OUT host-abort → guest disconnect (Codex + agy + Fable + Ollama)
Item #3 follow-up — the residual ASC (NCR 53C94) host-abort from the #263 ASC + R4030 DMA-seam audit. `dev_asc_transfer()` called `exit(1)` when a DATA_OUT transfer had a zero-length `data_out` buffer — a host abort reachable from guest register programming: the Transfer-Pad command (`NCRCMD_TRPAD`) allocates a fresh empty transfer via `dev_asc_newxfer()`, then runs a DATA_OUT transfer straight into the `exit`. The design was 4-model-panel-locked at **scope (a)**, unanimous.
- **#264** `devices/dev_asc.c` (both trees): the zero-length DATA_OUT branch now logs a `fatal()` and **returns 0** instead of `exit(1)`, so the existing `NCRCMD_TRANS`/`NCRCMD_TRPAD` handler converts it into a guest-visible **disconnect** (`NCRINTR_DIS|NCRSTAT_INT`) — the same soft-fault used for absent-target selection and the #167 no-SELECT guard, and the established host-abort→guest-fault pattern (#167/#197/#240). **DISCONNECT** is the correct fault: a legal Transfer-Pad opcode in a legal DATA_OUT phase is not an illegal command (`NCRINTR_ILL` would misclassify it, and the gross-error path has no cleanup plumbing). The `return 0` leaks nothing (`data_out` is allocated later, still NULL here) and does not free locally (the caller frees `xferp`). A faithful Transfer-Pad (pad/discard against the current nexus, scope (b)) is deferred as riskier.
Build **0/0** both trees; **pmax 15/15 + arc 13/13 boot → `uid=0(root)`**; the new `fatal()` never fires on a healthy boot (0 hits in both pty logs).
---
## Thirty-sixth round (#265, #266) — ASC FIFO occupancy + reset IRQ hygiene (Codex + agy + Fable + Ollama)
The ASC (NCR 53C94) FIFO/reset register-hygiene round from the same TODO-triage sweep; the design was 4-model-panel-locked. Fable caught the **fourth** occupancy site (the message-out drain) the other three seats undercounted, plus the read-side atomicity hazard (fixing a drain loop without the `dev_asc_fifo_read` guard would let a full FIFO infinite-loop the host, so all three read-side sites are changed in one commit).
- **#265** `devices/dev_asc.c` (both trees): the 16-byte FIFO tested occupancy with the pointer equality `fifo_in == fifo_out` at **four** sites — but that is **also true when the FIFO is exactly full (16 bytes)**, so a full FIFO was read as *empty*. `dev_asc_fifo_read` stuck returning the same byte (never decrementing); the CDB and message-out non-DMA drain loops copied **zero** of the bytes they had just allocated (`clearflag=0`), handing an uninitialized buffer tail to the SCSI command layer; and the write post-check false-warned on the legal 16th byte. All four sites now use the cached `n_bytes_in_fifo` count, and the overflow warning moves to the real drop site. Reachable by any guest that writes `NCR_FIFO` 16×; the arc/pmax boots top out at 15 bytes, so for n<16 the tests are equivalent → happy path unchanged.
- **#266** `devices/dev_asc.c` (both trees): a chip reset (`RSTCHIP`, the sole caller of `dev_asc_reset`) cleared `NCRSTAT_INT` but never released the physical interrupt line — `DEVICE_TICK(asc)` only asserts on a rising edge and the only deassert was the `NCR_INTR` read — so a reset taken with a pending interrupt left the IRQ **latched high with a zeroed status**. `dev_asc_reset` now deasserts the line (it runs only at RSTCHIP, after `INTERRUPT_CONNECT`).
FIFO Gross-Error status, `cur_phase` reset, and TC-preservation on the INTR read are deferred (boot-interaction risk, no demonstrated victim).
Build **0/0** both trees; **pmax 15/15 + arc 13/13 boot → `uid=0(root)`**; instrumented boot shows **0** full-FIFO reads/drains, **0** write-drops, and **0** pending-IRQ resets (all four changed branches dead on the SCSI-root boot path).
---
## Thirty-seventh round (#267) — R4030 DMA translation-table limit (Codex + agy + Fable + Ollama)
The last untreated R4030 DMA-engine gap from the #263 ASC + R4030 DMA-seam audit; the design was 4-model-panel-locked at **scope (a)** (bound-and-stop), unanimous, with the byte-size limit semantic pinned to the NetBSD/arc and Linux jazzdma drivers and confirmed by an instrumented arc boot.
- **#267** `devices/dev_jazz.c` (both trees): `dev_jazz_dma_controller()` translated a DMA address to physical by reading the PTE at `dma_translation_table_base + (dma_addr>>12)*8` but never bounded that index against the programmed **TL_LIMIT**, so a DMA address past the end of the table read an **arbitrary guest word as a PTE** and moved data to/from whatever physical page that word encoded — guest-memory corruption on a misprogrammed or hostile transfer (it stays within guest RAM, so not a host overrun). The walk is now bounded: when the table byte-offset reaches a **non-zero** `TL_LIMIT` the transfer stops and reports the bytes completed so far. The real R4030 raises a translation-limit fault (`DMA_ENAB_TL_IE` / `DMA_INT_SRC`); that error/interrupt path is not modeled and is a documented gap, as is DMA0 count-register masking (`R4030_DMA_COUNT_MASK`, a separate future #268). The limit is a table **byte-size** (NetBSD/arc `JAZZ_DMATLB_SIZE`, Linux jazzdma `VDMA_PGTBL_SIZE`); a limit of **0** (never programmed) is fail-open, so it cannot regress a guest that does not use the table.
Verified **empirically**: a non-enforcing probe observed OpenBSD 2.2/arc program **TL_LIMIT=0x8000** (4096 × 8) once at boot, the SCSI-root boot's **max table offset was 0x458** (~28 KB below the limit), and across **2602 DMA transfers 0** would exceed it — the bound never fires on the verified boot. Build **0/0** both trees; **arc 13/13 + pmax 15/15 boot → `uid=0(root)`**.
---
## Thirty-eighth round (#268) — R4030 DMA count-register width (Codex + agy + Fable + Ollama)
The follow-up flagged in #267 and the final item from the #263 ASC + R4030 DMA-seam audit; the design was 4-model-panel-locked, unanimous, with the empirical over-mask probe folded into the same round.
- **#268** `devices/dev_jazz.c` (both trees): the R4030 DMA channel-0 byte-count register is **20 bits wide** (`R4030_DMA_COUNT_MASK = 0x000fffff`, previously defined but unused), but the register write stored the **raw 32-bit value**, so a guest could express a DMA transfer **longer than any real R4030** — the upper bits are physically absent on the chip. The channel-0 count write is now masked to 20 bits; the read-back returns the masked value, and the copy-loop count/clamp (**#263**) and the translation-table bound (**#267**) now see a count that cannot exceed the hardware width. **Channel-0 only** (`dma1` stores only its mode register; `dma2`/`dma3` are unmodeled); the mask also clears bits 32–63 before the assign to the `uint32_t` field, slightly hardening the `dma_addr + dma0_count` sum in the copy-loop guard.
Verified **empirically**: an instrumented arc boot recorded **0** count writes with bits above the mask (guest SCSI transfers are bounded by **MAXPHYS**, far below 1 MB), so the mask is a **no-op on the verified boot**. Build **0/0** both trees; **arc 13/13 + pmax 15/15 boot → `uid=0(root)`**.
---
## ASC / R4030 audit closed — known gaps documented
Documentation only (round 39; no correction number). This closes the full NCR 53C94 "ASC" SCSI + Jazz R4030 DMA deep audit (a two-model deep audit — Codex 5.6-sol xhigh and Fable, cross-referenced and adjudicated against the source). Rounds 34–38 (#263–#268) fixed every reachable correctness/safety finding; the remaining items are recorded in **`REVIEW_FINDINGS.md`** under "ASC / R4030 DMA audit — known gaps & deferred items" as **unreachable / deferred / do-not-fix**: cosmetic PMAZ address-register fidelity (left as-is — every use masks the value to the 128 KB SRAM buffer, so fixing it would only risk the boot-critical SCSI path for no reachable guest benefit); findings unreachable by the target guests (DMA-mode SELECT, message-phase negotiation/recovery, the two-deep command sequencer / ENSEL, the PIO data stubs, the reset identity); items deferred for want of infrastructure beyond this scope (the R4030 translation-limit / memory-error fault interrupt, DMA residual / terminal-count fidelity, a nexus-preserving Transfer Pad, and the FIFO Gross-Error / cur_phase / TC-on-INTR datasheet details); and deliberately-stubbed items that must stay as-is (the empirically-tuned function-complete suppression, target-mode commands, the translation-cache-invalidate no-op, reserved read registers). No source change.
---


## Fortieth round (#269, #270) — self-review corrections: ASC FIFO diagnostic flood + breakpoint-listing honesty
A five-model code review of our own #254–#268 batch (Codex 5.6-sol ultra + agy Gemini 3.6 + Kimi 3 MAX + Fable 5 + Opus 5; two passes, unanimous on scope) found two defects **we** introduced. Both are host-side diagnostics — no guest-visible behaviour changes in either correction.
- **#269** `devices/dev_asc.c` (both trees): **#265** relocated the ASC FIFO overflow warning into the drop guard, which turned an at-most-once-per-fill message into **one host line per dropped byte** — measured, 24 overflow writes produced 24 host lines. The pre-existing read-side twin (the **#197** empty-FIFO guard, whose message says "overrun" for historical reasons although the condition is a read of an *empty* FIFO) behaves identically: 24 reads of an empty FIFO produced 24 lines. This matters beyond noise, because `fatal()` is **not verbosity-gated** and `va_debug()` writes stdout **one character at a time** — the same stream the boot harness pattern-matches — so an undrained pipe can block the single-threaded emulator. Both sites now warn **once per device**, via one-shot latches in `struct asc_data`, and deliberately keep `fatal()`: a verbosity-gated `debugmsg()` was rejected because under `-q` the harness verbosity settles at `VERBOSITY_ERROR` (`main.c` lowers it by one; `debugmsg_add_verbosity_level()` floors at 0), so a WARNING-level message would be **invisible to the boot-log hygiene grep**, while an ERROR-level one would change the printed form *and* would trip **#261**'s global break-on-ERROR whenever that is armed. The latches are deliberately **not** cleared by `dev_asc_reset()` or `dev_asc_fifo_flush()` — otherwise a guest could re-arm the flood with `RSTCHIP` — and are zeroed by the `memset` in `dev_asc_init()`. Everything the guest can observe (the dropped byte, the value returned by a read of an empty FIFO, the FIFO indices and count, the registers, the interrupts) is unchanged.
- **#270** `core/debugmsg.c` (both trees): **#261**'s global break-on-ERROR toggle was **invisible** in the `breakpoint subsystem` listing. `breakpoint subsystem all error` arms that global *and* sets every per-subsystem level; a later `breakpoint subsystem <name> off` clears only that subsystem's level, so an ERROR-level message from it still enters the debugger — yet `debugmsg_print_breakpoints()`, which skips subsystems at level < 0, listed it as unarmed and never mentioned the global (measured: 24 rows after arming, 22 after `cpu off`, `cpu` absent, the global never named). The listing now discloses the global, and no longer prints "No breakpoints on subsystem messages set." while it is armed. The **override semantics are deliberately unchanged** (panel-unanimous): they are not observable on pmax/arc — neither has a runtime-reachable ERROR-level `debugmsg()` — and every redesign considered was worse than simply stating the behaviour. Display only.
Verified: build **0/0** both trees; **pmax 15/15 + arc 13/13 → `uid=0(root)`**; log-hygiene greps all **0** (the "FIFO overrun" token is preserved, so that gate still works). Both flood probes drop from **24 host lines to 1** — write side and read side — while the deliberately-untouched `TRPAD` control still emits 10 lines for 10 commands. A single-session probe shows the two latches are **independent** (a 24-write overflow burst → 1 line; then, after draining the FIFO, a 24-read empty burst → 1 further line, which a shared latch would have suppressed) and that the latch **survives a guest `RSTCHIP`** (5 further empty reads → 0 lines, with `NCR_FFLAG` reading 0 afterwards, so those reads necessarily took the guard). For **#270**, the review probe's own assertion flips **false → true** with no edit to the probe, and `breakpoint subsystem all off` makes the new line disappear and the "No breakpoints …" message return.

**Known gaps (documented, deliberately not fixed in this round).** `dev_asc.c` still contains **20 further unconditional `fatal()`/`printf()` diagnostics** of the same family (22 live call sites, minus the two now latched). Two are worth naming. The stray-register-access report (`dev_asc.c` `:936`/`:939` before this round, `:969`/`:972` after) prints one host line **per access** at asc offsets ≥ 0x10 (arc/PICA) or ≥ 0x40 (pmax/DEC); because it carries a **variable payload** — the offset and the value — a one-shot latch would hide real information, so it wants **#245**-style verbosity gating instead. The **#264** zero-length-`DATA_OUT` site is excluded on **scope-coherence** grounds and *not* because it is untestable: it reproduces cleanly (10 `TRPAD` commands → 10 host lines), but its `fatal()` was panel-locked for symmetry with the **#167** guard, so revisiting it belongs with that guard rather than here. These belong to a dedicated `fatal()`-hygiene round.
---


## Forty-first round (#271, #272) — VGA CRTC: a guest-reachable host abort, and a driver-reachable diagnostic flood
Both corrections are in `devices/dev_vga.c`, which is **not** one of the five divergent files, so the two trees stay byte-identical. They were found by the same sweep and share one probe rig, but they are **not the same shape** — #271 is a control-flow change plus a latch, #272 is output-only — so this round carries **two independent probes** and neither is allowed to stand in for the other.
- **#271** `devices/dev_vga.c` (both trees): **two guest byte stores killed the emulator process.** Selecting CRTC index `0xff` and then writing a mode byte outside the eleven implemented modes reached `default: fatal("TODO! video mode change hack …"); exit(1);` inside `vga_crtc_reg_write()` — measured on the committed build: wait status `exited, code 1`, pty EOF, the `fatal()` text as the last output, while an *accepted* mode byte (`0x03`) survived. A guest must not be able to `exit()` the host — the **#167** / **#240** / **#264** rule — so the abort is gone. The arm now **returns** rather than breaking: a *rejected* mode must have **no side effects**, and falling through would have run the geometry/resize block and then `reset_palette(d, grayscale)` with `grayscale == 0`, i.e. a rejected write would clear the screen and reset the palette to colour. (The fall-through is *not* a **#182**-shape stale-length overrun — the geometry left in `d` is self-consistent — so this is side-effect suppression, not a memory-safety fix.) `d->crtc_reg[0xff]` is deliberately **left holding the rejected byte**: every other unhandled CRTC index is RAM-backed too, so making `0xff` read back differently would be the inconsistency, and the previously accepted mode is not reconstructible anyway (`0x00`/`0x01`, `0x02`/`0x03` and `0x09`/`0x0d` produce identical geometry, and a restore would need new state *and* a change in the caller). Because removing the abort turns a one-shot exit into a repeatable ungated `fatal()` — the **#265** → **#269** shape — the warning is latched to **once per device instance** through a new `invalid_mode_warned` field in `struct vga_data`, deliberately **not** cleared by `register_reset()` (an accepted mode set is the only guest-reachable reset here, so clearing it there would let a guest re-arm the flood) and zeroed by the `memset` in `dev_vga_init()`. `fatal()` is kept rather than gated: exactly one visible line is what a deficiency tripwire should leave under `-q`, the mode the boot harness runs.
- **#272** `devices/dev_vga.c` (both trees): the **outer** `default:` arm of the same function reported every unhandled CRTC index with an ungated `fatal()` — measured **1.00 host lines per guest data store**; arming the index is silent and one index store then licenses unlimited one-store repeats. Only indices `0x0a`–`0x0f` are handled (measured by sweep), so **every horizontal/vertical timing register an ordinary VGA driver writes during a mode set lands here** — this is reachable by legitimate driver software, not only by a hostile guest. The emulator survives it; this is a flood, not an abort. It is now `debugmsg(SUBSYS_DEVICE, "vga", VERBOSITY_DEBUG, …)` carrying the same payload. A latch was wrong here: the payload is *variable* (index and value), so latching would hide real information, and this is ordinary-if-unimplemented traffic rather than a deficiency tripwire, so it should simply be silent in a normal run. Output only; nothing the guest can observe changes.
Verified: build **0/0** both trees (223 pmax / 224 arc objects); **pmax 15/15 + arc 13/13 → `uid=0(root)`**; log-hygiene greps on both boot pty logs **0** for `vga_crtc_reg_write`, for `video mode change hack`, and for `panic`. **#271 probe, 11/11:** the two-store sequence that exited with code 1 on the committed build now leaves the process alive and answering (`dead=False`, `pc` readable); a witness byte planted in the handled register `0x0e` **survives** a rejected mode (`0x5a` → `0x5a`), proving the `return` suppressed the side effects, while an accepted `0x03` zeroes it (`0x5a` → `0x00`), proving the accepted path still performs the mode change; `crtc_reg[0xff]` reads back `0x55`, the rejected byte; **12 rejected sequences in one session produce exactly 1 host line**, and 3 more after an accepted mode set — the device reset — produce **0**, so the latch cannot be re-armed. **#272 probe, 8/8, both halves:** under `-V step` the call site still fires 8/8 = **1.00 per store** (`debugmsg.c:181` skips the verbosity test while `single_step` is set, so this proves the site is live, not that it is ungated); suppression is therefore measured **free-running**, with the CPU parked in a loop that stores to the data port and counts its own iterations — **93,454,400 stores in 2.51 s produced 0 lines** (10 bytes of host output total). Two controls keep that from being a blind rig: the same free run with `-v -v` (verbosity DEBUG) prints **313,468 lines for 314,080 stores**, and the pre-fix binary at default verbosity prints **418,881 lines for 420,160 stores** — i.e. the old `fatal()` did flood a normal, non-stepping run, and the new silence is the verbosity gate.

**Scope (honest).** This round swept the **pmax/arc device set** for guest-reachable `exit()`, not the whole tree. `devices/dev_wdc.c` still has four guest-reachable `exit(1)` calls — one fires on **any failed ATAPI command** (`WDC: ATAPI scsi error?`) — but neither `machine_pmax.c` nor `machine_arc.c` instantiates it (the ARC `wdc` line is inside `#if 0`), so it is out of scope here and left for a tree-wide `fatal()`/`exit()` hygiene round. Note also that **our tree is more exposed than upstream on exactly this device**: SEC's `machine_arc.c` forces `fb_console = 1` for PICA and therefore calls `dev_vga_init()` even headless, while `est`'s gates the same call on `machine->x11_md.in_use` — so on SEC a plain `-e pica` run instantiates the VGA device, and the abort was reachable without X11.
---


## Forty-second round (#273) — FP→integer conversion: undefined behaviour, and a result that depended on the build host
- **#273** `core/float_emul.c` (both trees): `ieee_store_float_value()` converted to the **W** (32-bit) and **L** (64-bit) integer formats with a bare `r3 = (int64_t) nf;`. In C, that cast is **undefined** when `nf` is NaN, ±Inf, or outside the destination range — so the guest-visible result was decided by the host's FP instruction rather than by the emulated CPU. On x86-64 `cvttsd2si` returns the "integer indefinite" `0x8000000000000000`, which the W path's trailing `r = (uint32_t) r` then truncates to **`0x00000000`**; on aarch64 `fcvtzs` **saturates** instead, so the same guest binary would see different answers on different build machines. Real R3010/R4010 hardware, with the Invalid trap disabled, returns the **maximum positive integer** — `0x7fffffff` for W, `0x7fffffffffffffff` for L — for **all five** invalid cases (NaN, +Inf, −Inf, +overflow, −overflow), with **no sign dependence**. Sources: MIPS R4000 User's Manual (Heinrich), `CVT.W.fmt` — "If Invalid operation is not enabled, then no exception is taken and 2^31−1 is returned"; MIPS IV ISA Rev 3.2 (Price, 1995) p. B-50, under the MIPS I heading — "the default result, 2^31−1, is written to `fd`"; corroborated by Linux `arch/mips/math-emu/ieee754.h` (`ieee754si_indef()` → `INT_MAX`, and `ieee754si_overflow()` **ignoring** the sign argument, when `!nan2008`) and by pre-2014 QEMU (`#define FP_TO_INT32_OVERFLOW 0x7fffffff`). The **`0x80000000`-for-negative-overflow** rule that an earlier note in this project assumed is the **NAN2008/r6** rule, which also returns **0** (not `0x7fffffff`) for NaN — neither applies to the R3010/R4010, which have no `FCSR.NAN2008` bit. Operands are now classified before the cast, and the cast runs **only when the value is in range**.
  The two range bounds are deliberately **asymmetric**, and the asymmetry is load-bearing: W's lower bound is `nf <= -2147483649.0`, **not** `nf < -2147483648.0`, because `trunc(-2147483648.5)` is exactly `INT32_MIN` — representable, therefore **not** an overflow, and it must convert normally to `0x80000000`. L's lower bound is a strict `<` because −2^63 **is** exactly representable. W's *upper* bound has deliberate slack (it rejects the open interval between 2147483647.0 and 2^31, where truncation would have produced `0x7fffffff` anyway) — harmless today, and it would only matter if FCSR Invalid **signalling** were added later. `2^63` is written as the literal `9223372036854775808.0` on purpose: `(double)INT64_MAX` rounds **up** to exactly 2^63, which would let the equality case fall through to the undefined cast.
  **Blast radius is zero outside MIPS.** `float_emul.c` is shared by the alpha, m88k, mips, ppc and sh cores (plus `dev_pvr`), but `IEEE_FMT_W`/`IEEE_FMT_L` occur only in `float_emul.c`, `include/float_emul.h:45-46` and `cpus/cpu_mips_coproc.c:1033` — the W/L arm has **no** non-MIPS caller, and the S and D arms (which do) are untouched. **#255**'s NaN canonicalizer still guards on `IEEE_FMT_S`/`IEEE_FMT_D` only, so W/L results pass through it unmodified, as before.
Verified: build **0/0** both trees (223 pmax / 224 arc objects); **pmax 15/15 + arc 13/13 → `uid=0(root)`**; log-hygiene greps **0** on both boot pty logs. **Measured first, on the committed build** (`p2_fp_cvt.py`): **11 of 13** non-control cases diverged from the hardware default, **identically on arc/R4000 and pmax/R3000A** ("arc vs pmax differences: none") — NaN, ±Inf and ±1e30 all returned `0x00000000` and +2^31 returned `0x80000000`. **#273 probe, 55/55 on arc and 44/44 on pmax**, across **all three** instructions that reach this arm (`cvt.w.fmt`, `trunc.w.fmt`, `trunc.l.fmt` — all route through `FPU_OP_CVT`; there is **no `cvt.l`** in the tree, so `IEEE_FMT_L` is produced by `trunc.l` alone): every invalid case now returns the pinned constant and every in-range control is unchanged (`2147483647.0`→`0x7fffffff`, `-2^31`→`0x80000000`, `3.0`/`3.5`/`3.25`→`3`, `-3.25`→`0xfffffffd`). The asymmetry is covered by its own boundary cases: **`-2147483648.5` → `0x80000000`** (the value a `< -2147483648.0` predicate would have wrongly saturated) and, for L, **−2^63 → `0x8000000000000000`** while **−2^63−2048 → `0x7fffffffffffffff`**. **In-guest end-to-end on OpenBSD/pmax**, against a purpose-built pre-#273 binary: `awk 'BEGIN{print sprintf("%d", 1e30)}'` prints **0 before → 2147483647 after**, and `-1e30` likewise prints **+2147483647**, the sign-independence no software clamp would reproduce; the in-range controls (`2147483647`, `-2147483648`, `3.9`→`3`, `-3.9`→`-3`) are byte-identical on both binaries. Note that awk's **`int()`** does *not* exercise this path — it stays in floating point (`int(1e30)` prints `1.00000000000000001988462483866e+30` on both binaries, and `int(3.9)` yields `4`, i.e. it is not a truncating C cast) — so `printf`/`sprintf` `%d`, which does cast a double to a C `long`, is the route that reaches the FPU.
---


## Forty-third round (#274, #275) — LANCE: descriptors held forever instead of dropped or failed
Both corrections are in `devices/dev_le.c`, which is **not** one of the five divergent files, so the two trees stay byte-identical. This round finishes what **#262** (receive) and **#199** (transmit) started: in five places the emulated Am7990 reached a descriptor it could not use and simply **returned** — OWN left set, the ring pointer not advanced — so nothing was delivered, nothing was dropped, no interrupt was raised, and a well-formed descriptor queued behind the bad one was never reached. Everything below was **measured on the committed build first**, in the cold debugger: `dev_le_access()` ends every access with `dev_le_tick()`, so one guest CSR0 load pumps the engine and no boot is needed.
- **#274** `devices/dev_le.c` (both trees): **receive.** A malformed receive descriptor — rmd2 without the `'1111'` mark, or a byte count outside the 12…1900 window the model accepts — made `le_rx()` `return 0` with the inbound frame still latched in `d->rx_packet`. Measured: the frame was **not delivered, not dropped, no RINT, no MISS**, and repairing the mark alone later delivered **the same frame** — held, not lost — while the bad-count arm re-emitted its `VERBOSITY_WARNING` on **every tick** for as long as the descriptor stayed bad. The **#262** lookahead that protects the chained case tested only the next descriptor's `OWN` bit, so a frame could still be walked into an OWNed-but-malformed descriptor mid-chain. The lookahead now requires the next descriptor to be **usable**, not merely chip-owned: `OWN` set **and** the mark **and** the count in range. That test and the one at the top of the loop now go through a single new static predicate, `le_rx_descr_ok()`, so their bounds cannot drift apart — a `<`/`<=` seam between the two is exactly where a frame could have slipped through. With the lookahead extended, the malformed arm at the top of the loop is reachable **only for the first buffer of a frame** (nothing changes under the engine within one call, and no exit leaves a frame in progress across calls any more), so it now mirrors the exhaustion path immediately above it: `CSR0.MISS`, release the frame, `return 1`. The descriptor is deliberately **not** written back and **no** `ERR|BUFF` is stamped — nothing was filled in, and the guest never updated rmd3, so consuming a descriptor we have just declared malformed would write status into a misconfigured ring entry. The `return 1` is load-bearing rather than tidy: returning 0 after freeing the frame lets `le_register_fix()` fall through and re-poll `net_ethernet_rx_avail()`, which **imports** packets on every call — the livelock trap that motivated #262's drain fix. The two arms collapse into one warning that names the descriptor and keeps the old `buflen = %i` text, and it is now emitted at most **once per dropped frame** instead of once per tick. Honest scope: the Am7990 manual defines **no** status for a descriptor that violates the `'1111'` programming rule, so reporting it as a missed packet is **hardened emulator policy, not proven silicon**.
- **#275** `devices/dev_le.c` (both trees): **transmit.** Four sites left a descriptor chip-owned forever. All four were measured on a two-entry ring with a well-formed **canary** behind the bad descriptor, which makes "did `txp` advance" directly observable: **(a)** a bad `'1111'` mark (`return`, and **totally silent**), **(b)** a byte count out of range (`return`, plus `le tx: buflen = N` **every tick**), **(c)** our own **#199** 64 KB aggregate cap (frees the host buffer, but never clears OWN and never writes back) and **(d)** an idle descriptor with `OWN` set and `STP` clear. In each case OWN stayed set, `d->txp` never advanced, the canary was never transmitted, `CSR0.TINT` was never raised and the guest waited forever; repairing tmd2 released both descriptors at once, proving the engine had been parked on the bad one. The "warns forever" long attributed to **(c)** is actually emitted by **(d)** on the following tick — the cap clears `tx_packet` while the descriptor still has `stp == 0` — and free-running it produced **82,264 warnings in 3.01 s (27,345 lines/second, 3.2 MB)** with `CSR0.TINT == 0`, a fixed point that never tells the guest anything.
  (a), (b) and (c) now **consume the descriptor with an error**, through one new helper `le_tx_abort()`: `ERR` in tmd1, `TBUFF|UFLO` in tmd3, the descriptor written back, `CSR0.TINT` set, `CSR0.TXON` cleared and `txp` advanced. `LE_TBUFF` is `0x8000`, **numerically identical to `LE_OWN`**; it belongs in tmd3 **only**, and the comment says so, because in tmd1 it would put OWN straight back and turn the hold into an own-forever. Clearing TXON is what the manual prescribes for this error class (`TMD3` bit 15: "BUFF error disables the transmitter (CSR0 = TXON = 0)") and it genuinely stops the engine here, since `le_register_fix()` gates the `le_tx()` call on `TXON` — which is also why the abort `return`s instead of walking on.
  **(d) gets a different fix, and the datasheet dictates it:** clear OWN, write tmd1 back, set TINT, advance — and set **no error bit at all**. The decision also moves **ahead** of the tmd2 validation, because while polling the chip reads TMD1 only and does not fetch the byte count from TMD2 until it has found OWN+STP; validating TMD2 on a descriptor hardware has not consumed is not hardware behaviour. Its message drops to `VERBOSITY_DEBUG`: skipping a bad-format entry is *defined* chip behaviour, not an error, and the guest is told through TINT. Neither NetBSD nor OpenBSD ever creates this condition (both stamp `OWN|STP|ENP` on every TX descriptor, and neither does TX data chaining), so **(d) is hardening, not a bug with a live victim**; (a) has no documented silicon behaviour either, so its consume-with-error is likewise **policy**.
  Two sub-decisions were taken from the manual rather than from the panel, and are recorded with their quotes in `REVIEW_FINDINGS.md`: **`CSR0.BABL` is deliberately NOT set** on the #199 cap path (BABL is defined as transmitter-on-channel time — "set after 1519 data bytes have been transmitted", with the chip *continuing* to transmit — and our cap aborts a frame that was never put on the channel), and **tmd1 `ERR` is set** there (the manual makes ERR the OR of LCOL/LCAR/**UFLO**/RTRY, and NetBSD's `am7990_tint()` counts an error-free descriptor as `if_opackets`, i.e. as a frame successfully sent).
Verified: build **0/0** both trees (223 pmax / 224 arc objects); **pmax 15/15 + arc 13/13 → `uid=0(root)`**; log-hygiene greps **0** on both boot pty logs for `panic`, `le rx:`, `le tx:`, `unusable`, `skipped`, `buflen =` and `all descriptors used up`; live ping **3/3 received, 0% loss**; `dev_le.c` byte-identical in all four tree copies (one md5) and the divergence set still exactly the five known files. **The shipping gate is the would-fire counter, not the boot**, because a false fault on the receive path is silent — a healthy chained frame truncated and dropped reads as a flaky network, never a crash. The observe-only instrumentation was therefore rebuilt against the **changed** predicate and re-measured: **`la_extra_reject` = 0** on a healthy boot + ping (`rx_calls=14 frames=14 top_badmark=0 top_badlen=0`) and **0** on a flood (`rx_calls=321 frames=321`), both counter lines **byte-identical to the pre-change measurement**; its positive control still passes on the changed binary (a cleared mark and a bad length on the *next* descriptor each score `la_extra_reject=1`, a healthy one scores 0), so the zero is a real zero and not dead code. **#274 probe:** a malformed **first** descriptor now sets `CSR0.MISS`, delivers nothing, leaves the descriptor untouched (OWN kept, rmd3 = 0) and emits exactly **one** host line; repairing it *without* soliciting a new frame delivers **nothing** (pre-change the same held frame arrived), and the **next** frame is then received normally (`rmd3 = 0x4e`) — the anti-livelock assertion. The chained control still delivers (`rmd3 = 0x4e`), while the mid-frame variants now terminate the first descriptor with `ERR|RBUFF` (`rmd1 = 0x4600`) and the mid-frame arm is unreachable (`le rx: buflen = 4` no longer appears). **#275 probe:** (a)/(b) leave `tmd1 = 0x4300` (ERR, OWN clear) with `tmd3 = 0xc000` (TBUFF|UFLO) and `CSR0 = 0x03a2` (TINT set, TXON clear), and the per-tick `buflen =` flood falls from **11 lines to 1**; (c) leaves descriptor 34 at `tmd1 = 0x4000` with TINT set and TXON clear, its warning count over six pumps falls from **12 to 0**, and the free-running flood falls from **27,345 lines/second to 0 lines in 3.01 s** (10 bytes of host output in the window); (d) clears OWN with `tmd1 = 0x0000`, `tmd3 = 0x0000` — **no error bit** — keeps TXON, sets TINT and transmits the canary **in the same pass**, and does so identically when tmd2 carries a bad mark, which is the direct test of the TMD1-only reordering. After (a)'s abort the canary goes out as soon as the driver performs the recovery the manual and `am7990.c` prescribe (STOP → re-queue → INIT|STRT restores `TXON`).
---


## Forty-fourth round (#276, #277) — ASC: two guest-repeatable diagnostic floods, fixed in deliberately opposite ways
Both corrections are in `devices/dev_asc.c`, which is **not** one of the five divergent files, so the two trees stay byte-identical. `fatal()` is ungated and writes stdout one character at a time — the stream the boot harness pattern-matches — so any guest-repeatable `fatal()` in a device model hands the guest control of the host log, and an undrained pipe can block the single-threaded emulator; **#269** already latched two sites in this same file. **The two sites in this round get opposite treatments, on purpose.** The axis is **not** payload variability — that heuristic is retired as a mis-classifying proxy, see `REVIEW_FINDINGS.md` — but **whether the guest is told what happened through some other channel**.
- **#276** `devices/dev_asc.c` (both trees): the final `else` arm of `DEVICE_ACCESS(asc)` reported every access to an offset the device does not model with an ungated `fatal()` — measured **1.00 host lines per guest access** on the committed build, for reads *and* writes, at offsets `0x10`, `0x40`, `0x300` and `0xff0`, while an in-range register (FFLAG) printed **0**. On arc/PICA `regnr == relative_addr` and the window is `DEV_ASC_PICA_LENGTH = 0x1000`, so **every** access in `0x10..0xfff` lands there; on pmax/DEC `regnr = relative_addr/4`, which makes the affected range `[0x40,0x300) ∪ [0x600,0x40000)` — the TURBOchannel redirect covers the gap. Free-running, a three-instruction guest loop produced **800,370 host lines / 26.4 MB in 3.07 s**. This is ordinary probing traffic for registers we do not implement, not a deficiency tripwire, **and the guest is answered either way** — a read returns `odata`, a write is dropped — so nothing is left waiting on a message that is not printed. Both arms are now `debugmsg(SUBSYS_DEVICE, "asc", VERBOSITY_DEBUG, …)` carrying the same payload; the hand-written `[ … ]` brackets and the trailing `\n` go away because the helper supplies them, and `relative_addr` (a `uint64_t`) is now cast for `%x`, as the disabled debug block at the top of the same function already does. Output only; nothing the guest can observe changes.
- **#277** `devices/dev_asc.c` (both trees): two **one-shot latches**, in the style of #269, on the two transfer diagnostics a guest can repeat indefinitely. `dev_asc_transfer()`'s final `else` (`!!! TODO: unknown/unimplemented phase in transfer: %i`) is reached because the transfer tail leaves `cur_phase == PHASE_STATUS`, which no branch above handles; `dev_asc_newxfer()`'s `freeing previous transfer` fires on two SELECTs without an intervening MSGOK. The two were measured **together at 2.00 host lines per guest store** on the committed build, identically on arc/PICA and pmax/DEC. Each gets its **own** `int` in `struct asc_data` (`unknown_phase_warned`, `newxfer_warned`) — a single shared flag would let whichever message fires first mask the other one for good — and neither is cleared by `dev_asc_reset()`, so a guest cannot re-arm the flood with RSTCHIP; both are zeroed by the `memset` in `dev_asc_init()`. `dev_asc_newxfer()`'s bare `printf()` becomes `fatal()`, the only bare `printf()` left in this path, so the line is decorated like the rest of the file; the transfer itself is still freed on **every** call. **`fatal()` is kept here, and #276's DEBUG gate deliberately not applied, in the same commit:** the `else` arm sets **no interrupt**, so the transfer simply hangs — under `-q`, the mode the boot harness runs, a gate would be total silence while the guest wedges, whereas a latch leaves exactly **one** line in the log the harness greps. Note that this site's payload *is* variable (`cur_phase`) and it is latched anyway; the payload rule does not decide these cases.
Verified: clean rebuild **0/0** both trees (223 pmax / 224 arc objects); **pmax 15/15 + arc 13/13 → `uid=0(root)`**; log-hygiene greps **0** on both boot pty logs for `panic`, `Segmentation`, `assert`, for **all four** strings this round changes (`asc: read from`, `asc: write to`, `unknown/unimplemented phase`, `freeing previous transfer`) and for `FIFO overrun` / `data_out_len == 0`; `dev_asc.c` byte-identical in all four tree copies (one md5) and the divergence set still exactly the five known files. **Before gating any string, the tree and the harness scripts were grepped for all four** — the only consumers anywhere are the two TEST-FIRST probe rigs themselves; no boot script, hygiene script or regression script matches on them, so a DEBUG gate cannot silence an existing assertion. **#276 probe, both halves plus a positive control:** under `-V step` the site still fires **12/12 reads and 12/12 writes** — `debugmsg.c:181` skips the verbosity test while `single_step` is set, so that proves the site is live, *not* that it is ungated — with the in-range control at **0**; suppression is therefore measured **free-running**, with the CPU parked in a loop hammering `asc+0x10`: **0 lines in 3.02 s** (2,010 bytes of host output in the whole window) against **800,370 lines / 26,414,220 bytes in 3.07 s** on a purpose-built pre-change binary, with the pc read back after `^C` and verified still inside the loop in both runs. The blind-rig control is the same free run with `-v -v` (SUBSYS_DEVICE at `VERBOSITY_DEBUG`): **505,944 lines / 20.2 MB**. **#277 probe, one session, both latches, counted with distinct substrings and never by subtraction:** 12 SELECT rounds — 11 of them entering `dev_asc_newxfer()` with `xferp != NULL` — print **11 lines before → 1 after**, and **0** `unknown/unimplemented phase` in either build, the SELECT path never entering `dev_asc_transfer()`; 12 `TRPAD|DMA` stores with `cur_phase == PHASE_STATUS` print **12 before → 1 after**. That second count *is* the cross-check: `newxfer`'s latch is already set when it runs, so a shared field would have reported **0**. After `RSTCHIP`, three more of each trigger print **0 and 0** — the reset does not re-arm. Liveness is asserted independently of the latched messages, so a dead trigger cannot pass as a working latch: **12** `TEST_UNIT_READY`s reached the disk, **12** entries into `dev_asc_transfer()`, and `STAT = 0x83` (`cur_phase == 3`) sampled with a genuine guest `lbu`.
---


## Forty-fifth round (#278) — MIPS exception path: nine ungated `fatal()` calls per low-address guest access
`cpus/cpu_mips.c` is **not** one of the five divergent files, so the two trees stay byte-identical — but unlike the last four rounds this file is shared by **every MIPS machine in the tree**, not just pmax/arc, which is why the correction gets its own commit and its own bisect point. The change is **output-only**: no control flow, no state, nothing a guest can observe.
- **#278** `cpus/cpu_mips.c` (both trees): in `mips_cpu_exception()`, `if (tlb && vaddr < 0x1000)` built **one** host line out of **nine separate `fatal()` calls**, once for every guest access to a low virtual address — measured **1.00 host lines per access on both CPUs** (arc/R4000 `EXC4K` and pmax/R3000 `EXC3K`), per-iteration attribution `1111111111`, so it is a per-event flood and not a once-only latch. `fatal()` is ungated, and this site sits **outside** the `if (!quiet_mode)` block that opens at `:1846` and closes at `:1916`, so `-q` did not silence it either. It is now a single `debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "LOW reference", VERBOSITY_DEBUG, …)` carrying the same payload — vaddr, exception name, pc, symbol — with the 32-bit/64-bit field widths preserved through a `%0*` width argument, and the `cpu%i: ` prefix now supplied by the helper. `SUBSYS_EXCEPTION` exists in this tree (`misc.h:250`, registered as `"exception"` at `debugmsg.c:691`) and is the subsystem the in-source TODO preferred; the general MIPS exception message added by **#210**, twenty lines below, already uses it.
- **Reproduction precondition — recorded deliberately, because without it the defect looks imaginary.** The site is gated on `tlb`, i.e. `memory_mips_v2p.c`'s `tlb_refill`. On a **never-booted** rig every TLB entry is zeroed, so the zeroed entry *matches* vaddr 0 (`entry_vpn2(0) == vaddr_vpn2(0)`, `entry_asid(0) == vaddr_asid(0)`), its V bit is clear, and the code takes the *TLB invalid* arm — which clears `tlb_refill`. The site then prints **nothing**: measured **0/10** on both CPUs. With a **non-zero ASID** (`EntryHi = 0x01` on arc, `0x40` on pmax — the state any OS running a user process is in) it is **10/10**. A control at vaddr `0x1000` takes the refill but does **not** print, isolating `vaddr < 0x1000` rather than "any TLB miss". A future reviewer running the obvious cold-rig test gets 0/10 and would otherwise conclude the defect was never real.
- **`VERBOSITY_DEBUG`, not the `VERBOSITY_WARNING` the in-source TODO asked for.** `main.c` prints INFO during startup and then subtracts one level, so a default run settles at `VERBOSITY_WARNING(1)`: a WARNING-level message would print on **every** call, and a WARNING-level gate was separately measured in this batch flooding a free-running rig at **27,345 lines/second**. Under `-q`, `main.c` sets `VERBOSITY_ERROR(0)` and `debugmsg_add_verbosity_level()` floors at 0, so a WARNING is **invisible in exactly the mode the boot harness greps**. WARNING is the one level that fails both goals; DEBUG is quiet in a normal run and under `-q`, and still visible under `-V` for the edge-branch proof. The site's own semantics agree: with a non-zero ASID it fires on **every userland NULL dereference**, which is ordinary guest behaviour, not an emulator deficiency, so it does not deserve tripwire status. The reasoning is in the source comment so the TODO's WARNING is not "restored" later as a fix.
- **No `ENOUGH_VERBOSITY()` pre-gate.** `debugmsg.c:181` is `if (!subsystem_breakpoint && !single_step && !ENOUGH_VERBOSITY(subsystem, verbosity)) return;` — the verbosity test is *deliberately* bypassed while `single_step` is set and for subsystem breakpoints. A raw pre-gate would suppress the message under `-V step` and stop `breakpoint subsystem exception` from ever firing here. `debugmsg` does its own gating; the preceding symbol lookup is not costly enough to justify pre-gating it.
Verified: clean rebuild **0/0** both trees (223 pmax / 224 arc objects); **pmax 15/15 + arc 13/13 → `uid=0(root)`**; log-hygiene greps **0** on both boot pty logs for `LOW reference`, `warning: LOW`, `exception LOW reference`, `panic`, `Segmentation`, `assert` and `Bus error` (the single `TODO` hit in the arc log is the pre-existing `[ pckbc: TODO: hack for non-8242 … ]` device line); `cpu_mips.c` byte-identical in all four tree copies (one md5) and the divergence set still exactly the five known files. **`LOW reference` was grepped tree-wide and across every harness/regression script before being gated**: the only consumers anywhere are the two TEST-FIRST probe rigs themselves and one read-only marker counter, plus a retired `_archive/` audit classifier; no boot script or gating assertion matches it. **Blast-radius gate:** five *other* MIPS machines (`testmips`, `baremips`, `evbmips/malta`, `sgi/o2`, `hpcmips/mobilepro770`) start under `-V`, reach the debugger prompt and produce output **byte-identical** to the pre-#278 binary. **Probe, 36/36 checks, both halves plus two controls, on both CPUs:** under `-V step` the site still fires **10/10 = 1.00 per faulting step** with the payload intact and each message **one** physical line — that proves the site is live, *not* that it is gated, because `debugmsg.c:181` skips the verbosity test while `single_step` is set — with the cold-TLB and vaddr-`0x1000` controls at **0**. Suppression is therefore measured **free-running**, with the CPU parked in a self-sustaining exception loop (a two-instruction handler written at every vector the refill can reach, counting its own iterations): **19,631,880 faults in 3.00 s → 0 lines** on arc and **19,366,920 in 3.01 s → 0** on pmax, pc read back after `^C` and verified still in the handler. Two controls keep that from being a blind rig: the same free run at `-v -v -v` (DEBUG) prints **123,015 / 115,557** lines, and the **pre-#278 binary at default verbosity prints 267,074 lines (28.6 MB) / 136,193 lines (12.4 MB)** in the same window — so the old `fatal()` did flood a normal non-stepping run, and the new silence is the verbosity gate. That baseline also prices the flood: in the same three-second window the flooding build got through **269,100** faults where the gated build got through **19,631,880** on arc (**1.4 %**), and **136,620** against **19,366,920** on pmax (**0.7 %**). **On a healthy boot the site is latent** — the pre-#278 binary, whose `fatal()` `-q` could not suppress, printed `LOW reference` **0** times across a full pmax 15/15 and arc 13/13 boot — so this is hardening and debuggability, not a log-hygiene defect the harness was living with.
---


## Forty-sixth round (#279) — `float_emul.c`: the reserved-format `fatal()` cluster, and one genuinely missing `return`
`core/float_emul.c` is **not** one of the five divergent files, so both trees stay byte-identical. Like **#278** this is an arch-shared file, and shared more widely than that one: `ieee_interpret_float_value()` and `ieee_store_float_value()` are called by the **alpha, m88k, mips, ppc and sh** cores plus `dev_pvr`. **#273** touched this same file but was confined to the MIPS-only W/L arm; this round touches the paths all five families use, so it gets its own commit, its own bisect point and its own blast-radius gate. Everything here is **output-only** except one `return` on an already-broken path.
- **#279** `core/float_emul.c` (both trees): five ungated `fatal()` sites — `:64`, `:82`, `:154` in `ieee_interpret_float_value()` and `:216`, `:306` in `ieee_store_float_value()` — fire whenever the format argument is not S/D/W/L. **Measured on the committed build first, identically on arc/R4000 and pmax/R3000A:** one `add.ps` produced **8.0 host lines per instruction** (6.0 interpret + 2.0 store), one `abs.ps` **5.0** (3.0 + 2.0); `fd` was silently written **`0x00000000`** and the emulator kept running. Per call that is **3.00** interpret lines (three sites in one function, no `return` between them) and **2.00** store lines.
- **The missing `return` at `:216` is a genuine bug, and it is now fixed.** That `default:` has no `return`, so it falls out of the first switch into the SECOND switch's `default:` at `:306`, which prints a second line for the same call. It now does `return 0` — `r` is still 0 there and the tail only masks it to 32 bits, so the value returned is exactly what the old path returned. **Measured with the latch forced off: 2.00 → 1.00 store lines per store CALL** (per-iteration attribution `111111111111`), on both CPUs. The `:306` arm is unreachable once `:216` returns; it is kept, and latched with the same flag, so the invariant survives if that `return` is ever removed again.
- **Scope is PS-only, and that was measured too.** `mips_fmt_to_ieee_fmt[]` (`cpu_mips_coproc.c:1029`) maps every fmt outside {S,D,W,L} to 0, but only PS reaches `float_emul.c` at all: `cpu_mips_instr.c:4991-4995` routes {S,D,W,L,PS} to `cop1_slow`, while every other reserved fmt hits the decoder's own single `fatal("COP1 floating point opcode = 0x%02x")` + `goto bad` at `:5006-5008`. The probe carries fmt 18 and fmt 23 as controls: **0** `float_emul` lines from either, on both CPUs.
- **A one-shot latch per message, not a verbosity gate — the axis #276 was decided on, landing the other way.** Here the guest is told **nothing**: `fd` is silently written 0, so this line is the only record that the emulator met a format it does not model — a deficiency tripwire — and exactly one of them should survive into a `-q` run, where a `VERBOSITY_DEBUG` gate would be invisible. (#276's site is gated precisely because there the guest **is** answered.) `fatal()` is kept because neither function has a `cpu` or `machine` pointer in scope, so `debugmsg_cpu()` is not available — verified in the signatures, which take only `(uint64_t, struct ieee_float_value *, int)` and `(double, int)`.
- **The two latches are PROCESS-GLOBAL file-scope statics, not per-instance like #269's and #277's.** `float_emul.c` is a stateless helper with no struct to hang state on. The cost is that in a multi-machine emulation only the first machine's bad format is reported. That is a deliberate deviation, stated in the source comment and here rather than left to be discovered. One flag per **distinct message** and never one shared flag: a shared flag would let whichever message fires first mask the other for good.
- **Recorded, NOT fixed — the upstream routing candidate (next-round, scoped).** A reviewer argued the real defect is that an R4000 is MIPS III while PS is MIPS-V/MIPS64, so `cpu_mips_instr.c:4995` admitting `COP1_FMT_PS` to `cop1_slow` is the bug and `fd = 0` is a correctness bug wearing a hygiene bug's clothes; the architecturally correct outcome is a **Reserved Instruction** exception. That is a semantic change to arch-shared instruction routing, needs its own panel and its own test-first reproduction, and is deliberately not folded into an output-only commit. **The open question it depends on is partly answered here:** the tree *does* emulate `isa_level == 64` CPUs with FPUs — `5Kc`, `5KE`, `SB1`, `SR7100` in `mips_cpu_types.h` — so the routing cannot simply be deleted; the fix has two halves, an ISA gate (RI below MIPS-V) *and* the fact that `float_emul.c` models no PS arithmetic at all. Same family as the pre-existing `trunc.l` observation recorded under **#273**: the COP1 decoder does not enforce ISA level.
Verified: clean rebuild **0/0** both trees (223 pmax / 224 arc objects); **pmax + arc both boot to `uid=0(root)`**; `float_emul.c` byte-identical in all four tree copies and the divergence set still exactly the five known files. **Probe: 22/22 checks with the latches engaged (11 per CPU) and 20/20 on the forced-off build (10 per CPU).** With the latches engaged, 12 `add.ps` plus 6 `abs.ps` produce **1 interpret line and 1 store line in total** — per-iteration `100000000000` for each message, counted with its own substring and never by subtraction — against 8.0 lines *per instruction* before. Both being 1 in one session is the independence cross-check: interpret latches first, so a single shared flag would have made store 0. Liveness is asserted on evidence **other** than the latched messages: `fd` is re-armed with a sentinel before every step and read back with a genuine guest `swc1`+`lw`, giving **12/12** and **6/6** writes of `0x00000000` — unchanged guest-visible behaviour — with the emulator still answering the debugger at the end. A legal-format positive control (`cvt.w.d`, run before any latch can fire) prints **0** lines and returns the correct **`0x00000001`**. **Blast-radius gate, because this file is arch-shared:** 15 non-MIPS machines covering all four calling families plus `dev_pvr` — alpha (`alphabook1`, `alphaserver4100`), m88k, ppc (incl. `macppc/g4`), sh (incl. `hpcsh/jornada680`, `dreamcast`), arm and riscv — produce output **byte-identical** to the pre-change binary, **15/15 on both trees**, 12 of them reaching the debugger prompt (the three that do not — `pmppc`, `mvme1600`, `dreamcast` — fail identically on the pre-change binary). **On a healthy boot this site is latent:** the pre-#279 boot logs, produced by a binary whose `fatal()` cluster was still ungated, contain **0** occurrences of `unimplemented format` — so this is hardening against a guest-repeatable flood, not the removal of noise the harness was living with.
---

## Forty-seventh round (#280) — `dev_fdc.c`: one host line per guest access to an unmodelled register
`devices/dev_fdc.c` is **not** one of the five divergent files, so both trees stay byte-identical. The file describes itself as "just a dummy skeleton", and it is: `DEV_FDC_LENGTH` is 6 and **0x04 — the PC floppy Main Status Register — is the only offset the `switch` handles**. Offsets 0, 1, 2, 3 and 5 all fall to `default:`, which printed an ungated `fatal()`.
- **#280** `devices/dev_fdc.c` (both trees): the `default:` arm now goes through `debugmsg(SUBSYS_DEVICE, "fdc", VERBOSITY_DEBUG, …)`, and the write arm's `2+len` `fatal()` calls collapse into **one** `debugmsg` with the bytes pre-formatted into a bounded buffer. **Measured on the committed build first: 1.00 host lines per guest access, reads and writes alike** (10 stores → 10 lines, 10 loads → 10 lines). The `2+len` calls were `2+len` *calls* building exactly **one line** — only the closer carried the `\n` — emitted a character at a time by `va_debug()`; a 1/2/4-byte store produced 1/2/4 byte tokens on that single line, and it still does.
- **Gated like #276, not latched like #277/#279, and the axis is the one this batch settled on: is the guest told?** Here it is. The probe fails through modelled behaviour and OpenBSD draws the right conclusion by itself — `fdc at pica0 slot 2 offset 0x0 not configured`, still printed once in the post-change boot log. **A latch would have been actively wrong at this site:** the two hits on a healthy arc boot are `fdcprobe`'s reset pulse, `write reg 2 = 0x00` then `write reg 2 = 0x04` (`FDO_FRST`), and a one-shot latch would suppress the **second** line — the only interesting thing the site shows.
- **The byte buffer is sized from the register array, never from `len` or `idata`:** `char buf[3 * DEV_FDC_LENGTH + 1]`, no VLA, no heap, and the loop is bounded by `DEV_FDC_LENGTH` as well as by `len` so the `snprintf` cursor cannot walk past the buffer even if `memory_rw.c`'s clamp ever changed. The read arm's payload is **deliberately unchanged** — adding the returned value was proposed and rejected: this is a hygiene gate, and changing the message contract in the same commit that gates it would make the two indistinguishable in a bisect.
- **Offset 0x04 must stay silent, and that is asserted rather than assumed.** `out_fdc()` (OpenBSD `arc/dev/fd.c`) spins ~100,000 times polling the Main Status Register at offset 4 on every arc boot. That offset is quiet today only because it is the one handled case; a refactor that routed it through the new `debugmsg` would emit ~100k lines under `-v -v`. The probe hammers 0x04 both under `-V step` and in a free-running `-v -v` window: **0 lines in both**.
- **Blast radius, stated precisely because it is narrower than it looks:** `BUS_ISA_FDC` is passed by exactly one caller tree-wide, `machines/machine_algor.c:77` (grep-verified). ARC **PICA and MAGNUM** instantiate the device directly at physical `0x80003000` (`machine_arc.c`), and **pmax does not instantiate `fdc` at all** — so a pmax boot proves nothing whatsoever about this gate, and it is not offered as if it did.
Verified: clean rebuild **0/0** both trees (223 pmax / 224 arc objects); **pmax + arc both reach `uid=0(root)`** (15/15 and 13/13 harness steps); `dev_fdc.c` byte-identical in all four tree copies and the divergence set unchanged. **Gate probe, both halves plus the pre-change binary as a third reference point:** under `-V step` (where `debugmsg.c:181` bypasses the verbosity test while `single_step` is set) the site still fires **12/12 reads and 12/12 writes**, and `sb`/`sh`/`sw` each produce **one line with 1/2/4 byte tokens**; free-running at default verbosity it produces **0** lines with the `pc` confirmed still inside the hammer loop, against **802,324** lines in 3.09 s on the pre-change binary and **528,517** in 3.08 s on the same post-change binary run with `-v -v` — the positive control, without which a bare zero would mean nothing. In the boot logs the `[ fdc: … ]` lines go **2 → 0** on arc (0 → 0 on pmax, which has no fdc), while `fdc at pica0 slot 2 … not configured` stays at **1**.
---

## Forty-eighth round (#281, #282) — ASC: a short DATA\_IN transfer reported as if the full count had moved
`devices/dev_asc.c` is **not** one of the five divergent files, so both trees stay byte-identical. This is a **semantic** change on a path every boot traverses, so it is separated from the hygiene commit before it and rests on the guest's own source rather than on plausibility.
- **#281** `devices/dev_asc.c` (both trees): a DATA\_IN DMA transfer whose target returns **fewer** bytes than the guest programmed now leaves `NCRSTAT_TC` **clear** and the residual `programmed − actual` in `NCR_TCL`/`NCR_TCM`. TC is set **iff** the residual is zero. **Measured on the committed build first, identically on arc and pmax: a short transfer was BIT-FOR-BIT INDISTINGUISHABLE from a complete one** — `STAT 0x93` (INT\|TC\|STATUS phase), residual `TCL/TCM = 0x00/0x00`, `INTR 0x18`, `STEP 0x04`, GE and PE clear — in *both* cases. The emulator was claiming the full programmed count had moved when e.g. 7,680 of 8,192 bytes never left the target. The site was already self-inconsistent: `:1058` **clears** `NCRSTAT_TC` when a DMA command loads the count, and this arm set it unconditionally a few hundred lines later.
- **The guest source says the change is safe and makes the driver strictly more correct.** `SCRIPT_MATCH(ir,csr) = ((ir) | (((csr) & 0x67) << 8))` (OpenBSD 2.2 `sys/dev/tc/asc.c:256`, `sys/arch/arc/dev/asc.c:236`) masks TC (0x10) **out**, so clearing TC cannot change driver dispatch. The residual, by contrast, **is** read and acted on: `asc_last_dma_in()` does `ASC_TC_GET(regs,len); len = state->dmalen - len; state->buflen -= len; bcopy(state->dmaBufAddr, state->buf, len)`. Today's lie actively harmed the guest — sized by a zero residual, that `bcopy` copied 1,024 bytes the target never sent straight over the driver's deliberate pre-zero, and `sd_mode_sense()` (`sys/scsi/sd.c:883`) `bzero`s its buffer precisely "so that checks for bogus values of 0 will work in case the mode sense fails".
- **Both bytes are written, and that is not a detail.** `ASC_TC_GET(ptr,val)` is `val = asc_tc_lsb | (asc_tc_msb << 8)` (`arch/pmax/dev/ascreg.h:173`, `arch/arc/dev/ascreg.h:150`) — a 16-bit counter, `TCH` never read, which is why TCH is left alone. On pmax the honest residual is **1024**, whose low byte is **0x00**: a fix that wrote only TCL would leave `0x0000`, indistinguishable from "complete", and a broken fix would have looked correct. Every check in the probe asserts **TCL and TCM and the TC bit**. Masking is likewise load-bearing — `reg_ro[]`/`reg_wo[]` are `uint32_t`, not `unsigned char`, and the DEC-mode read path returns the full 32-bit `odata`, so each byte is masked `& 255` on the way in.
- **The residual comes from the ASC boundary (`programmed − actual`), not from the #263 R4030 callback return.** Honouring that return would re-open the #264 retry-semantics adjudication and would change the guest-visible outcome of exactly the count-mismatch case #263 exists to guard. The seam is recorded as a **deliberately unwired gap**, not an oversight.
- **The dead `memset` is removed, and the history is ours, not inherited.** It zeroed exactly the region the following `memcpy` overwrites, and on arc it targeted `d->dma`, which is not the destination at all. Upstream `39748e3` had `memset(…, 0, lenIn2)` — the **full un-clamped count** — and **our own later hardening clamped it to `lenIn`**, which is what made it dead *and* silently changed the pmax tail from zeros to stale bytes. With an honest residual the driver's `bcopy` no longer reads that tail, which is why zeroing is unnecessary rather than merely redundant.
- **#282** `devices/dev_asc.c` (both trees): `size_t lenIn` / `size_t lenIn2` were passed to `%i` twice with **no cast** — undefined on LP64. Now `(int)` casts, not `%zu`: `%zu` appears **0 times in the entire tree** (grep-verified) and the neighbouring warning at `:454-457` already casts to `(int)`. **The message itself stays ungated this round, on purpose:** once the residual is honest the condition stops being an anomaly and a DEBUG gate becomes the right end state, but demoting the only instrument that shows the new behaviour in the same commit that changes it would leave nothing to observe. Gating it is recorded as the intended follow-up.
- **Out of scope, documented not reproduced:** `:592-598` (DATA\_OUT) and `:839-842` (COMMAND-phase DMA, which sets TC *while* writing back the full count) tell the same lie. Also worth knowing: Gavare `#if 0`'d the TCL/TCM copy-through at `:1027-1030` with the comment "Transfer count lo and middle", i.e. he knew the counter must not mirror the write registers — which is *why* a written residual survives until the next DMA reload.
Verified: clean rebuild **0/0** both trees (223 pmax / 224 arc objects); **pmax + arc both reach `uid=0(root)`**; `dev_asc.c` byte-identical in all four tree copies and the divergence set unchanged. **Probe, on BOTH machines and on BOTH the short and the matched path, asserting both residual bytes and the TC bit every time — 3/3 cases × 2 machines:** short (512 of 8,192) → residual **7,680**, `TCM 0x1e`, `TCL 0x00`, TC **clear**, `STAT 0x83` (was `0x93`); matched (512 of 512) → residual **0**, TC **still set**, `STAT 0x93` — the no-regression half; raw-count-zero (512 of 65,536) → residual **65,024**, `TCM 0xfe`, `TCL 0x00`, TC clear. **The gating guest observation is pmax READ CAPACITY, not INQUIRY:** `rz.c:311` is `if (biowait(&sc->sc_buf) || sc->sc_buf.b_resid != 0) return (0);` and `sc_blks` — hence the `rz1: 300MB, 614880 512 byte blocks` line at `rz.c:423` — is set **only** past that test, so the line's presence *is* the observation that `b_resid` was exactly 0. It is present and unchanged (`sc_capbuf[8]`, 8 programmed, 8 returned). INQUIRY has ~1,063 bytes of slack and would have absorbed an arithmetic error invisibly, the same "a false fault here is silent" shape as #267, so it is **not** the gate — though it corroborates: `rz1 at asc0 drive 1 slave 0 <DEC RZ58     (C) DEC rev 2000>` still takes the `i >= 36` branch with the true `i = 44` instead of the fictitious 1,068. Guest-visible SCSI/disk lines are **identical to a pre-change boot** on both machines (arc `sd0: 1024MB, 2081 cyl, 16 head, 63 sec, 512 bytes/sec, 2097648 sec total`, `root on sd0a`, filesystem marked clean); live LANCE ping **3/3 received, 0% loss**; the `{ asc: data in … }` count is **unchanged at 1 pmax / 5 arc** since the message stays ungated, and panics/aborts remain 0.
---

## Forty-ninth round (#283, #284, #285) — ASC: a short DATA\_OUT that committed bytes the guest never supplied
Three corrections. #283 and #284 close the two sites round 48 recorded as "out of scope, documented not reproduced"; #285 is a different layer with a different affected machine set, which is why it is a separate commit with its own no-regression evidence. `devices/dev_asc.c` and `disk/diskimage_scsicmd.c` are both **non-divergent**, so both trees stay byte-identical.
- **#283** `devices/dev_asc.c` (both trees): the DATA\_OUT DMA arm now **honours the byte count the external DMA controller returns**, at **both** call sites, and fails the transfer on **any** short move — honest residual in `NCR_TCL`/`NCR_TCM`, `NCRSTAT_TC` left **clear**, a new diagnostic, and `return 0` **before** `diskimage_scsicommand()`. **Measured on the committed build first, on arc:** `dev_jazz_dma_controller()` returns the actual count (added by #263), `dev_asc.c` discarded it and advanced `data_out_offset` by the **requested** `len2`; with an R4030 count of 128 and an ASC count of 512, the disk gate at `diskimage_scsicmd.c:778` (`data_out_offset != size`) **passed** and **512 bytes were committed, 384 of which the guest never supplied** — read back off the image as 128 × 0x33 followed by 384 × 0x00. The register state was no help: short (512 of 8,192) and matched (512 of 512) were **bit-for-bit indistinguishable** — `STAT 0x93`, TC set, `TCL/TCM 0x00/0x00`, `STEP 0x04`, `INTR 0x18`.
- **#263's `clearflag = 1` is currently the only thing keeping this to destruction rather than disclosure.** With `clearflag` reverted to 0 the same case wrote 384 bytes of the **previous command's heap buffer** to the disk image. After #283 that zeroing becomes defence in depth rather than the sole mitigation.
- **Abort on ANY short, not only on a zero return, and that is a measurement not a preference.** Fault injection on OpenBSD 2.2/arc: no remedy at all → `panic: asc_intr` on the **first** hit, for a zero return **and** for a positive partial; a remedy that fires only when the actual count is zero → survives the zero return but **panics** on the positive partial, because the remedy never fires; abort on any short → **survives both**. The "let the guest recover from an honest residual" theory is refuted by the panic line itself: `asc_intr: data overrun: buflen 8192 dmalen 8192 tc 8192 fifo 0` shows the guest read the honest residual and panicked anyway.
- **The disconnect is a deliberate ROBUSTNESS APPROXIMATION and is documented as one, in the code and here.** A real 53C94 does not synthesize a disconnect; it stalls waiting for a DREQ that never comes, and the measurement shows stalling panics the guest. An instantaneous emulator cannot express an indefinite bus stall, so `NCRINTR_DIS` is used as the nearest guest-handleable terminal state. **This is not hardware fidelity.** The faithful path is the R4030 `DMA_INT_SRC` translation-fault interrupt, recorded as a known gap since #267.
- **#284** `devices/dev_asc.c` (both trees): the COMMAND-phase DMA arm of `dev_asc_select()` stores a literal **0** in the transfer counter instead of the full count; TC stays set. The copy loop is infallible and exits at `i == len`, so the honest residual is provably zero, yet the counter was loaded with the whole count **while Terminal Count was asserted** — "nothing moved" and "the transfer completed" at once. **Measured:** count 6 → `TCL 0x06`; count 262 → `TCL 0x06 TCM 0x01`; both with `TC = 1`. **Conformance, not a guest-visible bug** — the next DMA command reloads the counter before any data phase reads it — but **not latent**: OpenBSD/pmax reaches this **1,659 times per boot**, once per SCSI command (arc preloads the CDB into the FIFO and reaches it 0 times).
- **#285** `disk/diskimage_scsicmd.c` (both trees): the MODE SELECT gate asks for the 12-byte parameter list and accepts it only when all 12 bytes have arrived, in the **set-then-compare** form. **Measured hole:** MODE SELECT(6) with 11 of 12 bytes transferred passed the old `data_out_offset == 0` gate, and `logical_block_size` was committed as **4096** where the guest's list said **4097** — computed from byte 11, which was never sent, and confirmed guest-side by a READ CAPACITY(10) reading 4096 back. #205's guard does not catch it because `data_out_len` **is** 12 on re-entry. This was the only `data_out` gate in the file that was not `!= size`.
- **The order of the two statements is load-bearing, and the naive form would have shipped a regression.** `data_out_len = 12` is assigned **inside** the old block, so on first entry it is 0; testing `data_out_offset != data_out_len` **before** setting it compares 0 against 0, never asks for the buffer, falls through to #205 with `data_out == NULL`, returns GOOD status, and turns every MODE SELECT into a silent no-op. The gate that proves the shipped form is right is therefore **not** "the partial no longer commits" but "**a complete one still does**".
Verified: clean rebuild **0/0** both trees (223 pmax / 224 arc objects); pmax **15/15** and arc **13/13** to `uid=0(root)`; both files one md5 across all four tree copies and the divergence set unchanged at five. **#283, on the arc rig:** the corrupting case now leaves the disk block **byte-identical to before the transfer** (was 128 supplied + 384 never supplied), `TCL 0x80` / `TCM 0x01` = residual **384**, TC **clear**, `STAT 0x80`, `INTR 0x38` (DIS set), one diagnostic line; the matched and over-programmed controls are **unchanged** (`STAT 0x93`, TC set, residual 0, all 512 persisted bytes guest-supplied). **On the guest, both fault shapes now survive** — zero return and positive partial alike: 0 panics, 0 `data overrun`, `asc0: SCSI device 0: unexpected disconnect`, and the shell still responsive afterwards. **No-regression, all four observations the panel asked for:** the new diagnostic fires **0** times on all six healthy boot logs; an instrumented count shows `moved == requested` on **145/145** pmax and **209/209** arc DATA\_OUT transfers, with a positive control (the deliberately short case scores 1) proving the counter is not dead code; the pmax boot's changed-block set against the golden master is **identical** across two pre-change boots and the post-change boot (125 blocks); and the pmax boot transcript is **identical** (101 distinct lines, 116 total) across all three. **#284:** the counter reads **0 with TC set** on both machines (was 6 and 262); over a healthy pmax boot the site fires **1,659** times and **0 of 4,136** guest reads of `TCL`/`TCM` could observe the changed value, against a positive control that scores 4. **#285:** the 11-of-12 partial no longer commits 4096 (block size stays **512**), and a **normal** MODE SELECT still works end to end — 12 of 12 bytes supplied commits **2048** for the NetBSD parameter list and **4097** for the list whose partial form used to fabricate 4096, both read back with a real READ CAPACITY(10); 20-machine, six-architecture smoke **byte-identical 20/20** against the pre-change binary on both trees. Log hygiene: **0** panics on either rig, `{ asc: data in … }` unchanged at **1 pmax / 5 arc**.
---


## Fiftieth round (#286) — ASC: a short DATA\_IN reported as complete, and the last discarded DMA return

One correction, closing the gap round 49 recorded against its own work: #281 made the DATA\_IN
residual honest with respect to the ASC's clamps, but still computed it from the count
**requested** rather than the count that **moved**, so the arc path stayed dishonest under a
short R4030 transfer. `devices/dev_asc.c` is **non-divergent**, so both trees stay byte-identical.

- **#286 (`devices/dev_asc.c`, SCSI/DMA, Medium — latent):** the `PHASE_DATA_IN` DMA branch
  discarded `d->dma_controller()`'s return. `dev_jazz_dma_controller()` has reported the count it
  actually moved since our own #263, and it can fall short four ways — the R4030 byte count can be
  smaller than the ASC asked for (it is also cleared after every call), #267's translation-limit
  `break` stops the table walk, #268 masks the count to 20 bits, and a wrong direction returns 0
  outright. The residual was then computed as `programmed - lenIn2`, so whenever
  `programmed == lenIn2` it read as **0 with `NCRSTAT_TC` set**: a short DATA\_IN was bit-for-bit
  indistinguishable from a complete one, and the undelivered tail of the guest's buffer kept
  whatever it held before. The multitransfer block below it compounded this by advancing
  `data_in` by `lenIn2` regardless. Fixed by capturing the return, and on
  `lenIn2 > 0 && moved < lenIn2` writing the honest residual `programmed - moved` to TCL **and**
  TCM with TC left clear, emitting one `fatal()` witness, and returning 0 **before** the
  multitransfer block — the `NCRCMD_TRANS`/`NCRCMD_TRPAD` caller converts that into
  `STATE_DISCONNECTED` + `NCRINTR_DIS | NCRSTAT_INT`, writing only INTR/STAT/STEP so the counter
  survives. This is the #283 shape, deliberately, and it is now the last discarded
  `dma_controller` return in the file.

### What was measured, and what it does not claim

**The defect reproduces on the committed logic.** With the R4030 forced short, the witness read
`programmed=2048 lenIn2=2048 moved=256 → TCL=00 TCM=00 residual=0 TC=SET`: 256 bytes delivered,
"all 2048 complete" reported. Three such transfers, all reported with TC set.

**It is LATENT on the reference guest and this round is not credited with a hygiene win.** A
control boot logged **2282** DATA\_IN transfers with **zero** shorts. OpenBSD 2.2/arc derives the
R4030 count and the ASC counter from the same `len` (`asc_dma_in()` → `DMA_START` +
`ASC_TC_PUT`), so none of our clamps can bite by construction. Same standing as #283 (0 of
145/209).

**The counter is genuinely consumed by the guest, which is why the honest value matters.**
`ASC_TC_GET` (`arch/arc/dev/ascreg.h:149`) reads exactly the TCL/TCM pair written here, and it
appears at six sites in `arch/arc/dev/asc.c`; `asc_last_dma_in()` derives `buflen` and
`xs->resid` from it. Note this does **not** contradict the round-47/49 record that `ASC_CSR_TC`
is referenced nowhere in `arch/arc` — that is the status **bit**, which is masked out of
`SCRIPT_MATCH` by `0x67`. The bit is ignored; the counter is not. Do not generalise the former
into the latter.

**The terminal state was chosen by fault injection, not by panel vote.** Of the five seats, the
four available at design time split 3–1; both the dissenting seat and one supporting seat
independently required the measurement first. (Codex answered only on a third attempt, after two
`at capacity` failures, and concurred with the shipped design; its accepted criticism was that
the first form of the in-code comment was too long for the charter, which is why the shipped one
is about half of it.)
Three designs were compiled into one binary and selected at runtime, with a single-shot short
injected on the Nth to-memory callback:

| design | outcome on OpenBSD 2.2/arc |
|---|---|
| discard the return (HEAD) | boot completes, nothing reported — the silent defect |
| honest residual, terminate the transfer normally | **guest panics** |
| honest residual, abort → synthesized DISCONNECT (**shipped**) | no panic; transfer abandoned |

The "terminate normally" design was argued from the observation that the benign clamp path
already produces a TC-clear nonzero residual safely on every healthy boot. That reasoning did not
survive contact: truncating mid-DMA leaves the guest's script state machine disagreeing with the
controller, and it panics.

**Verified.** Clean rebuild **0 warnings / 0 errors** both trees (223 pmax / 224 arc objects);
pmax **15/15** and arc **13/13** to `uid=0(root)`; `dev_asc.c` one md5 across all four tree copies
and the divergence set unchanged at five. The new `short DATA_IN DMA` witness fires **0** times on
both healthy boot logs, against a positive control (an injected short scores 1) proving the grep
is not dead. Log hygiene otherwise unchanged: 0 panics on either rig, and the pre-existing
`{ asc: data in … }` control still reads **1 pmax / 5 arc**.

**A measurement trap this round paid for, recorded so it is not repeated.** Emulator `fatal()`
output is **not** guest console output — it goes to stdout and interleaves into the pty stream, so
counting it from the reconstructed 80×25 arc screen loses it. `{ asc: data in }` reads **0** from
the screen rebuild and **5** from the raw arc pty log. Grade guest tokens from the reconstruction
(the VGA console repaints differentially); grade emulator diagnostics from the raw log.

**Honest limitation, recorded rather than glossed.** The shipped design does not let the guest
*recover* the transfer — it abandons it. The guest answers the synthesized disconnect with
`ASC_CMD_ENABLE_SEL`, and `NCRCMD_ENSEL` (`dev_asc.c:1221-1225`) is an unimplemented no-op, so
nothing ever reselects. A real 53C94 would stall awaiting a DREQ rather than disconnect at all,
so this remains a deliberate **robustness approximation, not fidelity** — the same disclaimer
#283 ships. The faithful path is the R4030 `DMA_INT_SRC` fault interrupt, a known gap since #267.
What the correction buys is that a fault our own guards detect can no longer be reported to the
guest as success.

---


## Fifty-first round (#287) — S-format overflow stored a NaN encoding where hardware gives ±Inf

One correction to `core/float_emul.c`'s `ieee_store_float_value()`, the arch-shared IEEE store
helper. `float_emul.c` is **non-divergent**, so both trees stay byte-identical.

- **#287 (`core/float_emul.c`, FPU, Medium):** the `FP_NORMAL` arm assembles the fraction bits and
  *then* forces the biased exponent to all-ones on overflow **without clearing that fraction** —
  and exponent-max with a nonzero fraction is a **NaN**, mostly a *signaling* one. The
  `FP_INFINITE` arm holds the right answer and is never reached, because the *double* is finite;
  it is the single-precision destination that overflows. Separately, the line labelled "Special
  case for 0.0" (`if (exponent == 0) r = 0;`) is never reached by 0.0 at all — `FP_ZERO` has its
  own arm — so it is purely an underflow flush, and it **discarded the sign bit** set at the top
  of the arm. Fixed by testing the biased exponent for all-ones and keeping only the sign before
  OR-ing the exponent in, and by flushing underflow to a *signed* zero.

### Measured, live in the emulator — not re-derived

Every previous record of this defect was a replay of the function's arithmetic on host doubles.
This round ran it through genuine guest `cvt.s.d` instructions on the committed binaries
(`_scratchpad/r50_probe.py`, on the validated `gxprobe` harness; the double is loaded as the
`$f0/$f1` pair with two MIPS-I `lwc1`s, since LDC1 is MIPS-II and traps on R3000).

| case | PRE | POST | hardware |
|---|---|---|---|
| `1e300` | `0x7fbf21e4` (NaN) | `0x7f800000` | `0x7f800000` |
| `-1e300` | `0xffbf21e4` (NaN) | `0xff800000` | `0xff800000` |
| **`3.5e38`** | **`0x7f83a7c6`** (NaN) | `0x7f800000` | `0x7f800000` |
| `1e40` | `0x7feb194f` (NaN) | `0x7f800000` | `0x7f800000` |
| `-1e-40` (pmax) | `0x00000000` | `0x80000000` | *(see below)* |
| `3.4e38` control | `0x7f7fc99e` | `0x7f7fc99e` | unmoved |
| `1.0` / `-2.5` / `0.0` controls | — | unchanged | unmoved |

**THE BRIEF THAT OPENED THIS ROUND PROPOSED A HALF-FIX, AND THE PANEL CAUGHT IT.** It asserted
(as does `OUTSTANDING_BUGS.md` item 8, in the same words) that "the clamp first fires at
|x| ≥ 2^128" and framed the fix as clearing the fraction *where the clamp fires*. The clamp tests
`>= (1 << n_exp)` = 256 and therefore first fires at **2^129**. For `|x|` in `[2^128, 2^129)` the
biased exponent reaches **255 with no clamp at all**. Four of five seats caught this
independently — 9,740 survivors over a 20M sweep, 20,000/20,000 in that octave, and
`4e38 → 0x7f967699` — and the live probe confirmed three such rows NaN-encoded with exponent 255.
**The test is therefore on the biased exponent, not on the clamp**, and `3.5e38` is a mandatory
acceptance case: a clamp-scoped fix passes on `1e300` and fails there.

### Blast radius: an offline differential, because the usual smoke is vacuous here

The #279 20-machine six-architecture smoke boots a zero blob under `-V` and quits **without
executing a single FP store**, so it would pass identically whether this fix were right, wrong or
absent. The function is pure, so the gate is an offline differential of old against new with a
**closed form for the change-set** — a regression being, by definition, any difference outside it:

```
old(x) != new(x)  =>  (finite && |x| >= 2^128) || (0 < |x| < 2^-126 && signbit(x))
```

Result over 20,016,002 samples (structured sweeps across both boundaries plus random
bit-patterns): 13,133,666 S differences, partitioning **exactly** into 8,756,599 overflow and
4,377,067 negative-underflow; **0 unexplained, 0 in-range S differences, 0 D-format differences**.
The empty D change-set is the *proof* that **alpha is untouched** (it stores only `IEEE_FMT_D`), and
that every D store on m88k, ppc and sh is unchanged. Real exposure is S stores on m88k, ppc
(`stfs`/`stfsx` only) and sh — four families, not the five the brief claimed.

### Why the fraction rounding was NOT also fixed

Routing the S store through a host `(float)` cast would have collapsed this defect together with
the 1-ulp truncation and the underflow sign loss, and was proposed. It was rejected because the
four S-storing families **do not share a rounding mode**: `cpu_sh.c:116` sets
`fpscr = 0x00040001` and `cpu_sh.h:199` defines `SH_FPSCR_RM_ZERO 0x1`, so **SH-4 resets to
round-to-zero** and truncation is architecturally *correct* there by default — a host
round-to-nearest cast would regress it across 16 store sites, on a measured 41% of its S stores.
PowerPC's `stfs` truncates by architecture too. The shared helper carries no rounding-mode
parameter, and adding one is the abstraction the charter forbids. The #254 precedent cuts the
other way: #254 was **MIPS-local**, inside `cpu_mips_coproc.c`. Rounding therefore stays as a
documented gap for a future `FCSR.RM`-aware change, which also owns the residual sliver
`[2^128 − 2^103, 2^128)` where round-to-nearest hardware gives Inf and this code still gives
FLT_MAX.

### The one intended difference, and one anomaly that was chased down

`-1e-40` now stores `0x80000000` (−0.0) where a generic IEEE cast gives the subnormal
`0x800116c2`. That is deliberate: gradual-underflow *generation* is per-family control-register
policy (MIPS `FCSR.FS`, SH-4 `FPSCR.DN`, both defaulting to flush) that a shared helper cannot
see. The probe carries this as a **named intended difference with its justification**, rather than
having its expected value edited to match the new output.

The first POST run showed `-1e-40 → 0xff800000` on **arc** against `0x80000000` on pmax. Since the
fix cannot produce −Inf there (the biased exponent clamps to 0, so the all-ones test cannot fire),
it was checked with a seeded protocol: put a known value in `$f2`, then run the case. arc returned
**the seed unchanged, with two `exception FPE … cause=0x1000003c` lines** — the instruction trapped
via #246's guard and never wrote `$f2`, so `fp_op`'s unconditional `swc1 $f2` stored the *previous*
case's value. A stale read, not a regression. **D3 is observable on pmax only**; arc's identical
input is a control proving #246 still gates that path.

### Reachability — better than latent, and verified from guest source

Four seats called this latent. One found a **stock-userland route, confirmed against the OpenBSD
2.2 sources on disk**: `lib/libc/stdio/vfscanf.c:651` does `*va_arg(ap, float *) = res;`, so a
plain `%f` narrows the parsed double to `float` — `cvt.s.d` on MIPS — and stock
`gnu/usr.bin/texinfo/makeinfo/multi.c` declares `float columnfrac;` (`:152`) and feeds
user-controlled `@columnfractions` text straight into `sscanf (params, "%f", &columnfrac)`
(`:177`). A `.texi` file containing `1e300` therefore reaches this defect through a stock binary,
with no hand assembly and no in-guest compiler. The honest classification is **reachable from
stock userland on crafted input, not exercised by the boot workload** — which is a stronger claim
than #283/#286's latency and a weaker one than boot-visible.

Verified: clean rebuild **0 warnings / 0 errors** both trees (223 pmax / 224 arc objects); pmax
**15/15** and arc **13/13** to `uid=0(root)`; `float_emul.c` one md5 across all four tree copies;
divergence set unchanged at five. Log hygiene unchanged, including the pre-existing
`{ asc: data in }` at 1 pmax / 5 arc.

---


## Fifty-second round (#288) — the arc keyboard queue discarded itself, and its drain loop starved the guest

One correction to `devices/dev_pckbc.c`, in two parts. `dev_pckbc.c` is **non-divergent**, so
both trees stay byte-identical.

- **#288 (`devices/dev_pckbc.c`, console input, Medium):** `pckbc_add_code()` advanced `head`
  and only *then* tested for collision, so an overrun left `head == tail` — the state every
  reader (`pckbc_get_code()`, the status DIB bit, the interrupt assert) treats as **EMPTY**.
  One overrun therefore discarded the **entire queue**, not the single code that did not fit.
  Fixed by computing the next head first and dropping the **incoming** code when the ring is
  full, warning once per port. Separately and more seriously, `DEVICE_TICK(pckbc)`'s drain loop
  had **no space guard at all** — unlike `lk201_tick()` (`lk201.c:253`) and `dev_luna88k.c`
  (`:371`, `:380`) — and because `console_charavail()` refills the console FIFO from the host
  *inside* that loop, an unbounded producer kept it true indefinitely and the tick never
  returned to the guest. Fixed with a room guard whose reserve exceeds the longest scancode
  sequence, so an admitted character always fits whole and a make cannot be queued with its
  break dropped.

### Measured, on the committed build and after

**The queue discard, reproduced.** A 44 KB paste (44,257 chars ≈ 132,771 scancodes against a
32,767-slot ring) into the arc rig:

| | PRE (committed) | POST (#288) |
|---|---|---|
| `pckbc: queue overrun` | **4** | 0 |
| first line delivered to the guest | `L1680` | **`R51FIRST`** |
| lines delivered of 1702 sent | 21 | 39 |

`R51FIRST` — a marker placed at the head of the flood **before** the run — is the
discriminator. A one-byte-drop implementation delivers it and loses something later; a
whole-queue wipe loses it, because at the wrap everything already queued becomes unreachable.
It was absent before and is present after.

An independent cross-check: the *old* code warns once per lap, so the warning count measures
the amplification. 132,771 codes / 32,767 slots = 4.05 laps, and exactly **4** warnings were
observed — two unrelated instruments agreeing.

**The starvation, with pmax as the control.** Under an unbounded producer:

| rig | control | unbounded producer |
|---|---|---|
| arc, before | 4 `OpenBSD` lines | **0 lines**, 10,806 overruns |
| arc, after | 4 lines | **4 lines**, **0 overruns** |
| pmax (already guarded) | 1 line | 1 line, 0 overruns |

Same host, same console layer, identical stimulus: the arc guest never reached its banner,
while pmax — whose drain loop has exactly this guard — was unaffected. That A/B is what
identifies the missing guard as the cause rather than anything else in the console path.

### What is NOT claimed

**The ring half has not been observed firing.** With the drain guard in place, back pressure
stops the queue filling, so `pckbc_add_code()`'s drop-and-latch path is never reached — which
is why the post-fix flood shows 0 overruns rather than 1. Both measurements above therefore
prove the **drain guard**. The ring change is retained as the correctness invariant
(`head == tail` must never mean "full") and as defence in depth for producers that bypass the
guarded tick — the guest-authored controller-response paths — not because it was measured.

The gap between 39 delivered lines and 1702 sent is the guest's own tty layer (`TTYHOG` ≈ 1024)
discarding the middle of the stream under flood. That was flagged as a confound in advance,
and is precisely why the grading rests on the first-marker asymmetry rather than on line counts.

### A behaviour change this fix introduces

**The arc console's stdin is now genuinely flow-controlled, and a harness that writes a large
blob inline while draining the same pty will DEADLOCK** — the writer blocks waiting for the
emulator to consume, the emulator blocks writing output because nobody is reading. This is
correct back pressure and is exactly what pmax has always done, but it broke this project's own
flood test, which had to be restructured to write from a background thread. Before the fix the
unbounded drain swallowed the whole blob instantly, so an inline write appeared to work; that
appearance *was* the defect. (Also run such probes with `python3 -u`: the first post-fix attempt
block-buffered into a pipe and `timeout` discarded every line, yielding a silent empty result
that looked like a crash.)

### Documented, not fixed — with the experiments that would reopen them

Three sites share the same advance-then-warn shape and are **not** changed, because none could
be reproduced and the charter forbids changing what cannot be tested:

* **`console/console.c:304`** — the stdin producer is bounded by the throttle at `:364`, and the
  `+1` in `room < sizeof(ch) + 1` is load-bearing (room 101 → read 100 → occupancy 4095, one
  slot short). Measured **0** overruns even under the flood that wrapped pckbc four times, and
  under an unbounded producer. Two seats nevertheless identified producers that bypass the
  throttle: the debugger's CTRL-K inserts **72** characters, not one, and `dev_ns16550.c:163`
  feeds every transmit byte straight to `console_makeavail()` when `MCR_LOOPBACK` is set, which
  is **guest-authored**. The named experiment that would reopen this file: on arc, drive
  `com_mcr` loopback from the guest and issue several thousand transmit writes into a handle
  nothing drains, then grep for `console fifo overrun`. **Until that is run, this arch-shared
  file must not be touched.**
* **`devices/dev_dc7085.c:103`** — unreachable, and the reference implementation. `lk201_tick()`
  re-tests `space_available_in_queue()` **every iteration** and `dev_dc7085.c:80` reserves 20
  entries, so occupancy parks at ~1004 of 1023. Measured 0 under both stimuli.
* **`devices/dev_scc.c:140`** — same shape, 1 char/tick feed, on machines that are not tested rigs.

Verified: clean rebuild **0 warnings / 0 errors** both trees (223 pmax / 224 arc objects); pmax
**15/15** and arc **13/13** to `uid=0(root)`; `dev_pckbc.c` one md5 across all four tree copies;
divergence set unchanged at five; log hygiene unchanged.

---


## Fifty-third round — R4030 DMA delivery accounting: assessed, NOT changed

Round 50 (#286) made `dev_asc.c`'s DATA_IN path trust `dev_jazz_dma_controller()`'s return to
decide whether a transfer was short, and its commit recorded a follow-on concern: the copy loop
discards **both** `cpu->memory_rw()` return values (`dev_jazz.c:228` PTE fetch, `:258` the copy)
while `i += ncpy` counts the bytes as moved regardless, so the count is "not proof of delivery".
This round audited that and **deliberately changes nothing.** The proposed correction would have
been dead code, and the reasoning is recorded here so it is not proposed a fourth time.

**Both returns are a constant `MEMORY_ACCESS_OK` for every address a guest can steer the R4030
at.** Both calls pass `PHYSICAL | NO_EXCEPTIONS`, and:

* `cpus/memory_rw.c:84-86` is `if (misc_flags & PHYSICAL || cpu->translate_v2p == NULL) { paddr
  = vaddr; } else { ... }`. The **#244** zero-fill *and* its `return MEMORY_ACCESS_FAILED` are
  both inside that `else`, so `PHYSICAL` bypasses them entirely. #244 can never execute for
  either call — the round-50 note citing it as the mechanism was wrong.
* Every other failure return is gated off by `NO_EXCEPTIONS`: `:423` (device-handler gate),
  `:442` (`res <= 0 && !no_exceptions`), `:515` (`paddr >= physical_max && !no_exceptions`),
  `:537`, `:584`.

The only surviving path to `MEMORY_ACCESS_FAILED` is a `DM_READS_HAVE_NO_SIDE_EFFECTS` device
handler that clears `cpu->running` — on PICA only the VGA unimplemented-mode arm — during which
the emulator is terminating anyway. **Consuming these returns would therefore guard nothing,
detect nothing and change nothing on any constructible input.** Worse than inert: a later round
could build on it believing DMA faults were being checked.

**The underlying phenomenon is real, but it is a silent absorb reported as success, not a failed
access.** Out-of-range reads are zero-filled and return OK — from `:520-522` (beyond
`physical_max`), `:569-573` (NULL memblock; by design, `memory.c:554-564`) or `:330-331` (#95) —
and out-of-range writes are discarded and return OK (`:548-551`).

**Measured by hand from the cold debugger on the committed build**, ASC transfers driven through
the R4030 with only `PTE[0]` varied, both observation pages seeded `0xEE`. Every row below
reported **residual 0, TC SET, and zero short-transfer messages** to the guest:

| run | `PTE[0]` | outcome |
|---|---|---|
| V (control) | `0x00300000` | 512 disk bytes land on the correct page; page 0 untouched |
| Z | `0x00000000` | **512 disk bytes land on guest physical page 0** — the exception vectors |
| X | `0x08000000` (past 64 MB RAM) | nothing lands anywhere; guest told 512/512 complete |
| D | `0x80000000` (device space) | write dropped — `TL_BASE` still reads `0x00200000` |
| E | `0x400a0000` (`vga_gfx`) | emulator survives; transfer reported complete |

And on the DATA_OUT side, against a throwaway image pre-filled `0xAA`:

| run | `PTE[0]` | host disk file before → after |
|---|---|---|
| Wc (control) | valid | `aa…` → `5a 5a 5a 5a …` (the write path itself is sound) |
| **Wh** | `0x08000000` | **`aa…` → `00 00 00 00 …`** |

**Run Wh is the strongest fact in this round:** a source page past installed RAM is zero-filled
and then *committed to the platter*, destroying 512 bytes of real data while the guest is told
the write completed. That is data destruction, not a mis-report — and it is still invisible in
the return value, which is why it does not justify #289.

**Why the two obvious guards are also wrong.** Neither is a smaller version of the right fix:

* **Rejecting `phys_addr < 0x1000`:** `dev_jazz.c:228-230` fetches `sizeof(tr)` = **4 bytes at a
  stride of 8** — the entry's second word is never read, so **the model has no validity bit at
  all**. A zero entry means physical page frame 0, and DMAing there is what the modelled hardware
  does. An absorbed fetch and a guest-written zero entry are indistinguishable *by value*. Such a
  guard would replace a faithful behaviour with an unfaithful one.
* **Bounding against `physical_max`:** DMA into device space is legitimate and works today for
  `DM_READS_HAVE_NO_SIDE_EFFECTS` devices (`vga_gfx` at `0x400a0000`), so a RAM-only bound would
  regress it. A correct detector would have to replicate `memory_rw`'s own dispatch —
  `physical_max` *and* the device window — inside a device model, which is the abstraction the
  charter forbids and which would drift.

**#286 is as much a reason to leave this loop alone as to touch it.** Since #283/#286 convert a
short return into a synthesized guest DISCONNECT, and rounds 47-49 measured mis-handling there as
a guest **panic**, any new early break here is more dangerous than when #267 shipped, not less.
A guard whose true-positive rate on the reference guest is **0 in 255,000** loop iterations has
only false positives available to it — and the ASC discards the controller's return at three
call sites, so a false break would be *silent*, surfacing as filesystem corruption rather than an
error.

**The faithful fix, and the reopen condition.** Both consequences are properly signalled by the
R4030's own address-error / `DMA_INT_SRC` machinery, which this emulator does not model — the
known gap already recorded when #267 added the translation-limit break. What has changed since
is that #283 and #286 have built the downstream guest-visible path (short transfer → honest
residual → synthesized DISCONNECT) and measured it survivable on OpenBSD 2.2/arc, so that round
now has somewhere to deliver its signal. **Reopen when the fault infrastructure is built, not
before.**

**Reachability: latent, and MEASURED rather than argued.** A full instrumented OpenBSD 2.2/arc
boot to `uid=0(root)` with a clean halt, counters on all four hazard conditions:

```
R52PROBE_ARM physmax=0x4000000 devmin=0x400a0000 devmax=0x1c000bc000
R52PROBE_TOT iters=255000 oorpte=0 pte0=0 oordst=0 dev=0      (2000+ controller calls)
```

Zero out-of-range table walks, zero zero-PTEs, zero out-of-range destinations, zero device-space
destinations. The guest builds its translation table from its own free pages and every one is a
real page under 64 MB. Every reproduction above required writing a bogus PTE from the debugger.
Consistent with #267's earlier measurement (`TL_LIMIT = 0x8000` written once, maximum table
offset `0x458`, 0 out-of-bound walks over 2602 transfers). Note the table base and the frame
values are validated against nothing; only the *walk offset* is bounded, by #267.
*Caveat, stated honestly:* that is one boot-to-shell profile — no `fsck`-heavy, swap-heavy or
network-loaded workload. The falsifier is to re-run the same instrumentation under such a load
and show any nonzero counter.

**Cosmetic, recorded so it is not "fixed":** the comment at `:244` says "copying 16 or 256 bytes"
while the code sets `ncpy = 15` / `255`, so the fast path de-aligns itself after one chunk. An
upstream performance quirk, not a correctness bug — and the reason a 512-byte transfer costs
~128 loop iterations.

Panel: five seats, **unanimous DOCUMENT-ONLY**. Three independently identified the #244
mis-citation. One seat drove the reproductions above by hand from the cold debugger and ran the
boot instrumentation, and also supplied the point that the model's 4-of-8-byte entry read means
there is no valid bit to consult — which is what makes any value-based page-0 guard unfaithful
by construction.

---


## Fifty-fourth round (#290) — the COP1 decoder enforced ISA level nowhere

One correction to `cpus/cpu_mips_instr.c`. The file is **non-divergent**, so both trees stay
byte-identical; it is `#include`d into `cpu_mips.o`, so `rm src/cpus/*.o` is required or the
change silently is not built.

> **#289 is VOID** — it was the number reserved for the R4030 DMA return-value check that the
> previous round audited and rejected as dead code, and the round-53 block already refers to it
> by that meaning ("…which is why it does not justify #289"). Reusing it here would leave two
> different things called #289 in a published document, so this correction takes **#290**.
> Same convention as the existing void numbers #247 and #249.

- **#290 (`cpus/cpu_mips_instr.c`, MIPS COP1 decode, Low — latent):** the COP1 format dispatch
  admitted `S`, `D`, `W`, `L` and `PS` on every CPU that has an FPU at all, with **no ISA-level
  test anywhere**. Measured on the committed build: `add.ps` executed on both an R3000A (MIPS I)
  and an R4000 (MIPS III), and `add.l` and `cvt.d.l` executed on the R3000A. Paired single is
  MIPS V; the L format needs a 64-bit FPU, i.e. MIPS III. Fixed by refusing each format below
  its ISA floor with a genuine Reserved Instruction.

### Two things this correction had to avoid, both of which the review caught

**`goto bad` is NOT a guest exception — it is a host-side emulation abort.**
`cpus/cpu_dyntrans.c:1983-2014` says "Abort the emulation", sets `about_to_enter_single_step`,
logs `UNIMPLEMENTED instruction`, and sets **`cpu->running = 0`**. Measured directly:
`add.ps` on the `default:` arm yields `cpu: UNIMPLEMENTED instruction ... emul: All machines
stopped.` with the guest's `cause` ExcCode still 0. The brief that opened this round asserted
that reserved formats "raise Reserved Instruction via `goto bad`", and **three seats
independently caught it**. A fix following that stated precedent would have *halted the
emulator* on `add.ps`. This project has already had to undo exactly that confusion twice, in
**#236** and **#237**. The correct idiom is `instr(reserved)` (`cpu_mips_instr.c:131-140`),
which syncs the PC and calls `mips_cpu_exception(EXCEPTION_RI, …)` — the same idiom the LDC1 /
SDC1 gate at `:5378` already uses, one of eleven `isa_level` gates already in this file.

**`PS` must not join the `x64` fall-through group.** Placed *after* it, `DMFC1`/`DMTC1`/`L`
would fall into the PS predicate and be refused on an R4000 — the catastrophic
restrictive-direction failure. Placed *before* it, legal PS would fall into `x64 = 1`. PS
therefore gets its own arm, duplicating two body lines to be immune to both orderings.

`L` needed no new predicate at all: it joins the existing `x64` label group, because
`is_32bit` is defined in `cpu_mips.c` as `isa_level <= 2 || isa_level == 32` — exactly "no
64-bit FPU" — and the `x64` tail already converts that to `instr(reserved)` with a one-shot
warning. `DMFC1`/`DMTC1` sit in that same arm and were **measured** giving RI on pmax and
nothing on arc, so the outcome was known before a line was written.

### Measured, PRE and POST, on both rigs

Each row is graded on two independent signals: the seed `0xa5a5a5a5` left in `$f2` before the
instruction (a trapped instruction leaves it, since `fp_op` runs its `swc1` regardless — the
stale-register trap paid for two rounds ago), and an exception line in the trace. A row counts
as trapped only when both agree.

| instruction | pmax (R3000A, MIPS I) | arc (R4000, MIPS III) |
|---|---|---|
| `add.ps`, `mul.ps` | executed → **TRAPPED** | executed → **TRAPPED** |
| `add.l`, `cvt.d.l` | executed → **TRAPPED** | **executed → executed** |
| `add.s`, `add.d`, `cvt.w.d`, `cvt.s.d` | executed → executed | executed → executed |

8/8 matching expectation on both rigs. **The arc `L` rows are the restrictive-direction
canaries** — the R4000 keeps its MIPS III right to the L format and loses only paired single.
If the gate were too broad they would have flipped to TRAPPED, and the round would be wrong.

Two refinements to the original description, both from measurement: `add.ps` writes only the
**low half** of the destination pair (`$f2 = 0`, upper single left stale) — "half a result",
not "writes 0"; and the "8 host lines per instruction" figure is **stale**, since #279 latched
both diagnostics and it is now two lines once per process.

### Scope: split, deliberately

Only the two *format* gates ship. `trunc.l` — the other symptom — is a **function**-level
defect: it carries fmt `D`, which MIPS I legitimately has, and its illegality is in the function
field decoded in `cpu_mips_coproc.c`. It is a different layer in a different file, and it
collides with a pre-existing defect found while measuring: an unimplemented COP1 *function*
raises **CoProcessor Unusable** (ExcCode 11, measured `cause = 0x1000002c` on both rigs) from an
**ungated, unlatched per-execution `fatal()`** at `cpu_mips_coproc.c:2365-2369` — the wrong
exception plus the log-flood class fixed in #265/#269/#280. That deserves its own design pass
and is recorded in the backlog rather than tacked on here.

Also left alone deliberately: PS *arithmetic*. `float_emul.c` models none, so on the
`isa_level == 64` parts PS stays admitted-and-unimplemented exactly as before, still recorded by
#279's latch. Implementing it would be a new feature on a shared five-CPU helper with no
reachable consumer.

### Reachability — latent, measured two ways

Static scan of both kernels for forbidden encodings, rejecting all-printable-ASCII words (OpenBSD
links strings into `.text`, and `"VAIL"` matches the COP1 masks): **0** of 293,344 words in
`gxemul_pmax_rig/bsd`, **0** of 543,623 in `gxemul_arc_rig/bsd`. Runtime: full boots to multiuser
on both rigs with **0** occurrences of `unimplemented format` — #279's latch is a perfect PS
tripwire, since PS is the only format that reaches `float_emul` at all — and 0 of
`UNIMPLEMENTED coproc`, `UNIMPLEMENTED instruction`, and the 64-bit-on-32-bit warning.
OpenBSD 2.2's gcc 2.7-era o32 toolchain cannot emit PS, and gas rejects `trunc.l` below `-mips3`.
Credited as latent, like #283/#286/#287.

**A behaviour change that must be named rather than buried:** on 32-bit MIPS machines, `add.l`
and `cvt.d.l` go from computing a plausible value to raising RI. No reference guest is affected
(0 encodings, 0 markers), but a non-reference 32-bit guest that today gets a value from `add.l`
would now take SIGILL. It would be executing an instruction an R3010 does not have, so the new
behaviour is the correct one — but it is a change.

Verified: clean rebuild **0 warnings / 0 errors** both trees (223 pmax / 224 arc objects);
`cpu_mips_instr.c` one md5 across all four tree copies; divergence set unchanged at five.

Panel: four substantive seats (Codex 5.6-SOL ultra, Fable 5, Opus 5, agy 3.6). **Kimi 3 MAX did
not deliver a verdict** — its output matched the completion marker only because it was restating
the required output format while still drafting, the same false-positive that affected a
different seat two rounds ago. A seat that does not answer is not counted as agreement.

---


## Fifty-fifth round — the regression harness itself, and two gates that could not fail

No correction number: nothing under `src/` changes. This round is about the instrument
rather than the patient, and it starts by retiring two gates this project had been
treating as evidence.

### The two vacuous gates

**The 20-machine `-V` smoke.** It booted twenty machines on a zero-filled blob and quit.
Round 51 instrumented it and measured that it executed **zero** floating-point stores —
so it would have passed identically whether #287 was correct, wrong, or absent. It was
reported as a pass in several earlier rounds.

**The 97-alias startup matrix**, added earlier in this same session and retired within it.
With no kernel, every machine prints `No filename. Aborting.`, so the matrix compared
*error strings* across three builds. It produced exactly one genuine signal — `g4plus`,
an MPC7455 subtype this fork added that upstream does not recognise — and could not have
caught a wrong answer anywhere.

Both are replaced by gates that either execute guest code or differentiate a pure function
in closed form.

### A measurement trap that manufactured a finding

The first version of the replacement A/B compared how many bytes each build produced on a
guest boot. It reported that upstream 0.7.0 suffered a capability regression on luna88k:
zero bytes, against 4,793 for the fork.

That was an artifact. When gxemul's stdout is a pipe it is 4 KB block-buffered, and
`timeout`'s SIGTERM discards a partial block — so a guest that produced 3 KB of perfectly
good boot output scores **zero**, while one that produced 5 KB scores 4096. Re-run under
`stdbuf -o0`, upstream produces its full 699-byte banner.

Two rules came out of it, both now enforced in `regress/lib.sh`:

- every emulator invocation goes through `run_emu()`, which forces `stdbuf -o0 -e0`;
- comparison is on **semantic markers**, never byte counts. Under a wall-clock timeout a
  byte count measures how fast the host happened to be. The luna88k A/B makes the point
  directly: HEAD and pre-batch differ by 47 bytes and are *identical* on every marker.

A third rule came from the same run: a missing binary must hard-fail (`need_exec`), never
score zero, because a wrong path is otherwise indistinguishable from total failure.

### Upstream 0.7.0 does not boot OpenBSD/luna88k

Measured unbuffered over 300 s: upstream emits its 699-byte banner and no guest output at
all, while both fork builds reach a `login:` prompt. `gate_ab.sh` asserts that as the
**expected** baseline rather than flagging it.

The obvious explanation was tested and **refuted**. The hypothesis was that the fork's
m88k signed-shift and shift-by-32 UB corrections (#36–40, #46) mattered because a modern
GCC exploits that undefined behaviour. Rebuilding pristine `39748e3` with
`-O2 -fwrapv -fno-strict-overflow -fno-strict-aliasing` compiles clean (223 objects) and
still produces nothing but the banner. Whatever fixed luna88k is a real source change
inside the first hardening commit; narrowing it further would need that commit split.

### New coverage: the first non-MIPS rig that checks an answer

`core/float_emul.c` is called by the alpha, m88k, mips, ppc and sh cores plus `dev_pvr`,
but until now only MIPS had ever executed it under test — which is precisely why #287, a
change to the *shared* S-format arm, had no non-MIPS evidence behind it.

**OpenBSD 7.7 / luna88k (M88100)** closes that. `cpus/cpu_m88k_instr.c` stores
`IEEE_FMT_S`, the exact arm #287 changed. The rig drives the guest to a root shell and
checks a **computed value**, not merely that the guest survived:

```
awk 'BEGIN{printf "%.6f %.6f", 1.5/3.0, 2.0**0.5}'   ->   0.500000 1.414214
```

**OpenBSD 7.6 / landisk (SH4)** boots the SH4 core through a full kernel device probe and
checks a value the guest itself prints — `shpcic0 at mainbus0: HITACHI SH7751R`. It sends
**no** guest input, and that turned into a finding of its own.

### A new bug candidate, found by trying to build a rig on it

The SuperH console **loses guest input non-deterministically**. Commands vanish whole: no
terminal echo, no output, no error, while the shell stays alive and a command sent moments
later runs correctly. Three explanations were tested and refuted before it was recorded as
a bug rather than worked around:

- *timing* — a settle delay before each write, and raising the post-write wait from 8 s to
  25 s, changed nothing;
- *line terminator* — moving from `\r` to `\n` (what the pmax and arc rigs have always
  used) improved it but did not fix it;
- *input length* — one boot, ten `echo` commands of increasing length: the **15, 23 and
  33** byte lines ran, the **9, 17, 27 and 41** byte ones were lost. Neither a length
  ceiling nor a strict alternation; roughly one write in three survives.

Retrying up to six times per command still could not land `$((6*7))` or `uname -m`
reliably. Since `BOOT_REACHED` is 1 on every run, the rig asserts the boot and drops the
interactive steps — an intermittent gate is worse than a narrow one, because it gets
ignored and then switched off. `OUTSTANDING_BUGS.md` carries the measurements and points
at `dev_scif.c` and the console host-glue, where rounds 26/27 (#251/#252) already found two
real defects.

Independently of that, no in-guest FP test is possible on this media anyway: the install
ramdisk was probed and has no `awk`, `perl`, `bc`, `dc` or `python`, so SH4's FP store path
remains unproven and the coverage table says so.

### The strongest gate is offline

`ieee_store_float_value()` is pure, so it is differentialled old-against-new over
**20,016,002** inputs in about twenty seconds. The gate does not ask "did anything
change" — it asserts a closed form for the change-set:

```
old(x) != new(x)  =>  (finite && |x| >= 2^128)          // S overflow
                  ||  (0 < |x| < 2^-126 && signbit(x))  // S negative underflow
```

with an **empty** change-set required for `IEEE_FMT_D`. A regression is by definition a
difference outside that set. Measured: 13,133,666 S-format differences, all classified
(8,756,599 overflow, 4,377,067 negative underflow), **0 unexplained**, **0** in-range
values moved, **0** D-format differences.

It also pins two thresholds that sit close together and were conflated in an earlier draft
of `regress/README.md`. They are not the same number, and the gate now determines both
empirically rather than trusting the prose:

- the stored exponent reaches 255 at **2^128** (bias 127, so `e + 127 >= 255`), which is
  what governs the change-set;
- the clamp statement `if (exponent >= 256)` only fires at **2^129**. Values in
  `[2^128, 2^129)` reach exponent 255 *without* the clamp — which is why the old code
  emitted Inf-with-garbage-mantissa there, and why the bug was never merely a clamping
  oversight.

### Addendum: gate 7 booted three builds against one writable image

Found by running the gate rather than reading it. Gate 7 returned a **non-deterministic
FAIL** — HEAD came back `1:1:0` (boot markers present, login prompt absent) after passing
`1:1:1` twice at the same commit with no code change in between.

Three explanations, resolved by measurement:

- *a regression?* No — both builds reach `login:` in about **100 s**;
- *a marginal timeout?* No — 100 s against a 300 s budget is three times the headroom;
- *shared mutable state?* Yes. The image's mtime tracked the most recent boot rather than
  the download.

GXemul's `-d` opens a disk image **read/write** by default, and the gate booted pristine,
pre-batch and HEAD **sequentially against the same 2 GB file**. Each build inherited
whatever filesystem state the previous one left behind — including an unclean unmount,
because the 300 s budget kills a guest that has already reached its login prompt. The runs
were never independent.

Fixed by booting through GXemul's `R:` prefix, which opens the base image read-only and
routes guest writes into a temporary overlay that is discarded at exit. Applied to gate 7
and to the gate 5 rig. Verified by running gate 7 **twice back to back** — a single pass
proves nothing about a flaky gate — with identical results both times and the image md5
unchanged (`82cce539…` before and after).

One measurement trap on the way: the first timing script reported "login never reached"
for *both* builds, which read like a serious regression. `login: ` is a prompt with **no
trailing newline**, so a line-oriented reader blocks forever waiting for a terminator that
never arrives. `grep` on the finished file sees it, because it reads the final partial
line. The instrument was broken, not the emulator.

`R:` freezes the image as it currently stands — the state many earlier read/write boots
left it in, not a pristine download. That buys reproducibility, which is what a gate needs,
but not provenance.

### The panel found the new harness had the exact defect it was built to remove

Two seats reviewed the harness independently and reached the same headline finding, which
is worth stating plainly because it is embarrassing: **gate 2 did not test the emulator.**
It transcribed *both* sides of its differential into its own C file and compared the copy
against itself. It never compiled, linked or executed `src/core/float_emul.c` — so
deleting #287 from the shipped source would have left all eight checks green. That is the
same defect as the 20-machine smoke this very round retired, one level of indirection
further back.

A second overstatement, also caught by both seats: the m88k rig was described as covering
#287. It does not. `1.5/3.0` and `sqrt(2)` are far inside the region where the two
implementations provably agree — the harness's own closed form says they can only differ
at `|x| >= 2^128` or `|x| < 2^-126` — so reverting #287 leaves every rig green. What the
rig proves is that the m88k **core** executes guest code and calls the shared function.
**No rig in the harness reaches the arm #287 changed**, MIPS included, and the coverage
table now says so.

What changed as a result:

- gate 2 compiles and links the real `float_emul.c`, and asserts the file it compiled is
  **byte-identical to the committed one**, so "the test passed" and "the repository is
  correct" became the same statement;
- it checks **absolute answers** as well as agreement — `1e300` must store as
  `0x7f800000` — because a purely relative differential passes when both sides are wrong
  the same way;
- the change-set is now checked as an **equivalence**. Containment alone is satisfied by a
  mutant that disables the overflow arm while keeping the underflow one; the completeness
  half rejects it, measured at **8,756,600** inputs that should have moved and did not.
  On the shipped source the two populations come out *identical* — 13,133,666 predicted,
  13,133,666 observed, **0 unexplained and 0 missed** — so the closed form is an
  empirically established equivalence rather than a one-way bound;
- a new `selftest_mutation.sh` gate exists for one purpose: to prove gate 2 can fail. It
  reverts #287 in a scratch copy and requires the differential to go red. It is the only
  gate that asserts something about the *harness* rather than the emulator;
- `count()` was emitting **two** lines on a zero match (`grep -c` prints `0` *and* exits 1,
  so the `|| echo 0` fired as well), which made gate 6's one deliberate expected-negative
  assertion impossible to satisfy. The full run reproduced it verbatim;
- the skip exit code moved from 2 to **77**, because bash exits 2 on a syntax error — a
  typo in a gate script was being reported as a coverage gap while the run exited 0;
- `gate_build.sh` now asserts that `est/` and `GXEMUL-SEC/` diverge in exactly the
  documented set. Nothing else in the harness would notice a correction applied to one
  tree and not the other: both build clean, both boot, and pmax quietly runs the old code.

Three of the harness's own assertions were wrong and were corrected by *running* it, not by
review — which is the point of a gate that can fail.

- `{ asc: data in }` (`dev_asc.c:417`) fires whenever a SCSI target has fewer bytes ready
  than the guest asked for — an ordinary event, measured at 1 on pmax and 5 on arc across
  a healthy boot — so requiring zero was simply wrong. It is bounded by a ceiling now,
  which still catches the flood class that round 40 found.
- A first-difference probe that swept exact powers of two reported "no difference
  anywhere", because at an exact power of two the assembled fraction is already zero and
  #287's mantissa clear is a no-op. It sweeps `1.5 * 2^e` instead.
- The completeness predicate initially excluded "exact powers of two" for that same
  reason, and the gate promptly found **one** input in 13,133,667 that contradicted it:
  `-1.1960164410049153e+198`, which both versions store as `ff800000` and which is not a
  power of two. The function *truncates* the fraction to 23 bits, so **any** double whose
  leading 23 fraction bits are zero assembles an all-zero mantissa; powers of two are
  merely the special case. With the predicate derived from the truncation rather than
  guessed, the missed count went to zero.

---


## Fifty-sixth round (#291) — the ARM cache-size fields shifted a negative number

One fix, in `cpus/cpu_arm.c`. The file is not one of the five that differ between the two
trees, so both stay byte-identical.

**What was wrong.** The ARM cache-type register packs each cache size into a 3-bit field,
encoded as `log2(bytes) - 9`. But 32 of the entries in `arm_cpu_types.h` leave
`dcache_shift` at 0 — ARM1136JSR1, which the Raspberry Pi machine selects, is one of them.
Those computed `0 - 9 = -9` and shifted it left, which is undefined behaviour in C.

**Inherited, not introduced.** UBSan reports it on unmodified upstream 0.7.0 as well.

**It was not just undefined, it was wrong.** −9 does not stay inside a 3-bit field.
Measured for ARM1136JSR1:

| | value |
|---|---|
| as shipped | `0xffdea0ea` |
| correct | `0x0b02a0ea` |
| bits wrongly set | `0xf4dc0000`, smeared across the CLASS and HARVARD fields |

**The obvious fix is the wrong one.** Casting to `uint32_t` makes the sanitizer stop
complaining and leaves the register exactly as corrupt — measured byte-identical at
`0xffdea0ea`. That is the same "quietly mask the problem" pattern rounds #118/#119 already
rejected in this project. An unspecified size now encodes as 0, and each field is masked to
its own width.

**Blast radius, measured rather than argued.** Only CPUs that leave a cache size
unspecified change. ARM920T, SA110 (used by `cats`) and 80321_400 produce byte-identical
values before and after.

**How it was found and how it was checked.** Gate 9 — the AddressSanitizer machine sweep
added in the previous round — reported it, which is the first time this project has had a
standing check capable of finding it. After the fix, `rpi` goes from 1 report to **0**, and
`cats`, `netwinder`, `iq80321`, `iyonix` and `testarm` all stay at 0. Both trees rebuild at
0 warnings and 0 errors.

The register is still marked "aren't used yet" in the source, so nothing observable to a
guest changes today. This is correctness groundwork, not a visible bug fix.

---


## Fifty-seventh round (#292) — single-precision results were 1 ulp low half the time

Files: `core/float_emul.c`, `include/float_emul.h`, `include/cpu_mips.h`,
`cpus/cpu_mips_coproc.c`. None are tree-divergent; both trees stay byte-identical.

**What was wrong, measured first.** `ieee_store_float_value()` assembles the fraction bit
by bit and throws the remainder away. Against the host's own `(float)` conversion — which
is correctly-rounded IEEE-754 and therefore an *independent* right answer — **50.12% of
in-range single-precision stores differed, always 1 ulp low, never high** (310,438 of
619,333 random in-range doubles). `1/3`, `0.1`, `1.7` and π all stored one bit small.
Double precision was exact, as expected: a host double has exactly the 52 fraction bits
the D format wants.

**What the review panel established before any edit** (four seats; all converged):

- The truncation is not sloppiness — it is **bit-exact round-toward-zero** (0 mismatches
  in 2.48M samples against a toward-zero oracle). That is *correct* for the SH-4, whose
  FPSCR resets to round-to-zero, and for PowerPC `stfs` per the recorded review — so an
  unconditional "fix" to nearest would have repaired 7 call sites by breaking 18.
- Only MIPS has the rounding mode in scope at its store: `fcr[FCSR]` is already read six
  lines above the call. The SH stores its mode but decodes it nowhere; m88k models no
  rounding register at all; Alpha and `dev_pvr` never store single precision.
- One seat disputes the "PowerPC `stfs` truncates architecturally" claim (believes it
  rounds per FPSCR.RN). Unresolved — flagged for the Power manual **before anyone wires
  PPC**. It does not affect this round: every seat keeps PPC on the legacy entry point.

**The change.** A mode-aware sibling, `ieee_store_float_value_rm(nf, fmt, rm)`, with modes
0–3 in the encoding MIPS FCSR, SH FPSCR and PPC FPSCR all share, plus `IEEE_RM_LEGACY`
reproducing the historical behaviour bit for bit. The old entry point becomes a one-line
wrapper selecting LEGACY, so all 24 untouched single-precision call sites and every
double-precision one keep their bytes. Exactly one caller changes: the MIPS result store
now passes `FCSR & 3`. The W/L integer formats **ignore the mode on purpose** — `cvt.w`
and `trunc.w` are indistinguishable at that call today and `trunc.w` is architecturally
round-toward-zero regardless of mode (see OUTSTANDING_BUGS before touching that).

Three implementation traps the panel predicted, each with a named test that would have
caught it: the carry must run out of the fraction into the exponent (`2−2^-24` must give
`0x40000000`, not wrap to 1.0); ties are to *even*, which a 20M random sweep cannot check
(an exact tie occurs about once per 2^29 inputs — `1+2^-24` stays, `1+3·2^-24` goes up);
and overflow is mode-dependent (nearest→Inf, toward-zero→largest finite, directed→per
side). The sliver `[2^128−2^103, 2^128)` rounds to Infinity under nearest *below* the
overflow line, and does.

**Verified.**
- Offline gate, extended: the nearest mode matches the host oracle over ~10M finite
  inputs with **0 mismatches** — "is the answer right", not "did it change as intended" —
  toward-zero likewise 0; ~9.99M mode-differing results; D untouched under every mode;
  14 named kill-vectors plus the legacy row all pass; every pre-existing #287 assertion
  unchanged (the legacy differential still classifies 13,133,666 differences with 0
  unexplained and 0 missed).
- The mutation self-test now runs **three mutants** — #287 reverted, ties-to-even broken
  to ties-away, and the mode parameter silently ignored — and the gate goes red on each.
  The ignored-parameter mutant exists because every differential ever written passes a
  parameter that is accepted and discarded.
- **In-emulator, both rigs** (the panel's own bar: without this, the pure-function tests
  can all pass while MIPS still calls the legacy entry): on a live R3000 (pmax) and R4000
  (arc), `ctc1` FCSR.RM=0 then `cvt.s.d` of 1/3 stores `0x3eaaaaab`; RM=1 stores
  `0x3eaaaaaa`. PROBE292_PASS.
- Clean rebuild 0 warnings / 0 errors, both trees.

## Fifty-eighth round (#293) — typed input on SuperH was stolen before the serial port saw it

One line plus a comment, `devices/dev_sh4.c`. Not tree-divergent.

**The symptom** (recorded as an outstanding bug two days earlier): commands typed at an
OpenBSD/landisk shell vanished whole — no echo, no execution — non-deterministically,
about one line in three, while the shell stayed alive. Timing, line terminators and line
length had already been measured and refuted as causes.

**The diagnosis was a chain of refuted instruments, worth keeping.** A counter pair on the
console layer showed 77 characters in, 77 out — which read as "delivery is perfect" and
sent the investigation at the SCIF's status bits. A patch setting the never-modelled RDF
flag alongside DR was built and measured: **no effect**. The panel then took the case
apart: one seat proved from the guest driver source that a delivered line *cannot* die
between the FIFO register and the tty (the driver stores at least `count` characters per
batch, and ksh switches modes with TCSADRAIN, which never discards) — and another seat
found the real mechanism and **ran the fix before recommending it**: on landisk nothing
ever claims `machine->main_console_handle`, so handle 0 — polled every tick for CTRL-C —
and the SCIF's own handle race for the same host stdin, and `console_charavail()` imports
up to 100 bytes into whichever polls first. When handle 0 wins, the line never reaches the
SCIF at all. The 77/77 counters were an artifact: they were global, and the debugger's
exit-time drain of handle 0 balanced the books.

**Confirmed from both sides.** A side-effect probe (`touch /tmp/mNN` × 12, then `ls`)
showed 10 of 12 commands vanished **and their files were never created** — the commands
never ran, killing the output-visibility theory. With the fix, the same probe delivers
**12 of 12**.

**The fix** is the claim `dev_dreamcast_maple.c`, `dev_luna88k.c` and `dev_vr41xx.c`
already make: the console-owning device sets `main_console_handle`. On the Dreamcast this
device is created with the CPU, *before* `dreamcast_maple` — so the maple keyboard still
overrides it and Dreamcast behaviour is unchanged.

**Harness consequence:** the landisk rig, which had deliberately sent no input since the
bug was found, is interactive again — it now boots to the installer shell and checks a
computed answer (`$((6*7))` → 42) on top of the hardware-probe assertion, with the
confirm-and-retry machinery kept as a free belt. The three refuted-hypothesis
measurements and the counter-artifact are recorded here so the next console mystery
starts from them.

## Fifty-ninth round (#294) — cvt.w now honours the rounding mode; trunc.w provably does not

Files: `core/float_emul.c`, `include/float_emul.h`, `cpus/cpu_mips_coproc.c`. None are
tree-divergent.

**The defect, measured first.** `cvt.w.d` of 3.5 yielded **3**; the MIPS default mode
(round-to-nearest-even) gives **4**. The cause was structural: `cvt.w`, `trunc.w` and
`trunc.l` all routed through the same convert operation and were indistinguishable at the
store — everything behaved like trunc. Upstream's own decoder carries `/*  TODO: not
CVT?  */` at both trunc sites; this round answers it: it *is* a convert, with the mode
forced.

**Design, from a four-seat panel with an adjudication pass.** The store's rounding mode
becomes an explicit parameter: the decoder forces toward-zero for `trunc.w`/`trunc.l`
(architecturally mode-independent) and everything else defers to FCSR. The integer (W/L)
arm of the store now rounds the value to an integral per the mode FIRST, then applies
#273's range clamps verbatim — once the value is integral, the same two constants express
exact range membership under every mode, so no per-mode clamp table exists to get wrong.
The adjudicator picked the parameter over per-instruction operation enums on the argument
that rounding policy is orthogonal to the operation, and future fixed-mode instructions
(`round.w`, `ceil.w`, `floor.w`) then need no new machinery at all.

**A proof in the design was refuted and repaired before implementation.** The tie test
"remainder equals 0.5" is NOT sound: `nf - floor(nf)` can round to exactly 0.5 for a
value that is not a tie (`nextafter(-0.5, 0)` — true distance 0.5 + 2^-54). No wrong
*result* survived the error, but the implementation compares against the exactly
representable midpoint `floor(nf) + 0.5` instead. `rint`/`nearbyint` are forbidden here
(they follow the HOST's mode) and `llround` rounds ties away from zero.

**Boundary facts pinned by the panel** (exact-rational arithmetic, encoded as vectors):
`-2147483648.5` stays IN RANGE under nearest — the tie lands on -2^31, which is *even* —
and under toward-zero and toward-+Inf; only toward--Inf floors it out. `+2147483647.5`
answers `0x7fffffff` under **all four modes** (two as a genuine result, two as the pinned
invalid default), so it discriminates nothing and the probes use exact integers. L has no
mode-dependent edge at its bounds: every double at that magnitude is already integral.

**Why the rigs cannot regress, from the guest's own toolchain source.** OpenBSD 2.2's
GAS expands `trunc.w.d` into an FCSR save, a `ctc1` forcing the mode field to toward-zero,
the `cvt.w.d`, and a restore — so pmax binaries execute `cvt.w` *frequently*, always under
forced toward-zero, where the new path is bit-identical by construction (and by a
406,405-double boundary sweep, 0 mismatches). The arc kernel uses the real `trunc.w`,
now forced toward-zero by the decoder. Measured: pmax 15/15 and arc 13/13 to `uid=0`,
unchanged.

**Verified.**
- Offline gate: 36 named vectors now, including the full tie matrix, the boundary table
  above, LEGACY rows that pin the historical truncation bit-for-bit (which the 20M sweep
  never covered for W), a NaN pin, and an L bound; every #287/#292 assertion unchanged.
- The mutation self-test runs a **fourth mutant** — the W arm rounding under LEGACY —
  and the gate goes red on it. Its first version was itself a no-op (LEGACY matched no
  case in the inner switch and fell through harmlessly); the self-test's own
  must-fail check caught that, which is precisely the job it exists to do.
- **Live on both rigs**: 32 probe rows — `cvt.w.d` ties under all four FCSR modes
  (3.5→4 nearest, 2.5→2 even, -2.5→-2 even, -2.5→-3 toward--Inf), `trunc.w.d` giving
  identical answers under different FCSR modes, the -2^31-0.5 boundary per mode, and a
  #292 S-arm regression row. PROBE294_PASS.
- Clean rebuild 0 warnings / 0 errors, both trees.

**Recorded, not fixed:** `round.w`, `ceil.w`, `floor.w` and `cvt.l` are not decoded at
all and fall through to a Coprocessor-Unusable exception *with CU1 enabled* — a
kernel-retry livelock shape (latent: zero occurrences across green boots). With this
round's machinery they are three decode blocks; see OUTSTANDING_BUGS.

## Sixtieth round (#295) — the fixed-rounding conversions, and a buffer declared full before it was filled

Two fixes, `cpus/cpu_mips_coproc.c` and `devices/dev_mb89352.c`. Neither file is
tree-divergent. Both came out of a backlog audit that found five of nine items in an older
block had silently been fixed while two live ones had never been indexed at all.

### `round` / `ceil` / `floor` / `cvt.l` were not decoded

`fpu_function()` matched no case for function codes `0x08`, `0x0a`, `0x0b`, `0x0c`, `0x0e`,
`0x0f` or `0x25`, returned 0, and the dispatcher tail did an ungated
`fatal("UNIMPLEMENTED coproc1 function")` **and** raised a Coprocessor-Unusable exception
for CP1 — with CU1 already enabled. Nothing in the CPU state changes across that trap
(same EPC, same instruction, CU1 already set), so a kernel that answers CpU(1) by granting
the FPU and returning re-executes it forever. Upstream's own TODO lists exactly these
opcodes.

**Reserved Instruction would have been the wrong exception**, and a panel seat settled it
from the primary source: the R4000 manual places a reserved COP1 *function* code under the
FPU's Unimplemented Operation exception (FCSR Cause.E, ExcCode 15) — which this file
already models in `fpu_unimpl_trap()`. RI is for CPU-level reserved encodings decided at
translate time (#231's ERET gate, #290's PS gate). So these are decoded **ungated**,
matching `trunc.l`/`trunc.w` which are ungated today and which #273 measured running on an
R3000A. Gating the whole table by ISA level is one coherent follow-on, not something to do
piecemeal.

Each instruction forces its own rounding mode through #294's parameter — nearest for
`round`, toward +Inf for `ceil`, toward −Inf for `floor` — while `cvt.l` defers to FCSR.

**The test had to be designed around an invisible bug.** The likeliest wrong
implementation is a copy-paste of the `cvt.w` block sitting seventy lines below, passing
`FPU_RM_FROM_FCSR` instead of a forced mode. Under the default `FCSR.RM = 0` that mutant
**agrees with a correct `round.w` on every input**. So every probe row runs under a
*non-zero* FCSR mode. Verified on both rigs: **20/20 rows**, including `round.w(2.5) → 2`
and `round.w(3.5) → 4` (ties to even), `ceil.w(−2.25) → −2` against `floor.w(−2.25) → −3`,
and `trunc.w` still ignoring FCSR entirely. Then the mutation was built for real:
`round.w(2.7)` under toward−Inf gives **3** on the shipped code and **2** on the mutant —
exactly the floor answer predicted.

### `dev_mb89352.c`: a DATA_OUT buffer declared full before any byte arrived

The backlog had this recorded as "the same defect as #263, on another host adapter". It
is not, and the difference matters. `mb89352_dreg_write()` only issues the command at
exact fill, so the natural path always supplies every byte — there is no short-transfer
tail. The actual defect is one line later: `data_out_offset = d->transfer_count` is set
**at allocation time**, and the disk layer's only guard is exactly that field
(`diskimage_scsicmd.c:778` compares it against the CDB size, then `:788` writes
`data_out` straight to the image). A guest that sets up a DATA_OUT phase, writes no data
bytes and then issues a WRITE therefore committed whatever the freed heap block last
held — and `scsi_transfer_alloc()` keeps a freelist for the transfer structs while the
buffers are `free()`d, so a same-size `malloc` very often returns the previous command's
sector data. #263 measured that exact consequence on the ASC: 384 bytes of the previous
command's buffer written onto the disk image.

Fixed by zeroing the allocation. **The honest repair — a truthful offset advanced as bytes
arrive — is deliberately deferred**, because the disk layer would then return "incomplete"
and this model discards that return, so the guest would be told a WRITE completed that
never reached the disk: exactly the defect #283 fixed in the ASC, re-created on the
luna88k write path. That needs its own round and its own probe.

`devices/dev_osiop.c:520` carries the same `clearflag = 0` and is **deliberately not
changed**: its offset advances only by bytes actually copied, so the disk layer's gate is
honest and a short transfer cannot commit uninitialised bytes; the grow-after-alloc route
is closed by the phase machine; and no harness rig instantiates it. Documented, not
patched.

**Verified.** Clean rebuild 0 warnings / 0 errors both trees; probe 20/20 on pmax and arc
with a real mutation as the negative control.

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

## Sixty-first round (#296) — SuperH read the rounding-mode field but never used it

One fix, `cpus/cpu_sh_instr.c`, not a tree-divergent file. A new regression gate. And a
repository cleanup that is unrelated to the code but touches the A/B baseline, so it is
recorded here rather than slipped in quietly.

### The field was decoded nowhere

`SH_FPSCR_RM_MASK` in `src/include/cpu_sh.h` was referenced by nothing in the tree except
the two `#define`s sitting directly under it. Every single-precision store called
`ieee_store_float_value(x, IEEE_FMT_S)` — the legacy two-argument entry point, which
truncates.

Truncation *is* round-toward-zero, and the SH-4 resets with RM = 01, toward zero. That is
why #292 wired the MIPS core and deliberately left this one alone: under the reset mode
there was no wrong answer to reproduce, and the rule here is not to touch what cannot be
reproduced.

What closed the gap was finding the guest that changes the mode. OpenBSD/landisk
`setregs()` does `pcb->pcb_fp.fpr_fpscr = FPSCR_PR` — RM = 00, round-to-nearest — at every
`exec`, and libc `fpsetround()` writes the field directly. So during user code it is not
the reset mode in force, it is nearest, and every result came back one unit-in-the-last-place
low.

**Measured on the committed build before any edit.** The SuperH serial port drops
host→guest writes non-deterministically (that is #293), so a probe that types at a guest
shell is not trustworthy here. Instead the debugger seeds registers cold, the guest itself
executes the instruction and stores the result with its own `fmov.s`, and the value is read
back out of memory — `reg` does not print floating-point registers on this core.

```
                      before        after
1.0/3.0  RM=01       3eaaaaaa      3eaaaaaa    toward zero, right both times
1.0/3.0  RM=00       3eaaaaaa      3eaaaaab    nearest: was one ulp low
```

### Thirteen of sixteen stores, and the first split was wrong

Wired: `float`, `fcnvds`, `fsqrt`, `fadd`, `fsub`, `fmul`, `fdiv`, `fmac`, `fipr`, and the
four `ftrv` stores.

Left on the legacy path: `fsca` (sin/cos) and `fsrra` (reciprocal square root). Those are
transcendental approximations where real silicon is documented to deviate by roughly 2^-21
— far more than a last-bit rounding choice — so no witness can be constructed whose correct
answer is decided by RM. Documented rather than changed.

**`fipr` and `ftrv` were in the second list until the panel took them out of it**, and the
reasoning that put them there was wrong twice over. The first draft argued that applying a
rounding mode to a reduced-precision instruction invents accuracy the silicon lacks. But
the reduced precision is in the *intermediate* — which is why the manual says the inexact
flag is always raised for these two — and the manual is explicit that the final result is
still rounded under RM. §6.4, verbatim:

> In a floating-point instruction, rounding is performed when generating the final
> operation result from the intermediate result. Therefore, the result of combination
> instructions such as FMAC, FTRV, and FIPR will differ from the result when using a basic
> instruction such as FADD, FSUB, or FMUL. … There are two rounding methods, the method to
> be used being determined by the RM field in FPSCR.

And the second error: this emulator does not model the reduced intermediate *at all*. It
evaluates the whole dot product in host double, so the final store is the only rounding in
the emulated path. Truncating it is not fidelity to imprecise hardware, just a different
wrong answer. Measured — `fipr` of {1.5,0,0,0} against {1+2^-23,0,0,0} is an exact
midpoint, and nearest returned the truncated `3fc00001` where it owes `3fc00002`.

`ftrc` is untouched and stays untouched: round-toward-zero by architecture regardless of
RM. It never routes through `ieee_store_float_value` at all, which was checked rather than
assumed.

RM values 10 and 11 are **reserved** on SH-4 and map here to the reset mode. This is not
hypothetical: OpenBSD's `fenv.h` defines `FE_UPWARD` as 0x2 and `FE_DOWNWARD` as 0x3 inside
its round mask, so `fesetround()` genuinely writes the reserved encodings. Keeping the
reset mode invents less than inventing directed rounding the hardware does not document.

### The rider: this also changes what overflow stores

Leaving `IEEE_RM_LEGACY` is not only a rounding change. LEGACY's overflow arm is
unconditional ±Infinity — that is #287, and gate 2 asserts it stays bit-identical — while
the real modes are mode-dependent. A second, independent behaviour change on the same
commit, so it was measured on its own. `1e30f * 1e30f`:

```
RM=00 nearest      7f800000   +Inf      unchanged
RM=01 toward zero  7f7fffff   FLT_MAX   CHANGED, was +Inf
```

This one had to be right, because a wrong answer would make the commit a regression on the
*reset* mode — the mode a bare-metal guest that never touches FPSCR runs in forever. The
manual settles it, §6.5:

> Overflow (O): When rounding mode = RZ, the maximum normalized number, with the same sign
> as the unrounded value, is generated. When rounding mode = RN, infinity with the same
> sign as the unrounded value is generated.

The emulator's reset value was checked to match too — `cpu_sh.c` initialises FPSCR to
`0x00040001`, which is the manual's reset state with RM = 01 — so a guest that never writes
the field still gets toward-zero, and the only thing that changed for it is the overflow
answer, in the direction the manual specifies.

### What the panel found, including where it was wrong

Two seats returned DO NOT SHIP. One was right and one was not, and both were settled by
measurement rather than by counting seats.

The right one is the `fipr`/`ftrv` finding above. Two seats derived the same exact-midpoint
witness independently, and running it reproduced the defect.

The other objection was that leaving the seven `IEEE_FMT_D` stores alone makes this a
half-fix. It does not, and the reason is a format identity rather than an oversight: the D
format **is** a host double — same 11-bit exponent, same 52-bit fraction — so the store is a
pure re-encode with no narrowing step for a mode to control. The rounding already happened
in the host's arithmetic. Measured: double `1.0/10.0` gives low word `9999999a` under both
modes, where a real toward-zero would owe `99999999`. Wiring those seven sites would have
been a provable no-op. The seat's own worked example was self-refuting as well — `1.0 +
2^-53` is an exact tie, and ties-to-even returns the 1.0 it called wrong — which two other
seats spotted independently.

**The objection does expose a real gap, now recorded rather than patched.** SuperH
double-precision arithmetic ignores FPSCR.RM entirely; it inherits the host's mode, which
is nearest. Under RM=00 that happens to agree with silicon, so the gap is invisible in the
common case; under RM=01 it diverges. Fixing it means running the arithmetic itself under a
controlled host mode, and #292 already established why that road is closed here.

A third finding corrected the commit's own comment rather than its code. The first draft
said truncation is "bit-exact round-toward-zero". It is not — it is toward-zero *of the
value handed to the store*. Every core here evaluates in host double and then narrows, so a
cancellation finer than 2^-53 is already gone: `fsub` of 1.0 and 2^-60 collapses to exactly
1.0 before the store sees it, and toward-zero then yields `3f800000` where silicon rounds
the exact difference to `3f7fffff`. Measured and confirmed. Pre-existing, shared by every
CPU core in the tree, untouched by this correction — and now stated accurately in the
comment and pinned in the gate.

A fourth corrected a claim about the build. The comment justified its include guard with
"this file is included twice". It is not, for SuperH: the second inclusion in
`tmp_sh_tail.c` sits under `#ifdef DYNTRANS_DUALMODE_32`, which `cpu_sh.c` never defines
(MIPS, PPC and RISC-V are the dual-mode cores). The guard is correct future-proofing and is
kept, but it is inert today and now says so. This project shipped #270 to fix exactly this
kind of overclaim.

One objection was raised and rejected on the merits: that the mode should be hoisted into
instruction selection rather than read per execution. It must not be. Translated
instruction calls are cached and nothing invalidates them when FPSCR is written, so a
translation-time mode would go stale the moment a guest called `fpsetround()` — which is
the defect being fixed. The per-execution read is a load and a compare in front of a store
primitive that already runs a bit-serial loop.

### Gate 10, and proving it can fail

`regress/gate_sh_rounding.sh` runs nine vectors under both rounding modes on real guest
instructions — eighteen pairs, all passing. Seven of the nine discriminate: their two modes
want different answers, so reverting the fix turns them red. `fdiv`, `float`, `fadd`,
`fmac`, `fipr`, `ftrv` and `fmul` are each named individually, so a single site reverting
cannot hide behind an aggregate count. The gate also asserts *how many* vectors
discriminate, because a table where every vector wanted the same answer in both modes would
pass vacuously — the failure mode this harness has now been bitten by five times.

Then it was proved rather than assumed. A mutant with `sh_fp_rm()` forced back to
`IEEE_RM_LEGACY` scores **11 of 18**: every one of the seven instructions fails exactly one
arm, which is the arithmetic the fix predicts.

The remaining two vectors are deliberately mode-independent and marked PIN — the
double-precision no-op and the double-rounding limitation. They record what is *not* fixed.
A pin going red means a known limitation moved without the record being updated, which is
worth knowing in either direction.

### Repository cleanup: two files that were never upstream

`src/cpus/grep.exe.stackdump` and `src/devices/grep.exe.stackdump` are git-bash crash dumps
that were swept into `39748e3`, the commit that is supposed to be pristine upstream 0.7.0.
They are not part of GXemul, appear in no object list, are referenced by nothing, and get
rewritten whenever a `grep` crashes — which made them show up as diff noise. Untracked and
added to `.gitignore`.

They cannot have affected any measurement: the build uses explicit object lists with no
wildcards, so no A/B or regression conclusion drawn against `39748e3` is disturbed. The
import commit is left alone rather than rewritten again; this note is the record that it
carries two files upstream never shipped.

## Sixty-second round (#297) — ftrc converted with a raw C cast, so the guest's answer depended on the host

One fix, `cpus/cpu_sh_instr.c`, not a tree-divergent file. First item of the five-seat
feasibility triage's queue, and the panel's unanimous rank 1.

### The defect

`ftrc` — SuperH's float-to-integer conversion — did `(int32_t) op1.f` on both arms. For
NaN, ±Infinity and out-of-range values that cast is undefined behaviour in C, which means
the *guest-visible* result was whatever the *host* CPU happened to do. On x86 the cast
delivers 0x80000000 for every special case; an aarch64 host saturates and gives NaN → 0 —
same guest, same program, different answer. The SH-4 manual instead specifies a value
ladder: +Inf and positive overflow deliver +MAX 0x7fffffff; −Inf, negative overflow and
**all NaN of either sign** deliver −MAX 0x80000000.

Measured on the committed build before the edit: ftrc(+Inf) and ftrc(2^40) both stored
0x80000000 where the manual owes 0x7fffffff. The in-range control (5.7 → 5) passed. That
is the reproduction the project rule requires, and it is also the practical exposure: an
organic guest path (any userland `(int)` cast of a NaN/Inf/huge double — awk's `int()`,
printf of casts) reaches this instruction, and OpenBSD runs SH-4 processes with PR=1, so
the double arm is the hot one.

### The fix mirrors the manual's own pseudocode, constants and all

The classifier runs on the raw register bits, exactly as the manual's
`ftrc_single_type_of` / `ftrc_double_type_of` do, and only then hands in-range values to
the old interpret-and-cast path — which keeps the happy path byte-identical.

The details that would have been easy to get wrong, each verified by a probe row:

- **The NaN test must come first.** A positive NaN's bits also exceed the positive range
  bound, and the manual routes NaN to −MAX, not +MAX. A ladder with the checks in the
  natural "range first" order ships NaN → +MAX and passes every non-NaN vector.
- **The single-precision bound is strict, the double bound is not.** 0x4effffff
  (2147483520) is NORM and truncates to 0x7fffff80; but exactly 2^31 in double is already
  Invalid → +MAX.
- **The negative double bound is −(2^31+1), not −2^31.** So −2147483648.5 is still NORM
  and truncates — legally — to −2^31. Same stored bits as the Invalid arm, different
  route; the distinction matters the day someone adds the V cause bit.
- **−2^31 exactly, in single, is NORM** (the strict negative check), and the cast of
  −2147483648.0 is defined C.

Every value the ladder admits to the NORM arm has an integral part representable in
int32 — the extreme admitted doubles are 0x41dfffffffffffff (truncates to INT32_MAX) and
0xc1e00000001fffff (truncates to INT32_MIN) — so the one cast that remains is defined C
on every host. A panel seat verified exactly those two witnesses.

Scope: values only. No FPSCR.V cause bit is raised — this model raises no SH FPU
exceptions anywhere, and a lone cause bit would be new guest-visible surface with no
victim. That mirrors #273's values-only scope on MIPS, **but not #273's result table**:
MIPS chose legacy-compatible 0x7fffffff for all five special cases; SH-4 documents the
±MAX split, and the two must not be cross-copied.

### Verification

21 probe rows on the fixed build, 21 passing — S and D arms, both defect witnesses
flipped, all four boundary semantics exact, NaN of both signs and both arms, and
subnormals (which route to NORM and truncate to 0, as the pseudocode implies).

Gate 10 grew six ftrc rows and now runs 15 vectors × 2 modes = 30 pairs. The ftrc rows
are **deliberately mode-independent** — the manual says "the rounding mode is always
truncation" — and the gate's discriminating-count check now cuts both ways: it fails if
the #296 table is weakened *and* if anyone ever wires ftrc to FPSCR.RM. The probe gained
an optional second instruction word per vector, because ftrc's result lands in FPUL and
the guest has to run `sts fpul,r2 ; mov.l r2,@r1` to get it into dumpable memory.

The negative control ran for real: a build with #297 reverted scores **24 of 30**,
failing exactly the three vectors whose x86-UB answer differs from the manual — +Inf,
+2^40 and the D 2^31 boundary, both arms each — while the rows where the UB cast happens
to coincide with the manual on x86 (NaN, the strict S edge, the negative D half) stay
green. That is the arithmetic the fix predicts, and it is also the honest statement of
what the old code got right by accident on this one host.

The five-seat adverse panel: three SHIP, one SHIP WITH CHANGES, no in-scope code defect
— every seat conceded all seven attack-surface points. One seat verified every constant
and comparison operator against the manual's pseudocode table by table; two
independently proved the extreme NORM-admitted doubles truncate to exactly INT32_MAX and
INT32_MIN, closing the cast-definedness question (one noting it holds *because* the
interpreted value is a double — a float there would re-open the UB); one confirmed the
early returns skip no bookkeeping because the dyntrans loop advances `next_ic` before
the handler runs.

Three findings were adopted, all about honesty rather than code:

- The comment's original "no victim" justification for skipping the FPSCR.V cause bit
  **argued the wrong thing** — FPSCR is *existing* guest-visible surface and `STS FPSCR`
  after ftrc(+Inf) falsifies the claim (hardware reads V=1, this model reads 0). The
  comment now states the boring true reason: no instruction in this core sets any FPSCR
  cause bit, so a lone V here would be the one flag a guest could observe, implying the
  others work. The whole missing SH FPU exception model is now indexed in
  OUTSTANDING_BUGS instead of being waved off.
- The negative-boundary probe rows are **value-vacuous by construction** — NORM
  truncation and the Invalid arm both store 0x80000000 for every value in
  (−2^31−1, −2^31], so those rows cannot distinguish the route, only the value. Stated
  here so the 21/21 is not over-read; the rows that carry the proof are +Inf, +2^40,
  the strict S edge, and the positive-NaN ordering witness — all four of which are
  durably gated in gate 10.
- A **pre-existing** subnormal decode defect in `ieee_interpret_float_value`
  (implicit-1 applied to subnormals; invisible through ftrc since both truncate to 0)
  was surfaced and indexed.

The organic in-guest witness, for the record: `awk 'BEGIN{print int(2^40)}'` owes
2147483647 and the old build on x86 printed −2147483648 — and a different wrong answer
on an ARM host, which is the whole point.

## Sixty-third round (#298) — m88k stored its rounding register, read it back, and used it nowhere

One fix across `cpus/cpu_m88k_instr.c` and `include/cpu_m88k.h`, neither tree-divergent.
Second item of the feasibility queue, and the one with a live victim.

### The defect was live on a rig that boots to root

fcr63 — the m88k FPCR, the user-mode FPU control register — was faithfully stored by
`m88k_fstcr()` and read back by `fldcr`, and decoded into nothing. All six m88k
single-precision arms stored through the legacy truncating entry point. OUTSTANDING_BUGS
had this recorded as "m88k models no rounding register at all — nothing to wire", which
the feasibility panel proved wrong twice over: the register file is modeled and retained,
and the defect does not even need a mode-changing guest. OpenBSD/m88k's `setregs()`
zeroes fcr63 at every exec — `fstcr r0, fcr63`, r0 being hardwired zero — and zero means
round-to-NEAREST. So every luna88k userland single-precision result was one ulp low about
half the time, on the OpenBSD 7.7 rig this project boots to a root shell in gate 4.

Reproduced cold on the committed build before any edit, with the pipeline proven first:

```
control  1.0f + 1.0f       -> 40000000    ok, the probe machinery works
defect   1.0f + 1.5*2^-24  -> 3f800000    round-to-nearest owes 3f800001
fcr63    fstcr 0x4000      -> fldcr reads it back: retained, unused
```

### The decode must swap the directed pair, and the gate is built around that fact

m88k's RM field is 00 nearest, 01 toward zero, **10 toward MINUS infinity, 11 toward PLUS
infinity** — the opposite directed order from MIPS FCSR, SH FPSCR, and `float_emul.h`'s
own IEEE_RM values. Primary sources, both from the feasibility round and re-verified by
this round's panel: the MC88100 User's Manual §2.4.4, and the guest's own authority —
OpenBSD's m88k `<ieeefp.h>` (`FP_RM=2` toward −Inf, `FP_RP=3` toward +Inf) with libc
`fpsetround()` writing exactly this field via `fstcr`.

The trap in that fact: a decode that FORGETS the swap passes every sign-symmetric test,
because the two directed modes simply trade places consistently. Only rows whose expected
value differs by the *sign* of the operand catch it. Gate 11 therefore runs
sign-asymmetric pairs — the same magnitudes with the sign flipped, where toward+Inf must
truncate the negative sum it grew on the positive side — and asserts those four rows by
name.

Six sites wired: `fadd.sss`, `fsub.sss`, `fsub.sds` (the mixed double-minus-single arm),
`fmul.sss`, `fdiv.sss`, and `flt.ss` (integer to single — exact into double, so the store
is the only rounding). The D-format arms are excluded on the established
nothing-to-round-at-the-store grounds, and the m88k `trnc`/`int` conversions — which have
the same raw-cast defect #297 just fixed on SH — are deliberately a separate round rather
than a rider on this one.

### Gate 11

Twenty rows on the luna-88k machine, cold debugger, nothing booted. Every row sets the
mode the way a real guest does — the guest itself executes `fstcr r5,fcr63` — so the
decode is proven end-to-end, not just the store arm. m88k floating point operates on
general registers, which the debugger seeds and prints directly; no memory round-trip.
The fcr63 retention row pins the #296-shape premise itself.

20 of 20 pass on the fixed build: the flipped defect row, all four modes on the positive
witness, the four asymmetric swap tripwires, one row per wired site including the exact
midpoint (`fmul` ties-to-even), `fdiv` 1.0/3.0, and the `flt` integer tie on both signs.

One measurement lesson is recorded in the probe rather than papered over: a single row in
the first full run returned no value at all — not a wrong value — and three targeted
re-runs all read the correct answer. The register dump had straggled in after the
prompt detector fired under host load. The probe now retries the *read* once (the value
cannot change between two `reg` commands, so retrying the read is honest where retrying
the row until green would not be).

Both negative controls ran for real, each with its prediction written down first:

- **The missing-swap mutant** — the panel's named likeliest wrong implementation, a
  decode without the 2↔3 exchange — scores **13 of 20**: all four asymmetric tripwires
  red by name, plus the three direction-pinned symmetric rows, while every RN/RZ row
  stays green. Exactly the failure signature the gate was designed to produce.
- **The legacy-revert mutant** — the helper forced back to truncation — scores
  **11 of 20**, failing the five RN rows a truncating store must fail plus the four
  directed rows truncation gets wrong, while the RZ rows (truncation *is* toward-zero)
  and the two accidental coincidences stay green.

### What the panel changed

One seat's DO NOT SHIP contained one finding that was adopted and one that was already
queued. Adopted: with the RM field now decoded, `m88k_fstcr()`'s blanket "UNIMPLEMENTED
fcr" warning became dishonest — a guest calling `fpsetround()` is doing something
implemented. fcr63 now warns only for bits *outside* the RM field, which really are
ignored (the #270 honesty class). Overruled by the queue: the D-format arms still follow
the host's rounding mode — that is round 65's fma-residual work, adjudicated by the
feasibility panel, not a rider on this round; and the seat's concrete witness was an
exact tie (`1.0 + 2^-53`), which rounds to the same value under nearest and toward-zero
alike, demonstrating no divergence. The same seat independently confirmed the swap from
MC88100 Table 2-4 and validated the asymmetric-vector design as the decisive measurement.

Another seat's SHIP-WITH-CHANGES did this round its biggest favour. It demanded a
positive control for the new zero-warning check — and chasing that demand exposed that
the check was **born vacuous**: the fstcr warning goes to the emulator's stdout, which
only the probe's pty capture ever sees, so the gate was grepping a log that could not
contain the string. A check that cannot fail, caught before it ever reported a
misleading green. The probe now counts the warning inside each session and reports two
markers — the accumulated count across all pure-RM sessions (asserted 0) and a
deliberate non-RM write of 0x1 as the positive control (asserted exactly 1, proving the
counter counts). The same seat re-ran gate 11 and the full luna88k boot rig itself on
the fixed build (20/20 and PASS with the exact expected answers), confirmed the swap
from four primary sources including the kernel's own FP-completion code, and did a full
handler census proving the six wired sites are the only single-precision result
producers in the file. Its census also surfaced a pre-existing coverage gap — the ISA's
mixed-format S-destination forms (`fadd.ssd` and friends) are undecoded entirely — which
is indexed, not patched.

The last seat found the one divergence the new modes can actually observe, and it is
pinned rather than hidden. The arms compute in host double before the store, so a
residue finer than 2^-53 collapses before a directed mode can see it: hardware's sticky
bit — "the logical OR of all the bits that would be in the result if the result was
infinitely precise" — rounds `1.0 + 2^-60` **up** under toward-+Inf, where this model
stores 1.0. The seat also proved the band's edges: add/sub only, because `fmul`'s
48-bit product is always exact in double and a nonzero `fdiv` residue always survives
the double grid, and RN/RZ are unaffected because the collapsed value is their answer
anyway. Only the two modes #298 *introduces* can observe it. Gate 11 now carries the
row as a named PIN, expected at today's divergent value, with the instruction that it
must flip and be rewritten as a discriminating vector when the next round's
round-to-odd helper lands — whose scope now explicitly includes these m88k arms.

## Sixty-fourth round (#299) — the sum was rounded twice, and round-to-odd makes the first rounding harmless

One shared helper in `core/float_emul.c`, routed from eight call sites across three CPU
families: SH (`fadd`, `fsub`, `fmac`), m88k (`fadd.sss`, `fsub.sss`, `fsub.sds`), and
MIPS (`add.s`, `sub.s`). Third item of the feasibility queue.

### The defect, pinned twice before the fix

Every core computes single-precision add/sub in host double, then stores. The double
rounds to 53 bits first — in the host's nearest mode — so a residue finer than the
double grid is gone before the store can round it. Gates 10 and 11 had this **pinned as
known-divergent** since the rounds that discovered it:

```
SH   fsub 1.0 − 2^-60   RZ           measured 3f800000    silicon owes 3f7fffff
m88k fadd 1.0 + 2^-60   toward +Inf  measured 3f800000    sticky bit owes 3f800001
```

And the one *organic, default-mode* victim: `fmac` under plain nearest. The SH-4 manual
says fmac rounds ONCE; the old path rounded the exact result to double, landed exactly on
a single-precision midpoint, and ties-to-even then picked the far side. The witness was
constructed offline from exact rationals: `(0x3fc00003 × 0x33fffffc) + 1.0` measured
`3f800002` where nearest owes `3f800001` — and gcc emits fmac on SH-4, so real compiled
guest code takes this path.

### Round-to-odd, and the two formulas the panel had already killed

Boldo–Melquiond: when the wide format carries at least 2p+2 bits of the narrow one — and
53 ≥ 2·24+2 — rounding the exact value to odd in the wide format, then rounding to the
narrow format in ANY mode, equals the direct correct rounding. Round-to-odd of a sum
needs no wider arithmetic: Knuth's 2Sum recovers the rounding error of `a + b` exactly
in six flops, and if the error is nonzero the sum is forced to the neighbouring double
with odd mantissa, stepping toward the error's sign.

Both halves of that sentence had wrong versions that were refuted before any code was
written, which is why the offline gate now asserts absolute answers rather than trusting
formulas. The feasibility brief's 2Sum was a broken three-flop hybrid that produces
garbage when |a| < |b| — every seat refuted it, and Knuth's magnitude-unconditional form
is what shipped. And the obvious odd-force — `bits |= 1` — steps away from zero
regardless of which side the exact value is on; the shipped step is ±1 on the
sign-magnitude pattern, toward the error's sign, cross-validated bit-for-bit against a
Python model in the offline constructor.

One case round-to-odd cannot express is handled explicitly: IEEE gives `x + (−x)` the
sign of the *mode* — +0 everywhere except toward-minus-infinity, where it is −0. The
host computes +0, so the helper flips an exact zero under that one mode, with
`(+0)+(+0)` excluded. Measured on the luna88k rig: the toward−Inf zero row reads
`0x80000000` and the nearest row reads `0x00000000`.

The helper is deliberately **not** safe for double arithmetic — for single operands the
intermediates can neither overflow nor reach subnormals, which is exactly the safety
argument, and it evaporates for doubles. That is the next round's fma-residual work,
with mandatory overflow and subnormal handling this function does not have.

### Verification

- **Gate 2 (offline)**: seventeen new absolute-answer vectors — all four band
  directions on both operand signs, the exact-zero sign table, no-change controls, the
  fmac witness, and a control asserting the *plain-double* path still gets the tie
  wrong (so the vector provably discriminates). Every expected value derived from exact
  rationals by the constructor and cross-checked against an independent Python model of
  the same bit-stepping. 0 failures.
- **Gate 10 (SH rig)**: the #296 PIN flipped exactly as its own comment required and is
  now a discriminating vector (8 of 16 vectors discriminate, up from 7); the fmac
  tie-band row is green on both modes; the faddinf Inf-pass-through row closes the panel's find. 34 pairs, PASS.
- **Gate 11 (m88k rig)**: the #298 PIN flipped to `3f800001`; the two exact-zero rows
  pass; the fsub.sds Inf row exercises the helper with an infinite double operand. 24 rows, PASS.
- **MIPS**: add.s/sub.s take the same helper, gated to single-in/single-out; the double
  path is untouched by construction and gate 2's D-untouched sweep stays at zero.

### The panel caught a guest-visible regression inside the fix, before it shipped

The review brief's attack-surface section contained a claim written with confidence and
exactly backwards: "2Sum's e is NaN, `e != 0.0` is false — passes through." In C,
`NaN != 0.0` is **true**. Three seats refuted it independently, each with the same
concrete input: with a ±Inf operand the 2Sum error is NaN, the odd-force branch runs,
and the raw bit step lands one below +Inf — which is DBL_MAX. `+Inf + 1.0` stored
`0x7f7fffff` under toward-zero, and `−Inf − 1.0` stepped **up** into a negative NaN. One
seat sharpened the reachability: `fsub.sds`'s first operand is a full *double*, so Inf
walks straight in on the m88k rig. The exact-rational constructor never saw it because
it only ever generated finite vectors — an instrument can only refute what its inputs
reach.

The sequence that followed is the project's discipline working as designed: the Inf
vectors were added to the offline gate **first** and watched fail on the unguarded
helper (`+Inf+1.0 RZ → 7f7fffff`; `−Inf−1.0 RM → ffffffff`); then the one-line
`isfinite(s)` guard went in; then the vectors went green — 0 of 22 — and rig rows on
both machines (`faddinf` on SH, `fsub.sds inf` on m88k) pin the contract where guests
actually run. The guard's comment credits the refutation and preserves the seat-proven
fact that finite `s` with nonzero `e` cannot be zero for any routed operand (the
2^-298 quantum floor).

The rest of the audit came back clean across every seat: the finite bit step is a true
nextafter including binade crossings; the exact-zero table is right in all rows; the
sub-as-negated-add identity is exact; the MIPS gate condition selects exactly
add.s/sub.s with no #246 subnormal-trap interplay (a grid argument — no representable
point inside the RTO-vs-RN sliver around FLT_MIN); the fmac product-exactness claim
holds down to subnormal singles; the scope is complete; and the build flags (-O3, no
fast-math, no fp-contract) protect 2Sum's preconditions.

### The negative control, one mutant, predictions written first

The helper neutered to plain `a + b` fails exactly what the fix claims and nothing else:
gate 2's band and zero-RM and fmac vectors (DIFF_FAIL), gate 10's band-RZ and fmac-RN
arms (30 of 32), gate 11's band and zero-toward-Inf rows (21 of 23) — measured, not
asserted.

One more measured find from the post-fix verification seat, documented and pinned rather
than left to drift: routing subtraction as `a + (−b)` means a NaN **subtrahend** is
negated before propagation, so `1.0 − qNaN` now stores the negative canonical NaN where
it stored the positive one (A/B-measured at the build's own optimisation level; MIPS is
immune behind its canonical-NaN override). IEEE leaves the sign of an arithmetic NaN
unspecified and class and quietness are preserved, so this is conformant — but it is a
real difference, and an undocumented one is how drift starts. The offline gate pins the
single-NaN case at its new full value; the Inf−Inf NaN stays class-only because that one
belongs to the host. The same seat also named the sharpest remaining structural hole:
the offline gate compiles the helper with its *own* flags, so a future `-ffast-math` in
configure would break the shipped emulator's 2Sum while the gate stayed green — the gate
now trips on the tree's flags directly. And its victim accounting is worth keeping: on
luna88k under default round-to-nearest, `fadd.sss`/`fsub.sss` are bit-identical to
before (53 ≥ 2·24+2 makes RN-then-RN innocuous) and only `fsub.sds` — the fmac-analog
whose first operand is already 53-bit — changes organically; on SH the band is organic
because toward-zero is the hardware reset mode; on MIPS the correction is latent until a
guest programs a directed mode.

## Sixty-fifth round (#300) — the D-format store has nothing to round, so the arithmetic learned to

Four helpers in `core/float_emul.c`, routed from twenty-five call sites across the same
three CPU families as #299: SH's five D arms, MIPS's five D operations in `fpu_op`, and
fifteen m88k D-destination arms. Fourth item of the feasibility queue, and the one whose
half-fix versions the panel pre-refused.

### Why the store could never fix this

A host double already has exactly the 52 fraction bits the D format wants, so
`ieee_store_float_value` on a D result is a pure re-encode — gate 10 carried that fact
as a PIN since round 61, with `1.0/10.0` under toward-zero measuring low word `…9a`
(the host's nearest answer) where silicon owes `…99`. The only place a rounding mode can
be honoured is the arithmetic itself, and the host's arithmetic runs under nearest.

The mechanism: take the host's nearest result, then recover — exactly — which side of
the true value it landed on. One fma does it per operation: `r = fma(q, b, −a)` is the
exact division residual (the Markstein lemma), `r = fma(q, q, −a)` the square root's,
`r = fma(a, b, −p)` the exact product error, and Knuth's 2Sum covers add and subtract.
If the residual says the nearest result sits on the wrong side for the requested
direction, step one ulp on the sign-magnitude bit pattern. Under nearest (and LEGACY)
the helpers return the plain host result, so nearest-mode guests — which is every stock
boot on all three rigs — are bit-identical by construction.

### The model sweep caught the predicted bug before any C existed

The feasibility panel's review of the *design sketch* had already refuted two formulas
and predicted a third failure mode: "the residual sign convention is self-inconsistent
across ops — an offline differential with per-op sign truth tables is a hard
requirement." So this round's first artifact was not code but a Python model of the
whole mechanism, checked against exact rational oracles: 80 000 division, 160 000
multiply/add, and 15 000 square-root property checks, plus named rows for every overflow
arm.

The sweep's first run failed 30 114 of 160 000 — the multiply overshoot test read
`r < 0` unconditionally, which is correct for positive products and *exactly backwards*
for negative ones. The division form never had the bug because it tests against
`sign(a)`. One line, invisible to every positive-operand test, precisely the flip the
panel named. Fixed in the model, swept to zero, and only then transliterated to C — the
19 offline gate vectors include the caught case as a permanent pin, and the C passed all
of them on its first run.

### The mandatory edges, all present

- **Overflow**: when the nearest result is ±Inf from finite operands, the fma residual
  would be NaN. `ieee_dir_overflow` answers by mode and sign — toward-zero clamps to
  ±DBL_MAX, toward+Inf keeps +Inf but clamps the negative side, toward−Inf mirrors.
- **The accepted-nearest bands** (in their final, thrice-reviewed form — the first two
  versions guarded the wrong quantity, and both stories are below): div and sqrt accept
  the nearest answer when the residual-scale *operand* is below 2^-969 — the residual's
  QUANTUM bound — mul when the *product* is, and add needs no band, only the single
  overflow-tie exclusion. Above the bands the correction is live everywhere, subnormal
  results included.
- **Non-finite operands and results pass through untouched.** After #299's lesson
  (`NaN != 0.0` is true in C), every helper checks `isfinite` first — structurally, not
  as an afterthought.

### Verification

- Gate 2: 19 absolute-answer vectors from the exact constructor — the round-61 case in
  all four modes, the `b < 0` sign trap, both overflow signs and directions, the caught
  negative-product mul case, the add band, exact-zero signs, `sqrt(2)`, and Inf/NaN
  pass-through. 0 failures, first run.
- Gate 10: the D pin **flipped exactly as its own comment required** — by correcting
  the arithmetic, the only mechanism its comment said could ever flip it — and is now
  the ninth discriminating vector.
- Gate 11: a new `fdiv.ddd` row proves the mode end-to-end on the m88k rig, guest
  `fstcr` included. Its first version failed with the *nearest* answer and the failure
  was real — in the probe: the row seeded r5 as the divisor's low word, silently
  clobbering the register the probe stages the rounding mode in before the guest's
  `fstcr` consumes it. The register plan is part of the vector, and the row's comment
  now says so.

### The panel's second pass redesigned the safety bands

Two seats attacked the helpers' edges and both connected. One filed the
subnormal-OPERAND witnesses with full traces: a subnormal dividend can yield a perfectly
normal quotient whose residual lives at the *dividend's* scale — beneath the subnormal
quantum — so the fma underflows it to zero and the helper mistakes underflow for
exactness, silently skipping the nudge. The result-magnitude guard could never see it.
The other seat went further on three fronts: the same class for sqrt from a barely-normal
input; **divide-by-zero's exact, mode-independent infinity falling into the overflow
clamp** (`1.0 / +0.0` under toward-zero returned DBL_MAX — and the seat also refuted the
model's own note claiming SH intercepts zero divisors; it does not); and the honest
observation that the result-magnitude band spanned **122 normal binades** in which the
correction was silently absent and, despite the comment's claim, unpinned.

The redesign, model-first as before: the bands moved to where the failure actually is —
the residual-scale *operand* (dividend, radicand) below 2^-1018 for div and sqrt, the
*product* below the same threshold for mul, and no band at all for add, whose 2Sum error
is exactly representable down through gradual underflow. Above the bands the correction
is now live everywhere, **including subnormal results**: the directed step works on the
sign-magnitude pattern down to and across zero, so a positive-tiny quotient under
toward-+Inf correctly yields 2^-1074 stepped from the +0 pattern — which also exposed
that a comparison-derived sign breaks at −0, fixed with signbit. Divide-by-zero passes
through exact. Each piece was model-validated first (a further ~9 000 subnormal-result
oracle checks and the zero-crossing rows), then transliterated; the offline gate grew to
28 vectors, with the 122-binade seat's own witness now a *corrected* row rather than an
accepted band, both div-by-zero signs pinned, and the agy witnesses pinned at the honest
band values.

One further find is indexed, not patched: `cvt.d.l` — a 64-bit integer with more than 53
significant bits — converts under host nearest before any mode can matter. Outside this
round's five operations; recorded in OUTSTANDING_BUGS with its witness.

### The third pass: the band was still wrong, and the proof needed construction

The post-fix verification seat rejected the second design too, with witnesses run on the
committed code. The 2^-1018 bound came from a typical-magnitude argument (the residual is
about 2^-53 times the operand) — but exactness is governed by the residual's **quantum**:
`a − q·b` is a multiple of 2^(eq+eb−104), representable only when the scale operand is at
or above ~2^-969. In the 48 binades between the two bounds the seat *constructed*
all-normal witnesses — significands chosen so `sq·sb ≡ 1 mod 2^51`, leaving the residual
a lone bit beneath the subnormal quantum — for div, sqrt, **and mul**, whose hole the
band redesign had silently re-opened (the deleted result band had been protecting it).
Random sweeps structurally cannot find these: the tail's probability is ~2^-51 per draw,
which is how 264 000 sweep checks and a green gate sat on top of the hole. The
constructed rows are now named vectors, with 2^-960 boundary controls proving the
corrected side, and the in-code comment carries the quantum derivation instead of the
magnitude heuristic.

The same seat found 2Sum's one exclusion: at the overflow-tie threshold (3·2^970 plus
−DBL_MAX gives a *finite* tie-to-even sum while `s − a` is infinite) the error term goes
NaN — and a NaN overshoot flag did not merely miss, under toward−Inf it stepped **away**
from the exact value. Guarded with accept-nearest, family pinned in both directions. It
also confirmed the D sub-arms' NaN-subtrahend sign change (the #299 class, MIPS immune)
— measured, pinned at the store's sign-preserving canonical NaN — verified the div-zero
fix it had independently derived, ran the full 25-site census clean (finding m88k's
`fdiv.dds` undecoded — a pre-existing gap on a legal encoding, indexed), and proved the
five gate-2 D rows it added all fail on the pre-guard build.

## Sixty-sixth round (#301) — cvt.d.l converted the integer before the rounding mode existed

One helper in `core/float_emul.c`, one wired site in `cpus/cpu_mips_coproc.c`, and a new
gate. First item of the post-queue backlog, flagged by a #300 panel seat with the witness
already recorded.

### The defect, and where it hid

`cvt.d.l` converts a 64-bit integer to a double. The conversion happened inside
`ieee_interpret_float_value()`'s L arm as a plain host cast — under the *host's* nearest
mode — before `fpu_op`'s CVT case ever saw the FCSR mode, and the D store is a pure
re-encode with nothing left to round. So for integers with more than 53 significant bits
the guest's rounding mode was never consulted. Reproduced on the arc rig with the guest
setting FCSR itself via `ctc1`:

```
2^53+1       toward +Inf   measured 4340000000000000    owes ...001
2^54+7       toward zero   measured 4350000000000002    owes ...001
-(2^54+7)    toward zero   measured c350000000000002    owes ...001
nearest rows and the small-integer control: correct
```

The scope fact that shapes everything else: **pmax raises Reserved Instruction on the
`ldc1`** — `cvt.d.l` is MIPS-III+, so the defect and its gate are arc-only, and the
R3000 rig is untouched by construction.

### An integer problem, solved in integers

Unlike #300 there is no fma and no residual lemma here: the discarded low bits of the
integer *are* the remainder, exactly. The helper counts significant bits; 53 or fewer is
exact and returns unrounded; otherwise it splits the magnitude into a 53-bit quotient and
a tail, and the mode decides on the tail — toward-zero keeps the quotient, the directed
modes bump it on their side, nearest compares the tail against half with ties-to-even.
The one carry (a bumped quotient reaching 2^53) is exactly representable, and INT64_MIN
is handled first because negating it overflows — it is −2^63, a power of two, exact.

The fix is wired at the MIPS CVT case only, from the raw source register: the shared
interpret arm is deliberately untouched, both because it feeds five CPU families and
because the queued subnormal-decode round owns that ground. `cvt.d.s` and `cvt.d.w` are
exact conversions and stay unwired. `cvt.s.l` — the L→S half — was deferred in the first
draft, and the panel overturned that; its section is below.

### The probe took four attempts, and the control row is why that was survivable

The first probe reported the defect REPRODUCED while measuring nothing at all — six
sentinel reads from guest code that had never run. Three real bugs, found one per run:
the rig is little-endian and the operand was laid out big-endian; the COP1 `fd` field is
bits 10:6, so the first encoding overwrote its own operand (`cvt.d.l r0,r0` — the
disassembler said so); and dropping one function bit turned the instruction into `sub.l`,
which computed x−x and stored the zero being read back. The row that caught every one of
them was the small-integer control: a probe whose control fails has measured nothing, and
no other row may be believed. That rule is now enforced in the gate itself — a dead
probe is a hard failure, never a quiet pass or a false REPRODUCED.

And the discipline cut the other way too: one offline vector failed against the *correct*
code, because the table had labelled 2^54+1 and 2^54+3 as ties. They are not — their
remainders are 1 and 3 of 4 — and the genuine ties (2^54+2 and 2^54+6, remainder exactly
half, opposite parities landing on opposite sides) replaced them. Absolute-answer tables
check the code and the table checks back.

### Verification

- **Gate 2**: 22 absolute-answer vectors — exacts, the first-decision integer in all
  four modes, negatives (where toward-±Inf swap roles), multi-bit tails, genuine ties of
  both parities, the carry row, INT64_MIN/MAX, zero. 0 failures.
- **Gate 12** (new): ten rows on the arc rig through the real decode path, guest-set
  FCSR, 10/10 — including the `cvt.s.l` witness — with the control row asserted by name
  so the wiring can never revert while the pure helper stays green (the helper-vs-wiring
  hole a #299 seat named).
- **Negative control**: the helper neutered to the old host cast fails **exactly the
  five predicted rows** — the directed rows whose answer differs from nearest, including
  INT64_MAX under toward-zero, where the cast rounds 2^63−1 up to 2^63 — and nothing
  else.

### The panel refused the deferral, and was right to

The brief deferred `cvt.s.l` — the L→S half — as "would double-round through the host
double, left for its own round." Two seats independently rejected that: `cvt.s.l` is
*decoded*, so a guest executing a legal instruction was getting wrong answers today, and
each seat brought its own witness class. One: `2^54 + 2^30 + 2` under nearest ties DOWN
twice — once at the double, once at the single — landing at `5a800000` where direct
rounding of the integer owes `5a800001`. The other: `0x400000bfffffffff` sits one *below*
a binary32 midpoint, the host double rounds it ONTO the midpoint, and ties-to-even then
picks the wrong upper neighbour. Both reproduced on the arc rig against the committed
build, control green, before any fix.

The repair is #299's own theorem pointed at an integer: `ieee_int64_to_double_odd()`
truncates the integer to 53 bits and, if inexact, forces the quotient's last bit odd —
round-to-odd can never land on a midpoint, so the ordinary single-precision store then
rounds correctly in every mode (53 ≥ 2·24 + 2). No carry is possible: only an even
quotient is ever bumped. Verified: 12 offline L→S vectors including both witness classes
and the INT64 extremes, 0 failures; the rig's `SL dbltie` row green through real guest
code; and the odd helper neutered to the host cast fails exactly the five predicted rows
— the two nearest-mode witnesses, the directed 2^53+1, the negative mirror, and
INT64_MAX under toward-zero — while every L→D vector stays green, because the two
helpers are separate by design.

### What the rest of the panel proved, and the paper-trail lesson — again

The two verification seats went further than the brief asked. One re-derived the entire
vector table by hand *and* by two independent oracles, swept the helper against an exact
oracle over eight million inputs at zero mismatches, hand-verified every probe encoding,
and confirmed the no-interaction claims (NaN plumbing, the #246 subnormal trap, #294's
store-side W/L rounding — `cvt.l.d` enters with fmt D and matches neither new arm). The
other built a **host-FPU oracle** — `fesetround` plus the hardware's own convert-from-int,
guarded against the rounds-57 fenv/CSE trap with volatiles and `-frounding-math` — and
differentialled both shipped paths against it over twenty million samples: zero
mismatches; then ran two mutants of its own (an RP-sign flip killed by exactly the
negative-operand vector the #298 lesson mandated, and an odd-force deletion killed by
three SL vectors, proving the sticky bit is load-bearing), re-ran gate 12 on the rig
itself, and audited gate 12 for checks that cannot fail — finding none, and correctly
classifying the one row-count check as a row-deletion tripwire rather than a behaviour
check.

The same seat blocked the commit over two comments — rightly. Both deferral comments,
written when `cvt.s.l` was still deferred, survived above the very arm that un-deferred
it: the file said "left to its own round" three lines above the wired code. The #270
honesty bar applies to comments exactly because they are the durable artifact; both are
rewritten, along with a vector comment that claimed a 4/4 rig instrument the repository
does not carry (the gate carries one rig row; the directed-mode behaviour is pinned
offline through the #292-validated store, and the comment now says precisely that).

And for the second round running, the panel's paper trail drifted: the review diff was
cut before the `cvt.s.l` half existed, so seats certified against a moving target and
said so. The remedy is the same as round 65's — the final state is what the gates,
mutants, and this block describe, and the commit is the artifact of record.

Two indexed notes from the seats, neither a defect in this round: some real silicon
(the VR4300 famously) raises Unimplemented Operation for L operands beyond 2^53 and lets
the kernel softfloat complete — architecturally the same FCSR-rounded value, and
GXemul's no-trap depth here matches its pre-existing modelling; and the helper's
`default:` arm folds LEGACY into nearest, which IS this conversion's legacy behaviour
(the host cast was nearest) — stated in the code now, so a future caller expecting
truncation from that constant reads the truth before relying on it.

One seat's closing added two demands that both landed. The FR=0 gap: every rig row ran
with Status.FR set, so the 32-bit-FPU pair-assembly that feeds the helper had no
end-to-end measurement — it rested on reading the code, "and this project's history is
precisely about reading versus measuring." Gate 12 now carries an FR=0 row — the same
witness with FR clear — measured green. And the LEGACY semantics clash: the header
defines LEGACY as truncate for the store entry points, while the int64 helpers fold it
to nearest, which *is* this conversion's legacy behaviour (the host cast rounded
nearest). One constant, two legacies; the clash is harmless only while no caller passes
it, which nothing enforces — so it is now stated outright at both sites, where the next
caller would look.

## Sixty-seventh round (#302) — the m88k truncations were raw C casts, and the third architecture has a third table

One shared mode-parametric ladder in `cpus/cpu_m88k_instr.c` serving the whole MC88100
float→int triad — `trnc` existed and was wrong; `int` and `nint` did not exist at all,
and executing either halted the emulator. Second item of the post-queue backlog, and the
second round running whose scope grew because the panel refused a deferral.

### The defect, and the survey that preceded the design

Both truncation handlers converted with `(int32_t) f1.f` — undefined behaviour in C for
NaN, ±Inf and out-of-range, so the guest-visible result was the *host's*: measured on
the committed build, every special case on both arms delivered x86's `0x80000000`, with
all seven in-range controls green. The same class #273 fixed on MIPS and #297 on SH — on
a rig that boots OpenBSD 7.7 to root.

### The contract took a primary-source hunt, and it is nobody else's table

For every *special* operand the MC88100 delivers no result itself: any operand with
exponent ≥ 30 takes the integer-conversion-overflow exception, reserved operands (NaN,
Inf) take the reserved-operand exception, and "since the instruction that caused the
precise exception is not executed, no result will be written" (UM §6.8.4). In-range
operands below the threshold convert directly in hardware — a seat caught the first
draft of this paragraph overclaiming "never" — and the trap window is deliberately
conservative: in-range values in [2^30, 2^31) trap too, and the handler completes them
with the correct result.

So the observable value belongs to the *guest's kernel*, and the guest this project
boots is OpenBSD: `m88100_fp.c` forces round-to-zero for trnc and lands in SoftFloat's
`float32/64_to_int32_round_to_zero`, which saturates —

```
NaN, either sign     7fffffff     SoftFloat forces the NaN's sign positive
+Inf, ≥ 2^31         7fffffff
−Inf, < −2^31        80000000
exactly −2^31        80000000     in range, explicitly guarded
```

The NaN row is the signature: **all NaN go positive** — not SH's all-NaN-to-`80000000`
(#297), not MIPS's all-`7fffffff`-for-everything (#273). Three architectures, three
distinct tables, which is exactly why cross-copying was named the hazard before design
began. Two honest wrinkles are on the record rather than smoothed over: Motorola's own
shipped BCS handler wrote a "nonsignaling NaN" *pattern* on true overflow — a different
contract, but not our guest's — and on the real kernel path fcr62 accumulates AFINV,
which this values-only fix states in its comment instead of modelling piecemeal (the
same scope call as #297 and #273, for the same reason).

### The fix, and why the NaN branch is load-bearing

A shared `m88k_toint_result(fv, rm)` — NaN first → `7fffffff` regardless of sign; then
round the double to an integral value under the requested mode (the #294-validated
exact-midpoint form, with the saturation applied to the *rounded* value, matching the
kernel completion, which rounds first and range-checks after); then the two saturations;
else the cast, now reachable only for integral values inside int32 by construction. NaN
*must* come first — it falls through both ordered comparisons as false, so without that
branch a NaN reaches exactly the raw cast this correction removes (the #297 lesson,
third appearance). Exact −2^31 merges into the ≤ branch, value-identically. For `.ss`
the operand was already widened single→double by the interpreter, so every int32
boundary comparison is exact. `trnc` calls the ladder with toward-zero, `int` with the
#298 fcr63 decode (swap included), `nint` with nearest.

Measured after the trnc fix: all 17 survey rows match the sourced table, controls
unchanged.

### Verification

Gate 11 grew fifteen rows — 40 total, PASS. The trnc six: **four
discriminators** (+Inf, the negative-NaN signature, the exact-2^31 double boundary, and
the positive double qNaN — a panel seat corrected the original count of three) whose
pre-#302 x86 answer differs, and two negative-side **host-independence pins** that
coincide with x86-UB today but would catch an aarch64 host's different saturation — the
same pin logic #297 used. The int/nint seven: mode-discrimination on 5.2 (toward-+Inf 6
against toward-zero 5), the sign-asymmetric −5.2 directed row (the #298 lesson), both
nint tie parities (2.5 → 2, 3.5 → 4 — catching a trunc-wired and a half-up-wired
mistake alike), the double-format int arm, and the shared NaN table through the new
instructions. Eight of the thirteen are asserted by name. The trnc mutant — the ladder
reverted to the raw cast — failed exactly the four discriminators (27 of 31 on the
pre-triad gate) while the pins stayed green, as x86-UB predicts.

### The panel refused to ship a third of a triad

The first draft indexed `int` (0x09) and `nint` (0x0a) — the other two thirds of the
MC88100's float→int triad — to the coverage-gap round. A seat refused: they are real,
correctly-disassembled instructions whose absence from the decoder sends a legal guest
instruction to `goto bad`, which **halts the emulator** — reproduced on the committed
build for both ("All machines stopped"), which is the round-53 lesson's definition of a
wrong answer, and the contract was *already sourced* in the same report (`int` honours
fcr63's rounding mode, `nint` forces nearest, both land in the same OpenBSD completion
and the same saturation table). The same refusal shape as round 66's `cvt.s.l`, accepted
for the same reason.

So the ladder generalized to `m88k_toint_result(fv, rm)` — round the double to an
integral value under the requested mode first (the #294-validated exact-midpoint form;
the saturation applies to the *rounded* value, matching the kernel, which rounds first
and range-checks after), then the same table. `trnc` calls it with toward-zero, `int`
with the #298 fcr63 decode, `nint` with nearest, and the decoder grew the two cases
mirroring `trnc`'s, odd-register double guard included.

### The verification seat's census, and the honest victim accounting

The final seat approved after a differential of its own — an exact Python mirror of the
new function against an independent SoftFloat-style reference sharing no code with it:
all thirteen row values re-derived, fifty-four adversarial edges, and 1,040,000 random
comparisons across all four modes at zero divergence, plus every named mutant failing
exactly the rows the comments claim. Three of its findings landed before commit: a
fossil "31 =" in the gate's row-count comment, the missing double-inclusion guard on the
new helper (its neighbour `m88k_fp_rm` established the idiom), and the one handler in
the triad no instrument executed — `nint.sd` — which now has its own row (39 total).

Its census of the shipped guest image is the round's honest victim accounting. `trnc`
appears about 3,500 times as real compiled code in the OpenBSD/luna88k world — the m88k
compiler emits it for every float→int cast — so the raw-cast defect had *ubiquitous*
organic victims: any userland cast of a value ≥ 2^31, or of +Inf or NaN, returned
−2147483648 where the kernel completion owes +2147483647, a sign-flipped answer in
ordinary code. `int` and `nint`, by contrast, appear **only as data** — assembler opcode
tables, termcap, DWARF bytecode — never as executed instructions. So the halt fix
protects against hand-written assembly rather than shipped code: the guest's own
toolchain puts the instruction one line away, and before this round that one line
stopped the whole emulator. A real defect, fixed with its thinness stated rather than
dressed up.

## Sixty-eighth round (#303) — every subnormal decoded wrong, on every architecture at once

One correction in `core/float_emul.c`'s `ieee_interpret_float_value()`, the decode
half of the module whose store half rounds 51–67 rebuilt. The widest blast radius of
the campaign: five CPU families consume this function for every S/D operand, and
before this round every subnormal bit pattern — all 2×8,388,607 single-precision
magnitudes, exhaustively — decoded to garbage.

### The defect

The S/D arm added the implicit leading 1 and used exponent `-bias` for every nonzero
finite input. A subnormal (biased exponent 0, mantissa m ≠ 0) has neither: its value
is `(m/2^frac)·2^(1-bias)`. The committed decode returned `(1+m/2^frac)·2^(-bias)` —
S 0x00000001 read as 5.877e-39 where the true value is 1.401e-45, a factor of 4.19
million; the worst D ratio is 2.25e15; the maximum D subnormal decoded as exactly
DBL_MIN, a NORMAL; and D m=3 and m=4 COLLIDED onto one host double (the garbled
ideals sit half a grid step apart and the decoder's own last halving rounds them
together — the committed loop rounded; the fixed one is exact, a property it
acquires because true subnormals are grid-aligned).

### Who consumed it — the panel refuted the masking claim and the rigs agreed

The pass-1 brief claimed MIPS was fully masked by #246's denormal trap. Two seats
independently refuted it from the code — `fpu_unimpl_trap()` returns 0 for EXC3K
because the R3010 signals through an external interrupt pin the emulated machines
never wire — and the rig settled it: pmax/R3000 stored `0x32000001` for
S-min × 2^100 (the garbled product, bit-exact with the offline oracle), while
arc/R4000 kept its `0xdeadbeef` sentinel (the trap fired; the store never ran). So
the measured victim list is m88k (every FP operand, on a rig that boots OpenBSD to
root), SH, Alpha, PPC — where `lfs` alone puts the garbled widening straight into
the FPR, no arithmetic involved — and pmax, our primary rig. arc is the no-change
control. A third seat's census found the two `dev_pvr.c` framebuffer decoders too
(13 sites, Dreamcast vertex data; no rig, cosmetic).

### The fix

Save the biased exponent where the unbiasing destroys it, then one branch at the
implicit-bit site: biased 0 → no implicit 1, exponent `1-bias`. Three lines of
mechanism; W/L arms, the zero check and the Alpha exponent-1024 hack untouched.
The guest-visible contracts this lands on are the ones the guests own: MIPS R3000
and m88k kernel completion compute exactly this decode; PPC hardware computes it
directly; SH is now a stated MIXED contract — operands per DN=0-with-completion,
subnormal results still flushed by the deliberate #287/#292 store policy — one gap,
named in the source, so nobody fixes half of it. The store side is untouched: its
flush is documented policy whose per-arch encode contract the queued store round
measures before changing anything.

### Verification — every byte pinned live before the fix, every transition measured after

Offline (gate 2, 23 → 30 checks): exhaustive S both signs, 400,010 D rows, the
m=3/m=4 collision row, 27 controls, and an FTZ/DAZ + rounding-mode canary built
from volatile operands — a constant expression would fold at compile time and pass
on exactly the poisoned build it exists to catch (a seat's demand, like the
generated-Makefile fast-math grep that closes the `CFLAGS=-Ofast ./configure` hole
the script-level grep cannot see). The mutation self-test grew mutant `revert303`,
defined as force-the-normal-arm after a seat proved deleting the branch body is
algebraically a no-op mutant; it fails exactly the interpret rows.

Rig rows, every committed-side byte measured live before the fix landed: m88k
(gate 11, 40 → 46 rows) — both fmul signs (0x32000001/0xb2000001 → 0x27000000/
0xa7000000), the fmul.dss widen with s2 pinned at 1.0f, the fmul.ddd scale row
whose committed byte 0x3E80000000000000 was settled three independent ways after
BOTH seats' pass-1 arithmetic had it one ulp wrong, and fcmp.ssd against a D
comparand inside the (true, garbled) gap — the ONLY discriminating compare shape:
the garble maps subnormals monotonically into (0, FLT_MIN), so every same-format
compare preserves order (a seat's band theorem, conceded and then sharpened by the
collision case). SH (gate 10, 34 → 36 pairs): fmul and fdiv rows that STRIP the
probe's DN=1 default — a numeric true-IEEE expectation under DN=1 would bless a
value real silicon flushes (the seat that caught it also pinned RM=RN in the same
write; SH-4 resets to round-to-zero). MIPS (gate 12, 11 → 15 rows): pmax mul.s and
cvt.d.s discriminators plus the arc trap control.

Two rows are pinned KNOWN-CHANGE, not failures — and they run on the NEGATIVE
operand, because the diff-review pass caught the positive form overclaiming: m88k
fmul.sss(−S-min, 2.0) and pmax add.s(−S-min, −S-min). The garbled product landed
S-normal (the positive twin measured 0x00800001 pre-fix; the negative one is the
same path with the sign applied last); the true result −2^-148 is subnormal and
takes the deliberate #287/#292 store flush to MINUS zero — the sign #287
preserves. A positive row reads +0 under both the old and the current store and
cannot see a #287 revert at all; the negative row trips a revert of EITHER
correction. They are the before/after evidence the queued store-side round
inherits.

### The panel

Four seats to concurrence in two passes — Codex xhigh, agy, and a Fable agent,
with GLM-5.2 seated for the fourth after Kimi wedged twice (alive, near-zero CPU;
stopped, relaunched, replaced). Every factual dispute was settled by measurement,
not vote: the masking refutation (above), the compare-witness refutations (the
original fcmp threshold was itself subnormal — both builds answer "less"), the
one-ulp committed-byte correction both its authors retracted, and eleven live
probe rows across four rigs that matched their predictions bit for bit. The PPC
lfs row ran once more on the fixed build (0x36a0000000000000, control clean) per a
seat's demand; its permanent gate row lands with round 69's PPC gate.

The DIFF then took its own four-seat pass: three SHIP, one FIX with four findings,
all adopted and re-measured — the arc trap row gained an integer-store execution
witness (a dead session previously left the same sentinel the trap does: the
project's own load-bearing-control rule, turned back on this round); gate 12's
late skip could discard failures the first section had already recorded (inputs
now preflighted, no-result is a failing check); the flip rows went negative
(above); and two canary comments claimed coverage of the generated-Makefile hole
that only the grep can see (narrowed — the canary is the HOST-level defence). A
SHIP seat added two one-line hardenings: a check_min on the D population and the
why-comment on the unpinned L INT64_MAX.

## Sixty-ninth round (#304, #305) — the PowerPC narrowed with a host cast, and threw away every NaN it touched

Two corrections in `cpus/cpu_ppc_instr.c`, and the gate that had to exist before
either of them could be believed. This is the architecture with no OS rig: nothing
boots on the PowerPC path, so every defect here was found by a cold-debugger spike
and each one is worth exactly what its instrument measured.

### Gate 13 came first, and it caught three of my own predictions

Fifty rows across `frsp`, `stfs`, `stfsx`, `lfs` and the composed store sequence a
compiler actually emits, run against the **committed** build before a line of the fix
existed, with every byte recorded. That baseline is what makes "the fix worked" a
measurement rather than a claim — and it immediately refuted three rows of my own
table: `frsp` of 2^128 under round-to-nearest gives Infinity, which is *correct*
(nearest overflows to infinity, so that row is a pin, not a defect); the negative
band row keeps its sign through the flush, because #287 fixed exactly that; and the
overflow row I had wanted at the pattern of 2^128 itself, a value no correct
implementation can produce. The emulator was right and the annotation was wrong,
three times, before any code changed.

### #304 — the mode the FPU never read, and the band it flushed

`frsp` narrowed with `float fl = frb.f` — a host C cast, which rounds to nearest
whatever FPSCR says. Three of the four architected modes were unreachable, so a
guest that set toward-zero got nearest anyway. The same cast handled the ISA's
denormalization band, and `stfs` did not handle it at all: the shared store's
documented flush answered signed zero across the whole band where Book I's
`SINGLE()` spells out a shift-and-truncate. And the NaN arm was worse than
mode-blind — it left `fl` at its initialiser, so **every NaN became +0.0**.

The fix is one PPC-local helper doing exact bit surgery on the significand: shift,
collect guard and sticky, decide once from (guard, sticky, lsb, sign), then increment
— and let the carry run out of the fraction into the exponent, which is how a
subnormal at the top of the band becomes the smallest normal and how the largest
finite single becomes Infinity, with no special case for either. `frsp` calls it with
`fpscr & PPC_FPSCR_RN_MASK` (a define this header never had; the encoding is
numerically identical to this project's `IEEE_RM_*`, verified rather than assumed);
`stfs`/`stfsx` intercept only the band and leave every other finite value on the
proven legacy path, because the legacy path already reproduces the splice bit for bit
and reproving the whole domain buys nothing.

### #305 — a NaN's payload is data, and the value domain cannot carry it

`lfs` and `stfs` converted through `interpret → host double → store`. That pair
reports only *that* a pattern is a NaN and then canonicalizes it to all-ones, so a
guest's `0xffc00001` arrived in the register as `0x7fffffffffffffff` — wrong sign,
wrong payload — and came back out of a store as `0x7fffffff`. Both measured. The
class is exactly decidable (exponent all-ones, fraction nonzero) and disjoint from
the finite path, so it is handled by pattern surgery on all four instructions:
truncate to what a single can hold on the way down, shift back on the way up. The
store does **not** quiet — quieting belongs to `frsp` alone, because a store must not
alter the class of what it stores — and a signalling-NaN row plus a collapse row
(a NaN whose payload lives entirely in the discarded bits splices to the *Infinity*
pattern, which is the extraction working as specified) keep an over-eager quiet bit
unshippable.

### Verification

All twenty-five discriminators flipped to bytes registered **before** the fix
existed, on the first run, with no byte adjusted after seeing a result; all
twenty-five pins held. The control rows prove `msr=0x2000` took, without which every
FP instruction raises FPU-unavailable and the probe measures nothing.

Then the diff review found three defects in the round's own work, and the last of
them was the most instructive. `frsp` had been *setting* `VXSNAN` and then clearing
it on the next non-NaN conversion — the bit is sticky in hardware, so
`frsp(sNaN); frsp(1.0)` erased the record, which is worse than never setting it; it
now sets the bit with its `VX`/`FX` summaries and never clears them, with a row that
runs exactly that sequence. `lfsx` was fixed but untested, so deleting the fix would
still have scored a clean sweep; it has its own NaN-payload row now. And the check
that was supposed to prove each rounding-mode write took **had never once worked**:
it parsed the debugger's plain `reg`, which does not print FPSCR on this CPU at all,
so every run reported "0 bad" out of readbacks that never parsed. A seat predicted
the hole from the code; the rewrite then measured it, forty-three rows of *unparsed*.
The replacement reads FPSCR the way a guest does — `mffs` into memory — and proves
the channel once per mode in its own session, because the first repair put that read
inside every row and its dump interleaved with theirs, corrupting one result and
losing twenty reads to straggle. Both numbers are asserted now, since "0 bad" and
"read nothing" are otherwise the same answer.

A fourth check was wrong in the same family: a name-anchored row count matched
`frsp qNaN` against `frsp qNaN payload` and counted two.

Final instrument: 54 rows — 25 discriminators, 25 pins (two of them policy pins
recording a deliberate divergence from the letter), one divergence row for
`fctiwz`'s NaN, the sticky-`VXSNAN` sequence, and the indexed load and store forms —
31 gate checks, all green.

### What the panel refused, and what it settled

The scope grew and shrank in review. A seat measured that the old "finite values
above 2^128 wrap" entry does **not** reproduce — #287 already gives Infinity there —
so it closes as a pin rather than a fix. Against that, the literal Book I splice
*would* wrap the exponent for finite values around 2^129, and the panel voted 3–1 to
keep #287's Infinity as deliberate policy: the letter turns a finite overflow into a
NaN pattern (1.5·2^128 → `0x7FC00000`), which is worse than the divergence. The
dissent is recorded rather than smoothed away.

The NaN round went the other way. One seat wanted it deferred and had the better
argument until the defect was measured; once `lfs` and `stfs` were shown destroying
payloads on the rig, the seat that proposed deferring flipped its own vote — its
position had been explicitly conditioned on there being no measured victim. The tie
broke on the same ground round 67 used when it refused to ship a third of a triad:
pinning bytes that are already scheduled to change manufactures a known-wrong
intermediate.

Filed, not fixed: `mtfsf`'s FM-mask stride (its nibble masks are built at an 8-bit
stride, so most of the register is unreachable through it — which is why this gate
sets the mode through the debugger and verifies it through `mffs`), the
single-precision arithmetic family (`fmuls` is a no-narrowing alias of `fmul`),
`fctiwz` of a NaN answering 0 where the ISA owes `0x80000000` (pinned here as a
divergence row so it cannot drift), the update-form loads and stores that are not
decoded at all, and the exception-enable bits nothing sets — the enable side of
`VXSNAN` included, so nothing above should be read as a working trap model. Each has
a round with its name on it.

## Seventieth round, part A (#306, #307, #308) — a family of legal instructions that stopped the machine

Two corrections in the m88k core, both of the class this project keeps finding: an
encoding the manual defines, the decoder rejects, and `goto bad` turns into
`cpu->running = 0`. A guest that executes one gets "All machines stopped" instead of
an answer.

### #306 — the decoder implemented whichever format combinations its guests happened to run

The size field of a major-0x21 floating-point instruction is a format *triple* —
(s1 is double) << 4 | (s2 is double) << 2 | (destination is double) — so each of
`fadd`, `fsub`, `fmul` and `fdiv` has eight legal forms. This tree had five or six of
each, and the gaps were not principled: `fsub` had `.sds` while `fadd` did not,
`fdiv` was missing four. They had been added over the years as guests demanded them,
which is exactly why a census beats a bug report. Twelve combinations were missing;
six were measured halting the emulator on the luna88k rig before the fix, spanning
all four instructions.

Each new handler is its sibling's body with the operand and result widths changed,
because the arithmetic contract does not vary with the triple: sources are
interpreted in their own formats — a double source is never pre-narrowed because the
destination happens to be single — the operation happens once, and the result is
rounded once, into the destination format, under fcr63's mode.

### #308 — the same witness fired twice, and the second time was worse

The first draft of the single-destination products and quotients copied `fmul_sss`
and `fdiv_sss`, which compute in host double and round at the store. A panel seat with
the MC88100 manual refused that and registered a counterexample *before the code was
tested*: `fmul.ssd` of 3.0f by the nearest double to 1/3. The exact product is just
below 1.0; the host product ties to exactly 1.0; a toward-zero store then answers
`0x3f800000` where a single correct rounding owes `0x3f7fffff`. It failed exactly
there.

The reason is worth stating plainly, because it is the whole lesson: those siblings
are safe *because* two single sources make the product exact in a double, so their
store rounds once. A double source voids that argument. "Copy the sibling" is only
sound when the sibling's correctness *argument* survives the change.

The second draft routed the six arms through #300's `_rm` residual helpers — and the
same seat caught that those **return the host result unchanged under round-to-nearest**,
since for a *double* destination the host's nearest result already is the correctly
rounded one. Narrowed to single, that is a double rounding again, and nearest is the
mode OpenBSD/m88k userland actually runs (fcr63 is zero at exec). Two more constructed
witnesses, both measured: `1.5f × 0x3FF555556AAAAAAB` gave `0x40000000` for the owed
`0x40000001`, and `0x3F800001 ÷ 0x3FF000000FFFFFF0` put the host quotient exactly on
the 1+2⁻²⁴ midpoint, giving `0x3f800000` for the owed `0x3f800001`. The first witness
set could not have found these: it only discriminated the directed modes.

So #308 adds the multiplicative twins of #299's sum helper — `ieee_mul_round_to_odd()`
and `ieee_div_round_to_odd()`, over the fma and Markstein residuals — and the six arms
now pass no mode to the arithmetic at all, only to the store. Round-to-odd fixes every
mode at once: with 53 ≥ 2·24 + 2 an odd intermediate can never sit on a destination
midpoint, so the narrowing store rounds once by construction.

The first attempt at the helpers had the step direction inverted, which the rig
reported immediately by *regressing* the directed rows that had been passing — the
witness set doing its job in the other direction. The repair was to stop hand-rolling
the bit arithmetic and reuse the file's own `overshoot` convention and `ieee_dir_step()`.
Verified three ways: all four rig witnesses, an offline differential against a single
correct rounding over 960,000 operand pairs in all four modes with zero mismatches, and
the gate rows themselves.

One filing was withdrawn in the same review. `fdiv_sss` had been recorded as carrying
this defect on the grounds that a quotient of two singles is not exact — but inexact is
not the same as double-rounds-wrong, and by the exclusion-zone argument its error can
never reach a single-precision midpoint. 400,000 random single÷single quotients found
no disagreement. The six arms this round introduced were the only ones that genuinely
had the hazard.

### #307 — `tcnd` was absent entirely, and upstream's own patch would not have fixed it

Trap-on-condition was not in the decoder at all, so every form halted the machine.
The abandoned 0.7.1 line upstream had added a narrow patch: treat `tcnd ne0,r0,x` as
a no-op, since r0 is never nonzero, and leave the rest halting. A seat refused to
adopt it and was right twice over — `tcnd eq0,r0` still reaches `goto bad`, and
`0 == 0` is precisely the case that must trap; and in user mode a trap to a hardware
vector owes a privilege violation whether or not the condition holds, so no-oping is
wrong there even for its own case.

The semantics are derived, not invented. The manual gives the condition field as a
mask over four mutually exclusive classes of the source register — maximum negative,
less than zero, equal to zero, greater than zero — where the zero test is the NOR of
the low *thirty-one* bits, which is what makes `0x80000000` its own class. All nine
entries of the disassembler's own condition table agree with that reading. The trap
itself is `tb0`/`tb1`'s body verbatim, including the privilege check before the
condition, which the manual retroactively confirms was the right order there too.
Disassembly was added as well, so the instruction no longer prints as UNIMPLEMENTED.

### Verification

Gate 11 grew from 46 rows to 71 and now runs 59 checks. Eighteen rows cover the new
format arms — one per instruction and format class, the register-pair word order on
the double-destination divide, a directed-mode row through the divide path, and the
three `fmul.ssd` mode rows that caught the double rounding. Seven rows cover `tcnd`,
and they measure a *trap*: the witness is the program counter after one step, since
a taken trap lands at VBR + 8·vector and an untaken one advances by four — and either
outcome proves the emulator survived, which is the whole point. One of those rows
pins the mask-not-enumeration reading by using a condition value with the reserved
bit set, and another pins the low-thirty-one-bit zero test by distinguishing
`0x80000000` from `0x7fffffff`.

The vector is 128 or above on purpose. The first version of the probe used vector 0,
which is RESET — the trap was delivered correctly and the machine reset, and the row
read a correct answer as a failure.

### What went to its own round

The four guest-reachable `exit(1)` calls in `dev_wdc.c` were reproduced in the same
sweep — a guest doubleword store to the data register kills the emulator outright,
with no message at all — but they ship separately, by panel verdict: the m88k work
has complete primary-source semantics and an existing instrument, and a single green
round should not let deterministic decoder fixes mask an under-specified device
change. That round also inherits a read-path twin of the same defect, found by the
same seat two lines from the write one.

## Seventieth round, part B (#309, #310) — two more decoders that stopped the machine

The same class as part A, on the two architectures it had not yet been swept on.
`goto bad` in a dyntrans decoder reaches a shared label in `cpu_dyntrans.c` that
prints "UNIMPLEMENTED instruction" and sets `cpu->running = 0` — so on every
dyntrans architecture, an encoding the decoder lacks stops the emulator rather
than faulting the guest.

### #309 — an unimplemented MIPS REGIMM sub-opcode halted instead of raising RI

REGIMM's `default` arm ran `fatal()` and fell into `goto bad`. The implemented
sub-opcodes are the branches, the trap-immediates, the branch-and-links and three
CPU-specific ones; everything else — rt = 4–7, 0xd, 0xf, 0x14–0x17, 0x1a–0x1e —
stopped the machine. Real silicon raises a Reserved Instruction exception, which
is what the guest kernel is written to handle.

Reproduced on both rigs with rt = 0x15, and again with 0x1e; BGEZ ran throughout
as the control. The repair is the tree's own shape from two arms above, where
trap opcodes on a pre-MIPS32 CPU already resolve to `instr(reserved)` behind a
latched warning — and it is the same conclusion upstream reached independently in
the 0.7.1 line it never released. The warning is latched rather than
verbosity-gated because it reports a deficiency of the emulator, which #279
argues should survive one quiet run; speculative decode still takes the old path,
because readahead must not warn at all.

### #310 — the float update forms were absent, and the family was twice the size reported

`lfsu`, `lfdu`, `stfsu` and `stfdu` were not defined in `opcodes_ppc.h` — the
header had blank lines exactly where their primary opcodes belong — and not
decoded anywhere. All four halted.

The round would have shipped four fixes if a panel seat had not demanded the
*indexed* twins be checked first, on the principle part A established: a compiler
emits `lfsux` from the same loops that emit `lfsu`, so fixing half a family
leaves the other half stopping the machine. The seat was right that they needed
checking and wrong about which encodings they are — 599 and 663 are `lfdx` and
`stfsx`, which this tree already decodes. The update forms are extended opcodes
567, 631, 695 and 759, none of which appeared anywhere in the tree, and all four
were then measured halting too. Eight, not four.

Each is its non-update sibling plus "rA receives the effective address", which
the generic load/store tables already implement, so the handlers differ from
`lfs`/`lfd`/`stfs`/`stfd` by one array index and inherit #304's and #305's
conversion work unchanged.

The two dispatch tables are not the same shape, and that cost a compile: the
D-form table carries a zero-displacement dimension and encodes update at +32,
while the indexed table has no displacement at all and encodes it at +16 in only
32 entries. The first draft used the D-form's term for the indexed handlers,
which reads past the end of the array; `-Warray-bounds` reported it as an
out-of-bounds subscript and the build failed. Without that warning it would have
been a call through whatever followed the table.

### Verification

Gate 12 grew five rows and gate 13 grew eighteen. The MIPS rows assert the
*outcome* rather than a register: "RI" for the unimplemented sub-opcodes, and a
memory witness for the BGEZ controls — the guest stores one marker on the
fall-through path and another at the branch target, so taken, not-taken and
nothing-ran are three distinguishable answers. Both rigs run every row, because
a fix reaching only one dyntrans mode would pass a single-rig gate. The PowerPC
rows give each of the eight forms both halves of its contract, a value row and a
base-register row, and two non-update rows assert the mirror image — that the
base is unchanged — with nonzero displacement and index, so an implementation
updating everything fails as loudly as one updating nothing.

Those rows reached that state through a diff review that found three of them
unable to fail. The two non-update controls used a zero displacement, which
makes the effective address equal the base, so a wrongly-updating implementation
would have written back exactly the value the row expected. Five of the eight
forms had a base row but no value row, so a wrong transfer size that still
advanced the base would have passed. And the MIPS classifier returned a
catch-all "ran-no-exception" for every outcome that was not exactly RI or a
halt, which meant a timeout, an EOF or a different exception all scored as
success — while BGEZ, tested with a zero offset, would have been satisfied by a
nop. Each is the same species of defect this harness exists to catch in the
emulator, and each is recorded next to the row it produced.

Those rows needed a register plan before they measured anything. The first
version used one register as both the index and the publish base, and published
through an instruction whose operands were reversed, so several rows reported
whichever value happened to survive. That is recorded in the probe next to the
plan, because the failure looked exactly like a broken fix.

### A claim this round withdrew

The reach of #310 was first argued from a census of the NetBSD/macppc kernel
that reported hundreds of update-form instructions. A seat re-ran it against the
ELF's section metadata rather than the broad read-write-execute segment and got a
different answer, which an independent parse then reproduced exactly: in that
kernel's executable text there are 34 `lfd`, 36 `stfd`, and **none** of the eight
update forms. The earlier count was data.

So the prevalence claim is withdrawn rather than softened. What justifies #310 is
what was always exact: eight legal encodings, measured stopping the emulator, in
a family whose other half this tree already implements. The methodology that
produced the bad number is recorded too — executable-section census first,
disassembly validation second, whole-image scanning only as reconnaissance.

## Seventy-first round (#311, #312, #313) — ARM: two wrong flags and one more halt

The first ARM round in this fork, and the first work on the architecture at all,
so it opens with an instrument: `testarm`/SA1110 under the cold debugger, guest
flags read by the guest's own `mrs`, 58 rows and 51 checks in gate 14. The machine needs a file
argument to construct — it prints usage and exits without one — so a four-byte raw
stub is loaded and immediately overwritten. Memory is little-endian here, the
opposite of the PowerPC rig, and every word the probe reads is byte-swapped back.

All three defects were reproduced on the committed build before anything was
edited. That sweep scored 39 of the 56 rows the table held at the time, failing in
exactly the 17 places the fixes were predicted to flip and nowhere else. Two pins
covering the PC-as-operand path were added afterwards and pass either way, so the
same build on the final 58-row table reads 41/58; the number is given both ways
rather than restated as the tidier 39/58, because it is evidence.

### #311 — the subtract carry ignored the borrow it had just subtracted

`cpu_arm_instr_dpi.c` computed the carry-out of every subtract-family instruction
as `a >= b`. ARM's subtract carry is NOT-BORROW, and for SUB, CMP and RSB that
formula is exactly right. But SBC and RSC compute `a - b - NOT(C)`, which borrows
whenever `a <= b`, so the correct flag is `a > b` — and the two disagree precisely
when `a == b` with the carry-in clear. There, `a - a - 1` borrows and the emulator
claimed it had not. Subtracting equal values is the ordinary way multi-word
arithmetic produces a zero limb, so this is not an exotic input.

The result register was always correct; only the flag was wrong, which is why
every value row in the gate is a pin rather than a discriminator, and why a fix
that repaired the flag by disturbing the arithmetic would fail the gate.

The repair takes the flag from the full 64-bit result the file already had in
hand, `c32 == c64` — the mirror image of the add arm's `c32 != c64` two lines
below. Because both operands are zero-extended from 32 bits, a subtraction that
did not borrow lands in `[0, 0xffffffff]` and equals its own low half, and one
that did wraps with the high bits set. That equivalence is what makes the change
safe for the three instructions that were already right, and the gate pins all
three rather than trusting the argument.

One panel seat proposed `(uint32_t)c64 == c32` as a more defensive spelling. It is
a tautology — `c32 = c64` is the assignment on the line above — and would have set
the carry unconditionally on every subtract and compare in the emulator. It was
caught by a second seat and by the reasoning, not by a test, which is worth
recording: the rig would have caught it too, but only because the pins exist.

### #313 — ADCS could clear the overflow flag but never set it

Found by a panel seat reading the `#if` nesting rather than the logic. `A__ADC` is
named in the outer guard that CLEARS V and recomputes it, but matched neither
inner formula — not the `ADD || CMN` arm, not the `SUB || RSB || CMP || RSC ||
SBC` one. So `v` stayed 0 and `ADCS` could only ever clear V. Of the eight
opcodes in the outer guard, ADC was the only one missing from an inner arm.

Measured: `ADCS 0x7fffffff + 0` with carry-in gives `0x80000000` with V clear,
while `ADDS` with the identical overflow correctly sets it. That pairing is what
makes the gate rows a statement about ADC rather than about V in general.

The fix adds ADC to the add arm. The sign rule stays exact with a carry-in
because it reads the actual result: operands of opposite sign cannot overflow
even when 1 is carried in, and operands of like sign overflow exactly when the
result's sign differs from theirs — the dual of why the subtract arm was already
correct for SBC and RSC.

### #312 — the undefined instruction space stopped the emulator

The same halt class as #264, #309 and #310. Unmatched encodings in the
`main_opcode >= 6, bit 4 set` space reached `goto bad`, which sets
`cpu->running = 0`. On the ARMv4 this models that whole space is architecturally
undefined, and it contains ARM's permanently-undefined encoding and the word GDB
plants for breakpoints; real silicon raises the Undefined Instruction exception.

The sharpest form of the defect is that the halt happened during DECODE. A
*conditional* undefined word whose condition was false — an instruction the guest
would never have executed — stopped the emulator anyway. That is measured, and it
is the row in gate 14 that states the reachability most plainly.

The witness is the handler, not the absence of a message: code planted at the UND
vector stores a marker, the mode and the return address, so a row cannot pass by
the instruction being quietly ignored. One row places the undefined word in the
last slot of a 4KB page, because `X(und)` reconstructs the faulting PC with a
hard-coded page mask whose arithmetic is entirely zero at offset 0 — a panel
seat's point that the obvious placement tests nothing.

The tree already contained the right routing for this, a few lines below, with a
comment naming GDB's breakpoint. It was unreachable: its predicate is bit-identical
to the enclosing block's guard, and every path through that block breaks first. All
four panel seats verified that identity independently — one additionally checked the
all-paths-break property the identity argument silently assumes — and three of the
four recommended deleting rather than annotating, which is what was done, with the
GDB rationale moved to the live path.

Encodings that are not the permanently-undefined pattern warn once before routing,
since they may be an extension nobody has implemented rather than a true
undefined; the true pattern is silent, because a guest executing it is not a
deficiency of the emulator. Speculative decode still takes the old path, which
both keeps the prior rounds' shape and preserves the warning for the real pass.

### What the diff review caught, all of it in the instrument

The three corrections came through review unchanged. Everything the seats found was
in the scaffolding around them, which is worth stating plainly because it is now the
third round running where that has been true.

**Two of gate 14's checks could never have passed.** The gate matches each named row
with two spaces after the name, so that a name which is a prefix of a longer one
cannot match both. But the probe padded names to a 26-wide column that was then 24
wide, and two names — `udf gdb-form handler ran` and `udf page-end handler ran` —
are exactly 24 characters. A name as long as its column gets no padding at all, so
only the format's single separator space follows it, and those two checks could match
nothing. Gate 14 would have reported FAIL on a fully correct build.

This is the exact mirror of the trap the gate's own comment says it is avoiding, and
the audit run here for prefix collisions did not catch it, because it was looking for
names that match *too much*. The seat that found it also observed that the 58/58 had
only ever come from running the probe directly — the gate script as a whole had never
executed end-to-end, so nothing had exercised the checks themselves. It has now, and
the column is 26 with the invariant written down next to it.

**The two new files were untracked.** `gate_arm.sh` and `arm_flags_probe.py` were
never added to git, so they did not appear in the diff under review and a commit of
tracked changes alone would have left `run.sh` invoking a gate that does not exist.
Caught by a seat that noticed the reviewed patch could not reproduce the result the
patch claimed.

**The `A__PC` corner was promoted from a note to a fix.** Three seats raised it and
one classified it as a regression this round would introduce rather than a
pre-existing corner, which is the correct reading: it is a case where the old test
was right and the new one would not be. Truncating the reconstructed PC operand to
32 bits is correct on its own terms — ARM's PC is 32 bits and reading it must wrap —
so the fix is not a workaround for the new carry test, and it also removes a spurious
carry the ADD family has been reporting at those two addresses since long before this
round. For every operand below 2^32 it is a no-op, which is every operand these rigs
can reach; the top-of-address-space behaviour it corrects is reasoned, not measured,
and is labelled as such in the code.

### Recorded, not fixed

- **The `A__PC` operand at the very top of the address space.** When Rn is PC the
  template recomputes the operand as page base + slot + 8 in 64-bit arithmetic,
  which exceeds 2^32 for the last two instruction slots of the 4GB space. There
  the old truncating test was right and `c32 == c64` would not be. It needs RAM
  mapped at `0xfffff000`, which no rig here has, so it is documented rather than
  fixed blind — this project does not change what it cannot test. The same corner
  already affects the ADD family identically and predates this round. A pin row
  covers the reachable part of that path.
- **Three more halts in the same decoder**, found by the panel while reviewing
  #312: `uxtab` and `uxtah` with a non-zero rotate, and a data-processing
  immediate path that rejects a legal non-canonical rotated immediate. These are a
  different sub-case — the decoder recognises the instruction and rejects only an
  unimplemented variant, so routing them to "undefined" would be its own kind of
  lie — and they get their own round.
- **The media encodings decode on every ARM model**, including the ARMv4 this rig
  runs, where silicon would raise Undefined. Pre-existing, a fidelity question
  rather than a halt, and deliberately not entangled with #312.

## Seventy-ninth round (#314) — SuperH answered a legal instruction by stopping

The round opened as "decode `synco`" and the panel turned it into something else
entirely, which is the second time in three rounds that reviewing a narrow fix
found the wide one underneath it.

`synco` (0x00AB) really is undecoded, and it really does stop the emulator: the
`main_opcode == 0` switch has no case for it, so it falls to a `default` that runs
`fatal()` and `goto bad`, and `goto bad` reaches the shared label in
`cpu_dyntrans.c` that sets `cpu->running = 0`. Measured on the landisk rig before
anything was edited.

The proposal was to add two `case` labels decoding `synco` and `prefi` as nops.
Three things killed it:

**The premise was false.** The diff justified itself by saying `PREF` (0x83) is
already treated as a nop. It is not — `pref_rn` is a 57-line store-queue writeback
engine that bursts to a QACR-derived external address and raises its own exception
for prohibited user access. Two seats caught it and the source confirms it. The
same objection applies to citing `MOVCA.L`: its existing nop silently drops a
guest-visible store, so it is a live bug, not a precedent.

**The CPU model is wrong for the fix.** This tree defines SH7708R and the
SH7750/7750R/7751R only — there is no SH-4A model, and landisk instantiates an
SH7751R. `synco` and `prefi` are SH-4A instructions, so on every core this emulator
can build they are *reserved encodings*. Decoding them as nops would have made an
SH-4 execute SH-4A instructions silently.

**Two encodings was a rounding error.** A sweep of legal encodings found eight that
stop the emulator, and three of them — `MAC.L`, `MAC.W` and `TST.B` — are BASE ISA,
present since SH-1/SH-2 and unambiguously legal on the modelled part. No argument
about extensions applies to those; the tree simply lacks them, and lacking them
killed the machine.

So the fix is the one this fork has already made three times: the ten
unimplemented-opcode `goto bad` sites now decode to `instr(reserved)`, which raises
the general illegal-instruction exception the guest kernel is written to handle.
That repairs every unimplemented encoding at once rather than the two that happened
to be named. The exception is raised at EXECUTE time, not from the decoder — a seat
made the point precisely: readahead translates instructions that may never run, so
raising during decode would corrupt state for a guest that never executed the word.
Readahead itself keeps `goto bad`, matching #309 and #312.

Baseline and result, measured on rebuilt binaries either side of the change: eight
of eight legal encodings halted before, none after, with `nop` unchanged as the
control.

**The measurement was wrong twice before it was right**, and both errors were mine.
The first sweep classified purely on whether a marker store after the test
instruction had run. That conflates three different outcomes — the emulator
stopped, the exception was raised so the store was never reached, and the
instruction ran but did not reach the store. It reported `SLEEP` as a halt, which
is false (`SLEEP` has a case and a handler and simply sleeps), and then, once the
fix landed, reported every repaired row as still broken. Reading the outcome off
the dyntrans halt message instead, and naming each outcome separately, is what made
the numbers mean anything. The row count came down from eleven to eight in the
process, and the smaller number is the true one.

### Recorded, not fixed

A seat's audit of all eleven `goto bad` sites found only four reachable by a legal
encoding; two are dead code, and one is an ifetch failure rather than an encoding
at all. The same audit named more legal encodings still unimplemented — `ICBI`,
`MOVCO.L`, the `SGR`/`DBR` load-store forms, `FPCHG` — which now raise the
exception instead of halting but are still not *implemented*. `MOVLI.L`/`MOVCO.L`
in particular must never become nops: they are the guest's atomics.

Separately, and out of this round's scope, four legal SH-4 sequences reach
`ABORT_EXECUTION`, which sets `cpu->running = 0` by a different route that a decode
sweep cannot see: `FMOV` with `FPSCR.SZ=1` on two paths, `FSRRA` with `PR=1`, and —
inside `pref_rn` itself — a store-queue prefetch while the MMU is enabled, which is
the ordinary way that hardware is used.

## Eightieth round (#315, #316, #317) — the SuperH halts a decode sweep cannot see

#314 converted this file's decode-time halts. These are the execute-time ones: they
need a state prologue — FPSCR.SZ or PR, SR.FD, a branch — so a sweep over bare
encodings is structurally blind to them, which is exactly how they outlived the
previous round. Three of them do not set `cpu->running = 0` at all; they call
`exit()` and kill the gxemul process outright.

Every row below was reproduced on the committed build before anything was edited.

### #315 — the FMOV register-pair family, and a store that killed the process

With FPSCR.SZ=1 an FMOV moves a register *pair*. Four of the six handlers were
wrong, in three different ways.

The two R0-indexed forms ran `ABORT_EXECUTION` outright — a legal FMOV stopping
the emulator. They now perform the transfer the postinc/predec siblings have always
performed.

`fmov drM,@rN` was worse than a halt: it **exited the host process** for half of all
rN. The odd-register check computed its parity from `ic->arg[1]`, which in a *store*
handler is the address register, not the floating-point one — so the parity of a
difference between two unrelated pointers decided whether the guest got its data or
gxemul died. Measured: `@r1` killed the process, `@r2` worked, same instruction.

And where the odd case did get detected, both handlers ran `fatal(); exit(1);` with
the correct redirect sitting unreachable on the very next line — an odd register
field selects the XD bank, which the siblings have always handled.

The trap in fixing that is worth recording, because a panel seat caught it in the
first draft and the measurement would not have: those dead redirect lines assign a
*local* that neither handler ever reads. Un-deadening the line and deleting the
`exit(1)` produces code that compiles, runs, passes every DR test, and silently
transfers the wrong bank. The base pointer has to be used for both words. Gate 10
now carries two XD rows that seed `fr0/fr1` and `xf0/xf1` differently, which are
the only rows in the table that can tell the two apart.

Two smaller defects fell out of the same reading: the register-pair alignment class
is 8 bytes and the R0-indexed forms asked for 4; and the plain store byte-swapped
its first word but not its second, so half of every pair went out in host order.

### #316 — reserved FPU mode combinations killed the host

`fsrra` with PR=1 ran `ABORT_EXECUTION`; `fneg` and `fabs` with an odd register field
under PR=1 called `exit(1)` (with a message naming the wrong instruction). All three
are reserved combinations, and all three now take the illegal-instruction exception —
or its delay-slot variant, since that distinction is architectural.

That last part had a prerequisite the panel found: `sh_exception` had **no case** for
either delay-slot event. `EXPEVT_SLOT_INST` is raised by `trapa` in a delay slot and
`EXPEVT_FPU_SLOT_DISABLE` by the FPU-availability macro every FP handler starts with —
both already in the tree, both falling to a `default` that called `exit()`. Measured:
a branch with `trapa` in its delay slot, and an FP instruction in a delay slot with
FD=1, each killed the process. Lazy-FPU kernels run user code with FD=1 and compilers
do schedule FP work into delay slots, so that one is plausibly reachable by a real
guest. Both now take their general vector.

### #317 — MOVCA.L dropped its store

`MOVCA.L R0,@Rn` was decoded as a nop. The cache allocation is the hint; the store is
the instruction. It now decodes to the existing longword-store handler, which has the
same alignment class and the same exception behaviour, so no new handler was needed.
Leaving the rest of the cache block untouched is a permitted realisation of contents
the ISA leaves undefined. Linux/sh `clear_page` and the BSD sh4 page-zeroing paths
use this instruction, so the dropped store was a wrong answer rather than a missing
optimisation. The gate row seeds a decoy: r12 is the decoder's *default* source for
this encoding, so forgetting the R0 override would silently store the wrong register.

### Rejected by the panel, and therefore not shipped

The round was scoped to include the store-queue prefetch — `pref` into the SQ region
with the MMU enabled, which is the ordinary way that hardware is used and which halts
the emulator today. The proposed fix was to translate the SQ address through the UTLB.
**Three seats independently refuted the mechanism**: `sh_translate_v2p` short-circuits
the whole `0xe0000000`–`0xe3ffffff` range before the MMU path is ever reached, returning
the virtual address unchanged. The patch would have compiled, never faulted, and
replaced a loud halt with a silent no-op that copies the store queue onto itself —
worse than the defect, because it is undiagnosable.

The correct route needs a dedicated entry point, since the identity mapping is
load-bearing for ordinary guest stores into the queues and cannot simply be removed.
That is a design no seat has reviewed, so it is deferred rather than improvised. The
constraint is recorded with it: exception class is the data-TLB **write** family, and
whichever of the raw or masked address is passed to translation, the other must be
used for the flush.

## Eighty-first round (#318) — the store-queue flush the previous round refused to guess at

Round 80 scoped this and then deliberately did not ship it, because three seats
refuted the mechanism. This round is the redesign.

`pref` into `0xE0000000`–`0xE3FFFFFF` is a store-queue write-back. With `MMUCR.AT`
set it ran `ABORT_EXECUTION` — the emulator stopping on the ordinary way store
queues are used once paging is on.

### Why the obvious fix was wrong, and what replaced it

The natural patch calls `cpu->translate_v2p`. That cannot work: `sh_translate_v2p`
short-circuits the entire store-queue range before the MMU path is reachable,
returning the virtual address unchanged and raising nothing. The patch would have
compiled, never faulted, and replaced a loud halt with a silent no-op copying the
queue onto itself.

The identity mapping cannot simply be removed or made conditional either — it is
how ordinary guest stores reach the modelled queue SRAM. So the flush gets its own
entry point, `sh_translate_sq_v2p`, a thin exported wrapper on the static MMU
walker. A flag threaded through the general function was the alternative and was
rejected: that function has exactly one caller, the dyntrans hook, whose signature
is fixed, and a new flag would have to live in the all-architectures namespace to
serve one SuperH quirk.

### Read or write — the question the previous round could not settle

The two round-80 seats split on whether the write-back's TLB fault is judged as a
load or a store, and the answer decides three exception codes. This round put it to
four seats and the split reappeared, so it was settled on evidence rather than
count: the store-queue chapter gives an SQ page's UTLB entry the same
`ASID/V/SZ/SH/PR/D` meanings as any other page while saying `C` and `WT` mean
nothing there — and the dirty bit is consulted only on a write. If the transfer
were judged a read, `D` would be exactly as meaningless as the two the manual
explicitly discards.

The dissenting seat's reasoning was also identified rather than merely outvoted: it
generalised from the manual's *plain* `PREF` description, where the instruction is
a droppable read that raises almost nothing. That sentence is quoted in the comment
directly above this very handler — which is presumably how it got there — and it is
true of every address range except this one.

It is a **write**, and the gate pins it: a clean page owes an initial-page-write
fault, so a build that judged the access as a read would complete the copy and fail
that row alone.

### Measured

The witness installs the UTLB entry and MMUCR through **guest stores** to the
architectural MMIO windows. An earlier version set them by debugger register name;
those names exist but do not reach the fields, so the AT branch was never entered
and the probe would have passed against a build containing no fix at all. It was
caught by instrumenting the branch and finding the marker absent.

The operand carries nonzero bits in both `[9:5]` and `[4:0]`, because the
architectural destination is the translated page plus `[9:5]` with `[4:0]` zeroed —
an address that is neither the operand nor the page base. Measured: operand
`0xE00000E7` lands at page + `0xE0`, which is the composition and not merely
survival. That works because the MMU walker already passes a page's in-page bits
through untranslated, so translating the *unmasked* operand and masking the
*result* produces the manual's rule; the comment says so, because translating an
already-aligned address instead would silently drop `[9:5]`.

Full ladder, five rows: valid+dirty+writable copies; no entry, read-only, and clean
each fault without copying; and with the MMU off the QACR composition is unchanged.

### Recorded, not fixed

The `SQMD` user-access check raises reserved-instruction where the hardware raises
a data address error, and it is consulted only when `AT=1` though the rule is not
conditioned on `AT`. Two seats wanted it in this round; two disagreed, and they also
disagreed on the correct event code — which is itself the argument for leaving it.
It needs a user-mode witness that does not exist yet, and under this project's
test-first rule that makes it a round of its own rather than a guess bundled into
this one. Also still open: ordinary queue-filling stores skip UTLB validation
entirely when `AT=1`, the identity mapping ignores address bits `[25:6]`, and
multiple-matching-entry detection remains unimplemented.

## Seventy-eighth round (#319, #320, #321) — ARM: two rejected rotations, and a carry read off the wrong value

Round 71 left three ARM decoder halts on the record. Working them turned up a
fourth defect that never halted at all, which is the more interesting half of
this round: it had been answering wrongly in silence.

### #319 — uxtab and uxtah rejected a rotation they had room to perform

Both instructions rotate their source before extracting, and both answered a
non-zero rotate with `goto bad` — stopping the emulator on an instruction the
decoder otherwise implements. There was no room for the rotate: rd, rn and rm
already fill all three argument slots. The variants added here carry the
instruction word instead and re-extract, which is the shape `mla` and the
block-transfer handlers already use, and costs one handler per instruction
rather than one per rotate.

A panel seat flagged the trap in doing this by symmetry, and it is worth
recording because the measurement would not have caught it either: a **byte**
extract gives the same answer under a rotate as under a shift at every encodable
amount, since the wrapped bits land above bit 7 — but a **halfword** at ROR 24
wraps rm's low byte into bits 15:8. Copying the byte form's shift would have
been silently wrong for exactly one of the four encodings. The sibling `uxth`
and `sxth` already spell that case out; the gate now has the row that
distinguishes them (`0x11223344` → `0x4411`, not `0x0011`).

### #320 — the immediate path rejected far more than the hazard it was guarding

ARM's shifter carry-out for an immediate is "unchanged if the rotate is zero,
otherwise bit 31 of the rotated value". The dpi template judges that from the
VALUE, treating "greater than 255" as a proxy for "was rotated". The proxy is
right except when a rotate lands at or below 255 — where the architecture says
clear the carry and the proxy leaves it alone — and the decoder answered that by
stopping the emulator.

It stopped it far more widely than the hazard. The rejection ignored the S bit
and the opcode both, so `mov r0, #4 ROR 2`, which writes no flags at all, halted
the machine. Only eight logical opcodes consume the shifter carry, and only with
S set — and the REGISTER path twenty lines above already names that exact set for
itself. Applying its own condition lets everything else decode normally.

For the remainder, the round originally proposed shipping a documented one-bit
divergence, on the grounds that a portable mechanism looked expensive. Two seats
refuted the cost estimate and pointed at the same in-file pattern used for #319:
carry the instruction word, and the condition-code wrappers come free from the
existing macro. That is one cold handler, reached only by encodings nothing
emits, and it closes the class outright instead of documenting it.

**And the guard was not even protecting the case it named.** Its test exempted
an imm8 of zero, so `movs r0, #0 ROR 4` decoded happily and shipped with the
wrong carry — the same defect, silent instead of loud, live on every build this
fork has ever cut. Two seats found it independently and the rig confirmed it.
That is what turns this from a halt fix into a wrong-answer fix, and the routing
condition here deliberately drops the `imm != 0` clause.

### #321 — MVNS took its carry from the complement, and was wrong in every band

Found by a seat auditing #320's blast radius. The decoder rewrites `mvn #imm`
into `mov #~imm` at decode time, and with S set the template then read the
shifter carry off the **complemented** operand. Measured on the committed build:
`mvns r0,#1` set the carry where the architecture leaves it alone;
`mvns r0,#0x3fc` set it where the architecture clears it; `mvns r0,#0xff000000`
cleared it where the architecture sets it.

The fix is to gate the rewrite on the S bit being clear. The flag-setting form
already had table entries — the generator emits all sixteen opcodes for S=1, and
the immediate `mvns` slots were simply unreachable because the rewrite always
fired first. The template's own MVN arm computes `~b` and runs the carry test on
the true operand, which is what the architecture asks for. All four bands now
measure correct, and the two that would have passed by coincidence are in the
gate alongside the two that would not.

### A measurement of mine that was wrong, and how it was caught

The first MVNS reproduction used `0xE3E0…`, which has the S bit **clear** — that
is `mvn`, not `mvns`, and it writes no flags at all. Every verdict in that run
was an artifact of the encoding rather than a property of the emulator, and two
of the four rows would have read as "confirmed defect" anyway. Re-run with
`0xE3F0…`, the real defect appeared exactly where the seat predicted. This is the
second time in this project a bad hand-assembled encoding has nearly produced a
finding out of nothing; the gate rows now carry the encodings that were actually
measured.

### Recorded, not fixed

- **The combined TST/TEQ handlers never update the carry at all**, and the
  combiner accepts rotated immediate forms — so the magnitude proxy is not the
  only thing wrong on that path once instruction combination kicks in. Separate
  from this round's residual and unmeasured here.
- **uxtab/uxtah are ARMv6 media instructions and this rig's SA1110 is ARMv4**, so
  faithful behaviour on *that* model is Undefined rather than execution. #319
  removes a halt and implements the instruction correctly for the models that
  have it; the missing CPU-model gating is the same gap round 71 recorded and is
  not claimed fixed here.
- Rd or Rm as PC in these encodings is unpredictable and the decoder accepts it.
### #322 — the carve-out the panel would not let stand

The first draft of #320 excluded `rn == PC` from routing, and this entry originally
argued the case was too rare to be worth a mechanism and that a cold handler could
not reach the PC+8 reconstruction anyway. **Four of the five diff-review seats
independently named that carve-out as the round's one remaining defect**, and one
supplied the encoding: `tst pc, #4 ROR 2`, which measured leaving the carry SET
where the architecture clears it.

Both halves of the argument for leaving it were wrong. It is reachable — the ARM
manual permits PC as the source for these logical operations — and the
reconstruction needs only `ic`, `cur_ic_page` and `cpu->pc`, all of which the
handler already has; the template does exactly the same three lines. Measured
before and after, with three controls that stay correct either way.

`rd == PC` stays excluded, and that exclusion is right rather than expedient:
writing the PC with S set is an exception return, and the existing handler
restores the flags from SPSR afterwards, so the shifter carry there is overwritten
rather than lost.

What the record below says about the residual is kept, because it is the reasoning
that was overturned and the overturning is the useful part:

- **The #320 routing left PC forms on the old path, and a diff-review seat put the
  sharp question: those encodings used to HALT, so this round moved them from loud
  to silently divergent — the very pattern #320 exists to condemn.** Taking it
  case by case rather than waving at it:
  - `rd == PC` is **moot, not lost**. With S set the template reloads the flags
    from SPSR after the write, so the shifter carry is overwritten before anything
    can observe it. Verified in the template, not assumed.
  - `rn == PC` on MOV or MVN is an SBZ-field violation, i.e. architecturally
    unpredictable. Routing it would only serve encodings that have no defined
    behaviour to be right about.
  - That leaves `ands`/`eors`/`orrs`/`bics`/`tst`/`teq` with **rn == PC** and a
    rotated small immediate. This was left, with the claim that the cold handler
    had no access to the PC+8 reconstruction — **and that claim was false.**
    #322 above closes it; the paragraph stands as written because the panel
    overturning it is the point.
  - The mirror case a second seat raised — `TST`/`TEQ` with the *unused* Rd field
    set to 15 — is the same SBZ argument in the other direction and gets the same
    answer.
- **`sxtab` and `sxtah` are not decoded at all** (raised by a diff-review seat,
  confirmed: the encodings `0x06a00070` and `0x06b00070` appear nowhere in the
  file). #319 gave the unsigned extend-and-add pair its rotation; the SIGNED pair
  has no handler in any form. Since #312 they raise Undefined rather than halting,
  so this is a missing instruction and not a halt — the same "half a family"
  shape #310 hit on PowerPC, and it belongs with the rest of the unimplemented
  ARMv6 media set.
- **Refuted, and worth recording because the reasoning is not obvious**: a seat
  reported that `uxtab_rot`/`uxtah_rot` read `r[15]` without the PC+8 adjustment
  the template applies. They cannot: `uxtb`'s mask pins rn to 15 and is tested
  BEFORE `uxtab` in the same else-chain, so an rn-of-15 encoding is claimed by
  `uxtb` and never reaches the new handler. Same for `uxth` ahead of `uxtah`.
  The concern is real in shape and unreachable in fact.

## Eighty-fourth round — three device bounds checks that would never have fired

**No source changed, on a unanimous five-seat verdict** (Codex, Fable, GLM, Kimi,
agy — the first round run under the standing five-seat rule, and the first with
Kimi back in the panel after several rounds of it wedging).

The round was scoped to add an end-of-buffer check to three MMIO handlers that copy
`len` bytes at `buffer + relative_addr` with no test that `relative_addr + len`
stays inside the allocation: `pvr_vram`, `asc_dma` and `ether_buf`. Read in
isolation all three look exactly like the end-span defects this project has already
fixed elsewhere. In context none of them is a defect.

The sharpest statement of why came from a seat and is worth quoting in shape: a
guest really can *request* a straddling access — a 32-byte PVR DMA at the final
VRAM byte, or the six-byte MAC write the ethernet device itself issues at the final
buffer byte — but the handler receives only the remaining byte.

`memory_rw.c` clamps before it dispatches to any handler:

```c
	paddr -= mem->devices[i].baseaddr;
	if (paddr + len > mem->devices[i].length) {
		...  truncation notice, debug verbosity, capped at 8  ...
		len = mem->devices[i].length - paddr;
	}
```

So `relative_addr + len <= length` is guaranteed on entry to every handler reached
that way, and the truncation is even reported — with a comment noting that probing
the end of a device's range is common and benign. A seat confirmed that dispatch
site is the *only* one in the tree, so there is no second path to worry about.

The proposed checks could not fire, which is the same defect class as a gate that
cannot fail. And they would not have been merely inert: a handler returning 0 is
not a no-op. `memory_rw.c` coerces it to `res = -1`, which raises a bus error on
MIPS and m88k and, on SuperH — the only architecture that has the PVR — silently
abandons the access. (An earlier draft of this entry said "raises a guest bus
error" flatly; that is true of two architectures and not of the one that owns the
first site.) Either way: three unreachable checks whose only possible effect would
have been to damage a guest.

Worth recording because it inverts the brief's own reasoning: the argument for
`return 0` over clamping was that "a partial copy would leave the caller believing
a whole access succeeded". That is precisely what the memory layer already does by
design, on every architecture — it clamps, serves the in-range prefix, zero-fills
the read tail (#95), and reports success.

### The distinction that makes the original audit's entries make sense

Some handlers are called **directly by other handlers**, bypassing that clamp
entirely — `dev_dec21030.c` and `dev_sgi_mardigras.c` both call `dev_fb_access`
with an offset they compute themselves. Those need their own bound, and
`dev_fb_access` has one; it is tagged `OB-1` and uses the overflow-safe form
`len > (uint64_t)size - relative_addr` rather than `addr + len > size`.

That is the whole rule, and it is coherent once stated: **a handler reachable only
through the memory layer relies on the central clamp; a handler that anything else
calls directly carries its own.** The three sites here are registered and never
called directly — checked by symbol grep, not assumed. OB-1 was fixed because it is
in the second category.

A seat found the one other direct invocation in the tree, `dev_pvr_ta_access` called
from the PVR's own DMA path — and it self-bounds with a mask, so it is in the second
category and already correct. It is also the honest caveat on this round's
conclusion: what has been shown is that no current call path can straddle, not that
one is structurally impossible. A future device that calls one of these three
directly would reintroduce the question, which is exactly why the rule is being
written down rather than the finding alone.

### Corrections to this round's own brief, from the seats

- The in-file precedent quoted in the design brief — `if (relative_addr + len > 4)
  return 0;` in the ASC address-register handler — was **misapplied, and also
  mis-located**. It sits immediately above the *second* site, not the third, and it
  is not an end-of-region guard at all: that handler's region is registered as 4096
  bytes over a page-sized buffer, so the check rejects offsets 4..4095 of a window
  whose meaningful register is 4 bytes wide. Its own end-straddle case is already
  unreachable. Copying its shape to a framebuffer-sized window was reasoning by
  appearance twice over.
- **The brief quoted only the read path of the first site.** The write path contains
  a second `memcpy` into the same buffer. A guard written "before the copy" as
  literally quoted would have covered one of the two and left the other — so the
  sketch was not merely unnecessary, it was half a fix. A real guard would have had
  to sit at the top of the function.
- The escape hatch the brief offered itself — "if a guest cannot produce a
  straddling access, document it and change nothing" — was the wrong test, and two
  seats corrected the phrasing independently. A guest *can* produce one: eight-byte
  accesses exist on these guests, and a non-CPU caller in the ethernet device passes
  a six-byte length. What is true is narrower and is the thing worth recording: the
  layer truncates the straddle before dispatch, so the handler's invariant already
  holds when it is entered.
- One seat reported that the `ether_buf` region is larger than its buffer, which
  would have made the proposed bound wrong there. **Refuted from the
  registration**: the device registers *two* regions, the buffer at `addr` with
  length `DEV_ETHER_BUFFER_SIZE` — exactly the buffer's size — and the control
  registers as a separate device at `addr + DEV_ETHER_BUFFER_SIZE`. The
  `relative_addr + DEV_ETHER_BUFFER_SIZE` expression that prompted the concern is
  in the *other* handler, re-deriving a documentation offset.

### Still genuinely open, and a different shape

The "window larger than backing" class is **not** covered by the clamp, which
bounds against the registered length and not the allocation: a device that
registers a window bigger than its buffer satisfies the clamp and overruns anyway.
OB-2, OB-12 and OB-15 are that shape; all three carry fix markers and are believed
done. The distinction is why that shape needs a per-device check and this one does
not.

## Seventy-sixth round (#323) — bcnd rejected two thirds of its own condition masks

`tcnd`'s twin, found while sourcing #307 and left on the record since. The m88k
`bcnd` handler table was generated only for the **nine** mask values the assembler
has mnemonics for; the other twenty-three stayed NULL, and the decoder answers a
NULL entry with `goto bad`, which stops the emulator.

Measured on the committed build: all nine named masks executed, and every one of
the eight unnamed masks tested — 0, 4, 6, 9, 0xa, 0xb, 0xf and 0x11 — halted the
machine.

The manual gives `m5` as a **mask** over four mutually exclusive classes of the
source register, not a list of comparisons: greater than zero, equal to zero, less
than zero *excluding* the most negative value, and the most negative value as its
own class, with bit 4 reserved. That is the same reading `tcnd` was given in #307,
and it reproduces all nine named cases exactly — `0x3` is gt0|eq0 = ">= 0", `0xc`
is maxneg|lt0 = "< 0", `0xd` adds gt0 and becomes "!= 0", and so on.

So the fix writes the mask once and **deletes the enumeration** rather than adding
a second mechanism beside it. The generator's `print_operator()` is gone; leaving
it would have left two answers to the same question.

The risk in that rewrite is a silent change to one of the nine cases that already
worked — which no amount of "the previously-halting masks now run" would catch. It
was put to the panel as the round's first question, and one seat did not argue it
but **measured** it: the old comparison against the new mask expression over
roughly 1.9 million values, zero mismatches. The signed/unsigned split is where
such an argument would have broken if it were going to, since the old code compared
unsigned for masks 5, 7 and 8 and signed for the rest; another seat singled out
exactly those three as the easily mishandled ones and worked them through by hand.

Because the rewrite touches those nine, the gate rows carry two of them as pins. The load-bearing row is the pair `m5=4` against
`m5=0xc`: both mean "negative", and they differ *only* on `0x80000000`, so an
implementation that collapsed those two classes would pass every other row and
fail that one. Seven rows in gate 11, asserting the branch **decision** rather
than survival — rounds 79 and 80 both showed a survival-only row cannot tell a
repaired instruction from one that merely stopped faulting.

### The generated table in the repository was stale

Also from a seat, and the more consequential of its two cleanup notes:
`tmp_m88k_bcnd.c` is **tracked** — this tree commits its generated sources, all
fifty of them — and it still held the pre-fix table, 101 NULLs where the new one
has 32. The build regenerates it, so nothing measured here was affected (the build
trees had it removed before each `make`), but committing the generator without its
output would have put an artifact in the repository that contradicts the code that
produces it, and any reader or marker-grep would have seen the old table. Regenerated
and committed alongside: 96 handlers, 32 NULLs, and those 32 are exactly the
`samepage`+delay-slot slots that have no handler by construction.

### The disassembler was calling both instructions unimplemented

Raised by a seat as non-blocking cleanup, taken because leaving it would have been
a false statement the tree makes about itself: the m88k disassembler printed
`unimplemented_N` for any condition outside the nine named ones — for **`tcnd` as
well as `bcnd`**. That was accurate while the decoder had no handler and stopped
the emulator; it stopped being accurate for `tcnd` at #307 and for `bcnd` here.
Both now print the mask value, since what those encodings lack is an assembler
mnemonic, not an implementation.

A wording correction from the same seat is taken too: the reserved bit 4 forms are
better described as *accepted field values* than as "legal encodings" — the manual
requires that bit be zero for future compatibility, so accepting them is tolerance
rather than conformance.

### An instrument error, and a review claim, both corrected

The first reproduction attempt reported *every* mask as halting, including the nine
that work. That was a placeholder instruction left in the probe, not a finding —
and the control rows failing is exactly what said so. The second attempt then
parsed no addresses at all because the m88k disassembly lines carry an `s` prefix
the regex did not expect. Both were instrument defects caught by controls rather
than by inspection, which is the whole reason the controls are there.

A diff-review seat noted that the `samepage`+delay-slot table slots remain NULL and
suggested a same-page delayed branch would still halt. **Refuted from the decoder:**
the NULL test guards only `ic->f`, which is taken from the non-samepage half of the
table; the same-page entry is used only under `samepage_function != NULL`, so a NULL
there means the optimisation is skipped, not that anything faults.

## Seventieth round, part C (#337) — four guest-reachable `exit(1)` calls in the IDE controller

A guest could kill the **host process** four different ways through `dev_wdc`, the same halt
class this fork has removed repeatedly (#184/#186/#187/#315/#316/#326). Two were reached by
nothing more than choosing an access width; two by issuing an ordinary ATAPI packet command.

- **The two `default:` length arms** (data-port writes of 3 or 8 bytes) now drop the access
  and warn once instead of aborting. Not reachable from SH-4, which has no 3- or 8-byte
  access — `fmov.d` is two 4-byte accesses — but reachable from a 64-bit MIPS machine
  carrying `wdc` over `bus_isa`/`bus_pci`.
- **`res == 0`** — any packet command the SCSI layer rejects. Now completes with no data and
  still asserts the interrupt, which is how a real drive reports a failed packet command,
  rather than taking the emulator down.
- **`res == 2`** — any ATAPI command wanting a DATA OUT phase, `MODE SELECT` among them.
  That arm **already set the correct phase and then called `exit(1)` anyway**, so deleting
  the abort is the entire fix; the transfer itself remains unimplemented and now says so.

Each replaced abort latches a warn-once flag. That is not decoration: #265 shipped an
unlatched warning that a retrying guest turned into a host-log flood, and #269 had to undo
it.

**Honest limits.** This is a *reachability-argued* round, not a rig-measured one. The queued
item asked for a PReP/IDE instrument; a review seat established that no such rig is needed —
`machine_landisk.c` already instantiates `wdc` and landisk is a passing gate-5 rig — but
building the ATAPI witness is its own round, and only `res == 0` and `res == 2` would be
measurable on it. The four sites are removed on the strength of the code path plus the class
precedent, and the harness confirms nothing regressed; no row asserts them yet. The queue
entry also said "four" — the file contains no other `exit(1)` now, but that was worth
checking rather than trusting.

## Ninety-first round (#336) — PowerPC double arithmetic never read its own rounding mode

`fadd`, `fsub`, `fmul` and `fdiv` computed in host double under the **host** rounding mode
and never consulted `FPSCR[RN]`. Only the conversions (`frsp`, `fctiw`) read it — which is
why the mode looked wired when gate 13 was built around those. Measured with the guest's
own instruction:

```
fadd RZ mode ignored   3ff0000000000001   owed 3ff0000000000000   DISC
fadd RN control        3ff0000000000001        3ff0000000000001   PIN  ok
```

`1.0 + 3·2^-54` is exactly three quarters of the way from `1.0` to the next double, so the
modes genuinely disagree: nearest rounds up, toward-zero truncates. Any operand pair whose
exact sum is representable would agree in every mode and measure nothing. The RN row is the
control and is a **PIN** — it must give the same byte before and after, which isolates *the
mode* as the thing that was ignored; without it, a "fix" that broke `fadd` outright would
still flip the RZ row and look like success.

- **#336 (`cpus/cpu_ppc_instr.c`)** — the four operations now go through #300's
  `ieee_add_round_rm` / `ieee_mul_round_rm` / `ieee_div_round_rm`, which already serve MIPS,
  SH and m88k. `PPC_FPSCR_RN_MASK` is 0..3 in the same encoding as `IEEE_RM_*`, so the field
  passes straight through. `fsub` is `ieee_add_round_rm(a, -b, rm)`: negating an operand is
  exact, so one rounding remains.

**Still not wired:** `fmadd`/`fmsub`. #335 made them correctly *fused*, but `fma()` rounds
per the host mode, so a directed-mode fused rounding needs an exact product-sum rather than
a helper call — the one case in this family that a two-operand helper cannot serve.

## Ninety-second round (#335) — `fmadd` rounded twice, and whether that was wrong depended on the compiler

PowerPC `fmadd` is architecturally **fused**: Book I defines it as rounding the product-sum
exactly once. The emulator computed `fra.f * frc.f + frb.f`, which rounds **twice** unless
the compiler contracts it into a hardware FMA — so this instruction's correctness was a
property of the **build host** rather than of this source. `gate_offline.sh` asserts only
that the generated Makefiles do not *add* `-ffp-contract=fast`, which cannot see GCC's own
GNU-mode default, and on a baseline x86-64 target there is no FMA instruction to contract
into at all.

Measured, offline first and then in the guest through the cold debugger:

```
a*b+c as written : 0x0p+0      UNFUSED (two roundings)
fma(a,b,c)       : -0x1p-104   the architectural answer

fmadd fused 1+-2^-52   0000000000000000   owed b970000000000000   DISC
fmsub fused 1+-2^-52   0000000000000000   owed b970000000000000   DISC
fmadd 2by3+1 control   401c000000000000   401c000000000000        PIN  ok
```

`(1+2^-52)·(1-2^-52)` is exactly `1 - 2^-104`, which needs 104 significant bits: the first
rounding destroys it and the second has nothing left to keep. Forcing `-std=c99` changed
nothing — the reason this build does not contract is the absent instruction, not the
language mode.

The `2.0 × 3.0 + 1.0 → 7.0` row is an operand-**routing** diagnostic and passes on both
sides. Its justification is narrower than the `fctiwz` precedent it resembles, and the
first version of this note overstated it: because the two defect rows expect a *nonzero*
byte, an empty or misrouted register makes them fail rather than pass by accident. What the
control adds is the ability to tell "the fusion is wrong" from "the operands never arrived"
— the same symptom on those rows, and different bugs.

- **#335 (`cpus/cpu_ppc_instr.c`)** — `fma(fra.f, frc.f, frb.f)` for `fmadd`, and
  `fma(fra.f, frc.f, -frb.f)` for `fmsub`; negating the **addend** rather than the result is
  what keeps it a single fused operation. Correct *and* host-independent, where the old
  expression was at best accidentally correct.

**Deliberately not fixed here, and one honest qualification.** `fma()` rounds per the
**host** mode, which is round-to-nearest. PowerPC `FPSCR[RN]` is not wired to arithmetic
anywhere in this tree — all six double-precision operations compute in host double and store
through the legacy entry point, and only the conversions (`frsp`, `fctiw`) read the mode.
That is its own queued round.

The first draft of this entry claimed the change was "no worse" for directed modes. **A
review seat refuted that with a witness**: for `a = 1+31u`, `c = 1+u`, `b = -1` (`u = 2^-52`)
the old double rounding happened to land on the toward-zero answer `3d00000000000000`, while
the fused result rounds to `3d00000000000001`. So directed-mode arithmetic can be *pointwise*
worse, not merely equally unsupported. Accidentally right is not a property worth preserving
— and the round's own `-2^-104` vector cannot expose this, because that result is exactly
representable in every mode.

**Adjacent, and left open:** `fmadd`/`fmsub` still raise none of their architectural
exception causes, where `fmul` calls the cause machinery — and an FMA can owe two at once
(`0·Inf` with an sNaN addend owes `VXIMZ|VXSNAN`), which the tree already documents. The new
rows read only the result, so they cannot see it. `fnmadd`/`fnmsub` are **not decoded at
all** and halt, so they never ran the defective expression; when they are implemented they
must negate the **already-rounded** result (`-fma(a,c,b)`), which is not the same as moving
the sign inside. The single-precision `fmadds`/`fmsubs` family must stay fused too and
cannot simply alias these handlers.

Gate 13 goes 118 → 121 rows (81 DISC / 40 PIN). The control row's name is `2by3+1` and not
`2*3+1` on purpose: a `*` in a row name is a BRE repetition operator and makes the gate's own
named-row check unsatisfiable, which this harness has already been bitten by once.

## Seventy-second round (#331–#334) — there was no gradual underflow, and three architectures were quietly relying on that

`ieee_store_float_value_rm()` could not produce a subnormal result. In double precision it
could not produce one *at all*: the `FP_SUBNORMAL` arm was an empty `// TODO` that returned
the sign bit, so every subnormal double stored as **±0**. In single precision the loss came
from somewhere else entirely, and the queued item named the wrong line — a single-subnormal
value such as `1e-40` is a **normal host double**, so it ran the `FP_NORMAL` arm, was
normalised to a biased exponent below zero, clamped to zero at `:533`, and flushed at `:594`.

Measured on the committed build before anything was edited, against two oracles that are not
the code under test — for D the identity (every finite double is exactly representable in D,
so there is nothing to round and the owed answer is the input's own bit pattern), for S the
host's own correctly-rounded cast taken under the matching hardware mode:

```
D-format: 220/220 wrong          (all four modes, every subnormal -> +/-0)
S-format: 65737/65740 wrong      (via FP_SUBNORMAL arm: 1, via FP_NORMAL arm: 65736)
  S 1e-40   cls=FP_NORMAL  gxemul 00000000  host 000116c2
  D 2^-1074                gxemul 0000000000000000  owed ...0001
```

**65736 of the 65737 single-precision failures arrived through the arm the queue did not
name.** A round that fixed only the `TODO` would have reported success and left every single
subnormal still flushing.

- **#331 (`core/float_emul.c`)** — `ieee_encode_subnormal()`. Every subnormal is an integer
  multiple of its format's quantum, so the encoding is "scale by one quantum, round to an
  integer": `2^149` for S, `2^1074` for D. The scaling is exact — a power of two only moves
  the exponent — so the single deliberate rounding is the only error in the path. `ldexp()`
  is required rather than a literal: **`0x1p1074` is not a finite double**, it is `+Inf`, and
  writing it would have turned every D subnormal into a NaN. The rounding carry is
  deliberately **not masked**: a result of exactly `2^n_frac` ORs into a word holding only the
  sign and lands as biased exponent 1 with a zero fraction, which is `FLT_MIN`. `IEEE_RM_RZ`
  and `IEEE_RM_LEGACY` are truncated here rather than handed to `ieee_round_to_integral()`,
  which returns those two *unchanged*.
- **#332 (`cpus/cpu_mips_coproc.c`)** — `fpu_subst_tiny()`. #292 justified the old flush with
  "MIPS routes non-flush denormal results away (#246)", and **both halves of that were
  wrong**: `fpu_unimpl_trap()` returns 0 on EXC3K so R3000 fell straight through, and the
  FS=1 arm *deliberately skips* the routing, so **R4000 was getting its flush-to-zero from
  this bug rather than from any code that meant it**. R4000 with FS set does not flush
  universally either — it substitutes signed zero *or MinNorm* by sign and rounding mode, so
  a positive tiny under round-toward-+Inf owes `+MinNorm`. Classification is done on the
  **encoded word**, which is tininess *after* rounding as MIPS specifies.
- **#333 (`cpus/cpu_alpha_instr.c`)** — `alpha_store_t()`. Only the *unqualified* `addt`,
  `subt`, `mult`, `divt` are decoded, and those owe zero on underflow. That used to fall out
  of the encoder's flush. Bit-identical to previous behaviour on every input, deliberately:
  there is no Alpha rig, so "preserve what shipped" is the only honest reading available.
- **#334 (`cpus/cpu_sh_instr.c`)** — `sh_dn()`. `SH_FPSCR_DN_ZERO` had been defined since the
  port was written and was **read by nothing**. SH-4 never delivers a subnormal result: DN=1
  writes a signed zero, DN=0 raises an FPU error. **FPSCR resets to `0x40001`**, so DN=1 is
  the default configuration and shipping #331 alone would have changed every SH guest.
  Applied through two macros rather than twenty-three hand edits — the safer construction,
  not merely the shorter one, because a per-site edit can miss a site silently and this
  cannot; the function is a no-op for everything that is not subnormal in the destination.

**What the instrument was doing wrong.** Gate 2's own oracles contained
`if (r != 0.0f && fabsf(r) < FLT_MIN) return signbit(x) ? 0x80000000u : 0u;` — they
**re-implemented the very flush they were checking**, so across the whole subnormal band the
"independent right answer" was neither independent nor right, and the band could not have
been measured wrong no matter how wrong it was. That is the complicit-instrument failure this
file's header already warns about, surviving in a second form. Removing it needed nothing
added; the host's cast was already correct. `must_differ()`'s `&& signbit(x)` was equally
stale — it dated from #287, when the only thing the band had to get right was *keeping the
sign of the zero it flushed to* — and leaving it in dropped 112190 positive band samples into
`unexplained`. Its new lower bound is not decoration either: the differential runs through
the LEGACY entry point, which truncates, so values below one whole quantum still truncate to
zero and legitimately agree with upstream; demanding otherwise claimed 4263461 inputs "should
have moved but did not".

Rows re-authored rather than deleted, because a class whose evidence disappears when it is
fixed cannot be shown to have stayed fixed: the absolute rows `±1e-40 → ±0`, and the named
vector literally called **"flush keeps the sign"**, whose *name* was as stale as its value.
Nine new named vectors, the load-bearing ones being `±0x1.fffffep-127` — the exact midpoint
`2^-126 - 2^-150` between the largest subnormal (odd) and `FLT_MIN` (even). The pre-existing
control at `0x1.ffffffp-127` sits **above** that midpoint and rounds up under every tie rule,
so it proved the carry happens but not that it happens for the right reason; the new rows
prove ties-to-even crosses *out* of the band, and an implementation that masks the carry
answers `0x00000000` — a full `FLT_MIN` of error. Two new mutants pin exactly those two
failure modes, and `revert287`'s anchor was retargeted: it quoted the deleted flush verbatim
and would have gone `SETUP_FAIL`, which is the third time that guard has caught a mutant
outliving the code it attacked.

**Panel.** Two seats, before the round. They **dissented from each other twice**, and the
more precise reading won both times: that R4000 FS=1 is a mode-dependent substitution and not
a plain flush, and that pmax must *not* be recorded as answering `0x80000002`, because the
R3010 leaves the destination register unchanged on UnImp and software completion is a later
action, not the CPU's answer. pmax is therefore left flushing, per #246's deliberate EXC3K
bit-identity — GXemul wires no R3010 interrupt pin, so an emulator that merely declined to
write the destination would leave the guest reading a **stale register**, which is worse than
either honest answer. The seats also corrected two claims in the brief itself: the macro is
`SH_FPSCR_DN_ZERO` and not `SH4_FPSCR_DN`, and `2^-149` is the minimum subnormal, not the
midpoint — the midpoint is `2^-150`.

**The one guest-visible row that moved**, and it is the row #303 pinned *for* this round:
m88k `fmul.sss(-S-min, 2.0)` went `0x80000000` → **`0x80000002`**, measured. It has now
flipped twice — garbled-nonzero before #303, minus-zero after it, and the true `-2^-148`
now — which is exactly what a KNOWN-CHANGE pin is for. m88k gets no call-site guard because
the MC88100's default underflow handler writes the denormalized result, so gradual underflow
is what that architecture owes. **pmax did not move**, which is the control: gate 12 passed
untouched, confirming #332 keeps EXC3K bit-identical rather than merely intending to.

**Left open, and recorded rather than guessed at:** PPC-D, Alpha and SH PR=1 D arithmetic
have no gate rows at all, so #331 changes them without a witness; the #246 trap predicate is
still pre-rounding and over-traps across the sliver that rounds up to `FLT_MIN`; and whether
Alpha wants `+0` for a negative tiny is unmeasurable here.

## Eighty-ninth round (#330) — the exception causes VX and FEX had nothing to derive from

#327 made FPSCR's VX and FEX derived and correct. This measured what they were deriving
*over*, and the answer was nothing: **ten distinct exception causes, none ever raised.**
Every FPSCR read back after an arithmetic instruction held only its FPCC nibble.

| operation | before | after | cause |
|---|---|---|---|
| `fadd` Inf + −Inf | `00001000` | `a0801000` | VXISI |
| `fsub` Inf − Inf | `00001000` | `a0801000` | VXISI |
| `fdiv` Inf / Inf | `00001000` | `a0401000` | VXIDI |
| `fdiv` 0 / 0 | `00001000` | `a0201000` | VXZDZ |
| `fmul` Inf × 0 | `00001000` | `a0101000` | VXIMZ |
| `fdiv` 1 / 0 | `00004000` | `84004000` | ZX |
| `fadd` / `fcmpu` sNaN | `00001000` | `a1001000` | VXSNAN |
| `fctiwz` sNaN / qNaN | `00000000` | `a1000100` / `a0000100` | VXCVI |

**Every one of those bytes was pre-registered from Book I before the code existed, and
two panel seats derived them independently and agreed byte for byte.** All seventeen new
rows — ten raised, seven negative controls — matched on the first run.

### The negative controls are the round

Seven rows assert that nothing is raised, and they are not decoration: a handler that
raised on any NaN, any infinity, or any zero divisor would pass every positive row above.
`qNaN + 1` must not raise VXSNAN; `Inf + Inf` must not raise VXISI (it is sign-specific);
`Inf × 1` must not raise VXIMZ; and **`Inf / 0` must raise nothing at all**, because ZX
needs a *finite nonzero* dividend — `0/0` is VXZDZ, not ZX, and `sNaN/0` is VXSNAN, not
ZX. Zero false positives across all seven.

### Three panel warnings that were load-bearing

- **`fmul` reads `arg[1]` and `arg[2]`; `fadd`/`fsub`/`fdiv` read `arg[0]` and `arg[1]`.**
  A shared operand macro across these handlers would have classified `fmul`'s
  **destination register**. Each handler binds its own named locals.
- **`struct ieee_float_value` cannot distinguish a signalling NaN from a quiet one** — it
  collapses every NaN to the host's `NAN` and takes a path that also drops the sign. So
  detection reads raw 64-bit patterns. And `frsp`'s bare quiet-bit test, lifted out of its
  already-NaN branch, calls **Infinity** a signalling NaN; the new predicate carries its
  own NaN-class guard.
- **Detect from operands, never from the host result.** `isnan(result)` is the obvious
  lure and it is wrong: for an `fmadd` whose product overflows the host, the host computes
  a NaN where the ISA's unrounded intermediate is an infinity and no exception is owed —
  a result-driven test would invent one.

`ppc_fpscr_raise()` takes a **mask**, because one instruction can owe two causes at once
(`fctiwz` of a signalling NaN owes VXSNAN and VXCVI together), and its FX test is
**per-bit** (`causes & ~fpscr`). Transplanting `mtfsb1`'s single-bit form would miss FX
exactly when one cause is already sticky and another transitions.

VXCVI is classified **separately from the result branches**, which the source has warned
about since #326: reusing `>= 2147483647.0` / `<= -2147483648.0` as the predicate would
call exactly 2^31−1 and exactly −2^31 invalid, and under RZ would see an unrounded value.
The predicate rounds under the real mode first and uses strict inequalities.

### Two things this round had to repair in the harness

**Three rows from #326 had gone vacuous.** The `VXSNAN sticky vs fadd/fmul/fcmpu` rows ran
their second instruction on the register still holding the signalling NaN. That was fine
while arithmetic raised nothing — but the moment this round made it *raise* VXSNAN, a
handler that cleared the bit and immediately re-raised it from its own operand would still
answer "set". They now run on a benign operand. A seat predicted this before the code
landed; nothing in the gate would have noticed.

**A row name containing `*` made its own check unsatisfiable.** `VXIMZ fmul Inf*0` passed
as a row and its named check counted **zero**, because the gate matches names with a plain
grep and `Inf*0` in a basic regular expression means "In" followed by any number of "f"
and then "0". Third variant of this trap here — first a name as long as its column, then a
name that was a prefix of another, now a metacharacter. Row names are letters, digits,
spaces and hyphens from now on.

### Deferred, with reasons

XX/FI (FI is non-sticky state this file has never modelled), OX/UX (**blocked**: the
subnormal store arm is a bare TODO that flushes to signed zero, so underflow cannot be
honestly reported over it), the FPRF class bit (it *moves* existing bytes), and
enable-driven result suppression (it changes what lands in the target register and drags
in trap delivery). Gate 13: 101 rows → **118**, 82 checks.

## Ninetieth round (#329) — the Thumb shift paths, where the flags came from a register the instruction never named

#328's completeness sweep swept past its own scope and found three more flag defects in
the same function. All three measured on the committed build, both controls passing.

**ASR-immediate took Z and N from `r[rd8]` while writing `r[rd]`.** In the
shift-immediate format (`000 op imm5 Rs Rd`), `rd8` is bits 10:8 — **the top three bits of
the shift amount**. So `asrs r0,r1,#12` computed the right value and then set its flags
from **r3**, a register the instruction does not mention. Change the shift count and the
flags come from a different register. LSL and LSR never had it; ASR alone did.

There is a trap in witnessing this, which the panel flagged before any row was written:
for a shift below 4, `rd8` is 0, so a row writing r0 reads back the right register **by
accident**. The witness uses `#12`.

**RORS never cleared Z and N** before ORing them in, unlike every neighbouring case — the
`tst` arm immediately below does it correctly. A stale Z survived a rotate to a nonzero
result, and a stale N survived one to a positive result.

**`LSR #0` and `ASR #0` encode shift-by-32, not shift-by-zero.** LSR gives 0, ASR gives a
sign fill, and both write C from bit 31 of the operand. Both executed as no-ops with C
untouched. `LSL #0` *is* a genuine no-op whose C must survive — it is the control here,
and the one member of the family whose zero encoding means what it says.

Written as explicit branches rather than by turning 0 into 32 and shifting: a shift of 32
on a 32-bit type is **undefined in C**, so the obvious form would have been UB on exactly
the case the fix exists to repair.

### Half the contract was unmeasurable, and the rig had to change first

C for the shift-by-32 cases is *always written* but **not always set** — a positive
operand clears it. The Thumb rig #328 built could not see that half: it never preset the
flags, so on a cold machine C starts clear, and both "LSR #0 clears C for a positive
operand" and "LSL #0 leaves C alone" passed against a build that never touched C at all.

`run_thumb` now presets carry with the same real `SUBS` gate 14 uses in ARM mode — never a
debugger `cpsr` write — placed before the `bx`, which is safe because `bx` touches no
flags. It can also publish a register other than r0, because every Thumb row until now
wrote and read r0, so a handler reading r0 instead of `rd` would have been invisible —
the shadow of this round's own first defect.

Gate 14: 129 rows → **149**, 142 checks.

### The boundary, stated

Both seats swept every flag write in the function and agree the set is now complete
*within what the interpreter implements*. One near-miss is worth recording as a
non-defect: `movs` with an 8-bit immediate clears Z and N and then sets only Z. That is
**correct** — an imm8 result is 0..255, so N is always 0 and the clear supplies it. It
would have been easy to "fix" into a bug.

What bounds the claim is coverage, not correctness: nine format-4 ALU operations
(register `LSL`/`LSR`/`ASR`, `ADC`, `SBC`, `NEG`, `CMN`, `BIC`, `MVN`) and the
hi-register `ADD`/`CMP` are not implemented at all and stop the emulator — the halt class
of rounds 70/78/79/80/87, not silent flag corruption.

## Seventy-seventh round (#328) — three flag defects in the Thumb interpreter

### Reaching Thumb at all was the round

Gate 14 has only ever driven ARM-mode encodings, and the Thumb interpreter
(`arm_cpu_interpret_thumb_SLOW`) is a completely separate implementation that #311 never
touched. Thumb is entered **architecturally** here — an ARM `bx` to an odd address sets
`ARM_FLAG_T` and `cpu_dyntrans.c` dispatches to the interpreter — and never by writing the
T bit with the debugger, for the reason gate 14 already records about carry-in: a debugger
write reaches `cpsr` but not the separate `flags` field the handlers read, so it would
preset nothing. `mrs` is ARM-only in Thumb-1, so each row returns to ARM with a second
`bx` before publishing; `bx` touches no flags.

### What was wrong

Four near-identical blocks — add/sub register+imm3, `CMP` imm8, add/sub imm8, and
format-4 register `CMP` — each computed

```c
uint64_t result = old + (uint32_t)(-b);
```

and read every flag off that value. **Three of the four flags were wrong.** Measured on
the committed build, with three controls passing including a genuine-borrow case:

- **Z** came from `result == 0`, the full 64-bit value. A subtract that reaches zero
  carries out of bit 31, so `result` is `0x100000000` — not zero — and Z stayed **clear**
  while the stored 32-bit result was 0. Subtracting equal values is the commonest way to
  reach zero, and `subs; bne` is how a Thumb countdown loop ends: it never did. The same
  line also missed Z for an **ADD that wrapped to zero**, which the round's first framing
  had not noticed.
- **C** came from bit 32. With `b == 0` the addend is `(uint32_t)(-0)` — which is 0 —
  nothing carries out, and C read 0. So `cmp r0, #0` reported a borrow that never
  happened.
- **V** came from the sign of the *negated* subtrahend, and negation is exactly what
  cannot work at `0x80000000`, the one value that is its own negation. V was wrong in
  **both directions**: `0 - INT_MIN` gave V=0 where 1 is owed, `-1 - INT_MIN` gave V=1
  where 0 is owed, and `INT_MIN - INT_MIN` — an `x - x` that cannot overflow — reported
  V set *and* Z clear, two defects on one instruction. Note this one is reachable in
  **two** of the four blocks, not four: imm3 and imm8 cannot encode `0x80000000`. Z and
  C were in all four.

**N was always right**, because it cast to `int32_t` before testing. That is the shape the
other three should have had, sitting in the same block the whole time.

### The fix, and the bug the panel caught in it

One helper, `thumb_addsub_flags()`, replacing all four inline copies. Carry mirrors
#311's committed ARM-mode formulation — compute in 64 bits on the **un-negated** operands
and compare against the truncated result. That mirroring is not a transplant: applying
#311's `c32 == c64` test to the *old* expression would have set C backwards for every
nonzero subtrahend, because `old + (uint32_t)(-b)` is a different 64-bit value.
Restructuring onto a true subtraction first is what makes the two agree.

The first draft of the fix would have shipped a bug. It tested `old >= b` — but **no `b`
exists** at that point: the subtrahend has already been destroyed by the negation, and in
the register block `r[rd] = result` executes *before* the flag code. Since `subs r0,r1,r0`
is legal, re-reading the register there would have computed carry from the value the
instruction had just written. The helper takes both operands as arguments, and a gate row
(`T alias subs rd==rm`) exists specifically because a review seat found that.

### Gate 14

Grows from 83 rows to **129**, 122 checks. Sixteen Thumb rows, each asserting the flags
**and** `rd` — these are flag defects, the computed value was already correct, and a row
checking only the flag could not tell a fixed flag from a broken result. Three are
controls, and the borrow control is the one that proves the rig can still distinguish a
real borrow from the broken ones.

Every defect row was measured failing on the committed build before the fix, including
the three V rows: those were first *derived* from the source, and then the change was
stashed, the tree rebuilt, and all thirteen re-measured — because a derivation presented
as a measurement is exactly the error #327's after-pass had just caught.

The after-pass then found a hole in the gate itself. Sixteen rows covered every *register*
form and both CMP forms, and left the **immediate** arms unpinned: nothing exercised
`ADDS Rd,#imm8` or either imm3 form, so a regression that read the register instead of the
imm3 field, or inverted `isSub` only where it shows on an ADD, would have passed the whole
table. Three rows close it. The same pass caught a `nzcv()` helper added here that
**shadowed an existing function of the same name** — harmless only because the file runs
top to bottom, which is a latent trap rather than a design; it is `thumb_nzcv()` now.

### Found while sweeping, not fixed here

The completeness question was answered by sweep rather than spot-check: `result &
0x100000000ULL` occurs exactly four times in the file, and every other Z/N site reads a
`uint32_t`. So these four blocks were the whole of *this* defect pair. But the same sweep
turned up three more, filed rather than folded in:

- **ASR-immediate sets Z and N from a register chosen by the shift amount.** It writes
  `r[rd]` and then tests `r[rd8]` — and in that encoding `rd8` is bits 10:8, the top three
  bits of `imm5`. `asr r0, r1, #12` sets flags from **r3**.
- **`RORS` never clears Z/N** before ORing them in, unlike every neighbouring case, so a
  stale Z survives a nonzero rotate.
- **`LSR #0` and `ASR #0` are shift-by-32** in this encoding, not shift-by-zero, and
  neither the result nor C reflects that.

Also noted: Thumb `ADC`, `SBC`, `NEG`, `CMN` and the hi-register `ADD`/`CMP` are not
implemented and reach a `default:` that stops the emulator — the same halt class as rounds
70/78/79/80/87.

## Eighty-eighth round (#327) — VX and FEX were stored, and the ISA says they are derived

### Measured first, in both directions

Book I does not describe these as storage. VX is "the OR of all the Invalid Operation
exception bits"; FEX is "the OR of all the floating-point exception bits masked by their
respective enable bits"; and no instruction may write either — "mcrfs, mtfsfi, mtfsf,
mtfsb0, and mtfsb1 cannot alter FPSCR VX / FEX explicitly". This fork stored both, so they
went stale each way. Measured on the committed build, control first:

| sequence | FPSCR via `mffs` | |
|---|---|---|
| `frsp(sNaN)` | `a1001000` | FX+VX+VXSNAN — **control, correct** |
| `frsp(sNaN); mtfsb0 7` | `a0001000` | cause cleared, **VX still set** |
| `mtfsb1 10` (VXZDZ) | `80200000` | cause set, **VX never rose** |
| `mtfsb1 7; mtfsb1 24` | `81000080` | VXSNAN+VE, **FEX never rose** |

"VX set with no cause" is a state hardware cannot produce, and **#326 is what made it
reachable**: three of the four instructions that may clear an exception bit did not exist
before it. Every record form then copied the phantom into CR1.

### The fix, and why both halves had to land in one commit

`ppc_fpscr_recompute()` derives both bits from the rest of the register, called from the
five FPSCR writers and from `frsp`. It deliberately leaves FX alone — FX is sticky and
latches on a 0→1 transition, so recomputing it would undo a guest's explicit clear.

`mtfsf` also stops copying FEX and VX out of the source FPR. #326 recorded that as a
divergence and its comment said the mask and the recompute "have to land together"; this
is that landing, and the reason is not tidiness. Before the recompute existed, `mtfsf`'s
unmasked write was **the only way a guest could clear a phantom VX** — every other path
either early-returns or masks the bit. Masking `mtfsf` alone would have made the phantom
permanent. FX is *not* masked out of `mtfsf`, because it is one of the two instructions
exempt from the implicit-FX rule and takes FX from its source.

Two smaller defects fixed alongside, both found by the panel:

- **`frsp` set FX unconditionally.** FX latches only on a 0→1 transition, so a second
  signalling NaN after the guest had explicitly cleared FX must not set it again.
- **FEX never rose at all**, however the guest got there: an enabled invalid operation
  left it clear. Two rows now pin that the two orderings agree.

  A correction to this round's own record, from the after-pass: the first draft said
  the old code was *order-dependent* here, giving different FEX for
  `mtfsb1 24; frsp(sNaN)` than for the reverse. **That was never measured and it is
  false** — with no recompute on either path both orderings answered `a1001080`,
  agreeing with each other and both missing FEX. The rows are kept, because
  order-independence is worth pinning now that FEX moves at all and a recompute wired
  to the wrong site would break it, but they did not catch a disagreement and the
  record should not say they did.

### Twelve pre-registered bytes, and four rows that had to move with the code

The panel worked out that the recompute changes **four existing `mtfsf` rows**, not the
one this round set out to fix, because the derived summaries re-establish themselves from
whatever `mtfsf` did write. Every byte was derived from Book I and written down *before*
the code was built, then verified independently:

| row | was | now | why |
|---|---|---|---|
| `mtfsf FM=0x80` | `f0000000` | `90000000` | FEX/VX no longer copied |
| `mtfsf FM=0x40` | `0f000000` | `2f000000` | VXSNAN derives VX |
| `mtfsf FM=0x0f` | `0000ffff` | `6000ffff` | VXSOFT/VXSQRT/VXCVI + VE derive both |
| `mtfsf clears` | `0fffffff` | `6fffffff` | preloaded causes/enables survive the write |

`FM=0xff` is unchanged **only by coincidence** — with every cause and enable set,
derivation happens to reproduce the copy — and `FM=0x01` selects a field containing no
causes. Six new rows cover the summaries directly (`80001000`, `a0200000`, `e1000080`,
`00000040`, and the two order-independence rows at `e1001080`).

Twelve rows were predicted in advance — the six `mtfsf` rows (four changing, two
predicted to stay put) and the six new ones — and every one matched on the first run.
Predicting that a row will *not* move is as much a prediction as predicting that it
will. That is what makes the gate this fix's acceptance test rather than a transcript
of it, and it is the discipline gate 13's header has demanded since #304.

One qualification the after-pass insisted on, and it is fair: three of those wants
(`80001000` and the two `e1001080` rows) contain an **FPRF nibble this fork models
incompletely**. Hardware gives a NaN the class `10001` — C *and* FU — while this
emulator sets only FU. So those bytes are Book I's answer for the summary bits plus
*this model's* answer for FPRF, not Book I end to end, and "pre-registered from the
ISA" would be an overclaim if said without that. The C bit (ISA 15) is a real
divergence, unpinned by any row; it belongs with the arithmetic exception work.

Also unrecorded until now: reserved ISA bit 20 is *retained* when `mtfsf` or `mtfsfi`
write it — `6000ffff` includes it — where a real G4 reads it back as zero. v2.01's
reserved-bit rule permits either, so this is policy rather than a defect, but it was
policy nobody had written down.

Gate 13 grows to 101 rows / 70 checks. The FPSCR bit table in `cpu_ppc.h` now covers
every bit this round needs — all the causes, all five enables, FR/FI and NI; FPRF's
class bit (ISA 15) is still undefined and unset, so "complete" would be an overclaim —
with **ISA bit 20 excluded from `VX_CAUSES` because it is reserved** — a contiguous-looking
mask over 7:12+20:23 would have folded it into the summary. Two hex literals left in #326's
code (`0x1ff80000 | 0x00000700`) were replaced by the named composition, verified identical.

## Eighty-seventh round (#326) — twenty-four legal PowerPC encodings stopped the emulator, and every record form was one of them

### What was measured first

A 28-row sweep stepped each encoding on a macppc/G4 with FP enabled and classified the
outcome as `alive` / `HALTED` / `DEAD`, reading a halt off the dyntrans
`UNIMPLEMENTED instruction` message and separately proving the session still answered.
Four control rows — `fadd`, `fmr`, `fctiwz`, `mtfsf`, all already implemented — read
`alive`. **Twenty-four rows read `HALTED`.**

This is not a guest-visible exception. Both floating-point blocks in the translator end
with `default: goto bad;`, and `bad:` sets `cpu->running = 0`. A legal instruction stops
the whole machine.

### The one that mattered was not an exotic instruction

`if (rc) { fatal(...); goto bad; }` sat at the entry of **both** the opcode-59 and
opcode-63 blocks. Every **record form** halted — `fadd.`, `frsp.`, `fctiwz.`, `fmr.`,
`fadds.` — including the record forms of instructions that worked perfectly with Rc=0.
That is what a compiler emits whenever a floating-point result feeds a condition test.

The fix follows the house pattern this same file already uses for the integer side:
an `FDOT(n)` macro, twin to `DOT0`, that runs the base handler and then sets CR field 1
from FPSCR[0:3] — Book I, "for all floating-point instructions in which Rc=1, CR Field 1
is a copy of the final state of FPSCR FX, FEX, VX, OX".

Three things about that were not obvious and were caught by the panel before any code was
written:

- **`CHECK_FOR_FPU_EXCEPTION` has to come first, in the wrapper.** The base handler's own
  check returns from the *base*, which would leave the wrapper writing CR1 on top of a
  just-entered exception context for an instruction that never ran. NetBSD/macppc does
  lazy FP — MSR[FP] is clear on a process's first floating-point instruction — so that is
  the ordinary path, not a corner.
- **`update_cr1` cannot be a static in `cpu_ppc_instr.c`.** That file is compiled twice
  (`DYNTRANS_DUALMODE_32`), so it lives beside `update_cr0` in `cpu_ppc.c` instead. The
  same trap caught the new `ppc_convert_to_word` helper, which needed the file's existing
  `#ifndef ..._INCLUDED` idiom.
- **`fcmpu` and `mcrfs` must NOT get record forms.** Neither defines an Rc bit; the low
  bit of their encoding is reserved. The `rc_f` selection therefore carries an explicit
  `NULL` guard, so those two keep being rejected — and so a case that forgets to set
  `rc_f` stays a loud halt rather than becoming a silent no-op that executes and never
  writes CR1.

### The rest of what was decoded

`mcrfs`, `mtfsb0`, `mtfsb1`, `mtfsfi` — the FPSCR control group. Their absence mattered
more than the count suggests: Book I names `mcrfs`, `mtfsfi`, `mtfsf` and `mtfsb0` as the
only four instructions that may clear a sticky exception bit, **and three of the four did
not exist.** Two ISA rules govern them, both verified against the text rather than
assumed: FEX and VX are OR summaries that none of these may write, and FX is implicitly
set by every FP instruction *except* `mtfsfi` and `mtfsf`.

`mcrfs`'s bit-clearing is the subtle one, and the first design was wrong. It clears only
the *exception* bits it copied, per a table in Book I — four of the eight fields clear
**nothing** — 4, 6 and 7 — and those are precisely the ones that would hurt: field 4 is the
FPCC, field 6 the exception enables, and **field 7 holds the rounding mode**, so a blanket
clear would have made `mcrfs x,7` silently reset the guest to round-to-nearest — which
#304's `frsp` reads. (Field 3 clears VXVC only, keeping FR and FI.)

`fctiw` — the round-per-RN sibling of `fctiwz` — now shares one body with it, split only
by the mode. The obvious shortcut here is a trap: `ieee_store_float_value_rm(..., W, rm)`
already rounds and range-checks, but it implements the **MIPS** contract (#273), where a
NaN and both overflow directions all give `0x7fffffff` with no sign dependence. PowerPC
owes `0x7FFF_FFFF` only for a positive out-of-range operand. Instead #294's rounding block
was factored out as `ieee_round_to_integral()` and is now shared, unchanged.

`fnabs` and `fsel`. `PPC_63_FNABS` had been *defined in `opcodes_ppc.h` all along* with no
case in the decoder — the define alone does nothing. Both are bit transport, never
interpret-and-restore, because `ieee_interpret_float_value` collapses every NaN to the
host's `NAN` and would lose the payload.

### Two defects in code that was already running

Found by reading for context, not by the sweep — which could not have found either, since
neither is a halt.

**`fcmpu` threw away the unordered bit.** It wrote `cr |= ((c & 0xe) << bf_shift)`, and
`c == 1` is the unordered case. Measured, with the three ordered rows as controls:
`1.0<2.0`, `2.0>1.0` and `1.0==1.0` all gave the right nibble; **both NaN rows gave `0`**
— neither less, greater, equal, nor unordered, a CR state hardware never produces. A
guest branching on unordered never took the branch. It reads like a transplanted
template: the integer compares build the same 8/4/2 and then OR `XER.SO` into the low bit,
where masking off "the bit I am not supplying" is sensible. In a floating-point compare
that bit is FU, a result.

**Seven handlers were erasing a sticky bit.** `fcmpu`, `fmul`, `fmadd`, `fmsub`, `fadd`,
`fsub` and `fdiv` each wrote `fpscr &= ~(PPC_FPSCR_FPCC | PPC_FPSCR_VXNAN)` when only the
FPCC half is theirs. Book I: the exception bits "are sticky; that is, once set to 1 they
remain set to 1 until they are set to 0 by an mcrfs, mtfsfi, mtfsf, or mtfsb0
instruction". None of those seven is one of the four. So #304 set VXSNAN on a signalling
NaN and the very next arithmetic instruction destroyed the record.

**Gate 13 had a blind spot exactly where the defect lived.** Its `VXSNAN sticky` row runs
a second `frsp` — and `frsp` is the *one* floating-point handler in the file that was not
clearing the bit. The property was proven against the only instruction that could not
break it. Three rows now run `fadd`, `fmul` and `fcmpu` in that second slot instead, which
is the shape of the lesson: an instrument only refutes what its inputs reach.

### Left halting, on purpose, and recorded as such

Twelve encodings still stop the emulator, and gate 15 asserts that they *do*, so the count
cannot drift and the queue cannot quietly lie. The reasons differ and the distinction is
the point:

- `fctid`, `fctidz`, `fcfid`, `fsqrt`, `fsqrts` — **64-bit-only, or outside the G4's
  instruction groups.** On the 32-bit machine this gate drives, real silicon takes a
  program interrupt. Implementing them unconditionally would make the model *less*
  faithful; the honest fix is the missing exception model.
- `fres`, `frsqrte` — estimate instructions with implementation-defined accuracy.
- `fcmpo`, `fnmadd`, `fnmsub`, `fmadds`, `fmsubs` — **no technical blocker at all.** A few
  dozen lines each at the fidelity bar this file already ships. They are out of this round
  for size alone, and that is recorded as the reason, because a queue entry that invents a
  blocker costs a future round the time to disprove it. `fmadds` is the one to do first:
  gcc emits it for ordinary `float` arithmetic, so it is probably the most frequently
  executed instruction still in the halting set.

### The refactor silently disarmed a mutation test, and the harness said so

Factoring `#294`'s rounding block out of `ieee_store_float_value_rm()` into
`ieee_round_to_integral()` is behaviour-preserving — the differential proves it, and the
MIPS path is token-for-token the same operations. But `selftest_mutation.sh` mutates by
**string replacement on the source**, and the `wlegacyrounds` mutant's fragment was the
block that moved. It stopped matching, so that mutant tested nothing, and `#294`'s W/L
rounding was left unguarded with every other gate still green.

The gate caught it, because a previous round had already been bitten by a mutant that
could not fail and added a `need()` check on the fragment: a mutation that no longer
applies reports `SETUP_FAIL` instead of quietly succeeding. It failed loudly, twice —
once as "could be applied" and once as "is DETECTED". Only that one mutant broke; the
other four still applied and were detected, which is what a partial failure here should
look like.

Retargeted at the helper with the same mutation. The rule this leaves behind: **when code
moves, grep the mutation script for the text that moved.**

### What the after-pass found, including a false statement in this round's own code

The finished diff went back to the panel, and two seats independently reached the same
defect: **FEX and VX are preserved where they should be recomputed.** Stopping the four
new instructions from *writing* those bits is only half of what Book I says. It defines
them as derived — VX is the OR of the invalid-operation causes, FEX the OR of the enabled
pending exceptions — so "cannot alter explicitly" is not "keep the stale value". This
fork stores them. The sharp case is one **this round made reachable**: three of the four
instructions that may clear an exception bit did not exist before it, and now a guest can
clear the last VXSNAN through `mcrfs` or `mtfsb0` and be left with **VX set and no
cause**, which hardware cannot produce — copied into CR1 by every record form thereafter.

A comment written in this round claimed all five move-to-FPSCR instructions mask FEX and
VX out of what they write. **That was false**: `mtfsf` does not, and `mtfsf` was in the
list. Corrected, and the reason it is not simply fixed is worth stating, because it is not
laziness — masking `mtfsf` too would make the behaviour *worse*. Its unmasked write is
currently the only way out of the phantom-VX state above. Remove it without adding the
recompute and the phantom becomes permanent. The mask and the recompute have to land
together, which is what #61 now says.

Two smaller corrections to this round's own commentary, both from the same pass: `mcrfs`
clears nothing in **three** of eight fields, not four (field 3 clears VXVC while keeping
FR and FI); and the claim that rounding-before-range-check meant status bits could be
added later "without moving anything" is **wrong for RZ**, where the helper deliberately
returns the operand unrounded and lets the cast truncate — so `2147483647.9` takes the
saturation branch though its converted value is in range. Same 32-bit result today, a
false VXCVI the moment those branches drive status.

### Gate 15

New: 28 rows, 22 checks. It is a **liveness** gate and nothing more: it proves each
encoding no longer stops the emulator, and inspects neither FRT, FPSCR, nor CR1. A wrong
shift in `update_cr1` would pass every check in both PowerPC gates. The semantic rows
that would close that — CR1 content per dot form, the eight `mcrfs` masks, `fctiw` under
all four modes with named tie vectors, `fsel`'s NaN and −0.0 arms, `fnabs`'s payload
transport, and the four repaired sticky sites (`fsub`, `fdiv`, `fmadd`, `fmsub`) the new
rows do not reach — are listed in #61 rather than implied to exist. Every encoding is built **from fields** rather than typed as hex,
and each row prints both the five-bit and ten-bit extended opcode — an A-form word reads
back as `xo10=125` where its real XO is 29, which is exactly how a wrong field hides
behind a plausible-looking number. Gate 13 grows to 94 rows / 63 checks.

## Seventy-third round (#324, #325) — two PowerPC corrections, and a gate row that was measuring the wrong register

### #324 — mtfsf spread its mask across sixty-four bits

The FPSCR is eight **four**-bit fields and the FM field has one bit per field, so
the decoder builds the write mask a nibble at a time. It shifted by **eight** bits
per iteration while ORing in four:

```c
	for (bi=7; bi>=0; bi--) {
		ic->arg[1] <<= 8;
		if (iword & (1 << (17+bi)))
			ic->arg[1] |= 0xf;
	}
```

so the mask sprawled across sixty-four bits. The first four FM bits landed entirely
above the 32-bit FPSCR and wrote **nothing**; the rest wrote the wrong fields.
Measured with every field selected and a source of all ones, the register came back
`0x0f0f0f0f` instead of `0xffffffff`; `FM=0x80` wrote nothing at all; and `FM=0x01`
was correct only by the coincidence of being the final iteration, with no shift
after it. One character: the stride is 4.

This is why gate 13 sets FPSCR by **debugger write** everywhere rather than through
the guest's own `mtfsf`, and why its mode rows read FPSCR back afterwards: a mode
that silently failed to take would have turned every directed-mode row into a second
copy of the RN row. That precaution is what made this finding possible — had the
gate driven the mode through `mtfsf`, the defect would have been baked into the
measurement instead of exposed by it. The debugger write stays for exactly that
reason, and `mtfsf` now has six rows of its own.

### #325 — fctiwz converted a NaN to zero

The ISA gives a NaN the same answer as an operand below the representable range:
the most negative value. This returned **zero**, which is the worse kind of wrong —
a legitimate result the guest cannot distinguish from a successful conversion of
0.0. Two lines.

### The part worth reading: the row that recorded that divergence never measured it

`fctiwz`'s defect has been pinned in gate 13 as a known divergence since #304, with
its committed answer recorded as `00000000`. **That row was not measuring `fctiwz`
of a NaN.** Its instruction word was `0xFC00001E`, whose frB field is **zero**, so
it converted `f0` while the probe seeded the operand into `f1`. The answer was zero
because it converted an empty register.

The source reading behind the original filing was right, and the row that appeared
to confirm it was measuring something else that happened to agree. Two independent
wrongs producing one plausible number is exactly the failure this harness exists to
prevent, and it survived a round-69 five-seat review and every run since.

It was caught only because the fix did not change the row. Chasing that produced
the diagnostic that mattered: **`fctiwz` of 1.0 also returned zero**, which no
theory of the NaN path can explain.

Two things follow, and both are in the gate now:

- The scope is exactly one encoding. Every other hand-assembled word in that probe
  was decoded field by field and is correct — `FRSP_F0_F1` genuinely has frB=1, so
  #304's verification, which is most of this gate, stands.
- The new **`fctiwz 1.0 control`** row is the one that could have caught it from the
  start. With a wrong frB the answer is zero for *any* operand, and every existing
  `fctiwz` row expected `0x80000000` or `0` — values a broken encoding can produce
  by accident. A row whose expected answer is small and nonzero cannot.

That is the third time in this project a hand-assembled encoding has nearly
manufactured a finding, and the first time one reached a committed gate.

### The after-pass: two seats disagreed about the ISA, and the ISA answered

The five-seat review of the finished diff split on one question — what `fctiwz` owes
for an operand that is too *large and positive*, a branch neither correction touches.
One seat held that PowerPC saturates to `0x7fffffff`. Another held that PowerPC uses a
single invalid sentinel, `0x80000000`, for every bad operand the way x87 does, and
filed the unchanged branch as a defect the round should have fixed.

Settled from Book I rather than by counting seats. The instruction's own definition:

> If the operand in FRB is greater than 2^31 - 1, then bits 32:63 of FRT are set to
> `0x7FFF_FFFF`. If the operand in FRB is less than -2^31, then bits 32:63 of FRT are
> set to `0x8000_0000`.

and Appendix A.2's model splits the invalid cases three ways: **Infinity Operand** and
**Large Operand** both branch on sign, while **SNaN Operand** and **QNaN Operand**
return `0x8000_0000` unconditionally. So the existing branch is right, the proposed
change would have been a regression, and #325's unconditional `0x80000000` for NaN is
right for both NaN kinds and both signs.

One thing had to be checked before that conclusion held, because #325 could have
broken infinities by accident: `ieee_interpret_float_value` does **not** set `nan` for
±Inf — it takes the `zero_or_no_reasonable_result` path, which applies the sign — so
`frb.nan` is false for infinities and they still reach the sign-dependent branches.
Had that function classified Inf as NaN, #325 would have turned `fctiwz(+Inf)` from
`0x7fffffff` into `0x80000000`.

The disagreement was worth having: it landed on a branch with **no gate coverage at
all**. Four rows now pin it — `+Inf`, `-Inf`, `2^31`, `-(2^31+1)` — so the misreading
that was proposed here cannot be applied later without a gate going red.

### What the same pass found in the gate rows themselves

Three more, each from a different seat and each verified before being acted on:

**The `mtfsf FM=0x80` row blesses a defect.** Field 0 is FX, FEX, VX, OX, and Book I's
own note says FX and OX come from `(FRB)32` and `(FRB)35` while *"Bits 1 and 2 (FEX and
VX) are set according to the usual rule ... and not from (FRB)33:34"* — they are OR
summaries and `mtfsf` must never copy them. This emulator copies all four, so it answers
`f0000000` where hardware answers `90000000`. Two seats found this independently. The row
stays, because it is what measures #324's field placement, but it is now labelled as
recording a divergence rather than conformance, and **`FM=0x40` was added as the clean
companion**: field 1 carries no summary bits.

That companion turned out to be the row worth having for another reason. Field 1 holds
**VXSNAN** — the sticky bit #304 made the emulator set, and which `frsp`'s own comment
names `mtfsf` as the guest's way to clear. Under the old stride, field 1's nibble landed
at bits 48–51, above the 32-bit FPSCR. **The guest could not clear VXSNAN at all.** #324
is what makes that documented path real; nobody had connected the two defects.

**Every `mtfsf` row measured only half the handler.** All of them started from a zeroed
FPSCR and wrote ones, so `fpscr &= ~mask` could have been deleted entirely and all four
would still have passed. One row now preloads all ones and writes zeros into the selected
field, so the clearing half is measured too.

**`fctiwz 1.0` cannot pin round-toward-zero.** An integer converts identically under
every rounding mode, so a decode that reached `fctiw` (XO 14, rounds per RN) instead of
`fctiwz` (XO 15) would pass it. `1.9 → 1` and `-1.9 → -1` separate them; nearest would
give 2 and -2. The control row was doing the job it was added for — proving the operand
register is read — and none of the job its name implied.

One caveat is recorded rather than acted on: the `>= 2147483647.0` / `<= -2147483648.0`
comparisons give the right *result* for every operand, but they are not a correct
*classification* of which operands are out of range. The model range-checks after
rounding, so under round-toward-zero an operand stays convertible while
`x < 2147483648.0`. Anyone who later reuses these branches to raise VXCVI will flag
exact endpoints and the fractional fringe that are not invalid at all.

### Still open in this cluster, deliberately

`fmuls`, `fadds`, `fsubs` and `fdivs` are bare aliases of their double-precision
handlers, each with a `/* TODO */` — they do not narrow at all. That is not a
one-liner: doing it properly means computing in double, rounding once to single
under FPSCR's mode, and representing the result back in double, which is #308's
round-to-odd machinery plus rounding-mode plumbing this round did not build. The
exception-enable bits (OE/UE/VE) and the FPRF class field remain unmodelled, and
the splice-letter divergence at ~2^129 stays a deliberate policy pin.

## Retrospective review of round 81 (#318) — the code stands, one bug record did not

Part of the standing rule that shipped work gets a panel pass after the fact, not only
before. #318 (the SH-4 store-queue flush with the MMU on) was re-reviewed against the
SH7750 manual and comes back **correct**: the exception-XOR-store property holds (a
failing translation returns before the copy loop, and every failing path inside
`translate_via_mmu` raises through the `exception:` label), the store-family EXPEVT/TEA/
PTEH/SPC state is right for the guest to fault and retry, translating the *unmasked*
address and masking the *result* is what preserves bits [9:5] as the manual requires, and
the write classification is load-bearing rather than cosmetic — a read classification
would let a flush to a clean page skip `EXPEVT_TLB_MOD` and lose the dirty bit, which is
exactly what gate 10's `sq at1 clean` row pins.

**What did not survive is an entry in `OUTSTANDING_BUGS.md`.** It claimed the store-queue
identity mapping ignores address bits [25:6], "so a guest filling a queue through a
non-zero offset stores where the flush will not read it". That is false. `memory_sh.c:301`
passes the **full** virtual address through, and the store-queue device wraps its index
with `% sizeof(d->sq)` (`dev_sh4.c:952`), so bits [5:0] — the queue select and the offset
within it — survive intact and an aliased fill lands exactly where the flush reads. That
is hardware's own don't-care treatment of [25:6], not a defect.

It was a bug report filed against correct behaviour, and it had been sitting in the queue
as scheduled work. Corrected in the record and withdrawn from round 82's task, with the
reason kept: a false entry in a bug list is not free — it costs a future round the time to
re-derive it, and it is the same dishonest-listing class #270 exists to prevent. The
review also noted a genuine gap the round did not have: gate 10's store-queue rows assert
the memory effect but pin none of the exception registers, so a regression that swapped
the store-family event codes for load-family would pass everything except one row. Folded
into round 82, which is already building the user-mode witness those rows need.

## Not changed (assessed, intentionally left)
- ELF64 `st_name` "truncation" — **false positive**: gxemul's `exec_elf.h` defines
  `Elf64_Half = uint32_t` (32-bit), so it is not truncated.
- Signed `byte<<24` assembly in the **CPU instruction cores** (e.g. `cpu_arm_instr_loadstore.c`,
  found via the per-device runtime fuzz) — UBSan-only, deterministic, hottest code path. The
  shared file-decoder source (`unencode`) is now fixed (#27); the per-arch instruction load/store
  assembly is left (whack-a-mole across every core, no real bug).
- a.out timeout signature — the emulator *running* a loaded garbage program until timeout
  (expected behaviour, not a loader bug).
