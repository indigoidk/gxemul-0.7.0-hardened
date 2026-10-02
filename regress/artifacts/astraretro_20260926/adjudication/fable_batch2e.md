VERDICT: 10 confirmed-new, 2 confirmed-filed, 8 record-L4, 5 test-gap, 0 refuted, 0 unsettled, 4 duplicate, of 29 findings

FABLE_RETRO_2e_ALIVE_0926

CHECKPOINT.md first line, verbatim:
`# CHECKPOINT -- 2026-09-30 11:55 RUNNING AGAIN (owner: grok freely, skip Ollama, Fable adjudicates, Astra confirms); loop cron d1e654c4 (13,43); codex re-run cron 14:27`

ASTRA RETRO-REVIEW -- FABLE ADJUDICATION, batch 2e (dev_asc.c, diskimage.c, diskimage_scsicmd.c, the src/file
bundle).  Adjudicated at `8ea26abb` (HEAD is `db8b1a33`; `git diff --stat 8ea26abb db8b1a33 -- src/` is empty, so
every source line below is HEAD's too).  Every source, regress and CHANGELOG citation is at `8ea26abb`;
`OUTSTANDING_BUGS.md` was read at `db8b1a33` (the draft's line numbers, re-checked).  Read only: `git show
8ea26abb:<path>` piped through `awk '{print NR": "$0}'`; no build, no run, no edit but this file.  Model:
claude-fable-5-1, first-hand.

The draft (`codexpack_20260928/draft_2e/codex_draft_2e.txt`) was read BEFORE the source, as the brief directs,
and every one of its lookups was re-run.  THREE of its 29 dispositions are changed: diskimagescsicmd:F1 (NEW HIGH
`modeselectbuflen` -> DUPLICATE of batch 2d's `mboutcapacity`: the draft searched OUTSTANDING_BUGS and this
batch, not the previous batch's rulings), diskimagescsicmd:F3 ("DUPLICATE-OF-ROW scsicapnosense" -> DUPLICATE
bundle_include1:F5: that is not a menu form, and no such row exists at HEAD -- it is batch 1b's pending filing),
diskimagescsicmd:F10 (FILED-BY-PROSE -> TEST-GAP-FILE: OUTSTANDING_BUGS.md:5234-5238 is an "assessed, not
changed" limitation note that itself says a row is needed; a note saying a row is owed is the gap, not its
filing).  Four replacement texts are rewritten (devasc:F5, diskimage:F7, diskimagescsicmd:F7, F8), one check the
draft skipped is done (devasc:F4's REVIEW_FINDINGS.md:965), and diskimage:F5's severity remark is NOT adopted
(a FILED row keeps its grade until its owner re-grades it).  Details in the last section.

Severity scale as the brief defines it: HIGH = a guest can end the process, read/write outside a buffer, or hang
it; MED = guest-visible behaviour contrary to the documentation; LOW = diagnostics, latent code, test gaps.
One qualifier that applies to both HIGH file-loader findings: the input is a file the operator names, or the OS
loader the boot-block code extracts from a disk image and feeds to the same loader (bootblock.c:445-490 ->
emul.c:638), so a guest that writes its own disk supplies it at the next boot.  That is this fork's established
threat model for src/file (#14-#66), and I grade by it.

======================================================================================================
bundle_file  (3 findings: 2 new, 0 filed, 0 record, 1 test-gap)
======================================================================================================

bundle_file:F1 | CONFIRMED-NEW HIGH symdemanglebound "The C++ demangler copies a length-prefixed name component without testing source termination, over-reading a NUL-terminated loader string by up to MAXLEN bytes"
Checked: `src/symbol/symbol_demangle.c:91-92` -- `while (len-- >= 1 && result_len < MAXLEN) result[result_len ++] =
*name++;` -- `len` is the decimal count parsed at `:79-83` from the name itself, `MAXLEN` is 1000 (`:46`) and
bounds the DESTINATION only; the `name[0]` test at `:73` guards the start of each component, never the copy.
Entry: `src/symbol/symbol.c:263` -> `symbol_demangle_cplusplus()` (`:236-246`, `_ZN` names only).  All four
loaders hand it a string whose START is bounded and whose table is NUL-terminated -- `file_aout.c:249,:265-267`,
`file_elf.c:675-677`, `file_ecoff.c:465-471`, `file_macho.c:295-299` -- so `_ZN999a` as the last string of a
table walks ~1000 bytes past the terminator and past the malloc block.  The a.out terminator at `:247-249` was
added for exactly the consumer that defeats it.  No OUTSTANDING_BUGS match (0 hits for `demangl`).

bundle_file:F2 | CONFIRMED-NEW HIGH ecoffoffsetspan "ECOFF table-offset guards admit a sign-extended negative offset, then seek unchecked and exit(1) on the resulting short read"
Checked: `src/file/file.c:85-89` -- `if (Wi == 0 && (Wb & 0x80)) Wuns = (uint64_t) -1; /* sign-extend */` then
`var = Wuns` -- so `f_symptr` (`file_ecoff.c:144`), `cbSsExtOffset` and `cbExtOffset` (`:293,:295`, all decoded as
`uint32_t` into `off_t`, `:67,:273`) go negative when bit 31 is set.  Guards `:322-326` and `:414-421` cast to
`uint64_t` and ADD the extent: `(uint64_t)(-1) + issExtMax + 1 == issExtMax`, below `file_size`, so they pass.
`fseek` results are discarded at `:332`, `:428`, `:439` (EINVAL leaves the position where the symhdr read put it);
the reads at `:333-337`, `:429-432`, `:440-444` then `exit(1)` on a short count -- or succeed on the WRONG bytes if
enough file remains.  This defeats the fork's own #59/#62 policy of skipping a bad table (CHANGELOG.md:21614-21618).
The draft's qualifier stands: converting a `uint64_t` >= 2^63 to `off_t` is implementation-defined in C99 (gcc:
modulo).  No OUTSTANDING_BUGS match.

bundle_file:F3 | TEST-GAP-FILE fileloaderrows
Checked: `regress/gate_upstream.sh:18-19` says in its own header "ECOFF, Mach-O, SREC and Android still have no
corpus here"; its case list `:104-110` is four ELF, one a.out, one b.out and the nonsense file.  CHANGELOG.md:
21614-21625 records replayed AUDIT cases as verification of #57-#66; none is a committed row.  Census of committed
non-artifact `regress/` for `ecoff|ECOFF|macho|Mach-O`: gate_upstream.sh only.  LOW.

======================================================================================================
devasc  (7 findings: 4 new, 0 filed, 2 record, 1 test-gap)
======================================================================================================

devasc:F1 | CONFIRMED-NEW HIGH ascwidecount "A 32-bit ASC transfer-count write during a continued DATA_OUT DMA yields a negative len2 that both span guards pass, and the DEC memcpy takes it as size_t"
Checked: `src/devices/dev_asc.c:1116` `idata = memory_readmax64(cpu, data, len)`; `:1155` `d->reg_wo[regnr] =
idata;` with no byte mask into `uint32_t reg_wo[]` (`:154`); `:577-578` `int len2 = TCL + TCM * 256` (uint32
arithmetic narrowed to int: TCL = 0xffffffff gives -1 on gcc); `:583` tests `== 0` only.  Destination guard
`:610-614`: `data_out_offset` is `size_t` (diskimage.h:189), so `offset + (size_t)(-1)` is `offset - 1` mod 2^64
and is NOT `> data_out_len` whenever `offset >= 1`.  Source guard `:618-622`: `dma_off + (size_t)(-1)` is
`dma_off - 1`, not `> ASC_DMA_SIZE` whenever `dma_off >= 1`.  Continued path `:662-665`: `memcpy(..., len2)` with
`len2 == -1` -> `SIZE_MAX`.  The FRESH path (`:629-649`) is safe by accident: offset 0 makes the destination guard
wrap and clamp to `data_out_len`.  Sequence: WRITE wanting two blocks; TRANS|DMA with TC 512 (fresh, offset 512);
a word store of 0xffffffff to NCR_TCL; DMA address low bits nonzero; TRANS|DMA again.  DEC/pmax only: on PICA
`dev_jazz.c:213` `i < (int32_t)len` is false for -1, the callback returns 0, `:707`'s `len2 > 0` is false, and the
guest survives with TC set.  The draft's C99 narrowing qualifier is kept.  OB-5 (OUTSTANDING_BUGS.md:2887) is the
DMA-window MMIO copies, a different site.

devasc:F2 | CONFIRMED-NEW MED ascoutresid "A DATA_OUT DMA clamped to the target's remaining length still reports residual 0 with Terminal Count set"
Checked: `:610-614` clamps `len2` to `data_out_len - data_out_offset`; `:707` compares `moved` against the CLAMPED
count -- and `:691-695` says why that is right for the FAILURE decision (the disk wanting less than offered is a
benign re-entry, #283 measured); but the epilogue `:755-761` then stores `len = 0` into TCL/TCM and sets
`NCRSTAT_TC` unconditionally.  Programmed 1,024, target 512: 512 moved, counter 0, TC set.  #281 fixed exactly
this for DATA_IN at `:560-568` (residual = programmed - moved, TC only at zero); #283 fixed the callback-short
half of DATA_OUT only (CHANGELOG.md:20541), and #282's own record at `:20535` had named the DATA_OUT arm as
telling "the same lie".  A fix is confined to the report; the `:707` decision must stay as measured.  MED; the
LSI 53CF92A citation was not checked (no local copy).  No OUTSTANDING_BUGS match.

devasc:F3 | CONFIRMED-NEW MED asccmddma "COMMAND-phase DMA reads the CDB from the private DEC buffer even when an external DMA controller is configured (PICA)"
Checked: `:984-1000` -- `ch = d->dma[ofs & (ASC_DMA_SIZE-1)];` with no `d->dma_controller` branch, unlike both
DATA arms (`:459-469`, `:638-648`); `d->dma` is zeroed at `:1573-1574` and guest-mapped only under
`DEV_ASC_DEC` (`:1583-1591`); `machine_arc.c:217-218` installs PICA with `dev_jazz_dma_controller`.  A PICA guest
issuing SELECT with the DMA bit gets `len` zero bytes as its CDB; `cmd_len = len` (`:991-992`) passes the #113
check at `diskimage_scsicmd.c:309-316` whenever it is at least the group length, so opcode 0x00 executes as
TEST UNIT READY with #284's residual 0 / TC.  `:1014-1016` records that arc preloads the FIFO -- the reference
guest's habit, not the hardware's contract.  The draft's qualifier (the CDB-length check must pass) is kept.

devasc:F4 | CONFIRMED-NEW MED ascpiozero "PIO DATA_IN pushes zeros from the never-populated incoming_data instead of xferp->data_in" -- assign the id to the stub already acknowledged at REVIEW_FINDINGS.md:965
Checked: `:367-392` -- the non-DMA DATA_IN arm tests `xferp->data_in` at `:368`, then reads `d->incoming_data` at
`:378-379`, whose own #105 comment says it "is never allocated" (no writer in the file besides the free at
`:386-387`; the struct is zeroed at `:1561`); `:383` pushes the 0 into the FIFO.  REVIEW_FINDINGS.md:965 already
records "PIO data-in returns zeroes (the source buffer is never populated)" as unreachable by Ultrix/NetBSD/
OpenBSD -- a known stub, but NO queue row (OUTSTANDING_BUGS: 0 hits for `incoming_data`; the `:2333-2342` sweep
lists `:373` as a diagnostic site only).  Reachable by any guest issuing TRANS without the DMA bit in DATA_IN.
MED by the rule; the fix is member 7 (deliver `xferp->data_in`) or member 2 (decline); its sibling, the PIO
DATA_OUT stub at `:573-574`, belongs in the same row (see (b)).

devasc:F5 | RECORD-L4 "LATCHED RATHER THAN VERBOSITY-GATED, unlike the stray-access messages of #276 in this same file: this arm falls through to the common epilogue below, which forces cur_phase to PHASE_STATUS and raises NCRSTAT_INT | NCRINTR_BS (DEVICE_TICK asserts the line), so the guest sees a bus-service interrupt in STATUS phase and nothing that names the unhandled phase.  A DEBUG gate would leave that silent under -q -- the mode the boot harness runs in -- whereas a latch keeps exactly one line in the log it greps.  (Until 2026-09-30 this comment said the arm 'sets no interrupt'; it does, through the epilogue.)"
Checked: `:835-841` says "this arm sets no interrupt, so the transfer simply hangs and the guest is never told
through any other channel".  The `else` arm `:829-848` sets neither `res` nor `all_done`, so `:856-861` forces
`cur_phase = PHASE_STATUS` and `:870-873` sets `NCRSTAT_INT`, `NCRINTR_BS` and the phase bits; `DEVICE_TICK(asc)`
`:175-178` asserts the IRQ on that rising edge.  The same sentence is in CHANGELOG.md:20491 ("the `else` arm sets
**no interrupt**, so the transfer simply hangs"; db8b1a33:20575) -- correct it in place to "the `else` arm reaches
the common epilogue, which forces PHASE_STATUS and raises NCRSTAT_INT | NCRINTR_BS -- a bus-service interrupt
that does not name the unhandled phase -- so under `-q` ...".  The latch's rationale survives on the corrected
basis; only the mechanism sentence was false.

devasc:F6 | RECORD-L4 "/*  #245: route the guest-spammable diagnostic through the verbosity-gated SUBSYS_DEVICE channel at VERBOSITY_DEBUG (suppressed by default; main.c drops one level after startup, so during the run it takes -v -v, or `break device`, or single-stepping) so a guest hammering NCR_CMD can't flood the host log.  */"
Checked: `:1495-1498` says "shown at -v or `break device`"; the call at `:1499` is `VERBOSITY_DEBUG`.  misc.h:
253-257: INFO 2, DEBUG 3, `ENOUGH_VERBOSITY` is `>=`; debugmsg.c:104 default INFO; main.c:698-699 each `-v` adds
1 (no upper clamp, debugmsg.c:404-415); main.c:803 subtracts 1 before `emul_run`.  One `-v`: 3 -> 2 during the
run, NOT shown; two: 4 -> 3, shown.  debugmsg.c:181-183 also shows it under `single_step` or a subsystem
breakpoint.  OUTSTANDING_BUGS.md:2582-2584 records the DEBUG gating correctly; only the comment is wrong.

devasc:F7 | TEST-GAP-FILE ascaccountrows
Checked: `regress/gate_hygiene.sh:876-877` with `:887-888` assert that `short DATA_IN DMA` / `short DATA_OUT DMA`
are ABSENT from the boot logs (count 0) -- a distress-absence row; `gate_mips.sh` boots.  CHANGELOG.md:20536
("Probe, on BOTH machines ... asserting both residual bytes and the TC bit") and `:20548` (#283's arc rig, block
byte-identical) describe round artifacts.  Census of committed non-artifact `regress/`: no file asserts
`NCR_TCL`, `NCR_TCM` or `NCRSTAT_TC`.  LOW.

======================================================================================================
diskimage  (9 findings: 4 new, 1 filed, 3 record, 1 test-gap)
======================================================================================================

diskimage:F1 | CONFIRMED-NEW MED writeflusherr "Under -f, a guest WRITE reports GOOD after fflush()/fsync() fail -- overlay data, flat file and bitmap all discard the results"
Checked: `src/disk/diskimage.c:1315-1318` (overlay data), `:1265-1268` (flat), `:1207-1212` (bitmap) call
`fflush`/`fsync` under `do_fsync` (`:49`, the `-f` flag) and test neither; `:1325` then publishes the bitmap and
`:1329` returns `len`, so `diskimage_scsicmd.c:907-912` reports GOOD (its MEDIUM ERROR fires only on a short
helper return).  Contrast `diskimage_sync()` `:2388-2412` (#437), which checks both.  With stdio buffering the
`fwrite` at `:1263`/`:1302` succeeds into the buffer and ENOSPC/EIO surfaces at `fflush`, so the guest is told
GOOD for bytes that are not on disk -- the durability lie #416/#417/#437 exist to remove, on the one flag whose
purpose is durability.  Needs a host I/O fault.  OUTSTANDING_BUGS.md:2729 is the discarded-return defect #416
repaired; `ovsync` (`:1271-1277`) is SC(16).  MED.

diskimage:F2 | CONFIRMED-NEW MED drecalccap "READ CAPACITY (and the two other recalc callers) re-run diskimage_recalc_size() on a d:-retyped floppy image and replace its exact geometry with 16/63"
Checked: `:2028` recalc runs before the retype; `:232-236` types FLOPPY only while `type == DISKIMAGE_UNKNOWN`;
`:2066-2067` retypes to the machine default; `diskimage_scsicmd.c:489` (READ CAPACITY) -- and also `:1139` (READ
SUBCHANNEL / READ CD CAPACITY) and `:1222` (READ TRACKINFO), the only other callers (`git grep`) -- call it again,
and the switch at `:238` now takes `default:` (`:268-272`, 16 heads / 63 spt).  `:291-307`: 1,474,560 / 516,096 ->
3 cylinders -> 1,548,288 B -> 3,024 blocks, was 2,880.  `:1592-1600` bounds reads by `nr_of_logical_blocks *
logical_block_size` (zero-filled) and writes by `total_size`, so the 144 phantom blocks read zeros and refuse
writes -- the exact consequence #418's comment at `:2044-2054` says its placement was chosen to avoid, and
`diff_diskimage_parse.c:214-215` cannot see (F10 below).  OUTSTANDING_BUGS.md:7624-7628 is the ordinary-image
rounding residual, not this.  MED.

diskimage:F3 | CONFIRMED-NEW MED stalelbsbound "MODE SELECT changes logical_block_size without refreshing nr_of_logical_blocks, so the read bound shrinks until a capacity command recalculates"
Checked: `diskimage_scsicmd.c:1319-1324` assigns `logical_block_size` only; `diskimage.c:1592-1593` bounds reads
by `nr_of_logical_blocks * logical_block_size`; the count is refreshed only at `:489`, `:1139`, `:1222`.  A
516,096-byte image: 1,008 blocks at 512; after MODE SELECT 256 the read limit is 1,008 * 256 = 258,048, so every
read past half the disk gets CHECK CONDITION 05/21/00 (`:816-825`) until a READ CAPACITY.  The draft's qualifier
is right: "upper half" is exact only for cylinder-aligned sizes.  `lbsmask` (OUTSTANDING_BUGS.md:471) is the
power-of-two mask -- different.  MED.

diskimage:F4 | CONFIRMED-NEW LOW cuebomparse "The CUE sniffer skips a UTF-8 BOM that the parser keeps in its first keyword, so a BOM-prefixed FILE line is dropped and the image falls back to flat"
Checked: `:623-625` skips EF BB BF in `diskimage__looks_like_cue()`; the parser `:685-689` tokenizes `line` from
byte 0 (`:505-536` keeps the bytes), so the keyword is BOM+"FILE", `:715` does not match, `:868` ignores it, the
next TRACK fails at `:767-772` ("before any FILE"), and `:1043-1058` falls back to a flat image.  Only a BOM on a
FILE first line matters (a BOM'd REM line is ignored either way).  Host-supplied input; LOW.

diskimage:F5 | CONFIRMED-FILED lbsmask
Checked: `:305-307` `if (size & (d->logical_block_size - 1))`; `diskimage_scsicmd.c:1319` accepts 256..8192
including non-powers of two; `regress/diff_diskimage_geom.c:718-722` `GEOM_ROW_LBS257` is `#ifdef`'d out.
OUTSTANDING_BUGS.md@db8b1a33:471-472 names `lbsmask` ("power-of-two block-size assumption, reachable only via
SCSI controllers that complete MODE SELECT"); `:15590-15591` "held behind GEOM_ROW_LBS257".  Rider for the row:
`diskimage_scsicmd.c:1224-1226` (READ TRACKINFO) carries the same mask.  The draft's "MED under this brief's rule,
although recorded LOW" is noted, not applied: a filed row keeps its grade until its owner re-grades it.

diskimage:F6 | RECORD-L4 "The bound above refuses a past-the-end write before it starts, so an in-bounds short result means either a genuine I/O failure or an overlay write the helper declined (#164: a length that is not a multiple of OVERLAY_BLOCK_SIZE, or an unaligned offset -- fwrite_helper returns 0 without touching the file)."
Checked: `:1643-1645` says "reachable only through a genuine I/O failure"; `fwrite_helper()` returns 0 at `:1279`
(length not a multiple of 512) and `:1285` (unaligned offset) on an overlay disk with no I/O attempted, and
`:1653` accepts that 0 as a short write.  Replace `:1643-1645`.

diskimage:F7 | RECORD-L4 "on the overlaid path this function now returns `len` or 0.  On `len` the caller's `lendone < len` memset is a deliberate no-op HERE; on 0 (the seek failures above) it zero-fills the whole request, which is the intended failure shape.  It is NOT dead -- MEASURED by deleting it: ..." (the rest of the paragraph unchanged)
Checked: `:1498-1500` says the memset is "a deliberate no-op HERE"; `:1397` and `:1407` return 0 on a seek
failure, and `:1627-1628` then executes `memset(buf + 0, 0, len)` -- the whole buffer, including slices already
read.  The same paragraph's producer count at `:1509-1512` names those seek failures, so the sentence contradicts
its own continuation.  The draft's rewrite is equivalent; mine keeps the measured "NOT dead" sentences intact
because they carry a kill this record depends on.

diskimage:F8 | RECORD-L4 "chosen because it leaves the fsync count intact -- a test counting fsync calls alone stays green -- while the fflush count drops from two to one and the ordered trace shows the missing F(data)"
Checked: CHANGELOG.md:25608-25610 (db8b1a33:25692-25694) "a mutant that drops the overlay-data `fflush` while
KEEPING the `fsync`, chosen because it leaves the counts intact and only the trace can see it".
`regress/selfmutants/diskimage_sync.why` says the opposite in its own words: "any test that counts fsync calls
alone stays GREEN.  Only the fflush row goes red."  `.old`/`.new` confirm the edit; trace with the fix `F(data)
S(data) F(bitmap) S(bitmap)` = (2 flush, 2 sync), mutant `S(data) F(bitmap) S(bitmap)` = (1, 2).  Replace the
clause.

diskimage:F9 | TEST-GAP-FILE cuemapgap
Checked: CHANGELOG.md:19826-19830 (db8b1a33:19910-19914) "each regression-gated ... real per-track sector
mapping ... per-sector raw-header stripping".  Committed non-artifact `regress/` mentions CUE once:
`diff_diskimage_io.c:134` `d->nr_of_tracks = 0;`, which routes every read AWAY from `diskimage_access__cue()`
(`diskimage.c:1620-1621`); `diff_diskimage_parse.c` fixtures are flat images.  Astra's `med` confidence is
right -- the #127 round may have gated it ad hoc -- but the committed tree carries no row.  LOW.  Rider: the
"each regression-gated" sentence is unsupported for the CUE bullet until the row lands.

======================================================================================================
diskimagescsicmd  (10 findings: 0 new, 1 filed, 3 record, 2 test-gap, 4 duplicate)
======================================================================================================

diskimagescsicmd:F1 | DUPLICATE bundle_devices1:F1  (batch 2d, `mboutcapacity` HIGH -- add `:1287` to that row)
Checked: `src/disk/diskimage_scsicmd.c:1283-1287` -- the #285 assignment `xferp->data_out_len = 12;` is
unconditional by design ("stays BEFORE the test on purpose"), so a data_out buffer of another size that survives
into MODE SELECT keeps its allocation and gains a 12-byte length; `dev_mb89352.c:225-226` and `:239-246` bound
DREG writes on `data_out_len`; `:279-280` enters PH_DATAOUT on `res == 2` with no allocation and no
`transfer_bufpos` reset; `:499-502` XFR CMD leaves `data_out` in place; `:661-665` a TCL/TCM/TCH write re-arms
DREG.  That is, byte for byte, the mechanism the Fable seat ruled HIGH in batch 2d for the WRITE site
(`fable_batch2d.md:29-42`: `diskimage_scsicmd.c:888-892` `data_out_len = size; return 2`, sequences (i) NULL
`data_out` and (ii) a retained short block written past).  Same controller weakness, second disk-layer site: ONE
row.  Riders for `mboutcapacity`: (1) `:1287` is the second re-sizing site, and the #285 comment's "on purpose"
is what makes it unconditional; (2) the ASC is NOT exposed -- `dev_asc_newxfer()` `dev_asc.c:318-330` frees the
transfer on every SELECT, so no buffer survives into a later command there.  The draft's "No same-defect match"
searched OUTSTANDING_BUGS and this batch; the match is the previous batch's ruling.

diskimagescsicmd:F2 | DUPLICATE diskimage:F2
Checked: `:489` `diskimage_recalc_size(d);` after the retype at `diskimage.c:2066-2067`; values re-derived above
(2,880 -> 3,024; CHS (80,2,18) -> (3,16,63)).  One row, `drecalccap`, carrying all three recalc callers.

diskimagescsicmd:F3 | DUPLICATE bundle_include1:F5  (batch 1b, `scsicapnosense` MED -- DISPOSITIONS.md:34-37; not yet a row in OUTSTANDING_BUGS.md at HEAD, 0 hits)
Checked: `:773-778` and `:880-885` call `diskimage__return_default_status_and_message()`, which clears the sense
latch at `:187-188`, then store status 0x02; REQUEST SENSE `:989-991` answers 0/0/0.  Identical to the batch 1b
finding (`fable_batch1b.md:31-33`, reach via a MODE SELECT block size or the tape 24-bit count).  The draft wrote
"DUPLICATE-OF-ROW scsicapnosense", which is not a menu form and names a row that does not exist at HEAD; the
disposition is the job:F form.  Seagate citation not checked (no local copy); the source contradiction stands
alone.

diskimagescsicmd:F4 | CONFIRMED-FILED ovsync
Checked: `diskimage.h:254` SYNCHRONIZE CACHE is 0x35; the only case is `:915-938`; `:1380-1384` `default:` sets
no status; `dev_asc.c:1284-1287` substitutes 0x00 (GOOD) for an absent status.  OUTSTANDING_BUGS.md@db8b1a33:
1271-1277 names "SYNCHRONIZE CACHE(16) `0x91` is undefined ... a guest gets GOOD with overlay and bitmap still
unflushed" and the closure condition.

diskimagescsicmd:F5 | DUPLICATE diskimage:F5  (`lbsmask`; rider: READ TRACKINFO `:1224-1226` is a sibling site)
Checked: `:1319-1324` accepts 257; `diskimage.c:305-307` masks; `:1224-1226` repeats the mask.  516,096 / 257 =
2,008 r 40; `40 & 256 == 0`; stored 2,008, ceiling 2,009.

diskimagescsicmd:F6 | RECORD-L4 "That defect is fixed separately -- this guard stops the 0 - 1 underflow regardless of how the disk got to zero blocks, and it stays correct after that fix lands.  Note what it does NOT do: READ CAPACITY(10) has no encoding for 'no blocks', so an empty disk still answers GOOD with last-LBA 0, i.e. it reports ONE block (CHANGELOG #412: 'a successful, inherently ambiguous zero')."
Checked: `:507-510` says "this guard is what makes an empty disk report itself as empty"; with
`nr_of_logical_blocks < 1`, `:551-552` sets `size = 0`, `:556-559` emit last-LBA 0 and `:561-564` block length
512, `:566` GOOD -- one block, not none.  CHANGELOG.md:27129 (db8b1a33:27213) already records the ambiguity; the
comment does not.  Replace `:507-510` (the sentence beginning "That defect is").

diskimagescsicmd:F7 | RECORD-L4 "The two halves are inseparable for the failures this helper reports: a CHECK CONDITION whose sense carries nothing -- key NO SENSE, no ASC/ASCQ, no FILEMARK/EOM/ILI bit -- tells the guest that something failed and then that nothing is wrong, which is not a state it can act on.  (Key NO SENSE with FILEMARK set is a defined, actionable pairing: the tape READ's feof branch below returns it, and REQUEST SENSE reports byte 2 = 0x80.)  Latching here is what makes the status meaningful."
Checked: `:203-206` is a blanket claim; `:799-809` quotes the standard's filemark rule and sets status 0x02 with
`d->filemark = 1`, and `:993-995` reports `data_in[2] = 0x80` (FILEMARK, key nibble NO SENSE).  The comment's
warrant for the helper is right; its generalisation is contradicted three hundred lines down in the same file.
The draft's text is equivalent; mine keeps the helper-scoped sentence first, because that is the part a future
editor must not break.  Seagate Table 28 not checked (no local copy).

diskimagescsicmd:F8 | RECORD-L4 "**Not fixed here, filed:** the ordering `continue` has no gate row (it needs fault injection) *[built by `e051fc5` (`m437ord`): `diff_diskimage_sync.c`'s two-overlay `failure skips only ITS OWN bitmap` row with its disarmed control, gated in `gate_offline.sh`]*; a multi-overlay disk reports CHECK CONDITION ..." (the rest of the list unchanged)
Checked: CHANGELOG.md:25618 (db8b1a33:25702) is stale, not wrong when written: `regress/diff_diskimage_sync.c:
600-603` asserts `F(d0) S(d0) F(d1) S(d1) F(b1) S(b1)` on an injected d0 failure, `:625-628` is the disarmed
control, `gate_offline.sh:1991-2010` gates the row by value; OUTSTANDING_BUGS.md@db8b1a33:5797-5801 records
`m437ord` "BUILT AND SHIPPED in `e051fc5`".  A dated in-place bracket rather than a rewrite, per the fork's
quote-what-you-refute rule; the draft's rewrite drops the original sentence.

diskimagescsicmd:F9 | TEST-GAP-FILE modeselectrow
Checked: CHANGELOG.md:20546-20547 (db8b1a33:20631-20632) names "a complete one still does" as the gate that
proves #285's set-then-compare form.  Census of committed non-artifact `regress/` for MODE SELECT: the hits are
in unrelated probes (`diff_m8820x.c`, `pcc2_width_probe.py`, ...); no `diff_diskimage_*.c` row issues opcode 0x15
against `diskimage_scsicommand()`, so neither the partial-refusal nor the complete-acceptance behaviour is
pinned.  LOW.

diskimagescsicmd:F10 | TEST-GAP-FILE scsicaprow
Checked: `regress/diff_diskimage_parse.c:195-215` asserts `d->nr_of_logical_blocks` immediately after
`diskimage_add()` and never issues READ CAPACITY, so the second recalc at `diskimage_scsicmd.c:489` is unobserved
-- which is how F2 shipped past a row named "advertised blocks exact" whose comment (`:204-212`) says "Only this
row fails on that variant".  OUTSTANDING_BUGS.md@db8b1a33:5234-5238 already says every parse.c row "asserts the
PARSER's output ... That needs a call-site row or a booting rig" -- an "assessed, not changed" limitation note,
which is the gap stated, not the gap filed.  The row is discharged by `drecalccap`'s detector (a READ CAPACITY
after `d:`-add on the four floppy sizes).  LOW.  Rider: the row label "advertised" names the guest-visible count,
which is 3,024, not the 2,880 it asserts -- qualify it when the row lands.

======================================================================================================
(a)  CODE findings I could NOT confirm as stated
======================================================================================================
None refuted; all 11 CODE findings that reached a source check trace as written.  Qualifiers that a filing
should carry:
* devasc:F1 -- the process kill is the DEC arm (`:662-665`); on PICA the jazz callback's `(int32_t)len` guard
  turns the negative count into a zero move and the guest survives.  The finding says "reaching memcpy", which is
  the DEC arm, so this narrows the machine set, not the claim.
* devasc:F3 -- the TEST UNIT READY outcome needs `cmd_len` >= the group length (`diskimage_scsicmd.c:309-316`);
  a DMA count below 6 is rejected as a short CDB instead (still wrong, differently).
* diskimage:F3 -- "upper half" is exact for cylinder-aligned sizes only (the draft's qualifier).
* bundle_file:F1/F2 -- the input class (command-line file or boot-block-extracted loader) is stated above; HIGH
  by the rule's letter and the fork's own src/file precedent, not by a measured guest witness -- none was run.
* Every external hardware-manual citation (LSI 53CF92A pages, Seagate SCSI commands reference) is UNCHECKED:
  `_scratchpad/` holds no 53C94 or SCSI command-set text.  Each finding that cites one also stands on a source
  contradiction, and I ruled on the source.

======================================================================================================
(b)  What I noticed that Astra did not (mine)
======================================================================================================
* `drecalccap` (diskimage:F2) has THREE triggers, not one: `diskimage_recalc_size()` is also called by READ
  SUBCHANNEL / READ CD CAPACITY (`diskimage_scsicmd.c:1139`) and READ TRACKINFO (`:1222`).  The fix must cover the
  helper, not the READ CAPACITY arm.
* `stalelbsbound` (diskimage:F3): the same three commands are the only refreshers, so a fix that recalculates at
  `:1324` is one line and removes the dependence on which command the guest happens to send next.
* `ascpiozero` (devasc:F4) has a sibling in the same round: the PIO DATA_OUT stub at `dev_asc.c:573-574`
  (`fatal("TODO...")`, moves nothing) falls through to `:850-854`, whose `diskimage_scsicommand()` re-issue meets
  the `data_out_offset != size` gate and returns 2 again -- inert rather than wrong, so it belongs in the same
  row as a LOW sibling, not its own.  REVIEW_FINDINGS.md:965-966 already names both stubs together.
* `ascoutresid` (devasc:F2) design note for the fix round: `:707`'s comparison against the CLAMPED count is a
  MEASURED choice (#283 fault injection: comparing against the programmed count fires on a benign re-entry);
  the repair is the report at `:755-761` only -- residual = programmed minus what this transfer moved, TC only
  at zero, the #281 shape.
* Checked and NOT new: the MB89352 route where a return-2 CDB leaves `data_out == NULL`, `data_out_len` nonzero
  and `transfer_bufpos` un-reset, re-armed by a TC write -- I traced it independently from `dev_mb89352.c:275-285`,
  `:637-650`, `:661-665` and then found it is sequence (i) of batch 2d's `mboutcapacity`.  Recorded so the next
  reader does not re-derive it.
* The `diff_diskimage_parse.c:214` row label ("advertised blocks exact") and its comment `:204-212` are a records
  defect in the detector itself, rider on F10 above: the row pins the PARSER's count, and the ADVERTISED count is
  what F2 shows to be wrong.

======================================================================================================
(c)  DENOMINATOR
======================================================================================================
29 of 29 findings checked against the source, committed regress code or records at `8ea26abb` (records also at
`db8b1a33`); 0 of 29 ruled on from Astra's text alone.  Breakdown: bundle_file 3/3, devasc 7/7, diskimage 9/9,
diskimagescsicmd 10/10.  All 29 were also cross-checked against DISPOSITIONS.md (batches 1a, 1b, 2a, 2b and the
2026-09-28 corrections) and against `fable_batch2c.md` / `fable_batch2d.md`, which DISPOSITIONS.md does not yet
carry; that is where the two cross-batch duplicates came from.  External manual citations: 0 of 29 checked (no
local copies).  Proposed ids: all 12 new/gap ids grepped absent from OUTSTANDING_BUGS.md at HEAD and from
DISPOSITIONS.md; the three existing ids (`lbsmask`, `ovsync`, `m437ord`) found at the lines cited.

======================================================================================================
Draft dispositions changed, and why
======================================================================================================
* diskimagescsicmd:F1  NEW HIGH `modeselectbuflen` -> DUPLICATE bundle_devices1:F1 (`mboutcapacity`, batch 2d).
  The draft's duplicate search covered OUTSTANDING_BUGS.md, DISPOSITIONS.md and this batch's answers; batch 2d's
  ruling is in `adjudication/fable_batch2d.md` and not yet in DISPOSITIONS.md.  Same controller weakness; a second
  disk-layer site is a rider, not a row.  Net: -1 new, +1 duplicate.
* diskimagescsicmd:F3  "DUPLICATE-OF-ROW scsicapnosense" -> DUPLICATE bundle_include1:F5.  Not a menu form, and
  `scsicapnosense` is a pending filing from batch 1b, not a row at HEAD (0 hits).  Category unchanged.
* diskimagescsicmd:F10  "FILED-BY-PROSE OUTSTANDING_BUGS.md:5234-5238" -> TEST-GAP-FILE `scsicaprow`.  That
  passage is an "assessed, not changed" note that itself says a row is needed; a note that names an owed row is
  the gap, not its filing -- the batch 2a precedent (prose WITHOUT an id is FILED) is about DEFECT entries, and this
  is neither a defect entry nor a row.  Net: -1 filed, +1 test-gap.
* devasc:F4  category kept (NEW MED); the draft left REVIEW_FINDINGS.md:965 unchecked -- checked, it records the
  stub, and the id is assigned to that acknowledged limitation with the PIO DATA_OUT sibling folded in.
* diskimage:F5  the draft's "MED under this brief's rule, although recorded LOW" is recorded here and NOT applied;
  CONFIRMED-FILED keeps the row's grade.
* Replacement texts rewritten: devasc:F5 (the draft's omits that the epilogue forces PHASE_STATUS and that the
  tick asserts the line -- the two facts the latch rationale now rests on), diskimage:F7 (keep the measured "NOT
  dead" sentences), diskimagescsicmd:F7 (helper-scoped sentence first), diskimagescsicmd:F8 (dated in-place
  bracket instead of deleting the refuted sentence).
* Everything else: the draft's dispositions stand, each re-checked at the lines above.
