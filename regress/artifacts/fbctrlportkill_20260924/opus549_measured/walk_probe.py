#!/usr/bin/env python3
"""Q1(b): walk widths 1/2/4/8 across every offset in the 0x20 window on big-endian -E testmips.
For each (offset,width): FIRST refuse the port (sw 9 to +0x00 -- with the fix this is declined and
current_port stays 0), THEN do a WRITE of the width at the offset, THEN a READ of the width at +0x10.
Report HOST-DIED (with which diagnostic) vs SURVIVED.  One fresh emulator per cell.
usage: walk_probe.py <binary>"""
import os, pty, re, select, signal, sys, time
BIN = sys.argv[1]
STUBADDR = 0xffffffff80100000
CODE = 0xffffffff80100020
FB = 0xffffffffb2f00000
R = dict(zr=0, t0=8, t1=9, t2=10, t3=11)
def it(op, rs, rt, imm): return (op<<26)|(rs<<21)|(rt<<16)|(imm & 0xffff)
def sw(rt, off, base): return it(0x2b, R[base], R[rt], off)
def sh(rt, off, base): return it(0x29, R[base], R[rt], off)
def sb(rt, off, base): return it(0x28, R[base], R[rt], off)
def sd(rt, off, base): return it(0x3f, R[base], R[rt], off)
def lw(rt, off, base): return it(0x23, R[base], R[rt], off)
def lh(rt, off, base): return it(0x21, R[base], R[rt], off)
def lb(rt, off, base): return it(0x20, R[base], R[rt], off)
def ld(rt, off, base): return it(0x37, R[base], R[rt], off)
STW = {1: sb, 2: sh, 4: sw, 8: sd}
LDW = {1: lb, 2: lh, 4: lw, 8: ld}
def run(prog, regs, stub):
    pid, fd = pty.fork()
    if pid == 0:
        os.execvp(BIN, [BIN, "-V", "-E", "testmips", "-M", "64", "0x%x:%s" % (STUBADDR, stub)]); os._exit(127)
    buf = ""; dead=[False]
    def rd(t=0.4):
        nonlocal buf
        r,_,_ = select.select([fd],[],[],t)
        if fd not in r: return True
        try: d = os.read(fd, 65536)
        except OSError: dead[0]=True; return False
        if not d: dead[0]=True; return False
        buf += d.decode("latin1","replace"); return True
    def wait(mark=0, echo=None, timeout=30):
        t=time.time()
        while time.time()-t < timeout:
            if not rd(): return False
            resp=buf[mark:]
            if echo is not None and echo not in resp: continue
            if len(buf)>mark and resp.rstrip().endswith("GXemul>"): return True
        return False
    def send(x, timeout=30):
        b=(x+"\n").encode("latin1"); _m=len(buf); n=0
        try:
            while n<len(b): n += os.write(fd, b[n:])
        except OSError: dead[0]=True; return False
        return wait(mark=_m, echo=x if x else None, timeout=timeout)
    status="?"; steps=0
    if not wait(timeout=120): status="NO-PROMPT"
    else:
        for i,w in enumerate(prog): send("put w 0x%x, 0x%08x" % (CODE+4*i, w))
        for name,val in regs: send("%s=0x%x" % (name, val))
        send("pc=0x%x" % CODE)
        status="SURVIVED"
        for i in range(len(prog)-1):
            if not send("step 1", timeout=30) or dead[0]:
                status="HOST-DIED"; break
            steps+=1
    try: os.write(fd, b"quit\n")
    except OSError: pass
    t1=time.time()
    while time.time()-t1 < 15.0:
        if not rd(0.1): break
    try: os.close(fd)
    except OSError: pass
    rpid,st=0,None; t1=time.time()
    while rpid==0 and time.time()-t1<10.0:
        try: rpid,st=os.waitpid(pid, os.WNOHANG)
        except OSError: break
        if rpid==0: time.sleep(0.05)
    if rpid==0:
        try: os.kill(pid, signal.SIGKILL); _,st=os.waitpid(pid,0)
        except OSError: st=None
    code = os.WEXITSTATUS(st) if st is not None and os.WIFEXITED(st) else None
    diag = ("DATA-OOR" if "[ fbctrl port number is out of range! ]" in buf else
            "UNIMPL-ADDR" if "unimplemented relative addr" in buf else
            "CMD-UNIMPL" if "fbctrl_command: Unimplemented command" in buf else
            "PORT-WARN-ONLY" if "WARNING: fbctrl port number" in buf else "-")
    return status, steps, code, diag
def main():
    stub = "/tmp/gx_walk549_%d.bin" % os.getpid()
    open(stub,"wb").write(b"\x00\x00\x00\x00")
    try:
        print("BIN=%s" % BIN)
        print("offset width  writeport9-then-op@off-then-read@0x10")
        for off in range(0, 0x20):
            for wdt in (1,2,4,8):
                # prog: sw 9 -> PORT(+0x00) [refused w/fix]; store width at off; load width at +0x10
                prog = [sw("t1", 0, "t0"), STW[wdt]("t2", off, "t0"), LDW[wdt]("t3", 0x10, "t0"), 0]
                regs = [("t0", FB), ("t1", 9), ("t2", 0x2a)]
                status, steps, code, diag = run(prog, regs, stub)
                tag = "SURVIVED" if status=="SURVIVED" else "DIED@step%d/%s" % (steps, diag)
                if status != "SURVIVED" or diag not in ("-","PORT-WARN-ONLY"):
                    print("  +0x%02x  %d    %s" % (off, wdt, tag))
        print("WALK_DONE")
    finally:
        try: os.unlink(stub)
        except OSError: pass
main()
