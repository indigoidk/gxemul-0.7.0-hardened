#!/usr/bin/env python3
"""WITNESS ATTEMPT -- lcairqstubkill.

Does an ordinary UART interrupt assertion reach lca_interrupt_assert() and terminate
the host, on the COMMITTED binary and an UNMODIFIED in-tree machine description?

Harness shape copied from regress/lca_confbus_probe.py (pty.fork + `-V -x`, dummy image
loaded at 0x20000000:).  No machine or device is added: bus_isa_init() installs the
ns16550 on ISA IRQ 4 unconditionally, which is the point.
"""
import os, pty, re, select, sys, time

BIN   = sys.argv[1] if len(sys.argv) > 1 else "./build/gxemul"
LABEL = sys.argv[2] if len(sys.argv) > 2 else "HEAD"
MACH  = "alphabook1"
K0SEG = 0xfffffc0000000000
def k0(p): return K0SEG | p

LCA_ISA_BASE = 0x1c0000000 + 0x10000000      # LCA_PCI_SIO + 0x10000000, dev_lca.c:47
UART         = LCA_ISA_BASE + 0x3f8          # bus_isa.c:250, isa_portbase + 0x3f8
IER, MCR, THR = UART + 1, UART + 4, UART + 0

DUMMY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alpha_dummy.bin")
if not os.path.exists(DUMMY):
    with open(DUMMY, "wb") as f:
        f.write(b"\0" * 8)

def session(cmds, settle=1.6, spin=2.5):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "alpha", "-e", MACH, "-M", "64",
                       "0x20000000:" + DUMMY])
        os._exit(127)
    buf = ""
    def rd(t):
        nonlocal buf
        end = time.time() + t
        while time.time() < end:
            r, _, _ = select.select([fd], [], [], 0.1)
            if not r:
                continue
            try:
                d = os.read(fd, 65536)
                if not d:
                    return False
                buf += d.decode("latin-1", "replace")
            except OSError:
                return False
        return True
    alive = rd(settle)
    for i, c in enumerate(cmds):
        try:
            os.write(fd, (c + "\n").encode("latin-1"))
        except OSError:
            alive = False; break
        if not rd(spin if i == len(cmds) - 1 else 0.35):
            alive = False; break
    try:
        os.write(fd, b"quit\n"); rd(0.4)
    except OSError:
        pass
    try:
        os.close(fd)
    except OSError:
        pass
    return buf.replace("\r", ""), alive

print("lcairq_probe -- binary=%s label=%s machine=%s" % (BIN, LABEL, MACH))
print("%-16s %-10s %-10s %s" % ("row", "got", "want", "note"))
def row(n, got, want, note):
    print("%-16s %-10s %-10s %-58s %s" % (n, got, want, note,
                                          "ok" if got == want else "*** FAIL ***"))

#  CONTROL 1 -- liveness: the session runs and the debugger answers at all.
t, alive = session(["step 50"])
row("live", "alive" if alive else "died", "alive",
    "CONTROL: plain step on an unmodified machine, no UART setup")

#  CONTROL 2 -- device signature: the UART answers, and RAM would not.
t2, alive2 = session(["dump 0x%x 0x%x" % (k0(UART), k0(UART) + 8)])
row("devsig", "alive" if alive2 else "died", "alive",
    "CONTROL: the UART window is readable through the same decode")

#  The 8-byte dummy is all zeros, which decodes as `call_pal PAL_halt' and STOPS THE MACHINE
#  before any device tick can fire -- measured, and it is why the first attempt read `alive'.
#  Plant a self-branch so the guest free-runs and DEVICE_TICK(ns16550) is reached.
#     br r31, -1  ==  (0x30 << 26) | (31 << 21) | 0x1fffff  ==  0xc3ffffff
#     target = PC + 4 + disp*4 = PC, i.e. a one-instruction infinite loop.
ENTRY   = 0x20000000
SELFBR  = 0xc3ffffff

#  CONTROL 3 -- the self-branch alone must NOT terminate: it separates "the loop kills it"
#  from "the interrupt kills it".
t3a, alive3a = session(["put w 0x%x, 0x%x" % (ENTRY, SELFBR), "continue"], spin=4.0)
row("spin only", "alive" if alive3a else "died", "alive",
    "CONTROL: free-running self-branch with NO UART setup must survive")

#  THE WITNESS -- enable transmit-empty interrupts, set OUT2, prime IIR_TXRDY, free-run.
seq = ["put w 0x%x, 0x%x" % (ENTRY, SELFBR),
       "put b 0x%x, 0x02" % k0(IER),     # IER_ETXRDY
       "put b 0x%x, 0x08" % k0(MCR),     # MCR_IENABLE (OUT2)
       "put b 0x%x, 0x41" % k0(THR),     # write to THR -> sets IIR_TXRDY
       "continue"]
t3, alive3 = session(seq, spin=4.0)
hit = "lca_interrupt_assert" in t3
row("irq assert", "died" if not alive3 else "alive", "died",
    "WITNESS: UART asserts ISA IRQ 4 -> isa_interrupt_common -> lca_interrupt_assert")
row("stub named", "yes" if hit else "no", "yes",
    "the TODO diagnostic names the stub it died in")

open("/tmp/lcairq_last.txt", "w").write(t3)
print("\n--- last 700 chars of the witness session ---")
print(t3[-700:])
print("\nLCAIRQ_PROBE_DONE")
