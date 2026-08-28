#!/usr/bin/env python3
"""census.py <logfile> -- tally 'non-existant' accesses by paddr.

COUNTS OCCURRENCES, NOT LINES, deliberately.  The emulator's warning lines
interleave with the guest console stream -- a warning is emitted mid-word,
"wd0 at wdc0 chan[ memory WRITE ... ]nel 0 drive 0" -- so a line-based count is
not obviously safe here.

HONEST SCOPE: in the four runs taken for this census the two counts AGREED at
12 (no log line carried two warnings), so the occurrence form is a structural
precaution and NOT a measured correction.  tally_runs.sh prints both forms, so
any future divergence shows up instead of being assumed either way.
"""
import re, sys, collections

pat = re.compile(
    r"\[ memory (READ|WRITE): (?:from|to) non-existant "
    r"paddr=0x([0-9a-f]+) len=(\d+) pc=0x([0-9a-f]+)(?: <([^>]*)>)? \]")

log = open(sys.argv[1], "rb").read().decode("latin-1")
hits = pat.findall(log)

by_addr = collections.Counter()
detail = collections.Counter()
for d, paddr, ln, pc, sym in hits:
    by_addr[int(paddr, 16)] += 1
    detail[(int(paddr, 16), d, int(ln), pc, sym)] += 1

print("TOTAL non-existant accesses in log: %d" % len(hits))
print()
print("--- ALL paddrs ---")
for a in sorted(by_addr):
    print("  0x%08x  %d" % (a, by_addr[a]))
print()
WLO, WHI = 0x14000000, 0x14000040
print("--- WINDOW 0x%08x .. 0x%08x (unmapped only; mapped accesses print nothing) ---"
      % (WLO, WHI))
win = [a for a in sorted(by_addr) if WLO <= a <= WHI]
if not win:
    print("  (none)")
for a in win:
    print("  0x%08x  %d" % (a, by_addr[a]))
print()
print("--- window detail (paddr, dir, len, pc, symbol) x count ---")
for k in sorted(detail):
    if WLO <= k[0] <= WHI:
        print("  0x%08x %-5s len=%d pc=0x%s <%s>  x%d" %
              (k[0], k[1], k[2], k[3], k[4], detail[k]))
#  denominators, so a zero is distinguishable from a broken pattern
print()
print("DENOMINATORS: log bytes=%d, 'non-existant' substring occurrences=%d, regex hits=%d"
      % (len(log), log.count("non-existant"), len(hits)))
