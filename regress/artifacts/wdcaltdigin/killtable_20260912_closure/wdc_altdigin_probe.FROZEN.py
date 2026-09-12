"""wdcaltdigin -- RUNG-3 WITNESS AND KILL-TABLE DETECTOR
Unmodified in-tree machine: evbmips -e malta (PIIX4 IDE / wdc).
Access direction: READ from offset 1 (Drive Address register / digin) vs offset 0 (Alt Status).

Defect:
  DEVICE_ACCESS(wdc_altstatus) at src/devices/dev_wdc.c:609 unconditionally calculates
  odata = status_byte(d, cpu) and on MEM_READ assigns data[0] = odata without checking relative_addr.
  Offset 1 (0x3f7) incorrectly returns status byte S rather than declining the unmapped read.
"""
import os
import pty
import re
import select
import sys
import time

BINARY = sys.argv[1] if len(sys.argv) > 1 else "/tmp/gxaltdigin_clone/gxemul"
LEG = sys.argv[2] if len(sys.argv) > 2 else "HEAD"
DISK = sys.argv[3] if len(sys.argv) > 3 else "/tmp/gxaltdigin_clone/scratch_disk.img"
OUTDIR = sys.argv[4] if len(sys.argv) > 4 else "/tmp/gxaltdigin_clone/run"

BASE = 0xffffffff80100000          # KSEG0 physical 0x00100000
WDC_HI, WDC_LO = 0xb800, 0x01f0    # wdc register file, KSEG1 physical 0x180001f0
ALT_HI, ALT_LO = 0xb800, 0x03f6    # wdc_altstatus region, KSEG1 physical 0x180003f6
RAM_HI = 0x8020                    # KSEG0 scratch physical 0x00200000

# Register offsets from wdc base
R_DATA, R_SECCNT, R_SECTOR = 0, 2, 3
R_CYL_LO, R_CYL_HI, R_SDH = 4, 5, 6
R_STATUS = 7

# Status bits
DRDY, DSC, DRQ, ERR = 0x40, 0x10, 0x08, 0x01
ST_POWERON = DRDY | DSC | ERR      # 0x51
ST_IDLE = DRDY | DSC               # 0x50
ST_ARMED = DRDY | DSC | DRQ        # 0x58

WDCC_WRITE = 0x30
WDCTL_RST = 0x04
WDCTL_IDS = 0x02
SRST_POKE = WDCTL_IDS | WDCTL_RST  # 0x06
FF = 0xff

STAGE = [0x71, 0x72, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78]

zero, v0, v1, a0, a1, a2, a3 = 0, 2, 3, 4, 5, 6, 7
t0, t1, t2, t3 = 8, 9, 10, 11
t4, t5, t6, t7 = 12, 13, 14, 15   # #525 pass 2: free o32 temporaries,
                                  # needed because every result register must
                                  # hold its value until the final readback
s0, s1, s2, s3, s4, s5, s6, s7 = 16, 17, 18, 19, 20, 21, 22, 23
t8, t9 = 24, 25

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
k0, k1 = 26, 27                   # #525 pass 3: kernel temporaries; this probe
                                  # takes no exception and has no jal/jr, so both
                                  # hold their value until the final readback
NAME = {zero: "zr", v0: "v0", v1: "v1", a0: "a0", a1: "a1", a2: "a2", a3: "a3",
        t0: "t0", t1: "t1", t2: "t2", t3: "t3", s0: "s0", s1: "s1", s2: "s2",
        s3: "s3", s4: "s4", s5: "s5", s6: "s6", s7: "s7", t8: "t8", t9: "t9",
        t4: "t4", t5: "t5", t6: "t6", t7: "t7", k0: "k0", k1: "k1"}

prog = []

def emit(word, mn):
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
    e_store(0xa0, R_SDH, t0)
    e_store(0x01, R_SECCNT, t0)
    e_store(0x01, R_SECTOR, t0)
    e_store(0x00, R_CYL_LO, t0)
    e_store(0x00, R_CYL_HI, t0)
    e_store(WDCC_WRITE, R_STATUS, t0)
    for b in STAGE:
        e_store(b, R_DATA, t0)

# Instruction emission
# Setup base registers
emit(lui(t0, WDC_HI), "lui t0,0xb800")
emit(ori(t0, t0, WDC_LO), "ori t0,t0,0x01f0")
emit(lui(t1, ALT_HI), "lui t1,0xb800")
emit(ori(t1, t1, ALT_LO), "ori t1,t1,0x03f6")
emit(lui(t2, RAM_HI), "lui t2,0x8020")

# 1. Controls
# RAM liveness
e_store(0x55, 0, t2)
e_lbu(v0, 0, t2)

# Register liveness
e_store(0x55, R_CYL_LO, t0)
e_store(0x66, R_CYL_HI, t0)
e_lbu(v1, R_CYL_LO, t0)
e_lbu(a0, R_CYL_HI, t0)

# FIFO signature
e_store(0x5a, R_DATA, t0)
e_store(0xa5, R_DATA, t0)
e_lbu(a1, R_DATA, t0)
e_lbu(a2, R_DATA, t0)

# Power-on status signature
e_lbu(a3, R_STATUS, t0)

# 2. Phase R1: Altstatus reads at power-on
e_lbu(s0, 0, t1)    # offset 0 (0x3f6) -> ACCEPT: returns S=0x51
e_lbu(s1, 1, t1)    # offset 1 (0x3f7) -> CORE: HEAD returns 0x51, BASE returns 0x00

# 2a. Phase R1a (#525 PASS 3): THE 0x01 CELL -- DRDY, DSC AND DRQ ALL CLEAR.
#
#  *** PASS 2 CLOSED DRDY-CLEAR ONLY JOINTLY WITH DRQ-SET, AND A DISJUNCTION WALKED
#  STRAIGHT THROUGH THE GAP. ***  The ninth seat BUILT `&& (odata & (WDCS_DRDY |
#  WDCS_DRQ))` -- guard kept, repair nulled -- and it scored 19/19 against the
#  shipped instrument.  Every status bit WAS driven in both polarities, so a
#  PER-BIT audit passed; but the predicate is a DISJUNCTION, whose negation
#  (DRDY clear AND DRQ clear) held in NO row.  The De Morgan form the carrier
#  names: a per-lvalue test can never fire on it.
#
#  d->error = 1 at DEVINIT (dev_wdc.c) and no command has run yet to clear it, so
#  the absent slave selected HERE reads ERR alone -- 0x01.  NOT the vacuous 0x00
#  the phase further down warns about: ERR is set, so a leak is distinguishable.
#  arm_a_write() below writes 0xa0 to R_SDH first, reselecting drive 0.
e_store(0xb0, R_SDH, t0)   # select drive 1 -- the absent slave, at power-on
e_lbu(t7, R_STATUS, t0)    # +7        -> 0x01  CONTROL: ERR only, precondition landed
e_lbu(k0, 1, t1)           # offset 1  -> 0x00  CORE: M_DRDYDRQ leaks 0x01 here

# 3. Phase R2: Altstatus reads while armed
arm_a_write()
e_lbu(s2, R_STATUS, t0)  # Armed status at +7 -> 0x58 (DRQ set)
e_lbu(s3, 0, t1)         # offset 0 (0x3f6) -> ACCEPT: returns S_armed=0x58
e_lbu(s4, 1, t1)         # offset 1 (0x3f7) -> CORE: HEAD returns 0x58, BASE returns 0x00

# 4. Phase W1: WRITE to offset 0 (#481 soft reset unregressed)
e_store(SRST_POKE, 0, t1)
e_lbu(s5, R_STATUS, t0)  # DRQ cleared -> 0x50
e_lbu(k1, 1, t1)         # #525 p3: offset 1 at status 0x50 -> 0x00.  DRQ and ERR both
                         # clear, so `&& (odata & (WDCS_DRQ | WDCS_ERR))` leaks 0x50 here --
                         # the second cell of the same class, which the 0x01 row alone
                         # does NOT kill (measured 22/22 against that repair).
e_lbu(s6, R_DATA, t0)    # Ring purged -> 0xff

# 5. Phase W2: WRITE to offset 1 (#494 decline unregressed)
arm_a_write()
e_lbu(s7, R_STATUS, t0)  # Armed status -> 0x58
e_store(SRST_POKE, 1, t1)
e_lbu(t8, R_STATUS, t0)  # DRQ still set -> 0x58

# 5b. Phase S (#525 PASS 2): DRIVE THE DECLINE WITH **DRDY CLEAR**, HERE AND
#     NOWHERE ELSE -- this is the one point in the program where DRQ is MEASURED
#     set by the line immediately above (t8 == 0x58).
#
#  WHY THE PHASE EXISTS: two seats independently predicted a ONE-TOKEN TOTAL
#  ESCAPE of the 16-row instrument -- `if (odata & WDCS_DRDY) odata = 0;`.  It
#  keeps the offset guard and nulls the repair only where DRDY is CLEAR, and
#  every other row drives DRDY SET (0x51 / 0x58), so the mutant zeroes anyway and
#  is invisible BY CONSTRUCTION.  Graded a pre-ship L1, closed here not filed.
#
#  *** TWO OF MY OWN 'MEASURED REFUTATIONS' OF EARLIER PLACEMENTS WERE INVALID,
#  AND THE CAUSE WAS THIS FILE'S OWN READBACK TUPLE. ***  `REGS` below drives
#  the register readback; a row whose register is ABSENT from it is never read
#  and scores 0x00 -- which is INDISTINGUISHABLE from a device that answered
#  0x00.  t4/t5/t6 were not in REGS, so the first two placements reported
#  'status 0x00' and I recorded each as a refutation of the DEVICE STATE.  Both
#  readings were of the apparatus, not the device, and neither placement is
#  actually known to fail.  *The honest statement is that they are UNTESTED, not
#  refuted.*  What IS established, by a run with REGS repaired: this placement
#  scores 19/19 with CONTROL=OK, and the status here is 0x08.
#
#  One earlier design IS refuted, by reading rather than running: 'run a session
#  with no disk image' gives status 0x00 (dev_wdc.c:584 sets DRDY|DSC only under
#  diskimage_exist()), and a correctly DECLINED 0x00 cannot be told from a LEAKED
#  0x00.  That one is a genuine vacuity and the reason a non-zero DRDY-clear
#  status was needed at all.
#
#  THE PHASE GOES **BETWEEN t8 AND t9**, where the ring still holds staged
#  bytes.  DRQ comes from transfer state and is INDEPENDENT OF IMAGE PRESENCE;
#  the absent slave removes DRDY and DSC; wd_sdh's write path (dev_wdc.c:2006)
#  sets only sectorsize/lba/drive/head and touches neither error nor transfer
#  state.  Status is therefore 0x08 -- NON-ZERO WITH DRDY CLEAR, the whole
#  requirement.  Drive 0 is restored before t9 so the #494 row below is
#  unchanged in meaning.
e_store(0xb0, R_SDH, t0)   # select drive 1 -- the absent slave
e_lbu(t4, R_STATUS, t0)    # +7        -> 0x08  (DRQ only; DRDY and DSC CLEAR)
e_lbu(t5, 0, t1)           # offset 0  -> 0x08  ACCEPT: legal read still answers
e_lbu(t6, 1, t1)           # offset 1  -> 0x00  CORE: declined while DRDY is clear
e_store(0xa0, R_SDH, t0)   # restore drive 0 before the #494 row below
#  Under the mutant the CORE read returns 0x08, because 0x08 & WDCS_DRDY == 0
#  leaves the status byte intact.  The ACCEPT row is here on the seat's own
#  correction: without it the phase never observes offset 0 in this state, and a
#  DEAD device would satisfy the CORE row for the wrong reason.

e_lbu(t9, R_DATA, t0)    # Staged bytes intact -> 0x71

HALT = len(prog)
emit(beq(zero, zero, -1), "b 0x")
emit(NOP, "nop")
HALT_ADDR = BASE + HALT * 4

#  *** t4/t5/t6 ADDED 2026-09-11 (#525 pass 2).  A ROW WHOSE REGISTER IS ABSENT
#  FROM THIS TUPLE IS NEVER READ BACK AND SCORES AS 0x00 -- which is
#  indistinguishable from a device that answered 0x00, and cost me two wrong
#  'refutations' of my own row design before I noticed. ***
REGS = ("v0", "v1", "a0", "a1", "a2", "a3",
        "s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7", "t8", "t9",
        "t4", "t5", "t6", "t7", "k0", "k1")

ROW_DEFS = [
    ("CONTROL_RAM_LIVENESS",       "v0", 0x55, "control", "RAM byte round-trip"),
    ("CONTROL_CYL_LO_LIVENESS",    "v1", 0x55, "control", "cyl_lo readback"),
    ("CONTROL_CYL_HI_LIVENESS",    "a0", 0x66, "control", "cyl_hi readback"),
    ("CONTROL_FIFO_DEVSIG_1",      "a1", 0x5a, "control", "FIFO data port 1st read"),
    ("CONTROL_FIFO_DEVSIG_2",      "a2", 0xa5, "control", "FIFO data port 2nd read"),
    ("CONTROL_STATUS_POWERON",     "a3", ST_POWERON, "control", "Status byte at power-on (+7)"),
    ("ACCEPT_READ_OFF0_POWERON",   "s0", ST_POWERON, "accept",  "Legal offset-0 read returns S (0x51 != 0)"),
    ("CORE_READ_OFF1_POWERON",     "s1", 0x00,       "core",    "Offset-1 read declined: want 0x00 != S"),
    ("CONTROL_STATUS_PWR_SLAVE",   "t7", 0x01,       "control", "#525 p3: absent slave at power-on -- ERR only, DRDY/DSC/DRQ clear"),
    ("CORE_READ_OFF1_PWR_SLAVE",   "k0", 0x00,       "core",    "#525 p3: declined at 0x01 -- kills (odata & (DRDY|DRQ))"),
    ("CONTROL_STATUS_EMPTYSLAVE",  "t4", 0x08,       "control", "#525 p2: empty slave + armed write -- DRQ only, DRDY CLEAR"),
    ("ACCEPT_READ_OFF0_EMPTYSLAVE","t5", 0x08,       "accept",  "#525 p2: legal offset-0 read still answers 0x08"),
    ("CORE_READ_OFF1_EMPTYSLAVE",  "t6", 0x00,       "core",    "#525 p2: offset-1 declined with DRDY CLEAR -- kills the (odata & WDCS_DRDY) mutant"),
    ("CONTROL_STATUS_ARMED",       "s2", ST_ARMED,   "control", "Armed status (+7) has DRQ set (0x58)"),
    ("ACCEPT_READ_OFF0_ARMED",     "s3", ST_ARMED,   "accept",  "Legal offset-0 read returns S_armed (0x58 != 0)"),
    ("CORE_READ_OFF1_ARMED",       "s4", 0x00,       "core",    "Offset-1 read armed declined: want 0x00 != S_armed"),
    ("WRITE0_SRST_DRQ_CLEAR",      "s5", ST_IDLE,    "accept",  "#481: offset-0 SRST clears DRQ (0x50)"),
    ("WRITE0_SRST_RING_PURGED",    "s6", FF,         "accept",  "#481: offset-0 SRST purges ring (0xff)"),
    ("CORE_READ_OFF1_SRST",        "k1", 0x00,       "core",    "#525 p3: declined at 0x50 -- kills (odata & (DRQ|ERR))"),
    ("CONTROL_STATUS_ARMED_W2",    "s7", ST_ARMED,   "control", "Re-armed status for Phase W2 (0x58)"),
    ("WRITE1_DECLINE_DRQ_SET",     "t8", ST_ARMED,   "accept",  "#494: offset-1 SRST declined: DRQ still set (0x58)"),
    ("WRITE1_DECLINE_RING_INTACT", "t9", 0x71,       "accept",  "#494: offset-1 SRST declined: byte 0x71 intact"),
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

def main():
    os.makedirs(OUTDIR, exist_ok=True)
    if not os.path.isfile(DISK):
        with open(DISK, "wb") as f:
            f.write(b"\0" * (8 * 1024 * 1024))

    rawbin = os.path.join(OUTDIR, "altdigin_%s.bin" % LEG)
    with open(rawbin, "wb") as f:
        for w, _ in prog:
            f.write(bytes([w & 0xff, (w >> 8) & 0xff, (w >> 16) & 0xff, (w >> 24) & 0xff]))

    argv = [BINARY, "-V", "-E", "evbmips", "-e", "malta",
            "-d", "iR:" + DISK, "0x%x:%s" % (BASE, rawbin)]

    print("==============================================================================")
    print("wdcaltdigin Rung-3 Witness -- Leg: %s" % LEG)
    print("==============================================================================")
    print("date       %s" % time.strftime("%Y-%m-%d %H:%M:%S"))
    print("binary     %s" % BINARY)
    print("command    %s" % " ".join(argv))
    sys.stdout.flush()

    emu = Emu(argv)

    # Control 0 check
    dis = emu.send("unassemble 0x%x 0x%x" % (BASE, BASE + len(prog) * 4), wait=3.0)
    seen = {}
    for line in dis.splitlines():
        m = re.match(r"^\s*([0-9a-f]{8,16}):\s+([0-9a-f]{8})\s+(?:<-)?\s*(.*)$", line)
        if m:
            seen[int(m.group(1), 16) & 0xffffffff] = (m.group(2), m.group(3).strip())

    w_ok = 0
    for i, (w, _) in enumerate(prog):
        addr = (BASE + i * 4) & 0xffffffff
        hit = seen.get(addr)
        if hit and hit[0] == "%08x" % w:
            w_ok += 1
    print("Control 0 disassembly: %d of %d words verified match" % (w_ok, len(prog)))

    emu.send("breakpoint add 0x%x" % HALT_ADDR, wait=0.5)
    t = time.time()
    emu.send("continue", wait=1.0)
    deadline = time.time() + 60
    hit = False
    while time.time() < deadline:
        emu.drain(0.5)
        tail = bytes(emu.buf[-4000:]).decode("latin1", "replace")
        if "BREAKPOINT" in tail.upper():
            hit = True
            break
    elapsed = time.time() - t
    print("Breakpoint at 0x%x reached: %s (%.2f s)" % (HALT_ADDR, hit, elapsed))

    got = {}
    for nm in REGS:
        v = reg(emu, nm)
        got[nm] = None if v is None else (v & 0xff)

    logpath = os.path.join(OUTDIR, "transcript_%s.log" % LEG)
    emu.close(logpath)

    # Report measured S explicitly
    s_pwr = got.get("s0")
    s_arm = got.get("s3")
    off1_pwr = got.get("s1")
    off1_arm = got.get("s4")
    print("------------------------------------------------------------------------------")
    print("MEASURED STATUS & OFFSET-1 SAMPLES:")
    print("  Power-on Altstatus (off 0): S = 0x%02x (want 0x51)" % (s_pwr if s_pwr is not None else 0))
    print("  Power-on Offset 1 (off 1):  0x%02x (BASE want 0x00, HEAD defect is 0x%02x)" %
          (off1_pwr if off1_pwr is not None else 0, s_pwr if s_pwr is not None else 0))
    print("  Armed Altstatus (off 0):    S_armed = 0x%02x (want 0x58)" % (s_arm if s_arm is not None else 0))
    print("  Armed Offset 1 (off 1):     0x%02x (BASE want 0x00, HEAD defect is 0x%02x)" %
          (off1_arm if off1_arm is not None else 0, s_arm if s_arm is not None else 0))
    print("------------------------------------------------------------------------------")

    # Evaluate rows
    npass = 0
    fails = []
    print("%-28s %-4s %-8s %-8s %-6s %s" % ("ROW NAME", "REG", "WANT", "GOT", "STATUS", "DESCRIPTION"))
    print("-" * 80)
    for name, rname, want, kind, desc in ROW_DEFS:
        g = got.get(rname)
        ok = (g == want)
        if ok:
            npass += 1
        else:
            fails.append((name, rname, want, g))
        #  #525 p3: None means the register was NEVER SAMPLED.  Rendering it 0x00
        #  printed `want 0x00 got 0x00 FAIL` -- a self-contradictory line whose
        #  natural reading is "probe bug", and it cost two wrong refutations.
        gs = ("0x%02x" % g) if g is not None else "--"
        print("%-28s %-4s 0x%02x     %-8s %-6s %s" %
              (name, rname, want, gs, "PASS" if ok else "FAIL", desc))

    print("-" * 80)
    print("SCORE %d/%d" % (npass, len(ROW_DEFS)))
    #  Gate-idiom lines, matching wdc_flood_probe.py in gate_sh_rounding.sh.
    #  PRINT-ONLY: no row verdict depends on them, so the instrument the kill
    #  table measured is unchanged.
    #  Index rather than unpack: ROW_DEFS entries are 5-tuples
    #  (name, reg, want, kind, desc) and an arity assumption here would
    #  break the summary on any future column change.
    _failed = {f[0] for f in fails}
    _ctl_bad = [r[0] for r in ROW_DEFS
                if r[0].startswith("CONTROL_") and r[0] in _failed]
    print("WDC_ALTDIGIN_CONTROL=%s" % ("OK" if not _ctl_bad else "BROKEN"))
    print("WDC_ALTDIGIN_RESULT=%d/%d" % (npass, len(ROW_DEFS)))
    if fails:
        print("FAILING ROWS (%d):" % len(fails))
        for name, rname, want, g in fails:
            print("  FAIL: %s (%s) want 0x%02x got %s" % (name, rname, want,
                  ("0x%02x" % g) if g is not None else "-- (never sampled)"))
    else:
        print("ALL ROWS PASSED CLEANLY.")

    print("WDCALTDIGIN_WITNESS_DONE")

if __name__ == "__main__":
    main()
