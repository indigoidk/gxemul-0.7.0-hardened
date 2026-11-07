# Reading task: closedraft_04 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBCLOSE04-4814` on a line of its own.

# GXemul hardened fork -- DRAFT THE CLOSURE RECORDS for 6 filed issues proposed for closing (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork keeps a
ledger of every filed issue.  An earlier triage pass proposed closing each row below.  Closing must be HONEST: a row closed
as documented says what was assessed and not changed; a dropped row says why it is not a defect worth a round; a row closed
as OVERTAKEN (someone else's fix removed the defect) is only closable on three conditions -- (1) a discriminating control,
measured at HEAD: neutralise the overtaking fix and this row's own symptom comes back; (2) the rows that now carry the
coverage named; (3) that control preserved at a durable path.  You cannot read files; work from the text.  Ledger at HEAD 8d9df658.

## The rows

### ROW `sh4itlbpr` -- state `open`, severity `-`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** sh4itlbpr  ITLB data array 1 is one bit too wide, and SIX shipped rows now REQUIRE the extra bit

**state_note (head):** *** FIRST EVIDENCE 2026-08-27, from a farmed codex job. The mask arithmetic is CONFIRMED exactly; the SEVERITY is lower than the seat implied, and the reason is a phrase in the manual the seat did not weigh. ***

**CONFIRMED, and recomputed here from the header's own constants rather than transcribed:** `dev_sh4.c:1020-1021` builds the ITLB data-array-1 mask with `SH4_PTEL_PR_MASK` = **0x60, a TWO-bit field**, giving 0x1ffffdfa. Narrowing PR to the ITLB's own `SH4_ITLB_DA1_PR` = 0x40 gives 0x1ffffdda. Both values match the seat digit for digit. **The extra bit is 0x20.**

**THE PRIMARY SOURCE AGREES, and it was read as PROSE, not off a figure** (`sh7750_hardware.txt:10035-10036`, section 3.7.2):
  *"In the data field, PPN is indicated by bits [28:10], V by bit [8], SZ by bits [7] and [4], PR by bit [6], C by bit [3], and SH by bit [1]."*
**Bit [6], singular** -- so for the ITLB, bit 5 is not part of PR. The sibling `sh4_utlb_da1` at `:1220-1224` keeps the two-bit mask and is CORRECT: the UTLB's PR really is [6:5].

*** BUT THE SAME FIGURE'S LEGEND (`:10062`) SAYS RESERVED BITS ARE "0 write value, UNDEFINED READ VALUE" -- SO RETURNING 0x20 IS ARCHITECTURALLY PERMITTED, NOT WRONG. *** That single clause is what moves this from 'defect' to 'fidelity nit', and no seat quoted it.

**THE SEAT'S LOAD-BEARING PREMISE -- 'no translation decision uses that bit' -- IS TRUE, BUT ONLY VIA A [... 2394 more characters not shown]

**hold_question:** (none)

**the triage pass's reason:** Architectural manual permits returning 0x20.

### ROW `gdromkeyindex` -- state `open`, severity `low`; PROPOSED: **CLOSE-OVERTAKEN**

**title:** gdromkeyindex  five mutants score a full 32/32 against #461's detector, and one of them writes the DMA arming registers from the CONTROL window

**state_note (head):** *** PARTLY STALE -- AND THE STALE PART IS THE HEADLINE NUMBER. ***
`dev_dreamcast_gdrom.c:566` (anchor `gdrom_unimpl_first`) **currently uses the correct bitmap index
and a cumulative bit update**, so there is no live bitmap corruption.

> **THE FIFTH ESCAPE IS OVERTAKEN.**  `accept dma`, `accept event` and `accept data` now distinguish
> disabled DMA; those checks arrived in `7c9dd9e` (`#462`).  **So "five mutants score 32/32 against
> #461's detector" is wrong about today's detector, and 32/32 is a historical claim** -- the row's
> title states it in the present tense.

Four gaps remain as debt: cross-window state preservation, revisiting a key after another key,
independent width/alignment discrimination, and diagnostic-text accuracy.  *No fresh escape scores
are claimed -- the seat ran nothing.*

*Evidence: codex evidence pass 2026-09-07, regress/artifacts/queueunrated/codex_bare2_20260907.txt.  Source-reading only -- no builds, gates or probes were run, so every
mutant outcome below is a static conclusion, not a fresh measurement.*

**hold_question:** (none)

**the triage pass's reason:** Core detector escapes overtaken by commit 7c9dd9e.

### ROW `gdromdriverclaims` -- state `open`, severity `-`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** gdromdriverclaims  #462's design rests on three guest-driver claims with no local artifact, and ONE of them was measured false the same day

**state_note (head):** 

**hold_question:** (none)

**the triage pass's reason:** citation re-derived and confirmed fine

### ROW `panelcite0824` -- state `open`, severity `med`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** panelcite0824  EIGHT uncited panel dirs (08-24 and 08-25) hold seat answers section G has never scoped -- including a pass 2 on a shipped commit

**state_note (head):** *** THIS ROW WAS FILED WITH THREE WRONG NUMBERS AND A CIRCULAR CITATION. The pass-2 adjudicator found all four; each is corrected here and the deriver is named so the next reader re-runs it instead of trusting me. ***

**(1) THE CENSUS WAS WRONG FOR THE THIRD TIME, BY THE OPPOSITE ERROR TO THE SECOND.** Filed as 166/76/94. Correct, suffix-aware: **174 dirs / 78 cited / 96 uncited.** My first attempt used a loose `panel_*` glob that matched `.out` FILES (229/157); my 'correction' then required `panel_<8>_<6>` EXACTLY, which silently dropped **eight real dirs carrying suffixes** (`..._024101_audit`, `..._044509_ledger11`, `..._110328_0798b90_pass2` and five more). Too loose, then too tight. **And the structure already knew** -- `check_seats_read.py:74-77` documents the suffix reality and resolves bare stems to suffixed dirs. I wrote a filter instead of reading the one that works.

**(2) THE ACTIONABLE SET IS EIGHT, NOT FOUR.** Four on 08-24, and FOUR MORE ON 08-25 that my exact-match filter could not see: `diffrec`, `ledger11`, `tailfacts`, and `0798b90_pass2`. **Two are heavyweight** (ledger11 carries a 1.29 MB codex answer; diffrec 1.07 MB) and **one is a PASS 2 ON A SHIPPED SOURCE-TOUCHING COMMIT** -- precisely the late-dissent shape where an unharvested answer reads as false unanimity.

**(3) THE OVERSTATEMENT WAS ~12x, NOT ~4x.** 96 uncited against 8 actionable.

*** (4) MY  [... 4598 more characters not shown]

**hold_question:** (none)

**the triage pass's reason:** resolved in place by stripping the citation prefix

### ROW `probeslow` -- state `open`, severity `-`; PROPOSED: **CLOSE-OVERTAKEN**

**title:** probeslow  gdrom_default_probe.py's cost is SESSIONS, not rows -- the 1800s overrun was real at 44 rows and is measured false at 52

**state_note (head):** *** AND THE FEATURE'S VALUE WAS DEMONSTRATED THE SAME HOUR, BY A SEAT THAT BUILT ONE. ***

While measuring Round 2's mutants the opus seat wrote its own probe WITH session selection
(`tprobe2.py <bin> <img> 'S1 badfmt,S4 acceptA'`) and used it immediately: for the Site A
fallthrough mutant it ran TWO sessions instead of eight, because only those two can
distinguish a decline from an accept.

**That is the argument for the feature and, read carefully, also the argument for why it
is a separate round.**  Selection is CHEAP in a purpose-built probe where it is designed
in; the cost measured here is RETROFITTING it to a 1200-line probe whose 36 sessions run
at module level.  The two facts are not in tension -- they are the same fact seen from
each end, and a future round should read them together rather than citing one.

*** A FOURTH COST FACT, MEASURED 2026-08-28, AND IT IS ABOUT THE FIX RATHER THAN THE COST: A ROW FILTER IS NOT A SMALL CHANGE TO THIS PROBE. ***

Round 2 was going to fold one in -- the owner approved it on a cost I stated -- and the estimate was wrong by roughly 10x.  Measured before building:

    session() calls at MODULE level (column 0)   36
    session() calls inside a block                3
                                                 --
                                                 39

**Skipping a row therefore means skipping TOP-LEVEL STATEMENTS.** [... 3015 more characters not shown]

**hold_question:** (none)

**the triage pass's reason:** folds into probetimebased per adjudication

### ROW `asicarray4` -- state `open`, severity `-`; PROPOSED: **DROP**

**title:** asicarray4  sizing the ASIC's four register arrays [4] instead of [3] would de-fang the whole out-of-bounds class

**state_note (head):** RAISED BY THE kimi SEAT on the #463 pass-2 panel (_scratchpad/panel_20260825_020219), via `kimi-k3:cloud` because the kimi CLI is quota-walled -- a DIFFERENT TRANSPORT, recorded as a substitute. The struct declares `pending_irq[3]`, `mask_13[3]`, `mask_11[3]`, `mask_9[3]` consecutively, so `mask_13[4]` IS `mask_11[1]` and any mask widening corrupts a neighbour silently. Padding each to [4] converts that class from CORRUPTION back to mere silent wrongness at a cost of 16 bytes. **The seat was explicit that this is a TRADE, not a fix**, and that framing is the reason to keep it: it does not make a wrong index right, it only stops it reaching another array. Weigh against `asicindexcase`, which it would also partly de-fang.  *** MEASURED AND PARTLY REFUTED 2026-08-25 by the opus5 research seat, which had first FAVOURED this option and then argued against it. *** Sizing the arrays [4] makes the `+1` translation mutant **ESCAPE** `mask9 rt`. The row's kill mechanism is that DEVICE_TICK ERASES `asserted_13` (`d->asserted_13 = ... = 0`, loop bound i<3) and the mask_9 write arm calls the tick immediately -- so at [3] the stored 0xb2 lands on asserted_13, is wiped, and the readback reddens the row. **At [4], index 3 is a real slot the tick never touches, the value survives, and the mutant escapes**: N=3 readback 0x0 (RED, killed) vs N=4 readback 0xb2 (GREEN, ESCAPES). So this option **co [... 1120 more characters not shown]

**hold_question:** (none)

**the triage pass's reason:** sizing to [4] violates hardware facts and costs a mutant kill.

## For EACH row return (a numbered block per row, its id first)

1. `AGREE` or `DISAGREE` with the proposed closure, and why in one line -- DISAGREE when the row's own text describes a live,
   reachable defect, or names work still owed.
2. If AGREE: the closure RECORD text, two to four lines, in that honest form (for OVERTAKEN: the control that would
   discriminate and the rows that would carry it, stated as OWED, never as done).
3. The ONE fact that would make closing wrong -- what someone must check before closing it.
Do not invent commits, measurements or file contents the text does not give.

End with one line: `CLOSEDRAFT_04: <a> AGREE, <d> DISAGREE`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBCLOSE04: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
