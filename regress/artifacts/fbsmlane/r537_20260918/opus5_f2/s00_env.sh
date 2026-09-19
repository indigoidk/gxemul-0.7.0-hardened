#!/bin/bash
# s00: toolchain + build/ object state, read-only.
set -u
ROOT=/mnt/c/DocumentNoSnc/CC/GXEMUL
SEC=$ROOT/GXEMUL-SEC
B=$ROOT/build
gcc --version | head -1
python3 --version
echo "objects (excl main.o, dev_footbridge.o): $(find $B/src -name '*.o' ! -name main.o ! -name dev_footbridge.o | wc -l)"
ls -la --time-style=full-iso $B/gxemul $B/src/devices/dev_footbridge.o $B/src/core/timer.o
for f in src/core/timer.c src/devices/dev_footbridge.c src/include/timer.h src/include/misc.h src/include/machine.h src/include/cpu.h src/include/device.h; do
  if cmp -s $SEC/$f $B/$f; then echo "SAME  $f"; else echo "DIFF  $f"; fi
done
ls -la $B/.MUTANT 2>&1 | head -1
echo "which gate: $(command -v gate || echo none)"
echo "dev_footbridge.c copies under SEC (excluding artifacts):"
find $SEC -name 'dev_footbridge.c' -not -path '*/artifacts/*' 2>/dev/null
echo "headers directly in SEC/src (the extra -I../src dir):"
ls $SEC/src/*.h 2>/dev/null | head; ls $SEC/src | head -40
