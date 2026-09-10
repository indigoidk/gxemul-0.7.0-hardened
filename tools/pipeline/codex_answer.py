#!/usr/bin/env python3
"""codex_answer.py -- pull codex's PROSE out of a streamed .err file.

*** WHY THIS EXISTS.  Measured 2026-09-08, four times in one session. ***

`codex exec` streams its reasoning, its shell calls and its file reads to STDERR and writes the
final answer to STDOUT.  Two things then go wrong, and they look identical from outside:

  *  a CONTENT-FILTER REFUSAL writes ZERO bytes to stdout and puts the refusal on stderr, so from
     the .txt alone it is indistinguishable from a seat that was never invoked;
  *  a run that is CUT SHORT -- budget, transport, or an unanswerable question -- also leaves an
     empty .txt, while its stderr holds real, substantive findings.

Both were live in one session.  One cut-short run's stderr carried the observation that settled a
design question two panels had left open (`only writes to that field'), and it would have been an
UNREAD REVIEW if nobody had opened the .err.

  > **THE RULE THIS ENFORCES: score a codex job from its .err, never from the size of its .txt.**

It deliberately does NOT try to be clever about what counts as an answer.  It reports what it finds
and lets a human read it, because the one thing worse than an unread review is a summariser that
drops the sentence nobody expected to matter.

Usage:  codex_answer.py <file.err> [--full]
"""
import io
import re
import sys

#  *** STDOUT MUST BE FORCED TO UTF-8 ON THIS MACHINE, AND THIS TOOL CRASHED WITHOUT IT ON ITS
#  VERY FIRST REAL USE.  Measured 2026-09-08. ***
#
#  git-bash python defaults to cp1252 here, and a seat answer routinely contains an en-dash or a
#  Unicode minus sign.  Without this, `print()` raises UnicodeEncodeError PARTWAY THROUGH, after
#  some output has already been emitted -- which is worse than failing cleanly, because the reader
#  sees a partial answer followed by a traceback and may take the partial answer as the whole one.
#  That is this project's unread-review class arriving by a new route: the answer is on disk, the
#  tool that exists to surface it stops halfway, and nothing says which half is missing.
#
#  The carrier already records this exact hazard for the panel helper -- write responses to utf-8
#  files, never through a bare print -- and the rule applies to any tool that echoes seat text.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REFUSAL = "flagged for possible cybersecurity risk"


def blocks(text):
    """codex prose arrives after a bare `codex' line and ends at the next `exec' line."""
    out = []
    for chunk in re.split(r"(?m)^codex[ \t]*$", text)[1:]:
        prose = re.split(r"(?m)^exec[ \t]*$", chunk)[0].strip()
        if prose:
            out.append(prose)
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    full = "--full" in sys.argv
    if not args:
        print(__doc__)
        return 2
    path = args[0]
    text = io.open(path, encoding="utf-8", errors="replace").read()

    #  *** COUNTING THE REFUSAL STRING IS UNSOUND, AND IT MISFIRED ON ITS SECOND DAY. ***
    #
    #  A codex run greps the repository, and this project's own ledger contains a row
    #  (`codexcyberflag') that QUOTES the refusal message verbatim.  So a healthy answer whose trace
    #  happens to include that grep output scores as REFUSED -- which is exactly what happened on
    #  the `#516' pass-2 panel: two "hits", both inside grep output, with three verdict markers and
    #  a substantive conclusion in the same file.
    #
    #  **A count cannot tell an ASSERTION from a QUOTATION OF ONE**, and this project has recorded
    #  that class twice already -- once for a stale-claim grep that flagged an honest correction,
    #  and once when a precommit check fired on codex quoting a committed file.  It gets STEADILY
    #  WORSE as the records improve, because every honest write-up quotes what it describes.
    #
    #  THE DISCRIMINATOR IS POSITION, which is what this project already uses for seat truncation:
    #  a REAL refusal terminates the stream, so it appears in the TAIL with no verdict after it.
    TAIL = text[-4000:]
    n_refusals = TAIL.count(REFUSAL)
    quoted_only = text.count(REFUSAL) - n_refusals
    found = blocks(text)

    print("codex_answer: %s" % path)
    print("  stream bytes   %d" % len(text))
    print("  prose blocks   %d" % len(found))
    print("  refusal marker %d in the TAIL%s" % (n_refusals,
          "   *** CONTENT-FILTER REFUSAL ***" if n_refusals else ""))
    if quoted_only:
        print("  (%d further occurrence(s) EARLIER in the stream -- almost certainly QUOTED, e.g. "
              "grep output over this project's own records.  Not counted as a refusal.)"
              % quoted_only)

    #  A verdict line is this project's convention, so say plainly whether one is present.
    verdicts = [b for b in found if re.search(r"(?im)^\W*\**VERDICT", b)]
    print("  verdict blocks %d%s" % (len(verdicts),
          "" if verdicts else "   -- NO VERDICT LINE: treat as CUT SHORT, not as agreement"))

    if not found:
        print("")
        print("  no prose blocks at all.  Last 400 bytes of the stream, verbatim:")
        print("  " + text[-400:].replace("\n", "\n  "))
        return 0

    show = found if full else found[-4:]
    for b in show:
        print("")
        print("  " + "-" * 68)
        body = b if full else b[:2500]
        print("  " + body.replace("\n", "\n  "))
    if not full and len(found) > len(show):
        print("")
        print("  (%d earlier block(s) not shown; pass --full)" % (len(found) - len(show)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
