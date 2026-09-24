#!/usr/bin/env python3
# P6 -- can any FILE CONTENT make the F5 classifier (98788b1b) stop partway?  Each pathological file is followed by a
# normal promptless file "after.py"; if the run dies at the pathological one, "after.py" is never classified (a PARTIAL
# census -- the shape the canary does not see).  Both modes; rc and the last stderr line recorded.  /tmp only.
import io, os, subprocess, sys, tempfile
CT = "/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/c5_frozen/census_tokens.py"
OUT = "/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/opus_c5/p6_crash.out"
B = tempfile.mkdtemp(prefix="gxc5_p6_")
EW = "ends" + "with"
io.open(os.path.join(B, "after.py"), "w", encoding="utf-8").write("import pty\nx = 1\n")   # promptless -> must be listed
CASES = {
    "nul":        b"import pty\nx = '\x00'\n",
    "nul_code":   b"import pty\nx = 1\x00\n",
    "ctrl_z":     b"import pty\nx = 1\x1a\n",
    "formfeed":   b"\x0cimport pty\nx = 1\n",
    "bom_mid":    "import pty\nx = 1\n﻿y = 2\n".encode("utf-8"),
    "unterm3q":   b'import pty\nx = """never closed\n',
    "deepnest":   b"import pty\nx = " + b"(" * 300 + b"1" + b")" * 300 + b"\n",
    "lone_bs":    b"import pty\nx = 1 \\",
    "longline":   b"import pty\nx = '" + b"a" * 2000000 + b"'\n",
    "nonbmp_id":  "import pty\n\U0001d4b3 = 1\n".encode("utf-8"),
    "bad_escape": b"import pty\nx = buf.rstrip()." + EW.encode() + b"('\\N{NO SUCH NAME}')\n",
    "big_int_str":b"import pty\nx = mybuf.rstrip()." + EW.encode() + b"('" + b"9" * 5000 + b"')\n",
    "latin1":     "import pty\nx = 'caf\xe9'\n".encode("latin-1"),
    "cr_only":    b"#!/usr/bin/env python3\rimport pty\rx = 1\r",
    "indent_err": b"import pty\nif 1:\n        x = 1\n    y = 2\n",
    "dedent_eof": b"import pty\nif 1:\n    x = (\n",
    "emptyfile":  b"",
    "only_bom":   b"\xef\xbb\xbf",
    "tab_mix":    b"import pty\nif 1:\n\tx = 1\n        y = 2\n",
}
lines = []
for name, data in CASES.items():
    io.open(os.path.join(B, name + ".py"), "wb").write(data)
    for mode in ("promptless", "whole"):
        r = subprocess.run([sys.executable, CT, mode, B], input="%s.py\nafter.py\n" % name, capture_output=True, text=True)
        out = r.stdout.split()
        err = (r.stderr.strip().split("\n") or [""])[-1][:90]
        # promptless: after.py must be listed (it is promptless); whole: nothing is expected for either
        cont = ("after.py" in out) if mode == "promptless" else (r.returncode == 0)
        lines.append("%-12s %-10s rc=%d  listed=%-28s run-continued=%-5s %s" %
                     (name, mode, r.returncode, ",".join(out)[:28], cont, ("STDERR: " + err) if r.returncode else ""))
crashes = [l for l in lines if " rc=0 " not in l]
lines.append("")
lines.append("CASES: %d contents x 2 modes = %d runs;  runs that did NOT exit 0: %d" % (len(CASES), 2 * len(CASES), len(crashes)))
lines.append("P6_DONE")
io.open(OUT, "w", encoding="utf-8").write("\n".join(lines) + "\n")
print("\n".join(lines))
import shutil; shutil.rmtree(B, ignore_errors=True)
