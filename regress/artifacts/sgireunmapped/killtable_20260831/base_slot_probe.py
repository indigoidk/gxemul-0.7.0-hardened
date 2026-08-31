#!/usr/bin/env python3
"""base_slot_probe.py <bin> <label>
ONE row: the same accept test, at the window's BASE slot instead of its top.
If this reds where `accept lina' stayed green, the detector's blindness is to
the NEAR bound specifically, not to the mutant."""
import os, sys
sys.path.insert(0, "/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad")
from gxprobe import Emu, EmuDied
BIN, LABEL = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
NOPS = os.path.join(HERE, "nops.bin")
SCRATCH = 0xffffffff80010000
def kseg1(p): return 0xffffffffa0000000 | p
RE = 0x15001000
W_SD = 0xfc220000
MSG_W = "unimplemented write to address"
e = Emu(BIN, ["-E","sgi","-e","ip32","-V","0x%x:%s"%(SCRATCH,NOPS)],
        log_path=os.path.join(HERE,"b_%s.txt"%LABEL), boot_wait=3.0)
try:
    e.set_reg("v0", 0x11223344); e.set_reg("at", kseg1(RE + 0x700))   # LIN_A BASE
    a = e.word_at(W_SD); e._reg_cache.pop("pc", None); e.set_reg("pc", a)
    e.send("step", 0.35)
except EmuDied:
    pass
e.drain(0.4)
hit = (MSG_W in e.raw_text) or (e.wait_exit(1.0)[0] == "exit")
print("  %-14s %-22s got=%-24s want=%-24s %s" %
      ("lina BASE slot", LABEL, str(hit), "False", "ok" if hit is False else "FAIL"))
e.close()
print("BASESLOT_DONE")
