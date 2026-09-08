# PASS 2 on `#511` (`c7d7414`) — a one-token shift repair with a two-direction witness

**VERDICT LINE FIRST**, then the body.

Tree under review: **`GXEMUL-SEC/src/`**. Ignore any other `src/` under the project root — three
pristine 2021 upstream copies live there and give line numbers off by hundreds.

## PLEASE DO NOT SIMPLY RATIFY

A recent panel here had seven of nine seats confirm a premise the brief stated wrongly. **Check the
premises, not just the derivations.** This round is small and looks obviously correct, which is
exactly when a bad premise survives. If you cannot settle something from this packet, say so.

## SETTLED PREMISES (inlined; you need not read files)

**1. The defect.** `DEVICE_ACCESS(lca_pci_conf)`'s device-scan loop was:

```c
	for (dev=0; dev<21; dev++)
		if (tag & (0x800 << dev))
			break;
```

`0x800` is `2^11` and a plain `int`; at `dev == 20` the expression is `2^31`, a signed overflow
(C99 6.5.7p4). Verified arithmetic: `0x800 << 20` = `0x80000000` = 2147483648 > INT_MAX `0x7fffffff`;
`0x800 << 19` = `0x40000000` fits. **Exactly one iteration overflows.**

**2. The measurement, both directions, same script.** `regress/lca_confbus_probe.py` (shipped the
same day for a DIFFERENT row) drives a guest `ldq` into the PCI config window with `ioc_conf == 0`,
which takes the `bus == 0` branch with `tag == 0`, so the loop runs all 21 iterations.

    HEAD    dev_lca.c:125:21: runtime error: left shift of 2048 by 20 places
                              cannot be represented in type 'int'       1 diagnostic
    FIXED   (none)                                                      0 diagnostics
    control build/ scores 3/4 BEFORE and AFTER; same three rows green; `bus kill` still RED
            (a different defect, `lcaconfbus1kill`)

**3. `fatal()` does not terminate** in this tree; only an explicit `exit(1)` does.

**4. The detector is the differential itself and is NOT gate-wired.** Wiring it is a separate filed
row (`ubsanshiftlane`) because a new measurement lane inside a fix round is a lane nobody reviewed.

## THE DIFF — the whole of it (1 hunks)

```diff
diff --git a/src/devices/dev_lca.c b/src/devices/dev_lca.c
index 7837239..4917cff 100644
--- a/src/devices/dev_lca.c
+++ b/src/devices/dev_lca.c
@@ -121,8 +121,28 @@ DEVICE_ACCESS(lca_pci_conf)
 	bus = d->ioc_conf & 1;
 
 	if (bus == 0) {
+		/*  #511: was `0x800 << dev'.  `0x800' is a plain int (2^11) and `dev'
+		    reaches 20, so the last iteration evaluates 2^31 -- a SIGNED
+		    OVERFLOW, undefined by C99 6.5.7p4, not merely
+		    implementation-defined.  MEASURED under UBSAN before the change:
+		    "dev_lca.c:125:21: runtime error: left shift of 2048 by 20 places
+		    cannot be represented in type 'int'", reached by an ordinary guest
+		    ldq into the PCI config window (regress/lca_confbus_probe.py against
+		    build-asan; artifacts/lcashiftub/ubsan_HEAD_20260907.raw).
+
+		    `0x800U' makes the operand unsigned, so 2048U << 20 is 0x80000000U --
+		    inside unsigned int -- and NOTHING ELSE MOVES: `tag' is already a
+		    wider unsigned quantity, so the `&' and its truth value are unchanged
+		    at every one of the 21 iterations.  The emitted code on every compiler
+		    this project targets was already what was intended; the repair is owed
+		    by the LANGUAGE, which is why no guest-visible value changes.
+
+		    *** THE LOOP THIS SITS IN IS THIS FILE'S OWN GRACEFUL-DEGRADATION
+		    PRECEDENT -- the `dev >= 21' arm below has a commented-out
+		    fatal()/exit(1) and substitutes `dev = 0' instead, and `lcabadval'
+		    cites it as a transferable warrant.  The safe path contained the UB. ***  */
 		for (dev=0; dev<21; dev++)
-			if (tag & (0x800 << dev))
+			if (tag & (0x800U << dev))	/*  #511  */
 				break;
 		if (dev >= 21) {
 			/*  fatal("[ LCA: No bus 0 device? TODO ]\n");
```

## QUESTIONS

1. **Is `0x800U` sufficient and is anything else perturbed?** My claim is that `tag` is already a
   wider unsigned quantity, so the `&` and its truth value are unchanged at every one of the 21
   iterations, and no guest-visible value moves. **Check the type of `tag` and the promotion rules
   rather than accepting my sentence.** If the comparison changes at any iteration, say which.

2. **Is the "exactly one iteration overflows" claim right?** I assert `dev == 20` only. Check it.

3. *** THE ONE I MOST WANT ATTACKED. *** **Is shipping a fix whose only detector is an UNWIRED
   differential acceptable here, or is it the vacuity-floor problem wearing different clothes?** The
   round argues that a measured two-direction differential beats a source pin because it tests
   behaviour rather than text — but it also admits a regression would be caught by nothing until
   `ubsanshiftlane` lands. **Is that the right trade, or should this round have shipped a source pin
   as well?**

4. **Is the comment honest and is it too long?** It is ~20 lines for a one-token change. This
   project values terse portable C99 and minimal surgical changes. Does the comment earn its length,
   or does it belong in the CHANGELOG?

5. **Did I miss a sibling?** The same `0x800 <<` shape, or any other signed-shift overflow, in
   `dev_lca.c` or its immediate neighbours. The round did not run a tree-wide census for this class
   — a partial one is filed as `shiftubcensus`.

6. If, while checking this, you found something ELSE — say so.

## Rules

* Answer from the packet. Where you assert tree behaviour beyond it, name file and function and flag
  that you are going past what was inlined.
* Disagreements are settled by measurement, never by vote.
