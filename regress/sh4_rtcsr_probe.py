#!/usr/bin/env python3
"""#449 DETECTOR: a guest RTCSR refresh-interrupt enable is DIAGNOSED ONCE PER BIT and the
host SURVIVES -- and the enable is still readable back, and legal bits stay silent.

Rung 3.  Real SH-4 guest instructions through real address decode, real `memory_rw` and
real device dispatch, on an UNMODIFIED in-tree `-E landisk`.

THE DEFECT (witnessed by `sh4_rtcsr_witness.py`, 8/8 on the pre-fix build, 6/8 after).
`sh4_timer_tick()` read `bsc_rtcsr` and called `exit(1)`.  The write itself lands and
RETURNS NORMALLY; the process dies about nine milliseconds later, from a 110 Hz host timer
callback.  *** EVERY OTHER SH-4 PROBE IN THIS TREE WATCHES THE STORE SITE AND IS BLIND TO
THAT BY CONSTRUCTION. ***  The witness keeps row S0 for exactly that reason.

*** F1 IS THE ROW THIS FILE EXISTS FOR, AND IT COULD NOT BE WRITTEN FOR ANY EARLIER ROUND.
***  The diagnostic here is emitted from a callback that fires at SH4_PSEUDO_TIMER_HZ, and
`timer.c` can burst several ticks inside one signal.  `fatal()` has NO quiet_mode
early-out, so an unlatched complaint is a flood that `-q` cannot stop.  F1 runs the guest
free for long enough that the callback fires MANY times and requires EXACTLY ONE line.  A
store-site row cannot measure that: it never lets the callback run twice.

THE ACCEPT-SIDE ROWS (A1-A3) ARE THE DE-ESCALATION CLAUSE.  A flagship adjudication
established it: a fatal->survive fix DELETES the accidental tripwire that made guard growth
self-announcing, so the detector must pin that legal values stay SILENT, not merely that
illegal ones are diagnosed.  Widen the guard to include RTCSR_CMF and A1 reddens.

A3 IS THE ROW A REVIEW SEAT ASKED FOR BY NAME.  The tempting fix from #447 -- mask the
offending bits out of the store -- is WRONG for this register.  RTCSR is MIXED: CKS, LMTS
and the CMF write-0-to-clear share the byte, so stripping the enables would refuse
clock-select bits too, and would leave the tick guard permanently false and any surviving
`exit(1)` in it a latent bomb no free-run row could reach.  A3 requires the enable to be
READABLE BACK, so that fix design fails loudly instead of looking clean.

WHAT IS NOT CLAIMED, and a seat checked each of these against the header:
  * CMF and OVF are NEVER set by this device, on any path, and this round does not start
    setting them -- that would invent a compare-match without an RTCNT to match against.
    A guest polling CMF already waits forever with the enables CLEAR; this fix does not
    change that, it only lets a guest with them SET survive to wait.  Filed as `sh4rtcflags`.
  * RTCNT (`0xff800020`) has NO `case` in this device at all.  Filed with it.

usage:  sh4_rtcsr_probe.py <gxemul-binary> <landisk-kernel>
"""
import os
import re
import sys

import sh4_pcic_probe as P

SH4_RTCSR = 0xff80001c          # thirdparty/sh4_bscreg.h:61   (16 bit)
RTCSR_CMF = 1 << 7              # :79
RTCSR_CMIE = 1 << 6             # :80
RTCSR_OVIE = 1 << 1             # :83
RTCSR_CKS = 0x0038              # :80   clock select, three ordinary storable bits
RTCSR_LMTS = 1 << 0             # :83   refresh-count limit select

#  MEASURED while writing the witness: 0x60000 and 0x200000 iterations are too short for
#  even ONE 110 Hz tick, so a probe using them would report every arm healthy.  0x2000000
#  is comfortably several ticks.
SPIN = 0x2000000

#  mov.w r0,@r1 ; dt r5 ; bf -3 ; mov.l r2,@r3 ; nop
OPS = [0x2101, 0x4510, 0x8BFD, 0x2322, 0x0009]
SENTINEL = 0x5a5a1234

#  The wording changed in pass 2 (see the source comment): "the interrupt is NOT
#  delivered" implied something becomes pending and is dropped, and nothing ever does.
DIAG_RE = re.compile(r"\[ sh4: refresh interrupt enable\(s\) 0x[0-9a-f]{2} stored,"
                     r" but refresh-interrupt generation is not implemented[^\]]*\]")

EXPECT_ROWS = 10

rows = []


def row(name, ok, got, want):
    rows.append((name, bool(ok), got, want))
    print("  %-4s %s" % ("ok" if ok else "FAIL", name))
    if not ok:
        print("       got  %s\n       want %s" % (got, want))


def diags(txt):
    return DIAG_RE.findall(txt or "")


def freerun(val, label, kw, spin=SPIN):
    return P.session(
        ["put w 0x%x, 0x%08x" % (P.DEST, P.POISON),
         "r0=0x%x" % val, "r1=0x%x" % SH4_RTCSR,
         "r5=0x%x" % spin, "r2=0x%x" % SENTINEL, "r3=0x%x" % P.DEST]
        + P.poke(OPS)
        + ["breakpoint add 0x%x" % (P.CODE + 8), "pc=0x%x" % P.CODE, "continue"],
        0, label, disasm_upto=0, **dict(kw, timeout=120))


def main():
    if len(sys.argv) != 3:
        print("usage:  sh4_rtcsr_probe.py <gxemul-binary> <landisk-kernel>")
        return 2
    b, k = sys.argv[1], sys.argv[2]
    kw = dict(binary=b, kernel=k)
    for p in (b, k):
        if not os.path.exists(p):
            print("OPERATIONAL FAILURE: %s does not exist (cwd=%s)" % (p, os.getcwd()))
            print("SH4RTCSR_RESULT=0/%d" % EXPECT_ROWS)
            print("SH4RTCSR_FAIL")
            return 2

    #  ---- R1/R2: the host SURVIVES, and says so once --------------------------------
    for name, val, want in [("R1 CMIE 0x40", RTCSR_CMIE, "0x40"),
                            ("R2 OVIE 0x02", RTCSR_OVIE, "0x02")]:
        buf, alive, st = freerun(val, name.split()[0], kw)
        d = diags(buf)
        sent = P.dumped(buf)
        row("%s -- host SURVIVES the free run, EXACTLY ONE diagnostic" % name,
            st and alive and len(d) == 1 and want in d[0] and sent == P.le(SENTINEL),
            "alive=%s lines=%d sentinel=%s %s" % (alive, len(d), sent, d),
            "alive, one line naming %s, and sentinel=%s proving the spin RAN"
            % (want, P.le(SENTINEL)))

    #  ---- R3: both enables in ONE store -> ONE line, and it names both ---------------
    buf, alive, st = freerun(RTCSR_CMIE | RTCSR_OVIE, "R3", kw)
    d = diags(buf)
    row("R3 BOTH enables in one store -> ONE line naming 0x42",
        st and alive and len(d) == 1 and "0x42" in d[0],
        "alive=%s lines=%d %s" % (alive, len(d), d),
        "one line naming 0x42 -- the latch takes a BIT SET, so one store that sets two "
        "fresh bits is one complaint, not two")

    #  ---- F1: THE FLOOD ROW.  This is the point of the file. ------------------------
    #  *** THE CALLBACK FIRES MANY TIMES DURING THIS SPIN. ***  An unlatched fatal() would
    #  print a line per tick at 110 Hz, and -q could not stop it because fatal() has no
    #  quiet_mode early-out.  Requiring EXACTLY ONE line over a multi-tick free run is a
    #  measurement no store-site row can make: those never let the callback run twice.
    buf, alive, st = freerun(RTCSR_CMIE, "F1", kw, spin=SPIN * 4)
    d = diags(buf)
    row("F1 FLOOD: many 110 Hz ticks with the enable set -> still EXACTLY ONE line",
        st and alive and len(d) == 1,
        "alive=%s lines=%d" % (alive, len(d)),
        "exactly ONE over a spin four times longer than R1's -- more than one means the "
        "latch is not holding across ticks, which is an unsilenceable flood")

    #  ---- L1: THE LATCH KEY, and it needs TWO STORES IN ONE PROCESS ------------------
    #  *** EVERY ROW ABOVE IS ITS OWN SESSION, SO THE LATCH IS FRESH EACH TIME AND NONE OF
    #  THEM CAN SEE THE BIT SUB-KEY. ***  A mutant passing a constant instead of the
    #  offending bits scored a clean 9/9 against R1-R3, F1 and A1-A3 -- measured, not
    #  supposed.  #448 hit the identical shape and closed it the same way.
    #  CMIE first, then OVIE: two distinct features, so a correct latch says it TWICE.
    #  *** THERE ARE TWO SPINS, AND THE FIRST DRAFT HAD ONLY ONE AND WAS FLAKY. ***  With
    #  a single spin the OVIE store is followed IMMEDIATELY by the sentinel and the
    #  breakpoint, so the second diagnostic appears only if a 110 Hz tick happens to race
    #  into that gap.  It passed once and failed once on the SAME binary -- caught because
    #  the mutation run scores the clean tree too.  An intermittent row is worse than a
    #  wrong one: this project's record is that an intermittent check gets ignored, and
    #  then disabled.  The second spin makes a tick certain after EACH store.
    buf, alive, st = P.session(
        ["put w 0x%x, 0x%08x" % (P.DEST, P.POISON),
         "r0=0x%x" % RTCSR_CMIE, "r4=0x%x" % RTCSR_OVIE, "r1=0x%x" % SH4_RTCSR,
         "r5=0x%x" % SPIN, "r6=0x%x" % SPIN, "r2=0x%x" % SENTINEL, "r3=0x%x" % P.DEST]
        #  mov.w r0,@r1 ; dt r5 ; bf -3 ; mov.w r4,@r1 ; dt r6 ; bf -3 ;
        #  mov.l r2,@r3 ; nop
        + P.poke([0x2101, 0x4510, 0x8BFD, 0x2141, 0x4610, 0x8BFD, 0x2322, 0x0009])
        + ["breakpoint add 0x%x" % (P.CODE + 14), "pc=0x%x" % P.CODE, "continue"],
        0, "L1", disasm_upto=0, **dict(kw, timeout=180))
    d = diags(buf)
    row("L1 LATCH: CMIE then OVIE in ONE process -> TWO lines",
        st and alive and len(d) == 2,
        "alive=%s lines=%d %s" % (alive, len(d), d),
        "exactly TWO -- one means the latch dropped the BIT sub-key and is silencing a "
        "second unimplemented feature the guest has not been told about")

    #  ---- A1/A2: THE ACCEPT SIDE.  The de-escalation clause. ------------------------
    #  *** A1 USED RTCSR_CMF AND WAS MEASURED VACUOUS. ***  CMF is WRITE-1-TO-KEEP: the
    #  store arm replaces a written 1 with the CURRENT CMF, and nothing in this device ever
    #  sets CMF on any path -- so a guest CANNOT set it, the accept row could never trip a
    #  widened guard, and a mutant adding CMF to the mask is EQUIVALENT rather than
    #  surviving.  CKS (clock select, 0x38) and LMTS (0x01) are ordinary storable bits and
    #  are what the row needs: legal, guest-settable, and nothing to do with an interrupt.
    for name, val in [("A1 ACCEPT: CKS|LMTS (0x39) are legal storable bits -- SILENT",
                       RTCSR_CKS | RTCSR_LMTS),
                      ("A2 ACCEPT: RTCSR 0x00 -- SILENT", 0x00)]:
        buf, alive, st = freerun(val, name.split()[0], kw)
        d = diags(buf)
        row(name, st and alive and len(d) == 0,
            "alive=%s lines=%d %s" % (alive, len(d), d),
            "alive and NO diagnostic -- a complaint here means the guard mask GREW to "
            "cover a bit it does not model an interrupt for")

    #  ---- A3: the enable is STORED, not masked away ---------------------------------
    #  mov.w r0,@r1 ; mov.w @r1,r2 ; mov.l r2,@r3 ; nop
    #  *** THE ENCODING IS 0x6211 AND NOT 0x6121. ***  0x6121 is `mov.w @r2,r1` -- the
    #  operands reversed -- which reads an unrelated register and answers ZERO.  That cost
    #  a measurement while this round's witness was written, and zero is exactly the value
    #  a careless row accepts.  This row wants a small NON-ZERO for that reason.
    buf, alive, st = P.session(
        ["put w 0x%x, 0x%08x" % (P.DEST, P.POISON),
         "r0=0x%x" % RTCSR_CMIE, "r1=0x%x" % SH4_RTCSR, "r3=0x%x" % P.DEST]
        + P.poke([0x2101, 0x6211, 0x2322, 0x0009]) + ["pc=0x%x" % P.CODE],
        3, "A3", disasm_upto=8, **kw)
    v = P.dumped(buf)
    row("A3 the enable is STORED and readable back -- the write is NOT masked away",
        st and alive and v == P.le(RTCSR_CMIE),
        "started=%s alive=%s val=%s" % (st, alive, v),
        "val=%s.  RTCSR is a MIXED register -- CKS, LMTS and the CMF write-0-to-clear "
        "share the byte -- so the #447 'strip the bits at the store' design would refuse "
        "clock-select too, and would leave the tick guard permanently false" % P.le(RTCSR_CMIE))

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
    print("SH4RTCSR_RESULT=%d/%d" % (len(rows) - bad, len(rows)))
    print("SH4RTCSR_PASS" if bad == 0 else "SH4RTCSR_FAIL")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
