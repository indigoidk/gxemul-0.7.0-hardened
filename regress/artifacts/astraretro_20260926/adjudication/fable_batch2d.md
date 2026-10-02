VERDICT: 15 confirmed-new, 3 confirmed-filed, 6 record-L4, 4 test-gap, 0 refuted, 0 unsettled, 0 duplicate, of 28 findings

FABLE_RETRO_2d_ALIVE_0926

CHECKPOINT.md first line, verbatim:
`# CHECKPOINT -- 2026-09-30 11:55 RUNNING AGAIN (owner: grok freely, skip Ollama, Fable adjudicates, Astra confirms); loop cron d1e654c4 (13,43); codex re-run cron 14:27`

ASTRA RETRO-REVIEW -- FABLE ADJUDICATION, batch 2d.  Adjudicated at `8ea26abb` (HEAD is `db8b1a33`; the
two differ only in records files, `git diff --stat 8ea26abb db8b1a33 -- src/` is empty).  Every source, regress
and CHANGELOG citation below is at `8ea26abb`; `OUTSTANDING_BUGS.md` citations say which commit they were read
at (the 62 lines `db8b1a33` adds shift its later entries).  Read only: `git show 8ea26abb:<path>` piped through
`awk '{print NR": "$0}'`; no build, no run, no edit but this file.  Model: claude-fable-5-1, first-hand.

The draft (`codexpack_20260928/draft_2d/codex_draft_2d.txt`) was read AFTER my own reading of each finding
and compared at the end.  THREE of its 28 dispositions are changed: devices1:F3 (DOUBTFUL -> CONFIRMED-NEW
HIGH, narrowed to the ARM subpage path it did not chase), devices3:F3 (FILED OB-28 -> CONFIRMED-NEW LOW: OB-28
is a RESOLVED row, and a closed row is not a filing), devices3:F7 (DOUBTFUL -> CONFIRMED-NEW MED: the file's own
register table is the local evidence).  Two are kept in category but their replacement texts are rewritten
(devices1:F6, devices2:F2), one gains an L4 correction the draft named but did not dispose (devices3:F9), and one
is broadened beyond ARM (devices4:F2).  Details in the last section.

Severity scale as the brief defines it: HIGH = a guest can end the process, read/write outside a buffer, or
hang it; MED = guest-visible behaviour contrary to the documentation; LOW = diagnostics, latent code, test gaps.

======================================================================================================
bundle_devices1  (8 findings: 5 new, 0 filed, 2 record, 1 test-gap)
======================================================================================================

bundle_devices1:F1 | CONFIRMED-NEW HIGH mboutcapacity "MB89352: the WRITE path re-sizes data_out_len without reallocating, and DREG writes bound on that length"
Checked: `src/devices/dev_mb89352.c:225-226` (PH_DATAOUT takes `p = data_out`, `len = data_out_len`), `:239-246`
(the only bound is `transfer_bufpos >= len`, then `p[transfer_bufpos++] = idata`), `:268-272` and `:276-280`
(PH_CMD honours `res == 2` by entering PH_DATAOUT with NO allocation), `:476-477,:495` (the only data_out
allocation is the XFR-DATAOUT arm), `:637-650` (DREG is gated only on `transfer_count > 0`, guest-set via
TCH/TCM/TCL at `:658-665`); `src/disk/diskimage_scsicmd.c:888-892` (`data_out_len = size; return 2` with no
realloc), `:89` (`scsi_transfer_alloc()` zeroes the struct, so `data_out == NULL`, `data_out_offset == 0`).  Two
guest sequences, both through ordinary MMIO: (i) SELECT, XFR CMD, write a WRITE(6) CDB for one block -> the disk
layer sets `data_out_len = 512` and returns 2, PH_CMD sets phase = PH_DATAOUT, `data_out` is still NULL and
`transfer_bufpos` is still the CDB length; set TCL and write DREG -> `p[6] = idata` through a NULL `p`.
(ii) XFR DATAOUT with a small `transfer_count` first (a 16-byte allocation), then the CDB: the same return-2 path
leaves the 16-byte block under `data_out_len = 512`, and DREG writes run `p[16..511]` past the heap block.
Not filed: `mb89352halt` (OB@db8b1a33:11414-11434) is the missing-status halt; OB@db8b1a33:21199-21203 is the
transfer_count width bound, "a bound, not an overflow", explicitly not this.

bundle_devices1:F2 | CONFIRMED-NEW LOW mbcdbincomplete "MB89352 dispatches a CDB whose uncollected bytes are uninitialised heap"
Checked: `dev_mb89352.c:500-501` (`scsi_transfer_allocbuf(&cmd_len, &cmd, transfer_count, 0)` -- clearflag 0,
`diskimage_scsicmd.c:158-159` memsets only when set), `:409-429` (a second XFR replaces the phase from PCTL with
no `transfer_bufpos == cmd_len` predicate), `:259-269` (DATAOUT fill dispatches whatever `cmd[]` holds);
`diskimage_scsicmd.c:298-316` (the #113 check tests `cmd_len`, which is the ALLOCATED length, not the bytes
received), `:1380-1383` (an unknown opcode is `debug()` only, the `exit(1)` is commented out, so garbage in
`cmd[0]` cannot end the process).  Consequence: a command parameterised by malloc residue -- for a WRITE, an LBA the
guest never wrote, bounded by `diskimage__internal_access()`.  LOW because the guest must abandon its own CDB
mid-phase and the harm needs the residue to decode as a write; no driver does this.  A real MB89352 target would
not leave COMMAND phase early, so a MED reading is arguable; I grade by consequence.

bundle_devices1:F3 | CONFIRMED-NEW HIGH vgadirtyarm "VGA: an untracked charcells write below the CRTC start leaves a ~-1.7e9 dirty-row origin unclipped, and the graphics redraw walks it"
Checked: `src/devices/dev_vga.c:738-744` (`r = relative_addr - base` is int; `y2 = (r+len-1) / (d->max_x*2)`
promotes to size_t: for r = -2, len = 1 that is (2^64-2)/160 = 0x0199999999999999, truncated to int y2 =
0x99999999 = -1717986919), `:760,:764` (`update_y1 = min(y, y2)` takes that value), `:545-558` (the clip to
[0, max_y-1] runs ONLY inside `if (low != -1)`), `:587-593` (graphics mode calls `vga_update_graphics(0, y1, 79,
0)` on it), `:352-356` (`for (y=y1; y<=y2; y++) for (x..)` with `int addr = (y*max_x + x)*bpp` -- signed overflow
for |y| > 2^31/max_x, then #98's bound keeps the READS in range).  Whether the write is tracked:
`src/cpus/memory_rw.c:526-547` records `dyntrans_write_low/high` for a slow-path write ONLY when
`!(ok & MEMORY_NOT_FULL_PAGE)`; both `memory_rw.c` setters (`:339`, `:426`) are under `#if 0`, and the ONE live
producer is `src/cpus/memory_arm.c:235` (`subpage`: a 1 KB tiny page at `:198-207` on non-XScale, or a small page
whose four AP fields differ at `:227-228`).  `dev_vga.c:1314-1317` registers the charcells page-rounded
(`:1285`), so on MIPS/PPC every DEVICE_ACCESS write is also a tracked write and the clip runs -- the draft's
refutation of the general "slow path" premise is right.  An ARM guest that maps the VGA text window with such a
descriptor gets EVERY write untracked, and the one ARM machine with a VGA is cats: `src/machines/machine_cats.c:82`
adds `s3_virge` unconditionally, `bus_pci.c:444` calls `dev_vga_init()`.  So: cats (SA-110, tiny pages are the
`case 3` arm), graphics mode set, one byte written to the charcells window below the CRTC start -> the next tick's
redraw loops on the order of 1.7e9 x max_x iterations (bounded memory, hours of wall clock), and the guest can
re-arm it every tick.  HIGH on the brief's scale (a guest can hang it) with the precondition stated; a bounded
stall, not an infinite loop, and UNMEASURED -- the witness is a cats guest with a tiny-page mapping.  Astra's
mechanism wording ("oversized rectangle ... unsigned arithmetic") is right in substance; the axis that grows is
`update_y1` going negative, not `update_y2` growing.  Text mode is bounded (`vga_update_text():413-430` clamps
`end` to `charcells_size` and returns on `start > end`).  Not filed: OB@db8b1a33:2472 is the differential-repaint
note, unrelated.

bundle_devices1:F4 | CONFIRMED-NEW LOW gberesizezero "GBE keeps a rejected VCMAP/HCMAP dimension in xres/yres and reads it back through negative shifts"
Checked: `src/devices/dev_sgi_gbe.c:542-543,:551-552` (`d->xres`/`d->yres` stored BEFORE the void
`dev_fb_resize()`), `src/devices/dev_fb.c:134-141` (#184 returns for `< 10`, framebuffer untouched), `:495`
(`((d->yres-1) << 12)` = `(-1) << 12`, undefined), `:536` (`d->yres-1` = -1 read back as 0xffffffff).  The tick is
safe: `:242` `screensize = xres*yres*3` = 0 -> `:269-277` breaks before any copy, and a rejected dimension is
always < 10 <= the old one, so the computed size never exceeds the live buffer.  LOW: UB on two read-back
registers the guest asked for by writing 0, no memory consequence.  Not filed: OB@db8b1a33:2395-2407 is the VGA
mode switch's resize, `sgigbeconvover` is the conversion tail.

bundle_devices1:F5 | CONFIRMED-NEW LOW vgacursoronly "VGA headless console: the OB-16 guard returns before the cursor-only tick can reposition the terminal cursor"
Checked: `dev_vga.c:581-584` (the tick calls `vga_update_textmode(m, d, 0, 2, 0)` -- base 0, start 2, end 0 --
with upstream's own comment "2 > 0, so this only updates the cursor"), `:268-269` (`/* OB-16 */ if (... end <
start) return;` -- the fork's #82 guard, CHANGELOG.md:21721 maps OB-16 to #82), `:334-335` (the cursor restore
sits AFTER the loop and is never reached on that call), `:818-821` (cursor register writes only recalculate the
position, `modified` stays 0), `:503-524` (`vga_update_cursor()` drives the X11 framebuffer cursor, not the
terminal).  So a cursor move with no cell change in the same tick leaves the host terminal's cursor stale until the
next cell write.  A fork regression in host rendering only; LOW.

bundle_devices1:F6 | RECORD-L4 "/*  #295: zero the buffer (clearflag 1).  [HISTORICAL as of #338: the 'declares it FULL' and 'DEFERRED on purpose' sentences below describe the code #295 found.  #338 (the comment after the allocbuf call) starts data_out_offset at 0 and publishes transfer_bufpos at fill, and the PH_CMD arm of mb89352_dreg_write() honours the disk layer's return of 2 by entering PH_DATAOUT.  The PH_DATAOUT arm still discards that return -- see 'TODO: How about failure results?' there.]"
Checked: `dev_mb89352.c:438-441` ("The line below declares it FULL -- data_out_offset = transfer_count") against
`:495` (`data_out_offset = 0`); `:463-472` ("the honest repair (offset 0, advanced as bytes arrive) is DEFERRED on
purpose") against `:266` (`data_out_offset = transfer_bufpos`) and `:279-280` (`if (res == 2) phase =
PH_DATAOUT`); `:271-272` (the PH_DATAOUT arm still discards `res`).  The replacement is the text to put in place
of line 438's opening sentence; the rest of the #295 block is kept because its #263 measurement is the history.  I
did not adopt the draft's whole-block rewrite: it drops that history.  The discarded return at `:271` is the
`mb89352halt` shape (a short DATAOUT leaves no status buffer), already filed.

bundle_devices1:F7 | RECORD-L4 "#  *** THE ANCHOR IS THE LOAD-BEARING HALF; `set -f` IS A SAFEGUARD, NOT A\n#  SUBSTITUTE.  Anchoring is what removes the prose words; `set -f` alone would\n#  leave all 14 of them and merely change the failure from a parse error to an\n#  undefined symbol.  With the anchor in place, dropping `set -f` is MEASURED to\n#  change nothing (regress/diff_autodev_gen.sh mutant 3, recorded not asserted);\n#  it is kept because a scraped name that ever carried a glob character would\n#  otherwise expand. ***"
Checked: `src/devices/makeautodev.sh:72-74` ("BOTH HALVES ARE LOAD-BEARING, they are not alternatives") -- the
supporting sentence establishes only that `set -f` is not a substitute; `regress/diff_autodev_gen.sh:202-209`
(mutant 3, anchor kept / noglob dropped, "measured: ... dropping noglob changes nothing -- noglob is belt, not
braces"); CHANGELOG.md:27938-27940 records that mutant as surviving.  The headline is false of the measurement the
same round shipped; the replacement is for lines 72-74 (seven comment lines, `\n` marks the breaks).

bundle_devices1:F8 | TEST-GAP-FILE autodevregorder
Checked: `regress/diff_autodev_gen.sh:63-64` (`names_of`/`pcinames_of` match the PROTOTYPE lines only), `:88-106`
(the load-bearing ordered rows compare those), `:146-152` (the planted comparison is `cmp` of the same generator's
output on two trees).  `makeautodev.sh:114-125` and `:128-139` are the registration loops -- a separate scrape,
observed by no row: a mutant confined to loop 2 (a dropped, reordered or mis-paired `device_register()`) passes.
CHANGELOG.md:27935 ("Order is asserted alongside the set because `device_register()` order is the order devices
are offered") states the property in terms of registration while the row pins prototypes.  LOW; the shipped
mutants edit all four loops, so the shipped defect class IS caught.

======================================================================================================
bundle_devices2  (6 findings: 1 new, 0 filed, 3 record, 2 test-gap)
======================================================================================================

bundle_devices2:F1 | CONFIRMED-NEW LOW lunaintshift "luna88k: signed 1 << 31 in the INT_ST_MASK read loop and the line-6 assert/deassert, and highestCurrentStatus << 29 for levels 4-6"
Checked: `src/devices/dev_luna88k.c:876` (`int m = 1 << (25 + i)`, i = 6 -> `1 << 31`), `:881` (`highestCurrentStatus
<< 29` in int, 4..6 -> 2^31..3*2^29, undefined), `:209` and `:216` (`1 << (interrupt->line + 25)`, line 6 ->
`1 << 31`), `:1008-1013` (lines 1..6 registered), `:1025-1027` (line 6 is the TIMER, so `:209` runs on every
tick).  On gcc/two's complement the values are the intended masks and `odata` is a uint64_t whose low 32 bits are
what a 4-byte read returns, so no guest-visible effect; C99-undefined and exercised, not latent.  LOW.
`shiftubcensus` (OB@db8b1a33:16920-16937) is a census with "the remaining shifts are not settled"; it files no
site, so this is NEW, and a records round may fold it with kn02banameshift and macesignedshift under that census.

bundle_devices2:F2 | RECORD-L4 "Bounded with a room guard whose reserve exceeds the longest scancode sequence, so an admitted character always fits whole and a make cannot be queued with its break dropped.  The guard bounds the drain only through queue room: a host character that none of the three converters maps to a scancode (`ascii_to_pc_scancodes_type1/2/3` enqueue nothing for it) consumes no room, so a host producer that never stops and sends only such bytes still keeps `console_charavail()` true and the tick in its loop.  That residual needs a host-side producer, not a guest, and is recorded here rather than claimed fixed."
Checked: CHANGELOG.md:20762-20768 ("the tick never returned to the guest. Fixed with a room guard ...");
`src/devices/dev_pckbc.c:664-680` (`while (pckbc_room_left(d,0) > 8 && console_charavail(...))`, the body's only
progress is what the converter enqueues); `:329-336`, `:454-469`, `:587-602` (all THREE converters -- Astra said
2/3; type 1 behaves the same -- add nothing when no `if (a==...)` matched and shift/ctrl are 0, e.g. any byte >=
0x80); `src/console/console.c:355-403` (`console_charavail()` refills from the host descriptor inside the loop).
The replacement is for the sentence at CHANGELOG.md:20766-20768.  Host-driven only (`yes $'\x80' | gxemul`), so
no code row is owed; the residual is written into the record so it is not lost.

bundle_devices2:F3 | RECORD-L4 "    Governs THIS FILE ONLY.  The header's SYSASIC_EVENT_TO_ADDR(e)\n    (dreamcast_sysasicvar.h) once reached the same fourth-word offsets\n    from the other side: 4*((e)>>5) lands on an r == 3 offset exactly\n    when (e>>5) & 3 == 3 (e in [96,127] -> +0x0c, and so on).  Since\n    #468/#469 the macro carries SYSASIC_EVENT_RANGE_OK(e), a compile-time\n    assertion that (e) is a constant in [0,95], so only quotients 0, 1\n    and 2 (+0x00, +0x04, +0x08) can be produced and an out-of-domain or\n    non-constant event fails to COMPILE.  The `asiceventaddr` id now\n    tracks the unguarded SYSASIC_EVENT_TO_BITMASK sibling on the next\n    header line, not this closed address hazard.  */"
Checked: `src/devices/dev_dreamcast_asic.c:182-191` ("reaches a fourth word via a header #define no comment here can
reach ... LATENT, not live.  Filed as `asiceventaddr`"); `src/include/thirdparty/dreamcast_sysasicvar.h:135-140`
(`SYSASIC_EVENT_RANGE_OK` is a bitfield-width assertion on `(e) >= 0 && (e) < 96`, added to `SYSASIC_EVENT_TO_ADDR`);
OB@8ea26abb:21528-21534 (the `asiceventaddr` id now names the BITMASK `1 << ((e) & 31)` sibling).  The comment is
false of the header at HEAD.  The replacement is for lines 182-191.  OB@8ea26abb:11363-11365 repeats the old
fourth-word statement inside a dated round residual list; it is history and I leave it.

bundle_devices2:F4 | RECORD-L4 "A **compensating pair, for the rows the harness drives**: with a post-1900 host clock every value `rs5c313_update_time()` stores is already below 16, so dropping the read-side `& 0x0f` alone changes no guest-visible row and only the pair is detectable — catching it needs a row that reads `d->reg[]` directly rather than through the device.  The read-side mask is NOT dead code in general: `rs5c313_update_time()` (`dev_rs5c313.c:86`) writes `tm_year % 10` into `YEAR1` on every access before any guest-write mask is consulted, and this file's own note records a pre-1900 host clock yielding `0xfa` there; the read mask returns `0x0a` for it and its removal would return `0xfa` through the SCI byte path (`dev_sh4.c:884-890`)."
Checked: CHANGELOG.md:28088-28091 ("dropping the read-side `& 0x0f` is dead code because the write side already
masks"); `src/devices/dev_rs5c313.c:152` (`rs5c313_update_time(d)` runs before every access), `:86`
(`reg[YEAR1] = tmp->tm_year % 10`, unmasked, negative for a pre-1900 `tm_year`), `:133-134` (the file records
"YEAR1 = 0xfa" measured), `:157` (write mask), `:159` (read mask); `src/devices/dev_sh4.c:884-890` (SCI reads the
device byte through `memory_rw` and stores it whole).  The replacement is for the sentence at 28088-28091.

bundle_devices2:F5 | TEST-GAP-FILE lunad3diag
Checked: CHANGELOG.md:25513 ("D3 proves bits 7..0 are unobservable and kills a narrowed guard");
`regress/luna_intmask_probe.py:224-231` (D3 writes 0xc4000041, bails only if the host DIED, then checks the
readback 0x00c40000), `:263-266` (E2 counts "reported once" markers = 2, i.e. D1's first hit on MASK0 and D4's on
MASK1; D3 is MASK0's third hit and prints through `debug()` at `dev_luna88k.c:861-863`, never counted);
`regress/gate_m88k_rounding.sh:308-313` (the gate names D2 and D4, not D3).  Under a guard whose mask is narrowed
to `0x03ffff00` (the natural "narrowed guard"), D3's survival, readback and E2 are all unchanged, so the row does
not kill it.  The sentence is TRUE for the mutant the probe's own bail text names -- a de-fatalisation that still
exits for bits 7..0 -- so it is ambiguous rather than false and I do not rule L4 on it; the gap is that no row
observes D3's own diagnostic.  LOW.

bundle_devices2:F6 | TEST-GAP-FILE fdcdiagrows
Checked: CHANGELOG.md:20522 ("Offset 0x04 must stay silent, and that is asserted rather than assumed ... The probe
hammers 0x04 ... 0 lines in both") and :20519 (1/2/4-byte tokens); `src/devices/dev_fdc.c:67-69` (`case 0x04:
break;`), `:100-105` (tokens); `git grep -il fdc 8ea26abb -- regress/` returns only `regress/artifacts/*` (panel
transcripts and kill tables), no probe, and `regress/gate_hygiene.sh` has no fdc line.  The measurement was
round-time only; nothing at HEAD observes either claim.  LOW.  The CHANGELOG describes a measurement, not a
committed detector, so no L4.

======================================================================================================
bundle_devices3  (10 findings: 7 new, 2 filed, 0 record, 1 test-gap)
======================================================================================================

bundle_devices3:F1 | CONFIRMED-NEW LOW pxdmatail "PX COPYSPANS decodes span records past the bytes the bounded SRAM copy filled"
Checked: `src/devices/dev_px.c:140` (`unsigned char dma_buf[32768]`, never initialised), `:155` (the first copy
is 224 bytes), `:255,:262-263` (`nspans` <= 255, so `dma_len` <= 3080, inside `dma_buf`), `:273-277` (#207 copies
`min(dma_len, sl)`), `:282-311` (the decoder walks all `nspans` records regardless), `:317-318,:323` (span
length capped at PX_XSIZE and rows bounded before the `memmove`).  So the uncopied tail is decoded from stale stack
into BOUNDED framebuffer row copies: nondeterministic pixels, no out-of-bounds access.  LOW.  The caller's
`sys_addr` is 2 KB-aligned (`:600-601`), so the 224-byte first read fits, as Astra's clean item says.  Not filed:
OB@db8b1a33:2703/2885 are the OB-3/#207 bounds, not the tail.

bundle_devices3:F2 | CONFIRMED-NEW HIGH dectxzero "DEC21143: an empty continuation of an empty first segment calls realloc(p, 0), which glibc answers with NULL, and CHECK_ALLOCATION ends the process"
Checked: `src/devices/dev_dec21143.c:772-774` (first segment: `malloc(bufsize == 0 ? 1 : bufsize)`, then
`cur_tx_buf_len = 0`), `:784-789` (continuation: `realloc(d->cur_tx_buf, d->cur_tx_buf_len + bufsize)` with no
zero guard -- `0 + 0` after an FS descriptor of size 0 followed by a middle descriptor of size 0), `:802` (the
length is added only after the call); `src/include/misc.h:190-193` -> `:181-188` (`CHECK_ALLOCATION` ->
`FAILURE` -> `exit(1)`).  glibc frees the block and returns NULL for `realloc(p, 0)`, and the build/rig platform
is WSL Gentoo glibc, so the qualification is "glibc-dependent" not "hypothetical".  Two descriptors with size
fields of 0 are within a guest driver's reach.  HIGH.  Not filed: OB@db8b1a33:2904 (OB-17) is unbounded growth,
`dec21143deadclamp` (OB@db8b1a33:16839-16858) is dead size guards.

bundle_devices3:F3 | CONFIRMED-NEW LOW gifputcharovf "ps2_gif putchar: (24 + y*xsize)*4 overflows int before #108's bound; residual of the RESOLVED OB-28"
Checked: `src/devices/dev_ps2_gif.c:232-234` (xsize <= 65535, ysize <= 65520), `:271` (`int addr = (24 +
y*xsize) * 4`, y*xsize up to 4,293,787,665 -- signed overflow), `:273-274` (`addr < 0 || (size_t)addr + 3 > len`
breaks the INNER loop only; a wrapped positive value inside `len` is read as data the guest supplied, so no
out-of-bounds read), `:268` (the outer loop keeps evaluating it).  OB@8ea26abb:2748-2752 marks OB-28 RESOLVED by
#108 and :2775-2777 is the closed candidate text, whose "(also an `int addr` overflow)" aside is what survives.  A
closed row is not a filing, so this is NEW, LOW: UB with nondeterministic pixel sourcing, memory bounded.  Draft
changed from FILED OB-28.

bundle_devices3:F4 | CONFIRMED-NEW LOW pxfilladd "PX fill: int32_t lw + 1 overflows at INT32_MAX before the row loop"
Checked: `dev_px.c:345,:351` (`int32_t lw = px_readword(...)`, a guest word), `:396` (`lw = (lw + 1) >> 2`),
`:426` (`fb_y < y2 + lw`, a second signed add), `:427` (every row is bounded before the `memcpy`).  At 0x7fffffff
the add is UB; at 0x7ffffffe the loop runs ~2^29 bounded iterations (seconds, not a hang).  LOW.

bundle_devices3:F5 | CONFIRMED-NEW LOW rtcpendovf "dev_rtc: pending_interrupts increments without saturation and wraps negative under an unacknowledged high-rate timer"
Checked: `src/devices/dev_rtc.c:54` (int), `:71` (`pending_interrupts ++`, the only increment), `:145` (zeroed on
hz = 0), `:158-159` (decremented only on ACK), `:79-82` (asserted while `> 0`); `src/core/timer.c:281-291` and
`src/include/timer.h:82` (up to 1,048,576 ticks per timer per signal, so at the #429-clamped 2^31 Hz the counter
passes INT_MAX within seconds of signals).  After the wrap the line deasserts until 2^31 further ticks.  LOW: a
guest must leave ~2^31 ticks unacknowledged, and the wrap costs it interrupts it was not servicing.

bundle_devices3:F6 | CONFIRMED-FILED fbctrlcmdkill
Checked: `src/devices/dev_fbctrl.c:101-102` (`default: fatal(...); exit(1)`), `:150-152` (a DATA write with port 0
selected calls it), `src/include/testmachine/dev_fb.h:52-53` (FILL 3 / COPY 4 documented, unhandled);
OB@db8b1a33:22549-22559 (`fbctrlcmdkill`, HIGH, "reached by a guest DATA write while the COMMAND port (0) is
selected").  Astra's `:22544` is the same entry at `8ea26abb`.

bundle_devices3:F7 | CONFIRMED-NEW MED gssiglblid "ps2_gs: N_GS_REGS excludes the file's own highest register, so SIGLBLID (0x1080) is refused -- writes dropped, reads 0"
Checked: `src/devices/dev_ps2_gs.c:46` (`N_GS_REGS 0x108`, `reg[0x108]` indexes 0..0x107), `:77`
(`GS_S_SIGLBLID_REG 0x108`) and `:79-81` (the commented name table lists SIGLBLID as the fourth privileged
register), `:94-105` (#99's guard `regnr >= N_GS_REGS` rejects it: loud-once, reads return 0, writes ignored).
The constant is upstream's off-by-one; #99 adopted it as the boundary.  The local evidence that SIGLBLID is a
register of this device is the file's own table; there is NO Sony GS manual under `_scratchpad/` (checked `ls
*.txt`), so the read/write contract is from the register's definition (SIGID/LBLID, EE-readable and writable),
not from a page I opened -- stated as such, per the cite-only-what-you-read rule.  MED on the brief's scale: a
documented register answers 0 and forgets writes; the fix is the constant.  Draft changed from DOUBTFUL.

bundle_devices3:F8 | CONFIRMED-NEW LOW kn02banameshift "kn02ba: 1 << i for i == 31 in the interrupt-name snprintf, the sibling #24 cast at :192 did not"
Checked: `src/devices/dev_kn02ba.c:185` (i in 0..31), `:188-189` (`"%s.kn02ba.0x%x", ..., 1 << i`), `:192`
(`templ.line = (uint32_t)1 << i` -- the #24 cast).  Construction-time UB once per DECstation machine, prints
0x80000000 in practice.  LOW.  Not filed (`shiftubcensus` names no site).

bundle_devices3:F9 | TEST-GAP-FILE mk48aliasrow
Checked: `regress/mk48_nvram_probe.py:290-297` (nine rows, each a fresh `session()` -- `:136-149` is one
`subprocess.run` per call -- writing ONE offset and reading the SAME offset back), `:286-287` and CHANGELOG.md:4736-
4737 ("each writing a DISTINCT byte so a mutant folding offsets onto one cell is caught too"): under any folding or
injective remap a same-offset write/read agrees, so the distinct bytes see nothing; `:183-189` (the `nvram0`
control compares 0x100/0x101 only).  `regress/artifacts/mk48nvramkill/killtable_20260910/t3/SCORES.txt` carries
M_OLD, M_HALF, M_ICSR, M_NULL and HEAD -- NO folding mutant, so the sentence was never measured.  The row owed is
one session writing all nine distinct bytes and reading all nine back.  L4 owed with the filing (the draft
named the overclaim and did not dispose it): CHANGELOG.md:4736-4737 -> "Nine round-trip rows close it (`0x1fef`
plus the eight), each writing a DISTINCT byte.  Each row runs in its own emulator session and touches one offset,
so the distinct bytes do NOT catch a mutant folding several offsets onto one cell -- a write and read-back of the
same offset agree under any remap.  The kill table carried no folding mutant; the aliasing row is filed as
`mk48aliasrow`."  and `mk48_nvram_probe.py:286-287` -> "#  Each row writes a DISTINCT byte so a stale value from
another row's scratch cannot satisfy it.  NOTE: these rows run one offset per session and cannot see a mutant
folding offsets onto one cell (filed: mk48aliasrow)."

bundle_devices3:F10 | CONFIRMED-FILED rtclen
Checked: `regress/diff_rtc_range.c:108-109` (the `memory_readmax64` stub returns `stub_in` and ignores `data` and
`len`), `:121-126` (`wr_hz` feeds it), `:180-205` (R1-R3 are the wide rows); OB@8ea26abb:6889-6890 (`rtclen`:
"`len` -> `4` ... passes all 18 detector rows").  Same defect, same id.

======================================================================================================
bundle_devices4  (3 findings: 1 new, 1 filed, 1 record)
======================================================================================================

bundle_devices4:F1 | CONFIRMED-FILED sgigbeconvover
Checked: `src/devices/dev_sgi_gbe.c:170` (automatic `buf[16384]`), `:259-264` (`len` bytes read, < 512 on a
partial tile), `:281` (`for (i = 0; i < 512; ...)` converts through byte 511), `:267,:297-298` (`fb_len` forwards
only the read pixels); OB@8ea26abb:15941-15956 (`sgigbeconvover`, LOW, "computed and discarded, not a guest
disclosure", fix `i < len`).  Same defect, same id.

bundle_devices4:F2 | CONFIRMED-NEW MED mpstartupsp "dev_mp STARTUPCPU sets the startup stack pointer only for MIPS and PPC; every other test machine starts the CPU with its old SP against the documented contract"
Checked: `src/devices/dev_mp.c:147-151` (`stack_addr` stored for any arch), `:98-115` (SP applied in the
`ARCH_MIPS` and `ARCH_PPC` arms only; the #221 `default:` warns and falls to `running = true`);
`doc/experiments.html:279-282` ("CPUs started with startupcpu() above will have their stack pointer set to this
value"); `src/machines/machine_test.c:148-152` (the `mp` device is added by `default_test()` for every test
machine, `:187-191` testarm among them).  Broadened from Astra's ARM: testarm, testsh, testm88k, testriscv and
every other non-MIPS/PPC test machine take the default arm.  MED: guest-visible, contrary to the device's own
documentation; the option-set member is IMPLEMENT (ARM r13, SH r15, m88k r31, RISC-V x2), a small edit per
arch.  Not filed: no OB line matches `startupstack`/`stack_addr`/`STARTUPCPU`; OB@db8b1a33:21168-21183 is the
allocation-growth row.

bundle_devices4:F3 | RECORD-L4 "- **#80 (OB-14, `dev_sgi_gbe.c`, tile over-read, High):** for a partial tile the per-line read length `partial_pixels * bytes_per_pixel` reaches 992 bytes at every depth (RHS field 31 x 32 x 8 / bitdepth pixels), which fits the 16 KiB read buffer; what overflowed was the CONVERTED copy, `fb_len = (len / bytes_per_pixel) * 3` -- up to 2976 bytes in 8-bit mode against `uint8_t fb_buf[512*3]` (1536 bytes) -- handed to `dev_fb_access()`.  Clamping the line length to 512 bytes bounds that converted copy to the buffer's 512 pixels."
Checked: CHANGELOG.md:21714-21716 ("can exceed the `uint8_t fb_buf[512*3]` per-line size" -- 992 bytes does not
exceed 1536); `dev_sgi_gbe.c:592-594` (`partial_pixels = (field & 0x1f) * 32 * 8 / bitdepth`, bitdepth 8/16/32/64
-> 992/496/248/124 pixels, times 1/2/4/8 bytes = 992 in every case), `:569` (overlay: `(field & 0x1f) * 32` = 992
at 1 byte/pixel), `:259-261` (the OB-14 clamp), `:267` (`fb_len` = 2976 for 992 8-bit pixels), `:279` (1536-byte
`fb_buf`), `:297-298` (that copy is what `dev_fb_access` reads).  The replacement is for the CHANGELOG item; the
source comment at `:260` should read `/* OB-14: fb_buf holds 512 pixels (512*3 bytes); a longer line over-reads
it in the converted copy */`.  LOW.

======================================================================================================
bundle_devices5  (1 finding: 1 new)
======================================================================================================

bundle_devices5:F1 | CONFIRMED-NEW LOW macesignedshift "MACE assert/deassert compute 1 << line in int; line 31 is registered and undefined"
Checked: `src/devices/dev_sgi_ip32.c:501` and `:513` (`uint32_t line = 1 << interrupt->line`), `:656-677` (lines
0..31 registered twice, SERIAL and MISC), `:417-419` (the CRIME siblings #24/#25 cast).  Reaching 31 needs a device
connected to that input; the standard IP32 wiring uses lower inputs, and the route Astra names is the debugger's
`device add` (`src/debugger/debugger_cmds.c:552-553`) with an interrupt path naming `.mace.31`, i.e. an OPERATOR
action followed by a guest-driven assert (`src/devices/dev_ns16550.c:95-102`).  So: undefined, exercised only by
configuration, no guest-only route.  LOW, qualification retained.  Not filed (`shiftubcensus` names no site).

======================================================================================================
(a)  CODE findings I could NOT confirm as stated
======================================================================================================

* devices1:F3 -- the stated premise ("slow-path writes are not tracked") is false in general: a slow-path write
  is exactly where `memory_rw.c:526-547` records the dyntrans window, so on every non-ARM machine the tick clips.
  What survives is the `MEMORY_NOT_FULL_PAGE` exemption in that very condition, whose only live producer is ARM
  subpage/tiny-page translation, on one machine (cats).  Confirmed in that narrowed form, unmeasured.
* devices3:F7 -- the register's rejection is confirmed from the file; its read/write hardware contract is NOT
  confirmed from any local source (no GS manual is present).  Ruled on the file's own register table.
* devices5:F1 -- confirmed as UB; not confirmed as guest-reachable without operator configuration, which Astra
  itself states.
* devices3:F3 -- confirmed as UB, NOT confirmed as an out-of-bounds read: the #108 bound holds a wrapped address
  inside `len`.  Astra's "already filed" is wrong in the sense that matters: OB-28 is closed.
* devices1:F2 -- confirmed as uninitialised consumption; a HIGH consequence is not established (an unknown
  opcode no longer exits, `diskimage_scsicmd.c:1383`).
* Everything Astra marked `high` on a memory or process consequence -- devices1:F1, devices3:F2 -- is confirmed
  at that grade.

======================================================================================================
(b)  What I noticed that Astra did not (mine)
======================================================================================================

1. devices1:F1 has a SECOND, simpler route that Astra's "existing allocation" wording does not cover: after the
   CDB returns 2 the phase is PH_DATAOUT with `data_out == NULL` and `data_out_len == size`, and a DREG write
   stores through `NULL + transfer_bufpos` (`dev_mb89352.c:225-226,:246`).  Same row, and the cheaper witness.
2. The `res` discarded at `dev_mb89352.c:271-272` (PH_DATAOUT completion) is the exact defect the #295 comment
   said #338 would re-create -- a short DATAOUT returns 2, no status buffer is built, and the guest's status read
   halts the CPU.  It is the `mb89352halt` class (OB@db8b1a33:11425-11434: "four different wrong outcomes from one
   omitted completion step"); worth naming in that row rather than filing again.
3. devices2:F2: the type-1 converter enqueues nothing for an unmapped byte too (`dev_pckbc.c:329-336`); the
   record text above says "all three", Astra and the draft said tables 2/3.
4. devices4:F2 is not ARM-specific: every test machine except testmips/testppc takes the default arm.
5. devices1:F4: the same rejected-dimension read-back appears at `dev_sgi_gbe.c:536` (`VT_VPIX_EN`, -1 ->
   0xffffffff) and the HCMAP mirror at `:546`; one row covers them.
6. devices3:F7: the comment table at `dev_ps2_gs.c:79-81` is upstream's own evidence that 0x108 was meant to be a
   valid index; the fix is `N_GS_REGS 0x109`, and the #99 guard then stands unchanged.
7. Three signed-shift rows (lunaintshift, kn02banameshift, macesignedshift) are one class; a records round may
   file them as children of `shiftubcensus` rather than as three peers -- I kept three ids because the brief asks
   for one per finding and they are different sites in different files.

======================================================================================================
(c)  DENOMINATOR
======================================================================================================

28 of 28 findings checked against committed source/regress/CHANGELOG text at `8ea26abb` (and OUTSTANDING_BUGS.md
at the commit stated per citation); 0 ruled from Astra's text alone.  Every existing id cited (mb89352halt,
fbctrlcmdkill, rtclen, sgigbeconvover, shiftubcensus, asiceventaddr) was confirmed present at `db8b1a33` by grep;
every proposed id (mboutcapacity, mbcdbincomplete, vgadirtyarm, gberesizezero, vgacursoronly, autodevregorder,
lunaintshift, lunad3diag, fdcdiagrows, pxdmatail, dectxzero, gifputcharovf, pxfilladd, rtcpendovf, gssiglblid,
kn02banameshift, mk48aliasrow, mpstartupsp, macesignedshift) was confirmed ABSENT there, and prose greps for each
defect (dec21143, startupstack/STARTUPCPU, SIGLBLID/N_GS_REGS, copyspans/dma_buf, pending_interrupts,
vga_update_textmode, VCMAP/HCMAP/dev_fb_resize, autodev, kn02ba, the luna/MACE expressions) found only the
unrelated entries named inline.  `DISPOSITIONS.md` (291 lines, batches 1a-2b) has no entry for any of these files,
so no cross-batch duplicate.  No builds, probes or edits were performed.

======================================================================================================
Draft dispositions changed, and why
======================================================================================================

* devices1:F3  DOUBTFUL -> CONFIRMED-NEW HIGH vgadirtyarm.  The draft's refutation ("ordinary slow-path writes also
  update tracking at memory_rw.c:526-547") is correct and stops one clause short: the condition it cites contains
  `!(ok & MEMORY_NOT_FULL_PAGE)`, and `memory_arm.c:235` produces that flag for subpage mappings, on a machine
  (cats) that constructs a VGA.  Astra's finding is right in a form narrower than it wrote.
* devices3:F3  FILED OB-28 -> CONFIRMED-NEW LOW gifputcharovf.  OB-28 is a RESOLVED row (OB@8ea26abb:2748-2752);
  a finding disposed as "filed" against a closed row is never acted on.  The draft's LOW grade is kept.
* devices3:F7  DOUBTFUL -> CONFIRMED-NEW MED gssiglblid.  The draft withheld a ruling for want of the Sony manual.
  The file's own definitions (`:77`, `:79-81`) are local evidence that the register exists on this device and that
  the array excludes it; what the manual would add is the R/W detail, and I have said which part is unverified.
* devices3:F9  category kept (TEST-GAP-FILE) and the L4 correction the draft named ("CL overclaims") is now
  disposed with exact text, because the false sentence sits in the CHANGELOG and the probe at HEAD.
* devices1:F6 and devices2:F2  category kept; replacement texts rewritten -- the F6 rewrite keeps the #263
  history the draft's version dropped, the F2 text covers all three converters and names the host-only residual.
* devices4:F2  category and grade kept; the title is broadened beyond ARM, which is what the source says.
* All other 21 dispositions agree with the draft in category and grade, each re-derived from the source above.
