#!/bin/bash
#  run_probe.sh <tag> <tree...> -- ONE frozen instrument for every tree in the comparison.
D=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/opus_landiskaux_20260918
TAG="$1"; shift
FROZEN=/tmp/lax_probe.frozen.$TAG.py
cp "$D/lax_probe.py" "$FROZEN"
echo "INSTRUMENT $(md5sum < "$FROZEN" | cut -c1-12) $FROZEN"
for T in "$@"; do
  B=/tmp/gxopus_lax_$T/gxemul
  echo "== $T  $(ls -la --time-style=full-iso "$B" | awk '{print $6, $7}')"
  python3 -u "$FROZEN" "$B" "$D/probe_${TAG}_$T.transcript" > "$D/probe_${TAG}_$T.out" 2>&1
  cat "$D/probe_${TAG}_$T.out"
done
echo RUN_PROBE_DONE
