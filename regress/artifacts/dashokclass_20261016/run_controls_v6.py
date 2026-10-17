#!/usr/bin/env python3
"""Controls for `dashokclass` (2026-10-17, v6 after the v5 pass): gen_dashboard.py's LEGACY class, check_entry_domain.py (a
ceiling over selected content, md5-pinned baseline) and its precommit section Q2.  Everything runs on temp copies and fixture
ledgers; nothing in the tree is written.  Exit 0 only if every control holds.  CTL_CHECKER / CTL_RENDER / CTL_PRECOMMIT override
the three files under test (run_mutants_v6.py and the staged runs use them); the defaults are the tree's.

  THE CONTRACT (v6) -- the v4 pass found pins that tested ONE edge of a decision, and v5 rowed the dual edge.  The v5 pass
  (GPT-6 Astra and Fable 5.1 measured, GLM 5.3 reasoned, Grok 4.7 traced) found the next layer on two axes.  A v5 pin covered
  PART of its decision's GENERATING SET -- the leading pad but not the trailing one, two of the baseline row's six string
  positions, the ISO shape's anchor but not its widths or separators, the glyph sets' Name stores while `globals()' and a dict
  mutation changed them, the hint's prefix, a tooltip whose fixture held no optional field, a CSS rule's presence but not the
  absence of an overriding one, the apparatus branch's first line on one-line output, four whitespace code points of 29, the
  newline and NBSP cells' class but not their tooltips, Q2's `else' at three of its 254 statuses, the named entry by a prefix
  of W2's output.  And a pin
  asserting a property of the SELECTED set said nothing about its COMPLEMENT (Fable 5.1) -- every legacy cell has the class
  line but not ONLY legacy cells, the padded cell's class but not its text, the set where it is DEFINED but not where it is
  USED.  So v6 enumerates each decision's generating set -- every operand position, both ends, every width and separator,
  every binding form and use, every optional field, every whitespace code point -- with its complement, and rows each
  member, or discloses it with its reason.
    checker  ledger shape: an object; `rows' present and a list; row objects;           C21a-f, C21i (rows absent: {} and
             `entries' absent = an empty row, else a list; entry objects                {"seats": []}), C21j (a row with no
                                                                                        entries key: rc 0); C23 (not JSON)
             baseline shape: a list of [six strings, a positive int] -- exactly seven   C13, C17 (a string count), C17b (a split
             fields, EACH of the six a str, the count an int and not a bool, > 0       key sums), C17c-g (eight fields; a count
                                                                                        of true, -1, 0, 1.0), C17h-m (each of the
                                                                                        six positions numeric in turn), C17n (a
                                                                                        None field), C21g (an object)
             md5 pin on the default path, CRLF folded; overrides skip it                C18, C18b; C11, C12, C17 (override)
             the selection: an explicit d, EXACT membership in the four, an ANSWER     C7 (no d), C14 (blank), C26 (null), C26b
                                                                                        (a list), C28 / C28b (a ✓ padded at its
                                                                                        start / its end), C2/C2b/C2c/C2d (each
                                                                                        glyph, C2c/C2d isolated), C8 (hold), C24
                                                                                        (a record, isolated)
             the key -- row, phase, seat, date, d, note -- byte for byte, at BOTH      C25a-k (the trailing end, case, a row
             ends; str() of d; a missing phase or seat keys as ""; the note's sha1     move), C25l-r (the leading end; a row id
             over its UTF-8 text, after str()                                          with a trailing or a leading space);
                                                                                        C15/C16 (the note); C26b; C29 (no phase,
                                                                                        no seat: its line exact); C20b (a
                                                                                        non-ASCII note: its line exact); C21k (a
                                                                                        list note holding no token: refused)
             the ceiling: a copy fails, a converted entry's allowance cannot refill     C9, C10, C15; d_nonote2 (design mutant)
             the cutoff: inclusive; a date counts only when the ISO shape -- four      C3, C4, C12 (isolated: before / on /
             digits, `-', two, `-', two -- OPENS it                                    after / far), C12s (a MATCHED identity
                                                                                        dated 2026-10-17T12:00:00), C12w (MATCHED
                                                                                        identities breaking the shape in one
                                                                                        place -- year, month or day width, either
                                                                                        separator: rc 0), C19a/b
             output: cp1252-safe with backslash escapes; the summary line WHOLE, and   C1 (the only line), C11 (the line count,
             ALONE on a clean run (its baseline number is the frozen total); each     the hint whole), C12 (the summary exact --
             refusal line WHOLE -- identifiers in order, its reason; the hint WHOLE    at C12-on the two numbers differ); C3,
                                                                                        C6, C9, C19a, C20, C20b, C29, C21k (the
                                                                                        refusal line exact; C20's d escaped)
             the glyph sets: ONE binding of DOMAIN and of D_CLASS, each the four,       C27 (an ast walk of both files: every
             and no other way to change either                                         binding form of the name -- a store, a
                                                                                        delete, a global, an import alias, a def
                                                                                        or class, an except or match name, a
                                                                                        parameter, an attribute or subscript store
                                                                                        keyed by it; a call to globals / vars /
                                                                                        locals / setattr / delattr / exec / eval /
                                                                                        compile / __import__; __dict__ or
                                                                                        __globals__ -- and every USE whitelisted:
                                                                                        DOMAIN in `in' and as `" ".join's
                                                                                        argument, D_CLASS in `.get(' and `in'; the
                                                                                        checker's EFFECTIVE DOMAIN read by
                                                                                        importing it)
    renderer the class: EXACT membership in the four -> its class, else legacy, on     R1 (per seat), R1h (a ✓ padded at each
             the answer a cell shows                                                    end), R1n (null), R3
             the class line opens EVERY legacy cell's tooltip -- the WHOLE tooltip,     R1 (OK), R1g (every simple legacy d,
             whatever optional fields the answer carries                                null, both pads, the newline and NBSP
                                                                                        cells included), R1w (all 29 whitespace
                                                                                        cells, whole), R1e (a
                                                                                        record beside it), R1f (a refused
                                                                                        exemption first), R1o (a grade, a badge
                                                                                        and evidence all present), R1q (neither
                                                                                        date nor note)
             ONLY a legacy cell carries the class line                                  R1p (the ok, pend, bad and hold cells)
             the glyph: escaped and otherwise UNCHANGED (a pad kept); `?` for a blank  R1b, R1h (the glyph text exact), R1d
             or whitespace-only d (any whitespace)                                     (space, tab, newline, NBSP); R1w (all 29
                                                                                        str.isspace() code points)
             the strip: each number the ledger's own count by EXACT membership, and     R2 (the shipped ledger: the whole strip
             its labels                                                                 string), R2b (the fixture ledger, whose
                                                                                        pads and null count legacy)
             the legend line; the two CSS rules the class adds, and no other rule in   R4; R5 (the two rules exact, and the ONLY
             the style block naming the class                                          rules naming `legacy')
    Q2       the branches: rc 0 GOOD with the checker's first line; rc 1 BAD with the  W1 (the output whole: GOOD and the
             refusal named; ANY other status BAD "could not run" with the checker's     summary, then the counter), W2 (the
                                                                                        output whole, the entry named), W3 (rc 2),
             FIRST line, stderr included                                                W7 (rc 7, a two-line message on stderr:
                                                                                        the output whole), W8 (python absent: rc
                                                                                        127), W9 (EVERY status 2-255: the else
                                                                                        partition exhausted)
             the checker absent -> BAD                                                  W6
             an exported GXDOMAIN_BASELINE / GXLEDGER stripped                          W4, W5
    DISCLOSED, each with its reason:
      a sha1-16 collision -- a note passing as a FROZEN entry's note is a fixed-target second preimage, about 2^64 work; an
        arbitrary collision between two new notes (about 2^32, birthday) passes nothing, since neither matches a frozen key
        (GPT-6 Astra, v4 pass: the two figures are different searches);
      `ISO.match' -> `ISO.search': equivalent, the pattern being anchored with `^'; the `[:10]' slice before the compare:
        equivalent, a string sharing the cutoff's first ten characters is never smaller than it; `repr' of a non-string date:
        equivalent to `str' for every JSON value;
      a missing or null NOTE hashed as "" (`d_notenone'): 0 of the 1,356 frozen answers has one, and 0 entries anywhere carry
        a note that is the literal string "None", which the mutant would hash a missing note as (GLM 5.3, v5 pass; measured);
      case-folding or whitespace-stripping INSIDE a field (C25 edits both ends; nothing edits the middle);
      the GOOD branch's `head -1': equivalent, the checker prints exactly one line on rc 0 (C1); the APPARATUS FAIL messages'
        wording: display only (their rc 2 is pinned; an emptied reason passes every row -- `x_apparatusmsg', Fable 5.1, v5
        pass, measured);
      the page's CSS outside the two rules this landing adds (a rule hiding every glyph would be HEAD's CSS, not this diff);
      a change to the glyph sets by a mechanism C27 does not name (a helper module rebinding them after import, a C
        extension) is outside the contract -- and the renderer has a second, ACCIDENTAL closure worth keeping deliberately:
        `summary()''s `n' is keyed by the four literal glyphs, so a fifth D_CLASS key CRASHES the generator (KeyError) on the
        first entry that spells it -- loud, never a silent misclassification (Fable 5.1, v5 pass, measured);
      the selection predicate widened by a DISJUNCT naming a spelling no fixture or ledger entry carries (`x["d"] in DOMAIN or
        x["d"] == "ZXQ"'): C27 pins DOMAIN's definition and every use of it, not the predicate around it, and no finite row
        set pins every novel spelling -- the plausible widenings, the ledger's own off-domain spellings, die on C1 (Fable 5.1,
        v5 pass, measured: `+ ("OK",)' at the use site 80/96);
      a renderer that CRASHES on the shipped ledger is a kill: R2's census is guarded, so the run completes with its tally and
        sentinel instead of dying INCOMPLETE (v5's controls crashed there, and the mutant driver scored a real kill as an
        apparatus failure -- Fable 5.1, v5 pass, measured on a comment-only renderer);
      the production good/bad reporters and the section's final exit: the W rows use counting stand-ins (the staged
        precommit's `bad' increments `fail', and both final exits return 1 when it is positive -- read, Fable 5.1, v4 pass);
      the Q2 section header: `say' is stubbed in the W block, and it is display only;
      the note-type scope of condition 2: "is it an answer" is `stage_tokens.is_answer', which tests membership on the untyped
        note -- a list or dict note holding a token as an element or a key is a NON-answer and is skipped, as the renderer
        also shows it (GPT-6 Astra, v5 pass, measured; K19's "nothing is skipped" was false); a list note holding no token is
        an answer and is refused (C21k); a bool note: True rc 2, False rc 1 (Astra, measured).
    A fold of d, or a fold or strip of the NOTE, is one-sided on this ledger -- the baseline holds raw values and only the
    note's sha -- so it dies on C1: some frozen keys stop matching (on HEAD's ledger the d fold changes 1,100 of the 1,356
    frozen answers' keys, the note strip 2, the note fold 1,352; measured by Fable 5.1, v4 pass).  The coherent fold of d is the
    two-edit design mutant d_dfold2, killed by C25d.  Two kills the shipped ledger already supplies are ALSO rowed in isolation,
    so no pin rests on the ledger's composition alone: the `entries' default (98 of 912 shipped rows carry no `entries' key;
    C21j) and a latin-1 note encoding (34 frozen notes are non-ASCII, one beyond latin-1; C20b).

  CHECKER (Astra's four conditions, the ruling's grandfathering amendment, pass 2's, the adjudication pass's and the v3 and
  v4 passes' findings):
    C1   shipped ledger, shipped baseline (md5 pin live): rc 0 and the summary line EXACTLY
    C2 / C2b  an answer ON / AFTER the cutoff with a valid glyph (positive)                       -> 0 / 0
    C2c / C2d  an answer after the cutoff with ⏸ / with …, in a ledger holding ONLY that entry (positive) -> 0 / 0
    C3   an answer ON the cutoff with "OK" (inclusive) -- its refusal line EXACTLY                  -> 1
    C4   an answer AFTER the cutoff with "OK"                                                       -> 1
    C5   a new answer dated BEFORE the cutoff with "OK" (back-dated)                                -> 1
    C6   an UNDATED answer with "N/A" -- its refusal line EXACTLY (date "(none)", no ISO clause)    -> 1
    C7   an answer after the cutoff with NO `d`                                                     -> 0
    C8   a HELD marker after the cutoff with d "HELD" (not an answer)                               -> 0
    C9   an identical copy of a frozen entry -- its refusal line EXACTLY                            -> 1
    C10  a frozen entry rewritten to a glyph (the population shrinks)                               -> 0
    C11  the baseline emptied (override): every shipped off-domain answer named, the summary EXACTLY, the hint -> 1
    C12  the cutoff ISOLATED: a fixture baseline holding an identity dated before / on / after / far   -> 0 / 1 / 1 / 1,
         each with its summary line EXACTLY (on/after/far: within = baseline - 1)
    C12s a MATCHED identity dated "2026-10-17T12:00:00" (the ISO shape opens it)                    -> 1
    C13  an unreadable baseline (override)                                                          -> 2
    C14  a new answer with an explicit BLANK d                                                      -> 1
    C15  REFILL: a frozen entry rewritten to a glyph, plus a new answer reusing its (row, phase, seat, date, d) -> 1
    C16  a frozen entry's NOTE edited, its d left off-domain                                        -> 1
    C17  a misshapen baseline (override; counts as strings)                                         -> 2
    C17b a key SPLIT across two baseline rows (override) sums                                       -> 0
    C17c-g  the shipped baseline plus ONE misshapen row (override): eight fields; a count of true; -1; 0; 1.0  -> 2 each
    C17h-m  the same, each of the six string positions numeric in turn: row, note sha, phase, seat, date, d     -> 2 each
    C17n the same, a None date (`isinstance(v, (str, type(None)))' would pass it)                    -> 2
    C18  the md5 PIN: a temp copy of the pipeline with one baseline line changed -> 2; unchanged -> 0
    C18b the same baseline with CRLF line endings passes the pin                                    -> 0
    C19  malformed dates on new answers: "10/18/2026" (its refusal line EXACTLY) and a number -- rc 1, no traceback,
         the date NAMED as not ISO                                                                  -> 1 / 1
    C20  a new answer whose d is non-ASCII, under the precommit's cp1252 pipe -- rc 1, no traceback, its line EXACT
         with the d backslash-escaped                                                               -> 1
    C20b a new answer whose NOTE is non-ASCII ("café — ✓") -- rc 1, its line EXACT (the note's UTF-8 sha)  -> 1
    C21  misshapen LEDGERS -- {"rows": null}, a row that is not an object, a list, {"rows": {}}, a string entry, entries
         that are an object; C21i {} and {"seats": []} (rows absent); C21g a baseline that is an object (override); C21h a
         note that is a number (it raises inside stage_tokens.is_answer -- the walk's except-arm)  -> 2 each, no traceback
    C21j a ledger whose row carries NO entries key (an empty row), beside a valid one               -> 0
    C21k a new answer whose note is a LIST holding no token -- an answer, refused, its line EXACT  -> 1
    C22  a frozen entry's `ev` edited -- outside the six fields (positive)                          -> 0
    C23  a ledger that is not JSON                                                                  -> 2
    C24  a non-answer RECORD (NOTSEAT) after the cutoff with d "OK", in a ledger holding ONLY it      -> 0
    C25  a frozen entry with ONE key field edited by its least visible change: a-k the date suffixed / a trailing space,
         d trailing space / case, note trailing space / case, seat trailing space / case, phase trailing space / case,
         the entry moved to another row; l-r the entry moved to a row whose id carries a trailing space, the date, d,
         note, seat and phase each with a LEADING space, the entry moved to a row whose id carries a leading space -> 1 each
    C26  a new answer with an explicit "d": null                                                     -> 1
    C26b a new answer whose d is a LIST -- rc 1, no traceback (the key takes str() of d)              -> 1
    C27  DOMAIN and D_CLASS: ONE binding each and NO other way to change them -- an ast walk of every binding form and
         every use (whitelisted), and the checker's EFFECTIVE DOMAIN read by importing it -- each exactly ✓ ✕ ⏸ …
    C28 / C28b  a new answer BEFORE the cutoff with a glyph padded at its START (" ✓") / its END ("✓ ")  -> 1 / 1
    C29  a new answer with NO phase and NO seat -- refused, its line EXACT (both identifiers empty)   -> 1
    C12w MATCHED identities whose date breaks the ISO shape in ONE place -- a five-digit year, a one-digit month, a
         one-digit day, a `/' for the first separator, for the second -- each in its fixture baseline, so only the shape
         decides                                                                                    -> 0 each
  RENDERER:
    R1   a fixture row, one entry per seat: class AND glyph per cell, and the legacy cell's tooltip EXACTLY
    R1b  an escapable `d` ("<b>&") renders escaped
    R1c  the fixture page says neither "not approval" nor "not a seat failure" anywhere
    R1d  a whitespace-only `d` -- a space, a tab, a newline, an NBSP -- shows `?`
    R1e  an answer cell with a non-answer record beside it: its WHOLE tooltip -- class line, date, note, the record line
    R1f  a legacy answer carrying a refused stage exemption: the refusal line first, then the class line, exactly
    R1g  EVERY simple legacy cell's WHOLE tooltip -- the class line for ITS d ("OK", "", "N/A", "<b>&", " ", " ✓", "\t",
         "\n", "\xa0", null), the date, the note
    R1h  a ✓ padded at its start (" ✓") and at its end ("✓ ") each renders legacy, its glyph text EXACTLY as written
    R1o  a legacy answer carrying a grade, a badge and evidence: its WHOLE tooltip, the class line first
    R1p  the NON-legacy answer cells -- ok, pend, bad, hold -- carry NO class line: each tooltip is the date and note alone
    R1q  a legacy answer with NO date and NO note (d "BARE"): its tooltip is the class line alone
    R1w  EVERY str.isspace() code point alone as d (29 in this python) shows `?' and carries its WHOLE tooltip -- the
         whitespace set exhausted
    R1n  an explicit "d": null renders legacy with the glyph "None", not …
    R2   the shipped ledger, BEFORE vs AFTER: only pend -> legacy moves; the strip string EXACTLY -- each number the ledger's
         own count by exact membership, and its labels
    R2b  the FIXTURE page's strip EXACTLY, against the fixture's own counts (its padded ✓ and null count legacy)
    R3   MUTANT renderers (fallback -> ok, -> pend; the escape dropped) must RENDER and then fail R1 / R1b -- a crash is not
         a kill
    R4   the legend carries the legacy line EXACTLY
    R5   the page carries the two CSS rules the class adds, EXACTLY, and NO other rule in its style block names `legacy'
  WIRING (section Q2, extracted from precommit_check.sh and run with reporters that COUNT failures; each first line must also
  carry its BRANCH's own words):
    W1   the shipped ledger                    -> exactly "GOOD <the summary line>" and "FAILURES 0"
    W2   a new off-domain answer               -> BAD, its WHOLE output: the first line, every line of the checker's
         output indented, the counter
    W3   the baseline absent (rc 2 path)       -> BAD "could not run (rc 2)", failures >= 1
    W4   an exported GXDOMAIN_BASELINE that would admit a new entry is IGNORED -> BAD, failures >= 1
    W5   an exported GXLEDGER naming a CLEAN ledger is IGNORED; the bad default ledger is read -> BAD, failures >= 1
    W6   the checker ABSENT from the fake tools dir                -> BAD "MISSING", failures >= 1
    W7   a checker that exits 7 with a TWO-line message on STDERR -> exactly "BAD ... could not run (rc 7): <its FIRST line>"
         and "FAILURES 1"
    W8   python ABSENT from PATH (a launch failure)               -> BAD "could not run (rc 127)", failures >= 1
    W9   EVERY status 2-255, a stub exiting each in turn (254 runs)    -> each exactly "BAD ... could not run (rc N): <its
         first line>" and the counter 1 -- the `else' partition EXHAUSTED
"""
import collections, copy, hashlib, html, io, json, os, re, shutil, subprocess, sys, tempfile

if hasattr(sys.stdout, "reconfigure"):          # this file prints glyphs (R2's strip); run it anywhere, piped or not
    sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, os.pardir, os.pardir, os.pardir))
PIPE = os.path.join(REPO, "tools", "pipeline")
CHECKER = os.environ.get("CTL_CHECKER") or os.path.join(PIPE, "check_entry_domain.py")
RENDER = os.environ.get("CTL_RENDER") or os.path.join(PIPE, "gen_dashboard.py")
PRE = os.environ.get("CTL_PRECOMMIT") or os.path.join(REPO, "tools", "precommit_check.sh")
BEFORE = os.path.join(HERE, "gen_dashboard_before.py")      # HEAD's renderer at the landing, preserved
#  the baseline travels WITH the checker under test: staged runs keep it beside the staged checker, and on the tree the two
#  directories are the same
BASELINE = os.path.join(os.path.dirname(os.path.abspath(CHECKER)), "entry_domain_baseline.json")
if not os.path.exists(BASELINE):
    BASELINE = os.path.join(PIPE, "entry_domain_baseline.json")
LEDGER = os.path.join(PIPE, "ledger.json")
sys.path.insert(0, PIPE)
import stage_tokens as st  # noqa: E402

T = tempfile.mkdtemp()
res = []


def say(label, ok, detail=""):
    res.append(ok)
    tag, rest = label.split(" ", 1)
    print("%-4s %-76s %s  %s" % (tag, rest, "ok" if ok else "NO", detail))


def wjson(name, obj):
    p = os.path.join(T, name)
    io.open(p, "w", encoding="utf-8").write(json.dumps(obj, ensure_ascii=False))
    return p


def pipe_copy(tag, baseline_text=None):
    """a temp copy of the pipeline dir holding the checker under test, stage_tokens.py and a baseline (default: shipped)"""
    d = os.path.join(T, "pipe_" + tag)
    os.makedirs(d, exist_ok=True)
    shutil.copy(CHECKER, os.path.join(d, "check_entry_domain.py"))
    shutil.copy(os.path.join(PIPE, "stage_tokens.py"), d)
    b = os.path.join(d, "entry_domain_baseline.json")
    if baseline_text is None:
        shutil.copy(BASELINE, b)
    else:
        io.open(b, "w", encoding="utf-8", newline="").write(baseline_text)
    return os.path.join(d, "check_entry_domain.py")


def run_checker(ledger_path, baseline_path=None, checker=None):
    #  NO PYTHONIOENCODING: the precommit sets none, so the checker must survive a cp1252 pipe (Fable 5.1, pass 2)
    env = dict(os.environ, GXLEDGER=ledger_path)
    for k in ("GXDOMAIN_BASELINE", "PYTHONIOENCODING", "PYTHONUTF8"):
        env.pop(k, None)
    if baseline_path is not None:
        env["GXDOMAIN_BASELINE"] = baseline_path
    r = subprocess.run([sys.executable, checker or DEFAULT_CHECKER], capture_output=True, env=env)
    out = (r.stdout + r.stderr).decode("cp1252", "replace")
    return r.returncode, out.strip().splitlines()


DEFAULT_CHECKER = pipe_copy("default")          # the checker under test, beside the SHIPPED baseline (md5 pin live)
L0 = json.load(io.open(LEDGER, encoding="utf-8"))
ROW0 = L0["rows"][0]["id"]
N_OFF = sum(1 for r in L0["rows"] for x in r.get("entries", [])
            if "d" in x and x["d"] not in ("✓", "✕", "⏸", "…") and st.is_answer(x))


def with_entries(entries, ledger=None):
    L = copy.deepcopy(ledger or L0)
    for row, e in entries:
        for r in L["rows"]:
            if r["id"] == row:
                r.setdefault("entries", []).append(e)
    return wjson("l_%d.json" % len(res), L)


def ans(date, **kw):
    e = {"phase": "review", "seat": "grok", "note": "a control entry"}
    if date is not None:
        e["date"] = date
    e.update(kw)
    return e


def sha16(note):
    return hashlib.sha1(str(note or "").encode("utf-8")).hexdigest()[:16]


WHY_CUT = "dated on or after the cutoff 2026-10-17"
WHY_CEIL = "beyond the frozen ceiling for its six fields -- a new answer, a copy, or an old one edited (classify it)"
WHY_ISO = "; its date is not ISO YYYY-MM-DD"


def offline(row, e, why):
    """the WHOLE refusal line the checker must print for entry e of row -- identifiers in their order, then the reason
    (v4 read only the count of lines, so a reason replaced or row and phase swapped passed -- Fable 5.1, GPT-6 Astra, v4 pass)"""
    dt = e.get("date")
    dt = dt if isinstance(dt, str) else ("" if dt is None else repr(dt))
    return "OFF-DOMAIN ANSWER  row %s  phase %s  seat %s  date %s  d %r  note %s -- %s" % (
        row, e.get("phase") or "", e.get("seat") or "", dt or "(none)", str(e["d"]), sha16(e.get("note")), why)


def cp(s):
    """what the checker's cp1252 stdout, reconfigured errors="backslashreplace", carries for s -- as run_checker decodes it"""
    return s.encode("cp1252", "backslashreplace").decode("cp1252")


def summary_line(n_cur, n_within, n_base):
    return ("entry domain: %d off-domain answer entries; %d within the frozen ceiling (baseline %d); cutoff 2026-10-17 inclusive"
            % (n_cur, n_within, n_base))


def ident(row, e):
    return [row, e.get("phase") or "", e.get("seat") or "", e.get("date") if isinstance(e.get("date"), str) else "",
            str(e["d"]), hashlib.sha1(str(e.get("note") or "").encode("utf-8")).hexdigest()[:16]]


print("# dashokclass controls (v6) -- checker %s | renderer %s | precommit %s | baseline %s"
      % (hashlib.md5(open(CHECKER, "rb").read()).hexdigest()[:8], hashlib.md5(open(RENDER, "rb").read()).hexdigest()[:8],
         hashlib.md5(open(PRE, "rb").read()).hexdigest()[:8], hashlib.md5(open(BASELINE, "rb").read()).hexdigest()[:8]))
# ------------------------------------------------------------------ the checker
rc, out = run_checker(LEDGER)
first = out[0] if out else ""
#  the summary's BASELINE number too: `sum(base.values())` -> `len(base)` printed 1,342 and passed every v3 control (Grok 4.7,
#  v3 pass) -- the count of frozen answers is 1,356 over 1,342 keys
#  v5: the WHOLE line -- "inclusive" dropped from it passed all 72 v4 controls (Fable 5.1, v4 pass)
#  v6: and ALONE -- the hint printed on a clean run passed all 96 v5 controls
say("C1 shipped ledger, shipped baseline, md5 pin live; the summary line EXACTLY, and the only line",
    rc == 0 and out == [summary_line(N_OFF, N_OFF, N_OFF)], "rc %d: %d lines; %s" % (rc, len(out), first))
for lab, ent, want in [
    ("C2 ON the cutoff, a valid glyph (positive)", ans("2026-10-17", d="✓"), 0),
    ("C2b AFTER the cutoff, a valid glyph (positive)", ans("2026-10-18", d="✕"), 0),
    ("C3 ON the cutoff, d OK (inclusive)", ans("2026-10-17", d="OK"), 1),
    ("C4 AFTER the cutoff, d OK", ans("2026-10-18", d="OK"), 1),
    ("C5 a new answer BEFORE the cutoff, d OK (back-dated)", ans("2026-09-01", d="OK", seat="minimax"), 1),
    ("C6 undated, d N/A", ans(None, d="N/A"), 1),
    ("C7 after the cutoff, NO d", ans("2026-10-18"), 0),
    ("C8 a HELD marker after the cutoff, d HELD", ans("2026-10-18", d="HELD", note=st.HELD + " grok] waiting"), 0),
    ("C14 a new answer with an explicit BLANK d", ans("2026-10-10", d=""), 1),
    ('C19a a new answer dated "10/18/2026", d OK', ans("10/18/2026", d="OK"), 1),
    ("C19b a new answer with a NUMERIC date, d OK", ans(20261018, d="OK"), 1),
    ("C20 a new answer with a non-ASCII d (cp1252 stdout, no traceback)", ans("2026-10-18", d="✗"), 1),
    #  an explicit "d": null is PRESENT and off-domain -- `if x.get("d") is None` would treat it as missing (Fable 5.1, v3 pass)
    ("C26 a new answer with an explicit null d", ans("2026-10-10", d=None), 1),
    #  v5: a LIST d -- the key takes str() of d; without it the Counter raises on an unhashable key (Fable 5.1, v4 pass)
    ("C26b a new answer whose d is a LIST", ans("2026-10-10", d=["OK"]), 1),
    #  v5: a PADDED glyph is outside the four for the checker as for the renderer (R1h) -- `str(d).strip() in DOMAIN` passed
    #  all 72 v4 controls (Fable 5.1, Grok 4.7, v4 pass)
    ("C28 a new answer BEFORE the cutoff with a padded glyph ' ✓'", ans("2026-10-10", d=" ✓"), 1),
    #  v6: the OTHER end -- `str(x["d"]).rstrip() in DOMAIN' passed all 96 v5 controls (GPT-6 Astra, v5 pass)
    ("C28b a new answer BEFORE the cutoff with a glyph padded at its END '✓ '", ans("2026-10-10", d="✓ "), 1),
    #  v6: a NON-ASCII note -- its sha is over the note's UTF-8; a latin-1 encode raises (or rehashes) on it (GLM 5.3, v5 pass)
    ("C20b a new answer whose note is non-ASCII", ans("2026-10-10", d="OK", note="café — ✓"), 1),
    #  v6: no phase, no seat -- each keys and prints as "" ; dropping the `or ""' printed "None" and passed all 96 v5 controls
    #  (GLM 5.3, v5 pass, measured)
    ("C29 a new answer with no phase and no seat", {"date": "2026-10-10", "d": "OK", "note": "no phase or seat"}, 1),
    #  v6: a LIST note holding no token is an ANSWER (is_answer finds no token in it) and is refused, never skipped; a
    #  mutant dropping the str() before the hash raised on it instead (Fable 5.1 measured rc 1 on the v4 pass)
    ("C21k a new answer whose note is a list holding no token", ans("2026-10-10", d="OK", note=["a list note"]), 1),
]:
    rc, out = run_checker(with_entries([(ROW0, ent)]))
    tb = any("Traceback" in l for l in out)
    #  a malformed date must be NAMED in the reason, not only refused: v1's lexical `t[3] >= CUTOFF` and a deleted suffix each
    #  passed every v2 control while calling a numeric date "on or after the cutoff" (Fable 5.1, adjudication pass)
    why = (not lab.startswith("C19")) or any("its date is not ISO" in l for l in out)
    #  v5: the WHOLE refusal line for C3 (the cutoff reason), C6 (an undated entry: "(none)", no ISO clause) and C19a (the
    #  ISO clause) -- v4 read only rc and the line count (Fable 5.1, GPT-6 Astra, v4 pass)
    #  v6: also C20 (its d backslash-escaped by the cp1252 reconfigure -- "replace" printed `?' and passed all 96 v5
    #  controls), C20b, C29 and C21k
    exact_why = {"C3": WHY_CUT, "C6": WHY_CEIL, "C19a": WHY_CEIL + WHY_ISO, "C20": WHY_CUT, "C20b": WHY_CEIL, "C29": WHY_CEIL,
                 "C21k": WHY_CEIL}.get(lab.split()[0])
    offl = [l.strip() for l in out if "OFF-DOMAIN ANSWER" in l]
    exact = exact_why is None or offl == [cp(offline(ROW0, ent, exact_why))]
    say(lab, rc == want and not tb and why and exact, "rc %d (want %d)%s%s%s" % (
        rc, want, " TRACEBACK" if tb else "", "" if why else " REASON NOT NAMED",
        "" if exact else " LINE NOT EXACT: %r" % (offl[:1],)))
#  C2c/C2d ISOLATED (GPT-6 Astra, v3 pass): the shipped ledger already carries 21 ⏸ and 35 … answers, so dropping either glyph
#  from DOMAIN reddened the v3 rows without their own entry; a ledger holding ONLY the fixture entry makes each its own witness
for lab, ent in (("C2c AFTER the cutoff, d ⏸, in a ledger holding only it (positive)", ans("2026-10-18", d="⏸")),
                 ("C2d AFTER the cutoff, d …, in a ledger holding only it (positive)", ans("2026-10-18", d="…"))):
    rc, out = run_checker(wjson("l_iso_%d.json" % len(res), {"rows": [{"id": "ctliso", "entries": [ent]}]}))
    say(lab, rc == 0, "rc %d" % rc)
#  C24 ISOLATED (GPT-6 Astra, v4 pass): the shipped ledger carries five off-domain NOTSEAT records, so `st.is_held(x)` for
#  `not st.is_answer(x)` reddened C24 for the LEDGER's reason; a ledger holding only the record makes it its own witness
rc, out = run_checker(wjson("l_iso_c24.json", {"rows": [{"id": "ctliso", "entries": [
    ans("2026-10-18", d="OK", note=st.NOTSEAT + " a main-loop record")]}]}))
say("C24 a non-answer RECORD (NOTSEAT) after the cutoff, d OK, in a ledger holding only it", rc == 0, "rc %d" % rc)
# a frozen entry, found from the shipped baseline: copied (C9), rewritten (C10), refilled (C15), note-edited (C16), ev-edited (C22)
base = [json.loads(l.rstrip(",\n")) for l in io.open(BASELINE, encoding="utf-8") if l.startswith("[\"")]
k0 = base[0]


def find_frozen(L):
    for r in L["rows"]:
        if r["id"] != k0[0]:
            continue
        for x in r["entries"]:
            if "d" in x and ident(r["id"], x) == k0[:6]:
                return x
    raise SystemExit("APPARATUS FAIL: the first baseline identity is not in the shipped ledger")


src = find_frozen(L0)
rc, out = run_checker(with_entries([(k0[0], dict(src))]))
offl = [l.strip() for l in out if "OFF-DOMAIN ANSWER" in l]
say("C9 an identical copy of a frozen entry (%s %s %s %s %r): its refusal line EXACTLY" % tuple(k0[:5]),
    rc == 1 and offl == [offline(k0[0], src, WHY_CEIL)], "rc %d; %r" % (rc, offl[:1]))
L = copy.deepcopy(L0); find_frozen(L)["d"] = "✓"
rc, out = run_checker(wjson("l_rewrite.json", L))
say("C10 a frozen entry rewritten to a glyph", rc == 0, "rc %d" % rc)
refill = dict(src); refill["note"] = "a different answer reusing the converted entry's slot"
rc, out = run_checker(with_entries([(k0[0], refill)], ledger=L))
say("C15 REFILL: the converted entry's (row, phase, seat, date, d) reused", rc == 1, "rc %d" % rc)
L2 = copy.deepcopy(L0); f = find_frozen(L2); f["note"] = (f.get("note") or "") + " (a later correction)"
rc, out = run_checker(wjson("l_noteedit.json", L2))
say("C16 a frozen entry's note edited, d left off-domain", rc == 1, "rc %d" % rc)
L3 = copy.deepcopy(L0); f = find_frozen(L3); f["ev"] = (f.get("ev") or "") + " (a corrected path)"
rc, out = run_checker(wjson("l_evedit.json", L3))
say("C22 a frozen entry's ev edited, outside the six fields (positive)", rc == 0, "rc %d" % rc)
#  C25: each key field of the FROZEN entry edited by its least visible change.  A mutant normalising one field on the ledger's
#  side -- `v[:10]` on the date, `.strip()`, `.lower()` -- passed every v3 control (GPT-6 Astra, v3 pass: the date suffix)
OTHER_ROW = next(r["id"] for r in L0["rows"] if r["id"] != k0[0])
for tag, field, how, fn in (("a", "date", "suffixed T12:00:00", lambda v: v + "T12:00:00"),
                            ("b", "date", "a trailing space", lambda v: v + " "),
                            ("c", "d", "a trailing space", lambda v: v + " "),
                            ("d", "d", "its case swapped", lambda v: v.swapcase()),
                            ("e", "note", "a trailing space", lambda v: v + " "),
                            ("f", "note", "its case swapped", lambda v: v.swapcase()),
                            ("g", "seat", "a trailing space", lambda v: v + " "),
                            ("h", "seat", "upper-cased", lambda v: v.upper()),
                            ("i", "phase", "a trailing space", lambda v: v + " "),
                            ("j", "phase", "upper-cased", lambda v: v.upper())):
    Le = copy.deepcopy(L0); fe = find_frozen(Le)
    assert fn(fe[field]) != fe[field], (tag, field)
    fe[field] = fn(fe[field])
    rc, out = run_checker(wjson("l_key_%s.json" % tag, Le))
    say("C25%s a frozen entry's %s, %s" % (tag, field, how), rc == 1, "rc %d" % rc)
Le = copy.deepcopy(L0); fe = find_frozen(Le)
for r in Le["rows"]:
    if r["id"] == k0[0]:
        r["entries"] = [x for x in r["entries"] if x is not fe]
    if r["id"] == OTHER_ROW:
        r.setdefault("entries", []).append(fe)
rc, out = run_checker(wjson("l_key_k.json", Le))
say("C25k a frozen entry moved to another row (%s)" % OTHER_ROW, rc == 1, "rc %d" % rc)
#  v5: the LEADING end of every field, and the row id at both ends -- `.lstrip()` on the date, d, seat, phase or note, and
#  `str(r.get("id")).strip()`, each passed all 72 v4 controls, which edited only the trailing end (Fable 5.1, Grok 4.7, GPT-6
#  Astra, v4 pass)


def moved_to(new_id):
    Lm = copy.deepcopy(L0); fm = find_frozen(Lm)
    for r in Lm["rows"]:
        if r["id"] == k0[0]:
            r["entries"] = [x for x in r["entries"] if x is not fm]
    Lm["rows"].append({"id": new_id, "title": "row id control", "sev": "LOW", "state": "open", "commits": "", "entries": [fm]})
    return Lm


rc, out = run_checker(wjson("l_key_l.json", moved_to(k0[0] + " ")))
say("C25l a frozen entry moved to a row whose id has a TRAILING space", rc == 1, "rc %d" % rc)
for tag, field in (("m", "date"), ("n", "d"), ("o", "note"), ("p", "seat"), ("q", "phase")):
    Le = copy.deepcopy(L0); fe = find_frozen(Le)
    fe[field] = " " + fe[field]
    rc, out = run_checker(wjson("l_key_%s.json" % tag, Le))
    say("C25%s a frozen entry's %s with a LEADING space" % (tag, field), rc == 1, "rc %d" % rc)
rc, out = run_checker(wjson("l_key_r.json", moved_to(" " + k0[0])))
say("C25r a frozen entry moved to a row whose id has a LEADING space", rc == 1, "rc %d" % rc)
rc, out = run_checker(LEDGER, wjson("b_empty.json", []))
nb = sum(1 for l in out if "OFF-DOMAIN ANSWER" in l)
#  and the SUMMARY line on this dirty ledger: it was pinned only on the clean one, where "passes" and "entries" agree, so
#  printing len(cur) for both passed every v3 control (GLM 5.3, v3 pass)
s11 = summary_line(N_OFF, 0, 0)
f11 = out[0] if out else ""
#  v6: the hint WHOLE -- a false "all records need classification" passed the v5 prefix test (GPT-6 Astra, v5 pass) -- and the
#  output exactly the summary, one line per refusal, the hint
HINT = cp("  -> give each a `d` from ✓ ✕ ⏸ … (or omit `d`, which renders as …); a non-answer record is exempt").strip()
hint = bool(out) and out[-1].strip() == HINT
say("C11 baseline emptied: every shipped off-domain answer named, the summary counts 0 within the ceiling, the hint WHOLE",
    rc == 1 and nb == N_OFF and f11 == s11 and hint and len(out) == N_OFF + 2, "rc %d, %d of %d named, %d lines; summary %s; hint %s"
    % (rc, nb, N_OFF, len(out), "ok" if f11 == s11 else repr(f11[:90]), "ok" if hint else repr(out[-1][:90] if out else "")))
# C12: the cutoff test isolated -- each fixture entry IS in its fixture baseline, so only the date can refuse it
#  and FAR after: a two-day membership test (`in ("2026-10-17", "2026-10-18")`) passed before/on/after (Grok 4.7, v3 pass)
for tag, dt, want in (("before", "2026-10-16", 0), ("on", "2026-10-17", 1), ("after", "2026-10-18", 1),
                      ("far", "2027-01-01", 1)):
    e = ans(dt, d="OK", seat="kimi", note="cutoff isolation " + tag)
    fb = wjson("b_cut_%s.json" % tag, base + [ident(ROW0, e) + [1]])
    rc, out = run_checker(with_entries([(ROW0, e)]), fb)
    #  v5: the summary EXACTLY -- here the fixture baseline holds N_OFF + 1 and a refused entry leaves N_OFF within, so the
    #  baseline number differs from the within-count; C1 and C11 cannot tell them apart (1356/1356, 0/0), and printing the
    #  within-count there passed all 72 v4 controls (Fable 5.1, v4 pass)
    s12 = summary_line(N_OFF + 1, N_OFF + 1 if want == 0 else N_OFF, N_OFF + 1)
    f12 = out[0] if out else ""
    say("C12 cutoff isolated: a FROZEN identity dated %s (%s), the summary EXACTLY" % (dt, tag), rc == want and f12 == s12,
        "rc %d (want %d); summary %s" % (rc, want, "ok" if f12 == s12 else repr(f12[:100])))
#  C12s: a MATCHED identity whose date the ISO shape OPENS -- `^...$' on the shape refused nothing and passed all 72 v4
#  controls (Fable 5.1, Grok 4.7, GPT-6 Astra, v4 pass); the checker reads the first ten characters
e = ans("2026-10-17T12:00:00", d="OK", seat="kimi", note="cutoff isolation suffixed")
fb = wjson("b_cut_suffixed.json", base + [ident(ROW0, e) + [1]])
rc, out = run_checker(with_entries([(ROW0, e)]), fb)
say("C12s cutoff isolated: a FROZEN identity dated 2026-10-17T12:00:00", rc == 1, "rc %d (want 1)" % rc)
#  C12w (v6): the ISO SHAPE's widths and separators -- `\d{1,2}' for the month passed all 96 v5 controls, reading
#  "2026-9-1" as a date after the cutoff (GPT-6 Astra, v5 pass).  Each identity is FROZEN and breaks the shape in one place,
#  each chosen to compare at or after the cutoff if the shape were loosened there, so only the shape decides: rc 0
#  (a one-edit mutant loosens ONE separator, so each has its own row: one date breaking both would miss either alone)
for tag, dt in (("year", "99999-10-18"), ("month", "2026-9-17"), ("day", "2026-10-9"), ("sep1", "2026/10-18"),
                ("sep2", "2026-10/18")):
    e = ans(dt, d="OK", seat="kimi", note="iso shape " + tag)
    fb = wjson("b_cut_w_%s.json" % tag, base + [ident(ROW0, e) + [1]])
    rc, out = run_checker(with_entries([(ROW0, e)]), fb)
    say("C12w the ISO shape's %s: a FROZEN identity dated %s is not read as a date" % (tag, dt), rc == 0, "rc %d (want 0)" % rc)
rc, out = run_checker(LEDGER, os.path.join(T, "no_such_baseline.json"))
say("C13 an unreadable baseline", rc == 2, "rc %d" % rc)
#  C27: the glyph SET, read from both files' own literals.  A fifth member (`"ZXQ"`) in the checker's DOMAIN, or a fifth key in
#  the renderer's D_CLASS, was invisible to every v3 control -- no control writes that spelling, and none can write every one
#  (Grok 4.7, v3 pass) -- so the set is pinned where it is defined, and the two files must agree, as the checker says
import ast  # noqa: E402
#  v5 counted the Name stores of each name; v6 walks EVERY binding form and EVERY use.  `globals()["DOMAIN"] = ...' and
#  `D_CLASS.update(ZXQ="ok")' each passed all 96 v5 controls -- the first is no Name store, the second mutates the dict
#  without rebinding it (GLM 5.3, GPT-6 Astra, v5 pass, measured).  So: exactly one binding, a module-level assignment of a
#  literal; no other binding form of the name (a store or delete, a global or nonlocal, an import alias, a def or class, an
#  except or match name, a parameter, an attribute or subscript store keyed by it); no call to the builtins that rebind by
#  name or by string (globals, vars, locals, setattr, delattr, exec, eval, compile, __import__) and no __dict__ / __globals__;
#  and every USE of the name on a whitelist -- DOMAIN only in `in' / `not in' and as `" ".join(...)''s argument, D_CLASS only
#  as `D_CLASS.get(...)' and in `in' / `not in'.  The checker is import-safe, so its EFFECTIVE DOMAIN is also read by importing
#  it; the renderer renders on import, so it is read by the walk alone.
BANNED = {"globals", "vars", "locals", "setattr", "delattr", "exec", "eval", "compile", "__import__"}


def walk_name(path, name, use_ok):
    tree = ast.parse(io.open(path, encoding="utf-8").read())
    parent = {c: p for p in ast.walk(tree) for c in ast.iter_child_nodes(p)}
    probs = []
    stores = [n for n in ast.walk(tree) if isinstance(n, ast.Name) and n.id == name and isinstance(n.ctx, ast.Store)]
    top = [n for n in tree.body if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)
           and n.targets[0].id == name]
    if len(stores) != 1 or len(top) != 1:
        probs.append("%d stores, %d module-level assignments" % (len(stores), len(top)))
    for n in ast.walk(tree):
        if isinstance(n, ast.Name) and n.id == name and isinstance(n.ctx, ast.Del):
            probs.append("del")
        elif isinstance(n, (ast.Global, ast.Nonlocal)) and name in n.names:
            probs.append("global/nonlocal")
        elif isinstance(n, (ast.Import, ast.ImportFrom)) and any((a.asname or a.name.split(".")[0]) == name for a in n.names):
            probs.append("import alias")
        elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and n.name == name:
            probs.append("def/class")
        elif isinstance(n, ast.ExceptHandler) and n.name == name:
            probs.append("except name")
        elif isinstance(n, ast.arg) and n.arg == name:
            probs.append("parameter")
        elif isinstance(n, (ast.MatchAs, ast.MatchStar)) and n.name == name:
            probs.append("match name")
        elif isinstance(n, ast.Attribute) and n.attr == name and not isinstance(n.ctx, ast.Load):
            probs.append("attribute store")
        elif (isinstance(n, ast.Subscript) and not isinstance(n.ctx, ast.Load) and isinstance(n.slice, ast.Constant)
              and n.slice.value == name):
            probs.append("subscript store keyed by the name")
        elif isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in BANNED:
            probs.append("call to " + n.func.id)
        elif isinstance(n, ast.Attribute) and n.attr in ("__dict__", "__globals__"):
            probs.append(n.attr)
        elif isinstance(n, ast.Name) and n.id == name and isinstance(n.ctx, ast.Load) and not use_ok(n, parent):
            probs.append("a use at line %d" % n.lineno)
    return (ast.literal_eval(top[0].value) if len(top) == 1 else None), probs


def in_compare(n, parent):
    p = parent.get(n)
    return (isinstance(p, ast.Compare) and n in p.comparators
            and isinstance(p.ops[p.comparators.index(n)], (ast.In, ast.NotIn)))


def dom_use(n, parent):
    p = parent.get(n)
    return in_compare(n, parent) or (isinstance(p, ast.Call) and p.args == [n] and isinstance(p.func, ast.Attribute)
                                     and p.func.attr == "join" and isinstance(p.func.value, ast.Constant))


def dcls_use(n, parent):
    p = parent.get(n)
    return in_compare(n, parent) or (isinstance(p, ast.Attribute) and p.attr == "get" and isinstance(parent.get(p), ast.Call)
                                     and parent.get(p).func is p)


dom, dprobs = walk_name(CHECKER, "DOMAIN", dom_use)
dcls, cprobs = walk_name(RENDER, "D_CLASS", dcls_use)
r_imp = subprocess.run([sys.executable, "-c", "import sys; sys.path.insert(0, sys.argv[1]); import check_entry_domain as c; "
                        "print(ascii(c.DOMAIN))", os.path.dirname(DEFAULT_CHECKER)], capture_output=True, text=True)
try:
    eff = ast.literal_eval(r_imp.stdout.strip()) if r_imp.returncode == 0 else None
except (ValueError, SyntaxError):
    eff = None
four = ("✓", "✕", "⏸", "…")
say("C27 ONE binding each and no other way to change it: DOMAIN (and its EFFECTIVE value) and D_CLASS's keys are ✓ ✕ ⏸ …",
    isinstance(dom, tuple) and isinstance(dcls, dict) and sorted(dom) == sorted(four) and sorted(dcls) == sorted(four)
    and not dprobs and not cprobs and isinstance(eff, tuple) and sorted(eff) == sorted(four),
    "DOMAIN %r %s | effective %r | D_CLASS keys %r %s" % (dom, dprobs or "", eff, sorted(dcls) if isinstance(dcls, dict) else dcls,
                                                          cprobs or ""))
rc, out = run_checker(LEDGER, wjson("b_shape.json", [k[:6] + [str(k[6])] for k in base]))
say("C17 a misshapen baseline (counts as strings)", rc == 2, "rc %d" % rc)
#  C17b: one key of count >= 2 split into two rows; the sum must hold (pass 2 fixed last-wins; the adjudication pass found
#  nothing pinned the sum -- GPT-6 Astra and GLM 5.3)
k2 = next(k for k in base if k[6] >= 2)
split = [k for k in base if k is not k2] + [k2[:6] + [1], k2[:6] + [k2[6] - 1]]
rc, out = run_checker(LEDGER, wjson("b_split.json", split))
say("C17b a key split across two baseline rows sums (%s %s %s %s %r x%d)" % (tuple(k2[:5]) + (k2[6],)), rc == 0, "rc %d" % rc)
#  v5: each clause of the baseline row test at its own edge, one misshapen row appended to the shipped baseline -- `len(k) >=
#  7', `isinstance(k[6], int)' (a bool is an int), `k[6] != 0', and the string test narrowed to five fields each passed all 72
#  v4 controls (Fable 5.1, Grok 4.7, GPT-6 Astra, v4 pass)
kx = base[0]
for tag, row_, how in (("c", kx[:6] + [1, "extra"], "eight fields"), ("d", kx[:6] + [True], "a count of true"),
                       ("e", kx[:6] + [-1], "a count of -1"), ("f", kx[:6] + [0], "a count of 0"),
                       ("g", kx[:6] + [1.0], "a count of 1.0"), ("h", [5] + kx[1:6] + [1], "a numeric first field"),
                       ("i", kx[:5] + [5, 1], "a numeric note sha"),
                       #  v6: the MIDDLE positions -- `for v in k[::5]' checked only the first and the sixth and passed all
                       #  96 v5 controls (GPT-6 Astra, v5 pass)
                       ("j", kx[:1] + [5] + kx[2:6] + [1], "a numeric phase"), ("k", kx[:2] + [5] + kx[3:6] + [1], "a numeric seat"),
                       ("l", kx[:3] + [5] + kx[4:6] + [1], "a numeric date"), ("m", kx[:4] + [5] + kx[5:6] + [1], "a numeric d"),
                       #  v6: a None field -- `isinstance(v, (str, type(None)))' passed all 96 v5 controls (Fable 5.1, v5 pass)
                       ("n", kx[:3] + [None] + kx[4:6] + [1], "a None date")):
    rc, out = run_checker(LEDGER, wjson("b_row_%s.json" % tag, base + [row_]))
    tb = any("Traceback" in l for l in out)
    say("C17%s a misshapen baseline row: %s (override)" % (tag, how), rc == 2 and not tb, "rc %d%s" % (rc, " TRACEBACK" if tb else ""))
txt = io.open(BASELINE, encoding="utf-8").read()
lines = txt.split("\n")
lines[1] = lines[1].replace('"y"', '"Y"', 1) if '"y"' in lines[1] else lines[1].replace(", 1]", ", 2]", 1)
rc_mod, out_mod = run_checker(LEDGER, checker=pipe_copy("md5mod", "\n".join(lines)))
rc_same, _ = run_checker(LEDGER, checker=pipe_copy("md5same", txt))
say("C18 md5 pin: one baseline line changed -> 2, unchanged -> 0", rc_mod == 2 and rc_same == 0,
    "changed rc %d, unchanged rc %d" % (rc_mod, rc_same))
#  C18b: the same bytes checked out with CRLF -- what a fresh clone under core.autocrlf=true writes (measured 06a3ffc6 ->
#  89d1d370 raw at the adjudication pass) -- must pass the pin, which folds line endings
rc_crlf, _ = run_checker(LEDGER, checker=pipe_copy("md5crlf", txt.replace("\n", "\r\n")))
say("C18b md5 pin: the baseline checked out with CRLF line endings -> 0", rc_crlf == 0, "rc %d" % rc_crlf)
for lab, obj in (('C21a a misshapen ledger: {"rows": null}', {"rows": None}),
                 ("C21b a misshapen ledger: a row that is not an object", {"rows": [42]}),
                 ("C21c a misshapen ledger: a list, not an object", []),
                 #  each of these walked as EMPTY and passed v3, rc 0 (GPT-6 Astra, v3 pass)
                 ('C21d a misshapen ledger: {"rows": {}}', {"rows": {}}),
                 ("C21e a misshapen ledger: an entry that is a string", {"rows": [{"id": "x", "entries": ["bogus"]}]}),
                 ("C21f a misshapen ledger: entries that are an object", {"rows": [{"id": "x", "entries": {}}]}),
                 #  v5: `rows' ABSENT -- `ledger.get("rows", [])' would walk it as empty (Grok 4.7, GLM 5.3, v4 pass)
                 ("C21i a misshapen ledger: no rows key -- {}", {}),
                 ('C21i a misshapen ledger: no rows key -- {"seats": []}', {"seats": []})):
    rc, out = run_checker(wjson("l_shape_%d.json" % len(res), obj))
    tb = any("Traceback" in l for l in out)
    say(lab, rc == 2 and not tb, "rc %d%s" % (rc, " TRACEBACK" if tb else ""))
rc, out = run_checker(LEDGER, wjson("b_dict.json", {}))
say("C21g a misshapen baseline: an object, not a list (override)", rc == 2, "rc %d" % rc)
#  C21j (v6): a row with NO entries key is an empty row, not a misshapen one -- `r.get("entries")' at either site turns it
#  into rc 2; the shipped ledger kills that today (98 of 912 rows carry no `entries'), so it is rowed in isolation (GLM 5.3,
#  v5 pass)
rc, out = run_checker(wjson("l_noentries.json", {"rows": [{"id": "ctlnoent"}, {"id": "ctlent", "entries": [ans("2026-10-18", d="✓")]}]}))
say("C21j a row with no entries key beside a valid one", rc == 0, "rc %d" % rc)
#  C21h: the shape check passes it, then is_answer raises on a NON-STRING note -- the one input that still reaches the walk's
#  except-arm, so that arm stays a measured rc 2 rather than dead code
rc, out = run_checker(wjson("l_shape_note.json", {"rows": [{"id": "x", "entries": [
    {"phase": "review", "seat": "grok", "date": "2026-10-18", "d": "OK", "note": 5}]}]}))
tb = any("Traceback" in l for l in out)
say("C21h an entry whose note is a number (it raises inside is_answer)", rc == 2 and not tb,
    "rc %d%s" % (rc, " TRACEBACK" if tb else ""))
pj = os.path.join(T, "l_notjson.json")
io.open(pj, "w", encoding="utf-8").write("{ this is not json")
rc, out = run_checker(pj)
tb = any("Traceback" in l for l in out)
say("C23 an unreadable ledger (not JSON)", rc == 2 and not tb, "rc %d%s" % (rc, " TRACEBACK" if tb else ""))

# ------------------------------------------------------------------ the renderer
SEATS = [s["id"] for s in L0["seats"]]
EXPECT = {   # seat -> (entry fields, class, glyph)
    "fable5": ({"d": "✓"}, "ok", "✓"),
    "opus5": ({"d": "OK"}, "legacy", "OK"),
    "codex": ({}, "pend", "…"),
    "agy": ({"d": ""}, "legacy", "?"),
    "grok": ({"d": "HELD", "note": st.HELD + " grok] waiting"}, "hold", "⏸"),
    "kimi": ({"d": "OK", "note": st.NOTSEAT + " a main-loop record"}, "tok", "∅"),
    "glm": ({"d": "✕"}, "bad", "✕"),
    "deepseek": ({"d": "⏸"}, "hold", "⏸"),
    "minimax": ({"d": "N/A"}, "legacy", "N/A"),
}
assert set(EXPECT) == set(SEATS), SEATS
#  the legacy cell's WHOLE tooltip: the class line, the date, the note -- joined and escaped exactly as cell() does.  A prefix
#  check let "(not approval, not a seat failure)" return after the checked words (GPT-6 Astra and GLM 5.3, adjudication pass)
LEGACY_TIP = html.escape("legacy -- verdict unclassified: d = 'OK' is outside ✓ ✕ ⏸ …; read the note for the outcome"
                         " — 2026-10-16 — a renderer control", quote=True)
LEGEND_LINE = ('<span><span class="g" style="color:var(--muted);font-style:italic">OK</span> legacy -- verdict text outside '
               '✓ ✕ ⏸ …, unclassified (read the note; <span class="g" style="color:var(--muted);font-style:italic">?</span> = '
               'an explicit blank)</span>')
REC_NOTE = st.NOTSEAT + " a record beside the answer"
REF_A = {"phase": "research", "seat": "fable5", "date": "2026-10-16", "d": "OK", "note": st.RE_READ + " refused re-read control"}
FX = copy.deepcopy(L0)
ents = []
for s in SEATS:
    e = {"phase": "review", "seat": s, "date": "2026-10-16", "note": "a renderer control"}
    e.update(EXPECT[s][0])
    ents.append(e)
FX["rows"] = [{"id": "ctlrow", "title": "renderer control row", "sev": "LOW", "state": "open", "commits": "", "entries": ents},
              {"id": "ctlesc", "title": "escape control row", "sev": "LOW", "state": "open", "commits": "",
               "entries": [{"phase": "assess", "seat": "fable5", "date": "2026-10-16", "d": "<b>&", "note": "escape control"}]},
              #  a whitespace-only `d` must show `?`, never an invisible glyph (0 such values in the ledger; Fable 5.1,
              #  adjudication pass, measured `{e(d) if d else "?"}` passing every v2 control)
              {"id": "ctlws", "title": "whitespace control row", "sev": "LOW", "state": "open", "commits": "",
               "entries": [{"phase": "assess", "seat": "fable5", "date": "2026-10-16", "d": " ", "note": "whitespace control"},
                           #  a TAB-only d: `.strip(" ")` would keep it invisible (Grok 4.7, v3 pass)
                           {"phase": "assess", "seat": "grok", "date": "2026-10-16", "d": "\t", "note": "tab control"},
                           #  v5: a newline and an NBSP -- `.strip(" \t")' kept both invisible and passed all 72 v4
                           #  controls (Fable 5.1, Grok 4.7, v4 pass)
                           {"phase": "assess", "seat": "opus5", "date": "2026-10-16", "d": "\n", "note": "newline control"},
                           {"phase": "assess", "seat": "codex", "date": "2026-10-16", "d": "\xa0", "note": "nbsp control"}]},
              #  v5: an explicit null d renders legacy with the glyph None -- a renderer that treats null as missing (…) or
              #  skips its class line passed all 72 v4 controls (Fable 5.1, Grok 4.7, GPT-6 Astra, v4 pass)
              {"id": "ctlnull", "title": "null control row", "sev": "LOW", "state": "open", "commits": "",
               "entries": [{"phase": "assess", "seat": "fable5", "date": "2026-10-16", "d": None, "note": "null control"}]},
              #  R1e: an ANSWER with a non-answer RECORD beside it in one cell -- deleting the record line passed every v3
              #  control and drops the note from 32 displayed cells (GPT-6 Astra, v3 pass)
              {"id": "ctlrec", "title": "record control row", "sev": "LOW", "state": "open", "commits": "",
               "entries": [{"phase": "review", "seat": "fable5", "date": "2026-10-16", "d": "OK", "note": "record control answer"},
                           {"phase": "review", "seat": "fable5", "date": "2026-10-16", "note": REC_NOTE}]},
              #  R1f: a legacy answer carrying a stage exemption (a re-read), refused by a LATER answer in its stage
              #  R1h: a PADDED glyph " ✓" is outside the domain and renders legacy (the checker refuses it as off-domain);
              #  `D_CLASS.get(str(d).strip(), ...)` would class it ok (Fable 5.1, v3 pass: caught only as a presence pin)
              {"id": "ctlpad", "title": "padded glyph control row", "sev": "LOW", "state": "open", "commits": "",
               "entries": [{"phase": "assess", "seat": "fable5", "date": "2026-10-16", "d": " ✓", "note": "padded glyph control"},
                           #  v6: the other end -- a renderer reading `str(d).rstrip()' would class it ok (GPT-6 Astra)
                           {"phase": "assess", "seat": "grok", "date": "2026-10-16", "d": "✓ ", "note": "padded trailing control"}]},
              #  v6 (R1o): a legacy answer carrying a grade, a badge and evidence -- with only a date and a note, `tip.insert(-2,
              #  ...)' and `if cls == LEGACY and not ent.get("ev")' each passed all 96 v5 controls, while 649 and 642 of the 670
              #  shipped legacy cells lost the class line (GPT-6 Astra, v5 pass)
              #  v6 (R1q): a legacy answer with NO date and NO note -- its tooltip is the class line alone; `if cls == LEGACY
              #  and tip:' would leave it empty (Fable 5.1, v5 pass: equivalent on the ledger, every off-domain answer has a note)
              {"id": "ctlbare", "title": "bare legacy control row", "sev": "LOW", "state": "open", "commits": "",
               "entries": [{"phase": "assess", "seat": "fable5", "d": "BARE"}]},
              {"id": "ctlopt", "title": "optional fields control row", "sev": "LOW", "state": "open", "commits": "",
               "entries": [{"phase": "assess", "seat": "fable5", "date": "2026-10-16", "d": "OK", "grade": "MANUAL", "b": "A",
                            "ev": "regress/artifacts/x/ctl.txt", "note": "optional fields control"}]},
              {"id": "ctlref", "title": "refused exemption control row", "sev": "LOW", "state": "open", "commits": "",
               "entries": [REF_A, {"phase": "research", "seat": "grok", "date": "2026-10-17", "d": "✓", "note": "a later answer"}]}]
#  v6 (R1w): EVERY whitespace code point alone as d, nine per row (one cell per seat) -- R1d's four were a SAMPLE of the set
#  `str.strip()' removes, and `.strip(" \t\n\xa0")' passed all 96 v5 controls but R3's presence pin (Fable 5.1, v5 pass)
WS = [chr(c) for c in range(0x110000) if chr(c).isspace()]
for i in range(0, len(WS), len(SEATS)):
    FX["rows"].append({"id": "ctlws%02d" % (i // len(SEATS)), "title": "whitespace set control row", "sev": "LOW", "state": "open",
                       "commits": "", "entries": [{"phase": "assess", "seat": SEATS[j], "date": "2026-10-16", "d": ch,
                                                   "note": "ws control U+%04X" % ord(ch)}
                                                  for j, ch in enumerate(WS[i:i + len(SEATS)])]})
fx_path = wjson("fx_render.json", FX)


def render(gen, ledger_path, tag):
    d = os.path.join(T, "r_" + tag)
    os.makedirs(d, exist_ok=True)
    shutil.copy(gen, os.path.join(d, "gen_dashboard.py"))
    shutil.copy(os.path.join(PIPE, "stage_tokens.py"), d)
    out = os.path.join(d, "out.html")
    env = dict(os.environ, GXLEDGER=ledger_path, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, os.path.join(d, "gen_dashboard.py"), "--out", out], capture_output=True, text=True,
                       encoding="utf-8", env=env)
    return io.open(out, encoding="utf-8").read() if r.returncode == 0 and os.path.exists(out) else None


CTL_OTHER = ("escape control", "whitespace control", "record control answer", "refused re-read control", "a later answer",
             "padded glyph control", "tab control", "newline control", "nbsp control", "null control", "padded trailing control",
             "optional fields control", "BARE", "ws control U+")


def cells(html_text):
    got = []
    for m in re.finditer(r'<td class="c ([a-z]+)">(.*?)</td>', html_text, re.S):
        if m.group(1) == "none":
            continue
        g = re.search(r'<span class="g">(.*?)</span>', m.group(2))
        tip = re.search(r'<span class="tip">(.*?)</span>', m.group(2), re.S)
        got.append((m.group(1), g.group(1) if g else None, tip.group(1) if tip else ""))
    return got


def r1(html_text):
    if html_text is None:
        return False, "render FAILED (a crash is not a kill)"
    got = [c for c in cells(html_text) if not any(k in c[2] for k in CTL_OTHER)]   # the control row's nine, in seat order
    want = [(EXPECT[s][1], EXPECT[s][2]) for s in SEATS]
    head = got[:len(want)]
    bad = [(s, g[:2], w) for s, g, w in zip(SEATS, head, want) if (g[0], g[1]) != w]
    legacy_tip = head[SEATS.index("opus5")][2] if len(head) == len(want) else ""
    tip_ok = legacy_tip == LEGACY_TIP
    return (len(head) == len(want) and not bad and tip_ok), ("%d cells; mismatches %s; legacy tip %s" % (
        len(head), bad[:3], "exact" if tip_ok else "WRONG: %r" % legacy_tip[:120]))


def r1b(html_text):
    if html_text is None:
        return False, "render FAILED (a crash is not a kill)"
    got = [c for c in cells(html_text) if "escape control" in c[2]]
    esc = got[0] if got else ("", "", "")
    return (esc[0] == "legacy" and esc[1] == "&lt;b&gt;&amp;"), "escape cell %r" % (esc[:2],)


def r1d(html_text):
    if html_text is None:
        return False, "render FAILED (a crash is not a kill)"
    got = [c for c in cells(html_text) if any(k in c[2] for k in ("whitespace control", "tab control", "newline control",
                                                                    "nbsp control"))]
    return (len(got) == 4 and all(c[0] == "legacy" and c[1] == "?" for c in got)), "whitespace cells %r" % ([c[:2] for c in got],)


def legacy_line(d):
    return "legacy -- verdict unclassified: d = %r is outside ✓ ✕ ⏸ …; read the note for the outcome" % d


def r1g(html_text):
    #  EVERY legacy cell, not only the "OK" one: `if cls == LEGACY` -> `if d == "OK"` passed every v3 control and drops the
    #  explanation from 305 displayed cells (GPT-6 Astra, v3 pass)
    if html_text is None:
        return False, "render FAILED (a crash is not a kill)"
    #  the WHOLE tooltip of each simple legacy cell -- class line, date, note -- not a prefix and not one cell: `if cls ==
    #  LEGACY and d == "OK"` and `... and str(d).strip()` passed all 46 v3 controls (Fable 5.1, v3 pass, measured)
    want = [(note, d, html.escape(" — ".join([legacy_line(d), "2026-10-16", note]), quote=True))
            for note, d in (("a renderer control", "OK"), ("a renderer control", ""), ("a renderer control", "N/A"),
                            ("escape control", "<b>&"), ("whitespace control", " "), ("padded glyph control", " ✓"), ("padded trailing control", "✓ "),
                            ("tab control", "\t"), ("null control", None),
                            #  v6: the newline and NBSP cells -- R1d checked their class and glyph only, so `if cls == LEGACY
                            #  and d not in ("\n", "\xa0")' passed all 96 v5 controls (Grok 4.7, v5 pass)
                            ("newline control", "\n"), ("nbsp control", "\xa0"))]
    legacy = [tip for cls_, g, tip in cells(html_text) if cls_ == "legacy"]
    missing = [(note, d) for note, d, whole in want if whole not in legacy]
    return not missing, "%d legacy cells; no exact tooltip for: %s" % (len(legacy), missing[:3])


def r1e(html_text):
    if html_text is None:
        return False, "render FAILED (a crash is not a kill)"
    got = [c for c in cells(html_text) if "record control answer" in c[2]]
    #  v5: the WHOLE tooltip -- class line, date, note, the record line.  v4 asserted the record substring, so a class line
    #  dropped from every cell with a record beside it passed all 72 v4 controls (Fable 5.1, GPT-6 Astra, v4 pass)
    want = html.escape(" — ".join([legacy_line("OK"), "2026-10-16", "record control answer", "record: 2026-10-16 — " + REC_NOTE]),
                       quote=True)
    return (len(got) == 1 and got[0][0] == "legacy" and got[0][2] == want), "cells %d; tooltip %s" % (
        len(got), "exact" if got and got[0][2] == want else "WRONG: %r" % (got[0][2][:140] if got else ""))


def r1f(html_text):
    if html_text is None:
        return False, "render FAILED (a crash is not a kill)"
    stage = [REF_A, {"phase": "research", "seat": "grok", "date": "2026-10-17", "d": "✓", "note": "a later answer"}]
    probs = st.stage_token_problems(stage)
    want = html.escape(" — ".join(["EXEMPTION REFUSED BY SECTION H: " + "; ".join(probs), legacy_line("OK"), "2026-10-16",
                                   REF_A["note"]]), quote=True)
    got = [c for c in cells(html_text) if "refused re-read control" in c[2]]
    return (bool(probs) and len(got) == 1 and got[0][2] == want), "refusals %d; cells %d; tooltip %s" % (
        len(probs), len(got), "exact" if got and got[0][2] == want else "WRONG: %r" % (got[0][2][:120] if got else ""))


ha_fx = render(RENDER, fx_path, "after")
ok, det = r1(ha_fx); say("R1 fixture row: class, glyph and the legacy tooltip EXACTLY, per seat", ok, det)
ok, det = r1g(ha_fx); say("R1g every simple legacy cell's WHOLE tooltip, the class line for ITS d", ok, det)
#  v6: both ends, and the glyph TEXT -- `html.escape(str(t).strip())' showed " ✓" as "✓" and passed all 96 v5 controls,
#  which read only the class (GPT-6 Astra, v5 pass)
pad = [c for c in cells(ha_fx or "") if "padded glyph control" in c[2]]
padt = [c for c in cells(ha_fx or "") if "padded trailing control" in c[2]]
say("R1h a ✓ padded at either end renders legacy, its glyph text exactly as written",
    len(pad) == 1 and pad[0][:2] == ("legacy", " ✓") and len(padt) == 1 and padt[0][:2] == ("legacy", "✓ "),
    "cells %r %r" % (pad[0][:2] if pad else None, padt[0][:2] if padt else None))
opt = [c for c in cells(ha_fx or "") if "optional fields control" in c[2]]
want_o = html.escape(" — ".join([legacy_line("OK"), "2026-10-16", "MANUAL", "the author did this review (shown, not hidden)",
                                  "optional fields control", "evidence: regress/artifacts/x/ctl.txt"]), quote=True)
say("R1o a legacy answer with a grade, a badge and evidence: its WHOLE tooltip, the class line first",
    len(opt) == 1 and opt[0][0] == "legacy" and opt[0][2] == want_o,
    "cell %r; tooltip %s" % (opt[0][:2] if opt else None, "exact" if opt and opt[0][2] == want_o else "WRONG: %r" % (opt[0][2][:140] if opt else "")))
#  R1p (v6): the class line ONLY on a legacy cell -- `if cls in (LEGACY, "pend")' and `if cls != "ok"' each passed all 96 v5
#  controls, putting the FALSE line "d = '…' is outside ✓ ✕ ⏸ …" on every pend cell, 833 on HEAD's ledger (Fable 5.1, v5 pass)
plain = html.escape("2026-10-16 — a renderer control", quote=True)
ctl = [c for c in cells(ha_fx or "") if not any(k in c[2] for k in CTL_OTHER)][:len(SEATS)]
tips = dict(zip(SEATS, [c[2] for c in ctl])) if len(ctl) == len(SEATS) else {}
bad_p = [s for s in ("fable5", "codex", "glm", "deepseek") if tips.get(s) != plain]
say("R1p the NON-legacy answer cells -- ok, pend, bad, hold -- carry no class line: the date and the note alone",
    bool(tips) and not bad_p, "wrong: %r" % ([(s, (tips.get(s) or "")[:70]) for s in bad_p],))
bare = [c for c in cells(ha_fx or "") if "BARE" in c[2]]
want_b = html.escape(legacy_line("BARE"), quote=True)
say("R1q a legacy answer with neither date nor note: its tooltip is the class line alone",
    len(bare) == 1 and bare[0][0] == "legacy" and bare[0][2] == want_b, "cells %d: %r" % (len(bare), [c[2][:80] for c in bare]))
wsc = [c for c in cells(ha_fx or "") if "ws control U+" in c[2]]
wsw = {html.escape(" — ".join([legacy_line(ch), "2026-10-16", "ws control U+%04X" % ord(ch)]), quote=True) for ch in WS}
wsbad = [c[2][-14:] for c in wsc if c[0] != "legacy" or c[1] != "?" or c[2] not in wsw]
say("R1w every str.isspace() code point alone as d (%d) shows ? and renders legacy, each with its WHOLE tooltip" % len(WS),
    len(wsc) == len(WS) == 29 and not wsbad and len({c[2] for c in wsc}) == 29,
    "%d cells of %d; wrong: %r" % (len(wsc), len(WS), wsbad[:5]))
ok, det = r1e(ha_fx); say("R1e an answer with a record beside it: its WHOLE tooltip", ok, det)
nul = [c for c in cells(ha_fx or "") if "null control" in c[2]]
say("R1n an explicit null d renders legacy with the glyph None", len(nul) == 1 and nul[0][:2] == ("legacy", "None"),
    "cell %r" % (nul[0][:2],) if nul else "render FAILED or no cell")
ok, det = r1f(ha_fx); say("R1f a refused exemption's line first, then the class line, exactly", ok, det)
ok, det = r1b(ha_fx); say("R1b an escapable d renders escaped", ok, det)
ok, det = r1d(ha_fx); say("R1d a whitespace-only d -- a space, a tab, a newline, an NBSP -- shows ?", ok, det)
low = (ha_fx or "").lower()
hits = [p for p in ("not approval", "not a seat failure") if p in low]
say("R1c the fixture page says neither 'not approval' nor 'not a seat failure'", ha_fx is not None and not hits,
    "render %s; found %s" % ("ok" if ha_fx is not None else "FAILED", hits or "none"))
leg = re.search(r'<div class="legend">(.*?)</div>', ha_fx or "", re.S)
say("R4 the legend carries the legacy line EXACTLY", bool(leg) and LEGEND_LINE in leg.group(1),
    "legend %s" % ("found" if leg else "MISSING"))
#  R5 (v5): the two CSS rules the class adds -- `font-size:0' made every legacy glyph invisible and passed all 72 v4 controls
#  (GPT-6 Astra, Fable 5.1, v4 pass)
CSS = ("td.c.legacy { outline:1px dashed var(--line); outline-offset:-3px; }",
       ".c.legacy .g { color:var(--muted); font-style:italic; font-size:11px; }")
#  v6: and they are the ONLY rules in the style block naming `legacy' -- a later `.c.legacy .g { font-size:0; }' left both
#  present and hid every legacy glyph (GPT-6 Astra, v5 pass)
sty = re.search(r"<style>(.*?)</style>", ha_fx or "", re.S)
leg_rules = [" ".join(m.group(0).split()) for m in re.finditer(r"[^{}]*legacy[^{}]*\{[^{}]*\}", sty.group(1) if sty else "")]
say("R5 the page carries the legacy class's two CSS rules EXACTLY, and no other rule names it",
    ha_fx is not None and all(c in ha_fx for c in CSS) and sorted(leg_rules) == sorted(CSS),
    "missing %r; legacy rules %d %r" % ([c[:30] for c in CSS if c not in (ha_fx or "")], len(leg_rules), [r[:40] for r in leg_rules]))


def census(html_text):
    c = collections.Counter(m.group(1) for m in re.finditer(r'<td class="c ([a-z]+)"', html_text))
    s = re.search(r'<span class="k">entries</span><b>([^<]*)</b>', html_text).group(1)
    return c, s


hb, ha = render(BEFORE, LEDGER, "before_real"), render(RENDER, LEDGER, "after_real")
#  v6: guarded -- a renderer that crashes on the shipped ledger made census() raise, so the controls died with no tally and no
#  sentinel and the mutant driver scored a KILL as INCOMPLETE (Fable 5.1, v5 pass); now R2 says NO and the run completes
cb, sb = census(hb) if hb else (collections.Counter(), "")
ca, sa = census(ha) if ha else (collections.Counter(), "")
same = all(cb[k] == ca[k] for k in ("ok", "hold", "bad", "tok", "none"))
moved = cb["pend"] - ca["pend"] == ca["legacy"] and ca["legacy"] > 0
nums = [int(x) for x in re.findall(r"(\d+)", sa)]
n_entries = sum(len(r.get("entries", [])) for r in L0["rows"])
n_legacy = sum(1 for r in L0["rows"] for x in r.get("entries", []) if "d" in x and x["d"] not in ("✓", "✕", "⏸", "…"))
#  the strip's FIFTH number is checked against the ledger itself: a renderer that folded legacy into … still summed (the
#  kill table measured R2 blind to that on its first run)
cnt = collections.Counter()
for r_ in L0["rows"]:
    for x in r_.get("entries", []):
        d_ = x.get("d", "…")
        cnt[d_ if d_ in ("✓", "✕", "⏸", "…") else "legacy"] += 1
#  EACH number against the ledger's own count: the v3 form checked only the total and the legacy number, so folding every
#  canonical glyph into ✓ passed (GPT-6 Astra, v3 pass)
sums = nums == [cnt["✓"], cnt["✕"], cnt["⏸"], cnt["…"], cnt["legacy"], n_entries] and nums[4] == n_legacy
#  v5: the WHOLE strip string -- its labels too: "1397 approved" passed all 72 v4 controls (GPT-6 Astra, v4 pass)
def strip_text(c, total):
    return "%d✓ %d✕ %d⏸ %d… %d legacy · %d in all" % (c["✓"], c["✕"], c["⏸"], c["…"], c["legacy"], total)


label_ok = sa == strip_text(cnt, n_entries)
say("R2 shipped ledger BEFORE vs AFTER: only pend -> legacy; the strip string EXACTLY (each number, its label)",
    same and moved and sums and label_ok,
    "before %s | after %s | strip '%s' | ledger %d entries, %d off-domain" % (dict(sorted(cb.items())), dict(sorted(ca.items())),
                                                                          sa, n_entries, n_legacy))
#  R2b (v5): the FIXTURE page's strip against the fixture's own counts, by exact membership -- its padded " ✓" and its null
#  count legacy.  R2 recomputes on the shipped ledger, which holds no padded glyph, so counting " ✓" as ✓ passed all 72 v4
#  controls (Fable 5.1, Grok 4.7, v4 pass)
cfx = collections.Counter()
for r_ in FX["rows"]:
    for x in r_.get("entries", []):
        d_ = x.get("d", "…")
        cfx[d_ if d_ in ("✓", "✕", "⏸", "…") else "legacy"] += 1
_, sfx = census(ha_fx) if ha_fx else (None, "")
want_fx = strip_text(cfx, sum(len(r_.get("entries", [])) for r_ in FX["rows"]))
say("R2b the FIXTURE page's strip EXACTLY, by exact membership (padded and null count legacy)", sfx == want_fx,
    "strip %r, want %r" % (sfx, want_fx))
src_r = io.open(RENDER, encoding="utf-8").read()
for tag, find, repl, check in (
        ("ok", "cls = D_CLASS.get(d, LEGACY)", 'cls = D_CLASS.get(d, "ok")', r1),
        ("pend", "cls = D_CLASS.get(d, LEGACY)", 'cls = D_CLASS.get(d, "pend")', r1),
        ("noescape", '{e(d) if str(d).strip() else "?"}', '{d if str(d).strip() else "?"}', r1b)):
    if src_r.count(find) != 1:
        say("R3 MUTANT %s: find-text present" % tag, False, "MUTANT TEXT NOT FOUND"); continue
    m = os.path.join(T, "gen_mut_%s.py" % tag)
    io.open(m, "w", encoding="utf-8").write(src_r.replace(find, repl))
    h = render(m, fx_path, "mut_" + tag)
    ok, det = check(h)
    say("R3 MUTANT %s renders and fails its check" % tag, h is not None and not ok, det)

# ------------------------------------------------------------------ the wiring: precommit section Q2, failures counted
BASH = os.environ.get("BASH_EXE") or r"C:\Program Files\Git\bin\bash.exe"
txt_pre = io.open(PRE, encoding="utf-8").read()
a, b = txt_pre.find('say ""; say "Q2.'), txt_pre.find("#  ---- R ----")
if a < 0 or b < a or not os.path.exists(BASH):
    say("W0 precommit Q2 block extracted and a git-bash found", False, "a=%d b=%d bash=%s" % (a, b, BASH))
else:
    blk = os.path.join(T, "q2_block.sh")
    io.open(blk, "w", encoding="utf-8", newline="\n").write(
        'say () { :; }\nfails=0\ngood () { echo "GOOD $*"; }\nbad () { echo "BAD $*"; fails=$((fails + 1)); }\n'
        '_HERE="$1"\n' + txt_pre[a:b] + '\necho "FAILURES $fails"\n')
    def w_tools(tag, ledger_path, baseline_text=None, nochecker=False, stub=None):
        """a fake tools/ dir: the block's own _HERE, holding the checker under test, the FIXTURE ledger as the default ledger
        and a baseline -- the block strips GXLEDGER / GXDOMAIN_BASELINE, so fixtures can only enter this way"""
        d = os.path.join(T, "w_" + tag)
        os.makedirs(os.path.join(d, "pipeline"), exist_ok=True)
        if stub is not None:
            io.open(os.path.join(d, "pipeline", "check_entry_domain.py"), "w", encoding="utf-8").write(stub)
        elif not nochecker:
            shutil.copy(CHECKER, os.path.join(d, "pipeline", "check_entry_domain.py"))
        shutil.copy(os.path.join(PIPE, "stage_tokens.py"), os.path.join(d, "pipeline"))
        shutil.copy(ledger_path, os.path.join(d, "pipeline", "ledger.json"))
        if baseline_text is None:
            shutil.copy(BASELINE, os.path.join(d, "pipeline", "entry_domain_baseline.json"))
        elif baseline_text != "<absent>":
            io.open(os.path.join(d, "pipeline", "entry_domain_baseline.json"), "w", encoding="utf-8").write(baseline_text)
        return d
    #  dated BEFORE the cutoff, so only the BASELINE decides W4: a post-cutoff entry is refused by the date rule whichever
    #  baseline is read, and the kill table measured W4 blind to the un-stripped override on its first run for that reason
    new_led = with_entries([(ROW0, ans("2026-10-10", d="OK", seat="deepseek", note="W new off-domain"))])
    permissive = wjson("b_permissive.json", base + [ident(ROW0, ans("2026-10-10", d="OK", seat="deepseek",
                                                                      note="W new off-domain")) + [1]])
    #  the FIRST LINE names which branch fired: W2 the rc-1 refusal, W3 the rc-2 apparatus line -- `-eq 1` -> `-eq 7` and a
    #  rewritten message each passed every v2 control, which tested only the BAD prefix and the counter (Fable 5.1,
    #  adjudication pass)
    for lab, tools, envx, want, wantf, msg in (
            ("W1 Q2 on the shipped ledger", w_tools("1", LEDGER), {}, "GOOD", 0, "within the frozen ceiling"),
            ("W2 Q2 with a new off-domain answer", w_tools("2", new_led), {}, "BAD", 1, "beyond the frozen legacy ceiling"),
            ("W3 Q2 with the baseline absent (rc 2 path)", w_tools("3", LEDGER, "<absent>"), {}, "BAD", 1,
             "could not run (rc 2)"),
            ("W4 Q2 ignores an exported GXDOMAIN_BASELINE that would admit the entry", w_tools("4", new_led),
             {"GXDOMAIN_BASELINE": permissive}, "BAD", 1, "beyond the frozen legacy ceiling"),
            #  the bad ledger is the block's DEFAULT; the exported GXLEDGER names the clean shipped one, so only the strip
            #  decides W5 (deleting `-u GXLEDGER` passed all 35 v2 controls -- GPT-6 Astra, adjudication pass)
            ("W5 Q2 ignores an exported GXLEDGER naming a clean ledger", w_tools("5", new_led), {"GXLEDGER": LEDGER},
             "BAD", 1, "beyond the frozen legacy ceiling"),
            #  the checker ABSENT: the missing-file branch was exercised by no v3 row, so `bad` -> `good` there passed
            #  (GPT-6 Astra, v3 pass)
            ("W6 Q2 with the checker absent", w_tools("6", LEDGER, nochecker=True), {}, "BAD", 1, "MISSING"),
            #  v5: ANY status other than 0 and 1 is "could not run" -- `else' narrowed to `elif [ $_cedrc -eq 2 ]' passed all 72
            #  v4 controls, leaving rc 7 or 127 silently green (GPT-6 Astra, Fable 5.1, v4 pass).  W7's message is on STDERR,
            #  which the section captures with 2>&1; W8 is a real launch failure: python is not on the PATH it is given -- and
            #  the git-bash wrapper PREPENDS /mingw64/bin, /usr/bin and ~/bin to that PATH; none holds a python on this
            #  machine, and if one did W8 would fail LOUDLY (GOOD instead of BAD), never pass falsely (Fable 5.1, v5 pass)
            ("W7 Q2 with a checker that exits 7, its message on stderr",
             w_tools("7", LEDGER, stub='import sys\nsys.stderr.write("STUB FIRST LINE\\nSTUB SECOND LINE\\n")\nsys.exit(7)\n'), {},
             "BAD", 1, "could not run (rc 7): STUB FIRST LINE"),
            ("W8 Q2 with python absent from PATH (rc 127)", w_tools("8", LEDGER),
             {"PATH": os.path.join(os.path.dirname(os.path.dirname(BASH)), "usr", "bin")}, "BAD", 1, "could not run (rc 127)")):
        env = dict(os.environ)
        for k in ("GXLEDGER", "GXDOMAIN_BASELINE", "PYTHONIOENCODING", "PYTHONUTF8"):
            env.pop(k, None)
        env.update(envx)
        r = subprocess.run([BASH, blk.replace("\\", "/"), tools.replace("\\", "/")], capture_output=True, env=env)
        outl = r.stdout.decode("cp1252", "replace").strip().splitlines()
        firstl = outl[0] if outl else ""
        fl = [l for l in outl if l.startswith("FAILURES ")]
        nf = int(fl[-1].split()[1]) if fl else -1
        #  W2's refusal must also NAME the entry to the committer: deleting Q2's `printf | sed` passed every v3 control, which
        #  read only the first line and the counter (Grok 4.7, v3 pass)
        named = (not lab.startswith("W2 ")) or any(l.strip().startswith("OFF-DOMAIN ANSWER  row") for l in outl)
        #  v6: W1 and W7 read the WHOLE output -- the apparatus branch's `head -1' -> `tail -1' passed all 96 v5 controls on
        #  one-line messages (GPT-6 Astra, v5 pass)
        whole = {"W1": ["GOOD " + summary_line(N_OFF, N_OFF, N_OFF), "FAILURES 0"],
                 "W7": ["BAD check_entry_domain.py could not run (rc 7): STUB FIRST LINE", "FAILURES 1"]}.get(lab.split()[0])
        #  v6: W2's WHOLE output -- its first line, then EVERY line of the checker's own output, indented, then the counter:
        #  Q2's `printf | sed' replaced by a constant "OFF-DOMAIN ANSWER  row ..." line passed all 96 v5 controls, which read a
        #  prefix (Grok 4.7, v5 pass).  The checker's lines come from running the checker in W2's own tools dir as Q2 does.
        if lab.split()[0] == "W2":
            e2 = subprocess.run([sys.executable, os.path.join(tools, "pipeline", "check_entry_domain.py")],
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
            whole = (["BAD an off-domain ledger answer is beyond the frozen legacy ceiling (a new one, a copy, or an old one "
                      "edited):"] + ["          " + l for l in e2.stdout.decode("cp1252", "replace").splitlines()] + ["FAILURES 1"])
        named = named and (whole is None or outl == whole)
        #  v6: W2's first line EXACT -- its parenthetical dropped passed all 96 v5 controls (Fable 5.1, v5 pass)
        named = named and (lab.split()[0] != "W2" or firstl == "BAD an off-domain ledger answer is beyond the frozen legacy ceiling "
                                                           "(a new one, a copy, or an old one edited):")
        ok = firstl.startswith(want + " ") and msg in firstl and ((nf == 0) if wantf == 0 else (nf >= 1)) and named
        say(lab, ok, "%s | failures %d" % (firstl[:90], nf))
    #  W9 (v6): EVERY status but 0 and 1 is "could not run".  The else partition is {2..255}, EXHAUSTED in ONE bash loop over
    #  a stub that exits $W9RC: `else' -> `elif [ $_cedrc -ne 3 ]' passed all 96 v5 controls, whose W3, W7 and W8 are three
    #  statuses of 254 (Grok 4.7, v5 pass)
    w9 = w_tools("9", LEDGER, stub='import os, sys\nsys.stderr.write("STUB rc %s\\n" % os.environ["W9RC"])\n'
                                   'sys.exit(int(os.environ["W9RC"]))\n')
    loop = os.path.join(T, "q2_loop.sh")
    io.open(loop, "w", encoding="utf-8", newline="\n").write(
        'say () { :; }\ngood () { echo "GOOD $*"; }\nbad () { echo "BAD $*"; fails=$((fails + 1)); }\n_HERE="$1"\n'
        'for W9RC in $(seq 2 255); do export W9RC; fails=0; echo "RC $W9RC"\n' + txt_pre[a:b] + '\necho "FAILURES $fails"\ndone\n')
    env = dict(os.environ)
    for k in ("GXLEDGER", "GXDOMAIN_BASELINE", "PYTHONIOENCODING", "PYTHONUTF8"):
        env.pop(k, None)
    r = subprocess.run([BASH, loop.replace("\\", "/"), w9.replace("\\", "/")], capture_output=True, env=env)
    got9 = r.stdout.decode("cp1252", "replace").splitlines()
    want9 = []
    for n_ in range(2, 256):
        want9 += ["RC %d" % n_, "BAD check_entry_domain.py could not run (rc %d): STUB rc %d" % (n_, n_), "FAILURES 1"]
    bad9 = ([n_ for n_ in range(2, 256) if got9[3 * (n_ - 2):3 * (n_ - 1)] != want9[3 * (n_ - 2):3 * (n_ - 1)]]
            if len(got9) == len(want9) else ["%d lines of %d" % (len(got9), len(want9))])
    say("W9 Q2 with EVERY status 2-255 (254 runs of one stub): each exactly BAD 'could not run (rc N)' with its first line, "
        "the counter 1", got9 == want9, "wrong at: %r" % (bad9[:8],))

shutil.rmtree(T, ignore_errors=True)
print("DASHOKCLASS CONTROLS: %d/%d as expected" % (sum(res), len(res)))
print("DASHOKCLASS_CONTROLS_DONE")
sys.exit(0 if all(res) else 1)
