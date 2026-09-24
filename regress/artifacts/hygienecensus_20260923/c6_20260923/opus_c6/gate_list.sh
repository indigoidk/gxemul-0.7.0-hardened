#!/bin/bash
# gate_list.sh LISTFILE -- run under WSL: the gate on every tree the git-bash driver left (paths /c/... -> /mnt/c/...)
set -u
OUT=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/opus_c6/out; TAB=${2:-$OUT/TABLE_G.txt}
while read -r lab d; do
  d=$(printf '%s' "$d" | sed 's#^/c/#/mnt/c/#'); o="$OUT/G_$lab.gate.out"; L=$(mktemp -d)
  ( cd "$d/GXEMUL-SEC/regress" && LOGDIR="$L" bash ./gate_hygiene.sh ) > "$o" 2>&1; rm -rf "$L"
  sed 's/\x1b\[[0-9;]*m//g' "$o" | grep -E '^\s*(FAIL|ok)' | grep -E 'readiness|whole-buffer' > "$o.rows"
  echo "$lab [G->WSLgate] GATE $(grep -cE '^\s*FAIL' "$o.rows") FAIL of $(wc -l < "$o.rows"): $(grep -E '^\s*FAIL' "$o.rows" | sed 's/^ *FAIL *//; s/  */ /g' | cut -c1-60 | tr '\n' ';')" >> "$TAB"
done < "$1"
echo GATE_LIST_DONE
