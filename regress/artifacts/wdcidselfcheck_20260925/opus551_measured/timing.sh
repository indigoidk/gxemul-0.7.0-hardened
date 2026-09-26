#!/bin/bash
W=/tmp/opus551p1; d=$W/dev/pristine/regress
F="-std=c99 -I$W/sec/src/include -I$W/sec/src/include/thirdparty -ffunction-sections -fdata-sections -Wl,--gc-sections"
for o in O2 O1 O0 O3 Os; do
  rm -f $d/smoke_$o
  s=$(date +%s%N); cc -$o $F -o $d/smoke_$o $d/smoke.c > $d/smoke_$o.cc 2>&1; rc=$?; e=$(date +%s%N)
  echo "$o build rc=$rc $(( (e-s)/1000000 )) ms; undefined refs: $(grep -o "undefined reference to \`[a-z_]*'" $d/smoke_$o.cc | sort | uniq -c | tr '\n' ' ')"
  if [ -x $d/smoke_$o ]; then s=$(date +%s%N); $d/smoke_$o > $d/smoke_$o.log 2>&1; rc=$?; e=$(date +%s%N); echo "   run rc=$rc $(( (e-s)/1000000 )) ms: $(grep -E '^[0-9]+ rows' $d/smoke_$o.log)"; fi
done
