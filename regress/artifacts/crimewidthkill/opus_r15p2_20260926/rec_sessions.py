#!/usr/bin/env python3
"""rec_sessions.py PROBE OUT.json -- run the probe's OWN top-level code with session() replaced by a recorder (no emulator),
so the ORDER of its session() calls and the rows each one feeds are read off the probe itself rather than transcribed.
Row outcomes in this dry run are meaningless (every transcript is empty); only the names and the order are kept."""
import json, sys

probe, outp = sys.argv[1], sys.argv[2]
src = open(probe, encoding="latin-1").read()
anchor = "def session(cmds, settle=1.5, spin=1.2):"
assert src.count(anchor) == 1
src = src.replace(anchor, "def _unused_real_session(cmds, settle=1.5, spin=1.2):")
REC = []


def fake_session(cmds, settle=1.5, spin=1.2):
    REC.append({"rows_before": len(G["rows"]), "cmds": list(cmds)})
    return "", False


G = {"__name__": "__probe__", "session": fake_session}
sys.argv = [probe, "/nonexistent/bin", "rec"]
exec(compile(src, "probe", "exec"), G)
rows = [n for n, ok in G["rows"]]
out = []
for i, r in enumerate(REC):
    end = REC[i + 1]["rows_before"] if i + 1 < len(REC) else len(rows)
    out.append({"idx": i, "rows": rows[r["rows_before"]:end], "cmds": r["cmds"]})
json.dump({"n_sessions": len(REC), "n_rows": len(rows), "sessions": out}, open(outp, "w"), indent=1)
sys.stderr.write("sessions=%d rows=%d\n" % (len(REC), len(rows)))
