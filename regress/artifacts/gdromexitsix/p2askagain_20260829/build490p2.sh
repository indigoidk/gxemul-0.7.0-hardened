#!/bin/bash
#  #490 pass-2 ASK-AGAIN: build phase.  Runs as a SCRIPT FILE, never as `wsl -- bash -c`,
#  because a `$` inside a -c string is eaten by the outer shell and a never-applied mutant
#  scores the BASE binary and reports a clean table.
set -u

SCRATCH=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad
CLONE=/tmp/gxopus490p2
BINS=/tmp/gxopus490p2_bins
PIN=/tmp/r2m_pinned/dev_dreamcast_gdrom.c.BASELINE
SRC=src/devices/dev_dreamcast_gdrom.c
MUT=$SCRATCH/mut490p2.py

BASE_SRC_MD5=85846dc966d00efe511d2b5755364490
BASE_BIN_MD5=8d473baa488b2aef3eabd3be569f2c9d

echo "=== BUILD490P2 START $(date -Is) ==="

#  (1) NAME THE BASELINE and verify the PIN is the round's post-fix working set.
echo "--- pin md5 ---"
md5sum "$PIN"
if [ "$(md5sum "$PIN" | cut -d' ' -f1)" != "$BASE_SRC_MD5" ]; then
    echo "BUILD490P2_ABORT: pin does not match the named baseline"; exit 1
fi

#  (2) Fresh clone from the previous seat's restored tree, then FORCE the source to the pin
#      rather than trusting whatever the clone inherited.
rm -rf "$CLONE" "$BINS"
cp -a /tmp/gxr2m "$CLONE" || { echo "BUILD490P2_ABORT: clone failed"; exit 1; }
mkdir -p "$BINS"
rm -f "$CLONE/.STALE"          # that marker is about build/, not this tree
cp "$PIN" "$CLONE/$SRC"
cmp -s "$PIN" "$CLONE/$SRC" || { echo "BUILD490P2_ABORT: pin copy differs"; exit 1; }
echo "clone source == pin: CLEAN"

cd "$CLONE" || exit 1

build_one () {
    tag=$1
    rm -f src/devices/dev_dreamcast_gdrom.o gxemul
    make -j4 > "/tmp/gxopus490p2_build_${tag}.log" 2>&1
    rc=$?
    if [ ! -x gxemul ]; then
        echo "BUILD $tag: FAILED (no binary), make rc=$rc"
        tail -5 "/tmp/gxopus490p2_build_${tag}.log" | sed 's/^/      /'
        return 1
    fi
    if [ gxemul -nt "$SRC" ]; then
        fresh=YES
    else
        fresh=NO
    fi
    m=$(md5sum gxemul | cut -d' ' -f1)
    cp gxemul "$BINS/$tag"
    echo "BUILD $tag: rc=$rc binary-newer-than-source=$fresh md5=$m"
    return 0
}

#  (3) Rebuild the BASELINE binary in the clone.  This doubles as the freshness proof.
build_one base || exit 1
if [ "$(md5sum "$BINS/base" | cut -d' ' -f1)" != "$BASE_BIN_MD5" ]; then
    echo "NOTE: baseline binary md5 differs from the r2measure baseline ($BASE_BIN_MD5)."
    echo "      (different build dir/paths can change the binary; the source is pin-identical)"
fi

#  (4) SENTINEL FIRST, then the mutants.
echo "$CLONE/.MUTANT: $SRC  #490 pass-2 ask-again mutants (opus measuring seat)" > "$CLONE/.MUTANT"
echo "sentinel dropped"

for tag in E1_aliasover E2_assignA E3_widenA; do
    cp "$PIN" "$SRC"
    python3 "$MUT" "$tag" "$PIN" "$SRC" || { echo "BUILD490P2_ABORT: mutator failed for $tag"; exit 1; }
    echo "--- diff for $tag ---"
    diff "$PIN" "$SRC" | sed 's/^/      /'
    build_one "$tag" || exit 1
done

#  (5) RESTORE, verified by cmp against the PIN, and REBUILD -- the restore is not
#      finished until the binary is rebuilt.
cp "$PIN" "$SRC"
if cmp -s "$PIN" "$SRC"; then
    echo "RESTORE cmp vs pin: CLEAN"
    build_one restore || exit 1
    if [ gxemul -nt "$SRC" ]; then
        rm -f "$CLONE/.MUTANT"
        echo "sentinel CLEARED (source cmp-clean AND binary newer than source)"
    else
        echo "sentinel KEPT: binary is not newer than source"
    fi
else
    echo "RESTORE FAILED -- sentinel KEPT"
fi

echo "--- binaries ---"
md5sum "$BINS"/*
echo "--- distinctness (each mutant must differ from base) ---"
md5sum "$BINS"/* | awk '{print $1}' | sort | uniq -c | sort -rn
echo "=== BUILD490P2_DONE $(date -Is) ==="
