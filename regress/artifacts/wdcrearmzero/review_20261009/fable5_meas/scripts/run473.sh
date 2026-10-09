#!/bin/bash
# fable5 late review of #473: score mutants of dev_wdc.c against a detector copy.
#   run473.sh <detector.c> <tag> <mutant>...
# Everything lives under /tmp/fable473 (my own scratch).  Nothing under /mnt/c is written.
set -u
W=/tmp/fable473
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/fableq
DET=$1; TAG=$2; shift 2
CC=$(command -v cc || command -v gcc)
score() {   # score <label> <log>
    local lab=$1 log=$2
    local sum tok nsf
    sum=$(grep -oE '^[0-9]+ rows, [0-9]+ failures' "$log" | tail -1)
    tok=$(grep -c 'WDC_IDENTIFY_PASS' "$log")
    nsf=$(grep '^  FAIL' "$log" | grep -vc '@@SELFCHECK@@')
    printf '%-22s %-26s PASS_token=%s  non-selfcheck FAIL rows=%s\n' "$lab" "${sum:-NO SUMMARY LINE}" "$tok" "$nsf"
    grep '^  FAIL' "$log" | grep -v '@@SELFCHECK@@' | sed 's/^/      /'
}
# baseline for THIS detector copy
B=$W/b_$TAG; rm -rf "$B"; mkdir -p "$B/src/devices" "$B/regress"
cp -r "$W/src/include" "$B/src/"; cp "$W/config.h" "$B/"
cp "$W/src/devices/dev_wdc.c" "$B/src/devices/"; cp "$DET" "$B/regress/diff_wdc_identify.c"
( cd "$B/regress" && $CC -O2 -std=c99 -I"$B/src/include" -I"$B/src/include/thirdparty" \
    -ffunction-sections -fdata-sections -Wl,--gc-sections -o "$B/det" diff_wdc_identify.c > "$B/build.log" 2>&1 ) \
    || { echo "BASELINE BUILD FAILED ($TAG)"; head -20 "$B/build.log"; exit 8; }
"$B/det" > "$B/run.log" 2>&1; echo "baseline rc=$?"
score "BASELINE[$TAG]" "$B/run.log"
for M in "$@"; do
    D=$W/m_${TAG}_$M; rm -rf "$D"; mkdir -p "$D/src/devices" "$D/regress"
    cp -r "$W/src/include" "$D/src/"; cp "$W/config.h" "$D/"
    cp "$DET" "$D/regress/diff_wdc_identify.c"
    python3 "$SP/mut473.py" "$W/src/devices/dev_wdc.c" "$D/src/devices/dev_wdc.c" "$M" || { echo "$M: MUTANT_FAULT"; continue; }
    cmp -s "$D/src/devices/dev_wdc.c" "$W/src/devices/dev_wdc.c" && { echo "$M: MUTANT_FAULT identical to base"; continue; }
    diff "$W/src/devices/dev_wdc.c" "$D/src/devices/dev_wdc.c" | grep -E '^[<>]' | sed 's/^/      /'
    ( cd "$D/regress" && $CC -O2 -std=c99 -I"$D/src/include" -I"$D/src/include/thirdparty" \
        -ffunction-sections -fdata-sections -Wl,--gc-sections -o "$D/det" diff_wdc_identify.c > "$D/build.log" 2>&1 ) \
        || { echo "$M: BUILD FAULT (not a kill)"; head -5 "$D/build.log"; continue; }
    [ "$D/det" -nt "$D/src/devices/dev_wdc.c" ] || { echo "$M: BINARY NOT NEWER THAN SOURCE -- fault"; continue; }
    "$D/det" > "$D/run.log" 2>&1; rc=$?
    [ $rc -gt 128 ] && echo "$M: SIGNAL rc=$rc (fault, not a detection)"
    score "$M" "$D/run.log"
done
echo "RUN473_DONE $TAG"
