#!/bin/bash
#  #490 pass-2 ASK-AGAIN: measure phase.  Serial runs, one frozen instrument, per-run
#  identity controls.  Script file, not `bash -c`.
set -u

OUT=/tmp/gxopus490p2_out
BINS=/tmp/gxopus490p2_bins
FROZEN=/tmp/gxopus490p2_probe.py
PIN_PROBE=/tmp/r2m_pinned/gdrom_decline_probe.py.FROZEN
KERNEL=/mnt/c/DocumentNoSnc/cc/GXEMUL/_images/openbsd76-landisk-bsd.rd
PROBE_MD5=188e92ebd8f9593664c294c63fed0d98

mkdir -p "$OUT"

#  FREEZE MY OWN COPY of the instrument -- a comparison run owes ONE instrument, and the
#  pinned file lives in a directory another session writes to.
cp "$PIN_PROBE" "$FROZEN"
got=$(md5sum "$FROZEN" | cut -d' ' -f1)
echo "instrument md5 $got"
if [ "$got" != "$PROBE_MD5" ]; then
    echo "MEASURE490P2_ABORT: instrument md5 mismatch (want $PROBE_MD5)"; exit 1
fi
if [ ! -f "$KERNEL" ]; then
    echo "MEASURE490P2_ABORT: kernel missing"; exit 1
fi

echo "=== MEASURE490P2 START $(date -Is) ==="

for tag in base E1_aliasover E2_assignA E3_widenA; do
    log="$OUT/probe_${tag}.log"
    {
        echo "PROBE_TAG=$tag"
        echo "PROBE_BIN=$BINS/$tag"
        echo "PROBE_BIN_MD5=$(md5sum "$BINS/$tag" | cut -d' ' -f1)"
        echo "PROBE_INSTRUMENT_MD5=$(md5sum "$FROZEN" | cut -d' ' -f1)"
        echo "PROBE_START=$(date -Is)"
    } > "$log"
    python3 -u "$FROZEN" "$BINS/$tag" "$KERNEL" >> "$log" 2>&1
    rc=$?
    {
        echo "PROBE_RC=$rc"
        echo "PROBE_END=$(date -Is)"
        echo "P2ASK_DONE"
    } >> "$log"
    echo "--- $tag: $(grep -o 'GDROM_DECL_RESULT=[0-9]*/[0-9]*' "$log" | tail -1)  control=$(grep -o 'GDROM_DECL_CONTROL=[A-Z]*' "$log" | tail -1)  rc=$rc"
done

echo "=== SUMMARY ==="
for tag in base E1_aliasover E2_assignA E3_widenA; do
    log="$OUT/probe_${tag}.log"
    printf "%-14s %-24s %s\n" "$tag" \
        "$(grep -o 'GDROM_DECL_RESULT=[0-9]*/[0-9]*' "$log" | tail -1)" \
        "$(grep -c ' FAIL$' "$log") failing rows"
    grep ' FAIL$' "$log" | sed 's/^/      /'
done
echo "=== MEASURE490P2_DONE $(date -Is) ==="
