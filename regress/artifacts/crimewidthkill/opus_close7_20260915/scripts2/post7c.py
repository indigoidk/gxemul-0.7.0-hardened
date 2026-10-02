#!/usr/bin/env python3
"""post7c.py BIN LABEL -- #529 closing pass 7, Opus FINISHING seat.  THIRD shape for the TIME 4-byte post-latch row,
after post7's magnitude oracle was measured VACUOUS and post7b's two shapes failed in opposite ways.

post7   POST prefix + ld; 4-byte; ld, magnitude threshold  -> base 0x10d49672, E2 0x86c913c: both LARGE, VACUOUS.
post7b  one run of [lb, ld, 4-byte, ld]
          FREE  -> base 0x84/0x42, E2 0x0/0x0, but K1 (a control) 0x0 once: FLAKY, a false red.
          STEP  -> base 0xfba, E2 0x8c4: both a nonzero multiple of 66, NON-DISCRIMINATING.

THIS SHAPE: fuse the refusal and the first TIME read into the session's FIRST `step 2', so d->last_microseconds is
initialised while TIME is still ~0; then issue the 4-byte access and the final read as SEPARATE `step 1' commands, so
the debugger's own ~0.25 s gap makes the 4-byte access's update huge and nothing else's.  On the fix the final ld
reads ~66 x 250000; under a TIME 4-byte bypass it reads only what the two steps' own ticks added.

Sentinel: POST7C_DONE (plus POST7C_RESULT=n/N).
"""
import os, pty, re, select, signal, sys, time

BIN = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"
DUMMY = "/tmp/dummy_crimep.bin"
if not os.path.exists(DUMMY):
    with open(DUMMY, "wb") as f:
        f.write(b"\0" * 16)

CODE = 0x80001000
CRIME = 0xb4000000
SENT = 0xdeadbeef
SMALL = 66 * 100000
R = {"zero": 0, "at": 1, "v0": 2, "v1": 3, "a0": 4, "a1": 5, "a2": 6, "a3": 7, "t0": 8, "t1": 9,
     "s0": 16, "s1": 17, "s2": 18, "s3": 19, "ra": 31}
OPC = {"lb": 0x20, "lh": 0x21, "lw": 0x23, "lbu": 0x24, "lhu": 0x25, "ld": 0x37,
       "sb": 0x28, "sh": 0x29, "sw": 0x2b, "sd": 0x3f}
OP_B_SELF = 0x1000ffff
OP_NOP = 0

rows = []


def enc(op, rs, rt, imm=0):
    return (OPC[op] << 26) | (R[rs] << 21) | (R[rt] << 16) | (imm & 0xffff)


assert enc("lb", "at", "v0") == 0x80220000 and enc("sw", "a3", "t0") == 0xace80000


def row(name, got, want, note=""):
    rows.append((name, got == want))
    print("%-16s %-22s %-22s %-40s %s" % (name, str(got), str(want), note, "ok" if got == want else "FAIL"))
    sys.stdout.flush()


def session(cmds, settle=1.5, spin=1.2):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "sgi", "-e", "ip32", "-M", "64", "0x80001000:" + DUMMY])
        os._exit(127)
    buf = ""

    def rd(t):
        nonlocal buf
        end = time.time() + t
        while time.time() < end:
            r, _, _ = select.select([fd], [], [], 0.1)
            if not r:
                continue
            try:
                d = os.read(fd, 65536)
            except OSError:
                return False
            if not d:
                return False
            buf += d.decode("latin-1", "replace")
        return True

    rd(settle)
    for i, c in enumerate(cmds):
        try:
            os.write(fd, (c + "\n").encode("latin-1"))
            ok = rd(spin if i == len(cmds) - 1 else 0.25)
        except OSError:
            break
        if not ok:
            break
    eof = True
    try:
        os.write(fd, b"quit\n")
        eof = not rd(10.0)
    except OSError:
        pass
    if not eof:
        try:
            os.kill(pid, signal.SIGKILL)
        except OSError:
            pass
    try:
        os.close(fd)
    except OSError:
        pass
    how = "nostatus"
    try:
        _, stat = os.waitpid(pid, 0)
        how = ("sig%d" % os.WTERMSIG(stat)) if os.WIFSIGNALED(stat) else ("exit%d" % os.WEXITSTATUS(stat))
    except OSError:
        pass
    return buf.replace("\r", ""), (eof and how == "exit0")


def nth(t, reg, n):
    ms = re.findall(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
    return int(ms[n], 16) if len(ms) > n else None


def mag(v):
    return "absent" if v is None else ("small" if v < SMALL else "large")


print("POST7C (third shape for the TIME 4-byte post-latch row) binary=%s label=%s" % (BIN, LABEL))
print("%-16s %-22s %-22s %-40s %s" % ("row", "got", "want", "note", ""))

notices = []


def gapped(kind):
    ops = [enc("lb", "a3", "t1"),                                            # 0: REFUSED lb +0x07 -- sets the latch
           enc("ld", "at", "v1"),                                            # 1: TIME 8R, TIME still ~0
           enc("sw", "at", "t0") if kind == "w" else enc("lw", "at", "a0"),  # 2: the TIME 4-byte cell under test
           enc("ld", "at", "v0")]                                            # 3: what it left behind
    at = CODE
    c = ["at=0x%x" % (CRIME + 0x38), "a3=0x%x" % (CRIME + 0x07), "t0=0x0a0b0c0d",
         "v0=0x%x" % SENT, "v1=0x%x" % SENT, "a0=0x%x" % SENT, "t1=0x%x" % SENT]
    for i, op in enumerate(ops):
        c.append("put w 0x%x, 0x%08x" % (at + 4 * i, op))
    c += ["put w 0x%x, 0x%08x" % (at + 4 * len(ops), OP_B_SELF),
          "put w 0x%x, 0x%08x" % (at + 4 * len(ops) + 4, OP_NOP), "pc=0x%x" % at]
    c += ["step 2", "step 1", "step 1", "print v0", "print v1"]
    t, clean = session(c)
    notices.append(t.count("-- declined.") if clean else "unclean")
    return nth(t, "v0", 0), nth(t, "v1", 0)


for kind in ("w", "r"):
    v0, v1 = gapped(kind)
    row("p t4%s gap" % kind, mag(v0), "large",
        "step2[lb,ld] step1[%s] step1[ld] (raw %s, first ld %s)"
        % ("sw" if kind == "w" else "lw", None if v0 is None else hex(v0), None if v1 is None else hex(v1)))

row("p t gap once", notices, [1, 1], "CONTROL: each session announced its one refusal")

npass = sum(1 for _, ok in rows if ok)
print("")
print("FAILING: " + ", ".join(n for n, ok in rows if not ok))
print("POST7C_RESULT=%d/%d" % (npass, len(rows)))
print("POST7C_DONE")
