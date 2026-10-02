#!/bin/bash
# run_rows.sh <variant...> -- runs a FROZEN copy of the rows probe (and the committed witness) against each binary
set -u
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
B=/tmp/gxopuscrime_bins
O=/tmp/gxopuscrime_out
mkdir -p "$O"
cp "$SP/crime_opus_rows.py" "$O/crime_opus_rows.FROZEN.py"
cp "$SEC/regress/artifacts/crimewidthkill/crime_width_witness_20260913.py" "$O/witness.FROZEN.py"
md5sum "$O/crime_opus_rows.FROZEN.py" "$O/witness.FROZEN.py"
for v in "$@"; do
    if [ "${WITNESS:-1}" = 1 ]; then
        python3 -u "$O/witness.FROZEN.py" "$B/$v" "$v" > "$O/witness_$v.out" 2>&1
        echo "WITNESS $v: $(grep -E 'CRIMEW_RESULT|CRIMEW_CONTROL' "$O/witness_$v.out" | tr '\n' ' ') $(tail -1 "$O/witness_$v.out")"
    fi
    python3 -u "$O/crime_opus_rows.FROZEN.py" "$B/$v" "$v" > "$O/rows_$v.out" 2>&1
    echo "ROWS $v: $(tail -1 "$O/rows_$v.out")"
done
echo RUN_ROWS_DONE
