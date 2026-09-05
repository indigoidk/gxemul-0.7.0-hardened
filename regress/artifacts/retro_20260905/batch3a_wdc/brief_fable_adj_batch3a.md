# FABLE 5.1 ADJUDICATION -- RETROSPECTIVE BATCH 3a (the seven older dev_wdc.c corrections, #337..#464), 2026-09-05

Liveness: open your answer with the token FABLE_ADJ_B3A_20260905 and a VERBATIM quote of the first line of
`C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\retro_batch3a_wdc\codex.txt` (prompt delivery and file access proven, not assumed).

## CONTEXT AND VOCABULARY
This is an ordinary software-correctness review of an open-source machine emulator (GXemul 0.7.0, a hardened fork) and its
IDE/ATAPI disk-controller model, `GXEMUL-SEC/src/devices/dev_wdc.c`.  The "guest" is an operating system running inside the
emulator.  Use plain engineering vocabulary: "the emulator process exits", "a stale byte is returned", "an index outside
the array".

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY
A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly.  Check the premises, not just
the derivations -- open the files; a seat that re-derives a fact from something this brief did NOT give it outranks one that
agrees.  THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/` (HEAD 99b92f9).  `C:\DocumentNoSnc\CC\GXEMUL\src\` is pristine 2021
upstream, NOT this fork -- if your line numbers disagree with the ones below by hundreds you are reading it.

READ-ONLY.  Never write to GXEMUL-SEC/, build/, est/, build-asan/ or /tmp/gxsec-build; do not build anything (codex jobs are
running and a build would contend).  Return your whole answer as TEXT in your final message -- the harness blocks seat file
writes; the main loop preserves it.

## YOUR HAT
This is the ADJUDICATION of a retrospective review, not another review.  The owner asked (2026-09-04) that previously
shipped corrections be re-checked by GPT-6 Astra at max effort and adjudicated by Fable 5.1.  Astra's batch-3a answer is
inlined below in full (17,151 bytes; `tokens used 351,627`).  Decide, per finding: DEFECT (becomes a queue row -- give id,
severity, witness shape, option set), RECORD (L4, corrected in place -- give the exact sentence and the correction), FILE
(coverage debt -- give the row id and rank), or DROP (with the measurement or reading that kills it).  Anything checkable in
under two minutes gets CHECKED, not judged.

## THE SEVEN COMMITS
| sha | round | subject (neutral paraphrase) |
|---|---|---|
| 052982a | #337 | four `exit(1)` calls in the IDE controller model became latched `fatal()` declines |
| c941fe3 | #341 | the ATAPI read accounted for bytes it never delivered |
| 2e709cd | #405 | ATA IDENTIFY packed its capacity bytes with `% 255`, not `& 255` |
| 085766a | #407 | #405's detector had four holes and a note that was wrong the flattering way |
| e86e293 | #408 | a citation-fixing round repeated the error; the detector relied on -O2 to hide undefined behaviour |
| 154d21c | #414 | every `-d g` disk and every floppy reported zero capacity (the executable fix is in `src/disk/diskimage.c`) |
| baacf9b | #464 | six unlatched `fatal()` calls bounded, and the detector's first gate |
`git -C GXEMUL-SEC show --format= <sha> -- <file>` gives a diff without the message; `git show --format=%B <sha>` the message.
CHANGELOG blocks (newest at the TOP of `GXEMUL-SEC/CHANGELOG.md`): `Seventieth round, part C` (#337),
`One-hundred-and-forty-fifth round` (#405), `One-hundred-and-forty-seventh round` (#407), `One-hundred-and-forty-eighth
round` (#408), `One-hundred-and-fifty-fourth round` (#414), `^## Round 464`.  #341's record is in `OUTSTANDING_BUGS.md`
(anchor `#341: dev_wdc's ATAPI read`).  No ATA/ATAPI standard is on disk.

## WHAT THE MAIN LOOP ALREADY CHECKED (each is a QUESTION if you can re-derive it)
1. **#341 odd-tail read (Astra's DEFECT).**  `dev_wdc.c`, `static uint64_t wdc_get_inbuf(struct wdc_data *d)`: on an EMPTY ring
   it latches a fatal() and `return (uint64_t) -1;`.  The data-port read (anchor `case wd_data:	/*  0: data  */`) assembles:
       LE:  odata = wdc_get_inbuf(d); if (len >= 2) odata += (wdc_get_inbuf(d) << 8); ...
       BE:  odata = wdc_get_inbuf(d); if (len >= 2) odata = (odata << 8) + wdc_get_inbuf(d); ...
   Main-loop arithmetic for a 2-byte read with ONE valid byte 0x23 left: LE gives 0x23 + (0xffff...ff << 8) = 0x...ff23 ->
   low 16 bits 0xff23 -> the guest's byte 0 is 0x23 (valid byte intact, padding 0xff).  BE gives (0x23 << 8) +
   0xffffffffffffffff = 0x22ff -> the guest sees 0x22, 0xff: **the valid byte itself is corrupted (0x23 -> 0x22)**.  Astra
   wrote 0x23ff; the value differs, the conclusion (BE corrupts the valid byte) holds and is if anything worse.  CHECK the
   arithmetic yourself, and check whether `memory_writemax64` (src/core/memory.c) writes the low `len` bytes of `odata`.
   Reachability: odd payload lengths come from the SCSI backend (INQUIRY returns odd lengths); a big-endian machine with this
   controller exists (`machine_evbmips.c` "MALTA (evbmips, big endian)" via `bus_pci.c` `PCIINIT(piix4_ide)`).  OpenBSD/NetBSD
   ATAPI drivers read the data port 16 bits at a time, so a 5-byte tail at the end of an INQUIRY is the realistic case.
2. **#337 packet failure status (Astra's DEFECT).**  `d->error = 0` at the top of `wdc_command()`; ABRT is set at several
   arms (`d->error |= WDCE_ABRT` x5 by grep); `status_byte()` ORs `WDCS_ERR` when `d->error` is set.  Astra's claim is that
   the ATAPI PACKET path ignores `atapi_st->status` (a CHECK CONDITION returned with `res == 1` by `diskimage_scsicommand`)
   and completes with status 0x50 (DRDY|DSC) and the error bit CLEAR, so a failed SCSI command reports success.  CHECK where
   the packet-completion path sets status/error, and whether `atapi_st->status` is consulted anywhere in dev_wdc.c.
3. **#464 census.**  `grep -c 'fatal('` = 19 and `grep -cE '\bexit\('` = 8 in dev_wdc.c TODAY -- those counts include
   COMMENTS; Astra's executable census is 13 fatal() and 0 exit().  Derive the executable count (strip comments) if you rely
   on it; the gate's fatal-call floor is 12.
4. **#407's totals.**  `CHANGELOG.md` anchor `built and ran **133 mutants**` vs the result line `90 detected, 17 no-op, 15
   survivors, 1 build failure` = 123.  Confirmed: ten unaccounted for.
5. **Astra corrected three brief premises**: #337 and #341 shipped NO dedicated detector; #341's record lives in
   OUTSTANDING_BUGS.md; #414's executable fix is in `src/disk/diskimage.c` (its dev_wdc.c hunk is commentary).  Treat as
   settled unless you find otherwise.
6. **Astra consulted an ONLINE T13 draft (ATA-d1410r3a)** for packet error signalling and word-49 bits.  The project's rule:
   a web source is not the manual; nothing on disk covers ATA.  Say whether any disposition below DEPENDS on that draft, and
   if so mark it BELIEVED rather than CONFIRMED.

## ASTRA'S ANSWER, VERBATIM (codex.txt)
052982a (#337): **DEFECT** — host exits are gone; packet failures can still complete without an error indication.  
c941fe3 (#341): **DEFECT** — accounting holds, but big-endian odd-tail reads corrupt a valid payload byte.  
2e709cd (#405): **RECORD** — packing holds; arithmetic-domain and survivor claims need correction in place.  
085766a (#407): **RECORD** — detector improvements hold; mutant totals and surviving descriptions disagree.  
e86e293 (#408): **RECORD** — CPU fixture repair holds; WDC MODE SELECT reachability is falsely asserted.  
154d21c (#414): **DEFECT** — geometry calculation holds; cylinder truncation remains live and was already disclosed.  
baacf9b (#464): **RECORD** — warning bounds hold; detector coverage and source descriptions remain overstated.  
BATCH: **DEFECT** — residual packet-status and payload defects remain; C/emulator checks were not run. A measuring seat should build both differentials and run the offline and SH gates.

I read the complete brief and reviewed only `GXEMUL-SEC/`, at HEAD `2bb9cb47ef191c1337ef3ae857fb205782692950`. No files were changed. Numerical results below come from enumeration; archived results were checked separately. Detector escapes are source-derived findings, not freshly measured mutant results or claims about the entire boot battery.

Three brief premises need correction: #337 and #341 shipped no dedicated detector; #341’s record is in `OUTSTANDING_BUGS.md`; and #414’s functional fix is in `src/disk/diskimage.c`—its `dev_wdc.c` change is commentary.

References to WDC constructs below mean [dev_wdc.c](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/dev_wdc.c). Detector function anchors refer to [diff_wdc_identify.c](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/diff_wdc_identify.c). Record-heading anchors refer to [CHANGELOG.md](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/CHANGELOG.md). The supplied anchors were checked for uniqueness in their named files.

1. **052982a / #337**

   All four executable aborts remain removed: both data-write width defaults, rejected SCSI dispatch, and DATA OUT. Later #478/#479 strengthened declined-access handling and reset command state; #495 now suppresses DATA OUT writes because that transfer path remains unimplemented.

   The recovery is incomplete. `wdc_command()` clears `d->error`; the rejected-command branch completes and interrupts without setting it. WDC also ignores `atapi_st->status`, including backend CHECK CONDITION results returned with `res == 1`. With an attached medium and an empty completed transfer, `status_byte()` consequently returns **0x50 with the error bit clear**. This is a source-derived guest-visible consequence, not a measured emulator result. The backend evidence is [diskimage_scsicmd.c](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/disk/diskimage_scsicmd.c), unique anchor `SCSI READ: refusing oversized transfer`.

   The current offline gate is [gate_offline.sh](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/gate_offline.sh), anchor `^WDCBIN=`. Relevant detector anchors are `^static void row_badlen_no_dispatch`, `^static void row_little_endian_arm`, and `^static void row_pkt_cdb_accept`. The packet row observes dispatch, not failure status. Its SCSI stub—anchor `^int diskimage_scsicommand`—returns only 0 or 1. **A regression confined to the DATA OUT return path is therefore unobserved.**

   The record at `Seventieth round, part C` honestly says the original fix was argued from reachability and had no asserting row. Its claim that completing and interrupting describes how a real drive reports failure omits the required error indication. Also, unsupported commands do not uniformly take the backend’s `res == 0` path.

2. **c941fe3 / #341**

   The requested-length accounting bug remains repaired, with #475’s additional remainder clamp. Enumerating handler widths **1–8** gives pop counts **1, 2, 2, 4, 2, 2, 2, 2**; accounting uses the lesser of that count and the remaining transfer. Thus widths 3 and 8 both pop two bytes—the retained “1 or 2” description is inaccurate. #473 changed chunk refill; #476/#477 added transfer and phase guards.

   **The original width distinction is still unpinned.** Every DATA-read call site in the offline differential uses width 2 or 4. Substituting requested-length accounting while retaining the remainder clamp therefore leaves those rows unchanged. Anchors `^static void row_odd_step`, `^static void row_odd_midwalk`, and `^static void row_odd_width` pin later odd-remainder behavior, not #341’s distinction at widths 3 and 8.

   There is also a live payload defect. `wdc_get_inbuf()` returns unsigned −1 when empty; the big-endian assembly adds that value without reducing it to a byte. The existing `row_odd_width` fixture queues **0x24** as its final valid byte and performs a two-byte read. WDC computes **0x23ff**: real big-endian conversion delivers **0x23**, corrupting the valid byte. The row checks counters only. Its conversion stub also always serializes little-endian.

   The real conversion is [memory.c](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/core/memory.c), anchor `^void memory_writemax64`. Odd payload lengths are produced by the backend’s `case SCSICMD_INQUIRY:`. A real big-endian WDC configuration exists through [machine_evbmips.c](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/machines/machine_evbmips.c), anchor `MALTA (evbmips, big endian)`, and [bus_pci.c](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/bus_pci.c), anchor `^PCIINIT(piix4_ide)`.

   The historical record is [OUTSTANDING_BUGS.md](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/OUTSTANDING_BUGS.md), anchor `#341: dev_wdc's ATAPI read`. Its later `wdcletwins` entry already acknowledges missing read-byte assertions; the unique anchor is `the endianness coverage residue, both arms of the read path`. The concrete corruption above gives that coverage gap a measurable consequence.

3. **2e709cd / #405**

   The six `% 255` replacements remain correct. The other two capacity-byte assignments already used masks. Enumeration produced these examples:

   | Sector count | Old decoded count | Fixed decoded count |
   |---|---:|---:|
   | `0x0000FF00` | 0 | 65,280 |
   | `0x00010000` | 65,792 | 65,536 |
   | `0x12345678` | 306,617,464 | 305,419,896 |
   | `0xFFFFFFFF` | 255 | 4,294,967,295 |

   Walking the **shipped** self-consistency domain—H=15, S=63, C=1…2000—gives **1,931 disagreements, first at C=70**. Walking the current default-geometry domain—H=16, S=63, C=1…65535—gives **65,471, first at C=65**. The original record attributed the latter result to a loop that implemented the former.

   The producer domain has also changed. At HEAD, #414 permits H=S=1, so **65,280 sectors at 33,423,360 bytes is reachable**. The retained assertion that this exact boundary is unreachable is false at HEAD; the stated 33,546,240-byte first divergence applies to default 16/63 geometry.

   Gate anchors are `wdc IDENTIFY: the >>24 threshold row is present` and `wdc IDENTIFY: the packing anchor is present`. The literal boundary rows detect each direct restoration of the six old modulo operations. `^static void row_anchor` supplies an independent word-53 check; `^static void row_selfconsistent` is relational, but **the whole detector is not merely a round-trip oracle**.

   The remaining effect-level escape is IDENTIFY transport ordering: exchanging its two enqueue operations corrupts guest-delivered words while preserving the directly inspected structure. `^static void row_command_fills_ring` checks occupancy, not delivered IDENTIFY bytes.

   At record anchor `One-hundred-and-forty-fifth round`, the original “known survivor” paragraph remains wrong despite later correction. Swapping capacity packing is observed by the capacity rows; word 53 does not detect a capacity-only swap because that mutation leaves word 53 untouched. The explanation that the low-byte *operand* is already one byte is also wrong—the result is masked.

4. **085766a / #407**

   This commit improved the detector and comments, not executable product behavior. Its slave and capability rows remain useful; the widened cylinder sweep closes the earlier 2000-cylinder limit. #408 subsequently strengthened slave geometry checks, and #409/#410 extended identity and ATAPI coverage.

   Gate anchors are `wdc IDENTIFY: the slave-drive row is present`, `wdc IDENTIFY: the word-49 capability row is present`, and `wdc IDENTIFY: the oracle sweeps the full 16-bit range`. Detector anchors are `^static void row_slave`, `^static void row_no_lba_claim`, and `^static void row_selfconsistent`. These observe the originally identified drive-selection, capability-byte, and cylinder-truncation regressions. The IDENTIFY transport-order escape described for #405 remains outside their assertions.

   At `One-hundred-and-forty-seventh round`, **133 mutants** does not reconcile with **90 detected + 17 no-op + 15 survivors + 1 build failure = 123**. Ten results are unaccounted for; this is not evidence that precisely 123 mutants actually ran.

   The editable gate comment still says “three rows added”; the commit added two and widened one. The detector’s capability-row comment still describes setting the low byte to 2 as advertising LBA. Its internal word value is **0x0002**, whereas the LBA bit is **0x0200**. Later corrections did not remove these surviving statements. I found no additional product defect specific to this detector-only change.

5. **e86e293 / #408**

   Providing an actual CPU whose `machine` pointer is valid fixes the NULL dereference independently of optimization. #409 subsequently moved the large initialization to first use and strengthened identity stubs; those later changes must receive credit. The current gate builds at `-O2`, so it does not itself preserve the recorded five-optimization-level check.

   Gate anchor `wdc IDENTIFY: the base_drive row is present` connects to `^static void row_base_drive`; `^static void row_slave` and `^static void row_identity` cover related selection behavior. A small surviving argument regression is selecting the wrong disk bus type: the disk-image stubs still ignore `type`, so that distinction is absent from their oracle.

   The important false premise is at `One-hundred-and-forty-eighth round`: MODE SELECT’s accepted block-size range does **not** establish WDC reachability. Enumerating the three-byte field gives **7,937 accepted values, 256…8192**, in the shared backend. But its `case SCSICMD_MODE_SELECT:` requires a completed 12-byte DATA OUT transfer. WDC neither fills that buffer and advances its offset nor re-enters the backend; #495 now declines those writes explicitly. WDC initialization supplies a 512-byte logical block size, and this packet route cannot change it.

   The claim that every citation in both files and CHANGELOG now names constructs is also false: old numeric citations remain in the #405 block and detector commentary. The fixture repair holds; these are record and coverage defects, not an additional live product defect introduced by this commit.

6. **154d21c / #414**

   The executable repair in [diskimage.c](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/disk/diskimage.c), anchor `^bool diskimage_recalc_size`, survives. Floppy SPT derives from byte size, and cylinder calculation now runs for overrides too. Later #416/#418 changed backing-file handling and override behavior without undoing this calculation.

   I enumerated all **65,025 legal H/S pairs**; the largest cylinder divisor is **33,292,800 bytes**. Concrete geometry results include:

   | Input | Result C/H/S | Logical blocks |
   |---|---|---:|
   | 40,960-byte floppy | 40/2/1 | 80 |
   | 39,424 bytes, H=7/S=11 | 1/7/11 | 77 |
   | 39,425 bytes, H=7/S=11 | 2/7/11 | 154 |
   | 1,474,560 bytes, H=3/S=7 | 138/3/7 | 2,898 |

   For the small floppy, enumerating all 80 CHS sector positions gives 80 distinct starts from 0 through 40,448; the last byte is 40,959. The four documented floppy sizes yield SPT **9, 15, 18, 36**.

   Gate anchors are `^GEOMLOG=` and `disk geometry: row failures`. In [diff_diskimage_geom.c](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/diff_diskimage_geom.c), unique anchors `override EXACT does not round up` and `override non-integral rounds up` pin the rounding boundary. There were 34 rows at shipment; the current detector has 35. Its tuples are independent expected values.

   A small parser escape remains: changing heads parsing to unsigned conversion is not observed by the negative sign-wrap case, which tests SPT only. Separately, `^#ifdef GEOM_ROW_LBS257` identifies an explicitly disabled residual test.

   **The disclosed live narrowing remains:** an accepted 32-MiB image with H=S=1 produces **65,536 cylinders**, but WDC encodes IDENTIFY word 1 as **zero**, while its capacity remains 65,536 sectors. The detector’s cylinder sweep stops at 65,535. Retain this as the existing disclosed item.

   At `One-hundred-and-fifty-fourth round`, bounding H×S×512 does not bound the final cylinder multiplication against overflow; the original universal claim survives beside a later limitation. The detector comment at `honouring the override redescribes` also still says an override never resizes capacity. The final table row above disproves that generalization.

7. **baacf9b / #464**

   All six warning latches remain effective. Later #484 added pre-store ring refusal and another guarded overrun diagnostic; #485 corrected interrupt placement; #486 replaced the invalidated overrun stimulus; #492 strengthened the census.

   The executable WDC census at HEAD is **0 `exit()` calls, 13 `fatal()` calls, 0 unlatched `fatal()` calls**. There are two calls each behind `warned_badlen` and `warned_inbuf_overrun`, and one each behind `warned_atapi_err`, `warned_atapi_dataout`, `warned_inbuf_overread`, `warned_unimpl_cmd`, `warned_nonbyte_write`, `warned_nonbyte_read`, `warned_data_unexpected`, `warned_null_xfer`, and `warned_empty_drain`. These fields have no runtime clearing assignments. `fatal()` logs and returns; see [debugmsg.c](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/core/debugmsg.c), anchor `^void fatal`.

   [gate_sh_rounding.sh](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/gate_sh_rounding.sh) anchors are `wdc_flood rows correct` and `wdcflood: every latch BALANCED`. In [wdc_flood_probe.py](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/wdc_flood_probe.py), row anchors include `^row("unimpl x2"`, `^row("overread x2"`, `^row("w16 x2"`, `^row("r16 x2"`, `^row("datawr x2"`, and `^row("overrun x2"`. The read-only [census](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/wdc_latch_census.py), anchor `WDC_LATCH_BALANCED=%d`, reports SET=6, READ=6, BALANCED=6, DECL=11.

   Its known coverage escape remains: the repeated-warning cases do not interpose sector-register writes, and the census does not reject latch-clearing assignments. Thus a regression resetting a latch at that transition escapes these checks. Also, the fatal-call floor remains 12 while HEAD contains 13; it cannot establish that every diagnostic retained its channel.

   At record anchor `^## Round 464`, preserved evidence is substantially stronger than for the earlier rounds: I reconciled **39 raw result logs**, including 27 mutant logs across five tables. The [26-row baseline](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/wdcflood/table5_indep/probe_base26.raw), anchor `^WDC_FLOOD_RESULT=26/26`, agrees internally.

   Remaining overclaims are concrete: `fire3` cannot detect every repeat period greater than one; three firings cannot expose the first repeat at firing four. `runloop` prints a completion register but does not score it. The probe’s all-stepped/channel description is stale after the free-running overrun row. WDC’s consumer comment still describes full/empty ambiguity that #484 removed. I found no remaining unbounded WDC `fatal()` site.

No ATA standard was on disk. I checked an online **T13/1410D revision 3a working draft**, not a published final standard. ATA/ATAPI-6 §8.23.6 settles packet error signalling—extracted text 7685–7712—and §8.15.24 settles word-49 bits—6101–6104. Its §§8.15.10 and 8.15.27 mark the legacy cylinder/current-CHS fields obsolete. Their historical architectural meaning needs **ATA/ATAPI-4, IDENTIFY DEVICE information and field-validity subsections**; arithmetic consistency alone does not establish that conformance. [ATA/ATAPI-6 draft](https://pdos.csail.mit.edu/6.828/2005/readings/hardware/ATA-d1410r3a.pdf)

I did not locate backing artifacts under `regress/artifacts` for #407’s 133-mutant total or #408’s optimization measurements, and did not authenticate the earlier runtime claims by rerunning them. A measuring seat should build the current **128-row WDC differential** and **35-row geometry differential**, repeat the WDC optimization sweep with sanitizers, and run `gate_offline.sh` and `gate_sh_rounding.sh`. The missing assertions are packet error status, unusual-width accounting, actual payload bytes on both endian paths, and the disclosed cylinder boundary.


## QUESTIONS
Q1 THE #341 BE ODD-TAIL DEFECT.  Confirm or refute by reading `wdc_get_inbuf` and the `case wd_data:` read assembly, and
   `memory_writemax64`.  If confirmed: (a) queue id + severity against the live queue head (OUTSTANDING_BUGS.md "OPEN LIST")
   -- a guest-visible data corruption on BE machines only; (b) the WITNESS shape: is a rung-3 cold-debugger probe possible on
   a committed BE machine with this controller (which machine, which command produces an odd tail -- INQUIRY? -- and what a
   16-bit data-port read returns pre-fix vs post-fix), or does the differential (`diff_wdc_identify.c`, whose conversion stub
   Astra says always serialises little-endian) have to grow a BE arm; (c) the OPTION SET: mask the empty-ring return to a
   byte (`& 0xff`) at the assembly, return 0 from `wdc_get_inbuf` on empty (changes the LE padding byte too -- say what real
   hardware returns past the end of a PIO transfer and whether anything on disk settles it), or pad per the byte count.
Q2 THE #337 PACKET-STATUS DEFECT.  Confirm or refute: does a rejected/failed ATAPI command complete with the error bit
   clear?  Read `status_byte()`, the PACKET/`wdc_command` completion arms, and where `atapi_st` is consumed.  If confirmed:
   id, severity (a guest driver retries or trusts a failed command -- name the consequence), witness shape (a rung-3 probe
   issuing a packet command the backend refuses and reading the status register), option set (set `WDCE_ABRT`/CHK on
   `res == 1`; mirror the backend's CHECK CONDITION into the ATAPI error register), and whether this DEPENDS on the online
   ATA draft (mark BELIEVED if so).
Q3 THE #414 CYLINDER TRUNCATION.  Astra says it is DISCLOSED already (an accepted H=S=1 32-MiB image gives 65,536 cylinders
   and IDENTIFY word 1 encodes zero; the detector sweep stops at 65,535).  Is there an existing row/queue item?  If yes:
   HOLDS with a pointer; if no: FILE (LOW) -- say which.
Q4 THE RECORD ITEMS -- verify each by opening the file; give the exact correction or DROP:
   (i) #405 block: the "known survivor" paragraph (capacity-packing swap vs word 53; the "low-byte operand is already one
   byte" explanation); the 33,546,240-byte first-divergence claim vs the reachable H=S=1 boundary at HEAD; (ii) #407 block:
   133 vs 123 mutants; the gate comment "three rows added" (two added, one widened); the capability-row comment about
   setting the low byte to 2 (internal word 0x0002 vs LBA bit 0x0200); (iii) #408 block: "MODE SELECT reachability" via the
   3-byte block-size field (7,937 accepted values) -- Astra says WDC never completes the 12-byte DATA OUT the backend's
   `case SCSICMD_MODE_SELECT:` requires, so the WDC route cannot change the block size; and "every citation now names
   constructs"; (iv) #414 block: bounding H*S*512 does not bound the final cylinder multiplication; the detector comment
   `honouring the override redescribes` says an override never resizes capacity (Astra's 1,474,560-byte H=3/S=7 row gives
   138/3/7 = 2,898 blocks); (v) #464 block: `fire3` cannot detect every repeat period > 1; `runloop` prints but does not
   score the completion register; the probe's all-stepped/channel description is stale after the free-running overrun row;
   dev_wdc.c's consumer comment still describes the full/empty ambiguity #484 removed; the fatal-call floor 12 vs 13;
   (vi) #341's retained "1 or 2" width description vs Astra's pop-count enumeration for widths 1..8 = 1,2,2,4,2,2,2,2.
Q5 THE DETECTOR RESIDUALS: #405's IDENTIFY transport-ordering escape (swap the two enqueues; `row_command_fills_ring` checks
   occupancy, not bytes); #408's disk-bus-type argument escape (stubs ignore `type`); #414's unsigned heads-parse escape and
   the `#ifdef GEOM_ROW_LBS257` disabled row; #464's latch-clearing-assignment escape (census does not reject `warned_* = 0`)
   and the missing sector-register interposition; #341's width-3/8 accounting unpinned.  Floor breach (which clause) or
   coverage debt to FILE?  Ids and ranks, below live defects.
Q6 UNVERIFIED MEASUREMENTS (#407's 133 mutants; #408's five-optimisation-level check -- the current gate builds at -O2 only).
   Disposition per the carrier's forward-only rule: annotate "artifact not located (retrospective review 2026-09-05)" or
   leave; rule with the reason.
Q7 WHICH OF THE MAIN LOOP'S PROPOSED DISPOSITIONS IS WRONG?  Proposed: Q1 -> new row `wdcbeoddtail`, HIGH (guest data
   corruption, BE machines); Q2 -> new row `wdcpktstatus`, MEDIUM (a failed command reports success); Q3 -> pointer or LOW
   file; Q4 (i)-(vi) -> L4 in place, one records commit; Q5 -> FILED under one id per detector (`wdcidentorder`,
   `wdcstubtype`, `wdcgeomparse`, `wdclatchclear`, `wdcwidth38`), LOW; Q6 -> annotated, not altered.  Name the wrong one(s)
   and why -- including any id you would MERGE with an existing row (grep the ledger ids: `python -c "import json;
   print([r['id'] for r in json.load(open('GXEMUL-SEC/tools/pipeline/ledger.json'))['rows'] if 'wdc' in r['id']])"`).

VERDICT LINE FIRST (one line per commit: HOLDS / DEFECT / RECORD, then a batch line), then Q1-Q7, then a NUMBERED
DISPOSITION LIST the main loop can file verbatim (id, severity, one-line title, witness shape, provenance = Astra batch 3a +
this adjudication).  Cite by grep anchor, not line number, except across files with the qualifier on the citation.
