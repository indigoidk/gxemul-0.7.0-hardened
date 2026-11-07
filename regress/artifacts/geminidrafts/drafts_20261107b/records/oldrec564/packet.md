# Reading task: oldrec564 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBOLDREC564-914b` on a line of its own.

# GXemul hardened fork -- RECORDS CHECK of one landed round's CHANGELOG block: #564 sgirekills (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator and this fork records each
fix in a CHANGELOG round block.  The block below has landed; a flagship review of it is still owed.  You cannot read files, so
judge the block AS WRITTEN.  Do not simply ratify it.  A bracketed dated note inside the block is this project's in-place
correction form (it quotes the text it corrects); it is not by itself a contradiction.

## The round block (CHANGELOG.md lines 3456-3545 of CHANGELOG_8d9df658.md; each line carries its own number -- cite those numbers)

```text
 3456| # `#564` (sgirekills, the MTE half): `do_mte_transfer()`'s five guest-reachable exits -- a stipple mode, a source buffer past TLB C, and a COPY, a depth other than 8 or a partial BYTEMASK to a linear destination -- decline the transfer and announce once per site, defended by a 68-row detector whose kill tables ran 34/34, 2/2 and 29/29
 3457| 
 3458| **The defect, witnessed at rung 3.**  `do_mte_transfer()` in `src/devices/dev_sgi_re.c` refused five transfer
 3459| parameters it does not implement with `fatal(); exit(1);` -- S1 `mode & MTE_MODE_STIPPLE` and S2 `src > MTE_TLB_C`
 3460| before `switch (dst_tlb)`, and S3 `mode & MTE_MODE_COPY`, S4 `depth != 8` and S5 `bytemask != 0xffffffff` inside its
 3461| linear arm.  Every one is reachable by an ordinary guest store: the MTE registers are guest-written, and a write whose
 3462| address carries `CRIME_DE_START` (0x800) runs the transfer (so does a START-tagged READ -- filed, `mtestartread`).
 3463| `regress/artifacts/sgirekills/witness_20261017/sgi_mte_exit_witness.py` on the unmodified `-E sgi -e ip32`, HEAD
 3464| `2951694f`: 4/9, five deaths each with only its own site's text (`witness_HEAD_2951694f.out`); the fix 9/9
 3465| (`witness_FIX_564.out`).
 3466| 
 3467| **The disposition -- member 3, decline + latched announce, at all five sites** (pass 1 unanimous: GPT-6 Astra, Grok
 3468| 4.7, GLM 5.3; Fable 5.1 a SEAT FAILURE, HTTP 429).  The `return` is OUTSIDE the latch, so every refused transfer is
 3469| refused and only the announcement is once; each site has its own bit.  S2 stays `src > MTE_TLB_C` for fills AND
 3470| copies: a fill never reads the source, but nothing establishes what the hardware does with SRC_BUF on a fill (filed,
 3471| `mtesrcfill`).  Declined: moving S5 above the linear arm's `debug()` (host-only).
 3472| 
 3473| **What ships.**
 3474| * `src/devices/dev_sgi_re.c` -- `SGIRE_W_MTE_STIPPLE`, `_SRC`, `_COPY`, `_DEPTH`, `_BYTEMASK` = `1 << 13` .. `1 << 17`;
 3475|   each site announces `... -- transfer declined (once)` with its old key phrase kept (the witness attributes on it;
 3476|   S5 gains the `[ sgi_mte:` prefix it lacked) and returns before any transfer data is written.  The enum's
 3477|   "next free bit" sentence moves to `1 << 18`.  The sixth `exit(1)` in the file, `DEVICE_ACCESS(sgi_mte)`'s width
 3478|   `else`, is unreachable and stays `sgimtewidth`'s.
 3479| * `regress/sgi_mte_decline_probe.py` (md5 422583b6) -- 68 rows in 17 sessions on the unmodified machine, real guest
 3480|   stores and loads: every refused transfer is aimed at a destination it would write, pre-painted, and read back; the
 3481|   ACCEPT side at every label; the latch (once, suppression, `return` inside the latch, shared and aliased bits --
 3482|   one session sets every pre-existing bit 0-12 first and proves it, `xbit primed`); a legal fill after a decline;
 3483|   the device's status.  Its CONTRACT names what it catches and, under NOT CLAIMED, every cell ruled outside the
 3484|   floor.
 3485| * `regress/gate_arm.sh` -- the block after the `sgi_re_width_probe` block, at depth 0: controls by name, all 68 rows by
 3486|   name, rows emitted 68, green 68, red 0.
 3487| 
 3488| **Measured** (all under `regress/artifacts/sgirekills/`).  The 53-row detector (`detector_564_20261017/`, one
 3489| instrument for both builds): HEAD 8/53 -- the controls and five ACCEPT rows green, every decline row `died` -- the fix
 3490| 53/53; null medium (`/bin/true`) 0/53.  Kill table 1 (`killtable_564_20261017/`, PRETABLE.out written before it): 34
 3491| one-edit mutants, **34/34**; table 2 (the S1 and S3 accept-side growth mutants table 1 lacked): **2/2**.  The repaired
 3492| 68-row detector (`killtable3_564_20261017/`, PRETABLE3.out before it): base 68/68, null 0/68, HEAD 10/68 (13 of the 15
 3493| new rows red; `fill b ok` and `fill c ok` are legal fills, green on HEAD too); kill table 3: 29 mutants -- the 20
 3494| latch-conditioned label exemptions of S1/S2, one alias per new bit onto a pre-existing one, S1/S2 grown to refuse B or
 3495| C -- **29/29**, each red on its own cell's row.  `gate_arm.sh`: the 53-row block 59/59 checks
 3496| (`gate_564_20261017/`, that run stopped deliberately after every sgi section passed); on the final state the whole
 3497| gate 14, **PASS, 1184 checks** (`gate2_564_20261018/gate_arm.out`, GATE_ARM_RC=0, zero FAIL), its sgi_mte block 74/74 --
 3498| the 3 controls, the 68 rows by name, emitted 68 / green 68 / red 0 (`gate2_564_20261018/sgi_mte_decline.log`, 68/68).
 3499| The shipped probe 422583b6 differs from the tabled 8928a02f in comment lines only (the pass-3 records fixes; the edit
 3500| script refused any non-comment change).
 3501| 
 3502| **Two construction defects caught before any table (L1).**  The first draft compared `lw` results -- which
 3503| SIGN-EXTEND, so the paint 0x99999999 read back 0xffffffff99999999 -- against the 32-bit literal: every `paint kept`
 3504| row read "written" on the fix and every `landed` row was vacuous (`detector_564_20261017/*.v1_signext.out`).  Then two
 3505| 14-character names in a 14-column field met the gate's two-space pattern: the field went to 16 columns (format only;
 3506| the tabled instrument was reconstructed and its md5 reproduced).
 3507| 
 3508| **The review chain -- three passes, two shared-findings passes, one repair.**
 3509| * **Pass 2** (`pass2_564_20261017/`): Astra SWC 3, Grok SWC 2, GLM SWC 3; Fable 429.  Two FLOOR breaches (L2): S1's and
 3510|   S2's `return` bypasses `switch (dst_tlb)`, so under the 2026-09-25 skipped-dispatch label clause -- its first reuse
 3511|   on a second device, fit checked -- the floor is {A, B, C, LIN_A, LIN_B} x latch {CLEAR, SET} per site, 20 cells of
 3512|   which 9 were held (`if (src > MTE_TLB_C && dst_tlb != MTE_TLB_B)` kept all 53 green); and a new latch bit ALIASED
 3513|   onto a pre-existing one escaped, because no session set bits 1-12 (`SGIRE_W_MTE_STIPPLE = 1 << 10`).  Records: a
 3514|   START-tagged READ also runs the transfer, so the fix's "the register store that carried START" was corrected.  A
 3515|   late Gemini 4 Argon reading of the same packet rediscovered both breaches.  GLM's "a fourth diff hunk was never
 3516|   shown" was refuted (four were, net +53).
 3517| * **The shared-findings pass** (`f2_564_20261017/`): Astra ALL UPHELD, GLM ALL UPHELD, Grok "1 WRONG (F9)" -- the floor
 3518|   upheld, the append recipe corrected (B and LIN_B mapped where first used, every cell repainted, linear cells at
 3519|   depth 8 / full mask / no COPY).
 3520| * **The repair**: 15 rows -- the 11 empty label x latch cells, legal tiled fills at B and C, the crossbit session --
 3521|   and the records fixes; table 3, above.
 3522| * **Pass 3** (`pass3_564_20261018/`): Grok **CLOSE**, zero breaches with its swept denominator; Astra SWC 3 (S1/S2's
 3523|   ACCEPT face with the latch SET at B, C, LIN_B, and S5's accept face after a decline); GLM SWC 3 (S3-S5's label x
 3524|   latch cells); Fable 429 (its third wall this round -- the re-fire-once rule discharged); Argon SWC 1, refuted (its
 3525|   "the bit-3 priming text is a substring of the bit-11 text" -- `for` vs `from`).
 3526| * **The shared-findings pass for pass 3** (`f2b_564_20261018/`), on one scope question with the rule texts quoted:
 3527|   **unanimous G1 OUT, G2 OUT, G3 OUT** (Astra, GLM, Grok).  The floor crosses a guard's DOMINATING predicates with
 3528|   the state its repair path reads, and the repair path never runs on the accept face; the skipped-dispatch label axis
 3529|   attaches only where the `return` bypasses the dispatch, which S3-S5's do not; the 2026-09-09 clause bounds labels
 3530|   to the guard operand's partition, never their cross with the latch.  Those cells are DISCLOSED in the probe's NOT
 3531|   CLAIMED list (clause e).  **The chain closes on pass 3**: zero floor breaches surviving adjudication, carried with
 3532|   the swept denominators.
 3533| * Records corrected in place, never in the order-proof files: `killtable_564_20261017/PRETABLE_ERRATA.txt` (8 entries)
 3534|   and `killtable3_564_20261017/PRETABLE3_ERRATA.txt` (6 entries), each quoting the text it corrects.
 3535| * Seats: the owner's roster of 2026-10-17 (Fable, Grok, Astra, GLM; Fable's adjudication HELD); Opus, agy, kimi,
 3536|   deepseek and minimax DELIBERATELY NOT FIRED.
 3537| 
 3538| **Records.**  `sgirekills` CLOSED -- its MTE half is this round, its six RE read arms were `#513`, and its sixth exit is
 3539| unreachable (`sgimtewidth`); witness `probe:regress/artifacts/sgirekills/witness_20261017/sgi_mte_exit_witness.py`.
 3540| REGRESS held for the flagship, with the row's earlier TEX question carried in its hold.  Filed: `mtestartread`,
 3541| `mtesrcfill`, `mteimplement`, `sgimteystep`, `mtedeclinecov`.  The bug file's `sgirexbit12` item gains a note: `tex xbit` primes
 3542| none of the five new bits either.  Section R: `tools/pipeline/check_probe_wiring.py`'s MANIFEST classifies the round's `.py`
 3543| files -- the detector DETECTOR (wired in `gate_arm.sh`), the witness WITNESS, the mutant writers, summarizers and
 3544| table generators TOOL, the preserved instruments RESEARCH.
 3545| 
```

## Questions -- verdict line first

1. Does the block contradict itself anywhere -- two different numbers for one quantity, a total that its own parts do not sum
   to, a claim in one paragraph that another paragraph undoes?  Quote both places, with their line numbers.
2. Which claims are stated as MEASURED but cite no artifact, or cite one only by a bare file name that could be ambiguous?
3. Which sentences overclaim -- 'every', 'all', 'never', 'exactly' -- where the block's own evidence covers less?
4. What would a reviewer checking this block against its artifacts most likely find wrong?
When you count items the block enumerates, list them by name before giving the count.

End with one line: `RECBLOCK_564: <c> CONTRADICTIONS, <u> UNCITED, <o> OVERCLAIMS`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBOLDREC564: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
