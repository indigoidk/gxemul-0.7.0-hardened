#!/usr/bin/env python3
"""Report each panel seat's VERDICT line, and whether the seat actually ANSWERED.

*** THIS EXISTS BECAUSE THE OBVIOUS GREP IS WRONG, AND IT WAS WRONG FOUR TIMES IN ONE
DAY. ***  Briefs instruct seats with a line like

    `VERDICT: SHIP` / `VERDICT: SHIP-WITH-CHANGES` / `VERDICT: DO-NOT-SHIP` -- one line

and every seat ECHOES the brief before answering (codex always does).  So
`grep -o 'VERDICT: [A-Z-]*' | tail -1` reads the brief's own menu and reports the LAST
option on it as the seat's verdict.  On 2026-08-22 that scored a seat DO-NOT-SHIP when it
had not answered at all, and the round nearly re-planned around it.

The discriminator is mechanical and cheap: an INSTRUCTION line lists several tokens, an
ANSWER line carries exactly one.  Anchoring to start-of-line is NOT enough on its own --
the instruction line often starts with a backtick and the token.

Second failure this guards: judging a seat by FILE SIZE.  A walled codex returns the
echoed brief plus its quota notice and can be the LARGEST file in the panel; the packet-fed
Ollama seats do not echo at all, so comparing their size to the brief marks them absent.
Novel-line ratio against the brief separates the two without reference to length.

usage:  seat_verdicts.py <panel_dir>
"""
import io
import os
import re
import sys

VERDICT_RE = re.compile(r"VERDICT\s*:\s*([A-Za-z][A-Za-z-]*)")
WALL_RE = re.compile(
    r"usage limit|rate.?limit|\b429\b|quota|too many requests|"
    r"unknown effort level|unknown model|not authenticated|invalid api key",
    re.I)

SEATS = ("codex", "agy", "grok", "kimi",
         "ollama_glm", "ollama_deepseek", "ollama_minimax")


def brief_lines(d):
    for name in ("brief_sent.md", "brief_sent.packet.md"):
        p = os.path.join(d, name)
        if os.path.exists(p):
            txt = io.open(p, encoding="utf-8", errors="replace").read()
            return set(l.strip() for l in txt.splitlines() if len(l.strip()) > 20)
    return set()


def verdict_of(text, brief_lines=()):
    """The seat's own verdict: a line carrying EXACTLY ONE verdict token.

    *** ONE TOKEN PER LINE IS NOT ENOUGH, MEASURED 2026-08-22. ***  A brief that
    lists its three options WRAPS, and the continuation line then carries a
    single token -- so this returned the brief's own menu as a seat's answer,
    which is the exact failure this whole file exists to stop.  Two further
    guards: skip any line that also appears in the brief, and skip any line that
    still reads as instruction rather than answer.
    """
    INSTRUCTIONAL = ("open with", "on line one", "then reasoning", "one line, then",
                     "` or `", "or `verdict")
    for line in text.splitlines():
        if len(VERDICT_RE.findall(line)) != 1:
            continue
        st = line.strip()
        if st in brief_lines:
            continue
        low = st.lower()
        if any(k in low for k in INSTRUCTIONAL):
            continue
        return VERDICT_RE.search(line).group(1).upper()
    return None


def main():
    if len(sys.argv) != 2:
        print(__doc__.strip().splitlines()[-1])
        return 2
    d = sys.argv[1]
    bl = brief_lines(d)
    answered = walled = absent = 0
    print("%-17s %8s %6s  %-22s %s" % ("seat", "bytes", "novel", "verdict", "state"))
    for s in SEATS:
        p = os.path.join(d, s + ".txt")
        if not os.path.exists(p):
            print("%-17s %8s %6s  %-22s %s" % (s, "-", "-", "-", "NOT CREATED"))
            absent += 1
            continue
        t = io.open(p, encoding="utf-8", errors="replace").read()
        long_lines = [l.strip() for l in t.splitlines() if len(l.strip()) > 20]
        novel = [l for l in long_lines if l not in bl]
        ratio = (len(novel) / len(long_lines)) if long_lines else 0.0
        v = verdict_of(t, bl)
        #  *** A WALL IS A FILE THAT *ENDS* WITH THE NOTICE.  Both the naive rule
        #  and my first correction of it were measured WRONG on 2026-08-22. ***
        #
        #  Keyword-anywhere reported a LIVE seat as walled, because its
        #  chain-of-thought mentioned a quota word while it was still writing.
        #  Replacing that with "a wall is a SHORT file" was worse: the carrier
        #  already records that codex's wall produces the LARGEST file in the
        #  panel -- the echoed brief plus the notice -- and a positive control
        #  against two known-walled panels showed the size rule missing both.
        #
        #  What actually separates them is POSITION.  A walled run ends with
        #  "ERROR: You've hit your usage limit ... try again at <date>" and
        #  nothing after it; a working seat that merely mentions a limit has it
        #  mid-reasoning and ends with substance.  Checked against both known
        #  walls and against a live seat that mentions limits.
        is_walled = bool(WALL_RE.search(t[-600:])) and not v
        if is_walled:
            state, walled = "*** WALLED ***", walled + 1
        elif not novel:
            state, absent = "ECHO ONLY -- no answer", absent + 1
        elif v:
            state, answered = "answered", answered + 1
        else:
            state, answered = "answered, NO VERDICT LINE (format miss)", answered + 1
        print("%-17s %8d %5.0f%%  %-22s %s"
              % (s, len(t), ratio * 100, v or "-", state))
    print("\n%d answered, %d walled, %d absent/echo-only" % (answered, walled, absent))
    return 0


if __name__ == "__main__":
    sys.exit(main())
