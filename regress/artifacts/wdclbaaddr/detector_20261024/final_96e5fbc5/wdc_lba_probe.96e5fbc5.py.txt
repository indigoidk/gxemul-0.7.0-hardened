"""wdclbaaddr -- RUNG-3 WITNESS AND DETECTOR for the wdc LBA-mode address decode.

Real guest instructions, real address decode, real memory_rw, on an UNMODIFIED
in-tree machine description (evbmips -e malta, whose committed piix4_ide path adds a
wdc whenever an IDE image is attached).  Attaching a disk image with -d is ordinary
operation, not a machine edit.

THE DEFECT (all in src/devices/dev_wdc.c at HEAD; durable keys are grep anchors):

    grep -n 'case wd_sdh:'        dev_wdc.c   -- SDH (taskfile offset 6) decoded the
        lba flag from BIT 5 on write (`d->lba = (idata >> 5) & 1;`) and recomposed it
        the same way on read.  ATA puts the LBA flag in BIT 6 (0x40); bits 7 and 5 are
        the obsolete "always 1" bits, so the CHS select byte is 0xa0 and the LBA select
        byte is 0xe0.  Under HEAD's bit-5 decode every CHS select byte 0xa0 ALSO sets
        `lba = 1`, which is why the FreeBSD patch could not be taken as a patch; and
        every 0xe0 is read as head = 0.  `d->lba` reaches no address computation on
        HEAD anyway:
    grep -n 'void wdc__read'      dev_wdc.c   -- offset = 512 * (sector - 1 +
        head*spt + heads*spt*cyl); the LBA28 alternative
        512 * (((head & 0xf) << 24) + (cyl << 8) + sector) sat inside `#if 0`.
    grep -n 'void wdc__write'     dev_wdc.c   -- the same CHS/LBA pair on the write
        side.
    grep -n '49: capabilities'    dev_wdc.c   -- IDENTIFY word 49 stays 0 this round
        (LBA is implemented but not advertised); words 3 and 6 carry heads and spt.

So a command issued in LBA mode was served from the CHS interpretation of the same
taskfile bytes.  The fix decodes lba from bit 6, keeps the read-back byte-exact through
the renamed reserved field `sdh_resv`, and enables the 64-bit LBA28 formula at both
sites.

THE PRE-FIX WITNESS is the as-run copy of this probe's FIRST revision, a 19-row instrument:
regress/artifacts/wdclbaaddr/witness_20261024/wdc_lba_probe.frozen.py (md5 8f3632ff).
On the committed build, before any edit, its base leg scored 19/19 (19-row HEAD column;
RESULTS_base.txt there); after the fix the same script's fixed leg scored 19/19 (19-row
FIX column; RESULTS_fix.txt there).  THIS revision is the shipping DETECTOR (ledger row
wdclbaaddr, round #572), not the witness instrument.

THE VEHICLE copies regress/wdc_altoffset_probe.py: the command line and disk prefix,
the pty/expect debugger driver (print/breakpoint/continue idioms), the MIPS encoders
(I, lui, ori, addiu, sb, lbu, beq, emit) plus lhu (opcode 0x25), sh (opcode 0x29) and
lw (opcode 0x23) added in the same style, the KSEG1 register addresses (0xb80001f0 + N:
0 data 16-bit, 2 seccnt, 3 sector, 4 cyl_lo, 5 cyl_hi, 6 SDH, 7 command/status), the
per-instruction disassembly self-check, and the row/verdict/sentinel protocol.  malta is
LITTLE-endian; the data port is read 16 bits at a time (lhu), 256 words per sector.
Every instruction is encoded from the field layout -- never a typed-in machine-code
constant.  A tag read is two 16-bit pops stored to adjacent RAM halfwords and read back
as one 32-bit word (lw), so one capture register holds the whole (word1<<16)|word0 tag.

THE DISK IMAGE (4096 sectors of 512 bytes, generated under the output dir, never the
repo): sector n carries, as little-endian 16-bit words, word0 = n & 0xffff,
word1 = (~n) & 0xffff, word2 = 0x4c42 ("LB"), word3 = 0x4100 ("A\\0"), rest zero.  The
TAG of a sector is the pair (word0, word1) and is a DEVICE SIGNATURE: no RAM cell holds
it, so a read that returns a tag proves the bytes came through the disk model.  IDENTIFY
geometry H = 16, S = 63; logical capacity rounds up to 5040 sectors, of which 4096 are
backed.  Payload words are chosen so no written payload equals any in-range sector tag
on this image (every payload maps to n >= 4096).

THE ROWS (one fresh emulator process per session; H = IDENTIFY word 3 = 16, S = word 6 = 63;
"zeros" is 0x00000000; a payload reads back as (word1 << 16) | word0; every want is a
literal or is derived at run time from the IDENTIFY geometry the device reports -- tag S,
tag H*S, tag H*S-1, tag S+4 -- so a dead or wrong geometry read fails those rows rather
than passing them):

    session   row            HEAD (committed)             FIX
    every     ram:<session>  0x5a5a                       0x5a5a
    identify  id w49         0x0000                       0x0000
              id geo         H != 0 and S >= 10           same
    chs       chs s1 / s2    tag 0 / tag 1                same
              chs h1         tag S        (0xa1, s1)      same
              chs c1         tag H*S      (0xa0, s1, cyl_lo 1)   same
    sdh       sdh rb, rb2    0xe5, 0xb3                   same
              sdh rb3        0x4c (bits 7 and 5 clear)    same
              sdh rb0        0x00 (write 0xe5, then 0x00) same
    lba       lba 70         tag 69       (0xe0, s70)     tag 70
              lba 256        tag H*S-1    (0xe0, s0, cyl_lo 1)   tag 256
              sel 40         tag 69       (0x40, s70)     tag 70
              lba cylhi      zeros        (0xe0, s70, cyl_hi 1)  zeros
    lba0      lba 0          zeros        (0xe0, s0)      tag 0
    lbah1     lba h1         tag S+4      (0xe1, s5)      zeros (LBA 0x1000005, past the file)
              lba h1 ctl     tag 2        (0xa0, s3)      tag 2
    lbawr     five single-sector writes, then nine reads through valid CHS triples:
              lba wr         tag 70       (W 0xe0 s70; R 0xa1 s8)          payload 0x88887777
              lba wr2        payload      (R 0xa1 s7, index 69)            tag 69
              lba wr h1      payload      (W 0xe1 s5; R 0xa1 s5)           tag 67 (refused)
              lba wr h1s5    tag 5        (R 0xa0 s6)                      tag 5
              lba wr256      tag 256      (W 0xe0 s0 cyl_lo 1; R 0xa4 s5)  payload 0x33332222
              lba wr256b     payload      (R 0xaf s63, index 1007)         tag 1007
              chs wr         payload      (W+R 0xa0 s10, index 9)          payload 0x44445555
              chs wr2        tag 10       (R 0xa0 s11)                     tag 10
              lba wr cylhi   tag 71       (W 0xe0 s71 cyl_hi 1; R 0xa1 s9) tag 71 (refused)
    The sectors the write session touches -- 5, 9, 10, 67, 69, 70, 71, 256, 1007 -- are
    pairwise disjoint.  Ten SYMPTOM rows differ HEAD vs FIX; the 23 identity rows agree.

THE CONTRACT (clause e).  Kills are cited from regress/artifacts/wdclbaaddr/detector_20261024/
SCORES.txt (table 1) and SCORES2.txt (table 2): GATE mode, FIX column, 33 rows, one mutant
per scratch build.
CATCHES
  * the decode moved off bit 6, onto bit 7, or qualified with bit 5 -- V1 and V2 17/33 (the
    CHS rows, the CHS-select read-backs, sel 40, sdh rb2/rb3), V3 31/33 (sel 40, sdh rb3);
  * the LBA arm disabled, unconditional, or qualified on head, cyl or sector -- NOTE the
    applicator's V14 suffixes: V14w is the READ arm disabled and V14r the WRITE arm disabled
    (mutants572.py), the reverse of the V4r/V4w convention; the scores below follow the
    applicator -- at the read
    site V14w 28/33, V13r 19/33, V4r 32/33 (lba h1), V5r 32/33 (lba 256), V6r 31/33
    (lba 256, lba 0); at the write site V14r 28/33, V13w 31/33 (chs wr, chs wr2), V4w 32/33
    (lba wr h1), V5w and V6w 31/33 (lba wr256, lba wr256b);
  * the head term dropped, or `sector - 1`, in the LBA arm at either site -- V8 32/33
    (lba h1), V8w 32/33 (lba wr h1s5), V11 29/33 (lba 70, lba 256, sel 40, lba 0), V11w
    30/33 (lba wr, lba wr2, lba wr256); a READ-site head shift that still lands inside the
    file, k <= 11 -- V9r8 32/33 (lba h1);
  * the cyl_lo << 8-only cylinder term at either site -- V10r 32/33 (lba cylhi), V10w 32/33
    (lba wr cylhi);
  * the write-site arm placed below the write_offset capture -- V20 28/33;
  * the read-back losing bit 6, dropping reserved bit 5, or forcing bits 7 and 5 -- V18,
    V17, V16, 31/33 each (two of the four sdh rb* rows each); the verbatim pre-#572
    composition reinstated over the new decode (clause (b) at this site) -- V17v, measured
    after pass 2 (SCORES_V17v.txt);
  * word 49 advertised nonzero -- id w49 reads word 49 directly.  The one CATCHES line with
    no kill in these tables: no word-49 mutant was built here; the offline differential's
    row_no_lba_claim (regress/diff_wdc_identify.c) pins the same two bytes.
MEASURED, NOT PROMISED: the unwidened 32-bit LBA product (V15) is undefined behaviour; on
  THIS build (cc -O3) it wrapped to sector 5 and scored 32/33 (lba h1).  That score does
  not generalise: a compiler that widens the product serves zeros, exactly like the fix.
BLIND / DISCLOSED
  * cyl_hi >= 1 DESTINATIONS: both the CHS and the LBA reading fall past a 4096-sector
    image, so lba cylhi / lba wr cylhi see only the cyl_lo-only variant at each site; V7,
    the cyl_hi-conditioned arm, stays blind here (measured: 33/33 with both sites
    conditioned, SCORES_V12_V7.txt).  The larger-image row (wdclbaimage) is FILED.
  * the band LBA 4096-5039 is advertised capacity served as a short zero-filled read (the
    #416 design) while the CHS reading of the same bytes is refused -- the guest sees zeros
    either way.
  * a WRITE-site head shift (only the read site is rowed for k <= 11); head shifts that
    miss the file (k >= 12; k >= 32 undefined); `& 0xf` removed (EQUIVALENT -- the one head
    writer masks already; V12 measured 33/33, SCORES_V12_V7.txt); head-nibble values 2..15
    (every LBA-mode command here drives head 0 or 1, so a head mask narrowed to its low bit
    or bits -- `& 1`, `& 7` -- is not seen; found by three pass-2 seats, disclosed); the
    joint cells of the address fields (cyl_lo, sector, head) are SAMPLED, not exhausted --
    an arm conditioned on a joint the rows never drive (e.g. sector with cyl_lo nonzero) is
    not seen; drive 1 and big-endian guests; a sector count of 0 (the ATA encoding of 256)
    and counts above 1 -- every command here passes count 1, so `&& d->seccnt != 0` on an
    arm is not seen (Grok, pass 2); the 48-bit
    commands; the deleted printf; a past-end completion carrying no error bit (the
    wdcmediastatus row, FILED); the both-out-of-range subdomain.
  * every read-back value has bit 7 == bit 5 (0xe5, 0xb3 set; 0x4c, 0x00 clear), so a
    mutant that derives one reserved bit from the other is invisible.
ANCHOR: every LBA moved by one sector at both sites -- T_m1 26/33 (lba 70, lba 256, sel 40,
  lba 0, lba wr, lba wr2, lba wr256) and T_p1 26/33 (lba 70, lba 256, sel 40, lba 0,
  lba wr, lba wr256, lba wr cylhi).  The tags name WHICH sector was served through image
  content the decode does not produce, so position is pinned absolutely.
HARNESS SELF-CHECK (not scored): main() asserts that the comparator fails a mismatch and
  treats a missing value as a failure.  It replaces the old scored `neg appar` row, whose
  got/want were constants and which therefore passed on every run.

Usage:  wdc_lba_probe.py <base_bin> <fix_bin | GATE | -> <outdir>
    <base> -   <outdir>   WITNESS: base leg only, judged against the HEAD column.
    <base> <fix> <outdir> two legs: base vs HEAD, fix vs FIX; prints WDC_LBA_RESULT_base=
                          / _fix= and WDC_LBA_CONTROL_base= / _fix=.
    <bin>  GATE <outdir>  ONE leg vs the FIX column; prints WDC_LBA_CONTROL=OK|FAIL then
                          WDC_LBA_RESULT=p/n, then the sentinel.  Exit 0 iff p == n and
                          control OK.
The file ends with the sentinel WDCLBA_PROBE_DONE once.  Each session's raw transcript is
kept under <outdir>/raw/<leg>_<session>.txt.  Exit status 0 only when every leg passed its
own column.
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
GATE = (FIX_ARG == "GATE")

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
SEL_CHS_H4 = 0xa4                  # CHS, drive 0, head 4
SEL_CHS_H15 = 0xaf                 # CHS, drive 0, head 15
SEL_LBA = 0xe0                     # LBA, drive 0 (high LBA nibble 0)
SEL_LBA_H1 = 0xe1                  # LBA, drive 0, LBA[27:24] = 1
SEL_BIT6 = 0x40                    # bit 6 set, bits 7 and 5 CLEAR (LBA, no obsolete 1s)

RAM_MAGIC = 0x5a5a

#  MIPS register numbers
zero, v0, v1, a0, a1, a2, a3 = 0, 2, 3, 4, 5, 6, 7
t0, t1, t2, t3 = 8, 9, 10, 11
t4, t5, t6, t7 = 12, 13, 14, 15
s0, s1, s2, s3 = 16, 17, 18, 19
s4, s5, s6, s7 = 20, 21, 22, 23
NAME = {zero: "zr", v0: "v0", v1: "v1", a0: "a0", a1: "a1", a2: "a2", a3: "a3",
        t0: "t0", t1: "t1", t2: "t2", t3: "t3", t4: "t4", t5: "t5", t6: "t6",
        t7: "t7", s0: "s0", s1: "s1", s2: "s2", s3: "s3", s4: "s4", s5: "s5",
        s6: "s6", s7: "s7"}


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


def lw(rt, off, base):
    return I(0x23, base, rt, off)


def beq(rs, rt, off):
    return I(0x04, rs, rt, off)


NOP = 0

prog = []
_slot = [8]                        # next free RAM result slot (word-aligned), reset in begin()


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


def e_lw(rt, off, base):
    emit(lw(rt, off, base), "lw %s,%d(%s)" % (NAME[rt], off, NAME[base]))


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


def e_read_tag(dst):
    """Pop word0 then word1 of the tag, store them to adjacent RAM halfwords, and load
    the pair back as one 32-bit word: dst = (word1 << 16) | word0.  A fresh RAM slot
    per read keeps the stored pair inspectable and never aliased."""
    slot = _slot[0]
    _slot[0] += 4
    e_lhu(t3, R_DATA, t0)
    e_sh(t3, slot, t2)
    e_lhu(t3, R_DATA, t0)
    e_sh(t3, slot + 2, t2)
    e_lw(dst, slot, t2)


def e_write_sector(w0, w1):
    """Push a full 512-byte sector: word0, word1, then 254 zero words.  The model drains
    (writes the sector to write_offset) when 512 bytes have accumulated."""
    e_push(w0)
    e_push(w1)
    for _ in range(254):
        e_sh(zero, R_DATA, t0)


def begin():
    """Common preamble: base registers + the RAM liveness control that every session
    carries (same sh/lhu shapes, through plain RAM), so a device row reading 0x00 can
    never be blamed on a bad encoding."""
    reset_prog()
    _slot[0] = 8                   # RAM result slots start past the 0x5a5a control word
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
    for _ in range(3):
        e_lhu(t3, R_DATA, t0)              # words 0..2
    e_lhu(s0, R_DATA, t0)                  # word 3  = heads (H)
    for _ in range(2):
        e_lhu(t3, R_DATA, t0)              # words 4..5
    e_lhu(s1, R_DATA, t0)                  # word 6  = sectors per track (S)
    for _ in range(42):
        e_lhu(t3, R_DATA, t0)              # words 7..48
    e_lhu(s2, R_DATA, t0)                  # word 49 = capabilities (LBA bit)
    p, halt = end()
    return p, halt, {"ram": "v0", "H": "s0", "S": "s1", "w49": "s2"}


def build_chs():
    begin()
    e_cmd(SEL_CHS, 1, 1, 0, 0, WDCC_READ)      # cyl 0, sector 1 -> index 0
    e_read_tag(a0)
    e_cmd(SEL_CHS, 1, 2, 0, 0, WDCC_READ)      # cyl 0, sector 2 -> index 1
    e_read_tag(a1)
    e_cmd(SEL_CHS_H1, 1, 1, 0, 0, WDCC_READ)   # head 1, sector 1 -> index S
    e_read_tag(a2)
    e_cmd(SEL_CHS, 1, 1, 1, 0, WDCC_READ)      # cyl_lo 1, sector 1 -> index heads*S (N8)
    e_read_tag(a3)
    p, halt = end()
    return p, halt, {"ram": "v0", "s1": "a0", "s2": "a1", "h1": "a2", "c1": "a3"}


def build_sdh():
    begin()
    e_store(0xe5, R_SDH, t0)
    e_lbu(s0, R_SDH, t0)                   # read-back must stay byte-exact
    e_store(0xb3, R_SDH, t0)
    e_lbu(s1, R_SDH, t0)
    e_store(0x4c, R_SDH, t0)               # bits 7 and 5 CLEAR (N4)
    e_lbu(s2, R_SDH, t0)
    e_store(0xe5, R_SDH, t0)
    e_store(0x00, R_SDH, t0)               # write 0xe5 then 0x00 -> 0x00
    e_lbu(s3, R_SDH, t0)
    p, halt = end()
    return p, halt, {"ram": "v0", "rb": "s0", "rb2": "s1", "rb3": "s2", "rb0": "s3"}


def build_lba():
    begin()
    e_li(a0, 0xdead)                           # poison the capture regs before the loads
    e_li(a1, 0xdead)
    e_li(a2, 0xdead)
    e_li(a3, 0xdead)
    e_cmd(SEL_LBA, 1, 70, 0, 0, WDCC_READ)     # LBA 70
    e_read_tag(a0)
    e_cmd(SEL_LBA, 1, 0, 1, 0, WDCC_READ)      # LBA 256 (sector 0, cyl_lo 1)
    e_read_tag(a1)
    e_cmd(SEL_BIT6, 1, 70, 0, 0, WDCC_READ)    # select 0x40 -- bit 6 only (N3)
    e_read_tag(a2)
    e_cmd(SEL_LBA, 1, 70, 0, 1, WDCC_READ)     # cyl_hi 1, cyl_lo 0 -- zeros both legs
    e_read_tag(a3)
    p, halt = end()
    return p, halt, {"ram": "v0", "l70": "a0", "l256": "a1",
                     "sel40": "a2", "cylhi": "a3"}


def build_lba0():
    begin()
    e_cmd(SEL_LBA, 1, 0, 0, 0, WDCC_READ)      # LBA 0; HEAD serves "CHS sector 0" (zeros)
    e_read_tag(a0)
    p, halt = end()
    return p, halt, {"ram": "v0", "l0": "a0"}


def build_lbah1():
    begin()
    e_li(a0, 0xbeef)                           # poison the capture regs before the loads
    e_li(a1, 0xbeef)
    e_cmd(SEL_LBA_H1, 1, 5, 0, 0, WDCC_READ)   # LBA 0x1000005 (head nibble 1) -- past file
    e_read_tag(a0)
    e_cmd(SEL_CHS, 1, 3, 0, 0, WDCC_READ)      # (0xa0, s3) -> index 2, tagged both legs
    e_read_tag(a1)
    p, halt = end()
    return p, halt, {"ram": "v0", "h1": "a0", "h1ctl": "a1"}


def build_lbawr():
    begin()
    #  Five single-sector writes to pairwise-disjoint target sectors, then nine reads.
    e_cmd(SEL_LBA, 1, 70, 0, 0, WDCC_WRITE)        # HEAD CHS index 69 / FIX LBA 70
    e_write_sector(0x7777, 0x8888)
    e_cmd(SEL_LBA_H1, 1, 5, 0, 0, WDCC_WRITE)      # HEAD CHS index 67 / FIX LBA past file
    e_write_sector(0x9999, 0x6666)
    e_cmd(SEL_LBA, 1, 0, 1, 0, WDCC_WRITE)         # HEAD CHS index 1007 / FIX LBA 256
    e_write_sector(0x2222, 0x3333)
    e_cmd(SEL_CHS, 1, 10, 0, 0, WDCC_WRITE)        # CHS index 9 both legs
    e_write_sector(0x5555, 0x4444)
    e_cmd(SEL_LBA, 1, 71, 0, 1, WDCC_WRITE)        # cyl_hi 1 -- past file both legs (refused)
    e_write_sector(0x1111, 0xaaaa)

    e_cmd(SEL_CHS_H1, 1, 8, 0, 0, WDCC_READ)       # index 70
    e_read_tag(a0)
    e_cmd(SEL_CHS_H1, 1, 7, 0, 0, WDCC_READ)       # index 69
    e_read_tag(a1)
    e_cmd(SEL_CHS_H1, 1, 5, 0, 0, WDCC_READ)       # index 67
    e_read_tag(a2)
    e_cmd(SEL_CHS, 1, 6, 0, 0, WDCC_READ)          # index 5
    e_read_tag(a3)
    e_cmd(SEL_CHS_H4, 1, 5, 0, 0, WDCC_READ)       # index 256
    e_read_tag(s0)
    e_cmd(SEL_CHS_H15, 1, 63, 0, 0, WDCC_READ)     # index 1007
    e_read_tag(s1)
    e_cmd(SEL_CHS, 1, 10, 0, 0, WDCC_READ)         # index 9
    e_read_tag(s2)
    e_cmd(SEL_CHS, 1, 11, 0, 0, WDCC_READ)         # index 10
    e_read_tag(s3)
    e_cmd(SEL_CHS_H1, 1, 9, 0, 0, WDCC_READ)       # index 71
    e_read_tag(t4)
    p, halt = end()
    return p, halt, {"ram": "v0", "wr": "a0", "wr2": "a1", "wrh1": "a2",
                     "wrh1s5": "a3", "wr256": "s0", "wr256b": "s1",
                     "chswr": "s2", "chswr2": "s3", "wrcylhi": "t4"}


SESSION_ORDER = [("identify", build_identify), ("chs", build_chs),
                 ("sdh", build_sdh), ("lba", build_lba),
                 ("lba0", build_lba0), ("lbah1", build_lbah1),
                 ("lbawr", build_lbawr)]


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
            try:
                n = os.write(self.fd, view)
            except OSError:
                break
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
        got[logical] = None if v is None else (v & 0xffffffff)
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


def PAYLOAD(w0, w1):
    """The value a written payload reads back as: (word1 << 16) | word0."""
    return ((w1 & 0xffff) << 16) | (w0 & 0xffff)


def show(v):
    return "0x%08x" % v if isinstance(v, int) else ("??" if v is None else str(v))


def build_rows(sess, H, S):
    """Return rows as (label, kind, got, want_head, want_fix, mode).

    mode: 'eq' got == want(column); 'geo' got is (H,S) with H != 0 and S >= 10."""
    rows = []
    for name, _ in SESSION_ORDER:
        g = sess.get(name, {}).get("ram")
        rows.append(("ram:%s" % name, "control", g, RAM_MAGIC, RAM_MAGIC, "eq"))

    idf = sess.get("identify", {})
    rows.append(("id w49", "control", idf.get("w49"), 0x0000, 0x0000, "eq"))
    rows.append(("id geo", "control", (idf.get("H"), idf.get("S")),
                 "H!=0,S>=10", "H!=0,S>=10", "geo"))

    chs = sess.get("chs", {})
    rows.append(("chs s1", "control", chs.get("s1"), TAG(0), TAG(0), "eq"))
    rows.append(("chs s2", "control", chs.get("s2"), TAG(1), TAG(1), "eq"))
    rows.append(("chs h1", "control", chs.get("h1"),
                 TAG(S) if S else None, TAG(S) if S else None, "eq"))
    rows.append(("chs c1", "control", chs.get("c1"),
                 TAG(H * S) if (H and S) else None,
                 TAG(H * S) if (H and S) else None, "eq"))   # index heads*S (N8)

    sdh = sess.get("sdh", {})
    rows.append(("sdh rb", "control", sdh.get("rb"), 0xe5, 0xe5, "eq"))
    rows.append(("sdh rb2", "control", sdh.get("rb2"), 0xb3, 0xb3, "eq"))
    rows.append(("sdh rb3", "control", sdh.get("rb3"), 0x4c, 0x4c, "eq"))   # N4
    rows.append(("sdh rb0", "control", sdh.get("rb0"), 0x00, 0x00, "eq"))

    lba = sess.get("lba", {})
    rows.append(("lba 70", "symptom", lba.get("l70"), TAG(69), TAG(70), "eq"))
    rows.append(("lba 256", "symptom", lba.get("l256"),
                 TAG(H * S - 1) if (H and S) else None, TAG(256), "eq"))
    rows.append(("sel 40", "symptom", lba.get("sel40"), TAG(69), TAG(70), "eq"))  # N3
    rows.append(("lba cylhi", "control", lba.get("cylhi"),
                 0x00000000, 0x00000000, "eq"))              # zeros both legs (V10 variant)

    l0 = sess.get("lba0", {})
    rows.append(("lba 0", "symptom", l0.get("l0"), 0x00000000, TAG(0), "eq"))

    lh = sess.get("lbah1", {})
    rows.append(("lba h1", "symptom", lh.get("h1"), TAG(67), 0x00000000, "eq"))
    rows.append(("lba h1 ctl", "control", lh.get("h1ctl"), TAG(2), TAG(2), "eq"))

    lw_ = sess.get("lbawr", {})
    p_wr = PAYLOAD(0x7777, 0x8888)
    p_h1 = PAYLOAD(0x9999, 0x6666)
    p_256 = PAYLOAD(0x2222, 0x3333)
    p_chs = PAYLOAD(0x5555, 0x4444)
    rows.append(("lba wr", "symptom", lw_.get("wr"), TAG(70), p_wr, "eq"))
    rows.append(("lba wr2", "symptom", lw_.get("wr2"), p_wr, TAG(69), "eq"))
    rows.append(("lba wr h1", "symptom", lw_.get("wrh1"), p_h1, TAG(67), "eq"))
    rows.append(("lba wr h1s5", "control", lw_.get("wrh1s5"), TAG(5), TAG(5), "eq"))
    rows.append(("lba wr256", "symptom", lw_.get("wr256"), TAG(256), p_256, "eq"))
    rows.append(("lba wr256b", "symptom", lw_.get("wr256b"), p_256, TAG(1007), "eq"))
    rows.append(("chs wr", "control", lw_.get("chswr"), p_chs, p_chs, "eq"))
    rows.append(("chs wr2", "control", lw_.get("chswr2"), TAG(10), TAG(10), "eq"))
    rows.append(("lba wr cylhi", "control", lw_.get("wrcylhi"), TAG(71), TAG(71), "eq"))
    return rows


def row_ok(mode, got, want, column="HEAD"):
    if mode == "geo":
        #  IDENTIFY geometry: heads nonzero and S >= 10 (DETECTOR_REVISION R2).  The CHS
        #  read-back triples are the valid ones for the S = 63 geometry diskimage pins for
        #  a non-floppy image; a different geometry also reds the literal-index rows.
        if not isinstance(got, tuple):
            return False
        H, S = got
        return H is not None and S is not None and H != 0 and S >= 10
    if got is None or want is None:
        return False
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
    out("  %-12s %-12s %-12s %-12s" % ("row", "got", "head", "fix"))
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
            out("  %-12s %-12s head %-10s fix %-10s [%s] %s"
                % (label, show(got), show(wh), show(wf),
                   column, "ok" if ok else "FAIL"))
        else:
            out("  %-12s %-12s want %-12s %s"
                % (label, show(got) if mode != "geo" else str(got),
                   show(want) if mode != "geo" else str(wh),
                   "ok" if ok else "FAIL"))
    ntot = npass + nfail
    leg_ctrl = ctrl_ok and enc_all and hit_all
    out("")
    out("  %d/%d passed" % (npass, ntot))
    out("  CONTROL=%s" % ("PASS" if leg_ctrl else "FAIL"))
    leg_pass = (nfail == 0 and leg_ctrl)
    out("  LEG %s VERDICT: %s" % (leg, "PASS" if leg_pass else "FAIL"))
    out("")
    return leg_pass, npass, ntot, leg_ctrl


def main():
    global DISK, RAWDIR
    #  Harness hygiene (NOT a scored row): the comparator must FAIL a mismatch and treat
    #  a missing value as a failure.  (Replaces the old `neg appar` scored row.)
    assert row_ok("eq", 1, 0, "FIX") is False and row_ok("eq", None, 0, "FIX") is False

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
    if GATE:
        out("mode      GATE -- one leg vs the FIX column")
    else:
        out("fix bin   %s" % ("(none -- WITNESS run)" if FIX_ARG == "-" else FIX_ARG))
    out("")

    if GATE:
        legs = [("gate", BASE_BIN, "FIX")]
    else:
        legs = [("base", BASE_BIN, "HEAD")]
        if FIX_ARG != "-":
            legs.append(("fix", FIX_ARG, "FIX"))

    results = []
    for leg, binary, column in legs:
        leg_pass, npass, ntot, leg_ctrl = run_leg(leg, binary, column, out)
        results.append(leg_pass)
        if GATE:
            out("WDC_LBA_CONTROL=%s" % ("OK" if leg_ctrl else "FAIL"))
            out("WDC_LBA_RESULT=%d/%d" % (npass, ntot))
        else:
            out("WDC_LBA_CONTROL_%s=%s" % (leg, "OK" if leg_ctrl else "FAIL"))
            out("WDC_LBA_RESULT_%s=%d/%d" % (leg, npass, ntot))

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
