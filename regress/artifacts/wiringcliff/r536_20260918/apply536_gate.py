"""#536: insert the mk48 + hpcmips sections (gate536_sections.sh) into regress/gate_arm.sh,
between the pcc2 c040 section and the PIT section.  Applied identically to the HEAD-based staged
blob and to the working tree (which also carries #529's uncommitted crime_width hunk at the END of
the file, not ours to ship).  Refuses unless the anchor occurs exactly once."""
import io, os, sys
p = sys.argv[1]
here = os.path.dirname(os.path.abspath(__file__))
sec = io.open(os.path.join(here, "gate536_sections.sh"), encoding="utf-8", newline="").read()
s = io.open(p, encoding="utf-8", newline="").read()
ANCHOR = ('    check "pcc2 c040 rows red"     "$(count "$C040LOG" " FAIL$")" "0"\n'
          'fi\n\n\n'
          'PITLOG=$LOGDIR/pit8253_latch.log\n')
n = s.count(ANCHOR)
assert n == 1, "anchor found %d times (want 1)" % n
assert "MK48LOG" not in s and "HPCLOG" not in s, "already applied"
head, tail = ANCHOR.split("PITLOG=", 1)
s = s.replace(ANCHOR, head + sec.rstrip("\n") + "\n\n\nPITLOG=" + tail)
io.open(p, "w", encoding="utf-8", newline="").write(s)
print("inserted %d lines" % sec.rstrip("\n").count("\n"))
