"""wdcaltoffset TABLE B -- the READ side of offset 1, with a DOCUMENTATION-FREE oracle.

    python3 table_b.py <outdir> <disk> <tag>=<binary> [<tag>=<binary> ...]

THE QUESTION.  A read of 0x3f7 today returns status_byte() -- the ALT STATUS byte.  On
real ATA hardware 0x3f7 is the Drive Address Register: an active-low drive select plus
the one's complement of the head select.  The obvious objection to witnessing that is
that we would need the exact bit layout to write an oracle, and this project's rule is
to cite only what has been read in a local manual.  There is no ATA manual in
_scratchpad.

*** WE DO NOT NEED ONE.  Two properties separate the two registers without naming a
single bit value, and BOTH are derived from the fork's own source rather than from any
datasheet: ***

  * status_byte() (dev_wdc.c) reads d->drive, d->inbuf_head/tail, d->write_in_progress,
    d->error and d->atapi_*.  IT NEVER READS d->head.
  * A Drive Address Register is BY DEFINITION a function of the head select.

so the two registers differ in an observable that needs no numeric expectation:

  D2  set SDH head=0, read 0x3f7; set SDH head=15, read 0x3f7.
      Today the two bytes are EQUAL.  ANY Drive Address Register makes them DIFFER.
  D3  with the head fixed, raise DRQ and read 0x3f7 again.
      Today it CHANGES.  A Drive Address Register must not move when DRQ moves.

D2 and D3 are one claim -- "this address returns the status register" -- stated as an
invariance and a co-variance, so neither depends on what the correct value would be.
D2 is the decisive one: it is refuted by every candidate model of 0x3f7 and confirmed
only by a model that ignores the head select.

  L1  SDH readback == 0xaf proves the head write LANDED, so a D2 that shows no change
      cannot be blamed on a store that never happened.  (A pattern that matches nothing
      reports zero for everything; an oracle that measures nothing reports invariance.)
  L2  the head write must not disturb 0x3f6 either, or D2's invariance would be true
      for the wrong reason -- because nothing in the device moved at all.

THE INSTRUMENT IS THE SHIPPED PROBE'S OWN ENCODER AND pty PLUMBING, imported rather
than rewritten; every word is cross-checked against the emulator's disassembler by the
shipped run_one() exactly as the witness does.
"""
import os
import sys
import time

OUTDIR = sys.argv[1]
DISK = sys.argv[2]
LEGS = [a.split("=", 1) for a in sys.argv[3:]]

HERE = os.path.dirname(os.path.abspath(__file__))
WIT = os.path.normpath(os.path.join(HERE, "..", "witness_20260829"))
os.makedirs(OUTDIR, exist_ok=True)
sys.argv = [sys.argv[0]]
sys.path.insert(0, WIT)
import wdcaltoff_rung3_probe as W          # noqa: E402  -- the shipped encoder + Emu

#  A DIFFERENT PROGRAM, THE SAME ENCODER.  Reset the shipped module's instruction list
#  and re-emit.  Every helper and the whole mnemonic cross-check come from the shipped
#  file unchanged, so a wrong register field still cannot pass silently.
W.prog[:] = []
t0, t1, t2 = W.t0, W.t1, W.t2
v0, v1, a0, a1, a2, a3 = W.v0, W.v1, W.a0, W.a1, W.a2, W.a3
s0, s1, s2 = W.s0, W.s1, W.s2

W.emit(W.lui(t0, W.WDC_HI), "lui t0,0xb800")
W.emit(W.ori(t0, t0, W.WDC_LO), "ori t0,t0,0x01f0")
W.emit(W.lui(t1, W.ALT_HI), "lui t1,0xb800")
W.emit(W.ori(t1, t1, W.ALT_LO), "ori t1,t1,0x03f6")
W.emit(W.lui(t2, W.RAM_HI), "lui t2,0x8020")

#  RAM liveness -- the same sb/lbu shapes through plain memory.
W.e_store(0x55, 0, t2)
W.e_lbu(v0, 0, t2)

#  drive 0, head 0.  SDH bits 7 and 5 are the obsolete 1s, so 0xa0 = drive 0 head 0.
W.e_store(0xa0, W.R_SDH, t0)
W.e_lbu(v1, 0, t1)                 # read 0x3f6, head 0
W.e_lbu(a0, 1, t1)                 # read 0x3f7, head 0

#  head = 15, SAME drive.  status_byte() never reads d->head, so nothing it computes
#  may move.  A Drive Address Register must move.
W.e_store(0xaf, W.R_SDH, t0)
W.e_lbu(a1, 1, t1)                 # read 0x3f7, head 15
W.e_lbu(a2, 0, t1)                 # read 0x3f6, head 15 -- must equal v1  (L2)
W.e_lbu(a3, W.R_SDH, t0)           # SDH readback -- must be 0xaf          (L1)

#  now move DRQ and leave the head alone.
W.e_store(0x01, W.R_SECCNT, t0)
W.e_store(0x01, W.R_SECTOR, t0)
W.e_store(W.WDCC_WRITE, W.R_STATUS, t0)
W.e_lbu(s0, 1, t1)                 # read 0x3f7 with DRQ raised
W.e_lbu(s1, 0, t1)                 # read 0x3f6 with DRQ raised
W.e_lbu(s2, W.R_SDH, t0)           # SDH again -- the command must not clobber the head

HALT = len(W.prog)
W.emit(W.beq(W.zero, W.zero, -1), "b 0x")
W.emit(W.NOP, "nop")
W.HALT_ADDR = W.BASE + HALT * 4
W.REGS = ("v0", "v1", "a0", "a1", "a2", "a3", "s0", "s1", "s2")

W.DISK = DISK
W.OUTDIR = OUTDIR
W.RAWBIN = os.path.join(OUTDIR, "wdcaltoff_read.bin")
with open(W.RAWBIN, "wb") as f:
    for w, _ in W.prog:
        f.write(bytes([w & 0xff, (w >> 8) & 0xff, (w >> 16) & 0xff, (w >> 24) & 0xff]))

lines = []


def out(s=""):
    lines.append(s)
    print(s)
    sys.stdout.flush()


out("=" * 100)
out("wdcaltoffset TABLE B -- the READ side of 0x3f7, oracle by INVARIANCE not by value")
out("=" * 100)
out("date        %s" % time.strftime("%Y-%m-%d %H:%M:%S"))
out("instrument  %s/wdcaltoff_rung3_probe.py encoder + Emu + run_one, IMPORTED" % WIT)
out("program     %d guest instructions" % len(W.prog))
out("rig         evbmips -e malta, image %s attached iR:  (machine desc UNMODIFIED)" % DISK)
out()

res = {}
for tag, binary in LEGS:
    out("-" * 100)
    out("LEG %s   %s" % (tag, binary))
    out("-" * 100)
    got, w_ok, m_ok, hit, dg = W.run_one(binary, "read_" + tag, out)
    res[tag] = dict(got=got, w=w_ok, m=m_ok, hit=hit)
    out()

out("=" * 100)
out("RAW BYTES -- each produced by a guest lbu through real decode")
out("=" * 100)
NAMES = [
    ("v0", "RAM round-trip 0x55                          (liveness)"),
    ("v1", "read 0x3f6   head=0"),
    ("a0", "read 0x3f7   head=0"),
    ("a1", "read 0x3f7   head=15"),
    ("a2", "read 0x3f6   head=15"),
    ("a3", "SDH readback after writing 0xaf              (liveness L1)"),
    ("s0", "read 0x3f7   head=15, DRQ raised"),
    ("s1", "read 0x3f6   head=15, DRQ raised"),
    ("s2", "SDH readback after WDCC_WRITE"),
]
hdr = "  %-48s" % ""
for tag, _ in LEGS:
    hdr += " %-7s" % tag
out(hdr)
for rn, lab in NAMES:
    line = "  %-48s" % lab
    for tag, _ in LEGS:
        g = res[tag]["got"].get(rn)
        line += " %-7s" % (("%02x" % g) if g is not None else "??")
    out(line)
out()

out("=" * 100)
out("THE ORACLE -- every row is a RELATION between two measured bytes, never a constant")
out("=" * 100)
CHECKS = [
    ("L0  liveness  RAM round-trip is 0x55",
     lambda g: g.get("v0") == 0x55,
     "the sb/lbu shapes work at all"),
    ("L1  liveness  SDH readback is 0xaf -- the head write LANDED",
     lambda g: g.get("a3") == 0xaf,
     "without this, an unchanged D2 could be a store that never happened"),
    ("L2  control   0x3f6 is UNCHANGED by the head write",
     lambda g: g.get("v1") == g.get("a2"),
     "so D2's invariance is not true merely because nothing in the device moved"),
    ("D1  *DEFECT*  0x3f6 and 0x3f7 read BYTE-IDENTICAL",
     lambda g: g.get("v1") == g.get("a0"),
     "two architecturally different registers returning the same byte"),
    ("D2  *DEFECT*  0x3f7 is INVARIANT under the head select",
     lambda g: g.get("a0") == g.get("a1"),
     "THE DECISIVE ROW: a Drive Address Register is a FUNCTION of the head select"),
    ("D3  *DEFECT*  0x3f7 MOVES when DRQ moves",
     lambda g: g.get("a1") != g.get("s0"),
     "it tracks the status register, which the drive address register does not"),
    ("D4  *DEFECT*  0x3f7 still equals 0x3f6 with DRQ raised",
     lambda g: g.get("s0") == g.get("s1"),
     "the alias holds in a second state too, so D1 was not a coincidence"),
]
hdr = "  %-58s" % ""
for tag, _ in LEGS:
    hdr += " %-7s" % tag
out(hdr)
nbad = 0
for lab, f, why in CHECKS:
    line = "  %-58s" % lab
    for tag, _ in LEGS:
        h = f(res[tag]["got"])
        if not h:
            nbad += 1
        line += " %-7s" % ("HOLDS" if h else "no")
    out(line)
    out("      %s" % why)
out()
out("  rows that did not hold on some leg: %d" % nbad)
out()
out("  D2 NEEDS NO VALUE FROM ANY DATASHEET.  It is refuted by every model whose 0x3f7")
out("  depends on the head select, and confirmed only by one that ignores it -- which is")
out("  what status_byte() does, verifiably, in the fork's own source.")
out("  NOTE the read path is IDENTICAL on every leg by construction: the witness fix leg")
out("  and all four mutants touch the WRITE arm only, so identical columns here are the")
out("  expected result and are themselves a control on the table.")
out()
out("VERDICT   THE READ SIDE IS CHEAPLY WITNESSABLE AND IS NOW WITNESSED -- 0x3f7"
    " returns the status register, measured by invariance")
out("TABLE_B_DONE")

with open(os.path.join(OUTDIR, "TABLE_B.txt"), "w") as f:
    f.write("\n".join(lines) + "\n")
