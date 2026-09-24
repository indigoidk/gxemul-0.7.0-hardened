#!/usr/bin/env python3
"""#545: add the round's own artifacts to tools/pipeline/check_probe_wiring.py's MANIFEST, classified by the round
(the #539 idiom, apply539_manifest.py).  None of them is a gated detector: #545's gated detectors are
regress/diff_footbridge.c (gate 2) and regress/footbridge_sites_probe.py (gate 14).

usage: apply545_manifest.py LISTFILE SRC OUT
  LISTFILE: one regress/-relative path per line (the files section R reported UNCLASSIFIED, plus this script)
  SRC/OUT:  the check_probe_wiring.py to read and the file to write -- run once on HEAD's copy (the commit blob) and
            once on the working copy (which also carries another unit's uncommitted lines, left as they are).
Refuses if the anchor (the apply539 entry) is not found exactly once, or a path is already in the MANIFEST."""
import io
import os
import sys

lst, src, out = sys.argv[1:4]
paths = [l.strip() for l in io.open(lst, encoding="utf-8") if l.strip()]
s = io.open(src, encoding="utf-8", newline="").read()
anchor = ('    "artifacts/n6/killtable_20260919/apply539_manifest.py":\n'
          '        (CLASS_TOOL, "#539: adds these MANIFEST lines -- the round\'s own artifacts, classified by the round"),\n')
assert s.count(anchor) == 1, s.count(anchor)


def where(f):
    d = os.path.dirname(f)
    for pre in ("artifacts/fbd5/", "artifacts/"):
        if d.startswith(pre):
            return d[len(pre):] or "."
    return d


def classify(f):
    b = os.path.basename(f)
    w = where(f)
    if b.endswith("_probe.py") or b.endswith("_witness.py"):
        return ("CLASS_WITNESS", "#545 %s: the frozen %s a kill table or seat ran -- the exact text it scored" % (w, b))
    if b.startswith("sites_") and "_probe" not in b:
        return ("CLASS_RESEARCH", "#545 %s: a variant copy of the sites probe a seat ran for one mutant" % w)
    if w.startswith("stateaudit_20260923"):
        return ("CLASS_TOOL", "the 2026-09-23 state audit: its %s deriver, preserved as run" % b[:-3])
    if b in ("legs.py", "opus_w.py"):
        return ("CLASS_RESEARCH", "#545 pass 1, the Opus seat's harness-leg measurement (%s)" % b)
    if b == "apply545_manifest.py":
        return ("CLASS_TOOL", "#545: adds these MANIFEST lines -- the round's own artifacts, classified by the round")
    return ("CLASS_TOOL", "#545 %s: %s, preserved as run (a mutator, driver, analyzer or predictor of a kill table or "
                          "seat measurement)" % (w, b))


lines = ["    #  #545 fbdeclinefive: the round's own artifacts -- kill-table mutators, drivers and analyzers, the seats'\n",
         "    #  measurement scripts, the frozen instruments the tables scored -- and the 2026-09-23 state audit's derivers,\n",
         "    #  classified by the round (artifacts/fbd5/q2_20260923/apply545_manifest.py).  None is a gated detector.\n"]
for f in sorted(set(paths)):
    assert ('"%s":' % f) not in s, "already in the MANIFEST: " + f
    cls, desc = classify(f)
    assert '"' not in desc and chr(92) not in desc, f
    lines.append('    "%s":\n        (%s, "%s"),\n' % (f, cls, desc))
s = s.replace(anchor, anchor + "".join(lines))
io.open(out, "w", encoding="utf-8", newline="").write(s)
print("%d MANIFEST lines added -> %s" % (len(set(paths)), out))
