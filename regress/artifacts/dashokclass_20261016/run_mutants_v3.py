#!/usr/bin/env python3
"""The KILL TABLE for `dashokclass`'s v3 controls (2026-10-16, after the adjudication pass): mutants of check_entry_domain.py,
gen_dashboard.py and precommit section Q2, each run through run_controls_v3.py -- BY THAT NAME (the v2 table's runner called
`run_controls.py`, the v1 suite, which crashes on the 7-field baseline; it reproduced only in a staging copy -- Fable 5.1 and
GPT-6 Astra, adjudication pass).  The files under test are CTL_CHECKER / CTL_RENDER / CTL_PRECOMMIT when set (a staged run),
else the tree's; the checker's baseline is the one beside it.  A mutant must turn at least the controls its line names red;
an UNPINNED one is measured too, so its escape is a recorded result.  A find-text that is absent is an apparatus failure.
Usage: run_mutants_v3.py      (writes only to a scratch dir it removes; exit 0 only if every line holds as recorded)"""
import io, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, os.pardir, os.pardir, os.pardir))
CONTROLS = os.path.join(HERE, "run_controls_v3.py")
ENV = {"checker": "CTL_CHECKER", "render": "CTL_RENDER", "precommit": "CTL_PRECOMMIT"}
FILES = {"checker": os.environ.get("CTL_CHECKER") or os.path.join(REPO, "tools", "pipeline", "check_entry_domain.py"),
         "render": os.environ.get("CTL_RENDER") or os.path.join(REPO, "tools", "pipeline", "gen_dashboard.py"),
         "precommit": os.environ.get("CTL_PRECOMMIT") or os.path.join(REPO, "tools", "precommit_check.sh")}
SHA = 'return hashlib.sha1(str(x.get("note") or "").encode("utf-8")).hexdigest()[:16]'
LOAD = "base[tuple(k[:6])] += k[6]"
BADMSG = '\t\tbad "an off-domain ledger answer is beyond the frozen legacy ceiling (a new one, a copy, or an old one edited):"'
MUTANTS = [   # name, file, [(find, replace), ...], controls that must go red (or "UNPINNED: why")
    ("d_cutoff18", "checker", [('CUTOFF = "2026-10-17"', 'CUTOFF = "2026-10-18"')], ["C12"]),
    ("d_cutgt", "checker", [("t[3][:10] >= CUTOFF", "t[3][:10] > CUTOFF")], ["C12"]),
    ("d_nodate", "checker", [("if ISO.match(t[3]) and t[3][:10] >= CUTOFF:", "if False:")], ["C12"]),
    ("d_lexdate", "checker", [("if ISO.match(t[3]) and t[3][:10] >= CUTOFF:", "if t[3] >= CUTOFF:")], ["C19b"]),
    ("d_noreason", "checker", [('why += "; its date is not ISO YYYY-MM-DD"', "pass")], ["C19a", "C19b"]),
    ("d_blank", "checker", [('if "d" not in x or x["d"] in DOMAIN', 'if not x.get("d") or x["d"] in DOMAIN')], ["C14"]),
    ("d_domnohold", "checker", [('DOMAIN = ("✓", "✕", "⏸", "…")', 'DOMAIN = ("✓", "✕", "…")')], ["C2c"]),
    ("d_domnopend", "checker", [('DOMAIN = ("✓", "✕", "⏸", "…")', 'DOMAIN = ("✓", "✕", "⏸")')], ["C2d"]),
    ("d_dupplus1", "checker", [("elif seen[t] > base[t]:", "elif seen[t] > base[t] + 1:")], ["C5", "C9"]),
    #  ONE-SIDED: the baseline still carries real note shas, so EVERY frozen answer stops matching -- a real kill by C1, and
    #  NOT evidence for the note property (GLM 5.3, GPT-6 Astra, Fable 5.1); d_nonote2 is
    ("d_nonote", "checker", [(SHA, 'return "0" * 16')], ["C1"]),
    #  the COHERENT note-out -- the pass-2 (v1) key reinstated on BOTH sides.  A deliberate TWO-edit DESIGN mutant: no
    #  one-edit form is coherent, and it exists to show C15 and C16, not C1's mismatch, discriminate the note
    ("d_nonote2", "checker", [(SHA, 'return "0" * 16'), (LOAD, 'base[tuple(k[:5]) + ("0" * 16,)] += k[6]')], ["C15", "C16"]),
    ("d_lastwins", "checker", [(LOAD, "base[tuple(k[:6])] = k[6]")], ["C17b"]),
    ("d_ledger1", "checker", [('ledger misshapen: %s (%s: %s)" % (LEDGER, type(ex).__name__, ex)); return 2',
                               'ledger misshapen: %s (%s: %s)" % (LEDGER, type(ex).__name__, ex)); return 1')],
     ["C21a", "C21b", "C21c"]),
    ("d_nomd5", "checker", [("if BASELINE == DEFAULT_BASELINE and md != BASELINE_MD5:", "if False:")], ["C18"]),
    ("d_pinoverride", "checker", [("if BASELINE == DEFAULT_BASELINE and md != BASELINE_MD5:",
                                   "if BASELINE != DEFAULT_BASELINE and md != BASELINE_MD5:")], ["C18"]),
    ("d_crlfpin", "checker", [('md = hashlib.md5(raw.replace(b"\\r\\n", b"\\n")).hexdigest()', "md = hashlib.md5(raw).hexdigest()")],
     ["C18b"]),
    ("d_noreconf", "checker", [('sys.stdout.reconfigure(errors="backslashreplace")', "pass")], ["C20"]),
    ("d_notenone", "checker", [('str(x.get("note") or "")', 'str(x.get("note"))')],
     "UNPINNED: equivalent on the ledger -- 0 of the 1,356 off-domain answers has an empty or missing note"),
    ("r_nolegend", "render", [("legacy -- verdict text outside ✓ ✕ ⏸ …, unclassified", "unclassified")], ["R4"]),
    ("r_tipclause", "render", [("; read the note for the outcome", " (not approval, not a seat failure)")], ["R1", "R1c"]),
    ("r_tiptail", "render", [("; read the note for the outcome", "")], ["R1"]),
    ("r_ok", "render", [("cls = D_CLASS.get(d, LEGACY)", 'cls = D_CLASS.get(d, "ok")')], ["R1"]),
    ("r_pend", "render", [("cls = D_CLASS.get(d, LEGACY)", 'cls = D_CLASS.get(d, "pend")')], ["R1"]),
    ("r_noescape", "render", [('{e(d) if str(d).strip() else "?"}', '{d if str(d).strip() else "?"}')], ["R1b"]),
    ("r_wsblank", "render", [('{e(d) if str(d).strip() else "?"}', '{e(d) if d else "?"}')], ["R1d"]),
    ("r_strip", "render", [("n[d if d in D_CLASS else LEGACY] += 1", 'n[d if d in D_CLASS else "…"] += 1')], ["R2"]),
    ("w_envkeep", "precommit", [('_ced=$(env -u GXDOMAIN_BASELINE -u GXLEDGER python "$CED" 2>&1)', '_ced=$(python "$CED" 2>&1)')],
     ["W4", "W5"]),
    ("w_ledgerkeep", "precommit", [("env -u GXDOMAIN_BASELINE -u GXLEDGER python", "env -u GXDOMAIN_BASELINE python")], ["W5"]),
    ("w_collapse", "precommit", [("\tif [ $_cedrc -eq 0 ]; then\n\t\tgood", "\tif [ $_cedrc -ne 1 ]; then\n\t\tgood")], ["W3"]),
    ("w_rc7", "precommit", [("\telif [ $_cedrc -eq 1 ]; then", "\telif [ $_cedrc -eq 7 ]; then")], ["W2"]),
    ("w_msg", "precommit", [(BADMSG, '\t\tbad "x"')], ["W2"]),
    ("w_subshell", "precommit", [(BADMSG, "\t\t( " + BADMSG.strip() + " )")], ["W2"]),
]
T = tempfile.mkdtemp()
env0 = dict(os.environ, PYTHONIOENCODING="utf-8", **{ENV[k]: v for k, v in FILES.items()})


def controls(env):
    r = subprocess.run([sys.executable, CONTROLS], capture_output=True, text=True, encoding="utf-8", env=env)
    tally = ([l for l in r.stdout.splitlines() if l.startswith("DASHOKCLASS CONTROLS:")] or ["x: (no tally)"])[0].split(":")[1].split()[0]
    #  one space can precede the status: a label longer than its padded column leaves no padding
    red = sorted({l.split()[0] for l in r.stdout.splitlines() if re.search(r"\sNO\s{2}", l)})
    return r, tally, red, "DASHOKCLASS_CONTROLS_DONE" in r.stdout


print("# dashokclass kill table (v3) -- controls %s" % os.path.basename(CONTROLS))
for k in ("checker", "render", "precommit"):
    print("#   %-9s %s" % (k, FILES[k]))
base, btally, bred, bdone = controls(env0)
print("BASE          %s" % btally)
if base.returncode != 0 or not bdone or bred:
    print("APPARATUS FAIL: the base run is not clean (red: %s)" % (" ".join(bred) or "none"))
    shutil.rmtree(T, ignore_errors=True); sys.exit(9)
ok = 0
for name, fkey, edits, named in MUTANTS:
    src = io.open(FILES[fkey], encoding="utf-8", newline="").read()
    missing = [f for f, _ in edits if src.count(f) != 1]
    for f, r in edits:
        if src.count(f) == 1:
            src = src.replace(f, r)
    if missing:
        print("%-13s MUTANT TEXT NOT FOUND (%s)" % (name, missing[0][:60])); continue
    d = os.path.join(T, name)
    os.makedirs(d)
    mp = os.path.join(d, os.path.basename(FILES[fkey]))
    io.open(mp, "w", encoding="utf-8", newline="").write(src)
    if fkey == "checker":      # the baseline travels with the checker
        shutil.copy(os.path.join(os.path.dirname(FILES["checker"]), "entry_domain_baseline.json"), d)
    r, tally, red, done = controls(dict(env0, **{ENV[fkey]: mp}))
    if isinstance(named, str):
        good = done and not red
        verdict = "escapes (as recorded)" if good else "CAUGHT by: %s (unexpected)" % (" ".join(red) or "a crash")
    else:
        good = done and all(n in red for n in named)
        verdict = ("killed by: " + " ".join(red)) if good else "NOT KILLED as named (red: %s)" % (" ".join(red) or "none")
    ok += good
    print("%-13s %-7s %-66s [%s]" % (name, tally, verdict, named if isinstance(named, str) else " ".join(named)))
shutil.rmtree(T, ignore_errors=True)
print("KILL TABLE: %d/%d as recorded" % (ok, len(MUTANTS)))
print("DASHOKCLASS_MUTANTS_DONE")
sys.exit(0 if ok == len(MUTANTS) else 1)
