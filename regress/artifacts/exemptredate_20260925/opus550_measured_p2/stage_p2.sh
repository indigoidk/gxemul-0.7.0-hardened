set -u
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad
cd /tmp/opus550p2 || exit 1
cp $S/p2/sched550v2.py .
cp exp/tools/pipeline/check_probe_wiring.py cpw_HEAD_export.py
cp $S/exempt550/cpw_550v2_onHEAD.py exp/tools/pipeline/check_probe_wiring.py
cp $S/exempt550/pcc_550v2_onHEAD.sh exp/tools/precommit_check.sh
cp $S/exempt550/goff_550v2.sh exp/regress/gate_offline.sh
echo "export .py files: $(find exp/regress -name '*.py' | wc -l)"
cmp -s exp/tools/pipeline/check_probe_wiring.py $S/exempt550/cpw_550v2_onHEAD.py && echo "checker in export == cpw_550v2_onHEAD.py"
cmp -s cpw_HEAD_export.py $S/exempt550/cpw_HEAD.py && echo "export's HEAD checker == exempt550/cpw_HEAD.py"
