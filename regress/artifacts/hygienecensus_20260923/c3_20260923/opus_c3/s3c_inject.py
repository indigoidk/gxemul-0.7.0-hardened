#!/usr/bin/env python3
# SECTION 3c -- definitive injection test for Unicode separators in --ruling.
# Clean write path: add a 4th REAL whole site to an ALLOWLISTED file (arm_bdt) -> EXPECT_WHOLE_FULL/WHOLE_FULL_FILES
# change -> NEED set, needs a ruling, and NO new promptless probe.  Then --write --ruling <sep embedded>.  Inspect the
# gate: rc, WRITTEN?, bash -n, any BARE (non-comment) line that is not there in the original, and the RULING line bytes.
import io, os, shutil, subprocess, sys, tempfile
SEC = "/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC"
FROZ = "/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/c3_frozen"
OUT = "/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/opus_c3/s3c"
shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
W = tempfile.mkdtemp(prefix="gxc3_s3c_")
SNAP = os.path.join(W, "snap")
os.makedirs(os.path.join(SNAP, "GXEMUL-SEC/regress")); os.makedirs(os.path.join(SNAP, "GXEMUL-SEC/tools"))
for f in os.listdir(os.path.join(SEC, "regress")):
    p = os.path.join(SEC, "regress", f)
    if os.path.isfile(p): shutil.copy2(p, os.path.join(SNAP, "GXEMUL-SEC/regress", f))
shutil.copy2(os.path.join(SEC, "tools/derive_hygiene_pins.sh"), os.path.join(SNAP, "GXEMUL-SEC/tools"))
for f in ("gate_hygiene.sh", "census_tokens.py"):
    shutil.copy2(os.path.join(FROZ, f), os.path.join(SNAP, "GXEMUL-SEC/regress", f))
shutil.copy2(os.path.join(FROZ, "derive_hygiene_pins.sh"), os.path.join(SNAP, "GXEMUL-SEC/tools"))
ORIG_LINES = set(io.open(os.path.join(SNAP, "GXEMUL-SEC/regress/gate_hygiene.sh"), encoding="utf-8").read().split("\n"))

def once(tag, sep, sep_label):
    d = os.path.join(W, tag); shutil.rmtree(d, ignore_errors=True); shutil.copytree(SNAP, d)
    rd = os.path.join(d, "GXEMUL-SEC/regress")
    # add a 4th whole site to the allowlisted arm_bdt (self.buf ends 'buf' -> a real whole site)
    p = os.path.join(rd, "arm_bdt_probe.py"); s = io.open(p, encoding="utf-8").read()
    io.open(p, "w", encoding="utf-8").write(s + '\n    _c4 = self.buf.rstrip().endswith("GXemul>")\n')
    ruling = "2026-09-23: a valid enough reason here" + sep + "EXPECT_WHOLE_FULL=999"
    env = dict(os.environ, GXROOT=d)
    r = subprocess.run(["bash", os.path.join(d, "GXEMUL-SEC/tools/derive_hygiene_pins.sh"), "--write", "--ruling", ruling],
                       env=env, capture_output=True, text=True, errors="replace")
    g = io.open(os.path.join(rd, "gate_hygiene.sh"), encoding="utf-8").read()
    bn = subprocess.run(["bash", "-n", "gate_hygiene.sh"], cwd=rd, capture_output=True, text=True)
    # a NEW bare (non-comment, non-blank) line that was not in the original and is not a known pin assignment
    newlines = [l for l in g.split("\n") if l not in ORIG_LINES and l.strip() and not l.lstrip().startswith("#")]
    ruling_line = [l for l in g.split("\n") if l.startswith("#  RULING")]
    io.open(os.path.join(OUT, tag + ".gate.txt"), "w", encoding="utf-8", errors="replace").write(g)
    verdict = "WRITTEN" if r.returncode == 0 else ("REFUSED(rc%d)" % r.returncode)
    print("== %s (%s)" % (sep_label, tag))
    print("   deriver: %s   bash-n: %s" % (verdict, "OK" if bn.returncode == 0 else "PARSE-FAIL " + bn.stderr.strip()[:60]))
    print("   NEW non-comment lines introduced: %d %s" % (len(newlines), ([l[:70] for l in newlines] if newlines else "")))
    for rl in ruling_line:
        print("   RULING line bytes:", rl.encode("utf-8", "replace"))

print("Clean injection test: a 4th whole site (arm_bdt) makes NEED non-empty with NO new promptless probe.\n")
once("plain", "", "no separator (control)")
once("nl", "\n", "U+000A newline")
once("nel", "\u0085", "U+0085 NEL")
once("ls", " ", "U+2028 LINE SEP")
once("ps", " ", "U+2029 PARA SEP")
shutil.rmtree(W, ignore_errors=True)
print("S3C_DONE")
