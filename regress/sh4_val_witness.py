#!/usr/bin/env python3
"""#447 WITNESS (rung 3): four value guards in DEVICE_ACCESS(sh4) end the HOST
PROCESS on ONE ordinary guest store, on an UNMODIFIED in-tree `-E landisk`.

    TCR0/1/2   0xffd80010/1c/28  w=2  0x0004  TCR_TPSC2
    DMATCR0..7 0xffa00008 + ...  w=4  0x01000000
    ICR        0xffd00000        w=2  0x0080  IRLM
    RCR1       0xffc80038        w=1  0x18    SH_RCR1_CIE|SH_RCR1_AIE

This asserts the PRE-FIX SYMPTOM, so it is RED once the defect is gone -- which
is what a witness should be, and is why it is not wired into a gate.  Its
sibling sh4_val_probe.py is the DETECTOR and asserts the repaired behaviour.
Grading one by the other's clauses is a category error in either direction.
MEASURED: 15/15 on the pre-fix build, 11/15 on the fixed one, the four
difference rows being exactly the four kills.

IT IS COMMITTED RATHER THAN LEFT IN _scratchpad/, which is the mrwstore2 lesson
this project has now paid for three times: that round's rung-3 probe left NO
artefact, so its reproduction became a remembered grep and a later row had to
re-cost the work.  #442 and #443 committed theirs for the same reason.

THE CONTROLS ARE WHAT MAKE IT A MEASUREMENT AND NOT A CRASH REPORT.  For every
kill there is a SURVIVING write at the SAME address and the SAME width, so the
result reads "this VALUE ends the host" and not "this address does" or "this
width does".  Two device-signature reads prove DEVICE_ACCESS(sh4) itself was
entered -- and they are values only that switch synthesises, so RAM cannot
supply them.  Four reads prove the guards are on the WRITE path only.

usage:  sh4_val_witness.py <gxemul-binary> <landisk-kernel>

    *** KEEP THE "./" ON THE BINARY. ***  `os.execvp` on a bare name searches
    PATH; when it misses, EVERY arm reports alive=False and a witness written
    the naive way "passes" having measured nothing.  W0 catches that.
"""
import os
import sys

#  Python puts this script's own directory on sys.path[0], so the session
#  machinery (the #392 readiness predicate, the echo guard, the fresh mark)
#  comes from the one place in the tree that has it, rather than a copy.
import sh4_pcic_probe as P

#  Every address and constant READ from a header in this repository.
SH4_TCR0 = 0xffd80010           # thirdparty/sh4_tmureg.h:54
SH4_DMATCR0 = 0xffa00008        # sh4_dmacreg.h:39
SH4_ICR = 0xffd00000            # thirdparty/sh4_intcreg.h:79
SH4_RCR1 = 0xffc80038           # thirdparty/sh4_rtcreg.h:68
SH4_PVR_ADDR = 0xff000030       # thirdparty/sh4_cpu.h:187
SH4_PRR_ADDR = 0xff000044       # :189
SH4_PVR_SH7751 = 0x04110000     # :196
SH4_PRR_7751R = 0x00000110      # :200
TCR_TPSC2 = 0x0004              # thirdparty/sh4_tmureg.h:82
TCR_TPSC_P64 = 0x0002           # :87
SH_RCR1_CIE, SH_RCR1_AIE = 0x10, 0x08     # thirdparty/sh4_rtcreg.h:72-73
SH_RCR1_AF = 0x01               # :75

ST = {1: 0x2100, 2: 0x2101, 4: 0x2102}    # mov.b/w/l r0,@r1

rows = []


def row(name, ok, got, want):
    rows.append((name, bool(ok), got, want))
    print("  %-4s %s" % ("ok" if ok else "FAIL", name))
    if not ok:
        print("       got  %s\n       want %s" % (got, want))


def rd(addr, label, kw):
    return P.read_arm(addr, label, kw)


def wr(addr, val, width, label, kw):
    return P.write_arm(addr, val, label, kw, op=ST[width])


def main():
    if len(sys.argv) != 3:
        print(__doc__.strip().splitlines()[-4])
        return 2
    b, k = sys.argv[1], sys.argv[2]
    kw = dict(binary=b, kernel=k)
    for p in (b, k):
        if not os.path.exists(p):
            print("OPERATIONAL FAILURE: %s does not exist (cwd=%s)"
                  % (p, os.getcwd()))
            print("SH4VAL_WITNESS_FAIL")
            return 2

    #  ---- the device is reached, and answers something only it knows --------
    buf, alive, st = rd(SH4_PVR_ADDR, "W-c1", kw)
    v = P.dumped(buf)
    row("W-c1 DEVICE SIGNATURE: PVR reads 0x04110000 in DEVICE_ACCESS(sh4)",
        st and alive and v == P.le(SH4_PVR_SH7751),
        "started=%s alive=%s val=%s" % (st, alive, v),
        "val=%s (RAM would answer %s)" % (P.le(SH4_PVR_SH7751), P.le(0)))

    buf, alive, st = rd(SH4_PRR_ADDR, "W-c2", kw)
    v = P.dumped(buf)
    row("W-c2 DEVICE SIGNATURE: PRR reads 0x00000110 (small non-zero)",
        st and alive and v == P.le(SH4_PRR_7751R),
        "started=%s alive=%s val=%s" % (st, alive, v),
        "val=%s" % P.le(SH4_PRR_7751R))

    #  ---- the four kills ---------------------------------------------------
    for name, addr, val, width, msg in [
            ("S1 TCR0    0xffd80010 w=2 0x0004 (TCR_TPSC2)",
             SH4_TCR0, TCR_TPSC2, 2, "Unimplemented SH4 timer control"),
            ("S2 DMATCR0 0xffa00008 w=4 0x01000000 (bit 24)",
             SH4_DMATCR0, 0x01000000, 4, "Attempt to set top 8 "),
            ("S3 ICR     0xffd00000 w=2 0x0080 (IRLM)",
             SH4_ICR, 0x0080, 2, "IRLM not yet "),
            ("S4 RCR1    0xffc80038 w=1 0x18 (CIE|AIE)",
             SH4_RCR1, SH_RCR1_CIE | SH_RCR1_AIE, 1,
             "TODO: RTC interrupt enable")]:
        buf, alive, st = wr(addr, val, width, name, kw)
        row("%s KILLS the host" % name,
            st and not alive and msg in (buf or ""),
            "started=%s alive=%s diagnostic=%s"
            % (st, alive, msg in (buf or "")),
            "started=True alive=False, and %r printed first" % msg)

    #  ---- matched SURVIVING controls: same address, same width --------------
    for name, addr, val, width in [
            ("C1 TCR0    w=2 0x0002 (TPSC_P64, accepted)",
             SH4_TCR0, TCR_TPSC_P64, 2),
            ("C2 DMATCR0 w=4 0x00000010 (inside 24 bits)",
             SH4_DMATCR0, 0x00000010, 4),
            ("C3 ICR     w=2 0x0000 (IRLM clear)", SH4_ICR, 0x0000, 2),
            ("C4 RCR1    w=1 0x01 (AF, not CIE/AIE)",
             SH4_RCR1, SH_RCR1_AF, 1)]:
        buf, alive, st = wr(addr, val, width, name, kw)
        row("%s SURVIVES" % name, st and alive,
            "started=%s alive=%s" % (st, alive),
            "alive=True -- so it is the VALUE, not the address and not the "
            "width")

    #  ---- every guard is on the WRITE path ---------------------------------
    for name, addr in [("R1 TCR0", SH4_TCR0), ("R2 DMATCR0", SH4_DMATCR0),
                       ("R3 ICR", SH4_ICR), ("R4 RCR1", SH4_RCR1)]:
        buf, alive, st = rd(addr, name, kw)
        row("%s READ survives -- all four guards are write-only" % name,
            st and alive and P.dumped(buf) is not None,
            "started=%s alive=%s val=%s" % (st, alive, P.dumped(buf)),
            "alive=True and a value came back")

    n = len(P.STARTS)
    nok = sum(1 for _, s in P.STARTS if s)
    row("W0 every session reached the debugger prompt",
        n > 0 and n == nok,
        "sessions=%d started=%d failed=%s"
        % (n, nok, [l for l, s in P.STARTS if not s][:6]),
        "started == sessions > 0 -- a session that never started ALSO reports "
        "alive=False, and scoring that as a kill would let a broken invocation "
        "masquerade as a measurement")

    f = sum(1 for _, ok, _, _ in rows if not ok)
    print()
    print("SH4VAL_WITNESS_RESULT=%d/%d" % (len(rows) - f, len(rows)))
    print("SH4VAL_WITNESS_PASS" if f == 0 else "SH4VAL_WITNESS_FAIL")
    return 1 if f else 0


if __name__ == "__main__":
    sys.exit(main())
