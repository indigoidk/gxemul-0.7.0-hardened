#!/usr/bin/env python3
"""RUNG-3 WITNESS for ledger row `gdromexitsix`, Round 1 -- the `case 0x14` TOC length
guard in dev_dreamcast_gdrom.c (`grep -n 'GDROM Read TOC not 408' <file>`).

*** THIS IS A WITNESS, NOT YET A DETECTOR.  It is written BEFORE the edit and must be
MEASURED RED ON THE COMMITTED BUILD FIRST.  If you are reading it after the fix shipped,
the `toc badlen` row's `want` has been inverted and this header must say so. ***

WHY IT EXISTS.  The row's `witness` field reads `none` because its previous `probe:` field
cited two scratchpad scripts that a `find` over the whole project cannot locate -- they
lived only in a rotated scratchpad.  So "fully witnessed" described vanished evidence.
This file is preserved under regress/artifacts/ precisely so that cannot recur.

THE DEFECT.  `handle_command()`, `case 0x14` (Read Table-Of-Contents):

    if (d->cnt != 408) {
            fatal("GDROM Read TOC not 408 bytes?\\n");
            exit(1);
    }
    alloc_data(d);

`d->cnt` is GUEST-SUPPLIED (two 16-bit stores to GDROM_CNTLO/GDROM_CNTHI).  So an ordinary
guest register access ends the host process.  That is the defect this witness pins.

*** AND THE GUARD IS LOAD-BEARING, WHICH IS WHY THE FIX IS A DECLINE AND NOT A DELETION. ***
`alloc_data()` mallocs `d->cnt` bytes, but the TOC writer immediately below uses HARDCODED
indices:

    grep -oE 'd->data\\[[0-9]+\\*4(\\+[0-9])?\\]' <file>   ->  highest byte index 407

so the writer needs 408 bytes REGARDLESS of cnt.  Deleting the exit(1) would turn a host
kill into a GUEST-CONTROLLED HEAP OVERFLOW of up to 408 bytes (and malloc(0) at cnt == 0).
Established by reading, after two packet-fed seats independently asked the question and
refused to certify the premise from the packet.

RUNG 3.  Every access below is a real guest instruction executed through real address
decode and real memory_rw, on the UNMODIFIED committed `dreamcast` machine description.
Nothing is device_add'ed and no machine description is introduced to reach the site.

ORACLE -- DEATH MODE, not merely "died".  The probe reports HOW the process ended:
  exit1  = fatal() + exit(1)   -- THE DEFECT (this device's guarded-refusal death)
  exit0  = survived and quit cleanly
  sig11  = a SIGSEGV            -- a DIFFERENT defect (the #465 class), not this one
Reporting the mode is what makes "died" evidence: a sig11 here would mean the packet
reached the NULL-deref path instead, and would NOT support this round.

*** NOTE THE ORACLE COLLISION WITH `gdrompionull`, DELIBERATELY AND IN THE OPPOSITE
DIRECTION. ***  That probe uses `exit1` to mean "a mis-built packet, NOT the defect",
because a wrong cmd[0] lands in `default:` and a wrong cmd[1] in the 0x30 format check --
both exit(1).  Here `exit1` IS the defect.  Same status, opposite meaning, because the two
rounds target different sites.  That is why this probe carries its own packet-validation
evidence (the `toc accept` row) rather than borrowing that oracle.

CONTROLS.  Each runs in its own session and none reaches the declined path.
  live        LIVENESS      -- a guest store then a guest load, through RAM
  devsig sh4  DEVICE-SIG    -- SH4 IPRD reset value; RAM would read 0
  gdrom map   REACHABILITY  -- a GDROM register read is served, not a paddr fault
  toc accept  ACCEPT SIDE   -- cnt == 408 still synthesizes a REAL TOC

*** `toc accept` IS NOT DECORATION.  It is the ACCEPT ROW the de-escalation clause
mandates. ***  This fix removes a host-fatal guard, and the carrier's rule is that doing so
DELETES the accidental tripwire which made guard-growth self-announcing: before the fix,
narrowing the accept set meant exit(1) on the first legal write -- unmissable.  After it,
the same edit means a silently refused TOC.  `toc accept` pins the accept side so that a
future guard that grows (e.g. `!= 408` -> `< 408 || > 408 || cnt & 7`) reddens instead of
going quiet.  It also validates the hand-assembled packet for free: 0x0010 then 0x9600 is
SYNTHESIZED by handle_command and exists nowhere in RAM, so a green accept row proves the
six-word packet really did reach `case 0x14`.

DREAMCAST NEEDS -x (two console inputs) or the session dies for a CONFIGURATION reason and
reports the same "died" the defect reports.

USAGE:  gdrom_toclen_witness.py <gxemul-binary> <kernel-image> [extra args...]
"""
import os
import pty
import re
import select
import sys
import time

BIN = sys.argv[1]
KERNEL = sys.argv[2]
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


#  cmd[0]=0x14 Read-TOC (NetBSD gdrom_read_toc).
CMD_TOC = [0x0014] * 6


def stage_toc(A, cnt):
    """CNTLO/CNTHI = cnt, COND = 0xa0, then the Read-TOC packet.  9 accesses.

    cnt is assembled by the device from the two halves, so 408 == 0x0198 is
    (CNTLO=0x98, CNTHI=0x01) -- the ONLY value the shipped guard accepts.
    """
    return (store16(GDROM_CNTLO, cnt & 0xff, A) +
            store16(GDROM_CNTHI, (cnt >> 8) & 0xff, A) +
            store16(GDROM_COND, 0xa0, A) +
            packet(CMD_TOC, A))


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

#  ACCEPT SIDE.  cnt == 408 is the one accepted value.  The TOC is SYNTHESIZED by
#  handle_command, so 0x0010 then 0x9600 exists nowhere in RAM and no other device
#  produces it -- a green pair proves the six-word packet really reached `case 0x14`.
#  THIS ROW IS THE DE-ESCALATION ACCEPT ROW and must stay green across the fix.
A = Addr(CODE)
t, alive, how = session(stage_toc(A, 408) +
                        ["r1=0x%x" % GDROM_DATA, "r2=0", "r3=0"] +
                        run([MOVW_LD(2, 1), MOVW_LD(3, 1)], A.take()) +
                        ["print r2", "print r3"])
row("toc accept0", printed(t, "r2") if alive else "died", "0x10",
    "ACCEPT: synthesized TOC halfword 0, device-only value")
row("toc accept1", printed(t, "r3") if alive else "died", "0xffff9600",
    "ACCEPT: TOC halfword 1, sign-extended by mov.w")
row("toc acceptx", how, "exit0", "ACCEPT: the legal length must NOT kill the host")
print("TOCLEN_CONTROL=%s" % ("OK" if all(ok for _, ok in rows) else "DEAD"))

# ------------------------------------------------------------------- the witness
#
#  NINE guest accesses, no disk image, no prior staging:
#    1-2   store CNTLO/CNTHI = 407      (d->cnt = 407, guest-chosen, != 408)
#    3     store COND = 0xa0            (busy |= 0x08, cmd_count = 0)
#    4-9   six stores to GDROM_DATA     (cmd[0] = 0x14 -> handle_command, case 0x14)
#                                       -> `d->cnt != 408` -> fatal() + exit(1)
#
#  407 is chosen deliberately: it is ONE BELOW the accepted value, so it is the
#  smallest possible departure from a legal request, and it is exactly the case in
#  which a bare deletion would malloc 407 bytes for a writer that indexes byte 407.
A = Addr(CODE)
t1, alive1, how1 = session(stage_toc(A, 407))
row("toc badlen", how1, "exit1",
    "WITNESS: cnt=407 ends the host -- PRE-FIX EXPECTATION")

#  cnt == 0 is the other end of the same guard, and it is the malloc(0) case.
A = Addr(CODE)
t2, alive2, how2 = session(stage_toc(A, 0))
row("toc zerolen", how2, "exit1",
    "WITNESS: cnt=0 ends the host too -- PRE-FIX EXPECTATION")

ok = all(o for _, o in rows)
print("")
print("TOCLEN_WITNESS=%s  (%d/%d rows)" %
      ("RED_AS_EXPECTED" if ok else "UNEXPECTED", sum(1 for _, o in rows if o),
       len(rows)))
print("badlen=%s zerolen=%s" % (how1, how2))
sys.exit(0 if ok else 1)
