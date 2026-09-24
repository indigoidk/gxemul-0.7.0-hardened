#!/usr/bin/env python3
# Proper backslash line-continuation test, built with chr(92) so the backslash survives (carrier rule).
import io, os, subprocess, sys, tempfile
CT = "/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/c4_frozen/census_tokens.py"
BASE = tempfile.mkdtemp(prefix="gxcont_")
EW = "ends" + "with"; BS = chr(92)
# real continuation: 'buf.rstrip() <backslash><newline>   .endswith("GXemul>")'
cont = "x = buf.rstrip() " + BS + "\n     ." + EW + "(\"GXemul>\")\n"
io.open(os.path.join(BASE, "cont.py"), "w", encoding="utf-8", newline="").write(cont)
# also: continuation between the arg tokens
cont2 = "x = buf.rstrip()." + EW + "(" + BS + "\n     \"GXemul>\")\n"
io.open(os.path.join(BASE, "cont2.py"), "w", encoding="utf-8", newline="").write(cont2)
print("cont.py bytes:", repr(io.open(os.path.join(BASE,"cont.py"),encoding="utf-8").read()))
for mode in ("promptless", "whole"):
    r = subprocess.run([sys.executable, CT, mode, BASE], input="cont.py\ncont2.py\n", capture_output=True, text=True)
    print("%-11s rc=%d out=[%s]" % (mode, r.returncode, r.stdout.strip().replace("\n", " | ")))
# and show tokenize handles it
import tokenize
for f in ("cont.py", "cont2.py"):
    src = io.open(os.path.join(BASE, f), encoding="utf-8").read()
    try:
        toks = [(tokenize.tok_name[t.type], t.string) for t in tokenize.generate_tokens(io.StringIO(src).readline)
                if t.type not in (tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT, tokenize.COMMENT, tokenize.ENCODING, tokenize.ENDMARKER)]
        print(f, "tokens OK:", toks)
    except Exception as e:
        print(f, "EXC", type(e).__name__, e)
print("S2_CONT_DONE")
