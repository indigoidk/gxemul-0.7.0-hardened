#!/usr/bin/env python3
"""fbd5 pass 1, measurement 4: THE HARNESS LEGS' PREMISE.

Three launchers exist and are separately implemented:
  S = regress/footbridge_sites_probe.py's nested helper inside run_arm()
  D = regress/fbpending_drain_probe.py's class Session
  W = regress/fbpending_witness.py's class Session
The helper bodies below are COPIED VERBATIM from those files (the only edit is
that the emulation name is a parameter, which is what a K1 leg needs).  Nothing
in the real probes is written.

LEG K1 -- startup rejection: launch with an unused -E name through the launcher
          itself; no prompt; the diagnostic names the bad input; exit status 1.
LEG K2 -- death after execution: a verified-complete prologue, then `quit`, then
          the NEXT ordinary interaction; does it fail, how, and how fast?

usage: legs.py <gxemul> <stub>
"""
import os, pty, re, select, signal, sys, time

BIN, STUB = sys.argv[1], sys.argv[2]
CODE, DATA = 0x00008000, 0x00009000
PRO = [(0x00, 0xEE110F10), (0x04, 0xE3C00001), (0x08, 0xEE010F10),
       (0x0c, 0xEE113F10), (0x10, 0xE3A00442), (0x14, 0xE3A04A09),
       (0x18, 0xE5945000), (0x1c, 0xE5906000), (0x20, 0xE1A00000)]


class L:
    """The launcher, in the three shapes the three probes use.

    kind='S' reproduces footbridge_sites_probe.py's run_arm() closure: a
        TOTAL-time wait deadline.
    kind='D'/'W' reproduce the two Session classes: an INACTIVITY deadline
        (`if len(self.buf) != seen: seen = ...; t = time.time()`), which is the
        only difference between the two families that matters here.
    """

    def __init__(self, kind, emul="cats"):
        self.kind, self.buf, self.dead = kind, "", False
        self.pid, self.fd = pty.fork()
        if self.pid == 0:
            os.execvp(BIN, [BIN, "-V", "-T", "-E", emul, "-M", "32",
                            "0x%x:%s" % (CODE, STUB)])
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
        t = time.time()
        seen = len(self.buf)
        while time.time() - t < timeout:
            if not self.rd():
                return False
            if self.kind != "S" and len(self.buf) != seen:
                seen = len(self.buf)
                t = time.time()
            resp = self.buf[mark:]
            if echo is not None and echo not in resp:
                continue
            if len(self.buf) > mark and resp.rstrip().endswith("GXemul>"):
                return True
        return False

    def send(self, x, timeout=60):
        b = (x + "\n").encode("latin1")
        _mark, n = len(self.buf), 0
        try:
            while n < len(b):
                n += os.write(self.fd, b[n:])
        except OSError:
            self.dead = True
            return False
        return self.wait(mark=_mark, echo=x if x else None, timeout=timeout)

    def reap(self, patience=10.0):
        try:
            os.close(self.fd)
        except OSError:
            pass
        pid, st, gone = 0, None, False
        t1 = time.time()
        while pid == 0 and time.time() - t1 < patience:
            try:
                pid, st = os.waitpid(self.pid, os.WNOHANG)
            except OSError:
                gone = True
                break
            if pid == 0:
                time.sleep(0.05)
        hk = False
        if pid == 0 and not gone:
            hk = True
            try:
                os.kill(self.pid, signal.SIGKILL)
            except OSError:
                pass
            try:
                _, st = os.waitpid(self.pid, 0)
            except OSError:
                st = None
        return dict(raw=st, gone=gone, harness_killed=hk,
                    exited=(st is not None and os.WIFEXITED(st)),
                    code=(os.WEXITSTATUS(st)
                          if st is not None and os.WIFEXITED(st) else None),
                    signal=(os.WTERMSIG(st)
                            if st is not None and os.WIFSIGNALED(st) else None))


def k1(kind, name="nosuchmachine"):
    print("")
    print("---- LEG K1 through launcher %s, -E %s" % (kind, name))
    s = L(kind, name)
    t0 = time.time()
    got_prompt = s.wait(timeout=30)
    el = time.time() - t0
    t1, eof = time.time(), False
    while time.time() - t1 < 5.0:
        if not s.rd(0.1):
            eof = True
            break
    r = s.reap()
    out = s.buf.replace("\r", "")
    print("  wait()->%s in %.2fs   eof=%s  dead=%s" % (got_prompt, el, eof, s.dead))
    print("  reaped: exited=%s code=%s signal=%s gone=%s harness_killed=%s"
          % (r["exited"], r["code"], r["signal"], r["gone"], r["harness_killed"]))
    print("  ---- everything the child wrote (%d bytes) ----" % len(out))
    for line in out.splitlines():
        if line.strip():
            print("  | %s" % line)
    names = name in out
    print("  NAMES-THE-INPUT=%s   K1 PASS-SHAPE=%s"
          % (names, got_prompt is False and r["exited"] and r["code"] == 1))
    return out


def k2(kind):
    print("")
    print("---- LEG K2 through launcher %s" % kind)
    s = L(kind)
    if not s.wait(timeout=120):
        print("  NO PROMPT -- cannot run this leg")
        return
    s.send("put w 0x%08x, 0x%08x" % (DATA, 0x11223344))
    for off, w in PRO:
        s.send("put w 0x%08x, 0x%08x" % (CODE + off, w))
    s.send("pc=0x%08x" % CODE)
    for _ in PRO[:-1]:
        if not s.send("step 1", timeout=30) or s.dead:
            print("  PROLOGUE DID NOT COMPLETE")
            return
    mark = len(s.buf)
    ok = s.send("reg", timeout=30)
    seg = s.buf[mark:]
    vals = {}
    for n in ("r3", "r5", "r6"):
        m = re.search(r"\b%s\s*=\s*0x([0-9a-fA-F]+)" % n, seg)
        vals[n] = m.group(1) if m else None
    print("  prologue verified by a FRESH reg: ok=%s  r3=%s (MMU bit0=%s) r5=%s r6=%s"
          % (ok, vals["r3"],
             (int(vals["r3"], 16) & 1) if vals["r3"] else "?",
             vals["r5"], vals["r6"]))
    #  now the quit, then the NEXT ordinary interaction -- no cleanup in between
    t0 = time.time()
    qok = s.send("quit", timeout=10)
    tq = time.time() - t0
    print("  send('quit') -> %s in %.2fs   dead=%s" % (qok, tq, s.dead))
    t0 = time.time()
    nok = s.send("reg", timeout=30)
    tn = time.time() - t0
    print("  NEXT send('reg') -> %s in %.2fs   dead=%s   <== the K2 observable"
          % (nok, tn, s.dead))
    r = s.reap()
    print("  reaped: exited=%s code=%s signal=%s gone=%s harness_killed=%s"
          % (r["exited"], r["code"], r["signal"], r["gone"], r["harness_killed"]))
    print("  K2 PASS-SHAPE=%s (next interaction failed, dead set, exit 0)"
          % (nok is False and s.dead and r["exited"] and r["code"] == 0))
    tail = s.buf.replace("\r", "").splitlines()[-4:]
    print("  tail: %s" % " / ".join(t.strip() for t in tail if t.strip()))


print("LEGS BINARY=%s" % BIN)
for kind in ("S", "D", "W"):
    k1(kind)
for kind in ("S", "D", "W"):
    k2(kind)
#  a control on K1 itself: the SAME leg with the CORRECT name must NOT pass it
print("")
print("==== K1 NEGATIVE CONTROL: the good name must not satisfy the leg ====")
k1("S", "cats")
print("LEGS_DONE")
