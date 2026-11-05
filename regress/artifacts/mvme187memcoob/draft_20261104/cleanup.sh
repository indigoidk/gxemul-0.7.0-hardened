#!/bin/bash
rm -rf /tmp/gxopus_memc /tmp/gxopus_memc_asan
echo "removed: $(ls -d /tmp/gxopus_memc /tmp/gxopus_memc_asan 2>&1)"
echo "SEC still clean: $(cmp -s /mnt/c/DocumentNoSnc/cc/GXEMUL/build/src/devices/dev_mvme187.c /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/devices/dev_mvme187.c && echo yes || echo NO)"
ls -la /mnt/c/DocumentNoSnc/cc/GXEMUL/build/.MUTANT /mnt/c/DocumentNoSnc/cc/GXEMUL/build-asan/.MUTANT 2>&1
echo CLEANUP_DONE
