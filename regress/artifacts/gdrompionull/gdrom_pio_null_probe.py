#!/usr/bin/env python3
"""WITNESS for ledger row `gdrompionull`.

The PIO data read at src/devices/dev_dreamcast_gdrom.c:611-613 dereferences
d->data with no NULL test:

    if (d->cur_data_offset < d->data_len) {
            odata  =  d->data[d->cur_data_offset ++];
            odata |= (d->data[d->cur_data_offset ++] << 8);

`d->data_len` has exactly ONE writer, alloc_data() at :307.  handle_command()
frees d->data and NULLs it at :324-326 but never clears data_len, and its tail
at :475-480 clears COND_DATA_AVAIL and zeroes d->cnt -- not data_len.  So
data==NULL with data_len>0 is a reachable steady state, and one legal guest
store of 0xef to GDROM_COND (:720, `d->cond = idata` sits OUTSIDE both arms)
puts bit 3 back and re-opens the read.

Rung 3: every access below is a real guest instruction, executed through real
address decode and real memory_rw, on the UNMODIFIED committed `dreamcast`
machine description.  Nothing is device_add'ed and no machine is introduced.

ORACLE.  The defect is a NULL dereference, so it kills the host with SIGSEGV.
Every OTHER death in this device is fatal() + exit(1) -- status exit1.  The
probe therefore reports HOW the process ended, not merely that it ended:
  sig11  = the deref                    (the defect)
  exit1  = some guarded refusal          (a mis-built packet, NOT the defect)
  exit0  = survived and quit cleanly
That distinction is what makes "died" evidence here.  It also validates the
hand-assembled packet for free: a wrong cmd[0] lands in handle_command's
`default:` arm and a wrong cmd[1] in the 0x30 arm's format check -- both
exit(1) -- so a coding error CANNOT be mistaken for the defect.

CONTROLS run in their own sessions and never reach the NULL path.
DREAMCAST NEEDS -x (console.c:994-1007, two console inputs) or the session dies
for a CONFIGURATION reason and prints the same "died" the defect prints.
"""
import os
import pty
import re
import select
import sys
import time

BIN = sys.argv[1] if len(sys.argv) > 1 else "/tmp/gxpio/gxemul"
KERNEL = sys.argv[2] if len(sys.argv) > 2 else \
    "/mnt/c/DocumentNoSnc/CC/GXEMUL/_images/openbsd76-landisk-bsd.rd"
#  Anything after argv[2] is passed straight to the emulator -- used to attach a
#  real IDE disk, so the disk-dependence of each route can be MEASURED.
EXTRA = sys.argv[3:]

CODE = 0x8c001000
SCRATCH = 0x8c001800

GDROM_DATA = 0xa05f7080
GDROM_BUSY = 0xa05f7018
GDROM_CNTLO = 0xa05f7090
GDROM_CNTHI = 0xa05f7094
GDROM_COND = 0xa05f709c
SH4_IPRD = 0xffd00010
IPRD_RESET = 0xda74
LIVE = 0x12345678

BRA_SELF = 0xaffe
NOP = 0x0009


def MOVW_ST(n, m):      # mov.w Rm,@Rn      0010 nnnn mmmm 0001
    return 0x2001 | (n << 8) | (m << 4)


def MOVW_LD(n, m):      # mov.w @Rm,Rn      0110 nnnn mmmm 0001
    return 0x6001 | (n << 8) | (m << 4)


def MOVL_ST(n, m):      # mov.l Rm,@Rn      0010 nnnn mmmm 0010
    return 0x2002 | (n << 8) | (m << 4)


def MOVL_LD(n, m):      # mov.l @Rm,Rn      0110 nnnn mmmm 0010
    return 0x6002 | (n << 8) | (m << 4)


rows = []


def row(name, got, want, note=""):
    ok = (got == want)
    rows.append((name, ok))
    print("%-14s %-12s %-12s %-46s %s" % (name, got, want, note,
                                          "ok" if ok else "FAIL"))
    return ok


def session(cmds, settle=8.0, spin=2.0, step=0.30):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "dreamcast", "-M", "64"] +
                 EXTRA + [KERNEL])
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
    if alive:
        for i, c in enumerate(cmds):
            try:
                os.write(fd, (c + "\n").encode("latin-1"))
            except OSError:
                alive = False
                break
            if not rd(spin if i == len(cmds) - 1 else step):
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


class Addr(object):
    """Non-overlapping code blocks in guest RAM."""

    def __init__(self, base):
        self.a = base

    def take(self):
        a = self.a
        self.a += 0x40
        return a


def run(ops, at):
    put = ["put h 0x%x, 0x%04x" % (at + 2 * i, op) for i, op in enumerate(ops)]
    put += ["put h 0x%x, 0x%04x" % (at + 2 * len(ops), BRA_SELF),
            "put h 0x%x, 0x%04x" % (at + 2 * len(ops) + 2, NOP)]
    return put + ["pc=0x%x" % at, "step %d" % len(ops)]


def store16(reg, val, A):
    """ONE guest 16-bit store of `val` to `reg`."""
    return ["r7=0x%x" % reg, "r8=0x%04x" % val] + run([MOVW_ST(7, 8)], A.take())


def load16(reg, A, dest=2):
    """ONE guest 16-bit load from `reg` into r<dest>, then print it."""
    return ["r1=0x%x" % reg, "r%d=0" % dest] + \
        run([MOVW_LD(dest, 1)], A.take()) + ["print r%d" % dest]


def packet(words, A):
    """SIX guest 16-bit stores to GDROM_DATA, one contiguous run."""
    setup = ["r7=0x%x" % GDROM_DATA]
    for i, w in enumerate(words):
        setup.append("r%d=0x%04x" % (8 + i, w))
    return setup + run([MOVW_ST(7, 8 + i) for i in range(len(words))], A.take())


#  cmd[0]=0x14 Read-TOC (NetBSD gdrom_read_toc).  cnt must be 408.
CMD_TOC = [0x0014] * 6
#  cmd[0]=0x70 Mount (NetBSD gdrom_mount_disk).  Modelled as a no-op.
CMD_MOUNT = [0x0070] * 6
#  cmd[0]=0x30 Read-sectors, cmd[1]=0x20 the only silently-accepted format,
#  sector_nr=0, sector_count=1 (cmd[8..10] = 00 00 01).
CMD_READ = [0x2030, 0x0000, 0x0000, 0x0000, 0x0000, 0x0001]

#  Every diagnostic this device (or the disk layer under it) can emit.
NOISE = [
    re.compile(r"non-16bit GDROM_DATA access"),
    re.compile(r"read from GDROM_DATA with no data"),
    re.compile(r"write to GDROM_DATA while not waiting"),
    re.compile(r"read past the end of the GDROM_DATA buffer"),
    re.compile(r"GDROM: diskimage_access failed"),
    re.compile(r"non-existant"),
    re.compile(r"GDROM: rejecting sector_count"),
    re.compile(r"unimplemented"),
]


def noise(t):
    return sum(len(p.findall(t)) for p in NOISE)


# ------------------------------------------------------------------- controls
A = Addr(CODE)
t, alive, how = session(["r7=0x%x" % SCRATCH, "r8=0x%08x" % LIVE,
                         "r1=0x%x" % SCRATCH, "r2=0"] +
                        run([MOVL_ST(7, 8), MOVL_LD(2, 1)], A.take()) +
                        ["print r2"])
row("live", printed(t, "r2") if alive else "died", "0x%x" % LIVE,
    "LIVENESS: guest store then guest load, through RAM")

A = Addr(CODE)
t, alive, how = session(["r1=0x%x" % SH4_IPRD, "r2=0"] +
                        run([MOVL_LD(2, 1)], A.take()) + ["print r2"])
g = printed(t, "r2") if alive else "died"
row("devsig sh4", ("0x%x" % (int(g, 16) & 0xffff)) if g.startswith("0x") else g,
    "0x%x" % IPRD_RESET, "DEVSIG: SH4 IPRD reset value, RAM reads 0")

A = Addr(CODE)
t, alive, how = session(["r1=0x%x" % GDROM_BUSY, "r2=0"] +
                        run([MOVL_LD(2, 1)], A.take()) + ["print r2"])
g = printed(t, "r2") if alive else "died"
row("gdrom map", ("mapped" if g.startswith("0x") else g) if alive else "died",
    "mapped", "GDROM_BUSY read is served, not a paddr fault")


def stage_toc(A):
    """CNTLO/CNTHI = 408, COND = 0xa0, then the Read-TOC packet.  9 accesses."""
    return (store16(GDROM_CNTLO, 0x98, A) +
            store16(GDROM_CNTHI, 0x01, A) +
            store16(GDROM_COND, 0xa0, A) +
            packet(CMD_TOC, A))


def stage_readsectors(A):
    """COND = 0xa0 then the Read-sectors packet.  7 accesses, cnt left at 0."""
    return store16(GDROM_COND, 0xa0, A) + packet(CMD_READ, A)


#  DEVICE-SIGNATURE, GDROM-SPECIFIC.  The TOC is SYNTHESIZED by handle_command
#  (:352-377); 0x0010 then 0x9600 exists nowhere in RAM and no other device
#  produces it.  This is also the SAME instruction at the SAME address as the
#  trigger rows below -- it differs only in whether d->data is NULL.
A = Addr(CODE)
t, alive, how = session(stage_toc(A) +
                        ["r1=0x%x" % GDROM_DATA, "r2=0", "r3=0"] +
                        run([MOVW_LD(2, 1), MOVW_LD(3, 1)], A.take()) +
                        ["print r2", "print r3"])
row("devsig gd0", printed(t, "r2") if alive else "died", "0x10",
    "DEVSIG: synthesized TOC halfword 0, device-only value")
row("devsig gd1", printed(t, "r3") if alive else "died", "0xffff9600",
    "DEVSIG: TOC halfword 1, sign-extended by mov.w")
print("GDROMPIO_CONTROL=%s" % ("OK" if all(ok for _, ok in rows) else "DEAD"))

# ------------------------------------------------------------------- triggers
#
#  CHEAP ROUTE -- 9 guest accesses, no disk image, no prior staging.
#    1     store COND = 0xa0            (busy |= 0x08, cmd_count = 0)
#    2-7   six stores to GDROM_DATA     (cmd = 30 20 00 .. 01 00 -> handle_command)
#            cnt == 0 so :409 sets cnt = 2048; alloc_data sets data_len = 2048;
#            diskimage_access returns 0 with no IDE disk (diskimage.c:1566-1571,
#            fatal() but NO exit); :445-446 free(d->data), d->data = NULL;
#            the tail zeroes d->cnt and clears COND_DATA_AVAIL -- NOT data_len.
#    8     store COND = 0xef            (:720 d->cond = 0xef, bit 3 back on)
#    9     LOAD  GDROM_DATA             -> 0 < 2048 -> d->data[0] on NULL
A = Addr(CODE)
t1, alive1, how1 = session(stage_readsectors(A) +
                           store16(GDROM_COND, 0xef, A) +
                           load16(GDROM_DATA, A))
row("cheap trig", how1, "sig11", "9 accesses: SIGSEGV at the deref")
cheap_noise = noise(t1)

#  Same eight accesses, 0xef store REMOVED.  The read is declined at :590.
A = Addr(CODE)
t2, alive2, how2 = session(stage_readsectors(A) + load16(GDROM_DATA, A))
row("cheap noef", how2, "exit0", "SAME 8 accesses minus 0xef: survives")
row("cheap noef v", printed(t2, "r2") if alive2 else "died", "0xffffffff",
    "declined read returns 0xffff, sign-extended")

#  Same nine accesses INCLUDING 0xef, final LOAD removed.  Isolates the read.
A = Addr(CODE)
t3, alive3, how3 = session(stage_readsectors(A) + store16(GDROM_COND, 0xef, A))
row("cheap noread", how3, "exit0", "SAME 9 accesses minus the LOAD: survives")

#  STAGED ROUTE -- 18 guest accesses, legal TOC then legal Mount.  No disk
#  access is attempted at all, so the device emits NO diagnostic of any kind.
A = Addr(CODE)
t4, alive4, how4 = session(stage_toc(A) +
                           store16(GDROM_COND, 0xa0, A) + packet(CMD_MOUNT, A) +
                           store16(GDROM_COND, 0xef, A) +
                           load16(GDROM_DATA, A))
row("staged trig", how4, "sig11", "18 accesses, TOC then Mount: SIGSEGV")
row("staged quiet", "%d of %d" % (noise(t4), len(NOISE)),
    "0 of %d" % len(NOISE), "NO diagnostic on the silent route")
row("cheap loud", "yes" if cheap_noise > 0 else "no", "yes",
    "cheap route IS loud (%d hits): premise-3 contrast" % cheap_noise)

#  Staged route minus the 0xef store: same 17 accesses, read declined.
A = Addr(CODE)
t5, alive5, how5 = session(stage_toc(A) +
                           store16(GDROM_COND, 0xa0, A) + packet(CMD_MOUNT, A) +
                           load16(GDROM_DATA, A))
row("staged noef", how5, "exit0", "SAME 17 accesses minus 0xef: survives")

n = sum(1 for _, ok in rows if ok)
print("GDROMPIO_RESULT=%d/%d" % (n, len(rows)))
print("GDROMPIO_VECTOR=" + ",".join(("1" if ok else "0") for _, ok in rows))
