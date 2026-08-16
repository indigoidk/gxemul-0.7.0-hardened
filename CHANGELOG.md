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
round") + the user's directive (keep ALL bounds checks for unvalidated ROMs, add just-enough rate-limited
verbosity, never crash). No bounds check removed.
| File | Corr. | What changed |
|------|-------|--------------|
| `devices/dev_osiop.c` | #118 | NULL guards in read_word/read_byte/write_byte + `osiop_hostpage_fault()` (warn-once + stop-script) + early-return in execute_scripts_instr — fixes a real host NULL-deref crash |
| `devices/dev_osiop.c` | #114 | NULL-`xferp` data phase: quiet skip+fake-completion → warn-once + stop-script + return (no fake, no exit) |
| `devices/dev_scc.c` | #101 | `% N_SCC_PORTS` alias → bounds-check + NO-OP out-of-range + warn-once (the bound kept, no aliasing) |
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
A whole-tree code review by **Codex CLI `gpt-5.6-sol`/ultra** (report
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
| **#183** | Cdx.2 | **HIGH** | `console/x11.c`: `x11_fb_resize()` computed the XImage allocation `new_xsize*new_ysize*alloc_depth/8` in 32-bit `int`; a guest-reachable resize within #156's 16384/axis cap (e.g. 12000×12000×32bpp) overflows `int`, under-allocates, then `XPutPixel` overruns the buffer → out-of-bounds host write on X11 builds. **Fix:** widen the arithmetic to `size_t`. |
| **#184** | Cdx.4 | MED | `devices/dev_fb.c`: the `dev_fb_resize()` too-small (`<10`) branch still did `exit(1)`; guest-reachable via GBE `HCMAP`/`VCMAP` written with a tiny/zero dimension → emulator-abort DoS. **Fix:** reject and keep the old framebuffer (return), matching the sibling `>16384` branch (#156 idiom). |
| **#186** | Cdx.6 | MED | `devices/dev_mb89352.c`: a valid guest `SCMD_XFR` with an unimplemented `PCTL` phase (4/5/6) hit `exit(1)`. **Fix:** log + `break` (#119 idiom). |
| **#187** | Cdx.7 | MED | `devices/dev_pvr.c`: eight guest-reachable PVR **MMIO register-write** `exit(1)`s (STARTRENDER read; OB_ADDR / TILEBUF_ADDR / TA_OPB_START / TA_OB_START unknown-bit; DIWCONF magic; TA access-len; and the default unhandled-register case). **Fix:** log-and-continue (mask-and-`DEFAULT_WRITE` / `break`), matching #166/#176. |

Provenance/severity: **#182 CRITICAL** overturns the Fable-panel-only "memory-safety clean" read — a genuine
out-of-bounds framebuffer write, latent in pristine upstream, exposed by any framebuffer that shrinks (SGI GBE, or
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
| **#211** | `cpus/cpu_mips.c`: an Address Error (AdEL/AdES) or VCE now updates **only BadVAddr**, not Context/EntryHi/XContext — real R3000/R4000 write those only on TLB Mod/Refill/Invalid. Stops the emulator polluting the CP0 fault fingerprint on the misalignment / kernel-touch faults a controlled-PC fault reaches. |
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
Two document-only items: the R3000 BEV=1 bootstrap-vector base (`0xbfc00200` vs `0xbfc00100`; off the fault
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
  rounded down to the IC index instead of raising instruction-fetch AdEL — so a controlled-PC fault that landed
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
OpenBSD 2.2 pmax/arc behaviour review. Recon found the fork already implements most of the TODO debugger wishlist
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
GCC relies on that undefined behaviour. Rebuilding pristine `39748e3` with
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
  decision below (UBSan-only, hottest path, no reachability path; the shared decoder is already fixed in #27).

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

## R7 (#433) — an ordinary guest register read terminated the host, on the rig that boots
`DEVICE_ACCESS(m8820x)` and its command helper carried five `exit(1)` calls. Measured before any
edit, driving every word offset in the mapped window with each probe forked so one host kill did
not end the run: **1007 of 1024 reads and 1009 of 1024 writes terminated the host process** — and
`dev_m8820x` is memory-mapped twice per CPU on **luna88k, which boots in this tree**. Unlike the
footbridge rounds, this one had a rig.

**Nine seats on the design. The measuring seat BOOTED the guest with instrumentation** — the
first time in this sequence that the central question could be settled empirically rather than
argued. A real OpenBSD/luna88k boot touches **17 of 1024 words and 7 of 256 commands, every one
already handled, and reaches none of the five exit sites**. The instrumentation was
vacuity-checked first: the same binary emits an `EXITSITE` line the moment a probe does reach the
default arm.

*** THE MOST REACHABLE EXIT WAS NOT THE DEFAULT ARM, and that reframed the round. *** Commands
`0x34` and `0x24` reach `exit(1)` through **`CMMU_SCR` — an offset the model FULLY HANDLES, and
which this guest writes 640,016 times per boot.** `0x34` (FLUSH_SUPER_LINE) is ONE BIT from
`0x35` (FLUSH_SUPER_PAGE), which the guest issues 158,664 times. The exposure was a
one-bit-different command on the hottest path in the device, not an obscure reserved offset.
Reachability is one supervisor-mode instruction, measured with every probe word disassembled
before stepping; the control row returns `r4 = 0x00a90000`, the real IDR value, which can only
have come through the device.

*** AND THE ADJUDICATION CAUGHT THAT THE FIX WOULD HAVE INTRODUCED A WORSE DEFECT. *** Converting
the default arm to complain-and-continue — which is the rest of this round — would have turned
`FLUSH_SUPER_LINE` into a **silently ignored TLB flush**. Before this round it died loudly, so no
silent path existed. `memory_m88k.c:190-234` is the translation fast path and a valid matching
PATC entry SHORT-CIRCUITS the table walk, so a guest that edited a PTE and issued the flush would
keep translating through the torn-down mapping. **So the fix and the fold are one change**, and
the seven commands that were falling through are folded in the same diff: the four PATC variants
(`0x30 0x32 0x34 0x36`) into the flush arm — LINE takes PAGE's settings since a line lies within a
page and the PATC is page-granular, SEGMENT takes ALL's since over-invalidation is safe in a model
that re-walks on a miss — and the three cache variants (`0x16 0x1a 0x1b`) into the no-op group,
for the same reason as the nine already there.

- **All five sites become complain-once-and-continue.** The default arm returns the `regs[]` value
  on a read and drops the write; `CMMU_IDR` write, `CMMU_SCR` read and `CMMU_SSR` write are
  access-SHAPE refusals rather than model gaps and are ignored; the command default — now exactly
  the two PROBEs and undefined values — complains and drops.
- **Nothing halts, and that is precedent, not preference.** The tree already assigns two shapes to
  two MEANINGS: `#220` uses `cpu->running = 0` at `dev_footbridge.c:348` because THE GUEST ASKED
  THE MACHINE TO HALT, and complain-and-continue at `:379` for a model gap. Neither m8820x site is
  a halt request. The adjudicating seat had proposed halting on the command default and **revised
  on the measurement**, because that would have parked session-death one flipped bit from a
  command issued 158,664 times a boot.
- **The MMU objection was answered by measurement, not argument.** Every register the emulator's
  own translation consults — `SAPR`/`UAPR` read at `memory_m88k.c:135,137`, `PFSR`/`PFAR` written
  at `:382-405` — is a HANDLED case label. Nothing reaching the default arm can alter what the
  emulator translates. The defined-but-unhandled registers are all cache diagnostics against a
  model with no cache, and the neighbouring `CSSP0` arm already answers exactly this way, silently,
  on a path a real boot exercises 1024 times.
- **The complaint is LATCHED, per device instance.** 640,016 SCR writes in 132 s is ~4,850/s, so an
  unlatched `fatal()` is a guest-drivable stderr flood — the `cflood` class — at roughly a quarter
  of a megabyte per second. First hit reports in full and names the instance; the rest go to
  `debug()` so `-v` keeps the stream.

**The detector is offline for BREADTH and the kill criterion is the EXIT STATUS.** That is not a
detail: the first reproduction of this defect got its headline number wrong by exactly six in each
direction, because the register-file arm calls `invalidate_translation_caches()` BEFORE the
writeflag check — so it fires on READS — and the driver had left that callback NULL. Six offsets
crashed in the HARNESS and were counted as device kills. A review seat derived 1007/1009/17 from
the source alone and named the mechanism; re-measuring with the callback installed and status 1
distinguished from a signal matched it to the offset. `regress/diff_m8820x.c` installs the callback
and reports a signal death as a FAULT, never as a detection.

**Verified:** differential **15 rows / 0 failures**, including the whole-window sweep (0 kills, 0
harness faults, against 1007/1009 before), the latch row, the white-box PATC row that defends the
fold, and both fold controls. **The re-run reproduction goes 1007 → 0.** Gate 2 **PASS at 195
checks** (was 184). **luna88k boots to a shell: `VERDICT=PASS`, both FP values correct, and ZERO
m8820x complaints** — the latch never fires on a clean boot, which is the census confirmed from the
other side. `gate_mips.sh` PASS 6/6. `dev_m8820x.c` byte-identical in `GXEMUL-SEC`, `est/` and both
build trees. **`mvme187` instantiates the same device and inherits the fix for free.**

**Filed, not fixed:** real PROBE semantics (`0x20`/`0x24`) — a dropped probe leaves `SSR` at zero,
V-bit clear, a deterministic "no valid translation" rather than a plausible-looking valid answer,
and the measured guest issues no probes at all; the register-file arm invalidating every
translation on a plain READ; and the `exitsweep` inventory, which this round now supplies a worked
exemplar and a detector template for.

## R6 (#432) — a guest-written zero made the footbridge timer divide by zero, and killed the host
`DEVICE_TICK(footbridge)` computed `random() % timer_load[i]`, and `TIMER_x_LOAD` accepts a
guest-written zero. Integer division by zero: the HOST process dies. Two seats reproduced it
independently, and it is **SIGFPE (exit 136) at every optimisation level** — measured at -O0, -O1,
-O2 and -O3 with gcc 15.2.1. An earlier draft of this block said "SIGILL at -O2, where the compiler
turns the UB into `ud2`"; that is wrong for this code. The divisor here is a runtime
`d->timer_load[i]`, so nothing is constant-folded and a real `div` is emitted — the `ud2` behaviour
needs a divisor the compiler can PROVE is zero, which is a standalone repro rather than this path.

**NINE SEATS ANSWERED THE DESIGN BRIEF — the first full roster since #420**, and two of the nine
had been believed down when the round opened. Kimi revived mid-panel with no calendar signal and
reproduced the crash itself; the Fable seat health-tested clean on the way in and then held the
adjudication alone.

**THE ROUND DOES NOT GET TO BLAME ITS OWN HARDENING, and finding that out was the review's best
work.** The filing said "#427/#428 convert a hang into a SIGFPE". Half wrong. There are two
routes, and the measuring seat found the second by RE-DERIVING the reproduction rather than
citing its own earlier run: `TIMER_x_LOAD` does not clear `pending_timer_interrupts` — `TIMER_x_CONTROL`
does — so an ORDINARY LEGAL timer accrues a backlog and a later write of zero divides, with no
`+INF` and no clamp involved. Measured against `863d238^`, the pre-#427 core: it crashes there
too. `DEVICE_TICK` runs from `machine_run()`, the main loop, not the signal handler, so the CPU
reaches the divide between signals. **The crash is pre-existing; our hardening added a second,
faster route.** Corrected in `213b56d` before this fix shipped.

**NONE OF THE THREE OBVIOUS FIX SITES IS SUFFICIENT, and that was settled by measurement rather
than by the 8-to-1 majority.** Guarding only `reload_timer_value()` still crashes by route 2 —
and it is the most dangerous option precisely because it passes the obvious test. Guarding only
the modulo leaves the backlog growing 1,048,576 per signal, reaching `INT_MAX` in ~31 s. Rejecting
at the guest write corrupts read-back: `TIMER_x_LOAD` returns the stored value, so the guest would
read something it never wrote — inventing an answer to a question the documentation has to settle.
Three seats (Codex, Opus, Fable) independently proposed the same fourth option, and that is what
ships: **one helper, both consumers, the stored register untouched.**

- **The zero-guard and the width fix are ONE fix or neither works.** The old `int cycles` with
  `cycles <<= 8` overflowed for exactly half the legal 24-bit range (first bad load `0x800000`),
  giving a NEGATIVE frequency that the core's floor clamp silently turned into one tick per ~3.2
  years — reachable with NO load write at all, since a single write of `ENABLE|FCLK_256` reaches
  it. And mapping zero to 2^24 while leaving `int` gives `2^24 << 8 == 2^32 == 0`, i.e. `+INF`
  again: **the obvious zero-guard RE-CREATES the bug it removes.** Three seats found the overflow
  independently. Hence `uint64_t` and multiplication, never a signed shift.
- **The two consumers live in different domains**, which a tenth reading caught. `timer_value` is
  a 24-bit GUEST-READABLE register; feeding it the PRESCALED span would store values far above 24
  bits — the measuring seat's own first proposal did exactly that and put 19,833 of 20,000 ticks
  out of range. The prescaler slows the RATE; it does not widen the COUNTER. The helper takes an
  explicit flag and the differential asserts the distinction.
- **`TIMER_EXTERNAL` no longer kills the host.** Both prescaler bits set is `0x0C`, and the
  datasheet obtained for this round gives bits 3:2 as 00/01/10/11 = fclk / fclk÷16 / fclk÷256 /
  **External event** (§7.3.41, p. 7-51) — a CONFORMING guest selecting the external clock source
  was reaching `fatal()` + `exit(1)`. The rate an external source would give depends on a pin this
  model has no signal for, so it is not invented; the encoding gets a defined, survivable meaning.

**THE DATASHEET WAS OBTAINED MID-ROUND** (`_scratchpad/dc21285.pdf`, Intel 278115-001, Sept 1998,
with a `pdftotext -layout` twin beside `ddi0100i`), and it did two things. It CONFIRMED the
`TIMER_EXTERNAL` encoding above. And it carries no direct statement about a zero load — §7.3.39
specifies `TimerNLoad` without saying what a count of zero does, and a search of the full
extraction for "minimum count" / "nonzero" / "reaches zero" finds no equivalent of the 8254's
Figure 22. So the mapping is **UNKNOWN by search rather than by assumption**, which is a stronger
thing to be able to say.

**Except that "silent" overstates it by half, and pass 2 caught that too — in the round's own
favour.** §7.3.41 bit 6 says a free-running timer "will wrap to FFFFFFh and continue to decrement",
which with §6.4's 24-bit down counter DETERMINES the free-run case: a load of 0 gives a period of
exactly 2^24, i.e. the shipped mapping is datasheet-IMPLIED there, and free-running is bit 6 == 0,
the reset mode. Genuinely unknown only for periodic. And the failure-asymmetry argument as written
weighs two alternatives when there are three: read mechanically, periodic mode with a zero load
reloads zero and interrupts every prescaled clock — a max-rate storm, which is the DANGEROUS
branch, not the silent one. The shipped mapping avoids that too. The conclusion is unchanged and
the argument was understating its own robustness. The choice rests on failure asymmetry (wrong-and-noisy beats wrong-and-silent: a
guest that gets a few unwanted interrupts limps visibly, a guest waiting on a tick that never
comes hangs at boot) and on arithmetic (the 24-bit mask aliases a legitimate write of `0x1000000`
to zero, so full-period is the unique choice that keeps the rate continuous across the register's
own truncation).

*** AND THE DATASHEET WITHDREW ONE OF THIS ROUND'S OWN ARGUMENTS. *** An earlier draft justified
the mapping partly with "devinit resets every load to `TIMER_MAX_VAL`, so the model's own
convention is full width". The datasheet says `TimerNLoad` and `TimerNControl` BOTH reset to 0 —
so that line was citing a MODEL BUG as evidence. The argument is withdrawn, the reset divergence
is filed, and the withdrawal is recorded here because it matters more than the argument did.

**The detector is offline because it is the ONLY thing it can be:** there is no netwinder or cats
rig anywhere in this tree, so nothing here boots a machine that has a footbridge.
`regress/diff_footbridge.c` `#include`s the shipped device exactly as `diff_sh4_tmu.c` does, needs
seven stubs, and runs **19 rows** (15 as first shipped; pass 2 added four). `-Wl,--gc-sections` is
load-bearing (eleven more symbols without it) and its cost is stated: it drops `DEVINIT`, so this
file cannot test devinit.

*** THE FORK RATIONALE AS FIRST WRITTEN WAS FALSE, and two seats measured it independently. ***
This block originally said "two of them fork, so a mutant that re-crashes is a named-row KILL
rather than a census FAULT that takes the gate binary with it." **D2 is UNFORKED and reaches the
divide first**, so any unconditional re-introduction of the crash kills the binary there, before
F1's fork — including the very mutant this round exists to prevent. What is true and narrower:
G1's fork IS load-bearing (the CONTROL-arm `exit(1)` is reachable nowhere else in-process), and
F1's contains one constructible class (a zero-guard conditioned on the prescaler bits survives D2,
whose control carries FCLK_256, and dies only in F1, whose control is bare ENABLE). Detection was
never at risk — every gate grep fails on a truncated log — so this was a WRONG RECORD rather than
a coverage gap, which is exactly the class the stopping rule says to fix rather than file.

**Census: 5 attempted, 4 killed, 0 survived, 0 faults**, control passes — the zero guard removed
(dies by signal, the crash itself), the prescaler back to a signed shift, the tick site
prescaling, and `TIMER_EXTERNAL` falling through as a bare ×16. A further mutant, the ×16 prescaler
as a signed shift, is **EQUIVALENT and deliberately not counted** — calling it a survivor would
overstate the detector's weakness exactly as calling it a kill would overstate its strength. The
REASON first given here was wrong even though the verdict was right: it said "2^24 << 4 cannot
overflow an `int`", but `cycles` is a `uint64_t`, so `int` overflow was never the question. **It is
the TYPE that makes it equivalent, not the magnitude** — on a `uint64_t`, `<<= 4` and `*= 16` are
the same operation for every value in range.

**Pass 2 then found three mutants that DID survive all fifteen rows**, and each is now killed by a
row written for it. (1) Changing the `1` to a `0` in `reload_timer_value()`'s helper call — **one
character** — silently deletes the prescaler from the RATE domain for every guest, asking for
100000 Hz where the correct answer is 390.625. Sections B and C proved the HELPER prescales and
D1/D2 proved the COUNTER consumer does not, but nothing pinned the RATE consumer, which is this
round's headline design decision; E2 was a sign-only oracle. (2) Replacing the tick's helper call
with the constant 16777216 passed everything, because every tick-path row used `load == 0` — for
which that constant is exactly right. (3) Reinstating normalize-at-write, **the precise alternative
this round rejected**, passed everything, because no row drove `TIMER_1_LOAD` through the access
handler at all: "the guest reads back exactly what it wrote" was a shipped, load-bearing claim with
no detector — the fifth vacuity class. Census now: **8 attempted, 7 killed, 0 survived, 0 faults.**

**Verified:** differential **19 rows / 0 failures**; gate 2 **PASS at 184 checks** (was 171); both
build trees rebuilt and the arc binary republished; **`gate_mips.sh` PASS 6/6** — pmax 15/15 and
arc 13/13, both to `uid=0(root)`. `dev_footbridge.c` byte-identical in `GXEMUL-SEC`, `est/` and
both build trees.

## R5 (#430, #431) — memory_rw translated the first page and then copied straight past it
`memory_rw()` translated the START vaddr once and then copied the whole length from the host
pointer for that one page. `memory_paddr_to_hostaddr()` returns a pointer INTO a 1 MB
memblock, so the copy walked host memory that is contiguous PHYSICALLY while the guest's span
is contiguous VIRTUALLY. Those coincide only by luck, and the moment the length ran past the
page boundary the guest read — or wrote — the physical page that happened to follow.

**The split that was already there is not this guard**, and it is easy to mistake for it: the
one at the end of the function fires at `BITS_PER_MEMBLOCK` (1 MB) granularity — one boundary
in 256 — and its job is to stop the `memcpy` running off a host allocation. It is a
host-bounds guard, never a page guard.

**The write side was worse than the read side, and the round nearly missed it.** The design
brief described #47 as reading the wrong page. Driven offline, a straddling STORE leaves the
guest's intended page unmodified and writes into an unrelated one instead. And a third
consequence nobody had named: when the tail page had no valid translation the old code
returned `MEMORY_ACCESS_OK` and wrote anyway — so this was a MISSING FAULT as well as a wrong
page. Both were found by building the instrument, not by reading.

- **#430, the split, placed BEFORE device dispatch.** The shipped body becomes a `static`
  one-page worker; a wrapper of the same external name loops over page-sized chunks. Placing
  it here rather than at the memblock check is not a preference — it was MEASURED. A late
  split leaves a straddling access that begins inside a device broken: the device length clamp
  truncates the length and the zero-fill supplies the rest, so the guest gets `d0 d0 00 00`
  where the correct answer is `d0 d0 bb bb`. One review seat dissented for the late split and
  that row is what settled it, rather than a vote.
- **A LOOP, not recursion** — the right implementation, for a reason the round had to correct.
  The first draft said "gcc does not turn the tail call into a loop at -O2". **Measured, it
  does**: gcc 15.2.1 performs the sibling-call optimisation at -O2 and -O3, leaving a 96-byte
  span. The loop is still correct — it does not depend on an optimisation being applied, and
  -O0 builds and other compilers are real, where a recursive split measured 1,834,896 bytes of
  stack for a 16 MB access — but **the row certifying it was VACUOUS**, passing under the very
  mutation it existed to catch, until the differential was given
  `-fno-optimize-sibling-calls`. With that flag: loop 0 bytes, recursion 1,572,768, row RED.
  One compile flag turned a decorative row into a detector.
- **Only when a translation actually happened.** Under `PHYSICAL`, or with no `translate_v2p`,
  `paddr == vaddr` and there is no per-page mapping to redo, so those go straight through.
  Without that exemption a 16 MB DMA would turn one call into four thousand; with it, the
  memblock split stays alive and load-bearing instead of becoming dead code.
- **The page size moved to one macro**, and the SPLIT GRANULE turned out to be a different
  number again. The mask is the HOST-page granule (8 KB under `MEM_ALPHA`, not 4 KB — one seat
  caught that the brief had said "4 KB page" throughout). But the granule the split needs is
  the smallest unit at which a translator here can send adjacent virtual addresses to unrelated
  physical ones, and **that is 1 KB**: `memory_arm.c:198-207` is a 1 KB page on any non-XScale
  core, `memory_sh.c:116` has `SH4_PTEL_SZ_1K`, and the VR41xx MIPS path likewise. A pass-2 seat
  produced the counterexample against the first draft — a four-byte read at `0x13fe` crosses a
  translation boundary but not a 4 KB one, so the loop never fired and the defect survived
  **exactly where `MEMORY_NOT_FULL_PAGE` says it is most likely**. Splitting finer is always
  safe; the cost is more worker calls on a slow path that large transfers do not use. A bonus
  the same seat noted: ARM *permissions* also change every 1 KB inside a 4 KB page
  (`memory_arm.c:210-232` picks `ap0..ap3` from `vaddr & 0xc00`), so each chunk is now
  permission-checked separately too.
- **The worker's name is derived from `MEMORY_RW`**, because `cpu_alpha.c` includes this file
  TWICE in one translation unit — `alpha_userland_memory_rw`, then `alpha_memory_rw` via
  `tmp_alpha_tail.c`. A plainly named static would have been a redefinition. The
  per-inclusion macros are `#undef`'d at the end of the file.
- **#431, the PPC halt is deleted, not replaced.** `LS_GENERIC_N` printed a TODO and set
  `cpu->running = false` for any access whose bytes crossed a page — legal guest code stopped
  the emulator, and the fast path guaranteed it was reached, because `LS_N` punts every
  unaligned non-byte access there before any page test. It is deleted rather than given a
  local split because the other producers of straddling accesses — `lvx`/`stvx`,
  `lwarx`/`stwcx.`, and the ARM `arm_pop` path — call `cpu->memory_rw` DIRECTLY and never
  passed through this function, so the halt never covered them. `memory_rw` is the choke
  point and #430 fixes it once.
  Checked before deleting, because a loud stub can be load-bearing: no gate, probe, CHANGELOG
  or OUTSTANDING_BUGS entry mentions the message or `LS_GENERIC_N`, and there is no PPC
  alignment exception in this tree to fall back to — `cpu_ppc.h` defines DSI/ISI/EI/FPU/DEC/SC
  and no alignment vector. What real 601-versus-later silicon does is **UNKNOWN**: there is no
  PowerPC manual in this project and none was reconstructed.

**The detector is OFFLINE, and that was the round's open question.** The defect needs two
pages adjacent virtually and NOT adjacent physically, which no rig here can be made to produce
on demand — so the map comes from a stub. `regress/diff_memory_rw.c` `#include`s the shipped
`memory_rw.c` with `MEMORY_RW` defined to a test name and no family macro (the flavour
PPC/ARM/SH/RISC-V/i960 actually ship), and needs six stubs. The expected values are painted
bytes, ABSOLUTE consequences of the fixture — deliberately not constants re-read from the code
under test, which is the `constblind` shape filed the same day.

**PASS 2 FOUND THREE DEFECTS IN THE FIX ITSELF, and they are the reason this block reads the
way it does.** Two were code, one was the detector. (1) The split broke **#244's promise** that
a failed read leaves the caller's WHOLE buffer zeroed: the worker zeroes only the chunk it was
handed, so a fault before the last chunk left the rest as uninitialised host stack — measured,
a 12,288-byte read faulting on its first page left **8,192 bytes untouched**, where the
unsplit code zeroed all of them. The wrapper now zeroes the remainder. (2) `offset + len >
granule` can WRAP for an absurd length, skipping the loop entirely; it is now
`len > granule - offset`, which cannot. (3) The 4 KB granule, above. A seat also FUZZED the
final arithmetic — 40,000 reads and 20,000 writes against a per-byte reference over a random
page *permutation*, **0 divergences**, with the pre-change file as a negative control at
**39,388** — and found a one-line off-by-one (`granule - offset + 1`) that passed all
twenty-one rows while diverging 1,089 times, because no row had a tail of exactly one byte.
Two rows now do.

**Verified:** differential **23 rows / 0 failures**; against the pre-change file
(`git show b9daca1:src/cpus/memory_rw.c`) the SAME differential fails **15 of 23** rows,
including the reproduction, the write into the wrong page, the device case and the missing
fault. Gate 2 **PASS at 171 checks** (was 157). The emulator builds across all eight flavours
including the Alpha double-inclusion, with no warnings naming either changed file. And the
integration half is not left for later this time: **`gate_mips.sh` PASS 6/6** — pmax (R3000)
15/15 harness steps and arc (R4000) 13/13, both reaching `uid=0(root)` on freshly built
binaries. Both changed sources are byte-identical in `GXEMUL-SEC`, `est/` and both build trees.

**A compile-time assert covers what the test cannot reach.** `MEM_ALPHA` is never compiled by
the differential (its fixture is 4 KB-specific), so a seat measured that widening
`MRW_OFFSET_MASK`, or hardcoding the worker's local back to `0xfff` — precisely the drift the
macro exists to prevent — leaves every row green. `MRW_SPLIT_MASK <= MRW_OFFSET_MASK` is now
asserted at compile time, in every flavour including the one the test cannot build.

**Filed, not fixed here:** an absurd length (near `SIZE_MAX`) now grinds rather than
mis-copying — the comment says so plainly instead of implying it is serviced; a straddling
STORE whose second chunk faults leaves the first written, so an MMIO device at the head sees
the write twice when the instruction restarts; this tree's `lvx`/`stvx` apply no alignment mask at all, which is
arguably its own defect rather than evidence for this one; a partial `stwcx.` still holding a
reservation; the ARM 1 KB / mixed-AP subpage sibling; and the observation that every surviving
straddle producer needs an UNALIGNED base, in a tree that models no alignment exception — which
makes #430 latent-but-real rather than routinely hit, and is the honest way to state its
severity.

## R4 follow-up — the round's detector certified six things it could not see, and its census entry was wrong
Nine seats were asked for R4's review; eight answered (the Fable seat was deliberately not
fired — the owner had warned of its hourly limit and it is reserved for the Sunday
regression batch, so that cell is a DEFERRAL, not a seat failure). **Every one of the eight
found a defect in the round's own instrument, and three of them MEASURED it.** No emulator
behaviour changes here: this is the detector, the gate wiring, and four wrong records.

**The finding that matters most is the shape of the others.** Every row in the differential
took its expected value FROM THE HEADER — the rule #425 established, because a transcribed
constant cannot notice drift. But a row that reads the constant is **green for any value of
it**. Three seats independently measured the consequence: `TIMER_MAX_CATCHUP` → 65536,
`TIMER_MAX_FREQUENCY` → 32768.0, and `TIMER_MIN_FREQUENCY` → 1e-300 each break a property
the round claims and pass every row. Reading the constant defeats transcription drift; it
cannot notice the constant being WRONG. **The answer is both** — read it, and also assert an
absolute consequence derived from outside the header. Hence a 40 MHz row (the pmax rate, so
it is the offline half of a case the battery boots), a structural
`TIMER_MAX_FREQUENCY == (double) INT_MAX`, and a floor-is-a-reachable-duration row.

**The stall was inert, and the row named for it still passed.** `run_periods()` advanced a
local the handler never reads: `timer_current_time` is advanced by `timer_tick()` itself,
and the `gettimeofday` stub was never called because `fresh()` had disabled the resync.
One seat measured `stall=0.0` and `stall=100000.0` as byte-identical output. The stall now
arms the SHIPPED resync path, and a row asserts the clock really moved — so it cannot go
inert again silently. It must also be DISARMED after one period: `timer_freq` is 0 in this
driver (`timer_start()` is deliberately never called), so the re-arm computes 0 and the
resync would otherwise fire every tick, injecting fresh lag and hiding the very difference
the next row exists to see. That was found by measurement, not by reading — the first
corrected version still let the drop mutant survive.

**The census entry R4 shipped was wrong, and three seats traced the same arithmetic.** It
recorded the drop-at-cap-hit survivor as "inert because the schedule is already ahead of the
clock there". At cap-hit a timer at the ceiling has advanced `next_tick_at` by ~4.88e-4 s
against a `timer_current_time` of ~1.54e-2 s — the schedule is **behind**, by a factor of
about thirty. The mutant survived because the DETECTOR was weak, not because the mutation
was harmless: one seat measured the real cost at **951,424 ticks — 9.51 s of guest time —
silently lost** on a 100 kHz timer after a 20 s stall. There is now a row that tells deduct
from drop, and it needs a case where one signal owes more than the cap and the next owes
less; a maximum-rate timer cannot show it, because both policies saturate.

**The gate's floor was one below the row count, which is the same class the identity row
exists to prevent.** `check_min` stood at 13 while the driver ran 14, so DELETING THE
IDENTITY ROW LEFT THE GATE FULLY GREEN. Two seats read it independently and a third measured
it. A floor set one under the count is not a weaker check; it is no check. It is now the
exact count, and eleven named-row checks make each sole-detector row's deletion a red row.

- **The reporting path had no detector at all.** Deleting `timer_catchup_hit = 1;` from the
  handler passed everything, measured by two seats. `timer_stop()` is now called by the
  driver (it only disarms a timer that was never armed), with a report-once row, a
  flag-cleared row, and a negative control — the last because the first two would pass under
  a mutant that simply reports every time.
- **A row that was green at zero.** "The complaint is made once, not once per write"
  asserted only the delta, so deleting `*was_clamped = 1` — the line that makes the clamp
  complain at all — passed the whole file. An absolute row now comes first.
- **A floor cannot catch a value that is too big.** `interval = 0.5 / freq` doubles every
  timer's rate and sails over every anti-regression floor. A reciprocal-exactness row.

**Measured: 24 rows / 0 failures, gate 2 PASS at 157 checks (was 148). A census of thirteen
mutants in copies kills thirteen and leaves no survivors** — the seven from R4's original
list plus the six the seats measured as passing it, with the unmutated control passing and
the denominator self-checked.

**Four wrong records corrected in the source, none of them behavioural.**
1. *"every rate derived from `emulated_hz` divides by at least one"* — FALSE.
   `dev_footbridge`'s `reload_timer_value()` divides by a guest-written `timer_load` that
   `TIMER_1_LOAD` accepts as ZERO. The conclusion survives and is stronger than the premise:
   before the clamp, `+INF` made `interval` 0.0 and the catch-up loop never advanced — **a
   guest-reachable HANG inside the signal handler, which #427/#428 fix.** That is the
   strongest justification the round has and it was not in the record.
2. *"the remainder is delivered by the signals that follow"* — true only for a RECOVERABLE
   backlog. Above `TIMER_MAX_CATCHUP * TIMER_BASE_FREQUENCY` = 68,157,440 Hz the debt grows
   forever; measured, a ceiling-rate timer sits 0.9683 s behind after one simulated second.
   The domain admits 32x more than the cap can serve. Recorded, filed, not answered.
3. *"the caller reports once per timer"* — measured false: 1000 alternating INFINITY/1000 Hz
   updates give 1000 complaints, because the suppressor is the `t->freq == new_freq`
   early-out, not a latch. A guest alternating two rates drives an unbounded stderr write.
4. *"NOTHING IS PRINTED HERE, in a signal handler"* — true of `timer.c`, and it was being
   read as a claim about the handler. `dev_sh4.c`'s `sh4_timer_tick()` is a callback this
   loop invokes and it calls `fatal()` then `exit(1)` from inside SIGALRM. Pre-existing;
   named so the comment cannot be read as covering it.

**Two properties this instrument cannot reach, now stated in the file rather than implied
as covered:** downgrading `volatile sig_atomic_t` to `int` passes every row because no
signal handler is ever installed (no row *can* catch it), and #429 lives in `dev_rtc.c`,
which the driver does not compile — reverting it entirely leaves the gate green, measured.

**Filed, not fixed here** (the stopping rule: only a measured false pass or a wrong record is
fixed in-round): the `dev_footbridge.c:141` `random() % 0` SIGFPE, which a seat reproduced as
a host core dump and which this round's clamp converts a hang INTO — the highest-priority
residual; the 32x domain-versus-cap gap; the per-timer budget against a four-timer device
(measured at 69% of a host period, inside the band the header's own reasoning rejects); the
complaint flood; `dev_sh4`'s `exit(1)` from a handler; and a `dev_rtc` detector, which needs
the guest-rate narrowing to move into the timer core and so belongs in its own round.

**Verified:** gate 2 PASS at 157 checks; diff_timer 24 rows / 0 failures; census 13/13
killed, 0 survived, 0 faults; `timer.c` and `timer.h` byte-identical in `GXEMUL-SEC`, `est/`
and both build trees, with the stale objects removed.

## R4 (#427, #428, #429) — the timer core clamped one end of a frequency and left the other unbounded
The first round in this sequence to touch the EMULATOR rather than the harness, so all three
source files land byte-identical in `GXEMUL-SEC`, `est/` and both build trees, and the round states
which of its claims are proven now and which wait for a rig.

**The panel's own disagreement was the finding.** Seven seats proposed a frequency ceiling between
32,768 Hz and 10 MHz — a factor of three hundred — and that spread is what a wrong instrument looks
like. The measured harm is not "a high frequency" but ITERATIONS PER SIGNAL in a handler with no
cap: even the largest proposed ceiling leaves ~153,846 of them per signal, while the smallest alters
requests a guest is entitled to make. The ceiling is therefore demoted to domain normalisation and
**the catch-up bound is the protection**.

- **#427, the domain, derived not chosen.** `machine->emulated_hz` is an `int` and every rate derived
  from it divides by at least one, so INT_MAX bounds every legitimate request in the tree;
  `TIMER_MAX_FREQUENCY` is the least clamp that truncates nothing. Both clamps are NaN-safe **by
  negation** — and precisely, because a census measured it: THE FLOOR'S NEGATION IS THE ONE THAT
  CATCHES NaN, since a NaN never reaches the ceiling test at all. The ceiling is negated anyway so
  the two read as one idiom and neither can later be reordered into a hole. The floor is tested
  first, so a NaN lands SLOW rather than fast.
- **#428, the catch-up bound, with the backlog RETAINED.** `TIMER_MAX_CATCHUP` = 2^20 ticks per timer
  per signal, derived from both sides: 65,536 breaks a legitimate 40 MHz timer (delivered rate
  1.0000 → 0.1065), and an iteration costs 2.16–2.82 ns, so 2^22 would fill 59–77% of a host period.
  Dropping missed ticks was rejected BY MEASUREMENT: catch-up *is* the delivery mechanism above
  65 Hz, so dropping caps every timer at 65 Hz and a 100 Hz timer falls to 0.65 of real time with no
  burst at all. The cap hit is recorded in a `sig_atomic_t` and reported from `timer_stop()`, never
  from the signal handler.
- **#429, the RTC narrowing.** `dev_rtc` range-checks in the uint64 domain BEFORE narrowing to `int`,
  because the narrowing is the defect: a guest write of 2^32 — or of 0x8000000000000000 — truncated
  to zero and turned an ADD into a silent REMOVE (both measured), and a write with bit 31 set became
  negative, so a guest asking for the fastest rate got one tick per three years. `idata == 0` keeps
  its documented meaning. `timer_update_frequency` now clamps ABOVE its early-out: clamping at the
  store alone is not merely insufficient but a REGRESSION, measured to lose idempotence on five of
  six input classes because the early-out would then compare a clamped record against a raw request.

**The detector is OFFLINE, which was the round's open question.** `regress/diff_timer.c` drives the
SHIPPED `timer.c` — `timer_tick` is static, so the driver `#include`s the repo file; the one stub is
`gettimeofday`; no signal handler is ever installed, so no host clock enters and the rows are not
load-sensitive. Every constant is READ FROM THE HEADER, never transcribed. 14 rows in gate 2.

**Measured against six mutants in copies:** no ceiling, clamp-below-the-early-out, unbounded
catch-up, both-clamps-written-plainly, and the drop-the-backlog policy all go RED; the shipped file
passes. Two further mutants survived and are recorded as understood rather than waved away: a
plainly-written CEILING survives because the negated FLOOR catches NaN first, and a drop applied
only at cap-hit is inert because the schedule is already ahead of the clock there.

**Three of the round's own test rows went red on correct code** and were fixed as TEST defects, not
code changes — a per-signal bound asserted against a two-period run, and two exact-count rows that a
floating-point period sum lands a hair under. They are floors now, with the arithmetic recorded.

**The pre-commit check caught two things the commit message would otherwise have claimed past:** the
new differential had no IDENTITY row, and all three source files DIFFERED FROM THE BUILD TREES —
the "measuring a stale binary" class. Both are fixed; the affected `.o` files were removed so the
next build is a real one. *(Correction to `863d238`'s message: it says 13 rows; the identity row
makes 14, and it predates the build-tree propagation.)*

**Waits for the battery, stated plainly:** this proves the ARITHMETIC and the POLICY, not the
INTEGRATION. Only a booted rig can show that the twelve untouched callers still boot and keep time,
that a guest writing 0x7fffffff leaves the emulator responsive, and that boot times do not regress.

**Verified:** gate 2 PASS at 148 checks (was 141); diff_timer 14 rows / 0 failures; both changed
source files compile clean; `est/` and both build trees byte-identical on all three.

## R3 (#425, #426) — the gate graded constants the run never used, and a green row said so
Gate 5 range-checks the progress constants the driver reports, and the driver read them TWICE — once
for the call that ENFORCES them, once for the record block the gate GRADES — with nothing tying the
two reads together.

**The hole was observed before it was fixed**, because a predicted false pass is a hypothesis.
Mutating only the call site left control and mutant outputs byte-identical apart from telemetry and
the gate's rows PASSING 11/11, while the run went from stopping at `REASON=BUDGET` with 13 G to
running on to `REASON=STALLED` at 20 G — both printing the same BUDGET. And a luna88k output with
`BUDGET=0` printed, literally, `ok luna88k: budget is deliberately absent (uncalibrated rig)` at
11/11: a GREEN ROW STATING A FALSEHOOD about a rig whose calibrated budget is 12 G, while the
calibrated range never ran. Negative-controlled both ways — landisk's legitimate zero stays green
under both orders.

- **#425** `boot_progress` records its FORMAL PARAMETERS and the record block prints those. Sharing a
  local is NOT enough, and four review seats proposed it: the mutation rewrites the ARGUMENT
  EXPRESSION, so a local — and any print taken from it — stays honest. A local proves what the caller
  INTENDED TO PASS; only the callee's parameters prove what it RECEIVED. The `.get` defaults are
  dropped with it, since `.get("stall", 120)` on both paths would make an omitted key print a PASSING
  120 where today it prints a FAILING 0.
- **#426** `budget_class()` moves to `lib.sh` — which is what makes the branch exercisable offline
  instead of only under a weekly boot — and the gate asks for a CLASS with the calibrated case
  decided before the zero case. Zero on a calibrated rig is `zeroed` and RED, not a skip: the gate
  HOLDS the calibration, so a skip would claim an ignorance it does not have.

**`selftest_budget.py` is the straddle**: it reads `BUDGET=N` from the driver's OWN OUTPUT — never a
literal, because passing literals is the precedent that left this hole open — then runs one leg under
N and one over it. Measured to kill three mutants in copies: the call-site multiply, a multiply AT
THE COMPARISON, and a deleted stop, with the unmutated copy passing. The comparison mutant is the one
no printing scheme can catch.

**The review found five defects, four of them in the file the round added** — the "offline" gate
required the image directory; the straddle passed a LITERAL, the exact practice its own docstring
forbids; an omitted rig key raised after `pty.fork()`; the comment claiming the straddle covers
in-body mutations was measured false twice; and the gate's default want-mapping would auto-bless an
unknown rig's zero. All fixed in `48b36b0`.

**And a defect that SURVIVED that follow-up** (`521085b`): dropping the `.get` defaults decapitated
gate 2's OTHER driver selftest, because a third rig dict declared neither key — and both its rows
kept passing, since the log files are opened before the raise. The wrapper had been reporting the
exception all along, into `DEVNULL`. Caught by TIMING: 1.573 s and fifteen driver lines became
0.062 s and one, still PASS. The wrapper's output is now GRADED, and the negative control states the
defect better than prose: with the keys removed the two log rows STILL read yes/yes while
`driver_ran` reports the KeyError.

**Verified:** gate 2 PASS at 141 checks; selftest_budget 7 rows / 0 failures; selftest_logdir PASS
with `driver_ran=yes` and FAIL under the negative control.

## R2 (#424) — the parser selftest ran nowhere, and could not see a mutant that moves text
`regress/selftest_absorb.py` shipped in r421 to test the pty record parser and was invoked by NO
GATE: dead coverage. The deeper defect was in its shape. Its helper returned `body + tail` and 27 of
its 29 rows compared that SUM, so **any mutant that merely RELOCATES text between the two halves
preserved the sum and stayed invisible** — including one that leaves a completed line in the tail,
where the boot loop never looks, so a guest that reached its milestone is reported as not reaching
it. Nine review seats assessed and researched the round; a measured census settled it.

**THE CENSUS CAME FIRST, IN RESEARCH, NOT AFTER THE FIX.** 22 mutants across the parser's decision
axes — the three hold clauses, which string the hold is taken from, the bound, the record regex, the
strip loop, the return — each applied to a COPY with its substitution asserted to apply EXACTLY
ONCE. Against the SHIPPED selftest: **17 killed, 5 SURVIVED, 0 faults**, and every survivor was
non-equivalent with an executed witness, so none could be retired as equivalent. Naming them, which
is the point: the newline clause (marker unreachable); the `i != -1` guard (a bracket-free read
holds its last character for ever); `<` → `<=` at the bound (the existing row used 400, far past the
shipped 256, so the boundary was never tested); `rest.rfind` → `tail.rfind` (a second record leaks
unstripped at one cut); and the ` instrs` literal (a look-alike line is eaten and a count INVENTED).

**The fix is two invariants and four edges, and it needed both.** The panel split: one seat wanted
rows added and the 27 sum rows left alone (rewrite = churn); another wanted every newline-terminated
row converted so the blind idiom stops existing. Settled by execution — a probe walked every cut
point of eleven streams, 2,575 parser steps, against the shipped parser: zero violations of either
proposed invariant, so the conversion is safe and the objection was about diff size, not
correctness. Both are adopted, because the invariants catch the CLASS but do not kill the edges: the
bound mutant still satisfies the length test, and the regex-literal mutant never touches the tail at
all.
- **I2, the hold shape**, checked inside `feed()` after EVERY step and reported as one row with its
  step count (685 today): the tail is empty, or a `[`-headed, newline-free run shorter than the
  bound. This is the parser's own guard restated as a postcondition, so it applies to all the
  file's existing calls including the offset sweeps.
- **I3, finality**: an input whose concatenation ends in a newline must leave the tail EMPTY. Every
  newline-terminated row now pins the pair instead of the sum, and the sum idiom is gone from the
  file.
- **Section K**, the edges the census named: the hold bound AT 254/255 rather than near it; a
  bracket-free read holding nothing; a multi-record split sweep pinning body, tail and count
  separately at every offset; and the regex literal (`[ 100 frobs; p]` must not parse).

**Result, measured: 52 rows, and the census now reports 22 of 22 killed, 0 survived, 0 faults.**

**`regress/absorb_census.py` is COMMITTED, because a detector's worth is what it kills and that must
be re-runnable by someone who was not here.** It carries the mutant table and enforces THE
DENOMINATOR RULE, which exists because the record once said "10/10 parser mutants killed" over a
census in which five of twenty-two survived: the header prints the identity `attempted = killed +
survived + faults` and the program EXITS NONZERO if it does not hold; every survivor is NAMED with a
disposition from a closed vocabulary; "Survivors: none" prints even when empty; A CRASH IS A FAULT,
NEVER A DETECTION; a substitution that does not apply exactly once is a FAULT, not a survivor. The
repository is never mutated — copies only, which is what the `.MUTANT` history is for.

**Wired into gate 2 BEFORE the compiler check**, since the selftest needs only python3 and a machine
without `cc` must not silently lose parser coverage as well as the differentials. **The positive
control is the named survivor mutant itself**, applied to copies: it proves THE ROW KILLS THE
MUTANT, where an in-process wrong-expectation row would only prove the reporter can still print
FAIL. Its rows separate three states — never ran, ran and crashed, ran and caught — because exit
status alone cannot tell a crash from a catch.

**One row was written too tight and the gate caught it**: the control asserted the kill came from
exactly ONE named row, but the mutant strands every bracket-carrying line and fails all three. It is
now a floor, with the reason recorded — pinning the exact number would turn a legitimately added row
into a red gate.

**Verified:** gate 2 PASS, 131 checks (was 122); selftest 52 rows / 0 failures on the shipped
parser; census 22/22 with the identity self-check green; `bash -n` clean.

## R1 (#422, #423) — the harness could not be pointed anywhere else, and it kept no wall time
Two harness corrections in one file, taken first because **#422 gates every mutation census**: a
census that cannot be given a private directory writes into the shared logs `gate_hygiene.sh`
grades. Nine review seats assessed and researched both; the round is recorded here in the order the
panel settled it, because two of its conclusions were settled *against* the majority.

**#422 — `drive_guest.py` ignored `$LOGDIR`, and `lib.sh` never exported it.**
`regress/drive_guest.py` built both pty log paths from the literal `/tmp/gxregress`, and
`regress/lib.sh:24` assigned `LOGDIR` without `export`, so even a driver that read the environment
would have seen nothing. Both halves ship together (`lib.sh:24-31`, `drive_guest.py:202-210`);
the export is what a caller who writes `LOGDIR=x; ./run.sh` needs -- the census shape -- while a
caller who had already exported would have been served by the driver half alone, so the defect was
CONDITIONALLY, not uniformly, silent. Three findings worth keeping:
- **The obvious form is wrong.** Eight of nine seats proposed `os.environ.get("LOGDIR", <default>)`.
  Measured: with `LOGDIR` set but **empty** that returns `""`, and the paths become
  `/drive_<rig>.log`. **Corrected by the review, because the mechanism matters more than the
  slogan:** nothing actually lands at the filesystem root — `os.makedirs("")` raises
  `FileNotFoundError` first, so the run dies before either `open()`. The defect is a crash on an
  empty value where the shell's own idiom falls back, not a stray write to `/`. The shipped form is
  `os.environ.get("LOGDIR") or "/tmp/gxregress"`, which matches `lib.sh`'s own `${LOGDIR:-...}`
  treatment of an empty value. *A unanimous panel is not a measurement.*
- **The defect was conditionally silent, which is worse than uniformly silent.** Measured across
  eleven invocation shapes: a driver-side read alone is dead for `LOGDIR=x; ./run.sh` but live for
  `export LOGDIR=x` or `LOGDIR=x ./run.sh` — it works when tested by hand and fails in the census
  that motivates it.
- **A gate-5 row would have been vacuous, measured.** In the default battery `$LOGDIR` *is* the old
  hardcoded string, so such a row finds the logs whether or not the driver honours the variable.

**Detector: `regress/selftest_logdir.py`, wired into gate 2** (`gate_offline.sh`, alongside the
`readiness_predicate_test.py` precedent). It imports the shipped `drive()`, injects a rig named
`selftest` so its basenames cannot collide with the `drive_<rig>.log` files gate 6 grades, points
`LOGDIR` at a private directory and runs a one-line stub in place of the emulator — no gxemul, no
image, no boot, no rig, no serialisation. Two rows, asserting **the files**: a measured half-fix
(console log relocated, raw log still hardcoded) printed a `LOG=` line pointing into the private
directory while the raw log escaped, so reading the driver's own claim would have called it fixed.
The selftest sets the variable itself rather than being invoked as `env LOGDIR=... `, which would
export from *outside* and pass even with `lib.sh`'s export missing. Negative-controlled in both
directions: `no/no → FAIL` on the unfixed tree before the edit, `yes/yes → PASS` after.

**#423 — no wall time was recorded anywhere.** The record block printed five values and no
duration, so the landisk load-sensitivity fact (counts nearly halve under host load) could never
accrue calibration data. `t_start` is taken immediately **before** `pty.fork()`
(`drive_guest.py:222-224`) — `boot_progress()`'s own `t0` is taken after the fork, so it cannot
cover process startup — and `BOOT_WALL=%.1f` prints beside `NINSTRS` (`:406-421`), which is the
count at that same instant, so the pair yields instructions-per-second. Because the record block runs before
the interactive steps, the window is the boot leg **by construction** and cannot silently grow.

**`BOOT_WALL` is telemetry and must never become an oracle** — a wall-clock threshold is
load-sensitive, and this battery has already lost a 45-minute run to one. Its two gate-5 rows
assert presence and **containment**: the gate brackets its own call to the driver with `date +%s`
and requires `0 < BOOT_WALL <= elapsed+2`. The gate's interval strictly contains the driver's, so
the row holds under any load — both dilate together. Stated limit, not hidden: a constant value
below the ceiling survives both rows; wrong telemetry costs a wrong calibration note, not a wrong
verdict.

**Records corrected with the fix** (`OUTSTANDING_BUGS.md:3772-3774` and the D1 entry at `:3958`):
both cited `drive_guest.py:110`, a line the code left long ago. The project-root `CLAUDE.md:326`
carried the same stale citation and was corrected in the same pass, but it is OUTSIDE this
repository, so no hunk here touches it -- the first commit message named it as if it were in the
diff, which a review seat caught.
**The #419 round block's own `drive_guest.py:110` sentence is deliberately NOT corrected** —
`git log -L` confirms `log_path` really was at `:110` when that block was written, so it is accurate
history and rewriting it would falsify the record. *It is named here without a line number on
purpose: this round's own additions moved it twice (`:4455` → `:4519` → `:4554`), which is a
self-invalidating citation demonstrating itself.* **This fix does not license concurrent gates**: the producer/consumer orderings
(`gate_build` withdraw/republish, hygiene grading gates 4 and 5, `gate_ab` vs `gate_upstream`) are
untouched, and `gate_hygiene.sh:259` still answers a missing rig log with `note` + `continue` rather
than `degrade`, so a writer/grader divergence would be silent coverage loss inside a green gate —
which is why both resolutions now come from one exported variable.

**Follow-up in the same round, after the final-review panel (nine seats: one NO-GO, five
GO-WITH-CHANGES).** The review found three defects in the change itself, and the first two are
recorded here because they are the interesting kind — a fix that introduced a hazard the original
did not have, and a detector that certified half of what it claimed.
- **A relative `$LOGDIR` would have broken.** `os.makedirs()` runs in the caller's directory while
  the two `open()` calls run after `os.chdir(IMAGES)`, so a relative value created the directory in
  one place and wrote the logs in another — and gate 6 would then grade a path neither used. The
  old hardcode was absolute, so the hazard arrived with the fix. `logdir` is now resolved with
  `os.path.abspath()` before the `chdir` (`drive_guest.py:207`, `:211`). Three seats caught it
  independently.
- ***The detector tested one half of the defect and certified the other.*** The first
  `selftest_logdir.py` set `os.environ` in-process and called `drive()` directly, so deleting
  `export LOGDIR` from `lib.sh` left both gate rows GREEN. That is precisely the trap the file's own
  comment warned about for `env LOGDIR=...`, walked into one level down. It now runs the driver the
  way the battery does — a child shell makes a BARE ASSIGNMENT, sources `lib.sh`, and execs python —
  and both halves are covered: measured, removing the export turns both rows red, and reverting the
  driver read turns both rows red.
- **Gate 2 no longer fails where the image directory is absent.** `drive()` chdirs to a hardcoded
  absolute image path; the selftest needs no image CONTENTS but cannot run without the directory, so
  it now prints `SELFTEST_LOGDIR_SKIP` with a distinguishable token rather than failing as though
  the driver were broken. A named coverage gap beats a red row that blames the wrong thing.

**Claims the review corrected, recorded rather than quietly dropped:** "neither half works alone"
was overbroad (above); "`boot_progress()`'s `t0` starts after the exec" was imprecise — parent and
child run concurrently, so it is guaranteed only after the fork; and the first commit message named
a `CLAUDE.md` correction that no hunk in this repository made. One packet-fed seat argued the record
block sits after the interactive steps and therefore times the whole run; checked against the file,
the prints are at `:406-421` and `for step in cfg["steps"]` is at `:435`, so the boot-leg claim
stands.

**Two further corrections from the measure seat's independent review**, recorded because both are
about the record rather than the code. First, *the round's own negative control polluted the
directory the round exists to protect*: running the detector against the unfixed driver wrote
`drive_selftest.log` and `drive_selftest.raw.log` into the shared `/tmp/gxregress` — inert (nothing
globs those names; the graders use literal rig names) and now removed, but it is exactly the
pollution #422 prevents, produced while proving #422. Second, the `CLAUDE.md` correction left a
**non sequitur**: the sentence read "a per-gate `LOGDIR` would NOT isolate them, *because* the
driver now honours `$LOGDIR`" — the number was updated and the reasoning was not. It now says what
is true: the ORDERINGS serialise the gates, and removing the driver's hardcode changed nothing about
them.

**The containment row, swept rather than argued.** The seat evaluated 8000 (start-fraction,
duration) pairs assuming the driver consumed the entire gate window: minimum slack exactly 1.000 s,
so `+1` would have sufficed and `+2` cannot false-fail from truncation or from load. The only
false-fail route is a boot leg under 0.05 s printing `0.0` against the `b > 0` guard — reachable
only when the emulator dies instantly, which is already red elsewhere.

**Verified:** gate 2 PASS, 122 checks, including the two new rows; the detector negative-controlled
before and after; both edited gate scripts pass `bash -n`; the containment arithmetic checked at
0.0, 12.4, 999.9 and missing (missing resolves to `-1`, never to zero).

## One-hundred-and-fifty-ninth round (#420) — the load witness was the first instrument to break, and it broke into the shape of a regression

#419 converted gate 7 to a budget of guest work. **Gate 5 had the same defect and broke under load
*before* gate 7 did**, which matters more than the ordering suggests: `nightly_battery.sh` prints
gate 5's `BOOT_REACHED` under the banner *"gate 5 boots the same luna88k with the same binary and
is the independent witness"* — it is the instrument used to tell host load from a real regression
in gate 7. The witness fails first, and it fails in the same direction, so it corroborates the
wrong conclusion.

### Reproduced, one script, both runs at 8 busy loops on 8 cores

| | unmodified `drive_guest.py` | same load, room to finish |
|---|---|---|
| `BOOT_REACHED` | **0** | 1 |
| markers | 0 : 0 : 0 | 2 : 1 : 1 |
| computed values | **(none)** | `0.500000,1.414214` ✓ |
| verdict | **FAIL (exit 1)**, three rows red | PASS |

*"Did it fail for the reason under test?"* — checked, not assumed. The failing log ends on ordinary
late rc output (`MARKING FILE SYSTEM CLEAN`) with `panic`, `FATAL`, `trap` and `Stopped at` all
**zero**, at **63.4 % of the instruction path to login**. The boot was entirely healthy;
`drive_guest.py:38`'s 600 s ended it. With room, the same load reached `login:` at 720.8 s — and
that run's instruction count landed **3,498 instructions** from #419's independently measured
7,349,301,148, across two sessions and two completely different drivers (file-polling vs pty).

### What did NOT port from gate 7, and why the round is not a copy

**BACKSTOP is a hard FAIL here.** Gate 7 can treat a wall-clock expiry as inconclusive because it
boots pristine, prebatch and HEAD in one run, so prebatch reaching its marker is free evidence the
host was healthy. **Gate 5 boots one guest per rig.** There is nothing to compare against, "the
host might have been slow" is unfalsifiable, and an unfalsifiable excuse must not soften a verdict.

**A per-step progress oracle cannot exist.** The ten step waits of 5–15 s looked like the same
defect at smaller scale. Measured across five healthy runs, 25 step windows: **16 saw zero
instruction records and none saw more than two**, because at a prompt the rate collapses from
63.5 M to 1.53 M instr/s. "Require zero records" false-FAILs healthy runs 16 times in 25; scaling
by the observed rate applies a boot-phase figure **40× wrong** for the phase it gates. They are
also not verdict-bearing individually — `drive_guest.py` retries and the verdict comes from the log
scan — and under the same 6× load **every step confirmed on attempt 0**. Left as wall clock, filed.

**Landisk gets no instruction budget at all.** Six idle boots span 2,046,965,550–2,852,740,381, a
**39.4 %** spread against luna88k's 3.57 %. A ceiling from six samples that scattered would repeat
the exact "mean quoted as a worst case" error #419 pass 4 corrected. It relies on the stall
detector and backstop until its rate is measured properly. Landisk also had no false-FAIL to fix —
7.2–8.3 s to prompt against a 420 s budget, 50× headroom — so converting it buys
**distinguishability**, not headroom: a hung SH4 core now reports STALLED instead of a timeout
indistinguishable from load.

### The interleaving hazard, where the brief was wrong in both directions

The design brief worried that a guest might print something shaped like an instruction record.
**Zero occurrences** in either complete log. The real hazard is the reverse: `cpu_show_cycles()`
writes the record into the same stdout as the console with **no leading newline**, so it lands at
the cursor and *terminates the guest's partial line*. That already happened **without `-N`** —
landisk had 7 of 20 bracketed messages mid-line, two splitting a guest word, one immediately after
`HITACHI SH7751R`, the exact string this gate asserts.

***And the anchored strip the brief proposed heals nothing***, because the pty emits bare CRs as
well as CRLF and Python's `^` only matches after `\n`:

| assertion | control | anchored strip | unanchored |
|---|---|---|---|
| `HITACHI (\w+)` | `SH7751R` | **`SH77`** | `SH7751R` |
| landisk boot pattern | MATCH | **(none)** | MATCH |
| `GX_FP …` | values | **(none)** | ✓ |

`SH77` is not a miss — it is a **wrong answer that reads as an SH4 emulation defect.** The shipped
form is unanchored and eats the trailing newline, which is what rejoins the split line. Validated
five ways including a record **split across two pty reads mid-record**, which no regex fixes: the
absorb loop holds a possible record prefix back rather than classifying it, and the hold is bounded
by a newline or a `]` so a guest line containing a bare `[` cannot stall the buffer.

The streams are also split now — `drive_<rig>.raw.log` keeps everything, `drive_<rig>.log` is
console-only — because `gate_hygiene.sh` greps that file for distress **substrings** and a record
embeds a guest symbol (`<sched_idle+0x8c>`). No collision measured today across 527 records; the
mechanism is removed for free.

### Pass 2: the round reintroduced a bug the previous round had already fixed

***`MARKER` did not always win.*** The milestone is tested at the top of the poll loop, but
`BUDGET`, `STALLED` and `BACKSTOP` are tested *after* `read_once()` without re-checking the newly
absorbed output — so a milestone arriving in the very read that crossed a threshold lost to the
failure reason, and a healthy run false-failed.

That is precisely the defect #419 pass 3 fixed in `lib.sh` (BACKSTOP reported with the marker
already in the log, measured 3/3 deterministic). Porting the loop's *shape* into the pty driver
carried the bug across and left the fix behind. **"A correct draft is not a correct implementation"
applies to porting an already-corrected implementation, too** — the corrected version is exactly the
one that looks safe to copy.

Fixed with a tie-break that re-checks before returning any failure reason, and which flushes
whatever `absorb()` is holding first — a milestone whose text begins with `[` would otherwise still
be inside the hold. Proven with the unfixed loop as a negative control, and with two controls
showing hang detection is not weakened:

| scenario | unfixed | fixed |
|---|---|---|
| marker arrives in the threshold-crossing read | **STALLED** (healthy run failed) | **MARKER** |
| marker arrives well before the threshold | MARKER | MARKER |
| genuine hang, no marker ever | STALLED | STALLED |

Two numeric records of this round's own also corrected. **"landisk's records are ~20× denser"** was
wrong twice over: the stated medians give 96×, and "denser" is the wrong word entirely — per guest
instruction both streams fire at the same 2²⁵ cadence, so what differs is how fast landisk executes,
not how often gxemul prints. And the 742 s figure **conflated two different runs**: 742 s was gate
7's file-polling driver reaching login with markers only, while this gate's pty driver reached it at
720.8 s *with* both computed values. Attributing one run's evidence to the other is the same class
of error as quoting a mean for a worst case.

The reviewing seat disclosed that it executed only arithmetic and source reads — the boot, gap and
log-size measurements were read rather than reproduced — which is why the tie-break was given its
own executed test instead of being accepted on the finding alone.

### Pass 2c: a live wrong answer in the strip, and a guard row that stated a falsehood

A measure seat ran three real boots, 1,100+ `absorb()` invocations with byte-exact chunk control,
and eighteen driver mutants across five chunkings. Three defects, all measured.

***The record terminator was optional, and that recreated the exact corruption the code above it
claims to prevent.*** `\[ *(\d+) instrs[^\]]*\]\r?\n?` matches the instant `]` arrives — so a read
boundary between `]` and its newline consumed the record *without* its terminator, emptied the
hold, and delivered the newline on the next read as ordinary console text. Result:
`HITACHI SH77\n51R`. The hold could not help, because it only engaged when the fragment contained
no `]` at all. Measured at 1 of 138 split offsets for LF and 2 of 81 for CRLF; **not reachable on
today's rigs** — zero of 740 real pty reads landed inside a record — but a wrong answer rather than
a miss. The terminator is now mandatory while streaming, optional only at end of run, and the hold
triggers on a missing newline rather than a missing bracket. Verified at every split offset with
the old code as control: old fails at offset 111 (and 112 for CRLF), new fails at none.

***A guard row that passed while stating a falsehood.*** Deleting the driver's
`print("BUDGET=%d")` produced **zero red rows**, and the gate then printed, green, *"budget is
deliberately absent (uncalibrated rig)"* for a rig whose budget is 12 G — because `${bg:-0}` turns
*missing* into *deliberately zero*. That is worse than an undetected mutant: the row asserts
something untrue and is believed. The three constants' presence is now asserted before any of them
is interpreted. `STALL` and `BACKSTOP` happened to default safely; a default that happens to be
safe is not a check.

***One bit of coverage, and three mutants walked through it.*** `NINSTRS > 0` was satisfied by
setting the count to a constant 1, by incrementing per record instead of parsing, and by keeping
only the first record — each silently disarming the budget oracle while every row stayed green.
Replaced with a per-rig floor from measured minima.

### The round stated a general property that holds for exactly one rig

"A budget of guest work is load-insensitive" is established for luna88k: two independent
measurements, different sessions and different drivers, **3,498 instructions apart** across load
levels. **For landisk it is false.** Measured under 8 busy loops on 8 cores, instructions to
milestone: **1,040,286,129 under load against 2,046,960,827 idle — a 49 % drop**, because the SH4
boot waits on host-clock-driven emulated timers. Its instruction count tracks the host nearly as
badly as wall clock does.

Giving landisk no budget was therefore right, but for a far stronger reason than this round gave;
the quoted 39.4 % spread was idle-host variation only, and the real spread across host conditions
is at least 2.74×. Any future landisk budget must be derived from loaded runs. Recorded, along with
the measurement that makes residual item 1 concrete: **the largest post-milestone inter-record gap
under load was 56.97 s against a 60 s stall** — a 5 % margin, latent only because the step phase is
not progress-checked.

Three further records corrected. `OUTSTANDING_BUGS.md` said the `head -1` issue was *"not a live
false pass today — landisk declares one value"*; landisk declares **two**, and the seat measured
both being printed, so the record contradicted itself and the false half was the exculpatory one.
The claim that free-stripping reproduces the previous log sizes *"exactly (6234 B, 3838 B)"* holds
for luna88k and not landisk, which gave 3837 because the guest prints a variable CPU speed — log
size was a coincidence that nearly became a fixture. And the anchored-vs-unanchored table was
produced by injecting into whole logs, whereas through `absorb()` an anchored pattern also matches
at position 0 of every chunk; the conclusion stands, the cited evidence does not describe the
shipped code.

### The mutant, again

Removing `-N` leaves the guest booting perfectly: every marker matches, every value is right, and
`REASON` is legitimately `MARKER` — there is nothing wrong with the boot. On landisk there is not
even a race to hide behind (8 s boot against a 60 s stall). The only observable difference is that
the count stayed at zero. **The kill row asserts the count, never the reason.**

## One-hundred-and-fifty-eighth round (#419) — a gate that could not tell a slow host from a broken build, and a cure that measured worse than the disease

`gate_ab` gave each luna88k boot 300 seconds of **host wall clock** and then counted semantic
markers. That is a load-sensitive oracle: under load the guest makes less progress in the same
seconds, `login:` never appears, and the row FAILs **indistinguishably from a real capability
regression.** It happened twice — once from panel seats loading the host, once from my own greps.

### The decisive measurement

Under **8 busy loops on 8 cores**, luna88k still reaches `login:` — at **7,349,301,148 instructions
in 742 s**, markers `1:1:1`, at 9.96 M instr/s. That is the same run which scored `1:1:0` and FAILed
against the 300 s budget. The build was never broken; the clock was the wrong ruler.

Eleven boots, instructions-to-login:

| condition | instrs@login | achieved i/s |
|---|---|---|
| 8 busy loops, saturated | 7,349,301,148 | 9.96 M |
| 2–4 busy loops | 7,315,767,413 – 7,315,778,918 | 38.9–47.9 M |
| idle (6 runs) | 7,517,144,375 – 7,785,570,754 | 60.7–67.2 M |
| page cache dropped | 7,550,703,750 | 64.9 M |

**3.57 % across eight idle runs; 6.42 % across an 8× host-speed range.** Dropping the page cache did
not widen it. Load moves the count *down* ~4 %, because the m88k idle fold credits 8191 instructions
per wall-paced `usleep(500)` main-loop iteration, so a busy host credits fewer — the count is not
pure guest work, but it errs in the safe direction for a ceiling.

### What the round actually changes

`run_emu_progress()` in `lib.sh` runs against a budget of **guest work** and — the part that fixes
the defect — **reports why it stopped**: `MARKER` (got there), `BUDGET` (executed a full allowance
and did not), `STALLED` (stopped executing at all), `BACKSTOP` (wall clock expired while still
advancing), `ABSENT` (no instruction stream ever). Only `BACKSTOP` is load-ambiguous, and even that
is inconclusive only when prebatch was hit too — gate_ab already boots all three builds, so the load
signal is free. If prebatch reached its marker, the host was fine and HEAD alone failing is a
regression.

Three constants, each measured: budget **12 G** (+54 % over the observed max; it bounds only the
failure path, since a healthy boot stops at the marker long before it), stall **120 s** (at the
slowest rate ever measured here a record arrives every 3.4 s, so 120 s of silence is 35 missed
records — no amount of load produces that), backstop **1800 s** (2.4× the worst boot measured).

### Four things the panel killed, all of which would have shipped

1. ***The naive "backstop → INCONCLUSIVE" was measured to be strictly worse than the defect.***
   Running the real `lib.sh` under synthetic gates: both `degrade` and `gate_skip` exit 77 → SKIP →
   `REGRESS_PASS_WITH_GAPS` (exit 3). A HEAD that hangs before `login:` exits 1 today. The cure
   would have turned a hard failure into a green-ish pass, and green is what gets read.
2. ***Scoring pristine by instruction budget would have made a long-standing PASS a permanent
   not-run.*** Upstream 0.7.0 emits **zero** `-N` records on luna88k (five runs, 768-byte logs):
   under 111,848 instr/s, so 12 G would take over 29 hours. It does not exit and does not idle — it
   **spins**, burning 100 % of one core, so "the process is alive" carries no information. The stall
   detector catches it in ~30 s. Row-scoped end conditions: the signal that means *hung* for HEAD is
   the *expected* state for pristine.
3. **The naive design was 2.3× SLOWER, not faster** (~2074 s vs 900 s), because nothing stopped a
   healthy boot at the marker. Stopping at the marker is where the speed-up is — today's run burns
   its whole budget *after* login, since the guest never exits.
4. **Piping gxemul's stdout into a reader re-creates the bug `lib.sh` rule 1 exists for.**
   `stdbuf -o0` fixes gxemul's buffering; a `gxemul | grep` reader block-buffers its *own* stdout,
   one process later. Worse, a SIGPIPE-based stop fires only on the emulator's next write — which
   never comes for a wedged guest, exactly the case the stop exists to catch. The implementation
   polls a file instead; the log is complete on disk however the run ends.

### The selftest, and why it is not optional

The `BUDGET` and `STALLED` branches are **only ever entered by a failing run**, so nothing on a
green run exercises them. Break the instruction extraction by one character and every leg falls to
`BACKSTOP` for ever while the battery stays green and the capability rows test nothing. Four fake
emulators drive all four reasons in seconds without the rig; the load-bearing one prints every
marker but no instruction record — the exact shape a dropped `-N` produces — and must read `ABSENT`.

### Corrections to this project's own records

* **My reproduction claimed 0.877 % drift. It was two samples two print-quanta apart** — the quantum
  is 2^25 (`emul.c:1026`), so instructions-to-login is only observable to ±0.44 %, and "0.877 %" was
  the resolution floor, not a distribution. The real figure is 3.57 % idle.
* **A review seat claimed 22 % from a log that was still being written.** It flagged its own doubt
  and used the number anyway. The completed file reads 7,315,767,413, not 6.38 G. *A partially
  flushed log is not a measurement.*
* ***`CLAUDE.md` asserted for months that `selftest_mutation.sh` does `rm -rf` on the shared gate
  workdir. It does not*** — `T=$LOGDIR/mutation` (`:27`), `rm -rf "$T"` (`:41`), scoped to one
  subdirectory. Nor do the rig images serialise: both consumers open them read-only via `R:` with a
  pid-unique overlay. The real serialisers are three producer/consumer orderings —
  `gate_build.sh:64-65` withdraws a binary `gate_mips.sh:30` needs, `gate_hygiene.sh:198-258` grades
  pty logs gates 4 and 5 produce, `gate_ab.sh:42` removes trees `gate_upstream.sh:46-47` reads — and
  a per-gate `LOGDIR` would not help, because `drive_guest.py:110` hardcodes its path.

### Pass 2 found the mutant this round was built to catch, still alive

Two seats reviewed the shipped diff — **Codex and Opus, and that is two seats, not a panel.**

***The dropped-`-N` mutant survived.*** The guard asserted `reason != ABSENT`, but `ABSENT` is
only assigned when the run did *not* reach the marker. A guest that boots perfectly with `-N`
removed therefore classifies as **MARKER** — there is nothing wrong with the boot — and every
reason-based check passed while the budget and stall protections were silently unarmed. The
selftest missed it because the fake written for that case never printed `login:`: **it had been
built to match the guard rather than the threat.**

Fixed by asserting the instruction **count** instead of the reason — zero records for pristine,
non-zero for prebatch and HEAD — and by adding a fake that boots cleanly with no instruction
stream, which pins `reason=MARKER` and `ninstrs=0` together so the two facts cannot drift apart.

The seat that found it disclosed that it had executed only `rev-parse`, status, arithmetic and
source counts — the gate, the mutant and the reaping tests were **read, not run**. So the mutant
was built and executed rather than taken on trust: `-N` removed from the real luna invocation,
against the fixed gate.

```
       pristine   ABSENT    instrs=0    0:0:0
       prebatch   MARKER    instrs=0    1:1:1     <- a PERFECT boot, oracle unarmed
       head       ABSENT    instrs=0    1:1:0
  FAIL prebatch: -N instruction stream was actually observed  got=0 records want=present
  FAIL HEAD:     -N instruction stream was actually observed  got=0 records want=present
  a-b-baselines: FAIL (4 of 14 checks)
```

That `prebatch` line is the whole finding in one row: markers `1:1:1`, reason `MARKER`, nothing
wrong with the boot at all — and the previous spelling of the check passed it.

Also corrected, both mine: the comment claiming pristine is caught "in ~30 s" (it uses the same
120 s constant — a prototype figure that outlived its truth), and "no amount of host load can
produce 120 s without progress", which is empirical rather than absolute since the detector reads
`date +%s` and a suspended or starved process looks identical. It is 35× the worst observed gap,
not a proof. And the pristine row previously accepted `STALLED` as well as `ABSENT`, so "one
instruction record followed by silence" would have passed a row whose name says there is no
instruction stream at all.

Filed rather than fixed: the differential witness assumes prebatch's success proves the host was
healthy for HEAD, but the three legs run **sequentially**, so that is not established — load
arriving between them defeats it.

### Pass 3: seventeen gate runs found five more mutants alive, and two live defects

A measure seat built a mutation testbed — a fake gxemul honouring `-N`, a fake `_images`,
scaled constants — that reproduces the shipped gate exactly in 35 s. It confirmed independently
that the two mutants alive at `ec30813` are dead at `ce9c0bc`, then found five more.

***Three of them were the measured constants themselves, and the cause is a vacuity shape worth
naming.*** Multiplying `LUNA_BUDGET` by 1000, or `LUNA_BACKSTOP` by 4000, or disabling
`LUNA_STALL` outright, left **all fourteen checks green**. The selftest exercises
`run_emu_progress()` with *literal* arguments, so it proves the function works while proving
nothing about the values the gate actually passes it — **the rows guard a different instance of
the thing they appear to guard.** Fixed with static range rows derived from the measurements
(budget within 1.05–2× the observed max, stall between 30 s and a quarter of the backstop,
backstop 1200–3600 s); each mutant now dies naming its row, at no boot cost.

A fourth was mine from pass 2: the fix deleted the only consumer of `PRI_R`, leaving a variable
assigned and never read, so nothing asserted that pristine is caught by the *absent-stream* path
rather than sitting out the full 1800 s backstop. Asserted rather than deleted.

**Two live defects in what this round shipped, both measured end-to-end:**

*The `tail -c 2048` window loses the oracle under output pressure.* A guest emitting one record
per 2 s with ~6 KB of console output between records scored `ABSENT`, `instrs=0` — a healthy
executing build reported as a harness fault **and** a capability regression, which is exactly the
misclassification this round exists to remove. The margin was thinner than the comment claimed:
**the maximum inter-record gap on the real luna88k log is 2334 bytes, already larger than the
window.** It failed to bite only because the miss must persist for the whole stall period. Now
64 KB, ~28× the observed worst gap, still O(1) per poll.

*`BACKSTOP` was reported with the marker already in the log* — 3/3, deterministic. The poll loop
never re-checked after exiting, and the measured poll period is ~1006 ms, so a marker landing in
the final window scored `BACKSTOP`: a successful boot called a regression, **while the marker-count
row simultaneously passed on `1:1:1`.** Two contradictory rows from one run. It now re-greps
before defaulting, and recovers a final count the same way.

**A mechanism claim of ours contradicted by the source.** The comment explained the ~4 % load
effect by "the m88k idle fold credits 8191 instructions per wall-paced `usleep(500)` iteration".
The constant is real (`cpu_m88k_instr.c:2611`, `:2660`) but it is **subtracted back** at
`cpu_dyntrans.c:377` before `n_instrs` accumulates at `:392`, so the net credit per fold is ~0.
The measured direction stands; the explanation did not, and has been replaced with a note saying
so. Also corrected: "9.96 M instr/s" was not derivable from the cited run (7,349,301,148 / 742 s
= 9.9 M), and the same file gave both "699-byte" and "768-byte" for one measurement.

**`run_emu()` now has no callers at all** — gate 7 was its last — while two comments still cited
it as the path every emulator invocation takes. Kept, because the rule is general and a future
gate will want the simple form, but no longer described as universal.

### Scope, stated narrowly on purpose

**This converts gate 7 only.** The battery carries roughly **37 wall-clock oracles** — 33
`while time.time() - t < …` loops across 18 probe files, plus `gate_asan_sweep.sh:60,62`,
`gate_upstream.sh:74`, and `run_emu` itself. Gate 5 has the same defect and worse: `drive_guest.py`
allows luna88k 600 s, and the saturated boot measured here took 742 s, so **gate 5 breaks under load
before gate 7 does.** No parallelism claim is made or earned. And the honest framing of the whole
round is that wall clock cannot be removed — the stall detector is still a clock — but its margin
moves from ~2.4× to ~200×, because it now needs one instruction record per window rather than a
whole boot per budget.

## One-hundred-and-fifty-seventh round (#418) — the documented `d:` override did nothing, and the obvious place to fix it was measurably the wrong one

`DISKIMAGE_FLOPPY` is a write-only type. No device references it: every controller hard-codes its
type argument — six `diskimage_scsicommand()` sites pass `DISKIMAGE_SCSI`, the ATAPI one passes
`DISKIMAGE_IDE` — and both selectors match on `d->type == type`. So a floppy-typed image is
invisible to every controller, while the console prints a confident `FLOPPY DISK id 0, read/write`.

The manual offers `d:` as the way out (`d: DISK (this is the default)`; *"the default for disks can
be either SCSI or IDE"*). Nothing acted on it. Measured on the shipping binary before any edit:

```
-d   fl144.img   FLOPPY DISK id 0, read/write, 1440 KB (CHS=80,2,18)
-d d:fl144.img   FLOPPY DISK id 0, read/write, 1440 KB (CHS=80,2,18)   <- byte-identical
```

### The placement is the whole round, and the design brief was wrong about it

The brief said the fix belonged in the prefix block, next to `i:`/`f:`/`s:`. A measure seat built
seven variants and ran them. That placement **also** makes `d:` work — and is killed by nothing in
the detector except one property. Because it assigns the type *before* `diskimage_recalc_size()`
runs, the image gets the generic 63/16 geometry instead of the exact floppy one, and the advertised
capacity rounds **up**:

| size | file blocks | prefix-block placement | after `recalc` (shipped) |
|---|---|---|---|
| 720 K | 1440 | **2016 (+40%)** | 1440 exact |
| 1.2 M | 2400 | 3024 (+26%) | 2400 exact |
| 1.44 M | 2880 | 3024 (+5%) | 2880 exact |
| 2.88 M | 5760 | 6048 (+5%) | 5760 exact |

Those phantom blocks are not inert. Under the asymmetric bound this file already carries, **reads**
are bounded by advertised capacity and **writes** by `d->total_size`, so the guest would be offered
blocks that read back as zeroes and refuse every write — a fresh instance of the residual #416
recorded as unfixable for the rig images, manufactured here for no benefit. Placing the assignment
after `recalc` keeps the geometry the heuristic already computed correctly.

The guard `!prefix_i && !prefix_f && !prefix_s` is equally load-bearing and equally measured. The
pre-existing mutual-exclusion check tests only `i+f+s > 1` and knows nothing about `d`, so `id:` and
`fd:` are accepted arguments; without the guard, `-d id:big.img` returned SCSI where the shipping
binary returns IDE. A live regression, not a hypothetical.

### The detector, and the mutation matrix that proves its rows reach the code

New `regress/diff_diskimage_parse.c` — 35 rows, fully offline, no binary and no guest. Six variants
built and run; every kill names its row, and no variant failed to build (a build fault is not a
detection):

```
base(FIXED)     0 failures   SURVIVES
revert         10   all [PROOF] type + reachability rows
noguard         2   [PREC] 'fd:' stays FLOPPY, [PREC] 'id:' stays IDE
hardscsi        3   the three IDE-default (malta) rows
prefixblock     4   ONLY the four [SIZE] rows
delprefixd      2   the two d:*.iso rows -- a TEN-CHARACTER deletion
```

Two of those deserve naming. **`prefixblock` is killed only by the four exactness rows** — delete
them and the wrong placement ships green, which is why they are checked individually in the gate.
**`delprefixd`** removes `&& !prefix_d`, the *only* pre-existing use of `prefix_d` in the file — so
the round that gives `prefix_d` a second use is precisely the round in which someone deletes the
first as redundant. Its effect is that `d:*.iso` becomes an unwritable CD-ROM, and a row set using
only `.img` filenames — which is what the design brief specified — passes it 100%.

`hardscsi` matters for a structural reason: `get_default_disk_type_for_machine()` returns SCSI for
exactly PMAX, ARC, SGI, LUNA88K and MVME88K, and IDE for everything else. Those five are precisely
the rigs this project can boot, so hard-coding `DISKIMAGE_SCSI` passes every row on every bootable
rig. `MACHINE_EVBMIPS` needs no image or kernel offline and is the only thing that distinguishes it.

Gate 2 went 110 → 120 checks.

### Not fixed, and said plainly so a reader of the diff is not misled

**A bare floppy-sized image with no prefix is still typed `DISKIMAGE_FLOPPY` and still invisible to
every controller.** This round makes the documented escape hatch work; it does not address the size
heuristic that creates the unreachable type in the first place. That is the default path — what a
user hits without reading the manual — and it remains broken. Four `[RECORD]` rows pin it so the
round that does fix it cannot land silently.

Two sub-defects found while measuring, filed rather than folded in, because the stopping rule admits
only a measured false pass or a wrong record: a small ISO at El Torito floppy sizes becomes a
`FLOPPY CD-ROM`, doubly unreachable (the heuristic tests only `type == DISKIMAGE_UNKNOWN` and ignores
`is_a_cdrom`); and `d:` is consulted for `.iso`/`.cdr` but not `.cue`. A seat corrected the brief on
the second: a `d:`-prefixed cue is *not* "additionally" unwritable — the unprefixed one is equally
read-only, since `is_a_cdrom` forces it in both cases.

### A record that invalidated itself the moment it was written

`diskimage_scsicmd.c` stated that `DISKIMAGE_FLOPPY` *"occurs in exactly seven places, all inside
`diskimage.c`/`diskimage.h`"*. Both halves were wrong on arrival: **spelling the identifier in a
sentence that counts occurrences of that identifier made the count eight**, and the location clause
is falsified by the file the sentence lives in. The same sentence was duplicated in this changelog —
found by a seat, not by the main loop, whose grep had silently scoped itself to `src/`. Both are
corrected to the structural form, which survives edits: *no device references it*. A tree-wide sweep
found no other instance, so this is a one-off rather than a class; the cheap rule it earns is that
**a record may not state a count of an identifier it also spells.**

### Seats

Pass 1 fired seven scriptable seats plus the Opus measure seat; **six of seven answered** — minimax
produced 203 bytes and is recorded as a seat failure, never as agreement. **Kimi 3 returned after
being quota-dead since ~08-12**, ran its own probe, and beat the main loop twice: it found the
duplicated count in the changelog and caught that `prefix_d` is absent from the mutual-exclusion
guard. Q7 was unanimous across all six. Q6 split 2–2 and was settled by the stopping rule rather
than by vote. The measure seat overturned the brief's central instruction, as it has in four of the
last five rounds; the four placement variants above are its work, re-run independently before the
edit was made. Pass 2 fired **two seats, Codex and Opus** — recorded as two seats, not as a panel.

## One-hundred-and-fifty-sixth round (#417) — #416's own bound disarmed the rows that tested it, and its sense latch outlived the failure it described

Two defects in what #416 shipped, both found by a pass-2 mutation sweep on the committed diff, and
both of a kind that leaves everything green.

### The bound silently disarmed three of its own tests — call it COLLATERAL VACUITY

#416 added a capacity check at the top of `diskimage__internal_access()`. Three rows in
`diff_diskimage_io.c` wrote at offset **8192 on an 8192-byte file** — exactly *at* the backed extent
— so the new bound refused them **before `fwrite()` was ever called**. They had been built to prove
that a short or failed write is reported, using `RLIMIT_FSIZE` to make the store refuse the bytes.
After the bound they proved nothing, and nothing went red.

**Measured: deleting #416's entire short-write check left all 31 rows green.** That check is the one
standing between a partial write and silent data loss, and it shipped untested.

*The rows had been announcing this in their own output.* Each prints an evidence line, and it had
changed from `errno 27` (EFBIG — the store refusing) to `errno 0` (nothing attempted). **A row that
prints evidence it does not assert will tell you it is broken and be ignored.**

The fixtures now write at 4096 inside an 8192-byte extent, with the rlimit doing the truncating.
Getting there took three attempts, and each failure reproduced the same masquerade by a different
route — the rlimit lowered *before* `mkfile()` truncated the fixture itself; then case A's rlimit
*leaking* into case B and truncating that one. The evidence line caught all three. **Only a mutation
test proved the rows finally reach the code they name**: deleting the check now fails
`short write (256 of 1024 absorbed)` and `write that lands 0 of 1024 bytes`.

The general shape is worth naming: **adding an EARLIER rejection can silently disarm every test that
depended on reaching a LATER failure.** It is distinct from a check that cannot fail, and distinct
from a row that computes evidence without asserting it — here the row and the code are each correct
in isolation, and only their order changed. It is also the second appearance of the same idea in one
round: #416's own CHANGELOG describes a rejected design scoring a deceptively *low* failure count
for exactly this reason.

### A regression #416 introduced: sense outlived the command that set it

`diskimage__return_default_status_and_message()` did not clear the latched sense, so a refused READ
followed by a **successful** READ left key `0x05` in place — and the next REQUEST SENSE blamed the
command that had worked. Before #416 that query returned `0x00`. Sense describes the last command,
so success must retire it. The helper now takes the disk and clears on success (23 call sites).

### The sense path had no coverage at all

**No row issued REQUEST SENSE**, so three separate one-character mutants survived: masking the key
with `0x00`, dropping the latch, and dropping the clear. A CHECK CONDITION whose sense says "no
sense" tells a guest that something failed and then that nothing is wrong — which ARC can read as
success — so the status and its sense are one mechanism and must be tested as one.

### Three more regions no row entered

* **An unaligned backed extent.** Every fixture was a whole number of 512-byte blocks, so
  `d->total_size` → `d->total_size + 1` survived: the slack is only reachable when
  `total_size % 512 != 0`. It grew a 10,239-byte image by one byte — falsifying #416's headline
  property literally by one byte, which is why that wording is corrected above.
* **A negative offset.** Dropping `offset < 0` survived everything. It is reachable:
  `diskimage_access()`'s own negative guard only fires when `override_base_offset != 0`, and #204
  records a guest seeking a flat CD/ISO handle to `0xffffffff`.
* **A 0-byte image**, which #416 changed deliberately and left unasserted in either direction.

`regress/diff_diskimage_io.c` goes 31 → **45 rows**, 0 failures at `-O0/-O1/-O2/-O3/-Os`, 0
UBSan/ASan runtime errors.

### Assessed, not changed

* **Sense-key classification is too coarse.** SCSI WRITE maps out-of-range, read-only and short
  write all to MEDIUM ERROR / WRITE ERROR; an out-of-range WRITE should report LBA OUT OF RANGE, as
  READ already does. An error-reason enum — plausibly the same `d->error` the ATA work needs — would
  fix propagation and classification together.
* **Signedness is safe for guest paths but not generically.** SCSI transfers are capped at 64 MiB,
  but the public `size_t len` interface admits `len > INT64_MAX`, which casts negative.
* **Short or errored READS still return success.** Only failures that make
  `diskimage__internal_access()` return zero propagate; a genuinely short read does not.
* **READ CAPACITY on a zero-sized medium** returns a successful, inherently ambiguous zero.
* A naming drift: section 2's row says "past EOF" but asserts "past *advertised*".

## One-hundred-and-fifty-fifth round (#416) — one guest WRITE past the end of a 10 KB image grew it to 512 MB, and the guest was told it succeeded

`diskimage__internal_access()` had no capacity check of any kind. The only limit on a guest LBA was
a byte-count cap, so a single `WRITE(10)` past the end of a 10,240-byte image **grew the host file
to 512,000,512 bytes** and its advertised capacity from 1,008 to 1,000,944 blocks — with **status
GOOD**, and permanently, because capacity is re-derived by `stat()` on the next run.

Three defects compounded to make it silent. The internal layer never reported a short or failed
transfer: its own check was compiled out under `#if 0`, and it read `lendone <= 0`, so it would not
have caught a *partial* write even if enabled. SCSI READ then **swallowed** the result — turning
`!result` into a zero-fill with status GOOD — while SCSI WRITE discarded it outright, the call
edited down to `/* int result = */` with `/* TODO: how about return code? */` beneath it.

### The hard part was not the bound, it was which extent to bound against

All five rig images carry a **480–992 block whole-cylinder round-up gap**: capacity is rounded up to
whole cylinders, so the last fraction of a megabyte is addressable but not backed by file. Reads of
that gap have succeeded as zero-fill for the life of this fork. `gxemul_pmax_rig/disk.img` records
`d_secperunit = 614880` against a 614,400-block file, with partition `c` extending 480 blocks past
the end — geometry the guest's own installer wrote.

**The design this round first specified was measured to be wrong.** Bounding *reads* against
`d->total_size`, the backed extent, **breaks all five rig images** (`internal_access → 0`) and the
detector's own control row. It also scored a *lower* failure count than the correct bound, which was
a **masquerade**: two short-write rows write at exactly `total_size`, so they passed because the
bound rejected them, not because a short write was detected — passing for the wrong reason.

**The bound that shipped is therefore asymmetric**, and the asymmetry is the whole design:

```c
limit = writeflag ? d->total_size                                  /* backed extent   */
                  : nr_of_logical_blocks * logical_block_size;     /* advertised      */
```

Writes stop at the backed extent, so **a guest can never grow a non-tape image beyond that extent**.
(#417 narrows this: tapes are exempt by design, overlay files still grow *within* the extent, and the
original wording "by even one byte" was falsified literally by one byte — see #417.)
Reads run to advertised capacity and zero-fill past EOF, so the round-up gap behaves exactly as the
rig images have always relied on. The comparison avoids `offset + len`, which would overflow before
it could be tested, and the read-side zero-fill is load-bearing rather than tidiness: `dev_wdc`'s
read path declares a 32 KB buffer **on the stack**, discards this function's return value, and
copies the whole buffer to the guest, so an early return leaving `buf` untouched would hand the
guest uninitialised host memory.

Three lines of evidence settled the choice, the first decisive:

* **The absence of a bound is itself the instrument.** The shipped code checked nothing, so a write
  into the gap would have grown the file permanently, and `stat` would still show it. All five sit
  at exact round sizes: 300 MiB, 300 MiB, 1 GiB, 1 GiB, 2 GiB.
  *** #417 CORRECTS THE STRENGTH OF THIS CLAIM, AND IT MATTERS. "Nothing has ever written there, a
  historical measurement" is more than the file sizes prove, and for `liveimage-luna88k` it is
  STRUCTURALLY VACUOUS: that image is only ever opened under the `R:` prefix, so guest writes go to
  an unlinked overlay and could never have changed it — measured, a gap write under the unbounded
  binary DID land in the overlay and read back as 0x99. The gates also boot writable COPIES, so the
  golden files are never what a guest writes to.
  THE SOUND EVIDENCE, which is stronger anyway: `/tmp/rig.img` and `/tmp/rig_arc23.img`, the actual
  writable copies from a pre-commit run under the UNBOUNDED binary, sit at exactly 314,572,800 and
  1,073,741,824 bytes — a full OpenBSD boot grew neither. That measures the guest's real write
  traffic rather than a read-only golden file. ***
* Partition tables agree: the pmax `a` (root, ends 548856) and `b` (swap, ends 614392) both finish
  *inside* the file; only the raw whole-disk `c` reaches the gap. On arc, `d_secperunit = 196608`
  leaves every partition 1.9M blocks short of the file end.
* The gates never write the base image at all — `gate_ab` and `gate_m88k_rounding` both use the `R:`
  prefix, which opens `d->f` read-only and routes guest writes into a throwaway overlay.

### CHECK CONDITION and sense data are one change, not two

Returning CHECK CONDITION without sense data is worse than returning nothing: `REQUEST SENSE`
hardcoded sense key `0x00`, so a guest told "something failed" and then "nothing is wrong" cannot
act — ARC in particular can read that pair as success. This round adds `sense_key`/`sense_asc`/
`sense_ascq` to `struct diskimage`, latches them at every new CHECK CONDITION, and has `REQUEST
SENSE` **report and then clear** them: sense is defined as "current errors" and is consumed by the
read, so clearing is contract, not tidiness — leaving it latched would make one failure answer every
later query.

Note the READ path already zeroed its buffer on failure (#159). That stops stale data reaching the
guest but *reports a successful read of zeros*, which is precisely how a refused transfer stayed
invisible. The status and the zero-fill defend different things and both are needed.

### The overlay `exit(1)` was four sites, not one

`overlay_set_block_in_use()` held three (bitmap seek for read, bitmap seek for write, bitmap write)
and `fwrite_helper()` a fourth. All are guest-triggerable — a guest write to an overlaid disk lands
there, so a full filesystem killed the emulator outright rather than failing the write. The function
now returns 1/0 and its caller propagates: a bitmap update that fails means the block is written but
not *recorded* as written, so a later read would take it from the wrong layer.

This completes a conversion the tree had already begun in exactly one place — #164 turned the two
abort paths in `fwrite_helper()` into `return 0` and left its immediate neighbour aborting, four
lines apart.

### Detector

`regress/diff_diskimage_io.c` goes **8 failures → 0**, the `-DDISKIMAGE_IO_UNFIXED` guard is
**deleted** (keeping it after the defects were fixed is exactly the permanent opt-out its own note
warned about), and a new SECTION G asserts the boundary. Gate 2 goes 105 → 110 checks; the detector
runs **31 rows, 0 failures at `-O0/-O1/-O2/-O3/-Os`, 0 UBSan/ASan runtime errors**.

Three mutants survived the old suite and are now killed by named rows, because **every** past-capacity
row aimed at LBA 1,000,000 on a 1,008-block disk — a point so far outside that nothing near the edge
was tested:

| surviving mutant | closing row |
|---|---|
| bound one block too permissive | `WRITE one block past ADVERTISED is refused` |
| only the START offset checked, so a transfer begins legally and runs off the end | `WRITE starting in range but running off the end is refused` |
| writes bounded by advertised rather than the backed extent | `WRITE into the advertised gap is refused` + `the host file did not grow` |

One row needed no new code at all: the past-EOF row **already computed `allzero` and only printed
it**, asserting nothing but the return value — so inverting the read-side zero-fill (one character)
passed the whole suite while leaking host memory. *A row that computes evidence and does not assert
it is the same class of defect as a check that cannot fail.* Its `check()` now exists.

The gate's `rows actually run` minimum was also raised from 3 to 31. It was written when only three
rows ran by default; leaving it would have permitted 28 rows to be deleted silently.

### Assessed, not changed

* **READ CAPACITY now advertises blocks the disk will refuse to write.** `disklabel(8)` or `fsck` on
  a raw partition can issue exactly that. It **cannot** be fixed by advertising less: the pmax rig's
  on-disk label already records `d_secperunit = 614880`, so the advertised number is baked into
  guest-written data and is permanent. Recorded rather than papered over.
* **A 0-byte image is now unwritable AND unreadable** — `nr_of_logical_blocks` is 0, so both limits
  are 0 and every LBA is refused in both directions. (#417 corrects two things here: the original
  wording said only "unwritable", understating it; and "advertised capacity is 0" conflated the
  block count with READ CAPACITY's convention of reporting the address of the LAST block, where a
  field value of 0 describes one addressable block at LBA 0. The bound uses the block count, which
  really is 0.) Shipped code allowed the write and grew the file. No escape hatch was added: a
  `nr_of_logical_blocks > 0` exemption is the same shape #414 measured letting a zero-block disk
  skip a bound entirely. The documented image-creation workflow (`dd … seek=N`) produces a **sparse
  file with full `st_size`**, so it is unaffected. #417 adds rows pinning both directions.
* **The misaligned overlay read is fixed by none of this.** `fread_helper` advances `buf` by
  `OVERLAY_BLOCK_SIZE` regardless of `lentoread`, while `fwrite_helper` guards both misalignments.
  No overlay rows exist in any detector — **do not read overlay correctness into the zero-filled
  rows above.** Filed.
* **IDE/ATA propagation is not in this round.** `dev_wdc` still ignores the result on both reads and
  writes; the bound stops the growth, but the guest is still told the transfer worked. Doing it
  properly needs `d->error` to raise `WDCS_ERR` — merely checking the return while still queueing
  zero data would be insufficient. Filed.

## One-hundred-and-fifty-fourth round (#414) — one multiplication, two factors nobody computed, and every `-d g` disk reported no capacity

`diskimage_recalc_size()` finishes with

```c
size = d->heads * d->sectors_per_track * d->cylinders * 512;
```

**Two independent upstream omissions each left one of those factors at zero**, so the product —
and therefore the whole disk — was zero. They look like separate bugs and are one line's worth of
consequence:

* **the floppy arm** derived `sectors_per_track` from `d->nr_of_logical_blocks`, a field *this same
  function* does not assign until about twenty lines further down. On a freshly zeroed struct that
  read 0, and it was **stably** 0: a second call recomputed spt from the 0 it had just stored.
  The author's formula was right and named the wrong field — `d->total_size` holds exactly the byte
  count they wanted and is assigned eighteen lines above the broken line. The four sizes the manual
  lists divide by 80·2·512 to give precisely 9, 15, 18 and 36.
* **the `-d gH;S` override arm** never computed cylinders at all. A census settled it: `d->cylinders`
  had **exactly two** assignment sites in the file, and *both* sat inside `if (!d->chs_override)`,
  so supplying an override did not merely skip a default — it removed every write to that field
  that existed.

Reproduced before any edit, on the committed tree: the geometry differential fails **21 of 26 rows**
with its control row green. The headline is broader than "floppies and unusual geometries":
`-d g16;63:` — which merely spells out the tree's *own* default heads and sectors-per-track — also
returned `blocks=0`. **Every** use of `-d g` produced a zero-capacity disk.

**The fix hoists the cylinder computation out of both arms** into one shared, unconditional block,
which *removes* a duplicated copy of the arithmetic rather than adding one. The floppy arm derives
spt from `d->total_size` and clamps it to `[1, 255]`; the parser parses both `g` fields with
`strtoll(…, 10)` into `int64_t` and range-checks them **before any narrowing**. `bytespercyl` is
guarded itself rather than only its factors — the guard prevents a SIGFPE, and the clamp is what
makes the answer right; measured, guarding alone still returned `40960/2/0 blocks=0` for a 40 KB
`-d f:` image where the clamp gives `40/2/1 blocks=80`.

`atoi` was not a style question. On the shipped binary `-d g4294967312;63` (2³²+16) was **accepted
as heads=16**, because the truncation happened before any check could see the value.

### The bound is derived, and it restores an assumption the code already made

`DISKIMAGE_MAX_HEADS` / `DISKIMAGE_MAX_SPT` = 255 are not chosen. In `diskimage_scsicmd.c`'s MODE
SENSE pages, heads (page 4 byte 5, page 5 byte 4) and sectors-per-track (page 3 byte 11, whose
companion byte 10 is hardwired to 0, and page 5 byte 5) are **the only unmasked byte stores in those
blocks** — every neighbouring field is written `& 255`. Those four bare stores *are* the codebase's
own assertion that H and S fit in a byte; nothing enforced it, and an unclamped 256 truncated to 0.
255 also caps `H·S·512` at 33,292,800, which makes the cylinder multiplication overflow unreachable
by construction.

**Measured, and it decides the scope question:** the shipped tree reports **0** UBSan errors here,
the fix reports 0, and the variant with the arms fixed but *without* the bound reports **2** signed
overflows. The overflow does not exist today only because `cylinders = 0` annihilates the product —
so the bound is not hardening bolted on beside a fix, it repairs a defect that fixing the arms
*introduces*. Splitting the round would have shipped a new UB site.

### Records corrected, including several of our own

* *"An override cannot change advertised capacity, only its description."* **False**, and it was the
  entire basis of an earlier decision recorded for this task. Three review seats produced three
  counterexamples on one 1.44 MB image (2880 blocks autodetected): `g3;7` → 2898, `fg7;11` → 2926,
  `fg16;63` → 3024. It holds only when `H·S·512` divides the file exactly, which the one example we
  had generalised from happened to do. The manual now **documents** the capacity change instead.
* `man/gxemul.1` and this file's own header comment both said the `gH;S;` prefix is *ignored* for
  floppies. It never was: the code skipped the floppy arm whenever the override was set and simply
  produced no cylinders. Code and documentation had disagreed all along and the zero-capacity defect
  hid it. Both carriers are corrected — a tree-wide grep confirms there were exactly two.
* The manual's claim that cylinders "are assumed to be 80" is true only for the four standard
  formats; with the fix, `-d f:` on 40 KB gives 40 and on 20 MB gives 81.
* An earlier note warned that swapping the parser's heads/spt assignments "survives every row".
  **False for this detector**, confirmed independently by two seats: the `bound: 16;63` row runs
  through the real `diskimage_add()` and asserts the full tuple, so a swap yields 63/16 — identical
  `bytespercyl`, identical block count, wrong tuple. The stale note described an earlier draft.
* A brief for this round cited the ATA SDH head field (`d->head = idata & 0xf`) as a wider carrier
  that "agrees with room". It is four bits, i.e. **narrower** than 255, so an IDE guest cannot
  address more than 16 heads. `diskimage.h` records that narrowing as a limitation rather than
  citing it as support.

### The detector, and the five evasions it closes

`regress/diff_diskimage_geom.c` is new: 30 rows against the real `diskimage.c`, wired into gate 2
(94 → 102 checks). Every row asserts the **full tuple** — cylinders, heads, sectors-per-track *and*
block count — because a row asserting only "capacity is no longer zero" passes on a fix that
computes the wrong cylinder count.

A measure seat compiled and ran **38 mutants** against the 26-row draft: 23 killed, 15 survived, of
which 5 are provably equivalent and 10 were real evasions. Five rows close the five that matter, and
each is annotated in place with the witness that proves the mutant is a behaviour change rather than
a synonym:

| surviving mutant | witness | closing row |
|---|---|---|
| `720*1024` → `721*1024` — **one character** | a plain `:` 737280 B image returned 2/16/63 blocks=2016 instead of 80/2/9 blocks=1440 | the four floppy rows now pass type **UNKNOWN**, so each covers its own autodetection predicate; previously only *one* row reached that code at all |
| `if (prefix_g)` → `if (prefix_g && !prefix_f)` — **one token**, and literally what the manual used to claim | `-d fg2;9:` returned 80/2/18 instead of 160/2/9 | `fg2;9 is honoured through the parser` — no row had ever driven both prefixes together |
| `atoi` left on spt while heads gets `strtoll` | `-d g16;4294967360:` accepted with spt=64 | `bound: 2^32+64 … in the SPT position` — the suite's only wrap vector had been in the heads position |
| `strtoll(…, 0)` instead of base 10 — **one character** | `g010;63:` becomes 8 heads; `g0x10;63:` flips from rejected to accepted-as-16 | `parse: leading zero is decimal, not octal` |
| `if (d->cylinders < 1) d->cylinders = 1;` — a plausible defensive edit | a 0-byte disk goes from blocks=0 to blocks=1008 | `0-byte image stays empty (guards #412)` — **this row guards a fix from three commits earlier, not this one**: it is what keeps #412's zero-block guard firing on its own gate vector. The suite had contained no zero-byte image. |

**A second mutation pass against the resulting 30-row file ran 46 more mutants and found TEN MORE
real evasions, in three families the first pass had not reached at all.** Four further rows close
them, and the shape of the misses is the lesson — each family was a whole *region* of the input
space that no row entered, so tightening the existing rows could never have found them:

| family | what survived all 30 rows | witness | closing row |
|---|---|---|---|
| **the floppy divisor was pinned from one side only** | `512` → `511` (one character), `80` → `79`, ceil-for-floor. All four documented floppy sizes are exact multiples of 81920, so the floor divide is insensitive: **every divisor in [79706, 81920] survived** — 2215 integers, with the shipped value at the top of the window | `-d f:` on 736,000 B returned 80/2/9 instead of 90/2/8 | an `f:` row whose size is deliberately **not** a multiple of 81920 |
| **no row reached the shared block at type SCSI or IDE** — and that is the default type for every primary rig | wrapping the block in `if (d->type != DISKIMAGE_SCSI)` | `-d s:` on 10 MB returned **0/16/63, blocks=0** — *this round's own defect, reinstated*, for the type `get_default_disk_type_for_machine()` returns on PMAX/ARC/SGI/LUNA88K/MVME88K | `parse("s:…")` and `parse("i:…")` |
| **an unsigned parse folds a negative value back into range** | `strtoll` → `strtoull` at the spt site (one inserted character) | `g16;-18446744073709551615:` — `strtoull` applies the minus in unsigned arithmetic, yielding **1**, accepted as spt=1 | a −ULLONG_MAX row; note a plain `-1` does *not* discriminate, since both parses land below 1 |

The root cause of the second family is structural and worth stating: `diskimage_add()` assigns the
machine-default type **after** it calls `diskimage_recalc_size()`, so every parser-level row is still
UNKNOWN when geometry is computed. An explicit `s:`/`i:` prefix is the only way in.

**Verified:** **34 rows, 0 failures** at `-O0`, `-O1`, `-O2`, `-O3` and `-Os`, 0 warnings under
`-Wall -Wextra` at all five, **0 UBSan runtime errors**, and gate 2 green at 102 checks.
ASan is clean **only with `detect_leaks=0`**: by default LeakSanitizer reports ~9.9 KB in 33
allocations and `_exit`s, which also swallows the detector's buffered stdout so the log shows the
leak report instead of the results. Those leaks are harness-lifetime and pre-existing — HEAD leaks
*more* (11,328 B / 45 allocations), because it accepts the out-of-range geometries this round
rejects. Recorded because any future sanitizer gate row must set that option or it fails showing
nothing.

### Assessed, not changed

* The whole-cylinder round-up now creates advertised-but-unbacked tails on paths that previously
  advertised *zero* — `-d f:` on a 20 MB file advertises 41310 blocks (21,150,720 B) for a
  20,971,520 B file, a 179,200-byte tail whose first unbacked LBA is 40,960. **The phenomenon
  itself is not new** and the round must not claim it is: the default arm already advertised a
  516,095-byte, 100%-unbacked tail for a 1-byte plain image before this change. What the round does
  is (a) give two paths a tail where they had none, and (b) raise the worst reachable case from
  516,095 to **33,292,799 bytes — a 64.5× increase**, hit by `-d g255;255:` on a 1-byte file.
  This **makes the open write-bound work harder, not easier**, and is filed there: a bound written
  against advertised capacity would let a guest legally write LBA 0..65024 on that 1-byte image and
  grow the host file to 33,292,800 bytes. The bound has to be against `d->total_size`.
* **The `g` parse still accepts trailing garbage** — `-d g16abc;63:` and `-d g16;63abc:` are both
  accepted as 16;63, because `strtoll(fname, NULL, 10)` discards the end pointer. The tree's own
  precedent, `parse_int_option()` in `main.c`, uses `&endp` and rejects a non-empty remainder, and
  its comment names "accepts trailing garbage" as the reason it dropped `atoi`. This round adopts
  half that precedent: it fixes the truncation but not the trailing-garbage acceptance, which is not
  a regression (`atoi` did the same) but is more awkward to fix here because the terminator is `;`
  or `:` rather than NUL. Assessed, not changed.
* A **stale cross-file citation this round created and then removed**: `dev_wdc.c` cited
  `diskimage.c:254-268` for the whole-cylinder round-up, and hoisting that code invalidated the
  range — nine lines below a block that states citations there "name constructs, not line numbers,
  and that is deliberate". This is the #405/#407 mechanism for a third time; the reference now names
  the construct. **A diff that moves code must re-check citations in files it does not touch.**
* **A method note, because the error is invisible when it works:** the evidence first offered for
  the new `PRIi64` format string was that `-Wall -Wextra` produced no warning. That check *cannot
  fail* — `fatal()` carries no printf format attribute, so nothing verifies its arguments. The
  conclusion was right and the reasoning was worthless; it was settled properly by recompiling with
  a forced `format(printf,1,2)` attribute under `-Wformat=2` (no diagnostics) and by execution.
* `size & (logical_block_size - 1)` is a mask standing in for a modulo and assumes a power of two,
  while MODE SELECT accepts 256..8192. It fails identically before and after this round, so it is
  neither fixed nor affected here; a row for it sits behind `#ifdef GEOM_ROW_LBS257` with its vector
  and reason so the round that fixes it need not rediscover them. There are at least three sites.
* `diskimage_dump_info()` prints `int64_t` cylinders and sectors-per-track with `%i`. Undefined
  behaviour in diagnostics only, invisible to `-Wall -Wformat` because `debug()`/`debugmsg()` carry
  no format attribute. Its guard is `FLOPPY || chs_override` — exactly the two configurations that
  reported zero, so it now prints real values for the first time.
* Cylinders have their own narrower carriers and are **not** covered by an H·S bound: MODE SENSE
  page 5 gives cylinders two bytes where page 4 gives three, so `-d g1;1` on a 32 MB file now yields
  C=65536 and truncates to 0 there and in IDENTIFY word 1. Newly reachable via the override; filed.
* Even with H·S bounded, `ceil(size/bytespercyl) · bytespercyl` can exceed `INT64_MAX` for a
  near-`INT64_MAX` sparse image. Residual, not a reason to widen this round.

## One-hundred-and-fifty-third round (#413) — #412's prose was wrong in four places: a floppy answers nothing, because no device ever asks for one

#412 wrote that *"every floppy currently answers READ CAPACITY with 2 TiB."* A measure seat
drove the shipping binary and the shipped parser and established that **a floppy answers
nothing at all.**

**`DISKIMAGE_FLOPPY` is a write-only type in this codebase.** ~~It occurs in exactly seven
places, all inside `diskimage.c`/`diskimage.h`, and~~ **no device references it**. Every
controller hard-codes its type argument — six call sites pass `DISKIMAGE_SCSI`, one passes
`DISKIMAGE_IDE` — and both `diskimage_access()` and `diskimage_scsicommand()` select on
`d->type == type`. A floppy-typed disk is therefore never reached by any controller.

> **CORRECTED BY #418, struck through above rather than deleted.** The count was wrong on
> arrival and wrong in two independent ways: spelling `DISKIMAGE_FLOPPY` in a sentence that
> counts occurrences of `DISKIMAGE_FLOPPY` made the count eight, and "all inside
> `diskimage.c`/`diskimage.h`" was falsified by the sibling copy of this same sentence living
> in `diskimage_scsicmd.c`. The structural claim — no device references it — was and remains
> true, and is the form that survives edits. Rule earned: **a record may not state a count of
> an identifier it also spells.**

Measured, not read:

```
  ok  diskimage_exist(id 0, SCSI) -- what dev_asc asks   = 0
  ok  diskimage_exist(id 0, IDE)  -- what dev_wdc asks   = 0
  ok  the disk IS there under type FLOPPY                = 1
  ok  [CONTROL] with 's:' the SCSI controller DOES see it = 1
```

**So `-d d:image` on a floppy-sized file does not hand the guest a zero-capacity disk — it
hands the guest no disk at all**, while the console prints `FLOPPY DISK id 0, read/write, 0 KB`,
which reads like a device that is present. That is a *different* and more serious defect than
the one #412 described, and it is filed rather than fixed here.

**#412's fix and its gate row are untouched and remain sound** — the row uses a 0-byte image,
which genuinely *is* a reachable zero-block SCSI disk. Only the prose over-reached. The true
carrier was in the same sentence: **`-d gH;S` keeps its SCSI/IDE type** while carrying zero
blocks, so it does reach the handler. Measured: a 10 MB image announced as
`SCSI DISK id 0, read/write, 0 MB (CHS=0,16,63)`. The correction is a narrowing, not a reversal,
and it was applied to all three live sites (this file, the gate comment, and the source
comment); #412's commit message is immutable and is corrected here.

### Measured while confirming it — the numeric sweep

Every numeric option in `diskimage_add()` parses with `atoi` and validates only from below:

| option | parse | validated | verdict |
|---|---|---|---|
| `g` heads | `atoi` → `int` | `< 1` only | truncating, **no upper bound** |
| `g` spt | `atoi` → `int` | `< 1` only | truncating, **no upper bound** |
| `o` offset | `atoi` → **`int64_t`** | `< 0` only | truncating, **silent above 2³²** |

**The `o` failure splits, and only one half is loud.** `[2³¹, 2³²)` truncates negative and is
caught by the existing `< 0` check — it aborts. **`≥ 2³²` truncates positive and passes
silently:** `o4294967296 → 0`, `o4294967396 → 100`, `o9999999999999 → 1316134911`. And the
consequence is guest-visible — the bootblock read at offset 0 goes negative and is **served
zeros**, printing `[ reading before start of disk image ]`. A detector that tests only 2³¹
passes on entirely unfixed code; the discriminating vectors are `≥ 2³²` with positive low words.

Also measured: `o0x1000` is silently taken as `0`; trailing garbage `o1000abc` is accepted as
`1000`; two id digits silently let the last win; and **a `;` inside the pathname is consumed as
geometry** (the heads scan stops at `';'` but not at `':'`). No out-of-bounds read — every scan
tests for NUL first.

## One-hundred-and-fifty-second round (#412) — a zero-block disk told the guest it held 2 TiB

> **#413 correction.** This round's original title and prose said *"every floppy"*. That
> over-reached — see the #413 block above. The fix and its gate row are unaffected.


`SCSICMD_READ_CAPACITY` computes `size = d->nr_of_logical_blocks - 1` where `size` is
`uint64_t` and the block count is `int64_t`. **A zero-block disk therefore underflows and
announces last-LBA `0xffffffff` — 4,294,967,296 blocks, 2 TiB at 512 bytes each** — rather
than reporting itself empty.

**This is not a corner case today.** A separate live defect leaves *every* floppy and every
`-d gH;S` disk with zero blocks — and such a disk **keeps its SCSI/IDE type**, so it reaches
the handler and is told it holds 2 TiB. Measured: a 10 MB image announced as
`SCSI DISK id 0, read/write, 0 MB (CHS=0,16,63)`.
The `0 KB` the operator sees on the console is only the host-side banner; the guest is told two
terabytes. That was found by measuring the shipped code, not by reading it.

`0xffffffff` is also the ATA/SCSI "capacity too large for this command" sentinel, which makes
it the worst available answer for an empty disk: not merely wrong, but the one value that means
something else entirely.

Measured both directions against the real handler: `0 blocks -> last-block 0xffffffff` before,
`0x00000000` after.

### The detector ships with four sections deliberately disabled

`regress/diff_diskimage_io.c` (new, wired into gate 2 — now 94 checks) stubs five symbols and
`#include`s the shipping `diskimage.c` and `diskimage_scsicmd.c`, so the code under test is the
code that ships. It runs **3 rows / 0 failures** by default and **19 rows / 8 failures** under
`-DDISKIMAGE_IO_UNFIXED`.

The disabled four assert defects that are **still live and confirmed**, and enabling them now
would make the gate red for things nobody has fixed — a phantom regression rather than a
finding. They are kept *with their vectors* so the rounds that fix them need not rediscover
anything: a short write (256 of 1024 absorbed) and a total failure both return success with
errno 27; a read starting past EOF returns success; **one `WRITE(10)` past capacity grew a
10 KB image to 512,000,512 bytes and its capacity from 1,008 to 1,000,944 blocks, status
GOOD**; and a write onto a full store returns GOOD.

**The staging constraint that round must respect, measured:** all five rig images carry a
480–992 block round-up gap. The `#if 0` failure check inside `diskimage__internal_access()` is
currently harmless *only because* the SCSI layer swallows the result — fix both and the last
~0.25–0.5 MB of **every bootable image** returns CHECK CONDITION. `section_roundup_gap` measures
that gap and stays green either way, deliberately: it is evidence, not an assertion.

**Why the row uses a 0-byte image rather than a floppy.** A floppy row would go vacuous the
moment the geometry defect is fixed. The zero case is reached deliberately through an empty
image so the row stays valid afterwards — the two fixes are semantically coupled (the handler
calls `diskimage_recalc_size()` one line above the subtraction) even though they do not overlap
textually, and whichever lands second must re-measure.

## One-hundred-and-fifty-first round (#411) — the stopping condition #410 wrote could be satisfied to the letter while still shipping a false pass

#410 declared `regress/diff_wdc_identify.c` done against a written condition, precisely so that
"done" would be checkable rather than felt. A measure seat was then asked to **attack that
condition**, and found three ways through it — one of which #410 already contained. This round
repairs the condition itself. **No rows changed; the detector is comment-only here.**

**1. The row-name requirement was written as history, not as a rule.** It appeared under *"what
was true when this file was declared done"*, so a later round could satisfy the mandatory rule
— cite a mutant re-run against the shipped row — while the kill actually came from an
*unrelated* row. That is the #409 shape one level up. It is now stated as a requirement.

**2. The survivor classification carried no obligation to demonstrate anything.** The three
buckets were self-assigned prose, so any future round could retire an inconvenient survivor
into "accepted gap" with one sentence and satisfy the condition completely. Each entry must now
name **a row, a measured mutant result, or an explicit blocker with a reproduction**.

**3. "Checked, not assumed" was doing the work of a test while being prose.** #410 used it for
the no-stack-leak claim. Measured: deleting `diskimage_getname`'s return-value check — the
mutant that would expose a leak — **survives green at all five optimisation levels**, because
this file's own stub returns 1 unconditionally and no row can observe the branch. The phrase is
now permitted only where a row or a measured mutant backs it.

### Two classification entries were wrong on the reasoning, and both are corrected

**The "unreachable" blocker was incomplete.** #410 named `chs_override` as the only route to
heads/spt above 255. It is not: **`-d f:` sets the type to FLOPPY at any file size**, before the
recalc, with no override at all. Measured against the real `diskimage_recalc_size` — `-d f:` on
a 20 MB file would give spt **256**, on a 100 MB file **1280**. It is masked *today* only by the
very defect (#113) named as its blocker, so **fixing the override arm alone will not re-close
that bucket** — the `-d f:` route opens at the same moment. Timing right, mechanism wrong.

**The stack-leak conclusion holds, but not for the stated reason.** `snprintf`'s
NUL-termination is *irrelevant* on that path. What actually carries it: `diskimage_getname` does
not write `buf` at all when it fails — it returns 0 without touching it — so the protection is
the **caller's** return-value check falling through to a string literal; and the failure path is
unreachable anyway, because `wdc_command` returns ABRT when `!diskimage_exist` and
`diskimage_exist` uses the *identical* id/type predicate. The original wording licensed exactly
the wrong refactor: *"it always NUL-terminates, so the caller's check is redundant."*

16 rows, 0 failures, unchanged. This is the difference between a criterion that reads well and
one that resists being gamed — and the file's own history is the argument for caring.

## One-hundred-and-fiftieth round (#410) — the wdc detector is DONE, and this is the written condition it is done against

Four rounds went into `regress/diff_wdc_identify.c` — #405 built it, #407, #408 and #409 each
repaired the last — and **every one of the first three shipped believing it was complete.**
The scope was put to a review panel, which said stop. This round is the bounded close-out.

**Why they were wrong every time, in one sentence:** each round's confidence rested on *"the
mutants I thought of are dead"*, which is not a falsifiable claim. So the file now carries a
condition that is:

> **Every claim of the form "X was uncovered, this row covers it" must cite a mutant re-run
> against the SHIPPED row, not the designed one.**

#409 is exactly why. It added a row named *"geometry words carry their high byte"* and gave it
`s = 17`, so **word 6's high byte stayed permanently zero** while the row's name, the file
comment, the gate and the commit message all claimed words 3 *and* 6. The designed row covered
both; the shipped row covered one. Measured: forcing word 6's high byte to `0` survived at all
five optimisation levels, exactly as before the row existed. The fixture now carries
**distinct** high bytes — 4096, 300, 770 → `0x10`, `0x01`, `0x03` — so a mutant that *swaps*
two high bytes is caught as well. (A first attempt at the multi-drive fixture used heads 400
and 271, both high byte `0x01`, and killed nothing.)

**#409's inverted CD-ROM poison closed one direction and opened another.** Making the drive
under test the *only* non-CD-ROM meant the row could observe nothing but the **negative**
answer — so four mutants survived and **the entire ATAPI announcement was deletable with all
fifteen rows green**: dropping the `if (cdrom)` branch, forcing `cdrom` to 0, `0x8580` →
`0x8500`, and dropping word 0's high byte. A new row takes the other branch and requires
`0x8580`. Reachability is real, not synthetic: `WDCC_IDENTIFY` is rejected for a CD-ROM before
the switch, but `ATAPI_IDENTIFY_DEVICE` falls into the **same case** and calls the same
initializer with `cdrom` set.

**And #409 introduced a phantom-regression risk in the gate.** Its named-row check grepped
`'the right id'`, which appears only in the *ok* line — so a genuinely failing row *also*
reported "not present", turning one red row into two and making a failure indistinguishable
from a deletion. It now matches text the row prints either way.

### The scope, written down so a later round need not re-derive it

> **This file is the oracle for what `wdc_initialize_identify_struct()` BUILDS. It is not an
> oracle for what the guest RECEIVES.**

Every row reads `identify_struct` directly, so the transmit loop between that array and the
guest is invisible to all of them — swapping its two pushes byte-swaps every word a guest reads
at **zero failures**. That boundary is assigned to a separate I/O harness (queue #112), not to
more rows here. Measured: the content detector kills 64 of 93 `dev_wdc.c` mutants, a transport
harness kills 20, together 80 — **neither subsumes the other.**

The surviving mutants are now **classified rather than left implicit**, which is what makes
"done" checkable: *equivalent* (`/512` as `>>9`); *unreachable* — heads/spt above 255 require
`chs_override`, i.e. the `-d gH;S` path, **which is itself broken and files as queue #113**, so
these become reachable only when that lands; and *accepted gaps* — six unasserted constant
fields, two `memset` variants already covered by `DEVINIT(wdc)`'s own, two serial/firmware
placements. Checked rather than assumed: `diskimage_getname` is `snprintf`, which always
NUL-terminates, so the padding loop always finds a NUL and **there is no stack leak**.

Gate 2 PASS, **89 checks** (was 88); 16 rows. Timing correction to #409's record: the commit
said the detector "runs in ~1 s"; measured it is **0.024–0.042 s**. The 4,358× claim itself
reproduced independently at ~4,100× (140,328 ms → 24-42 ms).

## One-hundred-and-forty-ninth round (#409) — #408's UB fix cost 148 seconds, and it poisoned one stub out of three

A compile-and-measure pass built **246 mutants across five optimisation levels** against
#408's thirteen rows, plus ASan and UBSan. It began by making measurement possible at all.

### #408 shipped a 4,358× slowdown

`sizeof(struct cpu)` is **60,821,568 bytes**. #408's `fake_cpu()` — the correct fix for the
`NULL`-`cpu` undefined behaviour — memset it **on every call**, and the self-consistency
oracle calls it 65,535 times: roughly **4 TB of memory traffic**. Measured, hoisting the
zeroing to first-call-only:

```
shipped: 148,188 ms      hoisted: 34 ms      output byte-identical (cmp)
```

The detector detected exactly the same things either way. *The fix was right; doing it per
call was not*, and nothing in #408 measured the cost of its own correctness fix.

### One stub poisoned, two left answering questions nobody asked

#408 poisoned `diskimage_getsize()` and wrote the reason into the file — *"a stub that answers
correctly for an id nobody asked about is not a stub, it is a second implementation"* — then
left `diskimage_is_a_cdrom()` and `diskimage_getname()` ignoring `id`. **Four mutants survived**
(each of those two, against both a dropped `base_drive` and an off-by-one id). #408's commit
message claims it closed `base_drive` "at all three call sites". **It closed one.**

The `is_a_cdrom` case is reachable: a machine with a disk at one id and a CD-ROM at the next
would make the disk announce itself ATAPI/removable.

**Poisoning it required inversion, and the obvious construction failed.** Putting the CD-ROM at
one specific id does not work — the correct id here is 3, so the dropped-`base_drive` mutant
asks about id 1 and the off-by-one asks about id 4, and both simply *miss* the CD-ROM and still
read "not a CD-ROM". Both survived the first attempt. The stub now answers **wrongly for every
id except the expected one**, so any id arithmetic error flips word 0 to `0x8580`.

### An out-of-bounds read that only ASan could see, closed with a row instead

`base_drive` is a diskimage id, not an array index, and the per-drive arrays are `int cyls[2]`.
A mutant indexing them as `[d->drive + d->base_drive]` reads element 2 of a two-element array —
and **survived all five optimisation levels**, because nothing asserted that drive's geometry.
Asserting it in `row_base_drive()` kills it without putting a sanitizer in the gate.

### Two more measured gaps

No fixture pushed heads or sectors-per-track past 255, so the `>> 8` half of words 3 and 6 was
never non-zero and could be replaced by a literal `0` undetected; a wide-geometry row now
carries `h=300`. And the `-Os` crash was **understated** — #408's message named `-O0` and `-O1`,
but `NULL` `cpu` gives `O0=CRASH O1=CRASH O2=SURVIVED O3=SURVIVED Os=CRASH`.

Gate 2 PASS, **88 checks** (was 86); 15 rows, and the whole detector now runs in about a
second. Every mutant above is killed **by the row that names it**.

## One-hundred-and-forty-eighth round (#408) — the round that corrected stale citations committed the identical error, and the detector was relying on the optimiser

#407's headline record was that #405's line citations had gone **stale by exactly +31 — the
length of the comment #405 itself inserted.** It wrote that lesson into the source: *"re-read
every line reference AFTER the edit is in place."*

**#407's own comment insertion was +9 lines net, and every citation it "corrected" is stale by
exactly +9.** Verified by reading each line: the transmit loop is at `:526-529`, not `:517-520`
(which is `d->int_assert = 1;` in `WDCC_RECAL`); reassembly is `:609-627`, not `:600-618`; the
six `& 255` lines are at `:287-289`/`:293-295`, not `:278-280`/`:284-286`. **Lines 279-284 —
precisely where the record said the defective lines were — contained #407's own sentence about
re-reading citations.**

**So writing the lesson down did nothing, and the fix is not better line numbers — it is
fewer of them.** A line reference inside a file the same commit edits is measured against the
file it was written in, not the one that ships. Every citation in both files and in the
CHANGELOG now **names the construct** (`wdc_command()`'s `WDCC_IDENTIFY` case, the `wd_data`
read in `dev_wdc_access()`, the capacity assignments for words 57-58/60-61), which survives
every future edit instead of resetting the cycle.

### The detector was relying on the optimiser to hide undefined behaviour

`wdc_initialize_identify_struct()` dereferences `cpu->machine` three times. #405 and #407 both
passed **`NULL`**. It appeared to work only because `-O2` inlines the stubs and deletes the
load. **Measured: the same driver segfaults at `-O0` and `-O1` (exit 139).**

That is not a latent nicety. It meant the gate's *optimisation flags were load-bearing for
correctness*, so a future "let's build the regress tools at `-O0` to debug this" would have
turned the gate red in a way indistinguishable from a real capability regression. The driver
now builds a real zeroed `struct cpu` pointing at a zeroed `struct machine`, and is verified
across **`-O0`, `-O1`, `-O2`, `-O3` and `-Os`** — 13 rows, 0 failures at every level. The
link-flag requirement (`-ffunction-sections -fdata-sections -Wl,--gc-sections`, without which
it does not link at all) is now recorded in the file as load-bearing rather than cosmetic.

### Three more holes, all found by mutation and all on live paths

**The slave's geometry was never checked — only its capacity.** #407 closed the mutant that
made the slave report the master's *capacity* and never asked whether it reports its own
*cylinders, heads and sectors*. Four mutants (`cyls`/`heads`/`sectors_per_track` reading
`[0]` instead of `[d->drive]`) survived all twelve rows. Master and slave are now given
**deliberately different geometries** (16/63 versus 15/17) so that reading the wrong drive's
field cannot coincidentally agree.

**`base_drive` was entirely ungated, and it is not hypothetical** — `dev_wdc_init()` sets it
to **2 for the secondary controller** (the `0x170` address arm), so every access there adds
it. Dropping `+ d->base_drive` from all three call sites survived every row. A new row puts
drive 0 on a `base_drive = 2` controller and requires it to read diskimage id 2.

**The stub was answering questions nobody asked.** #407's id-dependent `diskimage_getsize()`
fell back to the single `stub_size` for any unpopulated id — and `row_slave()` had set that
fallback to the *slave's* size, so the mutant `id + 1` returned the correct answer and
survived. The table is now **poisoned** outside the populated ids. A stub that answers
correctly for an input under test is not a stub; it is a second implementation.

### Records corrected

- **The word-49 narrative was wrong, though the row is right.** #407 called `[2*49+1] = 2` an
  "advertising LBA" mutant. That is the **low** byte, which is vendor-specific; LBA is `0x200`,
  the **high** byte. The in-tree OpenBSD guest settles it — its `wdc.c` takes capabilities from
  `tb[49] >> 8` and puts the low byte in `wdp_vendor3`, which is never read. The row pins both
  bytes, so the detector was always correct; only the description was not.
- **"`diskimage_getsize()` returns a multiple of 512 always" is too strong.** A guest MODE
  SELECT can set `logical_block_size` to any value in [256, 8192], and `dev_wdc.c` reaches
  that path for ATAPI. The dismissal of the `(total_size + 511)/512` mutants holds for every
  ordinary disk; the word "always" did not.
- #407's **commit message** says "three rows added". Two were added and `row_selfconsistent()`
  was widened. The message is immutable; the correction is recorded here.

## One-hundred-and-forty-seventh round (#407) — the detector two rounds ago shipped with four holes and a note that was wrong in the flattering direction

A pass-2 measure seat built and ran **133 mutants** against #405's `diff_wdc_identify.c`,
classifying each under **two independent oracles** — the shipped detector, and a 64-bit
behavioural signature over all 65,535 reachable whole-cylinder sizes plus 4,096 random counts
to 2⁴⁰, edge counts, non-512 multiples, slave drive and CD-ROM — so that no-ops could not be
miscounted as survivors. Result: **90 detected, 17 no-op, 15 survivors, 1 build failure**
(the seat's own malformed control, scored as a fault rather than a detection).

**No pure-arithmetic rewrite of the capacity block survives**, and the reason is measurable
rather than rhetorical. The seat computed which byte values the rows exercise per lane:
`>>0` and `>>8` are saturated at 256 of 256, while `>>16` sees 31 and `>>24` sees only 3.
Those two look wide open, but the `1`-sector and `0xFFFFFFFF` rows jointly pin every
single-constant rewrite to the identity — a mask must contain every bit of `0xFF`; `|`/`+`/`^`
must fix 0; `*` must fix 1; `%` and `/` must no-op on `0xFFFFFFFF`. **The all-ones row turns
out to be load-bearing.**

### The survivors all conditioned on state the harness pinned

**Smallest was ten characters** — delete `d->drive + ` from `dev_wdc.c:179`, and the **slave
announces the master's capacity**, passing all ten rows. Measured on a 100-cylinder master
with a 300-cylinder slave: drive 1 reported 100,800 sectors while still reporting 300
cylinders — a block contradicting its own geometry, which is exactly what the spec-free
oracle claims to guard. It was invisible because `build()` memset the struct and never set
`d->drive`, and the stub `diskimage_getsize()` ignored its `id`. Fixed by making the stub
id-dependent and adding one slave row.

**Runner-up was one character**: `[2 * 49 + 1] = 0` → `= 2`. (*#408: that sets the LOW byte,
which is vendor-specific — LBA is `0x200`, the HIGH byte. The row pins both bytes so it is
correct; only this description was wrong. The in-tree OpenBSD guest reads `tb[49] >> 8`.*)
#405 had
documented in prose why that zero is deliberate and then not gated it. Now asserted.

**An 11-bit cylinder truncation also survived.** `(cyls >> 8) & 7` produces 63,488
self-contradicting cylinder counts starting at c=2048 — and the oracle's loop stopped at
`c <= 2000`, **missing it by forty-eight.** The bound is now 65535, the last count word 1 can
represent. Gating the whole block on `cdrom` survives too, and `:455-462` shows that path is
reachable via `ATAPI_IDENTIFY_DEVICE`; that one is filed.

### Three records corrected, one of them wrong in the direction that flatters

**The "known survivor" note was false.** #405 recorded a compensating pair — swap `+0`/`+1`
in the eight capacity lines *and* swap the two transmit pushes — as invisible to the driver.
Built, it produces **eight failures**. So does the packing swap alone. The mutation that
genuinely is guest-invisible is the **whole-struct** swap plus the transmit swap, which the
note never described — and the word-53 anchor **catches even that**, nine failures, reporting
`02 00, want 00 02`. So the anchor earns its keep against a mutation nobody anticipated.

**The citations were stale by exactly +31 — the length of the comment #405 itself inserted.**
`:486-489` and `:571-575` had become the `WDCC_IDP` case and the tail of a `fatal()` string;
the real transmit loop is the `for (i=0; ...; i+=2)` in `wdc_command()`'s `WDCC_IDENTIFY`
case, and reassembly is the `wd_data` read in `dev_wdc_access()`. **Nothing the citations said was
wrong — only the numbers had moved.** A line reference written before its own insertion is
measured against the file it was written in, not the file it ships in.

**The oracle described a measurement it did not perform.** The comment claimed "65,471 of
65,535 … first at 65 cylinders", which is true for H=16 — the geometry `diskimage.c:255-256`
actually pins — but the loop used H=15 and stopped at 2000, so on reverted code it printed
"1931 of 2000, first at 70". Both true, of different geometries. The loop now uses H=16.

### Confirmed, and recorded so nobody re-investigates

**The byte order is correct**, settled by executing the whole guest path rather than by
argument: both the LE and BE branches plus `memory_writemax64` land the *same* two bytes in
guest memory, so the device layer is byte-stream-preserving. No ATA document was consulted —
there is none in this tree. Two apparent survivors (`(total_size + 511)/512` and `+256`) were
**discarded as artifacts of the seat's own probe**: `diskimage_getsize()` returns
`nr_of_logical_blocks * logical_block_size`, a multiple of 512 for every non-ATAPI disk.
(*#408: "always" was too strong — a guest MODE SELECT can set `logical_block_size` to any
value in [256, 8192], and `dev_wdc.c` reaches that path for ATAPI. The dismissal holds for
ordinary disks; the word "always" did not.*)

**The real blind spot is recorded and deliberately not closed here.** The transmit loop
(the `for (i=0; ...; i+=2)` in `wdc_command()`'s `WDCC_IDENTIFY` case) is entirely ungated: swapping its two pushes byte-swaps every IDENTIFY word a
guest reads — 4,096 heads, 13,330 cylinders — at **zero failures**, because this driver reads
`identify_struct` directly rather than through the path the guest uses. Closing it needs a
different harness (drive `wdc_command(WDCC_IDENTIFY)` then `dev_wdc_access` on `wd_data`),
which is new machinery rather than another row.

Gate 2 PASS, **84 checks** (was 81). Each new row was verified to kill its mutant **by name**
— the mutant harness asserts which row fired, not merely that something failed, because a
kill from an unrelated row would leave the named one still blind.

## One-hundred-and-forty-sixth round (#406) — a word in a comment broke the build, and the comment is still there on purpose

The first full battery run since #392 came back **`REGRESS_FAIL`**. Gate 1 failed 8 of 18
checks, no binary was published, and **eleven downstream gates therefore skipped** — so the
coverage debt that run was meant to pay is still open. All 358 pmax and 363 arc errors were in
one file, `autodev.c`, with **zero** errors anywhere else.

**The cause was a comment I wrote in the previous-but-one round.** `makeautodev.sh` scrapes
device names out of the sources:

```sh
C=`grep DEVINIT $a | cut -d \( -f 2|cut -d \) -f 1`
for B in $C; do
	printf "int devinit_$B(struct devinit *);\n" >> "$AD"
```

`for B in $C` is **unquoted**, so the shell applies word splitting *and pathname expansion*.
`dev_rs5c313.c:144` is a prose line in #404's own record comment — `" *  gmtime being the
right choice and consistent tree-wide, the DEVINIT defaults,"`. It matches `grep DEVINIT`; it
has no `(`, and `cut` passes a line through unchanged when its delimiter is absent; so its
leading `*` survived both cuts and became a glob over the whole directory.

**319 declarations instead of 77.** 229 of the extras carry a `.` — `Makefile.skel`,
`bus_isa.o`, and even this script's own in-flight temp file `autodev.c.new.NNNN` — and are
syntax errors. The other 14 are valid C identifiers (`Makefile`, `README`, `fonts`, and the
comment's own words) which would have failed at link time instead.

**It hid for exactly two commits, and the reason is worth recording.** `autodev.c` is a
*tracked generated file* and the committed copy is clean. The corruption only exists once the
generator runs, which needed the make rule to fire — and it fired because #405 edited a
`dev_*.c`. This is the tree's own "regenerate before believing a generated file" rule biting
from the opposite direction: the stale artifact **concealed** a live break. #404 armed it,
#405 tripped it.

### The fix, and why it has two halves

Anchored the four scrapes to `^DEVINIT(` / `^PCIINIT(`, and bracketed each inner loop with
`set -f`. **These are not alternatives.** Measured: anchoring is what removes the prose words;
noglob alone still emits all 14 of them and merely moves the failure from parse to link.

`set -f` is scoped to the inner loops rather than set once at the top of the script, because a
script-wide noglob would stop `for a in dev_*.c` from expanding at all — which fails
*silently*, generating an empty device table.

**Anchoring is exact, not a heuristic, and this was verified rather than assumed.** All 77
`^DEVINIT(` sites and all 28 `^PCIINIT(` sites sit at column 1; none is indented and none sits
under a nearby `#if`. The anchored name list is set- **and order-**identical to the committed
`autodev.c` in both trees, and the hardened generator's output is **byte-identical** to the
committed `src/devices/autodev.c`. So the change provably cannot alter the shipped device
table.

**`dev_rs5c313.c:144` was deliberately NOT reworded.** Rewording it was the obvious move and
it is the wrong one: it would make the hardening deletable in silence — revert the generator
and everything stays green. Left in place, the live tree *is* the hostile input, so the mutant
lane below genuinely fails the moment the anchor goes.

### The detector, and the mutant that would have slipped through

`regress/diff_autodev_gen.sh` (8 rows, wired into gate 2, now 81 checks) runs the **real**
generator in a scratch copy — never in the repo, which would write two tracked files — and
derives its expectation from the declarations rather than from the committed artifact, since a
tracked generated file is not evidence about its own generator.

*** The load-bearing row is the ORDERED NAME LIST, not a character check, and the mutant lane
proves why. *** Carried as a named case is the realistic half-repair — keep `set -f`, drop the
anchor — which emits **27 extra names of which 26 are dotless**. Those are valid C identifiers
that a "no identifier contains a stray character" row waves straight through. The full revert
emits 265 extra, 24 dotless. Order is asserted alongside the set because `device_register()`
order is the order devices are offered to a machine.

A third mutant — anchor kept, noglob dropped — is **recorded as surviving** in an unasserted
note rather than dressed up as a kill, because a valid C declaration cannot contain a glob
character and a row that passes either way proves nothing.

**Landing note, because a green row nearly hid this:** `gate_build.sh:95` syncs only `*.c`,
`*.h` and `*.cc` into the compile trees, so `makeautodev.sh` does **not** travel. Editing it in
the repo alone would have left both build trees running the old generator while "source tree
fully synced into compile tree" stayed green. It was hand-propagated to `est/` and to both
compile trees, and the corrupt `autodev.c` was **deleted** from each rather than overwritten
from the tracked copy — overwriting would have reinstated exactly the stale artifact that hid
the break.

Filed, not fixed here: the `COMMENT` loop uses a filename as a `printf` **format string**
(`printf "$a "`); `rm -f .index` may race under `make -j`; and `src/machines/makeautomachine.sh`
plus `experiments/make_index.sh` share the same unquoted-scrape idiom, with zero live triggers
today.

## One-hundred-and-forty-fifth round (#405) — the disk told the guest the wrong size, and the test that proves it had to be built backwards

`wdc_initialize_identify_struct()` packs the ATA IDENTIFY capacity into eight byte
assignments. **Six used `% 255` where `& 255` is meant** — the eight capacity assignments for
words 57-58 and 60-61 in `wdc_initialize_identify_struct()`.
The two that were already correct are the bottom line of each group — the only two whose
operand is a single byte to begin with. That asymmetry is the sole evidence of intent
available, because **there is no ATA specification in this repository**, and the fix is
scoped to exactly what that evidence supports.

This is not a rare corner. The other six lines shift **without pre-masking**, so their
operand is a multi-byte quantity and `% 255` is a base-256 digit sum rather than byte
extraction — verified in closed form with 0 counterexamples over 2²⁶:

    x % 255 == ((x >> 8) + (x & 255)) % 255

Above the divergence point it is wrong 100% of the time. The ~0.39% of sizes where the
`>> 8` byte comes out accidentally right are precisely the ones where `>> 16` is wrong.
Worst case a real disk announces **zero sectors**.

**Smallest divergence, reachable rather than theoretical.** The raw threshold is 65,280
sectors, but `diskimage_recalc_size()` (`diskimage.c:254-268`) rounds every image up to
whole cylinders, so that exact count cannot occur. The smallest count an actual image can
have is **33,546,240 bytes / 65 cylinders — a 32 MB disk that announces itself as 120 KB.**

**The byte order was examined and deliberately left alone**, and saying so matters because
two panel seats called it a second defect. They were reading the snippet. `:187` states the
convention in the file's own words ("Offsets are in 16-bit WORDS! High byte, then low"),
the geometry words follow it, the transmit loop in `wdc_command()`'s `WDCC_IDENTIFY` case
pushes `[i+1]` before `[i+0]`, and `dev_wdc_access()`'s `wd_data` read reassembles
`(high << 8) | low`. The two seats that read
the file found it consistent, and execution agreed. The 57-vs-58 *word* order is not
establishable from this tree at all — so a mask-only correction is exactly as much as the
source can justify, and no more.

### The detector, and why an obvious table would have been worthless

`regress/diff_wdc_identify.c` (10 rows, wired into gate 2, now 73 checks) is the third
instance of the offline-differential construction after `diff_ieee_store.c` and
`diff_sh4_tmu.c`: stub the `diskimage_*` externals, `#include` the device file, and the
function under test **is the one that ships**.

*** `%` and `&` return the same byte for every operand below 255. A table of
plausible-looking disk sizes therefore **passes on the unfixed code** — every disk under
33,423,360 bytes agrees. *** So each row names the specific byte it drives past the
divergence point: 65,280 (`>>8` threshold), 65,536 (carry into `>>16`), `0x12345678` (all
four bytes distinct), `0xFF0000` (the window where `>>8` is accidentally right, which is
what proves the `>>16` line is checked at all), `0xFF010203` (`>>24` threshold), and
`0xFFFFFFFF`. Two small controls sit below the threshold to show the rig reports true
values rather than to detect anything.

Measured against mutants rather than asserted: the **full revert fails 7 rows**, and a
**partial fix correcting only the two `>> 8` lines still fails 4** — the half-repair a
carelessly chosen table would have waved through. A positive control (`+1` on an
already-correct line) fires on 8, and the harness refuses to score a build failure or a
signal as a row kill.

**A spec-free oracle, which is the part worth reusing.** With no ATA document available the
absolute encoding cannot be cited — but images are rounded to whole cylinders, so the sector
count *is* the product of the geometry words in the same block. The block can therefore be
checked against **itself**, needing no specification whatsoever. On the shipped defect,
65,471 of 65,535 cylinder counts produce an IDENTIFY block that contradicts its own geometry.

**Known survivor, recorded rather than papered over.** A compensating pair that swaps `+0`/`+1`
across all eight capacity lines *and* swaps the two pushes in the transmit loop is invisible to
this driver, which reads `identify_struct` directly rather than through the transmit path. The
word-53 anchor catches the packing half alone; word 47 is `0x8080`, a byte-swap palindrome, and
would have been useless for that.

**Not touched, deliberately: word 49 (LBA support) stays zero.** The LBA offset arms in
`wdc__read`/`wdc__write` are `#if 0`, and `d->lba` is parsed in the `wd_sdh` case and then
never reaches an offset computation. Advertising
LBA while still computing CHS offsets would send a guest's requests to the wrong place — the
zero may be accidentally load-bearing. **#407 gated it**: a one-character edit setting word 49
to `2` passed all ten of this round's rows, so the deliberate zero is now asserted.

## One-hundred-and-forty-fourth round (#404) — the SH-4 RTC is not settable, and that is recorded rather than guessed

A device audit flagged `dev_rs5c313.c` as re-reading host time before every access including
writes, so a guest could never set the clock and was told the write succeeded. Both halves
reproduce against the real `DEVICE_ACCESS(rs5c313)`: one write of 9 to `SEC1` from an
all-zero register file moves **12 of 12** non-target time registers to host digits, and a
readback at the *same instant* returns host time rather than the written value. The
survivors are exactly `TINT`, `CTRL` and `TEST`.

**Two measurements narrow what that means, and they are why this ships a record rather than
a patch.** A variant that ignores writes to all thirteen clock registers outright is
**guest-indistinguishable** from what ships today. So is one that refreshes only on reads —
0 mismatches in 248,581 reads. This is therefore not corruption of a value a guest could
otherwise rely on: **the clock is simply not settable, and never has been.** A missing
feature, which is a different and lesser thing than the audit's original framing.

That also disposes of the obvious repair. "Call `update_time` only on reads" is not merely
insufficient, it is *unobservable* — shipping it would have been a false record.

**A correct fix needs an offset model, and it is not attempted for measured reasons rather
than cautious ones.** `rs5c313reg.h:64-67` names `CTRL_BSY`/`CTRL_ADJ` and
`CTRL_XSTP`/`CTRL_WTEN` — a hold/busy protocol this device ignores entirely — but supplies
**bit names only**. It does not say that `WTEN` gates writes, what event commits a staged
time, or whether the counter holds meanwhile.

The house pattern argues *against* guessing rather than for it. `dev_mk48txx.c:98-106` gates
on a latch that **its own header documents** — `mk48txxreg.h:101` reads
`/* want to read (freeze clock) */`. `dev_mc146818.c:532-540` does the same with
`MC_REGB_SET`, in a comment that says so. `rs5c313reg.h` carries no equivalent, so reasoning
across would be an analogy to a different chip. And the guess is not free: implementing
"hold while `WTEN` is set" is guest-**distinguishable** from today, **64,687 divergent
reads**, so a wrong guess can regress a machine that currently boots.
`dev_dreamcast_rtc.c:70-74` already records the project's position on RTC writes —
deliberately ignored, because setting the host's clock "would probably be very annoying".

The record now sits in `dev_rs5c313.c` above the access function, where the next person
finds it before re-deriving it. It also names the rest: `CTRL_24H` is accepted and never
consulted (a read at 13:00 is identical with the bit set or clear), `TINT` is unimplemented,
the two-digit year aliases so 2105 reads as "05", and a pre-1900 host clock yields non-BCD
digits through C99's negative `%`, measured as `YEAR1 = 0xfa`.

**`WDAY` is deliberately left alone.** Both siblings use `tm_wday + 1`
(`dev_mc146818.c:196`, `dev_mk48txx.c:69`) and `mk48txxreg.h:75` documents
`weekday (1..7)` — but that is a different chip and `rs5c313reg.h` says nothing. Changing it
on analogy is exactly the guess the rest of the note declines to make, so upstream's
"TODO: Is this correct?" stands, unanswered and honest.

Checked and **correct**, so they are not re-investigated: `YEAR10`, `MON1`/`MON10` and every
digit encoding (0 mismatches across ~170,000 samples spanning 1970–2105), `gmtime` being the
right choice and consistent tree-wide, the `DEVINIT` defaults, and the register bounds.

Two findings worth keeping beyond this device. A **compensating pair**: dropping the
read-side `& 0x0f` is dead code because the write side already masks, so each mutation alone
is invisible to every guest-visible row and only the pair is detectable — catching it needs
a row that reads `d->reg[]` directly rather than through the device. And the differential
harness itself had a bug that made both sides call the mutant, reporting INDISTINGUISHABLE
for a mutation that plainly changes a read value. **It was caught only because a
known-detectable mutant was carried as a positive control** — the strongest available form
of asking whether a test failed for the reason under test.

No behavioural change. Comment only; `dev_rs5c313.c` byte-identical in `est/` and
`GXEMUL-SEC`, and it compiles clean.

## One-hundred-and-forty-third round (#403) — gcov said the interrupt line had never run, and fourteen wrong versions passed

A measure seat replayed the #400/#401 table under gcov and found `dev_sh4.c`'s
`timer_interrupts_pending[i]++` marked `#####` — **never executed**. No row had ever set
`TCR_UNIE`. It then constructed **fourteen wrong implementations that passed the whole
table**, and that coverage hole is why most of them were invisible.

Re-measured against the committed table before fixing anything, because #401 had already
moved: `nomod` was dead, and **five were still live**. Only those five were treated as
real.

* **`signed_cmp`** — writing the borrow test signed declares an underflow from the reset
  default `TCNT = 0xffffffff` on the first tick and every tick after, raising a spurious
  interrupt 400 times in 400. No value-only row saw it: the counter still lands on the
  right number, and only the UNF flag differs.
* **`unf_assign`** — `d->tcr[i] = TCR_UNF` instead of `|=`. One character, and it wipes the
  guest's prescaler select and its UNIE bit on every underflow. `TCNT` is identical either
  way, so no arithmetic row can see it.
* **`period_tcor0`** — `tcor[0]` inside the *period* expression. #400 claimed the
  three-timer row killed the index mutants; it kills `tcnt[0]`, the reload's `tcor[0]`, and
  both together, but **this neighbour survived**, because every timer in that row had
  `remaining < period` so the modulo never reduced. Correcting the row's third timer to
  `step = 40` makes the subscript observable.
* **`no_pend`** and **`no_gate`** — deleting the interrupt increment, and ignoring `TSTR`
  entirely. Both invisible while no row set UNIE and every row started the timers it
  inspected.

Three rows close them: an underflow with `TCR_UNIE` set that asserts the pending count
*and* that the guest's other TCR bits survive; a stopped timer that must not move; and the
reset default asserting the value **and** `UNF = 0`. Sixteen rows now, and each of the five
dies to one, two or three of them — none is carried by the pile.

**The test's `fatal()` stub now prints.** A seat measured that a row tripping the refresh
branch at the top of the tick died with `exit 1`, sixty bytes on stdout and **zero on
stderr** — the message naming the cause was discarded by the stub. Failing closed is right;
failing closed and silent is not.

**Two records corrected.** #400's "the three-timer row kills both" is true of the two
mutants named and false of the third neighbour, as above. And `diff_sh4_tmu.c`'s claim that
"a mutation to dev_sh4.c is seen by this test by construction" had fourteen
counter-examples; the defensible statement — the one `gate_offline.sh` actually makes — is
narrower: *transcription drift* is impossible, because the function under test is the one
compiled. Being unable to drift is not the same as being unable to hide.

Also measured, and worth keeping: the patch is bit-identical to the pre-#400 code across
216,527 non-underflow cases on every observable field; at `step == cnt + 1` the old code
landed on `TCOR - 1` in only 5,081 of 19,231 cases and anywhere at all — including *above*
`TCOR` — in the rest, so no guest could have been written against it. `d->tcnt[]` is read
in exactly two places tree-wide, so the blast radius is one guest register. And the
already-filed truncation at `dev_sh4.c:204` loses **63.25 counts per second** at the
landisk P4 prescaler, which is the first number anyone has put on it.

Gate 2 is green at 63 checks.

## One-hundred-and-forty-first round (#401) — the eleven rows never once exercised the modulo, which is the correction

Panel pass 2 on the shipped #400 diff. **Four seats independently found a wrong
implementation that passed all eleven rows**: delete `% period` and the test stays green.

The reason is uncomfortable. No row ever reached `remaining >= period`. Three had
`remaining == 0`; the rest used a period (2^32, or 20834) far larger than any remaining
they produced. So the modulo — the thing the correction *is* — was never exercised, and
#400's kill map did not notice because it asked which mutants each row catches and never
asked **which mutant no row catches**.

One seat found the subtler sibling: `period = tcor ? tcor : 1` dodges the SIGFPE that #400
leaned on *and* passes all eleven rows. So the round's claim that the crash covers the
missing `+1` was incomplete — a guarded variant escapes both the fault and the table.

Two rows close it, and they were chosen to separate `TCOR+1` from `TCOR` as well:

* `TCOR=5, TCNT=3, step=20` — three ticks to zero, one more underflows to 5, sixteen
  remain; `16 % 6 == 4`, so `5 - 4 == 1`. With period `TCOR` it would be `16 % 5 == 1`
  and land on 4. Measured: `no_modulo` gives `fffffff5`, `guarded_period` gives `4`.
* `TCOR=20833, TCNT=100, step=100000` — `99899 % 20834 == 16563`, so `20833 - 16563 ==
  4270`. Measured: `guarded_period` gives `10aa` against `10ae`.

Both mutants now die, and by those rows specifically. The gate names them and requires two
of them, so deleting one is visible rather than silent, and the row floor rises to 13.

**A record was also too strong.** #400 said the transcription vacuity was *structurally
impossible* here. It is not. `static` only forecloses linking the function from a separate
translation unit; it does nothing to stop a test from `#include`-ing the file **and also**
carrying a second, differently-named transcribed copy, then asserting against that. What
actually rules the vacuity out in this file is that nobody wrote one — established by
reading it, not proved by the storage class. What is true, and is enough, is that **it cannot happen
silently while the include line remains** — deleting that line does not weaken the test,
it fails to compile. Corrected in the file.

Gate 2 is green at 60 checks.

The general lesson is the one this round is named for. A kill map that lists a killer for
every mutant you thought of still says nothing about the mutant you did not, and the
mutant you do not think of is disproportionately likely to be *the deletion of the thing
you just added* — because that is the edit whose absence you are least able to imagine.

## One-hundred-and-fortieth round (#400) — the SH-4 timer pinned itself at zero, and a booting guest's clock stopped

`sh4_timer_tick()` detected underflow and reloaded in `int32_t`, then clamped a negative
result to zero. Once a reload could not lift the counter back above the sign boundary,
`TCNT` pinned at 0 and every later tick re-underflowed and re-clamped.

Measured on a booting guest before anything was changed: OpenBSD/landisk's `date -u`,
sampled every 30 s, tracked host UTC exactly for seventeen samples — second for second —
then froze at `00:52:10` and returned that identical value for seventeen more. 8m43s of
divergence and still growing, while the guest stayed fully alive and answered all 34
debugger prompts. An offline replication pre-registered the freeze at 515.4 s; a measure
seat then reproduced it on the real function at call 56693, and the committed test now
reproduces it at call 56694 in milliseconds.

**Why it survived.** TMU0, the hardclock, is unaffected: its reload stays positive, so
scheduling keeps working perfectly while only the timecounter dies. Every obvious symptom
of a broken timer is absent. It took deliberately comparing the guest's clock against the
host's to see it at all.

**Three findings overturned the original diagnosis, and each one mattered.**

*`TCOR = 0xffffffff` is not required.* The 515.4 s delay comes from the **initial**
`TCNT = 0xffffffff`, the emulator's own reset default. `TCOR = 20833` — the hardclock
value everyone called safe — freezes too at the P4 prescaler, because the step (75757) is
larger than `TCOR`, so one `+= tcor` cannot undo a wrap of that size. The real trigger is
"a guest starts a fast timer without writing TCNT", which is far more reachable than "a
guest programs a maximum-period timer". This also reconciled a panel split: one seat had
assumed P4 and another P16, and each was right about its own configuration.

*The signed comparison is not the bug.* It differs from an unsigned borrow test only at
`step >= 0x80000001`, and the largest step either SH machine can produce is 113636. A fix
that keeps signed detection and repairs only the reload is measurably identical — so no
test row may assert the unsigned rewrite, or it would fail correct code.

*The old code did not implement its own comment.* At `step == cnt + 1` it landed on
`TCOR - 1`, not `TCOR`. The comment said "Set tcnt[i] to tcor[i]". That off-by-one is
present for every `TCOR`; the clamp is what turns it into a freeze for the top slice.

**The arithmetic now is all-unsigned**: borrow, then reload modulo the period. The 64-bit
cast around `TCOR + 1` is load-bearing — computed in `uint32_t`, `TCOR = 0xffffffff` makes
the period 0 and the modulo divides by zero. Modulo rather than a loop, because a loop
does not terminate for `TCOR = 0` or for a 32-bit period of 0.

**The assumption is recorded rather than assumed away.** A period is `TCOR + 1` counts.
There is no SH-4 manual in this source collection, and the only in-tree evidence was the
comment this hunk replaced.

*(#401 corrects the sentence that followed. It read "`TCOR` appears nowhere else, and the
hardclock's 20833 never appears in source at all" — true of the tree being looked at, and
FALSE of the tree this commit shipped, because `regress/diff_sh4_tmu.c` was added by the
same commit and contains both — measured just now, 18 occurrences of `TCOR` and 13 of
`20833`. The intended claim was about other
pre-existing files, and that does hold; but a reader who greps the shipped tree to check
the evidence for the `TCOR+1` assumption is exactly the reader the sentence was for, and
they would find it wrong on the first try.)* **The patch would have deleted the sole evidence for its own
premise**, so `dev_sh4.c` now restates the convention deliberately. A seat also measured
that the assumption is less load-bearing than feared: scored against a `TCOR`-period
oracle, the "delete the clamp and keep `+= tcor`" variant is wrong 416,082 times out of
507,904 — the old code is wrong under *both* conventions, so the assumption decides one
count per period, not who is right.

**Interrupt accounting is UNCHANGED, not corrected.** A call spanning several periods
still counts one pending interrupt, exactly as before. Measured, it never regresses
relative to the old code — identical wherever more than one underflow occurs, and exactly
right wherever at most one does. Whether the emulator should queue N or coalesce is a
separate design question this source cannot settle, so it is filed.

**The test compiles the shipped function.** `regress/diff_sh4_tmu.c` stubs `fatal()` and
`#include`s `dev_sh4.c`; `sh4_timer_tick()` is `static`, so there is no way to link it
without including the file — which is exactly what makes the `diff_ieee_store.c` vacuity
(transcribing both sides and never linking the code under test) structurally impossible
here. Eleven rows, all exact values.

**One row exists because two wrong variants survived everything else.** `tcor[0]` written
where `tcor[i]` is meant, and `cnt` read from `tcnt[0]`, are bit-identical to correct code
across all 824,288 single-timer cases — because every other row starts timer 0 only. They
are precisely the typo this rewrite newly risks, since it introduced two locals and four
`[i]` subscripts where the old code indexed inline, and a 9.5-minute live boot catches
neither. The three-timer row kills both, and only that row does.

Mutants, each scored by the row that caught it: the entire pre-#400 body (rejected by the
test, not by the compiler — the harness distinguishes those); `tcor[0]` and `tcnt[0]`
(three-timer row); `step < cnt` for `step <= cnt` (the boundary row, which the earlier
design left unguarded); dropping the `-1` from `remaining` (five rows). Dropping the `+1`
from the period is **detected by SIGFPE rather than by a row**, and is labelled that way:
"a crashing mutant counts as detected" is a vacuity this project tracks in its own right,
and the harness refuses to score a fault as an assertion.

Gate 2 is green at 59 checks.

## One-hundred-and-thirty-ninth round (#399) — four gate scripts did not know which gate they were, and a shipped record repeated one of them

`run.sh`'s `GATES` array and `regress/README.md`'s table agree on the numbering. Four
scripts did not:

```
  gate_mips.sh          calls itself GATE 3   array position 4
  gate_crossfamily.sh   calls itself GATE 4   array position 5
  gate_hygiene.sh       calls itself GATE 5   array position 6
  gate_ab.sh            calls itself GATE 6   array position 7
```

Everything from `gate_upstream.sh` onward is correct, and that is what localises the
cause: `selftest_mutation` was inserted at position 3 and only the scripts between it and
`gate_upstream` were never renumbered. `gate_upstream`'s correct "GATE 8" is also the
proof that the scheme is *meant* to count `selftest_mutation` — without it one could argue
the gate scripts number only themselves and are internally consistent. They are not.

This is not cosmetic, and the evidence is a shipped commit. #395's message and CHANGELOG
both said "gate 5" for `gate_hygiene.sh`, because the number was read out of a comment and
the comment was wrong. The project's standing rule is READ THE LINE BEFORE CITING IT; the
line was read, and **the line itself lied**. A self-label with nothing behind it is a
fact-shaped string.

`run.sh` already refused to run if the array's *size* disagreed with a manifest, on the
principle that "a number nobody checks is not a fact". That proves the battery did not
change size and says nothing about whether the scripts know their own position. It now
also asserts, per gate, that the script's `# GATE n` header equals its 1-based index.

**The named mutant is why the check compares the number rather than looking for a
header.** A check that merely greps for the *existence* of a `# GATE n` line passes on all
four of the wrong files — measured: `grep -c '^# GATE [0-9]'` returns 1 on a
deliberately-mislabelled `gate_hygiene.sh`. A missing header is treated as a failure too,
which is why `selftest_mutation.sh` gained the "GATE 3" label it never had rather than
being exempted. An exemption is a hole.

**One reference was deliberately left wrong-looking, and checking it was the point.**
`gate_arm.sh:27` says "gate 3's mutant machinery … operates on float_emul.c". That is
`selftest_mutation`, which genuinely *is* position 3. A blind renumber would have
corrupted a correct citation — which is precisely the failure this round exists to fix,
committed in the act of fixing it. Sixteen references were changed across four files;
that one was not.

Measured: baseline `run.sh 1` passes the manifest and reports `clean-build: PASS (18
checks)` / `REGRESS_PASS`; relabelling `gate_hygiene` back to "GATE 5" produces
`GATE LABEL MISMATCH: gate_hygiene.sh calls itself GATE 5 but is position 6`, exit 2, and
**refuses before running any gate**; removing its header entirely produces
`GATE LABEL MISSING … (expected 6)`, exit 2. That second mutant is an exact reconstruction
of the tree as it stood before this round.

## One-hundred-and-thirty-eighth round (#398) — the guard I added fired after the thing it was meant to prevent, and withdrawing by deletion was a denial of service

A measure seat replayed gate 1 in a scratch copy and falsified the claim #396 rests on.

**The invariant was false.** #396 said withdraw-then-republish makes "a published binary
exists" mean "the last gate 1 that ran, passed", for every termination route. Measured:
publication sat *between* `verdict=$?` and the stale-verdict guard, so when that guard
fired the binary had **already been published** — exit 1, both copies present and fresh.
A guard that runs after the action it is meant to prevent is a report, not a guard. It is
now above publication, and the detector shows the inversion directly: a red check between
the verdict and the guard now gives exit 1 with **nothing published**, where the same
input under #396 published first.

**Withdrawing by deletion was a denial of service, and #396 introduced it.** A SKIP
destroyed both published copies — and `grep -rn gxsec-build` shows that *nothing in this
repository ever creates* `/tmp/gxsec-build`. So a gate 1 run after a reboot, when WSL's
`/tmp` is empty, wiped the rig's only binary and could not replace it. Withdrawal is now
a rename to `*.withdrawn`: the published *name* still disappears for a failed run, which
is the honesty the round wanted, but the artifact stays recoverable. Measured: SKIP leaves
`/tmp/gxsec-gxemul` absent and `/tmp/gxsec-gxemul.withdrawn` present, on both copies. A
successful publish removes the withdrawn pair rather than leaving a decoy behind.

**`-e` was true for directories.** The allowlist entry check used `-e`, so a reason
wrapping onto a line beginning `devices …` left that row green — vacuous for precisely
the input its own comment claimed it caught. Now `-f`.

**And the comment above it was wrong, in a way worth spelling out.** #396 said that check
enforces the never-wrap rule. It does not, and two seats showed why from opposite
directions. The RED→GREEN wrap requires the continuation's first word to be *a real path
that is already divergent* — it then moves from unexpected to expected and the failure
disappears — and such a path both exists and is in the actual list, so it sails past
**both** new checks. #396's own detector used a continuation beginning `The`, which
cannot suppress anything; it reddened via the stale row. **The detector tested a different
mutant from the one the claim was about.** That is now a standing trap in its own right:
ask not only "did it fail?" but "is what I broke the same thing the claim is about?"

This round's own `-f` mutant makes the same point honestly. It reddens **both** rows —
`no stale allowlist entries` and `every allowlist entry names a real file` — because
`devices` is not in the actual list either, so the stale row was already catching it. So
`-f` fixes a false comment and removes a vacuity; it does **not** add detection power. The
existence row remains subsumed by the stale row. Saying otherwise would be the same
species of overclaim this round exists to correct.

**What is still not guaranteed, stated rather than papered over.** A check appended below
the publish block is invisible: the verdict and the exit status were both decided above
it. The guard narrows the window; it does not close it. The general property cannot be had
inside this script, because publication and adjudication are adjacent and whichever runs
first can be defeated from the other side — which is exactly why four consecutive rounds
of moving one guard produced four orderings, each with a hole somewhere else. The
structural answer is that publication belongs in `run.sh`, conditioned on gate 1's exit
status: **a gate cannot verify its own publication after its own verdict.** Filed, not
attempted here.

Three corrections were also applied to the #396/#397 blocks above: the false invariant;
the `check()` explanation, which was *understated* rather than overstated (it returns 0
unconditionally, so the naive form is permanently green — execution moved that claim in
the opposite direction from two seats' reading); and an unsupported provenance clause that
blamed one specific file's comment for the "gate 5" error when four scripts self-label one
low and which was read first is simply unrecorded. Inventing a plausible causal account of
one's own mistake is still an unsupported claim.

Detector: baseline `PASS (18 checks)`, published, no stale `.withdrawn` surviving; the
SKIP mutant leaving nothing published but the artifact recoverable; the late-check mutant
firing the guard, exiting 1, publishing nothing; the wrapped-`devices` mutant reddening
the real-file row. Restore returns `PASS (18 checks)` and republishes.

**This is the last round on this file.** Four rounds took the check count 14 → 14 → 16 →
18 while the severity of what remained fell, and a review seat asked to rank the project's
work put further hardening here below two emulator defects that a single first-pass audit
of the device layer had already found. What is left in `gate_build.sh` is filed.

## One-hundred-and-thirty-seventh round (#397) — a failed `cd` made the gate report PASS having built nothing

`build_tree` ends with

```sh
    cd "$tree" || return 1
```

and both call sites discarded that status. There is no `set -e`. So a failed `cd`
returns **before any `check()` runs**: the five build-result rows for that tree never
execute, never touch `_fails`, `gate_end` returns 0, and the gate reports PASS having
built nothing. If a stale executable is still sitting in the tree, #396's publish block
then hands it to the rigs under that green verdict.

That makes this the most dangerous of the three publication defects, and the reason is
worth stating plainly: #395's defect published under a visible `FAIL`, and #396's
reopened it under a `FAIL` as well. **This one is green.** Nothing in the output invites
a second look.

Six panel seats found it independently while reviewing #394/#395, and none of them could
run it — it is a code-reading finding that the round then measured.

The fix captures each return on the same line as its call:

```sh
build_tree pmax "$EST" "$PMAX_TREE" 223; rc_pmax=$?
build_tree arc  "$SEC" "$ARC_TREE"  224; rc_arc=$?
check "pmax: build_tree ran to completion" "$rc_pmax" "0"
check "arc: build_tree ran to completion"  "$rc_arc"  "0"
```

The same-line capture is load-bearing rather than stylistic: `check()` is itself a
command, so reading `$?` after the first `check` would report *that check's* status and — #398: **understated.** `check()` returns 0 *unconditionally* (`lib.sh:46` ends the
ok branch in `printf`; `lib.sh:49` ends the FAIL branch in the assignment
`_fails=$((_fails+1))`), so the naive form is not merely mismeasuring, it is permanently
green. Demonstrated: that form with arc's `cd` broken gives `PASS (13 checks)`, exit 0,
and publishes the *previous* run's binary. Two seats called this claim overstated from
reading alone; execution moved it the other way. What follows below is therefore weaker
than the truth, and is left in place so the correction is legible:
not
not `build_tree`'s — a version that looks equivalent and silently measures the wrong
thing.

**Detector.** The mutant forces `cd` to fail, and each call site is broken in turn,
because guarding only one passes any test that only breaks the other. Measured: baseline
`PASS (18 checks)` with both new rows green and the binary published; breaking pmax gives
`FAIL pmax: build_tree ran to completion got=1 want=0`, exit 1, nothing published;
breaking arc gives the arc row specifically; restore returns `PASS (18 checks)` and
republishes.

The corroborating detail is the check count. Both mutant runs report `1 of 13 checks`
rather than 1 of 18 — five rows genuinely vanish, which is the mechanism itself showing
up in the arithmetic. Before this round those thirteen would all have been green and the
verdict would have been PASS. Each mutant also stayed localised: breaking pmax left
`arc: objects built 224` intact, and breaking arc left `pmax: objects built 223`, so
neither failure is a general collapse of the gate.

**How this was found is the part worth keeping.** It was listed as the headline item of
the follow-up round and then not implemented in it. #396's commit message does not claim
it — the record stayed honest — but the round was closed in my head while one of its own
named items was outstanding. What caught it was re-reading the shipped diff against the
task's own fix list rather than against my memory of what the round was about. "It is not
in the message" and "it is done" are different statements, and only one of them was true.

## One-hundred-and-thirty-sixth round (#396) — the guard I shipped had the right quantity at the wrong time, and nine of my own claims were too strong

An eight-seat panel reviewed the shipped #394/#395 diff. Six seats answered (Kimi 403,
Fable quota-dead — both recorded as seat failures, never as agreement), plus a
compile-and-measure seat and a records seat standing in for Fable. They found defects in
both commits and in the prose describing them.

**The guard was positional, not semantic.** #395 replaced `[ -x "$ARC_TREE/gxemul" ]`
with `[ "$_fails" != 0 ]`. That reads the right quantity at the wrong moment. A seat
replaying the gate measured the consequence: append one failing `check` after the `fi`
and you get `clean-build: FAIL (1 of 15 checks)`, exit 1, **and the binary published**.
The defect #395 existed to close reopens completely, one line lower, the first time
anyone extends this gate. #395's own comment asserted "every check has already run by
this point" — true of the file that day, and not a property anything enforced.

Publication now keys off `gate_end`'s **return value**. `gate_end` is what decides
PASS/FAIL, so nothing can be appended between the decision and the action.

The seat also named the mutant a careful reviewer would write: "harden" `$_fails` to
`${_fails:-0}` for consistency with `lib.sh:102`. Measured — when unset that takes the
**publish** branch. Defaulting an unknown state to "publish" is exactly backwards for a
guard whose entire job is to withhold.

**Withdrawal moved to the top of the gate.** #395 removed the stale copies only on the
failing branch, so every route that never *reached* that block left them in place:
`need_file`'s SKIP (exit 77), a signal, a `set -u` abort, a death inside `make`. That is
not hypothetical — `$ARC_TREE` is `/tmp/gxsec-build`, in WSL's `/tmp`, which is cleared
on reboot, while `$RIG/gxsec-gxemul` survives, so the first gate 1 after a reboot takes
exactly that path. Withdraw-then-republish makes "a published binary exists" mean "the
last gate 1 that ran, passed" for every termination route.

**That claim is false, and #398 corrects it.** A seat measured the counter-case:
publication sat *between* `verdict=$?` and the stale-verdict guard, so when the guard
fired the binary had already been published — exit 1 with both copies present and fresh.
#398 moves the guard above publication, which buys the narrow property (nothing is
published unless `gate_end` returned 0) but not the general one.

**The mirror hazard, made loud rather than denied.** Moving `gate_end` earlier fixes one
ordering and opens its opposite: a check appended *below* it would now be ignored
entirely, since both the printed verdict and the exit status were already decided.
Neither ordering is structurally immune — publication and adjudication are adjacent
operations, and whichever runs first can be defeated from the other side. Rather than
assert an ordering guarantee that nothing enforces (which is precisely the claim #395
shipped and this round is correcting), the code captures `_fails` at the verdict and
fails loudly if it moved. Measured: the appended check prints `FAIL`, then
`*** A CHECK RAN AFTER gate_end: the verdict printed above is STALE (_fails was 0 at the
verdict, 1 now)`, and the gate exits 1 instead of 0.

**Two assertions #394 should have shipped.** Only `comm -23` was computed —
actual-minus-expected — so an entry that is allowlisted but *no longer divergent* could
never fail. Measured: normalise `disk/diskimage.c`, which is literally what its own
reason instructs, keep the entry, and the gate still reported `PASS (14 checks)`. A
silently stale exemption is the exact defect #394 claimed to be fixing, so #394 shipped
without the assertion that would have proved its own point. `comm -13` now covers it.

The second is subtler. The parser takes each line's first whitespace field, so any stray
line becomes an entry — and the realistic instance is not exotic: **a reason wrapped onto
a second line donates that line's first word.** Measured, that took a genuine divergence
from RED to GREEN. The reasons run 100–300 characters in a file wrapped at about 90
columns, so wrapping one is an ordinary edit. Every parsed entry must now name a file
that exists in at least one tree, which makes prose fail loudly: `The` is not a file.

**Three allowlist reasons were false**, which is worse than no reason — an exemption that
*looks* justified. `machines/machine_arc.c` is not wholly conditional (7 hunks, +33/−5;
the ne2000 `device_add` at `:209-212` is unconditional inside `machine_arc_init`; only
`:140-141` is PICA-gated). `promemul/arcbios.c` is not wholly `MACHINE_ARC`-gated
(`CHECK_ALLOCATION(boot_string)` at `arcbios.c:2654` sits outside that test). And the
`#257` tag named the wrong change entirely: `#257` is the R4030 interval-timer rate
(`CHANGELOG.md:726`), present in **both** trees and therefore not a divergence at all;
the real one is the arc-only `EXT_IMASK` IP3/IP4/IP6 split described at `:653-656`, which
belongs to the #251/#252 round and carries no number of its own.

**Nine record corrections** were applied to the #394/#395 blocks above, and they are worth
listing because most were mine and several were flattering:

* "published the binary four lines later" — **measured distance is 14**, and the block's
  own quoted `1 of 14 checks` refutes it: if all fourteen rows printed, the publish line
  cannot be four lines after the first failure. The phrase had shipped in four places.
* "every downstream gate ... was measuring" — only `gate_mips.sh:30` consumes the arc
  copy. Eleven gates consume the *pmax* binary, which this change still never withholds.
* "no gate-1 log persists on disk" — `$LOGDIR/build_{pmax,arc}.log`,
  `divergent_{actual,expected,unexpected}.txt` and `unsynced_*.txt` are all written. What
  is missing is a persisted combined **verdict**, which is a narrower and truer claim.
* "SEC's committed generated file ... was never hand-edited" — does not follow. Byte
  equality against the regenerated output proves the committed bytes match what the
  generator emits *today*; it says nothing about their history. This was the round's own
  self-congratulatory line and it was the weakest one in it.
* "gate 5" for `gate_hygiene.sh` — it is **gate 6**. (#398: the correction is right,
  but the *provenance* given here was not checked — `gate_hygiene.sh`'s own header also
  says "GATE 5", so blaming one specific file's comment was an invented causal story.
  Four scripts self-label one low; which one was read first is unrecorded.) It was read from
  `gate_mips.sh`'s own comment, and that comment is wrong: four scripts self-label one
  low. A new variant of this project's standing trap — the rule is *read the line before
  citing it*, and the line was read; the line itself was false. Filed separately.
* Plus: "a mid-string entry is the only safe target" (the others need quote-aware editing,
  not impossibility), "gate 1 calls make so it only runs under WSL" (true of this host's
  toolchain, not of the code), "can never be resolved" (holds under the current
  generator), and `selftest_mutation_295.sh:51-52` cited as precedent for a producer
  deleting its output when it is a consumer-side freshness check.

Also: `cp -f`'s status is now checked, so "published" is no longer printed when the copy
did not land.

The detector runs the baseline plus four mutants and requires each to die for its **own**
reason — a mutant that goes red for the wrong reason proves nothing. Measured: baseline
`PASS (16 checks)` and published; the stale entry killed by `FAIL no stale allowlist
entries got=1 want=0`; the wrapped reason killed by `ALLOWLIST ENTRY IS NOT A FILE IN
EITHER TREE: 'The'`; the late check producing the stale-verdict message and exit 1; and
the SKIP route leaving no published binary in either location.

The first attempt at that last mutant appended the check to the end of the file — after
`exit "$verdict"` — so it never executed, and the guard "failed" because the mutant was
dead code. The rule that every reproduction must answer *"did it fail for the reason under
test?"* is what caught it; without it this round would have "fixed" a guard that was never
exercised.

## One-hundred-and-thirty-fifth round (#395) — the gate reported FAIL and published the binary anyway

Gate 1 ended with:

```sh
# Publish the arc binary where the rigs expect it, but only if it really built.
if [ -x "$ARC_TREE/gxemul" ]; then
```

That comment was true of the *file* and false of the *verdict*. `[ -x ]` asks whether a
binary exists, never whether the gate passed. Measured on 2026-08-13, in a real run:

```
  FAIL no divergence outside the documented set             got=2 want=0
  --   arc binary published to rig and /tmp/gxsec-gxemul
clean-build: FAIL (1 of 14 checks)
```

The publish line sits *between* the failure and the verdict. Only `gate_mips.sh:30`
actually consumes that copy -- the count was overstated when first written -- but it
was measuring a binary handed over by a failing gate — the
silent-false-pass class this harness ranks first.

The guard now tests `_fails`, the harness's own accounting (`lib.sh:33`, reset per gate
at `:36`, incremented by `check()` at `:49` and `check_min()` at `:60`, read by
`gate_end()` at `:76`); `gate_build.sh` sources `lib.sh` into the same shell, so it is
live at the publish site, and every check in the gate has already run by then. That last
detail is the whole design: **the failure that triggered this was the divergence check**,
and a guard scoped to the arc build's own health would have sailed straight past it.

On failure the stale copies are **removed** rather than left. Leaving them is the worse
lie — downstream gates would go green against a binary that is not the code under test,
which is the same "build-tree residue is not evidence" trap that cost four rounds of #88.
Removing them makes the downstream `need_exec` preflights SKIP loudly. Precedent for
preferring a loud stop over a quiet stale pass: `gate_offline.sh:87-95` ("THE HONESTY
LINK") and `selftest_mutation_295.sh:51-52`.

**The detector, and why its injection is orthogonal.** An entry was dropped from the
`DIVERGENT` allowlist so the *divergence* check fails while both builds stay clean.
Measured: gate exits non-zero, `FAIL no divergence outside the documented set got=1
want=0`, **pmax 223 objects and arc 224 objects still built clean**, no publish line, and
both `/tmp/gxsec-gxemul` and the rig copy gone. Restored, the gate returns
`clean-build: PASS (14 checks)` and republishes the identical binary (`09839152a2b1`
before and after). The 223/224 assertion is not decoration: it is what proves the gate
went red for a reason outside the build, which is the only configuration that
distinguishes a whole-gate guard from a build-scoped one — the first mutant a reviewer
would plausibly write.

Writing the detector cost three false starts, all of the same family and all recorded
because each would have read as a pass:
- it first ran under **git-bash**, where `/tmp` is not WSL's `/tmp`. Gate 1 calls
  `make -j12`, and on this host that means WSL, so the git-bash view reported the published
  binary as `MISSING` — which looks exactly like "the guard already works".
- `git checkout -- <file>` restores from the **index**, and the guard was unstaged, so
  the restore step would have silently wiped the change under test.
- the injection first targeted `devices/dev_jazz.c`, which is the first allowlist entry
  and shares its line with `DIVERGENT="`, so `^devices/dev_jazz` matched nothing.
  `devices/autodev.c` is unusable for the opposite reason — it is last and carries the
  closing quote. A mid-string entry is the safe target for a naive line-delete;
  the other two need quote-aware editing rather than being impossible.

## Not changed, assessed (`gate_mips.sh:78-79`)

The sibling sweep found one other unconditional publish: `gate_mips.sh` copies the raw
pty logs to `$LOGDIR` whether or not the gate passed. **Deliberately left alone.** The
binary and the log are not the same kind of artifact — a binary is *tested with*, so
publishing a bad one poisons every later stage, while a log is *evidence*, and
suppressing it on failure destroys the diagnosis exactly when it is needed. Its own
comment already explains why it copies rather than leaving the file in `/tmp`.

There *is* a real hazard there, but it is a different one: a partial log from a failed
run could be graded as complete. The fix for that is for gate 6 (`gate_hygiene.sh`; its own header
mis-labels it 5) to know its input came
from a failed run, not for gate 4 to withhold it — and that belongs with the existing
record that `gate_hygiene` accepts published logs as proof the MIPS gate ran. Filed, not
folded, because a mechanical "apply the same fix to the sibling" would have deleted
evidence.

## One-hundred-and-thirty-fourth round (#394) — the divergence allowlist said which files may differ, never why

Gate 1 asserts that `est/` and `GXEMUL-SEC/` agree outside a fixed list of files. Run
alone, serially, it was **red**, and had been:

```
  --   UNEXPECTED divergence (likely an un-propagated correction):
         cpus/tmp_mips_loadstore_multi.c
         devices/autodev.c
  FAIL no divergence outside the documented set             got=2 want=0
```

The build itself was clean — pmax 223 objects, arc 224, zero warnings, zero errors —
so the red was purely the divergence check. The two files needed **opposite**
dispositions, and blanket-allowlisting both (the obvious move) would have silenced a
real staleness.

`devices/autodev.c` is generated by `makeautodev.sh:56-64,81-90`, which globs the
device directory and emits an entry per `DEVINIT()` it greps out. `dev_ne2000.c` is
the only device file SEC has and est lacks — confirmed with `comm -13` — and the
diff is exactly its declaration plus its `device_register()` call. Every other
generator input is byte-identical. So the divergence is a mechanical consequence of
the differing device sets and, under the current generator, cannot be resolved
while the trees differ. That is
proof from the generator, not inference, and it is the one that belongs on the list.

`cpus/tmp_mips_loadstore_multi.c` was the opposite: stale generated output. Its
generator source is byte-identical in both trees and both already carry #388's
fold-fire code, so the correction *did* propagate — only est's derived artifact was
never regenerated. SEC's own history records the identical failure a day earlier
(generator patched in `792fea0`, tracked output left stale until `078f88e`); that fix
was SEC-only and est is not a git repo, so it never reached est. **Regenerated in est
rather than allowlisted.** That work is not in this diff, because est is not tracked.

Regenerating instead of copying paid a dividend worth more than the fix. est's
generator was recompiled fresh, run to a temp file, and `cmp`'d against SEC *before*
anything was installed — and the bytes matched exactly. That proves SEC's committed
generated file matches what its generator emits TODAY. (It does not prove the file
was never hand-edited at some point in its history -- byte equality is a statement
about the current bytes, not about their provenance.) Nothing in
this harness checks that invariant; a `cp SEC est` would have fixed the symptom and
proved neither half. It also avoided a trap: est's `generate_mips_loadstore_multi`
**binary** is dated 2026-06-26, older than its own `.c` source, so re-invoking it in
place would have silently reproduced the old output.

The change here is that every allowlist entry now carries its reason, and the
comparison takes only the first whitespace-separated field. An unexplained exemption
is how a real divergence gets silenced: the list recorded *which* files may differ but
never *why*, so a legitimate entry and a stale one were indistinguishable. Writing the
reasons down immediately found one that cannot justify itself — `disk/diskimage.c`,
whose entire diff is trailing whitespace on one blank line, traced by `git blame` to
the root import `39748e3`, with the actual #115 correction beneath it byte-identical
in both trees. It is harmless today and is labelled SUSPECT rather than quietly kept,
because a filename-only list cannot tell it from a future real divergence.

The reason field is prose, not structure, and that is deliberate: `awk '{print $1}'`
is the whole parser. Reverting it fails in the safe direction — the expected list
would then hold full lines with prose, which can never match a bare filename from
`list_diffs`, so every real divergence would be reported as unexpected and the gate
would go loudly red rather than quietly green.

Measured, not argued: the allowlist parses to exactly 7 names, `list_diffs` reports
exactly those 7 files, 0 fall outside the set, and **dropping `autodev.c` from the
list turns the row red** — so the row is not vacuous. The floor assertion is kept
alongside the ceiling; an empty comparison means the check broke, which is precisely
how an earlier version of it passed while measuring nothing.

Not fixed here, and filed instead: gate 1 still publishes the arc binary without
checking that the gate passed (the same run that produced the red above printed
`arc binary published to rig and /tmp/gxsec-gxemul` before the verdict); no gate-1 log
persists on disk, so the last verdict was unrecoverable; est's stale generator binary
is still present; and round #393 shipped with no CHANGELOG block at all.

## One-hundred-and-thirty-second round (#392) — the readiness predicate matched the same prompt twice

Fourteen sites across eight probes decided "the command's response is complete" with

```python
if buf.rstrip().endswith(">"):
```

over the WHOLE accumulated buffer. Two independent defects live in that one line, and
fixing either alone leaves the probe broken — which is the part that took measuring to
learn.

**Measured first, on `m88k_rounding_probe` — four arms, only the reader width and the
predicate differing.** The 1-byte reader evaluates the predicate at every byte boundary,
which converts a scheduler race into a certainty; it invents no failure the committed code
cannot have, it removes the luck that usually hides it.

| arm | reader | predicate | result |
|---|---|---|---|
| base | 64 KB | bare `>`, whole buffer (as committed) | 80/80 |
| A | 1 byte | bare `>`, whole buffer (UNCHANGED) | **0/80** — 78 rows `None`, 2 rows WRONG |
| B | 1 byte | full `GXemul>`, whole buffer | **0/80** — identical to A |
| C | 1 byte | full `GXemul>` + fresh mark | **80/80** |

**Arm B is the result that mattered.** Changing the prompt STRING and nothing else helped
not at all. The reason is a detail that is easy to get backwards, so it was proved offline
rather than argued: the prompt is `"GXemul> "` **with a trailing space**. A wait that stops
as soon as it has seen `...GXemul>` leaves that space unread; the next wait's first read
consumes exactly that one byte; and `rstrip()` then DELETES IT AGAIN, so the whole-buffer
predicate matches the SAME prompt a second time and returns having read nothing of the new
reply. `rstrip()` erases the only evidence that the prompt was already consumed. A stricter
prompt string cannot help, because the string it matches is a real prompt — just the wrong
one.

That mechanism is now a committed test, `regress/readiness_predicate_test.py`, which
replays the probes' own `wait()` loop over a scripted byte stream. Pure Python: no emulator,
no pty, no host timing. Its four rows are a truth table, and the second wait reads
1 / 1 / 9 / 53 bytes for bare+whole, full+whole, bare+mark and full+mark respectively —
only the last sees the reply. A readiness test whose verdict moved with host load would
repeat the mistake that once false-FAILed a 45-minute battery.

**Shipped:** all 14 sites take a fresh `mark` before the write, require the full prompt
inside `buf[mark:]`, and require the command's own ECHO in that slice first. The echo is
emitted by the debugger's own read loop (`debugger.c:594`), not by the tty
(`console.c:859-863` clears `ECHO`), so its presence proves the debugger consumed the
command — measured: a command written 0.25 s into a 2,196,367-byte `dump` echoed at offset
2195480, i.e. only when the debugger reached its prompt, never interleaved. The empty
command is guarded, because an empty line is the debugger's repeat-last-command form and
echoes only `\r\n`; no probe sends one today. `send()` now also RETURNS its verdict.

**Four claims made during this round were WRONG and are recorded as such, because three of
them were believed by more than one reviewer:**

- *"`reg` is the only command that reaches a register dump."* **False.**
  `promemul/sh_ipl_g.c:105` dumps registers on any guest exception that is not `TRAPA #0xfc`,
  which fires during `step` on landisk — measured on a committed row. Since #314 makes every
  unimplemented SH encoding raise `EXPEVT_RES_INST`, every such row takes that path. The
  "arms 4 of 14" and "arms 7 of 14" counts are both withdrawn; the honest statement is that
  a `>`-terminated line can come from any command that runs guest code, and from several
  PROM paths.
- *"The two wrong values came from a stale register dump."* **False.** `run_tcnd` sends
  exactly one `reg`, so no earlier dump exists in that session; the only text matching
  `\bpc\s*=\s*0x` is the ECHO of the probe's own `send("pc=0x00010000")`. (Independently
  corroborated: the luna88k `boot` a.out carries no symbol table at all, so no symbol line
  could have supplied it either.)
- *"Requiring the echo therefore cannot be the fix."* **False**, and the correction is
  subtle: once every preceding send waits for its own echo AND prompt, that earlier echo
  necessarily precedes the later mark and cannot enter the slice. The consumer ambiguity is
  defence-in-depth, not a surviving hole; the real residual is an ignored wait failure.
- *"Anchor the consumer on the dump's two-space spelling."* **Would have broken MIPS** — the
  pmax dump prints the pc with no `0x` prefix at all. The portable form is
  `^cpu\d+:\s+pc\s*=\s*(?:0x)?([0-9a-f]+)`.

**Also assessed and REFUTED, recorded so it is not raised again:** a reviewer reported
`_images/openbsd76-landisk-bsd.rd` as a gzip-wrapped ELF that `file.c:307-311` rejects with
`exit(1)`, which would have made both SH probes dead. It IS gzip, but GXemul gunzips it
transparently first — the rejection is unreachable on that path. **And `-A`**, proposed for
all fourteen launch sites to strip colour: measured no-op (zero escape bytes on all five
rigs, and colour is embedded INSIDE the symbol name, so `<sym>` would still end in `>`).
Neither change was made.

**Gates.** `gate_hygiene` gains the positive half of the check — the bare count drops to 0
and three new counts require all fourteen anchored predicates, echo guards and marked sends,
by exact equality, so a single reverted site reddens two rows. `gate_offline` gains the
truth table. The offline test is exempted from the hygiene census (it deliberately contains
the broken spellings) and its own contents are pinned in the same gate, so the exemption
cannot outlive what it exempts. Mutants: reverting one site → bare-row and anchored-row both
FAIL; dropping one echo guard → echo-row FAILs; gutting a truth-table negative arm →
the pin FAILs; unmutated control all green. `gate_hygiene` PASS (45 checks); the converted
`m88k_rounding_probe` scores 80/80 with the committed reader, warn-control 1, warns 0.

**Deliberately NOT in scope, each filed:** the consumer/echo regex ambiguity; the three
halt detectors that compute a whole-buffer flag once and never re-evaluate it (reproduced —
a genuine halt reported "alive" on 2 of 6 runs when `CODE` sits on a symbol); the two
whole-buffer predicates in `arm_flags_probe.py`, which keep a fail-closed allowlist entry
here; and the unrecorded invariant that every probe's `CODE` address is safe only because it
happens to have no symbol, which nothing states or enforces.

**Pass 2 found a hole in the gate this round shipped, and it is the review's sharpest
result.** The new checks catch a REVERT but could not see an ADDITION of the OTHER broken
form. A fresh site spelled `buf.rstrip().endswith("GXemul>")` passed everything: bare was
still 0; the spelling is RECOGNISED, so `unknown` stayed 0; and it is not the anchored form,
so the converted count stayed 14. Yet arm B measured exactly that configuration — full
prompt, whole buffer — failing as completely as the bare one, at 0/80 and byte-identical.

The count is now asserted explicitly at 2. Those two are `arm_flags_probe.py:144` and `:645`,
already filed and deliberately outside this round's scope, so pinning the number turns that
scope decision into a FAIL-CLOSED ALLOWLIST rather than an unstated omission — and it goes to
0 in the commit that converts them. Mutants: adding a third such site reddens the new row
**while bare, unknown and anchored all stay green**, which is the measurement of the hole
rather than an argument for it; converting one of the two reddens it as well, so the allowlist
catches removals and not only additions.

Two smaller pass-2 corrections. The ratchet comment conflated two different failure routes: a
shared helper holding the prompt in a CONSTANT fails the `unknown` check, but a REGEX is not
an `endswith` at all, so `unknown` never moves and it fails the anchored COUNT instead. And
the three positive counts used two different file filters — one comment-stripped, two raw — so
a comment mentioning the echo guard would have inflated one and not the others. Latent, never
fired, fixed before it could.

Seat record for this pass: five live seats answered. The Codex seat FAILED with "Argument
list too long" — the brief inlined a 36 KB diff into argv, over the documented ~32 KB Windows
cap — and was re-fired with a pointer prompt. A dead seat is a seat failure and is never
counted as agreement.

**Pass 2b — the measure-seat found that half of #392 shipped with no detector at all, and
verified the other half end-to-end.**

Two things arrived together. First the verification the round was missing: **all eight
converted probes run green end-to-end** against the committed build, every result and control
line matching its gate's expectation — `MIPS_CVT 11/11` + `CONTROL=OK`, `MIPS_SUBN 9/9`,
`M295 28/28` with both rig controls OK, `SH_ROUND 36/36` + `DISCRIMINATING=9`,
`SH_HALT 26/26` + `CONTROL=OK`, `PPC_HALT 28/28` + `CONTROL=OK`, `PPC_CONV 138/138` +
`CONTROL=OK`, `MODEWRITES_BAD=0`, `MODEREADS=4`. No probe timed out and no rows were lost.
The seat also reproduced arm B independently — on `mips_rounding` and the arc rig, neither of
which this round used — at 0/11 with the control DEAD, confirming that the full prompt over a
whole buffer is no better than a bare `>`.

Then the defect, and it is in the gate this round shipped. `conv_mark` grepped
`'return wait(mark=_mark'` — **a PREFIX**. Deleting `, echo=s if s else None` from all
fourteen sites therefore left every readiness counter byte-identical, and the seat measured
that mutant passing `gate_hygiene`, `gate_offline`, `gate_mips_rounding` and
`gate_sh_rounding` simultaneously. Half the fix shipped with no detector — this project's
worst vacuity class, in a commit whose whole subject was detectors. The grep now anchors
through the comma.

Compounding it: **none of the truth table's four arms tested the echo at all**. They prove the
mark and the prompt string; the echo conjunct had zero behavioural coverage. Two arms are
added for the case only the echo can decide — a PREVIOUS command's prompt arriving *after* the
mark, where byte anchoring cannot help because the stale prompt is genuinely inside the slice.
Measured: without the echo the wait stops after 7 bytes on the stale prompt and never sees the
reply; with it, 60 bytes and the reply arrives. The pin was also grepping raw, so a seat gutted
both negative arms, left the two spellings in a *comment*, and it still read 2 — the comment
filter this file applies sixty lines above was missing from the one check whose job is keeping
an exemption honest.

Three findings recorded rather than changed. **`len(buf) > mark` is a dead conjunct** in all
fourteen sites: `resp = buf[mark:]`, so it is equivalent to `resp != ""`, and the empty string
cannot end with the prompt — brute-forced over all whitespace strings to length 4, none pass.
It matches the ARM house idiom and is harmless, but it does no work. **The empty-command guard
is a dead branch**: 4033 commands were instrumented across all eight probes and none had length
zero, so the repeat-last-command form the round guards against is never used. And
**MAX_CMD_BUFLEN truncation is unreachable** — the longest command measured is 42 characters
against a 71-character cutoff.

A credit the round did not claim: the startup waits were broken too, and this fixed them. On
pmax, landisk and macppc the pre-#392 bare `>` first matched 85–115 bytes *before* the prompt
existed, at the `cpu0: starting at 0x… <sym>` line, and on three of four rigs that `>` is
followed by a real line-flush boundary. The full-prompt anchor closes it: on all four rigs the
full form first becomes true only inside the genuine prompt. luna88k printed no prompt inside
the seat's capture window and remains untested.

Deferred with a task rather than fixed here: a *stalled* echo costs a full wait timeout and,
because `sh_halt_probe.py:318` returns `HOSTEXIT` before it checks `halted` at `:320`, converts
a genuine `HALTED` row into a different wrong verdict while the control stays green — 17 such
rows in the seat's forced-bad-echo run. Today's exposure is zero (293/293 sends verified live),
so it is a latent trap, not a live defect.

**Pass 2c — the pin proved token counts, not arms, and the "fixed" anchor still had a
one-word evasion.** Two seats answered (the three cloud seats were rate-limited, HTTP 429,
not silent — see below).

A seat built the strongest gutting and measured it: replace
`readiness_predicate_test.py` with a script that **computes nothing** and simply prints the
six expected rows, carrying the pinned token counts in a **trailing** comment — which the
gate's filter preserves, because it strips only lines that *begin* with `#`. That fake passed
the pin and every one of gate_offline's six row checks. So the earlier claim that
`gate_offline` made the exemption safe was wrong: the gate extracts self-reported fields, and
a transcript can report anything.

The fix does not try to out-grep the faker. The test now takes a **caller-supplied nonce**,
places it inside the scripted reply, and the reported byte counts shift by exactly its length;
`gate_offline` passes `n$$` and checks the arithmetic. Measured across nonce lengths 0, 5 and
10: `full-mark` is 53 + len and `late-echo` is 60 + len. A hardcoded transcript cannot satisfy
that without running the loops, and it cannot be pre-computed because the nonce differs every
run. Mutant: the real test reports 59 for a 6-character nonce; the fake reports 53 and the
gate reddens.

The second finding is the **third** tightening of one count. `conv_mark` began as
`'return wait(mark=_mark'` — a prefix satisfied by the de-echoed code. Pass 2b anchored it at
`', echo='`, and a seat pointed out that still admits `echo=None`, which passes the argument
and disables the guard in one word. It now anchors the whole conditional. Each round the
surviving prefix was a real substring of *both* the fixed and the broken form, which is
precisely the property a detector must not have. Mutant: rewriting all fourteen sites to
`echo=None` now reddens the row.

Two smaller corrections, both from the same pass: the docstring called mark-plus-prompt "the
shipped form", omitting the echo the round actually ships — two seats flagged it — and the
echo citation pointed at `debugger.c:589` where the character echo is at `:597`.

**Seat record, stated because a rate limit is not a considered non-answer.** Two seats
answered this pass; all three Ollama cloud seats returned HTTP 429 on both panel runs fired
within ten minutes of each other. `panel.sh` now distinguishes the two cases in its summary
and says so out loud, and it derives the seat denominator from the roster instead of the
hardcoded "6" that survived a seventh seat being added — the run that proved Grok working
printed "1/6 … no answer from: … grok".

## One-hundred-and-thirty-first round (#391) — a control that passed on evidence it never received

`arm_endian_probe.py`'s `send()` computed a readiness verdict and **discarded it**, returning
the output slice regardless. On a wait timeout that slice is EMPTY, so the caller's
`"FAILED" in send(...)` test was false, `put_ok` stayed true, `PUT_STATUS=OK` printed, and
gate 14's `endian puts all landed (379)` check asserted OK. The probe's own comment sits
eight lines below the defect and states exactly why that must never happen: a silently
failing `put w` leaves the page cold, routes the transfer through `bdt_*`, and turns DISC
rows architecturally green ON A BUGGY BUILD — "a false pass, the one direction a control
must never allow." The code contradicted its own stated intent. [Pass-2 narrowing: "every
DISC row" was too broad — one invocation affects only its own emulator group, and a code
`put` does not carry the same page-warmth consequence as a warm-page seed.]

The fix keeps `send()`'s return contract intact so every existing caller is unaffected: a
timed-out command is recorded out-of-band in a `timeouts` list, and the put loop fails
`put_ok` if that list grew. A put now counts as landed only if the debugger did not echo
FAILED **and** the command actually completed.

**Measured on both sides, which is the whole argument.** With one `put`'s response forced
never to arrive: the fixed probe reports `PUT_STATUS=FAIL`; the pre-#391 probe, given the
identical fault, reports `PUT_STATUS=OK`. Showing the fix fails proves little on its own —
showing that the old code PASSED on the same input is what demonstrates the defect was real
and silent. Unmutated: 102/102 rows, every control OK. Gate 14: PASS, 352 checks, 0 FAIL,
0 SKIP.

**This round's own brief was wrong on all three of its headline claims, and that is worth
more than the fix.** It asserted a deterministic wrong-value defect across six probes. A
compile-and-measure seat could not confirm any of it:

- **Scope**: ONE probe, not six. Only `arm_flags_probe.py` still has the whole-buffer
  readiness predicate. The other six already use the anchored model — and `arm_idle`'s own
  comment records that as fixed thirty rounds ago. The brief proposed generalising something
  already generalised.
- **Mechanism**: a load-dependent race, not determinism. GXemul always echoes the command,
  and the echo does not contain the prompt. **[Pass-2: the round claimed the echo "flushes
  atomically at the newline". That is FALSE — the debugger's read loop fflushes on EVERY
  iteration, so the echo is flushed ONE CHARACTER AT A TIME, up to N writes. The conclusion
  survives, but it rests on the echo's CONTENT, not its atomicity, and a round whose thesis
  is "do not state a mechanism you did not measure" must not assert the wrong one.]** The stale prompt is only at the tail if the echo is delayed past the 0.4 s
  select — a >400 ms stall, the same load class that already false-FAILs `gate_ab`. The
  brief's reproduction modelled a stream with no command echo, which GXemul cannot emit.
- **Consequence**: truncation, not misattribution — **for the read consumers that were
  actually checked.** Those take their mark immediately before sending and parse only from
  there, so an early return makes the slice SHORT rather than SHIFTED, giving `None` → DEAD
  row → FAIL. The item had been ranked first on a silent-wrong-value claim not reachable in
  those consumers.
  **[RETRACTED IN PASS 2 — MEASURED FALSE. The original brief was RIGHT and this correction
  was WRONG.]** A seat replayed the probe's own reader byte-for-byte against a scripted
  debugger with a virtual clock. With a stall on `step` (or on `pc=`, or on any `print`),
  the result is **misattribution producing WRONG VALUES, not `None`s**: one DEAD row followed
  by four registers each holding the PREVIOUS register's answer — the classic
  off-by-one-command shift. `buf` is shared and each mark is taken before the write, so
  output arriving after a timeout lands in the NEXT command's slice, and `re.search` returns
  the FIRST bare-hex line there.
  **What actually saves the group is not the parser but the VALUE TABLE**: no two adjacent
  rows in any of the 34 groups share an expected value, so every shifted value mismatches and
  the group fails. That is a property of the data, not of the code, and a future row pair
  with equal adjacent expectations would pass silently.
  So the honest record is: an early return CAN yield wrong values; the read parsers are not
  fail-safe; and the setup-command consumers were not either, which is what this round
  repaired. **This block reproduced the trigger and assumed the consequence a SECOND time,
  in the opposite direction — the very error it names.** Three instances in one session.

The method error is specific and worth naming, because it is the second instance in one
session: **the trigger was reproduced and the consequence was assumed.** Proving a predicate
misbehaves says nothing about what the consumer does with the result — that needs its own
measurement, and here it would have shown a fail-safe truncation rather than the silent
corruption claimed. The earlier instance was #390's LDRD reversal, where "the mutant did not
redden the row" became "the defect is not there". Same shape: one inference past the
evidence.

**Residuals, none of them touched here and all now specified.** Anchoring has NO detector —
reverting it passes on a healthy host, so it needs a stall-injection mutant. A bare `wait(15)`
survives outside `send()`. Two `wait_from` results are discarded after `^C`, where three
sibling probes check and kill. Byte-offset anchoring does NOT close the late-`^C`-prompt
hole; requiring the COMMAND ECHO in the slice before accepting a prompt does, is free, and is
strictly stronger than either predicate. `READS_RETRIED == 0` must NOT be asserted — retries
are triggered by host slowness, so that would make the oracle a proxy for load, which is the
`gate_ab` mistake in a new place; fail on reads that never answered instead. And "parse the
last complete response" is wrong for `tlbdump` — though the ROUND'S STATED REASON for that
was itself wrong, and pass 2 corrected it: `ls_general` increments during GUEST EXECUTION,
while interactive debugger commands run with emulation STOPPED, so two correctly
synchronised reads SHOULD agree. Taking only the last is still unsafe, but a disagreement is
a PROTOCOL FAILURE to be reported, not a legitimate monotonic increase to be tolerated. The
conclusion survives; the reasoning behind it did not. Filed, with the
non-ARM readiness sites — 14 of them matching a bare `>` across FOUR non-ARM families (MIPS,
PPC, SH, m88k) that print a `>`-terminated line first in their register dump; ARM is a fifth
family that emits such a line, but its relevant sites no longer use the bare predicate —
recorded as HIGHER severity than this round, because that one needs no unusual host
conditions at all.

**Residuals the round MISSED, added in pass 2:** the unacted `pc=`, `step` and `print`
failures (the fix covers puts only, and those siblings sit one line away); `PUT_STATUS=OK`
when `run()` returns `None`; no committed durable detector for the #391 timeout itself;
continuing a session after synchronisation has been lost rather than aborting; EOF and read
errors being mislabelled as timeouts; and `time.time()` used where a monotonic deadline is
required. The disposition those imply is larger than this round: propagate a structured
completion result rather than a side list, abort on a failed state-changing command instead
of continuing, and add PTY-level fault injection so the detector is real rather than
simulated by string-matching a command.

## One-hundred-and-thirtieth round (#390) — one scratch word, two roles: a PC-relative store's base was four bytes high

`A__NAME_PC` (`cpu_arm_instr_loadstore.c`) handles every load/store whose `Rn` or `Rd` is
the PC. It splits on `#ifdef A__L` — by INSTRUCTION CLASS — while the two uses of the
scratch word `tmp_pc` are distinguished by **ROLE**: the BASE value when `Rn == PC`, and
the DATA value when `Rd == PC` (the "stores store PC+12" quirk the file's own header
documents). The load arm is role-aware, setting `tmp + 8` only when `arg[0]` is the scratch
word. The store arm set `tmp + 12` **unconditionally** — and the decoder points `arg[0]` at
that same word whenever `rn == ARM_PC`, with no reference to the L bit. So the base came
from the data role's value.

`str rX,[pc,#imm]` therefore addressed **four bytes high**. That is not a latitude case:
for the non-writeback OFFSET forms, `Rn == R15` is architecturally DEFINED as the address
of the instruction plus eight — A5.2.2 (`ddi0100i.txt:18700`), A5.2.3 (`:18740`), A5.2.4
(`:18840`), and for mode 3 A5.3.2 (`:19425`) and A5.3.3 (`:19473`). Only the pre-/post-
indexed forms, which would write back to R15, are UNPREDICTABLE (`:18888`, `:18936`,
`:19046`, `:19104`, `:19156`, `:19272`, `:19526`, `:19570`, `:19623`, `:19665`). The
emulator's own decoder already agreed for LOADS: its pc-relative load fold computes
`(addr & 0xfff) + 8`. Nothing rescued stores — that fold requires the L bit.

**The fix is two scratch words, and the one-word version is measurably wrong.** A
role-aware guard on a single word looks sufficient until `str pc,[pc,#imm]`, where `arg[0]`
and `arg[2]` are the SAME pointer: setting it to `+8` for the base silently changes the
STORED word to `+8` too. A2-9 (`:1637-1641`) permits either `+8` or `+12` for a store of
R15 but **forbids using one for some ARM STR/STM instructions and the other for the rest**,
and this fork uses `+12` in both the template and the STM path. So `cpu_arm.h` gains
`tmp_pc_data[2]`, the decoder points `arg[2]` at it at both sites (mode 2 and the mode-3
twin), and the store arm computes both values unconditionally. Separating the roles at
DECODE time removes the need for a pointer-identity test **on the data role** (the load arm
still has one, and it is still sound — `arg[0]` is the scratch word only when `Rn == PC`;
pass-2 narrowed this sentence, which had claimed the test was gone altogether), and the
`[2]` sizing
keeps a doubleword's second-word access inside the scratch instead of landing on
`tmp_branch`, the THUMB branch-prefix register.

**Measured.** RED on the parent `495a07a`, both rigs identical: the value appeared at the
`+12` target and the `+8` target held its sentinel. GREEN after: the reverse. The data role
still stores instruction+12; the both-PC case now puts instruction+12 AT the `+8` target,
which is the combination a blanket `+8` gets wrong. Gate 14: **PASS, 352 checks, 0 FAIL,
0 SKIP**; the endian probe runs **102/102**. Blast radius, with the expected set declared
BEFORE looking: preprocessing all EIGHT generated flavor files old-against-new and
comparing brace-matched function bodies gives **80 changed bodies, all 80 `_pc`, and ZERO
load-named** — exactly the instantiations that compile the edited arm, nothing else.

**Four mutants, all caught, and the pairing is the point.** A blanket `+8`, a deleted data
assignment, and a reverted decoder redirect each redden the both-PC and data rows while
leaving the base rows GREEN (98/102); reverting the base to `+12` reddens the base and
both-PC rows while leaving the data rows GREEN (96/102, which is exactly the pre-fix
parent's own score). The base-role and data-role mutants produce OPPOSITE signatures —
that is what proves the rows separate the two roles rather than merely noticing that
something changed.

**[CORRECTED IN PASS 2 — the paragraph that stood here was WRONG, and its correction is
the most instructive thing in this round. It claimed "LDRD's base was never four bytes
high" and called the LDRD rows "a row whose defect does not exist". Both are false. The
compile-and-measure seat settled it by measuring, and the code as shipped is right — it
fixes MORE than this block originally credited it with.]**

**LDRD's base WAS four bytes high before this round, and this round fixed it.** The reason
the round briefly believed otherwise is a mechanism worth naming, because it is a
defect-hiding surface that will do this again. The general path masks the address with
`addr &= ~(datalen - 1)`, and `datalen` is 8 for LDRD/STRD. The base error is exactly +4.
So `(I+8+off)` and `(I+12+off)` land in the SAME eight-byte block precisely when the
correct address is doubleword-aligned — and A2.8 (`ddi0100i.txt:3031`) makes a
non-doubleword-aligned LDRD/STRD UNPREDICTABLE before ARMv6. **Therefore, on every
architecturally DEFINED mode-3 `Rn == PC` access, the mask always heals the +4 error, and
the defect is observable only where correct behaviour is already UNPREDICTABLE.** That is a
theorem, not an accident of the probe: the round's row used offset `0x40` at the code base,
which is exactly the aligned case. Rows at offset `0x44`, or with the instruction one word
later, show the pre-fix base plainly — measured `0xcccc0003` against the fixed build's
`0xaaaa0001`, on both rigs. The same reasoning covers STRD, whose PC-relative form is a
DEFINED encoding per A5.3.2.

So the dispatch chain was exactly what the three original sources said: `l=0, s=1, h=0`
gives `A__LDRD` with no `A__L`, `A__NAME_PC` takes the `#else` arm, the decoder selects the
populated `_pc` table entry, the general path reads `tmp_pc` as the base — and then the
mask hides the consequence. Nothing upstream supplies the base.

**The four LDRD rows are therefore the ORDINARY vacuity class — a row that cannot detect
its defect — not a row whose defect does not exist.** They stay CTRL, because no DISC row
is available: every layout that defeats the mask is architecturally UNPREDICTABLE, which
the #355 rule forbids asserting on. But the reason recorded against them was wrong, and the
promise that they "will redden if a later round drags LDRD into that path" is provably
false — reverting the base does not move them. That promise is withdrawn.

**The pre-parent methodology was sound; the INFERENCE was the error.** Restoring the three
touched source files into a copy of the build tree does produce a faithful parent binary,
and the one real hazard — stale `src/cpus/*.o` silently yielding the fixed binary — is
excluded by the round's own data, since the STR base rows went RED on that build, which a
stale-object build could not do. The measurement was right; what was drawn from it was not.

**The generalisable lessons, both of which survive intact and one of which is sharpened:**
a mutant that fails to redden a row is evidence about the ROW — that part held, and it is
what exposed the blindness in the first place. But the follow-up inference must be
"therefore this row cannot see its defect", NOT "therefore the defect is not there". The
first is a statement about the instrument; the second is a claim about the world, and it
needs its own measurement. This block made the leap and got it wrong within the same round
that congratulated itself for not making leaps.

**Not touched, each for its own reason** — the `+12` DATA value is correct and locked by
A2-9's consistency rule, but only STR (word) is the IMPLEMENTATION DEFINED case: STRB and
STRBT (`:14342`, `:14415`) and STRH (`:14690`) make `Rd == PC` flatly UNPREDICTABLE, and
STRD makes an odd `Rd` UNDEFINED (`:14503`). Writing "the architecture permits +8 or +12"
across all four would be an overclaim. Also untouched: the writeback forms with `Rn == PC`
(UNPREDICTABLE; their writeback already only clobbers the scratch), the pc-relative load
fold, and the doubleword alignment questions.

**Residuals**: the `A__NAME_PC` header TODO asking whether implementations use pc+8 or
pc+12 for stores is now answerable and answered; the TODO proposing to "separate the two
cases: a load where arg[0] = PC, and the case where arg[2] = PC" is exactly what this round
did. The two `+12` sites — this template and the STM path — must change together or not at
all per A2-9, and nothing in the code said so until now.

## One-hundred-and-twenty-ninth round (#389) — big-endian LDRD/STRD: two 32-bit words, not one 64-bit swap

The template's big-endian LDRD arm was three defects deep (`cpu_arm_instr_loadstore.c`,
the `A__LDRD`/`A__STRD` instantiations): **E1**, a word-pair inversion on BOTH sides — Rd
was sourced from the UPPER word where the architecture pairs Rd with the LOWER address
(A4.1.26: `Rd = Memory[address,4]; R(d+1) = Memory[address+4,4]`; the pair-order sentence
names "the address of the lower of the two words"); **E2**, a carry-corrupting
`data[1] << 6` term — wrong index AND wrong shift, and because the terms are `+`-summed
the bits[7:6] overlap CARRIES: the buggy Rd for memory `11 22 33 44 55 66 77 88` is
`0x55660908`, not even a byte permutation; **E3**, the R(d+1) BE branch was a verbatim
copy of the LE **Rd** expression — `data[0] + (data[1]<<8) + (data[2]<<16) + (data[3]<<24)`,
the LOWER word ascending, not the LE R(d+1) expression [pass-2 correction from a
diff-review seat: the block first said "a copy of the LE expression", which sends a
future reader tracing the copy-paste to the wrong source line; verified against
`f55a8e3:cpu_arm_instr_loadstore.c:262-265`, and it is why the RED r5 read
`0x44332211`]. STRD's only error was E1's store-side mirror (per-word bytes right, the
pair swapped). The LE arms were correct **behaviourally, as measured on this compiler** —
the LE rows are true invariance controls — but not as an ISO C claim: the old LE arms
carried the same uncast `data[n] << 24` this round fixed, so a byte ≥ 0x80 in the
top lane was already shift UB there too [pass-2, a diff-review seat]. Reachability: the decoder dispatches LDRD/STRD with NO version gate
(both rigs are ARMv4 SA1110 where the instructions are architecturally absent — the
emulator executes them regardless, recorded as-is), and both always take the general path
(the fast-path chicken-out is unconditional for `A__LDRD||A__STRD`).

**The fix**: two explicit per-word assemblies on each side, mirroring the word arm —
`(uint32_t)` casts on every shifted term of BOTH branches of the new statements (byte
operands promote to signed int; `0x88 << 24` is shift UB — the casts change definedness
only, declared detector-free by construction). The STRD arm leaves the shared descending
byte walk entirely (`#ifndef A__STRD` around the walk with its `int i` declared inside —
the walk's shared index IS what produced E1, and a dead `|| defined(A__STRD)` disjunct
left behind would be the #372 defect shape, so that guard is reduced to `#ifndef A__H` in
the same edit — **at :310 in the post-change file**; this block first cited `:293`, which
was its pre-change line, moved by this round's own insertions [pass-2; the FOURTH recorded
instance of a numeric site cite going stale in the round that touched it — cite the
CURRENT file]. Byte/halfword/word stores keep the walk byte-identical.
The `~7` alignment mask and the #362-rotate exclusion are untouched, and correct **for the
configurations this fork actually runs** (A2.8: non-doubleword-aligned LDRD/STRD is
UNPREDICTABLE pre-v6; LDRD's pseudocode has no Rotate_Right term). **Narrowed in pass-2:**
"correct" is not an architecture-wide claim. LDRD's own pseudocode (`ddi0100i.txt:8505-8509`)
guards on `(address[1:0] == 0b00) and ((CP15_reg1_Ubit == 1) or (address[2] == 0))`, so
from ARMv6 with the CP15 U bit SET, an address congruent to 4 modulo 8 is a legal
doubleword access — and `~7` would round it down by four bytes. Both ARM rigs here are
pre-v6, so nothing reachable exercises it; the ARMv6/U=1 case is filed as follow-up work
rather than claimed correct. The Time-order note LICENSES the emulator's single 8-byte
access **to RAM** — what the architecture forbids is the 64-bit byte REVERSAL, and an
aligned 8-byte access can never straddle a page. It does NOT license it for MMIO: GXemul
hands one `len=8` call to a single device callback, and a device whose handler serves one
register per access cannot reconstruct the two word transactions the architecture
describes. That path is filed rather than defended [pass-2, a diff-review seat].

**Measured, in order.** RED on the **parent commit `f55a8e3`** (named explicitly in pass-2:
"the committed build" is ambiguous now that this round's own commit is green): `ldrd
r4,[r3]` over seeded `11 22 33 44 55 66 77 88` on `-E barearm` read back
**r4=0x55660908, r5=0x44332211** — the exact predicted buggy values including the carry,
which simultaneously proved the mechanism and pinned **GXemul's decode route** for these
words (`0xE1C340D0`/`0xE1C340F0` — pass-2 narrowing: an execution result proves what the
emulator decodes them AS, not what the architecture says they are; the architectural
encoding rests on the field decode and the manual, and the two agree; a pass-1 seat's claim that these
words are misencoded — an "Rt2 field", bit 22 inverted, L=1 — was refuted by mechanism
first: mode-3 has no Rt2 field, bit 22 = 1 IS the immediate form, LDRD sits in the L=0
half; the RED values settled it empirically). Blast radius proven by `gcc -E` diff of the
`p1_u1_w0` instantiation flavor against the old and new template: exactly FOUR function
bodies changed out of 620 — the LDRD imm/reg and STRD imm/reg instantiations (named
`*_signed_byte_*`/`*_signed_halfword_*` by the generator's raw-field scheme) — nothing
else. **Pass-2 correction — this sentence originally ended "closing the
no-halfword-store-row exposure", which is an overclaim, and a substitute review seat
caught it by grepping for the row rather than trusting the prose:** there is no `strh`
row anywhere in `regress/`, before this round or after it. What the `gcc -E` result
establishes is that this diff provably does not TOUCH the halfword-store path — which is
why the missing row could not hide a #389 regression. It does not create coverage that
never existed. The STRH byte-order gap remains fully open and is now filed. Both trees
rebuilt at zero warnings
(the walk's `int i` scoping kept `gate_build`'s warnings==0 intact). GREEN: **90/90**
endian rows — the BE LDRD pair now equals the already-gated LDM rows' values on identical
memory (an internal-consistency cross-check performed **at development time**; pass-2
narrowing: `gate_arm.sh` adds no assertion comparing the LDRD constants to the LDM
constants, so a future regression that broke one and not the other would not be caught
here — the word "oracle" claimed more than the gate enforces, and promoting the
comparison to a real assertion is filed as follow-up), BE STRD lays `11 22 33 44 55 66 77 88`, all 20
new rows (10 DISC / 10 CTRL) at their derived constants, `ENDIAN_CONTROL_D=OK` (the LE
rows double as fix-state-independent liveness pins — a dead LDRD reads the MOV sentinels,
a dead STRD ladder reads unseeded zero).

**Mutants**: eight executed, each anchored on the NEW code and each built and probed in
its own `/tmp` copy of the build tree (the shared trees are never mutated, so no
`.MUTANT` window exists); **all eight CAUGHT, every one with its sibling arms still
green** — M1 restores the original carry-corrupting `data[1] << 6` line (89/90, only the
BE r4 row red because E3 is not restored with it), M2 is the plausible HALF-fix: it swaps
the two correctly-assembled BE words **in LDRD only**, i.e. E2 and E3 corrected but
**E1's pair inversion left standing** — the exact shape of a fix that notices the carry
bug and the copy-paste but not the pairing (88/90: the two LDRD BE rows; STRD keeps the
round's fix, which is why it is not 80/90 — two seats independently flagged that the
original wording did not say "LDRD only" and a reader could mis-derive the count), M6
puts the BE expression on **both branches of the `Rd` ternary, leaving the `R(d+1)`
statement untouched**, so the LE side breaks instead (89/90 — one row; a cloud seat read
the original "both ternary branches" as both STATEMENTS, derived 88/90, and called the
measurement inconsistent. Refuted by mechanism: the mutant's anchor text
`assert s.count(a)==1` matches only the `Rd` ternary, so exactly one row can redden, and
a second seat derived the same thing independently. The number was right and the sentence
was ambiguous — fixed here), M7 drops the `+1` on the pair write so both halves land on Rd
(86/90 — four rows: the r5 rows of both byte orders keep their sentinel and both r4 rows
take the upper word), M8/M9/M11 are the three distinct STRD-BE corruptions the fix must
exclude — pair inversion, per-word byte reversal, and the full 8-byte reversal (82/90
each), and M12 is an adjacent-index transcription slip inside the NEW LE store arm
(88/90, red on b1/b2 — the LE arm is rewritten code, so it needs its own mutant). M10
(`~7` → `~3`) remains the DECLARED survivor, and the record is stated here rather than
delegated: under the aligned bases the #355 rule requires, `addr & ~7 == addr & ~3 ==
addr`, so no legal row can separate the two masks. [pass-2 correction: this sentence
originally pointed at `OUTSTANDING_BUGS.md:2508-2514`, which contains the writeback-probe
row-omission rationale and says nothing about M10, `~3`, or mutants — a pointer to a
paragraph that does not hold the record is worse than no pointer, so the substance is
inlined. An Opus diff-review seat found it. Note the M10 declaration is itself
architecture-scoped, see the `~7` narrowing above: from ARMv6 with CP15 U set, the two
masks ARE separable, and M10 becomes killable at the same moment the mask becomes a
defect.]

**Gate 14** (`gate_arm.sh`), one clean serial run: **PASS, 340 checks, zero FAIL and zero
SKIP** — the committed 329 plus the ten named discriminator rows plus the
`endian control: ldrd/strd ran (389)` liveness check, with `endian rows run` reading 90.
Each of the ten new names matched exactly one row (`1`, not `2` and not `0`), so neither
half of the padded-column pattern trap is in play.

**Pass-2 review** ran on the committed diff with the records hunks inlined. Seat health
first, since a silent seat is not agreement: Kimi answered 328 bytes (its billing-cycle
403, unchanged) and **the Fable seat is newly quota-dead** — two relaunches failed
identically with a usage limit, which is a quota and not a wedge, so the roster is now six
live seats plus a clearly-labelled substitute carrying the static/records lens. Nobody
found a defect in the shipped code: every seat that derived the byte assembly
independently got the same answer, and the `#ifndef A__STRD` restructuring was confirmed
behaviour-preserving for the other 616 bodies. What the pass DID find was in the evidence
and the prose, which is where the last several rounds' real findings have been.
**Two distinct mutant-coverage gaps, both verified here before acceptance.** First: the
`(uint32_t)` casts have no detector and cannot get one from a value row — the seed's
top-lane bytes are `0x11` and `0x55`, both below 0x80, and even a high-MSB seed would not
catch cast deletion because the UB is benign on this compiler; the only real detector is a
shift-sanitizer build. The round declared the casts "detector-free by construction", which
was honest, but three seats converged on the sanitizer as the way to close it rather than
leave it declared. Second, and sharper: **no LDRD/STRD row is warm.** `seed_bytes` uses
`put b`, which does not warm the translation mapping, and the STRD rows seed nothing at
all, so every one of the ten rows takes the cold general path — which means the
`|| defined(A__STRD)` disjunct in the fast-path chicken-out at `:374-376` has NO detector.
Deleting it is not academic: `A__STRD` is only defined where `A__H` already is (`:53`), and
the fast path's halfword arm writes exactly two bytes (`:496-503`), so a warm-page STRD
would store 2 bytes where 8 are required, and all 90 rows would stay green. Both premises
were checked against the file, not taken on the seat's word.
One seat claim was **refuted**: that M6's measured 89/90 was "factually inconsistent" and
should be 88/90. It assumed the mutant altered both register statements; the mutant's own
anchor matches only the `Rd` ternary. The measurement stands, the sentence was ambiguous,
and the sentence is what changed — a second seat derived the correct reading unprompted.
Everything else the pass produced was a records correction, applied above and tagged in
place: the E3 lineage, the ISO-C status of "LE was correct", the architecture-wide reading
of the `~7` mask, the Time-order licence for MMIO, what the RED values actually prove, the
ambiguous parent-commit reference, the unenforced "oracle", and two numeric site cites
that this round's own insertions had made stale.

**The compile-and-measure seat (Opus) went further than the round did, in both
directions.** It strengthened the central proof: where this round preprocessed ONE flavor
file and reported 4 of 620 bodies changed, that seat preprocessed **all twenty macro sets
across all eight p/u/w flavor files — 160 instantiations, old against new — and got 128
identical, 32 differing, with every one of the 32 being LDRD/STRD imm+reg**. It also
confirmed 620 = 20 × 31 exactly, making the true global blast radius 32 of 4960. Seven
eighths of that proof had been inspection; it is now measurement. (It also caught its own
vacuous green on the way: a first run reported "160 identical, 0 differing" because a
broken `-I` path made both sides fail to preprocess. A comparison of two failed builds is
always "identical" — a new entry for this project's vacuity taxonomy, caught by a
non-emptiness self-check rather than by luck.)

In the other direction it found **the mutant gap that matters most, by compiling it**:
a single mis-transcribed cast — `((int8_t)data[1] << 16)` in place of
`((uint32_t)data[1] << 16)` — is **wrong on 50% of all doublewords and passes every one of
the 90 rows and all eight mutants**. Measured, not argued: identical to the shipped code on
the probe seed, `0x91a2b3c4` versus `0x90a2b3c4` on a high-bit seed, and divergent on
100,000 of 200,000 random doublewords. The mechanism is that the seed
`11 22 33 44 55 66 77 88` contains exactly one byte ≥ 0x80 and it only ever lands where
sign extension is harmless, so no sign-extension defect on `data[0..6]` can move any row.
This **corrects this block's own framing** of the casts: "detector-free by construction" is
true of cast DELETION (whose UB is benign on this compiler, so only a sanitizer sees it)
but NOT of a WRONG cast, which four extra rows on a high-bit seed would kill outright. The
concession was wider than the round realised, and cheaper to close.

Two further honesty points from the same seat, both accepted. First, **this round's
headline is a mental model, not a measured property**: "two 32-bit words, not one 64-bit
swap" describes how to think about the instruction, but for an ALIGNED access the shipped
code and the maligned "one 64-bit value, then split" formulation are the same function —
zero disagreements over 400,000 cases — because they diverge only at unaligned addresses,
exactly the UNPREDICTABLE region this round declined to gate. What was actually fixed is
E1/E2/E3: a wrong permutation and a carry. No row pins "64-bit-swap-ness" and none can.
Second, **"LDRD does not rotate" is asserted in prose and tested by nothing** — the
exclusion is incidental (the guard also requires `A__L`, which LDRD does not define), and
every LDRD row uses an 8-aligned base where the rotate amount is 0 anyway. A plausible
future "improvement" applying the #362 rotation per word would pass all 90 rows and all
eight mutants. Like M10 it cannot be gated with legal bases, so it is DECLARED here as
this round's second by-construction survivor rather than left silent. (Also corrected: the
prohibition on the 64-bit reversal follows from applying Table A2-2 per word, not from the
Time-order note, which licenses only the combining.)

The substitute seat re-derived the four arms and the "4 of 620" arithmetic from the
generator's own enumeration — reaching the same numbers by a different route than the
`gcc -E` runs — and independently reached the same manual citations for the residual
correction above, having read `ddi0100i.txt` rather than taking this block's word for it.
The same seat's naming point was taken too: the #389 liveness check is renamed
`endian control: ldrd/strd ran on the LE rig (389)`, because both of its pins are on
testarm and nothing in it pins BE execution — a fix-state-INDEPENDENT BE pin cannot exist
here, since on BE every LDRD/STRD row changes value with the fix by construction. Worth
recording alongside it, from the confirming gate run: the suite is not blind to a dead BE
rig in general — a separate `endian control: BE rig ran and stored` check already covers
that — so the rename sharpens what this particular pin claims rather than exposing an
unguarded rig.

Its own finding was the halfword-store overclaim corrected earlier in this block: it
checked by GREPPING for the row instead of trusting the prose, found `strh` appears
nowhere in `regress/`, and separated the two claims that had been conflated — that the
diff cannot touch that path (proved) versus that the path is covered (false, and still
false). Filed. It also flagged, correctly, that the records corrections in this block were
sitting uncommitted while `origin/main` still carried the wrong architecture claims; they
ship with this commit.

**Residuals**: the `A__NAME_PC` family (Rn==PC takes the store branch's pc+12; Rd==PC
pair-writes `tmp_pc`'s neighbour `tmp_branch` — THUMB state clobbered by a data access)
consolidated into task #68.
**[CORRECTED the same day, before any follow-up round, by reading the manual this repo
actually has: the clause "all UNPREDICTABLE inputs, #312 latitude rule attached" was
WRONG on both halves and is withdrawn.** For the two OFFSET forms of both addressing
modes, `Rn==R15` is architecturally **DEFINED**, not UNPREDICTABLE, and the value is the
address of the instruction **plus eight** — A5.2.2 (`ddi0100i.txt:18700`), A5.2.4
(`:18840`), A5.3.2 (`:19425`), A5.3.3 (`:19473`); only the pre-/post-indexed forms, which
would write back to R15, are UNPREDICTABLE (A5.3.4 `:19526`, A5.3.5 `:19570`). And
`Rd==R15` for LDRD/STRD is not UNPREDICTABLE either: R15 is odd-numbered, and both
A4.1.26 and A4.1.102 say an odd-numbered `<Rd>` makes the instruction **UNDEFINED** —
a category that requires an exception rather than granting latitude. So #68 is a
defined-behaviour divergence, not a latitude question, and the #312 rule does not apply
to it. The error was mine, introduced in this round's own residual sentence; it is
corrected here rather than silently in a later round.**

The committed "NO LDRD/STRD ROW" comments were narrowed to their actual unaligned/writeback
scope and now cross-reference the new aligned rows — the probe already carried a scar from
exactly this blanket-denial mistake. **Pass-2 correction: there were THREE copies of that
rationale, not two.** The round narrowed `gate_arm.sh` and `arm_writeback_probe.py` and
missed the one in `OUTSTANDING_BUGS.md` — which is the very paragraph this block cited for
M10 — so "the two committed comments narrowed" read as complete while a third still stated
the blanket denial. An Opus diff-review seat found it. All three are narrowed now, and
every line-number cite in them is replaced by the construct's NAME: the numbers have been
wrong at `:226-228`, then at `:338-340` (which this round's own insertions turned into the
middle of the new STRD arm), and a third number would have drifted the same way. The
template's own #357 comment already prescribes exactly this — no line numbers in this file.

## One-hundred-and-twenty-eighth round (#388, phase A) — the MIPS folds get their first witness: 34 variants, none of which any instrument could see fire

The nine MIPS COMBINE sites install 34 fold-handler variants (18 hand-written — five of
them living in the branch-handler block far from the others — plus 16 generated
`multi_{l,s}w_{2..5}_{le,be}`), and until this round NOTHING could witness one firing:
one `debugmsg` in the whole file (the unknown-opcode diagnostic), no counters, no harness
rows. Because most folds are architecturally transparent by construction, any
result-asserting row would pass whether or not the fold fired — the recorded vacuity
mode, now closed the same way m88k's #380 closed it: PULL counters, printed only by
`tlbdump`, zero output on any normal boot.

**What phase A ships** (design converged from a seven-seat pass-1 that materially changed
the brief — the details are the review's findings, not the original design):
- `cpu_mips.h`: `enum mips_fold_id` (34, mechanically verified against the 35 replacement
  sites — strlen's two mode-arms share one id), `enum mips_combine_site` (9), and
  `fold_arm[9]` / `fold_install[34]` / `fold_fire[34]` / `idle_entered[2]` at the very END
  of `struct mips_cpu`, so the hot `fold_fire` writes never share a cache line with the
  dispatch fields in `DYNTRANS_ITC`.
- `fold_arm` counts each COMBINE body ENTERED (before its `n_back` guard) — it separates
  "the opcode never appeared" from "appeared but no arm matched", the two zeros a census
  must not conflate. `fold_install` counts each per-variant replacement assignment — at
  the REPLACEMENT SITES inside the COMBINE bodies, not the decoder arming lines, which
  are unconditional, variant-blind, and re-fire on every re-translation (three seats
  convergent; installing there is the lying-instrument variant of the design). The 16
  multi-width assignments are brace-less if/else pairs, so their bumps are single
  ternary-indexed lines after each pair. Escalation supersedes installed widths before
  they ever dispatch, so **install-without-fire is the NORMAL state for `multi_*_2..4`**
  — recorded here so the census cannot manufacture phantom defects from it.
- `fold_fire` by the control-flow rule (unreachable from every delegating bail, once per
  folded execution, before the first fused effect), with the pinned exceptions: the two
  pmax idles bump immediately before `instr(idle)` (their unconditional lui commit would
  otherwise count every poll — `idle_entered[]` counts dispatches separately);
  `jr_ra_addiu` bumps after its delay-slot guard so the `#228` AdEL path (fused addiu
  already committed) stays counted; `memset` bumps after the page clamp (the clamp still
  folds — fire counts handler COMPLETIONS, one per page chunk).
- The generator emits the 32 generated bodies' bumps itself (`tmp_mips_loadstore_multi.c`
  is regenerated at build time; each build tree asserts the regenerated file carries
  exactly 32 — a stale copy propagated by hand would otherwise report the whole multi
  family as unreached).
- `tlbdump` prints, above its raw/nice split and for every CPU: `MFOLD_START version=1
  n=34`, one row per nonzero fold (`install= fire=`), nonzero `MFOLD_ARM`/`MFOLD_IDLE`
  rows, and ALWAYS `MFOLD_END n=<rows> nonzero=<K>` followed by a flush — absent END
  means DEAD, present END with nonzero=0 means a live all-zero instrument, and the
  START/END counts make a truncated print distinguishable from both.

**Measured this phase:** both build trees compile with the regenerated tmp at exactly 32
emitted bumps; a debugger-only smoke on `-E testmips` prints `MFOLD_START version=1 n=34`
/ `MFOLD_END n=0 nonzero=0` (the all-zero live state, over plain piped stdin — the
debugger needs no pty when no guest console is involved, an operational fact phase B
reuses). And the no-perturbation oracle: one clean serial gate 4 [#388 pass-2
correction: this said "gate 3", but run.sh's selectors are 1-based — gate 3 is
selftest_mutation and `./run.sh 3` would not reproduce the cited run; the boot gate
mips-rigs is gate 4; the 792fea0 commit message carries the same error, immutable] run
on the instrumented
build — **mips-rigs PASS, 6 checks, zero FAIL**, pmax boots OpenBSD 2.2 to `uid=0(root)`
and arc completes 13/13 harness steps to root, byte-for-byte the committed boot
behaviour. The counters are invisible until pulled.

**Phase B, measured.** `regress/mips_fold_probe.py` (new) drives real fold loops
free-running — never `step`, which disables combining — with the breakpoint on a
NON-ARMING instruction after each sequence, and grades the counters as EQUALITIES derived
per row from the read-ahead rule (a breakpoint anywhere disables read-ahead MACHINE-wide,
so fire == passes−1; with none set, folds install during read-ahead and fire == passes).
**All nine checks green at their derived values**: bne_samepage_nop, lui_ori, multi_lw_2
and memset rows across 3max (R3000/MODE32/LE) and testmips (5KE/64-bit/BE, plus
`-C R3000` for the 32-bit-BE cell) — the RUN containing the first big-endian MIPS guest
executions [#388 pass-2 attribution: bne_nop_tm64 precedes the multi rows in probe
order; verified by both re-derivation seats that NO prior BE MIPS guest execution exists
anywhere in the harness — the upstream/asan gates construct testmips but never execute
(dead stdin spins the debugger read loop)] — the multi rows being the first big-endian
MIPS guest
executions in this harness, with two value rows (`0x0badcafe`, sign-extended
`0xffffffffdeadbeef`) witnessing the `_be` generated body's BE32 assembly, not just its
selection [#388 pass-2 x2: the value witness became LOAD-BEARING only after in-loop
poisons were added — without them a fold body that wrote nothing kept pass 1's correct
values and the rows stayed green (measured: the stripped-writes mutant turns all six
value rows red at the surviving poison 0xdead0000); and the sign-extension expectation is
BUILD-dependent, measured — the 64-bit build prints 0xffffffffdeadbeef, the MODE32 builds
print 0xdeadbeef]; memset (1,1) confirming fire counts handler COMPLETIONS [#388 pass-2
correction: overclaim — in that row dispatch==completion==1, so the row cannot make that
discrimination; what (1,1) DOES establish is that the fold collapsed a 64-iteration loop
into one un-clamped chunk (fire is neither passes−1 nor 64), and the bump precedes the
memset() so it counts commitment]. One probe defect was
found and fixed by measurement en route: the debugger's `print <reg>` answers a BARE
`0x%x` line with no name echo (the `name = value` form is the assignment echo) — the
probe's docstring and parse both corrected, the bare-hex idiom the ARM probes already
use. **The non-vacuity mutant**: deleting the bne_samepage_nop replacement sub-arm
(including its install++ — an orphaned increment would NOT actually lie: it reads (1,0),
failing the vector and self-identifying [#388 pass-2 precision]) flips that fold to
(0,0) and reddens its two rows while every OTHER ROW stays green (M388MUT_PASS) — the
per-variant attribution `-J` cannot give. [#388 pass-2 x2: "every sibling sharing the
same COMBINE dispatcher stays green" was the shipped wording and is FALSE as stated — no
green row shares COMBINE(nop) with the mutated arm; the demonstrated isolation is
cross-SITE (the gate header's modest wording was right all along). And "exactly that
fold" overreaches: the deletion also permanently un-installs linux_pmax_idle, whose arm
requires ic[-5].f == instr(bne_samepage_nop) — a fold-feeds-fold coupling recorded as a
census fact for task #69.] **Gate 16**
(`gate_mips_folds.sh`, wired into run.sh) names all nine rows individually plus the
parse-liveness control and the 9/9 total: PASS, 11 checks.

**Phase C re-scoped to its own follow-up** (the fallback this round's design
pre-declared): the census must ctrl-C the out-of-repo pty boot harnesses at the login
prompt, a new scripting surface with real flake risk that does not belong on this
commit's green path. Its zeros, when taken, will be recorded as "unreached under the
committed rigs" with `expected_zero_reason` tags — never as "dead": pmax structurally
cannot reach `b_samepage_daddiu` (64-bit) nor arc the EXC3K-only cache fold, the
`netbsd_*`/`linux_*` names encode guests the committed rigs do not run, and
install-without-fire is the normal state for `multi_*_2..4`.

## One-hundred-and-twenty-seventh round (#387) — #386's pass-2: three wrong swp forms passed all 58 rows, and eight records read wrong

Detector + records only — no emulator code (all seven answering pass-2 seats verified the
shipped `X(swp)` clean against the manual, five of them re-deriving every constant).

**The detector hole (the Opus seat's finding, the fold-marker probe's own three-offsets
rule applied to this rig):** the #386 unaligned rows exercise ONLY offset +1, where three
wrong-but-plausible forms AGREE with the shipped code — a rotate amount of `8*(addr&1)`,
a rotate guard keyed on the raw odd bit, and an alignment mask of `~1` (which at +1 maps
`P+1` to `P`, indistinguishable from `~3`). All three passed the full 58-row set. Closed
with +2-offset groups on both orders (12 rows, every one DISC — the +1 `b2`
by-construction collision does not recur at +2), P+5 seeded `0xAA` so the buggy raw-read
constant does not lean on unseeded-RAM-is-zero, and the three hole-mutants EXECUTED,
each at its predicted count with the +1 rows GREEN (the hole property, confirmed) and
the +2 rows red: amount-`&1` 68/70 (un2 r2 = `0x11223344`, assembled right, unrotated),
raw-odd-guard 68/70, mask-`~1` 58/70 (both un2 groups entirely; the BE sentinel reads
`0x77` — the P+2-shifted write's own bits[15:8] byte landing at P+4). GREEN on the
committed build first: 70/70. The gate's named-row pattern now also pins each row's
KIND (`DISC ... ok`), closing the re-type-a-red-row-as-CTRL vacuity mode the same seat
named; rows 58 → 70, named DISC rows 31 → 43. Gate 14: **PASS, 329 checks** (was 317;
+12 = exactly the new named rows), zero FAIL/SKIP, single clean run.

**The records corrections (each tagged in place):** the #386 pass-1 seat count said
"eight", transcribed from the roster line — the artifacts show SEVEN answering seats
(kimi's 403 quota error is not a seat; the recheck seat's finding, and the commit
message's copy is immutable so the block carries the note); "sentinel stuck at 0x55" →
overwritten to (two seats convergent); "FABRICATED QUOTE" → misattributed from the
sibling handlers' real `word[*]` variable (with the #385 block's copy softened the same
way and its leading "Two" count marked); the mutant parentheticals now name the BE group
(the LE rows differ); the ladders parenthetical scoped to the aligned group; the
loadstore no-writeback citation pointed at the `#357` block comment (`:157`), not the
file "header"; and the stale "two rounds, `swp` first" sequencing pointer annotated
(#386 done; the ldrex-halt half remains).

**Two panel-seat mechanics worth the record:** a seat claimed `LDRB_R7_R0_4 = 0xE5D07004`
is the register-offset form (`ldrb r7,[r0,+r4]`) — REFUTED: the single-data-transfer
I-bit is INVERTED relative to data-processing (bit 25 = 0 IS the immediate form), the
same `0xE5D0` prefix has anchored the committed ladder for months of exact-value rows,
and this round's own sentinel measured exactly `0x99`/`0x55` — values that exist only at
`P+4`. The encoding-trap lesson gains its first refutation pattern. And one cloud seat
died of length (65,536 eval tokens, all thinking, empty response) — a seat-health mode
distinct from the quota death already on the roster.

## One-hundred-and-twenty-sixth round (#386) — a big-endian guest's every swp moved both its words byte-reversed, and an unaligned swp used the raw address

`X(swp)` (cpu_arm_instr.c) assembled the loaded word and emitted the stored word
little-endian UNCONDITIONALLY — no `cpu->byte_order` term on either side — and passed the
raw `Rn` to both `memory_rw` calls with no rotate. Every sibling has been order-aware since
`#372`/`#378`/`#382`/`#383` (ldrex/strex always were), leaving `swp` the last word-sized ARM
memory handler outside the series: on a BE guest every swp byte-reversed the value INTO
`Rd` AND the value INTO memory (the #342/#355 self-contradiction class — an `LDR` of the
same bytes disagreed with what the `SWP` beside it had just read). Unaligned, DDI 0100I
A4.1.108 (U==0) rotates the LOAD right by `8*address[1:0]` and gives BOTH accesses the
ALIGNED word (alignment per LDR on the read, per STR on the write, p. A4-213) — the "third
model" the 2026-08-11 alignment-family entry had already measured crossing a word boundary.

**The fix** mirrors the siblings token-for-token: runtime `cpu->byte_order` branches
(ldrex's assemble, strex's emit), `rot_sh = 8 * (addr & 3)` captured from the RAW address
BEFORE `addr &= ~(uint32_t)3` (the reversed order is the silent trap — a post-mask capture
is always 0 and every aligned row still passes), the rotate applied to the LOAD only and
guarded on `rot_sh` (`<<32` is UB in C), `Rd` written LAST (a data abort on either access
leaves it unchanged — the manual's both-access clause), `swpb` untouched (byte-sized,
order-free; A4.1.109 carries no Alignment note). Masking in place is safe because swp has
no base writeback (the `#357` block comment at `cpu_arm_instr_loadstore.c:157` lists it
[#387 precision: previously cited as the file "header"]). The aligned LE path is
byte-identical to the old code, and the alignment half is inert on aligned addresses (mask
a no-op, rotate skipped) — neither half can regress a currently-correct case.

**Measured, in order.** RED on the committed build: **42/58**, all 16 new DISC rows at
their EXACT predicted buggy values (`0x44332211` aligned; `0x99443322` unaligned on both
orders — the `0x99` sentinel byte visible in the top byte proves the raw `P+1..P+4` read;
ladders `88 77 66 55` [#387 precision: the ALIGNED group's; the unaligned groups' buggy
ladder is `11 88 77 66`]; sentinel overwritten to `0x55` [#387 correction: this said
"stuck at" — the sentinel was SEEDED 0x99 and the buggy shifted write OVERWROTE it]).
Exact-value hits double as the
register-field proof: a dead or wrong-register swp reads 0, matching neither column. GREEN
after the fix: **58/58**. Mutants, each executed, each at its predicted count: LE-revert
**48/58** (`swp be word` red at the buggy column), remove-rotate **56/58** (BE unaligned
r2 = `0x11223344` — assembled right, unrotated; the LE row reads `0x44332211`),
remove-mask **46/58** (BE sentinel = `0x88`, the shifted write's last byte landing at
P+4; the LE sentinel reads `0x55`). Three distinct signatures, both halves' detectors
proven load-bearing. Gate 14 grown 34 → 58 endian rows + 16 named DISC rows: **PASS, 317
checks** (was 301), zero FAIL/SKIP in the log, single clean run with nothing else on the
host.

**Probe design facts worth keeping** (from the pass-1 panel; the first is three seats
convergent): the LE-unaligned rows are ARCH rows, not must-not-move controls — the manual's
rotation is endian-independent, so the fix MOVES them (to `0x11443322`), and a habit-written
LE control would false-red the FIXED build; `swp be unal b2` is arch==buggy BY CONSTRUCTION
for the +1 shift (bits[15:8] of the store value lands at P+2 under both the buggy
shifted-LE write and the fixed BE write, for ANY value), so it is typed CTRL and kept out of
the gate's named-DISC list; and the P+4 sentinel is seeded `0x99`, NOT `0x55`, because the
buggy write's last byte IS `0x55` — a 0x55 seed makes survival and corruption
indistinguishable (the distinguishable-token rule applied at the byte level).

**Panel.** Pass 1: seven seats [#387 correction: this block and the commit message said
"eight", transcribed from the roster line rather than counted — kimi's 328-byte 403
quota error is not an answering seat, and the same commit's #385 entry counted its
identical panel honestly as seven], UNANIMOUS on both claims and on folding the alignment
half in, gated on the RED unaligned reproduction — satisfied above. Two seat claims
settled by mechanism: one "critical compile blocker" (the sketch's BE arm allegedly reads
`word[*]`) was a quote MISATTRIBUTED from the sibling handlers [#387 precision: `word[*]`
is ldrex/strex's real variable ~460 lines away — the seat most plausibly lifted the
sibling's identifiers and presented them as the sketch's text, which uses `d[*]`
throughout (proven from another seat's verbatim echo of the same brief); "fabricated"
overstated the mechanism]; a ladder-base observation (the unaligned witness must re-base
its byte reads at the aligned P, not at `r0 = P+1`) was REAL and adopted.
Pass 2 on the shipped diff follows this commit; its findings, if any, land as the next
round (the #384 precedent).

**Residuals, adjudicated at round end:** (1) `swp`'s `fatal("swp: load/store failed")` on a
legitimate guest data abort is console noise the template's silent return avoids, and the
handler does not reset `next_ic` the way the template's `!cpu->running` arm does — task
filed; the behaviour (return without writing Rd) is otherwise correct. (2)
`cpu_arm_instr_loadstore.c:248-249` lacks the `(uint32_t)` cast on its `<<24` term (formal
UB for byte values ≥ 0x80, benign on real compilers) — RECORDED, not tasked: the effect is
unmeasurable by construction, and a fix whose effect cannot be measured gets documented
instead.

## One-hundred-and-twenty-fifth round (#385) — the records re-audit: no committed expectation was wrong, six records were

Docs and comments only — no emulator code, no probe assertion, no gate expectation changed
(queue task #43). A read-only audit swept OUTSTANDING_BUGS.md, this file, REVIEW_FINDINGS.md
and the probe comments against source ground truth, re-verifying the mechanism once:
`cpu_dyntrans.c:1595-1596` (`host_store[index] = writeflag ? host_page : NULL`),
`memory_rw.c:585-589` (a *data* access passes `ok - 1` as that writeflag), `memory_arm.c:54-60`
(MMU-off translate returns 2, so `ok-1 == 1` for ANY data access — a load warms `host_store`
too; the flag tracks page WRITABILITY, not access direction, so a load leaves `host_store`
NULL only MMU-on on a page mapped read-only).

**Headline: no load-bearing records error.** Every committed `LSGEN` expectation is `1` and
none rests on the audited claims; what the audit found was advisory or reader-misleading.
(The six wrong records of the headline: the probe derivation comment, the #367 block's
claim, the #379 premise, the head index, the TST/TEQ blocker, the memcpy wording. The
REVIEW_FINDINGS freeze — the last bullet below — was deliberate and recorded: under-surfaced,
not wrong, so it is not counted.) Corrected, in rank order:

- **The host_store family's last two live sites** (the #382-established fact, applied):
  `arm_writeback_probe.py`'s derivation comment — "host_store iff the access was a write" →
  set on any data access MMU-off, and the "a cold load-then-store on one page is 2"
  hypothetical → **1** (2 only MMU-on on a read-only page). The `#367` round block below
  carries the same two claims verbatim: annotated `[#382 correction]` in place, not
  rewritten. The `#379` block's "(MMU-on)" reachability premise — retracted by #382 —
  got its forward-marker.
- **The OUTSTANDING open-list head brought current**: an honest status paragraph (the head
  is a 2026-08-01 snapshot that had drifted from its own "resolved are removed" charter),
  a post-2026-08-01 open-residuals block surfacing the four residual families that lived
  only in the dated tail (#364 / #378-latent / #380-#381 / #376-harness — harness tasks
  #42 #22 #59 #60 #61 #55 #56 #57; the fifth tail family, the #382 records sweep, is not
  surfaced as open because this round IS its completion), and the stale "still diverging" sentence
  updated in place (netbsd_idle and netbsd_memcpy were both resolved after it was written).
- **The TST/TEQ-carry entry re-filed**: its recorded blocker — "no positive control that
  the combination occurred exists" — predates #340's two-pass free-running driver and
  #358's fold-fired markers (and #358 measured the bare instruction-counter route the
  entry proposed to be insufficient by itself). Now filed as reproducible-now,
  defect-status UNMEASURED; nothing claims the C-flag divergence is fixed.
- **The memcpy-fold wording made precise**: "a copy whose source has never been stored
  into never folds" → never **warmed by any data access** (MMU-off, a load alone warms
  `host_store`); the "read-only source page is NULL in host_store" remark tagged
  MMU-on-only. The recorded 255/255-genuine measurement is re-filed as **UNRECONCILED**
  (the recheck seat's finding): under the corrected mechanism a fully-cold source should
  self-warm on its first delegated iteration (bail → `bdt_load` → `memory_rw` insert),
  predicting ~1 genuine + 254 folded — re-measurement queued as a follow-up task.
- **REVIEW_FINDINGS.md's freeze banner**: frozen at its final row (#290) per the decision
  recorded in the 2026-08-11 OUTSTANDING entry; the banner states it so the standing
  "row per correction" directive reads against the actual cutoff. The carrier's ethos
  line now says the same (that file lives outside the repo; local-only edit, recorded here).

**Assessed, not changed:** the ~30 ticked/struck head entries stay in place — clutter, not
a trap (a ticked entry cannot be re-worked by mistake), and mass removal was judged too
deletion-risky for a records round; an over-deleted open item is forgotten work. `#366`
keeps its inline-annotation record inside the `#365` block (real commit `0aceec2`; every
citation resolves; only the dedicated block is absent, by the micro-round precedent `#384`
also follows).

**Pass 2 (seven seats, all fixes landed pre-commit):** four seats convergently caught a
five-vs-four residual-family count in this block's own narrative; codex caught the block's
residual restatement of the very claim under correction ("iff the access was a write …
true only MMU-on" — the flag tracks page WRITABILITY, in no mode access direction); the
recheck seat caught the memcpy 255/255 re-endorsement (re-filed UNRECONCILED above) and
flagged that mid-review fixes superseded the inlined diff the seats were briefed on — the
committed version is the post-fix tree. Two seat claims were refuted against the brief
text and source (a fabricated "word[*]" quote; a "wrong filename" that exists and carries
the corrected fact). [#386 correction: the "word[*]" refutation belongs to the CONCURRENT
#29 pass-1 panel, not to this round's pass-2 — only the wrong-filename claim was refuted
here. The conflation itself shipped in this block: records rounds repeat their own error
class even in the paragraph saying so.] [#387: the sentence's leading "Two" therefore
also reads wrong for this round — ONE claim was refuted here; and "fabricated" is
softened to "misattributed": the `word[*]` tokens are ldrex/strex's real variable,
lifted and presented as the brief's text.] A records round catching its own restatement in
pass 2 is now the fifth consecutive instance of the class — the second pass stays
mandatory.

## One-hundred-and-twenty-third round (#382, #383) — a big-endian guest's copyin/copyout folds moved byte-reversed words

> **Correction numbers (#384): the load-bearing swap and its rows are tagged
> `#383` in the source, probe, gate and mutation test; `#382` marks only the
> record/comment corrections carried in the same commit (the
> `(#382 correction:)` lines). Both compile-and-measure seats flagged that the
> original block header said `#382` alone, which broke the grep-either-way
> tag↔CHANGELOG traceability and would have collided with round 124's `#383`.
> Read the bullets below accordingly: `#383` = the swap + probe rows, `#382` =
> the three record corrections.**

The `netbsd_copyin` and `netbsd_copyout` instruction-combiner folds move six
words each between the guest register file and the host page by raw `uint32_t`
access, with no byte-order term — while the single-register load/store template
they delegate to on a decline has assembled per `cpu->byte_order` since `#372`.
So on a big-endian guest the fold and the very handler its own bail-out falls
into disagree: the `#342`/`#355` self-contradiction class, and the divergence
`#354` forbids. Unlike the memset/memcpy folds — closed on big-endian by
`#378`'s install gate — these two are the only folds that gate escapes: their
matchers key on the GENERIC `load/store_w1_word_u1_p0_imm` handler, which
installs for a big-endian guest too, so they install and fire on `-E barearm`.

- **#383 (`cpus/cpu_arm_instr.c`)** — copyin swaps the six words in place
  (its `q32 = &r[6]` IS the destination), BEFORE `#362`'s rotation, because the
  architecture rotates the value assembled in the memory system's order, not
  the raw host word (DDI 0100I p. A4-44). copyout captures the six source words
  first (there `q32` aliases the guest's live `r6..r11`, so an in-place swap
  would corrupt them), swaps, then stores. Both use the open-coded byte-swap
  from `arm_push`/`arm_pop`, not `SWAP32` (which has no other use in `src/cpus`
  and evaluates its argument four times); the copy is textual, which makes a
  grep-audit of the two symmetric — it does not itself *prevent* drift
  (#384 corrected the earlier "cannot drift" over-claim). Two-armed
  `#ifdef HOST_LITTLE_ENDIAN` guards, the `#else` written for symmetry (the
  matchers are `#ifdef HOST_LITTLE_ENDIAN`, so a fold never runs on a
  big-endian host). Honest scope: copyout masks its base to a word
  (`r1 & 0xffc`) with no term for an unaligned base's addr[1:0], so the
  fold-vs-general equivalence for an *unaligned* copyout is unverified —
  correct for STR (aligns / UNPREDICTABLE pre-ARMv6) and NetBSD copyout
  aligns, so likely unreachable, but recorded here as copyin's #362 comment
  records the same for its own path (#384, both compile seats).
- **#383 (`regress/arm_fold_marker_probe.py`)** — `session()` gains a `machine`
  parameter; `barearm` is the big-endian rig `arm_endian_probe.py` uses. Four
  new rows: copyin BE at offsets +0/+1/+3 (the two-pass XOR reused verbatim —
  pass 1 declines and runs the order-aware general handler, pass 2 folds, and
  `r1 == 0` iff they agree), and a copyout BE row that compares the RAW stored
  bytes (never a little-assembled value, which would invert the expectation).
  A `FOLDMARK_CONTROL_BE` liveness pin (`r1 ^ sl` is the architectural word on
  every build) so a dead barearm session cannot false-green the group. The
  seed is laid with `put b` in big-endian byte order, so every expectation
  traces to DDI 0100I Table A2-2 alone. gate 14 fold-marker section 17 → 21.

**The unaligned rows are load-bearing, and a reviewer's sweep first missed
why.** A 4-byte reversal commutes with rotate-by-0 and rotate-by-16, so the
aligned copyin row cannot tell a swap placed BEFORE the rotation from one
placed AFTER; +1 and +3 are the offsets where the two orders diverge. A
compile-and-measure seat's first host-side sweep stepped its test word by
`0x10001`, generating only `XYXY` palindromes — for which the reversal IS a
rotate — and the wrong composition passed with zero mismatches: the same "a
sweep proves nothing about a tail it cannot reach" trap, self-inflicted and
caught. The mutation self-test's third mutant moves the swap AFTER the rotation
and is killed by exactly the +1/+3 rows (measured: m1 flips the three copyin
rows, m2 the copyout row, m3 the two unaligned rows and not +0).

**Both scout premises were confirmed by measurement, and both correct a
record.** The queue said these folds were "latent only behind `is_userpage`
(MMU-on)"; in fact `is_userpage` is set by the LDRT/STRT T-bit alone, MMU-off —
`fire=1 dec=1 inst=1` on the barearm rows measures it. And the "unmasked base
writeback" half of the task is VOID: post-`#357` the template also writes the
unmasked base, so the fold's `r0+24`/`r1+24` agree exactly — nothing witnesses
a divergence because there is none. Recorded as resolved-by-`#357`, not
measured. A third record error is corrected in the same pass: a comment
claiming "a load-only warm-up leaves `host_store` NULL" holds only with the MMU
on and the page read-only; MMU-off (the test rigs) a load sets `host_store`
too, so the store warm-up is the robust choice, not the only working one.

Adjudicated the handler-side swap over an `#378`-style install gate by all
seven answering seats (kimi is quota-dead). The decisive reason is recorded in
its accurate form, not the brief's persuasive one: a gate would leave the
fold's own big-endian code UNINSTALLED on barearm, so its behaviour never
reaches the test surface — the rows would re-exercise `#372`'s already-covered
generic handler. The swap keeps the folds correct AND on the test surface,
adds no dead order-blind body (the debt `#378` already carries twice), and is
twelve moves against `#378`'s generated 9,575-line file.

## One-hundred-and-twenty-first round (#380) — the m88k idle fold ran the bcnd.n delay slot zero times per taken branch

`COMBINE(idle)`'s third arm matches the OpenBSD/luna88k idle loop's
`tb1 / ld / bcnd.n` shape — five copies in the current boot image — but
installed `idle_with_tb1`, the handler written for the **plain**-`bcnd`
sequence. The `.n` delay slot, which the MC88100 executes once per branch
*whether or not it is taken* (UM p. 1-4 §1.2.5, p. 3-26 §3.3.2 — the manual's
own TOC mislabels this section "Shift Circular"; the body heading is
authoritative, a #381-recorded caveat so no future reader "corrects" a
correct cite — and p. 3-35),
therefore ran **zero** times per taken iteration for as long as the guest
idled. On loop exit it ran once — by accident (`next_ic = &ic[3]` happens to
be the slot) — which is exactly why no post-loop witness can see the defect:
every boot marker and exit register reads identical on buggy and fixed
builds. In the shipped image the slot is `or r2,rX,imm`, so the guest-visible
blast radius is a stale `r2` during every idle sleep (visible to trapframes
and in-guest debuggers); but the matcher never inspects the slot, so the same
fold accepts a store, an MMIO access, or a faulting instruction.

- **#380 (`cpus/cpu_m88k_instr.c`)** — a dedicated `idle_with_tb1_n` handler
  that keeps the generated `bcnd_n_eq0` protocol bit-for-bit around the slot
  call: pc moved to the *bcnd* (as the generated handler holds it), a real
  `delay_target` both ways, `TO_BE_DELAYED`, the slot counted even when it
  faults, the exception owning pc/next_ic on `EXCEPTION_IN_DELAY_SLOT`, and
  the taken path assigning the precomputed target rather than re-deriving via
  `SYNCH_PC` (a slot that undefinedly moved `cur_ic_page` — the manual's
  "programming error is not detected" class — would make the re-derivation
  compute a wrong page's address; assignment is immune). The untaken exit now
  runs the slot **inside** delay-slot context, closing the narrower sibling
  defect: the plain path's fault filing coincides with the protocol's for
  DATA_ACCESS, but diverges on the third `m88k_exception` branch's SFIP (the
  arm upstream itself labels "Perhaps something like this could work"), on
  INSTRUCTION_ACCESS's zeroing, and left `delay_target` stale-from-the-last-
  branch — consequence-bearing only jointly with the cleared flag, since no
  exception arm reads `delay_target` when `delay_slot` is `NOT_DELAYED`
  [#381 tightened]. (The commit message additionally listed XIP_E among the
  wrongly-filed state; that was wrong — XIP_E filing is unconditional on
  `delay_slot` and identical old and new. The message is immutable; this
  line is its correction, #381.)
- **#380 (matcher)** — arm 3 requires the slot to be a *real same-page ic*
  (`n_back <= ENTRIES-2`: at the page's last slot the "delay slot" would be
  the `end_of_page` sentinel, which repoints `cur_ic_page` when invoked. The
  bound prevents a desync the NEW handler would otherwise have introduced —
  the old code never called `ic[3]` as a slot, it merely dispatched it as
  `next_ic`, where `end_of_page` runs normally and correctly [#381 reframed
  this from "worse than the elision"]; the declined case falls through to the
  faithful path, which runs the slot natively). Both `tb1`
  arms gain `vector >= M88K_EXCEPTION_USER_TRAPS_START`: `X(tb1)` raises
  PRIVILEGE_VIOLATION in user mode for vectors below 128 and the fast paths
  never called it — an elided check closed by construction (the matched
  images use vector 0xff; zero live installs change). All three idle handlers
  gain a delay-slot entry guard (delegate to the faithful instruction if
  `cpu->delay_slot != NOT_DELAYED`) — assessed unreachable on the image, a
  by-construction guard. The old "we take a chance and hope" NOTE is replaced
  by the honest contract: collapsing the spin still runs the slot **once per
  idle break** rather than once per architectural iteration — exact for an
  idempotent slot whose inputs the loop does not write (the image's `or`,
  whose `r19` is loop-invariant, making the boot A/B a risk control rather
  than a witness), inexact for accumulating, MMIO, order-sensitive or
  polled-state-modifying slots; the same approximation the `ld`/`tb1` arms
  already carry. A matcher gate on the slot's identity is impossible, not
  merely undesirable: `combination_check` runs in the tail of the bcnd's own
  translation and read-ahead walks forward, so the slot is `TO_BE_TRANSLATED`
  at matcher time in *both* modes — an identity test would be dead on every
  first-touch path and unreliable in general (a resume into the slot address
  can pre-translate it before the bcnd re-arms the matcher — #381 softened
  the original "dead always"), which still fully supports the decision.
- **#380 (`cpu_m88k.h`, `cpu_m88k.c`)** — pull-only counters
  (`installs[3]`, `n_taken_plain`, `n_taken_n`, `slot_runs`, `in_delayslot`)
  printed first in `m88k_cpu_tlbdump` (on the test machines every CMMU slot
  is NULL, so the counter line is tlbdump's only output there). The two taken
  counters are deliberately distinct: the mutation self-test reverts arm 3 to
  the plain handler, and a single counter would read the same under mutant
  and fix — the mutant would blind its own diagnostics.
- **#380 (`regress/m88k_idle_probe.py`, gate 11 section 2, +6 checks)** — the
  witness makes the slot a **store** (`st r5,r7,0`) and reads the stored word
  *during* the idle: `taken` (fold path), `takenj` (`-J` reference — the
  faithful path stores on every build), `untaken` (the exit path stores on
  every build, then execution falls into zeroes and aborts — expected noise).
  Placement is load-bearing and derived from the pass-1 panel's false-green
  routes: free-running with no breakpoints (read-ahead installs the fold
  before the first dispatch — with any breakpoint set the first iteration
  runs the real branch and the slot executes once, a silent non-reproduction),
  the spin word inside the code page (a cold page would take the `p==NULL`
  fallback into the faithful sequence), DEST on a different page (a guest
  store to the code page would invalidate the loop's own translations every
  break). All four program words unassemble-verified with registers; the
  arming pattern is written only in masked form (`(iword & 0xffe0ffff) ==
  0xec40fffe` — as a literal word that spells `bcnd.n eq0,r0,-8`, which the
  matcher *rejects*).

**Measured end to end.** Test-first on the committed build: `taken` read the
`0xdeadbeef` seed — the slot demonstrably never ran — while `-J` and the exit
path both stored. Fixed build: 3/3, and the counters pin the semantics:
`installs 0/0/1, n_taken_n 6172, slot_runs 6172` — the taken path entered
6,172 times in the four-second idle window and the slot ran **exactly once
per entry** (the two counts are equal because this probe's loop never exits —
zero untaken entries; on the live rig they differ by exactly the untaken
count [#381 corrected the original "equal by construction"]; pre-fix the slot
count was zero), guard quiet. Mutation proof: arm 3 reverted to the plain handler by
constant (exactly-once anchor), `taken` back to `deadbeef`, references still
green, counters showing the designed signature `installs[2]>=1,
n_taken_plain>=1, n_taken_n==0`.

**The final gate took four runs, and the diagnosis is part of the record.**
`gate_ab` (the luna88k boot — five static copies of the arm-3 shape exist in
the image, and exactly **one** was translated and folded during the boot,
`installs[2] == 1`; the other four are almost certainly install-set copies
never executed [#381 corrected this sentence's original "five sequences now
running the new handler" over-claim]) FAILED **three times** on the `login:`
marker [#381: an earlier draft of this paragraph said "twice" in one place
and "the two red runs" in another while itself describing three failures —
initial, re-run, and post-`pkill` clean-host run]. On the second run the
pre-batch reference binary, which contains no `#380` code, missed the marker
too, which acquitted the fix and indicted the environment; a stray emulator
process was found and killed (`pkill` exit 0), yet the third, clean-host run
still failed on *both* binaries. What settled it was measurement, not theory:
a solo timestamped boot of the `#380` binary reached `login:` at 129.7 s
(budget 300 s) with the fold's counters healthy on the live rig
(`installs 0/0/1, n_taken_n 34415, slot_runs 38063 = 34415 taken + 3648
untaken` — one slot dispatch per entry, and user-mode PATC entries proving
userland up); the gate's *exact* `run_emu` invocation replicated solo scored
1:1:1 with `timeout` reaping the emulator cleanly; and the full gate re-run
(the fourth) under a 10-second process-count watcher **passed 1:1:1 / 1:1:1
(5 checks)** with exactly one emulator alive throughout. Net: three
independent green measurements of the `#380` boot; the three red runs were
transient host conditions — the third measured instance of the `gate_ab`
wall-clock oracle's load-sensitivity class, now the priority argument for the
queued gate-hardening item, which also inherits this round's diagnostic kit
(the marker-timestamp boot script and the process-count watcher). One
self-inflicted lesson kept honestly: the first diagnostic boot passed `-x`,
which routes consoles to X11 windows that do not exist under WSL, so its
marker capture was empty while its counters carried the verdict — boot
diagnostics must not use `-x`.

## One-hundred-and-twentieth round (#379) — #378's pass-2 review: a false-green route in the new probe, and four record errors

Seven of eight seats answered on `#378`'s committed diff (kimi produced its
fourth consecutive non-answer); all seven returned clean verdicts on the fix
itself — several re-derived the full 34-row table and the flip matrix
independently. What survived adversarial review of a *correct* fix was, again,
its instruments and records:

- **#379 (`regress/arm_endian_probe.py`, `regress/gate_arm.sh`) — the warmth
  false-green.** The ten warm-BE DISC rows depend entirely on `put w` having
  warmed the page, and nothing asserted it: a silently failing `put` (the
  debugger prints `FAILED!` and carries on) would leave the page cold, route
  the transfer through the always-correct `bdt_*`, and turn **every
  discriminating row architecturally green on a buggy build** — a false pass,
  the one direction a control must never allow. The probe now checks every
  `put` echo and emits `PUT_STATUS`; the gate asserts it. Gate 14 goes
  295 → **296 checks, single clean run green**; probe re-measured 34/34 with
  all three controls (`ENDIAN_CONTROL`, `ENDIAN_CONTROL378`, `PUT_STATUS`) OK.
- **#379 (records, five corrections).** (1) `tmp_arm_multi.c` is
  **9,575 lines** (9,056 is its non-blank count) — two seats reported the two
  numbers as a contradiction and `wc -l` settled it; the S1 paragraph now
  carries both. (2) "`== EMUL_LITTLE_ENDIAN` alone matches seven sites" was
  wrong — ten at HEAD, eight at the parent; no counting yields seven; the
  conclusion (single-term anchors are not exactly-once) stands and is
  stronger. (3) "the fast path no bootable guest uses" was loose — `barearm`
  IS a BE guest and is the probe's own rig; the claim is about BE ARM *OS*
  guests. (4) The install-gate comment cited "round-118" for S4 (it is this
  fork's round 119/#378) and under-mentioned the memcpy fold's two *bail-out*
  calls — a second, transitive route into the emitted handler, dead on BE
  only because the matcher declines. (5) `gate_arm.sh`'s endian preamble
  still described `#372`'s six-and-six row world above a 34-row check — the
  narrative is now scoped as `#372` history. The OUTSTANDING latent-defect
  record was rewritten in the same pass: "dead ONLY via the gate" softened to
  name the other suppressors (`HOST_LITTLE_ENDIAN`, statistics, trace mode),
  the one-armed-conjunct idiom note added (the conjunct is correct only under
  the enclosing host guard; the two-armed form is the hardening if that guard
  is ever relaxed), a historical marker added over the entry's discovery-time
  present tense, and a cross-reference to the copyin/copyout item.
- **Queue movement from the same pass:** `netbsd_copyin`/`netbsd_copyout`
  (task #17) re-ranked to the front — both agent seats independently traced
  that their matchers key on the **generic** load/store handlers, which
  install for BE guests too, so `#378`'s install gate does not close them;
  post-#378 they are the largest live ARM-BE divergence, latent only behind
  `is_userpage` (MMU-on). [#382 correction: `is_userpage` is set by the
  LDRT/STRT T-bit alone and is reachable MMU-off — the divergence is NOT gated
  on the MMU being enabled; see the #382 round block.] The LDM-with-PC instrument gap (no probe row loads
  PC through the multi path, so the round's headline severity is source-read,
  not measured) was merged into task #59.

## One-hundred-and-nineteenth round (#378) — a BE guest's every LDM/STM through a warm page was byte-reversed, 23 handlers of it into PC

`generate_arm_multi.c` emits the LDM/STM fast path as raw host-word moves — no
byte-order term anywhere in the generator — while the `bdt_load`/`bdt_store`
fallback (via `arm_pop`/`arm_push`) swaps on both its warm and cold arms. The
dispatcher installed the fast path with no `cpu->byte_order` test, so on this
LE host a big-endian guest's multi-transfers to a WARM page moved reversed
words and to a COLD page correct ones — `#372`'s self-contradiction class with
the **polarity inverted** (there the general path was wrong; here the fast
path). Not just data: **23 of the 256 emitted handlers load PC**, so a BE
`ldm {...,pc}` function return jumped to a byte-reversed address. LDM/STM sits
on every prologue/epilogue, making this the largest ARM-BE defect to date.

- **#378 (`cpus/cpu_arm_instr.c`)** — one line: the fast-path install gate now
  also requires `cpu->byte_order == EMUL_LITTLE_ENDIAN`, so a BE guest takes
  the already-correct `bdt_*` everywhere. Resolving the guest term at
  TRANSLATE time is sound because `byte_order` cannot change afterwards, a
  fact three review seats verified independently by exhausting the routes: the
  CP15 c1 B-bit write calls `fatal()` and **exits** (now commented as
  load-bearing in `cpu_arm_coproc.c` — a future endian-switch round needs
  translation-cache invalidation AND re-translation, since instruction decode
  reads `byte_order` too); SETEND is undecoded and `ARM_FLAG_E` inert; every
  host-side write is machine-setup-time. Closing the gate also closes the
  `netbsd_memcpy` fold's raw `pw[]` publishes **for free** — its matcher
  requires the fast-path handler installed, so it declines on BE (the `#354`
  invariant comment is amended to say so) — and disables the order-immune
  memset fold on BE (a performance note, not a correctness change).
- **#378 (`regress/arm_endian_probe.py`, rewritten)** — 12 → 34 rows with
  EXPLICIT per-row kinds: `#372`'s DISC rows are the COLD ones, `#378`'s are
  the WARM ones, and the old "cold in name ⇒ DISC" expression would have
  labelled the new rows backwards. New: warm/cold STM byte-witness ladders,
  warm/cold LDM word rows with zero sentinels, LE invariance mirrors, and a
  second liveness control (`ENDIAN_CONTROL378`: the cold multi rows go through
  `bdt_*` on every build, so they prove the machinery live independent of fix
  state). Grouped spawns; explicit `put` width on every command (`put_type` is
  static and sticky); r10/r11 read as `sl`/`fp` (the debugger has no rN
  spelling for them). All 18 new words unassemble-verified WITH REGISTERS.
- **#378 (`regress/gate_arm.sh`)** — endian section 12 → 34 rows, +11 checks
  (the ten new BE DISC rows named individually + the 378 control). Gate 14
  goes 284 → **295 checks, single clean run green**.

**Adjudicated S3 over S1 by all seven answering seats** (the eighth, kimi,
produced its third consecutive non-answer and is recorded as a seat failure).
S1 — teaching the generator an `arm_push`-style swap — would have kept a BE
fast path *no BE ARM OS guest boots to use* — the barearm rig IS a BE guest
and does exercise LDM/STM; it is the probe's own rig (#379 tightened this
wording) — at the cost of regenerating the 9,575-line (9,056 non-blank; both
counts were reported by seats and settled by measurement, #379)
tracked `tmp_arm_multi.c` across four no-VPATH trees, a coupled same-round fix
to the memcpy fold's publishes, a live runtime branch on the hottest LE path,
and a mutant exposed to the generator-regeneration vacuity trap (the Makefile
dependency is on the generator *binary*; a stale-mtime copy measures the
unmutated build). A pass-1 draft cited the in-tree MIPS multi generator as
precedent for S3; a seat corrected this — the MIPS shape emits `_le`/`_be`
variant bodies and picks at translate time, which is neither S1 nor S3 but a
fourth shape, **S4, and S4 is the recorded design for any future round that
wants a live BE fast path** (it must then also swap the memcpy fold's four
publishes — see the amended `#354` comment).

**Measured end to end.** Test-first on the committed build: exactly 24/34,
the ten warm-BE DISC rows red at precisely their predicted reversed values
(`44 33 22 11 88 77 66 55`; `0x44332211`/`0x88776655`) while both liveness
controls and all cold/LE rows stayed green — the warm/cold differential is
itself the proof the fast path fired. Fixed build: 34/34. Mutation proof
(`/tmp` copy, the full two-line install condition as the exactly-once anchor —
`== EMUL_LITTLE_ENDIAN` alone matches ten sites at HEAD, eight before this
commit (the first draft said seven; no counting gives seven — #379) — reverted
BY CONSTANT to
the pre-fix condition): the exact flip matrix, every DISC row red at its buggy
value, every control green. Pass-1 review also repaired the row design before
anything ran: the `ldrb` witnesses originally read through `r0` while the
transfers based on `r3` (rebased, deleting a MOV), and the `sl`/`fp` naming
and `put_type` stickiness were caught as would-be silent row failures.

## One-hundred-and-eighteenth round (#377) — #376's pass-2 review: one wrong measured fact in three records, and the trunc control's claim made measurable

The eight-seat pass-2 review of `#376`'s committed diff returned clean verdicts
on the code from every answering seat — all independently re-derived the flip
matrix, none found a false-pass path — and one seat found the round's single
real defect **in its records**: the "dump line address is TRUNCATED to 32 bits"
fact, stated as measured-on-both-rigs in the probe comment, the CHANGELOG
incident, and (worst) the `#56` queue entry that offers it as guidance for
future dump parsers. Traced in source: `debugger_cmd_dump` prints `%08x` only
when `c->is_32bit`, and arc's R4000 (ISA III) is 64-bit — so arc renders 16
digits, and the probe passed there only because its regex's `0x[0-9a-f]*`
prefix happens to tolerate both widths. A parser built from the recorded
guidance would break on every 64-bit CPU. All three records corrected; the
probe code needed no change. A wrong measured-fact record is exactly the class
this project's rounds keep getting burned by, and it survived one author pass
plus four clean seat verdicts before the fifth seat traced the flag.

- **#377 (`regress/selftest_mutation_295.sh`)** — a fourth mutant,
  `trunc: IEEE_RM_RZ -> FPU_RM_FROM_FCSR` (the W-format trunc line, unique by
  `COP1_FMT_W` against its single-line L sibling), converting the trunc control
  rows' advertised discrimination — "they kill a trunc revert, which no other
  row would" — from an asserted claim into a measured one. Predicted flips:
  `t35rp` 3 -> 4 (RP ceils the tie), `tn35rm` -3 -> -4 (RM floors it); every
  other row, including all round/ceil/floor discriminators, must stay green.
  Also: the self-test's scratch logs move to a PID-unique directory (stale
  fixed-name logs once confused forensics), fixing two expect() reads that
  still named the old paths.
- **#377 (records)** — the three-place dump-width correction above; the `#55`
  entry's cite corrected to the actual check line (`:167`, fed by the `:154`
  grep — the draft said ":153 area"); the probe/gate "controls cannot flip by
  construction" wording scoped to "under any committed mutant" (the trunc rows
  flipping under the trunc mutant is their job, not a violation).

Measured before commit: the extended self-test's full four-mutant run —
baseline green, exact flip matrix per op, all non-flip rows green each time.
Residual seat suggestions adjudicated and dropped with reasons (nightly
mini-selftest; a gate `tail -1` hardening that is already rig-bound by its grep
pattern) or folded into the comment-only docs task (`float_emul.c` W-guard cite
at the `rbnd` row, a `.s`-by-construction comment at the forced-constant site).

## One-hundred-and-seventeenth round (#376) — #295's fix gets the detector its reverting mutant demanded

`#295` (round 60) made `round.w`/`ceil.w`/`floor.w` force their architectural
rounding modes instead of inheriting FCSR.RM — and shipped with **no committed
detector**. Worse than uncovered: the likeliest wrong edit, copy-pasting `cvt.w`'s
`FPU_RM_FROM_FCSR` back over the forced constant, **equals the correct code
whenever FCSR.RM is 0** (the reset default), and every committed row left FCSR
alone — so the reverting mutant passed the *entire* battery. That is the
taxonomy's sharpest class: a shipped fix whose mutant nothing can see. Pure
instrument round; no emulator change.

- **#376 (`regress/mips_fixedmode_probe.py`, new)** — 14 rows × both rigs, every
  discriminating row under a NON-ZERO FCSR.RM set by guest `ctc1`. Nine
  must-flip rows (5 round incl. the `-2147483648.5` boundary witness, 2 ceil,
  2 floor), five controls (a `cvt.w.d` FCSR-consumer, a `cfc1` readback, two
  trunc-wiring contrasts, a NaN result pin using the tree's legacy-quiet
  encoding `0x7ff7ffffffffffff`). pmax loads doubles as the `$f0/$f1` pair with
  two MIPS-I `lwc1` and reads back via `swc1`, never `sdc1` (#273). Fresh
  emulator per row plus an explicit `$f2` poison from the seeded result slot, so
  a faulting op and a dead store are the same distinguishable token. Output is
  fixed-string `M295_ROW=rig:name RESULT=…` lines — this battery has already
  produced both a double-match and an unsatisfiable row from padded-column
  regexes.
- **#376 (`regress/gate_mips_rounding.sh`)** — section 3: 32 checks (28 rows,
  2 per-rig ctc1-witness controls, 2 totals). Gate 12 goes 21 → 53 checks, all
  green in a single clean run on the committed build.
- **#376 (`regress/selftest_mutation_295.sh`, new)** — the proof the rows are
  not vacuous: a full-build /tmp-copy mutation test (the offline
  `selftest_mutation.sh` compiles only `float_emul.c` by design and can never
  see this decoder wiring). Three per-op mutants, substitution BY CONSTANT with
  exactly-once anchors, a cmp-vs-repo baseline before trusting the copied tree,
  and crash/empty output counted as SETUP_FAIL, never detection. **Measured:
  M295MUT_PASS — the exact flip matrix**, every must-flip row failing with its
  predicted directed-mode value (`round.w(2.7)@RM` 3→2, the boundary row
  `0x80000000`→`0x7fffffff`, …) while every control stays green, three times.

**What the eight-seat panel changed before a line was written.** Two rows of the
round's own one-off probe were **born vacuous against the very mutant they
existed to catch** — `round(2.5)@RM` and `round(-2.5)@RP` give the same answer on
fix and mutant (re-moded to `@RP`/`@RM`, both now flip). The draft acceptance
rule "every committed row must flip" was rejected independently by five seats as
self-contradictory — the controls cannot flip; that is their purpose — and became
the two-tier matrix above. The trunc rows had been labeled "proves the RM write
took effect", which is exactly backwards (trunc is mode-*immune* in every state);
the witness that `ctc1` landed is the `cvt.w.d` row (it consumes FCSR, so a dead
write reads RN's 3 instead of RM's 2) plus the `cfc1` readback, whose `$t0` is
clobbered between write and read so a no-op `cfc1` cannot false-pass. Both-rigs
is recorded as *transport breadth*, not necessity — the constants sit in shared C
below the rigs' convergence (`cop1_slow → coproc_function → fpu_function`, traced
by a seat), and the `.s` spellings reach the same call sites with the same
constants (the fmt field is masked out of the decode switch), so D rows cover the
constant-mutant class by construction; `.l` on arc is queued (#57 in the harness
list). One seat's claim of separate per-format switch arms was refuted from the
decode mask. A non-answering seat (328 bytes) was recorded as a seat failure,
never agreement.

**Two measurement incidents, kept honestly.** (1) The *fifth* hand-assembled
encoding incident: the pinned `cvt.w.d` constant `0x46200024` disassembles as
`cvt.w.d r0,r0` — fd=0, overwriting the operand and never writing `$f2` (COP1
puts func in bits 5:0, fd in 10:6; the right word is `0x462000a4`). A
mnemonic-only unassemble check *blessed the wrong word*; the registers in the
disassembly and the probe's import-time `assert helper==constant` caught it.
(2) The probe's first full run scored 0/28 with every row `got=None` — the dump
parse assumed the requested address appears on the output line, but `dump`
prints the line address ALIGNED DOWN to 16 bytes, with only in-range words
printed (out-of-range slots as blank columns) in MEMORY order. The ctc1-witness
controls reported DEAD on both rigs, which is the control doing its one job:
refusing a dead instrument instead of writing a false verdict. Fixed parse
binds to the aligned line address. [This paragraph originally also claimed the
address is "TRUNCATED to 32 bits" — pmax-only, corrected by #377: the width
follows `c->is_32bit`, and arc's R4000 prints 16 digits.]

Panel pass 1 also surfaced three committed-harness defects, queued as their own
work: `selftest_mutation.sh` counts a *crashing* mutant as detection (exit
status ignored); `mips_rounding_probe.py`'s readback accepts any dump-shaped
line without binding the address; and the arc `.l` coverage gap. The stale
`cpu_mips_coproc.c:1185` comment (it still claims W/L ignore the mode and that
cvt.w/trunc.w are indistinguishable — false since #294) folds into the existing
comment-only docs task rather than forcing a shared-C propagation into this
regress-only round.

## One-hundred-and-sixteenth round (#375) — the mips_loadstore[] index was a silent cross-file coupling; now a checked invariant

The MIPS load/store dispatch table's index is computed one way in a generator and
re-derived by hand at a dozen sites in three other files, with no comment tying
them together and no check that they agree. That is the first non-ARM round, and
it is pure instrument: no emulator change.

- **#375 (`regress/gate_offline.sh`)** — twelve checks asserting the committed
  `mips32_loadstore[32]` and `mips_loadstore[32]` tables resolve their
  load-bearing indices to the handlers the hand-coded sites assume.

**The coupling.** `generate_mips_loadstore.c` emits the 32-entry table in the loop
order `endianness → store → size → signedness`, so an entry's index is
`endianness*16 + store*8 + size*2 + signedness`. `cpu_mips_instr.c` then hard-codes
that arithmetic's *results*: the multi-transfer fold bails to `mips*_loadstore[5]`
(plain `lw`), the coprocessor handlers use `[5]`/`[12]`/`[7]`/`[14]` for
`lwc1`/`swc1`/`ldc1`/`sdc1`, and the `COMBINE(nop)`/`strlen`/`#169` matchers key on
`[4+1]`, `[1]`, `[8]`. Reorder that one generator loop — swap `store` and `size`,
say — and every hand-coded index silently names a different handler: the fold bail
dispatches the wrong access *size*, `ldc1` becomes `lw`, and **nothing fails to
compile**. This is the taxonomy's silent-miscompile class, in a dispatch table.

**Byte rows are load-bearing in the other direction.** A byte access has no
endianness, so the generator makes the byte LE and BE entries the *same* symbol —
`[1]==[17]`, `[8]==[24]`. `#169`'s byte-store guard and the strlen byte-load guard
rely on that share (their `|| [x+16]` terms are deliberate no-ops today). The word
rows `[5]!=[21]` assert the discrimination the byte rows lack; if a generator change
ever split the byte entries, those tautologies would silently go live and the
matchers weaken. Both directions are now pinned.

**Offline and mutation-verified.** The rows read only the committed generated table
— no compiler, no rig, no emulator — so they sit at the top of `gate_offline`,
ahead of the float differential's `gate_skip`. Confirmed they discriminate: on a
copy of the table with index 5 repointed to the BE handler (exactly a loop-reorder's
effect), the `[5]=LE` and `[5]!=[21]` rows both go red. The real table is never
touched. `gate_offline` goes 31 → 43 checks.

**Found by the `#46` MIPS-combiner audit**, whose headline was that the MIPS
multi-transfer folds are *better built* than the ARM ones (byte order consulted, no
partial-commit window, this very index verified correct) — so `#46` is now scoped as
coverage-owed instrumentation, and the audit's live defects (an m88k idle fold that
drops a delay slot; this index coupling) are their own rounds. Both boot rigs are
little-endian, so the `_be` table entries are dead code on the harness today; the
coupling is pinned for whenever BE MIPS work happens. A one-line comment in the
generator naming the four dependent files is a cheap follow-up; the gate rows are the
load-bearing half and need no rebuild.

## One-hundred-and-fifteenth round (#372) — the general-path word STORE ignored byte order, because its arm was dead code

On a big-endian ARM guest, a word `STR` to a cold page wrote the register's
**host** bytes and a word `STR` to a warm page wrote guest order — the same
instruction disagreeing with itself by page residency, the `#342`/`#355` class.
And every `strt`, which is general-path on its first access per page (`#366`),
was reversed. The cause was an arm that had never once executed.

- **#372 (`cpus/cpu_arm_instr_loadstore.c`)** — two edits: the load-only aliasing
  optimisation is now gated on `A__L`, and the dead store wrapper is removed so
  the byte-order-aware walk serves the word store too.

**The arm was UNCONDITIONALLY EMPTY.** Its guard was
`!defined(A__B) && !defined(A__H) && defined(HOST_LITTLE_ENDIAN)` and its only
body was `#ifdef A__STRD` — but `A__STRD` is defined only under `A__H`, which the
guard excludes, so for a plain word `STR` on an LE host the block compiled to
nothing. The store emitted no bytes and `memory_rw` copied the register's host
bytes to guest memory, `cpu->byte_order` never consulted. Deleting the wrapper is
the fix, not cleanup: the wrapper is what emptied the arm.

**Two edits, because the one-line delete is a fresh regression.** In the
`datalen == 4` block, `data` *aliases the source register* on an LE host. Removing
only the wrapper leaves the byte walk running against that alias — and the walk
both reads `reg(ic->arg[2])` and writes `data[i]`, so each byte written corrupts
the value the next read consumes. Traced for BE with `0x11223344`, that produces
`44 33 33 44` — a *third* wrong answer. So the alias is gated on `A__L` (an exact
compile-time load/store discriminator here) and the store gets a real buffer; the
walk then fills it in order and `memory_rw` writes it. This was the scoping seat's
catch, verified before the edit.

**MEASURED, test-first, on `-E barearm`** — whose `MACHINE_SETUP` sets
`EMUL_BIG_ENDIAN` outright, so no config file or ELF is needed. Before the fix, a
cold store of `0x11223344` read back **`0x44332211`** (raw bytes `44 33 22 11`);
after, **`0x11223344`** (`11 22 33 44`). The LE guest is **unchanged** both ways —
on LE the broken code was accidentally right, host order being guest order, which
is exactly why LE could never have surfaced this.

**A new probe, `regress/arm_endian_probe.py`**, runs both byte orders — the first
in the battery to do so. **Five** of its six `be *` rows (barearm) are the
discriminators — the cold-page rows, which enter the buggy general store path; the
sixth, `be warm word`, takes the order-aware fast path and so is green on both
builds — it is the rig control (a pass-2 seat caught the probe mislabelling it DISC;
corrected). Its six `le *` rows (testarm) are **invariance controls**, present only
to catch a fix that repairs BE by breaking LE, which the pre-fix source shows is a
live shape.
The `ldrb` witnesses are the purest form: a byte load has no byte order, so it
reads the raw layout directly, and each buggy value is the exact reverse of its
arch value — the two mirror-image groups cannot both pass a swapped expectation
table. Swept against the pre-fix build (its own HEAD, restored by `cmp` afterward
under a `build/.MUTANT` sentinel): **7 of 12**, red at exactly the five cold BE
rows, at the host-order values; the BE warm control and all six LE controls green.
On the fixed build **12/12**. `r1` is built with immediates, never loaded, so no
load adds a stray general-path access; `COLD` is unseeded RAM (provably cold);
every encoding was checked through `unassemble`.

**Non-defects settled while here, so no future round re-derives them:** the
general halfword and byte store arms agree with the fast path and Table A2-2
(byte order handled or absent) **for their register-domain values — but note
these are assessed by reading, not by a probe row**; and the pre-`#357` UB in the
load-assembly expressions (`data[i] << 24` promoting `unsigned char` to `int`) is
left untouched — this round adds no assembling expression, and that UB has no
witness here. The LDRD big-endian load (`data[1] << 6`) is a separate, visibly
broken expression, recorded and queued.

> **✗ ONE CLAIM ABOVE WAS AN OVER-CLAIM (was: "STRD already took the walk (its
> guard was false for the same reason the word arm's was)"), corrected here by
> `#373`'s follow-up review.** STRD is `datalen == 8` and never reaches the
> `datalen == 4` block this round edited, so the `A__L` gate does not touch it —
> that much is right. But "took the walk" is a **reachability** statement, not a
> correctness one: on a BE guest the walk starts at `i = 7` and writes `Rd`'s
> bytes to `data[4..7]` and `Rd+1`'s to `data[0..3]`, so `Rd` lands at `addr+4`
> and `Rd+1` at `addr` — **the two words are swapped** (DDI 0100I p. A2-32:
> doubleword accesses are a series of word accesses at incrementing addresses).
> STRD on BE is a live defect, not a non-defect; it is the word-order half of the
> queued `BE LDRD/STRD` item, which the `data[1] << 6` note captured only the
> byte-lane half of. Two seats caught the over-claim independently.
>
> **And the round UNDER-claimed its own blast radius.** The impact is framed as
> cold-page-vs-warm-page plus `strt`, but **device pages are never in
> `host_store`**, so pre-`#372` *every* word store to a memory-mapped register on
> a BE ARM guest was byte-reversed permanently, not just on first touch — and
> `MACHINE_SETUP(barearm)`'s 128 MB `dev_ram` mirror at `0xa0000000` is a device
> to dyntrans, so the tree's one BE-ARM configuration sits **entirely** on the
> always-general path. `file_elf.c` also sets big-endian from an `armeb` header,
> so the reach is any ARM machine with a BE image, not only `barearm`. The fix is
> worth more than the block claimed.

## One-hundred-and-fourteenth round (#371) — a gate that failed after a green section could report SKIP, hiding the failure

The battery's own control flow carried the exact defect its rows are built to
catch: a green result that means nothing. `gate_skip()` in `regress/lib.sh` exited
with the SKIP code, which `run.sh` maps to `REGRESS_PASS_WITH_GAPS` — a pass-ish
verdict — and it never consulted the running failure counter. So a gate that had
**already recorded red checks** and then hit a `gate_skip` (a probe that produced no
result line, a missing rig image) reported those reds *as a skip*, and they vanished
from the battery.

- **#371 (`regress/lib.sh`)** — `gate_skip()` now checks `_fails`: a skip requested
  *after* failures is a FAIL, because a skip cannot un-record what already failed; a
  skip from a clean slate stays a genuine skip.

**Measured, test-first, on a synthetic gate** sourcing the committed `lib.sh` — no
emulator needed, which is why this was the round to run alongside a build-tree one.
Before: one recorded FAIL followed by `gate_skip` exited **77** (SKIP →
`PASS_WITH_GAPS`), the failure gone. After: the same sequence exits **1** and names
it (`N of M checks failed before this section could not run`). Two controls confirm
the fix is narrow: a `gate_skip` with **no** recorded failures still exits 77 — a
preflight that genuinely could not run (`need_file`/`need_exec`) is not a failure —
and `degrade()` is unchanged, because `gate_end()` already tests `_fails` before
`_degraded`, so a degraded gate with failures already reported FAIL. The five
mid-gate `gate_skip` sites in `gate_arm.sh` (a probe crashing after earlier sections
passed) are now safe by this backstop; converting them to `degrade` so an
all-green-then-crash renders as "N passed, part could not run" rather than SKIP is a
larger gate refactor, filed separately.

**Why this gate exists at all:** the same class the ARM gate rows keep finding — a
row asserting an absence passes when the guarded thing is dead; a count no row reads
is untested; a green that survives the very defect it guards. This one was in the
scaffold rather than a probe. Gate 14 re-run unchanged after the fix.

## One-hundred-and-thirteenth round (#368) — the copyin fold's rotation shipped unreachable, and its row is a cross-path XOR

`#362` added a six-word rotation to the `netbsd_copyin` instruction combiner, guarded by
`if (r0 & 3)`. **That body never executed under the battery**: every copyin arm in the
fold-marker probe bases on `mov r0,#0x10000`, so `r0 & 3 == 0` always. Measured in round
110 — neutralising the block left the writeback probe 17/17 and the fold-marker probe
14/14. Unreachable, not merely unmeasured.

- **#368 (`regress/arm_fold_marker_probe.py`, `regress/gate_arm.sh`)** — three arms that
  drive the fold with an unaligned base, at all three nonzero offsets. Harness only; no
  emulator source change.

**The row is a fold-versus-template differential on ONE binary**, not a check against
constants computed in the probe. Each arm runs two passes with the base re-seeded to
`0x1000N` at the top of each: pass 1 declines (the `is_userpage` bit is clear) and its six
loads run through the very handler the fold's bail-out delegates to; pass 2 folds. An XOR
accumulator in `r1` (`eor r1,r1,sl` once per pass) makes `r1 == 0` iff the two paths
**agree** — and when they do not, pass 1's own value is recoverable as `r1 ^ sl`.

> **✗ TWO CLAIMS IN THIS BLOCK ARE WRONG, corrected by `#370`.**
>
> **(1) "its six loads run through the very handler the fold's bail-out delegates to" —
> false.** Only the **entry** load reaches `A__NAME__general`. Its general-path access SETS
> the `is_userpage` bit, so the other five hit the **fast** body — a *different* rotation
> site. The commit message got this right and this block did not. It matters: it is precisely
> why an XOR of `sl` **alone** caught the secondary mutant, since `sl` is the one value in
> pass 1 produced by the general path.
>
> **(2) The XOR is REDUNDANT, not load-bearing**, and the over-claim is itself the finding.
> `vals == want` is an **absolute** check — `want` is computed in the probe from the seeds and
> the ROR model, and pass 2 is the fold — so any defect in the fold's rotation is caught by
> `vals` alone, *including* both passes wrong identically, since both-wrong must still differ
> from `want`. The primary mutant was in fact caught by `vals` (`vals=False`, in this round's
> own measurements); `agree` added nothing there. And the secondary mutant was **also** caught
> by the writeback probe's pre-existing `A wb rot word cold plus1/2/3` rows — as this commit
> message itself notes further down. So "a cross-path discrimination no aligned row and no
> value-only row can make" does not survive: it already existed elsewhere. What the XOR
> *uniquely* covers is a divergence in a world where the absolute expectations were themselves
> wrong in the same direction, and a **relative** check is precisely blind to that. Keep it —
> one word, good diagnostics, and same-loop self-contradiction is this fork's signature
> evidence class — but stop calling it the discriminator.
>
> **The real blind spot, now named:** only **one of six** values crosses the pass boundary.
> Pass 1's `fp, r6, r7, r8, r9` are overwritten by pass 2 and compared to nothing. A template
> rotation that is correct for the FIRST access and wrong for LATER ones — load 1 general,
> loads 2–6 fast — yields `agree == True`, `vals == want`, and correct marker counts, and
> nothing in the row catches it. Widening the accumulator to all six registers is queued.

**The XOR is the design, and it exists because the obvious shape was refuted in review.**
A row that reads registers only at the end measures pass 2 against hand-arithmetic,
because pass 2 *overwrites* r6–r11 and pass 1's values are gone by the time the probe
reads them. The accumulator carries the comparison inside the guest, where both values
still exist. `r1` is the accumulator deliberately: the shared `session()` already reads it
back, and only the copyout arms assert it, so the helper needed no change.

**Three offsets, not one.** `8 * (r0 & 1)` agrees with `8 * (r0 & 3)` at +1 and differs at
+2 and +3, and a guard of `if (r0 & 1)` would skip the rotation entirely at +2 — a single
arm cannot separate those mutants. The expected values are the ROR-8/16/24 images of the
six seeded words; "rotation absent" is the unrotated words, which is exactly what the
**aligned** `fires` row asserts, so a fold that stops rotating cannot pass these rows by
satisfying that one.

**Two records `#362`/`#365` got wrong are corrected in passing.** `#362`'s comment
describes the *broken* build ("pass 1 yields the rotated word while pass 2 folds and
yields the unrotated one") — on the shipped build both rotate, so the healthy expectation
is **agreement**, not contradiction. And the marker counts here are **derived, not
thresholded**: install 1, fire 1, decline 1 over two passes, which depends on `#366`'s
corrected fact that the general path's own insert sets the `is_userpage` bit — pass 1's
bail delegates only the entry slot, whose general-path access sets the bit, after which
the remaining five `ldrt` go fast and pass 2 folds.

**The five combiner traps, each avoided by construction** rather than by care: no `step`
anywhere (the session free-runs and interrupts); no breakpoint at all, which also keeps
read-ahead alive — `breakpoints.n` must be 0 for it, and with a 14-word block on one page
the arming slot is translated during read-ahead so the fold is installed *before* its slot
first dispatches, which is why there is no `passes − 1` correction; nothing re-marks the
entry slot; and the matcher provably never reads `r0`'s value — it runs at translation
time, where register values are meaningless.

**Encodings checked through `unassemble` before use**, the branch target especially:
`0x5AFFFFF4` disassembles as `bpl 0x8008`, the re-seed point. A target of `0x8004` would
give three passes and `fire=2`; `0x800c` would never re-seed the base. A wrong target
silently changes the pass count, and the pass count is what makes `fire=1 dec=1` derived
numbers. The other new words: `0xE3A01000` (`mov r1,#0`) and `0xE021100A`
(`eor r1,r1,sl`) — the latter arms `COMBINE(xchg)`'s matcher in passing, which was checked
and declines silently on the same-register short-circuit.

> **✗ THAT DECLINE MECHANISM IS WRONG, corrected by `#369`.** The conclusion holds — it
> declines, and prints nothing either way, since `xchg` prints only on install — but not for
> the stated reason. `COMBINE(xchg)` reads `a = ic[-2].arg[0]` and `b = ic[-1].arg[0]`, which
> at the `eor`'s slot are the `ldrt r8` and `ldrt r9` slots, whose `arg[0]` are **both
> `&r[0]`** — the two loads' shared *base* register. So `a != b` fails on that, not on any
> same-register property of `r1`; and independently `ic[-2].f` is a load handler rather than
> `instr(eor_regshort)`. Recorded because "checked and declines" was true while the *reason*
> given was invented, which is the failure mode this project keeps paying for.

**Honest scope — and `#370` downgrades this paragraph's own sourcing to UNVERIFIED.**
The `bcopyinout.S` claim below appears in this tree only in our own writing (this block,
the probe comment, and an OUTSTANDING entry); there is **no NetBSD source in the repo**,
so it is a load-bearing scope claim sourced from panel recollection — the exact DDI 0100I
provenance pattern `CLAUDE.md` warns about, caught this time before it aged. To settle it:
read `sys/arch/arm/arm/bcopyinout.S` in a real NetBSD tree, or disassemble `copyin` in the
ARM kernel image the battery already uses. Note the claim is also *narrower* than needed
even if true: that alignment test is about src/dst relative alignment, and the unaligned
path may still issue `ldrt` at unaligned addresses. Until checked, the honest statement is
"the rows pin internal consistency; guest reachability of the unaligned fold path is
UNVERIFIED", not "a real guest never reaches it". NetBSD's `bcopyinout.S` reportedly does `ands r3, r0, #0x03 / bne` before its
six-`ldrt` block, so a real guest never reaches this fold with an unaligned base. These
rows pin an **internal-consistency** property — the fold agreeing with the handler its own
bail-out delegates to, the `#342`/`#355` class — not a guest-reachable behaviour.

## One-hundred-and-twelfth round (#367) — path attribution stops being a comment and becomes a checked quantity

Which of the two load/store paths a probe row takes was asserted in prose, and it was
**wrong three rounds running**: `#364` found the `put w` / `put b` warming note **inverted**
and recorded as a *verified mechanism*, with two shipped rounds leaning on it; `#364`'s own
draft then attributed a writeback site to an offset form that compiles no writeback
statement at all; and `#365` found the general writeback sites reached but
**undiscriminated**. Each was rediscovered with a throwaway marker, a scratch build and a
fresh investigation, because the instrument never survived the round.

- **#367 (`include/cpu_arm.h`, `cpus/cpu_arm.c`, `cpus/cpu_arm_instr_loadstore.c`,
  `regress/arm_writeback_probe.py`, `regress/gate_arm.sh`)** — the emulator counts entries
  into `A__NAME__general`, `tlbdump` reads the counter out, and the gate asserts a derived
  expected count for every one of the 22 rows.

**The observation window was one empty function away.** `arm_cpu_tlbdump` was an **empty
stub**, while `tlbdump` is already the debugger's designated verb for exactly this state and
prints it on other architectures. So the state that decides fast-versus-slow — page presence
in `host_load`/`host_store` and the `is_userpage` bit — was unobservable from outside a build
one edit from exposing it. Filling an upstream-shaped stub is the smallest possible touch,
and it is **pull-only**: nothing prints unless a session asks, so the rows elsewhere in this
battery that assert an **absence** of output are untouched, and a free-running guest cannot
be flooded.

**There is no external answer, and the reason is structural rather than practical.** The
fast and general paths are *required* to produce identical architectural effects —
observational equivalence is the correctness condition for a dyntrans cache, and `#357` and
`#362` deliberately made them agree — so any guest-visible signal that distinguished them
would itself be a bug. Corollaries, recorded so the question is not reopened: instruction
counts are path-invariant (`A__NAME__general` is *called from* `A__NAME`, not dispatched, so
the `mp` NCYCLES register, `cpu->ninstrs` and the statistics facility all bill identically);
the translation arrays are private struct members; pty wall-clock timing is hopeless, as this
session's own load-induced `gate_ab` failure showed; and `dump`/`put b` can read or write
memory without warming but cannot *see* warmth. One further route is worse than useless —
`#250` write-watchpoints **coerce what they observe**, since `update_translation_table`
deliberately holds a watched page's `host_store` NULL to force stores down the slow path.

**A counter, not a marker — and the disqualifier is PERTURBATION, not cost.** `debugmsg`'s
quiet path is genuinely cheap (a varargs call and a few integer tests; the formatting sits
after the gate). It is disqualified three times over regardless: the verbosity gate is
**bypassed under single-step**, so a permanent template marker would print on every stepped
general-path access forever; the subsystem-breakpoint test runs **before** that gate, so
`breakpoint subsystem cpu` would enter the debugger once per access machine-wide; and this
fork's own `#278` convention **forbids** pre-gating a marker, so a conforming one is loud by
design and a pre-gated one violates the convention. A plain `++` has none of these modes, and
sits in a function that already pays a full `memory_rw` slow path per entry, so it is
structurally unmeasurable there. The fast path is untouched. Two other transports were
rejected with reasons worth keeping: a **guest-visible counter word**'s increment is itself a
memory access that can **recurse into the general path it counts**, and pollutes the
translation state under test; a new `mp`-style register is **self-counting**, since the
readout load from a device page is itself always a general-path access.

**The expected count is a RULE, not a table**, because a wrong expectation becomes a new
false red:

> count = (page × needed-permission) upgrade events + T-form first touches per page

The general path's own `memory_rw` **self-warms** — it inserts, setting `host_load`
unconditionally, `host_store` iff the access was a write, and the `is_userpage` bit iff it
was a user access. So every `put w`-seeded row is **0**, including all ten iterations of the
×10 rows and both passes of the re-seeded row; the four `put b`-seeded cold rows are **1**;
and the `ldrt` row is **1 even though its page is warm**, because the `is_userpage` test
precedes the page test and a kernel `put w` insert never sets that bit. Non-obvious cases
stated for whoever adds rows: a **cold ×10 row is 1**, not 0 and not 10, since iteration 1
warms via the general path's own insert — it is 10 only where insertion is *blocked* (a device
page, a partial page, MMU-on unmapped); and a cold row doing a load then a store on one page
is **2**, because the load's insert leaves `host_store` NULL.

> **[#382 correction]** Two claims in the paragraph above are inverted for the MMU-off
> testarm/barearm rigs these rows actually run on: `host_store` is set on ANY data access,
> not "iff the access was a write" (MMU-off ⇒ `update_translation_table` writeflag = `ok-1`
> = 1, so a *load* warms `host_store` too), and a cold load-then-store on one page is therefore
> **1**, not 2. The `2` / "leaves `host_store` NULL" case is MMU-on-on-a-read-only-page only.
> The shipped `LSGEN` expectations — five rows, every value `1` — are unaffected; only this
> derivation prose was wrong. Corrected statement: the #382 round block and
> `arm_endian_probe.py:56-59` (that probe carried the correct polarity from #382 on).

**MEASURED: 22/22 values and 22/22 paths.** Every derived expectation held on the first run —
seventeen zeros, five ones. The seventeen zeros are exactly the claim `#364` found inverted,
now permanently asserted rather than believed. Verified separately, one variable at a time, on
one binary: the same load from a `put w` page reads 0 and from a `put b` page reads 1, and the
T form reads 1 from a *warm* page — confirming it is general-path by construction and immune
to any future seeding change.

**The `" path"` suffix on the new rows' names is load-bearing, not cosmetic.** The gate greps
named rows as `^<name>  .*ok$` — two spaces — so printing a path row under the bare name would
have given every one of the 22 existing named checks a count of 2 where it expects 1, turning
the whole section red. Verified afterwards that all 22 value names and all 22 path names match
**exactly once each**, with the longest path name at 31 characters, inside the `%-32s` column.

**A harness bug of mine, reported because test-first caught it and the shape recurs.** The
first verification script reported the cold page as 0, which looks exactly like the instrument
failing. It was quoting: a multi-line seed passed through command substitution was mangled, so
the `put b` writes never landed. A rerun with a plain multi-line variable gave 1, and a
register readback confirmed the load had executed. Same class as the clobbered-pristine-binary
incident earlier in this session — when a measurement contradicts a derivation, suspect the
harness before the emulator.

Propagated byte-identically to `est/` and both in-place build trees; `src/cpus/*.o` removed
before rebuilding, since these `.c` files are `#include`d and the dependency rules miss them.
The build's own check caught that the first rebuild had compiled **stale** sources, which is
exactly the trap that no-VPATH tree exists to create.

## One-hundred-and-eleventh round (#365) — "unreached" was wrong; the sites were reached and nothing DISCRIMINATED the fix

`#364` recorded that both general-path writeback sites were **uncovered** and that
`#357`'s correction "still has no row reaching it". A falsification run refuted that,
and the corrected finding is sharper than the claim it replaces.

- **#365 (`regress/arm_writeback_probe.py`, `regress/gate_arm.sh`)** — two rows that are
  the first anywhere in the battery to **discriminate** `#357`'s general-path fix, plus
  the correction to `#364`'s claim. Harness only; no emulator source change.

**The refutation.** Deleting the two general-path writeback statements does **not** leave
gate 14 green: it turns **8 of 264 checks red** — and none of them in the writeback
probe, which stays at 20/20. The red rows are in two other sections, and they identify
which row was already reaching each site:

| site | already reached by |
|---|---|
| general **pre**-index | the strlen probe's `ldrb r3,[r4,#1]!` — P=1/W=1, taking the general arm on each new page |
| general **post**-index | the fold-marker probe's `copyin cold` / `copyout cold` arms — `ldrt`/`strt` with the `is_userpage` bit left clear, whose "r0/r1 advanced by 24" witness *is* a writeback assertion |

> **✗ One detail of the row above was wrong when it shipped, corrected by `#366`.** It said
> *all six* of those `ldrt`/`strt` run in `A__NAME__general`. Only the **first** does: the
> general path's own `memory_rw` insert **sets** the user bit — `cpu_dyntrans.c` does
> `if (useraccess) is_userpage[index >> 5] |= 1 << (index & 31)`, and the found-entry arm
> clears-then-sets it — so the second `ldrt` on that page finds the bit set and takes the
> **fast** path. The fold-marker probe's own docstring already said it ("only pass 2 and
> later can fold"), which is the tell that should have caught this before the commit. The
> count is **one** general entry per cold arm, not six. Nothing else changes: the arms still
> reach the site, and the 8-red measurement stands.

Attribution was then separated with a **post-index-only** mutant: strlen goes 7/7 green
and exactly the two fold cold arms go red. That pins each family to its own statement, as
it must — P=1/W=1 and P=0/W=1 are distinct translation units, each compiling only its
own `#ifdef` arm.

**But the round's substance survives, and this is the distinction worth keeping.** Built
with the *faithful* pre-`#357` bug — the general writeback **re-masked**, `addr` instead
of `wb_addr`, fast pair intact — the whole of gate 14 **passed at 264 checks, zero
failures**. Every row that reached those sites was blind to the mask: `ldrb` has
`datalen 1`, so `addr &= ~(datalen - 1)` is the **identity**, and the fold arms use
aligned bases `0x10000`/`0x11000` where masked and unmasked agree. So the honest word is
**undiscriminated**, not unreached — and *reaching a statement without discriminating its
correction measures nothing about it*. That is a fifth distinct way a green row can mean
nothing, and it is the subtlest so far: the row runs the code, and still cannot tell the
fix from the bug.

**The instrument is correct by construction, not by circumstance.** `ldrt` reaches
`A__NAME__general` because the template tests `is_userpage[addr >> 17]` **before** the
`page == NULL` test, and the bit is set only when `update_translation_table` receives
`MEMORY_USER_ACCESS`, which only the T-form family passes. So a `put w`-warmed page still
sends the first `ldrt` down the general path — immune to any future seeding change, unlike
a cold page, which the device arm or an unguarded `put w` can silently re-warm. Encoding
checked through `unassemble` (`e4b01004 → ldrt r1,[r0],#4`), and it lands in
`tmp_arm_loadstore_p0_u1_w1.c` — one of the four translation units the residual list says
nothing enters, so the count of those drops to three. `Rd` is **r1 and not r9** on
purpose: `0xE4B09004` is the word that arms `COMBINE(netbsd_copyin)`, which would have put
the row in the combiner's path measuring something else.

**Measured on four builds**, which is what makes these rows worth their lines:
pristine **22/22** and gate 14 **PASS at 266**; general writeback **deleted** → 20/22, red
at the un-incremented base; general writeback **re-masked** (the real `#357` bug) → 20/22,
red at exactly the predicted masked values; **post-index only** → 21/22, separating the two
sites. A row that passes on a good build but does not fail on the mutant measures nothing.

**Closed by construction rather than by a row**, and worth recording because it retires a
standing open question: the "double `reg_func` call on the fast-to-general fallback is
provably benign" claim is **unobservable**, not merely unmeasured. Load/store decode always
indexes the low half of `arm_r[8192]`, which the generator emits as the `s == 0` family — a
scan finds **4096 `s == 0` functions, none writing CPU state**, against 4080 of 4096
`s == 1` that do. Even the RRX case reads `ARM_F_C` and writes it only under `if (s)`. No
row can observe a doubled call through a pure function, so no row is owed.

**Still owed**, unchanged in substance but now correctly scoped: a general **store**-arm
row (`strt r2,[r0],#4` = `0xE4A02004` is warming-immune and preferable to a cold `str`),
a general register-offset row (`0xE6B01002 = ldrt r1,[r0],r2`), the `netbsd_copyin`
unaligned-base arm, and the permanent path telemetry. Note for whoever writes the store
row: with the MMU off `ok - 1 == 1` always, so **any** warming access — even a load — sets
`host_store` too, meaning a store-cold page must never be touched by a warming access at
all.

## One-hundred-and-tenth round (#364) — the row-to-site table was inverted, so two shipped rotations were never measured

`#362`'s commit message claimed its three new rows prevented "a measurable
self-disagreement behind a green gate". That was true of one of its three rotation
sites and false of the other two, and the reason was a mechanism note recorded here
as **verified** — with the two cases exactly the wrong way round.

- **#364 (`regress/arm_writeback_probe.py`, `regress/gate_arm.sh`)** — three
  `put b`-seeded rows that are the first in this probe's history to reach
  `A__NAME__general`, plus corrections to every record that asserted otherwise.
  Harness only; no emulator source change.

**What was believed.** The probe's docstring and the gate's row-to-site table both
said: "the fast path only runs once the page is in the translation array, so a
SINGLE-execution row measures the GENERAL path and nothing else." `OUTSTANDING_BUGS`
recorded the supporting mechanism among "two verifications worth keeping, because they
underwrite the row set": that `put w` seeding uses `CACHE_NONE | NO_EXCEPTIONS` and so
"cannot pre-populate the arrays".

**What is true.** That describes **`put b`**. `put w` routes through
`store_32bit_word` → `memory_rw` with **`CACHE_DATA`**, and insertion into the
translation array is gated on `!no_exceptions` — so seeding a page with `put w`
**warms** it, and `host_load` is non-NULL before the guest executes anything.

**MEASURED, and it is worse than "one site uncovered".** A temporary marker at the top
of `A__NAME__general` counted **zero** hits across **all 17 rows** — not only the
one-shot rows but every iteration of the ×10 rows and both passes of the re-seeded
row. No row in the file reached the general path at all. Consequences, each confirmed
independently rather than inferred:

- Neutralising `#362`'s **general-path** rotation left the writeback probe at
  **17/17** and the whole of **gate 14 PASS at 261 checks**.
- Neutralising `#362`'s **`netbsd_copyin`** rotation left writeback at **17/17** and
  the fold-marker probe at **14/14**. Worse: every copyin arm in that probe bases on
  `mov r0,#0x10000`, so `r0 & 3 == 0` always and the six-word rotation body **never
  executes**.
- `#357`'s general-path **writeback** sites are unmeasured by the same argument, so
  that round's historical 5-of-14 pre-fix sweep is entirely a fast-path result.

**The mechanism is pinned on ONE binary by ONE variable**, which is what makes this a
measurement rather than a story. On the general-rotation-dead build, changing only the
seeding width of the page being read: `put b` gave `ls_general=1` and the mask-only
answer `0x11223344`; `put w` gave `ls_general=0` and the rotated `0x44112233`.

**A proposal was refuted before any code was written**, which is the part of test-first
that pays for itself. The review suggested seeding via a **guest store**, on the theory
that it warms `host_store` only and leaves `host_load` NULL. Measured false:
`update_translation_table` sets `host_load` **unconditionally** and gates only
`host_store` on the write flag, so storing to a page warms it for loading too. `put b`
is the only seeding that leaves a page cold.

**Three rows added, not seventeen switched.** Switching the probe wholesale to `put b`
would move every existing row to the general path and **delete** the fast-path
coverage — which is currently the only coverage those four sites have. So the existing
17 rows and their seeding are untouched, and the new rows read a dedicated page at
`0x20000` that nothing else in the file touches. Measured both ways before landing:
**20/20** on the committed build, and **17/20** with the general-path rotation dead,
red at exactly the three new rows.

**Records corrected, because a false note that is *believed* costs more than a missing
one.** The probe's site table, and the docstrings of `once()` ("Reaches the GENERAL
path only" — it reaches it never), `loop10()` ("iteration 1 takes the general path")
and `warmed()` ("pass 2 is the only execution … that reaches the fast pre-index site" —
both passes do). The gate's table, which also **referred forward to a "CORRECTION
below" that was never written**, and its claim that "no row pins the unaligned loaded
DATA", falsified by `#362` itself. The struck mechanism note in `OUTSTANDING_BUGS`. And
`#362`'s own CHANGELOG claim. The numeric site cites (`:213/:216`, `:338/:342`) had
gone stale a **third** time in a file whose own `#357` note says a numeric cite here
has gone stale twice — so they are gone rather than refreshed.

**Records corrected — and the ones NOT corrected, named rather than implied.** A
review seat pointed out that "every record" was overstated, so: `#357`'s own block is
now struck where it asserts the inverted mapping, and the probe's stale
"NO UNALIGNED-LOAD-DATA ROW" section, its residual numeric site cites (stale a
**third** time in the file whose `#357` note warns about exactly that), and its
`%-34s`/`%-32s` column discrepancy are all fixed here. Still **not** re-audited: the
instrument-gap inventory in `OUTSTANDING_BUGS`, several of whose claims about which
fast paths are covered follow from the same inverted premise. That is a separate
round, and this block does not pretend otherwise.

Two smaller corrections from the same review: `put b` is **not** the only cold
seeding — the debugger's string modes `put s` and `put z` also write with
`CACHE_NONE | NO_EXCEPTIONS`, so it is the flag that matters and not the command.
And the evidence types differ and should not be conflated: `#362`'s two rotations
were **mutation-tested** (neutralised, gate still green), whereas `#357`'s writeback
sites are shown unmeasured by the **zero-hit marker** — sufficient, since nothing
inside a function no row enters can be measured, but not the same experiment.

**A draft of this round's own table repeated the error it corrects**, and the catch is
worth recording because it took a second review pass. The draft claimed the three new
rows cover "general post-index writeback". They do not: their `LDR_OFF0` is P=1/W=0,
and the template emits a writeback only under (P ∧ W) or (¬P) — so an **offset form has
no writeback statement at all**, and `wb_addr` is not even declared for it. What the
cold rows genuinely cover is `A__NAME__general`'s **load-and-rotate** arm and the
`memory_rw` slow path, which is a **data** site, not one of the four writeback sites.
The round's value is unchanged — `#362`'s general-path rotation was deletable with the
whole gate green before these rows existed — but the table now separates the two axes
instead of conflating them, which is the same discipline the inverted note failed at.

**Still owed and recorded, not quietly dropped:** **both** general-path **writeback**
sites, pre- and post-index, still have no row, so `#357`'s general-path fix remains
entirely unmeasured.

> **✗ REFUTED BY `#365`, and the correction is sharper than the claim.** Both sites were
> already being **reached** — deleting their two statements turns **8 of 264** gate checks
> red, in the strlen probe (whose `ldrb r3,[r4,#1]!` is P=1/W=1) and in the fold-marker
> probe's `copyin cold`/`copyout cold` arms (six `ldrt`/`strt` with `is_userpage` clear).
> What was missing was **discrimination**: rebuilt with the faithful pre-`#357` bug (the
> general writeback re-masked rather than deleted), the whole gate **passed at 264, zero
> failures**, because `ldrb` has `datalen 1` so the mask is the identity and the fold arms
> use aligned bases. The right word is *undiscriminated*, not *unreached*. `#365` adds the
> two rows that do discriminate it, verified against that exact mutant.

A better instrument than the cold page exists for that and the
project had already recorded it without using it: an **`ldrt` form is general-path by
construction** — the `#if !defined(A__P) && defined(A__W)` block tests `is_userpage`
and falls into `A__NAME__general` when the bit is clear, **regardless of warming** — so
it cannot be silently voided by a future `put w`, needs no cold page, and enters
`p0_u1_w1`, one of the four translation units the residual list says nothing enters.
The cold page is still required for general **pre-index**, which has no T form. The
`netbsd_copyin` rotation still has no row, which needs an unaligned-base two-pass
`ldrt` arm in the fold-marker probe rather than anything here. And a permanent
path-telemetry check — asserting the warm rows stay fast and the cold rows take
exactly one general fallback — would make this class self-reporting instead of
requiring a temporary marker and a subagent to rediscover it. All six are written up
in `OUTSTANDING_BUGS.md`, on the queue rather than in prose here: a review pass caught
this block, the probe and the gate all pointing at an entry that did not yet exist —
the same dangling forward reference this round removes from the gate, recreated by the
round removing it.

**Harness: gate 14 PASS at 264 checks** (261 + the three new named rows), and the probe
reads **20/20** on the committed build. The round took **two** review passes: the first
found the mechanism uncited and the alias hole; the second found this round's own table
repeating the error it corrects, plus the dangling reference, plus two wrong numbers in
notes whose subject is exactness (the strike note overclaimed "Fixed in `#364`" when
only the rotation half is, and the column note said the longest row name is 24 chars
when it is 26). Recorded because the pattern is the point: a records-correction round
is exactly where a false record is easiest to introduce.

## One-hundred-and-ninth round (#363) — the gate-14 flake: the prompt predicate matched the guest's own output

Gate 14 failed **exactly 2 of its checks in 1 run out of 4**, with no code change
between runs. That is corrosive out of proportion to its size: seven batteries
underwrite six shipped corrections, and an unexplained red row teaches the reader
to dismiss red rows.

- **#363 (`regress/arm_{flags,idle,memcpy,strlen,writeback,fold_marker}_probe.py`)** —
  the prompt-readiness predicate now matches the **full** prompt, `GXemul>`, instead of
  a bare `>`, at all **thirteen** sites. Plus one row that failed to a misleading value.

**The mechanism, and it is not where a reader would look.** `debug()` reaches
`va_debug()`, which emits **one `printf` per character**, so on a pty — `_IOLBF`, and
these six probes `exec` the binary directly rather than through `lib.sh`'s `stdbuf` —
the only flush boundary is the newline, and the ARM register dump arrives as **five
separate `write(2)`s**. Its **first** line ends in `>` unconditionally: `cpu_arm.c`
prints `  <%s>` with `" no symbol "` as the fallback, and `testarm` never calls
`machine_add_devices_as_symbols()`. A reader waking between line 1 and line 2 therefore
saw a bare `>`, decided the debugger was ready, and returned with the registers still
unread — while `cpsr`, which sits **on** line 1, was already there. That asymmetry is
the whole signature: `A idle path dest` failed alone while its sibling
`A idle path flags` passed, and in `gate_arm.sh` one red **named** row costs exactly
two checks (the aggregate `rows correct`, plus that row's own check).

**MEASURED, and the measurement is deterministic rather than statistical.** Replacing
`os.read(fd, 65536)` with `os.read(fd, 1)` evaluates the predicate at every byte
boundary, which converts the scheduler race into a certainty. On one idle host, in one
experiment: the committed probe scored **9/9**; the 1-byte reader with a bare `>`
scored **8/9** with `A idle path dest` reading `None`; the 1-byte reader with the full
prompt scored **9/9** again. The same run confirms the mechanism and validates the fix.
The 64 KB reader scores 9/9 either way, which is precisely why this was intermittent
instead of visible.

**The first test plan was wrong and was thrown away.** It proposed measuring the
truncation *rate* idle versus under load. That could not have refuted anything: at a
few per cent base rate, "30 post-fix runs show zero" is the expected outcome under both
hypotheses — the round-65 lesson that a sweep proves nothing about a tail it cannot
reach. Two seats also pointed out the load prediction may be **backwards**, since on an
idle multi-core host the woken reader can be dispatched on another CPU within
microseconds and catch a partial buffer, whereas load delays the reader as much as the
writer. Three more proposed `strace` on the `write(2)` granularity, which measures
mechanism where a rate measures only frequency; the 1-byte reader is that idea taken
one step further, and it doubles as the fix's validation.

**Matching the full prompt is SUFFICIENT, not merely safer** — worth stating because the
brief argued only the weaker claim. The prompt is written **after** all five lines and a
pty preserves order, so seeing the real prompt *guarantees* the complete dump has
arrived. It also disarms two latent `>` sources that are unarmed today only by the
probes' own choices, not by anything in the emulator: `cpu_arm.c`'s load/store
disassembly emits an **unguarded** `<0x%08x…>` whenever a breakpoint or trace hits one
(both `DISASSEMBLE` call sites pass `running = 1`; today every breakpoint in these
probes happens to land on a `NOP`), and `dump`'s ASCII column ends a line with its last
byte, which would end in `>` for a seed byte of `0x3e`. **A premise of the design brief
was false here** and is corrected in the source comment: the brief claimed
`< no symbol >` was the *only* `>`-terminated line and eliminated the disassembly as
symbol-guarded. It is not guarded. That collapsed the brief's diagnostic narrowing — but
it strengthens the fix, which now pre-empts both traps.

**A row must fail to a token DISTINGUISHABLE from the defect it guards.**
`A strlen alias moved` computed `"moved" if (r3 is not None and r3 > base + 16) else
"no"`, so a **lost read** produced `"no"` — byte-identical to the pre-`#355` signature
of a fold that exited after three bytes. Every other truncation-sensitive row in the
suite fails to `None`, `dead` or `DEAD`; this one alone failed to a value that reads as
a real regression, which is the corrosive-red-row problem inverted — it would have
taught the reader to *believe* a phantom. It now reads `"unread"`, and the change is
verdict-preserving on every successful read because `r3 is not None` was already
required for `"moved"`. `A fold scanc notbl` already had this shape; its comment states
the principle.

**Deliberately not in this round**, because each is a different defect with a different
justification and one of them has no measurement yet: `arm_flags_probe.py`'s two
remaining whole-buffer waits still match a **stale** prompt, so every `send()` after the
first returns instantly and ~1500 commands stream into the 4 KB console FIFO — a
deterministic defect, not a race, and one whose reproduction has not been run;
`send()`'s return value is discarded almost everywhere, so a prompt that never arrived
is indistinguishable from one that did; six reads still have no retry (three `reg`, two
`print`, and the fold-marker copyout `dump`); and a `READS_RETRIED` counter with a gate
check at zero would make the next such flake self-identifying instead of costing a panel
and a battery. Recorded in `OUTSTANDING_BUGS.md`. **Do not** "fix" the missing
`stdbuf -o0`: per-character `printf` under `-o0` makes every byte its own write and
multiplies exactly the boundaries this round removed.

## One-hundred-and-eighth round (#362) — unaligned word loads returned the aligned word, unrotated

The second of the two divergences `#357`'s research turned up, and the one it
deferred. An unaligned word **load** must return the aligned word **rotated right
by `8 * addr[1:0]`** — DDI 0100I A2.8 (p. A2-38) states it, and A4.1.23 LDR's
pseudocode is `data = Memory[address,4] Rotate_Right (8 * address[1:0])` when the
CP15 U bit is 0. This template masked and never rotated.

- **#362 (`cpus/cpu_arm_instr_loadstore.c`, `cpus/cpu_arm_instr.c`)** — capture
  `8 * (addr & 3)` before each mask and rotate after each word arm's byte
  assembly, in both the general and the fast path, plus the matching rotation in
  `netbsd_copyin`.

  **Measured, and the measurement identifies the model rather than merely failing
  an expectation.** With the word at the base seeded to `0x11223344`, the three
  candidate behaviours — mask-only, rotate, and the ARMv6 `U == 1` true unaligned
  access — are **pairwise distinct at every nonzero offset**, so a wrong answer
  says *which* model is implemented. Pre-fix read `0x11223344` at all four
  offsets, i.e. mask-only; post-fix reads `0x11223344 / 0x44112233 / 0x33441122 /
  0x22334411`, i.e. rotate.

  **LOADS ONLY.** A4.1.99 says STR ignores the low two address bits, so stores
  were already right — confirmed by measurement, a store at each offset leaves the
  aligned word modified and its neighbour untouched. A4.1.28 makes an unaligned
  halfword load's data UNPREDICTABLE, so masking without rotating stays permitted
  there. LDRD is excluded automatically, because `A__LDRD` does not define `A__L`.

**The fast path was not the hard part, and the note that said otherwise was
wrong.** `#357`'s record warned that a slow-path-only rotation would be silently
undone and that the fast path was materially more work — the reason this stayed
queued as a large round. It is the same three lines: that path already masks and
then assembles the bytes of the *aligned* word, so rotating the assembled value is
exactly equivalent to re-indexing them. Eleven lines, four sites, no warnings.

**`#357`'s `wb_addr` could not be reused**, which is worth recording because it is
the obvious shortcut: it exists only under `!defined(A__P) || defined(A__W)`, and
the plain offset-addressing word load has neither, so the rotation needs its own
guarded capture. It is taken *after* `page` and `is_userpage` are indexed from the
unmasked address, so `#357`'s bounds argument is untouched.

**`netbsd_copyin` had to change in the same commit**, and the measured form of why
is sharper than a fold-versus-`-J` differential. On **one binary** with an
unaligned base, pass 1 declines, runs through the template and yields the rotated
word, while pass 2 folds and yields the unrotated one — the emulator contradicting
itself inside a single guest loop, the `#342`/`#355` class. Its matcher inspects
only the preceding slots' handler, base register and offset, never the base's
*value*, so an unaligned base does fold. Every other fold is clear for a stated
reason: `copyout` does stores; `memcpy` and the block-transfer handlers are the
LDM/STM class this template cannot reach; `idle` reads one word but writes it only
when provably zero, and rotating zero is zero; `cacheclean` performs no read at
all; `scanc` and `strlen` are byte loads.

**Applied unconditionally rather than gated on architecture version, by a
dominance argument rather than a preference.** Rotation is correct for ARMv3/v4/v5
and for v6+ with `U == 0`; where v6+ with `U == 1` wants a true unaligned access,
masking and rotating are wrong *equally*. So this is never worse than what it
replaces, in any combination. Gating would also be unsound here: there is no
architecture level in the CPU type table — its own header says "TODO: Include ARM
level" and "Most of these are bogus" — deriving one from the ID register
misclassifies one part as ARMv6, wrong in the direction that changes behaviour,
and no `ARM_CONTROL_U` is defined anywhere. Recorded divergence: v6+ with
`U == 1`. Population supports it too: 7 of the 9 ARM machines select a v4/v5 CPU,
and the two in the divergence zone have neither a guest image nor a rig.

**Nothing depended on the old behaviour.** All six committed ARM probes read
251/251 on both builds, and the round adds three rows because the existing ones are
**all aligned-base** and blind to this: without them the change would ship a
measurable self-disagreement behind a green gate. Offset 0 deliberately gets no
row — rotation by zero is the identity, so it could never fail. Swept pre-fix:
14 of 17, red at exactly the three new rows.

> **✗ CORRECTED BY `#364`.** That last claim holds for the **fast** path only. The
> three rows added here seed their page with `put w`, which warms the translation
> mapping, so all three take the fast path — and the **general-path rotation and the
> `netbsd_copyin` rotation shipped in this round were both unmeasured**. Each was
> independently confirmed deletable with the whole of gate 14 still green at 261
> checks. Worse for `netbsd_copyin`: every fold-marker arm bases on `mov r0,#0x10000`,
> so `r0 & 3 == 0` always and that rotation's body **never executes**. The round did
> ship a measurable self-disagreement behind a green gate at two of its three sites,
> which is exactly what the sentence above claimed it prevented. `#364` adds three
> `put b`-seeded rows for the general path; the copyin row is still owed.

**Harness: gate 14 PASS at 261 checks** (was 258); full battery 14 of 15. The single
red gate was **not** this round's — gate 7 `gate_ab` returned HEAD `1:1:0` on luna88k
under host load, and `1:1:1` matching prebatch when re-run alone on a quiet machine.
Recorded separately in `OUTSTANDING_BUGS.md` as a harness defect in its own right: a
wall-clock oracle whose timeout is indistinguishable from a real capability regression,
since both produce `1:1:0`. This round could not have caused it regardless — it touches
only the two ARM files, and m88k compiles no ARM code.

## One-hundred-and-seventh round (#361) — the last two folds with markers but no rows, and a negative arm that was vacuous alone

`#358` gave five folds fire markers; `#360` gave two of them rows. This round
closes the debt on the other two — the scope criticism `#358` earned — and finds
the `#360` defect a third time, in a new place.

- **#361 (`cpus/cpu_arm_instr.c`)** — decline markers on **both** of
  `netbsd_scanc`'s bail sites plus install markers in its matcher and in
  `xchg`'s.

  `scanc`'s two sites **cannot share one reason expression** the way
  `copyin`/`copyout` do: the second tests a page derived from the byte the first
  proves unreadable, so each prints at its own guard, with distinct spellings so a
  row can say *which* page missed. Neither text contains "combined", which would
  make the probes tally declines as fires.

  `xchg` gets **no** decline marker, because it has no bail path. Its rejection
  happens in the **matcher**, so its signature is `install 0` — a fundamentally
  different shape from a guard decline's `install 1 / decline 1`, and the two must
  not share an expected form.

**The finding, and it is the `#360` lesson a third time.** The obvious `xchg`
negative arm — three EORs on one register, the shape `#342`'s guard rejects —
reads `install 0 / fire 0`, which is **identical on a healthy build and on one
with `xchg`'s arming removed**. Alone it cannot tell "the matcher rejected the
shape" from "the matcher does not exist". Measured on an arming-dead build:
`A fold xchg samereg` reads **ok** while the new `A fold xchg selective` goes
**red**.

The fix taken is to make the coupling explicit rather than to change the
emulator: selectivity is **one row spanning both arms**, which cannot pass unless
the matcher both installs for distinct registers and declines for equal ones. The
pair was always the meaningful unit; this stops a reader mistaking half of it for
a test. **The rejected alternative is recorded** — a seat built and measured a
version that relocates `#342`'s `a != b` term into the matched shape so the arm
self-diagnoses, and it works, but it edits a shipped correction's guard for
instrumentation's sake.

**`scanc` turned out to have a better witness than "none".** Its result register
was thought to read zero in every arm; it actually takes **three distinct
values** — the table byte when the fold runs, `table[0]` when the string page is
missing (an unmapped load yields zero, so the genuine path indexes the table with
zero), and zero when the table page itself is the missing one. Each arm therefore
has a value witness *and* a sentinel proving the program reached its end,
confirmed not to perturb the fold. Even so, the marker triple is the only real
detector: on an arming-dead build all three arms keep **byte-identical registers**
and only the markers move, so a value-only row would be vacuous for this fold too.

**Two construction facts measured along the way.** The debugger's `put b` does
**not** warm the translation mapping while `put w` does — the byte path uses
uncached, no-exception access while the wider stores go through the caching path.
That refines what an earlier round recorded as simply "`put w` populates it": the
width matters. And `scanc`'s second decline site is only reachable with the string
page already warm; without the warm-up the row declines at the *first* site
instead, so the warm-up is load-bearing for that arm specifically — and it must
use a base register the matcher does not pin, or the warm-up load is itself a fold
candidate.

**A probe defect of my own, recorded because its symptom misleads.** The session
helper read a fixed register list that omitted the two `scanc` witnesses, so all
three arms reported a zero result and a missing sentinel **while their marker
counts were already correct** — it looked as though the guest had not run when in
fact only the readback was absent. The comparison is now `is not None`-guarded,
because one arm legitimately expects zero and a missing readback must not pass as
a correct zero.

Gate 14 grows 6 checks; the fold-marker probe goes 8/8 → 14/14.

## One-hundred-and-sixth round (#360) — the row that asserted an absence still passed when the fold was dead

`#358` gave two folds a fire marker and a `quiet` row asserting that no marker
appears at default verbosity. That row tests the **verbosity gate**, not the fold:
an absence is exactly what a dead fold produces. This round replaces it with a
control that makes a positive statement.

- **#360 (`cpus/cpu_arm_instr.c`)** — a **decline marker** on `netbsd_copyin` and
  `netbsd_copyout`, computed in the guard's **own short-circuit** so the diagnosis
  cannot drift from the condition it describes (duplicating the three terms in a
  separate print would be a second thing to keep in sync), plus an **install
  marker** in each matcher.

  The install marker is what makes the diagnosis one-read, and the reason is that
  a decline marker alone gives only a **two-way** split: "the matcher declined"
  and "the slot was never dispatched" both read fire 0 / decline 0. With all three
  terms — install 1 / fire 1 / decline 0 is healthy; install 1 / fire 0 /
  decline 1 means the fold was reached and turned the operands down, and the text
  names which clause; install 1 / fire 0 / decline 0 means the slot never
  dispatched, i.e. a misplaced breakpoint; install 0 means the matcher declined.
  The install marker costs **one line per translation**, not per execution.

  The decline text deliberately avoids the word "combined", because the probes
  count fire markers by matching `<name>: combined` and a decline line containing
  it would be tallied as a fold that fired.

- **`regress/arm_fold_marker_probe.py`** — a `warm`/`cold` pair per fold, two
  programs differing by **one instruction**, where the cold arm is built by
  replacing the warm-up with a NOP rather than deleting it so the layout and every
  address-derived expectation stay identical. Expected counts are **numbers
  derived from the mechanism**, never thresholds: a straight-line single-pass
  block dispatches the entry slot exactly once, so warm is 1 fire / 0 declines and
  cold is 0 fires / 1 decline, with 1 install either way because the matcher runs
  at translation regardless.

**Why "reads zero" is not a control, measured rather than argued.** With verbosity
off the guest ran *perfectly* — the full six-transfer advance — and reported zero
fires **and zero installs**, so an install marker does not rescue that case
either; and a program whose pc never reaches the block also reads zero. Both are
indistinguishable from a dead fold if a row only counts absences. So every arm
asserts three things together: the verbosity echo, an execution witness (`r0`/`r1`
advanced by the full six transfers, which holds folded *or* not and therefore
proves the program ran without presuming the fold), and the exact decline count.

**The improvement is visible in a single measurement.** On a build with **only**
`netbsd_copyin`'s arming disabled, `A fold copyin quiet` still reads **ok** while
`A fold copyin cold` goes **red** — the vacuous row and its live replacement side
by side, on the same run. Measured **5 of 8**, red at exactly the three copyin
rows with copyout's four green, and the `install 0` signature naming the cause as
a matcher decline rather than a guard decline.

**A source-derived prediction that would otherwise have cost a false failure:**
`copyout`'s warm-up must be a **store**. A load sets the user-page bit but leaves
the store mapping empty, so the fold declines `no-page` instead of firing and the
healthy build fails its own row. A review seat derived that from the handler
reading the store array; the measurement confirms it, and the source comment now
says so where the next reader will look.

Gate 14 grows 4 checks. `xchg` and `scanc` still have markers without rows and
remain queued — with their measured constants, including that `xchg`'s negative
control is a **matcher** decline (install 0), a different signature that must not
share an expected shape with these, and that `scanc` needs a trailing sentinel
because its result register reads zero in every arm.

## One-hundred-and-fifth round (#359) — a fold that copied half the bytes passed every check in the gate

Harness-only: no emulator source changes. It closes a coverage hole that was
**measured, not suspected**.

- **#359 (`regress/arm_memcpy_probe.py`, `regress/gate_arm.sh`)** — five rows that
  read the **destination bytes** of the `netbsd_memcpy` fold, with the copy
  destination pre-filled with a sentinel (`0xbaadf00d`) so a word the fold never
  wrote is unmistakable rather than indistinguishable from zeroed RAM.

  **The hole.** A build whose fold called `memcpy` with **16 instead of 32** — same
  iteration count, same register advance, **half the bytes moved** — passed the
  committed memcpy probe **12/12** and the whole of gate 14 at **243 checks**.
  Nothing in the suite could see it, and the reason is structural rather than an
  oversight: `r3/r4/ip/lr` are published by a *direct page read that bypasses the
  fold's `memcpy` call* (that is #354's own design, and correct), and `r0`/`r1`
  advance unconditionally. So every register this gate asserts is right on a build
  that moves the wrong bytes.

  **A count-based row would not have closed it either.** The round that was
  originally planned here would have asserted reported iterations × 32 against the
  register advance — which still holds exactly when the copy size shrinks. That is
  worth recording, because the count row was the plan until a seat measured the
  mutant and found the count blind to it.

  Measured, healthy against mutant: **17/17** and **15/17**, red at exactly
  `1it dst w6` and `2it dst w14`, both reading the sentinel where a source word was
  owed. Gate 14 goes **243 → 248**.

  **They are PIN, not DISC,** and the distinction matters: the genuine
  `ldmia`/`stmia` moves the same bytes, so the destination is identical folded or
  not. These rows do not discriminate fold from no-fold — they discriminate a
  **broken copy**, which is a different axis from everything else in the gate.
  `2it dst w9` deliberately **passes** on that mutant, because it lies in the first
  16 bytes of the second iteration, which is still copied; keeping both `w9` and
  `w14` is what lets the row set say *which half* of the copy failed rather than
  merely that something did. The tail row asserts the sentinel **survives** at word
  8 after a one-iteration copy, catching the opposite mistake — a fold that writes
  past what it was asked to.

**A probe defect was introduced and fixed during authoring, recorded because its
symptom is misleading.** The original teardown sat between the register dump and
the new destination dump, so it killed the emulator before the second dump ran and
every destination row scored DEAD — which reads exactly like a dead fold rather
than like a broken probe. The teardown now follows both dumps.

**Measured facts about this fold that the round did not need but should not lose.**
A page-aligned multi-page copy never bails, because `(addr & 0xfff) + 32 > 0x1000`
is false at the last in-page offset (`0xfe0 + 32 == 0x1000` exactly), so an
8160-byte two-page copy is **one dispatch and one marker**; a 32-byte-misaligned
copy bails once per crossing and the deficit is exactly 32 bytes per bail, because
each bail delegates one genuine **uncounted** iteration. The general identity is
therefore `32 × (reported + bail delegations) == advance`, not the simpler form.
The fold reads `host_store` for its **source** page as well as its destination, so
a copy whose source has never been stored into never folds at all — measured, 255
of 255 iterations running genuinely. [#385 precision: the operative condition is
"never **warmed by any data access**" — on the MMU-off rigs a source page warmed by
a *load* alone is already in `host_store` (`ok-1 == 1`, the #382 mechanism), so
"never stored into" overstates; and "a read-only source page is NULL in host_store"
is an MMU-on-only property. The closing "255/255 genuine, source flag clear every time"
record is UNRECONCILED under this mechanism: a fully-cold source should SELF-WARM on the
first delegated iteration (the no-page bail runs the real ldmia via bdt_load → memory_rw,
which inserts), predicting ~1 genuine + 254 folded. Not settleable by reading —
re-measurement queued; until then treat the 255/255 as unexplained, not as confirmation.]
And the debugger's `put w` **does** populate
that array, which is why the committed probe folds with no explicit warm-up; that
had previously been recorded as *not established*.

**Deliberately still open, and named rather than implied:** the `copyin`/`copyout`
bail and install markers, the warm-up A/B rows, and rows for `xchg` and `scanc`.
Pass 1 measured that a "reads zero" negative control is **unsound on its own** — a
session whose verbosity raise silently failed reads zero markers while the program
ran perfectly correctly, and an install marker does not rescue it — so those rows
need the bail marker to become live statements about which guard ran. They are a
separate round rather than a half-finished part of this one.

## One-hundred-and-fourth round (#358) — five folds were doing work no test could see, and the last round removed the only witness

Five ARM instruction combiners produce results **identical** to the guest
sequences they replace — same registers, same addresses touched, same
instruction billing. That identity is the goal of several previous corrections,
and it has a cost nobody had written down: a harness row asserting a fold's
result **passes whether or not the fold ever fires**, so a broken matcher or
arming condition would delete the coverage silently with every row still green.
This project already calls that vacuously green and treats it as worse than no
row.

- **#358 (`cpus/cpu_arm_instr.c`)** — DEBUG-gated fold-fired markers for
  `netbsd_copyin`, `netbsd_copyout`, `netbsd_scanc`, `xchg` and `netbsd_memcpy`,
  in the existing `debugmsg_cpu(cpu, SUBSYS_CPU, name, VERBOSITY_DEBUG, …)`
  shape, deliberately **not** pre-gated with `ENOUGH_VERBOSITY()` so
  `breakpoint subsystem cpu` still catches a fold in flight.

  **#357 is what made this urgent rather than tidy.** Until last round the
  load/store template masked its base writeback while these folds did not, so an
  unaligned base read `r0 = 0x10019` folded against `0x10018` genuine. That
  one-bit difference was the *only* witness that `copyin`/`copyout` fire. #357
  corrected the template — the folds were right all along — and the detector went
  with it. Both folds also had **no harness rows of any kind** before this round.

  **Placement is the whole correctness argument.** For `copyin`, `copyout` and
  `scanc` the marker sits *after* the last bail-out, because those bail-outs
  delegate the first instruction to the genuine handler and return without
  setting `next_ic`, so the rest run genuinely too — a marker before one would
  report a fold that did no folding. `scanc` needs care: its second bail-out is
  reachable *after* the first passes, since the table address is computed from
  the byte just loaded, so a marker between them would fire on a call that wrote
  no guest state. `memcpy` is the opposite shape — both of its bail-outs are
  **inside** its loop — so it counts iterations, summarises once at the normal
  exit, and emits a **guarded** marker before each mid-loop return. That guard
  exists for **truthfulness, not flood control**, and must not be confused with
  the information-content guard an earlier round added to `strlen`: a
  summary-only marker would under-report every page-straddling copy (a 1 MB copy
  bails about 512 times), while an unguarded one would over-report the zero-work
  entries at page ends.

  **Flood control is split, and the rejected option is the interesting one.**
  `memcpy` summarises, because it has a real loop, so one **dispatch** emits one
  line however many iterations it folded: a copy that never straddles a page is a
  single dispatch and therefore a single line, while a straddling copy costs
  roughly one line per crossing, since the bail runs one genuine iteration and the
  back-branch re-dispatches the slot. (An earlier draft of this block, and of the
  source comment, said "one line per call by construction" — false for exactly the
  straddling case described two sentences later, where a 1 MB copy bails about 512
  times. A review seat caught it. The flood conclusion survives: lines track
  crossings, not iterations.) The other four
  have no loop to summarise and no natural information-content guard, so the
  volume is accepted and the rows copy blocks rather than megabytes. A **static
  first-N latch was rejected** on this project's own terms: it would gate the
  breakpoint path as well, so `breakpoint subsystem cpu` would die after N folds
  — the exact field capability the no-pre-gate convention exists to preserve.

  **`netbsd_memset` deliberately gets nothing.** It is dead: its arming for the
  iword `0xcaffffed` is unconditionally overwritten by the compare-and-branch
  catch-all, because that iword's condition field is in the catch-all's list and
  no `break` separates the two sites. A marker there could never fire, and this
  round will not ship an instrument that cannot be exercised. The 17
  compare-and-branch micro-folds are excluded for a different reason: a marker
  per compare would make raised verbosity unusable for everything else,
  **including the new rows** — the instrument would destroy its own channel.

**Measured, and one measurement overturned a review seat.** The folds *do* fire
on `testarm`, established on the pre-#357 snapshot where the old detector still
works (`0x10019` folded against `0x10018` under `-J`) and **deterministic across
5 consecutive runs**. The marker then discriminates on the new build: 1 line with
combining on, 0 under `-J`, with the verbosity echo confirmed in both — so the
zero is a real absence rather than a silently failed verbosity raise.

**A MARKER-FREE INSTRUMENT DOES EXIST, and this round's first framing was wrong
about that.** The design claimed the test machine's instruction counter could not
detect firing for any of these folds because each bills exactly. The billing is
exact; the conclusion does not follow. The run loop advances its counter by a
fixed amount per **batch of 120 dispatches** and only tests the batch limit at
those boundaries, so a fold — which changes instructions-per-dispatch — shifts the
**quantum**, and `ninstrs` lands elsewhere. Measured on the committed binary with
no source change and no marker, a guest reading the counter either side of a
copyin block: **0xabef with combining on against 0xa1b8 with `-J`**, reproducible,
and discriminating across block counts from 10 to 60. The broken-arming build
reads `0xa1b8`, agreeing with `-J`, which is the control. The unfolded reading is
`120 × 345` exactly, so the signal is quantisation rather than a billing error.

That witness is recorded here as the round's **pre-fix reproduction**, and
deliberately **not** turned into a gate row: it pins emulator internals — the
batch limit and the 120-dispatch unroll — rather than an architectural value, so a
future dyntrans change would silently rewrite it, and it has to be re-checked per
row (one shape collided, reading the same value folded and not). So the honest
position is not "no alternative exists" but "the alternative was measured and
rejected as too brittle for a row", which is a different and better claim. It also
means the round was **not** forced into an inverted order after all.

**And the `step` hazard this round was warned about is refuted as stated, with
something stronger in its place.** The concern was that an already-installed fold
would still execute under `step`, printing its marker at default verbosity through
the gate bypass. Measured: it does not — **stepping onto a fold slot re-translates
it uncombined**, so the step executes a plain instruction and no marker appears at
any step. That also explains this round's own earlier step-pc measurement, which
showed `pc + 4`: the mechanism is not "a breakpoint suppresses the fold" but
"stepping un-folds the slot". The correct warning is therefore sharper than the
original: a row must never drive the guest with `step`, because it would measure
the genuine sequence **while believing it measured the fold**.

**The breakpoint matrix, measured, because it is a booby trap for row authors.**
A breakpoint *after* the sequence gives one matcher install and seven folds over
eight passes. A breakpoint *inside* the loop gives **eight installs and zero
folds** — the matcher re-installs every pass and the fold never runs, so the row
reads exactly like a dead fold on a healthy binary. With read-ahead off (any
breakpoint present) the fold count is always `passes − 1`, because the install
lands after the entry slot has already dispatched once. Every row's expected count
must be written as a number derived from that rule rather than as "greater than
zero". This is also direct evidence for the separate open item about combiner rows
never exercising the read-ahead install path.

**Gate 14 grows 6 checks (237 → 243)** via a new `arm_fold_marker_probe.py`
carrying a `fires`/`quiet` pair per fold. The `fires` row demands the marker
**and** the verbosity echo **and** the six transferred values, so it cannot pass
on a printed line alone, and `copyout`'s row asserts the stored **memory** so a
future permutation regression stays visible. The `quiet` row asserts silence at
default verbosity and must never be rewritten to drive the guest with `step` —
though for a sharper reason than first written. The original worry was that
single-step **bypasses** the verbosity gate, so a stepped session would print
markers at default verbosity and fail the row for an unrelated reason. That gate
bypass is real in the code but the scenario is unreachable, because **stepping
onto a fold slot re-translates it uncombined**, so no marker is produced at all.
The true hazard is worse: a stepped row measures the **genuine sequence** while
appearing to measure the fold. The rows are free-running by necessity, per the
measurements above.

**Non-vacuity is proven per fold, not per round.** On a scratch tree built from
this exact source with **only** `netbsd_copyin`'s arming disabled: **3 of 4, with
exactly `A fold copyin fires` red** and `copyout`'s rows still green. So each row
tracks its own fold's arming rather than combining in general, which `-J` alone
could not show.

**Three probe defects of my own, recorded because each would have produced a
confident wrong conclusion.** The first step-pc probe put its breakpoint *on* the
entry slot — the case a seat had explicitly flagged as self-defeating, since the
breakpoint path re-marks its own slot for retranslation and the matchers test
`ic[i].f`, so a fold can never install there; it reported "genuine" for the wrong
reason. With the destinations left unzeroed it also showed all six registers
loaded from a *single* genuine load, which were pass-1 leftovers. And the first
arming break replaced the assignment with a comment, leaving a **dangling `if`**
that swallowed the adjacent `copyout` arming and killed both folds — one real
reason and one artifact. The break is now done by making the iword test
unsatisfiable, which preserves the statement structure.

**Scope stated plainly rather than implied: `xchg`, `scanc` and `memcpy` received
markers but no rows this round.** Their programs already exist in committed
probes, so adding marker assertions is mechanical, and it is queued with the
wider vacuity inventory — which also records that three folds had no rows at all,
that the gate's own text admits two `xchg` rows and all twelve `memcpy` rows
cannot distinguish folded-and-correct from not-folded-and-correct, that all seven
`strlen` rows are vacuous with respect to *firing* because an unfolded 16 KB walk
lands inside both asserted instruction bands, and that `netbsd_idle`'s two path
rows pass without the fold while the flag named in the source as its detector is
asserted by no row.

## One-hundred-and-third round (#357) — the load/store template masked the base writeback, so a post-index loop could not advance

`cpu_arm_instr_loadstore.c` is a macro template `#include`d once per variant to
generate every ARM single-register load/store — 8 p/u/w files × 20 addressing
forms. It computed one address, **masked it for alignment, and then wrote the
base register back from the masked value.**

- **#357 (`cpus/cpu_arm_instr_loadstore.c`)** — the writeback is computed from
  the UNMASKED address. ARM ARM DDI 0100I **A5.2.8** (immediate post-indexed) is
  `address = Rn` then `Rn = Rn + offset_12`; **A5.2.5** (pre-indexed) is
  `address = Rn + offset_12` then `Rn = address`. Both read the raw `Rn`, and
  **A2-43** puts the truncation inside `Memory[<address>,<size>]` — on the
  address sent to memory, never on the register. Where the manual really does
  force an address it says so plainly (LDC "ignores the least significant two
  bits of the address"); it never says anything comparable about a base
  register. A5.2.9/A5.2.10 (register and scaled offsets) and A5.3.6 (halfword)
  are the same shape, and **A4.1.31** makes `ldrt`/`strt` inherit A5.2.8
  unchanged ("the addressing mode is the same in all other respects"). The fix
  keeps the unmasked value in `wb_addr` and masks only the copy handed to
  memory: four sites, two per function, plus one guarded declaration each.

  **The reachable symptom is not a wrong value, it is a loop that stops
  advancing.** The masked writeback latches the base's low bits after a single
  iteration: the map `b → (b & ~(d-1)) + offset` drives the residue to
  `offset & (d-1)` and then holds it there, so from the second iteration onward
  the loop advances by exactly **`offset & ~(d-1)`** — the offset truncated down
  to a multiple of the access size. When the offset is *smaller* than the access
  size that advance is **zero** and the base becomes a **fixed point**: base
  `0x10001` masks to `0x10000`, plus 1 is `0x10001`, the value it started from.
  Measured on the committed build, `ldr r1,[r0],#1` ran ten times and left `r0`
  at `0x00010001` where the architecture gives `0x1000b`; entering the same loop
  **aligned** wedges too, reaching the fixed point after one step instead of
  `0x1000a`. The halfword form wedges identically (offset 1 < size 2). Nothing
  about this is guest-specific.

  *An earlier draft of this block claimed any non-multiple offset produces a
  fixed point. A review seat caught that as too broad and it was wrong: with a
  word access and offset 5 the loop advances by 4 per iteration, not 0. The law
  above was then checked against the iteration map rather than restated — it
  predicts both the fixed point at offset < size and the truncated advance
  above it, and it explains the aligned case, where the first step moves 1 and
  every later step moves 0.*

  **This round INVERTS two items the queue had recorded as fold defects.**
  `netbsd_cacheclean`'s `r[0] += r1` and `netbsd_copyin`/`copyout`'s `+ 24`
  write the base back unmasked, i.e. they already matched the architecture, and
  the template they were measured against was the one that was wrong. The two
  queued "mask the base on entry" fixes are **cancelled**; shipping them would
  have moved the emulator away from real hardware to agree with a local
  shortcut. The general lesson, now recorded twice: *measured against the
  handler is not measured against the architecture.*

  **Corroboration from inside the emulator, which is what made the reading
  safe:** every other ARM writeback path already implements the unmasked model —
  `arm_pop`/`arm_push` write back the raw stepped address, the generated LDM/STM
  masks its DATA pointer (`addr &= 0xffc`) but adds `4*n_regs` to the base raw,
  and all three folds are raw. This template was the sole outlier, so the fix
  makes the emulator internally consistent as well as architecturally correct —
  including the folds' own fallback into it on a page or user-page miss, which
  previously disagreed with the fold that called it.

  **Honest limit, recorded rather than glossed:** no silicon document states the
  writeback value for an unaligned post-indexed access. The SA-1110 manual and
  the ARM920T TRM both defer to the ARM ARM. The conclusion rests on the ARM ARM
  pseudocode being normative plus the absence of contradicting silicon text, and
  on the internal-consistency argument above — strong, but not independently
  silicon-confirmed. A panel seat added supporting evidence: the ARMv7 Base
  Updated Abort model writes back `Rn + offset` even when the access aborts,
  which is hard to reconcile with a masked writeback.

  **Completeness was established by enumeration, not by argument.**
  `reg(ic->arg[0]) =` occurs at exactly four lines in the single-register path,
  and `A__NAME_PC` plus every conditional variant (`__eq`, `__ne`, …) merely
  *call* `A__NAME`. Two seats suspected the PC special case held a third copy;
  it does not. LDRD/STRD are covered because the fast path delegates to the
  general function, which masks with `datalen - 1 == 7`. Negative offsets are
  covered because the sign is folded into `offset` before the address is
  computed, so `wb_addr + offset` already carries it — verified by measurement,
  not only by reading. A condition-failed access does no writeback at all,
  matching `if ConditionPassed(cond) then Rn = …`. The declaration is guarded
  `#if !defined(A__P) || defined(A__W)` because the offset-addressing
  instantiations have no writeback block and this file is included once per
  variant; a full ARM recompile produces **no warnings**.

**Gate 14 grows 17 checks (220 → 237)** via a new `arm_writeback_probe.py`, and
the row set is shaped by which of the four sites each row can actually reach —
a point a review seat raised and which changed the design. The fast path only
runs once the page is in the translation array, so a single-execution row
measures the **general** path and nothing else. Hence `:216` is covered by the
one-shot post-index rows and by iteration 1 of the ×10 rows, `:342` by
iterations 2+, `:213` by the pre-index one-shot, and **`:338` by one row alone**
— two passes with the base re-seeded each pass, because without the re-seed
pass 1 leaves an aligned base and the row has nothing left to discriminate.

> **✗ THAT SITE MAPPING IS INVERTED, and `#364` measured it.** A single-execution
> row measures the **fast** path and nothing else, because the probe's own `put w`
> seeding warms the page before the guest runs: `put w` → `store_32bit_word` →
> `memory_rw(CACHE_DATA)`, and insertion is gated on `!no_exceptions`. A marker at
> the top of `A__NAME__general` counted **zero** hits across all 17 rows, so **none
> of the general-path writeback sites claimed here was ever measured** — the
> re-seeded row reaches the fast pre-index site on **both** passes, not one. The
> 5-of-14 pre-fix sweep this round reports is therefore entirely a fast-path
> result. `#364` adds three `put b`-seeded rows that do reach `A__NAME__general`,
> but they are LOAD-DATA rows: the general-path **writeback** sites remain
> uncovered and are recorded in `OUTSTANDING_BUGS`. The re-seed itself is still
> load-bearing for the reason given above; only the site attribution was wrong.
Loads and stores are separate instantiations, so a load-only set could not see a
store-side regression: there is a store row. Register-offset forms are a third
family: there is a `ldr r1,[r0],r2` row. Swept against a snapshot of the pre-fix
binary: **5 of 14, with all nine DISC rows failing at exactly the predicted
masked values and all five PINs passing**; on the fixed build 14/14. The control
is the loaded-data row rather than a pass count, because `r1` starts at 0 and a
distinctive nonzero value proves the guest really executed and really loaded —
a wrong register field reads 0, and a row that accepts 0 accepts that mistake by
accident, which this harness has shipped before.

**Two rows deliberately absent, and one deliberately weakened.** No LDRD/STRD
row, overruling three seats that asked for one: A2.8 makes an unaligned
doubleword access UNPREDICTABLE prior to ARMv6, so every base that would
exercise the `~7` mask makes the instruction unspecified — covered by the fix,
not honestly assertable, and #355 already taught this project not to assert on
encodings the architecture declines to define. No row pins the **unaligned
loaded data**: this template masks without ROTATING where ARMv5 with CP15 A == 0
rotates right by `8 * addr[1:0]` (A2.8, A4.1.23), so a row pinning the
unrotated `0x11223344` would be inverted by the round that fixes rotation — the
row would be rewritten by the change it exists to guard. A seat caught that; the
data row now uses an **aligned** base, where no rotation applies in any
architecture version. And the halfword row is labelled **DISC-M**: an unaligned
halfword load's data is UNPREDICTABLE (A4.1.28) while its writeback stays
defined (A5.3.6), so it asserts the base only and pins the pseudocode model
rather than a silicon mandate. Every other DISC row is a word form, i.e. in
mandated space.

**An encoding error was caught before the sweep, by disassembling every word
through the emulator itself.** `0xe4002001` is `str r2,[r0],#-1`, a *negative*
offset — with `L == 0` the U bit sits in the same nibble — so the store row
needed `0xe4802001`. Left unchecked it would have produced an unexpected value
and sent the round debugging the emulator instead of the probe. This is the
fourth incident of its class here, one of which was a committed gate row that
measured the wrong register for months.

**Recorded, not fixed:** the missing rotation on unaligned word **loads**, which
is queued separately for a reason worth writing down. A seat made the strongest
case for folding it in — leaving it out creates a window in which a future
*slow-path-only* rotation fix would make the two paths disagree on data, and the
folds fall back from fast to slow, so that window is exactly where a fold's
fallback would change the visible value. The same seat supplied the tie-breaker:
the rotation must be fixed in **both** paths at once, and the fast path
assembles bytes individually, so shipping a slow-path-only rotation that the
fast path silently undoes would be worse than shipping neither. Stores need no
change (A4.1.99: "Prior to ARMv6, STR ignores the least significant two bits of
the address. This is different from the LDR behavior") and unaligned halfword
loads are UNPREDICTABLE, so the item is LOADS-ONLY. Also recorded: CP15's A
(alignment fault) bit is decorative in this tree — `ARM_CONTROL_ALIGN` is read
only to be printed — while `cpu_arm.c:129` ORs it into the initial control
value, contradicting SA-1110 reset state, where alignment faults are disabled;
because A == 0 on real silicon, hardware rotates silently rather than faulting,
which is what makes the rotation reachable rather than an exception. And a
sibling question: PowerPC's update forms do `ra = ea`, so if `ea` is masked
before that assignment it is the same mistake in a sibling template.

**One consequence of the fix worth stating, since it changes a pattern rather
than a value:** bases can now *retain* their low bits across iterations, where
previously the mask made them self-healing after one step. Unaligned fast-path
accesses therefore become more frequent for such guests. Each still masks
per-size before indexing memory, and `page`/`is_userpage` are still selected
from the unmasked address — correct because an AND cannot carry into bit 12, so
`(addr & ~3) >> 12 == addr >> 12` and a masked access can never land outside the
page that was selected — so there is no new host access pattern, only more of an
existing one. Three seats checked that page argument independently.

**Measured, and it is the strongest result of the round: the fix REMOVED three
live fold/no-fold divergences.** With an unaligned base the pre-fix un-folded
loop produced `(base & ~3) + n·stride` while all three folds produced
`base + n·stride`. Measured fold against `-J` — gate 14's own architectural
oracle — before and after: `netbsd_cacheclean` `0x9141` vs `0x9140` → both
`0x9141`; `netbsd_copyin` `0x10019` vs `0x10018` → both `0x10019`;
`netbsd_copyout` likewise. All three now agree, and the folds still fire
(`cacheclean`'s stale `r2 = 0x77` witness is present in both columns). So this
change did not merely satisfy the manual, it made the emulator self-consistent
where it previously answered two different values for one program depending on
whether a combination happened. `COMBINE(netbsd_cacheclean)` places no alignment
precondition on r0, so that divergence was reachable.

**One consequence measured rather than predicted:** a base can now *stay*
unaligned across iterations, so a walk can cross a page boundary that previously
it could not. Ten `ldr r1,[r0],#1` from `0x10ffd` read the *same* word ten times
on the pre-fix build and never crossed; on the fixed build the base sweeps
in-page offsets `0xffd/0xffe/0xfff`, lands correctly in the next page, and logs
zero non-existent-address complaints. Worth stating for the next reader: the mask
applied to the value used to index the host page is load-bearing for **bounds**,
not only for architecture — it is what keeps `page[(addr & 0xfff) + 3]` inside
the 4 KB page when the unmasked in-page offset is `0xfff`. A later
"simplification" that lifted it would be a memory defect, not a cosmetic one.

Eight-seat panel, both passes, and it earned its keep in both directions.
Pass 1 was unanimous on the reading and changed the row set in three places.
Pass 2 was unanimous that the code is correct and complete — one seat proved the
guard is an *identity* rather than a lucky enumeration, since the writeback text
emits a statement iff `(P ∧ W) ∨ ¬P`, which is exactly `¬P ∨ W` — but it forced
five corrections to this round's own **record**: the overbroad fixed-point claim
above, a `0xffc` bound that is word-specific in a template also instantiated for
halfword and byte, four **stale numeric line cites** in a new comment (the diff
shifted the mask sites by 42 lines, and this tree already carries a warning that
numeric cites have gone stale twice in two rounds), a cross-file claim asserted
without citations, and an enumeration of "every other writeback path" that
omitted `X(strlen)`'s own base writeback. A comment that overclaims counts as a
defect here, so all five were fixed rather than argued.

One seat measured that the **unguarded** form of the local emits 72 warnings and
would have failed `gate_build`'s zero-warning check outright — the guard is
load-bearing for the gate, not tidiness. Another independently rebuilt the probe
in a private tree and reproduced the pre-fix numbers, which is a second
measurement rather than a second reading; its first attempt was contaminated by
the *shared* build tree while this round was rebuilding, producing 167 rows of
"FAIL" that were all dead sessions rather than wrong values — diagnosed
correctly, and a reminder that a seat measuring against `build/` is racing the
main loop. Seat health, recorded because it drifts: the Codex seat produced no
review in pass 1 (transcript ends mid-tool-trace after failed searches for the
manual) but answered in pass 2 and is the seat that caught the fixed-point
overreach; the DeepSeek seat inverted that, answering in pass 1 and returning an
**empty** response in pass 2 with 199 KB of hidden reasoning and no output text —
the known thinking-model failure mode. Neither is counted as agreement where it
did not answer.

## One-hundred-and-second round (#355, #356) — the strlen fold answered a question the architecture never asked, and never came up for air

`X(strlen)` folds `ldrb rY,[rX,#1]! / cmps rY,#0 / bne` into an internal byte
walk. Two corrections, found by the combiner-publication audit and each
reproduced on the committed build before anything was edited.

- **#355 (`cpus/cpu_arm_instr.c`)** — `COMBINE(strlen)` pinned the load's
  destination to r3 and its immediate to 1 but never required the base and the
  destination to DIFFER, so `ldrb r3,[r3,#1]!` folded. The genuine writeback
  lands after the load, so r3 ends up holding the ADDRESS and `cmps r3,#0`
  compares an address — never zero, so the loop runs on. The fold's condition
  tests its local copy of the BYTE and exits at the first NUL. Measured, read-
  ahead on: folded the walk exited (sentinel stored, r3 parked at 0x9103);
  under `-J` it never exited, r3 walked to 0x037a2557 and was still climbing.
  One term, first in the chain: `ic[-2].arg[0] != ic[-2].arg[2]`, which rejects
  exactly one iword (0xe5f33001) and cannot refuse a genuine strlen — a
  base==dest walk cannot traverse a string at all.

  **This is a self-consistency fix, not a wrong-answer fix, and the record
  should not claim otherwise.** ARM calls the encoding UNPREDICTABLE, so the
  fold's answer is not "wrong". What is wrong is that THIS emulator returned
  two different answers for one program, selected by whether the combination
  happened — and `-J` is gate 14's own architectural oracle, so the divergence
  was an oracle defect regardless of what the architecture permits. #342 is
  cited for the guard's SHAPE only; its `eor rX,rX,rX` case is well-defined ARM
  and produced a demonstrably wrong value, which this one does not.
  **The rejected alternative is recorded in the source:** making the HANDLER
  faithful instead (test the register after the writeback) would put the
  guest's genuine infinite loop inside one C call — an unkillable host hang.
  Failing the match leaves the guest spinning on real dispatched instructions,
  which stay interruptible.

- **#356 (`cpus/cpu_arm_instr.c`)** — the walk had no budget bound: it ran to
  the end of the string inside ONE dispatch. Two consequences, and the round's
  first framing of both was wrong until the panel measured them:
  - **Reachability was understated ~30x.** `n_translated_instrs` is an int
    reset once per `run_instr`, not per fold entry, and the walk is
    REPLAYABLE — twenty back-to-back walks were measured accumulating 983,080
    instructions into one int with no group boundary. So the signed overflow
    needs roughly **18-24 MB of non-NUL memory at the DEFAULT `-M 64`**, from a
    ~6-instruction guest program, in seconds — not the ~700 MB a per-entry
    reading suggests. Past overflow the `>= N_SAFE_DYNTRANS_LIMIT` test fails
    on a negative value, `cpu->ninstrs` can run BACKWARDS (guest-visible), and
    the arithmetic is UB under this project's own sanitizer sweeps.
  - **No tick is skipped** — `machine_run` decrements by a constant and
    discards `run_instr`'s return, so the earlier "no device ticks" wording was
    simply wrong. The real faults are an instructions-per-tick ratio distorted
    by up to ~6000x for one call, and a guest-triggerable host stall in which
    ^C, the console and the debugger are all dead.

  The budget test sits at the **bottom** of the existing do-while, which
  structurally guarantees at least one completed iteration. That is
  load-bearing, not stylistic: a top-of-loop `if (room <= 0) return;` would
  skip the ldrb and still fall through to the genuine cmps — the dispatcher
  POST-increments `next_ic`, so an untouched return resumes at ic[1] — and a
  guest arriving with r3 == 0 would then take the not-taken bne and leave its
  loop having never loaded a byte. That is a NEW divergence of exactly the
  class this round fixes, and `room <= 0` at entry is reachable — the dominant
  producer being this fold's OWN prior yield inside the same group, since the
  group's +120 lands *after* the group and so always leaves at least one unit
  at a group start; a sibling fold like `netbsd_idle`, which adds the whole
  limit in one go, is the other. On yield the fold sets `next_ic = &ic[0]` — where the guest's own
  taken bne goes — and bills `(n_loops * 3) - 1`, identical to the normal exit,
  so no second accounting constant exists. Because the loop is bounded,
  `n_loops * 3 <= room + 2 <= 8193` and neither the unsigned wrap nor the
  signed conversion is reachable, so the bound SUBSUMES a #350-style
  `min(add, room)` and only one of the two shipped. The `(int)` cast in the
  condition is kept regardless: without it a negative `room` promotes to ~4
  billion and the bound silently vanishes.

  The three existing billing paths were checked and are exact — normal `3n-1`,
  NULL-page delegate a bare `3n`, and now the yield `3n-1` — each plus the
  dispatcher's blanket 1 for the call.

**Two hazards this round's own work created, both caught by measuring seats and
both fixed here.** The yield marker's low-information tail is the STEADY STATE,
not a corner: measured with `-v -v` on a 64 KB walk, 2706 marker lines of which
2683 (99.15%) said "yielded after 1 bytes". The mechanism is the fold's own
prior yield inside the same group -- the batch limit is only TESTED at the
120-dispatch boundary, so once the budget is gone the rest of that group each
re-enter, do one byte and print. An `n_loops > 1` guard drops the tail and
leaves every genuinely long walk its big-chunk line. Three seats argued the
flood was self-limiting; the measurement settled it.
And **#355 itself opened a probe hazard**: because the aliased loop no longer
exits, it marches off the end of RAM, and every byte past it logs a warning --
164,668 lines / 12.0 MB into the pty in under a second, making the row's r3
host-speed-dependent. The alias session now runs with `-T` (halt on a
non-existent access): one warning, 132 bytes, deterministic, and the pre/post
discrimination is untouched. `-q` cannot be used for this -- `main.c` ignores it
whenever `-V` is given.

**Gate 14 grows 7 rows** via a new `arm_strlen_probe.py`, and the yield is
witnessed **without a clock**: the test machine's `mp` device exposes
`cpu->ninstrs` at 0x110000d0, and that counter is committed only when
`run_instr` returns, so a guest sampling it either side of a 16 KB walk reads
~0 if the walk never left one dispatch. Measured: **42714 folded vs 41400 under
`-J`**, both ending at exactly 0x14000, where the pre-fix build read **0**.
Every numeric row asserts a BAND, and the dependency on
`N_SAFE_DYNTRANS_LIMIT` (8191) and the 120-dispatch group is named in the probe
so a future change to either moves the bands deliberately rather than silently.
Swept against a binary built from the pre-fix HEAD: **3 of 7, failing exactly
the four discriminators**; on the fixed build 7/7, whole gate 14 PASS at 220
checks (was 210).

**The probe caught a defect in itself during authoring, which is worth
recording.** Its first forward-progress row asserted through a guest store
placed after the loop — a store #355 makes unreachable, so the row could never
PASS. That is the mirror of the row-that-cannot-fail this harness already
retires, and the fix (read r3 from the debugger instead) is noted in the
docstring. Two rows were also relabelled PIN → DISC after the sweep showed them
failing pre-fix; a PIN here must pass on both builds.

Eight-seat panel, both passes (Codex xhigh, agy, Kimi, Ollama
glm-5.2/deepseek-v4-pro/minimax-m3, Opus 5 and Fable 5 via the Agent tool).
Pass 1 reshaped the round three times — the UNPREDICTABLE justification, the
severity figures, and the spurious-exit hazard in the round's own proposed fix
— and supplied the cycle-counter instrument that turned a defect the brief had
called possibly-unwitnessable into a hard deterministic row. A four-way split
over the billing constant was settled by reading the dispatcher rather than by
vote, which also refuted one seat's claim that the existing `-1` was missing:
it was already there.

**Recorded, not fixed:** the signed-overflow EVENT itself stays
reasoned-not-witnessed (~716 MB of contiguous non-NUL memory is not honestly
gateable), with #350 as the family argument.

Harness: REGRESS_PASS, 15/15.

## One-hundred-and-first round (#354) — the memcpy fold moved the bytes but never published the registers

`X(netbsd_memcpy)` folds the NetBSD/arm memcpy loop —
`ldmia r1!,{r3,r4,ip,lr} / stmia r0!,{...}` twice, then `subs r2,r2,#0x20 / bge`
— into one `memcpy(dst, src, 32)` per iteration. It advanced r0/r1 and delegated
the `subs` (so the flags were already right), but it never wrote **r3, r4, ip,
lr**, which the architecture leaves holding the LAST 16 bytes loaded: the final
iteration's second `ldmia`. A guest that read any of those four after a memcpy
got its pre-loop value.

Reproduced first on the committed build, read-ahead ON (no debugger breakpoint,
so `COMBINE(netbsd_memcpy)` installs the fold ahead of execution — the path a
real guest takes), one iteration, source words seeded per 16-byte block:

```
r3 = 0x00000033   owed 0x000000b0     r0 = 0x00009220  owed 0x00009220  ok
r4 = 0x00000044   owed 0x000000b1     r1 = 0x00009120  owed 0x00009120  ok
ip = 0x000000cc   owed 0x000000b2
lr = 0x000000ee   owed 0x000000b3
```

- **#354 (`cpus/cpu_arm_instr.c`)** — the fold now publishes the four registers
  from `page_1 + (addr_r1 & 0xffc) + 16` on every iteration, so the final
  iteration's second block persists exactly as the architecture leaves it. Three
  details, each settled by the panel rather than by preference:
  - **Direct host read, NO byteswap.** This matches the handler the fold
    emulates (`multi_0x08b15018`, `tmp_arm_multi.c:595-599`: `addr &= 0xffc;
    r[k] = p[k]`, machine-generated with no `cpu->byte_order` test) and — the
    decisive argument — the fold's OWN page-cross / NULL-page bail-outs, which
    delegate to that same handler. A byteswap would have made an on-page memcpy
    leave different registers than an identical memcpy that straddles a page:
    a page-alignment-dependent register result, manufactured by the fix. So
    fold == handler == bail-out for every guest byte order. Big-endian ARM is
    not a configured machine here and the fold is `#ifdef HOST_LITTLE_ENDIAN`,
    so a BE-guest row would only re-document a pre-existing upstream LDM
    limitation; none was added.
  - **Published BEFORE the memcpy — and not because that makes overlap safe.**
    A review seat measured that claim false and it was corrected before commit:
    the real second `ldmia` runs AFTER the first `stmia`, so on a *forward*
    overlap it loads post-store bytes, which no placement around a single
    `memcpy` can reproduce (`dst = src+16` diverges either way). The actual
    reason is determinism — publish-after would read bytes a UB-on-overlap
    `memcpy` had just written, making the registers depend on the host
    `memcpy`'s direction and vector width, while publish-before is identical
    in every case the fold is correct in (no overlap) and deterministic
    otherwise.
  - **Word-aligned base (`& 0xffc`)**, as the real handler masks — and this is
    load-bearing, not cosmetic, which the same seat established by
    measurement. ARM's LDM *ignores* `addr[1:0]` rather than requiring
    alignment, and the matcher matches code SHAPE not register values, so a
    guest with `r1 & 3 != 0` does fold: at `r1 = SRC+1` the masked read
    publishes what the genuine sequence publishes, while `& 0xfff` would have
    published byte-rotated words — the very bytes the fold's own unmasked
    `memcpy` writes. `(r1 & 0xfff) + 16 <= 0xff0` rules out a carry past bit
    11, so the publish address is bit-for-bit the real second `ldmia`'s.
    Bound: the entry guard gives `(r1 & 0xfff) <= 0xfe0` and masking only
    lowers it, so `+16..+31` stays inside the page.

**Gate 14 grows 12 rows** via a new `arm_memcpy_probe.py`, read-ahead ON with
`-J` (combining off) as the architectural control. The owed words are
full-width and distinct per register (`0x1a2a3a4X`), so an accidental byteswap
or a transposed register index is self-evident rather than hidden behind
single-byte values; the four r0/r1 rows are PINs that guard the advance the fold
always got right. Two loops: one iteration (owed the second `ldmia`'s block) and
**two** iterations (owed the final iteration's second block). Note `r2 = 0x40`
is *three* iterations, not two — `bge` continues on N==V regardless of Z, so the
`subs` reaching zero still branches; `r2 = 0x20` is the clean two-iteration
value.

Swept against a binary built from the committed HEAD (pre-#354): **4 of 12,
failing exactly the eight DISC rows** — r3/r4/ip/lr stale at their seeds on both
loops — and passing the four r0/r1 PINs. On the fixed build **12/12**; whole
gate 14 PASS at 210 checks. Build 0 warnings, all four trees byte-identical.

Seven-seat panel, both passes (Codex xhigh, agy, Kimi, Ollama
glm-5.2 / deepseek-v4-pro / minimax-m3, and Claude Opus 5 via the Agent tool).
The byte-order question was resolved BEFORE the panel by a read-only subagent
that traced the generated handler, then confirmed by every seat. Pass 1 was
unanimous approve-with-two-changes, both adopted: publish before the memcpy
(overlap ordering) and mask the base to a word (handler identity). One seat
implemented and measured the fix independently during review, and corrected the
brief's iteration arithmetic.

**Recorded, not fixed (pre-existing, out of scope for #354):** the fold's
`memcpy` uses exact byte offsets where both the real LDM and STM mask `0xffc`,
so an unaligned base diverges — an unaligned bail-out would be the honest fix;
and the fold reads its source through `host_store` where the handler uses
`host_load` (harmless: a read-only source page is NULL there and bails out to
the handler). Also worth an audit sweep: several ARM folds publish fewer
registers than the sequence they replace — `netbsd_cacheclean`'s known-stale r2
is the same species as this defect.

Harness: REGRESS_PASS, 15/15.

## One-hundredth round (#351, #352, #353) — the idle-loop fold skipped its writes, aliased a register, and hung the guest on a forward branch

`X(netbsd_idle)` folds the five-instruction NetBSD/arm idle loop
(`ldr rX,[rY] / teqs rX,#0 / bne out / teqs rZ,#0 / beq back`). Reproduced on
the committed build, three defects — and a fourth found by a review seat that
compiled variants rather than only reading:

- **#351 (`cpus/cpu_arm_instr.c`)** — on both fast paths (the idle handoff and
  the `rZ != 0` exit) the fold wrote NEITHER the load destination NOR the flags,
  though the loop it stands in for executes `ldr rX` and `teqs rZ` before either
  exit. Measured via translation read-ahead (which installs the fold before the
  `ldr` runs, so the destination is whatever it held on entry): the exit path
  returned `dest = 0x77` and `NZCV = 0x6` where the loop owes `dest = 0` and the
  second teqs's flags (`0xA` on this vector). The fix writes the destination
  first, then delegates the second teqs to the real dpi handler
  (`instr(teqs)(cpu, &ic[3])`, the netbsd_memcpy fold's own pattern — by name,
  because the combiner rewrote `ic[3]` to `teqs_beq_samepage`), and branches the
  idle/exit decision on the `ARM_F_Z` the delegation set. The stale
  `rZ = reg(ic[3].arg[0])` snapshot is DELETED, which makes a third defect
  impossible by construction:
  - the matcher pins `rZ != rY` but not `rZ != dest`, so a loop whose second
    teqs aliases the load destination was accepted; the fold read the stale
    destination and EXITED where the architecture idles. Writing the destination
    before the delegation reads it (now `0`) idles correctly. This is an ORDERING
    requirement on the handler, not a matcher guard — a pass-1 reproduction that
    concluded the alias was harmless was wrong, an artifact of its own debugger
    breakpoint (see the instrument note below); the defect is live under
    read-ahead. The store of `rX` is safe ONLY because `rX` is provably 0 here
    (a raw host word, no byte-swap); the comment says so, and any future
    non-zero fast path must byte-swap first.
  The exit path also bills the four instructions it stood in for
  (`n_translated_instrs += 4`).

- **#352 (`cpus/cpu_arm_instr.c`)** — a fold-fired marker
  (`debugmsg_cpu(SUBSYS_CPU, "netbsd_idle", VERBOSITY_DEBUG, ...)`) on the EXIT
  path ONLY. #351 makes that path architecturally transparent, so the marker is
  gate 14's fold-fired detector there. The idle path is deliberately NOT marked:
  an idling guest re-enters it ~2000×/s (`emul.c` sleeps 500 µs between wakes),
  and it needs no marker because `wants_to_idle` — set nowhere else on ARM — is
  already a fold signal. Not pre-gated with `ENOUGH_VERBOSITY()`, per the #278
  convention, so `breakpoint subsystem cpu` can catch a fold in flight.

- **#353 (`cpus/cpu_arm_instr.c`)** — the matcher never pinned the beq's TARGET,
  so a FORWARD `beq` (any same-page target) matched and `X(netbsd_idle)` treated
  a non-loop as an idle loop and HUNG the guest — measured on the committed
  build, pc parked at the fold slot, the real branch target never reached, no
  guest code able to change `rZ` or the memory word to break out. Higher
  severity than the flag/register defects, and #351 alone does NOT fix it. The
  matcher now requires `ic[0].arg[0] == (size_t)(&ic[-4])` — `b_samepage__eq`
  carries its taken target in `arg[0]`, so the loop-back beq targets the `ldr`
  at `ic[-4]`. Verified: the genuine backward-beq loop still folds and idles; a
  forward beq now reaches its target.

**Instrument correction (the reason two of these were invisible before).** Every
combiner witness in `arm_flags_probe.py` drives the guest with a debugger
`breakpoint`, and translation read-ahead is gated on
`cpu->machine->breakpoints.n == 0` — so a breakpoint turns read-ahead OFF and
the fold is only ever installed by the two-pass EXECUTE path, where the real
`ldr` pre-writes the very register the alias defect depends on. Real guests set
no breakpoint and take the read-ahead path, where the fold installs before the
`ldr` runs. The probe's comment asserting "a single forward run cannot work
either, however it is driven" was a false law; it is corrected. The new
`arm_idle_probe.py` runs every row with NO breakpoint (read-ahead ON) and `-J`
as the architectural neutralizer — the only way defects (c) and (d) can be
witnessed. Gate 14 grows by 9 rows (now 195 checks); swept against the pre-fix
HEAD (`704036e`) the idle probe scores **2/9, failing exactly the seven DISC
rows** (exit dest 0x77, exit flags 0x6, idle dest 0x77, idle flags 0x8, `alias
exits` 0x55, `target reached` deadbeef = hung, `fires` = no marker) and passing
the two PINs; on the fixed build **9/9**. Build 0 warnings, all four trees
byte-identical.

Seven-seat panel, both passes (Codex xhigh, agy, Kimi, Ollama glm-5.2 /
deepseek-v4-pro / minimax-m3, and Claude Opus 5 via the Agent tool). Pass 1
reshaped the round three times: it refuted a hypothesized fourth defect
(register-alias-as-matcher-gap → subsumed by #351's ordering), then a seat that
compiled variants overturned the "alias is harmless" reproduction (read-ahead
artifact) and found the forward-beq guest hang (#353) that no reading had
surfaced. Pass 2 on the diff was unanimous GO after one fix: a seat found the
new probe's PTY wait/recovery was not gate-robust (whole-buffer prompt match, no
dump retry, a ^C-recovery failure could hang ~60 s), so `session()` was rebuilt
to mark the buffer before every command, require a prompt past that mark,
terminate on failed recovery, and retry the dump — the round-99 pattern the new
probe had not inherited. Two seats independently reproduced the 2/9-vs-9/9 split
by compiling both binaries.

Still open on this handler, recorded in OUTSTANDING_BUGS: the idle path bills
`N_DYNTRANS_IDLE_BREAK` and is not re-examined here; the ARMv6-media / non-idle
combiner divergences (netbsd_memcpy) remain their own rounds; and the broader
read-ahead-blind-spot audit of prior combiner rounds is filed separately.

Harness: REGRESS_PASS, 15/15.

## Ninety-ninth round (#348, #349, #350) — the folds learned their exit flags, and the detector the fix would blind was rebuilt in the same change

Both cache-clean folds stand in for a loop whose final instruction is a
`subs`, and neither wrote any of the four flags that subtraction owes.
Measured on the committed build with the two-pass free-running driver, the
flags seeded by a `cmp` that re-runs on every pass and read back by the
guest's own `mrs`:

```
variant 1  ctr 0x20   armed: NZCV = seed (9)   neutralized: 6   <- Z|C owed
variant 2  ctr 0x40   armed: NZCV = seed (9)   neutralized: 6
variant 2  ctr 0x30   armed: NZCV = seed (6)   neutralized: 8   <- N owed
```

("neutralized" = the arming iword replaced by a nop, so nothing combines.
Registers agreed armed/neutralized in every row — #345/#346/#347 hold; the
flags were the last guest-visible divergence.)

- **#348 (`cpus/cpu_arm_instr.c`)** — both handlers now leave r1 at the
  final iteration's operand and delegate the last subtraction to the real
  dpi `subs` — the netbsd_memcpy fold's own pattern — whose arguments the
  matchers already pin to (r1, #0x20, r1). For variant 1 every terminating
  counter's final operand is 0x20 (nonzero multiples end 32 -> 0; the
  r1 == 0 wrap ends on the same operand after 2^27 iterations whose 2^32
  bytes of base advance return r0 to itself). For variant 2 the operand is
  `before_last = r1 - ((n-1) << 5)`, which lies in [0, 0x20] for every
  uint32 counter — 0 for r1 == 0, r1 & 31 for non-multiples, 0x20 for
  nonzero multiples — so the stored register result is byte-identical to
  #347's closed form and V is structurally 0: the dpi overflow rule needs a
  negative operand, and neither `before_last` nor 0x20 can be one. A zero
  exit answers Z|C, a borrow exit answers N, both measured against the
  un-combined loop. This is not a simulation of the flags: it is the real
  final iteration, executed by the real instruction; the only thing
  delegated away is the loop.

- **#349 (`cpus/cpu_arm_instr.c`)** — a fold-fired marker,
  `debugmsg_cpu(SUBSYS_CPU, ..., VERBOSITY_DEBUG, "combined N iterations")`,
  in both handlers. #348 makes the genuine variant-2 sequence
  architecturally transparent folded or unfolded, so gate 14's old control
  row — which proved the fold fired by reading the MISSING flags — dies
  with the defect it was built on, exactly as its own comment said it
  would. The marker replaces it: silent at default verbosity (the quiet
  rows pin that), visible under `verbosity cpu 3` (the fires rows, each
  carrying the echoed "3: DEBUG" as its own proof the level took), and
  deliberately NOT pre-gated with ENOUGH_VERBOSITY(), per the #278
  convention — a pre-gate would hide it under `-V step` and keep
  `breakpoint subsystem cpu` from firing on it. One review seat required
  the pre-gate in pass 1 and withdrew it without reservation in pass 2
  after reading the #278 comment, which a second seat had cited
  independently: for this site the catchability is load-bearing, since the
  marker IS the round's designed fold-observation channel.

- **#350 (`cpus/cpu_arm_instr.c`)** — variant 1's closed form terminated
  loops the architecture does not terminate: a counter that is not a
  multiple of 32 has an invariant nonzero residue, so its `subs` never
  reaches zero and the real `bne` loop runs forever, while the fold
  returned r1 = 0 and moved on. The matcher cannot refuse this — it runs
  at translation time and never sees r1 — so the HANDLER now bails out to
  the genuine pinned load handler whenever `r1 & 0x1f` is nonzero (the
  netbsd_memcpy bail-out shape; the fallback touches neither `next_ic` nor
  any register, so a data abort raised by the real load stands). The
  residue is invariant under the loop's own -0x20, so every re-entry bails
  too: the guest keeps its infinite loop, its real loads, its faults and
  its interruptibility. r1 == 0 stays folded — that loop terminates — and
  its marker and instruction accounting now use the honest n = 2^27 rather
  than the 0 that `r1 >> 5` reported. Both handlers also CLAMP the
  n_translated_instrs addition to the batch budget's remaining room: the
  billing reaches ~5*2^27, the limit (8191) is only tested per dispatch
  group, and the zero-counter fold is a fixed point (it leaves r1 == 0),
  so a two-instruction guest loop could otherwise drive the signed counter
  through overflow — the #169 class, sharpened by this very round and
  caught by a pass-2 seat. A #169-style bail would disable the fold for
  every counter above a few tens of KB; dropping the overshoot costs only
  the instruction statistics in that synthetic corner.

**Gate 14 goes 173 -> 190 rows** (the variant-1 block 7 -> 14, the
variant-2 block 8 -> 18, `A cclean2 still fold` retired). The new
discriminators: both `flags` rows (seeded `cmp r9,#0x80000000` = 0x9, so
every NZCV bit must move to reach the owed 0x6), `tail flags` (borrow
exit, seed 0x6 -> owed 0x8), `tail V` (the same borrow run seeded V=1,
pinning V's clearance on that exit), `zero flags` plus two register pins
(r1 == 0 is the one input where #347's `(r1 == 0 ||` disjunct is
load-bearing; an alternative closed form such as `(r1+31)>>5` fails
exactly there, and nothing had tested it), `fires` for both variants,
`nonmult`, and `zero n` — which reads the honest 2^27 off the marker text
itself, because a formula reverted to `r1 >> 5` reproduces every register
and flag and differs only in what it prints and bills. The #348 rows ride
a NEW 0x40-counter session because a review seat proved the existing
0x20 session could not fail against a fix that skipped the r1 preload —
at one iteration the live counter IS the preload value. `A cacheclean
fold r1` pins the genuine fold's counter result, unasserted since #345.
The probe's name column widened 26 -> 30 after a proposed name landed
exactly on the padded-column trap's width, and both pty argv lists gained
`-A`: under pty.fork() a CLICOLOR in the caller's environment would put
ANSI escapes inside the debugmsg line and silently fail every marker
grep — an environment-dependent FAIL that would have read as a real
regression.

Swept against a binary built from the pre-fix HEAD (`dea2fef`):
**181 of 190, failing exactly the nine new discriminators and nowhere
else** — the five flag rows at their seed values, both fires rows absent,
nonmult reading "fold", zero n reading "none". On the fixed build:
**190/190**, at 0 warnings, all four trees byte-identical.

**The #350 witness earned its own entries in the trap ledger.** Its first
draft planted a handler at the data-abort vector and expected the guarded
walk to fault at the top of RAM: measured FALSE — a read of non-existent
physical memory logs one host line per access
(`memory READ: from non-existant paddr=...`) and execution continues, r0
observed 4 MB past RAM top and still walking (which is also the live
proof the guard's fallback executes real loads: pc mid-loop, r0 in exact
0x20 strides, the residue invariant holding). The same draft compared a
dump string against "deadbeef" without byte-swapping — the little-endian
transposition the probe's own header warns about — and so read its own
sentinel's parity as a measurement. And its second draft's "live" verdict
was refuted by a pass-2 seat with a constructive counterexample: a broken
guard that returns WITHOUT calling the load also loops forever with the
residue invariant intact, but parks r0 at its phase-A value — so "live"
now additionally demands load progress. The per-access log line is filed
in OUTSTANDING_BUGS as a flood-class follow-up candidate.

Both passes ran the full six-seat panel (Codex xhigh, agy, Kimi, GLM,
MiniMax, Claude/Opus). Pass 1 (design): unanimous GO/GO-WITH-CHANGES;
it changed the round four times — the runtime guard (three seats, adopted
as #350), the honest zero count, the 0x40-counter session, and the
zero/tail-V rows — and one seat's claim that the r1 == 0 loop never
terminates was refuted by three others' proofs. Pass 2 (diff): three GO,
three GO-WITH-CHANGES, every required change adopted — the clamp, the
load-progress predicate, the `-A` flag, the zero-n row — except one:
numeric line citations for the arming/matcher sites, which had now gone
stale twice in two consecutive rounds (each round's own added lines
re-staled the previous fix), were replaced by symbol-anchored citations
instead of a third set of numbers.

Still open on these handlers, all recorded in OUTSTANDING_BUGS: variant
1's skipped load (stale r2 — kept deliberately as the fold detector
independent of the marker — plus the two consequences a review seat
sharpened: a folded run can never take the data abort or perform the MMIO
side effects the real loads could); both folds elide their MCRs, which
becomes visible the day cache operations are modelled; and the
netbsd_idle and netbsd_memcpy divergences found by #340's after-panel,
which are the next two rounds.

## Ninety-eighth round (#347) — the second cache-clean fold skipped a loop and updated nothing

`X(netbsd_cacheclean2)` replaced the five-instruction NetBSD cache-clean loop with
`n_translated_instrs += ((r[1] >> 5) * 5) - 1; next_ic = &ic[5];` and **nothing else**. It
skipped the two MCRs, the `add`, the `subs` and the branch, and left every guest register
exactly as it found it. That is wrong even for the sequence it was written for — unlike
variant 1, which at least performs `r[0] += r[1]; r[1] = 0`. On top of that its matcher had
the same shape-not-registers hole #345 fixed in variant 1: the two MCRs are pinned by exact
iword, but `add rX,rX,#32` and `subs rY,rY,#32` were tested only for `rn == rd` and an
immediate of 32, for **any** X and Y.

The premise had to be checked first, because the last round of this family turned on it:
`netbsd_memset`'s operands are pinned by the exact iwords its matcher demands, so there was
nothing to guard there. Here `instr(add)` and `instr(subs)` are the **generic** dpi table
entries (`arm_dpi_instr[]`, `cpu_arm_instr_dpi.c:72-74` — `arg[0] = &Rn`, `arg[1]` the
immediate, `arg[2] = &Rd`), selected by condition/opcode/S-bit alone. The registers really
are free.

Measured on the committed build with the two-pass free-running driver, `r0 = 0x9100`,
counter `0x40` (two iterations):

```
A cclean2 fold r0          00009100   owed 00009140   <- the genuine sequence
A cclean2 fold r1          00000040   owed 00000000   <- ...updated neither register
A cclean2 base r5          00009100   owed 00009140   <- add r5,r5,#32 folded anyway
A cclean2 base r1          00000040   owed 00000000
A cclean2 cnt r6           00000040   owed 00000000   <- subs r6,r6,#32 folded anyway
```

Every "owed" value is measured, not derived: the identical program with the first MCR
replaced by a nop, so that nothing combines. `cr7` is an unconditional no-op in this
emulator (`cpu_arm_coproc.c:209-215`), and a second neutraliser that instead perturbs only
the *second* MCR's opcode2 (`0xee070f56`, still `cr7`) returned identical values for all
three loops on both builds — so the substitution is not carrying the result.

- **#347 (`cpus/cpu_arm_instr.c`)** — the matcher now requires `ic[-2].arg[0] == &r[0]` and
  `ic[-1].arg[0] == &r[1]`, and the handler performs the update the fold stands in for.

**The closed form is not variant 1's.** This loop ends on `bhi` — `C && !Z` — so it exits
either when the `subs` reaches zero **or when the `subs` borrows**, and that second exit is
the one every counter that is not a nonzero multiple of 32 actually takes. The branch is
also at the *bottom*, so one iteration always runs and a partial tail costs a whole extra
one. Hence

```
n = (r1 == 0 || (r1 & 31) != 0) ? (r1 >> 5) + 1 : (r1 >> 5)
r[0] += n << 5;   r[1] = r1 - (n << 5);
```

which was swept against the un-combined loop for `r1` = 0, 1, 0x1f, 0x20, 0x21, 0x30, 0x40,
0x60 and 0x7f and agrees on all nine, folded and unfolded alike. `r[0] += r[1]; r[1] = 0` —
what the bug record proposed — agrees on **three** of those nine, `0x20`, `0x40` and `0x60`,
the only nonzero multiples of 32 in the set. Where it differs it is not close: `r1 = 0x30`
really leaves r0 advanced by `0x40` and r1 at `0xfffffff0`, where that form gives `0x30` and
0; `r1 = 0` really advances r0 by `0x20` and leaves r1 at `0xffffffe0`, where that form
leaves r0 alone. The 32-bit wraparound at `r1 = 0xffffffff` is correct by the same
arithmetic: `n << 5` truncates to 0, which is what advancing a 32-bit register by 2^32
bytes does.

**The control has to read the cpsr, not a register.** Once the closed form is right, r0 and
r1 are identical folded and unfolded — that is what "correct" means here — so no register
can show that the optimisation still fires, and an over-tight guard that silently disabled
it would pass every discriminator above. The one guest-visible difference left is that the
fold writes no **flags** though the loop ends on a `subs`: seeded N=1 by `cmp r9,#2`, the
folded run still reads N=1 where the real loop leaves Z=1 C=1. `A cclean2 still fold` pins
that, which means it pins a defect this round does not fix — deliberately and on the
record, the same trade #346 made with the stale load destination, and for the same reason:
it is the only fold detector available. It works only with a counter that is a nonzero
multiple of 32; any other value exits on a borrow and leaves N=1 too, which is the seed's
own value.

Two rows are neither discriminators nor controls. `A cclean2 base r0` and `A cclean2 cnt r1`
assert the sentinels 0x11 and 0x22 survive, and they pass on the pre-fix build as well —
they exist to catch the **opposite** error, a handler that now writes `r[0]`/`r[1]` by name
behind a matcher that still accepts any register. Without them the register guard could be
deleted and only rows that already pass would notice. `wrongcnt`'s r0 is deliberately not a
row: the architecture leaves `0x9140` there and an unguarded fold reading `r1 = 0x22`
computes `0x9140` too, so it can attribute nothing.

Gate 14 goes 165 → 173 rows. Swept against a binary built from the parent commit `be6ea08`:
**168 of 173**, failing exactly the five discriminators above and nowhere else, with all
three pins passing on both builds.

**Still open on this handler:** the flags, as above — the loop's final `subs` owes N/Z/C/V
and the fold writes none of them. Fixing it would also remove the only evidence that the
fold fires at all, so it needs a different instrument, not just a different line.

## Ninety-seventh round (#346) — the cache-clean fold ignored the stride its own arithmetic assumed

#345 checked the two registers `X(netbsd_cacheclean)` **writes** and stopped there. Two
review seats independently found that incomplete, and both were right: the load's own
remaining operands were still unchecked, and the first of them is a **stride**. The handler's
closed form `r[0] += r[1]` is arithmetic that is only true when each iteration advances the
base by 32 bytes, so the post-indexed immediate is part of the contract, not decoration.

Measured on the committed build with the two-pass free-running driver, on
`ldr r2,[r0],#4 / subs r1,r1,#0x20 / bne / mcr` — a loop of exactly the shape the matcher
accepts, with the registers #345 now requires:

```
A cacheclean imm4 r0       00009120   owed 00009104   <- base advanced by 32, not 4
A cacheclean imm4 r2       00000077   owed a5a5a5a5   <- the load was skipped
A cacheclean wrong Rd      00000066   owed a5a5a5a5   <- ldr r6,[r0],#32, r6 stranded
```

Every "owed" value above is not a derivation: it is the identical program with the MCR
replaced by a nop, so that nothing combines at all.

- **#346 (`cpus/cpu_arm_instr.c`)** — the matcher now also requires `ic[-3].arg[1] == 0x20`
  and `ic[-3].arg[2] == &r[2]`, the load's immediate and destination.

Eight times the real base advance, from a loop a compiler can emit — this is a live
miscompilation, not a degenerate encoding. `arg[2]` is pinned for a different reason: the
handler never performs the load, so a fold that fires on any other Rd strands that register
as well. That does not FIX the staleness, it confines it to the one register the NetBSD
sequence uses.

**The control row committed with #345 had to be rebuilt, and it was actively holding the
defect in place.** `run_cacheclean(use_r01=True)` built its "must still fold" loop with
`ldr r4,[r0],#4` — immediate 4, destination r4 — and asserted the FOLDED answer `0x9120`
for a program whose architectural answer is `0x9104`. It was pinning the miscompilation as
correct, and adding the immediate check would have failed it. It now runs the genuine
sequence out of the comment above `X(netbsd_cacheclean)`.

Rebuilding it surfaced the reason a naive control cannot work here: **for a real 32-stride
loop r0 cannot discriminate at all**, because the closed form is exactly right there — both
answers are `0x9120`, measured. The only value that separates folded from unfolded is the
load's destination, which the fold leaves stale. So the control asserts `r2 == 0x77`, its
seed, where the architecture leaves the fetched `0xa5a5a5a5`. That row pins a defect this
round does not fix, deliberately and on the record: it is the only evidence available that
the optimisation still fires, and an over-tight guard that silently disabled it would be
invisible to every discriminator in the gate.

Gate 14 goes 161 → 165 rows (four loops, each one field off the genuine sequence, so no row
can be satisfied by the wrong guard). Swept against a binary built from the parent commit:
**162 of 165**, failing the three rows above and nowhere else, with both controls passing on
both builds.

**Still open on this handler, both pre-existing, both already filed:** the load's
destination is never written (#346 narrows the blast radius to r2, it does not close it —
closing it means performing the final load, in a fold whose purpose is to skip loads); and
flags are never written though the loop it replaces ends on a `subs` reaching zero, which
owes Z=1 N=0 C=1 V=0.

## Ninety-fourth round (#345) — the cache-clean fold matched a loop's shape and ignored its registers

`X(netbsd_cacheclean)` replaces a NetBSD cache-clean loop with a closed-form update, and it
hardcodes `r[0] += r[1]; r[1] = 0`. Its matcher tested only the loop's **shape** — a
post-indexed word load, `subs rX,rX,#32`, a branch back to the load — and **never which
registers it used**. Any loop of that shape built on a different pair had r0 and r1 clobbered
and its own registers left untouched.

Measured with the two-pass free-running driver #340 built, on a loop using **r5 and r6**,
with r0 and r1 seeded to sentinels the loop never mentions:

```
A cacheclean r0 intact     00000033   owed 00000011   DISC   <- r0 was given r1's 0x22
A cacheclean r1 intact     00000000   owed 00000022   DISC   <- r1 was zeroed
A cacheclean still folds   00009120        00009120   PIN
```

- **#345 (`cpus/cpu_arm_instr.c`)** — the matcher now requires the load's base to be r0 and
  the counter to be r1, the two registers the handler actually writes.

This is the same species as #342's missing `a != b` and **worse in consequence**: that one
needed a degenerate encoding a compiler would never emit, while this fires on ordinary code
that merely happens to match the shape.

**The control row is doing real work here**, and it is the row that distinguishes this fix
from an over-tight one. A guard that was too strict would disable the optimisation
altogether — correct but silently slower, and invisible to the two DISC rows, which pass
either way. So the PIN runs a loop that genuinely does use r0 and r1 and asserts it **still
folds**: `0x9100 + 32 = 0x9120` folded versus `0x9104` unfolded. It reads `0x9120`.

Gate 14 goes 158 → 161 rows.

**Still open in this round:** the flag divergences that were originally filed —
`netbsd_cacheclean` and `netbsd_cacheclean2` never write flags though the loops they replace
contain a `subs` (the final one reaching zero owes Z=1 N=0 C=1 V=0), `netbsd_idle` skips both
TEQs without updating N/Z and never writes its guest destination register, and
`netbsd_memcpy` bypasses its LDMs without publishing the final r3/r4/ip/lr. All four are now
measurable with this driver; each needs its own NetBSD sequence reconstructed first.

## Ninety-sixth round (#344) — the negative multiply-adds were never decoded, and halted the emulator

Opcode 63's five-bit switch had cases for `FMSUB` (28) and `FMADD` (29) and **none** for
`FNMSUB` (30) or `FNMADD` (31), so both fell through to a ten-bit switch whose only arm is
`goto bad` — which sets `cpu->running = 0`. Two legal encodings, either of which let a guest
stop the whole emulator. The same halt class as #264/#309/#310/#326.

`PPC_63_FNMADD` and `PPC_63_FNMSUB` were not even defined; `PPC_59_FMSUBS` still isn't.

Gate 15 was already the measurement: both were pinned as **PEND**, with the probe's own note
that `fcmpo`/`fnmadd`/`fnmsub`/`fmadds`/`fmsubs` have *"no technical blocker at all and were
left out for round size alone"* — a record this round closes rather than a blocker it
disproves.

- **#344 (`cpus/cpu_ppc_instr.c`, `include/opcodes_ppc.h`)** — both encodings defined,
  decoded, and implemented, with their `Rc=1` forms via `FDOT`.

**The negation applies to the already-rounded result.** That is what the ISA specifies and it
is *not* the same as negating an operand: round-then-negate and negate-then-round can differ
under the directed modes. The FMA still ignores `FPSCR[RN]` here — recorded separately — so
the distinction is not yet observable, but writing it the other way would have to be undone
the moment it becomes so. FPCC describes the final result and is computed after the negation;
the invalid-operation causes are #343's and do not depend on the result's sign.

Gate 15 moves two rows PEND → FIXED (12/12 becomes 14 fixed / 10 pending). But "alive" only
proves the emulator survived — **a nop would pass that too** — so gate 13 gains two *value*
rows: `-(2×3+1) = -7` and `-(2×3−1) = -5`, which no nop and no un-negated implementation can
satisfy. 136 → 138 rows.

**Not done here:** `fmadds`/`fmsubs` remain undecoded — the single-precision forms need the
narrowing question that `fmuls`/`fadds` already have open against them, so aliasing them to
the double handlers would bake in a known divergence rather than close one. Book I's treatment
of a NaN result's sign under these two instructions is also not modelled, because this tree
collapses every guest NaN to the host NaN before arithmetic sees it — a gap recorded against
the whole FP path.

## Ninety-fifth round (#343) — the fused multiply-adds raised none of their exception causes

`#330` gave PowerPC arithmetic its invalid-operation causes, and `fmul` has called that
machinery ever since (`cpu_ppc_instr.c:1717`). The FMA handlers never did: they went straight
from operand conversion to computation and updated only FPCC. Measured on the committed
build, every cause row read `00001000` — the FPCC nibble alone, no cause bits, no summary
bits, nothing.

**An FMA cannot reuse `ppc_invalid_cause()`,** for two reasons. It returns a *single* cause,
and it abandons its operation-specific test at the first NaN — both correct for a two-operand
instruction and both wrong here. `ppc_invalid_cause_fma()` treats the three conditions as
what they are, independent:

- **VXNAN** — any of frA, frC, frB signalling.
- **VXIMZ** — the *multiply* is `Inf × 0`. This depends only on frA and frC, so a NaN
  **addend does not suppress it**: `Inf × 0` with an sNaN addend owes `VXIMZ | VXNAN`, the
  two-at-once case `cpu_ppc.c:1929` already documents and which no other instruction in this
  gate can exercise. That case is the reason the function exists.
- **VXISI** — the product is infinite *and* frB is an infinity that cancels it. `Inf × 0` is
  excluded first: there is no product for an addend to disagree with.

`fmsub` subtracts frB, so its addend's effective sign inverts.

Every **cause and summary** bit was derived from Book I before the code was written:

```
VXIMZ+VXSNAN fmadd    a1101000        <- the two-cause row
VXIMZ fmadd Inf-by-0  a0101000
VXSNAN fmadd sNaN     a1001000
VXISI fmadd Inf+-Inf  a0801000    clean fmadd Inf+Inf   00004000
VXISI fmsub Inf-Inf   a0801000    clean fmsub Inf--Inf  00004000
```

Those last four are a **2×2 on identical operands**: the addend that makes `fmadd` invalid is
exactly the one that makes `fmsub` clean, and vice versa. A fix that forgot `fmsub` negates
its addend fails one diagonal; one that negated unconditionally fails the other. What they do
**not** prove is *which* internal sign was flipped — negating the product and negating the
addend give the same Boolean for this predicate, so the rows pin that subtraction reverses
the cancellation relation, nothing finer.

**These are not Book I-complete bytes, and the first draft of this entry claimed they were.**
They carry this fork's four-bit FPCC model, not the full five-bit FPRF: Book I would also set
the class bit, making the invalid rows `a1111000` / `a0111000` / `a1011000` / `a0811000` and
the infinite clean row `00005000`. That FPRF gap is a pre-existing, separately recorded
divergence — the probe already says so about its other arithmetic oracles — so the rows are
right for what this tree currently models, and the *claim* was what needed narrowing.

- **#343 (`cpus/cpu_ppc_instr.c`)** — `ppc_invalid_cause_fma()` inside the existing
  `PPC_FP_CLASSIFY_INCLUDED` guard, wired into both handlers with the subtract flag.

**Five rows were added after review**, because the first table left whole clauses of the
helper unexercised — a helper that got any of them wrong would still have passed: `0 × Inf`
(the *either-order* half of VXIMZ), an sNaN in **frC** (the "any of all three operands" half
of VXSNAN), `Inf × 0` with a **qNaN** addend (general non-suppression, where the two-cause row
only shows the sNaN case), `Inf × 0` with an **infinite** addend (the direct discriminator
that VXISI is excluded once the multiply is invalid), and a **negative multiplier** (the
product-sign XOR, which an implementation reading only frA's sign would get wrong).

Gate 13 goes 123 → 136 rows (92 DISC / 44 PIN). The three clean PINs are what show the fix
raises causes only when owed — a change that started raising them unconditionally would pass
every DISC row and fail all three.

One naming note: the macro is historically `PPC_FPSCR_VXNAN`, but Book I and every other row
in this gate call the status bit **VXSNAN**, so the new rows use that.

**Still open in this item:** `fnmadd`/`fnmsub` are not decoded and halt, and FPSCR `NI` is
defined but never consumed. Both are their own rounds; the negative forms in particular must
negate the **already-rounded** result, which is not the same as moving the sign inside the
FMA.

## Ninety-third round (#342) — the XOR-swap fold had no "two distinct registers" guard

The combiner recognises the classic XOR swap — `eor a,a,b` / `eor b,b,a` / `eor a,a,b` —
and replaces it with `X(xchg)`, which exchanges the two registers directly. That is only a
swap when the two registers are **distinct**. With `a == b` the very same three encodings are
`eor rX,rX,rX` three times over, and each of those **zeroes** `rX`; `X(xchg)` exchanges `rX`
with itself and leaves it untouched. Nothing in the match excluded it.

Measured on the committed build with #340's two-pass free-running driver — the only
instrument that reaches a folded handler, since combining is disabled under `single_step`
and the combiner rewrites `ic[-2].f` while `ic[0]` is being translated:

```
A xchg same-reg zeroes   0000005a   owed 00000000   DISC
A xchg swap control      0000005a        0000005a   PIN  ok
```

`r0` is re-seeded to `0x5a` at the **top of the loop**, and that detail is what makes the
round measurable at all: without it pass 1 would zero `r0` and pass 2's "unchanged" would
also read zero, so the row could not fail. **The byte is its own proof.** Three standalone
EORs cannot leave a nonzero value, so only the folded handler can produce `0x5a` — the row
demonstrates both the defect and the fact that the fold occurred, which matters here because
this project has twice shipped combiner rows that were silently measuring the standalone
path.

- **#342 (`cpus/cpu_arm_instr.c`)** — `a != b` added to the match. One term; the whole
  defect.

**The after-panel found the control row wrong, and it was wrong twice over.** `eor_regshort`
is `arg[0] = Rn`, `arg[1] = Rm`, `arg[2] = Rd`, so the matcher's shape is `eor X,Y,X` —
**`Rm == Rd`**. My first control emitted `eor r0,r0,r1`, which is `Rn == Rd`, and therefore
never matched the combiner at all: it was measuring three standalone EORs while claiming to
exercise the fold. And even with the encodings corrected it still could not have pinned
anything, because `r1` was seeded once *outside* the loop — after pass 1 both registers held
`0x5a`, so a correct swap and a no-op give the same answer. Both registers are now re-seeded
to **distinct** values at the loop top and both are published.

That correction matters beyond this round: it is the *third* time an instrument here has
been caught measuring the standalone path while appearing to measure the folded one. The
DISC row was never affected — with every operand collapsed to one register it matches under
either reading of the convention — which is why the measurement stood and only the control
had to be rebuilt.

The swap rows are PINs, not discriminators. They now genuinely run `X(xchg)` on pass 2 and
pin that its swap is correct, so a broken handler fails them; they still cannot separate
folded-and-correct from not-folded-and-correct, which is exactly what keeps them out of the
DISC class.

One claim narrowed. "The folded handler only exists from the second pass" is true *of this
probe*, but not universally: translation read-ahead can translate the third instruction and
rewrite the first before the first executes. It holds here because the breakpoint disables
read-ahead, and `single_step` separately disables combination creation.

Gate 14 goes 154 → 158 rows.

## Eighty-third round (#340) — folding a compare into a branch changed the flags, and it took three attempts to see it

For a data-processing immediate with the S bit set, ARM sets C from the shifter carry-out.
The standalone `teqs`/`tsts` do that. The `*_samepage` handlers a `teq`/`tst`-followed-by-a-
branch is folded into **did not touch C at all**, and the `teqs` combiner has no operand
guard whatsoever while the `tsts` one guards only bit 31 — which is about **N** (with the top
bit clear, `a & b` cannot be negative), not about C. So the optimisation was observable.

**The measurement is the story here.** The defect looked *absent* twice, under two different
instruments that could not see it:

1. **`step` cannot reach it.** `cpu_dyntrans.c:1888` disables combining whenever
   `single_step` is set, so a stepped probe exercises the standalone handler while appearing
   to exercise the folded one. Five rows written that way passed **green** against a build
   with the defect still in it.
2. **A single forward run cannot reach it either**, however it is driven.
   `arm_combine_instructions` rewrites `ic[-1].f` — the *previous* instruction — while the
   **branch** is translated, and by then the compare has already executed. The folded handler
   therefore first exists on the **second pass** over that ic slot.

The working witness is free-running *and* two-pass: the pair sits in a loop that runs exactly
twice, flags are published on the second iteration, the breakpoint is after the loop (never on
the pair, because `single_step_breakpoint` is in the same guard — transient, but still fatal
if it lands on the sequence), and instruction tracing stays off, since
`!cpu->machine->instruction_trace` is the guard's third term. The carry preset uses `r7 = 0`
so `subs r6,r6,r7` re-establishes C on **both** passes without changing `r6`; a decrementing
preset would have differed silently between them.

```
A teq rot C combined       C1   owed C0   DISC     <- the defect, finally visible
A tst rot C combined       C1   owed C0   DISC
A teq rot C standalone     C0        C0   PIN  ok  <- control: same encoding, no branch
A tst rot C standalone     C0        C0   PIN  ok
A teq flat C preserved     C1        C1   PIN  ok  <- unrotated: C must be left alone
```

`0x0000FF00` is `0xFF ror 24`: rotated, above 255, bit 31 clear, so the owed answer is
`C := 0`. C is preset to **1** so "did nothing" is distinguishable from "cleared correctly".

- **#340 (`cpus/cpu_arm_instr.c`)** — `arm_combined_shifter_carry()`, applied in all four
  folded handlers. Guarded with `#ifndef ..._INCLUDED` because this file is compiled twice
  under `DYNTRANS_DUALMODE_32`. Whether `> 255` is an exact test for "was rotated" is a
  separate, pre-existing approximation in `cpu_arm_instr_dpi.c`; what this round fixes is
  that **folding must not change the flags**, and the standalone path is the oracle.

Gate 14 goes 149 → 154 rows. The wider hole this closes: the whole combined-handler family
(`cmps_*`, `teqs_*`, `tsts_*`, `netbsd_*`, `strlen`, `xchg`) had **no** gate coverage at all,
because every probe in `regress/` drives the guest with `step`. There is now a driver that can
reach them.

## Seventy-fourth round (#338) — the SCSI controller declared the write data had arrived before any of it had

`dev_mb89352` set `data_out_offset = transfer_count` at **allocation** time — "all the data
is here", asserted before a single byte was. `diskimage_scsicmd` gates a WRITE on
`data_out_offset != size` and on nothing else, so that satisfied the guard immediately.

The reachable sequence, which needs no data phase at all: `SCMD_SELECT`, then `SCMD_XFR`
with `PCTL = PH_DATAOUT` and TC sized to the write (this allocates the buffer and sets the
offset), then `SCMD_XFR` with `PCTL = PH_CMD`, then a six-byte `WRITE(6)` CDB — at which
point the CDB completes, the guard passes, and the buffer is committed to the disk image.
The `xferp` survives across `SCMD_XFR` commands; it is freed only on `SCMD_SELECT`.

#295 had already zeroed that buffer, so what remained was silent **corruption** of the disk
image rather than heap disclosure — which is why this half was deferred and why it still
mattered.

- **#338 (`devices/dev_mb89352.c`)** — the offset starts at **0**, and the `PH_DATAOUT` arm
  publishes `d->transfer_bufpos` — the count the byte-at-a-time write path actually
  maintained — immediately before calling `diskimage_scsicommand`. That arm is reached
  exactly when the buffer has filled, so a command now becomes eligible because the data is
  *present* rather than because it was *promised*.

The deferral note claimed the honest repair was blocked because "this model discards that
return". A review seat showed that is only half true: the `PH_CMD` arm already handles
`res == 2` by moving to `PH_DATAOUT`; only the `PH_DATAOUT` arm discards it, and that is a
separate `// TODO` this round does not touch.

Same limits as #337: reachability-argued from the code path, not rig-measured — a luna88k
mb89352 probe with a pre-poisoned sector is its own round. The harness confirms no
regression; no row asserts this yet.

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
