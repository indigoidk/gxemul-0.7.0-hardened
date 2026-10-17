#!/usr/bin/env python3
"""The KILL TABLE for `dashokclass`'s v7 controls (2026-10-17, after the v6 pass): mutants of check_entry_domain.py,
gen_dashboard.py and precommit section Q2, each run through run_controls_v7.py.  The files under test are CTL_CHECKER /
CTL_RENDER / CTL_PRECOMMIT when set (a staged run), else the tree's; the checker's baseline is the one beside it.  A mutant must
turn at least the controls its line names red; an UNPINNED one is measured too, so its escape is a recorded result.  A
find-text that is absent is an apparatus failure.  v5 keeps the v4 table whole and appends one mutant per survivor the v4 pass
measured or traced, and per dual edge v5's CONTRACT rows; v6 appends one per survivor the v5 pass measured and per member of
each decision's generating set that v6 rows; v7 appends one per survivor the v6 pass found and per member v7 rows.  Mutants run CTL_JOBS at a time (default 4) -- each control run has
its own scratch dir -- and EVERY run must carry the controls' completion sentinel and the base run's denominator, or it is
reported INCOMPLETE and fails the table (the launcher table's v4 driver lacked this check -- GPT-6 Astra, v4 pass).
Usage: run_mutants_v7.py      (writes only to a scratch dir it removes; exit 0 only if every line holds as recorded)"""
import concurrent.futures, io, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, os.pardir, os.pardir, os.pardir))
#  CTL_CONTROLS names a FROZEN copy of the controls (each mutant run re-reads the file)
CONTROLS = os.environ.get("CTL_CONTROLS") or os.path.join(HERE, "run_controls_v7.py")
JOBS = int(os.environ.get("CTL_JOBS") or 4)
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
    #  v4: C21a-c are now refused by the SHAPE check before the walk; only C21h (a non-string note) reaches the except-arm
    ("d_ledger1", "checker", [('ledger misshapen: %s (%s: %s)" % (LEDGER, type(ex).__name__, ex)); return 2',
                               'ledger misshapen: %s (%s: %s)" % (LEDGER, type(ex).__name__, ex)); return 1')],
     ["C21h"]),
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
    #  v4 -- the v3 pass's survivors (GPT-6 Astra) and the class closure's edges
    ("d_date10", "checker", [('return v if isinstance(v, str) else', 'return v[:10] if isinstance(v, str) else')], ["C25a", "C25b"]),
    ("d_dstrip", "checker", [('date_str(x), str(x["d"]),', 'date_str(x), str(x["d"]).strip(),')], ["C25c"]),
    #  ONE-SIDED on this ledger (measured, the first v4 table): the baseline holds the RAW d and the RAW note's sha, and the
    #  frozen population carries upper-case d ("OK", "N/A") and notes a fold or strip changes -- so SOME frozen keys stop
    #  matching (on HEAD's ledger the d fold changes 1,100 of the 1,356 frozen answers' keys, the note strip 2, the note fold
    #  1,352: measured by Fable 5.1, v4 pass; v4 said "everywhere"), C1's exact within-count reds, and C25d-f cannot be the
    #  discriminator here.  d_dfold2 is the COHERENT fold of d
    #  (both sides, a two-edit DESIGN mutant like d_nonote2) and shows C25d is; no coherent note fold or strip exists, because
    #  the baseline carries only the note's sha
    ("d_dfold", "checker", [('date_str(x), str(x["d"]),', 'date_str(x), str(x["d"]).lower(),')], ["C1"]),
    ("d_dfold2", "checker", [('date_str(x), str(x["d"]),', 'date_str(x), str(x["d"]).lower(),'),
                             (LOAD, "base[tuple(k[:4]) + (k[4].lower(), k[5])] += k[6]")], ["C25d"]),
    ("d_notestrip", "checker", [(SHA, SHA.replace('str(x.get("note") or "")', 'str(x.get("note") or "").strip()'))], ["C1"]),
    ("d_notefold", "checker", [(SHA, SHA.replace('str(x.get("note") or "")', 'str(x.get("note") or "").lower()'))], ["C1"]),
    ("d_seatstrip", "checker", [('str(x.get("seat") or "")', 'str(x.get("seat") or "").strip()')], ["C25g"]),
    ("d_seatfold", "checker", [('str(x.get("seat") or "")', 'str(x.get("seat") or "").lower()')], ["C25h"]),
    ("d_phasestrip", "checker", [('str(x.get("phase") or "")', 'str(x.get("phase") or "").strip()')], ["C25i"]),
    ("d_phasefold", "checker", [('str(x.get("phase") or "")', 'str(x.get("phase") or "").lower()')], ["C25j"]),
    ("d_shaperows", "checker", [("if not isinstance(rows, list):", "if not isinstance(rows, (list, dict)):")], ["C21d"]),
    ("d_shapeents", "checker", [("        if not isinstance(ents, list):", "        if False:")], ["C21f"]),
    ("d_shapeentry", "checker", [("            if not isinstance(x, dict):", "            if False:")], ["C21e"]),
    ("d_noshape", "checker", [("    if shape:\n", "    if False:\n")], ["C21d", "C21e", "C21f"]),
    ("d_basedict", "checker", [("        if not isinstance(rows_b, list):", "        if False:")], ["C21g"]),
    ("r_norecord", "render", [('        tip.append("record: " + " — ".join(p for p in (r.get("date"), r.get("note")) if p))',
                               "        pass")], ["R1e"]),
    ("r_okonly", "render", [("    if cls == LEGACY:", '    if d == "OK":')], ["R1g"]),
    ("r_stripok", "render", [("n[d if d in D_CLASS else LEGACY] += 1", 'n["✓" if d in D_CLASS else LEGACY] += 1')], ["R2"]),
    ("r_refusallast", "render", [('tip.insert(0, "EXEMPTION REFUSED BY SECTION H: " + "; ".join(refused))',
                                  'tip.append("EXEMPTION REFUSED BY SECTION H: " + "; ".join(refused))')], ["R1f"]),
    ("w_nochecker", "precommit", [('\tbad "check_entry_domain.py MISSING', '\tgood "check_entry_domain.py MISSING')], ["W6"]),
    #  GLM 5.3, v3 pass: the ledger-unreadable rc, and the summary's count of entries within the ceiling
    ("d_unread0", "checker", [('print("APPARATUS FAIL: ledger unreadable: %s (%s)" % (LEDGER, ex)); return 2',
                               'print("APPARATUS FAIL: ledger unreadable: %s (%s)" % (LEDGER, ex)); return 0')], ["C23"]),
    ("d_summary", "checker", [("% (len(cur), len(cur) - len(bad), sum(base.values()), CUTOFF))",
                               "% (len(cur), len(cur), sum(base.values()), CUTOFF))")], ["C11"]),
    #  Fable 5.1, v3 pass (measured escapes of the v3 controls, and the class closure's members)
    ("r_tipokonly", "render", [("    if cls == LEGACY:\n", '    if cls == LEGACY and d == "OK":\n')], ["R1g"]),
    ("r_tipnonblank", "render", [("    if cls == LEGACY:\n", "    if cls == LEGACY and str(d).strip():\n")], ["R1g"]),
    ("r_clsstrip", "render", [("cls = D_CLASS.get(d, LEGACY)", "cls = D_CLASS.get(str(d).strip(), LEGACY)")], ["R1h"]),
    ("d_isheld", "checker", [("x[\"d\"] in DOMAIN or not st.is_answer(x):", "x[\"d\"] in DOMAIN or st.is_held(x):")], ["C24"]),
    ("d_nulld", "checker", [('if "d" not in x or x["d"] in DOMAIN', 'if x.get("d") is None or x["d"] in DOMAIN')], ["C26"]),
    ("d_nohint", "checker", [('        print("  -> give each a `d` from %s (or omit `d`, which renders as …); a non-answer record is exempt"',
                              '        print("  -> (hint removed) %s"')], ["C11"]),
    #  Grok 4.7, v3 pass (traced escapes of the v3 controls)
    ("d_domzxq", "checker", [('DOMAIN = ("✓", "✕", "⏸", "…")', 'DOMAIN = ("✓", "✕", "⏸", "…", "ZXQ")')], ["C27"]),
    ("r_dclasszxq", "render", [('D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}',
                                'D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend", "ZXQ": "ok"}')], ["C27"]),
    ("d_cut2days", "checker", [("if ISO.match(t[3]) and t[3][:10] >= CUTOFF:",
                                'if ISO.match(t[3]) and t[3][:10] in ("2026-10-17", "2026-10-18"):')], ["C12"]),
    ("d_baselen", "checker", [("% (len(cur), len(cur) - len(bad), sum(base.values()), CUTOFF))",
                               "% (len(cur), len(cur) - len(bad), len(base), CUTOFF))")], ["C1"]),
    ("w_nosed", "precommit", [("\t\tprintf '%s\\n' \"$_ced\" | sed 's/^/          /'\n", "")], ["W2"]),
    ("r_wsspace", "render", [('{e(d) if str(d).strip() else "?"}', '{e(d) if str(d).strip(" ") else "?"}')], ["R1d"]),
    #  v5 -- the v4 pass's survivors (Fable 5.1 measured 21, GPT-6 Astra 10 more in memory, Grok 4.7 traced 6) and each pin's dual edge
    ("d_domredef", "checker", [('CUTOFF = "2026-10-17"               # inclusive',
                                'DOMAIN = ("✓", "✕", "⏸", "…", "ZXQ")\nCUTOFF = "2026-10-17"               # inclusive')], ["C27"]),
    ("r_dclassredef", "render", [('D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}',
                                  'D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}\n'
                                  'D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend", "ZXQ": "ok"}')], ["C27"]),
    ("d_dompad", "checker", [('x["d"] in DOMAIN or not st.is_answer(x):', 'str(x["d"]).strip() in DOMAIN or not st.is_answer(x):')],
     ["C28"]),
    ("d_rowstrip", "checker", [('out.append((str(r.get("id")),', 'out.append((str(r.get("id")).strip(),')], ["C25l", "C25r"]),
    ("d_rowrstrip", "checker", [('out.append((str(r.get("id")),', 'out.append((str(r.get("id")).rstrip(),')], ["C25l"]),
    ("d_rowlstrip", "checker", [('out.append((str(r.get("id")),', 'out.append((str(r.get("id")).lstrip(),')], ["C25r"]),
    ("d_datelstrip", "checker", [('return v if isinstance(v, str) else', 'return v.lstrip() if isinstance(v, str) else')], ["C25m"]),
    ("d_dlstrip", "checker", [('date_str(x), str(x["d"]),', 'date_str(x), str(x["d"]).lstrip(),')], ["C25n"]),
    ("d_notelstrip", "checker", [(SHA, SHA.replace('str(x.get("note") or "")', 'str(x.get("note") or "").lstrip()'))], ["C25o"]),
    ("d_seatlstrip", "checker", [('str(x.get("seat") or "")', 'str(x.get("seat") or "").lstrip()')], ["C25p"]),
    ("d_phaselstrip", "checker", [('str(x.get("phase") or "")', 'str(x.get("phase") or "").lstrip()')], ["C25q"]),
    ("d_cutreason", "checker", [('bad.append((t, "dated on or after the cutoff %s" % CUTOFF))', 'bad.append((t, "refused"))')], ["C3"]),
    ("d_ceilreason", "checker", [('why = "beyond the frozen ceiling for its six fields -- a new answer, a copy, or an old one edited (classify it)"',
                                  'why = ""')], ["C6", "C9"]),
    ("d_rowphaseswap", "checker", [('% (row, phase, seat, date or "(none)", d, ns, why))',
                                    '% (phase, row, seat, date or "(none)", d, ns, why))')], ["C9"]),
    ("d_basewithin", "checker", [("% (len(cur), len(cur) - len(bad), sum(base.values()), CUTOFF))",
                                  "% (len(cur), len(cur) - len(bad), len(cur) - len(bad), CUTOFF))")], ["C12"]),
    ("d_isodollar", "checker", [('ISO = re.compile(r"^\\d{4}-\\d{2}-\\d{2}")', 'ISO = re.compile(r"^\\d{4}-\\d{2}-\\d{2}$")')], ["C12s"]),
    ("d_len7ge", "checker", [("len(k) == 7", "len(k) >= 7")], ["C17c"]),
    ("d_boolcount", "checker", [("type(k[6]) is int", "isinstance(k[6], int)")], ["C17d"]),
    ("d_negcount", "checker", [("and k[6] > 0):", "and k[6] != 0):")], ["C17e"]),
    ("d_zerocount", "checker", [("and k[6] > 0):", "and k[6] >= 0):")], ["C17f"]),
    ("d_floatcount", "checker", [("type(k[6]) is int", "type(k[6]) in (int, float)")], ["C17g"]),
    ("d_str1", "checker", [("for v in k[:6])", "for v in k[1:6])")], ["C17h"]),
    ("d_str5", "checker", [("for v in k[:6])", "for v in k[:5])")], ["C17i"]),
    ("d_isosearch", "checker", [("if ISO.match(t[3]) and t[3][:10] >= CUTOFF:", "if ISO.search(t[3]) and t[3][:10] >= CUTOFF:")],
     "UNPINNED: equivalent -- the ISO pattern is anchored with ^, so search and match agree on every string"),
    ("d_nostr", "checker", [('date_str(x), str(x["d"]),', 'date_str(x), x["d"],')], ["C26b"]),
    ("d_hintundated", "checker", [("if t[3] and not ISO.match(t[3]):", "if not ISO.match(t[3]):")], ["C6"]),
    ("d_datenone", "checker", [('date or "(none)", d, ns, why))', 'date, d, ns, why))')], ["C6"]),
    ("d_cutoffmsg", "checker", [('cutoff %s inclusive"', 'cutoff %s"')], ["C1", "C11", "C12"]),
    ("d_rowsabsent", "checker", [('rows = ledger.get("rows")', 'rows = ledger.get("rows", [])')], ["C21i"]),
    ("r_sumstrip", "render", [("n[d if d in D_CLASS else LEGACY] += 1",
                               "n[str(d).strip() if str(d).strip() in D_CLASS else LEGACY] += 1")], ["R2b"]),
    ("r_tipnorecord", "render", [("    if cls == LEGACY:\n", "    if cls == LEGACY and all(st.is_answer(x) for x in mine):\n")], ["R1e"]),
    ("r_tipnotnull", "render", [("    if cls == LEGACY:\n", "    if cls == LEGACY and d is not None:\n")], ["R1g"]),
    ("r_nullpend", "render", [('    d = ent.get("d", "…")', '    d = ent.get("d") if ent.get("d") is not None else "…"')], ["R1n", "R1g"]),
    ("r_striplabel", "render", [("{n[LEGACY]} legacy · ", "{n[LEGACY]} approved · ")], ["R2"]),
    ("r_wsset", "render", [('{e(d) if str(d).strip() else "?"}', '{e(d) if str(d).strip(" \\t") else "?"}')], ["R1d"]),
    ("r_css0", "render", [("font-size:11px; }}", "font-size:0; }}")], ["R5"]),
    ("r_cssoutline", "render", [("td.c.legacy {{ outline:1px dashed var(--line); outline-offset:-3px; }}", "td.c.legacy {{ outline:0; }}")],
     ["R5"]),
    ("w_elif2", "precommit", [('\telse\n\t\tbad "check_entry_domain.py could not run',
                               '\telif [ $_cedrc -eq 2 ]; then\n\t\tbad "check_entry_domain.py could not run')], ["W7", "W8"]),
    ("w_no2to1", "precommit", [('python "$CED" 2>&1); _cedrc=$?', 'python "$CED"); _cedrc=$?')], ["W7"]),
    #  v6 -- the v5 pass's survivors (GLM 5.3 and GPT-6 Astra measured) and each decision's GENERATING SET
    ("d_domglobals", "checker", [('CUTOFF = "2026-10-17"               # inclusive',
                                  'globals()["DOMAIN"] = DOMAIN + ("ZXQ",)\nCUTOFF = "2026-10-17"               # inclusive')], ["C27"]),
    ("d_domglobalsaug", "checker", [('CUTOFF = "2026-10-17"               # inclusive',
                                     'globals()["DOMAIN"] += ("ZXQ",)\nCUTOFF = "2026-10-17"               # inclusive')], ["C27"]),
    ("d_domexec", "checker", [('CUTOFF = "2026-10-17"               # inclusive',
                               'exec(\'DOMAIN = DOMAIN + ("ZXQ",)\')\nCUTOFF = "2026-10-17"               # inclusive')], ["C27"]),
    ("d_domsetattr", "checker", [('CUTOFF = "2026-10-17"               # inclusive',
                                  'setattr(sys.modules[__name__], "DOMAIN", DOMAIN + ("ZXQ",))\nCUTOFF = "2026-10-17"               # inclusive')],
     ["C27"]),
    ("d_domarg", "checker", [("def off_domain_answers(ledger):", 'def off_domain_answers(ledger, DOMAIN=DOMAIN + ("ZXQ",)):')], ["C27"]),
    ("r_dclassglobals", "render", [('D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}',
                                    'D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}\nglobals()["D_CLASS"] = dict(D_CLASS, ZXQ="ok")')],
     ["C27"]),
    ("r_dclassupdate", "render", [('D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}',
                                   'D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}\nD_CLASS.update(ZXQ="ok")')], ["C27"]),
    ("r_dclasssetitem", "render", [('D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}',
                                    'D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}\nD_CLASS["ZXQ"] = "ok"')], ["C27"]),
    ("d_dompadr", "checker", [('x["d"] in DOMAIN or not st.is_answer(x):', 'str(x["d"]).rstrip() in DOMAIN or not st.is_answer(x):')],
     ["C28b"]),
    ("r_clsrstrip", "render", [("cls = D_CLASS.get(d, LEGACY)", "cls = D_CLASS.get(str(d).rstrip(), LEGACY)")], ["R1h"]),
    ("d_strskip1", "checker", [("for v in k[:6])", "for v in k[:1] + k[2:6])")], ["C17j"]),
    ("d_strskip2", "checker", [("for v in k[:6])", "for v in k[:2] + k[3:6])")], ["C17k"]),
    ("d_strskip3", "checker", [("for v in k[:6])", "for v in k[:3] + k[4:6])")], ["C17l"]),
    ("d_strskip4", "checker", [("for v in k[:6])", "for v in k[:4] + k[5:6])")], ["C17m"]),
    ("d_isowidthy", "checker", [('ISO = re.compile(r"^\\d{4}-\\d{2}-\\d{2}")', 'ISO = re.compile(r"^\\d{4,5}-\\d{2}-\\d{2}")')], ["C12w"]),
    ("d_isowidthm", "checker", [('ISO = re.compile(r"^\\d{4}-\\d{2}-\\d{2}")', 'ISO = re.compile(r"^\\d{4}-\\d{1,2}-\\d{2}")')], ["C12w"]),
    ("d_isowidthd", "checker", [('ISO = re.compile(r"^\\d{4}-\\d{2}-\\d{2}")', 'ISO = re.compile(r"^\\d{4}-\\d{2}-\\d{1,2}")')], ["C12w"]),
    ("d_isosep1", "checker", [('ISO = re.compile(r"^\\d{4}-\\d{2}-\\d{2}")', 'ISO = re.compile(r"^\\d{4}.\\d{2}-\\d{2}")')], ["C12w"]),
    ("d_isosep2", "checker", [('ISO = re.compile(r"^\\d{4}-\\d{2}-\\d{2}")', 'ISO = re.compile(r"^\\d{4}-\\d{2}.\\d{2}")')], ["C12w"]),
    ("d_hinttext", "checker", [("; a non-answer record is exempt", "; all records need classification")], ["C11"]),
    ("d_hintalways", "checker", [('    if bad:\n        print("  -> give each a `d` from %s (or omit `d`, which renders as …); a non-answer record is exempt"\n'
                                  '              % " ".join(DOMAIN))\n        return 1\n',
                                  '    print("  -> give each a `d` from %s (or omit `d`, which renders as …); a non-answer record is exempt"\n'
                                  '          % " ".join(DOMAIN))\n    if bad:\n        return 1\n')], ["C1"]),
    ("d_reconfreplace", "checker", [('reconfigure(errors="backslashreplace")', 'reconfigure(errors="replace")')], ["C20"]),
    ("d_notelatin1", "checker", [('str(x.get("note") or "").encode("utf-8")', 'str(x.get("note") or "").encode("latin-1")')], ["C20b"]),
    ("d_notenostr", "checker", [('str(x.get("note") or "").encode("utf-8")', '(x.get("note") or "").encode("utf-8")')], ["C21k"]),
    ("d_entriesdef1", "checker", [('        ents = r.get("entries", [])', '        ents = r.get("entries")')], ["C21j"]),
    ("d_entriesdef2", "checker", [('        for x in r.get("entries", []):', '        for x in r.get("entries"):')], ["C21j"]),
    ("d_phasenone", "checker", [('str(x.get("phase") or "")', 'str(x.get("phase"))')], ["C29"]),
    ("d_seatnone", "checker", [('str(x.get("seat") or "")', 'str(x.get("seat"))')], ["C29"]),
    ("r_tipinsertm2", "render", [('tip.insert(0, "legacy -- verdict unclassified:', 'tip.insert(-2, "legacy -- verdict unclassified:')],
     ["R1o"]),
    ("r_tipnoev", "render", [("    if cls == LEGACY:\n", '    if cls == LEGACY and not ent.get("ev"):\n')], ["R1o"]),
    ("r_escstrip", "render", [("e = lambda t: html.escape(str(t), quote=True)", "e = lambda t: html.escape(str(t).strip(), quote=True)")],
     ["R1h"]),
    ("r_cssoverride", "render", [(".c.legacy .g {{ color:var(--muted); font-style:italic; font-size:11px; }}",
                                  ".c.legacy .g {{ color:var(--muted); font-style:italic; font-size:11px; }}\n.c.legacy .g {{ font-size:0; }}")],
     ["R5"]),
    ("w_tail1", "precommit", [("could not run (rc $_cedrc): $(printf '%s\\n' \"$_ced\" | head -1)\"",
                               "could not run (rc $_cedrc): $(printf '%s\\n' \"$_ced\" | tail -1)\"")], ["W7"]),
    #  v6 -- Fable 5.1's v5-pass sweep (`extra_mutants_v5*.py'), each escape rebuilt here verbatim
    ("r_tippend", "render", [("    if cls == LEGACY:\n", '    if cls in (LEGACY, "pend"):\n')], ["R1p"]),
    ("r_tipnotok", "render", [("    if cls == LEGACY:\n", '    if cls != "ok":\n')], ["R1p"]),
    ("r_tipempty", "render", [("    if cls == LEGACY:\n", "    if cls == LEGACY and tip:\n")], ["R1q"]),
    ("r_glyphstrip", "render", [('{e(d) if str(d).strip() else "?"}', '{e(str(d).strip()) if str(d).strip() else "?"}')], ["R1h"]),
    ("r_wsset4", "render", [('{e(d) if str(d).strip() else "?"}', '{e(d) if str(d).strip(" " + chr(9) + chr(10) + chr(160)) else "?"}')],
     ["R1w"]),
    ("r_sumcrash", "render", [('D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}',
                               'D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}\nD_CLASS["OK"] = "ok"')], ["C27", "R2"]),
    ("d_domusesite", "checker", [('x["d"] in DOMAIN or not st.is_answer(x):', 'x["d"] in DOMAIN + ("ZXQ",) or not st.is_answer(x):')],
     ["C27"]),
    ("d_strnone", "checker", [("all(isinstance(v, str) for v in k[:6])", "all(isinstance(v, (str, type(None))) for v in k[:6])")],
     ["C17n"]),
    ("d_hinttail", "checker", [(' (or omit `d`, which renders as …); a non-answer record is exempt"', '"')], ["C11"]),
    ("d_isodigits", "checker", [('ISO = re.compile(r"^\\d{4}-\\d{2}-\\d{2}")', 'ISO = re.compile(r"^\\d{4}-\\d{1,2}-\\d{1,2}")')], ["C12w"]),
    ("w_q2paren", "precommit", [('ceiling (a new one, a copy, or an old one edited):"', 'ceiling:"')], ["W2"]),
    #  v6 -- Grok 4.7's v5-pass survivors, each rebuilt here verbatim
    ("r_tipnows", "render", [("    if cls == LEGACY:\n", '    if cls == LEGACY and d not in ("\\n", "\\xa0"):\n')], ["R1g"]),
    ("r_tipnows2", "render", [("    if cls == LEGACY:\n", '    if cls == LEGACY and d != "\\x0b":\n')], ["R1w"]),
    ("r_tipall", "render", [("    if cls == LEGACY:\n", "    if cls:\n")], ["R1p"]),
    ("d_hintjoin", "checker", [('% " ".join(DOMAIN))', '% "ZZZ")')], ["C11"]),
    ("d_domsysmod", "checker", [('CUTOFF = "2026-10-17"               # inclusive',
                                 'sys.modules[__name__].DOMAIN = DOMAIN + ("ZXQ",)\nCUTOFF = "2026-10-17"               # inclusive')],
     ["C27"]),
    ("d_isotrunc", "checker", [('ISO = re.compile(r"^\\d{4}-\\d{2}-\\d{2}")', 'ISO = re.compile(r"^\\d{4}-\\d{2}-")')], ["C12w"]),
    ("w_elifne3", "precommit", [('\telse\n\t\tbad "check_entry_domain.py could not run',
                                 '\telif [ $_cedrc -ne 3 ]; then\n\t\tbad "check_entry_domain.py could not run')], ["W9"]),
    ("w_named", "precommit", [("\t\tprintf '%s\\n' \"$_ced\" | sed 's/^/          /'\n",
                               "\t\tprintf '%s\\n' \"OFF-DOMAIN ANSWER  row redacted\"\n")], ["W2"]),
    #  v7 -- the v6 pass's survivors (four seats), each rebuilt here verbatim, and the generating-set members v7 rows
    ("d_domnonliteral", "checker", [('DOMAIN = ("✓", "✕", "⏸", "…")', 'DOMAIN = tuple(("✓", "✕", "⏸", "…"))')], ["C27"]),
    ("d_domattrexec", "checker", [('CUTOFF = "2026-10-17"               # inclusive',
                                   'import builtins\nbuiltins.exec(\'DOMAIN = DOMAIN + ("ZXQ",)\')\nCUTOFF = "2026-10-17"               # inclusive')],
     ["C27"]),
    ("d_dommain", "checker", [('if __name__ == "__main__":\n',
                               'if __name__ == "__main__":\n    import builtins\n    builtins.globals()["DOM" + "AIN"] = ("✓", "✕", "⏸", "…", "ZXQ")\n')],
     ["C27"]),
    ("d_domuseinline", "checker", [('x["d"] in DOMAIN or not st.is_answer(x):', 'x["d"] in ("✓", "✕", "⏸", "…", "ZXQ") or not st.is_answer(x):')],
     ["C27"]),
    ("r_dclassmatchrest", "render", [('D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}',
                                      'D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}\n'
                                      'match {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend", "ZXQ": "ok"}:\n'
                                      '    case {**D_CLASS}:\n        pass')], ["C27"]),
    ("r_dclassalias", "render", [('D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}',
                                  'D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}\n_e = exec\n_e(\'D_CLASS["ZXQ"] = "ok"\')')],
     ["C27"]),
    ("r_dclassbuiltins", "render", [('D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}',
                                     'D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}\nimport builtins\n'
                                     'builtins.exec(\'D_CLASS["ZXQ"] = "ok"\')')], ["C27"]),
    ("r_dclasssetattr", "render", [('D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}',
                                    'D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}\nimport builtins as _b, sys as _s\n'
                                    '_b.setattr(_s.modules[__name__], "D_CLASS", {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend", "ZXQ": "ok"})')],
     ["C27"]),
    ("r_dclassfglobals", "render", [('D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}',
                                     'D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}\nimport sys as _s2\n'
                                     '_s2._getframe().f_globals["D_CLASS"] = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend", "ZXQ": "ok"}')],
     ["C27"]),
    ("r_dclassuseinline", "render", [("cls = D_CLASS.get(d, LEGACY)",
                                      'cls = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend", "ZXQ": "ok"}.get(d, LEGACY)')], ["C27"]),
    ("r_sumuseinline", "render", [("n[d if d in D_CLASS else LEGACY] += 1", 'n[d if d in ("✓", "⏸", "✕", "…", "ZXQ") else LEGACY] += 1')],
     ["C27"]),
    ("d_rowlist", "checker", [("        if not isinstance(r, dict):", "        if not isinstance(r, (dict, list)):")], ["C21l"]),
    ("d_entrylist", "checker", [("            if not isinstance(x, dict):", "            if not isinstance(x, (dict, list)):")], ["C21m"]),
    ("d_rowidnone", "checker", [('str(r.get("id"))', 'str(r.get("id") or "")')], ["C29b"]),
    ("d_isoyear3", "checker", [('ISO = re.compile(r"^\\d{4}-\\d{2}-\\d{2}")', 'ISO = re.compile(r"^\\d{3,4}-\\d{2}-\\d{2}")')], ["C12w"]),
    ("d_isomonth3", "checker", [('ISO = re.compile(r"^\\d{4}-\\d{2}-\\d{2}")', 'ISO = re.compile(r"^\\d{4}-\\d{2,3}-\\d{2}")')], ["C12w"]),
    ("r_tipbadge", "render", [("    if cls == LEGACY:\n", "    if cls == LEGACY or badge:\n")], ["R1p2"]),
    ("r_tipev", "render", [("    if cls == LEGACY:\n", '    if cls == LEGACY or ent.get("ev"):\n')], ["R1p2"]),
    ("r_tipgradeonly", "render", [("    if cls == LEGACY:\n", '    if cls == LEGACY and (not ent.get("ev") or ent.get("grade")):\n')], ["R1o2"]),
    ("r_tipevonly", "render", [("    if cls == LEGACY:\n", '    if cls == LEGACY and (not ent.get("grade") or ent.get("ev")):\n')], ["R1o2"]),
    ("r_tipbadges", "render", [("    if cls == LEGACY:\n", '    if cls == LEGACY and badge != "s":\n')], ["R1o2"]),
    ("r_css2block", "render", [("</style>", "</style><style>.c.legacy .g {{ font-size:0; }}</style>")], ["R5"]),
    ("r_cssescape", "render", [(".c.legacy .g {{ color:var(--muted); font-style:italic; font-size:11px; }}",
                                ".c.legacy .g {{ color:var(--muted); font-style:italic; font-size:11px; }}\n.c.lega\\\\63 y .g {{ font-size:0; }}")],
     ["R5"]),
    ("r_sumcounterkey", "render", [("n[d if d in D_CLASS else LEGACY] += 1", "n[d if d in n else LEGACY] += 1")], ["R2b"]),
]
T = tempfile.mkdtemp()
env0 = dict(os.environ, PYTHONIOENCODING="utf-8", **{ENV[k]: v for k, v in FILES.items()})


def controls(env):
    r = subprocess.run([sys.executable, CONTROLS], capture_output=True, text=True, encoding="utf-8", env=env)
    tally = ([l for l in r.stdout.splitlines() if l.startswith("DASHOKCLASS CONTROLS:")] or ["x: (no tally)"])[0].split(":")[1].split()[0]
    #  one space can precede the status: a label longer than its padded column leaves no padding
    red = sorted({l.split()[0] for l in r.stdout.splitlines() if re.search(r"\sNO\s{2}", l)})
    return r, tally, red, "DASHOKCLASS_CONTROLS_DONE" in r.stdout


print("# dashokclass kill table (v7) -- controls %s, %d at a time" % (os.path.basename(CONTROLS), JOBS))
for k in ("checker", "render", "precommit"):
    print("#   %-9s %s" % (k, FILES[k]))
base, btally, bred, bdone = controls(env0)
print("BASE          %s" % btally)
den = btally.split("/")[-1]
if base.returncode != 0 or not bdone or bred:
    print("APPARATUS FAIL: the base run is not clean (red: %s)" % (" ".join(bred) or "none"))
    shutil.rmtree(T, ignore_errors=True); sys.exit(9)
def one(m):
    name, fkey, edits, named = m
    src = io.open(FILES[fkey], encoding="utf-8", newline="").read()
    missing = [f for f, _ in edits if src.count(f) != 1]
    if missing:
        return False, "%-15s MUTANT TEXT NOT FOUND (%s)" % (name, missing[0][:60])
    for f, r in edits:
        src = src.replace(f, r)
    d = os.path.join(T, name)
    os.makedirs(d)
    mp = os.path.join(d, os.path.basename(FILES[fkey]))
    io.open(mp, "w", encoding="utf-8", newline="").write(src)
    if fkey == "checker":      # the baseline travels with the checker
        shutil.copy(os.path.join(os.path.dirname(FILES["checker"]), "entry_domain_baseline.json"), d)
    r, tally, red, done = controls(dict(env0, **{ENV[fkey]: mp}))
    if not done or tally.split("/")[-1] != den:
        return False, "%-15s %-7s INCOMPLETE run (no sentinel, or a denominator other than %s)" % (name, tally, den)
    if isinstance(named, str):
        good = not red
        verdict = "escapes (as recorded)" if good else "CAUGHT by: %s (unexpected)" % " ".join(red)
    else:
        good = all(n in red for n in named)
        verdict = ("killed by: " + " ".join(red)) if good else "NOT KILLED as named (red: %s)" % (" ".join(red) or "none")
    return good, "%-15s %-7s %-66s [%s]" % (name, tally, verdict, named if isinstance(named, str) else " ".join(named))


with concurrent.futures.ThreadPoolExecutor(max_workers=JOBS) as pool:
    results = list(pool.map(one, MUTANTS))
ok = 0
for good, line in results:
    ok += good
    print(line)
shutil.rmtree(T, ignore_errors=True)
print("KILL TABLE: %d/%d as recorded" % (ok, len(MUTANTS)))
print("DASHOKCLASS_MUTANTS_DONE")
sys.exit(0 if ok == len(MUTANTS) else 1)
