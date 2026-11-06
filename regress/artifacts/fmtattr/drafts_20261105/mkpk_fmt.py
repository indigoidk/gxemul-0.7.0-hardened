#!/usr/bin/env python3
"""mkpk_fmt.py -- Gemini drafting packets for the format round (fmtattr + fmtmissarg + the x11.c comma), from GCC's warnings.
Groups ../fmt_warnings.tsv's -Wformat= and -Wformat-extra-args warnings by file, packs files into packets of about MAXL warning
lines, and inlines each flagged line with two lines of context (HEAD line numbers; `u` marks a line whose text is unique in
the file).  Gemini returns exact old/new edits; apply_fmt.py applies them and a GCC build with the four attributes verifies.
Writes PKT_<n>.md beside this script and prints the plan."""
import collections
import io
import os
import subprocess

REPO = "C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC"
D = "C:/DocumentNoSnc/cc/GXEMUL/_scratchpad/codescan/"
O = D + "fmtfix/"
MAXL = 24
files = subprocess.run(["git", "-C", REPO, "ls-files", "src"], capture_output=True, text=True).stdout.split()
where = {}
for f in files:
    where.setdefault(os.path.basename(f), f)
W = collections.OrderedDict()
for l in io.open(D + "fmt_warnings.tsv", encoding="utf-8"):
    p = l.rstrip("\n").split("\t")
    if len(p) != 4 or p[2] not in ("-Wformat=", "-Wformat-extra-args"):
        continue
    f = where[os.path.basename(p[0])]
    W.setdefault(f, []).append((int(p[1]), p[2], p[3]))
RULES = """## The fix rules (from the round's adjudication -- follow them exactly)

1. PRESERVE MEANING AND RADIX.  A `%i` stays decimal and a `%x` stays hex; do not convert everything to hex.
2. A 64-bit value printed in hex: the tree's idiom is `"0x%" PRIx64` (or `"%" PRIx64`) with the argument cast `(uint64_t)`.  A
   64-bit value printed in decimal: `"%" PRIi64` with `(int64_t)` or `"%" PRIu64` with `(uint64_t)`.
3. An `(int)` or `(unsigned)` cast is allowed ONLY where the value is small by construction (an offset inside a device's own
   register window, a register number, a byte, a loop index).  Say so in the `why` field.  Never narrow a value that can be
   large (an address, a 64-bit register, a size from the guest).
4. `size_t` -> `%zu` (or `%zx`); `long long` -> `%lli`/`%llx`; a pointer printed with `%x` -> `%p` with a `(void *)` cast.
5. A format with MORE conversions than arguments: add the missing argument ONLY if its value is computed at that point; if the
   value is not available yet (for example a variable still zero there), REMOVE the unsupported conversion instead.
6. A format with FEWER conversions than arguments (`-Wformat-extra-args`): first check for a missing conversion or a stray comma
   splitting a string literal; otherwise drop the extra argument.
7. Change nothing else: no reflowing, no renaming, no new comments.  Tabs stay tabs.  Keep lines within 79 columns where the
   original was; split a string literal with C's adjacent-literal concatenation if needed.
"""
pk, cur, n = [], [], 0
for f, ws in W.items():
    if cur and n + len(ws) > MAXL:
        pk.append(cur); cur, n = [], 0
    cur.append(f); n += len(ws)
if cur:
    pk.append(cur)
for k, group in enumerate(pk, 1):
    parts = []
    for f in group:
        src = subprocess.run(["git", "-C", REPO, "show", "HEAD:" + f], capture_output=True).stdout.decode("utf-8", "replace")
        L = src.split("\n")
        cnt = collections.Counter(x.strip() for x in L)
        ws = W[f]
        lines = sorted(set(x for ln, _, _ in ws for x in range(max(1, ln - 2), min(len(L), ln + 2) + 1)))
        blocks, prev = [], None
        for x in lines:
            if prev is not None and x != prev + 1:
                blocks.append("     ...")
            blocks.append("%5d%s| %s" % (x, "u" if cnt[L[x - 1].strip()] == 1 else " ", L[x - 1]))
            prev = x
        parts.append("### `%s` (%d warnings)\n\nGCC:\n%s\n\n```c\n%s\n```\n" % (
            f, len(ws), "\n".join("- line %d: %s (`%s`)" % (ln, m, kd) for ln, kd, m in ws), "\n".join(blocks)))
    body = "\n".join([
        "# GXemul hardened fork -- fix printf-format mismatches (packet %d of %d; a defensive code-quality task)" % (k, len(pk)), "",
        "PROJECT FRAMING -- a defensive software-robustness project.  GXemul is a computer-architecture emulator.  Its diagnostic",
        "functions `debug`, `fatal`, `debugmsg` and `debugmsg_cpu` are printf-like, and GCC (given printf-format attributes) reports",
        "the calls below whose format does not match its arguments.  You cannot read files; each flagged line is inlined with two",
        "lines of context and its line number (`u` = that line's text occurs once in its file).  This is a DRAFTING task: write the",
        "edits.  `uint64_t` is `unsigned long` on this platform and `<inttypes.h>` is already included.", "",
        RULES, "## The warnings and their code", "", "\n".join(parts),
        "## WHAT TO RETURN", "",
        "EXACTLY ONE fenced ```json block: a list of edits, one per changed call, applied to the file named in each:",
        '  [{"file": "src/...", "old": "<exact text from the code above, without the line-number prefix; must occur EXACTLY ONCE in that '
        'file>", "new": "<replacement>", "why": "<one line: which rule, and for a narrowing cast why the value is small>"}]',
        "Use JSON escapes: \\t for a tab, \\n for a newline.  Prefer one whole `u` line as `old`; include a neighbouring line only to",
        "make it unique.  Cover EVERY warning listed; if one should not change, say so after the json block with its line.", ""])
    io.open(O + "PKT_%d.md" % k, "w", encoding="utf-8", newline="\n").write(body)
    print("PKT_%d.md: %d files, %d warnings, %d bytes" % (k, len(group), sum(len(W[f]) for f in group), len(body.encode())))
