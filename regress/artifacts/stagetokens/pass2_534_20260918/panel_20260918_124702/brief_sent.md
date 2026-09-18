# `stagetokens` (#534) — ADJUDICATION PASS (§F2) on pass 2, and PASS 2 ON THE REPAIR it produced

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY
Tree under review: `GXEMUL-SEC/tools/pipeline/` (harness only).  Everything needed is inlined.  **VERDICT LINE FIRST**
(RATIFY / RATIFY-WITH-FINDINGS / DO NOT RATIFY).  Nothing is committed.  **You are now seeing all nine seats' findings
at once.  Where a finding is YOURS, be HARDER on it -- and check that my FIX is right, not only that your finding was.**

## 0. SETTLED (unchanged from pass 2; re-inlined)
ledger rows -> entries {seat, phase, date, note, ev}; a (row, phase) is a STAGE; nine seats.  Section H: every
post-2026-08-16 started stage has nine answering seats unless HELD, a one-seat filing, or EXEMPT.  Section I: a stage
run with >= 2 seats and no fable5 must be HELD and queued unless exempt.  Tokens: HELD `[HELD AWAITING SEAT: a, b]`;
ANNOTATION (pre-policy); RE_READ (single-seat re-read: an answer AND an exemption); NOPANEL (no panel convened);
NOTSEAT `[NOT A SEAT ANSWER]` (this entry only; exempts nothing).  Owner decision: pcc2c040assertrow REOPEN AND HOLD.

## 1. FINDINGS AND MY DISPOSITIONS (pass 2 = panel_20260918_122908 + Opus seat)
F1 [codex, grok, agy, kimi, Opus; independent] Deleting RE_READ from STAGE_EXEMPT passed all 16 controls: `t_reread`
   was a one-seat filing and never reached the exemption test.  ACCEPTED -> fixture `t_reread2` (codex filing + grok
   re-read, post-cutoff) + mutant M_reread_not_exempt (killed).
F2 [grok, Opus] Deleting ANNOTATION passed: `t_annot` is pre-cutoff, grandfathered by date first.  ACCEPTED ->
   `t_annot2` post-cutoff + M_annot_not_exempt (killed).
F3 [codex] `HELD in n` -> `HELD == n` in is_answer passed 16/16 + H2.  ACCEPTED -> `t_heldelse` (a HELD entry filed
   under a seat with no answer must render that seat as a record, not an answer) + M_held_is_answer (killed).
F4 [deepseek, agy, Opus] Dropping `not is_held` from exempts_stage passed (no entry carried both).  ACCEPTED ->
   `t_heldnop` + M_held_exempts (killed via section I: the stage must stay held-and-unqueued).
F5 [Opus] max->min, `>` -> `>=`, `findall()[:1]` in the guard all passed.  ACCEPTED -> `t_twonop`, `t_sameday`,
   `t_twopanel`; all three mutants killed.
F6 [codex, Opus, deepseek, minimax, agy, glm; six seats] `heldmasked` must NOT be filed: H counted seats before looking
   for a hold, so the owner's hold reported ok 9/9 and (Opus, MEASURED) the row could be CLOSED with H, I and the wall
   green.  ACCEPTED AS L3 -> `stage_tokens.live_holds()` (a named seat not answered in this stage at a STRICTLY LATER
   date); H tests a live hold BEFORE the count.  REFINED per codex + Opus: of "three" such stages only one hold was
   live; two were discharged, so nothing closed newly reds.  Rows: t_fullhold, t_fullclosed, t_discharged,
   t_samedayhold; mutants M_count_beats_hold, M_discharge_ge (killed).
F7 [Opus, codex] R1 was FALSE on the real ledger: cells classified by `d`, no real HELD entry has the hold glyph, so
   all 25 real held cells rendered as seat failures.  Holds rendered only in the column they were FILED under.
   ACCEPTED -> holds render from live_holds in EVERY awaited seat's column; answers chosen latest-by-date, not
   list-last.  Mutants M_dash_hold_by_d, M_held_blanked (killed).
F8 [codex, Opus, deepseek, minimax, kimi, agy] R4 scoped NOPANEL-only is a hole.  REFINED per Opus's measurement: clause
   (i) later-answer now binds EVERY exemption token; clause (ii) uncited-panel stays NOPANEL-only because only (ii) is
   retroactive.  One real stage then refused -- n6 assess, a 2026-08-30 single-seat reading adjudication after a
   2026-08-16 annotation -- and I TAGGED it RE_READ (its own text: a READING seat, nothing built or run).
F9 [minimax] NOTSEAT + an exemption token in one entry still exempted, against the docstring.  ACCEPTED -> NOTSEAT and
   HELD both dominate; `t_notseatnop`; M_notseat_not_dominant (killed).  The old M_notseat_exempts became EQUIVALENT
   and was RETIRED (33/33) -- recorded as a result.
F10 [kimi] the dashboard showed a REFUSED exemption as a calm empty-set glyph.  ACCEPTED -> tooltip prefixed "EXEMPTION
   REFUSED BY SECTION H"; M_dash_hides_refusal (killed).
F11 [deepseek] tooltip showed only the LAST record note.  ACCEPTED -> all record notes shown.
F12 [Opus] H2 missed a partial literal ("PRE-2026-08-16 POLICY").  ACCEPTED -> matched on each token's core phrase;
   M_partial_literal (killed by the SELFCHECK leg).  [kimi] explicit `+` concatenation across two constants still
   escapes: DISCLOSED, not fixed.
F13 [Opus] the controls never ran gen_codex_wall.  ACCEPTED -> GXLEDGER/GXQUEUE overrides; wall leg; M_wall_notseat
   (killed).  The wall now uses `st.HELD_SEATS`, the same parser as live_holds.
F14 [Opus, codex] check_fix_seats.py (the 4th consumer, the one #532 measured) has NO control.  DISPOSITION: it is
   another round's UNTRACKED draft that does not ship in #534; it imports st.is_answer; its control is OWED WHEN IT SHIPS.
F15 [me, found while repairing] the control driver scored a mutant whose find-text was MISSING as "killed".  FIXED
   (now scored WRONG); negative-controlled.
F16 [kimi] HELD-beats-exemption is a behaviour flip from the pre-#534 readers.  ACCEPTED as a record (CHANGELOG line).

Controls now: **base 33/33; 18 mutants, all killed.**  Real ledger: H PASS, I PASS, H2 PASS, wall regenerates.

## 2. DISAGREEMENTS
D1 deepseek on asiceventaddr.  deepseek seat: "absent a rule making a thinking burn a non-answer, holding deepseek is
   overreach: the ledger already records an answer from that seat."  minimax: "under-justified".  codex, Opus, agy,
   glm: correct -- the file is `response: ""`, `done_reason: "length"`, `eval_count: 65536`.  MY RULING: HOLD STANDS --
   the file carries no answer, and the ledger records NO deepseek entry on that stage (checked).  deepseek, minimax:
   does that fact change your reading?
D2 kimi: filing heldmasked was "defensible" because the dashboard also carries the hold.  Six seats: L3.  MY RULING: L3
   -- and F7 showed the dashboard did NOT carry it (the cell rendered as a seat failure).  kimi: does that settle it?

## 3. OWED, AND WHERE I MIGHT BE FOOLING MYSELF
* I accepted 14 of 16 findings outright.  That is a suspicious number.
* F8's tag of n6 as RE_READ is a records judgement by the author of the rule that refused it.
* live_holds requires a STRICTLY LATER answer, so a seat re-fired and answering the SAME DAY as a hold cannot discharge
  it.  That follows the carrier's rule (six same-day mis-clears on 2026-08-30), but it means pcc2c040assertrow's re-fire
  must be recorded on a date later than 2026-09-18.
* Fable5's pass on #534 is still owed and fires last.

## 4. QUESTIONS
Q1 Adjudicate F1..F16 and D1..D2: UPHOLD / OVERTURN / REFINE / CANNOT SETTLE, one line each.
Q2 WHICH OF MY ACCEPTED DISPOSITIONS IS WRONG?
Q3 (FLOOR, on the repaired composite): the smallest edit to stage_tokens.py or a reader that mis-classifies and still
   passes all 33 expectations + H2.  Name the fixture row that would have to change.
Q4 What did all nine of us miss?

## 5. stage_tokens.py IN FULL (new, untracked)
```python
"""THE ONE PLACE A LEDGER STAGE TOKEN IS SPELLED OR CLASSIFIED.  #534, 2026-09-18.

WHY THIS FILE EXISTS.  Four tools read ledger entries and each carried its own copy of the tokens:
check_stage_panels.py knew four, check_fable_queue.py was never taught RE_READ, gen_dashboard.py
filtered HELD markers it had no business filtering, and check_fix_seats.py knew only HELD -- so it
credited a stage-exemption entry written under `seat: fable5' as a FLAGSHIP ANSWER, and the row that
introduced the newest token passed its own flagship mandate on that token (#532 pass 2, Opus seat,
MEASURED).  One cause every time: a token added where it was needed and never mirrored.  So the
literals AND the classification live here, and precommit_check.sh refuses a token literal anywhere
else in tools/pipeline/.

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


HELD_SEATS = re.compile(re.escape(HELD) + r"[ \t]*([a-z0-9_]+(?:[ \t]*,[ \t]*[a-z0-9_]+)*)[ \t]*\]", re.I)


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
        for seat in held_seats(h):
            done = any(e.get("seat") == seat and is_answer(e) and (e.get("date") or "") > hd
                       for e in entries)
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
        if d > newest_tok:
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
        for n in ast.walk(tree):
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
```

## 6. READER DIFFS vs HEAD
```diff
diff --git a/tools/pipeline/check_fable_queue.py b/tools/pipeline/check_fable_queue.py
index 890a02f..4a31486 100644
--- a/tools/pipeline/check_fable_queue.py
+++ b/tools/pipeline/check_fable_queue.py
@@ -41,18 +41,11 @@ LEDGER = os.environ.get("GXLEDGER") or os.path.join(HERE, "ledger.json")
 QUEUE = os.environ.get("GXQUEUE") or os.path.join(HERE, "fable_queue.md")
 
 FLAGSHIP = "fable5"
-HELD = "[HELD AWAITING SEAT:"
-ANNOTATION = "[RUN UNDER THE PRE-2026-08-16 POLICY]"
-
-#  *** THESE TWO WERE KNOWN TO check_stage_panels.py AND NOT TO THIS FILE, SO A STAGE COULD PASS
-#  SECTION H AND STILL RED SECTION I ON THE SAME LEDGER ENTRY.  Found 2026-09-18 while adding
-#  NOPANEL, by asking what the OTHER checker does with the same tokens. ***  The two gates are
-#  deliberately non-redundant -- H asks whether the seat was FIRED, I asks whether owed flagship
-#  work is WRITTEN DOWN -- but "this stage is not a panel stage at all" is a fact about the
-#  LEDGER ENTRY, not about either question, so both must honour it or they disagree about what
-#  the entry means.  RE_READ has been in the other file since 2026-08-21 and was never mirrored.
-RE_READ = "[NOT A PANEL STAGE: SINGLE-SEAT RE-READ]"
-NOPANEL = "[NOT A PANEL STAGE: NO PANEL CONVENED]"
+#  #534 (R5): every stage token is spelled and classified ONCE, in stage_tokens.py.  This file used
+#  to carry its own copies, and it was the second of four tools to be blind to a token the others
+#  knew (RE_READ, until 2026-09-18).  The history of that miss is in stage_tokens.py's docstring.
+sys.path.insert(0, HERE)
+import stage_tokens as st  # noqa: E402
 
 #  Directive dates.  Work that predates a directive cannot be judged by it.
 CUTOFF_FULL_PANEL = "2026-08-16"   # full panel on every stage
@@ -111,13 +104,17 @@ def main(argv):
             phases_seen.add(ph)
             note = ent.get("note", "")
             d = stages.setdefault(ph, {"seats": set(), "newest": "", "held": False,
-                                       "annotated": False})
-            if ANNOTATION in note or RE_READ in note or NOPANEL in note:
+                                       "annotated": False, "all": []})
+            d["all"].append(ent)
+            #  #534: exempting the stage and being an answer are INDEPENDENT (a single-seat
+            #  re-read is both), so they are asked separately -- never as one if/continue.
+            if st.exempts_stage(ent):
                 d["annotated"] = True
-                continue
-            if HELD in note:
+            if st.is_held(ent):
                 d["held"] = True
                 continue
+            if not st.is_answer(ent):
+                continue
             d["seats"].add(ent.get("seat"))
             d["newest"] = max(d["newest"], ent.get("date", ""))
 
@@ -126,7 +123,11 @@ def main(argv):
                 continue          # flagship-only by directive; rule 3 covers its absence
             if len(d["seats"]) < 2:
                 continue          # a one-seat stage is a FILING, not a stage that ran
-            if FLAGSHIP in d["seats"] or d["annotated"]:
+            if FLAGSHIP in d["seats"]:
+                continue
+            #  #534 (R4): an exemption that a later answer or an uncited panel contradicts does not
+            #  exempt -- the same refusal check_stage_panels.py applies, from the same function.
+            if d["annotated"] and not st.stage_token_problems(d["all"]):
                 continue
             if d["newest"] < CUTOFF_FULL_PANEL:
                 continue          # predates the directive
diff --git a/tools/pipeline/check_stage_panels.py b/tools/pipeline/check_stage_panels.py
index 5d532dc..d9b18ab 100644
--- a/tools/pipeline/check_stage_panels.py
+++ b/tools/pipeline/check_stage_panels.py
@@ -26,6 +26,9 @@ import json
 import os
 import sys
 
+sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
+import stage_tokens as st   # #534: the ONE place a token is spelled or classified
+
 HERE = os.path.dirname(os.path.abspath(__file__))
 #  Overridable so controls run against COPIES.  Added 2026-08-17 after a negative control
 #  for the CLOSED-WHILE-HELD clause silently tested NOTHING: it wrote a mutated ledger to a
@@ -63,7 +66,7 @@ STAGES = ("assess", "research", "review")
 
 #  An annotation entry is not a review.  It exists to say WHY a stage is short, and it must
 #  not be counted as one of the seats that answered -- otherwise marking a gap would close it.
-ANNOTATION = "[RUN UNDER THE PRE-2026-08-16 POLICY]"
+ANNOTATION = st.ANNOTATION      # #534: spelled once, in stage_tokens.py
 
 #  A SECOND, DIFFERENT EXEMPTION, and it is deliberately not folded into the first.
 #
@@ -80,7 +83,7 @@ ANNOTATION = "[RUN UNDER THE PRE-2026-08-16 POLICY]"
 #
 #  This is a real recurring category rather than a one-off: any pass that sweeps filed rows can
 #  promote a filing into a short stage without anyone deciding to.
-RE_READ = "[NOT A PANEL STAGE: SINGLE-SEAT RE-READ]"
+RE_READ = st.RE_READ      # #534: spelled once, in stage_tokens.py
 
 #  A THIRD EXEMPTION, 2026-09-18, and like the second it exists because neither older token was
 #  TRUE of the situation -- which is the only reason this file ever gains a token.
@@ -123,7 +126,7 @@ RE_READ = "[NOT A PANEL STAGE: SINGLE-SEAT RE-READ]"
 #  ship-order ADJUDICATION -- real work on that very row, and not a panel seat answer at all.
 #  The checkable claim both gates need is only ever "no panel was convened on this stage";
 #  everything else is provenance, and provenance belongs in prose a reader can check.**
-NOPANEL = "[NOT A PANEL STAGE: NO PANEL CONVENED]"
+NOPANEL = st.NOPANEL      # #534: spelled once, in stage_tokens.py
 
 #  *** A STAGE DELIBERATELY HELD FOR A NAMED SEAT IS NOT A STAGE THAT MOVED ON. ***
 #
@@ -141,7 +144,7 @@ NOPANEL = "[NOT A PANEL STAGE: NO PANEL CONVENED]"
 #  row is a HARD violation.  You may wait for a seat; you may not close a round while waiting
 #  for one.  Without that clause "HELD" would be a way to mark any gap and walk away, which is
 #  worse than the conflation it replaces.
-HELD = "[HELD AWAITING SEAT:"
+HELD = st.HELD      # #534: spelled once, in stage_tokens.py
 
 
 def main(argv):
@@ -162,11 +165,10 @@ def main(argv):
     for row in ledger["rows"]:
         by_stage = {}
         for ent in row.get("entries", []):
-            if (ANNOTATION in ent.get("note", "") or RE_READ in ent.get("note", "")
-                    or NOPANEL in ent.get("note", "")):
-                by_stage.setdefault(ent.get("phase"), {})["_annotated"] = True
-                continue
-            if HELD in ent.get("note", ""):
+            by_stage.setdefault(ent.get("phase"), {}).setdefault("_all", []).append(ent)
+            if st.exempts_stage(ent):
+                by_stage[ent.get("phase")]["_annotated"] = True
+            if st.is_held(ent):
                 d = by_stage.setdefault(ent.get("phase"), {})
                 #  A LIST, NOT A SLOT.  This assigned a single value until 2026-08-17, so a
                 #  stage held for TWO seats kept only the LAST marker and reported one.
@@ -179,6 +181,8 @@ def main(argv):
                 #  seat early, and the missing seat's blank then reads as agreement.
                 d.setdefault("_held", []).append(ent.get("note", ""))
                 continue
+            if not st.is_answer(ent):
+                continue           # ANNOTATION / NOPANEL / NOTSEAT entries are not seat answers
             d = by_stage.setdefault(ent.get("phase"), {})
             d.setdefault("seats", set()).add(ent.get("seat"))
             d["newest"] = max(d.get("newest", ""), ent.get("date", ""))
@@ -188,7 +192,13 @@ def main(argv):
             if not info or "seats" not in info:
                 continue                       # stage never ran; not this check's business
             got, newest = info["seats"], info.get("newest", "")
-            if len(got) >= n_seats:
+            #  #534 (heldmasked, an L3 of this round per its pass 2): a LIVE hold -- a named seat not
+            #  answered in this stage at a strictly later date -- beats a full count.  Before this,
+            #  the count test ran first, so an owner-decision hold over nine misdirected answers
+            #  reported `ok 9/9` and the row could be CLOSED with H, I and the wall all green
+            #  (Opus, measured).  A DISCHARGED marker does not hold a full stage.
+            live = st.live_holds(info.get("_all", []))
+            if len(got) >= n_seats and not live:
                 complete += 1
                 if listing:
                     print("  ok    %-14s %-9s %d/%d" % (row["id"], stage, len(got), n_seats))
@@ -203,17 +213,25 @@ def main(argv):
                 else:
                     #  Every marker, de-duplicated, order preserved -- so two holds report
                     #  two seats and the operator sees the whole debt.
-                    names = []
-                    for mark in info["_held"]:
-                        nm = mark.split(HELD, 1)[1].split("]", 1)[0].strip()
-                        if nm and nm not in names:
-                            names.append(nm)
+                    names = list(live)
+                    if not names:
+                        for mark in info["_held"]:
+                            nm = mark.split(HELD, 1)[1].split("]", 1)[0].strip()
+                            if nm and nm not in names:
+                                names.append(nm)
                     held.append((row["id"], stage, len(got), ", ".join(names),
                                      newest, (row.get("hold_question") or "").strip()))
                 continue
             if len(got) == 1:
                 filed.append((row["id"], stage))
                 continue
+            if info.get("_annotated"):
+                #  #534: an exemption is REFUSED when a later answer or an uncited panel shows it
+                #  does not describe the stage as it now stands (stage_tokens.stage_token_problems).
+                probs = st.stage_token_problems(info.get("_all", []))
+                if probs:
+                    violations.append((row["id"], "TOKEN-REFUSED", stage, len(got), probs))
+                    continue
             if newest < CUTOFF or info.get("_annotated"):
                 grandfathered += 1
                 if listing:
diff --git a/tools/pipeline/gen_codex_wall.py b/tools/pipeline/gen_codex_wall.py
index 6b1b1e7..27acb74 100644
--- a/tools/pipeline/gen_codex_wall.py
+++ b/tools/pipeline/gen_codex_wall.py
@@ -30,8 +30,9 @@ import re
 import sys
 
 HERE = os.path.dirname(os.path.abspath(__file__))
-LEDGER = os.path.join(HERE, "ledger.json")
-QUEUE = os.path.join(HERE, "fable_queue.md")
+#  GXLEDGER / GXQUEUE (#534): the stage-token controls run this against a FIXTURE, as they do the checkers.
+LEDGER = os.environ.get("GXLEDGER") or os.path.join(HERE, "ledger.json")
+QUEUE = os.environ.get("GXQUEUE") or os.path.join(HERE, "fable_queue.md")
 
 BEGIN = "<!-- BEGIN GENERATED: codex-wall -- edit gen_codex_wall.py, not this block -->"
 END = "<!-- END GENERATED: codex-wall -->"
@@ -67,9 +68,12 @@ END = "<!-- END GENERATED: codex-wall -->"
 #  KNOWN AND ACCEPTED LIMIT: a real marker WRAPPED ACROSS LINES stays invisible.  Newlines
 #  are excluded deliberately -- admitting them re-opens the phantom surface -- so the
 #  generator requires markers to be written on one line, which is how they are generated.
-MARKER = re.compile(
-    r"\[HELD AWAITING SEAT:[ \t]*([a-z0-9_]+(?:[ \t]*,[ \t]*[a-z0-9_]+)*)[ \t]*\]",
-    re.I)
+#  #534 (R5): the literal AND the strict seat-list shape come from stage_tokens.py, which the
+#  live-hold rule in check_stage_panels.py also parses with -- one parser, so the two cannot
+#  disagree about which seats a marker names.
+sys.path.insert(0, HERE)
+import stage_tokens as st  # noqa: E402
+MARKER = st.HELD_SEATS
 
 PROSE = """
 *** TWO DIFFERENT KINDS OF HOLD APPEAR BELOW AND THEY MUST NOT BE READ ALIKE. ***
diff --git a/tools/pipeline/gen_dashboard.py b/tools/pipeline/gen_dashboard.py
index a40eca5..8bc736c 100644
--- a/tools/pipeline/gen_dashboard.py
+++ b/tools/pipeline/gen_dashboard.py
@@ -25,7 +25,9 @@ import os
 import sys
 
 HERE = os.path.dirname(os.path.abspath(__file__))
-LEDGER = os.path.join(HERE, "ledger.json")
+#  GXLEDGER (#534): the render leg of the stage-token controls feeds a FIXTURE ledger, the same
+#  override check_stage_panels.py and check_fable_queue.py already take.
+LEDGER = os.environ.get("GXLEDGER") or os.path.join(HERE, "ledger.json")
 #  `--out PATH` renders somewhere else WITHOUT touching the tracked file, so precommit
 #  section Q can regenerate into a temp path and cmp.  Added when it turned out NOTHING
 #  checked that matrix.html was current with ledger.json -- and the published artifact is
@@ -99,23 +101,62 @@ STATE_ORDER = {"active": 0, "held": 1, "pending": 2, "closed": 9, "dropped": 10}
 #  Found 2026-09-18 by asking what the OTHER tools do with a token this file does not know -- the
 #  same question that had just found `check_fable_queue.py` blind to RE_READ.  **Two tools, two
 #  blind spots, one cause: a token was added where it was needed and never mirrored.**
-STAGE_TOKENS = ("[RUN UNDER THE PRE-2026-08-16 POLICY]",
-                "[NOT A PANEL STAGE: SINGLE-SEAT RE-READ]",
-                "[NOT A PANEL STAGE: NO PANEL CONVENED]",
-                "[HELD AWAITING SEAT:")
+#  *** CORRECTED 2026-09-18 (#534 F3): the paragraph above says the dashboard "asserted that the
+#  flagship seat had answered" a stage no panel was convened on.  MEASURED FALSE by fable5 on #532
+#  pass 2: before #532, zero token cells rendered as agreement (1415 ok cells before and after) --
+#  ANNOTATION rendered as a held glyph, NOPANEL as the seat-failure glyph, HELD as its own `d'.  The
+#  finding that survives is narrower: the tool was blind to the tokens, so it rendered them by
+#  accident rather than by rule.  And #532's own fix over-reached the other way: filtering HELD
+#  blanked a real held cell, and filtering ANNOTATION rendered an honest annotation as nothing.
+#
+#  #534: the literals and the classification live in stage_tokens.py (R5).  A HELD entry renders as
+#  itself (R1); an entry that is not an answer renders the distinct glyph below WITH its note as the
+#  tooltip, so an exemption can be read, never mistaken for a blank (R1, ANNOTATION included).
+sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
+import stage_tokens as st  # noqa: E402
+
+TOKEN_GLYPH = "∅"   # empty set: this seat's entry here is a record, not an answer
+
+
+def _latest(xs):
+    """Date-latest entry, ties to the later-recorded one -- never simply list-last: an older answer
+    appended after a newer hold must not hide the hold (codex, #534 pass 2)."""
+    return max(enumerate(xs), key=lambda t: ((t[1].get("date") or ""), t[0]))[1]
 
 
-def _is_answer(x):
-    note = x.get("note") or ""
-    return not any(t in note for t in STAGE_TOKENS)
+def _held_cell(h, seat_id):
+    t = e(" — ".join(p for p in (h.get("date"), "awaiting " + seat_id, h.get("note")) if p))
+    return ('<td class="c hold"><span class="wrap" tabindex="0">'
+            f'<span class="g">⏸</span><span class="tip">{t}</span></span></td>')
 
 
 def cell(row, phase, seat):
-    ents = [x for x in row.get("entries", [])
-            if x["seat"] == seat["id"] and x.get("phase") == phase and _is_answer(x)]
+    stage = [x for x in row.get("entries", []) if x.get("phase") == phase]
+    mine = [x for x in stage if x["seat"] == seat["id"]]
+    #  #534 pass 2 (Opus + codex, measured): a hold renders from its SEMANTICS, never from its `d'
+    #  field -- no real HELD entry carries the hold glyph (25 say "HELD", others "--", "N/A", "" or
+    #  nothing), so all of them rendered as `pend', the seat-failure glyph.  And it renders in the
+    #  column of every seat it AWAITS, not only the column it happens to be filed under.
+    if seat["id"] in st.live_holds(stage):
+        return _held_cell(_latest([h for h in stage if seat["id"] in st.held_seats(h)]), seat["id"])
+    ents = [x for x in mine if st.is_answer(x)]
     if not ents:
-        return '<td class="c none"><span class="g">·</span></td>'
-    ent = ents[-1]
+        held = [x for x in mine if st.is_held(x) and not st.held_seats(x)]
+        if held:                         # a marker in no parseable shape: still a hold, never blank
+            return _held_cell(_latest(held), seat["id"])
+        recs = [x for x in mine if not st.is_answer(x)]
+        if not recs:
+            return '<td class="c none"><span class="g">·</span></td>'
+        #  every record's note, not only the last: a later NOTSEAT must not hide an exemption's reason
+        t = " || ".join(" — ".join(p for p in (r.get("date"), r.get("note")) if p) for r in recs)
+        #  a refused exemption must not render as a calm one (kimi, #534 pass 2)
+        refused = st.stage_token_problems(stage) if any(st.exempts_stage(r) for r in recs) else []
+        if refused:
+            t = "EXEMPTION REFUSED BY SECTION H: " + "; ".join(refused) + " || " + t
+        t = e(t)
+        return ('<td class="c tok"><span class="wrap" tabindex="0">'
+                f'<span class="g">{TOKEN_GLYPH}</span><span class="tip">{t}</span></span></td>')
+    ent = _latest(ents)
     d = ent.get("d", "…")
     cls = D_CLASS.get(d, "pend")
     badge = ent.get("b", "")
@@ -319,6 +360,7 @@ tr.ph.st-closed td.c.ok {{ background:color-mix(in srgb, var(--okbg) 55%, var(--
 .c.ok .g {{ color:var(--ok); }} .c.hold .g {{ color:var(--hold); }}
 .c.bad .g {{ color:var(--bad); font-weight:700; }} .c.pend .g {{ color:var(--pend); }}
 .c.none .g {{ color:var(--line); }}
+.c.tok .g {{ color:var(--muted); }}
 .b {{ font-size:9.5px; font-weight:700; margin-left:1px; color:var(--accent);
   border:1px solid var(--accent); border-radius:2px; padding:0 2px; vertical-align:6px; }}
 .b-s {{ color:var(--hold); border-color:var(--hold); }}
@@ -366,6 +408,7 @@ footer code {{ color:var(--ink); }}
   <span><span class="g" style="color:var(--hold)">⏸</span> held / in work</span>
   <span><span class="g" style="color:var(--bad)">✕</span> objection</span>
   <span><span class="g" style="color:var(--pend)">…</span> no answer / seat failure (not agreement)</span>
+  <span><span class="g" style="color:var(--muted)">∅</span> a record, not an answer (exemption or main-loop note; hover for why)</span>
   <span><span class="g" style="color:var(--line)">·</span> no input — input is possible</span>
   <span><sup class="b">A</sup> the author did this review (shown)</span>
   <span><sup class="b b-s">s</sup> a review by the same model family</span>
```

## 7. CONTROL FIXTURE ROWS AND MUTANTS (run_controls.py excerpt)
```python
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
        + [ent("fable5", "review", D1, st.HELD + " glm] old hold", d="HELD")], state="closed"),
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
                    "        if d > newest_tok:",
                    "        if d >= newest_tok:"),
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
                             "        if refused:",
                             "        if False:"),
    "M_fq_ignores_guard": ("check_fable_queue.py",
                           "if d[\"annotated\"] and not st.stage_token_problems(d[\"all\"]):",
                           "if d[\"annotated\"]:"),
}
```


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
