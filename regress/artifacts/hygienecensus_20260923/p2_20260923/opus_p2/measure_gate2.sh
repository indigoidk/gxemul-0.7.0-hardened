#!/bin/bash
# opus measuring seat -- second batch of single edits, same snapshot as measure_gate.sh, same method.
set -u
W=/tmp/opus_census0923
OUT=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/opus/runs
[ -f "$W/snap/regress/gate_hygiene.sh" ] && [ -f "$OUT/base.rows" ] || { echo "run measure_gate.sh first"; exit 9; }
mk() { local p=$W/c/$1; rm -rf "$p"; mkdir -p "$p/regress" "$p/logs"; cp -p "$W/snap/regress/"* "$p/regress/"; printf '%s' "$p/regress"; }
app() { python3 - "$@" <<'PY'
import io, sys
f, lines = sys.argv[1], sys.argv[2:]
s = io.open(f, encoding="utf-8", newline="").read()
if not s.endswith("\n"): s += "\n"
io.open(f, "w", encoding="utf-8", newline="").write(s + "".join(l + "\n" for l in lines))
PY
}
rows() { grep -E 'readiness' "$1" | sed 's/\x1b\[[0-9;]*m//g'; }
raw() {
  local d=$1 n tag=$2
  n=$(grep -n 'check "readiness: send takes a fresh mark (#392)"' "$d/gate_hygiene.sh" | cut -d: -f1)
  { head -n "$n" "$d/gate_hygiene.sh"
    printf '%s\n' 'echo "RAW allends=$allends bare=$bare full=$full unknown=$unknown whole_full=$whole_full whole_files=[$whole_files] ptyn=$_ptyn promptless=$_got/$_want new=[$(echo $_new)] conv=$conv_anchor/$conv_echo/$conv_mark"'
    echo 'exit 0'; } > "$d/zz_raw_gate.sh"
  ( cd "$d" && LOGDIR="$d/../logs_raw" bash ./zz_raw_gate.sh 2>/dev/null | grep '^RAW' ) > "$OUT/$tag.raw"
  rm -f "$d/zz_raw_gate.sh"
}
run() {
  local tag=$1 d=$2
  ( cd "$d" && LOGDIR="$d/../logs" bash ./gate_hygiene.sh ) > "$OUT/$tag.out" 2>&1
  rows "$OUT/$tag.out" > "$OUT/$tag.rows"; raw "$d" "$tag"
  { echo "===== $tag"
    sed 's/^/   /' "$OUT/$tag.rows"
    grep -A4 'NEW PROMPTLESS' "$OUT/$tag.out" | grep -v readiness | sed 's/^/   | /'
    sed 's/^/   /' "$OUT/$tag.raw"
    if diff -q "$OUT/base.rows" "$OUT/$tag.rows" >/dev/null; then echo "   -> readiness rows IDENTICAL to base (no row changed)"
    else echo "   -> readiness rows CHANGED vs base:"; diff "$OUT/base.rows" "$OUT/$tag.rows" | grep -E '^[<>]' | sed 's/^/      /'; fi
  } >> "$OUT/SUMMARY2.txt"
}
: > "$OUT/SUMMARY2.txt"
L=luna_absentcpu_probe.py
# e9: the #37 BARE-prompt defect itself, spelled with a space before the paren
d=$(mk e9_bare_space_before_paren); app "$d/$L" '_control_site = lambda buf: buf.endswith (">")'
run e9_bare_space_before_paren "$d"
# e9ctl: the same without the space must red the bare row
d=$(mk e9ctl_bare_plain); app "$d/$L" '_control_site = lambda buf: buf.endswith(">")'
run e9ctl_bare_plain "$d"
# e13: a NEW promptless pty probe whose only `endswith(` is inside a COMMENT
d=$(mk e13_new_promptless_comment_mentions); cp -p "$d/pcc2_width_probe.py" "$d/zz_opus_newprobe.py"
app "$d/zz_opus_newprobe.py" '# readiness: fixed waits, no endswith( predicate here'
run e13_new_promptless_comment_mentions "$d"
# e14: RENAME a grandfathered promptless probe (git mv): denominator and promptless COUNT both unchanged
d=$(mk e14_rename_grandfathered); mv "$d/gdrom_cond_probe.py" "$d/zz_renamed_cond_probe.py"
run e14_rename_grandfathered "$d"
echo MEASURE_GATE2_DONE >> "$OUT/SUMMARY2.txt"; echo MEASURE_GATE2_DONE
