# Reading task: F2: shfcnvsdfpul (Argon) (Gemini web; 2026-11-02)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBF2SHFCNVSD-9b3e` on a line of its own.

# ADJUDICATION PASS (F2) -- `shfcnvsdfpul` (#576): the panel shares its pass-2 findings; adjudicate them

Fired 2026-11-02 17:5x.  HEAD `987cb596`.  Roster (owner 2026-11-02): GPT-6 Astra, Fable 5.1, glm-5.3, Argon (Gemini web), Grok 4.7.
**Astra is on its WEEKLY wall from the hotmail login** ("try again at Nov 8th, 11:24 AM") after answering pass 1 on its third attempt; its
pass 2 and this adjudication are OWED, recorded as SEAT WALLED, not as agreement.  **The owner has ruled (17:4x) that the commit HOLDS
until Astra answers** (Nov 8, or a gmail Codex login).  Fable 5.1 ADJUDICATES this pass (the owner's 09-25 rule: codex walled means Fable
adjudicates and Astra confirms later); the other seats answer the three questions below.  Fable: F4-F7, F9 and three of the pass-2 changes
are yours -- disclosed self-review, be harder on them.

## READ THIS FIRST

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/` at HEAD `987cb596`.**  The diff is still in the scratch clone; no project tree is edited.
Packet-fed seats: everything you need is inlined.  **VERDICT LINE FIRST AND LAST**: `F2 VERDICT: RATIFY / RATIFY WITH CHANGES (<n>) /
NOT RATIFY`.  Count the arguments, not the seats.

## 1. Pass 2 as answered (`_scratchpad/w576/pass2_20261102/`)

| seat | verdict | where it stands |
|---|---|---|
| Argon (Gemini web) | SHIP | all five questions answered yes; no finding; format miss on the machine line (reply real, 2,137 b) |
| glm-5.3 | SHIP WITH CHANGES (2) | contract escape list incomplete (DRn value at DR0; FR=1; reserved RM); relabel `ftrcS-nan`; gate prose "17" stale |
| Grok 4.7 | SHIP WITH CHANGES (3) | the Q3 escape (DRn stores suppressed at DR0); the preserved mutator does not parse; records (low word, PR class never filed, gate prose) |
| Fable 5.1 | SHIP WITH CHANGES (3) | preserved mutator broken (artifact integrity); destination-axis overclaim + state axes undisclosed; four record sentences (PRETABLE timing, low word, "mis-copied", indefinite by reading) |
| GPT-6 Astra | WALLED (weekly) | owed |

Every seat: the one-line product diff is right and complete; every score in section 5 of the pass-2 packet reconciles with its raw log
(Fable and Grok opened all eleven `.raw` files); no floor cell is open.

## 2. Findings P1..P13, attributed, with MY DISPOSITION and what changed

| # | finding | raised by | disposition |
|---|---|---|---|
| P1 | `regress/artifacts/shfcnvsdfpul/killtable_20261102/mutate576.py` as preserved did NOT PARSE (a real newline inside the M_gm string: the heredoc backslash trap); it was copied at 17:24:47, BEFORE its 17:25 repair, so the preserved table was not reproducible from the preserved script; `KILLTABLE.log` carries the honest `M_gm APPLY-FAILED` then `applied M_gm` | Fable, Grok | **ACCEPTED, DONE 17:4x**: the parsing copy replaces it (`cmp` clean against `_scratchpad/w576/mutate576.py`; `ast.parse` ok); the round block gains the clause "the first M_gm apply failed on a malformed string and was repaired before the leg ran" |
| P2 | the contract's "a destination-keyed re-introduction is seen from both sides" OVERCLAIMS: true of the measured {DR0, not DR0} split on the FPUL channel, false of the register: a FPUL store keyed on DR4..DR14, or the DRn stores SUPPRESSED at DR0 (Grok's Q3 edit, first differs on the table's own `0.1` input), keep all 52 rows green | glm, Fable, Grok | **ACCEPTED as DISCLOSURE** (clause (e): the body tests nothing, so no floor cell is owed): the sentence now reads as in section 3; the DRn value is read at DR2 only; DR4..DR14 and a DR0-suppressed DRn store are named as escapes.  Row addition / re-targeting -> D1 |
| P3 | undisclosed STATE axes: FPSCR.FR=1, the reserved RM encodings 10/11, FPSCR.SZ, cause/enable/flag bits, a delay slot -- no row varies any | glm, Fable | **ACCEPTED**: named in the contract sentence (section 3) |
| P4 | the existing row `ftrcS-nan qNaN+` is mislabelled by the SH-4 convention (0x7fc00000, fraction MSB set, is SIGNALING) | glm (relabel now), Fable (F9), Grok | **ACCEPTED, DONE**: renamed `ftrcS-nan sNaN+` with a `#576` comment; oracle unchanged; the gate's loop matches on `ftrcS-nan` |
| P5 | gate prose stale in the same diff: "EXACTLY 9 of the 17 vectors" and "36 vector-mode pairs: 17 vectors x 2 modes" | glm, Grok, Fable | **ACCEPTED, DONE**: "9 of the 25 vectors (17 until #576 ...)" and "52 vector-mode pairs since #576 (36 before it)" |
| P6 | "`PRETABLE.out` written 17:18, before the base leg ran" is unsupported: the base leg's log was complete at 17:18:13 (so it started about 17:17:43), and the in-place correction at 17:29 destroyed the file's own mtime, the order proof the mandate relies on | Fable | **ACCEPTED**: the "17:18" literal is WITHDRAWN (a hand-written time, the frozen-number class).  What is established: PRETABLE.out was written by the tool call immediately preceding the base-leg launch in the same response, and `IMPLEMENTATION_PLAN.md` (mtime 17:15:08, now preserved beside the table as `IMPLEMENTATION_PLAN_20261102_1715.md`) carries the base, fixed and mutant predictions before any leg ran -- and predicts M_g CORRECTLY, where PRETABLE three minutes later inverted it.  The record cites the plan for the predictions and states the mtime loss.  Process note for the carrier's PRETABLE rule: write a correction to a SIBLING file, never into PRETABLE.out |
| P7 | "0x3dcccccd ... the one input with a nonzero low word" is false: `snan` widens to the all-ones NaN whose low word is 0xffffffff (`M_h.raw` measured it landing in FPUL) | Fable, Grok, glm | **ACCEPTED**: "the one NUMERIC input with a nonzero low word" |
| P8 | "the FTRC store mis-copied" is an inference (`git log -L` shows only the import), stated as fact in the product comment and the record | Fable | **ACCEPTED**: the product comment now says "the same store FTRC makes, apparently copied here" (final text in section 3); same in the record |
| P9 | "the host's indefinite 0x80000000 for finite values of 2^31 or more" is by reading (no row has such an input); measured only for Inf and NaN | Fable | **ACCEPTED**: marked "by reading, not rowed" in the record |
| P10 | "filed once as a class" for the PR-reserved encodings is FALSE: pass 1 ordered the filing, no row exists in the ledger or the bug file | Grok | **ACCEPTED**: a new row `shfpprreserved` is OPENED in this round's records: FCNVSD/FCNVDS at PR=0 (manual :10883, :10770) and FIPR/FTRV at PR=1 (:11251, :12852) convert instead of raising the reserved-instruction exception; FSRRA (:3279-3294) is the one handler that enforces its PR restriction; LOW, WRONG-RESULT |
| P11 | the M_b binary's md5 equals the HEAD binary's (`b76a7799a3ea` in both headers): clause (b) holds at the BINARY level; and PRETABLE's CHANNEL line names `M_e` (an RZ-only store) which was never built | Fable | **ACCEPTED**: both recorded; M_e is "caught by construction (every row runs both modes), not built" |
| P12 | the probe comment attributes the FD/PR sentence to "Astra, pass 1", but "Astra's pass 1 produced no answer" | Grok | **REJECTED**: Grok read the pass-1 directory before Astra's THIRD attempt landed (17:3x, `codex3/codex_shfcnvsdp1c.txt`, 12,359 b, PROCEED WITH CHANGES (3)); the attribution is correct |
| P13 | F8 (keep `inf`): Fable now agrees the rejection of its drop was right -- a leg is about 30 s so the two sessions cost about a second, and `inf` is the only row that reds an Inf-only re-introduction | Fable | **SETTLED**: `inf` stays |

Also from pass 2, recorded without a change: the only route by which the fix could alter DRn is a compiler having exploited the removed
UB on HEAD for Inf/NaN/overflow inputs -- unmeasured, in the defined direction, and HEAD's measured DRn halves for 0.1 equal the fixed
build's (Fable Q1).  The gate names are regexes (`.` in `1.5`, `0.1`): harmless today, noted (Fable, Grok).

## 3. The texts as they now stand (changed since pass 2; comment-only, the instrument the table measured is unchanged)

Product comment (replaces the pass-2 packet's section 1 comment; the deleted line is the same):

```c
	/*  #576: FCNVSD reads FPUL and writes DRn only (sh4_programming.txt
	    9.29, :10866-10871).  Upstream also stored (int32_t) op1.f into
	    fpul here -- the same store FTRC makes, apparently copied -- so a
	    guest reading FPUL after an FCNVSD saw a truncated integer.
	    Removed; nothing else in this handler changes.  */
```

Probe contract (the `#576` comment block in `sh_rounding_probe.NEW.py`, the destination and state sentences):

```
    #  `0.1' targets DR0 (0xf0ad) while the others target DR2 (0xf2ad), so a FPUL store keyed on
    #  {DR0, not DR0} is seen from both sides of THAT split (measured: M_g 42/52, M_gm 50/52); the
    #  DRn VALUE is read back at DR2 only, and destinations other than DR0 and DR2 are unrowed,
    #  so a store keyed on one of DR4..DR14, or a DRn store suppressed at DR0, escapes this
    #  table (pass 2: Fable, Grok); both halves of the destination pair are seeded with the
    #  sentinel.  Likewise unrowed STATE axes: FPSCR.SZ, FPSCR.FR, the reserved RM encodings
    #  10/11, the FPSCR cause/enable/flag bits, and a delay slot -- no row varies any of them.
    [...]
    #  row runs with sr.FD clear and FPSCR.PR set: the FD-set path (the FPU-disable exception)
    #  and the PR=0 reserved encoding are not rowed here (Astra, pass 1; the PR=0 class is filed
    #  as `shfpprreserved').
```

## 4. Disagreements D1..D2 -- each side in its own words, my ruling, its warrant

**D1 -- destination coverage: disclose, re-target, or add rows?**
* Grok: "The row that would catch the DR0 write is a `dr0 hi` / `dr0 lo` pair ... Clause (e) allows a sentence instead of those four
  sessions.  Write the sentence."
* Fable: "Every one of these is clause (e) by the rule's letter ... Optional, L1 pre-ship, if the adjudicator wants coverage rather
  than disclosure: re-target `inf` to DR14 (0xfead) and `snan` to DR8 (0xf8ad), zero added sessions, and re-run the ten legs ... I own
  this gap" and "disclosure is the honest terminal form whatever the owner decides about re-targeting."
* glm: "Fix: one sentence each in the probe's #576 comment, zero sessions; or close (a) with a `dr0 hi`/`dr0 lo` pair."
* **My ruling: DISCLOSE (section 3), no re-run.**  Warrant: the floor is one cell (sr.FD = 0), the body tests nothing, so the
  destination family is clause (e) -- "a filter may reject or repair a row; it may demand a new row only for a floor cell"; and the
  destination family has eight members, which six FPUL rows cannot close, so disclosure is the terminal form even after a re-target.
  The re-target is CHEAP (about six minutes) and would widen the measured split from {DR0, DR2} to {DR0, DR2, DR8, DR14} -- the
  adjudicator may order it; if so the table of record is re-run on the re-targeted instrument and the record names both runs.

**D2 -- the timing record (P6): withdraw the time, or re-run with a fresh PRETABLE?**
* The honest form (Fable): "`IMPLEMENTATION_PLAN.md` (17:15:08) carries the base, fixed and mutant predictions before any leg ran ...
  Write that."
* The alternative: re-run the whole table with a freshly written PRETABLE whose mtime survives.
* **My ruling: withdraw the literal and cite the plan** (section 2, P6).  The predictions' priority is established by an artifact that
  predates every leg; re-running would manufacture an order proof for a table that already exists.

## 5. What is still OWED, and where I might be fooling myself

* Astra's pass 2 and its confirmation of this adjudication (weekly wall; Nov 8 or a gmail login).  **The commit holds for it by owner
  ruling.**
* Application: the diff and the two detector files are NOT yet in any project tree.  Owed at landing: `GXEMUL-SEC` + `est/`
  byte-identical; `build/`, `build-asan/`, `/tmp/gxsec-build` propagated and REBUILT with the two-part clearance per tree; the SH gate run
  end to end on the applied tree; the gate file staged from the HEAD-based copy (the working copy's three unrelated hunks stay out).
* The probe comment changed after the table ran (comment-only; `ast` row list identical; both copies preserved beside the table).  If
  the adjudicator orders D1's re-target, the table re-runs.
* I accepted twelve of thirteen findings.  That is a suspicious number and agreement is not evidence -- question 2 below.

## 6. The three questions

1. Adjudicate P1..P13 and D1..D2: UPHOLD / OVERTURN / REFINE / CANNOT SETTLE, one line each with a reason.
2. WHICH OF MY ACCEPTED DISPOSITIONS IS WRONG?  I accepted twelve of thirteen; name the one most likely wrong and why.
3. WHAT DID ALL OF US MISS?  You now have the whole panel's output and the measured table.

End with `F2 VERDICT: RATIFY / RATIFY WITH CHANGES (<n>) / NOT RATIFY`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBF2SHFCNVSD: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
