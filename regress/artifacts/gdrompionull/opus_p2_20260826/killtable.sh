#!/bin/bash
#  #465 pass-2 opus seat kill table.  Runs entirely inside the scratch copy.
set -u
T=/tmp/gx465p2
OUT=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/p465
SRC=$T/src/devices/dev_dreamcast_gdrom.c
SHIPPROBE=$T/regress/artifacts/gdrompionull/gdrom_pio_null_probe.py
MISMPROBE=$OUT/mism_probe.py
KERNEL=/mnt/c/DocumentNoSnc/CC/GXEMUL/_images/openbsd76-landisk-bsd.rd

score () {   #  $1 = build label
    L=$1
    echo "===== $L ====="
    python3 "$OUT/mutate.py" "$L" || return 9
    echo "$L $SRC mutated" > "$T/.MUTANT"
    cd "$T" || return 9
    make > "$OUT/make_$L.log" 2>&1
    RC=$?
    if [ ! -f "$T/gxemul" ] || [ ! "$T/gxemul" -nt "$SRC" ]; then
        echo "BUILD_FAIL $L rc=$RC (binary not newer than source)"
        tail -20 "$OUT/make_$L.log"
        return 9
    fi
    echo "BUILD_OK $L rc=$RC"
    python3 "$SHIPPROBE" "$T/gxemul" "$KERNEL" > "$OUT/ship_$L.raw" 2>&1
    python3 "$MISMPROBE" "$T/gxemul" "$KERNEL" > "$OUT/mism_$L.raw" 2>&1
    grep -h 'GDROMPIO_RESULT\|GDROMPIO_VECTOR' "$OUT/ship_$L.raw"
    grep -h 'MISM_RESULT\|MISM_VECTOR' "$OUT/mism_$L.raw"
    echo "--- ship FAIL rows:"; grep '  FAIL$\|FAIL$' "$OUT/ship_$L.raw" | sed 's/^/    /'
    echo "--- mism FAIL rows:"; grep 'FAIL$' "$OUT/mism_$L.raw" | sed 's/^/    /'
}

for m in base Md_nolen Mret429 Mret420 Mtail Mtailret; do
    if [ "$m" = base ]; then
        python3 "$OUT/mutate.py" restore
        rm -f "$T/.MUTANT"
        cd "$T" && make > "$OUT/make_base2.log" 2>&1
        echo "===== base ====="
        echo "BUILD_OK base rc=$?"
        python3 "$SHIPPROBE" "$T/gxemul" "$KERNEL" > "$OUT/ship_base.raw" 2>&1
        python3 "$MISMPROBE" "$T/gxemul" "$KERNEL" > "$OUT/mism_base.raw" 2>&1
        grep -h 'GDROMPIO_RESULT\|GDROMPIO_VECTOR' "$OUT/ship_base.raw"
        grep -h 'MISM_RESULT\|MISM_VECTOR' "$OUT/mism_base.raw"
        echo "--- ship FAIL rows:"; grep 'FAIL$' "$OUT/ship_base.raw" | sed 's/^/    /'
        echo "--- mism FAIL rows:"; grep 'FAIL$' "$OUT/mism_base.raw" | sed 's/^/    /'
    else
        score "$m"
    fi
done

python3 "$OUT/mutate.py" restore
cd "$T" && make > "$OUT/make_restore.log" 2>&1
if cmp -s "$SRC" /mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/dev_dreamcast_gdrom.c; then
    rm -f "$T/.MUTANT"; echo "RESTORE VERIFIED by cmp against GXEMUL-SEC; sentinel cleared"
else
    echo "RESTORE FAILED -- sentinel LEFT IN PLACE"
fi
echo "KILLTABLE DONE"
