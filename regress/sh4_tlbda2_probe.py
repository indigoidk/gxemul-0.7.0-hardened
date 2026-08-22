#!/usr/bin/env python3
"""`#452` DETECTOR: an access to a TLB data array 2 is CONSUMED with a defined result --
it does not end the host, and it does not touch array 1.

This is the detector, not the witness.  sh4_tlbda2_witness.py asserts the PRE-FIX symptom
(three guest accesses that killed the host) and is RED now that they do not; this file
asserts the post-fix property and must stay green.

*** WHY "THE HOST SURVIVED" IS NOT THE PROPERTY. ***  This fix deletes two exit(1) calls,
and with them the tripwire that made a mistake in these handlers loud.  Afterwards a wrong
returned value, a corrupted array-1 entry and a silenced second site all look identical to a
liveness check.

A mutant the rows deliberately do NOT chase, recorded because three seats predicted it and
the measurement refuted them: dropping the `memory_writemax64(cpu, data, len, 0)` call on the
declined-read path.  The prediction was that the guest then receives stale host bytes.  It
does not.  memory_rw.c:484-491 -- correction #95 in this same tree -- zeroes the caller's
buffer before EVERY device read, as the root-cause fix for that exact class.  Measured in
five contexts (bare read; primed by an array-1 read; destination register pre-set to
0xdeadbeef; primed through RAM; primed through the OTHER TLB device): all returned 0 on the
mutant and on the fix alike.  It is an EQUIVALENT mutant, so no row here can kill it, and a
row written as though it could would be decoration.

What R1/R2 DO pin is that the declined read returns 0 rather than some other definite value:
a handler returning `mask` instead reddens R1.  R3 pins the mutant that survives everything
else -- deleting the early `return 1`, so the declined access falls through into the array-1
body where `e` comes from the same masked bits, letting a guest probing array 2 read and
WRITE real translation entries.

THE ROWS, and which mutant each exists to kill.  The ones marked (*) survive a detector
built the obvious way.

  R1  itlb: the da2 read returns EXACTLY 0, not some other definite value.
                  Kills a handler that answers `mask`.  It does NOT kill a dropped
                  memory_writemax64() -- that mutant is equivalent, see above.
  R2  utlb: the same.
  R3  itlb: STORE to da2, then read da1 -- the entry must be UNCHANGED.              (*)
                  Kills the missing `return 1`, which aliases array 2 onto array 1.
  X   BOTH sites in ONE session -- both diagnostics must appear.                     (*)
                  The offending quantity is `relative_addr & 0x800000`, the SAME value
                  at both sites, so a key derived from it lets whichever site complains
                  first silence the other for the device lifetime.  A review seat named
                  that collision before the edit was written.
  RPT one site twice -- exactly ONE line.
  A1  ACCEPT itlb array 1 at offset 0 -- EXACTLY 0x1ffffdfa.
  A2  ACCEPT utlb array 1 at offset 0 -- EXACTLY 0x1ffffdff.
  A3  ACCEPT array 1 at offset 0x400000 -- bit 22 SET, bit 23 clear.                 (*)
                  The de-escalation accept row.  The predicate that used to gate death
                  was `relative_addr & 0x800000`; the smallest realistic growth is
                  `& 0xc00000`, which starts refusing legal array-1 addresses from
                  0x400000 up.  A1/A2 sit at offset 0 and cannot see that.
  O   the array-1 oracle is LIVE -- without it the "reads 0" rows prove nothing.
  I   identity: row count.

usage:  sh4_tlbda2_probe.py <gxemul-binary> <landisk-kernel>
"""
import os
import re
import sys

import sh4_pcic_probe as P

ITLB_DA1 = 0xf3000000           # thirdparty/sh4_mmu.h:103
UTLB_DA1 = 0xf7000000           # thirdparty/sh4_mmu.h:133
DA2 = 0x800000

#  Spelled from sh4_mmu.h:49-60, the same constants the handlers OR together.  The two
#  masks DIFFER (utlb adds WT|D), so these values are per-device signatures.
_WT, _SH, _D, _C = 0x00000001, 0x00000002, 0x00000004, 0x00000008
_PR, _SZ, _V = 0x00000060, 0x00000090, 0x00000100
ITLB_MASK = _SH | _C | _SZ | _PR | _V | 0x1ffffc00               # 0x1ffffdfa
UTLB_MASK = _WT | _SH | _D | _C | _SZ | _PR | _V | 0x1ffffc00    # 0x1ffffdff

DECL_RE = re.compile(r"sh4: (ITLB|UTLB) data array 2 \(0x([0-9a-f]{8})\)")

EXPECT_ROWS = 15

rows = []


def row(name, ok, got, want):
    rows.append((name, bool(ok)))
    print("  %-4s %s" % ("ok" if ok else "FAIL", name))
    if not ok:
        print("       got  %s\n       want %s" % (got, want))


def run(ops, regs, label, kw):
    """One cold-debugger session.  Returns (readback, alive, started, declines)."""
    ops = list(ops) + [0x0009]
    buf, alive, st = P.session(
        ["put w 0x%x, 0x%08x" % (P.DEST, P.POISON)]
        + ["%s=0x%x" % (r, v) for r, v in regs]
        + P.poke(ops) + ["pc=0x%x" % P.CODE],
        len(ops) - 1, label, disasm_upto=0, **dict(kw, timeout=90))
    return (P.dumped(buf), alive, st, DECL_RE.findall(buf or ""))


#  Opcodes.  0x2402 and 0x6242 were CHECKED against the emulator's own disassembler in a
#  session that printed them, because a wrong register field is silent -- it yields 0,
#  which a "reads as zero" row accepts by accident.  That trap has been recorded five
#  times in this project.
ST_R0_AT_R1 = 0x2102        # mov.l r0,@r1
ST_R0_AT_R4 = 0x2402        # mov.l r0,@r4
LD_R1_TO_R2 = 0x6212        # mov.l @r1,r2
LD_R4_TO_R2 = 0x6242        # mov.l @r4,r2
ST_R2_AT_R3 = 0x2322        # mov.l r2,@r3


def main():
    if len(sys.argv) != 3:
        print("usage:  sh4_tlbda2_probe.py <gxemul-binary> <landisk-kernel>")
        return 2
    b, k = sys.argv[1], sys.argv[2]
    kw = dict(binary=b, kernel=k)
    for p in (b, k):
        if not os.path.exists(p):
            print("OPERATIONAL FAILURE: %s does not exist (cwd=%s)" % (p, os.getcwd()))
            print("SH4TLBDA2_RESULT=0/%d" % EXPECT_ROWS)
            print("SH4TLBDA2_FAIL")
            return 2

    #  ---- R1 / R2: the declined read is 0, and the buffer was PRIMED non-zero ---------
    for nm, base, mask, tag in [("R1 itlb", ITLB_DA1, ITLB_MASK, "ITLB"),
                                ("R2 utlb", UTLB_DA1, UTLB_MASK, "UTLB")]:
        got, alive, st, dec = run(
            [ST_R0_AT_R1,       # array 1 <- 0xffffffff
             LD_R1_TO_R2,       # r2 <- array 1  (large, non-zero -- primes the path)
             LD_R4_TO_R2,       # r2 <- array 2  (must be 0)
             ST_R2_AT_R3],
            [("r0", 0xffffffff), ("r1", base), ("r4", base | DA2), ("r3", P.DEST)],
            nm.split()[0], kw)
        row("%s da2 read returns EXACTLY 0 and raises exactly one %s decline" % (nm, tag),
            st and alive and got == P.le(0) and [t for t, _ in dec] == [tag],
            "alive=%s readback=%s declines=%s" % (alive, got, dec),
            "readback 0 and exactly one %s decline.  NOTE the array-1 access earlier in "
            "this session is NOT observed: its result lands in r2 and the da2 load "
            "overwrites it before anything stores r2.  Two seats caught an earlier "
            "version of this row CLAIMING that value in its name.  Array 1 is proved to "
            "work by A1/A2/O, in their own sessions" % tag)

    #  ---- R3: a da2 STORE must not reach array 1 --------------------------------------
    got, alive, st, dec = run(
        [ST_R0_AT_R1,           # array 1 <- 0xffffffff  -> reads back as the mask
         0xE000,                # mov #0,r0
         ST_R0_AT_R4,           # array 2 <- 0           (declined; must change nothing)
         LD_R1_TO_R2,           # r2 <- array 1
         ST_R2_AT_R3],
        [("r0", 0xffffffff), ("r1", ITLB_DA1), ("r4", ITLB_DA1 | DA2), ("r3", P.DEST)],
        "R3", kw)
    row("R3 an ITLB da2 STORE leaves the da1 entry UNCHANGED",
        st and alive and got == P.le(0xffffffff & ITLB_MASK) and [t for t, _ in dec] == ["ITLB"],
        "alive=%s da1-readback=%s declines=%s" % (alive, got, dec),
        "da1 still reads 0x%08x AND the store raised its decline line.  An earlier "
        "version checked only the readback; a seat pointed out the decline was named in "
        "the message and never asserted" % (0xffffffff & ITLB_MASK))

    #  ---- R3u: the SAME row at the OTHER site, and it is not redundant ----------------
    #  A seat found that R3, RPT and A3 were ALL built on ITLB, so three already-known
    #  mutants had an uncovered UTLB copy.  The sharpest is a WRITE-ONLY fallthrough --
    #  moving `return 1` inside the MEM_READ arm -- which is read-clean and therefore
    #  invisible to every read row, while a da2 STORE lands in utlb_lo[e] for the same
    #  entry array 1 just used.  This is #451's pass-2 lesson mirrored: there the FIRST
    #  site was under-exercised, here the second.
    got, alive, st, dec = run(
        [ST_R0_AT_R1, 0xE000, ST_R0_AT_R4, LD_R1_TO_R2, ST_R2_AT_R3],
        [("r0", 0xffffffff), ("r1", UTLB_DA1), ("r4", UTLB_DA1 | DA2), ("r3", P.DEST)],
        "R3u", kw)
    row("R3u a UTLB da2 STORE leaves the da1 entry UNCHANGED",
        st and alive and got == P.le(0xffffffff & UTLB_MASK) and [t for t, _ in dec] == ["UTLB"],
        "alive=%s da1-readback=%s declines=%s" % (alive, got, dec),
        "da1 still reads 0x%08x.  A write-only fallthrough at THIS site passes every "
        "read row in this file" % (0xffffffff & UTLB_MASK))

    #  ---- R4: a declined address that is NOT the base ---------------------------------
    #  Every other decline row uses exactly +0x800000, so a guard narrowed from `&` to
    #  `== 0x800000` declines that one address and silently ALIASES the rest of array 2
    #  onto array 1.  MEASURED at 10/10 before this row existed.
    got, alive, st, dec = run(
        [ST_R0_AT_R1, LD_R1_TO_R2, ST_R2_AT_R3],
        [("r0", 0xffffffff), ("r1", ITLB_DA1 + 0x800100), ("r3", P.DEST)],
        "R4", kw)
    row("R4 a da2 address that is NOT the base (+0x800100) still declines",
        st and alive and got == P.le(0) and [t for t, _ in dec] == ["ITLB"],
        "alive=%s readback=%s declines=%s" % (alive, got, dec),
        "declined, reading 0.  A guard narrowed to `== 0x800000` passes every other row "
        "in this file while aliasing all the rest of array 2 onto array 1")

    #  ---- X: both sites in ONE session ------------------------------------------------
    got, alive, st, dec = run(
        [LD_R1_TO_R2, LD_R4_TO_R2, ST_R2_AT_R3],
        [("r1", ITLB_DA1 | DA2), ("r4", UTLB_DA1 | DA2), ("r3", P.DEST)],
        "X", kw)
    row("X BOTH sites in one session -- both diagnostics print (keys do not alias)",
        st and alive and [t for t, _ in dec] == ["ITLB", "UTLB"],
        "alive=%s declines=%s" % (alive, dec),
        "one ITLB line and one UTLB line.  The offending value is the SAME at both "
        "sites, so a key derived from the address silences whichever reports second")

    #  ---- RPT: one site twice, one line -----------------------------------------------
    got, alive, st, dec = run(
        [LD_R1_TO_R2, LD_R4_TO_R2, ST_R2_AT_R3],
        [("r1", ITLB_DA1 | DA2), ("r4", ITLB_DA1 | DA2), ("r3", P.DEST)],
        "RPT", kw)
    row("RPT the same site twice -- exactly ONE line",
        st and alive and [t for t, _ in dec] == ["ITLB"],
        "alive=%s declines=%s" % (alive, dec),
        "one ITLB decline for two accesses -- the latch holds")

    #  ---- RPTu: the latch row at the OTHER site ---------------------------------------
    got, alive, st, dec = run(
        [LD_R1_TO_R2, LD_R4_TO_R2, ST_R2_AT_R3],
        [("r1", UTLB_DA1 | DA2), ("r4", UTLB_DA1 | DA2), ("r3", P.DEST)],
        "RPTu", kw)
    row("RPTu the UTLB site twice -- exactly ONE line",
        st and alive and [t for t, _ in dec] == ["UTLB"],
        "alive=%s declines=%s" % (alive, dec),
        "one UTLB decline for two accesses.  RPT covers only the ITLB latch, so dropping "
        "the guard at THIS site alone was invisible")

    #  ---- A1 / A2 / A3: the ACCEPT side of the de-fatalised predicate ------------------
    a1_got = None
    for nm, base, mask, off in [("A1 itlb", ITLB_DA1, ITLB_MASK, 0),
                                ("A2 utlb", UTLB_DA1, UTLB_MASK, 0),
                                ("A3 itlb", ITLB_DA1, ITLB_MASK, 0x400000)]:
        got, alive, st, dec = run(
            [ST_R0_AT_R1, LD_R1_TO_R2, ST_R2_AT_R3],
            [("r0", 0xffffffff), ("r1", base + off), ("r3", P.DEST)],
            nm.split()[0], kw)
        if nm.startswith("A1"):
            a1_got = got
        row("%s ACCEPT array 1 at +0x%x -- EXACTLY 0x%08x, and SILENT"
            % (nm, off, 0xffffffff & mask),
            st and alive and got == P.le(0xffffffff & mask) and dec == [],
            "alive=%s readback=%s declines=%s" % (alive, got, dec),
            "0x%08x and no decline line.  A3 sits at +0x400000 -- bit 22 SET -- so a "
            "guard grown from 0x800000 to 0xc00000 starts refusing it while A1/A2 at "
            "offset 0 stay green" % (0xffffffff & mask))

    #  ---- A4: the row that closes the whole OR-growth axis -----------------------------
    #  *** A3 TRIPS ON GROWTH INTO BIT 22 AND ONLY BIT 22, AND THAT IS THE WHOLE PROBLEM.
    #  ***  The guard is a bitwise-OR predicate, so growth into ANY of bits 8..22 is as
    #  realistic an edit as G1's and just as invisible: bits 8..13 are the ENTRY SELECTOR
    #  (SH7750 manual 3.7.3 -- "the entry is selected by bits [9:8]", six bits for the
    #  UTLB), so such a growth silently refuses REAL translation entries.  Three measured
    #  instances: `& 0x800100` and `== 0x800000` (both at 10/10) and `& 0x802000` at UTLB.
    #
    #  An accept offset with every probeable low bit SET trips on growth into any of them
    #  at once.  0x7ffffc is bits 2..22 -- bits 0..1 are unreachable with an aligned
    #  mov.l -- and it selects entry 3 of the ITLB and entry 63 of the UTLB, both legal.
    for nm, base, mask in [("A4i itlb", ITLB_DA1, ITLB_MASK),
                           ("A4u utlb", UTLB_DA1, UTLB_MASK)]:
        got, alive, st, dec = run(
            [ST_R0_AT_R1, LD_R1_TO_R2, ST_R2_AT_R3],
            [("r0", 0xffffffff), ("r1", base + 0x7ffffc), ("r3", P.DEST)],
            nm.split()[0], kw)
        row("%s ACCEPT array 1 at +0x7ffffc (bits 2..22 ALL set) -- EXACTLY 0x%08x"
            % (nm, 0xffffffff & mask),
            st and alive and got == P.le(0xffffffff & mask) and dec == [],
            "alive=%s readback=%s declines=%s" % (alive, got, dec),
            "0x%08x and silent.  Any single-bit growth of the guard into bits 2..22 "
            "reddens this row, which A1/A2 (offset 0) and A3 (bit 22 only) cannot see. "
            " One row per device, because the two predicates are separate"
            % (0xffffffff & mask))

    #  ---- O: without a live array-1 oracle the "reads 0" rows prove nothing ------------
    row("O the array-1 oracle is LIVE (A1 returned a real masked value)",
        a1_got == P.le(0xffffffff & ITLB_MASK),
        "A1 readback=%s" % (a1_got,),
        "A1 must have returned 0x%08x; if array 1 answered nothing then R1/R2's "
        "'reads 0' would pass for the wrong reason" % (0xffffffff & ITLB_MASK))

    row("I IDENTITY row count -- guards against a stale copy",
        len(rows) + 1 == EXPECT_ROWS, len(rows) + 1, EXPECT_ROWS)

    bad = sum(1 for _, ok in rows if not ok)
    print()
    print("SH4TLBDA2_RESULT=%d/%d" % (len(rows) - bad, len(rows)))
    print("SH4TLBDA2_PASS" if bad == 0 else "SH4TLBDA2_FAIL")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
