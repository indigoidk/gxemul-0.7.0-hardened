SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
#  ANCHOR ON THE LOG VARIABLE, never on the list's own first names: gate_arm.sh has several
#  `for v in "live" ...' loops and the first match belongs to a DIFFERENT probe.
LN=$(grep -n 'count "\$PCC2LOG" "\^\$v' "$SEC/regress/gate_arm.sh" | cut -d: -f1)
echo "check line for \$PCC2LOG: $LN ; list line: $((LN-1))"
sed -n "$((LN-1))p" "$SEC/regress/gate_arm.sh" | grep -o '"[^"]*"' | tr -d '"' | sort > /tmp/p8_gate_names.txt
sed -n '/^pcc2widthkills DETECTOR/,$p' /tmp/gxopus_p8/p8/probe_BASE.txt \
  | grep -E ' (ok|FAIL)$' | cut -c1-16 | sed 's/ *$//' | sort > /tmp/p8_probe_names.txt
echo "probe names: $(wc -l < /tmp/p8_probe_names.txt)   gate names: $(wc -l < /tmp/p8_gate_names.txt)"
echo "--- symmetric difference ---"; comm -3 /tmp/p8_probe_names.txt /tmp/p8_gate_names.txt
echo "--- diff count: $(comm -3 /tmp/p8_probe_names.txt /tmp/p8_gate_names.txt | wc -l) ---"
