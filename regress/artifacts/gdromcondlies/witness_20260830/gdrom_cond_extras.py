#!/usr/bin/env python3
#
#  gdromcondlies -- (1) the RAW OBSERVABLE of each kill, quoted rather than summarised, and
#  (2) two ADJACENT measurements taken while verifying the witness.  Kept OUT of the witness
#  file so that file stays exactly what it claims to be.
#
#  The adjacent pair are both UNLATCHED guest-drivable fatal() sites in the SAME device,
#  each one line away from a kill site this round is about to touch:
#
#      :1089  case GDROM_UNKNOWN_0x88, the MEM_READ arm -- fatal(), `// exit(1);`
#      :1104  case GDROM_STAT,         the write arm    -- fatal(), `/* exit(1); */`
#
#  Both were de-fatalised by COMMENTING OUT the exit and leaving the fatal() unlatched.
#  The carrier's house idiom is N = 1 per device instance plus an explicit suppression
#  marker, and fatal() cannot be silenced by -q.  Whether these flood is a MEASUREMENT,
#  not a reading, so it is measured here.
#
#  Sentinel: GDROMCOND_EXTRAS_DONE

import os, pty, re, select, sys, time

BIN = sys.argv[1]
KERNEL = sys.argv[2]

CODE = 0x8c001000
GDROM_UNK88 = 0xa05f7088
GDROM_STAT = 0xa05f708c
BRA_SELF = 0xaffe
NOP = 0x0009


def session(cmds, settle=8.0, spin=3.0):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "dreamcast", "-M", "64", KERNEL])
        os._exit(127)
    buf = ""

    def rd(t):
        nonlocal buf
        end = time.time() + t
        while time.time() < end:
            r, _, _ = select.select([fd], [], [], 0.25)
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

    alive = rd(settle)
    for i, c in enumerate(cmds):
        try:
            os.write(fd, (c + "\n").encode("latin-1"))
        except OSError:
            alive = False
            break
        if not rd(spin if i == len(cmds) - 1 else 0.35):
            alive = False
            break
    try:
        os.write(fd, b"quit\n")
        rd(0.6)
    except OSError:
        pass
    try:
        os.close(fd)
    except OSError:
        pass
    how = "nostatus"
    try:
        _, stat = os.waitpid(pid, 0)
        if os.WIFSIGNALED(stat):
            how = "sig%d" % os.WTERMSIG(stat)
        elif os.WIFEXITED(stat):
            how = "exit%d" % os.WEXITSTATUS(stat)
    except OSError:
        pass
    return buf, alive, how


class Addr(object):
    def __init__(self, base):
        self.a = base

    def take(self, n):
        g = self.a
        self.a += 2 * (n + 2) + 0x20
        return g


def run(ops, at):
    put = ["put h 0x%x, 0x%04x" % (at + 2 * i, op) for i, op in enumerate(ops)]
    put += ["put h 0x%x, 0x%04x" % (at + 2 * len(ops), BRA_SELF),
            "put h 0x%x, 0x%04x" % (at + 2 * len(ops) + 2, NOP)]
    return put + ["pc=0x%x" % at, "step %d" % len(ops)]


def store16(reg, val, A):
    return ["r7=0x%x" % reg, "r8=0x%04x" % val] + run([0x2001 | (7 << 8) | (8 << 4)],
                                                      A.take(1))


def load16(reg, A, dest=2):
    return ["r1=0x%x" % reg, "r%d=0" % dest] \
        + run([0x6001 | (dest << 8) | (1 << 4)], A.take(1)) + ["print r%d" % dest]


def tailquote(t, n=14):
    lines = [l.rstrip("\r") for l in t.split("\n") if l.strip()]
    return lines[-n:]


print("== RAW OBSERVABLE: Site A, one guest store of 0x0000 to GDROM_UNKNOWN_0x88 ==")
A = Addr(CODE)
t, alive, how = session(store16(GDROM_UNK88, 0x0000, A))
for l in tailquote(t):
    print("   | " + l)
print("   how=%s alive=%s" % (how, alive))
print("")

print("== RAW OBSERVABLE: Site B, one guest store of 0x0055 to GDROM_COND ==")
A = Addr(CODE)
t, alive, how = session(store16(0xa05f709c, 0x0055, A))
for l in tailquote(t):
    print("   | " + l)
print("   how=%s alive=%s" % (how, alive))
print("")

print("== ADJACENT 1: three guest READS of GDROM_UNKNOWN_0x88 (:1089, fatal, exit commented) ==")
A = Addr(CODE)
cmds = load16(GDROM_UNK88, A) + load16(GDROM_UNK88, A) + load16(GDROM_UNK88, A)
t, alive, how = session(cmds)
n = t.count("Read from GDROM_UNKNOWN_0x88?")
print("   occurrences of the diagnostic = %d   (3 = UNLATCHED, floods)" % n)
print("   how=%s alive=%s" % (how, alive))
print("")

print("== ADJACENT 2: three guest WRITES to GDROM_STAT (:1104, fatal, exit commented) ==")
A = Addr(CODE)
cmds = store16(GDROM_STAT, 0x0001, A) + store16(GDROM_STAT, 0x0002, A) \
    + store16(GDROM_STAT, 0x0003, A)
t, alive, how = session(cmds)
n = t.count("[ Write to GDROM_STAT? ]")
print("   occurrences of the diagnostic = %d   (3 = UNLATCHED, floods)" % n)
print("   how=%s alive=%s" % (how, alive))
print("")

print("GDROMCOND_EXTRAS_DONE")
