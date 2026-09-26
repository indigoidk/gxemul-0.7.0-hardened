set -u
mkdir -p /tmp/opus550f2b && cd /tmp/opus550f2b || exit 1
cp /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/wdc_altoffset_probe.py .
cp /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/f2b/rows_wb_wf.py .
python3 rows_wb_wf.py wdc_altoffset_probe.py
