#!/bin/bash
# SECTION 3 -- enumerate the deriver's refusals against its header.  Each case: fresh /tmp snapshot (SEC top-level +
# the 4 FROZEN files under review), an edit if needed, one deriver invocation, record rc + first REFUSED/DERIVE/usage
# line + whether the gate file changed.  /tmp only.  Helper edits are written by a tiny python appender to avoid
# backslash/heredoc hazards.
set -u
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
FROZ=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/c2_frozen
OUT=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/opus_c2/s3
W=/tmp/gxc2_s3
rm -rf "$W" "$OUT"; mkdir -p "$W/snap/GXEMUL-SEC/regress" "$W/snap/GXEMUL-SEC/tools" "$W/c" "$OUT"
S=$OUT/SUMMARY.txt; T=$OUT/TABLE.txt; : > "$S"; : > "$T"
(cd "$SEC/regress" && find . -maxdepth 1 -type f -exec cp -p {} "$W/snap/GXEMUL-SEC/regress/" \;)
cp -p "$SEC/tools/derive_hygiene_pins.sh" "$W/snap/GXEMUL-SEC/tools/"
cp -p "$FROZ/gate_hygiene.sh" "$W/snap/GXEMUL-SEC/regress/gate_hygiene.sh"
cp -p "$FROZ/census_tokens.py" "$W/snap/GXEMUL-SEC/regress/census_tokens.py"
cp -p "$FROZ/crime_width_probe.py" "$W/snap/GXEMUL-SEC/regress/crime_width_probe.py"
cp -p "$FROZ/derive_hygiene_pins.sh" "$W/snap/GXEMUL-SEC/tools/derive_hygiene_pins.sh"

# appender: append a python line to a probe file in a copy.  usage: app <copydir-regress> <file> <line>
app() { python3 -c 'import io,sys; p=sys.argv[1]; s=io.open(p,encoding="utf-8").read(); io.open(p,"w",encoding="utf-8").write(s+"\n"+sys.argv[2]+"\n")' "$1/$2" "$3"; }
mk() { rm -rf "$W/c/$1"; cp -a "$W/snap" "$W/c/$1"; }
rdir() { echo "$W/c/$1/GXEMUL-SEC/regress"; }
drv() {
  local tag=$1 lab=$2; shift 2
  local r=$W/c/$tag g; g=$(rdir "$tag")/gate_hygiene.sh
  [ -f "$g" ] && cp -p "$g" "$r/gate.before" || : > "$r/gate.before"
  ( GXROOT="$r" bash "$r/GXEMUL-SEC/tools/derive_hygiene_pins.sh" "$@" ) > "$OUT/$tag.drv" 2>&1; local rc=$?
  local first ch
  first=$(grep -m1 -E '^(REFUSED|DERIVE_FAIL|usage|WRITTEN|GRANDFATHERED|RELEASED)' "$OUT/$tag.drv" | cut -c1-150)
  if [ -f "$g" ] && cmp -s "$r/gate.before" "$g"; then ch="unchanged"; elif [ -f "$g" ]; then ch="CHANGED"; else ch="no-gate"; fi
  printf '%-11s rc=%-2s gate=%-9s %s\n' "$tag" "$rc" "$ch" "$first" >> "$T"
  { echo "=== $tag ($lab) :: args: $*"; echo "   rc=$rc gate=$ch"; sed 's/^/   /' "$OUT/$tag.drv" | head -8; echo; } >> "$S"
  LAST_RC=$rc
}
WHOLE='_c = lambda b: b.rstrip().endswith("GXemul>")'

# ---------- EXIT 2 ----------
mk r2_nogate; rm -f "$(rdir r2_nogate)/gate_hygiene.sh"; drv r2_nogate "no gate file" --write
mk r2_badarg;  drv r2_badarg "unknown first arg" --bogus
mk r2_extra;   drv r2_extra "extra args after --write" --write extra
mk r2_rulefmt; app "$(rdir r2_rulefmt)" arm_bdt_probe.py "$WHOLE"; drv r2_rulefmt "ruling bad format (no)" --write --ruling no
mk r2_rulechar; app "$(rdir r2_rulechar)" arm_bdt_probe.py "$WHOLE"; drv r2_rulechar "ruling forbidden char (quote)" --write --ruling '2026-09-23: a reason with a "quote" inside it here'

# ---------- EXIT 3 ----------
mk r3_enum; sed -i 's/^py_code() {/py_codeX() {/' "$(rdir r3_enum)/gate_hygiene.sh"; drv r3_enum "enumerator not found" --write
mk r3_asg;  sed -i '/^whole_files=\$(pty_driving/d' "$(rdir r3_asg)/gate_hygiene.sh"; drv r3_asg "assignment not found" --write
mk r3_denom; sed -i 's/^_ptylist=\$(find "\$HERE" -name "\*.py"/_ptylist=$(find "$HERE" -name "*.pyx"/' "$(rdir r3_denom)/gate_hygiene.sh"; drv r3_denom "denominator 0" --write

# ---------- EXIT 4 ----------
mk r4_nonames; drv r4_nonames "grandfather no names" --grandfather
mk r4_dup;     cp "$(rdir r4_dup)/pcc2_width_probe.py" "$(rdir r4_dup)/zz_dupe_probe.py"; drv r4_dup "grandfather dup name" --grandfather zz_dupe_probe.py zz_dupe_probe.py
mk r4_already; drv r4_already "grandfather already-listed" --grandfather gdrom_cond_probe.py
mk r4_notnew;  drv r4_notnew "grandfather a prompt-detecting file" --grandfather arm_endian_probe.py
mk r4_notgone; drv r4_notgone "release a still-promptless name" --release gdrom_cond_probe.py

# ---------- EXIT 5 ----------
mk r5_disagree; sed -i 's/if echo is not None and echo not in resp:/if False and echo not in resp:/' "$(rdir r5_disagree)/mips_rounding_probe.py"; drv r5_disagree "#392 counts disagree" --write
mk r5_gone; app "$(rdir r5_gone)" gdrom_cond_probe.py '_ready = lambda b: b.rstrip().endswith("GXemul>")'; drv r5_gone "grandfathered no longer promptless" --write
mk r5_bare; app "$(rdir r5_bare)" mips_rounding_probe.py '_b = lambda b: b.endswith(">")'; drv r5_bare "bare endswith grew" --write

# ---------- RULING EDGE CASES (brief Section 3) ----------
mk e1_wsrule; app "$(rdir e1_wsrule)" arm_bdt_probe.py "$WHOLE"; drv e1_wsrule "ruling whitespace-only reason" --write --ruling "2026-09-23:                     "
{ echo "   RULING lines in gate after e1: $(grep -c '^#  RULING' "$(rdir e1_wsrule)/gate_hygiene.sh")"
  echo "   the RULING line(s) written:"; grep -n '^#  RULING' "$(rdir e1_wsrule)/gate_hygiene.sh" | sed 's/^/     /'; } >> "$S"
mk e2_noneed; drv e2_noneed "ruling on a no-op write" --write --ruling "2026-09-23: this decision changes nothing at all"
echo "   RULING lines in gate after e2 (expect 0): $(grep -c '^#  RULING' "$(rdir e2_noneed)/gate_hygiene.sh")" >> "$S"
mk e3_two; drv e3_two "two --ruling flags" --write --ruling "2026-09-23: first ruling reason here" --ruling "2026-09-23: second ruling reason"
mk e4_nl; app "$(rdir e4_nl)" arm_bdt_probe.py "$WHOLE"
NL=$'2026-09-23: first line of the ruling\nmalicious_second_line=here'
drv e4_nl "ruling with a newline" --write --ruling "$NL"
{ echo "   gate parses after e4_nl? $(cd "$(rdir e4_nl)" && bash -n gate_hygiene.sh 2>&1 && echo 'bash -n OK' || echo 'bash -n FAIL')"
  echo "   RULING lines after e4: $(grep -c '^#  RULING' "$(rdir e4_nl)/gate_hygiene.sh")"
  echo "   context around any RULING line:"; grep -n -A2 '^#  RULING' "$(rdir e4_nl)/gate_hygiene.sh" | sed 's/^/     /'; } >> "$S"

rm -rf "$W"
echo "S3_DONE $(date '+%F %T')" >> "$S"; echo "S3_DONE" >> "$T"
cat "$T"
