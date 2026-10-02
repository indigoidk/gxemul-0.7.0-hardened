#!/bin/bash
#  build46.sh -- the Opus seat's measurement builds for the ACCEPTS enumeration.  WSL scratch clone ONLY:
#  /tmp/gxopus_acc46 (a cp -a of table 16's clone /tmp/gxopus_r14, which is READ, never written) and binaries in
#  /tmp/gxopus_acc46_bins.  No project tree is written.  Clone-local .MUTANT sentinel around the one mutation;
#  cleared only after the source cmp's clean against GXEMUL-SEC AND a rebuilt binary is newer than it.
set -u
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
SPW=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46
SRCCLONE=/tmp/gxopus_r14
C=/tmp/gxopus_acc46
B=/tmp/gxopus_acc46_bins
F=src/devices/dev_sgi_ip32.c

echo "BUILD46_START $(date '+%F %T')"
[ -e "$C" ] && { echo "clone $C already exists -- abort (never reuse a clone of unknown state)"; exit 1; }
[ -e "$SRCCLONE/.MUTANT" ] && { echo "source clone carries a sentinel -- abort"; exit 1; }
cp -a "$SRCCLONE" "$C" || { echo "cp -a failed"; exit 1; }
rm -rf "$B"; mkdir -p "$B"
cd "$C" || exit 1
if cmp -s "$F" "$SEC/$F"; then echo "BASELINE_CMP CLEAN"; else echo "clone differs from SEC -- abort"; exit 1; fi
md5sum "$SEC/$F" "$F" "$SPW/mut46.py"

build() {
    rm -f src/devices/dev_sgi_ip32.o
    nice -n 19 make -j4 > "$SPW/build_$1.log" 2>&1
    rc=$?
    if [ "$rc" = 0 ] && [ gxemul -nt "$F" ] && [ src/devices/dev_sgi_ip32.o -nt "$F" ]; then
        cp gxemul "$B/$1"; echo "BUILD_OK $1 $(date '+%T') $(md5sum < "$B/$1" | cut -c1-8)"
    else
        echo "BUILD_FAIL $1 rc=$rc"; tail -30 "$SPW/build_$1.log"; return 1
    fi
}
restore() {
    cp "$SEC/$F" "$F"
    build restored || { echo "RESTORE BUILD FAILED -- sentinel kept"; return 1; }
    if cmp -s "$F" "$SEC/$F" && [ gxemul -nt "$F" ]; then
        rm -f .MUTANT; echo "CLONE RESTORED cmp=clean binary-nt-source=yes"
    else
        echo "CLONE RESTORE INCOMPLETE -- sentinel kept"; return 1
    fi
}

rm -f src/cpus/*.o
echo "src/cpus/*.o removed $(date '+%T')"
build base || exit 1

echo "$F  opus_acc46 measurement mutant -- restore from GXEMUL-SEC, then REBUILD" > .MUTANT
python3 "$SPW/mut46.py" "$SEC/$F" "$F" || { restore; exit 1; }
diff -u "$SEC/$F" "$F" > "$SPW/mut46.diff"
echo "mutant diff: $(grep -c '^+' "$SPW/mut46.diff") added lines, $(grep -c '^-' "$SPW/mut46.diff") removed (incl. headers)"
build envmut || { restore; exit 1; }
restore || exit 1
if cmp -s "$B/base" "$B/restored"; then echo "restored == base (byte-identical)"; else echo "NOTE restored differs from base"; fi
cmp -s "$B/base" "$B/envmut" && echo "NOTE envmut IDENTICAL to base -- the mutation did not take" || echo "envmut differs from base (expected)"
ls -la "$B"
echo "BUILD46_DONE $(date '+%F %T')"
