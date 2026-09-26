**VERDICT #550: SHIP WITH CHANGES.** Three of your 19 #550 dispositions are wrong (P5, P8 and P14), and two of those fix my own findings. No date needs to move. v3 parses, and its ten EXEMPT dates and SC_EXEMPT are unchanged from v2 (measured). Only comments and the four Alpha tuple strings changed.

1. **P5's fix states something false (measured).** It says "every ROWS entry carries a want for the committed leg (`wb`) that the gate's one binary cannot supply". Of 18 ROWS, 14 have `wb == wf`, which the fix binary supplies. Only the four P2/P4 *DEFECT* rows differ (wb 0x50/0xff against wf 0x58/0x71). Also, "owes queue row `wdcaltoffleg` two things" is wrong: the row lists one item for the parent, (a). The single-leg form comes from the EXEMPT block's own comment. My pass-2 wording invited this. Suggested fix: "an exit status (`wdcaltoffleg` (a)) and a single-leg form: four of its 18 rows want the committed build's defect, which the gate's one binary cannot supply."

2. **P8's ip30 citation points at a directory that doesn't hold the number (measured).** `p1_runs/` holds 33/33 with CONTROL=OK, but no timing line. The 568 s is in `opus550_measured_p2/keep_p1_logs.out`, worked out from file modification times. The copied logs carry new timestamps, so it can't be re-derived from `p1_runs/`. Cite `keep_p1_logs.out` and say how the time was taken. The ppc citation is fine: `out_HEAD.txt` reads `SCORE 24/24 elapsed=0.0s`.

3. **P14: the order is right, but the reason is the premise already refuted for ip30.** "The Alpha four need a gate home that does not exist" doesn't hold. HEAD's `gate_arm.sh` already runs non-ARM cold-debugger probes: seven sgi ip32 and several mvme88k (mk48, pcc2_c040, pcc2_width). An alphabook1 block there is the same kind of work as ip30's. The real reasons, both measured:
   - #540's parked `PHYSICAL` change sits in `dev_lca.c`, while `dev_sgi_ip30.c` is clean.
   - The Alpha four take longer to run: 8 + 350 + 93 + at least 484 s, the last run incomplete, against ip30's 568 s.
   
   Keep the order, and fix the reason wherever it goes into the round record.

4. **The two derivers reproduce (measured).**
   - **7:** matches on HEAD and the working tree. As a control, every `sgi_` probe named on a non-comment line of HEAD `gate_arm.sh` also counts 7, so the `^python3` anchor misses none.
   - **12:** matches on both. But `-A13` is sized to today's list (the 13th line after the opener is the closing quote), so a 14th entry would fall outside the window. `sed -n '/^AB_EXEMPT="/,/^"/p' | grep -c` keys on the list's own quotes and also gives 12.

5. **P9 is right; one phrase is ambiguous (measured).** Gate 9 runs every subtype `gxemul -H` lists with `-V -E "$t" -e "$s" … </dev/null`, so it constructs machines and runs nothing on them. Alpha has four subtypes: alphabook1, alphaserver4100, 3000/300 and eb164. "(gate 9 only constructs one)" can read as "one machine"; "only constructs them" says it plainly.

6. **P15 is right, but its line contradicts the sentence above it (read).** Recording rather than wiring follows the owner ruling. The ppc line says "owed: RESULT/CONTROL lines, then a gate_ppc.sh block", directly under the corrected sentence saying a gate can score it by rows, as gate_arm scores mk48's (glm's point). Better: "a gate_ppc.sh block, scored by rows or after RESULT/CONTROL lines."

7. **The other v3 sentences hold against the tree (measured or read).**
   - P1: 24 `chk()` calls, 8 of them verdict-shaped; #484 added `chk()` on 2026-08-27.
   - P2: the extended regex matches only `gate_asan_sweep.sh:594`.
   - P6: sig takes its image as `argv[2]` and adds `ciR:` itself (:75).
   - P7: no scored ppc row calls the four helpers.
   - P10: both quotes are now verbatim against HEAD.
   - P3, P4, P11 and P13 also hold.
   - One gap: P12 explains why 10-29 is skipped but not 11-26 (Thanksgiving).

Everything is saved in `GXEMUL-SEC/regress/artifacts/exemptredate_20260925/opus550_measured_f2b/`, and each log ends in its completion sentinel. One gap: the alpha_tbi "8 s" line in the pass-1 driver log was overwritten by a shell "Terminated" notice, so that figure survives only in this transcript; its 15/15 result survives in `p1_runs/`. `NOTE_walls.txt` in that folder says so. Nothing else under the project was written.

---
*Recorded by the main loop: agent a8c6fd47a6c9c37ac (resumed for the F2 on pass 2), `agent_models.py` = clean, claude-opus-5-5; final text 2026-09-25T21:39:40.689Z UTC.  Badge s.*
