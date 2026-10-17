#!/usr/bin/env python3
"""Controls for `dashokclass` (2026-10-17, v4 after the v3 pass -- the CLASS CLOSURE): gen_dashboard.py's LEGACY class,
check_entry_domain.py (a ceiling over selected content, md5-pinned baseline) and its precommit section Q2.  Everything runs on
temp copies and fixture ledgers; nothing in the tree is written.  Exit 0 only if every control holds.  CTL_CHECKER /
CTL_RENDER / CTL_PRECOMMIT override the three files under test (run_mutants_v3.py and the staged runs use them); the defaults
are the tree's.

  THE CONTRACT (v4) -- the v3 pass (GPT-6 Astra) found five more one-edit survivors of the 46 v3 controls, the same class as the
  adjudication pass's, so v4 closes the class: each decision below is pinned at its edges, or DISCLOSED with its reason.
    checker  ledger shape (object, rows list, row objects, entries lists, entry objects)   C21a-f      (and C23: not JSON)
             baseline shape (a list of [6 strings, positive int])                         C13, C17, C21g; C17b sums a split key
             md5 pin on the default path, CRLF folded; overrides skip it                   C18, C18b; C11, C12, C17 (override)
             the selection: explicit d, outside the four, an ANSWER                        C7 (no d), C14 (blank), C2/C2b/C2c/C2d
                                                                                          (each glyph, C2c/C2d in a ledger holding
                                                                                          only their entry), C8 (hold), C24 (record)
             the key -- each of row, phase, seat, date, d, note -- byte for byte          C25a-k: a suffix, a trailing space, a case
                                                                                          change, a row move; C15/C16 (the note)
             the ceiling: a copy fails, a converted entry's allowance cannot be refilled  C9, C10, C15; d_nonote2 (design mutant)
             the cutoff: inclusive, ISO-shaped dates only                                  C3, C4, C12 (isolated), C19a/b
             output: cp1252-safe, the reason named, every refusal named                    C20, C19, C11
    renderer the class: explicit d outside the four -> legacy, on the answer a cell shows  R1 (per seat), R3
             the class line opens EVERY legacy cell's tooltip, exactly                    R1 (whole tooltip, OK), R1g (every legacy
                                                                                          d), R1c (no denial anywhere)
             a refused exemption's line comes first; a record's note is kept              R1f, R1e
             the glyph: escaped; `?` for a blank or whitespace d                          R1b, R1d
             the strip: each of the five numbers is the ledger's own count                R2
             the legend line                                                              R4
    Q2       the branches: rc 0 GOOD, rc 1 BAD with the refusal, else BAD "could not run"  W1, W2, W3 (first-line words)
             the checker absent -> BAD                                                     W6
             exported GXDOMAIN_BASELINE / GXLEDGER stripped                                W4, W5
    DISCLOSED: a sha1-16 collision of two notes (2^64 work); `k[6] > 0` -> `>= 0` (a zero count adds nothing: equivalent);
    case-folding or whitespace-stripping INSIDE a field rather than at its ends (C25 edits the ends); the production good/bad
    reporters and final exit (the W rows use counting stand-ins; correct by inspection).  A fold of d or a fold or strip of the
    NOTE is one-sided on this ledger -- the baseline holds raw values and only the note's sha -- so it dies on C1 (measured,
    the first v4 table); the coherent fold of d is the two-edit design mutant d_dfold2, killed by C25d.

  CHECKER (Astra's four conditions, the ruling's grandfathering amendment, pass 2's and the adjudication pass's findings):
    C1   shipped ledger, shipped baseline (the md5 pin is checked on the default path)             -> 0, all within the ceiling
    C2   an answer ON the cutoff with a valid glyph (positive)                                      -> 0
    C2b  an answer AFTER the cutoff with a valid glyph (positive)                                   -> 0
    C2c  / C2d  an answer after the cutoff with ⏸ / with …, in a ledger holding ONLY that entry (positive) -> 0 / 0
    C3   an answer ON the cutoff with "OK" (inclusive)                                              -> 1
    C4   an answer AFTER the cutoff with "OK"                                                       -> 1
    C5   a new answer dated BEFORE the cutoff with "OK" (back-dated)                                -> 1
    C6   an UNDATED answer with "N/A"                                                               -> 1
    C7   an answer after the cutoff with NO `d`                                                     -> 0
    C8   a HELD marker after the cutoff with d "HELD" (not an answer)                               -> 0
    C9   an identical copy of a frozen entry                                                        -> 1
    C10  a frozen entry rewritten to a glyph (the population shrinks)                               -> 0
    C11  the baseline emptied (override): every one of the shipped off-domain answers is named      -> 1
    C12  the cutoff ISOLATED: a fixture baseline holding an identity dated before / on / after it   -> 0 / 1 / 1
    C13  an unreadable baseline (override)                                                          -> 2
    C14  a new answer with an explicit BLANK d (blank is off-domain; only a MISSING d is …)         -> 1
    C15  REFILL: a frozen entry rewritten to a glyph, plus a new answer reusing its (row, phase, seat,
         date, d) with another note -- the per-tuple count let this through on pass 2                -> 1
    C16  a frozen entry's NOTE edited, its d left off-domain (editing means normalising)            -> 1
    C17  a misshapen baseline (override; counts as strings)                                         -> 2
    C17b a key SPLIT across two baseline rows (override) must sum -- the loader once kept the last  -> 0
    C18  the md5 PIN: a temp copy of the pipeline with one baseline line changed -> 2; unchanged -> 0
    C18b the same baseline with CRLF line endings (a fresh clone under core.autocrlf=true) passes the pin -> 0
    C19  malformed dates on new answers: "10/18/2026" and a number -- rc 1, never a traceback, and the
         output NAMES the date as not ISO                                                         -> 1 / 1
    C20  a new answer whose d is non-ASCII, under the precommit's cp1252 pipe -- rc 1, no traceback   -> 1
    C21  misshapen LEDGERS -- {"rows": null}, a row that is not an object, a list, {"rows": {}}, a string entry, entries
         that are an object -- rc 2, no traceback; C21g a baseline that is an object (override); C21h a note that is
         a number (it raises inside stage_tokens.is_answer -- the walk's except-arm)            -> 2 each
    C23  a ledger that is not JSON                                                              -> 2
    C24  a non-answer RECORD (NOTSEAT) after the cutoff with d "OK" (condition 2's other half)  -> 0
    C26  a new answer with an explicit "d": null (present, off-domain -- not "missing")         -> 1
    C25  a frozen entry with ONE key field edited by its least visible change -- date suffixed / trailing space,
         d trailing space / case, note trailing space / case, seat trailing space / case, phase trailing space / case,
         the entry moved to another row                                                         -> 1 each
    C22  a frozen entry's `ev` edited -- outside the six fields (positive)                          -> 0
  RENDERER:
    R1   a fixture row, one entry per seat: class AND glyph per cell (the record cell's glyph included), and the
         legacy cell's tooltip EXACTLY (the whole string, not a prefix)
    R1b  an escapable `d` ("<b>&") renders escaped
    R1c  the fixture page says neither "not approval" nor "not a seat failure" anywhere
    R1d  a whitespace-only `d` (" ") shows `?`
    R1g  EVERY simple legacy cell's WHOLE tooltip -- the class line for ITS d ("OK", "", "N/A", "<b>&", " ", " ✓"), the date,
         the note
    R1h  a padded glyph " ✓" renders legacy, not ok
    C27  the glyph SET, read from both files' literals: DOMAIN and D_CLASS's keys are exactly ✓ ✕ ⏸ …
    R1e  an answer cell with a non-answer record beside it keeps the record's note in its tooltip
    R1f  a legacy answer carrying a refused stage exemption: the refusal line first, then the class line
    R2   the shipped ledger, BEFORE vs AFTER: only pend -> legacy moves; EACH of the strip's five numbers is the ledger's own
         count of that class (the v3 form checked the total and the legacy number, so folding every glyph into ✓ passed)
    R4   the legend carries the legacy line EXACTLY
    R3   MUTANT renderers (fallback -> ok, -> pend; the escape dropped) must RENDER and then fail R1 / R1b -- a crash
         is not a kill
  WIRING (section Q2, extracted from precommit_check.sh and run with reporters that COUNT failures -- stand-ins for the
  production good/bad and its final exit, which are correct by inspection and not executed here; each first line must also
  carry its BRANCH's own words):
    W1   the shipped ledger                    -> GOOD, failures 0
    W2   a new off-domain answer               -> BAD "beyond the frozen legacy ceiling", failures >= 1
    W3   the baseline absent (rc 2 path)       -> BAD "could not run (rc 2)", failures >= 1
    W4   an exported GXDOMAIN_BASELINE that would admit a new entry is IGNORED -> BAD, failures >= 1
    W5   an exported GXLEDGER naming a CLEAN ledger is IGNORED; the bad default ledger is read -> BAD, failures >= 1
    W6   the checker ABSENT from the fake tools dir                -> BAD "MISSING", failures >= 1
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


def ident(row, e):
    return [row, e.get("phase") or "", e.get("seat") or "", e.get("date") if isinstance(e.get("date"), str) else "",
            str(e["d"]), hashlib.sha1(str(e.get("note") or "").encode("utf-8")).hexdigest()[:16]]


print("# dashokclass controls (v4) -- checker %s | renderer %s | precommit %s | baseline %s"
      % (hashlib.md5(open(CHECKER, "rb").read()).hexdigest()[:8], hashlib.md5(open(RENDER, "rb").read()).hexdigest()[:8],
         hashlib.md5(open(PRE, "rb").read()).hexdigest()[:8], hashlib.md5(open(BASELINE, "rb").read()).hexdigest()[:8]))
# ------------------------------------------------------------------ the checker
rc, out = run_checker(LEDGER)
first = out[0] if out else ""
#  the summary's BASELINE number too: `sum(base.values())` -> `len(base)` printed 1,342 and passed every v3 control (Grok 4.7,
#  v3 pass) -- the count of frozen answers is 1,356 over 1,342 keys
say("C1 shipped ledger, shipped baseline, md5 pin live", rc == 0 and ("%d within the frozen ceiling (baseline %d)" % (N_OFF, N_OFF))
    in first, "rc %d: %s" % (rc, first))
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
    ("C24 a non-answer RECORD (NOTSEAT) after the cutoff, d OK", ans("2026-10-18", d="OK", note=st.NOTSEAT + " a main-loop record"), 0),
    #  an explicit "d": null is PRESENT and off-domain -- `if x.get("d") is None` would treat it as missing (Fable 5.1, v3 pass)
    ("C26 a new answer with an explicit null d", ans("2026-10-10", d=None), 1),
]:
    rc, out = run_checker(with_entries([(ROW0, ent)]))
    tb = any("Traceback" in l for l in out)
    #  a malformed date must be NAMED in the reason, not only refused: v1's lexical `t[3] >= CUTOFF` and a deleted suffix each
    #  passed every v2 control while calling a numeric date "on or after the cutoff" (Fable 5.1, adjudication pass)
    why = (not lab.startswith("C19")) or any("its date is not ISO" in l for l in out)
    say(lab, rc == want and not tb and why, "rc %d (want %d)%s%s" % (rc, want, " TRACEBACK" if tb else "",
                                                                    "" if why else " REASON NOT NAMED"))
#  C2c/C2d ISOLATED (GPT-6 Astra, v3 pass): the shipped ledger already carries 21 ⏸ and 35 … answers, so dropping either glyph
#  from DOMAIN reddened the v3 rows without their own entry; a ledger holding ONLY the fixture entry makes each its own witness
for lab, ent in (("C2c AFTER the cutoff, d ⏸, in a ledger holding only it (positive)", ans("2026-10-18", d="⏸")),
                 ("C2d AFTER the cutoff, d …, in a ledger holding only it (positive)", ans("2026-10-18", d="…"))):
    rc, out = run_checker(wjson("l_iso_%d.json" % len(res), {"rows": [{"id": "ctliso", "entries": [ent]}]}))
    say(lab, rc == 0, "rc %d" % rc)
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
say("C9 an identical copy of a frozen entry (%s %s %s %s %r)" % tuple(k0[:5]), rc == 1, "rc %d" % rc)
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
rc, out = run_checker(LEDGER, wjson("b_empty.json", []))
nb = sum(1 for l in out if "OFF-DOMAIN ANSWER" in l)
#  and the SUMMARY line on this dirty ledger: it was pinned only on the clean one, where "passes" and "entries" agree, so
#  printing len(cur) for both passed every v3 control (GLM 5.3, v3 pass)
s11 = "%d off-domain answer entries; 0 within the frozen ceiling (baseline 0)" % N_OFF
f11 = out[0] if out else ""
hint = any("give each a `d` from" in l for l in out)      # the instruction line (Fable 5.1, v3 pass: no control asserted it)
say("C11 baseline emptied: every shipped off-domain answer named, the summary counts 0 within the ceiling, the hint printed",
    rc == 1 and nb == N_OFF and s11 in f11 and hint, "rc %d, %d of %d named; summary %s; hint %s"
    % (rc, nb, N_OFF, "ok" if s11 in f11 else repr(f11[:90]), "ok" if hint else "MISSING"))
# C12: the cutoff test isolated -- each fixture entry IS in its fixture baseline, so only the date can refuse it
#  and FAR after: a two-day membership test (`in ("2026-10-17", "2026-10-18")`) passed before/on/after (Grok 4.7, v3 pass)
for tag, dt, want in (("before", "2026-10-16", 0), ("on", "2026-10-17", 1), ("after", "2026-10-18", 1),
                      ("far", "2027-01-01", 1)):
    e = ans(dt, d="OK", seat="kimi", note="cutoff isolation " + tag)
    fb = wjson("b_cut_%s.json" % tag, base + [ident(ROW0, e) + [1]])
    rc, out = run_checker(with_entries([(ROW0, e)]), fb)
    say("C12 cutoff isolated: a FROZEN identity dated %s (%s)" % (dt, tag), rc == want, "rc %d (want %d)" % (rc, want))
rc, out = run_checker(LEDGER, os.path.join(T, "no_such_baseline.json"))
say("C13 an unreadable baseline", rc == 2, "rc %d" % rc)
#  C27: the glyph SET, read from both files' own literals.  A fifth member (`"ZXQ"`) in the checker's DOMAIN, or a fifth key in
#  the renderer's D_CLASS, was invisible to every v3 control -- no control writes that spelling, and none can write every one
#  (Grok 4.7, v3 pass) -- so the set is pinned where it is defined, and the two files must agree, as the checker says
import ast  # noqa: E402
def literal(path, name):
    for line in io.open(path, encoding="utf-8"):
        if line.startswith(name + " = "):
            return ast.literal_eval(line.split("=", 1)[1].split("#")[0].strip())
    return None
dom, dcls = literal(CHECKER, "DOMAIN"), literal(RENDER, "D_CLASS")
four = ("✓", "✕", "⏸", "…")
say("C27 the checker's DOMAIN and the renderer's D_CLASS keys are exactly ✓ ✕ ⏸ …",
    isinstance(dom, tuple) and isinstance(dcls, dict) and sorted(dom) == sorted(four) and sorted(dcls) == sorted(four),
    "DOMAIN %r | D_CLASS keys %r" % (dom, sorted(dcls) if isinstance(dcls, dict) else dcls))
rc, out = run_checker(LEDGER, wjson("b_shape.json", [k[:6] + [str(k[6])] for k in base]))
say("C17 a misshapen baseline (counts as strings)", rc == 2, "rc %d" % rc)
#  C17b: one key of count >= 2 split into two rows; the sum must hold (pass 2 fixed last-wins; the adjudication pass found
#  nothing pinned the sum -- GPT-6 Astra and GLM 5.3)
k2 = next(k for k in base if k[6] >= 2)
split = [k for k in base if k is not k2] + [k2[:6] + [1], k2[:6] + [k2[6] - 1]]
rc, out = run_checker(LEDGER, wjson("b_split.json", split))
say("C17b a key split across two baseline rows sums (%s %s %s %s %r x%d)" % (tuple(k2[:5]) + (k2[6],)), rc == 0, "rc %d" % rc)
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
                 ("C21f a misshapen ledger: entries that are an object", {"rows": [{"id": "x", "entries": {}}]})):
    rc, out = run_checker(wjson("l_shape_%d.json" % len(res), obj))
    tb = any("Traceback" in l for l in out)
    say(lab, rc == 2 and not tb, "rc %d%s" % (rc, " TRACEBACK" if tb else ""))
rc, out = run_checker(LEDGER, wjson("b_dict.json", {}))
say("C21g a misshapen baseline: an object, not a list (override)", rc == 2, "rc %d" % rc)
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
                           {"phase": "assess", "seat": "grok", "date": "2026-10-16", "d": "\t", "note": "tab control"}]},
              #  R1e: an ANSWER with a non-answer RECORD beside it in one cell -- deleting the record line passed every v3
              #  control and drops the note from 32 displayed cells (GPT-6 Astra, v3 pass)
              {"id": "ctlrec", "title": "record control row", "sev": "LOW", "state": "open", "commits": "",
               "entries": [{"phase": "review", "seat": "fable5", "date": "2026-10-16", "d": "OK", "note": "record control answer"},
                           {"phase": "review", "seat": "fable5", "date": "2026-10-16", "note": REC_NOTE}]},
              #  R1f: a legacy answer carrying a stage exemption (a re-read), refused by a LATER answer in its stage
              #  R1h: a PADDED glyph " ✓" is outside the domain and renders legacy (the checker refuses it as off-domain);
              #  `D_CLASS.get(str(d).strip(), ...)` would class it ok (Fable 5.1, v3 pass: caught only as a presence pin)
              {"id": "ctlpad", "title": "padded glyph control row", "sev": "LOW", "state": "open", "commits": "",
               "entries": [{"phase": "assess", "seat": "fable5", "date": "2026-10-16", "d": " ✓", "note": "padded glyph control"}]},
              {"id": "ctlref", "title": "refused exemption control row", "sev": "LOW", "state": "open", "commits": "",
               "entries": [REF_A, {"phase": "research", "seat": "grok", "date": "2026-10-17", "d": "✓", "note": "a later answer"}]}]
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
             "padded glyph control", "tab control")


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
    got = [c for c in cells(html_text) if "whitespace control" in c[2] or "tab control" in c[2]]
    return (len(got) == 2 and all(c[0] == "legacy" and c[1] == "?" for c in got)), "whitespace cells %r" % ([c[:2] for c in got],)


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
                            ("escape control", "<b>&"), ("whitespace control", " "), ("padded glyph control", " ✓"),
                            ("tab control", "\t"))]
    legacy = [tip for cls_, g, tip in cells(html_text) if cls_ == "legacy"]
    missing = [(note, d) for note, d, whole in want if whole not in legacy]
    return not missing, "%d legacy cells; no exact tooltip for: %s" % (len(legacy), missing[:3])


def r1e(html_text):
    if html_text is None:
        return False, "render FAILED (a crash is not a kill)"
    got = [c for c in cells(html_text) if "record control answer" in c[2]]
    want = html.escape("record: 2026-10-16 — " + REC_NOTE, quote=True)
    return (len(got) == 1 and got[0][0] == "legacy" and want in got[0][2]), "cells %d; record kept %s" % (
        len(got), bool(got) and want in got[0][2])


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
pad = [c for c in cells(ha_fx or "") if "padded glyph control" in c[2]]
say("R1h a padded glyph ' ✓' renders legacy, not ok", len(pad) == 1 and pad[0][0] == "legacy",
    "cell %r" % (pad[0][:2],) if pad else "render FAILED or no cell")
ok, det = r1e(ha_fx); say("R1e an answer with a record beside it keeps the record's note", ok, det)
ok, det = r1f(ha_fx); say("R1f a refused exemption's line first, then the class line, exactly", ok, det)
ok, det = r1b(ha_fx); say("R1b an escapable d renders escaped", ok, det)
ok, det = r1d(ha_fx); say("R1d a whitespace-only d -- a space, a tab -- shows ?", ok, det)
low = (ha_fx or "").lower()
hits = [p for p in ("not approval", "not a seat failure") if p in low]
say("R1c the fixture page says neither 'not approval' nor 'not a seat failure'", ha_fx is not None and not hits,
    "render %s; found %s" % ("ok" if ha_fx is not None else "FAILED", hits or "none"))
leg = re.search(r'<div class="legend">(.*?)</div>', ha_fx or "", re.S)
say("R4 the legend carries the legacy line EXACTLY", bool(leg) and LEGEND_LINE in leg.group(1),
    "legend %s" % ("found" if leg else "MISSING"))


def census(html_text):
    c = collections.Counter(m.group(1) for m in re.finditer(r'<td class="c ([a-z]+)"', html_text))
    s = re.search(r'<span class="k">entries</span><b>([^<]*)</b>', html_text).group(1)
    return c, s


hb, ha = render(BEFORE, LEDGER, "before_real"), render(RENDER, LEDGER, "after_real")
cb, sb = census(hb)
ca, sa = census(ha)
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
say("R2 shipped ledger BEFORE vs AFTER: only pend -> legacy; EACH strip number is the ledger's own count", same and moved and sums,
    "before %s | after %s | strip '%s' | ledger %d entries, %d off-domain" % (dict(sorted(cb.items())), dict(sorted(ca.items())),
                                                                          sa, n_entries, n_legacy))
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
    def w_tools(tag, ledger_path, baseline_text=None, nochecker=False):
        """a fake tools/ dir: the block's own _HERE, holding the checker under test, the FIXTURE ledger as the default ledger
        and a baseline -- the block strips GXLEDGER / GXDOMAIN_BASELINE, so fixtures can only enter this way"""
        d = os.path.join(T, "w_" + tag)
        os.makedirs(os.path.join(d, "pipeline"), exist_ok=True)
        if not nochecker:
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
            ("W6 Q2 with the checker absent", w_tools("6", LEDGER, nochecker=True), {}, "BAD", 1, "MISSING")):
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
        ok = firstl.startswith(want + " ") and msg in firstl and ((nf == 0) if wantf == 0 else (nf >= 1)) and named
        say(lab, ok, "%s | failures %d" % (firstl[:90], nf))

shutil.rmtree(T, ignore_errors=True)
print("DASHOKCLASS CONTROLS: %d/%d as expected" % (sum(res), len(res)))
print("DASHOKCLASS_CONTROLS_DONE")
sys.exit(0 if all(res) else 1)
