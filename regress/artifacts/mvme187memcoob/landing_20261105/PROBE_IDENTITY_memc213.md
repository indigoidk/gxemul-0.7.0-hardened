# PROBE_IDENTITY_memc213.md -- the staged regress/mvme187_memc_probe.py and the instrument table 6 measured

Built by the landing kit's build_staged_memc.py at HEAD edb3213f.  Working copy 60999 bytes md5 a42e90991b58346c60bfbaf64802a7fc; staged 61011 bytes md5 cd3e95ca72a75b4225062b5207559cc0; table 6's frozen instrument (`regress/artifacts/mvme187memcoob/r7_20261105/table6/probe213_frozen.py`) md5 1d69cc4e6cb1499894fdf1fcbe3049bd.

* `ast.dump` with the module docstring dropped, every string kept: staged == working copy: **True**.
* `ast.dump` with the module docstring dropped and every string constant replaced by 'S' (the method of `regress/artifacts/mvme187memcoob/r6_20261105/textonly_check.py`, check 1): staged == table6/probe213_frozen.py: **True** -- so every session, instruction word, seed, want, function body and non-string constant is the instrument table 6 measured; the printed text differs where repair 6's pass-2 record fix says (`regress/artifacts/mvme187memcoob/p6_20261105/DISPOSITION.md`, record 1; `r7_20261105/TEXTONLY_PROOF_p6rec.out`).
* `py_compile`: run by the pretest.

Edits staged on top of the working copy, docstring only: 4 hunk(s) -- `#NNN` set to #581 (derived: max round heading in HEAD's CHANGELOG.md (#580) + 1); and 4 score-shaped string(s) N/206 put in words ("N of 206"), because section U (`tools/pipeline/check_score_claims.py`) reads every N/M in a gated probe's docstring as a claim against the gate pin, 213, and these quote table 5's 206-row instrument.

```
@@ line 8
- THE FIX (#NNN).  Each served offset reads its own field (chipid +0x00, chiprev +0x04, memconf +0x08); controller 1 (+0x100..0x1ff)
+ THE FIX (#581).  Each served offset reads its own field (chipid +0x00, chiprev +0x04, memconf +0x08); controller 1 (+0x100..0x1ff)
@@ line 46
- L_DA_D_xori_any, L_MT_M_xori_M, L_MW_M_xori_M, L_DT_D_xori_D and L_DT_D_idat_W.D: 206/206 each in table 5 (r5_20261105/table5/
+ L_DA_D_xori_any, L_MT_M_xori_M, L_MW_M_xori_M, L_DT_D_xori_D and L_DT_D_idat_W.D: 206 of 206 each in table 5 (r5_20261105/table5/
@@ line 81
- L_ME_M_idat_nC 201/206 against :2999 L_ME_M_idat_W.nC 206/206) -- whose clearing stores -- the 0x00 controller-0 stores of R3, R7,
+ L_ME_M_idat_nC 201 of 206 against :2999 L_ME_M_idat_W.nC 206 of 206) -- whose clearing stores -- the 0x00 controller-0 stores of R3, R7,
@@ line 115
- table-4 variant red again; 3,518 variants PRED=match, 56 PRED=atleast-ok, one PRED=MISS (D7_fold, detected 175/206: a stale
+ table-4 variant red again; 3,518 variants PRED=match, 56 PRED=atleast-ok, one PRED=MISS (D7_fold, detected 175 of 206: a stale
```
