#!/usr/bin/env python3
# F5-targeted probes (Q1/Q2) on fresh /tmp copies (SEC regress top-level + tools + the three F5 frozen files).  WSL.
#   P1 whole_space   a prompt-detecting pty probe NAMED "zz x.py" with one whole-buffer site; --write --ruling
#   P2 whole_colon   the same, named "zz:9 x.py" -- does the per-file "name:count" parse misread it?
#   P3 whole_dollar  CONTROL: named "zz$HOME.py" -- the F5 check must refuse it
#   P4 canary_blind  census_tokens.py's call test replaced by `return True`: it runs, lists unreadable paths, and
#                    calls every readable probe prompt-detecting -- does the canary see it?  does --release accept?
#   P5 canary_file   a real file named zz_derive_canary_absent.py (pty.fork, prompt-detecting) lying in regress/
#   P7 glob_tree     a promptless pty probe NAMED "zz*.py" + a plain file zz_other.py -- the unquoted printed lists
#   P8 m14           ${RULING%%:*} on a reason holding colons (bash)
# For each: deriver rc/first line, the gate's readiness FAIL rows (12-row denominator enforced), key pins.  /tmp only.
import io, os, re, shutil, subprocess, sys, tempfile
SEC = "/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC"
FROZ = "/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/c5_frozen"
OUT = "/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/opus_c5/f5probes"
shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
W = tempfile.mkdtemp(prefix="gxc5_f5_")
SNAP = os.path.join(W, "snap")
os.makedirs(os.path.join(SNAP, "GXEMUL-SEC/regress")); os.makedirs(os.path.join(SNAP, "GXEMUL-SEC/tools"))
for f in os.listdir(os.path.join(SEC, "regress")):
    p = os.path.join(SEC, "regress", f)
    if os.path.isfile(p): shutil.copy2(p, os.path.join(SNAP, "GXEMUL-SEC/regress", f))
for f in ("gate_hygiene.sh", "census_tokens.py"):
    shutil.copy2(os.path.join(FROZ, f), os.path.join(SNAP, "GXEMUL-SEC/regress", f))
shutil.copy2(os.path.join(FROZ, "derive_hygiene_pins.sh"), os.path.join(SNAP, "GXEMUL-SEC/tools"))
EW = "ends" + "with"
RULE = "2026-09-23: owner ruled to allowlist this site pending its conversion"
LOG = []

def fresh(tag):
    d = os.path.join(W, tag); shutil.rmtree(d, ignore_errors=True); shutil.copytree(SNAP, d)
    return d, os.path.join(d, "GXEMUL-SEC/regress")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)
def gate(d):
    r = subprocess.run(["bash", "./gate_hygiene.sh"], cwd=os.path.join(d, "GXEMUL-SEC/regress"),
                       env=dict(os.environ, LOGDIR=os.path.join(d, "logs")), capture_output=True, text=True)
    rows = [re.sub(r"\x1b\[[0-9;]*m", "", l).strip() for l in r.stdout.split("\n")]
    rr = [l for l in rows if (l.startswith("FAIL") or l.startswith("ok")) and ("readiness" in l or "whole-buffer" in l)]
    fails = [l for l in rr if l.startswith("FAIL")]
    if len(rr) != 12:
        fails.append("GATE DID NOT COMPLETE: %d of 12 readiness rows" % len(rr))
    newp = [l for l in r.stdout.split("\n") if l.startswith("    ") and l.strip().endswith(".py")]
    return fails, newp
def drv(d, *args, cwd=None):
    r = subprocess.run(["bash", os.path.join(d, "GXEMUL-SEC/tools/derive_hygiene_pins.sh")] + list(args),
                       env=dict(os.environ, GXROOT=d), capture_output=True, text=True, cwd=cwd)
    first = [l for l in r.stdout.split("\n") if re.match(r"^(REFUSED|WRITTEN|RELEASED|GRANDFATHERED:|DERIVE_FAIL)", l)]
    return r.returncode, (first[0] if first else ""), r.stdout
def pins(r):
    g = rd(os.path.join(r, "gate_hygiene.sh"))
    return {k: (re.search(r"(?m)^%s=(.*)$" % k, g) or [None, "?"])[1] for k in ("EXPECT_WHOLE_FULL", "WHOLE_FULL_FILES", "EXPECT_PTY_PROBES")}
def block(tag, what, lines):
    LOG.append("== %s -- %s" % (tag, what)); LOG.extend("   " + l for l in lines); LOG.append("")
def fl(f): return ["gate: ALL 12 readiness rows GREEN"] if not f else ["gate: %d FAIL" % len(f)] + ["   " + x[:120] for x in f]

WHOLE = '\n_c = lambda mybuf: mybuf.rstrip().%s("GXemul>")\n' % EW
# ---------------- P1 / P2 / P3: whole-buffer FILE NAMES ----------------
for tag, name, what in (("whole_space", "zz x.py", "a SPACE in a whole-buffer file name"),
                        ("whole_colon", "zz:9 x.py", "a COLON+digit and a SPACE in a whole-buffer file name"),
                        ("whole_dollar", "zz$HOME.py", "CONTROL: a $ in a whole-buffer file name")):
    d, r = fresh(tag)
    src = rd(os.path.join(r, "arm_endian_probe.py")) + WHOLE       # prompt-detecting pty probe + one whole site
    wr(os.path.join(r, name), src)
    f0, _ = gate(d)
    rc, first, out = drv(d, "--write", "--ruling", RULE)
    f1, _ = gate(d)
    p = pins(r)
    block(tag, what, ["before --write: " + ("%d FAIL" % len(f0)),
                      "--write --ruling -> rc=%d %s" % (rc, first[:110]),
                      "pins after: EXPECT_WHOLE_FULL=%s  WHOLE_FULL_FILES=%s  EXPECT_PTY_PROBES=%s"
                      % (p["EXPECT_WHOLE_FULL"], p["WHOLE_FULL_FILES"], p["EXPECT_PTY_PROBES"]),
                      "true whole-buffer sites now: 4 (arm_bdt 1, arm_flags 2, the new file 1)"] + fl(f1))

# ---------------- P4: a classifier that RUNS and MISCLASSIFIES ----------------
d, r = fresh("canary_blind")
ct = os.path.join(r, "census_tokens.py"); s = rd(ct)
old = "def has_ends_with_call(toks):\n"
assert s.count(old) == 1
wr(ct, s.replace(old, old + "    return True   # simulated misclassification: every readable file 'has a call'\n", 1))
f0, _ = gate(d)
rc1, first1, out1 = drv(d)
gone = len([l for l in out1.split("\n") if l.startswith("  ") and l.strip().endswith(".py")
            and "GRANDFATHERED BUT" in out1])
rc2, first2, _ = drv(d, "--release", "gdrom_cond_probe.py")
block("canary_blind", "classifier runs, lists unreadable paths, calls every readable file prompt-detecting",
      fl(f0) + ["report: rc=%d %s" % (rc1, first1[:100] or "(no DERIVE_FAIL -- the canary passed)"),
                "report line: " + ([l for l in out1.split("\n") if l.startswith("promptless vs")] or ["?"])[0],
                "--release gdrom_cond_probe.py (still promptless) -> rc=%d %s" % (rc2, first2[:100])])

# ---------------- P5: a REAL file carrying the canary's name ----------------
d, r = fresh("canary_file")
wr(os.path.join(r, "zz_derive_canary_absent.py"), rd(os.path.join(r, "arm_endian_probe.py")))   # prompt-detecting pty probe
rc, first, _ = drv(d)
f0, _ = gate(d)
block("canary_file", "a prompt-detecting pty probe named zz_derive_canary_absent.py lies in regress/",
      ["report: rc=%d %s" % (rc, first[:140])] + fl(f0))

# ---------------- P7: a glob character in a TREE file name ----------------
d, r = fresh("glob_tree")
wr(os.path.join(r, "zz*.py"), rd(os.path.join(r, "pcc2_width_probe.py")))       # a promptless pty probe
wr(os.path.join(r, "zz_other.py"), "# a plain file, not a probe\n")
rc, first, out = drv(d, cwd=r)
newlist = []; on = False
for l in out.split("\n"):
    if l.startswith("NEW PROMPTLESS"): on = True; continue
    if on and l.startswith("  "): newlist.append(l.strip())
    elif on: on = False
f0, gnew = gate(d)
block("glob_tree", "a promptless pty probe NAMED zz*.py, plus a plain file zz_other.py (deriver and gate run in regress/)",
      ["deriver report's NEW PROMPTLESS list: %s   (the tree holds ONE new promptless probe)" % newlist] + fl(f0)
      + ["gate's printed NEW PROMPTLESS list: %s" % [x.strip() for x in gnew]])

# ---------------- P8: M14 ----------------
r = subprocess.run(["bash", "-c", 'R="2026-09-23: met at 14:00, ref ABC:123, owner ruled ok"; printf "%s" "${R%%:*}"'],
                   capture_output=True, text=True)
block("m14", "${RULING%%:*} on a reason holding two colons", ["result: [%s]" % r.stdout])

shutil.rmtree(W, ignore_errors=True)
LOG.append("F5_PROBES_DONE")
io.open(os.path.join(OUT, "SUMMARY.txt"), "w", encoding="utf-8").write("\n".join(LOG) + "\n")
print("\n".join(LOG))
