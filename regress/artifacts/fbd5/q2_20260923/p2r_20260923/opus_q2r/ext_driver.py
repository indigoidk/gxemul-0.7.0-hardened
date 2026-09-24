#!/usr/bin/env python3
"""Opus seat q2r -- SCRATCH EXPERIMENT: the frozen 491-row harness plus ext_rows.c (74 rows: Y1 cross-latch
order, Y2 legal access with latches SET keeps its value/effect, Y3 legal narrow +0x18c write), re-scored
against every variant that was GREEN on the 491 rows.  Works only in /tmp/opusq2r_ext; the variant sources
are rebuilt from the driver's one-hunk diffs against the FROZEN device."""
import csv, os, re, subprocess
P = "/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2r"
O = P + "/opus"
FROZEN_DEV = P + "/frozen/dev_footbridge.c"
FROZEN_HAR = P + "/frozen/diff_footbridge.c"
X = "/tmp/opusq2r"
E = "/tmp/opusq2r_ext"
os.makedirs(E + "/regress", exist_ok=True)
os.makedirs(E + "/src/devices", exist_ok=True)

har = open(FROZEN_HAR, encoding="utf-8", newline="").read()
ext = open(O + "/ext_rows.c", encoding="utf-8", newline="").read()
anchor = "\t/*  IDENTITY, as every differential here carries."
assert har.count(anchor) == 1
har2 = har.replace(anchor, ext + anchor)
assert har2.count('check("IDENTITY row count -- guards against a stale copy", buf, "491");') == 1
har2 = har2.replace('buf, "491");', 'buf, "565");')
open(E + "/regress/diff_footbridge.c", "w", encoding="utf-8", newline="").write(har2)

GCC = ["gcc", "-O2", "-std=c99", "-D_POSIX_C_SOURCE=200809L", "-D_DEFAULT_SOURCE",
       "-ffunction-sections", "-fdata-sections", "-Wl,--gc-sections",
       "-I" + X + "/src", "-I" + X + "/src/include", "-I" + X + "/src/include/thirdparty",
       "-o", "de", "diff_footbridge.c", "-lm"]


def score(tag):
    if os.path.exists(E + "/regress/de"):
        os.remove(E + "/regress/de")
    b = subprocess.run(GCC, cwd=E + "/regress", capture_output=True, text=True)
    if b.returncode:
        return ("BUILD-FAIL", "", "", b.stderr[-300:].replace("\n", " | "))
    r = subprocess.run(["./de"], cwd=E + "/regress", capture_output=True, text=True, timeout=120)
    out = r.stdout
    open(E + "/log_" + tag + ".log", "w").write(out)
    m = re.search(r"^(\d+) rows, (\d+) failures$", out, re.M)
    fails = [ln[8:].rstrip() for ln in out.splitlines() if ln.startswith("  FAIL  ") and "@@SELFCHECK@@" not in ln]
    return ("ok", m.group(1) if m else "?", m.group(2) if m else "?", fails[0] if fails else "-")


frozen_dev = open(FROZEN_DEV, encoding="utf-8", newline="").read()
open(E + "/src/devices/dev_footbridge.c", "w", encoding="utf-8", newline="").write(frozen_dev)
base = score("BASE")
print("EXT BASELINE", base, flush=True)
assert base[0] == "ok" and base[1] == "565" and base[2] == "0", base

greens = []
for fn in ("results.tsv", "results_dom.tsv"):
    for r in csv.DictReader(open(O + "/" + fn, encoding="utf-8"), delimiter="\t"):
        if r["build"] == "ok" and r["failures"] == "0":
            greens.append((r["vid"], r["family"], r["arm"], r["variant"]))
with open(O + "/results_ext.tsv", "w", encoding="utf-8") as f:
    f.write("vid\tfamily\tarm\tvariant\tbuild\trows\tfailures\tfirst_failing_row\n")
    for vid, fam, arm, text in greens:
        dev = E + "/src/devices/dev_footbridge.c"
        os.remove(dev)
        p = subprocess.run(["patch", "-s", "-o", dev, FROZEN_DEV], stdin=open(X + "/diffs/" + vid + ".diff"),
                           capture_output=True, text=True)
        if p.returncode:
            f.write("%s\t%s\t%s\t%s\tPATCH-FAIL\t\t\t\n" % (vid, fam, arm, text))
            continue
        st, rows, fails, first = score(vid)
        f.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (vid, fam, arm, text, st, rows, fails, first))
        f.flush()
open(E + "/src/devices/dev_footbridge.c", "w", encoding="utf-8", newline="").write(frozen_dev)
print("EXT_DONE", len(greens), flush=True)
