#!/usr/bin/env python3
"""#534 stage-token controls: CLASSIFICATION per token x tool, plus a RENDER leg (fable5 R5).

Runs the three shipped readers -- check_stage_panels.py, check_fable_queue.py, gen_dashboard.py --
from a COPY of tools/pipeline/ against a FIXTURE ledger, so neither the real ledger nor the real
tools are touched.  With a mutant name it first applies that mutant to the copy; every mutant must
turn at least one expectation red, and the base run must be all green.

    python run_controls.py            # base + every mutant, one line each
    python run_controls.py base -v    # one run, every expectation printed

codex's #532 pass-2 point is why this checks CLASSIFICATION and not exit status: its RE_READ mutant
(is_answer False for RE_READ) passes every exit-status control, because both checkers still exit 0.

CONTRACT (clause e).  Each MUTANTS entry names an edit this instrument is designed to catch; every one is
killed in controls_20260918_v3.out.  DISCLOSED, measured passing 48/48 by the fable5 last seat (#534,
scratchpad fable534/drive_fable.out) and NOT caught: moving the 2026-08-16 POLICY_CUTOFF boundary by a day;
dropping the zero-answer OPEN-hold listing (not the closed-row violation, which IS caught); removing the
`.lower()' on seat comparison (the ledger holds no mixed-case seat id); clause (ii) also reading citations in
an answer's NOTE rather than only its `ev'.  And the dashboard's malformed-hold fallback still does not fire
when the filer has also answered (zero instances in the ledger).  check_fix_seats.py -- the fourth reader
#532 measured -- is NOT covered: it is another round's untracked, unwired draft; its control is owed when it
ships.
"""
import copy
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PIPE = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "tools", "pipeline"))
sys.path.insert(0, PIPE)
import stage_tokens as st  # noqa: E402

REAL = json.load(io.open(os.path.join(PIPE, "ledger.json"), encoding="utf-8"))
SEATS = [s["id"] for s in REAL["seats"]]
TEMPLATE = next(r for r in REAL["rows"] if r.get("state") == "open")


def ent(seat, phase, date, note, ev="", d="✓"):
    return {"seat": seat, "phase": phase, "date": date, "note": note, "ev": ev, "d": d}


def row(rid, entries, state="open"):
    r = copy.deepcopy(TEMPLATE)
    r.update({"id": rid, "state": state, "entries": entries, "commits": None,
              "hold_question": "fixture hold question?"})
    return r


D1, D2, D3 = "2026-09-10", "2026-09-11", "2026-09-12"
THREE = [ent(s, "review", D1, "answer by %s" % s) for s in ("codex", "grok", "glm")]
ROWS = [
    #  HELD: eight answers plus a held flagship seat
    row("t_held", [ent(s, "review", D1, "answer") for s in SEATS if s != "fable5"]
        + [ent("fable5", "review", D1, st.HELD + " fable5] NONCE_HELD waiting", d="⏸")]),
    #  ANNOTATION: three answers and a pre-policy annotation
    row("t_annot", [dict(e, date="2026-08-10") for e in THREE]
        + [ent("fable5", "review", "2026-08-10", st.ANNOTATION + " NONCE_ANNOT")]),
    #  RE_READ: a single-seat re-read -- an ANSWER and a stage exemption at once
    row("t_reread", [ent("fable5", "review", D1, st.RE_READ + " NONCE_REREAD re-read")]),
    #  NOPANEL, honest: no later answer, no uncited panel
    row("t_nopanel", copy.deepcopy(THREE) + [ent("fable5", "review", D2, st.NOPANEL + " NONCE_NOPANEL")]),
    #  NOPANEL refused by guard (i): an answer dated after it
    row("t_late", copy.deepcopy(THREE) + [ent("fable5", "review", D2, st.NOPANEL + " NONCE_LATE x"),
                                         ent("kimi", "review", D3, "a later answer")]),
    #  NOPANEL refused by guard (ii): an answer cites a panel the exemption does not name
    row("t_uncited", [dict(e, ev="_scratchpad/panel_20260910_120000/x.txt") for e in THREE]
        + [ent("fable5", "review", D2, st.NOPANEL + " y")]),
    #  NOTSEAT: entry-scoped -- must NOT exempt the stage
    row("t_notseat", copy.deepcopy(THREE) + [ent("fable5", "review", D2, st.NOTSEAT + " NONCE_NOTSEAT")]),
    # ---- v2 (#534 pass 2: each row closes an escape a seat BUILT) ----
    #  RE_READ as an exemption, not only as an answer: two seats, post-cutoff (grok, codex, Opus)
    row("t_reread2", [ent("codex", "review", D1, "a filing"),
                      ent("grok", "review", D1, st.RE_READ + " a re-read")]),
    #  ANNOTATION reached AFTER the cutoff, so the date cannot grandfather it first (Opus, grok)
    row("t_annot2", copy.deepcopy(THREE) + [ent("fable5", "review", D1, st.ANNOTATION + " post-cutoff")]),
    #  guard (i) is strict: an answer dated THE SAME DAY as the exemption does not refuse it (Opus: >=)
    row("t_sameday", copy.deepcopy(THREE) + [ent("fable5", "review", D2, st.NOPANEL + " z"),
                                            ent("kimi", "review", D2, "same-day answer")]),
    #  two exemptions with an answer between: the NEWEST exemption governs (Opus: min vs max)
    row("t_twonop", copy.deepcopy(THREE) + [ent("fable5", "review", D1, st.NOPANEL + " first"),
                                           ent("kimi", "review", D2, "between"),
                                           ent("fable5", "review", D3, st.NOPANEL + " restated")]),
    #  guard (ii) reads EVERY cited panel, not the first (Opus: findall()[:1])
    row("t_twopanel", [dict(e, ev="_scratchpad/panel_20260910_120000/a _scratchpad/panel_20260910_130000/b")
                       for e in THREE]
        + [ent("fable5", "review", D2, st.NOPANEL + " names panel_20260910_120000 only")]),
    #  an entry carrying BOTH a hold and an exemption is a HOLD, and exempts nothing (deepseek, Opus)
    row("t_heldnop", copy.deepcopy(THREE) + [ent("fable5", "review", D2,
                                                st.HELD + " fable5] " + st.NOPANEL + " both")]),
    #  a LIVE hold beats a full count (heldmasked, L3 of this round) ...
    row("t_fullhold", [ent(s, "review", D1, "answer") for s in SEATS]
        + [ent("fable5", "review", D2, st.HELD + " glm] NONCE_FULLHOLD re-fire glm", d="HELD")]),
    #  ... and a row may not CLOSE over one ...
    row("t_fullclosed", [ent(s, "review", D1, "answer") for s in SEATS]
        + [ent("fable5", "review", D2, st.HELD + " glm] re-fire", d="HELD")], state="closed"),
    #  ... but a DISCHARGED hold (the named seat answered strictly later) does not hold anything
    row("t_discharged", [ent(s, "review", D2, "answer") for s in SEATS]
        + [ent("fable5", "review", D1, st.HELD + " glm, kimi] old hold", d="HELD")], state="closed"),
    # ---- v3 (#534 F2 pass: codex + Opus built these escapes against v2) ----
    #  a hold naming SEVERAL seats, one of which answered later: the other still holds (N10, codex `;')
    row("t_partial", [ent(s, "review", D1, "answer") for s in SEATS]
        + [ent("fable5", "review", D2, st.HELD + " glm, kimi] NONCE_PARTIAL", d="HELD"),
           ent("glm", "review", D3, "glm re-fired")]),
    #  a later answer by a DIFFERENT seat does not discharge (N3) ...
    row("t_otherseat", [ent(s, "review", D1, "answer") for s in SEATS]
        + [ent("fable5", "review", D2, st.HELD + " glm] x", d="HELD"), ent("kimi", "review", D3, "not glm")]),
    #  ... nor does a later NON-ANSWER by the named seat (N4)
    row("t_notseatdis", [ent(s, "review", D1, "answer") for s in SEATS]
        + [ent("fable5", "review", D2, st.HELD + " glm] x", d="HELD"),
           ent("glm", "review", D3, st.NOTSEAT + " a record")]),
    #  clause (i) binds ANNOTATION and RE_READ too (N1: F8 had no row) ...
    row("t_annlate", copy.deepcopy(THREE) + [ent("fable5", "review", D1, st.ANNOTATION + " a"),
                                            ent("kimi", "review", D3, "later")]),
    row("t_rereadlate", [ent("codex", "review", D1, "a filing"),
                         ent("grok", "review", D1, st.RE_READ + " NONCE_RRLATE"),
                         ent("kimi", "review", D3, "later")]),
    #  ... including a later answer by the SAME SEAT that wrote the exemption -- the n6 shape, the one
    #  real disputed stage; every other *late row used kimi (fable5, #534 last seat: F_selfseat_skip 48/48)
    row("t_selflate", copy.deepcopy(THREE) + [ent("fable5", "review", D1, st.ANNOTATION + " self"),
                                             ent("fable5", "review", D3, "the annotator's own later answer")]),
    #  ... but a later answer that itself PREDATES the directive is not judged by it (kimi)
    row("t_prepolicy", [dict(e, date="2026-08-10") for e in THREE]
        + [ent("fable5", "review", "2026-08-10", st.ANNOTATION + " b"),
           ent("kimi", "review", "2026-08-12", "later but pre-policy")]),
    #  a SHORT stage whose only hold is discharged is not held: its real gap shows (codex, Opus)
    row("t_shortdis", copy.deepcopy([dict(e, date=D2) for e in THREE])
        + [ent("fable5", "review", D1, st.HELD + " fable5] x", d="HELD"), ent("fable5", "review", D2, "answered")]),
    #  a CLOSED row whose stage holds ONLY a live hold (no answers) (codex, Opus)
    row("t_zeroheld", [ent("fable5", "review", D2, st.HELD + " glm] x", d="HELD")], state="closed"),
    #  a MALFORMED hold on a full, closed stage (codex)
    row("t_malformed", [ent(s, "review", D1, "answer") for s in SEATS]
        + [ent("fable5", "review", D2, st.HELD + " glm,] x", d="HELD")], state="closed"),
    #  answers picked latest-by-date, not list-last (N5, grok)
    row("t_order", [ent("codex", "review", D2, "NONCE_NEW newer"),
                    ent("codex", "review", D1, "NONCE_OLD older", d="✕"),
                    ent("grok", "review", D1, "g"), ent("glm", "review", D1, "l")]),
    #  section I: a short, flagship-less stage whose only hold is DISCHARGED is short, not held (codex)
    row("t_fqdis", [dict(e, date=D2) for e in THREE]
        + [ent("fable5", "review", D1, st.HELD + " opus5] x", d="HELD"), ent("opus5", "review", D2, "answered")]),
    #  a record filed after the seat's own answer still shows in that ANSWER cell (codex)
    row("t_ansrec", copy.deepcopy(THREE) + [ent("codex", "review", D2, st.NOTSEAT + " NONCE_ANSREC")]),
    #  ... and a SAME-DAY answer does not discharge it: the carrier's strictly-later rule, paid for by
    #  six mis-clears on 2026-08-30 by same-date siblings written in the batch that made the marker
    row("t_samedayhold", [ent(s, "review", D2, "answer") for s in SEATS]
        + [ent("fable5", "review", D2, st.HELD + " glm] same-day", d="HELD")]),
    #  an entry carrying NOTSEAT AND an exemption token exempts nothing (minimax)
    row("t_notseatnop", copy.deepcopy(THREE) + [ent("fable5", "review", D2,
                                                   st.NOTSEAT + " " + st.NOPANEL + " quoted")]),
    #  a HELD marker filed under a seat that has NOT answered is not that seat's answer (codex: HELD == n)
    row("t_heldelse", copy.deepcopy(THREE) + [ent("kimi", "review", D2,
                                                 st.HELD + " opus5] NONCE_HELDELSE", d="HELD")]),
]
FIX = {k: v for k, v in REAL.items() if k != "rows"}
FIX["rows"] = ROWS
QUEUE = ("# fixture queue\n\n### `t_held`\nheld fixture\n### `t_fullhold`\nx\n### `t_heldelse`\nx\n\n"
         "<!-- BEGIN GENERATED: codex-wall -- edit gen_codex_wall.py, not this block -->\n"
         "<!-- END GENERATED: codex-wall -->\n")

MUTANTS = {
    "M_reread_not_answer": ("stage_tokens.py",
                            "    return True          # RE_READ entries ARE answers",
                            "    return RE_READ not in n  # MUTANT"),
    #  M_notseat_exempts (NOTSEAT added to STAGE_EXEMPT) RETIRED as EQUIVALENT once exempts_stage
    #  excluded NOTSEAT outright -- measured 33/33 green in the v2 table, a result, not noise.  The
    #  property it pinned is now carried by M_notseat_not_dominant.
    "M_no_guard": ("stage_tokens.py",
                   "    if not tok:\n        return []",
                   "    if True:\n        return []"),
    "M_held_blanked": ("gen_dashboard.py",
                       "    return ('<td class=\"c hold\">",
                       "    return ('<td class=\"c pend\">"),
    "M_reread_not_exempt": ("stage_tokens.py",
                            "STAGE_EXEMPT = (ANNOTATION, RE_READ, NOPANEL)",
                            "STAGE_EXEMPT = (ANNOTATION, NOPANEL)"),
    "M_annot_not_exempt": ("stage_tokens.py",
                           "STAGE_EXEMPT = (ANNOTATION, RE_READ, NOPANEL)",
                           "STAGE_EXEMPT = (RE_READ, NOPANEL)"),
    "M_held_exempts": ("stage_tokens.py",
                       "    return (not is_held(e)) and NOTSEAT not in n and any(",
                       "    return NOTSEAT not in n and any("),
    "M_min_not_max": ("stage_tokens.py",
                      '    newest_tok = max((e.get("date") or "") for e in tok)',
                      '    newest_tok = min((e.get("date") or "") for e in tok)'),
    "M_ge_not_gt": ("stage_tokens.py",
                    "        if d > newest_tok and d >= POLICY_CUTOFF:",
                    "        if d >= newest_tok and d >= POLICY_CUTOFF:"),
    "M_first_panel_only": ("stage_tokens.py",
                           '            for p in PANEL_DIR.findall(e.get("ev") or ""):',
                           '            for p in PANEL_DIR.findall(e.get("ev") or "")[:1]:'),
    "M_held_is_answer": ("stage_tokens.py",
                         "    if HELD in n or NOTSEAT in n",
                         "    if HELD == n or NOTSEAT in n"),
    "M_count_beats_hold": ("check_stage_panels.py",
                           "            if len(got) >= n_seats and not live:",
                           "            if len(got) >= n_seats:"),
    "M_discharge_ge": ("stage_tokens.py",
                       'and (e.get("date") or "") > hd',
                       'and (e.get("date") or "") >= hd'),
    "M_dash_hold_by_d": ("gen_dashboard.py",
                         '    if seat["id"] in st.live_holds(stage):',
                         "    if False:"),
    "M_wall_notseat": ("gen_codex_wall.py",
                       "MARKER = st.HELD_SEATS",
                       "MARKER = re.compile(re.escape(st.NOTSEAT))"),
    "M_partial_literal": ("check_stage_panels.py",
                          '            live = st.live_holds(info.get("_all", []))',
                          '            live = st.live_holds(info.get("_all", [])) if "PRE-2026-08-16 POLICY" else []'),
    "M_notseat_not_dominant": ("stage_tokens.py",
                               " and NOTSEAT not in n and any(",
                               " and any("),
    "M_dash_hides_refusal": ("gen_dashboard.py",
                             "if any(st.exempts_stage(r) for r in recs) else []\n        if refused:",
                             "if any(st.exempts_stage(r) for r in recs) else []\n        if False:"),
    # ---- v3 ----
    "M_selfseat_skip": ("stage_tokens.py",
                        "        if not is_answer(e) or e in tok:",
                        "        if not is_answer(e) or e in tok or e.get(\"seat\") in {t.get(\"seat\") for t in tok}:"),
    "M_first_seat_only": ("stage_tokens.py",
                          'for x in m.group(1).split(",")] if m else []',
                          'for x in m.group(1).split(",")][:1] if m else []'),
    "M_clause_i_nopanel_only": ("stage_tokens.py",
                                "        if d > newest_tok and d >= POLICY_CUTOFF:",
                                "        if d > newest_tok and d >= POLICY_CUTOFF and nop:"),
    "M_no_policy_cutoff": ("stage_tokens.py",
                           "        if d > newest_tok and d >= POLICY_CUTOFF:",
                           "        if d > newest_tok:"),
    "M_any_seat_discharges": ("stage_tokens.py",
                              '            done = any((e.get("seat") or "").lower() == seat and is_answer(e)',
                              "            done = any(is_answer(e)"),
    "M_any_entry_discharges": ("stage_tokens.py",
                               '(e.get("seat") or "").lower() == seat and is_answer(e)',
                               '(e.get("seat") or "").lower() == seat'),
    "M_no_malformed": ("stage_tokens.py",
                       "            if MALFORMED not in out:\n                out.append(MALFORMED)",
                       "            pass"),
    "M_no_fold": ("stage_tokens.py",
                  "                v = fold(n)",
                  "                v = None"),
    "M_short_stale_hold": ("check_stage_panels.py",
                           '            if live:\n                if row.get("state") == "closed":',
                           '            if live or info.get("_held"):\n                if row.get("state") == "closed":'),
    "M_zero_skip": ("check_stage_panels.py",
                    '                if live0 and row.get("state") == "closed":',
                    "                if False:"),
    "M_fq_stale_hold": ("check_fable_queue.py",
                        'if d["held"] and st.live_holds(d["all"]):',
                        'if d["held"]:'),
    "M_wall_all_markers": ("gen_codex_wall.py",
                           '                if not s.startswith("?") and s not in live.get(e.get("phase", "?"), ()):',
                           "                if False:"),
    "M_dash_listlast": ("gen_dashboard.py",
                        "    ent = _latest(ents)",
                        "    ent = ents[-1]"),
    "M_dash_no_ansrec": ("gen_dashboard.py",
                         "    for r in (x for x in mine if not st.is_answer(x) and not st.is_held(x)):",
                         "    for r in ():"),
    "M_dash_rr_silent": ("gen_dashboard.py",
                         "    if st.exempts_stage(ent):",
                         "    if False:"),
    "M_fq_ignores_guard": ("check_fable_queue.py",
                           "if d[\"annotated\"] and not st.stage_token_problems(d[\"all\"]):",
                           "if d[\"annotated\"]:"),
}


def cell_classes(html, nonce):
    """Every cell (by class) whose tooltip carries the nonce -- a hold renders in several columns."""
    return re.findall(r'<td class="c (\w+)">(?:(?!</td>).)*?' + nonce, html, re.S)


def cell_class(html, nonce):
    m = re.search(r'<td class="c (\w+)">(?:(?!</td>).)*?' + nonce, html, re.S)
    return m.group(1) if m else "ABSENT"


def run(mutant, verbose):
    tmp = tempfile.mkdtemp(prefix="st534_")
    try:
        for f in os.listdir(PIPE):
            if f.endswith(".py"):
                shutil.copy(os.path.join(PIPE, f), tmp)
        #  a PLANTED offender: H2 must flag exactly this file, including its `+'-built spellings
        io.open(os.path.join(tmp, "fx_planted.py"), "w", encoding="utf-8").write(
            'A = "NOT A SEAT " + "ANSWER]"\nB = "PRE-2026-08-16 " + "POLICY"\n')
        if mutant != "base":
            f, old, new = MUTANTS[mutant]
            p = os.path.join(tmp, f)
            s = io.open(p, encoding="utf-8").read()
            if s.count(old) != 1:
                #  None, not False: a mutant that did not apply must never score as "killed"
                return "MUTANT TEXT NOT FOUND (%d)" % s.count(old), None
            io.open(p, "w", encoding="utf-8").write(s.replace(old, new))
        led = os.path.join(tmp, "fixture_ledger.json")
        io.open(led, "w", encoding="utf-8").write(json.dumps(FIX, ensure_ascii=False))
        q = os.path.join(tmp, "fixture_queue.md")
        io.open(q, "w", encoding="utf-8").write(QUEUE)
        env = dict(os.environ, GXLEDGER=led, GXQUEUE=q)
        py = sys.executable
        csp = subprocess.run([py, os.path.join(tmp, "check_stage_panels.py"), "--list"], env=env,
                             capture_output=True, text=True, encoding="utf-8").stdout
        fq = subprocess.run([py, os.path.join(tmp, "check_fable_queue.py"), "--list"], env=env,
                            capture_output=True, text=True, encoding="utf-8").stdout
        out = os.path.join(tmp, "m.html")
        subprocess.run([py, os.path.join(tmp, "gen_dashboard.py"), "--out", out], env=env,
                       capture_output=True, text=True, encoding="utf-8")
        html = io.open(out, encoding="utf-8").read() if os.path.exists(out) else ""
        subprocess.run([py, os.path.join(tmp, "gen_codex_wall.py")], env=env,
                       capture_output=True, text=True, encoding="utf-8")
        wall = io.open(q, encoding="utf-8").read()
        wall = wall[wall.index("BEGIN GENERATED"):] if "BEGIN GENERATED" in wall else ""
        sc = subprocess.run([py, os.path.join(tmp, "stage_tokens.py"), "--selfcheck"],
                            capture_output=True, text=True, encoding="utf-8").stdout

        def has(text, pat):
            return re.search(pat, text, re.M) is not None
        exp = [
            ("CSP t_held HOLD",           has(csp, r"HOLD\s+t_held\s+review")),
            ("CSP t_annot grandfathered", has(csp, r"t_annot\s+review\s+3/9\s+grandfathered")),
            ("CSP t_reread one-seat filing", not has(csp, r"^\s+t_reread\s")),
            ("CSP t_nopanel exempt",      has(csp, r"t_nopanel\s+review\s+3/9\s+grandfathered")),
            ("CSP t_late REFUSED",        has(csp, r"t_late\s+TOKEN-REFUSED")),
            ("CSP t_uncited REFUSED",     has(csp, r"t_uncited\s+TOKEN-REFUSED")),
            ("CSP t_notseat incomplete",  has(csp, r"t_notseat\s+open\s+review\s+3/9")),
            ("FQ t_notseat short",        has(fq, r"t_notseat\s+open\s+review\s+ran with 3")),
            ("FQ t_late short",           has(fq, r"t_late\s+open\s+review\s+ran with 4")),
            ("FQ t_nopanel exempt",       not has(fq, r"t_nopanel\s+open")),
            ("FQ t_held queued",          has(fq, r"t_held\s+review\s+HELD and queued")),
            ("DASH held renders held",    cell_class(html, "NONCE_HELD") == "hold"),
            ("DASH annotation renders tok", cell_class(html, "NONCE_ANNOT") == "tok"),
            ("DASH re-read renders answer", cell_class(html, "NONCE_REREAD") == "ok"),
            ("DASH nopanel renders tok",  cell_class(html, "NONCE_NOPANEL") == "tok"),
            ("DASH notseat renders tok",  cell_class(html, "NONCE_NOTSEAT") == "tok"),
            # ---- v2 ----
            ("CSP t_reread2 exempt",      has(csp, r"t_reread2\s+review\s+2/9\s+grandfathered")),
            ("CSP t_annot2 exempt",       has(csp, r"t_annot2\s+review\s+3/9\s+grandfathered")),
            ("CSP t_sameday exempt",      has(csp, r"t_sameday\s+review\s+4/9\s+grandfathered")),
            ("CSP t_twonop exempt",       has(csp, r"t_twonop\s+review\s+4/9\s+grandfathered")),
            ("CSP t_twopanel REFUSED",    has(csp, r"t_twopanel\s+TOKEN-REFUSED")),
            ("CSP t_heldnop HOLD",        has(csp, r"HOLD\s+t_heldnop\s+review")),
            ("FQ t_heldnop unqueued",     has(fq, r"t_heldnop\s+review\s+HELD but NOT NAMED")),
            ("CSP t_fullhold HOLD 9/9",   has(csp, r"HOLD\s+t_fullhold\s+review\s+9/9\s+awaiting: glm\s*$")),
            ("CSP t_fullclosed CLOSED-WHILE-HELD", has(csp, r"t_fullclosed\s+CLOSED-WHILE-HELD")),
            ("CSP t_notseatnop incomplete", has(csp, r"t_notseatnop\s+open\s+review\s+3/9")),
            ("DASH refused exemption says so", "EXEMPTION REFUSED" in (re.search(
                r'<td class="c tok">(?:(?!</td>).)*?NONCE_LATE', html, re.S) or re.search("$", "")).group(0)),
            ("CSP t_samedayhold HOLD",    has(csp, r"HOLD\s+t_samedayhold\s+review\s+9/9")),
            ("CSP t_discharged complete", has(csp, r"ok\s+t_discharged\s+review\s+9/9")),
            ("DASH hold renders in awaited column", cell_classes(html, "NONCE_FULLHOLD") == ["hold"]),
            ("DASH hold filer is not an answer", cell_classes(html, "NONCE_HELDELSE") == ["hold", "tok"]),
            ("WALL lists t_fullhold",     "`t_fullhold`" in wall),
            ("SELFCHECK flags only the planted file",
             sorted(set(re.findall(r"^\s+(\S+?\.py):", sc, re.M))) == ["fx_planted.py"]
             and len(re.findall(r"^\s+fx_planted\.py:", sc, re.M)) == 2),
            # ---- v3 ----
            ("CSP t_partial awaits kimi only", has(csp, r"HOLD\s+t_partial\s+review\s+9/9\s+awaiting: kimi\s*$")),
            ("DASH partial: kimi hold, glm answer", cell_classes(html, "NONCE_PARTIAL") == ["hold"]),
            ("CSP t_otherseat still HOLD", has(csp, r"HOLD\s+t_otherseat\s+review")),
            ("CSP t_notseatdis still HOLD", has(csp, r"HOLD\s+t_notseatdis\s+review")),
            ("CSP t_annlate REFUSED",     has(csp, r"t_annlate\s+TOKEN-REFUSED")),
            ("CSP t_rereadlate REFUSED",  has(csp, r"t_rereadlate\s+TOKEN-REFUSED")),
            ("CSP t_selflate REFUSED",    has(csp, r"t_selflate\s+TOKEN-REFUSED")),
            ("DASH refused re-read answer warns", "EXEMPTION REFUSED" in (re.search(
                r'<td class="c ok">(?:(?!</td>).)*?NONCE_RRLATE', html, re.S) or re.search("$", "")).group(0)),
            ("CSP t_prepolicy grandfathered", has(csp, r"t_prepolicy\s+review\s+4/9\s+grandfathered")),
            ("CSP t_shortdis incomplete, not held", has(csp, r"t_shortdis\s+open\s+review\s+4/9")),
            ("CSP t_zeroheld CLOSED-WHILE-HELD", has(csp, r"t_zeroheld\s+CLOSED-WHILE-HELD")),
            ("CSP t_malformed CLOSED-WHILE-HELD", has(csp, r"t_malformed\s+CLOSED-WHILE-HELD")),
            ("DASH latest answer by date", cell_classes(html, "NONCE_NEW") == ["ok"]),
            ("DASH record in answer cell", cell_classes(html, "NONCE_ANSREC") == ["ok"]),
            ("FQ t_fqdis short, not held", has(fq, r"t_fqdis\s+open\s+review\s+ran with 4")),
            ("WALL omits discharged holds", "`t_discharged`" not in wall and "`t_shortdis`" not in wall),
        ]
        if verbose:
            for name, ok in exp:
                print("  %-30s %s" % (name, "ok" if ok else "FAIL"))
        bad = [n for n, ok in exp if not ok]
        return ("%d/%d green" % (len(exp) - len(bad), len(exp))
                + ("" if not bad else "  red: " + ", ".join(bad))), not bad
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    verbose = "-v" in sys.argv
    names = [a for a in sys.argv[1:] if not a.startswith("-")] or ["base"] + list(MUTANTS)
    allgood = True
    for n in names:
        msg, green = run(n, verbose)
        want_green = (n == "base")
        good = green is not None and (green == want_green)
        allgood &= good
        print("%-22s %-7s %s" % (n, "ok" if good else "WRONG", msg))
    print("STAGE_TOKEN_CONTROLS_%s" % ("PASS" if allgood else "FAIL"))
    print("STAGE_TOKEN_CONTROLS_DONE")
