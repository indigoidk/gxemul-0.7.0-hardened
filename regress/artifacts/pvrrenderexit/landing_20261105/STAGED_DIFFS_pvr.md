# STAGED_DIFFS_pvr.md -- what the pvrrenderexit landing commits for each shared file, against HEAD and the working copy

HEAD cbd916d1.  Round number #581 (derived: max round heading in HEAD's CHANGELOG.md (#580) + 1).  Built by the landing kit's build_staged_pvr.py from `git show HEAD:<path>`, the working copy and `regress/artifacts/pvrrenderexit/r5_20261105/gate_pvr_block.new`, at 2026-11-05 08:01 local.  This record lands as `regress/artifacts/pvrrenderexit/landing_20261105/STAGED_DIFFS_pvr.md`.

## src/devices/dev_pvr.c (staged = the working copy with its six `#NNN` comment tags set to #581)

HEAD 77407 bytes md5 6af38de7eef85e602136c1768cb1b56d (== `regress/artifacts/pvrrenderexit/det_20261104/dev_pvr.c.HEAD`, the pre-fix source of every table's HEAD leg).  Working copy 78268 bytes md5 481755b4f10fc67a8749884a90594ff9 (== `regress/artifacts/pvrrenderexit/r5_20261105/dev_pvr.c.fix5`, the source table 5 measured: table5/MD5.txt).  Staged 78268 bytes md5 be26d31e9f5a4746bb9dace6f6829a70.

Every working-tree hunk is this round's: 5 hunks, 19 lines added and 6 removed (`git diff --stat`: 19 insertions, 6 deletions), each inside one of the four constructs the round edits (HEAD's lines: pvr_render() 1077-1427; simpleline() 650-718; struct pvr_data 96-151; texturedline() 720-898), each adding `zwrite_disabled` or the comment carrying its `#NNN` tag, and the only removed lines the two unguarded `vram_z` stores and the four-line `if (!zwrite) { fatal(...); exit(1); }`:

* HEAD line 147: 0 line(s) -> 4 line(s), inside struct pvr_data
* HEAD line 683: 1 line(s) -> 2 line(s), inside simpleline()
* HEAD line 767: 1 line(s) -> 2 line(s), inside texturedline()
* HEAD line 1131: 0 line(s) -> 4 line(s), inside pvr_render()
* HEAD line 1243: 4 line(s) -> 7 line(s), inside pvr_render()

### the working copy vs HEAD (the round's whole change; the staged file differs from it only in the six tags below)

5 hunk(s):

```
@@ insert  first side line 147 (0 lines) -> second side line 147 (4 lines)
+     int            zwrite_disabled;    /*  #NNN: ISP/TSP word 1 bit 26 of the
+                                 polygon being rendered.  When set, the
+                                 rasterizers skip their vram_z stores.
+                                 Cleared at every pvr_render entry.  */
@@ replace  first side line 683 (1 lines) -> second side line 687 (2 lines)
-                 d->vram_z[ofs] = z;
+                 if (!d->zwrite_disabled)    /*  #NNN: depth test kept, store skipped  */
+                     d->vram_z[ofs] = z;
@@ replace  first side line 767 (1 lines) -> second side line 772 (2 lines)
-                 d->vram_z[ofs] = z;
+                 if (!d->zwrite_disabled)    /*  #NNN: depth test kept, store skipped  */
+                     d->vram_z[ofs] = z;
@@ insert  first side line 1131 (0 lines) -> second side line 1137 (4 lines)
+     d->zwrite_disabled = 0;    /*  #NNN: per render.  A type-4 header in this
+                     call assigns it; a list with no header must
+                     not inherit the previous render's value.  */
+ 
@@ replace  first side line 1243 (4 lines) -> second side line 1253 (7 lines)
-             if (!zwrite) {
-                 fatal("pvr: no zwrite? not implemented yet.\n");
-                 exit(1);
-             }
+             /*  #NNN: ISP/TSP instruction word 1 bit 26 is "Z-write disable".
+                 A polygon with the bit set goes through the same depth test
+                 and rasterization as any other polygon, but its depth values
+                 are not stored.  Both rasterizers check d->zwrite_disabled
+                 at their vram_z stores.  Before #NNN this bit ended the
+                 emulator with fatal() + exit(1).  */
+             d->zwrite_disabled = !zwrite;
```

### the fill (staged vs the working copy)

Six `#NNN` -> `#581`, each inside a C comment (kit_pvr.fill_c asserts it), same width, so no line moves; comment-free forms equal: True.  The round number is HEAD-relative (derived: max round heading in HEAD's CHANGELOG.md (#580) + 1) and is re-derived whenever this builder runs.

```
line 147: int            zwrite_disabled;    /*  #581: ISP/TSP word 1 bit 26 of the
line 687: if (!d->zwrite_disabled)    /*  #581: depth test kept, store skipped  */
line 772: if (!d->zwrite_disabled)    /*  #581: depth test kept, store skipped  */
line 1137: d->zwrite_disabled = 0;    /*  #581: per render.  A type-4 header in this
line 1253: /*  #581: ISP/TSP instruction word 1 bit 26 is "Z-write disable".
line 1257: at their vram_z stores.  Before #581 this bit ended the
```

### the four trees (TREES_pvr.txt)

```
est                                      part 1 PASS (== the SEC working copy, md5 481755b4f10f); part 2 N/A (source tree, no binary); sentinels none (.MUTANT, .LANDING*)
                                           vs HEAD: the round's five hunks (== the working copy's); vs staged: 6 hunk(s) = the six #NNN fills only
build                                    part 1 PASS (== the SEC working copy, md5 481755b4f10f); part 2 PASS: binary newer (gxemul 11-05 01:33:18, dev_pvr.c 11-04 13:44:51); sentinels none (.MUTANT, .LANDING*)
                                           vs HEAD: the round's five hunks (== the working copy's); vs staged: 6 hunk(s) = the six #NNN fills only
build-asan                               part 1 PASS (== the SEC working copy, md5 481755b4f10f); part 2 PASS: binary newer (gxemul 11-05 01:35:37, dev_pvr.c 11-04 13:44:51); sentinels none (.MUTANT, .LANDING*)
                                           vs HEAD: the round's five hunks (== the working copy's); vs staged: 6 hunk(s) = the six #NNN fills only
//wsl.localhost/Gentoo/tmp/gxsec-build   part 1 PASS (== the SEC working copy, md5 481755b4f10f); part 2 PASS: binary newer (gxemul 11-05 01:36:12, dev_pvr.c 11-04 13:44:51); sentinels none (.MUTANT, .LANDING*)
                                           vs HEAD: the round's five hunks (== the working copy's); vs staged: 6 hunk(s) = the six #NNN fills only
TREES_SUMMARY ATTRIBUTED; TREES ALL CLEAR AGAINST THE WORKING COPY (part 1 and part 2); TREE UPDATE OWED IN THE LANDING WINDOW: the staged dev_pvr.c fills six #NNN comment tags, so est/, build/, build-asan/ and WSL /tmp/gxsec-build must take the staged file and the three build trees rebuild (both clearance parts re-run against it) before the commit's section A/B can pass
```

## regress/gate_arm.sh

HEAD 155139 bytes md5 ce5da7331a993a3d92162255a57af751; staged 161356 bytes md5 66739ac1c2ce4cd25be95ae4137ba847; working copy 166210 bytes md5 79474569408581ff6eba5fda5bdb7125 (READ only).  The staged block is `regress/artifacts/pvrrenderexit/r5_20261105/gate_pvr_block.new` (md5 ee043615bb81619618a82bdad55a7948, 42 lines + two blank, the four counts 148, 148 distinct row names) with its header's `(#NNN)` set to `(#581)`, inserted directly before `hpcmipsctor (#444) + #536`; in HEAD it follows the block headed `m88kbuserrregs (#570)`.  The working copy's own pvr block (30 lines, pin 68) is NOT used.  `bash -n` on the staged file: clean.  Section U's comment-line reading of the staged file for the stem pvr_zwrite: no stale claim.

### staged vs HEAD (the commit's whole diff of this file: the 148-row block and its two blank lines)

1 hunk(s):

```
@@ insert  first side line 2063 (0 lines) -> second side line 2063 (44 lines)
+ #  ------------------------------------------------------------ pvrrenderexit (#581)
+ #  dev_pvr.c's renderer ended the emulator (fatal() + exit(1)) on a polygon header whose list word 1 sets bit 26 (Z-write disable).
+ #  Now such a polygon goes through the same depth test and rasterization as any other and only its depth store is skipped, in both
+ #  rasterizers, and every render clears the flag first.  The rung-3 witness (regress/artifacts/pvrrenderexit/witness_20261104/) is
+ #  NOT run here; this is its detector: 148 rows -- the witness's nine plus fifty render sessions whose pixels are read back
+ #  through the linear VRAM window (the depth-test cells of both rasterizers, two renders in one session, the x-range bound at both
+ #  screen edges, the equal-depth edge, repair 2's y range, span end and start, swap and bit-26 decode neighbours, repair 3's class
+ #  closure -- the swap's other edges and body, reversed spans across both edges, the left clause's compares at their edge, a Z-off
+ #  polygon at equal depth, the decode's `== 1` and wider masks, and a Z-OFF TWIN of every single-layer geometry session and of the
+ #  swap-body session -- repair 4's half-pixel edges of simpleline's position compares and the swap body's far end, and repair 5's
+ #  swap body read from above and span starts at a negative x, each with its Z-off twin).  Needs only the binary: -E dreamcast with
+ #  a 4-byte dummy image at 0x8c010000, about two seconds (r5_20261105/base148f/: 2.2 s).  (Corrected 2026-11-05, repair 3: this
+ #  said 'fifteen render sessions' -- repair 2 made sixteen -- and 'about half a second', which held for the 51-row probe; the
+ #  68-row probe took ~90 s, because one session's input passed the 4100-byte debugger stdin cap and waited out its timeout --
+ #  r3_20261105/PVR3_NOTE.md.  The probe now refuses such a session before running anything.)  It sits here rather than in
+ #  gate_sh_rounding.sh with the other dreamcast probes only because that file carried another session's uncommitted work when it
+ #  landed.  Test-variant tables: regress/artifacts/pvrrenderexit/det_20261104/table1/ (the 51-row probe), r2_20261105/table2/ (the
+ #  68-row probe), r3_20261105/table3/ (the 128-row probe: 129 of its 130 predictions hit; the miss was a Z-off twin left out of one
+ #  prediction, r3_20261105/PRETABLE_3.errata.md), r4_20261105/table4/ (the 140-row probe: all 148 of its predictions hit -- B2t's
+ #  "EQUIVALENT" struck by r4_20261105/PRETABLE_4.errata.md) and r5_20261105/table5/ (this probe: all 192 of PRETABLE_5.out's
+ #  predictions hit -- 186 variants and six legs; four undefined-behaviour variants unpredicted, thirteen non-finite forms excluded).
+ #  (Corrected 2026-11-05, repair 4 -- codex pass 4, F2: this said table 3 was 'prepared, not yet run'.)  Like the blocks above, it
+ #  runs only if none of this gate's earlier skip points fired.
+ PVRLOG=$LOGDIR/pvr_zwrite.log
+ python3 -u pvr_zwrite_probe.py "$PMAX" gate > "$PVRLOG" 2>&1 || true
+ if ! grep -q "PVR_ZWRITE_PROBE_DONE" "$PVRLOG"; then
+     check "pvr zwrite probe completed" "no" "yes"
+ else
+     check "pvr zwrite probe completed" "yes" "yes"
+     check "pvr zwrite sentinel once" "$(grep -c '^PVR_ZWRITE_PROBE_DONE$' "$PVRLOG")" "1"
+     pzres=$(sed -n 's/^PVR_ZWRITE_RESULT=//p' "$PVRLOG")
+     check "pvr_zwrite rows run"     "${pzres#*/}" 148
+     check "pvr_zwrite rows correct" "${pzres%/*}" "148"
+     check "pvr zwrite controls" "$(grep -c '^PVR_ZWRITE_CONTROL=OK$' "$PVRLOG")" "1"
+     check "pvr zwrite symptom absent" "$(grep -c '^PVR_ZWRITE_SYMPTOM=ABSENT$' "$PVRLOG")" "1"
+     for v in "neg apparatus" "id session" "id r8" "zon session" "zon rendered" "zon prompt" "zoff rendered" "zoff session" "zoff prompt" "ovoff session" "ovoff overlap" "ovoff t2 only" "ovoff t1 only" "ovoff bg" "ovon overlap" "ovon t2 only" "ovon t1 only" "ovon bg" "behind session" "behind overlap" "behind t2 only" "behind t1 only" "texoff session" "texoff overlap" "texoff t1 only" "texoff t2 only" "texbeh session" "texbeh overlap" "texbeh t2 only" "texbeh t1 only" "texon overlap" "texon t2 only" "two session" "two overlap" "two t1 only" "two t2 only" "sticky session" "sticky overlap" "sticky t2 only" "edges l in" "edges l out" "edges r in" "edges r out" "edges rspan" "texedges l in" "texedges l out" "texedges r in" "texedges r out" "texedges rspan" "equal overlap" "equal t2 only" "texequal overlap" "texequal t2 only" "yedges t in" "yedges b in" "yedges b out" "yedges swap" "yedges s end" "yedges s past" "texyedges t in" "texyedges b in" "texyedges b out" "texyedges swap" "texyedges s end" "texyedges s past" "mask overlap" "mask t2 only" "mask25 overlap" "swap s before" "swap s tip" "swap vert" "swap frac past" "swap s start" "texswap s before" "texswap s tip" "texswap vert" "ramp l end" "texramp l end" "edges2 l rev" "edges2 r rev" "edges2 l tip" "edges2 x2 tip" "texedges2 l rev" "texedges2 r rev" "texedges2 l tip" "texedges2 x2 tip" "zleft tip" "texzleft tip" "zeq overlap" "texzeq overlap" "maskoff overlap" "maskhi overlap" "zedges l in" "zedges l out" "zedges r in" "zedges r out" "zedges rspan" "zyedges t in" "zyedges b in" "zyedges b out" "zyedges swap" "zyedges s end" "zyedges s past" "zswap s before" "zswap s tip" "zswap vert" "zswap frac past" "zswap s start" "zedges2 l rev" "zedges2 r rev" "zedges2 l tip" "zramp l end" "ztedges l in" "ztedges l out" "ztedges r in" "ztedges r out" "ztedges rspan" "ztyedges t in" "ztyedges b in" "ztyedges b out" "ztyedges swap" "ztyedges s end" "ztyedges s past" "ztswap s before" "ztswap s tip" "ztswap vert" "ztedges2 l rev" "ztedges2 r rev" "ztedges2 l tip" "ztramp l end" "half swap" "half r x1" "half r x2" "zhalf swap" "zhalf r x1" "zhalf r x2" "ramp8 r end" "zramp8 r end" "texramp8 r end" "ztramp8 r end" "ramp8hi r end" "ramp8hi l end" "zramp8hi r end" "zramp8hi l end" "negx n start" "znegx n start" "texnegx n start" "ztnegx n start"; do
+         check "pvr zwrite row: $v" "$(count "$PVRLOG" "^$v  .*ok$")" "1"
+     done
+     check "pvr zwrite rows emitted" "$(( $(count "$PVRLOG" " ok$") + $(count "$PVRLOG" " FAIL$") ))" "148"
+     check "pvr zwrite rows green"   "$(count "$PVRLOG" " ok$")"   "148"
+     check "pvr zwrite rows red"     "$(count "$PVRLOG" " FAIL$")" "0"
+ fi
+ 
+ 
```

### staged vs the working copy

The pvr blocks differ in 5 hunk(s) (the staged 148-row block against the working copy's 68-row block, which the working tree has not taken; both sit directly before the hpcmipsctor header).  Outside the pvr block the staged file is HEAD's, and the working copy minus its pvr block differs from HEAD in 4 hunk(s), none carrying a pvr line:

* fbsdram's uncommitted footbridge-block edits: HEAD line 1083, replace (1 -> 1 lines; grep -E "^(  arm |C[0-9]|A[0-9]|I1|H[12]|D1|E(C1|A1|[0-6])|S(C1|A1|[1-5]|F[12])|)
* fbsdram's uncommitted footbridge-block edits: HEAD line 1126, replace (3 -> 4 lines; #  stand in for a missing id -- pass 2), and the probe's own total by ROWS= (37 )
* fbsdram's uncommitted footbridge-block edits: HEAD line 1165, insert (0 -> 22 lines; #  #NNN fbsdrampair: a guest READ of SDRAM_BA_MASK (+0x100) or SDRAM_BA_OFFSET ()
* memc (mvme187memcoob)'s uncommitted block: HEAD line 2063, insert (0 -> 34 lines; #  ------------------------------------------------------------ mvme187memcoob ()

## regress/pvr_zwrite_probe.py (new file; only this round's)

Staged = the working copy with 3 docstring hunk(s) (the number; thirteen scores in words).  PROBE_IDENTITY_pvr.md: tree minus docstring, every string kept, equal to the working copy's: True; equal to table 5's frozen instrument's: True; section U stale claims 10 -> 0.

### staged vs the working copy

3 hunk(s):

```
@@ replace  first side line 8 (1 lines) -> second side line 8 (1 lines)
- THE FIX (#NNN).  Such a polygon goes through the same depth test and rasterization as any other polygon, and only its depth store
+ THE FIX (#581).  Such a polygon goes through the same depth test and rasterization as any other polygon, and only its depth store
@@ replace  first side line 230 (6 lines) -> second side line 230 (6 lines)
- 68-row probe the pre-fix build scored 42 of the 68 rows with the symptom PRESENT, and three null media -- /bin/true 9/68, an absent
- binary 0/68, /bin/false 1/68 -- each CONTROL=FAIL (r2_20261105/table2/SCORES.txt).  The 128-row probe (repair 3): the fix 128/128
- in ~3 s with no session timed out, the pre-fix build 60/128 with the symptom PRESENT (r3_20261105/base128/, head128/: table 2's 26
- red rows plus every repair-3 row whose session carries a Z-off header, 42), and its null media 9/128, 0/128 and 1/128
- (r3_20261105/table3/SCORES.txt).  The 140-row probe (repair 4): the fix 140/140 in ~2 s with no session timed out (48 sessions),
- and the pre-fix build 66/140 with the symptom PRESENT (r4_20261105/base140/, head140/: the 128-row probe's 68 red rows plus the six
+ 68-row probe the pre-fix build scored 42 of the 68 rows with the symptom PRESENT, and three null media -- /bin/true 9 of 68, an absent
+ binary 0 of 68, /bin/false 1 of 68 -- each CONTROL=FAIL (r2_20261105/table2/SCORES.txt).  The 128-row probe (repair 3): the fix 128 of 128
+ in ~3 s with no session timed out, the pre-fix build 60 of 128 with the symptom PRESENT (r3_20261105/base128/, head128/: table 2's 26
+ red rows plus every repair-3 row whose session carries a Z-off header, 42), and its null media 9 of 128, 0 of 128 and 1 of 128
+ (r3_20261105/table3/SCORES.txt).  The 140-row probe (repair 4): the fix 140 of 140 in ~2 s with no session timed out (48 sessions),
+ and the pre-fix build 66 of 140 with the symptom PRESENT (r4_20261105/base140/, head140/: the 128-row probe's 68 red rows plus the six
@@ replace  first side line 237 (1 lines) -> second side line 237 (1 lines)
- null media 9/140, 0/140 and 1/140 (r4_20261105/table4/SCORES.txt).  This 148-row probe (repair 5): the fix 148/148 in ~2 s with
+ null media 9 of 140, 0 of 140 and 1 of 140 (r4_20261105/table4/SCORES.txt).  This 148-row probe (repair 5): the fix 148/148 in ~2 s with
```

## tools/precommit_check.sh

HEAD md5 0b5946e4bd0f2c4580a86b5682c3d3bf (SCORE_CLAIMS_MANIFEST=45); staged md5 3ae05bafa8cd141871d709517c74b2ba (=46).  Written fresh against HEAD: the working copy's raises -- qhslowifetch, mvme187memcoob (naming a stale 74-row pin), pvrrenderexit (naming a stale 51-row pin) -- are not carried.  `bash -n`: clean.  (tools/pipeline/check_probe_wiring.py's MANIFEST is built with the records, phase 2.)

### staged vs HEAD

1 hunk(s):

```
@@ replace  first side line 374 (1 lines) -> second side line 374 (3 lines)
-     SCORE_CLAIMS_MANIFEST=45
+     #  RAISED 45 -> 46 ON 2026-11-05, DELIBERATELY.  One newly gated probe: pvr_zwrite_probe.py
+     #  (#581 pvrrenderexit, pinned UNQUOTED in gate_arm.sh at 148 rows under the stem pvr_zwrite; its docstring is checked).
+     SCORE_CLAIMS_MANIFEST=46
```
