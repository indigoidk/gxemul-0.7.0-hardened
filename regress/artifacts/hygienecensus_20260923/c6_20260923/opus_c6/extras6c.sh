#!/bin/bash
# extras6c.sh TAG -- the REAL BOM witness from artifacts/, copied to regress/ top level; F6d vs FIX-B (scratch only)
set -u
TAG=$1
case "$TAG" in
  W) B=/mnt/c/DocumentNoSnc/cc/GXEMUL; WORK=/tmp/opusc6_w ;;
  G) B=/c/DocumentNoSnc/cc/GXEMUL; WORK=$B/_scratchpad/census0923/opus_c6/work_g ;;
esac
SRC=$B/GXEMUL-SEC/regress; FROZ=$B/_scratchpad/census0923/c6_frozen; OUT=$B/_scratchpad/census0923/opus_c6/out
TAB=$OUT/TABLE_Z$TAG.txt; GLIST=$OUT/GLIST_Z.txt; : > "$TAB"; [ "$TAG" = G ] && : > "$GLIST"
. "$B/_scratchpad/census0923/opus_c6/lib6.sh"
[ -d "$WORK/_master" ] || master
AGY=$SRC/artifacts/wdcaltdigin/agy_altdigin_witness_20260911.py
fixB() { local t="$D/GXEMUL-SEC/tools/derive_hygiene_pins.sh"
    sed -i 's|    t = ast.parse(open(sys.argv\[1\], encoding="utf-8").read())|    t = ast.parse(open(sys.argv[1], encoding="utf-8-sig").read())|' "$t"
    echo "FIXB [$TAG] patch landed: $(grep -c 'encoding="utf-8-sig"' "$t")" >> "$TAB"; }
for V in F6d FIXB; do
    mk "S17_$V"; [ $V = FIXB ] && fixB; cp -p "$AGY" "$R/"
    echo "S17_$V [$TAG] first bytes: $(head -c3 "$R/agy_altdigin_witness_20260911.py" | od -An -tx1 | tr -s ' ') md5 $(md5sum < "$R/agy_altdigin_witness_20260911.py" | cut -c1-8)" >> "$TAB"
    run "S17_$V.1"; run "S17_$V.2" --write; run "S17_$V.3" --grandfather agy_altdigin_witness_20260911.py
    run "S17_$V.4" --write; gate "S17_$V.5"
done
echo EXTRAS6C_DONE
