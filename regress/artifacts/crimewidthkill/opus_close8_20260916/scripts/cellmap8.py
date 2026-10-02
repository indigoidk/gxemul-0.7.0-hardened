#!/usr/bin/env python3
"""cellmap8.py -- #529 CLOSING PASS 8 (Opus measuring seat).  THE DENOMINATOR.

Derives, from the SHIPPED probe source (never from a description of it), every ACCEPTED CRIME access that runs
with `d->warned & CRIME_W_LEN' SET, and classifies it on a FINER product than the contract's:

    {len 4, 8} x {R, W} x {7 switch labels} x {lane = relative_addr & 4} x {pc in the REV window}

A K-form mutant (`&& !(<cell> && (d->warned & CRIME_W_LEN))' on a width guard) can ONLY change behaviour through a
post-latch accepted access at its own cell -- pre-latch its conjunct is false and the guard is unchanged.  So a cell
with ZERO post-latch accesses is a GUARANTEED CLEAN SWEEP, and that is a mechanical escape test, not a judgement.

TWO CORRECTIONS to session_map2.py's method, both checked here rather than assumed:
  (a) the FIRST REFUSAL must be a 1/2-byte access TO CRIME.  A narrow access to RAM or to another device does not
      set this latch.  session_map2.py keys on `ln in (1,2)' with no address test.
  (b) an access is only a CRIME access if its base is in [CRIME, CRIME+0x280).  The device is 0x280 bytes; the
      probe's `(base & ~0xfff) == CRIME' also admits 0xb4000280..0xb4000fff, which is NOT this device.
Sentinel: CELLMAP8_DONE."""
import io, re, sys, contextlib

SRC = sys.argv[1] if len(sys.argv) > 1 else "/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/crime_width_probe.py"
src = open(SRC).read()
src = src.replace("t, clean = session(", "t, clean = _rec(")
assert "t, clean = session(" not in src
src = re.sub(r"(?m)^(\s*)row\(", lambda m: m.group(1) + "_row(", src)
assert re.search(r"(?m)^\s*row\(", src) is None

OPC = {0x20: ("lb", 1, "R"), 0x21: ("lh", 2, "R"), 0x23: ("lw", 4, "R"), 0x24: ("lbu", 1, "R"),
       0x25: ("lhu", 2, "R"), 0x37: ("ld", 8, "R"), 0x28: ("sb", 1, "W"), 0x29: ("sh", 2, "W"),
       0x2b: ("sw", 4, "W"), 0x3f: ("sd", 8, "W")}
CRIME = 0xb4000000
DEVLEN = 0x280
LABELS = {0x00: "REV", 0x08: "CTL", 0x10: "IST", 0x18: "IMK", 0x30: "DOG", 0x38: "TIM"}
SESSIONS, PEND = [], []


def _row(name, got, want, note=""):
    PEND.append(name)


def _rec(cmds, settle=1.5, spin=1.2):
    regs, acc, = {}, []
    for c in cmds:
        m = re.match(r"^([a-z0-9]+)=0x([0-9a-f]+)$", c)
        if m:
            regs[m.group(1)] = int(m.group(2), 16)
            continue
        m = re.match(r"^put w 0x([0-9a-f]+), 0x([0-9a-f]{8})$", c)
        if m:
            w = int(m.group(2), 16)
            op, rs = w >> 26, (w >> 21) & 0x1f
            if op in OPC and rs in (1, 7):
                base = regs.get("at" if rs == 1 else "a3")
                if base is not None:
                    acc.append((OPC[op], base, int(m.group(1), 16)))
    SESSIONS.append([acc, list(PEND)])
    del PEND[:]
    return "", True


sys.argv = ["crime_width_probe.py", "/nonexistent-binary", "map"]
buf = io.StringIO()
try:
    with contextlib.redirect_stdout(buf):
        exec(compile(src, SRC, "exec"), {"__name__": "__main__", "_rec": _rec, "_row": _row})
except SystemExit:
    pass
SESSIONS.append([[], list(PEND)])

nsess = len(SESSIONS) - 1
print("SESSIONS=%d   probe=%s" % (nsess, SRC))

cells = {}          # (ln, dir, label, lane, win) -> [ (sess, op, off, rows) ]
tot = 0
narrow_nonCRIME = []
for i in range(nsess):
    acc = SESSIONS[i][0]
    myrows = SESSIONS[i + 1][1]
    ref = None
    for j, ((op, ln, d), base, where) in enumerate(acc):
        incrime = CRIME <= base < CRIME + DEVLEN
        if ln in (1, 2) and not incrime:
            narrow_nonCRIME.append((i, op, hex(base)))
        if ln in (1, 2) and incrime:
            ref = j
            break
    if ref is None:
        continue
    for (op, ln, d), base, where in acc[ref + 1:]:
        if ln not in (4, 8) or not (CRIME <= base < CRIME + DEVLEN):
            continue
        off = base - CRIME
        lab = LABELS.get(off, "DFL")
        lane = (off & 4) >> 2 if ln == 4 else "-"
        win = 1 if (where & 0xffffff00) == 0xbfc05100 else 0
        key = (ln, d, lab, lane, win if lab == "REV" else "-")
        cells.setdefault(key, []).append((i, op, off, myrows))
        tot += 1

print("TOTAL post-latch accepted CRIME accesses: %d" % tot)
print("narrow non-CRIME accesses seen before a session's first CRIME refusal: %d %s"
      % (len(narrow_nonCRIME), narrow_nonCRIME[:8]))
print("")
print("=== THE CONTRACT'S 28-CELL PRODUCT {len}x{dir}x{label}, post-latch occupancy ===")
coarse = {}
for (ln, d, lab, lane, win), v in cells.items():
    coarse.setdefault((ln, d, lab), []).extend(v)
empty28 = []
for lab in ("REV", "CTL", "IST", "IMK", "DOG", "TIM", "DFL"):
    for ln in (8, 4):
        for d in ("W", "R"):
            v = coarse.get((ln, d, lab), [])
            tag = "C_%s%d%s" % ({"REV": "rev", "CTL": "ctl", "IST": "ist", "IMK": "imk",
                                 "DOG": "dog", "TIM": "tim", "DFL": "dfl"}[lab], ln, d.lower())
            offs = sorted(set("+0x%x" % o for _, _, o, _ in v))
            print("%-9s n=%-3d %s" % (tag, len(v), " ".join(offs)))
            if not v:
                empty28.append(tag)
print("EMPTY coarse cells (guaranteed clean sweep): %s" % (empty28 or "NONE"))
print("")
print("=== THE FINER PRODUCT: + lane (relative_addr & 4, a BODY-TESTED partition of the len==4 arm) ===")
print("    + the REV PROM-probe window (cpu->pc, a BODY-TESTED partition of the REV arm)")
fine_empty = []
for lab in ("REV", "CTL", "IST", "IMK", "DOG", "TIM", "DFL"):
    wins = (0, 1) if lab == "REV" else ("-",)
    for ln in (8, 4):
        lanes = (0, 1) if ln == 4 else ("-",)
        for d in ("W", "R"):
            for lane in lanes:
                for win in wins:
                    key = (ln, d, lab, lane, win)
                    v = cells.get(key, [])
                    nm = "%s %d%s lane=%s win=%s" % (lab, ln, d, lane, win)
                    offs = sorted(set("+0x%x" % o for _, _, o, _ in v))
                    sess = sorted(set(s for s, _, _, _ in v))
                    print("%-30s n=%-3d sess=%-16s %s" % (nm, len(v), str(sess)[:16], " ".join(offs)))
                    if not v:
                        fine_empty.append(nm)
print("")
print("FINE CELLS WITH ZERO POST-LATCH ACCESS (a K-form mutant there is a GUARANTEED CLEAN SWEEP):")
for nm in fine_empty:
    print("   %s" % nm)
print("N_FINE_EMPTY=%d" % len(fine_empty))
print("CELLMAP8_DONE")
