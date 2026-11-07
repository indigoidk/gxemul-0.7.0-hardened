#!/usr/bin/env python3
"""holdphase evidence deriver -- reads ONLY the HEAD copies extracted beside it.

    ledger_HEAD.json      = git show HEAD:tools/pipeline/ledger.json
    HEAD_stage_tokens.py  = git show HEAD:tools/pipeline/stage_tokens.py

Classification (is_held / held_seats / is_answer / live_holds / exempts_stage /
stage_token_problems) is IMPORTED from the HEAD stage_tokens.py, so a marker and an
answer mean here exactly what they mean to the three tools.  This file adds only the
ANY-PHASE variant and per-marker bookkeeping, and it cross-checks its own SAME-PHASE
result against st.live_holds() stage by stage.  It runs no gate and no tool main();
the per-stage tool classifications in section 7 are re-statements of the cited lines.

Writes analysis.out, markers.tsv, differing.tsv, frag_*.md (utf-8, LF).
"""
import collections
import importlib.util
import io
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("st_head", os.path.join(HERE, "HEAD_stage_tokens.py"))
st = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(st)

led = json.load(io.open(os.path.join(HERE, "ledger_HEAD.json"), encoding="utf-8"))
ROWS = led["rows"]
RBY = {r["id"]: r for r in ROWS}
ROSTER = [s["id"] for s in led["seats"]]
N_SEATS = len(ROSTER)

#  constants copied from the HEAD tools (cited in EVIDENCE.md)
SP_STAGES = ("assess", "research", "review")     # check_stage_panels.py:65
SP_CUTOFF = "2026-08-16"                         # check_stage_panels.py:40
FQ_FLAGSHIP = "fable5"                           # check_fable_queue.py:43
FQ_CUTOFF = "2026-08-16"                         # check_fable_queue.py:51
LIT = st.HELD

OUT = io.open(os.path.join(HERE, "analysis.out"), "w", encoding="utf-8", newline="\n")


def w(s=""):
    OUT.write(s + "\n")


def frag(name, text):
    with io.open(os.path.join(HERE, "frag_%s.md" % name), "w", encoding="utf-8", newline="\n") as f:
        f.write(text.rstrip("\n") + "\n")


def note(e):
    return e.get("note") or ""


def nlen(e):
    return len(note(e).strip())


def plain(t, n):
    t = " ".join(t.replace("*", "").replace("`", "'").replace("|", "/").split())
    return t if len(t) <= n else t[:n].rstrip() + "..."


def discharges(ents, h, seat, same_phase, cmp):
    """entries that discharge marker h for `seat` by the live_holds predicate
    (stage_tokens.py:106-107); the pool is the marker's phase, or the whole row."""
    hd = h.get("date") or ""
    out = []
    for j, e in enumerate(ents):
        if same_phase and e.get("phase") != h.get("phase"):
            continue
        if (e.get("seat") or "").lower() != seat or not st.is_answer(e):
            continue
        if cmp(e.get("date") or "", hd):
            out.append((j, e))
    return out


GT = lambda a, b: a > b
GE = lambda a, b: a >= b

# ------------------------------------------------------------------ 1. literal census
raw = io.open(os.path.join(HERE, "ledger_HEAD.json"), encoding="utf-8").read()
fieldc = collections.Counter()
for r in ROWS:
    for k, v in r.items():
        if k != "entries" and isinstance(v, str) and LIT in v:
            fieldc["row." + k] += v.count(LIT)
    for e in r.get("entries", []):
        for k, v in e.items():
            if isinstance(v, str) and LIT in v:
                fieldc["entry." + k] += v.count(LIT)
w("== 1. LITERAL CENSUS")
w("literal %r in the whole file text: %d" % (LIT, raw.count(LIT)))
for k, v in sorted(fieldc.items()):
    w("  %-22s %3d" % (k, v))
w("is_held() reads entry.note only (stage_tokens.py:53-54); the other fields are read by none of the three tools.")
for r in ROWS:
    for k, v in r.items():
        if k != "entries" and isinstance(v, str) and LIT in v:
            w("  outside note: row.%s on %s x%d (row-level prose)" % (k, r["id"], v.count(LIT)))
    for i, e in enumerate(r.get("entries", [])):
        for k, v in e.items():
            if k != "note" and isinstance(v, str) and LIT in v:
                w("  outside note: entry.%s on %s[%d] x%d -- this entry's note is %s"
                  % (k, r["id"], i, v.count(LIT), "a MARKER" if st.is_held(e)
                     else ("DEFANGED" if "HELD-AWAITING-SEAT" in note(e) else "neither")))
w("rows %d   entries %d   roster %d %s" % (len(ROWS), sum(len(r.get("entries", [])) for r in ROWS), N_SEATS, ROSTER))

# ------------------------------------------------------------------ 2. per-marker units
units, marker_entries, multi_lit = [], 0, 0
for r in ROWS:
    ents = r.get("entries", [])
    for i, h in enumerate(ents):
        if not st.is_held(h):
            continue
        marker_entries += 1
        multi_lit += note(h).count(LIT) > 1
        named = st.held_seats(h)
        base = dict(row=r["id"], state=r.get("state"), idx=i, phase=h.get("phase"), date=h.get("date") or "")
        if not named:
            units.append(dict(base, seat=st.MALFORMED, malformed=True, same=[], any=[], same_ge=[], any_ge=[]))
            continue
        for s in dict.fromkeys(named):
            units.append(dict(base, seat=s, malformed=False,
                              same=discharges(ents, h, s, True, GT), any=discharges(ents, h, s, False, GT),
                              same_ge=discharges(ents, h, s, True, GE), any_ge=discharges(ents, h, s, False, GE)))
NU = len(units)
stages_m = sorted({(u["row"], u["phase"]) for u in units})
w()
w("== 2. MARKERS")
w("marker entries %d (with >1 literal in one note: %d)   marker-seats (entry x named seat) %d   malformed %d"
  % (marker_entries, multi_lit, NU, sum(u["malformed"] for u in units)))
w("stages (row, phase) carrying a marker %d   rows %d" % (len(stages_m), len({u["row"] for u in units})))
pc = collections.Counter(u["phase"] for u in units)
w("marker-seats by phase: %s (of %d)" % (", ".join("%s %d" % kv for kv in sorted(pc.items())), NU))
w("marker-seats by seat:  %s (of %d)" % (", ".join("%s %d" % kv for kv in collections.Counter(u["seat"] for u in units).most_common()), NU))

# ------------------------------------------------------------------ 3. cross-check
mism = []
for (rid, ph) in stages_m:
    grp = [e for e in RBY[rid].get("entries", []) if e.get("phase") == ph]
    mine = {u["seat"] for u in units if u["row"] == rid and u["phase"] == ph and not u["same"]}
    if set(st.live_holds(grp)) != mine:
        mism.append((rid, ph))
w()
w("== 3. CROSS-CHECK  per-marker SAME-PHASE '>' vs st.live_holds(phase group): %d stages compared, %d mismatches %s"
  % (len(stages_m), len(mism), mism))

# ------------------------------------------------------------------ 4. the two rules
same_d = sum(bool(u["same"]) for u in units)
any_d = sum(bool(u["any"]) for u in units)
differ = [u for u in units if bool(u["same"]) != bool(u["any"])]
rev = [u for u in units if u["same"] and not u["any"]]


# a (row, phase, seat) is live if ANY marker naming that seat in that stage is undischarged
def live_triples(key):
    by = collections.defaultdict(list)
    for u in units:
        by[(u["row"], u["phase"], u["seat"])].append(bool(u[key]))
    return sorted(k for k, v in by.items() if not all(v))


lt_same, lt_any = live_triples("same"), live_triples("any")
all_triples = sorted({(u["row"], u["phase"], u["seat"]) for u in units})
ls_same = sorted({(a, b) for a, b, _ in lt_same})
ls_any = sorted({(a, b) for a, b, _ in lt_any})
w()
w("== 4. RULES")
w("unit marker-seat (of %d): SAME-PHASE live %d / discharged %d;  ANY-PHASE live %d / discharged %d;  DIFFER %d;  same-only %d"
  % (NU, NU - same_d, same_d, NU - any_d, any_d, len(differ), len(rev)))
w("unit distinct (row, phase, seat) (of %d): SAME-PHASE live %d;  ANY-PHASE live %d;  differ %d"
  % (len(all_triples), len(lt_same), len(lt_any), len(set(lt_same) - set(lt_any))))
w("unit stage (row, phase) (of %d): with a live hold SAME-PHASE %d;  ANY-PHASE %d;  stages holding a DIFFER marker-seat %d"
  % (len(stages_m), len(ls_same), len(ls_any), len({(u['row'], u['phase']) for u in differ})))
w("per phase (marker-seats):  n / SAME-dis / ANY-dis / differ")
for ph in sorted(pc):
    us = [u for u in units if u["phase"] == ph]
    w("  %-9s %3d / %3d / %3d / %3d" % (ph, len(us), sum(bool(u["same"]) for u in us),
                                        sum(bool(u["any"]) for u in us), sum(bool(u["same"]) != bool(u["any"]) for u in us)))
ge_flip = [u for u in units if bool(u["same_ge"]) != bool(u["same"])]
w("side: '>=' instead of '>' -> SAME-PHASE discharged %d of %d, ANY-PHASE %d of %d; same-phase flips %d: %s"
  % (sum(bool(u["same_ge"]) for u in units), NU, sum(bool(u["any_ge"]) for u in units), NU, len(ge_flip),
     ", ".join("%s/%s/%s" % (u["row"], u["phase"], u["seat"]) for u in ge_flip)))

# ------------------------------------------------------------------ 5. real length / what discharges
w()
w("== 5. REAL-LENGTH CLAUSE (no tool tests length)")
dis_same = [u for u in units if u["same"]]
best = sorted(max(nlen(e) for _, e in u["same"]) for u in dis_same)
w("SAME-PHASE-discharged marker-seats %d of %d; longest discharging note per marker-seat: min %d, median %d, max %d chars"
  % (len(dis_same), NU, best[0], best[len(best) // 2], best[-1]))
for L in (1, 40, 100, 200):
    w("  discharged ONLY by notes shorter than %3d chars: %d of %d" % (L, sum(b < L for b in best), len(dis_same)))
for u in dis_same:
    if max(nlen(e) for _, e in u["same"]) < 100:
        w("    %s [%d] %s/%s/%s <- %s" % (u["row"], u["idx"], u["phase"], u["seat"], u["date"],
                                        "; ".join("[%d] %s (%d) %r" % (j, e.get("date"), nlen(e), plain(note(e), 90))
                                                  for j, e in u["same"])))
w("  discharged ONLY by defanged copies: %d of %d;  ONLY by RE_READ entries: %d of %d"
  % (sum(all("HELD-AWAITING-SEAT" in note(e) for _, e in u["same"]) for u in dis_same), len(dis_same),
     sum(all(st.RE_READ in note(e) for _, e in u["same"]) for u in dis_same), len(dis_same)))
b2 = sorted(max(nlen(e) for _, e in u["any"]) for u in differ)
w("DIFFER set: longest other-phase discharging note per marker-seat: min %d, max %d" % (b2[0], b2[-1]))
w("  DIFFER discharged ONLY by defanged copies: %d of %d"
  % (sum(all("HELD-AWAITING-SEAT" in note(e) for _, e in u["any"]) for u in differ), len(differ)))

# ------------------------------------------------------------------ 6. tool scope at HEAD (same-phase rule)
def fq_gate(r, ph):
    """the filters at check_fable_queue.py:122-133 that decide whether :136 is reached."""
    if ph == "regress":
        return "regress (:122)"
    grp = [e for e in r.get("entries", []) if e.get("phase") == ph]
    seats, newest, ann = set(), "", False
    for e in grp:
        if st.exempts_stage(e):
            ann = True
        if st.is_held(e) or not st.is_answer(e):
            continue
        seats.add(e.get("seat"))
        newest = max(newest, e.get("date", ""))
    if len(seats) < 2:
        return "<2 seats (:124)"
    if FQ_FLAGSHIP in seats:
        return "fable5 answered (:126)"
    if ann and not st.stage_token_problems(grp):
        return "exempt (:130)"
    if newest < FQ_CUTOFF:
        return "pre-cutoff (:132)"
    return "REACHED"


L = lt_same
sp_n = [t for t in L if t[1] in SP_STAGES]
fqc = collections.Counter(fq_gate(RBY[t[0]], t[1]) for t in L)
closed = [t for t in L if RBY[t[0]].get("state") == "closed"]
closed_sp = [t for t in closed if t[1] in SP_STAGES]
w()
w("== 6. TOOL SCOPE AT HEAD over the %d live (row, phase, seat) holds (%d stages)" % (len(L), len(ls_same)))
w("  live holds by phase: %s" % dict(sorted(collections.Counter(t[1] for t in L).items())))
w("  check_stage_panels evaluates (phase in STAGES): %d of %d" % (len(sp_n), len(L)))
w("  check_fable_queue reaches its live test (:136): %d of %d; skipped: %s"
  % (fqc["REACHED"], len(L), dict((k, v) for k, v in fqc.items() if k != "REACHED")))
w("  gen_codex_wall lists: %d of %d (0 malformed, 0 unknown seats)" % (len(L), len(L)))
w("  live holds on CLOSED rows: %d of %d, by phase %s; flagged CLOSED-WHILE-HELD by check_stage_panels: %d"
  % (len(closed), len(L), dict(collections.Counter(t[1] for t in closed)), len(closed_sp)))
w("  closed-row live holds outside regress: %s" % [t for t in closed if t[1] != "regress"])
frag("scope", "\n".join([
    "| tool | live holds it evaluates (of %d) | not evaluated |" % len(L),
    "|---|---|---|",
    "| `check_stage_panels.py` | %d | %d: every `regress` and `design` hold (`:65`, `:190`) |" % (len(sp_n), len(L) - len(sp_n)),
    "| `check_fable_queue.py` | %d | %d: %s |" % (fqc["REACHED"], len(L) - fqc["REACHED"],
                                                 ", ".join("%s %d" % (k, v) for k, v in sorted(fqc.items()) if k != "REACHED")),
    "| `gen_codex_wall.py` | %d | 0 |" % len(L),
]))


# ------------------------------------------------------------------ 7. consequence of switching live_holds to ANY-PHASE
def live_set(r, ph, any_phase):
    ents = r.get("entries", [])
    grp = [e for e in ents if e.get("phase") == ph]
    if not any_phase:
        return st.live_holds(grp)
    out = []
    for h in grp:
        if not st.is_held(h):
            continue
        named = st.held_seats(h)
        if not named and st.MALFORMED not in out:
            out.append(st.MALFORMED)
        for s in named:
            if not discharges(ents, h, s, False, GT) and s not in out:
                out.append(s)
    return out


def sp_class(r, ph, live):
    """check_stage_panels.py:166-251 for one stage (reached only for STAGES, :190)."""
    if ph not in SP_STAGES:
        return "not evaluated"
    grp = [e for e in r.get("entries", []) if e.get("phase") == ph]
    seats, newest, ann = set(), "", False
    for e in grp:
        if st.exempts_stage(e):
            ann = True
        if st.is_held(e) or not st.is_answer(e):
            continue
        seats.add(e.get("seat"))
        newest = max(newest, e.get("date", ""))
    closed = r.get("state") == "closed"
    if not seats:
        return ("FAIL closed-while-held" if closed else "HELD 0/9") if live else "skipped"
    if len(seats) >= N_SEATS and not live:
        return "complete"
    if live:
        return "FAIL closed-while-held" if closed else "HELD %d/9" % len(seats)
    if len(seats) == 1:
        return "filed 1/9"
    if ann and st.stage_token_problems(grp):
        return "FAIL token-refused"
    if newest < SP_CUTOFF or ann:
        return "grandfathered"
    return "FAIL incomplete %d/9" % len(seats)


def fq_class(r, ph, live):
    """check_fable_queue.py:121-143 for one stage."""
    g = fq_gate(r, ph)
    if g != "REACHED":
        return "not evaluated"
    held = any(st.is_held(e) for e in r.get("entries", []) if e.get("phase") == ph)
    return "HELD" if (held and live) else "FAIL short, not held"


def wall_list(r, ph, live):
    """gen_codex_wall.py:156-182 for one phase: the seats it lists."""
    got = set()
    for e in r.get("entries", []):
        if e.get("phase", "?") != ph:
            continue
        m = st.HELD_SEATS.search(note(e))
        if not m:
            continue
        for s in (x.strip().lower() for x in m.group(1).split(",")):
            if s and (s not in ROSTER or s in live):
                got.add(s if s in ROSTER else "?" + s)
    return ",".join(sorted(got)) or "(not listed)"


dstages = sorted({(u["row"], u["phase"]) for u in differ})
chg = collections.Counter()
lines = ["| stage | row state | live, same -> any | `check_stage_panels` | `check_fable_queue` | `gen_codex_wall` |",
         "|---|---|---|---|---|---|"]
w()
w("== 7. IF the shared live_holds() were ANY-PHASE: the %d stages holding a DIFFER marker-seat" % len(dstages))
for (rid, ph) in dstages:
    r = RBY[rid]
    ls, la = live_set(r, ph, False), live_set(r, ph, True)
    cells = []
    for name, fn in (("check_stage_panels", sp_class), ("check_fable_queue", fq_class), ("gen_codex_wall", wall_list)):
        a, b = fn(r, ph, ls), fn(r, ph, la)
        chg[name] += a != b
        cells.append(a if a == b else "%s -> **%s**" % (a, b))
    w("  %-18s %-8s %-8s same=%s any=%s | %s" % (rid, ph, r.get("state"), ls, la, " | ".join(cells)))
    lines.append("| %s / %s | %s | %s -> %s | %s |" % (rid, ph, r.get("state"), ",".join(ls) or "-", ",".join(la) or "-",
                                                    " | ".join(cells)))
summ = ", ".join("%s %d of %d" % (k, chg[k], len(dstages)) for k in ("check_stage_panels", "check_fable_queue", "gen_codex_wall"))
w("  stages whose output changes: " + summ)
frag("consequence", "\n".join(lines) + "\n\nStages whose output changes: " + summ + ".")

# ------------------------------------------------------------------ 8. the differing set
w()
w("== 8. DIFFER SET: live under SAME-PHASE, discharged under ANY-PHASE -- %d of %d marker-seats" % (len(differ), NU))
dl = ["| # | row (state) | phase | seat | marker date [entry] | later entries by that seat, other phases: [entry] phase date (chars) opening words |",
      "|---|---|---|---|---|---|"]
for k, u in enumerate(differ, 1):
    r = RBY[u["row"]]
    w("- #%d %s [%d] phase=%s seat=%s date=%s state=%s" % (k, u["row"], u["idx"], u["phase"], u["seat"], u["date"], u["state"]))
    w("    marker: %s" % plain(note(r["entries"][u["idx"]]), 220))
    for j, e in u["any"]:
        w("    by [%d] %s %s (%d): %s" % (j, e.get("phase"), e.get("date"), nlen(e), plain(note(e), 200)))
    show = u["any"][:3]
    cell = "; ".join("[%d] %s %s (%d) \"%s\"" % (j, e.get("phase"), e.get("date"), nlen(e), plain(note(e), 70)) for j, e in show)
    rest = u["any"][3:]
    if rest:
        cell += "; +%d more (%s)" % (len(rest), ", ".join("%s %d" % kv for kv in sorted(collections.Counter(e.get("phase") for _, e in rest).items())))
    dl.append("| %d | %s (%s) | %s | %s | %s [%d] | %s |" % (k, u["row"], u["state"], u["phase"], u["seat"], u["date"], u["idx"], cell))
frag("differ", "\n".join(dl))

# ------------------------------------------------------------------ 9. context: hand-defanged copies (NOT markers)
DF = re.compile(r"\(HELD-AWAITING-SEAT[ /]+([a-z0-9_]+(?:[ \t]*[,/][ \t]*[a-z0-9_]+)*)")
dtab, n_df_ent, odd = collections.Counter(), 0, []
for r in ROWS:
    ents = r.get("entries", [])
    for i, h in enumerate(ents):
        ms = list(DF.finditer(note(h)))
        n_df_ent += bool(ms)
        for m in ms:
            for s in [x for x in re.split(r"[ \t]*[,/][ \t]*", m.group(1)) if x in ROSTER]:
                hd = h.get("date") or ""

                def has(same, cmp):
                    return any(j != i and (not same or e.get("phase") == h.get("phase")) and (e.get("seat") or "").lower() == s
                               and st.is_answer(e) and "HELD-AWAITING-SEAT" not in note(e) and cmp(e.get("date") or "", hd)
                               for j, e in enumerate(ents))
                k = "same-phase later" if has(True, GT) else ("same-phase same-date only" if has(True, GE)
                                                             else ("other-phase only" if has(False, GT) else "none"))
                dtab[k] += 1
                if k in ("other-phase only", "none"):
                    odd.append("%s[%d] %s/%s/%s" % (r["id"], i, h.get("phase"), s, hd))
all_df = sum(1 for r in ROWS for e in r.get("entries", []) if "HELD-AWAITING-SEAT" in note(e))
n_was = sum(1 for r in ROWS for e in r.get("entries", []) if "[was: HELD AWAITING SEAT" in note(e))
w("  entries using the unparsed '[was: HELD AWAITING SEAT ...]' defang spelling: %d" % n_was)
w()
w("== 9. CONTEXT (not markers): hand-defanged copies parsed by %r" % DF.pattern)
w("  entries parsed %d (entries spelling HELD-AWAITING-SEAT anywhere: %d); (entry, seat) pairs %d: %s; other-phase-only/none: %s"
  % (n_df_ent, all_df, sum(dtab.values()), dict(dtab), odd))

# ------------------------------------------------------------------ 10. appendix + tsv
app = ["%-20s %-5s %-9s %-9s %-10s %-8s %-28s %s" % ("row", "entry", "phase", "seat", "date", "state", "SAME-PHASE", "ANY-PHASE")]


def disp(lst):
    if not lst:
        return "live"
    j, e = lst[0]
    return "dis [%d] %s %s" % (j, e.get("phase"), e.get("date"))


for u in units:
    app.append("%-20s %-5s %-9s %-9s %-10s %-8s %-28s %s" % (u["row"], "[%d]" % u["idx"], u["phase"], u["seat"], u["date"],
                                                           u["state"], disp(u["same"]), disp(u["any"])))
frag("appendix", "```\n" + "\n".join(app) + "\n```")
with io.open(os.path.join(HERE, "markers.tsv"), "w", encoding="utf-8", newline="\n") as f:
    f.write("row\tentry\tphase\tseat\tdate\trow_state\tsame_gt_n\tany_gt_n\tsame_ge_n\tany_ge_n\tfirst_same\tfirst_any\n")
    for u in units:
        f.write("\t".join(str(x) for x in (u["row"], u["idx"], u["phase"], u["seat"], u["date"], u["state"],
                                           len(u["same"]), len(u["any"]), len(u["same_ge"]), len(u["any_ge"]),
                                           disp(u["same"]), disp(u["any"]))) + "\n")
with io.open(os.path.join(HERE, "differing.tsv"), "w", encoding="utf-8", newline="\n") as f:
    f.write("row\tentry\tphase\tseat\tdate\tby_entry\tby_phase\tby_date\tby_chars\n")
    for u in differ:
        for j, e in u["any"]:
            f.write("\t".join(str(x) for x in (u["row"], u["idx"], u["phase"], u["seat"], u["date"], j,
                                               e.get("phase"), e.get("date"), nlen(e))) + "\n")
w()
w("HOLDPHASE_ANALYSIS_DONE")
OUT.close()
