#!/usr/bin/env python3
"""Q4: is there a failability control that does NOT depend on the footbridge
ending the process?  The probes already pass -T ("halt on non-existent memory
access").  Measure what a guest read of unmapped physical space actually does.
usage: opus_q4.py <gxemul> <stub>
"""
import os, pty, re, select, sys, time

BIN, STUB = sys.argv[1], sys.argv[2]
CODE, NOP = 0x00008000, 0xE1A00000

ARMS = {
  "Q4a unmapped PA 0x90000000 read": [
      (0x20, 0xE3A00209, "mov r0,#0x90000000"),
      (0x24, 0xE5907000, "ldr r7,[r0]   -- unmapped physical space"),
      (0x28, NOP, "reached only if it survives")],
  "Q4b unmapped PA 0x70000000 read": [
      (0x20, 0xE3A0020E, "mov r0,#0xe0000000 (see disasm)"),
      (0x24, 0xE5907000, "ldr r7,[r0]   -- unmapped physical space"),
      (0x28, NOP, "reached only if it survives")],
  "Q4c control: RAM read at 0x9000": [
      (0x20, 0xE3A00A09, "mov r0,#0x9000"),
      (0x24, 0xE5907000, "ldr r7,[r0]   -- real RAM"),
      (0x28, NOP, "")],
}
PRE = [(0x00, 0xEE110F10, "read CP15 c1"),
       (0x04, 0xE3C00001, "clear MMU enable bit"),
       (0x08, 0xEE010F10, "MMU OFF -> VA == PA"),
       (0x0c, NOP, ""), (0x10, NOP, ""), (0x14, NOP, ""),
       (0x18, NOP, ""), (0x1c, NOP, "")]


def run(label, body):
    prog = PRE + body
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

    status, r7, dis = "SURVIVED", None, []
    if not wait(timeout=120):
        status = "NO-PROMPT"
    else:
        for o, w, _c in prog:
            send("put w 0x%08x, 0x%08x" % (CODE + o, w))
        send("pc=0x%08x" % CODE)
        for o, w, c in prog[:-1]:
            mark = len(buf)
            if not send("step 1", timeout=30) or dead[0]:
                status = "HOST-DIED"
                dis.append("0x%02x 0x%08x *** DIED HERE *** %s" % (o, w, c))
                break
            seg = buf[mark:]
            m = re.search(r"%08x:\s+%08x\s+([^\r\n<]+)" % (CODE + o, w), seg)
            got = re.sub(r"\s+", " ", m.group(1)).strip() if m else "(NO STEP LINE)"
            if c:
                dis.append("0x%02x 0x%08x %-24s | %s" % (o, w, got, c))
        if status == "SURVIVED":
            mark = len(buf)
            if send("reg", timeout=30) and not dead[0]:
                mm = re.search(r"\br7\s*=\s*0x([0-9a-fA-F]+)", buf[mark:])
                if mm:
                    r7 = int(mm.group(1), 16)
            else:
                status = "HOST-DIED" if dead[0] else "NO-REG"
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
    sig = os.WTERMSIG(st) if st is not None and os.WIFSIGNALED(st) else None
    print("---- %s" % label)
    for d in dis:
        print("     " + d)
    print("     status=%s exit=%s signal=%s r7=%s"
          % (status, code, sig, "-" if r7 is None else "0x%08x" % r7))
    #  Anything the emulator said that mentions a warning / non-existent memory:
    for m in set(re.findall(r"(\[[^\r\n\]]{0,90}\])", buf)):
        if "footbridge" in m or "non-exist" in m.lower() or "warning" in m.lower():
            print("     said: " + m)
    sys.stdout.flush()


for k in sorted(ARMS):
    run(k, ARMS[k])
print("Q4_DONE")
