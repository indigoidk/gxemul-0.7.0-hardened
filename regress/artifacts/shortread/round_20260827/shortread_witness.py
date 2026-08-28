#!/usr/bin/env python3
"""RUNG-3 WITNESS for the mid-transfer short read in fread_helper().

A real guest instruction sequence, through real address decode and real
memory_rw, on an UNMODIFIED in-tree machine description (`landisk`).  Nothing is
added to reach the site: the machine attaches wdc itself
(machine_landisk.c `wdc addr_mult=2 addr=0x14000000`), and the guest drives it
through the ordinary ATA register interface.

  fixture      base disk = all 'B'.  Overlay claims block 0 in its bitmap while
               its DATA FILE IS 200 BYTES LONG -- the state the offline
               differential builds, prepared by the HOST because GXemul's own
               writer provably cannot produce it (fwrite_helper() returns 0 on a
               short overlay write BEFORE overlay_set_block_in_use(), so the bit
               is never set).

  guest route  seccnt=3, sector=1, cyl=0, head=0, command 0x20 (READ SECTORS).
               wdc__read() then issues ONE diskimage_access() of 1536 bytes at
               offset 0 -- three OVERLAY_BLOCK_SIZE pieces, the first of which
               comes up short.  The guest then reads the 16-bit data port.

  oracle       THE TAIL ANCHOR.  Halfword 767 is bytes 1534..1535, which the base
               image supplies as 'B','B' = 0x4242.  On the shipped build the
               short first piece makes fread_helper() return 1224 rather than
               1536, and the caller zero-fills [1224,1536) -- destroying 312
               VALID base bytes at the far end and reporting success.  So the
               same halfword reads 0x0000.

  *** THE HOLE ITSELF IS NOT VISIBLE FROM THE GUEST HERE, AND SAYING SO IS PART
      OF THE RESULT. ***  The caller buffer is the device's own `d->inbuf`, not a
      guest-filled one, so the stale bytes at [200,512) are whatever that buffer
      last held -- zero on a fresh device.  This witness therefore measures the
      TAIL-DESTRUCTION half of the defect only.  The offline differential still
      carries the stale-hole half, which it can because it owns the buffer.

  controls     `live`   a known value round-trips through the same decode.
               `devsig` the STATUS register answers non-zero -- RAM and unmapped
                        space both answer 0, so this is what separates
                        "the device answered" from "something answered".
               `ovl`    halfword 0 is 'V','V': the truncated overlay really is
                        supplying block 0.  Without it a green tail row could
                        mean the overlay was never consulted and every byte came
                        from the base -- the vacuous-fixture failure this
                        project has already paid for once.
               `accept` a 3-sector read starting at sector 5 touches no overlay
                        block at all and must read 'B','B' on BOTH builds.  It
                        is what makes the tail row a statement about the short
                        read rather than about reads in general.

Usage:  shortread_witness.py <gxemul-binary> <kernel> <workdir>
"""
import os
import pty
import re
import select
import sys
import time

BIN = sys.argv[1]
KERNEL = sys.argv[2]
WORK = sys.argv[3]

BASE = os.path.join(WORK, "wit_base.img")
OVL = os.path.join(WORK, "wit_ovl.img")
MAP = OVL + ".map"

#  landisk: addr_mult=2, so ATA register N sits at 0x14000000 + 2N.  0xb4... is
#  the P2 (uncached) window, which is what a device access must use.
WDC = 0xb4000000
WD_DATA = WDC + 0
WD_SECCNT = WDC + 4
WD_SECTOR = WDC + 6
WD_CYLLO = WDC + 8
WD_CYLHI = WDC + 10
WD_SDH = WDC + 12
WD_CMD = WDC + 14

CODE = 0x8c001000
SCRATCH = 0x8c001800
LIVE = 0x5eed

NOP = 0x0009
BRA_SELF = 0xaffe
MOV_L_R8_AT_R7 = 0x2782            # mov.l r8,@r7
MOV_L_AT_R1_R2 = 0x6212            # mov.l @r1,r2
MOV_W_AT_R1_R2 = 0x6211            # mov.w @r1,r2
MOV_B_R8_AT_R7 = 0x2780            # mov.b r8,@r7
MOV_B_AT_R1_R2 = 0x6210            # mov.b @r1,r2
DT_R3 = 0x4310                     # dt r3


def BF_BACK(n):
    return 0x8b00 | ((-(n + 3)) & 0xff)


rows = []


def row(name, got, want, note=""):
    ok = (got == want)
    rows.append((name, ok, got, want))
    print("  %-10s %-12s %-12s %-46s %s"
          % (name, got, want, note, "ok" if ok else "FAIL"))
    return ok


def mkfile(path, n, ch):
    with open(path, "wb") as f:
        f.write(bytes([ch]) * n)


def session(cmds, settle=8.0, spin=3.0, disk=True):
    argv = [BIN, "-V", "-x", "-E", "landisk", "-M", "64"]
    if disk:
        argv += ["-d", "i0:" + BASE, "-d", "Vi0:" + OVL]
    argv.append(KERNEL)
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, argv)
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
    for fn in (lambda: os.close(fd), lambda: os.waitpid(pid, 0)):
        try:
            fn()
        except OSError:
            pass
    return buf, alive


def printed(t, reg):
    m = re.findall(r"print\s+%s\s*\r?\n\s*(0x[0-9a-f]+)" % reg, t)
    return m[-1] if m else "absent"


def run(steps, at=CODE):
    put = ["put h 0x%x, 0x%04x" % (at + 2 * i, op) for i, op in enumerate(steps)]
    put += ["put h 0x%x, 0x%04x" % (at + 2 * len(steps), BRA_SELF),
            "put h 0x%x, 0x%04x" % (at + 2 * len(steps) + 2, NOP)]
    return put + ["pc=0x%x" % at, "step %d" % len(steps)]


def stb(reg, val):
    """One BYTE store to an ATA register, as a real guest instruction."""
    return ["r7=0x%x" % reg, "r8=0x%08x" % val] + run([MOV_B_R8_AT_R7])


def runloop(body, count, at=CODE):
    """Emit `body` in a hardware loop of `count` iterations and FREE-RUN it.

    Free-running rather than stepping is not only speed: dev_wdc.c sets
    d->data_debug at attach, so every data-port read calls debug(), which PRINTS
    under single-stepping and is silent when free-running at verbose 0.  768
    stepped reads would be 768 pty lines per row.

    `print r3` is a COMPLETION control: session()'s reader returns True on a
    plain timeout, so without it a `continue` that never reached the breakpoint
    would leave the guest spinning and the row would score stale buffer text.
    """
    ops = list(body) + [DT_R3, BF_BACK(len(body))]
    end = at + 2 * len(ops)
    put = ["r3=%d" % count]
    put += ["put h 0x%x, 0x%04x" % (at + 2 * i, op) for i, op in enumerate(ops)]
    put += ["put h 0x%x, 0x%04x" % (end, BRA_SELF),
            "put h 0x%x, 0x%04x" % (end + 2, NOP)]
    return put + ["breakpoint add 0x%x" % end, "pc=0x%x" % at, "continue",
                  "print r3"]


def ata_read(sector, seccnt, nhalf):
    """Drive one READ SECTORS and consume `nhalf` halfwords from the data port.

    r2 is left holding the LAST halfword read, which is the oracle.
    """
    cmds = []
    cmds += stb(WD_SECCNT, seccnt)
    cmds += stb(WD_SECTOR, sector)
    cmds += stb(WD_CYLLO, 0)
    cmds += stb(WD_CYLHI, 0)
    cmds += stb(WD_SDH, 0)
    cmds += stb(WD_CMD, 0x20)
    cmds += ["r1=0x%x" % WD_DATA]
    cmds += runloop([MOV_W_AT_R1_R2], nhalf)
    cmds += ["print r2"]
    return cmds


def main():
    os.makedirs(WORK, exist_ok=True)
    #  Base: 1 MB of 'B'.  Overlay DATA truncated to 200 bytes of 'V' while its
    #  bitmap claims the whole of block 0 -- nothing in diskimage_add_overlay()
    #  checks the data file's length against the bitmap.
    mkfile(BASE, 1024 * 1024, ord('B'))
    mkfile(OVL, 200, ord('V'))
    with open(MAP, "wb") as f:
        f.write(bytes([0x01]))

    print("  %-10s %-12s %-12s %-46s %s"
          % ("row", "got", "want", "note", ""))

    #  ---- controls -----------------------------------------------------
    t, alive = session(["r7=0x%x" % SCRATCH, "r8=0x%08x" % LIVE]
                       + run([MOV_L_R8_AT_R7])
                       + ["r1=0x%x" % SCRATCH, "r2=0"]
                       + run([MOV_L_AT_R1_R2]) + ["print r2"])
    row("live", printed(t, "r2") if alive else "died", "0x5eed",
        "a known value round-trips through the decode")

    t, alive = session(["r1=0x%x" % WD_CMD, "r2=0"]
                       + run([MOV_B_AT_R1_R2]) + ["print r2"])
    st = printed(t, "r2") if alive else "died"
    row("devsig", "nonzero" if st not in ("died", "absent", "0x0") else st,
        "nonzero", "STATUS answers from device state, not RAM")

    #  ---- the fixture is live: block 0 really comes from the overlay ----
    t, alive = session(ata_read(sector=1, seccnt=3, nhalf=1))
    row("ovl", printed(t, "r2") if alive else "died", "0x5656",
        "halfword 0 is 'V','V' -- the truncated overlay is consulted")

    #  ---- THE DEFECT ---------------------------------------------------
    t, alive = session(ata_read(sector=1, seccnt=3, nhalf=768))
    row("tail", printed(t, "r2") if alive else "died", "0x4242",
        "bytes 1534..1535 are base 'B' -- shipped build reads 0x0000")

    #  ---- accept side: a read that touches no overlay block -------------
    t, alive = session(ata_read(sector=5, seccnt=3, nhalf=768))
    row("accept", printed(t, "r2") if alive else "died", "0x4242",
        "no overlay block crossed; must be 'B','B' on BOTH builds")

    bad = [r for r in rows if not r[1]]
    print("\n%d rows, %d failures" % (len(rows), len(bad)))
    print("SHORTREAD_WITNESS_%s" % ("PASS" if not bad else "FAIL"))


main()
