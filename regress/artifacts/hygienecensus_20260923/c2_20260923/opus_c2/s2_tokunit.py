#!/usr/bin/env python3
# SECTION 2 -- census_tokens.py claim-check, unit-level.  Creates crafted files under a /tmp dir, runs the FROZEN
# census_tokens.py (c2_frozen, md5 662ce35a) in both modes over each, prints what it did.  Read-only over the frozen tool.
import io, os, subprocess, sys, tempfile
CT = "/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/c2_frozen/census_tokens.py"
BASE = tempfile.mkdtemp(prefix="gxtok_")
EW = "ends" + "with"   # avoid writing the literal method+paren in THIS test file's own text

def write(name, text, binary=False):
    p = os.path.join(BASE, name)
    os.makedirs(os.path.dirname(p) or BASE, exist_ok=True)
    if binary:
        io.open(p, "wb").write(text)
    else:
        io.open(p, "w", encoding="utf-8", newline="").write(text)
    return name

def run(mode, names):
    inp = "\n".join(names) + "\n"
    r = subprocess.run([sys.executable, CT, mode, BASE], input=inp, capture_output=True, text=True)
    return r.stdout.strip(), r.returncode

# ---- build the crafted probe files -------------------------------------------------
CALL = "buf.rstrip().%s(\"GXemul>\")" % EW          # the canonical whole-buffer site (double quote)
cases = []
def C(name, text, claim, expect_pl, expect_whole, binary=False):
    write(name, text, binary); cases.append((name, claim, expect_pl, expect_whole))

# baseline: a plain code call -> NOT promptless, 1 whole site
C("base.py",        "x = %s\n" % CALL,                                  "baseline code call",            False, 1)
# comment is not code
C("comment.py",     "x = len(buf)  # %s\n" % CALL,                      "trailing comment not code",     True,  0)
C("fullcomment.py", "# %s\n x = 1\n" % CALL,                            "full-line comment not code",    True,  0)
# string is not code
C("string.py",      "x = \"%s\"\n" % CALL,                             "string literal not code",       True,  0)
# docstring is not code
C("docstring.py",   '"""doc mentions %s here."""\nx = 1\n' % CALL,      "module docstring not code",     True,  0)
# spacing between tokens ignored (whole)
C("space1.py",      "x = buf.rstrip( ).%s ( \"GXemul>\" )\n" % EW,      "spaces between tokens (whole)",  False, 1)
C("space2.py",      "x = buf .rstrip().%s(\"GXemul>\")\n" % EW,         "space before .rstrip (whole)",   False, 1)
# either quote
C("single.py",      "x = buf.rstrip().%s('GXemul>')\n" % EW,            "single-quoted arg (whole)",      False, 1)
# per-occurrence: two on one line, three across lines
C("twoline.py",     "x = %s or %s\n" % (CALL, CALL),                    "two sites on one line",         False, 2)
C("threefile.py",   "a = %s\nb = %s\nc = %s\n" % (CALL, CALL, CALL),    "three sites in a file",         False, 3)
# --- tokenizer edge cases the brief names ---
# line continuation (backslash) inside the whole-buffer form
C("cont.py",        "x = buf.rstrip() \\n     .%s(\"GXemul>\")\n" % EW, "backslash line-continuation",  False, 1)
# f-string containing the shape (3.12+ tokenizes interpolations as code)
C("fstring.py",     "x = f\"{buf.rstrip().%s('GXemul>')}\"\n" % EW,     "f-string interpolation",        None,  None)
# bytes literal argument
C("bytes.py",       "x = buf.rstrip().%s(b\"GXemul>\")\n" % EW,         "bytes literal arg",             None,  None)
# BOM + coding header
C("bom.py",         "﻿# coding: utf-8\nx = %s\n" % CALL,           "utf-8 BOM + coding header",     False, 1)
C("coding.py",      "# -*- coding: utf-8 -*-\nx = %s\n" % CALL,         "coding header only",            False, 1)
# untokenizable: unbalanced bracket at EOF
C("unbal.py",       "x = (1 + \n",                                       "unbalanced bracket (untok)",   True,  0)
C("straypar.py",    "x = 1)\n",                                          "stray close paren",            None,  None)
# CRLF file (write bytes so the CRLF survives)
C("crlf.py",        ("x = %s\r\n" % CALL).encode("utf-8"),               "CRLF line endings",            False, 1, binary=True)
# tabs vs spaces: consistent tabs
C("tabs.py",        "def f():\n\tx = %s\n\treturn x\n" % CALL,          "tab indentation (consistent)",  False, 1)
# mixed tabs/spaces -> TabError
C("mixtab.py",      "def f():\n\tif True:\n        x = %s\n" % CALL,     "mixed tab/space (TabError)",   True,  0)
# non-UTF8 bytes -> UnicodeDecodeError (unreadable), fail-closed promptless
C("latin1.py",      ("x = %s  # \xe9\r\n" % CALL).encode("latin-1"),     "non-UTF8 byte (unreadable)",   True,  0, binary=True)
# receiver not ending in buf
C("recv.py",        "x = self.buffer.rstrip().%s(\"GXemul>\")\n" % EW,  "receiver not ...buf (whole=0)", None,  0)
C("recvbuf.py",     "x = self.rxbuf.rstrip().%s(\"GXemul>\")\n" % EW,   "receiver rxbuf ends buf",       None,  1)
# absent file (never written) -> unreadable, fail-closed promptless
cases.append(("ABSENT_probe.py", "absent file (OSError)", True, 0))
# a site as the literal LAST line, no trailing blank (off-by-one guard)
C("lastline.py",    "y = 1\nx = %s" % CALL,                             "site on final line (no NL)",    False, 1)

# ---- measure ----
allnames = [c[0] for c in cases]
pl_out, pl_rc = run("promptless", allnames)
wh_out, wh_rc = run("whole", allnames)
pl_set = set(pl_out.split("\n")) - {""}
wh_map = {}
for line in wh_out.split("\n"):
    if ":" in line:
        k, v = line.rsplit(":", 1); wh_map[k] = int(v)

print("BASE=%s" % BASE)
print("promptless rc=%d  whole rc=%d" % (pl_rc, wh_rc))
print("%-16s %-32s %-10s %-10s %-6s" % ("file", "claim", "promptless", "whole", "OK?"))
bad = 0
for name, claim, epl, ewh in cases:
    gpl = name in pl_set
    gwh = wh_map.get(name, 0)
    ok = True
    if epl is not None and gpl != epl: ok = False
    if ewh is not None and gwh != ewh: ok = False
    if not ok: bad += 1
    exp = "pl=%s wh=%s" % (epl, ewh)
    got = "pl=%s wh=%s" % (gpl, gwh)
    print("%-16s %-32s %-22s %-22s %s" % (name, claim, exp, got, "ok" if ok else "**MISMATCH**"))
print("MISMATCHES vs my prediction: %d" % bad)
print("raw promptless output:\n  " + "\n  ".join(sorted(pl_set)))
print("raw whole output:\n  " + "\n  ".join("%s:%d" % (k, v) for k, v in sorted(wh_map.items())))
# usage-error exit code
r = subprocess.run([sys.executable, CT, "bogusmode", BASE], input="x\n", capture_output=True, text=True)
print("usage-error (bad mode) rc=%d (claim: 2)" % r.returncode)
r = subprocess.run([sys.executable, CT], input="", capture_output=True, text=True)
print("usage-error (no args) rc=%d (claim: 2)" % r.returncode)
print("S2_TOKUNIT_DONE")
