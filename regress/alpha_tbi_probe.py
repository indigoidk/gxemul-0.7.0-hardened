#!/usr/bin/env python3
"""alphatbi_probe.py -- witness for Alpha PAL_OSF1_tbi negative selector defect (alphatbinegsel)

    usage:  alphatbi_probe.py <gxemul-binary> [label]

WHAT THIS PINS.
In src/cpus/cpu_alpha_palcode.c, case 0x33 /* PAL_OSF1_tbi */:
    if (a0 >= 1)
        cpu->invalidate_translation_caches(cpu, a1, INVALIDATE_VADDR);
    else
        cpu->invalidate_translation_caches(cpu, 0, INVALIDATE_ALL);

a0 is uint64_t.
ALPHA_TBIA() is defined as alpha_pal_tbi(-2, 0), passing a0 = -2 (0xfffffffffffffffe).
ALPHA_TBIAP() is defined as alpha_pal_tbi(-1, 0), passing a0 = -1 (0xffffffffffffffff).
Because a0 is unsigned uint64_t without a signed cast or upper bound check:
    (uint64_t)-2 >= 1 is TRUE  -> takes INVALIDATE_VADDR branch with a1 = 0
    (uint64_t)-1 >= 1 is TRUE  -> takes INVALIDATE_VADDR branch with a1 = 0
INVALIDATE_VADDR invalidates only the entry matching virtual page (a1 & vaddr_mask) == 0.
INVALIDATE_ALL invalidates every translation cache entry.

Therefore, TBIA/TBIAP on HEAD flushes virtual page ZERO and NOTHING ELSE.

FIVE TRAPS HANDLED:
1. Debugger all-flushes between interactions:
   The fill (initial load caching VPN), remap (PTE update via K0SEG store),
   tbi (call_pal 0x33), and observing load are ALL executed within a SINGLE 'step N'.
2. K0SEG is checked before ptbr:
   The test addresses (0x2000, 0x4000, 0x6000) are in user virtual memory and consult
   the 3-level page table, warming and testing the dynamic translation cache.
3. Page 0 is flushed by the defect:
   We use non-zero VPNs (0x2000 = VPN 1, 0x4000 = VPN 2, 0x6000 = VPN 3).
4. Zero a1 explicitly before call_pal 0x33:
   LDA a1, 0(zero) is executed before TBIA/TBIAP palcalls.
5. Remap must change observed bytes:
   Initial pages hold VAL_A/VAL_C/VAL_E; remapped pages hold VAL_B/VAL_D/VAL_F.

ORACLE POLARITY:
Asserts the CORRECT behavior (re-walks and loads remapped data VAL_B / VAL_D).
Pre-fix committed build: RED (stale cached data VAL_A / VAL_C observed).
Post-fix build: GREEN (re-walked data VAL_B / VAL_D observed).

FIFTEEN ROWS.  Rows 1-7 (sessions 1-3) are the witness above.  Rows 8-15 are
the #520 ACCEPT ROWS: the fix ADDS a predicate, so every edit that moves what
the guard admits owes a row that reddens under it.  They use a TWO-PAGE
composite -- an invalidated target and an unrelated page that must survive a
selective invalidate -- because the single-page positive control cannot tell
the two arms apart at all.  See the AXIS SET comment above session 4.

CONTRACT -- what this detector is designed to catch, and what it is not.
ROWED, each with a MEASURED kill recorded in
regress/artifacts/alphatbinegsel/killtable_20260910/:
  * either bound of the [1,3] window moving in either direction
    (>=1 -> >=0 or >=2;  <=3 -> <=2 or <=4);
  * the window narrowing to exclude its interior (a0 = 2);
  * a conjunct on a1, the one lvalue the guarded body reads that the guard
    does not, at two thresholds (a1 == 0 and a1 == 0x8000);
  * OPERAND MAGNITUDE on a0: narrowing either cast to 32 bits, and a
    `<= 3' -> `!= 4' rewrite.  Both are invisible at every small selector
    value, so this axis is pinned by a0 = 0x0000000100000001, loaded from
    memory because load_const spans only a sign-extended 32-bit range.
NOT ROWED, disclosed rather than left to be discovered later:
  * the -1 vs -2 distinction.  On hardware they differ only in whether ASM=1
    (global) entries survive; this model's translation cache carries no
    ASM/ASN metadata, so the two are INDISTINGUISHABLE by any probe against
    it.  A row claiming to separate them would be vacuous by construction.
  * selector values above 4 individually -- a0 = 5.. lie in the same guard
    cell as a0 = 4 and are covered by "bnd out", not by rows of their own.
  * a1 thresholds other than 0 and 0x8000.
  * multi-axis joints, where a0 and a1 are perturbed in one edit.  *** SUCH A
    MUTANT IS PREDICTED TO SWEEP THIS INSTRUMENT 15/15 -- A TOTAL ESCAPE, NOT
    A CORNER. ***  The named discriminator is
        && !((int64_t)a0 == 1 && a1 == 0)
    which no row enters, because "bnd lo" drives a1 = 0x6000 and the two rows
    that drive a1 = 0 drive a0 = 2.  Clause (e) only does its job -- letting a
    later escape land as "outside the contract, as stated" rather than as a
    breach -- if the statement conveys the SIZE, so it is stated here.
  * the case-0x33 dispatch label: clause (e) here, because the palcode
    selector flows into no lvalue the guarded body reads and the body never
    re-tests it.
  * *** THE ITB/DTB DISTINCTION, AND TWO ROWS BELOW SILENTLY DEPEND ON ITS
    ABSENCE. ***  a0 = 1 (ITB), 2 (DTB) and 3 (both) are ARCHITECTURALLY
    different requests; this model has ONE unified translation cache and
    services all three identically, through one arm with identical arguments.
    So no row here can observe the split -- and, worse, "bnd lo" (a0 = 1,
    ITB) would go RED ON A CORRECT IMPLEMENTATION of it: it observes X with an
    ordinary DATA load, so a real ITB-only flush leaves that load reading the
    stale value.  "bnd mid" (a0 = 2, DTB) stays green.  A future round
    implementing the split MUST re-pin "bnd lo" FIRST and measure it red
    before changing the code, per the oracle-correction rule (#560).  Recorded now
    because found later this costs the whole re-pin-first dance.

FIVE ROWS CARRY NO KILL AND ARE NOT MEANT TO.  "live", "tbia fill",
"tbiap fill" and "pos fill" are declared CONTROLS -- they prove the session
ran and the initial walked load cached what it should -- and "pos obs" is the
pre-existing positive control, whose channel does not vary between the two
arms and therefore cannot see a guard edit.  That blindness is precisely why
the accept rows below were owed.
"""
import os, sys, pty, select, time, re

BIN   = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"
MACH  = "alphabook1"

rows = []
def row(name, got, want, note=""):
    ok = (got == want)
    rows.append((name, ok))
    print("%-16s %-20s %-20s %-50s %s" % (name, str(got), str(want), note,
                                          "ok" if ok else "FAIL"))
    return ok

# ---------------------------------------------------------------- encoder
ZERO, T0, T1, T2, T3, T4, T5 = 31, 1, 2, 3, 4, 5, 6
A0, A1 = 16, 17

def mem(op, ra, rb, disp):
    assert -32768 <= disp <= 32767, "displacement %d out of range" % disp
    return ((op & 0x3f) << 26) | ((ra & 31) << 21) | ((rb & 31) << 16) | (disp & 0xffff)

def LDA (ra, disp, rb=ZERO): return mem(0x08, ra, rb, disp)
def LDAH(ra, disp, rb=ZERO): return mem(0x09, ra, rb, disp)
def LDQ (ra, disp, rb):      return mem(0x29, ra, rb, disp)
def STQ (ra, disp, rb):      return mem(0x2d, ra, rb, disp)
def CALL_PAL(func):          return (0x00 << 26) | (func & 0x3ffffff)

def load_const(reg, val):
    hi, lo = (val >> 16) & 0xffff, val & 0xffff
    if lo & 0x8000:
        hi = (hi + 1) & 0xffff
    return [LDAH(reg, hi - 0x10000 if hi & 0x8000 else hi, ZERO),
            LDA (reg, lo - 0x10000 if lo & 0x8000 else lo, reg)]

# ---------------------------------------------------------------- addresses & map
K0SEG      = 0xfffffc0000000000
def k0(p): return K0SEG | p

PAGESHIFT  = 13
PTE_VALID  = 0x1
def pte(pfn): return (pfn << 32) | PTE_VALID

P_L1       = 0x01050000
P_L2       = 0x01052000
P_L3       = 0x01054000
P_DATA1    = 0x01056000  # TBIA initial page (VPN 1 = 0x2000)
P_DATA2    = 0x01058000  # TBIA remapped page
P_DATA3    = 0x0105a000  # TBIAP initial page (VPN 2 = 0x4000)
P_DATA4    = 0x0105c000  # TBIAP remapped page
P_DATA5    = 0x0105e000  # POSITIVE selector initial page (VPN 3 = 0x6000)
P_DATA6    = 0x01060000  # POSITIVE selector remapped page
P_PCB      = 0x01062000
P_PTRV     = 0x01064000
P_CODE     = 0x01066000

L1_PFN     = P_L1 >> PAGESHIFT

assert max(P_L1, P_L2, P_L3, P_DATA1, P_DATA2, P_DATA3, P_DATA4, P_DATA5, P_DATA6,
           P_PCB, P_PTRV, P_CODE) < 64 * 1024 * 1024, "addresses must fit in RAM"

VAL_A = 0xaaaa0000aaaa
VAL_B = 0xbbbb0000bbbb
VAL_C = 0xcccc0000cccc
VAL_D = 0xdddd0000dddd
VAL_E = 0xeeee0000eeee
VAL_F = 0xffff0000ffff
VAL_S = 0x55000055

DUMMY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alpha_dummy.bin")
if not os.path.exists(DUMMY):
    with open(DUMMY, "wb") as f:
        f.write(b"\0" * 8)

# ---------------------------------------------------------------- session
def session(cmds, timeout=6.0):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "alpha", "-e", MACH, "-M", "64",
                       "0x20000000:" + DUMMY])
        os._exit(127)
    buf = ""
    def wait_prompt(t=6.0):
        nonlocal buf
        last_pos = len(buf)
        end = time.time() + t
        while time.time() < end:
            r, _, _ = select.select([fd], [], [], 0.02)
            if not r:
                continue
            try:
                d = os.read(fd, 65536)
                if not d:
                    return False
                buf += d.decode("latin-1", "replace")
                if "gxemul>" in buf[last_pos:].lower():
                    return True
            except OSError:
                return False
        return False

    alive = wait_prompt(timeout)
    for c in cmds:
        try:
            os.write(fd, (c + "\n").encode("latin-1"))
        except OSError:
            alive = False; break
        if not wait_prompt(timeout):
            alive = False; break
    try:
        os.write(fd, b"quit\n")
        time.sleep(0.05)
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

# ---------------------------------------------------------------- table setup
setup = [
    # L1 and L2 tables
    "put d 0x%x, 0x%x" % (k0(P_L1),        pte(P_L2 >> PAGESHIFT)),
    "put d 0x%x, 0x%x" % (k0(P_L2),        pte(P_L3 >> PAGESHIFT)),
    # Initial L3 entries: L3[1] -> DATA1, L3[2] -> DATA3, L3[3] -> DATA5
    "put d 0x%x, 0x%x" % (k0(P_L3 + 8),    pte(P_DATA1 >> PAGESHIFT)),
    "put d 0x%x, 0x%x" % (k0(P_L3 + 16),   pte(P_DATA3 >> PAGESHIFT)),
    "put d 0x%x, 0x%x" % (k0(P_L3 + 24),   pte(P_DATA5 >> PAGESHIFT)),
    # Data pages
    "put d 0x%x, 0x%x" % (k0(P_DATA1 + 0), VAL_A),
    "put d 0x%x, 0x%x" % (k0(P_DATA2 + 0), VAL_B),
    "put d 0x%x, 0x%x" % (k0(P_DATA3 + 0), VAL_C),
    "put d 0x%x, 0x%x" % (k0(P_DATA4 + 0), VAL_D),
    "put d 0x%x, 0x%x" % (k0(P_DATA5 + 0), VAL_E),
    "put d 0x%x, 0x%x" % (k0(P_DATA6 + 0), VAL_F),
    # PCB setup (ptbr & flags)
    "put d 0x%x, 0x%x" % (k0(P_PCB + 16),  L1_PFN),
    "put d 0x%x, 0x%x" % (k0(P_PCB + 40),  L1_PFN),
    # Pointer vector
    "put d 0x%x, 0x%x" % (k0(P_PTRV + 0),  k0(P_PCB)),
    "put d 0x%x, 0x%x" % (k0(P_PTRV + 8),  k0(P_L3 + 8)),
    "put d 0x%x, 0x%x" % (k0(P_PTRV + 16), pte(P_DATA2 >> PAGESHIFT)),
    "put d 0x%x, 0x%x" % (k0(P_PTRV + 24), k0(P_L3 + 16)),
    "put d 0x%x, 0x%x" % (k0(P_PTRV + 32), pte(P_DATA4 >> PAGESHIFT)),
    "put d 0x%x, 0x%x" % (k0(P_PTRV + 40), k0(P_L3 + 24)),
    "put d 0x%x, 0x%x" % (k0(P_PTRV + 48), pte(P_DATA6 >> PAGESHIFT)),
    "put d 0x%x, 0x%x" % (k0(P_PTRV + 56), k0(P_PTRV)),
]

print("alphatbi_probe -- binary=%s label=%s machine=%s" % (BIN, LABEL, MACH))
print("%-16s %-20s %-20s %-50s %s" % ("row", "got", "want", "note", ""))

# ================================================================
# SESSION 1: TBIA (a0 = -2, a1 = 0) on VPN 1 (0x2000)
# ================================================================
prog1 = (load_const(T0, P_PTRV) +
         [LDQ(T0, 56, T0),      # t0 = k0(P_PTRV)
          LDQ(A0, 0, T0),       # a0 = k0(P_PCB)
          LDQ(T1, 8, T0),       # t1 = k0(P_L3 + 8) (PTE addr)
          LDQ(T2, 16, T0),      # t2 = pte(P_DATA2 >> 13) (new PTE)
          CALL_PAL(0x30)] +     # swpctx -> installs ptbr
         load_const(T3, 0x2000) +
         [LDQ(T4, 0, T3),       # WARM TRANSLATION CACHE: loads VAL_A from 0x2000
          STQ(T2, 0, T1),       # REMAP: L3[1] -> P_DATA2 (holding VAL_B)
          LDA(A0, -2, ZERO),    # a0 = -2 (ALPHA_TBIA)
          LDA(A1, 0, ZERO),     # a1 = 0 (TRAP 4: explicit zero)
          CALL_PAL(0x33)] +     # PAL_OSF1_tbi
         load_const(T5, VAL_S) +
         [LDQ(T5, 0, T3)])      # OBSERVING LOAD: reads 0x2000

cmds1 = setup + ["put w 0x%x, 0x%08x" % (k0(P_CODE) + 4 * i, op) for i, op in enumerate(prog1)]
cmds1 += ["pc=0x%x" % k0(P_CODE), "step %d" % len(prog1), "print t4", "print t5"]
t1txt, alive1 = session(cmds1)

t4_1 = printed(t1txt, "t4")
t5_1 = printed(t1txt, "t5")

row("live", "alive" if alive1 else "died", "alive",
    "CONTROL: emulator session survives sequence")
row("tbia fill", t4_1, "0x%x" % VAL_A,
    "CONTROL: initial walked load cached VAL_A")
row("tbia obs", t5_1, "0x%x" % VAL_B,
    "TBIA (a0=-2) must flush TLB and read remapped VAL_B")

# ================================================================
# SESSION 2: TBIAP (a0 = -1, a1 = 0) on VPN 2 (0x4000)
# ================================================================
prog2 = (load_const(T0, P_PTRV) +
         [LDQ(T0, 56, T0),      # t0 = k0(P_PTRV)
          LDQ(A0, 0, T0),       # a0 = k0(P_PCB)
          LDQ(T1, 24, T0),      # t1 = k0(P_L3 + 16) (PTE addr)
          LDQ(T2, 32, T0),      # t2 = pte(P_DATA4 >> 13) (new PTE)
          CALL_PAL(0x30)] +     # swpctx -> installs ptbr
         load_const(T3, 0x4000) +
         [LDQ(T4, 0, T3),       # WARM TRANSLATION CACHE: loads VAL_C from 0x4000
          STQ(T2, 0, T1),       # REMAP: L3[2] -> P_DATA4 (holding VAL_D)
          LDA(A0, -1, ZERO),    # a0 = -1 (ALPHA_TBIAP)
          LDA(A1, 0, ZERO),     # a1 = 0 (TRAP 4: explicit zero)
          CALL_PAL(0x33)] +     # PAL_OSF1_tbi
         load_const(T5, VAL_S) +
         [LDQ(T5, 0, T3)])      # OBSERVING LOAD: reads 0x4000

cmds2 = setup + ["put w 0x%x, 0x%08x" % (k0(P_CODE) + 4 * i, op) for i, op in enumerate(prog2)]
cmds2 += ["pc=0x%x" % k0(P_CODE), "step %d" % len(prog2), "print t4", "print t5"]
t2txt, alive2 = session(cmds2)

t4_2 = printed(t2txt, "t4")
t5_2 = printed(t2txt, "t5")

row("tbiap fill", t4_2, "0x%x" % VAL_C,
    "CONTROL: initial walked load cached VAL_C")
row("tbiap obs", t5_2, "0x%x" % VAL_D,
    "TBIAP (a0=-1) must flush TLB and read remapped VAL_D")

# ================================================================
# SESSION 3: Positive Selector Control (a0 = 2 DTB, a1 = 0x6000)
# ================================================================
prog3 = (load_const(T0, P_PTRV) +
         [LDQ(T0, 56, T0),      # t0 = k0(P_PTRV)
          LDQ(A0, 0, T0),       # a0 = k0(P_PCB)
          LDQ(T1, 40, T0),      # t1 = k0(P_L3 + 24) (PTE addr)
          LDQ(T2, 48, T0),      # t2 = pte(P_DATA6 >> 13) (new PTE)
          CALL_PAL(0x30)] +     # swpctx -> installs ptbr
         load_const(T3, 0x6000) +
         [LDQ(T4, 0, T3),       # WARM TRANSLATION CACHE: loads VAL_E from 0x6000
          STQ(T2, 0, T1),       # REMAP: L3[3] -> P_DATA6 (holding VAL_F)
          LDA(A0, 2, ZERO)] +   # a0 = 2 (PAL_tbi DTB)
         load_const(A1, 0x6000) + # a1 = 0x6000
         [CALL_PAL(0x33)] +     # PAL_OSF1_tbi
         load_const(T5, VAL_S) +
         [LDQ(T5, 0, T3)])      # OBSERVING LOAD: reads 0x6000

cmds3 = setup + ["put w 0x%x, 0x%08x" % (k0(P_CODE) + 4 * i, op) for i, op in enumerate(prog3)]
cmds3 += ["pc=0x%x" % k0(P_CODE), "step %d" % len(prog3), "print t4", "print t5"]
t3txt, alive3 = session(cmds3)

t4_3 = printed(t3txt, "t4")
t5_3 = printed(t3txt, "t5")

row("pos fill", t4_3, "0x%x" % VAL_E,
    "CONTROL: initial walked load cached VAL_E")
row("pos obs", t5_3, "0x%x" % VAL_F,
    "CONTROL: positive selector (a0=2, a1=0x6000) flushes vaddr on both builds")

# ================================================================
# SESSIONS 4+ (#520 ACCEPT ROWS): two-page composite bound rows.
#
# WHY THESE EXIST.  The #520 fix ADDS a predicate:
#     if (a0 >= 1)  ->  if ((int64_t)a0 >= 1 && (int64_t)a0 <= 3)
# A bound-moving edit owes rows that pin the ACCEPT side, and the existing
# positive control (session 3, a0=2) CANNOT do it: its oracle is "the
# observing load returns the remapped value", and BOTH arms produce that.
# An INVALIDATE_ALL flushes the target page too, so session 3 detects an
# OMITTED invalidation and is blind to an OVER-invalidation.  It cannot
# tell the two arms apart at all.
#
# THE DISCRIMINATOR IS A SECOND, UNRELATED PAGE.
#   Page X (target)     the page named by a1; invalidated by BOTH arms
#   Page Y (unrelated)  VA 0x4000, PTE k0(P_L3+16), P_DATA3 (VAL_C) -> P_DATA4 (VAL_D)
# BOTH are warmed, then BOTH PTEs are rewritten, then tbi is called naming
# page X only.  So:
#     selective arm (INVALIDATE_VADDR, addr=a1): X flushed, Y SURVIVES -> obs Y = VAL_C
#     conservative arm (INVALIDATE_ALL):         X and Y both flushed  -> obs Y = VAL_D
# X reads its remapped value under BOTH arms, so X is the CONTROL (it proves
# the session ran and the target really was invalidated); Y is the ONE
# DISCRIMINATING OBSERVATION -- the only cell whose value differs between the
# arms, and therefore the only thing that can pin the guard.
#
# WHY THE MODEL SUPPORTS THE DISTINCTION (verified in the source, not assumed):
#   cpu_dyntrans.c DYNTRANS_INVALIDATE_TC(), non-MODE32 arm: INVALIDATE_VADDR
#   walks vph_tlb_entry[] and invalidates only entries whose
#   (vaddr_page & cpu->vaddr_mask) == (addr_page & cpu->vaddr_mask);
#   INVALIDATE_ALL walks the same array and invalidates every valid entry.
#   cpu_alpha.c does NOT set vaddr_mask, so cpu.c's default gives a 64-bit
#   CPU (int64_t)-1 -- an identity mask -- and 0x4000 differs from every
#   target page used here, so Y survives a selective invalidate.
#
# ---------------------------------------------------------------- AXIS SET
# THE ROW SET IS THE GUARD'S FULL AXIS SET, CLOSED IN ONE DIFF.
# Three consecutive review passes each found ONE more axis of this same
# guard -- the window's four sides, then the body's other lvalue, then
# operand magnitude.  Buying one cell per pass converges linearly and never
# terminates, so the axes are enumerated here and closed together:
#
#   AXIS                     cell                     row         mutant it kills
#   lower bound, accept      a0 = 1                   bnd lo      >=1 -> >=2
#   lower bound, reject      a0 = 0                   bnd zero    >=1 -> >=0
#   upper bound, accept      a0 = 3                   bnd hi      <=3 -> <=2
#   upper bound, reject      a0 = 4                   bnd out     <=3 -> <=4
#   interior                 a0 = 2                   bnd mid     && a0 != 2
#   negative selectors       a0 = -1, -2              tbia/tbiap  loss of the cast
#                                                     obs         (the original defect)
#   a1, zero vs non-zero     a0 = 2, a1 = 0           bnd a1z     && a1 != 0
#   a1, MAGNITUDE            a0 = 2, a1 = 0x8000      bnd a1hi    && a1 < 0x8000
#   a0, MAGNITUDE            a0 = 0x0000000100000001  bnd wide    (int32_t) cast,
#                                                                 and <=3 -> !=4
#
# WHY THE MAGNITUDE AXIS NEEDED ITS OWN ROW.  a0 was sampled only in [-2,4]
# and a1 only at {0, 0x6000}.  Narrowing either cast to 32 bits is INVISIBLE
# at all seven selector values the other rows drive -- verified by
# enumeration, zero disagreements -- because for any small value
# (int32_t)a0 == (int64_t)a0.  The smallest discriminating input is
# a0 = 0x0000000100000001: the shipped fix sees 4294967297, fails <= 3 and
# invalidates EVERYTHING, while a narrowed cast truncates to 1 and flushes a
# single page.  The same row kills a `<= 3' -> `!= 4' rewrite, which sends
# that value to the selective arm too.
#   load_const() builds only sign-extended 32-bit constants and CANNOT make
# that value, so this row loads a0 from memory with LDQ off the pointer
# vector -- no new instruction encoding is introduced anywhere in this file.
#
# WHY bnd a1hi IS SEPARATE FROM bnd a1z.  bnd a1z distinguishes only
# a1 == 0 from a1 != 0, so a conjunct with any OTHER a1 threshold escapes it.
# bnd a1hi drives a1 = 0x8000 and pins one such threshold.
#
# NOT ROWED, DISCLOSED (clause (e)) -- see the contract in the file header:
#   * the -1 vs -2 distinction, which this model cannot represent at all;
#   * selector values above 4 individually (same guard cell as a0 = 4);
#   * a1 thresholds other than 0 and 0x8000;
#   * multi-axis joints, where a0 and a1 are perturbed in one edit;
#   * the case-0x33 dispatch label, which is clause (e) here because the
#     palcode selector flows into no lvalue the guarded body reads and the
#     body never re-tests it.
#
# TRAP HANDLED (same as sessions 1-3): the whole guest sequence -- warm X,
# warm Y, remap X, remap Y, tbi, observe X, observe Y -- runs inside ONE
# `step N'.  Debugger interaction flushes the caches, so splitting it would
# destroy exactly what these rows measure.
#
# TRAP HANDLED: both observation registers are pre-seeded with VAL_S before
# the observing loads, so a load that never executes reads back as VAL_S
# rather than as a stale value that might coincide with a wanted one.
#
# TRAP HANDLED: the extra page-table entries these rows need are added to a
# LOCAL copy of `setup', so sessions 1-3 run on the byte-identical map they
# were witnessed against and rows 1-7 cannot be perturbed by this block.
# ================================================================

# Extra pages used only by sessions 4+.
P_DATA7    = 0x01068000  # a1=0 target (VPN 0), initial backing
P_DATA8    = 0x0106a000  # a1=0 target (VPN 0), remapped backing
P_DATA9    = 0x0106c000  # a1=0x8000 target (VPN 4), initial backing
P_DATA10   = 0x0106e000  # a1=0x8000 target (VPN 4), remapped backing
VAL_G = 0x999900009999
VAL_H = 0x888800008888
VAL_I = 0x111100001111
VAL_J = 0x222200002222

# The a0 magnitude probe value.  (int64_t) 4294967297 -> conservative arm;
# (int32_t) 1 -> selective arm.  load_const cannot build it; it is loaded
# from the pointer vector instead.
A0_WIDE = 0x0000000100000001

assert max(P_DATA7, P_DATA8, P_DATA9, P_DATA10) < 64 * 1024 * 1024, \
    "addresses must fit in RAM"

# Sessions 4+ additionally map VPN 0 and VPN 4, and publish their PTE
# addresses / new PTEs plus the wide a0 constant in further pointer-vector
# slots.  Sessions 1-3 keep the original `setup' untouched.
bsetup = setup + [
    "put d 0x%x, 0x%x" % (k0(P_L3 + 0),     pte(P_DATA7 >> PAGESHIFT)),
    "put d 0x%x, 0x%x" % (k0(P_L3 + 32),    pte(P_DATA9 >> PAGESHIFT)),
    "put d 0x%x, 0x%x" % (k0(P_DATA7 + 0),  VAL_G),
    "put d 0x%x, 0x%x" % (k0(P_DATA8 + 0),  VAL_H),
    "put d 0x%x, 0x%x" % (k0(P_DATA9 + 0),  VAL_I),
    "put d 0x%x, 0x%x" % (k0(P_DATA10 + 0), VAL_J),
    "put d 0x%x, 0x%x" % (k0(P_PTRV + 64),  k0(P_L3 + 0)),
    "put d 0x%x, 0x%x" % (k0(P_PTRV + 72),  pte(P_DATA8 >> PAGESHIFT)),
    "put d 0x%x, 0x%x" % (k0(P_PTRV + 80),  k0(P_L3 + 32)),
    "put d 0x%x, 0x%x" % (k0(P_PTRV + 88),  pte(P_DATA10 >> PAGESHIFT)),
    "put d 0x%x, 0x%x" % (k0(P_PTRV + 96),  A0_WIDE),
]
A0_WIDE_SLOT = 96

SYMBOL = {VAL_A: "A", VAL_B: "B", VAL_C: "C", VAL_D: "D", VAL_E: "E",
          VAL_F: "F", VAL_G: "G", VAL_H: "H", VAL_I: "I", VAL_J: "J",
          VAL_S: "S"}

def sym(hexstr):
    """Render an observed register as its VAL_* letter, or raw hex if unknown."""
    if hexstr == "absent":
        return "absent"
    return SYMBOL.get(int(hexstr, 16), hexstr)

# Registers beyond the ones sessions 1-3 use.  Names must match
# ALPHA_REG_NAMES in src/include/cpu_alpha.h, because the rows read them
# back with the debugger's `print' command.
T6, T7, T8, T9, T10 = 7, 8, 22, 23, 24     # t6, t7, t8, t9, t10

VA_Y = 0x4000                # unrelated page: the DISCRIMINATOR
Y_PTE_SLOT, Y_NEW_SLOT = 24, 32

# Target-page descriptors: (VA, pointer-vector slot holding its PTE address,
#                           slot holding its new PTE, initial value, remapped value)
X_AT_6000 = (0x6000, 40, 48, VAL_E, VAL_F)
X_AT_0000 = (0x0000, 64, 72, VAL_G, VAL_H)
X_AT_8000 = (0x8000, 80, 88, VAL_I, VAL_J)

def bound_session(a0_imm, a0_slot, xspec, a1val):
    """Warm X and Y, remap both, tbi(a0, a1val), observe both.  One `step'.

    a0 is set either from an immediate (LDA) or, when the value cannot be
    built by load_const, from a pointer-vector slot (LDQ).  Exactly one of
    a0_imm / a0_slot is not None.  Both forms are ONE instruction, so the
    step count is unaffected.
    """
    assert (a0_imm is None) != (a0_slot is None), "give exactly one a0 source"
    va_x, x_pte_slot, x_new_slot, _x_init, _x_new = xspec
    set_a0 = LDA(A0, a0_imm, ZERO) if a0_slot is None else LDQ(A0, a0_slot, T0)
    prog = (load_const(T0, P_PTRV) +
            [LDQ(T0, 56, T0),              # t0 = k0(P_PTRV)  (kept live throughout)
             LDQ(A0, 0,  T0),              # a0 = k0(P_PCB)   (swpctx argument)
             LDQ(T1, x_pte_slot, T0),      # t1 = PTE address, page X
             LDQ(T2, x_new_slot, T0),      # t2 = new PTE,     page X
             LDQ(T6, Y_PTE_SLOT, T0),      # t6 = PTE address, page Y
             LDQ(T7, Y_NEW_SLOT, T0),      # t7 = new PTE,     page Y
             CALL_PAL(0x30)] +             # swpctx -> installs ptbr (and ALL-flushes)
            load_const(T3, va_x) +
            load_const(T8, VA_Y) +
            [LDQ(T4, 0, T3),               # WARM X
             LDQ(T9, 0, T8),               # WARM Y
             STQ(T2, 0, T1),               # REMAP X
             STQ(T7, 0, T6),               # REMAP Y
             set_a0] +                     # a0 = selector under test
            load_const(A1, a1val) +        # a1 = the page X is at (names X only)
            [CALL_PAL(0x33)] +             # PAL_OSF1_tbi
            load_const(T5,  VAL_S) +       # pre-seed observation X
            load_const(T10, VAL_S) +       # pre-seed observation Y
            [LDQ(T5,  0, T3),              # OBSERVE X (control)
             LDQ(T10, 0, T8)])             # OBSERVE Y (DISCRIMINATOR)

    cmds = bsetup + ["put w 0x%x, 0x%08x" % (k0(P_CODE) + 4 * i, op)
                     for i, op in enumerate(prog)]
    cmds += ["pc=0x%x" % k0(P_CODE), "step %d" % len(prog),
             "print t4", "print t9", "print t5", "print t10"]
    txt, alive = session(cmds)
    return (alive,
            printed(txt, "t4"),    # fill X
            printed(txt, "t9"),    # fill Y
            printed(txt, "t5"),    # observe X
            printed(txt, "t10"))   # observe Y

# (a0 immediate, a0 slot, a1, target page, row name, expected Y, note)
# Expected Y is VAL_C when the selective arm must run (Y survives) and VAL_D
# when the conservative arm must run (Y is flushed and re-walks).
BOUND_ROWS = [
    (0, None, 0x6000, X_AT_6000, "bnd zero", VAL_D,
     "ACCEPT: a0=0 undefined -> ALL, Y must DIE (catches >=1 grown to >=0)"),
    (1, None, 0x6000, X_AT_6000, "bnd lo",   VAL_C,
     "ACCEPT: a0=1 (architecturally ITB; this model has one unified cache -- see the ITB/DTB note in the header), Y must SURVIVE (catches >=1 grown to >=2)"),
    (2, None, 0x6000, X_AT_6000, "bnd mid",  VAL_C,
     "ACCEPT: a0=2 (architecturally DTB; unified here -- see the header note), Y must SURVIVE (catches a window excluding 2)"),
    (3, None, 0x6000, X_AT_6000, "bnd hi",   VAL_C,
     "ACCEPT: a0=3 both selective, Y must SURVIVE (catches <=3 shrunk to <=2)"),
    (4, None, 0x6000, X_AT_6000, "bnd out",  VAL_D,
     "ACCEPT: a0=4 undefined -> ALL, Y must DIE (catches <=3 grown to <=4)"),
    (2, None, 0x0000, X_AT_0000, "bnd a1z",  VAL_C,
     "ACCEPT: a0=2 with a1=0 still selective, Y must SURVIVE (catches a conjunct on a1)"),
    (2, None, 0x8000, X_AT_8000, "bnd a1hi", VAL_C,
     "ACCEPT: a0=2 with a1=0x8000 selective, Y must SURVIVE (catches an a1 threshold)"),
    (None, A0_WIDE_SLOT, 0x6000, X_AT_6000, "bnd wide", VAL_D,
     "ACCEPT: a0=0x100000001 -> ALL, Y must DIE (catches a 32-bit cast, and <=3 -> !=4)"),
]

for a0_imm, a0_slot, a1val, xspec, name, want_y, note in BOUND_ROWS:
    x_init, x_new = xspec[3], xspec[4]
    alive_b, fill_x, fill_y, obs_x, obs_y = bound_session(a0_imm, a0_slot, xspec, a1val)
    got  = "%s %s %s %s %s" % ("alive" if alive_b else "died",
                               sym(fill_x), sym(fill_y), sym(obs_x), sym(obs_y))
    want = "alive %s %s %s %s" % (SYMBOL[x_init], SYMBOL[VAL_C],
                                  SYMBOL[x_new], SYMBOL[want_y])
    row(name, got, want, note)
    a0desc = ("0x%x" % a0_imm) if a0_slot is None else ("0x%x (from PTRV+%d)"
                                                       % (A0_WIDE, a0_slot))
    # Raw values kept in the log so a future reader can re-derive the row
    # without trusting the symbol table above.
    print("%-16s %s" % ("", "  raw: fillX=%s fillY=%s obsX=%s obsY=%s  (live=%s, a0=%s, a1=0x%x, VA_X=0x%x)"
                        % (fill_x, fill_y, obs_x, obs_y, alive_b, a0desc, a1val, xspec[0])))

bad = [n for n, ok in rows if not ok]
print("\nALPHATBI_RESULT=%d/%d" % (len(rows) - len(bad), len(rows)))
if bad:
    print("FAILING: " + " ".join(bad))
print("ALPHATBI_DONE")
sys.exit(0 if not bad else 1)
