#!/usr/bin/env python3
# SECTION 4 (Q2) -- >=20 NEW edits aimed at the F3 changes (NEWLINE kept; a "." must precede the method), outside the
# filed shapes (nine spellings, three population omissions, e9, the semantic transforms).  Each appended to a fresh
# /tmp snapshot's luna (prompt-detecting), gate run.  Classify: SPELLING (expected pass), CLAIMED (a shape the census
# should count -> a PASS is a DEFECT), CONTROL (expected red -> census bites).  /tmp only.
import io, os, re, shutil, subprocess, sys, tempfile
SEC = "/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC"
FROZ = "/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/c3_frozen"
OUT = "/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/opus_c3/s4b"
TARGET = "luna_absentcpu_probe.py"
shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
W = tempfile.mkdtemp(prefix="gxc3_s4b_")
SNAP = os.path.join(W, "snap")
os.makedirs(os.path.join(SNAP, "GXEMUL-SEC/regress")); os.makedirs(os.path.join(SNAP, "GXEMUL-SEC/tools"))
for f in os.listdir(os.path.join(SEC, "regress")):
    p = os.path.join(SEC, "regress", f)
    if os.path.isfile(p): shutil.copy2(p, os.path.join(SNAP, "GXEMUL-SEC/regress", f))
shutil.copy2(os.path.join(SEC, "tools/derive_hygiene_pins.sh"), os.path.join(SNAP, "GXEMUL-SEC/tools"))
for f in ("gate_hygiene.sh", "census_tokens.py"):
    shutil.copy2(os.path.join(FROZ, f), os.path.join(SNAP, "GXEMUL-SEC/regress", f))
shutil.copy2(os.path.join(FROZ, "derive_hygiene_pins.sh"), os.path.join(SNAP, "GXEMUL-SEC/tools"))
EW = "ends" + "with"; BS = chr(92)

# each case appends a block of TEXT (statements) to luna.  aimed at F3:
#   dot-placement, statement-splitting, and forms that recreate a COUNTED shape across lines/dots.
CASES = [
 # -- SPELLING: dot present but spaced / non-buf receiver / non-endswith method (avoid the whole shape and literal endswith( ) --
 ("dot_spaced",   "SPELLING", "_a = resp . %s (\"GXemul>\")" % EW),                 # spaces around the dot and paren
 ("nl_bracket",   "SPELLING", "_b = (resp.rstrip()\n       .%s (\"GXemul>\"))" % EW), # split inside () on a non-buf receiver, spaced paren
 ("bscont_np",    "SPELLING", "_c = resp.rstrip() " + BS + "\n     .%s (\"GXemul>\")" % EW), # backslash cont, non-buf, spaced
 ("lambda_np",    "SPELLING", "_d = lambda resp: resp.%s (\"GXemul>\")" % EW),
 ("comp_np",      "SPELLING", "_e = [r for r in xs if r.%s (\"GXemul>\")]" % EW),
 ("cond_np",      "SPELLING", "_f = 1 if resp.%s (\"GXemul>\") else 0" % EW),
 ("walrus_dot",   "SPELLING", "_g = (w := resp).%s (\"GXemul>\")" % EW),
 ("subscript_rcv","SPELLING", "_h = bufs[-1].rstrip().%s(\"GXemul>\")" % EW),         # receiver is bufs[-1], not a bare NAME
 ("attr_rcv",     "SPELLING", "_i = self.tail.rstrip().%s(\"GXemul>\")" % EW),        # receiver self.tail (not ...buf)
 ("removeprefix", "SPELLING", "_j = resp[::-1].removeprefix(\">lumeXG\")"),
 ("rsplit_last",  "SPELLING", "_k = resp.rsplit(\"\\n\", 1)[-1] == \"GXemul>\""),
 ("endswith_kw",  "SPELLING", "_l = resp.%s (\"GXemul>\", 0)" % EW),                  # spaced -> textual blind; extra arg
 ("not_sem",      "SPELLING", "_m = not resp.%s (\"GXemul>\")" % EW),                 # semantic + spaced
 ("cmp_true",     "SPELLING", "_n = (resp.%s (\"GXemul>\")) == True" % EW),
 ("re_anchor",    "SPELLING", "_o = re.compile(\"GXemul>$\").search(resp) is not None"),
 ("in_last",      "SPELLING", "_p = \"GXemul>\" in resp.splitlines()[-1]"),
 ("bufname_nospc","SPELLING", "_q = tailbuf.removesuffix(\"GXemul>\") != tailbuf"),   # receiver ends buf but method is removesuffix (not the shape)
 ("semicolon",    "SPELLING", "_r = 0; _r = resp.%s (\"GXemul>\")" % EW),            # after ';' on one line, spaced
 # -- CLAIMED: a real WHOLE site (receiver ends buf + rstrip().endswith("GXemul>")) split across lines/dots -> the census MUST still count it (expect RED) --
 ("whole_nl_arg", "CLAIMED",  "_s = mybuf.rstrip().%s(\n    \"GXemul>\")" % EW),        # arg split inside () -> counted -> red
 ("whole_nl_chain","CLAIMED", "_t = (mybuf.rstrip()\n    .%s(\"GXemul>\"))" % EW),      # chain split inside () -> counted -> red
 ("whole_bscont", "CLAIMED",  "_u = mybuf.rstrip() " + BS + "\n    .%s(\"GXemul>\")" % EW), # backslash cont -> counted -> red
 ("whole_dotspc", "CLAIMED",  "_v = mybuf.rstrip() . %s (\"GXemul>\")" % EW),           # spaced dots -> counted -> red
 # -- CONTROL: forms that should red via the closed-world UNKNOWN count --
 ("unbound_arg",  "CONTROL",  "_w = str.%s(resp, \"GXemul>\")" % EW),                  # endswith(resp,... -> unknown++
 ("starargs",     "CONTROL",  "_x = resp.%s(*[\"GXemul>\"])" % EW),                    # endswith(*[ -> unknown++
]

def run_gate(rdir):
    logs = os.path.join(os.path.dirname(rdir), "logs"); os.makedirs(logs, exist_ok=True)
    env = dict(os.environ, LOGDIR=logs)
    r = subprocess.run(["bash", "./gate_hygiene.sh"], cwd=rdir, env=env, capture_output=True, text=True)
    rows = [re.sub(r"\x1b\[[0-9;]*m", "", l) for l in r.stdout.split("\n") if ("readiness" in l or "whole-buffer" in l)]
    return len([l for l in rows if l.strip().startswith("FAIL")])

lines = ["%-15s %-9s %-7s %s" % ("tag", "class", "result", "appended (first line)")]
npass = defect = ctlred = claimed_caught = 0
for tag, cls, block in CASES:
    cdir = os.path.join(W, tag); shutil.rmtree(cdir, ignore_errors=True); shutil.copytree(SNAP, cdir)
    rd = os.path.join(cdir, "GXEMUL-SEC/regress"); p = os.path.join(rd, TARGET)
    s = io.open(p, encoding="utf-8").read()
    io.open(p, "w", encoding="utf-8").write(s + "\n\ndef _q2_%s(resp=None, mybuf=None, bufs=None, xs=(), tailbuf=None):\n    " % tag
                                           + block.replace("\n", "\n    ") + "\n    return None\n")
    nf = run_gate(rd)
    res = "PASS" if nf == 0 else "red%d" % nf
    flag = ""
    if nf == 0:
        npass += 1
        if cls == "CLAIMED": flag = "  <-- DEFECT (claimed-counted shape passed)"; defect += 1
        if cls == "CONTROL": flag = "  <-- control did NOT red"
    else:
        if cls == "CONTROL": ctlred += 1
        if cls == "CLAIMED": claimed_caught += 1
    lines.append("%-15s %-9s %-7s %s%s" % (tag, cls, res, block.split(chr(10))[0][:52], flag))
    shutil.rmtree(cdir, ignore_errors=True)
lines += ["", "PASSES: %d   CLAIMED shapes correctly CAUGHT: %d   CONTROLS red: %d   DEFECTS (claimed passed): %d   total: %d"
          % (npass, claimed_caught, ctlred, defect, len(CASES))]
io.open(os.path.join(OUT, "TABLE.txt"), "w", encoding="utf-8").write("\n".join(lines) + "\nS4B_DONE\n")
print("\n".join(lines)); print("S4B_DONE")
shutil.rmtree(W, ignore_errors=True)
