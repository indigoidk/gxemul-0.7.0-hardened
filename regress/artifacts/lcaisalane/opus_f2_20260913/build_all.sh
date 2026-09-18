#!/bin/bash
#  lcaisalane F2 (Opus measuring seat, 2026-09-13): build HEAD and variants A, B, C in SCRATCH
#  CLONES under /tmp/gxlcaf2.  Touches no project build tree (build/, build-asan/,
#  /tmp/gxsec-build) and not /tmp/gxopuscrime.  Writes into GXEMUL-SEC only under this
#  artifacts dir (new files).
#
#  Each variant tree carries a .MUTANT sentinel naming its edit from BEFORE the edit until it is
#  deliberately discarded; the HEAD tree carries none and is cmp-checked against `git show HEAD:'.
#  Freshness is checked by [ gxemul -nt src/devices/dev_lca.c ] -- make's exit status is not
#  trusted on its own.
set -u
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
ART=$SEC/regress/artifacts/lcaisalane/opus_f2_20260913
R=/tmp/gxlcaf2
J=2
mkdir -p "$R"

say() { echo "[$(date '+%H:%M:%S')] $*"; }

if [ ! -x "$R/head/gxemul" ]; then
	rm -rf "$R/head"; mkdir -p "$R/head"
	say "archive HEAD -> $R/head"
	git -c safe.directory='*' -C "$SEC" rev-parse HEAD > "$ART/HEAD_SHA.txt"
	git -c safe.directory='*' -C "$SEC" archive HEAD | tar -x -C "$R/head" || { say "ARCHIVE FAILED"; exit 2; }
	cd "$R/head" || exit 2
	say "configure (head)"
	./configure > "$ART/build_head.log" 2>&1 || { say "CONFIGURE FAILED"; echo BUILD_ALL_DONE; exit 3; }
	say "make -j$J (head)"
	make -j$J >> "$ART/build_head.log" 2>&1; echo "make rc=$?" >> "$ART/build_head.log"
fi
cd "$R/head" || exit 2
if [ -x gxemul ] && [ gxemul -nt src/devices/dev_lca.c ]; then
	say "head: gxemul FRESH ($(stat -c %y gxemul))"
else
	say "head: gxemul MISSING or STALE"; echo BUILD_ALL_DONE; exit 4
fi
git -c safe.directory='*' -C "$SEC" show HEAD:src/devices/dev_lca.c > "$R/dev_lca.HEAD.c"
cmp -s "$R/dev_lca.HEAD.c" "$R/head/src/devices/dev_lca.c" && say "head: dev_lca.c == HEAD:dev_lca.c" \
	|| { say "head: dev_lca.c DIFFERS from HEAD"; echo BUILD_ALL_DONE; exit 5; }

python3 "$ART/mk_variants.py" "$R/dev_lca.HEAD.c" "$ART" || { say "MK_VARIANTS FAILED"; echo BUILD_ALL_DONE; exit 6; }
for v in A B C; do
	diff -u "$R/dev_lca.HEAD.c" "$ART/dev_lca.$v.c" \
	    | sed -e "1s|.*|--- HEAD:src/devices/dev_lca.c|" -e "2s|.*|+++ variant $v: src/devices/dev_lca.c|" \
	    > "$ART/variant_$v.diff"
done

for v in A B C; do
	T=$R/$v
	if [ -x "$T/gxemul" ] && [ "$T/gxemul" -nt "$T/src/devices/dev_lca.c" ] \
	    && cmp -s "$T/src/devices/dev_lca.c" "$ART/dev_lca.$v.c"; then
		say "$v: already built and fresh"; continue
	fi
	rm -rf "$T"
	say "cp -a head -> $v"
	cp -a "$R/head" "$T"
	echo "$T/src/devices/dev_lca.c  variant $v of lcaisalane F2 -- see $ART/variant_$v.diff" > "$T/.MUTANT"
	cp "$ART/dev_lca.$v.c" "$T/src/devices/dev_lca.c"
	touch "$T/src/devices/dev_lca.c"
	rm -f "$T"/src/cpus/*.o
	cd "$T" || exit 2
	say "make -j$J ($v)"
	make -j$J > "$ART/build_$v.log" 2>&1; echo "make rc=$?" >> "$ART/build_$v.log"
	if [ -x gxemul ] && [ gxemul -nt src/devices/dev_lca.c ]; then
		say "$v: gxemul FRESH ($(stat -c %y gxemul))"
	else
		say "$v: gxemul STALE OR MISSING -- see build_$v.log"
	fi
	cmp -s src/devices/dev_lca.c "$ART/dev_lca.$v.c" && say "$v: source == variant file" || say "$v: SOURCE MISMATCH"
done
say "done"
echo BUILD_ALL_DONE
