#!/usr/bin/env python3
"""jazz_vector_witness.py <gxemul-binary> [kernel] -- rung-3 witness for OB-22 (`jazzvecdeassert`, round #578).

Defect (GXEMUL-SEC/src/devices/dev_jazz.c, DEVICE_ACCESS(jazz_jazzio), HEAD 3cb8bdc1 :696-697): EVERY access to the
pica_jazzio register (physical 0xf0000000; offset 0 is the R4030 interrupt-source vector) ends with an unconditional
`INTERRUPT_DEASSERT(d->mips_irq_3)` ("This is needed by Windows NT during startup").  With a second JAZZ line still
pending, the vector read for the first drops the CPU's IRQ3 while a level interrupt is outstanding; nothing re-asserts
it until some line is asserted anew (the "self-healing" the old OB-22 entry describes).

Vehicle: the UNMODIFIED in-tree arc/pica machine (-e pica), the rig kernel loaded for construction only, the cold
debugger (-V).  Every device access is a genuine guest instruction through XKPHYS (the gxprobe stubs: sb / lbu / sw / lw),
never a debugger `put`; the CPU-side observable is COP0 Cause's IP3 bit (mips_irq_3 is line 1 << (STATUS_IM_SHIFT + 3)
= 0x800, cpu_mips.c), read with the debugger's `print cause`.  Interrupts are never DELIVERED here (the cold CPU has
Status.IE clear and the debugger suppresses exception dispatch while stepping); Cause.IP reflects the asserted lines
regardless, which is exactly the observable under test.

Two JAZZ lines are driven from two real devices wired by machine_arc.c for pica: the ns16550 at 0x80006000 (jazz.8) and
the ns16550 at 0x80007000 (jazz.9).  A UART asserts its line SYNCHRONOUSLY inside the guest's IER store (dev_ns16550.c:
the IER write sets IIR_TXRDY and calls dev_ns16550_tick, which asserts when MCR.IENABLE is set), so the whole witness
runs under single-step.  The R4030 EXT_IMASK register (jazz + 0xe8) must carry R4030_EXT_IP3 (0x02) or the Jazz device
never asserts the CPU line at all.

Rows (want on the FIXED build; HEAD's reading in brackets):
  jz imask       EXT_IMASK reads back 0x2 after the guest store          -- liveness + device signature of the R4030 register
  jz com0 ier    com0 IER reads back 0x2                                  -- device signature of the UART
  jz ip one      Cause.IP3 set after com0's IER write                     -- liveness of the interrupt path to the CPU
  jz ip both     Cause.IP3 set after com1's IER write too
  jz vec         the vector register reads 0x24 = (8 + 1) << 2            -- device signature of jazzio: RAM cannot answer this
  jz ip after    Cause.IP3 STILL set after the vector read  [HEAD: CLEAR -- THE DEFECT: com0 and com1 are both still pending]
  jz vec again   a second vector read still 0x24 (the read does not clear a line)
  jz vec com1    after com0's IER is cleared, the vector names line 9: 0x28
  jz ip com1     Cause.IP3 set with com1 alone pending  [HEAD: CLEAR -- nothing re-asserted it]
  jz ip reheal   re-enabling com0's IER re-asserts IP3 on both builds     -- the self-healing mechanism, a control
  jz ip none     both IERs cleared: IP3 clear on both builds              -- the deassert path works when nothing is pending
  jz vec none    vector reads 0 with nothing pending
  jz ip nt       Cause.IP3 clear after a vector read with nothing pending -- the Windows NT case the old comment names: unchanged
Names stay at 13 characters or fewer (%-14s column; the gate anchors `^name  .*ok$` with two spaces).
Ends with JAZZVEC_RESULT=n/N and the sentinel JAZZVEC_DONE.
"""
import os
import sys
import time

sys.path.insert(0, "/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad")
import gxprobe  # noqa: E402

BIN = sys.argv[1]
KERNEL = sys.argv[2] if len(sys.argv) > 2 else "/mnt/c/DocumentNoSnc/CC/GXEMUL/gxemul_arc_rig/bsd"
XK = 0x9000000000000000
JAZZ = XK | 0x80000000
EXT_IMASK = JAZZ + 0xe8          # R4030_SYS_EXT_IMASK (pica.h: R4030 + 0x00e8)
COM0 = XK | 0x80006000           # ns16550 at jazz.8
COM1 = XK | 0x80007000           # ns16550 at jazz.9
VEC = XK | 0xf0000000            # pica_jazzio, offset 0: the interrupt-source vector
IER, MCR = 1, 4                  # ns16550 register offsets (addrmult 1)
IP3 = 0x800                      # mips_irq_3 in COP0 Cause
R4030_EXT_IP3 = 0x02

rows = []


def row(name, got, want):
    ok = (got == want)
    rows.append(ok)
    g = "None" if got is None else "0x%x" % got
    print("%-14s %-24s %-24s %s" % (name, g, "0x%x" % want, "ok" if ok else "FAIL"), flush=True)


def ip3(emu):
    c = emu.read_reg("cause")
    return None if c is None else (c & IP3)


log = os.environ.get("JAZZVEC_LOG") or ("/tmp/jazzvec_%d.log" % os.getpid())
emu = gxprobe.Emu(BIN, ["-V", "-e", "pica", KERNEL], log_path=log, preset=gxprobe.MACHINES["arc"], boot_wait=4.0)
print("JAZZVEC binary=%s log=%s" % (BIN, log), flush=True)

emu.guest_store32(EXT_IMASK, R4030_EXT_IP3)
row("jz imask", emu.guest_load32(EXT_IMASK), R4030_EXT_IP3)

emu.guest_store8(COM0 + MCR, 0x08)          # MCR.IENABLE (OUT2): the UART may drive its line
emu.guest_store8(COM0 + IER, 0x02)          # IER.ETXRDY: THR empty -> the line asserts inside this store
row("jz com0 ier", emu.guest_load8(COM0 + IER), 0x02)
row("jz ip one", ip3(emu), IP3)

emu.guest_store8(COM1 + MCR, 0x08)
emu.guest_store8(COM1 + IER, 0x02)
row("jz ip both", ip3(emu), IP3)

row("jz vec", emu.guest_load32(VEC), (8 + 1) << 2)
row("jz ip after", ip3(emu), IP3)
row("jz vec again", emu.guest_load32(VEC), (8 + 1) << 2)

emu.guest_store8(COM0 + IER, 0x00)          # com0 serviced: its line deasserts; com1 still pending
row("jz vec com1", emu.guest_load32(VEC), (9 + 1) << 2)
row("jz ip com1", ip3(emu), IP3)

emu.guest_store8(COM0 + IER, 0x02)          # a fresh assert re-raises IRQ3 on both builds: the self-heal
row("jz ip reheal", ip3(emu), IP3)

emu.guest_store8(COM0 + IER, 0x00)
emu.guest_store8(COM1 + IER, 0x00)          # nothing pending
row("jz ip none", ip3(emu), 0)
row("jz vec none", emu.guest_load32(VEC), 0)
row("jz ip nt", ip3(emu), 0)

emu.close()
print("JAZZVEC_RESULT=%d/%d" % (sum(1 for r in rows if r), len(rows)), flush=True)
print("JAZZVEC_DONE", flush=True)
