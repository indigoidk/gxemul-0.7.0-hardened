"""wdcaltoffset -- build the FIX LEG and FOUR MUTANTS of it, by exact-text replacement.

    python3 mkmutants.py <leg-name> <path-to-dev_wdc.c>

WHY EXACT TEXT AND NOT A DIFF: a context diff applied to a shifted file can still
"succeed"; a string that must occur EXACTLY ONCE either fires or says so.  Every
replacement asserts count == 1 before it is made and re-reads the file afterwards, so
a mutant that did not apply is a hard failure and is never silently measured as its
own baseline.

*** THE @N@ PLACEHOLDER IS NOT DECORATION.  The first version of this file was written
through a Bash heredoc and ONE BACKSLASH LEVEL WAS CONSUMED on the way in: the two
characters backslash-n inside the C debug() string arrived as a REAL NEWLINE, the
anchor matched 0 times, and the build died at the first leg.  The carrier documents
exactly this ("use chr(92) for any backslash that must survive into the file").  @N@
carries no backslash at all, so nothing can eat it, and the substitution below is the
single place where the level is chosen. ***

THE LEGS
  base  no edit -- the committed source.
  fix   the witness fix leg, character-for-character what witness_20260829 measured.
  m1    OVER-REACHING FIX.  `!= 0` -> `!= 2`.  The region is TWO bytes, so the offset
        is always 0 or 1 and `!= 2` is ALWAYS TRUE: BOTH offsets are declined,
        including the legitimate Device Control write.  This is the de-escalation
        clause's accept side under test -- the fix's own cost.
  m2    NULLED DECODE (vacuity floor clause (d)).  `!= 0` -> `> 1`.  ALWAYS FALSE on a
        two-byte region: the guard is kept and its repair removed, so the handler is
        behaviourally identical to the committed build.
  m3    NARROWED GUARD.  Leaves the arm alone and guards only the destructive call,
        so `d->cur_command = COMMAND_RESET` stays reachable from offset 1.  A
        plausible "smaller fix"; built to be SCORED, not proposed.
  m4    WIDTH-1 REGISTRATION.  Handler untouched; the region is registered ONE byte
        wide so offset 1 is unmapped.  The alternative fix, built to measure what an
        unmapped access actually does on this machine.
"""
import io
import sys

BS = chr(92)
LEG = sys.argv[1]
P = sys.argv[2]


def C(s):
    """Turn @N@ into the two C-source characters backslash-n."""
    return s.replace("@N@", BS + "n")


def sub(src, anchor, repl, why):
    n = src.count(anchor)
    assert n == 1, "%s: anchor occurs %d times (want 1) -- %s" % (LEG, n, why)
    return src.replace(anchor, repl, 1)


FIX_ANCHOR = C(
    '\telse {\n'
    '\t\tdebug("[ wdc: write to ALT. CTRL: 0x%02x ]@N@",\n'
    '\t\t    (int)idata);\n'
)
FIX_HEAD = '\telse if (relative_addr != 0) {\n'
FIX_BODY = C(
    '\t\t/*  WITNESS FIX LEG ONLY -- NOT a proposed shipped fix.\n'
    '\n'
    '\t\t    dev_wdc_init registers this region TWO BYTES wide, so offset 1\n'
    '\t\t    is 0x3f7 -- the Drive Address Register, READ-ONLY on real ATA\n'
    '\t\t    hardware.  The committed handler reads relative_addr zero times,\n'
    '\t\t    so a guest store there is executed as a store to Device Control\n'
    '\t\t    and (since #481) performs a full soft reset.\n'
    '\n'
    '\t\t    Decline the write.  The READ path above is untouched, so the only\n'
    '\t\t    difference between the two legs of the witness is the aliased\n'
    '\t\t    STORE.  */\n'
    '\t\tdebug("[ wdc: write to DRIVE ADDRESS (read-only): 0x%02x,"\n'
    '\t\t    " ignored ]@N@", (int)idata);\n'
    '\t} else {\n'
    '\t\tdebug("[ wdc: write to ALT. CTRL: 0x%02x ]@N@",\n'
    '\t\t    (int)idata);\n'
)

M3_ANCHOR = (
    '\t\tif (idata & WDCTL_RST) {\n'
    '\t\t\td->cur_command = COMMAND_RESET;\n'
    '\t\t\twdc_new_command_reset(d);\n'
    '\t\t}\n'
)
M3_REPL = (
    '\t\tif (idata & WDCTL_RST) {\n'
    '\t\t\td->cur_command = COMMAND_RESET;\n'
    '\t\t\t/*  MUTANT m3 -- guard only the destructive call.  */\n'
    '\t\t\tif (relative_addr == 0)\n'
    '\t\t\t\twdc_new_command_reset(d);\n'
    '\t\t}\n'
)

M4_ANCHOR = (
    '\tmemory_device_register(devinit->machine->memory, "wdc_altstatus",\n'
    '\t    alt_status_addr, 2, dev_wdc_altstatus_access, d, DM_DEFAULT, NULL);\n'
)
M4_REPL = (
    '\t/*  MUTANT m4 -- register the region ONE byte wide.  */\n'
    '\tmemory_device_register(devinit->machine->memory, "wdc_altstatus",\n'
    '\t    alt_status_addr, 1, dev_wdc_altstatus_access, d, DM_DEFAULT, NULL);\n'
)

s = io.open(P, encoding="utf-8", newline="").read()
assert "WITNESS FIX LEG ONLY" not in s, "already edited: %s" % P
assert "MUTANT m" not in s, "already mutated: %s" % P

if LEG == "base":
    print("  base: no edit applied (this is the committed source)")
    sys.exit(0)
elif LEG == "fix":
    s = sub(s, FIX_ANCHOR, FIX_HEAD + FIX_BODY, "fix leg")
    MARK = "else if (relative_addr != 0) {"
elif LEG == "m1":
    s = sub(s, FIX_ANCHOR, FIX_HEAD + FIX_BODY, "fix leg (m1 base)")
    s = sub(s, FIX_HEAD, '\telse if (relative_addr != 2) {\n', "m1 over-reach")
    MARK = "else if (relative_addr != 2) {"
elif LEG == "m2":
    s = sub(s, FIX_ANCHOR, FIX_HEAD + FIX_BODY, "fix leg (m2 base)")
    s = sub(s, FIX_HEAD, '\telse if (relative_addr > 1) {\n', "m2 nulled decode")
    MARK = "else if (relative_addr > 1) {"
elif LEG == "m3":
    s = sub(s, M3_ANCHOR, M3_REPL, "m3 narrowed guard")
    MARK = "MUTANT m3"
elif LEG == "m4":
    s = sub(s, M4_ANCHOR, M4_REPL, "m4 width-1 registration")
    MARK = "MUTANT m4"
else:
    raise SystemExit("unknown leg %r" % LEG)

io.open(P, "w", encoding="utf-8", newline="").write(s)

#  READ IT BACK OFF DISK.  A write that did not land, or landed elsewhere, must not be
#  reported as an applied mutant -- the whole table would then measure the baseline.
back = io.open(P, encoding="utf-8", newline="").read()
assert back.count(MARK) == 1, "%s: marker %r occurs %d times AFTER writing" % (
    LEG, MARK, back.count(MARK))
print("  %s: applied and verified on disk (marker %r x1)" % (LEG, MARK))
