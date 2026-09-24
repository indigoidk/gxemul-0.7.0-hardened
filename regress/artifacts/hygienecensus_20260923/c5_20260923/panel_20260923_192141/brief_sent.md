# hygienecensus -- the F5 repair's own pass: do the deriver's input checks now refuse exactly what they say, and which of my dispositions of the F4 pass's findings is wrong?

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly.  **Check the premises,
not just the derivations.**  A seat that re-derives a premise from something this brief did NOT give it is worth more
than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/`** -- `regress/census_tokens.py`, `regress/gate_hygiene.sh`,
`tools/derive_hygiene_pins.sh`.  File-reading seats: read the FROZEN copies in
`C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\census0923\c5_frozen\` (census_tokens.py 98788b1b, gate_hygiene.sh 9d88b3f6,
derive_hygiene_pins.sh e1ce9c59); the F4 versions are in `c4_frozen\` (8b4e8468, c1399897, 23410fe1).  There are
pristine-2021-upstream copies of GXemul under the project root (`./src/`, `_archive/`); they are NOT this fork.

**If you cannot read files that is expected** -- the diff and the measurements are inlined below.  Name any premise
you cannot settle from this packet rather than guessing.  **ENUMERATE** any count or set rather than reasoning about it.
**VERDICT LINE FIRST**: `VERDICT: SHIP` or `VERDICT: DO NOT SHIP -- <reason>`.  **A zero needs a denominator**.

## Where the census round stands

Gate 6's readiness census counts, over the probes that drive the emulator through a pseudo-terminal, which spellings
of a prompt-readiness test they use and which probes have none; its pins are written only by
`tools/derive_hygiene_pins.sh` (owner rulings of 2026-09-23).  F2 -> F3 -> F4 -> **the F4 pass (panel
`panel_20260923_184642`, a dedicated codex job, the Opus measuring seat) -> THIS, F5.**  The gate's ROWS and the token
classifier's CODE are unchanged since F3; F4 and F5 changed only the deriver's input checks and comments.

## The F5 repair -- what changed (the full diff is inlined below)

1. **Names**: the allow-list is now COUNTED with `wc -c`.  F4 tested `$(...)` for emptiness, and command substitution
   strips trailing newlines, so a name holding a LINE FEED passed (measured: one argument grandfathered two names, one
   of them no file).
2. **`--ruling`**: an explicitly EMPTY ruling is refused; the date is parsed in UTC (`date -u -d`), because a local
   calendar can skip a midnight and GNU date then refuses a real day (measured under `TZ=America/Sao_Paulo`).
3. **The deriver runs the gate's census lines with the interpreter it found** (`python3` becomes a shell function
   calling it when `python3` itself does not run) and **proves the token classifier runs before trusting it**: a
   canary path that does not exist must come back listed.  Under git-bash `python3` is the Windows Store stub: the
   classifier printed nothing, all 43 grandfathered names read as GONE, and `--release` accepted a probe that is still
   promptless (the Opus seat, measured).
4. **The list writer anchors its search at line start** (`(?m)^GRANDFATHERED_PROMPTLESS="`, exactly one match), as the
   reader does: an unanchored search wrote into a COMMENT quoting the assignment and left a gate that no longer parses.
5. **`WHOLE_FULL_FILES`** -- the other double-quoted string the deriver writes FILE NAMES into -- gets the same byte
   allow-list (plus `:` and space for "name:count name:count"); it had none (grok).
6. **Comments**: the header's reason for refusing glob characters (they are inert inside double quotes; they expand in
   the gate's and the report's UNQUOTED printed lists); "a double quote", not "a quote"; the gate's helper sentence and
   its "cannot be evaded" / "closed-world" sentences (now: closed-world over the literal spellings on the PHYSICAL
   lines the comment filter keeps); the classifier docstring (a `match` class pattern fails OPEN; an alias call fails
   closed only if no other call is counted).

## Measured (on `/tmp` copies; predictions first)

`regress/artifacts/hygienecensus_20260923/controls_c5/` (predictions 18:57:02) and `controls_c5b/` (19:12:59):
* The whole earlier suite -- `real`, the 45 F2 edits, the seven closing-pass cases, every c4 ruling and name case --
  gives verdicts **IDENTICAL** to F4's, on F5 and again on F5b (`diff` of the tables: empty).
* `t_nlf` (`zz-a.py<LF>zz-ghost.py`): REFUSED rc 4, list unchanged (F4: GRANDFATHERED both).  `t_rempty` (`--ruling
  ""`): REFUSED rc 2.  `t_rtz` (2018-11-04 under `TZ=America/Sao_Paulo`, where local `date -d` says "invalid date"):
  WRITTEN, `bash -n` clean.  `t_bsl` (a bare-prompt call split by a backslash continuation between the name and the
  paren): PASSES every row -- the LINE-based class the gate comment now names.
* On F5b vs F5a: `t_canary` (census_tokens.py deleted): DERIVE_FAIL rc 3 vs a report listing every name as GONE;
  `t_anchor` (a comment quoting the assignment above it): the REAL list 43 -> 44, `bash -n` clean vs written into the
  comment and `bash -n` FAILED; `t_wholefile` (a pty probe named `zz$HOME.py` with two whole-buffer sites): REFUSED
  rc 5, gate unchanged vs WRITTEN with `zz$HOME.py:2` inside `WHOLE_FULL_FILES="..."`.
* **git-bash** (`python3` = the Store stub, rc 49): F5b's report equals every pin, no NEW or GONE names; F5a's
  listed all 43 grandfathered names as GONE and read EXPECT_WHOLE_FULL 0.
* After those runs the deriver changed once more, COMMENT-ONLY (45cc3934 -> e1ce9c59: "a double quote" twice).
* A seat's claim that `${RULING%%:*}` cuts at the LAST colon was measured false: it yields `2026-09-23` for a reason
  holding `14:00` and `ABC:123` (`%%` removes the longest suffix matching `:*`, from the FIRST colon).
* **Owed**: gate 6 on the final files, in the next quiet slot.

## §C — SETTLED PREMISES (recorded resolutions; say if the diff contradicts one)

1. The owner's rulings govern; the pins are written by the deriver, never by hand.
2. **The census is a SPELLING census**: it guarantees which spellings of a readiness test exist, not that a probe's
   readiness logic is right.
3. **The stopping rule**: in-round only a measured false pass or a wrong record in THIS round's material; pre-existing
   holes are FILED.  The deriver is new in this round, so all of it is this round's material.
4. The textual closed-world counts are LINE-based and drop every physical line beginning with `#`; the token
   classifier (`census_tokens.py`) is not a parser.

## The F5 diff (INLINED IN FULL, unified, two lines of context)

`regress/census_tokens.py` (8b4e8468 -> 98788b1b):

```diff
--- c4_frozen/census_tokens.py	2026-09-23 18:40:42.899255500 -0500
+++ c5_frozen/census_tokens.py	2026-09-23 19:20:32.662757200 -0500
@@ -17,5 +17,7 @@
 version credited one (codex, the same pass).  Tokens are not a parse: a class PATTERN of the same shape in a `match`
 statement (`case K.<name>(...)`) is still counted, and a call through an alias with no "." before the name is not
-(the F3 pass, codex; the second fails closed -- the probe is listed promptless).
+(the F3 pass, codex).  The second fails closed -- the probe is listed promptless, if no other call of it is counted.
+The first fails OPEN: a grandfathered probe that gains such a pattern reads as no longer promptless, and --release
+then takes it off the list with every row green (measured, the census F4 pass, the Opus seat; filed).
 
 The CLOSED-WORLD counts (a bare prompt-suffix test, an unrecognised spelling of the ends-with call) are NOT done here
```

`regress/gate_hygiene.sh` (c1399897 -> 9d88b3f6):

```diff
--- c4_frozen/gate_hygiene.sh	2026-09-23 18:40:42.900253700 -0500
+++ c5_frozen/gate_hygiene.sh	2026-09-23 19:20:32.665283500 -0500
@@ -73,6 +73,7 @@
 #      one of the two KNOWN literals.  A third spelling -- endswith(PROMPT),
 #      say -- is unknown, and unknown fails.  A helper module under regress/
-#      is scanned like a probe: its endswith( line counts as known when it
-#      uses a known literal, and fails when it does not.  What no count here
+#      is scanned like a probe: an endswith( line there with a known literal
+#      is not "unknown" (the bare one still fails the bare row), and one with
+#      an unrecognised argument fails "unknown".  What no count here
 #      sees is WHICH probe a helper's test serves: a probe whose ONLY test
 #      moved into a helper is listed promptless and the names row reds
@@ -81,11 +82,21 @@
 #      n3k2; this said a helper's line was unknown until the census F3 pass,
 #      codex and grok).  That converts "I grepped for the bad thing" into "I
-#      enumerated everything and recognised all of it", which is the only form
-#      that cannot be evaded by inventing a new way to write it.
-#      (*** 2026-09-23: "cannot be evaded" is FALSE for one spelling -- a space
-#      before the paren, `endswith (">")`, passes every count here, because all
-#      of them key on the literal `endswith(`.  Measured on a copy; filed as
-#      hygienecensusholes e9, ranked first.  The census is closed-world over the
-#      literal spellings, not over the method. ***)
+#      enumerated everything and recognised all of it" -- for the spellings
+#      these counts can SEE.
+#      (*** 2026-09-23: this said it was "the only form that cannot be evaded
+#      by inventing a new way to write it".  FALSE: every count here is LINE-
+#      based and keys on the literal `endswith(`, so a space before the paren
+#      (`endswith (">")`) or a backslash continuation between the name and
+#      the paren removes a call from all of them (both measured on copies,
+#      controls_f2 e_e9 and controls_c5 t_bsl).  Filed as hygienecensusholes
+#      e9, ranked first; the census F3 pass widened it from one spelling to
+#      this LINE-based class (glm, agy, the kimi substitute).  And the
+#      comment filter drops every PHYSICAL line that begins with `#`: code on
+#      such a line (after a closing triple quote, or in an f-string field) and
+#      a whole file saved with CR-only line endings (grep then sees one line,
+#      beginning `#!`) escape too -- measured, the census F4 pass (the Opus
+#      seat: hash_line, cr_only), filed with e10.  The census is closed-world
+#      over the literal spellings on the physical lines it keeps, not over
+#      the method. ***)
 EXPECT_BARE=0
 EXPECT_UNKNOWN=0
```

`tools/derive_hygiene_pins.sh` (23410fe1 -> e1ce9c59):

```diff
--- c4_frozen/derive_hygiene_pins.sh	2026-09-23 18:40:42.901165100 -0500
+++ c5_frozen/derive_hygiene_pins.sh	2026-09-23 19:20:32.668793500 -0500
@@ -18,7 +18,8 @@
 #    derive_hygiene_pins.sh --release F [F...]        remove NAMED grandfathered probes that are no longer promptless
 #      Both REFUSE a missing name list, a name given twice, a name that is empty or holds any byte but ASCII
-#      letters, digits, '.', '_', '-' and '/' (the list is space-separated and written into a double-quoted shell
-#      string, so blanks, glob characters, `$`, backticks, quotes and backslashes are all refused -- rename the
-#      probe), and a name that is not eligible (already grandfathered / not a NEW promptless probe; not a
+#      letters, digits, '.', '_', '-' and '/' (the list is space-separated, it is written into a double-quoted shell
+#      string where `$`, a backtick, a double quote or a backslash is live, and the gate's and this tool's printed name
+#      lists expand it UNQUOTED, where a glob character would -- so all of those are refused: rename the probe),
+#      and a name that is not eligible (already grandfathered / not a NEW promptless probe; not a
 #      grandfathered name that is no longer promptless).  --release matches names EXACTLY.
 #
@@ -26,4 +27,6 @@
 #    * the pty denominator is 0 -- the enumerators saw nothing (wrong tree, moved file);
 #    * the three #392 counts (anchor, echo, fresh mark) disagree -- one pin, and a disagreement IS a defect;
+#    * a whole-buffer FILE NAME holds a byte outside the names' allow-list below -- WHOLE_FULL_FILES is the other
+#      double-quoted string this tool writes names into;
 #    * a promptless probe is neither grandfathered nor given prompt detection, or a grandfathered probe is no longer
 #      promptless -- the gate grades the NAMES, so --grandfather / --release first;
@@ -32,7 +35,8 @@
 #      nothing), or EXPECT_WHOLE_FULL / WHOLE_FULL_FILES would change AT ALL (#392 measured the whole-buffer form at
 #      0/80; a site added, moved, respelled or converted is a decision, not a recount).
-#  --ruling "YYYY-MM-DD: <who ruled and why>" names that decision; it must look like one -- printable ASCII only (so
-#  ONE line), a real calendar date, at least 16 letters or digits of reason, no double quote, backslash, `$` or
-#  backtick; these check the FORM of a warrant, not who gave it -- and --write writes it
+#  --ruling "YYYY-MM-DD: <who ruled and why>" names that decision; it must look like one -- non-empty, printable
+#  ASCII only (so ONE line), a real calendar day (in UTC; its age is not checked), at least 16 letters or digits of
+#  reason, no double quote, backslash, `$` or backtick; these check the FORM of a warrant, not who gave it -- and
+#  --write writes it
 #  into the gate as a comment line above each pin change that needed it, so that change carries its warrant in the
 #  diff.  (A pin that moves without needing one -- the denominator, a rising #392 count -- gets no note.)
@@ -45,5 +49,9 @@
 #  repair's own pass found an impossible date, a punctuation-only reason and non-ASCII blanks or separators accepted
 #  in a ruling (each landed inside the comment line; none reached a pin), and a name holding `$`, a backtick, a
-#  quote or a backslash -- or no name at all -- written into the double-quoted list.)
+#  quote or a backslash -- or no name at all -- written into the double-quoted list.  And that repair's own pass
+#  found a name holding a LINE FEED accepted (one argument grandfathered two names), a real date refused where the
+#  local calendar skips a midnight, the gate's census lines run by a `python3` that did nothing (git-bash's Store
+#  stub: --release then accepted a probe still promptless), a list writer that would have written into a comment
+#  quoting the assignment, and whole-buffer FILE names written into WHOLE_FULL_FILES with no allow-list at all.)
 #
 #  Run it from anywhere; HERE is the regress directory beside this script's tools/ directory ($GXROOT overrides).
@@ -59,5 +67,8 @@
 case "${1:-}" in
     --write) MODE=write; shift
-             if [ "${1:-}" = --ruling ]; then RULING="${2:-}"; shift 2; fi
+             if [ "${1:-}" = --ruling ]; then
+                 [ -n "${2:-}" ] || { echo "REFUSED: --ruling needs its text -- an empty ruling is no ruling"; exit 2; }
+                 RULING="$2"; shift 2
+             fi
              [ $# -eq 0 ] || { echo "usage: $0 --write [--ruling \"YYYY-MM-DD: text\"]"; exit 2; } ;;
     --grandfather) MODE=grandfather; shift; GF=("$@") ;;
@@ -75,5 +86,6 @@
         || { echo "REFUSED: a ruling reads \"YYYY-MM-DD: <who ruled and why>\" (16+ characters of reason) -- got [$RULING]"; exit 2; }
     _day=${RULING%%:*}
-    [ "$(date -d "$_day" +%F 2>/dev/null)" = "$_day" ] || { echo "REFUSED: [$_day] is not a calendar date"; exit 2; }
+    #  in UTC: a local calendar can skip a midnight (a DST change), and GNU date then refuses a real day (the F4 pass)
+    [ "$(date -u -d "$_day" +%F 2>/dev/null)" = "$_day" ] || { echo "REFUSED: [$_day] is not a calendar date"; exit 2; }
     case "$RULING" in *'"'*|*'\'*|*'$'*|*'`'*) echo "REFUSED: the ruling text may not contain a double quote, a backslash, \$ or a backtick"; exit 2 ;; esac
     _why=$(printf '%s' "${RULING#*: }" | LC_ALL=C tr -cd 'A-Za-z0-9')
@@ -100,4 +112,13 @@
 GP=$(awk 'index($0,"GRANDFATHERED_PROMPTLESS=")==1 {p=1} p {print} p && /"[[:space:]]*$/ && NR>1 && !/^GRANDFATHERED_PROMPTLESS="[^"]*$/ {exit}' "$G")
 eval "$GP"
+#  The gate's census lines call `python3` BY NAME.  Under git-bash that can be the Windows Store stub, which exits
+#  without running anything: the classifier printed nothing, all 43 grandfathered names read as GONE, the report said
+#  "--release them", and --release accepted a probe that is still promptless (the census F4 pass, the Opus seat,
+#  measured).  So run them with the interpreter found above, and PROVE the classifier runs before trusting a word of
+#  its output: a path that does not exist must come back listed (census_tokens.py prints what it cannot read).
+python3 -c "import sys" >/dev/null 2>&1 || python3() { "$PY" "$@"; }
+_canary=$(printf 'zz_derive_canary_absent.py\n' | python3 "$HERE/census_tokens.py" promptless "$HERE" 2>/dev/null)
+[ "$_canary" = "zz_derive_canary_absent.py" ] || {
+    echo "DERIVE_FAIL: the token classifier did not run (census_tokens.py answered [$_canary] for a canary path); refusing"; exit 3; }
 eval "$CODE"
 
@@ -139,7 +160,9 @@
     for f in "${GF[@]}"; do
         #  the list is space-separated and written into a double-quoted shell string: a name with a blank cannot be
-        #  recorded (codex, the closing pass), `$`, a backtick, a quote or a backslash is live shell there, and an EMPTY
-        #  name matched the blank line an empty NEWP prints (the F3 pass).  So an allow-list, byte by byte:
-        [ -n "$f" ] && [ -z "$(printf '%s' "$f" | LC_ALL=C tr -d 'A-Za-z0-9._/-')" ] \
+        #  recorded (codex, the closing pass), `$`, a backtick, a double quote or a backslash is live shell there, and an EMPTY
+        #  name matched the blank line an empty NEWP prints (the F3 pass).  So an allow-list, COUNTED byte by byte with
+        #  wc -c: the F4 version tested $(...) for emptiness, and command substitution strips trailing newlines, so a
+        #  name holding a LINE FEED passed and grandfathered two names at once, one of them no file (the F4 pass).
+        [ -n "$f" ] && [ $(( $(printf '%s' "$f" | LC_ALL=C tr -d 'A-Za-z0-9._/-' | wc -c) )) -eq 0 ] \
             || { echo "REFUSED: [$f] -- a probe name here is ASCII letters, digits, '.', '_', '-' and '/' only; rename the probe"; exit 4; }
         if [ "$MODE" = grandfather ]; then
@@ -154,5 +177,9 @@
 g, mode, names = sys.argv[1], sys.argv[2], sys.argv[3:]
 s = io.open(g, encoding="utf-8", newline="").read()
-i = s.index('GRANDFATHERED_PROMPTLESS="') + len('GRANDFATHERED_PROMPTLESS="'); j = s.index('"', i)
+#  anchored at line start, as the reader above is: an unanchored search would write into the first COMMENT that
+#  quotes the assignment and leave a gate that no longer parses (the census F4 pass, the Opus seat)
+ms = list(re.finditer(r'(?m)^GRANDFATHERED_PROMPTLESS="', s))
+assert len(ms) == 1, "GRANDFATHERED_PROMPTLESS assignments at line start: %d" % len(ms)
+i = ms[0].end(); j = s.index('"', i)
 body = s[i:j]
 if mode == "grandfather":
@@ -173,4 +200,9 @@
 fi
 if [ "$MODE" = write ]; then
+    #  WHOLE_FULL_FILES is the other place this tool writes FILE NAMES into a double-quoted string in the gate, and it
+    #  had no allow-list: a pty file named with `$(...)` would have become shell source there on the next read (grok,
+    #  the F4 pass).  The same bytes as a grandfathered name, plus the ':' and the space of "name:count name:count":
+    [ $(( $(printf '%s' "$whole_files" | LC_ALL=C tr -d 'A-Za-z0-9._/: -' | wc -c) )) -eq 0 ] \
+        || { echo "REFUSED: a whole-buffer file name holds a byte outside A-Za-z0-9._/- -- rename the probe: [$whole_files]"; exit 5; }
     [ "$conv_anchor" = "$conv_echo" ] && [ "$conv_echo" = "$conv_mark" ] || {
         echo "REFUSED: the three #392 counts disagree ($conv_anchor/$conv_echo/$conv_mark) -- a guard present but uncounted; fix the probe, not the pin"; exit 5; }
```

## §F2 — the F4 pass's findings, with MY disposition of each

*(Self-review disclosed: I wrote F2-F5 and these dispositions.  The F4 pass: grok, glm, deepseek, minimax and the kimi
substitute DO NOT SHIP; agy SHIP; the kimi CLI walled; **the codex panel seat is a SEAT FAILURE -- its answer ends in a
content-filter refusal ("flagged for possible cybersecurity risk") and the "verdict" the tally found is text it had
echoed from a file**; the dedicated codex job (plain wording) answered FAIL; the Opus seat -- claude-opus-5-5 throughout,
verified from its transcript -- DO NOT SHIP, by measurement.)*

**M1 -- a name holding a LINE FEED passed the allow-list** (codex-dedicated, grok, glm; the Opus seat measured it end to
end: `$'\nzz_bogus.py'` written, `$'zz-legit_probe.py\nextra_name.py'` wrote a name nobody checked).  **ACCEPTED -> wc -c.**
**M2 -- `--ruling ""` skipped validation** (codex-dedicated).  **ACCEPTED -> refused.**
**M3 -- a real date refused where the local calendar skips a midnight** (codex-dedicated read it; the Opus seat measured
it on WSL; git-bash's date ignores TZ).  **ACCEPTED -> UTC.**
**M4 -- under git-bash the gate's `python3` is the Store stub; the classifier printed nothing and `--release` accepted a
probe that is still promptless** (the Opus seat, overturning my K16, which was reasoned, not measured).  **ACCEPTED ->
the interpreter shim and the canary.**
**M5 -- the list writer's search was unanchored** (the Opus seat, latent: today the literal occurs once).  **ACCEPTED ->
anchored, exactly one match.**
**M6 -- `WHOLE_FULL_FILES` receives file names with no allow-list; a pty probe named with `$(...)` would become shell
source** (grok).  **ACCEPTED -> the same byte allow-list.**
**M7 -- the header's reason for refusing glob characters was false: they are inert in the double-quoted list** (grok,
deepseek, glm, the kimi substitute, the Opus seat).  **ACCEPTED -> the real reason**: the gate's and the report's
printed lists expand names UNQUOTED.  The refusal itself is kept (no probe name needs a glob character).
**M8 -- "a quote" over-covers the apostrophe, which is inert in both places** (the kimi substitute).  **ACCEPTED.**
**M9 -- the gate's "closed-world over the literal spellings" is false: the textual comment filter drops every physical
line beginning with `#`, so code on such a line (after a closing triple quote -- `hash_line`) and a file saved with
CR-only line endings (`cr_only`: grep sees one line, beginning `#!`) escape** (the Opus seat, measured).  **ACCEPTED as
records** (the sentence now says "on the physical lines the comment filter keeps"); **the holes are FILED** with `e10`,
widened from f-strings to the comment filter's whole class (pre-existing code).
**M10 -- K7's "counts as known" is imprecise: a bare `">"` literal is known and still fails the bare row** (the Opus
seat).  **ACCEPTED as records.**
**M11 -- K14 fails OPEN: a grandfathered probe gaining `case K.endswith("GXemul>"):` reads as no longer promptless, and
`--release` then takes it off the list with every row green** (the Opus seat, measured).  **DISCLOSED** in the docstring,
**FILED** (a token classifier is not a parser; an `ast`-based credit would close it -- a classifier change, its own round).
**M12 -- K15 is now a measured false pass** (the Opus seat: a probe moved to `newsub/readiness_predicate_test.py`
passes all 12 rows).  **FILED** (pre-existing), with the measurement.
**M13 -- K12's spaced-dot shape is e9's line-based class, not the whole-shape class; `n3g` (`buf .rstrip()`) is caught**
(grok).  **ACCEPTED** for the filing text.
**M14 -- `${RULING%%:*}` cuts at the LAST colon, so a reason holding a colon is refused** (minimax).  **REJECTED BY
MEASUREMENT** (above): `%%` cuts at the FIRST colon.
**M15 -- years 0000/0001 and 9999 are accepted** (codex-dedicated, the Opus seat).  **KEPT, and said so**: the header
now says the date is checked for being a calendar day, not for its age.
**M16 -- the tool refuses names a filesystem allows (`probe+v2.py`, `O'Brien.py`, `café.py`)** (codex-dedicated, glm).
**KEPT as policy, stated** ("rename the probe"); all 43 grandfathered names are inside the allow-list.

**D3 -- DO NOT SHIP on F4** (all answering seats but agy).  Settled by measurement: M1 was real (the Opus seat's
end-to-end run), so were M3-M6.

**WHERE I MIGHT BE FOOLING MYSELF**: every pass over the deriver since F2 has found an input its checks let through, and
F5 again answers each by class (byte counts, allow-lists, a canary, an anchor).  I have enumerated the INPUTS the tool
takes (the ruling text, the name arguments, the tree's file names via the census) -- if there is a fourth input, I
have not listed it.

## §E -- QUESTIONS (answer each, numbered; from the packet alone, do Q1 and Q3 first)

**Q1 -- do the F5 checks refuse exactly what they say?**  (a) Every INPUT the deriver takes and writes into the gate:
is each one checked, and is each check byte-exact (no `$(...)` emptiness test, no line-based grep deciding a
multi-line value)?  Name any input I have not listed.  (b) The interpreter shim and the canary: can the classifier fail
in a way the canary does not see (it runs, prints the canary, and still misclassifies)?  (c) The anchored writer: can the
reader and the writer still disagree about which line is the list?
**Q2 -- the smallest input or tree state that gets past the F5 checks and does harm**: a ruling that lands anything but
comment lines, a pin moved without a warrant, a name or file name that changes meaning in the gate, or a census that
comes out empty or wrong while the deriver reports success.  If none, give your denominator.
**Q3 -- adjudicate M1-M16 and D3**: UPHOLD / OVERTURN / REFINE / CANNOT SETTLE, one line each with a reason.  Then:
**WHICH OF MY ACCEPTED DISPOSITIONS IS WRONG?**  In particular M9 and M11 (filed rather than fixed) and M14 (rejected).
**Q4 -- records**: is any sentence in the changed comments or the deriver's header false as of today?
**Q5 -- option-set completeness**: for M9 and M11, is there a disposition I did not name?

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
