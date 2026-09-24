#!/bin/bash
# a1_astcall.sh TAG -- astcall() EXTRACTED VERBATIM from the frozen deriver (awk, by name) and called on files, with
# PY chosen exactly as the deriver chooses it.  TAG: W (WSL) | G (git-bash).
set -u
TAG=$1
case "$TAG" in
  W) B=/mnt/c/DocumentNoSnc/cc/GXEMUL ;;
  G) B=/c/DocumentNoSnc/cc/GXEMUL ;;
esac
FROZ=$B/_scratchpad/census0923/c6_frozen; O=$B/_scratchpad/census0923/opus_c6/out/A1_$TAG.txt; : > "$O"
PY=""; for c in python3 python; do "$c" -c "import sys" >/dev/null 2>&1 && { PY=$c; break; }; done
python3() { command "$PY" "$@" | tr -d '\r'; }      # the deriver's shim is live when astcall runs; keep it live here
AC=$(awk '/^astcall\(\) \{/ {p=1} p {print} p && /^}$/ {exit}' "$FROZ/derive_hygiene_pins.sh")
eval "$AC"
echo "[$TAG] PY=$PY; astcall extracted: $(printf '%s\n' "$AC" | wc -l) lines, md5 $(printf '%s\n' "$AC" | md5sum | cut -c1-8)" >> "$O"
# test files -- in a PROJECT-LOCAL dir (both shells can reach it) and, under G, also in /tmp (the Windows temp dir)
T=$B/_scratchpad/census0923/opus_c6/work_a1_$TAG; rm -rf "$T"; mkdir -p "$T/newsub"
EW="ends""with"
printf 'import os\nx = 1\n' > "$T/nocall.py"
printf 'buf = ""\nif buf.rstrip().%s("GXemul>"):\n    pass\n' "$EW" > "$T/call.py"
sed 's/$/\r/' "$T/call.py" > "$T/call_crlf.py"; sed 's/$/\r/' "$T/nocall.py" > "$T/nocall_crlf.py"
printf 'def f()\n    return 1\nbuf.%s("x")\n' "$EW" > "$T/syntax.py"
printf 'buf.%s("x")\nx = (\n' "$EW" > "$T/unclosed.py"
{ printf '\xef\xbb\xbf'; cat "$T/call.py"; } > "$T/bom_call.py"
{ printf '\xef\xbb\xbf'; cat "$T/nocall.py"; } > "$T/bom_nocall.py"
printf '# \xe2\x80\x94 an em dash, \xc2\xb5s\nx = "\xc3\xa9"\n' > "$T/utf8_nocall.py"
printf 'x = "\xe9"\n' > "$T/latin1.py"
printf 'def f(x):\n    match x:\n        case K.%s("GXemul>"):\n            pass\n' "$EW" > "$T/matchonly.py"
printf 'buf = ""\ny = f"{buf.%s(\x27GXemul>\x27)}"\n' "$EW" > "$T/fstring.py"
printf 'g = lambda b: b.%s(">")\n' "$EW" > "$T/lambda.py"
cp "$T/call.py" "$T/newsub/sub_call.py"
exp() { printf '%s' "$1"; }
row() { astcall "$2"; local rc=$?; echo "A1 [$TAG] $1 rc=$rc want=$3 $( [ "$rc" = "$3" ] && echo ok || echo MISS)" >> "$O"; }
row nocall        "$T/nocall.py" 1
row call          "$T/call.py" 0
row call_crlf     "$T/call_crlf.py" 0
row nocall_crlf   "$T/nocall_crlf.py" 1
row syntax        "$T/syntax.py" 2
row unclosed      "$T/unclosed.py" 2
row missing       "$T/no_such_file.py" 2
row bom_call      "$T/bom_call.py" 2
row bom_nocall    "$T/bom_nocall.py" 2
row utf8_nocall   "$T/utf8_nocall.py" 1
row latin1        "$T/latin1.py" 2
row matchonly     "$T/matchonly.py" 1
row fstring       "$T/fstring.py" 0
row lambda        "$T/lambda.py" 0
row subdir        "$T/newsub/sub_call.py" 0
if [ "$TAG" = G ]; then
  U=$(mktemp -d); cp "$T/call.py" "$T/nocall.py" "$U/"
  row tmp_call    "$U/call.py" 0
  row tmp_nocall  "$U/nocall.py" 1
  rm -rf "$U"
fi
# the census classifier on the same files, the deriver's way (paths on stdin, relative)
( cd "$T" && ls *.py newsub/*.py ) | python3 "$FROZ/census_tokens.py" promptless "$T" | sed "s/^/A1 [$TAG] census-promptless: /" >> "$O"
rm -rf "$T"; echo A1_DONE >> "$O"; cat "$O"
