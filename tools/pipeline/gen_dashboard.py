#!/usr/bin/env python3
"""Render pipeline/matrix.html from pipeline/ledger.json.  NEVER hand-edit the output.

THE DOCSTRING SAID `dashboard.html` WHILE LINE 24 WROTE `matrix.html`, and an untracked,
stale dashboard.html has been sitting beside the real output as a result -- smaller and
hours older, and indistinguishable from the live board to anyone about to publish one.
The file this script writes is matrix.html; that is the tracked one and the one to publish.

Ledger-first (PIPELINE.md section 5): the JSON is the single source of truth; a cell without
a ledger entry behind it is a defect.  Idempotent.

Layout per the owner's directives (2026-08-15):
  * EVERY BUG SHOWS ALL FOUR PHASE ROWS (Assessment / Research / Final review / Regression);
    an empty phase is a row of dots — input is possible there.
  * BUGS IN WORK AT THE TOP, CLOSED BUGS AT THE BOTTOM, with a divider between them.
  * CELLS WITH CLEAR EDGES: full borders on the matrix cells.
  * THE BUG HEADER IS ONE LINE: id + title + state. The hold reason shows on
    MOUSE OVER only (owner, 2026-08-15): the state chip's title attribute and
    the id/title tooltip both carry it. Nothing inline.
Text on the page is ASD-STE100 unless a technical name is necessary.
"""
import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(HERE, "ledger.json")
OUT = os.path.join(HERE, "matrix.html")

L = json.load(open(LEDGER, encoding="utf-8"))
seats = L["seats"]
sid = {s["id"]: s for s in seats}
PHASES = ["assess", "research", "review", "regress"]
PLABEL = L["phase_labels"]

#  *** A SEAT ID THAT NO COLUMN DECLARES IS A HARD ERROR, NEVER A SILENT DROP. ***
#  Measured 2026-08-16: 59 entries were keyed "opus" while the column is declared
#  "opus5".  cell() matches on x["seat"] == seat["id"], so every one of them rendered
#  NOWHERE -- the measure seat's work simply was not on the dashboard, and the blank
#  cells read as "that seat never answered", which is the exact opposite of the truth
#  and the one reading this dashboard exists to prevent.  The owner spotted it by eye.
#
#  A dashboard that silently drops data it cannot place is worse than one that crashes:
#  a missing cell is indistinguishable from a seat failure, and this project's whole
#  discipline is that a seat failure is never counted as agreement.  So: refuse to
#  render, name every offender and how many entries it holds, and exit non-zero.
_declared = {s["id"] for s in seats}
_orphans = {}
for _r in L["rows"]:
    for _e in _r.get("entries", []):
        if _e.get("seat") not in _declared:
            _orphans.setdefault(_e.get("seat"), []).append(_r["id"])
if _orphans:
    sys.stderr.write("gen_dashboard: REFUSING TO RENDER -- seat ids used by entries "
                     "but declared by no column:\n")
    for _k in sorted(_orphans, key=lambda k: str(k)):
        _rows = sorted(set(_orphans[_k]))
        sys.stderr.write("  %-12r %3d entries across %d rows: %s%s\n"
                         % (_k, len(_orphans[_k]), len(_rows), ", ".join(_rows[:6]),
                            " ..." if len(_rows) > 6 else ""))
    sys.stderr.write("Fix the ledger (or add the column). Declared: %s\n"
                     % ", ".join(sorted(_declared)))
    sys.exit(2)

D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}
e = lambda t: html.escape(str(t), quote=True)

BADGE_TIP = {"A": "the author did this review (shown, not hidden)",
             "s": "a review by the same model family",
             "?": "attribution not confirmed"}

#  `dropped` sorts BELOW closed. Any state not named here falls to 5 and lands in the
#  in-work bucket -- which is how twelve adjudicated-off rows nearly published as "in
#  work". Add new states HERE and to the section split below; the two must agree.
STATE_ORDER = {"active": 0, "held": 1, "pending": 2, "closed": 9, "dropped": 10}


def cell(row, phase, seat):
    ents = [x for x in row.get("entries", [])
            if x["seat"] == seat["id"] and x.get("phase") == phase]
    if not ents:
        return '<td class="c none"><span class="g">·</span></td>'
    ent = ents[-1]
    d = ent.get("d", "…")
    cls = D_CLASS.get(d, "pend")
    badge = ent.get("b", "")
    tip = [p for p in (ent.get("date"), ent.get("grade"),
                       BADGE_TIP.get(badge), ent.get("note")) if p]
    if ent.get("ev"):
        tip.append("evidence: " + ent["ev"])
    t = e(" — ".join(tip))
    b = f'<sup class="b b-{badge}">{badge}</sup>' if badge else ""
    return (f'<td class="c {cls}"><span class="wrap" tabindex="0">'
            f'<span class="g">{d}</span>{b}<span class="tip">{t}</span></span></td>')


def fix_section(row):
    state = row.get("state", "pending")
    clo = row.get("closure", {}) or {}
    hold = row.get("hold", "")
    tiplist = [row["title"]]
    if row.get("commits"):
        tiplist.append("commits: " + row["commits"])
    if hold:
        tiplist.append("HOLD: " + hold)
    if clo.get("note"):
        tiplist.append(clo["note"])
    lt = e(" — ".join(tiplist))
    badge = clo.get("badge", "")
    b = f'<sup class="b b-{badge}">{badge}</sup>' if badge else ""
    # Hold reason is MOUSE-OVER ONLY (owner, 2026-08-15): native title on the
    # state chip + the custom .tip on the id/title wrap. Nothing inline.
    ht = f' title="{e(hold)}"' if hold else ""
    statechip = f'<span class="state st-{state}"{ht}>{e(state)}</span>'
    head = (f'<tr class="fixhead st-{state}"><th colspan="{len(seats)+1}">'
            f'<span class="hline"><span class="wrap" tabindex="0">'
            f'<span class="rid">{e(row["id"])}</span>'
            f'<span class="ttl">{e(row["title"])}</span>{b}'
            f'<span class="tip">{lt}</span></span>'
            f'{statechip}</span></th></tr>')
    body = "".join(
        f'<tr class="ph st-{state}"><th scope="row" class="phlabel">{e(PLABEL[p])}</th>'
        + "".join(cell(row, p, s) for s in seats) + "</tr>"
        for p in PHASES)
    return head + body


rows_sorted = sorted(L["rows"], key=lambda r: STATE_ORDER.get(r.get("state"), 5))
#  THREE buckets, not two. `dropped` is NOT `closed`: closed means the work shipped, dropped
#  means the premise was refuted by measurement and no work is owed. Folding them together
#  would erase the distinction the adjudication exists to record -- and leaving `dropped` out
#  of the split entirely (the state it was in until 2026-08-20) silently counted twelve
#  adjudicated-off rows as "in work", because open_rows was defined by NOT-closed.
open_rows = [r for r in rows_sorted if r.get("state") not in ("closed", "dropped")]
closed_rows = [r for r in rows_sorted if r.get("state") == "closed"]
dropped_rows = [r for r in rows_sorted if r.get("state") == "dropped"]


def _divider(label, n):
    return (f'<tr class="divider"><th colspan="{len(seats)+1}">{label}</th></tr>'
            if n else "")


sections = ("".join(fix_section(r) for r in open_rows)
            + _divider("closed", len(closed_rows))
            + "".join(fix_section(r) for r in closed_rows)
            + _divider("dropped &mdash; premise refuted by measurement, no work owed",
                       len(dropped_rows))
            + "".join(fix_section(r) for r in dropped_rows))


def summary():
    n = {"✓": 0, "⏸": 0, "✕": 0, "…": 0}
    for r in L["rows"]:
        for x in r.get("entries", []):
            n[x.get("d", "…")] = n.get(x.get("d", "…"), 0) + 1
    return n


n = summary()
bat = L["battery"]

heads = "".join(
    f'<th class="seat"><div class="diag"><span class="wrap" tabindex="0">'
    f'{e(s["name"])} <em>({e(s["ver"])})</em>'
    f'<span class="tip">{e(s["model"])} — {e(s["cls"])} — {e(s["note"])}</span>'
    f'</span><i class="cls cls-{e(s["cls"].split("+")[0])}">{e(s["cls"])}</i></div></th>'
    for s in seats)

page = f"""<title>GXemul Panel Ledger</title>
<style>
:root {{
  --ground:#f2f5f4; --panel:#ffffff; --ink:#1d2724; --muted:#5c6d68;
  --line:#c6d1cd; --line2:#e0e7e4; --accent:#1f6e64;
  --ok:#2f7d3b; --hold:#9a6b08; --bad:#ae352c; --pend:#7b8a86;
  --okbg:#eaf4eb; --holdbg:#f6eeda; --badbg:#f8e6e4;
  --chipbg:#e4ecea; --tipbg:#243330; --tipink:#e8f0ed;
  --fixbg:#e9efed; --closedbg:#f0f2f1;
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
    --ground:#121917; --panel:#1a2321; --ink:#d9e4e0; --muted:#8ca09a;
    --line:#3b4844; --line2:#27322f; --accent:#5fc4b4;
    --ok:#79c784; --hold:#dfb35c; --bad:#e77e74; --pend:#6d7f7a;
    --okbg:#1c2d21; --holdbg:#31280f; --badbg:#371f18;
    --chipbg:#22302d; --tipbg:#e8f0ed; --tipink:#1d2724;
    --fixbg:#202c29; --closedbg:#151d1b;
  }}
}}
:root[data-theme="dark"] {{
  --ground:#121917; --panel:#1a2321; --ink:#d9e4e0; --muted:#8ca09a;
  --line:#3b4844; --line2:#27322f; --accent:#5fc4b4;
  --ok:#79c784; --hold:#dfb35c; --bad:#e77e74; --pend:#6d7f7a;
  --okbg:#1c2d21; --holdbg:#31280f; --badbg:#371f18;
  --chipbg:#22302d; --tipbg:#e8f0ed; --tipink:#1d2724;
  --fixbg:#202c29; --closedbg:#151d1b;
}}
* {{ box-sizing:border-box; }}
body {{
  margin:0; background:var(--ground); color:var(--ink);
  font:14px/1.45 "Cascadia Mono","Consolas",ui-monospace,SFMono-Regular,Menlo,monospace;
  font-variant-numeric: tabular-nums; padding:28px 20px 60px;
}}
.sheet {{ max-width:1120px; margin:0 auto; display:flex; flex-direction:column; gap:18px; }}
header .eyebrow {{ font-size:11px; letter-spacing:.22em; text-transform:uppercase;
  color:var(--accent); font-weight:600; }}
header h1 {{ margin:2px 0 0;
  font-family:"Segoe UI Variable Display","Segoe UI",system-ui,sans-serif;
  font-size:30px; font-weight:650; letter-spacing:-.01em; text-wrap:balance; }}
header .sub {{ color:var(--muted); margin-top:4px; max-width:70ch; }}
.strip {{ display:flex; flex-wrap:wrap; gap:8px; }}
.chip {{ background:var(--chipbg); border:1px solid var(--line2); border-radius:3px;
  padding:4px 10px; font-size:12px; display:inline-flex; gap:7px; align-items:baseline; }}
.chip b {{ font-weight:600; }}
.chip .k {{ color:var(--muted); font-size:11px; letter-spacing:.08em; text-transform:uppercase; }}
.chip.pass b {{ color:var(--ok); }}
.matrix-scroll {{ overflow-x:auto; background:var(--panel); border:1px solid var(--line);
  border-radius:4px; padding:6px 10px 14px; }}
table {{ border-collapse:collapse; width:100%; min-width:980px; }}
thead th {{ height:150px; vertical-align:bottom; border-bottom:2px solid var(--accent); }}
thead th.rowhead {{ text-align:left; color:var(--muted); font-size:11px; font-weight:500;
  letter-spacing:.14em; text-transform:uppercase; padding:0 8px 8px; }}
th.seat {{ width:62px; }}
.diag {{ position:relative; height:150px; width:62px; }}
.diag > .wrap {{ position:absolute; bottom:34px; left:30px; transform:rotate(-50deg);
  transform-origin:bottom left; white-space:nowrap; font-size:12.5px; font-weight:600; }}
.diag em {{ color:var(--muted); font-style:normal; font-weight:500; }}
.diag .cls {{ position:absolute; bottom:8px; left:50%; transform:translateX(-50%);
  font-style:normal; font-size:9.5px; letter-spacing:.06em; color:var(--muted);
  border:1px solid var(--line2); border-radius:2px; padding:0 4px; }}
.cls-PK {{ color:var(--accent); border-color:var(--accent); }}
tr.fixhead th {{ text-align:left; background:var(--fixbg);
  border:1px solid var(--line); border-left:none; border-right:none;
  padding:7px 10px; font-weight:600; font-size:13px; }}
tr.fixhead.st-closed th, tr.fixhead.st-dropped th {{ background:var(--closedbg); }}
tr.fixhead.st-dropped .ttl {{ opacity:.55; text-decoration:line-through; }}
.state.st-dropped {{ color:var(--muted); border-color:var(--muted); }}
tr.fixhead.st-closed .ttl {{ opacity:.7; }}
/* ONE LINE: nothing in the header may wrap; long parts get an ellipsis. */
.hline {{ display:flex; align-items:baseline; gap:8px; white-space:nowrap; overflow:hidden; }}
.hline > .wrap {{ display:inline-flex; align-items:baseline; gap:6px; min-width:0;
  flex:0 1 auto; }}
.ttl {{ overflow:hidden; text-overflow:ellipsis; white-space:nowrap; max-width:430px;
  display:inline-block; vertical-align:bottom; }}
.rid {{ color:var(--accent); font-weight:700; flex:none; }}
.state {{ flex:none; font-size:9.5px; letter-spacing:.09em; text-transform:uppercase;
  border:1px solid var(--line2); border-radius:2px; padding:1px 6px; color:var(--muted); }}
.state.st-active {{ color:var(--accent); border-color:var(--accent); font-weight:700; }}
.state.st-held {{ color:var(--hold); border-color:var(--hold); }}
.state[title] {{ cursor:help; border-style:dashed; }}
tr.ph th.phlabel {{ text-align:left; font-weight:400; color:var(--muted); font-size:12.5px;
  padding:5px 10px 5px 22px; border:1px solid var(--line2); border-left:none;
  white-space:nowrap; }}
tr.ph td {{ border:1px solid var(--line2); text-align:center; padding:4px 0;
  background:var(--panel); }}
tr.ph.st-closed td, tr.ph.st-closed th.phlabel,
tr.ph.st-dropped td, tr.ph.st-dropped th.phlabel {{ background:var(--closedbg); }}
td.c.ok {{ background:var(--okbg); }}
td.c.hold {{ background:var(--holdbg); }}
td.c.bad {{ background:var(--badbg); }}
tr.ph.st-closed td.c.ok {{ background:color-mix(in srgb, var(--okbg) 55%, var(--closedbg)); }}
.c .g {{ font-size:15px; }}
.c.ok .g {{ color:var(--ok); }} .c.hold .g {{ color:var(--hold); }}
.c.bad .g {{ color:var(--bad); font-weight:700; }} .c.pend .g {{ color:var(--pend); }}
.c.none .g {{ color:var(--line); }}
.b {{ font-size:9.5px; font-weight:700; margin-left:1px; color:var(--accent);
  border:1px solid var(--accent); border-radius:2px; padding:0 2px; vertical-align:6px; }}
.b-s {{ color:var(--hold); border-color:var(--hold); }}
tr.divider th {{ background:var(--ground); color:var(--muted); text-align:left;
  font-size:10.5px; letter-spacing:.18em; text-transform:uppercase;
  padding:12px 10px 4px; border:none; border-bottom:2px solid var(--line); }}
.wrap {{ position:relative; cursor:default; }}
.wrap:focus {{ outline:2px solid var(--accent); outline-offset:1px; }}
.tip {{ display:none; position:absolute; z-index:9; left:50%; bottom:calc(100% + 8px);
  transform:translateX(-50%); width:340px; max-width:76vw; white-space:normal;
  text-align:left; font-size:12px; line-height:1.45; font-weight:400;
  background:var(--tipbg); color:var(--tipink); border-radius:4px; padding:9px 11px;
  box-shadow:0 6px 22px rgba(0,0,0,.28); text-transform:none; letter-spacing:0; }}
.wrap:hover .tip, .wrap:focus .tip {{ display:block; }}
thead .tip {{ transform:none; left:auto; right:-10px; bottom:auto; top:calc(100% + 6px); }}
tr.fixhead .tip {{ transform:none; left:0; bottom:auto; top:calc(100% + 6px); }}
.legend {{ display:flex; flex-wrap:wrap; gap:14px; color:var(--muted); font-size:12px; }}
.legend .g {{ font-size:14px; }}
footer {{ color:var(--muted); font-size:11.5px; max-width:78ch; }}
footer code {{ color:var(--ink); }}
</style>
<div class="sheet">
<header>
  <div class="eyebrow">multi-llm fix pipeline · made from the ledger</div>
  <h1>GXemul Panel Ledger</h1>
  <div class="sub">Each bug shows all four phases. A phase with no input shows a row of
  dots: input is possible there. Bugs in work are at the top; closed bugs are below the
  divider. Put the pointer on a cell, or give it focus, to see the date, the evidence
  grade, the note, and the path of the evidence file.</div>
</header>
<div class="strip">
  <span class="chip pass"><span class="k">battery</span><b>{e(bat["verdict"])} {e(bat["coverage"])}</b>
    <span>{e(bat["when"])} @ {e(bat["head"])}</span></span>
  <span class="chip"><span class="k">flagship</span><b>{e(sid[L["flagship"]]["name"])} ({e(sid[L["flagship"]]["ver"])})</b></span>
  <span class="chip"><span class="k">bugs</span><b>{len(open_rows)} in work · {len(closed_rows)} closed · {len(dropped_rows)} dropped</b></span>
  <span class="chip"><span class="k">entries</span><b>{n["✓"]}✓ {n["✕"]}✕ {n["⏸"]}⏸ {n["…"]}…</b></span>
  <span class="chip"><span class="k">updated</span><b>{e(L["updated"])}</b></span>
</div>
<div class="matrix-scroll"><table>
<thead><tr><th class="rowhead">bug · phase</th>{heads}</tr></thead>
<tbody>{sections}</tbody>
</table></div>
<div class="legend">
  <span><span class="g" style="color:var(--ok)">✓</span> approved</span>
  <span><span class="g" style="color:var(--hold)">⏸</span> held / in work</span>
  <span><span class="g" style="color:var(--bad)">✕</span> objection</span>
  <span><span class="g" style="color:var(--pend)">…</span> no answer / seat failure (not agreement)</span>
  <span><span class="g" style="color:var(--line)">·</span> no input — input is possible</span>
  <span><sup class="b">A</sup> the author did this review (shown)</span>
  <span><sup class="b b-s">s</sup> a review by the same model family</span>
  <span>FR = reads files · FR+M = reads files and does tests · <span style="color:var(--accent)">PK = gets a packet only</span></span>
</div>
<footer>The program <code>gen_dashboard.py</code> makes this page from
<code>pipeline/ledger.json</code>. Do not change this page manually. If a cell does not have
a ledger entry, the cell is a defect. A packet-fed seat examines the argument only. Its vote
about the contents of the repository is not equal to the vote of a seat that reads files
(PIPELINE.md, Section 1). An ✕ cell can be the most important cell in its row: the ✕ in the
Research phase of #419 changed the design. Rule for closed rows (owner, 2026-08-15): a closed
row does not need new tests when the flagship seat (Fable) examined the final change and its
evidence. That examination fills the Final review cell of the closed row.
<b>Regression phase (owner, 2026-08-15): only the flagship seat reviews the regression tests,
and the reviews are BATCHED TO SUNDAY NIGHT, after the full battery, which now runs Sunday at
18:00 so that its evidence covers the rounds the review examines.</b> The other eight cells in a Regression line are NOT
REQUIRED, and a Regression line that is empty on a round finished after Saturday is WAITING FOR THE
SUNDAY BATCH, not missing. So a line of dots there shows a rule, not a gap. The first three phases
still need all nine seats, per round, before that round proceeds.</footer>
</div>
"""

open(OUT, "w", encoding="utf-8").write(page)
sys.stdout.write("wrote %s (%d bytes, %d in work + %d closed, %d seats)\n"
                 % (OUT, os.path.getsize(OUT), len(open_rows), len(closed_rows), len(seats)))
