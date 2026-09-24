# hygienecensus closing pass -- does the F2 repair (a token-level classifier, per-occurrence counts, relative paths, a dated --ruling) do what it says, and which of my dispositions of the F2 findings is wrong?

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated
wrongly.  **Check the premises, not just the derivations.**  Where I state something as
fact, ask whether it is true.  A seat that re-derives a premise from something this brief
did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/`** -- `regress/gate_hygiene.sh`, the new `regress/census_tokens.py`,
`tools/derive_hygiene_pins.sh`, and one comment in `regress/crime_width_probe.py`.  File-reading seats: read the FROZEN
copies in `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\census0923\c2_frozen\` (md5 prefixes: gate_hygiene.sh 6a9cb517,
census_tokens.py 662ce35a, derive_hygiene_pins.sh cbb8488d, crime_width_probe.py a0af7c92; the versions the F2 pass
reviewed: gate_hygiene.f2in.sh 4cfc4a65, derive_hygiene_pins.f2in.sh 3feb2a43; HEAD's gate: gate_hygiene.HEAD.sh
12e179ad), not the working files.  There are THREE pristine-2021-upstream copies of GXemul under the project root
(`./src/`, and two under `_archive/`); they are NOT this fork.

**If you cannot read files that is expected** -- every fact you need is inlined below.  Name any premise you cannot
settle from this packet rather than guessing at it.

**Where this brief states an ARITHMETIC claim -- a count, a set, a membership -- ENUMERATE it rather than reasoning
about it.**

**VERDICT LINE FIRST**: `VERDICT: SHIP` or `VERDICT: DO NOT SHIP -- <reason>`.

**THIS IS A CLOSING PASS, SO A ZERO NEEDS A DENOMINATOR.**  If you find no breach, say which edit shapes you tried
against which rows.  "Nothing found" and "nothing looked for" must not read the same.

## What the round is (plain engineering language)

Gate 6 (`gate_hygiene.sh`) carries a readiness census over the regression probes that drive the emulator through a
pseudo-terminal: how many such probes exist (73), which of them have NO prompt-readiness check (43, all named in a
grandfathered list), and how many use each known spelling of a prompt test -- a bare `endswith(">")` (frozen at 0), an
unrecognised spelling (frozen at 0), the whole-buffer `buf.rstrip().endswith("GXemul>")` (3, allowlisted per file:
`arm_bdt_probe.py:1 arm_flags_probe.py:2`), and the three fixed forms (24 each).  The weekly battery of 2026-09-20
FAILED gate 6 on `crime_width_probe.py`, whose `op.endswith("P")` was read as an unrecognised readiness spelling.

**The owner's rulings of 2026-09-23** ("re-pin, count all"): grandfather the untracked promptless probes by name;
allowlist the whole-buffer site at `arm_bdt_probe.py:76` at pin 3; fix the `crime_width_probe.py` spelling; ONE bulk
re-derivation of the pins by `tools/derive_hygiene_pins.sh --write`, never by hand; its own panel pass and a gate 6 run
before the next weekly battery (Sunday).

## The chain so far (artifacts under `regress/artifacts/hygienecensus_20260923/`)

1. The first repair; its pass 2 (`p2_20260923/`: nine seats + the Opus measuring seat, 14 evasions measured) -> the
   pass-2 repair (C1-C7).
2. The F2 findings-sharing pass (`f2_20260923/`: the panel, the Opus seat's measurement, a dedicated codex job).  The
   Opus seat measured **31 edits still passing** the pass-2 repair (7 of its 14 plus 24 new).  -> **THE F2 REPAIR**,
   reviewed here.

## The F2 repair -- what changed

1. **`regress/census_tokens.py` (NEW, inlined whole below).**  The census's POSITIVE classifications -- "this probe has
   a prompt-readiness check", "this file holds N whole-buffer sites" -- now read Python TOKENS: a COMMENT, a STRING or a
   DOCSTRING is not code; whitespace between tokens does not matter; sites are counted per OCCURRENCE; a file that cannot
   be read or tokenized is listed promptless.  The CLOSED-WORLD spelling counts (bare, unrecognised) deliberately stay
   textual, so text that spells the method still counts there -- the safe direction.
2. **`gate_hygiene.sh`**: the pty-probe list is built NUL-safe and by path RELATIVE to `regress/` (a subdirectory probe
   was being classified by a same-named top-level file; a filename with a space was split); the promptless list and
   both whole-buffer rows come from `census_tokens.py`; the old line-based `WHOLE_RE` is gone; and the records the F2
   pass found false are corrected in place (the grandfather note's arithmetic, the population term, the fresh-clone
   sentence, two "closed-world" overclaims).
3. **`tools/derive_hygiene_pins.sh`**: an owner ruling is now `--ruling "YYYY-MM-DD: <text>"` on the command line,
   format-checked, and WRITTEN into the gate as a `#  RULING ...` line above the pins it moved -- replacing a
   `WHOLE_FULL_RULING` environment variable that accepted any non-empty string and recorded nothing; a name given twice
   to `--grandfather`/`--release` is refused; `EXPECT_BARE` is now written when it FALLS (as `EXPECT_UNKNOWN` already
   was), so fixing a bare site no longer forces a hand edit; it evaluates the gate's own new enumerators.
4. **`crime_width_probe.py`**: one comment rescoped (it said the census was "CLOSED-WORLD over that method").

## Measured after the F2 repair

* **Controls** (`controls_f2/`): all 47 of the Opus seat's own edits (its `edits.py`), each applied to a fresh `/tmp`
  copy and graded by the repaired gate and deriver; `PREDICTIONS.txt` written at 15:24:00, the run at 15:24:31.  **All
  47 matched the prediction.**  `red N` = N readiness rows fail:

      real   PASS; --write rc=0 and the gate file byte-identical    e_c1   red 2   (single-quoted 4th whole-buffer site)
      e_e1   PASS (another receiver name -- FILED)                    e_e2   red 2   (predicate split across two lines)
      e_e3   red 2   (`endswith (` in the whole-buffer form)          e_e4   PASS (slice compare -- FILED)
      e_e5   PASS (`strip()` -- FILED)                                e_e6   red 1   (a site moved between the files)
      e_e7   red 3   (new promptless probe, space in its name)        e_e9   PASS (`buf.endswith (">")` -- FILED, first)
      e_e14  red 1   (grandfathered probe swapped for a new one)      n1a/n1b/n1c/n1d  red 2 each (predicate hidden by a
      n3a    red 2   (`rstrip( )`)                                           trailing comment / string / docstring)
      n3b    PASS (`(buf).rstrip()` -- FILED)                         n3c    PASS (`(buf.rstrip()).endswith` -- FILED)
      n3d    red 3   (`endswith( "GXemul>" )`)                        n3e    red 1   (`endswith(("GXemul>"))`)
      n3f    PASS (`rstrip("\r\n")` -- FILED)                         n3g    red 2   (`buf .rstrip()`)
      n3h    PASS (`self.buffer` -- FILED)                            n3i    PASS (re.search -- FILED)
      n3j    red 2   (two sites on one line)                          n3m    red 1   (a site moved between the files)
      n3k/n3k2 PASS (helper module outside the population -- FILED)   n4a    PASS (os.forkpty population split -- FILED)
      n10    PASS (the #37 form as a slice -- FILED)                  clone  red 3   (the three untracked probes absent)
      e_dL1/e_dL2/e_dL3/e_dL5, n2a, n2b, n5a, n6, n8, n8b, n11: red before; `--write` REFUSED (rc 5); red after
      n5b: red; --write REFUSED; --grandfather of an already-grandfathered name REFUSED (rc 4); red; --release REFUSED
      n7: red 2; --write REFUSED; `--ruling no` REFUSED (format); `--ruling "2026-09-23: ..."` WRITTEN; PASS; 2 RULING lines
      n9: PASS; --write WRITTEN (no change); --release REFUSED; PASS        n12: red 1 (denominator 74); --write; PASS

  **13 of 47 still pass, every one a different SPELLING of the same test** (e_e1 e_e4 e_e5 e_e9 n3b n3c n3f n3h n3i
  n3k n3k2 n4a n10) -- all FILED under `hygienecensusholes`.
* **The deriver's last three changes** (`controls_f2/FINAL_DERIVER.txt`): `--grandfather X X` REFUSED ("a name given
  more than once", rc 4, the list unchanged); `EXPECT_BARE` set to 1 while the tree holds 0 -> a red row, then `--write`
  wrote `EXPECT_BARE=0` and the row went green; `--write` on an unmodified copy -> the gate file byte-identical.
* **Gate 6 on the real tree** -- `run.sh 1 2 4 6`, alone, 15:40-15:49 (`regress/artifacts/fbd5/q2_20260923/gate2/`):
  `log-hygiene: PASS (36 checks)`, graded on the logs gate 4 produced in that same run; the readiness rows read
  `bare 0, unknown 0, denominator 73, promptless 43 = 43, names new=none gone=none, whole-buffer 3, per file
  "arm_bdt_probe.py:1 arm_flags_probe.py:2", #392 anchor/echo/mark 24/24/24`.  **Three comment-only edits were made
  after that run** (G10 below: two in gate_hygiene.sh, 3991fd8e -> 6a9cb517, and one in census_tokens.py's docstring,
  cf238c58 -> 662ce35a), so gate 6 is re-run before the commit.

## §C — SETTLED PREMISES (recorded resolutions; do not re-derive, but say if the diff contradicts one)

1. **The owner's rulings** (above) govern: grandfather by name, allowlist at pin 3, re-derive by the tool, never by
   hand.
2. **The census is a SPELLING census** (glm, pass 2): it guarantees which spellings of a prompt test exist, not that a
   probe's readiness logic is correct.  A probe can have a real readiness wait the census cannot see --
   `alpha_tbi_probe.py`'s `"gxemul>" in buf[...].lower()`, `drive_guest.py`'s `expect(boot_pat)` -- and is then listed
   promptless; that is the lexical proxy, stated, not a defect of this round.
3. **The stopping rule**: in-round only a MEASURED FALSE PASS or a WRONG RECORD in THIS round's material; pre-existing
   evasions are FILED (`hygienecensusholes`), not fixed here.
4. **D1 of pass 2 is settled by measurement**: the recogniser `full` accepts either quote, so a single-quoted
   whole-buffer site raises `allends` and `full` together and leaves `unknown` at 0.
5. **`crime_width_probe.py` is promptless** (it reads its guest by timed drains; several seats checked); it is
   grandfathered by name, and the owner is told it is a THIRD name beyond the two the ruling named -- not assumed
   authorised.  It is UNTRACKED and belongs to its own round (#529); a fresh clone of the census commit alone therefore
   reds three rows (stated in the gate's note).
6. **`luna_absentcpu_probe.py`'s `mark` -> `_mark`** (the spelling the fresh-mark count keys on) was reviewed in pass 2.

## §F2 — the F2 pass's findings, with MY disposition of each

*(Self-review is disclosed: I wrote the repair and every disposition.  Seats whose finding I adopted: check that the
CHANGE answers your finding, not merely that the finding was right.)*

**G1 -- the classifier's "reads code, not comments" was false**: a probe whose only call of the ends-with method sat in
a TRAILING comment, a string or a docstring was counted as prompt-detecting (Opus n1a-n1d measured; kimi-substitute;
grok; codex: "every other census here strips full-line comments" is false -- `_ptylist` searches raw text).
**ACCEPTED -> `census_tokens.py`** (tokens); n1a-n1d now red 2 each.
**G2 -- the whole-buffer rows counted LINES**: two sites on one line counted once (codex Q4, modelled; Opus n3j
measured; grok Q4).  **ACCEPTED -> per-occurrence token counts**; n3j red 2.
**G3 -- spacing and bracketing variants of the whole-buffer form** (`rstrip( )`, `buf .rstrip()`, `endswith (`,
`endswith( "GXemul>" )`) passed (Opus n3a, n3g, e_e3, n3d).  **ACCEPTED -> tokens ignore spacing**; all four red.
**G4 -- paths**: a subdirectory probe was judged by a same-named top-level file (Opus n5a, grok (a)); a name with a space
was split by a bare `xargs` (Opus e_e7).  **ACCEPTED -> relative paths, NUL-safe**; both red.
**G5 -- the `WHOLE_FULL_RULING` hatch** accepted any non-empty string, survived in an exported environment, and wrote
nothing down (codex (d), grok Q1(d)).  **ACCEPTED -> `--ruling "YYYY-MM-DD: <text>"`**, format-checked (at least 16
characters after the date; no quote, backslash, `$` or backtick), written as `#  RULING <text> -- <what it licensed>
(tools/derive_hygiene_pins.sh --write)` above the pins it moved; the variable is gone.  n7 control.
**G6 -- `--grandfather F F` wrote a duplicate name** (codex, running the extracted writer in memory: 45 entries, 44
unique; `--release` then failed an assertion).  **ACCEPTED -> refused** ("a name given more than once", rc 4).
**G7 -- `EXPECT_BARE` was never written when it FELL** (deepseek; grok: "both may fall" named two policies).
**ACCEPTED -> written downward only**, like `EXPECT_UNKNOWN`.
**G8 -- the grandfather note credited the twenty promptless probes with the denominator's 46 -> 70** (glm, codex,
grok).  **ACCEPTED**: "46 -> 66; four prompt-detecting probes committed in the same weeks (luna_absentcpu, m88k_exc,
arm_bdt, xscale_inten) took it to 70".
**G9 -- the population term said TWO alternatives; it is four, and `os.forkpty` was named invisible although the
pattern matches it** (grok Q5).  **ACCEPTED**, corrected.
**G10 -- "CLOSED-WORLD over that method" overstates** (glm, codex): `endswith (` with a space passes every count.
**ACCEPTED, and its SIBLINGS corrected too** (this is the only change after the 15:40 gate run): the crime_width comment
("it sees only literal spellings"), the #37 block's older "the only form that cannot be evaded by inventing a new way to
write it" (a dated note now says one spelling does), the gate's new sentence "they must see anything that COULD be a
predicate", and the same phrase in `census_tokens.py`'s own docstring.
**G11 -- the ledger rows the round's text cites (`hygienecensusholes`, `armbdtreadiness`) do not exist yet** (codex
Q5, grok Q5).  **ACCEPTED as a RECORDS-ORDER duty**: the records script writes them before the commit.
**G12 -- thirteen of the Opus seat's edits still pass after the F2 repair** (the list above).  **FILED
(`hygienecensusholes`)**: each is another SPELLING of the same test (another receiver name, `strip()`, a slice or
`re.search` compare, extra parentheses, `rstrip("\r\n")`, a helper module outside the population, `os.forkpty`),
outside a spelling census's reach by construction.
**G13 -- e9 (`buf.endswith (">")`, the #37 bare defect with one space) walks past the #37 row** (Opus; codex: "can
remain separate, but the claim it contradicts must change now"; grok: "no sentence this round writes is false because
of it").  **FILED, ranked first in `hygienecensusholes`**; the claims it contradicts are corrected (G10).
**G14 -- `crime_width_probe.py` extends a ruling that named two files** (codex (b)).  **ACCEPTED**: reported to the
owner as a third name (§C.5).
**G15 -- the promptless list is lexical, not behavioural** (codex D4, grok D4: `alpha_tbi_probe.py` and
`drive_guest.py` have real readiness waits).  **ACCEPTED as a statement** (§C.2); the gate's grandfather note names
`alpha_tbi_probe.py`, and its older paragraph on `drive_guest.py` stands.
**G16 -- the fresh-mark row checks the call's spelling, not the value** (`_mark = -len(self.buf)` passes; codex, pass
2).  **FILED** (in `hygienecensusholes`).

**D1 -- SHIP (minimax) vs DO NOT SHIP (codex, glm, deepseek, kimi-substitute, grok) on the F2 packet.**  Settled by
measurement: the DO NOT SHIP findings were real (the Opus seat's 31, codex's duplicate-name run).

**WHAT IS STILL OWED**: the gate 6 re-run on the final files; the flagship seat's adjudication; the records (ledger rows,
OUTSTANDING_BUGS, the CHANGELOG block) and the commit.  **WHERE I MIGHT BE FOOLING MYSELF**: I accepted or refined
thirteen of sixteen findings and FILED three -- and the thirteen still-passing spellings are all "filed" by MY reading
that each is a different spelling rather than a defect in what the census claims to count.

## The F2-repair diff (INLINED IN FULL)

    regress/census_tokens.py          NEW FILE -- inlined whole
    regress/gate_hygiene.sh           INLINED (diff of the F2-reviewed 4cfc4a65 against 6a9cb517)
    tools/derive_hygiene_pins.sh      INLINED (diff of the F2-reviewed 3feb2a43 against cbb8488d)
    regress/crime_width_probe.py      INLINED (the one comment)
    regress/luna_absentcpu_probe.py   NOT SHOWN -- unchanged since pass 2 reviewed it (§C.6)

### regress/census_tokens.py (NEW, 662ce35a)

```python
#!/usr/bin/env python3
"""census_tokens.py -- the TOKEN-level half of gate_hygiene.sh's readiness census (hygienecensus, 2026-09-23).

Why tokens.  The census's POSITIVE classifications -- "this probe has a prompt-readiness check", "this file holds N
whole-buffer sites" -- were line-level greps, and text on a code line that is not code counted as code: a trailing
comment, a string, a docstring.  Measured on the census round's F2 pass (the Opus seat): a probe whose only call of
the ends-with method was a trailing comment or a docstring was counted as prompt-detecting, two whole-buffer sites on
ONE line counted as one, and a probe in a subdirectory was classified by a same-named top-level file.  Python's own
tokenizer separates COMMENT and STRING tokens from code, so those three cannot happen here.

The CLOSED-WORLD counts (a bare prompt-suffix test, an unrecognised spelling of the ends-with call) are NOT done here
and must not be: they count TEXT on code lines, in the gate itself, so a comment or a string that spells the method
is counted -- the safe direction.  They see only the literal spelling with no space before the parenthesis (a space
passes them: hygienecensusholes e9).  THIS FILE IS SCANNED BY THOSE COUNTS TOO (it is a top-level regress/*.py),
which is why the method's name never appears here followed directly by an opening parenthesis -- not in code, not in
this docstring.

Usage (paths are read one per line from stdin, relative to the directory given):
    census_tokens.py promptless DIR   print each path with NO code-level call of the ends-with method: a NAME token
                                      spelled ENDS_WITH, followed by the OP token "(".  A file that cannot be read or
                                      tokenized is PRINTED (listed promptless: it cannot be read, so it is not trusted).
    census_tokens.py whole DIR        print "path:N" for each path with N > 0 code-level whole-buffer sites: a NAME
                                      whose last three letters are "buf", then ".", "rstrip", "(", ")", ".", ENDS_WITH,
                                      "(", a STRING whose value is exactly "GXemul>", ")".  Counted per OCCURRENCE,
                                      either quote, any spacing between the tokens.
Exit status 2 on a usage error; otherwise 0 (an unreadable file is an OUTPUT, never an exception).
"""
import ast, io, os, sys, tokenize

ENDS_WITH = "ends" + "with"          # spelled in two halves: see the docstring's third paragraph
SKIP = (tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT, tokenize.COMMENT, tokenize.ENCODING)


def code_tokens(path):
    src = io.open(path, encoding="utf-8", errors="strict").read()
    return [t for t in tokenize.generate_tokens(io.StringIO(src).readline) if t.type not in SKIP]


def has_ends_with_call(toks):
    return any(a.type == tokenize.NAME and a.string == ENDS_WITH and b.type == tokenize.OP and b.string == "("
               for a, b in zip(toks, toks[1:]))


def is_prompt_string(t):
    if t.type != tokenize.STRING:
        return False
    try:
        return ast.literal_eval(t.string) == "GXemul>"
    except (ValueError, SyntaxError):
        return False


SHAPE = [(tokenize.OP, "."), (tokenize.NAME, "rstrip"), (tokenize.OP, "("), (tokenize.OP, ")"), (tokenize.OP, "."),
         (tokenize.NAME, ENDS_WITH), (tokenize.OP, "("), (tokenize.STRING, None), (tokenize.OP, ")")]


def whole_sites(toks):
    n = 0
    for i in range(len(toks) - len(SHAPE)):
        head = toks[i]
        if head.type != tokenize.NAME or head.string[-3:] != "buf":
            continue
        rest = toks[i + 1:i + 1 + len(SHAPE)]
        if all(t.type == kind and (text is None or t.string == text) for (kind, text), t in zip(SHAPE, rest)) \
                and is_prompt_string(rest[7]):
            n += 1
    return n


def main(argv):
    if len(argv) != 3 or argv[1] not in ("promptless", "whole"):
        sys.stderr.write(__doc__)
        return 2
    mode, base = argv[1], argv[2]
    for line in sys.stdin.read().split("\n"):
        rel = line.strip("\r")
        if not rel:
            continue
        try:
            toks = code_tokens(os.path.join(base, rel))
        except (OSError, UnicodeDecodeError, tokenize.TokenError, SyntaxError, IndentationError):
            if mode == "promptless":
                print(rel)
            continue
        if mode == "promptless":
            if not has_ends_with_call(toks):
                print(rel)
        else:
            n = whole_sites(toks)
            if n:
                print("%s:%d" % (rel, n))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
```

### regress/gate_hygiene.sh (4cfc4a65 -> 6a9cb517)

```diff
--- a/regress/gate_hygiene.sh
+++ b/regress/gate_hygiene.sh
@@ -75,6 +75,11 @@
 #      unknown fails.  That converts "I grepped for the bad thing" into "I
 #      enumerated everything and recognised all of it", which is the only form
 #      that cannot be evaded by inventing a new way to write it.
+#      (*** 2026-09-23: "cannot be evaded" is FALSE for one spelling -- a space
+#      before the paren, `endswith (">")`, passes every count here, because all
+#      of them key on the literal `endswith(`.  Measured on a copy; filed as
+#      hygienecensusholes e9, ranked first.  The census is closed-world over the
+#      literal spellings, not over the method. ***)
 EXPECT_BARE=0
 EXPECT_UNKNOWN=0
 #  CODE ONLY.  The first version of this check counted a line of PROSE -- a
@@ -353,8 +358,9 @@
 #  census counts files, not commits: crime_width_probe.py (#529), arm_msrmode_probe.py (armmsrmodekill)
 #  and lca_isaphys_probe.py (#540).  The owner chose to count all three.  Consequence, stated so nobody
 #  meets it cold: until all three are committed, a FRESH CLONE counts FEWER than 73 (70 with none of them)
-#  and reds this row -- and the promptless-names row too, because all three are grandfathered names that
-#  exist only in the working tree.  Written by `tools/derive_hygiene_pins.sh --write`, never by hand. ***
+#  and reds THREE rows -- this one, the promptless count and the promptless-names row -- because all three are
+#  grandfathered names that exist only in the working tree (measured on a copy with them removed: 70/73, 40/43,
+#  names gone=the three).  Written by `tools/derive_hygiene_pins.sh --write`, never by hand. ***
 EXPECT_PTY_PROBES=73
 #  *** AND THE SAME PROBE BROKE A SECOND CENSUS IN THIS FILE, WHICH pass 11's OWN
 #  REPAIR DID NOT FIX.  Found by the codex seat reviewing that repair. ***
@@ -392,16 +398,18 @@
 crime_width_probe.py"
 #  hygienecensus: tools/derive_hygiene_pins.sh --grandfather appended THREE blocks to the list above; they are
 #  named here by their FIRST NAME, never by position, because the next --grandfather appends another.
-#  The block beginning `alpha_harness_probe.py` (derived 2026-09-19): 20 pty probes committed between
-#  2026-09-05 and 2026-09-18 that moved NO PIN -- they moved the promptless census (20 -> 40) and the
-#  denominator (46 -> 70) while EXPECT_PTY_PROBES sat at b78bb0f's 46.  None contains the literal
-#  `endswith(` this census keys on: most use fixed waits or drain-to-EOF, and alpha_tbi_probe.py has a real
-#  readiness wait the census cannot see (`"gxemul>" in buf[...].lower()`).  GRANDFATHERED, not converted:
+#  The block beginning `alpha_harness_probe.py` (derived 2026-09-19): 20 PROMPTLESS pty probes committed
+#  between 2026-09-05 and 2026-09-18 that moved NO PIN -- they moved the promptless census (20 -> 40) and the
+#  denominator (46 -> 66); four prompt-detecting probes committed in the same weeks (luna_absentcpu, m88k_exc,
+#  arm_bdt, xscale_inten) took it to 70, while EXPECT_PTY_PROBES sat at b78bb0f's 46.  None makes a CODE-level
+#  call of the ends-with method, which is this census's key: most use fixed waits or drain-to-EOF, and
+#  alpha_tbi_probe.py has a real readiness wait the census cannot see (`"gxemul>" in buf[...].lower()`).
+#  GRANDFATHERED, not converted:
 #  converting a probe's readiness is its own round.  The block beginning `arm_msrmode_probe.py`
 #  (2026-09-23, OWNER RULING): arm_msrmode_probe.py (armmsrmodekill) and lca_isaphys_probe.py (#540).  The
 #  block beginning `crime_width_probe.py` (2026-09-23, pass 2 of this round, under the same ruling's
 #  principle): crime_width_probe.py (#529), hidden from this census by a comment until the classifier below
-#  learned to skip comments.  All three are UNTRACKED and lying in the tree, named so the census passes on
+#  learned to read tokens.  All three are UNTRACKED and lying in the tree, named so the census passes on
 #  the tree the weekly battery runs.  Re-derive, never hand-edit: `bash tools/derive_hygiene_pins.sh` (report),
 #  `--grandfather NAME...` / `--release NAME...`, then `--write`.
 
@@ -415,19 +423,24 @@
 #  be scanned by two censuses and missed by this one.  Equal counts are not an aligned
 #  population, and reading the equality as safety is how the flat glob survived the
 #  first repair.
-_ptylist=$(find "$HERE" -name "*.py" -type f ! -path "$HERE/artifacts/*" 2>/dev/null \
-           | xargs grep -l "pty.fork" 2>/dev/null | sed "s|.*/||" | sort)
+#  hygienecensus F2: paths RELATIVE TO regress/, not basenames -- a probe in a subdirectory was classified by a
+#  same-named top-level file (measured: a promptless copy at newsub/ read as prompt-detecting), and a bare xargs
+#  split a filename holding a space.  For every file in regress/ itself the relative path IS the basename, so the
+#  grandfathered names are unchanged.
+_ptylist=$(find "$HERE" -name "*.py" -type f ! -path "$HERE/artifacts/*" -print0 2>/dev/null \
+           | xargs -0 grep -l "pty.fork" 2>/dev/null | sed "s|^$HERE/||" | LC_ALL=C sort)
 _ptyn=$(printf '%s' "$_ptylist" | grep -c . )
-#  hygienecensus pass 2 (2026-09-23): THE CLASSIFIER READS CODE, NOT COMMENTS.  It was a raw `grep -L "endswith("`,
-#  so a comment naming the method hid a promptless probe -- measured: crime_width_probe.py's only `endswith(` was a
-#  comment this very round added, and it kept the file out of this set (reworded, the count read 43 against 42).  Every
-#  other census here strips full-line comments; this one now does too.  A basename that is not a file in $HERE (a
-#  probe in a subdirectory -- none today) is listed as promptless: FAIL-CLOSED, it cannot be read, so it is not trusted.
-code_has() { grep -v '^[[:space:]]*#' "$1" 2>/dev/null | grep -q -- "$2"; }
-#  `printf '%s\n'`, NOT `printf '%s'`: $(...) strips the list's final newline, and `while read` then DROPS THE LAST
-#  FILE -- measured by this round's own controls, where a new promptless probe named zz_* sorted last and vanished
-#  from both promptless rows (the `xargs grep -L` this replaced did not care).
-_promptless=$(cd "$HERE" && printf '%s\n' "$_ptylist" | tr ' ' '\n' | while IFS= read -r f; do [ -z "$f" ] || code_has "$f" 'endswith(' || echo "$f"; done | LC_ALL=C sort)
+#  hygienecensus (2026-09-23): THE CLASSIFIER READS PYTHON TOKENS -- regress/census_tokens.py, where a COMMENT, a
+#  STRING or a DOCSTRING is not code.  It was a raw `grep -L "endswith("`, so text naming the method hid a
+#  promptless probe: crime_width_probe.py's only such text was a comment this very round added (pass 2).  The
+#  first repair stripped only FULL-LINE comments and said it "reads code" -- the F2 pass measured seven probes
+#  still hidden by a TRAILING comment, a string or a docstring (the Opus seat).  A token is what Python runs, so
+#  none of those can hide a probe now.  A file that cannot be read or tokenized is listed promptless (it cannot
+#  be read, so it is not trusted).  The spelling counts above deliberately stay textual, so a comment or a string
+#  that spells the method is counted -- the safe direction.  They see only the LITERAL `endswith(`: a space before
+#  the paren passes every one of them (hygienecensusholes e9).  `printf '%s\n'`, not `'%s'`: $(...) strips the list's last
+#  newline, and a line-reader then drops the last file -- measured by this round's own controls.
+_promptless=$(printf '%s\n' "$_ptylist" | python3 "$HERE/census_tokens.py" promptless "$HERE" | LC_ALL=C sort)
 _want=$(printf '%s' "$GRANDFATHERED_PROMPTLESS" | tr ' ' '
 ' | grep -c . )
 _got=$(printf '%s' "$_promptless" | grep -c . )
@@ -617,13 +630,14 @@
 #  owner chose to allowlist it BY NAME rather than convert it inside the census round.  Converting its
 #  readiness to #392's anchored form is FILED (`armbdtreadiness`).  A count alone would let a site MOVE
 #  between files unseen, so a second row pins each FILE WITH ITS OWN COUNT (WHOLE_FULL_FILES, `name:count`,
-#  sorted under LC_ALL=C).  Pass 2 of this round MEASURED two holes in the first form of these rows, both
-#  closed here: a set of names alone let a site move between the two files (count 3, set unchanged), and
-#  both patterns matched only the double-quoted spelling while the closed-world spelling census accepts
-#  both quotes -- so a single-quoted whole-buffer site passed every row.  WHOLE_RE takes either quote. ***
+#  sorted under LC_ALL=C).  Pass 2 of this round MEASURED two holes in the first form of these rows (a set of
+#  names let a site move between the two files; the pattern matched only the double-quoted spelling), and the
+#  F2 pass two more in the repair (the rows counted LINES, so two sites on one line read as one, and a site kept
+#  as a trailing comment after its conversion still counted).  Both rows now come from census_tokens.py: code
+#  tokens only, either quote, any spacing, every OCCURRENCE.  Other spellings of the same test -- another
+#  receiver name, `strip()`, a slice compare -- are the filed `hygienecensusholes`, not closed here. ***
 WHOLE_FULL_FILES="arm_bdt_probe.py:1 arm_flags_probe.py:2"
 EXPECT_WHOLE_FULL=3
-WHOLE_RE="buf.rstrip().endswith([\"']GXemul>[\"'])"
 #  *** ROW 3: SCOPED TO FILES THAT CAN DRIVE A REAL GUEST, rather than exempting a
 #  filename.  Adjudicated 2026-08-29; the name-exclusion form was WITHDRAWN. ***
 #
@@ -640,7 +654,8 @@
 #  the POPULATION needs neither an exemption nor a companion pin, and it subsumes the
 #  readiness_predicate_test.py case automatically.
 #
-#  THE POPULATION TERM IS TWO ALTERNATIVES, and the second is not hypothetical:
+#  THE POPULATION TERM IS FOUR ALTERNATIVES -- pty.fork, forkpty, pty.spawn, importing drive_guest (it said
+#  "TWO" until 2026-09-23) -- and the drive_guest one is not hypothetical:
 #  `selftest_absorb.py`, `selftest_budget.py` and `selftest_logdir.py` import
 #  drive_guest and contain NO pty.fork literal -- measured -- so a pty.fork-only term
 #  would let a guest-driving file out of the census.  None holds a whole-full site
@@ -656,8 +671,8 @@
 #  the defect would make this pin answer a question it is not asking.
 #
 #  DISCLOSED RESIDUALS, all real, none live today: `from pty import fork` with a bare
-#  fork(); `import pty as p`; a statement-local import; `os.forkpty` directly (which is
-#  what pty.fork wraps); `import regress.drive_guest`.  Censused at 0 apiece.  THE
+#  fork(); `import pty as p`; a statement-local import; `import regress.drive_guest`.  Censused at 0
+#  apiece.  (`os.forkpty` was listed here too until 2026-09-23 -- the pattern MATCHES it.)  THE
 #  PRESENT VALUE (3, pinned above) IS CORRECT; THAT DOES NOT ESTABLISH POPULATION COMPLETENESS.
 #
 #  `-print0 | xargs -0` matches both neighbours: a bare xargs finds ZERO files when a
@@ -673,12 +688,12 @@
                 | xargs -0 grep -lE 'pty\.fork|forkpty|pty\.spawn|^[[:space:]]*(import|from) drive_guest' 2>/dev/null; }
 pty_code() { pty_driving | tr '\n' '\0' \
              | xargs -0 grep -h "$1" 2>/dev/null | grep -v '^[[:space:]]*#'; }
-whole_full=$(pty_code "$WHOLE_RE" | grep -c .)
+#  hygienecensus 2026-09-23: the allowlist BY NAME, WITH EACH FILE'S OWN COUNT -- `path:count` for every file
+#  holding a CODE-token whole-buffer site (census_tokens.py; per occurrence), over the same pty-driving
+#  population, paths relative to regress/, sorted under LC_ALL=C and space-joined.  The count is their sum.
+whole_files=$(pty_driving | sed "s|^$HERE/||" | python3 "$HERE/census_tokens.py" whole "$HERE" | LC_ALL=C sort | tr '\n' ' ' | sed 's/ $//')
+whole_full=$(printf '%s\n' $whole_files | awk -F: 'NF > 1 {s += $NF} END {print s + 0}')
 check "readiness: whole-buffer full-prompt sites (allowlist)" "$whole_full" "$EXPECT_WHOLE_FULL"
-#  hygienecensus 2026-09-23: the allowlist BY NAME, WITH EACH FILE'S OWN COUNT -- `name:count` for every file
-#  holding a code-line whole-buffer site (full-line comments stripped; a trailing comment or a string still
-#  counts), over the same pty-driving population as the count above, sorted under LC_ALL=C and space-joined.
-whole_files=$(pty_driving | while IFS= read -r f; do n=$(grep -h "$WHOLE_RE" "$f" 2>/dev/null | grep -v '^[[:space:]]*#' | grep -c .); [ "$n" -gt 0 ] && printf '%s:%s\n' "$(basename "$f")" "$n"; done | LC_ALL=C sort | tr '\n' ' ' | sed 's/ $//')
 check "readiness: whole-buffer sites, per allowlisted file" "$whole_files" "$WHOLE_FULL_FILES"
 check "readiness: anchored full-prompt sites (#392)" "$conv_anchor" "$EXPECT_CONVERTED"
 check "readiness: echo guard present (#392)"         "$conv_echo"   "$EXPECT_CONVERTED"
```

### tools/derive_hygiene_pins.sh (3feb2a43 -> cbb8488d)

```diff
--- a/tools/derive_hygiene_pins.sh
+++ b/tools/derive_hygiene_pins.sh
@@ -3,36 +3,35 @@
 #  hand-editing numbers.  (hygienecensus, 2026-09-19: EXPECT_PTY_PROBES sat at 46 while 24 pty probes were committed
 #  over two weeks, and nothing said so until a pre-flight read of the weekly battery.)
 #
-#  It does NOT re-implement the counting.  It extracts the gate's own enumerator functions (py_code, probe_code,
-#  pty_driving, pty_code, code_has) and assignment lines (bare/allends/full, _ptylist/_ptyn/_promptless, conv_*,
-#  WHOLE_RE/whole_full/whole_files) out of gate_hygiene.sh by name and evaluates them -- so an edit to how the gate
-#  counts flows into the deriver.  An enumerator it cannot find is a hard error, never a zero.
+#  The COUNTS are the gate's own: it extracts the gate's enumerator functions (py_code, probe_code, pty_driving,
+#  pty_code) and assignment lines (bare/allends/full/unknown, _ptylist/_ptyn/_promptless, conv_*, whole_files,
+#  whole_full) out of gate_hygiene.sh by name and evaluates them -- so an edit to how the gate counts flows in here.
+#  An enumerator it cannot find is a hard error, never a zero.  (The promptless NAME comparison -- NEW and GONE -- is
+#  its own code, written to agree with the gate's names row.)
 #
-#    derive_hygiene_pins.sh                 report: got vs pinned, per census, the promptless NAMES that differ, and
-#                                           the untracked files the censuses count
-#    derive_hygiene_pins.sh --write         rewrite EXPECT_UNKNOWN, EXPECT_PTY_PROBES, EXPECT_CONVERTED,
-#                                           EXPECT_WHOLE_FULL and WHOLE_FULL_FILES in place (EXPECT_BARE is never
-#                                           written; see the refusals)
-#    derive_hygiene_pins.sh --grandfather F [F...]
-#                                           append the NAMED files to GRANDFATHERED_PROMPTLESS (deliberate, never bulk)
-#    derive_hygiene_pins.sh --release F [F...]
-#                                           remove NAMED files from GRANDFATHERED_PROMPTLESS -- only files that are
-#                                           grandfathered and no longer promptless (converted, or gone)
+#    derive_hygiene_pins.sh                           report: got vs pinned per census, the promptless names that
+#                                                     differ, and the untracked files the censuses count
+#    derive_hygiene_pins.sh --write [--ruling TEXT]   rewrite EXPECT_BARE and EXPECT_UNKNOWN (only ever DOWN),
+#                                                     EXPECT_PTY_PROBES, EXPECT_CONVERTED, EXPECT_WHOLE_FULL and
+#                                                     WHOLE_FULL_FILES
+#    derive_hygiene_pins.sh --grandfather F [F...]    append NAMED new promptless probes to GRANDFATHERED_PROMPTLESS
+#    derive_hygiene_pins.sh --release F [F...]        remove NAMED grandfathered probes that are no longer promptless
 #
 #  --write REFUSES, each with its reason printed, and the refusals are the point of the tool:
-#    * the pty denominator is 0 -- the enumerators saw nothing (wrong tree, moved file); it never re-pins to zero;
-#    * the three #392 counts (anchor, echo, fresh mark) disagree -- they share ONE pin, and a disagreement IS a
-#      defect (a guard present but uncounted): fix the probe, not the pin;
-#    * a promptless probe is neither grandfathered nor given prompt detection, or a grandfathered name is no longer
+#    * the pty denominator is 0 -- the enumerators saw nothing (wrong tree, moved file);
+#    * the three #392 counts (anchor, echo, fresh mark) disagree -- one pin, and a disagreement IS a defect;
+#    * a promptless probe is neither grandfathered nor given prompt detection, or a grandfathered probe is no longer
 #      promptless -- the gate grades the NAMES, so --grandfather / --release first;
-#    * EXPECT_BARE or EXPECT_UNKNOWN would RISE -- a bare `endswith(">")` and an unrecognised spelling are defects the
-#      gate freezes at its pin (both may fall);
-#    * EXPECT_WHOLE_FULL would rise, or WHOLE_FULL_FILES would change other than by SHRINKING (a file's count falling
-#      or a file leaving) -- #392 measured the whole-buffer form at 0/80, so a new site is never answered by raising
-#      the pin.  The ONE way past it is an owner ruling, named in the environment: WHOLE_FULL_RULING="<ruling>".
-#  (hygienecensus pass 2, 2026-09-23: the first version raised EXPECT_UNKNOWN and EXPECT_WHOLE_FULL on --write --
-#  measured -- never derived WHOLE_FULL_FILES, re-pinned to zero on an empty population, and reported success after
-#  its own writer failed.)
+#    * EXPECT_BARE or EXPECT_UNKNOWN would RISE -- defects the gate freezes at their pins (they may fall);
+#    * WITHOUT A RULING: EXPECT_CONVERTED would FALL (a #392 guard removed -- or an enumerator narrowed until it sees
+#      nothing), or EXPECT_WHOLE_FULL / WHOLE_FULL_FILES would change AT ALL (#392 measured the whole-buffer form at
+#      0/80; a site added, moved, respelled or converted is a decision, not a recount).
+#  --ruling "YYYY-MM-DD: <who ruled and why>" names that decision; it must look like one, and --write writes it into
+#  the gate as a comment line above every pin it moves, so the change carries its warrant in the diff.
+#  (hygienecensus 2026-09-23, two measured passes: the first version raised EXPECT_UNKNOWN and EXPECT_WHOLE_FULL, never
+#  derived WHOLE_FULL_FILES, re-pinned to zero on an empty population and reported success after its writer failed;
+#  the second let EXPECT_CONVERTED fall silently, re-pinned two censuses to 0 after a one-character enumerator edit,
+#  and took its escape hatch from an environment variable that left no record and accepted "no".)
 #
 #  Run it from anywhere; HERE is the regress directory beside this script's tools/ directory ($GXROOT overrides).
 set -u
@@ -43,14 +42,21 @@
 [ -d "$HERE" ] || HERE="$(cd "$(dirname "$0")/../regress" 2>/dev/null && pwd)"
 G="$HERE/gate_hygiene.sh"
 [ -f "$G" ] || { echo "DERIVE_FAIL: no gate_hygiene.sh at $G"; exit 2; }
-MODE=report; GF=()
+MODE=report; GF=(); RULING=""
 case "${1:-}" in
-    --write) MODE=write ;;
+    --write) MODE=write; shift
+             if [ "${1:-}" = --ruling ]; then RULING="${2:-}"; shift 2; fi
+             [ $# -eq 0 ] || { echo "usage: $0 --write [--ruling \"YYYY-MM-DD: text\"]"; exit 2; } ;;
     --grandfather) MODE=grandfather; shift; GF=("$@") ;;
     --release) MODE=release; shift; GF=("$@") ;;
     "") ;;
-    *) echo "usage: $0 [--write | --grandfather FILE... | --release FILE...]"; exit 2 ;;
+    *) echo "usage: $0 [--write [--ruling TEXT] | --grandfather FILE... | --release FILE...]"; exit 2 ;;
 esac
+if [ -n "$RULING" ]; then
+    printf '%s' "$RULING" | grep -qE '^[0-9]{4}-[0-9]{2}-[0-9]{2}: .{16,}$' \
+        || { echo "REFUSED: a ruling reads \"YYYY-MM-DD: <who ruled and why>\" (16+ characters of reason) -- got [$RULING]"; exit 2; }
+    case "$RULING" in *'"'*|*'\'*|*'$'*|*'`'*) echo "REFUSED: the ruling text may not contain quotes, backslashes, \$ or backticks"; exit 2 ;; esac
+fi
 
 fn() {  # extract a shell function definition by name: from `name() {` through the first line ending in `}`
     awk -v n="$1" 'index($0, n "() {")==1 {p=1} p {print} p && /}[[:space:]]*$/ {exit}' "$G"
@@ -61,11 +67,11 @@
         p {print; q += gsub(/\047/, "\047"); if ($0 !~ /\\$/ && q % 2 == 0) exit}' "$G"
 }
 CODE=""
-for f in py_code probe_code pty_driving pty_code code_has; do
+for f in py_code probe_code pty_driving pty_code; do
     d=$(fn $f); [ -n "$d" ] || { echo "DERIVE_FAIL: enumerator $f() not found in gate_hygiene.sh"; exit 3; }
     CODE="$CODE$d"$'\n'
 done
-for v in bare allends full unknown _ptylist _ptyn _promptless conv_anchor conv_echo conv_mark WHOLE_RE whole_full whole_files; do
+for v in bare allends full unknown _ptylist _ptyn _promptless conv_anchor conv_echo conv_mark whole_files whole_full; do
     a=$(asg $v); [ -n "$a" ] || { echo "DERIVE_FAIL: assignment $v= not found in gate_hygiene.sh"; exit 3; }
     CODE="$CODE$a"$'\n'
 done
@@ -75,15 +81,14 @@
 
 pin() { sed -n "s/^$1=\([0-9]*\).*/\1/p" "$G" | head -1; }
 spin() { sed -n "s/^$1=\"\(.*\)\"$/\1/p" "$G" | head -1; }
-[ "${_ptyn:-0}" -gt 0 ] 2>/dev/null || { echo "DERIVE_FAIL: the pty denominator is ${_ptyn:-empty} -- the enumerators saw nothing; refusing to report or write zeros"; exit 3; }
+[ "${_ptyn:-0}" -gt 0 ] 2>/dev/null || { echo "DERIVE_FAIL: the pty denominator is ${_ptyn:-empty} -- the enumerators saw nothing; refusing to report or write"; exit 3; }
 _want=$(printf '%s' "$GRANDFATHERED_PROMPTLESS" | tr ' ' '\n' | grep -c .)
 _got=$(printf '%s' "$_promptless" | grep -c .)
 GFS=$(printf '%s' "$GRANDFATHERED_PROMPTLESS" | tr ' ' '\n' | grep . | LC_ALL=C sort)
 NEWP=$(LC_ALL=C comm -13 <(printf '%s\n' "$GFS") <(printf '%s\n' "$_promptless" | grep .))
 GONE=$(LC_ALL=C comm -23 <(printf '%s\n' "$GFS") <(printf '%s\n' "$_promptless" | grep .))
-#  -prune, not `! -path`: the old form still DESCENDED into artifacts/ (thousands of files) once per probe, which made
-#  one report take minutes over /mnt/c.  The untracked list it prints must not change (checked by the controls).
-UNTR=$(cd "$HERE" && printf '%s\n' $_ptylist | while read -r f; do p=$(find . -path ./artifacts -prune -o -name "$f" -print | head -1); git -C "$HERE" ls-files --error-unmatch "$p" >/dev/null 2>&1 || echo "$f"; done)
+#  paths are RELATIVE to regress/ (the gate's own form since 2026-09-23), so look each one up directly.
+UNTR=$(printf '%s\n' "$_ptylist" | while IFS= read -r p; do [ -z "$p" ] || git -C "$HERE" ls-files --error-unmatch "$p" >/dev/null 2>&1 || echo "$p"; done)
 WFP=$(spin WHOLE_FULL_FILES)
 
 printf '%-34s %6s %6s\n' census got pinned
@@ -105,8 +110,13 @@
 
 if [ "$MODE" = grandfather ] || [ "$MODE" = release ]; then
     [ ${#GF[@]} -gt 0 ] || { echo "REFUSED: --$MODE needs the file names, one by one"; exit 4; }
+    #  a name given twice was appended twice (45 entries, 44 names) and --release then could not remove it -- the
+    #  census F2 pass, codex, measured on the writer itself.  One name, once.
+    dup=$(printf '%s\n' "${GF[@]}" | LC_ALL=C sort | uniq -d | tr '\n' ' ')
+    [ -z "$dup" ] || { echo "REFUSED: a name given more than once: $dup"; exit 4; }
     for f in "${GF[@]}"; do
         if [ "$MODE" = grandfather ]; then
+            printf '%s\n' "$GFS" | grep -qxF -- "$f" && { echo "REFUSED: $f is already grandfathered"; exit 4; }
             printf '%s\n' $NEWP | grep -qxF -- "$f" || { echo "REFUSED: $f is not a NEW promptless probe"; exit 4; }
         else
             printf '%s\n' $GONE | grep -qxF -- "$f" || { echo "REFUSED: $f is not a grandfathered name that is no longer promptless"; exit 4; }
@@ -122,7 +132,7 @@
     body = body + "\n" + " ".join(names)
 else:
     for n in names:
-        body, k = re.subn(r"(?<![\w.])%s(?![\w.])" % re.escape(n), "", body)
+        body, k = re.subn(r"(?<![\w./])%s(?![\w.])" % re.escape(n), "", body)
         assert k == 1, (n, k)
     body = "\n".join(" ".join(l.split()) for l in body.split("\n"))
     body = "\n".join(l for l in body.split("\n") if l.strip())
@@ -139,26 +149,30 @@
     [ -z "$GONE" ] || { echo "REFUSED: grandfathered names are no longer promptless -- --release them first"; exit 5; }
     [ "$bare" -le "$(pin EXPECT_BARE)" ] || { echo "REFUSED: bare endswith(\">\") grew -- a defect, never re-pinned"; exit 5; }
     [ "$unknown" -le "$(pin EXPECT_UNKNOWN)" ] || { echo "REFUSED: an unrecognised endswith( spelling appeared -- a defect, never re-pinned"; exit 5; }
-    shrink=$("$PY" -c '
-import sys
-def parse(t): return dict((p.rsplit(":", 1)[0], int(p.rsplit(":", 1)[1])) for p in t.split())
-got, pinned = parse(sys.argv[1]), parse(sys.argv[2])
-print("yes" if all(n in pinned and c <= pinned[n] for n, c in got.items()) else "no")' "$whole_files" "$WFP") || { echo "DERIVE_FAIL: WHOLE_FULL_FILES does not parse (got [$whole_files] pinned [$WFP])"; exit 6; }
-    if [ "$whole_full" -gt "$(pin EXPECT_WHOLE_FULL)" ] || [ "$shrink" != yes ]; then
-        [ -n "${WHOLE_FULL_RULING:-}" ] || { echo "REFUSED: the whole-buffer sites grew or moved (got [$whole_files], pinned [$WFP]) -- #392 measured that form at 0/80; convert the site, or name an owner ruling in WHOLE_FULL_RULING"; exit 5; }
-        echo "WHOLE_FULL_RULING: $WHOLE_FULL_RULING"
+    NEED=""
+    [ "$conv_anchor" -ge "$(pin EXPECT_CONVERTED)" ] || NEED="$NEED EXPECT_CONVERTED($(pin EXPECT_CONVERTED)->$conv_anchor)"
+    [ "$whole_full" = "$(pin EXPECT_WHOLE_FULL)" ] || NEED="$NEED EXPECT_WHOLE_FULL($(pin EXPECT_WHOLE_FULL)->$whole_full)"
+    [ "$whole_files" = "$WFP" ] || NEED="$NEED WHOLE_FULL_FILES([$WFP]->[$whole_files])"
+    if [ -n "$NEED" ] && [ -z "$RULING" ]; then
+        echo "REFUSED: these pins change only by a named decision --$NEED -- a #392 guard removed, or a whole-buffer site added, moved, respelled or converted; fix the probe, or pass --ruling \"YYYY-MM-DD: <who ruled and why>\""
+        exit 5
     fi
-    pywrite "$G" "$unknown" "$_ptyn" "$conv_anchor" "$whole_full" "$whole_files" <<'PY'
+    pywrite "$G" "$bare" "$unknown" "$_ptyn" "$conv_anchor" "$whole_full" "$whole_files" "$RULING" "$NEED" <<'PY'
 import io, re, sys
-g, unk, pty, conv, whole, files = sys.argv[1:]
+g, bare, unk, pty, conv, whole, files, ruling, need = sys.argv[1:]
 s = io.open(g, encoding="utf-8", newline="").read()
-for k, v in (("EXPECT_UNKNOWN", unk), ("EXPECT_PTY_PROBES", pty), ("EXPECT_CONVERTED", conv), ("EXPECT_WHOLE_FULL", whole)):
-    s, n = re.subn(r"(?m)^%s=\d+" % k, "%s=%s" % (k, v), s, count=1)
+note = ("#  RULING %s -- %s (tools/derive_hygiene_pins.sh --write)\n" % (ruling, need.strip())) if (ruling and need.strip()) else ""
+for k, v in (("EXPECT_BARE", bare), ("EXPECT_UNKNOWN", unk), ("EXPECT_PTY_PROBES", pty), ("EXPECT_CONVERTED", conv),
+             ("EXPECT_WHOLE_FULL", whole)):
+    pre = note if (note and k + "(" in need) else ""
+    s, n = re.subn(r"(?m)^%s=\d+" % k, lambda m, k=k, v=v, pre=pre: pre + "%s=%s" % (k, v), s, count=1)
     assert n == 1, k
-s, n = re.subn(r'(?m)^WHOLE_FULL_FILES="[^"\n]*"', 'WHOLE_FULL_FILES="%s"' % files, s, count=1)
+pre = note if (note and "WHOLE_FULL_FILES(" in need) else ""
+s, n = re.subn(r'(?m)^WHOLE_FULL_FILES="[^"\n]*"', lambda m: pre + 'WHOLE_FULL_FILES="%s"' % files, s, count=1)
 assert n == 1, "WHOLE_FULL_FILES"
 io.open(g, "w", encoding="utf-8", newline="").write(s)
-print("WRITTEN: EXPECT_UNKNOWN=%s EXPECT_PTY_PROBES=%s EXPECT_CONVERTED=%s EXPECT_WHOLE_FULL=%s WHOLE_FULL_FILES=\"%s\"" % (unk, pty, conv, whole, files))
+print("WRITTEN: EXPECT_BARE=%s EXPECT_UNKNOWN=%s EXPECT_PTY_PROBES=%s EXPECT_CONVERTED=%s EXPECT_WHOLE_FULL=%s "
+      "WHOLE_FULL_FILES=\"%s\"%s" % (bare, unk, pty, conv, whole, files, ("  RULING: " + ruling) if note else ""))
 PY
 fi
 echo "DERIVE_DONE"
```

### regress/crime_width_probe.py (the one comment)

```diff
--- a/regress/crime_width_probe.py (the comment the F2 pass reviewed)
+++ b/regress/crime_width_probe.py (now)
@@ the comment above the re-spelled test @@
-    #  hygienecensus (2026-09-23, owner ruling): spelled `op[-1:] == "P"', not with the str method -- identical over the
-    #  eight op strings ACCEPTS produces (and on ""), but gate_hygiene's spelling census is CLOSED-WORLD over that method
-    #  and counted this operation-name test as a readiness predicate it could not classify (got=1 want=0 at the
-    #  2026-09-20 battery).  This probe has NO prompt predicate -- session() reads by timed drains -- so it is
-    #  grandfathered by name as promptless; pass 2 found that an earlier wording of THIS comment had hidden that.
+    #  hygienecensus (2026-09-23, owner ruling): spelled `op[-1:] == "P"', not with the str method -- identical over the
+    #  eight op strings ACCEPTS produces (and on ""), but gate_hygiene's spelling census counts every literal call of
+    #  that method on a code line and reads one it does not recognise as a readiness predicate it cannot classify; it
+    #  read got=1 want=0 on this line at the 2026-09-20 battery.  (It sees only literal spellings: a space before the
+    #  paren passes it -- filed as hygienecensusholes.)  This probe has NO prompt predicate -- session() reads by timed
+    #  drains -- so it is grandfathered by name as promptless; pass 2 found that an earlier wording of THIS comment
+    #  had hidden that.
     if op[-1:] == "P":
```

## §E -- QUESTIONS (answer each, numbered; answering from this packet alone, do Q1(c) and Q3 first)

**Q1 -- verify what the repair claims.**
 (a) `census_tokens.py` against its own docstring: for each shape it claims -- a trailing comment, a string, a
     docstring, spacing between tokens, either quote, per-occurrence counting, an unreadable or untokenizable file
     listed promptless -- does the code do it?  Is there a shape it claims and does not handle?
 (b) the deriver's refusals against its header: ENUMERATE every refusal the code can print and every refusal the
     header promises.  Is any in one list and not the other?
 (c) G12's thirteen still-passing edits: is each genuinely a DIFFERENT SPELLING of the test, outside what a spelling
     census claims to count -- or is one of them a shape this repair CLAIMS to close (a token-level variant of a
     spelling it does count)?
**Q2 -- the smallest edit that passes every readiness row and is not one of the thirteen filed shapes.**  Name the edit
and the rows you expect to stay green.  If you find none, give your denominator: which shapes, against which rows.
**Q3 -- adjudicate the §F2 list.**  G1..G16 and D1: UPHOLD / OVERTURN / REFINE / CANNOT SETTLE, one line each with a
reason.  Then: **WHICH OF MY ACCEPTED DISPOSITIONS IS WRONG?**  I accepted or refined thirteen of sixteen.
**Q4 -- records.**  Is any sentence in the changed comments (the gate's, `census_tokens.py`'s docstring, the deriver's
header, the crime_width comment) false as of today?  In particular: are G10's four corrections now TRUE, and does any
SIBLING of the "closed-world" overclaim survive anywhere in these files?
**Q5 -- option-set completeness.**  e9 (`buf.endswith (">")`) is FILED.  The textual counts could instead key on
`endswith` followed by optional whitespace and `(`.  Is there a reason not to close it in THIS round that survives the
stopping rule, or a disposition I did not name?

If, while verifying a claim, you found something ELSE -- say so.

End with a seat record: model, what you read, what you ran.


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
