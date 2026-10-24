T36 / #570 (m88kbuserrregs) -- what the files in staged/ are.  Written 2026-10-24 by the builder's pre-commit repair
step (REPAIR_SPEC section 3, PASS2_RULINGS D3/D4; repair1_20261024/).  Nothing here is run by any gate.

gate_arm.sh.txt
    The HEAD-based copy of regress/gate_arm.sh carrying the #570 block (inserted after #568's block, lines 1916-1944).
    It is byte-identical to the working-tree regress/gate_arm.sh, which has no other uncommitted change.  When gate 14
    ran (table1_20261023/gates/gate14_run.out) and when the two gate_arm.*.diff files below were made, both copies were
    md5 5ee94e61a100473ba95db05f43f34a96.  On 2026-10-24 the block's opening comment sentence was corrected in BOTH
    copies identically (comment lines 1917-1925 only, nine lines kept; repair1_20261024/GATE_COMMENT.txt), giving
    md5 f04fad2c589f9eb10f4a4fc3dc5896d9, and this copy was then RENAMED from gate_arm.sh to gate_arm.sh.txt.

check_probe_wiring.py.txt
    The HEAD-based copy of tools/pipeline/check_probe_wiring.py carrying the two #570 MANIFEST entries -- what the
    landing commit should contain for that file.  The working-tree checker carries the same two entries PLUS the
    peer's uncommitted lines, which the landing commit must exclude (PASS2_RULINGS D9).  Its #570 MANIFEST text was
    updated on 2026-10-24 identically in both copies (repair1_20261024/MANIFEST_TEXT.txt).

gate_arm.WT.diff / gate_arm.staged.diff / check_probe_wiring.WT.diff / check_probe_wiring.staged.diff
    The insertion diffs made at 23:16 on 2026-10-23: HEAD -> working tree, and HEAD -> staged copy.  They PREDATE the
    2026-10-24 comment and MANIFEST-text edits, and gate_arm.staged.diff's `+++' path names staged/gate_arm.sh -- the
    name before the rename.  Both are left exactly as written (historical receipts of the insertion).

WHY THE .txt SUFFIX.  Every script copy kept under this round's artifacts dir carries a .py.txt / .sh.txt name, which
is what the #570 MANIFEST sentence says ("kept as *.py.txt / *.sh.txt, outside this checker's domain"): a .txt copy is
outside check_probe_wiring.py's domain (git ls-files '*.py' under regress/, once staged -- BUILDER_QUESTIONS Q19), is
not executable by name, and cannot be mistaken for the live file by a grep or a launcher.  Until the rename the gate copy
was gate_arm.sh, which made that sentence false (pass-2 finding P12; PASS2_RULINGS D4).
