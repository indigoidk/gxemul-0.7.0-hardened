#!/usr/bin/env python3
"""`sh4chcr` WITNESS (rung 3): a guest CHCR write with TD=1 ends the HOST PROCESS,
on an UNMODIFIED in-tree `-E landisk`.

*** THIS IS EASIER TO REACH THAN ANYTHING #447 REPAIRED. ***  Each of that round's four
guards needed the guest to write a SPECIFIC unimplemented bit.  These need only that the
guest ENABLE A DMA CHANNEL, because of how the two switches compose:

    dev_sh4.c:1763-1775   the CHCR write STORES idata unconditionally, then
                          `if (idata & CHCR_TD) sh4_dmac_transfer(...)`
    dev_sh4.c:468-491     inside that call, ONLY `case 0x200:` survives the CHCR_RS
                          switch -- every other resource-select value reaches
                          `default: fatal(); exit(1);`
    dev_sh4.c:486         and with RS == 0x200, CHCR_IE reaches its own exit(1)

So the reachable-and-fatal set is not a corner: it is nearly every CHCR value with TD set.
Three more exits sit above it on the same path -- TS (`:436`), DM (`:445`), SM (`:454`) --
each guarding a `default:` in a switch whose other arms are the legal encodings.

WHAT THE STORE POSITION MEANS FOR THE FIX, and it differs from every site #447 touched.
`cpu->cd.sh.dmac_chcr[dma_channel] = idata` happens BEFORE the call and is unconditional,
so THE GUEST-VISIBLE STATE IS ALREADY CORRECT and no store has to move.  #447's TCR needed
its guard hoisted above a prescaler switch because `timer_hz` was computed upstream; its
RCR1 needed the store moved below the guard.  Here neither applies -- the whole defect is
that the process dies, and the repair is to diagnose and decline the transfer.  A fix
design copied from #447 without checking would move a store that is already in the right
place.

THE CONTROLS ARE WHAT MAKE THIS A MEASUREMENT AND NOT A CRASH REPORT.  *** C1 IS THE
DECISIVE ONE: it writes the SAME ADDRESS at the SAME WIDTH with the SAME ILLEGAL DM=3, and
only TD cleared -- and the host SURVIVES. ***  So the result reads "this VALUE ends the
host", not "this address does", not "this width does", and not even "an illegal field
does".  C2 narrows it further: RS=0x200 with TD SET also survives, which is the one arm of
that switch that returns normally.  C3 shows the guards are WRITE-path only.  Two
device-signature reads prove `DEVICE_ACCESS(sh4)` was entered at all, returning values only
that switch synthesises, so RAM cannot supply them.

MEASURED on the committed pre-fix build: 13/13, six kills and three survivals.

RUNG 3, and the ceiling for this defect: real SH-4 guest instructions through real address
decode, real `memory_rw` and real device dispatch, on a committed unmodified machine
description.  No source is edited and no `device_add` is introduced to reach the site.

*** THIS ASSERTS THE PRE-FIX SYMPTOM, so it is RED once the defect is gone. ***  That is
what a witness should be, and it is why it must NEVER be wired into a gate --
`check_probe_wiring.py` treats a gated witness as a HARD failure, because it manufactures
a phantom regression on the day the fix lands.  Its detector sibling will assert the
repaired behaviour.

usage:  sh4_chcr_witness.py <gxemul-binary> <landisk-kernel>

    *** KEEP THE "./" ON THE BINARY. ***  `os.execvp` on a bare name searches PATH; when
    it misses, EVERY arm reports alive=False and a witness written the naive way "passes"
    having measured nothing.  W0 catches that.
"""
import os
import sys

#  Python puts this script's own directory on sys.path[0], so the session machinery
#  comes from the one place in the tree that has it rather than a copy.
import sh4_pcic_probe as P

#  Every address and constant READ from a header in this repository, not remembered.
SH4_CHCR0 = 0xffa0000c          # src/include/sh4_dmacreg.h:40
SH4_CHCR3 = 0xffa0003c          # :55
CHCR_DM = 0x0000c000            # :117   valid arms are 0<<14, 1<<14, 2<<14
CHCR_SM = 0x00003000            # :121   valid arms are 0<<12, 1<<12, 2<<12
CHCR_TS = 0x00000070            # :127   valid arms are 0..4 << 4
CHCR_TS_4BYTE = 3 << 4          # :131
CHCR_IE = 0x00000004            # :134
CHCR_TD = 0x00000001            # :136
CHCR_DM_INCREMENTED = 1 << 14   # :119
CHCR_SM_INCREMENTED = 1 << 12   # :123

SH4_PVR_ADDR = 0xff000030       # thirdparty/sh4_cpu.h:187
SH4_PRR_ADDR = 0xff000044       # :189
SH4_PVR_SH7751 = 0x04110000     # :196
SH4_PRR_7751R = 0x00000110      # :200

ST = {1: 0x2100, 2: 0x2101, 4: 0x2102}    # mov.b/w/l r0,@r1

#  The IDENTITY constant.  A witness copied into a tree where it no longer runs all of its
#  rows must not report green over a shorter file.
EXPECT_ROWS = 13

rows = []


def row(name, ok, got, want):
    rows.append((name, bool(ok), got, want))
    print("  %-4s %s" % ("ok" if ok else "FAIL", name))
    if not ok:
        print("       got  %s\n       want %s" % (got, want))


def rd(addr, label, kw):
    return P.read_arm(addr, label, kw)


def wr(addr, val, label, kw):
    return P.write_arm(addr, val, label, kw, op=ST[4])


def main():
    if len(sys.argv) != 3:
        print("usage:  sh4_chcr_witness.py <gxemul-binary> <landisk-kernel>")
        return 2
    b, k = sys.argv[1], sys.argv[2]
    kw = dict(binary=b, kernel=k)
    for p in (b, k):
        if not os.path.exists(p):
            print("OPERATIONAL FAILURE: %s does not exist (cwd=%s)" % (p, os.getcwd()))
            print("SH4CHCR_WITNESS_FAIL")
            return 2

    #  ---- the device is reached, and answers something only it knows ------------------
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

    #  ---- THE KILLS ------------------------------------------------------------------
    #  Every value below sets TD.  The comment on each names WHICH default: arm it lands
    #  in, so a row that starts failing says which guard changed rather than merely that
    #  something did.
    kills = [
        ("S1 CHCR0 TS=5   -> dev_sh4.c:436",
         SH4_CHCR0, (5 << 4) | CHCR_TD, "Unimplemented transmit size"),
        ("S2 CHCR0 DM=3   -> dev_sh4.c:445",
         SH4_CHCR0, CHCR_DM | CHCR_TD, "Unimplemented destination delta"),
        ("S3 CHCR0 SM=3   -> dev_sh4.c:454",
         SH4_CHCR0, CHCR_SM | CHCR_TD, "Unimplemented source delta"),
        #  *** THE ONE THAT MAKES THIS BROAD.  Everything here is LEGAL -- 4-byte
        #  transfers, both addresses incrementing -- and it still dies, because RS is
        #  0x100 and only 0x200 survives the switch.
        ("S4 CHCR0 a SANE config, RS=0x100 -> dev_sh4.c:491",
         SH4_CHCR0,
         CHCR_DM_INCREMENTED | CHCR_SM_INCREMENTED | 0x100 | CHCR_TS_4BYTE | CHCR_TD,
         "Unimplemented SH4 RS DMAC"),
        #  RS == 0x200 survives its switch and then CHCR_IE kills at the next site, so
        #  this row reaches a DIFFERENT exit from S4 by a value one bit apart.
        ("S5 CHCR0 RS=0x200 with IE -> dev_sh4.c:486",
         SH4_CHCR0, 0x200 | CHCR_IE | CHCR_TD, "sh4 dmac interrupt"),
        #  A DIFFERENT CHANNEL, to show the defect is per-device and not per-address.
        ("S6 CHCR3 DM=3   -> dev_sh4.c:445, channel 3",
         SH4_CHCR3, CHCR_DM | CHCR_TD, "Unimplemented destination delta"),
    ]
    for name, addr, val, msg in kills:
        buf, alive, st = wr(addr, val, name.split()[0], kw)
        row("%s  KILLS the host (0x%08x)" % (name, val),
            st and not alive and msg in (buf or ""),
            "started=%s alive=%s diagnostic=%s" % (st, alive, msg in (buf or "")),
            "started, NOT alive, and the output names %r" % msg)

    #  ---- THE CONTROLS: same address, same width, and the host LIVES -----------------
    #  *** WITHOUT THESE THE SIX ROWS ABOVE WOULD BE A CRASH REPORT. ***  C1 is S2's value
    #  with ONE BIT cleared -- an illegal DM=3 is still written, the store still happens,
    #  and the host survives because sh4_dmac_transfer is never entered.  So the kill is
    #  attributable to TD, not to the address, the width, or the illegal field.
    buf, alive, st = wr(SH4_CHCR0, CHCR_DM, "C1", kw)
    row("C1 CONTROL: the SAME illegal DM=3 with TD CLEAR -- host SURVIVES",
        st and alive,
        "started=%s alive=%s" % (st, alive),
        "started and alive: the transfer is never entered, so nothing can exit")

    buf, alive, st = wr(SH4_CHCR0, 0x200 | CHCR_TD, "C2", kw)
    row("C2 CONTROL: RS=0x200 WITHOUT IE and TD set -- host SURVIVES",
        st and alive,
        "started=%s alive=%s" % (st, alive),
        "started and alive: 0x200 is the one arm that survives, and IE is clear")

    buf, alive, st = rd(SH4_CHCR0, "C3", kw)
    row("C3 CONTROL: READING CHCR0 is harmless -- the guards are WRITE-path only",
        st and alive,
        "started=%s alive=%s" % (st, alive),
        "started and alive")

    #  ---- W0: the absent-data guard -------------------------------------------------
    #  A witness whose sessions never started reports every arm as not-alive and "passes"
    #  having measured nothing.  This is the row that refuses that.
    n_ses = len(P.STARTS)
    n_ok = sum(1 for _, s in P.STARTS if s)
    row("W0 EVERY session reached the debugger prompt (absent data must FAIL)",
        n_ses > 0 and n_ok == n_ses,
        "sessions=%d started=%d" % (n_ses, n_ok),
        "all %d started" % n_ses)

    row("W-id IDENTITY row count -- guards against a stale copy",
        len(rows) + 1 == EXPECT_ROWS, len(rows) + 1, EXPECT_ROWS)

    bad = sum(1 for _, ok, _, _ in rows if not ok)
    print()
    print("SH4CHCR_WITNESS_RESULT=%d/%d" % (len(rows) - bad, len(rows)))
    print("SH4CHCR_WITNESS_PASS" if bad == 0 else "SH4CHCR_WITNESS_FAIL")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
