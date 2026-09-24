#!/usr/bin/env python3
# Q1(c): enumerate the timer fold against the five declined offsets, rather than reasoning about it.
T1L, T4C = 0x300, 0x36c
FIVE = {0x180: "IRQ_STATUS", 0x184: "IRQ_RAW_STATUS", 0x18c: "IRQ_ENABLE_CLEAR", 0x280: "FIQ_STATUS", 0x284: "FIQ_RAW_STATUS"}
print("offset  in [0x300,0x36c]?  offset & ~0x060  (offset>>5)&3  bits 5-6")
for a in sorted(FIVE):
    print("0x%03x   %-18s 0x%03x            %d              %s   %s" % (
        a, T1L <= a <= T4C, a & ~0x060, (a >> 5) & 3, "clear" if not (a & 0x60) else "SET", FIVE[a]))
# every address the SHIPPED fold rewrites, and whether any lands on the five
hits = [a for a in range(T1L, T4C + 1) if (a & ~0x060) in FIVE]
print("addresses in the shipped fold range that the fold maps ONTO one of the five:", [hex(a) for a in hits])
print("bit 7 set anywhere in [0x300,0x36c]?", any(a & 0x80 for a in range(T1L, T4C + 1)),
      "-- every one of the five has bit 7 set:", all(a & 0x80 for a in FIVE))
# every address in the 0x400 window that a WIDENED fold (lower bound removed) would alias onto the five
for lo in (0x000, 0x100, 0x180):
    al = {}
    for a in range(lo, T4C + 1):
        t = a & ~0x060
        if t in FIVE and a != t:
            al.setdefault(t, []).append(a)
    print("fold widened to [0x%03x,0x36c]: aliases onto the five (the five themselves unchanged):" % lo,
          ", ".join("%s<-{%s}" % (FIVE[t], ",".join(hex(x) for x in al[t])) for t in sorted(al)))
print("FOLD_ENUM_DONE")
