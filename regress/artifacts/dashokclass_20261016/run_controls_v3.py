#!/usr/bin/env python3
"""Controls for `dashokclass` (2026-10-16, v3 after the four-seat adjudication pass): gen_dashboard.py's LEGACY class,
check_entry_domain.py (a ceiling over selected content, md5-pinned baseline) and its precommit section Q2.  Everything runs on
temp copies and fixture ledgers; nothing in the tree is written.  Exit 0 only if every control holds.  CTL_CHECKER /
CTL_RENDER / CTL_PRECOMMIT override the three files under test (run_mutants_v3.py and the staged runs use them); the defaults
are the tree's.

  CHECKER (Astra's four conditions, the ruling's grandfathering amendment, pass 2's and the adjudication pass's findings):
    C1   shipped ledger, shipped baseline (the md5 pin is checked on the default path)             -> 0, all within the ceiling
    C2   an answer ON the cutoff with a valid glyph (positive)                                      -> 0
    C2b  an answer AFTER the cutoff with a valid glyph (positive)                                   -> 0
    C2c  / C2d  an answer after the cutoff with ⏸ / with … (positive, one row per glyph)            -> 0 / 0
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
    C21  misshapen LEDGERS -- {"rows": null}, a row that is not an object, a list -- rc 2, no traceback -> 2 / 2 / 2
    C22  a frozen entry's `ev` edited -- outside the six fields (positive)                          -> 0
  RENDERER:
    R1   a fixture row, one entry per seat: class AND glyph per cell (the record cell's glyph included), and the
         legacy cell's tooltip EXACTLY (the whole string, not a prefix)
    R1b  an escapable `d` ("<b>&") renders escaped
    R1c  the fixture page says neither "not approval" nor "not a seat failure" anywhere
    R1d  a whitespace-only `d` (" ") shows `?`
    R2   the shipped ledger, BEFORE vs AFTER: only pend -> legacy moves; the strip's five numbers sum to the ledger's
         actual entry count, and its legacy number is the ledger's own count of explicit off-domain `d`
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


print("# dashokclass controls (v3) -- checker %s | renderer %s | precommit %s | baseline %s"
      % (hashlib.md5(open(CHECKER, "rb").read()).hexdigest()[:8], hashlib.md5(open(RENDER, "rb").read()).hexdigest()[:8],
         hashlib.md5(open(PRE, "rb").read()).hexdigest()[:8], hashlib.md5(open(BASELINE, "rb").read()).hexdigest()[:8]))
# ------------------------------------------------------------------ the checker
rc, out = run_checker(LEDGER)
first = out[0] if out else ""
say("C1 shipped ledger, shipped baseline, md5 pin live", rc == 0 and ("%d within the frozen ceiling" % N_OFF) in first,
    "rc %d: %s" % (rc, first))
for lab, ent, want in [
    ("C2 ON the cutoff, a valid glyph (positive)", ans("2026-10-17", d="✓"), 0),
    ("C2b AFTER the cutoff, a valid glyph (positive)", ans("2026-10-18", d="✕"), 0),
    #  ⏸ and … were positive-pinned only INCIDENTALLY, by the shipped ledger's own 21 and 35 such answers (Fable 5.1,
    #  adjudication pass): one direct row each
    ("C2c AFTER the cutoff, d ⏸ (positive)", ans("2026-10-18", d="⏸"), 0),
    ("C2d AFTER the cutoff, d … (positive)", ans("2026-10-18", d="…"), 0),
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
]:
    rc, out = run_checker(with_entries([(ROW0, ent)]))
    tb = any("Traceback" in l for l in out)
    #  a malformed date must be NAMED in the reason, not only refused: v1's lexical `t[3] >= CUTOFF` and a deleted suffix each
    #  passed every v2 control while calling a numeric date "on or after the cutoff" (Fable 5.1, adjudication pass)
    why = (not lab.startswith("C19")) or any("its date is not ISO" in l for l in out)
    say(lab, rc == want and not tb and why, "rc %d (want %d)%s%s" % (rc, want, " TRACEBACK" if tb else "",
                                                                    "" if why else " REASON NOT NAMED"))
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
rc, out = run_checker(LEDGER, wjson("b_empty.json", []))
nb = sum(1 for l in out if "OFF-DOMAIN ANSWER" in l)
say("C11 baseline emptied: every shipped off-domain answer named", rc == 1 and nb == N_OFF, "rc %d, %d of %d named" % (rc, nb, N_OFF))
# C12: the cutoff test isolated -- each fixture entry IS in its fixture baseline, so only the date can refuse it
for tag, dt, want in (("before", "2026-10-16", 0), ("on", "2026-10-17", 1), ("after", "2026-10-18", 1)):
    e = ans(dt, d="OK", seat="kimi", note="cutoff isolation " + tag)
    fb = wjson("b_cut_%s.json" % tag, base + [ident(ROW0, e) + [1]])
    rc, out = run_checker(with_entries([(ROW0, e)]), fb)
    say("C12 cutoff isolated: a FROZEN identity dated %s (%s)" % (dt, tag), rc == want, "rc %d (want %d)" % (rc, want))
rc, out = run_checker(LEDGER, os.path.join(T, "no_such_baseline.json"))
say("C13 an unreadable baseline", rc == 2, "rc %d" % rc)
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
                 ("C21c a misshapen ledger: a list, not an object", [])):
    rc, out = run_checker(wjson("l_shape_%d.json" % len(res), obj))
    tb = any("Traceback" in l for l in out)
    say(lab, rc == 2 and not tb, "rc %d%s" % (rc, " TRACEBACK" if tb else ""))

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
               "entries": [{"phase": "assess", "seat": "fable5", "date": "2026-10-16", "d": " ", "note": "whitespace control"}]}]
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
    got = [c for c in cells(html_text) if "escape control" not in c[2] and "whitespace control" not in c[2]]   # nine, in seat order
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
    got = [c for c in cells(html_text) if "whitespace control" in c[2]]
    ws = got[0] if got else ("", "", "")
    return (ws[0] == "legacy" and ws[1] == "?"), "whitespace cell %r" % (ws[:2],)


ha_fx = render(RENDER, fx_path, "after")
ok, det = r1(ha_fx); say("R1 fixture row: class, glyph and the legacy tooltip EXACTLY, per seat", ok, det)
ok, det = r1b(ha_fx); say("R1b an escapable d renders escaped", ok, det)
ok, det = r1d(ha_fx); say("R1d a whitespace-only d shows ?", ok, det)
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
sums = len(nums) == 6 and sum(nums[:5]) == nums[5] == n_entries and nums[4] == n_legacy
say("R2 shipped ledger BEFORE vs AFTER: only pend -> legacy; strip sums, legacy = the ledger's count", same and moved and sums,
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
    def w_tools(tag, ledger_path, baseline_text=None):
        """a fake tools/ dir: the block's own _HERE, holding the checker under test, the FIXTURE ledger as the default ledger
        and a baseline -- the block strips GXLEDGER / GXDOMAIN_BASELINE, so fixtures can only enter this way"""
        d = os.path.join(T, "w_" + tag)
        os.makedirs(os.path.join(d, "pipeline"), exist_ok=True)
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
             "BAD", 1, "beyond the frozen legacy ceiling")):
        env = dict(os.environ)
        for k in ("GXLEDGER", "GXDOMAIN_BASELINE", "PYTHONIOENCODING", "PYTHONUTF8"):
            env.pop(k, None)
        env.update(envx)
        r = subprocess.run([BASH, blk.replace("\\", "/"), tools.replace("\\", "/")], capture_output=True, env=env)
        outl = r.stdout.decode("cp1252", "replace").strip().splitlines()
        firstl = outl[0] if outl else ""
        fl = [l for l in outl if l.startswith("FAILURES ")]
        nf = int(fl[-1].split()[1]) if fl else -1
        ok = firstl.startswith(want + " ") and msg in firstl and ((nf == 0) if wantf == 0 else (nf >= 1))
        say(lab, ok, "%s | failures %d" % (firstl[:90], nf))

shutil.rmtree(T, ignore_errors=True)
print("DASHOKCLASS CONTROLS: %d/%d as expected" % (sum(res), len(res)))
print("DASHOKCLASS_CONTROLS_DONE")
sys.exit(0 if all(res) else 1)
