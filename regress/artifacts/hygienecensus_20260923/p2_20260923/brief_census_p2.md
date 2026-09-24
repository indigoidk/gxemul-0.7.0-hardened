# hygienecensus -- PASS 2 on the diff: gate 6's readiness census re-derived by owner ruling (+ a one-word comment fix, separate commit)

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated
wrongly.  **Check the premises, not just the derivations.**  Where I state something as
fact, ask whether it is true.  A seat that re-derives a premise from something this brief
did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/`** (this round touches `regress/` and `tools/`, not
`src/` except one comment).  There are THREE pristine-2021-upstream copies of GXemul under the
project root (`./src/` and two under `_archive/audit-results-*/builds/`).  They are NOT this
fork.  If your line numbers disagree with mine by hundreds you are reading one of them — say so
rather than reconciling.

**If you cannot read files that is expected** — every fact you need is inlined.  Name any
premise you cannot settle from this packet rather than guessing at it.

**Where this brief states an ARITHMETIC claim — a count, a set, a membership — ENUMERATE it
rather than reasoning about it.**  And ENUMERATE THE RIGHT DOMAIN — ask what the PRODUCER of
these values can actually emit before you walk them.

**VERDICT LINE FIRST**, so your answer survives truncation: `VERDICT: SHIP` or
`VERDICT: DO NOT SHIP -- <reason>`.

## What this round is (plain engineering language)

`regress/gate_hygiene.sh` (gate 6 of the weekly battery) opens with a static CENSUS of the
Python probes in `regress/` that drive a guest over a pty: it counts them, lists the ones with no
prompt-readiness predicate, and counts three spellings of a readiness idiom (#392's anchored /
echo-guarded / fresh-mark form, and a "whole-buffer full-prompt" form that #392 measured failing
0/80 in one configuration).  Each count is PINNED; a new probe that moves a count without moving
its pin reds the gate.  **Several committed probes moved the counts without moving the pins, so
gate 6 was red at HEAD itself** (measured today on a pure export of HEAD's `regress/`:

    census                              got at HEAD   pinned at HEAD
    pty probes                               70            46
    promptless vs grandfathered              40            20
    anchored / echo / fresh-mark          24 / 24 / 23     23
    whole-buffer full-prompt sites            3             2
    unrecognised endswith spelling            0             0
)
and the weekly battery of 2026-09-20 failed gate 6 on seven rows.  The next battery runs
Sunday 2026-09-27 18:00 on the WORKING TREE, which also holds three UNTRACKED probes.

## §C — SETTLED PREMISES (owner rulings 2026-09-23 -- the design; do not re-open them, but DO say if the diff fails to implement them)

1. **Count every probe lying in the tree**, including the three untracked ones (`crime_width_probe.py`
   (#529), `arm_msrmode_probe.py`, `lca_isaphys_probe.py`) -- the census counts files, not commits.
2. **Grandfather** the two promptless ones (`arm_msrmode_probe.py`, `lca_isaphys_probe.py`) BY NAME.
3. **`arm_bdt_probe.py:76`**, a whole-buffer site committed 2026-09-12 (`if self.buf.rstrip().endswith("GXemul>"):`),
   is ALLOWLISTED BY NAME at pin 3 -- against the gate block's own default ("a new hit is never answered by
   raising the pin"), recorded as an exception; converting it is filed (`armbdtreadiness`).
4. **`crime_width_probe.py:956`**'s `op.endswith("P")` is re-spelled so the closed-world spelling census
   does not count it as an unrecognised readiness predicate.
5. **ONE bulk re-derivation of the pins** by `tools/derive_hygiene_pins.sh --write`, never by hand.

## Measured before this brief was written (artifacts: `GXEMUL-SEC/regress/artifacts/hygienecensus_20260923/`)

Deriver report on the tree AFTER the edits -- every census row got == pinned:

    EXPECT_BARE 0/0   EXPECT_UNKNOWN 0/0   EXPECT_PTY_PROBES 73/73   promptless 42/42
    EXPECT_CONVERTED (anchor/echo/fresh) 24/24 24/24 24/24   EXPECT_WHOLE_FULL 3/3

The gate's census rows run on COPIES of `regress/` (the pty-log half of gate 6 needs gate 4's logs and
skips there by design), three conditions -- verbatim rows:

    --- real ---
    ok   readiness: bare-prompt sites frozen (#37)            0
    ok   readiness: no unrecognised endswith spelling         0
    ok   readiness: pty-probe denominator (enumerate FIRST)   73
    ok   readiness: promptless probes, grandfathered set only 42
    ok   readiness: whole-buffer full-prompt sites (allowlist) 3
    ok   readiness: whole-buffer sites, allowlisted files     arm_bdt_probe.py arm_flags_probe.py
    ok   readiness: anchored full-prompt sites (#392)         24
    ok   readiness: echo guard present (#392)                 24
    ok   readiness: send takes a fresh mark (#392)            24
    ok   readiness: truth table keeps its 2 bad arms          2
    ok   readiness: truth table keeps its good arms + leftover demo 5
    --- move ---
    ok   readiness: bare-prompt sites frozen (#37)            0
    ok   readiness: no unrecognised endswith spelling         0
    ok   readiness: pty-probe denominator (enumerate FIRST)   73
    ok   readiness: promptless probes, grandfathered set only 42
    ok   readiness: whole-buffer full-prompt sites (allowlist) 3
    FAIL readiness: whole-buffer sites, allowlisted files     got=arm_flags_probe.py luna_absentcpu_probe.py want=arm_bdt_probe.py arm_flags_probe.py
    ok   readiness: anchored full-prompt sites (#392)         24
    ok   readiness: echo guard present (#392)                 24
    ok   readiness: send takes a fresh mark (#392)            24
    ok   readiness: truth table keeps its 2 bad arms          2
    ok   readiness: truth table keeps its good arms + leftover demo 5
    --- add ---
    ok   readiness: bare-prompt sites frozen (#37)            0
    ok   readiness: no unrecognised endswith spelling         0
    ok   readiness: pty-probe denominator (enumerate FIRST)   73
    ok   readiness: promptless probes, grandfathered set only 42
    FAIL readiness: whole-buffer full-prompt sites (allowlist) got=4 want=3
    FAIL readiness: whole-buffer sites, allowlisted files     got=arm_bdt_probe.py arm_flags_probe.py luna_absentcpu_probe.py want=arm_bdt_probe.py arm_flags_probe.py
    ok   readiness: anchored full-prompt sites (#392)         24
    ok   readiness: echo guard present (#392)                 24
    ok   readiness: send takes a fresh mark (#392)            24
    ok   readiness: truth table keeps its 2 bad arms          2
    ok   readiness: truth table keeps its good arms + leftover demo 5

(`move` = arm_bdt_probe.py's site replaced by a slice compare and one site ADDED to luna_absentcpu_probe.py: the count
stays 3, only the name row reds.  `add` = one site added, nothing removed: both rows red.)

## §F -- THE DIFF.  `git diff --numstat` for the round's files:

    41  4  regress/gate_hygiene.sh            INLINED in full below
     2  2  regress/luna_absentcpu_probe.py     INLINED (the #392 fresh-mark rename, prepared 2026-09-19)
     1  1  src/devices/dev_sgi_re.c           INLINED -- UNIT B, a SEPARATE commit (gate 8 fix)
   106  0  tools/derive_hygiene_pins.sh       NEW, untracked -- INLINED in full below
     4  1  regress/crime_width_probe.py       UNTRACKED (#529); diff vs its 2026-09-21 snapshot blob INLINED -- ships with #529, not here

```diff
diff --git a/regress/gate_hygiene.sh b/regress/gate_hygiene.sh
index 24fab1a..4659817 100644
--- a/regress/gate_hygiene.sh
+++ b/regress/gate_hygiene.sh
@@ -346,7 +346,15 @@ check "readiness: no unrecognised endswith spelling" "$unknown" "$EXPECT_UNKNOWN
 #  timeouts, no endswith( predicate).  Written into the checkpoint at the moment the
 #  witness was created, because #500 added a probe and moved NEITHER census, and it took
 #  two passes and three seats to find. ***
-EXPECT_PTY_PROBES=46
+#  *** 46 -> 73 ON 2026-09-23 BY ONE BULK RE-DERIVATION, BY OWNER RULING (hygienecensus; ledger row
+#  stateaudit0923).  The pin had sat at 46 since b78bb0f (2026-09-03) while committed pty probes grew to
+#  70, so this gate was RED AT HEAD -- measured on a pure export of HEAD's regress/, not inferred.  73 =
+#  those 70 plus THREE UNTRACKED probes that lie in the tree and are counted as they sit, because the
+#  census counts files, not commits: crime_width_probe.py (#529), arm_msrmode_probe.py (armmsrmodekill)
+#  and lca_isaphys_probe.py (#540).  The owner chose to count all three.  Consequence, stated so nobody
+#  meets it cold: until those three are committed, a FRESH CLONE counts 70 and reds this row.  Written by
+#  `tools/derive_hygiene_pins.sh --write`, never by hand. ***
+EXPECT_PTY_PROBES=73
 #  *** AND THE SAME PROBE BROKE A SECOND CENSUS IN THIS FILE, WHICH pass 11's OWN
 #  REPAIR DID NOT FIX.  Found by the codex seat reviewing that repair. ***
 #
@@ -377,7 +385,17 @@ sh_intprio_probe.py sh_iprbcd_probe.py sh_pclock_probe.py sh_tlbmulti_probe.py
 asic_badaddr_probe.py wdc_flood_probe.py gdrom_decline_probe.py
 gdrom_toclen_probe.py wdc_addtoinbuf_probe.py wdc_altoffset_probe.py
 gdrom_cond_probe.py sgi_re_width_probe.py
-sgi_de_width_probe.py sgi_re_unmapped_probe.py"
+sgi_de_width_probe.py sgi_re_unmapped_probe.py
+alpha_harness_probe.py alpha_pfnoffset_probe.py alpha_swpctx_v0_probe.py alpha_tbi_probe.py arm_bfx_width_probe.py landisk_aux_probe.py lca_badval_probe.py lca_confbus_probe.py lca_confwidth_probe.py lca_irqstub_probe.py lca_irqstub_uart_probe.py lca_isalane_probe.py lca_widewrite_probe.py maple_dmaaddr_probe.py pcc2_c040_probe.py sgi_mte_fill_probe.py sgi_re_colourdefault_probe.py sgi_re_randompixel_probe.py sgi_re_rgb_probe.py wdc_altdigin_probe.py
+arm_msrmode_probe.py lca_isaphys_probe.py"
+#  hygienecensus: the LAST TWO LINES of the list above were appended by tools/derive_hygiene_pins.sh
+#  --grandfather.  The first of them (2026-09-19): 20 promptless pty probes committed between 2026-09-05
+#  and 2026-09-18 that moved no census (b78bb0f pinned 46 probes; HEAD had 70).  Each uses a fixed-wait or
+#  drain-to-EOF session rather than a prompt predicate -- GRANDFATHERED, not converted: converting a
+#  probe's readiness is its own round.  The last (2026-09-23, OWNER RULING): arm_msrmode_probe.py
+#  (armmsrmodekill) and lca_isaphys_probe.py (#540), both UNTRACKED and lying in the tree, named here so
+#  the census can pass on the tree the weekly battery runs.  Re-derive, never hand-edit: run
+#  `bash tools/derive_hygiene_pins.sh` (report), `--grandfather NAME...`, then `--write`.
 
 #  *** THIS WAS THE THIRD POPULATION AND THE F2 EDIT MISSED IT.  Found by the agy seat
 #  on pass 2. ***  py_code and probe_code were converted to recursive-minus-artifacts
@@ -510,7 +528,12 @@ fi
 #  Committing it is the mrwstore2 lesson: that round's rung-3 probe left NO ARTEFACT, so its
 #  witness became a remembered grep and a later row had to re-cost the work.  #442's witness had
 #  the same problem and was committed one commit ago for the same reason.
-EXPECT_CONVERTED=23
+#  *** 23 -> 24 ON 2026-09-23, the same owner-ruled re-derivation.  luna_absentcpu_probe.py (committed
+#  79cd12e, 2026-09-06) is anchored and echo-guarded, so those two censuses counted it (24) -- but its
+#  send() spelled the fresh mark `mark=mark`, which the fresh-mark census does not read, so that one said
+#  23 and the three #392 counts DISAGREED at HEAD.  The probe's rename to `_mark` (same change) makes the
+#  three agree; the deriver refuses to write while they disagree, which is why the rename precedes the pin. ***
+EXPECT_CONVERTED=24
 #  One helper for all three, so they agree on WHAT they look at.  The first draft
 #  used py_code() for the anchored count and a raw grep for the other two, which
 #  meant a comment mentioning the echo guard would have inflated one count and not
@@ -566,7 +589,15 @@ conv_mark=$(probe_code 'return \(self\.\)\?wait(mark=_mark, echo=[a-z][a-z]* if
 #  at 2 turns that scope decision into a FAIL-CLOSED ALLOWLIST: those two are
 #  tolerated, a third is not, and when they are finally converted this number
 #  goes to 0 in the same commit.
-EXPECT_WHOLE_FULL=2
+#  *** 2 -> 3 ON 2026-09-23 BY OWNER RULING, AGAINST THIS BLOCK'S OWN DEFAULT -- recorded as an EXCEPTION,
+#  not a precedent.  The third site is arm_bdt_probe.py:76 (committed 4dfc716, #524, 2026-09-12): its
+#  `self.buf.rstrip().endswith("GXemul>")' raised the count to 3 in a commit that did not move this pin,
+#  so this row was red at HEAD.  The block below says a new hit is never answered by raising the pin; the
+#  owner chose to allowlist it BY NAME rather than convert it inside the census round.  Converting its
+#  readiness to #392's anchored form is FILED (`armbdtreadiness`).  A count alone would let a site MOVE
+#  between files unseen, so a second row pins the SET of files too (WHOLE_FULL_FILES, sorted). ***
+WHOLE_FULL_FILES="arm_bdt_probe.py arm_flags_probe.py"
+EXPECT_WHOLE_FULL=3
 #  *** ROW 3: SCOPED TO FILES THAT CAN DRIVE A REAL GUEST, rather than exempting a
 #  filename.  Adjudicated 2026-08-29; the name-exclusion form was WITHDRAWN. ***
 #
@@ -618,6 +649,12 @@ pty_code() { pty_driving | tr '\n' '\0' \
              | xargs -0 grep -h "$1" 2>/dev/null | grep -v '^[[:space:]]*#'; }
 whole_full=$(pty_code 'buf.rstrip().endswith("GXemul>")' | grep -c .)
 check "readiness: whole-buffer full-prompt sites (allowlist)" "$whole_full" "$EXPECT_WHOLE_FULL"
+#  hygienecensus 2026-09-23: the allowlist BY NAME -- the files holding a CODE (non-comment) whole-buffer
+#  site, over the same pty-driving population as the count above, sorted and space-joined.
+whole_files=$(pty_driving | while IFS= read -r f; do
+                  n=$(grep -h 'buf.rstrip().endswith("GXemul>")' "$f" 2>/dev/null | grep -v '^[[:space:]]*#' | grep -c .)
+                  [ "$n" -gt 0 ] && basename "$f"; done | sort | tr '\n' ' ' | sed 's/ $//')
+check "readiness: whole-buffer sites, allowlisted files" "$whole_files" "$WHOLE_FULL_FILES"
 check "readiness: anchored full-prompt sites (#392)" "$conv_anchor" "$EXPECT_CONVERTED"
 check "readiness: echo guard present (#392)"         "$conv_echo"   "$EXPECT_CONVERTED"
 check "readiness: send takes a fresh mark (#392)"    "$conv_mark"   "$EXPECT_CONVERTED"
diff --git a/regress/luna_absentcpu_probe.py b/regress/luna_absentcpu_probe.py
index fb868e0..0583b3c 100644
--- a/regress/luna_absentcpu_probe.py
+++ b/regress/luna_absentcpu_probe.py
@@ -213,7 +213,7 @@ class Sess:
 
     def send(self, x, timeout=60):
         b = (x + "\n").encode("latin1")
-        mark = len(self.buf)
+        _mark = len(self.buf)   # #hygienecensus: `_mark`, the spelling gate 6's fresh-mark census counts
         n = 0
         try:
             while n < len(b):
@@ -221,7 +221,7 @@ class Sess:
         except OSError:
             self.dead = True
             return False
-        return self.wait(mark=mark, echo=x if x else None, timeout=timeout)
+        return self.wait(mark=_mark, echo=x if x else None, timeout=timeout)
 
     def reg(self, name, cpu=None, cr=False):
         """Read GPR/pc (`reg [cpu]') or a control register (`reg [cpu],c')."""
diff --git a/src/devices/dev_sgi_re.c b/src/devices/dev_sgi_re.c
index 8e9727d..2eff307 100644
--- a/src/devices/dev_sgi_re.c
+++ b/src/devices/dev_sgi_re.c
@@ -507,7 +507,7 @@ DEVICE_ACCESS(sgi_re)
 			 *  #513: ACCEPT.  A guest read of a len == 8 TLB slot ended
 			 *  the host.  The write arm directly above already computes
 			 *  and stores the value, so the disposition is member 4 of
-			 *  the option set -- delete the kill and RETURN THE VALUE --
+			 *  the option set -- remove the kill and RETURN THE VALUE --
 			 *  rather than a decline: nothing is unimplemented here.
 			 *  This loop is the exact inverse of the write loop, cell for
 			 *  cell and shift for shift.
```

### `regress/crime_width_probe.py` (untracked; diff against the 2026-09-21 snapshot blob of this file)

```diff
@@ -953,7 +953,10 @@
 
 def accept(A, op, off, val, reg="a0"):
     """one ACCEPTED access of ACCEPTS; the `P' kinds run from pc 0xbfc05180, the REV arm's redirect window (pc = ra)"""
-    if op.endswith("P"):
+    #  hygienecensus (2026-09-23, owner ruling): spelled `op[-1:] == "P"', not `op.endswith("P")' -- identical for a str
+    #  (both False on ""), but gate_hygiene's census is CLOSED-WORLD over `endswith(' and counts any unrecognised
+    #  spelling as a readiness predicate it cannot classify (it read got=1 want=0 on this line at the 2026-09-20 battery).
+    if op[-1:] == "P":
         if op[0] == "s":
             x, _ = st(A, op[:2], CRIME + off, val, at=PROBE_PC)
         else:
```

### `tools/derive_hygiene_pins.sh` (NEW, 106 lines, full text)

```bash
#!/bin/bash
#  derive_hygiene_pins.sh -- re-derive gate_hygiene.sh's census pins FROM THE GATE'S OWN ENUMERATORS, instead of
#  hand-editing numbers.  (hygienecensus, 2026-09-19: EXPECT_PTY_PROBES sat at 46 while 24 pty probes were committed
#  over two weeks, and nothing said so until a pre-flight read of the weekly battery.)
#
#  It does NOT re-implement the counting.  It extracts the gate's own enumerator functions (py_code, probe_code,
#  pty_driving, pty_code) and assignment lines (bare/allends/full, _ptylist/_ptyn/_promptless, conv_*, whole_full)
#  out of gate_hygiene.sh by name and evaluates them -- so an edit to how the gate counts flows into the deriver.
#  An enumerator it cannot find is a hard error, never a zero.
#
#    derive_hygiene_pins.sh                 report: got vs pinned, per census, and any NEW promptless probe by name
#    derive_hygiene_pins.sh --write         rewrite EXPECT_BARE/UNKNOWN/PTY_PROBES/CONVERTED/WHOLE_FULL in place
#    derive_hygiene_pins.sh --grandfather F [F...]
#                                           append the NAMED files to GRANDFATHERED_PROMPTLESS (deliberate, never bulk)
#
#  Refusals, each with its reason printed: the three #392 counts (anchor, echo, fresh mark) share ONE pin, so --write
#  refuses while they disagree (the disagreement IS a defect: a guard present but uncounted); --write refuses while a
#  promptless probe is neither grandfathered nor given prompt detection (the gate's own rule); EXPECT_BARE is never
#  raised (a bare `endswith(">")` is a defect the gate freezes at its pin).
#
#  Run it from anywhere; HERE is the regress directory beside this script's tools/ directory ($GXROOT overrides).
set -u
PY=""; for c in python3 python; do "$c" -c "import sys" >/dev/null 2>&1 && { PY=$c; break; }; done   # RUN it: a Windows Store stub exists and fails
[ -n "$PY" ] || { echo "DERIVE_FAIL: no working python"; exit 2; }
ROOT=${GXROOT:-$(cd "$(dirname "$0")/../.." && pwd)}
HERE="$ROOT/GXEMUL-SEC/regress"
[ -d "$HERE" ] || HERE="$(cd "$(dirname "$0")/../regress" 2>/dev/null && pwd)"
G="$HERE/gate_hygiene.sh"
[ -f "$G" ] || { echo "DERIVE_FAIL: no gate_hygiene.sh at $G"; exit 2; }
MODE=report; GF=()
case "${1:-}" in --write) MODE=write ;; --grandfather) MODE=grandfather; shift; GF=("$@") ;; "") ;; *) echo "usage: $0 [--write | --grandfather FILE...]"; exit 2 ;; esac

fn() {  # extract a shell function definition by name: from `name() {` through the first line ending in `}`
    awk -v n="$1" 'index($0, n "() {")==1 {p=1} p {print} p && /}[[:space:]]*$/ {exit}' "$G"
}
asg() { # extract an assignment by variable name: continue while the line ends in a backslash OR a single quote is
        # still open (the gate writes `tr ' ' '<newline>'` with a LITERAL newline inside the quotes)
    awk -v n="$1" 'index($0, n "=")==1 {p=1}
        p {print; q += gsub(/\047/, "\047"); if ($0 !~ /\\$/ && q % 2 == 0) exit}' "$G"
}
CODE=""
for f in py_code probe_code pty_driving pty_code; do
    d=$(fn $f); [ -n "$d" ] || { echo "DERIVE_FAIL: enumerator $f() not found in gate_hygiene.sh"; exit 3; }
    CODE="$CODE$d"$'\n'
done
for v in bare allends full unknown _ptylist _ptyn _promptless conv_anchor conv_echo conv_mark whole_full; do
    a=$(asg $v); [ -n "$a" ] || { echo "DERIVE_FAIL: assignment $v= not found in gate_hygiene.sh"; exit 3; }
    CODE="$CODE$a"$'\n'
done
GP=$(awk 'index($0,"GRANDFATHERED_PROMPTLESS=")==1 {p=1} p {print} p && /"[[:space:]]*$/ && NR>1 && !/^GRANDFATHERED_PROMPTLESS="[^"]*$/ {exit}' "$G")
eval "$GP"
eval "$CODE"

pin() { sed -n "s/^$1=\([0-9]*\).*/\1/p" "$G" | head -1; }
_want=$(printf '%s' "$GRANDFATHERED_PROMPTLESS" | tr ' ' '\n' | grep -c .)
_got=$(printf '%s' "$_promptless" | grep -c .)
NEWP=$(comm -13 <(printf '%s' "$GRANDFATHERED_PROMPTLESS" | tr ' ' '\n' | grep . | sort) <(printf '%s' "$_promptless" | grep . | sort))
GONE=$(comm -23 <(printf '%s' "$GRANDFATHERED_PROMPTLESS" | tr ' ' '\n' | grep . | sort) <(printf '%s' "$_promptless" | grep . | sort))
UNTR=$(cd "$HERE" && printf '%s\n' $_ptylist | while read -r f; do p=$(find . -name "$f" ! -path './artifacts/*' | head -1); git -C "$HERE" ls-files --error-unmatch "$p" >/dev/null 2>&1 || echo "$f"; done)

printf '%-34s %6s %6s\n' census got pinned
printf '%-34s %6s %6s\n' EXPECT_BARE "$bare" "$(pin EXPECT_BARE)"
printf '%-34s %6s %6s\n' EXPECT_UNKNOWN "$unknown" "$(pin EXPECT_UNKNOWN)"
printf '%-34s %6s %6s\n' EXPECT_PTY_PROBES "$_ptyn" "$(pin EXPECT_PTY_PROBES)"
printf '%-34s %6s %6s\n' "promptless vs GRANDFATHERED" "$_got" "$_want"
printf '%-34s %6s %6s\n' "EXPECT_CONVERTED (anchor)" "$conv_anchor" "$(pin EXPECT_CONVERTED)"
printf '%-34s %6s %6s\n' "EXPECT_CONVERTED (echo)" "$conv_echo" "$(pin EXPECT_CONVERTED)"
printf '%-34s %6s %6s\n' "EXPECT_CONVERTED (fresh mark)" "$conv_mark" "$(pin EXPECT_CONVERTED)"
printf '%-34s %6s %6s\n' EXPECT_WHOLE_FULL "$whole_full" "$(pin EXPECT_WHOLE_FULL)"
[ -n "$NEWP" ] && { echo "NEW PROMPTLESS (neither grandfathered nor prompt-detecting):"; printf '  %s\n' $NEWP; }
[ -n "$GONE" ] && { echo "GRANDFATHERED BUT NO LONGER PROMPTLESS (remove from the list):"; printf '  %s\n' $GONE; }
[ -n "$UNTR" ] && { echo "UNTRACKED files counted by these censuses (the battery counts what is lying in the tree):"; printf '  %s\n' $UNTR; }

if [ "$MODE" = grandfather ]; then
    [ ${#GF[@]} -gt 0 ] || { echo "REFUSED: --grandfather needs the file names, one by one"; exit 4; }
    for f in "${GF[@]}"; do
        printf '%s\n' $NEWP | grep -qxF "$f" || { echo "REFUSED: $f is not a NEW promptless probe"; exit 4; }
    done
    "$PY" - "$G" "${GF[@]}" <<'PY'
import io, sys
g, add = sys.argv[1], sys.argv[2:]
s = io.open(g, encoding="utf-8", newline="").read()
i = s.index('GRANDFATHERED_PROMPTLESS="'); j = s.index('"', i + len('GRANDFATHERED_PROMPTLESS="'))
s = s[:j] + "\n" + " ".join(add) + s[j:]
io.open(g, "w", encoding="utf-8", newline="").write(s)
print("GRANDFATHERED:", " ".join(add))
PY
    exit 0
fi
if [ "$MODE" = write ]; then
    [ "$conv_anchor" = "$conv_echo" ] && [ "$conv_echo" = "$conv_mark" ] || {
        echo "REFUSED: the three #392 counts disagree ($conv_anchor/$conv_echo/$conv_mark) -- a guard present but uncounted; fix the probe, not the pin"; exit 5; }
    [ -z "$NEWP" ] || { echo "REFUSED: new promptless probes must be grandfathered by NAME or given prompt detection first"; exit 5; }
    [ "$bare" -le "$(pin EXPECT_BARE)" ] || { echo "REFUSED: bare endswith(\">\") grew -- a defect, never re-pinned"; exit 5; }
    "$PY" - "$G" "$unknown" "$_ptyn" "$conv_anchor" "$whole_full" <<'PY'
import io, re, sys
g, unk, pty, conv, whole = sys.argv[1:]
s = io.open(g, encoding="utf-8", newline="").read()
for k, v in (("EXPECT_UNKNOWN", unk), ("EXPECT_PTY_PROBES", pty), ("EXPECT_CONVERTED", conv), ("EXPECT_WHOLE_FULL", whole)):
    s, n = re.subn(r"(?m)^%s=\d+" % k, "%s=%s" % (k, v), s, count=1)
    assert n == 1, k
io.open(g, "w", encoding="utf-8", newline="").write(s)
print("WRITTEN: EXPECT_UNKNOWN=%s EXPECT_PTY_PROBES=%s EXPECT_CONVERTED=%s EXPECT_WHOLE_FULL=%s" % (unk, pty, conv, whole))
PY
fi
echo "DERIVE_DONE"
```

## §E -- QUESTIONS (answer each, numbered)

**Q1 -- premise audit.**  I state these as facts; check each rather than agreeing:
 (a) the census rows are STATIC source scans, so running them on a copy of `regress/` with an empty LOGDIR
     grades exactly what the battery will grade on those rows;
 (b) `op[-1:] == "P"` behaves identically to `op.endswith("P")` for every value `op` can take in
     `crime_width_probe.py` -- check the DOMAIN of `op` (what produces it), not just the str semantics;
 (c) the deriver refuses to write while the three #392 counts disagree, and while any promptless probe is
     neither grandfathered nor prompt-detecting -- read its refusal code;
 (d) the new name-set row fails CLOSED: say what it prints if `pty_driving` returns nothing, if a path holds
     a space, if the site appears only in a comment, or if `sort` orders underscores differently under
     another locale;
 (e) 73 = 70 committed + 3 untracked, and every grandfathered name really is promptless (no `endswith(`).
**Q2 -- the smallest edit that breaks this and still passes.**  Name an edit to a probe, to
`gate_hygiene.sh`, or to the deriver that re-opens what these rows guard while every census row stays green,
and name the row you expect to stay green.  (One I suspect, unmeasured: the census patterns are
double-quoted -- does `endswith('GXemul>')` with single quotes evade both the count and the name rows?)
**Q3 -- option-set completeness.**  The owner chose allowlist-by-name over converting `arm_bdt_probe.py`'s
readiness.  Is there a member neither named -- grep the fork's other gates for an existing idiom (a
per-file companion pin, an exemption with an expiry) before answering.
**Q4 -- records.**  Is any comment added in this diff false as of today, or stale the moment it lands (the
"LAST TWO LINES" wording, the provenance of each pin, the fresh-clone consequence)?
**Q5 -- the one-word fix (separate commit).**  Is rewording the comment at `dev_sgi_re.c:510` (`delete` -> `remove`) the right fix for
gate 8's `check_delete_calls.sh` failure, rather than adding `dev_sgi_re.c` to its exceptions list?

If, while verifying a claim, you found something ELSE -- say so.

End with a seat record: model, what you read, what you ran.
