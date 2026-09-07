#!/bin/bash
# pass-5 seat measurement (kimi): two mutants x two probes on the m88k exception composite.
# All paths absolute; no positional-param tricks (they got mangled through wsl bash -lc).
cd /tmp/gxkimi502 || exit 1
V5=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/m88kexcdeliver/killtable5/m88k_exc_probe.frozen5.py
V5P2=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/pass5_kimi_p502/m88k_exc_probe_v5p2.py

run() {
  name="$1"; probe="$2"; bin="$3"
  echo "=== RUN $name (probe=$(basename "$probe") bin=$(basename "$bin")) ==="
  python3 "$probe" "$bin" > "/tmp/gxkimi502/res_${name}.out" 2>&1
  grep -E "M88KEXC_RESULT=|M88KEXC_SELFTEST=|M88KEXC_CONTROLS=" "/tmp/gxkimi502/res_${name}.out"
  grep -E "M88KEXC_ROW=(trapfrzmis|usfu1) " "/tmp/gxkimi502/res_${name}.out"
}

run v5_fix            "$V5"   /tmp/gxkimi502/gxemul.fix
run v5_m_sfrztbmis    "$V5"   /tmp/gxkimi502/gxemul.m_sfrztbmis
run v5_m_fbsuponly    "$V5"   /tmp/gxkimi502/gxemul.m_fbsuponly
run v5p2_fix          "$V5P2" /tmp/gxkimi502/gxemul.fix
run v5p2_m_sfrztbmis  "$V5P2" /tmp/gxkimi502/gxemul.m_sfrztbmis
run v5p2_m_fbsuponly  "$V5P2" /tmp/gxkimi502/gxemul.m_fbsuponly
echo ALL-RUNS-DONE
