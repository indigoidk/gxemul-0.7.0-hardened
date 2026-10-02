# #529 closing pass 7 -- the Opus measuring seat WALLED mid-pass; this is the main loop's harvest of its artifacts

*** THE SEAT DID NOT WRITE ITS OWN REPORT.  It terminated on `You've hit your weekly limit - resets Sep 18, 3am
(America/Chicago)' (HTTP 429, model claude-opus-5, request req_011Cf5QLY29duuCPjRCAny1K) at ~09:3x on 2026-09-15, after
building and running every leg below and writing `PREDICT.md` (its own predictions, written BEFORE its builds -- its mtime
is the order proof).  A SEAT FAILURE is never agreement: its VERDICT is missing; these MEASUREMENTS survive.  The
right-hand column is the MAIN LOOP's reading, written 2026-09-16. ***

Instrument: the shipped 157-row probe, frozen as `scripts/crime_width_probe.frozen7.py`.  Clone `/tmp/gxopuscrimec7` --
checked after the wall: no `.MUTANT`, all three device sources cmp-CLEAN against GXEMUL-SEC, project trees CLEAN.

| leg | score | main loop's reading |
|---|---|---|
| base | 157/157 | the shipped instrument |
| E1_byp_ctl4r | 157/157 | CONTROL 4R silent bypass -- EQUIVALENT as item 6 says (the arm does nothing on reads; the high half is 0) |
| **E2_byp_time4** | **157/157** | TIME 4W/4R silent bypass.  Its own free-running discriminator MEASURED a guest difference: `ld; sw; ld` at +0x38 reads v0 = 0xc6 / 0x108 on base (6 of 6) and 0x0 under E2 (6 of 6) -- **a read's odata is taken BEFORE its own crime_update_crime_time(), so a skipped update arrives one read late**.  ITEM 6's "TIME 4W/4R EQUIVALENT" IS FALSE (codex said so; grok and kimi-k3 called it equivalent) |
| E3_byp_revout | 156/157 | as built it also caught the free-running refusal (`free rev said'); the corrected form is E3b |
| E3b_byp_revout_acc | 157/157 | REV out-of-window ACCEPTED cells only -- EQUIVALENT as item 6 says (the prelude rewrites REV) |
| **F1 / F1b (CONTROL 0x0201)** | **157/157** | glm's and codex's cell.  The seat's disc7b counted the CONTROL text: base 2, F1 1, F1b 1 -- so the difference is a HOST-LOG line (the arm's `fatal()' for the leftover 0x1), not a guest-visible outcome; the prelude rewrites CONTROL either way |
| F3_byp_sw04 | 157/157 | the kimi CLI seat's cell: EQUIVALENT at the guest (the store lands in REV's low lane, which the prelude rewrites); only the stepped default-arm debug WRITE line differs |
| F4a_byp_imask4r | 155/157 {imask ctl, gate line} | deepseek's claimed gap: KILLED, as predicted |
| F4b_byp_istat4r | 156/157 {istat ctl} | kimi-k3's query: KILLED |
| **K1 / K2 / K3** | **157/157 each** | the seat's OWN hunt, and the find of this pass: an accept guard keyed on the LATCH at ONE cell -- `(d->warned & CRIME_W_LEN)' && that cell -- declines SILENTLY once any refusal has happened.  Its PRE/POST discriminator measured the guest difference: after one refused `lb +0x07', K1 loses an accepted 4W to INTMASK (0x0 vs 0x1000000000000000), K2 loses the REV window redirect (pc 0xbfc05184 vs ra), K3 answers 0 for an accepted 8R of CONTROL -- while the notice count stays 1, so `latch said' and `rearm once' are both green |

**What this settles for closing pass 7: no floor gap of the announced or silent form the panel disputed** -- E1/E3b
EQUIVALENT confirmed, F4a/F4b killed, F1/F1b and F3 host-log-only -- **but a THIRD form exists and is unrowed**: an
accepted cell declined silently BECAUSE THE LATCH IS ALREADY SET (K1-K3).  Every value row in the 157-row probe sits in a
refusal-free session, so nothing in it can see that form.  Table 10's W_8r/W_8w are the WIDTH-level members of the same
class (both killed, by the `keeps' rows); the per-CELL members escape.

## *** CORRECTED 2026-09-16 BY THE FINISHING SEAT (OPUS_REPORT.md S1).  THREE OF MY READINGS WERE WRONG. ***

1. **"Every value row in the 157-row probe sits in a refusal-free session" is FALSE, and this round's OWN table 10
   refutes it.**  The seat derived a static session map (`scripts2/session_map2.py`, no emulator): 45 sessions, 72
   accepted CRIME accesses AFTER their session's first refusal, in eleven sessions, TEN of which carry a value or effect
   oracle -- and `W_8r`, the width-level form of this very class, scored 145/157 reddening TWELVE post-latch value rows
   (`killtable10_20260915/POSTTABLE.out`).  That is impossible if my sentence were true.  **It also sizes the repair:
   eight of the class's cells are already pinned, so the open set is smaller than "all 46".**
2. **The TIME attribution omitted minimax**, which also called item 6's equivalence wrong -- in its verdict line,
   independently, though by a wrong mechanism (it argued a "low lane" at +0x38, where a 4-byte access is the HIGH lane;
   the low lane is +0x3c, not a case label and not in ACCEPTS).  Count the arguments: codex right with the right reason,
   minimax right by a wrong route, grok and kimi-k3 ratified the wrong claim.
3. **F4b's credit was inverted.**  F4a/F4b refute DEEPSEEK (its item 3 is F4a verbatim, and its guess that INTSTAT 4R is
   "likely equivalent" is refuted by F4b at 156/157 {istat ctl} -- the channel is the REASSERT, not the value).  kimi-k3
   named INTSTAT 4R and got it RIGHT.
4. Minor: "both killed, by the `keeps' rows" undercounts `W_8r` -- four of its twelve red rows are `time * ctl`.

*The first is the one that mattered: I generalised from the four sessions I had built myself to all 45, and the round's
own kill table already held the counter-example.  The seat's session map is derived, not asserted, and is preserved.*
