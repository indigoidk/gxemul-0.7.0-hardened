"""The FULL escape corpus for `alpha_swpctx_v0_probe.py', run against the SHIPPED helpers.

Four escapes were reported across two passes, and the first repair for each pair let the OTHER
pair through:

    pass 4, seat A   second read moved BEFORE the second step   -- positional rejects, binding-only
                                                                   would too
    pass 4, seat B   first response REPLAYED as the second      -- positional PASSED it
    pass 5, codex 1  an EARLIER `step 4' echo rebinds to call 1 -- binding PASSED it 6/6, where the
                                                                   positional rule had 4/5
    pass 5, codex 2  unique marker, response 1 sits after it    -- binding PASSED it 6/6

So neither rule alone is sufficient and each covers the other's hole.  This exercises the composed
`bound_second' -- source EXTRACTED from the probe file, never retyped -- against all four plus the
genuine shape.
"""
import io, re, types

P = 'C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/alpha_swpctx_v0_probe.py'
src = io.open(P, encoding='utf-8', newline='').read()

#  Lift RESP + the three helpers out of the shipped file, so this tests what ships.
m = re.search(r'^RESP = r"(.*)"$', src, re.M)
assert m, 'RESP not extractable'
ns = {'re': re}
exec('RESP = r"%s"' % m.group(1), ns)
for fn in ('responses_at', 'step_marker', 'bound_second'):
    i = src.find('def %s(' % fn)
    assert i > 0, 'helper %s not found' % fn
    j = src.find('\ndef ', i + 1)
    k = src.find('\n\n\n', i + 1)
    end = min(x for x in (j, k, len(src)) if x > 0)
    exec(src[i:end], ns)
bound_second = ns['bound_second']

C, N = "0x1000000", "0x1010000"
S1, S2 = "GXemul> step 3", "GXemul> step 4"
A0 = "GXemul> print a0\n" + N + "\n"
def v0(x): return "GXemul> print v0\n" + x + "\n"

CASES = [
 ("GENUINE: response 1 before step 2, response 2 after",
  S1 + "\n" + v0(C) + S2 + "\n" + v0(N) + A0, N),
 ("pass 4 seat A: second read MOVED BEFORE the second step",
  S1 + "\n" + v0(C) + v0(C) + S2 + "\n" + A0, None),
 ("pass 4 seat B: first response REPLAYED as the second",
  S1 + "\n" + v0(C) + v0(C) + S2 + "\n", None),
 ("pass 5 codex 1: an EARLIER `step 4' echo rebinds to call 1",
  S2 + "\n" + S1 + "\n" + v0(C) + S2 + "\n" + v0(N) + A0, None),
 ("pass 5 codex 2: unique marker, response 1 sits AFTER it",
  S1 + "\n" + S2 + "\n" + v0(C) + v0(N) + A0, N),
]

print("  %-56s %-12s %s" % ("case", "bound v0", "verdict"))
fails = 0
for label, txt, want in CASES:
    val, why = bound_second(txt, "v0", 4)
    ok = (val == want)
    fails += not ok
    shown = val if val else ("rejected: " + why)
    print("  %-56s %-12s %s" % (label, str(val), ("ok" if ok else "*** FAIL ***")))
    if not val:
        print("  %-56s %s" % ("", "   -> " + why))

print("\n  FULL_CORPUS_RESULT=%d/%d" % (len(CASES) - fails, len(CASES)))
print("  FULL_CORPUS_DONE")
