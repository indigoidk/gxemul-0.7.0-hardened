# T4 `wdclbaaddr` pass-1 brief -- drafter's NOTES (inconsistencies and unsupported premises found while drafting)

Drafted 2026-10-24 against `GXEMUL-SEC` HEAD `cc1f69cc`.  Every claim below was checked by a command whose output is in
`C0_OUTPUT.txt` (same directory) or by reading the cited line at HEAD.  Items 1-5 are the ones I consider load-bearing for
the design; the rest are records nits, brief-construction notes and candidates for filing.  The brief carries each of
them as a premise (S#), a question (P#), a disagreement (D#), a cell/row/variant (C#/N#/V#) or a Q4 candidate.

## Load-bearing

1. **The detector's specified shape cannot be gate-wired, and its specified gate home does not exist.**  The design
   (DRAFTER_INPUTS item 2) and the witness brief specify "two legs in one invocation like `wdc_altoffset_probe.py`", and
   say "grep `regress/gate_*.sh` for `wdc_altoffset_probe` and put this probe beside it".  Measured: `wdc_altoffset_probe.py`
   runs in NO gate (it appears only in `gate_hygiene.sh`'s pty-probe census, :281 and :417); `check_probe_wiring.py`
   exempts it until 2026-11-05 as "two-leg differential; wants a single-leg mode before gate 10 can assert anything"
   (3301-3303), and the open row `wdcaltoffleg` owes those probes a single-leg form.  The frozen witness probe repeats the
   shape: leg `base` ALWAYS runs and is judged against the HEAD column (616-618), so gate 10's one post-fix binary would
   fail it.  The wired precedents are `wdc_altdigin_probe.py` (a `GATE` leg label, `gate_sh_rounding.sh` 1484, denominator
   pinned to 22 by equality at 1522-1523) and `#533`'s single-leg `landisk_aux_probe.py` (`check_probe_wiring.py` 643-654).
   Unless the probe gains a FIX-column-only mode, the round ships a third two-leg wdc differential and one more dated
   exemption.  (Brief: S16, S23, P7, D6, 7.7, Q3(b).)

2. **The "five rigs" census behind the word-49 decision is false.**  The main-loop position: advertising LBA would switch
   "every rig's guest" from CHS to LBA, "a guest-visible behaviour change on five rigs", and the follow-up's gate is "the
   five-rig boot battery".  Measured: PMAX, ARC, SGI, LUNA88K and MVME88K disks are SCSI
   (`get_default_disk_type_for_machine()`, `diskimage.c` 1701-1711), so the pmax, arc and luna88k rigs never reach
   `dev_wdc.c`.  The ONLY battery rig that does is landisk, and only when the OPTIONAL `_images/wdc-scratch-64m.img` exists
   -- "64 MiB of zeros" (`images.md` 139), attached `-d iR:` through an overlay (`drive_guest.py` 273-285) -- and its disked
   boot issues 3 READs and 1 READMULTI and no WRITE (`drive_guest.py` 89-99).  On an all-zero disk every sector reads
   alike, so no battery rig can observe a word-49 change at all: the proposed gate is non-discriminating, and the "cost on
   five rigs" side of the decision is not what the tree measures.  (S18, P5, P6, D7, Q3(a).)

3. **The LBA28 formula, enabled as written, overflows `int` for disks over 2 GiB -- and no source names it.**  The
   `#if 0` text (`dev_wdc.c` 472-474, 564-566) is `offset = 512 * (((d->head & 0xf) << 24) + (cyl << 8) + d->sector)`
   with every operand `int`: the product exceeds `INT_MAX` once the sum reaches 2^22 = 4,194,304 (undefined behaviour).
   The FreeBSD/DragonFly patch, B's recommendation 1 (the `|` form) and the design text all carry the same `int` product;
   the CHS line beside it already uses `(int64_t)` casts.  The pmax tree builds with `-O3` and no `-fwrapv`
   (`build/Makefile` 9), so the unwidened variant's behaviour is compiler-dependent: a wrapped product turns LBA
   16,777,221 into 2,560 bytes (LBA 5), a widened evaluation serves zeros.  It is the same class as `arcpartlba` ("the ARC
   partition LBA is multiplied by 512 in signed int and overflows").  (S6, P8, D2, V15.)

4. **A gate-2 row must be re-authored in the SAME change, and both files it lives in carry uncommitted peer hunks.**
   `regress/diff_wdc_identify.c` `#include`s `dev_wdc.c` (208); its `row_no_lba_claim()` (5606-5637) says "If LBA is ever
   implemented, this row must be re-authored in the SAME change", its FAIL text says "(0x200 = LBA, 0x100 = DMA -- neither
   is implemented)" and its warrant ("the LBA offset arms ... are `#if 0` ... d->lba ... never reaches an offset
   computation") becomes false.  `gate_offline.sh` pins the row by NAME (1895-1896) and its comment at 1890 reads
   "advertise LBA that is #if 0'd out".  The working tree holds +526/-29 uncommitted lines in `diff_wdc_identify.c` and
   +58/-3 in `gate_offline.sh` (other sessions), and gate 2 compiles the working-tree copy against the working-tree
   `dev_wdc.c` (1497-1499).  The design text does not mention this obligation; the commit must stage only this round's
   hunks (the `#533` precedent did exactly that for `gate_sh_rounding.sh`).  (S17, Q3(d).)

5. **"Keep the SDH read-back byte-exact" has no mechanism yet, and the witness rows cannot pin it.**  Today the four
   stored fields partition the byte (`dev_wdc.c` 2008-2009, 2014-2017).  Decoding `lba` from bit 6 while `sectorsize`
   keeps bits 7-6 holds bit 6 twice and bit 5 nowhere, so the read-back must be redesigned (raw byte, repurposed field,
   or a new bit) -- B and the main loop require the property and name no mechanism.  A new field is an addition under
   the licence rule.  Both witness read-back rows (0xe5, 0xb3) have bits 7 and 5 set, so a read-back that forces 0xa0
   passes both; a row with bits 7 and 5 clear (0x4c) is owed.  (S1, S4, D5, P13, V16-V18, N4, Q1(b).)

## Premises in the inputs that the tree does not support

6. **`& 0xf` dropped is EQUIVALENT, not "needs LBA >= 2^24".**  `d->head` is assigned only at `dev_wdc.c` 2017, as
   `idata & 0xf` (writer census in C0), so the mask in the LBA formula is redundant in every reachable state.  (S3, P9, V12.)

7. **`sectorsize` as "the pre-ATA WD1003 reading of bits 7-6" is unsupported.**  The fork's own header calls
   `WDSD_IBM 0xa0` "forced to 512 byte sector, ecc" (`wdcreg.h` 193), which reads as bit 7 = ECC and a size code in bits
   6-5 (01 = 512) -- a bits-7-6 field would match neither WD1003 nor ATA.  No WD1003 document is in `_scratchpad/`.  The
   field's only readers are the SDH arm's read-back and debug lines (reader census in C0).  (P2.)

8. **"Bits 7 and 5 are obsolete always-1 bits in ATA"**: the only ATA document on disk, the ATA-2 working draft, says
   "Bit 7 is reserved" and "Bit 5 is reserved" (`ata2_x3t10_948d.txt` 1605, 1610); "obsolete" is later-standard wording
   not checkable locally; driver practice (`WDSD_IBM` 0xa0, NetBSD `wdc.c` 1816) writes them as 1.  (S12, P1, D9.)

9. **"LATENT" rests on a host behaviour nobody here verified.**  ATA-2 1849-1851: "A host shall not attempt to use LBA
   addressing unless the device indicates the mode is supported"; NetBSD obeys (`wd.c` 394-395).  The only named host
   that does not -- FreeBSD 10+ -- comes from a 2013 ports commit message, and B's own limits say FreeBSD's ATA code was
   not re-read.  (P3.)

10. **`arcpartlba` is not a ledger row.**  The inputs list it among "Related rows by id (quote titles from
    `tools/pipeline/ledger.json`)"; HEAD's ledger has no such id.  `OUTSTANDING_BUGS.md` 24253: "named in this file only:
    no ledger row of its own"; 23432 lists it as a member of the class row `astraretrolow`.  Its own citation
    "OUTSTANDING_BUGS.md:2730-2731 at db8b1a33" now points at unrelated text (line drift).

11. **The research ruling calls a source reading a measurement.**  `ADJ_RULINGS.md` B: "Grok (the measurement above) says
    latent ... Grok's argument is the measured one"; its own header (4-5): "neither built or ran anything".  The LATENT
    conclusion stands on the source reading; the word does not.  (1.3, Q4 item 4.)

## The witness and its instrument (measured at 17:03-17:04, before any product edit)

12. **The witness exists and is valid at rung 3 for clause (i)'s first half** -- `RESULTS_base.txt` 19/19 against the
    HEAD column, sentinel `WDCLBA_PROBE_DONE`, `dev_wdc.c` md5 == HEAD.  The inputs said to inline "its RESULTS.txt"; the
    durable file is named `RESULTS_base.txt` (the probe writes `RESULTS.txt` into its volatile run dir).  The FIX column
    has not run (no fix exists); "red against FIX" is read from the printed wants.

13. **The dead run does not score zero, and two wants can be `None`.**  `chs h1`'s want is `TAG(S) if S else None` (504-505)
    and `lba 256`'s HEAD want is `hs = ... if (H and S) else None` (487); `"eq"` rows compare `got == want` (540), so a run
    whose sessions all die passes them; `neg appar` (526) is built from constants and always passes.  Predicted from the
    source: 3/19 (HEAD column), 2/19 (FIX column), CONTROL=FAIL, exit 1 -- IF the driver survives: `Emu.send()` calls
    `os.write` on the pty with no `OSError` handling (349-359), so a non-emulator binary that exits at once may instead
    end the run in a traceback with no sentinel.  Clause (c) needs the measured leg or a gate pin by equality.  (S24, P12.)

14. **`neg appar` is a check that cannot fail.**  It is a constant row (0x0001 vs 0x0000, mode `neg`) that feeds no parser,
    counts toward the score, and prints `got 0x00000001 want 0x00000000 ok` -- a self-contradictory-looking line.

15. **`lba 0`'s HEAD want is recorded, not predicted.**  Mode `nehead` accepts anything but tag 0 (536-539).  The value is
    derivable: CHS sector 0 at head 0, cylinder 0 is offset -512, which `diskimage__internal_access()` answers with a
    zero-filled buffer (`diskimage.c` 1595-1599); measured `0x00000000`.  (S8, P11, D8, N8.)

16. **The witness reads back through CHS sectors 71 and 70 with S = 63** (frozen probe 311, 313): addresses ATA-2 does not
    define (sectors run 1..S, `ata2` 1832-1833); they work only because the model never validates CHS.  Valid triples:
    index 70 = (head 1, sector 8), 69 = (head 1, sector 7).  (P10, N7.)

17. **Floor gaps in the witness's row set** (for the shipped detector): no LBA row with head != 0 (head-conditioned and
    head-term-dropped variants pass every row), no CHS WRITE row (a write-site LBA arm applied unconditionally passes),
    no write-site row with sector 0 or cyl_lo != 0, no bare 0x40 select (a decode that also requires bit 5 passes), no
    read-back with bits 7/5 clear.  On a 4,096-sector image the cyl_hi axis and any head shift `<< k` with k >= 12 are
    unobservable (both readings fall past the file), and the 16-bit tag aliases at 65,536 sectors (TAG(65536) == TAG(0)),
    so enlarging the image also needs a wider tag.  (C1-C20, N1-N9, V1-V20, P16.)

18. **The witness docstring misstates the operative fact**: "Under the HEAD decode every 0xe0 is read as head=0" (frozen
    probe 14-15); the fact that matters -- and the witness brief's own -- is that every 0xa0 (CHS) select sets `lba = 1`
    under HEAD's bit-5 decode.  (Q4 item 5.)

19. **`WITNESS.md` records two small inaccuracies**: it counts "the byte-exact SDH readback" as a device signature (a RAM
    cell would return a written byte identically, so only the sector tags are device-signature controls), and it cites
    "the ORDER the oracle-correction rule demands" where the governing rule is the witness ladder's clause (i).  (P15.)

20. **The base binary is fingerprinted by one source file.**  `RUN_IDENTITY.txt` records the `dev_wdc.c` md5 and the binary
    mtime; whether `/tmp/gxt2/base` was built from HEAD or from the working tree (five `src/` files differ, all off the
    malta/wdc path) is not recorded.  (2.4, P15.)

## Interactions and records the round touches

21. **A recorded alt-ctrl variant changes meaning.**  `OUTSTANDING_BUGS.md` 13001 and `CHANGELOG.md` 17817 say the
    `&& !d->lba` qualification "defeats the abort on every LBA-mode driver"; under HEAD's bit-5 decode `d->lba` is 1 for
    0xa0 (CHS) and 0xe0 (LBA) alike, so the sentence is accurate only after this round.  The rung-3 alt-ctrl probes write
    0xa0 (S19), so their reaction to that variant would change; `diff_wdc_identify.c`'s ROW F pokes `d.lba = 1` directly
    and is unaffected.  Any recorded score for that variant against a rung-3 probe would not reproduce post-fix.  (P17.)

22. **IDENTIFY is inconsistent under ATA-2 before and after the fix.**  Words 60-61 are nonzero while word 49 bit 9 is 0
    (ATA-2 2938-2940: "shall be set to 0" if LBA is unsupported); after the fix the device honours LBA with bit 9 still
    clear (2872-2873: bit 9 "is used to indicate").  Word 53 = 0x0002 declares words 54-58 invalid while 57-58 carry a
    capacity.  Pre-existing; the round should say which state it leaves.  (P4, Q4 item 2.)

23. **Out-of-range media requests complete with no error.**  Reads past the file are zero-filled and writes past it are
    refused, with no IDNF/ABRT to the guest (S8) -- true for CHS today; the fix makes it reachable for any LBA past the
    image.  Filing candidate.  (7.1, Q3(e), Q4 item 3.)

24. **`wdccylwrap` is adjacent.**  Its note: "word 49 advertises no LBA so the CHS words are the guest's only capacity";
    honouring LBA without advertising it leaves that true for word-49-honouring guests and changes nothing for capacity
    reporting.  Its severity may need a sentence.  (Q4 item 6.)

25. **LBA48 is out of scope and should be said so.**  `WDCC_READ_EXT 0x24`, `WDCC_WRITE_EXT 0x34` (and the MULTI/DMA EXT
    forms) have no arm and fall to `wdc_command()`'s `default:` (ABRT, an interrupt, one latched announcement).  (S11.)

## Records nits found on the way (not this round's to fix unless it touches them)

26. **The ATA-2 draft is on disk but unlisted.**  `_scratchpad/ata2_x3t10_948d.txt` (313,870 bytes; the PDF beside it) is
    not in the carrier's primary-source list; `dev_wdc.c`'s `#485` comment (1081-1082) and `gate_offline.sh` (1525-1526)
    say there is no ATA document "in this tree" (true of the repository), while `#525`'s comment in the same file (640)
    cites the draft; `#405`'s comment (418-420) says "there is no ATA specification here".  The draft is Revision 4c, not an
    approved standard.  (Q4 item 1.)

27. **Input line ranges slightly off** (cosmetic): `wdc__write()` is 552-575 (not "552-~600"); the struct's taskfile fields
    are 126-136 within 122-145 (not 120-142); IDENTIFY word 6's assignments are 346-347 (the cited 340-345 stops before
    them); B's F2 row is 126 and its detail 128-149 (not 125-145).

28. **The research records' class label** contains a word this brief does not use; the ledger title/state_note, TRIAGE
    row, ADJ ruling, OUTSTANDING_BUGS entry and B's F2 detail are quoted CONDENSED with the label bracketed.  A file-reading
    seat that opens them sees the original wording.

## Brief construction (for the coordinator)

29. **Forms and sizes** (bytes): `brief_FULL.md` 195,910; `brief_COMPACT.md` 89,699 (limit 90,000); `brief_PACKET.md`
    74,105 (limit 75,000; a launcher line of ~256 bytes before the QUESTIONS heading keeps each split packet under 75,000).
    Each form has exactly one `## 11. QUESTIONS` heading; Q1-Q4 split as Q1+Q2 / Q3+Q4.  The PACKET form carries no
    file-reading instruction (checked by the build) and marks claims DERIVED / NOT CHECKABLE only.  The word the inputs
    forbid occurs zero times in all three forms.

30. **What the condensed forms cut**, each cut marked in the text: COMPACT and PACKET drop 1.2 and 1.4 (the TRIAGE row and
    the OUTSTANDING_BUGS entry, both restating 1.1), condense 1.1's state note, 1.5, 1.6, 3.4 and section 10, and inline
    shorter source ranges (`wdc__read()` minus its one 30-line comment, which removes no statement); PACKET also drops the
    struct, IDENTIFY, drain, `wdcreg.h`, gate-wiring and primary-source code blocks where S-premises quote the lines used,
    paraphrases (marked) the rules it does not grade by, and condenses 3.1 (the design text) to its decisions.

31. **The template used is the WORKING-TREE `tools/BRIEF_TEMPLATE.md`** (+152 lines over HEAD: the scoped-settled-premise
    rule, the permitted-path check, §C5's third trigger, §C6 and §C7 -- owner rulings of 2026-10-09 that are not
    committed).  `tools/CLAUDE.md` is also dirty but byte-identical to the root `CLAUDE.md` that section 10 quotes.

32. **Codex scoping (§C5).**  The FULL form invites reading named files under `regress/artifacts/` (the witness and four
    research files) and forbids browsing the rest, the ledger, `CHANGELOG.md` and `OUTSTANDING_BUGS.md` (all inlined);
    the N5 pass ran the same pattern with codex answering.  It asks for no construction: variants and rows are supplied
    for classification (§C5 substitutes).

33. **The probe is cited by its FROZEN copy** (`regress/artifacts/wdclbaaddr/witness_20261024/wdc_lba_probe.frozen.py`,
    md5 `8f3632ff...`, identical to the untracked `regress/wdc_lba_probe.py` at drafting).  When the round commits, the
    artifacts dir's `.py` needs a `check_probe_wiring.py` MANIFEST line (the `#533` pattern classes a frozen instrument as
    `CLASS_TOOL`, the witness program as `CLASS_WITNESS`), or precommit section R refuses it.

34. **Every quotation was machine-checked** against its source after normalising whitespace and markdown: 219 fragments,
    6 not matched literally, all joins rather than edits -- "words 60-61" (ATA-2 hyphenates "60-" / "61" across a line)
    and the exemption string "two-leg differential; wants a single-leg mode before gate 10 can assert anything" (a Python
    string literal split across two lines in `check_probe_wiring.py` 3302-3303).
    The build and check scripts were temporary files in this directory and are deleted; their output closes
    `C0_OUTPUT.txt`.

35. **Section C0** found no shipped round (`grep wdclbaaddr CHANGELOG.md` at HEAD: nothing; `dev_wdc.c` last changed by
    `e16a8b7c`).  The third C0 question (does the tool exist?) changed answer DURING drafting: `regress/wdc_lba_probe.py`
    did not exist at 16:47 and was written at 17:03 for this round; no other committed probe reads an LBA-mode transfer.
