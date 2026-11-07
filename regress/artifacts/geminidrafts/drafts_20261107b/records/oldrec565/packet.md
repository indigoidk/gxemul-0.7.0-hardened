# Reading task: oldrec565 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBOLDREC565-6067` on a line of its own.

# GXemul hardened fork -- RECORDS CHECK of one landed round's CHANGELOG block: #565 wiringcliff (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator and this fork records each
fix in a CHANGELOG round block.  The block below has landed; a flagship review of it is still owed.  You cannot read files, so
judge the block AS WRITTEN.  Do not simply ratify it.  A bracketed dated note inside the block is this project's in-place
correction form (it quotes the text it corrects); it is not by itself a contradiction.

## The round block (CHANGELOG.md lines 3254-3329 of CHANGELOG_8d9df658.md; each line carries its own number -- cite those numbers)

```text
 3254| # `#565` (wiringcliff): `regress/ppc_rldicl_probe.py` is wired into gate 13 five days before its exemption would refuse every commit -- 30 checks score all 24 rows by name; floor clause (c) measured three ways, the identity body among them; the probe's records the new pin exposed are corrected
 3255| 
 3256| **The cliff.**  Section R (`tools/pipeline/check_probe_wiring.py`) held `#522`'s detector for `rldicl` writing zero,
 3257| `ppc_rldicl_probe.py`, in its EXEMPT table, dated 2026-10-22 after three re-dates by owner ruling (2026-09-18 in
 3258| `eec0f4a3`, 2026-09-24, then `04f3e7c0` on 2026-10-09).  With `d < today` it would have refused every commit from 2026-10-23.  Witness `harness:` --
 3259| the round's subject is the test apparatus: no `regress/gate_*.sh` named the probe at HEAD `69253c3c`, and section R
 3260| reported it exempt.
 3261| 
 3262| **What ships.**
 3263| * `regress/gate_ppc.sh` -- a block after the rldimi block and before the NetBSD prerequisite (`-E bareppc -M 64` needs no
 3264|   image, so a red row is recorded rather than skipped): the completion sentinel, exactly once; all 24 rows by name
 3265|   (`^name  .*ok$` once each); rows run / green / red pinned to 24 / 24 / 0; then EVERY `^SCORE ` line counted (it must be
 3266|   one) and `SCORE 24/24` read -- 30 checks when green.  Its comment carries a CONTRACT: the block transmits the probe's
 3267|   verdicts and re-derives none.  The gate's title gains "rldicl".
 3268| * `tools/pipeline/check_probe_wiring.py` -- the probe's EXEMPT tuple and its comment deleted; a dated DISCHARGED note
 3269|   beside `#536`'s and `#548`'s; the MANIFEST entry's `EXEMPT below rather than wired` marked historical; two MANIFEST
 3270|   qualifiers (below).
 3271| * `tools/precommit_check.sh` -- `SCORE_CLAIMS_MANIFEST` 33 -> 34, for the new `ppc_rldicl rows run ... 24` pin.
 3272| * `regress/ppc_rldicl_probe.py` -- records only.  Its verdict logic is unchanged: against HEAD's, its AST (docstring
 3273|   excluded) differs in ONE string constant, the `disasm total` row's printed note.
 3274| 
 3275| **Measured** (all under `regress/artifacts/ppcrldiclzero/gatewire_20261018/`).
 3276| * Gate 13, alone: PASS 140 checks, rc 0, the rldicl block's 30 among them (`gate13/`).
 3277| * The block's scoring text, extracted from the shipped gate and sourced against doctored copies of a green log
 3278|   (`controls/controls_final_20261018.out`): 13 legs, each red exactly where it should be -- the DONE line removed or
 3279|   doubled; a row renamed, turned FAIL, deleted or duplicated; a stray `ok` line; the SCORE line removed, wrong, doubled
 3280|   or contradicted -- and the pre-`#522` build's log (`02af7f3e`, SCORE 16/24) reds 11 of the 30.
 3281| * Section R (`controls/r_legs_final/`): the staged checker with the wired gate passes; HEAD's checker (tuple kept)
 3282|   reports STALE EXEMPTION; the exec line commented out reports UNWIRED DETECTOR; HEAD's checker with the gate unwired
 3283|   passes today and, at `--today 2026-10-23`, reports the probe EXPIRED -- the cliff this round removes.
 3284| * Section U: `SCORE_CLAIMS_PINNED=34`, PASS.  With HEAD's probe and the new gate it FAILED -- `STALE ppc_rldicl_probe.py
 3285|   docstring claims 16/19, pin is 24` (`controls/score_claims_u_headprobe_FAIL_20261018.out`) -- which is how this round
 3286|   came to read the probe's records.
 3287| * Floor clause (c), the null medium (`nullmedium/`): an IDENTITY BODY for X(rldicl) -- decode and retire, write nothing
 3288|   -- built in a scratch clone of `build/`: SCORE 16/24 and 11 of the block's 30 checks red; restored, 24/24, the clone
 3289|   `cmp`-clean and its binary fresh (`identity/IDENTITY.out`).  `/bin/true`: 22 of 30 red.  An absent binary reds the
 3290|   sentinel in the block's scoring text; in gate 13 `need_exec` turns it into a SKIP first.  Five rows stay green on
 3291|   `/bin/true` by construction -- `session` and `cand session` test exit status, `naive fix wrong` is arithmetic, `census
 3292|   run` counts the cells the probe drives, `census zero` counts parsed zeros -- recorded; not a breach.
 3293| 
 3294| **The records the new pin exposed, corrected** -- each beside the sentence it corrects, in the probe unless named:
 3295| * the docstring's M_NOMASK `16/19` is the 19-row figure (`pass2_20260910/opus_nomask.log:3`); on today's 24 rows it is
 3296|   19/24 (`killtable_20260910/t2/probe_M_NOMASK.raw:30`) -- section U's flag;
 3297| * `**THIS FILE HAS 19 ROWS, NOT 24**` qualified on its own line (24 since pass 2), and the second verbatim copy of `WHY
 3298|   THE SIBLING ROWS ARE NOT HERE` -- present twice since `e777ff06` -- deleted;
 3299| * the VACUITY comment's `could never fail, whatever the handler does`: `vacuous cell` is red under M_NOMASK (GPT-6 Astra),
 3300|   and under M_NAIVE, M_MASKEND and M_NOAND too, though it shares `naive fix wrong`'s CARRIED-NOT-COUNTED label (Grok 4.7);
 3301| * `every placed word` is disassembler-checked: only the control and census sessions' 196 words are COMPARED -- the
 3302|   32-bit, vacuity and candidate-row sessions' seven are disassembled and not compared, and the bogus-machine session's
 3303|   one is never placed (GPT-6 Astra, Grok 4.7, GLM 5.3) -- in the docstring, the printed note and the MANIFEST;
 3304| * `Four controls:` lists five (NL6), and the MANIFEST's t2 frozen copy is byte-identical to the shipped probe only AS
 3305|   SHIPPED AT `e777ff06` (NL7) -- both upheld by Fable 5.1 on 2026-10-16 as L4s to land when their file is next touched.
 3306| 
 3307| **Not done here, and why.**  The flagship ruled on 2026-09-11 that `naive fix wrong` be demoted to a print
 3308| (`ppcprobescorestale`); that changes the row count and belongs to its own round.  A note written after pass 2 that
 3309| redefined CARRIED-NOT-COUNTED to keep the row in SCORE contradicted that ruling and was withdrawn before commit: Grok 4.7
 3310| overturned it on F2, and GPT-6 Astra had upheld it without the ruling in its packet.  The probe's smallest escapes are
 3311| its own comparator -- `ok = True` (Grok 4.7) or `got >= want` (GPT-6 Astra) in `row()` -- which a block that scores only
 3312| ok/FAIL tokens cannot see; disclosed in the CONTRACT, and no value anchor added.  `alpha_tbi_probe.py`'s exemption comes
 3313| due the same day; it is the other session's Alpha area.
 3314| 
 3315| **The panel.**  Pass 1 on the design brief, pass 2 on the diff and the §F2 shared-findings pass, each by GPT-6 Astra
 3316| (ultra), Grok 4.7 (xhigh) and GLM 5.3; Gemini Argon gets the F2 packet when its quota window reopens.  Fable 5.1 NOT
 3317| FIRED -- held by the owner's 2026-10-17 directive; Opus, agy, kimi, deepseek and minimax deliberately not fired (owner
 3318| roster).  Flags: pass 1 3 + 4 + 7, pass 2 2 + 1 + 3, F2 3 + 5 + 4 -- every one taken, refined or rejected with its reason
 3319| (`brief_f2_body.md`, the ledger's `wiringcliff` entries).  D2 -- whether clause (c) needed the identity body -- was
 3320| settled by building it, not by vote.  A confirm pass (GPT-6 Astra) then found four wrong records in these
 3321| drafts -- the bogus-machine session's word is never placed, the exemption was re-dated three times, the 04:57 wall
 3322| was on 2026-10-18 (the same wrong date sat in two entries committed earlier today, `mapledmaaddr`'s and
 3323| `xscaleinten`'s, corrected in place), and the seats' FILE ruling did not cover the split note -- all corrected; every
 3324| measurement was re-run on the staged files (probe `9cc0ee84`, gate `7a970b9a`) and a micro-confirm closed the chain
 3325| at 0 flags (`codex_rldiclcf.txt`, `codex_rldiclcf2.txt`).
 3326| 
 3327| **Filed:** `ppcrldiclbanner` (LOW).  **Noted:** `wiringcliff` (next due: `alpha_tbi_probe.py`), `ppcprobescorestale` (part
 3328| 1 done, the demotion owed), `nullmediumlegs` (the rldicl half measured, the alpha half owed), `ppcrldiclzero`.
 3329| 
```

## Questions -- verdict line first

1. Does the block contradict itself anywhere -- two different numbers for one quantity, a total that its own parts do not sum
   to, a claim in one paragraph that another paragraph undoes?  Quote both places, with their line numbers.
2. Which claims are stated as MEASURED but cite no artifact, or cite one only by a bare file name that could be ambiguous?
3. Which sentences overclaim -- 'every', 'all', 'never', 'exactly' -- where the block's own evidence covers less?
4. What would a reviewer checking this block against its artifacts most likely find wrong?
When you count items the block enumerates, list them by name before giving the count.

End with one line: `RECBLOCK_565: <c> CONTRADICTIONS, <u> UNCITED, <o> OVERCLAIMS`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBOLDREC565: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
