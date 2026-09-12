#!/bin/bash
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
echo "=== DRY RUN: every mutant applied to a fresh copy of SEC's dev_sgi_re.c ==="
for m in M1_reinstate M2_noguard M3_zerofill M4_okinlatch M5_nolatch M6_sharedbit M7_silent \
         M8_declineall M9_dropcase_ci M10_dropcase_abgr M11_null M12_prefix_reworded \
         M16_dropcase_rgb M17_dropcase_rgba M13_widthdecline M14_lineardecline M15_jointwidthlin \
         M20_permit_tlba M21_permit_tlbb M22_permit_tlbc M23_permit_tiled_d4 \
         M24_permit_d2d8 M25_permit_d8 M26_permit_d2 M27_permit_bc_d2d8 M28_permit_othernibbles; do
    cp "$SEC/src/devices/dev_sgi_re.c" /tmp/o519dry.c
    out=$(python3 "$SP/mut519c.py" /tmp/o519dry.c "$m" 2>&1); rc=$?
    n=$(diff "$SEC/src/devices/dev_sgi_re.c" /tmp/o519dry.c | grep -cE '^[<>]')
    printf '%-22s rc=%-2s %-46s changed-lines=%s\n' "$m" "$rc" "$out" "$n"
done
rm -f /tmp/o519dry.c
