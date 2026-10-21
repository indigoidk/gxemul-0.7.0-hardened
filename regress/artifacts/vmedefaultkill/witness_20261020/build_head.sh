#!/bin/bash
# build_head.sh -- build committed HEAD 5dbc000e (minus regress/, which the build never reads)
# in a scratch clone at /tmp/gxvme_head_20261020.  Touches no project tree.
# Deliberately NOT set -e, and deliberately does not end in a comparison.
set -u
OUT=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/vme/witness_20261020
TAR="$OUT/head_5dbc000e_noregress.tar"
W=/tmp/gxvme_head_20261020

if [ -e "$W" ]; then echo "CLONE_ALREADY_EXISTS $W -- refusing to reuse"; exit 3; fi
mkdir -p "$W" || { echo "MKDIR_FAILED"; exit 3; }
cd "$W" || exit 3
tar -xf "$TAR" || { echo "TAR_FAILED"; exit 3; }
echo "EXTRACTED files: $(find . -type f | wc -l)"
echo "dev_vme.c md5 (extracted): $(md5sum src/devices/dev_vme.c | cut -d' ' -f1)"
echo "debugmsg.c md5 (extracted): $(md5sum src/core/debugmsg.c | cut -d' ' -f1)"
echo "CRLF lines in configure: $(grep -c $'\r' configure)"
echo "CRLF lines in dev_vme.c: $(grep -c $'\r' src/devices/dev_vme.c)"

date '+CONFIGURE_START %F %T'
./configure > "$OUT/configure.log" 2>&1
echo "CONFIGURE_RC=$?"
date '+MAKE_START %F %T'
make -j4 > "$OUT/make.log" 2>&1
echo "MAKE_RC=$?"
date '+MAKE_END %F %T'

if [ -f gxemul ] && [ gxemul -nt src/devices/dev_vme.c ] && [ gxemul -nt src/core/debugmsg.c ]; then
  echo "BINARY_FRESH=yes"
else
  echo "BINARY_FRESH=no"
fi
ls -la --time-style=full-iso gxemul src/devices/dev_vme.c src/devices/dev_vme.o src/core/debugmsg.c src/core/debugmsg.o 2>&1
echo "gxemul md5: $(md5sum gxemul | cut -d' ' -f1)"
echo "gxemul size: $(stat -c %s gxemul)"
echo "warnings/errors in make.log: $(grep -ciE 'error|warning' "$OUT/make.log")"
echo "BUILD_HEAD_DONE"
