import sys, re
SRC="/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/sh_pclock_probe.py"
BIN=sys.argv[1]; LABEL=sys.argv[2]
src=open(SRC).read()
cut=src.index("#  ---------------------------------------------------------------- controls")
g={"__name__":"x"}; sys.argv=[SRC,BIN,"/mnt/c/DocumentNoSnc/CC/GXEMUL/_images/openbsd76-landisk-bsd.rd"]
exec(src[:cut], g)
session, printed = g["session"], g["printed"]
AT=0x8c001000; BRA_SELF, NOP = g["BRA_SELF"], g["NOP"]
def prog(ctrl, ctrlval=0x0c, ndata=8):
    ops=[0x2781]*ndata + [0x2a90, 0x6210, 0x6430, 0x6650, BRA_SELF, NOP]
    cmds=["r7=0xb4000000","r8=0x1234","r10=0x%x"%ctrl,"r9=0x%x"%ctrlval,
          "r1=0xb400000e","r3=0xb400002c","r5=0xb4000206","r2=0xaa","r4=0xaa","r6=0xaa"]
    cmds+=["put h 0x%x, 0x%04x"%(AT+2*i,op) for i,op in enumerate(ops)]
    cmds+=["pc=0x%x"%AT, "step %d"%(ndata+4), "print r2","print r4","print r6"]
    return cmds
for tag, ctrl in [("ctl@0x2c",0xb400002c),("ctl@0x206",0xb4000206),("noctl(RAM)",0x8c002000)]:
    t,alive=session(prog(ctrl),machine="landisk",flag="-E")
    alt=[l for l in t.split("\n") if "wdc" in l.lower() and ("CTRL" in l or "ALT" in l or "unmapped" in l.lower())]
    um=[l for l in t.split("\n") if "nmapped" in l or "no memory" in l.lower()]
    print("%s %-11s alive=%s status(0xe)=%s alt@0x2c=%s alt@0x206=%s | %s | %s"%(LABEL,tag,alive,printed(t,"r2"),printed(t,"r4"),printed(t,"r6"),
          " / ".join(x.strip() for x in alt)[:200], " / ".join(x.strip() for x in um)[:200]))
print("LANDISK_DONE")
