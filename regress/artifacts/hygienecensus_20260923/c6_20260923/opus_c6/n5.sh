#!/bin/bash
set -u
TAG=$1
case "$TAG" in
  W) B=/mnt/c/DocumentNoSnc/cc/GXEMUL; WORK=/tmp/opusc6_w ;;
  G) B=/c/DocumentNoSnc/cc/GXEMUL; WORK=$B/_scratchpad/census0923/opus_c6/work_g ;;
esac
SRC=$B/GXEMUL-SEC/regress; FROZ=$B/_scratchpad/census0923/c6_frozen; OUT=$B/_scratchpad/census0923/opus_c6/out
TAB=$OUT/TABLE_N5$TAG.txt; : > "$TAB"
. "$B/_scratchpad/census0923/opus_c6/lib6.sh"
[ -d "$WORK/_master" ] || master
echo "env [$TAG]: PYTHONOPTIMIZE=[${PYTHONOPTIMIZE-unset}] PYTHONWARNINGS=[${PYTHONWARNINGS-unset}] PYTHONUTF8=[${PYTHONUTF8-unset}] PYTHONIOENCODING=[${PYTHONIOENCODING-unset}] BASH_ENV=[${BASH_ENV-unset}] MSYS_NO_PATHCONV=[${MSYS_NO_PATHCONV-unset}]" >> "$TAB"
mk N5; cp -p "$R/luna_absentcpu_probe.py" "$R/zz_canary_call.py"; cp -p "$R/lca_badval_probe.py" "$R/zz_canary_absent.py"
run N5.1
cat "$TAB"
