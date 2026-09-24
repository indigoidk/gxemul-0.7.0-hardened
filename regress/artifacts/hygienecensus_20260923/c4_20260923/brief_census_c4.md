# hygienecensus -- the F4 repair's own pass: do the deriver's new input checks refuse exactly what they say, and which of my dispositions of the F3 pass's findings is wrong?

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly.  **Check the premises,
not just the derivations.**  A seat that re-derives a premise from something this brief did NOT give it is worth more
than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/`** -- `regress/census_tokens.py`, `regress/gate_hygiene.sh`,
`tools/derive_hygiene_pins.sh`.  File-reading seats: read the FROZEN copies in
`C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\census0923\c4_frozen\` (md5 prefixes: census_tokens.py 8b4e8468,
gate_hygiene.sh c1399897, derive_hygiene_pins.sh 23410fe1); the versions the F3 pass reviewed are in `c3_frozen\`
(029fba36, 4220b6ee, f9533e22).  There are pristine-2021-upstream copies of GXemul under the project root (`./src/`,
`_archive/`); they are NOT this fork.

**If you cannot read files that is expected** -- the diff and the measurements are inlined below.  Name any premise
you cannot settle from this packet rather than guessing.  **ENUMERATE** any count or set rather than reasoning about it.
**VERDICT LINE FIRST**: `VERDICT: SHIP` or `VERDICT: DO NOT SHIP -- <reason>`.  **A zero needs a denominator**: if you
find nothing, say which inputs you tried against which checks.

## Where the census round stands

Gate 6's readiness census counts, over the probes that drive the emulator through a pseudo-terminal, which spellings
of a prompt-readiness test they use and which probes have none; its pins are written only by
`tools/derive_hygiene_pins.sh` (owner rulings of 2026-09-23: "re-pin, count all"; grandfather by name; one bulk
re-derivation, never by hand).  Pass 2 -> F2 (a Python-TOKEN classifier; a dated `--ruling`) -> the closing pass -> F3
(statement boundaries kept; a "." required before the method name; control characters refused in a ruling; the name
lists quoted; exact release) -> **the F3 pass (panel `panel_20260923_180958`, a dedicated codex job, the Opus
measuring seat) -> THIS, F4.**

## The F4 repair -- what changed (the full diff is inlined below)

1. **`--ruling`**: every byte must be printable ASCII (0x20-0x7e, counted with `LC_ALL=C tr`), so no newline, tab,
   non-breaking space, U+0085 or U+2028 gets through; the date must be a REAL calendar date (`date -d` must print it
   back unchanged); the reason must hold at least 16 ASCII letters or digits (not merely 16 non-blank characters); a
   double quote, backslash, `$` or backtick is still refused.  The header now says these check the FORM of a warrant,
   not who gave it, and names "double quote" rather than "quote".
2. **`--grandfather` / `--release` names**: an ALLOW-LIST, byte by byte -- non-empty, and nothing but ASCII letters,
   digits, `.`, `_`, `-`, `/` (the list is space-separated and written into a double-quoted shell string).  The old
   deny-list refused whitespace and `* ? [` and let `$`, a backtick, a quote, a backslash and an EMPTY name through.
3. **Comments**: `gate_hygiene.sh`'s helper sentence (it called a helper's `endswith(` line "unknown", which is false
   when the helper uses a known literal); `census_tokens.py`'s pointer to "the docstring's third paragraph" (now named
   by content) and its "a call is a METHOD call" sentence (a `match` class pattern of that shape is also credited; an
   alias call with no "." is not).  **The gate's rows and the classifier's code are unchanged.**

## Measured (on `/tmp` copies; predictions first; `regress/artifacts/hygienecensus_20260923/controls_c4/`)

Predictions 18:37:10, run 18:37-18:39 (`PREDICTIONS.txt`, `SUMMARY.txt`, `TABLE.txt`; `PREDICTIONS.corrections`):
* `real` PASS; the deriver's report equals every pin; `--write` leaves the gate byte-identical.
* **The 45 F2 edits and the seven closing-pass cases: verdicts IDENTICAL to the F3 run** (`diff` of the two tables:
  empty) -- 14 of the 45 pass: the 13 filed false passes and `n9` (a correct pass).
* Rulings on a tree where a whole-buffer site moved (so `--write` needs one): newline, tab, 21 spaces + `x`,
  `2026-99-99: ...`, `2026-02-30: ...`, 16 dots, 8 non-breaking spaces, U+0085, U+2028 -- **all nine REFUSED (rc 2),
  the gate byte-identical after them**; `2026-09-23: owner's ruling for this control case only` (an apostrophe) --
  **WRITTEN**: two comment lines, one above each ruling-gated pin that moved, `bash -n` clean (`t_rapos.diff`).
* Names: `zz opus.py`, `''`, `zz$HOME.py`, `zz<NBSP>x.py`, `zz[1].py` -- **all REFUSED (rc 4), the list unchanged**
  (the gate reds on each such new promptless probe either way); `zz-legit_probe.py` -- GRANDFATHERED, and the gate's
  names and grandfathered-count rows go green (its pty denominator still reds until `--write` re-derives it -- my
  prediction said "green" and was wrong; corrected in `PREDICTIONS.corrections`); `--release gdrom_cond_probe.py` with
  `x-gdrom_cond_probe.py` grandfathered -- exactly that one name removed (exact list read, `t_relpref_exact.txt`:
  43 -> 44 -> 43).
* **Owed**: gate 6 on the final files, in the next quiet slot.

## §C — SETTLED PREMISES (recorded resolutions; say if the diff contradicts one)

1. The owner's rulings govern; the pins are written by the deriver, never by hand.
2. **The census is a SPELLING census**: it guarantees which spellings of a readiness test exist, not that a probe's
   readiness logic is right.  A semantic change that keeps the spelling (`~`, `not`, a comparison) is outside it, as
   is a probe with a real readiness wait written without the method.
3. **The stopping rule**: in-round only a measured false pass or a wrong record in THIS round's material; pre-existing
   holes are FILED.  The deriver is new in this round, so ALL of it is this round's material.
4. The recogniser `full` needs `)` immediately after the quote, so an unrecognised spelling reds `unknown`.
5. The textual closed-world counts are LINE-based; the token classifier (`census_tokens.py`) is not a parser.

## The F4 diff (INLINED IN FULL, unified, two lines of context)

`regress/census_tokens.py` (029fba36 -> 8b4e8468):

```diff
--- c3_frozen/census_tokens.py	2026-09-23 18:04:57.786730600 -0500
+++ c4_frozen/census_tokens.py	2026-09-23 18:40:42.899255500 -0500
@@ -13,7 +13,9 @@
 REFERENCE on one statement and a parenthesised string on the next -- `x = buf.rstrip().endswith` / `("GXemul>")` --
 read as one whole-buffer call, and a probe whose readiness test had been turned into that passed every row (measured by
-the census closing pass, controls_c2/t_nljoin).  NL, the newline INSIDE brackets, is still layout.  And a call is a
-METHOD call: the name must follow a "." -- a function DEFINITION under that name calls nothing, and the first version
-credited one (codex, the same pass).
+the census closing pass, controls_c2/t_nljoin).  NL, the newline INSIDE brackets, is still layout.  And a call is
+counted only where the name follows a "." -- a function DEFINITION under that name calls nothing, and the first
+version credited one (codex, the same pass).  Tokens are not a parse: a class PATTERN of the same shape in a `match`
+statement (`case K.<name>(...)`) is still counted, and a call through an alias with no "." before the name is not
+(the F3 pass, codex; the second fails closed -- the probe is listed promptless).
 
 The CLOSED-WORLD counts (a bare prompt-suffix test, an unrecognised spelling of the ends-with call) are NOT done here
@@ -41,5 +43,5 @@
 import ast, io, os, sys, tokenize
 
-ENDS_WITH = "ends" + "with"          # spelled in two halves: see the docstring's third paragraph
+ENDS_WITH = "ends" + "with"          # spelled in two halves: see the docstring's CLOSED-WORLD paragraph
 SKIP = (tokenize.NL, tokenize.INDENT, tokenize.DEDENT, tokenize.COMMENT, tokenize.ENCODING)   # NEWLINE is KEPT
 
```

`regress/gate_hygiene.sh` (4220b6ee -> c1399897):

```diff
--- c3_frozen/gate_hygiene.sh	2026-09-23 18:04:49.753137400 -0500
+++ c4_frozen/gate_hygiene.sh	2026-09-23 18:40:42.900253700 -0500
@@ -71,10 +71,14 @@
 #    - accept either quote style;
 #    - and make the check CLOSED-WORLD: every .endswith() in the tree must use
-#      one of the two KNOWN literals.  A third spelling -- including
-#      endswith(PROMPT), or a helper's own endswith( line when the helper is
-#      a .py file under regress/ -- is unknown, and unknown fails.  (A helper
-#      module that forks no pty is still COUNTED here, but a probe that calls
-#      it has no readiness spelling of its own to census -- hygienecensusholes
-#      n3k.)  That converts "I grepped for the bad thing" into "I
+#      one of the two KNOWN literals.  A third spelling -- endswith(PROMPT),
+#      say -- is unknown, and unknown fails.  A helper module under regress/
+#      is scanned like a probe: its endswith( line counts as known when it
+#      uses a known literal, and fails when it does not.  What no count here
+#      sees is WHICH probe a helper's test serves: a probe whose ONLY test
+#      moved into a helper is listed promptless and the names row reds
+#      (fail-closed), while a probe that keeps one call of its own can move
+#      the rest into a helper with every row green (hygienecensusholes n3k,
+#      n3k2; this said a helper's line was unknown until the census F3 pass,
+#      codex and grok).  That converts "I grepped for the bad thing" into "I
 #      enumerated everything and recognised all of it", which is the only form
 #      that cannot be evaded by inventing a new way to write it.
```

`tools/derive_hygiene_pins.sh` (f9533e22 -> 23410fe1):

```diff
--- c3_frozen/derive_hygiene_pins.sh	2026-09-23 18:04:49.754137700 -0500
+++ c4_frozen/derive_hygiene_pins.sh	2026-09-23 18:40:42.901165100 -0500
@@ -17,7 +17,9 @@
 #    derive_hygiene_pins.sh --grandfather F [F...]    append NAMED new promptless probes to GRANDFATHERED_PROMPTLESS
 #    derive_hygiene_pins.sh --release F [F...]        remove NAMED grandfathered probes that are no longer promptless
-#      Both REFUSE a missing name list, a name given twice, a name holding whitespace or a glob character (the list
-#      is space-separated), and a name that is not eligible (already grandfathered / not a NEW promptless probe;
-#      not a grandfathered name that is no longer promptless).  --release matches names EXACTLY.
+#      Both REFUSE a missing name list, a name given twice, a name that is empty or holds any byte but ASCII
+#      letters, digits, '.', '_', '-' and '/' (the list is space-separated and written into a double-quoted shell
+#      string, so blanks, glob characters, `$`, backticks, quotes and backslashes are all refused -- rename the
+#      probe), and a name that is not eligible (already grandfathered / not a NEW promptless probe; not a
+#      grandfathered name that is no longer promptless).  --release matches names EXACTLY.
 #
 #  --write REFUSES, each with its reason printed, and the refusals are the point of the tool:
@@ -30,6 +32,7 @@
 #      nothing), or EXPECT_WHOLE_FULL / WHOLE_FULL_FILES would change AT ALL (#392 measured the whole-buffer form at
 #      0/80; a site added, moved, respelled or converted is a decision, not a recount).
-#  --ruling "YYYY-MM-DD: <who ruled and why>" names that decision; it must look like one -- ONE line, at least 16
-#  non-blank characters of reason, no control character, quote, backslash, `$` or backtick -- and --write writes it
+#  --ruling "YYYY-MM-DD: <who ruled and why>" names that decision; it must look like one -- printable ASCII only (so
+#  ONE line), a real calendar date, at least 16 letters or digits of reason, no double quote, backslash, `$` or
+#  backtick; these check the FORM of a warrant, not who gave it -- and --write writes it
 #  into the gate as a comment line above each pin change that needed it, so that change carries its warrant in the
 #  diff.  (A pin that moves without needing one -- the denominator, a rising #392 count -- gets no note.)
@@ -39,5 +42,8 @@
 #  and took its escape hatch from an environment variable that left no record and accepted "no".  The closing pass
 #  found the ruling's replacement accepting a NEWLINE -- the format check matched one line, and the rest landed in
-#  the gate as live shell (controls_c2/t_rnl) -- and --release matching `foo.py` inside `pref-foo.py`.)
+#  the gate as live shell (controls_c2/t_rnl) -- and --release matching `foo.py` inside `pref-foo.py`.  That
+#  repair's own pass found an impossible date, a punctuation-only reason and non-ASCII blanks or separators accepted
+#  in a ruling (each landed inside the comment line; none reached a pin), and a name holding `$`, a backtick, a
+#  quote or a backslash -- or no name at all -- written into the double-quoted list.)
 #
 #  Run it from anywhere; HERE is the regress directory beside this script's tools/ directory ($GXROOT overrides).
@@ -61,12 +67,16 @@
 esac
 if [ -n "$RULING" ]; then
-    #  ONE line, checked as a whole: `grep` tests LINES, so a newline let a valid first line carry live shell into
-    #  the gate (the census closing pass, measured).  Any control character is refused, not only newline.
-    case "$RULING" in *[[:cntrl:]]*) echo "REFUSED: the ruling text may not contain a control character (one line only)"; exit 2 ;; esac
+    #  PRINTABLE ASCII ONLY, byte by byte: `grep` tests LINES, so a newline let a valid first line carry live shell
+    #  into the gate (the census closing pass, measured), and a [[:cntrl:]] test then let through what the locale does
+    #  not call a control -- a non-breaking space, U+0085, U+2028 (the F3 pass; each stayed inside the comment line).
+    [ $(( $(printf '%s' "$RULING" | LC_ALL=C tr -d ' -~' | wc -c) )) -eq 0 ] \
+        || { echo "REFUSED: the ruling text must be printable ASCII, on one line"; exit 2; }
     printf '%s' "$RULING" | grep -qE '^[0-9]{4}-[0-9]{2}-[0-9]{2}: .{16,}$' \
         || { echo "REFUSED: a ruling reads \"YYYY-MM-DD: <who ruled and why>\" (16+ characters of reason) -- got [$RULING]"; exit 2; }
-    case "$RULING" in *'"'*|*'\'*|*'$'*|*'`'*) echo "REFUSED: the ruling text may not contain quotes, backslashes, \$ or backticks"; exit 2 ;; esac
-    _why=${RULING#*: }; _why=${_why//[[:space:]]/}
-    [ ${#_why} -ge 16 ] || { echo "REFUSED: a ruling needs at least 16 non-blank characters of reason -- got [$RULING]"; exit 2; }
+    _day=${RULING%%:*}
+    [ "$(date -d "$_day" +%F 2>/dev/null)" = "$_day" ] || { echo "REFUSED: [$_day] is not a calendar date"; exit 2; }
+    case "$RULING" in *'"'*|*'\'*|*'$'*|*'`'*) echo "REFUSED: the ruling text may not contain a double quote, a backslash, \$ or a backtick"; exit 2 ;; esac
+    _why=$(printf '%s' "${RULING#*: }" | LC_ALL=C tr -cd 'A-Za-z0-9')
+    [ ${#_why} -ge 16 ] || { echo "REFUSED: a ruling needs at least 16 letters or digits of reason -- got [$RULING]"; exit 2; }
 fi
 
@@ -128,7 +138,9 @@
     [ -z "$dup" ] || { echo "REFUSED: a name given more than once: $dup"; exit 4; }
     for f in "${GF[@]}"; do
-        #  the list is space-separated, and NEWP/GONE are newline-separated: a name holding whitespace cannot be
-        #  recorded, and an unquoted expansion split it and globbed it (codex, the closing pass) -- refuse by name
-        case "$f" in *[[:space:]]*|*'*'*|*'?'*|*'['*) echo "REFUSED: [$f] holds whitespace or a glob character -- rename the probe"; exit 4 ;; esac
+        #  the list is space-separated and written into a double-quoted shell string: a name with a blank cannot be
+        #  recorded (codex, the closing pass), `$`, a backtick, a quote or a backslash is live shell there, and an EMPTY
+        #  name matched the blank line an empty NEWP prints (the F3 pass).  So an allow-list, byte by byte:
+        [ -n "$f" ] && [ -z "$(printf '%s' "$f" | LC_ALL=C tr -d 'A-Za-z0-9._/-')" ] \
+            || { echo "REFUSED: [$f] -- a probe name here is ASCII letters, digits, '.', '_', '-' and '/' only; rename the probe"; exit 4; }
         if [ "$MODE" = grandfather ]; then
             printf '%s\n' "$GFS" | grep -qxF -- "$f" && { echo "REFUSED: $f is already grandfathered"; exit 4; }
```

## §F2 — the F3 pass's findings, with MY disposition of each

*(Self-review disclosed: I wrote F1-F4 and these dispositions.  Seats whose finding I adopted: check the CHANGE answers
it.  The F3 pass's verdicts: codex, grok DO NOT SHIP; agy, glm, deepseek, minimax, the kimi substitute SHIP; the kimi
CLI walled; the Opus seat SHIP -- its measurements were run by claude-opus-4-8 after two refusals by claude-opus-5-5,
and its verdict was re-asked and answered by claude-opus-5-5, from those logs.)*

**K1 -- a name holding `$`, a backtick, a quote or a backslash was accepted and written unescaped into the double-quoted
list; an EMPTY name was accepted when no new probe existed** (codex, codex-dedicated, grok, the kimi substitute,
deepseek).  **ACCEPTED -> the allow-list** (t_ndollar, t_nempty refused).
**K2 -- the old check wrongly refused `*`, `?`, `[`, which the quoted list can hold** (grok, glm, codex-dedicated).
**KEPT AS A DELIBERATE RESTRICTION**: the allow-list refuses them too, and says "rename the probe" (t_nbrack refused).
**K3 -- an impossible date passed** (`2026-99-99`: codex, codex-dedicated, glm).  **ACCEPTED -> `date -d` round trip**
(t_rdate, t_rfeb30 refused).
**K4 -- a reason of 16 dots, or of 8 non-breaking spaces, passed** (the Opus seat, codex-dedicated, grok).  **ACCEPTED
-> 16 ASCII letters or digits, and printable ASCII only** (t_rpunct, t_rnbsp refused).
**K5 -- U+0085, U+2028, U+2029 passed the control check; "no control character" was false for C1 controls** (the Opus
seat, measured non-injecting).  **ACCEPTED -> printable ASCII only** (t_rnel, t_r2028 refused).
**K6 -- the header said "no ... quote"; only a DOUBLE quote is refused, and an apostrophe is inert in the comment
line** (codex, grok, glm).  **ACCEPTED -> "double quote"** (t_rapos written, `bash -n` clean).
**K7 -- the gate's helper sentence was false** (codex, grok: `n3k`'s helper uses the known literal, so its line is
counted as known, not unknown).  **ACCEPTED -> rewritten**: a helper is scanned like a probe; what no count sees is
which probe a helper serves -- a probe whose ONLY test moved into a helper is listed promptless (fail-closed), one that
keeps a call of its own can move the rest with every row green (n3k, n3k2).
**K8 -- `census_tokens.py`'s "third paragraph" pointer went stale when a paragraph was added** (codex).  **ACCEPTED ->
named by content.**
**K9 -- "13 still pass" was false: 14 pass** (codex: the 13 filed + `n9`, which passes correctly).  **ACCEPTED** (records).
**K10 -- H8's label: the comma / `[:]` / `+""` forms DO miss the whole-buffer rows; the unknown row is what catches
them** (glm).  **ACCEPTED as wording** for the records.
**K11 -- e9's reach: "one regex family" under-states it -- the textual counts are LINE-based, so a backslash
continuation or a newline inside the parentheses removes a call from them too** (glm, agy, the kimi substitute).
**ACCEPTED**: e9 is re-filed as the LINE-BASED class (spacing, backslash continuation, a newline inside the call).
**K12 -- new Q2 shapes** -- codex: a bare-prompt call inside an f-string replacement field on a `#`-leading physical
line of a triple-quoted f-string escapes `py_code`'s comment filter; grok: `buf[:].rstrip().endswith(...)` escapes the
whole-buffer token SHAPE; the kimi substitute: a receiver whose name does not end in `buf`; the Opus seat: a spaced dot.
**FILED** (pre-existing): the f-string one as `e10`; the others with `n3b` as the whole-shape SPELLING class and with
e9 as the line-based class.
**K13 -- a call through an alias (`(lambda endswith: endswith("GXemul>"))(buf.endswith)`, or a two-statement alias)
is no longer counted** (codex-dedicated).  **DISCLOSED**, fail-closed (the probe is listed promptless; the names row
reds).  The docstring now says so.
**K14 -- a `match` class pattern `case K.endswith("GXemul>"):` is credited as a call** (codex-dedicated).
**DISCLOSED** (tokens are not a parse); the docstring's "a call is a METHOD call" was an over-claim and now says so.
**K15 -- the `readiness_predicate_test.py` exclusion matches the basename anywhere below regress/, while its content
pin reads only the top-level file** (codex-dedicated; `gate_hygiene.sh`'s "FAIL-CLOSED exception" sentence).
**FILED** (pre-existing text and code).
**K16 -- can a classifier or interpreter failure become an empty, passing census?** (codex-dedicated's question).
**REASONED, NOT MEASURED**: if the classifier yields nothing, the promptless list is empty and the whole-buffer count 0
-- the gate reds (43 and 3 pinned) and the deriver refuses (every grandfathered name is then GONE; the whole-buffer
pins would need a ruling).  A seat that can measure it: please do.
**K17 -- the truth-table content pin strips only full-line comments** (grok: delete the real arms, leave the method in
a trailing comment, the pin holds).  **FILED** with H13, and H13 is split: its three stale literals are a records
item, this is a detector weakness.
**K18 -- the release writer's `k == 1` counts words in comment lines of the extracted body** (glm).  **REJECTED**: the
body is the double-quoted string's CONTENT, which holds no comment lines (the writer reads between the quotes).

**D2 -- DO NOT SHIP (codex, grok: the records K7 and K9 were false) vs SHIP (the rest).**  Settled by reading the
artifacts: K7 is false against `n3k.g.rows` and K9 against `controls_c3/TABLE.txt`; both corrected in F4.

**WHERE I MIGHT BE FOOLING MYSELF**: three repairs of the deriver's input checks in one round, each after a seat found
an input the previous one let through.  F4 replaces deny-lists with allow-lists, which is the class closure -- but I
enumerated the inputs, and the previous two enumerations were incomplete.

## §E -- QUESTIONS (answer each, numbered; from the packet alone, do Q1 and Q3 first)

**Q1 -- do the new checks do what they claim?**  (a) The ruling: is there an input the checks accept that the header
says is refused, or one they refuse that a real ruling would need (a legitimate date, name or reason)?  Consider the
locale the deriver runs under, `date -d` on both git-bash and WSL, and what `tr -d ' -~'` and `tr -cd 'A-Za-z0-9'` do
with multi-byte input.  (b) The names: is there a name the allow-list accepts that is unsafe in the double-quoted list
or breaks `--release`, or a real probe name it refuses?  ENUMERATE the bytes you tried.
**Q2 -- the smallest input or edit that gets past the F4 checks and does harm** -- a ruling that lands anything but one
comment line, a pin moved without a warrant, a name that changes meaning in the gate -- or, for the census itself, an
edit that passes every readiness row and is NOT one of the filed shapes.  If none, give your denominator.
**Q3 -- adjudicate K1-K18 and D2**: UPHOLD / OVERTURN / REFINE / CANNOT SETTLE, one line each with a reason.  Then:
**WHICH OF MY ACCEPTED DISPOSITIONS IS WRONG?**  In particular K2 (refusing names the list could hold), K16
(reasoned, not measured) and K18 (rejected).
**Q4 -- records**: is any sentence in the changed comments or the deriver's header false as of today?
**Q5 -- option-set completeness**: for K2 and K12, is there a disposition I did not name?

If, while verifying a claim, you found something ELSE -- say so.

End with a seat record: model, what you read, what you ran.
