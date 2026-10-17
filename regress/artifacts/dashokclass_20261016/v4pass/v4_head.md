# V4 PASS -- `dashokclass`: the dashboard's legacy class and the entry-domain check, v4 = the CLASS CLOSURE

Four seats, by the owner's roster of 2026-10-16: Fable 5.1, GPT-6 Astra, Grok 4.7, GLM 5.3.  Opus, agy, kimi, deepseek and
minimax are DELIBERATELY NOT FIRED under that roster.  An ordinary review of a records tool (the dashboard generator), a
pre-commit check over its JSON ledger, and the controls that pin both.  READ-ONLY: write nothing to any project tree.  The
tree is `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC`; the v4 files are STAGED under
`regress/artifacts/dashokclass_20261016/staged_v4/` (mirroring `tools/`); the controls are `run_controls_v4.py` and
`run_mutants_v4.py` beside it, run with CTL_CHECKER / CTL_RENDER / CTL_PRECOMMIT naming the staged files; the v3-pass
answers are in `v3pass/`.  Everything a packet-fed seat needs is inlined below.

**Why v4 is a class closure.**  Pass 2, the adjudication pass and the v3 pass each found one-edit mutants that passed every
control of the version before -- the same class: a behaviour of the checker, the renderer change or the Q2 block that no
row pinned.  By the repair-chain rule the next repair owes the class: v4 enumerates every decision those three make, pins
each at its edges, and writes the rest into a CONTRACT in `run_controls_v4.py`'s docstring (inlined in section 4a).
**This pass's job is to VERIFY THE ENUMERATION** -- is any decision missing from the CONTRACT, or listed as pinned while a
one-edit mutant of it still passes all 72 controls?  The chain closes on the first pass whose zero floor breaches survive
adjudication; if you find none, name the decisions you checked.  Check the premises in 2b; do not ratify them.

<TOKEN_LINE>

## 1. The v3-pass verdicts -- all four SHIP WITH CHANGES (3)

GPT-6 Astra (`v3pass/codex_dashokv3.txt`), GLM 5.3 (`v3pass/glm_dashokv3.txt`), Fable 5.1 (`v3pass/fable5_dashokv3.md`;
agent_models.py: clean claude-fable-5-1, measuring in a mirror), Grok 4.7 (`v3pass/grok_dashokv3.txt`).

## 2. Every finding, numbered, with my disposition

| # | seats | finding | disposition |
|---|---|---|---|
| J1 | Astra | five one-edit survivors of the 46: the date's `v` -> `v[:10]`; the answer cell's `record:` line deleted (32 displayed cells lose it); `if cls == LEGACY` -> `if d == "OK"` (305 cells lose the class line); the strip folding the canonical glyphs into ✓; Q2's missing-checker `bad` -> `good` | **PINNED**: C25a/b (a frozen entry's date suffixed / given a trailing space), R1e (an answer with a record beside it keeps the record's note), R1g (every simple legacy cell's WHOLE tooltip), R2 (each strip number is the ledger's own count), W6 (the checker absent: BAD "MISSING") -- mutants `d_date10`, `r_norecord`, `r_okonly`, `r_stripok`, `w_nochecker` |
| J2 | Astra | `{"rows": {}}` and a string entry walk as EMPTY and pass (rc 0): the rc-2 promise is false in general | **FIXED in the checker**: `ledger_shape()` type-checks every container level (ledger object, rows list, row objects, entries lists, entry objects) before anything is walked, and the baseline must be a list; C21d-g.  The walk's except-arm stays for the one input that still reaches it -- a non-string note raises inside `stage_tokens.is_answer` (C21h) |
| J3 | Astra | C2c/C2d were red without their own entries (the shipped ledger carries 21 ⏸ and 35 … answers) | **FIXED**: each runs on a ledger holding ONLY its entry |
| J4 | Astra | records: "on the landed files"; "every explicit d renders as one class" (holds and records keep their rendering); "a new answer fails" (an admitted replacement can be new) | **CORRECTED** (sections 5a-5d) |
| J5 | GLM | the checker-absent and ledger-unreadable edges are unpinned | **PINNED**: W6, C23 (a ledger that is not JSON: rc 2) -- `w_nochecker`, `d_unread0` |
| J6 | GLM | the summary line is pinned only on a clean ledger, where "passes" and "entries" agree | **PINNED**: C11 asserts the dirty summary ("0 within the frozen ceiling (baseline 0)") -- `d_summary` |
| J7 | GLM | RULINGS_C's "5,150 at HEAD" and Q2's header "or is a frozen legacy entry" are stale | **CORRECTED** (5c; Q2's header now "or is within the frozen legacy ceiling") |
| J8 | Fable | `if cls == LEGACY and d == "OK"` and `... and str(d).strip()` pass all 46: R1 compared ONE cell's tooltip | **PINNED**: R1g compares the WHOLE tooltip of every simple legacy cell -- `OK`, blank, `N/A`, `<b>&`, a space, a tab, a padded ` ✓` -- `r_tipokonly`, `r_tipnonblank` |
| J9 | Fable | an explicit `"d": null`; a padded glyph `" ✓"`; condition 2's NOTSEAT half pinned only incidentally; the hint line asserted by nothing | **PINNED**: C26 (a new answer with d null: rc 1), R1h (the padded glyph renders legacy), C24 (a NOTSEAT record after the cutoff: rc 0), C11 asserts the hint -- `d_nulld`, `r_clsstrip`, `d_isheld`, `d_nohint` |
| J10 | Fable | records: the checker docstring quotes a clause RULINGS_C upheld but did not restate; grok's adjudication entry credited it with the CRLF measurement; dashmissingd's question omits section H | **CORRECTED** (the docstring cites packet_C_records.md F2 (d) as upheld by RULINGS_C F2; the entry says the main loop measured it; the filing names the H collision with Fable's measured counts) |
| J11 | Grok | the glyph SET is open at the top: a fifth member of DOMAIN, or a fifth key of D_CLASS, passes all 46 | **PINNED**: C27 reads both files' literals and requires exactly ✓ ✕ ⏸ … -- `d_domzxq`, `r_dclasszxq` |
| J12 | Grok | the cutoff was pinned on two days (`in ("2026-10-17", "2026-10-18")` passes) | **PINNED**: C12 adds a FAR-after frozen identity (2027-01-01) -- `d_cut2days` |
| J13 | Grok | the summary's baseline number and Q2's named-entry lines are never read | **PINNED**: C1 asserts "(baseline 1356)"; W2 asserts the OFF-DOMAIN ANSWER lines reach the committer -- `d_baselen`, `w_nosed` |
| J14 | Grok | a tab-only `d` would render invisible under `.strip(" ")` | **PINNED**: R1d adds a tab -- `r_wsspace` |
| J15 | main loop | the first v4 table: `d_dfold`, `d_notestrip`, `d_notefold` were killed by C1, not by C25d-f | **RE-NAMED**: they are ONE-SIDED here -- the baseline holds raw values and only the note's sha -- so the whole frozen population misses and C1 kills them; the COHERENT fold of d is the two-edit design mutant `d_dfold2`, killed by exactly C25d; no coherent note fold or strip can exist |
| J16 | main loop | the seat entries | answered seats carry `d` ✓ (their changes applied, entry by entry); seat failures and seats not fired carry none |

### The one DISAGREEMENT, both sides

* **GPT-6 Astra (v3 pass):** *"all five proposed NOT FIRED entries classify as answers under `stage_tokens.is_answer`.  Their
  prose and missing `d` do not make them non-answer records.  Adding the entry-scoped `NOTSEAT` token makes all five classify
  correctly."*
* **Mine, on Fable 5.1's measurement:** they stay plain entries.  `check_stage_panels.py` (precommit section H) tallies a
  stage's seats by `is_answer` -- an untokened entry counts as a recorded seat, a NOTSEAT one is skipped -- and the owner's
  standing directive records a seat not fired as DELIBERATELY NOT FIRED so the stage still shows nine recorded seats.
  Tokening them NOTSEAT turns H red at 4/9 on this landing.  Fable measured 158 such entries at HEAD (127 untokened); the
  collision is now part of `dashmissingd`'s rule question rather than settled here.  **Rule on it.**

## 2b. Premises to CHECK (stated as questions)

* **The CONTRACT's completeness** (section 4a).  Read the staged checker, the renderer's changed lines and the Q2 block for
  every `if`, comparison, literal, container walk, exit and printed line a caller reads.  Is any decision missing, or listed
  as pinned by a row that cannot see its mutant?
* **The NOTSEAT disagreement** above.
* **J2's shape check.**  Is there a misshapen ledger or baseline the v4 checker still walks as empty and passes?
