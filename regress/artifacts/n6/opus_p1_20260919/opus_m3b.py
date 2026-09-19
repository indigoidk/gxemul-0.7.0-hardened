#!/usr/bin/env python3
"""M3b: re-run the width arm and dump the RAW `reg` text, because the emulator
prints r10 as `sl` (and r11/r12/r13/r14 as fp/ip/sp/lr), so an r<N>= regex
silently misses them -- the pattern-that-selected-nothing class.
Also adds byte reads at +0x189/+0x18a-equivalent offsets and a halfword at +0x301.
usage: opus_m3b.py <gxemul> <stub>
"""
import os, pty, re, select, sys, time

BIN, STUB = sys.argv[1], sys.argv[2]
CODE, DATA, NOP = 0x00008000, 0x00009000, 0xE1A00000
CONSTS = {0x10: 0x00ABCDEF}

PROG = [
    (0x00, 0xEE110F10, "read CP15 c1"),
    (0x04, 0xE3C00001, "clear MMU enable bit"),
    (0x08, 0xEE010F10, "MMU OFF"),
    (0x0c, 0xEE113F10, "read CP15 c1 back -> r3 (overwritten later)"),
    (0x10, 0xE3A00442, "r0 = 0x42000000"),
    (0x14, 0xE3A04A09, "r4 = 0x9000"),
    (0x18, 0xE5906000, "A1 devsig ldr r6,[r0] VENDOR_ID"),
    (0x1c, 0xE5942010, "ldr r2,[r4,#16] r2 = 0x00ABCDEF"),
    (0x20, 0xE5802300, "str r2,[r0,#768] TIMER_1_LOAD <- 0x00ABCDEF"),
    (0x24, 0xE2808C03, "add r8,r0,#0x300"),
    (0x28, 0xE1D8A0B2, "ldrh r10,[r8,#2]  HALF read +0x302 -> r10 (sl)"),
    (0x2c, 0xE1D8B0B0, "ldrh r11,[r8]     HALF read +0x300 -> r11 (fp)"),
    (0x30, 0xE5D0C300, "ldrb r12,[r0,#768] BYTE read +0x300 -> r12 (ip)"),
    (0x34, 0xE5901300, "ldr r1,[r0,#768]  WORD read +0x300 -> r1"),
    (0x38, NOP, "landing pad"),
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
            print("HOST DIED at 0x%02x 0x%08x %s" % (o, w, c))
            break
        seg = buf[mark:]
        m = re.search(r"%08x:\s+%08x\s+([^\r\n<]+)" % (CODE + o, w), seg)
        got = re.sub(r"\s+", " ", m.group(1)).strip() if m else "(NO STEP LINE)"
        print("  0x%02x 0x%08x  %-26s | %s" % (o, w, got, c))
    mark = len(buf)
    send("reg", timeout=30)
    print("---- RAW `reg` OUTPUT ----")
    print(buf[mark:].replace("\r", ""))
    print("---- footbridge diagnostics ----")
    for f in re.findall(r"(\[[^\r\n\]]*footbridge[^\r\n\]]*\])", buf):
        print("  " + f)
    try:
        os.write(fd, b"quit\n")
        time.sleep(0.3)
        os.close(fd)
    except OSError:
        pass
    try:
        os.waitpid(pid, 0)
    except Exception:
        pass
    print("M3B_DONE")


main()
