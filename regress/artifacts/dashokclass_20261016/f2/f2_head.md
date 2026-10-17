# ADJUDICATION PASS (§F2) -- `dashokclass`: the four seats' pass-2 findings, my dispositions, and the repair (v2)

Four seats, by the owner's roster of 2026-10-16: Fable 5.1, GPT-6 Astra, Grok 4.7, GLM 5.3.  Opus, agy, kimi, deepseek and
minimax are DELIBERATELY NOT FIRED under that roster.  An ordinary review of a records tool (the dashboard generator) and a
pre-commit check over its JSON ledger.  READ-ONLY: write nothing to any project tree.  The tree is
`C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC`; the v2 files are STAGED under `regress/artifacts/dashokclass_20261016/staged_v2/`
(mirroring `tools/`), with `run_controls_v2.py`, `run_mutants.py`, `write_baseline.py`, `RECEIPT_v2_staged.txt` and
`KILLTABLE_staged.txt` beside them; the pass-2 answers are in `pass2/`.  Everything a packet-fed seat needs is inlined.

**This pass SHARES every seat's findings with every seat.**  Rule on your OWN findings harder than on anyone else's --
including whether the FIX I made is right, not only whether the finding was.  **The load-bearing question is section 6's:
which of my accepted dispositions is wrong?**

<TOKEN_LINE>

## 1. The pass-2 verdicts

* **GPT-6 Astra -- SHIP WITH CHANGES (3)** (`pass2/codex_dashok.txt`).
* **GLM 5.3 -- SHIP WITH CHANGES (4)** (`pass2/glm_dashok.txt`).
* **Fable 5.1 -- SHIP WITH CHANGES (7)** (`pass2/fable5_dashok.md`; `agent_models.py`: clean claude-fable-5-1).
* **Grok 4.7 -- SHIP WITH CHANGES (3)** (`pass2/grok_dashok.txt`).

## 2. Every finding, numbered, with my disposition

| # | seats | finding | disposition |
|---|---|---|---|
| D1 | Astra, Fable, Grok | the tooltip's "(not approval, not a seat failure)" is contradicted by legacy answers whose notes record real seat failures (`WALL` x3 per Astra/Grok; 73 answers / 20 displayed cells naming a non-answer, per Fable); the legend's "older entry" is not what the code tests | **FIXED**: tooltip "legacy -- verdict unclassified: d = 'X' is outside ✓ ✕ ⏸ …; read the note for the outcome"; legend "legacy -- verdict text outside ✓ ✕ ⏸ …, unclassified (read the note; ? = an explicit blank)"; pinned by R1 (tooltip prefix) and R4 (legend) |
| D2 | all four | a per-(row, phase, seat, date, d) COUNT lets a converted entry's slot be REFILLED by a new answer (measured rc 0 by Astra and Fable) | **FIXED**: the key is now the entry's IDENTITY -- row, phase, seat, date, d and the sha1 of its NOTE; C15 pins the refill (rc 1) |
| D3 | Astra, Fable, Grok | a legitimate correction (a frozen entry's date) fails Q2 | **ACCEPTED as designed**: editing a frozen off-domain answer means giving it a glyph -- the ruling's own way out ("an OK becomes ✓ only when a reader rewrites that one entry").  **Under v2 this now includes a NOTE-only edit** (C16) -- see section 3 |
| D4 | Astra, Grok | a note edit can change `is_answer` (defanging the `ns16550` blank-d HELD record makes it an answer) | **COVERED by D2/D3**: it becomes an off-domain answer that is not frozen, so it fails and is normalised |
| D5 | all four | the baseline writer's placement is not a guard; the checker trusts the file | **FIXED**: the checker pins the baseline's md5 (`BASELINE_MD5 = 06a3ffc6...`) on its default path -- a re-freeze is a reviewed change to that constant in the same commit; the writer refuses to overwrite; C18 pins (one changed line -> rc 2) |
| D6 | Grok | an exported `GXDOMAIN_BASELINE` is honoured inside the hook | **FIXED**: section Q2 runs `env -u GXDOMAIN_BASELINE -u GXLEDGER python check_entry_domain.py`; W4 pins (an override that would admit a new entry is ignored) |
| D7 | Grok | the loader's dict keeps the LAST count for a repeated key | **FIXED**: counts are summed and each row's shape is validated (C17: string counts -> rc 2) |
| D8 | Astra, Fable, Grok | `CUTOFF` -> 2026-10-18 passes all 19 controls: the inclusive boundary was unpinned (C3 red for the baseline reason) | **FIXED**: C12 isolates the date test with FROZEN identities dated before / on / after the cutoff (0 / 1 / 1); the kill table kills `d_cutoff18` there |
| D9 | all four | dates compare lexically; a non-string date raised `TypeError` (rc 1 with a traceback) | **FIXED**: the cutoff applies only to an ISO `YYYY-MM-DD` prefix; non-string dates are compared by `repr`; a malformed date on a non-frozen entry is named in the reason; C19a/C19b pin (rc 1, no traceback) |
| D10 | Astra, Fable, Grok | `"d" not in x` -> `not x.get("d")` lets a new explicit blank pass | **PINNED**: C14 |
| D11 | Astra, Grok, Fable | control gaps: C1 asserted only rc; no strictly-after positive; C11 named "at least one"; R1 skipped the record glyph and the tooltip; R2 did not check the total; R3 counted a crash as a kill; W1/W2 never ran the real failure counter | **ALL FIXED** (C1 "1356 frozen", C2b, C11 all 1,356 named, R1 record glyph + tooltip, R2 total = entry count and legacy = the ledger's off-domain count, R3 requires a successful render, W1-W4 count failures) |
| D12 | Fable | under the precommit's cp1252 stdout the checker's failure lines raise `UnicodeEncodeError` | **FIXED**: `sys.stdout.reconfigure(errors="backslashreplace")`; the controls run the checker WITHOUT `PYTHONIOENCODING`; C20 pins (a non-ASCII `d`, rc 1, no traceback) |
| D13 | GLM | rc 2 through the gate untested; no escapable-`d` fixture; no refill control; no `?` legend line | **FIXED**: W3, R1b, C15, the legend line |
| D14 | Fable | "Astra's wording" is Astra's phrase minus "OK" | **CORRECTED** in the records |
| D15 | Astra, Fable | the packet's 5,167 entries and R2 census were one commit stale | **CORRECTED**: HEAD 8bf8b5a1 has 5,177 entries; v2's receipt is of that ledger |
| D16 | Grok, Fable | the landing must regenerate `matrix.html` with the new renderer (section Q) | **IN THE COMMIT PLAN** |
| D17 | all four | "Q2 can only fail on an entry added after it lands", "cannot retro-fail", "this class can only shrink" are false | **CORRECTED**: the docstring and the Q2 comment say it fails on a new entry AND on an old one edited; the GRANDFATHERED population only shrinks, and the dashboard's legacy count is a different number |
| D18 | GLM | does the tooltip insert reach hold/record cells? | **SETTLED by reading** `cell()`: the hold and record branches return before `tip` is built |
| D19 | Fable | five answers carry `✗` (U+2717), a lookalike of the objection glyph | **NOTED** for a reader's one-at-a-time rewrite; no sweep (ruled) |
| D20 | Fable, Grok | on a refused stage exemption, that line opens the tooltip before the legacy line | **KEPT**: the refusal is the louder fact |

## 3. Disagreements, both sides in their own words

* **The note IN the key.**  All four seats on pass 2: *"Leaving the note out is right for ordinary note corrections"*
  (Astra); *"note-in-key would re-arm every correction/defang ... the refill hole is the price and the smaller evil"* (GLM);
  *"Note out of the key: right"* (Fable); *"Leaving the note out is right for a wording fix"* (Grok).  **I put it in**, to
  close the refill (D2): under a count key the two edits -- "convert X and add Y with X's tuple" and "correct X's note"
  -- are indistinguishable, so one of them must pass or both must fail.  I chose both-fail; the price is that a note-only
  correction of a frozen off-domain answer now needs a glyph (C16).  **Rule on this.**
* **The baseline guard.**  Fable: a `cmp` of the working baseline against `HEAD:` inside Q2 (`bad` on any difference).
  GLM: pin the total (1,356).  Astra: "baseline changes still need a protected, reviewed provenance rule".  **I chose an
  md5 pin in the checker**: it detects every unreviewed change, as the `cmp` would, and still lets a REVIEWED re-freeze
  land in one commit (the constant changes with the file); a `cmp` against HEAD would refuse every re-freeze for ever.
