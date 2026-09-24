#!/bin/bash
# K16 on the REAL git-bash environment of this machine (python3 = the Windows Store stub; python = a working 3.12).
# The deriver's own interpreter probe skips the stub and uses `python` for its writer, but the gate code it extracts and
# evaluates calls a literal `python3` for the token census.  Run the F4 deriver under git-bash on a git-bash /tmp copy:
# report, --write, --release of a probe that IS still promptless; then grade the SAME copy with the gate under WSL.
set -u
[ -f /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/gate_hygiene.sh ] || { echo "K16GB_FAIL: not git-bash layout"; exit 9; }
SEC=/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
FROZ=/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/c4_frozen
OUT=/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/opus_c4/k16_gitbash
WR=/tmp/gxc4_k16gb
rm -rf "$WR" "$OUT"; mkdir -p "$WR/GXEMUL-SEC/regress" "$WR/GXEMUL-SEC/tools" "$OUT"; S=$OUT/SUMMARY.txt; : > "$S"
(cd "$SEC/regress" && find . -maxdepth 1 -type f -exec cp -p {} "$WR/GXEMUL-SEC/regress/" \;)
cp -p "$FROZ/gate_hygiene.sh" "$FROZ/census_tokens.py" "$WR/GXEMUL-SEC/regress/"; cp -p "$FROZ/derive_hygiene_pins.sh" "$WR/GXEMUL-SEC/tools/"
D=$WR/GXEMUL-SEC/tools/derive_hygiene_pins.sh; G=$WR/GXEMUL-SEC/regress/gate_hygiene.sh
listn() { tr -d '\r' < "$G" | awk '/^GRANDFATHERED_PROMPTLESS="/{p=1} p{print} p&&/"$/&&!/^GRANDFATHERED_PROMPTLESS="[^"]*$/{exit}' | sed 's/^GRANDFATHERED_PROMPTLESS="//; s/"$//' | wc -w; }
{ echo "K16 on git-bash $(date '+%F %T'): python3 -> $(command -v python3); python -> $(command -v python)"
  echo "   copy at $(cygpath -w "$WR")"
  (cd "$WR/GXEMUL-SEC" && md5sum regress/gate_hygiene.sh regress/census_tokens.py tools/derive_hygiene_pins.sh | sed 's/^/   /')
  echo "== report (git-bash):"; ( GXROOT="$WR" bash "$D" ) > "$OUT/report.txt" 2>&1; echo "   rc=$?"
  grep -E '^(promptless vs|EXPECT_WHOLE_FULL|EXPECT_PTY|GRANDFATHERED BUT|NEW PROMPTLESS|DERIVE_FAIL)' "$OUT/report.txt" | sed 's/^/   /'
  echo "   GONE names the report asks to --release: $(awk '/^GRANDFATHERED BUT NO LONGER PROMPTLESS/{f=1;next} /^[A-Z]/{f=0} f' "$OUT/report.txt" | grep -c .)"
  echo "   stderr lines naming the Store stub: $(grep -c 'Python was not found' "$OUT/report.txt")"
  echo "== --write (git-bash):"; ( GXROOT="$WR" bash "$D" --write ) > "$OUT/write.txt" 2>&1; echo "   rc=$?  $(grep -m1 -E '^(REFUSED|WRITTEN|DERIVE_FAIL)' "$OUT/write.txt" | cut -c1-110)"
  echo "== --release gdrom_cond_probe.py (git-bash; the probe is STILL promptless):"; b=$(listn)
  ( GXROOT="$WR" bash "$D" --release gdrom_cond_probe.py ) > "$OUT/release.txt" 2>&1
  echo "   rc=$?  $(grep -m1 -E '^(REFUSED|RELEASED|DERIVE_FAIL)' "$OUT/release.txt" | cut -c1-110)   list $b -> $(listn) names"
  echo "   gate file now LF-only? CR bytes in it: $(tr -cd '\r' < "$G" | wc -c)"
} >> "$S"
cat > "$OUT/wsl_gate.sh" <<'EOF'
#!/bin/bash
W=/mnt/c/Users/User00/AppData/Local/Temp/gxc4_k16gb
( cd "$W/GXEMUL-SEC/regress" && LOGDIR=/tmp/gxc4_k16gb_logs bash ./gate_hygiene.sh ) 2>&1 | sed 's/\x1b\[[0-9;]*m//g' \
    | grep -E '^\s*FAIL.*(readiness|whole-buffer)' | sed 's/^\s*/   /'
rm -rf /tmp/gxc4_k16gb_logs; echo "   (end of FAIL rows)"
EOF
{ echo "== the SAME copy graded by the gate under WSL (working python3) after the git-bash --release:"
  MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash /mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/opus_c4/k16_gitbash/wsl_gate.sh; } >> "$S"
rm -rf "$WR"
echo "K16_GITBASH_DONE $(date '+%F %T')" >> "$S"
cat "$S"
