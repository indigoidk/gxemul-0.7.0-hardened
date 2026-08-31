# #499 BLOCKS AN ALREADY-SHIPPED GATE ROW — three gate checks, not one

MEASURED, `sib.out` (frozen copies of the shipped probes, run against the
pass-1 binaries):

    sgi_re_width_probe.py  on base           35/35
    sgi_re_width_probe.py  on fix            34/35   <-- `other kill` RED
    sgi_de_width_probe.py  on base           29/29
    sgi_de_width_probe.py  on fix            29/29   <-- unaffected

The failing row is the last one in `regress/sgi_re_width_probe.py`:

    row("other kill", how, "exit1",
        "the :372 catch-all still ends the host -- DEATH ONLY, not its identity")

#499 removes that `exit(1)`, so `how` becomes `exit0`.

`regress/gate_arm.sh` consumes it in THREE places, all of which go red:

    :1181   for v in ... "other kill"; do check "sgi_re row: $v" ... "1"
    :1208   check "sgi_re rows green"   "$(count "$SGILOG" " ok$")"   "35"
    :1209   check "sgi_re rows red"     "$(count "$SGILOG" " FAIL$")" "0"

## The re-pin is NOT invented here — the row's own comment prescribes it

That comment already files the row as `otherkilldeath` and says:

> *DEATH-ONLY.  This row observes THAT the catch-all kills, never WHICH kill it
> is ... the fix is the ok_txt test the siblings already carry.  Do NOT read
> this row as pinning the catch-all's identity.*

So the correction #499 owes is the one the file was already waiting for.

## ORDER DISCIPLINE — measured, not asserted

The carrier's oracle-correction rule: re-pin FIRST, measure the COMMITTED build
RED under the NEW expectation, THEN change the code.  `repin.py` implements the
new oracle only (it does not edit the shipped probe) and is run against `base`
and `fix` in `table3.out`.  Expected and to be read from that log:

    base  ->  got exit1-txt   want exit0+txt   FAIL   (committed build, new oracle: RED)
    fix   ->  got exit0+txt   want exit0+txt   ok

## PATCH A (recommended) — rename, and update the gate's row list

`regress/sgi_re_width_probe.py`, replacing the final row:

```
 A = Addr(CODE)
 t, alive, how = session(store(A, OUTSIDE))
-# *** DEATH-ONLY.  This row observes THAT the catch-all kills, never WHICH kill it is --
-# ... Filed as `otherkilldeath`; the fix is the ok_txt test the siblings already carry.
-# Do NOT read this row as pinning the catch-all's identity. ***
-row("other kill", how, "exit1",
-    "the :372 catch-all still ends the host -- DEATH ONLY, not its identity")
+# *** RE-PINNED BY #499, WHICH REMOVED THIS KILL.  The old row was DEATH-ONLY: it observed
+# THAT the catch-all killed, never WHICH kill it was, so a change to the message that left
+# exit(1) in place passed -- MEASURED 35/35 against a matched control at 34/35.  It was
+# filed as `otherkilldeath` and its own note prescribed this repair: "the fix is the ok_txt
+# test the siblings already carry."  #499 declines the access instead of dying, so the row
+# now pins BOTH channels -- survival AND identity -- and the death-only blindness goes with
+# it.  Order proof: the new oracle was measured RED on the committed pre-#499 build before
+# the code changed (killtable_20260831/port/table3.out, `other decl` on `base`). ***
+ok_txt = ("unimplemented write to address" in t) and ("-- declined." in t)
+row("other decl", how + ("+txt" if ok_txt else "-txt"), "exit0+txt",
+    "#499: the catch-all DECLINES and announces; it no longer ends the host")
```

`regress/gate_arm.sh:1181`: `"other kill"` -> `"other decl"`.
`:1208`/`:1209` need no change — the count stays 35 and red stays 0.

## PATCH B (minimal) — keep the name, change only the oracle

If touching `gate_arm.sh`'s row list is unwanted, keep `row("other kill", ...)`
with the new oracle and note.  `:1181` then needs no edit at all.  The cost is a
row whose NAME says `kill` about a site that no longer kills, which this project
has been bitten by before (a name that outlives its meaning), so PATCH A is
recommended.

## NOT APPLIED BY ME

Deliberately.  This is a re-pin of a shipped, gate-wired detector, which is the
one edit the oracle-correction rule says must not be made quietly by the person
whose fix turns it red.  The patch text and its order proof are supplied; the
edit is the coordinator's.
