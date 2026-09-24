#!/bin/bash
# parse (ast only, no bytecode written) every file an evasion case modified or added, in its copy
set -u
C=/tmp/opus_census0923/c
OUT=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/opus/runs/syntax_check.txt
: > "$OUT"
chk() { python3 - "$1" >> "$OUT" 2>&1 <<'PY'
import ast, io, sys
f = sys.argv[1]
try:
    ast.parse(io.open(f, encoding="utf-8").read(), filename=f); print("PARSES  " + f)
except SyntaxError as e:
    print("SYNTAX-ERROR  %s: %s" % (f, e))
PY
}
for c in c1_single_quote c2_inner_spaces c3a_comment_indented c3b_comment_col0 e1_receiver_named_out e2_split_across_lines \
         e3_space_before_paren e4_slice_compare e5_strip_not_rstrip e9_bare_space_before_paren e9ctl_bare_plain; do
  chk "$C/$c/regress/luna_absentcpu_probe.py"; tail -2 "$C/$c/regress/luna_absentcpu_probe.py" | sed 's/^/      tail| /' >> "$OUT"
done
chk "$C/e6_move_within_allowlist/regress/arm_flags_probe.py"; chk "$C/e6_move_within_allowlist/regress/arm_bdt_probe.py"
chk "$C/e7_new_promptless_space_name/regress/zz opus_newprobe.py"
chk "$C/e13_new_promptless_comment_mentions/regress/zz_opus_newprobe.py"
chk "$C/e15_crime_comment_reworded/regress/crime_width_probe.py"
echo SYNTAX_DONE >> "$OUT"; echo SYNTAX_DONE
