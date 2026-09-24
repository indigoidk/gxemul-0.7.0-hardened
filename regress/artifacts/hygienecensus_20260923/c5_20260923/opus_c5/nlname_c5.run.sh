#!/bin/bash
# End-to-end: a --grandfather / --release name holding a NEWLINE passes the F4 byte allow-list (tr leaves only the
# newline; $(...) strips trailing newlines).  What does the deriver then write, and what does the gate say after?
# Fresh /tmp copy per case (SEC regress top-level + tools + the three F4 frozen files).  /tmp only.
set -u
P=/mnt/c
SEC=$P/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
FROZ=$P/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/c5_frozen
OUT=$P/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/opus_c5/nlname
rm -rf "$OUT"; mkdir -p "$OUT"; S=$OUT/SUMMARY.txt; : > "$S"
mk() {
  local W=/tmp/gxc5_nl_$1; rm -rf "$W"; mkdir -p "$W/GXEMUL-SEC/regress" "$W/GXEMUL-SEC/tools" "$W/logs"
  (cd "$SEC/regress" && find . -maxdepth 1 -type f -exec cp -p {} "$W/GXEMUL-SEC/regress/" \;)
  cp -p "$FROZ/gate_hygiene.sh" "$FROZ/census_tokens.py" "$W/GXEMUL-SEC/regress/"
  cp -p "$FROZ/derive_hygiene_pins.sh" "$W/GXEMUL-SEC/tools/"; echo "$W"; }
listbody() { python3 -c '
import io,sys; s=io.open(sys.argv[1],encoding="utf-8").read()
i=s.index("GRANDFATHERED_PROMPTLESS=\"")+len("GRANDFATHERED_PROMPTLESS=\""); j=s.index("\"",i)
b=s[i:j]; print("   list: %d names, %d lines, last 2 lines: %r" % (len(b.split()), b.count(chr(10))+1, b.split(chr(10))[-2:]))' "$1"; }
gate_rows() { ( cd "$1/GXEMUL-SEC/regress" && LOGDIR="$1/logs" bash ./gate_hygiene.sh ) 2>&1 | sed 's/\x1b\[[0-9;]*m//g' \
              | grep -E '^\s*FAIL.*(readiness|whole-buffer)' | sed 's/^\s*/   gate: /'; }
drv() { local W=$1; shift; ( GXROOT="$W" bash "$W/GXEMUL-SEC/tools/derive_hygiene_pins.sh" "$@" ) 2>&1; }

echo "== A: real tree (NO new promptless probe, NEWP empty); --grandfather \$'\\nzz_bogus.py'" >> "$S"
W=$(mk A); listbody "$W/GXEMUL-SEC/regress/gate_hygiene.sh" >> "$S"
drv "$W" --grandfather $'\nzz_bogus.py' | grep -E '^(REFUSED|GRANDFATHERED|DERIVE)' | sed 's/^/   deriver: /' >> "$S"
listbody "$W/GXEMUL-SEC/regress/gate_hygiene.sh" >> "$S"; gate_rows "$W" >> "$S"; echo "   (no FAIL line above = all readiness rows green)" >> "$S"

echo "== B: real tree; --grandfather \$'\\narm_endian_probe.py' (a PROMPT-DETECTING probe smuggled into the list)" >> "$S"
W=$(mk B)
drv "$W" --grandfather $'\narm_endian_probe.py' | grep -E '^(REFUSED|GRANDFATHERED|DERIVE)' | sed 's/^/   deriver: /' >> "$S"
listbody "$W/GXEMUL-SEC/regress/gate_hygiene.sh" >> "$S"; gate_rows "$W" >> "$S"

echo "== C: a REAL new promptless probe zz-legit_probe.py; --grandfather \$'zz-legit_probe.py\\nextra_name.py'" >> "$S"
W=$(mk C); cp -p "$W/GXEMUL-SEC/regress/pcc2_width_probe.py" "$W/GXEMUL-SEC/regress/zz-legit_probe.py"
drv "$W" --grandfather $'zz-legit_probe.py\nextra_name.py' | grep -E '^(REFUSED|GRANDFATHERED|DERIVE)' | sed 's/^/   deriver: /' >> "$S"
listbody "$W/GXEMUL-SEC/regress/gate_hygiene.sh" >> "$S"; gate_rows "$W" >> "$S"

echo "== D: newline-ONLY name \$'\\n' (non-empty, so [ -n ] passes)" >> "$S"
W=$(mk D)
drv "$W" --grandfather $'\n' | grep -E '^(REFUSED|GRANDFATHERED|DERIVE)' | sed 's/^/   deriver: /' >> "$S"
listbody "$W/GXEMUL-SEC/regress/gate_hygiene.sh" >> "$S"

echo "== E: --release \$'\\ngdrom_cond_probe.py' (real tree, GONE empty)" >> "$S"
W=$(mk E)
drv "$W" --release $'\ngdrom_cond_probe.py' | grep -E '^(REFUSED|RELEASED|DERIVE)' | sed 's/^/   deriver: /' >> "$S"
listbody "$W/GXEMUL-SEC/regress/gate_hygiene.sh" >> "$S"

echo "== F: CONTROL -- --grandfather \$'\\tzz_bogus.py' (a TAB, which the allow-list does refuse)" >> "$S"
W=$(mk F)
drv "$W" --grandfather $'\tzz_bogus.py' | grep -E '^(REFUSED|GRANDFATHERED|DERIVE)' | sed 's/^/   deriver: /' >> "$S"
rm -rf /tmp/gxc5_nl_*
echo "NLNAME_E2E_DONE $(date '+%F %T')" >> "$S"
cat "$S"
