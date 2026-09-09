"""Measure the pass-4 step-binding repair against the two ORDER variants a seat reported.

Anchoring fixed the SHAPE of a response and could not fix its ORDER.  A pass-4 seat reported two
variants that still swept: a second read moved BEFORE the second step, and the first response
REPLAYED as the second.  Both are well-formed responses in the wrong place.

This exercises the SHIPPED `response_after' -- extracted from the probe file, not retyped -- so the
repair is measured rather than asserted.
"""
import io, re

P = 'C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/alpha_swpctx_v0_probe.py'
src = io.open(P, encoding='utf-8', newline='').read()

m = re.search(r'^RESP = r"(.*)"$', src, re.M)
assert m, 'RESP not extractable -- test aborted rather than guessed'
RESP = m.group(1).encode().decode('unicode_escape')

def responses_at(t, reg):
    return [(mm.group(1), mm.start()) for mm in re.finditer(RESP % reg, t, re.M)]

def response_after(t, reg, marker):
    k = t.find(marker)
    if k < 0:
        return None
    for val, pos in responses_at(t, reg):
        if pos > k:
            return val
    return None

C, N = "0x1000000", "0x1010000"
STEP2 = "GXemul> step 4"

GENUINE = ("GXemul> step 2\n"
           "GXemul> print v0\n" + C + "\n"
           + STEP2 + "\n"
           "GXemul> print v0\n" + N + "\n"
           "GXemul> print a0\n" + N + "\n")

#  A: the second read MOVED BEFORE the second step -- both responses precede STEP2
MOVED = ("GXemul> step 2\n"
         "GXemul> print v0\n" + C + "\n"
         "GXemul> print v0\n" + C + "\n"
         + STEP2 + "\n"
         "GXemul> print a0\n" + N + "\n")

#  B: the FIRST response REPLAYED as the second -- two identical values, both before STEP2
REPLAY = ("GXemul> step 2\n"
          "GXemul> print v0\n" + C + "\n"
          "GXemul> print v0\n" + C + "\n"
          + STEP2 + "\n")

print("  RESP extracted from the shipped probe: %r\n" % RESP)
print("  %-58s %-14s %s" % ("case", "bound v0", "verdict"))
fails = 0

v = response_after(GENUINE, "v0", STEP2)
ok = (v == N)
fails += not ok
print("  %-58s %-14s %s" % ("GENUINE: the response AFTER step 2 is call 2's", v,
                            "ok" if ok else "*** FAIL ***"))

for label, txt in (("seat A: second read moved BEFORE the second step", MOVED),
                   ("seat B: first response REPLAYED as the second", REPLAY)):
    v = response_after(txt, "v0", STEP2)
    ok = (v is None)
    fails += not ok
    print("  %-58s %-14s %s" % (label, str(v),
                                "ok -- rejected" if ok else "*** STILL ACCEPTED ***"))

#  and the old count-based rule would have PASSED both, which is the point
for label, txt in (("(old count rule on A)", MOVED), ("(old count rule on B)", REPLAY)):
    n = len(responses_at(txt, "v0"))
    print("  %-58s %-14s %s" % (label, "%d of 2" % n,
                                "would have passed" if n == 2 else ""))

print("\n  ORDER_ATTACK_RESULT=%d/3" % (3 - fails))
print("  ORDER_ATTACK_DONE")
