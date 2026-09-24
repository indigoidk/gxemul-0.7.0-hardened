#!/usr/bin/env python3
"""Opus seat q2h driver: score every shape on BOTH the 3d (6c92d7e5) and 3e (15a1c2a2) instruments.
Worker k owns /tmp/opusr3e_w<k>; mutates ONLY its device behind a .MUTANT sentinel; restores from the frozen
device, cmp-verifies, rebuilds both baselines, and clears the sentinel only when both are 864/0 and binaries fresh."""
import hashlib, io, json, os, re, subprocess, sys, time, difflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import collect  # noqa: E402

O = "/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2h/opus"
FZ = "/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2h/frozen"
DEVMD5 = "783c0c7fb86823c6e9a5ae84be98b965"
K, N = int(sys.argv[1]), int(sys.argv[2])
X = "/tmp/opusr3e_w%d" % K
SRC = X + "/src/devices/dev_footbridge.c"
REG = X + "/regress"
LOGS, SENT = X + "/logs", X + "/.MUTANT"


def cf(srcfile, out):
    return ["gcc", "-O2", "-std=c99", "-Wall", "-D_POSIX_C_SOURCE=200809L", "-D_DEFAULT_SOURCE",
            "-ffunction-sections", "-fdata-sections", "-Wl,--gc-sections", "-I" + X + "/src",
            "-I" + X + "/src/include", "-I" + X + "/src/include/thirdparty", "-o", out, srcfile, "-lm"]


def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


def build_run(srcfile, binf, tag):
    p = REG + "/" + binf
    if os.path.exists(p):
        os.remove(p)
    b = subprocess.run(cf(srcfile, binf), cwd=REG, capture_output=True)
    warn = b.stderr.decode("utf-8", "replace").count("warning:")
    if b.returncode != 0 or not os.path.exists(p):
        return dict(build="BUILD-FAIL", warn=warn, err=b.stderr.decode("utf-8", "replace")[-400:])
    if os.path.getmtime(p) < os.path.getmtime(SRC):
        return dict(build="STALE-BINARY")
    try:
        r = subprocess.run(["./" + binf], cwd=REG, capture_output=True, timeout=120)
        out = (r.stdout + r.stderr).decode("utf-8", "replace")
    except subprocess.TimeoutExpired as e:
        return dict(build="TIMEOUT", warn=warn)
    io.open(os.path.join(LOGS, tag + ".log"), "w", encoding="utf-8").write(out)
    m = re.search(r"^(\d+) rows, (\d+) failures$", out, re.M)
    failing = sorted(l[8:].rstrip() for l in out.splitlines()
                     if l.startswith("  FAIL  ") and "@@SELFCHECK@@" not in l)
    return dict(build="ok", warn=warn, bmd5=md5(p),
                rows=int(m.group(1)) if m else None, fails=int(m.group(2)) if m else None, failing=failing)


def main():
    os.makedirs(LOGS, exist_ok=True)
    assert md5(FZ + "/dev_footbridge.c") == DEVMD5
    frozen = io.open(FZ + "/dev_footbridge.c", encoding="utf-8", newline="").read()
    assert io.open(SRC, encoding="utf-8", newline="").read() == frozen, "scratch device != frozen at start"
    b3d0 = build_run(REG + "/diff_footbridge.3d.c", "b3d", "BASE3d_w%d" % K)
    b3e0 = build_run(REG + "/diff_footbridge.3e.c", "b3e", "BASE3e_w%d" % K)
    assert b3d0.get("rows") == 864 and b3d0.get("fails") == 0, b3d0
    assert b3e0.get("rows") == 864 and b3e0.get("fails") == 0, b3e0
    shapes = [v for i, v in enumerate(collect.all_shapes()) if i % N == K]
    rf = io.open(O + "/results_w%d.jsonl" % K, "w", encoding="utf-8")
    open(SENT, "w").write("dev_footbridge.c: q2h variant table (driver.py w%d)\n" % K)
    t0 = time.time()
    try:
        for n, v in enumerate(shapes):
            rec = {k: v[k] for k in ("vid", "family", "src", "arm", "text", "pred3d", "pred3e", "target", "note")}
            cnt = frozen.count(v["old"])
            if cnt != 1 or v["old"] == v["new"]:
                rec["err"] = "ANCHOR(count=%d)" % cnt
            else:
                io.open(SRC, "w", encoding="utf-8", newline="").write(frozen.replace(v["old"], v["new"]))
                rec["r3d"] = build_run(REG + "/diff_footbridge.3d.c", "b3d", v["vid"] + "_3d")
                rec["r3e"] = build_run(REG + "/diff_footbridge.3e.c", "b3e", v["vid"] + "_3e")
            rf.write(json.dumps(rec) + "\n")
            rf.flush()
            def st(r):
                if not r or r.get("build") != "ok":
                    return (r or {}).get("build", "?")
                return "GREEN" if r.get("fails") == 0 else "red%s" % r.get("fails")
            print("w%d %2d/%d %5.0fs %-8s 3d=%s 3e=%s" % (K, n, len(shapes), time.time() - t0, v["vid"],
                  st(rec.get("r3d")), st(rec.get("r3e"))), flush=True)
    finally:
        rf.close()
        io.open(SRC, "w", encoding="utf-8", newline="").write(frozen)
        c = subprocess.run(["cmp", SRC, FZ + "/dev_footbridge.c"]).returncode
        f3d = build_run(REG + "/diff_footbridge.3d.c", "b3d", "AFTER3d_w%d" % K)
        f3e = build_run(REG + "/diff_footbridge.3e.c", "b3e", "AFTER3e_w%d" % K)
        good = (c == 0 and f3d.get("rows") == 864 and f3d.get("fails") == 0 and f3d.get("bmd5") == b3d0["bmd5"]
                and f3e.get("rows") == 864 and f3e.get("fails") == 0 and f3e.get("bmd5") == b3e0["bmd5"])
        print("RESTORE w%d cmp=%d 3d=%s/%s 3e=%s/%s bins==base:%s" % (K, c, f3d.get("rows"), f3d.get("fails"),
              f3e.get("rows"), f3e.get("fails"), f3d.get("bmd5") == b3d0["bmd5"] and f3e.get("bmd5") == b3e0["bmd5"]),
              flush=True)
        if good:
            os.remove(SENT)
            print("SENTINEL CLEARED w%d" % K, flush=True)
        else:
            print("SENTINEL LEFT w%d -- restore NOT verified" % K, flush=True)
    print("DRIVER_DONE w%d %d shapes %.0fs" % (K, len(shapes), time.time() - t0), flush=True)


main()
