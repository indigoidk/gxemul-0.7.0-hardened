#!/bin/bash
# extras6b.sh TAG -- BOM consequences at --grandfather / --release, and FIX-B (utf-8-sig) on scratch copies only
set -u
TAG=$1
case "$TAG" in
  W) B=/mnt/c/DocumentNoSnc/cc/GXEMUL; WORK=/tmp/opusc6_w ;;
  G) B=/c/DocumentNoSnc/cc/GXEMUL; WORK=$B/_scratchpad/census0923/opus_c6/work_g ;;
esac
SRC=$B/GXEMUL-SEC/regress; FROZ=$B/_scratchpad/census0923/c6_frozen; OUT=$B/_scratchpad/census0923/opus_c6/out
TAB=$OUT/TABLE_Y$TAG.txt; GLIST=$OUT/GLIST_Y.txt; : > "$TAB"; [ "$TAG" = G ] && : > "$GLIST"
. "$B/_scratchpad/census0923/opus_c6/lib6.sh"
[ -d "$WORK/_master" ] || master
bom() { { printf '\xef\xbb\xbf'; cat "$1"; } > "$1.tmp" && mv "$1.tmp" "$1"; }
fixB() { local t="$D/GXEMUL-SEC/tools/derive_hygiene_pins.sh"
    sed -i 's|    t = ast.parse(open(sys.argv\[1\], encoding="utf-8").read())|    t = ast.parse(open(sys.argv[1], encoding="utf-8-sig").read())|' "$t"
    echo "FIXB [$TAG] patch landed: $(grep -c 'encoding="utf-8-sig"' "$t")" >> "$TAB"; }
for V in F6d FIXB; do
    mk "S9b_$V"; [ $V = FIXB ] && fixB; cp -p "$R/lca_badval_probe.py" "$R/zz_bomplain_probe.py"; bom "$R/zz_bomplain_probe.py"
    run "S9b_$V.1"; run "S9b_$V.2" --grandfather zz_bomplain_probe.py; run "S9b_$V.3" --write; gate "S9b_$V.4"
    mk "S9c_$V"; [ $V = FIXB ] && fixB; trio "$R/gdrom_cond_probe.py" ":"; bom "$R/gdrom_cond_probe.py"
    run "S9c_$V.1"; run "S9c_$V.2" --release gdrom_cond_probe.py; run "S9c_$V.3" --write; gate "S9c_$V.4"
done
echo EXTRAS6B_DONE
