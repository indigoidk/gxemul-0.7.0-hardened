#!/bin/bash
# opus measuring seat -- tools/derive_hygiene_pins.sh on COPIES (GXROOT=<dir>, <dir>/GXEMUL-SEC/{regress,tools}).
# Uses the snapshot measure_gate.sh took, so the regress bytes are identical to the gate cases.
set -u
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
W=/tmp/opus_census0923
OUT=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/opus/runs
SNAP=$W/snap/regress
[ -f "$SNAP/gate_hygiene.sh" ] || { echo "no snapshot -- run measure_gate.sh first"; exit 9; }
: > "$OUT/DERIVER_SUMMARY.txt"
echo "deriver md5 (tree): $(md5sum < "$SEC/tools/derive_hygiene_pins.sh")" >> "$OUT/DERIVER_SUMMARY.txt"

mkroot() {
  local r=$W/d/$1
  rm -rf "$r"; mkdir -p "$r/GXEMUL-SEC/regress" "$r/GXEMUL-SEC/tools" "$r/logs"
  cp -p "$SNAP/"* "$r/GXEMUL-SEC/regress/"
  cp -p "$SEC/tools/derive_hygiene_pins.sh" "$r/GXEMUL-SEC/tools/"
  printf '%s' "$r"
}
app() { python3 - "$@" <<'PY'
import io, sys
f, lines = sys.argv[1], sys.argv[2:]
s = io.open(f, encoding="utf-8", newline="").read()
if not s.endswith("\n"): s += "\n"
io.open(f, "w", encoding="utf-8", newline="").write(s + "".join(l + "\n" for l in lines))
PY
}
sub1() { python3 - "$@" <<'PY'
import io, sys
f, old, new = sys.argv[1:]
s = io.open(f, encoding="utf-8", newline="").read()
assert s.count(old) >= 1, ("absent", f, old)
io.open(f, "w", encoding="utf-8", newline="").write(s.replace(old, new, 1))
PY
}
elide() { awk '/^UNTRACKED files/ {skip=1; next} skip && /^  / {n++; next} {skip=0; print} END {if (n) print "  [UNTRACKED block elided: " n " names -- the copy is outside git, so every file reads untracked]"}'; }
derive() {  # derive <tag> <root> [args] -- runs it, records rc, and whether the gate file changed
  local tag=$1 r=$2; shift 2
  local g=$r/GXEMUL-SEC/regress/gate_hygiene.sh
  cp -p "$g" "$r/gate.before.$tag"
  ( GXROOT=$r bash "$r/GXEMUL-SEC/tools/derive_hygiene_pins.sh" "$@" ) > "$OUT/$tag.derive" 2>&1
  local rc=$?
  { echo "===== $tag: derive_hygiene_pins.sh $* -> rc=$rc"
    elide < "$OUT/$tag.derive" | sed 's/^/   /'
    if cmp -s "$r/gate.before.$tag" "$g"; then echo "   gate_hygiene.sh in the copy: UNCHANGED (cmp clean)"
    else echo "   gate_hygiene.sh in the copy: CHANGED:"; diff "$r/gate.before.$tag" "$g" | sed 's/^/      /'; fi
  } >> "$OUT/DERIVER_SUMMARY.txt"
}
gaterun() {  # gaterun <tag> <root> -- the unmodified-procedure gate on that copy, readiness rows vs base
  local tag=$1 r=$2
  ( cd "$r/GXEMUL-SEC/regress" && LOGDIR="$r/logs" bash ./gate_hygiene.sh ) > "$OUT/$tag.gate.out" 2>&1
  grep -E 'readiness' "$OUT/$tag.gate.out" > "$OUT/$tag.gate.rows"
  { echo "   gate after that: readiness rows ($(grep -c '^  FAIL' "$OUT/$tag.gate.rows") FAIL of $(wc -l < "$OUT/$tag.gate.rows"))"
    sed 's/^/      /' "$OUT/$tag.gate.rows"
    grep -A4 'NEW PROMPTLESS' "$OUT/$tag.gate.out" | sed 's/^/      | /'
  } >> "$OUT/DERIVER_SUMMARY.txt"
}
L=luna_absentcpu_probe.py

# ---- 0: unmodified copy, report + --write (the no-op control) ----
r=$(mkroot d0_unmodified); derive d0_report "$r"; derive d0_write "$r" --write

# ---- 7a: luna's `_mark` renamed back to `mark` (the three #392 counts disagree) ----
r=$(mkroot d7a_mark_rename)
sub1 "$r/GXEMUL-SEC/regress/$L" '_mark = len(self.buf)' 'mark = len(self.buf)'
sub1 "$r/GXEMUL-SEC/regress/$L" 'wait(mark=_mark, echo=x' 'wait(mark=mark, echo=x'
grep -nE '^\s*_?mark = len\(self\.buf\)|wait\(mark=_?mark' "$r/GXEMUL-SEC/regress/$L" > "$OUT/d7a_luna_lines.txt"
derive d7a_report "$r"; derive d7a_write "$r" --write

# ---- 7b: one extra pty probe with no endswith( (a copy of promptless pcc2_width_probe.py) ----
r=$(mkroot d7b_new_promptless)
cp -p "$r/GXEMUL-SEC/regress/pcc2_width_probe.py" "$r/GXEMUL-SEC/regress/zz_opus_newprobe.py"
derive d7b_report "$r"; derive d7b_write "$r" --write

# ---- does --write launder what the gate says must never be re-pinned? ----
# L1: a NEW unrecognised endswith spelling (the closed-world row) -- EXPECT_UNKNOWN is written, not refused?
r=$(mkroot dL1_unknown_spelling)
app "$r/GXEMUL-SEC/regress/$L" '_control_site = lambda buf: buf.rstrip().endswith(PROMPT)'
gaterun dL1_before "$r"; derive dL1_write "$r" --write; gaterun dL1_after "$r"
# L2: a 4th whole-buffer site inside an ALLOWLISTED file -- EXPECT_WHOLE_FULL 3 -> 4 and the name set is unchanged?
r=$(mkroot dL2_fourth_site_allowlisted_file)
app "$r/GXEMUL-SEC/regress/arm_bdt_probe.py" '_control_site = lambda buf: buf.rstrip().endswith("GXemul>")'
gaterun dL2_before "$r"; derive dL2_write "$r" --write; gaterun dL2_after "$r"
# L3: a NEW promptless pty probe in a new subdirectory -- NEWP cannot see it, so --write raises the denominator?
r=$(mkroot dL3_promptless_in_subdir)
mkdir -p "$r/GXEMUL-SEC/regress/newsub"
cp -p "$r/GXEMUL-SEC/regress/pcc2_width_probe.py" "$r/GXEMUL-SEC/regress/newsub/zz_opus_subprobe.py"
gaterun dL3_before "$r"; derive dL3_write "$r" --write; gaterun dL3_after "$r"
# L4 (control): a 4th site in a NON-allowlisted file (the brief's `add` case) -- the name row should stay red after --write
r=$(mkroot dL4_fourth_site_new_file)
app "$r/GXEMUL-SEC/regress/$L" '_control_site = lambda buf: buf.rstrip().endswith("GXemul>")'
derive dL4_write "$r" --write; gaterun dL4_after "$r"

# L5: a NEW promptless pty probe whose only `endswith(` is in a COMMENT -- grep -L sees the text, so NEWP is empty?
r=$(mkroot dL5_promptless_comment_mentions)
cp -p "$r/GXEMUL-SEC/regress/pcc2_width_probe.py" "$r/GXEMUL-SEC/regress/zz_opus_newprobe.py"
app "$r/GXEMUL-SEC/regress/zz_opus_newprobe.py" '# readiness: fixed waits, no endswith( predicate here'
gaterun dL5_before "$r"; derive dL5_write "$r" --write; gaterun dL5_after "$r"

echo "MEASURE_DERIVER_DONE" >> "$OUT/DERIVER_SUMMARY.txt"
echo MEASURE_DERIVER_DONE
