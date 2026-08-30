"""#494 -- THE ROW THE OTHER TWO DETECTORS DO NOT HAVE.

    python3 wdc_altoffset_4bit_probe.py <outdir> <disk> <tag>=<binary> ...

WHY.  The shipped 18-row detector pokes offset 1 with exactly three values -- 0x06
(P2), 0x02 (P3) and 0x04 (P4).  ALL THREE HAVE WDCTL_4BIT (0x08) CLEAR.  So every
offset-1 row lies in ONE equivalence class on the bit-3 axis, and a guard narrowed
with `&& !(idata & WDCTL_4BIT)` keeps all 18 rows green while re-opening the defect.

That is not a hypothetical bit.  dev_wdc.c's own #481 comment says WDCTL_4BIT is
"a head-addressing mode selector that Linux libata holds as its STEADY-STATE
ap->ctl", and that comment's level-vs-edge measurement asserts SRST with 0x0e.
libata's soft reset writes ap->ctl|ATA_SRST, i.e. 0x0c, or 0x0e with nIEN.  So the
values a mask guard re-opens are the ones the commonest modern driver actually
writes, and the values the detector tests are the ones it does not.

    PHASE 5   0x0e at OFFSET 1 (0x3f7)  -- the DEFECT row this detector lacks.
              base: reset happens.  fix: declined.  A mask-guard mutant: reset
              happens again, which is the kill.

    PHASE 6   0x0e at OFFSET 0 (0x3f6)  -- the ACCEPT row for the same value.
              The de-escalation clause wants the accept side pinned for each
              predicate the old exit(1) used to gate; 0x0e is a LEGAL control
              write and every leg must still reset.  Without this row a "fix"
              that declines 0x0e everywhere would look correct.

Both phases reuse the shipped encoder and Emu by import, so the instrument is the
committed one, not a re-implementation.

CONTRACT -- vacuity-floor clause (e).

  CATCHES: MASK-shaped narrowings of the offset decline.  The other two detectors
    use only 0x06, 0x02 and 0x04 at offset 1 -- ALL THREE WITH BIT 3 CLEAR -- so
    every offset-1 row they carry sits in one WDCTL_4BIT equivalence class, and a
    guard reading `!(idata & WDCTL_4BIT)` escapes both at 36/36 and declined.
    Measured, not predicted.  P6 is the ACCEPT half and is discharged by a MEASURED
    KILL: it reds under an over-reaching decline, so a fix that refused 0x0e
    everywhere cannot pass by looking correct.

  BLIND to: everything the other two cover (partial guards sparing the ring; DRQ
    and ring channels at other values; reads of the alt region, which NO probe in
    this family pins -- the handler read path has zero rows).  Values outside 0x0e
    at offset 1, except as the other detectors already cover them.

  NOT WIRED INTO A GATE: two-leg differential, dated-exempt with its siblings.
"""
import os
import sys
import time

OUTDIR = sys.argv[1]
DISK = sys.argv[2]
LEGS = [a.split("=", 1) for a in sys.argv[3:]]

HERE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUTDIR, exist_ok=True)
sys.argv = [sys.argv[0]]
sys.path.insert(0, HERE)
import wdc_altoffset_probe as W            # noqa: E402

W.DISK_PREFIX = "iR:"                      # plain IDE: the DRQ/ring channel
LIBATA_SRST = 0x0e                         # nIEN | SRST | 4BIT

W.prog[:] = []
t0, t1, t2 = W.t0, W.t1, W.t2
v0, v1, a0 = W.v0, W.v1, W.a0
s0, s1, s2, s3, s4, s5 = W.s0, W.s1, W.s2, W.s3, W.s4, W.s5

W.emit(W.lui(t0, W.WDC_HI), "lui t0,0xb800")
W.emit(W.ori(t0, t0, W.WDC_LO), "ori t0,t0,0x01f0")
W.emit(W.lui(t1, W.ALT_HI), "lui t1,0xb800")
W.emit(W.ori(t1, t1, W.ALT_LO), "ori t1,t1,0x03f6")
W.emit(W.lui(t2, W.RAM_HI), "lui t2,0x8020")

#  liveness -- RAM, then the wdc's own decode (#481's 0x6655 idiom).
W.e_store(0x55, 0, t2)
W.e_lbu(v0, 0, t2)
W.e_store(0x55, W.R_CYL_LO, t0)
W.e_store(0x66, W.R_CYL_HI, t0)
W.e_lbu(v1, W.R_CYL_LO, t0)
W.e_lbu(a0, W.R_CYL_HI, t0)

#  PHASE 5 -- 0x0e at the READ-ONLY offset 1.
W.arm_a_write()
W.e_lbu(s0, W.R_STATUS, t0)                # armed -> DRQ set, every leg
W.e_store(LIBATA_SRST, 1, t1)              # <<< 0x3f7
W.e_lbu(s1, W.R_STATUS, t0)                # base/mask-mutant: 50   fix: 58
W.e_lbu(s2, W.R_DATA, t0)                  # base/mask-mutant: ff   fix: 71

#  PHASE 6 -- 0x0e at offset 0, the LEGAL control write.  Accept row.
W.arm_a_write()
W.e_lbu(s3, W.R_STATUS, t0)                # armed -> DRQ set, every leg
W.e_store(LIBATA_SRST, 0, t1)              # <<< 0x3f6
W.e_lbu(s4, W.R_STATUS, t0)                # EVERY leg: 50, the reset happened
W.e_lbu(s5, W.R_DATA, t0)                  # EVERY leg: ff, the ring was purged

HALT = len(W.prog)
W.emit(W.beq(W.zero, W.zero, -1), "b 0x")
W.emit(W.NOP, "nop")
W.HALT_ADDR = W.BASE + HALT * 4
W.REGS = ("v0", "v1", "a0", "s0", "s1", "s2", "s3", "s4", "s5")

W.DISK = DISK
W.OUTDIR = OUTDIR
W.RAWBIN = os.path.join(OUTDIR, "wdcaltoff_4bit.bin")
with open(W.RAWBIN, "wb") as f:
    for w, _ in W.prog:
        f.write(bytes([w & 0xff, (w >> 8) & 0xff, (w >> 16) & 0xff, (w >> 24) & 0xff]))

lines = []


def out(s=""):
    lines.append(s)
    print(s)
    sys.stdout.flush()


def run_leg(binary, tag):
    import re
    argv = [binary, "-V", "-E", "evbmips", "-e", "malta",
            "-d", W.DISK_PREFIX + DISK, "0x%x:%s" % (W.BASE, W.RAWBIN)]
    out("  command   " + " ".join(argv))
    emu = W.Emu(argv)
    dis = emu.send("unassemble 0x%x 0x%x" % (W.BASE, W.BASE + len(W.prog) * 4), wait=3.0)
    seen = {}
    for line in dis.splitlines():
        m = re.match(r"^\s*([0-9a-f]{8,16}):\s+([0-9a-f]{8})\s+(?:<-)?\s*(.*)$", line)
        if m:
            seen[int(m.group(1), 16) & 0xffffffff] = m.group(2)
    w_ok = sum(1 for i, (w, _) in enumerate(W.prog)
               if seen.get((W.BASE + i * 4) & 0xffffffff) == "%08x" % w)
    out("  CONTROL 0 encodings: %d of %d words agree with the emulator's disassembler"
        % (w_ok, len(W.prog)))
    emu.send("breakpoint add 0x%x" % W.HALT_ADDR, wait=0.5)
    emu.send("continue", wait=1.0)
    deadline = time.time() + 90
    parked = False
    while time.time() < deadline:
        emu.drain(0.5)
        if "BREAKPOINT" in bytes(emu.buf[-4000:]).decode("latin1", "replace").upper():
            parked = True
            break
    out("  parked at the halt breakpoint: %s" % ("yes" if parked else "*** NO ***"))
    got = {}
    for nm in W.REGS:
        v = W.reg(emu, nm)
        got[nm] = None if v is None else (v & 0xff)
    emu.close(os.path.join(OUTDIR, "transcript_4bit_%s.log" % tag))
    return got, w_ok, parked


out("=" * 100)
out("wdcaltoffset -- THE 0x0e ROW.  Offset-1 pokes in the shipped detector are")
out("0x06/0x02/0x04, all with WDCTL_4BIT CLEAR.  This adds the bit-3-SET value.")
out("=" * 100)
out("date        %s" % time.strftime("%Y-%m-%d %H:%M:%S"))
out("rig         evbmips -e malta (UNMODIFIED), image %s attached iR:" % DISK)
out("program     %d guest instructions" % len(W.prog))
out("value       0x%02x = WDCTL_IDS|WDCTL_RST|WDCTL_4BIT -- libata's SRST assert" % LIBATA_SRST)
out()

res = {}
for tag, binary in LEGS:
    out("-" * 100)
    out("LEG %s   %s" % (tag, binary))
    out("-" * 100)
    got, w_ok, parked = run_leg(binary, tag)
    res[tag] = dict(got=got, w=w_ok, parked=parked)
    out()

#  label, reg, want-or-None.  A `None` want is RECORDED, not predicted.
NAMES = [
    ("v0", "liveness   RAM round-trip 0x55", 0x55),
    ("v1", "liveness   cyl_lo readback (0x6655 low)", 0x55),
    ("a0", "liveness   cyl_hi readback (0x6655 high)", 0x66),
    ("s0", "P5 live    armed before the 0x3f7 0x0e poke: DRQ SET", W.ST_ARMED),
    ("s1", "P5 DEFECT  status after 0x0e at 0x3f7   (50 = reset happened)", None),
    ("s2", "P5 DEFECT  data   after 0x0e at 0x3f7   (ff = ring purged)", None),
    ("s3", "P6 live    armed before the 0x3f6 0x0e poke: DRQ SET", W.ST_ARMED),
    ("s4", "P6 ACCEPT  status after 0x0e at 0x3f6   (50 on EVERY leg)", W.ST_IDLE),
    ("s5", "P6 ACCEPT  data   after 0x0e at 0x3f6   (ff on EVERY leg)", W.FF),
]

out("=" * 100)
out("THE TABLE")
out("=" * 100)
hdr = "  %-58s %-5s" % ("", "want")
for tag, _ in LEGS:
    hdr += " %-7s" % tag
out(hdr)
npass = nfail = 0
for rn, lab, want in NAMES:
    line = "  %-58s %-5s" % (lab, ("%02x" % want) if want is not None else "--")
    for tag, _ in LEGS:
        g = res[tag]["got"].get(rn)
        line += " %-7s" % (("%02x" % g) if g is not None else "??")
        if want is not None:
            npass += (g == want)
            nfail += (g != want)
    out(line)
out()
out("  %d of %d PREDICTED cells correct (the P5 pair is recorded, not predicted --"
    % (npass, npass + nfail))
out("  it is the differential, and its whole point is that it DIFFERS by leg)")
out()

out("=" * 100)
out("VERDICT -- per leg, did a 0x0e store to the READ-ONLY 0x3f7 perform a reset?")
out("=" * 100)
for tag, _ in LEGS:
    g = res[tag]["got"]
    reset = (g.get("s1") == W.ST_IDLE and g.get("s2") == W.FF)
    declined = (g.get("s1") == W.ST_ARMED and g.get("s2") == 0x71)
    accept_ok = (g.get("s4") == W.ST_IDLE and g.get("s5") == W.FF)
    armed_ok = (g.get("s0") == W.ST_ARMED and g.get("s3") == W.ST_ARMED)
    out("  %-6s armed both phases: %-3s   ACCEPT 0x3f6 0x0e still resets: %-3s"
        % (tag, "yes" if armed_ok else "NO", "yes" if accept_ok else "NO"))
    out("         0x3f7 0x0e -> %s"
        % ("*** RESET PERFORMED -- DEFECT PRESENT ***" if reset else
           ("declined (the fix's behaviour)" if declined else
            "INDETERMINATE s1=%s s2=%s" % (g.get("s1"), g.get("s2")))))
out()
out("  If the fix leg declines and a mask-guard mutant RESETS, the shipped 18 rows")
out("  are blind to a one-clause narrowing on a bit libata holds set at all times.")
out("ALTOFF_4BIT_DONE")

with open(os.path.join(OUTDIR, "TABLE_4BIT.txt"), "w") as f:
    f.write("\n".join(lines) + "\n")
