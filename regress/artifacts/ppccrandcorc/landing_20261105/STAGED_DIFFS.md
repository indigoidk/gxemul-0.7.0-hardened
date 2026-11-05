# STAGED_DIFFS.md -- what the #575 landing commits for each shared file, against HEAD and against the working copy

HEAD cbd916d1.  Built by build_staged_575.py from `git show HEAD:<path>` and the working copy.  Every hunk is printed.

## src/cpus/cpu_ppc_instr.c

HEAD 153602 bytes md5 29963c800505c1e6d949234c4d92a1fa; staged 153707 bytes md5 6efa6781b20375b984e209850277ef29; working copy 156866 bytes md5 54c9802bd12fde426372343cdbc828a8.

### staged vs HEAD (the commit's whole diff of this file: the two #575 lines)

2 hunk(s):

```
@@ replace  HEAD-side line 2735 (1 lines) -> staged-side line 2735 (1 lines)
-     if (!(ba & bb))
+     if (ba & !bb)    /*  #575: CR[BA] & ~CR[BB] (Book I); this was NAND  */
@@ replace  HEAD-side line 2762 (1 lines) -> staged-side line 2762 (1 lines)
-     if (!(ba | bb))
+     if (ba | !bb)    /*  #575: CR[BA] | ~CR[BB] (Book I); this was NOR  */
```

### staged vs the working copy (what stays uncommitted: qhslowifetch's read-failure block, 79 lines for HEAD's 4)

One hunk, at HEAD-side line 4130; the working-copy side opens `/*  #NNN: the instruction fetch failed.  This` and contains no `#575`.

## regress/gate_ppc.sh

HEAD 27688 bytes md5 0632bde42a09ffedd81da40df8c6e704; staged 31453 bytes md5 50265c7e9e8a96a2af115c3d466ead74; working copy 40138 bytes md5 616728ec6bde281a3cd16624549b2edf.  `bash -n` is run by the pretest.

### staged vs HEAD (the commit's whole diff of this file: the #575 block, 35 lines plus one blank)

1 hunk(s):

```
@@ insert  HEAD-side line 287 (0 lines) -> staged-side line 287 (36 lines)
+ # ---- ppccrandcorc (#575): crandc and crorc computed NAND and NOR -- its 70-row rung-3 detector ---------------------------------------
+ # X(crandc) and X(crorc) set CR[BT] on !(CR[BA] & CR[BB]) and !(CR[BA] | CR[BB]); PowerPC Book I v2.01 defines CR[BA] & ~CR[BB] and
+ # CR[BA] | ~CR[BB].  `-E bareppc -M 64` (PPC970) and `-C PPC603` run each CR logical instruction on a real guest through the real
+ # decoder, CR seeded from the debugger; the truth-table, edge and `hi' rows pre-set the destination to the INVERSE of the
+ # architectural result, two round-2 rows pre-set it EQUAL (the only way a BB read of CR[BT] shows), and the four round-3 rows
+ # compare the whole CR (round 3 corrected "every destination pre-set to the INVERSE": pass 3, R7); the five correct siblings run
+ # the same table as controls; edge rows pin BT 0 and 31; two rows pin the BA/BB field masks with every submask alias seeded
+ # opposite; four round-2 rows close every field mask 0..30, the BB read of CR[BT] and the read-before-clear order (the closure by
+ # simulation: regress/artifacts/ppccrandcorc/r2_20261105/CLOSURE.md, 239 cells); four round-3 whole-CR rows close the read-mask
+ # constants and the set literals (r3_20261105/CLOSURE3.md, 453 cells: 56 escaped the 66 rows; on the 70, 0 undetected beyond 36
+ # EQUIVALENT and 1 DISCLOSED -- the regress review, R1, corrected "0 escape the 70").  BEFORE the NetBSD
+ # prerequisite, like the blocks above.  Test-variant tables: regress/artifacts/ppccrandcorc/table1_20261105/, r2_20261105/ and
+ # r3_20261105/ (the pass-1 ruling: regress/artifacts/ppccrandcorc/adj_p1_20261105/).
+ CLLOG=$LOGDIR/ppc_crlogic.log
+ python3 -u ppc_crlogic_probe.py "$PMAX" gate > "$CLLOG" 2>&1 || true
+ if [ "$(grep -cx 'PPC_CRLOGIC_PROBE_DONE' "$CLLOG")" != 1 ]; then
+     note "ppc_crlogic: completion sentinel missing or duplicated; last lines follow"
+     tail -5 "$CLLOG" | sed 's/^/       /'
+     check "ppc_crlogic probe completed" "no" "yes"
+ else
+     check "ppc_crlogic probe completed" "yes" "yes"
+     check "ppc_crlogic sentinel is the last line" "$(tail -n 1 "$CLLOG")" "PPC_CRLOGIC_PROBE_DONE"
+     for k in RESULT CONTROL; do
+         check "ppc_crlogic $k= lines" "$(grep -c "^PPC_CRLOGIC_$k=" "$CLLOG")" "1"
+     done
+     check "ppc_crlogic RESULT=70/70" "$(grep -cx 'PPC_CRLOGIC_RESULT=70/70' "$CLLOG")" "1"
+     check "ppc_crlogic CONTROL=OK"   "$(grep -cx 'PPC_CRLOGIC_CONTROL=OK' "$CLLOG")" "1"
+     for v in "ctl session" "ctl live" "ctl seed holds" "ctl cr seed" "ctl mfcr" "neg apparatus" "64 session" "64 crandc 00" "64 crandc 01" "64 crandc 10" "64 crandc 11" "64 crorc 00" "64 crorc 01" "64 crorc 10" "64 crorc 11" "64 others" "64 mfcr" "64 disasm" "s64 session" "s64 crand 00" "s64 crand 01" "s64 crand 10" "s64 crand 11" "s64 cror 00" "s64 cror 01" "s64 cror 10" "s64 cror 11" "s64 crnor 00" "s64 crnor 01" "s64 crnor 10" "s64 crnor 11" "s64 creqv 00" "s64 creqv 01" "s64 creqv 10" "s64 creqv 11" "s64 crxor 00" "s64 crxor 01" "s64 crxor 10" "s64 crxor 11" "s64 others" "s64 mfcr" "s64 disasm" "edge session" "edge crandc bt0" "edge crorc bt31" "edge others" "edge mfcr" "edge disasm" "64 crandc hi" "64 crorc hi" "64 crandc bbmask" "64 crandc order" "64 crorc bamask" "64 crorc bbmask" "64 crorc baread" "64 crorc bbread" "64 crandc setbits" "64 crorc setbits" "32 session" "32 crandc 00" "32 crandc 01" "32 crandc 10" "32 crandc 11" "32 crorc 00" "32 crorc 01" "32 crorc 10" "32 crorc 11" "32 others" "32 mfcr" "32 disasm"; do
+         check "ppc_crlogic row: $v" "$(count "$CLLOG" "^$v  .*ok$")" "1"
+     done
+     clok=$(count "$CLLOG" " ok$"); clbad=$(count "$CLLOG" " FAIL$"); clrun=$((clok + clbad))
+     check "ppc_crlogic rows run"   "$clrun" 70
+     check "ppc_crlogic rows green" "$clok" 70
+     check "ppc_crlogic rows red"   "$clbad" 0
+ fi
+ 
```

### staged vs the working copy (what stays uncommitted)

3 hunk(s): qhs gate_begin title; qhs ppc_ifetch block (53 lines); the regress review's R1 comment fix, staged only (the working tree takes it from wt_gate_r1.patch).  The gate_begin title is left as HEAD's ("... + #579 llsc"): the task fixed the staged gate as HEAD's plus exactly the #575 block, and the title names no #575 in the working copy either (the Opus pass-1 seat had asked for one, Q5.3; not applied).

## tools/precommit_check.sh

HEAD md5 0b5946e4bd0f2c4580a86b5682c3d3bf; staged md5 81d10dfc8e952cbedc8412d6dc3afd9b.  The working copy (manifest 48) carries three other rounds' raises -- qhslowifetch, mvme187memcoob, pvrrenderexit -- which are NOT carried.

### staged vs HEAD

1 hunk(s):

```
@@ replace  HEAD-side line 374 (1 lines) -> staged-side line 374 (3 lines)
-     SCORE_CLAIMS_MANIFEST=45
+     #  RAISED 45 -> 46 ON 2026-11-05, DELIBERATELY.  One newly gated probe: ppc_crlogic_probe.py
+     #  (#575, pinned UNQUOTED in gate_ppc.sh at 70 rows under the stem ppc_crlogic; its docstring is checked).
+     SCORE_CLAIMS_MANIFEST=46
```

## regress/ppc_crlogic_probe.py (new file; only #575's)

Staged = the working copy with three docstring hunks (seven score-shaped strings in words); identity proof in PROBE_IDENTITY.md (full tree minus docstring equal: True; string-normalised tree equal to table 3's frozen instrument: True).

### staged vs the working copy

3 hunk(s):

```
@@ replace  HEAD-side line 35 (1 lines) -> staged-side line 35 (1 lines)
- t2).  The pre-fix build scores 52/62 (the ten DISC rows); /bin/true 5/62 and /bin/false 1/62 score CONTROL=FAIL, and an
+ t2).  The pre-fix build scores 52 of 62 (the ten DISC rows); /bin/true 5 of 62 and /bin/false 1 of 62 score CONTROL=FAIL, and an
@@ replace  HEAD-side line 46 (1 lines) -> staged-side line 46 (1 lines)
-   pre-fix build scores 56/66 (the ten DISC rows); /bin/true 5/66 and /bin/false 1/66 score CONTROL=FAIL.
+   pre-fix build scores 56 of 66 (the ten DISC rows); /bin/true 5 of 66 and /bin/false 1 of 66 score CONTROL=FAIL.
@@ replace  HEAD-side line 60 (1 lines) -> staged-side line 60 (1 lines)
-   (1) crnand (19/225) is not decoded at HEAD and stops the CPU; it is filed separately as
+   (1) crnand (opcode 19, extended opcode 225) is not decoded at HEAD and stops the CPU; it is filed separately as
```
