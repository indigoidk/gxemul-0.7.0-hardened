#!/usr/bin/env python3
"""NON-EQUIVALENCE CONTROL for the pop-side p_bit / u_bit cell.

Drives  LDMDB r0!, {r1}  -- p_bit=1, u_bit=0 -- which NO row of the 32-row
detector drives.  Decoded from the literal word:
    0xe9300002 = cond 1110 | 100 | P=1 U=0 S=0 W=1 L=1 | Rn=r0 | list=0x0002

  r0 = 0x2000a ; LDMDB decrements first, so the access address is 0x20006.
  fix present : 0x20006 & ~3 = 0x20004 -> bytes[4..7] = 88 77 66 55 -> 0x55667788
  fix absent  : 0x20006 raw          -> bytes[6..9] = 66 55 00 00 -> 0x00005566
  writeback (raw, unmasked) -> r0 = 0x20006 either way.
"""
import os, sys, pty, select, time, re
BIN = sys.argv[1]; LEG = sys.argv[2] if len(sys.argv) > 2 else "?"
STUB = "/tmp/stub_armbdt.bin"
CODE = 0x00008000; PAGE = 0x00020000

class S:
    def __init__(self, b):
        self.pid, self.fd = pty.fork()
        if self.pid == 0:
            os.execvp(b, [b, "-V", "-A", "-T", "-E", "testarm", "-M", "64", "0x%x:%s" % (CODE, STUB)])
            os._exit(127)
        self.buf = ""; self.dead = False; self.wait_prompt(30)
    def rd(self, t=0.2):
        r, _, _ = select.select([self.fd], [], [], t)
        if self.fd not in r: return False
        try: d = os.read(self.fd, 65536)
        except OSError: self.dead = True; return False
        if not d: self.dead = True; return False
        self.buf += d.decode("latin1", "replace"); return True
    def wait_prompt(self, timeout=20):
        t0 = time.time()
        while time.time() - t0 < timeout:
            if self.dead: return False
            self.rd(0.1)
            if self.buf.rstrip().endswith("GXemul>"): return True
        return False
    def send(self, c, timeout=15):
        if self.dead: return ""
        mark = len(self.buf)
        try: os.write(self.fd, (c + "\n").encode("latin1"))
        except OSError: self.dead = True; return ""
        t0 = time.time()
        while time.time() - t0 < timeout:
            self.rd(0.1)
            if len(self.buf) > mark and self.buf[mark:].rstrip().endswith("GXemul>"):
                return self.buf[mark:]
        return ""
    def run(self, words, t=3.0):
        for i, w in enumerate(words): self.send("put w 0x%x, 0x%08x" % (CODE + 4*i, w))
        self.send("pc=0x%x" % CODE)
        try: os.write(self.fd, b"continue\n")
        except OSError: self.dead = True; return
        t0 = time.time()
        while time.time() - t0 < t: self.rd(0.1)
        try: os.write(self.fd, b"\x03")
        except OSError: pass
        self.wait_prompt(5)
    def reg(self, n):
        m = re.search(r"0x([0-9a-fA-F]+)", self.send("print %s" % n)); return int(m.group(1), 16) if m else None
    def close(self):
        try: self.send("quit", timeout=2); os.kill(self.pid, 9); os.waitpid(self.pid, 0)
        except Exception: pass

s = S(BIN)
for i, b in enumerate([0x44,0x33,0x22,0x11,0x88,0x77,0x66,0x55]):
    s.send("put b 0x%x, 0x%02x" % (PAGE + i, b))
#  mov r0,#0x20000 ; add r0,r0,#10 ; ldmdb r0!,{r1} ; b .
s.run([0xe3a00802, 0xe280000a, 0xe9300002, 0xeafffffe])
r1 = s.reg("r1"); r0 = s.reg("r0"); s.close()
w_data = (r1 == 0x55667788); w_wb = (r0 == 0x20006)
print("LEG=%s  ARM_LDM_DB_DATA  r1=%s want 0x55667788 (fix-absent 0x00005566)  %s"
      % (LEG, "None" if r1 is None else "%#010x" % r1, "ok" if w_data else "FAIL"))
print("LEG=%s  ARM_LDM_DB_WB    r0=%s want 0x00020006                         %s"
      % (LEG, "None" if r0 is None else "%#010x" % r0, "ok" if w_wb else "FAIL"))
print("LDMDB_CONTROL_DONE")
