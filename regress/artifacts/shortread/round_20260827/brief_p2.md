# PASS 2 — the real `#488` diff, for review before it is committed

## PLEASE DO NOT RATIFY

Pass 1 on this round refuted **five** of my premises, four by seats that opened a file
I had not. Assume a sixth is in here. **Check the premises, not just the derivations.**

**Tree: `GXEMUL-SEC/`.** Ignore the three pristine-2021-upstream copies under the project
root. Everything you need is inlined; if you cannot read files, say which premise you
cannot settle rather than guessing.

---

## 1. THE PRODUCT CHANGE — two code lines, verbatim

```c
 		if (lenread != lentoread) {
 			fatal("[ INCOMPLETE READ from disk id %i, offset"
 			    " %lli ]\n", d->id, (long long)curofs);
+
+			/*  #488: ZERO-FILL THE SHORTFALL AT ITS OWN POSITION. ... */
+			memset(buf + lenread, 0, lentoread - lenread);
 		}
 
 		len -= lentoread;
-		totallenread += lenread;
+		totallenread += lentoread;
 		/*  #472/#488: ... */
 		buf += lentoread;
```

Everything else in the 69-line product diff is comment.

## 2. WHY B AND NOT THE ALTERNATIVE — measured, not argued

The alternative (stop the loop, report the contiguous prefix) makes the caller's tail
`memset` correct by construction. It was **built and measured**, and a **rung-3 witness on
unmodified `landisk`** settles it:

| build | guest `READ SECTORS`, halfword at byte 1534 |
|---|---|
| committed | `0x0000` — **FAIL** (disk holds `'B','B'`) |
| the alternative | `0x0000` — **FAIL, byte-identical to the defect** |
| **this fix** | **`0x4242` — ok** |

So the alternative does not merely waste data; **it reproduces the observable defect**. It
is not fail-stop, it is fail-more: the caller fixes the postcondition either way, so the
only freedom is *which* bytes are fabricated zeros, and it fabricates the lost bytes plus
every healthy byte after them — up to 63.5 sectors of a 64-sector `wdc__read`.

## 3. THE DETECTOR — 90 rows, and TEST-FIRST IS SHOWN IN BOTH DIRECTIONS

Same script, same binary-build recipe, opposite colour:

```
PRE-FIX   90 rows, 13 failures, 0 faults    DISKIMAGE_IO_FAIL
POST-FIX  90 rows,  0 failures, 0 faults    DISKIMAGE_IO_PASS
```

The 13 pre-fix failures are the defect at three positions plus their anchors:

```
  short read: caller bytes the read never wrote           = 312, want 0
  short read: base bytes surviving the tail zero-fill     = 712, want 1024
  [ANCHOR] byte 200 is the first unbacked byte            = 88 ('X'), want 0
  [ANCHOR] byte 1535 is still a base byte                 = 0, want 66 ('B')
  ROW L base-layer short: no sentinel survives            = 212, want 0
  ROW L base-layer short: the later overlay block arrives = 300, want 512
  [ANCHOR] ROW L byte 300 is the first unbacked byte      = 88, want 0
  ROW I short in iteration 2: no sentinel survives        = 324, want 0
  ROW I short in iteration 2: the later base block arrives= 188, want 512
  [ANCHOR] ROW I byte 700 is the first unbacked byte      = 88, want 0
  ROW W read-only disk: no sentinel survives              = 312, want 0
  ROW W read-only disk: all base bytes survive            = 712, want 1024
  [ANCHOR] ROW W byte 200 is the first unbacked byte      = 88, want 0
```

**Every new row fires on the REAL DEFECT, not only on its mutant.**

## 4. THE VACUITY FLOOR, CLAUSE BY CLAUSE

| clause | how it is met |
|---|---|
| (a) fails pre-fix | 13 rows, above |
| (b) verbatim reinstatement | `M1_revert` killed by the original four plus L and I |
| (c) null medium | `[IDENTITY]` row count pinned at 90 |
| (d) null-repair | `M3_countonly` (guard kept, count reverted) killed; `M2_pred0`, `M5_gtzero` killed |
| (e) contract | written into the section header — see §6 |
| (f) anchor | six `[ANCHOR]` rows pin *where* each region is |

**17 mutants measured.** Rows P/U kill `M4_remain`; ROW Z kills `M5_gtzero`; ROW L kills
`M8_layer`; ROW I kills `M9_firstiter`. **Not one new row is vacuous — each is discharged
by a measured kill.**

## 5. TWO MEASURED EQUIVALENCES, recorded as results rather than gaps

A 149,072-case sweep over base size × overlay size × bitmap × offset × length, hashing the
whole 8 KB buffer:

- `len - lenread` as the fill length: **0 differing cases.** Also provable: `buf + len` is
  invariant at the original request's end, so it can never write past the request.
- `lenread < lentoread` for `!=`: **0 differing cases** (`fread` cannot return more than
  requested).

Controls: `M4_remain` 69,880 differing, `M3_countonly` 9,686 — **the sweep can fail.**

## 6. WHAT THE ROUND FILES RATHER THAN FIXES

The capped ask-again (one per detector per round — that cap is the anti-runaway clause)
found **three** edits passing all 86 rows. **One row was taken, two are FILED:**

- **TAKEN — `&& d->writable`.** ROW W. It passed all 86 rows *and* all 149,072 sweep
  cases, because **neither ever opened a read-only disk**. Writability is not a length, an
  offset or a layer, so no amount of sweeping those could reach it. *That is this round's
  own lesson — "the fixture varies one dimension and the mutant lives in another" — turned
  on the instrument built to enforce it.*
- **FILED** — `&& totallenread < 1024` (no row shorts past iteration 2); fill only the
  first short per call (no single read shorts twice).

## 7. QUESTIONS

1. **Is the two-line change right?** Especially: is counting `lentoread` rather than
   `lenread` safe for every caller? I claim the only consumer is the tail `memset`, and
   that under this fix `fread_helper` returns `len` or 0 on the overlaid path.
2. **The caller's `memset` is now a deliberate no-op on the overlaid path.** I measured
   that it is NOT dead — deleting it reddens the round-up-gap row on a flat no-overlay
   image, which all five rig images rely on, and it has four live producers. The comment
   says so. **Is saying so enough, or does it want something stronger?**
3. **The smallest edit that breaks this fix and still passes all 90 rows.** Two are already
   filed (§6); I want a third if one exists.
4. **Is the `#472` comment repair correct?** That comment said "advance by what was
   CONSUMED" over a line advancing by the REQUESTED length — an L4 found by a seat that
   could not open the file. The replacement states the invariant as *claimed and made
   whole*. Is that the right statement?
5. **Anything wrong.** Five premises died in pass 1.

**VERDICT LINE FIRST.**
