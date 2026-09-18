#!/bin/bash
#  Copy the measurement record into the ONE repository path this seat may write.  No .bin files.
set -u
SRC=/mnt/c/DocumentNoSnc/CC/GXEMUL
WIN=/mnt/c/Users/User00/AppData/Local/Temp/opus530p2
DST="$SRC/GXEMUL-SEC/regress/artifacts/lcalenzerodrop/opus_p2_20260918"
LOGS=/tmp/gxopus530p2_logs
mkdir -p "$DST/logs" "$DST/variants" "$DST/scripts"
cp "$WIN/PREDICTIONS.txt" "$WIN/PREDICTIONS.stat.txt" "$WIN/README.md" "$WIN/RESULTS.txt" "$DST/"
cp "$WIN/lca_widecell_probe.py" "$DST/"
cp "$WIN"/variants/*.diff "$DST/variants/"
cp "$WIN/setup.sh" "$WIN/buildvariants.sh" "$WIN/run_matrix.sh" "$WIN/mkvariants.py" "$WIN/restore.sh" \
   "$WIN/summarize.py" "$WIN/collect.sh" "$DST/scripts/"
cp "$WIN"/setup.out "$WIN"/build.out "$WIN"/build2.out "$WIN"/build3.out "$WIN"/smoke.out \
   "$WIN"/matrix*.out "$DST/logs/" 2>/dev/null
[ -f "$WIN/restore.out" ] && cp "$WIN/restore.out" "$DST/logs/"
cp -r "$LOGS/smoke" "$DST/logs/"
cp "$LOGS"/*__*.log "$LOGS"/raw_*__*.txt "$LOGS"/build_*.log "$DST/logs/"
md5sum /tmp/gxopus530p2_bins/* > "$DST/logs/bins.md5"
find "$DST" -name '*.bin' -print -delete
echo "files: $(find "$DST" -type f | wc -l)"
du -sh "$DST"
echo "COLLECT_DONE"
