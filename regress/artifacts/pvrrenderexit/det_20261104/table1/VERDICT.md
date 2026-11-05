# pvrrenderexit -- test-variant table 1: verdict against PRETABLE

Instrument: `probe51_draft_frozen.py` (51 rows, md5 5da28a4dfcf7). Baseline: `dev_pvr.c.fix`, cmp-equal to GXEMUL-SEC. Run 2026-11-04
19:04-19:06 local (2026-11-05 01:04-01:06Z), in the WSL clone /tmp/gxpvr_det. Records: `../legs51/LEGS.log` and `SCORES.txt` in this directory. PRETABLE.out
(sections 1-5, addenda 6 and 7) was written before either.

**Every prediction held.**

- **Legs** (`../legs51/`): base 51/51, CONTROL=OK, SYMPTOM=ABSENT; the HEAD leg 25/51 with SYMPTOM=PRESENT and CONTROL=OK (predicted
  25/51); /bin/true 9/51, an absent binary 0/51 and /bin/false 1/51, each CONTROL=FAIL.
- **B1_exit** (the removed exit reinstated verbatim): 25/51, SYMPTOM=PRESENT, identical to the HEAD leg's score (predicted 25/51).
- **M1-M33** (35 variants): each reddened exactly the rows PRETABLE named. M17_reset_at_end scored 51/51, as predicted, because it is
  equivalent: the render loop has no early exit after the reset's old position.
- **CONTROL=OK on every variant**, so addendum 7's thirteen controls are never moved by an enumerated variant. That is the claim the
  addendum made after the design ruling corrected section 4.
- **R10 is not void.** `equal overlap` and `texequal overlap` read 0x07e0 on the base, so the equal-depth edge is reachable on this tree.
  M29 and M30 (`<=` to `<`) each red exactly their own row.
- **texon is OWED.** Addendum 7(c) decided the question in advance: if M27's red set is exactly {texon overlap}, texon stays. M27 scored
  50/51 with RED=texon_overlap, so Mythos's ruling holds and Opus's "excess" is overturned by measurement.
- **The clone was restored**: cmp clean against SEC, binary fresh, sentinel cleared (`SCORES.txt`, last line; the run log).

Detected: 35 of the 36 variants. The 36th, M17, is equivalent, so nothing can detect it.
