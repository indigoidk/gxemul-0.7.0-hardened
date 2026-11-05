# PROBE_IDENTITY_pvr.md -- the staged regress/pvr_zwrite_probe.py and the instrument table 5 measured

Built by the landing kit's build_staged_pvr.py at HEAD cbd916d1; lands as `regress/artifacts/pvrrenderexit/landing_20261105/PROBE_IDENTITY_pvr.md`.  Working copy 76090 bytes md5 ac6b07a8dffc22981051b96b2b8979cb (the probe `r6_20261105/AST_PROOF_p7.txt` names as shipped: True); staged 76129 bytes md5 628c1c58eee2f1e53b90391a0b6ecb74; table 5's frozen instrument (`regress/artifacts/pvrrenderexit/r5_20261105/table5/probe148_frozen.py`) md5 84fe7386d80139de97ec7026bbe23e7f.

* `ast.dump` with the module docstring dropped, every string kept: staged == working copy: **True**.
* `ast.dump` with the module docstring dropped, every string kept: staged == table5/probe148_frozen.py: **True** -- so every session, store, vertex, want, row name and row note is the instrument table 5 measured, and table 5's banked logs are what the staged probe prints (the method of `regress/artifacts/pvrrenderexit/r6_20261105/ast_same.py`, which found the same of the working copy).
* The staged source compiles (`compile()` in process).  Its 148 `row()` names, in order, are the staged gate block's 148 names and the 148 rows of table 5's base log (`table5/probe_base.out`): True.
* Section U (`tools/pipeline/check_score_claims.py`'s docstring reading against the 148-row pin): the working copy has 10 stale claim(s) (0/68, 1/68, 60/128, 9/128, 0/128, 1/128, 66/140, 9/140, 0/140, 1/140); the staged copy has 0.

Edits staged on top of the working copy, all in the module docstring: `THE FIX (#NNN).` -> `THE FIX (#581).` (derived: max round heading in HEAD's CHANGELOG.md (#580) + 1), and the history paragraph's thirteen scores of the 68-, 128- and 140-row instruments in words -- the ten section U reads as stale claims against the 148-row pin plus the three era-marked ones in the same sentences, so each sentence reads one way.  3 hunk(s):

```
@@ line 8
- THE FIX (#NNN).  Such a polygon goes through the same depth test and rasterization as any other polygon, and only its depth store
+ THE FIX (#581).  Such a polygon goes through the same depth test and rasterization as any other polygon, and only its depth store
@@ line 230
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
@@ line 237
- null media 9/140, 0/140 and 1/140 (r4_20261105/table4/SCORES.txt).  This 148-row probe (repair 5): the fix 148/148 in ~2 s with
+ null media 9 of 140, 0 of 140 and 1 of 140 (r4_20261105/table4/SCORES.txt).  This 148-row probe (repair 5): the fix 148/148 in ~2 s with
```
