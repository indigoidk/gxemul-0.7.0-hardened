# qhslowifetch -- record sentences owed by the repair-pass-3 adjudication (p3_20261105/ADJ_MYTHOS.md), for the CHANGELOG round block

* Pass 3 seats: Mythos 5.1 (cloud; review p3_20261105/MYTHOS.md and the ruling ADJ_MYTHOS.md), GPT-6 Astra (codex_qhs_p3.txt),
  glm-5.3 (ollama_glm.txt; its first firing was a 502, ollama_glm.502_try1.txt, re-fired once).  Opus 5.5 not fired (owner rule:
  skippable when the Fable-family seat and Astra agree -- both said REPAIR).
* Astra's B1/B2 were MEASURED escapes before the ruling (table_p3); glm's (A) was MEASURED unproduced (DHALT_NOTE.md).
* RULED: F1 IN (msr on every -T session; `again msr` added on the ruling's stated condition -- `again` is a -T session that parks
  in arm (c)); F2 IN (`T ra chkstop`); F3/F4/F5/F7 worded as ruled; F6 decided by READING the prologue (cpu_ppc_instr.c: cpu->pc is
  assigned before addr &= ~3, so a debugger-set unaligned pc keeps bits 0-1): filed beside the arm (b) disclosure, never a row.
* FILED: zero-initialising ib in X(to_be_translated) -- a product hardening that makes V12 deterministically green (a zero word
  decodes to bad:, which returns quietly during read-ahead); on application V12 joins the green-disclosed set and the green count
  becomes ten.
* Records corrected in place this pass: the probe's `T me` prompt/checkstop sentence (Astra R1 = Mythos R1); the ME-polarity
  sentence (Astra R2); table 3's VERDICT tally (Astra R3) and its V12 note (F4); table_p3's B1c note (ruling P3); the V12 clause.
* TABLE 4: 36 variants on 69 rows -- 26 red, 9 green (the predicted nine), V12 not predicted; HEAD 37/69 exactly as predicted.
* PASS 4 (Astra, codex_qhs_p4.txt R1): the F6 disclosure said the unaligned-pc route "is not a guest state (PowerPC branch targets
  are word-aligned)" -- FALSE in this fork: X(mtlr) copies the register into LR unmasked and X(bclr_20) sets cpu->pc = LR unmasked
  (cpu_ppc_instr.c), so mtlr + blr gives guest code an unaligned pc.  Corrected in place.
* FILE (new): PowerPC bclr (and its siblings that load pc from LR or CTR) do not clear the target's low two bits; architecturally
  the branch target is LR[0:61] || 0b00.  Guest-reachable fidelity defect; it also makes arm (b) of this fix guest-reachable.
