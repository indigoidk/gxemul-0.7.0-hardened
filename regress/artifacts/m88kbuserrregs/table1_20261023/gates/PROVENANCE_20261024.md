# Gate receipts -- dated provenance addendum, 2026-10-24

T36 / `#570` pre-commit repair (`../../pass2_20261023/PASS2_RULINGS.md` D2/D3 and section E; `../../pass2_20261023/REPAIR_SPEC.md`
section 7).  The raw receipts in this directory are **not relabelled**: each is a receipt for the bytes it names.

## What the receipts ran

`gate14_run.out` (gate 14: `PASS (1310 checks)`, `REGRESS_PASS`, wall 7974 s) and `gate11_run.out` (gate 11:
`PASS (111 checks)`, `REGRESS_PASS`) name the files they ran, on their lines 2-3:

* binary `build/gxemul` md5 `931e69fad9624daef30e83d274a4493d`;
* `regress/gate_arm.sh` md5 `5ee94e61a100473ba95db05f43f34a96`;
* `regress/m88k_buserr_probe.py` md5 `d57c12ab7ade903946c7d80a8e153ab7` (revision 2, the measured instrument; frozen as
  `../m88k_buserr_probe.rev2.frozen.py.txt`).

## What ships instead, and how it relates

| file | at the gate run | shipped | relation, and where it is shown |
|---|---|---|---|
| `regress/gate_arm.sh` | `5ee94e61` | `f04fad2c589f9eb10f4a4fc3dc5896d9` | the `#570` block's opening comment only (lines 1917-1925, nine lines kept); every non-comment line identical (`../../repair1_20261024/GATE_COMMENT.txt`) |
| `regress/m88k_buserr_probe.py` | `d57c12ab` (rev 2) | `a49f417d37484071143de7e13637f4a4` (documentation revision 2c) | docstring only: everything outside the module docstring byte-identical, AST identical, `REVISION = 2` unchanged (`../../repair1_20261024/rev2c_equivalence.txt`, `rev2c_ast_identity.out`).  Revision 2b (`9046d774`) is superseded, its receipts in `../../repair1_20261024/superseded_9046d774/`; `fe8cc784` was the intermediate (`superseded_fe8cc784/`) |
| `src/cpus/memory_rw.c` | `b36c9e13` | `4b71687469a8b38165f038d3e9171293` | the `#570` comment only (B2, B5), 13 lines kept (`../../repair1_20261024/product_comments.diff`, `LINE_CHECK.txt`) |
| `src/devices/dev_m8820x.c` | `c229294f` | `bd616d06d7a2a4da388429ca326c4a5e` | comments only (B1, B3, B4), 551 lines kept |
| `src/cpus/cpu_m88k.c`, `src/devices/dev_luna88k.c` | `0321e2ba`, `e43c39ca` | unchanged | -- |

**The binary is the same bytes.**  `build/` rebuilt from the comment-edited sources (`rm src/cpus/*.o; make`) gives
`build/gxemul` md5 `931e69fa...` again, with all 224 objects and the binary identical before and after
(`../../repair1_20261024/PROPAGATE_build.out`).  So the binary these receipts ran is the binary of the shipped sources.

**Rev 2c's own receipts.**  Rev 2c was run once on the fixed work binary (`3cd0501c`, 31/31, SYMPTOM=ABSENT) and once on
the HEAD binary (`2efeec55`, 21/31, SYMPTOM=PRESENT 10/10).  Every row, marker and sentinel matches rev 2's
`../fixed.out` and `../prefix_HEAD.out` (`../../repair1_20261024/rev2c_rowcompare.txt`).  Revision 2b's receipts,
which matched the same way, are kept in `../../repair1_20261024/superseded_9046d774/`.

**The caveat, from the adjudication (GPT-6 Astra, F2), kept verbatim:** "The two reruns alone do not demonstrate every
old mutation result or make the old gate receipt a rev-2b measurement; the verified documentation-only relationship
supplies that justification."  The gates were not re-run for comment or docstring edits (PASS2_RULINGS D3; REPAIR_SPEC
section 7).
