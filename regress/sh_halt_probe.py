#!/usr/bin/env python3
"""Gate 10's second instrument: legal SuperH encodings must not stop the emulator.

Prints one line per row:  <name> <got> <want> ok|FAIL
then SH_HALT_CONTROL=OK|DEAD and SH_HALT_RESULT=<passed>/<total>.
gate_sh_rounding.sh does the asserting.

What this protects
------------------
#314. The SH decoder answered an encoding it does not implement with `goto bad`,
which reaches the shared label in cpu_dyntrans.c and sets cpu->running = 0 -- a
legal instruction stopping the whole emulator. It now decodes to instr(reserved),
which raises the general illegal-instruction exception at EXECUTE time. Execute
time is load-bearing: readahead translates instructions that may never run, so
raising from the decoder would corrupt state for a guest that never executed the
word.

Measured on the committed build, all eight of the rows below stopped the
emulator. Three of them -- MAC.L, MAC.W and TST.B -- are BASE ISA, present since
SH-1/SH-2 and unambiguously legal on the SH7751R this rig models, so this is not
a question about accepting SH-4A extensions on an SH-4 core.

How the outcome is classified, and why that took three tries
-----------------------------------------------------------
A halt is read off the dyntrans "UNIMPLEMENTED instruction" message, NOT off a
memory marker. The first version of this sweep decided the outcome purely by
whether a store after the test instruction had run, which conflates three
different things:

  * the emulator stopped                          <- the defect
  * the exception was raised, so the store was    <- the FIX working
    never reached
  * the instruction ran and simply did not reach  <- e.g. SLEEP, which is
    the store                                        implemented and sleeps

That marker-only classifier reported SLEEP as a halt, which is false -- SLEEP has
a case and a handler -- and, after the fix landed, reported every repaired row as
still broken. Naming each outcome separately is what made the measurement mean
anything.

Row meaning: got is the observed outcome, want is "alive". A row can fail in
both directions -- it caught a real defect on the committed build, and it would
catch a regression that reintroduced the halt.
"""
import os
import pty
import re
import select
import sys
import time

BIN = sys.argv[1]
KERNEL = sys.argv[2]

CODE = 0x8c010000
DEST = 0x8c010100

#  mov #0x5a,r0 ; <test> ; mov.l r0,@r1   -- r1 = DEST
MOV_R0_5A = 0xe05a
MOV_L_R0_AT_R1 = 0x2102

ROWS = [
    (0x0009, "nop control",   "base"),
    (0x000f, "MAC.L",         "base ISA"),
    (0x400f, "MAC.W",         "base ISA"),
    (0xcc01, "TST.B",         "base ISA"),
    (0x003a, "STC SGR",       "SH-4 privileged"),
    (0x40f2, "STC.L DBR",     "SH-4 privileged"),
    (0x0063, "MOVLI.L",       "SH-4A"),
    (0x00ab, "SYNCO",         "SH-4A"),
    (0x00d3, "PREFI",         "SH-4A"),
]


def run(iw):
    """Return "alive", "HALTED", or None if the session never came up."""
    pid, fd = pty.fork()
    if pid == 0:
        os.execvp(BIN, [BIN, "-V", "-E", "landisk", "-M", "64", KERNEL])
        os._exit(127)
    buf = ""

    def rd(t=0.4):
        nonlocal buf
        r, _, _ = select.select([fd], [], [], t)
        if fd not in r:
            return True
        try:
            d = os.read(fd, 65536)
        except OSError:
            return False
        if not d:
            return False
        buf += d.decode("latin1", "replace")
        return True

    def wait(timeout=60, mark=0, echo=None):
        t = time.time()
        while time.time() - t < timeout:
            if not rd():
                return False
            resp = buf[mark:]
            #  #392: the ECHO first -- a prompt in the slice proves
            #  nothing until the debugger has taken the command.
            if echo is not None and echo not in resp:
                continue
            if len(buf) > mark and resp.rstrip().endswith("GXemul>"):
                return True
        return False

    def send(s):
        b = (s + "\n").encode("latin1")
        _mark = len(buf)
        n = 0
        while n < len(b):
            n += os.write(fd, b[n:])
        return wait(mark=_mark, echo=s if s else None)

    if not wait(90):
        try:
            os.kill(pid, 9)
            os.waitpid(pid, 0)
        except Exception:
            pass
        return None

    for c in ["r0=0x%x" % DEST, "r1=0x%x" % DEST,
              "put w 0x%x, 0xdeadbeef" % DEST,
              "put h 0x%x, 0x%04x" % (CODE, MOV_R0_5A),
              "put h 0x%x, 0x%04x" % (CODE + 2, iw),
              "put h 0x%x, 0x%04x" % (CODE + 4, MOV_L_R0_AT_R1),
              "pc=0x%x" % CODE, "step 3"]:
        send(c)

    halted = "UNIMPLEMENTED instruction" in buf

    #  Prove the session is still answering, so "not halted" cannot be read off
    #  a dead pty. A dump that returns nothing is reported as its own outcome
    #  rather than silently scoring as alive.
    responded = False
    for _ in range(3):
        mark = len(buf)
        send("dump 0x%x 0x%x" % (DEST, DEST + 4))
        if re.search(r"0x0*[0-9a-f]+\s+[0-9a-f]{8}", buf[mark:]):
            responded = True
            break
        time.sleep(1.0)
        rd(1.0)
    try:
        os.write(fd, b"quit\n")
        time.sleep(0.3)
        os.kill(pid, 9)
        os.waitpid(pid, 0)
    except Exception:
        pass

    if halted:
        return "HALTED"
    return "alive" if responded else "unresponsive"


#  ---- round 80: execute-time halts, and one dropped store --------------------
#  These need a state-setting prologue (FPSCR.SZ/PR, SR.FD, a branch), so a bare
#  encoding sweep like the one above is structurally blind to them -- which is
#  exactly why they survived round 79. Each row is (name, setup+code, expected
#  words at DEST or None to assert only "the emulator is alive").
#
#  The two XD rows are the load-bearing ones. The register-pair handlers pick a
#  base pointer, redirecting an ODD register field to the XF bank; an earlier
#  draft of the fix computed that redirect and then still transferred through
#  the original pointer, which every DR test passes and only an XD test can
#  catch. These rows seed fr0/fr1 and xf0/xf1 with different values, so reading
#  back fr's values where xf's were owed fails the row.
SRC = 0x8c010180

R80 = [
    ("movca.l",     # r12 is the decoder's DEFAULT source for this encoding:
                    # forgetting the R0 override stores r12 and this row says so
     ["r0=0xaaaa1111", "r12=0xbbbb2222", "r1=0x%x" % DEST,
      "put w 0x%x, 0xdeadbeef" % DEST,
      "put h 0x%x, 0x01c3" % CODE, "pc=0x%x" % CODE, "step 1"],
     [0xaaaa1111]),
    ("fmovd @r1",   # the rn parity that used to call exit(1)
     ["fpscr=0x00140001", "r1=0x%x" % DEST, "fr0=0x11111111", "fr1=0x22222222",
      "put w 0x%x, 0xdeadbeef" % DEST, "put w 0x%x, 0xdeadbeef" % (DEST + 4),
      "put h 0x%x, 0xf10a" % CODE, "pc=0x%x" % CODE, "step 1"],
     [0x11111111, 0x22222222]),
    ("fmovd @r2",   # same instruction, the parity that survived: must match
     ["fpscr=0x00140001", "r2=0x%x" % DEST, "fr0=0x11111111", "fr1=0x22222222",
      "put w 0x%x, 0xdeadbeef" % DEST, "put w 0x%x, 0xdeadbeef" % (DEST + 4),
      "put h 0x%x, 0xf20a" % CODE, "pc=0x%x" % CODE, "step 1"],
     [0x11111111, 0x22222222]),
    ("fmovd xd st",
     ["fpscr=0x00140001", "r2=0x%x" % DEST,
      "fr0=0x11111111", "fr1=0x22222222", "xf0=0x33333333", "xf1=0x44444444",
      "put w 0x%x, 0xdeadbeef" % DEST, "put w 0x%x, 0xdeadbeef" % (DEST + 4),
      "put h 0x%x, 0xf21a" % CODE, "pc=0x%x" % CODE, "step 1"],
     [0x33333333, 0x44444444]),
    ("fmovd xd ld",
     ["fpscr=0x00140001", "r2=0x%x" % SRC, "r3=0x%x" % DEST,
      "put w 0x%x, 0x55555555" % SRC, "put w 0x%x, 0x66666666" % (SRC + 4),
      "put w 0x%x, 0xdeadbeef" % DEST, "put w 0x%x, 0xdeadbeef" % (DEST + 4),
      "put h 0x%x, 0xf128" % CODE, "put h 0x%x, 0xf31a" % (CODE + 2),
      "pc=0x%x" % CODE, "step 2"],
     [0x55555555, 0x66666666]),
    ("fmovd r0idx",  # both R0-indexed forms used to ABORT_EXECUTION
     ["fpscr=0x00140001", "r0=0", "r2=0x%x" % SRC, "r3=0x%x" % DEST,
      "put w 0x%x, 0x77777777" % SRC, "put w 0x%x, 0x88888888" % (SRC + 4),
      "put w 0x%x, 0xdeadbeef" % DEST, "put w 0x%x, 0xdeadbeef" % (DEST + 4),
      "put h 0x%x, 0xf026" % CODE, "put h 0x%x, 0xf307" % (CODE + 2),
      "pc=0x%x" % CODE, "step 2"],
     [0x77777777, 0x88888888]),
    ("fmovs SZ=0",   # the single-precision control: alignment mask must stay 3
     ["fpscr=0x00040001", "r2=0x%x" % DEST, "fr0=0x99999999",
      "put w 0x%x, 0xdeadbeef" % DEST,
      "put h 0x%x, 0xf20a" % CODE, "pc=0x%x" % CODE, "step 1"],
     [0x99999999]),
    ("fsrra PR=1",   ["fpscr=0x000c0001", "put h 0x%x, 0xf07d" % CODE,
                      "pc=0x%x" % CODE, "step 1"], None),
    ("fneg odd PR=1", ["fpscr=0x000c0001", "put h 0x%x, 0xf14d" % CODE,
                       "pc=0x%x" % CODE, "step 1"], None),
    ("fabs odd PR=1", ["fpscr=0x000c0001", "put h 0x%x, 0xf15d" % CODE,
                       "pc=0x%x" % CODE, "step 1"], None),
    ("fp in slot",   ["sr=0x400080f0", "put h 0x%x, 0xa002" % CODE,
                      "put h 0x%x, 0xf000" % (CODE + 2),
                      "pc=0x%x" % CODE, "step 2"], None),
    ("trapa in slot", ["put h 0x%x, 0xa002" % CODE,
                       "put h 0x%x, 0xc300" % (CODE + 2),
                       "pc=0x%x" % CODE, "step 2"], None),
]


def run_seq(cmds, nwords, dumpat=DEST):
    """Return (outcome, values). Outcome distinguishes a host EXIT from an
    emulator halt from a live run -- three of round 80's defects killed the
    gxemul process outright rather than setting cpu->running = 0, and a probe
    that only looked for the halt message would have scored those as passes."""
    pid, fd = pty.fork()
    if pid == 0:
        os.execvp(BIN, [BIN, "-V", "-E", "landisk", "-M", "64", KERNEL])
        os._exit(127)
    buf = ""
    died = False

    def rd(t=0.4):
        nonlocal buf, died
        r, _, _ = select.select([fd], [], [], t)
        if fd not in r:
            return True
        try:
            d = os.read(fd, 65536)
        except OSError:
            died = True
            return False
        if not d:
            died = True
            return False
        buf += d.decode("latin1", "replace")
        return True

    def wait(timeout=60, mark=0, echo=None):
        t = time.time()
        while time.time() - t < timeout:
            if not rd():
                return False
            resp = buf[mark:]
            #  #392: the ECHO first -- a prompt in the slice proves
            #  nothing until the debugger has taken the command.
            if echo is not None and echo not in resp:
                continue
            if len(buf) > mark and resp.rstrip().endswith("GXemul>"):
                return True
        return False

    def send(s):
        b = (s + "\n").encode("latin1")
        _mark = len(buf)
        n = 0
        while n < len(b):
            n += os.write(fd, b[n:])
        return wait(mark=_mark, echo=s if s else None)

    if not wait(90):
        try:
            os.kill(pid, 9)
            os.waitpid(pid, 0)
        except Exception:
            pass
        return "noprompt", None

    ok = True
    for c in cmds:
        if not send(c):
            ok = False
            break
    halted = "UNIMPLEMENTED instruction" in buf or "Execution aborted" in buf
    vals = None
    if ok and not died:
        for _ in range(3):
            mark = len(buf)
            send("dump 0x%x 0x%x" % (dumpat, dumpat + 4 * nwords))
            w = re.findall(r"0x0*[0-9a-f]+\s+((?:[0-9a-f]{8}\s+){1,4})",
                           buf[mark:])
            flat = "".join(w).split()
            if len(flat) >= nwords:
                vals = [int.from_bytes(bytes.fromhex(h), "little")
                        for h in flat[:nwords]]
                break
            time.sleep(1.0)
            rd(1.0)
    try:
        os.write(fd, b"quit\n")
        time.sleep(0.3)
        os.kill(pid, 9)
        os.waitpid(pid, 0)
    except Exception:
        pass
    if died or not ok:
        return "HOSTEXIT", None
    if halted:
        return "HALTED", None
    return "alive", vals


#  ---- round 81: the store-queue flush with the MMU on -------------------------
#  #318. `pref` into 0xE0000000..0xE3FFFFFF is a store-queue write-back, and with
#  MMUCR.AT set the destination comes from the UTLB rather than from QACR. That
#  path used to run ABORT_EXECUTION.
#
#  MMUCR and the UTLB arrays are written by GUEST stores, not by debugger register
#  writes: the debugger names exist but do not reach the fields, so an earlier
#  version of this probe set them, never entered the AT branch at all, and would
#  have passed against a build with no fix in it. The prologue below installs the
#  entry through the architectural MMIO windows (UTLB address array 0xF6000000,
#  data array 0xF7000000) and sets MMUCR at 0xFF000010, exactly as a guest kernel
#  would.
#
#  The operand carries nonzero bits in BOTH [9:5] and [4:0] on purpose. The
#  architectural destination is the translated page plus the operand's own [9:5]
#  with [4:0] zeroed, so 0xE00000E7 must land at page|0xE0 -- an address that is
#  neither the raw operand nor the page base. That is what proves the composition
#  rather than merely proving the emulator survived.
#
#  *** THE JUDGEMENT IS READ TYPE, AND THIS COMMENT USED TO SAY THE OPPOSITE. ***
#  Corrected in #454 against the manual, which was not in this tree when the rows
#  were first pinned.  SH7750 Hardware Manual Rev.7.00 4.7.4 "SQ Protection",
#  page 144 -- `_scratchpad/sh7750_hardware.txt:11744-11746`, and word for word
#  again in the SH-4 programming manual 4.6.4 at `sh4_programming.txt:3561-3563`:
#
#      "Write type exception judgment is performed for writes to the SQs, and
#       read type for transfer from the SQs to external memory (PREF
#       instruction), and a TLB miss exception, protection violation exception,
#       or initial page write exception is generated."
#
#  The quotation is carried here in full ON PURPOSE: the rows it pins were
#  previously pinned to a panel VERDICT rather than to a document, so a future
#  seat must be able to re-derive them without trusting this round.
#
#  4.7.4 still lists the initial page write exception because the sentence covers
#  BOTH halves, and IPW belongs to the write half -- 3.6.7 defines it as occurring
#  on "a data access (write)", so a read-type access cannot raise it at all.  That
#  is what settles the alternative reading, under which "read type" would name
#  only the EXPEVT variant while the permission bits were still judged as a write.
#
#  Hence `sq pr00 rdok` and `sq d0 rdok`: in privileged mode a read is permitted
#  by PR=00 and is indifferent to D, so BOTH complete the copy.  They are named
#  for what they now prove, because the old names -- "prot" and "clean" -- assert
#  a protection case and a dirty-bit case that read-type judgement does not have.
#
#  The EXPEVT rows below are NOT decoration.  Post-correction the miss is the only
#  faulting row left in privileged mode and it yields the same destination word
#  either way, so the copy channel alone cannot see the change at all.  TWO
#  one-token mutants were MEASURED to score full marks against the value rows:
#  `FLAG_NOEXCEPTIONS`, which makes translate_via_mmu report SUCCESS with
#  *return_paddr = 0 so the 32-byte payload lands at PHYSICAL ZERO in silence, and
#  `FLAG_INSTR`, which is caught only by the two ITLB rows further down.
SQ_AA = 0xf6000000
SQ_DA1 = 0xf7000000
MMUCR = 0xff000010
DESTPHYS = 0x0c020000
DESTVIRT = 0x8c020000
SQ_AA_VAL = (0xe0000000 & 0xfffffc00) | 0x100 | 0x200      # VPN | V | D


def sq_da1(pr=3, d=1):
    return (DESTPHYS & 0x1ffffc00) | (pr << 5) | 0x100 | (0x004 if d else 0)


#  MMUCR bits, so a row can say which one it means.  SQMD is not decoration: see
#  the `sq pr00 rdok` row.
MMUCR_AT = 0x00000001
MMUCR_SQMD = 0x00000200


def sq_seq(da1val, install=True, operand=0xe00000e7, mmucr=MMUCR_AT):
    """Fill queue 1, install the UTLB entry + MMUCR from the guest, then pref."""
    c = ["put w 0x%x, 0x%08x" % (0xe0000020 + i * 4, 0xa0000000 + i)
         for i in range(8)]
    c += ["r1=0x%x" % SQ_AA, "r2=0x%08x" % SQ_AA_VAL,
          "r3=0x%x" % SQ_DA1, "r4=0x%08x" % da1val,
          "r5=0x%x" % MMUCR, "r6=0x%08x" % mmucr,
          "r7=0x%08x" % operand,
          "put w 0x%x, 0xdeadbeef" % (DESTVIRT + 0xE0)]
    if install:
        c += ["put h 0x%x, 0x2122" % CODE,        # mov.l r2,@r1  (UTLB AA)
              "put h 0x%x, 0x2342" % (CODE + 2),  # mov.l r4,@r3  (UTLB DA1)
              "put h 0x%x, 0x2562" % (CODE + 4),  # mov.l r6,@r5  (MMUCR.AT=1)
              "put h 0x%x, 0x0783" % (CODE + 6),  # pref @r7
              "pc=0x%x" % CODE, "step 4"]
    else:
        c += ["put h 0x%x, 0x2562" % CODE,
              "put h 0x%x, 0x0783" % (CODE + 2),
              "pc=0x%x" % CODE, "step 2"]
    return c


SENTINEL = [0xdeadbeef]
FLUSHED = [0xa0000000, 0xa0000001]

#  ---- the EXPEVT channel ------------------------------------------------------
#  P4 is direct-mapped (memory_sh.c:373-377), so EXPEVT stays reachable with AT=1.
SH4_EXPEVT = 0xff000024
EVSCRATCH = 0x8c010200
CODE2 = 0x8c010080
NOEXC = [0x00000999]            # the seed, still there == nothing was raised

#  *** THE SEED MUST NOT COLLIDE WITH ANY EXPEVT CODE, AND THAT IS AN ASSERTION
#  RATHER THAN A CONVENTION. ***  Found by asking the panel for one more mutant
#  AFTER the kill table was already clean -- which is exactly what that rule is
#  for.  The mutant is a plausible tidy-up: change the seed to 0x040, "the value
#  the row expects anyway".  All 31 rows stay GREEN, because `sq miss evt` then
#  cannot tell a raised 0x040 from a surviving seed -- and `sq miss evt` is the
#  ONLY row that kills FLAG_NOEXCEPTIONS, the mutant that lands the payload at
#  physical zero in silence.  So a one-token edit to a CONSTANT would have
#  re-opened the round's worst escape without reddening anything.
#
#  Every SH-4 EXPEVT code is a multiple of 0x20 (3.6, exception code table), so
#  this catches a collision with ANY code, present or future.  An enumerated list
#  of the codes these rows happen to raise would go stale the first time a row is
#  added; this cannot.  It is the vacuity taxonomy's "a row must fail to a
#  DISTINGUISHABLE token" made mechanical.
assert NOEXC[0] % 0x20 != 0, (
    "EXPEVT no-exception seed 0x%x is a multiple of 0x20 and so is every EXPEVT "
    "code -- a raised exception would be indistinguishable from the seed and the "
    "evt rows would pass vacuously" % NOEXC[0])


def sq_seq_ev(da1val, install=True, operand=0xe00000e7):
    """As sq_seq(), but SEEDS EXPEVT from the guest first and reads it back after.

    The seed is what makes "no exception" a POSITIVE reading instead of a guess at
    a reset value -- 0x999 can only be there because the guest put it there and
    nothing overwrote it.
    """
    c = ["put w 0x%x, 0x%08x" % (0xe0000020 + i * 4, 0xa0000000 + i)
         for i in range(8)]
    c += ["r1=0x%x" % SQ_AA, "r2=0x%08x" % SQ_AA_VAL,
          "r3=0x%x" % SQ_DA1, "r4=0x%08x" % da1val,
          "r5=0x%x" % MMUCR, "r6=0x00000001",
          "r7=0x%08x" % operand,
          "r10=0x%x" % SH4_EXPEVT, "r11=0x00000999",
          "put w 0x%x, 0xdeadbeef" % (DESTVIRT + 0xE0),
          "put w 0x%x, 0xdeadbeef" % EVSCRATCH]

    ins = [0x2ab2]                                  # mov.l r11,@r10  (seed EXPEVT)
    ins += [0x2122, 0x2342] if install else []      # UTLB AA, UTLB DA1
    ins += [0x2562, 0x0783]                         # MMUCR.AT=1, pref @r7
    c += ["put h 0x%x, 0x%04x" % (CODE + 2 * i, w) for i, w in enumerate(ins)]
    c += ["pc=0x%x" % CODE, "step %d" % len(ins)]

    #  *** READ BACK THROUGH r8/r9 ONLY, AND THAT IS NOT STYLE. ***  An exception
    #  sets SR.RB (cpu_sh.c:688), so r0-r7 are THE OTHER BANK afterwards and a
    #  register seeded before the pref would read back as someone else's.  r8-r15
    #  are unbanked, so they survive the switch; r0 is written and consumed
    #  entirely after it, which is safe.
    c += ["r8=0x%x" % SH4_EXPEVT, "r9=0x%x" % EVSCRATCH,
          "put h 0x%x, 0x6082" % CODE2,             # mov.l @r8,r0
          "put h 0x%x, 0x2902" % (CODE2 + 2),       # mov.l r0,@r9
          "pc=0x%x" % CODE2, "step 2"]
    return c


#  ---- the QACR composition, which nothing pinned -----------------------------
#  *** THE GATE CLAIMED `sq at0 qacr` WAS "the regression guard: the QACR
#  composition must be exactly as before".  MEASURED FALSE: the composition can be
#  DELETED OUTRIGHT and that row stays green. ***
#
#  Two reasons it was blind, and both are structural rather than unlucky.  NO row
#  in this file ever wrote QACR0 or QACR1 and `dev_sh4.c` seeds them nowhere, so
#  `(((qacrN >> 2) & 7) << 26)` was identically ZERO in every row -- the term
#  under test contributed nothing to any expected value.  And every SQ operand was
#  `0xe00000e7`, bit 5 SET, so `sq_nr` was 1 in all ten rows and **QACR0 was never
#  the register consulted, ever.**
#
#  The escape is guest-visible corruption, not a hypothetical: with AT=0 -- the
#  ordinary store-queue mode, without paging -- the destination AREA comes entirely
#  from QACR, so dropping the term or swapping the two registers lands 32 bytes on
#  the wrong physical page.  Both mutants scored 31/31 before these rows existed.
#
#  #454 made that edit MORE likely, which is why the rows ship with it: this round
#  adds three comments saying that with the MMU on "QACR takes no part" and "the
#  extaddr built above is discarded", and a maintainer tidying the now-dead-looking
#  composition four lines above is exactly the six-months-later edit.
QACR0 = 0xff000038
QACR1 = 0xff00003c
QRIGHT = 0x8c0000e0             # P1 alias of 0x0c0000e0 -- area 3, from QACR
QWRONG = 0x800000e0             # P1 alias of 0x000000e0 -- area 0, the composed-away one
Q0RIGHT = 0x8c0000c0
FLUSHED0 = [0xb0000000, 0xb0000001]


def sq_seq_qacr(operand=0xe00000e7, q0=0x00, q1=0x0c):
    """Seed BOTH queues and BOTH candidate destinations, then set QACR from the guest.

    Both queues are seeded with distinguishable payloads so a row can say WHICH
    queue was read, and both destinations carry distinct sentinels so a row can say
    WHICH page was written. `q1=0x0c` selects external area 3, because
    `(0x0c >> 2) & 7 == 3`.
    """
    c = ["put w 0x%x, 0x%08x" % (0xe0000000 + i * 4, 0xb0000000 + i)
         for i in range(8)]
    c += ["put w 0x%x, 0x%08x" % (0xe0000020 + i * 4, 0xa0000000 + i)
          for i in range(8)]
    c += ["put w 0x%x, 0x11111111" % QRIGHT,
          "put w 0x%x, 0x22222222" % QWRONG,
          "put w 0x%x, 0x33333333" % Q0RIGHT,
          "r1=0x%x" % QACR1, "r2=0x%08x" % q1,
          "r3=0x%x" % QACR0, "r4=0x%08x" % q0,
          "r7=0x%08x" % operand,
          "put h 0x%x, 0x2122" % CODE,          # mov.l r2,@r1   QACR1
          "put h 0x%x, 0x2342" % (CODE + 2),    # mov.l r4,@r3   QACR0
          "put h 0x%x, 0x0783" % (CODE + 4),    # pref @r7
          "pc=0x%x" % CODE, "step 3"]
    return c


#  ---- the ITLB divergence row -------------------------------------------------
#  The ONLY thing that separates a read-type UTLB walk from an INSTRUCTION walk:
#  FLAG_INSTR makes translate_via_mmu scan the ITLB first (memory_sh.c:113-122),
#  so give the two arrays entries that cover the same VPN and disagree about the
#  destination.  A correct build follows the UTLB; a FLAG_INSTR build follows the
#  ITLB, and the two pages swap contents.
SQ_ITLB_AA = 0xf2000000
SQ_ITLB_DA1 = 0xf3000000
DECOYPHYS = 0x0c030000
DECOYVIRT = 0x8c030000


def sq_seq_itlb():
    """Install BOTH a UTLB and an ITLB entry for the SQ page, pointing elsewhere."""
    c = ["put w 0x%x, 0x%08x" % (0xe0000020 + i * 4, 0xa0000000 + i)
         for i in range(8)]
    c += ["r1=0x%x" % SQ_AA, "r2=0x%08x" % SQ_AA_VAL,
          "r3=0x%x" % SQ_DA1, "r4=0x%08x" % sq_da1(),
          "r12=0x%x" % SQ_ITLB_AA, "r13=0x%08x" % SQ_AA_VAL,
          "r14=0x%x" % SQ_ITLB_DA1,
          "r15=0x%08x" % ((DECOYPHYS & 0x1ffffc00) | (3 << 5) | 0x100 | 0x004),
          "r5=0x%x" % MMUCR, "r6=0x00000001",
          "r7=0x%08x" % 0xe00000e7,
          "put w 0x%x, 0xdeadbeef" % (DESTVIRT + 0xE0),
          "put w 0x%x, 0xdeadbeef" % (DECOYVIRT + 0xE0)]
    ins = [0x2122,          # mov.l r2,@r1    UTLB address array
           0x2342,          # mov.l r4,@r3    UTLB data array 1
           0x2cd2,          # mov.l r13,@r12  ITLB address array
           0x2ef2,          # mov.l r15,@r14  ITLB data array 1
           0x2562,          # mov.l r6,@r5    MMUCR.AT=1
           0x0783]          # pref @r7
    c += ["put h 0x%x, 0x%04x" % (CODE + 2 * i, w) for i, w in enumerate(ins)]
    c += ["pc=0x%x" % CODE, "step %d" % len(ins)]
    return c

R81 = [
    ("sq at1 ok",   sq_seq(sq_da1()),          DESTVIRT + 0xE0, FLUSHED),
    ("sq at1 miss", sq_seq(sq_da1(), False),   DESTVIRT + 0xE0, SENTINEL),
    #  Both re-pinned in #454 from SENTINEL, and renamed: read-type judgement has
    #  no protection case at PR=00 in privileged mode and no dirty-bit case at all.
    #
    #  *** SQMD IS SET HERE ON PURPOSE, and it is the whole reason this row can
    #  see anything the other rows cannot. ***  A seat asked for one more mutant
    #  after the kill table was already clean and produced a plausible one: a
    #  maintainer starting on `sh4sqwrite` writes
    #  `flags = (mmucr & SQMD) ? FLAG_WRITEFLAG : 0`, reasoning that SQMD means
    #  "treat SQ accesses strictly".  It does not -- SQMD governs who may touch
    #  the queue WINDOW, and it never reclassifies the external transfer from
    #  read to write.  With every row leaving SQMD clear that mutant passed all
    #  31.  Setting it here costs nothing (SQMD only bars USER access, and this
    #  row is privileged, so a correct build still flushes) and reddens the
    #  mutant, which now judges PR=00 as a write and takes a protection
    #  violation.
    ("sq pr00 rdok", sq_seq(sq_da1(pr=0), mmucr=MMUCR_AT | MMUCR_SQMD),
     DESTVIRT + 0xE0, FLUSHED),
    ("sq d0 rdok",  sq_seq(sq_da1(d=0)),       DESTVIRT + 0xE0, FLUSHED),
    #  The exception channel.  Measured, all three observables move, not just the
    #  miss: the miss changes its CODE while prot and clean stop faulting entirely.
    #  The last two are the de-escalation clause's accept side -- they pin that a
    #  legal transfer still lands AND that nothing was raised to make it land.
    ("sq miss evt", sq_seq_ev(sq_da1(), False), EVSCRATCH, [0x040]),
    ("sq pr00 evt", sq_seq_ev(sq_da1(pr=0)),   EVSCRATCH, NOEXC),
    ("sq d0 evt",   sq_seq_ev(sq_da1(d=0)),    EVSCRATCH, NOEXC),
    #  A correct build walks the UTLB, so the payload lands on the UTLB's page and
    #  the ITLB's decoy keeps its sentinel.  FLAG_INSTR swaps the two.
    ("sq itlb utlb", sq_seq_itlb(),            DESTVIRT + 0xE0, FLUSHED),
    ("sq itlb decoy", sq_seq_itlb(),           DECOYVIRT + 0xE0, SENTINEL),
    #  The QACR composition. `dst` pins that the area bits ARRIVE; `neg` is
    #  load-bearing because without it a build writing to BOTH destinations passes;
    #  `sel` is the first row in this file to drive `sq_nr == 0` at all, so it pins
    #  the register SELECTION and proves queue 0 is the source.
    ("sq qacr1 dst", sq_seq_qacr(),            QRIGHT, FLUSHED),
    ("sq qacr1 neg", sq_seq_qacr(),            QWRONG, [0x22222222]),
    ("sq qacr0 sel", sq_seq_qacr(operand=0xe00000c7, q0=0x0c, q1=0x00),
     Q0RIGHT, FLUSHED0),
    #  AT=0 keeps the QACR composition: destination is addr & 0x03ffffe0, i.e.
    #  physical 0xE0, reachable through P1. This row is the regression guard.
    ("sq at0 qacr",
     ["put w 0x%x, 0x%08x" % (0xe0000020 + i * 4, 0xa0000000 + i)
      for i in range(8)]
     + ["r7=0xe00000e7", "put w 0x%x, 0xdeadbeef" % 0x800000e0,
        "put h 0x%x, 0x0783" % CODE, "pc=0x%x" % CODE, "step 1"],
     0x800000e0, FLUSHED),
]

rows = []
control = run(0x0009)
print("SH_HALT_CONTROL=%s" % ("OK" if control == "alive" else "DEAD"))
if control != "alive":
    print("SH_HALT_RESULT=0/0")
    sys.exit(0)

for iw, name, cls in ROWS:
    got = run(iw)
    ok = (got == "alive")
    rows.append(ok)
    print("%-14s %-14s %-8s %-16s %s"
          % (name, got if got else "dead", "alive", cls, "ok" if ok else "FAIL"))

for name, cmds, want in R80:
    st, vals = run_seq(cmds, len(want) if want else 1)
    if want is None:
        ok = (st == "alive")
        got, wnt = st, "alive"
    else:
        ok = (st == "alive" and vals is not None and vals[:len(want)] == want)
        got = st if st != "alive" else (
            ",".join("0x%08x" % v for v in (vals or [])[:len(want)]) or "nodump")
        wnt = ",".join("0x%08x" % w for w in want)
    rows.append(ok)
    print("%-14s %-14s %-8s %-16s %s"
          % (name, got, wnt, "round 80", "ok" if ok else "FAIL"))

for name, cmds, dumpat, want in R81:
    st, vals = run_seq(cmds, len(want), dumpat)
    ok = (st == "alive" and vals is not None and vals[:len(want)] == want)
    got = st if st != "alive" else (
        ",".join("0x%08x" % v for v in (vals or [])[:len(want)]) or "nodump")
    rows.append(ok)
    print("%-14s %-24s %-24s %-10s %s"
          % (name, got, ",".join("0x%08x" % w for w in want),
             "round 81", "ok" if ok else "FAIL"))

print("SH_HALT_RESULT=%d/%d" % (sum(1 for r in rows if r), len(rows)))
