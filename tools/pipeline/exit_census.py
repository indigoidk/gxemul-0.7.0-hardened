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
#  ------------------------------------------------------------------------------
#  CLASSIFY BY ENCLOSING CONSTRUCT.  174 SITES IS NOT 174 DEFECTS -- that is this
#  row's second half, and no census can answer it.  But part of the split IS
#  mechanical: a call inside DEVICE_ACCESS is on a guest access path BY
#  CONSTRUCTION, while one inside DEVINIT runs at machine construction where no
#  guest can reach it.
#
#  *** THIS IS A NARROWING, NOT A VERDICT, and the tool proves that on itself:
#  the first DEVICE_ACCESS site it reports for dev_dreamcast_gdrom.c is :1055,
#  which is UNREACHABLE -- cmd_count steps by 2 and the ==12 equality clears the
#  busy bit at the boundary.  Establishing that took a hand-derived warrant.
#  DEVICE_ACCESS means WHERE TO LOOK; reachability stays a per-site question. ***
MARK = re.compile(r"^(DEVICE_ACCESS|DEVINIT|DEVICE_TICK|static\s)", re.M)
#  *** AND A PLAIN, NON-STATIC FUNCTION DEFINITION IS ALSO A BOUNDARY.  Without this the
#  split was wrong in the ONE direction that matters: every call inside a plain function was
#  attributed to the preceding DEVICE_ACCESS, inflating the bucket this tool uses to say "on
#  a guest access path BY CONSTRUCTION". ***
#
#  MEASURED on src/devices/dev_sgi_re.c, whose true split was hand-derived and then
#  independently reproduced by two seats:
#      DEVICE_ACCESS(sgi_re) 13 + (sgi_de) 1 + (sgi_mte) 1  = 15
#      draw_primitive 1 + do_mte_transfer 5                 =  6   <-- NEITHER is static
#  Before this line the tool reported all 21 as DEVICE_ACCESS.  The FILE total was right the
#  whole time; only the reachability split was wrong, which is why nobody noticed -- the
#  number people quote is the per-file one.
#
#  The pattern requires a return type, an identifier, an open paren, and NO semicolon on the
#  line -- so it takes definitions and rejects declarations and prototypes.  It is not
#  general C parsing and does not pretend to be: a K&R definition or a return type on its own
#  line would be missed, and both would fail SAFE, back to the old behaviour.
#  The negative lookahead excludes the four kinds MARK already names.  Without it a
#  `DEVICE_ACCESS(foo)` line matches BOTH patterns and yields two marks at ONE offset --
#  measured as 4 duplicate offsets in dev_sgi_re.c alone.  Harmless today, because at an
#  equal offset the DEVICE_ACCESS label sorts last and therefore wins the attribution.
#  But that is a SILENT DEPENDENCE ON SORT ORDER inside a tool whose output ranks
#  defects, and it would flip if the label text ever changed.
PLAIN = re.compile(
    r"^(?!static\b|DEVICE_ACCESS\b|DEVINIT\b|DEVICE_TICK\b)"
    r"[A-Za-z_][A-Za-z0-9_]*(?:\s+[A-Za-z_][A-Za-z0-9_]*)*\s*\*?\s*"
    r"[A-Za-z_][A-Za-z0-9_]*\s*\([^;]*$", re.M)
kinds, da_files = {}, {}
for f in files:
    s2 = strip_comments(io.open(_os.path.join(D, f), encoding="utf-8",
                                errors="replace").read())
    marks = [(m.start(), m.group(1).strip()) for m in MARK.finditer(s2)]
    marks += [(m.start(), "(plain function)") for m in PLAIN.finditer(s2)]
    marks.sort()
    for m in PAT.finditer(s2):
        prev = [k for pos, k in marks if pos < m.start()]
        k = prev[-1] if prev else "(file scope)"
        kinds[k] = kinds.get(k, 0) + 1
        if k == "DEVICE_ACCESS":
            da_files.setdefault(f, s2[:m.start()].count(NL) + 1)
tot = sum(kinds.values())
print()
print("BY ENCLOSING CONSTRUCT (same %d calls):" % tot)
TAG = {"DEVICE_ACCESS": "  <-- on a guest access path BY CONSTRUCTION",
       "DEVINIT": "  <-- construction-time; no guest reaches it",
       "DEVICE_TICK": "  <-- timer/tick path"}
for k, n in sorted(kinds.items(), key=lambda kv: -kv[1]):
    print("  %-14s %4d  %5.1f%%%s" % (k, n, 100.0 * n / tot, TAG.get(k, "")))
print()
print("DEVICE_ACCESS sites appear in %d of %d files." % (len(da_files), len(files)))
print("*** WHERE TO LOOK, NOT WHAT IS BROKEN. ***")
print()
print("EXITCENSUS_DONE")
