#!/usr/bin/env python3
"""
crime_width_witness_20260913.py -- RUNG-3 WITNESS for `crimewidthkill' on UNMODIFIED `-E sgi -e ip32'.

src/devices/dev_sgi_ip32.c, DEVICE_ACCESS(crime): an access whose length is neither 8 nor 4 falls to

        } else {
                fatal("crime access len = %i!\n", len);
                exit(1);
        }

so one guest byte or halfword load or store to the IP32 CRIME (physical 0x14000000, KSEG1 0xb4000000) ends the
emulator.  This witness drives a real MIPS guest instruction through real address decode and memory_rw on the
unmodified machine, and asks only what EVERY candidate fix must change: does the HOST PROCESS SURVIVE the access?
It does not assert what the guest sees (a value, a declined 0, a bus error) -- that is the fix design's question.

Each width row runs the access in its OWN session, then a RAM round trip through the same apparatus: if the host
died at the access the round trip never prints; if it survived (whatever the guest saw -- a bus error vectors the
PC away, but the round trip sets its own PC) it prints the stored value.  `<op> says' counts whether the kill's own
text appeared -- the attribution control that the death, if any, is THIS kill.

CONTROLS: `live' (a RAM round trip), `devsig' (a 4-byte read of CRIME_REV's low half at 0xb4000004 returns the
model's revision 0x11 -- RAM would not), `devsig hi' (its high half at 0xb4000000 reads 0).  Committed build:
controls green, every `<op> surv' row RED with `<op> says' present.  A fixed build: every row green.

Sentinel: CRIMEW_DONE (plus CRIMEW_RESULT=n/N and CRIMEW_CONTROL=OK|FAIL).
"""
import os, pty, re, select, sys, time

BIN = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"
DUMMY = "/tmp/dummy_crimew.bin"
if not os.path.exists(DUMMY):
    with open(DUMMY, "wb") as f:
        f.write(b"\0" * 16)

CODE = 0x80001000
SCRATCH_RAM = 0xa0001800
LIVE_VAL = 0x12345678
CRIME = 0xb4000000
SENTINEL = 0xdeadbeef

OP_NOP = 0x00000000
OP_B_SELF = 0x1000ffff
OP_SW_T0_A3 = 0xace80000          # sw   $t0, 0($a3)
OP_SH_T0_A3 = 0xa4e80000          # sh   $t0, 0($a3)
OP_SB_T0_A3 = 0xa0e80000          # sb   $t0, 0($a3)
OP_LW_V0_AT = 0x8c220000          # lw   $v0, 0($at)
OP_LH_V0_AT = 0x84220000          # lh   $v0, 0($at)
OP_LHU_V0_AT = 0x94220000         # lhu  $v0, 0($at)
OP_LB_V0_AT = 0x80220000          # lb   $v0, 0($at)
OP_LBU_V0_AT = 0x90220000         # lbu  $v0, 0($at)

rows = []


def row(name, got, want, note=""):
    ok = (got == want)
    rows.append((name, ok))
    print("%-16s %-12s %-12s %-46s %s" % (name, str(got), str(want), note, "ok" if ok else "FAIL"))
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
                if not d:
                    return False
                buf += d.decode("latin-1", "replace")
            except OSError:
                return False
        return True

    rd(settle)
    for i, c in enumerate(cmds):
        try:
            os.write(fd, (c + "\n").encode("latin-1"))
        except OSError:
            break
        if not rd(spin if i == len(cmds) - 1 else 0.25):
            break
    try:
        os.write(fd, b"quit\n")
        rd(2.0)
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
    return buf.replace("\r", ""), how


def printed(t, reg):
    m = re.search(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
    return ("0x%x" % int(m.group(1), 16)) if m else "absent"


class Addr(object):
    def __init__(self, base):
        self.a = base

    def take(self, n):
        got = self.a
        self.a += 4 * (n + 2) + 0x20
        return got


def run_ops(ops, at):
    put = ["put w 0x%x, 0x%08x" % (at + 4 * i, op) for i, op in enumerate(ops)]
    put += ["put w 0x%x, 0x%08x" % (at + 4 * len(ops), OP_B_SELF),
            "put w 0x%x, 0x%08x" % (at + 4 * len(ops) + 4, OP_NOP)]
    return put + ["pc=0x%x" % at, "step %d" % len(ops)]


def store(A, addr, op=OP_SW_T0_A3, val=LIVE_VAL):
    return ["a3=0x%x" % addr, "t0=0x%x" % val] + run_ops([op], A.take(1))


def load(A, addr, op=OP_LW_V0_AT):
    return ["at=0x%x" % addr, "v0=0x%x" % SENTINEL] + run_ops([op], A.take(1))


def roundtrip(A):
    """a RAM round trip, printed in v1 so it cannot be confused with the access's own destination"""
    return (store(A, SCRATCH_RAM) + ["at=0x%x" % SCRATCH_RAM, "v1=0x%x" % SENTINEL]
            + run_ops([0x8c230000], A.take(1)) + ["print v1"])          # lw $v1, 0($at)


print("CRIME WIDTH WITNESS -- rung 3, unmodified -E sgi -e ip32   binary=%s  label=%s" % (BIN, LABEL))
print("%-16s %-12s %-12s %-46s %s" % ("row", "got", "want", "note", ""))

A = Addr(CODE)
t, how = session(roundtrip(A))
row("live", printed(t, "v1"), "0x%x" % LIVE_VAL, "LIVENESS: RAM round trip, same apparatus")
A = Addr(CODE)
t, how = session(load(A, CRIME + 4) + ["print v0"])
row("devsig", printed(t, "v0"), "0x11", "CRIME_REV low half (no framebuffer): a device")
A = Addr(CODE)
t, how = session(load(A, CRIME) + ["print v0"])
row("devsig hi", printed(t, "v0"), "0x0", "CRIME_REV high half reads 0")

WIDTH = (("lb", load, OP_LB_V0_AT, CRIME + 7), ("lbu", load, OP_LBU_V0_AT, CRIME + 7),
         ("lh", load, OP_LH_V0_AT, CRIME + 6), ("lhu", load, OP_LHU_V0_AT, CRIME + 6),
         ("sb", store, OP_SB_T0_A3, CRIME + 0x1f), ("sh", store, OP_SH_T0_A3, CRIME + 0x1e))
for name, fn, op, addr in WIDTH:
    A = Addr(CODE)
    t, how = session(fn(A, addr, op) + roundtrip(A))
    row("%s surv" % name, printed(t, "v1"), "0x%x" % LIVE_VAL, "host survives a %s to CRIME, then a RAM trip" % name)
    row("%s says" % name, "yes" if "crime access len" in t else "no", "no",
        "the kill's own text absent (%s)" % how)

npass = sum(1 for _, ok in rows if ok)
st = dict(rows)
control = all(st.get(n, False) for n in ("live", "devsig", "devsig hi"))
print("")
print("FAILING: " + ", ".join(n for n, ok in rows if not ok))
print("CRIMEW_RESULT=%d/%d" % (npass, len(rows)))
print("CRIMEW_CONTROL=%s" % ("OK" if control else "FAIL"))
print("CRIMEW_DONE")
