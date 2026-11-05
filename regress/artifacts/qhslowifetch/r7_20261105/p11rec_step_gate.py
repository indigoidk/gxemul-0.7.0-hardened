import io
import sys

# Pass-11 R1 repeated in gate_ppc.sh's qhslowifetch block comment: add the ruler's scope qualifier.  Only these lines change.
p = sys.argv[1]
s = io.open(p, encoding="utf-8", newline="").read()
assert "\r" not in s
old = ("# each pair presents the failure block with the same pc, addr, MSR, running and slot and differs only in translation_readahead, so a\n"
       "# toggle that cancels over the two-entry session's two visits shows once on its partner -- and six -T continues\n")
new = ("# each pair presents the failure block with the same pc, addr, MSR, running and slot and differs only in translation_readahead, so a\n"
       "# toggle that cancels over the two-entry session's two visits, under a condition on state the block reads that the toggle itself\n"
       "# leaves unchanged, shows once on its partner (scope: the probe's docstring; codex pass 11, R1) -- and six -T continues\n")
assert s.count(old) == 1, s.count(old)
qs = s.index("# ---- qhslowifetch (#NNN)")
qe = s.index("# ---- ppccrandcorc (#575)")
assert qs < s.index(old) < qe, "edit outside the qhs block"
assert max(len(x) for x in new.split("\n")) <= 133
s = s.replace(old, new)
io.open(p, "w", encoding="utf-8", newline="").write(s)
print("GATE-P11 APPLIED")
