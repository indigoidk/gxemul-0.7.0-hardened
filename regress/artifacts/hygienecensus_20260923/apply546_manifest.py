#!/usr/bin/env python3
"""#546 (hygienecensus): add the round's new regress/ python files to tools/pipeline/check_probe_wiring.py's MANIFEST,
classified by the round (the #539 / #545 idiom): gate 6's token classifier, and the census passes' measurement and
control scripts preserved as evidence.  None is a gated detector.

usage: apply546_manifest.py LISTFILE SRC OUT   (run once on HEAD's copy, once on the working copy)"""
import io
import os
import sys

lst, src, out = sys.argv[1:4]
paths = [l.strip() for l in io.open(lst, encoding="utf-8") if l.strip()]
s = io.open(src, encoding="utf-8", newline="").read()
anchor_key = '    "artifacts/fbd5/q2_20260923/apply545_manifest.py":\n'
assert s.count(anchor_key) == 1, s.count(anchor_key)
i = s.index(anchor_key) + len(anchor_key)
j = s.index("\n", i) + 1                      # the entry's tuple line
PASS = {"c2": "the closing pass", "c3": "F3's pass", "c4": "F4's pass", "c5": "F5's pass", "c6": "F6's pass",
        "f2": "the F2 pass"}


def classify(f):
    b = os.path.basename(f)
    if f == "census_tokens.py":
        return ("CLASS_TOOL", "#546: gate 6's TOKEN classifier -- gate_hygiene.sh and tools/derive_hygiene_pins.sh call it "
                              "for the promptless list and the whole-buffer sites; comments, strings and docstrings are "
                              "not code")
    if b == "apply546_manifest.py":
        return ("CLASS_TOOL", "#546: adds these MANIFEST lines -- the round's own files, classified by the round")
    parts = f.split("/")
    k = next((p.split("_")[0] for p in parts if p.endswith("_20260923")), "")
    if "/opus_" in f:
        return ("CLASS_RESEARCH", "#546 %s: the Opus measuring seat's measurement script %s, preserved as run"
                % (PASS.get(k, k), b))
    return ("CLASS_TOOL", "#546 %s: %s -- the controls' edit generator, preserved as run" % (parts[2] if len(parts) > 2
                                                                                          else "", b))


lines = ["    #  #546 hygienecensus: gate 6's token classifier and the census passes' measurement and control scripts,\n",
         "    #  classified by the round (artifacts/hygienecensus_20260923/apply546_manifest.py).  None is a gated detector.\n"]
for f in sorted(set(paths)):
    assert ('"%s":' % f) not in s, "already in the MANIFEST: " + f
    cls, desc = classify(f)
    assert '"' not in desc and chr(92) not in desc, f
    lines.append('    "%s":\n        (%s, "%s"),\n' % (f, cls, desc))
s = s[:j] + "".join(lines) + s[j:]
io.open(out, "w", encoding="utf-8", newline="").write(s)
print("%d MANIFEST lines added -> %s" % (len(set(paths)), out))
