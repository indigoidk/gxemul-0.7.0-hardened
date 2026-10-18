**Your token: `ASTRA_IP30WIRECF2_20261018`** -- open your answer with it.

# #566 -- micro-confirm of the two confirm-pass fixes

Your confirm pass raised two records flags; both are fixed.  Check ONLY that each fix is exact and adds no new false
sentence.  READ-ONLY.  The tree is `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC`.

1. `fableheldform`'s totals: `OUTSTANDING_BUGS.md` (working tree; `git diff HEAD -- OUTSTANDING_BUGS.md`, the `fableheldform` bullet) now
   reads "of the 32 fable5 entries dated since the owner's 2026-10-17 hold at HEAD `2036a3d5` (before `#566` adds two HELD
   markers), 10 are HELD markers ...", and the ledger row's state note (built by the commit from HEAD) now says "Derived
   from the ledger at HEAD 2036a3d5, before #566's two HELD markers: of the 32 fable5 entries dated since 2026-10-17 ...".
2. `15 doctored logs` -> 15 negative cases, in the CHANGELOG block and the commit message:

```diff
--- regress/artifacts/ip30abortkill/gatewire_20261018/confirm/CHANGELOG_BLOCK_draft.md	2026-10-18 14:57:41.365981800 -0500
+++ regress/artifacts/ip30abortkill/gatewire_20261018/confirm/CHANGELOG_BLOCK_final.md	2026-10-18 15:01:17.841259300 -0500
@@ -52,10 +52,10 @@
   `bf7b6af6`, the scoring text `21d7b874`; the legs ran the probe as `5bf04f2d`, before its docstring note, and it ships
   as `7fbf52ab` with an identical AST).  In the full gate an absent binary stops at `need_exec` first, a SKIP;
   `/bin/true` reaches the block.  The clone was restored to HEAD and cleared both parts (`legs/RESTORE.out`).
-* The scoring text against doctored copies of the 33/33 log (`selftest/SELFTEST.out`): 15 cases, each red where it
-  should be -- a row turned FAIL, lost, duplicated or renamed; a DEAD vehicle; an empty log; DONE removed or doubled;
-  RESULT doubled, contradicted or shrunk; CONTROL doubled or malformed; the good log under a non-zero exit status; and a
-  REAL invocation of a probe file that does not exist (python3 exits 2).
+* The scoring text against 15 negative cases (`selftest/SELFTEST.out`), each red where it should be: thirteen doctored
+  copies of the 33/33 log -- a row turned FAIL, lost, duplicated or renamed; a DEAD vehicle; an empty log; DONE removed
+  or doubled; RESULT doubled, contradicted or shrunk; CONTROL doubled or malformed -- the unchanged good log under a
+  non-zero exit status, and a REAL invocation of a probe file that does not exist (python3 exits 2).
 * Section R (`controls/R_CONTROLS.out`, on the final gate): the commit checker with the wired gate passes (77/85
   detectors run by a gate, 8 dated-exempt, 44 witnesses correctly ungated) and at `--today 2026-10-31` fails only on the
   other session's four expiries; HEAD's checker reports STALE EXEMPTION at the exec line; the exec line commented out
--- regress/artifacts/ip30abortkill/gatewire_20261018/confirm/COMMIT_MSG_draft.txt	2026-10-18 14:57:41.396603800 -0500
+++ regress/artifacts/ip30abortkill/gatewire_20261018/confirm/COMMIT_MSG_final.txt	2026-10-18 15:01:17.861506900 -0500
@@ -24,7 +24,7 @@
 binary PASS 1225 checks, the block's 41 green;
 HEAD rebuilt in a scratch clone 33/33, 41 of 41 green; HEAD with dev_sgi_ip30.c from 686d179c^
 (clause (a)) 10/33, 26 checks red, every abort site among them; /nonexistent/gxemul and /bin/true
-(clause (c)) 38 red; 15 doctored logs each red; six section R legs as required; section U PASS 35.
+(clause (c)) 38 red; 15 negative cases each red; six section R legs as required; section U PASS 35.
 
 Panel: GPT-6 Astra, Grok 4.7 and GLM 5.3 on pass 1, pass 2 and F2; {CONFIRM_LINE}.  Fable 5.1 not
 tried on pass 1 or 2 (an omission against the owner's 2026-10-17 directive), walled on F2 (HTTP 429):
```

**Format:** your token first, then ONE line `VERDICT: <n> flags -- <one line>`.  Every defect is a line starting `FLAG:`.
