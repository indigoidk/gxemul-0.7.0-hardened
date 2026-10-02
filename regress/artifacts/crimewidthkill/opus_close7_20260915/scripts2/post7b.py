#!/usr/bin/env python3
"""post7b.py BIN LABEL -- #529 closing pass 7, Opus FINISHING seat.  The REPAIR of post7.py's two vacuous TIME rows.

post7.py rowed the TIME 4-byte cells POST (after one refused lb +0x07) with a magnitude oracle and E2_byp_time4
scored 29/29: base read 0x10d49672 and E2 0x86c913c -- a factor of exactly 2, far above the 66 x 100000 threshold in
both cases.  The POST prefix's own `step' runs the CPU, dev_crime_tick fires and sets d->last_microseconds, and after
that every accepted TIME access only CATCHES UP, so skipping one halves the total instead of zeroing it.

THE CORRECTED SHAPE: the refusal AND the three TIME accesses in ONE run, as the session's FIRST CPU EXECUTION.  Then
d->last_microseconds is 0 at the first TIME arm (delta 0, no add, TIME stays 0) and the 4-byte access is the ONLY
thing that can move TIME before the final read.  Want: a NONZERO MULTIPLE OF 66 (disc7 measured base 0xc6 = 3x66,
0x108 = 4x66; E2 exactly 0x0, 12 of 12 over two scripts).  Both a FREE-RUNNING and a STEPPED variant are measured
because I cannot tell by reading whether four instructions inside one `step 4' fall in one microsecond, which would
leave base at 0 too and make the stepped form unusable.

Sentinel: POST7B_DONE (plus POST7B_RESULT=n/N).
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
            if c == "<RUN>":
                os.write(fd, b"continue\n")
                ok = rd(2.0)
                os.write(fd, b"\x03")
                ok = ok and rd(1.5)
            else:
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


def mult66(v):
    return "absent" if v is None else ("mult66" if (v != 0 and v % 66 == 0) else ("zero" if v == 0 else "other"))


print("POST7B (repair of post7's TIME rows) binary=%s label=%s" % (BIN, LABEL))
print("%-16s %-22s %-22s %-40s %s" % ("row", "got", "want", "note", ""))

SD = (OPC["sd"] << 26) | (R["at"] << 21) | (R["t0"] << 16)
notices = []


def one(kind, run):
    """the refused lb and the three TIME accesses in ONE run, the session's FIRST CPU execution."""
    ops = [enc("lb", "a3", "t1"),                               # REFUSED lb +0x07: sets d->warned & CRIME_W_LEN
           enc("ld", "at", "v1"),                               # TIME 8R: initialises last_microseconds, TIME stays 0
           enc("sw", "at", "t0") if kind == "w" else enc("lw", "at", "a0"),    # the TIME 4-byte cell under test
           enc("ld", "at", "v0")]                               # TIME 8R: what the 4-byte access left behind
    at = CODE
    c = ["at=0x%x" % (CRIME + 0x38), "a3=0x%x" % (CRIME + 0x07), "t0=0x0a0b0c0d",
         "v0=0x%x" % SENT, "v1=0x%x" % SENT, "a0=0x%x" % SENT, "t1=0x%x" % SENT]
    for i, op in enumerate(ops):
        c.append("put w 0x%x, 0x%08x" % (at + 4 * i, op))
    c += ["put w 0x%x, 0x%08x" % (at + 4 * len(ops), OP_B_SELF),
          "put w 0x%x, 0x%08x" % (at + 4 * len(ops) + 4, OP_NOP), "pc=0x%x" % at]
    c += ["<RUN>"] if run else ["step %d" % len(ops)]
    c += ["print v0", "print v1"]
    t, clean = session(c)
    notices.append(t.count("-- declined.") if clean else "unclean")
    return nth(t, "v0", 0)


for run, tag in ((True, "free"), (False, "step")):
    for kind in ("w", "r"):
        v = one(kind, run)
        row("p t4%s %s" % (kind, tag), mult66(v),
            "mult66", "one run: lb +0x07, ld, %s +0x38, ld (raw %s)"
            % ("sw" if kind == "w" else "lw", None if v is None else hex(v)))

row("p t post once", notices, [1, 1, 1, 1], "CONTROL: each session announced its one refusal")

npass = sum(1 for _, ok in rows if ok)
print("")
print("FAILING: " + ", ".join(n for n, ok in rows if not ok))
print("POST7B_RESULT=%d/%d" % (npass, len(rows)))
print("POST7B_DONE")
