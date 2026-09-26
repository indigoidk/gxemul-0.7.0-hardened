# #550 F2-on-pass-2 corrections, queued until every F2 seat has answered (then ONE patch to edit550v3.py)

From the Opus 5.5 seat (exemptredate_20260925/opus5_f2b.md), each checked before queuing:

A. P5's fix is FALSE: of the parent probe's 18 ROWS, 14 have wb == wf; only the four P2/P4 *DEFECT* rows differ
   (wb ST_IDLE / FF against wf ST_ARMED / 0x71) -- CHECKED by parsing ROWS.  And the queue row lists ONE item for the
   parent, (a); the single-leg form comes from the EXEMPT block's own "#494 ... TWO-LEG DIFFERENTIALS" comment.
   New text: "owes an exit status (`wdcaltoffleg' (a): it exits 0 whatever its `ok' says) and a single-leg form:
   four of its 18 rows want the committed build's defect, which the gate's one binary cannot supply."
B. P8: the ip30 citation `p1_runs/' holds 33/33 but no time; the 568 s is `opus550_measured_p2/keep_p1_logs.out'
   line 8, "ip30 wall from file mtimes: 568 s" -- CHECKED.  Cite that file and say the time is from file mtimes.
C. The twelve deriver's `-A13' is sized to today's list; use the list's own quotes:
   sed -n '/^AB_EXEMPT="/,/^"/p' regress/gate_asan_sweep.sh | grep -c ':2026-11-30'   (verify 12 before writing)
D. P9's "(gate 9 only constructs one)" reads as one machine -> "(gate 9 only constructs them)".
E. P15: the ppc "owed:" line contradicts the corrected sentence above it -> "owed: a gate_ppc.sh block beside
   rldimi/rlwimi, scoring its rows or after RESULT/CONTROL lines are added".
F. P12 explains 10-29 but not 11-26 -> add "(11-26, Thanksgiving, is skipped)" to the header.
G. P14 (NO TEXT CHANGE in the diff): my stated REASON was false -- a gate home for alphabook1 is the same kind of work
   as ip30's (gate_arm.sh already runs non-ARM cold-debugger probes: sgi ip32, mvme88k).  The order stands; the round
   record must carry the real reasons: #540's parked PHYSICAL change sits in dev_lca.c (dev_sgi_ip30.c is clean), and
   the Alpha four run longer together (8 + 350 + 93 + >= 484 s against ip30's 568 s).

From the dedicated grok job (wdcidselfcheck_20260925/f2b/grok_dedicated_f2b.txt), checked before queuing:

L. P2's correction NAMES THE WRONG BLOCK: `grep -nE 'E sgi|-e ip30' regress/gate_*.sh' matches exactly ONE line,
   gate_asan_sweep.sh:594 -- the #450 UB row (`for s in ip12 ip28 ip30 ip32 ip35', `-E sgi -e "$s" /dev/null', a
   liveness grep for `model: SGI-') -- not the construction sweep, which is run_machine() with `-E "$t" -e "$s"'.
   CHECKED.  New text: "as an extended regex it matches one line, gate 9's #450 row, which constructs ip12, ip28,
   ip30, ip32 and ip35 on /dev/null and runs no guest session".
   (grok also confirms A (P5, 14 of 18 -- it names the four as s4, s5, t5, t6) and D (P9: four Alpha subtypes plus the
   bare type), and Q4 for #551.)
