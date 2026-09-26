You are the DEDICATED adversarial reviewer (a separate job from the panel's grok seat) for a re-dating of eleven dated
test exemptions in a C emulator's test harness (GXemul change #550).  Read-only review.

Read `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\exemptredate_20260925\p1_brief.md` first -- it inlines
every fact, the exact three-file diff and the measurements.  The tree is `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\`;
ignore any other `src/`.

FIRST LINE: `VERDICT: <SHIP | SHIP WITH CHANGES | DO NOT SHIP>`, then numbered findings.  Push hard; agreement is worth
nothing.
1. Every reason line this diff adds: true of the tree today?  (The ip30 probe's needs, the parked ppc_rldicl repair,
   the four Alpha/LCA probes' shared missing gate, ieee_store's six inline counters.)
2. Any comment this diff leaves or edits that is now FALSE, anywhere in the three files.
3. Any path by which the gate_offline.sh change blocks a commit, or hides a red it should show.
Settle by reading the files and by arithmetic; say plainly which findings are readings.  No files may be changed.
