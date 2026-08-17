#!/usr/bin/env python3
"""CENSUS: every call site in src/devices/ that can terminate the emulator process.

*** WHY THIS IS A SCRIPT AND NOT A NUMBER IN A CHANGELOG. ***

An inventory of these sites was recorded on 2026-08-15 as "220 sites, 114 in-handler,
17 init, 89 helper" -- a remembered grep, with no committed instrument. Two days later a
panel re-derived it four different ways and got 302 / 280 / 260 / 247, and six of seven
seats concluded the record was unsound. It was not: a measure seat rebuilt the scan and
found 220 reproduces EXACTLY at `84f442d`, the HEAD it was recorded on, and is 215 today
because #433 removed five sites. **The record was stale by one round, and nothing could
tell the difference between stale and wrong, because the method was gone.**

So the census ships as an instrument. Re-run it and the number is current by construction.

*** THREE MEASURED REASONS A TEXTUAL grep IS THE WRONG UNIT, all of them load-bearing. ***

1. **COMMENTS AND IDENTIFIERS.** 87 of 302 textual matches are not calls. Worse, 22 are
   prose written by this project's OWN FIX ROUNDS -- `dev_8253.c` carries
   `/* #223: warn+ignore, don't exit() the host */`, and so do dev_footbridge, dev_kn02ba
   and dev_vga. **The raw count therefore GROWS EVERY TIME A SITE IS FIXED.** It is
   anti-correlated with the defect it claims to measure.

2. **MACRO-MEDIATED TERMINATION IS INVISIBLE TO EVERY `exit(` PATTERN.**
   `src/include/misc.h` defines CHECK_ALLOCATION -> FAILURE -> exit(1), and a census that
   greps for `exit(` reports none of them. They are the majority of all terminators here,
   and a handful sit inside DEVICE_ACCESS handlers -- including a `malloc(512 * count)` in
   dev_wdc.c where the count is guest-set.

   *** THE COUNTS ABOVE AND BELOW ARE DELIBERATELY NOT WRITTEN DOWN HERE. *** Run the
   script; its output is the answer. Numbers quoted in prose are what created the problem
   this file exists to solve -- a docstring cannot be re-run, so its figures rot silently
   while looking authoritative. The one snapshot worth dating: on 2026-08-17 this reported
   398 sites (215 direct + 183 macro), 120 of them inside a DEVICE_ACCESS handler.

3. **`exit(2)` AND `abort()` EXIST.** Patterns built only from `exit(1)`/`exit(0)` miss
   `dev_pmagja.c` and `dev_px.c`; `abort()` appears both as a call and inside the
   identifier `le_tx_abort`, which a naive pattern counts four times.

*** WHAT THIS SCRIPT DELIBERATELY DOES NOT DO. *** It does not decide whether a site is a
DEFECT. Terminating from a device-init function because the machine cannot be built as
asked is CORRECT; terminating from inside a guest register access is not. The script
reports the bucket and leaves the judgement to a round, because the judgement needs the
site's semantics and a script does not have them.

Usage:
    python census_exits.py                 # counts, by bucket
    python census_exits.py --by-file       # per-file table, worst first
    python census_exits.py --list ACCESS   # every site in one bucket
    python census_exits.py --json          # machine-readable, for a gate row
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SEC = os.environ.get("GXSEC") or os.path.normpath(os.path.join(HERE, "..", ".."))
DEVDIR = os.path.join(SEC, "src", "devices")

#  Direct terminators. `\b` on the name keeps `le_tx_abort(` out; the identifier is a real
#  function in dev_le.c and a bare `abort(` matches it four times.
DIRECT = re.compile(r"\b(exit|abort)\s*\(")
#  Macro-mediated: these expand to exit(1) through misc.h's FAILURE.
MACRO = re.compile(r"\b(CHECK_ALLOCATION|FAILURE)\s*\(")
#  Handler roots. A site's bucket is decided by the function it sits in.
ACCESS_RE = re.compile(r"^\s*DEVICE_ACCESS\s*\(")
INIT_RE = re.compile(r"^\s*(DEVINIT\s*\(|\w[\w\s*]*\bdev\w*_init\s*\()")
FUNC_RE = re.compile(r"^[A-Za-z_][\w \t*]*\**(\w+)\s*\(")


def func_name(ln):
    """The identifier immediately before the first '(' -- i.e. the function's name.

    FUNC_RE's own capture group cannot be used for this: `[\\w \\t*]*` is greedy, so on
    `static void vga_crtc_reg_write(` it swallows the name and captures the single letter
    `e`. Harmless to the COUNTS, which key on the bucket, but the census exists to be READ
    by someone deciding which sites matter, and a table of one-letter function names is
    not readable. Take the last identifier before the paren instead.
    """
    head = ln.split("(", 1)[0]
    toks = re.findall(r"\w+", head)
    return toks[-1] if toks else "?"


def strip_noncode(src):
    """Blank out comments and string literals, preserving line structure.

    Byte-for-byte length is not preserved -- only NEWLINES are -- because every consumer
    here is line-oriented. Getting this wrong in the other direction (dropping lines) would
    silently shift every reported line number, which is worse than a wrong count: a wrong
    count is visible, a wrong citation is believed.
    """
    out, i, n = [], 0, len(src)
    while i < n:
        c = src[i]
        if c == "/" and i + 1 < n and src[i + 1] == "*":
            j = src.find("*/", i + 2)
            j = n if j < 0 else j + 2
            out.append("\n" * src.count("\n", i, j))
            i = j
        elif c == "/" and i + 1 < n and src[i + 1] == "/":
            j = src.find("\n", i)
            j = n if j < 0 else j
            i = j
        elif c in "\"'":
            q, j = c, i + 1
            while j < n and src[j] != q:
                j += 2 if src[j] == "\\" else 1
            out.append(" ")
            i = min(j + 1, n)
        else:
            out.append(c)
            i += 1
    return "".join(out)


def bucket_of(lines, idx):
    """Walk backwards to the enclosing function definition and classify it."""
    for k in range(idx, -1, -1):
        ln = lines[k]
        if ACCESS_RE.match(ln):
            return "ACCESS", ln.strip()
        if INIT_RE.match(ln) and "(" in ln:
            return "INIT", ln.strip()
        m = FUNC_RE.match(ln)
        #  A brace in column 0 on the next line is the usual definition shape here.
        if m and not ln.lstrip().startswith(("if", "for", "while", "switch", "return")):
            if k + 1 < len(lines) and lines[k + 1].startswith("{"):
                return "HELPER", func_name(ln)
        #  MULTI-LINE SIGNATURES.  This tree wraps long parameter lists, so the name can sit
        #  several lines above the `{`.  Without this, dev_ps2_gif.c:88 landed in UNKNOWN --
        #  and a bucket called UNKNOWN that nobody ever resolves is the blank-cell problem in
        #  miniature: it reads as "nothing here" when it means "not looked at".
        if ln.startswith("{"):
            for j in range(k - 1, max(k - 12, -1), -1):
                mm = FUNC_RE.match(lines[j])
                if mm and not lines[j].lstrip().startswith(
                        ("if", "for", "while", "switch", "return")):
                    if ACCESS_RE.match(lines[j]):
                        return "ACCESS", lines[j].strip()
                    if INIT_RE.match(lines[j]):
                        return "INIT", lines[j].strip()
                    return "HELPER", func_name(lines[j])
    return "UNKNOWN", "?"


def census():
    rows = []
    for fn in sorted(os.listdir(DEVDIR)):
        if not fn.endswith(".c"):
            continue
        path = os.path.join(DEVDIR, fn)
        with open(path, encoding="utf-8", errors="replace") as f:
            raw = f.read()
        lines = strip_noncode(raw).split("\n")
        for i, ln in enumerate(lines):
            for rx, kind in ((DIRECT, "direct"), (MACRO, "macro")):
                if rx.search(ln):
                    b, fname = bucket_of(lines, i)
                    rows.append({"file": fn, "line": i + 1, "kind": kind,
                                 "bucket": b, "func": fname[:60],
                                 "text": ln.strip()[:90]})
    return rows


def main(argv):
    rows = census()
    if "--json" in argv:
        print(json.dumps(rows, indent=1))
        return 0

    if "--check" in argv:
        #  THE ONE THING WORTH FAILING ON, and deliberately NOT a pinned count.
        #  Pinning "398" would recreate the exact disease this script cures: the number
        #  goes stale, someone re-derives it differently, and nobody can tell stale from
        #  wrong. What must never drift is the parser's COVERAGE -- if the tree grows a
        #  function shape bucket_of() cannot classify, the site lands in UNKNOWN and
        #  silently stops being counted anywhere. That is a blind spot, and a blind spot
        #  reads exactly like a clean bill of health.
        unknown = [r for r in rows if r["bucket"] == "UNKNOWN"]
        if unknown:
            print("CENSUS_FAIL  %d site(s) the parser could not attribute to a function:"
                  % len(unknown))
            for r in unknown[:20]:
                print("    %s:%d  %s" % (r["file"], r["line"], r["text"][:60]))
            print("  These are counted in the total and in NO bucket, so every bucket")
            print("  below understates. Extend bucket_of() rather than ignoring them.")
            return 1
        print("CENSUS_PASS  %d sites, all attributed to an enclosing function" % len(rows))
        return 0

    for a in argv:
        if a == "--list":
            want = argv[argv.index("--list") + 1].upper() if len(argv) > argv.index("--list") + 1 else "ACCESS"
            for r in rows:
                if r["bucket"] == want:
                    print("%-28s:%-5d %-6s %-34s %s"
                          % (r["file"], r["line"], r["kind"], r["func"], r["text"][:44]))
            return 0

    direct = [r for r in rows if r["kind"] == "direct"]
    macro = [r for r in rows if r["kind"] == "macro"]

    def n(rs, b):
        return sum(1 for r in rs if r["bucket"] == b)

    if "--by-file" in argv:
        per = {}
        for r in rows:
            d = per.setdefault(r["file"], {"ACCESS": 0, "HELPER": 0, "INIT": 0, "UNKNOWN": 0})
            d[r["bucket"]] += 1
        print("%-30s %7s %7s %6s %8s" % ("file", "ACCESS", "HELPER", "INIT", "UNKNOWN"))
        for fn, d in sorted(per.items(), key=lambda kv: -kv[1]["ACCESS"]):
            if sum(d.values()):
                print("%-30s %7d %7d %6d %8d"
                      % (fn, d["ACCESS"], d["HELPER"], d["INIT"], d["UNKNOWN"]))
        return 0

    print("census_exits: process-terminating call sites in src/devices/")
    print()
    print("  %-10s %7s %7s %7s %9s %7s" % ("kind", "ACCESS", "HELPER", "INIT", "UNKNOWN", "total"))
    print("  " + "-" * 52)
    for label, rs in (("direct", direct), ("macro", macro)):
        print("  %-10s %7d %7d %7d %9d %7d"
              % (label, n(rs, "ACCESS"), n(rs, "HELPER"), n(rs, "INIT"),
                 n(rs, "UNKNOWN"), len(rs)))
    print("  " + "-" * 52)
    print("  %-10s %7d %7d %7d %9d %7d"
          % ("TOTAL", n(rows, "ACCESS"), n(rows, "HELPER"), n(rows, "INIT"),
             n(rows, "UNKNOWN"), len(rows)))
    print()
    print("  ACCESS  = inside a DEVICE_ACCESS handler: a guest load/store reaches it.")
    print("  HELPER  = a plain function; guest-reachable ONLY if called from a handler,")
    print("            which this script does NOT resolve -- reachability is a separate")
    print("            question and pretending otherwise would overstate the ACCESS bucket.")
    print("  INIT    = device construction. Terminating here is usually CORRECT.")
    print()
    print("  This counts SITES, not defects. Whether a site should stop the emulator")
    print("  depends on its semantics, which a script does not have.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
