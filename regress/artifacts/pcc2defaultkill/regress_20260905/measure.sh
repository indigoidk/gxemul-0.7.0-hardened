#!/bin/bash
set -u
G=/mnt/c/DocumentNoSnc/CC/GXEMUL
SEC=$G/GXEMUL-SEC
F=src/devices/dev_pcc2.c
T=/tmp/gxfable501r
OUT=/tmp/f501r
ASRUN=$SEC/regress/artifacts/pcc2defaultkill/killtable4_20260905/killdk501c.asrun.sh
say(){ echo "[$(date +%H:%M:%S)] $*"; }
die(){ echo "*** ABORT: $*"; exit 9; }
mkdir -p "$OUT"
say "space: $(df -h /tmp | tail -1)"; say "nproc $(nproc)  make $(command -v make)  py $(command -v python3)"
[ -d "$G/build" ] || die "no build/ tree"
rm -rf "$T"
cp -a "$G/build" "$T" || die "clone failed"
cmp -s "$T/$F" "$SEC/$F" && say "clone $F already == SEC" || { cp "$SEC/$F" "$T/$F"; say "clone $F refreshed from SEC"; }
grep -q "pcc2defaultkill" "$T/$F" || die "clone lacks the #501 fix comment"
build(){ cd "$T" || die cd; rm -f src/devices/dev_pcc2.o; make -j4 > "$OUT/build_$1.log" 2>&1; [ "$T/gxemul" -nt "$T/$F" ] || die "$1: binary NOT newer than source (build failed?)"; say "  $1 built: binary $(date -r "$T/gxemul" +%H:%M:%S) source $(date -r "$T/$F" +%H:%M:%S)"; }
score(){ cd "$SEC/regress" || die cd; python3 -u pcc2_default_probe.py "$T/gxemul" "$1" > "$OUT/$1.out" 2>&1; grep -q PCC2D_PROBE_DONE "$OUT/$1.out" || die "$1 NO SENTINEL"; say "  $1: $(grep -m1 PCC2D_RESULT "$OUT/$1.out")  $(grep -m1 PCC2D_RED "$OUT/$1.out" | cut -c1-90)"; }
say "=== BASE (committed fix) ==="; build BASE; score FABLE_BASE
say "=== M_EXIT (verbatim exit(1) arm, DKN->DKO from the as-run script) ==="
eval "$(grep -m1 -E '^DKN=' "$ASRUN")"
eval "$(grep -m1 -E '^DKO=' "$ASRUN")"
echo "$F  mutant M_EXIT (fable regress verify)" > "$T/.MUTANT"
cp "$SEC/$F" "$T/$F"
python3 - "$T/$F" <<PYEOF
import io,sys
p=sys.argv[1]
s=io.open(p,encoding='utf-8').read()
a='$DKN'
b='$DKO'
assert s.count(a)==1, ("DKN match count=%d" % s.count(a))
s=s.replace(a,b)
io.open(p,'w',encoding='utf-8',newline='\n').write(s)
print("mutation applied; exit1 present:", s.count('exit(1)'))
PYEOF
[ $? -eq 0 ] || die "mutator failed"
cmp -s "$T/$F" "$SEC/$F" && die "M_EXIT: file UNCHANGED"
say "  M_EXIT diff vs SEC: $(diff "$SEC/$F" "$T/$F" | grep -c '^[<>]') lines"
build M_EXIT; score FABLE_MEXIT
say "=== RESTORE from SEC + REBUILD + verify, THEN clear sentinel ==="
cd "$T" || die cd; cp "$SEC/$F" "$T/$F"; cmp -s "$T/$F" "$SEC/$F" || die "restore cmp FAILED -- sentinel KEPT"
rm -f src/devices/dev_pcc2.o; make -j4 > "$OUT/build_restore.log" 2>&1; [ "$T/gxemul" -nt "$T/$F" ] || die "restore: binary not newer"
rm -f "$T/.MUTANT"; say "  restored + rebuilt + verified, sentinel cleared"
say "FABLE501R_DONE"
