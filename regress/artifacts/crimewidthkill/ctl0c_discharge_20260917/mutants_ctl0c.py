#!/usr/bin/env python3
"""The ctl0c DISCHARGE leg -- Fable's L1 obligation on #529, before it may commit.

*** WHAT IS BEING TESTED, AND IT IS NOT THE CODE. ***  `acc ctl0c' and `p acc ctl0c' are ACCEPT
rows with ZERO measured kills across the fifteen legs of table 12.  Accept-row failability says a
row is NOT DISCHARGED BY EXISTING -- it is discharged by a MEASURED KILL.  So either a mutant reds
them, or they come out of the probe.

*** WHY THE OBVIOUS MUTANT CANNOT WORK, and this is the whole design point. ***  `acc ctl0c' reads
`lw +0x0c' and wants 0x100.  That value is produced by the WIDTH ARM (`} else if (len == 4) {' ...
`odata = d->reg[relative_addr / 8]', then `if (relative_addr & 4) odata = (int32_t)odata'), which
runs BEFORE the register switch.  +0x0c has no case label, so it lands in `default:' -- a debug
print only.  **A mutant that declines at `default:' therefore cannot move this row**, and
`G_clr_ctl4r''s `relative_addr == CRIME_CONTROL' (0x08) never touches 0x0c either.  That is exactly
why fifteen legs left it green.

So the discharging mutant must decline BEFORE the width arm:

    if (relative_addr == 0x0c) goto crime_declined;

which is a plausible future edit -- someone deciding this device should REFUSE unimplemented
offsets rather than answer them out of the width arm -- and is the clause-(d) shape: keep the
guard, reroute its effect.

PREDICTION, written before the run so its own mtime proves the order:
  * `acc ctl0c' and `p acc ctl0c' RED (they want 0x100; a declined read answers 0).
  * `acc ctl4r' / `p acc ctl4r' UNMOVED -- they read +0x08, which this mutant does not touch.
  * everything else unmoved.  EXPECTED SCORE 202/204.
If ctl0c does NOT red, the rows are VACUOUS BY CONSTRUCTION and must be REMOVED, not kept.
"""
import io, sys
ANCHOR = "\tif (len == 8) {"
MUTANTS = {
 "M_ctl0c_decline": (ANCHOR, "\tif (relative_addr == 0x0c) goto crime_declined;\n" + ANCHOR),
}
if len(sys.argv) > 1 and sys.argv[1] == "list":
    print(" ".join(sorted(MUTANTS))); raise SystemExit(0)
name, src, dst = sys.argv[1], sys.argv[2], sys.argv[3]
find, repl = MUTANTS[name]
t = io.open(src, encoding="utf-8", newline="").read()
n = t.count(find)
if n != 1:
    print("MUTANT TEXT NOT FOUND (or not unique): %d occurrences -- FAIL" % n); raise SystemExit(9)
io.open(dst, "w", encoding="utf-8", newline="").write(t.replace(find, repl, 1))
print("APPLIED %s (1 edit)" % name)
