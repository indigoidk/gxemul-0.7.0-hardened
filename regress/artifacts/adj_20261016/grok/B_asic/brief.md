# Grok adjudicator -- packet B (READ-ONLY; plan mode)

Open with the token `GROK_ADJ_B_20261016`.  You are one of three independent adjudicators (Grok 4.7, Fable 5.1, GPT-6 Astra).  The packet follows in full; every file it cites is on disk under C:/DocumentNoSnc/cc/GXEMUL -- open what you rely on, say READ vs REASONED, and answer its QUESTIONS section exactly as it directs, VERDICT LINE FIRST.  The tree under review is GXEMUL-SEC at HEAD e483d931 (`git show e483d931:<path>`); the working tree carries two sessions' uncommitted edits (dev_wdc.c is not one of them); ignore the project root's pristine 2021 `src/`.  Write nothing.

---

# ADJUDICATION PACKET B -- asiceventaddr: the final build's pass-2 findings and grok's fixture-pin draft

Prepared 2026-10-16 ~11:4x CDT by the main loop (Opus 5.5, session 087a90).  Owner directive of 2026-10-16:
**"Adjudicate any pending findings with both the Fable, Astra, and Grok."**  Three adjudicators answer this packet
independently: Fable 5.1 (Agent seat), GPT-6 Astra (codex, ultra), Grok 4.7 (xhigh, plan mode).

This is the ADJUDICATION PASS (BRIEF_TEMPLATE §F2).  It is an ordinary regression-instrument coverage review for a
device-model test suite.  **READ-ONLY: write nothing to any project tree.**

## 0. Ground rules

- Tree: `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC` at HEAD **e483d931**; read committed text with
  `git -C C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC show e483d931:<path>`.  The project root's `src/` is pristine 2021
  upstream -- never read it.  Rules: `GXEMUL-SEC/tools/CLAUDE.md` (working tree; D2 and the 10-09 rulings are
  working-tree only).  Excerpt with line numbers:
  `C:/DocumentNoSnc/cc/GXEMUL/_scratchpad/gweb/jobs_20261016_argonpack7/_support/carrier_floor_rules_excerpt.md`.
- Nothing about this round is committed.  The final build is a FROZEN CANDIDATE.  HEAD's
  `src/include/thirdparty/dreamcast_sysasicvar.h` ALREADY holds the range macro (`SYSASIC_EVENT_RANGE_OK` :135-137,
  `SYSASIC_EVENT_TO_ADDR` :139-140, `SYSASIC_EVENT_TO_BITMASK` :141, `SYSASIC_TRIGGER_EVENT` with `uint8_t buf[8]` :143-150);
  the final build's header diff adds 15 comment lines above them and **leaves the macro bodies byte-identical** (I
  diffed HEAD :135-170 against the composite :150-185: identical).  The composite with the final diffs applied:
  `C:/DocumentNoSnc/cc/GXEMUL/_scratchpad/gweb/jobs_20261016_argonpack7/_support/asic_final/{dreamcast_sysasicvar.h,
  dev_dreamcast_asic.c, dev_dreamcast_gdrom.c}`.
- Separate READ / REASONED / MEASURED.  Count arguments, not seats.

## 1. Evidence index (paths relative to `GXEMUL-SEC/regress/artifacts/` unless absolute)

| short | path | what |
|---|---|---|
| FB | `asiceventaddr/f2_20261013/opus5_final/` | the final build: `deliver/` (sysasic_range_check.py, sysasic_range_cases.c, six diffs incl. gate_offline.sh.diff), SUMMARY.txt, PRETABLE.out, STATUS.md, table2_20261013/ |
| OM | `asiceventaddr/finalpass_20261013/opus5/` | MEASURING seat on the final build: STATUS.md (verdict and every log named), q1_manifest.tsv, q1_results_fixed.tsv (395 one-token media), typed_results.tsv, pinbreak/RESULTS.txt, pins/asanleg.txt, logs/s4b_pins.out, logs/s11_latent.out, bothsweep/RESULTS.tsv; own MANIFEST.md5 |
| CXA | `asiceventaddr/finalpass_20261013/codex_rerun/codex_asicpass_records.txt` | Astra records-framed rerun (the panel's codex run did not return a verdict) |
| GPA | `asiceventaddr/finalpass_20261013/panel_20261013_234442/` | panel: grok CLEAN, minimax CLEAN, kimi substitute CLEAN, deepseek "BUILT", glm BREACH (`buf[8]`), agy/kimi CLI no answer |
| GAA | `asiceventaddr/finalpass_20261013/grok_adversarial_finalpass.txt` | grok adversarial: ESCAPE (the memory_rw length) |
| ARA | `adj_20261016/inputs/argon_asic_r1.out` | Gemini 4 Argon reading, tally `10 ATTACKS 1 BROKEN 5 HOLDS 4 UNSETTLED` |
| PIN | `agypack_20261013/asicpins_spec/grok_asicpins_spec.txt` | grok's draft: pins A (full-width length), B (AddressSanitizer on the two run rows), C (writeflag vs memory.h); 5 records; 4 open questions |
| PINA | `agypack_20261013/asicpins_spec_adv/grok_asicpins_spec_adv.txt` | a second grok run asked to break PIN: ESCAPE (the paren-drop) |
| ADJB | `asiceventaddr/adj_20261013/` | the 10-13 ruling that ordered the final build ("SHIP WITH CHANGES (10)") |
| PSB | `adj_20261016/prescreen/prescreen_asic.md` | IF PRESENT: an Opus pre-screen of the agy-pack second readings (grok + Argon) of the asic briefs; its LIVE list is part of this adjudication.  If absent, say so. |

## 2. Findings F1..F16 with MY DISPOSITION

**F1. TRIGGER's `memory_rw` length `8` -> `0x100000008` (one token; also `8+(1ull<<32)`, `-4294967288`) passes all 30
rows; product objects differ (the maple object passes the wide length).**  MEASURED (OM 00:05, 00:25); GAA ESCAPE
(independent); CXA "INCONSISTENT" (the docstring says "length 8" while the stub records `rw_len = (int)len`).  **MINE:
ACCEPT, FLOOR** (the contract claims the length argument is pinned; the stub narrows it).  Repair: PIN's pin A, REFINED
-- record and compare at `size_t` width (`len == (size_t)8`, printing `(unsigned long long)len` with `%llu`) rather than
through `(long long)`, which is PIN's own open question 3; OM measured the long-long form red on all four wide values
and green on 109 shipped-green media.

**F2. `uint8_t buf[8]` -> `buf[1]`/`[2]`/`[4]`/`[6]`/`[7]` (one token) passes all 30 rows; product objects differ; gcc
prints "-Wstringop-overflow" 112 times and the driver reads only `error:`.**  MEASURED (OM); glm BREACH (independent).
In `dev_dreamcast_gdrom_dma_access` the 4-byte buffer moves to 0x24(%rsp) and the product's 8-byte
`memory_writemax64` overwrites the low four bytes of the saved %rbx (OM 00:4x, logs/s12_frame.out).  **MINE: ACCEPT,
FLOOR.**  Repair: an extent pin -- form disputed, D1.

**F3. The stub's `#define MEM_WRITE` drifted to 2 (or 0) keeps BASE green, and under the drifted stub a header passing
literal 2 passes (red on the shipped stub).**  MEASURED (OM pinbreak: `weak_mw2`, `weak_mw0`).  The cases-file comment
"a stub that drifted from these two lines reds the committed header" is FALSE for MEM_WRITE.  **MINE: ACCEPT -- RECORD
(PIN record 3) plus PIN's pin C** (record `writeflag`, compare it to `memory.h`'s `MEM_WRITE` the way flags are compared
to 32).  L1: the round is unshipped.  Contested by PIN itself (open Q2): D3.

**F4. Paren-drops `(e) >= 0` -> `e >= 0` and `(e) < 96` -> `e < 96` inside `SYSASIC_EVENT_RANGE_OK` pass all 30 rows
with product objects IDENTICAL, yet ACCEPT out-of-domain raises spelled as low-precedence expressions:**
`1 ? 200 : 5` under either drop, `200 | 0` and `100 ^ 4` (= 96) under the second -- which the committed header REFUSES.
MEASURED acceptance (OM logs/s11_latent.out; q1_results_fixed.tsv lines for `q1s_R_e1noparen` / `q1s_R_e2noparen`).
OM: "not a breach by the brief's rule" (product-identical today: every product raise passes a define).  PINA: ESCAPE,
"the row owed is one TRIGGER refusal of `1 ? 200 : 5` ... That single expression kills both paren-drops."
**MINE: FLOOR -- ROW IT (one TRIGGER compile that must be REFUSED: `SYSASIC_TRIGGER_EVENT(1 ? 200 : 5)`).**  The
macro's contract is over ARGUMENT EXPRESSIONS, not over today's call sites; product-identity today is not equivalence
on the macro's domain, and a parenthesis dropped from a macro is a textbook plausible edit.  Contested: D2.

**F5. Census:** the gate's lexical population count stays 4 with maple switched to a wrapper header while FIVE TUs reach
the header -- the DISCLOSED hole, re-measured (OM logs/s14_wrapper.out); and the gate comment's "an unanchored LINE
count is 5 at e483d931" is wrong -- the cited `git grep -n 'thirdparty/dreamcast_sysasicvar' -- src` gives 6 at
e483d931 (gdrom.c:288 also spells the path), 5 only on the composite after R10.  **MINE: disclosure stands; RECORD
(PIN record 4).**

**F6. `cpu->byte_order`:** `memory_writemax64` reads it (`memory.c:92`); the stub ignores it.  PINA's round-trip
argument: the device builds `idata` with `memory_readmax64`, the inverse, so a big-endian cpu round-trips to the same
`idata` -- no row owed.  **MINE: ACCEPT (no row); list the field in the fixture class table** (PIN's table omits it).

**F7. `static uint8_t buf[8]`** passes, objects differ, guest values identical (one raise overwrites all 8 bytes before
the device reads them; reentrancy only).  OM, PINA.  **MINE: (e) DISCLOSED** in the contract.

**F8. Typed cells:** of 58 type-identity cells, 14 green (long, unsigned long, plain char at 0/95; `_Bool` at 0/1), all
product-identical; `_Bool` disclosed; the other three are type identities inside sampled sizeof/sign classes.  OM.
**MINE: RECORD (disclosure precision), no row.**

**F9. Table 2's 23-26 EQUIVALENT/DISCLOSED classifications reproduce** (OM Q2: every row line the same, product objects
identical, compiler stderr identical; CXA Q2: supported within their stated scope).  **MINE: ACCEPT.**

**F10. CXA: "A TRIGGER that stops calling ADDR keeps every ADDR row green; these rows, TSWEEP and CENSUS see it" is too
broad** (`e_dblguard_bypass` computes the address directly and guards BITMASK; recorded green correctly).  **MINE:
RECORD** -- these rows detect loss of the refusal or changed counts, not ADDR route identity.

**F11. CXA: the `product_defines` docstring says "neither a commented-out copy ... can satisfy it", but its line
regexes do not strip multi-line comments.**  **MINE: RECORD** -- call it a lexical uniqueness check.

**F12. The pass-2 handle alias (`want_mem = c`) keeps BASE green and lets `t_memalias` pass; the F20 distinct-object
repair catches it** (OM pinbreak).  **MINE: no action.**

**F13. The premise question (where did grok read the header?).**  PIN and PINA cite RANGE_OK `:137`, TO_ADDR `:140`,
TO_BITMASK `:141`: those are HEAD's lines, 15 below the composite's.  The macro bodies are byte-identical (diffed).
**MINE: SETTLED -- no claim in PIN/PINA changes against the final header; only their line numbers are HEAD's.**

**F14. PIN records 1, 2, 5** (the "length 8" paragraph; the CATCHES claim; the four "until 2026-10-13" sentences to
take the closing commit's date).  **MINE: ACCEPT.**

**F15. Panel CLEANs (grok, minimax, kimi substitute) and deepseek "BUILT"** -> REFUTED on Q1 by F1/F2 (measured).
codex panel seat: no verdict; records rerun answered (CXA).  agy and the kimi CLI did not answer -- seat failures.

**F16. PIN's landing shape for pin B** (inside `run_row`, so the gate's `--prod-flags` cannot drop it -- PIN open Q4).
**MINE: ACCEPT inside `run_row`;** OM measured the flag on every PROD row and the red set was still only ID and TVAL.

### My build list as disposed (for you to attack)

Pin A at `size_t` width (F1); an extent pin (F2, form per D1); pin C + record 3 (F3); one refusal row for
`1 ? 200 : 5` through TRIGGER (F4); records 1-5 (F5, F14), the byte_order line (F6), the static-buffer and typed-cell
disclosures (F7, F8), the two CXA wording corrections (F10, F11).  PRETABLE first.  Before the table, MEASURE under the
chosen extent pin the four product-equivalent variants PIN lists as "must stay green" (a pointer refactor of an 8-byte
object, a cast, `buf + 0`, `(size_t)8`) -- PIN open Q1 says none was built under AddressSanitizer.

## 3. DISAGREEMENTS D1..D4

**D1. Extent pin form (F2).**  OM measured three forms and a combined `both` stub: a `sizeof` capture over the
serializer call (110 media, 13 red exactly as intended, zero false reds), an AddressSanitizer leg (red on `buf[1/4/7]`
and `buf + 1`, green on BASE/HEAD/`buf[16]`; does NOT catch the length), and `-Werror=stringop-overflow` (red on the
shrinks, but only because `-O3` inlines the store).  PIN chose AddressSanitizer and DECLINED `sizeof` because on LP64
`sizeof` of a pointer is 8: it cannot red a pointer to a 4-byte array and passes for the wrong reason ("Repairing only
the array lvalue and leaving the decayed pointer open is the cell-by-cell chain this repair is not allowed to repeat"),
and declined `-Werror` as a heuristic.  **Ruling (mine): AddressSanitizer (PIN)**, provided the four equivalent variants
are measured green under it before the table, and the gate's toolchain is shown to link `-fsanitize=address` (OM did
it in a WSL clone; the gate runs in WSL Gentoo).  Opus measured `sizeof`; grok declined it -- each of you, argue the
other side's case before ruling.

**D2. The paren-drop (F4): FLOOR or EQUIVALENT?**  OM: product-identical, so "not a breach by the brief's rule".  PINA:
ESCAPE, row owed.  **Ruling (mine): FLOOR, one row** -- the equivalence class in table 2 was judged on product objects,
and the two paren-drops are the measured counterexample that product-identity is narrower than macro-equivalence.  If
you uphold OM, the contract must then DISCLOSE that the refusal is guaranteed only for primary-expression arguments.

**D3. Pin C (F3): owed, or a record fix only?**  PIN open Q2: the shipped composite already reds when the HEADER alone
changes (pinbreak `q1_T54_MEM_WRITE_2` red on the shipped stub); the escape needs the STUB to move too.  Class closure
says close it here; the stopping rule says fix the false pass or wrong record and file the rest.  **Ruling (mine):
adopt pin C** -- L1 construction on an unshipped round, one line, and the record is wrong either way.

**D4. Pin A's comparison width** (PIN open Q3): `(long long)len` (measured: red on a value above `LLONG_MAX`) vs a
`size_t`-width compare (Argon's `rw_len = (len == 8) ? 8 : -1`, not swept).  **Ruling (mine): `size_t` width, and
print the full value** -- no signed conversion anywhere on the path; the long-long form's measured red is kept as the
control.

## 4. What is still owed, and where I may be fooling myself

- I accepted or refined 15 of 16.  Suspicious count.
- The AddressSanitizer pin's four "must stay green" variants are unmeasured, and the gate's ability to build with
  `-fsanitize=address` is assumed from one WSL clone.
- F4's row: is `SYSASIC_TRIGGER_EVENT(1 ? 200 : 5)` refused by the committed header through TRIGGER (OM s11 says
  "through BOTH routes"), and does ONE row truly kill both drops (`1 ? 200 : 5` is accepted under either drop -- s11)?
- The census hole stays disclosed; nobody has argued it should close in this round.
- PSB may hold a LIVE item.

## 5. QUESTIONS (answer all; VERDICT LINE FIRST)

Open with your seat token and ONE verbatim line from `asiceventaddr/finalpass_20261013/opus5/STATUS.md` (its
`## SUMMARY (final)` section).

`VERDICT: UPHOLD ALL / UPHOLD WITH CHANGES (<n> rulings changed) / OVERTURN (<the load-bearing ruling>) -- <one line>`

1. Adjudicate F1..F16 and D1..D4: UPHOLD / OVERTURN / REFINE / CANNOT SETTLE, one line each with the reason.
2. **WHICH OF MY ACCEPTED DISPOSITIONS IS WRONG?**  I accepted or refined 15 of 16.  Agreement is not evidence.
3. **WHAT DID ALL OF US MISS?**  In particular: is the fixture class table (every stub parameter against the product
   prototypes in `memory.h`, `cpu.h`, `memory.c` at HEAD; every buffer extent the macros pass) complete after pins
   A/B/C and F6?  Name any parameter or extent still UNPINNED.
4. Does my build list close the round's floor so that the CLOSING pass verifies an enumeration rather than hunts?
5. If PSB exists: rule on each item in its `## LIVE items for the adjudicators` list.

Seat-specific:
- **Fable 5.1**: you wrote the 10-13 ruling (ADJB) that ordered this build -- self-review; be harder on its gaps.
- **Grok**: PIN, PINA, GAA and the panel grok answer are four of your runs; the panel answer said CLEAN and was
  refuted by measurement.  Attack PIN first; D1 adopts PIN's choice -- scrutinise it more.
- **Astra**: CXA is yours.  You cannot run code -- say where a claim needs a run.
