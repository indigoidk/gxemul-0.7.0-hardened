#!/bin/bash
# drv6.sh TAG [fresh] GROUP... -- W: WSL on /tmp; D: WSL on DrvFs (project-local); G: git-bash (project-local)
set -u
TAG=$1; FRESH=$2; shift 2
case "$TAG" in
  W) B=/mnt/c/DocumentNoSnc/cc/GXEMUL; WORK=/tmp/opusc6_w ;;
  D) B=/mnt/c/DocumentNoSnc/cc/GXEMUL; WORK=$B/_scratchpad/census0923/opus_c6/work_d ;;
  G) B=/c/DocumentNoSnc/cc/GXEMUL; WORK=$B/_scratchpad/census0923/opus_c6/work_g ;;
  *) echo "bad tag"; exit 2 ;;
esac
SRC=$B/GXEMUL-SEC/regress; FROZ=$B/_scratchpad/census0923/c6_frozen; OUT=$B/_scratchpad/census0923/opus_c6/out
TAB=$OUT/TABLE_$TAG.txt; GLIST=$OUT/GLIST.txt
mkdir -p "$OUT" "$WORK"
if [ "$FRESH" = fresh ]; then : > "$TAB"; [ "$TAG" = G ] && : > "$GLIST"; fi
. "$B/_scratchpad/census0923/opus_c6/lib6.sh"
echo "drv6 $TAG groups [$*] start $(date '+%F %T') bash $BASH_VERSION; python3 rc $(python3 -c 'import sys' >/dev/null 2>&1; echo $?); python rc $(python -c 'import sys' >/dev/null 2>&1; echo $?)" >> "$TAB"
[ -d "$WORK/_master" ] && [ "$FRESH" != fresh ] || master
for g in "$@"; do "c_$g"; done
echo "drv6 $TAG groups [$*] end $(date '+%F %T')" >> "$TAB"
echo DRV6_DONE
