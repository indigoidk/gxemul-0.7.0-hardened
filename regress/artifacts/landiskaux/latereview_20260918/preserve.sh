#!/bin/bash
D=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/opus_landiskaux_20260918/logs
mkdir -p "$D"
cp /tmp/lax_boot_base_v0.log /tmp/lax_boot_fix_v0.log /tmp/lax_boot_base_v0_run2.log /tmp/lax_boot_winm1_v0.log \
   /tmp/lax_bootcd_base.log /tmp/lax_bootcd_fix.log "$D/"
for f in base_v1 fix_v1 winm1_v1; do
  L=/tmp/lax_boot_$f.log
  { echo "### EXTRACT of $L -- FULL SIZE $(wc -c < $L) bytes; kept: every ALT. CTRL / ALTSTATUS / DRIVE ADDRESS / non-existant line, in order"
    grep -a -o -E 'wdc: write to ALT\. CTRL: 0x[0-9a-f]+|wdc: read from ALTSTATUS[^]]*|wdc: write to DRIVE ADDRESS[^]]*|non-existant paddr=0x[0-9a-f]+ len=[0-9]+ pc=0x[0-9a-f]+' "$L"
    echo "### 'read from DATA' occurrences: $(grep -a -o 'wdc: read from DATA' $L | wc -l)"
    echo "### EXTRACT_COMPLETE"; } > "$D/boot_${f}_EXTRACT.log"
done
ls -la "$D"
