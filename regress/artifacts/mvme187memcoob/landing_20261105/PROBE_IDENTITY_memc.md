# PROBE_IDENTITY_memc.md -- the staged regress/mvme187_memc_probe.py differs from the working copy in its docstring only

Built by build_staged_memc.py at HEAD cbd916d1.  Working copy 57173 bytes md5 647d0d5e6c1c87d4527370b272539b23; staged 57173 bytes md5 eec0285d793a2f54a94f7f4af6c33dbc; table 5's frozen instrument (`regress/artifacts/mvme187memcoob/r5_20261105/table5/probe206_frozen.py`) md5 5d0cb614dc185067ee850d975a904062.

* `ast.dump` with the module docstring dropped, every string kept: staged == working copy: **True**.
* `ast.dump` with the module docstring dropped and every string constant replaced by 'S' (the method of `regress/artifacts/mvme187memcoob/r6_20261105/textonly_check.py`, check 1): staged == table5/probe206_frozen.py: **True** -- so every row name, session, instruction word, seed, want, function body and non-string constant is the instrument table 5 measured; the printed text differs where the records corrections (r6_20261105/RECORDS6_NOTE.md, sections 1-8) say.
* `py_compile`: run by the pretest.

Why the one edit: the docstring's `THE FIX (#NNN).` names the round number the landing assigns (#581, derived: max round heading in HEAD's CHANGELOG.md (#580) + 1).  Hunks:

```
@@ line 8
- THE FIX (#NNN).  Each served offset reads its own field (chipid +0x00, chiprev +0x04, memconf +0x08); controller 1 (+0x100..0x1ff)
+ THE FIX (#581).  Each served offset reads its own field (chipid +0x00, chiprev +0x04, memconf +0x08); controller 1 (+0x100..0x1ff)
```
