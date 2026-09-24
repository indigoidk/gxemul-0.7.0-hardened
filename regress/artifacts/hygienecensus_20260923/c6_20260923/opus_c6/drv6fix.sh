#!/bin/bash
# drv6fix.sh TAG fresh|keep GROUP... -- drv6.sh with FIX-A + FIX-B applied to the master's deriver (scratch copies only)
set -u
TAG=$1; FRESH=$2; shift 2
case "$TAG" in
  W) B=/mnt/c/DocumentNoSnc/cc/GXEMUL; WORK=/tmp/opusc6_wf ;;
  G) B=/c/DocumentNoSnc/cc/GXEMUL; WORK=$B/_scratchpad/census0923/opus_c6/work_gf ;;
esac
SRC=$B/GXEMUL-SEC/regress; FROZ=$B/_scratchpad/census0923/c6_frozen; OUT=$B/_scratchpad/census0923/opus_c6/outfix
TAB=$OUT/TABLE_$TAG.txt; GLIST=$OUT/GLIST.txt
mkdir -p "$OUT" "$WORK"
if [ "$FRESH" = fresh ]; then : > "$TAB"; [ "$TAG" = G ] && : > "$GLIST"; fi
. "$B/_scratchpad/census0923/opus_c6/lib6.sh"
if [ "$FRESH" = fresh ] || [ ! -d "$WORK/_master" ]; then
  master; t="$WORK/_master/GXEMUL-SEC/tools/derive_hygiene_pins.sh"
  sed -i 's|^            if \[ -e "\$HERE/\$f" \]; then$|            if printf '"'"'%s\n'"'"' "$_ptylist" \| grep -qxF -- "$f"; then|' "$t"
  sed -i 's|    t = ast.parse(open(sys.argv\[1\], encoding="utf-8").read())|    t = ast.parse(open(sys.argv[1], encoding="utf-8-sig").read())|' "$t"
  echo "[$TAG] FIXED master deriver $(md5sum "$t" | cut -c1-8): FIX-A $(grep -c '"$_ptylist" | grep -qxF -- "$f"; then' "$t") FIX-B $(grep -c 'utf-8-sig' "$t"); diff vs frozen: $(diff "$FROZ/derive_hygiene_pins.sh" "$t" | grep -c '^[<>]') lines" >> "$TAB"
fi
for g in "$@"; do "c_$g"; done
echo DRV6FIX_DONE
