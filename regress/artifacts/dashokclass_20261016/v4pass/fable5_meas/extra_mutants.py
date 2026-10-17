#!/usr/bin/env python3
"""Fable 5.1 v4-pass sweep: one-edit mutants NOT in run_mutants_v4.py, each run through the 72 v4 controls in the
scratch MIRROR (never the project tree).  Same find/replace discipline as the project's runner: a find-text must occur
exactly once.  First entry is a POSITIVE CONTROL (a mutant the table already kills) so a 'passes all 72' here is a result
and not a broken driver."""
import io, os, re, shutil, subprocess, sys, tempfile
sys.stdout.reconfigure(encoding="utf-8")
M = sys.argv[1]                                   # the mirror root
ART = os.path.join(M, "regress", "artifacts", "dashokclass_20261016")
CONTROLS = os.path.join(ART, "run_controls_v4.py")
A = os.path.join(ART, "staged_v4", "tools")
FILES = {"checker": os.path.join(A, "pipeline", "check_entry_domain.py"),
         "render": os.path.join(A, "pipeline", "gen_dashboard.py"),
         "precommit": os.path.join(A, "precommit_check.sh")}
ENV = {"checker": "CTL_CHECKER", "render": "CTL_RENDER", "precommit": "CTL_PRECOMMIT"}
SUMMARY = "% (len(cur), len(cur) - len(bad), sum(base.values()), CUTOFF))"
MUTANTS = [
    ("ctl_r_ok", "render", [("cls = D_CLASS.get(d, LEGACY)", 'cls = D_CLASS.get(d, "ok")')], "POSITIVE CONTROL: expect R1 red"),
    ("d_basewithin", "checker", [(SUMMARY, "% (len(cur), len(cur) - len(bad), len(cur) - len(bad), CUTOFF))")],
     "summary's baseline number printed as the within-count (C1 and C11 both have within == baseline sum)"),
    ("d_cutreason", "checker", [('bad.append((t, "dated on or after the cutoff %s" % CUTOFF))', 'bad.append((t, "x"))')],
     "the cutoff refusal's REASON text replaced"),
    ("d_ceilreason", "checker", [('why = "beyond the frozen ceiling for its six fields -- a new answer, a copy, or an old one edited (classify it)"',
                                  'why = ""')], "the ceiling refusal's REASON text emptied (the ISO sub-reason still appends)"),
    ("d_len7ge", "checker", [("len(k) == 7", "len(k) >= 7")], "baseline shape: an 8-field row accepted"),
    ("d_boolcount", "checker", [("type(k[6]) is int", "isinstance(k[6], int)")], "baseline shape: a boolean count accepted"),
    ("d_str5", "checker", [("all(isinstance(v, str) for v in k[:6])", "all(isinstance(v, str) for v in k[:5])")],
     "baseline shape: a non-string note sha accepted"),
    ("d_isosearch", "checker", [("if ISO.match(t[3]) and t[3][:10] >= CUTOFF:", "if ISO.search(t[3]) and t[3][:10] >= CUTOFF:")],
     "the ISO anchor dropped on the cutoff test"),
    ("d_nostr", "checker", [('date_str(x), str(x["d"]),', 'date_str(x), x["d"],')], "d not stringified in the key"),
    ("d_hintundated", "checker", [("if t[3] and not ISO.match(t[3]):", "if not ISO.match(t[3]):")],
     "an UNDATED refusal also says 'its date is not ISO'"),
    ("d_datenone", "checker", [('% (row, phase, seat, date or "(none)", d, ns, why))', '% (row, phase, seat, date, d, ns, why))')],
     "the '(none)' placeholder for an undated refusal dropped"),
    ("r_recheld", "render", [("    for r in (x for x in mine if not st.is_answer(x) and not st.is_held(x)):",
                              "    for r in (x for x in mine if not st.is_answer(x)):")],
     "a HELD marker beside an answer would be appended as a record line (HEAD code, outside the diff)"),
    ("r_sumor", "render", [('            d = x.get("d", "…")\n            n[d if d in D_CLASS else LEGACY] += 1',
                            '            d = x.get("d") or "…"\n            n[d if d in D_CLASS else LEGACY] += 1')],
     "strip: an explicit blank counted as … (expect R2 red)"),
    ("d_cutoffmsg", "checker", [('; cutoff %s inclusive"', '; cutoff %s"')], "the summary's 'inclusive' word dropped"),
    ("d_domredef", "checker", [('ISO = re.compile(r"^\\d{4}-\\d{2}-\\d{2}")',
                                'ISO = re.compile(r"^\\d{4}-\\d{2}-\\d{2}")\nDOMAIN = ("✓", "✕", "⏸", "…", "ZXQ")')],
     "a SECOND DOMAIN assignment after the first: C27 reads the first literal line, Python uses the last"),
    ("r_dclassredef", "render", [('LEGACY = "legacy"', 'LEGACY = "legacy"\nD_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend", "ZXQ": "ok"}')],
     "a SECOND D_CLASS assignment after the first: C27 reads the first literal line, Python uses the last"),
    ("d_dompad", "checker", [('if "d" not in x or x["d"] in DOMAIN or not st.is_answer(x):',
                              'if "d" not in x or str(x["d"]).strip() in DOMAIN or not st.is_answer(x):')],
     "checker-side twin of R1h: a padded glyph ' ✓' admitted as in-domain while the renderer classes it legacy"),
    ("d_rowstrip", "checker", [('out.append((str(r.get("id")), ', 'out.append((str(r.get("id")).strip(), ')],
     "the ROW id normalised at its ends: C25 pins row only by a MOVE (C25k), no suffix/space/case row"),
    ("d_rowfold", "checker", [('out.append((str(r.get("id")), ', 'out.append((str(r.get("id")).lower(), ')],
     "the ROW id case-folded on the ledger side (one-sided only if some frozen row id has upper case)"),
    #  batch 3: hypotheses from the codex (GPT-6 Astra) and grok v4 answers, measured here rather than taken
    ("d_isodollar", "checker", [('ISO = re.compile(r"^\\d{4}-\\d{2}-\\d{2}")', 'ISO = re.compile(r"^\\d{4}-\\d{2}-\\d{2}$")')],
     "ISO anchored at both ends: a suffixed on/after-cutoff date in a MATCHED identity is no longer refused by date"),
    ("d_rowphaseswap", "checker", [("for (row, phase, seat, date, d, ns), why in bad:", "for (phase, row, seat, date, d, ns), why in bad:")],
     "the refusal line names the wrong row/phase (C11 counts lines, W2 checks the prefix)"),
    ("d_negcount", "checker", [("k[6] > 0", "k[6] != 0")], "a negative baseline count accepted (the disclosed >= 0 is a different edit)"),
    ("d_datelstrip", "checker", [("return v if isinstance(v, str) else", "return v.lstrip() if isinstance(v, str) else")],
     "the LEADING end of the date stripped: C25 edits only the trailing end"),
    ("d_dlstrip", "checker", [('date_str(x), str(x["d"]),', 'date_str(x), str(x["d"]).lstrip(),')],
     "the LEADING end of d stripped"),
    ("r_tipnorecord", "render", [("    if cls == LEGACY:\n", "    if cls == LEGACY and all(st.is_answer(x) for x in mine):\n")],
     "the class line dropped when a non-answer sits beside the answer (R1e asserts the record substring only)"),
    ("r_tipnotnull", "render", [("    if cls == LEGACY:\n", "    if cls == LEGACY and d is not None:\n")],
     "the class line dropped for an explicit null d (no renderer null fixture)"),
    ("r_nullpend", "render", [('    d = ent.get("d", "…")\n', '    d = ent.get("d") if ent.get("d") is not None else "…"\n')],
     "an explicit null d rendered pend instead of legacy (no renderer null fixture; HEAD has none)"),
    ("r_striplabel", "render", [("{n[LEGACY]} legacy · ", "{n[LEGACY]} approved · ")], "the strip's LABEL changed (R2 reads the numbers)"),
    ("r_sumstrip", "render", [("n[d if d in D_CLASS else LEGACY] += 1", "n[str(d).strip() if str(d).strip() in D_CLASS else LEGACY] += 1")],
     "the strip counts a padded glyph as its glyph (R2 recomputes on the shipped ledger, which has none)"),
    ("r_wsset", "render", [('{e(d) if str(d).strip() else "?"}', '{e(d) if str(d).strip(" \\t") else "?"}')],
     "the whitespace set narrowed to space+tab: a newline/NBSP-only d stays invisible (R1d pins space and tab)"),
    ("w_elif2", "precommit", [('\telse\n\t\tbad "check_entry_domain.py could not run', '\telif [ $_cedrc -eq 2 ]; then\n\t\tbad "check_entry_domain.py could not run')],
     "Q2's catch-all narrowed to rc 2: rc 127 (no python) or any other status is silently NOT a failure"),
]
if len(sys.argv) > 2:                             # a name filter, so a second batch can run a few without re-running all
    MUTANTS = [m for m in MUTANTS if m[0] in sys.argv[2:]]
T = tempfile.mkdtemp()
env0 = dict(os.environ, PYTHONIOENCODING="utf-8", **{ENV[k]: v for k, v in FILES.items()})


def controls(env):
    r = subprocess.run([sys.executable, CONTROLS], capture_output=True, text=True, encoding="utf-8", env=env)
    tally = ([l for l in r.stdout.splitlines() if l.startswith("DASHOKCLASS CONTROLS:")] or ["x: (no tally)"])[0].split(":")[1].split()[0]
    red = sorted({l.split()[0] for l in r.stdout.splitlines() if re.search(r"\sNO\s{2}", l)})
    return tally, red, "DASHOKCLASS_CONTROLS_DONE" in r.stdout


print("# fable5 extra mutants (v4 pass) -- controls %s in the MIRROR %s" % (os.path.basename(CONTROLS), M))
bt, br, bd = controls(env0)
print("BASE          %s  red=%s done=%s" % (bt, br, bd))
for name, fkey, edits, why in MUTANTS:
    src = io.open(FILES[fkey], encoding="utf-8", newline="").read()
    missing = [f for f, _ in edits if src.count(f) != 1]
    if missing:
        print("%-13s MUTANT TEXT NOT FOUND (%s)" % (name, missing[0][:70])); continue
    for f, r in edits:
        src = src.replace(f, r)
    d = os.path.join(T, name); os.makedirs(d)
    mp = os.path.join(d, os.path.basename(FILES[fkey]))
    io.open(mp, "w", encoding="utf-8", newline="").write(src)
    if fkey == "checker":
        shutil.copy(os.path.join(os.path.dirname(FILES["checker"]), "entry_domain_baseline.json"), d)
    t, red, done = controls(dict(env0, **{ENV[fkey]: mp}))
    verdict = ("killed by: " + " ".join(red)) if red else ("PASSES ALL 72" if done else "NO SENTINEL (crash?)")
    print("%-13s %-7s %-40s -- %s" % (name, t, verdict, why))
shutil.rmtree(T, ignore_errors=True)
print("FABLE_EXTRA_MUTANTS_DONE")
