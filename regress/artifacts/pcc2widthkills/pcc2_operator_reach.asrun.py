#!/usr/bin/env python3
"""pcc2widthkills -- does the DEBUGGER reach the odd-offset width kills?

The Fable seat claims `put h <odd addr>, 0' prints "WARNING: address isn't aligned" and
then STORES anyway, straight through memory_rw to the device handler -- so the seven
odd-offset arms the m88k alignment check makes GUEST-unreachable are OPERATOR-reachable,
and therefore have an executable detector row.  The codex seat says the fork's precedent
forbids fixing an unreachable guard WITHOUT an executable row.  If this probe ends the
host, both seats are satisfied: the row exists, fix all twelve.

Three sessions on the committed build:
    odd_h   put h 0xfff42003 (VECBASE, odd)  -> prediction: exit1 (the kill), or the
            debugger refuses and the host lives.
    even_h  put h 0xfff42002 (GENCTL, even)  -> exit1 on the pre-fix build (control: the
            debugger path reaches the handler at all).
    ram_h   put h 0x00020002 (RAM)           -> lives (control: put h works).
Sentinel: PCC2_OPREACH_DONE
"""
import os, pty, select, sys, time
BIN = sys.argv[1]
open("/tmp/pcc2_dummy.bin", "wb").write(b"\x00" * 4)

def session(cmds, settle=1.5, spin=1.0):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "mvme88k", "-e", "mvme187", "-M", "64", "0x10000:/tmp/pcc2_dummy.bin"])
        os._exit(127)
    buf = b""
    def rd(t):
        nonlocal buf
        end = time.time() + t
        while time.time() < end:
            r, _, _ = select.select([fd], [], [], 0.1)
            if r:
                try:
                    d = os.read(fd, 65536)
                    if not d: return False
                    buf += d
                except OSError:
                    return False
        return True
    rd(settle)
    for c in cmds:
        try: os.write(fd, (c + "\n").encode())
        except OSError: break
        if not rd(spin): break
    try: os.write(fd, b"quit\n"); rd(0.4)
    except OSError: pass
    try: os.close(fd)
    except OSError: pass
    _, st = os.waitpid(pid, 0)
    how = "exit%d" % os.WEXITSTATUS(st) if os.WIFEXITED(st) else "sig%d" % os.WTERMSIG(st)
    return buf.decode("latin-1", "replace").replace("\r", ""), how

for name, addr in (("ram_h", 0x00020002), ("even_h", 0xfff42002), ("odd_h", 0xfff42003)):
    t, how = session(["put h 0x%x, 0x1234" % addr])
    warned = "isn't aligned" in t
    killed = "non-byte reads and writes" in t
    print("%-8s how=%-6s aligned-warning=%-5s width-kill-message=%-5s" % (name, how, warned, killed))
print("PCC2_OPREACH_DONE")
