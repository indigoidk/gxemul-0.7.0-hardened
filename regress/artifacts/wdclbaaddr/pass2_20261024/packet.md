PROJECT FRAMING.  GXemul is a computer-architecture emulator; this fork is a software-correctness hardening effort on the
emulator's own C device models.  This round corrects a DECODE defect in the IDE/ATA disk model: an LBA-mode request was served
from the cylinder/head/sector reading of the same taskfile bytes because the LBA flag was decoded from bit 5 (ATA: bit 6) and the
LBA28 address formula was compiled out.  Ordinary device-model correctness review.  Tree: `GXEMUL-SEC/` at HEAD cc1f69cc; ignore any
other `src/` under the project root.  PLEASE DO NOT SIMPLY RATIFY: check the premises and the diff, not only the derivations.

## 1. SETTLED PREMISES (recorded; each with its warrant -- re-state them as questions if you doubt them)

S1  The witness (`regress/artifacts/wdclbaaddr/witness_20261024/`, rung 3, UNMODIFIED `evbmips -e malta`, measured 17:03 before any
    edit on a binary whose `dev_wdc.c` is HEAD's): LBA 70 served as tag 69, LBA 256 as tag 1007 (H*S-1 at 16/63), LBA 0 as zeros,
    a WRITE at LBA 70 landing at index 69; 19/19 against the HEAD column, the five `lba *` rows red against the FIX wants.
S2  The same FROZEN instrument (md5 8f3632ff) on the fixed build (`witness_20261024/RESULTS_fix.txt`): fix leg 19/19 against the
    FIX column (LBA 70 -> tag 70, LBA 256 -> tag 256, LBA 0 -> tag 0, the write at index 70); base leg unchanged 19/19 vs HEAD.
S3  Pass 1 (seven answers, `pass1_20261024/`) and its two-seat adjudication (`ADJ_PACKET.md`, `codex_t4adj1.txt`, `grok_t4adj1.txt`)
    settled: decode bit 6; the reserved bits 7/5 kept in the field renamed `sectorsize` -> `sdh_resv` (no field added or deleted);
    two local LBA arms with the product in 64-bit arithmetic; the two printfs deleted; word 49 unchanged (the advertisement filed;
    the "five rigs" rationale retracted); member 7 IMPLEMENT; the detector rows N1-N8 + `lba cylhi` + `sdh rb0` + the write twin
    `lba wr cylhi`; `neg appar` out of the score; V15 (the unwidened product) MEASURED, not promised; clause (c) by a measured dead
    run; the frozen copy CLASS_WITNESS; `wdcmediastatus` filed.  Dispositions by id in `pass1_20261024/ADJ_PACKET.md`.
S4  `dev_wdc.c` facts: the data ring is reset on every command (:936-938, :915-923); READ is served synchronously (:973);
    `d->head`'s only writer is `:2017` (`idata & 0xf`); `write_offset` is assigned after the LBA arm; geometry 16/63 with cylinders
    rounded up (`diskimage.c:270-271, :295-297`): 4096 sectors -> capacity 5040; the LBA 4096-5039 band is a short zero-filled read
    returning success (#416's design), not a refused access.
S5  The gate-2 row `row_no_lba_claim()` and `gate_offline.sh`'s comment are re-authored IN THE SAME CHANGE by comment text; both
    files carry other sessions' uncommitted hunks, so the landing stages HEAD-based copies plus this round's hunks only.

## 2. THE PRODUCT DIFF (`git diff HEAD -- src/devices/dev_wdc.c`, 5 hunks)

```diff
diff --git a/src/devices/dev_wdc.c b/src/devices/dev_wdc.c
index d7eda83b..d257ac5f 100644
--- a/src/devices/dev_wdc.c
+++ b/src/devices/dev_wdc.c
@@ -129,7 +129,7 @@ struct wdc_data {
 	int		sector;
 	int		cyl_lo;
 	int		cyl_hi;
-	int		sectorsize;
+	int		sdh_resv;
 	int		lba;
 	int		drive;
 	int		head;
@@ -371,8 +371,11 @@ static void wdc_initialize_identify_struct(struct cpu *cpu, struct wdc_data *d)
 	d->identify_struct[2 * 47 + 0] = 0x80;
 	d->identify_struct[2 * 47 + 1] = 128;
 
-	/*  49: capabilities:  */
-	/*  (0x200 = LBA, 0x100 = DMA support.)  */
+	/*  49: capabilities: (0x200 = LBA, 0x100 = DMA support.)  #572
+	    honours LBA28 commands (the LBA bit of the select byte) but does
+	    NOT advertise LBA here: the advertisement is a separate, measured
+	    decision (see the wdclbaadvertise row); words 60-61 already carry
+	    the capacity.  */
 	d->identify_struct[2 * 49 + 0] = 0;
 	d->identify_struct[2 * 49 + 1] = 0;
 
@@ -467,13 +470,11 @@ void wdc__read(struct cpu *cpu, struct wdc_data *d)
 	    + (int64_t)d->head * d->sectors_per_track[d->drive] +
 	    (int64_t)d->heads[d->drive] * d->sectors_per_track[d->drive] * cyl);
 
-#if 0
-	/*  LBA:  */
+	/*  #572: LBA28 -- head[3:0] is LBA[27:24]; the product is 64-bit
+	    (it overflows int for any head != 0).  */
 	if (d->lba)
-		offset = 512 * (((d->head & 0xf) << 24) + (cyl << 8)
-		    + d->sector);
-	printf("WDC read from offset %lli\n", (long long)offset);
-#endif
+		offset = 512 * (int64_t)(((d->head & 0xf) << 24) +
+		    (cyl << 8) + d->sector);
 
 	while (count > 0) {
 		int to_read = count > max_sectors_per_chunk?
@@ -559,13 +560,11 @@ void wdc__write(struct cpu *cpu, struct wdc_data *d)
 	uint64_t offset = 512 * (d->sector - 1
 	    + (int64_t)d->head * d->sectors_per_track[d->drive] +
 	    (int64_t)d->heads[d->drive] * d->sectors_per_track[d->drive] * cyl);
-#if 0
-	/*  LBA:  */
+	/*  #572: LBA28 -- head[3:0] is LBA[27:24]; the product is 64-bit
+	    (it overflows int for any head != 0).  */
 	if (d->lba)
-		offset = 512 * (((d->head & 0xf) << 24) +
+		offset = 512 * (int64_t)(((d->head & 0xf) << 24) +
 		    (cyl << 8) + d->sector);
-	printf("WDC write to offset %lli\n", (long long)offset);
-#endif
 
 	d->write_in_progress = d->cur_command;
 	d->write_count = count;
@@ -2003,21 +2002,26 @@ DEVICE_ACCESS(wdc)
 		}
 		break;
 
-	case wd_sdh:	/*  6: sectorsize/drive/head  */
+	case wd_sdh:	/*  6: SDH -- bit 6 = LBA, bit 4 = drive,
+			    bits 3..0 = head / LBA[27:24]  */
 		if (writeflag==MEM_READ) {
-			odata = (d->sectorsize << 6) + (d->lba << 5) +
-			    (d->drive << 4) + (d->head);
-			debug("[ wdc: read from SDH: 0x%02x (sectorsize %i,"
-			    " lba=%i, drive %i, head %i) ]\n", (int)odata,
-			    d->sectorsize, d->lba, d->drive, d->head);
+			odata = d->sdh_resv | (d->lba << 6) | (d->drive << 4) |
+			    d->head;
+			debug("[ wdc: read from SDH: sdh=0x%02x lba=%i drive=%i"
+			    " head=%i ]\n", (int)odata, d->lba, d->drive,
+			    d->head);
 		} else {
-			d->sectorsize = (idata >> 6) & 3;
-			d->lba   = (idata >> 5) & 1;
+			/*  #572: bits 7 and 5 of the select byte (reserved in
+			    ATA), kept for a byte-exact readback.  */
+			d->sdh_resv = idata & 0xa0;
+			/*  #572: ATA puts the LBA flag in bit 6 (WDSD_LBA); it
+			    was decoded from bit 5.  */
+			d->lba   = (idata >> 6) & 1;
 			d->drive = (idata >> 4) & 1;
 			d->head  = idata & 0xf;
-			debug("[ wdc: write to SDH: 0x%02x (sectorsize %i,"
-			    " lba=%i, drive %i, head %i) ]\n", (int)idata,
-			    d->sectorsize, d->lba, d->drive, d->head);
+			debug("[ wdc: write to SDH: sdh=0x%02x lba=%i drive=%i"
+			    " head=%i ]\n", (int)idata, d->lba, d->drive,
+			    d->head);
 		}
 		break;
 
```

## 3. THE BUILDER'S REPORT (`detector_20261024/BUILD_REPORT.md`)

# `#572` (wdclbaaddr) -- BUILD REPORT, written 2026-10-24 21:2x by the main loop (087a90) FROM THE ARTIFACTS in this directory
# (the builder sub-agent produced every artifact below and then went idle without writing its report; nothing here is asserted
# that a named file does not show).

## 1. The product edit

`src/devices/dev_wdc.c` (working tree; `git diff HEAD -- src/devices/dev_wdc.c` is the pass-2 packet's section 2): five `#572`
sites -- the SDH arm's decode (`lba` from bit 6, the reserved bits 7/5 kept in the field renamed `sectorsize` -> `sdh_resv`, drive
bit 4, head bits 3-0) and its byte-exact readback composition, the LBA28 arm in `wdc__read()` and in `wdc__write()` (each
`512 * (int64_t)(((d->head & 0xf) << 24) + (cyl << 8) + d->sector)`, the old `printf` gone), the word-49 comment.  `grep -c '#572'`
= 5; `grep -c sectorsize` = 0.  The twin `est/src/devices/dev_wdc.c` is byte-identical (checked at packet time; the landing script
re-checks).  Fix clone `/tmp/gxt2/fix` built from it (`make_fix.log`); every table's `final:` line records the fix tree `cmp CLEAN vs
SEC`.

## 2. The detector

`regress/wdc_lba_probe.py`: 827 lines, md5 `5e4ecd477c2a4acbcb79d4382ffa4183` (the shipped bytes).  Seven debugger-driven guest
sessions on the unmodified `evbmips -e malta` with the tagged 4096-sector image (`identify`, `chs`, `sdh`, `lba`, `lba0`, `lbah1`,
`lbawr`), 33 scored rows = 7 ram-liveness + 2 IDENTIFY + 4 CHS + 4 SDH readbacks + 4 LBA reads + 1 LBA-0 + 2 head-1 + 9 write-session
rows (the derivation is in `HUNKS_gate_sh_rounding.sh.diff`'s pin comment).  Modes: `<bin> - <outdir>` (witness), `<base> <fix>
<outdir>` (two legs), `<bin> GATE <outdir>` (one leg vs the FIX column; `WDC_LBA_RESULT=p/n`, `WDC_LBA_CONTROL=OK|FAIL`, sentinel
`WDCLBA_PROBE_DONE`).  `None` observations and wants fail their row; the constant `neg appar` row is out of the score (a startup
comparator self-check replaces it); the pty driver survives a dead child and still prints the result lines and the sentinel
(`dead_run.out`).

Revisions: the kill-table instrument is `wdc_lba_probe.frozen.py` here, md5 `fc878c423319892979271d87b47666b8` (frozen before table
1); the shipped `5e4ecd47` differs from it in ONE row's predicate -- `id geo` now requires `S >= 10` (mode `geo`) instead of `S != 0`
(mode `nz`), 8 executable lines (`rev_equivalence.txt` (a)); every one of the 41 preserved run logs read `(16, 63)` for that row
except the dead run's `(None, None)`, so both predicates return the same verdict on every preserved observation and the table scores
transfer row for row (`rev_equivalence.txt` (b), "VERDICT: scores transfer row-for-row").  The shipped bytes additionally carry
their OWN measurements: GATE 33/33 CONTROL=OK (`final_5e4ecd47/RESULTS_gate.txt`, 20:53) and the two-leg base 33/33 vs HEAD /
fix 33/33 vs FIX (`final_5e4ecd47/RESULTS_twoleg.txt`, 21:19-21:23, run by the main loop from a frozen copy).  Intermediate
revisions `b0c7498c` and `d9b93abe` have their own GATE + two-leg results under `final_<md5>/`.

## 3. Measurements (every number from the named file)

* Witness instrument (`../witness_20261024/wdc_lba_probe.frozen.py`, md5 8f3632ff): base leg 19/19 vs HEAD, 17:03, BEFORE any edit
  (`RESULTS_base.txt`); fix leg 19/19 vs FIX, 19:04 (`RESULTS_fix.txt`) -- the `probe:` term's two halves on the SAME script.
* Revised detector two-leg: base 33/33 vs HEAD, fix 33/33 vs FIX (`twoleg/RESULTS.txt`; also `final_b0c7498c/`, `final_d9b93abe/`,
  `final_5e4ecd47/RESULTS_twoleg.txt`).
* GATE mode on the fix binary: 33/33 CONTROL=OK (`gate/RESULTS.txt`; `final_*/RESULTS_gate.txt`).
* Dead run (`/bin/false` as the binary, GATE mode): `WDC_LBA_RESULT=0/33`, `WDC_LBA_CONTROL=FAIL`, sentinel present (`dead_run.out`,
  19:11-19:25) -- clause (c): measured at `detector_20261024/dead_run.out`.
* `PRETABLE.out` (19:01, before table 1): sibling parity, claim->row, guard field vs body field with the body-induced partition,
  CHANNEL per scored row.
* Kill table 1 (`SCORES.txt`, 19:25-20:05, instrument fc878c42, GATE mode vs the FIX column, baseline 33/33 OK): 18/18 KILLED, no
  escape -- V1 17/33, V2 17/33, V3 31/33, V4r 32/33, V4w 32/33, V5w 31/33, V6w 31/33, V8 32/33, V11 29/33, V13r 19/33, V13w 31/33,
  V14r 28/33, V14w 28/33, V15 32/33 (the unwidened product: killed on THIS gcc -O3 build by the head-1 row; undefined in general,
  recorded as a measurement that does not generalise), V16 31/33, V17 31/33, V18 31/33, V20 28/33.
* Kill table 2, contract claims at both sites (`SCORES2.txt`, 20:06-20:3x): 9/9 KILLED -- V5r 32/33, V6r 31/33, V8w 32/33, V11w
  30/33, V9r8 (head shift by 8, lands in the file) 32/33, V10r 32/33 and V10w 32/33 (the cylinder-low-only arms, killed by the two
  high-cylinder rows), T_m1 26/33 and T_p1 26/33 (the +-1 translations; the shipped rows see more than the witness's four).
* Single builds (`SCORES_V12_V7.txt`, 20:45-20:51): V12 (`& 0xf` dropped) 33/33 SURVIVED -- EQUIVALENT, as expected (one masked
  writer of `d->head`); V7 (the cylinder-high-conditioned arm) 33/33 SURVIVED -- the disclosed BLIND cell on this image.
* Applicators: `mutants572.py` (final), `mutants572_table1.py.txt`, `mutants572_table2.py.txt`; per-mutant logs `raw_mut/*.out`.
* Gate 2's offline harness `regress/diff_wdc_identify.c` built WITH this round's hunk against the fixed model: 128 rows, 0 failures,
  `WDC_IDENTIFY_PASS` (`offline_identify_hunk.out`).

## 4. The hunks for the four files the landing stages from HEAD-based copies

`HUNKS_gate_sh_rounding.sh.diff` (+52: the gate-10 block, denominator pinned to 33 with its derivation, CONTROL=OK, sentinel),
`HUNKS_check_probe_wiring.py.diff` (+21: `wdc_lba_probe.py` CLASS_DETECTOR, the witness frozen copy CLASS_WITNESS, this directory's
frozen instrument and applicator CLASS_TOOL), `HUNKS_diff_wdc_identify.c.diff` (+4 net: the `row_no_lba_claim()` comment and FAIL
text re-authored; assertion, name and "ok" string unchanged), `HUNKS_gate_offline.sh.diff` (one comment line).  All four dry-applied
cleanly to HEAD's copies by the main loop at 19:4x (the later 20:35 revisions of the first two re-checked at landing).

## 5. Not done / caveats

* The builder's own six-line report was not delivered; this file stands in, from the artifacts only.
* No measurement of the gate-10 SCRIPT with the block in place (the landing's precommit run and gate 10 itself do that); the GATE
  mode's protocol lines the block greps were exercised by the GATE runs above.


## 4. THE PRE-TABLE RECORD (`detector_20261024/PRETABLE.out`, written before the first table)

```
wdclbaaddr (#572) -- PRE-TABLE CHECK for regress/wdc_lba_probe.py
written BEFORE the first kill-table run; its mtime proves the order.
detector: 33 scored rows, 10 of them symptom rows (HEAD want != FIX want).  The fix
edits src/devices/dev_wdc.c at four sites: the SDH decode (write) and its read-back
composition (grep `case wd_sdh:`), the LBA28 arm in `wdc__read` (grep `void wdc__read`)
and in `wdc__write` (grep `void wdc__write`); word 49 is unchanged (grep `49: capabilities`).

================================================================================
SCOPE.  This block binds because the round ships/extends a kill-table-backed detector.

FLOOR BOOKKEEPING (vacuity floor a-f):
 (a) pre-fix RED: the five+ symptom rows show the CHS reading on the committed build
     (witness_20261024/RESULTS_base.txt, 19/19 vs HEAD; the lba* rows are RED vs FIX).
 (b) verbatim reinstatement at EVERY fixed site -> V1 (decode back on bit 5), V14
     (one site left #if 0, two halves), V17 (read-back recomposed with the old formula).
 (c) null medium: a NON-EMULATOR executable -- the dead run on /bin/false, recorded
     here as `(c): measured at detector_20261024/dead_run.out`.  gate 10's need_exec
     turns an ABSENT binary into a whole-gate SKIP, so an executable-that-is-not-the-
     emulator is the medium that exercises the probe.
 (d) DEPENDS-ON: at wdc__read / wdc__write the only dominating predicate the fix adds is
     `if (d->lba)`; at the decode line the io_enabled test, `case wd_sdh:` and the
     read/write split are unchanged.  The guarded BODY reads d->head, d->cyl_lo,
     d->cyl_hi (via cyl) and d->sector; the body TESTS none of them (no if over them),
     so the body-induced partition of each is EMPTY and there are NO joint cells.  The
     single-axis conditioned-arm mutants V4/V5/V6 (head/cyl/sector) are enumerated and
     rowed or disclosed per cell below -- adjudicated as the floor by the pass-1 panel.
 (e) the contract: the probe docstring's CATCHES / clause (e) DISCLOSURES / MEASURED-
     NOT-PROMISED (V15) / ANCHOR paragraph.
 (f) ANCHOR: each tag names WHICH sector was served, through image content the decode
     does not produce.  "If every LBA moved by one sector, which row reds?" -> the five
     `lba` read rows (lba 70, lba 256, sel 40, lba 0, lba h1) and, on the write side,
     lba wr / lba wr256.  A +1 shift reds four read rows and lba wr; a -1 shift also reds
     lba wr2.
 R21 compare edges: N/A (a bit test and a flag test; the disk-layer bounds are #416's).
 R14: N/A (no `exit(` deleted by this fix).

================================================================================
SIBLING PARITY (read site vs write site).
 Read site rows (L=1): lba 70, lba 256, sel 40, lba 0, lba h1, lba cylhi.  CHS rows:
   chs s1/s2/h1/c1, lba h1 ctl.
 Write site rows (L=1): lba wr, lba wr h1, lba wr256, lba wr cylhi (via refusal).  CHS
   write rows: chs wr, chs wr2.
 ASYMMETRY and how it is covered: the write site has fewer L=1 observation points than
 the read site because a write is observed only by reading the target back.  Each write
 cell has a dedicated read-back row through a VALID CHS triple (head 1 sector 8/7/5/9,
 head 4 sector 5, head 15 sector 63, head 0 sector 6/10/11) -- the valid-triple choice
 is the witness note's correction (sectors 71/70 outside 1..S were only served because
 the model does not validate CHS).  No de-fatalised arm, so no completion-event sibling
 row is owed.

CLAIM -> ROW (each added comment asserting an observable consequence owes a row):
 "LBA served at the LBA, not the CHS reading"  -> lba 70, sel 40, lba wr, lba wr256.
 "read-back byte-exact through sdh_resv"       -> sdh rb, sdh rb2, sdh rb3, sdh rb0.
 "word 49 stays 0 (LBA implemented, not advertised)" -> id w49.
 "the 64-bit product honours head != 0"        -> lba h1 (FIX zeros; past the file).
 No comment claims a channel that no row observes.

GUARD FIELD vs BODY FIELD (R10), with the body-induced partition per lvalue:
 guard reads  d->lba              (written in the SDH write arm, bit 6).
 body reads   d->head   -- written same SDH arm, independent bits 3..0; partition EMPTY
                           (the LBA body does not test head); SAMPLED {0, 1}.
              d->sector -- written wd_sector; partition EMPTY; SAMPLED {0, 5, 70}.
              d->cyl_lo -- written wd_cyl_lo; partition EMPTY; SAMPLED {0, 1}.
              d->cyl_hi -- written wd_cyl_hi; partition EMPTY; SAMPLED {0, 1}.
 Disagreeing states (lba=1 with head!=0 / cyl_lo!=0 / cyl_hi!=0 / sector==0) are reachable
 by ordinary register writes and are rowed (lba h1, lba 256, lba cylhi, lba 0) or
 disclosed (cyl_hi destinations past a 4096-sector image: C6/C11, clause (e)).

================================================================================
CHANNEL per scored row -- the mutant it kills and the observable that differs.
A row whose named channel cannot vary under its named mutant would be vacuous by
construction; none below is.

 ram:*           apparatus liveness (0x5a5a RAM round-trip)   -- a bad encoding/boot
 id w49          word 49 advertised nonzero (C18)             -- the 16-bit IDENTIFY word
 id geo          H,S read back zero                           -- geometry words 3/6
 chs s1/s2/h1    decode on bit 7 (V2) / unconditional LBA (V13) -- CHS tag at index 0/1/S
 chs c1          cyl_lo dropped on the CHS path               -- tag at index heads*S (N8)
 sdh rb          read-back drops bit 6 (V18)                  -- 0xe5 byte
 sdh rb2         read-back recomposed old formula (V17)       -- 0xb3 (reads 0x93 if lba<<5)
 sdh rb3         read-back forces bits 7/5 to 1 (V16)         -- 0x4c (bits 7,5 CLEAR)
 sdh rb0         a stuck reserved/field bit                   -- 0x00 after 0xe5 then 0x00
 lba 70          decode off bit 6 / LBA arm disabled (V1-V3,V13) -- tag 69(HEAD) vs 70(FIX)
 lba 256         LBA arm conditioned on cyl/sector (V5r/V6r)  -- tag 1007(HEAD) vs 256(FIX)
 sel 40          decode qualified by bits 7/5 (V2,V3)         -- 0x40: tag 69 vs 70 (N3)
 lba cylhi       cyl_lo<<8-only cylinder term (V10 variant)   -- zeros both; reds a cyl_lo-
                                                                 only mutant that serves 70
 lba 0           LBA arm disabled / sector-1 offset (V11)     -- zeros(HEAD) vs tag 0(FIX)
 lba h1          head term dropped / 32-bit product (V8,V15)  -- tag 67(HEAD) vs zeros(FIX)
 lba h1 ctl      (anchor: a tagged sector reachable in-session) -- tag 2 both legs
 lba wr          write-site LBA disabled / offset captured early (V14w,V20) -- tag70 vs payload
 lba wr2         write-site decode (V1w/V13w)                 -- payload(HEAD) vs tag69(FIX)
 lba wr h1       write-site head term (V8w)                   -- payload(HEAD) vs tag67(FIX)
 lba wr h1s5     (control: index 5 untouched)                 -- tag 5 both legs
 lba wr256       write-site cyl/sector condition (V5w/V6w/V11w) -- tag256(HEAD) vs payload
 lba wr256b      write-site landing (V11w)                    -- payload(HEAD) vs tag1007(FIX)
 chs wr          CHS write stays CHS (V13w on a CHS select)   -- payload both legs
 chs wr2         (control: index 10 untouched)                -- tag 10 both legs
 lba wr cylhi    write-arm cyl_lo<<8-only variant (V10w)      -- tag71 both (refused); a
                                                                 cyl_lo-only write lands 71

================================================================================
KILL TABLE to run (BUILD_SPEC D3): V1, V2, V3, V4r/V4w, V5w, V6w, V8, V11, V13r/V13w,
V14 (both halves), V15 [measured, recorded non-generalising], V16, V17, V18, V20.
One mutant per build in a scratch clone of /tmp/gxt2/fix, .MUTANT sentinel dropped
first, cmp vs GXEMUL-SEC after restore.  The dead run on /bin/false is clause (c).
```

## 5. THE MEASURED SCORES (every file matching SCORES*/RESULTS*/KILLTABLE*/POSTTABLE under detector_20261024/)

--- SCORES.txt (2223 bytes) ---
wdclbaaddr (#572) KILL TABLE   2026-10-24 19:25:41
baseline: /tmp/gxt2/fix (the round's post-fix working set); dev_wdc.c == GXEMUL-SEC == the shipped fix
instrument: wdc_lba_probe.frozen.py (GATE mode, FIX column), md5 fc878c42
applicator: mutants572.py
KILLED := the FIX-column score p < n (33) or CONTROL=FAIL; ESCAPE := p==n AND CONTROL=OK
---------------------------------------------------------------------------
baseline cmp CLEAN vs SEC; baseline binary fresh
BASE          score=33/33 control=OK  (expect 33/33 OK)
---------------------------------------------------------------------------
V1            score=17/33 control=FAIL  -> KILLED   reds: chs,chs,chs,chs,sdh,sdh,sel,lba,lba,lba,lba,lba,lba,lba,chs,lba,LEG
V2            score=17/33 control=FAIL  -> KILLED   reds: chs,chs,chs,chs,sdh,sdh,sel,lba,lba,lba,lba,lba,lba,lba,chs,lba,LEG
V3            score=31/33 control=FAIL  -> KILLED   reds: sdh,sel,LEG
V4r           score=32/33 control=OK  -> KILLED   reds: lba,LEG
V4w           score=32/33 control=OK  -> KILLED   reds: lba,LEG
V5w           score=31/33 control=OK  -> KILLED   reds: lba,lba,LEG
V6w           score=31/33 control=OK  -> KILLED   reds: lba,lba,LEG
V8            score=32/33 control=OK  -> KILLED   reds: lba,LEG
V11           score=29/33 control=OK  -> KILLED   reds: lba,lba,sel,lba,LEG
V13r          score=19/33 control=FAIL  -> KILLED   reds: chs,chs,chs,chs,lba,lba,lba,lba,lba,lba,lba,chs,chs,lba,LEG
V13w          score=31/33 control=FAIL  -> KILLED   reds: chs,chs,LEG
V14r          score=28/33 control=OK  -> KILLED   reds: lba,lba,lba,lba,lba,LEG
V14w          score=28/33 control=OK  -> KILLED   reds: lba,lba,sel,lba,lba,LEG
V15           score=32/33 control=OK  -> KILLED   reds: lba,LEG
V16           score=31/33 control=FAIL  -> KILLED   reds: sdh,sdh,LEG
V17           score=31/33 control=FAIL  -> KILLED   reds: sdh,sdh,LEG
V18           score=31/33 control=FAIL  -> KILLED   reds: sdh,sdh,LEG
V20           score=28/33 control=OK  -> KILLED   reds: lba,lba,lba,lba,lba,LEG
---------------------------------------------------------------------------
built=18/18  killed=18  escapes: none
final: fix src/devices/dev_wdc.c cmp CLEAN vs SEC (SEC untouched)
KILLTABLE_DONE


--- SCORES2.txt (1465 bytes) ---
wdclbaaddr (#572) KILL TABLE 2 (contract-claim follow-up)   2026-10-24 20:06:27
baseline: /tmp/gxt2/fix (the round's post-fix working set); dev_wdc.c == GXEMUL-SEC == the shipped fix
instrument: wdc_lba_probe.frozen.py (GATE mode, FIX column), md5 fc878c42
applicator: mutants572.py
KILLED := the FIX-column score p < n (33) or CONTROL=FAIL; ESCAPE := p==n AND CONTROL=OK
---------------------------------------------------------------------------
baseline cmp CLEAN vs SEC; baseline binary fresh
BASE          score=33/33 control=OK  (expect 33/33 OK)
---------------------------------------------------------------------------
V5r           score=32/33 control=OK  -> KILLED   reds: lba,LEG
V6r           score=31/33 control=OK  -> KILLED   reds: lba,lba,LEG
V8w           score=32/33 control=FAIL  -> KILLED   reds: lba,LEG
V11w          score=30/33 control=OK  -> KILLED   reds: lba,lba,lba,LEG
V9r8          score=32/33 control=OK  -> KILLED   reds: lba,LEG
V10r          score=32/33 control=FAIL  -> KILLED   reds: lba,LEG
V10w          score=32/33 control=FAIL  -> KILLED   reds: lba,LEG
T_m1          score=26/33 control=OK  -> KILLED   reds: lba,lba,sel,lba,lba,lba,lba,LEG
T_p1          score=26/33 control=FAIL  -> KILLED   reds: lba,lba,sel,lba,lba,lba,lba,LEG
---------------------------------------------------------------------------
built=9/9  killed=9  escapes: none
final: fix src/devices/dev_wdc.c cmp CLEAN vs SEC (SEC untouched)
KILLTABLE_DONE


--- SCORES_V12_V7.txt (990 bytes) ---
wdclbaaddr (#572) V12 / V7 SINGLE BUILDS   2026-10-24 20:45:34
baseline: /tmp/gxt2/fix (the round's post-fix working set); dev_wdc.c == GXEMUL-SEC == the shipped fix
instrument: wdc_lba_probe.frozen.py (GATE mode, FIX column), md5 fc878c42
applicator: mutants572.py
KILLED := p < n (33) or CONTROL=FAIL;  SURVIVED := p==n AND CONTROL=OK -- expected here: V12 EQUIVALENT, V7 the disclosed BLIND cell; NOT escapes
---------------------------------------------------------------------------
baseline cmp CLEAN vs SEC; baseline binary fresh
BASE          score=33/33 control=OK  (expect 33/33 OK)
---------------------------------------------------------------------------
V12           score=33/33 control=OK  -> SURVIVED   reds: none
V7            score=33/33 control=OK  -> SURVIVED   reds: none
---------------------------------------------------------------------------
built=2/2  killed=0  survived: V12 V7
final: fix src/devices/dev_wdc.c cmp CLEAN vs SEC (SEC untouched)
KILLTABLE_DONE


--- final_5e4ecd47\RESULTS_gate.txt (5146 bytes) ---
======================================================================================
wdclbaaddr -- RUNG-3 WITNESS + DETECTOR on unmodified `evbmips -e malta`
======================================================================================
date      2026-10-24 20:53:02
machine   evbmips -e malta   LITTLE endian   (machine desc UNMODIFIED)
wdc       physical 0x180001f0 via bus_pci piix4_ide; KSEG1 0xffffffffb80001f0
disk      /tmp/gxt2/work/t4/gatefinal_205302/wdc-lba-scratch.img  (4096 sectors; tag n = (n, ~n))
base bin  /tmp/gxt2/fix/gxemul
mode      GATE -- one leg vs the FIX column

--------------------------------------------------------------------------------------
LEG gate -- gate build, judged against the FIX column
--------------------------------------------------------------------------------------
    [gate_identify] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/gatefinal_205302/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/gatefinal_205302/raw/gate_identify.bin
    encodings: 62/62 words, 62/62 mnemonics agree with the disassembler
    parked at 0xffffffff801000f0: yes   (1.52 s)
    [gate_chs] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/gatefinal_205302/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/gatefinal_205302/raw/gate_chs.bin
    encodings: 76/76 words, 76/76 mnemonics agree with the disassembler
    parked at 0xffffffff80100128: yes   (1.52 s)
    [gate_sdh] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/gatefinal_205302/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/gatefinal_205302/raw/gate_sdh.bin
    encodings: 22/22 words, 22/22 mnemonics agree with the disassembler
    parked at 0xffffffff80100050: yes   (1.51 s)
    [gate_lba] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/gatefinal_205302/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/gatefinal_205302/raw/gate_lba.bin
    encodings: 80/80 words, 76/80 mnemonics agree with the disassembler
    parked at 0xffffffff80100138: yes   (1.52 s)
    [gate_lba0] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/gatefinal_205302/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/gatefinal_205302/raw/gate_lba0.bin
    encodings: 25/25 words, 25/25 mnemonics agree with the disassembler
    parked at 0xffffffff8010005c: yes   (1.52 s)
    [gate_lbah1] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/gatefinal_205302/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/gatefinal_205302/raw/gate_lbah1.bin
    encodings: 44/44 words, 42/44 mnemonics agree with the disassembler
    parked at 0xffffffff801000a8: yes   (1.52 s)
    [gate_lbawr] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/gatefinal_205302/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/gatefinal_205302/raw/gate_lbawr.bin
    encodings: 1511/1511 words, 1508/1511 mnemonics agree with the disassembler
    parked at 0xffffffff80101794: yes   (1.52 s)

  row          got          head         fix         
  ram:identify 0x00005a5a   want 0x00005a5a   ok
  ram:chs      0x00005a5a   want 0x00005a5a   ok
  ram:sdh      0x00005a5a   want 0x00005a5a   ok
  ram:lba      0x00005a5a   want 0x00005a5a   ok
  ram:lba0     0x00005a5a   want 0x00005a5a   ok
  ram:lbah1    0x00005a5a   want 0x00005a5a   ok
  ram:lbawr    0x00005a5a   want 0x00005a5a   ok
  id w49       0x00000000   want 0x00000000   ok
  id geo       (16, 63)     want H!=0,S>=10   ok
  chs s1       0xffff0000   want 0xffff0000   ok
  chs s2       0xfffe0001   want 0xfffe0001   ok
  chs h1       0xffc0003f   want 0xffc0003f   ok
  chs c1       0xfc0f03f0   want 0xfc0f03f0   ok
  sdh rb       0x000000e5   want 0x000000e5   ok
  sdh rb2      0x000000b3   want 0x000000b3   ok
  sdh rb3      0x0000004c   want 0x0000004c   ok
  sdh rb0      0x00000000   want 0x00000000   ok
  lba 70       0xffb90046   head 0xffba0045 fix 0xffb90046 [FIX] ok
  lba 256      0xfeff0100   head 0xfc1003ef fix 0xfeff0100 [FIX] ok
  sel 40       0xffb90046   head 0xffba0045 fix 0xffb90046 [FIX] ok
  lba cylhi    0x00000000   want 0x00000000   ok
  lba 0        0xffff0000   head 0x00000000 fix 0xffff0000 [FIX] ok
  lba h1       0x00000000   head 0xffbc0043 fix 0x00000000 [FIX] ok
  lba h1 ctl   0xfffd0002   want 0xfffd0002   ok
  lba wr       0x88887777   head 0xffb90046 fix 0x88887777 [FIX] ok
  lba wr2      0xffba0045   head 0x88887777 fix 0xffba0045 [FIX] ok
  lba wr h1    0xffbc0043   head 0x66669999 fix 0xffbc0043 [FIX] ok
  lba wr h1s5  0xfffa0005   want 0xfffa0005   ok
  lba wr256    0x33332222   head 0xfeff0100 fix 0x33332222 [FIX] ok
  lba wr256b   0xfc1003ef   head 0x33332222 fix 0xfc1003ef [FIX] ok
  chs wr       0x44445555   want 0x44445555   ok
  chs wr2      0xfff5000a   want 0xfff5000a   ok
  lba wr cylhi 0xffb80047   want 0xffb80047   ok

  33/33 passed
  CONTROL=PASS
  LEG gate VERDICT: PASS

WDC_LBA_CONTROL=OK
WDC_LBA_RESULT=33/33
======================================================================================
VERDICT   every leg passed its own column
WDCLBA_PROBE_DONE


--- final_5e4ecd47\RESULTS_twoleg.txt (9900 bytes) ---
======================================================================================
wdclbaaddr -- RUNG-3 WITNESS + DETECTOR on unmodified `evbmips -e malta`
======================================================================================
date      2026-10-24 21:19:23
machine   evbmips -e malta   LITTLE endian   (machine desc UNMODIFIED)
wdc       physical 0x180001f0 via bus_pci piix4_ide; KSEG1 0xffffffffb80001f0
disk      /tmp/gxt2/work/t4/twoleg_final_5e4ecd47_211922/wdc-lba-scratch.img  (4096 sectors; tag n = (n, ~n))
base bin  /tmp/gxt2/base/gxemul
fix bin   /tmp/gxt2/fix/gxemul

--------------------------------------------------------------------------------------
LEG base -- base build, judged against the HEAD column
--------------------------------------------------------------------------------------
    [base_identify] /tmp/gxt2/base/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/twoleg_final_5e4ecd47_211922/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/twoleg_final_5e4ecd47_211922/raw/base_identify.bin
    encodings: 62/62 words, 62/62 mnemonics agree with the disassembler
    parked at 0xffffffff801000f0: yes   (1.52 s)
    [base_chs] /tmp/gxt2/base/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/twoleg_final_5e4ecd47_211922/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/twoleg_final_5e4ecd47_211922/raw/base_chs.bin
    encodings: 76/76 words, 76/76 mnemonics agree with the disassembler
    parked at 0xffffffff80100128: yes   (1.52 s)
    [base_sdh] /tmp/gxt2/base/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/twoleg_final_5e4ecd47_211922/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/twoleg_final_5e4ecd47_211922/raw/base_sdh.bin
    encodings: 22/22 words, 22/22 mnemonics agree with the disassembler
    parked at 0xffffffff80100050: yes   (1.51 s)
    [base_lba] /tmp/gxt2/base/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/twoleg_final_5e4ecd47_211922/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/twoleg_final_5e4ecd47_211922/raw/base_lba.bin
    encodings: 80/80 words, 76/80 mnemonics agree with the disassembler
    parked at 0xffffffff80100138: yes   (1.52 s)
    [base_lba0] /tmp/gxt2/base/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/twoleg_final_5e4ecd47_211922/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/twoleg_final_5e4ecd47_211922/raw/base_lba0.bin
    encodings: 25/25 words, 25/25 mnemonics agree with the disassembler
    parked at 0xffffffff8010005c: yes   (1.52 s)
    [base_lbah1] /tmp/gxt2/base/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/twoleg_final_5e4ecd47_211922/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/twoleg_final_5e4ecd47_211922/raw/base_lbah1.bin
    encodings: 44/44 words, 42/44 mnemonics agree with the disassembler
    parked at 0xffffffff801000a8: yes   (1.52 s)
    [base_lbawr] /tmp/gxt2/base/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/twoleg_final_5e4ecd47_211922/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/twoleg_final_5e4ecd47_211922/raw/base_lbawr.bin
    encodings: 1511/1511 words, 1508/1511 mnemonics agree with the disassembler
    parked at 0xffffffff80101794: yes   (1.52 s)

  row          got          head         fix         
  ram:identify 0x00005a5a   want 0x00005a5a   ok
  ram:chs      0x00005a5a   want 0x00005a5a   ok
  ram:sdh      0x00005a5a   want 0x00005a5a   ok
  ram:lba      0x00005a5a   want 0x00005a5a   ok
  ram:lba0     0x00005a5a   want 0x00005a5a   ok
  ram:lbah1    0x00005a5a   want 0x00005a5a   ok
  ram:lbawr    0x00005a5a   want 0x00005a5a   ok
  id w49       0x00000000   want 0x00000000   ok
  id geo       (16, 63)     want H!=0,S>=10   ok
  chs s1       0xffff0000   want 0xffff0000   ok
  chs s2       0xfffe0001   want 0xfffe0001   ok
  chs h1       0xffc0003f   want 0xffc0003f   ok
  chs c1       0xfc0f03f0   want 0xfc0f03f0   ok
  sdh rb       0x000000e5   want 0x000000e5   ok
  sdh rb2      0x000000b3   want 0x000000b3
[... 1900 bytes cut ...]
ffffff80100000:/tmp/gxt2/work/t4/twoleg_final_5e4ecd47_211922/raw/fix_chs.bin
    encodings: 76/76 words, 76/76 mnemonics agree with the disassembler
    parked at 0xffffffff80100128: yes   (1.52 s)
    [fix_sdh] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/twoleg_final_5e4ecd47_211922/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/twoleg_final_5e4ecd47_211922/raw/fix_sdh.bin
    encodings: 22/22 words, 22/22 mnemonics agree with the disassembler
    parked at 0xffffffff80100050: yes   (1.52 s)
    [fix_lba] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/twoleg_final_5e4ecd47_211922/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/twoleg_final_5e4ecd47_211922/raw/fix_lba.bin
    encodings: 80/80 words, 76/80 mnemonics agree with the disassembler
    parked at 0xffffffff80100138: yes   (1.52 s)
    [fix_lba0] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/twoleg_final_5e4ecd47_211922/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/twoleg_final_5e4ecd47_211922/raw/fix_lba0.bin
    encodings: 25/25 words, 25/25 mnemonics agree with the disassembler
    parked at 0xffffffff8010005c: yes   (1.51 s)
    [fix_lbah1] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/twoleg_final_5e4ecd47_211922/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/twoleg_final_5e4ecd47_211922/raw/fix_lbah1.bin
    encodings: 44/44 words, 42/44 mnemonics agree with the disassembler
    parked at 0xffffffff801000a8: yes   (1.52 s)
    [fix_lbawr] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/twoleg_final_5e4ecd47_211922/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/twoleg_final_5e4ecd47_211922/raw/fix_lbawr.bin
    encodings: 1511/1511 words, 1508/1511 mnemonics agree with the disassembler
    parked at 0xffffffff80101794: yes   (1.52 s)

  row          got          head         fix         
  ram:identify 0x00005a5a   want 0x00005a5a   ok
  ram:chs      0x00005a5a   want 0x00005a5a   ok
  ram:sdh      0x00005a5a   want 0x00005a5a   ok
  ram:lba      0x00005a5a   want 0x00005a5a   ok
  ram:lba0     0x00005a5a   want 0x00005a5a   ok
  ram:lbah1    0x00005a5a   want 0x00005a5a   ok
  ram:lbawr    0x00005a5a   want 0x00005a5a   ok
  id w49       0x00000000   want 0x00000000   ok
  id geo       (16, 63)     want H!=0,S>=10   ok
  chs s1       0xffff0000   want 0xffff0000   ok
  chs s2       0xfffe0001   want 0xfffe0001   ok
  chs h1       0xffc0003f   want 0xffc0003f   ok
  chs c1       0xfc0f03f0   want 0xfc0f03f0   ok
  sdh rb       0x000000e5   want 0x000000e5   ok
  sdh rb2      0x000000b3   want 0x000000b3   ok
  sdh rb3      0x0000004c   want 0x0000004c   ok
  sdh rb0      0x00000000   want 0x00000000   ok
  lba 70       0xffb90046   head 0xffba0045 fix 0xffb90046 [FIX] ok
  lba 256      0xfeff0100   head 0xfc1003ef fix 0xfeff0100 [FIX] ok
  sel 40       0xffb90046   head 0xffba0045 fix 0xffb90046 [FIX] ok
  lba cylhi    0x00000000   want 0x00000000   ok
  lba 0        0xffff0000   head 0x00000000 fix 0xffff0000 [FIX] ok
  lba h1       0x00000000   head 0xffbc0043 fix 0x00000000 [FIX] ok
  lba h1 ctl   0xfffd0002   want 0xfffd0002   ok
  lba wr       0x88887777   head 0xffb90046 fix 0x88887777 [FIX] ok
  lba wr2      0xffba0045   head 0x88887777 fix 0xffba0045 [FIX] ok
  lba wr h1    0xffbc0043   head 0x66669999 fix 0xffbc0043 [FIX] ok
  lba wr h1s5  0xfffa0005   want 0xfffa0005   ok
  lba wr256    0x33332222   head 0xfeff0100 fix 0x33332222 [FIX] ok
  lba wr256b   0xfc1003ef   head 0x33332222 fix 0xfc1003ef [FIX] ok
  chs wr       0x44445555   want 0x44445555   ok
  chs wr2      0xfff5000a   want 0xfff5000a   ok
  lba wr cylhi 0xffb80047   want 0xffb80047   ok

  33/33 passed
  CONTROL=PASS
  LEG fix VERDICT: PASS

WDC_LBA_CONTROL_fix=OK
WDC_LBA_RESULT_fix=33/33
======================================================================================
VERDICT   every leg passed its own column
WDCLBA_PROBE_DONE


--- final_b0c7498c\RESULTS_gate.txt (5161 bytes) ---
======================================================================================
wdclbaaddr -- RUNG-3 WITNESS + DETECTOR on unmodified `evbmips -e malta`
======================================================================================
date      2026-10-24 20:33:12
machine   evbmips -e malta   LITTLE endian   (machine desc UNMODIFIED)
wdc       physical 0x180001f0 via bus_pci piix4_ide; KSEG1 0xffffffffb80001f0
disk      /tmp/gxt2/work/t4/final_202902/gate/wdc-lba-scratch.img  (4096 sectors; tag n = (n, ~n))
base bin  /tmp/gxt2/fix/gxemul
mode      GATE -- one leg vs the FIX column

--------------------------------------------------------------------------------------
LEG gate -- gate build, judged against the FIX column
--------------------------------------------------------------------------------------
    [gate_identify] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/final_202902/gate/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/final_202902/gate/raw/gate_identify.bin
    encodings: 62/62 words, 62/62 mnemonics agree with the disassembler
    parked at 0xffffffff801000f0: yes   (1.52 s)
    [gate_chs] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/final_202902/gate/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/final_202902/gate/raw/gate_chs.bin
    encodings: 76/76 words, 76/76 mnemonics agree with the disassembler
    parked at 0xffffffff80100128: yes   (1.52 s)
    [gate_sdh] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/final_202902/gate/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/final_202902/gate/raw/gate_sdh.bin
    encodings: 22/22 words, 22/22 mnemonics agree with the disassembler
    parked at 0xffffffff80100050: yes   (1.52 s)
    [gate_lba] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/final_202902/gate/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/final_202902/gate/raw/gate_lba.bin
    encodings: 80/80 words, 76/80 mnemonics agree with the disassembler
    parked at 0xffffffff80100138: yes   (1.51 s)
    [gate_lba0] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/final_202902/gate/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/final_202902/gate/raw/gate_lba0.bin
    encodings: 25/25 words, 25/25 mnemonics agree with the disassembler
    parked at 0xffffffff8010005c: yes   (1.52 s)
    [gate_lbah1] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/final_202902/gate/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/final_202902/gate/raw/gate_lbah1.bin
    encodings: 44/44 words, 42/44 mnemonics agree with the disassembler
    parked at 0xffffffff801000a8: yes   (1.52 s)
    [gate_lbawr] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/final_202902/gate/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/final_202902/gate/raw/gate_lbawr.bin
    encodings: 1511/1511 words, 1508/1511 mnemonics agree with the disassembler
    parked at 0xffffffff80101794: yes   (1.52 s)

  row          got          head         fix         
  ram:identify 0x00005a5a   want 0x00005a5a   ok
  ram:chs      0x00005a5a   want 0x00005a5a   ok
  ram:sdh      0x00005a5a   want 0x00005a5a   ok
  ram:lba      0x00005a5a   want 0x00005a5a   ok
  ram:lba0     0x00005a5a   want 0x00005a5a   ok
  ram:lbah1    0x00005a5a   want 0x00005a5a   ok
  ram:lbawr    0x00005a5a   want 0x00005a5a   ok
  id w49       0x00000000   want 0x00000000   ok
  id geo       (16, 63)     want H,S!=0       ok
  chs s1       0xffff0000   want 0xffff0000   ok
  chs s2       0xfffe0001   want 0xfffe0001   ok
  chs h1       0xffc0003f   want 0xffc0003f   ok
  chs c1       0xfc0f03f0   want 0xfc0f03f0   ok
  sdh rb       0x000000e5   want 0x000000e5   ok
  sdh rb2      0x000000b3   want 0x000000b3   ok
  sdh rb3      0x0000004c   want 0x0000004c   ok
  sdh rb0      0x00000000   want 0x00000000   ok
  lba 70       0xffb90046   head 0xffba0045 fix 0xffb90046 [FIX] ok
  lba 256      0xfeff0100   head 0xfc1003ef fix 0xfeff0100 [FIX] ok
  sel 40       0xffb90046   head 0xffba0045 fix 0xffb90046 [FIX] ok
  lba cylhi    0x00000000   want 0x00000000   ok
  lba 0        0xffff0000   head 0x00000000 fix 0xffff0000 [FIX] ok
  lba h1       0x00000000   head 0xffbc0043 fix 0x00000000 [FIX] ok
  lba h1 ctl   0xfffd0002   want 0xfffd0002   ok
  lba wr       0x88887777   head 0xffb90046 fix 0x88887777 [FIX] ok
  lba wr2      0xffba0045   head 0x88887777 fix 0xffba0045 [FIX] ok
  lba wr h1    0xffbc0043   head 0x66669999 fix 0xffbc0043 [FIX] ok
  lba wr h1s5  0xfffa0005   want 0xfffa0005   ok
  lba wr256    0x33332222   head 0xfeff0100 fix 0x33332222 [FIX] ok
  lba wr256b   0xfc1003ef   head 0x33332222 fix 0xfc1003ef [FIX] ok
  chs wr       0x44445555   want 0x44445555   ok
  chs wr2      0xfff5000a   want 0xfff5000a   ok
  lba wr cylhi 0xffb80047   want 0xffb80047   ok

  33/33 passed
  CONTROL=PASS
  LEG gate VERDICT: PASS

WDC_LBA_CONTROL=OK
WDC_LBA_RESULT=33/33
======================================================================================
VERDICT   every leg passed its own column
WDCLBA_PROBE_DONE


--- final_b0c7498c\RESULTS_twoleg.txt (9639 bytes) ---
======================================================================================
wdclbaaddr -- RUNG-3 WITNESS + DETECTOR on unmodified `evbmips -e malta`
======================================================================================
date      2026-10-24 20:29:02
machine   evbmips -e malta   LITTLE endian   (machine desc UNMODIFIED)
wdc       physical 0x180001f0 via bus_pci piix4_ide; KSEG1 0xffffffffb80001f0
disk      /tmp/gxt2/work/t4/final_202902/twoleg/wdc-lba-scratch.img  (4096 sectors; tag n = (n, ~n))
base bin  /tmp/gxt2/base/gxemul
fix bin   /tmp/gxt2/fix/gxemul

--------------------------------------------------------------------------------------
LEG base -- base build, judged against the HEAD column
--------------------------------------------------------------------------------------
    [base_identify] /tmp/gxt2/base/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/final_202902/twoleg/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/final_202902/twoleg/raw/base_identify.bin
    encodings: 62/62 words, 62/62 mnemonics agree with the disassembler
    parked at 0xffffffff801000f0: yes   (1.51 s)
    [base_chs] /tmp/gxt2/base/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/final_202902/twoleg/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/final_202902/twoleg/raw/base_chs.bin
    encodings: 76/76 words, 76/76 mnemonics agree with the disassembler
    parked at 0xffffffff80100128: yes   (1.51 s)
    [base_sdh] /tmp/gxt2/base/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/final_202902/twoleg/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/final_202902/twoleg/raw/base_sdh.bin
    encodings: 22/22 words, 22/22 mnemonics agree with the disassembler
    parked at 0xffffffff80100050: yes   (1.51 s)
    [base_lba] /tmp/gxt2/base/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/final_202902/twoleg/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/final_202902/twoleg/raw/base_lba.bin
    encodings: 80/80 words, 76/80 mnemonics agree with the disassembler
    parked at 0xffffffff80100138: yes   (1.52 s)
    [base_lba0] /tmp/gxt2/base/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/final_202902/twoleg/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/final_202902/twoleg/raw/base_lba0.bin
    encodings: 25/25 words, 25/25 mnemonics agree with the disassembler
    parked at 0xffffffff8010005c: yes   (1.52 s)
    [base_lbah1] /tmp/gxt2/base/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/final_202902/twoleg/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/final_202902/twoleg/raw/base_lbah1.bin
    encodings: 44/44 words, 42/44 mnemonics agree with the disassembler
    parked at 0xffffffff801000a8: yes   (1.52 s)
    [base_lbawr] /tmp/gxt2/base/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/final_202902/twoleg/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/final_202902/twoleg/raw/base_lbawr.bin
    encodings: 1511/1511 words, 1508/1511 mnemonics agree with the disassembler
    parked at 0xffffffff80101794: yes   (1.52 s)

  row          got          head         fix         
  ram:identify 0x00005a5a   want 0x00005a5a   ok
  ram:chs      0x00005a5a   want 0x00005a5a   ok
  ram:sdh      0x00005a5a   want 0x00005a5a   ok
  ram:lba      0x00005a5a   want 0x00005a5a   ok
  ram:lba0     0x00005a5a   want 0x00005a5a   ok
  ram:lbah1    0x00005a5a   want 0x00005a5a   ok
  ram:lbawr    0x00005a5a   want 0x00005a5a   ok
  id w49       0x00000000   want 0x00000000   ok
  id geo       (16, 63)     want H,S!=0       ok
  chs s1       0xffff0000   want 0xffff0000   ok
  chs s2       0xfffe0001   want 0xfffe0001   ok
  chs h1       0xffc0003f   want 0xffc0003f   ok
  chs c1       0xfc0f03f0   want 0xfc0f03f0   ok
  sdh rb       0x000000e5   want 0x000000e5   ok
  sdh rb2      0x000000b3   want 0x000000b3   ok
  sdh rb3      0x0000004c   want 0x0000004c   ok
  sdh rb0      0x00000000   want 0x00000000   ok
  lba 70       0xffba0045   hea
[... 1639 bytes cut ...]
/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/final_202902/twoleg/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/final_202902/twoleg/raw/fix_chs.bin
    encodings: 76/76 words, 76/76 mnemonics agree with the disassembler
    parked at 0xffffffff80100128: yes   (1.52 s)
    [fix_sdh] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/final_202902/twoleg/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/final_202902/twoleg/raw/fix_sdh.bin
    encodings: 22/22 words, 22/22 mnemonics agree with the disassembler
    parked at 0xffffffff80100050: yes   (1.52 s)
    [fix_lba] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/final_202902/twoleg/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/final_202902/twoleg/raw/fix_lba.bin
    encodings: 80/80 words, 76/80 mnemonics agree with the disassembler
    parked at 0xffffffff80100138: yes   (1.52 s)
    [fix_lba0] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/final_202902/twoleg/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/final_202902/twoleg/raw/fix_lba0.bin
    encodings: 25/25 words, 25/25 mnemonics agree with the disassembler
    parked at 0xffffffff8010005c: yes   (1.51 s)
    [fix_lbah1] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/final_202902/twoleg/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/final_202902/twoleg/raw/fix_lbah1.bin
    encodings: 44/44 words, 42/44 mnemonics agree with the disassembler
    parked at 0xffffffff801000a8: yes   (1.52 s)
    [fix_lbawr] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/final_202902/twoleg/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/final_202902/twoleg/raw/fix_lbawr.bin
    encodings: 1511/1511 words, 1508/1511 mnemonics agree with the disassembler
    parked at 0xffffffff80101794: yes   (1.52 s)

  row          got          head         fix         
  ram:identify 0x00005a5a   want 0x00005a5a   ok
  ram:chs      0x00005a5a   want 0x00005a5a   ok
  ram:sdh      0x00005a5a   want 0x00005a5a   ok
  ram:lba      0x00005a5a   want 0x00005a5a   ok
  ram:lba0     0x00005a5a   want 0x00005a5a   ok
  ram:lbah1    0x00005a5a   want 0x00005a5a   ok
  ram:lbawr    0x00005a5a   want 0x00005a5a   ok
  id w49       0x00000000   want 0x00000000   ok
  id geo       (16, 63)     want H,S!=0       ok
  chs s1       0xffff0000   want 0xffff0000   ok
  chs s2       0xfffe0001   want 0xfffe0001   ok
  chs h1       0xffc0003f   want 0xffc0003f   ok
  chs c1       0xfc0f03f0   want 0xfc0f03f0   ok
  sdh rb       0x000000e5   want 0x000000e5   ok
  sdh rb2      0x000000b3   want 0x000000b3   ok
  sdh rb3      0x0000004c   want 0x0000004c   ok
  sdh rb0      0x00000000   want 0x00000000   ok
  lba 70       0xffb90046   head 0xffba0045 fix 0xffb90046 [FIX] ok
  lba 256      0xfeff0100   head 0xfc1003ef fix 0xfeff0100 [FIX] ok
  sel 40       0xffb90046   head 0xffba0045 fix 0xffb90046 [FIX] ok
  lba cylhi    0x00000000   want 0x00000000   ok
  lba 0        0xffff0000   head 0x00000000 fix 0xffff0000 [FIX] ok
  lba h1       0x00000000   head 0xffbc0043 fix 0x00000000 [FIX] ok
  lba h1 ctl   0xfffd0002   want 0xfffd0002   ok
  lba wr       0x88887777   head 0xffb90046 fix 0x88887777 [FIX] ok
  lba wr2      0xffba0045   head 0x88887777 fix 0xffba0045 [FIX] ok
  lba wr h1    0xffbc0043   head 0x66669999 fix 0xffbc0043 [FIX] ok
  lba wr h1s5  0xfffa0005   want 0xfffa0005   ok
  lba wr256    0x33332222   head 0xfeff0100 fix 0x33332222 [FIX] ok
  lba wr256b   0xfc1003ef   head 0x33332222 fix 0xfc1003ef [FIX] ok
  chs wr       0x44445555   want 0x44445555   ok
  chs wr2      0xfff5000a   want 0xfff5000a   ok
  lba wr cylhi 0xffb80047   want 0xffb80047   ok

  33/33 passed
  CONTROL=PASS
  LEG fix VERDICT: PASS

WDC_LBA_CONTROL_fix=OK
WDC_LBA_RESULT_fix=33/33
======================================================================================
VERDICT   every leg passed its own column
WDCLBA_PROBE_DONE


--- final_d9b93abe\RESULTS_gate.txt (5161 bytes) ---
======================================================================================
wdclbaaddr -- RUNG-3 WITNESS + DETECTOR on unmodified `evbmips -e malta`
======================================================================================
date      2026-10-24 20:42:55
machine   evbmips -e malta   LITTLE endian   (machine desc UNMODIFIED)
wdc       physical 0x180001f0 via bus_pci piix4_ide; KSEG1 0xffffffffb80001f0
disk      /tmp/gxt2/work/t4/final_203844/gate/wdc-lba-scratch.img  (4096 sectors; tag n = (n, ~n))
base bin  /tmp/gxt2/fix/gxemul
mode      GATE -- one leg vs the FIX column

--------------------------------------------------------------------------------------
LEG gate -- gate build, judged against the FIX column
--------------------------------------------------------------------------------------
    [gate_identify] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/final_203844/gate/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/final_203844/gate/raw/gate_identify.bin
    encodings: 62/62 words, 62/62 mnemonics agree with the disassembler
    parked at 0xffffffff801000f0: yes   (1.52 s)
    [gate_chs] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/final_203844/gate/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/final_203844/gate/raw/gate_chs.bin
    encodings: 76/76 words, 76/76 mnemonics agree with the disassembler
    parked at 0xffffffff80100128: yes   (1.51 s)
    [gate_sdh] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/final_203844/gate/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/final_203844/gate/raw/gate_sdh.bin
    encodings: 22/22 words, 22/22 mnemonics agree with the disassembler
    parked at 0xffffffff80100050: yes   (1.52 s)
    [gate_lba] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/final_203844/gate/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/final_203844/gate/raw/gate_lba.bin
    encodings: 80/80 words, 76/80 mnemonics agree with the disassembler
    parked at 0xffffffff80100138: yes   (1.52 s)
    [gate_lba0] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/final_203844/gate/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/final_203844/gate/raw/gate_lba0.bin
    encodings: 25/25 words, 25/25 mnemonics agree with the disassembler
    parked at 0xffffffff8010005c: yes   (1.52 s)
    [gate_lbah1] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/final_203844/gate/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/final_203844/gate/raw/gate_lbah1.bin
    encodings: 44/44 words, 42/44 mnemonics agree with the disassembler
    parked at 0xffffffff801000a8: yes   (1.52 s)
    [gate_lbawr] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/final_203844/gate/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/final_203844/gate/raw/gate_lbawr.bin
    encodings: 1511/1511 words, 1508/1511 mnemonics agree with the disassembler
    parked at 0xffffffff80101794: yes   (1.51 s)

  row          got          head         fix         
  ram:identify 0x00005a5a   want 0x00005a5a   ok
  ram:chs      0x00005a5a   want 0x00005a5a   ok
  ram:sdh      0x00005a5a   want 0x00005a5a   ok
  ram:lba      0x00005a5a   want 0x00005a5a   ok
  ram:lba0     0x00005a5a   want 0x00005a5a   ok
  ram:lbah1    0x00005a5a   want 0x00005a5a   ok
  ram:lbawr    0x00005a5a   want 0x00005a5a   ok
  id w49       0x00000000   want 0x00000000   ok
  id geo       (16, 63)     want H,S!=0       ok
  chs s1       0xffff0000   want 0xffff0000   ok
  chs s2       0xfffe0001   want 0xfffe0001   ok
  chs h1       0xffc0003f   want 0xffc0003f   ok
  chs c1       0xfc0f03f0   want 0xfc0f03f0   ok
  sdh rb       0x000000e5   want 0x000000e5   ok
  sdh rb2      0x000000b3   want 0x000000b3   ok
  sdh rb3      0x0000004c   want 0x0000004c   ok
  sdh rb0      0x00000000   want 0x00000000   ok
  lba 70       0xffb90046   head 0xffba0045 fix 0xffb90046 [FIX] ok
  lba 256      0xfeff0100   head 0xfc1003ef fix 0xfeff0100 [FIX] ok
  sel 40       0xffb90046   head 0xffba0045 fix 0xffb90046 [FIX] ok
  lba cylhi    0x00000000   want 0x00000000   ok
  lba 0        0xffff0000   head 0x00000000 fix 0xffff0000 [FIX] ok
  lba h1       0x00000000   head 0xffbc0043 fix 0x00000000 [FIX] ok
  lba h1 ctl   0xfffd0002   want 0xfffd0002   ok
  lba wr       0x88887777   head 0xffb90046 fix 0x88887777 [FIX] ok
  lba wr2      0xffba0045   head 0x88887777 fix 0xffba0045 [FIX] ok
  lba wr h1    0xffbc0043   head 0x66669999 fix 0xffbc0043 [FIX] ok
  lba wr h1s5  0xfffa0005   want 0xfffa0005   ok
  lba wr256    0x33332222   head 0xfeff0100 fix 0x33332222 [FIX] ok
  lba wr256b   0xfc1003ef   head 0x33332222 fix 0xfc1003ef [FIX] ok
  chs wr       0x44445555   want 0x44445555   ok
  chs wr2      0xfff5000a   want 0xfff5000a   ok
  lba wr cylhi 0xffb80047   want 0xffb80047   ok

  33/33 passed
  CONTROL=PASS
  LEG gate VERDICT: PASS

WDC_LBA_CONTROL=OK
WDC_LBA_RESULT=33/33
======================================================================================
VERDICT   every leg passed its own column
WDCLBA_PROBE_DONE


--- final_d9b93abe\RESULTS_twoleg.txt (9639 bytes) ---
======================================================================================
wdclbaaddr -- RUNG-3 WITNESS + DETECTOR on unmodified `evbmips -e malta`
======================================================================================
date      2026-10-24 20:38:44
machine   evbmips -e malta   LITTLE endian   (machine desc UNMODIFIED)
wdc       physical 0x180001f0 via bus_pci piix4_ide; KSEG1 0xffffffffb80001f0
disk      /tmp/gxt2/work/t4/final_203844/twoleg/wdc-lba-scratch.img  (4096 sectors; tag n = (n, ~n))
base bin  /tmp/gxt2/base/gxemul
fix bin   /tmp/gxt2/fix/gxemul

--------------------------------------------------------------------------------------
LEG base -- base build, judged against the HEAD column
--------------------------------------------------------------------------------------
    [base_identify] /tmp/gxt2/base/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/final_203844/twoleg/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/final_203844/twoleg/raw/base_identify.bin
    encodings: 62/62 words, 62/62 mnemonics agree with the disassembler
    parked at 0xffffffff801000f0: yes   (1.51 s)
    [base_chs] /tmp/gxt2/base/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/final_203844/twoleg/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/final_203844/twoleg/raw/base_chs.bin
    encodings: 76/76 words, 76/76 mnemonics agree with the disassembler
    parked at 0xffffffff80100128: yes   (1.51 s)
    [base_sdh] /tmp/gxt2/base/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/final_203844/twoleg/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/final_203844/twoleg/raw/base_sdh.bin
    encodings: 22/22 words, 22/22 mnemonics agree with the disassembler
    parked at 0xffffffff80100050: yes   (1.51 s)
    [base_lba] /tmp/gxt2/base/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/final_203844/twoleg/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/final_203844/twoleg/raw/base_lba.bin
    encodings: 80/80 words, 76/80 mnemonics agree with the disassembler
    parked at 0xffffffff80100138: yes   (1.52 s)
    [base_lba0] /tmp/gxt2/base/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/final_203844/twoleg/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/final_203844/twoleg/raw/base_lba0.bin
    encodings: 25/25 words, 25/25 mnemonics agree with the disassembler
    parked at 0xffffffff8010005c: yes   (1.51 s)
    [base_lbah1] /tmp/gxt2/base/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/final_203844/twoleg/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/final_203844/twoleg/raw/base_lbah1.bin
    encodings: 44/44 words, 42/44 mnemonics agree with the disassembler
    parked at 0xffffffff801000a8: yes   (1.52 s)
    [base_lbawr] /tmp/gxt2/base/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/final_203844/twoleg/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/final_203844/twoleg/raw/base_lbawr.bin
    encodings: 1511/1511 words, 1508/1511 mnemonics agree with the disassembler
    parked at 0xffffffff80101794: yes   (1.52 s)

  row          got          head         fix         
  ram:identify 0x00005a5a   want 0x00005a5a   ok
  ram:chs      0x00005a5a   want 0x00005a5a   ok
  ram:sdh      0x00005a5a   want 0x00005a5a   ok
  ram:lba      0x00005a5a   want 0x00005a5a   ok
  ram:lba0     0x00005a5a   want 0x00005a5a   ok
  ram:lbah1    0x00005a5a   want 0x00005a5a   ok
  ram:lbawr    0x00005a5a   want 0x00005a5a   ok
  id w49       0x00000000   want 0x00000000   ok
  id geo       (16, 63)     want H,S!=0       ok
  chs s1       0xffff0000   want 0xffff0000   ok
  chs s2       0xfffe0001   want 0xfffe0001   ok
  chs h1       0xffc0003f   want 0xffc0003f   ok
  chs c1       0xfc0f03f0   want 0xfc0f03f0   ok
  sdh rb       0x000000e5   want 0x000000e5   ok
  sdh rb2      0x000000b3   want 0x000000b3   ok
  sdh rb3      0x0000004c   want 0x0000004c   ok
  sdh rb0      0x00000000   want 0x00000000   ok
  lba 70       0xffba0045   hea
[... 1639 bytes cut ...]
/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/final_203844/twoleg/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/final_203844/twoleg/raw/fix_chs.bin
    encodings: 76/76 words, 76/76 mnemonics agree with the disassembler
    parked at 0xffffffff80100128: yes   (1.51 s)
    [fix_sdh] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/final_203844/twoleg/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/final_203844/twoleg/raw/fix_sdh.bin
    encodings: 22/22 words, 22/22 mnemonics agree with the disassembler
    parked at 0xffffffff80100050: yes   (1.51 s)
    [fix_lba] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/final_203844/twoleg/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/final_203844/twoleg/raw/fix_lba.bin
    encodings: 80/80 words, 76/80 mnemonics agree with the disassembler
    parked at 0xffffffff80100138: yes   (1.51 s)
    [fix_lba0] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/final_203844/twoleg/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/final_203844/twoleg/raw/fix_lba0.bin
    encodings: 25/25 words, 25/25 mnemonics agree with the disassembler
    parked at 0xffffffff8010005c: yes   (1.52 s)
    [fix_lbah1] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/final_203844/twoleg/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/final_203844/twoleg/raw/fix_lbah1.bin
    encodings: 44/44 words, 42/44 mnemonics agree with the disassembler
    parked at 0xffffffff801000a8: yes   (1.51 s)
    [fix_lbawr] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/final_203844/twoleg/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/final_203844/twoleg/raw/fix_lbawr.bin
    encodings: 1511/1511 words, 1508/1511 mnemonics agree with the disassembler
    parked at 0xffffffff80101794: yes   (1.51 s)

  row          got          head         fix         
  ram:identify 0x00005a5a   want 0x00005a5a   ok
  ram:chs      0x00005a5a   want 0x00005a5a   ok
  ram:sdh      0x00005a5a   want 0x00005a5a   ok
  ram:lba      0x00005a5a   want 0x00005a5a   ok
  ram:lba0     0x00005a5a   want 0x00005a5a   ok
  ram:lbah1    0x00005a5a   want 0x00005a5a   ok
  ram:lbawr    0x00005a5a   want 0x00005a5a   ok
  id w49       0x00000000   want 0x00000000   ok
  id geo       (16, 63)     want H,S!=0       ok
  chs s1       0xffff0000   want 0xffff0000   ok
  chs s2       0xfffe0001   want 0xfffe0001   ok
  chs h1       0xffc0003f   want 0xffc0003f   ok
  chs c1       0xfc0f03f0   want 0xfc0f03f0   ok
  sdh rb       0x000000e5   want 0x000000e5   ok
  sdh rb2      0x000000b3   want 0x000000b3   ok
  sdh rb3      0x0000004c   want 0x0000004c   ok
  sdh rb0      0x00000000   want 0x00000000   ok
  lba 70       0xffb90046   head 0xffba0045 fix 0xffb90046 [FIX] ok
  lba 256      0xfeff0100   head 0xfc1003ef fix 0xfeff0100 [FIX] ok
  sel 40       0xffb90046   head 0xffba0045 fix 0xffb90046 [FIX] ok
  lba cylhi    0x00000000   want 0x00000000   ok
  lba 0        0xffff0000   head 0x00000000 fix 0xffff0000 [FIX] ok
  lba h1       0x00000000   head 0xffbc0043 fix 0x00000000 [FIX] ok
  lba h1 ctl   0xfffd0002   want 0xfffd0002   ok
  lba wr       0x88887777   head 0xffb90046 fix 0x88887777 [FIX] ok
  lba wr2      0xffba0045   head 0x88887777 fix 0xffba0045 [FIX] ok
  lba wr h1    0xffbc0043   head 0x66669999 fix 0xffbc0043 [FIX] ok
  lba wr h1s5  0xfffa0005   want 0xfffa0005   ok
  lba wr256    0x33332222   head 0xfeff0100 fix 0x33332222 [FIX] ok
  lba wr256b   0xfc1003ef   head 0x33332222 fix 0xfc1003ef [FIX] ok
  chs wr       0x44445555   want 0x44445555   ok
  chs wr2      0xfff5000a   want 0xfff5000a   ok
  lba wr cylhi 0xffb80047   want 0xffb80047   ok

  33/33 passed
  CONTROL=PASS
  LEG fix VERDICT: PASS

WDC_LBA_CONTROL_fix=OK
WDC_LBA_RESULT_fix=33/33
======================================================================================
VERDICT   every leg passed its own column
WDCLBA_PROBE_DONE


--- gate\RESULTS.txt (5071 bytes) ---
======================================================================================
wdclbaaddr -- RUNG-3 WITNESS + DETECTOR on unmodified `evbmips -e malta`
======================================================================================
date      2026-10-24 19:08:57
machine   evbmips -e malta   LITTLE endian   (machine desc UNMODIFIED)
wdc       physical 0x180001f0 via bus_pci piix4_ide; KSEG1 0xffffffffb80001f0
disk      /tmp/gxt2/work/t4/gate_190857/wdc-lba-scratch.img  (4096 sectors; tag n = (n, ~n))
base bin  /tmp/gxt2/fix/gxemul
mode      GATE -- one leg vs the FIX column

--------------------------------------------------------------------------------------
LEG gate -- gate build, judged against the FIX column
--------------------------------------------------------------------------------------
    [gate_identify] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/gate_190857/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/gate_190857/raw/gate_identify.bin
    encodings: 62/62 words, 62/62 mnemonics agree with the disassembler
    parked at 0xffffffff801000f0: yes   (1.52 s)
    [gate_chs] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/gate_190857/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/gate_190857/raw/gate_chs.bin
    encodings: 76/76 words, 76/76 mnemonics agree with the disassembler
    parked at 0xffffffff80100128: yes   (1.52 s)
    [gate_sdh] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/gate_190857/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/gate_190857/raw/gate_sdh.bin
    encodings: 22/22 words, 22/22 mnemonics agree with the disassembler
    parked at 0xffffffff80100050: yes   (1.52 s)
    [gate_lba] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/gate_190857/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/gate_190857/raw/gate_lba.bin
    encodings: 80/80 words, 76/80 mnemonics agree with the disassembler
    parked at 0xffffffff80100138: yes   (1.52 s)
    [gate_lba0] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/gate_190857/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/gate_190857/raw/gate_lba0.bin
    encodings: 25/25 words, 25/25 mnemonics agree with the disassembler
    parked at 0xffffffff8010005c: yes   (1.52 s)
    [gate_lbah1] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/gate_190857/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/gate_190857/raw/gate_lbah1.bin
    encodings: 44/44 words, 42/44 mnemonics agree with the disassembler
    parked at 0xffffffff801000a8: yes   (1.52 s)
    [gate_lbawr] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/gate_190857/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/gate_190857/raw/gate_lbawr.bin
    encodings: 1511/1511 words, 1508/1511 mnemonics agree with the disassembler
    parked at 0xffffffff80101794: yes   (1.52 s)

  row          got          head         fix         
  ram:identify 0x00005a5a   want 0x00005a5a   ok
  ram:chs      0x00005a5a   want 0x00005a5a   ok
  ram:sdh      0x00005a5a   want 0x00005a5a   ok
  ram:lba      0x00005a5a   want 0x00005a5a   ok
  ram:lba0     0x00005a5a   want 0x00005a5a   ok
  ram:lbah1    0x00005a5a   want 0x00005a5a   ok
  ram:lbawr    0x00005a5a   want 0x00005a5a   ok
  id w49       0x00000000   want 0x00000000   ok
  id geo       (16, 63)     want H,S!=0       ok
  chs s1       0xffff0000   want 0xffff0000   ok
  chs s2       0xfffe0001   want 0xfffe0001   ok
  chs h1       0xffc0003f   want 0xffc0003f   ok
  chs c1       0xfc0f03f0   want 0xfc0f03f0   ok
  sdh rb       0x000000e5   want 0x000000e5   ok
  sdh rb2      0x000000b3   want 0x000000b3   ok
  sdh rb3      0x0000004c   want 0x0000004c   ok
  sdh rb0      0x00000000   want 0x00000000   ok
  lba 70       0xffb90046   head 0xffba0045 fix 0xffb90046 [FIX] ok
  lba 256      0xfeff0100   head 0xfc1003ef fix 0xfeff0100 [FIX] ok
  sel 40       0xffb90046   head 0xffba0045 fix 0xffb90046 [FIX] ok
  lba cylhi    0x00000000   want 0x00000000   ok
  lba 0        0xffff0000   head 0x00000000 fix 0xffff0000 [FIX] ok
  lba h1       0x00000000   head 0xffbc0043 fix 0x00000000 [FIX] ok
  lba h1 ctl   0xfffd0002   want 0xfffd0002   ok
  lba wr       0x88887777   head 0xffb90046 fix 0x88887777 [FIX] ok
  lba wr2      0xffba0045   head 0x88887777 fix 0xffba0045 [FIX] ok
  lba wr h1    0xffbc0043   head 0x66669999 fix 0xffbc0043 [FIX] ok
  lba wr h1s5  0xfffa0005   want 0xfffa0005   ok
  lba wr256    0x33332222   head 0xfeff0100 fix 0x33332222 [FIX] ok
  lba wr256b   0xfc1003ef   head 0x33332222 fix 0xfc1003ef [FIX] ok
  chs wr       0x44445555   want 0x44445555   ok
  chs wr2      0xfff5000a   want 0xfff5000a   ok
  lba wr cylhi 0xffb80047   want 0xffb80047   ok

  33/33 passed
  CONTROL=PASS
  LEG gate VERDICT: PASS

WDC_LBA_CONTROL=OK
WDC_LBA_RESULT=33/33
======================================================================================
VERDICT   every leg passed its own column
WDCLBA_PROBE_DONE


--- twoleg\RESULTS.txt (9465 bytes) ---
======================================================================================
wdclbaaddr -- RUNG-3 WITNESS + DETECTOR on unmodified `evbmips -e malta`
======================================================================================
date      2026-10-24 19:04:46
machine   evbmips -e malta   LITTLE endian   (machine desc UNMODIFIED)
wdc       physical 0x180001f0 via bus_pci piix4_ide; KSEG1 0xffffffffb80001f0
disk      /tmp/gxt2/work/t4/twoleg_190446/wdc-lba-scratch.img  (4096 sectors; tag n = (n, ~n))
base bin  /tmp/gxt2/base/gxemul
fix bin   /tmp/gxt2/fix/gxemul

--------------------------------------------------------------------------------------
LEG base -- base build, judged against the HEAD column
--------------------------------------------------------------------------------------
    [base_identify] /tmp/gxt2/base/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/twoleg_190446/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/twoleg_190446/raw/base_identify.bin
    encodings: 62/62 words, 62/62 mnemonics agree with the disassembler
    parked at 0xffffffff801000f0: yes   (1.51 s)
    [base_chs] /tmp/gxt2/base/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/twoleg_190446/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/twoleg_190446/raw/base_chs.bin
    encodings: 76/76 words, 76/76 mnemonics agree with the disassembler
    parked at 0xffffffff80100128: yes   (1.52 s)
    [base_sdh] /tmp/gxt2/base/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/twoleg_190446/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/twoleg_190446/raw/base_sdh.bin
    encodings: 22/22 words, 22/22 mnemonics agree with the disassembler
    parked at 0xffffffff80100050: yes   (1.52 s)
    [base_lba] /tmp/gxt2/base/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/twoleg_190446/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/twoleg_190446/raw/base_lba.bin
    encodings: 80/80 words, 76/80 mnemonics agree with the disassembler
    parked at 0xffffffff80100138: yes   (1.52 s)
    [base_lba0] /tmp/gxt2/base/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/twoleg_190446/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/twoleg_190446/raw/base_lba0.bin
    encodings: 25/25 words, 25/25 mnemonics agree with the disassembler
    parked at 0xffffffff8010005c: yes   (1.52 s)
    [base_lbah1] /tmp/gxt2/base/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/twoleg_190446/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/twoleg_190446/raw/base_lbah1.bin
    encodings: 44/44 words, 42/44 mnemonics agree with the disassembler
    parked at 0xffffffff801000a8: yes   (1.51 s)
    [base_lbawr] /tmp/gxt2/base/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/twoleg_190446/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/twoleg_190446/raw/base_lbawr.bin
    encodings: 1511/1511 words, 1508/1511 mnemonics agree with the disassembler
    parked at 0xffffffff80101794: yes   (1.52 s)

  row          got          head         fix         
  ram:identify 0x00005a5a   want 0x00005a5a   ok
  ram:chs      0x00005a5a   want 0x00005a5a   ok
  ram:sdh      0x00005a5a   want 0x00005a5a   ok
  ram:lba      0x00005a5a   want 0x00005a5a   ok
  ram:lba0     0x00005a5a   want 0x00005a5a   ok
  ram:lbah1    0x00005a5a   want 0x00005a5a   ok
  ram:lbawr    0x00005a5a   want 0x00005a5a   ok
  id w49       0x00000000   want 0x00000000   ok
  id geo       (16, 63)     want H,S!=0       ok
  chs s1       0xffff0000   want 0xffff0000   ok
  chs s2       0xfffe0001   want 0xfffe0001   ok
  chs h1       0xffc0003f   want 0xffc0003f   ok
  chs c1       0xfc0f03f0   want 0xfc0f03f0   ok
  sdh rb       0x000000e5   want 0x000000e5   ok
  sdh rb2      0x000000b3   want 0x000000b3   ok
  sdh rb3      0x0000004c   want 0x0000004c   ok
  sdh rb0      0x00000000   want 0x00000000   ok
  lba 70       0xffba0045   head 0xffba0045 fix 0xffb90046 [HEAD] ok
  lba 256      0xfc1003ef   head 0xfc1003ef fix 0xfe
[... 1465 bytes cut ...]
parked at 0xffffffff801000f0: yes   (1.52 s)
    [fix_chs] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/twoleg_190446/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/twoleg_190446/raw/fix_chs.bin
    encodings: 76/76 words, 76/76 mnemonics agree with the disassembler
    parked at 0xffffffff80100128: yes   (1.52 s)
    [fix_sdh] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/twoleg_190446/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/twoleg_190446/raw/fix_sdh.bin
    encodings: 22/22 words, 22/22 mnemonics agree with the disassembler
    parked at 0xffffffff80100050: yes   (1.52 s)
    [fix_lba] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/twoleg_190446/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/twoleg_190446/raw/fix_lba.bin
    encodings: 80/80 words, 76/80 mnemonics agree with the disassembler
    parked at 0xffffffff80100138: yes   (1.52 s)
    [fix_lba0] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/twoleg_190446/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/twoleg_190446/raw/fix_lba0.bin
    encodings: 25/25 words, 25/25 mnemonics agree with the disassembler
    parked at 0xffffffff8010005c: yes   (1.52 s)
    [fix_lbah1] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/twoleg_190446/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/twoleg_190446/raw/fix_lbah1.bin
    encodings: 44/44 words, 42/44 mnemonics agree with the disassembler
    parked at 0xffffffff801000a8: yes   (1.52 s)
    [fix_lbawr] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/twoleg_190446/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/twoleg_190446/raw/fix_lbawr.bin
    encodings: 1511/1511 words, 1508/1511 mnemonics agree with the disassembler
    parked at 0xffffffff80101794: yes   (1.52 s)

  row          got          head         fix         
  ram:identify 0x00005a5a   want 0x00005a5a   ok
  ram:chs      0x00005a5a   want 0x00005a5a   ok
  ram:sdh      0x00005a5a   want 0x00005a5a   ok
  ram:lba      0x00005a5a   want 0x00005a5a   ok
  ram:lba0     0x00005a5a   want 0x00005a5a   ok
  ram:lbah1    0x00005a5a   want 0x00005a5a   ok
  ram:lbawr    0x00005a5a   want 0x00005a5a   ok
  id w49       0x00000000   want 0x00000000   ok
  id geo       (16, 63)     want H,S!=0       ok
  chs s1       0xffff0000   want 0xffff0000   ok
  chs s2       0xfffe0001   want 0xfffe0001   ok
  chs h1       0xffc0003f   want 0xffc0003f   ok
  chs c1       0xfc0f03f0   want 0xfc0f03f0   ok
  sdh rb       0x000000e5   want 0x000000e5   ok
  sdh rb2      0x000000b3   want 0x000000b3   ok
  sdh rb3      0x0000004c   want 0x0000004c   ok
  sdh rb0      0x00000000   want 0x00000000   ok
  lba 70       0xffb90046   head 0xffba0045 fix 0xffb90046 [FIX] ok
  lba 256      0xfeff0100   head 0xfc1003ef fix 0xfeff0100 [FIX] ok
  sel 40       0xffb90046   head 0xffba0045 fix 0xffb90046 [FIX] ok
  lba cylhi    0x00000000   want 0x00000000   ok
  lba 0        0xffff0000   head 0x00000000 fix 0xffff0000 [FIX] ok
  lba h1       0x00000000   head 0xffbc0043 fix 0x00000000 [FIX] ok
  lba h1 ctl   0xfffd0002   want 0xfffd0002   ok
  lba wr       0x88887777   head 0xffb90046 fix 0x88887777 [FIX] ok
  lba wr2      0xffba0045   head 0x88887777 fix 0xffba0045 [FIX] ok
  lba wr h1    0xffbc0043   head 0x66669999 fix 0xffbc0043 [FIX] ok
  lba wr h1s5  0xfffa0005   want 0xfffa0005   ok
  lba wr256    0x33332222   head 0xfeff0100 fix 0x33332222 [FIX] ok
  lba wr256b   0xfc1003ef   head 0x33332222 fix 0xfc1003ef [FIX] ok
  chs wr       0x44445555   want 0x44445555   ok
  chs wr2      0xfff5000a   want 0xfff5000a   ok
  lba wr cylhi 0xffb80047   want 0xffb80047   ok

  33/33 passed
  CONTROL=PASS
  LEG fix VERDICT: PASS

WDC_LBA_CONTROL_fix=OK
WDC_LBA_RESULT_fix=33/33
======================================================================================
VERDICT   every leg passed its own column
WDCLBA_PROBE_DONE



## 6. THE DETECTOR DIFF (frozen witness copy -> shipped `regress/wdc_lba_probe.py`, 827 lines, md5 5e4ecd477c2a4acbcb79d4382ffa4183)

```diff
diff --git a/regress/artifacts/wdclbaaddr/witness_20261024/wdc_lba_probe.frozen.py b/regress/wdc_lba_probe.py
index e9649057..b3184c25 100644
--- a/regress/artifacts/wdclbaaddr/witness_20261024/wdc_lba_probe.frozen.py
+++ b/regress/wdc_lba_probe.py
@@ -7,70 +7,147 @@ operation, not a machine edit.
 
 THE DEFECT (all in src/devices/dev_wdc.c at HEAD; durable keys are grep anchors):
 
-    grep -n 'case wd_sdh:'        dev_wdc.c   -- SDH (taskfile offset 6) decodes the
-        lba flag from BIT 5 on write (`d->lba = (idata >> 5) & 1;`) and recomposes it
-        the same way on read (byte-exact: the four fields partition the byte).  ATA
-        puts the LBA flag in BIT 6 (0x40); bits 7 and 5 are the obsolete "always 1"
-        bits, so the CHS select byte is 0xa0 and the LBA select byte is 0xe0.  Under
-        the HEAD decode every 0xe0 is read as head=0, and d->lba is never consulted
-        for an address anyway:
+    grep -n 'case wd_sdh:'        dev_wdc.c   -- SDH (taskfile offset 6) decoded the
+        lba flag from BIT 5 on write (`d->lba = (idata >> 5) & 1;`) and recomposed it
+        the same way on read.  ATA puts the LBA flag in BIT 6 (0x40); bits 7 and 5 are
+        the obsolete "always 1" bits, so the CHS select byte is 0xa0 and the LBA select
+        byte is 0xe0.  Under HEAD's bit-5 decode every CHS select byte 0xa0 ALSO sets
+        `lba = 1`, which is why the FreeBSD patch could not be taken as a patch; and
+        every 0xe0 is read as head = 0.  `d->lba` reaches no address computation on
+        HEAD anyway:
     grep -n 'void wdc__read'      dev_wdc.c   -- offset = 512 * (sector - 1 +
         head*spt + heads*spt*cyl); the LBA28 alternative
-        512 * (((head & 0xf) << 24) + (cyl << 8) + sector) sits inside `#if 0`.
+        512 * (((head & 0xf) << 24) + (cyl << 8) + sector) sat inside `#if 0`.
     grep -n 'void wdc__write'     dev_wdc.c   -- the same CHS/LBA pair on the write
         side.
     grep -n '49: capabilities'    dev_wdc.c   -- IDENTIFY word 49 stays 0 this round
-        (LBA is not advertised); words 3 and 6 carry heads and spt.
+        (LBA is implemented but not advertised); words 3 and 6 carry heads and spt.
 
-So a command issued in LBA mode is served from the CHS interpretation of the same
-taskfile bytes.  The fix decodes lba from bit 6, keeps the readback byte-exact, and
-enables the LBA28 formula at both sites.
+So a command issued in LBA mode was served from the CHS interpretation of the same
+taskfile bytes.  The fix decodes lba from bit 6, keeps the read-back byte-exact through
+the renamed reserved field `sdh_resv`, and enables the 64-bit LBA28 formula at both
+sites.
+
+THE PRE-FIX WITNESS is the as-run copy of this probe's FIRST revision, a 19-row instrument:
+regress/artifacts/wdclbaaddr/witness_20261024/wdc_lba_probe.frozen.py (md5 8f3632ff).
+On the committed build, before any edit, its base leg scored 19/19 (19-row HEAD column;
+RESULTS_base.txt there); after the fix the same script's fixed leg scored 19/19 (19-row
+FIX column; RESULTS_fix.txt there).  THIS revision is the shipping DETECTOR (ledger row
+wdclbaaddr, round #572), not the witness instrument.
 
 THE VEHICLE copies regress/wdc_altoffset_probe.py: the command line and disk prefix,
 the pty/expect debugger driver (print/breakpoint/continue idioms), the MIPS encoders
-(I, lui, ori, addiu, sb, lbu, beq, emit) plus lhu (opcode 0x25) and sh (opcode 0x29)
-added in the same style, the KSEG1 register addresses (0xb80001f0 + N: 0 data 16-bit,
-2 seccnt, 3 sector, 4 cyl_lo, 5 cyl_hi, 6 SDH, 7 command/status), the per-instruction
-disassembly self-check, and the row/verdict/sentinel protocol.  malta is LITTLE-endian;
-the data port is read 16 bits at a time (lhu), 256 words per sector.  Every instruction
-is encoded from the field layout -- never a typed-in machine-code constant.
+(I, lui, ori, addiu, sb, lbu, beq, emit) plus lhu (opcode 0x25), sh (opcode 0x29) and
+lw (opcode 0x23) added in the same style, the KSEG1 register addresses (0xb80001f0 + N:
+0 data 16-bit, 2 seccnt, 3 sector, 4 cyl_lo, 5 cyl_hi, 6 SDH, 7 command/status), the
+per-instruction disassembly self-check, and the row/verdict/sentinel protocol.  malta is
+LITTLE-endian; the data port is read 16 bits at a time (lhu), 256 words per sector.
+Every instruction is encoded from the field layout -- never a typed-in machine-code
+constant.  A tag read is two 16-bit pops stored to adjacent RAM halfwords and read back
+as one 32-bit word (lw), so one capture register holds the whole (word1<<16)|word0 tag.
 
 THE DISK IMAGE (4096 sectors of 512 bytes, generated under the output dir, never the
-repo):  sector n carries, as little-endian 16-bit words, word0 = n & 0xffff,
+repo): sector n carries, as little-endian 16-bit words, word0 = n & 0xffff,
 word1 = (~n) & 0xffff, word2 = 0x4c42 ("LB"), word3 = 0x4100 ("A\\0"), rest zero.  The
 TAG of a sector is the pair (word0, word1) and is a DEVICE SIGNATURE: no RAM cell holds
-it, so a read that returns a tag proves the bytes came through the disk model.  The
-probe reads word0 and word1 and compares the combined value (word1 << 16) | word0.
-
-THE ROWS (one fresh emulator process per session; H = IDENTIFY word 3, S = word 6):
-
-    row            session   want on COMMITTED (HEAD)         want on FIXED
-    live ram       every     0x5a5a                           0x5a5a
-    id w49         identify  0x0000                            0x0000
-    id geo         identify  words 3,6 nonzero                 same
-    chs s1         chs       tag 0                             tag 0
-    chs s2         chs       tag 1                             tag 1
-    chs h1         chs       tag S                             tag S
-    sdh rb         sdh       0xe5 (byte-exact readback)        0xe5
-    sdh rb2        sdh       0xb3                              0xb3
-    lba 70         lba       tag 69 (served as CHS sector 70)  tag 70
-    lba 256        lba       tag (H*S - 1)                     tag 256
-    lba 0          lba0      NOT tag 0 (served value recorded) tag 0
-    lba wr         lbawr     tag 70 (write landed at sec 69)   0x7777/0x8888
-    lba wr2        lbawr     0x7777/0x8888                     tag 69
-    neg appar      --        a forced-mismatch line must FAIL  same
-
-lba 70, lba 256, lba 0, lba wr, lba wr2 are the SYMPTOM rows: red on HEAD against the
-FIXED wants, and BOTH wants are printed so a reader sees the sector actually served
-rather than a bare FAIL.  Every other row is an identity row that must hold on both
-legs.
-
-Usage:  wdc_lba_probe.py <base_bin> <fix_bin or -> <outdir>
-Leg 1 runs <base_bin> against the HEAD column; if <fix_bin> is "-" the fixed leg is
-skipped (the WITNESS run, before any fix exists).  Each leg prints its rows, N/M passed,
-CONTROL=PASS|FAIL; the file ends with the sentinel WDCLBA_PROBE_DONE once.  Every
-session's raw transcript is kept under <outdir>/raw/<leg>_<session>.txt.  Exit status 0
-only when every leg passed its own column.
+it, so a read that returns a tag proves the bytes came through the disk model.  IDENTIFY
+geometry H = 16, S = 63; logical capacity rounds up to 5040 sectors, of which 4096 are
+backed.  Payload words are chosen so no written payload equals any in-range sector tag
+on this image (every payload maps to n >= 4096).
+
+THE ROWS (one fresh emulator process per session; H = IDENTIFY word 3 = 16, S = word 6 = 63;
+"zeros" is 0x00000000; a payload reads back as (word1 << 16) | word0; every want is a
+literal):
+
+    session   row            HEAD (committed)             FIX
+    every     ram:<session>  0x5a5a                       0x5a5a
+    identify  id w49         0x0000                       0x0000
+              id geo         H != 0 and S >= 10           same
+    chs       chs s1 / s2    tag 0 / tag 1                same
+              chs h1         tag S        (0xa1, s1)      same
+              chs c1         tag H*S      (0xa0, s1, cyl_lo 1)   same
+    sdh       sdh rb, rb2    0xe5, 0xb3                   same
+              sdh rb3        0x4c (bits 7 and 5 clear)    same
+              sdh rb0        0x00 (write 0xe5, then 0x00) same
+    lba       lba 70         tag 69       (0xe0, s70)     tag 70
+              lba 256        tag H*S-1    (0xe0, s0, cyl_lo 1)   tag 256
+              sel 40         tag 69       (0x40, s70)     tag 70
+              lba cylhi      zeros        (0xe0, s70, cyl_hi 1)  zeros
+    lba0      lba 0          zeros        (0xe0, s0)      tag 0
+    lbah1     lba h1         tag S+4      (0xe1, s5)      zeros (LBA 0x1000005, past the file)
+              lba h1 ctl     tag 2        (0xa0, s3)      tag 2
+    lbawr     five single-sector writes, then nine reads through valid CHS triples:
+              lba wr         tag 70       (W 0xe0 s70; R 0xa1 s8)          payload 0x88887777
+              lba wr2        payload      (R 0xa1 s7, index 69)            tag 69
+              lba wr h1      payload      (W 0xe1 s5; R 0xa1 s5)           tag 67 (refused)
+              lba wr h1s5    tag 5        (R 0xa0 s6)                      tag 5
+              lba wr256      tag 256      (W 0xe0 s0 cyl_lo 1; R 0xa4 s5)  payload 0x33332222
+              lba wr256b     payload      (R 0xaf s63, index 1007)         tag 1007
+              chs wr         payload      (W+R 0xa0 s10, index 9)          payload 0x44445555
+              chs wr2        tag 10       (R 0xa0 s11)                     tag 10
+              lba wr cylhi   tag 71       (W 0xe0 s71 cyl_hi 1; R 0xa1 s9) tag 71 (refused)
+    The sectors the write session touches -- 5, 9, 10, 67, 69, 70, 71, 256, 1007 -- are
+    pairwise disjoint.  Ten SYMPTOM rows differ HEAD vs FIX; the 23 identity rows agree.
+
+THE CONTRACT (clause e).  Kills are cited from regress/artifacts/wdclbaaddr/detector_20261024/
+SCORES.txt (table 1) and SCORES2.txt (table 2): GATE mode, FIX column, 33 rows, one mutant
+per scratch build.
+CATCHES
+  * the decode moved off bit 6, onto bit 7, or qualified with bit 5 -- V1 and V2 17/33 (the
+    CHS rows, the CHS-select read-backs, sel 40, sdh rb2/rb3), V3 31/33 (sel 40, sdh rb3);
+  * the LBA arm disabled, unconditional, or qualified on head, cyl or sector -- at the read
+    site V14w 28/33, V13r 19/33, V4r 32/33 (lba h1), V5r 32/33 (lba 256), V6r 31/33
+    (lba 256, lba 0); at the write site V14r 28/33, V13w 31/33 (chs wr, chs wr2), V4w 32/33
+    (lba wr h1), V5w and V6w 31/33 (lba wr256, lba wr256b);
+  * the head term dropped, or `sector - 1`, in the LBA arm at either site -- V8 32/33
+    (lba h1), V8w 32/33 (lba wr h1s5), V11 29/33 (lba 70, lba 256, sel 40, lba 0), V11w
+    30/33 (lba wr, lba wr2, lba wr256); a READ-site head shift that still lands inside the
+    file, k <= 11 -- V9r8 32/33 (lba h1);
+  * the cyl_lo << 8-only cylinder term at either site -- V10r 32/33 (lba cylhi), V10w 32/33
+    (lba wr cylhi);
+  * the write-site arm placed below the write_offset capture -- V20 28/33;
+  * the read-back losing bit 6, dropping reserved bit 5, or forcing bits 7 and 5 -- V18,
+    V17, V16, 31/33 each (two of the four sdh rb* rows each);
+  * word 49 advertised nonzero -- id w49 reads word 49 directly.  The one CATCHES line with
+    no kill in these tables: no word-49 mutant was built here; the offline differential's
+    row_no_lba_claim (regress/diff_wdc_identify.c) pins the same two bytes.
+MEASURED, NOT PROMISED: the unwidened 32-bit LBA product (V15) is undefined behaviour; on
+  THIS build (cc -O3) it wrapped to sector 5 and scored 32/33 (lba h1).  That score does
+  not generalise: a compiler that widens the product serves zeros, exactly like the fix.
+BLIND / DISCLOSED
+  * cyl_hi >= 1 DESTINATIONS: both the CHS and the LBA reading fall past a 4096-sector
+    image, so lba cylhi / lba wr cylhi see only the cyl_lo-only variant at each site; V7,
+    the cyl_hi-conditioned arm, stays blind here (measured: 33/33 with both sites
+    conditioned, SCORES_V12_V7.txt).  The larger-image row (wdclbaimage) is FILED.
+  * the band LBA 4096-5039 is advertised capacity served as a short zero-filled read (the
+    #416 design) while the CHS reading of the same bytes is refused -- the guest sees zeros
+    either way.
+  * a WRITE-site head shift (only the read site is rowed for k <= 11); head shifts that
+    miss the file (k >= 12; k >= 32 undefined); `& 0xf` removed (EQUIVALENT -- the one head
+    writer masks already; V12 measured 33/33, SCORES_V12_V7.txt); drive 1 and big-endian
+    guests; MULTI / seccnt > 1; the 48-bit
+    commands; the deleted printf; a past-end completion carrying no error bit (the
+    wdcmediastatus row, FILED); the both-out-of-range subdomain.
+  * every read-back value has bit 7 == bit 5 (0xe5, 0xb3 set; 0x4c, 0x00 clear), so a
+    mutant that derives one reserved bit from the other is invisible.
+ANCHOR: every LBA moved by one sector at both sites -- T_m1 26/33 (lba 70, lba 256, sel 40,
+  lba 0, lba wr, lba wr2, lba wr256) and T_p1 26/33 (lba 70, lba 256, sel 40, lba 0,
+  lba wr, lba wr256, lba wr cylhi).  The tags name WHICH sector was served through image
+  content the decode does not produce, so position is pinned absolutely.
+HARNESS SELF-CHECK (not scored): main() asserts that the comparator fails a mismatch and
+  treats a missing value as a failure.  It replaces the old scored `neg appar` row, whose
+  got/want were constants and which therefore passed on every run.
+
+Usage:  wdc_lba_probe.py <base_bin> <fix_bin | GATE | -> <outdir>
+    <base> -   <outdir>   WITNESS: base leg only, judged against the HEAD column.
+    <base> <fix> <outdir> two legs: base vs HEAD, fix vs FIX; prints WDC_LBA_RESULT_base=
+                          / _fix= and WDC_LBA_CONTROL_base= / _fix=.
+    <bin>  GATE <outdir>  ONE leg vs the FIX column; prints WDC_LBA_CONTROL=OK|FAIL then
+                          WDC_LBA_RESULT=p/n, then the sentinel.  Exit 0 iff p == n and
+                          control OK.
+The file ends with the sentinel WDCLBA_PROBE_DONE once.  Each session's raw transcript is
+kept under <outdir>/raw/<leg>_<session>.txt.  Exit status 0 only when every leg passed its
+own column.
 """
 import os
 import pty
@@ -83,6 +160,7 @@ import time
 BASE_BIN = sys.argv[1] if len(sys.argv) > 1 else "/tmp/gxlba/base/gxemul"
 FIX_ARG = sys.argv[2] if len(sys.argv) > 2 else "-"
 OUTDIR = sys.argv[3] if len(sys.argv) > 3 else "/tmp/gxlba/run"
+GATE = (FIX_ARG == "GATE")
 
 DISK_PREFIX = "iR:"                # i = IDE, R = pid-unique temporary overlay
 DISK = None                        # set in main(), lives under OUTDIR
@@ -103,19 +181,24 @@ WDCC_IDENTIFY = 0xec
 
 SEL_CHS = 0xa0                     # CHS, drive 0, head 0 (bits 7 and 5 the obsolete 1s)
 SEL_CHS_H1 = 0xa1                  # CHS, drive 0, head 1
+SEL_CHS_H4 = 0xa4                  # CHS, drive 0, head 4
+SEL_CHS_H15 = 0xaf                 # CHS, drive 0, head 15
 SEL_LBA = 0xe0                     # LBA, drive 0 (high LBA nibble 0)
+SEL_LBA_H1 = 0xe1                  # LBA, drive 0, LBA[27:24] = 1
+SEL_BIT6 = 0x40                    # bit 6 set, bits 7 and 5 CLEAR (LBA, no obsolete 1s)
 
-WR_W0, WR_W1 = 0x7777, 0x8888      # lbawr payload words 0 and 1
 RAM_MAGIC = 0x5a5a
 
 #  MIPS register numbers
 zero, v0, v1, a0, a1, a2, a3 = 0, 2, 3, 4, 5, 6, 7
 t0, t1, t2, t3 = 8, 9, 10, 11
-t4, t5, t6 = 12, 13, 14
+t4, t5, t6, t7 = 12, 13, 14, 15
 s0, s1, s2, s3 = 16, 17, 18, 19
+s4, s5, s6, s7 = 20, 21, 22, 23
 NAME = {zero: "zr", v0: "v0", v1: "v1", a0: "a0", a1: "a1", a2: "a2", a3: "a3",
         t0: "t0", t1: "t1", t2: "t2", t3: "t3", t4: "t4", t5: "t5", t6: "t6",
-        s0: "s0", s1: "s1", s2: "s2", s3: "s3"}
+        t7: "t7", s0: "s0", s1: "s1", s2: "s2", s3: "s3", s4: "s4", s5: "s5",
+        s6: "s6", s7: "s7"}
 
 
 def I(op, rs, rt, imm):
@@ -150,6 +233,10 @@ def lhu(rt, off, base):
     return I(0x25, base, rt, off)
 
 
+def lw(rt, off, base):
+    return I(0x23, base, rt, off)
+
+
 def beq(rs, rt, off):
     return I(0x04, rs, rt, off)
 
@@ -157,6 +244,7 @@ def beq(rs, rt, off):
 NOP = 0
 
 prog = []
+_slot = [8]                        # next free RAM result slot (word-aligned), reset in begin()
 
 
 def reset_prog():
@@ -190,6 +278,10 @@ def e_lhu(rt, off, base):
     emit(lhu(rt, off, base), "lhu %s,%d(%s)" % (NAME[rt], off, NAME[base]))
 
 
+def e_lw(rt, off, base):
+    emit(lw(rt, off, base), "lw %s,%d(%s)" % (NAME[rt], off, NAME[base]))
+
+
 def e_store(val, off, base):
     """Byte store of a small literal: li t3,val; sb t3,off(base)."""
     e_li(t3, val)
@@ -214,15 +306,26 @@ def e_cmd(select, seccnt, sector, cyl_lo, cyl_hi, command):
     e_store(command, R_STATUS, t0)
 
 
-def e_read_tag(rlo, rhi):
-    """Pop two 16-bit words from the data-port FIFO: word0 then word1 of the tag."""
-    e_lhu(rlo, R_DATA, t0)
-    e_lhu(rhi, R_DATA, t0)
-
-
-def e_discard(n):
-    for _ in range(n):
-        e_lhu(t3, R_DATA, t0)
+def e_read_tag(dst):
+    """Pop word0 then word1 of the tag, store them to adjacent RAM halfwords, and load
+    the pair back as one 32-bit word: dst = (word1 << 16) | word0.  A fresh RAM slot
+    per read keeps the stored pair inspectable and never aliased."""
+    slot = _slot[0]
+    _slot[0] += 4
+    e_lhu(t3, R_DATA, t0)
+    e_sh(t3, slot, t2)
+    e_lhu(t3, R_DATA, t0)
+    e_sh(t3, slot + 2, t2)
+    e_lw(dst, slot, t2)
+
+
+def e_write_sector(w0, w1):
+    """Push a full 512-byte sector: word0, word1, then 254 zero words.  The model drains
+    (writes the sector to write_offset) when 512 bytes have accumulated."""
+    e_push(w0)
+    e_push(w1)
+    for _ in range(254):
+        e_sh(zero, R_DATA, t0)
 
 
 def begin():
@@ -230,6 +333,7 @@ def begin():
     carries (same sh/lhu shapes, through plain RAM), so a device row reading 0x00 can
     never be blamed on a bad encoding."""
     reset_prog()
+    _slot[0] = 8                   # RAM result slots start past the 0x5a5a control word
     emit(lui(t0, WDC_HI), "lui t0,0xb800")
     emit(ori(t0, t0, WDC_LO), "ori t0,t0,0x01f0")
     emit(lui(t2, RAM_HI), "lui t2,0x8020")
@@ -249,11 +353,14 @@ def build_identify():
     begin()
     e_store(SEL_CHS, R_SDH, t0)            # select drive 0
     e_store(WDCC_IDENTIFY, R_STATUS, t0)   # ring := 256 words of IDENTIFY data
-    e_discard(3)                           # words 0..2
+    for _ in range(3):
+        e_lhu(t3, R_DATA, t0)              # words 0..2
     e_lhu(s0, R_DATA, t0)                  # word 3  = heads (H)
-    e_discard(2)                           # words 4..5
+    for _ in range(2):
+        e_lhu(t3, R_DATA, t0)              # words 4..5
     e_lhu(s1, R_DATA, t0)                  # word 6  = sectors per track (S)
-    e_discard(42)                          # words 7..48
+    for _ in range(42):
+        e_lhu(t3, R_DATA, t0)              # words 7..48
     e_lhu(s2, R_DATA, t0)                  # word 49 = capabilities (LBA bit)
     p, halt = end()
     return p, halt, {"ram": "v0", "H": "s0", "S": "s1", "w49": "s2"}
@@ -262,64 +369,113 @@ def build_identify():
 def build_chs():
     begin()
     e_cmd(SEL_CHS, 1, 1, 0, 0, WDCC_READ)      # cyl 0, sector 1 -> index 0
-    e_read_tag(a0, a1)
+    e_read_tag(a0)
     e_cmd(SEL_CHS, 1, 2, 0, 0, WDCC_READ)      # cyl 0, sector 2 -> index 1
-    e_read_tag(a2, a3)
+    e_read_tag(a1)
     e_cmd(SEL_CHS_H1, 1, 1, 0, 0, WDCC_READ)   # head 1, sector 1 -> index S
-    e_read_tag(s0, s1)
+    e_read_tag(a2)
+    e_cmd(SEL_CHS, 1, 1, 1, 0, WDCC_READ)      # cyl_lo 1, sector 1 -> index heads*S (N8)
+    e_read_tag(a3)
     p, halt = end()
-    return p, halt, {"ram": "v0", "s1_lo": "a0", "s1_hi": "a1",
-                     "s2_lo": "a2", "s2_hi": "a3", "h1_lo": "s0", "h1_hi": "s1"}
+    return p, halt, {"ram": "v0", "s1": "a0", "s2": "a1", "h1": "a2", "c1": "a3"}
 
 
 def build_sdh():
     begin()
     e_store(0xe5, R_SDH, t0)
-    e_lbu(s0, R_SDH, t0)                   # readback must stay byte-exact
+    e_lbu(s0, R_SDH, t0)                   # read-back must stay byte-exact
     e_store(0xb3, R_SDH, t0)
     e_lbu(s1, R_SDH, t0)
+    e_store(0x4c, R_SDH, t0)               # bits 7 and 5 CLEAR (N4)
+    e_lbu(s2, R_SDH, t0)
+    e_store(0xe5, R_SDH, t0)
+    e_store(0x00, R_SDH, t0)               # write 0xe5 then 0x00 -> 0x00
+    e_lbu(s3, R_SDH, t0)
     p, halt = end()
-    return p, halt, {"ram": "v0", "rb": "s0", "rb2": "s1"}
+    return p, halt, {"ram": "v0", "rb": "s0", "rb2": "s1", "rb3": "s2", "rb0": "s3"}
 
 
 def build_lba():
     begin()
+    e_li(a0, 0xdead)                           # poison the capture regs before the loads
+    e_li(a1, 0xdead)
+    e_li(a2, 0xdead)
+    e_li(a3, 0xdead)
     e_cmd(SEL_LBA, 1, 70, 0, 0, WDCC_READ)     # LBA 70
-    e_read_tag(a0, a1)
+    e_read_tag(a0)
     e_cmd(SEL_LBA, 1, 0, 1, 0, WDCC_READ)      # LBA 256 (sector 0, cyl_lo 1)
-    e_read_tag(a2, a3)
+    e_read_tag(a1)
+    e_cmd(SEL_BIT6, 1, 70, 0, 0, WDCC_READ)    # select 0x40 -- bit 6 only (N3)
+    e_read_tag(a2)
+    e_cmd(SEL_LBA, 1, 70, 0, 1, WDCC_READ)     # cyl_hi 1, cyl_lo 0 -- zeros both legs
+    e_read_tag(a3)
     p, halt = end()
-    return p, halt, {"ram": "v0", "l70_lo": "a0", "l70_hi": "a1",
-                     "l256_lo": "a2", "l256_hi": "a3"}
+    return p, halt, {"ram": "v0", "l70": "a0", "l256": "a1",
+                     "sel40": "a2", "cylhi": "a3"}
 
 
 def build_lba0():
     begin()
-    e_cmd(SEL_LBA, 1, 0, 0, 0, WDCC_READ)      # LBA 0; HEAD serves "CHS sector 0" -- recorded, not predicted
-    e_read_tag(a0, a1)
+    e_cmd(SEL_LBA, 1, 0, 0, 0, WDCC_READ)      # LBA 0; HEAD serves "CHS sector 0" (zeros)
+    e_read_tag(a0)
     p, halt = end()
-    return p, halt, {"ram": "v0", "l0_lo": "a0", "l0_hi": "a1"}
+    return p, halt, {"ram": "v0", "l0": "a0"}
+
+
+def build_lbah1():
+    begin()
+    e_li(a0, 0xbeef)                           # poison the capture regs before the loads
+    e_li(a1, 0xbeef)
+    e_cmd(SEL_LBA_H1, 1, 5, 0, 0, WDCC_READ)   # LBA 0x1000005 (head nibble 1) -- past file
+    e_read_tag(a0)
+    e_cmd(SEL_CHS, 1, 3, 0, 0, WDCC_READ)      # (0xa0, s3) -> index 2, tagged both legs
+    e_read_tag(a1)
+    p, halt = end()
+    return p, halt, {"ram": "v0", "h1": "a0", "h1ctl": "a1"}
 
 
 def build_lbawr():
     begin()
-    e_cmd(SEL_LBA, 1, 70, 0, 0, WDCC_WRITE)    # arm WRITE SECTORS, LBA 70
-    e_push(WR_W0)                              # word 0 = 0x7777
-    e_push(WR_W1)                              # word 1 = 0x8888
-    for _ in range(254):                       # 254 zero words -> 512 bytes -> drain
-        e_sh(zero, R_DATA, t0)
-    e_cmd(SEL_CHS, 1, 71, 0, 0, WDCC_READ)     # read CHS sector 71 (index 70)
-    e_read_tag(a0, a1)
-    e_cmd(SEL_CHS, 1, 70, 0, 0, WDCC_READ)     # read CHS sector 70 (index 69)
-    e_read_tag(a2, a3)
+    #  Five single-sector writes to pairwise-disjoint target sectors, then nine reads.
+    e_cmd(SEL_LBA, 1, 70, 0, 0, WDCC_WRITE)        # HEAD CHS index 69 / FIX LBA 70
+    e_write_sector(0x7777, 0x8888)
+    e_cmd(SEL_LBA_H1, 1, 5, 0, 0, WDCC_WRITE)      # HEAD CHS index 67 / FIX LBA past file
+    e_write_sector(0x9999, 0x6666)
+    e_cmd(SEL_LBA, 1, 0, 1, 0, WDCC_WRITE)         # HEAD CHS index 1007 / FIX LBA 256
+    e_write_sector(0x2222, 0x3333)
+    e_cmd(SEL_CHS, 1, 10, 0, 0, WDCC_WRITE)        # CHS index 9 both legs
+    e_write_sector(0x5555, 0x4444)
+    e_cmd(SEL_LBA, 1, 71, 0, 1, WDCC_WRITE)        # cyl_hi 1 -- past file both legs (refused)
+    e_write_sector(0x1111, 0xaaaa)
+
+    e_cmd(SEL_CHS_H1, 1, 8, 0, 0, WDCC_READ)       # index 70
+    e_read_tag(a0)
+    e_cmd(SEL_CHS_H1, 1, 7, 0, 0, WDCC_READ)       # index 69
+    e_read_tag(a1)
+    e_cmd(SEL_CHS_H1, 1, 5, 0, 0, WDCC_READ)       # index 67
+    e_read_tag(a2)
+    e_cmd(SEL_CHS, 1, 6, 0, 0, WDCC_READ)          # index 5
+    e_read_tag(a3)
+    e_cmd(SEL_CHS_H4, 1, 5, 0, 0, WDCC_READ)       # index 256
+    e_read_tag(s0)
+    e_cmd(SEL_CHS_H15, 1, 63, 0, 0, WDCC_READ)     # index 1007
+    e_read_tag(s1)
+    e_cmd(SEL_CHS, 1, 10, 0, 0, WDCC_READ)         # index 9
+    e_read_tag(s2)
+    e_cmd(SEL_CHS, 1, 11, 0, 0, WDCC_READ)         # index 10
+    e_read_tag(s3)
+    e_cmd(SEL_CHS_H1, 1, 9, 0, 0, WDCC_READ)       # index 71
+    e_read_tag(t4)
     p, halt = end()
-    return p, halt, {"ram": "v0", "wr_lo": "a0", "wr_hi": "a1",
-                     "wr2_lo": "a2", "wr2_hi": "a3"}
+    return p, halt, {"ram": "v0", "wr": "a0", "wr2": "a1", "wrh1": "a2",
+                     "wrh1s5": "a3", "wr256": "s0", "wr256b": "s1",
+                     "chswr": "s2", "chswr2": "s3", "wrcylhi": "t4"}
 
 
 SESSION_ORDER = [("identify", build_identify), ("chs", build_chs),
                  ("sdh", build_sdh), ("lba", build_lba),
-                 ("lba0", build_lba0), ("lbawr", build_lbawr)]
+                 ("lba0", build_lba0), ("lbah1", build_lbah1),
+                 ("lbawr", build_lbawr)]
 
 
 class Emu(object):
@@ -351,7 +507,10 @@ class Emu(object):
         data = (cmd + "\n").encode()
         view = memoryview(data)
         while len(view):
-            n = os.write(self.fd, view)
+            try:
+                n = os.write(self.fd, view)
+            except OSError:
+                break
             view = view[n:]
             if len(view):
                 self.drain(0.05)
@@ -450,7 +609,7 @@ def run_session(binary, prog_list, halt_addr, rawbin, regmap, tag, out):
     got = {}
     for logical, mips in regmap.items():
         v = reg(emu, mips)
-        got[logical] = None if v is None else (v & 0xffff)
+        got[logical] = None if v is None else (v & 0xffffffff)
     emu.close(os.path.join(RAWDIR, "%s.txt" % tag))
     return got, enc_ok, hit
 
@@ -469,10 +628,9 @@ def TAG(n):
     return (((~n) & 0xffff) << 16) | (n & 0xffff)
 
 
-def COMB(lo, hi):
-    if lo is None or hi is None:
-        return None
-    return (hi << 16) | lo
+def PAYLOAD(w0, w1):
+    """The value a written payload reads back as: (word1 << 16) | word0."""
+    return ((w1 & 0xffff) << 16) | (w0 & 0xffff)
 
 
 def show(v):
@@ -482,10 +640,7 @@ def show(v):
 def build_rows(sess, H, S):
     """Return rows as (label, kind, got, want_head, want_fix, mode).
 
-    mode: 'eq' got==want(column); 'nz' got is (H,S) and both nonzero;
-    'neg' a forced mismatch the parser must report as FAIL (passes iff got!=want)."""
-    hs = (TAG(H * S - 1)) if (H and S) else None   # lba 256 on the CHS (HEAD) decode
-    wr = COMB(WR_W0, WR_W1)                         # 0x88887777, the written payload
+    mode: 'eq' got == want(column); 'geo' got is (H,S) with H != 0 and S >= 10."""
     rows = []
     for name, _ in SESSION_ORDER:
         g = sess.get(name, {}).get("ram")
@@ -494,49 +649,66 @@ def build_rows(sess, H, S):
     idf = sess.get("identify", {})
     rows.append(("id w49", "control", idf.get("w49"), 0x0000, 0x0000, "eq"))
     rows.append(("id geo", "control", (idf.get("H"), idf.get("S")),
-                 "H,S!=0", "H,S!=0", "nz"))
+                 "H!=0,S>=10", "H!=0,S>=10", "geo"))
 
     chs = sess.get("chs", {})
-    rows.append(("chs s1", "control", COMB(chs.get("s1_lo"), chs.get("s1_hi")),
-                 TAG(0), TAG(0), "eq"))
-    rows.append(("chs s2", "control", COMB(chs.get("s2_lo"), chs.get("s2_hi")),
-                 TAG(1), TAG(1), "eq"))
-    rows.append(("chs h1", "control", COMB(chs.get("h1_lo"), chs.get("h1_hi")),
+    rows.append(("chs s1", "control", chs.get("s1"), TAG(0), TAG(0), "eq"))
+    rows.append(("chs s2", "control", chs.get("s2"), TAG(1), TAG(1), "eq"))
+    rows.append(("chs h1", "control", chs.get("h1"),
                  TAG(S) if S else None, TAG(S) if S else None, "eq"))
+    rows.append(("chs c1", "control", chs.get("c1"),
+                 TAG(H * S) if (H and S) else None,
+                 TAG(H * S) if (H and S) else None, "eq"))   # index heads*S (N8)
 
     sdh = sess.get("sdh", {})
     rows.append(("sdh rb", "control", sdh.get("rb"), 0xe5, 0xe5, "eq"))
     rows.append(("sdh rb2", "control", sdh.get("rb2"), 0xb3, 0xb3, "eq"))
+    rows.append(("sdh rb3", "control", sdh.get("rb3"), 0x4c, 0x4c, "eq"))   # N4
+    rows.append(("sdh rb0", "control", sdh.get("rb0"), 0x00, 0x00, "eq"))
 
     lba = sess.get("lba", {})
-    rows.append(("lba 70", "symptom", COMB(lba.get("l70_lo"), lba.get("l70_hi")),
-                 TAG(69), TAG(70), "eq"))
-    rows.append(("lba 256", "symptom", COMB(lba.get("l256_lo"), lba.get("l256_hi")),
-                 hs, TAG(256), "eq"))
-    l0 = sess.get("lba0", {})
-    rows.append(("lba 0", "symptom", COMB(l0.get("l0_lo"), l0.get("l0_hi")),
-                 TAG(0), TAG(0), "nehead"))     # HEAD: anything but tag 0; FIX: tag 0
-
-    lw = sess.get("lbawr", {})
-    rows.append(("lba wr", "symptom", COMB(lw.get("wr_lo"), lw.get("wr_hi")),
-                 TAG(70), wr, "eq"))
-    rows.append(("lba wr2", "symptom", COMB(lw.get("wr2_lo"), lw.get("wr2_hi")),
-                 wr, TAG(69), "eq"))
+    rows.append(("lba 70", "symptom", lba.get("l70"), TAG(69), TAG(70), "eq"))
+    rows.append(("lba 256", "symptom", lba.get("l256"),
+                 TAG(H * S - 1) if (H and S) else None, TAG(256), "eq"))
+    rows.append(("sel 40", "symptom", lba.get("sel40"), TAG(69), TAG(70), "eq"))  # N3
+    rows.append(("lba cylhi", "control", lba.get("cylhi"),
+                 0x00000000, 0x00000000, "eq"))              # zeros both legs (V10 variant)
 
-    rows.append(("neg appar", "control", 0x0001, 0x0000, 0x0000, "neg"))
+    l0 = sess.get("lba0", {})
+    rows.append(("lba 0", "symptom", l0.get("l0"), 0x00000000, TAG(0), "eq"))
+
+    lh = sess.get("lbah1", {})
+    rows.append(("lba h1", "symptom", lh.get("h1"), TAG(67), 0x00000000, "eq"))
+    rows.append(("lba h1 ctl", "control", lh.get("h1ctl"), TAG(2), TAG(2), "eq"))
+
+    lw_ = sess.get("lbawr", {})
+    p_wr = PAYLOAD(0x7777, 0x8888)
+    p_h1 = PAYLOAD(0x9999, 0x6666)
+    p_256 = PAYLOAD(0x2222, 0x3333)
+    p_chs = PAYLOAD(0x5555, 0x4444)
+    rows.append(("lba wr", "symptom", lw_.get("wr"), TAG(70), p_wr, "eq"))
+    rows.append(("lba wr2", "symptom", lw_.get("wr2"), p_wr, TAG(69), "eq"))
+    rows.append(("lba wr h1", "symptom", lw_.get("wrh1"), p_h1, TAG(67), "eq"))
+    rows.append(("lba wr h1s5", "control", lw_.get("wrh1s5"), TAG(5), TAG(5), "eq"))
+    rows.append(("lba wr256", "symptom", lw_.get("wr256"), TAG(256), p_256, "eq"))
+    rows.append(("lba wr256b", "symptom", lw_.get("wr256b"), p_256, TAG(1007), "eq"))
+    rows.append(("chs wr", "control", lw_.get("chswr"), p_chs, p_chs, "eq"))
+    rows.append(("chs wr2", "control", lw_.get("chswr2"), TAG(10), TAG(10), "eq"))
+    rows.append(("lba wr cylhi", "control", lw_.get("wrcylhi"), TAG(71), TAG(71), "eq"))
     return rows
 
 
 def row_ok(mode, got, want, column="HEAD"):
-    if mode == "nz":
-        H, S = got
-        return bool(H) and bool(S) and H != 0 and S != 0
-    if mode == "neg":
-        return got != want          # the parser MUST report this mismatch as a FAIL
-    if mode == "nehead":            # HEAD column: any served value but `want`; FIX column: exactly `want`
-        if got is None:
+    if mode == "geo":
+        #  IDENTIFY geometry: heads nonzero and S >= 10 (DETECTOR_REVISION R2).  The CHS
+        #  read-back triples are the valid ones for the S = 63 geometry diskimage pins for
+        #  a non-floppy image; a different geometry also reds the literal-index rows.
+        if not isinstance(got, tuple):
             return False
-        return got != want if column == "HEAD" else got == want
+        H, S = got
+        return H is not None and S is not None and H != 0 and S >= 10
+    if got is None or want is None:
+        return False
     return got == want
 
 
@@ -558,7 +730,7 @@ def run_leg(leg, binary, column, out):
     S = sess.get("identify", {}).get("S")
 
     out("")
-    out("  %-10s %-4s %-12s %-12s %-12s" % ("row", "", "got", "head", "fix"))
+    out("  %-12s %-12s %-12s %-12s" % ("row", "got", "head", "fix"))
     npass = nfail = 0
     ctrl_ok = True
     for label, kind, got, wh, wf, mode in build_rows(sess, H, S):
@@ -569,26 +741,31 @@ def run_leg(leg, binary, column, out):
         if kind == "control" and not ok:
             ctrl_ok = False
         if kind == "symptom":
-            out("  %-10s %-4s %-12s head %-10s fix %-10s [%s] %s"
-                % (label, "", show(got),
-                   ("!=" + show(wh)) if mode == "nehead" else show(wh), show(wf),
+            out("  %-12s %-12s head %-10s fix %-10s [%s] %s"
+                % (label, show(got), show(wh), show(wf),
                    column, "ok" if ok else "FAIL"))
         else:
-            out("  %-10s %-4s %-12s want %-12s %s"
-                % (label, "", show(got) if mode != "nz" else str(got),
-                   show(want) if mode != "nz" else str(wh),
+            out("  %-12s %-12s want %-12s %s"
+                % (label, show(got) if mode != "geo" else str(got),
+                   show(want) if mode != "geo" else str(wh),
                    "ok" if ok else "FAIL"))
+    ntot = npass + nfail
+    leg_ctrl = ctrl_ok and enc_all and hit_all
     out("")
-    out("  %d/%d passed" % (npass, npass + nfail))
-    out("  CONTROL=%s" % ("PASS" if (ctrl_ok and enc_all and hit_all) else "FAIL"))
-    leg_pass = (nfail == 0 and ctrl_ok and enc_all and hit_all)
+    out("  %d/%d passed" % (npass, ntot))
+    out("  CONTROL=%s" % ("PASS" if leg_ctrl else "FAIL"))
+    leg_pass = (nfail == 0 and leg_ctrl)
     out("  LEG %s VERDICT: %s" % (leg, "PASS" if leg_pass else "FAIL"))
     out("")
-    return leg_pass
+    return leg_pass, npass, ntot, leg_ctrl
 
 
 def main():
     global DISK, RAWDIR
+    #  Harness hygiene (NOT a scored row): the comparator must FAIL a mismatch and treat
+    #  a missing value as a failure.  (Replaces the old `neg appar` scored row.)
+    assert row_ok("eq", 1, 0, "FIX") is False and row_ok("eq", None, 0, "FIX") is False
+
     os.makedirs(OUTDIR, exist_ok=True)
     RAWDIR = os.path.join(OUTDIR, "raw")
     os.makedirs(RAWDIR, exist_ok=True)
@@ -610,16 +787,29 @@ def main():
     out("wdc       physical 0x180001f0 via bus_pci piix4_ide; KSEG1 0xffffffffb80001f0")
     out("disk      %s  (4096 sectors; tag n = (n, ~n))" % DISK)
     out("base bin  %s" % BASE_BIN)
-    out("fix bin   %s" % ("(none -- WITNESS run)" if FIX_ARG == "-" else FIX_ARG))
+    if GATE:
+        out("mode      GATE -- one leg vs the FIX column")
+    else:
+        out("fix bin   %s" % ("(none -- WITNESS run)" if FIX_ARG == "-" else FIX_ARG))
     out("")
 
-    legs = [("base", BASE_BIN, "HEAD")]
-    if FIX_ARG != "-":
-        legs.append(("fix", FIX_ARG, "FIX"))
+    if GATE:
+        legs = [("gate", BASE_BIN, "FIX")]
+    else:
+        legs = [("base", BASE_BIN, "HEAD")]
+        if FIX_ARG != "-":
+            legs.append(("fix", FIX_ARG, "FIX"))
 
     results = []
     for leg, binary, column in legs:
-        results.append(run_leg(leg, binary, column, out))
+        leg_pass, npass, ntot, leg_ctrl = run_leg(leg, binary, column, out)
+        results.append(leg_pass)
+        if GATE:
+            out("WDC_LBA_CONTROL=%s" % ("OK" if leg_ctrl else "FAIL"))
+            out("WDC_LBA_RESULT=%d/%d" % (npass, ntot))
+        else:
+            out("WDC_LBA_CONTROL_%s=%s" % (leg, "OK" if leg_ctrl else "FAIL"))
+            out("WDC_LBA_RESULT_%s=%d/%d" % (leg, npass, ntot))
 
     out("=" * 86)
     allok = all(results)
```

## 7. THE FROZEN INSTRUMENT'S FIXED LEG (`witness_20261024/RESULTS_fix.txt`)

```
======================================================================================
wdclbaaddr -- RUNG-3 WITNESS + DETECTOR on unmodified `evbmips -e malta`
======================================================================================
date      2026-10-24 19:02:13
machine   evbmips -e malta   LITTLE endian   (machine desc UNMODIFIED)
wdc       physical 0x180001f0 via bus_pci piix4_ide; KSEG1 0xffffffffb80001f0
disk      /tmp/gxt2/work/t4/witfix_190213/wdc-lba-scratch.img  (4096 sectors; tag n = (n, ~n))
base bin  /tmp/gxt2/base/gxemul
fix bin   /tmp/gxt2/fix/gxemul

--------------------------------------------------------------------------------------
LEG base -- base build, judged against the HEAD column
--------------------------------------------------------------------------------------
    [base_identify] /tmp/gxt2/base/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/witfix_190213/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/witfix_190213/raw/base_identify.bin
    encodings: 62/62 words, 62/62 mnemonics agree with the disassembler
    parked at 0xffffffff801000f0: yes   (1.52 s)
    [base_chs] /tmp/gxt2/base/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/witfix_190213/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/witfix_190213/raw/base_chs.bin
    encodings: 50/50 words, 50/50 mnemonics agree with the disassembler
    parked at 0xffffffff801000c0: yes   (1.52 s)
    [base_sdh] /tmp/gxt2/base/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/witfix_190213/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/witfix_190213/raw/base_sdh.bin
    encodings: 14/14 words, 14/14 mnemonics agree with the disassembler
    parked at 0xffffffff80100030: yes   (1.52 s)
    [base_lba] /tmp/gxt2/base/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/witfix_190213/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/witfix_190213/raw/base_lba.bin
    encodings: 36/36 words, 36/36 mnemonics agree with the disassembler
    parked at 0xffffffff80100088: yes   (1.52 s)
    [base_lba0] /tmp/gxt2/base/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/witfix_190213/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/witfix_190213/raw/base_lba0.bin
    encodings: 22/22 words, 22/22 mnemonics agree with the disassembler
    parked at 0xffffffff80100050: yes   (1.52 s)
    [base_lbawr] /tmp/gxt2/base/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/witfix_190213/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/witfix_190213/raw/base_lbawr.bin
    encodings: 306/306 words, 305/306 mnemonics agree with the disassembler
    parked at 0xffffffff801004c0: yes   (1.52 s)

  row             got          head         fix         
  ram:identify      0x00005a5a   want 0x00005a5a   ok
  ram:chs         0x00005a5a   want 0x00005a5a   ok
  ram:sdh         0x00005a5a   want 0x00005a5a   ok
  ram:lba         0x00005a5a   want 0x00005a5a   ok
  ram:lba0        0x00005a5a   want 0x00005a5a   ok
  ram:lbawr       0x00005a5a   want 0x00005a5a   ok
  id w49          0x00000000   want 0x00000000   ok
  id geo          (16, 63)     want H,S!=0       ok
  chs s1          0xffff0000   want 0xffff0000   ok
  chs s2          0xfffe0001   want 0xfffe0001   ok
  chs h1          0xffc0003f   want 0xffc0003f   ok
  sdh rb          0x000000e5   want 0x000000e5   ok
  sdh rb2         0x000000b3   want 0x000000b3   ok
  lba 70          0xffba0045   head 0xffba0045 fix 0xffb90046 [HEAD] ok
  lba 256         0xfc1003ef   head 0xfc1003ef fix 0xfeff0100 [HEAD] ok
  lba 0           0x00000000   head !=0xffff0000 fix 0xffff0000 [HEAD] ok
  lba wr          0xffb90046   head 0xffb90046 fix 0x88887777 [HEAD] ok
  lba wr2         0x88887777   head 0x88887777 fix 0xffba0045 [HEAD] ok
  neg appar       0x00000001   want 0x00000000   ok

  19/19 passed
  CONTROL=PASS
  LEG base VERDICT: PASS

--------------------------------------------------------------------------------------
LEG fix -- fix build, judged against the FIX column
--------------------------------------------------------------------------------------
    [fix_identify] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/witfix_190213/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/witfix_190213/raw/fix_identify.bin
    encodings: 62/62 words, 62/62 mnemonics agree with the disassembler
    parked at 0xffffffff801000f0: yes   (1.51 s)
    [fix_chs] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/witfix_190213/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/witfix_190213/raw/fix_chs.bin
    encodings: 50/50 words, 50/50 mnemonics agree with the disassembler
    parked at 0xffffffff801000c0: yes   (1.52 s)
    [fix_sdh] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/witfix_190213/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/witfix_190213/raw/fix_sdh.bin
    encodings: 14/14 words, 14/14 mnemonics agree with the disassembler
    parked at 0xffffffff80100030: yes   (1.52 s)
    [fix_lba] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/witfix_190213/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/witfix_190213/raw/fix_lba.bin
    encodings: 36/36 words, 36/36 mnemonics agree with the disassembler
    parked at 0xffffffff80100088: yes   (1.52 s)
    [fix_lba0] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/witfix_190213/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/witfix_190213/raw/fix_lba0.bin
    encodings: 22/22 words, 22/22 mnemonics agree with the disassembler
    parked at 0xffffffff80100050: yes   (1.52 s)
    [fix_lbawr] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/witfix_190213/wdc-lba-scratch.img 0xffffffff80100000:/tmp/gxt2/work/t4/witfix_190213/raw/fix_lbawr.bin
    encodings: 306/306 words, 305/306 mnemonics agree with the disassembler
    parked at 0xffffffff801004c0: yes   (1.52 s)

  row             got          head         fix         
  ram:identify      0x00005a5a   want 0x00005a5a   ok
  ram:chs         0x00005a5a   want 0x00005a5a   ok
  ram:sdh         0x00005a5a   want 0x00005a5a   ok
  ram:lba         0x00005a5a   want 0x00005a5a   ok
  ram:lba0        0x00005a5a   want 0x00005a5a   ok
  ram:lbawr       0x00005a5a   want 0x00005a5a   ok
  id w49          0x00000000   want 0x00000000   ok
  id geo          (16, 63)     want H,S!=0       ok
  chs s1          0xffff0000   want 0xffff0000   ok
  chs s2          0xfffe0001   want 0xfffe0001   ok
  chs h1          0xffc0003f   want 0xffc0003f   ok
  sdh rb          0x000000e5   want 0x000000e5   ok
  sdh rb2         0x000000b3   want 0x000000b3   ok
  lba 70          0xffb90046   head 0xffba0045 fix 0xffb90046 [FIX] ok
  lba 256         0xfeff0100   head 0xfc1003ef fix 0xfeff0100 [FIX] ok
  lba 0           0xffff0000   head !=0xffff0000 fix 0xffff0000 [FIX] ok
  lba wr          0x88887777   head 0xffb90046 fix 0x88887777 [FIX] ok
  lba wr2         0xffba0045   head 0x88887777 fix 0xffba0045 [FIX] ok
  neg appar       0x00000001   want 0x00000000   ok

  19/19 passed
  CONTROL=PASS
  LEG fix VERDICT: PASS

======================================================================================
VERDICT   every leg passed its own column
WDCLBA_PROBE_DONE
```

## 8. THE FOUR HUNKS THE LANDING STAGES INTO HEAD-BASED COPIES

--- HUNKS for gate_sh_rounding.sh ---
--- a/regress/gate_sh_rounding.sh
+++ b/regress/gate_sh_rounding.sh
@@ -1524,6 +1524,58 @@
     fi
 fi
 
+# ---------------------------------------------------------------------------
+# #572 (wdclbaaddr): the wdc SDH taskfile decoded the ATA LBA flag from BIT 5
+# (0x20) instead of BIT 6 (0x40 = WDSD_LBA), and the LBA28 offset formula was
+# `#if 0'd out at both wdc__read and wdc__write, so an LBA-mode request was served
+# from the CHS reading of the same taskfile bytes.  The fix decodes lba from bit 6,
+# keeps the SDH read-back byte-exact through the renamed reserved field sdh_resv,
+# and enables the 64-bit LBA28 arm at BOTH sites.  WIRED IN THE SAME COMMIT AS THE
+# PROBE, so it cannot ship unwired and let its pin drift red between commits.
+#
+# rung 3 on UNMODIFIED `evbmips -e malta`: real MIPS PIO through the committed
+# piix4_ide path, device-signature tags (word0,word1) = (n, ~n) that no RAM cell
+# holds.  Pre-fix witness: regress/artifacts/wdclbaaddr/witness_20261024/ (base leg
+# 19/19 vs HEAD, the five lba* rows RED vs the FIX column).  Kill table and the
+# two-leg / GATE / dead-run measurements: regress/artifacts/wdclbaaddr/detector_20261024/.
+LBALOG=$LOGDIR/gate_wdc_lba.log
+LBADIR=$LOGDIR/wdclba
+python3 -u wdc_lba_probe.py "$PMAX" GATE "$LBADIR" > "$LBALOG" 2>&1 || true
+
+if ! grep -q "WDC_LBA_RESULT=" "$LBALOG"; then
+    note "wdc_lba probe produced no result line; last lines follow"
+    tail -5 "$LBALOG" | sed 's/^/       /'
+    check "wdc_lba probe completed" "no" "yes"
+else
+    grep -E ' (ok|FAIL)$' "$LBALOG" | sed 's/^/       /'
+    #  PARSE BEFORE SCORE: a result line that EXISTS but is MALFORMED still satisfies
+    #  the outer grep; lbares is then empty and `check "" ""` passes on nothing (the
+    #  wdcflood / wdc_altdigin lesson).
+    lbares=$(grep -o "WDC_LBA_RESULT=[0-9]*/[0-9]*" "$LBALOG" | tail -1 | cut -d= -f2)
+    if [ -z "$lbares" ]; then
+        note "wdc_lba result line present but unparseable; last lines follow"
+        tail -3 "$LBALOG" | sed 's/^/       /'
+        check "wdc_lba result parses" "no" "yes"
+    else
+        check "wdc_lba result parses" "yes" "yes"
+        lbactl=$(grep -o "WDC_LBA_CONTROL=[A-Z]*" "$LBALOG" | tail -1 | cut -d= -f2)
+        #  CONTROL=OK requires every IDENTITY row (the rows whose HEAD and FIX wants agree:
+        #  ram liveness, IDENTIFY, the CHS reads, the SDH read-backs, the untouched-sector
+        #  and refused-write controls) AND every session's encodings and halt breakpoint.
+        check "wdc_lba control: identity rows, encodings, breakpoints" "${lbactl:-missing}" "OK"
+        #  DENOMINATOR PINNED TO A LITERAL (the wdc_altdigin idiom).  The literal is the
+        #  revised probe's scored-row count: 7 ram + 2 identify + 4 chs + 4 sdh + 4 lba
+        #  + 1 lba0 + 2 lbah1 + 9 lbawr = 33.  A pin that follows the probe's own
+        #  denominator cannot tell a probe that LOST rows from one that never had them,
+        #  so the literal moves BY HAND and says why.
+        check "wdc_lba rows run"     "${lbares#*/}" 33
+        check "wdc_lba rows correct" "${lbares%/*}" "${lbares#*/}"
+    fi
+    #  The probe must reach its own completion sentinel, not merely emit a result line.
+    check "wdc_lba probe reached its sentinel" \
+          "$(grep -cx 'WDCLBA_PROBE_DONE' "$LBALOG")" "1"
+fi
+
 #  *** A SOURCE GREP, BECAUSE A STEP-BASED PROBE CANNOT SEE CHANNEL SEMANTICS. ***
 #  `fatal(` -> `debug(` at any of the six sites scores a CLEAN SWEEP against every row
 #  above: they all single-step, and debug() always prints under stepping (its early-out


--- HUNKS for diff_wdc_identify.c ---
--- a/regress/diff_wdc_identify.c
+++ b/regress/diff_wdc_identify.c
@@ -5604,19 +5604,22 @@
 }
 
 /*
- *  #407: WORD 49 MUST STAY ZERO, and this row is worth one character of mutant.
- *  Setting the LOW byte of word 49 (`identify_struct[2 * 49 + 1]`, dev_wdc.c:236 at
- *  085766a) to 2 gives word 0x0002 -- a reserved bit, NOT LBA (LBA is 0x0200, the
- *  high byte); that mutant passed all ten original rows, and this row pins both
- *  bytes so either mutant reds.  (This comment said "advertises LBA" until the
- *  2026-09-05 retrospective review.)
- *  It is not cosmetic: the LBA offset arms in wdc__read/wdc__write are `#if 0`
- *  (:315-321, :361-367), the live offsets at :311-313/:358-360 are pure CHS, and
- *  d->lba is parsed at :970 and never reaches an offset computation. A guest
- *  told LBA is supported would have its LBA addresses read as C/H/S.
- *
- *  This asserts the CURRENT, DELIBERATE state. If LBA is ever implemented, this
- *  row must be re-authored in the SAME change -- that is the point of pinning it.
+ *  #407 / #572: WORD 49 STAYS ZERO -- a POLICY row, worth one character of mutant.
+ *  Setting the LOW byte of word 49 (`identify_struct[2 * 49 + 1]`) to 2 gives word
+ *  0x0002 -- a reserved bit, NOT LBA (LBA is 0x0200, the high byte); that mutant
+ *  passed all ten original rows, and this row pins both bytes so either mutant reds.
+ *  (This comment said "advertises LBA" until the 2026-09-05 retrospective review.)
+ *
+ *  #572 IMPLEMENTS LBA28 (the LBA bit of the select byte now reaches the LBA28
+ *  offset arms in wdc__read/wdc__write) but DELIBERATELY DOES NOT ADVERTISE LBA
+ *  here: advertising word 49 is a separate, measured decision (the wdclbaadvertise
+ *  row), and words 60-61 already carry the capacity.  So this row no longer pins
+ *  "LBA unimplemented"; it pins the ADVERTISEMENT POLICY -- implemented, not
+ *  advertised.  A guest that does not read word 49 drives LBA commands today and
+ *  they are honoured; one that honours word 49 keeps using C/H/S, as before.
+ *
+ *  If the advertisement is ever turned on, this row must be re-authored in the SAME
+ *  change -- that is the point of pinning it.
  */
 static void row_no_lba_claim(void)
 {
@@ -5627,7 +5630,8 @@
 	if (d.identify_struct[2 * 49 + 0] != 0 ||
 	    d.identify_struct[2 * 49 + 1] != 0) {
 		printf("  FAIL word 49 claims a capability: %02x %02x"
-		    " (0x200 = LBA, 0x100 = DMA -- neither is implemented)\n",
+		    " (0x200 = LBA -- implemented by #572, deliberately not"
+		    " advertised; 0x100 = DMA -- not implemented)\n",
 		    d.identify_struct[2 * 49 + 0], d.identify_struct[2 * 49 + 1]);
 		failures ++;
 	} else {


--- HUNKS for gate_offline.sh ---
--- a/regress/gate_offline.sh
+++ b/regress/gate_offline.sh
@@ -1887,7 +1887,7 @@
     #  mutant -- verified by asserting the row NAME in the kill, not just that
     #  something failed.
     #    slave      <- 10 chars: drop `d->drive + ` at dev_wdc.c:179
-    #    word 49    <- 1 char:   advertise LBA that is #if 0'd out
+    #    word 49    <- 1 char:   advertise LBA that #572 implements but does not advertise
     #    65535 loop <- 11-bit cylinder truncation, first contradiction at c=2048,
     #                  which the old c<=2000 bound missed by FORTY-EIGHT
     check     "wdc IDENTIFY: the slave-drive row is present" \


--- HUNKS for check_probe_wiring.py ---
--- a/tools/pipeline/check_probe_wiring.py
+++ b/tools/pipeline/check_probe_wiring.py
@@ -3221,6 +3221,31 @@
                         "(witness_20261023/WITNESS_headbin.out), 24/24 on the fixed build (table1_20261023/fixed_witness24.out)"),
     "ppc_dsform_probe.py": (CLASS_DETECTOR, "#571 ppcdsformxo: the 64-bit DS-form loads and stores (opcodes 58 and 62: ld, ldu, lwa, std, stdu, the reserved XO encodings, and ldu/stdu with RA = 0) -- 39 rows on unmodified -E bareppc -M 64; gated in gate_ppc.sh (gate 13) under the stem ppc_dsform, pinned at 39; kill table artifacts/ppcdsformxo/table1_20261024/ (SCORES.txt)"),
     "artifacts/ppcdsformxo/witness_20261024/ppc_dsform_probe.py": (CLASS_RESEARCH, "#571 ppcdsformxo: the frozen rung-3 pre-fix instrument of the LOADS (8 rows, md5 5e96b69d), preserved as evidence -- 5/8 on HEAD (witness_20261024/WITNESS_headbin.out), 8/8 post-fix (table1_20261024/fixed_witness8.out): it asserts the REPAIRED property and is green once the defect is gone, so by the WITNESS/DETECTOR line above it is RESEARCH, not WITNESS; the stores' pre-fix artifact is table1_20261024/prefix_BASE.out"),
+    # -- #572 wdclbaaddr -------------------------------------------------------------------
+    #  The wdc SDH LBA-flag decode (bit 5 -> bit 6) and the 64-bit LBA28 offset arms.  The
+    #  SHIPPING detector is CLASS_DETECTOR and gated in gate_sh_rounding.sh (gate 10) in the
+    #  same commit; its wiring is DERIVED below, not asserted here.  The frozen witness copy
+    #  is CLASS_WITNESS: its as-run base leg asserts the PRE-FIX symptom (HEAD column) and
+    #  would go RED on a repaired base, so it is ungated by design.  The detector_20261024/
+    #  frozen instrument and the mutant applicator are CLASS_TOOL (kill-table evidence).
+    "wdc_lba_probe.py":
+        (CLASS_DETECTOR, "#572 wdclbaaddr: wdc LBA-mode address decode -- SDH decodes the LBA "
+                         "flag from bit 6 (was bit 5) and the 64-bit LBA28 arm is enabled at both "
+                         "read and write sites.  33 rows on unmodified evbmips -e malta; wired in "
+                         "gate_sh_rounding.sh (gate 10) in the same commit, pinned at 33; kill tables "
+                         "artifacts/wdclbaaddr/detector_20261024/ (SCORES.txt 18/18 killed, "
+                         "SCORES2.txt 9/9 killed; null medium dead_run.out 0/33 CONTROL=FAIL)."),
+    "artifacts/wdclbaaddr/witness_20261024/wdc_lba_probe.frozen.py":
+        (CLASS_WITNESS, "#572 wdclbaaddr: the as-run rung-3 pre-fix WITNESS (md5 8f3632ff) -- base "
+                        "leg 19/19 vs the HEAD column (witness_20261024/RESULTS_base.txt); asserts "
+                        "the pre-fix symptom, RED on a repaired base, ungated by design."),
+    "artifacts/wdclbaaddr/detector_20261024/wdc_lba_probe.frozen.py":
+        (CLASS_TOOL, "#572 wdclbaaddr: the frozen detector instrument both kill tables ran against (md5 "
+                     "fc878c42); the shipped probe differs only in its module docstring (rev_equivalence.txt)"),
+    "artifacts/wdclbaaddr/detector_20261024/mutants572.py":
+        (CLASS_TOOL, "#572 wdclbaaddr: kill-table mutant applicator -- table 1 (18 mutants, V1..V20) and table 2 "
+                     "(V5r, V6r, V8w, V11w, V9r8, V10r, V10w and the T_m1/T_p1 anchor translations); table 1's "
+                     "applicator is kept byte-for-byte as mutants572_table1.py.txt, outside this checker's domain"),
 }
 
 #  DATED, NAMED DEBT -- not a count and not a silent allowlist.  gate_offline.sh MEASURED that



## 9. FILE-READING SEATS MAY OPEN: `src/devices/dev_wdc.c` (working tree = the diff applied), `regress/wdc_lba_probe.py`, everything under `regress/artifacts/wdclbaaddr/`, `regress/gate_sh_rounding.sh` (gate 10's wdc_altdigin block :1480-1535), `tools/pipeline/check_probe_wiring.py`, `regress/diff_wdc_identify.c` at HEAD (`git show HEAD:...`; the WT carries other hunks).

## 10. ROSTER: Astra, Grok, Argon (agy), GLM x2, DeepSeek x2; Fable HELD; kimi/minimax/Opus-seat NOT FIRED by roster.

## 11. QUESTIONS (VERDICT LINE FIRST: `READY TO LAND | LAND WITH CHANGES | DO NOT LAND`, then Q1-Q4; mark each claim READ / DERIVED / NOT CHECKABLE)

Q1  THE DIFF (section 2).  Is the product edit exactly the adjudicated repair and nothing else -- the five `#572` sites, the field
    rename complete (no `sectorsize` reader left), the readback byte-exact for all 256 select bytes, both arms widened before the
    multiply, the write arm above the `write_*` assignments, the printfs gone, every must-not-change item untouched (the CHS
    formula and casts, the ABRT arms, `#481`'s arm, `wdc_altstatus`, ATAPI, the `#484` ring cap, the drain, every IDENTIFY word)?
    Is the `est/` twin byte-identical (the builder's report says; NOT CHECKABLE for packet-fed seats)?  Any defect the edit
    introduces?
Q2  THE DETECTOR (sections 3-6).  Does the measured table discharge the floor as adjudicated -- every enumerated variant red at
    the row the pre-table record names, no escape unexplained, the dead run measured, the GATE mode's denominator pinned by
    equality, the contract's CATCHES / MEASURED-NOT-PROMISED / BLIND lists honest against the rows that exist?  Which row or
    variant is vacuous or mis-predicted?  One ask-again: name ONE further single-edit variant of the shipped diff that no row sees.
Q3  RECORDS (sections 7-8).  Are the four HUNKS correct and minimal (the gate-10 block's pins, the gate-2 row's re-authoring with its
    assertion / name / "ok" string unchanged, the comment, the MANIFEST classes)?  What must the CHANGELOG block claim and not claim?
Q4  Anything else in the diff's neighbourhood (standing licence): a false comment, a stale record, a sibling the edit makes
    reachable.  Say "none" if none.
