"""wdcringambig -- RUNG-3 WITNESS.  Real guest instructions, real address decode, real
memory_rw, on an UNMODIFIED in-tree machine description (`evbmips -e malta`).

THE MACHINE IS NOT MODIFIED AND NO DEVICE IS ADDED.  malta carries a wdc through its own
committed path: machine_evbmips.c:100 `bus_pci_add(..., "piix4_ide")` -> bus_pci.c:868-874,
which does `device_add(machine, "wdc addr=<isa_portbase+0x1f0> ...")` whenever an IDE image
is attached.  isa_portbase = 0x18000000 (dev_gt.c:259).  Attaching a disk image is ordinary
operation, not a machine edit -- the `#if 0` wdc in machine_arc.c:232-236 is NOT used, and
landisk (machine_landisk.c:87-90) is the only other in-tree carrier.

    wdc data port    physical 0x180001f0  ->  KSEG1 0xffffffffb80001f0
    wdc status reg   physical 0x180001f7  ->  KSEG1 0xffffffffb80001f7   (+7)

WHY FREE-RUNNING AND NOT `step`:  dev_wdc.c:1653 sets `d->data_debug = 1`, so every
data-port access calls debug().  debugmsg.c:365-381 -- debug() adds 1 to `verbose` when
single_step is set and subtracts 1 when emul_executing -- so a STEPPED run prints a line
per access (262k lines) while a FREE-RUNNING run at default verbosity has v == -1 and
prints nothing.  The probe therefore breakpoints and continues.  MEASURED: 1.53 s for
262666 device accesses, about 172k/second.

THE RING (dev_wdc.c:47-48, :182-201, :209-232):
    WDC_INBUF_SIZE = 512*(512+1) = 262656.  wdc_addtoinbuf() advances head modulo the
    size with NO capacity check, so head == tail encodes BOTH empty and full.

THE STATUS ORACLE, AND ITS PROVENANCE.  An earlier draft of this probe predicted 0x58/0x50
and measured 0x59/0x51.  The extra bit is WDCS_ERR (0x01, wdcreg.h:85), and it is correct:
DEVINIT sets `d->error = 1` at dev_wdc.c:1655 and only wdc_command() clears it
(dev_wdc.c:668).  This probe issues NO command, so the power-on error bit stands the whole
run.  status_byte() (dev_wdc.c:462-478) ORs:
        WDCS_DRDY|WDCS_DSC   0x50   because diskimage_exist() is true for the IDE image
        WDCS_ERR             0x01   because d->error is still its power-on 1
        WDCS_DRQ             0x08   iff  d->inbuf_head != d->inbuf_tail
so 0x59 with the ring non-empty and 0x51 with head == tail.  The oracle was re-pinned from
those lines, not from the measurement; the bit that carries the CLAIM is DRQ alone.

WHAT THE GUEST DOES -- every observation below is a guest load:

    A  RAM LIVENESS      sb/lbu 0x55 to plain RAM through the same instruction shapes.
    B  DEVICE SIGNATURE  push 0x5a then 0xa5, read the SAME address twice.
                         A FIFO returns 5a,a5.  RAM returns a5,a5.
    C  LIVENESS          one byte staged -> status must show DRQ SET.
    D  LIVENESS at the boundary   fill to SIZE-1 -> DRQ still SET.
    E  *** DEFECT ***    one more push -> occupancy reads 0, DRQ CLEAR, while 262656
                         staged bytes sit in the buffer.
    F  *** DEFECT ***    a data read now returns 0xff (wdc_get_inbuf's -1) and the tail
                         does not advance -- the staged bytes are unreachable.
    G  *** DEFECT ***    one more push overwrites the OLDEST UNREAD byte.  The guest
                         reads back 0x44 where FIFO order demands the 0x11 staged at C.

Ring trace, SHIPPED (derived by hand, then confirmed by the measured bytes):
    B: push 5a -> [0], push a5 -> [1]; two reads take tail to 2.  head=2 tail=2.
    C: push 11 -> [2].  head=3 tail=2, occupancy 1.
    D: push 262654 x 0x22.  head = 3+262654 = 262657 % 262656 = 1.  tail=2.
       occupancy = (1-2) % 262656 = 262655 = SIZE-1.  head != tail -> DRQ SET.
    E: push 33 -> [1].  head=2 == tail=2.  occupancy reads 0.  DRQ CLEAR.
       Nothing is destroyed yet -- [1] held an already-consumed byte.  This isolates the
       AMBIGUITY from the CORRUPTION, which the queue entry conflates.
    F: read -> c = inbuf[2] = 0x11, but head==tail so it returns -1 and DOES NOT advance.
    G: push 44 -> [2], DESTROYING the 0x11.  head=3, occupancy 1, DRQ back.
       read -> 0x44.  The oldest byte is gone and nothing said so.

Ring trace, FIXED LEG (a capacity check reserving one slot; NOT a proposed shipped fix,
it exists only to prove this probe CAN go green):
    D: all 262654 pushes still fit -- capacity is SIZE-1 and occupancy was 1.
    E: push 33 REFUSED, head stays 1, occupancy stays 262655 -> DRQ still SET  (0x51 -> 0x59)
    F: read -> the real oldest byte 0x11                                       (0xff -> 0x11)
    G: push 44 fits (one slot freed by F); read -> 0x22, the next bulk byte in
       FIFO order, because the 0x11 was delivered rather than destroyed         (0x44 -> 0x22)

NOTHING IN THE REPO IS WRITTEN.  Both trees under measurement are copies under /tmp.
"""
import os
import pty
import re
import select
import sys
import time

SHIPPED_BIN = "/tmp/gxwit/gxemul"     # source-identical to GXEMUL-SEC at HEAD
FIXED_BIN   = "/tmp/gxfix/gxemul"     # + a capacity check in wdc_addtoinbuf()
DISK   = "/tmp/wdcscratch.img"
BASE   = 0xffffffff80100000           # KSEG0, physical 0x00100000, inside malta's 128 MB
RAWBIN = "/tmp/gxwit_probe/wdcring.bin"
LOGDIR = "/tmp/gxwit_probe"

DATA_HI, DATA_LO = 0xb800, 0x01f0     # wdc data port, KSEG1
STATUS_OFF = 7                        # wd_command reads back status_byte()
RAM_HI = 0x8020                       # KSEG0 scratch for the RAM liveness control

INBUF_SIZE = 512 * (512 + 1)          # 262656
BULK = 262654                         # pushes needed to reach occupancy SIZE-1

DRDY, DSC, DRQ, ERR = 0x40, 0x10, 0x08, 0x01
ST_DRQ   = DRDY | DSC | ERR | DRQ     # 0x59  ring non-empty
ST_NODRQ = DRDY | DSC | ERR           # 0x51  head == tail

zero, t0, t1, t2, t3, t4 = 0, 8, 9, 10, 11, 12
s0, s1, s2, s3, s4, s5, s6, s7 = 16, 17, 18, 19, 20, 21, 22, 23
t8, t9 = 24, 25


def R(op, rs, rt, rd, sa, fn):
    return (op << 26) | (rs << 21) | (rt << 16) | (rd << 11) | (sa << 6) | fn


def I(op, rs, rt, imm):
    return (op << 26) | (rs << 21) | (rt << 16) | (imm & 0xffff)


def lui(rt, imm):       return I(0x0F, 0, rt, imm)
def ori(rt, rs, imm):   return I(0x0D, rs, rt, imm)
def addiu(rt, rs, imm): return I(0x09, rs, rt, imm)
def sb(rt, off, base):  return I(0x28, base, rt, off)
def lbu(rt, off, base): return I(0x24, base, rt, off)
def bne(rs, rt, off):   return I(0x05, rs, rt, off)
def beq(rs, rt, off):   return I(0x04, rs, rt, off)
def or_(rd, rs, rt):    return R(0, rs, rt, rd, 0, 0x25)


NOP = 0
prog = []


def emit(word, want_mnemonic):
    """want_mnemonic is checked against the EMULATOR'S OWN disassembly."""
    prog.append((word, want_mnemonic))


emit(lui(t0, DATA_HI),        "lui t0,0xb800")
emit(ori(t0, t0, DATA_LO),    "ori t0,t0,0x01f0")
emit(lui(t4, RAM_HI),         "lui t4,0x8020")

emit(addiu(t3, zero, 0x55),   "addiu t3,zr,85")
emit(sb(t3, 0, t4),           "sb t3,0(t4)")
emit(lbu(t8, 0, t4),          "lbu t8,0(t4)")

emit(addiu(t3, zero, 0x5a),   "addiu t3,zr,90")
emit(sb(t3, 0, t0),           "sb t3,0(t0)")
emit(addiu(t3, zero, 0xa5),   "addiu t3,zr,165")
emit(sb(t3, 0, t0),           "sb t3,0(t0)")
emit(lbu(s0, 0, t0),          "lbu s0,0(t0)")
emit(lbu(s1, 0, t0),          "lbu s1,0(t0)")

emit(addiu(t3, zero, 0x11),   "addiu t3,zr,17")
emit(sb(t3, 0, t0),           "sb t3,0(t0)")
emit(lbu(s2, STATUS_OFF, t0), "lbu s2,7(t0)")

emit(lui(t2, (BULK >> 16) & 0xffff), "lui t2,0x4")
emit(ori(t2, t2, BULK & 0xffff),     "ori t2,t2,0x01fe")
emit(addiu(t3, zero, 0x22),   "addiu t3,zr,34")
emit(sb(t3, 0, t0),           "sb t3,0(t0)")
emit(addiu(t2, t2, -1),       "addiu t2,t2,-1")
#  GXemul renders `bne rs,rt` with the operands the other way round, and turns
#  `beq zr,zr` into the `b` pseudo-op.  The WORD is the authoritative check; these
#  expectations are written to what the disassembler actually prints so the control
#  reports a real pass instead of crying wolf on two correct encodings.
emit(bne(t2, zero, -3),       "bne zr,t2,")
emit(NOP,                     "nop")
emit(lbu(s3, STATUS_OFF, t0), "lbu s3,7(t0)")

emit(addiu(t3, zero, 0x33),   "addiu t3,zr,51")
emit(sb(t3, 0, t0),           "sb t3,0(t0)")
emit(lbu(s4, STATUS_OFF, t0), "lbu s4,7(t0)")

emit(lbu(s5, 0, t0),          "lbu s5,0(t0)")

emit(addiu(t3, zero, 0x44),   "addiu t3,zr,68")
emit(sb(t3, 0, t0),           "sb t3,0(t0)")
emit(lbu(s6, STATUS_OFF, t0), "lbu s6,7(t0)")
emit(lbu(s7, 0, t0),          "lbu s7,0(t0)")

emit(or_(t9, t2, zero),       "or t9,t2,zr")
HALT = len(prog)
emit(beq(zero, zero, -1),     "b 0x")
emit(NOP,                     "nop")

HALT_ADDR = BASE + HALT * 4

REGS = ("t8", "s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7", "t9")

#  label, register, want SHIPPED, want FIXED, kind
ROWS = [
    ("A  RAM LIVENESS     RAM readback, same sb/lbu shapes", "t8", 0x55, 0x55, "control"),
    ("B  DEVICE SIGNATURE 1st read of the data port",        "s0", 0x5a, 0x5a, "control"),
    ("B  DEVICE SIGNATURE 2nd read -- a FIFO, not a cell",   "s1", 0xa5, 0xa5, "control"),
    ("C  LIVENESS         status, 1 byte staged: DRQ SET",   "s2", ST_DRQ, ST_DRQ, "control"),
    ("D  LIVENESS         status at SIZE-1: DRQ still SET",  "s3", ST_DRQ, ST_DRQ, "control"),
    ("E  *** DEFECT ***   status at SIZE: DRQ CLEAR",        "s4", ST_NODRQ, ST_DRQ, "defect"),
    ("F  *** DEFECT ***   data read on a FULL ring",         "s5", 0xff, 0x11, "defect"),
    ("G  *** DEFECT ***   status after one more push",       "s6", ST_DRQ, ST_DRQ, "control"),
    ("G  *** DEFECT ***   data read: oldest byte destroyed", "s7", 0x44, 0x22, "defect"),
    ("   loop counter drained",                              "t9", 0x00, 0x00, "control"),
]


class Emu(object):
    def __init__(self, argv, boot_wait=5.0):
        self.buf = bytearray()
        self.pid, self.fd = pty.fork()
        if self.pid == 0:
            try:
                os.execvp(argv[0], argv)
            finally:
                os._exit(127)
        self.drain(boot_wait)

    def drain(self, seconds):
        end = time.time() + seconds
        while time.time() < end:
            r, _, _ = select.select([self.fd], [], [], 0.05)
            if self.fd in r:
                try:
                    d = os.read(self.fd, 65536)
                except OSError:
                    return
                if not d:
                    return
                self.buf.extend(d)

    def send(self, cmd, wait=0.4):
        start = len(self.buf)
        data = (cmd + "\n").encode()
        view = memoryview(data)
        while len(view):
            n = os.write(self.fd, view)
            view = view[n:]
            if len(view):
                self.drain(0.05)
        self.drain(wait)
        return bytes(self.buf[start:]).decode("latin1", "replace")

    def close(self, log):
        try:
            os.write(self.fd, b"quit\n")
            self.drain(0.4)
        except OSError:
            pass
        for fn in (lambda: os.close(self.fd),
                   lambda: os.kill(self.pid, 9),
                   lambda: os.waitpid(self.pid, 0)):
            try:
                fn()
            except OSError:
                pass
        with open(log, "w") as f:
            f.write(bytes(self.buf).decode("latin1", "replace"))


def reg(emu, name):
    for _ in range(5):
        out = emu.send("print %s" % name, wait=0.35)
        m = re.findall(r"0x[0-9a-fA-F]+", out)
        if m:
            return int(m[-1], 16)
        emu.drain(0.25)
    return None


def run_one(binary, tag):
    """Run the SAME guest program on `binary` and return the observed bytes."""
    argv = [binary, "-V", "-E", "evbmips", "-e", "malta",
            "-d", "iR:" + DISK, "0x%x:%s" % (BASE, RAWBIN)]
    print("  command   " + " ".join(argv))
    emu = Emu(argv)

    #  CONTROL 0 -- every hand-encoded word checked against the emulator's own
    #  disassembler.  A wrong register field silently yields 0, and 0 is a value
    #  several rows below would accept by accident.  Addresses are printed WITHOUT
    #  an 0x prefix ("ffffffff80100000: 3c08b800  <- lui t0,0xb800"), which broke
    #  an earlier version of this parse -- so the check reported 0 of 34 and could
    #  not have passed.  A control that cannot pass is worth nothing.
    dis = emu.send("unassemble 0x%x 0x%x" % (BASE, BASE + len(prog) * 4), wait=1.8)
    seen = {}
    for line in dis.splitlines():
        m = re.match(r"^\s*([0-9a-f]{8,16}):\s+([0-9a-f]{8})\s+(?:<-)?\s*(.*)$", line)
        if m:
            seen[int(m.group(1), 16) & 0xffffffff] = (m.group(2), m.group(3).strip())

    enc_ok = enc_bad = 0
    bad_lines = []
    for i, (w, want_mn) in enumerate(prog):
        addr = (BASE + i * 4) & 0xffffffff
        hit = seen.get(addr)
        if hit is None:
            enc_bad += 1
            bad_lines.append("  BAD  0x%08x  no disassembly line" % addr)
            continue
        gotw, gotmn = hit
        norm = " ".join(gotmn.replace("\t", " ").split())
        want_norm = " ".join(want_mn.split())
        if gotw == "%08x" % w and norm.startswith(want_norm):
            enc_ok += 1
        else:
            enc_bad += 1
            bad_lines.append("  BAD  0x%08x  word %s vs %08x | %r vs want %r"
                             % (addr, gotw, w, norm, want_norm))
    print("  CONTROL 0 encodings: %d of %d words AND mnemonics agree with the"
          " emulator's disassembler" % (enc_ok, len(prog)))
    for l in bad_lines:
        print(l)

    pc0 = reg(emu, "pc")
    print("  pc at entry = %s (want 0x%016x)"
          % (("0x%016x" % pc0) if pc0 is not None else "UNREADABLE", BASE))

    emu.send("breakpoint add 0x%x" % HALT_ADDR, wait=0.5)
    t = time.time()
    emu.send("continue", wait=1.0)
    deadline = time.time() + 300
    while time.time() < deadline:
        emu.drain(0.5)
        tail = bytes(emu.buf[-4000:]).decode("latin1", "replace")
        if "BREAKPOINT" in tail.upper():
            break
    elapsed = time.time() - t

    got = {}
    for nm in REGS:
        v = reg(emu, nm)
        got[nm] = None if v is None else (v & 0xff)

    whole = bytes(emu.buf).decode("latin1", "replace")
    diags = {n: whole.count(n) for n in
             ("wdc inbuf overrun", "wdc inbuf full", "write to DATA, but not",
              "reading too much")}
    emu.close(os.path.join(LOGDIR, "transcript_%s.log" % tag))
    return got, elapsed, enc_ok, diags


def main():
    os.makedirs(LOGDIR, exist_ok=True)
    with open(RAWBIN, "wb") as f:
        for w, _ in prog:
            f.write(bytes([w & 0xff, (w >> 8) & 0xff,
                           (w >> 16) & 0xff, (w >> 24) & 0xff]))

    print("=" * 90)
    print("wdcringambig -- RUNG-3 WITNESS on unmodified `evbmips -e malta`")
    print("=" * 90)
    print("machine   evbmips -e malta   5Kc, little endian, 128 MB   (machine desc UNMODIFIED)")
    print("wdc       physical 0x180001f0 via bus_pci piix4_ide; reached at KSEG1"
          " 0xffffffffb80001f0")
    print("program   %d guest instructions at 0x%016x, parks at 0x%016x"
          % (len(prog), BASE, HALT_ADDR))
    print("ring      WDC_INBUF_SIZE = %d ; bulk loop pushes %d bytes" % (INBUF_SIZE, BULK))
    print()

    print("-" * 90)
    print("LEG 1 -- SHIPPED build (source-identical to GXEMUL-SEC at HEAD)")
    print("-" * 90)
    ship, t_ship, enc_ship, dg_ship = run_one(SHIPPED_BIN, "shipped")
    print("  elapsed %.2f s for %d guest device accesses -> %.0f accesses/second"
          % (t_ship, BULK + 12, (BULK + 12) / max(t_ship, 1e-9)))
    print()

    print("-" * 90)
    print("LEG 2 -- FIXED build (capacity check in wdc_addtoinbuf), SAME guest program")
    print("-" * 90)
    fix, t_fix, enc_fix, dg_fix = run_one(FIXED_BIN, "fixed")
    print("  elapsed %.2f s" % t_fix)
    print()

    print("-" * 90)
    print("RESULTS -- every value was produced by a guest load through real address decode")
    print("-" * 90)
    print("  %-52s %-4s %-16s %-16s" % ("", "reg", "SHIPPED", "FIXED"))
    npass = nfail = 0
    changed = []
    for label, rn, wship, wfix, kind in ROWS:
        gs, gf = ship.get(rn), fix.get(rn)
        oks = (gs == wship)
        okf = (gf == wfix)
        npass += oks + okf
        nfail += (not oks) + (not okf)
        if wship != wfix:
            changed.append((label, rn, wship, wfix, gs, gf))
        print("  %-52s %-4s want %02x got %-4s want %02x got %-4s  %s"
              % (label, rn, wship,
                 ("%02x" % gs) if gs is not None else "??",
                 wfix,
                 ("%02x" % gf) if gf is not None else "??",
                 ("ok" if (oks and okf) else "FAIL")))
    print()
    print("  %d of %d predictions correct across both legs" % (npass, npass + nfail))
    print()

    print("-" * 90)
    print("THE DIFFERENTIAL -- the rows the defect owns, same script, opposite colour")
    print("-" * 90)
    for label, rn, wship, wfix, gs, gf in changed:
        print("  %-52s %-4s  %02x -> %02x   %s"
              % (label, rn, gs if gs is not None else 0, gf if gf is not None else 0,
                 "AS PREDICTED" if (gs == wship and gf == wfix) else "MISMATCH"))
    print()

    print("-" * 90)
    print("WHY THIS IS THE DEVICE AND NOT RAM  (device-signature control)")
    print("-" * 90)
    print("  s0/s1 read the SAME address twice and returned 0x%02x then 0x%02x."
          % (ship.get("s0") or 0, ship.get("s1") or 0))
    print("  A memory cell returns the last value written (0xa5) BOTH times; only a FIFO")
    print("  returns them in push order.  This is the wdc inbuf, not a memory word.")
    print("  Status reads returned 0x%02x/0x%02x from +7.  DRDY|DSC|ERR = 0x51 is computed"
          % (ship.get("s2") or 0, ship.get("s4") or 0))
    print("  by status_byte() (dev_wdc.c:462-478) out of diskimage_exist() and the")
    print("  power-on d->error (dev_wdc.c:1655).  The guest never wrote any of it, and RAM")
    print("  at 0x180001f7 would answer 0x00.")
    print()
    print("  RAM liveness (t8=0x%02x) proves the sb/lbu shapes themselves work, so a"
          % (ship.get("t8") or 0))
    print("  device row reading 0x00 could not have been blamed on a bad encoding.")
    print()

    print("-" * 90)
    print("EMULATOR DIAGNOSTICS DURING EACH RUN")
    print("-" * 90)
    for n in sorted(set(list(dg_ship) + list(dg_fix))):
        print("  %-32s shipped x%d   fixed x%d" % (n, dg_ship.get(n, 0), dg_fix.get(n, 0)))
    print()
    print("  transcripts: %s/transcript_shipped.log , transcript_fixed.log" % LOGDIR)


if __name__ == "__main__":
    main()
