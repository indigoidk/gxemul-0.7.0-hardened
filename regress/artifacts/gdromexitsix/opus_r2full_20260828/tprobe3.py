import os, pty, re, select, sys, time
BIN, KERNEL = sys.argv[1], sys.argv[2]
CODE=0x8c001000
CNTLO=0xa05f7090; CNTHI=0xa05f7094; COND=0xa05f709c; DATAP=0xa05f7080
EVT_HI=0xa05f6904
MOVW=0x2781; LDW=0x6211; LDL=0x6212; BRA=0xaffe; NOP=0x0009

def session(cmds, settle=8.0, spin=2.0):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN,"-V","-x","-E","dreamcast","-M","64",KERNEL]); os._exit(127)
    buf=""
    def rd(t):
        nonlocal buf
        end=time.time()+t
        while time.time()<end:
            r,_,_=select.select([fd],[],[],0.25)
            if not r: continue
            try: d=os.read(fd,65536)
            except OSError: return False
            if not d: return False
            buf+=d.decode("latin-1","replace")
        return True
    alive=rd(settle)
    for i,c in enumerate(cmds):
        try: os.write(fd,(c+"\n").encode("latin-1"))
        except OSError: alive=False; break
        if not rd(spin if i==len(cmds)-1 else 0.35): alive=False; break
    try: os.write(fd,b"quit\n"); rd(0.6)
    except OSError: pass
    try: os.close(fd)
    except OSError: pass
    st=None
    try: _,st=os.waitpid(pid,0)
    except OSError: pass
    return buf,alive,st

def run(steps,at=CODE):
    p=["put h 0x%x, 0x%04x"%(at+2*i,op) for i,op in enumerate(steps)]
    p+=["put h 0x%x, 0x%04x"%(at+2*len(steps),BRA),"put h 0x%x, 0x%04x"%(at+2*len(steps)+2,NOP)]
    return p+["pc=0x%x"%at,"step %d"%len(steps)]

def death(st):
    if st is None: return "nowait"
    if os.WIFSIGNALED(st): return "sig%d"%os.WTERMSIG(st)
    if os.WIFEXITED(st): return "exit%d"%os.WEXITSTATUS(st)
    return "st%d"%st

def stage_toc(at, cnt=408):
    lo = cnt & 0xff; hi = (cnt >> 8) & 0xff
    return (["r7=0x%x"%CNTLO,"r8=0x%02x"%lo]+run([MOVW],at)
          + ["r7=0x%x"%CNTHI,"r8=0x%02x"%hi]+run([MOVW],at+0x20)
          + ["r7=0x%x"%COND,"r8=0xa0"]+run([MOVW],at+0x40)
          + ["r7=0x%x"%DATAP,"r8=0x0014"]+run([MOVW]*6,at+0x60)), at+0xa0

def cmd12(words, at):
    out = ["r7=0x%x"%COND,"r8=0xa0"]+run([MOVW],at); at+=0x20
    out += ["r7=0x%x"%DATAP]
    for w in words:
        out += ["r8=0x%04x"%w]+run([MOVW],at); at+=0x20
    return out, at

UNK   = re.compile(r"unimplemented command")
FMTB  = re.compile(r"unimplemented data format")          # BARE -- matches 0x24 warn AND decline
FMTD  = re.compile(r"data format 0x[0-9a-f]+ -- declined") # the ROUND-2 decline only
FMT24 = re.compile(r"Continuing anway")                    # the upstream 0x24 warn only
TOCD  = re.compile(r"Read TOC with")                       # #489 decline
HUH   = re.compile(r"Huh\? GDROM data_len")
REJ   = re.compile(r"rejecting sector_count")

def vals(t):
    return re.findall(r"print\s+r2\s*\r?\n\s*(0x[0-9a-f]+)", t)

def chans(at):
    return (["r1=0x%x"%COND,"r2=0xdead"]+run([LDW],at)+["print r2"]
          + ["r1=0x%x"%CNTLO,"r2=0xdead"]+run([LDW],at+0x20)+["print r2"]
          + ["r1=0x%x"%EVT_HI,"r2=0xdead"]+run([LDL],at+0x40)+["print r2"])

def emit(tag,t,alive,st):
    v=vals(t)
    g=lambda i:(v[i] if len(v)>i else "absent")
    print("%-12s alive=%-5s death=%-6s COND=%-7s CNT=%-7s EVT32=%-6s unk=%d fmtB=%d fmtD=%d f24=%d toc=%d huh=%d rej=%d"
          %(tag,alive,death(st),g(0),g(1),g(2),len(UNK.findall(t)),len(FMTB.findall(t)),
            len(FMTD.findall(t)),len(FMT24.findall(t)),len(TOCD.findall(t)),
            len(HUH.findall(t)),len(REJ.findall(t))))
    sys.stdout.flush()

W = lambda c0,c1,c10=0: [c1*256+c0,0,0,0,0,c10]

ALL = ["S1 good","S1 unkcmd","S1 badfmt","S1 mount","S2 unk x2","S2 fmt x2",
       "S3 both","S4 acceptA","S5 toc+fmt","S6 toc+unk","S7 fmt24","S8 acceptTOC"]
raw = sys.argv[3] if len(sys.argv) > 3 else ""
SEL = [x.strip() for x in raw.split(",") if x.strip()] if raw.strip() else list(ALL)
unknown = [x for x in SEL if x not in ALL]
if unknown:
    print("SELECTOR NAMES NO SUCH SESSION: %s" % unknown); sys.exit(2)
if not SEL:
    print("SELECTOR MATCHED ZERO SESSIONS"); sys.exit(2)
print("SELECTED %d of %d: %s" % (len(SEL), len(ALL), ",".join(SEL)))
def want(tag): return tag in SEL

#  S1: legal TOC then ONE second command; read the three tail channels.
for tag,w in (("S1 good",W(0x30,0x20)),("S1 unkcmd",W(0x31,0x20)),
              ("S1 badfmt",W(0x30,0x21)),("S1 mount",W(0x70,0x00))):
    a,at=stage_toc(CODE); b,at=cmd12(w,at)
    if not want(tag): continue
    t,al,st=session(a+b+chans(at)); emit(tag,t,al,st)

#  S2: legal TOC then the SAME bad command TWICE -- the per-site latch test.
for tag,w in (("S2 unk x2",W(0x31,0x20)),("S2 fmt x2",W(0x30,0x21))):
    a,at=stage_toc(CODE); b,at=cmd12(w,at); c,at=cmd12(w,at)
    if not want(tag): continue
    t,al,st=session(a+b+c+chans(at)); emit(tag,t,al,st)

#  S3: legal TOC then BOTH bad commands -- the A-vs-B shared-latch test.
a,at=stage_toc(CODE); b,at=cmd12(W(0x31,0x20),at); c,at=cmd12(W(0x30,0x21),at)
if want("S3 both"):
    t,al,st=session(a+b+c+chans(at)); emit("S3 both",t,al,st)

#  S4: ACCEPT SIDE OF SITE A.
a,at=stage_toc(CODE); b,at=cmd12(W(0x30,0x20,1),at)
if want("S4 acceptA"):
    t,al,st=session(a+b+chans(at)); emit("S4 acceptA",t,al,st)

#  S5: SHORT TOC (cnt=407 -> #489 declines, sets GDROM_W_TOCLEN) THEN a bad
#  format.  If Site A's latch bit COLLIDES with GDROM_W_TOCLEN the format
#  diagnostic is suppressed and fmtD reads 0.  NO PLANNED ROW BUILDS THIS STATE.
a,at=stage_toc(CODE,407); b,at=cmd12(W(0x30,0x21),at)
if want("S5 toc+fmt"):
    t,al,st=session(a+b+chans(at)); emit("S5 toc+fmt",t,al,st)

#  S6: SHORT TOC then an unknown command -- the same test for Site B's bit.
a,at=stage_toc(CODE,407); b,at=cmd12(W(0x31,0x20),at)
if want("S6 toc+unk"):
    t,al,st=session(a+b+chans(at)); emit("S6 toc+unk",t,al,st)

#  S7: cmd[1] == 0x24 -- the upstream warn-and-continue arm, which MUST stay
#  byte-identical (P5).  Distinguishes the bare regex from the anchored one.
a,at=stage_toc(CODE); b,at=cmd12(W(0x30,0x24),at)
if want("S7 fmt24"):
    t,al,st=session(a+b+chans(at)); emit("S7 fmt24",t,al,st)

#  S8: legal TOC ALONE -- the 0x14 accept side; COND must carry DATA_AVAIL.
a,at=stage_toc(CODE)
if want("S8 acceptTOC"):
    t,al,st=session(a+chans(at)); emit("S8 acceptTOC",t,al,st)

print("TPROBE3_DONE")
