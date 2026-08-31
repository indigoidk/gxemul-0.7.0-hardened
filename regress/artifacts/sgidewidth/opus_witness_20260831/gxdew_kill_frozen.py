#!/usr/bin/env python3
"""sgidewidth kill table -- one row per channel.  Prints  name got want ok."""
import sys
sys.path.insert(0, "/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad")
from gxprobe import Emu

BIN = sys.argv[1]; TAG = sys.argv[2]
SCRATCH = 0xffffffff80010000; NOPS = "/tmp/gxdew_nops.bin"
ARGS = ["-V","-E","sgi","-e","ip32","0x%x:%s" % (SCRATCH,NOPS)]
DE   = 0xffffffffb5002000     # sgi_de  @ phys 0x15002000
RE   = 0xffffffffb5001000     # sgi_re  @ phys 0x15001000
W = {"sb":0xa0220000,"sh":0xa4220000,"sw":0xac220000,"sd":0xfc220000,
     "lbu":0x90220000,"lhu":0x94220000,"lw":0x8c220000,"ld":0xdc220000}
SENT = 0xa5a5a5a5
DECL = "sgi_de: unimplemented len="      # the fix's decline announcement
KILL = "sgi_de: len = "                  # the pre-fix host kill
DRAW = "sgi_de: UNIMPLEMENTED drawing op = 0x00000000"
SCIS = "sgi_de: TODO: non-zero CRIME_DE_SCISSOR"

rows=[]
def check(n,g,w,note=""):
    ok=(g==w); rows.append((n,g,w,ok))
    print("  %-14s %-4s got=%-22r want=%-22r %s"%(n,"ok" if ok else "FAIL",g,w,note),flush=True)

def E():
    return Emu(BIN,ARGS,preset={"scratch":SCRATCH},boot_wait=3.0,default_wait=0.30)
def go(e,insn,addr,v0=None,wait=0.8):
    if v0 is not None: e.set_reg("v0",v0)
    e.set_reg("at",addr); e.set_reg("pc",e.word_at(W[insn])); return e.send("step",wait)
def rd(e):
    e._reg_cache.pop("v0",None); return e.read_reg("v0")
def fin(e):
    st=e.wait_exit(timeout=2.0); t=e.text; e.close(); return st,t

print("=== %s ===" % TAG, flush=True)

# ---- CONTROL 1: LIVENESS -- a known value returns through the same decode
e=E(); go(e,"sw",DE+0x0d0,v0=0xdeadbeef); go(e,"lw",DE+0x0d0,v0=SENT)
v=rd(e); st,t=fin(e)
check("live", None if v is None else v & 0xffffffff, 0xdeadbeef, "LIVENESS")

# ---- CONTROL 2: DEVICE SIGNATURE -- RAM cannot emit this, and it echoes our value
e=E(); go(e,"sw",DE+0x048,v0=0x12345678); st,t=fin(e)
check("devsig", t.count(SCIS+": 0x0000000012345678"), 1, "DEVICE-SIGNATURE")

# ---- LOWER HALF (startFlag CLEAR): the width kill itself
e=E(); go(e,"sb",DE+0x0d0,v0=0x5a); st,t=fin(e)
check("lo_kill",   t.count(KILL+"1 not implemented"), 1 if TAG=="base" else 0)
check("lo_decl",   t.count(DECL+"1 -- declined"),     0 if TAG=="base" else 1)
check("lo_alive",  st, ("exit",1) if TAG=="base" else ("running",None))

# ---- SENTINEL READ: a declined READ must answer 0, not leave the reg untouched
if TAG!="base":
    e=E(); go(e,"lbu",DE+0x0d0,v0=SENT); v=rd(e); st,t=fin(e)
    check("lo_sent", v, 0, "0=declined+answered; 0xa5a5a5a5=guest bus error")

# ---- LATCH: two declined accesses at DIFFERENT offsets -> ONE message
if TAG!="base":
    e=E(); go(e,"sb",DE+0x0d0,v0=1); go(e,"sb",DE+0x0e4,v0=2); st,t=fin(e)
    check("lo_latch", t.count(DECL), 1, "N=1 per device instance")

# ---- UPPER HALF (startFlag SET): THE DISCRIMINATOR for the tail
e=E(); go(e,"sb",DE+0x8d0,v0=0x5a,wait=1.2); st,t=fin(e)
check("hi_kill",  t.count(KILL+"1 not implemented"), 1 if TAG=="base" else 0)
check("hi_draw",  t.count(DRAW), 0, "a DECLINED access must not draw")
check("hi_alive", st, ("exit",1) if TAG=="base" else ("running",None))

# ---- TAIL ACCEPT ROW: an ACCEPTED width with startFlag must STILL draw
e=E(); go(e,"sw",DE+0xfd0,v0=0x11223344,wait=1.2); st,t=fin(e)
check("tail_acc",  t.count(DRAW), 1, "accepted width still reaches draw_primitive")
check("tail_acc_x",st, ("exit",1), "(that kill is sgirekills/BADVAL, not this row's)")

# ---- SWITCH SIDE EFFECT: does a DECLINED write still announce a TODO?
e=E(); go(e,"sb",DE+0x048,v0=0x01,wait=1.0); st,t=fin(e)
check("dec_switch", t.count(SCIS), 0,
      "a declined write must not announce a TODO about a write that never happened")

# ---- ACCEPT ROWS at the LAST legal slot of the reachable window --------
e=E(); go(e,"sw",DE+0x7fc,v0=0xcafebabe); go(e,"lw",DE+0x7fc,v0=SENT)
v=rd(e); st,t=fin(e)
check("acc4_last", None if v is None else v & 0xffffffff, 0xcafebabe,
      "len=4 W+R at +0x7fc, the last 4-slot with startFlag CLEAR")

e=E(); go(e,"sd",DE+0x7f8,v0=0x1122334455667788)
go(e,"lw",DE+0x7f8,v0=SENT); vhi=rd(e)
go(e,"lw",DE+0x7fc,v0=SENT); vlo=rd(e)
st,t=fin(e)
check("acc8_hi32", None if vhi is None else vhi & 0xffffffff, 0x11223344,
      "len=8 write lands in de_reg[regnr]")
check("acc8_lo32", None if vlo is None else vlo & 0xffffffff, 0x55667788,
      "...and de_reg[regnr+1]")

e=E(); go(e,"sd",DE+0x7f8,v0=0x1122334455667788); go(e,"ld",DE+0x7f8,v0=SENT)
v=rd(e); st,t=fin(e)
check("acc8_read", v, 0x1122334455667788, "len=8 READ direction, last 8-slot")

# ---- SHARED-LATCH row: trip sgi_re's TLB_A decline first
e=E(); go(e,"sb",RE+0x000,v0=0x5a,wait=1.0); go(e,"sb",DE+0x0d0,v0=0x5a,wait=1.0)
st,t=fin(e)
check("re_first", t.count("sgi_re: unimplemented len=1 for CRIME_RE_TLB_A"),
      1 if TAG!="base" else 1, "#497's own latch (present on every build)")
check("sharedlatch", t.count(DECL), 0 if TAG=="base" else 1,
      "sgi_de must keep its OWN latch bit, not #497's")

n_ok=sum(1 for r in rows if r[3])
print("SCORE %s: %d/%d" % (TAG,n_ok,len(rows)), flush=True)
print("KILLTABLE_ROW %s %d %d" % (TAG,n_ok,len(rows)))
