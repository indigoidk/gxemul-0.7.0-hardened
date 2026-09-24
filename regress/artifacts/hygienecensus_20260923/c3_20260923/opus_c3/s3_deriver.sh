#!/bin/bash
# SECTION 3 (Q1 c/d) -- can a non-comment line still reach the gate through --ruling, and do the name checks
# wrongly refuse/accept?  Fresh /tmp snapshot (SEC top-level + the 3 FROZEN F3 files).  /tmp only.
set -u
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
FROZ=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/c3_frozen
OUT=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/opus_c3/s3
W=/tmp/gxc3_s3
rm -rf "$W" "$OUT"; mkdir -p "$W/snap/GXEMUL-SEC/regress" "$W/snap/GXEMUL-SEC/tools" "$W/c" "$OUT"
S=$OUT/SUMMARY.txt; T=$OUT/TABLE.txt; : > "$S"; : > "$T"
(cd "$SEC/regress" && find . -maxdepth 1 -type f -exec cp -p {} "$W/snap/GXEMUL-SEC/regress/" \;)
cp -p "$SEC/tools/derive_hygiene_pins.sh" "$W/snap/GXEMUL-SEC/tools/"
cp -p "$FROZ/gate_hygiene.sh" "$W/snap/GXEMUL-SEC/regress/gate_hygiene.sh"
cp -p "$FROZ/census_tokens.py" "$W/snap/GXEMUL-SEC/regress/census_tokens.py"
app() { python3 -c 'import io,sys; p=sys.argv[1]; s=io.open(p,encoding="utf-8").read(); io.open(p,"w",encoding="utf-8").write(s+"\n"+sys.argv[2]+"\n")' "$1/$2" "$3"; }
mk() { rm -rf "$W/c/$1"; cp -a "$W/snap" "$W/c/$1"; }
rdir() { echo "$W/c/$1/GXEMUL-SEC/regress"; }
drv() {
  local tag=$1; shift
  local r=$W/c/$tag g; g=$(rdir "$tag")/gate_hygiene.sh
  cp -p "$g" "$r/gate.before"
  ( GXROOT="$r" bash "$r/GXEMUL-SEC/tools/derive_hygiene_pins.sh" "$@" ) > "$OUT/$tag.drv" 2>&1; local rc=$?
  local first ch parse inj
  first=$(grep -m1 -E '^(REFUSED|DERIVE_FAIL|usage|WRITTEN|GRANDFATHERED|RELEASED)' "$OUT/$tag.drv" | cut -c1-95)
  if cmp -s "$r/gate.before" "$g"; then ch="unchanged"; else ch="CHANGED"; fi
  parse=$(cd "$(rdir "$tag")" && bash -n gate_hygiene.sh 2>&1 && echo OK || echo PARSE-FAIL)
  inj=$(grep -c '^EXPECT_WHOLE_FULL=999' "$g" 2>/dev/null || echo 0)
  printf '%-12s rc=%-2s gate=%-9s bash-n=%-10s inj999=%s  %s\n' "$tag" "$rc" "$ch" "$parse" "$inj" "$first" >> "$T"
  { echo "=== $tag :: $*"; echo "   rc=$rc gate=$ch bash-n=$parse inj999=$inj"; sed 's/^/   /' "$OUT/$tag.drv" | head -4; echo; } >> "$S"
}
WHOLE='_c = lambda mybuf: mybuf.rstrip().endswith("GXemul>")'   # a real whole site -> NEED non-empty (receiver ends buf)

echo "== byte check of the multibyte separators we will pass:" >> "$S"
printf '  U+2028 bytes: '; printf '%s' $' ' | xxd | head -1
{ printf '  U+2028 bytes: '; printf '%s' $' ' | od -An -tx1 | head -1
  printf '  U+0085 bytes: '; printf '%s' $'\u0085' | od -An -tx1 | head -1; } >> "$S"

# ---- Q1(c): ruling -> non-comment line? ----
# newline (must be refused now)
mk r_nl;   app "$(rdir r_nl)" luna_absentcpu_probe.py "$WHOLE"
drv r_nl   --write --ruling "$(printf '2026-09-23: valid reason enough here\nEXPECT_WHOLE_FULL=999')"
# tab (control char)
mk r_tab;  app "$(rdir r_tab)" luna_absentcpu_probe.py "$WHOLE"
drv r_tab  --write --ruling "$(printf '2026-09-23: valid reason enough here\tEXPECT_WHOLE_FULL=999')"
# vertical tab / carriage return (control)
mk r_cr;   app "$(rdir r_cr)" luna_absentcpu_probe.py "$WHOLE"
drv r_cr   --write --ruling "$(printf '2026-09-23: valid reason enough here\rEXPECT_WHOLE_FULL=999')"
# U+0085 NEL
mk r_nel;  app "$(rdir r_nel)" luna_absentcpu_probe.py "$WHOLE"
drv r_nel  --write --ruling "2026-09-23: valid reason enough here"$'\u0085'"EXPECT_WHOLE_FULL=999"
# U+2028 LINE SEPARATOR
mk r_ls;   app "$(rdir r_ls)" luna_absentcpu_probe.py "$WHOLE"
drv r_ls   --write --ruling "2026-09-23: valid reason enough here"$' '"EXPECT_WHOLE_FULL=999"
# very long single-line ruling (5000 chars) -- expect WRITTEN, gate parses
mk r_long; app "$(rdir r_long)" luna_absentcpu_probe.py "$WHOLE"
LONG="2026-09-23: $(python3 -c 'print("reason "*800)')"
drv r_long --write --ruling "$LONG"
# 16 non-blank but meaningless (dots) -- expect WRITTEN (weak warrant; minor)
mk r_dots; app "$(rdir r_dots)" luna_absentcpu_probe.py "$WHOLE"
drv r_dots --write --ruling "2026-09-23: ................"
# whitespace-only reason (must be refused now)
mk r_ws;   app "$(rdir r_ws)" luna_absentcpu_probe.py "$WHOLE"
drv r_ws   --write --ruling "2026-09-23:                     "

# ---- Q1(d): name checks + exact release ----
# space in name -> refused
mk n_space; cp "$(rdir n_space)/pcc2_width_probe.py" "$(rdir n_space)/zz new probe.py" 2>/dev/null || true
drv n_space --grandfather "zz new probe.py"
# glob char '?' -> refused
mk n_q; drv n_q --grandfather 'zz?.py'
# glob char '*' -> refused
mk n_star; drv n_star --grandfather 'zz*.py'
# glob char '[' -> refused
mk n_brk; drv n_brk --grandfather 'zz[a].py'
# legit hyphen name that IS a new promptless probe -> accepted
mk n_ok; cp "$(rdir n_ok)/pcc2_width_probe.py" "$(rdir n_ok)/zz-legit_probe.py"; drv n_ok --grandfather zz-legit_probe.py
echo "   n_ok: list now names it? $(grep -o 'zz-legit_probe\.py' "$(rdir n_ok)/gate_hygiene.sh" | wc -l)" >> "$S"
# EXACT release: two grandfathered names sharing a suffix; release the short one -> exactly one removed
mk n_relpref
python3 - "$(rdir n_relpref)/gate_hygiene.sh" <<'PY'
import io,sys
p=sys.argv[1]; s=io.open(p,encoding="utf-8").read()
# add x-gdrom_cond_probe.py beside the existing gdrom_cond_probe.py in the list
s=s.replace('gdrom_cond_probe.py sgi_re_width_probe.py','gdrom_cond_probe.py x-gdrom_cond_probe.py sgi_re_width_probe.py',1)
io.open(p,"w",encoding="utf-8").write(s)
PY
# make BOTH no longer promptless so --release is allowed: give each a real code endswith call
app "$(rdir n_relpref)" gdrom_cond_probe.py '_r = lambda gbuf: gbuf.rstrip().endswith("GXemul>")'
# x-gdrom_cond_probe.py doesn't exist as a file, so it stays promptless-by-name-only; release only the real one
drv n_relpref --release gdrom_cond_probe.py
echo "   n_relpref after: gdrom_cond_probe.py count=$(grep -o '\bgdrom_cond_probe\.py' "$(rdir n_relpref)/gate_hygiene.sh" | wc -l)  x-gdrom count=$(grep -o 'x-gdrom_cond_probe\.py' "$(rdir n_relpref)/gate_hygiene.sh" | wc -l)" >> "$S"

rm -rf "$W"
echo "S3_DONE $(date '+%F %T')" >> "$S"; echo "S3_DONE" >> "$T"
cat "$T"; echo; grep -E 'n_ok:|n_relpref after:|U\+' "$S"
