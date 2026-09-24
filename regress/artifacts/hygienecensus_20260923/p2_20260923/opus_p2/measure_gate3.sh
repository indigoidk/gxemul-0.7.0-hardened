#!/bin/bash
# opus measuring seat -- (1) e15: crime_width_probe.py with its COMMENT reworded so the literal `endswith(` is gone;
# (2) a property census of the census: every pty probe the gate classes as prompt-detecting (raw `endswith(` present),
#     with how many of those occurrences are in CODE and how many code lines hold a prompt literal.
set -u
W=/tmp/opus_census0923
OUT=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/opus/runs
[ -f "$W/snap/regress/gate_hygiene.sh" ] && [ -f "$OUT/base.rows" ] || { echo "run measure_gate.sh first"; exit 9; }
mk() { local p=$W/c/$1; rm -rf "$p"; mkdir -p "$p/regress" "$p/logs"; cp -p "$W/snap/regress/"* "$p/regress/"; printf '%s' "$p/regress"; }
: > "$OUT/SUMMARY3.txt"

d=$(mk e15_crime_comment_reworded)
python3 - "$d/crime_width_probe.py" <<'PY' >> "$OUT/SUMMARY3.txt"
import io, re, sys
f = sys.argv[1]
lines = io.open(f, encoding="utf-8", newline="").read().split("\n")
n = 0
for i, l in enumerate(lines):
    if re.match(r"\s*#", l) and "endswith(" in l:
        lines[i] = l.replace("endswith(", "ends-with("); n += 1
io.open(f, "w", encoding="utf-8", newline="").write("\n".join(lines))
print("e15: comment lines reworded in crime_width_probe.py: %d (code lines untouched)" % n)
PY
( cd "$d" && LOGDIR="$d/../logs" bash ./gate_hygiene.sh ) > "$OUT/e15_crime_comment_reworded.out" 2>&1
grep -E 'readiness' "$OUT/e15_crime_comment_reworded.out" > "$OUT/e15_crime_comment_reworded.rows"
{ echo "===== e15_crime_comment_reworded"
  sed 's/^/   /' "$OUT/e15_crime_comment_reworded.rows"
  grep -A4 'NEW PROMPTLESS' "$OUT/e15_crime_comment_reworded.out" | grep -v readiness | sed 's/^/   | /'
  if diff -q "$OUT/base.rows" "$OUT/e15_crime_comment_reworded.rows" >/dev/null; then echo "   -> IDENTICAL to base"
  else echo "   -> CHANGED vs base:"; diff "$OUT/base.rows" "$OUT/e15_crime_comment_reworded.rows" | grep -E '^[<>]' | sed 's/^/      /'; fi
} >> "$OUT/SUMMARY3.txt"

# property census over the snapshot's pty population (the gate's own _ptylist form)
S=$W/snap/regress
{ echo; echo "===== property census: pty probes the gate classes PROMPT-DETECTING (raw endswith( present)"
  printf '%-34s %5s %5s %6s %8s\n' file raw code prompt gxcode
  cd "$S" && find . -maxdepth 1 -name '*.py' -type f | xargs grep -l 'pty.fork' | sed 's|.*/||' | sort | while read -r f; do
    raw=$(grep -c 'endswith(' "$f")
    [ "$raw" -gt 0 ] || continue
    code=$(grep -v '^[[:space:]]*#' "$f" | grep -c 'endswith(')
    pr=$(grep -v '^[[:space:]]*#' "$f" | grep -cE "endswith\([\"'](GXemul)?>[\"']\)")
    gx=$(grep -v '^[[:space:]]*#' "$f" | grep -c 'GXemul>')
    flag=""; [ "$pr" -eq 0 ] && flag="   <-- no prompt literal in code"
    printf '%-34s %5s %5s %6s %8s%s\n' "$f" "$raw" "$code" "$pr" "$gx" "$flag"
  done
  echo "columns: raw = lines with endswith( (what grep -L keys on); code = those outside # comment lines;"
  echo "         prompt = code lines holding endswith(\"GXemul>\") or endswith(\">\") in either quote; gxcode = code lines mentioning GXemul>"
} >> "$OUT/SUMMARY3.txt"
echo MEASURE_GATE3_DONE >> "$OUT/SUMMARY3.txt"; echo MEASURE_GATE3_DONE
