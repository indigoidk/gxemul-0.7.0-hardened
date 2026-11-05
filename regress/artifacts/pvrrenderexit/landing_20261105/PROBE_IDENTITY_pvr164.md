# PROBE_IDENTITY_pvr164.md -- the staged regress/pvr_zwrite_probe.py and the instrument table 7 measured

Built by the landing kit's build_staged_pvr.py at HEAD f58105b7; lands as `regress/artifacts/pvrrenderexit/landing_20261105/PROBE_IDENTITY_pvr164.md`.  Working copy 84104 bytes md5 e989843bcd0dc599ad279698787e858c (the probe `r7_20261105/AST_PROOF_r7.txt` names as shipped: True); staged 84158 bytes md5 c70b1d2fd8f7a343aaa53776994bc88f; table 7's frozen instrument (`regress/artifacts/pvrrenderexit/r7_20261105/table7/probe164_frozen.py`) md5 ebce4d7f4c91c837f64232ea03150dbd.

* `ast.dump` with the module docstring dropped, every string kept: staged == working copy: **True**.
* `ast.dump` with the module docstring dropped, every string kept: staged == table7/probe164_frozen.py: **True** -- so every session, store, vertex, want, row name and row note is the instrument table 7 measured, and table 7's banked logs are what the staged probe prints (the method of `regress/artifacts/pvrrenderexit/r6_20261105/ast_same.py`, which found the same of the working copy).
* The staged source compiles (`compile()` in process).  The 164 rows of table 7's base log (`table7/probe_base.out`), in order, are the staged gate block's 164 names: True; the source's 148 literal `row("...")` names are among them, and the other 16 (fbhi s px, fbhi t px, zfbhi s px, zfbhi t px, fbedge l tip, fbedge x2 tip, zfbedge l tip, zfbedge x2 tip, fbtedge l tip, fbtedge x2 tip, zfbtedge l tip, zfbtedge x2 tip, palcfg x2 tip, palcfg l tip, zpalcfg x2 tip, zpalcfg l tip) come from repair 7's loops.
* Section U (`tools/pipeline/check_score_claims.py`'s docstring reading against the 164-row pin): the working copy has 14 stale claim(s) (0/68, 1/68, 60/128, 9/128, 0/128, 1/128, 66/140, 9/140, 0/140, 1/140, 70/148, 9/148, 0/148, 1/148); the staged copy has 0.

Edits staged on top of the working copy, all in the module docstring: `THE FIX (#NNN).` -> `THE FIX (#583).` (derived: max round heading in HEAD's CHANGELOG.md (#582) + 1), and the history paragraph's eighteen scores of the 68-, 128-, 140- and 148-row instruments in words -- the fourteen section U reads as stale claims against the 164-row pin plus the four era-marked ones in the same sentences, so each sentence reads one way.  4 hunk(s):

```
@@ line 8
- THE FIX (#NNN).  Such a polygon goes through the same depth test and rasterization as any other polygon, and only its depth store
+ THE FIX (#583).  Such a polygon goes through the same depth test and rasterization as any other polygon, and only its depth store
@@ line 255
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
@@ line 262
- null media 9/140, 0/140 and 1/140 (r4_20261105/table4/SCORES.txt).  The 148-row probe (repair 5): the fix 148/148 in ~2 s with
- no session timed out (54 sessions), and the pre-fix build 70/148 with the symptom PRESENT (r5_20261105/base148/, head148/: the
+ null media 9 of 140, 0 of 140 and 1 of 140 (r4_20261105/table4/SCORES.txt).  The 148-row probe (repair 5): the fix 148 of 148 in ~2 s with
+ no session timed out (54 sessions), and the pre-fix build 70 of 148 with the symptom PRESENT (r5_20261105/base148/, head148/: the
@@ line 265
- `znegx n start`, `ztnegx n start`); its null media 9/148, 0/148 and 1/148, each CONTROL=FAIL
+ `znegx n start`, `ztnegx n start`); its null media 9 of 148, 0 of 148 and 1 of 148, each CONTROL=FAIL
```
