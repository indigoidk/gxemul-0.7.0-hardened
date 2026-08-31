#!/usr/bin/env python3
"""ATTRIBUTION probe: is the extra kill the WIDTH guard or the TAIL?
   Same offset, same instruction, only the 0x800 CRIME_DE_START bit differs."""
import sys, os
sys.path.insert(0, "/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad")
from gxprobe import Emu
BIN = sys.argv[1]; SCRATCH = 0xffffffff80010000; NOPS = "/tmp/gxdew_nops.bin"
ARGS = ["-V","-E","sgi","-e","ip32","0x%x:%s" % (SCRATCH,NOPS)]
DE = 0xffffffffb5002000
W = {"sb":0xa0220000,"sh":0xa4220000,"sw":0xac220000,"sd":0xfc220000,
     "lbu":0x90220000,"lhu":0x94220000,"lw":0x8c220000,"ld":0xdc220000,
     "ldl":0x68220000,"ldr":0x6c220000}
rows=[]
def check(n,g,w,note=""):
    ok=(g==w); rows.append((n,ok))
    print("%-16s %-4s got=%-24r want=%-24r %s"%(n,"ok" if ok else "FAIL",g,w,note),flush=True)
def run(insn, off, v0=0x11223344, wait=1.0):
    e=Emu(BIN,ARGS,preset={"scratch":SCRATCH},boot_wait=3.0,default_wait=0.30)
    e.set_reg("v0",v0); e.set_reg("at",DE+off)
    e.set_reg("pc", e.word_at(W[insn])); e.send("step",wait)
    st=e.wait_exit(timeout=2.0)
    t=e.text; e.close()
    return st, t

#  Pair 1: identical instruction+alignment, offsets differing ONLY in bit 0x800
for insn, lo, hi in (("sd",0x7f8,0xff8), ("ldl",0x7fd,0xffd), ("ldr",0x7fd,0xffd),
                     ("sw",0x7d0,0xfd0), ("lw",0x7d0,0xfd0)):
    st_lo,t_lo = run(insn, lo)
    st_hi,t_hi = run(insn, hi)
    check("%s@0x%03x"%(insn,lo), st_lo, ("running",None), "startFlag CLEAR -> survives")
    check("%s@0x%03x"%(insn,hi), st_hi, ("exit",1),      "startFlag SET   -> dies")
    check("%s_hi_why"%insn, t_hi.count("sgi_de: UNIMPLEMENTED drawing op = 0x00000000"), 1,
          "and it dies in draw_primitive(), NOT in the width guard")
    check("%s_hi_nowidth"%insn,
          sum(t_hi.count("sgi_de: len = %d not implemented"%n) for n in (1,2,3,5,6,7)), 0,
          "no width message at all -- this kill is width-independent")

#  Pair 2: a DECLINED width in each half.  Lower half: width kill only.
st,t = run("sb", 0x7d0)
check("sb@0x7d0_msg", t.count("sgi_de: len = 1 not implemented"), 1, "width kill")
check("sb@0x7d0_die", st, ("exit",1), "")
st,t = run("sb", 0xfd0)
check("sb@0xfd0_msg", t.count("sgi_de: len = 1 not implemented"), 1,
      "upper half: width kill fires FIRST, so the tail is never reached today")
check("sb@0xfd0_die", st, ("exit",1), "")

print("\nSUMMARY: %d/%d ok"%(sum(1 for r in rows if r[1]),len(rows)))
print("DEWPROBE2_DONE")
