#!/bin/bash
# Build each named variant (var/v/<name>.c) into bins/gx_<name>.  Clone-local sentinel; restore from GXEMUL-SEC, rebuild,
# and require the fix build's md5 before clearing it.
set -u
CL=/tmp/gxo549cf2
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
FIXMD5=b5b99e6d1e5fd077c8cf782d8c6a6a2c
cd "$CL" || exit 2
echo "src/devices/dev_fbctrl.c: closing-F2 variant builds, started $(date +%T)" > "$CL/.MUTANT"
for name in "$@"; do
    cp "var/v/$name.c" src/devices/dev_fbctrl.c || { echo "[$name] NO SOURCE"; continue; }
    rm -f src/devices/dev_fbctrl.o
    make -j8 > "var/make_$name.log" 2>&1
    rc=$?
    if [ "$rc" = 0 ] && [ gxemul -nt src/devices/dev_fbctrl.c ] && [ src/devices/dev_fbctrl.o -nt src/devices/dev_fbctrl.c ]; then
        cp gxemul "bins/gx_$name"
        echo "[$name] built md5=$(md5sum < gxemul | cut -c1-8) warn=$(grep -c 'warning:' "var/make_$name.log")"
    else
        rm -f "bins/gx_$name"; echo "[$name] BUILD FAILED rc=$rc"; tail -5 "var/make_$name.log"
    fi
done
cp "$SEC/src/devices/dev_fbctrl.c" src/devices/dev_fbctrl.c
rm -f src/devices/dev_fbctrl.o
make -j8 > var/make_restore.log 2>&1
m=$(md5sum < gxemul | cut -d' ' -f1)
if cmp -s src/devices/dev_fbctrl.c "$SEC/src/devices/dev_fbctrl.c" && [ gxemul -nt src/devices/dev_fbctrl.c ] && [ "$m" = "$FIXMD5" ]; then
    rm -f "$CL/.MUTANT"; echo "RESTORED: cmp SEC clean, binary fresh, md5 $m == fix build; sentinel cleared"
else
    echo "RESTORE NOT VERIFIED (md5 $m) -- sentinel LEFT"
fi
