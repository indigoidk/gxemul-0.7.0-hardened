#!/usr/bin/env python3
"""unasm.py <gxemul> <out> -- disassemble OpenBSD 7.6 landisk's own wdc_obio code
with GXemul's SH4 disassembler (symbols come from the kernel's ELF symtab).
No guest instruction is executed: `-V` stops before the first one."""
import os, pty, select, sys, time
BIN, OUT = sys.argv[1], sys.argv[2]
IMG = "/mnt/c/DocumentNoSnc/CC/GXEMUL/_images"
argv = [BIN, "-V", "-E", "landisk", "-M", "64", "-d", "iR:%s/wdc-scratch-64m.img" % IMG,
        "%s/openbsd76-landisk-bsd.rd" % IMG]
cmds = ["unassemble 0x8c1600e0 0x8c160124",     # wdc_obio_write_reg (64 bytes)
        "unassemble 0x8c160080 0x8c1600c4",     # wdc_obio_read_reg (66 bytes)
        "unassemble 0x8c160120 0x8c160256",     # wdc_obio_attach (308 bytes)
        "dump 0x8c160120 0x8c160280",           # its literal pool
        "dump 0x8c160080 0x8c160120",
        "unassemble 0x8c15f6e0 0x8c15f6f0"]     # obio_iomem_write_1 (census pc +0x8)
pid, fd = pty.fork()
if pid == 0:
    os.execv(BIN, argv); os._exit(127)
buf = b""
def rd(t):
    global buf
    end = time.time() + t
    while time.time() < end:
        r, _, _ = select.select([fd], [], [], 0.25)
        if r:
            try:
                d = os.read(fd, 65536)
            except OSError:
                return
            if not d:
                return
            buf += d
rd(6.0)
for c in cmds:
    os.write(fd, (c + "\n").encode()); rd(2.0)
os.write(fd, b"quit\n"); rd(1.0)
try:
    os.close(fd); os.waitpid(pid, 0)
except OSError:
    pass
open(OUT, "wb").write(buf)
print("UNASM_DONE bytes=%d" % len(buf))
