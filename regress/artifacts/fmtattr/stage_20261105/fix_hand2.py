#!/usr/bin/env python3
"""fix_hand2.py -- make the attributed build WARNING-FREE, as gate 1 requires once the attributes are permanent (gate_build.sh
checks `warnings == 0`).  Run after apply_fmt.py and fix_hand.py, on the staged files (HEAD's where a file is not staged).
  1. the 19 -Wformat-zero-length calls: `..., VERBOSITY_X, "");` -> `..., VERBOSITY_X, "%s", "");` (prints the same empty
     line).  Lines are taken from the last verification build's log (v_make.log, staged numbering), each asserted to end that way.
  2. the 4 -Wformat-overflow warnings (3 calls): an unreachable `default:` in each inner mnemonic switch, so GCC sees `mnem`
     assigned on every path.  The enclosing switches admit exactly the listed values (GPT-6 Astra's proof), so it never runs;
     `mnem == NULL` stays the sentinel cpu_alpha.c's other paths test."""
import io
import os
import re
import subprocess

REPO = "C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC"
O = "C:/DocumentNoSnc/cc/GXEMUL/_scratchpad/codescan/fmtfix/"
ST = O + "stage/"
tracked = subprocess.run(["git", "-C", REPO, "ls-files", "src"], capture_output=True, text=True).stdout.split()


def path_of(base):
    m = [t for t in tracked if os.path.basename(t) == base]
    assert len(m) == 1, (base, m)
    return m[0]


def cur(f):
    p = ST + f
    if os.path.exists(p):
        return io.open(p, encoding="latin-1", newline="").read()
    return subprocess.run(["git", "-C", REPO, "show", "HEAD:" + f], capture_output=True).stdout.decode("latin-1")


def put(f, t):
    os.makedirs(os.path.dirname(ST + f), exist_ok=True)
    io.open(ST + f, "w", encoding="latin-1", newline="").write(t)


zl = {}
for l in io.open(O + "v_make.log", encoding="utf-8", errors="replace"):
    m = re.match(r"^(\S+?\.c):(\d+):\d+: warning: .*\[-Wformat-zero-length\]", l.strip())
    if m:
        zl.setdefault(path_of(os.path.basename(m.group(1))), set()).add(int(m.group(2)))
n = 0
for f, lines in sorted(zl.items()):
    L = cur(f).split("\n")
    for ln in sorted(lines):
        s = L[ln - 1]
        assert s.rstrip().endswith(', "");'), (f, ln, s)
        L[ln - 1] = s[:s.rindex(', "");')] + ', "%s", "");' + s[s.rindex(', "");') + len(', "");'):]
        n += 1
    put(f, "\n".join(L))
print("zero-length: %d calls in %d files" % (n, len(zl)))

TAG = "\t\t%s/*  #NNN: unreachable (the enclosing switch admits only the\n\t\t%s    cases above); keeps GCC's -Wformat-overflow quiet.  */\n"
SITES = [("src/cpus/cpu_alpha.c", '\t\tcase 0x2f: mnem = "stq_c"; break;\n\t\t}\n', ""),
         ("src/cpus/cpu_alpha.c", '\t\tcase 0x3f: mnem = "bgt"; break;\n\t\t}\n', ""),
         ("src/cpus/cpu_m88k.c", '\t\t\tcase 0x2a: mnem = "rot"; break;\n\t\t\t}\n', "\t")]
for f, anchor, ind in SITES:
    t = cur(f)
    assert t.count(anchor) == 1, (f, anchor, t.count(anchor))
    last, close = anchor.split("\n")[0], ind + "\t\t}"
    new = last + "\n" + TAG % (ind, ind) + ind + "\t\tdefault:   mnem = \"?\"; break;\n" + close + "\n"
    put(f, t.replace(anchor, new))
print("overflow accommodations: %d switches" % len(SITES))
