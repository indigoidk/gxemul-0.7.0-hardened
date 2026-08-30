#!/usr/bin/env python3
#
#  gdromcondlies -- THE RUNG-3 WITNESS, BUILT BEFORE ANY FIX EXISTS.
#
#  Two guest-reachable host kills survive in src/devices/dev_dreamcast_gdrom.c at HEAD
#  8404520.  Both are the #443 BADVAL class: a KNOWN register rejecting a VALUE by ending
#  the host process.
#
#      Site A   case GDROM_UNKNOWN_0x88   `if (idata != 0xb) { fatal(...); exit(1); }`
#      Site B   case GDROM_COND, else arm `fatal("... unimplemented GDROM_COND = 0x%02x");
#                                           exit(1);`
#
#  ONE GUEST STORE EACH.  Nothing is staged, no packet is assembled, no command dispatches.
#
#  *** WHAT MAKES THIS A RUNG-3 WITNESS AND NOT A HARNESS. ***  Every row below drives a
#  REAL SH4 INSTRUCTION (`mov.w Rm, @Rn`), planted into guest RAM and executed by the CPU,
#  through REAL address decode and REAL memory_rw, on an UNMODIFIED in-tree machine
#  description -- `-E dreamcast`, whose own machine_dreamcast.c does the `device_add`.
#  No device_add of mine, no machine edit, no #include of the device.  Removing the machine
#  description and the dispatch would leave nothing that compiles, which is rung 1's
#  mechanical discriminator applied in the negative.
#
#  *** BOTH MANDATORY CONTROLS ARE PRESENT, AND ONE WOULD NOT BE ENOUGH. ***  This tree has
#  already shipped a probe that returned 0x0 everywhere WITH ITS RAM CONTROL GREEN, so:
#
#    LIVENESS         `live`        a guest store then a guest load, through RAM.  Proves
#                                   instructions execute and the decode routes.
#    DEVICE-SIGNATURE `devsig st`   GDROM_STAT reads 6 on a fresh device.  dreamcast_gdrom_
#                                   update_stat() sets d->stat = 6 and only lowers it to 0
#                                   when diskimage_exist(..., DISKIMAGE_IDE); no IDE image is
#                                   attached here.  **RAM WOULD READ 0.**  No guest store
#                                   precedes it, so the value is the model's, not an echo.
#    DEVICE-SIGNATURE `devsig cnt`  a TRANSFORMATION only the device performs: the write arm
#                                   is `d->cnt = (d->cnt & 0xff00) | (idata & 0xff)`, so a
#                                   16-bit store of 0x1234 to CNTLO reads back as 0x34.
#                                   **RAM WOULD RETURN 0x1234 VERBATIM.**  This is the
#                                   stronger of the two signatures because it discriminates
#                                   against a RAM-backed window as well as against a dead
#                                   one, and it sits in the SAME REGISTER FILE as both kills.
#    (cross-check)    `devsig sh4`  SH4 IPRD reset value 0xda74, copied verbatim from
#                                   gdrom_decline_probe.py so this probe's apparatus is
#                                   comparable with its siblings' rather than novel.
#
#  *** AND AN ATTRIBUTION CONTROL PER SITE, which is the "did it fail for the reason under
#  test?" rule made mechanical. ***  A row that only reads `how` cannot tell THIS kill from
#  any other way the emulator might die.  So every kill row is paired with the site's own
#  diagnostic text, and Site B's row additionally checks that the ECHOED BYTE TRACKS THE
#  GUEST DATUM (0x55 -> "= 0x55", 0x01 -> "= 0x01") -- which proves the guest's own value
#  reached the predicate, not merely that something in that function died.
#
#  *** AND AN ACCEPT CONTROL PER SITE, which is what makes this a BADVAL witness rather than
#  an "any access here dies" witness. ***  Site A survives 0xb; Site B survives 0xa0 and
#  0xef.  Without these rows the measurement would be equally consistent with the whole
#  offset being unserviceable -- which is the #461 default-arm defect, a DIFFERENT and
#  already-fixed one.  The accept rows are what pin the defect to the VALUE.
#
#  *** WHY `how` AND NEVER `alive`. ***  Spelling copied verbatim from
#  gdrom_decline_probe.py / gdrom_toclen_probe.py, because three gdrom probes must not
#  disagree about what "died" means.  `alive` is False for a HUNG emulator too; `how` comes
#  from waitpid and separates exit1 (this defect) from exit0 (survived) from sigN (a crash
#  that is NOT this defect).
#
#  NOT A DETECTOR.  It ships no gate section and claims no vacuity floor: it exists to show
#  the SYMPTOM ON THE COMMITTED BUILD before an edit, which is test-first itself.  The
#  round's detector is a later deliverable and is not this file.
#
#  Sentinel: GDROMCOND_WITNESS_DONE

import os, pty, re, select, sys, time

if len(sys.argv) < 3:
    sys.stderr.write("usage: gdrom_cond_witness.py <gxemul> <kernel>\n")
    sys.exit(2)

BIN = sys.argv[1]
KERNEL = sys.argv[2]

CODE = 0x8c001000
SCRATCH = 0x8c001800

#  0x005f7000 + offset, through the P2 uncached window.  The device registers itself at
#  0x005f7000 for 0x100 bytes in DEVINIT(dreamcast_gdrom); the offsets are the file's own
#  #defines.
GDROM_BUSY = 0xa05f7018
GDROM_DATA = 0xa05f7080
GDROM_UNK88 = 0xa05f7088        # Site A
GDROM_STAT = 0xa05f708c
GDROM_CNTLO = 0xa05f7090
GDROM_CNTHI = 0xa05f7094
GDROM_COND = 0xa05f709c         # Site B

IPRD_RESET = 0xda74
LIVE = 0x12345678
BRA_SELF = 0xaffe
NOP = 0x0009

#  Site A's text contains [ and ], which are regex metacharacters -- counted as a PLAIN
#  SUBSTRING so no escaping question can arise.
A88_TEXT = "[ Write to GDROM_UNKNOWN_0x88: TODO ]"
#  Site B's text, with the echoed byte left as a capture so a row can check it TRACKS the
#  guest's datum rather than merely existing.
COND_TEXT = re.compile(r"dreamcast_gdrom: unimplemented GDROM_COND = 0x([0-9a-f]{2})")

rows = []


def row(name, got, want, note=""):
    ok = (got == want)
    rows.append((name, ok))
    print("%-14s %-12s %-12s %-46s %s" % (name, got, want, note,
                                          "ok" if ok else "FAIL"))
    return ok


def session(cmds, settle=8.0, spin=3.0):
    """Run one gxemul, feed debugger commands, return (transcript, alive, how)."""
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


def printed(t, reg):
    m = re.search(r"print\s+%s\s*\r?\n\s*(0x[0-9a-f]+)" % reg, t)
    return m.group(1) if m else "absent"


def MOVW_ST(n, m):
    return 0x2001 | (n << 8) | (m << 4)     # mov.w Rm, @Rn


def MOVW_LD(n, m):
    return 0x6001 | (n << 8) | (m << 4)     # mov.w @Rm, Rn


def MOVL_ST(n, m):
    return 0x2002 | (n << 8) | (m << 4)     # mov.l Rm, @Rn


class Addr(object):
    """Hands out non-overlapping code addresses so planted runs cannot collide."""

    def __init__(self, base):
        self.a = base

    def take(self, n_ops):
        got = self.a
        self.a += 2 * (n_ops + 2) + 0x20
        return got


def run(ops, at):
    put = ["put h 0x%x, 0x%04x" % (at + 2 * i, op) for i, op in enumerate(ops)]
    put += ["put h 0x%x, 0x%04x" % (at + 2 * len(ops), BRA_SELF),
            "put h 0x%x, 0x%04x" % (at + 2 * len(ops) + 2, NOP)]
    return put + ["pc=0x%x" % at, "step %d" % len(ops)]


def store16(reg, val, A):
    return ["r7=0x%x" % reg, "r8=0x%04x" % val] + run([MOVW_ST(7, 8)], A.take(1))


#  operands as CORRECTED in gdrom_decline_probe.py: MOVW_LD(dest, 1) is `mov.w @R1, Rdest`.
#  Reversing them made three sibling rows pass vacuously, so this is copied, not re-derived.
def load16(reg, A, dest=2):
    return ["r1=0x%x" % reg, "r%d=0" % dest] + run([MOVW_LD(dest, 1)], A.take(1)) \
        + ["print r%d" % dest]


def load32(reg, A, dest=2):
    return ["r1=0x%x" % reg, "r%d=0" % dest] + run([0x6002 | (1 << 4) | (dest << 8)],
                                                   A.take(1)) + ["print r%d" % dest]


print("gdromcondlies WITNESS -- rung 3, on the COMMITTED build, BEFORE any fix.")
print("binary: %s" % BIN)
print("")
print("%-14s %-12s %-12s %-46s %s" % ("row", "got", "want", "note", ""))

# ------------------------------------------------------------------ MANDATORY CONTROLS
#  Emitted over the CONTROL ROWS ONLY.  Measured lesson from the sibling probe's first run:
#  a CONTROL line that also goes DEAD on a product failure sends a reader hunting a broken
#  rig for a real defect.

A = Addr(CODE)
t, alive, how = session(["r7=0x%x" % SCRATCH, "r8=0x%08x" % LIVE]
                        + run([MOVL_ST(7, 8)], A.take(1))
                        + ["r1=0x%x" % SCRATCH, "r2=0"]
                        + run([0x6002 | (1 << 4) | (2 << 8)], A.take(1)) + ["print r2"])
row("live", printed(t, "r2") if alive else "died", "0x%x" % LIVE,
    "LIVENESS: guest store then guest load, through RAM")

#  32-bit load and mask, NOT a 16-bit one -- SH4_IPRD does not serve a halfword access and
#  the row would fail OPEN.  Copied from the sibling probe, which had already solved it.
A = Addr(CODE)
t, alive, how = session(load32(0xffd00010, A))
g = printed(t, "r2")
row("devsig sh4", ("0x%x" % (int(g, 16) & 0xffff)) if g.startswith("0x") else g,
    "0x%x" % IPRD_RESET, "DEVSIG: SH4 IPRD reset value; RAM would read 0")

#  *** THE GDROM-LOCAL DEVICE SIGNATURE, at an IMPLEMENTED offset in the same register file
#  as both kill sites.  update_stat() sets d->stat = 6 unless an IDE diskimage exists; none
#  is attached, and no guest store precedes this read.  RAM would read 0. ***
A = Addr(CODE)
t, alive, how = session(load16(GDROM_STAT, A))
g = printed(t, "r2")
row("devsig st", g if alive else "died", "0x6",
    "DEVSIG: fresh GDROM_STAT = 6 (no IDE image); RAM = 0")

#  *** THE STRONGER SIGNATURE: A TRANSFORMATION.  The write arm masks to a byte, so a
#  16-bit store of 0x1234 reads back 0x34.  A RAM-backed window would return 0x1234. ***
A = Addr(CODE)
t, alive, how = session(store16(GDROM_CNTLO, 0x1234, A) + load16(GDROM_CNTLO, A))
g = printed(t, "r2")
row("devsig cnt", g if alive else "died", "0x34",
    "DEVSIG: device masks CNTLO to a byte; RAM would give 0x1234")

print("GDROMCOND_CONTROL=%s"
      % ("OK" if rows and all(ok for _, ok in rows) else "DEAD"))
print("")

# ------------------------------------------------------- SITE A: GDROM_UNKNOWN_0x88, != 0xb
#  observable: the DEATH MODE from waitpid, plus the site's own diagnostic for attribution.

A = Addr(CODE)
t, alive, how = session(store16(GDROM_UNK88, 0x0000, A))
row("a88 kill", how, "exit1",
    "ONE guest store of 0x0000 -- host process ends")
row("a88 says", "%d" % t.count(A88_TEXT), "1",
    "ATTRIBUTION: it died at THIS site, announcing once")

#  not only zero: the guard is `!= 0xb`, so an arbitrary byte kills too.
A = Addr(CODE)
t, alive, how = session(store16(GDROM_UNK88, 0x0055, A))
row("a88 alt", how, "exit1",
    "and a different bad value kills identically")

#  *** THE ACCEPT CONTROL.  Without it the measurement is equally consistent with the whole
#  offset being unserviceable, which is a DIFFERENT (and already-fixed) defect. ***
A = Addr(CODE)
t, alive, how = session(store16(GDROM_UNK88, 0x000b, A))
row("a88 ok", how, "exit0",
    "ACCEPT: the legal value 0xb survives -- so it is BADVAL")
row("a88 quiet", "%d" % t.count(A88_TEXT), "0",
    "and the legal value announces nothing")

# ------------------------------------------------------ SITE B: GDROM_COND, outside {a0,ef}

A = Addr(CODE)
t, alive, how = session(store16(GDROM_COND, 0x0055, A))
m = COND_TEXT.search(t)
row("cond kill", how, "exit1",
    "ONE guest store of 0x0055 -- host process ends")
row("cond says", m.group(1) if m else "absent", "55",
    "ATTRIBUTION: the guest's own byte reaches the fatal")

#  the echoed byte must TRACK the datum -- a constant would prove far less.
A = Addr(CODE)
t, alive, how = session(store16(GDROM_COND, 0x0001, A))
m = COND_TEXT.search(t)
row("cond echo", m.group(1) if m else "absent", "01",
    "and it tracks the value, so the predicate saw it")

#  *** THE TWO ACCEPT CONTROLS: the register is KNOWN and serves two command bytes. ***
A = Addr(CODE)
t, alive, how = session(store16(GDROM_COND, 0x00a0, A))
row("cond a0", how, "exit0",
    "ACCEPT: 0xa0 (start a command) survives")
row("cond quiet", "%d" % len(COND_TEXT.findall(t)), "0",
    "and announces nothing")

A = Addr(CODE)
t, alive, how = session(store16(GDROM_COND, 0x00ef, A))
row("cond ef", how, "exit0",
    "ACCEPT: 0xef (ROM) survives -- so it is BADVAL")

# ------------------------------------------------------------------------------ result
ok = sum(1 for _, o in rows if o)
print("")
print("GDROMCOND_WITNESS_RESULT=%d/%d" % (ok, len(rows)))
print("GDROMCOND_WITNESS_DONE")
