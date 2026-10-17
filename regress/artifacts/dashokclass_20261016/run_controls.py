#!/usr/bin/env python3
"""Controls for `dashokclass` (2026-10-16): gen_dashboard.py's LEGACY class and check_entry_domain.py (precommit Q2).
Everything runs on temp copies and fixture ledgers; nothing in the tree is written.  Exit 0 only if every control holds.

  CHECKER (Astra's four completeness conditions, plus the ruling's grandfathering amendment):
    C1  the shipped ledger against the shipped baseline                                  -> 0
    C2  + an answer dated ON the cutoff carrying a valid glyph (the POSITIVE row)        -> 0
    C3  + an answer dated ON the cutoff carrying "OK" (inclusive cutoff)                 -> 1
    C4  + an answer dated AFTER the cutoff carrying "OK"                                 -> 1
    C5  + an answer dated BEFORE the cutoff carrying "OK", a new tuple (back-dated)      -> 1
    C6  + an UNDATED answer carrying "N/A"                                               -> 1
    C7  + an answer after the cutoff with NO `d` (renders as the default)                -> 0
    C8  + a HELD marker after the cutoff carrying "HELD" (not an answer)                 -> 0
    C9  + a second copy of a grandfathered entry (its tuple's count exceeded)            -> 1
    C10 a grandfathered entry rewritten to a glyph (the population shrinks)              -> 0
    C11 MUTANT: the baseline removed (an empty list) on the shipped ledger               -> 1
    C12 MUTANT: the cutoff test removed, on a fixture whose baseline holds a post-cutoff
        tuple -- the real checker fails it, the mutant passes it                         -> 1 / 0
    C13 an unreadable baseline                                                           -> 2
  RENDERER:
    R1  a fixture row, one entry per seat: the AFTER renderer gives exactly the expected class and glyph per cell
        (✓ ok, "OK" legacy, missing d pend, blank legacy "?", a HELD marker hold, a NOT-A-SEAT record tok, ✕ bad,
        ⏸ hold, "N/A" legacy)
    R2  the shipped ledger, BEFORE vs AFTER renderer: ok / hold / bad / tok / none unchanged, pend falls by exactly
        the legacy count, and the AFTER strip sums to the entry total
    R3  MUTANTS of the AFTER renderer -- the fallback mapped to "ok" (OK rendered as approval) and back to "pend"
        (the old behaviour) -- each fails R1
"""
import collections, copy, io, json, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, os.pardir, os.pardir, os.pardir))
PIPE = os.path.join(REPO, "tools", "pipeline")
CHECKER = os.path.join(PIPE, "check_entry_domain.py")
RENDER = os.path.join(PIPE, "gen_dashboard.py")
BEFORE = os.path.join(HERE, "gen_dashboard_before.py")      # HEAD's renderer at the landing, preserved
BASELINE = os.path.join(PIPE, "entry_domain_baseline.json")
LEDGER = os.path.join(PIPE, "ledger.json")
sys.path.insert(0, PIPE)
import stage_tokens as st  # noqa: E402

T = tempfile.mkdtemp()
res = []


def say(label, ok, detail=""):
    res.append(ok)
    print("%-4s %-70s %s  %s" % (label.split()[0], label[len(label.split()[0]) + 1:], "ok" if ok else "NO", detail))


def wjson(name, obj):
    p = os.path.join(T, name)
    io.open(p, "w", encoding="utf-8").write(json.dumps(obj, ensure_ascii=False))
    return p


def run_checker(ledger_path, baseline_path, checker=CHECKER):
    env = dict(os.environ, GXLEDGER=ledger_path, GXDOMAIN_BASELINE=baseline_path, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, checker], capture_output=True, text=True, encoding="utf-8", env=env)
    return r.returncode, (r.stdout + r.stderr).strip().splitlines()


L0 = json.load(io.open(LEDGER, encoding="utf-8"))
ROW0 = L0["rows"][0]["id"]


def with_entry(entry, row=ROW0):
    L = copy.deepcopy(L0)
    for r in L["rows"]:
        if r["id"] == row:
            r.setdefault("entries", []).append(entry)
    return wjson("l_%d.json" % len(res), L)


def ans(date, **kw):
    e = {"phase": "review", "seat": "grok", "note": "a control entry"}
    if date is not None:
        e["date"] = date
    e.update(kw)
    return e


print("# dashokclass controls -- repo %s" % REPO)
# ------------------------------------------------------------------ the checker
rc, out = run_checker(LEDGER, BASELINE)
say("C1 shipped ledger, shipped baseline", rc == 0, "rc %d: %s" % (rc, out[0] if out else ""))
for lab, ent, want in [
    ("C2 on the cutoff, a valid glyph (positive)", ans("2026-10-17", d="✓"), 0),
    ("C3 on the cutoff, d OK (inclusive)", ans("2026-10-17", d="OK"), 1),
    ("C4 after the cutoff, d OK", ans("2026-10-18", d="OK"), 1),
    ("C5 before the cutoff, d OK, a new tuple (back-dated)", ans("2026-09-01", d="OK", seat="minimax"), 1),
    ("C6 undated, d N/A", ans(None, d="N/A"), 1),
    ("C7 after the cutoff, no d", ans("2026-10-18"), 0),
    ("C8 a HELD marker after the cutoff, d HELD", ans("2026-10-18", d="HELD", note=st.HELD + " grok] waiting"), 0),
]:
    rc, out = run_checker(with_entry(ent), BASELINE)
    say(lab, rc == want, "rc %d (want %d)" % (rc, want))
# C9 / C10: a grandfathered entry, duplicated and then rewritten
base = json.load(io.open(BASELINE, encoding="utf-8"))
row, phase, seat, date, d, n = base[0]
src = next(x for r in L0["rows"] if r["id"] == row for x in r.get("entries", [])
           if (x.get("phase") or "", x.get("seat") or "", x.get("date") or "", str(x.get("d"))) == (phase, seat, date, d))
rc, out = run_checker(with_entry(dict(src), row=row), BASELINE)
say("C9 a second copy of grandfathered (%s %s %s %s %r)" % (row, phase, seat, date, d), rc == 1, "rc %d" % rc)
L = copy.deepcopy(L0)
for r in L["rows"]:
    if r["id"] == row:
        for x in r["entries"]:
            if (x.get("phase") or "", x.get("seat") or "", x.get("date") or "", str(x.get("d"))) == (phase, seat, date, d):
                x["d"] = "✓"
rc, out = run_checker(wjson("l_rewrite.json", L), BASELINE)
say("C10 grandfathered entries rewritten to a glyph", rc == 0, "rc %d" % rc)
rc, out = run_checker(LEDGER, wjson("b_empty.json", []))
nb = sum(1 for l in out if "NEW OFF-DOMAIN" in l)
say("C11 MUTANT baseline removed: the shipped ledger fails", rc == 1 and nb > 0, "rc %d, %d entries named" % (rc, nb))
# C12: a fixture baseline holding a post-cutoff tuple; the cutoff test is what refuses it
fx_led = with_entry(ans("2026-10-20", d="OK", seat="kimi"))
fx_base = wjson("b_post.json", base + [[ROW0, "review", "kimi", "2026-10-20", "OK", 1]])
rc_real, _ = run_checker(fx_led, fx_base)
mut = os.path.join(T, "check_entry_domain_nocutoff.py")
src_c = io.open(CHECKER, encoding="utf-8").read()
assert src_c.count("if t[3] >= CUTOFF:") == 1
io.open(mut, "w", encoding="utf-8").write(src_c.replace("if t[3] >= CUTOFF:", "if False:"))
shutil.copy(os.path.join(PIPE, "stage_tokens.py"), T)
rc_mut, _ = run_checker(fx_led, fx_base, checker=mut)
say("C12 MUTANT cutoff removed: real fails, mutant passes", rc_real == 1 and rc_mut == 0, "real rc %d, mutant rc %d" % (rc_real, rc_mut))
rc, out = run_checker(LEDGER, os.path.join(T, "no_such_baseline.json"))
say("C13 an unreadable baseline", rc == 2, "rc %d" % rc)

# ------------------------------------------------------------------ the renderer
SEATS = [s["id"] for s in L0["seats"]]
EXPECT = {   # seat -> (entry fields, expected class, expected glyph)
    "fable5": ({"d": "✓"}, "ok", "✓"),
    "opus5": ({"d": "OK"}, "legacy", "OK"),
    "codex": ({}, "pend", "…"),
    "agy": ({"d": ""}, "legacy", "?"),
    "grok": ({"d": "HELD", "note": st.HELD + " grok] waiting"}, "hold", "⏸"),
    "kimi": ({"d": "OK", "note": st.NOTSEAT + " a main-loop record"}, "tok", None),
    "glm": ({"d": "✕"}, "bad", "✕"),
    "deepseek": ({"d": "⏸"}, "hold", "⏸"),
    "minimax": ({"d": "N/A"}, "legacy", "N/A"),
}
assert set(EXPECT) == set(SEATS), SEATS
FX = copy.deepcopy(L0)
ents = []
for s in SEATS:
    f, _, _ = EXPECT[s]
    e = {"phase": "review", "seat": s, "date": "2026-10-16", "note": "a renderer control"}
    e.update(f)
    ents.append(e)
FX["rows"] = [{"id": "ctlrow", "title": "renderer control row", "sev": "LOW", "state": "open", "commits": "", "entries": ents}]
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
    if r.returncode != 0:
        return None
    return io.open(out, encoding="utf-8").read()


def cells(html):
    got = []
    for m in re.finditer(r'<td class="c ([a-z]+)">(.*?)</td>', html, re.S):
        if m.group(1) == "none":
            continue
        g = re.search(r'<span class="g">(.*?)</span>', m.group(2))
        got.append((m.group(1), g.group(1) if g else None))
    return got


def r1(html):
    if html is None:
        return False, "render failed"
    got = cells(html)
    want = [(EXPECT[s][1], EXPECT[s][2]) for s in SEATS]
    bad = [(s, g, w) for s, g, w in zip(SEATS, got, want) if g[0] != w[0] or (w[1] is not None and g[1] != w[1])]
    return (len(got) == len(want) and not bad), ("%d cells; mismatches %s" % (len(got), bad[:3]))


ok, det = r1(render(RENDER, fx_path, "after"))
say("R1 fixture row: class and glyph per seat (AFTER renderer)", ok, det)


def census(html):
    c = collections.Counter(m.group(1) for m in re.finditer(r'<td class="c ([a-z]+)"', html))
    s = re.search(r'<span class="k">entries</span><b>([^<]*)</b>', html).group(1)
    return c, s


hb, ha = render(BEFORE, LEDGER, "before_real"), render(RENDER, LEDGER, "after_real")
cb, sb = census(hb)
ca, sa = census(ha)
same = all(cb[k] == ca[k] for k in ("ok", "hold", "bad", "tok", "none"))
moved = cb["pend"] - ca["pend"] == ca["legacy"] and ca["legacy"] > 0
nums = [int(x) for x in re.findall(r"(\d+)", sa)]
sums = len(nums) == 6 and sum(nums[:5]) == nums[5]
say("R2 shipped ledger BEFORE vs AFTER: only pend -> legacy moves; strip sums", same and moved and sums,
    "before %s | after %s | strip '%s'" % (dict(sorted(cb.items())), dict(sorted(ca.items())), sa))
src_r = io.open(RENDER, encoding="utf-8").read()
assert src_r.count("cls = D_CLASS.get(d, LEGACY)") == 1
for tag, repl in (("ok", 'cls = D_CLASS.get(d, "ok")'), ("pend", 'cls = D_CLASS.get(d, "pend")')):
    m = os.path.join(T, "gen_mut_%s.py" % tag)
    io.open(m, "w", encoding="utf-8").write(src_r.replace("cls = D_CLASS.get(d, LEGACY)", repl))
    ok, det = r1(render(m, fx_path, "mut_" + tag))
    say("R3 MUTANT fallback -> %s: R1 must fail" % tag, not ok, det)

#  ------------------------------------------------------------------ the precommit wiring (section Q2), extracted and run
#  with stub reporters -- a section that never calls the checker, or reads its status wrong, passes every C row above.
#  Windows python's "bash" can be the WSL launcher, so the git-bash binary is named (BASH_EXE overrides).
BASH = os.environ.get("BASH_EXE") or r"C:\Program Files\Git\bin\bash.exe"
PRE = os.path.join(REPO, "tools", "precommit_check.sh")
txt = io.open(PRE, encoding="utf-8").read()
a, b = txt.find('say ""; say "Q2.'), txt.find("#  ---- R ----")
if a < 0 or b < a or not os.path.exists(BASH):
    say("W0 precommit Q2 block extracted and a git-bash found", False, "a=%d b=%d bash=%s" % (a, b, BASH))
else:
    blk = os.path.join(T, "q2_block.sh")
    io.open(blk, "w", encoding="utf-8", newline="\n").write(
        'say () { :; }\ngood () { echo "GOOD $*"; }\nbad () { echo "BAD $*"; }\n_HERE="$1"\n' + txt[a:b])
    tools = os.path.join(REPO, "tools").replace("\\", "/")
    for lab, led, want in (("W1 Q2 on the shipped ledger", LEDGER, "GOOD"),
                           ("W2 Q2 with a new off-domain answer", with_entry(ans("2026-10-18", d="OK")), "BAD")):
        env = dict(os.environ, GXLEDGER=led, GXDOMAIN_BASELINE=BASELINE, PYTHONIOENCODING="utf-8")
        r = subprocess.run([BASH, blk.replace("\\", "/"), tools], capture_output=True, text=True, encoding="utf-8", env=env)
        first = (r.stdout.strip().splitlines() or [""])[0]
        say(lab, first.startswith(want + " "), first[:120])

shutil.rmtree(T, ignore_errors=True)
print("DASHOKCLASS CONTROLS: %d/%d as expected" % (sum(res), len(res)))
print("DASHOKCLASS_CONTROLS_DONE")
sys.exit(0 if all(res) else 1)
