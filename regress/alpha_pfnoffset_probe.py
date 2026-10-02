#!/usr/bin/env python3
#
#  alphapfnoffset -- RUNG-3 WITNESS: the Alpha page-table walk drops the within-page offset.
#
#      memory_alpha.c   (*return_paddr) = ALPHA_PTE_TO_PFN(pte3) << pageSizeShift;
#      memory_rw.c      offset = paddr & offset_mask;
#
#  The walk returns a PAGE BASE, so `paddr & offset_mask' is zero and a walked access resolves to
#  the page's first bytes.  A codex reachability pass enumerated all 8192 offsets: the walk yields
#  offset zero throughout, differing from the offset-preserving address for 8191 of them.
#
#  *** THIS IS A WITNESS (rung 3), NOT A DETECTOR.  It shows the symptom on the COMMITTED build,
#  which is what licenses a fix, and it must NOT be gated -- a witness stays red until the fix
#  lands.  Its rows therefore assert the CORRECT behaviour and are expected to FAIL here. ***
#  [#556, 2026-10-02 -- a records correction; the text above is kept as it was written] Post-fix detector for
#  alphapfnoffset: the page-table walk now preserves within-page offset at src/cpus/memory_alpha.c:186; expected
#  rows pass on HEAD.  (hbundle_regress27:F8: regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md)
#
#  ---------------------------------------------------------------------------------------------
#  SIX THINGS THE DESIGN REVIEW (grok, 2026-09-07) ESTABLISHED.  Four are traps that would have
#  produced a GREEN run on the defective build; none is obvious from the source.
#
#  1. THE SWAP IS NOT A BLOCKER.  `swpctx' is the only writer of apcb_ptbr -- but it is only a
#     CONFOUND when ptbr and flags DIFFER.  Put the SAME L1 PFN in both PCB fields and the
#     defective line and the corrected line both leave apcb_ptbr = L1_PFN.  (The inverse is a
#     trap: PFN in flags with ptbr = 0 arms the walk on HEAD and leaves IDENTITY MAPPING on a
#     fixed PAL, so post-fix green would be the bootstrap, not the repair.)
#
#  2. PFN, NOT BYTE ADDRESS.  apcb_ptbr and the PTE high halves hold PFNs.  ptbr = 0x01050000
#     would give base = 0x01050000 << 13, past RAM, and the walk reports `wasn't found'.
#
#  3. ONE COLD SHOT.  The fast path caches the page from `paddr & ~offset_mask' -- the CORRECT
#     physical page -- so the walked paddr is wrong only for the FILL.  A second access at any
#     offset is a hit and reads the right bytes, i.e. GOES GREEN ON HEAD.  Load once; never retry.
#
#  4. THE POLARITY TRAP.  Planting B *through the walk* makes HEAD store it at data+0 and read it
#     back from data+0 -- the defect measured against itself, green.  A cousin: planting at vaddr
#     0/N while ptbr == 0 hits PHYSICAL 0/N, not the data page.  So A and B are planted through
#     K0SEG of the DATA PAGE, before the walk is ever used.
#
#  5. A FAILED WALK DOES NOT WRITE THE DESTINATION REGISTER.  LS_GENERIC_N returns on a memory_rw
#     failure without storing, so "faults or returns zero" is false.  Hence a THREE-WAY oracle
#     with a sentinel S pre-loaded into the destination:
#         S = the walk never completed        0 = walked onto unmapped physical
#         A = right page, offset dropped      B = correct
#
#  6. ONLY ALPHA_PTE_VALID IS LOAD-BEARING.  Verified in memory_alpha.c: each level tests
#     `!(pteN & ALPHA_PTE_VALID)' and nothing else -- not KR/KW/UR/UW, FAULT_ON_*, ASM or
#     granularity.  Setting bits the walk does not implement and calling them required would be
#     the "cannot hurt" addition this project refuses.
#
#  Usage:  alpha_pfnoffset_probe.py <gxemul-binary> [label]
import os, sys, pty, select, time, re

BIN   = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"
MACH  = "alphabook1"

rows = []
def row(name, got, want, note="", negate=False):
    ok = (got != want) if negate else (got == want)
    rows.append((name, ok))
    shown = ("NOT " + str(want)) if negate else str(want)
    print("%-14s %-20s %-22s %-44s %s" % (name, str(got), shown, note, "ok" if ok else "FAIL"))
    return ok

# ---------------------------------------------------------------- encoder
ZERO, T0, T1, T2, T3, T4 = 31, 1, 2, 3, 4, 5
A0 = 16

def mem(op, ra, rb, disp):
    assert -32768 <= disp <= 32767, "displacement %d out of range" % disp
    return (op << 26) | (ra << 21) | (rb << 16) | (disp & 0xffff)

def LDA (ra, disp, rb=ZERO): return mem(0x08, ra, rb, disp)
def LDAH(ra, disp, rb=ZERO): return mem(0x09, ra, rb, disp)
def LDQ (ra, disp, rb):      return mem(0x29, ra, rb, disp)
def CALL_PAL(n):             return n & 0x3ffffff

def load_const(reg, val):
    lo, hi = val & 0xffff, (val >> 16) & 0xffff
    if lo & 0x8000:
        hi = (hi + 1) & 0xffff
    return [LDAH(reg, hi if hi < 0x8000 else hi - 0x10000),
            LDA (reg, lo if lo < 0x8000 else lo - 0x10000, reg)]

# ---------------------------------------------------------------- the map
K0SEG      = 0xfffffc0000000000
def k0(p): return K0SEG | p

PAGESHIFT  = 13
PTE_VALID  = 0x1
def pte(pfn): return (pfn << 32) | PTE_VALID

#  Off the PROM pocket (0x10000 entry stub, 0x10100 initial ctx, 0x12000 argspace, 0x14000 HWRPB)
#  and off the sibling probes' 0x0102/0103/0104xxxx scratch.
P_L1, P_L2, P_L3, P_DATA = 0x01050000, 0x01052000, 0x01054000, 0x01056000
P_PCB, P_CODE            = 0x01058000, 0x0105a000
P_DATA2                  = 0x0105c000          # mapped at vaddr 0x2000 via L3[1]
L1_PFN = P_L1 >> PAGESHIFT

#  -M 64.  A page past physical_max is written to nothing and read back as zero, SILENTLY.
assert max(P_L1, P_L2, P_L3, P_DATA, P_DATA2, P_PCB, P_CODE) < 64 * 1024 * 1024
assert all(p % 8192 == 0 for p in (P_L1, P_L2, P_L3, P_DATA, P_DATA2)), "pages must be page-aligned"

VADDR = 0x0000            # i1 = i2 = i3 = 0
N     = 8                 # aligned: an unaligned N forces the generic path for the WRONG reason
VAL_A = 0xaaaa0000aaaa    # planted at data + 0   -- what the DEFECT returns
VAL_B = 0xbbbb0000bbbb    # planted at data + N   -- what a CORRECT walk returns
#  ---- the SECOND cold row: non-zero VPN, offset in the UPPER 4 KB ----
VADDR2 = 0x2000           # i1 = i2 = 0, i3 = 1  -- the VPN is NON-ZERO, which is the point
N2     = 0x1008           # upper 4 KB, 8-aligned
VAL_A2 = 0xcccc0000cccc   # data2 + 0        <- what a page-base result reads
VAL_B2 = 0xdddd0000dddd   # data2 + 0x1008   <- CORRECT
VAL_C2 = 0xeeee0000eeee   # data2 + 0x0008   <- what a 0xfff mask, or `| 8', reads
assert (VADDR2 >> 13) == 1, "VADDR2 must select L3[1] -- a NON-ZERO VPN is the whole point"
assert N2 >= 0x1000 and N2 % 8 == 0, "N2 must sit in the upper 4 KB and be 8-aligned"

VAL_S = 0x55000055        # sentinel: unchanged means the load never stored.  32-bit with
                          # bit 31 CLEAR, because load_const builds it -- a wider value
                          # would silently truncate and the row would compare the wrong thing.

DUMMY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alpha_dummy.bin")
if not os.path.exists(DUMMY):
    with open(DUMMY, "wb") as f:
        f.write(b"\0" * 8)

def session(cmds, settle=1.6, spin=2.4):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "alpha", "-e", MACH, "-M", "64",
                       "0x20000000:" + DUMMY])
        os._exit(127)
    buf = ""
    def rd(t):
        nonlocal buf
        end = time.time() + t
        while time.time() < end:
            r, _, _ = select.select([fd], [], [], 0.1)
            if not r:
                continue
            try:
                d = os.read(fd, 65536)
                if not d:
                    return False
                buf += d.decode("latin-1", "replace")
            except OSError:
                return False
        return True
    alive = rd(settle)
    for i, c in enumerate(cmds):
        try:
            os.write(fd, (c + "\n").encode("latin-1"))
        except OSError:
            alive = False; break
        if not rd(spin if i == len(cmds) - 1 else 0.3):
            alive = False; break
    try:
        os.write(fd, b"quit\n"); rd(0.4)
    except OSError:
        pass
    try:
        os.close(fd)
    except OSError:
        pass
    return buf.replace("\r", ""), alive

def printed(t, reg):
    m = re.search(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
    return "absent" if not m else "0x%x" % int(m.group(1), 16)

print("alpha_pfnoffset_probe -- binary=%s label=%s machine=%s" % (BIN, LABEL, MACH))
print("%-14s %-20s %-22s %-44s %s" % ("row", "got", "want", "note", ""))

#  ---- setup: tables, data and the PCB, ALL planted while ptbr is still 0 ----------------------
#  K0SEG for the data page (trap 4); the table pages are equally reachable either way.
setup = [
    "put d 0x%x, 0x%x" % (k0(P_L1),        pte(P_L2 >> PAGESHIFT)),
    "put d 0x%x, 0x%x" % (k0(P_L2),        pte(P_L3 >> PAGESHIFT)),
    "put d 0x%x, 0x%x" % (k0(P_L3),        pte(P_DATA >> PAGESHIFT)),
    "put d 0x%x, 0x%x" % (k0(P_DATA + 0),  VAL_A),
    "put d 0x%x, 0x%x" % (k0(P_DATA + N),  VAL_B),
    #  the second page, and L3[1] -> it.  Entry 1 is at byte offset 8 of the L3 page.
    "put d 0x%x, 0x%x" % (k0(P_L3 + 8),    pte(P_DATA2 >> PAGESHIFT)),
    "put d 0x%x, 0x%x" % (k0(P_DATA2 + 0),      VAL_A2),
    "put d 0x%x, 0x%x" % (k0(P_DATA2 + 8),      VAL_C2),
    "put d 0x%x, 0x%x" % (k0(P_DATA2 + N2),     VAL_B2),
    #  PCB: ptbr AND flags both the L1 PFN, so the swpctx defect cannot change what gets armed.
    "put d 0x%x, 0x%x" % (k0(P_PCB + 16),  L1_PFN),     # apcb_ptbr
    "put d 0x%x, 0x%x" % (k0(P_PCB + 40),  L1_PFN),     # apcb_flags
    "put d 0x%x, 0x%x" % (k0(P_CODE - 8),  k0(P_PCB)),  # a0 source for swpctx
]

#  ---- SESSION 1: the K0SEG controls, before any walk ------------------------------------------
#  T0 must hold a K0SEG address, which load_const CANNOT build (it makes 32-bit sign-extended
#  constants and K0SEG needs bits 63..42).  So the pointer is planted in memory and read with ldq,
#  which is the same bootstrap the two sibling Alpha probes use.
cmds = setup + ["put d 0x%x, 0x%x" % (k0(P_CODE - 16), k0(P_DATA))]
prog_ctl = (load_const(T3, P_CODE - 16) +
            [LDQ(T0, 0, T3),      # t0 = k0(P_DATA)
             LDQ(T1, 0, T0),      # t1 = *(data + 0)   -- must be A
             LDQ(T2, N, T0)])     # t2 = *(data + N)   -- must be B
cmds += ["put w 0x%x, 0x%08x" % (k0(P_CODE) + 4 * i, op) for i, op in enumerate(prog_ctl)]
cmds += ["pc=0x%x" % k0(P_CODE), "step %d" % len(prog_ctl), "print t1", "print t2"]
t1txt, alive1 = session(cmds)

row("data0 k0", printed(t1txt, "t1"), "0x%x" % VAL_A,
    "CONTROL: A really is at data+0")
row("dataN k0", printed(t1txt, "t2"), "0x%x" % VAL_B,
    "CONTROL: B really is at data+N")

#  ---- SESSION 2: arm the walk, then ONE cold walked load --------------------------------------
prog_walk = (load_const(T3, P_CODE - 8) +
             [LDQ(A0, 0, T3),               # a0 = k0(P_PCB)
              CALL_PAL(0x30)] +             # swpctx -> apcb_ptbr = L1_PFN
             load_const(T4, VAL_S) +
             [LDQ(T4, VADDR + N, ZERO)])    # THE ONE COLD WALKED LOAD
cmds = setup + ["put w 0x%x, 0x%08x" % (k0(P_CODE) + 4 * i, op) for i, op in enumerate(prog_walk)]
cmds += ["pc=0x%x" % k0(P_CODE), "step %d" % len(prog_walk), "print t4"]
t2txt, alive2 = session(cmds)

dest     = printed(t2txt, "t4")
notfound = "wasn't found" in t2txt

#  ---- SESSION 3: the second cold load, non-zero VPN, offset in the upper 4 KB ---------------
#  A SEPARATE session because the load must be COLD: the fast path caches the correct physical
#  page, so a second access in the same run is a hit and reads the right bytes on HEAD.
prog_walk2 = (load_const(T3, P_CODE - 8) +
              [LDQ(A0, 0, T3), CALL_PAL(0x30)] +
              load_const(T4, VAL_S) +
              [LDQ(T4, VADDR2 + N2, ZERO)])
cmds = setup + ["put w 0x%x, 0x%08x" % (k0(P_CODE) + 4 * i, op) for i, op in enumerate(prog_walk2)]
cmds += ["pc=0x%x" % k0(P_CODE), "step %d" % len(prog_walk2), "print t4"]
t3txt, alive3 = session(cmds)
dest2 = printed(t3txt, "t4")

row("walk found", "absent" if not notfound else "wasn't found", "absent",
    "CONTROL: the table walked to a valid L3")
#  *** AN INEQUALITY PASSES ON EVERY NON-OBSERVATION.  Repaired 2026-09-07 -- see the same note
#  in alpha_harness_probe.py.  Both rows below scored GREEN when `dest' was "absent" or "died",
#  i.e. when the readback never happened.  `walk off' reds on those, so the detector did not
#  escape; the defect was in these two rows' claim to be CONTROLS. ***
obs = dest.startswith("0x") and dest != "0x0"
stored = obs and dest != ("0x%x" % VAL_S)
row("walk stored", "yes" if stored else dest, "yes",
    "CONTROL: an OBSERVED word that is not the sentinel -- the sentinel surviving, or no readback at all, means the load never wrote t4")
row("walk mapped", "yes" if obs else dest, "yes",
    "CONTROL: a real nonzero word -- 0x0/absent/died all mean the walk found no physical page")
row("walk off", dest, "0x%x" % VAL_B,
    "the walked load must return data+N, not data+0")

#  *** THE SECOND COLD ROW.  Six lesser edits score 6/6 on the row above; three of them die
#  here, and the three-way plant says WHICH: ***
#      VAL_B2  correct
#      VAL_C2  a 0xfff mask (the 4 KB copy) or a hardcoded `| 8'
#      VAL_A2  a page-base result
#  *** THAT LAST CLAIM WAS ARITHMETICALLY FALSE AND IS CORRECTED, 2026-09-07, BY THE
#  RETROSPECTIVE PASS 2 ON THIS COMMIT.  It read: "0x3fff and 0x7fff are EQUIVALENT inside an
#  8 KB page -- bits 13/14 of an offset are always zero there -- so no row kills them and none
#  should pretend to."  The premise is about an OFFSET; the expression masks the FULL VIRTUAL
#  ADDRESS.  This row drives vaddr = VADDR2 + N2 = 0x3008, so:
#
#      mask 0x0fff -> 0x0008     mask 0x1fff -> 0x1008  (correct)
#      mask 0x3fff -> 0x3008     mask 0x7fff -> 0x3008
#
#  The two wider masks equal EACH OTHER and BOTH differ from the correct 0x1008 -- bit 13 is
#  set, so `base | 0x3008' lands in the NEXT 8 KB page, which nothing planted.  **`walk vpn'
#  therefore DOES kill both.**  The correction makes this detector STRONGER than it claimed,
#  which is the safe direction to have been wrong in and is still a wrong record. ***
#  NOT separately measured: no mutant was built for either mask.  The arithmetic above is the
#  warrant, and it is checkable by reading -- unlike the survival the old sentence asserted.
row("walk vpn", dest2, "0x%x" % VAL_B2,
    "non-zero VPN, offset in the UPPER 4 KB: kills the 0xfff mask and unmasked +vaddr")

ok = sum(1 for _, o in rows if o)
print()
print("ALPHAPFN_RESULT=%d/%d" % (ok, len(rows)))
print("ALPHAPFN_DONE")
sys.exit(0 if ok == len(rows) else 1)
