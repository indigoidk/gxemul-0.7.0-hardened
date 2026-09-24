#!/bin/bash
# SECTION 2 (gate-integration) -- show census_tokens.py's docstring claims moving REAL gate rows, on /tmp copies.
#  g_untok  : a prompt-detecting probe made UNTOKENIZABLE -> census lists it promptless -> names row RED (new=that file)
#  g_crlf   : a prompt-detecting probe rewritten with CRLF endings -> still classified correctly -> all rows GREEN
#  g_tabpred: a probe's predicate re-indented with TABs -> still tokenizes -> all rows GREEN
#  g_docstr : a promptless-hiding docstring on a NEW-less edit (in-place) -> names row RED (token classifier)
set -u
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
FROZ=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/c2_frozen
OUT=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/opus_c2/s2gate
W=/tmp/gxc2_s2g
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
  { echo "=== $tag : $nf readiness FAIL(s)"
    grep -E '^\s*FAIL.*(readiness|whole-buffer)|NEW PROMPTLESS' "$OUT/$tag.out" | sed 's/^/   /'; echo; } >> "$S"
}

# g_untok: truncate arm_endian mid-expression so tokenize raises (unbalanced) -> fail-closed promptless
mk g_untok; python3 -c 'import io,sys; p=sys.argv[1]; s=io.open(p,encoding="utf-8").read(); io.open(p,"w",encoding="utf-8").write(s+"\nx = (1 +\n")' "$(rdir g_untok)/arm_endian_probe.py"
runrows g_untok

# g_crlf: rewrite a prompt-detecting probe with CRLF endings; must stay classified the same (all green)
mk g_crlf; python3 -c 'import io,sys; p=sys.argv[1]; s=io.open(p,encoding="utf-8",newline="").read(); io.open(p,"wb").write(s.replace("\n","\r\n").encode("utf-8"))' "$(rdir g_crlf)/arm_endian_probe.py"
echo "   g_crlf: CR count in file = $(grep -c $'\r' "$(rdir g_crlf)/arm_endian_probe.py")" >> "$S"
runrows g_crlf

# g_tabpred: re-indent arm_endian's predicate block with a leading TAB replacing 12 spaces (consistent) -> tokenizes -> green
mk g_tabpred; python3 -c '
import io,sys
p=sys.argv[1]; s=io.open(p,encoding="utf-8").read()
# convert the whole file to tab indentation deterministically: leading 4-space groups -> tabs
out=[]
for l in s.split("\n"):
    i=0
    while l[i:i+4]=="    ": i+=4
    out.append("\t"*(i//4)+l[i:])
io.open(p,"w",encoding="utf-8").write("\n".join(out))
' "$(rdir g_tabpred)/arm_endian_probe.py"
runrows g_tabpred

# g_docstr: hide arm_endian's ONLY predicate behind a docstring mention + a bare wait (in place, no new file) -> promptless -> names RED
mk g_docstr; python3 -c '
import io,sys
p=sys.argv[1]; s=io.open(p,encoding="utf-8").read()
old="            if len(buf) > mark and buf[mark:].rstrip().endswith(\"GXemul>\"):\n"
new="            if len(buf) > mark:  # buf[mark:].rstrip().endswith GXemul prompt (comment only)\n"
assert s.count(old)==1, s.count(old)
io.open(p,"w",encoding="utf-8").write(s.replace(old,new))
' "$(rdir g_docstr)/arm_endian_probe.py"
runrows g_docstr

rm -rf "$W"
echo "S2GATE_DONE $(date '+%F %T')" >> "$S"
cat "$S"
