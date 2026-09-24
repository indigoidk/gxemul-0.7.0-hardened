#!/bin/bash
echo "--- WSL: TZ=America/Sao_Paulo date -d 2018-11-04 +%F -> [$(TZ=America/Sao_Paulo date -d 2018-11-04 +%F 2>&1)]"
for d in 0000-01-01 0001-01-01 9999-12-31; do printf '    WSL  date -d %s +%%F -> %s\n' "$d" "$(date -d $d +%F 2>&1)"; done
echo DATES_WSL_DONE
