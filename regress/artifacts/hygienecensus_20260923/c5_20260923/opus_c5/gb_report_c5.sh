#!/bin/bash
# git-bash, REAL environment (python3 = Windows Store stub -> the F5 shim runs Windows `python`, which writes CRLF to a
# pipe).  Run the F5 deriver on an UNMODIFIED git-bash /tmp copy: report, --write, and --grandfather/--release of real
# names; show the NEW/GONE counts and the raw bytes of the census, to see whether CRs reach the name comparisons.
set -u
[ -f /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/gate_hygiene.sh ] || { echo "GB_FAIL: not git-bash layout"; exit 9; }
SEC=/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
FROZ=/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/c5_frozen
OUT=/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/opus_c5/gb_report
WR=/tmp/gxc5_gbrep
rm -rf "$WR" "$OUT"; mkdir -p "$WR/GXEMUL-SEC/regress" "$WR/GXEMUL-SEC/tools" "$OUT"; S=$OUT/SUMMARY.txt; : > "$S"
(cd "$SEC/regress" && find . -maxdepth 1 -type f -exec cp -p {} "$WR/GXEMUL-SEC/regress/" \;)
cp -p "$FROZ/gate_hygiene.sh" "$FROZ/census_tokens.py" "$WR/GXEMUL-SEC/regress/"; cp -p "$FROZ/derive_hygiene_pins.sh" "$WR/GXEMUL-SEC/tools/"
D=$WR/GXEMUL-SEC/tools/derive_hygiene_pins.sh; R=$WR/GXEMUL-SEC/regress
{ echo "git-bash report on F5 $(date '+%F %T'): python3 -> $(command -v python3) (rc of import: $(python3 -c 'import sys' >/dev/null 2>&1; echo $?)); python -> $(command -v python)"
  (cd "$WR/GXEMUL-SEC" && md5sum regress/gate_hygiene.sh regress/census_tokens.py tools/derive_hygiene_pins.sh | sed 's/^/   /')
  echo "== the classifier through Windows python, raw bytes of its first two output lines:"
  printf 'gdrom_cond_probe.py\ngdrom_data_probe.py\n' | python "$R/census_tokens.py" promptless "$R" | od -c | head -3 | sed 's/^/   /'
  echo "== report:"; ( GXROOT="$WR" bash "$D" ) > "$OUT/report.txt" 2>&1; echo "   rc=$?"
  grep -E '^(EXPECT_|promptless vs|NEW PROMPTLESS|GRANDFATHERED BUT|DERIVE_FAIL)' "$OUT/report.txt" | sed 's/^/   /'
  echo "   NEW names printed: $(awk '/^NEW PROMPTLESS/{f=1;next} /^[A-Z]/{f=0} f' "$OUT/report.txt" | grep -c .)   GONE names printed: $(awk '/^GRANDFATHERED BUT/{f=1;next} /^[A-Z]/{f=0} f' "$OUT/report.txt" | grep -c .)"
  echo "   CR bytes anywhere in the report: $(tr -cd '\r' < "$OUT/report.txt" | wc -c)"
  cp -p "$R/gate_hygiene.sh" "$WR/gate.before"
  echo "== --write (no edit; should be a no-op):"; ( GXROOT="$WR" bash "$D" --write ) > "$OUT/write.txt" 2>&1; echo "   rc=$?  $(grep -m1 -E '^(REFUSED|WRITTEN|DERIVE_FAIL)' "$OUT/write.txt" | cut -c1-120)"
  cmp -s "$WR/gate.before" "$R/gate_hygiene.sh" && echo "   gate byte-identical after --write" || { echo "   gate CHANGED by --write:"; diff "$WR/gate.before" "$R/gate_hygiene.sh" | cut -c1-120 | head -8 | sed 's/^/      /'; }
  echo "== --release gdrom_cond_probe.py (still promptless -> must be REFUSED):"; ( GXROOT="$WR" bash "$D" --release gdrom_cond_probe.py ) > "$OUT/release.txt" 2>&1; echo "   rc=$?  $(grep -m1 -E '^(REFUSED|RELEASED|DERIVE_FAIL)' "$OUT/release.txt" | cut -c1-120)"
  cp -p "$R/pcc2_width_probe.py" "$R/zz-legit_probe.py"
  echo "== --grandfather zz-legit_probe.py (a real NEW promptless probe -> must be accepted):"; ( GXROOT="$WR" bash "$D" --grandfather zz-legit_probe.py ) > "$OUT/grandfather.txt" 2>&1; echo "   rc=$?  $(grep -m1 -E '^(REFUSED|GRANDFATHERED:|DERIVE_FAIL)' "$OUT/grandfather.txt" | cut -c1-120)"
} >> "$S" 2>&1
rm -rf "$WR"
echo "GB_REPORT_DONE $(date '+%F %T')" >> "$S"
cat "$S"
