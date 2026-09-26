#!/bin/bash
set -u
CL=/tmp/gxo549close
C=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/fbctrlportkill_20260924/opus549_measured/close
SRC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/fbctrl_port_probe.py
cp "$SRC" "$CL/probe/frozen_x.py"; cp "$C/close_rows_proto.py" "$CL/probe/xrows.frozen.py"
T=$C/TABLE_xrows.out
echo "# $(date +%T) shipped probe (imported) md5=$(md5sum < $CL/probe/frozen_x.py | cut -c1-8)  xrows md5=$(md5sum < $CL/probe/xrows.frozen.py | cut -c1-8)" > "$T"
mkdir -p "$C/xrows"
cd "$CL/probe" || exit 2
for name in "$@"; do
    python3 -u xrows.frozen.py "$CL/bins/gx_$name" "$CL/probe/frozen_x.py" > "$C/xrows/$name.out" 2>&1
    rc=$?
    red=$(grep -E '^  FAIL ' "$C/xrows/$name.out" | sed -E 's/^  FAIL +//; s/ +got=.*//' | tr '\n' ';')
    printf '%-12s rc=%s %s done=%s | %s\n' "$name" "$rc" "$(grep -E '^XROWS_RESULT=' "$C/xrows/$name.out")" "$(grep -cx XROWS_DONE "$C/xrows/$name.out")" "$red" >> "$T"
done
echo "# $(date +%T) done" >> "$T"
cat "$T"
