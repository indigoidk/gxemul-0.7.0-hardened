#!/usr/bin/env python3
"""#545 r3e table, one worker: score the variants named in LIST (index % N == K) on the instrument INSTR (md5 prefix
MD5), writing results_<TAG>_w<K>.jsonl.  Tree /tmp/fbd5r3e_<TAG>_w<K>: a copy of SEC src; ONLY
src/devices/dev_footbridge.c is mutated, behind .MUTANT; at the end it is restored from SEC, cmp'd, rebuilt and re-run
(must be 864 rows, 0 failures) before the sentinel is cleared.
usage: run_r3e_worker.py K N TAG INSTR MD5 LIST"""
import hashlib, io, json, os, re, shutil, subprocess, sys

R = "/mnt/c/DocumentNoSnc/CC/GXEMUL"
SEC = R + "/GXEMUL-SEC"
OUT = SEC + "/regress/artifacts/fbd5/q2_20260923/r3e_20260923"
V = "/tmp/fbd5r3e_var"
K, N, TAG, INSTR, MD5, LIST = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6]
X = "/tmp/fbd5r3e_%s_w%d" % (TAG, K)
DEV = X + "/src/devices/dev_footbridge.c"
SENT = X + "/.MUTANT"
CF = ["gcc", "-O2", "-std=c99", "-Wall", "-D_POSIX_C_SOURCE=200809L", "-D_DEFAULT_SOURCE", "-ffunction-sections",
      "-fdata-sections", "-Wl,--gc-sections", "-I" + X + "/src", "-I" + X + "/src/include",
      "-I" + X + "/src/include/thirdparty"]


def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


def build_and_run():
    exe = X + "/d"
    if os.path.exists(exe):
        os.remove(exe)
    b = subprocess.run(CF + ["-o", exe, "diff_footbridge.c", "-lm"], cwd=X + "/regress", capture_output=True)
    if b.returncode != 0 or not os.path.exists(exe) or os.path.getmtime(exe) < os.path.getmtime(DEV):
        return dict(build="FAIL", err=b.stderr.decode("utf-8", "replace")[-400:])
    warn = b.stderr.decode("utf-8", "replace").count("warning:")
    try:
        r = subprocess.run([exe], capture_output=True, timeout=120)
        out, rc = r.stdout.decode("utf-8", "replace"), r.returncode
    except subprocess.TimeoutExpired:
        return dict(build="ok", warn=warn, rc="TIMEOUT", rows=None, fails=None, failing=[], verdict="TIMEOUT")
    m = re.search(r"^(\d+) rows, (\d+) failures$", out, re.M)
    failing = sorted(set(l[8:].rstrip() for l in out.splitlines()
                         if l.startswith("  FAIL  ") and "@@SELFCHECK@@" not in l))
    v = re.search(r"^DIFF_FOOTBRIDGE_(\w+)$", out, re.M)
    return dict(build="ok", warn=warn, rc=rc, rows=int(m.group(1)) if m else None,
                fails=int(m.group(2)) if m else None, failing=failing,
                verdict=v.group(1) if v else "NONE", nlines=out.count("\n"))


shutil.rmtree(X, ignore_errors=True)
os.makedirs(X + "/regress")
shutil.copytree(SEC + "/src", X + "/src", symlinks=True)
shutil.copy(R + "/build/config.h", X + "/config.h")      # misc.h includes ../../config.h
shutil.copy(INSTR, X + "/regress/diff_footbridge.c")
assert md5(X + "/regress/diff_footbridge.c").startswith(MD5), "instrument md5"
assert md5(DEV) == md5(SEC + "/src/devices/dev_footbridge.c"), "worker tree device != SEC before the run"
open(SENT, "w").write("#545 r3e worker %s %d -- restore dev_footbridge.c from SEC\n" % (TAG, K))
names = [l.strip() for l in io.open(LIST, encoding="utf-8") if l.strip()]
mine = [n for i, n in enumerate(names) if i % N == K]
with io.open(OUT + "/results_%s_w%d.jsonl" % (TAG, K), "w", encoding="utf-8", newline="\n") as fh:
    for n in mine:
        shutil.copy(V + "/" + n + ".c", DEV)
        res = build_and_run()
        res.update(vid=n, dev_md5=md5(DEV)[:8])
        fh.write(json.dumps(res) + "\n")
        fh.flush()
shutil.copy(SEC + "/src/devices/dev_footbridge.c", DEV)
ok = md5(DEV) == md5(SEC + "/src/devices/dev_footbridge.c")
base = build_and_run()
if ok and base.get("rows") == 864 and base.get("fails") == 0:
    os.remove(SENT)
    print("WORKER %s %d: %d variants; restored (cmp == SEC), rebuilt, baseline 864/0; sentinel cleared" % (TAG, K, len(mine)))
else:
    print("WORKER %s %d: RESTORE NOT VERIFIED -- cmp %s, baseline %s; SENTINEL LEFT" % (TAG, K, ok, base))
print("WORKER_DONE %s %d" % (TAG, K))
