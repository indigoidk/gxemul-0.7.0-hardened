"""A COMMENT-AWARE census of live process-terminating calls in src/devices/.

*** WHY NOT A GREP.  `exitdenom` records this census as three-generations unstable, and
my own grep of ONE file today produced a false positive: `break;  /* OB-20: was exit(1) */`
counted as a live exit.  A naive grep gets steadily MORE wrong as this fork gets more
honest, because every de-fatalisation leaves a comment QUOTING the exit(1) it removed. ***

So this strips C comments with a state machine before counting, and reports the
denominator alongside the numerator so a pattern that selects nothing is visible.
"""
import io
import os
import re
import sys

NL = chr(10)
#  *** SCOPE AND METHOD ARE THE POINT OF THIS FILE.  `exitdenom` records that this
#  census has had THREE GENERATIONS -- 114 -> 170 -> 360 -- each written down as if
#  authoritative, and the numbers cannot be compared because none of them said what
#  it counted.  A fourth number would not fix that.  A DERIVER does. ***
#
#      SCOPE    src/devices/*.c only  (override with $GXEXITDIR)
#      PATTERN  exit( | abort( | _exit(   -- process termination, any spelling
#      COMMENTS STRIPPED FIRST, with a state machine that respects string literals
#      UNIT     SITES, not defects.  A site may be unreachable, construction-time,
#               or already triaged; this counts CALLS, and says so.
#
#  Run it; do not quote a remembered figure.  It prints the raw count beside the
#  live one precisely so the two can never be confused again.
import os as _os
D = _os.environ.get("GXEXITDIR") or _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), _os.pardir, _os.pardir,
    "src", "devices")


def strip_comments(s):
    """Remove /* */ and // comments, preserving line structure and string literals."""
    out = []
    i, n = 0, len(s)
    while i < n:
        c = s[i]
        if c == '"' or c == chr(39):
            q = c
            out.append(c)
            i += 1
            while i < n:
                if s[i] == chr(92):
                    out.append("  ")
                    i += 2
                    continue
                out.append(s[i])
                if s[i] == q:
                    i += 1
                    break
                i += 1
            continue
        if s.startswith("/*", i):
            j = s.find("*/", i + 2)
            j = n if j < 0 else j + 2
            out.append("".join(ch if ch == NL else " " for ch in s[i:j]))
            i = j
            continue
        if s.startswith("//", i):
            j = s.find(NL, i)
            j = n if j < 0 else j
            out.append(" " * (j - i))
            i = j
            continue
        out.append(c)
        i += 1
    return "".join(out)


PAT = re.compile(r"\b(exit|abort|_exit)\s*\(")
files = sorted(f for f in os.listdir(D) if f.endswith(".c"))
raw_hits = live_hits = 0
per = {}
for f in files:
    s = io.open(os.path.join(D, f), encoding="utf-8", errors="replace").read()
    raw_hits += len(PAT.findall(s))
    stripped = strip_comments(s)
    lines = [(i + 1, l) for i, l in enumerate(stripped.split(NL)) if PAT.search(l)]
    live_hits += len(lines)
    if lines:
        per[f] = lines

print("files scanned                : %d" % len(files))
print("raw grep hits (WITH comments): %d" % raw_hits)
print("LIVE calls (comments stripped): %d" % live_hits)
print("  -> %d of %d raw hits are inside comments (%.0f%%)"
      % (raw_hits - live_hits, raw_hits, 100.0 * (raw_hits - live_hits) / max(raw_hits, 1)))
print()
if not per:
    sys.exit("*** ZERO live calls found across %d files -- that is a contradiction, not a "
             "result.  Refusing to report it." % len(files))
print("PER FILE (live only):")
for f in sorted(per, key=lambda k: -len(per[k])):
    print("  %-34s %2d" % (f, len(per[f])))
    for ln, txt in per[f][:4]:
        print("        %5d  %s" % (ln, txt.strip()[:64]))
print()
print("EXITCENSUS_DONE")
