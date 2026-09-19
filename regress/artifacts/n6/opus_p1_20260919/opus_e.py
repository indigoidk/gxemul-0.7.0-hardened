#!/usr/bin/env python3
"""E0-E6: the brief's section-5 ACCEPT rows, measured.  Runs on whatever binary
it is given, so the same script scores the pre-fix baseline (host dies at E0)
and a post-fix build.  Register parsing is NAME-AWARE: the emulator prints
r10..r14 as sl/fp/ip/sp/lr, so an r<N>= regex silently misses them.
usage: opus_e.py <gxemul> <stub> <label>
"""
import os, pty, re, select, sys, time

BIN, STUB = sys.argv[1], sys.argv[2]
LABEL = sys.argv[3] if len(sys.argv) > 3 else "?"
CODE, DATA, NOP = 0x00008000, 0x00009000, 0xE1A00000
P, Q = 0x00002002, 0x60000000
CONSTS = {0x00: 0x11223344, 0x08: P, 0x0c: Q}
ALIAS = {10: "sl", 11: "fp", 12: "ip", 13: "sp", 14: "lr"}

PROG = [
    (0x00, 0xEE110F10, "read CP15 c1"),
    (0x04, 0xE3C00001, "clear MMU enable bit"),
    (0x08, 0xEE010F10, "MMU OFF -> VA == PA"),
    (0x0c, 0xEE113F10, "C2: read CP15 c1 BACK -> r3 (overwritten by E1)"),
    (0x10, 0xE3A00442, "r0 = 0x42000000 footbridge base"),
    (0x14, 0xE3A04A09, "r4 = 0x9000 scratch RAM"),
    (0x18, 0xE5942000, "C1 liveness: ldr r2,[r4] -> 0x11223344 (checked as r2? no: see C1)"),
    (0x1c, 0xE5906000, "A1 devsig: ldr r6,[r0] VENDOR_ID -> 0x1011"),
    (0x20, 0xE5901188, "E0 : ldr r1,[r0,#392]   read +0x188 BEFORE any enable write"),
    (0x24, 0xE5942008, "     ldr r2,[r4,#8]     r2 = P = 0x00002002"),
    (0x28, 0xE5802188, "     str r2,[r0,#392]   IRQEnableSet <- P"),
    (0x2c, 0xE5903188, "E1 : ldr r3,[r0,#392]   read back -> want P"),
    (0x30, 0xE594200C, "     ldr r2,[r4,#12]    r2 = Q = 0x60000000"),
    (0x34, 0xE5802188, "     str r2,[r0,#392]   IRQEnableSet <- Q"),
    (0x38, 0xE5905188, "E2 : ldr r5,[r0,#392]   read back -> want P|Q"),
    (0x3c, 0xE5D0A188, "E3 : ldrb sl,[r0,#392]  BYTE read -> want 0x02"),
    (0x40, 0xE2808D06, "     add r8,r0,#0x180   r8 = 0x42000180"),
    (0x44, 0xE1D890B8, "E6 : ldrh r9,[r8,#8]    HALF read +0x188 -> want 0x2002"),
    (0x48, 0xE5942008, "     ldr r2,[r4,#8]     r2 = P again"),
    (0x4c, 0xE580218C, "     str r2,[r0,#396]   IRQEnableClear <- P"),
    (0x50, 0xE5907188, "E5 : ldr r7,[r0,#392]   read back -> want Q"),
    (0x54, NOP, "landing pad -- planted, never stepped"),
]


def main():
    pid, fd = pty.fork()
    if pid == 0:
        os.execvp(BIN, [BIN, "-V", "-T", "-E", "cats", "-M", "32",
                        "0x%x:%s" % (CODE, STUB)])
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
        return wait(mark=_mark, echo=x if x else None)

    print("==== E-ROWS on %s (%s)" % (LABEL, BIN))
    status, regs, died_at = "SURVIVED", {}, None
    if not wait(timeout=120):
        print("NO-PROMPT")
        return
    for o in sorted(CONSTS):
        send("put w 0x%08x, 0x%08x" % (DATA + o, CONSTS[o]))
    for o, w, _c in PROG:
        send("put w 0x%08x, 0x%08x" % (CODE + o, w))
    send("pc=0x%08x" % CODE)
    for o, w, c in PROG[:-1]:
        mark = len(buf)
        if not send("step 1", timeout=30) or dead[0]:
            status, died_at = "HOST-DIED", (o, w, c)
            print("  0x%02x 0x%08x  *** HOST DIED HERE ***      | %s" % (o, w, c))
            break
        seg = buf[mark:]
        m = re.search(r"%08x:\s+%08x\s+([^\r\n<]+)" % (CODE + o, w), seg)
        got = re.sub(r"\s+", " ", m.group(1)).strip() if m else "(NO STEP LINE)"
        print("  0x%02x 0x%08x  %-26s | %s" % (o, w, got, c))
    if status == "SURVIVED":
        mark = len(buf)
        if send("reg", timeout=30) and not dead[0]:
            for n in range(16):
                for nm in ([ALIAS[n]] if n in ALIAS else ["r%d" % n]):
                    mm = re.search(r"\b%s\s*=\s*0x([0-9a-fA-F]+)" % nm, buf[mark:])
                    if mm:
                        regs[n] = int(mm.group(1), 16)
        else:
            status = "NO-REG"
    fatals = re.findall(r"(\[[^\r\n\]]*footbridge[^\r\n\]]*\])", buf)
    try:
        os.write(fd, b"quit\n")
        time.sleep(0.3)
        os.close(fd)
    except OSError:
        pass
    try:
        _, st = os.waitpid(pid, 0)
    except Exception:
        st = None
    code = os.WEXITSTATUS(st) if st is not None and os.WIFEXITED(st) else None

    print("  status=%s exit=%s" % (status, code))
    if fatals:
        print("  footbridge diagnostics: %s" % fatals)
    else:
        print("  footbridge diagnostics: NONE")

    def row(tag, reg, want, note):
        got = regs.get(reg)
        g = "-" if got is None else "0x%08x" % got
        print("%-4s %-38s got=%-12s want=0x%08x %s"
              % (tag, note, g, want, "ok" if got == want else "FAIL"))

    print("  --- rows ---")
    row("A1", 6, 0x1011, "device signature VENDOR_ID")
    row("E0", 1, 0x00000000, "read +0x188 before any enable write")
    row("E1", 3, 0x00002002, "read back after IRQEnableSet <- P")
    row("E2", 5, 0x60002002, "read back after Set <- Q  (pins |=)")
    row("E3", 10, 0x00000002, "BYTE read of +0x188 (low byte)")
    row("E6", 9, 0x00002002, "HALFWORD read of +0x188 (low 2 bytes)")
    row("E5", 7, 0x60000000, "read back after IRQEnableClear <- P")
    e4 = not any("ENABLE SET" in f for f in fatals)
    print("%-4s %-38s %-30s %s" % ("E4", "no ENABLE SET diagnostic in this arm",
                                   "fatals=%d" % len(fatals), "ok" if e4 else "FAIL"))
    print("E_PROBE_DONE")


main()
