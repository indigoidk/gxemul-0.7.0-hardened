#!/usr/bin/env python3
#  opus_c2_demo2.py -- lca_isalane_probe.py lines 157-337 and 467-494 (helpers, verbatim) + demo2_tail.part
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
def STL (ra, disp, rb):      return mem(0x2c, ra, rb, disp)   # longword store -> memory_rw len 4  (#530 pass 2)
def STQ (ra, disp, rb):      return mem(0x2d, ra, rb, disp)   # quadword store -> memory_rw len 8  (#530 pass 2)
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
UART_IER = 0x3f9
UART_MCR = 0x3fc              # 0 mod 4: modem control, stores and returns its low bits (pass 2)
DRETRIED = []

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
        #  recorded since pass 2 (Opus): before it, this retry was SILENT and LCAISALANE_RETRIED reported
        #  only the three witness sessions
        DRETRIED.append(tag)
        txt, alive = session(cmds, settle * 3, spin * 3)
    if RAW:
        with open(os.path.join(RAW, "raw_%s.txt" % tag), "w", encoding="utf-8") as f:
            f.write("### cmds\n" + "\n".join(cmds) + "\n### transcript\n" + txt)
    vals = prints_in_order(txt)
    got = {n: (vals[i] if i < len(vals) else None) for i, n in enumerate(names)}
    print("  RAW[%s]: alive=%s %s" % (tag, alive, " ".join("%s=%s" % (n, hx(got[n])) for n in names)))
    evidence(txt, tag)
    return alive, got

# ================================================================ OPUS closing-pass-2 DISCRIMINATOR 2 (panel mutants K1, C1)
#   [k1]  an unaligned LDQ at SP(0x3ff) + 0x1c splits into a 4-byte head at port 0x3ff (lane 3) and a 4-byte TAIL at
#         port 0x400 (lane 0, unmapped).  Base: 0x5a at register byte 3, tail zero.  K1 declines the tail, so the whole
#         load is abandoned and the register keeps its sentinel.  Also a direct LDL at SP(0x400) (len 4 at 0x400).
#   [c1]  STQ 0x04 via SP(MSR 0x3fe) (len 8, lane 2): position 2 is 0x00.  Base forwards 0 -> MSR 0 -> flat read 0xb0;
#         C1 forwards data[0] = 0x04 when data[2] == 0 -> flat read 0xb4.  Then STL 0x04 (len 4, lane 2), same.
print("opus_c2_demo2 -- binary=%s label=%s" % (BIN, LABEL))
CK = [k0(FLAT(UART_SCR)), SCR_VALUE, k0(SP(UART_SCR) + 0x1c), k0(SP(0x400))]
PK = [([LDQ(T1, 0, T0), LDQ(T2, 8, T0), STB(T2, 0, T1), LDQ(T1, 16, T0)] + sent(T3) + [LDQ(T3, 0, T1)], "t3"),
      ([LDQ(T1, 24, T0)] + sent(T4) + [LDL(T4, 0, T1)], "t4")]
ak, gk = dsession("k1", CK, PK, ["h4", "l400"])
row("k1 alive", "alive" if ak else "dead", "alive", "CONTROL")
row("k1 h4tail4", hx(gk["h4"]), hx(SCR_VALUE << 24), "LDQ SP(SCR)+0x1c: head (4,3) 0x5a at byte 3, tail (4,0) @0x400 zero")
row("k1 ldl400", hx(gk["l400"]), hx(0), "LDL SP(0x400): (4,0) at an unmapped port answers zero (not a fault)")
print("")

CC = [k0(FLAT(UART_MSR)), k0(SP(UART_MSR))]
PC = [([LDQ(T1, 0, T0), STB(ZERO, 0, T1)] + load_const(T3, 0x04) + [LDQ(T1, 8, T0), STQ(T3, 0, T1),
        LDQ(T1, 0, T0)] + sent(T4) + [LDBU(T4, 0, T1)], "t4"),
      ([LDQ(T1, 0, T0), STB(ZERO, 0, T1)] + load_const(T3, 0x04) + [LDQ(T1, 8, T0), STL(T3, 0, T1),
        LDQ(T1, 0, T0)] + sent(T5) + [LDBU(T5, 0, T1)], "t5")]
ac, gc = dsession("c1", CC, PC, ["q", "l"])
row("c1 alive", "alive" if ac else "dead", "alive", "CONTROL")
row("c1 stq", hx(gc["q"]), hx(MSR_FIXED), "(8,2) STQ 0x04 -> MSR: position 2 is 0 -> flat MSR 0xb0")
row("c1 stl", hx(gc["l"]), hx(MSR_FIXED), "(4,2) STL 0x04 -> MSR: position 2 is 0 -> flat MSR 0xb0")
print("")

ok = sum(1 for _, o in rows if o)
print("OPUSC2_RETRIED=%s" % (",".join(DRETRIED) if DRETRIED else "none"))
print("OPUSC2_RESULT=%d/%d" % (ok, len(rows)))
print("OPUSC2_DONE")
