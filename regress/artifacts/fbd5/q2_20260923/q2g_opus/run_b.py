#!/usr/bin/env python3
"""Addendum runner: score gen_r3d_opus_b's two variants on BOTH the 864-row 3d harness and the 872-row scratch extension,
in /tmp/opusr3d_b (a copy of /tmp/opusr3d plus diff_ext.c).  Mutates only src/devices/dev_footbridge.c behind .MUTANT;
restores from the FROZEN copy, cmp-verifies, rebuilds BOTH binaries and re-runs both baselines before clearing it."""
import hashlib, io, json, os, re, subprocess, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_r3d_opus_b as gb  # noqa: E402
O = "/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2g/opus"
X = "/tmp/opusr3d_b"
SRC, REG, SENT = X + "/src/devices/dev_footbridge.c", X + "/regress", X + "/.MUTANT"
def cf(out, src):
    return ["gcc", "-O2", "-std=c99", "-Wall", "-D_POSIX_C_SOURCE=200809L", "-D_DEFAULT_SOURCE", "-ffunction-sections",
            "-fdata-sections", "-Wl,--gc-sections", "-I" + X + "/src", "-I" + X + "/src/include",
            "-I" + X + "/src/include/thirdparty", "-o", out, src, "-lm"]
def run(binname, src):
    p = REG + "/" + binname
    if os.path.exists(p):
        os.remove(p)
    b = subprocess.run(cf(binname, src), cwd=REG, capture_output=True)
    if b.returncode or os.path.getmtime(p) < os.path.getmtime(SRC):
        return dict(build="FAIL")
    r = subprocess.run(["./" + binname], cwd=REG, capture_output=True, timeout=120)
    out = r.stdout.decode("utf-8", "replace")
    m = re.search(r"^(\d+) rows, (\d+) failures$", out, re.M)
    return dict(rows=int(m.group(1)), fails=int(m.group(2)), warn=b.stderr.decode().count("warning:"),
                failing=[l[8:].rstrip() for l in out.splitlines() if l.startswith("  FAIL  ") and "@@SELFCHECK" not in l])
shutil.rmtree(X, ignore_errors=True)
subprocess.run(["cp", "-a", "/tmp/opusr3d", X], check=True)
shutil.copy(O + "/diff_ext.c", REG + "/diff_ext.c")
frozen = io.open(gb.FROZEN, encoding="utf-8", newline="").read()
assert io.open(SRC, encoding="utf-8", newline="").read() == frozen
b864, b872 = run("d", "diff_footbridge.c"), run("e", "diff_ext.c")
print("BASELINES", b864["rows"], b864["fails"], b872["rows"], b872["fails"], flush=True)
assert (b864["rows"], b864["fails"], b872["rows"], b872["fails"]) == (864, 0, 872, 0)
open(SENT, "w").write("src/devices/dev_footbridge.c: q2g addendum (run_b.py)\n")
res = []
try:
    for v in gb.variants():
        assert frozen.count(v["old"]) == 1
        io.open(SRC, "w", encoding="utf-8", newline="").write(frozen.replace(v["old"], v["new"]))
        r1, r2 = run("d", "diff_footbridge.c"), run("e", "diff_ext.c")
        rec = dict(vid=v["vid"], pred=v["pred"], on864=r1, on872=r2)
        res.append(rec)
        print("%-5s 864: %s/%s fails %s   872: %s/%s fails %s  warn %s/%s" % (v["vid"], r1.get("rows"), r1.get("fails"),
              r1.get("failing"), r2.get("rows"), r2.get("fails"), r2.get("failing"), r1.get("warn"), r2.get("warn")), flush=True)
finally:
    io.open(SRC, "w", encoding="utf-8", newline="").write(frozen)
    c = subprocess.run(["cmp", SRC, gb.FROZEN]).returncode
    f1, f2 = run("d", "diff_footbridge.c"), run("e", "diff_ext.c")
    ok = c == 0 and (f1["rows"], f1["fails"], f2["rows"], f2["fails"]) == (864, 0, 872, 0)
    print("RESTORE cmp rc=%d, rebuilt 864: %s/%s, 872: %s/%s" % (c, f1["rows"], f1["fails"], f2["rows"], f2["fails"]))
    if ok:
        os.remove(SENT); print("SENTINEL CLEARED")
    else:
        print("SENTINEL LEFT -- restore NOT verified")
io.open(O + "/results_b.jsonl", "w", encoding="utf-8").write("".join(json.dumps(r) + "\n" for r in res))
print("RUN_B_DONE")
