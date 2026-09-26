#!/bin/bash
# Build the named variants in the clone, one binary each (bins/gx_<name>).  Clone-local sentinel first; the clone is
# restored from GXEMUL-SEC (never from a backup of its own), rebuilt, and md5-checked against the fix build before the
# sentinel goes.  usage: s3_build.sh <name>...   (names of var/v/<name>.c)
set -u
CL=/tmp/gxo549f2m
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
FIXMD5=4cc158f6c631615365be0c3983f00987
cd "$CL" || exit 2
echo "src/devices/dev_fbctrl.c: variant builds by the opus F2 seat, started $(date +%T)" > "$CL/.MUTANT"
for name in "$@"; do
    src=var/v/$name.c
    if [ ! -f "$src" ]; then echo "[$name] NO SOURCE"; continue; fi
    cp "$src" src/devices/dev_fbctrl.c
    rm -f src/devices/dev_fbctrl.o
    make -j8 > "var/make_$name.log" 2>&1
    rc=$?
    if [ "$rc" = 0 ] && [ gxemul -nt src/devices/dev_fbctrl.c ] && [ src/devices/dev_fbctrl.o -nt src/devices/dev_fbctrl.c ]; then
        cp gxemul "bins/gx_$name"
        echo "[$name] built rc=$rc md5=$(md5sum < gxemul | cut -c1-8) warn=$(grep -c 'warning:' "var/make_$name.log")"
    else
        rm -f "bins/gx_$name"
        echo "[$name] BUILD FAILED rc=$rc (see var/make_$name.log)"; tail -5 "var/make_$name.log"
    fi
done
cp "$SEC/src/devices/dev_fbctrl.c" src/devices/dev_fbctrl.c
rm -f src/devices/dev_fbctrl.o
make -j8 > var/make_restore.log 2>&1
m=$(md5sum < gxemul | cut -d' ' -f1)
if cmp -s src/devices/dev_fbctrl.c "$SEC/src/devices/dev_fbctrl.c" && [ gxemul -nt src/devices/dev_fbctrl.c ] && [ "$m" = "$FIXMD5" ]; then
    rm -f "$CL/.MUTANT"; echo "RESTORED: source cmp SEC clean, binary fresh, md5 $m == fix build; sentinel cleared"
else
    echo "RESTORE NOT VERIFIED (md5 $m) -- sentinel LEFT"
fi
