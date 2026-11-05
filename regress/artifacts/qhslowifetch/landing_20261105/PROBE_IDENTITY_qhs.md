# PROBE_IDENTITY_qhs.md -- the staged regress/ppc_ifetch_probe.py is the working copy, which differs from the measured instrument in its docstring only

Built by build_staged_qhs.py at HEAD acdf8ce4, 2026-11-05 14:03:22 local.  Working copy 59820 bytes md5 345232855497e5af313e1c885cab4b8c; staged 59820 bytes md5 6a098d38c17e1e71a62b05fcea3b3d26; the copy before the coordinator's decision-3 docstring edit (`bk/ppc_ifetch_probe.py.pre_wtdoc`, after the regress review's R-B) md5 488394b7c6c2ceaf5eba36465a8b36ea; table 12's frozen instrument (`regress/artifacts/qhslowifetch/r7_20261105/table12/probe249_frozen.py`) md5 39c630216eaf595bece277e1080c9fbc.

* `ast.dump` with the module docstring dropped, EVERY STRING KEPT: staged == working copy: **True**; staged == the pre-decision-3 copy: **True**; staged == table12/probe249_frozen.py: **True** -- every row name, note, want, session command and protocol key the gate block reads is the measured instrument's, so table 12's banked logs are what the staged probe prints.
* `ast.dump` with every string constant masked: staged == frozen: **True**.
* The decision-3 edit's own proof, the round's `r7_20261105/p11rec_proof.py` run by wtdoc_qhs.py --apply: `landing_20261105/PROOF_wtdoc_qhs.out` (all six comparisons EQUAL, the negative control DIFFERENT).
* Section U, HEAD's `tools/pipeline/check_score_claims.py` run unmodified in a scratch tree with the staged gate_ppc.sh: staged probe rc 0 `SCORE_CLAIMS_PASS  7 gate comment set(s) checked; 5 of 7 stems also have a probe docstring checked`; negative control (the staged probe with `PAIRS_OK=8/8` put back) rc 1 `SCORE_CLAIMS_FAIL  1 stale score claim(s)`.
* Docstring width: longest line 131 characters.  Placeholders left: none.  The rows the docstring names are filed by this landing: `ppcmpcheckstop`, `ppcifetchibinit`, `ppcbranchlowbits`, `ppcifetchdeclineprod`.  `py_compile`: run by the pretest.

Staged vs the working copy: 1 hunk(s) (the round number moved since decision 3).
