set -e
cd /tmp/gxopus_p8
python3 /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/pcc2p8_opus/mk_f1.py
diff <(sed 's/^ *//' p8/frozen_probe.py) <(sed 's/^ *//' p8/f1_probe.py) | head -0 || true
echo "--- lines added: $(( $(wc -l < p8/f1_probe.py) - $(wc -l < p8/frozen_probe.py) )) ---"
python3 -u p8/f1_probe.py /tmp/gxopus_p8/gxemul F1 > /tmp/gxopus_p8/p8/f1_out.txt 2> /tmp/gxopus_p8/p8/f1_err.txt || true
echo "=== STDERR (F1 diagnostics) ==="
grep -E "^F1" /tmp/gxopus_p8/p8/f1_err.txt
echo "=== the four rows this reached ==="
grep -E "pend2|^live|^devsig" /tmp/gxopus_p8/p8/f1_out.txt | head
