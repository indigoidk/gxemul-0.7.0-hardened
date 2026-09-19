"""#536: classify the round's four preserved editors (regress/artifacts/wiringcliff/r536_20260918/*.py) in the
MANIFEST -- every tracked .py under regress/ must be classified or the checker reds UNCLASSIFIED.  Applied identically
to the staged blob and the working copy; refuses unless its anchor occurs exactly once and the entries are absent."""
import io, sys
p = sys.argv[1]
s = io.open(p, encoding="utf-8", newline="").read()
A = ('    "artifacts/lcalenzerodrop/opus_p2_20260918/scripts/summarize.py":\n'
     '        (CLASS_TOOL, "#530 pass 2: tabulates score and getenv value per (cell, binary); refuses a leg with no sentinel"),\n')
assert s.count(A) == 1, "anchor x%d" % s.count(A)
assert "artifacts/wiringcliff/r536_20260918/" not in s, "already applied"
N = ('    #  #536 wiringcliff: the four editors that produced this round\'s staged blobs, preserved as run.\n'
     '    "artifacts/wiringcliff/r536_20260918/apply536_gate.py":\n'
     '        (CLASS_TOOL, "#536: inserts the mk48 + hpcmips sections into gate_arm.sh at a unique anchor; refuses otherwise"),\n'
     '    "artifacts/wiringcliff/r536_20260918/apply536_exempt.py":\n'
     '        (CLASS_TOOL, "#536: drops the two wired exemptions, re-dates eleven to 2026-09-27, derives the selftest\'s M5 days"),\n'
     '    "artifacts/wiringcliff/r536_20260918/apply536_manifest.py":\n'
     '        (CLASS_TOOL, "#536: adds these MANIFEST lines -- the round\'s own tools, classified by the round"),\n'
     '    "artifacts/wiringcliff/r536_20260918/apply536_precommit.py":\n'
     '        (CLASS_TOOL, "#536: corrects precommit_check.sh section R\'s comment, which named the old 2026-09-20 date"),\n')
s = s.replace(A, A + N)
io.open(p, "w", encoding="utf-8", newline="").write(s)
print("classified 4 artifact tools")
