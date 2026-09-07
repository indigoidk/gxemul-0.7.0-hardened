# PASS 2 on `83df95c` -- the review this commit never got, because the seat walled mid-panel.  2026-09-06.

## WHAT THIS IS
An ordinary correctness review of a device model in a hardware simulator for obsolete workstations (GXemul 0.7.0,
a maintained fork): the WD-compatible disk controller's data-register read path.  Plain engineering vocabulary; no
security framing is intended or wanted, and none of this concerns a production system.

**The tree under review is `GXEMUL-SEC/src/`.  Ignore any other `src/` you find** -- three pristine-2021 upstream
copies sit under the project root and are NOT this fork; a copy reports line numbers off by hundreds.  The file is
`GXEMUL-SEC/src/devices/dev_wdc.c`.  Cite by grep anchor, not by line number.

**VERDICT LINE FIRST.**

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY
This commit's product diff is **COMMENT-ONLY** -- both hunks sit inside `/* */`.  So there is no behaviour to
review, and the entire question is whether the corrected comments are **TRUE**.  That is a sharper test than it
sounds: this project has repeatedly shipped a records correction that was itself wrong, and a correction carries
more authority than the error it replaces, so it earns a second reading rather than less of one.

**Check the claims, not the plausibility of the wording.**

## THE COMPLETE PRODUCT DIFF (two hunks, both comments)

```diff
@@ -291,9 +291,10 @@ static uint64_t wdc_get_inbuf(struct wdc_data *d)
 		    the SECOND over-read falls through to the tail advance
 		    below and corrupts the ring pointer -- a fix strictly worse
 		    than the flood it removes.  Row `overread -1` pins it.
-		    See `wdcringambig`: after an overrun this predicate is
-		    unsound, because a FULL ring is indistinguishable from an
-		    empty one.  */
+		    See `wdcringambig`: BEFORE #484 this predicate was unsound
+		    after an overrun, because a FULL ring was indistinguishable
+		    from an empty one; #484 sacrifices one slot, so head == tail
+		    now means EMPTY (stale wording corrected 2026-09-05).  */

@@ -1137,7 +1138,8 @@ DEVICE_ACCESS(wdc)
 				    from the buffer, not for what the guest
 				    asked for. The reads above take one byte,
 				    two if len >= 2, four only if len == 4 --
-				    so a 3- or 8-byte access consumes 1 or 2
+				    so a 3- or 8-byte access consumes 2 (widths
+				    1..8 pop 1, 2, 2, 4, 2, 2, 2, 2; "1 or 2" until 2026-09-05)
 				    while `len` says 3 or 8. Subtracting the
 				    requested length let atapi_len step PAST
 				    zero, which its `== 0` test then never
```

## THE TWO CLAIMS, AND WHAT WOULD REFUTE EACH
1. **THE WIDTH CENSUS.**  The new comment asserts that for access widths 1 through 8 the number of bytes actually
   popped from the input ring is exactly **1, 2, 2, 4, 2, 2, 2, 2**.  Derive this from the read code itself
   (anchor on `wdc_get_inbuf` and the `DEVICE_ACCESS(wdc)` data-register arm) rather than from the comment.
   **Give me the eight values you derive and the control expression that produces each.**  If any cell differs,
   the comment is a fresh wrong record in the place a previous wrong record was just corrected.
2. **THE RING PREDICATE.**  The new comment asserts that `#484` "sacrifices one slot, so `head == tail` now means
   EMPTY".  Verify against the ring's actual definition and its writers: does `#484` in fact make the full and
   empty states distinguishable, and is `head == tail` unambiguously EMPTY now?  **If the ring can still reach a
   state where `head == tail` while data is pending, the correction has replaced one unsound sentence with
   another.**

## THE THIRD QUESTION -- what the commit did NOT do
The same commit touched `regress/diff_wdc_identify.c`, `regress/wdc_flood_probe.py`, `regress/gate_offline.sh` and
`regress/diff_diskimage_geom.c`.  Given that the product change is comment-only, **is there any detector row in
those files whose oracle depends on the OLD wording being true?**  A row written against a sentence that has just
been corrected is a row that may now be pinning the wrong thing.

## THE SECOND QUESTION, with the count named
Of the claims above -- (i) the eight-value width census, (ii) `head == tail` means empty after #484, (iii) that a
comment-only product diff needs no detector change -- **WHICH IS WRONG?**  Assume at least one is.

VERDICT LINE FIRST (`BOTH CLAIMS HOLD` / `CLAIM <n> IS WRONG: <what>` / `CANNOT SETTLE: <why>`), then the derived
width table with its control expressions, then anything else.  Under a page.
