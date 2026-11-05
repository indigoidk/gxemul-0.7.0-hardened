# qhslowifetch -- record sentences owed by the repair-pass-2 adjudication (p2r_20261105/ADJ_FABLE.md), for the CHANGELOG round block

* Q12 -- arm (b)'s comment: pass 2's sentence ("refresh it here rather than rely on ppc_exception having done so") was SUPERSEDED by
  FINAL F7's ruled text ("ppc_exception() re-resolves it ... The refresh here is redundant and harmless"), which is the shipped text.
* Q13 -- the gate runs the in-tree probe while each table ran a frozen copy; the in-tree probe is AST-equal to the frozen copy apart
  from the module docstring (checked for table 3's probe62_frozen.py by ast.dump after the records edit: AST_EQUAL in RECORDS.out).
* Q21 -- `T ra` seeds SRR0 but no row reads it: no bound shape moves SRR0 without moving pc on `T ra`, and W4 is caught by `T ra pc`.
* Q10 -- FILE the IR fact beside #QQQ (the ppc_exception MSR-modelling filing): the session that measured ppc_exception() leaving
  MSR[ME] set shows it also leaves MSR[IR] set, where the architecture clears it.
* Q23 -- how both pass-2 gaps survived five seats: the replication's sweep listed "conjoined with ME" per predicate yet omitted it
  for arm (a), and no seat's sweep listed "conjoined with ME, exit to bad:" for arm (c).
* Q7 -- table 2's D12 errata corrected in place (det_20261104/PRETABLE_2.errata.md item 3): one halt at 0xfec00208, the stale ib
  buffer decoded harmlessly across 128 slots (r24 0x00000e00).  Q15 -- an errata line for B1's duplicated `again session` (item 4).
  Q14 -- table2/VERDICT.md "row" -> "rows", in place; the gate comment's exception parenthetical now covers `T me`.
* RULE (section 3) -- a records-only correction is reviewed by one reading seat; when rows also change, that read rides on the owed
  pass; when a records-only correction is the last change, it owes a single-seat read of the final text, not a fan-out.  The chain
  closes when one pass returns 0 gaps and 0 false records on the final text.
* TABLE 3 (r3_20261105/table3/VERDICT.md) -- 32 variants, 23 red, 9 green (the predicted nine); 30 of 32 on exactly the predicted
  rows, the other two (D12, V12) BUILD-DEPENDENT and red; HEAD 36/62; null media CONTROL=FAIL each.
