#  NON-EQUIVALENCE CONTROLS for the three clean sweeps, and a preview of the rows that
#  would kill them.  Same session()/program() machinery as the shipped probe.
import os, pty, re, select, sys, time
BIN, LABEL = sys.argv[1], sys.argv[2]
DUMMY = "/tmp/pcc2_dummy.bin"; open(DUMMY, "wb").write(b"\x00\x00\x00\x00")
CODE, SCRATCH, PCC2 = 0x00010000, 0x00020000, 0xfff42000
GENCTL, VECBASE, IPL = 0x02, 0x03, 0x3e
DECL = "-- declined.  (once) ]"
def enc(o,rd,rs1,imm): return (o<<26)|(rd<<21)|(rs1<<16)|(imm&0xffff)
def LD_H(rd,off): return enc(0x06,rd,2,off)
def LD_BU(rd,off): return enc(0x03,rd,2,off)
def ST_B(rs,off): return enc(0x0b,rs,2,off)
def ST_H(rs,off): return enc(0x0a,rs,2,off)
I_BR_SELF = 0xc0000000
def program(insns, at=CODE):
    w = list(insns)+[I_BR_SELF,0]
    return ["put w 0x%x, 0x%08x"%(at+4*i,x) for i,x in enumerate(w)]+["pc=0x%x"%at,"step %d"%len(insns)]
def setup(r5="0x5a5a5a5a", r6="0x0"):
    return ["r2=0x%x"%PCC2,"r3=0x%x"%SCRATCH,"r5=%s"%r5,"r6=%s"%r6,"r4=0xdeadbeef"]
def session(cmds, settle=1.5, spin=1.2):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN,[BIN,"-V","-x","-E","mvme88k","-e","mvme187","-M","64","0x10000:"+DUMMY]); os._exit(127)
    buf=""
    def rd(t):
        nonlocal buf
        end=time.time()+t
        while time.time()<end:
            r,_,_=select.select([fd],[],[],0.1)
            if not r: continue
            try:
                d=os.read(fd,65536)
                if not d: return False
                buf+=d.decode("latin-1","replace")
            except OSError: return False
        return True
    alive=rd(settle)
    for i,c in enumerate(cmds):
        try: os.write(fd,(c+"\n").encode("latin-1"))
        except OSError: alive=False; break
        if not rd(spin if i==len(cmds)-1 else 0.25): alive=False; break
    try: os.write(fd,b"quit\n"); rd(0.4)
    except OSError: pass
    try: os.close(fd)
    except OSError: pass
    try: os.waitpid(pid,0)
    except OSError: pass
    return buf.replace("\r","")
def printed(t,reg):
    m=re.search(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)"%reg,t)
    return "0x%x"%int(m.group(1),16) if m else "absent"

#  (1) the row that would kill MA: wide write AT VECBASE, then read VECBASE back
t = session(setup(r5="0x50") + program([ST_B(5, VECBASE)])
            + ["put h 0x%x, 0xaabb" % (PCC2 + VECBASE)]
            + program([LD_BU(4, VECBASE)], at=CODE + 0x100) + ["print r4"])
print("  %-6s PROPOSED rb vecbase wr = %-8s (BASE wants 0x50; MA lands 0xb0)" % (LABEL, printed(t,"r4")))

#  (2) the row that would kill MB: IPL's read-only 'ignored' print in the wide-write session
t = session(setup(r6="0x1234") + program([ST_H(6, IPL)]))
print("  %-6s PROPOSED hwr ipl noro = %-8s (BASE wants 0; MB prints 1)"
      % (LABEL, t.count("write to read-only PCCTWO_IPL")))

#  (3) the row that would kill MC: a wide READ must be accepted SILENTLY
t = session(setup() + program([LD_H(4, GENCTL)]))
print("  %-6s PROPOSED hrd genctl nod = %-6s (BASE wants 0; MC prints 1)" % (LABEL, t.count(DECL)))
print("NONEQ_%s_DONE" % LABEL)
