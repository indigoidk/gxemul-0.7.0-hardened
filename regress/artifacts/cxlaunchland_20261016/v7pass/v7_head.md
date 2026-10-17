# V7 PASS -- `cxlaunchquotation` / `cxlaunchdaybreak`: the codex launcher `tools/cxlaunch.sh`, v7 = EACH CHECK DECIDED BY THE ROW, NOT BY THE LAUNCHER'S TEXT, AND THE V6 PASS'S FINDINGS SHARED

Four seats, by the owner's roster of 2026-10-16: Fable 5.1, GPT-6 Astra, Grok 4.7, GLM 5.3.  Opus, agy, kimi, deepseek and
minimax are DELIBERATELY NOT FIRED under that roster.  An ordinary review of a shell wrapper that launches a read-only
review CLI and classifies its exit, and of the test harness that pins it.  READ-ONLY: write nothing to any project tree.
The tree is `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC`; the v7 launcher is `tools/cxlaunch.sh` in the WORKING TREE
(uncommitted; v6 is preserved as `regress/artifacts/cxlaunchland_20261016/cxlaunch_landed_v6.sh`, md5 c53b99ab -- v7 changes
COMMENTS ONLY, and its executable lines are v6's byte for byte); the controls and mutant table are `run_controls_v7.sh`,
`run_mutants_v7.sh` and `mut_launcher_v7.py` beside it; the v6-pass answers are in `v6pass/`, with the main loop's
measurements of the v6 pass's claims in `v6pass/main_meas/`.  Everything a packet-fed seat needs is inlined below.

**This is the closing pass, in the shared-findings shape.**  Every seat answered the v6 pass blind to the others.  Here
every finding from every seat that answered is in ONE numbered list with my disposition (section 2), and the places where
seats DISAGREED -- with each other or with a measurement -- are set out with both sides in their own words (section 2c).
**Rule on the disagreements you are a party to first, and be HARDER on a disposition that adopts your own position than on
one that rejects it.**

**What v7 changed.**  The v6 pass found no floor breach (GPT-6 Astra, Grok 4.7 and GLM 5.3; Fable 5.1 walled twice) and one
shape in v6's OWN new checks: **a check that reads the launcher's text to decide what it expects.**  PK decided "is this
codex's own rc 7?" from the log's `codex exited 7`, so a refusal echo rewritten to that text passed all 269 (Astra).  v7
decides it by the ROW (R7X, and its rc-8 twin R8X), extends LOG to OV's non-default lines, adds RXM (each raw-status
message's own number), and rows four values no row had varied: a two-line brief (MB), occupied refused destinations (RN2),
a lower-case tag (TG), and every member of the ANSI strip's class in one line (CSX).  Controls 78 rows / 269 checks -> 83 /
289; kill table 133 -> 144 (Astra's nine, R8X's twin of `m_lost7`, and Grok's re-classification mutant).  The launcher's
own comments carried four of the false sentences (its exit list on codex's own rc 8, the UNVERIFIED conditions, the usage
line's "the brief is not checked"), so v7 edits them; nothing executable moved.

**The chain closes on this pass if it finds zero floor breaches that survive adjudication.**  Check the premises in 2b; do
not ratify them.

<TOKEN_LINE>

## 1. The v6-pass verdicts

* **Fable 5.1 -- SEAT FAILURE** (`v6pass/fable5_cxlandv6.md` is its stub: two md5 measurements, no findings).  Walled on a
  usage limit ("You've reached your Fable limit", HTTP 429) at 07:17 after writing the stub; re-fired ONCE at 07:5x under
  the walled-seat rule and walled again before any work.  Not counted as agreement.  It is fired again on this pass.
* **GPT-6 Astra -- SHIP WITH CHANGES (6)** (`v6pass/codex_cxlandv6.txt`).  Zero floor breaches over 32 construct groups,
  the 133 table mutants and nine outside-table one-edit mutants (A-I, reasoned 269/269), all graded clause-(e) debt; eight
  record corrections.  Its bash would not start, so every survival claim was REASONED.
* **Grok 4.7 -- CLOSE** (`v6pass/grok_cxlandv6.txt`).  Zero floor breaches over the 133/133 table (READ) and its
  outside-table sweep (REASONED; its bash would not start either); two items.
* **GLM 5.3 -- SHIP WITH CHANGES (3)** (`v6pass/glm_cxlandv6.txt`, packet-fed).  Zero floor breaches; three unnamed edges,
  three kill-table record defects, one census question.

## 2. Every finding, numbered, with my disposition

| # | seats | finding | disposition |
|---|---|---|---|
| Z1 | Astra (A) | PK keyed codex's own rc 7 on the log's `codex exited 7`: the refusal echo rewritten to that text passes all 269, and real refusals lose `The answer is LOST`, the done marker the runner reads | **PINNED by the ROW**: PK decides R7X and R8X by row identity, never by the launcher's text; every other exit-7 row must print LOST.  Mutant `m_lostecho7` |
| Z2 | Astra (on Y11) | "`SEAT WALLED` iff exit 8" is false of codex's own rc 8 with an answer: it prints `codex exited 8` and exits 8 | **CORRECTED and PINNED**: "iff the CLASSIFIED wall exit" in the CONTRACT, PK's label, the launcher's exit list and the CHANGELOG; row R8X (rc 8 with an answer -> 8, no SEAT WALLED) and check R8XL.  Mutant `m_rc8wall` (`m_lost7`'s twin at the wall exit).  The launcher's exit list now also says what the pack runner does with each: it keys its messages on the STATUS (a 7 is reported "REFUSED on both models", an 8 stops the pack -- `run_pack_body.sh` lines 48-49) and its done test on the phrases, so it retries either |
| Z3 | Astra (B) | LOG's runs all asked `ultra`: `asked: $1 / ultra` passes | **PINNED**: LOG also compares OV's two lines (`m-primary / low`, `m-fallback / high`).  Mutant `m_askedultra`.  **Grok graded the same edit display-only -- 2c, D1** |
| Z4 | Astra (C) | the raw-status message's number: `codex exited 7 --` hardcoded passes (only R7XL read the number, against 7) | **PINNED**: RXM -- RC1A, RC3A, FR, R7X and R8X each say `codex exited N` with N their own rc.  Mutant `m_rcmsg7` |
| Z5 | Astra (D) | every brief was one line: `"$(head -n 1 "$BRIEF")"` passes | **PINNED**: row MB, check MBA (a two-line brief reaches codex whole, as ONE argument).  Mutant `m_briefhead` |
| Z6 | Astra (E, F) | the refused destinations were always fresh: `mv -n` passes at either move | **PINNED**: row RN2 (both `.refused.*` pre-seeded with stale files), check RN2F (each REPLACED, byte-for-byte this run's).  Mutants `m_mvntxt`, `m_mvnerr` |
| Z7 | Astra (G) | every tag was upper-case: `TAG="${3^^}"` passes | **PINNED**: row TG (tag `tg_lower`), check TGF.  2,352 of the 2,383 `codex_*.err` tags on record are lower-case (`v6pass/main_meas/TAGCASE.txt`).  Mutant `m_tagupper` |
| Z8 | Astra (H, I) | the strip class's members: `[0-8;]` and `[A-Zm]` pass | **PINNED, the class EXHAUSTED**: row CSX -- one stderr line carrying `ESC[0;1;2;3;4;5;6;7;8;9m` and `ESC[1<L>` for every letter A-Z and a-z, then `ERROR: ...flagged...` (rc 1 -> 7; the tracked and before files read 6).  Mutants `m_strip8`, `m_stripazm` |
| Z9 | Astra, all four | the completeness language -- "every decision ... each pinned or disclosed" -- unsupported while nine one-edit escapes stood | **NARROWED**: the CONTRACT heading, the OB block and the closure note claim each LISTED decision's named edges, and say rows SAMPLE briefs, tags, out-dir states and header shapes; the strip's class and the patterns' alternatives are the only sets EXHAUSTED |
| Z10 | Astra, GLM | "every rc row and every Daybreak answer sits off CENSUS_v5's diagonal" is false: the Daybreak answers (DB_OK, OV2) and D5's refusal sit ON it, and a real fallback receipt exists | **CORRECTED**: the rc rows (RC1A, RC3A, RC2W, IR, FR, RN, R7X, R8X) sit off it; the Daybreak answers on it, synthetic in no shape, their refusal-then-answer sequence with one real instance (`dossier_gdromdma.launch.log`) |
| Z11 | Astra (on Y16) | the `cxlaunchempty` records said the launcher checks the brief's "neither existence nor size" -- it checks the size against the argv cap | **CORRECTED** in the OB bracket and the ledger note: the size only, against the cap, before the `cd`, from the caller's directory; neither existence nor a minimum size |
| Z12 | Astra (on Y16) | "a missing or relative brief reaches codex as an EMPTY prompt" -- a relative path can resolve from the project root, and then a file IS read | **CORRECTED** in the launcher's usage line, the CONTRACT, the OB bracket, the ledger note and the CHANGELOG: a missing brief, or a relative one that does not resolve from the project root |
| Z13 | Astra (on Y14) | "model UNVERIFIED, exit 0, with no model line" needs its conditions | **CORRECTED** in the launcher's exit list and residuals and the CHANGELOG: a run that ANSWERED (rc 0, a non-empty stdout, no earlier exit) |
| Z14 | Astra | the v6 brief and draft said "all four seats graded the v5 pass ZERO floor breaches"; GLM's v5 answer labels its Changes 1 and 2 floor breaches | **CORRECTED** in the CHANGELOG: three graded zero, GLM two -- the truncation and effort edges, both rowed in v6 (RS/RSF, OV/OVA) whatever their grade |
| Z15 | Astra (on Y26) | the caller derivation: the quoted grep's scope cannot find `census_v5.py`, which parses the `codex rc=` line, not the four phrases | **CORRECTED** in the CONTRACT: the PHRASE readers are the two pack scripts; `census_v5.py` reads the rc line (LOG) |
| Z16 | Grok (on Y25) | Y25 said D4 pins that `classify` re-runs on the fallback; D4's second run refuses too, so it cannot | **AGREED, and MEASURED in the table**: the CONTRACT names the rows that do -- D1, D2 and every row whose fallback answers (D3, OV, RN, RN2, FR): a stale refusal count would exit 7 -- and `m_noreclassify` (the fallback's `classify` deleted) is killed by D1 and D2 |
| Z17 | Grok | the exit-0 UNVERIFIED line's text after `model UNVERIFIED` is unpinned and off the display bullet | **DISCLOSED** in the display bullet, with what IS pinned (N1V and WMT the answered phrase whole; the loop `model UNVERIFIED` and no `answered by:`) |
| Z18 | GLM (1) | the STREAM of each caller-read phrase: moving a phrase to stderr passes (the controls merge the streams) -- "not settleable from the packet" | **SETTLED by reading, DISCLOSED as equivalent**: both phrase readers read `launch.log`, which `run_pack_body.sh:66` writes with `> launch.log 2>&1` |
| Z19 | GLM (2) | the RAN grep's missing `-a`: a NUL in an opening block makes grep print `Binary file`, RAN garbage, exit 5 -- fail-safe | **MEASURED: EQUIVALENT, not fail-safe.**  Bash drops every NUL in `HDR=$(...)` before the grep reads it (warning `ignored null byte in input`): a NUL in the workdir line verifies; one INSIDE the model name is deleted -- `gpt-6-a<NUL>stra` verifies as gpt-6-astra; one after `gpt-6-other` still exits 5 (`v6pass/main_meas/NUL_HDR.txt`).  0 of the 979 opening blocks on record carry a NUL (`NUL_BLOCKS.txt`).  DISCLOSED with that.  **2c, D2** |
| Z20 | GLM (3) | a `?`-parameter CSI, and the census's 2 "other ESC" files, are unnamed | **DISCLOSED, measured**: neither is stripped, so a refusal behind one exits 6, 5 or the raw rc on the shapes the launcher classifies -- never 0, never 7; 0 of 8,601 `.err` files carry a `?`-CSI, and the 2 other-ESC files (two `lcabadval` audits) carry none before an `ERROR:` (`v6pass/main_meas/ESC_WHERE.txt`) |
| Z21 | GLM | kill-table record defects: `m_ws1` "killed by WMT WS", `m_head40`'s list omits X9, `m_v2awk`'s tally one short | **REFUTED by reading `KILLTABLE_v6.txt`, which the packet inlined verbatim**: `m_ws1` reads `killed by: WMT WZ`; `m_head40`'s list carries X9; `m_v2awk`'s 8 reds are rows X10, W13, K31, HB and the UNVERIFIED loop's X9, W13, K31, HB -- the loop names `M2 X6 X9 W13 K31 NM HB R9B`, not X10.  **2c, D2** |
| Z22 | GLM | CENSUS_v5 read 2,425 codex `.err` files and RULELEN 2,427 -- unreconciled | **SETTLED**: the same roots and the same name test; CENSUS_v5 ran at 02:59 and RULELEN at 04:34, and seat runs wrote two more files between (2,429 at 07:50, `NUL_BLOCKS.txt`).  Each count is true of its run |
| Z23 | main loop | v6's synthetic list put RS, MP and OV under "CENSUS_v5.txt names each count" -- caller inputs, which no census counts | **CORRECTED**: RS, MP, RN2, OV, MB and TG are listed as CALLER inputs |

## 2b. Premises to CHECK (stated as questions)

* **PK by the row** (Z1, Z2).  Is keying R7X and R8X on row identity sound -- does any other row's exit 7 or 8 come from
  codex's own rc rather than a classification, so that PK now demands LOST or SEAT WALLED where the launcher rightly prints
  neither?
* **CSX** (Z8).  Does one line carrying every member EXHAUST the class -- can a one-edit change to the strip keep CSX's line
  starting with `ERROR:` after the strip while dropping a member?
* **The NUL measurement** (Z19).  Is "bash drops the NUL before the grep" true of the bash the launcher runs under (git-bash
  5.2.26 here), and does it make the missing `-a` equivalent for EVERY placement of a NUL in an opening block?
* **The launcher's comment edits** (Z2, Z12, Z13).  Is each new sentence true of the executable lines, which did not move?
* **Anything else** -- after v7, is there a decision of `tools/cxlaunch.sh` whose edge no row straddles and no disclosure
  names, or a v7 check that reads the launcher's text to decide what it expects?
