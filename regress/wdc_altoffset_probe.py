"""wdcaltoffset -- RUNG-3 WITNESS AND DETECTOR.  Real guest instructions, real address
decode, real memory_rw, on an UNMODIFIED in-tree machine description (evbmips -e malta).

THE DEFECT.  DEVICE_ACCESS(wdc_altstatus) in src/devices/dev_wdc.c reads relative_addr
ZERO times, while dev_wdc_init registers its region TWO BYTES WIDE.  The durable keys are
grep anchors, not line numbers:

    grep -n 'DEVICE_ACCESS(wdc_altstatus)'   src/devices/dev_wdc.c
    grep -n '"wdc_altstatus",'               src/devices/dev_wdc.c

        memory_device_register(..., "wdc_altstatus", alt_status_addr, 2,
            dev_wdc_altstatus_access, d, DM_DEFAULT, NULL);

    offset 0  ->  0x3f6  Device Control      (write: nIEN, SRST, 4BIT)
    offset 1  ->  0x3f7  Drive Address Reg   READ-ONLY on real ATA hardware

Both offsets land in the same handler body, so a guest STORE to 0x3f7 is executed as a
store to Device Control.  Since #481 corrected the arm's bit to WDCTL_RST and wired in
wdc_new_command_reset(), that store now performs a full soft reset: write_in_progress is
cleared and the input ring is purged.  A write to a register the guest is not even
allowed to write aborts a live ATA WRITE SECTORS and destroys its staged bytes.

THE MACHINE IS NOT MODIFIED AND NO DEVICE IS ADDED.  malta carries a wdc through its own
committed path: machine_evbmips.c bus_pci_add(..., "piix4_ide") -> bus_pci.c
PCIINIT(piix4_ide), which does device_add(machine, "wdc addr=<isa_portbase+0x1f0> ...")
whenever an IDE image is attached; isa_portbase = 0x18000000.  Attaching a disk image is
ordinary operation, not a machine edit.

    wdc registers      physical 0x180001f0 + N  ->  KSEG1 0xffffffffb80001f0 + N
    wdc_altstatus      physical 0x180003f6      ->  KSEG1 0xffffffffb80003f6
    the read-only reg  physical 0x180003f7      ->  KSEG1 0xffffffffb80003f7

THE SHAPE OF THE WITNESS -- FOUR phases, IDENTICAL except for the address of one
store (phases 2 and 4 differ only in the VALUE stored).

    PHASE 1  poke 0x06 (nIEN|SRST) at 0x3f6, the REAL Device Control register.
             A legitimate soft reset.  BOTH builds must abort the armed write.
             This is the ACCEPT control the de-escalation clause demands: it proves the
             fix leg does not disable the register it is supposed to leave alone, and it
             proves the reset machinery this probe observes is alive.

    PHASE 2  poke the SAME 0x06 at 0x3f7, the READ-ONLY Drive Address Register.
             *** THE DEFECT.  Committed build: identical to phase 1.  Fix leg: nothing
             happens. ***

    PHASE 3  poke 0x02 (nIEN alone, WDCTL_RST clear) at 0x3f7.
             Neither build resets.  This is the discriminator that says the defect is
             the RESET BIT reaching a register that has none, rather than "any store to
             0x3f7 does something".

PHASE 1 AND PHASE 2 ARE THE ANCHOR (vacuity-floor clause (f)).  They are the same
stimulus at ADJACENT addresses, so the pair pins WHERE the store lands, not merely that
two addresses behave differently.  On the committed build the two phases are
indistinguishable -- which IS the defect, stated as a measurement.

THE TWO CONTROLS THE WITNESS LADDER DEMANDS FOR AN ACCESS WITNESS:

    LIVENESS          three of them.
                      (a) RAM: the same sb/lbu instruction shapes round-trip 0x55
                          through plain RAM, so a device row reading 0x00 could not be
                          blamed on a bad encoding.
                      (b) DEVICE REGISTER: 0x55 -> cyl_lo and 0x66 -> cyl_hi read back
                          as 0x6655 through the wdc's own decode.  This is #481's
                          preserved liveness=0x6655 idiom, kept deliberately so this
                          witness and that one are comparable.
                      (c) per phase: the ARMED status read, which must show DRQ before
                          the poke or the phase measured nothing.

    DEVICE SIGNATURE  two of them.
                      (a) FIFO: push 0x5a then 0xa5 to the data port and read the SAME
                          address twice.  A memory cell returns 0xa5 both times; only a
                          FIFO returns them in push order.
                      (b) STATUS: the byte at +7 is COMPUTED by status_byte() out of
                          diskimage_exist(), d->error and d->write_in_progress.  The
                          guest never wrote it.  RAM would answer with what was stored.

WHY THIS IS ALSO A DETECTOR, NOT ONLY A WITNESS.  Every row carries a want for BOTH
legs.  Phase 2's two rows are the only ones whose want DIFFERS between the legs; every
other row is an identity row that must hold on both.  So the file fails on the committed
build, passes once the handler decodes its offset, and still fails if a future fix
over-reaches: a build that refuses offset 0 as well reds PHASE 1, and a build that keeps
the decode but nulls its effect reds PHASE 2 again.

BYTE ORDER.  evbmips -e malta is LITTLE-endian.  Every access here is a single byte, so
byte order cannot silently change what a row means -- stated because a sibling detector
in this tree was measured testing the wrong endianness.

Usage:  wdcaltoff_rung3_probe.py <base-binary> <fix-binary> <disk-image> [outdir]

BOTH LEGS RUN INSIDE ONE PYTHON INVOCATION, SO THE INSTRUMENT IS IDENTICAL BY
CONSTRUCTION.  A driver shaped "for t in base fix; do python3 probe.py $t; done" gives
the two legs different instruments if the probe is edited between them, and the
difference lands in the very output being diffed.

NOTHING IN THE REPO IS WRITTEN.  Both trees under measurement are copies under /tmp, and
the disk image is attached with the iR: prefix, whose overlay is pid-unique.
CONTRACT -- vacuity-floor clause (e).  What this detector is DESIGNED to catch, and
what it is blind to.  Stated so a later escape is either outside this contract or a
breach of it, rather than an argument about whether the round overclaimed.

  CATCHES: edits to the offset decode of the wdc_altstatus WRITE arm.
    * widening the decline so it also refuses offset 0   -> P1 accept rows red
    * nulling or narrowing it so a store addressed at offset 1 reaches the reset
      again -> P2 and P4 red, via DRQ and the input ring
    * value-conditioned guards ("decline only the value we have seen") -> P4 exists
      for exactly this: its store carries the bare reset bit 0x04, not the 0x06 the
      witness and #481's comment both use

  BLIND BY CONSTRUCTION -- each of these is another row's job or another row's absence:
    * PARTIAL-GUARD edits that clobber d->cur_command but spare the ring.  NO row here
      observes cur_command.  That is wdc_altoffset_sig_probe.py's contract, and it
      needs a ciR: CD-ROM rig.  Measured: such a mutant passes all 18 rows here.
    * READS of the alt region.  No row reads either offset.  Tracked as wdcaltdigin.
    * MULTI-BYTE stores.  Every row is len == 1; a len == 2 store at offset 0 passes
      the decode and its second byte is consumed silently.  Tracked as wdcaltwidth.
    * the DIAGNOSTIC TEXT.  No row reads debug output, so an edit that declines
      correctly while naming the wrong register passes.  Filed, not fixed.
    * anything outside DEVICE_ACCESS(wdc_altstatus).

  NOT WIRED INTO A GATE.  Both probes are two-leg differentials -- they take a
  PRE-FIX binary and a post-fix one -- and no gate builds a second leg.  Dated-exempt
  in check_probe_wiring.py until 2026-09-20, pending a single-leg mode.  Until then
  THE BATTERY DEFENDS NONE OF THIS; the kill table is the evidence.

"""
import os
import pty
import re
import select
import sys
import time

BASE_BIN = sys.argv[1] if len(sys.argv) > 1 else "/tmp/gxaltoff/base/gxemul"
FIX_BIN = sys.argv[2] if len(sys.argv) > 2 else "/tmp/gxaltoff/fix/gxemul"
DISK = sys.argv[3] if len(sys.argv) > 3 else "/tmp/gxaltoff/altoff-scratch.img"

#  HOW THE IMAGE IS ATTACHED, as a parameter rather than a hardcode.  The measuring
#  seat that found the m3 escape had to SHIM run_one() to reach the CD-ROM prefix,
#  and said so; a companion probe that needs `ciR:` sets this instead.  The prefix is
#  not cosmetic -- `c` is what makes diskimage_is_a_cdrom() true, and the ATAPI
#  signature channel is DEAD without it.
DISK_PREFIX = "iR:"
OUTDIR = sys.argv[4] if len(sys.argv) > 4 else "/tmp/gxaltoff/run"

BASE = 0xffffffff80100000          # KSEG0, physical 0x00100000, inside malta's 128 MB
RAWBIN = None                      # set in main(), lives under OUTDIR

WDC_HI, WDC_LO = 0xb800, 0x01f0    # wdc register file, KSEG1
ALT_HI, ALT_LO = 0xb800, 0x03f6    # wdc_altstatus region, KSEG1
RAM_HI = 0x8020                    # KSEG0 scratch for the RAM liveness control

#  Register offsets from the wdc base -- src/include/thirdparty/wdcreg.h
R_DATA, R_SECCNT, R_SECTOR = 0, 2, 3
R_CYL_LO, R_CYL_HI, R_SDH = 4, 5, 6
R_STATUS = 7                       # wd_command on write, wd_status on read

#  Status bits -- wdcreg.h
DRDY, DSC, DRQ, ERR = 0x40, 0x10, 0x08, 0x01

#  status_byte() ORs DRDY|DSC because diskimage_exist() is true for the attached IDE
#  image; DRQ iff (inbuf_head != inbuf_tail) OR write_in_progress; ERR iff d->error.
#
#  d->error IS SET AT DEVINIT.  Grep it as "->error" -- dev_wdc_init writes
#  "d->error      = 1;" with the field name padded, so a grep for "d->error = 1" with a
#  SINGLE space MATCHES NOTHING and reports that the field starts at 0.  It did, while
#  this file was being written, and the first run's measured 0x51 against a predicted
#  0x50 is what sent me back to look.  A pattern that matches nothing reports zero for
#  everything, which is this project's oldest apparatus trap -- and here the measurement
#  caught the reading rather than the other way round.
#
#  wdc_command() clears it ("d->error = 0" at the top), so the power-on ERR bit stands
#  only until the first phase issues WDCC_WRITE.
ST_POWERON = DRDY | DSC | ERR      # 0x51  before any command has been issued
ST_IDLE = DRDY | DSC               # 0x50  ring empty, no write armed, error cleared
ST_ARMED = DRDY | DSC | DRQ        # 0x58  write_in_progress set

WDCC_WRITE = 0x30                  # wdcreg.h
WDCTL_RST = 0x04
WDCTL_IDS = 0x02
SRST_POKE = WDCTL_IDS | WDCTL_RST  # 0x06 -- what older OpenBSD asserts; #481's value
NIEN_POKE = WDCTL_IDS              # 0x02 -- no reset bit at all
BARE_RST = WDCTL_RST               # 0x04 -- RST with nothing else set

STAGE = [0x71, 0x72, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78]

zero, v0, v1, a0, a1, a2, a3 = 0, 2, 3, 4, 5, 6, 7
t0, t1, t2, t3 = 8, 9, 10, 11
t4, t5, t6 = 12, 13, 14            # PHASE 4's results; t3 is e_store()'s scratch
s0, s1, s2, s3, s4, s5, s6, s7 = 16, 17, 18, 19, 20, 21, 22, 23
t9 = 25


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


def lbu(rt, off, base):
    return I(0x24, base, rt, off)


def beq(rs, rt, off):
    return I(0x04, rs, rt, off)


NOP = 0
NAME = {zero: "zr", v0: "v0", v1: "v1", a0: "a0", a1: "a1", a2: "a2", a3: "a3",
        t0: "t0", t1: "t1", t2: "t2", t3: "t3", t4: "t4", t5: "t5", t6: "t6",
        s0: "s0", s1: "s1", s2: "s2",
        s3: "s3", s4: "s4", s5: "s5", s6: "s6", s7: "s7", t9: "t9"}

prog = []


def emit(word, mn):
    """mn is checked against the EMULATOR'S OWN disassembly.

    A wrong register field silently yields 0, and 0 is a value several rows below would
    accept by accident -- this project has shipped that mistake into a committed gate.
    """
    prog.append((word, mn))


def e_li(rt, v):
    emit(addiu(rt, zero, v), "addiu %s,zr,%d" % (NAME[rt], v))


def e_sb(rt, off, base):
    emit(sb(rt, off, base), "sb %s,%d(%s)" % (NAME[rt], off, NAME[base]))


def e_lbu(rt, off, base):
    emit(lbu(rt, off, base), "lbu %s,%d(%s)" % (NAME[rt], off, NAME[base]))


def e_store(val, off, base):
    e_li(t3, val)
    e_sb(t3, off, base)


def arm_a_write():
    """Arm WDCC_WRITE and stage STAGE into the input ring.

    wdc_command() -> wdc__write() sets d->write_in_progress = d->cur_command, which is
    what makes status_byte() raise DRQ.  wdc_command() also calls
    wdc_new_command_reset(), so each phase starts from a clean ring on BOTH legs
    regardless of what the previous phase left -- that is what keeps the phases
    independent, and it is why phase 3 measures the same thing on both legs even though
    phase 2 left them in different states.

    len(STAGE) is 8, deliberately NOT a multiple of 512: the sector drain inside
    DEVICE_ACCESS(wdc) fires on "inbuf_len % 512 == 0", so nothing reaches the disk
    image and the staged bytes simply sit in the ring where the reset can destroy them.
    """
    e_store(0xa0, R_SDH, t0)       # drive 0, head 0 (bits 7 and 5 are the obsolete 1s)
    e_store(0x01, R_SECCNT, t0)
    e_store(0x01, R_SECTOR, t0)
    e_store(0x00, R_CYL_LO, t0)
    e_store(0x00, R_CYL_HI, t0)
    e_store(WDCC_WRITE, R_STATUS, t0)
    for b in STAGE:
        e_store(b, R_DATA, t0)


#  ---------------------------------------------------------------- setup
emit(lui(t0, WDC_HI), "lui t0,0xb800")
emit(ori(t0, t0, WDC_LO), "ori t0,t0,0x01f0")
emit(lui(t1, ALT_HI), "lui t1,0xb800")
emit(ori(t1, t1, ALT_LO), "ori t1,t1,0x03f6")
emit(lui(t2, RAM_HI), "lui t2,0x8020")

#  A -- RAM LIVENESS: the same instruction shapes, through plain RAM.
e_store(0x55, 0, t2)
e_lbu(v0, 0, t2)

#  B -- DEVICE-REGISTER LIVENESS: #481's 0x6655, through the wdc's own decode.
e_store(0x55, R_CYL_LO, t0)
e_store(0x66, R_CYL_HI, t0)
e_lbu(v1, R_CYL_LO, t0)
e_lbu(a0, R_CYL_HI, t0)

#  C -- DEVICE SIGNATURE: the data port is a FIFO, not a cell.
e_store(0x5a, R_DATA, t0)
e_store(0xa5, R_DATA, t0)
e_lbu(a1, R_DATA, t0)
e_lbu(a2, R_DATA, t0)

#  D -- DEVICE SIGNATURE: a status byte the guest never wrote.
e_lbu(a3, R_STATUS, t0)

#  ------------------------------------------------- PHASE 1: 0x3f6, a real SRST
arm_a_write()
e_lbu(s0, R_STATUS, t0)            # armed -> DRQ set
e_store(SRST_POKE, 0, t1)          # <<< 0x3f6, the Device Control register
e_lbu(s1, R_STATUS, t0)            # both legs: DRQ CLEAR
e_lbu(s2, R_DATA, t0)              # both legs: 0xff, the ring is empty

#  ------------------------------------- PHASE 2: 0x3f7, THE READ-ONLY REGISTER
arm_a_write()
e_lbu(s3, R_STATUS, t0)            # armed -> DRQ set
e_store(SRST_POKE, 1, t1)          # <<< 0x3f7, the Drive Address Register
e_lbu(s4, R_STATUS, t0)            # base: DRQ CLEAR   fix: DRQ still SET
e_lbu(s5, R_DATA, t0)              # base: 0xff        fix: 0x71, the staged byte

#  ------------------------- PHASE 3: 0x3f7 again, with the RESET BIT NOT SET
arm_a_write()
e_lbu(s6, R_STATUS, t0)            # armed -> DRQ set
e_store(NIEN_POKE, 1, t1)          # <<< 0x3f7 with WDCTL_RST clear
e_lbu(s7, R_STATUS, t0)            # both legs: DRQ still SET
e_lbu(t9, R_DATA, t0)              # both legs: 0x71

#  ---------------- PHASE 4: 0x3f7 carrying the BARE reset bit, 0x04 not 0x06
#
#  WHY A SECOND VALUE AT THE SAME OFFSET IS NOT A DUPLICATE ROW.  Phase 2's only
#  defect-side store is 0x06, and 0x06 is ALSO the value #481's comment records as
#  real traffic ("Older OpenBSD asserts with 0x06").  So the plausible future edit
#  is to tighten the decline to the value someone has seen -- `relative_addr != 0 &&
#  idata == 0x06` -- which keeps every phase-2 row GREEN and re-opens the defect for
#  0x04, 0x0c and 0x0e.  This phase is the row that refuses that edit.
#
#  0x04 is the discriminating choice rather than an arbitrary second value: it kills
#  an equality guard on 0x06, and phase 2 symmetrically kills any re-aim to 0x04.
arm_a_write()
e_lbu(t4, R_STATUS, t0)            # armed -> DRQ set
e_store(BARE_RST, 1, t1)           # <<< 0x3f7, reset bit alone
e_lbu(t5, R_STATUS, t0)            # base: DRQ CLEAR   fix: DRQ still SET
e_lbu(t6, R_DATA, t0)              # base: 0xff        fix: 0x71, the staged byte

HALT = len(prog)
emit(beq(zero, zero, -1), "b 0x")
emit(NOP, "nop")
HALT_ADDR = BASE + HALT * 4

REGS = ("v0", "v1", "a0", "a1", "a2", "a3", "t4", "t5", "t6",
        "s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7", "t9")

FF = 0xff       # wdc_get_inbuf() returns (uint64_t)-1 on an empty ring; lbu takes 0xff

#  label, register, want on the COMMITTED build, want on the FIX leg, kind
ROWS = [
    ("A   liveness   RAM round-trip, same sb/lbu shapes",
     "v0", 0x55, 0x55, "control"),
    ("B   liveness   cyl_lo readback (0x6655 low byte)",
     "v1", 0x55, 0x55, "control"),
    ("B   liveness   cyl_hi readback (0x6655 high byte)",
     "a0", 0x66, 0x66, "control"),
    ("C   devsig     data port 1st read -- a FIFO",
     "a1", 0x5a, 0x5a, "control"),
    ("C   devsig     data port 2nd read -- not a cell",
     "a2", 0xa5, 0xa5, "control"),
    ("D   devsig     status byte computed by the device",
     "a3", ST_POWERON, ST_POWERON, "control"),
    ("P1  liveness   armed for the 0x3f6 phase: DRQ SET",
     "s0", ST_ARMED, ST_ARMED, "control"),
    ("P1  accept     0x3f6 SRST aborts the write: DRQ CLEAR",
     "s1", ST_IDLE, ST_IDLE, "accept"),
    ("P1  accept     0x3f6 SRST purged the ring: 0xff",
     "s2", FF, FF, "accept"),
    ("P2  liveness   armed for the 0x3f7 phase: DRQ SET",
     "s3", ST_ARMED, ST_ARMED, "control"),
    ("P2  *DEFECT*   0x3f7 store aborts the live write",
     "s4", ST_IDLE, ST_ARMED, "defect"),
    ("P2  *DEFECT*   0x3f7 store purged the staged bytes",
     "s5", FF, 0x71, "defect"),
    ("P3  liveness   armed for the nIEN phase: DRQ SET",
     "s6", ST_ARMED, ST_ARMED, "control"),
    ("P3  control    0x3f7 without WDCTL_RST: DRQ still SET",
     "s7", ST_ARMED, ST_ARMED, "control"),
    ("P3  control    0x3f7 without WDCTL_RST: bytes intact",
     "t9", 0x71, 0x71, "control"),
    ("P4  liveness   armed for the bare-RST phase: DRQ SET",
     "t4", ST_ARMED, ST_ARMED, "control"),
    ("P4  *DEFECT*   0x3f7 bare RST 0x04 aborts the write",
     "t5", ST_IDLE, ST_ARMED, "defect"),
    ("P4  *DEFECT*   0x3f7 bare RST 0x04 purged the bytes",
     "t6", FF, 0x71, "defect"),
]

#  THE PADDED-COLUMN TRAP, refused by construction.  The result line formats the
#  label with %-56s; a label AT OR OVER that width runs into the next column and a
#  gate grepping for `^<label> .*ok$` then matches NOTHING -- the row silently stops
#  being tested.  This project has shipped that defect before, so it is asserted
#  here rather than remembered.
_LW = max(len(r[0]) for r in ROWS)
assert _LW < 56, 'row label %d chars, the %%-56s column silently truncates' % _LW

#  And the registers must be DISTINCT: two rows sharing one register would both
#  report whatever the later store left, which reads as agreement.
assert len(set(r[1] for r in ROWS)) == len(ROWS), 'two rows share a register'


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


def run_one(binary, tag, out):
    argv = [binary, "-V", "-E", "evbmips", "-e", "malta",
            "-d", DISK_PREFIX + DISK, "0x%x:%s" % (BASE, RAWBIN)]
    out("  command   " + " ".join(argv))
    emu = Emu(argv)

    #  CONTROL 0 -- every hand-encoded word checked against the emulator's own
    #  disassembler.  Addresses are printed WITHOUT an 0x prefix.  The WORD is the
    #  authoritative check; the mnemonic is a rendering and is counted separately so a
    #  spelling this file guessed wrong cannot masquerade as a bad encoding.
    dis = emu.send("unassemble 0x%x 0x%x" % (BASE, BASE + len(prog) * 4), wait=3.0)
    seen = {}
    for line in dis.splitlines():
        m = re.match(r"^\s*([0-9a-f]{8,16}):\s+([0-9a-f]{8})\s+(?:<-)?\s*(.*)$", line)
        if m:
            seen[int(m.group(1), 16) & 0xffffffff] = (m.group(2), m.group(3).strip())

    w_ok = m_ok = 0
    bad = []
    for i, (w, want_mn) in enumerate(prog):
        addr = (BASE + i * 4) & 0xffffffff
        hit = seen.get(addr)
        if hit is None:
            bad.append("  BAD  0x%08x  no disassembly line" % addr)
            continue
        gotw, gotmn = hit
        norm = " ".join(gotmn.replace("\t", " ").split())
        if gotw == "%08x" % w:
            w_ok += 1
        else:
            bad.append("  BAD  0x%08x  word %s vs %08x" % (addr, gotw, w))
        if norm.startswith(" ".join(want_mn.split())):
            m_ok += 1
        else:
            bad.append("  MNEMONIC 0x%08x  got %r want %r" % (addr, norm, want_mn))
    out("  CONTROL 0 encodings: %d of %d WORDS and %d of %d mnemonics agree with the"
        " emulator's own disassembler" % (w_ok, len(prog), m_ok, len(prog)))
    for l in bad:
        out(l)

    pc0 = reg(emu, "pc")
    out("  pc at entry = %s (want 0x%016x)"
        % (("0x%016x" % pc0) if pc0 is not None else "UNREADABLE", BASE))

    emu.send("breakpoint add 0x%x" % HALT_ADDR, wait=0.5)
    t = time.time()
    emu.send("continue", wait=1.0)
    deadline = time.time() + 120
    hit = False
    while time.time() < deadline:
        emu.drain(0.5)
        tail = bytes(emu.buf[-4000:]).decode("latin1", "replace")
        if "BREAKPOINT" in tail.upper():
            hit = True
            break
    elapsed = time.time() - t
    out("  parked at the halt breakpoint: %s   (%.2f s)"
        % ("yes" if hit else
           "*** NO -- the guest never reached 0x%016x ***" % HALT_ADDR, elapsed))

    got = {}
    for nm in REGS:
        v = reg(emu, nm)
        got[nm] = None if v is None else (v & 0xff)

    whole = bytes(emu.buf).decode("latin1", "replace")
    diags = {n: whole.count(n) for n in
             ("write to DATA, but not", "reading too much", "wdc inbuf overrun",
              "wdc inbuf full", "write to ALT. CTRL", "DRIVE ADDRESS")}
    emu.close(os.path.join(OUTDIR, "transcript_%s.log" % tag))
    return got, w_ok, m_ok, hit, diags


def main():
    global RAWBIN
    os.makedirs(OUTDIR, exist_ok=True)
    RAWBIN = os.path.join(OUTDIR, "wdcaltoff.bin")
    with open(RAWBIN, "wb") as f:
        for w, _ in prog:
            f.write(bytes([w & 0xff, (w >> 8) & 0xff,
                           (w >> 16) & 0xff, (w >> 24) & 0xff]))

    lines = []

    def out(s=""):
        lines.append(s)
        print(s)
        sys.stdout.flush()

    out("=" * 94)
    out("wdcaltoffset -- RUNG-3 WITNESS + DETECTOR on unmodified `evbmips -e malta`")
    out("=" * 94)
    out("date      %s" % time.strftime("%Y-%m-%d %H:%M:%S"))
    out("machine   evbmips -e malta   5Kc, LITTLE endian   (machine desc UNMODIFIED)")
    out("wdc       physical 0x180001f0 via bus_pci piix4_ide; KSEG1 0xffffffffb80001f0")
    out("altstat   physical 0x180003f6 len 2; offset 1 = 0x180003f7 = the READ-ONLY")
    out("          Drive Address Register, KSEG1 0xffffffffb80003f7")
    out("program   %d guest instructions at 0x%016x, parks at 0x%016x"
        % (len(prog), BASE, HALT_ADDR))
    out("staged    %d bytes per phase (%s) -- NOT a multiple of 512, so the sector"
        % (len(STAGE), " ".join("%02x" % b for b in STAGE)))
    out("          drain never fires and nothing reaches the disk image")
    out("base bin  %s" % BASE_BIN)
    out("fix bin   %s" % FIX_BIN)
    out()

    out("-" * 94)
    out("LEG 1 -- COMMITTED build (source-identical to GXEMUL-SEC at the named baseline)")
    out("-" * 94)
    b_got, b_w, b_m, b_hit, b_dg = run_one(BASE_BIN, "base", out)
    out()

    out("-" * 94)
    out("LEG 2 -- FIX LEG (the handler decodes relative_addr; 0x3f7 declines the write)")
    out("-" * 94)
    f_got, f_w, f_m, f_hit, f_dg = run_one(FIX_BIN, "fix", out)
    out()

    out("-" * 94)
    out("RESULTS -- every value below was produced by a GUEST LOAD through real decode")
    out("-" * 94)
    out("  %-56s %-4s %-14s %-14s" % ("", "reg", "COMMITTED", "FIX LEG"))
    npass = nfail = 0
    fails = []
    changed = []
    for label, rn, wb, wf, kind in ROWS:
        gb, gf = b_got.get(rn), f_got.get(rn)
        okb, okf = (gb == wb), (gf == wf)
        npass += okb + okf
        nfail += (not okb) + (not okf)
        if not (okb and okf):
            fails.append(label)
        if wb != wf:
            changed.append((label, rn, wb, wf, gb, gf))
        out("  %-56s %-4s want %02x got %-5s want %02x got %-5s  %s"
            % (label, rn, wb, ("%02x" % gb) if gb is not None else "??",
               wf, ("%02x" % gf) if gf is not None else "??",
               "ok" if (okb and okf) else "FAIL"))
    out()
    out("  %d of %d predictions correct across both legs" % (npass, npass + nfail))
    for l in fails:
        out("  FAIL  %s" % l)
    out()

    out("-" * 94)
    out("THE DIFFERENTIAL -- the rows the defect owns.  Same script, opposite colour.")
    out("-" * 94)
    for label, rn, wb, wf, gb, gf in changed:
        out("  %-56s %-4s  %02x -> %02x   %s"
            % (label, rn, gb if gb is not None else 0, gf if gf is not None else 0,
               "AS PREDICTED" if (gb == wb and gf == wf) else "MISMATCH"))
    out()

    def hx(d, k):
        return ("%02x" % d[k]) if d.get(k) is not None else "??"

    out("  On the COMMITTED build phase 1 and phase 2 are BYTE-IDENTICAL:")
    out("    0x3f6 -> status %s, data %s   (the Device Control register)"
        % (hx(b_got, "s1"), hx(b_got, "s2")))
    out("    0x3f7 -> status %s, data %s   <-- a register the guest may not write"
        % (hx(b_got, "s4"), hx(b_got, "s5")))
    out("  On the FIX LEG they separate:")
    out("    0x3f6 -> status %s, data %s   (UNCHANGED -- the accept row)"
        % (hx(f_got, "s1"), hx(f_got, "s2")))
    out("    0x3f7 -> status %s, data %s   (the write is declined)"
        % (hx(f_got, "s4"), hx(f_got, "s5")))
    out()

    out("-" * 94)
    out("WHY THIS IS THE DEVICE AND NOT RAM  (device-signature controls)")
    out("-" * 94)
    out("  The data port was read TWICE at the SAME address and returned 0x%s then 0x%s."
        % (hx(b_got, "a1"), hx(b_got, "a2")))
    out("  A memory cell returns the last value written (0xa5) both times; only a FIFO")
    out("  returns them in push order.  This is the wdc input ring, not a memory word.")
    out("  The status byte at +7 read 0x%s at power-on and 0x%s armed.  DRDY|DSC = 0x50"
        % (hx(b_got, "a3"), hx(b_got, "s0")))
    out("  is computed by status_byte() out of diskimage_exist(), the ERR bit out of the")
    out("  d->error that dev_wdc_init sets, and DRQ out of d->write_in_progress.  The")
    out("  guest wrote none of those three, and RAM would return what was stored.")
    out("  RAM liveness (0x%s) and register liveness (0x%s%s -- #481's 0x6655 idiom)"
        % (hx(b_got, "v0"), hx(b_got, "a0"), hx(b_got, "v1")))
    out("  prove the sb/lbu shapes and the wdc decode both work, so a device row")
    out("  reading 0x00 could not have been blamed on a bad encoding.")
    out()

    out("-" * 94)
    out("EMULATOR DIAGNOSTICS DURING EACH RUN -- INFORMATIONAL, NOT EVIDENCE")
    out("-" * 94)
    out("  debug() RETURNS SILENTLY WHEN FREE-RUNNING at default verbosity (it subtracts")
    out("  1 from verbose while emul_executing and returns on v < 0), and this probe")
    out("  breakpoints and continues rather than stepping.  So every debug()-only line")
    out("  below reads 0 on BOTH legs and a zero here means nothing; only fatal() lines")
    out("  can appear.  The rows above are the measurement.")
    for n in sorted(set(list(b_dg) + list(f_dg))):
        out("  %-28s committed x%d   fix x%d" % (n, b_dg.get(n, 0), f_dg.get(n, 0)))
    out()
    out("  transcripts: %s/transcript_base.log , transcript_fix.log" % OUTDIR)
    out("  raw guest program: %s (%d bytes)" % (RAWBIN, 4 * len(prog)))
    out()

    ok = (nfail == 0 and b_hit and f_hit
          and b_w == len(prog) and f_w == len(prog))
    out("VERDICT   %s"
        % ("WITNESS CONFIRMED -- the committed build treats 0x3f7 as 0x3f6 and the fix"
           " leg separates them" if ok else
           "*** SOMETHING DID NOT HOLD -- read the FAIL lines above ***"))
    out("          %d of %d row predictions; encodings %d/%d and %d/%d; both legs"
        " parked: %s" % (npass, npass + nfail, b_w, len(prog), f_w, len(prog),
                         b_hit and f_hit))
    out("ALTOFF_DET_DONE")

    with open(os.path.join(OUTDIR, "RESULTS.txt"), "w") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
