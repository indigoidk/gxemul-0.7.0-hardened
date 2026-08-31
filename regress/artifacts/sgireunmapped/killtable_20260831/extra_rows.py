#!/usr/bin/env python3
"""extra_rows.py <gxemul-binary> <label>

FOUR rows the shipped detector does not contain, each with the mutant it
kills and the observable that differs -- written to test two predictions
made BEFORE any table ran:

  X1 `tlb2 narrow'  kills M4 bitcollide.  Two NARROW accesses in ONE emu,
     one in TLB_A and one in TLB_B.  With distinct latch bits both arms
     announce; with SGIRE_W_TLBA_LEN == SGIRE_W_TLBB_LEN the second is
     silently suppressed.  channel: count of the TLB_B decline text.
     THE ACCEPT ROWS CANNOT SEE THIS -- they perform ONE 8-byte access in
     a FRESH emulator, so no width guard is entered and no latch is set.
  X2 `tlb1 narrow'  the CONTROL for X1: the FIRST decline must still fire
     under the collision, which is what makes X1's kill attributable to
     suppression rather than to the session never reaching the guards.
  X3 `de/unmap latch' kills fix6.  A `sb' to sgi_de (len=1 -> #498 decline,
     sets SGIRE_W_DE_LEN) followed by an unmapped sgi_re write.  If the
     catch-all's new latch bit is 1<<6 it collides with SGIRE_W_DE_LEN --
     which DEVICE_ACCESS(sgi_de) shares via the same `struct sgi_re_data'
     -- and the sgi_re announcement is suppressed.
  X4 the CONTROL for X3: the sgi_de decline itself must fire.
"""
import os, sys
sys.path.insert(0, "/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad")
from gxprobe import Emu, EmuDied

BIN   = sys.argv[1]
LABEL = sys.argv[2]
HERE  = os.path.dirname(os.path.abspath(__file__))
NOPS  = os.path.join(HERE, "nops.bin")
SCRATCH = 0xffffffff80010000
def kseg1(p): return 0xffffffffa0000000 | p

RE_BASE = 0x15000000
RE      = RE_BASE + 0x1000          # sgi_re window; handler adds 0x1000 back
DE      = RE_BASE + 0x2000          # sgi_de window

W_SD = 0xfc220000       # sd  $v0, 0($at)
W_SW = 0xac220000       # sw  $v0, 0($at)   -> len 4
W_SB = 0xa0220000       # sb  $v0, 0($at)   -> len 1

rows = []
def row(name, got, want, chan):
    ok = (got == want)
    rows.append((name, ok))
    print("  %-14s %-22s got=%-24s want=%-24s %s" %
          (name, LABEL, str(got), str(want), "ok" if ok else "FAIL"))

def emu(tag):
    return Emu(BIN, ["-E","sgi","-e","ip32","-V","0x%x:%s"%(SCRATCH,NOPS)],
               log_path=os.path.join(HERE,"x_%s_%s.txt"%(LABEL,tag)), boot_wait=3.0)

def acc(e, word, addr, val=0x5a5a5a5a):
    e.set_reg("v0", val); e.set_reg("at", addr)
    a = e.word_at(word)
    e._reg_cache.pop("pc", None)
    e.set_reg("pc", a)
    out = e.send("step", 0.35)
    e._reg_cache.pop("pc", None)
    return out

MSG_W  = "unimplemented write to address"
MSG_A  = "CRIME_RE_TLB_A -- declined"
MSG_B  = "CRIME_RE_TLB_B -- declined"
MSG_DE = "sgi_de: unimplemented len"

# ---- X1 / X2 : two narrow accesses, two DIFFERENT windows, ONE emu --------
e = emu("x12")
try:
    acc(e, W_SW, kseg1(RE + 0x000))      # relative_addr 0x1000 -> TLB_A, len 4
    acc(e, W_SW, kseg1(RE + 0x200))      # relative_addr 0x1200 -> TLB_B, len 4
except EmuDied:
    pass
e.drain(0.4)
row("tlb1 narrow", e.count(MSG_A), 1, "count of the TLB_A decline (control)")
row("tlb2 narrow", e.count(MSG_B), 1, "count of the TLB_B decline")
e.close()

# ---- X3 / X4 : sgi_de narrow decline, THEN an unmapped sgi_re write -------
e = emu("x34")
try:
    acc(e, W_SB, kseg1(DE + 0x000))      # sgi_de len=1 -> #498 decline, sets DE bit
    acc(e, W_SD, kseg1(RE + 0x800))      # sgi_re catch-all write
except EmuDied:
    pass
e.drain(0.4)
row("de decline", e.count(MSG_DE), 1, "count of the sgi_de decline (control)")
row("de/unmap latch", e.count(MSG_W), 1, "count of the catch-all write announcement")
e.close()

n = sum(1 for _, ok in rows if ok)
print("XSCORE %s: %d/%d" % (LABEL, n, len(rows)))
print("EXTRA_DONE")
