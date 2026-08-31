#!/bin/bash
#  #499 pass 4: does the 48-row closure KILL the two mutants that swept 36 rows clean?
#  Plus a re-score of T and W, because added rows perturb other mutants' scores.
#  SCRATCH CLONE ONLY.
set -u
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
T=/tmp/gx499f
F=src/devices/dev_sgi_re.c
OUT=/tmp/kill48
say(){ echo "[$(date +%H:%M:%S)] $*"; }
die(){ say "*** ABORT: $* ***"; exit 1; }

mkdir -p "$OUT"
say "clone + baseline"
rm -rf "$T"; cp -a /mnt/c/DocumentNoSnc/cc/GXEMUL/build "$T" || die clone
cd "$T" || die cd
cmp -s "$T/$F" "$SEC/$F" || die "clone differs from SEC"
mkdir -p "$T/rg"
cp "$SEC/regress/sgi_re_unmapped_probe.py" "$T/rg/probe.py" || die probe
say "  frozen instrument: $(wc -c < $T/rg/probe.py) bytes"

build_and_score () {
    local label="$1"
    rm -f src/devices/dev_sgi_re.o
    make -j4 > "$OUT/build_$label.log" 2>&1
    [ "$T/gxemul" -nt "$T/$F" ] || { say "  $label: binary NOT newer -- SKIP"; return 1; }
    ( cd "$T/rg" && timeout 600 python3 -u probe.py "$T/gxemul" "$label" > "$OUT/$label.out" 2>&1 )
    local ok fail res
    ok=$(grep -ac " ok\$" "$OUT/$label.out"); fail=$(grep -ac " FAIL\$" "$OUT/$label.out")
    res=$(grep -a 'OPUS499T_RESULT' "$OUT/$label.out" | head -1)
    say "  $label: ok=$ok fail=$fail  $res"
    if [ "$fail" -gt 0 ]; then say "    RED rows: $(grep -a ' FAIL$' $OUT/$label.out | awk '{printf "%s, ", $1$2}')"; fi
}

say "BASE (expect 48/48)"
rm -f src/cpus/*.o
build_and_score base

apply () {  # $1 = label, $2 = python edit
    cd "$T"; echo "$1" > "$T/.MUTANT"
    cp "$SEC/$F" "$T/$F"
    python3 -c "$2" || die "mutator $1"
}

say "M1  read arm qualified to component 2  (swept 36 rows CLEAN)"
apply M1 "
import io
p='src/devices/dev_sgi_re.c'; s=io.open(p,encoding='utf-8').read()
a='\t\t} else {\n\t\t\tif (!(d->warned & SGIRE_W_UNMAP_RD)) {'
assert s.count(a)==1
b=('\t\t} else if (relative_addr < CRIME_RE_LINEAR_A) {\n'
   '\t\t\tfatal(\"TODO: read from CRIME_RE_CLIP_IDS\");\n'
   '\t\t\texit(1);\n'
   '\t\t} else {\n\t\t\tif (!(d->warned & SGIRE_W_UNMAP_RD)) {')
io.open(p,'w',encoding='utf-8',newline='').write(s.replace(a,b))
print('  M1 applied')
"
build_and_score M1

say "M2  component 1 far edge swallowed by LINEAR_A  (swept 36 rows CLEAN)"
apply M2 "
import io
p='src/devices/dev_sgi_re.c'; s=io.open(p,encoding='utf-8').read()
a='relative_addr >= CRIME_RE_LINEAR_A && relative_addr < CRIME_RE_LINEAR_A + 0x80'
assert s.count(a)==1
b='relative_addr >= CRIME_RE_LINEAR_A - 0x10 && relative_addr < CRIME_RE_LINEAR_A + 0x80'
io.open(p,'w',encoding='utf-8',newline='').write(s.replace(a,b))
print('  M2 applied')
"
build_and_score M2

say "V  zero-datum write rerouted  (the VALUE axis opus derived but did not build)"
apply V "
import io
p='src/devices/dev_sgi_re.c'; s=io.open(p,encoding='utf-8').read()
a='\t\tif (writeflag == MEM_WRITE) {\n\t\t\tif (!(d->warned & SGIRE_W_UNMAP_WR)) {'
assert s.count(a)==1, s.count(a)
b='\t\tif (writeflag == MEM_WRITE && idata) {\n\t\t\tif (!(d->warned & SGIRE_W_UNMAP_WR)) {'
io.open(p,'w',encoding='utf-8',newline='').write(s.replace(a,b))
print('  V applied')
"
build_and_score V

say "RESTORE from SEC, REBUILD, verify BOTH clearance parts"
cd "$T"; cp "$SEC/$F" "$T/$F"
cmp -s "$T/$F" "$SEC/$F" || die "restore cmp FAILED, sentinel kept"
rm -f src/devices/dev_sgi_re.o; make -j4 > "$OUT/build_restore.log" 2>&1
if [ "$T/gxemul" -nt "$T/$F" ]; then rm -f "$T/.MUTANT"; say "  restored + REBUILT, sentinel cleared"
else say "  *** rebuild stale -- SENTINEL KEPT ***"; fi
say "KILL48_DONE"
