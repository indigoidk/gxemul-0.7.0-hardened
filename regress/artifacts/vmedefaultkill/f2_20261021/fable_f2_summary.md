**ALREADY IN: Fable 5.1's adjudication of this packet (verdict PROCEED WITH CHANGES; full text
`vme/f2/out/fable5_f2.md`).  Check its two overturns -- they are claims, not rulings, until you agree.**

* **F3's FIX OVERTURNED -- "reaches five" is still an overcount; the guest reaches FOUR.**  Fable: *"`vme2chip_init()`
  runs at attach (vme.c:351, BUS_PCCTWO) and touches MASTERCTL (:452 read, :494 write-back), MASTER3 (:467), MASTER4
  (:480), MASTER4MOD (:482) -- four registers; the `master1/master2` reads are `#if 0`. A struct-field grep of all of
  `sys/arch/mvme88k` for the 26 population-2 fields finds NO other site. IRQSTAT (:576) and IRQCLR (:581) live only in
  `vme2abort()`, installed as the ABORT-switch NMI handler by `intr_establish(110, &sc->sc_abih)` at :539 -- and
  dev_vme.c contains no interrupt assertion at all, so vector 110 is never delivered by this model."*  My pass-2
  correction said five; the witness's "7 of 7" is a SITE census, not a reach claim.  **Adopted provisionally:** the
  comment will say the driver has access sites at six, its attach reaches four, and IRQSTAT/IRQCLR sit in the
  ABORT-switch interrupt handler this model never triggers.  *Is the NMI-handler reading right?*
* **F10(c) REFINED -- two rows need two legs.**  Fable: GL's mutant is `len == 2` only; the `st.b` lane-0 access kills
  the `len == 1` twin, so table 2 owes M_LANE0H AND M_LANE0B or the st.b addition ships unmeasured.  **Adopted.**
* **D5 REFINED -- the "adopt the macro if M_ONENARROW escapes" test cannot fire.**  Fable: the kill is UB-mediated --
  on x86-64 `1u << 35` masks to bit 3 (SLAVELMOD2's), silencing MISC in `p2 ann rd`; where a 32-bit shift by >= 32 gives
  0, MISC never latches and `p2 ann rd 2` reds instead.  *"A kill either way, by DIFFERENT rows ... write 'macro FILED'
  outright and record the platform beside the leg."*  **Adopted: the macro is FILED; M_ONENARROW is measured and its
  red row recorded with the host it ran on.**
* **D1 / F5 -- Fable CONCEDES ALIGN** (its KEEP rested on the re-run cost, which rev 3 removes); table 1's provenance is
  never rewritten -- tables 1/1b measured the `%x` form (fix568, md5 4e3e7fc2), table 2 measures fix568b.
* **D2, D3, D4 -- Fable UPHOLDS** the rev-3 rulings and taking F10 (a)-(c) under L1, and supplies the CHANNEL lines:
  `p2 zero wr` (a first-access `st r0` -- r0 is hardwired zero -- in its OWN short session, want one write-form line;
  one width is enough because the swap tests idata's zero-ness and the body tests nothing on len), `p2 nw rd 2` /
  `p2 nw wr 2` (a second pass over the six non-word accesses, want 0 lines), `p1 quiet` (count `[ vme:` in the existing
  free-running census continue text, want 0 -- it varies ONLY because that session free-runs at verbosity 0),
  `p1 widths` + `ld.hu` and `st.b` at word-aligned population-1 offsets (8 faults).
* **Owed, from Fable's "what we all missed":** re-derive the probe's `unasm` literal BY HAND before rev 3's first run
  (its own rule); move the gate's row list and its three count pins to rev 3's count (38 rows); one `grep -c` for the
  CPU's own fault text on a free-running fault transcript, to settle D5's "INFO-level line" record; M_ONENARROW's red
  row named with its platform.  F17 is DONE: the kill tables' build logs are now under `killtable1_20261020/build/` and
  `table1b/build/`.
