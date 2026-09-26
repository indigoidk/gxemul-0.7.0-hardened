OPUS549P1B_ALIVE
VERDICT: PROCEED WITH CHANGES

The code change is sound as written. The only change I ask for is in the round's contract: disclose the power-on reset-state finding in point 4. All four points restate the logs already under `opus549_measured/`.

**1. Does the change behave as intended? Yes — measured.**
- **Before and after:** on HEAD's build, the witness's arm K ended the process (`HOST-DIED`, exit 1). On the fix build, arm K survives (exit 0) and every control stays OK.
- **Walk on the fix build** (widths 1/2/4/8 at every offset in the 0x20 window): zero accesses reach the DATA arm's range check (`walk_fix.out`).
- **The truncation premise** is real on HEAD: `sd 0x100000003` to PORT sets port 3, and DATA reads back port[3]. On the fix build, the wide row refuses that store and PORT still reads 5.

**2. Which rows are individually needed? Measured** (`rows_*.out`). A row is individually needed if it is the only row catching some variant.

| row | what it alone catches |
|---|---|
| boundary, PORT=8 refused | `>=` → `>` |
| wide, `sd 0x100000003` refused | the compare done on `(uint32_t)idata` |
| announce, exactly one `(once)` | the latch never being set (the fix build announces 1, this variant 3) |

- **The refusal rows ("DATA reads 0x2a", "PORT reads 5")** each fail under the reset-to-0 edit and the "store `idata & 7` anyway" edit. They are needed as a group, but no single one is the only catcher.
- **The negative row (`sw -1`)** reddens under the `(int)idata` variant, but so does the wide row.
- **The zero-`(once)`-in-controls row** reddened under nothing I built.

Neither of those last two was the sole catcher of any variant. Keep them as cheap coverage, but they are not load-bearing on this evidence. Separately, one edit passed every row: setting the latch before the announce instead of after. It is behaviourally identical, not a defect.

**3. The DATA arm's range check: keep it as it is. Measured for keeping; the quiet-refusal alternative I read and reasoned, not built.**
- **Measured:** with the PORT fix deliberately broken (`>` accepts 8), writing PORT=8 and then touching DATA still ends the process with the check's own diagnostic. The check is a loud backstop against a future edit that undoes the refusal.
- **Read and reasoned:** a quiet refusal there would leave `current_port == 8` indexing `port[8]`, one past the 8-element array. That is a silent out-of-bounds access, which is worse than a clean exit.

**4. The reset-state finding: disclose it here and leave that arm to its own round. Measured.**
- **What happens:** on the fix build, 4 walk cells at +0x10 end through `fbctrl_command()`'s default arm. At power-on the selector is 0 (COMMAND). A refused selector keeps it 0, so a following DATA write of any value other than commands 0–2 invokes that default arm.
- **Why its own round:** it is the terminating call section 4 already scopes out, and taking it needs a different oracle (an unknown-command row) and a different design decision (decline and announce, or implement the documented FILL/COPY commands).
- **Why disclose it here:** this round's keep-the-selector choice is what routes a guest that writes garbage into that arm through the same two accesses. The contract should name it explicitly, so a reader does not take the round to have removed the guest-drivable process exit from `dev_fbctrl.c`. The unmapped-offset default arm (any offset other than 0x00 and 0x10) also stays reachable, as measured in the walk; name it the same way.
