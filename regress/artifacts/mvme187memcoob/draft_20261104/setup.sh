#!/bin/bash
# Create the two scratch clones (cp -a keeps timestamps).  Read-only sources.
set -e
B=/mnt/c/DocumentNoSnc/cc/GXEMUL
rm -rf /tmp/gxopus_memc /tmp/gxopus_memc_asan
cp -a "$B/build"      /tmp/gxopus_memc
cp -a "$B/build-asan" /tmp/gxopus_memc_asan
echo "clone plain: $(du -sh /tmp/gxopus_memc | cut -f1)"
echo "clone asan:  $(du -sh /tmp/gxopus_memc_asan | cut -f1)"
# both must start byte-identical to SEC
for t in /tmp/gxopus_memc /tmp/gxopus_memc_asan; do
    if cmp -s "$t/src/devices/dev_mvme187.c" "$B/GXEMUL-SEC/src/devices/dev_mvme187.c"; then
        echo "$t dev_mvme187.c == SEC (baseline clean)"
    else
        echo "$t dev_mvme187.c DIFFERS from SEC -- STOP"; exit 1
    fi
done
echo SETUP_DONE
