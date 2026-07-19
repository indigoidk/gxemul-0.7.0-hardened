# GXemul 0.7.0 — Code Examination, Corrections & Security Findings

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
| 3 | `core/emul.c` | **Shell command injection**: `system("mv %s …")` / `system("gunzip … %s")` with unquoted, attacker-influenceable file names | Replaced with a `fork()`+`execlp("gunzip",…)`+`dup2()` helper — never invokes a shell |
| 4 | `core/emul.c` | `snprintf` truncation warning (`tmpstr[20]`) | `tmpstr[32]` |
| 5 | `promemul/arcbios.c` | `malloc(0)` (`-Walloc-size`) | `NULL` (the following `realloc(NULL,…)` behaves like `malloc`) |
| 6 | `file/file_srec.c` | **Uninitialized stack leak**: `bytes[270]` never cleared; attacker-controlled `count` makes the type switch read past the parsed data into the load address / emulated RAM. Also `count-1-data_start` could go negative → huge `size_t` length | `memset(bytes,0,…)` per record + guard the write length `> 0` |
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
(correction #14) — an attacker-controlled `str_index` indexing past the string
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

**Tooling note (checkers):** `agy`/Gemini 3.1 Pro **refused** the CPU chunk under a "vulnerability
analysis" framing (needed reframing as plain correctness QA), emits findings only to its transcript
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
  → a local attacker could pre-plant a symlink at the guessable path in the close→reopen window (TOCTOU).
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
security bounds (untrusted ROMs cannot be validated, so security stays regardless of upstream intent), add
*just-enough* rate-limited verbosity in the author's style, and above all NEVER crash. Approach + each item
were passed through Codex (gpt-5.5/xhigh) + agy (Gemini 3.1 Pro); the user chose "keep both behavior
refinements." **No security bound was removed.**
- **#118 `dev_osiop.c` (real host crash):** `read_word`/`read_byte`/`write_byte` dereferenced
  `memory_paddr_to_hostaddr()` with no NULL check (it returns NULL on a read miss) — a guest pointing the
  SCSI SCRIPTS engine at unmapped RAM crashed the host. Added a NULL guard + `osiop_hostpage_fault()`
  (warn-once `fatal()` + stop the local script via `scripts_running=0`; an early-return in
  `osiop_execute_scripts_instr` keeps the bogus fetch from reaching a `TODO; exit(1)`). No deref, no exit.
- **#101 `dev_scc.c` (refined):** the prior `% N_SCC_PORTS` was host-safe but ALIASED out-of-range offsets
  onto a valid port (wrong hardware). Now bounds-check + **NO-OP** out-of-range (read returns 0) + warn-once
  — same security (no OOB into `scc_register_r[]`), no aliasing. (The author's SGI `0xf` remap is left
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
real bugs *in our course-correction edits* that no build/boot test surfaces (they need a malicious guest):
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
A full-tree security pass by **Codex CLI `gpt-5.6-sol`/ultra** (report `../harness/codex_sol_ultra_to_fable.md`):
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
correct ExcCode/CE/BadVAddr/EPC/BD. Document-only: R3000 BEV=1 vector base (off exploit window); `mtc0`-writable
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
