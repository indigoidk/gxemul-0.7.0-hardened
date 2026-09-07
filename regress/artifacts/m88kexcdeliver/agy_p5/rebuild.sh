#!/bin/bash
set -e

C=/tmp/gxagy502

cd "$C/src/cpus"
rm -f cpu_m88k.o
make -s -j4
cd "$C"
make -s -j4

if [ "$C/gxemul" -nt "$C/src/cpus/cpu_m88k.c" ]; then
    echo "REBUILD_DONE"
else
    echo "REBUILD_FAILED_STALE_BINARY"
    exit 1
fi
