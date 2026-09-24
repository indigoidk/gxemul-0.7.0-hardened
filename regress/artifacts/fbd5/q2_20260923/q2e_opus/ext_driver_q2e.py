#!/usr/bin/env python3
"""Opus seat, #545 q2e: SCRATCH CLOSURE EXPERIMENT -- re-score variants on the 862 rows + the 19 Y rows (mkext_q2e.py).
Mutates ONLY /tmp/opusq2e_ext/src/devices/dev_footbridge.c behind /tmp/opusq2e_ext/.MUTANT; restores from the FROZEN
copy, cmp-verifies, rebuilds, re-runs the 881-row baseline, and only then clears the sentinel.  The field z_failing holds
the failing Y rows (name kept from the q2c driver).  Usage: ext_driver_q2e.py ALL | GREENS | <vid>..."""
import hashlib, io, json, os, re, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # the frozen run copy's own gen_variants
import gen_q2e as gen_variants  # noqa: E402
O = "/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2e/opus"    # results in, results out

X = "/tmp/opusq2e_ext"
SRC = X + "/src/devices/dev_footbridge.c"
REG = X + "/regress"
SENT = X + "/.MUTANT"
FROZEN = gen_variants.FROZEN
CF = ["gcc", "-O2", "-std=c99", "-Wall", "-D_POSIX_C_SOURCE=200809L", "-D_DEFAULT_SOURCE", "-ffunction-sections",
      "-fdata-sections", "-Wl,--gc-sections", "-I" + X + "/src", "-I" + X + "/src/include",
      "-I" + X + "/src/include/thirdparty", "-o", "e", "diff_ext.c", "-lm"]


def build_run():
    if os.path.exists(REG + "/e"):
        os.remove(REG + "/e")
    b = subprocess.run(CF, cwd=REG, capture_output=True)
    if b.returncode != 0 or os.path.getmtime(REG + "/e") < os.path.getmtime(SRC):
        return None
    r = subprocess.run(["./e"], cwd=REG, capture_output=True, timeout=120)
    out = (r.stdout + r.stderr).decode("utf-8", "replace")
    m = re.search(r"^(\d+) rows, (\d+) failures$", out, re.M)
    failing = [l[8:].rstrip() for l in out.splitlines() if l.startswith("  FAIL  ") and "@@SELFCHECK@@" not in l]
    return dict(rows=int(m.group(1)) if m else None, fails=int(m.group(2)) if m else None, failing=failing,
                bmd5=hashlib.md5(open(REG + "/e", "rb").read()).hexdigest(), warn=b.stderr.decode().count("warning:"))


vids = sys.argv[1:]
if vids == ["ALL"]:
    vids = [v["vid"] for v in gen_variants.variants()]
elif vids == ["GREENS"]:
    vids = []
    for fn in ("results_all.jsonl",):
        for l in io.open(os.path.join(O, fn), encoding="utf-8"):
            r = json.loads(l)
            if r.get("build") == "ok" and r.get("rows") == 862 and r.get("fails") == 0:
                vids.append(r["vid"])
frozen = io.open(FROZEN, encoding="utf-8", newline="").read()
assert io.open(SRC, encoding="utf-8", newline="").read() == frozen, "scratch device is not the frozen copy at start"
allv = {v["vid"]: v for v in gen_variants.variants()}
base = build_run()
print("BASELINE ext:", base["rows"], base["fails"], base["failing"], "warnings", base["warn"], flush=True)
assert base["rows"] == 881 and base["fails"] == 0
open(SENT, "w").write("src/devices/dev_footbridge.c: closure-experiment re-score in progress (ext_driver.py)\n")
res = io.open(os.path.join(O, "ext_results.jsonl"), "w", encoding="utf-8")
try:
    for vid in vids:
        v = allv[vid]
        assert frozen.count(v["old"]) == 1
        io.open(SRC, "w", encoding="utf-8", newline="").write(frozen.replace(v["old"], v["new"]))
        r = build_run()
        z = [f for f in r["failing"] if f.startswith("Y")] if r else None
        rec = dict(vid=vid, rows=r and r["rows"], fails=r and r["fails"], z_failing=z,
                   other_failing=[f for f in r["failing"] if not f.startswith("Y") and not f.startswith("IDENTITY")] if r else None)
        res.write(json.dumps(rec) + "\n")
        res.flush()
        print("%-22s %s" % (vid, ("GREEN" if r and r["fails"] == 0 else "RED  y=%d: %s" % (len(z), "; ".join(z[:2])))
                            if r else "BUILD-FAIL"), flush=True)
finally:
    res.close()
    io.open(SRC, "w", encoding="utf-8", newline="").write(frozen)
    c = subprocess.run(["cmp", SRC, FROZEN]).returncode
    fin = build_run()
    ok = c == 0 and fin and fin["rows"] == 881 and fin["fails"] == 0 and fin["bmd5"] == base["bmd5"]
    print("RESTORE cmp rc=%d after: %s %s binary==base %s" % (c, fin and fin["rows"], fin and fin["fails"],
                                                             fin and fin["bmd5"] == base["bmd5"]), flush=True)
    if ok:
        os.remove(SENT)
        print("SENTINEL CLEARED", flush=True)
    else:
        print("SENTINEL LEFT IN PLACE -- restore NOT verified", flush=True)
print("EXT_DONE", len(vids))
