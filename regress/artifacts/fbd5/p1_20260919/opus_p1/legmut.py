#!/usr/bin/env python3
"""fbd5 pass 1: mutants of the LEGS themselves (brief Q2 h/i, Q4).

usage: legmut.py <fixed-gxemul> <prefix-gxemul> <stub>

h) K1 passing on ANY nonzero exit: measure what OTHER startup refusals exit with,
   so the question "is exit!=0 a discriminator?" is settled by measurement.
i) K2 passing when the child died BEFORE the prologue completed: drive the K2
   observables on a PRE-FIX binary whose prologue contains a terminating access,
   and report which of the leg's clauses still fire.
"""
import os, pty, re, select, signal, sys, time

FIXED, PREFIX, STUB = sys.argv[1], sys.argv[2], sys.argv[3]
CODE, DATA = 0x00008000, 0x00009000
PRO = [(0x00, 0xEE110F10), (0x04, 0xE3C00001), (0x08, 0xEE010F10),
       (0x0c, 0xEE113F10), (0x10, 0xE3A00442), (0x14, 0xE3A04A09),
       (0x18, 0xE5945000), (0x1c, 0xE5906000)]
KILL = (0x20, 0xE590718C)        # ldr r7,[r0,#396] -- +0x18c, terminating pre-fix
PAD = (0x24, 0xE1A00000)


class L:
    def __init__(self, binary, argv):
        self.buf, self.dead = "", False
        self.pid, self.fd = pty.fork()
        if self.pid == 0:
            os.execvp(binary, argv)
            os._exit(127)

    def rd(self, t=0.4):
        r, _, _ = select.select([self.fd], [], [], t)
        if self.fd not in r:
            return True
        try:
            d = os.read(self.fd, 65536)
        except OSError:
            self.dead = True
            return False
        if not d:
            self.dead = True
            return False
        self.buf += d.decode("latin1", "replace")
        return True

    def wait(self, mark=0, echo=None, timeout=60):
        t, seen = time.time(), len(self.buf)
        while time.time() - t < timeout:
            if not self.rd():
                return False
            if len(self.buf) != seen:
                seen, t = len(self.buf), time.time()
            resp = self.buf[mark:]
            if echo is not None and echo not in resp:
                continue
            if len(self.buf) > mark and resp.rstrip().endswith("GXemul>"):
                return True
        return False

    def send(self, x, timeout=60):
        b, n, _mark = (x + "\n").encode("latin1"), 0, len(self.buf)
        try:
            while n < len(b):
                n += os.write(self.fd, b[n:])
        except OSError:
            self.dead = True
            return False
        return self.wait(mark=_mark, echo=x if x else None, timeout=timeout)

    def reap(self):
        t1, eof = time.time(), False
        while time.time() - t1 < 5.0:
            if not self.rd(0.1):
                eof = True
                break
        try:
            os.close(self.fd)
        except OSError:
            pass
        pid, st = 0, None
        t1 = time.time()
        while pid == 0 and time.time() - t1 < 10.0:
            try:
                pid, st = os.waitpid(self.pid, os.WNOHANG)
            except OSError:
                break
            if pid == 0:
                time.sleep(0.05)
        if pid == 0:
            try:
                os.kill(self.pid, signal.SIGKILL)
                _, st = os.waitpid(self.pid, 0)
            except OSError:
                st = None
        return (os.WEXITSTATUS(st) if st is not None and os.WIFEXITED(st) else None,
                os.WTERMSIG(st) if st is not None and os.WIFSIGNALED(st) else None,
                eof)


print("==== Q2(h): what do OTHER startup refusals exit with? ====")
CASES = [
    ("unused -E name   ", [FIXED, "-V", "-T", "-E", "nosuchmachine", "-M", "32",
                           "0x8000:" + STUB]),
    ("no file argument ", [FIXED, "-V", "-T", "-E", "cats", "-M", "32"]),
    ("missing file     ", [FIXED, "-V", "-T", "-E", "cats", "-M", "32",
                           "0x8000:/no/such/file.bin"]),
    ("unknown option   ", [FIXED, "-V", "-T", "--no-such-option", "-E", "cats",
                           "-M", "32", "0x8000:" + STUB]),
    ("bad -M value     ", [FIXED, "-V", "-T", "-E", "cats", "-M", "notanumber",
                           "0x8000:" + STUB]),
]
for label, argv in CASES:
    s = L(FIXED, argv)
    got = s.wait(timeout=20)
    code, sig, eof = s.reap()
    first = [x for x in s.buf.replace("\r", "").splitlines() if x.strip()]
    print("  %s prompt=%-5s exit=%-4s signal=%-4s  first line: %s"
          % (label, got, code, sig, (first[0][:70] if first else "(silence)")))
    print("      names 'nosuchmachine'? %s" % ("nosuchmachine" in s.buf))

print("")
print("==== Q2(i): the K2 leg with the child dead BEFORE the prologue ended ====")
for label, binary in (("PRE-FIX (dies at +0x18c)", PREFIX), ("FIXED (survives)", FIXED)):
    s = L(binary, [binary, "-V", "-T", "-E", "cats", "-M", "32",
                   "0x%x:%s" % (CODE, STUB)])
    if not s.wait(timeout=120):
        print("  %s : NO PROMPT" % label)
        continue
    s.send("put w 0x%08x, 0x%08x" % (DATA, 0x11223344))
    for off, w in PRO + [KILL, PAD]:
        s.send("put w 0x%08x, 0x%08x" % (CODE + off, w))
    s.send("pc=0x%08x" % CODE)
    completed = True
    for _ in PRO + [KILL]:
        if not s.send("step 1", timeout=30) or s.dead:
            completed = False
            break
    mark = len(s.buf)
    fresh = s.send("reg", timeout=30) and not s.dead
    r6 = re.search(r"\br6\s*=\s*0x([0-9a-fA-F]+)", s.buf[mark:])
    qok = s.send("quit", timeout=10)
    nok = s.send("reg", timeout=30)
    code, sig, eof = s.reap()
    fatals = re.findall(r"(\[[^\r\n\]]*footbridge[^\r\n\]]*\])", s.buf)
    print("  %-26s prologue-completed=%-5s fresh-reg=%-5s r6=%s"
          % (label, completed, fresh, r6.group(1) if r6 else None))
    print("      quit->%-5s next-send->%-5s dead=%-5s exit=%-4s signal=%s"
          % (qok, nok, s.dead, code, sig))
    print("      leg clauses: [next-send-fails]=%s [dead]=%s [exit==0]=%s "
          "[prologue verified by a FRESH reg]=%s" %
          (nok is False, s.dead, code == 0, fresh))
    print("      complaints: %s" % (fatals or "NONE"))
print("LEGMUT_DONE")
