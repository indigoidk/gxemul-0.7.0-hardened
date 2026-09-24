#!/usr/bin/env python3
"""Opus seat, #545 q2c: score every variant on the FROZEN 707-row harness, and on the GATED copy with each row
family disabled at code level.

Usage: driver_q2c.py <worker k> <n workers>
Worker k owns /tmp/opusq2c_w<k> (a copy of /tmp/opusq2c) and takes the variants with index % n == k.
It mutates ONLY <tree>/src/devices/dev_footbridge.c, behind <tree>/.MUTANT, and at the end restores it from the
FROZEN copy, cmp-verifies it, rebuilds BOTH binaries, re-runs the baseline (707 rows, 0 failures, and the gated
binary byte-identical with FBSKIP unset), and only then clears the sentinel.
A variant whose anchor does not match exactly once is recorded as ANCHOR-ERROR, never as green.
"""
import hashlib, io, json, os, re, subprocess, sys, time, difflib

OUT = "/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2c/opus"
FZ = "/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2c/frozen"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # the frozen run copy's own gen_variants
import gen_variants  # noqa: E402

K, N = int(sys.argv[1]), int(sys.argv[2])
X = "/tmp/opusq2c_w%d" % K
SRC = X + "/src/devices/dev_footbridge.c"
REG = X + "/regress"
LOGS = X + "/logs"
DIFFS = X + "/diffs"
SENT = X + "/.MUTANT"
FROZEN_DEV = FZ + "/dev_footbridge.c"
BASELOG = OUT + "/baseline.log"
GATES = ["P", "X1", "X2", "X3", "X4", "X5", "X6", "X6R", "X6W", "X6P", "X7", "X7W", "X7R", "X8", "X9", "X9R", "X9W",
         "X10", "X10R", "X10W", "X11", "X12", "SEEDED", "ZERO", "WIDE", "ONES", "X9,X12", "X7,X10",
         "P,X1,X2,X3,X4,X5", "X6,X7,X9,X10,X11,X12"]
CF = ["gcc", "-O2", "-std=c99", "-Wall", "-D_POSIX_C_SOURCE=200809L", "-D_DEFAULT_SOURCE", "-ffunction-sections",
      "-fdata-sections", "-Wl,--gc-sections", "-I" + X + "/src", "-I" + X + "/src/include",
      "-I" + X + "/src/include/thirdparty"]


def sh(cmd, cwd=None, timeout=300, env=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, timeout=timeout, env=env)


def md5(path):
    return hashlib.md5(open(path, "rb").read()).hexdigest()


def parse(out):
    rows = fails = None
    verdict = "NONE"
    failing = []
    for ln in out.splitlines():
        m = re.match(r"^(\d+) rows, (\d+) failures$", ln)
        if m:
            rows, fails = int(m.group(1)), int(m.group(2))
        if ln.startswith("DIFF_FOOTBRIDGE_"):
            verdict = ln.strip()
        if ln.startswith("  FAIL  ") and "@@SELFCHECK@@" not in ln:
            failing.append(ln[8:].rstrip())
    return rows, fails, verdict, failing


def build():
    res = {}
    for exe, srcf in (("d", "diff_footbridge.c"), ("g", "diff_gated.c")):
        p = os.path.join(REG, exe)
        if os.path.exists(p):
            os.remove(p)
        b = sh(CF + ["-o", exe, srcf, "-lm"], cwd=REG)
        if b.returncode != 0 or not os.path.exists(p):
            return dict(ok=False, err=(b.stderr or b"").decode("utf-8", "replace")[-800:])
        if os.path.getmtime(p) < os.path.getmtime(SRC):
            return dict(ok=False, err="STALE-BINARY " + exe)
        res[exe] = md5(p)
        res["warn_" + exe] = (b.stderr or b"").decode("utf-8", "replace").count("warning:")
    res["ok"] = True
    return res


def run(exe, gate=None):
    env = dict(os.environ)
    env.pop("FBSKIP", None)
    if gate is not None:
        env["FBSKIP"] = gate
    try:
        r = sh(["./" + exe], cwd=REG, timeout=120, env=env)
        out, rc = (r.stdout + r.stderr).decode("utf-8", "replace"), r.returncode
    except subprocess.TimeoutExpired as e:
        so = e.stdout or b""
        out, rc = so.decode("utf-8", "replace"), "TIMEOUT"
    return out, rc


def score(tag):
    """Build both binaries for the current device text and run everything."""
    b = build()
    if not b["ok"]:
        return dict(build="BUILD-FAIL", err=b["err"])
    out_d, rc_d = run("d")
    io.open(os.path.join(LOGS, tag + ".log"), "w", encoding="utf-8").write(out_d)
    rows, fails, verdict, failing = parse(out_d)
    out_g, rc_g = run("g")
    gated_same = (out_g == out_d)
    gates = {}
    for g in GATES:
        o, rc = run("g", g)
        gr, gf, gv, gfail = parse(o)
        nonid = [x for x in gfail if not x.startswith("IDENTITY")]
        gates[g] = dict(rows=gr, n=len(nonid), done=gv != "NONE", rc=rc)
    return dict(build="ok", bmd5_d=b["d"], bmd5_g=b["g"], warn_d=b["warn_d"], warn_g=b["warn_g"], rc=rc_d, rows=rows,
                fails=fails, verdict=verdict, failing=failing, gated_same=gated_same, gates=gates)


def main():
    os.makedirs(LOGS, exist_ok=True)
    os.makedirs(DIFFS, exist_ok=True)
    frozen = io.open(FROZEN_DEV, encoding="utf-8", newline="").read()
    assert md5(FROZEN_DEV) == "783c0c7fb86823c6e9a5ae84be98b965", "frozen device md5 changed"
    assert md5(FZ + "/diff_footbridge.c") == "4d7bdcc3c6de6f904996cbb2b85719c2", "frozen harness md5 changed"
    assert io.open(SRC, encoding="utf-8", newline="").read() == frozen, "scratch device is not the frozen copy at start"
    assert sh(["cmp", REG + "/diff_footbridge.c", FZ + "/diff_footbridge.c"]).returncode == 0
    allv = gen_variants.variants()
    pre = os.environ.get("VIDPREFIX")   # second table: only the variants whose id starts with one of these
    if pre:
        allv = [v for v in allv if any(v["vid"].startswith(p) for p in pre.split(","))]
    mine = [v for i, v in enumerate(allv) if i % N == K]
    base = score("BASELINE_w%d" % K)
    baselog = io.open(BASELOG, encoding="utf-8").read()
    print("BASELINE", base["rows"], base["fails"], base["verdict"], "gated_same", base["gated_same"],
          "same as setup baseline.log", io.open(os.path.join(LOGS, "BASELINE_w%d.log" % K), encoding="utf-8").read() == baselog,
          flush=True)
    assert base["rows"] == 707 and base["fails"] == 0 and base["verdict"] == "DIFF_FOOTBRIDGE_PASS" and base["gated_same"]
    assert all(base["gates"][g]["n"] == 0 for g in GATES), "a gate reds the frozen device"
    base_d, base_g = base["bmd5_d"], base["bmd5_g"]
    open(SENT, "w").write("src/devices/dev_footbridge.c: one-line variant table in progress (driver_q2c.py w%d)\n" % K)
    rf = io.open(OUT + "/results%s_w%d.jsonl" % (os.environ.get("RESULTS_TAG", ""), K), "w", encoding="utf-8")
    t0 = time.time()
    try:
        for n, v in enumerate(mine):
            cnt = frozen.count(v["old"])
            rec = dict(vid=v["vid"], family=v["family"], arm=v["arm"], text=v["text"], pred=v["pred"], note=v["note"])
            if cnt != 1 or v["old"] == v["new"]:
                rec["build"] = "ANCHOR-ERROR(count=%d)" % cnt
            else:
                mut = frozen.replace(v["old"], v["new"])
                io.open(SRC, "w", encoding="utf-8", newline="").write(mut)
                diff = "".join(difflib.unified_diff(frozen.splitlines(True), mut.splitlines(True),
                                                    "frozen/dev_footbridge.c", v["vid"] + "/dev_footbridge.c", n=1))
                io.open(os.path.join(DIFFS, v["vid"] + ".diff"), "w", encoding="utf-8").write(diff)
                r = score(v["vid"])
                rec.update(r)
                if r.get("build") == "ok":
                    rec["binary_same_as_base"] = (r["bmd5_d"] == base_d)
            rf.write(json.dumps(rec) + "\n")
            rf.flush()
            if n % 10 == 0:
                print("w%d %4d/%d %6.0fs %s" % (K, n, len(mine), time.time() - t0, v["vid"]), flush=True)
    finally:
        rf.close()
        io.open(SRC, "w", encoding="utf-8", newline="").write(frozen)
        c = sh(["cmp", SRC, FROZEN_DEV])
        fin = score("BASELINE_AFTER_w%d" % K)
        ok = (c.returncode == 0 and fin.get("rows") == 707 and fin.get("fails") == 0
              and fin.get("verdict") == "DIFF_FOOTBRIDGE_PASS" and fin.get("gated_same")
              and fin.get("bmd5_d") == base_d and fin.get("bmd5_g") == base_g
              and os.path.getmtime(REG + "/d") > os.path.getmtime(SRC))
        print("RESTORE w%d cmp rc=%d after: %s %s %s gated_same=%s binary==base: %s/%s" % (
            K, c.returncode, fin.get("rows"), fin.get("fails"), fin.get("verdict"), fin.get("gated_same"),
            fin.get("bmd5_d") == base_d, fin.get("bmd5_g") == base_g), flush=True)
        if ok:
            os.remove(SENT)
            print("SENTINEL CLEARED w%d" % K, flush=True)
        else:
            print("SENTINEL LEFT IN PLACE w%d -- restore NOT verified" % K, flush=True)
    print("DRIVER_DONE w%d %d variants in %.0fs" % (K, len(mine), time.time() - t0), flush=True)


main()
