# hygienecensus -- the F6 repair's own pass (F6, F6b, F6c, F6d together): the LAST review pass of this chain, by owner ruling

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly.  **Check the premises,
not just the derivations.**  A seat that re-derives a premise from something this brief did NOT give it is worth more
than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/`** -- `tools/derive_hygiene_pins.sh` and `regress/gate_hygiene.sh`
(`regress/census_tokens.py` is unchanged since F5).  File-reading seats: read the FROZEN copies in
`C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\census0923\c6_frozen\` (derive_hygiene_pins.sh 58feb3d3, gate_hygiene.sh
9edb00bb, census_tokens.py 98788b1b); the F5 versions the last pass reviewed are in `c5_frozen\` (e1ce9c59, 9d88b3f6,
98788b1b).  There are pristine-2021-upstream copies of GXemul under the project root (`./src/`, `_archive/`); they are
NOT this fork.

**If you cannot read files that is expected** -- the diff and the measurements are inlined below.  Name any premise
you cannot settle from this packet rather than guessing.  **ENUMERATE** any count or set rather than reasoning about it.
**VERDICT LINE FIRST**: `VERDICT: SHIP` or `VERDICT: DO NOT SHIP -- <reason>`.  **A zero needs a denominator**.

## THE OWNER'S RULING FOR THIS PASS (2026-09-23) -- it changes what a finding buys

This is the chain's LAST review pass.  **A finding is fixed in this round only if a REAL probe name, or REAL use of the
tool under git-bash or WSL, could trigger it.**  Findings that need a crafted file name, a deliberately broken
interpreter or classifier, a hand-edited gate layout or an unusual environment variable are FILED as one LOW item.
So for every finding, say which kind it is, and **why** -- the classification is the question, not a formality.

## Where the census round stands

Gate 6's readiness census counts, over the probes that drive the emulator through a pseudo-terminal, which spellings
of a prompt-readiness test they use and which probes have none; its pins are written only by
`tools/derive_hygiene_pins.sh`.  F2 -> F3 -> F4 -> F5 -> **the F5 pass (`panel_20260923_192141`: codex, grok, glm and
minimax DO NOT SHIP, all on M6; agy and kimi-k3:cloud SHIP; deepseek answered without a verdict line; the kimi CLI
walled on its weekly limit; a dedicated codex job; the Opus measuring seat) -> F6, F6b, F6c, F6d: THIS pass.**

## What changed since F5 (the full diff F5 -> F6d is inlined below; `census_tokens.py` is unchanged)

**F6** (19:34; the F5 pass's dedicated codex job):
1. **Both writers check every field against its grammar immediately before writing** -- counts decimal,
   WHOLE_FULL_FILES `name:count` tokens, names the allow-list, the ruling and the change note printable ASCII -- and
   refuse with rc 5, nothing written ("a value no check anticipated is refused at the sink").
2. **Every census value is checked as a count** right after the gate's lines run (a failed or garbled census line
   leaves an empty or non-numeric value; three empty #392 counts compare equal): DERIVE_FAIL rc 3.
3. **A `--grandfather` name must be a FILE** under regress/.
4. **The classifier canary runs in BOTH modes, in a fresh temp directory**: a file holding one whole-buffer call must
   be NOT promptless and hold 1 whole site; a path that does not exist must be listed.
5. **WHOLE_FULL_FILES is checked PER TOKEN**: each space-separated entry `name:count`, the name in the names'
   allow-list (the F5 byte set admitted a space or a colon INSIDE a name).
6. Records: the header; the gate's line-based sentence now says only the TEXTUAL counts are line-based.

**F6b** (19:40; the F5 pass's Opus measuring seat):
1. **Every whole-buffer entry must name a FILE** (`[ -f "$HERE/${_e%:*}" ]`): a tree file named `zz:9 x.py` split into
   `zz:9` and `x.py:1` and wrote EXPECT_WHOLE_FULL=13 for 4 real sites, every row green.
2. **The interpreter shim is unconditional and strips CRs**: `python3() { command "$PY" "$@" | tr -d '\r'; }` -- under
   git-bash the fallback python writes CRLF and the CRs refused every `--write` ("rename the probe").
3. **`--grandfather` / `--release` re-check the named file with Python's own parser** (`astcall`: rc 0 if an
   `X.endswith(...)` Call exists, 1 if it parses and none does, 2 if it cannot parse): `--grandfather` needs rc 1,
   `--release` needs rc 0 for a file still in the tree.  A classifier that failed part-way, or a `match` class pattern
   `case K.endswith("GXemul>"):` it credits, let `--release` take a still-promptless probe off the list.
4. **The printed NEW and GONE lists, and the gate's own NEW list, print under `set -f`**: a tree file named `zz*.py`
   printed as every file the glob matched.

**F6c** (20:1x; the rest of the F5 pass, under the owner's ruling):
1. **The UNTRACKED list prints under `set -f` too** -- the third list the F5 finding named.
2. Records: the canary is described as a LIVENESS check, not a proof (a classifier that dies part-way or misclassifies
   passes it; the report can then be wrong; `--release` is parser-checked and `--write` refuses while any grandfathered
   name reads as GONE); the LINE FEED sentence names the class measured (a name whose ONLY disallowed byte was a LF);
   the crafted-name residue is named where it lives, as filed.

**F6d** (20:3x; found by F6c's own controls, **a defect F6b introduced**):
1. **`pywrite` calls `command "$PY"`.**  Under WSL `PY` is the NAME `python3`, which F6b's now-unconditional shim
   shadows; a pipe's status is `tr`'s, so from F6b on **every writer refusal (rc 5) or death (rc 1) read as success
   under WSL and the tool printed DERIVE_DONE** (control t_pyopt0: the writer's multiplicity assertion failed, rc 0).
   git-bash was spared (`PY` is `python` there).  `astcall` already bypassed the shim.

## Measured (on `/tmp` or project-local copies; predictions written first, misses recorded)

`regress/artifacts/hygienecensus_20260923/controls_c6/` (F6 vs F5, predictions 19:34:48), `controls_c6b/` (F6c vs F6,
20:10:47 + an addendum 20:1x + CORRECTIONS), `controls_c6d/` (F6d vs F6, 20:18:11):
* **The whole earlier suite** (`real`, the 45 F2 edits, the closing-pass cases, every c4/c5 ruling and name case)
  gives verdicts **IDENTICAL** to F5's on F6, F6c and F6d (`diff` of the tables: empty).
* `t_wfcolon2` -- a pty probe named `zz:9 x.py` (a copy of arm_flags_probe.py, two whole-buffer sites): **F6d REFUSED
  rc 5** "the whole-buffer entry [zz:9] names no file", gate unchanged.  F6 WROTE EXPECT_WHOLE_FULL=14 for 5 real sites,
  every gate row green.
* `t_wfcolon3` -- a probe named `arm_bdt_probe.py:9 x.py` beside a real `x.py`: **WRITTEN on F6d too** (14 for 5, green)
  -- the crafted-name residue, FILED LOW by the owner's ruling.
* `t_k14release` / `t_partial` -- a `match` class pattern credited as a readiness call / a classifier that raises after
  ten inputs (38 names read GONE), then `--release gdrom_cond_probe.py`: **F6d REFUSED rc 4** "the parser finds no
  readiness call in it (rc 1): it is still promptless", list 43.  F6 RELEASED it (42).  The same under git-bash
  (`t_gbk14`); a real release (a real call added) is RELEASED on both shells (`t_gbrelease`), and a real grandfather
  GRANDFATHERED (`t_gbgrand`).
* `t_globname` -- a promptless probe named `zz*.py` beside a plain `zz_other.py`: F6d prints `zz*.py` in NEW, UNTRACKED
  and the gate's own list; F6 printed both names in all three.
* `t_rlf` / `t_rctl` -- a ruling holding a LINE FEED (glm) / a `\x01` (minimax): REFUSED rc 2 "printable ASCII, on one
  line" on both, gate unchanged.  (The check is `tr -d ' -~' | wc -c`, byte-exact.)
* `t_pyopt0` -- a duplicate GRANDFATHERED_PROMPTLESS line, then `--grandfather`: **F6c printed DERIVE_DONE rc 0 with the
  writer's assertion failing** -- the defect F6d fixes -- and **F6d prints DERIVE_FAIL rc 6**.  `t_pyopt1` (the same
  under PYTHONOPTIMIZE=1): GRANDFATHERED rc 0 on every version -- the assert is dropped; FILED LOW.
* `t_gpbytes` -- the gate's own name pins through the names' allow-list: GRANDFATHERED_PROMPTLESS 43 names, 0 bytes
  outside it; WHOLE_FULL_FILES 0 (glm's M16 premise, now shown).
* **git-bash** (`python3` = the Store stub, rc 49; the fallback `python` 3.12.10 writes CRLF): F6d's report equals every
  pin with 0 CR bytes (F6's WHOLE_FULL_FILES carried 2); **`--write` with a new whole-buffer probe WRITES clean LF pins
  and the gate, run under WSL on that tree, passes 12 of 12 readiness rows**; F6 REFUSED it (rc 5, at its sink).
* Prediction misses, each recorded in `controls_c6b/PREDICTIONS.corrections.txt`: t_pyopt0 (the defect); my t_gpbytes
  counted a newline; c6new's t_sink is now refused one check earlier; F6's git-bash refusal came from its sink, not its
  per-token check; the WSL gate step on a git-bash tree measured nothing twice (git-bash's `/tmp` is not WSL's).
* **Owed**: gate 6 on the final files, in the next quiet slot.

## §C — SETTLED PREMISES (recorded resolutions; say if the diff contradicts one)

1. The owner's rulings govern; the pins are written by the deriver, never by hand.  **This is the chain's last pass;
   exotic-input findings are FILED LOW** (the ruling above).
2. **The census is a SPELLING census**: it guarantees which spellings of a readiness test exist, not that a probe's
   readiness logic is right.
3. **The stopping rule**: in-round only a measured false pass or a wrong record in THIS round's material.
4. The textual closed-world counts are LINE-based and drop every physical line beginning with `#`; the token classifier
   (`census_tokens.py`) is not a parser -- `astcall` (F6b) is a separate check by Python's own parser, at the two
   decisions that change the grandfather list.
5. `${RULING%%:*}` yields the text before the FIRST colon (measured on F5; `%%` removes the longest suffix matching `:*`).

## The diff, F5 -> F6d (INLINED IN FULL)

`tools/derive_hygiene_pins.sh`, e1ce9c59 -> 58feb3d3 (7 hunks):

```diff
--- _scratchpad/census0923/c5_frozen/derive_hygiene_pins.sh	2026-09-23 19:20:32.668793500 -0500
+++ _scratchpad/census0923/c6_frozen/derive_hygiene_pins.sh	2026-09-23 20:17:38.434146200 -0500
@@ -26,8 +26,11 @@
 #  --write REFUSES, each with its reason printed, and the refusals are the point of the tool:
 #    * the pty denominator is 0 -- the enumerators saw nothing (wrong tree, moved file);
 #    * the three #392 counts (anchor, echo, fresh mark) disagree -- one pin, and a disagreement IS a defect;
-#    * a whole-buffer FILE NAME holds a byte outside the names' allow-list below -- WHOLE_FULL_FILES is the other
-#      double-quoted string this tool writes names into;
+#    * a whole-buffer entry is not "name:count" with the name in the names' allow-list below and naming a FILE --
+#      WHOLE_FULL_FILES is the other double-quoted string this tool writes names into;
+#    * a census value is not a count, or the token classifier fails its canaries (DERIVE_FAIL, before any report);
+#  and BOTH writers check every field against its grammar immediately before writing -- counts, name:count tokens,
+#  names, the printable ruling and change note -- so a value no check above anticipated is refused at the sink;
 #    * a promptless probe is neither grandfathered nor given prompt detection, or a grandfathered probe is no longer
 #      promptless -- the gate grades the NAMES, so --grandfather / --release first;
 #    * EXPECT_BARE or EXPECT_UNKNOWN would RISE -- defects the gate freezes at their pins (they may fall);
@@ -49,7 +52,8 @@
 #  repair's own pass found an impossible date, a punctuation-only reason and non-ASCII blanks or separators accepted
 #  in a ruling (each landed inside the comment line; none reached a pin), and a name holding `$`, a backtick, a
 #  quote or a backslash -- or no name at all -- written into the double-quoted list.  And that repair's own pass
-#  found a name holding a LINE FEED accepted (one argument grandfathered two names), a real date refused where the
+#  found a name whose one disallowed byte was a LINE FEED accepted (one argument grandfathered two names), a real
+#  date refused where the
 #  local calendar skips a midnight, the gate's census lines run by a `python3` that did nothing (git-bash's Store
 #  stub: --release then accepted a probe still promptless), a list writer that would have written into a comment
 #  quoting the assignment, and whole-buffer FILE names written into WHOLE_FULL_FILES with no allow-list at all.)
@@ -114,13 +118,33 @@
 #  The gate's census lines call `python3` BY NAME.  Under git-bash that can be the Windows Store stub, which exits
 #  without running anything: the classifier printed nothing, all 43 grandfathered names read as GONE, the report said
 #  "--release them", and --release accepted a probe that is still promptless (the census F4 pass, the Opus seat,
-#  measured).  So run them with the interpreter found above, and PROVE the classifier runs before trusting a word of
-#  its output: a path that does not exist must come back listed (census_tokens.py prints what it cannot read).
-python3 -c "import sys" >/dev/null 2>&1 || python3() { "$PY" "$@"; }
-_canary=$(printf 'zz_derive_canary_absent.py\n' | python3 "$HERE/census_tokens.py" promptless "$HERE" 2>/dev/null)
-[ "$_canary" = "zz_derive_canary_absent.py" ] || {
-    echo "DERIVE_FAIL: the token classifier did not run (census_tokens.py answered [$_canary] for a canary path); refusing"; exit 3; }
+#  measured).  So run them with the interpreter found above, and check that the classifier ANSWERS before using its
+#  output -- in BOTH of its modes and on BOTH of its paths, on canaries in a fresh temp directory (the F5 canary
+#  exercised only the unreadable-path branch, and a real file of its name would have failed it; codex, the F5 pass):
+#  a file holding one whole-buffer call is NOT promptless and holds 1 whole site; a path that does not exist IS listed.
+#  That is a LIVENESS check, not a proof: a classifier that dies part-way through the real tree, or misclassifies a
+#  readable file, passes it (the F5 pass: grok, codex; the Opus seat measured a crash after ten inputs), and its
+#  report can then be wrong.  So --release is re-checked by Python's own parser, and --write refuses while any
+#  grandfathered name reads as no longer promptless; the report alone stays unproven (filed LOW, owner ruling
+#  2026-09-23).
+#  ALWAYS through the interpreter found above, and with CRs stripped: Windows python writes CRLF, and under git-bash the
+#  CRs rode into whole_files and refused every --write ("rename the probe"; the F5 pass, the Opus seat).  `command`
+#  so a PY of "python3" does not call this function again.
+python3() { command "$PY" "$@" | tr -d '\r'; }
+_cd=$(mktemp -d 2>/dev/null) && [ -d "$_cd" ] || { echo "DERIVE_FAIL: no temp directory for the classifier canary"; exit 3; }
+printf 'buf.rstrip().ends''with("GXemul>")\n' > "$_cd/zz_canary_call.py"
+_c1=$(printf 'zz_canary_call.py\n' | python3 "$HERE/census_tokens.py" promptless "$_cd" 2>/dev/null)
+_c2=$(printf 'zz_canary_call.py\n' | python3 "$HERE/census_tokens.py" whole "$_cd" 2>/dev/null)
+_c3=$(printf 'zz_canary_absent.py\n' | python3 "$HERE/census_tokens.py" promptless "$_cd" 2>/dev/null)
+rm -rf "$_cd"
+[ -z "$_c1" ] && [ "$_c2" = "zz_canary_call.py:1" ] && [ "$_c3" = "zz_canary_absent.py" ] || {
+    echo "DERIVE_FAIL: the token classifier failed its canaries (promptless [$_c1], whole [$_c2], absent [$_c3]); refusing"; exit 3; }
 eval "$CODE"
+#  every census value is a COUNT: an enumerator or classifier line that failed leaves an empty or garbled value, and
+#  three empty #392 counts compare equal (codex, the F5 pass).  Refuse to report or write from one.
+for _v in bare allends full unknown _ptyn conv_anchor conv_echo conv_mark whole_full; do
+    case "${!_v}" in ''|*[!0-9]*) echo "DERIVE_FAIL: the census value $_v is [${!_v}], not a count -- a census line failed"; exit 3 ;; esac
+done
 
 pin() { sed -n "s/^$1=\([0-9]*\).*/\1/p" "$G" | head -1; }
 spin() { sed -n "s/^$1=\"\(.*\)\"$/\1/p" "$G" | head -1; }
@@ -144,12 +168,33 @@
 printf '%-34s %6s %6s\n' "EXPECT_CONVERTED (fresh mark)" "$conv_mark" "$(pin EXPECT_CONVERTED)"
 printf '%-34s %6s %6s\n' EXPECT_WHOLE_FULL "$whole_full" "$(pin EXPECT_WHOLE_FULL)"
 printf '%-34s got    [%s]\n%-34s pinned [%s]\n' WHOLE_FULL_FILES "$whole_files" "" "$WFP"
-[ -n "$NEWP" ] && { echo "NEW PROMPTLESS (neither grandfathered nor prompt-detecting):"; printf '  %s\n' $NEWP; }
-[ -n "$GONE" ] && { echo "GRANDFATHERED BUT NO LONGER PROMPTLESS (--release them):"; printf '  %s\n' $GONE; }
-[ -n "$UNTR" ] && { echo "UNTRACKED files counted by these censuses (the battery counts what is lying in the tree):"; printf '  %s\n' $UNTR; }
+#  set -f: a tree file named with a glob character must print as itself, not as the files it matches (the F5 pass
+#  named all three lists; F6b quoted two)
+[ -n "$NEWP" ] && { echo "NEW PROMPTLESS (neither grandfathered nor prompt-detecting):"; ( set -f; printf '  %s\n' $NEWP ); }
+[ -n "$GONE" ] && { echo "GRANDFATHERED BUT NO LONGER PROMPTLESS (--release them):"; ( set -f; printf '  %s\n' $GONE ); }
+[ -n "$UNTR" ] && { echo "UNTRACKED files counted by these censuses (the battery counts what is lying in the tree):"; ( set -f; printf '  %s\n' $UNTR ); }
 
 #  run the python writer and FAIL LOUDLY if it fails -- the first version printed DERIVE_DONE after a failed write
-pywrite() { "$PY" - "$@"; local rc=$?; [ $rc -eq 0 ] || { echo "DERIVE_FAIL: the writer failed (rc=$rc); nothing to trust in $G"; exit 6; }; }
+#  astcall FILE: rc 0 if Python's parser finds a CALL of the form X.endswith(...) in FILE, 1 if it parses and finds none,
+#  anything else if it cannot read or parse it -- an independent check of the token census at the grandfather/release
+#  decision, with its exit status read (the census lines' is not).
+astcall() { command "$PY" - "$1" <<'PY'
+import ast, sys
+try:
+    t = ast.parse(open(sys.argv[1], encoding="utf-8").read())
+except Exception:
+    sys.exit(2)
+m = "ends" + "with"
+sys.exit(0 if any(isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == m
+                  for n in ast.walk(t)) else 1)
+PY
+}
+#  rc 5 is the writer's own grammar check refusing BEFORE it writes anything (F6): a refusal, and the gate is untouched.
+#  `command`: PY is the NAME python3 under WSL, which the CR-stripping shim above shadows, and a pipe's status is tr's
+#  -- so from F6b to F6c a writer that refused or died read as success under WSL, and the tool printed DERIVE_DONE
+#  (census F6c controls, t_pyopt0: the writer's own multiplicity check failed, rc 0).  astcall already bypassed it.
+pywrite() { command "$PY" - "$@"; local rc=$?; [ $rc -eq 0 ] && return; [ $rc -eq 5 ] && exit 5
+            echo "DERIVE_FAIL: the writer failed (rc=$rc); nothing to trust in $G"; exit 6; }
 
 if [ "$MODE" = grandfather ] || [ "$MODE" = release ]; then
     [ ${#GF[@]} -gt 0 ] || { echo "REFUSED: --$MODE needs the file names, one by one"; exit 4; }
@@ -162,19 +207,35 @@
         #  recorded (codex, the closing pass), `$`, a backtick, a double quote or a backslash is live shell there, and an EMPTY
         #  name matched the blank line an empty NEWP prints (the F3 pass).  So an allow-list, COUNTED byte by byte with
         #  wc -c: the F4 version tested $(...) for emptiness, and command substitution strips trailing newlines, so a
-        #  name holding a LINE FEED passed and grandfathered two names at once, one of them no file (the F4 pass).
+        #  name whose ONLY disallowed byte was a LINE FEED passed -- and grandfathered two names at once, one of them
+        #  no file (the F4 pass).
         [ -n "$f" ] && [ $(( $(printf '%s' "$f" | LC_ALL=C tr -d 'A-Za-z0-9._/-' | wc -c) )) -eq 0 ] \
             || { echo "REFUSED: [$f] -- a probe name here is ASCII letters, digits, '.', '_', '-' and '/' only; rename the probe"; exit 4; }
         if [ "$MODE" = grandfather ]; then
+            #  a FILE in regress/: the census's enumerators are line-based, so a file name holding a newline reaches the
+            #  classifier as fragments that do not exist -- and it lists what it cannot read (codex, the F5 pass)
+            [ -f "$HERE/$f" ] || { echo "REFUSED: $f is not a file under regress/"; exit 4; }
             printf '%s\n' "$GFS" | grep -qxF -- "$f" && { echo "REFUSED: $f is already grandfathered"; exit 4; }
             printf '%s\n' "$NEWP" | grep -qxF -- "$f" || { echo "REFUSED: $f is not a NEW promptless probe"; exit 4; }
+            #  and Python's own PARSER agrees: no `.endswith(...)` CALL in it (the token census is not a parser -- F6b)
+            astcall "$HERE/$f"; _a=$?
+            [ $_a -eq 1 ] || { echo "REFUSED: $f -- the parser finds a readiness call, or cannot parse it (rc $_a); the census disagrees"; exit 4; }
         else
             printf '%s\n' "$GONE" | grep -qxF -- "$f" || { echo "REFUSED: $f is not a grandfathered name that is no longer promptless"; exit 4; }
+            #  a probe still in the tree must now make a real `.endswith(...)` CALL, by Python's own parser: a classifier
+            #  that failed part-way, or a `match` class pattern it credits, let --release take a still-promptless probe
+            #  off the list (the F5 pass, the Opus seat, measured).  A probe deleted from the tree is released as it is.
+            if [ -e "$HERE/$f" ]; then
+                astcall "$HERE/$f"; _a=$?
+                [ $_a -eq 0 ] || { echo "REFUSED: $f -- the parser finds no readiness call in it (rc $_a): it is still promptless"; exit 4; }
+            fi
         fi
     done
     pywrite "$G" "$MODE" "${GF[@]}" <<'PY'
 import io, re, sys
 g, mode, names = sys.argv[1], sys.argv[2], sys.argv[3:]
+if not all(re.fullmatch(r"[A-Za-z0-9._/-]+", n) for n in names):
+    print("REFUSED: the writer's grammar check failed for a name -- nothing written"); sys.exit(5)
 s = io.open(g, encoding="utf-8", newline="").read()
 #  anchored at line start, as the reader above is: an unanchored search would write into the first COMMENT that
 #  quotes the assignment and leave a gate that no longer parses (the census F4 pass, the Opus seat)
@@ -201,9 +262,18 @@
 if [ "$MODE" = write ]; then
     #  WHOLE_FULL_FILES is the other place this tool writes FILE NAMES into a double-quoted string in the gate, and it
     #  had no allow-list: a pty file named with `$(...)` would have become shell source there on the next read (grok,
-    #  the F4 pass).  The same bytes as a grandfathered name, plus the ':' and the space of "name:count name:count":
-    [ $(( $(printf '%s' "$whole_files" | LC_ALL=C tr -d 'A-Za-z0-9._/: -' | wc -c) )) -eq 0 ] \
-        || { echo "REFUSED: a whole-buffer file name holds a byte outside A-Za-z0-9._/- -- rename the probe: [$whole_files]"; exit 5; }
+    #  the F4 pass).  PER TOKEN, "name:count" with the name in the grandfather allow-list: the F5 byte set admitted a
+    #  space or a colon INSIDE a name, since both are also its separators (codex, the F5 pass).
+    [ -z "$(printf '%s' "$whole_files" | tr ' ' '\n' | LC_ALL=C grep -vxE '[A-Za-z0-9._/-]+:[0-9]+')" ] \
+        || { echo "REFUSED: a whole-buffer entry is not name:count with the name in A-Za-z0-9._/- -- rename the probe: [$whole_files]"; exit 5; }
+    #  and every entry names a FILE: a tree file named `zz:9 x.py` splits into two well-formed entries, `zz:9` and
+    #  `x.py:1`, and wrote EXPECT_WHOLE_FULL=13 for 4 real sites with every row green (the F5 pass, the Opus seat)
+    for _e in $(printf '%s' "$whole_files" | tr ' ' '\n'); do
+        [ -f "$HERE/${_e%:*}" ] || { echo "REFUSED: the whole-buffer entry [$_e] names no file under regress/ -- a file name the census split; rename it"; exit 5; }
+    done
+    #  NOT refused, and filed LOW by owner ruling (2026-09-23: a CRAFTED name is filed, not fixed): a name whose
+    #  space-split pieces each read as an existing file with a count -- `arm_bdt_probe.py:9 x.py` beside a real x.py
+    #  (grok, the F5 pass, on the F6 draft).  Validating the TREE's names before the census serialises them closes it.
     [ "$conv_anchor" = "$conv_echo" ] && [ "$conv_echo" = "$conv_mark" ] || {
         echo "REFUSED: the three #392 counts disagree ($conv_anchor/$conv_echo/$conv_mark) -- a guard present but uncounted; fix the probe, not the pin"; exit 5; }
     [ -z "$NEWP" ] || { echo "REFUSED: new promptless probes must be grandfathered by NAME (--grandfather) or given prompt detection first"; exit 5; }
@@ -221,6 +291,16 @@
     pywrite "$G" "$bare" "$unknown" "$_ptyn" "$conv_anchor" "$whole_full" "$whole_files" "$RULING" "$NEED" <<'PY'
 import io, re, sys
 g, bare, unk, pty, conv, whole, files, ruling, need = sys.argv[1:]
+#  F6: THE SINK checks every field it is about to write, whatever the shell above already checked -- the class the census
+#  passes kept finding one member of at a time (a newline, a `$`, a space, an empty count)
+_bad = [k for k, v, rx in (("EXPECT_BARE", bare, r"[0-9]+"), ("EXPECT_UNKNOWN", unk, r"[0-9]+"),
+                           ("EXPECT_PTY_PROBES", pty, r"[0-9]+"), ("EXPECT_CONVERTED", conv, r"[0-9]+"),
+                           ("EXPECT_WHOLE_FULL", whole, r"[0-9]+"),
+                           ("WHOLE_FULL_FILES", files, r"(?:[A-Za-z0-9._/-]+:[0-9]+(?: [A-Za-z0-9._/-]+:[0-9]+)*)?"),
+                           ("the ruling", ruling, r'[ !#%&-\[\]-_a-~]*'), ("the change note", need, r"[ -~]*"))
+        if not re.fullmatch(rx, v)]
+if _bad:
+    print("REFUSED: the writer's grammar check failed for %s -- nothing written" % ", ".join(_bad)); sys.exit(5)
 s = io.open(g, encoding="utf-8", newline="").read()
 note = ("#  RULING %s -- %s (tools/derive_hygiene_pins.sh --write)\n" % (ruling, need.strip())) if (ruling and need.strip()) else ""
 for k, v in (("EXPECT_BARE", bare), ("EXPECT_UNKNOWN", unk), ("EXPECT_PTY_PROBES", pty), ("EXPECT_CONVERTED", conv),
```

`regress/gate_hygiene.sh`, 9d88b3f6 -> 9edb00bb (2 hunks):

```diff
--- _scratchpad/census0923/c5_frozen/gate_hygiene.sh	2026-09-23 19:20:32.665283500 -0500
+++ _scratchpad/census0923/c6_frozen/gate_hygiene.sh	2026-09-23 19:40:28.261996200 -0500
@@ -84,8 +84,9 @@
 #      enumerated everything and recognised all of it" -- for the spellings
 #      these counts can SEE.
 #      (*** 2026-09-23: this said it was "the only form that cannot be evaded
-#      by inventing a new way to write it".  FALSE: every count here is LINE-
-#      based and keys on the literal `endswith(`, so a space before the paren
+#      by inventing a new way to write it".  FALSE: every TEXTUAL count here
+#      (bare, allends, full, unknown -- the token classifier is not one of
+#      them) is LINE-based and keys on `endswith(`, so a space before the paren
 #      (`endswith (">")`) or a backslash continuation between the name and
 #      the paren removes a call from all of them (both measured on copies,
 #      controls_f2 e_e9 and controls_c5 t_bsl).  Filed as hygienecensusholes
@@ -485,8 +486,8 @@
 if [ -n "$_new" ]; then
         echo "  NEW PROMPTLESS PTY PROBE(S) -- add prompt detection, or grandfather"
         echo "  deliberately by editing GRANDFATHERED_PROMPTLESS above:"
-        printf '    %s
-' $_new
+        ( set -f; printf '    %s
+' $_new )   # set -f: a tree file named with a glob character prints as itself (census F5 pass)
 fi
 
 #  THE POSITIVE HALF OF THE #392 CHECK, and it is the half that binds the offline
```

## §F2 — the F5 pass's findings, with MY disposition of each

* **N1** [codex, grok, deepseek, minimax; the Opus seat measured `zz:9 x.py` -> 13 for 4] M6's byte set admitted a space
  and a colon inside a name.  **F6 + F6b**: per-token `name:count`, each naming a file.  Residue (grok): pieces that each
  name a real file -- **FILED LOW** (crafted name).
* **N2** [the Opus seat, codex] under git-bash every `--write` was refused and the report's WHOLE_FULL_FILES carried
  CRs ("equals every pin" was false).  **F6b**: the shim strips CRs.  REAL use -> fixed; measured on git-bash.
* **N3** [the Opus seat K14, k_partial, P4; grok; codex; glm; deepseek] `--release` took a still-promptless probe off the
  list (a `match` class pattern, a classifier that died part-way, one that misclassified).  **F6b**: `astcall`.
* **N4** [the Opus seat P7; grok] glob characters in TREE names expanded in the printed lists.  **F6b + F6c** (`set -f`
  on all four lists).  Crafted-name class, fixed before the ruling; kept.
* **N5** [the Opus seat P5] a real file named like the canary made every mode DERIVE_FAIL.  **F6**: the canary lives in
  a fresh temp directory.
* **N6** [grok, agy] the canary never exercised `whole` mode or a readable file.  **F6**: both modes, both paths.
* **N7** [codex, grok, minimax, glm] the canary proves liveness, not correctness; the census lines' exit status is
  discarded, so a partial crash yields a partial report.  **F6c**: the comment says so; `--release` is parser-checked
  and `--write` refuses while a name is GONE.  The REPORT alone stays unproven -> **FILED LOW** (a broken classifier).
* **N8** [codex] a garbled census value (three empty #392 counts compare equal).  **F6**: every value checked as a count.
* **N9** [glm, minimax] does the ruling check refuse a LF, or a control byte?  **Measured: yes, rc 2** (t_rlf, t_rctl).
* **N10** [glm] the gate's own GRANDFATHERED_PROMPTLESS is `eval`'d before any check.  **Measured clean** (t_gpbytes);
  a live byte needs a hand edit -> **FILED LOW**.
* **N11** [codex] PYTHONOPTIMIZE drops the writers' four asserts.  **Measured** (t_pyopt1) -> **FILED LOW** (an unusual
  environment).
* **N12** [codex, glm, kimi-k3:cloud, grok] the reader and the writers key on different layouts of a hand-edited gate;
  the numeric writers replace the first `^NAME=` line.  **FILED LOW** (hand edit).
* **N13** [kimi-k3:cloud] the LINE FEED record overstated the class measured.  **F6c**: reworded.
* **N14** [grok, the Opus seat] the canary comment claimed a proof.  **F6c**: reworded (liveness).
* **N15** [codex, glm, deepseek] M11's option set lacked a deriver-side guard at `--release`.  Taken as `astcall` (N3).
  M9's comment filter stays FILED (pre-existing).
* **N16** (mine, from F6c's controls) **F6b made every writer failure read as success under WSL** -- REAL use, fixed as
  **F6d**, measured both ways.  It was found by a control written for N11, not by the suite: every writer failure the
  suite drives is refused by a bash check before the writer runs.

## §E -- QUESTIONS (answer each, numbered)

**Q1 -- do F6-F6d do what they claim?**  For each of N1-N16, is the closure correct, and is the classification (REAL
use -> fixed, exotic -> filed) right?  Name any FILED item a real probe name or real git-bash/WSL use could trigger.
**Q2 -- the smallest REAL-use input** (a real probe name, a real ruling, git-bash or WSL as installed) that gets past F6d
and does harm -- a wrong pin written, a wrong name listed or released, a failure reported as success.  With a
denominator: which inputs and which of the tool's paths you swept.
**Q3 -- F6b/F6d introduced the shim and `astcall`**: is either wrong under REAL use in either shell (argument paths
under MSYS conversion, CRLF, the heredoc on stdin, a probe that does not parse, a probe deleted from the tree)?
**Q4 -- records**: is any sentence in the F6-F6d comments or header false as of today?
**Q5 -- closing**: is this pass VALID to close the chain (the diff delivered, the roster, your denominator)?  If you would
not close it, name the one measurement that would let you.

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
