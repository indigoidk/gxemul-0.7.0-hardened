#!/bin/bash
#  PASS-4 OPUS SEAT.  Two candidate escapes of the 96-row detector, both in the SHARED
#  helper pcc2_width_decline() -- a cell the 12x9 enumeration does not contain, because
#  all nine shapes are edits at the twelve CALL SITES.
#    M_LATCHASSIGN  `d->warned |= (1u << bit);' -> `d->warned = (1u << bit);'   ONE character.
#                   Clause (d): guard kept (!(warned & bit)), its repair (accumulation) nulled.
#                   Predicted 96/96 -- no session writes wide to block A, then B, then A.
#    M_BITSHIFT     `1u << bit' -> `1u << (bit + 1)'  -- a TRANSLATION of the latch space.
#                   Predicted 96/96 and EQUIVALENT (bits are private); clause (f) control.
set -u
G=/mnt/c/DocumentNoSnc/CC/GXEMUL; SEC=$G/GXEMUL-SEC; T=/tmp/gxopus_p4; F=src/devices/dev_pcc2.c
OUT=/tmp/killopus_p4; PROBE=pcc2_width_probe.py
say() { echo "[$(date +%H:%M:%S)] $*"; }
die() { echo "*** ABORT: $*"; exit 9; }
rm -rf "$T" "$OUT"; mkdir -p "$OUT"
cp -a "$G/build" "$T" || die "clone failed"
cmp -s "$T/$F" "$SEC/$F" || { cp "$SEC/$F" "$T/$F"; say "  clone's $F refreshed from SEC"; }
cp "$SEC/regress/$PROBE" "$OUT/frozen_probe.py" || die "cannot freeze probe"
say "  instrument frozen: $(wc -c < "$OUT/frozen_probe.py") bytes  md5 $(md5sum < "$OUT/frozen_probe.py" | cut -c1-8)"
build() { cd "$T" || die cd; rm -f src/devices/dev_pcc2.o; make -j4 > "$OUT/build_$1.log" 2>&1; [ "$T/gxemul" -nt "$T/$F" ] || die "$1: binary not newer than source"; }
score() {
    cd "$SEC/regress" || die cd
    python3 -u "$OUT/frozen_probe.py" "$T/gxemul" "$1" > "$OUT/$1.out" 2>&1
    grep -q PCC2W_PROBE_DONE "$OUT/$1.out" || die "$1: NO COMPLETION SENTINEL"
    say "  RESULT $1 [$2]: $(grep -m1 PCC2W_RESULT "$OUT/$1.out")"
    grep -m1 PCC2W_RED "$OUT/$1.out" | sed 's/PCC2W_RED=/      RED: /' || true
}
mut() {
    echo "$F  mutant $1" > "$T/.MUTANT"; cp "$SEC/$F" "$T/$F"
    python3 - "$T/$F" "$3" <<'PYEOF'
import io, sys
p, body = sys.argv[1], sys.argv[2]; s = io.open(p, encoding='utf-8').read()
ns = {'s': s}; exec(body, ns); io.open(p, 'w', encoding='utf-8', newline='\n').write(ns['s'])
PYEOF
    [ $? -eq 0 ] || die "$1: mutator failed"
    cmp -s "$T/$F" "$SEC/$F" && die "$1: file UNCHANGED after mutation"
    say "    MUTANT $1 proof -- helper body now: $(grep -c 'd->warned |= ' "$T/$F") x '|=' , $(grep -c 'd->warned = ' "$T/$F") x '=' , $(grep -c '1u << bit' "$T/$F") x '1u << bit' , $(grep -c '1u << (bit + 1)' "$T/$F") x 'bit+1'"
    build "$1"
    say "    MUTANT $1 binary $(date -r "$T/gxemul" +%H:%M:%S)  source $(date -r "$T/$F" +%H:%M:%S)"
    score "$1" "$2"
}
say "BASE -- 96/96 owed (the clone reproduces part 3c on the SHIPPED instrument)"
build BASE; say "    BASE binary $(date -r "$T/gxemul" +%H:%M:%S)  source $(date -r "$T/$F" +%H:%M:%S)"
score BASE CONTROL
mut M_LATCHASSIGN 'predict 96/96 ESCAPE' "a='\t\td->warned |= (1u << bit);\n'; assert s.count(a)==1, s.count(a); s=s.replace(a,'\t\td->warned = (1u << bit);\n')"
mut M_BITSHIFT 'predict 96/96 EQUIVALENT' "a='(1u << bit)'; assert s.count(a)==2, s.count(a); s=s.replace(a,'(1u << (bit + 1))')"
say "RESTORE from SEC + REBUILD + verify, THEN clear the sentinel"
cp "$SEC/$F" "$T/$F"; cmp -s "$T/$F" "$SEC/$F" || die "restore cmp FAILED -- sentinel KEPT"
build restore; [ -f "$T/gxemul" ] || die "no binary after restore"
rm -f "$T/.MUTANT"; say "  restored + REBUILT + verified, sentinel cleared"
say "KILLOPUS_P4_DONE"
