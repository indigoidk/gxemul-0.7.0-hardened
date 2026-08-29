#!/bin/bash
#  #490 SUPPLEMENTARY pass 2, measuring seat.
#  NO BUILD: the ask-again's mutant binaries survive and their md5s were verified
#  against RESULTS.md before this ran.  Read-only against every project tree.
set -u
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/assertattack
OUT=/tmp/gxsupp490_out
BINS=/tmp/gxopus490p2_bins
PIN=/tmp/r2m_pinned/gdrom_decline_probe.py.FROZEN
FROZEN=/tmp/gxsupp490_probe.py
KERNEL=/mnt/c/DocumentNoSnc/cc/GXEMUL/_images/openbsd76-landisk-bsd.rd
PIN_MD5=188e92ebd8f9593664c294c63fed0d98

mkdir -p "$OUT"
got=$(md5sum "$PIN" | cut -d' ' -f1)
[ "$got" = "$PIN_MD5" ] || { echo "SUPP_ABORT: pinned instrument md5 $got != $PIN_MD5"; exit 1; }
[ -f "$KERNEL" ] || { echo "SUPP_ABORT: kernel missing"; exit 1; }

#  ONE instrument, frozen once, used for all three runs.
python3 "$SP/extend.py" "$PIN" "$FROZEN" || { echo "SUPP_ABORT: extend failed"; exit 1; }
python3 -c "import ast,sys; ast.parse(open(sys.argv[1]).read())" "$FROZEN" \
    || { echo "SUPP_ABORT: extended instrument does not parse"; exit 1; }
INST=$(md5sum "$FROZEN" | cut -d' ' -f1)
echo "extended instrument md5 $INST  (from pinned $PIN_MD5)"

echo "=== SUPP490 START $(date -Is) ==="
for tag in base E2_assignA E3_widenA; do
    log="$OUT/probe_${tag}.log"
    {
      echo "PROBE_TAG=$tag"
      echo "PROBE_BIN_MD5=$(md5sum "$BINS/$tag" | cut -d' ' -f1)"
      echo "PROBE_INSTRUMENT_MD5=$INST"
      echo "PROBE_START=$(date -Is)"
    } > "$log"
    python3 -u "$FROZEN" "$BINS/$tag" "$KERNEL" >> "$log" 2>&1
    rc=$?
    { echo "PROBE_RC=$rc"; echo "PROBE_END=$(date -Is)"; echo "SUPP490_DONE"; } >> "$log"
    echo "--- $tag  $(grep -o 'GDROM_DECL_RESULT=[0-9]*/[0-9]*' "$log" | tail -1)  control=$(grep -o 'GDROM_DECL_CONTROL=[A-Z]*' "$log" | tail -1)  rc=$rc"
done

echo
echo "=== THE TWO CANDIDATE ROWS ==="
printf "%-16s %-22s %-22s %s\n" "row" "base" "E2_assignA" "E3_widenA"
for v in "latch keep" "both sites rev"; do
    line=""
    for tag in base E2_assignA E3_widenA; do
        r=$(grep "^$v  " "$OUT/probe_${tag}.log" | tail -1 | sed 's/  */ /g' | cut -c1-40)
        line="$line|$r"
    done
    echo "  $v => $line"
done
echo
echo "=== FULL FAIL LISTS ==="
for tag in base E2_assignA E3_widenA; do
    echo "--- $tag: $(grep -c ' FAIL$' "$OUT/probe_${tag}.log") failing"
    grep ' FAIL$' "$OUT/probe_${tag}.log" | sed 's/^/      /'
done
echo "=== SUPP490_ALLDONE $(date -Is) ==="
