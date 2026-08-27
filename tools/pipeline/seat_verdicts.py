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
import json
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
#  #470: A LINE THAT BEGINS `path:NNN:` IS TOOL OUTPUT THE SEAT STREAMED, NEVER ITS OWN
#  PROSE.  The file-reading seats (codex, agy, grok) write their grep and read results
#  into the same file as their answer, so a verdict quoted from ANOTHER PANEL'S RECORD
#  arrives looking exactly like this seat's conclusion.
#
#  *** MEASURED, and this is not hypothetical. ***  On panel_20260826_222557 the
#  extractor reported `codex ... SHIP-WITH ... answered` while codex had issued NO
#  verdict and was STILL RUNNING -- its file grew 909,882 -> 965,763 bytes during the
#  check.  The match was at codex.txt:924, inside a line codex had grepped out of
#  regress/pass2_ledger.tsv: a receipt from 2026-08-18 recording a DIFFERENT panel.
#  A FABRICATED RATIFICATION would have entered the round record.
#
#  SCOPE, measured across every panel dir on disk (1,310 seat files):
#      5,341 lines contain "VERDICT"; 91 of those are grep-output lines.
#      1,062 lines the extractor ACCEPTS as a verdict; this rule kills exactly TWO,
#      both in codex.txt, both the same grepped ledger line, from which it would have
#      taken the verdict "the DECLINE is the".  Zero packet-fed seats affected -- an
#      Ollama seat cannot grep, so its output contains only its own words.
#
#  2 of 1,062 is the whole footprint: it removes the false-positive class and touches
#  nothing else.  It does NOT address the other half of `verdictprose` -- extracting
#  from a seat that has not finished -- which needs a COMPLETION RECORD and is filed
#  with its nine designed controls.  A stable file size is NOT that record: a thinking
#  model stalls its output while still running.
GREP_OUTPUT_LINE = re.compile(r"^[A-Za-z0-9_./\\-]+\.[A-Za-z0-9]{1,5}[-:][0-9]+[-:]")

VERDICT_RE = re.compile(
    #  *** THE DASH MUST BE SURROUNDED BY SPACE, AND THE FIRST VERSION OF
    #  THIS LINE DID NOT SAY SO. ***  A bare [-] in the class matched the
    #  hyphen inside a word, so "a verdict-driven review process" returned
    #  "DRIVEN REVIEW PROCESS" -- a false positive introduced by the fix for
    #  a false negative.  A colon needs no spacing; a dash does.
    #  *** THE LABEL IS ANCHORED TO LINE START, AND WITHOUT THAT A SENTENCE OF
    #  PROSE SWALLOWS A REAL VERDICT. ***  Measured by a review seat:
    #
    #      "My verdict: the code is fine and the records are honest."
    #          ->  "THE CODE IS FINE"
    #
    #  Case-insensitive matching made every mid-sentence "verdict:" a
    #  candidate, and first-qualifying-line-wins means one such sentence of
    #  preamble outranks the seat's actual answer further down.  That is the
    #  silent-wrong-answer class this file exists to prevent, arriving through
    #  the fix for a silent-missing-answer class -- the second time in this
    #  round that the loosening did that.
    #
    #  Only whitespace, emphasis, list and quote markers may precede the
    #  label.  Checked against every row: none has prose before it.
    #  *** AND THE ANCHOR MUST ALSO ADMIT A SENTENCE BOUNDARY, OR IT BLANKS
    #  AN ENTIRE SEAT. ***  Measured: line-start-only rejected 52 of grok's
    #  58 answers, because grok streams its reasoning with no newlines and
    #  ends the giant first line with `...name the mutant.**VERDICT: SHIP
    #  WITH CHANGES**`.  A check that silently blanks one seat in seven is
    #  worse than the false positives it prevents -- that is a seat failure
    #  manufactured by the tool.
    #
    #  So the label is admitted at LINE START or after SENTENCE-ENDING
    #  punctuation, in both cases through optional emphasis and list
    #  markers.  Mid-sentence prose ("My verdict: the code is fine") still
    #  matches neither, which is the whole point.
    #  *** A QUALIFYING WORD MAY SIT BETWEEN THE MARKUP AND THE LABEL, AND
    #  OMITTING IT REPORTED A LIVE SEAT AS WALLED. ***  Measured 2026-08-27:
    #  agy ended with "### **FINAL VERDICT: GO-WITH-CHANGES**".  The class here
    #  allowed MARKUP before VERDICT but not a WORD, so the verdict was missed;
    #  and because the wall test is "keyword in the tail AND no verdict", that
    #  miss let the word "non-quota" -- which the seat used while DISCUSSING
    #  panel.sh's own quota handling -- tip a 10.6 KB answer to *** WALLED ***.
    #
    #  A live seat scored dead is the seat-ledger failure inverted, and it is
    #  the worse direction: a walled seat gets re-fired; a seat recorded walled
    #  that actually ANSWERED becomes an unread review.
    #
    #  Added to the LINE-ANCHORED branch only.  The mid-sentence branch is left
    #  alone deliberately -- that is where "My verdict: the code is fine"
    #  produced a false positive, and widening it would reopen that.
    r"(?:^[ \t]*(?:[*_`#>|+-]{1,6}[ \t]*)*(?:(?:FINAL|OVERALL|SEAT|PANEL)[ \t]*(?:[*_`]{1,3}[ \t]*)?)?|[.!?][ \t]*[*_`]{0,3}[ \t]*)VERDICT[ \t]*[*_`]{0,3}[ \t]*(?::|[ \t]+[—–-][ \t]+)"
    r"\s*[*_`\x22\x27]{0,3}\s*([A-Za-z][A-Za-z-]{1,}(?:\s+[A-Za-z][A-Za-z-]*){0,3})",
    re.I)
#  *** TWO PATTERNS, BECAUSE ANCHORING THE EXTRACTOR BROKE THE OLDEST GUARD
#  IN THIS FILE AND THE SELFTEST CAUGHT IT. ***
#
#  The count-per-line rule -- an INSTRUCTION line lists several tokens, an
#  ANSWER line carries exactly one -- is the discriminator this whole file was
#  built around.  Anchoring VERDICT_RE to line start made the SECOND token on
#  "VERDICT: SHIP / VERDICT: DO NOT SHIP" unmatchable, so findall returned 1,
#  the menu passed the guard, and three rows went red at once.
#
#  So: VERDICT_RE (anchored) EXTRACTS the value; MENU_RE (unanchored) COUNTS
#  candidates on the line.  They must stay in step -- MENU_RE has to match
#  everything VERDICT_RE does, or a real answer gets counted as zero and
#  skipped.
MENU_RE = re.compile(r"VERDICT[ \t]*[*_`]{0,3}[ \t]*(?::|[ \t]+[—–-][ \t]+)", re.I)

WALL_RE = re.compile(
    r"usage limit|rate.?limit|\b429\b|quota|too many requests|"
    r"unknown effort level|unknown model|not authenticated|invalid api key",
    re.I)

SEATS = ("codex", "agy", "grok", "kimi",
         "ollama_glm", "ollama_deepseek", "ollama_minimax",
         #  the kimi SUBSTITUTE transport (added 2026-08-25). The CLI seat
         #  "kimi" above is 403-walled; this is the road that answers.
         "ollama_kimi")


def brief_lines(d):
    for name in ("brief_sent.md", "brief_sent.packet.md"):
        p = os.path.join(d, name)
        if os.path.exists(p):
            txt = io.open(p, encoding="utf-8", errors="replace").read()
            return set(l.strip() for l in txt.splitlines() if len(l.strip()) > 20)
    return set()


def verdicts_of(text, brief_lines=()):
    """EVERY distinct verdict this text offers, in order of appearance.

    *** IT RETURNS A LIST BECAUSE PICKING ONE IS THE FAILURE MODE. ***  A
    measuring seat scored this file over 953 real seat answers and found that
    loosening the regex raised the count of SILENTLY WRONG verdicts from 57 to
    79: the loosening did fix the shapes it targeted, and it converted loud
    failures (a mangled token, a bare None -- a human sees those and checks)
    into quiet ones, a plausible verdict lifted from the wrong line.

    LAST-WINS IS NOT THE FIX, and that was measured too: on this round's own
    pass 2, codex quotes `VERDICT: DO NOT SHIP` inside an ILLUSTRATIVE EXAMPLE
    below its real answer, so last-wins reports codex as DO NOT SHIP.  Neither
    end of the file is reliably the answer.

    So the caller is told about the disagreement instead.  That is this file's
    own doctrine -- never silently convert a failure into agreement -- applied
    to itself, and it needs no guess about which line is the answer.

    *** ONE TOKEN PER LINE IS NOT ENOUGH, MEASURED 2026-08-22. ***  A brief that
    lists its three options WRAPS, and the continuation line then carries a
    single token -- so this returned the brief's own menu as a seat's answer,
    which is the exact failure this whole file exists to stop.  Two further
    guards: skip any line that also appears in the brief, and skip any line that
    still reads as instruction rather than answer.
    """
    #  *** A SEAT RE-RENDERING THE BRIEF'S MENU AS A BULLET DEFEATS ALL THREE
    #  GUARDS, AND IT IS LIVE ON A PANEL FROM TODAY. ***  Measured on
    #  panel_20260823_085034/kimi.txt:4:
    #
    #      - VERDICT LINE FIRST: `VERDICT: SHIP` / `SHIP WITH CHANGES` / ...
    #
    #  Exactly ONE `VERDICT:` on the line, so the count rule passes; re-rendered
    #  as a bullet so it is not byte-identical to any brief line; and it says
    #  "LINE FIRST" rather than "on line one".  The extractor reported SHIP.
    #  The seat had written SHIP WITH CHANGES three times further down.
    out = []
    INSTRUCTIONAL = ("open with", "on line one", "then reasoning", "one line, then",
                     "` or `", "or `verdict", "verdict line first",
                     "line first")
    for line in text.splitlines():
        if len(MENU_RE.findall(line)) != 1:
            continue
        st = line.strip()
        if st in brief_lines:
            continue
        low = st.lower()
        if any(k in low for k in INSTRUCTIONAL):
            continue
        #  *** THE TWO PATTERNS DELIBERATELY DISAGREE, so this cannot assume
        #  a match. ***  MENU_RE is unanchored and counts candidates;
        #  VERDICT_RE is anchored and extracts.  A prose line carrying
        #  "My verdict:" mid-sentence passes the count rule and matches
        #  nothing here -- which is exactly the rejection wanted, but it
        #  arrives as None rather than as a skip.  The first version of
        #  this pairing crashed on it.
        #  #470: skip tool output the seat streamed into its own file.  A line
        #  beginning `path:NNN:` is a grep/read result, never the seat's prose --
        #  and a verdict quoted from another panel's record looks identical to a
        #  conclusion once the label anchor is satisfied.
        if GREP_OUTPUT_LINE.match(line):
            continue
        m = VERDICT_RE.search(line)
        if m is None:
            continue
        v = m.group(1).upper().strip()
        #  belt and braces: a one-character token is a truncated match,
        #  never a verdict, whatever the regex happens to allow today.
        if len(v) < 2:
            continue
        if v not in out:
            out.append(v)
    return out


def verdict_of(text, brief_lines=()):
    """The FIRST distinct verdict, or None.

    Kept because callers and rows read more clearly against a single value,
    but *** ANY CALLER THAT ONLY USES THIS IS THROWING AWAY THE DISAGREEMENT
    SIGNAL ***, which is the thing a measurement showed matters most here.
    Use verdicts_of() and report a split.
    """
    v = verdicts_of(text, brief_lines)
    return v[0] if v else None


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
        vs = verdicts_of(t, bl)
        #  *** REPORT THE DISAGREEMENT; DO NOT RESOLVE IT. ***  Measured: on
        #  406 modern real seat answers, 57 files offer two or more accepted
        #  verdict lines that DISAGREE.  Taking the first is right often
        #  enough to look fine and wrong often enough to matter, and taking
        #  the last is measurably no better.
        v = vs[0] if vs else None
        if len(vs) > 1:
            v = " | ".join(vs) + "   <- SPLIT, read the file"
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
        recovered = ""
        st = t.lstrip()
        if st.startswith('{"model"') and '"response": ""' in st[:4000]:
            reason = "unknown"
            m = re.search(r'"done_reason":\s*"([a-z_]+)"', st)
            if m:
                reason = m.group(1)
            ev = re.search(r'"eval_count":\s*(\d+)', st)
            raw = "%s%s" % (reason, (", %s tokens" % ev.group(1)) if ev else "")

            #  *** AN EMPTY `response` IS NOT ALWAYS A LOST SEAT.  Measured
            #  2026-08-26: kimi-k3:cloud returned `"response": ""` with
            #  `done_reason: "stop"` and 18,002 chars of `thinking` holding a
            #  COMPLETE answer, opening `<|open|>response<|sep|># VERDICT: ...`
            #  and closing cleanly.  The rule above fired and called it DOWN.
            #
            #  THE DISCRIMINATOR IS `done_reason`:
            #    "length" -> ran out mid-thought, no answer exists (the deepseek
            #                case this rule was built from).  Genuinely DOWN.
            #    "stop"   -> the model FINISHED.  If `thinking` carries a
            #                channel-marked response block, the answer EXISTS and
            #                recording the seat as down is the unread-review class
            #                with extra steps -- the answer is on disk already.
            if reason == "stop":
                try:
                    obj = json.loads(st)
                    think = obj.get("thinking") or ""
                except Exception:
                    think = ""
                mm = re.search(r"<\|open\|>response<\|sep\|>(.*?)(?:<\|close\|>|$)",
                               think, re.S)
                cand = (mm.group(1) if mm else "").strip()
                #  Require real substance: a stray marker with a few words is not
                #  an answer, and calling it one would be the mirror failure.
                if len(cand) >= 400:
                    recovered = cand
                    raw = ""

        err = t.lstrip()[:400] if t.lstrip().startswith("OLLAMA_SEAT_ERROR") else ""
        #  MEASURED 2026-08-23: a wall can be a MOMENT, not a state.  Kimi walled
        #  mid-answer at 23:01 with 36 KB already written, and answered a liveness
        #  test an hour later.  So a WALLED row is not a verdict on the seat -- it
        #  is a verdict on that invocation, and the seat should be RE-FIRED ONCE
        #  before the round closes rather than recorded as gone.
        is_walled = bool(WALL_RE.search(t[-600:])) and not v
        if recovered:
            #  Write it beside the raw envelope so the answer is READABLE, not just
            #  known to exist.  A seat whose answer nobody can open is, in practice,
            #  a seat that did not answer.
            rp = os.path.join(d, s + ".RECOVERED.md")
            try:
                io.open(rp, "w", encoding="utf-8", newline="\n").write(recovered + "\n")
            except Exception:
                pass
            vv = verdict_of(recovered)
            if vv:
                v = vv
            state = ("RECOVERED -- answer was in `thinking`, not `response` "
                     "(%d chars -> %s.RECOVERED.md)" % (len(recovered), s))
            answered += 1
        elif raw:
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
BQ = chr(96)    # backtick
NL = chr(10)
BS = chr(92)    # backslash -- Windows path separator in grep output
ENDASH = chr(8211)

CASES = [
    #  (label, text, brief_lines, expected)
    ("plain",          "VERDICT: SHIP", (), "SHIP"),

    #  *** #470, MEASURED on panel_20260826_222557: the extractor reported codex as
    #  SHIP-WITH while codex had issued NO verdict and was still running.  The match
    #  came from a line codex had GREPPED out of regress/pass2_ledger.tsv -- another
    #  panel's verdict, from 2026-08-18, streamed into its own output file.  A
    #  FABRICATED RATIFICATION would have entered the round record.
    #
    #  Both grep forms are covered: a MATCH line uses `path:NNN:` and a CONTEXT line
    #  uses `path-NNN-`.  The real data carried both, side by side.
    #  *** THESE FIXTURES ARE REAL LINES FROM REAL PANEL FILES, NOT SYNTHETIC. ***
    #  The first synthetic attempt was MEASURED VACUOUS by M14: `path:NNN:  VERDICT:`
    #  is rejected by the ANCHOR anyway, because a colon satisfies neither the
    #  line-start branch nor the sentence-boundary branch.  It looked like the defect
    #  and could not reproduce it.  The real lines carry EMPHASIS AND SENTENCE
    #  PUNCTUATION after the grep prefix, which is what satisfies the anchor and is
    #  precisely why the guard is needed.
    ("grep match line with anchor",
     "." + BS + "_scratchpad" + BS + "r52_kimi.txt:450:  " + ST * 2
     + "1. VERDICT: DOCUMENT-ONLY" + ST * 2, (), None),
    ("grep context line with anchor",
     "_scratchpad" + BS + "r100_kimi.txt-1143-  x. VERDICT: unobservable", (), None),

    #  AND THE RULE MUST NOT BLANK A SEAT THAT GREPS: a real verdict AFTER quoted
    #  tool output is still the seat's own conclusion and must be found.
    ("real verdict after grep output",
     "regress/pass2_ledger.tsv:32:  x. VERDICT: DO NOT SHIP" + NL + "VERDICT: SHIP",
     (), "SHIP"),

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

    #  *** EACH OF THESE ISOLATES ONE GUARD, and the first drafts did not. ***
    #  Anchoring the label made four older guards redundant FOR THE ROWS AS
    #  WRITTEN -- every one of those rows was rejected by the anchor before its
    #  own guard was reached, so four mutants could not be made to fail and the
    #  guards looked dead.  They are not dead; the rows were badly cut.  Each
    #  now STARTS with the label, so the anchor passes and only the guard under
    #  test can reject it.
    ("instruction rejected",
     "VERDICT: SHIP -- one line, then reasoning.", (), None),

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

    #  *** THREE ROWS FROM A MEASURED REGRESSION, not from imagination. ***
    #  A measuring seat scored this file over 953 real seat answers and found
    #  that the loosening above, while it cut hard failures from 97 to 36,
    #  raised DISAGREEMENTS from 14 to 57 -- more accepted lines per file,
    #  including echoed menus -- which first-wins then resolved silently.

    #  The bullet form, from panel_20260823_085034/kimi.txt:4.  One VERDICT:
    #  on the line, not byte-identical to any brief line, and it says LINE
    #  FIRST rather than on line one -- so it defeated all three guards and
    #  reported SHIP for a seat that wrote SHIP WITH CHANGES three times.
    ("menu bullet rejected",
     "VERDICT: SHIP -- verdict line first", (), None),

    #  The dash separator matched INSIDE a hyphenated word -- a false
    #  positive introduced by the fix for a false negative.
    #  Starts WITH the label, so the anchor passes and only the separator's
    #  space requirement can reject it.  (Its twin below is the prose-first
    #  form, which isolates the anchor instead -- the two were swapped in the
    #  first draft, so each was tested by the other's guard and M11 could not
    #  be made to fail.)
    ("hyphen not a separator", "verdict-driven review process here.",
     (), None),

    #  A seat that echoes the menu and THEN answers must not be resolved to
    #  the menu's first option.  verdicts_of returns both; main() prints the
    #  split.  This row pins that the real answer is among them.
    ("menu then answer",
     "VERDICT: SHIP / VERDICT: DO NOT SHIP -- one line" + NL
     + "I read the diff." + NL + "VERDICT: SHIP WITH CHANGES",
     (), "SHIP WITH CHANGES"),

    #  *** NEGATIVE ROWS FOR THE LOOSENED CLASSES, WHICH HAD NONE. ***  A seat
    #  pointed out that all five case-insensitivity rows tested the ACCEPT side
    #  only -- so the selftest was 20/20 green while the extractor happily
    #  turned a sentence of prose into a verdict.  A row set that only proves
    #  what should match is half a detector.
    ("prose verdict rejected",
     "My verdict: the code is fine and the records are honest.", (), None),
    ("hyphenated prose rejected",
     "This is a verdict-driven review process.", (), None),

    #  AND THE ONE THAT MATTERS MOST: prose ABOVE a real answer.  First-line-
    #  wins means one sentence of preamble outranks the seat's verdict -- and
    #  this round's own briefs are ABOUT the verdict extractor, so the very
    #  next panel would have hit it.
    ("prose above a real answer",
     "Below is my VERDICT: SHIP as a summary." + NL + "VERDICT: DO NOT SHIP",
     (), "DO NOT SHIP"),

    #  *** THE FORM ONE WHOLE SEAT ACTUALLY USES. ***  grok streams its
    #  reasoning with no newlines and ends the giant first line with the
    #  verdict, so a line-start-only anchor rejected 52 of its 58 answers --
    #  a seat blanked by the tool rather than by the seat.  This row is real
    #  text from panel_20260823_140419/grok.txt.
    ("verdict at a sentence boundary",
     "That is enough to score the three attacks and name the mutant."
     + ST * 2 + "VERDICT: SHIP WITH CHANGES" + ST * 2,
     (), "SHIP WITH CHANGES"),
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
     [("if len(MENU_RE.findall(line)) != 1:", "if False:")],
     ("menu line rejected",)),

    ("M4  brief-line guard dropped",
     [("if st in brief_lines:", "if False:")],
     ("wrapped menu rejected",)),

    ("M5  instructional guard dropped",
     [("if any(k in low for k in INSTRUCTIONAL):", "if False:")],
     ("instruction rejected",)),

    #  *** M6 DIED AND THEN CAME BACK, AND THE ABSENCE RECORD WENT FALSE
    #  WITHIN ONE COMMIT. ***
    #
    #  At e9f8c0c this slot held a note saying there was no M6: a mutant aimed
    #  at a LEADING emphasis class could not be made to fail, because
    #  re.search was UNANCHORED -- the match simply started at VERDICT and the
    #  TRAILING class consumed the closing `**`.  That was measured, and true,
    #  and the class was deleted with its absence recorded as the result.
    #
    #  Then 8eeeea2 ANCHORED the label and introduced a NEW leading class in
    #  the anchor branch -- broader than the one that died, since it also
    #  admits `-`, `>` and `#` list markers -- and nothing re-ran the death
    #  measurement.  A regress seat re-tested it and found the class ALIVE,
    #  load-bearing, and covered by no mutant at all: dropping it reddens
    #  `label emphasis`, measured on HEAD.
    #
    #  *** THE CLAUSE THIS COST: AN ABSENCE RECORD IS TIME-INDEXED. ***  It
    #  must name its warrant -- this one did, which is the only reason it could
    #  be re-tested -- and ANY EDIT TOUCHING THAT WARRANT RE-RUNS THE DEATH
    #  MEASUREMENT.  "Deleted, absence recorded as the result" was the right
    #  disposition; the missing half was the expiry check.
    #  *** THESE TWO MUTANTS ARE COUPLED TO THE PATTERN'S EXACT TEXT, AND AN EDIT TO
    #  THE PATTERN SILENTLY TURNS THEM INTO MIS-BUILT MUTANTS. Measured 2026-08-27. ***
    #  Widening the pattern left `[*_`#>|+-]{0,6}` present ONLY inside these mutant
    #  definitions.  M6 then mutated ITS OWN definition line, changed nothing about the
    #  regex, and the rows stayed GREEN -- which section V correctly reported as a
    #  detector that can no longer be shown to fail.  M12's text vanished outright.
    #
    #  Both are now DERIVED from the live pattern line at runtime-authoring time rather
    #  than transcribed, so the coupling is visible.  A find-text that no longer occurs
    #  in the target is the driver's MUTANT-TEXT-NOT-FOUND fail; a find-text that occurs
    #  only in the mutant's own definition is worse, because it applies cleanly and
    #  proves nothing.
    ("M6  anchor-branch marker class dropped (died at e9f8c0c, alive again",
     [('(?:[*_`#>|+-]{1,6}[ \\t]*)*', "")],
     ("label emphasis",)),

    ("M12 label anchor dropped (prose becomes a verdict)",
     [('(?:^[ \\t]*(?:[*_`#>|+-]{1,6}[ \\t]*)*(?:(?:FINAL|OVERALL|SEAT|PANEL)[ \\t]*(?:[*_`]{1,3}[ \\t]*)?)?|[.!?][ \\t]*[*_`]{0,3}[ \\t]*)', '')],
     ("prose verdict rejected", "prose above a real answer")),

    ("M10 menu-bullet guard dropped (BOTH keywords)",
     [('"verdict line first",', '"@@a@@",'),
      ('"line first")', '"@@b@@")')],
     ("menu bullet rejected",)),

    ("M11 dash separator un-spaced (the hyphen false positive)",
     #  BOTH patterns carry their own copy of the separator, and the count
     #  rule (MENU_RE) is what actually rejects the hyphen row -- mutating
     #  only the extractor left it green.
     [('[ \\t]+[—–-][ \\t]+)', '[—–-])'),
      ('[ \\t]+[—–-][ \\t]+)', '[—–-])')],
     ("hyphen not a separator",)),

    #  *** RE-AIMED: its old target text vanished when the separator was made
    #  space-aware, and the selftest reported MUTANT TEXT NOT FOUND rather
    #  than passing quietly.  That is the failure mode a measuring seat
    #  warned about -- mutants anchored to regex substrings drift with the
    #  next regex edit -- and it is why the not-found case is a FAIL here.
    #  The sentence-boundary branch had NO mutant, so the grok row's only
    #  provable failure was via M2's multiword capture -- attributable to the
    #  wrong feature.  Named by a regress seat.  This edit also documents the
    #  52-of-58 seat-blanking incident as something a single edit can restore.
    #  #470: without this guard a verdict QUOTED from another panel, inside tool
    #  output the seat streamed into its own file, is read as the seat's conclusion.
    ("M14 grep-output guard dropped (a quoted verdict becomes this seat's)",
     [("if GREP_OUTPUT_LINE.match(line):", "if False and GREP_OUTPUT_LINE.match(line):")],
     ("grep match line with anchor", "grep context line with anchor")),

    ("M13 sentence-boundary branch dropped (blanks a whole seat)",
     [('|[.!?][ \\t]*[*_`]{0,3}[ \\t]*)', ')')],
     ("verdict at a sentence boundary",)),

    ("M7  dash separators dropped",
     [('(?::|[ \\t]+[—–-][ \\t]+)', ":")],
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
