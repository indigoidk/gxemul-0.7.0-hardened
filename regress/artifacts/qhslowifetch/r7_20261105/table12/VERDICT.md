# qhslowifetch -- test-variant TABLE 12 (repair 11: 249 rows; no product change since repair 5), 2026-11-05 ~11:16-11:31Z

Driver `../table12_qhs.run.sh` (frozen copy of `../table12_qhs.sh`), in THREE phases (88 variants on a 31-session probe): phase a
(`../table12_run_a.log`) cloned build/ to /tmp/gxqhs18 under a clone-local .MUTANT sentinel, checked the clone's sources against the
baseline, ran the legs and variants 1-30 and put the baseline source back with the sentinel KEPT; phases b and c (`../table12_run_b.log`,
`../table12_run_c.log`) each refused unless the sentinel and the baseline source were still there, ran variants 31-60 and 61-88, and c
restored, cmp-clean against GXEMUL-SEC, rebuilt fresh, and only then cleared the sentinel.  Every build `fresh`.  Instrument
`probe249_frozen.py` == `../base249/probe249_run.py` (cmp-checked by the driver; 249/249 on build/ after both clearance checks,
`../CLEARANCE.txt`'s repair-11 section).  Baseline `../cpu_ppc_instr.c.fix7` == GXEMUL-SEC.  `../PRETABLE_12.out` was written before
anything here.  Table 11 stays the record of the 177-row probe.  Scores: `SCORES.txt`; the mechanical comparison: `COMPARE.out`
(`../compare12.py`), **COMPARE12_MISSES=0**.

* **Legs, all exact.**  base 249/249, CONTROL=OK, SYMPTOM=ABSENT.  HEAD 108/249 (141 rows red), CONTROL=OK, SYMPTOM=PRESENT: the red
  set EQUALS the prediction (table 11's + each partner's session, pc, stopped, msr and srr0 rows).  Null media: /bin/true 94/249, an
  absent binary 64/249, /bin/false 65/249 -- each the predicted score, CONTROL=FAIL on all three.
* **THE PAIRING INVARIANT, checked on this table's own base leg:** `../pair_check.py sessions_base` -> `PAIRS_base.out`, PAIRS_OK=8/8
  (as on build/, `../base249/PAIRS.out`): every partner prints ONE halt report, textually identical to each of its two-entry pair's
  two, with the same msr command and the same final pc, MSR and SRR0.
* **Repair 11's nine, predicted EXACTLY, every one matching:** R11_tog_full (pass 10's B1, an SRR0 toggle gated on `(pc & ~0xb) !=
  addr`) 241/249 -- the srr0 rows of all eight partners; R11_tog_full_<k><c|m> 248/249 each -- its own cell's partner only.  All nine
  were 177/177 on the 177-row probe (`../B123_NOTE.md`, repair 11): they cancel on the two-entry sessions and never fire on the
  0x0204000x one-entry sessions; a partner at the same full pc sees each once.
* **Table 11's 79.**  The 56 predicted AT LEAST their table-11 sets all held, and no deterministic variant's red set on the 177 old
  rows changed; the fourteen predicted GREEN stayed green; the four BUILD-DEPENDENT variants are red; the four failure-test
  narrowings stayed inside their sessions, now widened by the partners whose fetch each refuses (each also reddened partner rows:
  R7b_f_me the ME-clear partners, R7b_f_meclr the ME-set ones, R7b_f_ra all eight, R7b_f_unal the aligned two); V12_fail_ra, NOT
  PREDICTED, reddened 29 rows, every read-ahead leg except `T ra` and no partner row (its stale-buffer decode happens on the
  read-ahead visit, which a partner does not have) -- counted in neither tally.
* **Tallies for the probe's clause (e):** 88 variants on the 249-row probe; 73 red, every one on this probe; 14 green, the
  predicted fourteen; V12 NOT PREDICTED (red here).

No variant went undetected that PRETABLE_12 did not name in advance, and no prediction missed.
