#!/usr/bin/env python3
"""
sgidewidth rung-3 witness + premise audit, OPUS 5 seat, 2026-08-31.

Machine: UNMODIFIED in-tree `-E sgi -e ip32` (SGI O2 / IP32, R10000).
Device : sgi_de, registered at PHYSICAL 0x15002000 (0x15000000 + 0x2000),
         DEV_SGI_DE_LENGTH = 0x1000.  Reached through KSEG1 0xffffffffb5002000.
No machine description, no device_add, no source edit: the machine is the
committed one and every access is a REAL GUEST INSTRUCTION single-stepped
through real address decode and real memory_rw().

Every row is its own emulator session, because most of them kill the host.
"""
import sys, os, re, time
sys.path.insert(0, "/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad")
from gxprobe import Emu

BIN     = sys.argv[1] if len(sys.argv) > 1 else "/tmp/gxopusdew/gxemul"
TAG     = sys.argv[2] if len(sys.argv) > 2 else "base"
NOPS    = "/tmp/gxdew_nops.bin"
SCRATCH = 0xffffffff80010000
ARGS    = ["-V", "-E", "sgi", "-e", "ip32", "0x%x:%s" % (SCRATCH, NOPS)]

DE      = 0xffffffffb5002000          # KSEG1 | physical 0x15002000
W_FG    = DE + 0x0d0                  # CRIME_DE_FG   (0x20d0) - plain r/w reg
W_SCIS  = DE + 0x048                  # CRIME_DE_SCISSOR (0x2048) - fatal()s our value
W_START = DE + 0x800                  # CRIME_DE_START bit set  (startFlag)
W_END8  = DE + 0xff8                  # last 8-aligned slot in the window
W_ENDM3 = DE + 0xffd                  # 3 bytes before the end - the brief's "ld"

SENTINEL = 0xa5a5a5a5                 # never returned by this device

#  Encodings.  EVERY one is re-checked against the debugger's own
#  `unassemble` at run time (verify()), because a wrong register field
#  yields 0 and every zero-accepting row would pass by accident.
W = {
  "sb":  0xa0220000, "sh":  0xa4220000, "sw":  0xac220000, "sd":  0xfc220000,
  "lbu": 0x90220000, "lhu": 0x94220000, "lw":  0x8c220000, "ld":  0xdc220000,
  "ldl": 0x68220000, "ldr": 0x6c220000,
}

rows = []
def check(name, got, want, note=""):
    ok = (got == want)
    rows.append((name, got, want, ok, note))
    print("%-9s %-4s got=%-46r want=%-46r %s" %
          (name, "ok" if ok else "FAIL", got, want, note), flush=True)

def newemu():
    return Emu(BIN, ARGS, preset={"scratch": SCRATCH}, boot_wait=3.0,
               default_wait=0.30)

def step_one(e, word, addr, v0=None, wait=0.6):
    """Set at=addr (and optionally v0), then single-step ONE guest `word`."""
    if v0 is not None:
        e.set_reg("v0", v0)
    e.set_reg("at", addr)
    a = e.word_at(word)
    e.set_reg("pc", a)
    return e.send("step", wait)

def alive(e):
    return e.wait_exit(timeout=1.2)[0] == "running"

# ---------------------------------------------------------------- encodings
e = newemu()
bad = []
for n, w in W.items():
    a = e.word_at(w)
    _, txt = e.disasm_word(a)
    mn = txt.split()[0] if txt else "?"
    if mn != n:
        bad.append((n, txt))
check("encodings", bad, [], "unassemble agrees with every hand-built word")
e.close()

# ---------------------------------------------------------------- LIVENESS
#  A known value written by a real guest `sw` returns through the same decode.
e = newemu()
step_one(e, W["sw"], W_FG, v0=0xdeadbeef)
e.set_reg("v0", SENTINEL)
step_one(e, W["lw"], W_FG)
e._reg_cache.pop("v0", None)
v = e.read_reg("v0")
check("live", None if v is None else (v & 0xffffffff), 0xdeadbeef,
      "LIVENESS: len=4 write+read round-trips through sgi_de")
check("live_up", alive(e), True, "host alive after an accepted access")
e.close()

# ------------------------------------------------------- DEVICE SIGNATURE
#  RAM cannot print this.  The value in the message is the one we stored,
#  so the answer could only have come from THIS device's handler.
e = newemu()
step_one(e, W["sw"], W_SCIS, v0=0x12345678)
sig = "sgi_de: TODO: non-zero CRIME_DE_SCISSOR: 0x0000000012345678"
check("devsig", e.count(sig), 1, "DEVICE-SIGNATURE: only sgi_de emits this")
e.close()

# ------------------------------------------------- THE DEFECT: width 1 and 2
for nm, insn, want_len in (("w1_sb", "sb", 1), ("w2_sh", "sh", 2),
                           ("w1_lbu", "lbu", 1), ("w2_lhu", "lhu", 2)):
    e = newemu()
    step_one(e, W[insn], DE, v0=SENTINEL, wait=1.0)
    msg = "sgi_de: len = %d not implemented" % want_len
    check(nm + "_msg", e.count(msg), 1, "%s at +0x000 -> width kill" % insn)
    check(nm + "_die", e.wait_exit(timeout=2.0), ("exit", 1), "host process ENDS")
    e.close()

# --------------------------------- THE BRIEF'S CLAIM: ld at +0xffd -> len 3 ?
e = newemu()
out = step_one(e, W["ld"], W_ENDM3, v0=SENTINEL, wait=1.0)
check("ld_ffd_len3", e.count("sgi_de: len = 3 not implemented"), 0,
      "REFUTES BRIEF: an ordinary `ld` at +0xffd never reaches the device")
st = e.wait_exit(timeout=1.5)
check("ld_ffd_alive", st, ("running", None), "host SURVIVES the unaligned ld")
cause = e.read_reg("cause")
exccode = None if cause is None else ((cause >> 2) & 0x1f)
check("ld_ffd_adel", exccode, 4, "COP0 Cause.ExcCode == 4 (AdEL): alignment "
      "exception raised BEFORE memory_rw")
e.close()

# ------------------- and the unaligned-access instruction family is no door
for nm, insn in (("ldl_ffd", "ldl"), ("ldr_ffd", "ldr")):
    e = newemu()
    step_one(e, W[insn], W_ENDM3, v0=SENTINEL, wait=1.0)
    hits = sum(e.count("sgi_de: len = %d not implemented" % n) for n in (1,2,3,5,6,7))
    check(nm + "_nokill", hits, 0,
          "%s aligns DOWN (addr & ~7) and issues len=8: no odd width" % insn)
    check(nm + "_alive", e.wait_exit(timeout=1.5), ("running", None), "host survives")
    e.close()

# --------------------------------------------- accepted widths at the far end
e = newemu()
step_one(e, W["sd"], W_END8, v0=0x1122334455667788, wait=0.8)
check("w8_end_ok", e.wait_exit(timeout=1.2), ("running", None),
      "aligned `sd` at +0xff8 is len=8, ACCEPTED, no truncation")
e.close()

# ================================================================= THE TAIL
#  A *legal* 4-byte store with CRIME_DE_START set reaches the tail and calls
#  draw_primitive() with a cold register file (op==0).
e = newemu()
step_one(e, W["sw"], W_START, v0=0x11223344, wait=1.2)
check("draw_op0_msg", e.count("sgi_de: UNIMPLEMENTED drawing op = 0x00000000"), 1,
      "SECOND HOST KILL, inside draw_primitive(), on an ACCEPTED width")
check("draw_op0_die", e.wait_exit(timeout=2.0), ("exit", 1),
      "the tail kills the host today, with no width defect involved")
e.close()

print("\nSUMMARY %s: %d/%d rows ok" % (TAG, sum(1 for r in rows if r[3]), len(rows)))
for n,g,w,ok,note in rows:
    if not ok:
        print("  FAILED: %s got=%r want=%r  (%s)" % (n,g,w,note))
print("DEWPROBE_DONE")
