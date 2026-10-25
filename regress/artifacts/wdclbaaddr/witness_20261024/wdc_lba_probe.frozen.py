"""wdclbaaddr -- RUNG-3 WITNESS AND DETECTOR for the wdc LBA-mode address decode.

Real guest instructions, real address decode, real memory_rw, on an UNMODIFIED
in-tree machine description (evbmips -e malta, whose committed piix4_ide path adds a
wdc whenever an IDE image is attached).  Attaching a disk image with -d is ordinary
operation, not a machine edit.

THE DEFECT (all in src/devices/dev_wdc.c at HEAD; durable keys are grep anchors):

    grep -n 'case wd_sdh:'        dev_wdc.c   -- SDH (taskfile offset 6) decodes the
        lba flag from BIT 5 on write (`d->lba = (idata >> 5) & 1;`) and recomposes it
        the same way on read (byte-exact: the four fields partition the byte).  ATA
        puts the LBA flag in BIT 6 (0x40); bits 7 and 5 are the obsolete "always 1"
        bits, so the CHS select byte is 0xa0 and the LBA select byte is 0xe0.  Under
        the HEAD decode every 0xe0 is read as head=0, and d->lba is never consulted
        for an address anyway:
    grep -n 'void wdc__read'      dev_wdc.c   -- offset = 512 * (sector - 1 +
        head*spt + heads*spt*cyl); the LBA28 alternative
        512 * (((head & 0xf) << 24) + (cyl << 8) + sector) sits inside `#if 0`.
    grep -n 'void wdc__write'     dev_wdc.c   -- the same CHS/LBA pair on the write
        side.
    grep -n '49: capabilities'    dev_wdc.c   -- IDENTIFY word 49 stays 0 this round
        (LBA is not advertised); words 3 and 6 carry heads and spt.

So a command issued in LBA mode is served from the CHS interpretation of the same
taskfile bytes.  The fix decodes lba from bit 6, keeps the readback byte-exact, and
enables the LBA28 formula at both sites.

THE VEHICLE copies regress/wdc_altoffset_probe.py: the command line and disk prefix,
the pty/expect debugger driver (print/breakpoint/continue idioms), the MIPS encoders
(I, lui, ori, addiu, sb, lbu, beq, emit) plus lhu (opcode 0x25) and sh (opcode 0x29)
added in the same style, the KSEG1 register addresses (0xb80001f0 + N: 0 data 16-bit,
2 seccnt, 3 sector, 4 cyl_lo, 5 cyl_hi, 6 SDH, 7 command/status), the per-instruction
disassembly self-check, and the row/verdict/sentinel protocol.  malta is LITTLE-endian;
the data port is read 16 bits at a time (lhu), 256 words per sector.  Every instruction
is encoded from the field layout -- never a typed-in machine-code constant.

THE DISK IMAGE (4096 sectors of 512 bytes, generated under the output dir, never the
repo):  sector n carries, as little-endian 16-bit words, word0 = n & 0xffff,
word1 = (~n) & 0xffff, word2 = 0x4c42 ("LB"), word3 = 0x4100 ("A\\0"), rest zero.  The
TAG of a sector is the pair (word0, word1) and is a DEVICE SIGNATURE: no RAM cell holds
it, so a read that returns a tag proves the bytes came through the disk model.  The
probe reads word0 and word1 and compares the combined value (word1 << 16) | word0.

THE ROWS (one fresh emulator process per session; H = IDENTIFY word 3, S = word 6):

    row            session   want on COMMITTED (HEAD)         want on FIXED
    live ram       every     0x5a5a                           0x5a5a
    id w49         identify  0x0000                            0x0000
    id geo         identify  words 3,6 nonzero                 same
    chs s1         chs       tag 0                             tag 0
    chs s2         chs       tag 1                             tag 1
    chs h1         chs       tag S                             tag S
    sdh rb         sdh       0xe5 (byte-exact readback)        0xe5
    sdh rb2        sdh       0xb3                              0xb3
    lba 70         lba       tag 69 (served as CHS sector 70)  tag 70
    lba 256        lba       tag (H*S - 1)                     tag 256
    lba 0          lba0      NOT tag 0 (served value recorded) tag 0
    lba wr         lbawr     tag 70 (write landed at sec 69)   0x7777/0x8888
    lba wr2        lbawr     0x7777/0x8888                     tag 69
    neg appar      --        a forced-mismatch line must FAIL  same

lba 70, lba 256, lba 0, lba wr, lba wr2 are the SYMPTOM rows: red on HEAD against the
FIXED wants, and BOTH wants are printed so a reader sees the sector actually served
rather than a bare FAIL.  Every other row is an identity row that must hold on both
legs.

Usage:  wdc_lba_probe.py <base_bin> <fix_bin or -> <outdir>
Leg 1 runs <base_bin> against the HEAD column; if <fix_bin> is "-" the fixed leg is
skipped (the WITNESS run, before any fix exists).  Each leg prints its rows, N/M passed,
CONTROL=PASS|FAIL; the file ends with the sentinel WDCLBA_PROBE_DONE once.  Every
session's raw transcript is kept under <outdir>/raw/<leg>_<session>.txt.  Exit status 0
only when every leg passed its own column.
"""
import os
import pty
import re
import select
import struct
import sys
import time

BASE_BIN = sys.argv[1] if len(sys.argv) > 1 else "/tmp/gxlba/base/gxemul"
FIX_ARG = sys.argv[2] if len(sys.argv) > 2 else "-"
OUTDIR = sys.argv[3] if len(sys.argv) > 3 else "/tmp/gxlba/run"

DISK_PREFIX = "iR:"                # i = IDE, R = pid-unique temporary overlay
DISK = None                        # set in main(), lives under OUTDIR
RAWDIR = None                      # OUTDIR/raw

BASE = 0xffffffff80100000          # KSEG0, physical 0x00100000, inside malta's 128 MB
WDC_HI, WDC_LO = 0xb800, 0x01f0    # wdc register file, KSEG1 0xffffffffb80001f0
RAM_HI = 0x8020                    # KSEG0 scratch (physical 0x200000) for RAM liveness

#  Register offsets from the wdc base -- src/include/thirdparty/wdcreg.h
R_DATA, R_SECCNT, R_SECTOR = 0, 2, 3
R_CYL_LO, R_CYL_HI, R_SDH = 4, 5, 6
R_STATUS = 7                       # wd_command on write, wd_status on read

WDCC_READ = 0x20                   # wdcreg.h
WDCC_WRITE = 0x30
WDCC_IDENTIFY = 0xec

SEL_CHS = 0xa0                     # CHS, drive 0, head 0 (bits 7 and 5 the obsolete 1s)
SEL_CHS_H1 = 0xa1                  # CHS, drive 0, head 1
SEL_LBA = 0xe0                     # LBA, drive 0 (high LBA nibble 0)

WR_W0, WR_W1 = 0x7777, 0x8888      # lbawr payload words 0 and 1
RAM_MAGIC = 0x5a5a

#  MIPS register numbers
zero, v0, v1, a0, a1, a2, a3 = 0, 2, 3, 4, 5, 6, 7
t0, t1, t2, t3 = 8, 9, 10, 11
t4, t5, t6 = 12, 13, 14
s0, s1, s2, s3 = 16, 17, 18, 19
NAME = {zero: "zr", v0: "v0", v1: "v1", a0: "a0", a1: "a1", a2: "a2", a3: "a3",
        t0: "t0", t1: "t1", t2: "t2", t3: "t3", t4: "t4", t5: "t5", t6: "t6",
        s0: "s0", s1: "s1", s2: "s2", s3: "s3"}


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


def lhu(rt, off, base):
    return I(0x25, base, rt, off)


def beq(rs, rt, off):
    return I(0x04, rs, rt, off)


NOP = 0

prog = []


def reset_prog():
    del prog[:]


def emit(word, mn):
    """mn is checked against the EMULATOR'S OWN disassembly.  A wrong register field
    silently yields 0, and 0 is a value several rows would accept by accident -- this
    project has shipped that mistake into a committed gate."""
    prog.append((word, mn))


def e_li(rt, v):
    emit(addiu(rt, zero, v), "addiu %s,zr,%d" % (NAME[rt], v))


def e_sb(rt, off, base):
    emit(sb(rt, off, base), "sb %s,%d(%s)" % (NAME[rt], off, NAME[base]))


def e_sh(rt, off, base):
    emit(sh(rt, off, base), "sh %s,%d(%s)" % (NAME[rt], off, NAME[base]))


def e_lbu(rt, off, base):
    emit(lbu(rt, off, base), "lbu %s,%d(%s)" % (NAME[rt], off, NAME[base]))


def e_lhu(rt, off, base):
    emit(lhu(rt, off, base), "lhu %s,%d(%s)" % (NAME[rt], off, NAME[base]))


def e_store(val, off, base):
    """Byte store of a small literal: li t3,val; sb t3,off(base)."""
    e_li(t3, val)
    e_sb(t3, off, base)


def e_push(val):
    """16-bit store to the data port: li t3,val; sh t3,0(t0)."""
    e_li(t3, val)
    e_sh(t3, R_DATA, t0)


def e_cmd(select, seccnt, sector, cyl_lo, cyl_hi, command):
    """Load the taskfile and issue a command.  The command store is LAST because it
    runs wdc_command() synchronously inside the guest's own store, so the ring is
    filled (reads) or armed (writes) before the next guest instruction executes."""
    e_store(select, R_SDH, t0)
    e_store(seccnt, R_SECCNT, t0)
    e_store(sector, R_SECTOR, t0)
    e_store(cyl_lo, R_CYL_LO, t0)
    e_store(cyl_hi, R_CYL_HI, t0)
    e_store(command, R_STATUS, t0)


def e_read_tag(rlo, rhi):
    """Pop two 16-bit words from the data-port FIFO: word0 then word1 of the tag."""
    e_lhu(rlo, R_DATA, t0)
    e_lhu(rhi, R_DATA, t0)


def e_discard(n):
    for _ in range(n):
        e_lhu(t3, R_DATA, t0)


def begin():
    """Common preamble: base registers + the RAM liveness control that every session
    carries (same sh/lhu shapes, through plain RAM), so a device row reading 0x00 can
    never be blamed on a bad encoding."""
    reset_prog()
    emit(lui(t0, WDC_HI), "lui t0,0xb800")
    emit(ori(t0, t0, WDC_LO), "ori t0,t0,0x01f0")
    emit(lui(t2, RAM_HI), "lui t2,0x8020")
    e_li(t3, RAM_MAGIC)
    e_sh(t3, 0, t2)
    e_lhu(v0, 0, t2)               # v0 = RAM round-trip of 0x5a5a


def end():
    halt = len(prog)
    emit(beq(zero, zero, -1), "b 0x")
    emit(NOP, "nop")
    return list(prog), BASE + halt * 4


def build_identify():
    begin()
    e_store(SEL_CHS, R_SDH, t0)            # select drive 0
    e_store(WDCC_IDENTIFY, R_STATUS, t0)   # ring := 256 words of IDENTIFY data
    e_discard(3)                           # words 0..2
    e_lhu(s0, R_DATA, t0)                  # word 3  = heads (H)
    e_discard(2)                           # words 4..5
    e_lhu(s1, R_DATA, t0)                  # word 6  = sectors per track (S)
    e_discard(42)                          # words 7..48
    e_lhu(s2, R_DATA, t0)                  # word 49 = capabilities (LBA bit)
    p, halt = end()
    return p, halt, {"ram": "v0", "H": "s0", "S": "s1", "w49": "s2"}


def build_chs():
    begin()
    e_cmd(SEL_CHS, 1, 1, 0, 0, WDCC_READ)      # cyl 0, sector 1 -> index 0
    e_read_tag(a0, a1)
    e_cmd(SEL_CHS, 1, 2, 0, 0, WDCC_READ)      # cyl 0, sector 2 -> index 1
    e_read_tag(a2, a3)
    e_cmd(SEL_CHS_H1, 1, 1, 0, 0, WDCC_READ)   # head 1, sector 1 -> index S
    e_read_tag(s0, s1)
    p, halt = end()
    return p, halt, {"ram": "v0", "s1_lo": "a0", "s1_hi": "a1",
                     "s2_lo": "a2", "s2_hi": "a3", "h1_lo": "s0", "h1_hi": "s1"}


def build_sdh():
    begin()
    e_store(0xe5, R_SDH, t0)
    e_lbu(s0, R_SDH, t0)                   # readback must stay byte-exact
    e_store(0xb3, R_SDH, t0)
    e_lbu(s1, R_SDH, t0)
    p, halt = end()
    return p, halt, {"ram": "v0", "rb": "s0", "rb2": "s1"}


def build_lba():
    begin()
    e_cmd(SEL_LBA, 1, 70, 0, 0, WDCC_READ)     # LBA 70
    e_read_tag(a0, a1)
    e_cmd(SEL_LBA, 1, 0, 1, 0, WDCC_READ)      # LBA 256 (sector 0, cyl_lo 1)
    e_read_tag(a2, a3)
    p, halt = end()
    return p, halt, {"ram": "v0", "l70_lo": "a0", "l70_hi": "a1",
                     "l256_lo": "a2", "l256_hi": "a3"}


def build_lba0():
    begin()
    e_cmd(SEL_LBA, 1, 0, 0, 0, WDCC_READ)      # LBA 0; HEAD serves "CHS sector 0" -- recorded, not predicted
    e_read_tag(a0, a1)
    p, halt = end()
    return p, halt, {"ram": "v0", "l0_lo": "a0", "l0_hi": "a1"}


def build_lbawr():
    begin()
    e_cmd(SEL_LBA, 1, 70, 0, 0, WDCC_WRITE)    # arm WRITE SECTORS, LBA 70
    e_push(WR_W0)                              # word 0 = 0x7777
    e_push(WR_W1)                              # word 1 = 0x8888
    for _ in range(254):                       # 254 zero words -> 512 bytes -> drain
        e_sh(zero, R_DATA, t0)
    e_cmd(SEL_CHS, 1, 71, 0, 0, WDCC_READ)     # read CHS sector 71 (index 70)
    e_read_tag(a0, a1)
    e_cmd(SEL_CHS, 1, 70, 0, 0, WDCC_READ)     # read CHS sector 70 (index 69)
    e_read_tag(a2, a3)
    p, halt = end()
    return p, halt, {"ram": "v0", "wr_lo": "a0", "wr_hi": "a1",
                     "wr2_lo": "a2", "wr2_hi": "a3"}


SESSION_ORDER = [("identify", build_identify), ("chs", build_chs),
                 ("sdh", build_sdh), ("lba", build_lba),
                 ("lba0", build_lba0), ("lbawr", build_lbawr)]


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
        end_t = time.time() + seconds
        while time.time() < end_t:
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


def run_session(binary, prog_list, halt_addr, rawbin, regmap, tag, out):
    """Run one guest program to its halt breakpoint and read back the capture regs."""
    with open(rawbin, "wb") as f:
        for w, _ in prog_list:
            f.write(bytes([w & 0xff, (w >> 8) & 0xff,
                           (w >> 16) & 0xff, (w >> 24) & 0xff]))

    argv = [binary, "-V", "-E", "evbmips", "-e", "malta",
            "-d", DISK_PREFIX + DISK, "0x%x:%s" % (BASE, rawbin)]
    out("    [%s] %s" % (tag, " ".join(argv)))
    emu = Emu(argv)

    #  CONTROL 0 -- every hand-encoded word checked against the emulator's own
    #  disassembler.  The WORD is the authoritative check; the mnemonic is a
    #  rendering and is counted separately so a spelling guessed wrong here cannot
    #  masquerade as a bad encoding.
    dwait = max(3.0, len(prog_list) * 0.03)
    dis = emu.send("unassemble 0x%x 0x%x" % (BASE, BASE + len(prog_list) * 4),
                   wait=dwait)
    seen = {}
    for line in dis.splitlines():
        m = re.match(r"^\s*([0-9a-f]{8,16}):\s+([0-9a-f]{8})\s+(?:<-)?\s*(.*)$", line)
        if m:
            seen[int(m.group(1), 16) & 0xffffffff] = (m.group(2), m.group(3).strip())
    w_ok = m_ok = 0
    bad = []
    for i, (w, want_mn) in enumerate(prog_list):
        addr = (BASE + i * 4) & 0xffffffff
        hit = seen.get(addr)
        if hit is None:
            bad.append("      BAD 0x%08x no disassembly line" % addr)
            continue
        gotw, gotmn = hit
        norm = " ".join(gotmn.replace("\t", " ").split())
        if gotw == "%08x" % w:
            w_ok += 1
        else:
            bad.append("      BAD 0x%08x word %s vs %08x" % (addr, gotw, w))
        if norm.startswith(" ".join(want_mn.split())):
            m_ok += 1
    enc_ok = (w_ok == len(prog_list))
    out("    encodings: %d/%d words, %d/%d mnemonics agree with the disassembler"
        % (w_ok, len(prog_list), m_ok, len(prog_list)))
    for l in bad[:8]:
        out(l)

    emu.send("breakpoint add 0x%x" % halt_addr, wait=0.5)
    t = time.time()
    emu.send("continue", wait=1.0)
    deadline = time.time() + 120
    hit = False
    while time.time() < deadline:
        emu.drain(0.5)
        tail = bytes(emu.buf[-4000:]).decode("latin1", "replace")
        #  Match the real hit line, not the echoed `breakpoint add` command.  The
        #  emulator prints `BREAKPOINT: pc = 0x...` on a real hit.
        if "BREAKPOINT: PC" in tail.upper():
            hit = True
            break
    out("    parked at 0x%016x: %s   (%.2f s)"
        % (halt_addr, "yes" if hit else "*** NO ***", time.time() - t))

    got = {}
    for logical, mips in regmap.items():
        v = reg(emu, mips)
        got[logical] = None if v is None else (v & 0xffff)
    emu.close(os.path.join(RAWDIR, "%s.txt" % tag))
    return got, enc_ok, hit


def gen_disk(path):
    if os.path.exists(path) and os.path.getsize(path) == 4096 * 512:
        return
    with open(path, "wb") as f:
        for n in range(4096):
            words = [n & 0xffff, (~n) & 0xffff, 0x4c42, 0x4100] + [0] * 252
            f.write(struct.pack("<256H", *words))


def TAG(n):
    """The 32-bit signature of sector n: (word1 << 16) | word0 = (~n , n)."""
    return (((~n) & 0xffff) << 16) | (n & 0xffff)


def COMB(lo, hi):
    if lo is None or hi is None:
        return None
    return (hi << 16) | lo


def show(v):
    return "0x%08x" % v if isinstance(v, int) else ("??" if v is None else str(v))


def build_rows(sess, H, S):
    """Return rows as (label, kind, got, want_head, want_fix, mode).

    mode: 'eq' got==want(column); 'nz' got is (H,S) and both nonzero;
    'neg' a forced mismatch the parser must report as FAIL (passes iff got!=want)."""
    hs = (TAG(H * S - 1)) if (H and S) else None   # lba 256 on the CHS (HEAD) decode
    wr = COMB(WR_W0, WR_W1)                         # 0x88887777, the written payload
    rows = []
    for name, _ in SESSION_ORDER:
        g = sess.get(name, {}).get("ram")
        rows.append(("ram:%s" % name, "control", g, RAM_MAGIC, RAM_MAGIC, "eq"))

    idf = sess.get("identify", {})
    rows.append(("id w49", "control", idf.get("w49"), 0x0000, 0x0000, "eq"))
    rows.append(("id geo", "control", (idf.get("H"), idf.get("S")),
                 "H,S!=0", "H,S!=0", "nz"))

    chs = sess.get("chs", {})
    rows.append(("chs s1", "control", COMB(chs.get("s1_lo"), chs.get("s1_hi")),
                 TAG(0), TAG(0), "eq"))
    rows.append(("chs s2", "control", COMB(chs.get("s2_lo"), chs.get("s2_hi")),
                 TAG(1), TAG(1), "eq"))
    rows.append(("chs h1", "control", COMB(chs.get("h1_lo"), chs.get("h1_hi")),
                 TAG(S) if S else None, TAG(S) if S else None, "eq"))

    sdh = sess.get("sdh", {})
    rows.append(("sdh rb", "control", sdh.get("rb"), 0xe5, 0xe5, "eq"))
    rows.append(("sdh rb2", "control", sdh.get("rb2"), 0xb3, 0xb3, "eq"))

    lba = sess.get("lba", {})
    rows.append(("lba 70", "symptom", COMB(lba.get("l70_lo"), lba.get("l70_hi")),
                 TAG(69), TAG(70), "eq"))
    rows.append(("lba 256", "symptom", COMB(lba.get("l256_lo"), lba.get("l256_hi")),
                 hs, TAG(256), "eq"))
    l0 = sess.get("lba0", {})
    rows.append(("lba 0", "symptom", COMB(l0.get("l0_lo"), l0.get("l0_hi")),
                 TAG(0), TAG(0), "nehead"))     # HEAD: anything but tag 0; FIX: tag 0

    lw = sess.get("lbawr", {})
    rows.append(("lba wr", "symptom", COMB(lw.get("wr_lo"), lw.get("wr_hi")),
                 TAG(70), wr, "eq"))
    rows.append(("lba wr2", "symptom", COMB(lw.get("wr2_lo"), lw.get("wr2_hi")),
                 wr, TAG(69), "eq"))

    rows.append(("neg appar", "control", 0x0001, 0x0000, 0x0000, "neg"))
    return rows


def row_ok(mode, got, want, column="HEAD"):
    if mode == "nz":
        H, S = got
        return bool(H) and bool(S) and H != 0 and S != 0
    if mode == "neg":
        return got != want          # the parser MUST report this mismatch as a FAIL
    if mode == "nehead":            # HEAD column: any served value but `want`; FIX column: exactly `want`
        if got is None:
            return False
        return got != want if column == "HEAD" else got == want
    return got == want


def run_leg(leg, binary, column, out):
    out("-" * 86)
    out("LEG %s -- %s build, judged against the %s column" % (leg, leg, column))
    out("-" * 86)
    sess = {}
    enc_all = hit_all = True
    for name, builder in SESSION_ORDER:
        prog_list, halt_addr, regmap = builder()
        got, enc_ok, hit = run_session(binary, prog_list, halt_addr,
                                       os.path.join(RAWDIR, "%s_%s.bin" % (leg, name)),
                                       regmap, "%s_%s" % (leg, name), out)
        sess[name] = got
        enc_all = enc_all and enc_ok
        hit_all = hit_all and hit
    H = sess.get("identify", {}).get("H")
    S = sess.get("identify", {}).get("S")

    out("")
    out("  %-10s %-4s %-12s %-12s %-12s" % ("row", "", "got", "head", "fix"))
    npass = nfail = 0
    ctrl_ok = True
    for label, kind, got, wh, wf, mode in build_rows(sess, H, S):
        want = wh if column == "HEAD" else wf
        ok = row_ok(mode, got, want, column)
        npass += ok
        nfail += (not ok)
        if kind == "control" and not ok:
            ctrl_ok = False
        if kind == "symptom":
            out("  %-10s %-4s %-12s head %-10s fix %-10s [%s] %s"
                % (label, "", show(got),
                   ("!=" + show(wh)) if mode == "nehead" else show(wh), show(wf),
                   column, "ok" if ok else "FAIL"))
        else:
            out("  %-10s %-4s %-12s want %-12s %s"
                % (label, "", show(got) if mode != "nz" else str(got),
                   show(want) if mode != "nz" else str(wh),
                   "ok" if ok else "FAIL"))
    out("")
    out("  %d/%d passed" % (npass, npass + nfail))
    out("  CONTROL=%s" % ("PASS" if (ctrl_ok and enc_all and hit_all) else "FAIL"))
    leg_pass = (nfail == 0 and ctrl_ok and enc_all and hit_all)
    out("  LEG %s VERDICT: %s" % (leg, "PASS" if leg_pass else "FAIL"))
    out("")
    return leg_pass


def main():
    global DISK, RAWDIR
    os.makedirs(OUTDIR, exist_ok=True)
    RAWDIR = os.path.join(OUTDIR, "raw")
    os.makedirs(RAWDIR, exist_ok=True)
    DISK = os.path.join(OUTDIR, "wdc-lba-scratch.img")
    gen_disk(DISK)

    lines = []

    def out(s=""):
        lines.append(s)
        print(s)
        sys.stdout.flush()

    out("=" * 86)
    out("wdclbaaddr -- RUNG-3 WITNESS + DETECTOR on unmodified `evbmips -e malta`")
    out("=" * 86)
    out("date      %s" % time.strftime("%Y-%m-%d %H:%M:%S"))
    out("machine   evbmips -e malta   LITTLE endian   (machine desc UNMODIFIED)")
    out("wdc       physical 0x180001f0 via bus_pci piix4_ide; KSEG1 0xffffffffb80001f0")
    out("disk      %s  (4096 sectors; tag n = (n, ~n))" % DISK)
    out("base bin  %s" % BASE_BIN)
    out("fix bin   %s" % ("(none -- WITNESS run)" if FIX_ARG == "-" else FIX_ARG))
    out("")

    legs = [("base", BASE_BIN, "HEAD")]
    if FIX_ARG != "-":
        legs.append(("fix", FIX_ARG, "FIX"))

    results = []
    for leg, binary, column in legs:
        results.append(run_leg(leg, binary, column, out))

    out("=" * 86)
    allok = all(results)
    out("VERDICT   %s" % ("every leg passed its own column" if allok
                          else "*** a leg failed -- read the FAIL lines above ***"))
    out("WDCLBA_PROBE_DONE")

    with open(os.path.join(OUTDIR, "RESULTS.txt"), "w") as f:
        f.write("\n".join(lines) + "\n")

    sys.exit(0 if allok else 1)


if __name__ == "__main__":
    main()
