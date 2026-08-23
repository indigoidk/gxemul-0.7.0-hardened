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

#  #461: TOLERATE MARKDOWN EMPHASIS AROUND THE VERDICT WORD.
#
#  MEASURED on the #460 pass-2 panel: minimax answered `VERDICT: **SHIP**` and grok
#  answered `VERDICT: SHIP WITH CHANGES**`.  The old pattern required a LETTER
#  immediately after the colon, so the `*` defeated it and BOTH correct answers
#  landed under "answered, NO VERDICT LINE (format miss)".
#
#  *** THAT IS THE MIRROR IMAGE OF THE FAILURE THIS FILE EXISTS TO PREVENT. ***  It
#  was built so a DEAD seat is never counted as agreement; here a LIVE seat with a
#  correct verdict was being downgraded to a formatting failure, which is the same
#  error pointing the other way and just as silent.
#
#  The leading class is OPTIONAL and bounded, so the findall-count discriminator
#  below still works: the brief's own menu line still yields three matches and is
#  still skipped.  Only the emphasis characters are new.
#  AND IT KEEPS THE WHOLE PHRASE, WHICH THE OLD PATTERN DID NOT.  Capturing one
#  word made `SHIP` and `SHIP WITH CHANGES` IDENTICAL in the report -- two
#  materially different answers rendered the same -- and collapsed every
#  OPTION A / OPTION B / OPTION C verdict to a bare "OPTION", so a pass-1 panel
#  that SPLIT read as unanimous.  That defect predates the emphasis one and is
#  worse: emphasis lost a seat, this lost the ANSWER while still reporting it.
#
#  Uppercase-only, up to four tokens: it takes "SHIP WITH CHANGES", "DO NOT
#  SHIP", "OPTION A" and "SOMETHING ELSE", and stops dead at lowercase prose or
#  punctuation, so "VERDICT: SHIP -- the code is fine" still yields just SHIP.
#  *** FOUR FORMS A LIVE SEAT WRITES THAT THE FIRST TWO VERSIONS MISSED, ALL
#  NAMED BY PANEL SEATS AND THEN MEASURED. ***
#
#    **VERDICT**: SHIP          emphasis on the LABEL, not the value
#    verdict: ship              lowercase
#    VERDICT — SHIP             an em dash instead of a colon
#    VERDICT: "SHIP"            a quoted value
#
#  And one that was worse than a miss: `VERDICT: Ship with changes` returned
#  the single letter "S".  Not None -- an actual token, which would have been
#  REPORTED as the seat's verdict, because [A-Z][A-Z-]* matched the S and
#  stopped dead at the lowercase.  A silent wrong answer beats a silent
#  missing answer for damage, and this file exists to prevent exactly that.
#
#  So: the label may carry emphasis, the separator may be a colon or a dash,
#  the value may be quoted, and the value is matched CASE-INSENSITIVELY and
#  upper-cased on the way out.  A one-character token is refused outright
#  (there is no real one-letter verdict, and it is the signature of a
#  truncated match).
VERDICT_RE = re.compile(
    r"VERDICT\s*[*_`]{0,3}\s*[:—–-]"
    r"\s*[*_`\x22\x27]{0,3}\s*([A-Za-z][A-Za-z-]{1,}(?:\s+[A-Za-z][A-Za-z-]*){0,3})",
    re.I)
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
        v = VERDICT_RE.search(line).group(1).upper().strip()
        #  belt and braces: a one-character token is a truncated match,
        #  never a verdict, whatever the regex happens to allow today.
        if len(v) < 2:
            continue
        return v
    return None


def main():
    if len(sys.argv) != 2:
        print(__doc__.strip().splitlines()[-1])
        return 2
    d = sys.argv[1]
    bl = brief_lines(d)
    answered = walled = absent = down = 0
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
        #  *** A TRANSPORT FAILURE IS NOT A WALL AND IS NEVER AN ANSWER. ***
        #  Added 2026-08-22 after this tool scored three DOWN seats "answered".
        #  The whole Ollama daemon was not running -- localhost:11434 refused the
        #  connection -- so panel_ollama.py wrote its 155-byte error file as the
        #  ENTIRE seat output.  Every earlier rule missed it: the file is short
        #  but so is a stall; it carries no quota keyword so the wall rule passes
        #  it; and it is 100% novel against the brief so the echo rule passes it
        #  too.  It then landed in the "answered, NO VERDICT LINE (format miss)"
        #  bucket -- a DOWN seat recorded as a live seat with bad formatting,
        #  which is exactly the "seat failure counted as agreement" this file
        #  exists to prevent.
        #
        #  Kept separate from WALLED on purpose, because the REMEDY differs and
        #  the round record should say which happened: a wall is the seat
        #  refusing and you wait it out; a refused connection is the daemon not
        #  running and one `ollama serve` fixes it, so a panel that reports it
        #  as a wall silently gives up three seats it could have had.
        #  *** A THINKING MODEL CAN SPEND ITS WHOLE BUDGET AND SAY NOTHING. ***
        #  Added 2026-08-22, the same day as the transport class below, and found the
        #  same way: by this tool mis-scoring it.  deepseek returned a 214 KB file --
        #  by far the largest in the panel -- consisting of raw JSON with
        #  `"done_reason": "length"`, `"eval_count": 65536` and **`"response": ""`**.
        #  It filled its entire context with hidden reasoning and never emitted an
        #  answer.  panel_ollama.py's `resp.get("response") or json.dumps(resp)`
        #  fallback then wrote the whole envelope to the file.
        #
        #  Every earlier rule passed it: no quota keyword, 100% novel against the
        #  brief, and enormous rather than short.  It landed in "answered, NO VERDICT
        #  LINE (format miss)" -- a seat that said NOTHING recorded as a live seat
        #  with bad formatting.  That is the third distinct way this file has scored
        #  a failure as agreement, after the big-file wall and the dead daemon.
        #
        #  The carrier already warns that these are thinking models and a num_predict
        #  cap starves the response; panel_ollama.py correctly sends none.  This is
        #  the model reaching its OWN limit, which no caller-side setting prevents.
        raw = ""
        st = t.lstrip()
        if st.startswith('{"model"') and '"response": ""' in st[:4000]:
            reason = "unknown"
            m = re.search(r'"done_reason":\s*"([a-z_]+)"', st)
            if m:
                reason = m.group(1)
            ev = re.search(r'"eval_count":\s*(\d+)', st)
            raw = "%s%s" % (reason, (", %s tokens" % ev.group(1)) if ev else "")

        err = t.lstrip()[:400] if t.lstrip().startswith("OLLAMA_SEAT_ERROR") else ""
        #  MEASURED 2026-08-23: a wall can be a MOMENT, not a state.  Kimi walled
        #  mid-answer at 23:01 with 36 KB already written, and answered a liveness
        #  test an hour later.  So a WALLED row is not a verdict on the seat -- it
        #  is a verdict on that invocation, and the seat should be RE-FIRED ONCE
        #  before the round closes rather than recorded as gone.
        is_walled = bool(WALL_RE.search(t[-600:])) and not v
        if raw:
            state = ("*** SEAT DOWN -- NO ANSWER: spent its whole budget on hidden "
                     "reasoning (%s) ***" % raw)
            down += 1
        elif err:
            state = ("*** SEAT DOWN -- daemon refused the connection; "
                     "start ollama and re-fire ***"
                     if "ConnectionRefused" in err or "refused it" in err
                     else "*** SEAT DOWN -- transport/model error ***")
            down += 1
        elif is_walled:
            state, walled = "*** WALLED ***", walled + 1
        elif not novel:
            state, absent = "ECHO ONLY -- no answer", absent + 1
        elif v:
            state, answered = "answered", answered + 1
        else:
            state, answered = "answered, NO VERDICT LINE (format miss)", answered + 1
        print("%-17s %8d %5.0f%%  %-22s %s"
              % (s, len(t), ratio * 100, v or "-", state))
    print("\n%d answered, %d walled, %d DOWN, %d absent/echo-only"
          % (answered, walled, down, absent))
    if down:
        #  Loud on purpose.  A down seat that reads as a quiet row is how a
        #  three-seat outage got recorded as a full panel.
        print("*** %d SEAT(S) DOWN -- OPERATIONAL failure, never agreement."
              "  Name them in the round record. ***" % down)
    return 0



#  ------------------------------------------------------------------ selftest
#
#  *** THE FIX THAT PROMPTED THIS FILE'S LAST TWO CORRECTIONS SHIPPED WITH NO
#  DETECTOR, WHICH IS THE ONE THING THE ETHOS FORBIDS. ***  Both defects were
#  found by a seat READING the regex, not by anything executing it -- and the
#  second (single-word capture) had been live since the file was written, so
#  every split panel this project ran was reported as unanimous.
#
#  Each row below is a MUTATION row: it names an edit a future round might
#  plausibly make and asserts the answer CHANGES.  A row green under its own
#  mutant is vacuous, and the driver proves that by applying the mutants and
#  requiring red.
#
#  Run:  python tools/pipeline/seat_verdicts.py --selftest

BQ = chr(96)    # backtick -- written as chr() so no quoting level can eat it
ST = chr(42)    # asterisk
US = chr(95)    # underscore
DQ = chr(34)    # double quote
EMDASH = chr(8212)
ENDASH = chr(8211)

CASES = [
    #  (label, text, brief_lines, expected)
    ("plain",          "VERDICT: SHIP", (), "SHIP"),

    #  *** DEFECT 1, measured on the #460 pass-2 panel. ***  minimax answered
    #  with markdown emphasis and was filed under "answered, NO VERDICT LINE
    #  (format miss)" -- a LIVE seat with a correct verdict downgraded to a
    #  formatting failure, the mirror image of what this file exists to prevent.
    ("bold",           "VERDICT: " + ST * 2 + "SHIP" + ST * 2, (), "SHIP"),
    ("underscore",     "VERDICT: " + US * 2 + "DO NOT SHIP" + US * 2, (),
                       "DO NOT SHIP"),
    ("backtick",       "VERDICT: " + BQ + "OPTION B" + BQ, (), "OPTION B"),

    #  *** DEFECT 2, and it is the worse of the two. ***  The capture was a
    #  SINGLE word, so SHIP WITH CHANGES read as SHIP and every OPTION A/B/C
    #  collapsed to OPTION.  A dissent and an endorsement became one token.
    ("multiword",      "VERDICT: SHIP WITH CHANGES", (), "SHIP WITH CHANGES"),
    ("multiword bold", "VERDICT: " + ST * 2 + "SHIP WITH CHANGES" + ST * 2, (),
                       "SHIP WITH CHANGES"),

    #  The original failure: a brief lists its menu, a seat echoes the brief,
    #  and a naive grep reports the LAST option as the seat's answer.
    ("menu line rejected",
     "VERDICT: SHIP / VERDICT: DO NOT SHIP -- one line", (), None),

    #  A wrapped menu puts ONE token on the continuation line, so the
    #  count-per-line rule alone is not enough; the brief-line guard catches it.
    ("wrapped menu rejected",
     "VERDICT: DO NOT SHIP", ("VERDICT: DO NOT SHIP",), None),

    ("instruction rejected",
     "Open with VERDICT: SHIP on line one, then reasoning.", (), None),

    #  A real answer sitting below an echoed brief must still be found --
    #  rejecting the echo must not also reject the answer.
    ("answer after echo",
     "VERDICT: SHIP / VERDICT: DO NOT SHIP -- one line\nI read the diff.\n"
     "VERDICT: DO NOT SHIP", (), "DO NOT SHIP"),

    ("silent seat", "I could not reach the repository.", (), None),

    #  *** FIVE FORMS THREE PANEL SEATS NAMED AND A MEASUREMENT CONFIRMED,
    #  AFTER the first 11 rows were already green. ***  That is the ask-again
    #  earning its keep: a clean table redirects seats away from the shapes the
    #  author already thought of.
    ("label emphasis",  "" + ST * 2 + "VERDICT" + ST * 2 + ": SHIP", (), "SHIP"),
    ("lowercase",       "verdict: ship", (), "SHIP"),
    ("em dash",         "VERDICT " + EMDASH + " SHIP", (), "SHIP"),
    ("en dash",         "VERDICT " + ENDASH + " DO NOT SHIP", (), "DO NOT SHIP"),
    ("quoted value",    "VERDICT: " + DQ + "SHIP" + DQ, (), "SHIP"),

    #  *** AND THE ONE THAT WAS WORSE THAN A MISS. ***  This returned the single
    #  letter "S" -- not None, an actual token that would have been REPORTED as
    #  the seat's verdict, because [A-Z][A-Z-]* matched the S and stopped at the
    #  lowercase.  A silent WRONG answer, which is the failure this file exists
    #  to prevent, arriving through the fix for the failure it was built for.
    ("title case",      "VERDICT: Ship with changes", (), "SHIP WITH CHANGES"),
]

#  Each mutant is applied to this module's own source; `rows` names the cases
#  that MUST redden under it.
#  Each mutant is a LIST of (find, replace) edits applied to this module's own
#  source, plus the case labels that MUST redden under it.
MUTANTS = [
    ("M1  value-emphasis class dropped (shipped defect, restored)",
     [('[*_`\\x22\\x27]{0,3}', "")],
     ("bold", "underscore", "backtick", "multiword bold", "quoted value")),

    ("M2  capture narrowed to one word (the worse shipped defect)",
     [('(?:\\s+[A-Za-z][A-Za-z-]*){0,3}', "")],
     ("multiword", "multiword bold", "title case", "en dash")),

    ("M3  per-line token count dropped",
     [("if len(VERDICT_RE.findall(line)) != 1:", "if False:")],
     ("menu line rejected",)),

    ("M4  brief-line guard dropped",
     [("if st in brief_lines:", "if False:")],
     ("wrapped menu rejected",)),

    ("M5  instructional guard dropped",
     [("if any(k in low for k in INSTRUCTIONAL):", "if False:")],
     ("instruction rejected",)),

    #  *** THERE IS NO M6, AND ITS ABSENCE IS A RESULT. ***  It was written to
    #  kill a LEADING emphasis class matching the `**` of `**VERDICT**: SHIP`,
    #  and it measured GREEN -- because re.search is UNANCHORED, so the match
    #  simply starts at VERDICT and the TRAILING class consumes the closing
    #  `**`.  The leading class was dead the moment it was written.
    #
    #  It is deleted rather than kept-and-annotated: the `label emphasis` row
    #  still passes without it, which is the proof.  A mutant that cannot be
    #  made to fail is telling you the code it targets does nothing.

    ("M7  dash separators dropped",
     [('[:—–-]', ":")],
     ("em dash", "en dash")),

    #  *** THE HISTORICAL DEFECT, WHICH TAKES TWO EDITS TO RECONSTRUCT. ***
    #  `re.I` supplies the case-insensitivity, so narrowing the class alone is
    #  a NO-OP -- a one-edit mutant measured GREEN and reported these rows as
    #  defended when nothing defended them.  Both edits together restore
    #  exactly what shipped: "VERDICT: Ship with changes" -> the single letter
    #  "S", the silent WRONG answer.
    ("M8  case-sensitivity restored (class AND flag)",
     [('([A-Za-z][A-Za-z-]{1,}(?:\\s+[A-Za-z][A-Za-z-]*){0,3})', '([A-Z][A-Z-]*(?:\\s+[A-Z][A-Z-]*){0,3})'),
      ("    re.I)", "    0)")],
     ("lowercase", "title case")),

    #  With M8's regex in place the one-character guard is what turns that
    #  "S" into a MISS instead of a WRONG ANSWER.  Dropping the guard on top
    #  of M8 is the only way to reach it, which is why this mutant carries
    #  three edits and why the guard is not dead code.
    ("M9  one-character guard dropped (on top of M8)",
     [('([A-Za-z][A-Za-z-]{1,}(?:\\s+[A-Za-z][A-Za-z-]*){0,3})', '([A-Z][A-Z-]*(?:\\s+[A-Z][A-Z-]*){0,3})'),
      ("    re.I)", "    0)"),
      ("        if len(v) < 2:", "        if False:")],
     ("title case",)),
]


def selftest():
    import types
    src = io.open(__file__, encoding="utf-8").read()
    fails = []

    bad = []
    for label, text, briefs, want in CASES:
        got = verdict_of(text, set(briefs))
        if got != want:
            bad.append("%s: got %r want %r" % (label, got, want))
    for b in bad:
        fails.append("FAIL  " + b)
    print("  %-50s %d/%d rows" % ("the shipped extractor",
                                  len(CASES) - len(bad), len(CASES)))

    for label, edits, must_redden in MUTANTS:
        missing = [f for f, _ in edits if f not in src]
        if missing:
            #  *** A MUTANT WHOSE TEXT IS GONE SILENTLY STOPS TESTING.
            #  ***  It happened here: the regex was rewritten and three
            #  mutants kept pointing at text that no longer existed.
            fails.append("FAIL  MUTANT TEXT NOT FOUND, so it never ran: "
                         "%s -- missing %r" % (label, missing[0][:40]))
            continue
        m = types.ModuleType("m")
        m.__dict__["__file__"] = __file__
        try:
            mut = src
            for f, r in edits:
                mut = mut.replace(f, r, 1)
            exec(compile(mut, "<mutant>", "exec"), m.__dict__)
        except Exception:
            print("  %-50s did not compile (counts as red)" % label)
            continue
        red = set()
        for lbl, text, briefs, want in CASES:
            try:
                if m.verdict_of(text, set(briefs)) != want:
                    red.add(lbl)
            except Exception:
                red.add(lbl)
        missed = [r for r in must_redden if r not in red]
        if missed:
            fails.append("FAIL  %s -- rows stayed GREEN under it, so they are "
                         "VACUOUS: %s" % (label, ", ".join(missed)))
        else:
            print("  %-50s reddens %s" % (label, ", ".join(sorted(red))))

    for f in fails:
        print("  " + f)
    if fails:
        print("SEAT_VERDICTS_SELFTEST_FAIL  %d problem(s)" % len(fails))
        return 1
    print("SEAT_VERDICTS_SELFTEST_PASS  %d rows, %d mutants, every mutant red"
          % (len(CASES), len(MUTANTS)))
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    sys.exit(main())
