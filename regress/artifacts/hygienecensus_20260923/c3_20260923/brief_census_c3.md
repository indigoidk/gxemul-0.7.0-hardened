# hygienecensus -- the F3 repair's own pass: does it close what the closing pass measured, and which of my dispositions of that pass's findings is wrong?

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly.  **Check the premises,
not just the derivations.**  A seat that re-derives a premise from something this brief did NOT give it is worth more
than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/`** -- `regress/census_tokens.py`, `regress/gate_hygiene.sh`,
`tools/derive_hygiene_pins.sh`.  File-reading seats: read the FROZEN copies in
`C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\census0923\c3_frozen\` (md5 prefixes: census_tokens.py 029fba36,
gate_hygiene.sh 4220b6ee, derive_hygiene_pins.sh f9533e22; the versions the closing pass reviewed:
census_tokens.c2.py 662ce35a, gate_hygiene.c2.sh 6a9cb517, derive_hygiene_pins.c2.sh cbb8488d), not the working files.
There are pristine-2021-upstream copies of GXemul under the project root (`./src/`, `_archive/`); they are NOT this fork.

**If you cannot read files that is expected** -- every fact you need is inlined below.  Name any premise you cannot
settle from this packet rather than guessing.  **ENUMERATE** any count or set rather than reasoning about it.
**VERDICT LINE FIRST**: `VERDICT: SHIP` or `VERDICT: DO NOT SHIP -- <reason>`.  **A zero needs a denominator**: if you
find nothing, say which edit shapes you tried against which rows.

## Where the census round stands

Gate 6's readiness census counts, over the probes that drive the emulator through a pseudo-terminal, which spellings of
a prompt-readiness test they use and which probes have none (the owner's rulings of 2026-09-23: "re-pin, count all";
grandfather by name; allowlist the whole-buffer site at `arm_bdt_probe.py:76`; one bulk re-derivation by
`tools/derive_hygiene_pins.sh --write`, never by hand).  Pass 2 -> the pass-2 repair; the F2 findings-sharing pass ->
the F2 repair (a Python-TOKEN classifier, per-occurrence counts, relative paths, a dated `--ruling`); **the closing pass
(panel `panel_20260923_173123`, the Opus measuring seat, a dedicated codex job) -> THIS, the F3 repair.**

## The F3 repair -- what changed (the full diff is inlined below)

1. **`census_tokens.py` keeps STATEMENT BOUNDARIES** (NEWLINE is no longer skipped; NL, the newline inside brackets,
   still is), so a method REFERENCE on one statement and a parenthesised string on the next is no longer one call;
   **a call must be a METHOD call** -- the name must follow a `.` -- so a function DEFINITION under that name is not
   credited; `ValueError` (an embedded NUL in a path) is caught like the other read errors; the docstring's claims
   corrected.
2. **The deriver's `--ruling`** refuses any CONTROL character (a newline let a valid first line carry live shell into
   the gate) and needs at least 16 NON-BLANK characters of reason; **`--grandfather` / `--release`** quote their name
   lists and refuse a name holding whitespace or a glob character by name (the list is space-separated); **`--release`
   matches names EXACTLY** (a boundary regex matched `foo.py` inside `pref-foo.py`); the header corrected.
3. **`gate_hygiene.sh`**: comment corrections only (listed under H11 below).  Its rows are unchanged.

## Measured (on `/tmp` copies; predictions written before each run; all in `regress/artifacts/hygienecensus_20260923/`)

* **The closing pass's disputed readings, on the F2 files** (`controls_c2/`, predictions 17:57:53, run 17:57:54):
  `t_comma` (`buf.rstrip().endswith("GXemul>",)` appended), `t_slice` (`...endswith("GXemul>"[:])`), `t_plus`
  (`...endswith("GXemul>"+"")`) -- **red 1 each, the unrecognised-spelling row**, as predicted (grok and agy had read them
  as passing every row); `t_nljoin` (arm_bdt:76 turned into `ready = self.buf.rstrip().endswith` / `("GXemul>")` /
  `if ready:`) -- **PASS: a real false pass**; `t_tilde` (`if ~self.buf.rstrip().endswith("GXemul>"):`) -- PASS, the
  lexical limit; `t_rnl` (a `--ruling` with an embedded newline) -- **WRITTEN, and two live `echo INJECTED` lines landed
  in the gate**; `t_defend` (m88k's calls renamed, `def endswith():` added) -- red 1, **not the PASS I predicted**: the
  textual count reads `def endswith(` as an unrecognised spelling (corrected in `PREDICTIONS.corrections`).
* **The F3 repair** (`controls_c3/`, predictions 18:05:33, run 18:06:26), all as predicted: `real` PASS, the deriver's
  report equals every pin, `--write` byte-identical; **the 45 edits of the F2 controls give the same verdicts they gave
  on the F2 files** (13 still pass -- the filed ones); `t_nljoin` **red 2** (whole-buffer 2/3 and the per-file row);
  `t_comma` / `t_slice` / `t_plus` red 1; `t_defend` red 3; `t_defendsp` (`def endswith (self):`, with a space, the
  calls renamed) **red 2** -- it passed every row on the F2 files; `t_tilde` PASS (disclosed); the newline, tab and
  whitespace-only rulings **REFUSED** (rc 2) with the gate unchanged; a promptless probe named `zz opus.py` -- the gate
  reds 3 rows and `--grandfather "zz opus.py"` is **REFUSED** by name (rc 4); `--release gdrom_cond_probe.py` with
  `x-gdrom_cond_probe.py` also grandfathered removes exactly the one name (an exact read of the list:
  `t_relpref_exact.txt`; the first run's line-grep could not tell the list from a comment -- `NOTE.txt`).
* **Owed**: gate 6 on the final files, in the next quiet slot (the gate's rows are unchanged by F3; its classifier is not).

## §C — SETTLED PREMISES (recorded resolutions; say if the diff contradicts one)

1. The owner's rulings govern; the pins are written by the deriver, never by hand.
2. **The census is a SPELLING census**: it guarantees which spellings of a readiness test exist, not that a probe's
   readiness logic is right.  A semantic change that keeps the spelling (`~`, `not`, a comparison) is outside it
   (`t_tilde`), as is a probe with a real readiness wait written without the method (`alpha_tbi_probe.py`,
   `drive_guest.py`).
3. **The stopping rule**: in-round only a measured false pass or a wrong record in THIS round's material; pre-existing
   holes are FILED.
4. The recogniser `full` needs `)` immediately after the quote, so an unrecognised spelling reds `unknown` (measured
   again this pass: `t_comma`, `t_slice`, `t_plus`).
5. `crime_width_probe.py` is promptless and grandfathered by name; it is a THIRD name beyond the two the owner's ruling
   named, and the owner is told so.

## §F2 — the closing pass's findings, with MY disposition of each

*(Self-review disclosed: I wrote the repair and these dispositions.  Seats whose finding I adopted: check the CHANGE
answers it.)*

**H1 -- statement boundaries were dropped** (codex panel Q2 and codex-dedicated TASK 1; my `t_nljoin`: a real false
pass).  **ACCEPTED -> NEWLINE kept** (`t_nljoin` red 2).
**H2 -- a function DEFINITION under the method's name was credited as a call** (codex-dedicated).  **ACCEPTED -> a `.`
must precede the name** (`t_defend` red 3, `t_defendsp` red 2).
**H3 -- a `--ruling` holding a newline wrote live shell into the gate** (kimi-substitute, grok, codex, codex-dedicated,
the Opus seat; my `t_rnl`).  **ACCEPTED -> any control character refused** (`t_rnl`, `t_rtab` refused).
**H4 -- a whitespace-only reason passed** (the Opus seat).  **ACCEPTED -> 16 non-blank characters** (`t_rblank`).
**H5 -- the name checks expanded `$NEWP` / `$GONE` unquoted** (split and globbed), **and a space-named probe could not
be grandfathered** (codex, codex-dedicated, grok).  **ACCEPTED -> quoted; a name with whitespace or a glob character is
refused by name** (`t_spacegf`).  Fail-closed before, too: the gate reds on such a probe either way.
**H6 -- `--release` matched `foo.py` inside `pref-foo.py`** (codex).  **ACCEPTED -> exact names** (`t_relpref`).
**H7 -- "above every pin it moves" overstated where a ruling is written** (codex, codex-dedicated).  **ACCEPTED as
wording**: above each pin change that NEEDED a ruling.
**H8 -- a trailing comma, `[:]` or `+""` after the string evades the whole-buffer rows** (grok, agy).  **REJECTED BY
MEASUREMENT**: the unrecognised-spelling row reds each one.  The token counter does miss them; the closed-world count
is what catches them, by design.
**H9 -- the blanket rationale "thirteen alternate spellings outside a spelling census" was false** (glm, deepseek,
codex, grok).  **ACCEPTED**: per item, NINE are other spellings of the test (e_e1, e_e4, e_e5, n3b, n3c, n3f, n3h,
n3i, n10), THREE are POPULATION omissions (n3k, n3k2 -- a helper module that forks no pty; n4a -- a promptless probe
forking with `os.forkpty`, outside `_ptylist`), and e9 is a SPACING of a spelling the census DOES count (H10).
**H10 -- e9 (`buf.endswith (">")`): fix now or file?** (deepseek: fix, a measured false pass; codex: filing is
acceptable, closing it is optional; the Opus seat: filing is right -- widening a closed-world count is not free and owes
its own pass; glm: the rationale was false).  **FILED, with the rationale corrected**: it is IN reach -- one regex
family (`endswith[[:space:]]*(` in `py_code`'s filter and in `bare` / `allends` / `full`) -- and deferred because it
widens a CLOSED-WORLD count, which owes its own pass and its own audit of the prose the wider pattern would then count.
**H11 -- wrong records in this round's comments** (codex, grok, glm, codex-dedicated): the #37 block's "any
indirection through a helper" (twice); "The owner chose to count all three" (true of the DENOMINATOR -- the owner said
"count all" -- and now says the third name's GRANDFATHERING is the part the ruling did not name); "until the classifier
learned to read tokens" (pass 2's comment stripping exposed crime_width; tokens came with F2); "seven probes" (seven
EDITS on five files); "NUL-safe" (as far as grep; `grep -l` prints lines); census_tokens.py's docstring (the
subdirectory fix was the gate's relative paths, not the tokenizer; whole mode prints nothing for an unreadable file;
f-strings tokenize as code only on Python 3.12+).  **ACCEPTED, all corrected.**
**H12 -- the control counts were wrong** (codex): `controls_f2` is **45 edits** plus the unmodified `real` (46 lines),
not 47; and the F2 Opus seat's "31 edits still pass (7 + 24)" is, re-derived from its own `runs2`-`runs4/TABLE.txt`,
**34 PASS -- 32 without n5b and n7, which pass only through a deriver option -- = 7 of the fourteen + 25 new**.
**ACCEPTED**; the records carry the derived figures.
**H13 -- pre-existing gate text**: the #392 truth table's content pins strip only full-line comments (codex-dedicated),
and three stale literals ("EVERY current probe is promptless", "all fifteen of each", "2 bad arms, but 3 good
occurrences").  **FILED** (pre-existing; decayed legacy counts are filed, not swept).
**H14 -- `~`, `not` or a comparison around the call keeps its spelling** (codex-dedicated TASK 3).  **DISCLOSED** (§C.2).
**H15 -- a file that tokenizes but would not compile is graded** (codex-dedicated).  **DISCLOSED** in the docstring.
**H16 -- an embedded NUL in a path raised an uncaught `ValueError`** (codex-dedicated).  **ACCEPTED -> caught.**
**H17 -- "G10 cites non-existent docstring text"** (agy).  **REJECTED**: the sentence G10 corrected no longer exists
because G10 corrected it.

**D1 -- SHIP (the Opus seat, minimax) vs DO NOT SHIP (codex, grok, glm, deepseek, the kimi substitute, agy).**  Settled
by measurement: H1 and H3 were real (`t_nljoin`, `t_rnl`), and the Opus seat's forty new edits had not included either
shape.  **WHERE I MIGHT BE FOOLING MYSELF**: I accepted or refined thirteen of seventeen findings.

## The F3-repair diff (INLINED IN FULL -- each against the version the closing pass reviewed)

    regress/census_tokens.py        INLINED (662ce35a -> 029fba36)
    regress/gate_hygiene.sh         INLINED (6a9cb517 -> 4220b6ee, comments only)
    tools/derive_hygiene_pins.sh    INLINED (cbb8488d -> f9533e22)

### regress/census_tokens.py (662ce35a -> 029fba36)

```diff
--- a/regress/census_tokens.py
+++ b/regress/census_tokens.py
@@ -4,9 +4,17 @@
 Why tokens.  The census's POSITIVE classifications -- "this probe has a prompt-readiness check", "this file holds N
 whole-buffer sites" -- were line-level greps, and text on a code line that is not code counted as code: a trailing
 comment, a string, a docstring.  Measured on the census round's F2 pass (the Opus seat): a probe whose only call of
-the ends-with method was a trailing comment or a docstring was counted as prompt-detecting, two whole-buffer sites on
-ONE line counted as one, and a probe in a subdirectory was classified by a same-named top-level file.  Python's own
-tokenizer separates COMMENT and STRING tokens from code, so those three cannot happen here.
+the ends-with method was a trailing comment or a docstring was counted as prompt-detecting, and two whole-buffer sites
+on ONE line counted as one.  Python's tokenizer separates COMMENT and STRING tokens from code, and every occurrence is
+a separate match, so neither can happen here.  (A probe in a subdirectory judged by a same-named top-level file was
+the third defect that pass measured; the GATE fixed that, by passing paths relative to regress/.)
+
+Statement boundaries are KEPT.  The first version dropped NEWLINE tokens with the other layout tokens, so a method
+REFERENCE on one statement and a parenthesised string on the next -- `x = buf.rstrip().endswith` / `("GXemul>")` --
+read as one whole-buffer call, and a probe whose readiness test had been turned into that passed every row (measured by
+the census closing pass, controls_c2/t_nljoin).  NL, the newline INSIDE brackets, is still layout.  And a call is a
+METHOD call: the name must follow a "." -- a function DEFINITION under that name calls nothing, and the first version
+credited one (codex, the same pass).
 
 The CLOSED-WORLD counts (a bare prompt-suffix test, an unrecognised spelling of the ends-with call) are NOT done here
 and must not be: they count TEXT on code lines, in the gate itself, so a comment or a string that spells the method
@@ -16,19 +24,24 @@
 this docstring.
 
 Usage (paths are read one per line from stdin, relative to the directory given):
-    census_tokens.py promptless DIR   print each path with NO code-level call of the ends-with method: a NAME token
-                                      spelled ENDS_WITH, followed by the OP token "(".  A file that cannot be read or
-                                      tokenized is PRINTED (listed promptless: it cannot be read, so it is not trusted).
+    census_tokens.py promptless DIR   print each path with no method call of the ends-with method: the OP token ".",
+                                      a NAME token spelled ENDS_WITH, the OP token "(", in one statement.  A file that
+                                      cannot be read or tokenized is PRINTED (listed promptless: it cannot be read, so it
+                                      is not trusted).  Tokens are not a parse: a file that tokenizes but would not
+                                      compile is graded like any other.
     census_tokens.py whole DIR        print "path:N" for each path with N > 0 code-level whole-buffer sites: a NAME
                                       whose last three letters are "buf", then ".", "rstrip", "(", ")", ".", ENDS_WITH,
-                                      "(", a STRING whose value is exactly "GXemul>", ")".  Counted per OCCURRENCE,
-                                      either quote, any spacing between the tokens.
-Exit status 2 on a usage error; otherwise 0 (an unreadable file is an OUTPUT, never an exception).
+                                      "(", a STRING whose value is exactly "GXemul>", ")", in one statement.  Counted
+                                      per OCCURRENCE, either quote, any spacing between the tokens.  An unreadable file
+                                      prints NOTHING here (it has no count); the promptless mode is what names it.
+Exit status 2 on a usage error; otherwise 0 -- an unreadable path is an output (promptless) or a missing count (whole),
+never an exception.  On Python 3.12 and later an f-string's replacement fields are tokenized as code, so a call inside
+one counts; on earlier versions it is one STRING token and does not (no probe relies on either).
 """
 import ast, io, os, sys, tokenize
 
 ENDS_WITH = "ends" + "with"          # spelled in two halves: see the docstring's third paragraph
-SKIP = (tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT, tokenize.COMMENT, tokenize.ENCODING)
+SKIP = (tokenize.NL, tokenize.INDENT, tokenize.DEDENT, tokenize.COMMENT, tokenize.ENCODING)   # NEWLINE is KEPT
 
 
 def code_tokens(path):
@@ -37,8 +50,9 @@
 
 
 def has_ends_with_call(toks):
-    return any(a.type == tokenize.NAME and a.string == ENDS_WITH and b.type == tokenize.OP and b.string == "("
-               for a, b in zip(toks, toks[1:]))
+    return any(d.type == tokenize.OP and d.string == "." and a.type == tokenize.NAME and a.string == ENDS_WITH
+               and b.type == tokenize.OP and b.string == "("
+               for d, a, b in zip(toks, toks[1:], toks[2:]))
 
 
 def is_prompt_string(t):
@@ -78,7 +92,7 @@
             continue
         try:
             toks = code_tokens(os.path.join(base, rel))
-        except (OSError, UnicodeDecodeError, tokenize.TokenError, SyntaxError, IndentationError):
+        except (OSError, ValueError, UnicodeDecodeError, tokenize.TokenError, SyntaxError, IndentationError):
             if mode == "promptless":
                 print(rel)
             continue
```

### regress/gate_hygiene.sh (6a9cb517 -> 4220b6ee)

```diff
--- a/regress/gate_hygiene.sh
+++ b/regress/gate_hygiene.sh
@@ -71,8 +71,11 @@
 #    - accept either quote style;
 #    - and make the check CLOSED-WORLD: every .endswith() in the tree must use
 #      one of the two KNOWN literals.  A third spelling -- including
-#      endswith(PROMPT) or any indirection through a helper -- is unknown, and
-#      unknown fails.  That converts "I grepped for the bad thing" into "I
+#      endswith(PROMPT), or a helper's own endswith( line when the helper is
+#      a .py file under regress/ -- is unknown, and unknown fails.  (A helper
+#      module that forks no pty is still COUNTED here, but a probe that calls
+#      it has no readiness spelling of its own to census -- hygienecensusholes
+#      n3k.)  That converts "I grepped for the bad thing" into "I
 #      enumerated everything and recognised all of it", which is the only form
 #      that cannot be evaded by inventing a new way to write it.
 #      (*** 2026-09-23: "cannot be evaded" is FALSE for one spelling -- a space
@@ -139,7 +142,7 @@
 bare=$(py_code | grep -o "endswith([\"']>[\"'])" | wc -l)
 #  Every endswith( in code, minus the two we recognise: the bare prompt above
 #  and the correct full prompt.  Anything left is a spelling nobody reviewed --
-#  including endswith(PROMPT) or any indirection through a helper.
+#  including endswith(PROMPT), wherever it sits under regress/ (a helper module included).
 allends=$(py_code | grep -o "endswith(" | wc -l)
 full=$(py_code | grep -o "endswith([\"']GXemul>[\"'])" | wc -l)
 unknown=$((allends - bare - full))
@@ -356,7 +359,9 @@
 #  70, so this gate was RED AT HEAD -- measured on a pure export of HEAD's regress/, not inferred.  73 =
 #  those 70 plus THREE UNTRACKED probes that lie in the tree and are counted as they sit, because the
 #  census counts files, not commits: crime_width_probe.py (#529), arm_msrmode_probe.py (armmsrmodekill)
-#  and lca_isaphys_probe.py (#540).  The owner chose to count all three.  Consequence, stated so nobody
+#  and lca_isaphys_probe.py (#540).  The owner chose to count all three in this denominator (2026-09-23,
+#  "count all"); grandfathering crime_width_probe.py as PROMPTLESS is the part the ruling did not name -- it was
+#  reported to the owner as a third name, not assumed authorised.  Consequence, stated so nobody
 #  meets it cold: until all three are committed, a FRESH CLONE counts FEWER than 73 (70 with none of them)
 #  and reds THREE rows -- this one, the promptless count and the promptless-names row -- because all three are
 #  grandfathered names that exist only in the working tree (measured on a copy with them removed: 70/73, 40/43,
@@ -408,8 +413,9 @@
 #  converting a probe's readiness is its own round.  The block beginning `arm_msrmode_probe.py`
 #  (2026-09-23, OWNER RULING): arm_msrmode_probe.py (armmsrmodekill) and lca_isaphys_probe.py (#540).  The
 #  block beginning `crime_width_probe.py` (2026-09-23, pass 2 of this round, under the same ruling's
-#  principle): crime_width_probe.py (#529), hidden from this census by a comment until the classifier below
-#  learned to read tokens.  All three are UNTRACKED and lying in the tree, named so the census passes on
+#  principle): crime_width_probe.py (#529), hidden from this census by a comment until pass 2 stopped the
+#  classifier reading full-line comments (it reads tokens since the F2 repair).  All three are UNTRACKED and lying
+#  in the tree, named so the census passes on
 #  the tree the weekly battery runs.  Re-derive, never hand-edit: `bash tools/derive_hygiene_pins.sh` (report),
 #  `--grandfather NAME...` / `--release NAME...`, then `--write`.
 
@@ -425,7 +431,9 @@
 #  first repair.
 #  hygienecensus F2: paths RELATIVE TO regress/, not basenames -- a probe in a subdirectory was classified by a
 #  same-named top-level file (measured: a promptless copy at newsub/ read as prompt-detecting), and a bare xargs
-#  split a filename holding a space.  For every file in regress/ itself the relative path IS the basename, so the
+#  split a filename holding a space.  NUL-safe as far as grep: `grep -l` prints one name per LINE, so a file name
+#  holding a newline is not supported (and a name holding a space cannot be grandfathered -- the list is
+#  space-separated; the deriver refuses it by name).  For every file in regress/ itself the relative path IS the basename, so the
 #  grandfathered names are unchanged.
 _ptylist=$(find "$HERE" -name "*.py" -type f ! -path "$HERE/artifacts/*" -print0 2>/dev/null \
            | xargs -0 grep -l "pty.fork" 2>/dev/null | sed "s|^$HERE/||" | LC_ALL=C sort)
@@ -433,9 +441,11 @@
 #  hygienecensus (2026-09-23): THE CLASSIFIER READS PYTHON TOKENS -- regress/census_tokens.py, where a COMMENT, a
 #  STRING or a DOCSTRING is not code.  It was a raw `grep -L "endswith("`, so text naming the method hid a
 #  promptless probe: crime_width_probe.py's only such text was a comment this very round added (pass 2).  The
-#  first repair stripped only FULL-LINE comments and said it "reads code" -- the F2 pass measured seven probes
-#  still hidden by a TRAILING comment, a string or a docstring (the Opus seat).  A token is what Python runs, so
-#  none of those can hide a probe now.  A file that cannot be read or tokenized is listed promptless (it cannot
+#  first repair stripped only FULL-LINE comments and said it "reads code" -- the F2 pass measured seven edits, on
+#  five probe files, where a TRAILING comment, a string or a docstring changed the answer (the Opus seat's n1a-n1d,
+#  n2a, n2b, n9).  A comment, a string or a docstring is never a "." NAME "(" sequence of tokens, so none of
+#  those can hide a probe now; and the classifier keeps STATEMENT boundaries, so a method reference on one line
+#  and a parenthesised string on the next is not a call (the closing pass, codex -- controls_c2/t_nljoin).  A file that cannot be read or tokenized is listed promptless (it cannot
 #  be read, so it is not trusted).  The spelling counts above deliberately stay textual, so a comment or a string
 #  that spells the method is counted -- the safe direction.  They see only the LITERAL `endswith(`: a space before
 #  the paren passes every one of them (hygienecensusholes e9).  `printf '%s\n'`, not `'%s'`: $(...) strips the list's last
```

### tools/derive_hygiene_pins.sh (cbb8488d -> f9533e22)

```diff
--- a/tools/derive_hygiene_pins.sh
+++ b/tools/derive_hygiene_pins.sh
@@ -16,6 +16,9 @@
 #                                                     WHOLE_FULL_FILES
 #    derive_hygiene_pins.sh --grandfather F [F...]    append NAMED new promptless probes to GRANDFATHERED_PROMPTLESS
 #    derive_hygiene_pins.sh --release F [F...]        remove NAMED grandfathered probes that are no longer promptless
+#      Both REFUSE a missing name list, a name given twice, a name holding whitespace or a glob character (the list
+#      is space-separated), and a name that is not eligible (already grandfathered / not a NEW promptless probe;
+#      not a grandfathered name that is no longer promptless).  --release matches names EXACTLY.
 #
 #  --write REFUSES, each with its reason printed, and the refusals are the point of the tool:
 #    * the pty denominator is 0 -- the enumerators saw nothing (wrong tree, moved file);
@@ -26,12 +29,16 @@
 #    * WITHOUT A RULING: EXPECT_CONVERTED would FALL (a #392 guard removed -- or an enumerator narrowed until it sees
 #      nothing), or EXPECT_WHOLE_FULL / WHOLE_FULL_FILES would change AT ALL (#392 measured the whole-buffer form at
 #      0/80; a site added, moved, respelled or converted is a decision, not a recount).
-#  --ruling "YYYY-MM-DD: <who ruled and why>" names that decision; it must look like one, and --write writes it into
-#  the gate as a comment line above every pin it moves, so the change carries its warrant in the diff.
+#  --ruling "YYYY-MM-DD: <who ruled and why>" names that decision; it must look like one -- ONE line, at least 16
+#  non-blank characters of reason, no control character, quote, backslash, `$` or backtick -- and --write writes it
+#  into the gate as a comment line above each pin change that needed it, so that change carries its warrant in the
+#  diff.  (A pin that moves without needing one -- the denominator, a rising #392 count -- gets no note.)
 #  (hygienecensus 2026-09-23, two measured passes: the first version raised EXPECT_UNKNOWN and EXPECT_WHOLE_FULL, never
 #  derived WHOLE_FULL_FILES, re-pinned to zero on an empty population and reported success after its writer failed;
 #  the second let EXPECT_CONVERTED fall silently, re-pinned two censuses to 0 after a one-character enumerator edit,
-#  and took its escape hatch from an environment variable that left no record and accepted "no".)
+#  and took its escape hatch from an environment variable that left no record and accepted "no".  The closing pass
+#  found the ruling's replacement accepting a NEWLINE -- the format check matched one line, and the rest landed in
+#  the gate as live shell (controls_c2/t_rnl) -- and --release matching `foo.py` inside `pref-foo.py`.)
 #
 #  Run it from anywhere; HERE is the regress directory beside this script's tools/ directory ($GXROOT overrides).
 set -u
@@ -53,9 +60,14 @@
     *) echo "usage: $0 [--write [--ruling TEXT] | --grandfather FILE... | --release FILE...]"; exit 2 ;;
 esac
 if [ -n "$RULING" ]; then
+    #  ONE line, checked as a whole: `grep` tests LINES, so a newline let a valid first line carry live shell into
+    #  the gate (the census closing pass, measured).  Any control character is refused, not only newline.
+    case "$RULING" in *[[:cntrl:]]*) echo "REFUSED: the ruling text may not contain a control character (one line only)"; exit 2 ;; esac
     printf '%s' "$RULING" | grep -qE '^[0-9]{4}-[0-9]{2}-[0-9]{2}: .{16,}$' \
         || { echo "REFUSED: a ruling reads \"YYYY-MM-DD: <who ruled and why>\" (16+ characters of reason) -- got [$RULING]"; exit 2; }
     case "$RULING" in *'"'*|*'\'*|*'$'*|*'`'*) echo "REFUSED: the ruling text may not contain quotes, backslashes, \$ or backticks"; exit 2 ;; esac
+    _why=${RULING#*: }; _why=${_why//[[:space:]]/}
+    [ ${#_why} -ge 16 ] || { echo "REFUSED: a ruling needs at least 16 non-blank characters of reason -- got [$RULING]"; exit 2; }
 fi
 
 fn() {  # extract a shell function definition by name: from `name() {` through the first line ending in `}`
@@ -115,11 +127,14 @@
     dup=$(printf '%s\n' "${GF[@]}" | LC_ALL=C sort | uniq -d | tr '\n' ' ')
     [ -z "$dup" ] || { echo "REFUSED: a name given more than once: $dup"; exit 4; }
     for f in "${GF[@]}"; do
+        #  the list is space-separated, and NEWP/GONE are newline-separated: a name holding whitespace cannot be
+        #  recorded, and an unquoted expansion split it and globbed it (codex, the closing pass) -- refuse by name
+        case "$f" in *[[:space:]]*|*'*'*|*'?'*|*'['*) echo "REFUSED: [$f] holds whitespace or a glob character -- rename the probe"; exit 4 ;; esac
         if [ "$MODE" = grandfather ]; then
             printf '%s\n' "$GFS" | grep -qxF -- "$f" && { echo "REFUSED: $f is already grandfathered"; exit 4; }
-            printf '%s\n' $NEWP | grep -qxF -- "$f" || { echo "REFUSED: $f is not a NEW promptless probe"; exit 4; }
+            printf '%s\n' "$NEWP" | grep -qxF -- "$f" || { echo "REFUSED: $f is not a NEW promptless probe"; exit 4; }
         else
-            printf '%s\n' $GONE | grep -qxF -- "$f" || { echo "REFUSED: $f is not a grandfathered name that is no longer promptless"; exit 4; }
+            printf '%s\n' "$GONE" | grep -qxF -- "$f" || { echo "REFUSED: $f is not a grandfathered name that is no longer promptless"; exit 4; }
         fi
     done
     pywrite "$G" "$MODE" "${GF[@]}" <<'PY'
@@ -131,11 +146,13 @@
 if mode == "grandfather":
     body = body + "\n" + " ".join(names)
 else:
+    #  EXACT names, per line: a boundary regex matched `foo.py` inside `pref-foo.py` (codex, the closing pass)
+    lines = [l.split() for l in body.split("\n")]
     for n in names:
-        body, k = re.subn(r"(?<![\w./])%s(?![\w.])" % re.escape(n), "", body)
+        k = sum(l.count(n) for l in lines)
         assert k == 1, (n, k)
-    body = "\n".join(" ".join(l.split()) for l in body.split("\n"))
-    body = "\n".join(l for l in body.split("\n") if l.strip())
+        lines = [[w for w in l if w != n] for l in lines]
+    body = "\n".join(" ".join(l) for l in lines if l)
 io.open(g, "w", encoding="utf-8", newline="").write(s[:i] + body + s[j:])
 print("%s: %s" % ("GRANDFATHERED" if mode == "grandfather" else "RELEASED", " ".join(names)))
 PY
```

## §E -- QUESTIONS (answer each, numbered; from the packet alone, do Q1 and Q3 first)

**Q1 -- does the F3 repair do what it claims?**  (a) With NEWLINE kept: is any legitimate one-statement readiness call
now LOST -- a call split across lines inside brackets, after a backslash continuation, or inside a lambda or a
comprehension?  ENUMERATE the token sequences.  (b) With a `.` required before the name: is any legitimate readiness
call lost (an unbound `str.<method>(buf, ...)`, a `getattr` form) -- and does that fail CLOSED (the probe becomes
promptless and the names row reds) or open?  (c) The ruling checks: is there still a way to put a non-comment line into
the gate, or to move a ruling-gated pin with a blank or malformed warrant?  (d) The name checks and the exact release:
any name the list can hold that the checks now wrongly refuse, or any name they wrongly accept?
**Q2 -- the smallest edit that passes every readiness row and is not one of the filed shapes** (the nine spellings, the
three population omissions, e9, the semantic transforms of §C.2).  Name the edit and the rows that stay green; if none,
give your denominator.
**Q3 -- adjudicate H1-H17 and D1**: UPHOLD / OVERTURN / REFINE / CANNOT SETTLE, one line each with a reason.  Then:
**WHICH OF MY ACCEPTED DISPOSITIONS IS WRONG?**  In particular H10 (e9 filed) and H8 (rejected by measurement).
**Q4 -- records**: is any sentence in the changed comments false as of today?
**Q5 -- option-set completeness**: for H10 and H13, is there a disposition I did not name?

If, while verifying a claim, you found something ELSE -- say so.

End with a seat record: model, what you read, what you ran.
