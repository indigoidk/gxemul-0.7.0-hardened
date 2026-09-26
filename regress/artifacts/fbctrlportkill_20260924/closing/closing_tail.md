
## 6. QUESTIONS

1. **The floor, asked of the SHIPPED COMPOSITE (the 73-row detector), not only of the repair:** is there an edit of
   `dev_fbctrl.c` inside the DEPENDS-ON enumeration -- the predicates dominating the fixed arm (`writeflag == MEM_READ`,
   `idata >= DEV_FBCTRL_NPORTS`, `!d->warned_port`), weakened or qualified, or their operands swapped for fields the
   guarded body reads (`idata`, `current_port`, `warned_port`, `port[]`) -- that scores 73/73 and is NOT one of the eight
   the contract discloses?  Give the exact tokens and the rows you expect to stay green.
2. **What is the smallest edit that breaks the fix and still passes all 73 rows?**  Name the edit and the row(s) you
   expect to stay green.  An edit already in the table (§5) is worth nothing; say so if yours is one.
3. **Is any row vacuous by construction** -- its named channel cannot differ under its named edit?  In particular the
   R session's "refuse 9 after the NOP, PORT keeps 5" killed nothing on its own in table 3: keep it, or drop it?
4. **The contract (the probe's header, §4b):** is any sentence false, or true only of the case measured?  The same for
   the gate comment (§4c) and the one changed sentence in `dev_fbctrl.c` (§4a).
5. **The gate's reconciliation rows:** can a probe log pass all eight gate checks while a row is wrong?
6. **The dispositions in §2** -- which one is wrong?  Name the count.

If, while verifying a claim, you found something ELSE -- say so.
