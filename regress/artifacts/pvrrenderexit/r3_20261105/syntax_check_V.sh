#!/bin/bash
# syntax_check_V.sh -- read-only: compiles each NEW table-3 variant (no object kept: -fsyntax-only) with build/'s own flags and
# includes, from a scratch copy in /tmp (nothing in build/ or GXEMUL-SEC is written).  Prints one line per variant.
A=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/pvrrenderexit/r3_20261105
INC=/mnt/c/DocumentNoSnc/cc/GXEMUL/build/src/include
T=$(mktemp -d /tmp/pvrsyn_XXXX)
ok=0; bad=0
for v in $A/variants/[A-Z]*.c; do
  n=$(basename $v .c)
  case $n in B1_exit|E1*|E2*|K1*|K2*|L1*|M[0-9]*|O1*|O2*|R1s_*|R1t_*|S1s_*|S1t_*|X1s_*|X1t_*|Y[1-4]*) continue;; esac
  cp $v $T/dev_pvr.c
  if cc -fsyntax-only -Wall -Wextra -Wno-unused-parameter -I/usr/X11R6/include -I$INC $T/dev_pvr.c 2> $T/err.txt; then ok=$((ok+1));
  else bad=$((bad+1)); echo "SYNTAX FAIL $n"; head -3 $T/err.txt; fi
done
rm -rf $T
echo "SYNTAX_CHECK new variants: $ok ok, $bad failed"
