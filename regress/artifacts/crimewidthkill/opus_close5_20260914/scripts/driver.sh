#!/bin/bash
# driver.sh MUT1 MUT2 ...  -- build each mutant into the clone (device relink only), run the frozen probe, record score.
set -u
CLONE=/tmp/gxopuscrimec5
WD=/tmp/opuscrimec5
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
MUT=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/opuscrimec5/mutate.py
PROBE="$WD/probe.py"
ORIG="$WD/dev_sgi_ip32.c.orig"
mkdir -p "$WD/logs"

run_probe () {
    local bin="$1" label="$2" out="$3"
    python3 -u "$PROBE" "$bin" "$label" > "$out" 2>&1
    local res last ctl
    res=$(grep -oE 'CRIMEP_RESULT=[0-9]+/[0-9]+' "$out" | tail -1)
    last=$(tail -1 "$out")
    ctl=$(grep -oE 'CRIMEP_CONTROL=(OK|FAIL)' "$out" | tail -1)
    echo "  $label: $res $ctl last=[$last]"
}

echo "=== base re-run (gxemul_base) ==="
run_probe "$WD/gxemul_base" "base" "$WD/logs/probe_base.raw"

for name in "$@"; do
    echo "=== mutant $name ==="
    python3 "$MUT" "$name" "$ORIG" "$WD/mut_$name.c" || { echo "  MUTATE FAILED"; continue; }
    echo "$name applied" > "$CLONE/.MUTANT"
    cp "$WD/mut_$name.c" "$CLONE/src/devices/dev_sgi_ip32.c"
    ( cd "$CLONE" && rm -f src/devices/dev_sgi_ip32.o gxemul && make >"$WD/build_$name.log" 2>&1 )
    if [ ! -f "$CLONE/gxemul" ] || [ ! "$CLONE/gxemul" -nt "$CLONE/src/devices/dev_sgi_ip32.c" ]; then
        echo "  BUILD FAILED/STALE"; tail -6 "$WD/build_$name.log"
        cp "$ORIG" "$CLONE/src/devices/dev_sgi_ip32.c"; rm -f "$CLONE/.MUTANT"; continue
    fi
    cp "$CLONE/gxemul" "$WD/gxemul_$name"
    run_probe "$WD/gxemul_$name" "$name" "$WD/logs/probe_$name.raw"
    # restore source and verify clean vs SEC
    cp "$ORIG" "$CLONE/src/devices/dev_sgi_ip32.c"
    if cmp -s "$CLONE/src/devices/dev_sgi_ip32.c" "$SEC/src/devices/dev_sgi_ip32.c"; then rm -f "$CLONE/.MUTANT"; else echo "  RESTORE MISMATCH"; fi
done

echo "=== FINAL RESTORE CHECK ==="
cp "$ORIG" "$CLONE/src/devices/dev_sgi_ip32.c"
if cmp -s "$CLONE/src/devices/dev_sgi_ip32.c" "$SEC/src/devices/dev_sgi_ip32.c"; then echo "CLONE SOURCE restored == SEC (clean)"; rm -f "$CLONE/.MUTANT"; else echo "CLONE SOURCE MISMATCH"; fi
echo "DRIVER_DONE"
