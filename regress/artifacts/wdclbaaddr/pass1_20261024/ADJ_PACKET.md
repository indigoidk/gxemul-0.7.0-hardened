# T4 `wdclbaaddr` (-> #572) -- PASS-1 ADJUDICATION PACKET (the §F2 shape), 2026-10-24 18:3x, main loop 087a90

PROJECT FRAMING.  GXemul is a computer-architecture emulator; this fork is a software-correctness hardening effort on the
emulator's own C device models.  This round corrects a DECODE defect in the IDE/ATA disk model: an LBA-mode request is served
from the cylinder/head/sector reading of the same taskfile bytes because the LBA flag is decoded from bit 5 (ATA: bit 6) and
the LBA28 formula is compiled out.  Tree under review: `GXEMUL-SEC/src/` at HEAD cc1f69cc (`src/devices/dev_wdc.c` unchanged
since e16a8b7c, identical in the working tree and in `est/`).  Ignore any other `src/` under the project root.

YOU ARE ADJUDICATING, NOT RE-REVIEWING.  Seven seats answered the pass-1 brief (`packet.md` here; the drafter's 35 NOTES in
`drafter_NOTES.md`).  Below: every finding consolidated with the MAIN LOOP'S DISPOSITION, then the DISAGREEMENTS with each
side in its own words, then the questions.  Open the seat answers in THIS directory to check any disposition:
`codex_t4p1.txt` (Astra), `grok_t4p1.txt`, `argon_agy_t4p1.txt`, `ollama_glm_t4p1_Q12.txt` / `_Q34.txt`,
`ollama_deepseek_t4p1_Q12.txt` / `_Q34.txt`.  The witness: `../witness_20261024/` (RESULTS_base.txt, WITNESS.md, RUN_IDENTITY.txt,
the frozen probe).  Do not build or run anything.  Do not propose reproduction recipes.

VERDICT LINE FIRST: `ADJUDICATION: CONFIRM | CONFIRM WITH CHANGES | REJECT`, then "WRONG DISPOSITIONS: <ids or none>", then the
numbered answers.  Mark each claim READ (opened the file) / DERIVED / NOT CHECKABLE.

## 1. THE SEATS (verified by content; two Argon sections are NOT credited)

| seat | verdict | credited |
|---|---|---|
| GPT-6 Astra | READY WITH CHANGES | all |
| Grok 4.7 | READY WITH CHANGES | all (read the WORKING tree: its `diff_wdc_identify.c` line numbers are WT numbers, HEAD's are 5606-5637) |
| Gemini 4 Argon (agy) | READY WITH CHANGES | Q1, Q2(a-c), Q3(a), Q3(c-e), Q4.  **NOT credited: Q2(d) P15 and Q3(b)** -- they describe a `--expect` flag, a `regress/check_probe_wiring.py` with a STANDALONE list and a "Gate 10 at gate_offline.sh:1049-1069"; none exists (the checker is `tools/pipeline/check_probe_wiring.py`, gate 10 is `gate_sh_rounding.sh`, those gate_offline lines are the selfmutant block).  Its `row_484_read_cap_holds_on_lba_path()` exists neither at HEAD nor in the WT (grep 0/0).  Its cobalt rig: `machine_cobalt.c:105` adds `vt82c586_ide`, but no cobalt test exists in `regress/` -- not a battery rig. |
| GLM 5.3 Q1-2 / Q3-4 | READY WITH CHANGES | all; arithmetic re-derived by enumeration |
| DeepSeek v4-pro Q1-2 / Q3-4 | NOT READY / READY WITH CHANGES | all |
| Fable 5.1 | HELD (owner) | `fable5.HELD.txt` carries the hold question |
| kimi, minimax, Opus-seat | NOT FIRED (roster) | `roster_NOT_FIRED.txt` |

## 2. MAIN-LOOP CHECKS (measured by reading or running; the seats' claims were tested against these)

M1 `dev_wdc.c:936-938/:915-923` the data ring is reset on every command.  M2 `:967-973` READ is served synchronously.
M3 geometry 16/63 (`diskimage.c:270-271`), cylinders rounded up (`:295-297`): 4096 sectors -> capacity 5040.
M4 the base clone is HEAD-equivalent for `dev_wdc.c` (md5 71407161); `RUN_IDENTITY.txt`'s `6159736b` is the binary's byte size.
M5 words 57-58 and 60-61 already carry `total_size / 512` (`:433-442`).  M6 `wdcreg.h:193-195` `WDSD_IBM 0xa0 / WDSD_CHS 0x00 /
WDSD_LBA 0x40`.  M7 `wdc__write()` stores `write_offset` at `:572`, after the `#if 0` block.  M8 `d->head` has one writer,
`:2017` `idata & 0xf`.  M9 CHANGELOG `:31193` carries #405's "never reaches an offset computation"; `_scratchpad/ata2_x3t10_948d.txt`
exists (2026-09-10) while `dev_wdc.c:1081-1082` and `gate_offline.sh:1525` say no ATA document is in the tree and `:640` cites it.
M10 the witness (17:03, committed build, before any edit): lba 70 -> tag 69, lba 256 -> tag 1007, lba 0 -> zeros, the LBA-70 write
landed at index 69; CHS rows and SDH readback green; 490/490 encodings.

## 3. DISPOSITIONS (accepted unless marked OPEN; seat positions by answer-file:line)

A1 DECODE: `lba` = bit 6 (`WDSD_LBA`), drive bit 4, head bits 3-0 unchanged.  All seven.  ACCEPTED.
A2 READBACK MECHANISM -- see D1.
A3 ARITHMETIC: 64-bit multiply at both sites, the CHS line's `(int64_t)` idiom, `offset = 512 * (int64_t)(((d->head & 0xf) << 24)
   + (cyl << 8) + d->sector)`; the two `printf`s DELETED, not converted (`debug()` prints under `-V`: Grok :48 read
   `debugmsg.c:365-376` and `main.c:473-478`).  All seven on widening; Grok prefers one helper (:41-48), GLM (:20), Astra (:60)
   and Argon (:66) two local arms.  See D2.
A4 ORDERING: the LBA arm precedes `write_offset` (M7); V20 in the contract.  ACCEPTED.
A5 OPTION SET: member 7 IMPLEMENT (Astra :70, Grok :50, GLM :22, Argon :86, DeepSeek Q12 :49).  `WDCE_ABRT` at `:947-954`/`:1155`
   is the available decline idiom; honouring the command is chosen because the measured defect is the wrong sector.  ACCEPTED.
A6 WORD 49: UNCHANGED at 0.  The "five rigs" rationale is RETRACTED (only landisk reaches `dev_wdc.c`, with an optional all-zero
   image: drafter NOTES #2; Grok :115; GLM Q34 :9; Astra :189).  Re-warranted under the addition licence: no measured delta or
   transferred warrant licenses the advertisement.  Follow-up FILED with its gate = a word-49-honouring guest on a content-bearing
   image with a checked sector (Grok :117; GLM Q34 :10; Astra :191 adds truthful capacity words and DMA bit clear).  "Linux
   guests" dropped from the records (GLM Q34 :14; Astra :40 "attributed, unverified").  ACCEPTED.
A7 COMMENTS re-authored in `dev_wdc.c`: the word-49 lines `:374-377` (policy + the interim ATA-2 tension, GLM Q12 :15), the arm
   label `:2006`, the SDH debug lines `:2010-2012`/`:2018-2020` (all seats).  ACCEPTED.
A8 MUST-NOT-CHANGE additions: word 49 and the IDENTIFY layout; the 48-bit opcodes' `default:` ABRT; the drain mechanics; the `#481`
   reset arm does not clear the taskfile (Grok :52); sector-count 0 = 256.  ACCEPTED into the pass-2 checklist.
A9 CHANGELOG #405's sentence (M9) becomes false; this round's block says so.  ACCEPTED.

B1 APPARATUS (L1): `row_ok` fails on a None got OR want; `OSError` guarded with the result lines and sentinel still emitted;
   `neg appar` -- see D3.  Dead run MEASURED afterwards.  ACCEPTED.
B2 VALID CHS TRIPLES at every CHS readback (index 70 = (0xa1, s8), 69 = (0xa1, s7), 256 = (0xa4, s5), 1007 = (0xaf, s63), 9 =
   (0xa0, s10), 67 = (0xa1, s5), 5 = (0xa0, s6)); Grok :77, GLM :34, Argon :221.  ACCEPTED.
B3 `lba 0` HEAD want = literal zeros (measured; derived from `diskimage.c:1595-1599`; Grok :78 "nehead also passes an empty-ring
   read").  ACCEPTED.
B4 ROWS ADDED: N1 `lba h1` (0xe1, s5: HEAD tag 67; FIX zeros, capture registers poisoned, tagged companion in-session -- Argon
   :245); N2 `lba wr h1` (0xe1, s5 write, read back index 67 via (0xa1,s5) AND index 5 via (0xa0,s6) -- Argon :206-214 found the
   brief's single readback could not see the head-conditioned variant); N3 `sel 40`; N4 `sdh rb3` 0x4c; N5 `lba wr256`; N6 `chs wr`;
   N7 the valid triples; N8 `chs c1` (cyl_lo 1, sector 1 -> index 1008).  PLUS two from Astra: `lba cylhi` (0xe0, s70, cyl_hi 1:
   HEAD zeros, FIX zeros, a `cyl_lo << 8`-only variant serves tag 70 -- Astra :126 "V10's IMAGE classification is false") and
   `sdh rb0` (write 0x00 after 0xe5, read back 0x00 -- Astra :109 zero-valued SDH writes).  N9 (enlarged image, wider tag) FILED.
   ACCEPTED.
B5 FLOOR GRADING: FLOOR C1-C3, C7-C9, C12-C17; C5/C10 rowed by N1/N2 and graded (d) by Grok (:63), GLM (:30), Argon (:136) and
   (e)-made-contractual by Astra (:93) -- recorded as such in the contract; C4 kept as a row (Astra :92: not a distinct cell);
   C6/C11 disclosed (both readings out of range on 4096 sectors); C18 a policy pin; C19/C20 clause (e).  ACCEPTED.
B6 VARIANTS: V12 equivalent (M8); V19 disclosed; V20 in CATCHES; the untabulated swap forms and `>> 4` / `& 3` tabulated (GLM :32);
   V1/V2/V13r also red the write-session readbacks (Argon :160-163); V15 -- see D4.  ACCEPTED.
B7 ANCHOR: a -1 shift reds five `lba` rows, a +1 shift four (`lba wr2` reads index 69); write anchor = `lba wr` + N5 (GLM :37,
   Astra :183, Grok :109).  ACCEPTED (the brief's R8 claim corrected).
B8 The brief's 7.1 row "past the file's end -- changed? yes" is false as a CONTENT claim (all seats).  Contract discloses the
   both-out-of-range subdomain.  ACCEPTED.
B9 NULL MEDIUM: executable non-emulator; record form -- see D5.

C1 GATE HOME: single-leg `GATE` mode in gate 10 (`gate_sh_rounding.sh`) beside `wdc_altdigin_probe.py`; lines `WDC_LBA_RESULT=p/n`,
   `WDC_LBA_CONTROL=OK`, sentinel; gate pins the denominator by EQUALITY to a literal, numerator == denominator, control == OK,
   result line present (Grok :121, Astra :199-203).  `tools/pipeline/check_probe_wiring.py`: CLASS_DETECTOR for the shipping
   probe; the frozen witness copy -- see D6.  ACCEPTED.
C2 WITNESS TERM: `probe:regress/wdc_lba_probe.py -- rung 3, unmodified evbmips -e malta, regress/artifacts/wdclbaaddr/witness_20261024/`
   once the fixed leg is green with the same script (all).  `WITNESS.md` already carries the three P15 corrections (Astra :207-213
   confirms).  ACCEPTED.
C3 SAME-CHANGE RECORDS: `row_no_lba_claim()` (assertion + "ok" string + name kept; comment + FAIL text re-authored);
   `gate_offline.sh:1890` comment; the `&& !d->lba` sentences (`OUTSTANDING_BUGS.md:13001`, `CHANGELOG.md:17817`) given explicit
   before/after semantics, no historical score re-interpreted (Astra :230, Grok :139); only this round's hunks staged in the two
   files that carry uncommitted hunks.  ACCEPTED.
C4 FILINGS: the word-49 advertisement follow-up (A6); media-access failure returns discarded at the read site and the drain,
   completion without status -- see D7; word 53: the brief's candidate is REFUTED (bit 0 clear = words 54-58 MAY be valid: Grok
   :149, Astra :252) -- Astra's words-54-56-zero coherence note recorded, not filed; LBA48: a CHANGELOG sentence.
C5 RECORD CORRECTIONS (L4): `ADJ_RULINGS.md`'s "measured" (all); the probe docstring keeps the true 0xe0 sentence and ADDS the
   bit-5 fact (Grok :155, Astra :260, GLM Q34 :30); the "no ATA document" comments reworded when touched (not this round: Grok :147).
C6 `wdccylwrap`: no severity change this round (all).

## 4. DISAGREEMENTS (each side in its own words; the main loop's ruling marked, open for you to overturn)

D1 -- READBACK FIELD.  (ii) keep bits 7 and 5 in the existing `sectorsize` field as `idata & 0xa0`, recompose `sectorsize | lba<<6
   | drive<<4 | head`: DeepSeek Q12 :26-31, Argon :40-53 ("zero struct changes"), Grok :29-39 ("`sectorsize` keeps a reader under
   (ii). Do not delete the field this round").  (i) raw byte: GLM :18 ("(ii) is byte-exact but makes the field name a lie").
   Astra :43-48: either, but "Rename the storage so its name and debug output describe preserved bits".
   MAIN-LOOP RULING: (ii) WITH THE FIELD RENAMED `sectorsize` -> `sdh_resv` (one struct line; its only readers are the arm and the
   two debug lines, which this round re-authors anyway).  No field added, none deleted.
D2 -- HELPER vs TWO ARMS.  Grok :41-48: one static helper (removes V20 as a statement-order hazard).  GLM :20 / Astra :60 / Argon
   :66: two local arms (smallest diff; mirrors the patch; keeps V14's halves constructible).  RULING: two local arms.
D3 -- `neg appar`.  Grok :91 and Astra :163: drop it from the score (or make it a genuine parser test); DeepSeek :96 / GLM :36:
   replace with a real comparator self-test.  RULING: DROP it from the scored rows; keep a comparator self-check as a non-scored
   startup assertion.  The denominator is recomputed from the revised probe and pinned by equality.
D4 -- V15 (the unwidened 32-bit product).  Argon :59-63: N1/N2 observe it (the wrap serves sector 5).  Grok :73 and Astra :131/:138:
   undefined behaviour; a compiler may widen; "N1 is not an oracle for it"; widen regardless; do not label it detected or
   invisible.  RULING: widen; BUILD V15 in the kill table and RECORD its measured score on this build in the contract as a
   measurement that does not generalise ("undefined in general").
D5 -- CLAUSE (c) RECORD FORM.  Grok :91: `(c): by construction via gate 10's result-line check and CONTROL=OK equality, leg not
   run`.  Astra :167-171: by-construction only after the wiring exists and is inspected, else the measured form.  RULING:
   MEASURE the dead run (an executable non-emulator) and record `(c): measured at <artifact>`; the gate's pins are additionally
   described.
D6 -- THE FROZEN WITNESS COPY'S CLASS.  Grok :123 and drafter NOTES #33: CLASS_WITNESS (the #533 pair).  Astra :205: CLASS_RESEARCH
   ("preserved nonshipping evidence; must not acquire a duplicate gating obligation").  RULING: read the checker's class
   definitions at landing; the main loop leans CLASS_WITNESS because the file IS the as-run witness instrument.
D7 -- OUT-OF-RANGE MEDIA COMPLETION.  Grok :143/:151: inherited `#416` contract, say so in the CHANGELOG, no new row.  Astra :256,
   GLM Q34 :28, DeepSeek Q34 :43: file separately (a completion-status defect: failure returns discarded at `:531-533` and the
   drain `:1868-1870`; distinguish legitimate zero-fill padding from refused accesses).  RULING: FILE one row (LOW-MED), CHS and
   LBA alike, pre-existing; not fixed in-round.

## 5. QUESTIONS

Q1 WHICH OF THE 22 ACCEPTED DISPOSITIONS ABOVE (A1-A9, B1-B8, C1-C3, C5-C6) IS WRONG?  Name the id and the fact that refutes it.
Q2 Rule D1-D7.  Where you overturn the main loop, say what changes in the fix, the detector or the records.
Q3 Anything the seven seats and the main loop all missed about the fix's partition, the detector's floor, or the records?

Verdict vocabulary: ADJUDICATION: CONFIRM | CONFIRM WITH CHANGES | REJECT.
