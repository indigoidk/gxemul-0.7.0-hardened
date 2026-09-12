#!/usr/bin/env bash
set -euo pipefail
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus524
tr -d '\r' < "$SP/ldmdb_control.py" > /tmp/opus524_frozen/ldmdb_control.py
tr -d '\r' < "$SP/control_run.sh"   > /tmp/opus524_frozen/control_run.sh
chmod +x /tmp/opus524_frozen/*
python3 -c "import ast;ast.parse(open('/tmp/opus524_frozen/ldmdb_control.py').read());print('control parses')"
bash -n /tmp/opus524_frozen/control_run.sh && echo "runner parses"
