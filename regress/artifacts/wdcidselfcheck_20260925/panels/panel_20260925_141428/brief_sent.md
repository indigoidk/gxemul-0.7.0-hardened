# #551 wdcidselfcheck -- PASS 1 (design, BEFORE any edit): give diff_wdc_identify.c a comparator a self-check can feed

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly.  **Check the premises,
not just the derivations.**  A seat that re-derives a premise from something this brief did NOT give it is worth more
than a seat that agrees.  **THE TREE UNDER REVIEW IS `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\`**; other copies of GXemul
under the project root are not this fork.  **Read only `regress/diff_wdc_identify.c`, `regress/diff_rtc_range.c`,
`regress/gate_offline.sh` and `regress/selfmutant.py`** -- not `regress/artifacts/` and not `tools/pipeline/ledger.json`.
If you cannot read files that is expected; every fact you need is inlined, and a premise you cannot settle from this
packet should be NAMED rather than guessed.  **VERDICT LINE FIRST**: `VERDICT: <PROCEED | PROCEED WITH CHANGES |
DO NOT PROCEED>`, then numbered findings.

## 0. HAS THIS ALREADY SHIPPED?

    git log -1 -- regress/diff_wdc_identify.c   ->  an older round; no SELFCHECK in the file (grep -c '@@SELFCHECK@@' = 0)
    grep wdcidselfcheck CHANGELOG.md             ->  nothing
No.  Test-harness only: no emulator code changes.

## 1. SETTLED PREMISES (re-inlined; do not re-derive)

* **Owner ruling 2026-09-25 (verbatim option chosen):** "Fix wdc_identify now -- a harness round right after #549 that
  moves diff_wdc_identify.c's nine row functions onto one comparator with a @@SELFCHECK@@ block, done before 09-28."
  The deadline is real: gate 2's `SC_EXEMPT` entry `wdc_identify:2026-09-27` turns one gate-2 row red from 2026-09-28.
* **What gate 2 checks** (`regress/gate_offline.sh`): every `diff_*.c` stem is in `SC_COVERED` or dated in `SC_EXEMPT`;
  every COVERED stem's SOURCE contains `@@SELFCHECK@@` (the "H"); every COVERED stem's LOG contains the text
  `SELFCHECK the comparator can still fail` (the "G").  Separately, `selfmutant.py` breaks `dev_wdc.c` and demands a
  NAMED row go red (wdc_identify's is "geometry words carry their high byte") -- that control already exists and
  passes; it answers "does the fixture reach the code", and the SELFCHECK answers "can the comparator still fail".
* **The exemption's own reason, verbatim from gate_offline.sh:** "NOTHING TO FEED A MISMATCH TO.  Read every row
  function ... ZERO-ARGUMENT with the expected value hardcoded in the body, and row(why, sectors) derives its
  expectation FROM ITS INPUT (`got57 != sectors`), so changing the input changes the answer too and no mismatch can be
  produced ... This one needs the nine row functions refactored onto a shared helper first: a round, not a line."
* **The template, `diff_rtc_range.c`**, where every row goes through one `chk(why, got, want)`: its sentinel calls
  `chk("@@SELFCHECK@@/narrow", 1, 2)` and `chk("@@SELFCHECK@@/wide", 0x100000000LL, 0)`, requires `failures` to rise
  for each, restores `failures` and `rows` afterwards (so the identity row count is unchanged), and prints
  `ok    SELFCHECK the comparator can still fail` or a FAIL line.  `selfmutant.py` filters lines carrying
  `@@SELFCHECK@@` so the deliberate FAILs are never read as kills.

## 2. THE FACTS ABOUT THE FILE TODAY (measured by script, not by reading)

The "nine row functions" is the census of 2026-08-19.  **Today:** 5,738 lines; **128 rows** (an identity row pins
`rows != 128`); **95 `failures ++` sites in 59 functions**; 96 `rows ++` sites.  Each site is hand-written:

    rows ++;                                  (placement varies; sometimes lines above)
    if (<COND>) {                             (14 of the 95 have a multi-line or braceless condition)
        printf("  FAIL <label> <details>", ...);
        failures ++;
    } else {
        printf("  ok   <label> <details>", ...);
    }

The conditions are heterogeneous: `stub_disk_writes != 0`, `occ != 512`, `lo != 0x14 || hi != 0xeb`,
`d.atapi_len != 0`, `ran != 256 || wide >= 0 || narrow >= 0 || half >= 0`, `if (bad)` after a loop that sets `bad`,
... -- there is no one `(got, want)` shape.  Gate 2 greps several row LABELS in the log by name
(`threshold: >>8 byte reaches 255`, `carry: >>8 wraps into >>16`, ...), plus the `N rows, M failures` line and
`WDC_IDENTIFY_PASS`.

## 3. THE DESIGN OPTIONS

* **A. A shared VERDICT helper.**  `static int bad(int c) { if (c) failures ++; return c; }`; every site becomes
  `if (bad(<COND>)) {` with its `failures ++;` deleted (rows ++ left where it is).  Mechanical over 95 sites, and the
  printed output is UNCHANGED line for line.  The sentinel feeds `bad(1)` (failures must rise) and `bad(0)` (must not).
  COVERS: the verdict path of all 128 rows -- a helper edited into always-passing reds.  DOES NOT COVER: any one row's
  condition expression, which stays that row's own (the same limit gate 2's comment already records for `sh4_tmu`,
  12 of 18).
* **B. Typed comparators.**  `chk_u64(why, got, want)` for the simple `x != k` sites and `bad()` only for compound
  ones.  Stronger where it applies (the comparison itself moves into the helper), but every converted site's printf
  changes, so the output is NOT identical and equivalence has to be argued site by site.
* **C. Partial.**  Sentinel-feed only the existing `row(why, sectors)` helper after giving it an explicit `want`.
  Covers the few rows that use it; honest only with a stated fraction.

**PROPOSED: A**, because the owner's deadline and a 95-site edit together need an equivalence proof that is
MECHANICAL: build the differential before and after, against the real `dev_wdc.c` and against several `dev_wdc.c`
mutants (the self-mutant above; the `% 255` revert that reddens seven rows; at least one mutant per group of rows), at
-O0 and -O2, and require byte-identical stdout except the one new SELFCHECK line.  Then the vacuity controls on the
new helper itself: `bad()` stubbed to `return 0` must red the SELFCHECK (and only it -- every row then prints ok);
`bad()` stubbed to ignore `c` must red it; and the SELFCHECK deleted must red gate 2's H and G rows.

## 4. QUESTIONS

1. **Premise audit.**  Is option A an honest discharge of the exemption's stated reason, or a check that cannot fail
   dressed as one?  The exemption says there is nothing to feed a mismatch to; under A the thing fed is the verdict
   helper, not a comparison.  Say which, and what the COVERED exception comment must then say.
2. **The smallest edit that breaks A and still passes.**  E.g. a `bad()` that goes inert after its first few calls
   would pass a sentinel run FIRST (the template runs it before its rows).  Where must the sentinel run -- first,
   last, both -- and is there a stateful edit that survives every placement?
3. **Option-set completeness.**  Is there a member not named here -- e.g. a macro that owns rows++ AND the verdict, or
   converting only the compound sites -- that the tree already has an idiom for?  Grep the other `diff_*.c`.
4. **Is the equivalence proof sufficient** to license a 95-site mechanical edit of a 128-row detector without a
   row-by-row review?  What mutant set would you require?
5. **The deadline.**  If A cannot be shipped with its proof before 2026-09-28, what is the honest fallback -- a partial
   (C) with a stated fraction, or letting the one gate-2 row go red and saying so?

If, while verifying a claim, you found something ELSE -- say so.


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
