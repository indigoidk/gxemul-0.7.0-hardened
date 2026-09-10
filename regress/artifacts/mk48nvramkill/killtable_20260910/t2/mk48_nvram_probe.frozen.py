#!/usr/bin/env python3
"""mk48_nvram_probe.py -- the #521 DETECTOR for dev_mk48txx.c (mk48nvramkill).

PROVENANCE.  This is the round's rung-3 WITNESS, shipped as its detector with
exactly ONE row inverted (see "msg silent" below).  The witness as run is
preserved unmodified at
    regress/artifacts/mk48nvramkill/opus_mk48_nvram_witness_20260910.py
and scored 15/47 on the committed build and 46/47 after the fix; the 46th was
that one row, which by construction cannot be green on a fixed build.  This
file therefore scores 47/47 post-fix and 14/47 pre-fix.


DEFECT.  DEVICE_ACCESS(mk48txx) accepts everything outside
[MK48T08_CLKOFF, MK48T08_CLKOFF + MK48TXX_ISEC) = [0x1ff0, 0x1ff9) via an early
`goto ret'.  The switch it then reaches holds exactly ONE case,
MK48T08_CLKOFF + MK48TXX_ICSR = 0x1ff8.  The other EIGHT offsets 0x1ff0..0x1ff7
fall to `default:' -> fatal() -> exit(1), in BOTH directions.

CONSTANTS VERIFIED IN-TREE (src/include/thirdparty/mk48txxreg.h):
    MK48T08_CLKSZ  8192 (=MK48TXX_LEN, the registration length)
    MK48T08_CLKOFF 0x1ff0      MK48TXX_ICSR 8      MK48TXX_ISEC 9
Attach: src/machines/machine_mvme88k.c, MVME187 subtype, "mk48txx addr=0xfffc0000".
So the killing guest physical addresses are 0xfffc1ff0 .. 0xfffc1ff7.

REACHABILITY -- WHY THE CENSUS IS ALL EIGHT, NOT THE PCC2 SUBSET.  dev_pcc2.c's
width kills were half-unreachable because a non-byte m88k access is alignment-checked
before memory_rw.  Here the killing accesses are BYTE accesses: cpu_m88k_instr.c
decodes op26 0x03 as ld.bu (opsize 0) and 0x0b as st.b (opsize 0), and
cpu_m88k_instr_loadstore.c guards its alignment check with `#ifndef LS_1', so a
size-1 access is never alignment-checked.  Every one of the eight offsets is
guest-reachable in BOTH directions: 16 killing accesses, and the full census is free.

RUNG 3: real MC88100 instructions executed by the CPU through real address decode
and real memory_rw, on the UNMODIFIED in-tree `-E mvme88k -e mvme187'.  No machine
description edited, no device_add added -- mvme187 already attaches this device.

THE ORACLE, and why it is not a timeout and not a grep.  The symptom is PROCESS
DEATH.  Four independent discriminators, and a kill row is scored on the FIRST TWO
jointly:
  (1) REAPED WAIT STATUS.  subprocess returncode 1 == exit(1); 0 == the debugger's
      own `quit'.  A HANG is a distinct third state (TimeoutExpired), so "timed out"
      can never be read as "killed".
  (2) POST-ACCESS OBSERVABLE.  Every session is st r5,r3,0 ; <ACCESS> ; ld r4,r3,0
      and ends `print r4'.  If the guest ran on, r4 == 0x5a5a5a5a; if the host died,
      the third step and the print never happen.  This separates DEATH from a
      fatal() that merely COMPLAINS AND RETURNS -- which this fork has many of.
  (3) ATTRIBUTION BY MESSAGE.  The message names the offset, so the death is tied to
      the access rather than to the session.  Corroboration, never proof on its own.
  (4) ATTRIBUTION BY SIBLING.  Otherwise-identical sessions at 0x1fef (below the
      window), 0x1ff8 (the implemented case) and 0x1ff9 (first accepted clock reg)
      must run to completion.

CONTROLS, clause (ii) of the witness ladder:
  live      a byte written to NVRAM offset 0x100 round-trips through the same decode
  nvram0    a never-written neighbour reads 0x00 -- the array is zero-filled, so a
            nonzero clock byte cannot be zero-fill or a stuck bus
  devsig *  FOUR clock registers (0x1ffc..0x1fff) are compared against the HOST's own
            gmtime, each with its own encoding: year/mon/mday are BCD, wday is
            tm_wday+1 RAW.  A four-way match with two different encodings could only
            come from mk48txx_update_regs().  RAM answers 0; a fallback answers 0.
  shape     the identical session with a RAM load in the access slot exits 0.

TEST-FIRST SHAPE: every `want' below is the FIXED behaviour.  On the committed
pre-fix build the 32 kill rows red; after a fix the same script goes green.

Sentinel: MK48_WITNESS_DONE  (kept: the driver greps for it)
"""

import re
import subprocess
import sys
import time

if len(sys.argv) < 2:
    sys.stderr.write("usage: mk48_nvram_witness.py <gxemul> [label]\n")
    sys.exit(2)

BIN = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "local"
DUMMY = "/tmp/mk48_dummy.bin"
open(DUMMY, "wb").write(b"\x00\x00\x00\x00")

CODE = 0x00010000
SCRATCH = 0x00020000
MK48 = 0xfffc0000                 # machine_mvme88k.c, MVME187
CLKOFF = 0x1ff0
ICSR = 8
ISEC = 9


def enc(op26, rd, rs1, imm):
    return (op26 << 26) | (rd << 21) | (rs1 << 16) | (imm & 0xffff)


def LD_W(rd, rs1, i):
    return enc(0x05, rd, rs1, i)          # ld    (word)


def LD_BU(rd, rs1, i):
    return enc(0x03, rd, rs1, i)          # ld.bu (byte, unsigned, never alignment-checked)


def ST_W(rd, rs1, i):
    return enc(0x09, rd, rs1, i)          # st    (word)


def ST_B(rd, rs1, i):
    return enc(0x0b, rd, rs1, i)          # st.b  (byte,           never alignment-checked)


BR_SELF = 0xc0000000
SENT = 0xdeadbeef
SETUP = ["r2=0x%x" % MK48, "r3=0x%x" % SCRATCH, "r5=0x5a5a5a5a",
         "r4=0x%x" % SENT, "r6=0x%x" % SENT, "r7=0x%x" % SENT, "r8=0x%x" % SENT]

rows = []
msgs = []


def row(name, got, want, note=""):
    assert name not in [n for n, _ in rows], "DUPLICATE ROW NAME %r" % name
    assert len(name) <= 15, name
    ok = (got == want)
    rows.append((name, ok))
    print("%-16s %-22s %-22s %-54s %s" % (name, str(got), str(want), note,
                                          "ok" if ok else "FAIL"))
    return ok


def program(insns, at=CODE):
    words = list(insns) + [BR_SELF, 0]
    cmds = ["put w 0x%x, 0x%08x" % (at + 4 * i, w) for i, w in enumerate(words)]
    return cmds + ["pc=0x%x" % at, "step %d" % len(insns)]


def session(cmds, timeout=60, subtype="mvme187"):
    """-> (transcript, how) where how is exit0 / exit1 / exitN / sigN / TIMEOUT."""
    argv = [BIN, "-V", "-x", "-E", "mvme88k", "-e", subtype, "-M", "64",
            "0x10000:" + DUMMY]
    inp = ("\n".join(list(cmds) + ["quit"]) + "\n").encode("latin-1")
    try:
        p = subprocess.run(argv, input=inp, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, timeout=timeout)
    except subprocess.TimeoutExpired as e:
        out = (e.output or b"").decode("latin-1", "replace").replace("\r", "")
        return out, "TIMEOUT"
    rc = p.returncode
    how = ("sig%d" % -rc) if rc < 0 else ("exit%d" % rc)
    return p.stdout.decode("latin-1", "replace").replace("\r", ""), how


def printed(t, reg):
    """the bare 0x... line the debugger emits after `print rN', skipping chatter."""
    m = re.search(r"print\s+%s\b" % reg, t)
    if not m:
        return "absent"
    for line in t[m.end():].split("\n")[1:]:
        s = line.strip()
        if not s or s.startswith("["):
            continue
        mm = re.match(r"^(0x[0-9a-fA-F]+)$", s)
        return ("0x%x" % int(mm.group(1), 16)) if mm else "absent"
    return "absent"


def access_session(access_word):
    """The access under test always sits between a scratch STORE and a scratch LOAD,
       so a survivor has a positive observable and a corpse has none."""
    return session(SETUP + program([ST_W(5, 3, 0), access_word, LD_W(4, 3, 0)])
                   + ["print r4"])


def bcd(x):
    return ((x // 10) << 4) + (x % 10)


print("mk48nvramkill RUNG-3 WITNESS -- binary=%s label=%s" % (BIN, LABEL))
print("machine: -E mvme88k -e mvme187 -M 64 (UNMODIFIED); device at 0x%08x" % MK48)
print("%-16s %-22s %-22s %-54s %s" % ("row", "got", "want", "note", ""))
t0 = time.time()

# ------------------------------------------------------------------- controls
t, how = session(SETUP + program([ST_B(5, 2, 0x0100), LD_BU(4, 2, 0x0100),
                                  LD_BU(6, 2, 0x0101)])
                 + ["print r4", "print r6"])
row("live", printed(t, "r4"), "0x5a",
    "a byte round-trips through the SAME decode (NVRAM 0x100)")
row("nvram0", printed(t, "r6"), "0x0",
    "a never-written neighbour reads 0 -- the array is zero-filled")

# APPARATUS NEGATIVE CONTROL.  Prove the liveness oracle CAN go red, so a green
# `live' is evidence rather than a check that cannot fail.  pcc2_width_witness.py
# learned this by accident: `-e 187' is not a subtype, the machine never starts, and
# EVERY row went red including the pure-RAM control.  Here that state is asserted.
t, how = session(SETUP + program([ST_B(5, 2, 0x0100), LD_BU(4, 2, 0x0100)])
                 + ["print r4"], subtype="187")
row("neg apparatus", "%s/%s" % (how, printed(t, "r4")), "exit1/absent",
    "bogus subtype -> no machine -> `live' MUST fail; the oracle is failable")

# DEVICE SIGNATURE: four clock regs vs the HOST clock, in two different encodings.
#
# *** C's struct tm AND PYTHON'S struct_time DISAGREE ON TWO OF THESE FOUR FIELDS,
# and the first run of this probe got tm_mon wrong and reported the DEVICE as
# defective when the device was right. ***
#     tm_mon   C: 0..11   Python: 1..12   -> device BCD(tm_mon+1) == bcd(py tm_mon)
#     tm_wday  C: 0=Sun   Python: 0=Mon   -> C wday == (py tm_wday + 1) % 7
#     tm_year  C: yr-1900 Python: full    -> equal mod 100 for 2000..2099 only
#     tm_mday  same in both.
g = time.gmtime()
t, how = session(SETUP + program([LD_BU(4, 2, CLKOFF + 15), LD_BU(6, 2, CLKOFF + 14),
                                  LD_BU(7, 2, CLKOFF + 13), LD_BU(8, 2, CLKOFF + 12)])
                 + ["print r4", "print r6", "print r7", "print r8"])
row("devsig yr", printed(t, "r4"), "0x%x" % bcd(g.tm_year % 100),
    "0x1fff = BCD(host UTC year%100) -- RAM or a fallback answers 0")
row("devsig mon", printed(t, "r6"), "0x%x" % bcd(g.tm_mon),
    "0x1ffe = BCD(host UTC month); py tm_mon is ALREADY 1-based")
row("devsig mday", printed(t, "r7"), "0x%x" % bcd(g.tm_mday),
    "0x1ffd = BCD(host UTC day of month)")
row("devsig wday", printed(t, "r8"), "0x%x" % (((g.tm_wday + 1) % 7) + 1),
    "0x1ffc = tm_wday+1 RAW, NOT BCD -- a second encoding, same block")

t, how = session(SETUP + program([ST_W(5, 3, 0), LD_W(4, 3, 0), LD_W(4, 3, 0)])
                 + ["print r4"])
row("shape", "%s/%s" % (how, printed(t, "r4")), "exit0/0x5a5a5a5a",
    "the session SHAPE with a RAM load in the access slot does not kill")

# sibling-offset attribution controls
for lbl, off, wr in (("ok rd 1fef", 0x1fef, 0), ("ok wr 1fef", 0x1fef, 1),
                     ("ok rd 1ff8", 0x1ff8, 0), ("ok wr 1ff8", 0x1ff8, 1),
                     ("ok rd 1ff9", 0x1ff9, 0), ("ok wr 1ff9", 0x1ff9, 1)):
    w = ST_B(5, 2, off) if wr else LD_BU(4, 2, off)
    t, how = access_session(w)
    row(lbl, "%s/%s" % (how, printed(t, "r4")), "exit0/0x5a5a5a5a",
        "0x%04x %s -- accepted arm, must run to completion"
        % (off, "wr" if wr else "rd"))

#  ------------------------------------------------------------- CSR RISING EDGE
#
#  *** THIS ROW EXISTS BECAUSE THE FIRST KILL TABLE FOUND A FLOOR BREACH: M_ICSR
#  ESCAPED 47/47. ***  That mutant moves the accept block's UPPER bound to
#  CLKOFF+ICSR, making the condition `addr < 0x1ff8 || addr >= 0x1ff8' a TAUTOLOGY --
#  every address is accepted and the switch is NEVER REACHED, so 0x1ff8 is served as
#  plain RAM and the control register stops doing its work.
#
#  The rows `ok rd 1ff8' / `ok wr 1ff8' could not see it, and the reason is the one
#  this project keeps re-learning: THEY ARE SURVIVE-ONLY AT THAT OFFSET.  They assert
#  the access ran to completion, which is true on the RAM path too.  A survival oracle
#  cannot distinguish two arms that both survive.
#
#  THE CHANNEL THAT DOES VARY is the ICSR case's SIDE EFFECT.  Writing the READ bit
#  0 -> 1 calls mk48txx_update_regs(), refreshing the clock registers from the host.
#  So: clear ICSR, poison a clock slot, drive the rising edge, read the slot back.
#  Fixed build -> the poison is gone, replaced by the host value.  M_ICSR -> the
#  poison survives, because no update ever ran.
#
#  r5's low byte is 0x5a, and 0x5a & MK48TXX_CSR_READ (0x40) is 0x40, so ST_B of r5
#  BOTH poisons a slot and drives the edge -- no new instruction encoding is needed.
#  0x5a is a safe poison: BCD day-of-month never exceeds 0x31.
t, how = session(SETUP + program([ST_B(0, 2, CLKOFF + 8),      # ICSR = 0, READ bit clear
                                  ST_B(5, 2, CLKOFF + 13),     # poison the mday slot
                                  ST_B(5, 2, CLKOFF + 8),      # READ bit 0 -> 1
                                  LD_BU(4, 2, CLKOFF + 13)])
                 + ["print r4"])
row("csr rise", printed(t, "r4"), "0x%x" % bcd(g.tm_mday),
    "ICSR read-bit 0->1 must REFRESH the clock regs (kills M_ICSR)")

# ------------------------------------------------------------------ the kills
#  full census: eight offsets x two directions, all byte-width, all guest-reachable
for wr in (0, 1):
    for off in range(CLKOFF, CLKOFF + ICSR):          # 0x1ff0 .. 0x1ff7
        w = ST_B(5, 2, off) if wr else LD_BU(4, 2, off)
        t, how = access_session(w)
        tag = "%s %04x" % ("wr" if wr else "rd", off)
        want_msg = ("[ mk48txx: unimplemented %s offset 0x%x"
                    % ("WRITE to" if wr else "READ from", off))
        if want_msg in t:
            msgs.append(tag)
        row(tag, how, "exit0",
            "%s of 0x%04x must not end the host process"
            % ("st.b" if wr else "ld.bu", off))
        row(tag + " obs", printed(t, "r4") if how == "exit0" else "died",
            "0x5a5a5a5a",
            "...and the guest runs on -- kills a death however it is spelled")

#  INVERTED FROM THE WITNESS, DELIBERATELY, and this is the only row whose
#  polarity differs.  The witness asserted 16 -- the defect naming its own
#  offsets -- which is green only while the defect is LIVE.  A detector must
#  assert the post-fix truth: the eight offsets are ordinary NVRAM and produce
#  NO unimplemented-access diagnostic at all.  KILLS: any mutant restoring the
#  old boundary brings all sixteen messages back.  CHANNEL: the count itself,
#  which varies 0 <-> 16 across that edit, so the row cannot be vacuous.
row("msg silent", len(msgs), 0,
    "NO access to 0x1ff0..0x1ff7 may announce an unimplemented offset")

bad = [n for n, ok in rows if not ok]
print("MK48_RESULT=%d/%d" % (len(rows) - len(bad), len(rows)))
print("MK48_LABEL=%s" % LABEL)
print("MK48_ELAPSED=%.1fs" % (time.time() - t0))
if bad:
    print("MK48_RED=%s" % ",".join(bad))
print("MK48_WITNESS_DONE")
