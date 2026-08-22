#!/usr/bin/env python3
"""`sh4tlbda2` WITNESS (rung 3): ONE guest access to the upper half of a TLB data array
ends the HOST PROCESS -- on an UNMODIFIED in-tree `-E landisk`.

*** THE DISCRIMINATOR HERE IS A SINGLE ADDRESS BIT, WHICH IS SHARPER THAN ANY SH-4 ROUND
BEFORE IT. ***  #443 needed a particular transaction, #447 a particular value, #448 a
particular field encoding and #451 a whole clocked byte.  Here the SAME device, at the
SAME width, answers normally at 0xf3000000 and ends the host at 0xf3800000.  Nothing
about the access differs but bit 23 of the address.

    dev_sh4.c   DEVINIT registers both da1 devices for 0x01000000 -- SIXTEEN MEGABYTES:
                  sh4_itlb_da1   SH4_ITLB_DA1 = 0xf3000000   (sh4_mmu.h:103)
                  sh4_utlb_da1   SH4_UTLB_DA1 = 0xf7000000   (sh4_mmu.h:133)
                and each handler opens with

                    if (relative_addr & 0x800000) {
                            fatal("sh4_?tlb_da1: TODO: da2 area\\n");
                            exit(1);
                    }

    0x800000 is 8 MB.  It is INSIDE the 16 MB the device claimed, so the device answers
    for an address range whose upper half it cannot service -- and the guard runs BEFORE
    the writeflag test, so a LOAD and a STORE both end the host.

THE CONTROL IS THE SAME DEVICE.  C1/C2 access the LOWER half at the same width and the
host lives.  They also prove the answer came from the DEVICE and not from RAM: the handler
masks the stored value (`itlb_lo[e] &= ~mask; |= idata & mask`), so writing 0xffffffff and
reading it back returns a value that is NEITHER zero NOR 0xffffffff.  RAM would return
what was written; only this device folds it through a mask.

usage:  sh4_tlbda2_witness.py <gxemul-binary> <landisk-kernel>
"""
import os
import sys

import sh4_pcic_probe as P

ITLB_DA1 = 0xf3000000           # thirdparty/sh4_mmu.h:103
UTLB_DA1 = 0xf7000000           # thirdparty/sh4_mmu.h:133
DA2 = 0x800000                  # dev_sh4.c: the bit each handler dies on

#  The EXACT value each handler returns after a 0xffffffff store, spelled from the same
#  constants the handler ORs together (sh4_mmu.h:49-60) rather than from a run.  The two
#  DIFFER -- utlb's mask adds SH4_PTEL_WT (0x1) and SH4_PTEL_D (0x4) -- so an equality
#  test is a PER-DEVICE signature and not merely a liveness check.
#
#  *** AN EARLIER DRAFT ASSERTED INEQUALITY AGAINST THREE WRONG VALUES AND A PANEL SEAT
#  CALLED IT A WEAK SPOT, CORRECTLY. ***  "neither 0xffffffff nor the poison nor zero"
#  passes for ANY other wrong value -- a mutated mask included -- so it proves far less
#  than it looks like it proves.  Equality against the one correct value is the fix.
_WT, _SH, _D, _C = 0x00000001, 0x00000002, 0x00000004, 0x00000008
_PR, _SZ, _V = 0x00000060, 0x00000090, 0x00000100
ITLB_MASK = _SH | _C | _SZ | _PR | _V | 0x1ffffc00        # dev_sh4.c, itlb_da1
UTLB_MASK = _WT | _SH | _D | _C | _SZ | _PR | _V | 0x1ffffc00   # ... utlb_da1 adds WT|D

EXPECT_ROWS = 7

rows = []


def row(name, ok, got, want):
    rows.append((name, bool(ok)))
    print("  %-4s %s" % ("ok" if ok else "FAIL", name))
    if not ok:
        print("       got  %s\n       want %s" % (got, want))


def read32(addr, label, kw):
    """One guest `mov.l @r1,r2`, stored to DEST so the value is recoverable."""
    ops = [0x6212,      # mov.l @r1,r2      (validated in sh4_pcic_probe's OPS table)
           0x2322,      # mov.l r2,@r3
           0x0009]      # nop
    return P.session(
        ["put w 0x%x, 0x%08x" % (P.DEST, P.POISON),
         "r1=0x%x" % addr, "r3=0x%x" % P.DEST]
        + P.poke(ops) + ["pc=0x%x" % P.CODE],
        len(ops) - 1, label, disasm_upto=0, **dict(kw, timeout=90))


def write_then_read(addr, value, label, kw):
    """Store `value`, then load the same address back through the same handler."""
    ops = [0x2102,      # mov.l r0,@r1
           0x6212,      # mov.l @r1,r2
           0x2322,      # mov.l r2,@r3
           0x0009]      # nop
    return P.session(
        ["put w 0x%x, 0x%08x" % (P.DEST, P.POISON),
         "r0=0x%x" % value, "r1=0x%x" % addr, "r3=0x%x" % P.DEST]
        + P.poke(ops) + ["pc=0x%x" % P.CODE],
        len(ops) - 1, label, disasm_upto=0, **dict(kw, timeout=90))


def main():
    if len(sys.argv) != 3:
        print("usage:  sh4_tlbda2_witness.py <gxemul-binary> <landisk-kernel>")
        return 2
    b, k = sys.argv[1], sys.argv[2]
    kw = dict(binary=b, kernel=k)
    for p in (b, k):
        if not os.path.exists(p):
            print("OPERATIONAL FAILURE: %s does not exist (cwd=%s)" % (p, os.getcwd()))
            print("SH4TLBDA2_WITNESS_FAIL")
            return 2

    #  ---- the kills: one LOAD each, at the two sites -----------------------------------
    for name, base, msg in [
            ("S1 itlb_da1 LOAD at 0x%08x" % (ITLB_DA1 | DA2), ITLB_DA1,
             "sh4_itlb_da1: TODO: da2 area"),
            ("S2 utlb_da1 LOAD at 0x%08x" % (UTLB_DA1 | DA2), UTLB_DA1,
             "sh4_utlb_da1: TODO: da2 area")]:
        buf, alive, st = read32(base | DA2, name.split()[0], kw)
        seen = msg in (buf or "")
        row("%s KILLS the host" % name,
            st and not alive and seen,
            "started=%s alive=%s diagnostic=%s" % (st, alive, seen),
            "started, NOT alive, and the output names %r" % msg)

    #  ---- and a STORE kills too: the guard runs BEFORE the writeflag test --------------
    buf, alive, st = write_then_read(ITLB_DA1 | DA2, 0xffffffff, "S3", kw)
    row("S3 itlb_da1 STORE at 0x%08x KILLS the host too" % (ITLB_DA1 | DA2),
        st and not alive and "sh4_itlb_da1: TODO: da2 area" in (buf or ""),
        "started=%s alive=%s" % (st, alive),
        "the guard is above `if (writeflag == MEM_WRITE)`, so direction does not matter")

    #  ---- the controls: SAME device, SAME width, bit 23 clear --------------------------
    for name, base, m in [("C1 itlb_da1", ITLB_DA1, ITLB_MASK),
                          ("C2 utlb_da1", UTLB_DA1, UTLB_MASK)]:
        buf, alive, st = write_then_read(base, 0xffffffff, name.split()[0], kw)
        got = P.dumped(buf)
        want = P.le(0xffffffff & m)
        row("%s CONTROL at 0x%08x -- SURVIVES, readback is EXACTLY 0x%08x"
            % (name, base, 0xffffffff & m),
            st and alive and got == want,
            "started=%s alive=%s readback=%s" % (st, alive, got),
            "alive, and a readback EQUAL to 0x%08x -- the value this device's own mask "
            "folds 0xffffffff to.  RAM would echo 0xffffffff and an absent store would "
            "leave the poison, but so would many other wrong values; only equality "
            "identifies THIS handler, and the two devices' masks differ (0x%08x vs "
            "0x%08x) so the rows cannot be satisfied by each other"
            % (0xffffffff & m, 0xffffffff & ITLB_MASK, 0xffffffff & UTLB_MASK))

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
    print("SH4TLBDA2_WITNESS_RESULT=%d/%d" % (len(rows) - bad, len(rows)))
    print("SH4TLBDA2_WITNESS_PASS" if bad == 0 else "SH4TLBDA2_WITNESS_FAIL")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
