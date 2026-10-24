# PASS-3 -- the SCOPED REVIEW of round `#569`'s REPAIR DIFF (ledger row `m88kscaledbyte`, GXemul hardened fork)

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated
wrongly.  **Check the premises, not just the derivations.**  Where I state something as
fact, ask whether it is true.  A seat that re-derives a premise from something this brief
did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.**  There are THREE pristine-2021-upstream
copies of GXemul under the project root (`./src/` and two under
`_archive/audit-results-*/builds/`).  They are NOT this fork.  If your line numbers
disagree with mine by hundreds you are reading one of them — say so rather than
reconciling.

**If you cannot read files that is expected** — every fact you need is inlined.  Name any
premise you cannot settle from this packet rather than guessing at it.

**Where this brief states an ARITHMETIC claim — an index range, an offset, a count of
reachable addresses — ENUMERATE it rather than reasoning about it.**  Walk the values.
A derivation that skips one masking line reads exactly like a correct one.

**And ENUMERATE THE RIGHT DOMAIN — a domain is itself a premise.**  Ask what the PRODUCER of
these values can actually emit before you walk them.  Walking every member of a set you have
not audited is not enumeration; it is a derivation with more steps, and it reads exactly like
a correct one.

**VERDICT LINE FIRST**, so your answer survives truncation.

---

## 0. What this pass is, and how to answer

Pass 2 (`regress/artifacts/m88kscaledbyte/pass2_20261023/`) reviewed round `#569`'s diff and GPT-6 Astra adjudicated it
(`pass2_20261023/f2/codex_t1f2.txt`: SHIP WITH THE NAMED REPAIRS).  The named repairs were then MADE and MEASURED
(`regress/artifacts/m88kscaledbyte/repair1_20261023/`).  Under the project's repair-chain rule a repair made in response to a
pass 2 owes its own scoped pass: **review EFFORT is scoped to the repair diff (section 2); the FLOOR QUESTION -- does any
edit inside the detector's contract keep every one of its 123 rows green -- is asked of the SHIPPED COMPOSITE.**  The chain
closes on the first VALID pass that finds zero breaches: the delivered diff inspected, roster absences named, the
cells/shapes inspected stated.  This packet is self-contained (packet-fed seats: READ / REASONED / NOT CHECKABLE per claim;
nothing here asks you to read files).  The tree under review is `GXEMUL-SEC/`; the round's fix (the generator's NULL arm
removed, the table regenerated, the 123-row driver) is NOT re-litigated -- only the repair diff and the composite floor.

VERDICT LINE FIRST: `VERDICT: <CLOSE | REPAIR AGAIN | DO NOT SHIP> -- <one sentence>`; then Q1-Q5 one line each; then
your reasoning.  CLOSE means: zero breaches found, with the denominator stated (which cells and shapes you inspected).

## 1. What commanded the repair -- GPT-6 Astra's F2 ruling, VERBATIM excerpts (`pass2_20261023/f2/codex_t1f2.txt`)

```text
VERDICT: SHIP WITH THE NAMED REPAIRS -- The table repair and detector are supported by the recorded measurements, but compiler integration, comment and record corrections, and a valid scoped repair pass remain owed before landing.

F1 AMEND: Require the repaired staged-gate measurement; 485 remains derived until observed, and swapping one file does not create a clean tree.  
F2 UPHOLD: Move immediately after compiler selection, pass `CC`, and repair the standalone fallback.  
F3 UPHOLD: Correct the generator’s consumer claim; retain all 24 pins.  
...
F9 AMEND: The reread resolves the condition—the gate comment does not assert that all 24 slots have consumers.  
F14 UPHOLD: Reject “closed”; retain the documented Fable hold.  
F15 AMEND: The roster correction is present, but its manifest checksum is stale.  
F20 AMEND: Clarify the index notation consistently; do not append the proposed contradictory explanation.  
F23 AMEND: The gate reword is optional clarification, not an established second L4 breach.  
F24 AMEND: Separate loss of detector discrimination from deletion of its wiring.  
...
**Q2. In-round repairs and their closing passes.**

| Repair | Licence and scoped pass | Stop condition |
|---|---|---|
| R1/R2, with R5 validation | **L1.** Inspect the delivered gate move, explicit `CC`, and standalone fallback across cc, gcc-only, neither compiler, explicit override, and compiler-present/unconfigured-tree cases. Record one repaired staged-gate run. | Correct control flow, unchanged 123 detector identities/126 successful-path gate checks, and a completed green receipt for the repaired gate. |
| Generator consumer comment | **L4.** Read the corrected wording against the actual consumers; verify the diff changes no output-generating behavior. | No false reachability claim; all 24 generator-output cells remain required. |
| Driver index explanation | **L4 clarification.** Review the replacement notation against generator flag values and loop order. | One unambiguous formula consistent with the existing indices; no row changes. |
| Landing records and stale manifest | **L4 and existing landing obligations.** Review tree descriptions, witness/hold records, filings, artifact inclusion, refreshed manifest, executable mode, and committed gate identity. | Accurate records, matching hashes, and the required landing attestations. |

The correct insertion point is after compiler selection and before `need_file`: the current staged file selects `CC` at line 230 and can skip for an unconfigured tree at line 238. Thus the earlier “before #412” proposal would unnecessarily suppress this compiler-only detector. See [staged gate:228](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/m88kscaledbyte/table1_20261022/staged/gate_offline.sh:228).

R3’s proposed verification is insufficient: rows that do not observe comments cannot validate a comment’s truth. Replace that claim in [repair_proposal.md:81](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/m88kscaledbyte/pass2_20261023/f2/repair_proposal.md:81) with the source-reading check above. Carry the generator comment correction into the required source mirrors; A5 still requires matching source copies. See [PASS1_RULINGS.md:29](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/m88kscaledbyte/pass1_20261022/PASS1_RULINGS.md:29).

Each repair closes on its **first valid zero-breach pass**: inspect the actual delivered diff, name roster absences, state the cells/shapes inspected, and apply the existing floor question to the composite. This does not authorize another unrestricted ask-again. See [pass-2 packet:2984](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/m88kscaledbyte/pass2_20261023/packet.md:2984).

**Filed:** the wiring gap, the separate future discrimination-loss gap, and the already-owed C1/C2 findings. No present L2 breach or missing L3 detector row was established. Neither a recurring mutation lane nor a driver hash pin becomes mandatory merely because it could strengthen future checks.
...
**Q4. Decisive corrections and completed verifications.**

**The comment disagreement is settled by the text.** The generator explicitly says “them,” referring to the 24 slots. The gate instead says the **table** is indexed unchecked, followed by singular “calls the slot” and “installs it.” Grok’s claim that both comments say “them” is inaccurate. Compare [generator:254](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/cpus/generate_m88k_loadstore.c:254) with [staged gate:75](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/m88kscaledbyte/table1_20261022/staged/gate_offline.sh:75). GLM’s distinction is supported; “two readers” does not overturn it.

The source establishes twelve sync decoder consumers and four plain nosync xmem consumers. The remaining eight are `424, 440, 480, 484, 488, 496, 500, 504`. The relevant indexing and upstream rejection appear at [cpu_m88k_instr.c:2377](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/cpus/cpu_m88k_instr.c:2377), [2411](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/cpus/cpu_m88k_instr.c:2411), and [3606](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/cpus/cpu_m88k_instr.c:3606). All 24 remain floor cells because the generator emits them.

**F20’s proposed repair needs repair.** The driver actually says “loop order,” not “loop variables.” Its weighted formula is valid for Boolean flags, whereas the generator variables already contain their weights. Either explicitly define Boolean flags or replace it with:

`index = no_pc_sync + registeroffset + usr + scaledness + endianness + signedness + store + size`

and identify these as the generator’s flag-valued variables. Do not leave the weighted formula beside a contradictory explanation. See [driver:119](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/diff_m88k_loadstore_gen.sh:119), [generator:221](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/cpus/generate_m88k_loadstore.c:221), and [proposal:69](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/m88kscaledbyte/pass2_20261023/f2/repair_proposal.md:69).

**F24 is the misfiled finding.** Deleting the block removes its checks; changing the comparator can preserve the block, identities, count, and sentinel while destroying discrimination. The current comparator really compares operands at [driver:103](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/diff_m88k_loadstore_gen.sh:103); the gate observes summaries and identities at [gate:91](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/gate_offline.sh:91). Extending wiring discovery to `.sh` does not check comparison semantics. Split GLM A’s finding from GLM B’s deletion finding. A hash pin detects textual drift, not continued discrimination after an accepted update.

For F19, filing follows [R16:2939](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/m88kscaledbyte/pass2_20261023/packet.md:2939). Also, deleting only the driver is already caught by the surviving block’s executable check. GLM’s precedent argument needs qualification: [diff_autodev_gen.sh:189](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/diff_autodev_gen.sh:189) does execute mutation controls on each invocation.
...
**Two record corrections remain.** The corrected roster banner is present, but [MANIFEST.md5:5](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/m88kscaledbyte/pass1_20261022/MANIFEST.md5:5) records `0735ace9fd7fcde14f96c78f2711fff7`; the current file hashes to `1e3b3b301cb66e4c7c3d1b38132cd2cd`. Refresh the manifest. F28’s eighteen outputs are explicitly sixteen v3 rows plus v1 PRE/FIX at [packet:2409](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/m88kscaledbyte/pass2_20261023/packet.md:2409); correct the attribution, not the measurement table.

Finally, R5’s gate-file swap leaves the foreign `diff_wdc_identify.c` unless separately isolated. Describe that run accurately; do not label it a clean committed-tree run. Preserve the earlier 502-check receipt and GATE 11’s stated limitations.
```

## 2. THE REPAIR DIFF -- every hunk, INLINED (the pass-2 state -> the repair; `repair1_20261023/`)

### 2.1 `src/cpus/generate_m88k_loadstore.c` -- the `#569` comment's consumer sentence (R3; comment only; the generator's OUTPUT is unchanged, see `TABLE_UNCHANGED.out` in section 3)

```diff
--- pass2_generator
+++ repair1_generator
@@ -256,9 +256,11 @@
 			    is the unscaled one, and print_function_name()
 			    already omits "_scaled" for size 0: these 24 slots
 			    name the unscaled byte handlers.  They were NULL,
-			    and xmem_slow() calls them unguarded while the
-			    ld/st decoder installs them as ic->f (both in
-			    cpu_m88k_instr.c).  */
+			    and cpu_m88k_instr.c indexes the table with no
+			    NULL check: the register-form ld/st decoder
+			    installs twelve of the slots as ic->f and
+			    xmem_slow() calls four; the other eight have no
+			    caller today and are repaired with them.  */
 
 			printf("\tm88k_instr_");
 			print_function_name(size, store, signedness,
```

### 2.2 `regress/diff_m88k_loadstore_gen.sh` -- the standalone `CC` fallback (R2), the index explanation replaced by the sum form (R4), the NOT-OBSERVED line (F25)

```diff
--- pass2_driver
+++ repair1_driver
@@ -71,7 +71,9 @@
 #  scaled doubleword names; the immediate-form byte cells; the size tests in
 #  print_function_name beyond the halfword edge; the generated DEFINITIONS
 #  beyond their count (unique names, flags, references -- the generated file
-#  is not compiled here).
+#  is not compiled here).  A name swap among UNPINNED cells (e.g. the scaled
+#  word/halfword cells not in the accept set, 185/186), made in both
+#  artifacts, keeps every row green: outside the contract.
 #
 #  (c): measured at regress/artifacts/m88kscaledbyte/table1_20261022/L3_commentgen.out
 #  (a comment-only generator: the compile row and every fresh-side row red) and
@@ -79,8 +81,9 @@
 #  .../L8_allnull.out (an all-NULL initializer) is supplementary.  SCORES.txt there.
 #
 #  Overrides, so a table of variants runs WITHOUT touching the repo:
-#  GEN=<generator source>, TABLE=<committed table>, CC=<compiler>.  Gate 2
-#  clears GEN and TABLE so it always tests the committed files.
+#  GEN=<generator source>, TABLE=<committed table>, CC=<compiler> (default cc,
+#  else gcc; gate 2 passes its own).  Gate 2 clears GEN and TABLE so it always
+#  tests the committed files.
 #
 #  Offline: a C compiler, no guest, no build tree.  Wired into gate 2.
 set -u
@@ -89,7 +92,7 @@
 SEC=$(cd "$HERE/.." && pwd)
 GEN=${GEN:-$SEC/src/cpus/generate_m88k_loadstore.c}
 TABLE=${TABLE:-$SEC/src/cpus/tmp_m88k_loadstore.c}
-CC=${CC:-cc}
+CC=${CC:-$(command -v cc >/dev/null 2>&1 && echo cc || echo gcc)}
 
 WORK=${TMPDIR:-/tmp}/gxsec-m88klsgen.$$
 #  A killed run must not reach the sentinel: the signal trap EXITS (and the exit
@@ -116,8 +119,9 @@
 
 #  index class expected-name description.  R repair with a guest consumer today,
 #  N repair with none, A accept, C counterpart (index - 32) of a repair.
-#  index = 256*no_pc_sync + 128*registeroffset + 64*usr + 32*scaledness +
-#  16*endianness + 8*signedness + 4*store + size, the generator's loop order.
+#  index = no_pc_sync + registeroffset + usr + scaledness + endianness +
+#  signedness + store + size: a SUM of the generator's flag-VALUED loop
+#  variables, each 0 or its flag (256, 128, 64, 32, 16, 8, 4), size 0..3.
 cat > "$WORK/spec" <<'EOF'
 160 R m88k_instr_ld_u_1_le_regofs scaled ld.bu le sync
 164 R m88k_instr_st_1_le_regofs scaled st.b le sync
```

### 2.3 `regress/gate_offline.sh` -- the `#569` block MOVED from after the `#375` reader to after the gate's `CC=` selection (R1): the pass-2 staged copy -> the repair's staged copy

```diff
--- pass2_staged/regress/gate_offline.sh
+++ repair1_staged/regress/gate_offline.sh
@@ -71,51 +71,6 @@
         "$([ "$(ls_entry $arr 5)" != "$(ls_entry $arr 21)" ] && echo differ || echo same)" "differ"
 done
 
-# ---- #569: the m88k load/store dispatch-table generator --------------------------
-# generate_m88k_loadstore.c printed NULL for the 24 scaled-byte slots of
-# m88k_loadstore[512], which cpu_m88k_instr.c indexes with no NULL check
-# (xmem_slow() calls the slot; the register-form ld/st decoder installs it as
-# ic->f). The fix deletes that NULL arm, so the slots name the unscaled byte
-# handlers. The driver compiles and runs the REAL generator in a scratch copy and
-# reads the COMMITTED table separately -- each alone stays green when only the
-# other is reverted -- against names hard-coded in the driver, never read from
-# either artifact. GEN and TABLE are cleared so this always tests the committed
-# files. A missing or non-compiling generator, one that fails to run, and a
-# missing table are each a red row inside the driver, never a skip.
-MLSLOG=$LOGDIR/diff_m88k_loadstore_gen.log
-if [ ! -x "$HERE/diff_m88k_loadstore_gen.sh" ]; then
-    check "m88k loadstore generator: driver is executable" "no" "yes"
-else
-    GEN= TABLE= "$HERE/diff_m88k_loadstore_gen.sh" > "$MLSLOG" 2>&1
-    sed 's/^/       /' "$MLSLOG"
-    check     "m88k loadstore generator: row failures" \
-              "$(sed -n 's/^ROWS=[0-9]* FAIL=\([0-9]*\)$/\1/p' "$MLSLOG")" "0"
-    check     "m88k loadstore generator: rows run (the denominator is the pin)" \
-              "$(sed -n 's/^ROWS=\([0-9]*\) FAIL=[0-9]*$/\1/p' "$MLSLOG")" "123"
-    check     "m88k loadstore generator: completion sentinel" \
-              "$(grep -c '^M88KLS_DONE$' "$MLSLOG")" "1"
-    #  EVERY ROW BY IDENTITY, each exactly once, from lists held HERE and not read
-    #  from the driver: a deleted, renamed or duplicated row is red by name, which
-    #  the total alone cannot say.  The lists are the driver's contract -- the 24
-    #  repaired slots; the 6 further accepts plus the 3 counterparts that are also
-    #  accepts; the other 21 counterparts -- in both artifacts, plus the generator
-    #  status rows and the cmp row: 4 + 2 x (5 + 24 + 9 + 21) + 1 = 123.
-    _mls_pin="160 164 168 176 180 184 224 228 232 240 244 248 416 420 424 432 436 440 480 484 488 496 500 504"
-    _mls_acc="161 177 418 422 434 438 144 400 404"
-    _mls_cp="128 132 136 148 152 192 196 200 208 212 216 384 388 392 408 448 452 456 464 468 472"
-    _mls_ids="gen_compiles gen_exit gen_stdout gen_count cmp_fresh_committed"
-    for _a in fresh committed; do
-        _mls_ids="$_mls_ids ${_a}_present ${_a}_inits ${_a}_entries ${_a}_nulls ${_a}_lsn"
-        for _i in $_mls_pin; do _mls_ids="$_mls_ids ${_a}_pin$_i"; done
-        for _i in $_mls_acc; do _mls_ids="$_mls_ids ${_a}_acc$_i"; done
-        for _i in $_mls_cp;  do _mls_ids="$_mls_ids ${_a}_cp$_i"; done
-    done
-    for _id in $_mls_ids; do
-        check "m88k loadstore generator: row $_id, exactly once" \
-              "$(grep -ow -- "$_id" "$MLSLOG" | wc -l | tr -d ' ')" "1"
-    done
-fi
-
 #  b1w: the pty record parser's selftest, and a POSITIVE CONTROL that proves the selftest can
 #  still catch something.  Placed BEFORE the compiler check on purpose: it needs only python3,
 #  and a machine without cc must not silently lose parser coverage as well as the
@@ -228,6 +183,54 @@
 command -v cc >/dev/null 2>&1 || command -v gcc >/dev/null 2>&1 || \
     gate_skip "no C compiler on PATH"
 CC=$(command -v cc || command -v gcc)
+
+# ---- #569: the m88k load/store dispatch-table generator --------------------------
+# generate_m88k_loadstore.c printed NULL for the 24 scaled-byte slots of
+# m88k_loadstore[512], which cpu_m88k_instr.c indexes with no NULL check
+# (xmem_slow() calls the slot; the register-form ld/st decoder installs it as
+# ic->f). The fix deletes that NULL arm, so the slots name the unscaled byte
+# handlers. The driver compiles and runs the REAL generator in a scratch copy and
+# reads the COMMITTED table separately -- each alone stays green when only the
+# other is reverted -- against names hard-coded in the driver, never read from
+# either artifact. GEN and TABLE are cleared so this always tests the committed
+# files. A missing or non-compiling generator, one that fails to run, and a
+# missing table are each a red row inside the driver, never a skip. Placed after
+# the gate's compiler detection so the driver gets `$CC`; standalone it falls
+# back to cc, then gcc.
+MLSLOG=$LOGDIR/diff_m88k_loadstore_gen.log
+if [ ! -x "$HERE/diff_m88k_loadstore_gen.sh" ]; then
+    check "m88k loadstore generator: driver is executable" "no" "yes"
+else
+    GEN= TABLE= CC="$CC" "$HERE/diff_m88k_loadstore_gen.sh" > "$MLSLOG" 2>&1
+    sed 's/^/       /' "$MLSLOG"
+    check     "m88k loadstore generator: row failures" \
+              "$(sed -n 's/^ROWS=[0-9]* FAIL=\([0-9]*\)$/\1/p' "$MLSLOG")" "0"
+    check     "m88k loadstore generator: rows run (the denominator is the pin)" \
+              "$(sed -n 's/^ROWS=\([0-9]*\) FAIL=[0-9]*$/\1/p' "$MLSLOG")" "123"
+    check     "m88k loadstore generator: completion sentinel" \
+              "$(grep -c '^M88KLS_DONE$' "$MLSLOG")" "1"
+    #  EVERY ROW BY IDENTITY, each exactly once, from lists held HERE and not read
+    #  from the driver: a deleted, renamed or duplicated row is red by name, which
+    #  the total alone cannot say.  The lists are the driver's contract -- the 24
+    #  repaired slots; the 6 further accepts plus the 3 counterparts that are also
+    #  accepts; the other 21 counterparts -- in both artifacts, plus the generator
+    #  status rows and the cmp row: 4 + 2 x (5 + 24 + 9 + 21) + 1 = 123.
+    _mls_pin="160 164 168 176 180 184 224 228 232 240 244 248 416 420 424 432 436 440 480 484 488 496 500 504"
+    _mls_acc="161 177 418 422 434 438 144 400 404"
+    _mls_cp="128 132 136 148 152 192 196 200 208 212 216 384 388 392 408 448 452 456 464 468 472"
+    _mls_ids="gen_compiles gen_exit gen_stdout gen_count cmp_fresh_committed"
+    for _a in fresh committed; do
+        _mls_ids="$_mls_ids ${_a}_present ${_a}_inits ${_a}_entries ${_a}_nulls ${_a}_lsn"
+        for _i in $_mls_pin; do _mls_ids="$_mls_ids ${_a}_pin$_i"; done
+        for _i in $_mls_acc; do _mls_ids="$_mls_ids ${_a}_acc$_i"; done
+        for _i in $_mls_cp;  do _mls_ids="$_mls_ids ${_a}_cp$_i"; done
+    done
+    for _id in $_mls_ids; do
+        check "m88k loadstore generator: row $_id, exactly once" \
+              "$(grep -ow -- "$_id" "$MLSLOG" | wc -l | tr -d ' ')" "1"
+    done
+fi
+
 need_file "$HERE/diff_ieee_store.c" "$SEC/src/$SRC"
 
 # Pick a configured tree: it must have the generated config.h AND the header directory.
```

### 2.4 `regress/gate_offline.sh` -- HEAD -> the repair's staged copy (what will be COMMITTED): one hunk, the block at its new place

```diff
--- HEAD/regress/gate_offline.sh
+++ repair1_staged/regress/gate_offline.sh
@@ -183,6 +183,54 @@
 command -v cc >/dev/null 2>&1 || command -v gcc >/dev/null 2>&1 || \
     gate_skip "no C compiler on PATH"
 CC=$(command -v cc || command -v gcc)
+
+# ---- #569: the m88k load/store dispatch-table generator --------------------------
+# generate_m88k_loadstore.c printed NULL for the 24 scaled-byte slots of
+# m88k_loadstore[512], which cpu_m88k_instr.c indexes with no NULL check
+# (xmem_slow() calls the slot; the register-form ld/st decoder installs it as
+# ic->f). The fix deletes that NULL arm, so the slots name the unscaled byte
+# handlers. The driver compiles and runs the REAL generator in a scratch copy and
+# reads the COMMITTED table separately -- each alone stays green when only the
+# other is reverted -- against names hard-coded in the driver, never read from
+# either artifact. GEN and TABLE are cleared so this always tests the committed
+# files. A missing or non-compiling generator, one that fails to run, and a
+# missing table are each a red row inside the driver, never a skip. Placed after
+# the gate's compiler detection so the driver gets `$CC`; standalone it falls
+# back to cc, then gcc.
+MLSLOG=$LOGDIR/diff_m88k_loadstore_gen.log
+if [ ! -x "$HERE/diff_m88k_loadstore_gen.sh" ]; then
+    check "m88k loadstore generator: driver is executable" "no" "yes"
+else
+    GEN= TABLE= CC="$CC" "$HERE/diff_m88k_loadstore_gen.sh" > "$MLSLOG" 2>&1
+    sed 's/^/       /' "$MLSLOG"
+    check     "m88k loadstore generator: row failures" \
+              "$(sed -n 's/^ROWS=[0-9]* FAIL=\([0-9]*\)$/\1/p' "$MLSLOG")" "0"
+    check     "m88k loadstore generator: rows run (the denominator is the pin)" \
+              "$(sed -n 's/^ROWS=\([0-9]*\) FAIL=[0-9]*$/\1/p' "$MLSLOG")" "123"
+    check     "m88k loadstore generator: completion sentinel" \
+              "$(grep -c '^M88KLS_DONE$' "$MLSLOG")" "1"
+    #  EVERY ROW BY IDENTITY, each exactly once, from lists held HERE and not read
+    #  from the driver: a deleted, renamed or duplicated row is red by name, which
+    #  the total alone cannot say.  The lists are the driver's contract -- the 24
+    #  repaired slots; the 6 further accepts plus the 3 counterparts that are also
+    #  accepts; the other 21 counterparts -- in both artifacts, plus the generator
+    #  status rows and the cmp row: 4 + 2 x (5 + 24 + 9 + 21) + 1 = 123.
+    _mls_pin="160 164 168 176 180 184 224 228 232 240 244 248 416 420 424 432 436 440 480 484 488 496 500 504"
+    _mls_acc="161 177 418 422 434 438 144 400 404"
+    _mls_cp="128 132 136 148 152 192 196 200 208 212 216 384 388 392 408 448 452 456 464 468 472"
+    _mls_ids="gen_compiles gen_exit gen_stdout gen_count cmp_fresh_committed"
+    for _a in fresh committed; do
+        _mls_ids="$_mls_ids ${_a}_present ${_a}_inits ${_a}_entries ${_a}_nulls ${_a}_lsn"
+        for _i in $_mls_pin; do _mls_ids="$_mls_ids ${_a}_pin$_i"; done
+        for _i in $_mls_acc; do _mls_ids="$_mls_ids ${_a}_acc$_i"; done
+        for _i in $_mls_cp;  do _mls_ids="$_mls_ids ${_a}_cp$_i"; done
+    done
+    for _id in $_mls_ids; do
+        check "m88k loadstore generator: row $_id, exactly once" \
+              "$(grep -ow -- "$_id" "$MLSLOG" | wc -l | tr -d ' ')" "1"
+    done
+fi
+
 need_file "$HERE/diff_ieee_store.c" "$SEC/src/$SRC"
 
 # Pick a configured tree: it must have the generated config.h AND the header directory.
```

## 3. THE MEASUREMENTS (VERBATIM; `regress/artifacts/m88kscaledbyte/repair1_20261023/`)

### 3.1 `REPAIR_REPORT.md` (whole)

```text
# `#569` repair pass (R1-R5 + F25) -- the builder's report (2026-10-23; HEAD `5986c137`, unchanged throughout)

Spec: `pass2_20261023/f2/REPAIR_SPEC.md`, with its header amendments applied over section 1; the edits as amended in
`f2/repair_proposal.md`; the ruling is `f2/codex_t1f2.txt` (GPT-6 Astra: SHIP WITH THE NAMED REPAIRS).  Same sandbox
as BUILD_SPEC section 0: no git write, nothing under `tools/`, no peer file, `diff_wdc_identify.c` untouched.  Every
number below names the file that holds it.  The scoped pass on this repair diff (spec section 3) is the main loop's.

## 1. What was done, in order (2026-10-23)
| time | step | receipt |
|---|---|---|
| 11:44 | pre-check: the four round files equal pass 2's (same md5s), HEAD `5986c137`, nothing running | -- |
| 11:45 | the consumers read and enumerated BEFORE the wording was chosen | `R3_SOURCE_READING.out` |
| 11:45 | **R3**: the generator's `#569` consumer sentence reworded (comment only) | `generator_r3.diff` |
| 11:46 | the repaired generator compiled and run in `/tmp/gxt1/repair`: its output == the committed table | `TABLE_UNCHANGED.out` |
| 11:47 | **R2, R4, F25** in the driver | `driver_r1.diff` |
| 11:47 | **R1**: the block moved in the working-tree file; the new staged copy built from a fresh HEAD read | `staged/` |
| 11:48 | **M1**: the driver on the repo defaults; R2's compiler selection measured | `M1.out`, `fixed_r1.out`, `M1_cc_cases.out`, `cc_*.out` |
| 11:51-11:54 | **M2 (= R5)**: GATE 2 with the staged gate swapped in, then restored | `GATE2_committedform_tail.out`, `wt_gate_offline.sh.bak` |
| 11:55-11:58 | **M3**: GATE 2 on the working tree | `GATE2_wt_tail.out` |
| 11:58-12:02 | **M4**: propagation; `build/`, `build-asan/`, `/tmp/gxsec-build` rebuilt one at a time; clearance re-run | `CLEARANCE_r1.out` |
| 12:03 | F25's disclosure measured, supplementary | `F25.out` |

## 2. Diff stat (plain `diff` against `git show HEAD:<file>`; all LF)
| file | HEAD -> now | the repair's own delta (pass 2 -> now) |
|---|---|---|
| `src/cpus/generate_m88k_loadstore.c` | +10 -4 (working tree) | +5 -3 (R3, a comment) |
| `src/cpus/tmp_m88k_loadstore.c` | +24 -24 (working tree) | none (`TABLE_UNCHANGED.out`) |
| `regress/diff_m88k_loadstore_gen.sh` (new) | +280 -0 (working tree) | +10 -6 (R2, R4, F25) |
| `regress/gate_offline.sh` | +48 -0 (HEAD -> `repair1_20261023/staged/gate_offline.sh`) | +48 -45 (the move; `staged/move_staged.diff`, `staged/move_WT.diff`) |

`diff HEAD-blob staged` is ONE hunk, `185a186,233` (unified: `@@ -183,6 +183,54 @@`): **N = 48**, at `:185/186`
(`staged/insert_HEAD.diff`).  The working-tree insertion (`staged/insert_WT.diff`, against the pre-#569 working tree)
is the same 48 lines at the same place, compared byte for byte; the foreign hunks are unchanged apart from the shift.
`#569` occurs exactly once in each file.  md5: generator `699b7309...`, table `d222e737...` (unchanged), driver
`7c888857...`, working-tree gate `2af22d40...`, staged gate `faebdd85...`.

## 3. The repairs
* **R1** -- the block is now between `CC=$(command -v cc || command -v gcc)` and `need_file "$HERE/diff_ieee_store.c"`.
  It is invoked as `GEN= TABLE= CC="$CC" "$HERE/diff_m88k_loadstore_gen.sh" > "$MLSLOG" 2>&1`.  Its comment gains the
  proposal's placement sentence.  Its consumer sentence is UNCHANGED, as the header amendment requires (F9/F16/F23).
  The old `table1_20261022/staged/` copy is left as pass 2's record.
* **R2** -- `CC=${CC:-$(command -v cc >/dev/null 2>&1 && echo cc || echo gcc)}`; the header's override line now reads
  `CC=<compiler> (default cc, else gcc; gate 2 passes its own)`.
* **R3** -- the generator comment now says: the register-form ld/st decoder installs twelve of the slots as ic->f and
  xmem_slow() calls four; the other eight have no caller today and are repaired with them.  It is verified by READING
  the consumers (`R3_SOURCE_READING.out`: `cpu_m88k_instr.c` `:2377`, `:2411`, `:3606`/`:3611`, `:3622`, with
  `:2359`, `:2368-2373`, `:3043`, `:3087`, `:3599-3600`, `:3655`).  The enumeration of the index expressions gives
  decoder 12 (160 164 168 176 180 184 224 228 232 240 244 248), xmem_slow 4 (416 420 432 436), immediate form 0, no
  caller 8 (424 440 480 484 488 496 500 504), no overlap: MATCHES.  All 24 stay pinned.  The table is byte-unchanged.
  The comment is propagated to `est/` and the three build trees.
* **R4** -- the weighted formula is REPLACED, not annotated: `index = no_pc_sync + registeroffset + usr + scaledness +
  endianness + signedness + store + size`, "a SUM of the generator's flag-VALUED loop variables, each 0 or its flag
  (256, 128, 64, 32, 16, 8, 4), size 0..3".  It agrees with the existing indices (160 = 128 + 32; 504 = 256 + 128 + 64
  + 32 + 16 + 8).  No row or expected name changed (M1).
* **F25** -- one disclosure in the NOT-OBSERVED paragraph: "A name swap among UNPINNED cells (e.g. the scaled
  word/halfword cells not in the accept set, 185/186), made in both artifacts, keeps every row green: outside the
  contract."  The qualifier is D-1 below, measured in `F25.out`.
* **R5** = M2.

## 4. Measurements
* **M1** (`M1.out`, `fixed_r1.out`): `ROWS=123 FAIL=0`, sentinel; **byte-identical to `table1_20261022/fixed.out`**.
  The driver prints no version or CC line; its only note lines are GEN and TABLE.  Supplementary (`M1_cc_cases.out`,
  one `cc_<case>.out` each):
  * cc present: green.
  * gcc only (no cc on PATH): green, byte-identical output.
  * neither compiler: red at `gen_compiles` (64/123), the explicit row, never a skip.
  * `CC=gcc`: green.
  * `CC=/bin/false`: red at `gen_compiles`, which shows the override is honoured.
* **M2** (`GATE2_committedform_tail.out`): `offline-differential: PASS (485 checks)`, `REGRESS_PASS`, rc 0, 179 s.
  The block's 126 checks are all ok, with 0 gate-level FAIL rows.  The working-tree file was backed up
  (`wt_gate_offline.sh.bak`, md5 `2af22d40...`), the staged copy swapped in (`faebdd85...`), and the file restored
  afterwards; `cmp` against the backup is CLEAN.  **This is NOT a clean committed-tree run.**  21 of 702 tracked
  `src/`, top-level `regress/` and `tools/` files differ from HEAD (listed in the receipt), among them the foreign
  `regress/diff_wdc_identify.c` and the peer's five `src/` files.  The receipt also lists the untracked files.  485
  equals the derived 359 + 126.  The 502 receipt from pass 2 and GATE 11's recorded limitations stand as written.
* **M3** (`GATE2_wt_tail.out`): `PASS (502 checks)`, `REGRESS_PASS`, rc 0, 171 s; 126/126.  502 = 485 + the 17 checks
  the foreign hunks add, the same count as pass 2's working-tree run.
* **M4** (`CLEARANCE_r1.out`, run 12:02:05):

  | tree | part 1, generator / table | part 2 (`gxemul -nt` each file) |
  |---|---|---|
  | `est/` | CLEAN / CLEAN | N/A (source tree, no binary) |
  | `build/` | CLEAN / CLEAN | yes / yes (11:59:20) |
  | `build-asan/` | CLEAN / CLEAN | yes / yes (12:01:18) |
  | `/tmp/gxsec-build` | CLEAN / CLEAN | yes / yes (12:01:52) |

  In each build tree make itself re-ran the generator rule once (log lines 113/113/111), and the in-tree table compares
  CLEAN against GXEMUL-SEC.  The **driver was not propagated: no tree has a `regress/` directory, `est/` included**
  (measured; listed in the receipt).  GATE 11 was not re-run, as specified.

## 5. What disagreed with the spec or a ruling (by id), and notes
* **D-1 (F25's wording).**  "made in both artifacts" was added.  A swap in one artifact alone reds the fresh ==
  committed row: `F25.out`, F25a 1/123 (table only) against F25b 0/123 (both).  The variants exist as files only
  (`F25_table.diff`, `F25_generator.diff`).
* **D-2 (M4's parenthetical).**  The spec says "the driver only exists in GXEMUL-SEC/est"; `est/` has no `regress/`
  either, so the driver exists only in GXEMUL-SEC.
* **D-3 (section 1 R3 vs the header).**  Section 1 says "the gate block's comment likewise"; the header amendment says
  the generator only.  The header was followed.
* **D-4 (R3's words).**  The proposal's original R3 text does not carry the twelve/four/eight counts that section 1's
  parenthetical asks for.  I used the proposal's AMENDED sentence (written for the gate comment), moved into the
  generator.  The exact words are in `generator_r3.diff`, for pass 3.
* **D-5 (landing, new).**  `.gitignore:33` `regress/diff_*` (re-included only for `!regress/diff_*.c`) matches the new
  driver, so `git ls-files --others --exclude-standard` does not list it and a plain `git add` refuses it.  Land it
  with `git add -f` AND mode 100755, then check `git ls-files -s` (F4/F26).  The tracked `regress/diff_autodev_gen.sh`
  (100755) sits under the same rule.
* **D-6.**  `wt_gate_offline.sh.bak` (kept as M2 requires) contains another session's uncommitted `gate_offline.sh`
  hunks.  Committing it would publish that work; that is the coordinator's call.
* **D-7.**  `make -j8`, one make job, as in the build.
* **Supplementary measurements, beyond the spec:** M1's five compiler cases and `F25.out`.
* **F28.**  The "18 outputs" are the 16 v3 outputs plus v1's PRE/FIX.  The root `table1_20261022/RUNS.log` holds only
  the 16 v3 runs.  v1's PRE/FIX are recorded in `driver_v1/prefix_HEAD.meta` and `driver_v1/fixed.meta`, and v1's ten
  legs in `driver_v1/RUNS.log`.
* **Not done here (records / landing, the main loop's):**
  * the stale `pass1_20261022/MANIFEST.md5` (F15);
  * the landing records (F7, F21, F26);
  * the filings (F13, F19, F24, C1/C2);
  * the scoped pass (spec section 3).  Its diff to inline is `generator_r3.diff`, `driver_r1.diff`,
    `staged/insert_HEAD.diff` and `staged/move_staged.diff`.

REPAIR_REPORT_DONE
```

### 3.2 `M1.out` -- the driver on the repaired repo files

```text
# M1 -- 2026-10-23 12:02:54 -0500; driver md5 7c88885772775dd6388b20cbc8953384; generator 699b7309881e997d2998044f95ad3cd9; table d222e737a0644e3b633fc1bffdb8e974
fixed_r1.out: rc 0; ROWS=123 FAIL=0; last line M88KLS_DONE
fixed_r1.out == table1_20261022/fixed.out: BYTE-IDENTICAL (the driver prints no version or CC line; its two note lines are GEN and TABLE, unchanged)
M1_DONE
```

### 3.3 `M1_cc_cases.out` -- the five compiler cases (cc; gcc only; CC=gcc; neither; CC=/bin/false)

```text
# M1_cc_cases.out -- R2 (the driver's standalone CC default) measured, 2026-10-23 12:02:54 -0500.  Each case's full
# output is cc_<case>.out.  PATH dirs under /tmp/gxt1/repair/paths hold symlinks to the tools the driver uses;
# gcconly adds gcc (+ as, ld) and NO cc; none holds no compiler.  In this environment: cc -> /usr/x86_64-pc-linux-gnu/gcc-bin/15/x86_64-pc-linux-gnu-gcc,
# gcc -> /usr/x86_64-pc-linux-gnu/gcc-bin/15/x86_64-pc-linux-gnu-gcc.
gcconly: as awk bash cat cmp cp diff dirname gcc grep head ld mkdir rm sed sh 
none:    awk bash cat cmp cp diff dirname grep head mkdir rm sed sh 

default      PATH=(inherited)    CC=unset       rc 0  ROWS=123 FAIL=0    gen_compiles: yes
gcconly      PATH=paths/gcconly  CC=unset       rc 0  ROWS=123 FAIL=0    gen_compiles: yes
nocompiler   PATH=paths/none     CC=unset       rc 1  ROWS=123 FAIL=64   gen_compiles: got=no -- the compile or link failed want=yes
override     PATH=(inherited)    CC=gcc         rc 0  ROWS=123 FAIL=0    gen_compiles: yes
overridebad  PATH=(inherited)    CC=/bin/false  rc 1  ROWS=123 FAIL=64   gen_compiles: got=no -- the compile or link failed want=yes

expected: default/gcconly/override green 123/0 (cc, gcc, gcc); nocompiler and overridebad red at gen_compiles
(the fallback names gcc, which is absent -> the explicit red row, never a skip; /bin/false proves CC is honoured)
M1_CC_DONE
```

### 3.4 `GATE2_committedform_tail.out` -- GATE 2 with the repair's STAGED gate swapped in (tail)

```text
  ok   m88k loadstore generator: row committed_acc400, exactly once 1
  ok   m88k loadstore generator: row committed_acc404, exactly once 1
  ok   m88k loadstore generator: row committed_cp128, exactly once 1
  ok   m88k loadstore generator: row committed_cp132, exactly once 1
  ok   m88k loadstore generator: row committed_cp136, exactly once 1
  ok   m88k loadstore generator: row committed_cp148, exactly once 1
  ok   m88k loadstore generator: row committed_cp152, exactly once 1
  ok   m88k loadstore generator: row committed_cp192, exactly once 1
  ok   m88k loadstore generator: row committed_cp196, exactly once 1
  ok   m88k loadstore generator: row committed_cp200, exactly once 1
  ok   m88k loadstore generator: row committed_cp208, exactly once 1
  ok   m88k loadstore generator: row committed_cp212, exactly once 1
  ok   m88k loadstore generator: row committed_cp216, exactly once 1
  ok   m88k loadstore generator: row committed_cp384, exactly once 1
  ok   m88k loadstore generator: row committed_cp388, exactly once 1
  ok   m88k loadstore generator: row committed_cp392, exactly once 1
  ok   m88k loadstore generator: row committed_cp408, exactly once 1
  ok   m88k loadstore generator: row committed_cp448, exactly once 1
  ok   m88k loadstore generator: row committed_cp452, exactly once 1
  ok   m88k loadstore generator: row committed_cp456, exactly once 1
  ok   m88k loadstore generator: row committed_cp464, exactly once 1
  ok   m88k loadstore generator: row committed_cp468, exactly once 1
  ok   m88k loadstore generator: row committed_cp472, exactly once 1

## the next gate line after the block
  --   compiling against configured tree: /mnt/c/DocumentNoSnc/CC/GXEMUL/build

## the closing lines (completion line, summary, verdict)
offline-differential: PASS (485 checks)
############################################################
## SUMMARY
############################################################
  PASS 2. gate_offline

  passed 1   failed 0   skipped 0
  GATE_COVERAGE=1/16 (SUBSET: 2)

REGRESS_PASS

GATE2_TAIL_DONE
```

### 3.5 `GATE2_wt_tail.out` -- GATE 2 on the working tree (tail)

```text
  ok   m88k loadstore generator: row committed_cp392, exactly once 1
  ok   m88k loadstore generator: row committed_cp408, exactly once 1
  ok   m88k loadstore generator: row committed_cp448, exactly once 1
  ok   m88k loadstore generator: row committed_cp452, exactly once 1
  ok   m88k loadstore generator: row committed_cp456, exactly once 1
  ok   m88k loadstore generator: row committed_cp464, exactly once 1
  ok   m88k loadstore generator: row committed_cp468, exactly once 1
  ok   m88k loadstore generator: row committed_cp472, exactly once 1

## the next gate line after the block
  --   compiling against configured tree: /mnt/c/DocumentNoSnc/CC/GXEMUL/build

## the closing lines (completion line, summary, verdict)
offline-differential: PASS (502 checks)
############################################################
## SUMMARY
############################################################
  PASS 2. gate_offline

  passed 1   failed 0   skipped 0
  GATE_COVERAGE=1/16 (SUBSET: 2)

REGRESS_PASS

GATE2_TAIL_DONE
```

### 3.6 `CLEARANCE_r1.out` -- the four-tree clearance after the rebuilds

```text
# CLEARANCE_r1.out -- T1 / #569 repair M4: propagation and the two-part clearance, RUN 2026-10-23 12:02:05 -0500
# part 1: cmp <tree>/<file> GXEMUL-SEC/<file>; part 2: [ <tree>/gxemul -nt <tree>/<file> ] (build trees only).
# repo: generator 699b7309881e997d2998044f95ad3cd9  table d222e737a0644e3b633fc1bffdb8e974

## the divergence set, DERIVED (grep -vE '^\s*(#|$)' tools/est_divergence.txt) -- neither file is in it:
   src/devices/.index
   src/devices/Makefile.skel
   src/devices/autodev.c
   src/devices/dev_jazz.c
   src/devices/dev_ne2000.c
   src/machines/machine_arc.c
   src/cpus/generate_m88k_loadstore.c: shared (not listed) -> the clearance applies
   src/cpus/tmp_m88k_loadstore.c: shared (not listed) -> the clearance applies

## sentinels
   /mnt/c/DocumentNoSnc/cc/GXEMUL/est: no .MUTANT
   /mnt/c/DocumentNoSnc/cc/GXEMUL/build: no .MUTANT
   /mnt/c/DocumentNoSnc/cc/GXEMUL/build-asan: no .MUTANT
   /tmp/gxsec-build: no .MUTANT

## the clearance
   est         part 1  cmp src/cpus/generate_m88k_loadstore.c   : CLEAN
   est         part 1  cmp src/cpus/tmp_m88k_loadstore.c        : CLEAN
   est         part 2  est/: source tree, part 2 N/A (no binary exists)
   build       part 1  cmp src/cpus/generate_m88k_loadstore.c   : CLEAN
   build       part 1  cmp src/cpus/tmp_m88k_loadstore.c        : CLEAN
   build       part 2  [ gxemul -nt src/cpus/generate_m88k_loadstore.c ] : yes   (gxemul 2026-10-23 11:59:20.462, file 2026-10-23 11:58:45.684)
   build       part 2  [ gxemul -nt src/cpus/tmp_m88k_loadstore.c ] : yes   (gxemul 2026-10-23 11:59:20.462, file 2026-10-23 11:59:02.246)
   build-asan  part 1  cmp src/cpus/generate_m88k_loadstore.c   : CLEAN
   build-asan  part 1  cmp src/cpus/tmp_m88k_loadstore.c        : CLEAN
   build-asan  part 2  [ gxemul -nt src/cpus/generate_m88k_loadstore.c ] : yes   (gxemul 2026-10-23 12:01:18.934, file 2026-10-23 11:59:26.002)
   build-asan  part 2  [ gxemul -nt src/cpus/tmp_m88k_loadstore.c ] : yes   (gxemul 2026-10-23 12:01:18.934, file 2026-10-23 12:00:17.835)
   gxsec-build part 1  cmp src/cpus/generate_m88k_loadstore.c   : CLEAN
   gxsec-build part 1  cmp src/cpus/tmp_m88k_loadstore.c        : CLEAN
   gxsec-build part 2  [ gxemul -nt src/cpus/generate_m88k_loadstore.c ] : yes   (gxemul 2026-10-23 12:01:52.433, file 2026-10-23 12:01:23.773)
   gxsec-build part 2  [ gxemul -nt src/cpus/tmp_m88k_loadstore.c ] : yes   (gxemul 2026-10-23 12:01:52.433, file 2026-10-23 12:01:38.930)

## did make regenerate the table IN-TREE? (dependency-driven: only when the generator binary or the template is
## newer -- here the generator source was newer, so its binary was rebuilt and the rule fired; shown, not assumed)
   build       rule ran: 1 time(s) (log line 113)   generator stderr: ./generate_m88k_loadstore: generated_functions = 198
   build-asan  rule ran: 1 time(s) (log line 113)   generator stderr: ./generate_m88k_loadstore: generated_functions = 198
   gxsec-build rule ran: 1 time(s) (log line 111)   generator stderr: ./generate_m88k_loadstore: generated_functions = 198

## the per-tree build records (copy time, make rc/wall, mtimes after make), as printed by build_tree.sh
   == est (/mnt/c/DocumentNoSnc/cc/GXEMUL/est, source tree)  start 2026-10-23 11:58:40
   copied   src/cpus/generate_m88k_loadstore.c 2026-10-23 11:58:40.263   src/cpus/tmp_m88k_loadstore.c 2026-10-23 11:58:40.275
   -- clearance (part 1: source cmp against GXEMUL-SEC; part 2: [ binary -nt source ])
      part 1  cmp est/src/cpus/generate_m88k_loadstore.c  GXEMUL-SEC/src/cpus/generate_m88k_loadstore.c : CLEAN
      part 1  cmp est/src/cpus/tmp_m88k_loadstore.c  GXEMUL-SEC/src/cpus/tmp_m88k_loadstore.c : CLEAN
      part 2  est: source tree, part 2 N/A (no binary exists)
   == est done 11:58:40

   == build (/mnt/c/DocumentNoSnc/cc/GXEMUL/build, build tree)  start 2026-10-23 11:58:45
   copied   src/cpus/generate_m88k_loadstore.c 2026-10-23 11:58:45.684   src/cpus/tmp_m88k_loadstore.c 2026-10-23 11:58:45.698
   make     rc=0  wall=35s  log lines 128  (log: scratchpad t1/build/build_r1_build.log)
            lines matching 'error' (case-insensitive): 0
            log: 39:cc -Wshadow -Wcast-align -Wstrict-aliasing -Wall  -Wextra -Wno-unused-parameter -Wno-cast-align -fstrict-aliasing -fomit-frame-pointer -fpeephole -fgnu89-inline -O3 -DNDEBUG  -I../include/    generate_m88k_loadstore.c   -o generate_m88k_loadstore
            log: 113:./generate_m88k_loadstore > tmp_m88k_loadstore.c
            log: 114:./generate_m88k_loadstore: generated_functions = 198
   after    gen-bin 2026-10-23 11:58:46.328   src/cpus/tmp_m88k_loadstore.c 2026-10-23 11:59:02.246   gxemul 2026-10-23 11:59:20.462
            cpu_m88k.o 2026-10-23 11:59:12.509
   -- clearance (part 1: source cmp against GXEMUL-SEC; part 2: [ binary -nt source ])
      part 1  cmp build/src/cpus/generate_m88k_loadstore.c  GXEMUL-SEC/src/cpus/generate_m88k_loadstore.c : CLEAN
      part 1  cmp build/src/cpus/tmp_m88k_loadstore.c  GXEMUL-SEC/src/cpus/tmp_m88k_loadstore.c : CLEAN
      part 2  [ build/gxemul -nt build/src/cpus/generate_m88k_loadstore.c ] : yes
      part 2  [ build/gxemul -nt build/src/cpus/tmp_m88k_loadstore.c ] : yes
   == build done 11:59:20

   == build-asan (/mnt/c/DocumentNoSnc/cc/GXEMUL/build-asan, build tree)  start 2026-10-23 11:59:25
   copied   src/cpus/generate_m88k_loadstore.c 2026-10-23 11:59:26.002   src/cpus/tmp_m88k_loadstore.c 2026-10-23 11:59:26.013
   make     rc=0  wall=112s  log lines 128  (log: scratchpad t1/build/build_r1_build-asan.log)
            lines matching 'error' (case-insensitive): 0
            log: 39:cc -Wshadow -Wcast-align -Wstrict-aliasing -Wall  -Wextra -Wno-unused-parameter -Wno-cast-align -fstrict-aliasing -fomit-frame-pointer -fpeephole -fgnu89-inline -O3 -DNDEBUG -fsanitize=address,undefined -fno-omit-frame-pointer -g -I../include/    generate_m88k_loadstore.c   -o generate_m88k_loadstore
            log: 113:./generate_m88k_loadstore > tmp_m88k_loadstore.c
            log: 114:./generate_m88k_loadstore: generated_functions = 198
   after    gen-bin 2026-10-23 11:59:26.634   src/cpus/tmp_m88k_loadstore.c 2026-10-23 12:00:17.835   gxemul 2026-10-23 12:01:18.934
            cpu_m88k.o 2026-10-23 12:01:06.683
   -- clearance (part 1: source cmp against GXEMUL-SEC; part 2: [ binary -nt source ])
      part 1  cmp build-asan/src/cpus/generate_m88k_loadstore.c  GXEMUL-SEC/src/cpus/generate_m88k_loadstore.c : CLEAN
      part 1  cmp build-asan/src/cpus/tmp_m88k_loadstore.c  GXEMUL-SEC/src/cpus/tmp_m88k_loadstore.c : CLEAN
      part 2  [ build-asan/gxemul -nt build-asan/src/cpus/generate_m88k_loadstore.c ] : yes
      part 2  [ build-asan/gxemul -nt build-asan/src/cpus/tmp_m88k_loadstore.c ] : yes
   == build-asan done 12:01:19

   == gxsec-build (/tmp/gxsec-build, build tree)  start 2026-10-23 12:01:23
   copied   src/cpus/generate_m88k_loadstore.c 2026-10-23 12:01:23.773   src/cpus/tmp_m88k_loadstore.c 2026-10-23 12:01:23.782
   make     rc=0  wall=29s  log lines 126  (log: scratchpad t1/build/build_r1_gxsec-build.log)
            lines matching 'error' (case-insensitive): 0
            log: 19:cc -Wshadow -Wcast-align -Wstrict-aliasing -Wall  -Wextra -Wno-unused-parameter -Wno-cast-align -fstrict-aliasing -fomit-frame-pointer -fpeephole -fgnu89-inline -O3 -DNDEBUG  -I../include/    generate_m88k_loadstore.c   -o generate_m88k_loadstore
            log: 111:./generate_m88k_loadstore > tmp_m88k_loadstore.c
            log: 112:./generate_m88k_loadstore: generated_functions = 198
   after    gen-bin 2026-10-23 12:01:24.041   src/cpus/tmp_m88k_loadstore.c 2026-10-23 12:01:38.930   gxemul 2026-10-23 12:01:52.433
            cpu_m88k.o 2026-10-23 12:01:48.269
   -- clearance (part 1: source cmp against GXEMUL-SEC; part 2: [ binary -nt source ])
      part 1  cmp gxsec-build/src/cpus/generate_m88k_loadstore.c  GXEMUL-SEC/src/cpus/generate_m88k_loadstore.c : CLEAN
      part 1  cmp gxsec-build/src/cpus/tmp_m88k_loadstore.c  GXEMUL-SEC/src/cpus/tmp_m88k_loadstore.c : CLEAN
      part 2  [ gxsec-build/gxemul -nt gxsec-build/src/cpus/generate_m88k_loadstore.c ] : yes
      part 2  [ gxsec-build/gxemul -nt gxsec-build/src/cpus/tmp_m88k_loadstore.c ] : yes
   == gxsec-build done 12:01:52

## the driver (regress/diff_m88k_loadstore_gen.sh): NOT propagated -- no tree has a regress/ directory (measured):
   /mnt/c/DocumentNoSnc/cc/GXEMUL/est: no regress/ directory
   /mnt/c/DocumentNoSnc/cc/GXEMUL/build: no regress/ directory
   /mnt/c/DocumentNoSnc/cc/GXEMUL/build-asan: no regress/ directory
   /tmp/gxsec-build: no regress/ directory
   so the driver exists only in GXEMUL-SEC/regress/ (repo md5 7c88885772775dd6388b20cbc8953384).

CLEARANCE_DONE
```

### 3.7 `TABLE_UNCHANGED.out` -- the repaired generator's output vs the committed table

```text
# TABLE_UNCHANGED.out -- T1 / #569 repair: the repaired generator's output against the committed table
# 2026-10-23 11:46:07 -0500; the generator is compiled and run in /tmp/gxt1/repair, never in the repo
generator source md5 699b7309881e997d2998044f95ad3cd9 (== repo: yes)
compile rc=0 (diagnostic lines: 0)
run rc=0; stderr: ./generate_m88k_loadstore: generated_functions = 198
fresh_R3.c md5 d222e737a0644e3b633fc1bffdb8e974  committed table md5 d222e737a0644e3b633fc1bffdb8e974
CMP: IDENTICAL -- R3 changes no generated byte; the committed table stands unchanged
TABLE_UNCHANGED_DONE
```

### 3.8 `R3_SOURCE_READING.out` -- the consumer reading behind the new comment wording

```text
# R3_SOURCE_READING.out -- T1 / #569 repair R3, 2026-10-23 11:46:06 -0500.  The adjudication's check: the
# corrected wording read against the consumers (cpu_m88k_instr.c :2377, :2411, :3606, :3622), not 'rows do not
# observe comments'.  Line numbers are the working tree's (cpu_m88k_instr.c md5 8a67c4efb3839469c1f8dcf024d39576, == HEAD's: yes).

## 1. the reworded #569 comment (generator, working tree)
   254: 			/*  #569: no NULL arm for scaled byte accesses.  A
   255: 			    byte's scale factor is 1, so a scaled byte access
   256: 			    is the unscaled one, and print_function_name()
   257: 			    already omits "_scaled" for size 0: these 24 slots
   258: 			    name the unscaled byte handlers.  They were NULL,
   259: 			    and cpu_m88k_instr.c indexes the table with no
   260: 			    NULL check: the register-form ld/st decoder
   261: 			    installs twelve of the slots as ic->f and
   262: 			    xmem_slow() calls four; the other eight have no
   263: 			    caller today and are repaired with them.  */

## 2. the consumers
-- xmem_slow: operand decode (user is iword & 0x80; the immediate form zeroes scaled and user)
   2350: 	uint32_t iword = ic->arg[0];
   2351: 	uint32_t tmp;
   2352: 	int d      = (iword >> 21) & 0x1f;
   2353: 	int s1     = (iword >> 16) & 0x1f;
   2354: 	int s2     =  iword        & 0x1f;
   2355: 	int imm16  =  iword        & 0xffff;
   2356: 	int regofs = (iword & 0xf0000000) != 0;
   2357: 	int scaled = iword & 0x200;
   2358: 	int size   = iword & 0x400;
   2359: 	int user   = iword & 0x80;
   2360: 	uint32_t pc_before_memory_access;
   2361: 	void (*xmem_load)(struct cpu*, struct m88k_instr_call*);
   2362: 	void (*xmem_store)(struct cpu*, struct m88k_instr_call*);
   2363: 	struct m88k_instr_call call;
   2364: 
   2365: 	SYNCH_PC;
   2366: 	pc_before_memory_access = (uint32_t)cpu->pc;
   2367: 
   2368: 	if (!regofs) {
   2369: 		/*  immediate offset:  */
   2370: 		scaled = 0;
   2371: 		size = (iword >> 26) & 1;
   2372: 		user = 0;
   2373: 	}
-- xmem_slow: the load index :2377 and the store index :2411 (no SIGNEDNESS; always NO_PC_SYNC)
   2377: 	xmem_load = m88k_loadstore[ (size? 2 : 0)
   2378: 	    + (cpu->byte_order == EMUL_BIG_ENDIAN? M88K_LOADSTORE_ENDIANNESS : 0)
   2379: 	    + (scaled? M88K_LOADSTORE_SCALEDNESS : 0)
   2380: 	    + (user? M88K_LOADSTORE_USR : 0)
   2381: 	    + (regofs? M88K_LOADSTORE_REGISTEROFFSET : 0)
   2382: 	    + M88K_LOADSTORE_NO_PC_SYNC ];
   2411: 	xmem_store = m88k_loadstore[ (size? 2 : 0)
   2412: 	    + M88K_LOADSTORE_STORE
   2413: 	    + (cpu->byte_order == EMUL_BIG_ENDIAN? M88K_LOADSTORE_ENDIANNESS : 0)
   2414: 	    + (scaled? M88K_LOADSTORE_SCALEDNESS : 0)
   2415: 	    + (user? M88K_LOADSTORE_USR : 0)
   2416: 	    + (regofs? M88K_LOADSTORE_REGISTEROFFSET : 0)
   2417: 	    + M88K_LOADSTORE_NO_PC_SYNC ];
-- the immediate-form xmem is installed at :3043; the immediate-form ld/st index :3087 has no SCALEDNESS/USR/REGOFS
   3041: 	case 0x00:
   3042: 	case 0x01:
   3043: 		ic->f = instr(xmem_slow);
   3044: 		ic->arg[0] = iword;
   3087: 			ic->f = m88k_loadstore[ opsize
   3088: 			    + (store? M88K_LOADSTORE_STORE : 0)
   3089: 			    + (signedness? M88K_LOADSTORE_SIGNEDNESS:0)
   3090: 			    + (cpu->byte_order == EMUL_BIG_ENDIAN?
   3091: 			       M88K_LOADSTORE_ENDIANNESS : 0) ];
-- the register-form decoder: op and signedness (:3565-3575), store => unsigned (:3599-3600)
   3565: 			int op = 0, opsize, user = 0, wt = 0;
   3566: 			int signedness = 1, scaled = 0;
   3567: 
   3568: 			switch (iword & 0xf000) {
   3569: 			case 0x2000: op = 1; /* st */  break;
   3570: 			case 0x3000: op = 2; /* lda */ break;
   3571: 			default:     if ((iword & 0xf800) >= 0x0800)
   3572: 					op = 0; /* ld */
   3573: 				     else
   3574: 					op = 3; /* xmem */
   3575: 			}
   3598: 				} else {
   3599: 					if (opsize >= 2 || op == 1)
   3600: 						signedness = 0;
   3601: 				}
-- :3604-3614: 0x100 -> user, 0x80 -> wt, and wt -> goto bad BEFORE any index or xmem_slow install
   3604: 			if (iword & 0x100)
   3605: 				user = 1;
   3606: 			if (iword & 0x80)
   3607: 				wt = 1;
   3608: 			if (iword & 0x200)
   3609: 				scaled = 1;
   3610: 
   3611: 			if (wt) {
   3612: 				fatal("wt bit not yet implemented! TODO\n");
   3613: 				goto bad;
   3614: 			}
-- :3620-3629: the ld/st index (REGISTEROFFSET, never NO_PC_SYNC); :3653-3656: xmem_slow installed (register form)
   3620: 			if (op == 0 || op == 1) {
   3621: 				/*  ld or st:  */
   3622: 				ic->f = m88k_loadstore[ opsize
   3623: 				    + (op==1? M88K_LOADSTORE_STORE : 0)
   3624: 				    + (signedness? M88K_LOADSTORE_SIGNEDNESS:0)
   3625: 				    + (cpu->byte_order == EMUL_BIG_ENDIAN?
   3626: 				       M88K_LOADSTORE_ENDIANNESS : 0)
   3627: 				    + (scaled? M88K_LOADSTORE_SCALEDNESS : 0)
   3628: 				    + (user? M88K_LOADSTORE_USR : 0)
   3629: 				    + M88K_LOADSTORE_REGISTEROFFSET ];
   3653: 			} else {
   3654: 				/*  xmem:  */
   3655: 				ic->f = instr(xmem_slow);
   3656: 				ic->arg[0] = iword;

## 3. the enumeration (scratchpad t1/build/r3_reading.py mirrors the index expressions above)
repaired slots (24):               160 164 168 176 180 184 224 228 232 240 244 248 416 420 424 432 436 440 480 484 488 496 500 504
register-form ld/st decoder :3622 -> 12 : 160 164 168 176 180 184 224 228 232 240 244 248
xmem_slow :2377 load / :2411 store -> 4 : 416 420 432 436
immediate-form ld/st :3087        -> 0 : -
no caller today                   -> 8 : 424 440 480 484 488 496 500 504
overlap decoder & xmem             -> none
(record only) xmem_slow if the user bit reached it (N2): adds 480 484 496 500
the comment's 'twelve ... four ... the other eight': MATCHES
exit 0

R3_READING_DONE
```

### 3.9 `F25.out` -- the unpinned-cell swap, measured in one artifact and in both

```text
# F25.out -- the driver header's new NOT-OBSERVED disclosure, measured (2026-10-23 12:03:57 -0500; driver md5 7c88885772775dd6388b20cbc8953384)
F25a  committed table only swapped at 185/186: rc 1  ROWS=123 FAIL=1  red: cmp_fresh_committed 
F25b  both artifacts swapped at 185/186:       rc 0  ROWS=123 FAIL=0  red: 
      fresh[185], fresh[186] in F25b (the generator's own output): 59 fresh rows ok; cmp row:  ok cmp_fresh_committed fresh == committed, byte for byte (cmp) identical
so: a swap among unpinned cells is invisible to every row when BOTH artifacts carry it (the disclosure), and the
fresh == committed row catches it when only one does -- hence 'made in both artifacts' in the header line.
variants: F25_table.diff, F25_generator.diff (files only)
F25_DONE
```

## 4. SETTLED PREMISES carried from pass 2 (VERBATIM) -- and the F2 dispositions F1-F28 are the ruling lines in section 1

## 5. SETTLED PREMISES -- re-inlined so nobody spends an answer re-deriving them

Copied forward from the pass-1 brief, pruned, and appended with what pass 1 and the build settled; each RE-READ IN THIS
SCOPE (the working tree over HEAD `5986c137`) by the drafter.  `cpu_m88k_instr.c`, `cpu_m88k_instr_loadstore.c`,
`cpu_dyntrans.c`, `Makefile.skel`, `regress/lib.sh`, `regress/run.sh` are byte-identical to HEAD; in the generator every
line before 254 is unchanged and every line after it moved by +4.

* **S0 -- section C0: the round is IN FLIGHT, not shipped** (section 4; this brief's `C0_OUTPUT.txt`): no CHANGELOG hit
  for `m88kscaledbyte` or `#569` at HEAD or in the working tree (HEAD's newest round block is `#568`); both src files last
  committed at the upstream import `39748e3c`; the driver and the whole `regress/artifacts/m88kscaledbyte/` are
  UNTRACKED; the ledger row is unchanged (state `open`, witness `none`, commits empty, no `entries`); HEAD's
  `regress/gate_offline.sh`, generator and table are all mode 100644; `core.fileMode=false`, `core.autocrlf=false`.
* **S1 -- the generation early return is KEPT:** `loadstore()` still returns on `if (size == 0 && scaledness)` (generator
  :104-105, untouched), so no scaled-byte handler and no size-0 `_scaled` name is generated (A2).
* **S2 -- the deleted arm and its siblings:** HEAD's table printer had four `NULL` arms -- `store && signedness`
  (:239-242), `!registeroffset && usr` (:244-247), `!registeroffset && scaledness` (:249-252), all unchanged -- and
  `size == 0 && scaledness` (HEAD :254-257), deleted whole.  MEASURED: 296 `NULL` of 512 at HEAD (BASELINE.out), split
  128 + 96 + 48 + 24 by arm (pass-1 census; PRETABLE.out section 1); 272 after the fix (FIX.out; S18a).
* **S3 -- the consumers (unchanged; 8.2):** `X(xmem_slow)` indexes the table for its load (:2377-2382) and store
  (:2411-2417) halves, ALWAYS adding NO_PC_SYNC and NEVER SIGNEDNESS, `scaled` from `iword & 0x200` (:2357), `user` from
  `iword & 0x80` (:2359), and calls both with no NULL test (:2395, :2426).  The register-form `ld`/`st` decoder installs
  the slot as `ic->f` (:3622-3629: adds SCALEDNESS and USR, never NO_PC_SYNC); a NULL `ic->f` hits `fatal("INTERNAL
  ERROR: ic->f == NULL!\n"); goto bad;` (cpu_dyntrans.c:1906-1908), which stops the CPU.  The immediate form (:3087-3091)
  never adds SCALEDNESS, USR or REGISTEROFFSET.  These four sites are the only ones (CHECKS #3).
* **S4 -- consumers of the 24 today (A6; B8 as amended by E):** 16 -- 160 164 168 176 180 184 224 228 232 240 244 248 (the
  decoder, both endians, plain and `.usr`) and 416 420 432 436 (`xmem_slow`, `ld.bu`/`st.b`, both endians).  480 484 496
  500 gain `xmem_slow` only if `m88kxmemusr` is fixed (the decoder sends bit `0x80` to `fatal("wt bit not yet
  implemented! TODO\n"); goto bad;`, :3606-3614, before `xmem_slow`; the immediate form forces `user = 0`, :2372).  424
  440 488 504: none (`xmem_slow` never adds SIGNEDNESS).  The little-endian half IS reachable (A6).  **ALL 24 ARE THE
  FLOOR** (E/B8); 16 is the guest-consumer SUBSET.
* **S5 -- the alias is the architecture:** MC88100 manual (`mc88100.txt:2961-2965`, OCR): "When the source 2 operand is
  scaled, it is shifted by 0, 1, 2, or 3 bits (multiplied by scale factor 1, 2, 4, or 8) for byte, half-word, word, or
  double-word accesses, respectively. For byte accesses, the 5UBOPCODE [SUBOPCODE] field is distinctly different from
  the register indirect with index (unscaled) cases but the result is identical."  The handlers compute
  `reg(ic->arg[1]) + LS_SIZE * reg(ic->arg[2])` under `LS_SCALED` (cpu_m88k_instr_loadstore.c:65-70), LS_SIZE 1 for a
  byte.  `print_function_name()` appends `_scaled` only `if (scaledness && size > 0)` (:80-81) and prints `_le` for every
  byte entry (:74-75), so each repaired slot prints its index-32 counterpart's existing name (12 distinct names) -- the
  idiom the table already uses for big-endian byte slots (`loadstore()` :101-102 generates no big-endian byte function).
* **S6 -- two fixed sites, both live:** the table is TRACKED, and `Makefile.skel:134-135` regenerates it only when the
  template or the generator binary is newer, so a build compiles EITHER the committed copy OR fresh output (A5; B1).
* **S7 -- the decoder is not edited** (A3).  **S8 -- the witness:** rung-3 attempt BLOCKED; witness term
  `detector:<path>` (section 2; R18).
* **S9-S15 -- the detector as ruled, inlined VERBATIM in 3.1:** shape B1/B2/B10 (the REAL generator run in a scratch
  copy, the COMMITTED table read separately, ABSOLUTE name pins hard-coded in the driver, a `cmp`; `slot[i] == slot[i-32]`
  is NOT a pin); clause (c) B6 (comment-only generator and table, "measured at"); clause (d) B7 + E (re-introduction under
  a different predicate; L5 = `grok_t1p1.txt:76` only, first difference 416; L5b supplementary; L6 = the little-endian
  half); accept B3/B9 + E (161/177 under R12, not rule D2; v6 not silent); counts B4 + E (272 supplementary; 198/198 a
  narrow suppression-count control, not definition integrity); B5 + E (explicit red for compile, exit, stdout and missing
  inputs, never `need_file`, which calls `gate_skip`); B12 + E (54 distinct pins per artifact = 24 + 24 + 6, with 144 400
  404 emitted once as accepts; 4 + 2 x (5 + 54) + 1 = **123** rows).
* **S16 -- C1 and C2 are FILED outside T1 in T1's landing** as `m88kxmemaddrovl` (MED; wrong-address access with possible
  secondary fault behaviour; unmeasured) and `m88klepsrbo` (CPU-STOP / MED; source-established; unmeasured).  Neither
  row exists yet in the ledger or OUTSTANDING_BUGS.md.
* **S17 -- propagation:** `tools/precommit_check.sh` section A compares only `src/` paths with `est/`; neither src file is
  in the derived divergence set; `est/` has no `regress/`.
* **S18 -- the drafter's own derivations (CHECK THEM; computed from the files):** (a) in HEAD's and the working tree's
  512-entry initializer exactly 24 entries differ, at 160 164 168 176 180 184 224 228 232 240 244 248 416 420 424 432
  436 440 480 484 488 496 500 504, all `NULL` at HEAD, each now equal to its index-32 entry in BOTH trees (12 distinct
  names), `NULL` 296 -> 272, the declaration at line 3738 in both; (b) all 54 expected names in the driver's spec equal
  `print_function_name()`'s rule applied to their index (0 differ); (c) the gate block's three lists equal the driver's
  classes R+N (24), A (9), C (21) and, with its 5 fixed ids, yield exactly 123 identities; (d) the 54 index->name pairs
  are identical in drivers v2 and v3; (e) GATE 2's driver log is byte-identical to `fixed.out` (md5 `5f803a73`).
* **S19 -- modes:** HEAD's `regress/gate_offline.sh` is 100644 and run by `bash` (`regress/run.sh:85`); the GATE 2 block
  EXECUTES the driver directly, so the driver needs the executable bit; the precedent `regress/diff_autodev_gen.sh` is
  committed 100755; `core.fileMode=false` here.
* **S20 -- coverage outside the block:** `tools/pipeline/check_probe_wiring.py` governs `.py` files only ("A `.sh' path
  can therefore NEVER be in the domain", :1248); GATE 2's self-variant manifest loops over `"$HERE"/diff_*.c` only
  (HEAD `gate_offline.sh:1155`).  Neither covers a `.sh` driver, the committed `diff_autodev_gen.sh` included; no `.py`
  exists under the round's artifacts directory.

---

## 5. QUESTIONS -- VERDICT LINE FIRST (format in section 0)

**Q1 THE REPAIR DIFF (section 2) -- is it exactly what the ruling commanded, and nothing else?**  (a) R1: the block now sits
between the gate's `CC=$(command -v cc || command -v gcc)` and its first `need_file`, invoked `GEN= TABLE= CC="$CC" ...`; HEAD ->
staged is ONE hunk (+48); the block's own comment gained only the placement sentence; its consumer sentence is unchanged
(the ruling: it does not over-state).  (b) R2: the driver's `CC` default is cc if present, else gcc, and the header note.
(c) R3: the generator comment's new sentence -- "the register-form ld/st decoder installs twelve of the slots as ic->f and
xmem_slow() calls four; the other eight have no caller today and are repaired with them" -- TRUE against the consumers
(`cpu_m88k_instr.c:2377`, `:2411`, `:3087`, `:3622`; the register-form decoder adds SCALEDNESS/USR, never NO_PC_SYNC;
`xmem_slow` adds NO_PC_SYNC, never SIGNEDNESS; bit 0x80 rejected as .wt at `:3606-3614`), with 12 + 4 + 8 = 24?  (d) R4: the
sum form of the index, consistent with the 54 hard-coded indices?  (e) F25: the NOT-OBSERVED line as measured in `F25.out`
(0/123 red when both artifacts swap; 1/123 when one does)?  (f) Anything in the diff beyond R1-R5 + F25?

**Q2 THE FLOOR QUESTION ON THE COMPOSITE** (the shipped generator + regenerated table + 123-row driver + the gate block as
it will be committed): name any edit INSIDE the detector's contract (the 24 repaired cells, the 9 accept cells, the 24
counterparts, the structural/status rows, the fresh-vs-committed equality, in either artifact) that keeps all 123 rows green
-- or state the cells/shapes you inspected and that none exists.  Does moving the block change any of the 123 identities or
the 126 gate checks?  Is the placement's trade-off right: a compiler-less host SKIPs gate 2 at its own `gate_skip` (as before
this round), a host WITH a compiler reds on a missing/non-compiling/non-running generator (B5)?

**Q3 THE MEASUREMENTS (section 3)** -- is each receipt what the report says: the committed-form GATE 2 run `PASS (485 checks)`
= the 2026-10-04 battery's 359 at `1329d894` + this block's 126 (the derived number OBSERVED; the run's tree described
honestly -- 21 of 702 tracked files differed from HEAD, the foreign `diff_wdc_identify.c` and the peer's five `src/` files
among them); the working-tree run 502 (= 485 + the foreign hunks' 17); the five compiler cases (three green with identical
output, two red at `gen_compiles`); the table unchanged; the clearance clean on all four trees with the binaries newer than
both sources; the driver output byte-identical to pass 2's `fixed.out`?  Is anything claimed that a receipt does not show?

**Q4 THE LANDING** -- the builder's D-5: `.gitignore:33` (`regress/diff_*`) IGNORES the new driver, so it must be added with
`git add -f` and mode 100755 (verified by `git ls-files -s` after the commit; the precedent `diff_autodev_gen.sh` is tracked
100755 under the same ignore rule).  D-6: `repair1_20261023/wt_gate_offline.sh.bak` holds ANOTHER SESSION's uncommitted gate
hunks -- the main loop will move it OUT of the artifacts dir before the commit (its md5 stays in the report) so no foreign
in-flight work lands under `#569`.  Right?  What else must the landing record for this repair (the CHANGELOG `#569` block
already names the move, the committed-form 485 and the working-tree 502 with their trees, `(c): measured at ...`, the four
filed rows)?

**Q5 ANYTHING ELSE**, with the file:line that settles it.  Roster for this pass: GLM 5.3, DeepSeek, Grok 4.7 (file-reading, the
same packet); GPT-6 Astra adjudicates; Fable 5.1 HELD by the owner; Gemini 4 Argon NOT FIRED (its transport failed four
controls today -- recorded as a seat failure, not agreement); agy/kimi/minimax/Opus-seat not on the owner's roster.
