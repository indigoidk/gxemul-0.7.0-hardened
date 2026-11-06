# PROBE_IDENTITY_fbs.md -- the staged regress/footbridge_sites_probe.py and the instrument table 1 measured

Built by the landing kit's build_staged_fbs.py at HEAD ab39ba0d; lands as `regress/artifacts/fbsdrampair/landing_20261105/PROBE_IDENTITY_fbs.md`.  HEAD's probe 40104 bytes md5 9e9961de60fd50b23dbd96b19817167e (== `impl_20261105/footbridge_sites_probe.py.pre_fbs`, the probe before this round); working copy 59684 bytes md5 f29bd449a21ab23c005a43f799fb40ee; staged 59684 bytes md5 e0c4a48b9bf1889eb92714fc79269890; table 1's frozen instrument (`regress/artifacts/fbsdrampair/table1_20261105/probe56_frozen.py`) md5 a52267ff1856bc4127c2052a4b30f8e0.

* `ast.dump` with EVERY docstring removed (module and function docstrings; comments are never in the AST), every other string kept: staged == working copy: **True**.
* The same, staged == table1_20261105/probe56_frozen.py: **True** -- so every session, planted word, row name, row note and verdict line is the instrument table 1 measured, and table 1's banked logs are what the staged probe prints (the method of `p2_20261105/AST_PROOF.txt`, which found the same of the probe after pass 2's record fixes).  Against HEAD's probe: different, as it must be (the round's six arms and nineteen rows).
* The staged source compiles (`compile()` in process).  Table 1's base log (`table1_20261105/runs/probe_base.out`) prints 56 distinct rows and `ROWS=56 of 56`.
* Every `#NNN` sat inside a comment or a docstring (tokenize + ast, kit_fbs.py_tag_sites): line 52 docstring, line 53 docstring, line 176 docstring, line 178 docstring, line 240 docstring, line 347 comment, line 431 docstring, line 445 docstring, line 506 comment, line 645 comment, line 804 comment, line 920 comment.

Edits staged on top of the working copy: the twelve `#NNN` -> `#585` (derived: max round heading in HEAD's CHANGELOG.md (#584) + 1).  11 hunk(s):

```
@@ line 52
- writes) instead of dying, and #NNN declines the last two -- the SDRAM reads at +0x100/+0x104
- (`fbsdrampair`, arms M/O/X/W/B/U below; until #NNN this line said no arm here touched them) --
+ writes) instead of dying, and #585 declines the last two -- the SDRAM reads at +0x100/+0x104
+ (`fbsdrampair`, arms M/O/X/W/B/U below; until #585 this line said no arm here touched them) --
@@ line 176
- ARMS M, O, X, W, B, U (#NNN, `fbsdrampair`) -- the two SDRAM register READS, SDRAM_BA_MASK (+0x100)
+ ARMS M, O, X, W, B, U (#585, `fbsdrampair`) -- the two SDRAM register READS, SDRAM_BA_MASK (+0x100)
@@ line 178
- (DC21285 7.3.9, 7.3.10) and both write arms keep nothing, so #NNN DECLINES the read: odata stays 0
+ (DC21285 7.3.9, 7.3.10) and both write arms keep nothing, so #585 DECLINES the read: odata stays 0
@@ line 240
- COST, measured: see PROBE_WALL below -- 12 cold-debugger launches (#545: +S, +Q, +H; #NNN: +M, O, X,
+ COST, measured: see PROBE_WALL below -- 12 cold-debugger launches (#545: +S, +Q, +H; #585: +M, O, X,
@@ line 347
- #  #NNN (fbsdrampair): arms M, O, X, W, B, U.  Every SDRAM operand and every value-row destination's
+ #  #585 (fbsdrampair): arms M, O, X, W, B, U.  Every SDRAM operand and every value-row destination's
@@ line 431
-     """#NNN (fbsdrampair): run_arm's own `reg` parse, as a function, for the snapshot taken before an
+     """#585 (fbsdrampair): run_arm's own `reg` parse, as a function, for the snapshot taken before an
@@ line 445
-     BEFORE teardown.  #NNN (fbsdrampair): `data` plants extra (address, word) RAM operands, and
+     BEFORE teardown.  #585 (fbsdrampair): `data` plants extra (address, word) RAM operands, and
@@ line 506
-     pre = {}                       # #NNN: the registers just before `snap_at` is stepped
+     pre = {}                       # #585: the registers just before `snap_at` is stepped
@@ line 645
- #  #NNN (fbsdrampair): snap_at = each arm's first SDRAM access.
+ #  #585 (fbsdrampair): snap_at = each arm's first SDRAM access.
@@ line 804
- #  ---- #NNN (fbsdrampair): the SDRAM reads are DECLINED with 0 and announced once per register.  Each
+ #  ---- #585 (fbsdrampair): the SDRAM reads are DECLINED with 0 and announced once per register.  Each
@@ line 920
-            and mc and oc and xc and wc and bc and uc and u1)      # #NNN: the six SDRAM arms' controls
+            and mc and oc and xc and wc and bc and uc and u1)      # #585: the six SDRAM arms' controls
```
