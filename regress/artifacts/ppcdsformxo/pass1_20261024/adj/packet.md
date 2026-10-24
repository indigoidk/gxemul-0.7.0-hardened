# ADJUDICATION of T2 (`ppcdsformxo`, round `#571`) PASS 1 -- for GPT-6 Astra (adjudicator; owner roster 2026-10-23/24)

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

You adjudicate the pass-1 design review of one regression-testing round in the GXemul hardened fork (a correctness fix
to the emulator's PowerPC instruction decoder -- the 64-bit DS-form load/store forms selected by the instruction word's
two XO bits, which the decoder folds into the displacement -- and the regression rows it owes).  The main loop has read
all seven seat answers and written its dispositions in `..\PASS1_RULINGS.md` (the parent directory of this packet).
**Your job is to find which of those dispositions is WRONG**, settle the eight disputes by argument and by the source
(you may open every file named here and the tree at HEAD `add098b9`; `tools/pipeline/check_probe_wiring.py` carries
uncommitted peer edits -- read it via `git show HEAD:<path>`), and be HARDER on the positions that adopted YOUR OWN
pass-1 claims than on the others: a ruling in your favour is the one you are least likely to test.  Do not build or run
anything; do not propose reproduction recipes or program listings; dispositions by id.

All paths are under `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\ppcdsformxo\pass1_20261024\` unless
absolute.  The brief the seats answered is `packet.md` (FULL: Astra, Grok) / `packet_compact.md` (Argon) /
`packet_packetfed.md` (GLM and DeepSeek, split Q1-2 / Q3-4).  The witness is `..\witness_20261024\`
(`WITNESS_REPORT.md`, `ppc_dsform_probe.py`, `WITNESS_headbin.out`, `receipts\`).

## 1. The seats and where their answers are

| seat | file | verdict | class |
|---|---|---|---|
| GPT-6 Astra (you, as reviewer) | `codex_t2p1.txt` | READY WITH CHANGES | file-reading |
| Grok 4.7 (xhigh, plan mode, cwd GXEMUL-SEC) | `grok_t2p1.txt` | READY WITH CHANGES | file-reading (WORKING tree) |
| Gemini 4 Argon (through agy, --add-dir) | `argon_agy_t2p1.txt` | READY WITH CHANGES | file-reading (see `argon_transport_20261024.txt`) |
| GLM 5.3 | `ollama_glm_t2p1_Q12.txt`, `ollama_glm_t2p1_Q34.txt` | READY WITH CHANGES | packet-fed |
| DeepSeek v4-pro | `ollama_deepseek_t2p1_Q12.txt`, `ollama_deepseek_t2p1_Q34.txt` | NOT READY (x2) | packet-fed |
| Fable 5.1 | `fable5.HELD.txt` | HELD by the owner, with its question | -- |
| kimi, minimax, Opus-as-seat | `roster_NOT_FIRED.txt` | DELIBERATELY NOT FIRED by roster | -- |

The main loop's own measured checks are section "MAIN-LOOP CHECKS" (M1-M5) of `..\PASS1_RULINGS.md`; the drafter's
notes are `drafter_NOTES.md`.

## 2. The dispositions under test -- `PASS1_RULINGS.md` sections A (A1-A9), B (B1-B13), C (C1-C9): THIRTY-ONE

Read them there; this section names only what each rests on, so you can aim.

* A1, A2, A4, A5, A7, A8, A9, B1, B2, B3, B9, B11, B12, B13: unanimous or near-unanimous across the seats; the main
  loop ACCEPTED all of them.  **Which accepted disposition is wrong?**  Thirty-one were written; a round that accepts
  everything has either had a very good panel or has stopped arguing.
* A3 rests on Argon's census of every `goto bad` site and on M1 (`cpu_dyntrans.c:2004-2014`): dispute D2.
* A6 rests on R17 and on the census YOU and Argon supplied: dispute D1 -- your pass-1 answer chose the other option.
* B4, B5, B6, B7, B8: disputes D4, D5, D3, D6, D7.  B6 ADOPTS your four-session RA = 0 claim -- test it harder.  B7
  REJECTS your "all 22 labels" reading -- test that too.
* B10 corrects the brief's gloss on the `lwa size 3` null (host exit, not neighbour consumption) -- your finding and
  Grok's and GLM's; is the "run it as its own leg, scored as host exit" disposition right, or is a host-exit leg a
  category error in a kill table?
* C1-C4 filings rest on M3 (unfiled: the `ldx` family and the FP-update disassembler cases); C5-C9 are record
  corrections, two of them (C5, C6) adopting your readings -- scrutinise them MORE.

## 3. The disputes -- in `..\PASS1_RULINGS.md` section D, each side quoted verbatim

D1 (32-bit width test: (i) disclose vs (ii) gate 58/62), D2 (a `fatal()` line before the reserved-XO `goto bad`),
D3 (RA = 0 update stops at both DS partitions, four sessions, vs one per form), D4 (DS = 0 value rows shipped vs (e)),
D5 (C9 positive-word `lwa` and C18 `stdu` RA = RS), D6 (C21/C22 scope: representatives vs all 22 labels), D7 (clause
(c) record form: measured vs by construction), D8 (the store anchor: debugger `dump` vs a reload by `ld`).

## 4. The questions -- VERDICT LINE FIRST (`VERDICT: UPHOLD | AMEND | REJECT -- <one line>`), then by id

Q1. Of the THIRTY-ONE dispositions (A1-A9, B1-B13, C1-C9), which are WRONG, and why (file:line)?  Name at least the
    ones you are least sure of even if you uphold them.
Q2. D1-D8: rule each, in your own words, against the source and the quoted rule text (the carrier's clause (d)
    DEPENDS-ON bound and its joint-cell clause -- "DEPENDS-ON enumerates JOINT cells over the guard's operands and the
    body-read lvalues EXACTLY WHEN THE GUARDED BODY'S OWN CODE DISTINGUISHES THEM"; the addition licence -- "measured
    deltas or a transferred warrant, never 'it cannot hurt'"; R17 -- a second site joins only if witnessed, same device
    and class, covered by the same detector with no new oracle; the option set's availability rule).  For D1 be harder
    on (ii) than on (i); for D3 be harder on four sessions than on two; for D6 be harder on "all 22" than on two.
Q3. The row budget: the loads session (`ld value`, `ld RA after`, `ldu value`, `ldu RA after`, `ldu ds0 value`,
    `lwa value`, `lwa RA after`, `lwa ds0 value`, `lwz value`, `lwz odd`, `live`), the stores session (`std value`,
    `std RA after`, `stdu value`, `stdu neigh`, `stdu RA after`, `stdu ds0 value`, `stdu alias val`, `stdu alias RA`,
    `stw odd`, `st live`), seven stop sessions (`xo58_3`, `xo62_2`, `xo62_3`, `ldu ra0`, `stdu ra0`, `ldu ra0z`,
    `stdu ra0z` -- each a `live` and a `bad` row), `unasm census`, `word pins`, `neg apparatus`: about 38 rows.  Is any
    row VACUOUS BY CONSTRUCTION (its channel cannot vary under its named mutant)?  Is any owed row MISSING from the
    floor as you enumerate it from the diff (the mask line and the two case lines, inside `X(to_be_translated)`)?  Does
    the gate pin (N by literal equality, the `#565`/`#570` shape) need anything else?  Are all names within the probe's
    15-character / unique-name asserts?
Q4. Your own pass-1 claims that the rulings ADOPTED: the mask-placement requirement (codex:33-43), the C26 reachability
    correction (codex:164), the P8 qualification (codex:74), the four RA = 0 sessions (codex:152, 210), the `lwa size 3`
    host-exit reading (codex:172), the twelve-form census (codex:64-70).  Scrutinise each MORE than the others; say
    which you would now weaken or withdraw.
Q5. The build order in `PASS1_RULINGS.md` section E: anything that must happen BEFORE something the order puts after it
    (the PRETABLE before table 1; the grown detector's BASE run before the C edit; the frozen witness's post-fix run; the
    rounding probe re-run; the identity-body leg's prediction derived from the frozen detector source before its run)?

## 5. Seats not in the evidence basis

Fable 5.1 is HELD by the owner (hold question in `fable5.HELD.txt`); kimi, minimax and the Opus seat were deliberately
not fired by roster.  Neither is agreement; say in your verdict line that the basis is FOUR reviewing seats (seven
answers).  Argon's answer was checked for cross-seat reading (none found; its file landed before any other file-reading
seat's answer had content) -- see `argon_transport_20261024.txt`.
