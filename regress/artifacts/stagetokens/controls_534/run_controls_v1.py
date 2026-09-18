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
    row("t_late", copy.deepcopy(THREE) + [ent("fable5", "review", D2, st.NOPANEL + " x"),
                                         ent("kimi", "review", D3, "a later answer")]),
    #  NOPANEL refused by guard (ii): an answer cites a panel the exemption does not name
    row("t_uncited", [dict(e, ev="_scratchpad/panel_20260910_120000/x.txt") for e in THREE]
        + [ent("fable5", "review", D2, st.NOPANEL + " y")]),
    #  NOTSEAT: entry-scoped -- must NOT exempt the stage
    row("t_notseat", copy.deepcopy(THREE) + [ent("fable5", "review", D2, st.NOTSEAT + " NONCE_NOTSEAT")]),
]
FIX = {k: v for k, v in REAL.items() if k != "rows"}
FIX["rows"] = ROWS
QUEUE = "# fixture queue\n\n### `t_held`\nheld fixture\n"

MUTANTS = {
    "M_reread_not_answer": ("stage_tokens.py",
                            "    return True          # RE_READ entries ARE answers",
                            "    return RE_READ not in n  # MUTANT"),
    "M_notseat_exempts": ("stage_tokens.py",
                          "STAGE_EXEMPT = (ANNOTATION, RE_READ, NOPANEL)",
                          "STAGE_EXEMPT = (ANNOTATION, RE_READ, NOPANEL, NOTSEAT)"),
    "M_no_guard": ("stage_tokens.py",
                   "    if not tok:\n        return []",
                   "    if True:\n        return []"),
    "M_held_blanked": ("gen_dashboard.py",
                       "    ents = [x for x in mine if st.is_answer(x) or st.is_held(x)]",
                       "    ents = [x for x in mine if st.is_answer(x)]"),
    "M_fq_ignores_guard": ("check_fable_queue.py",
                           "if d[\"annotated\"] and not st.stage_token_problems(d[\"all\"]):",
                           "if d[\"annotated\"]:"),
}


def cell_class(html, nonce):
    m = re.search(r'<td class="c (\w+)">(?:(?!</td>).)*?' + nonce, html, re.S)
    return m.group(1) if m else "ABSENT"


def run(mutant, verbose):
    tmp = tempfile.mkdtemp(prefix="st534_")
    try:
        for f in os.listdir(PIPE):
            if f.endswith(".py"):
                shutil.copy(os.path.join(PIPE, f), tmp)
        if mutant != "base":
            f, old, new = MUTANTS[mutant]
            p = os.path.join(tmp, f)
            s = io.open(p, encoding="utf-8").read()
            if s.count(old) != 1:
                return "MUTANT TEXT NOT FOUND (%d)" % s.count(old), False
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

        def has(text, pat):
            return re.search(pat, text, re.M) is not None
        exp = [
            ("CSP t_held HOLD",           has(csp, r"HOLD\s+t_held\s+review")),
            ("CSP t_annot grandfathered", has(csp, r"t_annot\s+review\s+3/9\s+grandfathered")),
            ("CSP t_reread one-seat filing", not has(csp, r"^\s+t_reread")),
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
        good = (green == want_green)
        allgood &= good
        print("%-22s %-7s %s" % (n, "ok" if good else "WRONG", msg))
    print("STAGE_TOKEN_CONTROLS_%s" % ("PASS" if allgood else "FAIL"))
    print("STAGE_TOKEN_CONTROLS_DONE")
