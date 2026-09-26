#!/usr/bin/env python3
r"""#549 F2 (measuring seat): is a SECOND fbctrl instance reachable with no device added -- two UNMODIFIED testmips
machines in one process, from a config file -- and what do announce counts do there?

Every access is a real guest sb/sw/lw placed with `put w` into EACH machine's own memory (`focus 0,<m>`), executed by
`step 1`, which runs one instruction on EVERY machine (checked: each step's output must carry each machine's planted
word at CODE+4i exactly once per machine that planted it).  No device is added; the config names only type/memory/load.

MODES
  stagger    two machines (serial 1, 2).  m0: PORT=5, refuse 9 [m0a], lw, refuse 8 [m0b], lw, then nops.
             m1: nops, then the same five.  The staggering makes each announce attributable to its machine.
  lockstepP  two machines, both running the SHIPPED session P program (same words, same registers) in lockstep; the
             shipped P announce rows are evaluated on the process-wide output, exactly as the shipped probe would.
  serial2    ONE machine with serial_nr(2): PORT=5, refuse 9, lw.
usage: twoinst_probe.py <gxemul> <mode>
"""
import os
import pty
import re
import select
import signal
import sys
import time

BIN, MODE = sys.argv[1], sys.argv[2]
STUBADDR = 0xffffffff80100000
CODE = 0xffffffff80100020
FBCTRL = 0xffffffffb2f00000
M64 = 0xffffffffffffffff
ONCE_RE = re.compile(r"\[ fbctrl: port number 0x[0-9a-f]+ is out of range; the selector is unchanged \(once\) \]")
REG = dict(zr=0, v0=2, v1=3, a0=4, a1=5, a2=6, a3=7, t0=8, t1=9, t2=10, t3=11, t4=12, t5=13, t6=14, t7=15,
           s0=16, s1=17, s2=18, s3=19, s4=20, s5=21, s6=22, s7=23, t8=24, t9=25)
OPS = dict(sb=0x28, sh=0x29, sw=0x2b, sd=0x3f, lw=0x23)
NOP = None


def ins(op, rt, off, base="t0"):
    return (OPS[op] << 26) | (REG[base] << 21) | (REG[rt] << 16) | (off & 0xffff)


assert ins("sw", "t1", 0) == 0xad090000 and ins("lw", "t2", 0x10) == 0x8d0a0010 and ins("sd", "t5", 0) == 0xfd0d0000
ANCHOR = 0x3c0f0000


def word(e):
    return 0 if e is NOP else ins(e[0], e[1], e[2])


def run(label, nmach, serial, progs, regs, reads, tags):
    stub = "/tmp/gx_fbctrl549f2t_%d.bin" % os.getpid()
    cfg = "/tmp/gx_fbctrl549f2t_%d.cfg" % os.getpid()
    with open(stub, "wb") as f:
        f.write(b"\x00\x00\x00\x00")
    with open(cfg, "w") as f:
        for i in range(nmach):
            f.write('machine(\n\tname("m%d")\n\ttype("testmips")\n\tmemory(64)\n' % i)
            if serial is not None:
                f.write("\tserial_nr(%d)\n" % serial)
            f.write('\tload("0x%x:%s")\n)\n' % (STUBADDR, stub))
    pid, fd = pty.fork()
    if pid == 0:
        os.execvp(BIN, [BIN, "-V", "@" + cfg])
        os._exit(127)
    buf = ""
    dead = [False]

    def rd(t=0.4):
        nonlocal buf
        r, _, _ = select.select([fd], [], [], t)
        if fd not in r:
            return True
        try:
            d = os.read(fd, 65536)
        except OSError:
            dead[0] = True
            return False
        if not d:
            dead[0] = True
            return False
        buf += d.decode("latin1", "replace")
        return True

    def wait(mark=0, echo=None, timeout=60):
        t = time.time()
        while time.time() - t < timeout:
            if not rd():
                return False
            resp = buf[mark:]
            if echo is not None and echo not in resp:
                continue
            if len(buf) > mark and resp.rstrip().endswith("GXemul>"):
                return True
        return False

    def send(x, timeout=60):
        b = (x + "\n").encode("latin1")
        _mark = len(buf)
        n = 0
        try:
            while n < len(b):
                n += os.write(fd, b[n:])
        except OSError:
            dead[0] = True
            return False
        return wait(mark=_mark, echo=x if x else None, timeout=timeout)

    n = len(progs[0])
    words = [[word(e) for e in p] + [ANCHOR] for p in progs]
    status, badstep, once_after, vals, serials, steps = "?", [], {}, {}, {}, 0
    if not wait(timeout=120):
        status = "NO-PROMPT"
    else:
        for m in range(nmach):
            send("focus 0,%d" % m)
            for i, w in enumerate(words[m]):
                send("put w 0x%x, 0x%08x" % (CODE + 4 * i, w))
            for name, val in regs[m]:
                send("%s=0x%x" % (name, val & M64))
            send("pc=0x%x" % CODE)
            mk = len(buf)
            send("print serial_nr")
            mm = re.search(r"(?m)^0x([0-9a-fA-F]+)\s*$", buf[mk:])
            serials[m] = int(mm.group(1), 16) if mm else None
        send("focus 0,0")
        status = "SURVIVED"
        for i in range(n):
            mark = len(buf)
            if not send("step 1", timeout=30) or dead[0]:
                status = "HOST-DIED"
                break
            steps += 1
            seg = buf[mark:]
            want = {}
            for m in range(nmach):
                want[words[m][i]] = want.get(words[m][i], 0) + 1
            for w, k in want.items():
                got = len(re.findall(r"%016x:?\s+%08x\b" % (CODE + 4 * i, w), seg))
                if got != k:
                    badstep.append("step %d word 0x%08x: %d lines, want %d" % (i, w, got, k))
            if i in tags:
                once_after[tags[i]] = len(ONCE_RE.findall(buf))
        if status == "SURVIVED":
            for m in range(nmach):
                send("focus 0,%d" % m)
                for name in reads[m]:
                    mark = len(buf)
                    send("print %s" % name, timeout=30)
                    mm = re.search(r"(?m)^0x([0-9a-fA-F]+)\s*$", buf[mark:])
                    vals[(m, name)] = int(mm.group(1), 16) if mm else None
    try:
        os.write(fd, b"quit\n")
    except OSError:
        pass
    t1 = time.time()
    while time.time() - t1 < 20.0:
        if not rd(0.1):
            break
    try:
        os.close(fd)
    except OSError:
        pass
    rpid, st = 0, None
    t1 = time.time()
    while rpid == 0 and time.time() - t1 < 10.0:
        try:
            rpid, st = os.waitpid(pid, os.WNOHANG)
        except OSError:
            break
        if rpid == 0:
            time.sleep(0.05)
    if rpid == 0:
        try:
            os.kill(pid, signal.SIGKILL)
            _, st = os.waitpid(pid, 0)
        except OSError:
            st = None
    for p in (stub, cfg):
        try:
            os.unlink(p)
        except OSError:
            pass
    code = os.WEXITSTATUS(st) if st is not None and os.WIFEXITED(st) else None
    print("  run %-9s machines=%d serials=%s %s steps=%d/%d exit=%s once=%d lockstep_mismatches=%d" % (
        label, nmach, [serials.get(m) for m in range(nmach)], status, steps, n, code,
        len(ONCE_RE.findall(buf)), len(badstep)))
    for b in badstep[:6]:
        print("      STEP-LINE MISMATCH: %s" % b)
    return {"status": status, "vals": vals, "once_after": once_after, "badstep": badstep, "buf": buf,
            "serials": serials, "steps": steps, "n": n}


RES = []


def row(name, got, want):
    ok = got == want
    RES.append(ok)
    print("  %-4s %-60s got=%-14s want=%s" % ("ok" if ok else "FAIL", name, got, want))


def hx(v):
    return "-" if v is None else "0x%x" % v


FIVE = [("sw", "a0", 0), ("sw", "t1", 0), ("lw", "s0", 0), ("sw", "t2", 0), ("lw", "s1", 0)]
REGS5 = [("t0", FBCTRL), ("a0", 5), ("t1", 9), ("t2", 8), ("s0", 0xdead), ("s1", 0xdead)]

if MODE == "stagger":
    progs = [FIVE + [NOP] * 5, [NOP] * 5 + FIVE]
    R = run("stagger", 2, None, progs, [REGS5, REGS5], [["s0", "s1"], ["s0", "s1"]],
            {1: "m0a", 3: "m0b", 6: "m1a", 8: "m1b"})
    row("construct: two machines, serials 1 and 2", str([R["serials"].get(0), R["serials"].get(1)]), "[1, 2]")
    row("every step ran one instruction on each machine", len(R["badstep"]), 0)
    row("m0 first refusal announces: count after m0's refusal", R["once_after"].get("m0a"), 1)
    row("m0 second refusal silent: count after m0's repeat", R["once_after"].get("m0b"), 1)
    row("m1 FIRST refusal announces (own latch): count", R["once_after"].get("m1a"), 2)
    row("m1 second refusal silent: count", R["once_after"].get("m1b"), 2)
    row("m0 PORT keeps 5 after 9", hx(R["vals"].get((0, "s0"))), "0x5")
    row("m0 PORT keeps 5 after 8", hx(R["vals"].get((0, "s1"))), "0x5")
    row("m1 PORT keeps 5 after 9", hx(R["vals"].get((1, "s0"))), "0x5")
    row("m1 PORT keeps 5 after 8", hx(R["vals"].get((1, "s1"))), "0x5")
elif MODE == "lockstepP":
    #  the SHIPPED session P, verbatim (regress/fbctrl_port_probe.py md5 4a31bf36), on both machines at once
    REFUSE = [("sw", "t1", 9), ("sw", "t2", 8), ("sw", "t3", 16), ("sd", "t4", 0x200000000), ("sd", "t5", 0x100000003),
              ("sd", "t6", M64), ("sw", "t7", 0xffffffff), ("sb", "t8", 0xff), ("sh", "t9", 0x100)]
    READ_P = ["s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7", "v0"]
    P = [("sw", "a0", 0), ("sw", "a1", 16)]
    RG = [("t0", FBCTRL), ("a0", 5), ("a1", 0x2a), ("a2", 7)]
    tags = {}
    for k, (w, r, v) in enumerate(REFUSE):
        RG.append((r, v))
        if k:
            P.append(("sw", "a0", 0))
        tags[len(P)] = "r%d" % k
        P.append((w, r, 0))
        P.append(("lw", READ_P[k], 0))
    P += [("sw", "a2", 0)]
    tags[len(P)] = "r9"
    P += [("sw", "t1", 0), ("lw", "v1", 0)]
    R = run("lockstepP", 2, None, [P, P], [RG, RG], [READ_P + ["v1"]] * 2, tags)
    row("every step ran one instruction on each machine", len(R["badstep"]), 0)
    print("  -- the SHIPPED P rows, evaluated as the shipped probe evaluates them (process-wide count):")
    row("SHIPPED 'announce: exactly 1 right after the FIRST refusal'", R["once_after"].get("r0"), 1)
    row("SHIPPED 'announce: still exactly 1 after ten refusals'", R["once_after"].get("r9"), 1)
    row("per instance: 2 after the first refusal (one per device)", R["once_after"].get("r0"), 2)
    row("per instance: still 2 after ten refusals", R["once_after"].get("r9"), 2)
    for m in range(2):
        row("m%d every refusal kept 5 (9 rows)" % m,
            str([hx(R["vals"].get((m, r))) for r in READ_P]), str(["0x5"] * 9))
        row("m%d refuse 9 after PORT=7 kept 7" % m, hx(R["vals"].get((m, "v1"))), "0x7")
elif MODE == "serial2":
    R = run("serial2", 1, 2, [FIVE], [REGS5], [["s0", "s1"]], {1: "a", 3: "b"})
    row("construct: one machine, serial 2", str([R["serials"].get(0)]), "[2]")
    row("every step ran", len(R["badstep"]), 0)
    row("first refusal announces on serial 2: count", R["once_after"].get("a"), 1)
    row("repeat silent: count", R["once_after"].get("b"), 1)
    row("PORT keeps 5 after 9", hx(R["vals"].get((0, "s0"))), "0x5")
else:
    sys.exit("mode?")
print("TWOINST_%s_RESULT=%d/%d" % (MODE.upper(), sum(RES), len(RES)))
print("TWOINST_DONE")
