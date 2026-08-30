"""wdcaltoffset TABLE C -- is m3's ESCAPE a real defect, or an equivalent mutant?

    python3 table_c.py <outdir> <cdrom-image> <tag>=<binary> [<tag>=<binary> ...]

*** A MUTANT THAT WILL NOT DIE IS A RESULT, NOT NOISE, and it has exactly three
explanations: the mutant is mis-built, the target is dead, or the row is mis-cut.  m3
escaped the shipped detector with a CLEAN SWEEP.  This table decides which. ***

CONTRACT -- vacuity-floor clause (e).  This probe pins ONE channel: the ATAPI
signature (cyl_lo/cyl_hi reading 0x14/0xeb), which the device returns only when
`cur_command == COMMAND_RESET` AND the attached image is a CD-ROM.  It catches
edits that let a store addressed at offset 1 set cur_command while sparing the
ring -- the shape the main detector passes at 36 of 36 row predictions.

  REQUIRES a ciR: rig.  The `c` is what makes diskimage_is_a_cdrom() true; on a
  plain disk this channel is DEAD and every row here is vacuous while still
  printing a verdict.  The L1/L2 controls exist to make that visible: if the
  legal 0x3f6 poke does not latch 14/eb, the run measured nothing.

  DOES NOT OBSERVE DRQ, the input ring, or any read of the alt region.


WHAT m3 IS.  It keeps the committed arm and guards only the destructive call:

        if (idata & WDCTL_RST) {
                d->cur_command = COMMAND_RESET;
                if (relative_addr == 0)              <-- m3 adds this
                        wdc_new_command_reset(d);
        }

so a guest store to the READ-ONLY 0x3f7 no longer purges the ring -- and STILL sets
d->cur_command = COMMAND_RESET.

WHY THE SHIPPED WITNESS CANNOT SEE IT.  Its two defect rows observe DRQ (s4) and the
input ring (s5).  Both are functions of write_in_progress and inbuf_head/tail, which
wdc_new_command_reset() clears and which m3 no longer reaches.  cur_command is not
cleared by that helper at all -- it is assigned by the CALLER -- so the shipped rows
are blind to it BY CONSTRUCTION, not by accident.

THE CHANNEL cur_command HAS.  dev_wdc.c reads COMMAND_RESET at exactly two sites, in
the wd_cyl_lo and wd_cyl_hi read arms, and both return the ATAPI signature 0xEB14 --
BUT ONLY WHEN diskimage_is_a_cdrom() is true for the selected drive.  The shipped
witness attaches a plain IDE disk, so on ITS rig the channel is dead.  That is a RIG
choice, not a property of the defect: attach the same bytes with the 'c' prefix and
the channel is live.

  L1  cyl_lo/cyl_hi round-trip 0x55/0x66 before the poke      (liveness; #481's idiom)
  L2  the 0x3f6 poke DOES latch the signature on every leg    (the channel is alive,
                                                               so a quiet 0x3f7 row is
                                                               a refusal and not a
                                                               dead path)
  D   the 0x3f7 poke latches the signature -- committed and m3 YES, fix NO

A row that shows 0x14/0xeb here is showing a guest write to a register the guest may
not write changing what two OTHER registers report.
"""
import os
import sys
import time

OUTDIR = sys.argv[1]
DISK = sys.argv[2]
LEGS = [a.split("=", 1) for a in sys.argv[3:]]

HERE = os.path.dirname(os.path.abspath(__file__))
WIT = HERE                       # the COMMITTED detector, not the frozen witness copy
os.makedirs(OUTDIR, exist_ok=True)
sys.argv = [sys.argv[0]]
sys.path.insert(0, WIT)
import wdc_altoffset_probe as W            # noqa: E402  -- the shipped encoder + Emu

#  The `c` is not cosmetic: it is what makes diskimage_is_a_cdrom() true, and the
#  ATAPI signature channel is DEAD without it.  Set through the parameter rather
#  than by shimming run_one(), which is what the measuring seat had to do.
W.DISK_PREFIX = "ciR:"

W.prog[:] = []
t0, t1, t2 = W.t0, W.t1, W.t2
v0, v1, a0, a1, a2, a3 = W.v0, W.v1, W.a0, W.a1, W.a2, W.a3
s0, s1, s2, s3 = W.s0, W.s1, W.s2, W.s3

W.emit(W.lui(t0, W.WDC_HI), "lui t0,0xb800")
W.emit(W.ori(t0, t0, W.WDC_LO), "ori t0,t0,0x01f0")
W.emit(W.lui(t1, W.ALT_HI), "lui t1,0xb800")
W.emit(W.ori(t1, t1, W.ALT_LO), "ori t1,t1,0x03f6")
W.emit(W.lui(t2, W.RAM_HI), "lui t2,0x8020")

#  RAM liveness.
W.e_store(0x55, 0, t2)
W.e_lbu(v0, 0, t2)

#  L1 -- the cylinder registers round-trip while cur_command is NOT COMMAND_RESET.
W.e_store(0xa0, W.R_SDH, t0)
W.e_store(0x55, W.R_CYL_LO, t0)
W.e_store(0x66, W.R_CYL_HI, t0)
W.e_lbu(v1, W.R_CYL_LO, t0)        # want 55 on every leg
W.e_lbu(a0, W.R_CYL_HI, t0)        # want 66 on every leg

#  D -- poke 0x3f7 with the reset bit, then read the cylinder registers again.
W.e_store(W.SRST_POKE, 1, t1)
W.e_lbu(a1, W.R_CYL_LO, t0)        # committed/m3: 14   fix: 55
W.e_lbu(a2, W.R_CYL_HI, t0)        # committed/m3: eb   fix: 66

#  L2 -- rewrite the cylinder registers, then poke 0x3f6 (the LEGAL control write).
#  Every leg must latch the signature here.  Without this row a quiet D row could be a
#  dead channel rather than a declined write.
W.e_store(0x55, W.R_CYL_LO, t0)
W.e_store(0x66, W.R_CYL_HI, t0)
W.e_lbu(a3, W.R_CYL_LO, t0)        # want 14 on EVERY leg once 0x3f6 has been poked?
#  (read BEFORE the 0x3f6 poke on the fix leg the latch is still clear from D; on the
#  committed and m3 legs it is already set.  a3 is therefore recorded, not predicted --
#  the predicted row is s0/s1 below.)
W.e_store(W.SRST_POKE, 0, t1)
W.e_store(0x55, W.R_CYL_LO, t0)
W.e_store(0x66, W.R_CYL_HI, t0)
W.e_lbu(s0, W.R_CYL_LO, t0)        # want 14 on EVERY leg
W.e_lbu(s1, W.R_CYL_HI, t0)        # want eb on EVERY leg

HALT = len(W.prog)
W.emit(W.beq(W.zero, W.zero, -1), "b 0x")
W.emit(W.NOP, "nop")
W.HALT_ADDR = W.BASE + HALT * 4
W.REGS = ("v0", "v1", "a0", "a1", "a2", "a3", "s0", "s1")

W.DISK = DISK
W.OUTDIR = OUTDIR
W.RAWBIN = os.path.join(OUTDIR, "wdcaltoff_sig.bin")
with open(W.RAWBIN, "wb") as f:
    for w, _ in W.prog:
        f.write(bytes([w & 0xff, (w >> 8) & 0xff, (w >> 16) & 0xff, (w >> 24) & 0xff]))

#  the shipped run_one() hardcodes the iR: prefix; this table needs the CD-ROM prefix,
#  so the argv is built here and run_one's body is otherwise reused via a thin shim.
_orig = W.run_one


def run_cd(binary, tag, out):
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
            seen[int(m.group(1), 16) & 0xffffffff] = (m.group(2), m.group(3).strip())
    w_ok = 0
    for i, (w, want_mn) in enumerate(W.prog):
        hit = seen.get((W.BASE + i * 4) & 0xffffffff)
        if hit and hit[0] == "%08x" % w:
            w_ok += 1
    out("  CONTROL 0 encodings: %d of %d WORDS agree with the emulator's own disassembler"
        % (w_ok, len(W.prog)))
    cd = emu.send("print cpu", wait=0.4)
    emu.send("breakpoint add 0x%x" % W.HALT_ADDR, wait=0.5)
    emu.send("continue", wait=1.0)
    import time as _t
    deadline = _t.time() + 60
    parked = False
    while _t.time() < deadline:
        emu.drain(0.5)
        #  *** MATCH THE HIT LINE, NOT THE BARE WORD. ***  This read
        #  `if "BREAKPOINT" in <tail>.upper():` until 2026-08-30, and the
        #  transcript contains the probe's OWN echoed setup command,
        #  `breakpoint add 0x...`.  The check matched its own input and could
        #  never return False.  It was right by accident in every run where the
        #  guest parked, and silently wrong in the first run where it did not:
        #  a mutant returning 0 from the device handler raises EXCEPTION_DBE, the
        #  guest re-executes the faulting store forever, and the probe still
        #  reported `breakpoint reached: True` with every register reading ??.
        #  That was scored as a KILL -- a failed run counted as a table result.
        #  The emulator prints `BREAKPOINT: pc = 0x...` on a real hit.
        if "BREAKPOINT: PC" in bytes(emu.buf[-4000:]).decode("latin1", "replace").upper():
            parked = True
            break
    out("  parked at the halt breakpoint: %s" % ("yes" if parked else "*** NO ***"))
    got = {}
    for nm in W.REGS:
        v = W.reg(emu, nm)
        got[nm] = None if v is None else (v & 0xff)
    whole = bytes(emu.buf).decode("latin1", "replace")
    iscd = "CD-ROM" in whole or "cdrom" in whole.lower()
    out("  the emulator's own startup listing calls the image a CD-ROM: %s" % iscd)
    emu.close(os.path.join(OUTDIR, "transcript_sig_%s.log" % tag))
    return got, w_ok, parked, iscd


lines = []


def out(s=""):
    lines.append(s)
    print(s)
    sys.stdout.flush()


out("=" * 100)
out("wdcaltoffset SIGNATURE detector -- the channel the DRQ/ring rows cannot see")
out("=" * 100)
out("date        %s" % time.strftime("%Y-%m-%d %H:%M:%S"))
out("instrument  %s/wdc_altoffset_probe.py encoder + Emu, IMPORTED" % WIT)
out("program     %d guest instructions" % len(W.prog))
out("rig         evbmips -e malta, image %s attached ciR:  -- the 'c' prefix is what" % DISK)
out("            makes diskimage_is_a_cdrom() true and the signature channel LIVE")
out()

res = {}
for tag, binary in LEGS:
    out("-" * 100)
    out("LEG %s   %s" % (tag, binary))
    out("-" * 100)
    got, w_ok, parked, iscd = run_cd(binary, tag, out)
    res[tag] = dict(got=got, w=w_ok, parked=parked, iscd=iscd)
    out()

out("=" * 100)
out("THE TABLE")
out("=" * 100)
NAMES = [
    ("v0", "RAM round-trip 0x55                       (liveness)", None),
    ("v1", "L1  cyl_lo round-trip BEFORE any poke", 0x55),
    ("a0", "L1  cyl_hi round-trip BEFORE any poke", 0x66),
    ("a1", "D   cyl_lo after the 0x3f7 poke", None),
    ("a2", "D   cyl_hi after the 0x3f7 poke", None),
    ("a3", "    cyl_lo re-written, read back (recorded, not predicted)", None),
    ("s0", "L2  cyl_lo after the LEGAL 0x3f6 poke", 0x14),
    ("s1", "L2  cyl_hi after the LEGAL 0x3f6 poke", 0xeb),
]
hdr = "  %-58s %-5s" % ("", "want")
for tag, _ in LEGS:
    hdr += " %-7s" % tag
out(hdr)
for rn, lab, want in NAMES:
    line = "  %-58s %-5s" % (lab, ("%02x" % want) if want is not None else "--")
    for tag, _ in LEGS:
        g = res[tag]["got"].get(rn)
        line += " %-7s" % (("%02x" % g) if g is not None else "??")
    out(line)
out()

out("=" * 100)
out("VERDICT")
out("=" * 100)
for tag, _ in LEGS:
    g = res[tag]["got"]
    sig = (g.get("a1") == 0x14 and g.get("a2") == 0xeb)
    live = (g.get("s0") == 0x14 and g.get("s1") == 0xeb)
    rt = (g.get("v1") == 0x55 and g.get("a0") == 0x66)
    out("  %-6s round-trip before any poke: %-3s   channel live (0x3f6 latches): %-3s"
        % (tag, "yes" if rt else "NO", "yes" if live else "NO"))
    out("         a store to the READ-ONLY 0x3f7 latched the ATAPI signature: %s"
        % ("YES -- DEFECT PRESENT" if sig else "no -- declined"))
out()
out("  m3 escapes the 18-row main detector at 36 of 36 row predictions.  If its D")
out("  reads 14/eb while the fix leg's reads 55/66, then m3 is NOT an equivalent mutant:")
out("  it is a real escape of a real, guest-observable consequence, and the shipped")
out("  detector is blind to it because its only two defect rows observe DRQ and the ring.")
out("ALTOFF_SIG_DONE")

with open(os.path.join(OUTDIR, "TABLE_C.txt"), "w") as f:
    f.write("\n".join(lines) + "\n")
