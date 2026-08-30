# The four ratchet reds the 2026-08-29 battery found -- dispositions, MEASURED

Battery `verdict_20260829_160646`, HEAD `fb0cc78`, TREE_DIRTY=no.
Six FAIL rows: **2 are a real regression, 4 are pinned ratchets owed by recent rounds.**

## 1-2. readiness: pty-probe denominator 35 -> 37, promptless 9 -> 11

The gate NAMED its offenders, which is the whole point of the `comm -13`:

    NEW PROMPTLESS PTY PROBE(S) -- add prompt detection, or grandfather
    deliberately by editing GRANDFATHERED_PROMPTLESS above:
      gdrom_decline_probe.py     <- #490, mine
      gdrom_toclen_probe.py      <- #489

`gate_hygiene.sh` is explicit that adding them is NOT a bypass -- the list is
*"promptless probes we KNOW about"* -- but it demands the REASON be written down
rather than the count quietly raised.

### *** AND THE REASON THE COMMENT GIVES IS WRONG ABOUT ITS OWN SET. Measured. ***

It says both new entries are promptless *"for exactly the reason the five already
listed are -- they free-run to a breakpoint"*.  Censused by grepping every member:

    member                      breakpoint   budget-drain
    drive_guest.py                   0            0
    gdrom_data_probe.py              0            1
    gdrom_default_probe.py           0            2
    sh_intprio_probe.py              4            1
    sh_iprbcd_probe.py               4            1
    sh_pclock_probe.py               0            1
    sh_tlbmulti_probe.py             0            1
    asic_badaddr_probe.py            0            1
    wdc_flood_probe.py               4            1

**Breakpoint is true of THREE of the nine.  BUDGET-DRAIN is true of EIGHT.**

The real shared mechanism is readiness by TIME BUDGET rather than by prompt:

    end = time.time() + t
    while time.time() < end:
        r, _, _ = select.select([fd], [], [], 0.25)

-- byte-identical in `gdrom_decline_probe.py` and in the already-grandfathered
`gdrom_default_probe.py`.

**WHY IT MATTERS RATHER THAN BEING TIDY:** a future round adding a promptless probe
reads that comment, finds its probe is not breakpoint-based, and concludes it must
"add prompt detection" -- when the majority precedent says it belongs in the set.
The comment sends the reader to the wrong one of the two dispositions the gate
itself offers.

**DISPOSITION:** add both probes by name; raise `EXPECT_PTY_PROBES` 35 -> 37; and
CORRECT the rationale to name budget-drain as the dominant reason, with breakpoint
as the minority one.  Three edits, one of them an L4 correction.

## 3. readiness: whole-buffer full-prompt 2 -> 4  *** DO NOT BUMP THIS ONE. ***

**IT IS NOT A DENOMINATOR.  IT IS A FAIL-CLOSED ALLOWLIST OVER A MEASURED-BROKEN
PATTERN**, and raising it is precisely the bypass its own comment forbids:

>  #392 MEASURED that exact configuration (full prompt, whole buffer) failing just as
>  completely as the bare one: arm B scored **0/80**, byte-identical to arm A. ...
>  those two are tolerated, a third is not, and when they are finally converted this
>  number goes to **0** in the same commit.

**And it is NOT my two probes** -- `gdrom_decline_probe.py` and `gdrom_toclen_probe.py`
contain ZERO `endswith(`, which is why they trip the promptless row instead.  The two
new sites are `selftest_inactivity.py:87` and `:102`, from `29b450c` (#467/#468).

### Read, not guessed -- and the answer is that BOTH are legitimate

    def wait_absolute(s, timeout):
        """The PRE-#467 shape, kept here as the negative control.  Do not 'fix' it."""

`:87` is a DELIBERATELY PRESERVED NEGATIVE CONTROL whose docstring says not to fix it.
`:102` is #467's CORRECT shape, which also checks the prompt but resets its clock on
progress.

**Decisively: neither drives a real guest.**  `s.rd()` pops from `self.chunks` -- a
SIMULATED stream built to test wait() semantics.  There is no pty, so the #392 failure
mode (a real guest's own output racing the predicate) cannot arise.

### THE DISPOSITION, and all three naive ones are wrong

* **Raise the pin to 4** -- widens a fail-closed allowlist to tolerate two more REAL
  instances of a pattern measured at 0/80.  This is the bypass the comment forbids.
* **"Fix" the selftest** -- destroys a negative control that says DO NOT FIX IT.
* **Leave it red** -- the battery stays red forever and the next reader learns to
  ignore it, which is how the 2026-08-23 red hid five other defects.

**Correct: EXCLUDE `selftest_inactivity.py` from `probe_code`'s scan, keep the pin at
2, and record why.**  That preserves the fail-closed property exactly -- a genuine
third GUEST-PROBE instance still fails -- while not counting a simulated stream as a
readiness site.

*The gate's grep cannot distinguish a simulated stream from a real pty, and that is the
actual defect: the scan's POPULATION is wrong, not its threshold.*

## 4. class ratchet: the sweep still sees the whole call set 24 -> 21

**DOWNWARD, which is the ambiguous direction.**  `DIAG_DIV_TOTAL` is the DENOMINATOR
guard, and `gate_hygiene.sh` says why it exists: *"if the sweep silently stopped
finding ANYTHING the count above would still read 2 only by luck, and a zero total is
the classic vacuous green."*

The numerator still reads 2 (`drivable divisions in diagnostic argument position`
PASSES), so **the sweep is working, not broken** -- three sites were genuinely removed
between 2026-08-23 and HEAD.

The gate's own instruction is *"A THIRD site means someone added a new instance of the
class: read it before raising this number."*  That is written for the UP direction; the
DOWN direction has no instruction, and it should get one -- a removal is good news, but
only if you can name which three went and why.

**OWED: run `diag_div_sweep.py`, diff its site list against the 24 pinned on
2026-08-16, and name the three.**  Do not re-pin to 21 until they are named.

*** AND DO NOT SUBSTITUTE A GREP FOR THE SWEEP.  I tried, 2026-08-29, and it
produced pure noise. ***  A pattern like `% *[a-z_]` matches PRINTF FORMAT
SPECIFIERS -- `0x%02x` reads as a modulo -- so it reported seven commits
'removing divisions' when they had removed format strings.  Every number it gave
was a false positive that LOOKED like a result.

`gate_hygiene.sh` says why the sweep exists and it is exactly this: the call *"may
span lines"*, so `diag_div_sweep.py` *"balances the parens and does that; it also
splits constant divisors (which cannot be zero, so are not the shape) from drivable
ones."*  **The tool was built because the regex cannot do this job, and reaching
for the regex anyway reproduced the defect the tool was written to avoid.**

## 5. asic_badaddr rows run 13 -> 14  (appeared later in the same run)

    ok   asic_badaddr result parses      yes
    FAIL asic_badaddr rows run           got=14 want=13
    ok   asic_badaddr rows correct       14

**All fourteen rows PASS.  Only the pinned denominator is stale**, by one, from a
prior asic round that added a row without raising the gate's pin.  Note the gate
separates "how many RAN" from "how many were CORRECT" -- denominator and numerator --
which is why this reads as a pin defect and not as a broken probe.

## *** THE PATTERN, and it is ONE finding rather than five. ***

Five of the seven reds are **battery-only pins that drifted**, contributed by at least
three different rounds (#489, #490, an asic round, and whatever removed the three
diagnostic divisions).

**They drifted for a structural reason, not a careless one: `precommit_check.sh` does
not run the gates, so a pin that lives inside a gate is checked ONLY by the weekly
battery.**  A round can be fully green at commit time -- as #490 was, PRECOMMIT_PASS,
targeted gate 20/20 and 60/60 -- and still leave a battery pin un-raised, because
nothing between the commit and Sunday looks at it.

**And the unread red hid the accumulation.**  The battery had been RED since
2026-08-23 on an unrelated stale allowlist entry, and `nightly_check.sh` cannot
distinguish "fixed" from "never looked at".  So five pins drifted behind one red that
everyone already had an explanation for.

*That is the seat-failure-counted-as-agreement shape, one level up: a red nobody reads
is not a signal, and a second defect arriving behind it is invisible.*

**This is an argument for a cheap pin-drift check, NOT for more gates.**  The pins are
mechanically derivable -- each is a `check "<name>" "$got" "<literal>"` whose `$got`
comes from a probe's own emitted row count.  Whether that can be checked without
running the probes is the open question, and it is the right question to ask before
building anything.

## 6. wdcflood: six warned_ guards present  12 -> 15

    ok   wdcflood: fatal() call sites intact (channel not downgraded) 13 (>= 12)
    FAIL wdcflood: six warned_ guards present (one set + one read each) got=15 want=12

*** THE PIN'S OWN COMMENT CLAIMS IMMUNITY TO THE FAILURE IT JUST SUFFERED, and calls
that claim "THE WHOLE LESSON". ***

>  AND THIS COMPANION PIN IS CORRECT, WHICH IS THE WHOLE LESSON.  It sits two lines
>  below the one that was red for two rounds, counts the same kind of thing, and did
>  not decay -- because it ENUMERATES SIX NAMED LATCHES in its regex instead of
>  counting an open set.  The device carries ELEVEN warned_ latches today; **this pin
>  still reads 12 because growth cannot reach it.**
>
>  A CENSUS PIN OVER AN OPEN SET BREAKS ON GROWTH.  A PIN OVER A NAMED SET DOES NOT.

**Growth reached it.**  Measured per latch:

    d->warned_inbuf_overrun      4   <-- grew by 2
    d->warned_inbuf_overread     2
    d->warned_unimpl_cmd         3   <-- grew by 1
    d->warned_nonbyte_write      2
    d->warned_nonbyte_read       2
    d->warned_data_unexpected    2
                                --
                                15   pin says 12

`#485` (`d819188`, *"242 of 256 opcodes ended a command and never raised its
interrupt"*) is one contributor.

### THE DIAGNOSIS: naming the set closes ONE dimension of growth, not both

* **MEMBERS** -- a NEW latch name cannot reach the pin.  The comment is right; the
  device carries eleven latches and only six are named.
* **OCCURRENCES** -- a new *guarded site* re-using an ALREADY-NAMED latch adds a
  matching line.  `grep -c` counts LINES, so a second `if (!d->warned_inbuf_overrun)`
  at a new site increments it.  **Nothing about naming the members closes this.**

### AND THE COMMENT'S OWN RULE WOULD HAVE PREVENTED IT

Its last sentence is correct and was not followed:

>  Never an equality over a set the codebase is expected to add to.

`d->warned_X` OCCURRENCES are exactly such a set -- every newly-guarded site adds one.
The members were named, and then an EQUALITY was used over their occurrences anyway.

**THE FIX IS THE ADJACENT LINE.**  Two lines above, `wdcflood: fatal() call sites
intact` uses a FLOOR -- `13 (>= 12)` -- and it PASSED in this same run.  Change the
equality to `>= 12` and the pin keeps its meaning (each of the six is still guarded)
while surviving legitimate growth.

*The correct pattern was literally adjacent, passing, in the same gate section.  This
is the freshly-minted-exemplar problem: a rule was minted, an example attached, and the
example was asserted to be immune on a dimension nobody had tested.*

## SIBLING SEARCH for the wdcflood class -- done properly, and the answer is ONE

The equality-over-a-growing-set defect invites the question the carrier's mechanical
rule 2 demands: *"When correcting a claim, grep for its siblings before calling it
fixed."*  I broke that rule earlier today on the assert L4 and paid for it, so it was
run here BEFORE the fix rather than after.

**MEASURED, with a positive control and a denominator:**

    checks whose got-expression uses `grep -c`      257     <- DENOMINATOR
    of those, an EQUALITY over a SOURCE-line count     1     <- wdcflood, the one that broke

**The class population is ONE.**  There is no hidden family, and the battery-reds round
is bounded to the single row.

### The apparatus note, because the FIRST attempt returned a confident zero

A stricter multi-line regex returned **0 hits** -- including on the instance I already
knew existed.  `0` with no denominator is the phantom-absence shape this project has
recorded six times, and it would have licensed the sentence *"no siblings exist"* on the
strength of a pattern that matched nothing.

**What made it safe was asking the pattern to find the KNOWN instance first.**  It could
not, so the pattern was rewritten (checks wrap across lines with backslashes, which the
first form did not join).  The rewritten form finds wdcflood and reports 257 considered.

> *A sibling search that returns zero is only evidence if it can be shown to find the
> case you already have.  Otherwise it is the same sentence a broken grep prints.*

## 4 (RESOLVED): the class ratchet 24 -> 21, measured with the TOOL not a grep

`python diag_div_sweep.py` at HEAD:

    diagnostic-argument divisions: 21 total, 19 constant-divisor, 2 NON-CONSTANT
      NONCONST  devices/dev_ns16550.c:79   debug(, d->name, (int)(115200 / d->divisor))
      NONCONST  disk/diskimage.c:543       debugmsg(... (int)(bytes_left % ct->sector_size))
    DIAG_DIV_NONCONST=2
    DIAG_DIV_TOTAL=21

| | 2026-08-16 census | HEAD |
|---|---|---|
| total | 24 | **21** |
| constant-divisor | 22 | **19** |
| **NON-constant** | **2** | **2** |

*** THE LOAD-BEARING FACT: THE TWO NON-CONSTANT SITES ARE UNCHANGED AND ARE EXACTLY
THE TWO THE GATE'S OWN COMMENT NAMES. ***  Those are what the ratchet protects -- a
constant divisor "cannot be zero, so is not the shape."  The numerator is intact; only
the benign class shrank.

**ATTRIBUTION.**  Of the ten files holding const sites, only TWO were edited since the
census -- `dev_dreamcast_gdrom.c` (11 commits) and `diskimage.c` (4).  Two of those
commits removed lines carrying a diagnostic-position division: **`00d546d` (#472)** and
**`09362f0` (#488)**.  So the drop is accounted for by our own rounds editing
diagnostics in two files, all in the constant class.

**DISPOSITION: re-pin 24 -> 21 IS SAFE**, and the round should say WHY rather than just
bumping: the protected quantity (NONCONST) did not move, and the removals are
attributable and benign.

### AND THE GATE COMMENT OWES A LINE FOR THE *DOWN* DIRECTION

It says *"A THIRD site means someone added a new instance of the class: read it before
raising this number"* -- written for growth only.  A DECREASE is ambiguous in a way the
comment never addresses: it can mean the code improved, or that **the sweep stopped
finding things**, which is the vacuous-green shape the denominator exists to catch.

> **The discriminator is the NUMERATOR: if `DIAG_DIV_NONCONST` still reads 2 and names
> the same two sites, the sweep is working and a lower total is real.  If the numerator
> moves too, suspect the tool before the code.**

*Recorded because I first tried to answer this with a grep and got pure noise --
`% *[a-z_]` matches printf format specifiers, so `0x%02x` read as a modulo and seven
commits appeared to "remove divisions" when they had removed format strings.*

# *** CORRECTIONS FROM THE PASS-1 PANEL (panel_20260829_190701, 9/9). ***
# Everything above this line predates them.  Three of my claims are WRONG.

## C1.  IT IS SIX REDS, NOT FIVE.  I dropped one that THIS FILE had already dispositioned.

The brief was titled "THE FIVE" and omitted `asic_badaddr rows run got=14 want=13` --
**item 5 of this very document.**  fable5 named it and drew the consequence: a round
fixing five leaves `gate_sh_rounding` red and the battery `REGRESS_FAIL`, so *"get the
battery green" fails entirely on the dropped row.*

It also observed that this document gives THREE different counts -- "The four ratchet
reds", "Six FAIL rows", "Five of the seven reds" -- so the round owes ONE derived count
with its deriver:  `sed -n '/---- FAIL rows ----/,/---- gate_ab/p' verdict_20260829_160646.txt | grep -E '^[0-9]+:[[:space:]]+FAIL' | grep -vE 'FAIL [0-9]+\. gate_' | wc -l`

> *** THE DERIVER FIRST WRITTEN HERE PRODUCED **3**, NOT 8 -- it matched only the
> three GATE-LEVEL ROLLUP lines.  The counts rule broken inside the correction
> that was fixing the counts rule.  Caught by fable5 on pass 2. ***.

*This is the counts rule broken by the file that records the counts rule.*

## C2.  THE 24 -> 21 DROP IS A CONSOLIDATION, NOT THREE REMOVALS.

I wrote "3 constant sites removed" and told a round to go NAME them.  **They were never
removed.**  The pre-#462 tree carried FOUR one-division
`fatal("  %08x", (int) d->dma_reg[N / sizeof(uint32_t)])` calls; HEAD carries the SAME
FOUR DIVISIONS as arguments of ONE `fatal()`.

**`DIAG_DIV_TOTAL` counts CALLS carrying at least one division.**  Merging four calls
into one moves the total while the division census does not change at all.

ATTRIBUTION SETTLED BY MEASUREMENT, because the two Agent seats disagreed -- opus5 said
`fb0cc78` (#490), fable5 said `7c9dd9e` (#462):

    git show 7c9dd9e -- src/devices/dev_dreamcast_gdrom.c | grep -c dma_reg   ->  9
    git show fb0cc78 -- src/devices/dev_dreamcast_gdrom.c | grep -c dma_reg   ->  0

**fable5 is right.**  One command, no tally -- the empirical-settlement rule working.

*So the DOWN instruction I proposed for the gate comment is wrong as drafted: a DOWNWARD
move can mean CONSOLIDATION, not removal, and the check is to diff the sweep's site list
against the last green tree -- at FILE granularity, since the line numbers are wrong.*

## C3.  THE DISCRIMINATOR I SAID DID NOT EXIST IS TWELVE LINES ABOVE, IN THE SAME GATE.

My Q3b asked for something better than a filename and said I could not find it.  It is
`pty.fork`, already the census basis at `gate_hygiene.sh:162`.  opus5 MEASURED it:

    whole_full   4 -> 2      (== EXPECT_WHOLE_FULL, unmoved)
    conv_anchor / conv_echo / conv_mark   23 / 23 / 23   (all unchanged)

**Row 3 goes green with NO pin moved, NO allowlist widened and NO filename exemption**,
and it subsumes the existing `readiness_predicate_test.py` exemption automatically.

And my bare exclusion was the shape **the gate itself rejects**: `:92-95` and `:347-348`
require an exemption to travel WITH a content pin on the excluded file -- *"an allowlist
entry that checks what it exempts."*  I proposed it without one.

## C4.  MY ROW-5 FLOOR IS MEASURED VACUOUS.

Under `>= 12`, deleting ONE latch's two-line guard pair PASSES at raw 13 -- restoring the
exact unbounded flood `#464` fixed.  Gutting a guard while naming the latch twice in a
COMMENT also passes at raw 15.  Six per-latch `>= 2` rows are ALSO inadequate: satisfied
by two reads and no set, while the row's label claims "one set + one read each".

opus5's shape, measured: TWO rows over COMMENT-STRIPPED code, `SET_OK == 6` and
`READ_OK == 6` -- 6/6 at HEAD, kills both mutants, and scores 0/6 on a null medium
(floor clause (c)).  The stripper already exists in the tree.

## C5.  A FINDING LARGER THAN ANY RED: `regress/artifacts/` IS IN TWO SCOPES AND OUT OF A THIRD.

Verified independently by me after opus5 raised it:

    recursive find  (py_code / probe_code population)   138
    flat glob       (_ptylist population)                59
    recursive MINUS artifacts/                           59      <- exactly equal
    pty-forking probes under artifacts/                  10      <- INVISIBLE

Two censuses recurse; a third uses a flat glob -- **evasion route #3, which this gate
condemns ninety lines earlier.**  Ten pty-forking promptless probes are invisible to the
denominator, to the promptless pin, and to the `comm -13` offender-naming: invisible to
the entire mechanism built to find promptless pty probes.

**And the hazard is SCHEDULED in the other direction.**  `CLAUDE.md` MANDATES frozen
probe copies for a comparison run.  Copying one converted probe into `artifacts/` takes
`conv_anchor` 23 -> 24 and reds the gate -- so **the next round that freezes a probe reds
this gate FOR DOING THE RIGHT THING**, which is the identical trap that produced today's
reds.

One decision fixes it: `-not -path '*/artifacts/*'` in all three censuses, KEEPING
recursion so a genuinely new subdirectory is still scanned.

# *** THE CANONICAL COUNT, WITH ITS DERIVER.  Derived 2026-08-29 after the ***
# *** adjudicator caught this document giving THREE different counts.      ***

    sed -n '/---- FAIL rows ----/,/---- gate_ab/p' verdict_20260829_160646.txt \
      | grep -E '^[0-9]+:[[:space:]]+FAIL' | grep -vE 'FAIL [0-9]+\. gate_' | wc -l
    -> 8

**EIGHT ROW-LEVEL FAILURES = 2 fixed by `#491` + 6 in this round.**

## WHY MY COUNTS DRIFTED, which is the part worth keeping

The verdict's FAIL-rows section holds **ELEVEN** lines, and three of them are
GATE-LEVEL ROLLUPS rather than row failures:

    FAIL 1. gate_build          FAIL 6. gate_hygiene          FAIL 10. gate_sh_rounding

So a bare `grep -c FAIL` over that section returns 11; over the whole verdict it
returns something else again; and counting only the rows a human recognises as
"reds" returns 8.  **Three defensible-looking greps, three different answers, and I
used a different one each time without noticing** -- "the four ratchet reds", "six
FAIL rows", "five of the seven".

> **A COUNT OVER A LOG NEEDS ITS EXCLUSIONS IN THE DERIVER, NOT IN THE READER'S
> HEAD.**  The rollup lines are legitimate output; what made them a hazard is that
> they match the same pattern as the thing being counted.  This is the
> denominator rule one level up: it is not enough to state how many the grep
> selected, when the grep is selecting two different KINDS of thing.

*The adjudicator's instruction was exact and is followed here: ONE derived count,
with the command that reproduces it, in the round's record.*
