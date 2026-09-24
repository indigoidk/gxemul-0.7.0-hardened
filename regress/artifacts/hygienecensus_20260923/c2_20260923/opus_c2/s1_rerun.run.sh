#!/bin/bash
# SECTION 1 -- re-run the Opus seat's 47 cases against the FINAL FROZEN files (c2_frozen).
# Snapshot = SEC regress top-level + tools/derive, then OVERWRITE the 4 files-under-review with the exact frozen bytes,
# so the measured gate/census/deriver/crime_width are byte-for-byte the c2_frozen copies (md5 6a9cb517/662ce35a/cbb8488d/a0af7c92).
# /tmp copies only.  Reuses edits.py (unchanged) and the main loop's control shape.
set -u
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
FROZ=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/c2_frozen
EDITS=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/opus_f2/edits.py
OUT=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/opus_c2/s1
W=/tmp/gxc2_s1
rm -rf "$W" "$OUT"; mkdir -p "$W/snap/GXEMUL-SEC/regress" "$W/snap/GXEMUL-SEC/tools" "$W/c" "$OUT"
S=$OUT/SUMMARY.txt; T=$OUT/TABLE.txt; : > "$S"; : > "$T"
(cd "$SEC/regress" && find . -maxdepth 1 -type f -exec cp -p {} "$W/snap/GXEMUL-SEC/regress/" \;)
cp -p "$SEC/tools/derive_hygiene_pins.sh" "$W/snap/GXEMUL-SEC/tools/"
# overwrite the four under review with the exact frozen bytes
cp -p "$FROZ/gate_hygiene.sh"          "$W/snap/GXEMUL-SEC/regress/gate_hygiene.sh"
cp -p "$FROZ/census_tokens.py"         "$W/snap/GXEMUL-SEC/regress/census_tokens.py"
cp -p "$FROZ/crime_width_probe.py"     "$W/snap/GXEMUL-SEC/regress/crime_width_probe.py"
cp -p "$FROZ/derive_hygiene_pins.sh"   "$W/snap/GXEMUL-SEC/tools/derive_hygiene_pins.sh"
{ echo "SECTION 1 re-run vs FINAL FROZEN -- $(date '+%F %T')"
  (cd "$W/snap/GXEMUL-SEC" && md5sum regress/gate_hygiene.sh regress/census_tokens.py tools/derive_hygiene_pins.sh regress/crime_width_probe.py)
  echo "expected: 6a9cb517 gate / 662ce35a census / cbb8488d deriver / a0af7c92 crime_width"; } >> "$S"

mk() { rm -rf "$W/c/$1"; cp -a "$W/snap" "$W/c/$1"; }
rdir() { echo "$W/c/$1/GXEMUL-SEC/regress"; }
gate() {
    local tag=$1 lab=$2 d; d=$(rdir "$1"); mkdir -p "$W/c/$1/logs_$lab"
    ( cd "$d" && LOGDIR="$W/c/$1/logs_$lab" bash ./gate_hygiene.sh ) > "$OUT/$tag.$lab.out" 2>&1
    grep -E 'readiness|whole-buffer' "$OUT/$tag.$lab.out" | sed 's/\x1b\[[0-9;]*m//g' > "$OUT/$tag.$lab.rows"
    local nf nr; nf=$(grep -cE '^\s*FAIL' "$OUT/$tag.$lab.rows"); nr=$(grep -cE '^\s*(ok|FAIL)' "$OUT/$tag.$lab.rows")
    { echo "   gate [$lab]: $nf FAIL of $nr readiness rows"; grep -E '^\s*FAIL' "$OUT/$tag.$lab.rows" | sed 's/^\s*/      /'; } >> "$S"
    LAST_NF=$nf
}
drv() {
    local tag=$1 lab=$2; shift 2
    local r=$W/c/$tag g; g=$(rdir "$tag")/gate_hygiene.sh
    cp -p "$g" "$r/gate.before.$lab"
    ( GXROOT="$r" bash "$r/GXEMUL-SEC/tools/derive_hygiene_pins.sh" "$@" ) > "$OUT/$tag.$lab.drv" 2>&1; local rc=$?
    { echo "   deriver [$lab] $* -> rc=$rc"
      grep -E '^(REFUSED|WRITTEN|DERIVE_FAIL|GRANDFATHERED|RELEASED)' "$OUT/$tag.$lab.drv" | cut -c1-240 | sed 's/^/      /'
      if cmp -s "$r/gate.before.$lab" "$g"; then echo "      gate file UNCHANGED"
      else echo "      gate file CHANGED"; fi; } >> "$S"
    LAST_RC=$rc
}
begin() {
    mk "$1"
    { echo; echo "===== $1  $(python3 "$EDITS" --desc "$1" 2>/dev/null || echo 'unmodified copy')"; } >> "$S"
    if [ "$1" != real ]; then
        python3 "$EDITS" "$1" "$(rdir "$1")" > "$OUT/$1.edit" 2>&1 || { echo "   EDIT FAILED:"; sed 's/^/      /' "$OUT/$1.edit"; } >> "$S"
    fi
}
row() { printf '%-7s %s\n' "$1" "$2" >> "$T"; }
v() { [ "$1" -eq 0 ] && echo PASS || echo "red $1"; }

begin real; gate real before; b=$LAST_NF; drv real report; drv real write --write; w=$LAST_RC; gate real after
row real "before $(v $b); --write rc=$w; after $(v $LAST_NF)"
for c in e_c1 e_e1 e_e2 e_e3 e_e4 e_e5 e_e6 e_e7 e_e9 e_e14 n1a n1b n1c n1d n3a n3b n3c n3d n3e n3f n3g n3h n3i n3j n3m n3k n3k2 n4a n10 clone; do
    begin "$c"; gate "$c" gate; row "$c" "$(v $LAST_NF)"
done
for c in e_dL1 e_dL2 e_dL3 e_dL5 n2a n2b n5a n6 n8 n8b n11; do
    begin "$c"; gate "$c" before; b=$LAST_NF; drv "$c" write --write; w=$LAST_RC; gate "$c" after
    row "$c" "before $(v $b); --write rc=$w; after $(v $LAST_NF)"
done
begin n5b; gate n5b before; b=$LAST_NF
drv n5b write1 --write; w1=$LAST_RC; drv n5b grandfather --grandfather gdrom_cond_probe.py; g1=$LAST_RC
drv n5b write2 --write; w2=$LAST_RC; gate n5b after; a=$LAST_NF; drv n5b release --release gdrom_cond_probe.py; rl=$LAST_RC
row n5b "before $(v $b); --write rc=$w1; --grandfather rc=$g1; --write rc=$w2; after $(v $a); --release rc=$rl"
begin n7; gate n7 before; b=$LAST_NF
drv n7 write0 --write; w0=$LAST_RC; drv n7 write_no --write --ruling no; wn=$LAST_RC
drv n7 write_ok --write --ruling "2026-09-23: control case only, never a real ruling"; wk=$LAST_RC
gate n7 after; a=$LAST_NF
row n7 "before $(v $b); --write rc=$w0; --ruling no rc=$wn; --ruling <dated> rc=$wk; after $(v $a); RULING lines $(grep -c '^#  RULING ' "$(rdir n7)/gate_hygiene.sh")"
begin n9; gate n9 before; b=$LAST_NF
drv n9 write1 --write; w1=$LAST_RC; drv n9 release --release gdrom_cond_probe.py; r1=$LAST_RC
drv n9 write2 --write; w2=$LAST_RC; gate n9 after; a=$LAST_NF
row n9 "before $(v $b); --write rc=$w1; --release rc=$r1; --write rc=$w2; after $(v $a)"
begin n12; gate n12 before; b=$LAST_NF; drv n12 write --write; w=$LAST_RC; gate n12 after
row n12 "before $(v $b); --write rc=$w; after $(v $LAST_NF)"
rm -rf "$W"
echo "S1_DONE $(date '+%F %T')" >> "$S"; echo "S1_DONE" >> "$T"
cat "$T"
