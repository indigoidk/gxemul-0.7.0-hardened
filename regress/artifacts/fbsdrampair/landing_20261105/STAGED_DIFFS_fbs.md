# STAGED_DIFFS_fbs.md -- what the fbsdrampair landing commits for each shared file, against HEAD and the working copy

HEAD ab39ba0d.  Round number #585 (derived: max round heading in HEAD's CHANGELOG.md (#584) + 1).  Built by the landing kit's build_staged_fbs.py from `git show HEAD:<path>` and the working copy, at 2026-11-06 15:49 local.  This record lands as `regress/artifacts/fbsdrampair/landing_20261105/STAGED_DIFFS_fbs.md`.

## src/devices/dev_footbridge.c (staged = the working copy with its three `#NNN` comment tags set to #585)

HEAD 34970 bytes md5 0b3370b87bed1d03989e9db3c457102f (== `regress/artifacts/fbsdrampair/impl_20261105/dev_footbridge.c.pre_fbs`, the pre-fix source of every table's HEAD leg).  Working copy 36163 bytes md5 ccaf09d4d30c5a29e6fe0422c0681314 (== `regress/artifacts/fbsdrampair/table1_20261105/dev_footbridge.c.fix1`, the source table 1 measured: table1_20261105/MD5.txt).  Staged 36163 bytes md5 3de599da243837671786aa5ef05dfa86.

Every working-tree hunk is this round's: 3 hunks, 29 lines added and 4 removed (`git diff --stat`: 29 insertions, 4 deletions), each inside one of the two constructs the round edits (HEAD's lines: DEVICE_ACCESS(footbridge) 508-781; struct footbridge_data 60-95), each adding a latch field or the comment carrying its `#NNN` tag, and the only removed lines the two `fatal("[ footbridge read from sdram_ba_...]\n"); exit(1);` pairs:

* HEAD line 95: 0 line(s) -> 5 line(s), inside struct footbridge_data
* HEAD line 734: 2 line(s) -> 16 line(s), inside DEVICE_ACCESS(footbridge)
* HEAD line 759: 2 line(s) -> 8 line(s), inside DEVICE_ACCESS(footbridge)

### the working copy vs HEAD (the round's whole change; the staged file differs from it only in the three tags below)

3 hunk(s):

```
@@ insert  first side line 95 (0 lines) -> second side line 95 (5 lines)
+     /*  #NNN: one warn-once latch per SDRAM register READ that used to end
+         the process (7.3.9, 7.3.10: both registers are R/W).  Zeroed by
+         the same memset and calloc as the five above.  */
+     int        warned_sdram_mask_r;
+     int        warned_sdram_offset_r;
@@ replace  first side line 734 (2 lines) -> second side line 739 (16 lines)
-             fatal("[ footbridge read from sdram_ba_mask ]\n");
-             exit(1);
+             /*  #NNN: an R/W register (DC21285 7.3.9; 7.3.10 for
+                 104h), so this read is legal -- it used to end the
+                 emulator with exit(1).  The write arms keep nothing
+                 (hardware would read back W & 0x8ffc0000 here,
+                 W & 0x0ffc0000 at 104h; keeping writes is filed),
+                 so the read is declined: odata stays 0 and the
+                 common tail below returns it -- keep the break.
+                 0 is also both registers' normal reset value;
+                 00FC0000h is only the mask's blank-ROM-programming
+                 default.  Announced once per register.  */
+             if (!d->warned_sdram_mask_r) {
+                 d->warned_sdram_mask_r = 1;
+                 fatal("[ footbridge: read of sdram_ba_mask "
+                     "declined, reads 0 (written values are "
+                     "not kept) (once) ]\n");
+             }
@@ replace  first side line 759 (2 lines) -> second side line 778 (8 lines)
-             fatal("[ footbridge read from sdram_ba_offset ]\n");
-             exit(1);
+             /*  #NNN: declined with 0 and announced once, as for
+                 SDRAM_BA_MASK (7.3.10: R/W, reset value 0).  */
+             if (!d->warned_sdram_offset_r) {
+                 d->warned_sdram_offset_r = 1;
+                 fatal("[ footbridge: read of sdram_ba_offset "
+                     "declined, reads 0 (written values are "
+                     "not kept) (once) ]\n");
+             }
```

### the fill (staged vs the working copy)

Three `#NNN` -> `#585`, each inside a C comment (kit_fbs.fill_c asserts it), same width, so no line moves; comment-free forms equal: True.  The round number is HEAD-relative (derived: max round heading in HEAD's CHANGELOG.md (#584) + 1) and is re-derived whenever this builder runs.

```
line 95: /*  #585: one warn-once latch per SDRAM register READ that used to end
line 739: /*  #585: an R/W register (DC21285 7.3.9; 7.3.10 for
line 778: /*  #585: declined with 0 and announced once, as for
```

### the four trees (TREES_fbs.txt)

```
est                                      part 1 PASS (== the SEC working copy, md5 3de599da2438); part 2 N/A (source tree, no binary); sentinels none
                                           vs staged: 0 hunk(s) (the tree update has run: the tree holds the staged file)
build                                    part 1 PASS (== the SEC working copy, md5 3de599da2438); part 2 PASS: binary newer (gxemul 11-06 14:24:07, dev_footbridge.c 11-06 14:23:56); sentinels none
                                           vs staged: 0 hunk(s) (the tree update has run: the tree holds the staged file)
build-asan                               part 1 PASS (== the SEC working copy, md5 3de599da2438); part 2 PASS: binary newer (gxemul 11-06 14:24:32, dev_footbridge.c 11-06 14:23:56); sentinels none
                                           vs staged: 0 hunk(s) (the tree update has run: the tree holds the staged file)
//wsl.localhost/Gentoo/tmp/gxsec-build   part 1 PASS (== the SEC working copy, md5 3de599da2438); part 2 PASS: binary newer (gxemul 11-06 14:24:35, dev_footbridge.c 11-06 14:23:56); sentinels none
                                           vs staged: 0 hunk(s) (the tree update has run: the tree holds the staged file)
TREES_SUMMARY ALL CLEAR: the landing window's tree update has run (UPDATE_FBS.out), so the SEC working copy and all four trees hold the staged dev_footbridge.c (md5 3de599da243837671786aa5ef05dfa86), and the three build trees' binaries are newer than it
```

## regress/gate_arm.sh

HEAD 167781 bytes md5 36f7b1bed04c26dde9b4553cd6d70864; staged 169943 bytes md5 a059e4392267c0e00f17a5779609457e; working copy 169942 bytes md5 e23ed42545161a181a55fe407e9a1495 (READ only).  HEAD's footbridge block: lines 1060-1169 (110 lines); the working copy's: lines 1060-1192 (133 lines).  The staged block is the working copy's footbridge block, which equals HEAD's block plus the banked diff exactly, with its two `#NNN` tags set to `#585`; its difference from HEAD's block is exactly `regress/artifacts/fbsdrampair/impl_20261105/gate_arm.sh.fbs.diff` (three hunks: the display regex, the ROWS pin 37 -> 56, six SDRAM checks).  The block carries 30 `check` calls; 29 run on a log with a verdict (the other is its no-verdict arm).  `bash -n` on the staged file: clean.

### staged vs HEAD (the commit's whole diff of this file)

3 hunk(s):

```
@@ replace  first side line 1083 (1 lines) -> second side line 1083 (1 lines)
- grep -E "^(  arm |C[0-9]|A[0-9]|I1|H[12]|D1|E(C1|A1|[0-6])|S(C1|A1|[1-5]|F[12])|N[0-5O]) " "$FBLOG" | sed 's/^/       /'
+ grep -E "^(  arm |C[0-9]|A[0-9]|I1|H[12]|D1|E(C1|A1|[0-6])|S(C1|A1|[1-5]|F[12])|N[0-5O]|[MOXWBU](C|[1-3])) " "$FBLOG" | sed 's/^/       /'
@@ replace  first side line 1126 (3 lines) -> second side line 1126 (4 lines)
-     #  stand in for a missing id -- pass 2), and the probe's own total by ROWS=.
-     check "footbridge: the sites probe ran all 37 rows green (ROWS=37 of 37)" \
-           "$(grep -cE '^ROWS=37 of 37$' "$FBLOG")" "1"
+     #  stand in for a missing id -- pass 2), and the probe's own total by ROWS= (37 at #545; 56 since
+     #  #585 added the nineteen SDRAM rows below).
+     check "footbridge: the sites probe ran all 56 rows green (ROWS=56 of 56)" \
+           "$(grep -cE '^ROWS=56 of 56$' "$FBLOG")" "1"
@@ insert  first side line 1165 (0 lines) -> second side line 1166 (22 lines)
+     #  #585 fbsdrampair: a guest READ of SDRAM_BA_MASK (+0x100) or SDRAM_BA_OFFSET (+0x104) used to end
+     #  the emulator (fatal() then exit(1)); both are R/W (DC21285 7.3.9, 7.3.10) and both write arms keep
+     #  nothing, so the read is DECLINED with 0 and announced once per register.  Six arms, one process
+     #  each: M and O read one register three times (one site per process, so the pre-fix build shows
+     #  each site's own death), X reads both (per-register latches), W only writes (a write never takes the
+     #  read path; HEAD's write announces intact), B writes, reads, writes again (writes are not kept; a
+     #  write with the read latch set still takes the write path), U is M's reads with the MMU left ON
+     #  (never the device).  Each control (MC OC XC WC BC UC) is a `reg` taken BEFORE the arm's first
+     #  SDRAM access, so the pre-fix build reds M1-M3 O1-O3 X1 B1-B3 under green controls (measured,
+     #  regress/artifacts/fbsdrampair/impl_20261105/probe_HEAD.out: ROWS=46 of 56, CONTROL=OK).
+     check "footbridge: SDRAM controls MC OC XC WC BC UC -- six DISTINCT green ids" \
+           "$(grep -E '^[MOXWBU]C .*ok$' "$FBLOG" | cut -d' ' -f1 | sort -u | wc -l | tr -d ' ')" "6"
+     check "footbridge: SDRAM rows M1-M3 O1-O3 X1 W1 W2 B1-B3 U1 -- thirteen DISTINCT green ids" \
+           "$(grep -E '^([MOB][1-3]|X1|W[12]|U1) .*ok$' "$FBLOG" | cut -d' ' -f1 | sort -u | wc -l | tr -d ' ')" "13"
+     check "footbridge: M2 three SDRAM_BA_MASK reads each return 0 (the declined value)" \
+           "$(grep -cE '^M2 .*r7=0x00000000 r8=0x00000000 r9=0x00000000 .*ok$' "$FBLOG")" "1"
+     check "footbridge: O2 three SDRAM_BA_OFFSET reads each return 0" \
+           "$(grep -cE '^O2 .*r7=0x00000000 r8=0x00000000 r9=0x00000000 .*ok$' "$FBLOG")" "1"
+     check "footbridge: X1 one read announce per register, mask first" \
+           "$(grep -cE '^X1 .*order=mask,offset .*ok$' "$FBLOG")" "1"
+     check "footbridge: B1/B2 a written mask/offset is not kept (reads 0 after a write)" \
+           "$(grep -cE '^B[12] .*r[78]=0x00000000 .*ok$' "$FBLOG")" "2"
```

### the working copy outside its footbridge block, against HEAD (NOT carried: other rounds' uncommitted edits)

1 hunk(s):

* HEAD line 1990 (outside the block), delete (1 -> 0 lines; blank)

## regress/footbridge_sites_probe.py

Staged = the working copy with its twelve `#NNN` tags filled (11 hunk(s), all comment or docstring lines).  PROBE_IDENTITY_fbs.md: tree minus docstrings, every other string kept, equal to the working copy's: True; equal to table 1's frozen instrument's: True.  HEAD's probe == impl_20261105/footbridge_sites_probe.py.pre_fbs, so the working copy's whole difference from HEAD is this round's.

### staged vs the working copy

11 hunk(s):

```
@@ replace  first side line 52 (2 lines) -> second side line 52 (2 lines)
- writes) instead of dying, and #NNN declines the last two -- the SDRAM reads at +0x100/+0x104
- (`fbsdrampair`, arms M/O/X/W/B/U below; until #NNN this line said no arm here touched them) --
+ writes) instead of dying, and #585 declines the last two -- the SDRAM reads at +0x100/+0x104
+ (`fbsdrampair`, arms M/O/X/W/B/U below; until #585 this line said no arm here touched them) --
@@ replace  first side line 176 (1 lines) -> second side line 176 (1 lines)
- ARMS M, O, X, W, B, U (#NNN, `fbsdrampair`) -- the two SDRAM register READS, SDRAM_BA_MASK (+0x100)
+ ARMS M, O, X, W, B, U (#585, `fbsdrampair`) -- the two SDRAM register READS, SDRAM_BA_MASK (+0x100)
@@ replace  first side line 178 (1 lines) -> second side line 178 (1 lines)
- (DC21285 7.3.9, 7.3.10) and both write arms keep nothing, so #NNN DECLINES the read: odata stays 0
+ (DC21285 7.3.9, 7.3.10) and both write arms keep nothing, so #585 DECLINES the read: odata stays 0
@@ replace  first side line 240 (1 lines) -> second side line 240 (1 lines)
- COST, measured: see PROBE_WALL below -- 12 cold-debugger launches (#545: +S, +Q, +H; #NNN: +M, O, X,
+ COST, measured: see PROBE_WALL below -- 12 cold-debugger launches (#545: +S, +Q, +H; #585: +M, O, X,
@@ replace  first side line 347 (1 lines) -> second side line 347 (1 lines)
- #  #NNN (fbsdrampair): arms M, O, X, W, B, U.  Every SDRAM operand and every value-row destination's
+ #  #585 (fbsdrampair): arms M, O, X, W, B, U.  Every SDRAM operand and every value-row destination's
@@ replace  first side line 431 (1 lines) -> second side line 431 (1 lines)
-     """#NNN (fbsdrampair): run_arm's own `reg` parse, as a function, for the snapshot taken before an
+     """#585 (fbsdrampair): run_arm's own `reg` parse, as a function, for the snapshot taken before an
@@ replace  first side line 445 (1 lines) -> second side line 445 (1 lines)
-     BEFORE teardown.  #NNN (fbsdrampair): `data` plants extra (address, word) RAM operands, and
+     BEFORE teardown.  #585 (fbsdrampair): `data` plants extra (address, word) RAM operands, and
@@ replace  first side line 506 (1 lines) -> second side line 506 (1 lines)
-     pre = {}                       # #NNN: the registers just before `snap_at` is stepped
+     pre = {}                       # #585: the registers just before `snap_at` is stepped
@@ replace  first side line 645 (1 lines) -> second side line 645 (1 lines)
- #  #NNN (fbsdrampair): snap_at = each arm's first SDRAM access.
+ #  #585 (fbsdrampair): snap_at = each arm's first SDRAM access.
@@ replace  first side line 804 (1 lines) -> second side line 804 (1 lines)
- #  ---- #NNN (fbsdrampair): the SDRAM reads are DECLINED with 0 and announced once per register.  Each
+ #  ---- #585 (fbsdrampair): the SDRAM reads are DECLINED with 0 and announced once per register.  Each
@@ replace  first side line 920 (1 lines) -> second side line 920 (1 lines)
-            and mc and oc and xc and wc and bc and uc and u1)      # #NNN: the six SDRAM arms' controls
+            and mc and oc and xc and wc and bc and uc and u1)      # #585: the six SDRAM arms' controls
```

### staged vs HEAD (the commit's whole diff of this file)

14 hunk(s):

```
@@ replace  first side line 52 (4 lines) -> second side line 52 (5 lines)
- writes) instead of dying, so nothing a guest can do to this device ends the process any more
- -- except the two SDRAM reads at +0x100/+0x104 (`fbsdrampair`), which no arm here touches.  The
- control that "this harness notices a dead child" therefore has to come from the HARNESS, and
- it comes from two legs that need no product defect:
+ writes) instead of dying, and #585 declines the last two -- the SDRAM reads at +0x100/+0x104
+ (`fbsdrampair`, arms M/O/X/W/B/U below; until #585 this line said no arm here touched them) --
+ so nothing a guest can do to this device ends the process any more.  The control that "this
+ harness notices a dead child" therefore has to come from the HARNESS, and it comes from two legs
+ that need no product defect:
@@ insert  first side line 175 (0 lines) -> second side line 176 (55 lines)
+ ARMS M, O, X, W, B, U (#585, `fbsdrampair`) -- the two SDRAM register READS, SDRAM_BA_MASK (+0x100)
+ and SDRAM_BA_OFFSET (+0x104), used to end the process with fatal() then exit(1).  Both are R/W
+ (DC21285 7.3.9, 7.3.10) and both write arms keep nothing, so #585 DECLINES the read: odata stays 0
+ (also both registers' normal reset value), the common tail returns it, and each register announces
+ ONCE through its own latch.  Six arms, six processes.  Each arm verifies its prologue in a `reg`
+ taken BEFORE its first SDRAM access (`snap_at`), so its control row (MC OC XC WC BC UC) holds on a
+ build that ends the process at that access: the pre-fix build shows the defect rows red under green
+ controls.  Every value-row destination is preloaded with 0x12345678 from RAM, so a 0 read back
+ proves the load wrote it; every SDRAM operand is loaded from RAM (SD_DATA, DATA+16..+32).
+   M  three mask reads -> r7,r8,r9          M1 survived, exit 0    M2 each read returns 0
+                                             M3 the arm's diagnostics are exactly [mask announce]
+   O  the same three reads of +0x104         O1 O2 O3 likewise.  ONE SITE PER PROCESS: the pre-fix
+                                             build ends at the first read, so M and O each show
+                                             their own site's death
+   X  mask, mask, offset, offset             X1 the diagnostics are exactly [mask announce, offset
+                                             announce], in that order -- one latch per register
+   W  mask <- 0x01FC0000, mask <- 0x12345678, W1 survived, exit 0, no read announce (a write never
+      offset <- 0, offset <- 0x00040000         takes the read path)
+                                             W2 the write announces are exactly [mask 0x12345678,
+                                             offset 0x40000]: HEAD's write arms, unchanged
+   B  mask <- 0x03FC0000, offset <- 0x40000,  B1 mask read = 0 (not 0x03FC0000), announced once
+      read mask, read offset,                 B2 offset read = 0 (not 0x40000), announced once
+      mask <- 0x12345678, offset <- 0x80000   B3 both AFTER-THE-READ writes still announce: a write
+                                             with the read latch SET still takes the write path
+   U  arm M's reads with the MMU LEFT ON      U1 survived, exit 0, NO footbridge diagnostic, both
+      (VA 0x42000100/104 -> PA 0x02000100/104,  loads completed with 0 -- a CONTROL: it never
+      past -M 32's RAM end: zero fill)           reaches the device, so no product edit can red it
+ The announces are matched as WHOLE bracketed lines (SD_MASK, SD_OFFSET), so a misnamed register,
+ HEAD's exit text kept without its exit, or any extra footbridge diagnostic reds the row.
+ Values are DERIVED from the code, not fitted: odata is initialised to 0 and the read arms never
+ assign it; the write arms' announce texts are `%#llx` of the value written, and 0x01FC0000 /
+ 0x03FC0000 are Table 7-7 values the mask whitelist accepts silently.
+ SDRAM CONTRACT -- designed to catch: the exit reinstated at either site (M1-M3 / O1-O3, X1, B1-B3)
+ or kept after the new announce (mask: M1/M2, X1, B1-B3; offset: O1/O2, B1-B3, measured 51/56 in
+ artifacts/fbsdrampair/settle_20261105/SCORES.txt); the announce unlatched (M3/O3 count 3, X1) or never made -- removed, latch test
+ inverted or never passing, HEAD's text restored without
+ the exit, the read predicate never true (M3/O3, X1, B1/B2); a latch shared between the registers
+ in either direction (X1, B2) or one arm setting the other's latch (mask arm: M3, X1, B2; offset
+ arm: O3, X1); a nonzero
+ declined value at either site, inside or outside the latch -- e.g. the blank-ROM 0x00FC0000 (M2/O2,
+ B1/B2); the read predicate inverted (M3/O3, X1, W1, W2, B3), made always true (W1, W2, B3), its
+ operand swapped for the latch (`latch == MEM_READ`: W1) or widened by `|| latch` (B3); the write
+ path setting the read latch (B1/B2); a written value kept and returned (B1/B2).
+ NOT COVERED, each derived from the code, none assumed: (1) an early `return 1` after the announce is
+ EQUIVALENT -- memory_rw.c (#95) zeroes the read buffer before the handler runs and the declined
+ value is 0, so the guest reads 0 either way (M2/O2 would see it if either premise changed);
+ (2) the predicate qualified by the latch (`&& !latch`) is EQUIVALENT under a 0 decline: later reads
+ take the write arm with idata 0, which the mask whitelists and the offset does not announce;
+ (3) a width conjunct (`&& len == 4`): every SDRAM row is a word access and the decline tests no
+ width, so byte and halfword reads are unrowed; (4) the two arms exchanging latches consistently is
+ a renaming, EQUIVALENT; (5) W2 and B3 pin HEAD's write announces, and change legitimately when the
+ write side (`fbsdramwrites`, filed) lands; (6) the hardware read-back (W & 0x8ffc0000, W &
+ 0x0ffc0000) is NOT modelled, and B1/B2 pin that it is not; (7) arm U's sentinel form (store
+ through the alias, read it back) is unavailable at -M 32: PA 0x02000100 is past the end of RAM.
+ 
@@ replace  first side line 184 (1 lines) -> second side line 240 (2 lines)
- COST, measured: see PROBE_WALL below -- 6 cold-debugger launches (#545: +S, +Q, +H), no boot.  A booting-rig row
+ COST, measured: see PROBE_WALL below -- 12 cold-debugger launches (#545: +S, +Q, +H; #585: +M, O, X,
+ W, B, U), no boot.  A booting-rig row
@@ insert  first side line 290 (0 lines) -> second side line 347 (80 lines)
+ #  #585 (fbsdrampair): arms M, O, X, W, B, U.  Every SDRAM operand and every value-row destination's
+ #  sentinel comes from RAM (`ldr rd,[r4,#n]`, r4 = 0x9000), planted by run_arm's `data`.
+ def _ldr4(rd, off):
+     return 0xE5940000 | (REG[rd] << 12) | off, "ldr %s,[r4,#%d]" % (rd, off)
+ SD_SENT = 0x12345678                    # DATA+4 (A2's value): the destinations' sentinel
+ SD_DATA = [(DATA + 16, 0x01FC0000),     # SDRAM_MASK_32MB: a Table 7-7 value, whitelisted, silent
+            (DATA + 20, 0x03FC0000),     # SDRAM_MASK_64MB: whitelisted and != 0 -- what a backing edit keeps
+            (DATA + 24, 0x00040000),     # offset bit 18 (27:18 R/W): the offset write arm announces it
+            (DATA + 28, 0x00080000),     # offset bit 19: B3's after-the-read write, a DIFFERENT announce
+            (DATA + 32, 0x00000000)]     # offset 0: not announced
+ #  The device's own texts (dev_footbridge.c `case SDRAM_BA_MASK:` / `case SDRAM_BA_OFFSET:`), matched as
+ #  WHOLE bracketed lines.  SD_W*: the write arms' unchanged announces, `%#llx` of the value written.
+ SD_MASK = "[ footbridge: read of sdram_ba_mask declined, reads 0 (written values are not kept) (once) ]"
+ SD_OFFSET = "[ footbridge: read of sdram_ba_offset declined, reads 0 (written values are not kept) (once) ]"
+ SD_WMASK = "[ footbridge write to sdram_ba_mask 0x12345678 ]"
+ SD_WOFF4 = "[ footbridge write to sdram_ba_offset 0x40000 ]"
+ SD_WOFF8 = "[ footbridge write to sdram_ba_offset 0x80000 ]"
+ SD_NAMES = {SD_MASK: "mask", SD_OFFSET: "offset", SD_WMASK: "wmask", SD_WOFF4: "woff4", SD_WOFF8: "woff8",
+             "[ footbridge read from sdram_ba_mask ]": "oldmask",          # HEAD's exit texts
+             "[ footbridge read from sdram_ba_offset ]": "oldoffset"}
+ SD_MREAD = [                            # arm M: three SDRAM_BA_MASK reads
+     _w(0x2c, _ldr4("r7", 4), "r7 <- sentinel"),
+     _w(0x30, _ldr4("r8", 4), "r8 <- sentinel"),
+     _w(0x34, _ldr4("r9", 4), "r9 <- sentinel"),
+     _w(0x38, _ldr("r7", 0x100), "M: SDRAM_BA_MASK read #1 -> 0, announced (snap_at)"),
+     _w(0x3c, _ldr("r8", 0x100), "M: read #2 -> 0, silent"),
+     _w(0x40, _ldr("r9", 0x100), "M: read #3 -> 0, silent"),
+     (0x44, NOP, NOPTXT, "landing pad -- planted, never stepped"),
+ ]
+ SD_OREAD = [                            # arm O: three SDRAM_BA_OFFSET reads
+     _w(0x2c, _ldr4("r7", 4), "r7 <- sentinel"),
+     _w(0x30, _ldr4("r8", 4), "r8 <- sentinel"),
+     _w(0x34, _ldr4("r9", 4), "r9 <- sentinel"),
+     _w(0x38, _ldr("r7", 0x104), "O: SDRAM_BA_OFFSET read #1 -> 0, announced (snap_at)"),
+     _w(0x3c, _ldr("r8", 0x104), "O: read #2 -> 0, silent"),
+     _w(0x40, _ldr("r9", 0x104), "O: read #3 -> 0, silent"),
+     (0x44, NOP, NOPTXT, "landing pad -- planted, never stepped"),
+ ]
+ SD_MIX = [                              # arm X: mask, mask, offset, offset
+     _w(0x2c, _ldr4("r7", 4), "r7 <- sentinel"),
+     _w(0x30, _ldr4("r8", 4), "r8 <- sentinel"),
+     _w(0x34, _ldr4("r9", 4), "r9 <- sentinel"),
+     _w(0x38, _ldr4("sl", 4), "sl <- sentinel"),
+     _w(0x3c, _ldr("r7", 0x100), "X: mask read #1 -> announced (snap_at)"),
+     _w(0x40, _ldr("r8", 0x100), "X: mask read #2 -> silent"),
+     _w(0x44, _ldr("r9", 0x104), "X: offset read #1 -> announced: its OWN latch"),
+     _w(0x48, _ldr("sl", 0x104), "X: offset read #2 -> silent"),
+     (0x4c, NOP, NOPTXT, "landing pad -- planted, never stepped"),
+ ]
+ SD_WRITES = [                           # arm W: writes only
+     _w(0x2c, _ldr4("r7", 16), "r7 <- 0x01FC0000"),
+     _w(0x30, _ldr4("r8", 32), "r8 <- 0"),
+     _w(0x34, _ldr4("r9", 24), "r9 <- 0x00040000"),
+     _w(0x38, _str("r7", 0x100), "W: mask <- 0x01FC0000 (whitelisted: silent) (snap_at)"),
+     _w(0x3c, _str("r2", 0x100), "W: mask <- 0x12345678 (not in Table 7-7: the write arm announces)"),
+     _w(0x40, _str("r8", 0x104), "W: offset <- 0 (not announced)"),
+     _w(0x44, _str("r9", 0x104), "W: offset <- 0x00040000 (the write arm announces)"),
+     (0x48, NOP, NOPTXT, "landing pad -- planted, never stepped"),
+ ]
+ SD_BACK = [                             # arm B: write, read, write again
+     _w(0x2c, _ldr4("r9", 20), "r9 <- 0x03FC0000"),
+     _w(0x30, _ldr4("sl", 24), "sl <- 0x00040000"),
+     _w(0x34, _ldr4("fp", 28), "fp <- 0x00080000"),
+     _w(0x38, _ldr4("r7", 4), "r7 <- sentinel"),
+     _w(0x3c, _ldr4("r8", 4), "r8 <- sentinel"),
+     _w(0x40, _str("r9", 0x100), "B: mask <- 0x03FC0000 (whitelisted; a backing edit keeps it) (snap_at)"),
+     _w(0x44, _str("sl", 0x104), "B: offset <- 0x00040000 (announced by the write arm)"),
+     _w(0x48, _ldr("r7", 0x100), "B1: mask read -> 0, not 0x03FC0000; announced"),
+     _w(0x4c, _ldr("r8", 0x104), "B2: offset read -> 0, not 0x00040000; announced"),
+     _w(0x50, _str("r2", 0x100), "B3: mask <- 0x12345678, read latch SET: still the write arm's announce"),
+     _w(0x54, _str("fp", 0x104), "B3: offset <- 0x00080000, read latch SET: still the write arm's announce"),
+     (0x58, NOP, NOPTXT, "landing pad -- planted, never stepped"),
+ ]
+ SD_MMUON = [                            # arm U: arm M's reads with the boot MMU LEFT ON
+     _w(0x2c, _ldr4("r7", 4), "r7 <- sentinel"),
+     _w(0x30, _ldr4("r9", 4), "r9 <- sentinel"),
+     _w(0x34, _ldr("r7", 0x100), "U: VA 0x42000100 -> PA 0x02000100, zero fill, never the device (snap_at)"),
+     _w(0x38, _ldr("r9", 0x104), "U: VA 0x42000104 -> PA 0x02000104"),
+     (0x3c, NOP, NOPTXT, "landing pad -- planted, never stepped"),
+ ]
@@ replace  first side line 293 (1 lines) -> second side line 430 (12 lines)
- def run_arm(label, prog, emul="cats", quit_leg=False):
+ def parse_regs(seg):
+     """#585 (fbsdrampair): run_arm's own `reg` parse, as a function, for the snapshot taken before an
+     arm's first SDRAM access."""
+     regs = {}
+     for n in (0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14):
+         mm = re.search(r"\b%s\s*=\s*0x([0-9a-fA-F]+)" % REGNAME.get(n, "r%d" % n), seg)
+         if mm:
+             regs[n] = int(mm.group(1), 16)
+     return regs
+ 
+ 
+ def run_arm(label, prog, emul="cats", quit_leg=False, snap_at=None, data=()):
@@ replace  first side line 297 (1 lines) -> second side line 445 (4 lines)
-     BEFORE teardown."""
+     BEFORE teardown.  #585 (fbsdrampair): `data` plants extra (address, word) RAM operands, and
+     `snap_at` takes a `reg` just BEFORE the word at that offset is stepped (returned as "pre"), so
+     an arm's controls are measured even on a build that ends the process at that word.  With the
+     defaults the six older arms' sessions are exactly what they were."""
@@ insert  first side line 355 (0 lines) -> second side line 506 (1 lines)
+     pre = {}                       # #585: the registers just before `snap_at` is stepped
@@ insert  first side line 366 (0 lines) -> second side line 518 (2 lines)
+         for addr, dword in data:
+             send("put w 0x%08x, 0x%08x" % (addr, dword))
@@ insert  first side line 371 (0 lines) -> second side line 525 (7 lines)
+             if off == snap_at:
+                 mark = len(buf)
+                 if send("reg", timeout=30) and not dead[0]:
+                     pre = parse_regs(buf[mark:])
+                 else:
+                     status = "HOST-DIED" if dead[0] else "NO-REG"
+                     break
@@ replace  first side line 460 (1 lines) -> second side line 621 (1 lines)
-             "prompt": "GXemul>" in buf}
+             "prompt": "GXemul>" in buf, "pre": pre}
@@ insert  first side line 484 (0 lines) -> second side line 645 (7 lines)
+ #  #585 (fbsdrampair): snap_at = each arm's first SDRAM access.
+ SM = run_arm("M  sdram mask x3      (fbsdram)", MMU_OFF + BODY + SD_MREAD, snap_at=0x38, data=SD_DATA)
+ SO = run_arm("O  sdram offset x3    (fbsdram)", MMU_OFF + BODY + SD_OREAD, snap_at=0x38, data=SD_DATA)
+ SX = run_arm("X  sdram mask+offset  (fbsdram)", MMU_OFF + BODY + SD_MIX, snap_at=0x3c, data=SD_DATA)
+ SW = run_arm("W  sdram writes only  (fbsdram)", MMU_OFF + BODY + SD_WRITES, snap_at=0x38, data=SD_DATA)
+ SB = run_arm("B  sdram write/read/write (fbsdram)", MMU_OFF + BODY + SD_BACK, snap_at=0x40, data=SD_DATA)
+ SU = run_arm("U  sdram reads, MMU ON (fbsdram)", MMU_NOP + BODY + SD_MMUON, snap_at=0x34, data=SD_DATA)
@@ replace  first side line 636 (1 lines) -> second side line 804 (107 lines)
- nbad = sum(len(a["badis"]) for a in (L, T, E, S, QL))
+ #  ---- #585 (fbsdrampair): the SDRAM reads are DECLINED with 0 and announced once per register.  Each
+ #  control (xC) is the `reg` taken BEFORE the arm's first SDRAM access, so it holds on a build that ends
+ #  the process there; every other row reads one channel -- survival, a value, or the arm's diagnostics.
+ def sd_seen(fatals):
+     """Bracketed footbridge diagnostics, named, in arrival order (`other` = none of SD_NAMES)."""
+     return ",".join(SD_NAMES.get(f, "other") for f in fatals) or "-"
+ 
+ 
+ def sd_alive(a):
+     return a["status"] == "SURVIVED" and a["exit"] == 0 and a["signal"] is None
+ 
+ 
+ def sd_row(tag, note, ok, shown):
+     print("%-4s %-40s %-30s %s" % (tag, note, shown, "ok" if ok else "FAIL"))
+     return ok
+ 
+ 
+ def sd_ctrl(tag, note, a, mmu, want):
+     """The prologue ran and the operands are what the rows assume: CP15 c1 bit 0 == `mmu`, the RAM
+     liveness word and every (register, value) in `want`; MMU off also needs the device signature
+     (r6 = 0x1011), MMU on needs r6 PRESENT and NOT 0x1011 (C4's trap guard)."""
+     p = a["pre"]
+     sig = p.get(6) == 0x1011 if mmu == 0 else (6 in p and p[6] != 0x1011)
+     nops = sum(1 for r, v in want if p.get(r) == v)
+     ok = 3 in p and (p[3] & 1) == mmu and p.get(5) == 0x11223344 and sig and nops == len(want)
+     return sd_row(tag, note, ok, "mmu=%s r6=%s ops=%d/%d"
+                   % ((p[3] & 1) if 3 in p else "-", hexs(p.get(6)), nops, len(want)))
+ 
+ 
+ def sd_vals(tag, note, a, want):
+     """Each (register, value) in `want`, from the post-run `reg` (a missing key is red)."""
+     r = a["regs"]
+     return sd_row(tag, note, all(r.get(n) == v for n, v in want),
+                   " ".join("%s=%s" % (REGNAME.get(n, "r%d" % n), hexs(r.get(n))) for n, _v in want))
+ 
+ 
+ #  M: three SDRAM_BA_MASK reads.  M1 kills the exit reinstated at +0x100 (or kept after the announce):
+ #  survival.  M2 kills a nonzero declined value, inside or outside the latch: each read's value, into a
+ #  destination that held 0x12345678.  M3 kills the announce unlatched (3 lines), never made, misnamed,
+ #  or HEAD's exit text kept: the arm's diagnostics must be exactly [mask announce].
+ mc = sd_ctrl("MC", "arm M prologue + sentinels (pre-read)", SM, 0,
+              [(1, 0x00345678), (7, SD_SENT), (8, SD_SENT), (9, SD_SENT)])
+ results.append(mc)
+ results.append(sd_row("M1", "3 SDRAM_BA_MASK reads survived, exit 0", sd_alive(SM),
+                       "status=%s exit=%s" % (SM["status"], SM["exit"])))
+ results.append(sd_vals("M2", "each SDRAM_BA_MASK read returns 0", SM, [(7, 0), (8, 0), (9, 0)]))
+ results.append(sd_row("M3", "mask read announced ONCE over 3 reads", SM["fatals"] == [SD_MASK],
+                       "seen=%s" % sd_seen(SM["fatals"])))
+ #  O: the same at +0x104.  O2 kills a nonzero declined value there; an early return is EQUIVALENT
+ #  (memory_rw.c's #95 pre-zero and a 0 decline), so no row here or in M can see one.
+ oc = sd_ctrl("OC", "arm O prologue + sentinels (pre-read)", SO, 0,
+              [(1, 0x00345678), (7, SD_SENT), (8, SD_SENT), (9, SD_SENT)])
+ results.append(oc)
+ results.append(sd_row("O1", "3 SDRAM_BA_OFFSET reads survived, exit 0", sd_alive(SO),
+                       "status=%s exit=%s" % (SO["status"], SO["exit"])))
+ results.append(sd_vals("O2", "each SDRAM_BA_OFFSET read returns 0", SO, [(7, 0), (8, 0), (9, 0)]))
+ results.append(sd_row("O3", "offset read announced ONCE over 3 reads", SO["fatals"] == [SD_OFFSET],
+                       "seen=%s" % sd_seen(SO["fatals"])))
+ #  X: mask, mask, offset, offset in ONE process -- a latch SHARED between the two (the second register
+ #  never announces) or one arm setting the other's latch reds X1.  Order is checked too: the announces
+ #  must arrive mask first.
+ xc = sd_ctrl("XC", "arm X prologue + sentinels (pre-read)", SX, 0,
+              [(1, 0x00345678), (7, SD_SENT), (8, SD_SENT), (9, SD_SENT), (10, SD_SENT)])
+ results.append(xc)
+ results.append(sd_row("X1", "one announce per register, mask first", SX["fatals"] == [SD_MASK, SD_OFFSET],
+                       "order=%s" % sd_seen(SX["fatals"])))
+ #  W: writes only.  W1 kills a write taking the read path (the predicate inverted, made always true,
+ #  or its operand swapped for the latch): a read announce appears.  W2 pins HEAD's write arms -- no
+ #  announce for 0x01FC0000 or 0, one each for 0x12345678 and 0x40000 -- and changes legitimately when
+ #  the write side (`fbsdramwrites`, filed) lands.
+ wc = sd_ctrl("WC", "arm W prologue + operands (pre-write)", SW, 0,
+              [(1, 0x00345678), (2, SD_SENT), (7, 0x01FC0000), (8, 0), (9, 0x00040000)])
+ results.append(wc)
+ results.append(sd_row("W1", "writes: alive, exit 0, no read announce",
+                       sd_alive(SW) and SD_MASK not in SW["fatals"] and SD_OFFSET not in SW["fatals"],
+                       "status=%s seen=%s" % (SW["status"], sd_seen(SW["fatals"]))))
+ w_ann = [f for f in SW["fatals"] if f.startswith("[ footbridge write to sdram_ba_")]
+ results.append(sd_row("W2", "write announces exactly wmask, woff4", w_ann == [SD_WMASK, SD_WOFF4],
+                       "writes=%s" % sd_seen(w_ann)))
+ #  B: write, read, write.  B1/B2 kill a written value kept and returned (0x03FC0000 / 0x40000 back) and
+ #  the write path setting the read latch (the read then announces nothing).  B3 kills a write taken
+ #  into the read path once the read latch is SET (`|| latch`, an inverted or always-true predicate):
+ #  both after-the-read writes must still print the write arm's own announce.
+ bc = sd_ctrl("BC", "arm B prologue + operands (pre-write)", SB, 0,
+              [(1, 0x00345678), (2, SD_SENT), (7, SD_SENT), (8, SD_SENT), (9, 0x03FC0000),
+               (10, 0x00040000), (11, 0x00080000)])
+ results.append(bc)
+ results.append(sd_row("B1", "mask read after a write: 0, once",
+                       SB["regs"].get(7) == 0 and SB["fatals"].count(SD_MASK) == 1,
+                       "r7=%s mask=%d" % (hexs(SB["regs"].get(7)), SB["fatals"].count(SD_MASK))))
+ results.append(sd_row("B2", "offset read after a write: 0, once",
+                       SB["regs"].get(8) == 0 and SB["fatals"].count(SD_OFFSET) == 1,
+                       "r8=%s offset=%d" % (hexs(SB["regs"].get(8)), SB["fatals"].count(SD_OFFSET))))
+ results.append(sd_row("B3", "writes after the reads still announce",
+                       SB["fatals"].count(SD_WMASK) == 1 and SB["fatals"].count(SD_WOFF8) == 1,
+                       "seen=%s" % sd_seen(SB["fatals"])))
+ #  U: arm M's reads with the boot MMU LEFT ON -- a CONTROL.  It never reaches the device, so no product
+ #  edit can red it; it shows that M/O/X/B's deaths and announces come from PA 0x42000100/104.
+ uc = sd_ctrl("UC", "arm U: MMU ON, cannot see the device", SU, 1, [(7, SD_SENT), (9, SD_SENT)])
+ results.append(uc)
+ u1 = sd_row("U1", "MMU-on SDRAM reads: alive, no diagnostic",
+             sd_alive(SU) and not SU["fatals"] and SU["regs"].get(7) == 0 and SU["regs"].get(9) == 0,
+             "status=%s seen=%s r7=%s r9=%s" % (SU["status"], sd_seen(SU["fatals"]),
+                                               hexs(SU["regs"].get(7)), hexs(SU["regs"].get(9))))
+ results.append(u1)
+ 
+ nbad = sum(len(a["badis"]) for a in (L, T, E, S, QL, SM, SO, SX, SW, SB, SU))
@@ replace  first side line 645 (1 lines) -> second side line 919 (2 lines)
- ctrl_ok = c1 and c2 and c3 and c4 and c5 and ec1 and ea1 and sc1 and sa1
+ ctrl_ok = (c1 and c2 and c3 and c4 and c5 and ec1 and ea1 and sc1 and sa1
+            and mc and oc and xc and wc and bc and uc and u1)      # #585: the six SDRAM arms' controls
@@ replace  first side line 650 (1 lines) -> second side line 925 (1 lines)
- print("PROBE_WALL=%.1fs for 6 cold-debugger arms" % (time.time() - t0))
+ print("PROBE_WALL=%.1fs for 12 cold-debugger arms" % (time.time() - t0))
```
