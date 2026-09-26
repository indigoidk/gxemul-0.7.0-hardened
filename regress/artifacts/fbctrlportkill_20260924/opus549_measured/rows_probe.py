#!/usr/bin/env python3
r"""The PROPOSED detector rows for #549, as MIPS guest sequences on -E testmips, one fresh
emulator per arm.  Emits one line per row: ok/FAIL.  Also FBCTRLR_ANNOUNCE=<n> (count of the
new (once) marker after three refused writes) and FBCTRLR_CONTROLONCE=<n> (in a controls-only arm).
usage: rows_probe.py <binary>"""
import os, pty, re, select, signal, sys, time
BIN = sys.argv[1]
STUBADDR = 0xffffffff80100000
CODE = 0xffffffff80100020
FB = 0xffffffffb2f00000
R = dict(zr=0, t0=8, t1=9, t2=10, t3=11, t4=12, t5=13, t6=14, t7=15, s0=16, s1=17, s2=18, s3=19)
def it(op, rs, rt, imm): return (op << 26) | (rs << 21) | (rt << 16) | (imm & 0xffff)
def sw(rt, off, base): return it(0x2b, R[base], R[rt], off)
def sd(rt, off, base): return it(0x3f, R[base], R[rt], off)
def lw(rt, off, base): return it(0x23, R[base], R[rt], off)

def session(prog, regs, reads):
    stub = "/tmp/gx_rows549_%d.bin" % os.getpid()
    open(stub, "wb").write(b"\x00\x00\x00\x00")
    pid, fd = pty.fork()
    if pid == 0:
        os.execvp(BIN, [BIN, "-V", "-E", "testmips", "-M", "64", "0x%x:%s" % (STUBADDR, stub)]); os._exit(127)
    buf = ""; dead = [False]
    def rd(t=0.4):
        nonlocal buf
        r, _, _ = select.select([fd], [], [], t)
        if fd not in r: return True
        try: d = os.read(fd, 65536)
        except OSError: dead[0] = True; return False
        if not d: dead[0] = True; return False
        buf += d.decode("latin1", "replace"); return True
    def wait(m=0, e=None, to=30):
        t = time.time()
        while time.time() - t < to:
            if not rd(): return False
            s = buf[m:]
            if e and e not in s: continue
            if len(buf) > m and s.rstrip().endswith("GXemul>"): return True
        return False
    def send(x, to=30):
        b = (x + "\n").encode("latin1"); m = len(buf); n = 0
        try:
            while n < len(b): n += os.write(fd, b[n:])
        except OSError: dead[0] = True; return False
        return wait(m, x or None, to)
    status = "SURVIVED"; steps = 0; vals = {}
    if not wait(to=120): status = "NO-PROMPT"
    else:
        for i, w in enumerate(prog): send("put w 0x%x, 0x%08x" % (CODE + 4 * i, w))
        for nm, v in regs: send("%s=0x%x" % (nm, v))
        send("pc=0x%x" % CODE)
        for i in range(len(prog) - 1):
            if not send("step 1", to=30) or dead[0]:
                status = "HOST-DIED"; break
            steps += 1
        if status == "SURVIVED":
            for nm in reads:
                v = None
                for _ in range(2):
                    m = len(buf)
                    if not send("print %s" % nm, to=30) or dead[0]: break
                    mm = re.search(r"(?m)^0x([0-9a-fA-F]+)\s*$", buf[m:])
                    if mm: v = int(mm.group(1), 16); break
                vals[nm] = v
    try: os.write(fd, b"quit\n")
    except OSError: pass
    t1 = time.time()
    while time.time() - t1 < 15.0:
        if not rd(0.1): break
    try: os.close(fd)
    except OSError: pass
    rp, st = 0, None; t1 = time.time()
    while rp == 0 and time.time() - t1 < 10.0:
        try: rp, st = os.waitpid(pid, os.WNOHANG)
        except OSError: break
        if rp == 0: time.sleep(0.05)
    if rp == 0:
        try: os.kill(pid, signal.SIGKILL); os.waitpid(pid, 0)
        except OSError: pass
    code = os.WEXITSTATUS(st) if st is not None and os.WIFEXITED(st) else None
    try: os.unlink(stub)
    except OSError: pass
    once = buf.count("(once)")
    warnold = buf.count("[ WARNING: fbctrl port number is out of range! ]")
    return dict(status=status, steps=steps, exit=code, vals=vals, once=once, warnold=warnold, buf=buf)


def main():
    print("BIN=%s" % BIN)
    R_ = []
    def row(n, ok, d): print("  %-4s %-46s %s" % ("ok" if ok else "FAIL", n, d)); R_.append(ok)

    # refusal-anchored: PORT=5, DATA=0x2a, PORT=9 (refused) -> survive; DATA reads 0x2a; PORT reads 5
    p = [sw("t1", 0, "t0"), sw("t2", 0x10, "t0"), sw("t3", 0, "t0"), lw("t4", 0x10, "t0"), lw("t5", 0, "t0"), 0]
    rg = [("t0", FB), ("t1", 5), ("t2", 0x2a), ("t3", 9), ("t4", 0xdead), ("t5", 0xdead)]
    a = session(p, rg, ["t4", "t5"])
    row("refusal: survives PORT=9 after PORT=5", a["status"] == "SURVIVED", "%s steps=%d" % (a["status"], a["steps"]))
    row("refusal: DATA still reads 0x2a (port 5, not 0)", a["vals"].get("t4") == 0x2a, "t4=%s" % a["vals"].get("t4"))
    row("refusal: PORT still reads 5", a["vals"].get("t5") == 5, "t5=%s" % a["vals"].get("t5"))

    # boundary: PORT=5, DATA=0x2a, PORT=8 (refused) -> PORT reads 5
    p = [sw("t1", 0, "t0"), sw("t2", 0x10, "t0"), sw("t3", 0, "t0"), lw("t5", 0, "t0"), 0]
    a = session(p, [("t0", FB), ("t1", 5), ("t2", 0x2a), ("t3", 8), ("t5", 0xdead)], ["t5"])
    row("boundary: PORT=8 refused, PORT reads 5", a["status"] == "SURVIVED" and a["vals"].get("t5") == 5,
        "%s t5=%s" % (a["status"], a["vals"].get("t5")))
    # PORT=7 accepted, DATA=0x77 round-trips (far slot); PORT reads 7
    p = [sw("t1", 0, "t0"), sw("t2", 0x10, "t0"), lw("t4", 0x10, "t0"), lw("t5", 0, "t0"), 0]
    a = session(p, [("t0", FB), ("t1", 7), ("t2", 0x77), ("t4", 0xdead), ("t5", 0xdead)], ["t4", "t5"])
    row("boundary: PORT=7 accepted, reads 7", a["status"] == "SURVIVED" and a["vals"].get("t5") == 7,
        "%s t5=%s" % (a["status"], a["vals"].get("t5")))
    row("boundary: DATA=0x77 round-trips at port 7", a["vals"].get("t4") == 0x77, "t4=%s" % a["vals"].get("t4"))

    # wide: PORT=5, DATA=0x2a, sd 0x100000003 to PORT (refused) -> PORT reads 5
    p = [sw("t1", 0, "t0"), sw("t2", 0x10, "t0"), sd("t3", 0, "t0"), lw("t5", 0, "t0"), 0]
    a = session(p, [("t0", FB), ("t1", 5), ("t2", 0x2a), ("t3", 0x100000003), ("t5", 0xdead)], ["t5"])
    row("wide: sd 0x100000003 refused, PORT reads 5", a["status"] == "SURVIVED" and a["vals"].get("t5") == 5,
        "%s t5=%s" % (a["status"], a["vals"].get("t5")))

    # negative: PORT=5, DATA=0x2a, sw -1 to PORT (refused) -> PORT reads 5
    p = [sw("t1", 0, "t0"), sw("t2", 0x10, "t0"), sw("t3", 0, "t0"), lw("t5", 0, "t0"), 0]
    a = session(p, [("t0", FB), ("t1", 5), ("t2", 0x2a), ("t3", 0xffffffff), ("t5", 0xdead)], ["t5"])
    row("negative: sw -1 refused, PORT reads 5", a["status"] == "SURVIVED" and a["vals"].get("t5") == 5,
        "%s t5=%s" % (a["status"], a["vals"].get("t5")))

    # announce: three refused writes on one device -> exactly ONE (once) marker
    p = [sw("t1", 0, "t0"), sw("t1", 0, "t0"), sw("t1", 0, "t0"), 0]
    a = session(p, [("t0", FB), ("t1", 9)], [])
    row("announce: exactly ONE (once) after three refused", a["once"] == 1, "once=%d survived=%s" % (a["once"], a["status"] == "SURVIVED"))
    print("FBCTRLR_ANNOUNCE=%d" % a["once"])
    print("FBCTRLR_OLDWARN=%d" % a["warnold"])
    # controls-only arm: legal traffic, ZERO (once)
    p = [sw("t1", 0, "t0"), sw("t2", 0x10, "t0"), lw("t4", 0x10, "t0"), 0]
    a = session(p, [("t0", FB), ("t1", 5), ("t2", 0x2a), ("t4", 0xdead)], ["t4"])
    row("announce: ZERO (once) in controls-only arm", a["once"] == 0, "once=%d" % a["once"])
    print("FBCTRLR_ALLGREEN=%s" % ("yes" if all(R_) else "no"))
    print("FBCTRLR_DONE")

main()
