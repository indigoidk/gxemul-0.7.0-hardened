#!/usr/bin/env python3
"""
detector.py <gxemul-binary> <label>
A candidate DETECTOR for the sgireunmapped fix, plus the rows the brief's
stated pin-set does NOT contain.  Every row names the mutant it kills and the
observable that differs under it (the CHANNEL line).
"""
import os, sys, time
sys.path.insert(0, "/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad")
from gxprobe import Emu, EmuDied

BIN   = sys.argv[1]
LABEL = sys.argv[2]
HERE  = os.path.dirname(os.path.abspath(__file__))
NOPS  = os.path.join(HERE, "nops.bin")
SCRATCH = 0xffffffff80010000
def kseg1(p): return 0xffffffffa0000000 | p
RE = 0x15001000

W_SD = 0xfc220000; W_LW = 0x8c220000; W_SW = 0xac220000

rows = []
def row(name, got, want, chan):
    ok = (got == want)
    rows.append((name, ok))
    print("  %-14s %-22s got=%-24s want=%-24s %s" %
          (name, LABEL, str(got), str(want), "ok" if ok else "FAIL"))

def emu(tag):
    return Emu(BIN, ["-E","sgi","-e","ip32","-V","0x%x:%s"%(SCRATCH,NOPS)],
               log_path=os.path.join(HERE,"d_%s_%s.txt"%(LABEL,tag)), boot_wait=3.0)

def acc(e, word, addr, val=0x5a5a5a5a):
    """One genuine guest instruction at `addr`.

    THE pc CACHE MUST BE INVALIDATED BY HAND.  gxprobe caches register
    assignments and skips redundant ones; `step' advances pc, so a second
    call with the SAME instruction word finds pc already "set" to that
    address and SKIPS the assignment -- executing the following nop instead
    of the store.  gxprobe's own _exec_at() pops it; this driver steps
    directly, so it must too.  MEASURED: without this the `msg once' row
    performed ONE access and two nops, and therefore COULD NOT FAIL --
    mnolatch (announce, never latch) scored a clean sweep because of it.
    """
    e.set_reg("v0", val); e.set_reg("at", addr)
    a = e.word_at(word)
    e._reg_cache.pop("pc", None)
    e.set_reg("pc", a)
    out = e.send("step", 0.35)
    e._reg_cache.pop("pc", None)
    return out

MSG_W = "unimplemented write to address"
MSG_R = "unimplemented read from address"

# R1 survive-write   kills: the shipped exit(1)      channel: host exit status
e = emu("r1")
try: acc(e, W_SD, kseg1(RE+0x800))
except EmuDied: pass
e.drain(0.3); row("survive w", e.wait_exit(1.2)[0], "running", "host exit status")
e.close()

# R2 survive-read
e = emu("r2")
try: acc(e, W_LW, kseg1(RE+0x800), 0)
except EmuDied: pass
e.drain(0.3); row("survive r", e.wait_exit(1.2)[0], "running", "host exit status")
e.close()

# R3-VACUOUS  read-returns-0 with v0 PRE-SET TO 0.  This is the naive form of
#             the brief's pin.  It cannot tell a serviced read from a DBE that
#             never wrote v0, because v0 was already 0.
e = emu("r3v")
try:
    acc(e, W_LW, kseg1(RE+0x800), 0)     # v0 pre-set 0
    e._reg_cache.pop("v0", None); v = e.read_reg("v0")
except EmuDied: v = None
row("read0 VACUOUS", "0x%x"%(v or 0), "0x0", "v0 after load, pre-set 0")
e.close()

# R3-REAL     same read, v0 PRE-SET NONZERO.  A DBE leaves v0 untouched, so the
#             sentinel survives and the row reds.  kills: M_ret0
e = emu("r3")
try:
    acc(e, W_LW, kseg1(RE+0x800), 0xa5a5a5a5)
    e._reg_cache.pop("v0", None); v = e.read_reg("v0")
except EmuDied: v = None
row("read0 REAL", "0x%x"%(v if v is not None else 0xdead), "0x0",
    "v0 after load, pre-set 0xa5a5a5a5")
e.close()

# R4 no-DBE   the declined read must NOT raise a guest bus error. kills: M_ret0
e = emu("r4")
try: acc(e, W_LW, kseg1(RE+0x800), 0xa5a5a5a5)
except EmuDied: pass
e.drain(0.3)
row("no DBE", ("exception DBE" in e.raw_text) or ("DBE" in e.raw_text), False,
    "guest exception text")
e.close()

# R5 msg-once two DIFFERENT unmapped writes -> exactly one announcement
e = emu("r5")
try:
    acc(e, W_SD, kseg1(RE+0x800)); acc(e, W_SD, kseg1(RE+0x900))
except EmuDied: pass
e.drain(0.3); row("msg once", e.count(MSG_W), 1, "count of write announcement")
e.close()

# R6 LATCH-COLLISION.  Touch TEX with a NARROW access first (sets the #497 TEX
#    latch), THEN hit the catch-all.  If the fix reuses an existing bit the
#    announcement is silently suppressed.  kills: M_latch
e = emu("r6")
try:
    acc(e, W_SW, kseg1(RE+0x600))          # len=4 in TEX -> #497 decline, sets TEX bit
    acc(e, W_SD, kseg1(RE+0x800))          # catch-all
except EmuDied: pass
e.drain(0.3)
row("latch fresh", e.count(MSG_W), 1, "announcement after a TEX narrow access")
e.close()

# R7 DIRECTION PARITY.  Read side must also be de-fatalised. kills: M_wonly
e = emu("r7")
try: acc(e, W_LW, kseg1(RE+0x900), 0xa5a5a5a5)
except EmuDied: pass
e.drain(0.3)
st = e.wait_exit(1.2)[0]
row("read defatal", st, "running", "host exit status on a READ")
e.close()

# R8..R12 ACCEPT ROWS (de-escalation).  The old exit(1) was an ACCIDENTAL
#    tripwire: before the fix, shrinking any window bound meant a host kill on
#    the first legal access.  Afterwards it is a SILENT refusal, so the fix owes
#    a row per de-fatalised predicate proving legal accesses still land.
#
#    THE ANCHOR LESSON, MEASURED: the first draft of this row wrote to the
#    window's BASE (0x1700) and scored 9/9 against a mutant that halved the
#    window -- a base-anchored accept row CANNOT see the far bound move.  Each
#    row below therefore uses the LAST 8-byte slot of its window.
ACCEPTS = [
    ("accept tlba", 0x1f8, "TLB_A  top slot 0x11f8"),
    ("accept tlbb", 0x3f8, "TLB_B  top slot 0x13f8"),
    ("accept tlbc", 0x5f8, "TLB_C  top slot 0x15f8"),
    ("accept tex",  0x6d8, "TEX    top slot 0x16d8"),
    ("accept lina", 0x778, "LIN_A  top slot 0x1778"),
    ("accept linb", 0x7f8, "LIN_B  top slot 0x17f8"),
]
for nm, off, note in ACCEPTS:
    e = emu(nm.replace(" ", "_"))
    try:
        acc(e, W_SD, kseg1(RE + off), 0x11223344)
    except EmuDied:
        pass
    e.drain(0.3)
    hit = (MSG_W in e.raw_text) or (e.wait_exit(1.0)[0] == "exit")
    row(nm, hit, False, note + " must NOT reach the catch-all")
    e.close()

n = sum(1 for _,ok in rows if ok)
print("SCORE %s: %d/%d" % (LABEL, n, len(rows)))
print("DETECTOR_DONE")
