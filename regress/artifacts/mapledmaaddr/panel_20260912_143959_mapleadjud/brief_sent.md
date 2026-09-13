# ADJUDICATION PASS (§F2) — `mapledmaaddr` (#528): every pass-2 finding, shared, with the measured repair

VERDICT LINE FIRST, then the liveness token `ADJUD_MAPLE_20260912`.

You answered pass 2 blind to the other seats.  Below is every finding from the seven scriptable seats and the Opus
measuring seat, my disposition on each, and the MEASURED result.  **Please do not ratify** — I accepted almost everything,
and that is a suspicious count.  Tree: `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\` (ignore any other `src/`).

## SETTLED PREMISES (re-inlined)

* The fix: in `dev_dreamcast_maple.c`, case 0x04 (MAPLE_DMAADDR), the read arm `fatal(TODO); odata = d->dmaaddr;
  exit(1);` becomes `odata = d->dmaaddr;` (ACCEPT, upheld 9/9 on pass 1).  `switch (relative_addr)` has labels 0x04, 0x10
  RESET2, 0x14 ENABLE, 0x18 STATE, 0x80 SPEED, 0x8c RESET, 0xe8, and a default arm that prints `UNIMPLEMENTED read` and
  returns 0.  The field's consumer, `maple_do_dma_xfer()` (a different function), tests `!d->enable` and `addr & 0x1f`.
* Fable's pass-1 rule (the floor for a pure deletion whose guarded body tests nothing): clause (b) reinstatement plus the
  dominating predicates' accept/complement cells; every re-introduction keyed on a body-read operand the body does not
  test (`field == v`, `field & bit`) is clause (e), disclosed by class; any row added for one is L1 — "licensed because
  cheap, never graded floor because cheap".  DEPENDS-ON's BOUND stops at the enclosing function: never into callees.
* On SH4 a handler `return 0` silently skips the load (memory_rw.c raises no SH exception).

## FINDINGS (pass 2) — disposition — what changed

* **F1 `other read` pinned RESET2 only** (codex `switch (relative_addr & ~0x08)`, grok `if (relative_addr & 4)
  relative_addr = 0x04;`, glm/minimax/kimi `case 0x04: case 0x18:`).  ACCEPTED, graded **FLOOR**: the switch partitions
  the offsets by case label, so the complement of `relative_addr == 0x04` is every other label.  CHANGE: a read at every
  other label (0x10 0x14 0x18 0x80 0x8c 0xe8), plus reads at the default-arm single-bit aliases 0x0c 0x24 0x44 0x84.
* **F2 the silence row keyed on the literal `dreamcast_maple`** (codex, glm, kimi; Opus MEASURED 16/16 with
  `fatal("[ maple: TODO ...]")`).  ACCEPTED, FLOOR (the pass-1 ruling made interval silence floor; its literal form was
  vacuous by construction).  CHANGE: a line counts as noise if it is outside the debugger's quiet grammar (prompt echo,
  bare hex value, `put` confirmation, stepped disassembly) — measured on a clean session first.
* **F3 width: `if (len != 4) exit(1)`** (glm, kimi; Opus measured 16/16).  ACCEPTED as clause (e) (`len` is read by the
  common tail, not the guarded body); taken as an L1 row, `read width16` (mov.w).
* **F4 the consumer's partitions** (Opus, MEASURED 16/16 each): a read DECLINED only for a 32-byte-aligned value (`} else
  if (d->dmaaddr & 0x1f) {`) or only once enabled (`} else if (!d->enable) {`), and an exit under either.  Every row wrote
  an unaligned value to a never-enabled device; an aligned value is exactly what a working driver writes.  ACCEPTED, graded
  **clause (e) taken as L1** — the alignment form is `field & bit`, and `d->enable` is not a field the guarded body reads.
  CHANGE: `read aligned` (0x0c0f0000) and `read enabled` (after MAPLE_ENABLE = 1).  **See D1.**
* **F5 a per-process read counter** (Opus, measured: exit on the third read).  ACCEPTED as (e)/L1: `reread 3`; the
  contract now discloses "an effect starting after the third read".
* **F6 CONTRACT overclaims** (Opus, codex, kimi): "never one literal string" (false); "DECLINE" unqualified (only the
  unconditional form was caught); "masking of high bits" and "any single SET bit" listed as MEASURED (only low-five masking
  and bit 30 were).  ACCEPTED; rewritten.
* **F7 moving `odata = d->dmaaddr` out of the `else`** (deepseek, minimax).  REJECTED as a survivor: EQUIVALENT — the
  common tail writes `odata` only on MEM_READ.  Disclosed.
* **F8 `fatal()` under a never-true value predicate** (`d->dmaaddr == 0xdeadbeef`, minimax).  Clause (e) by the pass-1
  rule; disclosed by class, no row.

## MEASURED — kill table 2 (`regress/artifacts/mapledmaaddr/killtable2_20260912/`), frozen 29-row instrument, scratch clone

25 legs, **24 exactly on prediction, zero escapes**; BASE 29/29, HEAD 14/29.  Every survivor above is killed:
M_TOKENFREE 28/29 (read silent alone); M_ALIAS08/20/40 27/29 (their alias row + read silent, because the mask also sends
0x8c/0xe8 to the default arm); M_AND4 23/29; M_LEN 27/29; **M_ALIGNDECLINE 28/29 and M_ENDECLINE 28/29, each on its own
row alone**; M_ALIGNEXIT, M_ENEXIT, M_THIRDREAD 27/29.  Table 1's legs all re-killed.  The one miss: M_BIT30 also reddened
`read silent` — the process had already died, and the pty echoed the probe's own typed `quit` without a prompt; timing-
dependent (M_EQ4 dies the same way and did not), possible only on an already-dead process (POSTTABLE.out).

## DISAGREEMENTS

* **D1 — F4's grade.**  *Opus:* M_ALIGNDECLINE is "the canonical (d) shape, `if (X)` -> `if (X && Y)`, on the dominating
  arm, Y reading the body-read field, so it falls inside the DEPENDS-ON bound" — and either way "the record is wrong" until
  rowed.  *My disposition:* clause (e) taken as L1, on the pass-1 rule's own text (`field & bit` is (e)); the enable form is
  outside the BOUND (`d->enable` is not read by the body).  The rows exist either way; D1 decides the CHANGELOG grade and
  whether the pass-1 rule survives contact with a decline (it was written about re-introduced EXITS).
* **D2 — F1's grade.**  I graded the label/alias reads FLOOR; one could argue the alias offsets (default-arm) are value-
  domain cells of `relative_addr`, i.e. (e).  My warrant: the switch TESTS `relative_addr` by label — a body-tested
  partition — while the aliases are the cells a single-bit selector weakening would merge.

## QUESTIONS

1. Adjudicate F1–F8 and D1–D2: UPHOLD / OVERTURN / REFINE / CANNOT SETTLE, one line each with a reason.
2. **WHICH OF MY DISPOSITIONS IS WRONG?**  I accepted seven of eight.
3. **Is there a mutant that survives the 29-row instrument?**  Name the exact edit.  If none, what did you sweep?
4. Is #528 ready to commit once gate 10 is green?


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
