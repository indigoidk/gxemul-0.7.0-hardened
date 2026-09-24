#!/usr/bin/env python3
# Q2 (census side) + measured checks of K7, K11, K13, K14, K15, K18 -- on fresh /tmp copies (SEC regress top-level +
# tools + the three F4 frozen files), UNMODIFIED F4 gate and deriver.  Each case: an edit, the gate's readiness FAIL rows,
# and (where the case needs it) deriver steps.  /tmp only; never writes under GXEMUL-SEC.
import io, os, re, shutil, subprocess, sys, tempfile
SEC = "/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC"
FROZ = "/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/c5_frozen"
OUT = "/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/opus_c5/q2"
shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
W = tempfile.mkdtemp(prefix="gxc5_q2_")
SNAP = os.path.join(W, "snap")
os.makedirs(os.path.join(SNAP, "GXEMUL-SEC/regress")); os.makedirs(os.path.join(SNAP, "GXEMUL-SEC/tools"))
for f in os.listdir(os.path.join(SEC, "regress")):
    p = os.path.join(SEC, "regress", f)
    if os.path.isfile(p): shutil.copy2(p, os.path.join(SNAP, "GXEMUL-SEC/regress", f))
for f in ("gate_hygiene.sh", "census_tokens.py"):
    shutil.copy2(os.path.join(FROZ, f), os.path.join(SNAP, "GXEMUL-SEC/regress", f))
shutil.copy2(os.path.join(FROZ, "derive_hygiene_pins.sh"), os.path.join(SNAP, "GXEMUL-SEC/tools"))
EW = "ends" + "with"; BS = chr(92)
AE = "arm_endian_probe.py"
AE_OLD = '            if len(buf) > mark and buf[mark:].rstrip().%s("GXemul>"):\n' % EW
AE_BARE = '            if len(buf) > mark and buf[mark:].rstrip().%s(">"):\n' % EW      # the #37 bare defect

def fresh(tag):
    d = os.path.join(W, tag); shutil.rmtree(d, ignore_errors=True); shutil.copytree(SNAP, d)
    return d, os.path.join(d, "GXEMUL-SEC/regress")
def rd(r, f): return io.open(os.path.join(r, f), encoding="utf-8", newline="").read()
def wr(r, f, s):
    os.makedirs(os.path.dirname(os.path.join(r, f)), exist_ok=True)
    io.open(os.path.join(r, f), "w", encoding="utf-8", newline="").write(s)
def sub(r, f, old, new):
    s = rd(r, f); assert s.count(old) == 1, (f, s.count(old)); wr(r, f, s.replace(old, new))
def gate(d):
    r = subprocess.run(["bash", "./gate_hygiene.sh"], cwd=os.path.join(d, "GXEMUL-SEC/regress"),
                       env=dict(os.environ, LOGDIR=os.path.join(d, "logs")), capture_output=True, text=True)
    rows = [re.sub(r"\x1b\[[0-9;]*m", "", l).strip() for l in r.stdout.split("\n")]
    rr = [l for l in rows if (l.startswith("FAIL") or l.startswith("ok")) and ("readiness" in l or "whole-buffer" in l)]
    fails = [l for l in rr if l.startswith("FAIL")]
    if len(rr) != 12:   # DENOMINATOR: gate 6 prints 12 readiness rows; fewer means it stopped early
        tail = r.stderr.strip().split("\n")[-1] if r.stderr.strip() else ""
        fails = fails + ["GATE DID NOT COMPLETE: %d of 12 readiness rows printed; stderr tail: %s" % (len(rr), tail[:90])]
    return fails
def drv(d, *args):
    r = subprocess.run(["bash", os.path.join(d, "GXEMUL-SEC/tools/derive_hygiene_pins.sh")] + list(args),
                       env=dict(os.environ, GXROOT=d), capture_output=True, text=True)
    first = [l for l in r.stdout.split("\n") if re.match(r"^(REFUSED|WRITTEN|RELEASED|GRANDFATHERED|DERIVE_FAIL)", l)]
    return "rc=%d %s" % (r.returncode, (first[0][:100] if first else ""))
def compiles(path):
    r = subprocess.run([sys.executable, "-c", "import sys; compile(open(sys.argv[1],'rb').read(), sys.argv[1], 'exec')", path],
                       capture_output=True, text=True)
    return "compiles" if r.returncode == 0 else ("does NOT compile: " + r.stderr.strip().split("\n")[-1][:70])
LOG = []
def rep(tag, what, fails, extra=""):
    LOG.append("== %s  -- %s" % (tag, what))
    LOG.append("   gate: %s" % ("ALL readiness rows GREEN" if not fails else "%d FAIL" % len(fails)))
    for f in fails: LOG.append("      " + f[:118])
    if extra: LOG.append("   " + extra)

# ---- Q2-cr: the #37 bare defect in arm_endian, file saved with CR-ONLY line endings --------------------------------
d, r = fresh("cr_ctl"); sub(r, AE, AE_OLD, AE_BARE)
rep("cr_ctl", "CONTROL: arm_endian's predicate -> the #37 bare form, normal LF file", gate(d))
d, r = fresh("cr_only"); sub(r, AE, AE_OLD, AE_BARE)
s = rd(r, AE).replace("\n", "\r"); io.open(os.path.join(r, AE), "w", encoding="utf-8", newline="").write(s)
rep("cr_only", "the same bare predicate, file rewritten with CR-only line endings (first line is the #! shebang)", gate(d),
    "python: " + compiles(os.path.join(r, AE)) + "   (grep sees %d line(s) in the file)" % (s.count("\n") + 1))

# ---- Q2-hash: code on a '#'-leading physical line, after a triple-quoted (non-f) string closes -----------------------
d, r = fresh("hash_ctl"); s = rd(r, "luna_absentcpu_probe.py")
wr(r, "luna_absentcpu_probe.py", s + '\n_t = ""\n_c = lambda buf: buf.%s(">")\n' % EW)
rep("hash_ctl", "CONTROL: a bare-prompt lambda appended to luna on an ordinary line", gate(d))
d, r = fresh("hash_line"); s = rd(r, "luna_absentcpu_probe.py")
wr(r, "luna_absentcpu_probe.py", s + '\n_t = """\n#"""; _c = lambda buf: buf.%s(">")\n' % EW)
rep("hash_line", "the same lambda on the physical line that closes a triple-quoted string, which begins with '#'", gate(d),
    "python: " + compiles(os.path.join(r, "luna_absentcpu_probe.py")))

# ---- K11: a backslash continuation BETWEEN the method name and its paren (the line-based class) ----------------------
d, r = fresh("k11"); s = rd(r, "luna_absentcpu_probe.py")
wr(r, "luna_absentcpu_probe.py", s + "\n_c = lambda buf: buf.%s " % EW + BS + '\n    (">")\n')
rep("k11", "K11: bare call with a backslash continuation between the name and '(' (filed line-based class)", gate(d),
    "python: " + compiles(os.path.join(r, "luna_absentcpu_probe.py")))

# ---- K15: a probe renamed to readiness_predicate_test.py in a SUBDIRECTORY, carrying the #37 bare predicate ----------
d, r = fresh("k15"); sub(r, AE, AE_OLD, AE_BARE)
os.makedirs(os.path.join(r, "newsub")); os.rename(os.path.join(r, AE), os.path.join(r, "newsub/readiness_predicate_test.py"))
rep("k15", "K15: arm_endian (bare predicate) moved to newsub/readiness_predicate_test.py", gate(d))

# ---- K13: a call through an alias as a probe's ONLY readiness test (expect: listed promptless, fail-closed) -----------
d, r = fresh("k13")
sub(r, AE, AE_OLD, '            if len(buf) > mark and (lambda %s: %s("GXemul>"))(buf[mark:].rstrip().%s):\n' % (EW, EW, EW))
rep("k13", "K13: arm_endian's only test becomes an alias call (no '.' before the name at the call)", gate(d))

# ---- K7: a probe's ONLY test moved into a helper module that forks no pty (expect: promptless, names row red) ------
d, r = fresh("k7")
wr(r, "zz_ready_helper.py", '"""helper"""\n\n\ndef at_prompt(s):\n    return s.rstrip().%s("GXemul>")\n' % EW)
sub(r, AE, "import os\n", "import os\nimport zz_ready_helper\n")
sub(r, AE, AE_OLD, "            if len(buf) > mark and zz_ready_helper.at_prompt(buf[mark:]):\n")
rep("k7", "K7: arm_endian's only test moved into zz_ready_helper.py (forks no pty)", gate(d))

# ---- K14: a GRANDFATHERED promptless probe gains a match CLASS PATTERN of the call's shape; then --release ---------
d, r = fresh("k14"); s = rd(r, "gdrom_cond_probe.py")
wr(r, "gdrom_cond_probe.py", s + '\n\ndef _k14(x):\n    match x:\n        case K.%s("GXemul>"):\n            pass\n' % EW)
f1 = gate(d); rel = drv(d, "--release", "gdrom_cond_probe.py"); f2 = gate(d)
rep("k14", "K14: gdrom_cond (grandfathered, promptless) gains `case K.<method>(\"GXemul>\"):`", f1,
    "then --release gdrom_cond_probe.py -> %s ; gate after: %s   python: %s"
    % (rel, "ALL GREEN" if not f2 else "%d FAIL %s" % (len(f2), f2), compiles(os.path.join(r, "gdrom_cond_probe.py"))))

# ---- K18: a COMMENT above the list quoting the assignment; --grandfather a real new promptless probe --------------
d, r = fresh("k18"); g = rd(r, "gate_hygiene.sh")
g = g.replace('GRANDFATHERED_PROMPTLESS="pcc2_width_witness.py',
              '#  (the list reads GRANDFATHERED_PROMPTLESS="name name ...", one name per probe)\nGRANDFATHERED_PROMPTLESS="pcc2_width_witness.py', 1)
wr(r, "gate_hygiene.sh", g)
shutil.copy2(os.path.join(r, "pcc2_width_probe.py"), os.path.join(r, "zz-legit_probe.py"))
res = drv(d, "--grandfather", "zz-legit_probe.py"); g2 = rd(r, "gate_hygiene.sh")
gl = g2.split("\n"); ci = [k for k, l in enumerate(gl) if l.startswith("#  (the list reads")][0]
around = "\n".join("      L%d: %r" % (k + 1, gl[k][:100]) for k in range(ci, ci + 3))
lst = g2[g2.index('\nGRANDFATHERED_PROMPTLESS="'):]; lst = lst[:lst.index('"', 30)]
bn = subprocess.run(["bash", "-n", "gate_hygiene.sh"], cwd=r, capture_output=True, text=True)
rep("k18", "K18 (latent): a comment above the list quotes `GRANDFATHERED_PROMPTLESS=\"`; --grandfather zz-legit_probe.py",
    gate(d), "deriver: %s\n   the three lines from the comment on:\n%s\n   real list names it: %s   bash -n: %s"
    % (res, around, "zz-legit_probe.py" in lst, "ok" if bn.returncode == 0 else "FAIL " + bn.stderr.strip()[:80]))

shutil.rmtree(W, ignore_errors=True)
LOG.append("Q2_CENSUS_DONE")
io.open(os.path.join(OUT, "SUMMARY.txt"), "w", encoding="utf-8").write("\n".join(LOG) + "\n")
print("\n".join(LOG))
