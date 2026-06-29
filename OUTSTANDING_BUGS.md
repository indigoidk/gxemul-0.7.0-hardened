# GXemul est/ — Outstanding bug candidates (not yet fixed)

> ## ✅ 2026-06-28 — OB-35 RESOLVED (correction #117; build 0/0, Codex+agy APPROVE FOR COMMIT, regression-clean)
> Added a **7445/7455 CPU model** as a NEW, purely-additive macppc subtype **`-e g4plus`** (→ MPC7455, PVR
> 0x80010000) so the existing `-e g4` (MPC7400) and g3/g5 are unchanged and OpenBSD 3.4/macppc stays
> regression-safe. **Verified:** on `-e g4plus`, NetBSD 8.2/macppc sets HID0[HIGH_BAT_EN] → #116's extended
> BATs **engage** (gate-opened=1, confirmed via a temporary ppc_bat debug) → it advances past the BAT/MMU
> layer; on `-e g4` the gate stays closed. Files: `cpu_ppc.h` (cpu_type row), `machine.h`
> (MACHINE_MACPPC_G4PLUS=4), `machine_macppc.c` (CPU map + subtype). See CHANGELOG/REVIEW_FINDINGS
> "Eleventh round".
> - **Known residual (NOT a safety bug, pre-existing): macppc OpenFirmware is skeletal.** Past the MMU,
>   NetBSD 8.2/macppc stalls in GXemul's incomplete OpenFirmware (`machine_macppc.c` skeletal model + `of.c`
>   device-tree `getprop` gaps). Reaching a full NetBSD-8.2/macppc multiuser boot is open-ended OF/device
>   work beyond OB-35's CPU-model scope — left as a future enhancement, not tracked as an OOB/safety OB.


> ## ✅ 2026-06-28 — OB-27..34 RESOLVED (corrections #106–#113; build 0/0, pmax+arc regression-clean)
> All 8 deferred Phase-B/C candidates were Claude-verified (**all confirmed real**) and fixed — see
> CHANGELOG / REVIEW_FINDINGS "Eighth round". Map: OB-27→#106 (dev_fb from_x), OB-28→#108 (ps2_gif),
> OB-29→#107 (pvr span), OB-30→#109 + OB-31→#110 (iso9660), OB-32→#111 (bootblock n_blocks), OB-33→#112
> (diskimage %s), OB-34→#113 (SCSI CDB-length).
> ~~Still open: OB-25 / OB-26~~ → **now also RESOLVED: OB-25→#115 (mymkstemp unpredictable overlay temp
> names), OB-26→#114 (osiop skip data phase instead of exit(1)) — see "Ninth round". ALL OB-1..34 are now
> resolved.**

> ## 2026-06-28 — Phase-C deeper audit (3-agent fan-out): #101–#105 applied; 1 new candidate
> Agents swept network/NAT, SCSI/ATA storage, and the remaining devices + dyntrans. Claude verified +
> fixed 5 bugs (#101–#105, incl. 2 CRITICAL: dev_scc OOB heap write + net_arp heap overflow — see
> CHANGELOG / REVIEW_FINDINGS "Seventh round"). One candidate deferred:
> - **OB-34 `disk/diskimage_scsicmd.c` short-CDB over-read (med):** `diskimage_scsicommand()` only checks
>   `cmd_len >= 1`, then every opcode reads fixed CDB offsets (up to `cmd[8]`) — so a guest that submits a
>   short CDB (the SCSI/ATA controllers allocate `cmd[]` to the guest's byte count) causes an OOB read of
>   the host `cmd` buffer, influencing the computed LBA/transfer length. Fix with a per-opcode CDB-length
>   table (6/10/12/16) validated before the reads, under its own regression (touches every controller).

> ## 2026-06-28 — Phase-B new-surface audit (3-agent fan-out): #96–#100 applied; 7 new candidates
> Agents swept the PROMs (all CLEAN), the framebuffer renderers, and the disk parsers; Claude verified +
> fixed 5 bugs (#96–#100, incl. a CRITICAL ps2_gs OOB heap write and a HIGH Apple-partition stack
> over-read — see CHANGELOG / REVIEW_FINDINGS "Sixth round"). These further agent-found candidates are
> **not yet exact-fix-verified by Claude** (record for a follow-up fix pass):
> - **OB-27 `devices/dev_fb.c` `framebuffer_blockcopyfill` (high):** in copy mode the source column
>   `from_x` is not clipped (dst `x1/x2` and `from_y` are), so the `memmove` source over-reads the host
>   framebuffer; reachable from dev_ps2_gif blockcopy and dev_igsfb scroll → host-heap info leak.
> - **OB-28 `devices/dev_ps2_gif.c` TA-putchar (high):** pixel source offset `(24 + y*xsize)*4` uses
>   guest `xsize`/`ysize` (≤65535) with no check against the input `len` → large OOB read of the host DMA
>   buffer (also an `int addr` overflow).
> - **OB-29 `devices/dev_pvr.c:2438` (med):** the 24-bit `pvr_fb_tick` copy wraps only the start
>   `vram_ofs % VRAM_SIZE`, not the span → reads past the 8 MB VRAM; also signed `vram_ofs` can go
>   negative. Other pixelmodes wrap each access.
> - **OB-30 `disk/bootblock_iso9660.c:188` (med):** the root-directory walk reads the 8-byte record
>   header + up to 64 name bytes past `dirbuf` (guard only checks `dp < dirbuf+dirlen` at the top).
> - **OB-31 `disk/bootblock_iso9660.c:308` (med):** `if (i < len - strlen(filename))` underflows
>   `size_t` when `strlen(filename) > len`, defeating the bound → over-read.
> - **OB-32 `disk/bootblock.c` (low):** the bootblock/OSLoader size "WARNING" checks call `fatal()`,
>   which does NOT exit (debugmsg.c:334), so a disk-controlled `n_blocks*512` proceeds with int-overflow
>   UB → `malloc` abort (DoS). Make the checks `return`; use size_t math + an upper bound.
> - **OB-33 `disk/diskimage.c:321` (low):** `fatal("… type %i …", id, diskimage_types[type])` passes a
>   `char *` to `%i` (UB on the not-found path); use `%s`.

> ## 2026-06-28 — multi-model review (Codex + agy + Claude): #89–#94 applied; 2 new candidates
> A three-engine review (Codex `gpt-5.5`/xhigh, agy `Gemini 3.1 Pro`/High, Claude verification + a
> consensus rebuttal loop) of the full hardening diff fixed **6 confirmed bugs (#89–#94** — see
> `CHANGELOG.md` / `REVIEW_FINDINGS.md` "Fifth round") and **rejected 3 false positives** (both models
> conceded). **2 lower-severity items remain open:**
> - **OB-25 `disk/diskimage.c` temp-file TOCTOU (low, local-only).** #7/#20 create the overlay temp
>   files with `fopen "wx"` but then close and **reopen them by name** in `diskimage_add_overlay()`,
>   leaving a swap/symlink race window. Fix: `mkstemp()` + pass the fd; never reopen by name.
> - **OB-26 `devices/dev_osiop.c` guest-reachable `exit(1)` (low DoS).** The #10 NULL-`xferp` guard
>   calls `exit(1)` on a state a guest can drive (SCSI data phase, no active transfer) → a guest can
>   halt the emulator. Prefer aborting the phase (`break`) over killing the process. (Replaced a worse
>   null-deref, so not a regression — a hardening-quality improvement.)

> ## ✅ RESOLVED 2026-06-27 — see CHANGELOG.md "#70–#88"
> All 24 candidates below were triaged (Codex `gpt-5.5` *xhigh* proposals + independent source audit):
> - **19 fixed → corrections #70–#88** (builds 0/0; pmax + arc rigs re-verified):
>   OB-1 #70 · OB-2 #71 · OB-3 #72 · OB-6 #73 · OB-7 #74 · OB-8 #75 · OB-9 #76 · OB-11 #77 ·
>   OB-12 #78 · OB-13 #79 · OB-14 #80 · OB-15 #81 · OB-16 #82 · OB-17 #83 · OB-18 #84 · OB-19 #85 ·
>   OB-20 #86 · OB-21 #87 · OB-23 #88.
> - **3 false positives (not real)** — OB-4, OB-5, OB-10: `cpus/memory_rw.c:288` clamps `len` to the
>   device length before the handler runs, and these three are registered with length == backing size
>   and have no direct callers, so the "end-span" is unreachable.
> - **1 deferred** — OB-22 (jazz jazzio vector-ack): emulation correctness, not host-OOB;
>   medium-confidence; in the #69 arc interrupt path — deferred to avoid regressing the verified arc boot.
> - **1 skipped** — OB-24 (signed `byte<<24` in CPU instruction cores): UBSan-only, hottest path, no
>   exploit path; consistent with the pre-existing "intentionally left" decision (shared decoder fixed in #27).
>
> The per-finding analysis below is retained as the audit record.

---

Consolidated from two **read-only** Codex reviews (model `gpt-5.5`, effort `high` + `xhigh`)
on 2026-06-27, plus the manual audit. These are **static-analysis findings** — bounds/overflow
reasoning from reading the source; most are **not yet runtime-confirmed** (several need a specific
guest/board, e.g. Dreamcast, SGI, TURBOchannel framebuffers). They are candidates for the next
correction set (#70+). The 69 already-applied corrections are in `REVIEW_FINDINGS.md` / `CHANGELOG.md`
and are **not** repeated here. `src/` (pristine baseline) is untouched.

**Threat model:** the emulator runs untrusted guest OS images (device MMIO/DMA) and loads untrusted
executable files (loaders). HIGH = a malicious guest or input file can cause a guest→**host**
memory-safety violation (OOB read/write of host memory). MED/LOW = host DoS / UB / device-state
corruption without a clear host-OOB path.

**Two dominant root patterns** (almost every HIGH below is one of these):
1. **End-span not checked.** An MMIO handler validates the *start* (`addr < size`) but then
   `memcpy`/indexes `len` bytes, so a 2/4/8-byte access at the last valid offset crosses the host
   buffer. Fix shape: require `addr + len <= size` (or clamp `len`).
2. **MMIO window larger than its backing array.** The registered device length exceeds the
   allocation, so high offsets index past it. Fix shape: bound the offset to the real backing size.

---

## High — guest → host OOB read/write

| ID | Site | Pattern | Trigger / impact |
|----|------|---------|------------------|
| OB-1 | `devices/dev_fb.c:646` (+ callers `dev_dec21030.c:135`, `dev_sgi_mardigras.c:200`) | end-span | `dev_fb_access()` checks `relative_addr >= framebuffer_size` only, then `memcpy(framebuffer+addr,…,len)` — wide access at last pixel → host fb heap OOB R/W |
| OB-2 | `devices/dev_px.c:608` | window>backing | PX SRAM MMIO window is 512 KB (`0x200000..0x27ffff`) but `sram[]` is 128 KB; offsets >`0x21ffff` corrupt host heap — any PX/PXG TURBOchannel guest |
| OB-3 | `devices/dev_px.c:315` (+`:414`,`:531`) | unchecked rows | PX STAMP DMA copyspans/fill/putchar use guest `span_src/span_dst` rows in fb pointer math with only `span_len` capped → fb heap OOB R/W |
| OB-4 | `devices/dev_pvr.c:2551` / `:2567` | end-span | `dev_pvr_vram_access()` copies to/from `vram+relative_addr` without `addr+len <= VRAM_SIZE` (distinct from the fixed #65/#68 render/texture paths) |
| OB-5 | `devices/dev_asc.c:778` / `:794` | end-span | ASC 128 KB DMA window: raw `memcpy(dma+addr,…,len)` with no end check |
| OB-6 | `devices/dev_adb.c:300` / `:305` | unbounded append | `output_buf[MAX_BUF=100]` appended via `output_buf[cur_output_offset++]=c` with no cap; guest toggles ACK in output mode → heap OOB write past `struct adb_data` |
| OB-7 | `devices/dev_igsfb.c:183` | unbounded index | DAC `palette_write_index` unclamped; `rgb_palette[index*3+sub]` past the 256-entry palette (start at 255) |
| OB-8 | `devices/dev_kn01.c:171` | unbounded index | KN01 VDAC overlay palette has 16 entries but `cur_write_addr_overlay` is raw guest data → `rgb_palette_overlay+3*addr` OOB |
| OB-9 | `devices/dev_sgi_mardigras.c:220` / `:224` | end-span | microcode-RAM MMIO validates `< MICROCODE_END` only, copies `len` → OOB past `microcode_ram` |
| OB-10 | `devices/dev_ether.c:82` / `:89` | end-span | test-ethernet `buf` MMIO copies to/from `buf+addr` with no end check |
| OB-11 | `devices/dev_pcc2.c:327` (+`:372`) | end-span | `relative_addr %= PCC2_SIZE` folds the *start* only; wide access near end of the 0x40-byte `pcctwo_reg[]` spans past it |
| OB-12 | `devices/dev_pmagja.c:111` | window>backing | PMAG-JA treats all `>=0x200000` as 8-bit pixels up to `0x3c0000`, but `pixeldata` is only 1280×1024 → OOB (and drives `dev_fb_access` out of range) |
| OB-13 | `devices/dev_sgi_gbe.c:706` | unmasked index | GBE palette store `selected_palette[color_index]` instead of `[color_index & 0xff]`; cmap 1..31 writes far past the 256-entry cache |
| OB-14 | `devices/dev_sgi_gbe.c:274` | stack over-read | tile convert: `fb_buf` sized for 512 px but guest partial-tile fields make `fb_len` up to 992 px → `dev_fb_access` copies past `fb_buf` (stack-byte leak into emulated fb) |
| OB-15 | `devices/dev_vga.c:607` | window>backing | VGA gfx window is fixed `0x18000` but `gfx_mem_size` is realloc'd per mode (e.g. 64,000 for mode 0x13) → access in-window but past `gfx_mem` → heap OOB |
| OB-16 | `devices/dev_vga.c:412` | unchecked index | VGA CRTC guest-programmed `base` (start hi/lo) added to every visible charcell index without `base+end` check → charcell heap OOB read on redraw |

## Medium — host DoS / overflow / device-state corruption

| ID | Site | Issue |
|----|------|-------|
| OB-17 | `devices/dev_dec21143.c:763` | TX descriptor chain: many non-`LS` descriptors → repeated `realloc(cur_tx_buf_len+bufsize)` (unbounded host alloc); `int cur_tx_buf_len` can wrap → alloc/copy size bug |
| OB-18 | `file/file_android.c:103` / `:146` / `:186` | file-controlled `page_size`: `==0` → divide-by-zero; very large → 32-bit page/seek overflow → crash/misload |
| OB-19 | `file/file_elf.c:94` (loop `:450`–`:482`) | PT_LOAD copy cursor `ofs` is `int` vs file-controlled `p_filesz` → signed overflow/UB on huge segments (chunk buffer itself is bounded) |
| OB-20 | `devices/dev_dreamcast_gdrom.c:183` (`:90`) | `READ_SECTORS` with `cnt==0` derives `cnt = 2048*sector_count` from guest bytes, then allocates it → guest-triggered host OOM/hard-exit |
| OB-21 | `devices/dev_dreamcast_g2.c:94` | EXTDMA maps `0x100` but `extdma_reg[]` is 0x80; offsets `0x90..0xbc` index `extdma_reg[>=36]` → C subobject OOB into adjacent `misc_reg` (device-state corruption) |
| OB-22 | `devices/dev_jazz.c:613` (`jazz_jazzio`) | **pre-existing, correctness only** (NOT a #69 regression): after reporting a vector it deasserts `mips_irq_3` without clearing `int_asserted` → possible stuck/missed non-timer JAZZ IRQs until next edge/mask write |

## Low / reviewed

| ID | Site | Note |
|----|------|------|
| OB-23 | `devices/dev_sgi_re.c:1127` | MTE fill subtracts `sizeof(zerobuf)` from `dstlen` while writing only `fill_len` → mis-accounting → guest hang / wrong emulated writes (no host OOB observed) |
| OB-24 | `cpus/*` (e.g. `cpu_arm_instr_loadstore.c:297`; ARM/MIPS/PPC/m88k/PROM) | residual signed `byte<<24` UB; real C UB but does not feed host pointers/sizes/indices — sanitizer/portability cleanup, no exploit path found |

## Confirmed clean
- **#69 (arc Jazz interrupt-enable mask)** — both review passes independently found **no regression**:
  assert/deassert gate on `int_asserted & int_enable_mask`, `EXT_IMASK` recomputes IRQ3/6 on mask
  change, and masked pendings stay in `int_asserted` (delivered when later enabled).

## Suggested remediation order
1. **Window>backing (OB-2, OB-12, OB-15):** straight host-heap corruption from any access in-window;
   bound the offset to the real allocation size. Highest priority.
2. **End-span family (OB-1, OB-4, OB-5, OB-9, OB-10, OB-11):** add `addr+len <= size`; many share the
   `dev_fb_access` helper (fix once in OB-1 covers OB-1's direct callers).
3. **Unbounded index/append (OB-6, OB-7, OB-8, OB-13, OB-14, OB-16, OB-3):** clamp/mask the
   guest-controlled index; size the temp buffer to the max (OB-14).
4. **Loader/alloc (OB-17..OB-21):** reject `page_size==0`, cap aggregate/realloc sizes, widen `int`
   cursors to `off_t`/`size_t`, validate `cnt`.

> Generated read-only; no source was modified. Raw review transcripts:
> session scratchpad `codex_review.txt` (high) and `codex_review_xhigh.txt` (xhigh).
