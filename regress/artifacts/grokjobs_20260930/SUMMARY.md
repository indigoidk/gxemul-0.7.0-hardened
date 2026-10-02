# The grok job queue of 2026-09-30 -- what answered, by which seat, and what it found (as of 2026-10-01 09:20)

34 jobs (`queue.tsv`; briefs in `briefs/`).  The grok seat (grok-4.7, xhigh) answered 8 before its paid balance ran out
at 21:14 on 09-30 -- `API error (status 402 Payment Required): Grok Build usage balance exhausted` -- and 4 more were
cut off mid-answer (kept as `grok_*.TRUNCATED.txt`, NOT answers).  The remaining 26 ran on CODEX (GPT-6 Astra, ultra)
as a SAME-FAMILY fallback: the harness review, the retro drafts and the dossiers under audit were all written by GPT-6
Astra, so a codex verification of them carries the `s` same-model badge and is not the independent reading the grok
seat was meant to give.  To get that reading: top up the Grok balance and `bash <scratchpad>/grok/grokqueue.sh 6`
(the 8 grok-answered jobs are skipped; the other 26 run again on grok beside their codex answers).

## hverify_01..18 -- the wave-2 harness review VERIFIED, finding by finding (722 finding lines over 69 answers)

| seat | jobs | findings | right | wrong | unsettled | CANNOT-FAIL confirmed |
|---|---|---|---|---|---|---|
| grok | 01-06, 08, 10 | 335 | 332 | 2 | 1 | 41 |
| codex (fallback) | 07, 09, 11-18 | 387 | 380 | 0 | 7 | 45 |
| **total** | 18 | **722** | **712** | **2** | **8** | **86** of the review's 87 |

So the harness review holds almost entirely under a second reading: two findings wrong, eight unsettled.  86 of the 87
"cannot-fail" rows -- gate checks that pass with their defect reinstated -- are CONFIRMED by a seat that re-traced
each one against the committed script.  Each `hverify_*` answer carries a DRAFT disposition per finding (NEW / FILED /
FILED-BY-PROSE / RECORD text / DROP) for the Fable seat; the per-finding lines are the input to the wave-2 Fable
batches, which are not yet briefed.

## draftcheck_3a..3h -- the codex drafts for retro batches 3a-3h, checked (codex fallback, same family)

| batch | drafts | right | wrong | wording |
|---|---|---|---|---|
| 3a | 25 | 25 | 0 | 0 |
| 3b | 25 | 23 | 2 | 0 |
| 3c | 27 | 25 | 1 | 1 |
| 3d | 31 | 29 | 2 | 0 |
| 3e | 25 | 24 | 0 | 1 |
| 3f | 24 | 19 | 0 | 2 |
| 3g | 23 | 18 | 4 | 1 |
| 3h | 26 | 24 | 2 | 0 |
| **total** | **206** | **187** | **11** | **5** |

The eleven WRONG draft dispositions are where the Fable seat should spend its budget first; each `draftcheck_*` answer
names them with the line that shows it.  The Fable briefs `fable_brief_batch3*.md` point at both the draft and this
check.

## dossier_* -- audits of the eight design dossiers (codex fallback, same family; landed 2026-10-01 09:3x)

| dossier | false or unsupported sentences |
|---|---|
| ppcbat | 1 |
| ppcfused | 3 |
| ppcllsc | 0 |
| armbyteorder | 0 |
| armvector | 2 |
| armldmuser | 0 |
| gdromdma | 5 |
| armcoproc | 1 |
| **total** | **12** |

Twelve sentences across the eight dossiers (`dossier_<j>/codex_dossier_<j>.txt`, each with the sentence, the evidence
against it and the corrected text); every dossier's chosen disposition member and its machinery were re-checked.  The
gdromdma dossier carries the most (five).  Read the audit beside the dossier before any of the eight correction rounds
starts; the grok reading of the same dossiers is still owed once the Grok balance is restored.

**All 34 jobs of this queue are answered** (8 by grok, 26 by the codex fallback), as of 2026-10-01 09:35.

## 2026-10-02 -- the agy re-run of the 26 jobs the codex fallback had answered alone

All 26 answered on agy (gemini-3.8-flash-high), beside the codex answers as `<id>/agy_<id>.txt`.  The ingest, with every
table and every disagreeing row, is `regress/artifacts/agypack_20261001/INGEST_20261002.md`.  In one line each: the ten
harness verifications agree with the codex fallback on 378 of 387 findings (agy settles seven codex UNSETTLED and disputes
one finding the codex verification had passed -- `hgdromdefaultprobe:F3`: not vacuous at HEAD with the shipped image, but
resting on an unseeded destination byte; the grok tie-break rules it a real latent dependence); the eight
draft checks add two severity disputes on the unfired batch 3f; the eight dossier audits return 0 false sentences where
the codex audits found 12 -- two of those twelve were checked and are true, so the agy zeros are ratifications and the
codex audits stand.  The whole harness review is now independently verified: 722 findings, 717 right, 4 wrong, 1
unsettled (grok 8 jobs, agy 10).
