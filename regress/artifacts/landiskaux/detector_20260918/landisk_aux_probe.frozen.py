#!/usr/bin/env python3
"""DETECTOR for landiskaux: landisk's wdc AUXILIARY (alt-status / Device Control) register.

THE DEFECT.  dev_wdc.c's `Special hacks for individual machines' switch had no MACHINE_LANDISK
case, so landisk kept the pre-switch PC-layout default `devinit->addr + 0x206' and registered
`wdc_altstatus' at 0x14000206.  The OpenBSD 7.6 landisk kernel writes Device Control at
0x1400002c -- twelve byte stores per boot, the first 0x0c = SRST|4BIT, a real ATA soft reset
(regress/artifacts/landiskaux/census_20260827/) -- so every one landed on memory no device
claimed and the reset was silently lost.

THE ADDRESS IS A PRIMARY-SOURCE CONSTANT, NOT A DERIVATION.  NetBSD and OpenBSD
sys/arch/landisk/dev/wdc_obio.c both define WDC_OBIO_AUXREG_OFFSET 0x2c and map the aux
register at `or_addr + WDC_OBIO_AUXREG_OFFSET', unscaled (copies preserved in
regress/artifacts/landiskaux/rung3_opus_20260918/).

Rows assert the POST-FIX state, so this is green after the fix and safe to gate.  The WITNESS is
the recorded fact that the same guest program scored the pre-fix symptom on the committed build
(regress/artifacts/landiskaux/rung3_opus_20260918/opus_landiskaux_rung3_20260918.out).

Rung 3: a real guest program on UNMODIFIED `-E landisk'.  Nothing is added to reach the site.
Each session fills the ATA data ring with eight `mov.w' to 0xb4000000 (sets DRQ, status 0x09),
optionally makes ONE Device Control byte store of 0x0c, then reads back main status (0xb400000e)
and the two candidate aux addresses (0xb400002c, 0xb4000206).  A soft reset that reaches the
device purges the ring and status drops to 0x01; a store that lands nowhere leaves 0x09.

CONTRACT (clause e).  Designed to catch, and each row names what it kills:
  * the landisk case missing or mis-keyed (the pre-fix state)       -- `aux 2c reset', `aux 2c read'
  * a wrong offset: `+ 0x16' unscaled, `+ 0x2d', any value != 0x2c   -- `aux 2c reset', `aux 2c read'
  * the case placed above IQ80321 without `break' (falls to +0x402)  -- `aux 2c reset', `aux 2c read'
  * REGISTERING BOTH addresses (old kept, new added)                 -- `aux 206 gone', `206 ctl dead'
DISCLOSED, not caught: the pre-switch initialiser `+ 0x206' changing (landisk overwrites it, so no
landisk row can see it); IQ80321 losing its own `break' after this case is appended (no IQ80321
rig); the registration width 2 -> 1 (every access here is 1 byte at offset 0 -- that is
`wdcaltwidth'); keying on machine_type alone (a second wdc on a future landisk model would
inherit +0x2c).  And the fix DELIVERS the five WDCTL_IDS (nIEN) writes; it does not IMPLEMENT
nIEN -- the aux handler acts on WDCTL_RST only.

NO ROW RESTS ON A DEBUG LINE.  `[ wdc: write to ALT. CTRL ]' goes quiet under -q and when
free-running; every row reads a guest-visible register value instead.
"""
import os
import pty
import re
import select
import sys
import time

BIN = sys.argv[1] if len(sys.argv) > 1 else "../../build/gxemul"
KERNEL = sys.argv[2] if len(sys.argv) > 2 else "../../_images/openbsd76-landisk-bsd.rd"

AT = 0x8c001000          # landisk RAM, as sh_pclock_probe.py's LANDISK_CODE
RAM_CTRL = 0x8c002000    # a RAM address for the no-control liveness session
BRA_SELF = 0xaffe
NOP = 0x0009
#  Encodings as MEASURED in the rung-3 witness run, not re-derived:
MOV_W_R8_AT_R7 = 0x2781  # mov.w r8,@r7    -- fill the data ring
MOV_B_R9_AT_R10 = 0x2a90 # mov.b r9,@r10   -- the ONE Device Control store
MOV_B_AT_R1_R2 = 0x6210  # mov.b @r1,r2    -- main status
MOV_B_AT_R3_R4 = 0x6430  # mov.b @r3,r4    -- aux at 0x2c
MOV_B_AT_R5_R6 = 0x6650  # mov.b @r5,r6    -- aux at 0x206

rows = []


def row(name, got, want, note=""):
    ok = (got == want)
    rows.append((name, ok))
    print("%-14s %-8s %-8s %-52s %s" % (name, got, want, note, "ok" if ok else "FAIL"))
    return ok


def session(cmds, settle=6.0, spin=2.0):
    """One cold-debugger session on unmodified -E landisk.  (transcript, survived)."""
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-E", "landisk", "-M", "64", KERNEL])
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
    try:
        os.waitpid(pid, 0)
    except OSError:
        pass
    return buf, alive


def printed(t, reg):
    m = re.search(r"print\s+%s\s*\r?\n\s*(0x[0-9a-f]+)" % reg, t)
    return m.group(1) if m else "absent"


def prog(ctrl, ctrlval=0x0c, ndata=8):
    """Fill the ring, one byte store of ctrlval to ctrl, then read status and both aux addresses."""
    ops = ([MOV_W_R8_AT_R7] * ndata
           + [MOV_B_R9_AT_R10, MOV_B_AT_R1_R2, MOV_B_AT_R3_R4, MOV_B_AT_R5_R6, BRA_SELF, NOP])
    cmds = ["r7=0xb4000000", "r8=0x1234", "r10=0x%x" % ctrl, "r9=0x%x" % ctrlval,
            "r1=0xb400000e", "r3=0xb400002c", "r5=0xb4000206",
            "r2=0xaa", "r4=0xaa", "r6=0xaa"]
    cmds += ["put h 0x%x, 0x%04x" % (AT + 2 * i, op) for i, op in enumerate(ops)]
    cmds += ["pc=0x%x" % AT, "step %d" % (ndata + 4), "print r2", "print r4", "print r6"]
    return cmds


print("landisk_aux_probe -- binary=%s" % BIN)

#  Session 1: NO control store (it goes to RAM).  Liveness, and the at-rest aux reads.
t, alive = session(prog(RAM_CTRL))
st, a2c, a206 = printed(t, "r2"), printed(t, "r4"), printed(t, "r6")
row("live", st, "0x9",
    "ring fill sets DRQ: status 0x09 -- the ring is live, so 0x01 elsewhere is the reset")
row("aux 2c rest", a2c, "0x9",
    "0x2c answers with STATUS (0x09) -- device signature; pre-fix unmapped reads 0x0")
row("aux 206 gone", a206, "0x0",
    "0x206 is UNMAPPED on landisk: pre-fix 0x09; kills a register-BOTH mutant")

#  Session 2: the soft reset goes to 0x2c, where the kernel sends it.
t, alive = session(prog(0xb400002c))
st, a2c = printed(t, "r2"), printed(t, "r4")
row("aux 2c reset", st, "0x1",
    "SRST at 0x2c PURGES the ring: status 0x01; pre-fix the store is lost, stays 0x09")
row("aux 2c read", a2c, "0x1",
    "0x2c then reads the post-reset status 0x01 -- same device, same value")

#  Session 3: the soft reset goes to the OLD address.
t, alive = session(prog(0xb4000206))
st = printed(t, "r2")
row("206 ctl dead", st, "0x9",
    "SRST at 0x206 must land NOWHERE: status stays 0x09; pre-fix it purged (0x01)")

n = sum(1 for _, ok in rows if ok)
print("LANDISK_AUX_RESULT=%d/%d" % (n, len(rows)))
print("LANDISK_AUX_VECTOR=" + ",".join(("1" if ok else "0") for _, ok in rows))
print("LANDISK_AUX_DONE")
