# `#520` PASS 2 -- findings and their disposition (main loop, running as Opus 5)

**EVIDENCE BASIS: SIX of the seven scriptable transports, and the panel is SHORT TWO SEATS.**
Panel dir `regress/artifacts/alphatbinegsel/pass2_20260910/` (copied from
`_scratchpad/panel_20260910_105816/`).  This file is written while the Opus review seat is still
answering, so it is PROVISIONAL ON ITS FACE per the provisional-adjudication rule and will be revised
rather than replaced when that seat lands.

## SEAT ROSTER, and two failures recorded BY NAME rather than as agreement

* **`fable5` -- WALLED.  A GENUINE SEAT FAILURE.**  `HTTP 429 -- You've reached your Fable limit. Run
  /usage-credits to continue or switch models with /model.`  Model `claude-fable-5-1`.
  **This is a PER-MODEL QUOTA WALL, not the shared-transport class**: the Opus seat launched in the same
  minute answered normally, so the Agent tool itself was up.  **There is NO substitute transport** -- the
  carrier records that there is no fable CLI -- so unlike the kimi seat this one cannot be recovered on
  another road.  Probable cause, stated as a GUESS and not a measurement: the main loop itself ran as
  Fable 5.1 all session until the owner switched it to Opus 5, so the loop was spending the same budget as
  the seat.  **OWED: one re-fire before this round closes** (a wall is a moment, not a state, and this
  project has twice recovered a seat by testing rather than by reasoning).  If it is still walled the
  round closes with the miss named.
* **`kimi` CLI -- walled on its weekly 403, COVERED by `kimi-k3:cloud`**, which answered.  One seat
  covered, not one lost.
* **`agy` -- DELIBERATELY NOT FIRED** (measurement reserve).  Not a failure and not agreement.
* Answering: codex, grok, glm, deepseek, the kimi substitute, minimax.

## THE TWO FINDINGS THAT CHANGED THE ROUND, both SETTLED BY ENUMERATION rather than by vote

### 1. THE SIGNED CASTS ARE MEASURED REDUNDANT -- my comment attributed the repair to the wrong property

Raised by the kimi substitute, whose verdict line puts it exactly: *"THE LOAD-BEARING PROPERTY OF THE ONE
EXECUTABLE LINE IS ITS TWO-SIDEDNESS, NOT ITS SIGNEDNESS."*

CHECKED, not judged.  `a0 >= 1 && a0 <= 3` **unsigned** agrees with the shipped signed form on every
input tested: every boundary class (0, 1, 2, 3, 4, 5, 7, the 32-bit and 63-bit boundaries and their
neighbours, and the top of the range) plus 300,000 random 64-bit values -- **300,037 values, ZERO
disagreements**.  The reason is structural rather than lucky: a negative selector is a huge UNSIGNED
value that fails the UPPER bound exactly where the signed reading fails the LOWER one, so both arrive at
the conservative arm by different routes.

**DISPOSITION: the casts are KEPT and the COMMENT is corrected (L4).**  Keeping them costs nothing and
states the selector's signedness to a reader; describing them as the repair was a wrong record, and the
corrected comment now says the two-sidedness is load-bearing and the casts are not.  *A fix whose stated
reason is wrong gets that reason reused, which is why this is corrected in the source and not only here.*

### 2. THE CAST-WIDTH AXIS IS REAL AND UNROWED -- the answer to the brief's own question 2

Raised by deepseek, the only NOT-RATIFY of the panel: *"the 13-row suite still misses the signed-cast
width axis: a mutant changing `(int64_t)a0` to `(int32_t)a0` passes all rows."*

CHECKED, not judged.  Narrowing either cast to 32 bits is **invisible to every selector any row drives**
-- `a0` in {0, 1, 2, 3, 4, -1, -2}, seven values, zero disagreements.  It is nonetheless a real behaviour
change: the smallest discriminating input is **`a0 = 0x100000001`**, where the 64-bit reading invalidates
EVERYTHING and a 32-bit one truncates to 1 and flushes a single page.

**DISPOSITION: clause-(d) gap, ONE ROW OWED, repaired in-round.**  It is a predicate the fix depends on,
weakened, and it is exactly the shape this round has already been caught by twice -- first the two-sided
window's four sides, now the comparison's width.  *Three consecutive passes have each found one more axis
of the same guard, which is the trigger the class-closure amendment names: the next repair enumerates the
guard's full axis set in ONE diff rather than adding a row per pass.*  The axes now known: lower bound,
upper bound, both reject sides, the interior, the body's other lvalue, and the comparison width.

**HELD until the Opus review seat lands**, deliberately: it is reading the 13-row instrument right now,
and editing a file underneath a running job is its own documented defect class.

## WHAT THE PANEL RATIFIED
The executable line itself.  grok *"ratify the executable line"*; glm *"the executable fix is sound and
every score in the inlined kill table reconciles by enumeration"*; minimax *"PASS"* with two flags; the
kimi substitute *"the fix is correct and the table arithmetic is internally consistent"*.  **No seat
disputed the defect, the fix, or any measured score.**  Both findings above are about what the ROUND
CLAIMS and what the DETECTOR COVERS, not about whether the one changed line is right.

## STILL OPEN AT WRITING
* The Opus review seat's answer, including whether any of the thirteen rows is unkillable the way the
  pre-existing `a0 = 2` control is.
* deepseek's second item, that a comment "asserts hardware ASM/ASN exact[ness]" -- to be checked against
  the corrected comment text rather than the version it read.
* glm's item that "the brief's model of the guard is wrong" -- to be read in full and disposed.
