#!/usr/bin/env python3
"""apply_fmt.py -- apply Gemini's format-fix edits (gweb/jobs_20261105_fmtfix/fmt_*/reply.txt) to HEAD's sources, staged OUTSIDE
the repo: fmtfix/stage/<path>.  Deterministic checks only: one ```json block per reply; each edit names a tracked file; its
`old` occurs exactly once in that file's text at the time it is applied; new != old.  Writes stage/, FIX.diff (against HEAD),
REJECTS.txt and SUMMARY.txt.  The repo is read with `git show HEAD:` and never written."""
import difflib
import glob
import io
import json
import os
import re
import subprocess

REPO = "C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC"
O = "C:/DocumentNoSnc/cc/GXEMUL/_scratchpad/codescan/fmtfix/"
J = "C:/DocumentNoSnc/cc/GXEMUL/_scratchpad/gweb/jobs_20261105_fmtfix/"
head = subprocess.run(["git", "-C", REPO, "rev-parse", "--short=8", "HEAD"], capture_output=True, text=True).stdout.strip()
tracked = set(subprocess.run(["git", "-C", REPO, "ls-files", "src"], capture_output=True, text=True).stdout.split())
cur, base, rej, ok, why = {}, {}, [], 0, []
done_dup = {}
WARN = {}
for wl in io.open("C:/DocumentNoSnc/cc/GXEMUL/_scratchpad/codescan/fmt_warnings.tsv", encoding="utf-8"):
    wp = wl.rstrip("\n").split("\t")
    if len(wp) == 4:
        bn = os.path.basename(wp[0])
        for t in tracked:
            if os.path.basename(t) == bn:
                WARN.setdefault(t, set()).add(int(wp[1]))
                break
for rp in sorted(glob.glob(J + "fmt_*/reply.txt")):
    job = rp.split("/")[-2] if "/" in rp else os.path.basename(os.path.dirname(rp))
    job = os.path.basename(os.path.dirname(rp))
    blocks = re.findall(r"```json\s*\n(.*?)\n```", io.open(rp, encoding="utf-8").read(), re.S)
    if len(blocks) != 1:
        rej.append("%s: %d json blocks" % (job, len(blocks)))
        continue
    try:
        edits = json.loads(blocks[0])
    except ValueError as e:
        rej.append("%s: json does not parse: %s" % (job, e))
        continue
    for k, e in enumerate(edits):
        f, old, new = e.get("file", ""), e.get("old", ""), e.get("new", "")
        tag = "%s #%d %s" % (job, k, f)
        if f not in tracked:
            rej.append("%s: not a tracked src file" % tag)
            continue
        if f not in cur:
            t = subprocess.run(["git", "-C", REPO, "show", "HEAD:" + f], capture_output=True).stdout.decode("latin-1")
            cur[f] = base[f] = t
        n = cur[f].count(old) if old else 0
        if n > 1 and old != new and done_dup.get((f, old)) is None:
            # the same call repeated: replace every occurrence only when GCC warned inside each one (fmt_warnings.tsv lines are
            # HEAD lines, so the spans are taken in HEAD's text)
            starts = [m.start() for m in re.finditer(re.escape(old), base[f])]
            spans = [(base[f].count("\n", 0, a) + 1, base[f].count("\n", 0, a) + old.count("\n") + 1) for a in starts]
            if len(starts) == n and f in WARN and all(any(a <= w <= b for w in WARN[f]) for a, b in spans):
                cur[f] = cur[f].replace(old, new)
                done_dup[(f, old)] = new
                ok += n
                why.append("%s: (x%d, GCC warned in every copy) %s" % (tag, n, e.get("why", "")[:120]))
                continue
        if (f, old) in done_dup and done_dup[(f, old)] == new:
            why.append("%s: duplicate of an edit already applied to every copy" % tag)
            continue
        if n != 1 or old == new:
            rej.append("%s: `old` occurs %d time(s)%s: %r" % (tag, n, " (new == old)" if old == new else "", old[:90]))
            continue
        cur[f] = cur[f].replace(old, new)
        ok += 1
        why.append("%s: %s" % (tag, e.get("why", "")[:140]))
diff = []
for f in sorted(cur):
    if cur[f] == base[f]:
        continue
    p = O + "stage/" + f
    os.makedirs(os.path.dirname(p), exist_ok=True)
    io.open(p, "w", encoding="latin-1", newline="").write(cur[f])
    diff += difflib.unified_diff(base[f].splitlines(True), cur[f].splitlines(True), "a/" + f, "b/" + f)
io.open(O + "FIX.diff", "w", encoding="latin-1", newline="").write("".join(diff))
io.open(O + "REJECTS.txt", "w", encoding="utf-8", newline="\n").write("\n".join(rej) + "\n")
io.open(O + "WHY.txt", "w", encoding="utf-8", newline="\n").write("\n".join(why) + "\n")
s = "HEAD %s: %d edits applied to %d files; %d rejected (REJECTS.txt); FIX.diff %d lines" % (
    head, ok, sum(1 for f in cur if cur[f] != base[f]), len(rej), len(diff))
io.open(O + "SUMMARY.txt", "w", encoding="utf-8", newline="\n").write(s + "\n")
print(s)
