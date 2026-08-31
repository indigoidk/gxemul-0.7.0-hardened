#!/usr/bin/env python3
"""
sgi_re_unmapped_probe.py -- RUNG-3 witness for `sgireunmapped`.

WHAT IS BEING WITNESSED
    DEVICE_ACCESS(sgi_re)'s final `else' (the window-cascade catch-all) prints a
    fatal() and calls a bare exit(1), with NO width predicate and no direction
    predicate.  Any access to an unmatched address inside the device's own
    registered window -- 2080 of the 4096 -- ends the HOST process.

WHY THIS IS RUNG 3 AND NOT LOWER
    Every access below is a GENUINE GUEST INSTRUCTION (`sw'/`lw' executed by
    `step') on the UNMODIFIED in-tree machine description `-E sgi -e ip32'.
    No device is added, no machine file is edited, and no debugger `put d' is
    used to touch the device -- `put w' writes only scratch RAM (instruction
    stubs).  The carrier forbids witnessing a device effect with `put d'
    because it bypasses the guest instruction path; that rule is obeyed here.

CONTROLS (a witness with one control has already fooled this project once --
the footbridge probe returned 0x0 everywhere WITH its RAM control green)
    LIVENESS       : row `live ram'  -- a known value round-trips through the
                     same guest store/load machinery into scratch RAM.
    DEVICE SIGNATURE: row `devsig lina' -- a 4-byte store to a MAPPED RE window
                     is DECLINED by #497's width guard and announces itself with
                     text only this device emits.  RAM answers silently.  So the
                     store demonstrably reaches THIS handler through real decode.
    NEIGHBOUR      : row `devsig destat' -- a guest load from the sibling
                     de_status device returns the CRIME_DE_*_IDLE bit pattern,
                     a value RAM at that address could not produce.

ORACLE
    The host's own exit status, taken with wait_exit() BEFORE close() signals
    anything.  ("exit",1) is the defect; ("running",None) is a survivor.
    A survival-only oracle would be vacuous here, so every kill row ALSO pins
    the device's message text and the exact relative address it reports.
"""
import os, sys, time

sys.path.insert(0, "/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad")
from gxprobe import Emu, EmuDied, INSTR

BIN   = "/mnt/c/DocumentNoSnc/cc/GXEMUL/build/gxemul"
HERE  = os.path.dirname(os.path.abspath(__file__))
NOPS  = os.path.join(HERE, "nops.bin")
SCRATCH = 0xffffffff80010000

# KSEG1 (uncached, unmapped) on 64-bit MIPS = 0xffffffffa0000000 | phys
def kseg1(phys):
    return 0xffffffffa0000000 | phys

RE_BASE   = 0x15001000          # memory_device_register(... baseaddr+0x1000 ...)
DESTAT    = 0x15004000          # sibling device, dev_sgi_de_status

rows = []
def row(name, got, want, note):
    ok = (got == want)
    rows.append((name, got, want, ok, note))
    print("  %-16s got=%-34s want=%-34s %s   %s" %
          (name, str(got), str(want), "ok" if ok else "FAILED", note))
    return ok

def new_emu(tag):
    e = Emu(BIN,
            ["-E", "sgi", "-e", "ip32", "-V",
             "0x%x:%s" % (SCRATCH, NOPS)],
            log_path=os.path.join(HERE, "log_%s.txt" % tag),
            boot_wait=3.0)
    return e

def status_of(e):
    """How did the host die?  Reap on the child's own terms first."""
    st = e.wait_exit(1.5)
    return st

# ---------------------------------------------------------------- section 1
print("SGI_RE_UNMAPPED RUNG-3 WITNESS")
print("binary : %s" % BIN)
print("machine: -E sgi -e ip32   (unmodified in-tree machine description)")
print()
print("[1] CONTROLS -- these must hold or nothing below means anything")

e = new_emu("controls")
try:
    # ---- LIVENESS: value round-trips through the same guest instructions
    e.guest_store32(SCRATCH + 0x200, 0xdeadbeef)
    v = e.guest_load32(SCRATCH + 0x200)
    row("live ram", "0x%x" % (v or 0), "0xdeadbeef",
        "guest sw/lw round-trip in RAM")

    # ---- endianness / stub sanity
    row("endian", e.detect_endian(), "big", "IP32 is big-endian")

    # ---- DEVICE SIGNATURE: a 4-byte store to a MAPPED RE window is declined
    #      by #497's width guard and announces itself.  RAM is silent.
    n0 = e.count("CRIME_RE_LINEAR_A")
    e.guest_store32(kseg1(RE_BASE + 0x700), 0x11223344)   # relative 0x1700
    n1 = e.count("CRIME_RE_LINEAR_A")
    row("devsig lina", n1 - n0, 1,
        "sw to MAPPED 0x1700 -> #497 width decline, device-only text")
    st = status_of(e)
    row("lina survives", st[0], "running", "declined access must NOT kill")

    # ---- NEIGHBOUR device: a value RAM could not produce
    v = e.guest_load32(kseg1(DESTAT))
    row("devsig destat", "0x%x" % (v or 0), "0x1e000000",
        "sibling de_status CRIME_DE_*_IDLE bits")

    # ---- ENCODING CHECK: the hand-assembled sd/ld must be what we think.
    #      The carrier records four incidents where a wrong instruction field
    #      silently produced a plausible zero; check against the debugger.
    for nm, w, want in (("sb", 0xa0220000, "sb"), ("sw", 0xac220000, "sw"),
                        ("sd", 0xfc220000, "sd"), ("lw", 0x8c220000, "lw"),
                        ("ld", 0xdc220000, "ld")):
        a = e.word_at(w)
        _, txt = e.disasm_word(a)
        row("enc %s" % nm, txt.split()[0] if txt else "?", want,
            "0x%08x disassembles as %s" % (w, want))
finally:
    e.close()

# ---------------------------------------------------------------- section 2
print()
print("[2] THE DEFECT -- one fresh session per kill (the host does not survive)")

# Widths are enumerated rather than argued: the six window arms accept ONLY
# len==8 and decline everything else, so if the catch-all had a width predicate
# patterned on them, len=1 and len=4 would DECLINE here rather than kill.
# sb=1, sw=4, sd=8.  Encodings verified against the debugger's own unassemble
# in section 0 below.
W_SB = 0xa0220000   # sb v0,0(at)
W_SW = 0xac220000   # sw v0,0(at)
W_SD = 0xfc220000   # sd v0,0(at)
W_LW = 0x8c220000   # lw v0,0(at)
W_LD = 0xdc220000   # ld v0,0(at)

def do_access(e, word, addr, val=0x5a5a5a5a):
    """One genuine guest instruction at `addr`."""
    e.set_reg("v0", val)
    e.set_reg("at", addr)
    a = e.word_at(word)
    e.set_reg("pc", a)
    return e.send("step", 0.35)

KILLS = [
    # tag,      off,   word,  len, dir,     expected device text
    ("w1800b",  0x800, W_SB,  1, "write", "unimplemented write to address 0x1800"),
    ("w1800w",  0x800, W_SW,  4, "write", "unimplemented write to address 0x1800"),
    ("w1800d",  0x800, W_SD,  8, "write", "unimplemented write to address 0x1800"),
    ("r1800w",  0x800, W_LW,  4, "read",  "unimplemented read from address 0x1800"),
    ("r1800d",  0x800, W_LD,  8, "read",  "unimplemented read from address 0x1800"),
    ("w16e0d",  0x6e0, W_SD,  8, "write", "unimplemented write to address 0x16e0"),
    ("w16f8d",  0x6f8, W_SD,  8, "write", "unimplemented write to address 0x16f8"),
    ("r16fcw",  0x6fc, W_LW,  4, "read",  "unimplemented read from address 0x16fc"),
    ("w1ff8d",  0xff8, W_SD,  8, "write", "unimplemented write to address 0x1ff8"),
    ("w1fffb",  0xfff, W_SB,  1, "write", "unimplemented write to address 0x1fff"),
]

for tag, off, word, ln, direction, want_text in KILLS:
    e = new_emu(tag)
    addr = kseg1(RE_BASE + off)
    try:
        do_access(e, word, addr)
    except EmuDied:
        pass
    time.sleep(0.25)
    e.drain(0.35)
    st = status_of(e)
    txt = e.raw_text
    row("%s exit" % tag, "%s,%s" % st, "exit,1",
        "guest %s len=%d @0x%x" % (direction, ln, RE_BASE + off))
    row("%s text" % tag, want_text in txt, True, want_text)
    e.close()

# ---------------------------------------------------------------- section 3
print()
print("[3] NEGATIVE CONTROL -- the same guest instruction one byte lower,")
print("    inside a MAPPED window, must NOT kill")
e = new_emu("neg")
try:
    e.guest_store32(kseg1(RE_BASE + 0x6dc), 0x5a5a5a5a)   # relative 0x16dc = TEX
    st = status_of(e)
    row("tex survives", st[0], "running", "sw to MAPPED 0x16dc (TEX) -- alive")
    row("tex text", "unimplemented write to address" in e.raw_text, False,
        "must NOT report the catch-all")
finally:
    e.close()

print()
npass = sum(1 for r in rows if r[3])
print("RESULT %d/%d rows ok" % (npass, len(rows)))
for name, got, want, ok, note in rows:
    if not ok:
        print("  FAILING: %s got=%s want=%s (%s)" % (name, got, want, note))
print("SGIRE_WITNESS_DONE")
