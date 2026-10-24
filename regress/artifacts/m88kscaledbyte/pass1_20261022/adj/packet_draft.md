# ADJUDICATION of T1 (`m88kscaledbyte`, round `#569`) PASS 1 -- for GPT-6 Astra (adjudicator; owner roster 2026-10-23)

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

You are the ADJUDICATOR of this round's pass-1 design review, not a reviewer of the design: four review seats
(GLM 5.3, DeepSeek, Grok 4.7, Gemini 4 Argon) and you (as a reviewer, before this packet) have answered the pass-1
brief; the main loop consolidated their findings into dispositions.  **Your job is to find which of the main loop's
accepted dispositions is WRONG**, which seat finding was mis-filed, and which disagreement the main loop settled by
preference where it should have been settled by a reading or a measurement.  Everything you need is in this
directory (`regress/artifacts/m88kscaledbyte/pass1_20261022/`): the brief (`packet.md`), the seat answers (named
below), the main loop's rulings (`PASS1_RULINGS.md`) and its checks (`CHECKS_mainloop.md`).  You may open every file
named here and the repository source under `GXEMUL-SEC/src/` at HEAD; do not build or run anything.  The tree under
review is `GXEMUL-SEC/src/`; ignore any other `src/` under the project root (pristine 2021 upstream).

VERDICT LINE FIRST: `VERDICT: <UPHOLD | AMEND | OVERTURN> -- <one sentence>`, then one line per numbered item below
(`A1 UPHOLD` / `B7 AMEND: ...`), then your reasoning.  Cite answer files as `<file>:<line>`.

## 1. The seats and where their answers are

| seat | transport | answer | verdict line |
|---|---|---|---|
| GPT-6 Astra (ultra) -- you, as reviewer | codex CLI, file-reading | `codex_t1p1.txt` (19,643 b) | READY WITH CHANGES |
| Grok 4.7 (xhigh, plan mode) | grok CLI, file-reading | `grok_t1p1.txt` (21,832 b) | READY WITH CHANGES |
| GLM 5.3 | Ollama cloud, PACKET-FED, two firings (Q1-Q2 / Q3-Q4) | `ollama_glm_t1p1_Q12.txt` (17,369 b), `ollama_glm_t1p1_Q34.txt` (9,008 b) | READY WITH CHANGES (both) |
| DeepSeek v4-pro | Ollama cloud, PACKET-FED, two firings | `ollama_deepseek_t1p1_Q12.txt` (10,187 b), `ollama_deepseek_t1p1_Q34.txt` (4,171 b) | NOT READY (Q1-Q2: "row set under-specified"); READY WITH CHANGES (Q3-Q4) |
| Gemini 4 Argon | gemini_webapi, PACKET-FED, two packets (Q1 / Q2-Q4) | `argon_t1p1_A.out`, `argon_t1p1_B.out` | (appended in section 5 when banked) |
| Fable 5.1 | Agent tool | `fable5.HELD.txt` | DELIBERATELY NOT FIRED (owner hold 10-21/10-22); hold question carried |

Not fired by the owner's roster: agy, kimi, minimax, Opus-as-seat.  The packet-fed seats saw the COMPACT brief
(`packet_compact.md`, split by question); the file-reading seats the FULL brief (`packet.md`).

## 2. The main loop's dispositions under test -- `PASS1_RULINGS.md` sections A (A1-A6), B (B1-B12), C (C1-C4)

Read them there; they are not restated here.  The claims most worth attacking, with the seat positions by line:

* **B7 -- v1-v4 classification.** Astra files them "partial (b)" (`codex_t1p1.txt:110-123`); Grok (`grok_t1p1.txt:75-78`),
  GLM (`ollama_glm_t1p1_Q12.txt:50`) and DeepSeek (`ollama_deepseek_t1p1_Q12.txt:51-55`) file them clause (d).  The
  main loop recorded both and built ONE representative (v2) plus the endianness narrowing.  Is "no row consequence"
  true, and is one representative enough for the floor's clause (d), or does the floor owe a measured kill PER
  predicate axis (sync, signedness, usr, endianness -- four legs)?
* **B8 -- the floor's size.** Astra 24 as the output contract (`codex_t1p1.txt:138-144`); Grok 16 floor + 8 clause (e)
  (`grok_t1p1.txt:84-89`); GLM 24 floor (`ollama_glm_t1p1_Q12.txt:52`); DeepSeek 16 (`ollama_deepseek_t1p1_Q12.txt:61-67`).
  The main loop pins all 24 and writes Grok's split into the contract.  Right, or does the carrier's R7 make the
  24-vs-16 question decidable one way?
* **B6 -- clause (c) medium.** Adopted: comment-only generator (compile row) + comment-only table (reader rows), both
  legs RUN.  DeepSeek proposes instead an ALL-NULL table and a generator emitting one, recorded by construction
  (`ollama_deepseek_t1p1_Q34.txt:20-21`); the builder was asked to run the all-NULL table as an extra leg (L8).
  Is comment-only the right medium under the carrier's clause-(c)-by-instrument rule, and is "measured at
  <artifact>" the right record form?
* **B3 -- the halfword accept pin via rule D2.** GLM derives it from D2's B+1 edge of `:80`'s `size > 0`
  (`ollama_glm_t1p1_Q12.txt:54`); Astra says D2 cannot pull a callee compare across the DEPENDS-ON boundary and the
  row is owed by R12 instead (`codex_t1p1.txt:146-148`); DeepSeek says D2 does not apply because `size == 0` is an
  equality, R12 supplies it (`ollama_deepseek_t1p1_Q12.txt:70`).  Same row, three warrants: which warrant is the
  record's, and does it matter for a future escape's grading?
* **B4 -- the NULL-count row.** Grok: "the wrong pin" (`grok_t1p1.txt:124`); GLM/Astra/DeepSeek: supplementary by
  equality.  The main loop kept it supplementary.
* **A5 -- the committed table as a second fixed site**, and what the diff owes for `est/` (Grok `grok_t1p1.txt:47`:
  the diff owes the est copies; DeepSeek `ollama_deepseek_t1p1_Q12.txt:22`: not a commit obligation).  The main loop:
  precommit section A makes est byte-identity a commit-time obligation (CHECKS #4).
* **C1 / C2 -- the two findings filed as NEW ROWS** (Astra's `xmem` address-operand overlap, `codex_t1p1.txt:200-202`,
  confirmed in CHECKS #7; Grok's PSR byte-order bit, `grok_t1p1.txt:132`, lines verified).  Right severity, right
  disposition (filed, outside T1's contract)?
* **DeepSeek's NOT READY** (`ollama_deepseek_t1p1_Q12.txt:1`): every point it names is already an amendment in
  PASS1_RULINGS (A6, B2, B3, B8).  Is anything in its answer NOT covered by a ruling?

## 3. The main loop's own checks (`CHECKS_mainloop.md`, 11 items) -- which is wrong?

Each names the command or lines read.  #1 (`p` from `host_load[addr >> 12]`), #2 (`ls_entry` hard-codes `[32]`),
#3 (four table sites), #4 (est/ propagation vs git), #5 (296 NULLs at HEAD), #6 (agreement at HEAD owed to the
builder), #7 (Astra's C1 in source), #8 (`diff_autodev_gen.sh` + the `#406` block tracked), #9 (`need_file` skips),
#10 (the make rule is dependency-driven), #11 (`gate_offline.sh`'s foreign hunks; GATE 2 is the home).

## 4. The questions

Q1. VERDICT on PASS1_RULINGS as a whole, then per item A1-A6, B1-B12, C1-C4: UPHOLD / AMEND (say how) / OVERTURN.
Q2. Which of the 11 checks is wrong or incomplete, by number?
Q3. The build is already running on `BUILD_SPEC.md` (same directory).  Name anything in it that a ruling you amend
    would change -- by section number -- so the builder can be told before it lands; if nothing, say so.
Q4. Anything else, with the file:line that settles it.

## 5. Gemini 4 Argon's answers (appended when banked)
