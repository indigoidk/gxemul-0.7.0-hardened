# `#529 crimewidthkill` -- claims in THIS TREE that a later pass REFUTED

**Why this file exists, and why the refuted sentences are still sitting in the files below unedited.**

Everything under this directory is EVIDENCE: frozen instruments preserved as run, briefs preserved as sent, seat
reports in the seats' own words, PRE/POSTTABLE blocks recording what a table did. **Editing any of them would falsify
the record** -- a frozen probe that no longer matches the run it is the artifact of is worse than a wrong sentence,
because the score it produced can no longer be re-derived from it.

So the refuted claims stay where they are, and this file is the pointer. It exists because of a failure mode this
project has already measured and written into the carrier:

> *DEMOTING A NUMBER IN PLACE DOES NOT STOP IT BEING REUSED, BECAUSE THE REUSER IS SEARCHING FOR THE SUBJECT, NOT
> READING THE PARAGRAPH.*

A future round greps this tree for `TIME 4W/4R` or `twelve guest-visible cells`, lands in a frozen instrument or a sent
brief, and finds a confident sentence with nothing next to it saying it was measured false. **This file is in the
directory that grep is already searching.**

**It is a POINTER, never a second copy of the finding.** The finding lives in
`opus_close7_20260915/OPUS_REPORT.md`; the live corrections live in `../../crime_width_probe.py` (item 6) and in
`killtable10_20260915/POSTTABLE.out`. If this file and those disagree, THEY are right.

---

## 1. TIME 4W/4R is NOT equivalent at the guest -- it is guest-visible on four channels

**Refuted by:** closing pass 7, mutant `E2` (codex's, verbatim), **157/157** against repair 12, with the difference
measured on four separate channels. Evidence: `opus_close7_20260915/OPUS_REPORT.md` (section E2) and
`opus_close7_20260915/logs2/post7c_*.out`.

**Mechanism, which the refuted sentences also got wrong:** a read takes `odata` **BEFORE** its own
`crime_update_crime_time()`, so an update skipped at the 4-byte access **arrives one access LATE** rather than
"accumulating" back to the same value. Free-running `ld;sw;ld` reads `0xc6`/`0x108` on base and `0x0` under the
bypass, 6/6 each way.

| file | where | the refuted text |
|---|---|---|
| `crime_width_probe.first13.py` | item 6, lines ~106-108 | *"...and TIME 4W/4R (the high half is 0; updates accumulate)"* |
| `killtable10_20260915/crime_width_probe.table10.py` | item 6, lines ~106-108 | same sentence -- **this is the instrument table 10 ran; do not touch it** |
| `opus_close7_20260915/scripts/crime_width_probe.frozen7.py` | item 6, line ~109 | same sentence, frozen for closing pass 7's own runs |
| `opus_close6_20260915/OPUS_REPORT.md` | the per-cell table, line ~98 | *"TIME 4W, 4R \| no \| be value-equivalent (hi half 0; updates accumulate) -- notice only"* -- the close-6 seat's prediction, later measured false |
| `panel_20260915_073005/brief_sent.md` and `.packet.md` | ~367, ~567 | the same sentence, as it was SENT to the panel |

**Consequence for the next repair:** TIME 4W/4R is an **unrowed single-axis FLOOR cell**, and its rows owe the
**GAPPED** step shape (`opus_close7_20260915/scripts2/post7c.py`). The two obvious shapes were measured VACUOUS by the
seat that wrote them, and one gave a FALSE RED on a control -- which is this round's own evidence that a CHANNEL line
must be RUN against its mutant, not merely written.

## 2. "CAUGHT where a bypassed cell is guest-visible" is true only of an UNCONDITIONAL bypass

**Refuted by:** closing pass 7, mutants `K1`/`K2`/`K3` -- an accept guard grown with a conjunct on the fix's OWN latch
(`&& !(<cell> && (d->warned & CRIME_W_LEN))`) at INTMASK 4W, the REV 4-byte cell and CONTROL 8R. **Each 157/157**,
because every value row repair 12 added is measured while the latch is CLEAR.

Same three frozen instruments as above, item 6, line ~103-104; and the sent briefs at ~362 / ~562.

**The qualifier the sentence needs:** *...and the catching row runs in the BYPASS'S OWN LATCH STATE.* Eight of the 31
guest-visible ACCEPTS entries ARE already pinned post-latch; the map is derived in
`opus_close7_20260915/scripts2/session_map2.py`.

## 3. "The remaining ACCEPTS cells' accept side is pinned by the rows below" is false in three places

**Refuted by:** closing pass 7 -- `F3` at `sw +0x04` (157/157, guest-equivalent but with a host WRITE-line delta
nothing counts), `F1`/`F1b` at CONTROL `0x0201` both widths (157/157, host-log only), and **eight cells whose only pin
is an INCIDENTAL access in another session that no enumeration names**.

Same frozen instruments, item 6 line ~108; sent briefs ~367 / ~567.

## 4. "the twelve GUEST-VISIBLE cells" -- the guest-visible set has THIRTY-ONE members

Twelve is what the **ruling ENUMERATED**, not what the device exposes. Derived twice and independently in closing
pass 7 (`OPUS_REPORT.md` S1/S2b, and codex's separate 46-entry audit): of the 46 ACCEPTS entries, **31 are
guest-visible**, 10 are EQUIVALENT and 5 are host-diagnostic only.

| file | where |
|---|---|
| `killtable10_20260915/POSTTABLE.out` | FLOOR line -- **already corrected in place**, since it is a claim block rather than a frozen run |
| `killtable10_20260915/mutants529j.py` | docstring, line 4 -- *"the twelve cells repair 12's value rows carry"*: TRUE as written (it names the twelve the mutator built), and listed here only so a reader who arrives from item 4 does not mistake it for the same claim |
| `killtable10_20260915/PRETABLE.out` | lines ~8, ~37 -- *"the twelve cells the silent form is..."*: also TRUE as written, naming the twelve rowed cells |
| `panel_20260915_073005/brief_sent.md` / `.packet.md` | ~802, ~942, ~951 -- as SENT, including the uncorrected FLOOR line |

*Note the distinction this table is drawing, because it is the whole point of the item: **"the twelve cells the ruling
enumerated" is true and "the twelve guest-visible cells" is false**, and the two sentences look alike. Only the second
is refuted.*

---

## What was checked and found CLEAN

`CHANGELOG.md`, `OUTSTANDING_BUGS.md`, `_scratchpad/cl529_draft.md` and `_scratchpad/os529_draft.md` carry **none** of
these four claims. **The wrong sentences never reached the shipped records** -- they lived in the probe header, the
artifacts and the briefs, and the probe header is corrected.

*This sweep was run because the carrier mandates it -- "when correcting a claim, grep for its siblings before calling
it fixed" -- after an "un-fakeable" claim was once corrected in one place and survived in three. It found nine
sibling files for one correction, all of which correctly must NOT be edited.*


---

## 5. The FROZEN table-11 instrument still heads repair 13's block "DRAFT -- NOT APPLIED"

**Found by grok, closing pass 8**, and it is the one finding in that pass whose correct disposition is to change NOTHING.

`killtable11_20260916/crime_width_probe.table11.py` -- the instrument kill table 11 actually ran -- carries
`#  REPAIR 13 DRAFT -- NOT APPLIED.  Splice this block into crime_width_probe.py ...` at the head of the repair-13
session block. The LIVE probe (`../../crime_width_probe.py`) carried the same banner and **was corrected in place**
later the same day, after the agy and grok seats both read it.

**The frozen copy must keep it.** It is the artifact that records what the table ran, and a frozen instrument edited
after its run can no longer re-derive the scores it produced. So the two files now differ by that banner, deliberately,
and this entry is the reconciliation.

*grok stated the asymmetry precisely -- "the live probe was corrected in place later the same day; the artifact table 11
actually ran was not" -- which is the correct reading and the correct disposition in one sentence.*

## 6. `PRETABLE 11` predicted four negative controls; the table could only run one

**grok again.** `mutants529k.py` contains exactly ONE equivalent-cell member, `C_ctl4r`. The other three were
closing-pass-7 PROTOTYPE legs (`E1`/`E3b`/`F1`/`F3`), not legs of this table. Corrected in `PRETABLE.out` in place --
it is a claim block, not a frozen run.

**And deepseek showed the one it did run is vacuous**: no row drives a 4-byte READ at CRIME_CONTROL post-latch, so
`C_ctl4r`'s 188/188 is want-of-a-driver, not equivalence. **Table 11 therefore ran ZERO effective negative controls**,
which `POSTTABLE.out` now says.

## 7. "Every value row this probe had was measured with the latch CLEAR" -- FALSE, and written TWICE

**codex, closing pass 8.** `imask keeps`, `sb keeps`, `sh keeps` and the TIME controls already operate AFTER a refusal.

*The reason this one is recorded here rather than only in the probe: **the close-7 seat had already corrected the same
over-generalisation** in `opus_close7_20260915/MAINLOOP_HARVEST.md` (45 sessions, 72 post-refusal accepted accesses in
eleven of them), and I reintroduced it while writing repair 13's contract text. A sentence corrected once and rewritten
later is worse than one never corrected, because the correction is on record and looks applied.*
