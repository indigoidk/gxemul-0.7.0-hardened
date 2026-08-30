"""wdcaddtoinbufbound -- RUNG-3 WITNESS.  Real guest instructions, real address
decode, real memory_rw, on an UNMODIFIED in-tree machine description
(`evbmips -e malta`).  No device is added and no machine description is edited.

THE DEFECT.  The guest WRITE arm of the wdc data port pushes bytes into the
shared inbuf ring with NO phase guard.  During an ATAPI DATA-IN transfer the
one diagnostic that could announce a stray write is suppressed, because its
condition requires !atapi_cmd_in_progress and that flag is 1 for the whole of
DATAIN.  Injected bytes grow `head` WITHOUT touching `atapi_len`, so they sit
in the ring ahead of the next chunk and the guest's whole next chunk arrives
SHIFTED.

THE ORACLE IS ABSOLUTE, NOT RELATIVE.  Chunk 2's bytes are poisoned at known
image offsets, so the fixed leg's expected values are tied to DISK CONTENT
through a channel outside the ring -- not merely "different from the shipped
leg".

THE PATH (all references GXEMUL-SEC/src/devices/dev_wdc.c at HEAD c125450):
  wd_command(7) <- 0xa0   wdc_command() ATAPI_PKT_CMD arm: sets
                          atapi_cmd_in_progress=1, atapi_phase=PHASE_CMDOUT.
  wd_data(0)   <- 12 CDB bytes (READ(10), LBA 0, 128 blocks -- see READ_BLOCKS
                          below for why 128 and not 32).  On the 12th,
                          inbuf_len==12 and the dispatch
                          fires (guarded by atapi_cmd_in_progress && !badlen_this
                          && atapi_phase==PHASE_CMDOUT && inbuf_len==12).
                          diskimage_scsicommand() READ(10) -> res==1,
                          data_in_len=65536; atapi_len clamped to 32768 and
                          32768 bytes pushed; atapi_phase=PHASE_DATAIN.
  wd_data(0)   -> 32767 byte reads.  Each pops one byte and decrements
                          atapi_len (consumed = len==4?4:(len>=2?2:1), clamped
                          to what remains).  atapi_len -> 1, ring holds 1.
  wd_data(0)   <- ONE 2-byte store.  The write arm's `case 2:` pushes
                          idata&0xff then (idata>>8)&0xff -- 0xa5 then 0x5a for
                          0x5aa5 little-endian.  atapi_len is UNTOUCHED.
  wd_data(0)   -> one byte read.  Pops the last chunk-1 byte, atapi_len -> 0,
                          and the re-arm fires: atapi_received(32768) <
                          data_in_len(65536), so atapi_len = 32768 and
                          data_in[32768+j] is pushed ONTO THE DIRTY RING.
  wd_data(0)   -> the next reads.  *** SHIPPED: the guest is handed its own
                          injected bytes back as disk data.  FIXED: chunk 2. ***

STATUS ORACLE, PINNED FROM SOURCE AND NOT FROM A MEASUREMENT.  status_byte()
ORs DRDY|DSC (0x50, diskimage_exist true), DRQ (0x08) when head != tail, DRQ
again when atapi_cmd_in_progress && (atapi_phase & WDCS_DRQ) -- PHASE_DATAIN is
WDCS_DRQ|WDCI_IN so that arm is set too -- and ERR (0x01) only when d->error.
wdc_command() assigns `d->error = 0` at its top, so after ATAPI_PKT_CMD the ERR
bit is CLEAR.  Expected: 0x58.  (The wdcringambig probe sees 0x59 because it
issues no command at all and the power-on d->error = 1 stands.)

WHY FREE-RUNNING AND NOT `step`:  DEVINIT sets d->data_debug = 1, so every
data-port access calls debug().  debug() adds 1 to `verbose` when single_step is
set and subtracts 1 when emul_executing, so a STEPPED run prints a line per
access while a FREE-RUNNING run at default verbosity has v == -1 and prints
nothing.  The probe therefore breakpoints and continues.

CONTROLS CARRIED (both mandated for an access witness):
  A  RAM LIVENESS      a known value round-trips through plain RAM using the
                       IDENTICAL sb/lbu instruction shapes.
  B  DEVICE SIGNATURE  two reads of the SAME data-port address return PUSH
                       ORDER (0x5a then 0xa5).  A memory cell cannot do this;
                       RAM would return a5,a5.
  D  DISK CONTENT      the first DATA-IN byte is the poisoned image byte 0xC0,
                       so the ring demonstrably holds real disk data.
  CONTROL 0            every hand-assembled word is checked against the
                       emulator's OWN disassembler.  A wrong register field
                       silently yields 0, which several rows would accept.

NOTHING IN THE REPO IS WRITTEN.  Both trees under measurement are copies under
/tmp, and the CD image is generated under /tmp.
"""
import os
import pty
import re
import select
import sys
import time

SHIPPED_BIN = "/tmp/gxadd/base/gxemul"
FIXED_BIN = os.environ.get("FIXBIN", "/tmp/gxadd/fixA/gxemul")
FIXTAG = os.environ.get("FIXTAG", "fixA")
CD = "/tmp/gxadd/cd.iso"
BASE = 0xffffffff80100000          # KSEG0, physical 0x00100000, inside malta's 128 MB
RAWBIN = "/tmp/gxadd/probe/addtoinbuf.bin"
LOGDIR = "/tmp/gxadd/probe"

DATA_HI, DATA_LO = 0xb800, 0x01f0  # wdc data port, KSEG1 (physical 0x180001f0)
CMD_OFF = 7                        # wd_command (W) / wd_status (R)
RAM_HI = 0x8020                    # KSEG0 scratch for the RAM liveness control

DRDY, DSC, DRQ, ERR = 0x40, 0x10, 0x08, 0x01
ST_DATAIN = DRDY | DSC | DRQ       # 0x58 -- ERR cleared by wdc_command()

ATAPI_PKT_CMD = 0xa0
# READ(10): opcode, flags, LBA[4] big-endian, reserved, len[2] big-endian, control
#
# *** THE BLOCK COUNT IS 128, NOT THE 32 THE ROUND'S SKETCH ASSUMED, AND THE
#     DIFFERENCE IS THE WHOLE WITNESS.  MEASURED, then explained: ***
# The sketch said "32 blocks on a CD-ROM", which reads as 32 x 2048 = 65536.
# In THIS tree a CD-ROM's logical_block_size is 512, not 2048 --
# diskimage.c:1984-1990 wraps the pmax/2048 choice in `#if 0` and assigns 512
# unconditionally, with a comment recording that OpenBSD/arc requires 512.
# diskimage_scsicmd.c:766 then computes size = retlen * logical_block_size.
# So 32 blocks is 16384 bytes -- BELOW the 32768 chunk clamp, so the whole
# transfer fits in chunk 1, atapi_received reaches data_in_len exactly, the
# re-arm takes its `else` branch to PHASE_COMPLETED, and NO SECOND CHUNK IS
# EVER FETCHED.  The defect cannot be exhibited at 32 blocks.
# MEASURED at 32 blocks: row F returned a5 (the injected byte) with the ring
# holding only the injection, and the over-read latch fired -- the signature of
# a transfer that ended early, not of the defect.
# 128 blocks x 512 = 65536 -> chunk 1 = 32768, chunk 2 = 32768, which is the
# two-chunk shape the defect needs.  ofs = LBA * 512 = 0, so data_in[j] is
# still image[j] and the poisoned offsets are unchanged.
READ_BLOCKS = 128
CDB = [0x28, 0, 0, 0, 0, 0, 0,
       (READ_BLOCKS >> 8) & 0xff, READ_BLOCKS & 0xff, 0, 0, 0]

DRAIN_AFTER_FIRST = 32766          # 1 (row D) + 32766 = 32767 pops -> atapi_len == 1
INJECT = 0x5aa5                    # -> pushes 0xa5 then 0x5a

zero, t0, t1, t2, t3, t4, t5, t6 = 0, 8, 9, 10, 11, 12, 13, 14
s0, s1, s2, s3, s4, s5, s6, s7 = 16, 17, 18, 19, 20, 21, 22, 23
t8, t9 = 24, 25


def R(op, rs, rt, rd, sa, fn):
    return (op << 26) | (rs << 21) | (rt << 16) | (rd << 11) | (sa << 6) | fn


def I(op, rs, rt, imm):
    return (op << 26) | (rs << 21) | (rt << 16) | (imm & 0xffff)


def lui(rt, imm):
    return I(0x0F, 0, rt, imm)


def ori(rt, rs, imm):
    return I(0x0D, rs, rt, imm)


def addiu(rt, rs, imm):
    return I(0x09, rs, rt, imm)


def sb(rt, off, base):
    return I(0x28, base, rt, off)


def sh(rt, off, base):
    return I(0x29, base, rt, off)


def lbu(rt, off, base):
    return I(0x24, base, rt, off)


def bne(rs, rt, off):
    return I(0x05, rs, rt, off)


def beq(rs, rt, off):
    return I(0x04, rs, rt, off)


def or_(rd, rs, rt):
    return R(0, rs, rt, rd, 0, 0x25)


NOP = 0
prog = []


def emit(word, want_mnemonic):
    prog.append((word, want_mnemonic))


emit(lui(t0, DATA_HI), "lui t0,0xb800")
emit(ori(t0, t0, DATA_LO), "ori t0,t0,0x01f0")
emit(lui(t4, RAM_HI), "lui t4,0x8020")

# A -- RAM LIVENESS, identical instruction shapes, plain RAM.
emit(addiu(t3, zero, 0x55), "addiu t3,zr,85")
emit(sb(t3, 0, t4), "sb t3,0(t4)")
emit(lbu(t8, 0, t4), "lbu t8,0(t4)")

# B -- DEVICE SIGNATURE.  Two pushes, then two reads of the SAME address.
emit(addiu(t3, zero, 0x5a), "addiu t3,zr,90")
emit(sb(t3, 0, t0), "sb t3,0(t0)")
emit(addiu(t3, zero, 0xa5), "addiu t3,zr,165")
emit(sb(t3, 0, t0), "sb t3,0(t0)")
emit(lbu(s0, 0, t0), "lbu s0,0(t0)")
emit(lbu(s1, 0, t0), "lbu s1,0(t0)")
# ring is empty again here: head == tail == 2.

# ARM the packet command.
emit(addiu(t3, zero, ATAPI_PKT_CMD), "addiu t3,zr,160")
emit(sb(t3, CMD_OFF, t0), "sb t3,7(t0)")

# Send the 12-byte CDB.  t3 is reloaded only when the value changes.
last = None
for b in CDB:
    if b != last:
        emit(addiu(t3, zero, b), "addiu t3,zr,%d" % b)
        last = b
    emit(sb(t3, 0, t0), "sb t3,0(t0)")
# On the 12th byte the dispatch fires and 32768 bytes are pushed.

# C -- status with the DATA-IN chunk queued.
emit(lbu(s2, CMD_OFF, t0), "lbu s2,7(t0)")

# D -- first DATA-IN byte: the poisoned image byte 0xC0 (disk-content control).
emit(lbu(s3, 0, t0), "lbu s3,0(t0)")

# drain the rest of chunk 1 but ONE byte.
emit(ori(t2, zero, DRAIN_AFTER_FIRST), "ori t2,zr,0x7ffe")
emit(lbu(t5, 0, t0), "lbu t5,0(t0)")
emit(addiu(t2, t2, -1), "addiu t2,t2,-1")
emit(bne(t2, zero, -3), "bne zr,t2,")
emit(NOP, "nop")

# E -- THE INJECTION.  One 2-byte store while atapi_phase == PHASE_DATAIN.
emit(ori(t6, zero, INJECT), "ori t6,zr,0x5aa5")
emit(sh(t6, 0, t0), "sh t6,0(t0)")

# F -- the last chunk-1 byte.  THIS read takes atapi_len to 0 and fires the
#      re-arm, which refills chunk 2 onto a ring still holding the injected bytes.
emit(lbu(s4, 0, t0), "lbu s4,0(t0)")

# G/H/I -- what the guest is handed as "chunk 2".
emit(lbu(s5, 0, t0), "lbu s5,0(t0)")
emit(lbu(s6, 0, t0), "lbu s6,0(t0)")
emit(lbu(s7, 0, t0), "lbu s7,0(t0)")

emit(or_(t9, t2, zero), "or t9,t2,zr")
HALT = len(prog)
emit(beq(zero, zero, -1), "b 0x")
emit(NOP, "nop")

HALT_ADDR = BASE + HALT * 4
REGS = ("t8", "s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7", "t9")

# label, register, want SHIPPED, want FIXED, kind
ROWS = [
    ("A  RAM LIVENESS     RAM readback, same sb/lbu shapes", "t8", 0x55, 0x55, "control"),
    ("B  DEVICE SIGNATURE 1st read of the data port", "s0", 0x5a, 0x5a, "control"),
    ("B  DEVICE SIGNATURE 2nd read -- a FIFO, not a cell", "s1", 0xa5, 0xa5, "control"),
    ("C  LIVENESS         status with chunk 1 queued", "s2", ST_DATAIN, ST_DATAIN, "control"),
    ("D  DISK CONTENT     chunk 1 byte 0 (image[0])", "s3", 0xC0, 0xC0, "control"),
    ("F  DISK CONTENT     chunk 1 LAST byte (image[32767])", "s4", 0xC1, 0xC1, "control"),
    ("G  *** DEFECT ***   1st byte after re-arm", "s5", 0xa5, 0xC2, "defect"),
    ("H  *** DEFECT ***   2nd byte after re-arm", "s6", 0x5a, 0xC3, "defect"),
    ("I  *** DEFECT ***   3rd byte after re-arm", "s7", 0xC2, 0xC4, "defect"),
    ("   drain loop counter reached zero", "t9", 0x00, 0x00, "control"),
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
    argv = [binary, "-V", "-E", "evbmips", "-e", "malta",
            "-d", "ciR:" + CD, "0x%x:%s" % (BASE, RAWBIN)]
    print("  command   " + " ".join(argv))
    emu = Emu(argv)

    # CONTROL 0 -- hand-assembled words checked against the emulator's own
    # disassembler.  Addresses print WITHOUT an 0x prefix.
    dis = emu.send("unassemble 0x%x 0x%x" % (BASE, BASE + len(prog) * 4), wait=2.5)
    seen = {}
    for line in dis.splitlines():
        m = re.match(r"^\s*([0-9a-f]{8,16}):\s+([0-9a-f]{8})\s+(?:<-)?\s*(.*)$", line)
        if m:
            seen[int(m.group(1), 16) & 0xffffffff] = (m.group(2), m.group(3).strip())

    word_ok = word_bad = mn_ok = mn_bad = 0
    bad_lines = []
    for i, (w, want_mn) in enumerate(prog):
        addr = (BASE + i * 4) & 0xffffffff
        hit = seen.get(addr)
        if hit is None:
            word_bad += 1
            mn_bad += 1
            bad_lines.append("  BAD  0x%08x  no disassembly line" % addr)
            continue
        gotw, gotmn = hit
        norm = " ".join(gotmn.replace("\t", " ").split())
        want_norm = " ".join(want_mn.split())
        if gotw == "%08x" % w:
            word_ok += 1
        else:
            word_bad += 1
            bad_lines.append("  BADWORD 0x%08x  %s vs %08x" % (addr, gotw, w))
        if norm.startswith(want_norm):
            mn_ok += 1
        else:
            mn_bad += 1
            bad_lines.append("  MNEMONIC 0x%08x  %r vs want %r" % (addr, norm, want_norm))
    print("  CONTROL 0  words %d of %d ; mnemonics %d of %d agree with the"
          " emulator's disassembler" % (word_ok, len(prog), mn_ok, len(prog)))
    for l in bad_lines[:14]:
        print(l)

    pc0 = reg(emu, "pc")
    print("  pc at entry = %s (want 0x%016x)"
          % (("0x%016x" % pc0) if pc0 is not None else "UNREADABLE", BASE))

    emu.send("breakpoint add 0x%x" % HALT_ADDR, wait=0.5)
    t = time.time()
    emu.send("continue", wait=1.0)
    deadline = time.time() + 300
    hit = False
    while time.time() < deadline:
        emu.drain(0.5)
        tail = bytes(emu.buf[-4000:]).decode("latin1", "replace")
        if "BREAKPOINT" in tail.upper():
            hit = True
            break
    elapsed = time.time() - t
    if not hit:
        print("  *** BREAKPOINT NOT REACHED within 300 s"
              " -- rows below are NOT a measurement")

    got = {}
    for nm in REGS:
        v = reg(emu, nm)
        got[nm] = None if v is None else (v & 0xff)

    whole = bytes(emu.buf).decode("latin1", "replace")
    diags = {n: whole.count(n) for n in
             ("wdc inbuf overrun", "write to DATA, but not", "reading too much",
              "ATAPI command rejected", "DATA OUT")}
    emu.close(os.path.join(LOGDIR, "transcript_%s.log" % tag))
    return got, elapsed, hit, diags


def main():
    os.makedirs(LOGDIR, exist_ok=True)
    with open(RAWBIN, "wb") as f:
        for w, _ in prog:
            f.write(bytes([w & 0xff, (w >> 8) & 0xff,
                           (w >> 16) & 0xff, (w >> 24) & 0xff]))

    print("=" * 94)
    print("wdcaddtoinbufbound -- RUNG-3 WITNESS on unmodified `evbmips -e malta`")
    print("=" * 94)
    print("machine   evbmips -e malta  5Kc, little endian, 128 MB (machine desc UNMODIFIED)")
    print("wdc       physical 0x180001f0 via bus_pci piix4_ide; KSEG1 0xffffffffb80001f0")
    print("media     -d ciR:%s  (CD-ROM, IDE, read-only)" % CD)
    print("program   %d guest instructions at 0x%016x, parks at 0x%016x"
          % (len(prog), BASE, HALT_ADDR))
    print("transfer  READ(10) LBA 0 x %d blocks of 512 = %d B; chunk 1 = 32768"
          % (READ_BLOCKS, READ_BLOCKS * 512))
    print("inject    ONE 2-byte store of 0x%04x while atapi_phase == PHASE_DATAIN" % INJECT)
    print()

    print("-" * 94)
    print("LEG 1 -- SHIPPED build (source-identical to GXEMUL-SEC at HEAD c125450)")
    print("-" * 94)
    ship, t_ship, hit_s, dg_s = run_one(SHIPPED_BIN, "shipped")
    print("  elapsed %.2f s   breakpoint reached: %s" % (t_ship, hit_s))
    print("  diagnostics seen: %s" % dg_s)
    print()

    print("-" * 94)
    print("LEG 2 -- %s build, SAME guest program, SAME image" % FIXTAG)
    print("-" * 94)
    fix, t_fix, hit_f, dg_f = run_one(FIXED_BIN, FIXTAG)
    print("  elapsed %.2f s   breakpoint reached: %s" % (t_fix, hit_f))
    print("  diagnostics seen: %s" % dg_f)
    print()

    print("-" * 94)
    print("RESULTS -- every value below was produced by a GUEST LOAD through real decode")
    print("-" * 94)
    print("  %-52s %-4s %-16s %-16s" % ("", "reg", "SHIPPED", FIXTAG.upper()))
    npass = nfail = 0
    changed = []
    for label, rn, wship, wfix, kind in ROWS:
        gs, gf = ship.get(rn), fix.get(rn)
        oks, okf = (gs == wship), (gf == wfix)
        npass += oks + okf
        nfail += (not oks) + (not okf)
        if wship != wfix:
            changed.append((label, rn, wship, wfix, gs, gf))
        print("  %-52s %-4s want %02x got %-4s want %02x got %-4s  %s"
              % (label, rn, wship, ("%02x" % gs) if gs is not None else "??",
                 wfix, ("%02x" % gf) if gf is not None else "??",
                 ("ok" if (oks and okf) else "FAIL")))
    print()
    print("  %d of %d predictions correct across both legs" % (npass, npass + nfail))
    print()

    print("-" * 94)
    print("THE DIFFERENTIAL -- the rows the defect owns, same script, opposite colour")
    print("-" * 94)
    for label, rn, wship, wfix, gs, gf in changed:
        print("  %-52s %-4s  %02x -> %02x   %s"
              % (label, rn, gs if gs is not None else 0, gf if gf is not None else 0,
                 "AS PREDICTED" if (gs == wship and gf == wfix) else "MISMATCH"))
    print()
    print("-" * 94)
    print("WHY THIS IS THE DEVICE AND NOT RAM  (device-signature control)")
    print("-" * 94)
    print("  s0/s1 read the SAME address twice and returned 0x%02x then 0x%02x."
          % (ship.get("s0") or 0, ship.get("s1") or 0))
    print("  A memory cell returns the last value written to BOTH reads (a5,a5).")
    print("  Push order (5a,a5) can only come from a FIFO -- the wdc inbuf ring.")
    print("  And row D returned 0x%02x, the poisoned CD image byte at offset 0,"
          % (ship.get("s3") or 0))
    print("  so the ring demonstrably holds real DISK data, not device scratch.")
    print()
    print("ADDTOINBUF_RUNG3_DONE")


main()
