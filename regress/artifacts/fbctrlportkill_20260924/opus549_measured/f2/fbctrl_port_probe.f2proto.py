#!/usr/bin/env python3
r"""#549 F2 PROTOTYPE -- the measuring seat's COPY of regress/fbctrl_port_probe.py (md5 4a31bf36), NOT the shipped probe.

It adds the D-rows in the CORRECTED forms the Astra / grok F2 rulings give, and -- as rows marked "diag", which are
left out of FBCTRLP_RESULT -- the forms the F2 brief first proposed, so that one run per binary shows which form goes
red on which device edit.  Helper code (session, row, encodings) is the shipped probe's, plus `ld` and a buffer
position recorded per tag (so a count can be re-derived with a second pattern after the run).

SESSIONS (each on a fresh emulator; C, A, K as shipped except where marked)
  C  + D11: Y1 is PREFILLED 123 before GET_RESOLUTION, then read back (want 0).
  A  + Astra F2 #3: no (once) line anywhere in A.
  P  D9: the first refusal is 8 (was 9); two more refusals (16 by sb, 16 by sh) go BEFORE the tail -> twelve refusals;
     the tail's count tag is its own ("rtail", not "r9").  D10: the first announce must name 0x8, bounded by " is".
     diag: the count sampled at the 10th refusal; the three counts re-derived with the NARROW 0x8/0x9 pattern.
  R  D4, in its own session (a DATA access in P would turn every accepted-8 mutant into a session death that blanks
     P's other rows): PORT=5, refuse 9, DATA write to port 5, PORT=0 + DATA=0 (NOP), PORT=5, refuse 9 -> count still 1.
  F  D3: a guest `lw` of PORT into a poisoned t2 after the refused sw, executed by the free-run (want 0).
     D10: the announce names 0x9.
  F0 diag (D3 as first worded): the shipped F plus a `print` of a GPR that no guest instruction loads.
  V  D5: COMMAND=GET_RESOLUTION, X1=123, one refusal, read X1 (want 123); fill ports 1-7 with 0x11*p (COMMAND keeps 2 --
     writing port 0 would execute it), four refusals (9, 16, 0x100000003 sd, 0xff sb), read back all eight ports.
  W  D7: sb / sh / sd of 0, each after its own PORT=5.  D6: `ld` of PORT with selector 5 (want exactly 0x5).
     D2: sd 0x8000000000000000 after PORT=5.  D8: previous 7 and previous 6.  grok F2 #7: sd of 8 after PORT=5.
     diag: D2 as first worded (sd 0x8000000000000005).
  U7 diag (D7 as first worded): sb 0 then sd 0 from power-on, no non-zero predecessor.

Output: one row per check, then FBCTRLP_CONTROL=OK|FAILED, FBCTRLP_RESULT=n/t (non-diag rows),
FBCTRLP_DIAG=n/t, FBCTRLP_DONE.
usage: fbctrl_port_probe.f2proto.py <gxemul-binary>
"""
import os
import pty
import re
import select
import signal
import sys
import time

BIN = sys.argv[1]

STUBADDR = 0xffffffff80100000
CODE = 0xffffffff80100020
FBCTRL = 0xffffffffb2f00000

ONCE_RE = re.compile(r"\[ fbctrl: port number 0x[0-9a-f]+ is out of range; the selector is unchanged \(once\) \]")
VAL_RE = re.compile(r"\[ fbctrl: port number (0x[0-9a-f]+) is out of range; the selector is unchanged \(once\) \]")
NARROW_RE = re.compile(r"\[ fbctrl: port number 0x[89] is out of range; the selector is unchanged \(once\) \]")

REG = dict(zr=0, v0=2, v1=3, a0=4, a1=5, a2=6, a3=7, t0=8, t1=9, t2=10, t3=11, t4=12, t5=13, t6=14, t7=15,
           s0=16, s1=17, s2=18, s3=19, s4=20, s5=21, s6=22, s7=23, t8=24, t9=25)
OPS = dict(sb=0x28, sh=0x29, sw=0x2b, sd=0x3f, lw=0x23, ld=0x37)


def ins(op, rt, off, base="t0"):
    return (OPS[op] << 26) | (REG[base] << 21) | (REG[rt] << 16) | (off & 0xffff)


def text(op, rt, off, base="t0"):
    return "%s %s,%d(%s)" % (op, rt, off, base)


ANCHOR = (0x0f << 26) | (REG["t7"] << 16)                   # lui t7,0 -- the breakpoint anchor, never executed
assert ins("sw", "t1", 0) == 0xad090000
assert ins("lw", "t2", 0x10) == 0x8d0a0010
assert ins("sd", "t5", 0) == 0xfd0d0000
assert ins("sb", "t8", 0) == 0xa1180000
assert ins("sh", "t9", 0) == 0xa5190000
assert ins("ld", "s3", 0) == 0xdd130000
assert ins("sb", "zr", 0) == 0xa1000000
assert ANCHOR == 0x3c0f0000


def stub_path():
    p = "/tmp/gx_fbctrl549f2p_%d.bin" % os.getpid()
    with open(p, "wb") as f:
        f.write(b"\x00\x00\x00\x00")
    return p


def session(label, prog, regs, reads, stub, free_run=False):
    """prog: list of (op, rt, off, tag).  As the shipped probe, plus pos_after (tag -> len(buf) right after that step)."""
    pid, fd = pty.fork()
    if pid == 0:
        os.execvp(BIN, [BIN, "-V", "-E", "testmips", "-M", "64", "0x%x:%s" % (STUBADDR, stub)])
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

    words = [ins(op, rt, off) for op, rt, off, _t in prog] + [ANCHOR]
    status, badis, vals, once_after, pos_after, steps = "?", [], {}, {}, {}, 0
    if not wait(timeout=120):
        status = "NO-PROMPT"
    else:
        for i, w in enumerate(words):
            send("put w 0x%x, 0x%08x" % (CODE + 4 * i, w))
        for name, val in regs:
            send("%s=0x%x" % (name, val & 0xffffffffffffffff))
        send("pc=0x%x" % CODE)
        status = "SURVIVED"
        if free_run:
            send("breakpoint add 0x%x" % (CODE + 4 * len(prog)))
            mark = len(buf)
            b = b"continue\n"
            try:
                os.write(fd, b)
            except OSError:
                dead[0] = True
            if not wait(mark=mark, timeout=60) or dead[0]:
                status = "HOST-DIED" if dead[0] else "NO-BREAK"
            elif ("%016x" % (CODE + 4 * len(prog))) not in buf[mark:] and \
                    ("%08x" % ((CODE + 4 * len(prog)) & 0xffffffff)) not in buf[mark:]:
                status = "NO-BREAK"
            else:
                steps = len(prog)
                once_after["free"] = len(ONCE_RE.findall(buf))
                pos_after["free"] = len(buf)
        else:
            for i, (op, rt, off, tag) in enumerate(prog):
                mark = len(buf)
                if not send("step 1", timeout=30) or dead[0]:
                    status = "HOST-DIED"
                    break
                steps += 1
                seg = buf[mark:]
                w = words[i]
                m = re.search(r"%016x:?\s+%08x\s+([^\r\n<]+)" % (CODE + 4 * i, w), seg)
                got = re.sub(r"\s+", " ", m.group(1)).strip() if m else "(no step line)"
                if not got.startswith(text(op, rt, off)):
                    badis.append("+0x%02x planted 0x%08x -> %r, expected %r" % (4 * i, w, got, text(op, rt, off)))
                if tag:
                    once_after[tag] = len(ONCE_RE.findall(buf))
                    pos_after[tag] = len(buf)
        if status == "SURVIVED":
            for name in reads:
                got = None
                for _ in range(2):
                    mark = len(buf)
                    if not send("print %s" % name, timeout=30) or dead[0]:
                        break
                    m = re.search(r"(?m)^0x([0-9a-fA-F]+)\s*$", buf[mark:])
                    if m:
                        got = int(m.group(1), 16)
                        break
                vals[name] = got
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
    code = os.WEXITSTATUS(st) if st is not None and os.WIFEXITED(st) else None
    print("  session %-2s %-9s steps=%d/%d exit=%s once=%d" % (label, status, steps, len(prog), code,
                                                              len(ONCE_RE.findall(buf))))
    for b in badis:
        print("      DISASSEMBLY MISMATCH: %s" % b)
    return {"status": status, "exit": code, "badis": badis, "vals": vals, "once_after": once_after,
            "pos_after": pos_after, "steps": steps, "buf": buf, "n": len(prog)}


RESULTS = []
DIAG = []


def row(name, got, want, note="", diag=False):
    ok = got == want
    (DIAG if diag else RESULTS).append(ok)
    tagw = ("ok" if ok else "FAIL") if not diag else ("dok" if ok else "DRED")
    print("  %-4s %-58s got=%-20s want=%-20s %s" % (tagw, name, got, want, note))
    return ok


def hx(v):
    return "-" if v is None else "0x%x" % v


def count_at(S, tag, rx):
    p = S["pos_after"].get(tag)
    return None if p is None else len(rx.findall(S["buf"][:p]))


def first_val(S):
    m = VAL_RE.findall(S["buf"])
    return m[0] if m else "-"


M64 = 0xffffffffffffffff

# ---------------------------------------------------------------- sessions
PROG_C = [("sw", "t1", 0, None), ("sw", "t3", 16, None), ("lw", "t4", 16, None), ("lw", "t5", 0, None),
          ("sw", "t6", 0, None), ("sw", "t7", 16, None),
          ("sw", "s1", 0, None), ("sw", "t7", 16, None),                  # D11: PORT=2 (Y1), Y1 = 123
          ("sw", "s0", 0, None), ("sw", "s1", 16, None),
          ("sw", "t6", 0, None), ("lw", "s2", 16, None),
          ("sw", "s1", 0, None), ("lw", "s3", 16, None)]                  # D11: PORT=2, read Y1
REGS_C = [("t0", FBCTRL), ("t1", 5), ("t3", 0x2a), ("t6", 1), ("t7", 123), ("s0", 0), ("s1", 2),
          ("t4", 0xdead), ("t5", 0xdead), ("s2", 0xdead), ("s3", 0xdead)]

ACC = [(0, "sw"), (1, "sb"), (2, "sh"), (3, "sw"), (4, "sd"), (5, "sb"), (6, "sh"), (7, "sd")]
SEL_REG = ["t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8"]
VAL_REG = ["zr", "a0", "a1", "a2", "a3", "v0", "v1", "t9"]
PORT_RB = ["s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7"]
PROG_A, REGS_A = [], [("t0", FBCTRL)]
for k, (p, w) in enumerate(ACC):
    REGS_A.append((SEL_REG[k], p))
    REGS_A.append((PORT_RB[k], 0xdead))
    if k:
        REGS_A.append((VAL_REG[k], 0x11 * p))
    PROG_A.append((w, SEL_REG[k], 0, None))
    PROG_A.append(("lw", PORT_RB[k], 0, None))
    PROG_A.append(("sw", VAL_REG[k], 16, None))
for k, (p, w) in enumerate(ACC):
    if k:
        PROG_A.append(("sw", SEL_REG[k], 0, None))
        PROG_A.append(("lw", SEL_REG[k], 16, None))
READS_A = PORT_RB + SEL_REG[1:]

#  P: first refusal 8 (D9), nine read-back refusals, two count-only refusals, then the tail.
REFUSE = [("sw", "t2", 8, "8 (sw)"), ("sw", "t1", 9, "9 (sw)"), ("sw", "t3", 16, "16 (sw)"),
          ("sd", "t4", 0x200000000, "0x200000000 (sd)"), ("sd", "t5", 0x100000003, "0x100000003 (sd)"),
          ("sd", "t6", M64, "all-ones (sd)"), ("sw", "t7", 0xffffffff, "all-ones (sw)"),
          ("sb", "t8", 0xff, "0xff (sb)"), ("sh", "t9", 0x100, "0x100 (sh)")]
EXTRA = [("sb", "t3", "16 (sb)"), ("sh", "t3", "16 (sh)")]
READ_P = ["s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7", "v0"]
PROG_P = [("sw", "a0", 0, None), ("sw", "a1", 16, None)]
REGS_P = [("t0", FBCTRL), ("a0", 5), ("a1", 0x2a), ("a2", 7)]
for k, (w, r, v, _n) in enumerate(REFUSE):
    REGS_P.append((r, v))
    if k:
        PROG_P.append(("sw", "a0", 0, None))
    PROG_P.append((w, r, 0, "r%d" % k))
    PROG_P.append(("lw", READ_P[k], 0, None))
for j, (w, r, _n) in enumerate(EXTRA):
    PROG_P.append(("sw", "a0", 0, None))
    PROG_P.append((w, r, 0, "x%d" % j))
PROG_P += [("sw", "a2", 0, None), ("sw", "t1", 0, "rtail"), ("lw", "v1", 0, None)]
READS_P = READ_P + ["v1"]

#  R (D4): a DATA write and a NOP command between two refusals.
PROG_R = [("sw", "a0", 0, None), ("sw", "t1", 0, "ra"), ("lw", "s0", 0, None),
          ("sw", "a1", 16, None), ("sw", "zr", 0, None), ("sw", "zr", 16, None),
          ("sw", "a0", 0, None), ("sw", "t1", 0, "rb"), ("lw", "s1", 0, None)]
REGS_R = [("t0", FBCTRL), ("a0", 5), ("a1", 0x2a), ("t1", 9), ("s0", 0xdead), ("s1", 0xdead)]

PROG_K = [("sw", "t1", 0, None), ("sw", "t3", 16, None), ("sw", "t2", 0, None), ("lw", "s0", 16, None),
          ("sw", "t4", 16, None), ("sw", "t1", 0, None), ("lw", "s1", 16, None)]
REGS_K = [("t0", FBCTRL), ("t1", 5), ("t3", 0x2a), ("t2", 9), ("t4", 0x77), ("s0", 0xdead), ("s1", 0xdead)]

#  F (D3): the free-run executes the refused sw AND a guest lw of PORT into a poisoned t2.
PROG_F = [("sw", "t1", 0, None), ("lw", "t2", 0, None)]
REGS_F = [("t0", FBCTRL), ("t1", 9), ("t2", 0xdead)]
#  F0 diag: the shipped F, plus a print of a GPR nothing loads.
PROG_F0 = [("sw", "t1", 0, None)]
REGS_F0 = [("t0", FBCTRL), ("t1", 9)]

#  V (D5)
REGS_V = [("t0", FBCTRL)] + [("s%d" % p, p) for p in range(1, 8)] + [("t%d" % p, 0x11 * p) for p in range(1, 8)] + \
         [("t8", 123), ("a0", 9), ("a1", 16), ("a2", 0x100000003), ("a3", 0xff), ("v0", 0xdead), ("v1", 0xdead)]
PROG_V = [("sw", "zr", 0, None), ("sw", "s2", 16, None),            # COMMAND = GET_RESOLUTION (X1 = Y1 = 0)
          ("sw", "s1", 0, None), ("sw", "t8", 16, None),            # X1 = 123
          ("sw", "a0", 0, None),                                     # refuse 9
          ("sw", "s1", 0, None), ("lw", "v0", 16, None)]             # read X1
for p in range(1, 8):
    PROG_V += [("sw", "s%d" % p, 0, None), ("sw", "t%d" % p, 16, None)]
PROG_V += [("sw", "a0", 0, None), ("sw", "a1", 0, None), ("sd", "a2", 0, None), ("sb", "a3", 0, None)]
PROG_V += [("sw", "zr", 0, None), ("lw", "v1", 16, None)]
for p in range(1, 8):
    PROG_V += [("sw", "s%d" % p, 0, None), ("lw", "s%d" % p, 16, None)]
READS_V = ["v0", "v1"] + ["s%d" % p for p in range(1, 8)]

#  W (D7, D6, D2, D8, grok #7; diag D2 as first worded)
REGS_W = [("t0", FBCTRL), ("a0", 5), ("a2", 7), ("a3", 6), ("t1", 9), ("t2", 0x8000000000000000),
          ("t3", 0x8000000000000005), ("t4", 8)] + [(r, 0xdead) for r in
                                                    ("s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7", "v0")]
PROG_W = [("sw", "a0", 0, None), ("sb", "zr", 0, None), ("lw", "s0", 0, None),
          ("sw", "a0", 0, None), ("sh", "zr", 0, None), ("lw", "s1", 0, None),
          ("sw", "a0", 0, None), ("sd", "zr", 0, None), ("lw", "s2", 0, None),
          ("sw", "a0", 0, None), ("ld", "s3", 0, None),
          ("sw", "a0", 0, None), ("sd", "t2", 0, None), ("lw", "s4", 0, None),
          ("sw", "a0", 0, None), ("sd", "t3", 0, None), ("lw", "s5", 0, None),
          ("sw", "a2", 0, None), ("sw", "t1", 0, None), ("lw", "s6", 0, None),
          ("sw", "a3", 0, None), ("sw", "t1", 0, None), ("lw", "s7", 0, None),
          ("sw", "a0", 0, None), ("sd", "t4", 0, None), ("lw", "v0", 0, None)]
READS_W = ["s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7", "v0"]

#  U7 diag: D7 as first worded (no non-zero predecessor)
PROG_U7 = [("sb", "zr", 0, None), ("lw", "s0", 0, None), ("sd", "zr", 0, None), ("lw", "s1", 0, None)]
REGS_U7 = [("t0", FBCTRL), ("s0", 0xdead), ("s1", 0xdead)]


def main():
    stub = stub_path()
    try:
        C = session("C", PROG_C, REGS_C, ["t4", "t5", "s2", "s3"], stub)
        A = session("A", PROG_A, REGS_A, READS_A, stub)
        P = session("P", PROG_P, REGS_P, READS_P, stub)
        R = session("R", PROG_R, REGS_R, ["s0", "s1"], stub)
        K = session("K", PROG_K, REGS_K, ["s0", "s1"], stub)
        F = session("F", PROG_F, REGS_F, ["t2"], stub, free_run=True)
        F0 = session("F0", PROG_F0, REGS_F0, ["t2"], stub, free_run=True)
        V = session("V", PROG_V, REGS_V, READS_V, stub)
        W = session("W", PROG_W, REGS_W, READS_W, stub)
        U7 = session("U7", PROG_U7, REGS_U7, ["s0", "s1"], stub)
    finally:
        try:
            os.unlink(stub)
        except OSError:
            pass
    ctl = []
    print("CONTROLS")
    ctl.append(row("C every step survived", "%s %d/%d" % (C["status"], C["steps"], C["n"]),
                   "SURVIVED %d/%d" % (len(PROG_C), len(PROG_C))))
    ctl.append(row("C disassembly of every stepped word", len(C["badis"]), 0))
    ctl.append(row("C LIVENESS: DATA round-trips 0x2a", hx(C["vals"].get("t4")), "0x2a"))
    ctl.append(row("C LIVENESS: PORT reads back 5", hx(C["vals"].get("t5")), "0x5"))
    ctl.append(row("C SIGNATURE: X1 zeroed by GET_RESOLUTION", hx(C["vals"].get("s2")), "0x0",
                   "(RAM: 2; banked w/o command: 123)"))
    row("C nothing refused, no (once) line", len(ONCE_RE.findall(C["buf"])), 0)
    for lab, S in (("A", A), ("P", P), ("R", R), ("K", K), ("V", V), ("W", W), ("U7", U7)):
        ctl.append(row("%s disassembly of every stepped word" % lab, len(S["badis"]), 0))
    print("D11 (session C)")
    row("D11 Y1 (prefilled 123) zeroed by GET_RESOLUTION", hx(C["vals"].get("s3")), "0x0")
    print("ACCEPT (session A: %s %d/%d)" % (A["status"], A["steps"], A["n"]))
    for k, (p, w) in enumerate(ACC):
        row("accept selector %d written by %s" % (p, w), hx(A["vals"].get(PORT_RB[k])), hx(p))
    for k, (p, w) in enumerate(ACC):
        if k:
            row("port %d round-trips its DATA value" % p, hx(A["vals"].get(SEL_REG[k])), hx(0x11 * p))
    row("A nothing refused, no (once) line [Astra]", len(ONCE_RE.findall(A["buf"])), 0)
    print("REFUSE (session P: %s %d/%d)" % (P["status"], P["steps"], P["n"]))
    for k, (w, r, v, name) in enumerate(REFUSE):
        row("refuse %s, PORT keeps 5" % name, hx(P["vals"].get(READ_P[k])), "0x5")
    row("refuse 9 after PORT=7, PORT keeps 7", hx(P["vals"].get("v1")), "0x7")
    row("announce: exactly 1 right after the FIRST refusal (8)", P["once_after"].get("r0"), 1)
    row("announce: still exactly 1 after twelve refusals [D9]", P["once_after"].get("rtail"), 1)
    row("D10 P first announce names the refused value", first_val(P), "0x8")
    row("UNCORR-D9 count sampled at the 10th refusal", P["once_after"].get("x0"), 1, "", True)
    row("UNCORR-D10 narrow (0x8/0x9) count after the FIRST refusal", count_at(P, "r0", NARROW_RE), 1, "", True)
    row("UNCORR-D10 narrow (0x8/0x9) count after twelve refusals", count_at(P, "rtail", NARROW_RE), 1, "", True)
    print("RE-ARM (session R: %s %d/%d)" % (R["status"], R["steps"], R["n"]))
    row("D4 announce still 1 after a DATA write and a NOP between refusals", R["once_after"].get("rb"), 1)
    print("THE WITNESS PAIR (session K)")
    row("K survives DATA after a refused PORT write", "%s %d/%d" % (K["status"], K["steps"], K["n"]),
        "SURVIVED %d/%d" % (len(PROG_K), len(PROG_K)))
    row("K DATA read after the refusal is port 5's", hx(K["vals"].get("s0")), "0x2a")
    row("K DATA write after the refusal lands in port 5", hx(K["vals"].get("s1")), "0x77")
    print("FREE-RUNNING (session F)")
    row("F free-run reached its breakpoint", F["status"], "SURVIVED")
    row("F refusal announced while free-running (fatal)", F["once_after"].get("free"), 1)
    row("D3 F guest lw of PORT after the power-on refusal", hx(F["vals"].get("t2")), "0x0")
    row("D10 F announce names the refused value", first_val(F), "0x9")
    row("UNCORR-D3 F0 print of an unloaded GPR after the free-run", hx(F0["vals"].get("t2")), "0x0", "", True)
    print("FILL / READ-BACK (session V: %s %d/%d)" % (V["status"], V["steps"], V["n"]))
    row("D5 X1=123 survives a refusal (COMMAND=GET_RESOLUTION)", hx(V["vals"].get("v0")), hx(123))
    row("D5 port 0 (COMMAND) still 2 after four refusals", hx(V["vals"].get("v1")), "0x2")
    for p in range(1, 8):
        row("D5 port %d keeps its fill after four refusals" % p, hx(V["vals"].get("s%d" % p)), hx(0x11 * p))
    print("WIDTHS / PREDECESSORS (session W: %s %d/%d)" % (W["status"], W["steps"], W["n"]))
    row("D7 accept selector 0 written by sb after PORT=5", hx(W["vals"].get("s0")), "0x0")
    row("D7 accept selector 0 written by sh after PORT=5", hx(W["vals"].get("s1")), "0x0")
    row("D7 accept selector 0 written by sd after PORT=5", hx(W["vals"].get("s2")), "0x0")
    row("D6 ld of PORT reads exactly 5", hx(W["vals"].get("s3")), "0x5")
    row("D2 refuse 0x8000000000000000 (sd), PORT keeps 5", hx(W["vals"].get("s4")), "0x5")
    row("UNCORR-D2 refuse 0x8000000000000005 (sd), PORT keeps 5", hx(W["vals"].get("s5")), "0x5", "", True)
    row("D8 refuse 9 after PORT=7, PORT keeps 7 (W)", hx(W["vals"].get("s6")), "0x7")
    row("D8 refuse 9 after PORT=6, PORT keeps 6", hx(W["vals"].get("s7")), "0x6")
    row("G7 refuse 8 (sd), PORT keeps 5", hx(W["vals"].get("v0")), "0x5")
    print("DIAG (session U7)")
    row("UNCORR-D7 sb 0 from power-on reads 0", hx(U7["vals"].get("s0")), "0x0", "", True)
    row("UNCORR-D7 sd 0 after that reads 0", hx(U7["vals"].get("s1")), "0x0", "", True)
    control = all(ctl)
    n_ok, n = sum(RESULTS), len(RESULTS)
    print("FBCTRLP_CONTROL=%s" % ("OK" if control else "FAILED"))
    print("FBCTRLP_RESULT=%d/%d" % (n_ok, n))
    print("FBCTRLP_DIAG=%d/%d" % (sum(DIAG), len(DIAG)))
    print("FBCTRLP_DONE")


if __name__ == "__main__":
    main()
