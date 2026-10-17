# ADJUDICATION PASS (§F2) -- the `tools/cxlaunch.sh` landing: the four seats' pass-2 findings, my dispositions, and the repair

Four seats, by the owner's roster of 2026-10-16: Fable 5.1, GPT-6 Astra, Grok 4.7, GLM 5.3.  Opus, agy, kimi, deepseek and
minimax are DELIBERATELY NOT FIRED under that roster.  An ordinary review of a test-harness script (a launcher that runs one
read-only review job through a CLI and classifies how it ended).  READ-ONLY: write nothing to any project tree.  The tree is
`C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC`; the REPAIRED launcher is now the working-tree `tools/cxlaunch.sh` (v2), and its
controls and kill table are in `regress/artifacts/cxlaunchland_20261016/` (`run_controls_v2.sh`, `RECEIPT_v2.txt`,
`mut_launcher.py`, `run_mutants.sh`, `KILLTABLE.txt`).  Everything a packet-fed seat needs is inlined.

**This pass SHARES every seat's findings with every seat.**  Rule on your OWN findings harder than on anyone else's --
including whether the FIX I made for it is right, not only whether the finding was.  **The load-bearing question is
section 5's: which of my accepted dispositions is wrong?**

Open with your seat token -- `FABLE_CXLANDF2_20261016` / `ASTRA_CXLANDF2_20261016` / `GROK_CXLANDF2_20261016` /
`GLM_CXLANDF2_20261016` -- then ONE line: `VERDICT: SHIP / SHIP WITH CHANGES (<n>) / DO NOT SHIP (<one line>)`.

## 1. The pass-2 verdicts (answers in `regress/artifacts/cxlaunchland_20261016/pass2/`)

* **GPT-6 Astra -- SHIP WITH CHANGES (2)** (`codex_cxland.txt`).
* **GLM 5.3 -- SHIP WITH CHANGES (2)** (`glm_cxland.txt`).
* **Grok 4.7 -- SHIP WITH CHANGES (1)** (`grok_cxland.txt`).
* **Fable 5.1 -- SHIP WITH CHANGES (2)** (`fable5_cxland_v2.md`).  ITS FIRST RUN FELL BACK: two Fable refusals, then
  claude-opus-4-8 wrote `FALLBACK_opus48_cxland.md` (credited as Opus 4.8, NOT Fable); the agent was resumed and Fable 5.1
  wrote v2 itself, re-affirming the fallback's findings.  **Fable disclosed that the fallback run executed the TRACKED
  launcher unmodified -- it names its codex binary under `$HOME` and honours no override -- and so launched NINE REAL Astra
  calls on a 13-byte brief before stopping them** (nothing written to any tree).  That hazard is now pinned (E0, below).

## 2. Every finding, numbered, with my disposition

| # | seat | finding | disposition |
|---|---|---|---|
| F1 | Astra | identity: a `model:` line is read from the first 40 stderr lines; with the header absent a QUOTED `model:` line could be read; and an unverified run still printed "answered by: <requested>" | **ACCEPTED, FIXED**: only codex's header BLOCK is read (`OpenAI Codex vX`, then the lines between the next two `--------` rules); an unverified run prints "seat answered -- model UNVERIFIED ... (requested: X)" and still exits 0.  Controls X6, M2 |
| F2 | Astra | the controls driver exits 0 whatever its tally | **ACCEPTED, FIXED**: it exits non-zero unless pass == total |
| F3 | Astra, GLM, Fable, Grok | delete the `^` from `grep '^ERROR:'` -> passes all 30 | **ACCEPTED, PINNED**: X1 (rc 1, empty stdout, only a PREFIXED quotation of a refusal line -> 6) |
| F4 | Astra | `model_reasoning_effort="$2"` -> `"$1"` passes all 30 (the fake ignores arguments) | **ACCEPTED, PINNED**: the fake logs its arguments; E1/E2 assert `-m` and `model_reasoning_effort=ultra` per call |
| F5 | GLM | the UNVERIFIED note misstated its cause; the 40-line window had one fixture behind it | **SUPERSEDED by F1** (no window now); header-line census quoted in the comment (Astra: line 5 in 599 of 600 codex `.err`, line 7 in one) |
| F6 | GLM | the ANSI strip widens the two recorded residuals to colour-prefixed quoted lines | **ACCEPTED as a RECORDED RESIDUAL** in the launcher's header (bounded by classify-on-failure) |
| F7 | GLM | a refused FIRST run's header is never compared | **RECORDED RESIDUAL** (its answer is discarded; the fallback's own run is compared) |
| F8 | GLM | "a coloured real wall" overstated the on-record warrant | **CORRECTED**: the header now cites the real coloured REFUSAL, `_scratchpad/panel_20260919_013302/codex_adv540p2.REFUSED1.err` (unstripped `^ERROR:` 0 lines, stripped 2 -- re-run by me) |
| F9 | Fable (C1) | the controls' baseline was the farm copy, which already had the quotation fix, so no control showed `cxlaunchquotation`'s defect | **ACCEPTED, FIXED**: a THIRD column runs the TRACKED file the landing replaces (`cxlaunch_tracked.sh`, md5 cb180d9d), via a scratch `$HOME` whose codex path is the fake; N1/N2 exit 8 there and 0 after, D1 7 there and 0 after |
| F10 | Fable (C2) | two bug-file statements are now false: the `cxlaunchdaybreak` heading and the rule statement "greps stdout freely"; the ruling's line numbers are stale | **ACCEPTED**: both corrected in place by content, quoting what they refute; the ruling's two targets re-located by id |
| F11 | Fable | `body -eq 0` -> `verd -eq 0` passes all 30 | **ACCEPTED, PINNED**: X2 (rc 0, an answer with NO verdict line, column-0 wall lines on stderr -> 0) |
| F12 | Fable | a suffix-only identity compare passes all 30 | **ACCEPTED, PINNED**: X5 (asked gpt-5-astra, header gpt-6-astra -> 5) |
| F13 | Fable | `-ne 0` -> `-eq 1`, and the strip narrowed to SGR, pass all 30 | **NOT PINNED, by Fable's own ruling**: the first is observable only inside the recorded N4 residual (a pin would assert its wrong exit), the second needs a shape with 0 instances on record; with GLM's precedence escape, FILED as `cxlaunchunpinned`, each measured to ESCAPE in the kill table |
| F14 | GLM | moving the wall exit above the refusal exit passes all 30 | **NOT PINNED** (no stderr on record carries both) -- in `cxlaunchunpinned` |
| F15 | Grok | `grep` without `-a` reads a stderr carrying a NUL as BINARY and prints `Binary file (standard input) matches`: the real 2026-09-19 wall `_scratchpad/cxfarm3_20260919/out/codex_l1_batterypreflight.err` (1,449 NULs from byte 2,318,517; its two column-0 usage-limit lines after them) was recorded exit 6 | **ACCEPTED, FIXED, measured by me on that file**: `grep -a`; X8 (a NUL before the wall lines) exits 6 on both older launchers and 8 after |
| F16 | Grok | exit 5 is new to callers: the farm pack runner special-cases 7 and 8 only and RETRIES a 5 | **RECORDED** in the launcher's header (a different model's answer is not this seat's answer) |
| F17 | Grok, GLM | N1's stderr says `reasoning effort: max` (a max-era run) while the control asks ultra -- so the effort must NOT be compared | **AGREED**; only the model is compared |
| F18 | Astra | census scope: inside GXEMUL-SEC 493 launch logs / 319 pairs, not 519 / 322 | **CORRECTED**: the header states both scopes (519 / 322 under the project root incl. `_scratchpad`) |
| F19 | Grok | `cxlaunchquotation`'s state note still prescribes the replaced fix; `cxlaunchwallfp`'s merge must say its fix was withdrawn | **ACCEPTED**: both written so |

## 3. Disagreements, both sides in their own words

* **Pin the five escapes now, or file them?**  Fable's fallback reading (Opus 4.8): *"above-floor coverage debt, not a
  clause-(d) breach of this landing ... FILE a row to add two pins."*  Fable 5.1 itself (v2): *"CHANGE from my earlier
  'file' to PIN NOW, under L1: the controls are uncommitted, so they are pre-ship construction ... Take four ... Skip two."*
  Astra required the `^` pin and the effort pin as changes.  **I followed Fable's v2** and Astra: four pins plus the
  header-block control, three escapes filed.
* **Does the ANSI strip have an on-record warrant?**  GLM: *"no real codex diagnostic on record is coloured -- the coloured
  walls that exist are quoted panel text -- so the strip's on-record warrant is consistency."*  Fable's fallback reading
  found a real coloured REFUSAL (`codex_adv540p2.REFUSED1.err`), which I re-ran: unstripped 0, stripped 2.  **I hold the
  strip warranted by that real instance.**
