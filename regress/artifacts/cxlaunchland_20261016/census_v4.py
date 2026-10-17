#!/usr/bin/env python3
"""census_v4.py [root ...] -- the on-record shapes behind the v4 contract's DISCLOSED lines (2026-10-17, the v3 pass's
findings).  Reads every codex*.err under the roots (default: GXEMUL-SEC and _scratchpad, beside this repo) and reports:
  * opening header blocks found by the landed launcher's rule (banner and first rule by line 12, closing rule within the
    block) -- how many lack a `model:' line, carry two or more, or never close within the read; and how many files show a
    banner in their first 200 lines WITHOUT an opening block (a late or displaced header);
  * the classification population -- runs whose sibling .txt is empty or absent -- and how many of those carry BOTH a
    column-0 refusal `ERROR:' line and a column-0 wall `ERROR:' line (after the ANSI strip), which is the only shape on
    which the refusal-before-wall precedence (m_prec) is observable.
Read-only.  Prints its denominators beside every count."""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, os.pardir, os.pardir, os.pardir, os.pardir))
roots = sys.argv[1:] or [os.path.join(PROJ, "GXEMUL-SEC"), os.path.join(PROJ, "_scratchpad")]
ESC = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
REF = re.compile(r"flagged for possible cybersecurity|cannot help with|can.t help with|I won.t help", re.I)
WAL = re.compile(r"usage limit|quota|rate limit|not authenticated", re.I)
n_err = blocks = nomodel = twomodel = unclosed = late = cls = both = 0
both_files = []
for root in roots:
    for dp, dn, fn in os.walk(root):
        if os.sep + ".git" in dp or dp.endswith(".git"):
            continue
        for f in fn:
            if not (f.endswith(".err") and "codex" in f.lower()):
                continue
            p = os.path.join(dp, f)
            try:
                raw = open(p, "rb").read()
            except OSError:
                continue
            n_err += 1
            lines = ESC.sub("", raw.decode("utf-8", "replace")).split("\n")
            h = 0; body = []; closed = False
            for i, l in enumerate(lines, 1):
                if i > 12 and h < 2:
                    break
                if h == 0 and l.startswith("OpenAI Codex"):
                    h = 1; continue
                if h == 1 and l.startswith("--------"):
                    h = 2; continue
                if h == 2 and l.startswith("--------"):
                    closed = True; break
                if h == 2:
                    body.append(l)
            if h == 2:
                blocks += 1
                m = sum(1 for l in body if l.startswith("model:"))
                nomodel += m == 0
                twomodel += m > 1
                unclosed += not closed
            elif any(l.startswith("OpenAI Codex") for l in lines[:200]):
                late += 1
            t = p[:-4] + ".txt"
            if (not os.path.exists(t)) or os.path.getsize(t) == 0:
                cls += 1
                errl = [l for l in lines if l.startswith("ERROR:")]
                if any(REF.search(l) for l in errl) and any(WAL.search(l) for l in errl):
                    both += 1; both_files.append(p)
print("roots: %s" % " ".join(roots))
print("codex .err files read: %d" % n_err)
print("opening blocks by the landed rule: %d of %d files | no model line: %d | two or more: %d | unclosed: %d"
      % (blocks, n_err, nomodel, twomodel, unclosed))
print("files with a banner in their first 200 lines but no opening block: %d of %d" % (late, n_err))
print("classification population (sibling .txt empty or absent): %d of %d | carrying BOTH a column-0 refusal and a "
      "column-0 wall ERROR line: %d" % (cls, n_err, both))
for b in both_files:
    print("  both: %s" % b)
print("CENSUS_V4_DONE")
