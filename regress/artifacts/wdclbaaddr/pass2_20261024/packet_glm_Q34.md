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

## 2. THE PRODUCT DIFF (5 hunks)

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

## 3. THE BUILDER'S REPORT

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


## 4. THE PRE-TABLE RECORD

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

## 5. THE MEASURED SCORES

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
    [gate_lba] /tmp/gxt2/fix/gxemul -V -E evbmips -e malta -d iR:/tmp/gxt2/work/t4/final_20290
[... scores cut to fit the packet cap; the FULL form carries them all ...]


## 6. THE DETECTOR: you cannot read files; the report above names the rows, the modes, the contract and the counts; the detector diff is NOT inlined -- mark detector-internal claims NOT CHECKABLE and say what fact would settle each.

## 7. THE FROZEN INSTRUMENT'S FIXED LEG

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

## 8. THE HUNKS (gate 10 and gate 2 only)

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



## 9. (file list omitted for packet-fed seats)

## 10. ROSTER: as above.

**THIS FIRING ANSWERS Q3 AND Q4 ONLY.**  Q1 and Q2 went to a separate firing of this same packet; treat the settled design as given here and do not answer them.  Keep hidden reasoning short and put the VERDICT line and the answers in the response itself.

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
