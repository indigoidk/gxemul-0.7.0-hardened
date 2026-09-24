# Main-loop dispositions of the Grok 4.7 review (seats/grok_verify.txt, 16,575 b, rc 0, no wall text)

Grok read files only (its shell was blocked by plan mode) and returned `VERDICT: INVENTORY HAS 7 ERRORS`.  Every claim
below was CHECKED here by a command before being accepted or rejected -- none is accepted on the seat's word.

| # | Grok's finding | check run here | disposition |
|---|---|---|---|
| G1 | A's "NO FILE WAS LOST" rests on a name-status against one snapshot; it does not show that every file the RECORDS name still exists.  The falsifier: test each cited path. | `cited_paths.py 2026-09-12` over the working-tree ledger (entries dated >= 09-12), OUTSTANDING_BUGS.md's tail and CHANGELOG.md's head -> `cited_paths_missing.txt`: **883 cited paths, 867 exist, 16 do not.**  All 16 classified by reading their context: 8 are truncated/prose/hypothetical (`panel_`, `panel_20260815_`, `panel_20260915_074x`, `regress/arm_`, `regress/diff_`, `probe188_`, `regress/dev_footbridge.c` -- a hypothetical stray file in `fbnobuild`'s scope --, `tools/pipeline/evidence` -- the filed row `evdeadarchive`, a directory never built); 1 is a spec deliberately NOT built (`regress/arm_thumbabort_probe.py`, armthumbabortkill entry [4] "DO NOT BUILD ... FROM THE SPEC"); 3 are NAME MISMATCHES (`crimewidthkill/panel_20260916_194735/{deepseek,glm,minimax}.txt` exist as `ollama_*.txt`); 2 are volatile scratch helpers (`_scratchpad/ledgeradd.py`, `recover.py`); **2 are durable copies that were PROMISED AND NEVER MADE, with the source surviving in scratch**: `regress/artifacts/n6/p1_20260919/fable5_p1_20260919.md` (MINE, #539; source `_scratchpad/n6/fable5_p1_20260919.md`) and `regress/artifacts/ip30abortkill/PROBEATTACK_grok_20260917.txt` (source `_scratchpad/grokpush_20260917/grok_ip30probeattack.txt`, 13,519 b). | **ACCEPTED -- and the falsifier, now run, does NOT falsify the claim for the cited population: no cited evidence is lost.**  The claim is re-worded to its measured scope, and the two missing durable copies become repairs R1/R2. |
| G2 | "git status (187 entries)" is not in the evidence dir. | It was measured (cmp_snapshot.sh printed `porcelain=187` before and after) but the transcript was not saved. | ACCEPTED -- `status_counts.txt` added. |
| G3 | 35 of the 47 untracked artifact dirs have no unit. | Listed each with its untracked count, its HEAD-tracked count, and which COMMITTED records cite it: **18 have ZERO tracked files yet are cited by HEAD's CHANGELOG / OUTSTANDING_BUGS / ledger** (largest: `seataudit_20260917` 38 files, cited by all three; `codex_research_20260913` 22; `panelseatlabel` 15; `armmsrmodekill` 13; `armthumbabortkill` 7; `wdcerrfamily` 4; ...); 7 are partially tracked with leftover untracked files (`wdcaltdigin` 8 of 83, `ppcrlwhighhalf` 6 of 10, `wiringcliff`, `makercfalse`, `landiskaux`, `sgirandomcolour`, `lcaconfwidth`); 10 are cited by no committed record. | **ACCEPTED, and it is the largest real exposure the review found**: committed records whose evidence is "durable in location only".  The 09-21 snapshot and today's 60b28f6 hold all of it, so nothing is lost -- but a fresh clone, or a `git clean`, would leave HEAD citing evidence that does not exist.  New unit U16 (see below). |
| G4 | The check_probe_wiring.py manifest is not all #529: five keys are the 2026-09-13 rung-3 attempts (b115, fbclearread, wdcnullxfer x2, wdcrearmzero). | 73 + 5 = 78 GHOST lines, confirmed from `checkers/check_probe_wiring.out`. | ACCEPTED. |
| G5 | U2 names the wrong blockers: the 09-20 battery log names `arm_msrmode_probe.py` and `lca_isaphys_probe.py` as the new PROMPTLESS probes, not crime_width. | `_scratchpad/nightly/battery_20260920_180002.log:1887-1893` and `tools/derive_hygiene_pins.sh` (report mode, today): NEW PROMPTLESS = arm_msrmode + lca_isaphys; UNTRACKED files the censuses count = arm_msrmode + crime_width + lca_isaphys; EXPECT_UNKNOWN got 1 = `crime_width_probe.py:956` `op.endswith("P")` (Grok's reading; consistent with the count). | ACCEPTED.  My checkpoint and INVENTORY named two of the three and mislabelled the role of one. |
| G6 | C2 overstates: the battery runs `run.sh` on the DIRTY tree, so U3 is already in effect (gate 8 should pass) and committing U2/U3 changes nothing it runs.  What fails on 09-27 is gate 6's seven checks until the pins are written, the two promptless probes are handled, and the `endswith("P")` spelling is resolved. | Read `tools/nightly_battery.sh` / `run.sh` claims against the 09-20 log: gate 8's two files are both clean now; gate 6's counts are unchanged since 09-20 (deriver above). | ACCEPTED, with one addition Grok did not weigh: `nightly_check.sh` (the dead-man switch) FAILS on TREE_DIRTY independently of the battery's verdict, so Sunday reports FAIL there unless the tree is clean. |
| G7 | U7's "pin now reads 204" is true of gate_arm.sh and false of two comments added in the same unit. | `tools/precommit_check.sh:340` "pinned UNQUOTED in gate_arm.sh at 188 rows"; the new manifest entry says "141 rows". | ACCEPTED -- two stale-number comments inside #529's uncommitted work (L4 when #529 ships). |
| Q3/M9 | U1's draft says all 49 variants are detected by the combined detector; M9's only GUEST detection is table 2 on the 36-row probe (`killtable_20260919/TABLE2.log:37`, 33/36), never re-run on the final 37-row probe (`F2_FINDINGS.md` G27 already said so); table 4 measured 327 rows, before X8. | Confirmed from the logs Grok cites. | **ACCEPTED -- a wrong record in MY draft (`cl545_draft.md`).**  Repair R3: either re-measure M9 on the final 37-row probe in a scratch clone (one build, one run) or disclose the instrument it was measured on.  The draft must not ship as written. |

## Units added / corrected by this review

* **U16 (NEW) -- untracked evidence cited by committed records.**  18 artifact directories with zero tracked files are
  cited by HEAD's CHANGELOG, OUTSTANDING_BUGS or ledger (list: `untracked_cited_dirs.txt`).  Protected today only by
  the working tree and the snapshot refs.  Not mine to stage: each belongs to its round's commit, or to a records
  round the owner schedules.
* **U7** now also carries the five non-#529 manifest keys (the 09-13 rung-3 attempt probes of b115, fbclearread,
  wdcnullxfer, wdcrearmzero) -- so committing that manifest requires FOUR other rounds' untracked artifacts too.
* **U2** blockers corrected: arm_msrmode_probe.py (U11) and lca_isaphys_probe.py (U8) are the promptless ones;
  crime_width_probe.py (U7) moves the pty / unknown-spelling counts.

## Repairs identified (NOT yet applied -- the review's evidence must stay fixed while the other seats read it)

* R1 (mine, #539): copy `_scratchpad/n6/fable5_p1_20260919.md` to the durable path the n6/fiqenableread ledger
  entries already cite, `GXEMUL-SEC/regress/artifacts/n6/p1_20260919/fable5_p1_20260919.md`.
* R2 (ip30abortkill's round): copy `_scratchpad/grokpush_20260917/grok_ip30probeattack.txt` to the cited
  `GXEMUL-SEC/regress/artifacts/ip30abortkill/PROBEATTACK_grok_20260917.txt` -- after confirming the content is the
  answer entry [15] quotes.
* R3 (mine, #545): M9 on the final instrument -- re-measure or disclose (above).
* R4 (#529's owner): the two stale-number comments (G7).
* R5 (records): the three crimewidthkill citations that drop the `ollama_` prefix.
