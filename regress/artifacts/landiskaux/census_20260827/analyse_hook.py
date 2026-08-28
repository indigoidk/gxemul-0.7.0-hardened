#!/usr/bin/env python3
"""analyse_hook.py <build-B log> -- the 0x14000000..0x14000040 window census.

Register numbering: landisk registers the wdc with addr_mult=2, so device
register N sits at paddr 0x14000000 + 2N (machine_landisk.c; DEVICE_ACCESS(wdc)
does relative_addr /= d->addr_mult).
"""
import re, sys, collections

REG = {0x00: "0 data", 0x02: "1 error/features", 0x04: "2 seccnt",
       0x06: "3 sector", 0x08: "4 cyl_lo", 0x0a: "5 cyl_hi",
       0x0c: "6 sdh", 0x0e: "7 status/command"}
CTL = {0x08: "WDCTL_4BIT", 0x04: "WDCTL_RST", 0x02: "WDCTL_IDS"}

pat = re.compile(r"GXCENSUS ([RW]) paddr=0x([0-9a-f]+) len=(\d+) nx=(\d+) "
                 r"val=0x([0-9a-f]+) pc=0x([0-9a-f]+)")
log = open(sys.argv[1], "rb").read().decode("latin-1")
hits = pat.findall(log)
print("DENOMINATORS: log bytes=%d, 'GXCENSUS' occurrences=%d, regex hits=%d"
      % (len(log), log.count("GXCENSUS"), len(hits)))
print()

tally = collections.Counter()
nx = collections.Counter()
for d, pa, ln, n, val, pc in hits:
    tally[(int(pa, 16), d, int(ln))] += 1
    nx[int(n)] += 1

print("--- WINDOW CENSUS 0x14000000..0x1400003f ---")
print("%-12s %-20s %-3s %-4s %s" % ("paddr", "wdc register", "dir", "len", "count"))
for (pa, d, ln) in sorted(tally):
    off = pa - 0x14000000
    name = REG.get(off, "*** NOT MAPPED ***")
    print("0x%08x  %-20s %-3s %-4d %d" % (pa, name, d, ln, tally[(pa, d, ln)]))
print()
print("no_exceptions flag on those accesses: %s  (0 = real guest access)" % dict(nx))
print()

#  ---- the +0x2c writes, in order, with their bit decomposition ----
tc = [h for h in hits if int(h[1], 16) == 0x1400002c]
print("--- EVERY ACCESS AT 0x1400002c, IN ORDER ---")
vals = collections.Counter()
for i, (d, pa, ln, n, val, pc) in enumerate(tc, 1):
    v = int(val, 16)
    bits = " | ".join(CTL[b] for b in (0x08, 0x04, 0x02) if v & b) or "(no bits set)"
    print("%-3d %s len=%s val=0x%02x  = %-32s pc=0x%s" % (i, d, ln, v, bits, pc))
    vals[v] += 1
print()
print("VALUE HISTOGRAM at 0x1400002c (%d accesses):" % len(tc))
for v in sorted(vals):
    bits = " | ".join(CTL[b] for b in (0x08, 0x04, 0x02) if v & b) or "(none)"
    print("   0x%02x  x%-3d  %s" % (v, vals[v], bits))
print()
print("WRITES=%d  READS=%d  carrying WDCTL_RST(0x04)=%d"
      % (sum(1 for h in tc if h[0] == "W"), sum(1 for h in tc if h[0] == "R"),
         sum(1 for h in tc if int(h[4], 16) & 0x04)))

#  ---- where in the probe does the RST write land? ----
print()
print("--- CONTEXT: the 12 window accesses immediately before/after each 0x1400002c write ---")
idx = [i for i, h in enumerate(hits) if int(h[1], 16) == 0x1400002c]
for k, i in enumerate(idx[:2] + idx[-1:], 0):
    lo, hi = max(0, i - 4), min(len(hits), i + 5)
    print("  ... around hit index %d (val 0x%s):" % (i, hits[i][4]))
    for j in range(lo, hi):
        d, pa, ln, n, val, pc = hits[j]
        off = int(pa, 16) - 0x14000000
        mark = "  <<<" if j == i else ""
        print("      %-6s %-20s val=0x%-4s%s"
              % (d, REG.get(off, "UNMAPPED +0x%02x" % off), val, mark))
