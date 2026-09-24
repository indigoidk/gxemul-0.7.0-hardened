#!/usr/bin/env python3
"""Opus seat, #545 repair-3c pass (q2f): score gen_q2f's variants on the FROZEN 864-row instrument.

Usage: driver_q2f.py <worker k> <n workers>.  Worker k owns /tmp/opusq2f_w<k> (a copy of /tmp/opusq2f) and takes the
variants with index % n == k.  It mutates ONLY <tree>/src/devices/dev_footbridge.c behind <tree>/.MUTANT, and at the
end restores it from the FROZEN copy, cmp-verifies, rebuilds, re-runs the baseline (864 rows, 0 failures, the same
binary md5 as before), and only then clears the sentinel.  An anchor that does not match exactly once is recorded as
ANCHOR-ERROR, never as green.
"""
import hashlib, io, json, os, re, subprocess, sys, time, difflib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # the frozen run copy's own gen_q2f
import gen_q2f  # noqa: E402

OUT = "/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2f/opus"
FZ = "/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2f/frozen"
K, N = int(sys.argv[1]), int(sys.argv[2])
X = "/tmp/opusq2f_w%d" % K
SRC = X + "/src/devices/dev_footbridge.c"
REG = X + "/regress"
LOGS, DIFFS, SENT = X + "/logs", X + "/diffs", X + "/.MUTANT"
CF = ["gcc", "-O2", "-std=c99", "-Wall", "-D_POSIX_C_SOURCE=200809L", "-D_DEFAULT_SOURCE", "-ffunction-sections",
      "-fdata-sections", "-Wl,--gc-sections", "-I" + X + "/src", "-I" + X + "/src/include",
      "-I" + X + "/src/include/thirdparty", "-o", "d", "diff_footbridge.c", "-lm"]


def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


def score(tag):
    p = REG + "/d"
    if os.path.exists(p):
        os.remove(p)
    b = subprocess.run(CF, cwd=REG, capture_output=True)
    if b.returncode != 0 or not os.path.exists(p):
        return dict(build="BUILD-FAIL", err=b.stderr.decode("utf-8", "replace")[-800:])
    if os.path.getmtime(p) < os.path.getmtime(SRC):
        return dict(build="STALE-BINARY")
    try:
        r = subprocess.run(["./d"], cwd=REG, capture_output=True, timeout=120)
        out, rc = (r.stdout + r.stderr).decode("utf-8", "replace"), r.returncode
    except subprocess.TimeoutExpired as e:
        out, rc = (e.stdout or b"").decode("utf-8", "replace"), "TIMEOUT"
    io.open(os.path.join(LOGS, tag + ".log"), "w", encoding="utf-8").write(out)
    m = re.search(r"^(\d+) rows, (\d+) failures$", out, re.M)
    failing = [l[8:].rstrip() for l in out.splitlines() if l.startswith("  FAIL  ") and "@@SELFCHECK@@" not in l]
    v = re.search(r"^DIFF_FOOTBRIDGE_(\w+)", out, re.M)
    return dict(build="ok", bmd5=md5(p), warn=b.stderr.decode("utf-8", "replace").count("warning:"), rc=rc,
                rows=int(m.group(1)) if m else None, fails=int(m.group(2)) if m else None,
                verdict=v.group(1) if v else "NONE", failing=failing)


def main():
    os.makedirs(LOGS, exist_ok=True)
    os.makedirs(DIFFS, exist_ok=True)
    assert md5(FZ + "/dev_footbridge.c") == "783c0c7fb86823c6e9a5ae84be98b965"
    assert md5(FZ + "/diff_footbridge.c") == "8309c5b779a4f909f45e4863a484f9ac"
    frozen = io.open(FZ + "/dev_footbridge.c", encoding="utf-8", newline="").read()
    assert io.open(SRC, encoding="utf-8", newline="").read() == frozen, "scratch device is not the frozen copy at start"
    assert subprocess.run(["cmp", REG + "/diff_footbridge.c", FZ + "/diff_footbridge.c"]).returncode == 0
    mine = [v for i, v in enumerate(gen_q2f.variants()) if i % N == K]
    base = score("BASELINE_w%d" % K)
    print("BASELINE", base.get("rows"), base.get("fails"), base.get("verdict"), "same as setup baseline.log:",
          io.open(os.path.join(LOGS, "BASELINE_w%d.log" % K), encoding="utf-8").read()
          == io.open(OUT + "/baseline.log", encoding="utf-8").read(), flush=True)
    assert base["rows"] == 864 and base["fails"] == 0 and base["verdict"] == "PASS"
    open(SENT, "w").write("src/devices/dev_footbridge.c: q2f variant table in progress (driver_q2f.py w%d)\n" % K)
    rf = io.open(OUT + "/results_w%d.jsonl" % K, "w", encoding="utf-8")
    t0 = time.time()
    try:
        for n, v in enumerate(mine):
            rec = {k: v[k] for k in ("vid", "family", "arm", "text", "pred", "target", "note")}
            cnt = frozen.count(v["old"])
            if cnt != 1 or v["old"] == v["new"]:
                rec["build"] = "ANCHOR-ERROR(count=%d)" % cnt
            else:
                mut = frozen.replace(v["old"], v["new"])
                io.open(SRC, "w", encoding="utf-8", newline="").write(mut)
                io.open(os.path.join(DIFFS, v["vid"] + ".diff"), "w", encoding="utf-8").write("".join(
                    difflib.unified_diff(frozen.splitlines(True), mut.splitlines(True), "frozen/dev_footbridge.c",
                                         v["vid"] + "/dev_footbridge.c", n=1)))
                rec.update(score(v["vid"]))
            rf.write(json.dumps(rec) + "\n")
            rf.flush()
            print("w%d %3d/%d %5.0fs %s %s" % (K, n, len(mine), time.time() - t0, v["vid"],
                                               "GREEN" if rec.get("fails") == 0 else "red %s" % rec.get("fails")), flush=True)
    finally:
        rf.close()
        io.open(SRC, "w", encoding="utf-8", newline="").write(frozen)
        c = subprocess.run(["cmp", SRC, FZ + "/dev_footbridge.c"]).returncode
        fin = score("BASELINE_AFTER_w%d" % K)
        ok = (c == 0 and fin.get("rows") == 864 and fin.get("fails") == 0 and fin.get("bmd5") == base["bmd5"]
              and os.path.getmtime(REG + "/d") > os.path.getmtime(SRC))
        print("RESTORE w%d cmp rc=%d after: %s %s binary==base: %s" % (K, c, fin.get("rows"), fin.get("fails"),
                                                                     fin.get("bmd5") == base["bmd5"]), flush=True)
        if ok:
            os.remove(SENT)
            print("SENTINEL CLEARED w%d" % K, flush=True)
        else:
            print("SENTINEL LEFT IN PLACE w%d -- restore NOT verified" % K, flush=True)
    print("DRIVER_DONE w%d %d variants in %.0fs" % (K, len(mine), time.time() - t0), flush=True)


main()
