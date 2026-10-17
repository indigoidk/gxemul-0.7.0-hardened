#!/usr/bin/env python3
# Fable D adjudication rung-3 witness for the three NEW host-exit HIGH rows.
# A guest instruction, on an UNMODIFIED in-tree machine, through the real decode.
# Each case: (A) a LIVENESS control -- a benign word stepped, host survives, pc advances;
# (B) the trap word stepped, host DIES (EOF + nonzero exit + the fatal string).
# Only the one word differs between A and B, same decode path, same machine.
import os, pty, select, signal, sys, time, re

BIN = sys.argv[1]

def run(machine, bits, code, loadaddr, stub, word, label, kill_re):
    pid, fd = pty.fork()
    if pid == 0:
        os.execvp(BIN, [BIN, "-V", "-E", machine, "-M", "64",
                        "0x%x:%s" % (loadaddr, stub)])
        os._exit(127)
    buf = ""
    dead = [False]
    def rd(t=0.5):
        nonlocal buf
        r,_,_ = select.select([fd],[],[],t)
        if fd not in r: return True
        try: d = os.read(fd, 65536)
        except OSError: dead[0]=True; return False
        if not d: dead[0]=True; return False
        buf += d.decode("latin1","replace"); return True
    def wait(mark=0, timeout=40):
        t=time.time()
        while time.time()-t<timeout:
            if not rd(): return False
            if buf[mark:].rstrip().endswith("GXemul>"): return True
        return False
    def send(x, timeout=40):
        m=len(buf)
        try: os.write(fd,(x+"\n").encode("latin1"))
        except OSError: dead[0]=True; return False
        return wait(m, timeout)
    res={"label":label,"prompt":False,"pc_before":None,"pc_after":None,
         "alive_after_step":None,"kill_line":False,"exit":None,"signal":None,"status":label+" ?"}
    if not wait(timeout=40):
        res["status"]="NO-PROMPT"; _teardown(fd,pid,res,buf); return res
    res["prompt"]=True
    send("put w 0x%x, 0x%08x" % (code, word))
    send("pc=0x%x" % code)
    m=len(buf); send("reg")
    mm=re.search(r"pc\s*=\s*0x([0-9a-fA-F]+)", buf[m:])
    res["pc_before"]= mm.group(1) if mm else None
    m=len(buf)
    stepped = send("step 1", timeout=30)
    seg=buf[m:]
    if dead[0] or not stepped:
        res["alive_after_step"]=False
    else:
        res["alive_after_step"]=True
        mm=re.search(r"pc\s*=\s*0x([0-9a-fA-F]+)", seg)
        # read pc via a fresh reg if the step line didn't show it
        if not mm:
            m2=len(buf); send("reg"); mm=re.search(r"pc\s*=\s*0x([0-9a-fA-F]+)", buf[m2:])
        res["pc_after"]= mm.group(1) if mm else None
    if re.search(kill_re, buf):
        res["kill_line"]=True
    _teardown(fd,pid,res,buf)
    return res

def _teardown(fd,pid,res,buf):
    try: os.write(fd,b"quit\n")
    except OSError: pass
    t=time.time()
    while time.time()-t<8:
        r,_,_=select.select([fd],[],[],0.1)
        if fd in r:
            try:
                if not os.read(fd,65536): break
            except OSError: break
    try: os.close(fd)
    except OSError: pass
    st=None; t=time.time()
    while time.time()-t<8:
        try: rp,st=os.waitpid(pid,os.WNOHANG)
        except OSError: st=None; break
        if rp: break
        time.sleep(0.05)
    if st is None:
        try: os.kill(pid,signal.SIGKILL); _,st=os.waitpid(pid,0)
        except OSError: st=None
    if st is not None and os.WIFEXITED(st): res["exit"]=os.WEXITSTATUS(st)
    if st is not None and os.WIFSIGNALED(st): res["signal"]=os.WTERMSIG(st)
    # save the last 40 lines of transcript for the record
    res["tail"]="\n".join(buf.splitlines()[-40:])

def report(r):
    print("=== %s ===" % r["label"])
    print("  prompt=%s pc_before=%s pc_after=%s alive_after_step=%s kill_line=%s exit=%s signal=%s"
          % (r["prompt"],r["pc_before"],r["pc_after"],r["alive_after_step"],
             r["kill_line"],r["exit"],r["signal"]))

# MIPS H2: syscall 0x30378 -> X(promemul) default on testmips -> fatal+exit(1)
MIPS_NOP   = 0x00000000                      # sll zero,zero,0
MIPS_TRAP  = (0x30378 << 6) | 0x0c           # = 0x00C0DE0C, SPECIAL/SYSCALL code 0x30378
MIPS_LOAD  = 0xffffffff80100000
MIPS_CODE  = 0xffffffff80100000
# ARM H1: magic SWI 0xef8c64be -> X(openfirmware) -> of_emul, of_data==NULL -> fatal+exit(1)
ARM_NOP    = 0xe1a00000                      # mov r0,r0
ARM_TRAP   = 0xef8c64be
ARM_LOAD   = 0x00008000
ARM_CODE   = 0x00008000

def write_stub(path, word_le_bytes):
    with open(path,"wb") as f: f.write(word_le_bytes*4)  # 16 bytes, harmless

if __name__=="__main__":
    mstub="/tmp/fableD/mips_stub.bin"; astub="/tmp/fableD/arm_stub.bin"
    write_stub(mstub, b"\x00\x00\x00\x00")
    write_stub(astub, b"\x00\x00\xa0\xe1")  # mov r0,r0 little-endian
    km=r"Unimplemented machine type for PROM magic trap"
    ka=r"of_emul\(\): no of_data struct"
    results=[]
    results.append(run("testmips",64,MIPS_CODE,MIPS_LOAD,mstub,MIPS_NOP ,"H2-MIPS LIVENESS (nop)",   km))
    results.append(run("testmips",64,MIPS_CODE,MIPS_LOAD,mstub,MIPS_TRAP,"H2-MIPS KILL (syscall 0x30378)",km))
    results.append(run("testarm" ,32,ARM_CODE ,ARM_LOAD ,astub,ARM_NOP ,"H1-ARM  LIVENESS (mov r0,r0)",ka))
    results.append(run("testarm" ,32,ARM_CODE ,ARM_LOAD ,astub,ARM_TRAP,"H1-ARM  KILL (swi 0xef8c64be)",ka))
    for r in results: report(r)
    print("---- TAILS ----")
    for r in results:
        print("## %s" % r["label"]); print(r.get("tail","")); print()
    print("WITNESS_DONE")
