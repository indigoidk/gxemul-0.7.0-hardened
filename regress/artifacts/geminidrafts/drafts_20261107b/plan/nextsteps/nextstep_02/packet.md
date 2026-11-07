# Reading task: nextstep_02 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBNEXT02-1611` on a line of its own.

# GXemul hardened fork -- THE NEXT STEP for 6 filed issues that must NOT be closed yet (a defensive project's queue work)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork keeps a
ledger of every filed issue.  An earlier pass found that each row below still names work owed, so it stays open.  You cannot
read files; work from the text.  Ledger at HEAD 8d9df658.  Proposals only.

## The rows

### ROW `gdromkeyindex` -- state `open`, severity `low`

**title:** gdromkeyindex  five mutants score a full 32/32 against #461's detector, and one of them writes the DMA arming registers from the CONTROL window

**state_note:** 

*** PARTLY STALE -- AND THE STALE PART IS THE HEADLINE NUMBER. ***
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

### ROW `gdromdriverclaims` -- state `open`, severity `-`

**title:** gdromdriverclaims  #462's design rests on three guest-driver claims with no local artifact, and ONE of them was measured false the same day

**state_note:** 

**hold_question:** (none)

### ROW `panelcite0824` -- state `open`, severity `med`

**title:** panelcite0824  EIGHT uncited panel dirs (08-24 and 08-25) hold seat answers section G has never scoped -- including a pass 2 on a shipped commit

**state_note:** *** THIS ROW WAS FILED WITH THREE WRONG NUMBERS AND A CIRCULAR CITATION. The pass-2 adjudicator found all four; each is corrected here and the deriver is named so the next reader re-runs it instead of trusting me. ***

**(1) THE CENSUS WAS WRONG FOR THE THIRD TIME, BY THE OPPOSITE ERROR TO THE SECOND.** Filed as 166/76/94. Correct, suffix-aware: **174 dirs / 78 cited / 96 uncited.** My first attempt used a loose `panel_*` glob that matched `.out` FILES (229/157); my 'correction' then required `panel_<8>_<6>` EXACTLY, which silently dropped **eight real dirs carrying suffixes** (`..._024101_audit`, `..._044509_ledger11`, `..._110328_0798b90_pass2` and five more). Too loose, then too tight. **And the structure already knew** -- `check_seats_read.py:74-77` documents the suffix reality and resolves bare stems to suffixed dirs. I wrote a filter instead of reading the one that works.

**(2) THE ACTIONABLE SET IS EIGHT, NOT FOUR.** Four on 08-24, and FOUR MORE ON 08-25 that my exact-match filter could not see: `diffrec`, `ledger11`, `tailfacts`, and `0798b90_pass2`. **Two are heavyweight** (ledger11 carries a 1.29 MB codex answer; diffrec 1.07 MB) and **one is a PASS 2 ON A SHIPPED SOURCE-TOUCHING COMMIT** -- precisely the late-dissent shape where an unharvested answer reads as false unanimity.

**(3) THE OVERSTATEMENT WAS ~12x, NOT ~4x.** 96 uncited against 8 actionable.

*** (4) MY OWN NOTE MADE AN UNCITED DIR LOOK CITED, WHICH IS A DEFECT SHAPE I HAVE NOT SEEN BEFORE. *** The first draft listed that dir's name in full (prefix included), so a suffix-aware grep found it in the ledger and scored it CITED -- **on the strength of the sentence saying it was uncited.** A record ABOUT an unread review made the review look read. The adjudicator hit this too: its own first census scored that dir cited for the same reason.

**RESOLVED BY STRIPPING THE `panel_` PREFIX in the backlog list below**, so the names stay human-readable and greppable-by-timestamp while NOT matching the citation pattern. *The adjudicator asked for the names in full; written in full they re-create the circularity, so this takes the instruction's intent -- make them findable -- by a form that cannot false-cite.*

THE BACKLOG (prefix stripped deliberately; prepend `panel_` to open them):
    20260824_030624   5 substantial answers
    20260824_034510   5
    20260824_041606   7
    20260824_124655   6
    20260825_032831_diffrec     codex 1.07 MB, minimax 61 KB
    20260825_044509_ledger11    codex 1.29 MB, deepseek 281 KB, seven seats
    20260825_100232_tailfacts   MARGINAL -- two sub-2 KB answers; may close by annotation
    20260825_110328_0798b90_pass2   *** pass 2 on a SHIPPED commit ***

**THE CUTOFF IS RE-WARRANTED, because the reason I filed was an unchecked absence claim** -- the class this project mandates checking rather than asserting. I wrote 'older dirs belong to closed rounds whose findings WERE acted on' and checked none of them. The adjudicator checked THREE across two era

**hold_question:** (none)

### ROW `gdrompiooddlen` -- state `open`, severity `-`

**title:** gdrompiooddlen  the GDROM PIO read guards ONE byte and then reads TWO -- LATENT, because no path can produce an odd length today

**state_note:** *** FOUND 2026-08-25 WHILE VERIFYING A PREMISE IN THE `gdrompionull` PASS-1 BRIEF, NOT WHILE LOOKING FOR IT. *** The brief's Q4 asked, almost as an afterthought, whether `d->cur_data_offset` is reset anywhere -- because the round had reasoned about `data_len` throughout and barely looked at the guard's OTHER operand. It is reset (`:327`, beside the NULL). But reading the guard to check that showed something else. *** THE GUARD CHECKS ONE BYTE AND THE BODY READS TWO. *** Verified by reading, three lines:   (1) `dev_dreamcast_gdrom.c:611` -- `if (d->cur_data_offset < d->data_len) {`   (2) `:612-613` -- `odata = d->data[d->cur_data_offset ++];` then `odata |= (d->data[d->cur_data_offset ++] << 8);` -- **two increments, one bounds test**   (3) `alloc_data` `:309` -- `malloc(d->data_len)`, **exactly `data_len` bytes, no padding, no rounding**. So at `cur_data_offset == data_len - 1` the guard PASSES, the first read is the last valid byte, and **the second read is `d->data[data_len]` -- one byte past the allocation**. *** REACHABILITY, STATED AS WHAT IS READ AND WHAT IS OWED. *** READ: `data_len = d->cnt` (`:307`), and `d->cnt` is GUEST-WRITABLE A BYTE AT A TIME -- `:704` sets the low byte from a CNTLO store and `:712` the high byte from CNTHI, so an ODD count is expressible. The two subsequent adjustments do not remove oddness: `:409-410` only replaces `cnt` when it is ZERO, and `:486-487` only rewrites the single value 65536. **OWED: a measurement that an odd `cnt` actually survives to `alloc_data` on a path a guest can drive.** The existing `gdrom_pio_null_probe.py` already stages commands through these registers and could answer it with two extra stores; I have NOT run it, and this row does not claim the defect is reachable until that runs. *** WHY THIS IS A DIFFERENT DEFECT FROM `gdrompionull` AND MUST NOT BE FOLDED INTO IT. *** That row is `data` NULL while `data_len` lies -- a state-invariant violation whose fix is one assignment in the tail. This is an OFF-BY-ONE in a bounds test, on a path where `data` is a perfectly valid pointer and `data_len` is honest. Different fix design (`< data_len` becomes `+ 1 < data_len`, or the read becomes width-aware), different oracle (a heap over-read, not a SIGSEGV), so under the reopening rule they are separate rounds. **Note the two interact in the safe direction: `gdrompionull`'s fix sets `data_len = 0`, under which this guard is false and the over-read cannot occur on THAT path.** It does nothing for the odd-count path. *** AND UNLIKE THIS DEVICE'S OTHER OUT-OF-BOUNDS ISSUES, ASan SHOULD SEE THIS ONE. *** The file's own comment at `:272` records that ASan cannot detect its member-to-member overrun because that is intra-object inside one malloc. **This is a read PAST a malloc'd buffer's end**, which is the case ASan is built for -- so `build-asan/` is a real second oracle here, where for the aliasing family it was not. That is worth testing early because it is cheap and because a positive ASan result would 

**hold_question:** (none)

### ROW `fbclearidempotent` -- state `open`, severity `-`

**title:** fbclearidempotent  the DC21285 says a timer clear has no effect if the interrupt was already clear, but the write arm reloads a periodic timer unconditionally

**state_note:** PRE-EXISTING, not introduced by `#474`.  Named by the pass-2 codex seat, which said
explicitly that it *"deserves a separate filing, not an untested expansion of #474"* -- and
that is the disposition taken.

Datasheet, section 7.3.42: *"The write has no effect if the associated interrupt was
already clear."*  The model reloads the counter whenever the periodic bit is set,
regardless of whether anything was pending.  Needs a row of its own and a reading of what
the reload is actually for.

**hold_question:** Is `reload_timer_value()` at TIMER_x_CLEAR a MODELLING SHORTCUT standing in for the hardware's automatic reload-at-zero, or is it modelling the Clear write itself?  The fix differs: if a shortcut, guarding it on `pending > 0` is right but for a different reason than the datasheet gives; if not, the guard changes when periodic timers reload.

### ROW `gdromdefaultstatusless` -- state `open`, severity `-`

**title:** gdromdefaultstatusless  gdrom_default_probe.py's session() calls waitpid and DISCARDS the status, so NO row in 52 can tell a clean exit from a signal from a decline

**state_note:** *** MATERIALLY ADVANCED BY #490 AND THIS RECORD DID NOT KNOW.  Added 2026-08-29 after a
pass-2 seat found the gap -- the gap-closes-itself shape. ***

`#490` added TWO rows to `regress/gdrom_default_probe.py` that bear directly on this row:
**`stale quiet`** (the two anchored decline regexes must BOTH read zero on a session that
sends a well-formed packet) and **`stale how`** (the session must end `exit0`, read from the
exit status rather than from `alive`).

`stale how` closes something this tree had left inert: **`how` had been threaded through 37
call sites and NO ROW READ IT.**  `alive` is False only when a read fails inside a budget
window, so it is true of a hung emulator, a frozen one, and -- measured -- one already killed
after the last budget check.  The exit status cannot be fooled that way.

**HONEST LIMIT: neither new row has a MEASURED RED on disk yet.**  The preserved blinding
artifacts predate them (58-row era).  One rot-packet run of the 60-row probe reds
`stale quiet` and discharges both under this project's own bar that a row is discharged by a
measured kill, not by existing.  Owed before #490 closes.

*(`stale how`'s kills-annotation was also FALSE as first written -- it claimed floor clause
(b), but that session sends a CORRECT packet reaching neither de-fatalised site, so a
reinstated exit(1) leaves it exiting 0 and the row green.  Corrected in-round.)*

FILED 2026-08-27 while designing gdromexitsix Round 2, and it is that round's FIRST obligation rather than a later tidy-up.

MEASURED 2026-08-28 on the committed build (regress/artifacts/gdromexitsix/challenge_freeze_20260828/): a mis-assembled packet (cmd[0]=0x31) scores 55/58, and the three rows that fall -- `nodata stale`, `stale says`, `stale idle` -- ALL report `died`. Their channel is process termination.

*** SO ROUND 2 BLINDS THEM BY SUCCEEDING. *** De-fatalising `default:` stops the host dying, all three revert to their C0 values, and the probe scores 58/58 on a mis-assembled packet -- which is also what a CORRECT packet scores. That is worse than vacuous: a future maintainer whose test packet rots gets a clean run.

THE PROBE'S OWN HEADER ALREADY SAID SO, before this round existed: *'THE SURVIVAL ROWS DETECT PROCESS TERMINATION ONLY ... they are true of an emulator that is HUNG, one that is FROZEN, and, measured, one that has ALREADY BEEN KILLED.'* The #489 pattern exactly -- the governing sentence present in the file, unconsulted at row-writing time.

*** THE SENTENCE ABOVE PREDICTED THAT ONE ROT-PACKET RUN 'reds `stale quiet` and discharges
BOTH'.  THE RUN HAPPENED AND REFUTED THE SECOND HALF.  Corrected 2026-08-29. ***

`regress/artifacts/gdromexitsix/rot_20260829/` -- post-fix binary, one-line frozen-probe edit
(packed format byte 0x20 -> 0x21):

    base.log   GDROM_DEF_RESULT=60/60    stale quiet  0 vs 0      ok
    rot.log    GDROM_DEF_RESULT=59/60    stale quiet  1 vs 0    **FAIL**

The two `GDROM_DEF_VECTOR` lines differ in EXACTLY ONE POSITION -- discrimin

**hold_question:** (none)

## For EACH row (a numbered block, its id first)

1. The ONE concrete next step that would resolve it, as exactly one of: FIX-ROUND (a code change, with its site),
   MEASUREMENT (what to run and what result settles it), READING (a question a careful reading of named code or a manual
   answers), RECORD (a correction or closure note), OWNER-DECISION (the question, phrased so it can be answered).
2. If it is a READING or a RECORD that the text above already settles, DRAFT it now (two to six lines).  Otherwise say
   what the step needs that is not in the text.
3. Whether it can be COMBINED with another row in this packet (same device, same next step).
Do not invent measurements, commits or file contents.

End with one line: `NEXTSTEP_02: <f> FIX-ROUND, <m> MEASUREMENT, <r> READING, <c> RECORD, <o> OWNER-DECISION`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBNEXT02: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
