GAP: in `dev_sgi_ip32.c:91`, replace `CRIME_W_LEN`’s `(1 << 0)` with `(1 << !!(relative_addr & 0x80))`.
`CRIME_CLOSE3_20260913`

The enumeration is incomplete. The independent mutants below are **predicted 121/121**, based on tracing all 33 sessions and their 121 row checks. These are static predictions, not fresh emulator measurements.

1. **The address-bit latch class remains open at bits 7 and 8.**

   The edit above makes the warning latch depend on bit 7. Substituting `0x100` produces the bit-8 counterpart.

   All refusals in the [middle session](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/crime_width_probe.py:695) use `0x1ff`, `0x1fe`, or `0x1fc`; both bits stay set. Every other session’s refusals keep both bits clear. Consequently, neither mutant changes any notice in any session: `mid once` and `mid said` remain 1.

   A refusal crossing either boundary within one device instance would produce a second notice. This directly contradicts CONTRACT 4’s claim that the latch class is “closed on its single axes.” The label-crossing repair was not extended to these address bits.

2. **A notice suppressed whenever address bit 1 is clear also escapes.**

   At [the announcement guard](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/dev_sgi_ip32.c:314), replace:

   ```c
   if (!(d->warned & CRIME_W_LEN)) {
   ```

   with:

   ```c
   if (!(d->warned & CRIME_W_LEN) && (relative_addr & 2)) {
   ```

   Every offset checked by an exact `said` row has bit 1 set. The named labels have it clear, but their counted sessions subsequently refuse at `+0x07`. That later access supplies the missing notice, leaving `rev once`, `sh08b once`, `imask once`, `istat once`, `time once`, and `dog once` at 1.

   Thus, exercising both bit values does not establish announcement coverage. The first refusal’s expected text must be checked in those sessions; counting one notice somewhere permits this substitution.

3. **Branch re-arms are exercised; corresponding branch pre-sets are missing.**

   Insert this single statement inside the existing `CRIME_CONTROL_DOG_ENABLE` branch:

   ```c
   d->warned |= CRIME_W_LEN;
   ```

   The only accepted access entering that branch is `sw 0x0201` in [the re-arm session](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/crime_width_probe.py:628), after the first refusal has already set the latch. The insertion is therefore invisible. The `latch x5` prologue writes `0x01`, which skips the branch.

   The same insertion **inside** the REV PROM-window condition is another survivor. `rev pc ctl` enters it but has no subsequent refusal; `rearm once` enters it after latching. The ordinary REV read added to the latch prologue does not enter that condition. Table 5’s `c2_pre_rev` inserts **before** the condition and therefore does not establish this branch’s coverage.

   There is also an INTSTAT-only pre-set survivor: insert the statement immediately after `case CRIME_INTSTAT:`, before `case CRIME_INTMASK:`. Setup enters INTMASK; accepted INTSTAT accesses occur after refusals.

   The requested enumeration must distinguish **before-first-refusal pre-sets** from **between-refusals re-arms**, for each applicable entry and branch.

4. **Far-block store checks cannot observe a clearing mutation.**

   Replace the width arm’s `goto crime_declined;` with:

   ```c
   if (writeflag == MEM_WRITE && (relative_addr & 0x200))
       d->reg[relative_addr / 8] &= idata;
   goto crime_declined;
   ```

   Every refused far-block store operates on a register containing zero. ANDing it with the incoming data leaves zero, so [hi keeps](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/crime_width_probe.py:675) passes. The separate top session seeds a nonzero register but performs only refused **reads** over it.

   This is a store effect conditioned on one address bit, matching the claimed class. Seed the far register with nonzero data and observe it after each refused store; retain zero-seed coverage for effects that only set bits.

The remaining enumeration also needs precise corrections:

| Claim | Review result |
|---|---|
| Named-label answers | All six labels have a halfword answer check. Repair 7 supplies the advertised nonzero IRQ lanes. CONTROL has no byte-read check; its `0x100` seed has a **zero low byte**. POSTTABLE 5’s “low byte, at both widths” wording is false. This alone does not defeat the width-independent, label-only answer checks. |
| Width, direction, and named-label latch keys | The repaired sequences cross these values. Address bits 7 and 8 lack that transition. |
| Listed branch re-arms | DOG_ENABLE, control text, and REV redirect are interleaved with refusals. This does not establish their pre-set coverage. |
| Every address bit carried both ways by each kind | Literally false: aligned halfword accesses never set bit 0, and `0x1fc` clears bits 0 and 1. More substantively, findings 1, 2, and 4 invalidate the claimed observable coverage. |

The incorrect closure claims are in [CONTRACT 4](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/crime_width_probe.py:53), the [address-bit disclosure](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/crime_width_probe.py:135), and [POSTTABLE 5’s DENOMINATOR](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/killtable5_20260913/POSTTABLE.out:43). Exact predictions for selected mutants do not establish those broader classes.

I verified the inlined function/header against the current files, the current probe’s executable AST against frozen table 6, the recorded source hash, and the completion markers in all table-5/6 probe logs. This read-only session could not build or measure new mutants. The outstanding measurements are the seven independent variants above; each has a predicted empty failing-row set.

NO-GO
