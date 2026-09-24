#!/bin/bash
# SECTION 3b -- ruling-write edge cases with a PROPER whole-buffer receiver (ending in "buf") so NEED is non-empty
# and the ruling path is actually exercised.  Also confirms r5_gone's REFUSED line and shows a valid ruling writing a
# RULING comment line.  /tmp only.
set -u
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
FROZ=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/c2_frozen
OUT=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/opus_c2/s3b
W=/tmp/gxc2_s3b
rm -rf "$W" "$OUT"; mkdir -p "$W/snap/GXEMUL-SEC/regress" "$W/snap/GXEMUL-SEC/tools" "$W/c" "$OUT"
S=$OUT/SUMMARY.txt; : > "$S"
(cd "$SEC/regress" && find . -maxdepth 1 -type f -exec cp -p {} "$W/snap/GXEMUL-SEC/regress/" \;)
cp -p "$SEC/tools/derive_hygiene_pins.sh" "$W/snap/GXEMUL-SEC/tools/"
cp -p "$FROZ/gate_hygiene.sh" "$W/snap/GXEMUL-SEC/regress/gate_hygiene.sh"
cp -p "$FROZ/census_tokens.py" "$W/snap/GXEMUL-SEC/regress/census_tokens.py"
cp -p "$FROZ/derive_hygiene_pins.sh" "$W/snap/GXEMUL-SEC/tools/derive_hygiene_pins.sh"
app() { python3 -c 'import io,sys; p=sys.argv[1]; s=io.open(p,encoding="utf-8").read(); io.open(p,"w",encoding="utf-8").write(s+"\n"+sys.argv[2]+"\n")' "$1/$2" "$3"; }
mk() { rm -rf "$W/c/$1"; cp -a "$W/snap" "$W/c/$1"; }
rdir() { echo "$W/c/$1/GXEMUL-SEC/regress"; }
drv() { local tag=$1; shift; ( GXROOT="$W/c/$tag" bash "$W/c/$tag/GXEMUL-SEC/tools/derive_hygiene_pins.sh" "$@" ) > "$OUT/$tag.drv" 2>&1; echo $?; }
# a REAL whole-buffer site (receiver ends in "buf") in a NON-allowlisted pty probe -> whole_full 3->4, whole_files changes -> NEED set
WHOLE='_c = lambda mybuf: mybuf.rstrip().endswith("GXemul>")'

echo "=== confirm the whole-buffer edit actually registers (receiver ends in buf)" >> "$S"
mk probe; app "$(rdir probe)" luna_absentcpu_probe.py "$WHOLE"
echo "  census_tokens whole over luna: $(printf 'luna_absentcpu_probe.py\n' | python3 "$(rdir probe)/census_tokens.py" whole "$(rdir probe)")" >> "$S"

echo "=== E-noruling: real whole change, --write with NO ruling -> REFUSED exit 5" >> "$S"
mk e0; app "$(rdir e0)" luna_absentcpu_probe.py "$WHOLE"
rc=$(drv e0 --write); echo "  rc=$rc  $(grep -m1 REFUSED "$OUT/e0.drv" | cut -c1-160)" >> "$S"

echo "=== E1: real whole change, --write --ruling with a WHITESPACE-ONLY reason that passes the format regex" >> "$S"
mk e1; app "$(rdir e1)" luna_absentcpu_probe.py "$WHOLE"
before=$(md5sum "$(rdir e1)/gate_hygiene.sh" | cut -c1-8)
rc=$(drv e1 --write --ruling "2026-09-23:                     ")
after=$(md5sum "$(rdir e1)/gate_hygiene.sh" | cut -c1-8)
{ echo "  rc=$rc  gate $before->$after  $(grep -m1 WRITTEN "$OUT/e1.drv" | cut -c1-80)"
  echo "  RULING lines: $(grep -c '^#  RULING' "$(rdir e1)/gate_hygiene.sh")"
  grep -n '^#  RULING' "$(rdir e1)/gate_hygiene.sh" | cat -A | sed 's/^/    /'
  echo "  new pins:"; grep -nE '^(EXPECT_WHOLE_FULL|WHOLE_FULL_FILES)=' "$(rdir e1)/gate_hygiene.sh" | sed 's/^/    /'; } >> "$S"

echo "=== E1b: same but a VALID descriptive ruling (control: what a good RULING line looks like)" >> "$S"
mk e1b; app "$(rdir e1b)" luna_absentcpu_probe.py "$WHOLE"
rc=$(drv e1b --write --ruling "2026-09-23: owner allowlisted a 4th whole-buffer site pending conversion")
{ echo "  rc=$rc  RULING lines: $(grep -c '^#  RULING' "$(rdir e1b)/gate_hygiene.sh")"
  grep -n -B0 '^#  RULING' "$(rdir e1b)/gate_hygiene.sh" | sed 's/^/    /'; } >> "$S"

echo "=== E4: real whole change, --write --ruling containing a NEWLINE (injection check)" >> "$S"
mk e4; app "$(rdir e4)" luna_absentcpu_probe.py "$WHOLE"
NL=$'2026-09-23: legitimate looking first line here\nEXPECT_WHOLE_FULL=999'
rc=$(drv e4 --write --ruling "$NL")
{ echo "  rc=$rc  $(grep -m1 -E 'REFUSED|WRITTEN' "$OUT/e4.drv" | cut -c1-90)"
  echo "  gate parses (bash -n)? $(cd "$(rdir e4)" && bash -n gate_hygiene.sh 2>&1 && echo OK || echo FAIL)"
  echo "  RULING lines: $(grep -c '^#  RULING' "$(rdir e4)/gate_hygiene.sh")"
  echo "  did a spurious EXPECT_WHOLE_FULL=999 land?  $(grep -c '^EXPECT_WHOLE_FULL=999' "$(rdir e4)/gate_hygiene.sh")"
  echo "  context around RULING:"; grep -n -A3 '^#  RULING' "$(rdir e4)/gate_hygiene.sh" | cat -A | sed 's/^/    /'; } >> "$S"

echo "=== r5_gone: full deriver output (confirm the REFUSED line, not just the report)" >> "$S"
mk g1; app "$(rdir g1)" gdrom_cond_probe.py '_ready = lambda gbuf: gbuf.rstrip().endswith("GXemul>")'
rc=$(drv g1 --write); { echo "  rc=$rc"; grep -E '^REFUSED' "$OUT/g1.drv" | sed 's/^/    /'; } >> "$S"

rm -rf "$W"
echo "S3B_DONE $(date '+%F %T')" >> "$S"
cat "$S"
