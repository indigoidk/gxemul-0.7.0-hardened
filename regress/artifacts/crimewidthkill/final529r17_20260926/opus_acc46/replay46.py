#!/usr/bin/env python3
"""replay46.py -- session-replay driver for the Opus seat's ACCEPTS enumeration (#529, probe r17).

  replay46.py capture PROBE BIN CACHE LABEL
        Run PROBE in full on BIN with ACC46 UNSET; pickle every session's (cmds, transcript, clean) to CACHE.
  replay46.py replay  PROBE BIN CACHE LABEL SPEC
        Run PROBE on BIN with ACC46=SPEC -- but only the sessions holding at least one access SPEC matches IN ITS
        LATCH STATE (static decode of the session's own command list); every other session is served its CAPTURED
        transcript, on which the binary is inert by construction (nothing in it matches).
  replay46.py plan    PROBE SPEC...
        Print, per spec, the sessions a replay would re-run and their predicted match counts (no emulator).

SPEC is mut46.py's grammar: LEN:DIR:OFF:WIN:VAL:LATCH, `*' = any.  The replay prints the probe's own rows and
CRIMEP_* lines, then REPLAY46 lines: every re-run session with its predicted match count and the observed number of
`[ACC46HIT' markers (the mutant's own evidence that it fired, where, and in which latch state).
Sentinel: REPLAY46_DONE."""
import os, pickle, re, sys

MODE, PROBE = sys.argv[1], sys.argv[2]

OPC = {0x20: ("lb", 1, "R"), 0x21: ("lh", 2, "R"), 0x23: ("lw", 4, "R"), 0x24: ("lbu", 1, "R"),
       0x25: ("lhu", 2, "R"), 0x37: ("ld", 8, "R"), 0x28: ("sb", 1, "W"), 0x29: ("sh", 2, "W"),
       0x2b: ("sw", 4, "W"), 0x3f: ("sd", 8, "W")}
RNUM = {"zero": 0, "at": 1, "v0": 2, "v1": 3, "a0": 4, "a1": 5, "a2": 6, "a3": 7, "t0": 8, "t1": 9,
        "s0": 16, "s1": 17, "s2": 18, "s3": 19, "s4": 20, "ra": 31}
CRIME = 0xb4000000


def decode(cmds):
    """the CRIME accesses a session's command list executes, in order, each with its latch state"""
    regs, mem, acc, pc, latch = {}, {}, [], None, False
    for c in cmds:
        m = re.match(r"^([a-z0-9]+)=0x([0-9a-f]+)$", c)
        if m:
            if m.group(1) == "pc":
                pc = int(m.group(2), 16)
            else:
                regs[RNUM[m.group(1)]] = int(m.group(2), 16)
            continue
        m = re.match(r"^put w 0x([0-9a-f]+), 0x([0-9a-f]{8})$", c)
        if m:
            mem[int(m.group(1), 16)] = int(m.group(2), 16)
            continue
        m = re.match(r"^step (\d+)$", c)
        if m or c == "<RUN>":
            n = int(m.group(1)) if m else 10 ** 6
            while n > 0 and pc in mem:
                w = mem[pc]
                if w == 0x1000ffff:
                    break
                op, rs, rt = w >> 26, (w >> 21) & 0x1f, (w >> 16) & 0x1f
                if op in OPC:
                    name, ln, d = OPC[op]
                    base = regs.get(rs)
                    if base is not None and CRIME <= base < CRIME + 0x280:
                        acc.append({"len": ln, "dir": d, "off": base - CRIME,
                                    "win": 1 if (pc & 0xffffff00) == 0xbfc05100 else 0,
                                    "val": regs.get(rt) if d == "W" else None, "latch": "S" if latch else "C"})
                        if ln in (1, 2):
                            latch = True
                    if d == "R":
                        regs.pop(rt, None)
                pc += 4
                n -= 1
    return acc


def parse(spec):
    out = []
    for s in spec.split(";"):
        f = s.split(":")
        assert len(f) == 6, s
        out.append(f)
    return out


def matches(a, specs):
    n = 0
    for ln, d, off, win, val, lt in specs:
        if a["len"] != int(ln) or a["dir"] != d or a["off"] != int(off, 16):
            continue
        if win != "*" and a["win"] != int(win):
            continue
        if val != "*" and (a["dir"] != "W" or a["val"] != int(val, 16)):
            continue
        if lt != "*" and a["latch"] != lt:
            continue
        n += 1
        break
    return n


def load_probe():
    src = open(PROBE, encoding="utf-8").read()
    n = src.count("t, clean = session(")
    src = src.replace("t, clean = session(", "t, clean = _sess(")
    code = [l for l in src.split("\n") if not l.lstrip().startswith("#")]
    left = [l for l in code if re.search(r"(?<![a-z_])session\(", l) and "def session(" not in l]
    assert not left, left[:3]
    return src, n


if MODE == "plan":
    src, n = load_probe()
    SESS = []

    def _sess(cmds, settle=1.5, spin=1.2):
        SESS.append(list(cmds))
        return "", True
    g = {"__name__": "__main__", "_sess": _sess}
    plan_specs = sys.argv[3:]
    sys.argv = [PROBE, "/nonexistent", "plan"]
    import io, contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        try:
            exec(compile(src, PROBE, "exec"), g)
        except SystemExit:
            pass
    for spec in plan_specs:
        if not spec:
            continue
        sp = parse(spec)
        tot = 0
        parts = []
        for i, cmds in enumerate(SESS):
            k = sum(matches(a, sp) for a in decode(cmds))
            if k:
                parts.append("S%d:%d" % (i, k))
                tot += len(cmds)
        print("PLAN %s  sessions=%s  cmds=%d" % (spec, ",".join(parts), tot))
    print("PLAN_SESSIONS=%d" % len(SESS))
    sys.exit(0)

BIN, CACHE, LABEL = sys.argv[3], sys.argv[4], sys.argv[5]
SPEC = sys.argv[6] if MODE == "replay" else None
specs = parse(SPEC) if SPEC else []
src, nsess = load_probe()
cache = pickle.load(open(CACHE, "rb")) if MODE == "replay" else []
#  REPLAY_FROMCACHE=38,52: sessions served from the capture EVEN WHEN THE SPEC MATCHES IN THEM -- declared, and
#  printed as FROMCACHE below, so a reader never mistakes a derivation-served session for a measured one.
FROMCACHE = set(int(x) for x in os.environ.get("REPLAY_FROMCACHE", "").split(",") if x.strip())
log = []
g = {"__name__": "__main__"}
counter = [0]


def _sess(cmds, settle=1.5, spin=1.2):
    i = counter[0]
    counter[0] += 1
    real = g["session"]
    if MODE == "capture":
        os.environ.pop("ACC46", None)
        t, clean = real(cmds, settle, spin)
        cache.append((list(cmds), t, clean))
        return t, clean
    c0, t0, k0 = cache[i]
    assert c0 == list(cmds), "session %d: command list differs from the captured one" % i
    npred = sum(matches(a, specs) for a in decode(cmds))
    if npred and i in FROMCACHE:
        log.append((i, npred, -1, k0, -1))          # matched, but served from the capture BY DECLARATION
        return t0, k0
    if npred == 0:
        return t0, k0
    os.environ["ACC46"] = SPEC
    try:
        t, clean = real(cmds, settle, spin)
    finally:
        os.environ.pop("ACC46", None)
    log.append((i, npred, t.count("[ACC46HIT"), clean, t.count("[ACC46INIT n=%d]" % len(specs))))
    return t, clean


g["_sess"] = _sess
sys.argv = [PROBE, BIN, LABEL]
try:
    exec(compile(src, PROBE, "exec"), g)
except SystemExit:
    pass
sys.stdout.flush()
if MODE == "capture":
    pickle.dump(cache, open(CACHE, "wb"))
    print("REPLAY46 CAPTURED sessions=%d" % len(cache))
else:
    for i, npred, nhit, clean, ninit in log:
        if nhit < 0:
            print("REPLAY46 S%d predicted_matches=%d FROMCACHE (declared; not re-run)" % (i, npred))
            continue
        print("REPLAY46 S%d predicted_matches=%d observed_hits=%d init_ok=%d clean=%s %s"
              % (i, npred, nhit, ninit, clean, "OK" if (npred == nhit and ninit == 1) else "MISMATCH"))
    print("REPLAY46 SPEC=%s rerun=%d fromcache=%d" % (SPEC, sum(1 for x in log if x[2] >= 0),
                                                     sum(1 for x in log if x[2] < 0)))
print("REPLAY46_DONE")
