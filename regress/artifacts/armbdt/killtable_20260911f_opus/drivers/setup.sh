#!/usr/bin/env bash
set -euo pipefail
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus524
F=/tmp/opus524_frozen
rm -rf "$F"; mkdir -p "$F"
tr -d '\r' < "$SP/mutate_opus.py" > "$F/mutate_opus.py"
tr -d '\r' < /mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/arm_bdt_probe.py > "$F/arm_bdt_probe.py"
tr -d '\r' < "$SP/table_opus.sh" > "$F/table_opus.sh"
chmod +x "$F"/*
python3 -c "import ast,sys; t=ast.parse(open('$F/arm_bdt_probe.py').read()); print('probe record() call sites:', sum(1 for n in ast.walk(t) if isinstance(n,ast.Call) and getattr(n.func,'id','')=='record'))"
bash -n "$F/table_opus.sh" && echo "driver parses"
echo FROZEN_OK
