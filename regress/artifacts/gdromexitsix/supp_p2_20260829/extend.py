#  Build a 22-row instrument from the pinned 20-row one by adding exactly two
#  candidate rows.  ANCHORED and unique-asserted: a miss is a hard failure, never
#  a silent no-op.
import io, sys
src, dst = sys.argv[1], sys.argv[2]
L = io.open(src, encoding="utf-8").read().split(chr(10))

def uniq(pred, what):
    h = [i for i, s in enumerate(L) if pred(s)]
    assert len(h) == 1, "want ONE %s, got %d" % (what, len(h))
    return h[0]

#  1. the TOC-decline regex, beside the two existing decline regexes
i = uniq(lambda s: s.startswith("CMD_DECL = re.compile("), "CMD_DECL")
L[i+1:i+1] = [
 "#  #490 SUPP: the #489 TOC-length decline, anchored the same way.  The candidate",
 "#  `latch keep` row reads it to test that a Site-A decline PRESERVES other latches.",
 'TOC_DECL = re.compile(r"Read TOC with cnt=-?[0-9]+, not 408 -- declined")',
]

#  2. the two candidate rows, immediately before the scoring tail
i = uniq(lambda s: s.startswith("n = sum(1 for _, ok in rows if ok)"), "score tail")
L[i:i] = [
 "# ------------------------------------------------ #490 SUPP: two CANDIDATE rows",
 "#  Neither exists in the shipped 20.  Each is aimed at one of the two ask-again",
 "#  escapes that the compile-time assert cannot reach, because both are",
 "#  STATEMENT-level defects and no constant-expression can see a statement.",
 "#",
 "#  kills: E2_assignA  (`d->warned |= GDROM_W_FMT` -> `d->warned = GDROM_W_FMT`)",
 "#  via:   the #489 TOC diagnostic COUNT.  A Site-A decline that ASSIGNS clears",
 "#         GDROM_W_TOCLEN, so the second identical short TOC re-announces.  The",
 "#         channel is a latch OTHER THAN the one Site A owns -- which is why every",
 "#         existing row is blind to it: they all read the two NEW sites.",
 "A = Addr(CODE)",
 "t, alive, how = session(packet(TOC_SHORT, A) + packet(BAD_FMT, A)",
 "                        + packet(TOC_SHORT, A))",
 'row("latch keep", "%d" % len(TOC_DECL.findall(t)), "1",',
 '    "a Site-A decline must PRESERVE the other eight latch bits")',
 "",
 "#  kills: E3_widenA  (Site A guard widened to `& (GDROM_W_FMT | GDROM_W_CMD)`)",
 "#  via:   the FMT decline count under the REVERSED site order.  `both sites` and",
 "#         `crossbit` both fix FMT-then-CMD, and at that order warned is 0 when",
 "#         Site A is reached, so a widened guard is indistinguishable.  CMD-then-FMT",
 "#         is the order a probing guest walks naturally.",
 "A = Addr(CODE)",
 "t, alive, how = session(packet(BAD_CMD, A) + packet(BAD_FMT, A))",
 'row("both sites rev", "%d,%d" % (len(FMT_DECL.findall(t)), len(CMD_DECL.findall(t))),',
 '    "1,1", "reversed order -- each site still speaks for itself")',
 "",
]
io.open(dst, "w", encoding="utf-8", newline=chr(10)).write(chr(10).join(L))
print("extended ok")
