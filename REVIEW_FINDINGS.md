# GXemul 0.7.0 — Code Examination, Corrections & Correctness Findings

*Built & verified under Linux (gcc 15.2.1): primary gcc build **0 errors, 0 warnings**, binary runs.
Last updated 2026-06-27.*

This is the full sweep: a manual review, a `gcc -fanalyzer` static-analysis pass
over every translation unit, and an ASan/UBSan **fuzzing** campaign against the
file loaders — with corrections applied to the `est/` source and re-verified by a
clean rebuild (67 corrections + 1 performance optimization, #67; the **primary gcc build is
0 errors / 0 warnings**, confirmed by a fresh clean `make -j`). Every
source change is also recorded as a unified diff in `est/CHANGES.patch`. An independent
**6,772-case fuzz audit shows no ASan/UBSan reports** on the est tree — note this means no
sanitizer signature was observed before the cases run to timeout, *not* a full behavioral
pass. (The ASan/UBSan, clang, and `-fanalyzer` build configs still emit some pre-existing
non-fatal compiler warnings, mostly in generated dyntrans code; the 0/0 figure is the
primary gcc build.) The `-fgnu89-inline` build fix is also applied
to the **root `configure`** so the original baseline builds cleanly too (the code under
`src/` is otherwise untouched, kept as the reference for orig-vs-est comparison).

---

## Corrections applied (all built clean & verified)

| # | File | Problem | Fix |
|---|------|---------|-----|
| 1 | `core/misc.c` | `mystrlcpy`/`mystrlcat` (strlcpy fallbacks) ignored `size` → buffer overflow by construction | Correct bounded BSD-semantics implementations |
| 2 | `core/misc.c` | `mymkstemp` weak: 10-digit charset, no retry | 62-char alphanumeric set + collision retry; keeps atomic `O_CREAT\|O_EXCL` |
| 3 | `core/emul.c` | **Unsafe shell invocation**: `system("mv %s …")` / `system("gunzip … %s")` with unquoted, caller-influenceable file names | Replaced with a `fork()`+`execlp("gunzip",…)`+`dup2()` helper — never invokes a shell |
| 4 | `core/emul.c` | `snprintf` truncation warning (`tmpstr[20]`) | `tmpstr[32]` |
| 5 | `promemul/arcbios.c` | `malloc(0)` (`-Walloc-size`) | `NULL` (the following `realloc(NULL,…)` behaves like `malloc`) |
| 6 | `file/file_srec.c` | **Uninitialized stack read**: `bytes[270]` never cleared; caller-controlled `count` makes the type switch read past the parsed data into the load address / emulated RAM. Also `count-1-data_start` could go negative → huge `size_t` length | `memset(bytes,0,…)` per record + guard the write length `> 0` |
| 7 | `disk/diskimage.c` | Memory leak of `overlay_basename` on two `fopen` error paths | `free()` on both error paths |
| 8 | `devices/dev_fb.c` | **Guest-triggerable OOB host write**: in `framebuffer_blockcopyfill`, clipping never ensures `x2 >= x1`, so `linelen = (x2-x1+1)*bpp` (a `size_t`) wraps huge → `memset`/copy past the framebuffer | Early-return when `x2 < x1`; bounded 8-bit `memset` size |
| 9 | `configure` | Stock `./configure && make` fails to link on modern glibc | Auto-detect & add `-fgnu89-inline` (see build note below) |
| 10 | `devices/dev_osiop.c` | Guest-triggerable NULL-deref: a forced SCSI data phase with no active transfer dereferences `d->xferp` (5 analyzer findings) | Guard before the phase switch → clean diagnostic exit (matches the file's existing convention) |
| 11 | thirdparty headers ×4 (`bootblock.h`, `dp83932reg.h`, `pcireg.h`, `sgi_arcbios.h`) | `#define __attribute__(x)` neutered **all** attributes — the root cause of the link errors, and it silently discarded `__attribute__((packed))` on hardware/disk structs | Removed the neutering (the Debian `remove_defines` approach). Verified: 0 new warnings, byte-identical binary size → no struct-layout change on this codebase |
| 12 | `devices/dev_pvr.c` | `realloc(d->ta_commands,…)` and the initial `malloc` had no NULL check; the `wf_*[]` strip-vertex arrays could be read uninitialized | `CHECK_ALLOCATION` on both allocations; zero-init the `wf_*` arrays |
| 13 | `cpus/generate_arm_r.c` | `(int)(1 << 31)` signed left-shift **UB** (caught by UBSan in the build-time generator) | `1U << …` (identical output, no UB) |
| 14 | `file/file_aout.c` | **OOB read / SEGV — found by fuzzing**: `str_index` from the a.out symbol table is used as `string_symbols + str_index` with no bounds check → reads past the string table | NUL-terminate the table + validate `str_index < strings_len` |
| 15 | `file/file_elf.c` | Same class: `st_name` (from the ELF symbol) used unvalidated as `symbol_strings + st_name` | Skip symbols whose `st_name >= symbol_length` |
| 16 | `file/file_ecoff.c`, `file/file_macho.c` | Same class: `es_strindex` / `n_strx` (the latter **signed**) used as unvalidated string-table offsets | Bounds-check the index; Mach-O now `calloc`s the table so it is always NUL-terminated |
| 17 | `file/file_aout.c` | **2nd fuzzer find (i960 b.out)**: `symbsize` was `int32_t`; a symbol-table size with the high bit set → signed left-shift UB (UBSan) and `malloc(symbsize)` sign-extended to ~`2^64` (ASan) | Make `symbsize` `uint32_t` + sanity-bound it against the file size before allocating |
| 18 | `symbol/symbol.c` | **Stack buffer overflow** (external review): `fscanf("%s", b)` into `char[80]` symbol-file tokens is unbounded — a long token smashes the stack (CWE-121) | Bounded `%79s` conversions |
| 19 | `file/file_macho.c` | **OOB read / infinite loop** (external review): the load-command loop trusts `sizeofcmds`/`cmd_len` and indexes `buf[pos+…]` (64 KiB) with no bounds; `cmd_len==0` loops forever | Bound the header + whole command against the bytes actually read; reject `cmd_len < 8`. **(anti-gravity follow-up)** also zero-init `buf` and add `pos+256 > len` so a truncated `LC_UNIXTHREAD` can't read uninitialized stack |
| 20 | `disk/diskimage.c` | Temp overlay files created `fopen(…,"w")` with predictable names and `fclose()`d with no NULL check (symlink race + crash on failed create) | Exclusive create `"wx"` + NULL-check both opens |
| 21 | `devices/dev_fb.c` | 24-bit framebuffer fill bounded by `sizeof(buf)` where `buf` is a pointer → painted only 8 bytes/line (correctness, not safety) | Bound by `linelen` |
| 22 | `net/net_ip.c`, `net/net.c` | **Signed left-shift UB** (found by the network fuzz harness): `packet[N] << 24` overflows `int` for bytes ≥ 128 — in TCP seq/ack and IP-address assembly (6 sites) | Cast the high byte to `uint32_t` |
| 23 | `machines/machine_macppc.c` | **OOB heap read** (found by running the machine under ASan): `store_buf(…, boot_string_argument, 256)` reads a fixed 256 bytes, but the default arg is `strdup("")` (1 byte) → 255-byte over-read copied into emulated RAM on *every* macppc boot | Copy only `strlen()+1` bytes, capped at 256 |
| 24 | `devices/dev_gc.c` + 9 interrupt controllers (`dev_bebox`, `dev_cpc700`, `dev_footbridge`, `dev_i80321`, `dev_irqc`, `dev_kn02`, `dev_kn02ba`, `dev_kn230`, `dev_sgi_ip32`) | **Signed left-shift UB**: `templ.line = 1 << i` over `for i<32` → `1<<31` UB at `i==31` | `(uint32_t)1 << i` |
| 25 | `promemul/arcbios.c`, `devices/dev_sgi_ip32.c`, `cpus/cpu_dyntrans.c` (ARM), `devices/dev_luna88k.c` | More **signed-shift UB** in setup/PROM/dyntrans, found by an ASan "run every machine" sweep (`byte<<24`, `1<<31`, `nibble<<28`) | Cast to `uint32_t` |
| 26 | `file/file_elf.c` | **ELF allocation-size-too-big** (external fuzz audit — 11 of est's 12 remaining ASan signatures): `malloc(sh_size)` / `malloc(sh_size+1)` with `sh_size` from the untrusted section header → absurd allocation (ASan abort / OOM) | Reject `sh_size > file size` before allocating the symbol/string tables |
| 27 | `file/file.c` | **`unencode` signed-shift UB** (3rd external fuzz audit — the single root of all 102 remaining UBSan signatures): the byte-assembly macro sign-extended via `var = -1; var <<= 8`, i.e. left-shifting a negative `int`. This macro decodes *every* multi-byte field in *every* file loader (ELF/a.out/Mach-O/ECOFF) | Accumulate in a `uint64_t`, sign-extend in a defined way, then assign back — traced behavior-identical, no UB |
| 28 | `file/file_elf.c` | **ELF section-bounds tightening** (P3): also require `sh_offset` within the file and `sh_size <= filesize - sh_offset`, and the symbol-table `sh_size` to be a multiple of the entry size, before allocating/reading | Extended the SYMTAB/STRTAB guards |
| 29 | `cpus/cpu_dyntrans.c` | **Signed-shift UB** (5th external audit): `translations_bitmap \|= (1 << x)` shifts into bit 31 of a signed `int` | `(uint32_t)1 << x` |
| 30 | `cpus/cpu_ppc.c` | **Signed-shift UB** (5th external audit): `instr[0] << 24` (high byte) in the PPC instruction disassembler | `(uint32_t)instr[0] << 24` |
| 31 | `devices/dev_disk.c` | **Guest→host OOB read/write** (found by the new device-MMIO fuzzer): `dev_disk_buf_access` does `memcpy(d->buf + relative_addr, …, len)` with **no bound** — `d->buf` is only `arch_pagesize`, so an end-spanning/misaligned data-buffer access reads or (write branch) **writes** past it | Bound to `buf_len`: skip if `rel ≥ len`, clamp `len`, zero-fill OOB reads |
| 32 | `core/emul_parse.c` | **OOB write** (found by cppcheck): `cur_machine_device[]` declared `[MAX_N_DISK]` (10) but the guard uses `MAX_N_DEVICE` (20) — a config file with 11–20 `device()` lines writes 10 pointers past the array | Declare it `[MAX_N_DEVICE]` |
| 33 | `devices/dev_mp.c` | **Guest→host OOB** (device-MMIO fuzzer): `DEV_MP_STARTUPCPU` does `d->cpus[which_cpu]->pc = …` with `which_cpu` = the guest-written value, unbounded → OOB pointer read then write | Reject `which_cpu` outside `[0, ncpus)` |
| 34 | `promemul/arcbios.c` | **Guest→host OOB read/write** (PROM-call fuzzer): the ARCBIOS `Close`/`Seek`/`Read`/`Write` calls index `file_handle_in_use[]`/`current_seek_offset[]` (`int[ARC_MAX_HANDLES]`) with the guest's handle arg, unbounded (`Seek` writes a guest value OOB) | Reject handles `≥ ARC_MAX_HANDLES`, matching the already-guarded calls |
| 35 | `devices/dev_8253.c` | **Guest→host OOB** (device-MMIO fuzzer): `counter_select = idata >> 6` (signed `int`) can go **negative**, bypassing the `> 2` guard → `d->mode[counter_select]` OOB on `int[3]` | Mask to the 2-bit field: `(idata >> 6) & 3` |
| 36 | `cpus/cpu_m88k.c` | **Signed-shift UB** (mutation fuzz, 168 hits — dominant): `byte<<24` assembling the M88K instruction word | `(uint32_t)` cast |
| 37 | `cpus/cpu_m88k_instr.c` | **Signed-shift UB**: `1 << d` shifts into bit 31 | `1U << d` |
| 38 | `cpus/cpu_ppc_instr.c` | **Shift-by-32 UB** (×3 rotate instrs): `tmp >> (32-sh)` is UB when `sh == 0` | `sh ? rotate : tmp` |
| 39 | `cpus/cpu_ppc_instr.c` | **Signed-shift UB** (×10 condition-register instrs): `0xf << bf_shift` overflows `int` at `bf_shift == 28` | `(uint32_t)0xf << bf_shift` |
| 40 | `cpus/cpu_sh_instr.c` | **Negative-shift UB** (×2 SH shift instrs): `rn <<= sa` on a negative `int32_t` | shift as `uint32_t`, assign back |
| 41 | `cpus/cpu_mips_instr.c` | **[P1] inherited dyntrans crash — root-caused & fixed**: a **branch in a branch's delay slot**. The inner branch ran nested branch logic and then did `cpu->delay_slot = NOT_DELAYED`, wiping the `EXCEPTION_IN_DELAY_SLOT` bit the *outer* branch checks; the outer branch therefore applied its branch and `next_ic++` ran one past the single-entry `nothing_call` sentinel → global-buffer-overflow reading `ic->f` @ `cpu_dyntrans.c:354` (reproduces in root too) | Detect the nested case at branch entry (`if (cpu->delay_slot & TO_BE_DELAYED)`): flag the outer branch via `EXCEPTION_IN_DELAY_SLOT` and `return` instead of running nested logic. **Verified with the audit reproducer (no crash, defensive holder removed) and pmax/arc/sgimips boot clean** |
| 42 | `core/emul.c` | **Subprocess hardening** (external review): `execlp("gunzip",…)` trusts `$PATH`; and `close(fd)` could close stdout if `open()` reused fd 1 | Try `/bin/gunzip` & `/usr/bin/gunzip` (absolute) before a PATH fallback; `if (fd != STDOUT_FILENO) close(fd)`. **(anti-gravity follow-up)** `--` before `src_name` so a filename starting with `-` can't be parsed as a gunzip option |
| 43 | `core/misc.c` | **Predictable temp names** (external review): `mymkstemp` drew its suffix from unseeded `random()` → a local user could pre-create the 256 candidate names (extraction DoS). (`O_EXCL`+retry already blocked the symlink race) | Draw the suffix from `/dev/urandom`; `random()` only as a fallback |
| 44 | `promemul/arcbios.c` | **OOM-safety**: ~10 ARCBIOS boot-string / env setup allocations (`malloc(strlen(boot_device)+50)` etc.) were unwrapped → NULL-deref in the following `snprintf` on OOM. (Non-guest, setup-only — *not* the guest-to-host DoS an external audit claimed; the guest-controlled `malloc(gpr[A2])` calls in arcbios/dec_prom were already `CHECK_ALLOCATION`'d) | Wrap with `CHECK_ALLOCATION` |
| 45 | `include/misc.h` + `cpus/cpu_{alpha,arm,arm_instr,i960,i960_instr}.c` | **Shift-UB cleanup** (external review TIP): per-byte `byte<<24` instruction-word assembly in the disassemblers (signed-shift UB class) | New `READ_WORD_LE`/`READ_WORD_BE` macros that promote each byte to `uint32_t` before shifting; 9 disassembler fetch sites converted to use them |
| 46 | `cpus/cpu_m88k_instr.c`, `cpu_ppc_instr.c` | **Residual CPU shift UBs** (codex audit, mutation-fuzz replay): M88K `ext` signed bitfield-extract used signed shifts; PPC CR-compare (`cmpd`/`cmpld`) inserted `c << bf_shift` which overflows `int` (e.g. `15 << 28`) | M88K extract now sign-extends via unsigned masks (`1u<<(w-1)`, mask, OR-in high bits); PPC casts to `(uint32_t)` before shifting. Verified UBSan-clean + 103-finding replay → 0 signatures |
| 47 | `cpus/cpu_sh_instr.c` | **[P1-class] SH4 dyntrans crash — same nested-branch bug as #41, found by this session's completeness review**: a delayed conditional branch (`bt/s`/`bf/s`) sitting in another delayed branch's delay slot — the inner branch clears `cpu->delay_slot`, so the outer's not-taken path does `next_ic++` one past `nothing_call` → global-buffer-overflow in **`sh_run_instr`** @ `cpu_dyntrans.c:354`. **Newly reproduced** with a hand-built `bt/s` chain on `testsh` | Apply the #41 entry-check to every SH delayed-branch/jump handler (`if (cpu->delay_slot & TO_BE_DELAYED) { \|= EXCEPTION_IN_DELAY_SLOT; return; }`). **Verified: reproducer no longer crashes + NetBSD/landisk (SH4) boots clean** |
| 48 | `promemul/of.c` | **Guest→host OOB write** (found by static audit of the OpenFirmware emulator, confirmed with a new in-process OF harness): the `call-method` **"set-colors"** service does `memcpy(vfb_data->rgb_palette + 3*color, rgb, 3)` with `color = OF_GET_ARG(3)` an **unbounded guest value** → writes 3 guest-controlled bytes at an arbitrary offset into/past the fixed 768-byte host palette. **Reproduced**: crafted `of_emul` set-colors call with `color=0x40000` → SEGV at `of.c:180`; the harness shows the fixed build returns cleanly | Reject `color < 0 \|\| color >= 256` before the palette write |
| 49 | `devices/dev_osiop.c` | **Guest→host OOB write (CRITICAL)** (device DMA audit): the NCR SCSI SCRIPTS `DATA_OUT_PHASE` copies `xfer_byte_count` (guest-controlled, up to 16 MB, from the table-indirect descriptor) into `data_out[data_out_offset++]` with **no** bound — `data_out` is malloc'd only to the SCSI command's `data_out_len`. `DATA_IN_PHASE` already had the symmetric guard | Add `&& data_out_offset < data_out_len` to the copy loop |
| 50 | `devices/dev_asc.c` | **Guest→host OOB write** (DMA audit): on a short DATA_IN, `memset(d->dma + off, 0, lenIn2)` used the **un-clamped** guest transfer count `lenIn2` (clamped to the buffer only *afterwards*) → ~64 KB zero-write past the 128 KB `d->dma` | `memset(…, lenIn)` (the already-clamped length) |
| 51 | `devices/dev_asc.c` | **Guest→host OOB read** (DMA audit): the DATA_OUT `memcpy`/dma_controller source `d->dma + off` with `len2` was clamped to the *dest* (`data_out_len`) only; `off` is guest-controlled → reads past `d->dma` into the disk image | Also clamp `len2` so `off + len2 <= ASC_DMA_SIZE` |
| 52 | `devices/dev_sgi_mec.c` | **Guest→host OOB read** (DMA audit): the TX fill loops bound writes to `MAX_TX_PACKET_LEN` (1700), but `cur_tx_packet_len = len` (guest, up to 65536) was handed to `net_ethernet_tx` → its `memcpy` reads ~63 KB past `cur_tx_packet` and ships host memory onto the emulated network | Transmit `j` (bytes actually copied), not `len` |
| 53 | `devices/dev_dreamcast_maple.c` | **Guest→host OOB read + wild-pointer deref** (DMA audit): `port = buf[2]` (guest DMA byte, 0–255) indexes `device[N_MAPLE_PORTS=4]` in `MAPLE_COMMAND_DEVINFO`; a non-NULL garbage pointer is then dereferenced and copied to the guest | Reject `port < 0 \|\| port >= N_MAPLE_PORTS` |
| 54 | `devices/dev_mb8696x.c` | **Guest→host OOB read** (DMA audit): the EEPROM read index `(eeprom_command & 0x7f) << 1` (0–254, guest) indexes `eeprom[FE_EEPROM_SIZE=32]`, and the value is clocked back to the guest | Mask `addr &= (FE_EEPROM_SIZE - 2)` |
| 55 | `devices/dev_pvr.c` | **Host OOB read (LOW)** (DMA audit): texture fetch `vram[addr+1]` reaches `VRAM_SIZE` (1 byte past the 8 MB VRAM) at `addr == VRAM_SIZE-1`; texture reads weren't masked like the other VRAM paths | Clamp `addr` to `VRAM_SIZE - 2` |
| 56 | `file/file_macho.c` | **Unbounded allocation / over-read** (external review P1): LC_SYMTAB `nsyms`/`strsize`/`symoff`/`stroff` are file-controlled and fed to `malloc(12*nsyms)` / `calloc(strsize+1)` / `fread` / `fseek` with no range check → huge/negative/overflowed sizes (same class as ELF #26) | Bound all four against the real file size (`ftell` to EOF); skip the symtab on bogus values. **Also (P2)** corrected the load-command loop bound from `pos < sizeofcmds` to `pos < header_size + sizeofcmds` (pos is an absolute file offset) |
| 57 | `file/file_macho.c` | **Over-strict load-command bound (P2, external audit)**: the loop required `pos + 256 <= len` before *every* load command, so a valid compact command near EOF was rejected — a minimal PPC `LC_UNIXTHREAD` needs only `pos+176`, so a 204-byte image died with *"No entry point? Aborting"* (it loaded only when padded to 284). Refines #19 | Replace the blanket 256 with **per-command bounds** (LC_SEGMENT `pos+40`, LC_SYMTAB `pos+24`, LC_UNIXTHREAD `pos+176`). **Verified** against the audit's regression cases: the 204-byte image now executes; a truly-truncated 160-byte thread is still rejected |
| 58 | `file/file_macho.c` | **LC_SYMTAB incomplete bounds (P2, external audit)**: #56 bounded `symoff`/`nsyms`/`stroff`/`strsize` *individually* but not the products, so `symoff + 12*nsyms` / `stroff + strsize` could still run past EOF → a hard `exit(1)` at the `fread`s, and a sparse / `int`-overflow `nsyms` reached `malloc` (OOM at line 248). Refines #56 | Bound the **products** against the file size (uint64 math). **Verified**: the two "extend past EOF" cases now skip the bad symtab and keep loading instead of aborting |
| 59 | `file/file_ecoff.c` | **Unbounded symbol allocations (P2, external audit)**: `f_nsyms` (MS-COFF fallback), `issExtMax`, `iextMax` are file-controlled and fed to `malloc()`/`fread` with no file-size bound, and the MS-COFF `fread` result was unchecked → huge/overflowed counts ⇒ OOM / over-read (same class as ELF #26, Mach-O #56). Refines #16 | Bound each table (`offset + count*size ≤ file size`) before allocating; bogus ⇒ graceful skip; add the missing `fread` check. **Verified**: `huge`/`1000`-symbol cases now print `[ ECOFF: bogus f_nsyms/f_symptr ]` and skip (no OOM), a valid 1-symbol case still loads |
| 60 | `core/emul.c` | **gzip temp reopen race (P3, external audit)**: the gunzip helper `mkstemp`'d the temp, **closed** it, then the child `open()`ed it again **by name** — a same-user symlink/replace race on that path (the `--`/PATH/no-shell hardening of #42/#43 was already in). Completes #42/#43 | Pass the open `mkstemp` fd to the child and `dup2()` it to stdout instead of reopening by name. **Verified**: a gzipped ELF still loads identically to the raw file |
| 61 | `devices/makeautodev.sh` | **Flaky parallel build (build robustness, found this session)**: the recursive-make chain (`all`→`objs`→`autodev.o`) can run `makeautodev.sh` concurrently; it appended to `autodev.c` non-atomically, so two runs interleaved and dropped a line's first `printf`, corrupting a random `device_register`/`pci_register` entry → intermittent `make` failure (`expected ';' before ')'` at a moving line). This is why a stock `make -j` failed nondeterministically | Build into a PID-unique temp file, then atomic `mv` into place. **Verified**: 24 concurrent runs all produce a correct 76-entry file; clean `make -j` now succeeds |
| 62 | `file/file_macho.c`, `file_ecoff.c`, `file_elf.c`, `include/misc.h` | **Sparse/huge-file allocation cap (judgment call after #58)**: the loader symbol/string-table allocations were bounded only by the file size (ELF #26, Mach-O #56/#58, ECOFF #59), so a **sparse multi-GB file** could pass that bound and still drive a (file-bounded) `malloc` to OOM | Added a shared 256 MB `LOADER_MAX_TABLE_BYTES` cap (`misc.h`) and reject any symbol/string table larger than it, in all three loaders. **Verified**: a 512 MB file with a 360 MB symtab is now rejected in 46 ms (`bogus LC_SYMTAB sizes`) instead of attempting the 360 MB allocation |
| 63 | `file/file_macho.c` | **Command shorter than the fields it declares (P2/P3, external audit)**: #57's per-command bound checked `pos+need` against the data, but a command declaring `cmd_len == 8` for LC_SYMTAB/LC_UNIXTHREAD could still make the parser read fields *outside* the declared command (into later file bytes) | Also require `cmd_len >= need` in the per-command guard. Refines #57 |
| 64 | `file/file_macho.c` | **Signed `int32` fields reused for the allocation (P2, external audit)**: #58 bounds-checked uint64 *copies*, but `malloc(12 * nsyms)` / `calloc(strsize + 1)` / `fread` still used the signed `int32_t` `nsyms`/`strsize` directly (`12 * nsyms` computed in `int` → overflow for large values) | Do the alloc/read arithmetic in `size_t` (`(size_t) nsyms * 12`, `(size_t) strsize + 1`); the #62 cap also bounds the values so the products can't overflow; the symtab `fseek`s also cast offsets `(long)(uint32_t)` so a valid file with an offset ≥ 0x80000000 seeks correctly (not negative — codex compat caveat). Refines #58 |
| 65 | `devices/dev_pvr.c` | **Guest→host OOB write (P1, external audit)**: `pvr_render()` (STARTRENDER) takes `fb_base` straight from the guest register `FB_RENDER_ADDR1` and does `memset(d->vram + fb_base, 0, xsize*ysize*bpp)` with **no bound** — a high or sign-flipped value, or a frame larger than the 8 MB VRAM, writes before/after the host VRAM allocation (the triangle rasterizers reuse the same `fb_base`) | Bound `fb_base >= 0` and `fb_base + frame_bytes <= VRAM_SIZE` at the top of `pvr_render`; skip the render on violation (the per-triangle writers already wrap with `% VRAM_SIZE`) |
| 66 | `file/file_ecoff.c` | **MS-COFF long-name read unbounded (P3, external audit)**: after the symbol table is bounded (#59), the long-name lookup still computes `ofs = f_symptr + altname + sizeof(ms_sym)*f_nsyms` (file-controlled `altname`), `fseek`s there and hard-`exit(1)`s if the 300-byte `fread` is short | Bound `ofs + sizeof(name) <= file_size` and skip the symbol (no `exit`) on out-of-range or short read. Refines #59 |
| 67 | `devices/dev_pvr.c` | **Performance optimization (not a bug fix; user-approved)**: the alt-VRAM write path called `pvr_extend_update_region(d, addr, addr)` **once per byte** (its own comment: *"probably ultra-slow… should not be called for every byte"*) | Track the touched min/max **per VRAM bank** (the twiddle splits writes across two 4 MB banks) and extend the dirty region **once per bank** afterwards — far fewer calls, and without dirtying the 4 MB gap when a write hits both banks. `fb_update_y1/y2` is a line *range*, so within a bank this matches the per-byte result except for writes straddling the visible-FB edge (a few extra lines, redrawn identically) |
| 68 | `devices/dev_pvr.c` | **Guest→host heap overflow (P1, external proposal)**: `pvr_geometry_updated()` had an **inverted** condition — `if (d->vram_z == NULL)` under a *"Scrap Z buffer if we have one"* comment — so on a guest resolution change the OLD (smaller) Z buffer was **kept**, and `pvr_render()` then wrote the new `xsize*ysize` doubles into it → heap overflow when the new resolution is larger | Free + NULL the stale Z buffer on geometry change (condition becomes `!= NULL`) so `pvr_render` reallocates it at the new size; also wrap that render allocation in `CHECK_ALLOCATION` |

The highest-severity items are **#3** (shell injection) and the guest-reachable
out-of-bounds **writes** into host memory: **#8** (framebuffer, found via the `-O3`
`-Wstringop-overflow` warning), **#49** (the CRITICAL unbounded SCSI DATA_OUT write),
**#65** (PVR STARTRENDER `fb_base`), and **#68** (PVR stale Z-buffer kept across a
guest resolution change — both PVR writes from the latest rounds).

## Static-analysis sweep (`gcc -fanalyzer`, all 265 TUs)

46 analyzer findings, triaged:
- **Fixed** (real, above): `file_srec.c` uninitialized reads (8 findings), `dev_fb.c`,
  `diskimage.c` overlay leaks.
- **Fixed:** `dev_osiop.c` (5× NULL-deref of `d->xferp` — see correction #10).
- **Fixed:** `dev_pvr.c` (4× — `realloc`/`malloc` NULL-checks + zero-init of the
  `wf_*` triangle-strip arrays; see correction #12).
- **False positives (left as-is):** `settings.c:408` "double-free" (the `memmove`
  overwrites the freed slot — no pointer freed twice); `net_ip.c:577` socket "fd
  leak" (the fd is owned by the long-lived `tcp_connections[]` slot); `device.c:339`
  (guarded by the `!= NULL` check one line above); numerous `malloc-leak` reports on
  allocations intentionally kept for the program's lifetime (machine/device names,
  `statistics.fields`, framebuffer titles, …).

## Fuzzing the loaders (ASan/UBSan + mutated fixtures)
No libFuzzer/clang is available here, so I built gxemul with
`-fsanitize=address,undefined` and fed mutated copies of the `test/FileLoader_*`
fixtures (byte-flips, truncation, header corruption, oversized 32-bit fields) into
the loader, watching for sanitizer reports. This **immediately found a real OOB
read (SEGV)** in the a.out loader — `add_symbol_name` ← `file_load_aout`
(correction #14) — a caller-controlled `str_index` indexing past the string
table. The **identical pattern existed in the ELF, ECOFF and Mach-O** symbol
loaders; all four are fixed (#14–16). UBSan additionally flagged the generator
shift UB (#13). A first re-fuzz confirmed the `str_index` fixes but surfaced a
**second** a.out bug — the i960 b.out `symbsize` was signed → UB + an absurd
`malloc` (#17); after fixing that, a further re-fuzz of all 7 fixtures (420 cases)
is clean. Coverage note: the fixtures exercise ELF + a.out directly; ECOFF/Mach-O
were fixed by code inspection of the same pattern (no fixtures).

## Fuzzing the network stack (in-process harness)
An in-process ASan/UBSan harness (`harness_net.c`, linked against every object but
`main.o`) drives `net_ethernet_tx()` — the guest→network path that parses
ARP/IP/TCP/UDP — with mutated ethernet frames. The first run flagged a **signed
left-shift UB** in the TCP/IP byte assembly (`packet[N] << 24`, 6 sites — #22).
After fixing those, **500,000 mutated packets produce 0 UBSan errors and 0 ASan
memory errors**: the (author-acknowledged "ugly") TCP/UDP code has no memory-safety
fault under this fuzzing.

## Machine-setup ASan sweep
Running **23 machine types/subtypes under ASan** (machine setup runs before the
file loader, so any small ELF reaches it) found the macppc heap-overflow (#23) and
several signed-shift UBs in setup/PROM/dyntrans code (#24, #25). Crucially, across
all 23 machines there were **no other ASan memory errors** — the macppc OOB was the
only memory-safety bug; everything else is the low-severity (deterministic on
two's-complement) shift-UB class. Note: signed `byte<<24`-style assembly is
pervasive in this codebase; the fixes target the spots actually exercised by setup
and the fuzzers, not every occurrence.

## Guest-OS boot validation
The 26 fixes are **behavior-preserving**: real NetBSD 8.2 guests boot on the
hardened `build/gxemul` across **all four CPU families** (kernels from
archive.netbsd.org, run on a pty so the console is captured):

| OS / machine | CPU | Result |
|---|---|---|
| NetBSD/pmax (3max) | MIPS R3000 | boots → sysinst installer (`Terminal type? [vt100]`) |
| NetBSD/arc (pica) | MIPS R4000 | boots, full device probe |
| NetBSD/hpcmips | NEC VR4100 | boots |
| NetBSD/sgimips (o2) | MIPS R10000 | boots (`boot device: mec0`) |
| NetBSD/macppc (g4) | PowerPC + OpenFirmware | boots (OF emulation; macppc #23 fix held) |
| NetBSD/landisk | SH4 | boots (`root file system type: ffs`) |
| NetBSD/cats | ARM SA-110 | boots (footbridge/PCI/VGA device probe) |
| NetBSD/algor (p5064) | MIPS RM5200 | boots |
| **OpenBSD/luna88k** | **Motorola M88100 (M88K)** | **boots** (`OMRON LUNA-88K2`, `M88100 rev 0x3, 2 CMMU`) — a 2nd OS family **and** the 5th CPU arch |
| **Linux 3.2 / Malta** (evbmips) | MIPS 5Kc | **boots** (kernel init, `3.45 BogoMIPS`, Security Framework) — a **3rd OS family** (needs the little-endian kernel; `-o 'console=ttyS0'`) |

Coverage now spans **5 CPU architectures** (MIPS, PowerPC, SH4, ARM, M88K) and **3 OS
families** (NetBSD, OpenBSD, Linux). Even OpenBSD 7.7 (2025) — far newer than GXemul 0.7.0
(2021) — boots, exercising the M88100 core + LUNA-88K2 devices.

Also confirmed: the external audit's 10 crashing ELF cases now run with **0 ASan
crashes** after correction #26.

### Per-device runtime fuzz (guests booted under ASan)
Booting NetBSD under the **ASan** build lets the real guest drivers exercise each
device model (probe, DMA, register I/O, interrupts). Across **pmax** (asc/le/dz/fb/
mcclock), **sgimips** (mec/crime/mace), **cats** (footbridge/tlp/aceride/vga) and
**landisk** (SH4): **0 ASan memory errors.** The device emulation is memory-safe
under real driver traffic. The only runtime sanitizer hit was a UBSan signed-shift
in the **ARM CPU core** (`cpu_arm_instr_loadstore.c:297` — `byte<<24` word-load
assembly): the pervasive deterministic shift-UB class in the hottest code path,
documented but not chased (fixing one site is whack-a-mole across every CPU core).

## Verified OK (no change needed)
Segment-loading paths use `CHECK_ALLOCATION` + self-bounding `fread`; device
register dispatch is `switch(relative_addr)`-bounded; string handling uses
`snprintf`/`strlcpy`. No format-string misuse. (The symbol-*table* parsing was the
exception — see fuzzing, above.)

---

## Latest external-audit rounds (#57–#66): Mach-O / ECOFF / gzip / build / PVR
A further external audit surfaced four residual loader issues plus a build-system
flake; all are now fixed (#57–#61), the primary gcc `-O3 -Wall -Wextra` build stays
**0/0**, and each fix is **verified by re-running the audit's own focused regression
cases against the rebuilt binary**:

- **Mach-O compact `LC_UNIXTHREAD` (#57)** — the 204-byte `macho_valid_thread_compact_204`
  case went from `rc=1` *"No entry point? Aborting"* to **executing** (`rc=124`, runs);
  a genuinely-truncated 160-byte thread and a `cmd_len==0` case are still rejected.
- **Mach-O `LC_SYMTAB` products (#58)** — `…_symbols_extend_past_eof` and
  `…_strings_extend_past_eof` went from a hard `exit(1)` to **gracefully skipping**
  the bad symtab and continuing (`rc=124`); `huge_symtab_fields` still reports
  `[ Mach-O: bogus LC_SYMTAB sizes ]`.
- **ECOFF allocations (#59)** — `ecoff_huge_f_nsyms` / `ecoff_f_nsyms_1000` now print
  `[ ECOFF: bogus f_nsyms/f_symptr ]` and skip (no OOM / huge `malloc`); a valid
  1-symbol case still loads.
- **gzip fd-passing (#60)** — a gzipped ELF loads identically to the raw file
  (decompression still works; the reopen-by-name race is gone).
- **Build race (#61)** — 24 concurrent `makeautodev.sh` runs all yield a correct
  76-entry `autodev.c`, and a stock `make -j"$(nproc)"` now builds reliably (it had
  been failing nondeterministically at `autodev.c`).
- **Real ASan/UBSan rebuild (#57–#59):** a genuinely instrumented rebuild (103 MB
  binary, `-fsanitize=address,undefined`) running the Mach-O + ECOFF cases reports
  **0 AddressSanitizer/UBSan memory errors** — the only ASan output is a benign,
  identical 300-byte LeakSanitizer report at the `exit(1)` reject paths (machine
  state not freed on abort; pre-existing, unrelated to the fixes). *Caveat:* the
  audit's bundled `gxemul-asanubsan` is 5.96 MB with no `-fsanitize` on its compile
  lines, i.e. it was **not** actually instrumented, so that audit's "0 sanitizer
  reports" reflects a plain build.

**Second round (#62–#66, this session):** a follow-up audit found a guest→host OOB
write in the PVR plus four loader refinements; all fixed, primary build still **0/0**:

- **PVR STARTRENDER (#65, P1)** — `pvr_render` now rejects an out-of-VRAM
  `fb_base`/frame before the `memset` (and the rasterizers reuse the same `fb_base`).
  Verified by code inspection and a clean primary + ASan rebuild (it compiles cleanly
  under ASan); the OOB path itself needs a Dreamcast guest to exercise at runtime, so
  it is not covered by the loader regression set.
- **Loader allocation cap (#62)** — a 512 MB file with a 360 MB symtab is rejected in
  **46 ms** (`bogus LC_SYMTAB sizes`) instead of attempting a 360 MB allocation.
- **Mach-O `cmd_len >= need` (#63), size_t alloc arithmetic (#64), ECOFF altname
  bound (#66)** — re-running the full focused regression set is **unchanged** (compact
  thread still executes; truncated / `cmd_len==0` / extend-past-EOF behave as in round
  one), confirming these tightenings introduced no regressions.

> **Note on `audit-results-20260627_current-review/`:** that directory holds **pre-fix**
> snapshots — its recorded `*.out.txt`/`summary.json` show the *old* behavior (e.g.
> `macho_valid_thread_compact_204` = "No entry point", the symtab EOF cases as hard read
> failures, the sparse case as OOM). The **input cases are reusable**, and the
> verification above is a *fresh re-run* of those inputs against the rebuilt binary — so
> the stale recorded outputs should not be read as current.

## Third round (#69): arc/Jazz interrupt-enable mask — guest-compat correctness (Codex-assisted)
A cross-arch exercise (running OpenBSD/arc 2.3 on the Acer PICA-61, `-E arc -e pica`) surfaced a real
correctness bug in the Jazz/R4030 interrupt controller, `dev_jazz.c`. The controller forwarded JAZZ
interrupts to the MIPS IRQ lines **ignoring `int_enable_mask`**: `jazz_interrupt_assert()`/`deassert()`
drove `mips_irq_3` (JAZZ 0..14) and `mips_irq_6` (JAZZ 15 = interval timer) unconditionally, and
`DEVICE_TICK(jazz)` gated the timer on `& 2` (the `/* Hm? */` "the mask seems shifted" TODO) instead of
the real JAZZ-15 bit `0x8000`. So the free-running 100 Hz Jazz timer raised a clock interrupt before the
guest had enabled it; OpenBSD/arc then entered `hardclock` before `cpu_initclocks()` and faulted
(null-deref `[0]+0xb8` at `hardclock+0xac`). **Diagnosis** (gxemul debugger): bp at `cpu_initclocks`
(0x801b77a8) never hit before the fault; the firing IRQ was Cause IP6. **Root cause found by Codex
(gpt-5.5, high effort)** reading the source after a long manual hunt — the missed detail was that
`jazz_interrupt_assert()` never consulted the enable mask. **Fix (#69, `dev_jazz.c`):** add
`PICA_TIMER_IRQ_MASK (1<<15)`; AND `int_enable_mask` into the assert/deassert forwarding and the DEVICE_TICK
gate; use the mask define in the `EXT_IMASK` recompute; route the pending-tick assert via `jazz_timer_irq`.
**Result:** OpenBSD/arc 2.3 now boots to the kernel idle loop on 0.7.0 (previously only gxemul ≤0.3.6 did;
0.3.7's dyntrans rewrite regressed it). **pmax unaffected** (DECstation uses `dev_mc146818`, R3000/EXC3K) —
re-verified pmax boots multiuser (root login, inetd) on the same rebuilt binary. Builds 0/0; `src/`
baseline untouched. Tooling: `gxemul_arc_audit/arc_audit.sh bootcheck` (BOOTED vs FAULTED via debugger PC
sampling over the serial PTY).

> **Workflow note:** `build/` is a copy of `est/src`; on the `/mnt/c` 9p mount, Windows-side edits lag the
> WSL view and `make` links **stale** `.o`. Edit est/build sources *from WSL* (or `make clean`) and verify
> with `strings build/gxemul`. This masked the working fix through several iterations.

---

## Fourth round (#70–#88): outstanding-bug remediation (Codex `gpt-5.5` *xhigh* + independent audit)
A dual read-only Codex review (`gpt-5.5`, effort high + xhigh) of the whole tree produced 24 ranked
candidates (`OUTSTANDING_BUGS.md`, OB-1..OB-24). Each was **independently verified against the current
source before implementing** — Codex proposed, the audit decided. Outcome: **19 fixed (#70–#88), 3 false
positives, 1 deferred, 1 skipped.** Full per-fix detail is in `CHANGELOG.md`; the OB→# map is in the
`OUTSTANDING_BUGS.md` header. Highlights:

- **Two root patterns** dominated the HIGH set: *end-span* (start offset checked, then `memcpy`/index
  `len` bytes — #70 dev_fb, #76 mardigras microcode, #77 pcc2-after-modulo) and *window>backing* (MMIO
  window registered larger than the backing array, so `memory_rw.c`'s clamp to the window still allows
  OOB — #71 px SRAM, #78 pmagja, #81 vga 8-bit). Guest-controlled indices/append were the rest
  (#73 adb, #74 igsfb, #75 kn01, #79 sgi_gbe, #82 vga CRTC charcells).
- **The triage mattered.** OB-4/5/10 were proven **false positives**: `cpus/memory_rw.c:288` clamps
  `len` to the device length before the handler runs, and `pvr_vram`/`asc_dma`/`ether_buf` register
  length == backing size with no direct callers — so their "end-spans" are unreachable. (Guards
  speculatively added in an early batch were **reverted** once the clamp was confirmed, keeping the
  patch limited to real bugs.) The window>backing cases are real *because* their window exceeds backing.
- **Loaders** (apply to every guest): #84 file_android rejects div-by-zero/oversized `page_size`;
  #85 file_elf widens the PT_LOAD cursor (`int ofs`→`uint64_t`) so a ≥2 GiB segment can't overflow it.
- **#82 (vga CRTC)** corrected an off-by-one in Codex's draft: the redraw indexes `charcells[base+i]`
  *and* `[base+i+1]`, so the bound must reserve the `+1`; casts keep `-Wsign-compare` clean.
- **#72 (px STAMP DMA)** is the one HIGH fix that is **compile-verified only** (no PX/TURBOchannel test
  guest): coordinates are signed and `%=`-negative, so instead of Codex's coordinate clamps (which
  missed negatives) each of the three framebuffer writes got an explicit in-bounds row/col guard.
- **Deferred:** OB-22 (jazz jazzio vector-ack) is emulation correctness (not host-OOB), medium
  confidence, and lives in the #69 arc interrupt path — deferred to protect the verified arc boot.
- **Re-verification:** built `-O3 -Wall -Wextra` 0/0 after every batch; pmax boots to multiuser/root
  login/clean halt; arc OpenBSD 2.3 ELF (`bsd`) loads with symbols and runs to the console driver
  (`<pccngetc>`, past the #69 hardclock point) and ECOFF (`bsd.rd`) runs in-kernel — both fault-free,
  confirming #82 (VGA) and #85 (ELF loader) did not regress arc. `src/` baseline untouched.

---

## Fifth round (#89–#94): multi-model review — Codex `gpt-5.5`/xhigh + agy `Gemini 3.1 Pro`/High + Claude consensus
A three-engine review of the full `src/`→`est/src/` hardening diff (70 files). Codex CLI and Google
Antigravity (`agy`) each reviewed independently; Claude then verified every finding against source and
ran a **consensus rebuttal loop** — each verdict Claude disputed was sent back through *both* models,
which **conceded all three disputes**. The two engines surfaced almost-disjoint real bugs (validating
the multi-engine approach). Net: **6 confirmed fixes (#89–#94), 3 false positives, 2 lower-severity
items deferred.** Clean rebuild (Gentoo WSL, `-O3 -Wall -Wextra`): **0 errors / 0 warnings.**

**Confirmed & fixed:**
- **#89 `dev_px.c` (CRITICAL, Codex)** — completes OB-3/#72. The STAMP clear/fill guarded the
  framebuffer `memcpy` but not the preceding `memset(pixels, attr, (x2-x)*bytesperpixel)`: `x`/`x2` are
  guest DMA values and only `x2-x > PX_XSIZE` was clamped, so a guest setting `x2 < x` made `(x2-x)` a
  huge `size_t` → host **stack** overflow of `pixels`. Fix: `if (x2 < x) x2 = x;` before the fill.
- **#90 `cpu_mips_instr.c` (Codex)** — completes the nested-delay-slot fix (#41/#47), which guarded the
  canonical branch handlers but **not** the dyntrans *fused* variants `beq/bne/b_samepage_addiu` and
  `beq/bne_samepage_nop`. A fused branch in another branch's delay slot still corrupted `next_ic`. The
  same `TO_BE_DELAYED → EXCEPTION_IN_DELAY_SLOT` guard was added to all five (after the declarations).
- **#91 `dev_vga.c` (Codex + agy)** — completes OB-15/#81. On an out-of-range 8-bit write the bounded
  `memcpy` is skipped but `modified=1` was still set, so `vga_update_graphics()` (no bound on
  `gfx_mem[addr]`) later read OOB; and an out-of-range read left `data` uninitialized. Fix: set
  `modified` only when the copy runs; `memset(data,0,len)` on the skipped read.
- **#92 `file_aout.c` (Codex)** — `strings_len` is `uint32_t`, so `malloc(strings_len + 1)` wraps to
  `malloc(0)` at `0xffffffff`, then `string_symbols[strings_len]='\0'` writes ~4 GB out. Fix: size in
  `size_t` — `malloc((size_t)strings_len + 1)`. (Narrow: needs a ~4 GB a.out, but real UB.)
- **#93 `dev_pcc2.c` / #94 `dev_pmagja.c` (agy)** — complete OB-11/#77 and OB-12/#78. The out-of-range
  guard skipped the copy into the guest-read `data` but still returned success → uninitialized host
  memory leaked to the guest. Fix: zero `data` / `data[i]` on the skipped read.

**False positives — Claude-flagged, both models conceded in the rebuttal loop:**
- *jazz timer mask* (Codex): the `& 2 → & PICA_TIMER_IRQ_MASK` change *is* the intended, runtime-verified
  #69 fix (OpenBSD/arc boots; `& 2` was the bug), not a regression.
- *`dev_px.c` COPYSPANS memmove* (agy): `span_len` is already clamped to `PX_XSIZE`; the copy is ≤ one
  row starting at a valid row → in bounds.
- *`m88k_ext` `o+w>32`* (agy): the rewritten unsigned-mask extract (#46) is *defined* and correct for
  every normal encoding; the original was UB in that corner. Low edge case, not a regression — left as-is.

**Deferred (recorded in OUTSTANDING_BUGS.md, OB-25/OB-26):** diskimage temp-file TOCTOU (reopened by
name; local-only) and the osiop `exit(1)` on a guest-reachable state (host DoS, but it replaced a worse
null-deref; #10).

**Tooling note (checkers):** `agy`/Gemini 3.1 Pro **refused** the CPU chunk under an offensive-security
framing (needed reframing as plain correctness QA), emits findings only to its transcript
(empty stdout in headless `--print`), and mixes **hallucinated** placeholder findings (fake paths like
`src/cpu/cpu_mips_map.c`) into checkpoint summaries — only its *final* answer is reliable. Codex ran
clean headless. Every accepted finding was verified against source before acceptance.

---

## Sixth round (#96–#100): Phase-B new-surface audit (PROMs / framebuffer renderers / disk parsers) — 3-agent fan-out + Claude verification
Three parallel audit agents swept surfaces the prior rounds hadn't: the non-arcbios/of PROM emulators,
every framebuffer/video renderer, and the disk-image + config parsers. Claude verified each finding
against source before fixing. **5 confirmed & fixed (#96–#100); PROMs + config parser CLEAN; 7 agent
candidates deferred to OUTSTANDING_BUGS (OB-27..33) pending exact-fix verification.** Build 0/0.

- **#96 `dev_kn01.c` (med):** `DEV_VDAC_OVERRA` set the overlay-palette *read* index from a guest byte
  with no mask; `DEV_VDAC_OVER` then did `memcpy(..., rgb_palette_overlay + 3*idx, 3)` into a 16-entry
  (48 B) array → OOB read (idx→255, offset 765). The *write* index was masked in #75; the read index was
  missed. Fix: `& 15` (OB-8b).
- **#97 `disk/bootblock_apple.c` (high):** `n_partitions = buf[0x207]` (guest disk byte, 0-255) drove a
  `do…while(partnr<n_partitions)` loop with `ofs = 0x200*(partnr+1)` over a 32 KB stack `buf` → `ofs`
  reaches ~130 KB → large OOB **stack** read (crash + disclosure via `debug %s`). Reachable from
  `emul.c`→`load_bootblock` on a malformed Apple-partition disk. Fix: bound the loop + `%.32s`.
- **#98 `dev_vga.c` (med):** `vga_update_graphics()` read `gfx_mem[addr]` unbounded; in 4-bit mode the
  redraw region can exceed the buffer → OOB read painted to screen. Fix: bound the 8-bit and 4-bit reads
  against `gfx_mem_size` (complements #91's write-side fix).
- **#99 `dev_ps2_gs.c` (CRITICAL):** `regnr = relative_addr/16` (0x2000 window → up to 511) indexed
  `reg[N_GS_REGS=264]`; the default-case `reg[regnr]=idata` is a **guest-controlled 64-bit OOB heap
  write** (~2 KB past the array). Fix: reject `regnr >= N_GS_REGS`.
- **#100 `dev_sgi_re.c` (high):** `horrible_getputpixel()` did `memory_rw(buf, bufdepth, …)` with
  `bufdepth = 1<<((mode>>8)&3)` up to 8 into `uint8_t buf[4]` → **stack overflow** (guest tile data on
  read); plus `tile_nr` (up to 271) indexed `re_tlb_[abc][256]`. Fix: `buf[8]` + bound `tile_nr < 256`.

**CLEAN (verified):** all 6 non-arcbios/of PROMs (dec_prom read/bootread use matched malloc/transfer +
guest-bounded `store_buf`; getenv/printf snprintf-bounded); `core/emul_parse.c`; `core/emul.c`; most fb
devices (bt45x/bt431/sfb/gbe/mardigras/px/pmagja/dec21030 carry prior bounds).

**Tooling:** scan-build (clang analyzer) whole-tree = 0 real runtime findings (6 reports, all build-time
codegen tools). CodeQL + qemu-system-mips (CPU differential testing) unavailable here; the uninit class
was instead closed at the root in #95.

---

## Seventh round (#101–#105): Phase-C deeper audit (network / storage-SCSI / remaining devices + dyntrans) — 3-agent fan-out + Claude verification
Three agents swept the surfaces not covered by Phase B: network devices + the NAT/IP stack, the SCSI/ATA/
disk command paths, and the remaining (non-fb/PROM) device handlers + CPU dyntrans. Claude verified each
finding. **5 fixed (#101–#105): 2 CRITICAL + 1 HIGH + 2 lower; 1 candidate deferred (OB-34).** Build 0/0.

- **#101 `dev_scc.c` (CRITICAL):** `port = relative_addr/8` was unbounded; the 0x1000 window gives port
  up to 511 vs SCC arrays `[N_SCC_PORTS=2 * N_SCC_REGS=16]`, so `scc_register_w[port*16+sel] = idata` is a
  **guest 64-bit OOB heap write** ~8 KB past the array (+ OOB reads of the other SCC arrays). Sibling
  `dev_z8530.c` masks correctly. Drives the DECstation 5000/1xx serial. Fix: `% N_SCC_PORTS`.
- **#102 `net/net.c` `net_arp` (CRITICAL):** ARP/RARP reply did `memcpy(lp->data+14, packet, len)` into a
  74-byte (60-usable) heap buffer with `len` = guest ARP frame length (up to ~65 KB) → controlled heap
  overflow, reachable in the default NAT config. Fix: clamp the copy to the 60-byte body.
- **#103 `net/net_ip.c` `net_ip` (HIGH):** the guest IP length field shrinks `len` with no lower bound, so
  `net_ip_udp`'s `sendto(..., packet+42, len-42, …)` underflows to a huge `size_t` (and `net_ip_icmp`
  writes its reply checksum past a too-small buffer). Fix: reject packets shorter than IP+L4 headers
  (ICMP/UDP ≥ 42, TCP ≥ 54).
- **#104 `disk/diskimage_scsicmd.c` READ_TOC (med):** a guest TOC allocation length 0-7 sized `data_in`,
  then 8 fixed header bytes were written → OOB heap write. Fix: allocate ≥ 12 but report only `retlen`.
- **#105 `dev_asc.c` (low):** the unfinished non-DMA DATA_IN path dereferenced `incoming_data`, never
  allocated → guest-triggerable NULL deref (DoS). Fix: NULL guard.

**CLEAN (verified):** dec21143/le/sgi_mec/mb8696x/ether NIC paths; net_ether/misc/tap; diskimage.c, wdc,
mb89352, the asc/osiop DMA paths (#49-52 bounds hold); mc146818/mk48txx/ioasic/z8530/ns16550/8259/8253/
bus bridges/RTCs; and the dyntrans core + loadstore (the nested-delay-slot family incl. the #90 fused MIPS
handlers — independently re-verified).

**Deferred (OB-34):** the SCSI CDB handlers read fixed `cmd[]` offsets (up to cmd[8]) without validating
`cmd_len` for short CDBs → OOB read of the controller-sized `cmd` buffer; best fixed with a per-opcode
CDB-length table under its own regression.

---

## Eighth round (#106–#113): OB-27..34 remediation (deferred Phase-B/C candidates, Claude-verified + fixed)
The 8 agent candidates deferred from rounds Six/Seven were each verified against source (**all 8 confirmed
real**) and fixed. Build 0/0; pmax (boots from a SCSI disk → exercises #113) + arc regression-clean.
- **#106 `dev_fb.c` (OB-27, high):** `framebuffer_blockcopyfill` copy clipped dst x1/x2 + from_y but not
  the source column `from_x` → `memmove` source ran past the framebuffer (via ps2_gif blockcopy / igsfb
  scroll). Fix: clip `from_x` to the line.
- **#107 `dev_pvr.c` (OB-29, med):** the 24-bit `pvr_fb_tick` copy wrapped only the start, not the span →
  read past the 8 MB VRAM. Fix: size_t cast (handles negative ofs) + clamp the length to `VRAM_SIZE-vo`.
- **#108 `dev_ps2_gif.c` (OB-28, high):** the TA-putchar loop read `data[(24+y*xsize)*4 + …]` (guest
  xsize/ysize) unbounded vs the input `len` → OOB read of the host DMA buffer. Fix: `break` when `addr+3 > len`.
- **#109 `bootblock_iso9660.c` (OB-30, med):** the dir-record walk read the 8-byte header + name past
  `dirbuf`. Fix: require the header fits + clamp the name to the remaining buffer.
- **#110 `bootblock_iso9660.c` (OB-31, med):** `if (i < len - strlen(filename))` underflowed `size_t`.
  Fix: `i + strlen(filename) <= len`.
- **#111 `bootblock.c` (OB-32, low):** `fatal()` does not exit, so the disk-controlled `n_blocks*512` size
  check didn't stop the int-overflow/malloc-abort. Fix: cap `n_blocks` to [1,128].
- **#112 `diskimage.c` (OB-33, low):** `%i` passed a `char*` (`diskimage_types[type]`). Fix: `%s`.
- **#113 `diskimage_scsicmd.c` (OB-34, med):** only `cmd_len >= 1` was checked before reading fixed CDB
  offsets up to `cmd[8]` → OOB read of the controller-sized `cmd[]` on a short CDB. Fix: validate `cmd_len`
  against the CDB group length (`cmd[0]>>5` → 6/10/10/6/16/12/6/6).

---

## Ninth round (#114–#115): OB-25 / OB-26 remediation (the last two low-severity candidates)
- **#115 `disk/diskimage.c` (OB-25, low):** the `-d …R:` read-only-overlay path created its temp data +
  `.map` files at predictable `getpid()`-based names, then `diskimage_add_overlay()` reopened them by name
  → a local caller could pre-plant a symlink at the guessable path in the close→reopen window (TOCTOU).
  Fix: create the data file with `mymkstemp()` (unpredictable /dev/urandom suffix, atomic O_CREAT|O_EXCL)
  and the `.map` exclusively, so the path can't be guessed/pre-planted.
- **#114 `devices/dev_osiop.c` (OB-26, low):** the #10 NULL-`xferp` guard called `exit(1)` on a state a
  guest can drive (SCSI data phase with no active transfer) → a guest could halt the emulator. Fix: skip
  the data phase (`debug` + `else`) instead of dereferencing `xferp` or exiting.

With this, **every OUTSTANDING_BUGS candidate (OB-1..34) is resolved.** Build 0/0; regression: the pmax
full-boot rig + a multi-arch boot sweep (MIPS pmax/arc/sgimips/hpcmips + Linux/Malta, PPC macppc, ARM
cats, SH landisk) all clean.

---

## Tenth round (#116): PowerPC extended BAT (IBAT4-7 / DBAT4-7) support — Codex + agy + Claude consensus
A *capability addition* (not a bug fix): the 7445/7455 extended block-address-translation registers, which
GXemul never implemented. Surfaced by the macppc/NetBSD-8.2 investigation — the kernel programs IBAT4-7/
DBAT4-7 for its MMU, GXemul dropped the writes, so the mappings were inert and the kernel stalled.
**Process:** Claude drafted; Codex + agy reviewed (agy APPROVE, Codex APPROVE-WITH-CHANGES → "gate it");
a consensus re-confirmation round agreed on **HID0[HIGH_BAT_EN] gating** (mask 0x00800000 — both engines
independently gave the same bit); both then gave **APPROVE FOR COMMIT** on the final diff.
- **#116a `cpu_ppc.c`:** widen the SPR known-register filter to accept `SPR_IBAT4U..SPR_DBAT7L`
  (0x230-0x23f), so the writes are stored without the spurious `UNIMPLEMENTED spr` warning (the generic
  `mtspr` already stored them).
- **#116b `memory_ppc.c`:** factor the BAT scan into `ppc_bat_block()` (faithful extraction of the original
  loop), scan the base BATs, then the extended block at 0x230 — but ONLY when `HID0[HIGH_BAT_EN]`
  (0x00800000) is set. The gate stops the aliased cache-debug SPRs (DC_ADR/DC_DAT/DC_CST at
  0x231/0x232/0x238) from spoofing a BAT on a non-745x guest.
**Regression (build 0/0):** OpenBSD 3.4/macppc still boots; full multi-arch sweep — NetBSD 8.2 cats(ARM) /
arc / hpcmips / sgimips(MIPS) / landisk(SH4), Linux 3.2 Malta(mipsel) — all BOOTED, `emu-crash=0`; pmax +
arc clean. A PPC guest that never sets HIGH_BAT_EN sees byte-identical behavior.
**Outcome / limitation (honest):** NetBSD 8.2/macppc on `-e g4` does NOT engage the gate — that path
advertises an MPC7400 (no extended BATs), so the kernel never sets HIGH_BAT_EN; it stalls at the same
OpenFirmware point as before (the extended BATs stay inert for it; the 18→2 drop in `UNIMPLEMENTED spr`
warnings is just the new SPRs being recognised). #116 is the correct, safe **foundation**. Actually
booting NetBSD 8.2/macppc additionally needs a 7445/7455 CPU model (addable safely as a new `-e g4plus`
subtype so `-e g4` stays unchanged) plus likely further OpenFirmware/device work (machine_macppc is
skeletal) — tracked as **OB-35**.

---

## Eleventh round (#117, OB-35): MPC7455 CPU model + `g4plus` macppc subtype — engages #116's extended BATs
Follow-up to #116 (user-requested; same Codex + agy + Claude consensus + regression discipline). #116's
HID0-gated extended BATs were inert for NetBSD 8.2/macppc because `-e g4` selects an MPC7400 (no high BATs),
so the kernel never set HID0[HIGH_BAT_EN]. #117 adds a 745x model the guest can opt into:
- **`cpu_ppc.h`:** new `PPC_CPU_TYPE_DEFS` row `{ "MPC7455", 0x80010000, 32, 0, 15,5,8, 15,5,8, 18,5,8, 1 }`
  (PVR = MPC7455 `0x8001<<16`; 32 KB 8-way L1 I/D, 256 KB 8-way L2, AltiVec).
- **`machine.h`:** `MACHINE_MACPPC_G4PLUS = 4`.
- **`machine_macppc.c`:** `MACHINE_DEFAULT_CPU` maps `G4PLUS`→"MPC7455"; `MACHINE_REGISTER` adds the
  `-e g4plus` subtype. **Purely additive** — `-e g4` (7400) and g3/g5 are untouched.
**Verified the gate now engages:** with a temporary one-shot debug in `ppc_bat()` (since removed), NetBSD
8.2 on `-e g4plus` **DOES set HID0[HIGH_BAT_EN]** → #116's extended BATs activate (gate-opened=1) → it
advances past the BAT/MMU layer; on `-e g4` the gate stays closed (gate-opened=0), proving the model gates
it correctly. **Consensus:** both Codex (gpt-5.5/xhigh) and agy (Gemini 3.1 Pro) gave **APPROVE FOR
COMMIT** (Codex cross-checked the NXP MPC7450/7455 manuals). **Regression (build 0/0):** OpenBSD 3.4/macppc
boots on BOTH `-e g4` and `-e g4plus`; full sweep cats(ARM)/arc/hpcmips/sgimips(MIPS)/landisk(SH4) + Linux
3.2 Malta all BOOTED; pmax + arc clean.
**Residual (honest):** NetBSD 8.2/macppc still does not reach its banner on `-e g4plus` — past the MMU it
stalls in GXemul's *skeletal* OpenFirmware (`machine_macppc.c` + `of.c` device-tree gaps). That OF work is
a separate, open-ended effort beyond OB-35's CPU-model scope.

---

## Twelfth round (#118, #119, #101/#114 refined): course-correction — silent masks made LOUD, ethos-aligned
A maximally-critical self-review (Codex + agy + Claude) asked whether our hardening fit GXemul's *ethos*.
Finding: the author's runtime policy is **warn VISIBLY (`fatal()` = printed, never exits; `debug()` = quiet
unless `-v`) and CONTINUE when sane, hard-EXIT only on truly unrecoverable state, but NEVER silently hide a
guest-triggered anomaly** (`fatal()` at src/core/debugmsg.c; ~756 `fatal()` in src/devices; `dev_scc`
default = `debug()` + continue; see [[gxemul-author-error-ethos]]). Our host-safety fixes had gone SILENT
(clamp/zero/skip with no message) — the one option the author never uses. **User directive:** keep ALL
bounds checks (untrusted ROMs cannot be validated, so the checks stay regardless of upstream intent), add
*just-enough* rate-limited verbosity in the author's style, and above all NEVER crash. Approach + each item
were passed through Codex (gpt-5.5/xhigh) + agy (Gemini 3.1 Pro); the user chose "keep both behavior
refinements." **No bounds check was removed.**
- **#118 `dev_osiop.c` (real host crash):** `read_word`/`read_byte`/`write_byte` dereferenced
  `memory_paddr_to_hostaddr()` with no NULL check (it returns NULL on a read miss) — a guest pointing the
  SCSI SCRIPTS engine at unmapped RAM crashed the host. Added a NULL guard + `osiop_hostpage_fault()`
  (warn-once `fatal()` + stop the local script via `scripts_running=0`; an early-return in
  `osiop_execute_scripts_instr` keeps the bogus fetch from reaching a `TODO; exit(1)`). No deref, no exit.
- **#101 `dev_scc.c` (refined):** the prior `% N_SCC_PORTS` was host-safe but ALIASED out-of-range offsets
  onto a valid port (wrong hardware). Now bounds-check + **NO-OP** out-of-range (read returns 0) + warn-once
  — same bound (no OOB into `scc_register_r[]`), no aliasing. (The author's SGI `0xf` remap is left
  untouched: his code, and not an OOB.)
- **#114 `dev_osiop.c` (refined):** the NULL-`xferp` data phase used a quiet `debug()` and then *fell
  through to fake "Transfer complete"*. Now warn-once `fatal()` + stop the script + return (no fake
  completion, no process exit).
- **#119 loud-once warnings** on every silent host-safety drop, rate-limited with a `static` first-N guard
  so a hostile ROM cannot flood (both engines confirmed GXemul is single-threaded, so `static` is
  sufficient): `dev_disk` (beyond buffer), `dev_pcc2` (beyond reg space), `dev_vga` (gfx read/write beyond
  `gfx_mem`), `dev_pmagja` (pixel ofs outside), `dev_ps2_gs` (`debug()`→first-N `fatal()` on out-of-range
  register), `dev_pvr` (first-N suppression on the existing `pvr_render` skip), `net.c` (oversized ARP/RARP
  frame). `#95` (generic `memory_rw` zero-fill) left UNWARNED by consensus — it cannot distinguish probing
  from a dropped fault and would flood benign boots.
**Regression (gcc build 0/0):** full sweep cats/arc/hpcmips/sgimips/landisk/luna88k/prep BOOTED + macppc
early + Linux Malta, **0 spurious course-correction warnings** in normal operation (the guards are inert
unless a guest actually goes out of range); pmax deep (osiop/disk/net: root + NAT 0% loss + disk cksum +
syslogd + clean halt) clean; arc past-hardclock.
**Cross-compiler validation (the author's compiler is clang/FreeBSD):** the whole est tree also builds with
**clang 21** — `-fgnu89-inline` accepted, `MAKE_RC=0`, **0 errors and 0 warnings in any file we changed**
(the only 3 clang warnings are pre-existing: generated `tmp_arm_r0.c` + the author's `dev_sh4.c`). Native
BSD/macOS *OS-axis* builds still need those hosts; the `fopen(...,"wx")` overlay-map path (#115) is the one
newer-libc dependency to smoke-test there.

**Commit-review (Codex + agy, 5 iterations → unanimous APPROVE FOR COMMIT):** the end-of-batch review caught
real bugs *in our course-correction edits* that no build/boot test surfaces (they need a crafted guest):
(1) **agy** found `dev_ps2_gs` #99 still did a bare `return 0` (skipped output + signalled a guest bus
fault) → fixed to `memory_writemax64(...,0); return 1;`. (2) **Codex** found `dev_pcc2`'s OOB-read guard
fell through to guest-reachable `exit(1)` in PCCTWO_IPL/MASK → converted those to warn-once + continue. (3)
`dev_disk`'s end-spanning clamp was still silent → made loud-once. (4) **#118 was incomplete across several
iterations**: a host-page fault during a MOVE still acted before stopping — Codex caught, phase by phase,
that the *instruction-fetch*, then *COMMAND/DATA_OUT* (incl. two guest-reachable `res==0` `exit(1)` →
warn+stop), then *DATA_IN/STATUS/MSG_IN* (phase-advance/transfer-free), then *MSG_OUT* (phase-advance) paths
all needed a `if (!d->scripts_running) return 1;` guard. **Final state:** every host-page-fault path in the
MOVE handler stops before acting (no diskimage call, free, phase advance, or fake transfer-complete); both
`res==0` exits gone; gcc 0/0; pmax boot-from-SCSI clean with 0 spurious warnings. **Honest residual:**
`dev_osiop` still has ~25 `exit(1)` for the author's *unimplemented-feature* MOVE forms (indirect/
table-indirect addressing, unaligned DSP) + setup paths — left as-is per consensus (these are the author's
deliberate "hard-exit on unimplemented/unrecoverable", not host-page-fault-driven, and out of #118's scope;
converting *every* guest-reachable `exit(1)` emulator-wide would be a separate, larger pass).

---

## Thirteenth round (#120–#129): feature additions + SuperH alignment
Additive `doc/TODO.html` work, each regression-gated: SuperH unaligned-access exceptions (#124) and 64-bit
`fmov` 8-byte alignment (#129); multi-track CUE/BIN CD images (#127); testmips RAM above 256 MB (#120);
subsystem-level `debugmsg` breakpoints (#128); and debugger conveniences — step-into-call, `find`/`put`,
expression and dump/disassemble-range fixes (#122/#125/#126). No memory-safety regressions; full boot sweep
and the pmax rig clean after each.

## Fourteenth round (#130–#154): full-project multi-model review + remediation
A whole-codebase (not just recent-changes) adversarial review of the **core-critical subset** — the four CPU
instruction cores, the shared dynamic-translation engine, the guest→host memory boundary + main loop, the
file loaders, network, disk, debugger, and the highest-risk devices — explicitly weighing the author's
warn-loudly / never-silently-mask ethos and the TODO wishlist. **Pipeline:** parallel per-subsystem Claude
review agents (each told to skip the ~119 already-fixed items and diff against the pristine baseline) → three
independent cloud models (GLM / DeepSeek-V3 / Qwen3-Coder) cross-checking the top findings against extracted
code → a Claude adjudicator ruling each finding *confirmed-real / already-handled / false-positive* against
the actual source. **Outcome: ~23 confirmed fixes (#130–#154), no surviving false positives, every one
pre-existing in the pristine baseline** (the prior hardening simply had not reached them).

**Headlines — 1 CRITICAL, 2 HIGH:**
- **#137 (CRITICAL) — MIPS `memset` instruction combiner (`cpus/cpu_mips_instr.c`).** An unsigned
  `end - start` underflow whose value *also* wrapped the page-boundary clamp → a direct multi-gigabyte
  `memset` into the host heap, bypassing the `memory_rw` length clamp; guest-triggerable on pmax. Fixed by
  falling back to the per-instruction path when `end < start` (which then faults safely on unmapped memory).
- **#145 (HIGH) — PVR framebuffer (`devices/dev_pvr.c`).** A guest→host heap **write**: the refresh copy was
  bounded to guest display geometry but not to the fixed host framebuffer allocation. Now clamped to both.
- **#149 (HIGH) — S-record loader (`file/file_srec.c`).** A host-stack **over-read** (~4 KB) into guest RAM
  from an over-long `count` field (a non-hex byte survives the warn-and-continue path). Clamped to the parsed
  record length; the parse loop itself proven un-overflowable.

**Medium/low tail:** an unbounded guest-set SCSI transfer size (OOM-exit DoS), a TCP timestamp-option
over-read echoed to the guest, a PPC Time-Base-Upper that never incremented, several recoverable
`dev_osiop` `exit(1)`s converted to warn-and-stop, `free()` on an `mmap`-backed allocation, plus format-string,
odd-length-checksum, NULL-deref, delay-slot-guard, FDIV-by-zero, divide-by-zero, CLI-argument, and
signed-shift-UB hardening. **Re-confirmed sound (no OOB):** the dyntrans engine, the `memory_rw` boundary,
and the ELF/ECOFF/Mach-O/a.out loaders. **Deferred** (confirmed, not host-safety, disproportionate fix risk):
a double-precision op on an odd FP register (stays within the FP register union) and the silent — but already
host-safe — nested-delay-slot guard. **Verification:** build 0/0; 9-machine multi-arch boot sweep; OpenBSD/pmax
full-boot + NAT rig; and a positive S-record over-read test (crafted record clamps; valid record loads clean).

---

## Fifteenth round (#155–#177) — Codex 5.6-Sol-Ultra review, Fable-verified (ported from est/)
A full-tree code review by **Codex CLI `gpt-5.6-sol`/ultra** (report `../harness/codex_sol_ultra_to_fable.md`):
**21 findings, all confirmed REAL by 4 Fable verifiers (0 false positives)**, applied as minimal ethos-matched
corrections + 2 companions (#176/#177). Developed and build-verified in `est/`, then ported here byte-identically;
the full ranked table is in `../est/CHANGELOG.md` (and `est/REVIEW_FINDINGS.md`). Headlines: **3 CRITICAL** —
framebuffer partial-page dyntrans OOB (bypassing #70), `dev_fb_resize` int-overflow → OOB write, SGI-GBE
fb-realloc use-after-free; **2 HIGH** — CUE path-traversal host-file read, tape uninitialized-heap disclosure;
then a MEDIUM tier (PVR/SCSI/net/loader/PROM DoS + OOB) and a LOW tail. #173 (overlay TOCTOU) deferred — not a
cross-user hole. **This fork builds 0/0** (`make -j12`, gcc 15.2.1, 2026-07-09) and the pmax rig **boots +
NAT-pings 0% loss + halts cleanly** on the rebuilt `gxsec-gxemul` — no regression.

## Sixteenth round (#178–#181) — NE2000 / NAT hardening (Codex 5.6-Sol-Ultra NE2000 review)
A focused Codex `gpt-5.6-sol`/ultra review of the new arc NE2000 NIC (`src/devices/dev_ne2000.c`) + its NAT/Jazz
surface (`../harness/codex_ne2000_to_fable.md`): **4 findings, all confirmed REAL by a Fable verifier (0 false
positives), 0 CRITICAL** — the device's earlier panel fixes (RX FCS, lost-interrupt, bounds-checked card memory)
re-confirmed sound. **#178 HIGH** — bound the NAT reply queue (drop-oldest cap) + drain a stopped/monitor NE2000
and make `STP` dominate `STA`, closing a guest OOM/`exit(1)`; **#179 MED** — de-`fatal()` the Jazz CONFIG/undefined
MMIO output sink; **#180/#181 LOW** — NE2000 TX source-span validation and remote-DMA stop-at-`RBCR==0`
(hardware-fidelity/hardening, no host OOB). Builds **0/0**; **both rigs regression-pass** (pmax `le0` + arc NE2000
`ed0` ping 0% loss, clean halt) on the rebuilt `gxsec-gxemul`.

## Seventeenth round (#182–#187) — full-tree Codex 5.6-Sol-Ultra + Fable panel (fb-resize CRITICAL)
A whole-tree re-review: **Codex `gpt-5.6-sol`/ultra** (17 findings) cross-checked against a **4-reviewer Fable panel**,
each finding source-verified. Headline is a **seam bug** the area-partitioned panel missed and the holistic Codex pass
caught: **#182 (CRITICAL)** — on a framebuffer *shrink*, `dev_fb_resize()` (`devices/dev_fb.c`) updated only the
dyntrans data pointer via `memory_device_update_data()` and left the device's registered `length` stale, so the #155
fast-map gate (`cpus/memory_rw.c`, `(paddr|mask) < length`) installed a writable host mapping past the new, smaller
allocation → guest→host OOB write (SGI O2/GBE `HCMAP` shrink, then touch a now-unbacked offset). Latent in pristine
upstream. Fixed with a new `memory_device_update_length()` (`core/memory.c`) that syncs `length`/`endaddr`/
`mmap_dev_maxaddr`, paired with the existing #157 cache-invalidate. **#183 (HIGH, X11 builds)** — `console/x11.c`
XImage alloc `x*y*depth/8` overflowed 32-bit `int` inside #156's 16384/axis cap → under-alloc + `XPutPixel` overrun;
widened to `size_t`. **#184/#186/#187 (MED)** — guest-reachable `exit(1)` DoS converted to log-and-continue
(#118/#119 ethos): `dev_fb_resize` too-small branch, `dev_mb89352` unimplemented transfer phase, and eight `dev_pvr`
MMIO register-write aborts. **Deferred & tracked in `OUTSTANDING_BUGS.md`** (not silently dropped): the ASC
`data_out_len==0` `exit(1)` (#185, structural), the PVR render/texture-loop `exit(1)`s (868/1084/1245/1419), and
Codex's remaining medium/low findings (CUE symlink-follow bypass of #158; cross-memblock invalidation gap in #165;
overlay write silent-success; Jazz `LB_IE` / dual-pending IRQ; ARC partition signed-`*512`; TCP-debug over-read;
NE2000 TX log-flood; one `dev_ram` MAP_FAILED). Builds **0/0** (gcc 15.2.1); applied byte-identically to `est/` and
`GXEMUL-SEC/`. Rig regression run pending.

## Eighteenth round (#188–#208) — accuracy/debuggability pass: Codex 5.6-Sol-Ultra + Fable panel
Codex `gpt-5.6-sol`/ultra (holistic, 17 findings) + a 4-reviewer **Fable panel** (seam / framebuffer-DMA /
storage-net-loaders / SEC-ARC-surface) + this session's per-site source verification, against a **narrowed
brief**: hardware-accuracy + debuggability + ethos, *not* new hardening for its own sake. **21 corrections
(#188–#208)**, each converting a guest-reachable `exit()`/`abort()`/host-crash on guest-controlled state into a
hardware-plausible fault or a bound, or fixing a guest→host OOB — full per-correction table in `CHANGELOG.md`
"Eighteenth round".

- **MIPS/CP0 + PROM (pmax+arc path):** #188/#189 R4000 invalid-PageMask host-`exit()` (write-canonicalize +
  translate-refill; two-sided find — Codex write-path + Fable translate-path), #190 `TLBWR` `WIRED>=nr_of_tlbs`
  SIGFPE, #191 DEC-PROM read/bootread `malloc` cap, #192 ARC-PROM Read/Write `malloc` cap + Write
  success-on-failure (triple-found: Codex F12 + Fable + this session).
- **Other-arch fidelity:** #193 ARM null-L2 `exit`→fault, #194 Alpha walk `abort`→no-translation, #195 m88k
  `INT_MIN/-1` SIGFPE, #196 GBE unimplemented-WID `exit`→black.
- **Guest→host DoS:** #197 ASC FIFO under/overflow, #198 PS2 DMAC QWC mask, #199 LANCE TX cap, #200 PVR TA cap,
  #201 OF `nargs` clamp.
- **Guest→host OOB (Codex HIGH):** #202 SII register-window, #203 MEC TX outer-loop overflow, #204 flat-CD
  negative-offset stack read, #205 MODE SELECT short-buffer, #206 zero-length-write NULL `exit`, #207 PX
  copyspans SRAM over-read (Fable), #208 `dev_ram` MAP_FAILED (clears the #175 straggler above).

**#209 (audit follow-up):** the MIPS Integer-Overflow *trap* is in fact already implemented
(`add`/`addi`/`sub`/`dadd`/`daddi`/`dsub` → `EXCEPTION_OV`); #209 removes the signed-overflow UB in the
overflow-*detection* math (unsigned wrap, bit-identical result, trap unchanged) at all six sites, clearing the
UBSan hit. **Build 0/0** both trees, **22 tags** present+matched; pmax boots to multiuser; corroborated by the
audit's ASan cross-check (emulator memory-clean during the #54/#82 fires).

## Nineteenth round (#210–#223) — MIPS exception fidelity + debuggability + host-halt sweep
Codex `gpt-5.6-sol`/ultra + a 2-agent Fable panel (remaining guest-reachable host-halts; MIPS exception
fidelity), per-site verified. **14 corrections (#210–#223)** — per-correction table in `CHANGELOG.md`
"Nineteenth round".
- **MIPS audit path (★):** #210 wire every exception to the trappable `SUBSYS_EXCEPTION` breakpoint (catches
  controlled-PC-into-unmapped that `-p` can't reach); #211 AdEL/AdES no longer clobber Context/EntryHi (BadVAddr
  only, like silicon); #212 unaligned LL/SC → AdEL/AdES; #213 CONFIG select 2..7 → defined-0 / ignore; #214
  R3000 ENTRYLO1 → ignore.
- **Other-arch host-crash → guest fault:** #215 Alpha load/store, #216 PPC lwarx/stwcx, #217 SH reserved-instr.
- **Device/PROM host-halts (round-18 pattern):** #218 OF getprop/read/write guest-buffer, #219 OF unknown
  service, #220 footbridge reset / PCI-bus-255, #221 mp STARTUPCPU, #222 kn02ba MER/MSR, #223 8253 (5 sites).

**Fidelity baseline (not a gap):** GXemul already raises AdEL/AdES (not TLBL) for unaligned *mapped* targets with
correct ExcCode/CE/BadVAddr/EPC/BD. Document-only: R3000 BEV=1 vector base (off the fault window); `mtc0`-writable
`BADVADDR` (Irix compat). **Build 0/0** both trees, all tags matched; **pmax boot regression PASS**.

## Twentieth round (#224–#226) — MIPS FPU memory-safety (Codex 5.6-Sol-Ultra)
Three **HIGH guest→host** MIPS-FPU memory-safety bugs from the Codex round-19 pass, per-site verified: **#224**
`ldc1`/`sdc1` `ft=31` indexed `reg[32]` (OOB into the adjacent `tlbs` pointer) → now RI; **#225** `ldc1` copied
an uninitialised `fpr` into the guest FPR on a *faulting* load (host-stack leak) → now seeded from the current
register; **#226** coproc paired-store sign-extension used raw `cp->reg[fd+1]` (OOB into `tlbs` for `fd=31`) →
now masked `(fd+1)&31`. **Build 0/0** both trees; **pmax + arc boot**. The remaining **22 Codex round-19 items**
(fault-signature fidelity trio + more host-halts) are logged in `OUTSTANDING_BUGS.md` for #227+.

## Twenty-first round (#227–#229) — fault-signature fidelity trio (multi-model panel)
Codex `gpt-5.6-sol` + agy Gemini + Fable panel (Ollama unavailable on host), **unanimous 3-0 FIX**, each verified
against source: **#227** the `SWL/SWR` store pre-read mislabeled *every* fault as TLBS → now maps only load codes
to store (`TLBL→TLBS`, `AdEL→AdES`); **#228** a misaligned `jr`/`jalr` target was silently rounded down → now
raises instruction-fetch AdEL (BadVAddr=EPC=rs, BD=0) in all 6 register-jump handlers; **#229** `mtc0 $8`
`BadVAddr` made **read-only** (a payload could otherwise erase the fault address an auditor reads). The panel
resolved the BadVAddr reviewer disagreement 3-0 to fix; Codex confirmed OpenBSD 2.2 pmax/arc only `mfc0`-read $8
(no boot regression). **Build 0/0** both trees; **pmax + arc boot**. ~19 Codex round-19 items remain in
`OUTSTANDING_BUGS.md` for #230+.

## Twenty-second round (#230–#233) — MIPS fault-signature fidelity (full 4-model panel)
Full 4-model panel — Codex `gpt-5.6-sol` + agy Gemini + **Ollama** (`gpt-oss:20b`; `qwen3-coder:480b-cloud` was
HTTP 410) + Fable — on 4 fidelity items: **#230** R3000 RFE preserve KUo/IEo (`~0x3f`→`~0x0f`); **#231** ERET on
R3000 → RI (decode-gate); **#232** J/JAL region from the delay-slot PC `(branch+4)[31:28]` not the branch
page-base (mask `~0x0fffffff`); **#233** `mtc0`/`dmtc0` add `cop0_availability_check` (writes only). The panel
**deferred** the privilege-transition fast-map bleed (invalidate-all would hang the R3000 boot; correct fix =
structural refactor) and the read-side/`$zero`/KUc remainder of #233 (load-bearing heuristic). **Build 0/0** both
trees; **pmax + arc boot**. ~15 Codex round-19 items remain for #234+.

## Twenty-third round (#234–#244) — guest-reachable host-halt tail → hardware-plausible faults (Fable + agy panel)
A Fable (source-verified) + agy panel triaged the remaining guest-reachable **host-halt** tail from the Codex
round-19 backlog (~13 places a guest can drive GXemul to `exit(1)`/`cpu->running=0` on guest-controlled state).
**10 DO-NOW**, all on the MIPS/pmax(R3000)/arc(R4000) audit path, were converted to the correct fault or graceful
error-return: **#234** failed ifetch `goto bad`→`return` (exception already installed + PC redirected, cf. #210);
**#235** `break 0x30378` reboot sentinel gated to the reset stub (phys `0x1fc00000`), else real **BP**; **#236**
reserved COP0 fn → **RI**; **#237** COP0 STANDBY/SUSPEND/HIBERNATE → idle on R4100 / RI elsewhere (was HIBERNATE
`goto bad` + SUSPEND reboot-at-any-PC); **#238** `memory_mips_v2p` supervisor/reserved KSU → TLB walk not `exit(1)`;
**#239** R3000 `tlbw*` under Status.IsC → `return` (entry already written); **#240** `dev_asc` unimplemented cmd →
deliver the illegal-command IRQ, no exit; **#241** `dec_prom` unsupported services → `V0=-1`+return; **#242**
`arcbios` non-SGI private call / `0x888` no-handler / unimplemented vector → `V0=ARCBIOS_EINVAL`+return; **#243**
`diskimage_scsicmd` `malloc(0)`→`malloc(1)`; **#244** `memory_rw` zero-fill the read buffer on a failed/
`NO_EXCEPTIONS` translation (whole class — DEC-PROM uninit-buf, cf. #95). **Deferred** (off audit path, both models):
PPC/ARM slow-path ifetch exit (#10; data side already #216), PPC `MSR.IP` reboot hack (#11), m88k CMMU/`mb89352`
(#12). Fable verified the SPECIAL3 **RDHWR** halt is **unreachable** on R3000/R4000 (ISA-gated to RI). **Build 0/0**
both trees; **pmax + arc boot** (pmax 15/15 → uid=0(root)/OpenBSD 2.2/clean halt; arc 13/13 → uid=0(root)/clean
halt). ~5 off-path/deferred Codex round-19 items remain for #245+.

## Twenty-fourth round (#245–#246) — debuggability logging + FPU denormal fidelity (5-model panel)
A **5-model panel** (Codex `gpt-5.6-sol` + Fable + agy Gemini + Ollama `gpt-oss:120b-cloud` + Kimi `kimi-k2.5`)
reviewed the round-23 Part-B suggestions. Of the four hardware-accuracy candidates, C1 (R3000 IsC cache) and C4
(R3000 delayed-IE) were found **already correct** in GXemul (C1: real `malloc`'d per-cache buffers +
`memory_cache_R3000` isolated routing; C4: the delay-slot `Cause.BD`/`EPC=branch` signature is textbook — only the
IE cycle-timing hazard is unmodeled, and nothing depends on it), and C2 (R4000 TLB-Shutdown) was **DO-NOT** (no
machine-check delivery exists; R4000 multiple-match is architecturally undefined = a reset-latched wedge, not an
exception; MIPS32 ExcCode 24 would be anachronistic + panic-prone; first-match is a valid concretization). Only two
changes were made:
- **#245 (C5, debuggability):** the guest-reachable fault-conversion diagnostics from rounds 18–23
  (`dev_asc`/`dec_prom`/`arcbios`, 8 sites) now route through the verbosity-gated `debugmsg`/`ENOUGH_VERBOSITY`
  channel at `VERBOSITY_DEBUG`, so a guest/fuzzer can't flood the host log; full state stays at `-v`/`break`. Reuses
  the #210 channel — no new machinery.
- **#246 (C3, fidelity):** `cpus/cpu_mips_coproc.c` — R3010/R4000 FPUs don't compute denormals in hardware; they
  set FCSR cause E (no enable bit → always traps) and let the kernel softfloat complete. GXemul computed *wrong*
  values (`float_emul.c` misreads denormal operands / flushes results to ±0). Now a denormal S/D operand, or a
  denormal result with FCSR.FS clear, raises `EXCEPTION_FPE` with no result written — **gated to EXC4K+ (arc)**;
  EXC3K (pmax) is bit-identical (MIPS-I has no ExcCode 15). pmax boot risk zero by construction; arc verified
  booting to multiuser with the trap active + no misfire. `#247` left unconsumed (C2 DO-NOT). **Build 0/0** both
  trees; **pmax + arc boot** (15/15, 13/13 → uid=0(root), clean halt).

## Twenty-fifth round (#248, #250) — debugger QoL for the audit (4-model panel)
Scoped `doc/TODO.html` for **debuggability** wins for the OpenBSD 2.2 audit. Recon: the fork already ships most of
the TODO debugger wishlist (`find`, `put s/z`, `step call`, `verbosity`, subsystem breakpoints, prefix-abbrev — the
#120–#128 round) and the `-f` fsync option (so the tentative **#249** fsync-toggle candidate was already done →
**#249 VOID**). A **4-model panel** (Codex `gpt-5.6-sol` + agy Gemini + Ollama `gpt-oss:120b-cloud` + Kimi
`kimi-k2.5`; Fable seat down on credits) ranked the two remaining items DO-NOW. Both opt-in and guest-invisible
(single `n != 0` early-out when unset).
- **#248 (breakpoint hit-counts + "run N then break"):** `struct breakpoints` + parallel `hitcount`/`ignore_left`;
  the dyntrans `TO_BE_TRANSLATED_HEAD` check counts every hit and, while `ignore_left > 0`, decrements and keeps
  running (reusing the `single_step_breakpoint` re-translation path; the instr-combination gate now also excludes
  `single_step_breakpoint`). `breakpoint add addr[, N]`; `show` + CTRL-T display counts. Verified: ignore-5 on a
  64-iter loop → first stop at hits=6, next at hits=7.
- **#250 (data write-watchpoints):** `watchpoint add addr[, len]` breaks on a guest store into the range, reporting
  writer pc/width/value/vaddr/paddr. (a) `update_translation_table()` keeps a watched page off the fast store map
  (`host_store=NULL`); add/delete uses `invalidate_translation_caches(INVALIDATE_ALL)` (clears the *data* fast-map).
  (b) Check placed **early in `memory_rw`, before the R3000 `memory_cache_R3000()` early-return**. Matched on
  **physical** address (translated from the typed vaddr at add-time) → defeats vaddr sign-extension + kseg0/kseg1
  aliasing. Verified on pmax: watching paddr 0x0 caught the kernel's `_bcopy` exception-vector install.

**Not consumed / deferred:** #249 VOID (fsync already the shipped `-f`); CTRL-T in the run loop (DEFER); PC/exec
statistics (DO-NOT). See `OUTSTANDING_BUGS.md`. **Build 0/0** both trees; **pmax + arc boot** → uid=0(root) with
nothing set (zero behavioural change), features then verified live.

## Twenty-sixth round (#251, #252) — console host-glue fidelity (3-view panel)
An OpenBSD 2.2 pmax/arc audit reported three "emulation-layer" bugs; a source-verified panel (Codex `gpt-5.6-sol`
high + Fable + reviewer holistic pass, each `diff`-checked against pristine `src/`) **converged** that the audit
mis-attributed the subsystem in all three. The two real, fixable defects are in the shared host-console glue
(`console/console.c`, byte-identical to stock 0.7.0 → upstream-latent), guest-invisible, host-I/O-only.
- **#251 (`console/console.c` `console_putchar`, serial output loss / "L12"):** the `'\n'` branch cleared
  `console_stdout_pending`, assuming libc flushes on newline — true only for a tty. With stdout a pipe/file
  (fully buffered), a newline-terminated burst never flushes *and* the cleared flag no-ops `console_flush()`, so
  the burst is lost if the process is killed/wedges. Fix: always mark pending (drop the newline special-case). The
  DZ/ns16550 UART TX itself is lossless (every byte reaches `console_putchar`) — not the loss source.
- **#252 (`console/console.c` `console_charavail`, console/pty "hang" / "L5"):** on stdin EOF, `select()` reports
  the fd readable forever and `read()` returns 0, so the drain `while()` spins **inside a device tick** →
  `machine_run()` never returns → the whole emulator freezes. Fix: `if (len < 1) break;` after the `read()` (not
  clearing `in_use_for_input`, which `console_putchar` re-arms).

| # | file | Problem | Fix |
|---|------|---------|-----|
| 251 | `console/console.c` | `console_putchar` clears the flush-pending flag on `'\n'` (assumes libc line-flush); false for pipe/file stdout → newline-terminated bursts sit in the fully-buffered stdio buffer and are lost on kill/wedge (audit "L12 serial drops output") | Always set `console_stdout_pending = 1`; `console_flush()` then drains within its existing cadence. Tty behaviour unchanged |
| 252 | `console/console.c` | `console_charavail` drain loop spins forever on stdin EOF (`select`→readable, `read`→0, FIFO never fills); inside a device tick it wedges the entire emulator (audit "L5 pty/forkpty hang") | `if (len < 1) break;` after `read()` — treat EOF/error as no input |

**Reproduced (pmax rig, before→after):** `gxemul -e 3max -d 1:disk bsd.pmax < /dev/null` froze at **0 bytes**;
the sole changed variable — an open stdin — booted to `root device?`. After #251/#252 the `< /dev/null` run boots
to `root device?` (979 bytes) like the control. **Triaged, NOT changed:** L13 inetd UDP (NAT has no unsolicited-
inbound path — config/tap or hole-punch, not a device bug); L12 UART model (lossless); est/ `dev_jazz.c`
`EXT_IMASK` gating (real but SEC already carries the corrected split; pmax has no jazzio). **Build 0/0** both
trees; **pmax 15/15 + arc 13/13 boot** → `uid=0(root)`.

## Twenty-seventh round (#253) — Linux tun/tap enablement (Codex + Fable)
GXemul's Ethernet tap backend (`net/net_tap.c`) opened the device BSD-style (`open(tapdev)`), so tap networking —
the only way to give the guest a real L2 link, and thus receive **unsolicited inbound** traffic the userspace NAT
cannot deliver (the L13 class) — did not work on Linux. A Codex `gpt-5.6-sol` + Fable panel designed the minimal
Linux path (converged on the body; split on the include header, resolved by test-compiling all three variants under
`-Wall -Wextra -Wshadow`).

| # | file | Problem | Fix |
|---|------|---------|-----|
| 253 | `net/net_tap.c` | `net_tap_init()` opened the tap BSD-style (`open(tapdev)` device node); Linux needs the clone device `/dev/net/tun` + `TUNSETIFF`, so tap networking was Linux-broken and the guest could not receive unsolicited inbound traffic (L13 class) | `#if defined(__linux__)`: open `/dev/net/tun` + `ioctl(TUNSETIFF, IFF_TAP\|IFF_NO_PI, ifr_name=tapdev)` (Linux tapdev = interface name); BSD device-path `open()` unchanged in `#else`; shared FIONBIO/tail; gated includes `<net/if.h>`+`<linux/if_tun.h>` |

**Verified live (pmax rig, R3000):** `-e 3max -L tap0` attaches (`tap0` → `UP,LOWER_UP`, 0 errors); guest `ifconfig
le0 10.0.0.10`; host→guest **unsolicited** `ping` → 4/4 replies (ttl=255), and a host UDP datagram to a closed guest
port → ICMP port-unreachable (reached the guest kernel with no prior NAT mapping). Both NAT boot regressions still
pass (pmax 15/15 + arc 13/13 → `uid=0(root)`); build **0/0** both trees. arc cannot demo — its SONIC (`dev_sn.c`) is
a register stub with no RX/TX; use the pmax LANCE (`dev_le.c`).

## Twenty-eighth round (#254, #255) — MIPS FPU result-correctness (4-model panel)
`fpu_op()` IEEE-754 result bugs on the MIPS FP path (item #1 of the 8-item TODO-triage batch), designed+reviewed by
a 4-model panel (Codex `gpt-5.6-sol`/xhigh + agy + Fable + Ollama). Result-correctness only; FCSR flags/trap deferred.

| # | file | Problem | Fix |
|---|------|---------|-----|
| 254 | `cpus/cpu_mips_coproc.c` | `fpu_op()`: DIV mis-routed valid small/NaN divisors to a `fatal()`+stale-fd branch; `sqrt(neg)`→`fatal()`+0.0; c.olt/c.ole true for ANY ordered pair (`\|\| !unordered`) + nine compare conds `fatal()`'d/`#if 0`'d | host IEEE div (Inf/NaN), host sqrt (NaN), unified all-16-cond compare formula `((cond&4)&&less)\|\|((cond&2)&&equal)\|\|((cond&1)&&unordered)`; drop dead `nan` local |
| 255 | `cpus/cpu_mips_coproc.c` | NaN arithmetic result stored as all-ones (a legacy-MIPS *signaling* NaN) not the hardware **quiet** NaN | canonicalize NaN result to `0x7fbfffff` (S) / `0x7ff7ffffffffffff` (D) in `fpu_store_float_value`; MOV/W/L unaffected |

Build **0/0** both trees; **pmax 15/15 + arc 13/13 boot** → `uid=0(root)`; 0 removed-`fatal()` hits in boot logs;
FP microtest 11/11 (host-side logic validation — rig image lacks an in-guest compiler). 4/4 diff-review faithful+safe.

## Twenty-ninth round (#256) — interactive debugger MIPS breakpoint sign-extension
Item #2 of the 8-item TODO-triage batch (Codex xhigh + Fable + Ollama, unanimous).

| # | file | Problem | Fix |
|---|------|---------|-----|
| 256 | `debugger/debugger_cmds.c` | interactive `breakpoint add <kseg0 addr>` never fired on arc/R4000 — the add path parses with `writeflag=0` so the MIPS sign-extension is skipped; stored `0x00000000_80…` != sign-extended pc `0xffffffff_80…` (R3000/pmax masked by its 32-bit compare) | after the parse, mirror `emul.c add_breakpoints` verbatim: `if (arch==ARCH_MIPS && (tmp>>32)==0 && (tmp>>31)&1) tmp \|= 0xffffffff00000000`; ARCH_MIPS-only guard |

Build 0/0 both trees; verified on arc (`breakpoint show` → `0xffffffff80100000`); pmax 15/15 + arc 13/13 boot unaffected.

## Thirtieth round (#257) — R4030 interval timer honors the guest-programmed rate
Item #5 of the 8-item TODO-triage batch (Codex xhigh + Fable + Ollama; base clock resolved empirically = OpenBSD writes IT_VALUE 9 → 100 Hz → 1 kHz base).

| # | file | Problem | Fix |
|---|------|---------|-----|
| 257 | `devices/dev_jazz.c` (both trees) | R4030 interval timer hardcoded to 100 Hz; guest `R4030_SYS_IT_VALUE` writes (the arc OS clock rate) were stored but ignored | on IT_VALUE write, `timer_update_frequency(d->timer, 1000.0/((double)idata+1.0))` (1 kHz base, empirically confirmed OpenBSD writes 9→100 Hz); unsigned idata (div-0-safe, bounds (0,1000] Hz); 100 Hz stays the power-on default |

Build 0/0 both trees; arc 13/13 + pmax 15/15 boot → `uid=0(root)`. OpenBSD's IT_VALUE=9 → exactly 100.0 Hz → no-op on the verified boot.

## Thirty-first round (#258) — decoded STATUS/CAUSE/FCSR in the MIPS register dump
Item #6 of the 8-item TODO-triage batch (Codex xhigh + Fable + Ollama; display-only).

| # | file | Problem | Fix |
|---|------|---------|-----|
| 258 | `cpus/cpu_mips.c` (both trees) | the debugger register dump printed COP0 STATUS/CAUSE + FPU FCSR as raw hex only, unhelpful for the fault-signature workflow | two static helpers decode named bit-fields under the raw hex (R3000 KU/IE stack vs R4000 KSU/ERL/EXL via exc_model; CAUSE mnemonic via exception_names[]; FCSR cause/enable/flag EVZOUI groups); display-only, R5900 FCSR skipped |

Build 0/0 both trees; pmax 15/15 + arc 13/13 boot → `uid=0(root)`; display-only, no behavior change.

---
## Thirty-second round (#259, #260, #261) — debugger/net QoL
Items #8a/#8b/#7 of the 8-item TODO-triage batch (Codex xhigh + Fable + Ollama; all low-risk).

| # | file | Change |
|---|------|--------|
| 259 | `core/emul.c`, `debugger/debugger_cmds.c` | `-K` (debugger-at-halt) implicit + sticky when any breakpoint is set (config/`-p`/interactive/subsystem) |
| 260 | `net/net.c` | route the 4 `net_init()` config-error diagnostics through `debugmsg(SUBSYS_NET, VERBOSITY_ERROR)`; leave the `net_add_nic` `exit(1)` |
| 261 | `core/debugmsg.c`, `include/misc.h` | opt-in default-OFF global break-on-ERROR-debugmsg (`debugmsg_break_on_error`, toggled by `breakpoint subsystem all error`); not the TODO's fragile always-break |

Build 0/0 both trees; pmax 15/15 + arc 13/13 boot → `uid=0(root)`; all three inert on a normal boot.

## Thirty-third round (#262) — LANCE RX-ring exhaustion (CSR0.MISS / descriptor BUFF)
Item #4 of the 8-item TODO-triage batch. 4-model DESIGN review (Codex xhigh + agy + Fable + Ollama) + a DIFF review of Codex's patch (agy + Fable + Ollama). `le_rx()` used to hold an incoming frame in `d->rx_packet` forever when the chip reached a receive descriptor it did not own (ring full); the guest never saw the loss. Real Am7990 drops the frame. Two naive designs were rejected: writing BUFF to the *previous* (already-released) descriptor is a DMA-contract violation, and a simple re-poll drain is a livelock (`net_ethernet_rx_avail()` imports fresh TAP/UDP/TCP traffic every call).

| # | file | Change |
|---|------|--------|
| 262 | `devices/dev_le.c` (both trees) | `le_rx()` void→int; drop the held frame on RX-ring exhaustion. First buffer → `CSR0.MISS`. Mid-frame chained → that descriptor's `ERR`+`BUFF` error bits plus `RINT` (no ENP), detected by looking ahead while it is still chip-owned. `le_register_fix()` drains only the already-resident queue on exhaustion (no ingress re-poll). Stale "not emulated yet" TODO updated. |

Build 0/0 both trees; pmax 15/15 + arc 13/13 boot → `uid=0(root)`; instrumented boot shows 0 exhaustion hits.

## Thirty-fourth round (#263) — ASC/R4030 DMA accounting (host-heap disclosure + count over-transfer)
Item #3 of the 8-item TODO-triage batch — a deep ASC (NCR 53C94) + R4030 DMA-seam audit. 4-model DESIGN review (Codex 5.6-sol xhigh + agy Gemini Pro + Fable + Ollama), unanimous **scope (a): safety guards only**; the residual/TC-suppression fidelity (**A4**) is deferred to **#264**. Both bugs were found by the Codex xhigh audit (Fable's parallel audit missed them), adjudicated real against source, and tempered from Codex's CRITICAL to **HIGH** (guest-memory / host→guest-disk, not a host overrun).

| # | file | Change |
|---|------|--------|
| 263 A2 | `devices/dev_jazz.c` (both trees) | `dev_jazz_dma_controller()` bounded its 1/15/255-byte copy quantum only by the ASC-requested `len`, never by the R4030 programmed byte count (`dma0_count`); a short R4030 count against a larger ASC length could over-read/over-write up to 254 bytes of **guest** memory. Now clamped to the remaining R4030 count, and the callback returns the **actual** bytes moved (`return (size_t) i`) instead of the requested `len`. `dma0_count = 0` left unchanged (panel-unanimous; residual is A4/#264). |
| 263 A1 | `devices/dev_asc.c` (both trees) | the DATA_OUT first-transfer path allocated its buffer with `scsi_transfer_allocbuf(..., clearflag=0)` — uninitialized host heap — and (via the deferred A4) advanced the offset / set Terminal Count even when the DMA callback moved nothing (wrong-direction), so host heap could be written into the guest disk image. Now zero-filled (`clearflag=1`), neutralizing the disclosure regardless of the residual A4 offset/TC fidelity. |

Both stay within the additive-guard envelope: on matched ASC/R4030 counts and correct direction (the arc/pmax SCSI-root boot path) the clamp never fires and the zero-fill is overwritten by real data, so behavior is byte-for-byte unchanged. Build 0/0 both trees; pmax 15/15 + arc 13/13 boot → `uid=0(root)`; instrumented boot shows 0 clamp/short-DMA hits (guards dead on the happy path).

## Thirty-fifth round (#264) — ASC zero-length DATA_OUT host-abort → guest disconnect
Item #3 follow-up — the residual ASC host-abort from the #263 ASC (NCR 53C94) + R4030 DMA-seam audit. 4-model DESIGN review (Codex 5.6-sol xhigh + agy Gemini Pro + Fable + Ollama), unanimous **scope (a)**: convert the abort to a guest fault; a faithful Transfer-Pad (pad/discard against the current nexus, **scope (b)**) is deferred as riskier.

The `exit(1)` in `dev_asc_transfer()`'s DATA_OUT branch (`data_out_len == 0`) was a host abort **reachable from guest register programming**: the Transfer-Pad command (`NCRCMD_TRPAD`) allocates a fresh empty transfer via `dev_asc_newxfer()` and then runs a DATA_OUT transfer straight into the `exit`. It now logs a `fatal()` and **returns 0**, so the existing `NCRCMD_TRANS`/`NCRCMD_TRPAD` handler reports a guest-visible **disconnect** (`NCRINTR_DIS|NCRSTAT_INT`) — matching the #167/#240 host-abort→guest-fault pattern and the absent-target selection path. **DISCONNECT** was chosen over **ILLEGAL** (`NCRINTR_ILL`): a legal Transfer-Pad opcode in a legal DATA_OUT phase is not an illegal command, and the gross-error path has no cleanup plumbing. The `return 0` leaks nothing — `data_out` is allocated later and is still NULL here — and must not free locally (the caller frees `xferp`).

Verified: build **0/0** both trees; **pmax 15/15 + arc 13/13 boot → `uid=0(root)`**; the new `fatal()` never fires on a healthy boot (0 hits in both pty logs — the branch is dead on the SCSI-root boot path).

## Thirty-sixth round (#265, #266) — ASC FIFO occupancy + chip-reset IRQ hygiene
The ASC (NCR 53C94) FIFO/reset register-hygiene round from the same TODO-triage sweep. 4-model DESIGN review (Codex 5.6-sol xhigh + agy Gemini Pro + Fable + Ollama); **Fable caught the fourth occupancy site (the MSG_OUT drain) the other three seats undercounted, plus the read-side atomicity hazard** — a drain loop fixed without the `dev_asc_fifo_read` guard would let a full FIFO infinite-loop the host, so all three read-side sites are changed atomically in one commit.
- **#265** `devices/dev_asc.c` (both trees): the 16-byte FIFO tested occupancy with the pointer equality `fifo_in == fifo_out` at **four** sites, but that is **also true when the FIFO is exactly full (16)** — so a full FIFO was read as *empty*. Consequences: `dev_asc_fifo_read` stuck returning the same byte (never decrementing `n_bytes_in_fifo`); the CDB and MSG_OUT non-DMA drain loops copied **zero** of the bytes they had just allocated (`scsi_transfer_allocbuf(..., clearflag=0)`) → an uninitialized buffer tail handed to the SCSI command layer; and the write post-check false-warned on the legal 16th byte. All four sites now use the cached `n_bytes_in_fifo` count, and the overflow warning moves to the real drop site (the #197 write guard). Reachable by any guest that writes `NCR_FIFO` 16×; the arc/pmax boots top out at 15 bytes, so for n<16 the tests are equivalent and the happy path is provably unchanged.
- **#266** `devices/dev_asc.c` (both trees): a chip reset (`RSTCHIP`, the sole caller of `dev_asc_reset`) cleared `NCRSTAT_INT` in `reg_ro` but never released the physical IRQ line — `DEVICE_TICK(asc)` only asserts on a rising edge and the only deassert was the `NCR_INTR` register read — so a reset taken with a pending interrupt left the line **latched high with a zeroed status** until the guest happened to read INTR. `dev_asc_reset` now deasserts (`INTERRUPT_DEASSERT(d->irq); d->irq_asserted = 0;`); it runs only at RSTCHIP, after `INTERRUPT_CONNECT`.
Deferred to a future round (boot-interaction risk, no demonstrated victim): FIFO Gross-Error status, `cur_phase` reset, and TC-preservation on the INTR read.
Verified: build **0/0** both trees; **pmax 15/15 + arc 13/13 boot → `uid=0(root)`**; instrumented boot shows **0** full-FIFO reads/drains, **0** write-drops, and **0** pending-IRQ resets (all four changed branches dead on the SCSI-root boot path).

## Thirty-seventh round (#267) — R4030 DMA translation-table limit
Last untreated R4030 DMA-engine gap from the #263 ASC + R4030 DMA-seam audit. 4-model DESIGN review (Codex 5.6-sol xhigh + agy Gemini Pro + Fable + Ollama), unanimous **scope (a)**: bound the walk and stop the transfer; the hardware translation-limit fault/interrupt (**scope (b)**) is deferred as riskier and unmodeled. The byte-size limit semantic was pinned to the NetBSD/arc and Linux jazzdma drivers and then confirmed by an instrumented arc boot.
- **#267** `devices/dev_jazz.c` (both trees): `dev_jazz_dma_controller()` translated each DMA address to physical by reading the page-table entry at `dma_translation_table_base + (dma_addr>>12)*8`, but never bounded that index against the programmed **TL_LIMIT** — so a DMA address past the end of the table read an **arbitrary guest word as a PTE** and moved data to/from whatever physical page that word encoded (guest-memory corruption on a misprogrammed or hostile transfer; it stays within guest RAM, so not a host overrun). The walk is now bounded: when the table byte-offset `(dma_addr>>12)*8` reaches a **non-zero** `TL_LIMIT` the transfer stops and returns the bytes completed so far. The real R4030 raises a translation-limit fault (`DMA_ENAB_TL_IE` / `DMA_INT_SRC`); that error/interrupt path is not modeled and is left a documented gap. The limit is a table **byte-size** (NetBSD/arc `JAZZ_DMATLB_SIZE`, Linux jazzdma `VDMA_PGTBL_SIZE`); a limit of **0** (never programmed) is fail-open, so a guest that does not use the table cannot regress.
Deferred to a follow-up: the TL-fault interrupt model (`DMA_INT_SRC` + invalid-address register + `TL_IE` wire) and DMA0 count-register masking (`R4030_DMA_COUNT_MASK`, a separate #268).
Verified **empirically**: a non-enforcing probe observed OpenBSD 2.2/arc program **TL_LIMIT=0x8000** (4096 × 8) exactly once at boot; the SCSI-root boot's **maximum table offset was 0x458** (0x460 incl. the entry, ~28 KB below the limit); and across **2602 DMA transfers 0** would exceed the limit — so the bound never fires on the verified boot (its condition is identical to the proven-0 would-break condition). Build **0/0** both trees; **arc 13/13 + pmax 15/15 boot → `uid=0(root)`**.

## Thirty-eighth round (#268) — R4030 DMA count-register width
The follow-up flagged in #267, and the last item from the #263 ASC + R4030 DMA-seam audit. 4-model DESIGN + DIFF review (Codex 5.6-sol xhigh + agy Gemini Pro + Fable + Ollama), unanimous: mask the channel-0 count write to the documented hardware width, with the empirical over-mask probe folded into the same round.
- **#268** `devices/dev_jazz.c` (both trees): the R4030 DMA channel-0 byte-count register is **20 bits wide** (`R4030_DMA_COUNT_MASK = 0x000fffff`, previously defined but unused), but the register write stored the **raw 32-bit value**, so a guest could express a DMA transfer **longer than any real R4030** — the extra high bits are physically absent on the chip. The channel-0 count write is now masked to 20 bits; the read-back returns the masked value, and the copy-loop count/clamp (**#263**) and the translation-table bound (**#267**) now see a value that is correctly bounded to the hardware width. **Channel-0 only** (`dma1` stores only its mode register; `dma2`/`dma3` are unmodeled). The mask also clears bits 32–63 before the assign to the `uint32_t` field, so it slightly hardens the `dma_addr + dma0_count` sum in the copy-loop guard and puts the previously-unused header constant to its intended use.
Verified **empirically**: an instrumented arc boot recorded **0** count writes with bits above the mask (guest SCSI transfers are bounded by **MAXPHYS**, far below 1 MB), so the mask is a **no-op on the verified boot**. Build **0/0** both trees; **arc 13/13 + pmax 15/15 boot → `uid=0(root)`**.

## ASC / R4030 DMA audit — known gaps & deferred items

This records the outcome of the full NCR 53C94 "ASC" SCSI + Jazz R4030 DMA audit (a two-model deep audit —
Codex 5.6-sol xhigh and Fable — cross-referenced and adjudicated against the source). The reachable
correctness/safety findings were fixed in rounds 34–38 (#263 DMA count-clamp + heap-disclosure, #264
zero-length DATA_OUT host-abort → guest disconnect, #265 FIFO full-as-empty, #266 chip-reset IRQ hygiene,
#267 R4030 translation-table limit, #268 R4030 DMA count-register width mask). The items below were
deliberately NOT changed — either because they are unreachable by the target guests (Ultrix / NetBSD /
OpenBSD 2.2 on pmax + arc), because a faithful fix needs infrastructure disproportionate to the low reach, or
because the "fix" would add more risk to the boot-critical SCSI path than the non-bug it addresses. Each is
recorded here so the audit is complete and a future round can pick any of them up with full context.

### Assessed and intentionally left as-is (fixing would be a regression risk for ~zero guest benefit)

- **PMAZ DMA address register — reads allowed, direction/alignment not enforced** (`dev_asc.c`
  `DEVICE_ACCESS(asc_address_reg)`). On real DEC PMAZ-AA hardware this 4-byte register is write-only (reads
  bus-timeout), bit 31 selects DMA direction, and bit 0 is ignored (halfword alignment). GXemul allows reads,
  does not enforce the direction bit, and keeps bit 0. **Why left as-is:** every use of the register masks the
  value with `& (ASC_DMA_SIZE-1)` = `& 0x1FFFF`, so the address is always safely bounded to the 128 KB SRAM
  buffer and bit 31 is already discarded — there is no memory-safety or data-correctness bug that reaches any
  guest. Ultrix/BSD program a correct direction and an aligned address, so the alignment/direction/write-only
  fidelity gaps are never exercised. Making reads fail or rejecting a "wrong-direction" transfer would add a
  guest-visible behavior change to a boot-critical pmax path with no demonstrated beneficiary. Cosmetic
  fidelity only.

### Unreachable by the target guests (documented; fix only if a guest is found that needs it)

- **DMA-mode target SELECT sources the CDB from the built-in SRAM even on arc** (`dev_asc.c`, the SELECT-with-
  DMA path). On arc the command bytes would arrive through the Jazz DMA controller, but the code reads the DEC
  SRAM buffer (all-zero on arc). Unreachable: the ncr53c9x/esp drivers load the CDB into the FIFO and issue
  SELECT without the DMA bit (`dmaflag == 0`), which is handled correctly. A `NCR_F_DMASELECT` front-end would
  expose it.
- **Message-phase rejection / negotiation / recovery** (`dev_asc.c` MSGACK + MSG-IN/OUT handling). Message
  Accepted always disconnects (raises DIS) even when ATN is set, and DMA MESSAGE OUT is a stub. Real hardware
  would transition to MESSAGE OUT for MESSAGE REJECT / abort / parity recovery / sync negotiation. Unreachable:
  the target disks never disconnect and the guests use no synchronous negotiation on this controller; the
  normal command-complete path has ATN clear and works.
- **No two-deep command / interrupt sequencer; ENSEL is a no-op** (`dev_asc.c` command-register dispatch). The
  53C94 has a two-entry command FIFO and two-level interrupt stacking; GXemul executes each command
  immediately and ORs causes into one interrupt register. Unreachable: with the synchronous diskimage backend
  there is no real mid-command disconnect/reselection, so the stacking and ENSEL/DISSEL semantics are dormant.
- **Non-DMA (PIO) DATA-IN / DATA-OUT are stubs** (`dev_asc.c`). PIO data-in returns zeroes (the source buffer
  is never populated) and PIO data-out transfers nothing. Unreachable: Ultrix/NetBSD/OpenBSD use DMA for all
  SCSI data on both machines; only an exotic PIO fallback would hit these.
- **Power-on/reset identity mixes 53C94 and F9x semantics** (`dev_asc.c` init + reset). CFG3 is initialized
  with the F9x `CDB` bit before any reset, `dev_asc_reset()` is not called at init, and the readable Config-1
  bus-ID is forced to 7. Probe/diagnostic-visible only; boot drivers issue Reset Chip then program the ID.

### Deferred — a faithful fix needs infrastructure beyond the audited scope

- **R4030 translation-limit / memory-error FAULT reporting** (the scope-(b) companion to #267). The real R4030
  raises a translation-limit interrupt (`R4030_DMA_ENAB_TL_IE`) with a fault/invalid-address status readable via
  `R4030_SYS_DMA_INT_SRC`. GXemul models none of that: there is no DMA interrupt-source register handler, no
  invalid-address register (pica.h does not even define one), and no DMA fault interrupt wire. #267 stops the
  out-of-range transfer safely (no bad PTE fetch) but does not raise the guest-visible fault. Modeling it means
  adding a status register, an invalid-address register, and a new interrupt line — low reach (only a
  misprogramming/faulting guest), and a spurious interrupt on an unmodeled line could itself break a verified
  boot.
- **ASC/R4030 DMA residual + Terminal Count fidelity** (the A2/A4 family, scope-(b) companion to #263). On a
  short or partial DMA the ASC still reports Terminal Count with a zero residual, and the R4030 count/address
  registers are not left in a hardware-faithful residual state (the address is not advanced, so a naive
  residual would be wrong). A correct model needs a live R4030 register file (advancing address + decrementing
  count during the transfer) with the honored callback return threaded through all three ASC call sites — a
  coherent standalone correction, deferred because it touches the boot-critical completion path and no target
  guest exercises a short DMA on the happy boot.
- **Transfer-Pad against the current nexus** (the scope-(b) companion to #264). Real 53C94 Transfer Pad
  pads/discards excess bytes on the CURRENT SCSI nexus; GXemul allocates a fresh empty transfer
  (`dev_asc_newxfer`), which is why #264 had to convert the resulting zero-length DATA_OUT into a guest
  disconnect. A faithful Transfer Pad (preserve the nexus, pad DATA_OUT with zeros / discard DATA_IN, keep
  TC/BS/phase correct) plus cleaning up the non-DMA-TRPAD fall-through is a separate correction with its own
  state-machine risk; the guests only reach TRPAD on error/padding recovery.
- **FIFO Gross-Error status; chip-reset cur_phase reset; TC preserved across an INTR read** (deferred from
  #265/#266). Setting the Gross-Error bit on a FIFO overflow, resetting `cur_phase` on a chip reset, and NOT
  clearing Terminal Count when the interrupt register is read are all datasheet-correct, but each interacts
  with the empirically-tuned interrupt/phase handling (the INTR-read block is hand-tuned "For Mach/PMAX", next
  to the function-complete suppression that must not change), and none has a demonstrated victim on the target
  guests. Deferred, to be done one at a time with instrumentation if a guest is found that needs them.

### Deliberately stubbed and correct for this scope — do NOT "fix"

- **Function-complete (FC) interrupt suppressed after a data transfer** (`dev_asc.c`). Empirically tuned:
  asserting `NCRINTR_FC` here made Linux/DECstation and OpenBSD/pmax choke. Only `NCRINTR_BS` is raised by
  design. Leave it.
- **Target-mode commands** (SNDMSG/SNDSTAT/RECCMD/…) are unimplemented — the diskimage topology has no
  external initiator, so initiator-only operation is correct.
- **R4030 DMA channels 1–3** are not modeled — only channel 0 (SCSI) is wired; the others are unused by the
  target machines.
- **`R4030_SYS_TL_IVALID` (translation-cache invalidate) is a no-op** — GXemul re-reads the guest PTE on every
  copy quantum, so it is over-coherent; there is no cached translation to invalidate until a translation cache
  is introduced.
- **Reserved read registers** (CCF/test read-back) are not faithfully modeled — the NCR datasheet defines those
  addresses as reserved, so there is no stable real value to score against.

## Fortieth round (#269, #270) — self-review corrections: ASC FIFO diagnostic flood + breakpoint-listing honesty
A five-model code review of our own #254–#268 batch (Codex 5.6-sol ultra + agy Gemini 3.6 + Kimi 3 MAX + Fable 5 + Opus 5; two passes, unanimous on scope) found two defects **we** introduced. Both are host-side diagnostics — no guest-visible behaviour changes in either correction.
- **#269** `devices/dev_asc.c` (both trees): **#265** relocated the ASC FIFO overflow warning into the drop guard, which turned an at-most-once-per-fill message into **one host line per dropped byte** — measured, 24 overflow writes produced 24 host lines. The pre-existing read-side twin (the **#197** empty-FIFO guard, whose message says "overrun" for historical reasons although the condition is a read of an *empty* FIFO) behaves identically: 24 reads of an empty FIFO produced 24 lines. This matters beyond noise, because `fatal()` is **not verbosity-gated** and `va_debug()` writes stdout **one character at a time** — the same stream the boot harness pattern-matches — so an undrained pipe can block the single-threaded emulator. Both sites now warn **once per device**, via one-shot latches in `struct asc_data`, and deliberately keep `fatal()`: a verbosity-gated `debugmsg()` was rejected because under `-q` the harness verbosity settles at `VERBOSITY_ERROR` (`main.c` lowers it by one; `debugmsg_add_verbosity_level()` floors at 0), so a WARNING-level message would be **invisible to the boot-log hygiene grep**, while an ERROR-level one would change the printed form *and* would trip **#261**'s global break-on-ERROR whenever that is armed. The latches are deliberately **not** cleared by `dev_asc_reset()` or `dev_asc_fifo_flush()` — otherwise a guest could re-arm the flood with `RSTCHIP` — and are zeroed by the `memset` in `dev_asc_init()`. Everything the guest can observe (the dropped byte, the value returned by a read of an empty FIFO, the FIFO indices and count, the registers, the interrupts) is unchanged.
- **#270** `core/debugmsg.c` (both trees): **#261**'s global break-on-ERROR toggle was **invisible** in the `breakpoint subsystem` listing. `breakpoint subsystem all error` arms that global *and* sets every per-subsystem level; a later `breakpoint subsystem <name> off` clears only that subsystem's level, so an ERROR-level message from it still enters the debugger — yet `debugmsg_print_breakpoints()`, which skips subsystems at level < 0, listed it as unarmed and never mentioned the global (measured: 24 rows after arming, 22 after `cpu off`, `cpu` absent, the global never named). The listing now discloses the global, and no longer prints "No breakpoints on subsystem messages set." while it is armed. The **override semantics are deliberately unchanged** (panel-unanimous): they are not observable on pmax/arc — neither has a runtime-reachable ERROR-level `debugmsg()` — and every redesign considered was worse than simply stating the behaviour. Display only.
Verified: build **0/0** both trees; **pmax 15/15 + arc 13/13 → `uid=0(root)`**; log-hygiene greps all **0** (the "FIFO overrun" token is preserved, so that gate still works). Both flood probes drop from **24 host lines to 1** — write side and read side — while the deliberately-untouched `TRPAD` control still emits 10 lines for 10 commands. A single-session probe shows the two latches are **independent** (a 24-write overflow burst → 1 line; then, after draining the FIFO, a 24-read empty burst → 1 further line, which a shared latch would have suppressed) and that the latch **survives a guest `RSTCHIP`** (5 further empty reads → 0 lines, with `NCR_FFLAG` reading 0 afterwards, so those reads necessarily took the guard). For **#270**, the review probe's own assertion flips **false → true** with no edit to the probe, and `breakpoint subsystem all off` makes the new line disappear and the "No breakpoints …" message return.

**Known gaps (documented, deliberately not fixed in this round).** `dev_asc.c` still contains **20 further unconditional `fatal()`/`printf()` diagnostics** of the same family (22 live call sites, minus the two now latched). Two are worth naming. The stray-register-access report (`dev_asc.c` `:936`/`:939` before this round, `:969`/`:972` after) prints one host line **per access** at asc offsets ≥ 0x10 (arc/PICA) or ≥ 0x40 (pmax/DEC); because it carries a **variable payload** — the offset and the value — a one-shot latch would hide real information, so it wants **#245**-style verbosity gating instead. The **#264** zero-length-`DATA_OUT` site is excluded on **scope-coherence** grounds and *not* because it is untestable: it reproduces cleanly (10 `TRPAD` commands → 10 host lines), but its `fatal()` was panel-locked for symmetry with the **#167** guard, so revisiting it belongs with that guard rather than here. These belong to a dedicated `fatal()`-hygiene round.

## Forty-first round (#271, #272) — VGA CRTC: a guest-reachable host abort, and a driver-reachable diagnostic flood
Both corrections are in `devices/dev_vga.c`, which is **not** one of the five divergent files, so the two trees stay byte-identical. They were found by the same sweep and share one probe rig, but they are **not the same shape** — #271 is a control-flow change plus a latch, #272 is output-only — so this round carries **two independent probes** and neither is allowed to stand in for the other.
- **#271** `devices/dev_vga.c` (both trees): **two guest byte stores killed the emulator process.** Selecting CRTC index `0xff` and then writing a mode byte outside the eleven implemented modes reached `default: fatal("TODO! video mode change hack …"); exit(1);` inside `vga_crtc_reg_write()` — measured on the committed build: wait status `exited, code 1`, pty EOF, the `fatal()` text as the last output, while an *accepted* mode byte (`0x03`) survived. A guest must not be able to `exit()` the host — the **#167** / **#240** / **#264** rule — so the abort is gone. The arm now **returns** rather than breaking: a *rejected* mode must have **no side effects**, and falling through would have run the geometry/resize block and then `reset_palette(d, grayscale)` with `grayscale == 0`, i.e. a rejected write would clear the screen and reset the palette to colour. (The fall-through is *not* a **#182**-shape stale-length overrun — the geometry left in `d` is self-consistent — so this is side-effect suppression, not a memory-safety fix.) `d->crtc_reg[0xff]` is deliberately **left holding the rejected byte**: every other unhandled CRTC index is RAM-backed too, so making `0xff` read back differently would be the inconsistency, and the previously accepted mode is not reconstructible anyway (`0x00`/`0x01`, `0x02`/`0x03` and `0x09`/`0x0d` produce identical geometry, and a restore would need new state *and* a change in the caller). Because removing the abort turns a one-shot exit into a repeatable ungated `fatal()` — the **#265** → **#269** shape — the warning is latched to **once per device instance** through a new `invalid_mode_warned` field in `struct vga_data`, deliberately **not** cleared by `register_reset()` (an accepted mode set is the only guest-reachable reset here, so clearing it there would let a guest re-arm the flood) and zeroed by the `memset` in `dev_vga_init()`. `fatal()` is kept rather than gated: exactly one visible line is what a deficiency tripwire should leave under `-q`, the mode the boot harness runs.
- **#272** `devices/dev_vga.c` (both trees): the **outer** `default:` arm of the same function reported every unhandled CRTC index with an ungated `fatal()` — measured **1.00 host lines per guest data store**; arming the index is silent and one index store then licenses unlimited one-store repeats. Only indices `0x0a`–`0x0f` are handled (measured by sweep), so **every horizontal/vertical timing register an ordinary VGA driver writes during a mode set lands here** — this is reachable by legitimate driver software, not only by a hostile guest. The emulator survives it; this is a flood, not an abort. It is now `debugmsg(SUBSYS_DEVICE, "vga", VERBOSITY_DEBUG, …)` carrying the same payload. A latch was wrong here: the payload is *variable* (index and value), so latching would hide real information, and this is ordinary-if-unimplemented traffic rather than a deficiency tripwire, so it should simply be silent in a normal run. Output only; nothing the guest can observe changes.
Verified: build **0/0** both trees (223 pmax / 224 arc objects); **pmax 15/15 + arc 13/13 → `uid=0(root)`**; log-hygiene greps on both boot pty logs **0** for `vga_crtc_reg_write`, for `video mode change hack`, and for `panic`. **#271 probe, 11/11:** the two-store sequence that exited with code 1 on the committed build now leaves the process alive and answering (`dead=False`, `pc` readable); a witness byte planted in the handled register `0x0e` **survives** a rejected mode (`0x5a` → `0x5a`), proving the `return` suppressed the side effects, while an accepted `0x03` zeroes it (`0x5a` → `0x00`), proving the accepted path still performs the mode change; `crtc_reg[0xff]` reads back `0x55`, the rejected byte; **12 rejected sequences in one session produce exactly 1 host line**, and 3 more after an accepted mode set — the device reset — produce **0**, so the latch cannot be re-armed. **#272 probe, 8/8, both halves:** under `-V step` the call site still fires 8/8 = **1.00 per store** (`debugmsg.c:181` skips the verbosity test while `single_step` is set, so this proves the site is live, not that it is ungated); suppression is therefore measured **free-running**, with the CPU parked in a loop that stores to the data port and counts its own iterations — **93,454,400 stores in 2.51 s produced 0 lines** (10 bytes of host output total). Two controls keep that from being a blind rig: the same free run with `-v -v` (verbosity DEBUG) prints **313,468 lines for 314,080 stores**, and the pre-fix binary at default verbosity prints **418,881 lines for 420,160 stores** — i.e. the old `fatal()` did flood a normal, non-stepping run, and the new silence is the verbosity gate.

**Scope (honest).** This round swept the **pmax/arc device set** for guest-reachable `exit()`, not the whole tree. `devices/dev_wdc.c` still has four guest-reachable `exit(1)` calls — one fires on **any failed ATAPI command** (`WDC: ATAPI scsi error?`) — but neither `machine_pmax.c` nor `machine_arc.c` instantiates it (the ARC `wdc` line is inside `#if 0`), so it is out of scope here and left for a tree-wide `fatal()`/`exit()` hygiene round. Note also that **our tree is more exposed than upstream on exactly this device**: SEC's `machine_arc.c` forces `fb_console = 1` for PICA and therefore calls `dev_vga_init()` even headless, while `est`'s gates the same call on `machine->x11_md.in_use` — so on SEC a plain `-e pica` run instantiates the VGA device, and the abort was reachable without X11.

**Do not re-litigate (panel-verified in this round).** (1) *The fall-through was memory-safe.* Had the rejected-mode arm fallen through instead of returning, the geometry block would have used the **previous** mode's `max_x`/`max_y`/`font_*`/`pixel_rep*` — which are mutually consistent, because the arm assigns none of them — so `dev_fb_resize()`, `fb_size` and the `gfx_mem` allocation would all have agreed. This is **not** the **#182** stale-length shape, and #271 is not a memory-safety fix; the reason to `return` is side-effect suppression (a seat measured the fall-through running `reset_palette(d, grayscale)` with `grayscale == 0`, i.e. clearing the screen and resetting the palette to colour on a mode write the device had just refused). (2) *`crtc_reg[0xff]` deliberately keeps the rejected byte* (panel 3–2): the register file is RAM-backed for every other unhandled index, so a special-cased `0xff` would be the inconsistency, and the previously accepted mode cannot be reconstructed anyway — `0x00`/`0x01`, `0x02`/`0x03` and `0x09`/`0x0d` yield identical geometry, so a restore would require new state *and* a change in the caller. (3) *Latch, not verbosity gate* (panel 3–1): a latch leaves exactly one line under `-q`, which is what a deficiency tripwire should do and what the boot-log hygiene grep can see; #272's site got the opposite treatment because its payload is variable. (4) *Scope and exposure* are stated in the paragraph above — the sweep covered the pmax/arc device set only, `dev_wdc.c` remains as noted, and SEC instantiates `dev_vga` on PICA where est does not.

## Forty-second round (#273) — FP→integer conversion: undefined behaviour, and a host-dependent guest result
- **#273** `core/float_emul.c` (both trees): the W/L arm of `ieee_store_float_value()` used a bare `r3 = (int64_t) nf;`. That cast is **undefined behaviour** in C for NaN, ±Inf and any value outside the destination range, so the guest-visible answer was decided by the *host's* FP instruction: x86-64 `cvttsd2si` yields the integer indefinite `0x8000000000000000`, which the W path's trailing `r = (uint32_t) r` truncates to **`0x00000000`**, whereas aarch64 `fcvtzs` **saturates**. **The same guest binary therefore produced different results depending on the machine GXemul was built on** — removing that host-dependence is an independent reason for this change, over and above the constant being wrong. Operands are now classified first and the cast executes only for in-range values.

**The pinned constant, with its primary citations.** With the Invalid trap disabled, the R3010/R4010 return the **largest positive integer** for **all five** invalid cases — NaN, +Inf, −Inf, +overflow, −overflow — and there is **no sign dependence**: W → `0x7fffffff`, L → `0x7fffffffffffffff`.
- MIPS **R4000 User's Manual** (Heinrich), `CVT.W.fmt`: "If Invalid operation is not enabled, then no exception is taken and 2^31−1 is returned."
- **MIPS IV Instruction Set** Rev 3.2 (Price, 1995) p. **B-50**, under the heading labelled **MIPS I**: "the default result, 2^31−1, is written to `fd`."
- MIPS32 Vol II (NAN2008-aware revision) carries **both** rules, selected by **`FCSR.NAN2008`** — a bit the R3010/R4010 **do not have**.
- Corroboration: Linux `arch/mips/math-emu/ieee754.h` — `ieee754si_indef()` returns `INT_MAX` when `!nan2008`, and `ieee754si_overflow()` **ignores its sign argument** when `!nan2008`; pre-2014 QEMU — `#define FP_TO_INT32_OVERFLOW 0x7fffffff`.
- **The `0x80000000`-for-negative-overflow rule assumed by an earlier note in this project is wrong for these CPUs.** It is the NAN2008/r6 rule, and that same rule also returns **0**, not `0x7fffffff`, for NaN. Adopting half of it would have been incoherent.

**The `<=` / `<` asymmetry is deliberate — do not "simplify" it.**
```
W:  isnan(nf) || nf >= 2147483648.0          || nf <= -2147483649.0
L:  isnan(nf) || nf >= 9223372036854775808.0 || nf <  -9223372036854775808.0
```
- W's lower bound is **`<= -2147483649.0`, not `< -2147483648.0`**. `trunc(-2147483648.5)` is exactly `INT32_MIN`, which **is** representable, so that operand is **not** an overflow and must convert normally to `0x80000000`. The `<` form is the classic off-by-one here and yields an observably wrong guest value; **two of the five panel seats wrote it that way in the first pass** before the arithmetic settled it. The probe covers `-2147483648.5` explicitly for exactly this reason.
- L's lower bound **is** a strict `<`, because −2^63 is exactly representable and `trunc(-2^63)` is a valid `INT64_MIN`. The first genuine overflow below it is −2^63−2048 (the next double down), which the probe also covers.
- W's **upper** bound carries deliberate slack: values in the open interval (2147483647.0, 2^31) are treated as overflow although truncation would have produced `0x7fffffff` anyway. Harmless as long as the Invalid **flag** is not signalled; it would need revisiting if FCSR Invalid signalling is ever added.
- **2^63 is written as the literal `9223372036854775808.0`.** `(double)INT64_MAX` **rounds up** to exactly 2^63, which would let the equality case fall straight through to the undefined cast. (2^63 *is* exactly representable as a double — an earlier note in this project claiming otherwise was backwards.)

**Blast radius: zero outside MIPS (grep-verified).** `float_emul.c` is shared by the alpha, m88k, mips, ppc and sh cores plus `dev_pvr`, but `IEEE_FMT_W` and `IEEE_FMT_L` appear **only** in `core/float_emul.c`, `include/float_emul.h:45-46` and `cpus/cpu_mips_coproc.c:1033`. The W/L arm has no non-MIPS caller. The **S and D arms — which do reach the other five families — are untouched.** **#255**'s NaN canonicalizer (`cpu_mips_coproc.c`) still guards on `IEEE_FMT_S`/`IEEE_FMT_D` only, so W/L results continue to pass through it unmodified; re-confirmed after this change, in the source and in the measurements (a NaN operand yields `0x7fffffff` / `0x7fffffffffffffff`, not a canonicalized S/D pattern).

**Out of scope, deliberately (each a separate item).**
- **Rounding mode.** `cvt.w` truncates here (`3.5` → `3`), where MIPS default RN would give `4`. A future rounding fix must honour `FCSR.RM` for `cvt.w` **but must not "fix" `trunc.w`**, which is architecturally round-toward-zero regardless of `FCSR.RM`. The controls in this round's probe deliberately include both a rounding-sensitive (`3.5`) and a rounding-insensitive (`3.25`) case so the two defects can never be confused.
- **FCSR Invalid flag signalling** — still not raised on these conversions (documented deferred TODO). Only the *result* is corrected here.
- The `float_emul.c` **reserved-format `fatal()` cluster** (`:64`, `:82`, `:154`, `:216`, `:306`) — panel-unanimous that it is a separate commit; not folded in.

**Testing note — how L was actually reached, and one thing the probe disproved.** There is **no `cvt.l` instruction in the tree**, so `IEEE_FMT_L` is produced by `trunc.l` alone. On pmax the first probe reported a Reserved Instruction for every `trunc.l.d` case, but the faulting pc was the harness's **`sdc1` readback stub** (stubs sit at `scratch + 4*i`; `sdc1` is index 7 → `+0x1c`), i.e. the MIPS-II 64-bit *store*, not the instruction under test. Re-read with two MIPS-I `swc1`s, `trunc.l.d` **does execute on the R3000A** and returns the pinned values (`3.0`→`3`, NaN→`0x7fffffffffffffff`, −2^63→`0x8000000000000000`). So GXemul's COP1 decoder does **not** gate `trunc.l` by ISA level even though it is MIPS III and an R3010 would raise RI — a pre-existing fidelity gap, unrelated to and unchanged by #273, recorded here only because it is what makes the L arm observable on pmax at all.

Verified: build **0/0** both trees (223 pmax / 224 arc objects); **pmax 15/15 + arc 13/13 → `uid=0(root)`**; log-hygiene greps **0** on both boot pty logs. **Measured on the committed build first** (`p2_fp_cvt.py`, TEST-FIRST): **11 of 13** non-control cases diverged from the hardware default, **identically on arc/R4000 and pmax/R3000A** ("arc vs pmax differences: none"). **#273 probe: 55/55 on arc, 44/44 on pmax** across `cvt.w.d`, `trunc.w.d`, `cvt.w.s`, `trunc.w.s` and `trunc.l.d` — all five invalid cases return the pinned constant on every instruction, every in-range control is unchanged, and both asymmetry boundaries land correctly (`-2147483648.5` → `0x80000000`; −2^63 → `0x8000000000000000` vs −2^63−2048 → `0x7fffffffffffffff`). **In-guest end-to-end on OpenBSD/pmax against a purpose-built pre-#273 binary:** `awk 'BEGIN{print sprintf("%d", 1e30)}'` gives **0 before → 2147483647 after**; `-1e30` gives **+2147483647**, the sign-independence that no software clamp would produce; in-range controls byte-identical on both binaries. **awk's `int()` is not a probe of this path** — it stays in floating point (`int(1e30)` prints `1.0000000000000000198…e+30` on *both* binaries and `int(3.9)` gives `4`, so it is not a truncating C cast); `printf`/`sprintf` `%d`, which casts a double to a C `long`, is the route that reaches the FPU. That distinction is why the in-guest gate is reported on the `%d` route and not the `int()` one.

## Forty-third round (#274, #275) — LANCE: descriptors held forever instead of dropped or failed
Both corrections are in `devices/dev_le.c` (not a divergent file; both trees stay byte-identical). Five sites met a descriptor they could not use and simply `return`ed, leaving OWN set and the ring pointer parked: the guest waited forever, and a well-formed descriptor behind the bad one was never reached. All five were reproduced on the committed build before anything was changed.

**The idle non-STP transmit descriptor (case d) — what the datasheet actually says, and why the test moved.**
AMD, *Am7990 LANCE Technical Manual* (1986), §4.5.2 "Transmit Descriptor Ring Format", printed page 4-4:

> When the LANCE is polling the Transmit Ring, it will skip over Transmit Ring entries having a bad format. For the first buffer in a packet, when the LANCE owns the buffer and STP (Start of Packet) is not set, it will simply turn the ownership back over to the host. The LANCE will then generate a TINT interrupt and go on to the next buffer. The LANCE continues to skip over transmit buffers (by clearing the OWN bit and setting TINT bit) until it finds a buffer with a good format (both STP and OWN bit set) to transmit.

So "skip" is the manual's own *label* for clear-OWN + TINT — the parenthetical defines it — which is why a register-summary reading of the same behaviour (printed page 1-27, TMD1 bit 09: "the LANCE will skip over this descriptor, poll the next descriptor(s) entry until the OWN and STP bits are set") can be misread as *leave OWN set*. The same loop is described independently on printed page 1-15 in the retry-abort context ("it clears the own bit and sets the TINT bit in each Descriptor Table Entry it polls until it finds a buffer with both the STP bit and OWN bit set"), and QEMU's `hw/net/pcnet.c` implements exactly this (`goto txdone` → clear OWN, store, set TINT, no error bit, no BCNT fetch). Hence: clear OWN, write tmd1 back, set TINT, advance — **no tmd1 ERR and no tmd3 bits**.
**The reorder** comes from the same manual, printed page 1-15: "the LANCE automatically polls the first transmit ring entry in memory. The polling occurs every 1.6ms and consists of reading the status word (TMD1) of the transmit ring entry until it finds the OWN bit and STP bit set to one" — and only *then* "transfers the low order bits of the buffer address from TMD0 and byte count from TMD2". The chip has not read TMD2 when it makes this decision, so gating the STP decision on the TMD2 `'1111'` mark or byte count is not hardware behaviour. The idle-!STP test therefore now sits **before** the tmd2 validation, and the probe confirms the behaviour is identical whether tmd2 is well formed or carries a cleared mark.

**CSR0 BABL on the #199 cap path — decided from the manual, and NOT set.** The panel split 3–1 in favour of setting it (a >64 KB chain must have exceeded the babble threshold). The manual's definition does not support that here. CSR0 bit 14 (Technical Manual, register section):

> BABL — BABBLE is a transmitter timeout error. It indicates that the transmitter has been on the channel longer than the time required to send the maximum length packet. … BABL is a flag which indicates excessive length in the transmit buffer. It is set after 1519 data bytes have been transmitted; the chip continues to transmit until the whole packet is transmitted or there is a failure.

and §4.9, printed page 4-15:

> BABL error occurs after the LANCE starts loading the 1519th byte to the SILO (maximum Ethernet packet is 1518 bytes). The LANCE continues to send the remainder of the packet following 1518 bytes.

Every clause is about bytes **actually put on the channel**, and BABL explicitly coexists with the frame still being transmitted. Our #199 cap is a host-side aggregate limit: `net_ethernet_tx()` is called only at ENP, which this path never reaches, so **nothing has been transmitted** when the cap fires and the frame is abandoned rather than completed. The threshold does not match either — the chip babbles at 1519 bytes, not at 64 KB, and this model does not set BABL anywhere else (a 1900-byte single buffer goes out silently), so setting it on this one path would be an inconsistency as well as an over-claim. BABL is also the heavier claim: it feeds `ERR`/`SERR` and `INTR` (`dev_le.c` `le_register_fix()`), §4.9 classes it with MERR as an error the driver "should recognize as fatal", and NetBSD/OpenBSD `am7990_intr()` counts it as a *second* `if_oerrors` on top of the one the descriptor's own ERR already produces. Deliberate omission, recorded here so it can be revisited if a guest is ever found that needs it.

**tmd1 ERR on the #199 cap path — SET, for two independent reasons.** The manual makes it mandatory once UFLO is set (TMD1 bit 14: "ERR — ERROR summary is the 'OR' of LCOL, LCAR, UFLO or RTRY"), and TMD3 bit 15 says the two travel together ("BUFF … If a Buffer Error occurs, an Underflow Error will also occur"). Independently, the driver requires it: NetBSD `sys/dev/ic/am7990.c` `am7990_tint()` takes `if (tmd.tmd1_bits & LE_T1_ERR) { … if_statinc(ifp, if_oerrors); } else { … if_statinc(ifp, if_opackets); }`, so a descriptor returned **without** an error bit is counted as a **successfully transmitted packet** — the emulator would be reporting a frame it dropped as a frame it sent. With ERR + `TBUFF|UFLO` the same driver prints "transmit buffer error" and calls `lance_reset()`, which is the documented recovery and the one a live OpenBSD 2.2 guest was observed to perform (it printed `le0: transmitter disabled`, issued STOP → INIT → STRT and restored `TXON` within one interrupt, losing only the killed packet).

**What is policy rather than silicon (stated plainly).** The manual gives **no** status behaviour for a descriptor that violates the rmd2/tmd2 `'1111'` programming rule. Consume-with-error on the transmit side and drop-with-`MISS` on the receive side are therefore **hardened emulator policy**: they are chosen because the alternative measured behaviour is an indefinite hold, not because a datasheet prescribes them. Likewise, `BUFF`'s documented trigger is "does not find the ENP flag in the current buffer and does not own the next buffer", which is *close to* but not identical with a host-side 64 KB cap; it is used as the nearest defined "this frame could not be completed from the ring" status.

**Reachability (honest).** Case (d) is **unreachable from a correct BSD guest**: NetBSD and OpenBSD `am7990_start()` both stamp `tmd1_bits = LE_T1_OWN | LE_T1_STP | LE_T1_ENP` on every transmit descriptor and neither does TX data chaining (Linux `declance.c` matches, with `LE_T1_POK|LE_T1_OWN`), so no correct driver ever creates an OWN'd non-STP entry. It is hardening. The same is true of every malformed-descriptor arm here: on the rigs the guest never posts one (see the counter below).

**#199 was a net improvement, not a regression.** The 64 KB cap traded an unbounded host-memory growth path — a guest re-arming a non-ENP descriptor could make the emulator `realloc()` without limit — for a log loop. This round *completes* it by adding the guest-visible half the original correction lacked (ERR + TBUFF|UFLO + TINT + TXON cleared + `txp` advanced), which also removes the log loop as a side effect. The cap itself is unchanged and still wanted.

**The would-fire measurement (the shipping gate).** A false fault in the extended receive lookahead is *silent* — a healthy chained frame would simply be truncated and dropped, which reads as a flaky network and never as a crash — so a successful boot proves nothing about it. The gate is an observe-only counter, compiled into the build tree only (est/ and GXEMUL-SEC/ untouched by construction), that evaluates the extended predicate wherever the old OWN-only predicate passed. Against the **changed** code it measured **`la_extra_reject` = 0** on a healthy boot with pings (`rx_calls=14 frames=14 top_badmark=0 top_badlen=0 top_len_min=top_len_max=1536`) and **0** on a flood (`rx_calls=321 frames=321`) — both lines byte-identical to the pre-change measurement — while its positive control, which forces chaining, still scores `la_extra_reject=1` for a cleared mark and 1 for a bad length on the next descriptor and 0 for a healthy one, so the zero is live code returning zero. The guest never chains in practice (OpenBSD 2.2 posts uniform 1536-byte buffers and the NAT caps inbound at 1500), which is why the lookahead is normally not even evaluated (`la_eval = 0`) and why the shadow counter was needed to get a sample at all.

**Documented, NOT fixed: STP on the last descriptor of a chained frame.** In `le_rx()` the end-of-packet block clears `d->rx_middle_bit` (and frees the frame) and the `STP` block a few lines below then sets `LE_STP` because `rx_middle_bit` is clear — so the **last** descriptor of a chained frame is stamped `STP` as well as `ENP`, and it carries the *whole* frame length in rmd3. A BSD driver reads that as a complete single-buffer packet (`am7990_rint()` accepts only `(STP|ENP)` and otherwise prints "dropping chained buffer"), i.e. the model's chained receive path would hand the driver the last buffer with a full-frame length. This is **pre-existing**, is not reachable on either rig (the guest never chains, as the counter above shows), and is out of scope for this commit; it is recorded here so that anyone who makes chaining reachable fixes it first.

Verified: build **0/0** both trees (223 pmax / 224 arc objects); **pmax 15/15 + arc 13/13 → `uid=0(root)`**; log-hygiene greps **0** on both boot pty logs; live ping **3/3, 0% loss**; all four tree copies of `dev_le.c` share one md5 and the divergence set is still exactly the five known files. Pre-change baselines (TEST-FIRST): the receive hold delivered *the same frame* after a mark repair; the transmit holds left descriptor 0 **and** the canary chip-owned with `TINT=0`, the bad-count arm printing 11 `buflen =` lines over five pumps and the #199 cap 12 warnings over six pumps, free-running at **27,345 lines/second**. Post-change: `MISS` + drop + next frame accepted (`rmd3 = 0x4e`) on receive; `tmd1 = 0x4300`, `tmd3 = 0xc000`, `CSR0 = 0x03a2` (TINT set, TXON clear) for (a)/(b)/(c); `tmd1 = 0x0000`, `tmd3 = 0x0000`, TXON kept and the canary transmitted in the same pass for (d), identically with a bad tmd2; the flood measurements fall to 1 line, 0 warnings and **0 lines in 3.01 s**.

## Forty-fourth round (#276, #277) — ASC diagnostic hygiene: one site gated, one latched, in the same commit
Both corrections are in `devices/dev_asc.c` (not a divergent file; both trees stay byte-identical) and both are output-only — no guest-visible state changes. They are the same *class* of defect (an ungated `fatal()` a guest can repeat) and they get **opposite** fixes, which is the interesting part of the round.

**The amplification was measured first, on the committed build.** The stray-offset arm of `DEVICE_ACCESS(asc)` emits **1.00 host lines per guest access**: 12 accesses → 12 lines at each of `0x10`, `0x40`, `0x300` and `0xff0`, reads and writes alike, with an in-range register printing **0**; free-running from a three-instruction guest loop that is **800,370 lines / 26.4 MB in 3.07 s**. `dev_asc_transfer()`'s unknown-phase arm and `dev_asc_newxfer()`'s "freeing previous transfer" were measured **together at 2.00 lines per guest store** once `cur_phase` has moved to `PHASE_STATUS` (9 stores → 9 + 8 lines; 5 stores → 5 + 5), identically on arc/PICA and pmax/DEC.

**The "variable payload → gate" heuristic is retired.** #272 justified its gate partly on the grounds that its payload was variable, so latching would hide real information. That is a **mis-classifying proxy** and it must not creep back in: #277's unknown-phase message also carries a variable payload (`cur_phase`) and is **latched** anyway. The axis that actually decides is **whether the guest is told what happened through some other channel**:
- **#276 — the guest is answered.** A read returns `odata`, a write is dropped, the access completes and the machine goes on. The message is a note about *our* coverage of a register file we do not model, so DEBUG is where it belongs.
- **#277 — the guest is not told.** The unknown-phase arm sets no interrupt and no status, so the transfer simply hangs; "freeing previous transfer" reports that a transfer the guest still believes in has been thrown away. Silence there turns a wedged guest into an unexplained hang with nothing in the log.

**A DEBUG gate is invisible in a normal run *and* under `-q`.** `main.c` prints INFO during startup and then subtracts one level, so the default settles at `VERBOSITY_WARNING`; `-q` sets `VERBOSITY_ERROR`, and `debugmsg_add_verbosity_level()` floors at 0. A `VERBOSITY_DEBUG` message is therefore suppressed in **both** modes — including the one the boot harness runs — which is precisely why gating is only ever appropriate for a site the guest learns about by other means, and why #269 kept `fatal()` for the FIFO diagnostics rather than lowering them below what the hygiene grep can see.

**Gate suppression cannot be tested with `-V step`.** `debugmsg.c:181` reads `if (!subsystem_breakpoint && !single_step && !ENOUGH_VERBOSITY(subsystem, verbosity)) return;` — while the debugger holds `single_step`, the verbosity test is **bypassed and a DEBUG message still prints**. Stepping the site therefore proves only that the code path is live and the probe is aimed correctly; it says nothing at all about the gate. Suppression has to be measured **free-running** (`continue`, `single_step` clear), and a bare zero from a free run proves nothing on its own — a mis-aimed loop yields zero too. So the identical free run is repeated with `-v -v` (SUBSYS_DEVICE at DEBUG) as a **positive control**, and the pc is read back after `^C` to confirm the CPU really was still in the hammer loop. #272's probe established this shape; this round reuses it, and adds the pre-change binary as a third reference point (**800,370 lines → 0** in the same 3-second window, same loop, same default verbosity).

**Two latches need two fields, and the probe has to prove it.** `unknown_phase_warned` and `newxfer_warned` are separate `int`s in `struct asc_data`. A single shared flag is a live failure mode, not a hypothetical — whichever message fired first would mask the other permanently — and that is exactly the copy-paste shape #269's verification had to rule out. The probe therefore fires one trigger and then the other **in the same session** and requires both to report 1: the second reporting **0** is the signature of the shared field. Neither latch is cleared by `dev_asc_reset()` (same rule as #269: RSTCHIP is guest-reachable, so clearing there would let a guest re-arm the flood); both are zeroed by the `memset` in `dev_asc_init()`. Triggers used: 12 SELECTs carrying a valid six-byte TEST UNIT READY CDB, which reach `dev_asc_newxfer()` with `xferp != NULL` but never enter `dev_asc_transfer()`, then 12 `TRPAD|DMA` stores with `cur_phase == PHASE_STATUS`, which do the opposite. Liveness is asserted on evidence *other than* the latched messages — the `TEST_UNIT_READY`s that reached the disk, the entries into `dev_asc_transfer()`, and `STAT & 7 == 3` read with a genuine guest `lbu` — so a trigger that silently stopped firing cannot be reported as a working latch. Counting rule (unchanged, and load-bearing here): each message is counted with its own distinct substring and **never** by subtracting one count from another.

**One string, four call sites, checked before gating.** A DEBUG gate makes a message invisible to any `-q` assertion, so the tree, the boot rigs and every regression/hygiene script were grepped for all four strings being changed (`asc: read from`, `asc: write to`, `unknown/unimplemented phase`, `freeing previous transfer`) before touching them. The only consumers anywhere are the two TEST-FIRST probe rigs that measured the defect; nothing in the harness matches on them. (The two `debug()`-level DMA and register-name variants of the same wording, further up the same file, are unchanged and remain gated behind `quiet_mode` / `ASC_FULL_REGISTER_ACCESS_DEBUG` as before.)

Verified: clean rebuild **0/0** both trees (223 pmax / 224 arc objects); **pmax 15/15 + arc 13/13 → `uid=0(root)`**; log-hygiene greps **0** on both boot pty logs for `panic`, `Segmentation`, `assert`, for all four changed strings and for `FIFO overrun` / `data_out_len == 0`; `dev_asc.c` byte-identical in all four tree copies and the divergence set still exactly the five known files. **#276 probe:** `-V step` 12/12 reads + 12/12 writes still printed, in-range control 0; free run **0 lines in 3.02 s** (2,010 bytes of host output) vs **800,370 lines / 26,414,220 bytes in 3.07 s** pre-change, pc verified inside the loop in both; `-v -v` positive control **505,944 lines**. **#277 probe:** `freeing previous transfer` **11 → 1** over 11 triggering SELECT rounds; `unknown/unimplemented phase` **12 → 1** over 12 triggering transfer stores *after* the other latch had already been set (the cross-check); **0 and 0** after `RSTCHIP`; liveness 12 selects / 12 transfers / `STAT = 0x83`.

## Forty-fifth round (#278) — the MIPS "LOW reference" diagnostic: nine ungated `fatal()` calls per guest access
One correction, in `cpus/cpu_mips.c` (not a divergent file; both trees stay byte-identical). It is output-only — no control flow, no state, nothing guest-visible — but this file is shared by **every MIPS machine in the tree**, not just pmax/arc, so it gets its own commit and its own bisect point rather than riding along with a device round.

**The amplification was measured first, on the committed build.** `mips_cpu_exception()`'s `if (tlb && vaddr < 0x1000)` arm emitted **nine separate `fatal()` calls** that together build **one** host line, once per guest access to a low virtual address: **1.00 lines per access**, per-iteration attribution `1111111111`, identically on arc/R4000 (`EXC4K`) and pmax/R3000 (`EXC3K`), with the raw transcript confirming **0** line breaks inside the message. `fatal()` is ungated, and — a detail worth stating because it inverts the usual assumption about this file — the site sits **outside** the `if (!quiet_mode)` block that opens at `:1846` and closes at `:1916`, so `-q` did **not** silence it before. It is now one `debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "LOW reference", VERBOSITY_DEBUG, …)`. `SUBSYS_EXCEPTION` is the subsystem the in-source TODO preferred and it does exist here (`misc.h:250`, named `"exception"` at `debugmsg.c:691`); the general MIPS exception message from **#210**, twenty lines below in the same function, already uses it. The nine calls existed only to switch field widths on `cpu->is_32bit`, which a single `%0*` width argument does in one call, so the 32-bit rendering is preserved exactly (`vaddr=0x00000000`, `pc=0x8001000c` on pmax) rather than being widened to 64 bits; the hand-written `[ … ]` brackets, the `\n` and the manual `cpu%i: ` prefix go away because `debugmsg` supplies all three.

**THE REPRODUCTION PRECONDITION. This is the most important note in this entry.** The site is gated on `tlb`, i.e. `memory_mips_v2p.c`'s `tlb_refill` — a genuine TLB **refill**, not any TLB miss. On a **never-booted** rig every TLB entry is zeroed, so the zeroed entry *matches* vaddr 0 (`entry_vpn2(0) == vaddr_vpn2(0)` and `entry_asid(0) == vaddr_asid(0)`), its V bit is clear, and translation takes the **TLB invalid** arm, which clears `tlb_refill`. The transcript shows it directly: `[ exception TLBL vaddr=… ]` with **no** ` <tlb>` marker, and the site prints **nothing — 0/10, on both CPUs**. Give the CPU a non-zero ASID (`EntryHi = 0x01` on arc, `0x40` on pmax — bits 0–7 on R4000, bits 6–11 on R3000), which is exactly the state any OS runs in once it has a user process, and the zeroed entries stop matching: vaddr 0 becomes a refill and the site fires **10/10**. A control at vaddr `0x1000` takes the refill (the `<tlb>` marker is present, 5/5) but prints **0**, isolating `vaddr < 0x1000` rather than "any TLB miss". **A reviewer who re-runs the obvious cold-rig test will get 0/10 and would, without this paragraph, conclude the defect was imaginary.** The exception rewrites `EntryHi` from the faulting address, preserving `vaddr_asid`, so the ASID must be re-asserted per iteration only because the probe also re-arms `pc`; the ASID itself survives.

**Why `VERBOSITY_DEBUG` and not the `VERBOSITY_WARNING` the in-source TODO asked for.** The panel split 2–2 on this and the measurements broke the tie. `main.c` prints INFO during startup and then subtracts one level (`debugmsg_add_verbosity_level(SUBSYS_ALL, -1)`), so a default run settles at `VERBOSITY_WARNING(1)` — a WARNING-level message therefore prints on **every single call**, which is the flood we are removing, and a WARNING-level gate was separately measured in this same batch flooding a free-running rig at **27,345 lines/second**. Under `-q`, `main.c` sets `VERBOSITY_ERROR(0)` and `debugmsg_add_verbosity_level()` floors at 0, so a WARNING is **invisible under `-q`** — exactly the mode the boot harness runs and greps. WARNING is thus the one level that fails **both** goals: too loud where we want quiet, silent where we want a tripwire. DEBUG is quiet in a normal run *and* under `-q`, and still visible under `-V` for the edge-branch proof. The semantics of the site agree with the measurement: with a non-zero ASID this fires on **every userland NULL dereference**, which is ordinary guest behaviour rather than an emulator deficiency, so it is not tripwire material. That reasoning is repeated in the source comment specifically so the TODO's WARNING is not "restored" later as a fix.

**Why there is no `ENOUGH_VERBOSITY()` pre-gate.** `debugmsg.c:181` is `if (!subsystem_breakpoint && !single_step && !ENOUGH_VERBOSITY(subsystem, verbosity)) return;`. The verbosity test is *deliberately* bypassed while `single_step` is set and whenever a subsystem breakpoint is armed. Wrapping the call in a raw `if (ENOUGH_VERBOSITY(…))` would therefore suppress the message under `-V step` — the mode every edge-branch proof in this project uses — and stop `breakpoint subsystem exception` from ever firing on this site, which is precisely the debuggability #210 added. `debugmsg` does its own gating and must be allowed to. The symbol lookup that precedes the call is not expensive enough to justify pre-gating it; if it ever were, the fix would be to move the lookup, not to add a gate that defeats the debugger.

**Gate suppression cannot be tested with `-V step`** (the rule established in #272 and reused here): stepping proves only that the call site is live and the probe is aimed correctly. Suppression is measured **free-running**, with the CPU parked in a self-sustaining exception loop — a two-instruction handler (`addiu s0,s0,1 ; lw v0,0(at)`, encodings verified by disassembly) written at **every** vector the low-address refill can reach (`base+0x000` TLB refill, `+0x080` XTLB refill, `+0x180` general once `EXL` is set, with `STATUS.BEV` checked so `base` is `0xffffffff80000000`), `at = 0` and a non-zero ASID. Each iteration counts itself in `s0`, so the fault traffic is **measured, not assumed**, and the pc is read back after `^C` to confirm the CPU was still in the handler. A bare zero from a free run proves nothing on its own, so the identical run is repeated at `-v -v -v` (DEBUG) as a positive control **and** on a purpose-kept pre-#278 binary as a regression baseline.

**On a healthy boot this site is latent.** Booting both rigs on the pre-#278 binary — where the message was an ungated `fatal()` that `-q` could not suppress — produced `LOW reference` **0** times across a full pmax 15/15 and arc 13/13 login (both still reaching `uid=0(root)`). So this correction buys hardening against a guest-repeatable flood plus a message the debugger can now trap, not the removal of noise the harness was already living with. Recorded here so the round is not later credited with a log-hygiene win it did not deliver.

Verified: clean rebuild **0/0** both trees (223 pmax / 224 arc objects); **pmax 15/15 + arc 13/13 → `uid=0(root)`**; log-hygiene greps **0** on both boot pty logs for `LOW reference`, `warning: LOW`, `exception LOW reference`, `panic`, `Segmentation`, `assert`, `Bus error` (the one `TODO` hit in the arc log is the pre-existing `[ pckbc: TODO: hack for non-8242 … ]` line); `cpu_mips.c` byte-identical in all four tree copies and the divergence set still exactly the five known files. **`LOW reference` grepped tree-wide and across every harness/regression script before gating:** the only consumers anywhere are the two TEST-FIRST probe rigs and one read-only marker counter, plus a retired `_archive/` audit classifier that also keys on `TLBL`/`exception`; no boot script or gating assertion matches it. **Blast radius:** five other MIPS machines (`testmips`, `baremips`, `evbmips/malta`, `sgi/o2`, `hpcmips/mobilepro770`) start under `-V`, reach the prompt, and emit output **byte-identical** to the pre-#278 binary. **Probe, 36/36 on both CPUs.** Step half: **10/10 = 1.00 per faulting step**, payload intact, **10 of 10** occurrences one physical line, `exception LOW reference:` ×10 and the old `warning: LOW reference:` wording ×**0**; controls 0 (cold TLB) and 0 (vaddr `0x1000`). Free-run half: arc **19,631,880 faults in 3.00 s → 0 lines** (2,010 bytes of host output in the whole window), pmax **19,366,920 in 3.01 s → 0** (10 bytes). Controls: `-v -v -v` prints **123,015** (arc) and **115,557** (pmax) lines; the pre-#278 binary at default verbosity prints **267,074 lines / 28,578,928 bytes** (arc) and **136,193 lines / 12,393,573 bytes** (pmax) in the same window. That baseline also prices the flood: in the same three-second window the flooding build got through **269,100** faults against the gated build's **19,631,880** on arc (**1.4 %**) and **136,620** against **19,366,920** on pmax (**0.7 %**), so an ungated `fatal()` a guest can keep firing costs roughly **99 %** of emulated throughput.

## Forty-sixth round (#279) — `float_emul.c`'s reserved-format diagnostics: five ungated `fatal()` sites, and one genuinely missing `return`
One correction, in `core/float_emul.c` (not a divergent file; both trees stay byte-identical). Like **#278** this is an arch-shared file, and shared more widely than that one: `ieee_interpret_float_value()` and `ieee_store_float_value()` are called by the **alpha, m88k, mips, ppc and sh** cores plus `dev_pvr`. **#273** touched this same file three rounds ago but was confined to the MIPS-only W/L arm, and said so; this round touches the paths all five families use, so it gets its own commit, its own bisect point and its own blast-radius gate. Everything is output-only except one `return` on a path that was already broken.

**The amplification was measured first, on the committed build, and it is the same on both CPUs.** Five sites print an ungated `fatal()` whenever the format argument is not S/D/W/L: `:64`, `:82`, `:154` in `ieee_interpret_float_value()` and `:216`, `:306` in `ieee_store_float_value()`. Stepping the instruction repeatedly on arc/R4000 and pmax/R3000A: `add.ps` (`0x46c00080`, two operands) → **6.0 interpret + 2.0 store = 8.0 host lines per instruction**; `abs.ps` (`0x46c00085`, one operand) → **3.0 + 2.0 = 5.0**. Per call that is **3.00** interpret lines and **2.00** store lines. `fd` is silently written **`0x00000000`** and the emulator survives, which is the whole reason the messages matter: nothing else tells anyone this happened.

**The missing `return` at `:216` is a genuine, if small, bug — confirmed by measurement, not by reading.** The two sites inside each function print **byte-identical text** after concatenation, so "two distinct strings" could never have been the test; the discriminator is the count **per call**, which is why the probe uses `abs.ps` (one operand → exactly one interpret call and one store call) alongside `add.ps` (two operands, which would otherwise confuse "two sites" with "two operands"). `:216`'s `default:` has no `return`, so it falls out of the first switch into the second switch's `default:` at `:306` and prints a **second** line for the same call. It now does `return 0`: `r` is still 0 at that point and the trailing `if (fmt == IEEE_FMT_S || fmt == IEEE_FMT_W) r = (uint32_t) r;` cannot change that for a format that is neither, so the returned value is **exactly** what the old path returned. The `:306` arm becomes unreachable; it is kept anyway, and latched with the same flag, so the invariant holds if that `return` is ever removed again. The interpret side's three sites are deliberately **not** given returns — they are latched, not restructured.

**Scope is PS-only, and that was measured rather than assumed.** `mips_fmt_to_ieee_fmt[]` (`cpu_mips_coproc.c:1029`) maps every fmt outside {S,D,W,L} to 0, which invites the conclusion that any reserved fmt floods this file. It does not: `cpu_mips_instr.c:4991-4995` routes only {S,D,W,L,PS} to `cop1_slow`, and every other reserved fmt hits the decoder's own single `fatal("COP1 floating point opcode = 0x%02x")` + `goto bad` at `:5006-5008` — one line, then the machine stops. The probe carries fmt 18 and fmt 23 as controls and both produce **0** `float_emul` lines on both CPUs.

**A one-shot latch per message, not a verbosity gate.** This batch converged on the rule that the axis is **whether the guest is told**, not whether the payload varies — and this site lands on the opposite side from **#276**, which is in the same batch and *is* gated. Here the guest is told nothing at all: `fd` is silently written 0, so the host line is the only record that the emulator met a format it does not model, i.e. a deficiency tripwire, and exactly one of them should survive into a `-q` boot log. A `VERBOSITY_DEBUG` gate would be invisible in a normal run **and** under `-q`, which is the mode the boot harness greps. #276's site is gated precisely because the guest **is** answered there (a read returns `odata`, a write is dropped), so its line is noise. `fatal()` is kept rather than converted: neither function has a `cpu` or a `machine` pointer in scope — verified in the signatures, `(uint64_t x, struct ieee_float_value *fvp, int fmt)` and `(double nf, int fmt)` — so `debugmsg_cpu()` is not available, and a bare `debugmsg()` would need a subsystem this helper does not belong to.

**The latches are PROCESS-GLOBAL, and that is a deliberate deviation — stated here rather than left for someone to discover.** #269 and #277 hang their latches on the per-device struct, so each instance warns once. `float_emul.c` has no instance: it is a stateless helper, called with a value and a format and nothing else. The flags are therefore file-scope `static int`s, and the cost is real if small — in a multi-machine emulation only the **first** machine's bad format is reported. There is one flag per **distinct message** (interpret, store) and never one shared flag, for the reason #277 already recorded: a shared flag lets whichever message fires first mask the other one for good. The probe checks exactly that, and never by subtracting one count from another.

**Recorded, deliberately NOT fixed: the upstream routing candidate.** A reviewer argued that the real fix site is not this file at all. An R4000 is MIPS III; PS (Paired Single) is MIPS-V/MIPS64; so an R4000 executing a PS-format COP1 op should take a **Reserved Instruction** exception, which makes `cpu_mips_instr.c:4995` admitting `COP1_FMT_PS` to `cop1_slow` the actual defect and `fd = 0` "a correctness bug wearing a hygiene bug's clothes". That is not implemented here, for three reasons: it is a **semantic** change to arch-shared instruction routing where this commit is output-only; it needs its own design panel and its own test-first reproduction; and it depends on an open question. **That open question is partly answered by this round, and the answer says the routing cannot simply be removed:** `mips_cpu_types.h` does contain CPUs with `isa_level == 64` and no `NOFPU` flag — `5Kc`, `5KE`, `SB1`, `SR7100` — for which PS is architecturally plausible (MIPS64r1 defines it; r6 removes it). So the fix has **two halves**: an ISA gate that raises RI below MIPS-V, *and* the fact that `float_emul.c` models no PS arithmetic whatsoever, so gating alone leaves those CPUs without the format they are entitled to. Whoever picks this up must decide both. It is the same family as the pre-existing observation recorded under **#273** — `trunc.l` executes on an R3000 although it is MIPS III and an R3010 would raise RI — namely that **the COP1 decoder does not enforce ISA level anywhere**.

**How each half of the probe was measured, including the part a latch makes impossible.** (i)/(iii)/(iv) are measured on the committed build: 12 `add.ps` plus 6 `abs.ps` produce **1 interpret line and 1 store line in TOTAL**, per-iteration attribution `100000000000` for each, each message counted with its own substring. Both counts being 1 in **one session** is the independence cross-check — interpret latches first because it runs first, so a single shared flag would have reported store as 0. (ii) is the one the latch makes unmeasurable on that build, so it is measured on a **purpose-built binary carrying the `return` fix with the latch condition forced true** (`if (!x)` → `if (1)`, built in throwaway copies of both build trees so neither real tree was touched): there the store side is **1.00 line per store CALL**, per-iteration `111111111111`, against **2.00** on the pre-change build — the `return` is what changed, and the latch is not hiding it. The same binary shows the interpret side unchanged at **3.00 per call** (`666666666666` per `add.ps`), which is the point: only `:216`'s `return` was added. **Liveness is asserted on evidence other than the latched messages**, so a dead trigger cannot pass as a working latch: `fd` is re-armed with a `0x11223344` sentinel before **every** step and read back with a genuine guest `swc1` + `lw`, giving **12/12** and **6/6** writes of `0x00000000`. A legal-format positive control (`cvt.w.d`, run **first**, before either latch can fire) prints 0 lines and returns the correct `0x00000001` on both CPUs — so "0 lines" can never be blamed on a broken FP path. (That control also caught a defect in the probe itself on its first run: it loaded the operand as a `$f0/$f1` pair on arc as well, but the R4000 rig runs with `STATUS.FR = 1` (`0x34000000`), where `$f0` is a full 64-bit register and the pair load leaves it `0.0`. The probe now loads at the width the CPU actually has. Recorded because the reading was a **rig** defect, not an emulator one, and the difference matters.)

Verified: clean rebuild **0/0** both trees (223 pmax / 224 arc objects); **pmax + arc both reach `uid=0(root)`**; `float_emul.c` byte-identical in all four tree copies (one md5) and the divergence set still exactly the five known files. **Probe: 22/22 with the latches engaged (11 per CPU), 20/20 on the forced-off build (10 per CPU).** **Before latching anything, the two message strings were grepped tree-wide and across every harness and regression script:** zero consumers in the source (outside `float_emul.c` itself), zero in the repo docs, zero in the boot rigs — the only consumers anywhere are the TEST-FIRST probe rigs themselves, so no gating assertion can be silenced by this. **Blast-radius gate:** 15 non-MIPS machines covering all four calling families plus `dev_pvr` — alpha (`alphabook1`, `alphaserver4100`), m88k (`testm88k`, `barem88k`), ppc (`testppc`, `bareppc`, `macppc/g4`, `pmppc`, `mvme1600`), sh (`testsh`, `baresh`, `hpcsh/jornada680`, `dreamcast`), plus `testarm` and `testriscv` — produce output **byte-identical to the pre-change binary, 15/15, on both trees**; 12 reach the debugger prompt, and the three that do not (`pmppc`, `mvme1600`, `dreamcast`) fail *identically* on the pre-change binary, `mvme1600` with the same pre-existing `SIGABRT` (rc 134) in both. **On a healthy boot this site is latent:** the pre-#279 boot pty logs — produced by a binary whose `fatal()` cluster was still ungated, so `-q` could not have suppressed it — contain **0** occurrences of `unimplemented format`. This round therefore buys hardening against a guest-repeatable flood, **not** the removal of noise the harness had been living with; stated so it is not later credited with a log-hygiene win it did not deliver.

**Probe-rig correction shipped alongside (`scratchpad/p2_fp_cvt.py`), called out because editing a probe deserves suspicion.** That rig's expectation column still encoded the pre-**#273** claim that −overflow and −Inf convert to `0x80000000`, so it reported **4 false divergences** (−Inf and −1e30, in both formats) against an emulator that is now correct. The expectation is now the rule #273 pinned from primary sources — `0x7fffffff` for **all five** invalid cases on R3010/R4010, with no sign dependence (R4000 User's Manual `CVT.W.fmt`; MIPS IV Rev 3.2 p. B-50; MIPS32 Vol II's rule selected by `FCSR.NAN2008`, a bit these CPUs do not have) — with a comment recording that the old value was the NAN2008/r6 rule, which also returns 0 rather than `0x7fffffff` for NaN, so adopting half of it would have been incoherent. The `-2^31` row deliberately **keeps** `0x80000000`: that value is in range, not an overflow. This is a correction of a stale **expectation** after the emulator was changed on primary-source evidence — not a probe edited to make a failing emulator pass — and it is recorded here so the distinction is auditable.

## Forty-seventh round (#280) — `dev_fdc.c`: the probe chatter, and why it is gated rather than latched
One correction, in `devices/dev_fdc.c` (not a divergent file; both trees stay byte-identical). The file's own header calls it "just a dummy skeleton", and the measurement bears that out: `DEV_FDC_LENGTH` is **6**, and **0x04 is the only offset the `switch` handles**. Reads and writes at 0, 1, 2, 3 and 5 all reach `default:`.

**Measured on the committed build first, in the cold debugger, with genuine guest instructions.** 10 one-byte stores → **10** host lines (1.00 per store); 10 one-byte loads → **10** (1.00 per load). The write arm was `2+len` `fatal()` **calls** producing exactly **one line** — only the closer carries the `\n`, and `va_debug()` emits it a character at a time — so `sb`/`sh`/`sw` at the same offset gave 1/2/4 byte tokens on one line each. The offset map was measured rather than read off the source: 0/1/2/3/5 print, **0x04 prints nothing**, and 6/7 are outside the device and produce `non-existant paddr` instead. A read-back after writing `0x5a` everywhere returns `0x5a` from the `default:` offsets and **`0x00` from 0x04** — the register the guest actually polls is hard-wired to zero, which is why the probe times out.

**The axis this batch settled on is whether the guest is told, and here it is — so this is a gate, not a latch.** The two hits on a healthy arc boot are `fdcprobe`'s reset pulse (`write reg 2 = 0x00`, then `= 0x04` = `FDO_FRST`), after which OpenBSD prints `fdc at pica0 slot 2 offset 0x0 not configured` and moves on. The probe fails through **modelled** behaviour; nothing hangs waiting for a message that is not printed. **A latch would have been actively wrong here** — it would suppress the *second* line of a two-line reset pulse, i.e. the only interesting thing the site shows. That reasoning is in the source comment, not only here, because the next person to look at this file will be deciding the same question. (#276 is the shape borrowed; #277/#279 are the shape rejected, and both are in this same batch.)

**Two implementation constraints worth keeping.** (1) The byte string is built into `char buf[3 * DEV_FDC_LENGTH + 1]` — **sized from the register array, never from `len` or `idata`** — and the loop is bounded by `DEV_FDC_LENGTH` *as well as* by `len`, so the `snprintf` cursor cannot walk off the end even if `memory_rw.c`'s clamp to the remaining device bytes were ever changed. No VLA, no heap. (2) The read arm's payload is deliberately **unchanged**: adding the returned value to the message was proposed and rejected, because this commit gates a message and changing its contract at the same time makes the two indistinguishable in a bisect.

**Offset 0x04 stays silent, asserted in every mode.** `out_fdc()` (OpenBSD `arc/dev/fd.c`) spins ~100,000 times polling the Main Status Register at offset 4 on every arc boot; the offset is quiet today only because it is the one handled case. If a refactor had routed it through the new `debugmsg`, a `-v -v` run would emit ~100k lines. The probe hammers 0x04 under `-V step` (12 reads + 12 writes → **0**) and free-running under `-v -v` (**0** over a 3.02 s window, `pc` confirmed still in the loop).

**Blast radius, corrected from an earlier working assumption.** `BUS_ISA_FDC` is passed by exactly **one** caller in the tree, `machines/machine_algor.c:77`. ARC **PICA and MAGNUM** add the device directly (`fdc addr=0x80003000`, `machine_arc.c`), and **pmax does not instantiate `fdc` at all** — so a pmax boot is not evidence about this gate and is not presented as such. The arc boot is.

Verified: clean rebuild **0/0** both trees (223 pmax / 224 arc objects); pmax **15/15** and arc **13/13** harness steps to `uid=0(root)`; `dev_fdc.c` one md5 across all four tree copies; divergence set unchanged. **Gate probe, all three halves, with the pre-change binary kept as a third reference point:** under `-V step` the site still fires **12/12** reads and **12/12** writes (this proves only that the call path is live — `debugmsg.c:181` skips the verbosity test while `single_step` is set — which is exactly why the free run is also required); the collapsed message carries **1 line / 1, 2, 4 byte tokens** for `sb`/`sh`/`sw`; free-running at default verbosity → **0** lines, `pc` still inside the hammer loop, against **802,324** lines in 3.09 s from the pre-change binary and **528,517** in 3.08 s from the same post-change binary at `-v -v`. Boot logs: arc `[ fdc: … ]` **2 → 0**, `fdc at pica0 slot 2 … not configured` **1 → 1**, pmax 0 → 0.

*(One probe defect found and fixed during the run, recorded because editing a probe deserves suspicion: the first version reused the mark names `SW_B`/`SW_E` for both the amplification block and the 4-byte width case, and `seg()` resolves a tag to its **first** occurrence, so the width test silently measured the earlier block and reported "12 lines, 1 token". The marks were renamed; no assertion was weakened, and the diagnosis is independently confirmed by the fact that the **pre-change** binary passes the same width check with the renamed marks.)*

## Forty-eighth round (#281, #282) — ASC: a short DATA\_IN transfer that claimed the full count had moved
Two corrections, both in `devices/dev_asc.c` (not a divergent file; both trees stay byte-identical). #281 is a **semantic** change on a path every boot traverses, which is why it is split from the hygiene commit before it and why it rests on the guest's own source.

**Measured on the committed build first, on arc and pmax, and the measurement is the finding.** Driving a real `READ(6)` for one block (target returns 512 bytes) with the ASC transfer count set to 8,192, then reading the registers in the only safe order — `STAT`, `TCL`, `TCM`, `STEP`, and `INTR` **last**, because reading `NCR_INTR` clears `STAT`/`INTR`/`STEP` — gave `STAT 0x93` (INT\|TC\|STATUS phase), residual `TCL/TCM = 0x00/0x00`, `INTR 0x18`, `STEP 0x04`, GE and PE clear. The **control** — the identical transfer with the count set to exactly 512 — gave **the same six values**. A short transfer was **bit-for-bit indistinguishable from a complete one**: `NCRSTAT_TC` set and the residual zeroed, i.e. the emulator asserting that all 8,192 bytes had moved when 7,680 never left the target. The file already contradicted itself about this: `:1058` **clears** `NCRSTAT_TC` when a DMA command loads the count.

**The safety question ("does making this honest break the guest?") is answered from guest source, not from plausibility.** OpenBSD 2.2, `C:\DocumentNoSnc\CC\OpeBSD_2.2_CD\.codex-audit\clean-src\`:
* **TC is never tested.** `SCRIPT_MATCH(ir,csr) = ((ir) | (((csr) & 0x67) << 8))` — `sys/dev/tc/asc.c:256` and `sys/arch/arc/dev/asc.c:236` — masks TC (0x10) **out** of the status byte before the script dispatch. Clearing TC cannot change which script step runs.
* **The residual is read and acted on.** `asc_last_dma_in()` (`asc.c:1531-1546`): `ASC_TC_GET(regs,len); len = state->dmalen - len; state->buflen -= len; bcopy(state->dmaBufAddr, state->buf, len);` and `asc_end()` (`:1396`) publishes `scsicmd->resid = state->buflen`, which becomes `b_resid`.
* **The counter the driver reads is 16 bits and `TCH` is never read:** `ASC_TC_GET(ptr,val)  val = (ptr)->asc_tc_lsb | ((ptr)->asc_tc_msb << 8)` (`arch/pmax/dev/ascreg.h:173`, `arch/arc/dev/ascreg.h:150`), with `ASC_TC_MAX 0x10000`. Hence: write both bytes, leave TCH alone.
* **The old behaviour actively harmed the guest.** Sized by a zero residual, that `bcopy` copied 1,024 bytes the target never sent over the top of the driver's own pre-zeroing; `sd_mode_sense()` (`sys/scsi/sd.c:883`) `bzero`s its buffer explicitly "so that checks for bogus values of 0 will work in case the mode sense fails". Being honest restores that.

**Both bytes, and the masks, are load-bearing.** On pmax the honest residual is **1024 = 0x0400**, whose **low byte is 0x00** — a TCL-only fix would leave `0x0000`, indistinguishable from "complete", and would pass a careless check. Every assertion in the probe therefore names **TCL and TCM and the TC bit**. `reg_ro[]`/`reg_wo[]` are `uint32_t` (`dev_asc.c:152-153`), not `unsigned char`, and the DEC-mode read path returns the full 32-bit `odata` (`odata = d->reg_ro[regnr]`), so a residual above 255 would leak on a 4-byte register read if the `& 255` on each byte were dropped.

**THE GATING GUEST OBSERVATION IS pmax READ CAPACITY — deliberately not INQUIRY.** `rz.c:311` is `if (biowait(&sc->sc_buf) || sc->sc_buf.b_resid != 0) return (0);` — **exactly zero or nothing**. `sc->sc_blks` is set only past that test, and `rz.c:423` prints `rz%d: %dMB, %d %d byte blocks` only `if (sc->sc_blks)`, so the presence of `rz1: 300MB, 614880 512 byte blocks` in the boot log **is** the observation that `b_resid` was 0 on that command; the disk would otherwise fail to establish geometry *silently*. It is present and unchanged, and it must be: `sc_capbuf[8]` gives `b_bcount = 8`, the emulator's `SCSIBLOCKCMD_READ_CAPACITY` allocates exactly 8 (`diskimage_scsicmd.c:448`), so the residual is 0 and TC is still set. **INQUIRY is not the gate** even though it is the command the diagnostic fires on: `rz.c:374` only needs `(i = sizeof(inqbuf) - b_resid) >= 5`, ~1,063 bytes of slack, so an arithmetic error there would be absorbed **invisibly** — the same "a false fault here is silent" shape recorded under #267. It does corroborate, though: the attach line still takes the `i >= 36` branch and prints `rz1 at asc0 drive 1 slave 0 <DEC RZ58     (C) DEC rev 2000>`, now with the true `i = 44` rather than the fictitious 1,068. arc uses MI `sd`, which has no `resid != 0 → error` test, and its `sd0: 1024MB, 2081 cyl, 16 head, 63 sec, 512 bytes/sec, 2097648 sec total` line is likewise unchanged.

**The residual is taken at the ASC boundary, not from the #263 R4030 callback — a deliberate non-wiring.** `programmed − actual` is computed from the count snapshotted before the clamps. One reviewer argued the DMA controller's return value is the more truthful source; two rejected it and the risk is concrete: the callback's return is discarded at all three call sites today, honouring it would re-open the #264 retry-semantics adjudication (a wrong-direction zero-return becomes a guest `TRANSFER` retry livelock), and it would change the guest-visible outcome of exactly the count-mismatch case #263 exists to guard. **Recorded here as a known, deliberately unwired seam**, so a later reader does not mistake it for an oversight.

**The dead `memset` is removed, and the history is partly ours.** It zeroed exactly the region the following `memcpy` overwrites, and on arc it targeted `d->dma`, which is not the destination at all (the R4030 is). But it was not always dead: upstream `39748e3` wrote `memset(…, 0, lenIn2)` — the **full un-clamped guest count** — and **our own later hardening clamped that third argument to `lenIn`**, which is what made it a no-op *and* silently changed the pmax tail from zeros to stale bytes. That is stated plainly rather than described as inherited. With the honest residual the driver's `bcopy` no longer reads that tail at all, which is why zeroing is now unnecessary rather than merely redundant.

**#282, and why the witness is left ungated this round.** `size_t lenIn` / `size_t lenIn2` were passed to `%i` twice with no cast — undefined behaviour on LP64, benign in practice on this ABI but not defensible. `(int)` casts, not `%zu`: `%zu` appears **0 times in the entire tree** (grep-verified across `src/` and `include/`), and the neighbouring warning at `:454-457` already casts to `(int)`, so this is both file- and tree-consistent. The message itself stays **ungated**: once the residual is honest the condition stops being an anomaly and demoting it to `VERBOSITY_DEBUG` becomes right, but doing that in the same commit that changes the semantics would remove the only instrument that shows the new behaviour. **Gating it is the intended follow-up.**

**Out of scope, documented not reproduced.** `:592-598` (DATA\_OUT) and `:839-842` (COMMAND-phase DMA, which sets TC *while* writing back the full count rather than zero) tell the same lie and were not driven, so they are not touched. `:1027-1030` is Gavare's own `#if 0` around the TCL/TCM copy-through, commented "Transfer count lo and middle" — he knew the counter must not mirror the write registers, which is precisely **why** a written residual survives until the next DMA reload. `:1275-76` also zeroes TCL/TCM but is inside `#if 0` and is not a clobber risk.

Verified: clean rebuild **0/0** both trees (223 pmax / 224 arc objects); pmax **15/15** and arc **13/13** to `uid=0(root)`; `dev_asc.c` one md5 across all four tree copies; divergence set unchanged. **Probe: 3 cases × 2 machines, every one asserting both residual bytes and the TC bit.** Short (512 of 8,192): residual **7,680**, `TCM 0x1e`, `TCL 0x00`, TC **clear**, `STAT 0x83` — no longer `0x93`. Matched (512 of 512), the no-regression half: residual **0**, TC **still set**, `STAT 0x93`, and the diagnostic still silent. Raw-count-zero (512 of 65,536, the corner where a count register of 0 means 65,536): residual **65,024**, `TCM 0xfe`, `TCL 0x00`, TC clear. That last corner is also why TC matters at all — a 16-bit counter cannot represent 65,536, so a full 65,536-byte transfer and a zero-byte one both read back as `0x0000`, and the status bit is the only thing that separates them. Data movement is unchanged (the 512 bytes that did arrive are byte-correct against the host image; the tail past them is untouched, as it was before). Guest-visible SCSI/disk lines byte-identical to a pre-change boot on both machines; live LANCE ping **3/3, 0% loss**; in-guest FP unchanged; `{ asc: data in … }` **1 pmax / 5 arc, unchanged**, and 0 panics/aborts/`unknown phase` on either.

## Forty-ninth round (#283, #284, #285) — the DATA\_OUT half: bytes committed to the image that the guest never supplied
Round 48 closed with two sites listed as "out of scope, documented not reproduced": `dev_asc.c`'s DATA\_OUT arm and its COMMAND-phase DMA arm. Both were then driven, and the first turned out to be worse than the DATA\_IN lie it mirrors — it does not merely misreport, it **writes**.

**Measured on the committed build first, on arc, and the measurement is the finding.** `dev_jazz_dma_controller()` has returned the number of bytes it actually moved since #263 (`dev_jazz.c:269`). `dev_asc.c` discarded that return at every call site and advanced `data_out_offset` by the **requested** `len2`. Driving a real `WRITE(6)` of one block with the ASC count at 512 and the R4030 count at 128: 128 bytes copied, offset advanced 512, the disk gate at `diskimage_scsicmd.c:778` (`data_out_offset != size`) **passed**, and 512 bytes were committed to the image — **384 of them never supplied by the guest**, read back as 128 × 0x33 followed by 384 × 0x00. The registers gave the guest nothing to go on: the short case and a matched 512-of-512 case were **bit-for-bit indistinguishable** — `STAT 0x93`, TC set, `TCL/TCM 0x00/0x00`, `STEP 0x04`, `INTR 0x18`.

**#263's `clearflag = 1` is, at HEAD, the only thing keeping this to destruction rather than disclosure.** The counterfactual was run: with `clearflag` back at 0, the same case wrote 384 bytes of the **previous command's `data_out` heap buffer** onto the disk image. That is worth stating plainly because it inverts how #263 has been described until now — it was filed as a defence-in-depth zeroing, and it has in fact been load-bearing. After #283 it becomes defence in depth again.

**The fault-injection table, in full.** Run on OpenBSD 2.2/arc at a root shell, `dd` to the disk with the fault armed mid-run from the host, 50 s of observation per case. Route 0 forces the R4030 byte count to zero (the copy loop runs zero iterations and the #263 tail returns 0); route 2 halves it (a positive partial); "no remedy" honours the return and reports an honest residual but adds no terminal state.

| design | fault | outcome |
|---|---|---|
| HEAD (discard the return) | zero return | **58 hits in 63.3 s, no symptom at all** — silent corruption, `dd` reports success |
| no remedy, honest residual | zero return | `panic: asc_intr` on hit #1, **zero retries** |
| no remedy, honest residual | positive partial | panic |
| disconnect only when actual == 0 | zero return | survives |
| disconnect only when actual == 0 | **positive partial** | **panic** — the remedy never fires |
| abort on ANY short | zero return | survives |
| abort on ANY short | positive partial | survives |

Two things follow, and neither was predicted. **There is no livelock**: #264 feared that returning 0 would send the guest into a `TRANSFER` retry loop, and the guest instead dies immediately, with no retry at all. **#264 was reasonable on the evidence then available** — it was reasoning about a zero-length-buffer abort with no fault injector in existence, and the retry hazard it named is a real shape, just not this driver's. It is recorded here as superseded by measurement, not as a mistake. And **the "honest residual lets the guest recover" theory is refuted by the guest's own panic line**: `asc_intr: data overrun: buflen 8192 dmalen 8192 tc 8192 fifo 0` — it read the honest residual and panicked anyway. The arc driver dispatches on **phase** (`SCRIPT_MATCH` masks TC out with `0x67`), `ASC_CSR_TC` is referenced nowhere in `arch/arc`, and `xs->timeout = 60000` (`sd.c:623`) is stored but never armed.

**The disconnect is a deliberate robustness approximation. It is not hardware fidelity, and must never be described as such.** A real 53C94 does not synthesize a disconnect when DREQ stops coming; it **stalls**. The measurement says stalling panics the guest, and an instantaneous emulator has no way to express an indefinite bus stall, so `NCRINTR_DIS` is chosen as the nearest guest-handleable terminal state. The faithful path is the R4030 `DMA_INT_SRC` translation-fault interrupt, which needs an invalid-address register and a `TL_IE` wire and has been on record as a known gap since #267. The approximation is at least internally coherent: a real mid-DATA\_OUT target disconnect leaves exactly the register state now written — a residual counter with TC clear — so the guest's disconnect handler consumes a consistent state rather than a lie.

**Both call sites, and the comparison is against the POST-clamp count.** Two reviewers independently flagged that fixing only the fresh-transfer path would leave the multi-transfer continuation able to commit an underfilled final chunk, so both are captured. All four converged independently on comparing `moved` against `len2` **after** the `data_out_len - data_out_offset` and `ASC_DMA_SIZE` clamps: comparing against the programmed count would trip a spurious disconnect on a benign re-entry, where the disk simply wants less than the guest offered — the over-programmed case (512 wanted, 8,192 programmed) is a normal, correct transfer and must stay one. The `len2 > 0` guard is load-bearing for a second reason: `len2` is `int` and the first clamp can make it **negative**, which `(size_t)` would promote to an enormous value and turn every transfer into a "short" one.

**#267 and #268 are sources of this callback's shorts, and they are load-bearing for each other with #283.** The translation-limit break and the 20-bit count mask both stop the copy loop early, and `moved < requested` covers them mechanically. But `dev_jazz.c:266` zeroes `dma0_count` even on a limit break, so the R4030 **cannot resume mid-transfer** — which is consistent only because the fabricated disconnect forces the guest to re-arm the whole transfer. Neither is safe alone.

**The diagnostic is new, and it had to be.** During design it was claimed the existing `[ asc: data_out, multitransfer … ]` line at `:610` would serve as the witness. Two reviewers independently refuted that and they were right: under this fix the short path `return`s **before** that line, and it is a `!quiet_mode`-gated `debug()` in any case — invisible in the mode the boot harness runs in. The claim was a leftover from a rejected design in which the transfer continued; it is recorded here so it is not re-proposed. The corruption had **no witness whatsoever** before this round, which is the whole reason it measured as "58 hits, no symptom".

**#284 — "nothing moved" and "complete" at the same time.** In `dev_asc_select()`'s DMA arm every one of the `len` bytes is copied by an infallible loop that exits at `i == len`, so the honest residual is zero; the counter was nevertheless loaded with the **full count** while `NCRSTAT_TC` was asserted. Measured: count 6 → `TCL 0x06`, count 262 → `TCL 0x06 TCM 0x01`, `TC = 1` in both. **Stated carefully: this is harmless today.** `:1091-1094` reloads the counter from the write-only registers on the next DMA command, so the stale value is overwritten before any data-phase read, and although the pmax driver does read the counter on the interrupt path (`sys/dev/tc/asc.c:1013`, gated by `DMA_IN_PROGRESS`) **no case was constructed in which that read coincides** — so no guest-visible harm is claimed. It is not latent, though: `sys/dev/tc/asc.c:805` issues `SEL_ATN|DMA` for every SCSI command, and the site fires **1,659 times per pmax boot**; arc preloads the CDB into the FIFO and reaches it zero times. **Open question, recorded rather than acted on:** one reviewer disputed whether the count-262 case proves the real-silicon outcome, arguing that a real target changes phase after the actual CDB and would leave a residual with TC **clear**. That is plausible and unmeasured. The count-6 case is the conformance witness this round rests on; 262 is not claimed as one.

**#285 — the gate that had to be written in the right order.** `diskimage_scsicmd.c:1126` refused an **empty** `data_out` buffer but accepted a **partial** one, and the parse below reads fixed offsets up to byte 11. Measured: MODE SELECT(6) with 11 of 12 bytes transferred committed `logical_block_size = 4096` where the guest's parameter list said **4097** — a value computed from byte 11, which was never transferred — confirmed guest-side by a READ CAPACITY(10) reading 4096 back. #205's guard cannot catch it: `data_out_len` **is** 12 on re-entry. This was the only `data_out` gate in the file that was not `!= size`.

**The naive tightening would have shipped a regression, and this is the part worth remembering.** `xferp->data_out_len = 12` is assigned **inside** the `data_out_offset == 0` block. So on first entry `data_out_len` is **0**, and `if (data_out_offset != data_out_len)` evaluates `0 != 0` → false → never fires → falls through to #205 with `data_out == NULL` → silent GOOD status, and the 2048-sector setup this branch exists for **never runs**. The set-then-compare form is correct under either reading. One reviewer caught this; another got it wrong. The gate that matters is therefore not "the partial no longer commits" but "**a complete one still does**", and it is asserted directly: 12 of 12 bytes supplied commits **2048** for the NetBSD list and **4097** for the list whose partial form fabricated 4096.

**Blast radius, checked independently by two reviewers who agreed.** Four HBAs reach `diskimage_scsicommand()`, and none depends on the permissive gate. `dev_osiop.c` stays in DATA OUT on `res == 2` and appends (`:546-547`) — the same contract the strict `:778` gate already demands of it. `dev_mb89352.c` always arrives with `offset == data_out_len` (`:248-261`, `:432`). `dev_wdc.c` never populates `data_out` at all. `scsi_transfer_allocbuf()` frees and reallocates on every call and sets `*lenp = want_len`, so no path can leave a 12-byte length describing a shorter buffer. **One reviewer's additional finding, recorded as UNMEASURED:** `dev_osiop.c:519-521` passes `clearflag 0` on its DATA\_OUT `allocbuf`, so at HEAD a partial osiop supply parses an **uninitialised heap tail** at `:1154-1157` — the same `clearflag = 0` family flagged in round 34. The strict gate makes that unreachable, which makes this a **reachable** fix on luna/hpcsh rather than future-proofing, and is the argument against skipping the commit. It was not reproduced.

**Still open, carried forward deliberately.** #281's residual on the arc DATA\_IN path is still `programmed − lenIn2`, i.e. it uses the count the transfer was *allowed* to move rather than what the controller *did* move; honouring the return at `:456` cascades into the multi-transfer buffer management at `:478-486` and is tracked separately rather than bundled here.

Verified: clean rebuild **0/0** both trees (223 pmax / 224 arc objects); pmax **15/15** and arc **13/13** to `uid=0(root)`; `dev_asc.c` and `diskimage_scsicmd.c` each one md5 across all four tree copies; divergence set unchanged at five files (`dev_jazz.c`, `diskimage.c`, `machine_arc.c`, `arcbios.c`, and `dev_ne2000.c` which exists only in SEC). **#283:** the corrupting case leaves the block **byte-identical to before the transfer**, `TCL 0x80`/`TCM 0x01` = residual **384**, TC **clear**, `STAT 0x80`, `INTR 0x38`, `STEP 0x00`, one diagnostic line; matched and over-programmed controls unchanged at `STAT 0x93` / TC set / residual 0 with all 512 persisted bytes guest-supplied; on the guest, **both** fault shapes survive with 0 panics and 0 `data overrun`. **No-regression, the union of all four observations the panel proposed, because they did not converge and the union is cheap:** 0 diagnostic lines on six healthy boot logs; `moved == requested` on **145/145** pmax and **209/209** arc DATA\_OUT transfers with a positive control scoring 1 on the deliberately short case; the pmax changed-block set against the golden master **identical** across two pre-change boots and the post-change boot (125 blocks); the pmax boot transcript **identical** (101 distinct / 116 total lines) across all three. **The literal "byte-identical disk image" form of that gate is not well posed and was not faked:** two boots of the *same* pre-change binary already differ (680 bytes pmax, 1,653 arc) because the guest writes wall-clock timestamps, so the deterministic changed-block set is used instead. On arc that set varies run to run even same-binary (the varying blocks are `/var/log/messages` and a `/var/run` directory block holding `inetd.pid`), so the arc half rests on the mechanism instead: with `do_short = 0` every DATA\_OUT transfer took the unchanged path, and `cmddma = 0` and 0 MODE SELECTs mean #284 and #285 executed no changed line on that boot at all. **#284:** counter reads **0 with TC set** on both machines; **1,659** hits per pmax boot and **0 of 4,136** guest `TCL`/`TCM` reads able to observe the changed value, against a positive control scoring 4. **#285:** the 11-of-12 partial keeps block size at **512** (was 4096); a normal MODE SELECT still commits **2048** and **4097**; 20-machine six-architecture smoke **byte-identical 20/20** on both trees against the pre-change binary, 17/20 reaching the prompt identically before and after. Log hygiene: **0** panics either rig, `{ asc: data in … }` unchanged at **1 pmax / 5 arc**.

## Fiftieth round (#286) — the DATA\_IN counter: our own residual was still the requested count

Round 48 (#281) made the `PHASE_DATA_IN` residual honest with respect to the ASC's own clamps, and
round 49 recorded, against our own work, that it was still computed from `programmed - lenIn2` —
the count **requested** — and so remained dishonest on arc whenever the R4030 moved less. This
round closes that, and with it the last discarded `dma_controller` return in the file.

| # | file | Problem | Fix |
|---|---|---|---|
| 286 | `devices/dev_asc.c` | `PHASE_DATA_IN` discarded `d->dma_controller()`'s return and computed the residual from the requested count, so a short transfer reported residual 0 with `NCRSTAT_TC` set — indistinguishable from a complete one — while the multitransfer block advanced `data_in` by the requested count regardless | capture the return; on `lenIn2 > 0 && moved < lenIn2` write residual `programmed - moved` to TCL **and** TCM, leave TC clear, emit one witness, and `return 0` **before** the multitransfer block |

### Why the guest cares, and a distinction that must not be blurred

`ASC_TC_GET` (`arch/arc/dev/ascreg.h:149`) reads exactly the TCL/TCM pair written here, and it
appears at **six** sites in `arch/arc/dev/asc.c`; `asc_last_dma_in()` derives `state->buflen` and
`xs->resid` from it. So the value is consumed, not inert.

This does **not** contradict the round-47/49 record that `ASC_CSR_TC` is referenced nowhere in
`arch/arc` — re-verified, zero occurrences. That is the status **bit** (`0x10`), which
`SCRIPT_MATCH` masks out with `0x67`. The bit is ignored; the counter is not. **Do not generalise
the former into the latter** — a future round reasoning "arc ignores TC, so the residual does not
matter" would be wrong.

### The terminal state was chosen by fault injection, over the panel majority's reasoning

Four seats reviewed (Codex was unreachable — see below). Three specified the #283 mirror; one
dissented, arguing the transfer should instead be terminated normally so the guest's own
resume path could run. Both the dissenting seat and one supporting seat independently required a
DATA\_IN measurement before shipping, so the split was settled by experiment. Three designs were
compiled into one binary, selected at runtime, with a single-shot short injected on the Nth
to-memory callback, at **two independent injection points**:

| design | point 1 (N=40, K=64) | point 2 (N=120, K=128) |
|---|---|---|
| discard the return (HEAD) | 13/13 steps, no report — the silent defect | 11/11 steps, no report |
| honest residual, terminate normally | **panic** | **panic** |
| honest residual, abort → DISCONNECT (**shipped**) | no panic, transfer abandoned | no panic, transfer abandoned |

The dissent's argument — that the benign clamp path already produces a TC-clear nonzero residual
safely on every healthy boot — did not survive contact: truncating mid-DMA leaves the guest's
script state machine disagreeing with the controller, and it panics at both points.

**The dissent was still right about the mechanism, and that finding is kept.** `NCRCMD_ENSEL`
(`dev_asc.c:1221-1225`) is `/* TODO */ break;` — an unimplemented no-op — so when the guest
answers the synthesized disconnect with `ASC_CMD_ENABLE_SEL`, nothing reselects. The shipped fix
therefore **reports the fault; it does not repair it**. That is a deliberate robustness
approximation, as in #283, not fidelity; a real 53C94 would stall awaiting a DREQ. The faithful
path remains the R4030 `DMA_INT_SRC` fault interrupt, a known gap since #267.

A correction to how #283's evidence was carried into this round: "the guest survives" there meant
"did not panic", **not** "recovered" — round 49's own matrix recorded `records out 0` for the
abort designs against `4+0 records out` for HEAD. The brief that opened this round over-read that,
and the dissenting seat caught it.

### Reachability — stated plainly

**Latent.** A control boot logged **2282** DATA\_IN transfers with **zero** shorts.
OpenBSD 2.2/arc derives the R4030 count and the ASC counter from the same `len`
(`asc_dma_in()` → `DMA_START` + `ASC_TC_PUT`), so #263's clamp, #267's break and #268's mask
cannot bite by construction, and the direction check cannot fire either. Same standing as #283
(0 of 145/209). This round is **not** credited with a log-hygiene win; what it buys is that a
fault our own guards detect can no longer be reported to the guest as success.

### Panel note

**Five seats, but Codex 5.6-SOL took three attempts.** The first two returned
`ERROR: Selected model is at capacity` — the first after 324,615 tokens of exploration — and the
third answered. It **concurred** with the shipped design, deriving the same guard, the same
`programmed - moved` residual and the same placement independently, and it independently
confirmed both of this round's load-bearing readings: that "`ASC_CSR_TC` is unused" applies only
to the status **bit** while the driver actively consumes TCL/TCM, and that "#283's DATA\_OUT
result did not by itself establish the correct DATA\_IN terminal state; direction-specific
testing was necessary."

**Its one substantive criticism was accepted and acted on:** the first form of the in-code
comment ran to roughly 55 lines, longer than any other in this file and out of proportion to a
twelve-line change under a charter that asks for terse, minimal edits. It was cut to about 30,
keeping the mechanism and the two load-bearing warnings (the counter-versus-bit distinction, and
that `NCRCMD_ENSEL` is a no-op so the transfer is abandoned rather than retried) and deferring
the rest to this round block. Its other notes were line-number precision — `:421-425` reduces
`lenIn`, not `lenIn2`, so `lenIn2` is not directly clamped twice — and one observation recorded
as a **separate** gap, not folded in: `dev_jazz_dma_controller()` counts loop-accounted bytes and
discards both `memory_rw()` return values, so its count is not proof of delivery.

**A trap in verifying seats, worth keeping:** a seat's output can *look* complete, because the
brief embeds the completion marker in its own REQUIRED OUTPUT FORMAT section, so any seat that
echoes its prompt satisfies a naive marker grep. Codex's first failed run matched four times
while having answered nothing. Require the marker in the file's **tail**, and never count a seat
that did not answer as agreement.

---


## Fifty-first round (#287) — the S-format store: overflow produced a NaN, underflow lost the sign

| # | file | Problem | Fix |
|---|---|---|---|
| 287 | `core/float_emul.c` | `FP_NORMAL` wrote the fraction and then forced the biased exponent to all-ones without clearing it — exponent-max plus a nonzero fraction is a NaN (mostly *signaling*) where hardware gives ±Inf; and the "special case for 0.0" line, which 0.0 never reaches, flushed underflow to zero **discarding the sign** | test the biased exponent for all-ones and keep only the sign before OR-ing the exponent in; flush underflow to a *signed* zero |

### The finding that changed the fix

The brief opening this round — and `OUTSTANDING_BUGS.md` item 8, in the same words — located the
defect at the clamp (`:367-368`) and said it "first fires at |x| ≥ 2^128". **Both are wrong.** The
clamp tests `>= (1 << n_exp)` = 256 and first fires at **2^129**; for `|x|` in `[2^128, 2^129)`
the biased exponent arrives at **255 with no clamp at all** and is written straight over the
fraction. A fix scoped to the clamp branch — the literal reading of the proposal — would have
shipped still-broken across that entire binade, passing a probe built from `1e300` while failing
on `3.5e38`, which the brief itself printed as a headline defect.

**Four of five seats caught this independently** (9,740 survivors over a 20M sweep; 20,000/20,000
in that octave; `4e38 → 0x7f967699`), and the live probe confirmed three first-binade rows
NaN-encoded with exponent field 255. This is the same class of boundary trap as round 49's
`:1126` set-then-compare. `3.5e38` is therefore mandatory in the acceptance suite.

### Why rounding was left alone (the Option-B rejection)

A host `(float)`-cast rewrite would have collapsed three defects at once and was seriously
proposed by one seat. It was rejected on a fact from the tree itself: `cpu_sh.c:116` sets
`fpscr = 0x00040001` and `cpu_sh.h:199` defines `SH_FPSCR_RM_ZERO 0x1`, so **SH-4 resets to
round-to-zero** — truncation is architecturally *correct* there by default, and a
round-to-nearest cast would regress it on a measured 41% of its S stores across 16 sites.
PowerPC's `stfs` truncates by architecture as well. The four S-storing families do not share a
rounding mode and the shared helper has no parameter to carry one. The #254 precedent argues the
other way: #254 was MIPS-**local**. Rounding remains a documented gap owned by a future
`FCSR.RM`-aware change, which also owns the residual `[2^128 − 2^103, 2^128)` sliver.

### Gate methodology — the usual smoke was the wrong instrument

The #279 20-machine smoke executes a zero blob under `-V` and quits **without a single FP store**,
so it is vacuous for this change: it would pass whether the fix were right, wrong or absent. Since
the function is pure, the gate is an offline differential with a **closed form for the
change-set**, so that a regression is definitionally a difference outside it:

```
old(x) != new(x)  =>  (finite && |x| >= 2^128) || (0 < |x| < 2^-126 && signbit(x))
```

20,016,002 samples → 13,133,666 S differences, partitioning exactly into 8,756,599 overflow and
4,377,067 negative underflow; **0 unexplained, 0 in-range, 0 D-format**. The empty D change-set is
the *proof* that alpha (D-only) and every D store on m88k/ppc/sh are untouched — stronger than any
boot run, and it makes the real blast radius four families, not five.

### A stale reading, investigated instead of accepted

The first POST run gave `-1e-40 → 0xff800000` on arc against `0x80000000` on pmax. The fix cannot
produce −Inf there, so it was re-run with `$f2` seeded to a known value: arc returned **the seed
unchanged plus two `exception FPE … cause=0x1000003c` lines**, proving the instruction trapped via
#246 and that `fp_op`'s unconditional `swc1 $f2` had stored the neighbouring case's value. Not a
regression. **Keep the rule:** after a trapped FP instruction neither the sentinel nor an adjacent
row's value may be read as a result — seed a distinctive value first. D3 is observable on **pmax
only**; arc's identical input is a control proving #246 still gates.

### Reachability

**Reachable from stock userland on crafted input; not exercised by the boot workload.** Verified
against the OpenBSD 2.2 sources: `lib/libc/stdio/vfscanf.c:651` is
`*va_arg(ap, float *) = res;`, so a plain `%f` narrows a parsed double to `float` (`cvt.s.d` on
MIPS), and `gnu/usr.bin/texinfo/makeinfo/multi.c` declares `float columnfrac;` (`:152`) and parses
user-controlled `@columnfractions` through `sscanf (params, "%f", &columnfrac)` (`:177`). Four
seats called it latent; one found this route and it checks out. Stronger than #283/#286's latency,
weaker than boot-visible — state it that way.

### Documented, not fixed

* **D2 — the fraction loop truncates instead of rounding to nearest-even.** S-only (the D loop
  extracts all 52 bits exactly). Measured 41% of inexact S stores differ from round-to-nearest.
  Belongs to the future `FCSR.RM`-aware change, together with the `[2^128 − 2^103, 2^128)` sliver
  where round-to-nearest hardware gives Inf and this code gives FLT_MAX.
* **D4 — no gradual-underflow generation.** The empty `FP_SUBNORMAL` arm returns a signed zero,
  which is correct flush-to-zero behaviour for MIPS (`FCSR.FS`) and reset-state SH-4
  (`FPSCR.DN`), so it is a D-format gap rather than an S defect. Naming it here so a future seat
  does not "fix" code that is already right by default.

### Panel

Five seats (Codex 5.6-SOL ultra, Fable 5, Opus 5, agy 3.6, Kimi 3 MAX), **4–1**. The dissent
argued the host-cast rewrite; the four points above answer it. Two contributions were decisive and
came from single seats: the binade correction (found by four, but it inverted the fix) and the
stock-userland reachability route (found by one, verified from source here).

---


## Fifty-second round (#288) — the keyboard ring that read as empty, and the drain loop with no guard

| # | file | Problem | Fix |
|---|---|---|---|
| 288 | `devices/dev_pckbc.c` | (a) `pckbc_add_code()` advanced `head` before testing for collision, so an overrun left `head == tail` — which every reader treats as EMPTY, discarding the **whole queue** rather than the one code that did not fit. (b) `DEVICE_TICK(pckbc)`'s drain loop had **no space guard**, and `console_charavail()` refills from the host inside it, so an unbounded producer starved the guest indefinitely | (a) compute the next head first; on a full ring drop the **incoming** code, warn once per port. (b) add a room guard whose reserve exceeds the longest scancode sequence, as `lk201_tick()` and `dev_luna88k.c` already have |

### The finding that changed the fix

Three of five seats proposed the ring fix alone. That is correct but incomplete, and shipping it
alone would have made the system **worse observationally**: the starvation would have remained
while the new one-shot latch removed the only evidence it was happening. One seat identified the
missing drain guard and measured it; the A/B below confirms it.

| rig | control | unbounded producer |
|---|---|---|
| arc, before | 4 `OpenBSD` lines | **0 lines**, 10,806 overruns |
| arc, after | 4 lines | **4 lines**, 0 overruns |
| pmax (drain loop already guarded) | 1 line | 1 line, 0 overruns |

Identical stimulus through the identical console layer; only the guard differs. `dev_pckbc.c`
was the **only** console drain loop in the tree without one.

### Reachability — and the methodological error that hid it

The brief opening this round asserted the pckbc path "requires a graphical run; the rigs are
headless." **False, and it was the one site the brief was most confident about.**
`machine_arc.c:139-141` forces `fb_console = 1` on PICA unconditionally, making pckbc the arc
rig's `main_console_handle` and its stdin consumer — the fork's own comment at `:136` says so.
The defect reproduces 4 times on a 44 KB paste and 10,806 times under an unbounded producer.

The error underneath it: **"0 occurrences on both healthy boot logs" was allowed to stand in for
a reachability argument.** The harness types ~50 characters into a 32,767-slot ring; that control
cannot speak to reachability at all. Same lesson as #262's dead-on-healthy-boot branch. A seat
that argued document-only rested its pckbc case on exactly this and was refuted by measurement.

### What is NOT claimed

The **ring half has not been observed firing.** The drain guard prevents the queue from filling,
so the drop-and-latch path is unreached (0 overruns post-fix, not 1). Both measurements prove the
guard. The ring change stands as the correctness invariant — `head == tail` must never mean
"full" — and as defence in depth for the guest-authored controller-response producers that
bypass the tick.

### A seat that refuted its own prediction

One seat predicted the whole-queue discard would strand a shift make-code and latch a modifier
in the guest, ran it (400,000 × `A`, 73 discards all landing inside shift make/break pairs), and
found login behaviour **identical to the control** — the shift state is self-healing, since the
next complete sequence delivers a fresh release. It reported the refutation rather than dropping
it. Recorded because the same seat had an unmeasured remedy refuted by fault injection two rounds
earlier, and this is the corrected practice.

### Quantitative discriminator, for reuse

The pre-fix code warns once per **lap**, which turns the warning count into an independent
measure of amplification: `overruns = floor(k·N / 32768)`. Verified at two amplification factors
and four input sizes, exact to the integer (`a`, k=3: 100K→9, 200K→18, 400K→36; `A`, k=6:
400K→73). Single-byte-drop would predict `k·N − 32767` — a 100K:200K ratio of 8.4 against the
2.0 measured. That is how the two failure modes were distinguished by measurement rather than
by inspection.

### Documented, not fixed

* **`console/console.c:304`** — the `:364` throttle bounds the stdin producer exactly (the `+1`
  is load-bearing). 0 overruns measured under both the flood and an unbounded producer. But two
  seats found bypassing producers: the debugger's CTRL-K inserts **72** characters, and
  `dev_ns16550.c:163` feeds `console_makeavail()` directly under `MCR_LOOPBACK`, which is
  **guest-authored**. **Named experiment before this arch-shared file is touched:** drive
  `com_mcr` loopback from an arc guest, issue several thousand transmit writes into an undrained
  handle, grep for `console fifo overrun`.
* **`devices/dev_dc7085.c:103`** — unreachable and the reference implementation: `lk201_tick()`
  re-tests `space_available_in_queue()` every iteration; `:80` reserves 20 entries; occupancy
  parks at ~1004 of 1023.
* **`devices/dev_scc.c:140`** — same shape, 1 char/tick, non-rig machines.

### A design smell recorded, not changed

`console_charavail()` is a **mutator named as a query**: it performs `select()` and a 100-byte
`read()` as a side effect, and is called from ordinary guest status-register reads
(`dev_ns16550.c:84,135`, `dev_ssc.c`, `dev_clmpcc.c`, `dev_sh4.c`, `dev_cons.c`). A saturated
stdin therefore adds host syscall cost to plain MMIO reads. Arch-shared, no reproduction of
harm — documented so it is not rediscovered.

### Harness consequence of this fix

The arc console's stdin is now genuinely flow-controlled. A harness writing a large blob **inline
while draining the same pty deadlocks** — writer waits on the emulator, emulator waits on the
reader. Correct back pressure, identical to pmax's long-standing behaviour, but this project's
own flood test had to be restructured to write from a background thread. Run such probes with
`python3 -u`; the first post-fix attempt block-buffered into a pipe and `timeout` discarded every
line, producing a silent empty result indistinguishable from a crash.

### Panel

Five seats (Codex 5.6-SOL ultra, Fable 5, Opus 5, agy 3.6, Kimi 3 MAX). Four for a fix, one for
document-only. The decisive contribution — the missing drain guard, which changed what shipped —
came from a single seat and was confirmed by an independent A/B. One seat's proposed diff
transposed the `pckbc_add_code(d, code, port)` parameters; copying it verbatim would have swapped
scancode and port at every call site.

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


## Build note: `-fgnu89-inline`
On modern glibc/gcc the link fails with `multiple definition of __cmsg_nxthdr /
recv / recvfrom / inet_ntop / inet_pton` — glibc's `extern inline` socket wrappers
emit an external definition in every TU. `configure` now auto-adds `-fgnu89-inline`,
which restores the GNU89 inline semantics this code was written for. Details in
`build/BUILD_NOTES.md`.

### Cross-reference: the Debian fork hit the same wall (root cause)
`github.com/threader/gxemul` (Debian packaging of 0.7.0) carries
`debian/patches/remove_defines`, whose changelog note is verbatim our symptom:
*"Building … fails with duplicate definitions from bits/socket.h being 'extern
inlined' twice."* Their **root-cause** fix removes the
`#define __attribute__(x) /* */` neutering from four thirdparty headers
(`bootblock.h`, `dp83932reg.h`, `pcireg.h`, `sgi_arcbios.h`). Those `#define`s
strip glibc's `__attribute__((__gnu_inline__))` — exactly what causes the multiple
definitions.

That neutering ALSO silently discards **37 real `__attribute__((…))`** uses in
those headers — overwhelmingly `packed` on hardware/disk-layout structs (14 in
`bootblock.h` alone). So the macro hides a latent correctness concern, not just a
build break.

**Resolution (applied):** we adopted the Debian `remove_defines` root-cause fix
(correction #11) — the four headers no longer neuter `__attribute__`. Re-verified:
the build stays clean (**0 warnings**, no `-Waddress-of-packed-member`) and the
binary is byte-size-identical, i.e. restoring `packed` changed no struct layout on
this codebase, so it is behaviorally safe here. `-fgnu89-inline` is **kept as a
belt-and-suspenders** safety net (the root cause is now also gone, so a plain
build no longer depends on it).

> Scope: framework + loaders + a `-fanalyzer` sweep of all TUs. Not an exhaustive
> per-device behavioral audit — a fuzzing campaign on `src/file/*.c`, `src/net/`,
> and the device register handlers remains the recommended next step.
