#!/bin/bash
#  sgirandompixel kill table.  Predictions are in PRETABLE_sgirandom.out, written before the first build.
#  Scratch clone by default; no project tree is mutated.
set -u
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
OUT=$SEC/regress/artifacts/sgirandompixel/killtable
CLONE=/tmp/gxsgir
SRC=src/devices/dev_sgi_re.c
mkdir -p "$OUT"

[ -d "$CLONE" ] || cp -a /mnt/c/DocumentNoSnc/CC/GXEMUL/build "$CLONE" || exit 9
cp "$SEC/$SRC" "$CLONE/$SRC"
cmp -s "$CLONE/$SRC" "$SEC/$SRC" || { echo "BASELINE MISMATCH"; exit 9; }
echo "baseline: clone == SEC (post-fix working set)"

PROBE=/tmp/sgirand_frozen.py
cp "$SEC/regress/sgi_re_randompixel_probe.py" "$PROBE"
echo "frozen probe: $(md5sum $PROBE | cut -c1-8)"

build() {
    rm -f "$CLONE/src/devices/dev_sgi_re.o" "$CLONE/src/devices/devices.a" "$CLONE/gxemul" 2>/dev/null
    ( cd "$CLONE" && make -j4 ) > /tmp/ksgi.log 2>&1
    [ -x "$CLONE/gxemul" ] && [ "$CLONE/gxemul" -nt "$CLONE/$SRC" ]
}
run() {
    timeout 300 python3 -u "$PROBE" "$CLONE/gxemul" "$1" > "$OUT/$1.out" 2>&1
    grep -oE 'SGIRAND_RESULT=[0-9]+/[0-9]+' "$OUT/$1.out" | tail -1
}
mutate() {
    python3 - "$CLONE/$SRC" "$1" "$2" <<'PY'
import io, sys
p, a, b = sys.argv[1], sys.argv[2], sys.argv[3]
s = io.open(p, encoding='utf-8').read()
if s.count(a) != 1:
    print("MUTANT-TEXT-NOT-FOUND count=%d" % s.count(a)); sys.exit(9)
io.open(p, 'w', encoding='utf-8', newline='\n').write(s.replace(a, b))
print("applied")
PY
}
restore() { cp "$SEC/$SRC" "$CLONE/$SRC"; cmp -s "$CLONE/$SRC" "$SEC/$SRC" || { echo RESTORE-FAILED; exit 9; }; }

GUARD='		if (!(d->warned & SGIRE_W_BADMODE)) {
			d->warned |= SGIRE_W_BADMODE;'

echo "=== BASE (opening) ==="
echo "gxsgir BASE" > "$CLONE/.MUTANT"
build || { echo "BASE BUILD FAILED"; tail -6 /tmp/ksgi.log; exit 9; }
rm -f "$CLONE/.MUTANT"
echo "  $(run BASE)"

m() {   # $1 tag, $2 find, $3 replace
    echo "=== $1 ==="
    echo "gxsgir $1" > "$CLONE/.MUTANT"
    if mutate "$2" "$3"; then
        if build; then echo "  $(run $1)"; else echo "  BUILD FAILED"; tail -4 /tmp/ksgi.log; fi
    fi
    restore; rm -f "$CLONE/.MUTANT"
}

#  (b) VERBATIM reinstatement: the random() assignment AND the original UNLATCHED announce.  The first
#  attempt used `if (0)', which also silenced the announce -- the mutant then reddened THREE rows and
#  died for two reasons, so the kill was not attributable to the value channel.  `if (1)' reproduces
#  the pre-fix behaviour exactly: announce every call, and assign random().
m M_RANDOM "$GUARD" "		*color = random();
		if (1) {"

#  (d) the guard kept, its repair nulled
m M_ZERO "$GUARD" "		*color = 0;
		if (!(d->warned & SGIRE_W_BADMODE)) {
			d->warned |= SGIRE_W_BADMODE;"

#  the latch dropped: announce becomes per-pixel
m M_NOLATCH "$GUARD" "		if (1) {
			d->warned |= SGIRE_W_BADMODE;"

#  member 2 instead of member 3: decline silently
m M_SILENT "$GUARD" "		if (0) {
			d->warned |= SGIRE_W_BADMODE;"

#  restore the host kill
m M_EXIT "$GUARD" "		exit(1);
		if (!(d->warned & SGIRE_W_BADMODE)) {
			d->warned |= SGIRE_W_BADMODE;"

echo "=== BASE (closing) -- a closing BASE that is not 8/8 VOIDS the table ==="
build || { echo "CLOSING BUILD FAILED"; exit 9; }
echo "  $(run BASE_final)"
cmp -s "$CLONE/$SRC" "$SEC/$SRC" && echo "clone CLEAN vs SEC" || echo "*** CLONE DIRTY ***"
ls "$CLONE/.MUTANT" 2>/dev/null && echo "*** SENTINEL LEFT ***" || echo "no sentinel left"
echo KILLSGI_DONE
