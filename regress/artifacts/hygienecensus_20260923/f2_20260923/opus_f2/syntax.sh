#!/bin/bash
cd /mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/opus_f2
python3 -c "import ast,io; ast.parse(io.open('edits.py',encoding='utf-8').read()); print('edits.py parses')"
python3 edits.py --desc n3m
python3 edits.py --desc e_e9
python3 --version; git --version
