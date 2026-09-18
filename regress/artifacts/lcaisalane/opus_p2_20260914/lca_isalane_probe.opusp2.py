#!/usr/bin/env python3
#
#  lcaisalane -- RUNG-3 WITNESS: the LCA sparse-I/O byte-lane handler ends the host process on an
#  ordinary byte access to a documented ISA register, and SILENTLY ANSWERS ZERO on another.
#
#  THE DEFECT, quoted from `DEVICE_ACCESS(lca_isa)' in src/devices/dev_lca.c:
#
#      relative_addr >>= 5;
#
#      ofs = relative_addr & 3;
#      if (ofs > len) {
#              fatal("[ ofs=%i len=%i in lca_isa access function. "
#                  "aborting ]\n", ofs, len);
#              exit(1);
#      }
#
#      if (writeflag == MEM_WRITE) {
#              byte = data[ofs % len];
#              return cpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE +
#                  relative_addr, &byte, 1, writeflag, CACHE_NONE);
#      }
#
#      cpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE + relative_addr,
#          &byte, 1, MEM_READ, CACHE_NONE);
#
#      for (i=0; i<len; i++)
#              data[i] = i == ofs? byte : 0x00;
#
#  *** THE LANE IS NOT AN INDEPENDENT FIELD.  IT IS THE LOW TWO BITS OF THE ISA PORT NUMBER. ***
#  The shift comes FIRST, so `ofs' is bits 6:5 of the incoming relative address -- which are bits
#  1:0 of the derived port -- and the forwarded access goes to `LCA_ISA_BASE + (r >> 5)', i.e. to
#  that same port INCLUDING those two bits.  So there is no way to address ONE port through two
#  different lanes: the lane is a FUNCTION of the port.  The defect therefore partitions the whole
#  64 K ISA port space by `port & 3', and for a BYTE (len == 1) access it reads:
#
#      port & 3 == 0   ->  ofs 0.  data[0] = byte.                        CORRECT
#      port & 3 == 1   ->  ofs 1.  1 > 1 is FALSE, so ACCEPTED -- and the packing loop runs
#                          `for (i = 0; i < 1; i++) data[i] = (i == 1)? byte : 0', which is
#                          never true, so THE DEVICE BYTE IS DISCARDED AND THE GUEST IS HANDED
#                          ZERO with a success return.  A false success, not a decline.
#      port & 3 == 2   ->  ofs 2.  2 > 1  ->  fatal() + exit(1).          HOST DEATH
#      port & 3 == 3   ->  ofs 3.  3 > 1  ->  fatal() + exit(1).          HOST DEATH
#
#  For len == 2 the same arithmetic gives ofs 2 a zero answer and ofs 3 a death; for len 4 and 8
#  `ofs > len' is never true and the packing index is always in range, so those widths are clean.
#  The guard's `>' (rather than `>=') is what admits the zero-answering case: `ofs == len' passes
#  the guard and then indexes nothing.
#
#  WHAT THAT COSTS AT A REAL DEVICE, and it is why the ns16550 is the right subject.  The console
#  UART sits at ISA 0x3f8..0x3ff, so its eight registers fall into all four classes:
#
#      0x3f8 data     ofs 0   ok        0x3fc mcr       ofs 0   ok
#      0x3f9 ier      ofs 1   ZERO      0x3fd lsr       ofs 1   ZERO
#      0x3fa iir      ofs 2   DEATH     0x3fe msr       ofs 2   DEATH
#      0x3fb lctl     ofs 3   DEATH     0x3ff scratch   ofs 3   DEATH
#
#  A byte read of the LINE STATUS REGISTER -- the register a polling console driver reads before
#  every character -- returns zero, and a byte read of the MODEM STATUS or LINE CONTROL register
#  ends the emulator.  No unusual value, no driver setup, four guest instructions.
#
#  ---------------------------------------------------------------------------------------------
#  *** #530: IT IS NOW THE WITNESS AND THE DETECTOR.  Sessions 1-3 are the witness below, unchanged but
#  for the sentinel; the #530 sessions at the end are the detector for the fix. ***
#
#  THE FIX (disposition B, regress/artifacts/lcaisalane/FABLE_F2_RULING_20260914.md): the byte for port
#  P sits at buffer position (P & 3) % len on BOTH arms; `len == 0' is refused first; no latch, no
#  announce (there is no event -- member 4, ACCEPT).  HEAD 19/37, fix 37/37
#  (regress/artifacts/lcaisalane/fix530_20260914/HEAD_det.out, FIX_det.out).
#
#  CONTRACT (clause e) -- the detector is DESIGNED to catch: the removed exit reinstated at any of the
#  six cells that ended the host (reads AND writes at (1,2) (1,3) (2,3)); a decline beyond the width or
#  at-and-beyond it (a store dropped, a load's register kept); one arm folding and the other not; the
#  byte placed at position 0 instead of (P & 3) % len (the clamp, anchored on (2,1) == (2,3)); a lane
#  decode that drops bit 1 or the `& 3'; a byte replicated into every position; the read arm's success
#  return turned into a failure.  DISCLOSED, not caught: the len 3 and 5-7 heads that memory_rw's 1 KB
#  split produces for a TRANSLATED unaligned LDL/LDQ (this probe runs on K0SEG, untranslated), so
#  `& (len - 1)' for `% len' is equivalent on every probed cell; the len-0 refusal (no producer); the
#  size field a<4:3> (lcaisasize); the quadword lane (lcaisaqword); the missing PHYSICAL (lcaisaphys).
#
#  *** WHAT THE WITNESS (sessions 1-3) IS AND IS NOT.  IT IS A WITNESS, NOT A DETECTOR. ***
#
#  It establishes, on unmodified `alphabook1' with no disk image and no OS: that the sparse window
#  IS live and does reach ISA devices (`live', 0x55 from the 8042 through the same handler); that a
#  BYTE read of a device register whose port is 1 mod 4 completes successfully and hands the guest
#  zero while the device's own byte is demonstrably present (`ofs1 devsig' + `ofs1 wide'); and that
#  a byte read of a register whose port is 2 or 3 mod 4 ends the host with the arm's own diagnostic.
#
#  It is NOT a detector of any repair.  `alive' greens equally for a decline, for a latched
#  announce, for a fault and for a full implementation, and `ofs1 zero' greens for any fix that
#  hands the byte back.  A fix round owes rows that discriminate those -- at minimum, per the codex
#  design reading (regress/artifacts/lcaisalane/codex_design_20260910.err): a REFUSED access must
#  leave the destination register holding its previous value (the `answer' channel this probe
#  already reads), the refusal must repeat without re-announcing, and a supported lane must still
#  deliver the correctly packed byte at every width.
#
#  ---------------------------------------------------------------------------------------------
#  SHAPE, and every element of it is answering a specific objection:
#
#    1.  ONE PROCESS PER OUTCOME, CONTROL FIRST.  A death ends the process, so the two killing
#        lanes get their own runs -- but inside each run the DEVICE SIGNATURE and the WIDE control
#        are taken BEFORE the killing access, so between the access that lives and the access that
#        dies only the WIDTH differs: same address, same window, same process, same instant.
#    2.  ZERO READBACK ALONE PROVES NOTHING, and the design seat said so in those words.  Unmapped
#        space, a missed device and a zero-filled failure buffer all read 0 (`memory_rw.c''s #95
#        pre-zero).  So `ofs1 zero' is never asserted on its own: `ofs1 devsig' reads the SAME
#        register through the flat ISA mapping and gets a nonzero value the device alone produces,
#        and `ofs1 wide' reads it through THIS handler at len 4 and finds the byte sitting in lane
#        1 -- so the byte reaches the packing loop and the loop is what drops it.
#    3.  THE DESTINATION REGISTER IS PRE-SEEDED WITH A SENTINEL before every load.  A load that
#        FAULTS leaves the register untouched (cpu_alpha_instr_loadstore.c returns before
#        writeback when memory_rw fails), so `ofs1 answer' distinguishes "the model answered zero"
#        from "the access failed and the guest kept its old value".  On HEAD it is the former: a
#        FALSE SUCCESS.  This is the discriminator the design seat asked for, taken pre-fix.
#    4.  ATTRIBUTION IS BY THE ARM'S OWN TEXT, NEVER BY EXIT STATUS.  `in lca_isa access function'
#        appears exactly once in src/.  A death for any other reason -- a bad encoding, a different
#        arm -- reds the attrib row instead of passing as a reproduction.
#    5.  EVERY ACCESS IS A GUEST INSTRUCTION.  `lca_isa' is registered DM_DEFAULT, so debugger
#        `dump' would skip the handler entirely and read the pre-zero.  Every `put d' below targets
#        SCRATCH, which is RAM.
#    6.  STAY ON `step'.  Nothing here needs a host timer: the 8042 reply and the UART register
#        file are synchronous with the guest access.
#
#  THE NEGATIVE CONTROL IS ISA PORT 0x300 (`ctl'), which is 0 mod 4 and has NO device behind it.
#  It survives and answers zero.  That is what attributes the two deaths to the LANE rather than to
#  the sparse window, to the byte width, to K0SEG, or to hitting empty ISA space -- and note the
#  two killing ports DO have a device behind them, so the pair brackets the question from both
#  sides.
#
#  Usage:  lca_isalane_probe.py <gxemul-binary> [label]
#          LCAISALANE_RAW=<dir>   -- optional: dump each session's raw pty transcript there
import os, sys, pty, select, time, re

BIN   = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"
MACH  = "alphabook1"          #  device_add(machine, "lca") is ST_ALPHABOOK1 ONLY
RAW   = os.environ.get("LCAISALANE_RAW", "")

rows = []
def row(name, got, want, note=""):
    ok = (got == want)
    rows.append((name, ok))
    print("%-14s %-24s %-24s %-56s %s" % (name, str(got), str(want), note, "ok" if ok else "FAIL"))
    return ok

# ---------------------------------------------------------------- encoder (memory format only)
ZERO, T0, T1, T2, T3, T4, T5, T6 = 31, 1, 2, 3, 4, 5, 6, 7
#  T6 is the highest used.  A probe reaching for an undefined register name dies with a NameError
#  rather than emitting a bad encoding, which is the safe direction (#516 found this the hard way).

def mem(op, ra, rb, disp):
    assert -32768 <= disp <= 32767, "displacement %d out of range" % disp
    return (op << 26) | (ra << 21) | (rb << 16) | (disp & 0xffff)

def LDA (ra, disp, rb=ZERO): return mem(0x08, ra, rb, disp)
def LDAH(ra, disp, rb=ZERO): return mem(0x09, ra, rb, disp)
def LDBU(ra, disp, rb):      return mem(0x0a, ra, rb, disp)   # BWX byte load  -> memory_rw len 1
def LDL (ra, disp, rb):      return mem(0x28, ra, rb, disp)   # longword load  -> memory_rw len 4
def LDQ (ra, disp, rb):      return mem(0x29, ra, rb, disp)   # quadword load  -> memory_rw len 8
def STB (ra, disp, rb):      return mem(0x0e, ra, rb, disp)   # BWX byte store -> memory_rw len 1
def LDWU(ra, disp, rb):      return mem(0x0c, ra, rb, disp)   # BWX word load  -> memory_rw len 2  (#530)
def STW (ra, disp, rb):      return mem(0x0d, ra, rb, disp)   # BWX word store -> memory_rw len 2  (#530)
#  LDBU/STB are opcodes 0x0a/0x0e and are decoded with `loadstore_type = 0' in
#  cpu_alpha_instr.c, which selects the 1-byte template in cpu_alpha_instr_loadstore.c -- so the
#  handler under test really does see len == 1.  Not a new capability: lca_irqstub_probe.py already
#  drives STB on this machine, and there is no BWX gate in this tree.

def load_const(reg, val):
    #  32-bit only, and deliberately so: this builds SCRATCH pointers and sentinels, never a
    #  64-bit operand.  Every 64-bit address this probe drives arrives via `put d' + LDQ.
    lo = val & 0xffff
    hi = (val >> 16) & 0xffff
    if lo >= 0x8000:
        hi = (hi + 1) & 0xffff
    ops = [LDAH(reg, hi if hi < 0x8000 else hi - 0x10000)]
    if lo:
        ops.append(LDA(reg, lo if lo < 0x8000 else lo - 0x10000, reg))
    return ops

SENT = 0x0bad1d8a         #  the pre-seed.  A load that FAULTS leaves this in the register.
#  #530: was 0x0bad1dea, whose low byte 0xea has bits 5-6 SET -- so `ofs1 zero', masked to
#  LSR_FIXED (0x60), read a declined load (sentinel kept) as the LSR byte and went GREEN under a
#  decline (measured on the F2 A variant, regress/artifacts/lcaisalane/opus_f2_20260913/).  0x8a
#  has bits 5-6 CLEAR.  Re-pinned FIRST, HEAD re-run 13/16 with the same three reds, THEN the fix
#  (the oracle-correction order; FABLE_F2_RULING_20260914.md R3).
def sent(reg): return load_const(reg, SENT)

# ---------------------------------------------------------------- addresses
K0SEG        = 0xfffffc0000000000
def k0(p):   return K0SEG | p

LCA_PCI_SIO  = 0x1c0000000               # alpha_lcareg.h; DEVINIT maps 0x10000<<5 bytes here as
                                         # "lca_isa" -- THE HANDLER UNDER TEST
LCA_ISA_BASE = LCA_PCI_SIO + 0x10000000  # dev_lca.c:47.  bus_isa_init put the real devices here,
                                         # and this is where the handler FORWARDS to.
def SP(port):   return LCA_PCI_SIO  + (port << 5)   # the guest-visible sparse address
def FLAT(port): return LCA_ISA_BASE + port          # the internal flat mapping

#  ---- the ports, and why each one ----------------------------------------------------------
KBC_CMD, KBC_DAT = 0x64, 0x60      # 8042: both 0 mod 4.  0xAA is the standard self-test command
KBC_SELFTEST, KBC_REPLY = 0xAA, 0x55
UART_LSR   = 0x3fd                 # 1 mod 4 -> ofs 1.  DEVICE_ACCESS(ns16550) sets
LSR_FIXED  = 0x60                  #   `d->reg[com_lsr] |= LSR_TXRDY | LSR_TSRE' at the TOP of
                                   #   every access, so 0x20|0x40 is there by construction, with
                                   #   no setup.  Masked to those two bits because LSR_RXRDY (0x01)
                                   #   tracks console input and is the one bit a stray keystroke
                                   #   could flip -- a witness must not have a race in its oracle.
UART_MSR   = 0x3fe                 # 2 mod 4 -> ofs 2.  Same handler unconditionally sets
MSR_FIXED  = 0xb0                  #   MSR_DCD|MSR_DSR|MSR_CTS = 0x80|0x20|0x10, and nothing else
                                   #   ever sets an MSR bit, so this is exact.
UART_SCR   = 0x3ff                 # 3 mod 4 -> ofs 3.  reg 7 falls to the ns16550 `default:' arm,
SCR_VALUE  = 0x5a                  #   which stores and returns the byte -- a plain scratchpad.
NODEV_PORT = 0x300                 # 0 mod 4, and bus_isa_init registers nothing at 0x300.

SCRATCH      = 0x01020000
CODE         = 0x01040000
assert max(SCRATCH, CODE) < 64 * 1024 * 1024, "scratch/code must be inside RAM"

DUMMY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alpha_dummy.bin")
if not os.path.exists(DUMMY):
    with open(DUMMY, "wb") as f:
        f.write(b"\0" * 8)

# ---------------------------------------------------------------- session
def session(cmds, settle, spin):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "alpha", "-e", MACH, "-M", "64",
                       "0x20000000:" + DUMMY])
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
                if not d:
                    return False
                buf += d.decode("latin-1", "replace")
            except OSError:
                return False
        return True
    alive = rd(settle)
    for i, c in enumerate(cmds):
        try:
            os.write(fd, (c + "\n").encode("latin-1"))
        except OSError:
            alive = False; break
        if not rd(spin if i == len(cmds) - 1 else 0.45):
            alive = False; break
    try:
        os.write(fd, b"quit\n"); rd(0.5)
    except OSError:
        pass
    try:
        os.close(fd)
    except OSError:
        pass
    return buf.replace("\r", ""), alive

def printed(t, reg):
    m = re.search(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
    return None if not m else int(m.group(1), 16)

def build(consts, phases):
    """consts -> SCRATCH slots 0,8,16,...   phases = list of (ops, printreg|None).
    Returns the debugger command list."""
    prog = load_const(T0, SCRATCH)
    lens = [len(prog)]
    for ops, _ in phases:
        prog += ops
        lens.append(len(ops))
    cmds  = ["put d 0x%x, 0x%x" % (SCRATCH + 8 * i, v) for i, v in enumerate(consts)]
    cmds += ["put w 0x%x, 0x%08x" % (k0(CODE) + 4 * i, op) for i, op in enumerate(prog)]
    cmds += ["pc=0x%x" % k0(CODE), "step %d" % lens[0]]
    for (ops, pr), n in zip(phases, lens[1:]):
        cmds.append("step %d" % n)
        if pr is not None:
            cmds.append("print %s" % pr)
    return cmds

def run(tag, consts, phases, want_regs, settle=3.0, spin=4.0):
    """want_regs: registers whose `print' MUST be present for the run to be READY.  A run that is
    not ready timed out rather than measured, and is retried ONCE with tripled patience -- the
    machine may be loaded.  Returns (txt, alive, retried)."""
    cmds = build(consts, phases)
    txt, alive = session(cmds, settle, spin)
    retried = False
    if not all(printed(txt, r) is not None for r in want_regs):
        retried = True
        txt, alive = session(cmds, settle * 3, spin * 3)
    if RAW:
        with open(os.path.join(RAW, "raw_%s.txt" % tag), "w", encoding="utf-8") as f:
            f.write("### cmds\n" + "\n".join(cmds) + "\n### transcript\n" + txt)
    return txt, alive, retried

def evidence(txt, tag):
    for _l in txt.split(chr(10)):
        if ("lca_isa access function" in _l or "lca:" in _l or "pckbc:" in _l
                or "non-existant" in _l):
            print("  EVIDENCE[%s]: %s" % (tag, _l.strip()))

def hx(v):
    return "absent" if v is None else "0x%x" % v

ATTRIB = "in lca_isa access function"     # unique in src/; the arm's own diagnostic

print("lca_isalane_probe -- binary=%s label=%s machine=%s" % (BIN, LABEL, MACH))
print("  sparse LCA_PCI_SIO=0x%x  flat LCA_ISA_BASE=0x%x  ofs = (r>>5) & 3 = port & 3"
      % (LCA_PCI_SIO, LCA_ISA_BASE))
print("%-14s %-24s %-24s %-56s %s" % ("row", "got", "want", "note", ""))

# ================================================================ SESSION 1: the surviving rows
#  [A] STB 0xAA -> sparse(0x64)      8042 command, ofs 0
#  [B] LDBU     <- sparse(0x60)      8042 data,    ofs 0   -> 0x55            `live'
#  [C] LDBU     <- flat(0x3fd)       LSR via the internal mapping             `ofs1 devsig'
#  [D] LDBU     <- sparse(0x3fd)     LSR, len 1, ofs 1 -> 0 on HEAD           `ofs1 zero'
#  [E] LDL      <- sparse(0x3fd)     LSR, len 4, ofs 1 -> byte in lane 1      `ofs1 wide'
#  [F] LDBU     <- sparse(0x300)     no device, ofs 0                         `ctl'
C1 = [k0(SP(KBC_CMD)), KBC_SELFTEST, k0(SP(KBC_DAT)), k0(FLAT(UART_LSR)),
      k0(SP(UART_LSR)), k0(SP(NODEV_PORT))]
P1 = [([LDQ(T1, 0, T0), LDQ(T2, 8, T0), STB(T2, 0, T1),
        LDQ(T1, 16, T0)] + sent(T3) + [LDBU(T3, 0, T1)], "t3"),
      ([LDQ(T1, 24, T0)] + sent(T4) + [LDBU(T4, 0, T1)], "t4"),
      ([LDQ(T1, 32, T0)] + sent(T5) + [LDBU(T5, 0, T1)], "t5"),
      ([LDQ(T1, 32, T0)] + sent(T6) + [LDL (T6, 0, T1)], "t6"),
      ([LDQ(T1, 40, T0)] + sent(T2) + [LDBU(T2, 0, T1)], "t2")]
t1x, a1, r1 = run("base", C1, P1, ["t3", "t4", "t5", "t6", "t2"])
b_live, b_flat, b_byte, b_wide, b_ctl = (printed(t1x, r) for r in ("t3", "t4", "t5", "t6", "t2"))
print("  RAW[base]: live=%s flatLSR=%s sparseLSR=%s wideLSR=%s nodev=%s alive=%s retried=%s"
      % (hx(b_live), hx(b_flat), hx(b_byte), hx(b_wide), hx(b_ctl), a1, r1))

row("base alive", "alive" if a1 else "dead", "alive",
    "CONTROL: nothing in this session may end the host")

#  ---- LIVENESS + DEVICE SIGNATURE, through the handler under test ---------------------------
#  Only the 8042 answers 0x55 to a load from ISA 0x60 after 0xAA reached ISA 0x64.  RAM and
#  unmapped space cannot, and this proves the SPARSE window reaches devices at all.
row("live", hx(b_live), hx(KBC_REPLY),
    "LIVENESS+DEVSIG: 8042 self-test reply, THROUGH lca_isa at ofs 0")

#  ---- the device byte exists, taken through the OTHER mapping --------------------------------
row("ofs1 devsig", hx(None if b_flat is None else b_flat & LSR_FIXED), hx(LSR_FIXED),
    "DEVSIG: TXRDY|TSRE are set by the ns16550 handler on every access")

#  ---- THE DEFECT ROW -------------------------------------------------------------------------
#  ORACLE POLARITY is the witness ladder's: assert the CORRECT behaviour, so this is RED pre-fix
#  and GREEN post-fix with the SAME script.  WANT = THE DEVICE BYTE.  For len == 1 the caller's
#  buffer has exactly one lane and it is data[0]; `i == ofs' with ofs 1 selects nothing, so the
#  byte is dropped.  (A DECLINE is the other defensible disposition and would also red this row --
#  which is correct: a decline must not be reported as a successful read of zero.  What a fix may
#  NOT do is keep answering a false zero.)
row("ofs1 zero", hx(None if b_byte is None else b_byte & LSR_FIXED),
    hx(None if b_flat is None else b_flat & LSR_FIXED),
    "*** DEFECT: byte read of ISA 0x3fd (LSR) -- port 1 mod 4 -> ofs 1 ***")

#  ---- the zero is an ANSWER, not a fault -----------------------------------------------------
#  A load whose memory_rw fails returns before writeback (cpu_alpha_instr_loadstore.c), leaving
#  the sentinel.  This row says which of the two happened, and on HEAD it is a FALSE SUCCESS.
row("ofs1 answer", "completed" if (b_byte is not None and b_byte != SENT) else "faulted/absent",
    "completed",
    "the handler returned 1: the guest was ANSWERED zero, not refused")

#  ---- the byte DOES reach the packing loop ---------------------------------------------------
#  Same address, same process, len 4 instead of 1: ofs 1 <= 4, so the loop writes data[1] and the
#  guest sees the byte shifted into lane 1.  This is what makes `ofs1 zero' a lane-packing finding
#  rather than "the sparse window does not reach the UART".
row("ofs1 wide", hx(None if b_wide is None else (b_wide >> 8) & LSR_FIXED), hx(LSR_FIXED),
    "SAME ADDRESS at len 4: the device byte lands in lane 1 -- so it arrived")

#  ---- the negative control for the window ----------------------------------------------------
row("ctl", "alive" if a1 else "dead", "alive",
    "CONTROL: byte access to an ISA port with NO device, ofs 0, survives")
row("ctl zero", hx(b_ctl), hx(0),
    "CONTROL: and it answers zero -- so zero alone proves nothing (see ofs1 devsig)")
evidence(t1x, "base")
print("")

# ================================================================ SESSION 2: ofs 2 ends the host
#  [A] LDBU <- flat(0x3fe)     MSR through the internal mapping   -> 0xb0
#  [B] LDL  <- sparse(0x3fe)   MSR, len 4, ofs 2 -> byte in lane 2, SURVIVES
#  [C] LDBU <- sparse(0x3fe)   MSR, len 1, ofs 2 -> 2 > 1 -> exit(1)
C2 = [k0(FLAT(UART_MSR)), k0(SP(UART_MSR))]
P2 = [([LDQ(T1, 0, T0)] + sent(T2) + [LDBU(T2, 0, T1)], "t2"),
      ([LDQ(T1, 8, T0)] + sent(T3) + [LDL (T3, 0, T1)], "t3"),
      ([LDQ(T1, 8, T0)] + sent(T4) + [LDBU(T4, 0, T1)], None)]
t2x, a2, r2 = run("ofs2", C2, P2, ["t2", "t3"])
m_flat, m_wide = printed(t2x, "t2"), printed(t2x, "t3")
print("  RAW[ofs2]: flatMSR=%s wideMSR=%s alive=%s retried=%s" % (hx(m_flat), hx(m_wide), a2, r2))

row("ofs2 devsig", hx(m_flat), hx(MSR_FIXED),
    "DEVSIG: DCD|DSR|CTS are set by the ns16550 handler on every access")
row("ofs2 wide", hx(None if m_wide is None else (m_wide >> 16) & 0xff), hx(MSR_FIXED),
    "CONTROL: the SAME sparse address at len 4 survives and packs lane 2")
row("ofs2 exit", "alive" if a2 else "dead", "alive",
    "*** DEFECT: byte read of ISA 0x3fe (MSR) -- port 2 mod 4 -> ofs 2 ***")
row("ofs2 attrib", "yes" if (a2 or ATTRIB in t2x) else "died-elsewhere", "yes",
    "ATTRIBUTION: a death here must carry the arm's own diagnostic")
evidence(t2x, "ofs2")
print("")

# ================================================================ SESSION 3: ofs 3 ends the host
#  [A] STB 0x5a -> flat(0x3ff);  LDBU <- flat(0x3ff)   scratch register, through the flat mapping
#  [B] LDL  <- sparse(0x3ff)     len 4, ofs 3 -> byte in lane 3, SURVIVES
#  [C] LDBU <- sparse(0x3ff)     len 1, ofs 3 -> 3 > 1 -> exit(1)
C3 = [k0(FLAT(UART_SCR)), SCR_VALUE, k0(SP(UART_SCR))]
P3 = [([LDQ(T1, 0, T0), LDQ(T2, 8, T0), STB(T2, 0, T1)] + sent(T3) + [LDBU(T3, 0, T1)], "t3"),
      ([LDQ(T1, 16, T0)] + sent(T4) + [LDL (T4, 0, T1)], "t4"),
      ([LDQ(T1, 16, T0)] + sent(T5) + [LDBU(T5, 0, T1)], None)]
t3x, a3, r3 = run("ofs3", C3, P3, ["t3", "t4"])
s_flat, s_wide = printed(t3x, "t3"), printed(t3x, "t4")
print("  RAW[ofs3]: flatSCR=%s wideSCR=%s alive=%s retried=%s" % (hx(s_flat), hx(s_wide), a3, r3))

row("ofs3 devsig", hx(s_flat), hx(SCR_VALUE),
    "DEVSIG: the ns16550 scratchpad returns the byte just written to it")
row("ofs3 wide", hx(None if s_wide is None else (s_wide >> 24) & 0xff), hx(SCR_VALUE),
    "CONTROL: the SAME sparse address at len 4 survives and packs lane 3")
row("ofs3 exit", "alive" if a3 else "dead", "alive",
    "*** DEFECT: byte read of ISA 0x3ff (scratch) -- port 3 mod 4 -> ofs 3 ***")
row("ofs3 attrib", "yes" if (a3 or ATTRIB in t3x) else "died-elsewhere", "yes",
    "ATTRIBUTION: a death here must carry the arm's own diagnostic")
evidence(t3x, "ofs3")
print("")

# ================================================================ #530: THE DETECTOR SESSIONS
#  Everything above is the rung-3 WITNESS, unchanged except for the sentinel.  Everything below is
#  the DETECTOR for the #530 fix (disposition B, FABLE_F2_RULING_20260914.md): the byte for port P
#  sits at buffer position `(P & 3) % len' on BOTH arms -- the rule HEAD already ran at every served
#  cell -- so no access ends the host and none is answered with a discarded byte.  Each row names
#  the enumerated mutant it kills (R3's table) and the channel: a FULL-REGISTER read (so a declined
#  load, which keeps the sentinel, and a replicated or mis-laned byte all differ from the want), or
#  a store read back through the FLAT mapping, which is a plain forward independent of the handler.
#
#  Ports: LSR 0x3fd (1 mod 4; TXRDY|TSRE forced), MSR 0x3fe (2 mod 4; reads reg|0xb0), IER 0x3f9
#  (1 mod 4; stores and returns the byte), SCR 0x3ff (3 mod 4; scratch).
UART_IER = 0x3f9

def prints_in_order(txt):
    #  The detector sessions reuse register names, so values are taken IN PRINT ORDER rather than
    #  by name (printed() returns the FIRST match, which would read an earlier phase's value).
    return [int(v, 16) for _, v in re.findall(r"print\s+(t\d)\s*\n\s*(0x[0-9a-f]+)", txt)]

def dsession(tag, consts, phases, names, settle=3.0, spin=4.0):
    """Returns (alive, {name: value|None}).  A run that did not produce every print is retried ONCE
    with tripled patience -- the load-tolerance rule the witness sessions already follow."""
    need = sum(1 for _, pr in phases if pr is not None)
    cmds = build(consts, phases)
    txt, alive = session(cmds, settle, spin)
    if len(prints_in_order(txt)) < need and alive:
        txt, alive = session(cmds, settle * 3, spin * 3)
    if RAW:
        with open(os.path.join(RAW, "raw_%s.txt" % tag), "w", encoding="utf-8") as f:
            f.write("### cmds\n" + "\n".join(cmds) + "\n### transcript\n" + txt)
    vals = prints_in_order(txt)
    got = {n: (vals[i] if i < len(vals) else None) for i, n in enumerate(names)}
    print("  RAW[%s]: alive=%s %s" % (tag, alive, " ".join("%s=%s" % (n, hx(got[n])) for n in names)))
    evidence(txt, tag)
    return alive, got

#  ---- SESSION 4: the cells that never ended the host (no mutant in the table can kill them) --
#  slots: 0 SP(LSR) 1 FLAT(LSR) 2 SP(MSR) 3 FLAT(MSR) 4 SP(IER) 5 FLAT(IER)
C4 = [k0(SP(UART_LSR)), k0(FLAT(UART_LSR)), k0(SP(UART_MSR)), k0(FLAT(UART_MSR)),
      k0(SP(UART_IER)), k0(FLAT(UART_IER))]
P4 = [([LDQ(T1, 8, T0)]  + sent(T2) + [LDBU(T2, 0, T1)], "t2"),                 # lsr  (flat)
      ([LDQ(T1, 0, T0)]  + sent(T3) + [LDBU(T3, 0, T1)], "t3"),                 # r11  len 1 ofs 1
      ([LDQ(T1, 0, T0)]  + sent(T4) + [LDWU(T4, 0, T1)], "t4"),                 # r21  len 2 ofs 1
      ([LDQ(T1, 0, T0)]  + sent(T5) + [LDQ (T5, 0, T1)], "t5"),                 # r81  len 8, P%8 == 5
      ([LDQ(T1, 24, T0)] + sent(T6) + [LDBU(T6, 0, T1)], "t6"),                 # msr  (flat)
      ([LDQ(T1, 16, T0)] + sent(T2) + [LDWU(T2, 0, T1)], "t2"),                 # r22  len 2 ofs 2
      (load_const(T3, 0x3a) + [LDQ(T1, 32, T0), STB(T3, 0, T1),
       LDQ(T1, 40, T0)] + sent(T4) + [LDBU(T4, 0, T1)], "t4"),                  # w11  STB -> IER
      (load_const(T3, 0x5a00) + [LDQ(T1, 32, T0), STW(T3, 0, T1),
       LDQ(T1, 40, T0)] + sent(T5) + [LDBU(T5, 0, T1)], "t5"),                  # w21  STW -> IER
      (load_const(T3, 0x0040) + [LDQ(T1, 16, T0), STW(T3, 0, T1),
       LDQ(T1, 24, T0)] + sent(T6) + [LDBU(T6, 0, T1)], "t6")]                  # w22  STW -> MSR
a4, g4 = dsession("fold", C4, P4, ["lsr", "r11", "r21", "r81", "msr", "r22", "w11", "w21", "w22"])
lsr = g4["lsr"]
row("fold alive", "alive" if a4 else "dead", "alive",
    "CONTROL: none of these cells ever ended the host")
row("r11 byte", hx(g4["r11"]), hx(lsr),
    "(1,1) LDBU LSR, FULL register == the flat LSR: kills the A decline (sentinel) + C/HEAD (0)")
row("r21 anchor", hx(g4["r21"]), hx(None if lsr is None else lsr << 8),
    "(2,1) LDWU LSR: position 1 on HEAD and after -- the P mod len ANCHOR; kills replicate/lane edits")
row("r81 lane", hx(g4["r81"]), hx(None if lsr is None else lsr << 8),
    "(8,1) LDQ LSR, port 5 mod 8: lane 1, not 5 -- kills dropping the `& 3' (m_nomask)")
row("r22 byte", hx(g4["r22"]), hx(g4["msr"]),
    "(2,2) LDWU MSR == flat MSR at position 0: kills the A decline and C/HEAD's discarded byte")
row("w11 lands", hx(g4["w11"]), hx(0x3a),
    "(1,1) STB 0x3a -> IER, flat readback: lands on HEAD -- kills the A decline (F3)")
row("w21 lane", hx(g4["w21"]), hx(0x5a),
    "(2,1) STW 0x5a00 -> IER forwards position 1 on HEAD and after")
row("w22 lands", hx(g4["w22"]), hx(0x40 | MSR_FIXED),
    "(2,2) STW 0x0040 -> MSR, flat readback reg|0xb0: lands on HEAD -- kills the A decline")
print("")

#  ---- SESSIONS 5-10: the six cells that ENDED THE HOST on HEAD, one process each -------------
#  A mutant that reinstates the exit ends exactly one of these, so each gets its own process and
#  its own `alive' row -- and a value row, because `alive' greens equally for a decline (the C and A
#  mutants), so the value is what separates the fix from them.
EXITS = [
  #  tag   consts                                              phases                                      names            rows (name, key, want-fn, note)
  ("r12", [k0(FLAT(UART_MSR)), k0(SP(UART_MSR))],
          [([LDQ(T1, 0, T0)] + sent(T2) + [LDBU(T2, 0, T1)], "t2"),
           ([LDQ(T1, 8, T0)] + sent(T3) + [LDBU(T3, 0, T1)], "t3")],
          ["msr", "r12"],
          [("r12 byte", "r12", lambda g: g["msr"],
            "(1,2) LDBU MSR == flat MSR: was host death; kills C/A (sentinel)")]),
  ("r13", [k0(FLAT(UART_SCR)), SCR_VALUE, k0(SP(UART_SCR))],
          [([LDQ(T1, 0, T0), LDQ(T2, 8, T0), STB(T2, 0, T1),
             LDQ(T1, 16, T0)] + sent(T3) + [LDBU(T3, 0, T1)], "t3")],
          ["r13"],
          [("r13 byte", "r13", lambda g: SCR_VALUE,
            "(1,3) LDBU SCR after a flat store of 0x5a: was host death; kills C/A")]),
  ("r23", [k0(FLAT(UART_SCR)), SCR_VALUE, k0(SP(UART_SCR))],
          [([LDQ(T1, 0, T0), LDQ(T2, 8, T0), STB(T2, 0, T1),
             LDQ(T1, 16, T0)] + sent(T3) + [LDWU(T3, 0, T1)], "t3")],
          ["r23"],
          [("r23 lane", "r23", lambda g: SCR_VALUE << 8,
            "(2,3) LDWU SCR -> position 1, paired with `r21 anchor': kills the clamp (position 0)")]),
  ("w12", [k0(SP(UART_MSR)), k0(FLAT(UART_MSR))],
          [(load_const(T3, 0x40) + [LDQ(T1, 0, T0), STB(T3, 0, T1),
            LDQ(T1, 8, T0)] + sent(T4) + [LDBU(T4, 0, T1)], "t4")],
          ["w12"],
          [("w12 lands", "w12", lambda g: 0x40 | MSR_FIXED,
            "(1,2) STB 0x40 -> MSR, flat readback: was host death; kills C/A (store dropped)")]),
  ("w13", [k0(SP(UART_SCR)), k0(FLAT(UART_SCR))],
          [(load_const(T3, 0x3c) + [LDQ(T1, 0, T0), STB(T3, 0, T1),
            LDQ(T1, 8, T0)] + sent(T4) + [LDBU(T4, 0, T1)], "t4"),
           ([LDQ(T1, 0, T0)] + sent(T5) + [LDBU(T5, 0, T1)], "t5")],
          ["w13", "w13rt"],
          [("w13 lands", "w13", lambda g: 0x3c,
            "(1,3) STB 0x3c -> SCR, flat readback: was host death; kills C/A and the unfolded write"),
           ("w13 roundtrip", "w13rt", lambda g: 0x3c,
            "SELF-COHERENCE: stb then ldbu at ONE sparse address returns what was stored")]),
  ("w23", [k0(SP(UART_SCR)), k0(FLAT(UART_SCR))],
          [(load_const(T3, 0x7e00) + [LDQ(T1, 0, T0), STW(T3, 0, T1),
            LDQ(T1, 8, T0)] + sent(T4) + [LDBU(T4, 0, T1)], "t4")],
          ["w23"],
          [("w23 lane", "w23", lambda g: 0x7e,
            "(2,3) STW 0x7e00 -> SCR forwards position 1 (as `w21 lane'): kills the clamp")]),
]
for tag, consts, phases, names, rws in EXITS:
    ax, gx = dsession(tag, consts, phases, names)
    row("%s alive" % tag, "alive" if ax else "dead", "alive",
        "was a host death on HEAD (`ofs > len'); kills the reinstated exit")
    for nm, key, wantf, note in rws:
        w = wantf(gx)
        row(nm, hx(gx[key]), hx(w), note)
    print("")

# ---------------------------------------------------------------- summary
#  Computed adjacent to the print on purpose: #516 shipped a probe whose numerator was counted
#  over an older row set while the denominator was evaluated at print time, and every row said
#  `ok' beside a summary that did not.
ok = sum(1 for _, o in rows if o)
retr = ",".join(t for t, r in (("base", r1), ("ofs2", r2), ("ofs3", r3)) if r)
print("")
print("LCAISALANE_RETRIED=%s" % (retr if retr else "none"))
print("LCAISALANE_RESULT=%d/%d" % (ok, len(rows)))
print("LCAISALANE_WITNESS=%s" % ("PASS" if ok == len(rows) else "FAIL"))
print("LCAISALANE_DONE")
sys.exit(0 if ok == len(rows) else 1)
