#!/bin/bash
# Score named binaries with a FROZEN, cmp-verified copy of the shipped 73-row probe.  usage: c3_run.sh <tag> <name>...
set -u
CL=/tmp/gxo549cf2
C=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/fbctrlportkill_20260924/opus549_measured/close2
SRC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/fbctrl_port_probe.py
tag=$1; shift
FZ=$CL/probe/frozen_$tag.py
cp "$SRC" "$FZ"
T=$C/TABLE_$tag.out
echo "# $(date +%T) probe md5=$(md5sum < "$FZ" | cut -c1-8) (shipped regress/fbctrl_port_probe.py, frozen copy)" > "$T"
mkdir -p "$C/$tag"
cd "$CL/probe" || exit 2
for name in "$@"; do
    b=$CL/bins/gx_$name
    python3 -u "$FZ" "$b" > "$C/$tag/$name.out" 2>&1
    rc=$?
    red=$(grep -E '^  FAIL ' "$C/$tag/$name.out" | sed -E 's/^  FAIL +//; s/ +got=.*//' | tr '\n' ';')
    printf '%-12s md5=%s rc=%s %s %s done=%s | %s\n' "$name" "$(md5sum < "$b" | cut -c1-8)" "$rc" \
        "$(grep -E '^FBCTRLP_RESULT=' "$C/$tag/$name.out")" "$(grep -E '^FBCTRLP_CONTROL=' "$C/$tag/$name.out")" \
        "$(grep -cx FBCTRLP_DONE "$C/$tag/$name.out")" "$red" >> "$T"
done
cmp -s "$FZ" "$SRC" && echo "# probe source unchanged during the run" >> "$T"
echo "# $(date +%T) done" >> "$T"
cat "$T"
