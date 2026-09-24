#!/bin/bash
# SECTION 2 fail-direction -- when the F3 classifier LOSES a probe's only readiness call, does the gate fail CLOSED?
# Replace arm_endian_probe.py's sole predicate with each lost form; expect the names row to RED (new=arm_endian).
set -u
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
FROZ=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/c3_frozen
OUT=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/opus_c3/s2c
W=/tmp/gxc3_s2c
rm -rf "$W" "$OUT"; mkdir -p "$W/snap/GXEMUL-SEC/regress" "$W/snap/GXEMUL-SEC/tools" "$W/c" "$OUT"
S=$OUT/SUMMARY.txt; : > "$S"
(cd "$SEC/regress" && find . -maxdepth 1 -type f -exec cp -p {} "$W/snap/GXEMUL-SEC/regress/" \;)
cp -p "$SEC/tools/derive_hygiene_pins.sh" "$W/snap/GXEMUL-SEC/tools/"
cp -p "$FROZ/gate_hygiene.sh" "$W/snap/GXEMUL-SEC/regress/gate_hygiene.sh"
cp -p "$FROZ/census_tokens.py" "$W/snap/GXEMUL-SEC/regress/census_tokens.py"
mk() { rm -rf "$W/c/$1"; cp -a "$W/snap" "$W/c/$1"; }
rdir() { echo "$W/c/$1/GXEMUL-SEC/regress"; }
runrows() {
  local tag=$1 d; d=$(rdir "$tag"); mkdir -p "$W/c/$tag/logs"
  ( cd "$d" && LOGDIR="$W/c/$tag/logs" bash ./gate_hygiene.sh ) 2>&1 | sed 's/\x1b\[[0-9;]*m//g' > "$OUT/$tag.out"
  local nf; nf=$(grep -cE '^\s*FAIL.*(readiness|whole-buffer)' "$OUT/$tag.out")
  { echo "=== $tag : $nf readiness FAIL(s)"; grep -E '^\s*FAIL.*(readiness|whole-buffer)' "$OUT/$tag.out" | sed 's/^/   /'; echo; } >> "$S"
}
OLD='            if len(buf) > mark and buf[mark:].rstrip().endswith("GXemul>"):'
# nljoin form (reference then paren on next statement) as the sole predicate
mk f_nljoin; python3 - "$(rdir f_nljoin)/arm_endian_probe.py" "$OLD" <<'PY'
import io,sys
p,old=sys.argv[1],sys.argv[2]
s=io.open(p,encoding="utf-8").read()
new="            _ready = buf[mark:].rstrip().endswith\n            _ok = (\"GXemul>\")\n            if len(buf) > mark and _ready == _ok:"
assert s.count(old)==1
io.open(p,"w",encoding="utf-8").write(s.replace(old,new))
PY
runrows f_nljoin
# getattr indirection as the sole predicate
mk f_getattr; python3 - "$(rdir f_getattr)/arm_endian_probe.py" "$OLD" <<'PY'
import io,sys
p,old=sys.argv[1],sys.argv[2]
s=io.open(p,encoding="utf-8").read()
new="            if len(buf) > mark and getattr(buf[mark:].rstrip(), \"ends\"+\"with\")(\"GXemul>\"):"
assert s.count(old)==1
io.open(p,"w",encoding="utf-8").write(s.replace(old,new))
PY
runrows f_getattr
rm -rf "$W"
echo "S2C_DONE $(date '+%F %T')" >> "$S"
cat "$S"
