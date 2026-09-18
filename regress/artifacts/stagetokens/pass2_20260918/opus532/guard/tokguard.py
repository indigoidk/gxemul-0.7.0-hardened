#  Opus seat's candidate guard for #532 Q2 (fixture only, not for SEC as-is).
import os, re
PANEL_RE = re.compile(r"panel_\d{8}_\d{6}")
ROOTS = [p for p in (os.environ.get("GXPANELS"),
         os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "_scratchpad")),
         r"C:\DocumentNoSnc\CC\GXEMUL\_scratchpad") if p]
STAGE_TOKENS = ("[NOT A PANEL STAGE: SINGLE-SEAT RE-READ]", "[NOT A PANEL STAGE: NO PANEL CONVENED]")
def _title(d):
    for r in ROOTS:
        p = os.path.join(r, d, "brief_sent.md")
        if os.path.exists(p):
            with open(p, encoding="utf-8", errors="replace") as f:
                return f.readline()
    return None
def refuse(row, phase):
    """Return a reason string if a stage token on (row, phase) must NOT be honoured."""
    ents = [e for e in row.get("entries", []) if e.get("phase") == phase]
    toks = [e for e in ents if any(t in (e.get("note") or "") for t in STAGE_TOKENS)]
    if not toks:
        return None
    tdate = max(e.get("date", "") for e in toks)
    tallied = [e for e in ents if e not in toks and "[HELD AWAITING SEAT:" not in (e.get("note") or "")
               and "[RUN UNDER THE PRE-2026-08-16 POLICY]" not in (e.get("note") or "")]
    late = [e["seat"] for e in tallied if e.get("date", "") > tdate]
    if late:
        return "token %s predates entries from %s" % (tdate, ",".join(sorted(set(late))))
    for e in tallied:
        for d in PANEL_RE.findall("%s %s" % (e.get("ev", ""), e.get("note", ""))):
            t = _title(d)
            if t is not None and ("`%s`" % row["id"]) in t:
                return "%s's brief is convened on this row: %s" % (d, t.strip()[:60])
    return None
