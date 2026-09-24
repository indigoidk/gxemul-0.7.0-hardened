#!/usr/bin/env python3
# SECTION 3b -- (1) does the F3 control-char check catch Unicode line/para separators, and if one slips through and is
# WRITTEN, can it inject a non-comment line into the gate?  (2) exact --release, inspected on the LIST BODY not a grep.
import io, os, shutil, subprocess, sys, tempfile
SEC = "/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC"
FROZ = "/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/c3_frozen"
OUT = "/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/opus_c3/s3b"
shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
W = tempfile.mkdtemp(prefix="gxc3_s3b_")
SNAP = os.path.join(W, "snap")
os.makedirs(os.path.join(SNAP, "GXEMUL-SEC/regress")); os.makedirs(os.path.join(SNAP, "GXEMUL-SEC/tools"))
for f in os.listdir(os.path.join(SEC, "regress")):
    p = os.path.join(SEC, "regress", f)
    if os.path.isfile(p): shutil.copy2(p, os.path.join(SNAP, "GXEMUL-SEC/regress", f))
shutil.copy2(os.path.join(SEC, "tools/derive_hygiene_pins.sh"), os.path.join(SNAP, "GXEMUL-SEC/tools"))
for f in ("gate_hygiene.sh", "census_tokens.py"):
    shutil.copy2(os.path.join(FROZ, f), os.path.join(SNAP, "GXEMUL-SEC/regress", f))
shutil.copy2(os.path.join(FROZ, "derive_hygiene_pins.sh"), os.path.join(SNAP, "GXEMUL-SEC/tools"))
DERIV = os.path.join(SNAP, "GXEMUL-SEC/tools/derive_hygiene_pins.sh")   # snapshot copy; per-case we re-copy the tree

def fresh(tag):
    d = os.path.join(W, tag); shutil.rmtree(d, ignore_errors=True); shutil.copytree(SNAP, d); return d
def rdir(d): return os.path.join(d, "GXEMUL-SEC/regress")
def add_whole(d):  # a real whole-buffer site so NEED is non-empty
    p = os.path.join(rdir(d), "luna_absentcpu_probe.py")
    s = io.open(p, encoding="utf-8").read()
    io.open(p, "w", encoding="utf-8").write(s + '\n_c = lambda mybuf: mybuf.rstrip().endswith("GXemul>")\n')
def run(d, args):
    env = dict(os.environ, GXROOT=d)
    return subprocess.run(["bash", os.path.join(d, "GXEMUL-SEC/tools/derive_hygiene_pins.sh")] + args,
                          env=env, capture_output=True, text=True, errors="replace")
def bashn(d):
    r = subprocess.run(["bash", "-n", "gate_hygiene.sh"], cwd=rdir(d), capture_output=True, text=True)
    return "OK" if r.returncode == 0 else "PARSE-FAIL: " + r.stderr.strip()[:80]

print("== Q1(c) Unicode separators in --ruling (real bytes) ==")
for label, sep in [("U+0085 NEL", "\u0085"), ("U+2028 LS", " "), ("U+2029 PS", " "), ("U+000B VT", "\u000b")]:
    d = fresh("u_" + repr(sep)); add_whole(d)
    ruling = "2026-09-23: a valid enough reason here" + sep + "EXPECT_WHOLE_FULL=999"
    r = run(d, ["--write", "--ruling", ruling])
    g = io.open(os.path.join(rdir(d), "gate_hygiene.sh"), encoding="utf-8").read()
    inj = "\nEXPECT_WHOLE_FULL=999" in g and not g.split("EXPECT_WHOLE_FULL=999")[0].rstrip("\r ").endswith("#  RULING 2026-09-23: a valid enough reason here" + sep)
    # simpler injection test: is there a bare (non-comment) line equal to EXPECT_WHOLE_FULL=999 ?
    bare999 = any(l.strip() == "EXPECT_WHOLE_FULL=999" for l in g.split("\n"))
    verdict = "REFUSED" if r.returncode != 0 else "WRITTEN"
    print("  %-11s rc=%d %-8s bash-n=%-11s bare-999-line=%s  first=[%s]" %
          (label, r.returncode, verdict, bashn(d), bare999, (r.stdout.strip().split(chr(10))[0][:60] if r.stdout.strip() else "")))
    io.open(os.path.join(OUT, "u_%s.txt" % label.split()[0]), "w", encoding="utf-8", errors="replace").write(r.stdout + "\n---STDERR---\n" + r.stderr)

print("\n== Q1(d) exact --release on the LIST BODY (not a comment-polluted grep) ==")
def gf_body(d):
    s = io.open(os.path.join(rdir(d), "gate_hygiene.sh"), encoding="utf-8").read()
    i = s.index('GRANDFATHERED_PROMPTLESS="') + len('GRANDFATHERED_PROMPTLESS="'); j = s.index('"', i)
    return s[i:j].split()
d = fresh("relpref")
# insert x-gdrom_cond_probe.py beside gdrom_cond_probe.py in the LIST
gp = os.path.join(rdir(d), "gate_hygiene.sh"); s = io.open(gp, encoding="utf-8").read()
s = s.replace("gdrom_cond_probe.py sgi_re_width_probe.py", "gdrom_cond_probe.py x-gdrom_cond_probe.py sgi_re_width_probe.py", 1)
io.open(gp, "w", encoding="utf-8").write(s)
before = gf_body(d)
# make gdrom_cond_probe.py NO LONGER promptless (real code endswith); x-gdrom_cond_probe.py is not a file -> also 'gone'
p = os.path.join(rdir(d), "gdrom_cond_probe.py"); s = io.open(p, encoding="utf-8").read()
io.open(p, "w", encoding="utf-8").write(s + '\n_r = lambda gbuf: gbuf.rstrip().endswith("GXemul>")\n')
r = run(d, ["--release", "gdrom_cond_probe.py"])
after = gf_body(d)
print("  --release gdrom_cond_probe.py -> rc=%d  %s" % (r.returncode, (r.stdout.strip().split(chr(10))[-1][:50])))
print("  list had gdrom_cond_probe.py: %d, x-gdrom_cond_probe.py: %d  (before)" % (before.count("gdrom_cond_probe.py"), before.count("x-gdrom_cond_probe.py")))
print("  list has  gdrom_cond_probe.py: %d, x-gdrom_cond_probe.py: %d  (after)" % (after.count("gdrom_cond_probe.py"), after.count("x-gdrom_cond_probe.py")))
print("  exact-release OK (removed the exact name, kept the prefixed one): %s" %
      (after.count("gdrom_cond_probe.py") == before.count("gdrom_cond_probe.py") - 1 and "x-gdrom_cond_probe.py" in after))
shutil.rmtree(W, ignore_errors=True)
print("S3B_DONE")
