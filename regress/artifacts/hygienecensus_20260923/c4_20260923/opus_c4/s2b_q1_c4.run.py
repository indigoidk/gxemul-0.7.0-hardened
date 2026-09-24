#!/usr/bin/env python3
# SECTION 2 (Q1 a/b) -- does the F3 census_tokens.py LOSE any legitimate one-statement readiness call?
# NEWLINE is kept (a match can no longer span two statements); a "." must precede the method name.
# For each crafted file: run the FROZEN F3 census_tokens.py (029fba36) promptless+whole, and my expectation.
# A LOST legitimate call is only safe if it fails CLOSED -- the probe becomes promptless -> the gate names row reds.
import io, os, subprocess, sys, tempfile
CT = "/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/c4_frozen/census_tokens.py"
BASE = tempfile.mkdtemp(prefix="gxq1_")
EW = "ends" + "with"; BS = chr(92)
def W(name, text):
    io.open(os.path.join(BASE, name), "w", encoding="utf-8", newline="").write(text); return name
def run(mode, names):
    r = subprocess.run([sys.executable, CT, mode, BASE], input="\n".join(names)+"\n", capture_output=True, text=True)
    return r.stdout.strip(), r.returncode

CALL = "buf.rstrip().%s(\"GXemul>\")" % EW
WCALL = "mybuf.rstrip().%s(\"GXemul>\")" % EW   # receiver ends 'buf' -> a WHOLE site when single-statement
cases = []
def C(name, text, claim, exp_pl, exp_wh):
    W(name, text); cases.append((name, claim, exp_pl, exp_wh))

# ---- Q1(a): NEWLINE kept -- legitimate ONE-statement calls that MIGHT be lost ----
# 1 split across lines INSIDE brackets (newline is NL, still skipped) -- must still count
C("br_split.py",   "def f(mybuf):\n    return (mybuf.rstrip()\n            .%s(\"GXemul>\"))\n" % EW, "chain split inside ()", False, 1)
# 2 split INSIDE the endswith parens
C("arg_split.py",  "def f(mybuf):\n    return mybuf.rstrip().%s(\n        \"GXemul>\")\n" % EW, "arg split inside endswith()", False, 1)
# 3 backslash continuation (chr(92)) -- one logical line
C("bscont.py",     "def f(mybuf):\n    return mybuf.rstrip() " + BS + "\n        .%s(\"GXemul>\")\n" % EW, "backslash continuation", False, 1)
# 4 inside a lambda (one statement)
C("lambda.py",     "f = lambda mybuf: mybuf.rstrip().%s(\"GXemul>\")\n" % EW, "lambda body", False, 1)
# 5 inside a comprehension (one statement); receiver ends buf -> whole
C("comp.py",       "xs = [mybuf for mybuf in data if mybuf.rstrip().%s(\"GXemul>\")]\n" % EW, "comprehension filter", False, 1)
# 6 conditional expression
C("cond.py",       "r = 1 if buf.rstrip().%s(\"GXemul>\") else 0\n" % EW, "conditional expr", False, 0)  # receiver buf ends 'buf'? 'buf'[-3:]='buf' -> whole=1!
# 7 decorator argument (one logical line ending in NEWLINE)
C("deco.py",       "import functools\n@functools.wraps(mybuf.rstrip().%s)\ndef g(): pass\n" % EW, "decorator arg (no call paren)", True, 0)
# 8 call right after a ';' on one physical line
C("semi.py",       "x = 1; ready = mybuf.rstrip().%s(\"GXemul>\")\n" % EW, "call after ';'", False, 1)
# 9 THE t_nljoin false-positive that F3 must now LOSE: reference on one stmt, paren on next
C("nljoin.py",     "ready = mybuf.rstrip().%s\n(\"GXemul>\")\n" % EW, "reference then paren (2 stmts) -- MUST be lost", True, 0)
# 10 chained on the SAME statement but with an intervening real call on next line (two statements, both real)
C("twostmt.py",    "a = mybuf.rstrip().%s(\"GXemul>\")\nb = other.strip()\n" % EW, "two statements, first is the call", False, 1)

# ---- Q1(b): "." required before the method name ----
# 11 unbound str.endswith(buf, ...) -- HAS a dot -> still counted (not lost)
C("unbound.py",    "ok = str.%s(mybuf.rstrip(), \"GXemul>\")\n" % EW, "unbound str.endswith(buf,...)", False, 0)  # '.' before endswith present -> promptless False; not the whole SHAPE
# 12 getattr indirection -- endswith is a STRING, no NAME -> not a call (promptless) -- fail-closed
C("getattr.py",    "ok = getattr(mybuf.rstrip(), \"%s\")(\"GXemul>\")\n" % EW, "getattr indirection", True, 0)
# 13 a NAME 'endswith' with NO preceding dot: a bare function call (from-import style)
C("nodot.py",      "from x import %s\nok = %s(mybuf, \"GXemul>\")\n" % (EW, EW), "bare endswith( ) no dot", True, 0)
# 14 method reference passed as a callback, dot present, but NO immediate '(' -> not a call
C("ref_only.py",   "cb = mybuf.rstrip().%s\nok = cb(\"GXemul>\")\n" % EW, "method reference stored, called later", True, 0)
# 15 double-dot chained attribute then call (obj.attr.endswith()) -- dot present -> counted
C("attrchain.py",  "ok = self.io.%s(\"GXemul>\")\n" % EW, "obj.attr.endswith() (not whole shape)", False, 0)

out, _ = run("promptless", [c[0] for c in cases]); pls = set(out.split("\n")) - {""}
wout, _ = run("whole", [c[0] for c in cases]); wm = {}
for l in wout.split("\n"):
    if ":" in l:
        k, v = l.rsplit(":", 1); wm[k] = int(v)
print("%-14s %-38s %-16s %-16s %s" % ("file", "claim", "expect", "got", "OK?"))
bad = 0
for name, claim, epl, ewh in cases:
    gpl, gwh = name in pls, wm.get(name, 0)
    ok = (gpl == epl) and (gwh == ewh); bad += 0 if ok else 1
    print("%-14s %-38s pl=%-5s wh=%-6s pl=%-5s wh=%-6s %s" % (name, claim, epl, ewh, gpl, gwh, "ok" if ok else "**MISMATCH**"))
print("MISMATCHES vs expectation: %d of %d" % (bad, len(cases)))
print("S2B_Q1_DONE")
