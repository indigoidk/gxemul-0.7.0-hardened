FABLE_SEAT_ALIVE_20261009_RGD
# CHECKPOINT -- 2026-10-07 11:3x RUNNING (087a90 sections rewritten; the peer's sections below are untouched)

MODEL: claude-fable-5-1 (Fable 5.1) -- flagship REGRESS seat, queue batch 8n, 2026-10-09.
HEAD measured: a05660af.  READ-ONLY on every project tree: git-archive tarballs of the shas built in
/tmp/gxfable_rgd (WSL Gentoo); every log and note under
C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-cc-GXEMUL\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\fable_rgd\
(below: SCRATCH).  No git command that writes the index, no gate run, no tracked file edited.  The working
tree carries the peer's uncommitted edits (incl. regress/gate_sh_rounding.sh), so every gate/probe/device
reading below is from `git show <sha>:`, never from the tree.  Regress is flagship-only: no other seat fired.

VERDICT LINES
wdcaltctrlbit: REGRESS CLEAN -- all three OVERTAKEN conditions hold and condition (1) is re-measured at today's HEAD (base 0/128 red, Md_bitswap 11/128, Mb_revert 12/128; the five named rows red 5/96 on the true parent device, 0/96 on the commit).  One dated-count note, no wrong record.
diskimagesign: REGRESS WITH FINDINGS (3) -- the detector discriminates both ways (parent 2 -Wsign-compare at :1382, commit/HEAD 0; the arm swap is warning-free and ABORTS the gated diff_diskimage_io.c with 10 rows red and no PASS token); two wrong records in OUTSTANDING_BUGS.md (a WITHDRAWN row still standing as HIGH; a closed row still "IN WORK" in the open list) and a witness field that names no detector.
sgirergbroundtrip: REGRESS CLEAN -- committed 10-row probe, one instrument: parent 4/10 (six RGB rows red, every value 0xbbccdd00), commit 10/10; fix, probe and gate pins intact at HEAD.  One records suggestion, no wrong record.
landiskaux: REGRESS WITH FINDINGS (1) -- committed 6-row probe, one instrument: true parent 1/6 (vector 1,0,0,0,0,0, values identical to the preserved prefix_HEAD.out), commit 6/6; fix, probe and gate intact at HEAD; the closed row's `hold` and `hold_question` still describe an unshipped round.
pcc2c040mienannounce: REGRESS WITH FINDINGS (2) -- on the bb8efbf build: base 18/18, A 17/18, F 17/18 (`c040 once mien`, count 7), pass-1 M_announce_notmien 16/18 (both new rows red); committed probe token-identical to Opus's measured copy and to HEAD; gate pins 18 by name.  Witness term `probe:` on a round that changed no src/ file; a stale (LOW) bug-file heading.

======================================================================================================
1. wdcaltctrlbit  (closed, 867c697 -- OVERTAKEN by #481)
======================================================================================================
READ
* Ledger row (tools/pipeline/ledger.json:27815-27950, HEAD): state closed, commits 867c697, closure by opus5
  badge A "OVERTAKEN by #481 ... No fix and no row -- the carrier is #481's own detector"; witness (:27948)
  `detector:regress/diff_wdc_identify.c -- carrying rows NAMED BY LABEL: ...` five labels, the two
  discriminating ones named (0x06 false negative, 0x08 false positive, 0x0c settles nothing), controls
  `PREFIX_committed_device.out (5 ...)` and `bin_Md_bitswap.out (8 red ...)`.
* The predicate: aa3faff1 (parent) `src/devices/dev_wdc.c:497 if (idata & WDCTL_4BIT)`; 867c697 `:567
  if (idata & WDCTL_RST) {`; HEAD a05660af `:832 if (idata & WDCTL_RST) {` (0 diff lines on dev_wdc.c
  since e16a8b7; the arm is unchanged).
* All five labels exist in HEAD's regress/diff_wdc_identify.c (:4000, :4050, :4112, :4153, :4234), plus the
  sixth `the libata SRST form signs too` (:4350) and the four #479/#480 rows (:2582-2823).  The file grew
  96 -> 128 rows over 10 commits (#482..#485, #551, #553, #556, two records commits); none removed a row.
* Gate wiring at HEAD (regress/gate_offline.sh): compile-and-run block :1447-1463 (row failures 0,
  rows >= 42 via check_min, WDC_IDENTIFY_PASS token) plus `selfmutant_one diff_wdc_identify.c
  src/devices/dev_wdc.c wdc_identify ...` :1024; gate_offline is GATES[1] in regress/run.sh:10.
* Condition (3): regress/artifacts/wdcaltctrl/killtable_20260827/ holds PREFIX_committed_device.out
  (96 rows, 5 failures -- the five labels), bin_Md_bitswap.out (96 rows, 8 failures = the four #479/#480
  rows + 0x06/0x08/nIEN/signs; the 0x0c row GREEN, as the witness says), base.out (96/0), TABLE.txt.

RAN  (SCRATCH\offline_rgd.sh -> offline_rgd.log; full differential outputs SCRATCH\offline_out\wdc_*.out)
Each tree git-archived, `./configure`d (config.h is needed), the differential compiled with the gate's own
line (`gcc -O2 -std=c99 -I src/include -I src/include/thirdparty -ffunction-sections -fdata-sections
-Wl,--gc-sections`), gcc 15.2.1.
    PARENT aa3faff1, its OWN differential vs its own device     87 rows, 0 failures, PASS   (the rows did not exist yet)
    PREFIX  = 867c697 differential vs aa3faff1 device           96 rows, 5 failures, FAIL   exactly the five labels,
                                                                diagnostics byte-identical to PREFIX_committed_device.out
                                                                (cur_command 0x0 / 0xec -> 0x100 / 0x0a->0x100 0x02->0xec /
                                                                 wip 0x30 flag 1 occ 40 / 0x0000 want 0xeb14)
    COMMIT  867c697 differential vs 867c697 device              96 rows, 0 failures, PASS
    HEAD    a05660af differential vs HEAD device               128 rows, 0 failures, PASS
    HEAD + Md_bitswap (WDCTL_RST -> WDCTL_4BIT, repair kept)   128 rows, 11 failures: the 8 recorded + `a 0x88 control
                                                                write is not a reset`, `an SRST purges an orphan ring`,
                                                                `reset ACTS IFF bit 2 is set`
    HEAD + Mb_revert (verbatim pre-#481 arm)                   128 rows, 12 failures (the five + seven later rows)
(The `@@SELFCHECK@@` FAIL lines in the HEAD outputs are #551's deliberate self-check rows; the summary line
counts them at 0, so the score is the summary's.)
So: condition (1) holds today, more strongly than recorded; (2) the labels are present and the two
discriminating ones red under the bitswap at HEAD; (3) the control is durable and its figures match.

NOTE (not a wrong record): the witness says "Controls at HEAD: ... bin_Md_bitswap.out (8 red ...)" while
citing 2026-08-27 artifacts -- "HEAD" there is 867c697's HEAD, and today's HEAD gives 11.  The artifact is
correctly described; the field would be clearer as "measured at 867c697 (2026-08-27); re-measured at
a05660af 2026-10-09: 11/128".

======================================================================================================
2. diskimagesign  (closed, 18893de -- #491)
======================================================================================================
READ
* Ledger row (ledger.json:28538-28646): closed, commits 18893de, witness (:28541)
  `detector:regress/artifacts/diskimagesign/cascade_20260829`; kimi's arm-swap dissent recorded with outcome
  REFUTED (opus5 2026-09-17 measured SIGABRT + 7 rows red; fable5 2026-09-18 ruled the dissent "dies rather
  than files").
* The clamp: fb0cc783 (parent) `src/disk/diskimage.c:1382 lentoread = len > remain? remain : len;`;
  18893de `:1388 lentoread = len > (size_t) remain? remain : (off_t) len;`, unchanged at HEAD (0 diff lines).
  Its context (:1380-1381) is `inblock = curofs & (OVERLAY_BLOCK_SIZE - 1); remain = OVERLAY_BLOCK_SIZE -
  inblock;`, so the row's "remain is in [1, 512]" is right.
* Detectors at HEAD: regress/gate_build.sh:124 `check "$lab: warnings" "$warn" "0"` (both pmax and arc);
  regress/gate_offline.sh:2036-2057 compiles and runs diff_diskimage_io.c (row failures 0, faults 0,
  DISKIMAGE_IO_PASS token) and :1055 `selfmutant_one diff_diskimage_io.c src/disk/diskimage.c diskimage_io
  "refused read leaves NO caller bytes"`.  gate_build.sh changed by one comment hunk since 18893de (#556);
  diff_diskimage_io.c by comment hunks (#556) and one row relabel [PROOF] -> [CONTROL] (#560) -- no oracle.
* The preserved cascade (regress/artifacts/diskimagesign/cascade_20260829/): gate_build.log `pmax: warnings 0
  / arc: warnings 0 / PASS (18 checks)`, gate_mips.log `mips-rigs: PASS (6 checks)` -- the cascade claim.

RAN  (SCRATCH\offline_rgd.log; outputs SCRATCH\offline_out\io_*.out, di_*)
Warning compile with the build's own CWARNINGS as generated by `./configure` in the 18893de tree
(Makefile:8 `-Wshadow -Wcast-align -Wstrict-aliasing -Wall -Wextra -Wno-unused-parameter -Wno-cast-align`),
`-std=gnu99 -O3 -DNDEBUG`:
    PARENT fb0cc783        rc=0  2 sign-compare warnings, both at diskimage.c:1382 (:33 size_t vs off_t; :43 ?: signedness)
    COMMIT 18893de         rc=0  0
    HEAD   a05660af        rc=0  0
    HEAD + arm swap        rc=0  0     <- the dissent's premise ("zero warnings, casts intact") is TRUE
Gated differential, the gate's compile line (-O2 -std=gnu99 ...):
    COMMIT 18893de  diff_diskimage_io.c vs own diskimage.c     98 rows, 0 failures, 0 faults, DISKIMAGE_IO_PASS
    HEAD            same                                        98 rows, 0 failures, 0 faults, DISKIMAGE_IO_PASS
    HEAD + arm swap (`? (off_t) len : remain`)                  ABORTED rc=134 "*** stack smashing detected ***",
                                                                10 rows FAIL before the abort (overlay unaligned, overlay
                                                                short-unaligned, short read x2, [ANCHOR] x2, ROW P x2,
                                                                ROW U x2), NO summary line, NO PASS token
So gate_offline's "verdict token" (want 1) and "row failures" parse both red on the swap: the dissent's
conclusion is false, as the ledger records.  (Opus 2026-09-17 recorded "7 rows RED"; I measure 10 at today's
98-row differential -- same verdict, the count depends on where the stack guard fires.)  The row note's
object sizes 44072/44112 b are not reproduced (44104/44104 here, a different toolchain build) -- immaterial.

FINDINGS
F2.1  WRONG RECORD (L4) -- OUTSTANDING_BUGS.md:20150 `### \`diskimageternaryoob\` (HIGH, coverage/(d)-floor) --
      filed 2026-09-17, kimi seat via the late-review panel`, :20152-20153 `**\`#491\`'s CLAMP CAN BE NULLED BY
      SWAPPING TWO TERNARY ARMS, AND NOTHING IN THIS TREE WOULD NOTICE.**`, :20166 `> *** THE REASON NOTHING
      CATCHES IT: \`#491\`'s ONLY DETECTOR IS THE BUILD-WARNING GATE. ***`.  The ledger has this row
      `dropped`, title `WITHDRAWN -- #491's ternary swap is NOT undetected ...` (ledger.json:47678-47681),
      and the measurement above refutes the headline sentence directly.  The bug-file entry carries no
      withdrawal while the very next heading (`pcc2c040returnmutant`, :20190) carries the house form
      `*[#560: as filed; superseded by ...]*`.  Annotate in place: WITHDRAWN 2026-09-17, caught by
      regress/diff_diskimage_io.c (abort + rows red), gate_offline.sh.
F2.2  WRONG RECORD (stale state) -- OUTSTANDING_BUGS.md:787-789, in the open-list head: `> ### OPEN -- filed
      2026-08-29: what the re-run battery found behind a five-day-old red` / `**\`diskimagesign\`** -- IN WORK as
      \`#491\`.`  The ledger closed the row 2026-09-11 ("THE LEDGER WAS THE STALE SIDE HERE" -- the same note
      that said the bug file was right); the file's own charter is "Resolved ones are removed, not annotated".
      The entry below it (`propagatecpsilent`, :799) is already called out as HALF-annotated for the same reason.
F2.3  RECORDS, imprecise not false -- the witness `detector:regress/artifacts/diskimagesign/cascade_20260829`
      names a directory of gate LOGS, not a detector (check_witness.py's ghost check never sees it: no .py/.c/.sh).
      The house precedent (wdcoddstep) names the instrument.  The detectors are regress/gate_build.sh
      (`$lab: warnings` = 0) and regress/diff_diskimage_io.c (gate_offline.sh); the cascade dir is the preserved
      measurement.

======================================================================================================
3. sgirergbroundtrip  (closed, 7a41b3f -- #505)
======================================================================================================
READ
* Ledger row (ledger.json:37984-...): closed, med, commits 7a41b3f, witness (:37989)
  `probe:regress/sgi_re_rgb_probe.py -- prefix_a264a34.raw SGIRGB_RESULT=4/6, postfix_505.raw ... 10/10 ...
  NOTE THE DENOMINATORS DIFFER ... Wired at gate_arm.sh.`  The state_note records the same-script pair
  (`killtable6_20260907/prefix10row 4/10` vs base 10/10) and the #505 CHANGELOG pointer correction.
* The hunk (a264a34d..7a41b3f, src/devices/dev_sgi_re.c): GET `case DE_MODE_TYPE_RGB:` `(buf[1] << 24) +
  (buf[2] << 16) + (buf[3] << 8)` -> `(buf[0] << 24) + (buf[1] << 16) + (buf[2] << 8)` with the #505
  comment; at HEAD (:408) the corrected form survives through four later commits to the file.
* Probe: 0 diff lines 7a41b3f..HEAD.  Gate (regress/gate_arm.sh HEAD :1610-1651): runs
  sgi_re_rgb_probe.py, SGIRGB_DONE sentinel, SGIRGB_WITNESS=PASS, all ten rows by name with the two-space
  anchor, emitted/green/red pinned 10/10/0 -- the block is the same as at 7a41b3f (:1322-1360) plus a #556
  comment; gate_arm is in run.sh GATES.  check_probe_wiring.py: CLASS_DETECTOR (:728).
* CHANGELOG.md:7957-7958 carries the rgb_witness.py -> sgi_re_rgb_probe.py correction in place.
* Artifacts: prefix_a264a34.raw 4/6 and postfix_505.raw 10/10 exist; killtable6_20260907/ base 10/10,
  base_recheck 10/10, M1..M14 all killed except M4_or (recorded EQUIVALENT), prefix10row 4/10, nullmedium 1/10.

RAN  (SCRATCH\runprobes_rgd.log; probe_sgi_sgi_parent.out, probe_sgi_sgi_commit.out)
Committed probe from the 7a41b3f tree's own regress dir (md5 cbe1c089...), one instrument, both builds fresh
(binary newer than dev_sgi_re.c, MAKE_RC=0, distinct md5s):
    PARENT a264a34d   SGIRGB_RESULT=4/10  FAIL  -- rgb chan, rgb not corrupt, rgb samemode, rgb depth64, rgb tiled,
                                                   rgb tiled64 all read 0xbbccdd00 (the buf[1..3] shift)
    COMMIT 7a41b3f    SGIRGB_RESULT=10/10 PASS
Both end SGIRGB_DONE.  Same figures as the preserved prefix10row.raw / base.raw -- clause (i) on the
committed parent/commit pair, one script.

NOTE (records suggestion, not a wrong record): the witness field cites only the 4/6 -> 10/10 cross-instrument
pair and flags it; the same-script 4/10 -> 10/10 pair it needs is in the artifacts
(killtable6_20260907/prefix10row.raw, base.raw) and now re-measured on the true parent -- cite it there.

======================================================================================================
4. landiskaux  (closed, e16a8b7 -- #533)
======================================================================================================
READ
* Ledger row (ledger.json:27953-28329): closed, commits e16a8b7, witness (:28325)
  `boot:regress/artifacts/landiskaux/boot_20260918/ -- drive_guest.py landisk ... SAME script: pre-fix emulator
  log 12 unmapped accesses at 0x1400002c, fixed 0; both reach the shell ... Rung-3 companion: .../rung3_opus_20260918/`.
  The only `regress` entry is the peer Opus late review marked NOT A SEAT ANSWER; this is the owed review.
* The hunk (686d179c..e16a8b7, src/devices/dev_wdc.c): `case MACHINE_LANDISK:` ... `alt_status_addr =
  devinit->addr + 0x2c; break;` appended AFTER MACHINE_IQ80321, as the panel prescribed; at HEAD :2110, and
  dev_wdc.c has 0 diff lines since e16a8b7.
* Probe: 16 diff lines e16a8b7..HEAD, all docstring (#556 late-review note); comment/docstring-stripped
  token stream identical.  Gate (regress/gate_sh_rounding.sh HEAD :1687-1727, committed): runs
  landisk_aux_probe.py "$PMAX" "$KERNEL", LANDISK_AUX_DONE sentinel, PARSE-BEFORE-SCORE, rows run 6, rows
  correct 6, `live` control by name, the five rows by full name -- unchanged from e16a8b7 (:1672-1712);
  the file's 54 diff lines since are #556 comments; the peer's UNCOMMITTED edit to this file touches hunks at
  :527/:587/:819 only.  gate_sh_rounding is in run.sh GATES.
* Boot witness (boot_20260918/): drive_landisk_prefix.log carries exactly twelve `[ memory WRITE: to
  non-existant paddr=0x1400002c len=1 pc=0x8c15f6e8 <obio_iomem_write_1+0x8> ]` lines, drive_landisk_fixed.log
  zero; both boot_*.out VERDICT=PASS, SH7751R, 42.  The field says exactly that; the guest-visible consequence
  (the reset never performed) is the rung-3 probe's `aux 2c reset` 0x09 -> 0x01, which the field names as the
  companion.  Clause (ii): `live` (RAM session, status 0x09) is the liveness control, `aux 2c rest` (0x2c
  answers the status byte) the device signature.
* Kill-table instrument: detector_20260918/landisk_aux_probe.frozen.py differs from the committed probe ONLY
  in docstring text and the `aux 206 gone` note string ("0x206 is UNMAPPED on landisk ..." -> "0x206 reads 0
  (unmapped OR declined -- cannot tell)") -- the L4 the CHANGELOG records; no oracle differs, so TABLE.out
  (base 6/6, M_head 1/6, M_0x16 3/6, M_0x2d 3/6, M_both 4/6, M_above 3/6) transfers to the committed probe.
  PRETABLE.out (08:28) predates the table logs (08:29-08:36).

RAN  (SCRATCH\runprobes_rgd.log; probe_land_land_parent.out, probe_land_land_commit.out)
Committed probe from the e16a8b7 tree (md5 710960d4...), kernel _images/openbsd76-landisk-bsd.rd (read-only),
one instrument, both builds fresh:
    PARENT 686d179c   LANDISK_AUX_RESULT=1/6  VECTOR=1,0,0,0,0,0 -- aux 2c rest 0x0, aux 206 gone 0x9,
                                                                    aux 2c reset 0x9, aux 2c read 0x0, 206 ctl dead 0x1
    COMMIT e16a8b7    LANDISK_AUX_RESULT=6/6  VECTOR=1,1,1,1,1,1
Both end LANDISK_AUX_DONE.  The round's pre-fix 1/6 was taken on "build/ = the working tree MINUS the landisk
case" (CHANGELOG.md:2906), not on the committed parent; the true parent reproduces it value for value.

FINDINGS
F4.1  WRONG RECORD (stale) -- the closed row's own fields still describe an unshipped round: ledger.json:28324
      `"hold": "READY TO IMPLEMENT.  The panel's gate -- 'ship, but not on this packet' -- is discharged: ..."`
      and :28327 `"hold_question": "FIX DESIGN IS SETTLED (see 2026-09-18 correction): ... OWED before the edit:
      the rung-3 witness -- a guest byte store to 0x1400002c on unmodified -E landisk ..."`.  The fix shipped
      in e16a8b7 and the rung-3 witness exists (rung3_opus_20260918/).  Clear both or date them as history --
      the carrier's own sgiarcbiosoob case is this shape.

======================================================================================================
5. pcc2c040mienannounce  (closed, bb8efbf -- #535)
======================================================================================================
READ
* Ledger row (ledger.json:51279-51406): closed, MED, commits bb8efbf, witness (:51284)
  `probe:regress/pcc2_c040_probe.py (rows \`c040 says mien', \`c040 once mien'; gated in gate_arm.sh)`.
* bb8efbf changed NO src/ file (stat: regress/, tools/, artifacts only); src/devices/dev_pcc2.c has 0 diff
  lines bb8efbf..HEAD.  CHANGELOG.md:2702 block: "No emulator code changes".
* The committed probe is token-identical (comments and docstrings stripped) to Opus's measured
  r535_20260918/opus535/probe.r2.py, and HEAD's probe is token-identical to bb8efbf's (16 diff lines, the
  #560 comment).  Both new rows read `td`, the 0x06 session (:501, :560, :572).
* Gate (regress/gate_arm.sh HEAD :1738-1750): runs `pcc2_c040_probe.py "$PMAX" gate`, PCC2C040_DONE
  sentinel, all 18 rows by name incl. `c040 says mien` and `c040 once mien`, emitted/green/red 18/18/0.
  check_probe_wiring.py :736 CLASS_DETECTOR with the #535 reclass recorded.  gate_arm is in run.sh GATES.
* Artifacts (r535_20260918/opus535/): r2_BASE 18/18, r2_A 17/18, r2_F 17/18, each red on exactly `c040 once
  mien` with count 7, all ending PCC2C040_DONE; mutate.py anchors; fable5_lastseat.md (badge s).

RAN  (SCRATCH\runprobes_rgd.log; probe_pcc2_{BASE,A_latch_bypass_mien,F_latchset_mienclear,M_announce_notmien}.out)
bb8efbf tree, committed probe (md5 dc2a7a5b...), dev_pcc2.c md5 d13d150a...; a clone-local .MUTANT sentinel,
each mutant applied by the preserved anchors (count must be 1), `rm dev_pcc2.o; make -j4`, `[ gxemul -nt
dev_pcc2.c ]` checked before every run:
    BASE                                   18/18 PASS
    A_latch_bypass_mien   (pass-2 L2)      17/18 FAIL  c040 once mien: got 7 want 1
    F_latchset_mienclear  (pass-2 L2)      17/18 FAIL  c040 once mien: got 7 want 1
    M_announce_notmien    (pass-1 L2)      16/18 FAIL  c040 says mien: no want yes; c040 once mien: 0 want 1
    BASE restore: cmp against bb8efbf's dev_pcc2.c clean, binary fresh, sentinel CLEARED.
All four end PCC2C040_DONE.  The {presence, count} x {MIEN} product is rowed and each cell's mutant is
killed by the row written for it; the pass-1 mutant that swept the shipped 16-row probe is red on both rows.
(A peer session ran its own pcc2 probe concurrently; it writes the same four zero bytes to the probe's shared
/tmp/pcc2_c040_dummy.bin, which is benign, and no row went spuriously red.)

FINDINGS
F5.1  WRONG RECORD (witness kind) -- ledger.json:51284 `"witness": "probe:regress/pcc2_c040_probe.py (rows
      \`c040 says mien', \`c040 once mien'; gated in gate_arm.sh)"`.  `probe:` is the rung-3 term for a guest
      instruction witnessing an EMULATOR defect, and check_witness.py scores it rung 3; this round's subject is
      the test apparatus (a missing detector cell), it changed no src/ file, and its proof is a mutation
      (16/16 -> 16/17; A/F 17/17 -> 17/18).  The carrier's own definition makes that `harness:`; the sibling
      detector-repair rows on this very probe use `detector:` (pcc2c040assertrow, pcc2c040ctlq).  Re-key it,
      e.g. `detector:regress/pcc2_c040_probe.py -- rows c040 says mien / c040 once mien; A 17/18, F 17/18,
      M_announce_notmien 16/18 vs base 18/18 (r535_20260918/opus535/, re-measured 2026-10-09)`.
F5.2  WRONG RECORD (stale severity) -- OUTSTANDING_BUGS.md:21890 `### \`pcc2c040mienannounce\` (LOW) --
      predicted: an announce gated on !MIEN passes all 16 rows ...`; the ledger carries MED ("Severity LOW -> MED;
      this is an L2 repair", the opus5 assess entry) and the tail entry at :21902 does not restate the
      re-grade.  The file's own form for this is two lines above (:21888 `fiqenableread (MED; it said LOW until
      #554 re-graded it, 2026-10-02)`).

======================================================================================================
WHAT WAS NOT RUN, AND WHY
======================================================================================================
* pcc2c040mienannounce parent/commit binary pair: deliberately not built -- bb8efbf changed no product
  source, so the two binaries would be behaviourally identical and discriminate nothing; the discriminating
  runs are the committed probe against the three mutants, which were run on the commit tree.
* The battery gates themselves (gate_offline, gate_arm, gate_sh_rounding, gate_build) were NOT run (no gate
  by instruction); their wiring was read at HEAD and the detectors were run with the gates' own compile lines
  or probe invocations.
* wdcaltctrlbit at HEAD was measured on the offline differential only (its carrier); no emulator build is
  involved in that row.

ARTIFACTS (SCRATCH\)
build_rgd.sh / build_rgd.log (five builds, MAKE_RC=0, freshness checks, device md5s);
offline_rgd.sh / offline_rgd.log + offline_out\ (wdc_*.out, io_*.out, *.cc);
runprobes_rgd.sh / runprobes_rgd.log + probe_sgi_*.out, probe_land_*.out, probe_pcc2_*.out;
frozen\ (every detector, gate and device source at its commit and at HEAD, from git show);
work\ (the nine git-archive tarballs, ledger_HEAD.json); inspect_off.sh.
/tmp/gxfable_rgd (WSL) is volatile and may be deleted.
