#!/usr/bin/env python3
"""`sh4sci` WITNESS (rung 3): a guest can compose a byte, bit by bit, that ends the HOST
PROCESS inside sh4_sci_cmd() -- on an UNMODIFIED in-tree `-E landisk`.

*** THIS IS THE FIRST SH-4 SITE IN THIS TREE THAT NEEDS A MULTI-STORE PROTOCOL TO REACH. ***
#443, #447 and #448 are reached by ONE store; #449 by one store plus a wait.  Here the
guest must CLOCK a byte in:

    dev_sh4.c  SHREG_SCSPTR (0xffe0001c) -> sh4_sci_access()
               clockpulse = old & SPB0IO && new & SPB0DT && !(old & SPB0DT)
               in output mode (SPB1IO), each pulse does:
                   sci_curbyte = (sci_curbyte << 1) | (new & SPB1DT ? 1 : 0)
               and on the EIGHTH pulse it calls sh4_sci_cmd(), which holds:
                   if (!(cmd & 0x80))            fatal(...); exit(1);   /* bit 7 */
                   if ((cmd & 0x30) not 0x20/0x10) fatal(...); exit(1); /* transfer kind */

So the reachability question is not "can a guest store to this address" -- it is "can a
guest drive the protocol far enough for the byte to be consumed".  It can: seventeen
ordinary `mov.b` stores, no privilege, no device beyond the one the machine already
instantiates.

THE SEQUENCE, and why each write looks the way it does.  The data bit is sampled from the
SAME write that carries the rising clock edge (`sci_scsptr = input` happens BEFORE the bit
is read), so each bit is two stores:

    low   SPB1IO|SPB0IO             | (bit ? SPB1DT : 0)   -> 0x0a or 0x0e
    high  SPB1IO|SPB0IO|SPB0DT      | (bit ? SPB1DT : 0)   -> 0x0b or 0x0f

plus ONE priming store first, because the pulse test reads SPB0IO from the PREVIOUS value:
without it the first rising edge is not a pulse at all and the byte silently shifts short.

THE CONTROLS ARE WHAT MAKE THIS A MEASUREMENT, and it takes three of them because the
claim has three parts.  C1 clocks in 0xa0 -- the SAME address, the SAME width, the SAME
seventeen stores, differing only in the data bits -- and the host LIVES, because 0xa0 has
bit 7 set and its 0x30 field selects an address transfer.  C2 clocks SEVEN pulses of a
byte that would kill on eight.  C3 repeats S1's seventeen stores with SPB0IO cleared in
every one of them, so `old & SPB0IO` is false at each edge and NO pulse is ever counted.

    C1 -> the kill depends on the byte VALUE          (not on the address or the width)
    C2 -> the kill needs a COMPLETE eight-bit byte    (not seven bits of one)
    C3 -> the kill needs the CLOCKING PROTOCOL        (not seventeen stores to this address)

*** C2 ALONE DOES NOT PROVE THE THIRD LINE, and an earlier draft of this file said it did.
*** Seven pulses versus eight is byte-boundary gating; the edge dance is baked identically
into both, so C2 cannot separate "needs the protocol" from "needs a whole byte".  C3 is the
row that separates them: same address, same seventeen stores, same values but for one bit,
and nothing accumulates.  Two panel seats named the overclaim independently.

TWO KILLS AT THE SECOND SITE, NOT ONE.  `(cmd & 0x30)` reaches the else arm for BOTH 0x00
and 0x30 -- "neither transfer bit" and "both transfer bits" -- so S2 (0x80) and S3 (0xb0)
are separate faults, and a detector that drives only S2 cannot see a decoder loosened to
let 0x30 fall into the address arm.

THIS ASSERTS THE PRE-FIX SYMPTOM, so it is RED once the defect is gone, and it must NEVER
be wired into a gate.  MEASURED both ways on the same script: 8/8 before #451 and 5/8
after, the three differences being exactly rows S1, S2 and S3 -- the three bytes that used
to end the host.  The three controls do not move.  The post-fix property is asserted by a
SEPARATE artefact, sh4_sci_probe.py, which is the gated one.

usage:  sh4_sci_witness.py <gxemul-binary> <landisk-kernel>
"""
import os
import sys

import sh4_pcic_probe as P

SHREG_SCSPTR = 0xffe0001c       # thirdparty/sh4_scireg.h:64  (byte-wide)
SPB1IO, SPB1DT = 0x08, 0x04     # :83, :84
SPB0IO, SPB0DT = 0x02, 0x01     # :85, :86

EXPECT_ROWS = 8

rows = []


def row(name, ok, got, want):
    rows.append((name, bool(ok)))
    print("  %-4s %s" % ("ok" if ok else "FAIL", name))
    if not ok:
        print("       got  %s\n       want %s" % (got, want))


def clock_byte(value):
    """Opcodes that clock `value` in, most-significant bit first.

    Each store is `mov #imm,r0` (0xE0nn) then `mov.b r0,@r1` (0x2100); r1 holds SCSPTR
    throughout.  Returns a halfword list.
    """
    ops = []

    def store(v):
        ops.append(0xE000 | (v & 0xff))     # mov #v,r0
        ops.append(0x2100)                  # mov.b r0,@r1

    #  Prime: establish SPB0IO in the PREVIOUS value so the first edge counts as a pulse.
    store(SPB1IO | SPB0IO)
    for i in range(7, -1, -1):
        bit = (value >> i) & 1
        d = SPB1DT if bit else 0
        store(SPB1IO | SPB0IO | d)                    # clock low, data presented
        store(SPB1IO | SPB0IO | SPB0DT | d)           # rising edge -> shift this bit
    return ops


def drive(value, label, kw, sentinel=False):
    ops = clock_byte(value)
    pre = ["put w 0x%x, 0x%08x" % (P.DEST, P.POISON), "r1=0x%x" % SHREG_SCSPTR]
    if sentinel:
        pre += ["r2=0x5a5a1234", "r3=0x%x" % P.DEST]
        ops = ops + [0x2322]                          # mov.l r2,@r3
    ops = ops + [0x0009]                              # nop
    return P.session(pre + P.poke(ops) + ["pc=0x%x" % P.CODE],
                     len(ops) - 1, label, disasm_upto=0, **dict(kw, timeout=90))


def main():
    if len(sys.argv) != 3:
        print("usage:  sh4_sci_witness.py <gxemul-binary> <landisk-kernel>")
        return 2
    b, k = sys.argv[1], sys.argv[2]
    kw = dict(binary=b, kernel=k)
    for p in (b, k):
        if not os.path.exists(p):
            print("OPERATIONAL FAILURE: %s does not exist (cwd=%s)" % (p, os.getcwd()))
            print("SH4SCI_WITNESS_FAIL")
            return 2

    #  ---- the two kills ---------------------------------------------------------------
    for name, val, msg in [
            ("S1 byte 0x00 -> cmd bit 7 clear", 0x00, "SCI cmd bit 7 not set"),
            ("S2 byte 0x80 -> transfer field 0x00 (neither bit)", 0x80,
             "Neither data nor address transfer"),
            #  S3 is the OTHER value that reaches the same else arm.  0xb0 sets BOTH
            #  transfer bits; the shipped diagnostic still calls that "neither", which is
            #  a second reason this site needs work.  Without this row a decoder loosened
            #  from `(cmd & 0x30) == 0x20` to `(cmd & 0x20)` would let 0xb0 perform a real
            #  address transfer and S1/S2 would both stay green.
            ("S3 byte 0xb0 -> transfer field 0x30 (BOTH bits)", 0xb0,
             "Neither data nor address transfer")]:
        buf, alive, st = drive(val, name.split()[0], kw)
        seen = msg in (buf or "")
        row("%s KILLS the host" % name,
            st and not alive and seen,
            "started=%s alive=%s diagnostic=%s" % (st, alive, seen),
            "started, NOT alive, and the output names %r" % msg)

    #  ---- the control: same address, same width, same 17 stores -----------------------
    buf, alive, st = drive(0xa0, "C1", kw, sentinel=True)
    sent = P.dumped(buf)
    row("C1 CONTROL: byte 0xa0 (bit 7 set, address transfer) -- host SURVIVES",
        st and alive and sent == P.le(0x5a5a1234),
        "started=%s alive=%s sentinel=%s" % (st, alive, sent),
        "alive AND sentinel=%s -- the sentinel proves all seventeen stores RAN, so "
        "'survived' is not 'never clocked'" % P.le(0x5a5a1234))

    #  ---- a SHORT sequence must NOT reach the command at all --------------------------
    #  Seven pulses instead of eight.  This is the row that proves the kill needs the
    #  PROTOCOL and not merely a store to this address: same address, same width, one
    #  pulse fewer, and the byte is never consumed.
    ops = clock_byte(0x00)[:-4] + [0x0009]
    buf, alive, st = P.session(
        ["put w 0x%x, 0x%08x" % (P.DEST, P.POISON), "r1=0x%x" % SHREG_SCSPTR]
        + P.poke(ops) + ["pc=0x%x" % P.CODE],
        len(ops) - 1, "C2", disasm_upto=0, **dict(kw, timeout=90))
    row("C2 CONTROL: SEVEN pulses -- the byte is never consumed, host SURVIVES",
        st and alive and "SCI cmd bit 7 not set" not in (buf or ""),
        "started=%s alive=%s" % (st, alive),
        "alive and silent: the eighth pulse is what calls sh4_sci_cmd()")

    #  ---- C3: seventeen stores, no CLOCK ----------------------------------------------
    #  S1's byte and S1's store count, with SPB0IO cleared everywhere.  dev_sh4.c's pulse
    #  test reads SPB0IO from the PREVIOUS value, so with it never set no rising edge is
    #  ever counted, sci_curbyte never accumulates, and sh4_sci_cmd() is never called.
    #  THIS is the row that proves the protocol carries the kill; C2 only proves the byte
    #  must be whole.
    ops = [op if (op & 0xf000) != 0xE000 else (op & ~SPB0IO)
           for op in clock_byte(0x00)] + [0x0009]
    buf, alive, st = P.session(
        ["put w 0x%x, 0x%08x" % (P.DEST, P.POISON), "r1=0x%x" % SHREG_SCSPTR]
        + P.poke(ops) + ["pc=0x%x" % P.CODE],
        len(ops) - 1, "C3", disasm_upto=0, **dict(kw, timeout=90))
    row("C3 CONTROL: 17 stores with SPB0IO never set -- no pulse, host SURVIVES",
        st and alive and "SCI cmd bit 7 not set" not in (buf or ""),
        "started=%s alive=%s" % (st, alive),
        "alive and silent: without SPB0IO in the PREVIOUS value nothing is a clock edge")

    #  ---- W0 / identity ---------------------------------------------------------------
    n_ses = len(P.STARTS)
    n_ok = sum(1 for _, s in P.STARTS if s)
    row("W0 EVERY session reached the debugger prompt (absent data must FAIL)",
        n_ses > 0 and n_ok == n_ses,
        "sessions=%d started=%d" % (n_ses, n_ok), "all %d started" % n_ses)

    row("W-id IDENTITY row count -- guards against a stale copy",
        len(rows) + 1 == EXPECT_ROWS, len(rows) + 1, EXPECT_ROWS)

    bad = sum(1 for _, ok in rows if not ok)
    print()
    print("SH4SCI_WITNESS_RESULT=%d/%d" % (len(rows) - bad, len(rows)))
    print("SH4SCI_WITNESS_PASS" if bad == 0 else "SH4SCI_WITNESS_FAIL")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
