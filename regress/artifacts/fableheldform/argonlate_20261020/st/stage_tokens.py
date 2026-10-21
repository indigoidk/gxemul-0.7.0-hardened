"""THE ONE PLACE A LEDGER STAGE TOKEN IS SPELLED OR CLASSIFIED.  #534, 2026-09-18.

WHY THIS FILE EXISTS.  Four tools read ledger entries and each carried its own copy of the tokens:
check_stage_panels.py knew four, check_fable_queue.py was never taught RE_READ, gen_dashboard.py
filtered HELD markers it had no business filtering, and check_fix_seats.py knew only HELD -- so it
credited a stage-exemption entry written under `seat: fable5' as a FLAGSHIP ANSWER, and the row that
introduced the newest token passed its own flagship mandate on that token (#532 pass 2, Opus seat,
MEASURED).  One cause every time: a token added where it was needed and never mirrored.  So the
literals AND the classification live here, and precommit_check.sh refuses a token literal anywhere
else in tools/pipeline/.  *** THREE of those four readers ship with #534 and are covered by its controls;
check_fix_seats.py is another round's untracked, unwired draft -- it imports is_answer from here but NO
control covers it until it ships (fable5, #534 last seat: this sentence overclaimed until then). ***

AN ENTRY HAS TWO INDEPENDENT PROPERTIES, and the #532 code conflated them:

  is_answer(e)     -- does this entry count as the seat answering?
  exempts_stage(e) -- does this entry exempt its WHOLE (row, phase) stage from the panel rule?

                    is_answer   exempts_stage
    HELD             no           no          (a promise; handled by its own rules)
    ANNOTATION       no           yes         (pre-2026-08-16 policy)
    RE_READ          YES          yes         (a real single-seat re-read -- fable measured one
                                               rendering as agreement pre-#532, rightly)
    NOPANEL          no           yes         (no panel was convened on this stage)
    NOTSEAT          no           NO          (THIS ENTRY is a main-loop record, not a seat
                                               answer; it can never silence other entries)
    anything else    yes          no

NOTSEAT IS THE ENTRY-SCOPED MARKER, and it is the one to reach for by default.  #532 used the
stage-scoped NOPANEL for six records that meant only "this entry is not a seat answer"; on those
rows any panel LATER recorded under the same phase would have been silently exempted in advance
(fable5, #532 pass 2, R2).  A stage exemption is a claim about everything in the stage and must be
earned; see stage_token_problems() for the guard.
"""
import re

HELD = "[HELD AWAITING SEAT:"
ANNOTATION = "[RUN UNDER THE PRE-2026-08-16 POLICY]"
RE_READ = "[NOT A PANEL STAGE: SINGLE-SEAT RE-READ]"
NOPANEL = "[NOT A PANEL STAGE: NO PANEL CONVENED]"
NOTSEAT = "[NOT A SEAT ANSWER]"

STAGE_EXEMPT = (ANNOTATION, RE_READ, NOPANEL)
ALL = (HELD, ANNOTATION, RE_READ, NOPANEL, NOTSEAT)

PANEL_DIR = re.compile(r"panel_\d{8}_\d{6}")


def _note(e):
    return e.get("note") or ""


def is_held(e):
    return HELD in _note(e)


def exempts_stage(e):
    n = _note(e)
    #  HELD and NOTSEAT both dominate: a hold is a promise and NOTSEAT says "this entry only" -- an
    #  entry carrying either can never exempt the stage, whatever else it quotes (minimax, #534 pass 2:
    #  the docstring promised this of NOTSEAT and the code did not deliver it).
    return (not is_held(e)) and NOTSEAT not in n and any(t in n for t in STAGE_EXEMPT)


def is_answer(e):
    n = _note(e)
    if HELD in n or NOTSEAT in n or ANNOTATION in n or NOPANEL in n:
        return False
    return True          # RE_READ entries ARE answers; so is every untokened entry


HELD_SEATS = re.compile(re.escape(HELD) + r"[ \t]*([a-z0-9_]+(?:[ \t]*,[ \t]*[a-z0-9_]+)*)[ \t]*\]")
#  case-SENSITIVE, like is_held() -- they disagreed until the #534 F2 pass (codex); the ledger holds
#  zero non-canonical spellings, so this changes no real reading


MALFORMED = "?malformed-hold"
POLICY_CUTOFF = "2026-08-16"   # full panel on every stage; work before it is not judged by it


def held_seats(e):
    """The seats a HELD entry names, in order, or [] if it names none in the strict shape."""
    m = HELD_SEATS.search(_note(e))
    return [x.strip().lower() for x in m.group(1).split(",")] if m else []


def live_holds(entries):
    """Seats still awaited in one (row, phase): named by a HELD entry and NOT answered by that seat
    in this stage at a STRICTLY LATER date -- the carrier's discharge rule, applied here so every
    reader agrees on it.  (#534 pass 2, codex + Opus: two of the three stages that showed a full count
    over a hold were DISCHARGED holds, and one was live; a reader must tell them apart.)"""
    out = []
    for h in entries:
        if not is_held(h):
            continue
        hd = h.get("date") or ""
        named = held_seats(h)
        if not named:
            #  a hold in no parseable shape can never be discharged by an answer -- it holds until
            #  someone writes it properly; a malformed marker must not read as "nothing owed"
            #  (codex, #534 F2 pass: `[HELD AWAITING SEAT: glm,]` let a closed row pass H and I)
            if MALFORMED not in out:
                out.append(MALFORMED)
            continue
        for seat in named:
            done = any((e.get("seat") or "").lower() == seat and is_answer(e)
                       and (e.get("date") or "") > hd for e in entries)
            if not done and seat not in out:
                out.append(seat)
    return out


def stage_token_problems(entries):
    """Why a stage's exemption must be REFUSED, or [] if it stands.  `entries' = one (row, phase).

    (i)  STRICTLY LATER -- EVERY exemption token: a tallied answer dated after the newest exemption
         entry.  An exemption is a claim about the stage AS IT STOOD; material recorded afterwards is
         new, and nothing about a token's vintage makes it cover the future (#534 pass 2: codex, Opus,
         deepseek, minimax, kimi all refused the NOPANEL-only scope; Opus measured that clause (i) was
         never the part that refused the legacy stages).
    (ii) UNCITED PANEL -- NOPANEL ONLY: a tallied answer cites a panel dir that no exemption entry
         names.  This clause IS the retroactive one: annotations and re-reads were written before an
         exemption had to name its panels, and applying it to them refused seven legacy stages for a
         requirement nobody owed at the time.  (A stage whose answers cite no panel dir passes it --
         Opus fixture G, a DISCLOSED escape.)

    Brief-TITLE matching is deliberately absent: a correlate that missed BOTH real disputed cases
    (fable5, #532 pass 2, R4)."""
    tok = [e for e in entries if exempts_stage(e)]
    if not tok:
        return []
    newest_tok = max((e.get("date") or "") for e in tok)
    nop = [e for e in tok if NOPANEL in _note(e)]
    cited = set()
    for e in nop:
        cited |= set(PANEL_DIR.findall(_note(e) + " " + (e.get("ev") or "")))
    out = []
    for e in entries:
        if not is_answer(e) or e in tok:
            continue
        d = e.get("date") or ""
        #  a later answer that itself PREDATES the full-panel directive is not judged by it: the
        #  pre-policy stage it joined was grandfathered, and stays so (kimi, #534 F2 pass)
        if d > newest_tok and d >= POLICY_CUTOFF:
            out.append("answer by %s dated %s is LATER than the exemption (%s)"
                       % (e.get("seat"), d, newest_tok))
        if nop:
            for p in PANEL_DIR.findall(e.get("ev") or ""):
                if p not in cited:
                    out.append("answer by %s cites %s, which the exemption does not name"
                               % (e.get("seat"), p))
    return out


_CORES = {HELD: ("HELD AWAITING SEAT",), ANNOTATION: ("PRE-2026-08-16 POLICY", "RUN UNDER THE PRE"),
          RE_READ: ("SINGLE-SEAT RE-READ",), NOPANEL: ("NO PANEL CONVENED",),
          NOTSEAT: ("NOT A SEAT ANSWER",)}


def literal_offenders(paths):
    """(path, line, token) for every CODE string constant outside this module that spells a token.

    The control fable5 required with R5: the literals live here or nowhere.  Docstrings and comments
    are exempt -- they DESCRIBE tokens, and a prose mention never classified an entry.  An AST walk,
    not a grep, because a grep cannot tell a docstring from a constant and would either flag every
    history paragraph or be loosened until it flagged nothing."""
    import ast
    out = []
    for p in paths:
        src = open(p, encoding="utf-8").read()
        tree = ast.parse(src, p)
        docs = set()
        for n in ast.walk(tree):
            if isinstance(n, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                b = getattr(n, "body", None)
                if b and isinstance(b[0], ast.Expr) and isinstance(b[0].value, ast.Constant):
                    docs.add(id(b[0].value))
        def fold(n):
            """a string built by explicit `+' of constants, folded -- or None"""
            if isinstance(n, ast.Constant) and isinstance(n.value, str):
                return n.value
            if isinstance(n, ast.BinOp) and isinstance(n.op, ast.Add):
                a, b = fold(n.left), fold(n.right)
                return a + b if a is not None and b is not None else None
            return None
        for n in ast.walk(tree):
            if isinstance(n, ast.BinOp) and isinstance(n.op, ast.Add):
                v = fold(n)
                hit = [t for t in ALL if v is not None and any(c in v for c in _CORES[t])]
                if hit:
                    #  #534 F2 pass (kimi, minimax, deepseek): "NOT A SEAT " + "ANSWER]" escaped the
                    #  per-constant match; fold the concatenation and test the whole
                    out.append((p, n.lineno, hit[0]))
                continue
            if isinstance(n, ast.Constant) and isinstance(n.value, str) and id(n) not in docs:
                for t in ALL:
                    #  Matched on the token's CORE PHRASE, brackets and punctuation stripped: a
                    #  fragment like "PRE-2026-08-16 POLICY" or "HELD AWAITING SEAT" classifies just
                    #  as well as the whole literal, and a whole-literal match missed it (Opus, #534
                    #  pass 2: `or "PRE-2026-08-16 POLICY" in note' passed this check).
                    if any(c in n.value for c in _CORES[t]):
                        out.append((p, n.lineno, t))
                        break
    return out


if __name__ == "__main__":
    import glob
    import os
    import sys
    if sys.argv[1:2] == ["--census"]:
        #  fable5 F2 (#534): #532 stated this population three ways ("nine", "eleven of twelve",
        #  and the true 17 stages / 23 entries) because each was counted by hand.  This is the one
        #  deriver: per token, ENTRIES and distinct (row, phase) STAGES -- two units, both named.
        import io
        import json
        led = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "ledger.json")
        rows = json.load(io.open(led, encoding="utf-8"))["rows"]
        names = {HELD: "HELD", ANNOTATION: "ANNOTATION", RE_READ: "RE_READ",
                 NOPANEL: "NOPANEL", NOTSEAT: "NOTSEAT"}
        for t in ALL:
            n_ent, stages = 0, set()
            for r in rows:
                for e in r.get("entries", []):
                    if t in _note(e):
                        n_ent += 1
                        stages.add((r["id"], e.get("phase")))
            print("%-10s %4d entries  %4d stages" % (names[t], n_ent, len(stages)))
        print("STAGE_TOKEN_CENSUS  ledger=%s" % led)
        sys.exit(0)
    if sys.argv[1:2] != ["--selfcheck"]:
        print("usage: stage_tokens.py --selfcheck [files...] | --census [ledger.json]")
        sys.exit(2)
    here = os.path.dirname(os.path.abspath(__file__))
    files = sys.argv[2:] or [f for f in sorted(glob.glob(os.path.join(here, "*.py")))
                             if os.path.basename(f) != "stage_tokens.py"]
    bad = literal_offenders(files)
    for p, ln, t in bad:
        print("  %s:%d spells %s -- import it from stage_tokens.py" % (os.path.basename(p), ln, t))
    print("STAGE_TOKENS_%s  %d file(s) scanned, %d literal(s) outside stage_tokens.py"
          % ("FAIL" if bad else "PASS", len(files), len(bad)))
    sys.exit(1 if bad else 0)
