#!/usr/bin/env python3
"""Does #95 (memory_rw.c) supply the value a DECLINED device read returns?
   z0: #95 fills 0x00.   za: #95 fills 0xa5.   Both use the early-`return 1'
   decline, so the sgi_de handler never touches the caller's buffer."""
import sys
sys.path.insert(0,"/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad")
from gxprobe import Emu
SCRATCH=0xffffffff80010000; NOPS="/tmp/gxdew_nops.bin"
ARGS=["-V","-E","sgi","-e","ip32","0x%x:%s"%(SCRATCH,NOPS)]
DE=0xffffffffb5002000
W={"lbu":0x90220000,"lhu":0x94220000,"sw":0xac220000,"lw":0x8c220000}
SENT=0xa5a5a5a5
def one(binp, insn, off, v0):
    e=Emu(binp,ARGS,preset={"scratch":SCRATCH},boot_wait=3.0,default_wait=0.30)
    e.set_reg("v0",v0); e.set_reg("at",DE+off); e.set_reg("pc",e.word_at(W[insn]))
    e.send("step",0.8); e._reg_cache.pop("v0",None); v=e.read_reg("v0"); e.close(); return v
for tag,binp in (("z0","/tmp/gxdew_bin_z0"),("za","/tmp/gxdew_bin_za")):
    #  three repeats: a NONDETERMINISTIC stack-garbage answer would vary
    r1 = [one(binp,"lbu",0x0d0,SENT) for _ in range(3)]
    r2 = [one(binp,"lhu",0x0d0,SENT) for _ in range(3)]
    #  control: an ACCEPTED width read of a register we just wrote must still work
    print("%s  lbu(declined,len=1) x3 = %s   lhu(declined,len=2) x3 = %s" %
          (tag, [hex(x) if x is not None else None for x in r1],
                [hex(x) if x is not None else None for x in r2]), flush=True)
print("MZ_PROBE_DONE")
