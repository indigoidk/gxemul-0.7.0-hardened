#!/bin/bash
set -u
G=/mnt/c/DocumentNoSnc/CC/GXEMUL; SEC=$G/GXEMUL-SEC; T=/tmp/gxopus_p9; F=src/devices/dev_pcc2.c
OUT=/tmp/killopus_p9; PROBE=/tmp/frozen_probe_p9.py
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/pcc2p9_opus
say() { echo "[$(date +%H:%M:%S)] $*"; }
die() { echo "*** ABORT: $*"; exit 9; }
mkdir -p "$OUT"
build() { cd "$T" || die cd; rm -f src/devices/dev_pcc2.o; make -j4 > "$OUT/build_$1.log" 2>&1; [ "$T/gxemul" -nt "$T/$F" ] || die "$1: binary not newer than source"; }
score() {
    cd "$SEC/regress" || die cd
    python3 -u "$PROBE" "$T/gxemul" "$1" > "$OUT/$1.out" 2>&1
    grep -q PCC2W_PROBE_DONE "$OUT/$1.out" || die "$1: NO COMPLETION SENTINEL"
    say "  $1: $(grep -m1 PCC2W_RESULT "$OUT/$1.out")"
    grep -m1 PCC2W_RED "$OUT/$1.out" | sed 's/PCC2W_RED=/      RED: /' || echo "      RED: (none)"
    cp "$OUT/$1.out" "$SP/$1.out"
}
mut() {
    echo "$F  mutant $1 (opus pass-9 seat)" > "$T/.MUTANT"
    cp "$SEC/$F" "$T/$F"
    python3 "$SP/mutate.py" "$T/$F" "$2" || die "$1: mutator failed"
    cmp -s "$T/$F" "$SEC/$F" && die "$1: file UNCHANGED after mutation"
    MD=$(diff "$SEC/$F" "$T/$F" | grep -c "^[<>]")
    say "    [$1] mutant diff vs SEC: $MD lines; first added: $(diff "$SEC/$F" "$T/$F" | grep '^>' | head -1 | cut -c1-120)"
    [ "$MD" -gt 0 ] || die "$1: MUTATION NOT APPLIED"
    build "$1"
    say "    [$1] binary $(date -r "$T/gxemul" +%H:%M:%S)  source $(date -r "$T/$F" +%H:%M:%S)"
    score "$1"
}
restore() {
    cp "$SEC/$F" "$T/$F"
    cmp -s "$T/$F" "$SEC/$F" || die "restore: cmp FAILED"
    build restore
    cmp -s "$T/$F" "$SEC/$F" || die "restore: cmp FAILED after rebuild"
    [ "$T/gxemul" -nt "$T/$F" ] || die "restore: binary NOT newer than source"
    rm -f "$T/.MUTANT"
    say "  restored from SEC + REBUILT + verified, sentinel cleared"
}
mut M_OPUS_PENDBOTH PENDBOTH
mut M_OPUS_IDATA2   IDATA2
restore
say "KILLOPUS_P9_DONE"
