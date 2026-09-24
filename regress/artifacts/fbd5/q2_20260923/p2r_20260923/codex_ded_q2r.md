Read-only code review task (C, GXemul hardened fork).  Do NOT edit, build or run anything.

Tree: C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\fbd5\q2r\frozen\ -- read ONLY these frozen copies:
  dev_footbridge.c (md5 783c0c7f; the device model, function dev_footbridge_access),
  diff_footbridge.c (md5 ff8f87b6; an offline test harness that #includes dev_footbridge.c and checks 491 rows),
  diff_footbridge.prerepair.c (md5 116083d0; the same harness before today's change, 333 rows),
  gate_offline.sh (md5 03cea4dc; the gate that runs the harness and pins its row counts).
Ignore every other copy of GXemul under C:\DocumentNoSnc\cc\GXEMUL (./src/ and _archive/ are upstream 2021).

Background, one paragraph: five register arms of dev_footbridge_access -- writes to IRQ_STATUS, IRQ_RAW_STATUS,
FIQ_STATUS, FIQ_RAW_STATUS and the read of IRQ_ENABLE_CLEAR -- are "declined": no field changes, a declined
read returns 0, and each site reports once through its own warn-once flag (warned_*).  Today's harness change
added the X9 rows (every legal access with every flag still clear, from three states: seeded, all-zero,
wide) and a "wide" third state to the X6/X7 rows, after five one-condition edits to the direction test
(e.g. `if (writeflag == MEM_READ && d->irq_enable)` at IRQ_STATUS) were measured to leave all 333 old rows
green.  They now make 2-3 X9 rows fail each.

TASK 1 -- for each of these ten SUPPLIED one-line variants of dev_footbridge.c, work out BY READING which of the
491 harness rows fail (name the first such row by its exact printed name and the value that differs), or
state that none fails.  For a variant where none fails, say whether it is EQUIVALENT (no guest-observable
difference in any reachable state) or a real behaviour change the rows cannot see, and give the smallest
guest access sequence that shows the difference.
  V1  IRQ_STATUS:        `if (writeflag == MEM_READ && !d->warned_irq_raw_w)`
  V2  IRQ_RAW_STATUS:    `if (writeflag == MEM_READ && len == 4)`
  V3  IRQ_STATUS:        `if (writeflag == MEM_READ && d->irq_enable != 0x10)`
  V4  FIQ_ENABLE_CLEAR:  `if (writeflag == MEM_WRITE && d->fiq_enable)`
  V5  IRQ_ENABLE_SET:    `if (writeflag == MEM_WRITE && d->irq_status) {`
  V6  IRQ_STATUS:        `else if (!d->warned_irq_status_w && d->irq_enable) {`
  V7  IRQ_ENABLE_CLEAR:  `} else if (!d->warned_irq_clear_r && len == 4) {`
  V8  IRQ_STATUS:        `odata = d->irq_status & d->irq_enable & 0xffff;`
  V9  IRQ_ENABLE_CLEAR:  `d->irq_enable &= ~(idata & 0xff);`
  V10 IRQ_ENABLE_CLEAR:  `if (d->irq_status & idata)` in place of `if (d->irq_status & d->irq_enable)`

TASK 2 -- enumerate, from the handler's own code, every predicate that DOMINATES each of the five declines
(walk up to the function boundary, not into callers or callees) and every field read by EITHER branch under
the direction test.  For each (predicate, field) pair where a one-condition addition could change which
branch a legal or a declined access takes, name the harness row that pins it, or say that none does.
Report the count as N covered of M enumerated, and list the uncovered ones.

TASK 3 -- audit the prose: the rewritten CONTRACT comment above the X6 rows and the X9 header comment in
diff_footbridge.c.  Quote any sentence that the code or the rows contradict, with the file line.

TASK 4 -- name at least one question about this change that the task list above did not ask.

Answer format: start with one line `VERDICT: <one sentence>`, then TASK 1 as a ten-row table, then TASKS 2-4.
No "no findings" without the denominator you checked.  End with what you read.
