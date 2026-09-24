#!/bin/bash
S=/tmp/opus_census0923/snap/regress
T=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress
n=0; d=0
for f in "$S"/*; do b=$(basename "$f"); n=$((n+1)); cmp -s "$f" "$T/$b" || { d=$((d+1)); echo "DIFFERS: $b"; }; done
echo "compared $n snapshot files against the tree: $d differ"
