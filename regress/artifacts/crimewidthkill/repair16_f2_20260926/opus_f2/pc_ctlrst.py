#!/usr/bin/env python3
"""pc_ctlrst.py BIN SESSIONS.json -- replay the probe's own `ctlrst sw' session on BIN and print the value its AFTER
`print pc' returns (the pc after the 0x0800 store's step), plus v1 -- the evidence for Q3 item 3."""
import json, re, sys
sys.argv = [sys.argv[0]] + sys.argv[1:]
exec(open("/tmp/replay_ctl.frozen.py").read().split('print("REPLAY_CTL binary=%s" % BIN)')[0])
s = [x for x in S if "ctlrst sw msg" in x["rows"]][0]
t, clean = session(s["cmds"])
pcs = re.findall(r"print\s+pc\s*\n\s*(0x[0-9a-f]+)", t)
v1 = re.findall(r"print\s+v1\s*\n\s*(0x[0-9a-f]+)", t)
print("S%02d ctlrst sw: clean=%s print-pc=%s v1=%s stopped-notice=%d" % (s["idx"], clean, pcs, v1,
      t.count("All machines stopped")))
