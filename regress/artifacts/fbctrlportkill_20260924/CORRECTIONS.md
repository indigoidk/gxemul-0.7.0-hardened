# #549 fbctrlportkill -- false sentences in DATED artifacts, corrected HERE (not edited: their mtimes are the order proof)

Each correction was found by a seat and checked against the named file before it was written here.  The ruling that
disposes of them: `pass_v6/fable5_f2_v6.md` (the flagship seat, fired last on v6's adjudication pass).

## `PRETABLE_ADDENDUM_t6.out` (pre-registered before variant table 6)

Every RED/GREEN prediction it made held (`table6/TABLE.out`: zero mismatches).  Its CHANNEL lines -- which rows each
edit would turn red -- were wrong in four places, and its latch witness named the wrong edit (N23, N24; the panel and
dedicated grok jobs, verified against `table6/TABLE.out`):

1. **The count row catches latch periods through 107, not "up to 106".**  A re-arm of period N announces on refusal
   N+1; N = 107 re-announces on B's 108th refusal and reds the count row, and N = 108 would need a 109th refusal no
   session makes -- measured by the Opus seat: period 107 at 116/117, period 108 at 117/117
   (`opus549_measured/f2v6/TABLE_f2v6.out`).
2. **`MK_b5_7` is red on all four of B's widths**, not on sb alone (`got=0x80` at each).
3. **`MK_b9_31` is also red at sd** (`got=0xffffffff80000000`: bit 31 kept through the later refused bits).
4. **`B_mod11` is also red on P's twelve-refusal row**, which the B-count line did not name.
5. **Its latch witness `CELL_keep_l0` is the wrong edit** (`idata >= 8 && d->warned_port`): the latch is set only
   inside that branch, so it never sets, every value is stored, and B's sb read is the LAST store (0x80), not the first.
   The effect the addendum meant -- an early bad store preserved by later refusals -- is real and is shown by `MKB_03`
   (all four widths stay 0x8).

## Round records in the pass packets

* **"Six behaviour changers" (`pass_v6/f2_v6_findings.md`, N15) counts one binary twice.**  `table6`'s `BR_ge9` and
  `table5`'s `M_gt` are the same edit (md5 9b21ac29 in both tables): five NEW behaviour changers plus one re-run.
* **N20's proposed LIMITS sentence ("only K and R read DATA without re-selecting") was false** -- `PROG_R` re-selects
  PORT=5 before its DATA read; the accesses made without a fresh selector after a refusal are K's read, K's write and
  R's write.  The v6b header carries the corrected sentence.
* **minimax's premise that `fatal()` exits (N13) is REFUTED, not dropped**: `src/core/debugmsg.c`'s `fatal()` prints
  and returns (no early-out, no exit); the v6b header now states the premise the twelve refusals in P and 108 in B rest on.
* **A brief defect of the main loop's (the adjudication pass):** `pass_v6/f2_v6_brief.md` quoted the joint-cell rule's
  generating-set sentence WITHOUT its bounds; the packet-fed FLOOR votes on D1 reasoned largely from that sentence -- glm's conditionally, deepseek's and
  minimax's outright; kimi-k3's partition-asymmetry argument was SEPARATE, as the packet itself records, and the bounded
  rule answers it rather than dismissing it (this said all four reasoned from the sentence: GPT-6 Astra, confirming #549).  Disclosed
  in `pass_v6/f2b_v6_findings.md`; the carrier's sentence is now pinned ("TESTS" means masks or compares as a case).

## Provenance of the Agent-seat files (which model wrote each answer -- matched to the transcripts by text and time)

Four pass-1 files carry no provenance footer.  Matched 2026-09-25 to the writing model in each agent's transcript
(`agent_models.py`, and the answer text located in the transcript by content):

| file | written by | counted as |
|---|---|---|
| `fable5_p1.md` | claude-opus-4-8, 2026-09-24T16:07:35Z (a fallback after refusal events) | NOT the flagship seat |
| `fable5_p1b.md` | claude-fable-5-1, 16:12:11Z (the re-issue) | the flagship seat's pass-1 ruling |
| `opus5_p1.md` | claude-opus-4-8, 15:44:18Z (a fallback after refusal events) | NOT the Opus seat |
| `opus5_p1b.md` | claude-opus-5-5, 15:54:39Z (the re-issue) | the Opus seat's pass-1 answer |

The rest carry their own footers: `opus5_f2`, `opus5_close`, `opus5_close2` and `opus5_close3` are claude-opus-5-5;
`opus5_close3_FALLBACK_opus48.md` and both `pass_v6/opus5_pass_v6*_FALLBACK_opus48.md` are NOT the Opus seat (so the
Opus seat is a SEAT FAILURE on v6's own pass); `pass_v6/opus5_f2_v6.md` is claude-opus-5-5; `fable5_f2.md` and
`closing2/fable5_close2.md` (its re-issue) and `pass_v6/fable5_f2_v6.md` are claude-fable-5-1.  The pass-1 fallbacks'
MEASUREMENTS remain evidence (`opus549_measured/`); their prose is not counted as a seat.

**One seat answer was never written to disk, and is recovered here.**  The Opus seat's PASS-2 answer (agent
a86286fc69054c85b, claude-opus-5-5, 2026-09-24T16:45:07Z, VERDICT: SHIP WITH CHANGES) was READ and USED -- the F2
packet (`f2_brief.md`) cites its fourteen built variants and its findings R3, P1, D4, D5 -- but it was never saved as an
artifact.  Found while building #549's ledger records on 2026-09-25 and recovered verbatim from the transcript as
`opus5_p2.md`.  The same agent's F2 re-fire was stopped by a safety classifier before it measured anything (a seat
failure); the F2 answer is a fresh agent's (`opus5_f2.md`).

## GPT-6 Astra's confirmation (2026-09-26, `final549/codex_astra549.txt`): CONFIRM WITH CHANGES

* **v6b did NOT carry the ruling's texts.**  Ten quoted code spans in the probe's header reached the file as the byte
  0x01: the generator's replacement `\1` (`xform_v6b.py`, the `re.sub` over the ruling's `x' quotes) was eaten by the
  heredoc that wrote the script -- the carrier's backslash trap, in a file this project then called comment-only and
  AST-verified, which it was: an AST check cannot see a docstring's bytes.  v6c refills the ten IN ORDER from the
  ruling's own quotations, derived by regex from `pass_v6/fable5_f2_v6.md` (`final549v6c/mk_549v6c.py.txt`).
* **The ruling's consequence bound is false**: "a guest's FIRST out-of-range selector, once per device ... the
  pre-#549 defect, for one write".  The D1 edit changes the comparison and does not set `warned_port` on the
  accepting path, so the escape remains possible while the latch is clear.  Corrected in the header (0) and in
  `fbctrlportdebt`; `pass_v6/fable5_f2_v6.md` is the seat's answer and is not edited.
* Also corrected in v6c and the records: "each" of the sixty anchor escapes "measured" (a static walk plus six
  representative measurements); "no finite row set"; B's LIMITS sentence; the gate's one-width narrowings; "a selector
  of 8 or more"; gate 16's log vs the probe's log; four fallback answers (five); the docstring count (18,545 for v6b,
  19,449 for v6c -- 7,277 was an earlier version's); B's marginal coverage vs THE FLOOR; `lb`/`lh`; `f2v6/logs/`.
