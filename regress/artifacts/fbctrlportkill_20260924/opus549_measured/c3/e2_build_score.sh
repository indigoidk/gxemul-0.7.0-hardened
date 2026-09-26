#!/bin/bash
# Build each var/v/<name>.c in the clone, score with a frozen copy of v5; clone-local sentinel; restore + md5 verify.
set -u
CL=/tmp/gxo549c3
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
C=$SEC/regress/artifacts/fbctrlportkill_20260924/opus549_measured/c3
FIXMD5=b5b99e6d1e5fd077c8cf782d8c6a6a2c
FZ=$CL/probe/frozen_v5.py
cp "$SEC/regress/fbctrl_port_probe.py" "$FZ"
cmp "$FZ" "$SEC/regress/fbctrl_port_probe.py" && echo "frozen v5 == SEC ($(md5sum < "$FZ" | cut -c1-8))"
T=$C/TABLE_c3.out
echo "# $(date +%T) v5 probe md5=$(md5sum < "$FZ" | cut -c1-8); base fix md5 $FIXMD5" > "$T"
mkdir -p "$C/logs"
cd "$CL" || exit 2
echo "src/devices/dev_fbctrl.c: verifying-pass floor edits, started $(date +%T)" > "$CL/.MUTANT"
for name in "$@"; do
    cp "var/v/$name.c" src/devices/dev_fbctrl.c || { echo "$name NO-SRC"; continue; }
    rm -f src/devices/dev_fbctrl.o
    make -j4 > "var/make_$name.log" 2>&1
    rc=$?
    if [ "$rc" != 0 ] || [ ! gxemul -nt src/devices/dev_fbctrl.c ] || [ ! src/devices/dev_fbctrl.o -nt src/devices/dev_fbctrl.c ]; then
        echo "$name BUILD-FAILED rc=$rc" | tee -a "$T"; tail -3 "var/make_$name.log"; continue
    fi
    m=$(md5sum < gxemul | cut -c1-8)
    python3 -u "$FZ" gxemul > "$C/logs/$name.out" 2>&1
    prc=$?
    res=$(grep -E '^FBCTRLP_RESULT=' "$C/logs/$name.out"); ctl=$(grep -E '^FBCTRLP_CONTROL=' "$C/logs/$name.out")
    red=$(grep -E '^  FAIL ' "$C/logs/$name.out" | sed -E 's/^  FAIL +//; s/ +got=.*//' | tr '\n' ';')
    printf '%-14s md5=%s prc=%s %s %s | %s\n' "$name" "$m" "$prc" "$res" "$ctl" "${red:0:200}" >> "$T"
done
cp "$SEC/src/devices/dev_fbctrl.c" src/devices/dev_fbctrl.c
rm -f src/devices/dev_fbctrl.o
make -j4 > var/make_restore.log 2>&1
m=$(md5sum < gxemul | cut -d' ' -f1)
if cmp -s src/devices/dev_fbctrl.c "$SEC/src/devices/dev_fbctrl.c" && [ gxemul -nt src/devices/dev_fbctrl.c ] && [ "$m" = "$FIXMD5" ]; then
    rm -f "$CL/.MUTANT"; echo "RESTORED: cmp SEC clean, fresh, md5 $m == fix; sentinel cleared" | tee -a "$T"
else
    echo "RESTORE NOT VERIFIED md5 $m -- sentinel LEFT" | tee -a "$T"
fi
cmp -s "$FZ" "$SEC/regress/fbctrl_port_probe.py" && echo "# probe unchanged during run" >> "$T"
echo "# $(date +%T) done" >> "$T"
echo "----- TABLE_c3.out"; cat "$T"
