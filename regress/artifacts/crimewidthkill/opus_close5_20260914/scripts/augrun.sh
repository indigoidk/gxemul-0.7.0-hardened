#!/bin/bash
# augrun.sh -- run the AUGMENTED probe (ACCEPTS + ldP + CONTROL 0x100) against base and the P1/P2 survivor binaries.
set -u
WD=/tmp/opuscrimec5
AUG="$WD/probe_aug.py"
python3 /mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/opuscrimec5/augprobe.py "$WD/probe.py" "$AUG"
# sanity: same row count as shipped
echo "row() sites shipped=$(grep -c 'row(' "$WD/probe.py")  aug=$(grep -c 'row(' "$AUG")"
mkdir -p "$WD/logs"
for b in base P1_win8r_rearm P1b_win8r_preset P2_ctl_endi_rearm P2b_ctl_endi_preset; do
    bin="$WD/gxemul_$b"
    [ -f "$bin" ] || { echo "  (no binary $b yet)"; continue; }
    python3 -u "$AUG" "$bin" "aug_$b" > "$WD/logs/aug_$b.raw" 2>&1
    res=$(grep -oE 'CRIMEP_RESULT=[0-9]+/[0-9]+' "$WD/logs/aug_$b.raw" | tail -1)
    ctl=$(grep -oE 'CRIMEP_CONTROL=(OK|FAIL)' "$WD/logs/aug_$b.raw" | tail -1)
    fail=$(grep -E '^FAILING:' "$WD/logs/aug_$b.raw" | tail -1)
    echo "  aug_$b: $res $ctl  $fail"
done
echo "AUGRUN_DONE"
