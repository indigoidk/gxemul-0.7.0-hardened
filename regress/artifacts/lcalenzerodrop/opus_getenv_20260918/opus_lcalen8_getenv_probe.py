import sys
SRC="/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/lca_isalane_probe.py"
lines=open(SRC,encoding="utf-8").read().split("\n")[:459]
sys.argv=[SRC, sys.argv[1], sys.argv[2]]
g={"__file__":SRC,"__name__":"x"}
exec("\n".join(lines), g)
T0,T1,T2,T3,T4,T5=g["T0"],g["T1"],g["T2"],g["T3"],g["T4"],g["T5"]
LDQ,STB,LDBU,sent,k0,SP,run=g["LDQ"],g["STB"],g["LDBU"],g["sent"],g["k0"],g["SP"],g["run"]
A0,A1,A2,A3=16,17,18,19
CALLPAL_PROM=0x03fffffe
RA=26
CODE=g["CODE"]
def mk(ra1, ra2):
    c=[k0(SP(0x3ff)), 0x5a, 0x22, 6, 64, g["SCRATCH"]+0x100, ra1, ra2]
    ph=[([LDQ(T1,0,T0),LDQ(T2,8,T0),STB(T2,0,T1)]+sent(T3)+[LDBU(T3,0,T1)],"t3"),
        ([LDQ(A0,16,T0),LDQ(A1,24,T0),LDQ(A2,0,T0),LDQ(A3,32,T0),LDQ(RA,48,T0),CALLPAL_PROM],"v0"),
        (sent(T4)+[LDBU(T4,0,T1)],"t4"),
        ([LDQ(A0,16,T0),LDQ(A1,24,T0),LDQ(A2,40,T0),LDQ(A3,32,T0),LDQ(RA,56,T0),CALLPAL_PROM,LDQ(T5,0x100,T0)],"t5")]
    return c,ph
c,ph=mk(0,0)
prog=g["load_const"](T0,g["SCRATCH"])
for o,_ in ph: prog+=o
idx=[i for i,w in enumerate(prog) if w==CALLPAL_PROM]
consts,ph=mk(k0(CODE)+4*(idx[0]+1), k0(CODE)+4*(idx[1]+1))
txt,alive,ret=run("getenv",consts,ph,["t3","v0","t4","t5"])
P=g["printed"]
print("LABEL",sys.argv[2],"alive",alive,"retried",ret)
print("seed SCR   t3 =",hex(P(txt,"t3") or -1))
print("getenv v0     =",hex(P(txt,"v0") or -1))
print("SCR after  t4 =",hex(P(txt,"t4") or -1))
t5=P(txt,"t5"); print("RAM getenv t5 =",hex(t5 or -1), (t5 or 0).to_bytes(8,"little"))
print("\n".join(l for l in txt.split("\n") if "lca" in l.lower() or "fatal" in l.lower() or "PALcode" in l)[:2000])
print("GETENV_DONE")
