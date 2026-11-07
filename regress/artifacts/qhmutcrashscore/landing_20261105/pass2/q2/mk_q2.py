#!/usr/bin/env python3
"""mk_q2.py -- the pass-2 Q2 measurement's inputs: the STAGED gate 3 and two mutants of it, each an exact replacement
of the fix's one guard line asserted to occur once.

  STAGED  regress/selftest_mutation.sh as the unit stages it (the committed form, #NNN tag filled)
  M_q2a   Gemini 4 Argon's pass-2 Q2 edit, literally: `|| { echo "NOLOG rc=$rc"; return; }` -> `|| echo 0`
          (no `return`, so the count line below it still runs)
  M_q2b   the clause-(d) null repair the round block PREDICTED: the guard kept, its effect nulled --
          `|| { echo "NOLOG rc=$rc"; return; }` -> `|| { echo 0; return; }`

Writes q2/gates/{STAGED,M_q2a,M_q2b}.sh and q2/gates/MD5.txt.  Reads the kit's unit/files/ only."""
import hashlib
import os

Q = os.path.dirname(os.path.abspath(__file__))
L = os.path.dirname(Q)
staged = open(os.path.join(L, "unit", "files", "regress", "selftest_mutation.sh"), "rb").read()
GUARD = b"""|| { echo "NOLOG rc=$rc"; return; }"""
assert staged.count(GUARD) == 1, "the staged gate's guard was not found exactly once"
out = {"STAGED": staged,
       "M_q2a": staged.replace(GUARD, b"|| echo 0", 1),
       "M_q2b": staged.replace(GUARD, b"|| { echo 0; return; }", 1)}
d = os.path.join(Q, "gates")
os.makedirs(d, exist_ok=True)
lines = []
for k, b in out.items():
    open(os.path.join(d, k + ".sh"), "wb").write(b)
    lines.append("%s  %s.sh" % (hashlib.md5(b).hexdigest(), k))
    if k != "STAGED":
        assert b.count(b"\n") == staged.count(b"\n") and b != staged
open(os.path.join(d, "MD5.txt"), "w", newline="\n").write("\n".join(lines) + "\n")
print("\n".join(lines))
print("MK_Q2_DONE")
