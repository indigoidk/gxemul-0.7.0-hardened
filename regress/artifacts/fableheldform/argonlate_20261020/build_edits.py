"""Build PROPOSED edits (never applied to the repo) against HEAD blobs saved in this work dir.

Inputs  (this dir): CHANGELOG_HEAD.md, OB_HEAD.md, ledger_HEAD_blob.json  -- `git cat-file -p HEAD:<path>`
Outputs (this dir): patched/CHANGELOG.md, patched/OUTSTANDING_BUGS.md, patched/ledger.json
Output  (parent)  : ../edits.diff  -- unified diff, a/ b/ repo-relative paths, line endings preserved
Every replacement must match EXACTLY ONCE in its scope, or the build stops.
"""
import difflib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.dirname(HERE)
os.makedirs(os.path.join(HERE, "patched"), exist_ok=True)


def once(text, old, new, label):
    n = text.count(old)
    if n != 1:
        sys.exit("STOP: %s matched %d times" % (label, n))
    return text.replace(old, new)


# ---------------------------------------------------------------- CHANGELOG.md (LF)
cl = io.open(os.path.join(HERE, "CHANGELOG_HEAD.md"), encoding="utf-8", newline="").read()
cl0 = cl
cl = once(cl, "Seventeen `fable5` entries since 2026-10-16 recorded one in untokened prose",
          "Seventeen `fable5` entries since 2026-10-16 recorded a non-answer in untokened prose", "C1")
cl = once(cl, "* tags fifteen walls with the HELD token, keeping each entry's prose and receipt, and `cxlaunchquotation`'s 2026-10-16\n"
              "  v2 and V3 walls with the non-answer token instead -- a later pass superseded each and Fable answered that one (V4,\n",
          "* tags fifteen non-answers (seven walls, eight passes Fable was not fired on) with the HELD token, keeping each entry's\n"
          "  prose and receipt, and `cxlaunchquotation`'s 2026-10-16 v2 and V3 stalls with the non-answer token instead -- a later\n"
          "  pass superseded each and Fable answered that one (V4,\n", "C2ab")
cl = once(cl, "  one on the v2 wall would already be cleared by V4 (Grok 4.7; GPT-6 Astra's confirm corrected `forever');",
          "  one on the v2 stall would already be cleared by V4 (Grok 4.7; GPT-6 Astra's confirm corrected `forever');", "C2c")
cl = once(cl, "heading its state note with the warrant, and adding to its `hold_question` the packet of the pass Fable walled on;",
          "heading its state note with the warrant, and adding to its `hold_question` the packet of the pass Fable walled on or\n"
          "  was not fired on;", "C3")
cl = once(cl, "`cxlaunchquotation`'s 2026-10-16 wall (Astra, GLM); `cxlaunchquotation` walled on V3 and V6 as well as V7 (all three);",
          "`cxlaunchquotation`'s 2026-10-16 stall (Astra, GLM); `cxlaunchquotation` did not answer V3 (it stalled) or V6 (it\n"
          "walled) as well as V7 (all three);", "C4")
anchor = ("2026-10-17 roster).  `ledger.json`, `OUTSTANDING_BUGS.md`, `fable_queue.md`, `matrix.html` and this block only.\n"
          "\n# Records, 2026-10-18: `ip30abortkill`'s closure records")
cl = once(cl, anchor,
          "2026-10-17 roster).  `ledger.json`, `OUTSTANDING_BUGS.md`, `fable_queue.md`, `matrix.html` and this block only.\n"
          "\n"
          "*Corrected 2026-10-20, from a records check of a late Gemini (Argon) reading of the design pass: this block said\n"
          "`walled Fable entries`, `fifteen walls`, `v2 and V3 walls`, `the 2026-10-16 wall` and `walled on V3`.  Of the\n"
          "seventeen, seven are walls (HTTP 429); `cxlaunchquotation`'s v2 and V3 entries STALLED (stream watchdog, 600 s), as\n"
          "both entries say and GPT-6 Astra and Grok 4.7 said of V3; eight record a pass Fable was not fired on after an earlier\n"
          "wall that day -- and the carrier keeps a seat failure and a seat deliberately not fired apart.  The ledger's own counts\n"
          "give the four Fable walls of 2026-10-17 without V3: V6 at 07:17 and its 07:5x re-fire, `dashokclass` V7 (its third\n"
          "wall that morning) and `cxlaunchquotation` V7 (its fourth wall that day).  The heading keeps the commit subject's\n"
          "wording.*\n"
          "\n# Records, 2026-10-18: `ip30abortkill`'s closure records", "C5")

# ---------------------------------------------------------------- OUTSTANDING_BUGS.md (LF)
ob = io.open(os.path.join(HERE, "OB_HEAD.md"), encoding="utf-8", newline="").read()
ob0 = ob
ob = once(ob, "never agreement; seventeen entries had recorded one\n"
              "  in untokened prose, which `stage_tokens.is_answer()` counts as an answer.  Fifteen now carry the HELD token (prose and\n"
              "  receipt kept); `cxlaunchquotation`'s 2026-10-16 v2 wall and its V3 wall carry the non-answer token instead, because a\n",
          "never agreement; seventeen entries had recorded a\n"
          "  non-answer in untokened prose, which `stage_tokens.is_answer()` counts as an answer.  Fifteen (seven walls, eight\n"
          "  passes Fable was not fired on) now carry the HELD token (prose and receipt kept); `cxlaunchquotation`'s 2026-10-16 v2\n"
          "  stall and its V3 stall carry the non-answer token instead, because a\n", "O12")
ob = once(ob, "(a later-date one could), and one on the v2 wall would already be cleared",
          "(a later-date one could), and one on the v2 stall would already be cleared", "O3")
ob = once(ob, "held a Fable wall written as an untokened\n"
              "  note; a row may not close while a stage awaits a seat (`check_stage_panels.py`, CLOSED-WHILE-HELD), so with the token\n",
          "held a Fable wall, or a pass Fable was not\n"
          "  fired on, written as an untokened note; a row may not close while a stage awaits a seat (`check_stage_panels.py`,\n"
          "  CLOSED-WHILE-HELD), so with the token\n", "O4")
ob = once(ob, "its `hold_question` the packet of the pass Fable walled on.  GPT-6 Astra's confirm on `ip30abortkill` earlier the same\n",
          "its `hold_question` the packet of the pass Fable walled on or was not fired on.  GPT-6 Astra's confirm on\n"
          "  `ip30abortkill` earlier the same\n", "O5")
ob = once(ob, "  of the history when a round touches it (no sweep).\n\n### 2026-10-19 -- `#564`'s stranded gate-6 census",
          "  of the history when a round touches it (no sweep).\n"
          "* **Corrected 2026-10-20** (a records check of a late Gemini (Argon) reading of the design pass): this section said\n"
          "  `walled Fable entries`, `v2 wall`, `V3 wall` and `held a Fable wall` throughout.  Seven of the seventeen are walls;\n"
          "  `cxlaunchquotation`'s v2 and V3 entries STALLED (stream watchdog), as both entries say; eight record a pass Fable\n"
          "  was not fired on after an earlier wall that day.  `untokenedanswers` gains two measured consequences -- an untokened\n"
          "  non-answer also DISCHARGES a live hold (`sgirekills`' assess stage), and `fableheldform`'s own review stage reds\n"
          "  section H when Fable's answer lands -- and a keyword-free option for its forward-only check.\n"
          "\n### 2026-10-19 -- `#564`'s stranded gate-6 census", "O6")

# ---------------------------------------------------------------- ledger.json (CRLF, one field per line)
raw = io.open(os.path.join(HERE, "ledger_HEAD_blob.json"), encoding="utf-8", newline="").read()
lines = raw.split("\r\n")


def row_range(rid):
    idx = [i for i, l in enumerate(lines) if l == '   "id": "%s",' % rid]
    if len(idx) != 1:
        sys.exit("STOP: row %s found %d times" % (rid, len(idx)))
    s = e = idx[0]
    while lines[s] != "  {":
        s -= 1
    while lines[e] not in ("  },", "  }"):
        e += 1
    return s, e


def field_line(rid, key):
    s, e = row_range(rid)
    hit = [i for i in range(s, e) if lines[i].startswith('   "%s": ' % key)]
    if len(hit) != 1:
        sys.exit("STOP: %s.%s found %d times" % (rid, key, len(hit)))
    return hit[0]


def edit_field(rid, key, old, new, label):
    i = field_line(rid, key)
    lines[i] = once(lines[i], old, new, label)


def edit_row_text(rid, old, new, label):
    """for an entry note: the substring must occur exactly once within the row's lines"""
    s, e = row_range(rid)
    hits = [i for i in range(s, e) if old in lines[i]]
    if len(hits) != 1 or lines[hits[0]].count(old) != 1:
        sys.exit("STOP: %s matched %d lines" % (label, len(hits)))
    lines[hits[0]] = lines[hits[0]].replace(old, new)


for t in (chr(34), chr(92)):          # no quote or backslash may enter a JSON string by these edits
    pass

edit_field("fableheldform", "state_note",
           "The records commit tokened the 17 walled Fable entries the census found (15 HELD, 2 non-answer: 16 since the "
           "owner's 2026-10-17 hold plus cxlaunchquotation's 2026-10-16 v2 wall, which",
           "The records commit tokened the 17 untokened Fable non-answers the census found (15 HELD, 2 non-answer: 16 since the "
           "owner's 2026-10-17 hold plus cxlaunchquotation's 2026-10-16 v2 stall, which", "L1")
edit_field("fableheldform", "state_note",
           "6 are Fable's own answers (the cxlaunchquotation and dashokclass V3-V6 passes, read by hand)",
           "6 are Fable's own answers (cxlaunchquotation's V4 and V5 passes and dashokclass's V3-V6, read by hand -- "
           "corrected 2026-10-20: this said `the cxlaunchquotation and dashokclass V3-V6 passes', but cxlaunchquotation's V3 "
           "stalled and its V6 walled, as design pass 1 found)", "L2")
edit_field("fableheldform", "hold_question",
           "is option A right -- the walls tokened HELD,",
           "is option A right -- the walls and not-fired passes tokened HELD,", "L3a")
edit_field("fableheldform", "hold_question",
           "and cxlaunchquotation's two superseded walls given the non-answer token instead?",
           "and cxlaunchquotation's two superseded stalls given the non-answer token instead?", "L3b")
edit_row_text("fableheldform",
              "the census is bounded (cxlaunchquotation's 2026-10-16 v2 wall is the same defect); cxlaunchquotation walled on V3 "
              "and V6 as well as V7;",
              "the census is bounded (cxlaunchquotation's 2026-10-16 v2 stall is the same defect); cxlaunchquotation stalled on V3 "
              "and walled on V6 as well as V7 [corrected 2026-10-20: this said `v2 wall' and `walled on V3'; the answer says "
              "`V2 failure' and `V3 stalled'];", "L4")
edit_row_text("fableheldform",
              "Flags taken: cxlaunchquotation walled on V3 and V6 too; the census undercounts (cxlaunchquotation's 2026-10-16 v2 "
              "wall),",
              "Flags taken: cxlaunchquotation did not answer V3 or V6 either (GLM called V3 a wall; its entry says STALLED); the "
              "census undercounts (cxlaunchquotation's 2026-10-16 v2 stall, GLM's own word),", "L5")

NOTFIRED = "held a Fable non-answer -- a pass Fable was not fired on after its 04:57 wall that day --"
for rid in ("mapledmaaddr", "xscaleinten", "ppcrldimimask", "ppcrlwimiwidth", "ppcgateimageskip"):
    edit_field(rid, "state_note", "held a Fable wall written as untokened prose",
               NOTFIRED + " written as untokened prose", "L6:" + rid)
    edit_field(rid, "reopened", "held a Fable wall recorded as an untokened note",
               NOTFIRED + " recorded as an untokened note", "L7:" + rid)

UA_APPEND = (
    "  ||  [2026-10-20, a records check of a late Gemini (Argon) reading of fableheldform's design pass, measured read-only "
    "on copies of the ledger at HEAD 5dbc000e; receipts to be copied to regress/artifacts/fableheldform/argonlate_20261020/ "
    "before this lands] TWO MEASURED CONSEQUENCES, both waiting on owed item (2), and AN OPTION FOR item (1).  (a) AN "
    "UNTOKENED NON-ANSWER ALSO DISCHARGES A LIVE HOLD: live_holds() counts it as the named seat's answer.  sgirekills' assess "
    "hold [2] (2026-08-30: codex, grok, kimi, opus5) reads discharged for kimi and opus5 only by #564's close entries [70] "
    "and [71], whose notes say the seat `never answered' -- with the non-answer token on those two, sgirekills' re-close "
    "after Fable answers is CLOSED-WHILE-HELD on assess (7/9); without it, section H passes the re-close.  The only "
    "non-answer found among the ledger's 36 discharged (hold, seat) pairs: five matched a broad non-answer keyword net and "
    "were read; three are answers.  (b) fableheldform's own review stage (GPT-6 Astra, plus the Fable hold: 1/9) goes RED in "
    "section H as a 2/9 short panel the moment Fable's answer is recorded -- its narrowed roster is recorded only in the "
    "CHANGELOG.  (c) for item (1), a keyword-free key: a positive answer marker (the `d' glyph, or a new token) required on "
    "every NEW entry counted as an answer.  All 17 fableheldform entries and sgirekills [70]/[71] carry no `d', while 7 "
    "entries counted as answers since 2026-10-01 carry `d' and match a 12-phrase non-answer keyword net in their first 400 "
    "characters -- genuine answers a keyword check would red; the round's own first count, keyed on NOT FIRED, found 8 of "
    "16.  The cost is a habit not yet held: 185 of the 319 entries counted as answers since 2026-10-01 carry no `d'.")
i = field_line("untokenedanswers", "state_note")
if lines[i].endswith('",'):
    lines[i] = lines[i][:-2] + UA_APPEND + '",'
elif lines[i].endswith('"'):                 # the row's last field: no trailing comma
    lines[i] = lines[i][:-1] + UA_APPEND + '"'
else:
    sys.exit("STOP: untokenedanswers.state_note line shape")

new_raw = "\r\n".join(lines)
for txt in (UA_APPEND, NOTFIRED):
    if chr(34) in txt or chr(92) in txt:
        sys.exit("STOP: a quote or backslash would enter a JSON string")
json.loads(new_raw)                                     # still valid JSON

# ---------------------------------------------------------------- write + diff
outs = (("CHANGELOG.md", cl0, cl), ("OUTSTANDING_BUGS.md", ob0, ob), ("tools/pipeline/ledger.json", raw, new_raw))
diff = []
for path, a, b in outs:
    io.open(os.path.join(HERE, "patched", os.path.basename(path)), "w", encoding="utf-8", newline="").write(b)
    al, bl = a.splitlines(keepends=True), b.splitlines(keepends=True)
    d = list(difflib.unified_diff(al, bl, "a/" + path, "b/" + path, n=1))
    if not d:
        sys.exit("STOP: no change in " + path)
    diff.append("diff --git a/%s b/%s\n" % (path, path))
    for ln in d:
        if ln.startswith(("--- ", "+++ ")):
            ln = ln.rstrip("\n") + "\n"
        if not ln.endswith("\n"):
            ln += "\n\\ No newline at end of file\n"
        diff.append(ln)
io.open(os.path.join(OUTDIR, "edits.diff"), "w", encoding="utf-8", newline="").write("".join(diff))
print("BUILD_EDITS_DONE  files=%d  diff_bytes=%d" % (len(outs), len("".join(diff).encode("utf-8"))))
