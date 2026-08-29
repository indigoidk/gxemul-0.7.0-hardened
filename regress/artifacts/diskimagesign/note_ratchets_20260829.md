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
