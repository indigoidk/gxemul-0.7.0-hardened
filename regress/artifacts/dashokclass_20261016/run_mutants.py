#!/usr/bin/env python3
"""The KILL TABLE for `dashokclass`'s controls (2026-10-16): one-edit mutants of check_entry_domain.py, gen_dashboard.py and
precommit section Q2, each run through run_controls_v2.py (CTL_CHECKER / CTL_RENDER / CTL_PRECOMMIT).  A mutant must turn at
least the controls its line names red.  A find-text that is absent is an apparatus failure, never a silent skip.
Usage: run_mutants.py      (writes only to a scratch dir it removes; exit 0 only if every mutant is killed as named)
CORRECTED at the adjudication pass (Fable 5.1, GPT-6 Astra): this runner called `run_controls.py`, which in this directory is
the v1 suite -- it dies on the 7-field baseline, so KILLTABLE_staged.txt reproduced only in a staging copy holding v2 under v1's
name.  It now names run_controls_v2.py, and takes the files under test from CTL_CHECKER / CTL_RENDER / CTL_PRECOMMIT when set
(the staged_v2 files), else the tree's -- run_controls_v2.py reads the TREE's baseline, so it reproduces once the tree holds
the baseline (byte-identical to staged_v2's, md5 06a3ffc6).  The v3 table is run_mutants_v3.py."""
import io, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, os.pardir, os.pardir, os.pardir))
FILES = {"checker": os.environ.get("CTL_CHECKER") or os.path.join(REPO, "tools", "pipeline", "check_entry_domain.py"),
         "render": os.environ.get("CTL_RENDER") or os.path.join(REPO, "tools", "pipeline", "gen_dashboard.py"),
         "precommit": os.environ.get("CTL_PRECOMMIT") or os.path.join(REPO, "tools", "precommit_check.sh")}
CONTROLS = os.path.join(HERE, "run_controls_v2.py")
ENV = {"checker": "CTL_CHECKER", "render": "CTL_RENDER", "precommit": "CTL_PRECOMMIT"}
MUTANTS = [   # name, file, find, replace, controls that must go red
    ("d_cutoff18", "checker", 'CUTOFF = "2026-10-17"', 'CUTOFF = "2026-10-18"', ["C12"]),
    ("d_blank", "checker", 'if "d" not in x or x["d"] in DOMAIN', 'if not x.get("d") or x["d"] in DOMAIN', ["C14"]),
    ("d_nonote", "checker", 'return hashlib.sha1(str(x.get("note") or "").encode("utf-8")).hexdigest()[:16]',
     'return "0" * 16', ["C1"]),       # a checker without the note no longer matches the frozen baseline at all
    ("d_nomd5", "checker", "if BASELINE == DEFAULT_BASELINE and hashlib.md5(raw).hexdigest() != BASELINE_MD5:", "if False:",
     ["C18"]),
    ("d_nodate", "checker", "if ISO.match(t[3]) and t[3][:10] >= CUTOFF:", "if False:", ["C12"]),
    ("d_noreconf", "checker", 'sys.stdout.reconfigure(errors="backslashreplace")', "pass", ["C20"]),
    ("r_nolegend", "render", "legacy -- verdict text outside ✓ ✕ ⏸ …, unclassified", "unclassified", ["R4"]),
    ("r_ok", "render", "cls = D_CLASS.get(d, LEGACY)", 'cls = D_CLASS.get(d, "ok")', ["R1"]),
    ("r_pend", "render", "cls = D_CLASS.get(d, LEGACY)", 'cls = D_CLASS.get(d, "pend")', ["R1"]),
    ("r_noescape", "render", '{e(d) if str(d).strip() else "?"}', '{d if str(d).strip() else "?"}', ["R1b"]),
    ("r_strip", "render", 'n[d if d in D_CLASS else LEGACY] += 1', 'n[d if d in D_CLASS else "…"] += 1', ["R2"]),
    ("w_envkeep", "precommit", '_ced=$(env -u GXDOMAIN_BASELINE -u GXLEDGER python "$CED" 2>&1)', '_ced=$(python "$CED" 2>&1)', ["W4"]),
    ("w_collapse", "precommit", "\tif [ $_cedrc -eq 0 ]; then\n\t\tgood", "\tif [ $_cedrc -ne 1 ]; then\n\t\tgood", ["W3"]),
    ("w_subshell", "precommit",
     '\t\tbad "an off-domain ledger answer is not a frozen legacy entry (a new one, or an old one edited):"',
     '\t\t( bad "an off-domain ledger answer is not a frozen legacy entry (a new one, or an old one edited):" )', ["W2"]),
]
T = tempfile.mkdtemp()
env0 = dict(os.environ, PYTHONIOENCODING="utf-8")
base = subprocess.run([sys.executable, CONTROLS], capture_output=True, text=True,
                      encoding="utf-8", env=env0)
bl = [l for l in base.stdout.splitlines() if l.startswith("DASHOKCLASS CONTROLS:")]
print("# dashokclass kill table")
print("BASE        %s" % (bl[0] if bl else "NO TALLY"))
if base.returncode != 0:
    print("APPARATUS FAIL: the base run is not clean"); shutil.rmtree(T, ignore_errors=True); sys.exit(9)
ok = 0
for name, fkey, find, repl, named in MUTANTS:
    src = io.open(FILES[fkey], encoding="utf-8", newline="").read()
    if src.count(find) != 1:
        print("%-11s MUTANT TEXT NOT FOUND (%d)" % (name, src.count(find))); continue
    mp = os.path.join(T, name + os.path.splitext(FILES[fkey])[1])
    io.open(mp, "w", encoding="utf-8", newline="").write(src.replace(find, repl))
    env = dict(env0, **{ENV[fkey]: mp})
    r = subprocess.run([sys.executable, CONTROLS], capture_output=True, text=True,
                       encoding="utf-8", env=env)
    #  one space can precede the status: a label longer than its padded column leaves no padding (R2's does)
    red = sorted({l.split()[0] for l in r.stdout.splitlines() if re.search(r"\sNO\s{2}", l)})
    tally = ([l for l in r.stdout.splitlines() if l.startswith("DASHOKCLASS CONTROLS:")] or ["(no tally)"])[0].split(":")[1].split()[0]
    killed = all(n in red for n in named)
    ok += killed
    print("%-11s %-7s %-60s [%s]" % (name, tally, ("killed by: " + " ".join(red)) if killed else
                                     "NOT KILLED as named (red: %s)" % (" ".join(red) or "none"), " ".join(named)))
shutil.rmtree(T, ignore_errors=True)
print("KILL TABLE: %d/%d killed as named" % (ok, len(MUTANTS)))
print("DASHOKCLASS_MUTANTS_DONE")
sys.exit(0 if ok == len(MUTANTS) else 1)
