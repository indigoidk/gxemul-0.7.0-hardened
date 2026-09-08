"""Measure the pass-3 repair against the seat's own synthetic attacks.

codex found three parser escapes by exercising the scorer over 31 synthetic transcripts.  This
runs the SHIPPED regex -- extracted from the probe file itself, not retyped -- against those
attacks plus the genuine shapes, so the repair is MEASURED rather than asserted.
"""
import io, re

P = 'C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/alpha_swpctx_v0_probe.py'
src = io.open(P, encoding='utf-8', newline='').read()

m = re.search(r'^RESP = r"(.*)"$', src, re.M)
assert m, 'could not extract RESP from the probe -- test aborted rather than guessed'
RESP = m.group(1).encode().decode('unicode_escape')
print('  RESP extracted from the shipped probe: %r\n' % RESP)

def responses(t, reg):
    return re.findall(RESP % reg, t, re.M)

GENUINE = ("GXemul> print v0\n"
           "0x1000000\n"
           "GXemul> print v0\n"
           "0x1010000\n"
           "GXemul> print a0\n"
           "0x1010000\n")

ATTACKS = [
 ("codex A: a TRACE LINE substitutes for a missing second response",
  "GXemul> print v0\n0x1000000\nGXemul> step 4\ntrace: print v0\n0x1000000\n"
  "GXemul> print v0\nGXemul> print a0\n0x1010000\n", 1),
 ("codex B: `sprint v0' matched because nothing anchored the word",
  "GXemul> print v0\n0x1000000\nsprint v0\n0x1010000\n", 1),
 ("codex C: a value with trailing text",
  "GXemul> print v0\n0x1000000: diagnostic\nGXemul> print v0\n0x1010000\n", 1),
]

print("  %-62s %-8s %s" % ("case", "v0 resp", "verdict"))
fails = 0
n = len(responses(GENUINE, "v0"))
ok = (n == 2)
fails += not ok
print("  %-62s %-8s %s" % ("GENUINE: two real responses must both parse", n,
                           "ok" if ok else "*** FAIL ***"))
n = len(responses(GENUINE, "a0"))
ok = (n == 1)
fails += not ok
print("  %-62s %-8s %s" % ("GENUINE: the a0 response must parse", n,
                           "ok" if ok else "*** FAIL ***"))

for label, txt, want in ATTACKS:
    n = len(responses(txt, "v0"))
    ok = (n == want)
    fails += not ok
    print("  %-62s %-8s %s" % (label, "%d (want %d)" % (n, want),
                               "ok -- rejected" if ok else "*** STILL ACCEPTED ***"))

print("\n  ATTACK_RESULT=%d/%d" % (5 - fails, 5))
print("  ATTACK_DONE")
