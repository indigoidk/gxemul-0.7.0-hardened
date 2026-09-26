#!/bin/bash
# Run a FROZEN copy of a probe against named binaries in the clone; one full log per binary under f2/<tag>/, one
# summary line per binary in f2/TABLE_<tag>.out.   usage: s4_run.sh <proto|shipped> <tag> <name>...
set -u
CL=/tmp/gxo549f2m
F2=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/fbctrlportkill_20260924/opus549_measured/f2
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
kind=$1; tag=$2; shift 2
case "$kind" in
    proto)   src=$F2/fbctrl_port_probe.f2proto.py ;;
    shipped) src=$SEC/regress/fbctrl_port_probe.py ;;
    *) echo "bad kind"; exit 2 ;;
esac
frozen=$CL/probe/frozen_${kind}_${tag}.py
cp "$src" "$frozen"
echo "# $(date +%T) kind=$kind probe=$(md5sum < "$frozen" | cut -c1-8) ($src)" > "$F2/TABLE_$tag.out"
mkdir -p "$F2/$tag"
cd "$CL/probe" || exit 2
for name in "$@"; do
    b=$CL/bins/gx_$name
    if [ ! -x "$b" ]; then echo "$name NO-BINARY" >> "$F2/TABLE_$tag.out"; continue; fi
    python3 -u "$frozen" "$b" > "$F2/$tag/$name.out" 2>&1
    rc=$?
    res=$(grep -E '^FBCTRLP_RESULT=' "$F2/$tag/$name.out" | head -1)
    ctl=$(grep -E '^FBCTRLP_CONTROL=' "$F2/$tag/$name.out" | head -1)
    dia=$(grep -E '^FBCTRLP_DIAG=' "$F2/$tag/$name.out" | head -1)
    done_=$(grep -cx 'FBCTRLP_DONE' "$F2/$tag/$name.out")
    red=$(grep -E '^  (FAIL|DRED) ' "$F2/$tag/$name.out" | sed -E 's/^  (FAIL|DRED) +//; s/ +got=.*//' | tr '\n' ';')
    printf '%-16s md5=%s rc=%s %s %s %s done=%s | %s\n' "$name" "$(md5sum < "$b" | cut -c1-8)" "$rc" "$res" "$ctl" "$dia" "$done_" "$red" >> "$F2/TABLE_$tag.out"
done
if cmp -s "$frozen" "$src"; then echo "# probe source unchanged during the run" >> "$F2/TABLE_$tag.out"; else echo "# NOTE: probe source CHANGED during the run; the frozen copy is what ran" >> "$F2/TABLE_$tag.out"; fi
echo "# $(date +%T) done" >> "$F2/TABLE_$tag.out"
cat "$F2/TABLE_$tag.out"
