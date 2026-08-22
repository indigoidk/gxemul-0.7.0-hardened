#!/usr/bin/env python3
"""`sh4rtcsr` WITNESS (rung 3): a guest RTCSR write ends the host process MILLISECONDS
LATER, from a 110 Hz host timer callback -- on an UNMODIFIED in-tree `-E landisk`.

*** THIS IS A SHAPE NO OTHER PROBE IN THIS TREE CAN SEE, AND THE REASON IS STRUCTURAL. ***

Every SH-4 probe here observes the STORE SITE: issue one guest store, then ask whether the
host survived that instruction.  #443, #447 and #448 are all built that way, and it is the
right shape for them -- their defects die inside `DEVICE_ACCESS(sh4)`, on the store.

This one does not.  The write lands, the handler returns, the debugger prompt comes back,
and the process is killed afterwards by a callback:

    dev_sh4.c   case SH4_RTCSR:  d->bsc_rtcsr = idata & 0x00ff;   <- returns normally
    dev_sh4.c   sh4_timer_tick():
                    if (d->bsc_rtcsr & (RTCSR_CMIE | RTCSR_OVIE)) {
                            fatal("sh4: RTCSR_CMIE | RTCSR_OVIE: TODO");
                            exit(1);
                    }
    dev_sh4.c   d->sh4_timer = timer_add(SH4_PSEUDO_TIMER_HZ, sh4_timer_tick, d);

SH4_PSEUDO_TIMER_HZ is 110.0, so the callback fires about every nine milliseconds of free
running.  A store-site probe asks its question and gets "alive" -- correctly, and
uselessly.  Row S0 below is that observation, kept as a ROW rather than a footnote,
because the distance between S0 and S1 IS the finding.

HOW THE GUEST IS MADE TO RUN FREE, and why the spin is BOUNDED.  The session helper
decides liveness by sending `dump` after the run: an UNBOUNDED spin never returns to the
prompt, so `dump` never answers and the row would read `alive=False` on a perfectly
healthy host -- a false positive indistinguishable from the defect.  So the sequence is
`dt`/`bf` for a fixed count, then a sentinel store, then a breakpoint that returns control.

    mov.w r0,@r1   store the RTCSR value
    dt    r5       decrement and test
    bf    -3       loop while non-zero
    mov.l r2,@r3   sentinel: proves the loop RAN TO COMPLETION
    nop            breakpoint sits here

*** THE SPIN COUNT WAS MEASURED, NOT CHOSEN, AND THE FIRST ATTEMPT AT THIS WITNESS FOUND
NOTHING. ***  At 0x60000 and 0x200000 iterations every arm survived -- the guest simply did
not run long enough in HOST time for one callback.  0x2000000 kills in about 0.2 s.  A
reproduction that finds nothing because it did not wait is not evidence of absence, and
the earlier numbers are recorded here so nobody re-derives them.

THE CONTROLS ARE WHAT MAKE THIS A MEASUREMENT.  C1 and C2 write the SAME REGISTER at the
SAME WIDTH with the SAME spin and the host LIVES, so the result reads "these BITS end the
host" rather than "this register does" or "a long free run does".  C2 is the sharper of
the two: RTCSR_CMF is a different bit of the same byte.  D1 proves the store reached the
DEVICE at all by reading the value back through the same decode.

*** A NOTE ON THE READ-BACK ROW, because getting it wrong cost a measurement here. ***
The first draft used opcode 0x6121 for `mov.w @r1,r2`.  That encoding is `mov.w @r2,r1` --
the operands reversed -- so it read an unrelated register and returned ZERO, which looks
exactly like "the store never landed".  The correct encoding is 0x6211.  This is the
hand-assembled-encoding trap this project has recorded four times: A WRONG REGISTER FIELD
YIELDS ZERO, AND ZERO IS THE VALUE A CARELESS ROW ACCEPTS AS MEANINGFUL.  D1 expects a
SMALL NON-ZERO value for exactly that reason.

THIS ASSERTS THE PRE-FIX SYMPTOM, so it is RED once the defect is gone, and it must NEVER
be wired into a gate -- `check_probe_wiring.py` treats a gated witness as a HARD failure.

usage:  sh4_rtcsr_witness.py <gxemul-binary> <landisk-kernel>
"""
import os
import sys

import sh4_pcic_probe as P

SH4_RTCSR = 0xff80001c          # thirdparty/sh4_bscreg.h:61   (16 bit)
RTCSR_CMF = 1 << 7              # :79
RTCSR_CMIE = 1 << 6             # :80
RTCSR_OVIE = 1 << 1             # :83

#  MEASURED: 0x60000 and 0x200000 are both too short -- every arm survives.  0x2000000
#  kills in ~0.2 s wall clock.  Left generous rather than trimmed to the edge, because a
#  spin tuned to the threshold turns a loaded host into a false green.
SPIN = 0x2000000

#  mov.w r0,@r1 ; dt r5 ; bf -3 ; mov.l r2,@r3 ; nop
OPS = [0x2101, 0x4510, 0x8BFD, 0x2322, 0x0009]
SENTINEL = 0x5a5a1234

EXPECT_ROWS = 8

rows = []


def row(name, ok, got, want):
    rows.append((name, bool(ok), got, want))
    print("  %-4s %s" % ("ok" if ok else "FAIL", name))
    if not ok:
        print("       got  %s\n       want %s" % (got, want))


def freerun(val, label, kw):
    """Store `val` to RTCSR, then run free for SPIN iterations."""
    return P.session(
        ["put w 0x%x, 0x%08x" % (P.DEST, P.POISON),
         "r0=0x%x" % val, "r1=0x%x" % SH4_RTCSR,
         "r5=0x%x" % SPIN, "r2=0x%x" % SENTINEL, "r3=0x%x" % P.DEST]
        + P.poke(OPS)
        + ["breakpoint add 0x%x" % (P.CODE + 8), "pc=0x%x" % P.CODE, "continue"],
        0, label, disasm_upto=0, **dict(kw, timeout=90))


def main():
    if len(sys.argv) != 3:
        print("usage:  sh4_rtcsr_witness.py <gxemul-binary> <landisk-kernel>")
        return 2
    b, k = sys.argv[1], sys.argv[2]
    kw = dict(binary=b, kernel=k)
    for p in (b, k):
        if not os.path.exists(p):
            print("OPERATIONAL FAILURE: %s does not exist (cwd=%s)" % (p, os.getcwd()))
            print("SH4RTCSR_WITNESS_FAIL")
            return 2

    #  ---- D1: the store reaches the DEVICE ------------------------------------------
    #  mov.w r0,@r1 ; mov.w @r1,r2 ; mov.l r2,@r3 ; nop   -- note 0x6211, see the header.
    buf, alive, st = P.session(
        ["put w 0x%x, 0x%08x" % (P.DEST, P.POISON),
         "r0=0x%x" % RTCSR_CMIE, "r1=0x%x" % SH4_RTCSR, "r3=0x%x" % P.DEST]
        + P.poke([0x2101, 0x6211, 0x2322, 0x0009]) + ["pc=0x%x" % P.CODE],
        3, "D1", disasm_upto=8, **kw)
    v = P.dumped(buf)
    row("D1 DEVICE: RTCSR reads back the CMIE bit just written (small NON-ZERO)",
        st and alive and v == P.le(RTCSR_CMIE),
        "started=%s alive=%s val=%s" % (st, alive, v),
        "val=%s -- a wrong register field would answer %s, which is why this row wants "
        "a non-zero" % (P.le(RTCSR_CMIE), P.le(0)))

    #  ---- S0: THE ROW THAT NAMES THE SHAPE ------------------------------------------
    #  *** THE STORE ITSELF IS HARMLESS, AND THAT IS THE POINT. ***  Every other SH-4
    #  probe in this tree would stop here and report the host healthy.
    buf, alive, st = P.write_arm(SH4_RTCSR, RTCSR_CMIE, "S0", kw, op=0x2101)
    row("S0 the STORE returns normally -- a store-site probe sees NOTHING wrong",
        st and alive,
        "started=%s alive=%s" % (st, alive),
        "alive: the handler stores and returns, so the defect is invisible to every "
        "probe shape this project has used on this device")

    #  ---- S1/S2: the DELAYED kills ---------------------------------------------------
    for name, val, bit in [("S1 CMIE 0x40", RTCSR_CMIE, "CMIE"),
                           ("S2 OVIE 0x02", RTCSR_OVIE, "OVIE")]:
        buf, alive, st = freerun(val, name.split()[0], kw)
        seen = "RTCSR_CMIE | RTCSR_OVIE" in (buf or "")
        row("%s KILLS the host from the 110 Hz callback, AFTER the store returned"
            % name,
            st and not alive and seen,
            "started=%s alive=%s diagnostic=%s" % (st, alive, seen),
            "started, NOT alive, and the timer's own diagnostic present (%s)" % bit)

    #  ---- C1/C2: same register, same width, same spin, and the host LIVES ------------
    for name, val in [("C1 CONTROL 0x00 -- no interrupt-enable bit", 0x00),
                      ("C2 CONTROL 0x80 -- RTCSR_CMF, a DIFFERENT bit of the same byte",
                       RTCSR_CMF)]:
        buf, alive, st = freerun(val, name.split()[0], kw)
        sent = P.dumped(buf)
        row("%s -- host SURVIVES the same free run" % name,
            st and alive and sent == P.le(SENTINEL),
            "started=%s alive=%s sentinel=%s" % (st, alive, sent),
            "alive AND sentinel=%s -- the sentinel proves the spin RAN TO COMPLETION, so "
            "'survived' is not 'never ran'" % P.le(SENTINEL))

    #  ---- W0 / identity ---------------------------------------------------------------
    n_ses = len(P.STARTS)
    n_ok = sum(1 for _, s in P.STARTS if s)
    row("W0 EVERY session reached the debugger prompt (absent data must FAIL)",
        n_ses > 0 and n_ok == n_ses,
        "sessions=%d started=%d" % (n_ses, n_ok), "all %d started" % n_ses)

    row("W-id IDENTITY row count -- guards against a stale copy",
        len(rows) + 1 == EXPECT_ROWS, len(rows) + 1, EXPECT_ROWS)

    bad = sum(1 for _, ok, _, _ in rows if not ok)
    print()
    print("SH4RTCSR_WITNESS_RESULT=%d/%d" % (len(rows) - bad, len(rows)))
    print("SH4RTCSR_WITNESS_PASS" if bad == 0 else "SH4RTCSR_WITNESS_FAIL")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
