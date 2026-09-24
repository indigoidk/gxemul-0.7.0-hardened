#!/bin/bash
# Part 1 + part 2 of the two-part clearance for the WSL arc build tree, against the SEC working tree.
S=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
T=/tmp/gxsec-build
DIV=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/divergence.txt
cd "$S" || exit 9
n=0; bad=""
for f in $(git ls-files 'src/*.c' 'src/*.h' 2>/dev/null); do
  grep -qxF "$f" "$DIV" && continue
  n=$((n+1))
  if [ ! -f "$T/$f" ]; then bad="$bad MISSING:$f"; elif ! cmp -s "$f" "$T/$f"; then bad="$bad DIFF:$f"; fi
done
echo "/tmp/gxsec-build: shared files checked=$n  mismatches:${bad:- none}"
echo "divergence paths vs SEC (expected to differ for build/ but the arc tree IS the SEC layer):"
for f in $(cat "$DIV"); do if [ -f "$T/$f" ]; then cmp -s "$f" "$T/$f" && echo "  $f SAME-AS-SEC" || echo "  $f DIFFERS"; else echo "  $f ABSENT"; fi; done
nf=$(find $T/src -type f \( -name '*.c' -o -name '*.h' \) -newer $T/gxemul | wc -l)
echo "part 2: sources newer than binary = $nf ; binary: $(stat -c '%y' $T/gxemul) md5 $(md5sum $T/gxemul | cut -c1-8)"
ls -la $T/.MUTANT 2>/dev/null || echo "no sentinel"
