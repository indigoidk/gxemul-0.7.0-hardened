#!/usr/bin/env python3
"""
crime_width_probe.py BIN [LABEL] -- #529 crimewidthkill DETECTOR, rung 3, cold debugger, UNMODIFIED `-E sgi -e ip32'.

src/devices/dev_sgi_ip32.c, DEVICE_ACCESS(crime): an access whose length is neither 8 nor 4 used to reach

        fatal("crime access len = %i!\n", len);
        exit(1);

so one guest lb/lbu/lh/lhu/sb/sh anywhere in CRIME (physical 0x14000000, KSEG1 0xb4000000) ended the emulator
(witnessed 6/6 at rung 3: regress/artifacts/crimewidthkill/crime_width_witness_20260913.py).  #529 DECLINES the width
with one latched `(once)' announce and a `goto' to the function's common tail, skipping the register switch -- the
#498 sgi_de shape.  A read is answered 0 by the tail, a write is dropped, the PC advances, no exception is raised.

Every access here is a real MIPS guest instruction through real address decode and memory_rw, one `step' at a time.

CONTRACT -- the edits this detector is designed to catch (clause (e)), each MEASURED in a kill table under
artifacts/crimewidthkill/ (killtable_20260913/, killtable2_20260913/, killtable3_20260913/):
  1. the kill reinstated verbatim, or any other host death at the width arm, before or after the announce
                                                       <op> surv (six widths), hi surv, latch surv, sb08 run
  2. FAULT: the width arm returning 0 (a guest data bus error, EXCEPTION_DBE)      <op> pc, <op> exc, lb/lh/lbu/lhu v0
  3. the refused access FALLING INTO THE REGISTER SWITCH -- the goto lost, or narrowed by width, direction, or ADDRESS.
     The switch's observable arms, per refusal cell:
        CRIME_CONTROL (+0x08), writes     sb 0x01 prints the unimplemented-control fatal    sb08 msg
                                          sh 0x0800 stops every CPU (HARD_RESET)            sh08 run, sh08 pc
                                          and the arm's TESTED idata bits both ways at 2W: sh 0x0201 (DOG set,
                                          RESET clear) and sh 0x0a00 (both set)             sh08b msg, sh08b run
        CRIME_REV (+0x00), reads AND writes, from pc 0xbfc05180: the PROM-probe hack sets pc = ra (it does not test
                                          the direction)                                    lb/lh/sb/sh rev pc
        CRIME_INTMASK (+0x18), CRIME_INTSTAT (+0x10), all four cells: the arm calls crime_interrupt_reassert(),
                                          which raises cause.IP2 after a SOFTINT store   imask/istat lb, sb, lh, sh
        CRIME_TIME (+0x38), all four cells: the arm advances TIME, which the NEXT read shows   time lb, sb, lh, sh
        the default arm (any unlabelled offset): a debug() line, printed while stepping      lb/lh/sb/sh nodflt,
                                          at +0x07, +0x06, +0x1f, +0x1e and +0x27f           hi nodflt
     Each channel carries a LIVE control on an accepted width that shows it can vary:
        rev pc ctl (lw redirects), sw08 halts (sw 0x800 stops the CPUs), sw08 msg ctl (sw 0x01 prints the text),
        imask/istat pre + ctl (IP2 low after the setup; an accepted lw sets it), time lb/sb/lh/sh ctl (an accepted ld
        moves TIME), dflt ctl (lw +0x04 prints the default-arm line).
     The INTSTAT/INTMASK/TIME rows came from the pass-2 Opus seat, which MEASURED a decline narrowed to skip those
     labels passing the 40-row version of this detector 40/40 (opus_pass2_20260913/OPUS_REPORT.md); their 2-byte cells
     from the F2 pass (grok, glm): `len != 2 || relative_addr != CRIME_INTSTAT' passed the 71-row version.  So every
     observable label carries the whole {1,2} x {R,W} refusal floor (CONTROL's reads and DOG have no body: below).
     *** THE sh08 AND sw08 CHANNELS EXIST BECAUSE OF A SEPARATE DEFECT, `crimectllane' (filed): the switch matches
     CRIME_CONTROL by its exact label 0x08 and reads the RAW idata, so a 32-bit write to the high half, or a halfword at
     +0x08, carries bit 11 into HARD_RESET, while NetBSD's +0x0c write does nothing.  A round that fixes that lane
     removes or moves these channels and owes their re-derivation -- the sw08 controls will go red to say so. ***
  4. the latch removed, never set, or keyed on the access (its bit taken from len, relative_addr or writeflag --
     Opus, F2): five refused accesses in one session, a 2-byte read at an even address FIRST, owe EXACTLY ONE
     announce (latch x5); a session whose first refusal is a store owes one too (warm once)
  5. the announce: its text (`unimplemented len=N at 0xA -- declined.  (once) ]' exactly once in each width's own
     session: lb/lh/sb/sh said, hi said), and its CHANNEL -- fatal(), which prints when the guest free-runs, where a
     debug() would not (free said)
  6. the ACCEPT SET shrunk at any single cell (the de-escalation clause: the deleted exit(1) used to announce this),
     at BOTH ends of the window:  CRIME_DOG +0x30 -- acc8 st+ld (8W, 8R), acc4 rhi, acc4 rlo, acc4 wlo, acc4 whi;
     the last slot +0x278 -- top8 st+ld, top4 rhi, top4 rlo, top4 w.  Those rows are ROUND TRIPS and cannot see an
     accept arm that re-maps its register index (kimi-k3:cloud, F2: `d->reg[(relative_addr & 0x3f) / 8]' passed the
     71-row version), so one row is ANCHORED: `top8 anchor' reads bank-1 control at +0x210, a value the PRELUDE writes
     by bank index (1 for -M 64), not by the decode under test.  *** It pins the model's CURRENT bank layout, which the
     filed `crimebankorder' disputes; a round that re-orders the banks owes this row's re-derivation. ***
  7. a refused store that LANDS: CRIME_DOG seeded by an accepted sd survives a refused sb and sh     sb keeps, sh keeps;
     and at the far block, a refused sb +0x27f leaves +0x278 reading 0 (Opus, F2: a store landing only >= 0x200)
                                                                                                        hi keeps
  8. state carried ACROSS calls: a declined read after accepted reads of a nonzero register still answers 0 (an
     `odata' made static), and an accepted access between two refusals does not re-arm the announce    warm v0,
     warm once  (the codex seat, F2)

DISCLOSED, not rowed:
  * `goto crime_declined' -> `return 1' is EQUIVALENT on every channel: memory_rw pre-zeroes a device read buffer
    (#95, src/cpus/memory_rw.c -- `if (writeflag == MEM_READ)' then `memset(data, 0, len);', immediately above
    `paddr -= mem->devices[i].baseaddr;'), and on a declined access nothing between the entry and the tail writes
    HARDINT or SOFTINT, so the tail's restore and recompute are identities.  Measured 40/40 in kill table 1.
  * a fall-through confined to the two label cells whose arms have NO body for that access, both EQUIVALENT:
      CRIME_DOG (0x30)       `No warning.' -- the arm is `break;'
      CRIME_CONTROL, reads   the arm acts only on MEM_WRITE
    Each measured as a survivor in kill table 2 (`!= CRIME_DOG', the CONTROL-read-only fall-through).
  * ACCEPT cells at offsets other than +0x30, +0x210 and +0x278: an accept arm narrowed by an address strictly INSIDE
    the window (e.g. `len == 8 && relative_addr != 0x100', kill table 2's acc8mid, 71/71) is not seen.
  * an effect ADDED to the decline arm and keyed on ONE offset the switch does not name -- a refused store that lands
    only at +0x31, a declined read answering nonzero only at +0x20, a silent decline only at +0x100, a fall-through only
    at +0x40 (kimi CLI, glm, F2).  The rows pin the refusal floor at every observable LABEL and at five default-arm
    offsets; an arbitrary single offset inside a partition the body does not distinguish is clause (e) debt.
  * a fall-through only at CRIME_SOFTINT (0x20), which the switch does not name -- measured 71/71 by the Opus seat
    (F2, `sft'); it is the single-unnamed-offset class of the bullet above.
  * a FUNCTION-STATIC latch in place of `d->warned' is NOT equivalent in general -- two IP32 machines in one gxemul
    process would share it -- and this single-machine probe cannot see it (kimi-k3:cloud, F2; the pass-2 Opus seat had
    recorded it "equivalent", which holds only for one machine per process).
  * widths 3, 5, 6, 7 (no MIPS load/store issues them); the unaligned-pair instructions (lwl/lwr/swl/swr, ldl/ldr) are
    not rowed.  The RAM-size checks ABOVE the width arm (`-M 48' exits at the first CRIME access) are filed, not here.
  * independence between two CRIME instances (the latch is per instance by construction; IP32 has one CRIME).

Sentinel: CRIMEP_DONE (plus CRIMEP_RESULT=n/N and CRIMEP_CONTROL=OK|FAIL).
"""
import os, pty, re, select, signal, sys, time

BIN = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"
DUMMY = "/tmp/dummy_crimep.bin"
if not os.path.exists(DUMMY):
    with open(DUMMY, "wb") as f:
        f.write(b"\0" * 16)

CODE = 0x80001000
SCRATCH_RAM = 0xa0001800
LIVE_VAL = 0x12345678
CRIME = 0xb4000000
SENT = 0xdeadbeef
RA = 0x80004000
PROBE_PC = 0xbfc05180           # inside the CRIME_REV hack's window, (pc & 0xffffff00) == 0xbfc05100

R = {"zero": 0, "at": 1, "v0": 2, "v1": 3, "a0": 4, "a1": 5, "a2": 6, "a3": 7, "t0": 8, "t1": 9,
     "s0": 16, "s1": 17, "s2": 18, "s3": 19, "ra": 31}
OPC = {"lb": 0x20, "lh": 0x21, "lw": 0x23, "lbu": 0x24, "lhu": 0x25, "ld": 0x37,
       "sb": 0x28, "sh": 0x29, "sw": 0x2b, "sd": 0x3f}
OP_B_SELF = 0x1000ffff
OP_NOP = 0


def enc(op, rs, rt, imm=0):
    return (OPC[op] << 26) | (R[rs] << 21) | (R[rt] << 16) | (imm & 0xffff)


#  hand-assembled encodings checked against the committed witness's constants (a wrong register field reads 0, which
#  a decline's own answer would accept by accident -- so the accept rows carry nonzero wants)
assert enc("lb", "at", "v0") == 0x80220000 and enc("lhu", "at", "v0") == 0x94220000
assert enc("sb", "a3", "t0") == 0xa0e80000 and enc("sh", "a3", "t0") == 0xa4e80000
assert enc("sw", "a3", "t0") == 0xace80000 and enc("lw", "at", "v0") == 0x8c220000

rows = []


def row(name, got, want, note=""):
    ok = (got == want)
    rows.append((name, ok))
    print("%-16s %-20s %-20s %-40s %s" % (name, str(got), str(want), note, "ok" if ok else "FAIL"))
    sys.stdout.flush()


def session(cmds, settle=1.5, spin=1.2):
    """one emulator, read to the pty's EOF after `quit'.  Returns (text, clean): clean = EOF reached AND exit 0."""
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "sgi", "-e", "ip32", "-M", "64", "0x80001000:" + DUMMY])
        os._exit(127)
    buf = ""

    def rd(t):
        nonlocal buf
        end = time.time() + t
        while time.time() < end:
            r, _, _ = select.select([fd], [], [], 0.1)
            if not r:
                continue
            try:
                d = os.read(fd, 65536)
            except OSError:
                return False
            if not d:
                return False
            buf += d.decode("latin-1", "replace")
        return True

    rd(settle)
    for i, c in enumerate(cmds):
        try:
            if c == "<RUN>":        # free-run: `continue', let the guest run, then break back in with CTRL-C
                os.write(fd, b"continue\n")
                ok = rd(2.0)
                os.write(fd, b"\x03")
                ok = ok and rd(1.5)
            else:
                os.write(fd, (c + "\n").encode("latin-1"))
                ok = rd(spin if i == len(cmds) - 1 else 0.25)
        except OSError:
            break
        if not ok:
            break
    eof = True                      # a process already gone before `quit' has closed the pty; its status says how
    try:
        os.write(fd, b"quit\n")
        eof = not rd(10.0)          # to EOF, so anything printed on the way out is in the transcript
    except OSError:
        pass
    if not eof:
        try:
            os.kill(pid, signal.SIGKILL)    # a session that never reached EOF is ended, never waited on forever
        except OSError:
            pass
    try:
        os.close(fd)
    except OSError:
        pass
    how = "nostatus"
    try:
        _, stat = os.waitpid(pid, 0)
        how = ("sig%d" % os.WTERMSIG(stat)) if os.WIFSIGNALED(stat) else ("exit%d" % os.WEXITSTATUS(stat))
    except OSError:
        pass
    return buf.replace("\r", ""), (eof and how == "exit0")


def pr(t, reg):
    m = re.search(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
    return ("0x%x" % int(m.group(1), 16)) if m else "absent"


def exc(t):
    c = pr(t, "cause")
    return ("%d" % ((int(c, 16) >> 2) & 0x1f)) if c != "absent" else "absent"


def count(t, s, clean):
    """a text count is evidence only from a whole transcript: an unclean session reads `unclean', never a number"""
    return t.count(s) if clean else "unclean"


class Addr(object):
    def __init__(self, base):
        self.a = base

    def take(self, n):
        got = self.a
        self.a += 4 * (n + 2) + 0x20
        return got


def run_ops(ops, at):
    put = ["put w 0x%x, 0x%08x" % (at + 4 * i, op) for i, op in enumerate(ops)]
    put += ["put w 0x%x, 0x%08x" % (at + 4 * len(ops), OP_B_SELF),
            "put w 0x%x, 0x%08x" % (at + 4 * len(ops) + 4, OP_NOP)]
    return put + ["pc=0x%x" % at, "step %d" % len(ops)]


def ld(A, op, addr, rt, at=None):
    """one load `op rt, 0(at)', rt seeded with SENT; returns (cmds, code address)"""
    here = A.take(1) if at is None else at
    return ["at=0x%x" % addr, "%s=0x%x" % (rt, SENT)] + run_ops([enc(op, "at", rt)], here), here


def st(A, op, addr, val, at=None):
    here = A.take(1) if at is None else at
    return ["a3=0x%x" % addr, "t0=0x%x" % val] + run_ops([enc(op, "a3", "t0")], here), here


AFTER = ["print pc", "print cause"]


def roundtrip(A):
    """a RAM round trip printed in v1: absent if the host died, the sentinel if the CPU was stopped"""
    c1, _ = st(A, "sw", SCRATCH_RAM, LIVE_VAL)
    c2, _ = ld(A, "lw", SCRATCH_RAM, "v1")
    return c1 + c2 + ["print v1"]


def said(t, ln, off, clean):
    """the whole announce, `(once)' marker included -- a reworded or unmarked announce reads 0"""
    return count(t, "unimplemented len=%d at 0x%x -- declined.  (once) ]" % (ln, off), clean)


def dflt(t, clean, off, write):
    """the register switch's default-arm debug() line FOR THIS REFUSED ACCESS -- `[ crime: read from 0xOFF,' or
    `[ crime: write to 0xOFF:' -- printed while stepping, so a refused access that falls into the switch at an
    unlabelled offset says so here.  Keyed on the access's own offset and direction, because an ACCEPTED access at a
    default-arm offset in the same session prints the same kind of line (hi keeps' ld +0x278 does)."""
    if not clean:
        return "unclean"
    return t.count(("[ crime: write to 0x%x:" if write else "[ crime: read from 0x%x,") % off)


print("CRIME WIDTH PROBE (#529) -- rung 3, unmodified -E sgi -e ip32   binary=%s  label=%s" % (BIN, LABEL))
print("%-16s %-20s %-20s %-40s %s" % ("row", "got", "want", "note", ""))

# ---- CONTROLS: liveness + device signature, one session ----
A = Addr(CODE)
c = roundtrip(A)
x, _ = ld(A, "lw", CRIME + 4, "s1"); c += x
x, _ = ld(A, "lw", CRIME + 0, "s2"); c += x
t, clean = session(c + ["print s1", "print s2"])
row("live", pr(t, "v1"), "0x%x" % LIVE_VAL, "LIVENESS: RAM round trip, same apparatus")
row("devsig", pr(t, "s1"), "0x11", "CRIME_REV low half = rev 0x11: a device")
row("devsig hi", pr(t, "s2"), "0x0", "CRIME_REV high half reads 0")
row("dflt ctl", count(t, "[ crime: read from 0x4,", clean), 1, "CONTROL: default-arm text prints when stepped")

# ---- the switch channels are LIVE on an accepted width (else rows 3.x could not vary) ----
A = Addr(CODE)
x, _ = ld(A, "lw", CRIME + 0, "v0", at=PROBE_PC)
t, clean = session(["ra=0x%x" % RA] + x + AFTER)
row("rev pc ctl", pr(t, "pc"), "0x%x" % RA, "CONTROL: lw CRIME_REV from 0xbfc051xx -> ra")

A = Addr(CODE)
x, _ = st(A, "sw", CRIME + 0x08, 0x0800)
t, clean = session(x + AFTER + roundtrip(A))
row("sw08 halts", pr(t, "v1"), "0x%x" % SENT, "CONTROL: sw 0x800 +0x08 stops CPUs (crimectllane)")

A = Addr(CODE)
x, _ = st(A, "sw", CRIME + 0x08, 0x01)
t, clean = session(x + AFTER + roundtrip(A))
row("sw08 msg ctl", count(t, "CRIME_CONTROL: unimplemented", clean), 1, "CONTROL: sw 0x01 +0x08 prints the text")

# ---- ACCEPT cells on CRIME_DOG (0x030): 8W, 8R, 4R hi/lo, 4W lo/hi -- nonzero wants ----
A = Addr(CODE)
c = []
x, _ = st(A, "sd", CRIME + 0x30, 0x1122334455667788); c += x   # 8W
x, _ = ld(A, "ld", CRIME + 0x30, "a0"); c += x                  # 8R
x, _ = ld(A, "lw", CRIME + 0x30, "a1"); c += x                  # 4R high half
x, _ = ld(A, "lw", CRIME + 0x34, "a2"); c += x                  # 4R low half
x, _ = st(A, "sw", CRIME + 0x34, 0x0badcafe); c += x            # 4W low half
x, _ = ld(A, "ld", CRIME + 0x30, "s0"); c += x
x, _ = st(A, "sw", CRIME + 0x30, 0x0defaced); c += x            # 4W high half
x, _ = ld(A, "ld", CRIME + 0x30, "s3"); c += x
t, clean = session(c + ["print a0", "print a1", "print a2", "print s0", "print s3"])
row("acc8 st+ld", pr(t, "a0"), "0x1122334455667788", "8W then 8R at CRIME_DOG")
row("acc4 rhi", pr(t, "a1"), "0x11223344", "4R of the high half (+0x30)")
row("acc4 rlo", pr(t, "a2"), "0x55667788", "4R of the low half (+0x34)")
row("acc4 wlo", pr(t, "s0"), "0x112233440badcafe", "4W low half lands, high half kept")
row("acc4 whi", pr(t, "s3"), "0xdefaced0badcafe", "4W high half lands, low half kept")

# ---- REFUSED widths, one session each: value, pc, exccode, survival, own announce ----
for op, off, full in (("lb", 7, True), ("lh", 6, True), ("lbu", 7, False), ("lhu", 6, False)):
    A = Addr(CODE)
    x, here = ld(A, op, CRIME + off, "v0")
    t, clean = session(x + AFTER + ["print v0"] + roundtrip(A))
    ln = 1 if op in ("lb", "lbu") else 2
    row("%s v0" % op, pr(t, "v0"), "0x0", "declined read answers 0 (dest seeded 0x%x)" % SENT)
    if full:
        row("%s pc" % op, pr(t, "pc"), "0x%x" % (here + 4), "pc advances, no vector")
        row("%s exc" % op, exc(t), "0", "cause.ExcCode 0 (a bus error is 7)")
        row("%s said" % op, said(t, ln, off, clean), 1, "own announce, len=%d at 0x%x, once" % (ln, off))
        row("%s nodflt" % op, dflt(t, clean, off, False), 0, "switch default arm NOT reached at 0x%x" % off)
    row("%s surv" % op, pr(t, "v1"), "0x%x" % LIVE_VAL, "host survives, then a RAM trip")

for op, off, val in (("sb", 0x1f, 0xff), ("sh", 0x1e, 0xffff)):
    A = Addr(CODE)
    x, here = st(A, op, CRIME + off, val)
    t, clean = session(x + AFTER + roundtrip(A))
    ln = 1 if op == "sb" else 2
    row("%s pc" % op, pr(t, "pc"), "0x%x" % (here + 4), "pc advances, no vector")
    row("%s exc" % op, exc(t), "0", "cause.ExcCode 0 (a bus error is 7)")
    row("%s said" % op, said(t, ln, off, clean), 1, "own announce, len=%d at 0x%x, once" % (ln, off))
    row("%s nodflt" % op, dflt(t, clean, off, True), 0, "switch default arm NOT reached at 0x%x" % off)
    row("%s surv" % op, pr(t, "v1"), "0x%x" % LIVE_VAL, "host survives, then a RAM trip")

# ---- the switch is NOT entered by a refused width, per cell (contract 3) ----
A = Addr(CODE)
x, here = st(A, "sh", CRIME + 0x08, 0x0800)
t, clean = session(x + AFTER + roundtrip(A))
row("sh08 pc", pr(t, "pc"), "0x%x" % (here + 4), "2W sh 0x800 +0x08: pc advances")
row("sh08 run", pr(t, "v1"), "0x%x" % LIVE_VAL, "2W: CPUs NOT stopped (RAM trip runs)")

A = Addr(CODE)
x, here = st(A, "sb", CRIME + 0x08, 0x01)
t, clean = session(x + AFTER + roundtrip(A))
row("sb08 msg", count(t, "CRIME_CONTROL: unimplemented", clean), 0, "1W sb 0x01 +0x08: no CONTROL text")
row("sb08 run", pr(t, "v1"), "0x%x" % LIVE_VAL, "1W: the session completes (a RAM trip)")

#  THE CONTROL ARM TESTS BITS OF idata, so the 2-byte write cell owes each tested bit written both clear and set (the
#  generating-set clause; the Opus seat, F2: `relative_addr != CRIME_CONTROL || !(idata & CRIME_CONTROL_DOG_ENABLE)'
#  passed the 71-row version because no refused row carried DOG_ENABLE).  sh08 above writes HARD_RESET set / DOG clear;
#  here 0x0201 writes HARD_RESET clear / DOG set / bit 0 (the arm would print its unimplemented-control text) and 0x0a00
#  writes both set (the arm would stop every CPU).  A 1-byte write cannot carry either bit.
A = Addr(CODE)
x, _ = st(A, "sh", CRIME + 0x08, 0x0201)
y, _ = st(A, "sh", CRIME + 0x08, 0x0a00)
t, clean = session(x + y + AFTER + roundtrip(A))
row("sh08b msg", count(t, "CRIME_CONTROL: unimplemented", clean), 0, "2W sh 0x0201 +0x08 (DOG set): no CONTROL text")
row("sh08b run", pr(t, "v1"), "0x%x" % LIVE_VAL, "2W sh 0x0a00 +0x08 (DOG+RESET): CPUs NOT stopped")

for op in ("lb", "lh"):
    A = Addr(CODE)
    x, _ = ld(A, op, CRIME + 0, "v0", at=PROBE_PC)
    t, clean = session(["ra=0x%x" % RA] + x + AFTER)
    row("%s rev pc" % op, pr(t, "pc"), "0x%x" % (PROBE_PC + 4), "%dR at CRIME_REV from 0xbfc05180: pc NOT ra"
        % (1 if op == "lb" else 2))

#  the CRIME_REV arm's PROM-probe hack does not test writeflag, so the WRITE cells at +0 are side-effect cells too
for op, val in (("sb", 0xa5), ("sh", 0xa5a5)):
    A = Addr(CODE)
    x, _ = st(A, op, CRIME + 0, val, at=PROBE_PC)
    t, clean = session(["ra=0x%x" % RA] + x + AFTER)
    row("%s rev pc" % op, pr(t, "pc"), "0x%x" % (PROBE_PC + 4), "%dW at CRIME_REV from 0xbfc05180: pc NOT ra"
        % (1 if op == "sb" else 2))

# ---- the INTSTAT / INTMASK labels: their arm calls crime_interrupt_reassert(), which is NOT idempotent -- ----
#  INTMASK = bit 28 and SOFTINT = bit 28 are stored with 8-byte writes; SOFTINT's store goes to the default arm and does
#  NOT reassert, so the CPU's IP2 (cause bit 0x400) stays low until something reasserts.  A refused access at the label
#  must leave it low; the accepted `lw' that follows is the CONTROL that the arm reasserts at once.  (Measured by the
#  pass-2 Opus seat, opus_pass2_20260913/scripts/crime_p2_escape.py E1/E2: a fall-through at the label sets IP2.)
BIT = 0x10000000


def nth(t, reg, n):
    ms = re.findall(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
    return int(ms[n], 16) if len(ms) > n else None


def ip2(v):
    return "absent" if v is None else ("set" if v & 0x400 else "clear")


for lbl, off in (("imask", 0x18), ("istat", 0x10)):
    A = Addr(CODE)
    c = []
    x, _ = st(A, "sd", CRIME + 0x18, BIT); c += x
    x, _ = st(A, "sd", CRIME + 0x20, BIT); c += x
    c += ["print cause"]
    x, _ = ld(A, "lb", CRIME + off, "v0"); c += x
    c += ["print cause"]
    x, _ = st(A, "sb", CRIME + off, 0); c += x
    c += ["print cause"]
    x, _ = ld(A, "lh", CRIME + off, "v0"); c += x
    c += ["print cause"]
    x, _ = st(A, "sh", CRIME + off, 0); c += x
    c += ["print cause"]
    x, _ = ld(A, "lw", CRIME + off, "v0"); c += x
    c += ["print cause"]
    t, clean = session(c)
    row("%s pre" % lbl, ip2(nth(t, "cause", 0)), "clear", "IP2 low after SOFTINT's default-arm store")
    row("%s lb" % lbl, ip2(nth(t, "cause", 1)), "clear", "refused lb +0x%x: no reassert" % off)
    row("%s sb" % lbl, ip2(nth(t, "cause", 2)), "clear", "refused sb +0x%x: no reassert" % off)
    row("%s lh" % lbl, ip2(nth(t, "cause", 3)), "clear", "refused lh +0x%x: no reassert" % off)
    row("%s sh" % lbl, ip2(nth(t, "cause", 4)), "clear", "refused sh +0x%x: no reassert" % off)
    row("%s ctl" % lbl, ip2(nth(t, "cause", 5)), "set", "CONTROL: accepted lw +0x%x reasserts" % off)

# ---- the TIME label: an accepted read returns the value of the PREVIOUS update, then updates -- so a refused access
#  that reached crime_update_crime_time() would show in the NEXT read.  The first `ld' latches last_microseconds; on the
#  fixed build nothing else updates TIME before the next `ld' -- the device tick (machine_add_tickfunction, CRIME_TICKSHIFT
#  14) fires every 2^14 cycles and a session steps only a few dozen instructions -- so that read is far below SMALL (0.1 s
#  of TIME; each row prints its raw value -- the Opus seat's separate apparatus read 66 or 132); a fall-through at 0x38
#  makes it the wall-clock interval of the intervening debugger commands, ~1e8.  The third `ld' is the CONTROL that the
#  channel moves.  (Opus pass 2, E3; the tick-spacing wording corrected by the kimi CLI seat on the F2 pass.)
#  ASSUMPTION, disclosed: no tick boundary falls between the first `ld' and the refused access.
SMALL = 66 * 100000


def mag(v):
    return "absent" if v is None else ("small" if v < SMALL else "large")


for op in ("lb", "sb", "lh", "sh"):
    A = Addr(CODE)
    c = []
    x, _ = ld(A, "ld", CRIME + 0x38, "s0"); c += x
    if op in ("lb", "lh"):
        x, _ = ld(A, op, CRIME + 0x38, "v0"); c += x
    else:
        x, _ = st(A, op, CRIME + 0x38, 0); c += x
    x, _ = ld(A, "ld", CRIME + 0x38, "s1"); c += x
    x, _ = ld(A, "ld", CRIME + 0x38, "s2"); c += x
    t, clean = session(c + ["print s1", "print s2"])
    s1, s2 = nth(t, "s1", 0), nth(t, "s2", 0)
    row("time %s" % op, mag(s1), "small", "after refused %s +0x38 (raw %s)" % (op, s1))
    row("time %s ctl" % op, mag(s2), "large", "CONTROL: accepted ld moved TIME (raw %s)" % s2)

# ---- a refused store leaves the register it names untouched (CRIME_DOG seeded by an accepted sd) ----
A = Addr(CODE)
c = []
x, _ = st(A, "sd", CRIME + 0x30, 0x0123456789abcdef); c += x
x, _ = st(A, "sb", CRIME + 0x37, 0xa5); c += x
x, _ = ld(A, "ld", CRIME + 0x30, "a0"); c += x
x, _ = st(A, "sh", CRIME + 0x30, 0x5a5a); c += x
x, _ = ld(A, "ld", CRIME + 0x30, "a1"); c += x
#  the codex seat, F2: every other refused read runs in a COLD session, so an `odata' that survived from the previous
#  call (`static uint64_t idata = 0, odata = 0;') answered 0 there by luck.  Here a refused lbu follows accepted reads
#  of a nonzero register; and the announce count across refused-accepted-refused catches a latch re-armed by an
#  accepted access (`d->warned = 0;' in an accept arm), which `latch x5' -- no accepted access -- cannot.
x, _ = ld(A, "lbu", CRIME + 0x07, "v0"); c += x
t, clean = session(c + ["print a0", "print a1", "print v0"])
row("sb keeps", pr(t, "a0"), "0x123456789abcdef", "refused sb +0x37 leaves CRIME_DOG as seeded")
row("sh keeps", pr(t, "a1"), "0x123456789abcdef", "refused sh +0x30 leaves CRIME_DOG as seeded")
row("warm v0", pr(t, "v0"), "0x0", "refused lbu AFTER accepted reads of 0x0123..: still 0")
row("warm once", count(t, "-- declined.", clean), 1, "refused, accepted, refused: still one announce")

# ---- ACCEPT cells at the window's LAST 8-byte slot (+0x278; no case label, no prelude write) -- the far bound ----
A = Addr(CODE)
c = []
x, _ = ld(A, "ld", CRIME + 0x210, "s2"); c += x
x, _ = st(A, "sd", CRIME + 0x278, 0x0102030405060708); c += x
x, _ = ld(A, "ld", CRIME + 0x278, "a0"); c += x
x, _ = ld(A, "lw", CRIME + 0x278, "a1"); c += x
x, _ = ld(A, "lw", CRIME + 0x27c, "a2"); c += x
x, _ = st(A, "sw", CRIME + 0x27c, 0x0a0b0c0d); c += x
x, _ = st(A, "sw", CRIME + 0x278, 0x11112222); c += x
x, _ = ld(A, "ld", CRIME + 0x278, "s0"); c += x
t, clean = session(c + ["print s2", "print a0", "print a1", "print a2", "print s0"])
row("top8 anchor", pr(t, "s2"), "0x1", "8R +0x210: bank-1 ctrl the PRELUDE wrote (-M 64)")
row("top8 st+ld", pr(t, "a0"), "0x102030405060708", "8W then 8R at +0x278")
row("top4 rhi", pr(t, "a1"), "0x1020304", "4R high half at +0x278")
row("top4 rlo", pr(t, "a2"), "0x5060708", "4R low half at +0x27c")
row("top4 w", pr(t, "s0"), "0x111122220a0b0c0d", "4W both halves at +0x278/+0x27c")

# ---- a refused width at the window's LAST byte: declined, announced, default arm not reached ----
A = Addr(CODE)
x, here = st(A, "sb", CRIME + 0x27f, 0xff)
y, _ = ld(A, "ld", CRIME + 0x278, "a0")        # the refused byte's register, read back by an ACCEPTED ld
t, clean = session(x + AFTER + roundtrip(A) + y + ["print a0"])
row("hi said", said(t, 1, 0x27f, clean), 1, "sb +0x27f: own announce, once")
row("hi nodflt", dflt(t, clean, 0x27f, True), 0, "switch default arm NOT reached at 0x27f")
row("hi surv", pr(t, "v1"), "0x%x" % LIVE_VAL, "host survives, then a RAM trip")
row("hi keeps", pr(t, "a0"), "0x0", "refused sb +0x27f does not land (ld +0x278)")

# ---- FREE-RUNNING: the announce is a fatal(), so it prints when the guest is NOT single-stepped (a debug() would not) ----
A = Addr(CODE)
here = A.take(2)
c = ["at=0x%x" % (CRIME + 7), "v0=0x%x" % SENT,
     "put w 0x%x, 0x%08x" % (here, enc("lb", "at", "v0")),
     "put w 0x%x, 0x%08x" % (here + 4, OP_NOP),
     "put w 0x%x, 0x%08x" % (here + 8, OP_B_SELF),
     "put w 0x%x, 0x%08x" % (here + 12, OP_NOP),
     "pc=0x%x" % here, "<RUN>", "print v0"]
t, clean = session(c)
ran = t.split("continue", 1)[1] if "continue" in t else ""
row("free said", ran.count("unimplemented len=1 at 0x7 -- declined.  (once) ]"), 1, "free-running lb +7: announce printed")
row("free v0", pr(t, "v0"), "0x0", "free-running lb +7: declined read answers 0")

# ---- the latch: five refused accesses, one session, exactly one announce ----
A = Addr(CODE)
c = []
#  lh FIRST (Opus seat, F2): a latch whose bit is taken from the access -- `d->warned |= len' or `|= relative_addr' --
#  sets bit 0 only for a 1-byte access or an odd address, so the lh at +0x06 would leave it clear and the lb after it
#  would announce again.  With lb first, both shapes passed.
for op, off in (("lh", 6), ("lb", 7), ("lbu", 0x3f)):
    x, _ = ld(A, op, CRIME + off, "v0"); c += x
for op, off, val in (("sb", 0x37, 0xab), ("sh", 0x36, 0xabcd)):
    x, _ = st(A, op, CRIME + off, val); c += x
t, clean = session(c + roundtrip(A))
row("latch x5", count(t, "-- declined.", clean), 1, "5 refused accesses -> one (once)")
row("latch surv", pr(t, "v1"), "0x%x" % LIVE_VAL, "host survives all five")

npass = sum(1 for _, ok in rows if ok)
st_ = dict(rows)
control = all(st_.get(n, False) for n in ("live", "devsig", "devsig hi", "dflt ctl", "rev pc ctl", "sw08 halts",
                                          "sw08 msg ctl", "imask pre", "imask ctl", "istat pre", "istat ctl",
                                          "time lb ctl", "time sb ctl", "time lh ctl", "time sh ctl"))
print("")
print("FAILING: " + ", ".join(n for n, ok in rows if not ok))
print("CRIMEP_RESULT=%d/%d" % (npass, len(rows)))
print("CRIMEP_CONTROL=%s" % ("OK" if control else "FAIL"))
print("CRIMEP_DONE")
