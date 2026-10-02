#!/bin/bash
set -u
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
RPT="$SEC/regress/artifacts/crimewidthkill/opus_close5_20260914"
WD=/tmp/opuscrimec5
mkdir -p "$RPT/logs" "$RPT/scripts"
# preserve logs + scripts to durable path
cp "$WD"/logs/*.raw "$RPT/logs/" 2>/dev/null
cp /mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/opuscrimec5/*.py /mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/opuscrimec5/*.sh "$RPT/scripts/" 2>/dev/null
cp "$WD/probe_aug.py" "$RPT/scripts/" 2>/dev/null
# final restore checks
for C in /tmp/gxopuscrimec5 /tmp/gxopuscrimec5b; do
    if [ -d "$C" ]; then
        if cmp -s "$C/src/devices/dev_sgi_ip32.c" "$SEC/src/devices/dev_sgi_ip32.c"; then echo "$C: source CLEAN vs SEC"; else echo "$C: source MISMATCH"; fi
        [ -f "$C/.MUTANT" ] && echo "$C: SENTINEL PRESENT" || echo "$C: no sentinel"
    fi
done
# delete clones
rm -rf /tmp/gxopuscrimec5 /tmp/gxopuscrimec5b
echo "CLONES DELETED"
ls "$RPT/logs" | wc -l
echo "FINISH_DONE"
