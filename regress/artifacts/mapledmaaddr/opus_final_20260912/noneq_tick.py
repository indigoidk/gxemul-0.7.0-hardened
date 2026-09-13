#!/usr/bin/env python3
"""Non-equivalence demo: one DMAADDR read stepped exactly as the probe does, then FREE-RUN the guest's `bra .'
self-loop for a few seconds (emulated time advances, device ticks fire), and report what the emulator printed."""
import os, pty, select, sys, time, signal
BIN, KERNEL = sys.argv[1], sys.argv[2]
cmds = ["r1=0xa05f6c04", "r2=0x8c012345", "put h 0x8c001000, 0x2122", "put h 0x8c001002, 0xaffe",
        "put h 0x8c001004, 0x0009", "pc=0x8c001000", "step 1",
        "r1=0xa05f6c04", "r2=0xa5a55a5a", "put h 0x8c001020, 0x6212", "put h 0x8c001022, 0xaffe",
        "put h 0x8c001024, 0x0009", "pc=0x8c001020", "step 1", "print r2"]
pid, fd = pty.fork()
if pid == 0:
    os.execv(BIN, [BIN, "-V", "-x", "-E", "dreamcast", "-M", "64", KERNEL]); os._exit(127)
buf = ""
def rd(t):
    global buf
    end = time.time() + t
    while time.time() < end:
        r, _, _ = select.select([fd], [], [], 0.2)
        if not r: continue
        try: d = os.read(fd, 65536)
        except OSError: return False
        if not d: return False
        buf += d.decode("latin-1", "replace")
    return True
rd(2.5)
for c in cmds:
    os.write(fd, (c + "\n").encode()); rd(0.3)
stepped = buf
os.write(fd, b"continue\n"); rd(4.0)
freerun = buf[len(stepped):]
try: os.kill(pid, signal.SIGKILL)
except OSError: pass
try: os.close(fd)
except OSError: pass
os.waitpid(pid, 0)
key = "DMAADDR was read"
print("binary=%s" % BIN)
print("print r2 value in stepped part: %s" % ("0x8c012345" in stepped))
print("IN_STEPPED(what the probe's sessions cover): %s" % (key in stepped))
print("IN_FREERUN(after `continue', 4 s):           %s" % (key in freerun))
print("freerun bytes=%d  first 400 chars: %r" % (len(freerun), freerun[:400]))
print("NONEQ_DONE")
