# `stagetokens` (#534) — PASS 2 on the repair of #532.  A repair owes its own pass 2.

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY
A recent panel had seven of nine seats confirm a premise the brief stated wrongly. **Check the premises, not just the
derivations.** The tree under review is `GXEMUL-SEC/tools/pipeline/` (harness only; no `src/` change).  If you cannot
read files that is expected -- everything is inlined.  **VERDICT LINE FIRST** (RATIFY / RATIFY-WITH-FINDINGS / DO NOT
RATIFY).  Nothing here is committed yet.

## 1. WHAT THE TOOLS DO (settled; re-inlined so nobody re-derives it)
* `tools/pipeline/ledger.json` has rows; each row has `entries`, each entry `{seat, phase, date, note, ev}`.  A
  (row, phase) is a STAGE.  Nine seats by design.
* `check_stage_panels.py` (precommit section H): every post-2026-08-16 stage that STARTED must carry nine answering
  seats, unless HELD for named seats, a one-seat filing, or EXEMPT.
* `check_fable_queue.py` (section I): a stage that ran with >= 2 seats and no fable5 answer must be HELD and the row
  named in `fable_queue.md`, unless exempt.
* `gen_dashboard.py` renders the ledger to a matrix; one cell per (row, phase, seat).
* Stage tokens live in a note's text: HELD `[HELD AWAITING SEAT: x, y]`; ANNOTATION (pre-2026-08-16 policy);
  RE_READ (a single-seat re-read: IS an answer AND exempts the stage); NOPANEL (no panel was convened on this stage);
  and new here NOTSEAT `[NOT A SEAT ANSWER]` (this ENTRY is a main-loop record; exempts nothing).

## 2. SETTLED BY #532'S PASS 2 (fable5 adjudication, adopted; owner decision on R3)
* R5: one module holds literals + classifier; no token literal elsewhere; controls on CLASSIFICATION per token x tool
  plus a RENDER leg (codex: a RE_READ-not-an-answer mutant passes every exit-status control).
* R2: entry-scoped NOTSEAT; convert entries that only meant "not a seat answer".
* R4: guard (i) an answer STRICTLY LATER than the exemption refuses it; (ii) an answer citing a panel dir the
  exemption does not name refuses it.  Brief-title matching REJECTED (a correlate).
* R1: HELD renders as itself; exemption/non-answer tokens get a distinct glyph WITH the note as tooltip.
* F1: asiceventaddr's NOPANEL was FALSE (its panel was pass 2 on its own commit) -> HELD.  R3: pcc2c040assertrow's
  NOPANEL was FALSE; the OWNER chose REOPEN AND HOLD its four packet-fed seats (fable had recommended filing).
* F3: #532's claim that the dashboard "asserted the flagship had answered" is MEASURED FALSE (1,415 ok cells before
  and after); corrected in place.

## 3. MEASURED (logs in regress/artifacts/stagetokens/controls_534/)
* `run_controls.py`: copies tools/pipeline/*.py to a temp dir, feeds a 7-row fixture ledger, runs the three readers.
  **base 16/16 green**; mutants, each must red >= 1:
    M_reread_not_answer 15/16 (red: DASH re-read renders answer)      -- the codex mutant, killed ONLY by the render leg
    M_notseat_exempts   14/16 (red: CSP t_notseat incomplete, FQ t_notseat short)
    M_no_guard          13/16 (red: CSP t_late, CSP t_uncited REFUSED, FQ t_late short)
    M_held_blanked      15/16 (red: DASH held renders held)
    M_fq_ignores_guard  15/16 (red: FQ t_late short)
* H2 literal check (`stage_tokens.py --selfcheck`, AST walk, docstrings exempt): PASS on the tree (25 files); FAIL on
  each of the four HEAD copies of the readers (4/4/1/4 literals); PASS on a docstring+comment-only fixture.
* Real ledger after the repair: H `STAGE_PANELS_PASS` (244 complete, 16 HELD, 0 incomplete); I `FABLE_QUEUE_PASS`.
* Census (`stage_tokens.py --census`): NOPANEL stages 0 at 686d179~1, 13 at 686d179, 9 now.

## 4. PREMISES I AM NOT SURE OF -- CHECK THEM, DO NOT RATIFY THEM
* P1. I restricted guard R4 to NOPANEL only, because applying it to ANNOTATION refused six legacy (pre-policy) stages.
  Is that a principled scope or a hole?  (RE_READ is also unguarded.)
* P2. asiceventaddr: fable's F1 named HELD fable5, opus5.  I ALSO held deepseek, whose answer in that panel is a
  142 KB thinking burn.  Right or overreach?
* P3. FOUND AND FILED, NOT FIXED: section H tests `len(got) >= n_seats` BEFORE the HELD test, so a stage with nine
  answers AND a live hold reports ok 9/9 -- pcc2c040assertrow's owner-decision hold is invisible to H.  Three such
  stages today, one on a CLOSED row that a reorder would newly red.  Is filing (`heldmasked`) right, or is it an L3
  obligation of THIS round because the owner decision's only mechanical carrier is H?
* P4. gen_dashboard: a cell whose seat has BOTH a non-answer token entry and no answer shows the LAST token entry's
  note.  A HELD entry wins over tokens.  Is there a cell state that now renders misleadingly?

## 5. QUESTIONS
Q1 (FLOOR, asked of the composite): name the smallest edit to stage_tokens.py or any reader in the diff below that
   MIS-CLASSIFIES an entry and still passes all 16 controls and H2.  Say which fixture row would have to change.
Q2: Answer P1-P4.
Q3: WHICH OF MY DISPOSITIONS IS WRONG?  (There are about seven: R1-R5, F1 incl. deepseek, R3 hold, heldmasked filed.)

## 6. THE NEW MODULE, IN FULL (tools/pipeline/stage_tokens.py, untracked, new)
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
    return (not is_held(e)) and any(t in n for t in STAGE_EXEMPT)


def is_answer(e):
    n = _note(e)
    if HELD in n or NOTSEAT in n or ANNOTATION in n or NOPANEL in n:
        return False
    return True          # RE_READ entries ARE answers; so is every untokened entry


def stage_token_problems(entries):
    """Why a stage's exemption must be REFUSED, or [] if it stands.  `entries' = one (row, phase).

    (i)  STRICTLY LATER: a tallied answer dated after the newest exemption entry.  An exemption is a
         claim about the stage AS IT STOOD; a panel recorded afterwards is new material the token
         never saw (Opus fixture C: a token planted during filing silently covered a real short
         panel that landed two days later).  Same shape as the HELD strictly-later rule.
    (ii) UNCITED PANEL: a tallied answer cites a panel dir that no exemption entry names.  An
         exemption must name the panels it is exempting, so an exempted stage can always be checked
         against its briefs by a reader.  (A stage whose answers cite no panel dir passes this
         clause -- that is Opus's fixture G, a DISCLOSED escape: nothing in the ledger says which
         panel such answers came from, so there is nothing to compare.)

    The rejected alternative, reading each brief's TITLE for the row id, is deliberately absent: it
    is a correlate that missed BOTH real disputed cases (fable5, #532 pass 2, R4)."""
    #  ONLY NOPANEL is guarded.  ANNOTATION asserts a historical policy vintage (pre-2026-08-16) and
    #  predates this guard; applying the rule to it refused six legacy stages whose annotations were
    #  written before exemptions had to name their panels -- a retroactive requirement nobody owed.
    tok = [e for e in entries if NOPANEL in _note(e) and not is_held(e)]
    if not tok:
        return []
    newest_tok = max((e.get("date") or "") for e in tok)
    cited = set()
    for e in tok:
        cited |= set(PANEL_DIR.findall(_note(e) + " " + (e.get("ev") or "")))
    out = []
    for e in entries:
        if not is_answer(e):
            continue
        d = e.get("date") or ""
        if d > newest_tok:
            out.append("answer by %s dated %s is LATER than the exemption (%s)"
                       % (e.get("seat"), d, newest_tok))
        for p in PANEL_DIR.findall(e.get("ev") or ""):
            if p not in cited:
                out.append("answer by %s cites %s, which the exemption does not name"
                           % (e.get("seat"), p))
    return out


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
                    #  the HELD literal is also matched without its bracket, which is how the
                    #  pre-#534 check_fix_seats.py spelled it
                    if t in n.value or (t is HELD and "HELD AWAITING SEAT" in n.value):
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

## 7. THE DIFF TO THE READERS AND precommit (git diff, working tree vs HEAD; precommit shows only its #534 hunk)
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
index 5d532dc..2923b36 100644
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
@@ -214,6 +218,13 @@ def main(argv):
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
index 6b1b1e7..b81d9c4 100644
--- a/tools/pipeline/gen_codex_wall.py
+++ b/tools/pipeline/gen_codex_wall.py
@@ -67,8 +67,11 @@ END = "<!-- END GENERATED: codex-wall -->"
 #  KNOWN AND ACCEPTED LIMIT: a real marker WRAPPED ACROSS LINES stays invisible.  Newlines
 #  are excluded deliberately -- admitting them re-opens the phantom surface -- so the
 #  generator requires markers to be written on one line, which is how they are generated.
+#  #534 (R5): the literal comes from stage_tokens.py; only the strict seat-list SHAPE lives here.
+sys.path.insert(0, HERE)
+import stage_tokens as st  # noqa: E402
 MARKER = re.compile(
-    r"\[HELD AWAITING SEAT:[ \t]*([a-z0-9_]+(?:[ \t]*,[ \t]*[a-z0-9_]+)*)[ \t]*\]",
+    re.escape(st.HELD) + r"[ \t]*([a-z0-9_]+(?:[ \t]*,[ \t]*[a-z0-9_]+)*)[ \t]*\]",
     re.I)
 
 PROSE = """
diff --git a/tools/pipeline/gen_dashboard.py b/tools/pipeline/gen_dashboard.py
index a40eca5..24a283f 100644
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
@@ -99,22 +101,35 @@ STATE_ORDER = {"active": 0, "held": 1, "pending": 2, "closed": 9, "dropped": 10}
 #  Found 2026-09-18 by asking what the OTHER tools do with a token this file does not know -- the
 #  same question that had just found `check_fable_queue.py` blind to RE_READ.  **Two tools, two
 #  blind spots, one cause: a token was added where it was needed and never mirrored.**
-STAGE_TOKENS = ("[RUN UNDER THE PRE-2026-08-16 POLICY]",
-                "[NOT A PANEL STAGE: SINGLE-SEAT RE-READ]",
-                "[NOT A PANEL STAGE: NO PANEL CONVENED]",
-                "[HELD AWAITING SEAT:")
-
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
 
-def _is_answer(x):
-    note = x.get("note") or ""
-    return not any(t in note for t in STAGE_TOKENS)
+TOKEN_GLYPH = "∅"   # empty set: this seat's entry here is a record, not an answer
 
 
 def cell(row, phase, seat):
-    ents = [x for x in row.get("entries", [])
-            if x["seat"] == seat["id"] and x.get("phase") == phase and _is_answer(x)]
+    mine = [x for x in row.get("entries", [])
+            if x["seat"] == seat["id"] and x.get("phase") == phase]
+    ents = [x for x in mine if st.is_answer(x) or st.is_held(x)]
     if not ents:
-        return '<td class="c none"><span class="g">·</span></td>'
+        recs = [x for x in mine if not st.is_answer(x)]
+        if not recs:
+            return '<td class="c none"><span class="g">·</span></td>'
+        r = recs[-1]
+        t = e(" — ".join(p for p in (r.get("date"), r.get("note")) if p))
+        return ('<td class="c tok"><span class="wrap" tabindex="0">'
+                f'<span class="g">{TOKEN_GLYPH}</span><span class="tip">{t}</span></span></td>')
     ent = ents[-1]
     d = ent.get("d", "…")
     cls = D_CLASS.get(d, "pend")
@@ -319,6 +334,7 @@ tr.ph.st-closed td.c.ok {{ background:color-mix(in srgb, var(--okbg) 55%, var(--
 .c.ok .g {{ color:var(--ok); }} .c.hold .g {{ color:var(--hold); }}
 .c.bad .g {{ color:var(--bad); font-weight:700; }} .c.pend .g {{ color:var(--pend); }}
 .c.none .g {{ color:var(--line); }}
+.c.tok .g {{ color:var(--muted); }}
 .b {{ font-size:9.5px; font-weight:700; margin-left:1px; color:var(--accent);
   border:1px solid var(--accent); border-radius:2px; padding:0 2px; vertical-align:6px; }}
 .b-s {{ color:var(--hold); border-color:var(--hold); }}
@@ -366,6 +382,7 @@ footer code {{ color:var(--ink); }}
   <span><span class="g" style="color:var(--hold)">⏸</span> held / in work</span>
   <span><span class="g" style="color:var(--bad)">✕</span> objection</span>
   <span><span class="g" style="color:var(--pend)">…</span> no answer / seat failure (not agreement)</span>
+  <span><span class="g" style="color:var(--muted)">∅</span> a record, not an answer (exemption or main-loop note; hover for why)</span>
   <span><span class="g" style="color:var(--line)">·</span> no input — input is possible</span>
   <span><sup class="b">A</sup> the author did this review (shown)</span>
   <span><sup class="b b-s">s</sup> a review by the same model family</span>
diff --git a/tools/precommit_check.sh b/tools/precommit_check.sh
index 9dae9cf..13c7fef 100644
--- a/tools/precommit_check.sh
+++ b/tools/precommit_check.sh
@@ -840,6 +843,21 @@ else
 ' "$out" | sed 's/^/          /'
 fi
 
+#  H2 (#534, fable5 R5): four tools read ledger stage tokens and each once carried its own copy;
+#  every mis-classification this project measured came from one copy not mirroring another.  The
+#  literals and the classifier now live in stage_tokens.py, and this refuses a token spelled as a
+#  CODE string anywhere else in tools/pipeline/ (docstrings and comments exempt -- they describe).
+say ""; say "H2. stage tokens are spelled in one place"
+TOKCHK=$_HERE/pipeline/stage_tokens.py
+if [ ! -f "$TOKCHK" ]; then
+	bad "stage_tokens.py MISSING -- H, I and the dashboard import it"
+elif out=$(python "$TOKCHK" --selfcheck 2>&1); then
+	good "$(printf '%s' "$out" | tail -1)"
+else
+	bad "A STAGE TOKEN IS SPELLED OUTSIDE stage_tokens.py:"
+	printf '%s\n' "$out" | sed 's/^/          /'
+fi
+
 say ""; say "G. every seat that answered in a cited panel is recorded"
 SEATCHK=$_HERE/pipeline/check_seats_read.py
 if [ ! -f "$SEATCHK" ]; then
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
