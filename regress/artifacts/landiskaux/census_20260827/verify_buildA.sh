#!/bin/bash
B=/tmp/gxcensusA/gxemul
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
echo "binary: $(ls -la $B)"
for s in src/devices/dev_wdc.c src/cpus/memory_rw.c src/machines/machine_landisk.c src/core/memory.c src/debugger/debugger_cmds.c; do
    if [ "$B" -nt "/tmp/gxcensusA/$s" ]; then fr="FRESH"; else fr="***STALE***"; fi
    if cmp -s "/tmp/gxcensusA/$s" "$SEC/$s"; then id="IDENTICAL-TO-SEC"; else id="***DIFFERS-FROM-SEC***"; fi
    echo "$fr $id $s"
done
