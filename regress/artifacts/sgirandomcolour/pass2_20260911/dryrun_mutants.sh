#!/bin/bash
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/p2
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
BL=$SEC/regress/artifacts/sgirandomcolour/killtable3_20260910/BASELINE_FIX519_T3.c
echo "python3: $(python3 --version 2>&1)"
echo "=== DRY RUN: every mutant applied to a FRESH copy of the named baseline ==="
for m in M28r_permit_othernib M30_tilenrdecline M31_tilenrguard M32_tilenrxdecline M33_tiledorigin; do
    cp "$BL" /tmp/dry.c
    out=$(python3 "$SP/mut519p2.py" /tmp/dry.c "$m" 2>&1); rc=$?
    if [ $rc -ne 0 ]; then
        printf '%-24s rc=%d  *** %s ***\n' "$m" "$rc" "$out"
    else
        d=$(diff "$BL" /tmp/dry.c | grep -c '^[<>]')
        printf '%-24s rc=0  %s  (diff lines: %s)\n' "$m" "$out" "$d"
        diff "$BL" /tmp/dry.c | sed 's/^/      /'
    fi
done
echo "=== negative control: a bogus mutant name must be REFUSED ==="
cp "$BL" /tmp/dry.c
python3 "$SP/mut519p2.py" /tmp/dry.c M99_doesnotexist; echo "rc=$?"
echo "=== negative control: applying to an ALREADY-MUTATED file must be REFUSED (presence pin) ==="
cp "$BL" /tmp/dry.c
python3 "$SP/mut519p2.py" /tmp/dry.c M30_tilenrdecline >/dev/null
python3 "$SP/mut519p2.py" /tmp/dry.c M30_tilenrdecline; echo "rc=$? (9 = correct: find-string consumed)"
rm -f /tmp/dry.c
