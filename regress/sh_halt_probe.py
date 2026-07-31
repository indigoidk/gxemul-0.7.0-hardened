#!/usr/bin/env python3
"""Gate 10's second instrument: legal SuperH encodings must not stop the emulator.

Prints one line per row:  <name> <got> <want> ok|FAIL
then SH_HALT_CONTROL=OK|DEAD and SH_HALT_RESULT=<passed>/<total>.
gate_sh_rounding.sh does the asserting.

What this protects
------------------
#314. The SH decoder answered an encoding it does not implement with `goto bad`,
which reaches the shared label in cpu_dyntrans.c and sets cpu->running = 0 -- a
legal instruction stopping the whole emulator. It now decodes to instr(reserved),
which raises the general illegal-instruction exception at EXECUTE time. Execute
time is load-bearing: readahead translates instructions that may never run, so
raising from the decoder would corrupt state for a guest that never executed the
word.

Measured on the committed build, all eight of the rows below stopped the
emulator. Three of them -- MAC.L, MAC.W and TST.B -- are BASE ISA, present since
SH-1/SH-2 and unambiguously legal on the SH7751R this rig models, so this is not
a question about accepting SH-4A extensions on an SH-4 core.

How the outcome is classified, and why that took three tries
-----------------------------------------------------------
A halt is read off the dyntrans "UNIMPLEMENTED instruction" message, NOT off a
memory marker. The first version of this sweep decided the outcome purely by
whether a store after the test instruction had run, which conflates three
different things:

  * the emulator stopped                          <- the defect
  * the exception was raised, so the store was    <- the FIX working
    never reached
  * the instruction ran and simply did not reach  <- e.g. SLEEP, which is
    the store                                        implemented and sleeps

That marker-only classifier reported SLEEP as a halt, which is false -- SLEEP has
a case and a handler -- and, after the fix landed, reported every repaired row as
still broken. Naming each outcome separately is what made the measurement mean
anything.

Row meaning: got is the observed outcome, want is "alive". A row can fail in
both directions -- it caught a real defect on the committed build, and it would
catch a regression that reintroduced the halt.
"""
import os
import pty
import re
import select
import sys
import time

BIN = sys.argv[1]
KERNEL = sys.argv[2]

CODE = 0x8c010000
DEST = 0x8c010100

#  mov #0x5a,r0 ; <test> ; mov.l r0,@r1   -- r1 = DEST
MOV_R0_5A = 0xe05a
MOV_L_R0_AT_R1 = 0x2102

ROWS = [
    (0x0009, "nop control",   "base"),
    (0x000f, "MAC.L",         "base ISA"),
    (0x400f, "MAC.W",         "base ISA"),
    (0xcc01, "TST.B",         "base ISA"),
    (0x003a, "STC SGR",       "SH-4 privileged"),
    (0x40f2, "STC.L DBR",     "SH-4 privileged"),
    (0x0063, "MOVLI.L",       "SH-4A"),
    (0x00ab, "SYNCO",         "SH-4A"),
    (0x00d3, "PREFI",         "SH-4A"),
]


def run(iw):
    """Return "alive", "HALTED", or None if the session never came up."""
    pid, fd = pty.fork()
    if pid == 0:
        os.execvp(BIN, [BIN, "-V", "-E", "landisk", "-M", "64", KERNEL])
        os._exit(127)
    buf = ""

    def rd(t=0.4):
        nonlocal buf
        r, _, _ = select.select([fd], [], [], t)
        if fd not in r:
            return True
        try:
            d = os.read(fd, 65536)
        except OSError:
            return False
        if not d:
            return False
        buf += d.decode("latin1", "replace")
        return True

    def wait(timeout=60):
        t = time.time()
        while time.time() - t < timeout:
            if not rd():
                return False
            if buf.rstrip().endswith(">"):
                return True
        return False

    def send(s):
        b = (s + "\n").encode("latin1")
        n = 0
        while n < len(b):
            n += os.write(fd, b[n:])
        wait()

    if not wait(90):
        try:
            os.kill(pid, 9)
            os.waitpid(pid, 0)
        except Exception:
            pass
        return None

    for c in ["r0=0x%x" % DEST, "r1=0x%x" % DEST,
              "put w 0x%x, 0xdeadbeef" % DEST,
              "put h 0x%x, 0x%04x" % (CODE, MOV_R0_5A),
              "put h 0x%x, 0x%04x" % (CODE + 2, iw),
              "put h 0x%x, 0x%04x" % (CODE + 4, MOV_L_R0_AT_R1),
              "pc=0x%x" % CODE, "step 3"]:
        send(c)

    halted = "UNIMPLEMENTED instruction" in buf

    #  Prove the session is still answering, so "not halted" cannot be read off
    #  a dead pty. A dump that returns nothing is reported as its own outcome
    #  rather than silently scoring as alive.
    responded = False
    for _ in range(3):
        mark = len(buf)
        send("dump 0x%x 0x%x" % (DEST, DEST + 4))
        if re.search(r"0x0*[0-9a-f]+\s+[0-9a-f]{8}", buf[mark:]):
            responded = True
            break
        time.sleep(1.0)
        rd(1.0)
    try:
        os.write(fd, b"quit\n")
        time.sleep(0.3)
        os.kill(pid, 9)
        os.waitpid(pid, 0)
    except Exception:
        pass

    if halted:
        return "HALTED"
    return "alive" if responded else "unresponsive"


rows = []
control = run(0x0009)
print("SH_HALT_CONTROL=%s" % ("OK" if control == "alive" else "DEAD"))
if control != "alive":
    print("SH_HALT_RESULT=0/0")
    sys.exit(0)

for iw, name, cls in ROWS:
    got = run(iw)
    ok = (got == "alive")
    rows.append(ok)
    print("%-14s %-14s %-8s %-16s %s"
          % (name, got if got else "dead", "alive", cls, "ok" if ok else "FAIL"))

print("SH_HALT_RESULT=%d/%d" % (sum(1 for r in rows if r), len(rows)))
