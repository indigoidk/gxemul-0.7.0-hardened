# PRETABLE errata -- #579 (2026-11-04)

The PRETABLE files beside this one are NOT edited: each one's modification time is the proof that it was written before its table ran.
Each entry below quotes the sentence it corrects, names the ruling that ordered the correction, and gives the measured fact.

From the F2 ruling of record (`../adj_20261103/MYTHOS_F2R.md`, item F18):

* `PRETABLE.out` line 6: "the store arm has a reservation state the load arm has not" -- wrong: the load arm creates the reservation
  (AFTER:2329-2330) and the store arm consumes it (:2351).
* `PRETABLE.out` line 38: "every session fails to answer: RESULT near 0/73" -- wrong in the claim, the number and the denominator:
  `/bin/true` passed 15/77 (table 2) and 15/83 (table 4), 14/83 after census repair B; a missing binary passed 1/77 and 1/83, 0/83 after
  repair B (`../f2r_20261104/probe_true.out`, `probe_absent.out`).

From the Fable 5.1 regress review (`../adj_20261103/FABLE_REGRESS.md`, finding R5):

* `PRETABLE.out` line 19: "old_so {0, set} EXHAUSTED" -- exhausted on the success path only.  Test variant M18 (the failure path's XER[SO]
  copy dropped) scored 77/77 in table 3, so the failure-and-SO cell was empty until the `nso` session was added; table 4 reds M18 on `nso cr`.
* `PRETABLE2.out` lines 11-12: "the 14 exit-status rows and the empty census pass" and "nothing passes but the census" -- superseded by
  census repair B: the census reads 0/35 FAIL on both dead-binary runs (`../f2r_20261104/probe_true.out`, `probe_absent.out`).
* `PRETABLE2.out` line 9: "ra {0, != 0} is now EXHAUSTED on the load path (lw ra)" -- holds for the valid form only; RA is 0 on every
  bit-31 form.  The probe docstring's sampling sentence is the precise statement.
