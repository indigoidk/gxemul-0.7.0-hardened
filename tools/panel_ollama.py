#!/usr/bin/env python3
"""One Ollama-cloud panel seat. Run from Windows git-bash (NOT WSL -- WSL
cannot reach the Windows host's localhost:11434). Writes a utf-8 file; never
print()s the response (git-bash stdout is cp1252 and crashes on it).

    python panel_ollama.py <model> <out_file> <brief_file>
"""
import json
import sys
import urllib.request

model, out, brief_path = sys.argv[1], sys.argv[2], sys.argv[3]
brief = open(brief_path, encoding="utf-8").read()

#  *** THE PACKET-FED PREAMBLE, AND IT IS PREPENDED HERE RATHER THAN WRITTEN INTO EACH
#  BRIEF ON PURPOSE. ***
#
#  These seats CANNOT read files.  The carrier has said so for months, and it asserted
#  that this script wraps the brief in a "PACKET_BRIEF" -- IT DID NOT.  This file sent
#  the brief VERBATIM, so a brief written for the file-reading seats reached the cloud
#  seats carrying instructions they cannot obey: "you may check the premises against the
#  source", "grep the fork for how other devices handle this".
#
#  A seat that TRIES to comply stalls.  Measured 2026-08-27: kimi-k3:cloud returned 127
#  bytes -- "I'll check the premises against the actual tree before reasoning about any
#  of them. Starting by locating" -- and stopped.  With the CLI seat 403-walled, that
#  lost the kimi seat entirely, and the extractor filed it as "answered, NO VERDICT LINE
#  (format miss)" rather than as the stall it was.
#
#  This is the exact failure the carrier already records -- "it was never the seat, it
#  was the BRIEF" -- recurring because the remedy lived in PROSE (remember to inline
#  every fact) instead of in the tool that fires every time.  Two of the nine seats were
#  once written off as broken for days for this reason.
#
#  The preamble does not tell the seat to ignore the brief; it tells it what it CANNOT
#  do and what to say instead, so an uncheckable premise comes back as an honest
#  "cannot verify from the packet" rather than as silence.
PACKET_PREAMBLE = """*** YOU ARE A PACKET-FED SEAT.  YOU CANNOT READ FILES, RUN COMMANDS, OR OPEN A
REPOSITORY.  There is no tree for you to look at. ***

The brief below may contain instructions written for the seats that CAN read files --
phrases like "check the premises against the source", "grep the fork", or a file path.
DO NOT ATTEMPT THEM and do not announce that you are about to.  A seat that opens with
"I'll check the actual tree first" and then stops has produced nothing, and that has
cost this panel real seats.

What is wanted from you instead, and it is genuinely valuable BECAUSE you are blind to
the repository: reason from the inlined text alone.  You are the seat most likely to
catch an argument that only works if you already believe the author.

So:
  * Audit the premises AS STATED.  If a premise is self-contradictory, or the
    derivation does not follow from the facts given, say so -- that needs no file.
  * Where a premise CANNOT be settled from the packet, say exactly that, name the
    premise, and say what single fact would settle it.  An honest "not checkable from
    the packet" outranks a confident guess and is recorded as such.
  * Do not pad.  A short answer that names one real defect beats a long one that
    restates the brief.

VERDICT LINE FIRST, so it survives truncation.  Label each claim READ (from the packet)
or REASONED.  Never label anything MEASURED -- you cannot measure.

---- the brief follows ----

"""
brief = PACKET_PREAMBLE + brief


def _ask(payload):
    #  2026-11-02: the daemon forwards the CLIENT's User-Agent to ollama.com for a `:cloud` model, and
    #  Cloudflare there bans urllib's default one ("Python-urllib/3.x") with `HTTP 403 ... error code: 1010`.
    #  Measured in both directions the same minute: curl -A "Python-urllib/3.12" -> 403 (the 1010 HTML);
    #  the same request with any other agent, or urllib with this header -> 200 and the liveness token.
    #  Every "glm SEAT DOWN -- Ollama cloud 403/1010" record from ~2026-10-2x to 11-02 was THIS, not the
    #  account: `ollama run glm-5.3:cloud` from the CLI answered throughout.
    req = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "User-Agent": "gxemul-panel/1.0"})
    return json.load(urllib.request.urlopen(req, timeout=1500))


try:
    resp = _ask({"model": model, "prompt": brief, "stream": False})
    body = resp.get("response") or ""

    #  *** THE THINKING-BURN RECOVERY.  MEASURED 2026-09-07, after glm burned TWICE IN ONE DAY
    #  and both answers had to be recovered by hand. ***
    #
    #  The burn signature is an EMPTY `response` beside a huge `thinking` field, with
    #  done_reason "stop" -- the model FINISHES and never emits an answer.  It is invisible to
    #  every size check (glm's burns were 115 kB and 121 kB, among the largest files in their
    #  panels) and `seat_verdicts.py` correctly reports SEAT DOWN, which is honest and loses the
    #  answer anyway.
    #
    #  *** BOTH RECOVERED BURNS CONTAINED THE BEST CRITIQUE IN THEIR PANEL. ***  The first found
    #  three unstated premises in a warrant four other seats had ratified; the second
    #  reconstructed a per-row kill matrix from the scores alone.  So the answer is NOT to turn
    #  thinking off -- the hidden reasoning is where this seat's value is.
    #
    #  MEASURED, one small prompt, three states:
    #      glm-5.3:cloud  baseline           response  238   thinking 2363
    #      glm-5.3:cloud  think=False        response 2592   thinking    0
    #      glm-5.3-flash  baseline           response  288   thinking 3676
    #  `think: False` is accepted by this daemon (0.33.2) and moves everything to `response`.
    #  Answer quality was comparable on the control question -- all three were correct.
    #
    #  So: KEEP thinking, and re-fire with it disabled ONLY when the first shot burned.  That
    #  preserves the seat when it works and guarantees an answer when it does not.  The
    #  recovered `thinking` is written out too, because a hand-recovery twice today proved it is
    #  worth reading even when a verdict line is lost.
    if not body.strip():
        thinking = resp.get("thinking") or ""
        note = ("*** THINKING BURN RECOVERED BY panel_ollama.py ***\n"
                "First shot returned an EMPTY response beside %d chars of hidden reasoning\n"
                "(done_reason=%s).  Re-fired with think=False.\n\n"
                % (len(thinking), resp.get("done_reason")))
        try:
            retry = _ask({"model": model, "prompt": brief, "stream": False, "think": False})
            body = retry.get("response") or ""
            note += ("RETRY response: %d chars.\n" % len(body)) if body.strip() else \
                    "RETRY ALSO EMPTY -- the burn is not thinking-budget alone.\n"
        except Exception as re_err:
            note += "RETRY FAILED: %r\n" % (re_err,)
        #  The first shot's reasoning is preserved regardless: it is what was worth reading
        #  both times this happened.
        body = (note + "\n---- retry answer ----\n" + body +
                "\n\n---- first shot's hidden reasoning, preserved ----\n" + thinking)

    if not body.strip():
        body = json.dumps(resp)
except Exception as e:      # a retired model returns an HTTP 500 with a reason
    #  *** READ THE RESPONSE BODY, NOT JUST THE STATUS.  MEASURED 2026-09-06. ***
    #
    #  This used to write `OLLAMA_SEAT_ERROR: <HTTPError 429: 'Too Many Requests'>` and
    #  nothing else.  All three cloud seats returned exactly that, twice, forty minutes
    #  apart -- and the operator read it as a transient rate limit and planned to re-fire
    #  after spacing.  A direct POST to the same endpoint carried the real reason in the
    #  BODY: "you (<user>) have reached your WEEKLY usage limit".  Three of the nine seats
    #  were down for the week, and the seat file said something indistinguishable from a
    #  five-minute wait.
    #
    #  A bare status code cannot tell a transient limit from a quota wall, and this
    #  project's own rule is that a WALL is waited out while a REFUSED CONNECTION is one
    #  command away -- two remedies that need different information to choose between.
    #  urllib puts the server's explanation in the exception's readable body and throws it
    #  away unless somebody asks; asking costs three lines.
    detail = ""
    try:
        raw = e.read()                      # HTTPError is a file-like object
        if raw:
            detail = " BODY: " + raw.decode("utf-8", "replace").strip()
    except Exception:
        pass
    body = "OLLAMA_SEAT_ERROR: %r%s" % (e, detail)
open(out, "w", encoding="utf-8").write(body)
