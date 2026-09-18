#!/usr/bin/env python3
#  opus_c2_demo.py -- assembled from lca_isalane_probe.py lines 157-337 and 467-494 (helpers, verbatim) + demo_tail.part
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

# ================================================================ OPUS closing-pass-2 DISCRIMINATOR (not a detector)
#  Two channels the 77-row probe has no row on, each on an UNMODIFIED alphabook1:
#   [iir]    a store through lca_isa to ISA 0x3fa (the ns16550 FCR/IIR port, lane 2).  dev_ns16550.c's com_iir READ
#            arm clears IIR_TXRDY -- a read side effect -- so a write arm that falls through into the read arm
#            (x_wfallthru) loses a pending transmitter-ready interrupt.  Channel: flat LDBU of IIR, masked 0x03.
#   [tailr]/[tailw]  the split TAIL cells (len 7,6,5,3 at lane 0) at a MAPPED port: an unaligned LDQ/STQ at
#            SP(0x5f) + 0x1f/0x1e/0x1d/0x1b splits at 1 KB into a head at port 0x5f (lane 3, unmapped) and a tail at
#            port 0x60 -- the 8042 DATA port.  Read channel: 0x55 (self-test reply) lands at register byte h (the head
#            length).  Write channel: the 8042 command byte (K_LDCMDBYTE 0x60 then the tail's forwarded byte, read
#            back with K_RDCMDBYTE 0x20 through the FLAT mapping).
print("opus_c2_demo -- binary=%s label=%s" % (BIN, LABEL))
UART_IIR = 0x3fa

def arm():
    #  IER 0 -> ETXRDY: dev_ns16550.c's com_ier write arm sets IIR_TXRDY on that transition
    return load_const(T3, 0x02) + [LDQ(T1, 0, T0), STB(ZERO, 0, T1), STB(T3, 0, T1)]
CI = [k0(FLAT(UART_IER)), k0(FLAT(UART_IIR)), k0(SP(UART_IIR))]
PI = [(arm() + [LDQ(T1, 8, T0)] + sent(T2) + [LDBU(T2, 0, T1)], "t2"),                       # control, no lca store
      (arm() + [LDQ(T1, 16, T0), STB(ZERO, 0, T1), LDQ(T1, 8, T0)] + sent(T4) + [LDBU(T4, 0, T1)], "t4"),   # STB (1,2)
      (arm() + [LDQ(T1, 16, T0), STL(ZERO, 0, T1), LDQ(T1, 8, T0)] + sent(T5) + [LDBU(T5, 0, T1)], "t5")]   # STL (4,2)
ai, gi = dsession("iir", CI, PI, ["ctl", "stb", "stl"])
m3 = lambda v: None if v is None else v & 0x03
row("iir alive", "alive" if ai else "dead", "alive", "CONTROL")
row("iir ctl", hx(m3(gi["ctl"])), hx(0x02), "CONTROL: IER 0->ETXRDY sets IIR_TXRDY, flat IIR & 3 = TXRDY")
row("iir stb", hx(m3(gi["stb"])), hx(0x02), "(1,2) STB 0 -> SP(0x3fa) FCR: TXRDY must survive the store")
row("iir stl", hx(m3(gi["stl"])), hx(0x02), "(4,2) STL 0 -> SP(0x3fa) FCR: TXRDY must survive the store")
print("")

HEADS = ((1, 0x1f), (2, 0x1e), (3, 0x1d), (5, 0x1b))   # (head length h, byte offset) -> tail len 8-h at port 0x60
CR = [k0(FLAT(KBC_CMD)), KBC_SELFTEST, k0(SP(KBC_DAT))] + [k0(SP(0x5f) + o) for _, o in HEADS]
def selftest(): return [LDQ(T1, 0, T0), LDQ(T2, 8, T0), STB(T2, 0, T1)]
PR = [(selftest() + [LDQ(T1, 16, T0)] + sent(T3) + [LDQ(T3, 0, T1)], "t3")]                   # control: aligned (8,0)
for i in range(len(HEADS)):
    PR.append((selftest() + [LDQ(T1, 24 + 8 * i, T0)] + sent(T4) + [LDQ(T4, 0, T1)], "t4"))
ar, gr = dsession("tailr", CR, PR, ["ctl"] + ["t%d" % (8 - h) for h, _ in HEADS])
row("tailr alive", "alive" if ar else "dead", "alive", "CONTROL")
row("tailr ctl", hx(gr["ctl"]), hx(KBC_REPLY), "CONTROL: aligned LDQ at SP(0x60), the (8,0) cell, reads 0x55")
for h, _ in HEADS:
    row("tailr t%d" % (8 - h), hx(gr["t%d" % (8 - h)]), hx(KBC_REPLY << (8 * h)),
        "(%d,0) TAIL at port 0x60: position 0 -> register byte %d" % (8 - h, h))
print("")

def v(h): return (0x44 << (8 * h)) | (0x21 << (8 * (h + 1)))   # tail position 0 = 0x44, position 1 = 0x21
CW = [k0(FLAT(KBC_CMD)), 0x60, 0x20, k0(FLAT(KBC_DAT))] + [k0(SP(0x5f) + o) for _, o in HEADS] + [v(h) for h, _ in HEADS]
def ldcmd(): return [LDQ(T1, 0, T0), LDQ(T2, 8, T0), STB(T2, 0, T1)]
def rdcmd(): return [LDQ(T1, 0, T0), LDQ(T2, 16, T0), STB(T2, 0, T1), LDQ(T1, 24, T0)]
PW = [(ldcmd() + load_const(T3, 0x04) + [LDQ(T1, 24, T0), STB(T3, 0, T1)] + rdcmd() + sent(T4) + [LDBU(T4, 0, T1)], "t4")]
for i in range(len(HEADS)):
    PW.append((ldcmd() + [LDQ(T3, 64 + 8 * i, T0), LDQ(T1, 32 + 8 * i, T0), STQ(T3, 0, T1)] + rdcmd()
               + sent(T5) + [LDBU(T5, 0, T1)], "t5"))
aw, gw = dsession("tailw", CW, PW, ["ctl"] + ["t%d" % (8 - h) for h, _ in HEADS])
row("tailw alive", "alive" if aw else "dead", "alive", "CONTROL")
row("tailw ctl", hx(gw["ctl"]), hx(0x04), "CONTROL: flat cmdbyte round trip")
for h, _ in HEADS:
    row("tailw t%d" % (8 - h), hx(gw["t%d" % (8 - h)]), hx(0x44),
        "(%d,0) STQ TAIL at port 0x60 forwards position 0 (0x44), not 1 (0x21)" % (8 - h))
print("")

ok = sum(1 for _, o in rows if o)
print("OPUSC2_RETRIED=%s" % (",".join(DRETRIED) if DRETRIED else "none"))
print("OPUSC2_RESULT=%d/%d" % (ok, len(rows)))
print("OPUSC2_DONE")
