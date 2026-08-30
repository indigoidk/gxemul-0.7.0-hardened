"""#494 Q2 -- WHAT DOES `return 0` FROM THIS HANDLER ACTUALLY DO?

The shipped comment says a 0 "would route it to unassigned-address handling, which
warns per access with no bound and halts every CPU under -T".  Reading memory_rw.c
says otherwise: a REGISTERED device that returns 0 never reaches that path.  It sets
res = -1, takes the `res <= 0 && !no_exceptions` arm, emits a debug() naming the
DEVICE, raises EXCEPTION_DBE on MIPS and returns MEMORY_ACCESS_FAILED.

This settles it by RUNNING both legs with -v, which is the verbosity at which that
debug() prints while free-running (it subtracts 1 from verbose, so v == 0, not < 0).

    n6  = the fix with `return 0;` added to the decline arm
    fix = the shipped fix           <- negative control: must NOT print the line

Usage: q2_mechanism.py <probedir> <n6-binary> <fix-binary> <disk>
"""
import os
import re
import sys
import time

D = sys.argv[1]
N6 = sys.argv[2]
FIX = sys.argv[3]
DISK = sys.argv[4]

sys.path.insert(0, D)
saved = sys.argv
sys.argv = [sys.argv[0]]
import wdc_altoffset_probe as W            # noqa: E402
sys.argv = saved

RAW = os.path.join(D, "wdcaltoff_4bit.bin")   # its P5 pokes 0x0e at offset 1
BASE = W.BASE


def run(binary, tag, verbose):
    argv = [binary]
    if verbose:
        argv.append("-v")
    argv += ["-V", "-E", "evbmips", "-e", "malta",
             "-d", "iR:" + DISK, "0x%x:%s" % (BASE, RAW)]
    print("-" * 92)
    print("LEG %-14s %s" % (tag, " ".join(argv)))
    print("-" * 92)
    emu = W.Emu(argv)
    emu.send("continue", wait=1.0)
    emu.drain(6.0)
    #  Interrupt back to the prompt so pc is readable even though the guest
    #  never parks (there is no breakpoint here on purpose -- we want to see
    #  where it ENDED UP, not to stop it at a place we chose).
    whole = bytes(emu.buf).decode("latin1", "replace")

    fails = re.findall(r"device '([^']+)' addr ([0-9a-f]+) failed", whole)
    nonex = whole.count("non-existant")
    print("  \"device '<name>' addr ... failed\" lines : %d  %s"
          % (len(fails), fails[:4]))
    print("  \"non-existant\" (unassigned-address path) : %d" % nonex)
    for pat in ("write to DRIVE ADDRESS", "write to ALT. CTRL"):
        print("  %-38s : %d" % ('"%s"' % pat, whole.count(pat)))
    emu.close(os.path.join(D, "q2_%s.log" % tag))
    return len(fails), nonex


print("=" * 92)
print("Q2 MECHANISM -- what a REGISTERED device returning 0 does, MEASURED")
print("=" * 92)
print("date %s" % time.strftime("%Y-%m-%d %H:%M:%S"))
print("probe program %s" % RAW)
print()
print("PREDICTION, written from memory_rw.c BEFORE this ran:")
print("  n6  : >=1 \"device 'wdc_altstatus' addr ... failed\"  and ZERO \"non-existant\"")
print("  fix : ZERO of both  (negative control)")
print()

n6f, n6n = run(N6, "n6_ret0", True)
print()
fxf, fxn = run(FIX, "fix", True)
print()
print("=" * 92)
print("VERDICT")
print("=" * 92)
print("  n6_ret0 : device-failed lines %d   non-existant %d" % (n6f, n6n))
print("  fix     : device-failed lines %d   non-existant %d" % (fxf, fxn))
if n6f > 0 and n6n == 0 and fxf == 0:
    print("  ==> CONFIRMED.  `return 0` takes the DEVICE-ACCESS-FAILED path (EXCEPTION_DBE")
    print("      on MIPS), NOT unassigned-address handling.  The shipped comment names")
    print("      the wrong mechanism, and the real one is more severe.")
elif n6f == 0 and n6n > 0:
    print("  ==> the comment is RIGHT and my reading is wrong: it reached the")
    print("      unassigned-address path.")
else:
    print("  ==> INDETERMINATE -- neither pattern cleanly matched; read the logs.")
print("Q2MECH_DONE")
