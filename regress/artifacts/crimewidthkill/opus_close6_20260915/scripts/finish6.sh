#!/bin/bash
# finish6.sh -- preserve logs, instruments, scripts to the durable report dir; final clone check; delete clone + bins.
set -u
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
RPT="$SEC/regress/artifacts/crimewidthkill/opus_close6_20260915"
WD=/tmp/gxopuscrimec6_work
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opuscrimec6
CLONE=/tmp/gxopuscrimec6
mkdir -p "$RPT/logs" "$RPT/scripts" "$RPT/mutants"
for f in "$WD"/logs/*.raw; do
    tail -1 "$f" | grep -q CRIMEP_DONE || echo "WARNING: $(basename "$f") has no CRIMEP_DONE sentinel"
    cp "$f" "$RPT/logs/"
done
cp "$WD"/lane_*.out "$RPT/logs/"
cp "$WD/probe.frozen.py" "$RPT/scripts/crime_width_probe.frozen.py"
cp "$WD/probe.aug6.py" "$RPT/scripts/crime_width_probe.aug6.py"
for f in "$WD"/mut_*.c; do n=$(basename "$f" .c); diff -u "$WD/dev_sgi_ip32.c.orig" "$f" > "$RPT/mutants/${n#mut_}.diff"; done
cp "$SP"/*.py "$SP"/*.sh "$SP"/build6.out "$RPT/scripts/" 2>/dev/null
cmp -s "$RPT/scripts/crime_width_probe.frozen.py" "$SEC/regress/crime_width_probe.py" && echo "frozen probe still == shipped probe"
if [ -d "$CLONE" ]; then
    cmp -s "$CLONE/src/devices/dev_sgi_ip32.c" "$SEC/src/devices/dev_sgi_ip32.c" && echo "$CLONE: source CLEAN vs SEC" || echo "$CLONE: source MISMATCH"
    [ "$CLONE/gxemul" -nt "$CLONE/src/devices/dev_sgi_ip32.c" ] && echo "$CLONE: binary newer than source"
    [ -f "$CLONE/.MUTANT" ] && echo "$CLONE: SENTINEL PRESENT" || echo "$CLONE: no sentinel"
fi
ps -eo pid,args | grep -E '[g]xopuscrimec6' && echo "WARNING: processes still using the clone"
rm -rf "$CLONE" /tmp/gxopuscrimec6_bins "$WD"
[ -d "$CLONE" ] || echo "CLONE, BINS AND WORKDIR DELETED"
ls "$RPT/logs" | wc -l
echo "FINISH6_DONE"
