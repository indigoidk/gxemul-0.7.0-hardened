#!/bin/bash
echo "python3: $(python3 --version 2>&1)  at $(command -v python3)"
echo "grep: $(grep --version | head -1)"
echo "bash: $BASH_VERSION"
echo "LANG=[${LANG:-}] LC_ALL=[${LC_ALL:-}] LC_CTYPE=[${LC_CTYPE:-}]"
locale 2>&1 | head -20
echo "--- lib.sh / run.sh locale settings:"
grep -nE 'LC_ALL|LANG|LC_CTYPE' /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/lib.sh /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/run.sh /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/tools/nightly_battery.sh 2>/dev/null | head -20
echo "--- tokenize on BOM str:"
python3 - <<'PY'
import io, tokenize, sys
for label, src in (("bom", "﻿x = 1\n"), ("cr_only", "#!x\rx = 1\ry = 2\r"), ("fstring", 'z = f"{buf.rstrip().endswith(\'GXemul>\')}"\n')):
    try:
        toks = list(tokenize.generate_tokens(io.StringIO(src).readline))
        print(label, "OK", [(tokenize.tok_name[t.type], t.string) for t in toks][:14])
    except Exception as e:
        print(label, "EXC", type(e).__name__, e)
print(sys.version)
PY
