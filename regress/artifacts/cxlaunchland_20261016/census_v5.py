#!/usr/bin/env python3
"""census_v5.py [root ...] -- the on-record shapes behind the v5 contract (2026-10-17, the v4 pass's findings).  Read-only.  Every
count prints its denominator and names its population, because the v4 records cited one fact at three populations (2,372 /
4,851 / 2,422 files -- GLM 5.3 and Grok 4.7, v4 pass).  Roots default to GXEMUL-SEC and _scratchpad beside this repo.

POPULATIONS
  CODEX   every *.err whose name contains `codex' (case-insensitive) -- the launcher's and panel.sh's codex stderr captures
  ALLERR  every *.err of any name -- the wider scope Fable 5.1 used for the escape census (v4 pass)
  LAUNCH  every file whose name ends `.launch.log', or contains `launch' and ends `.log' or `.txt' -- launcher stdout captures

REPORTS
  1. opening header blocks found by the landed rule WITH its 30-line body cap (census_v4 omitted the cap -- GPT-6 Astra): how
     many lack a model line, carry two or more, or never close within the cap; the banner, first-rule and model-line positions;
     blocks carrying ANSI escapes and how many of those are answered runs; and the synthetic row shapes -- WS (a model line with
     a tab, a doubled space, trailing whitespace or a CR), MA (a line containing `model:' not at column 0 inside the block), HB
     (a banner-shaped line inside the block), NM (a block with no model line followed within 30 lines by one), BA (a rule line,
     or a non-column-0 `OpenAI Codex', above the banner), R7 (a line of exactly seven dashes in the first 50 lines)
  2. escapes, at CODEX and ALLERR: files carrying ESC; a non-SGR CSI (final byte other than `m'); an SGR whose parameters hold
     a `;'; an OSC; any other ESC
  3. column-0 `ERROR:' lines after the ANSI strip, at CODEX: per pattern alternative, case-insensitive and case-sensitive (lines,
     files) -- the case-only hits are what the `-i' decides
  4. the empty-or-absent-sibling subset (a sibling .txt that is empty or missing -- NOT a measure of exit status): how many of
     its files carry BOTH a refusal and a wall ERROR line (the RW shape)
  5. LAUNCH: every `codex rc=N   stdout=N b' line, as a table of rc by empty/non-empty stdout -- the diagonal the launcher's
     classify-on-failure gate rests on"""
import os, re, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, os.pardir, os.pardir, os.pardir, os.pardir))
roots = sys.argv[1:] or [os.path.join(PROJ, "GXEMUL-SEC"), os.path.join(PROJ, "_scratchpad")]
ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
NONSGR = re.compile(r"\x1b\[[0-9;?]*[A-Za-ln-z]")
SEMISGR = re.compile(r"\x1b\[[0-9]*;[0-9;]*m")
OSC = re.compile(r"\x1b\]")
OTHERESC = re.compile(r"\x1b(?![\[\]])")
REF_ALTS = ["flagged for possible cybersecurity", "cannot help with", "can.t help with", "I won.t help"]
WAL_ALTS = ["usage limit", "quota", "rate limit", "not authenticated"]
REF = re.compile("|".join(REF_ALTS), re.I)
WAL = re.compile("|".join(WAL_ALTS), re.I)
RCLINE = re.compile(r"^codex rc=(\d+)\s+stdout=(\d+) b")

codex, allerr, launch = [], [], []
for root in roots:
    for dp, dn, fn in os.walk(root):
        if os.sep + ".git" in dp or dp.endswith(".git"):
            continue
        for f in fn:
            fl = f.lower()
            p = os.path.join(dp, f)
            if fl.endswith(".err"):
                allerr.append(p)
                if "codex" in fl:
                    codex.append(p)
            if fl.endswith(".launch.log") or ("launch" in fl and (fl.endswith(".log") or fl.endswith(".txt"))):
                launch.append(p)

def read(p):
    try:
        return open(p, "rb").read().decode("utf-8", "replace")
    except OSError:
        return None

blocks = nomodel = twomodel = unclosed = ansi_blocks = ansi_answered = 0
banner_at, rule_at, model_at = Counter(), Counter(), Counter()
shape = Counter()
alt_i, alt_s, alt_files = Counter(), Counter(), Counter()
col0 = col0_files = 0
cls = both = 0
for p in codex:
    raw = read(p)
    if raw is None:
        continue
    rawlines = raw.split("\n")
    lines = ANSI.sub("", raw).split("\n")
    #  1. the opening block by the landed rule, with the cap
    h = 0; n = 0; body = []; closed = False; braw = []; bline = rline = 0; pre = []
    for i, l in enumerate(lines, 1):
        if i > 12 and h < 2:
            break
        if h == 0 and l.startswith("OpenAI Codex"):
            h = 1; bline = i; continue
        if h == 0:
            pre.append(l)
        if h == 1 and l.startswith("--------"):
            h = 2; rline = i; continue
        if h == 2 and l.startswith("--------"):
            closed = True; endline = i; break
        if h == 2:
            n += 1
            if n > 30:
                break
            body.append((i, l)); braw.append(rawlines[i - 1] if i - 1 < len(rawlines) else "")
    if h == 2:
        blocks += 1
        banner_at[bline] += 1; rule_at[rline] += 1
        ml = [(i, l) for i, l in body if l.startswith("model:")]
        nomodel += not ml
        twomodel += len(ml) > 1
        unclosed += not closed
        for i, l in ml[:1]:
            model_at[i] += 1
            v = l[len("model:"):]
            if v.startswith("\t") or v.startswith("  ") or v != v.rstrip() or "\r" in l:
                shape["WS"] += 1
        if any("model:" in l and not l.startswith("model:") for i, l in body):
            shape["MA"] += 1
        if any(l.startswith("OpenAI Codex") for i, l in body):
            shape["HB"] += 1
        if not ml and closed and any(l.startswith("model:") for l in lines[endline:endline + 30]):
            shape["NM"] += 1
        if any(l.startswith("--------") or ("OpenAI Codex" in l and not l.startswith("OpenAI Codex")) for l in pre):
            shape["BA"] += 1
        if any("\x1b" in r for r in braw):
            ansi_blocks += 1
            t = p[:-4] + ".txt"
            if os.path.exists(t) and os.path.getsize(t) > 0:
                ansi_answered += 1
    if any(re.fullmatch(r"-{7}\r?", l) for l in lines[:50]):
        shape["R7"] += 1
    #  3. column-0 ERROR lines, per alternative
    errl = [l for l in lines if l.startswith("ERROR:")]
    if errl:
        col0 += len(errl); col0_files += 1
    for a in REF_ALTS + WAL_ALTS:
        ci = [l for l in errl if re.search(a, l, re.I)]
        cs = [l for l in errl if re.search(a, l)]
        alt_i[a] += len(ci); alt_s[a] += len(cs); alt_files[a] += bool(ci)
    #  4. the empty-or-absent-sibling subset
    t = p[:-4] + ".txt"
    if (not os.path.exists(t)) or os.path.getsize(t) == 0:
        cls += 1
        if any(REF.search(l) for l in errl) and any(WAL.search(l) for l in errl):
            both += 1

def escapes(files):
    c = Counter()
    for p in files:
        raw = read(p)
        if raw is None:
            continue
        c["read"] += 1
        if "\x1b" in raw:
            c["esc"] += 1
            c["nonsgr"] += bool(NONSGR.search(raw))
            c["semisgr"] += bool(SEMISGR.search(raw))
            c["osc"] += bool(OSC.search(raw))
            c["other"] += bool(OTHERESC.search(raw))
    return c

rc_tab = Counter(); nlaunchlines = 0; nlaunchfiles = 0
for p in launch:
    raw = read(p)
    if raw is None:
        continue
    hit = False
    for l in raw.split("\n"):
        m = RCLINE.match(l)
        if m:
            hit = True; nlaunchlines += 1
            rc_tab[(int(m.group(1)), "empty" if m.group(2) == "0" else "stdout")] += 1
    nlaunchfiles += hit

print("roots: %s" % " ".join(roots))
print("POPULATIONS: CODEX %d files | ALLERR %d files | LAUNCH %d files (%d carrying a `codex rc=' line)"
      % (len(codex), len(allerr), len(launch), nlaunchfiles))
print("1. CODEX opening blocks by the landed rule (window 12, cap 30): %d of %d files | no model line: %d | two or more: %d | "
      "not closed within the cap: %d" % (blocks, len(codex), nomodel, twomodel, unclosed))
print("   banner line: %s" % dict(sorted(banner_at.items())))
print("   first rule line: %s" % dict(sorted(rule_at.items())))
print("   model line (file line): %s" % dict(sorted(model_at.items())))
print("   blocks carrying ANSI escapes: %d of %d (answered runs -- sibling .txt non-empty: %d)" % (ansi_blocks, blocks, ansi_answered))
print("   synthetic row shapes, blocks (R7: files): WS %d | MA %d | HB %d | NM %d | BA %d | R7 %d (of %d files)"
      % (shape["WS"], shape["MA"], shape["HB"], shape["NM"], shape["BA"], shape["R7"], len(codex)))
for name, files in (("CODEX", codex), ("ALLERR", allerr)):
    c = escapes(files)
    print("2. %s escapes: %d files read | with ESC %d | non-SGR CSI %d | `;'-joined SGR %d | OSC %d | other ESC %d"
          % (name, c["read"], c["esc"], c["nonsgr"], c["semisgr"], c["osc"], c["other"]))
print("3. CODEX column-0 ERROR lines (after the strip): %d lines in %d files" % (col0, col0_files))
for a in REF_ALTS + WAL_ALTS:
    print("   %-36s case-insensitive %5d lines / %4d files | case-sensitive %5d | case-only %d"
          % ("refusal: " + a if a in REF_ALTS else "wall: " + a, alt_i[a], alt_files[a], alt_s[a], alt_i[a] - alt_s[a]))
print("4. the empty-or-absent-sibling subset of CODEX: %d of %d files | carrying BOTH a refusal and a wall ERROR line: %d"
      % (cls, len(codex), both))
print("5. LAUNCH `codex rc=' lines: %d | %s" % (nlaunchlines, ", ".join("rc %d %s: %d" % (k[0], k[1], v) for k, v in sorted(rc_tab.items()))))
print("CENSUS_V5_DONE")
