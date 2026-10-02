#!/bin/bash
# driver2.sh MUT1 MUT2 ...  -- panel mutants via mutate2.py; no base re-run (already have it).
set -u
CLONE=/tmp/gxopuscrimec5b
WD=/tmp/opuscrimec5
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
MUT=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/opuscrimec5/mutate2.py
PROBE="$WD/probe.py"
ORIG="$WD/dev_sgi_ip32.c.orig"
mkdir -p "$WD/logs"

run_probe () {
    local bin="$1" label="$2" out="$3"
    python3 -u "$PROBE" "$bin" "$label" > "$out" 2>&1
    local res last ctl fail
    res=$(grep -oE 'CRIMEP_RESULT=[0-9]+/[0-9]+' "$out" | tail -1)
    last=$(tail -1 "$out")
    ctl=$(grep -oE 'CRIMEP_CONTROL=(OK|FAIL)' "$out" | tail -1)
    fail=$(grep -E '^FAILING:' "$out" | tail -1)
    echo "  $label: $res $ctl last=[$last]"
    echo "  $fail"
}

for name in "$@"; do
    echo "=== mutant $name ==="
    python3 "$MUT" "$name" "$ORIG" "$WD/mut2_$name.c" || { echo "  MUTATE FAILED"; continue; }
    echo "$name applied" > "$CLONE/.MUTANT"
    cp "$WD/mut2_$name.c" "$CLONE/src/devices/dev_sgi_ip32.c"
    ( cd "$CLONE" && rm -f src/devices/dev_sgi_ip32.o gxemul && make >"$WD/build2_$name.log" 2>&1 )
    if [ ! -f "$CLONE/gxemul" ] || [ ! "$CLONE/gxemul" -nt "$CLONE/src/devices/dev_sgi_ip32.c" ]; then
        echo "  BUILD FAILED/STALE"; tail -6 "$WD/build2_$name.log"
        cp "$ORIG" "$CLONE/src/devices/dev_sgi_ip32.c"; rm -f "$CLONE/.MUTANT"; continue
    fi
    cp "$CLONE/gxemul" "$WD/gxemul_$name"
    run_probe "$WD/gxemul_$name" "$name" "$WD/logs/probe_$name.raw"
    cp "$ORIG" "$CLONE/src/devices/dev_sgi_ip32.c"
    if cmp -s "$CLONE/src/devices/dev_sgi_ip32.c" "$SEC/src/devices/dev_sgi_ip32.c"; then rm -f "$CLONE/.MUTANT"; else echo "  RESTORE MISMATCH"; fi
done

echo "=== FINAL RESTORE CHECK ==="
cp "$ORIG" "$CLONE/src/devices/dev_sgi_ip32.c"
if cmp -s "$CLONE/src/devices/dev_sgi_ip32.c" "$SEC/src/devices/dev_sgi_ip32.c"; then echo "CLONE SOURCE restored == SEC (clean)"; rm -f "$CLONE/.MUTANT"; else echo "CLONE SOURCE MISMATCH"; fi
echo "DRIVER2_DONE"
