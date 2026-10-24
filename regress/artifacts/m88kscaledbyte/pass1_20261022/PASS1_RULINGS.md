# T1 (`m88kscaledbyte`) -- pass-1 design review: rulings (main loop, 2026-10-22; HEAD cb2eba1e at firing)

**[Corrected 2026-10-23 after the adjudication (its Q4 last paragraph) and the pass-2 drafter: the line below was
written before DeepSeek answered and before Argon failed.  The evidence basis of the ADJUDICATED pass 1 is FOUR
reviewing seats -- GPT-6 Astra as reviewer, Grok 4.7, GLM 5.3 (two firings), DeepSeek v4-pro (two firings,
`ollama_deepseek_t1p1_Q12.txt` / `_Q34.txt`) -- plus GPT-6 Astra as ADJUDICATOR (`adj/codex_t1p1adj.txt`, AMEND);
Gemini 4 Argon is a SEAT FAILURE (`argon_t1p1.DROPPED.txt`), Fable 5.1 is HELD.  Neither absence is agreement.  The
"all three seats agree" cells in A-C are the pre-adjudication record and section E's amendments supersede them.]**
*(pre-adjudication text, kept:)* **Evidence basis: 3 of 4 rostered seats** (owner roster 2026-10-20/21: GLM 5.3 + Grok + Astra + Fable).
GPT-6 Astra `ultra` (`codex_t1p1.txt`, 19,643 b, rc 0, header model verified) -- READY WITH CHANGES.
Grok 4.7 xhigh plan-mode (`grok_t1p1.txt`, 21,832 b, rc 0) -- READY WITH CHANGES.
GLM 5.3 cloud, packet-fed, TWO firings of one seat per the one-question-per-packet rule (`ollama_glm_t1p1_Q12.txt`
17,369 b; `ollama_glm_t1p1_Q34.txt` 9,008 b; both plain text, verdict first, finished tails) -- READY WITH CHANGES.
Fable 5.1: DELIBERATELY NOT FIRED (`fable5.HELD.txt`, owner holds of 10-21/10-22; hold question carried there).
NOT FIRED by owner roster: agy, kimi, deepseek, minimax, opus5.  Every seat answered; no seat failure.
Provisional on its face until the Fable hold lifts; the build proceeds because all three answering seats agree on
every design point and the Fable stage is HELD with its question.

Dispositions are by seat answer file : line.  The main loop's own checks are in `CHECKS_mainloop.md` (11 items).

## A. The repair -- SETTLED, all three seats agree

| # | ruling | Astra | Grok | GLM |
|---|---|---|---|---|
| A1 | Remove the WHOLE arm `generate_m88k_loadstore.c:254-257` (condition, `printf("\tNULL")`, `continue`, brace).  Deleting only the `continue` emits two initializer tokens (the drafter's P5 upheld). | :46 | :45 | Q12:31 |
| A2 | Keep `:104-105` (the generation early return): without it `loadstore()` emits duplicate `LS_N`/`LS_GENERIC_N` definitions under the unscaled byte names; the generated-definition count stays 198. | :46, :57 | :41 | Q12:29 |
| A3 | The decoder is NOT edited (S4/S5; the ajfa `op != 3` recipe is not in this tree and cannot reach `xmem_slow`'s own `scaled`). | :85 | :59 | Q12:37 |
| A4 | All 24 slots alias to the 12 unscaled byte handler names (the counterpart at index-32); the 8 slots with no producer today are aliased too -- a partial repair would ADD a predicate, which is the clause-(d) shape. | :11-44 | :10-39 | Q12:10-27 |
| A5 | The committed generated table `src/cpus/tmp_m88k_loadstore.c` is REGENERATED IN THE SAME COMMIT (24 lines `NULL` -> name; 296 -> 272 NULLs; 512 entries).  Both files land byte-identical in `est/` (precommit section A; neither is on `tools/est_divergence.txt`) and are propagated to the three build trees with the two-part clearance.  `Makefile.skel:134-135` is dependency-driven, so both artifacts are live fixed sites. | :59-61 | :47 | Q12:33 |
| A6 | P1 ("`cpu_m88k.c:130` forces big-endian") is FALSE: the loader (`emul.c:651-652`, `file_elf.c:693-694`) and a config `byte_order` (`emul.c:737-738`) set little-endian later; 16 of the 24 cells have a producer today (12 sync both endians + 4 nosync plain), 4 gain one after N2, 4 have none.  P2/P3 confirmed. | :63-74 | :51-55 | Q12:35 |

## B. The detector -- SETTLED on shape and pins

| # | ruling | Astra | Grok | GLM |
|---|---|---|---|---|
| B1 | TWO LEGS, both required by clause (b)'s "every fixed site": (i) compile and run the REAL generator (it has its own `main`; no `#include` harness) and pin its stdout; (ii) read the COMMITTED table with a reader parametrized by file and array size (`[512]`; the `#375` `ls_entry` hard-codes `[32]` and `$MIPSLS` -- CHECKS #2); plus (iii) full fresh-vs-committed equality.  Either leg alone is green under the other site's reversion (both seats' revert matrices). | :168-180 | :120-122 | Q34:7-17 |
| B2 | Primary pins: ABSOLUTE handler names BY EQUALITY at all 24 indices (both endian halves; the expected names come from the design, never from the committed file), in BOTH artifacts.  The relative `slot[i] == slot[i-32]` row is NOT a pin (anchor rule R11): it holds under a joint rename and under `NULL == NULL`. | :150 | :101 | Q12:56 |
| B3 | Accept pins by equality: scaled HALFWORD 161 (`m88k_instr_ld_u_2_le_scaled_regofs`) and 177 (`..._2_be_scaled_regofs`) -- rule D2's B+1 edge of `:80`'s `size > 0`, and the kill for v6's only silent form (`size > 0` -> `size > 1`, first difference 161, which a word-only row cannot see); scaled WORD xmem 434/438 (BE) and 418/422 (LE); unscaled byte 144, 400, 404; the 24 counterparts as supplementary. | :146-148 | :91-99 | Q12:54 |
| B4 | Structural rows: exactly one 512-entry initializer per artifact; NULL count == 272 by equality as a SUPPLEMENTARY row (Grok :124: not the floor carrier -- a moved NULL keeps the count; the absolute pins are the carriers); generator stderr `generated_functions = 198` and 198 `#define LS_N` blocks as the control on the kept early return (deleting `:104-105` keeps every name pin green and shows up only there and at link time). | :152-162, :187 | :114-116 | Q34:23-26 |
| B5 | A missing or non-compiling product is an EXPLICIT RED `check` row, never `need_file` (which `gate_skip`s, `lib.sh:147-151`) and never `check_min`. | :192 | :124 | Q34:26 |
| B6 | Clause (c) medium, by instrument kind (offline): a COMMENT-ONLY generator source -> the compile row reds; a COMMENT-ONLY committed table -> every reader row reds.  The identity `xmem` body (the crit packet's framing) is the medium of a runtime handler instrument and does not apply.  Record form: both legs are RUN ONCE by the builder and recorded `(c): measured at <artifact>`, the stronger of the two permitted forms. | :102-108, :194 | :69, :126 | Q12:47, Q34:30 |
| B7 | Clause (d): the repair adds no predicate (pure deletion), so the (d) form is the arm re-introduced under a DIFFERENT predicate -- the seats' v1-v4 (first differences 160 / 416 / 168 / 224), all killed by the absolute pins.  Astra files v1-v4 as "partial (b)", Grok and GLM as (d): a classification difference with NO row consequence (same pins kill them); recorded, not settled by vote.  The table builds ONE representative (v2, Grok :76 / Astra :100 -- the `no_pc_sync` predicate, first difference 416) plus the endianness narrowing GLM Q12:52 names (one half left `NULL`), since that is the shape a BE-only pin set would miss. | :98-100, :110-123 | :71-79 | Q12:48-50 |
| B8 | Floor enumeration: Astra :138-144 and GLM Q12:52 -- all 24 cells are the OUTPUT CONTRACT; Grok :84-89 -- the FLOOR (R7, producible cells) is 16, the 8 no-producer cells clause (e) "pinned in the same equality list".  All three pin all 24, so no row differs.  CONTRACT HEADER states Grok's split: an escape at one of the 16 is a floor breach, at one of the 8 is coverage debt. | :138-144 | :84-89 | Q12:52 |
| B9 | DEPENDS-ON bound: the edited lines are in `main()`; `print_function_name`'s `:74`/`:80` tests are callee compares -- clause (e), not floor (R5).  The halfword pin is still OWED as the accept side of the deleted predicate (B3), not as a floor cell. | :141, :148 | :82, :99 | Q12:52-54 |
| B10 | Home: GATE 2 (`regress/gate_offline.sh`), a new driver `regress/diff_m88k_loadstore_gen.sh` on the committed `diff_autodev_gen.sh` pattern (#406: derive the expectation from the generator's INPUTS, never from the committed output; scratch copy, never run the generator in-tree), wired in a block placed away from the foreign uncommitted hunks (CHECKS #11).  Presence pins name each floor row (deleting one is a red row). | :170 | :124 | Q34:17 |
| B11 | No floor cell is observable only on a guest path; the exchanged-byte / neighbour-preservation / zero-extension channels are the BLOCKED rung-3 witness's and stay with the owner's record (`WITNESS_ATTEMPT.md`); the contract header says so instead of claiming them. | :196 | :128 | Q34:34 |
| B12 | Bounded: one deleted arm, 24 indices, the accept pairs, the structural rows; ~40 equality rows per artifact, no runtime matrix, no open-ended follow-up (not the #392 shape). | :152 | :103 | Q12:58 |

## C. Findings outside T1 -- FILED as rows in T1's landing

| # | finding | seat | disposition |
|---|---|---|---|
| C1 | `xmem` address-operand overlap: the load half writes `r[d]` (`cpu_m88k_instr.c:2385`, `:2395`); the store half reuses `arg[1]`/`arg[2]` (`:2421`) and the handler recomputes the effective address from `r[s1]`/`r[s2]` (`cpu_m88k_instr_loadstore.c:248-256`), so with `d == s1` or `d == s2` the write goes to an address computed from the loaded value; the manual requires the write "to that address" (`mc88100.txt:8184-8187`).  Confirmed in source (CHECKS #7). | Astra :200-202 | NEW ROW `m88kxmemaddrovl` (MED; guest-visible wrong result; witness none, source-established).  Not T1's contract. |
| C2 | `M88K_PSR_BO` is set only at `cpu_m88k.c:182-183` right after `:130` assigns big-endian, so it stays clear when the loader/config later sets little-endian; the generic load/store path sets `DMT_BO` from `cpu->byte_order` (`cpu_m88k_instr_loadstore.c:111-112`) and `ldcr` of a DMT stops the CPU when that bit disagrees with the PSR (`cpu_m88k.c:472-477`). | Grok :132 | NEW ROW `m88klepsrbo` (MED-LOW; a little-endian m88k guest's generic-path access can stop the CPU on the DMT/PSR disagreement; witness none).  Line numbers to be re-read at HEAD before filing. |
| C3 | The ledger row's `state_note` and `OUTSTANDING_BUGS.md` still say "fix shape DISPUTED; pass 1 settles it" and "witness: none -- not yet reproduced"; `WITNESS_ATTEMPT.md` is untracked. | drafter NOTES item 4 | Corrected in T1's landing records (row state_note, witness `detector:<path>` with the BLOCKED attempt named, the witness file tracked). |
| C4 | The clause-(c)-by-instrument and D2 rules exist only in the working-tree carrier/template. | drafter NOTES item 5 | Owner's files (never committed by this session); the brief quoted the working-tree text and said so.  No action here. |

## E. ADJUDICATED by GPT-6 Astra, 2026-10-23 ~09:55 (`adj/codex_t1p1adj.txt`, 10,134 b): VERDICT AMEND -- the repair
## (A1-A6) UPHELD; the amendments below SUPERSEDE the rows they name.  Evidence basis: FOUR reviewing seats (Astra-as-
## reviewer, Grok, GLM 5.3, DeepSeek); Argon a SEAT FAILURE (`argon_t1p1.DROPPED.txt`); Fable HELD.  Neither absence
## is agreement, and the "all three agree" wording of sections A-C above is the PRE-adjudication record.

| item | ruling | amendment (quoting what it refutes) |
|---|---|---|
| B3 | AMEND (`:11`, `:36-38`) | "the kill for v6's only silent form" is WRONG: the same name printer names the generated DEFINITIONS, so that form also yields duplicate definition names (`generate_m88k_loadstore.c:118-125`); the driver does not compile the definitions, so the table-token difference at 161 is the observable, not silence.  The halfword pins stay; their warrant is R12 (adjacent modelled size), NOT rule D2 (a callee compare is outside the DEPENDS-ON walk). |
| B4 | AMEND (`:12`, `:40`) | The NULL count stays supplementary (Grok objected to it as the PRIMARY carrier, `grok_t1p1.txt:124`).  But "198 `#define LS_N` blocks as the control" must not be read as a definition-integrity check -- Astra said 198 blocks alone do NOT establish correct unique definitions and valid references (`codex_t1p1.txt:187`); it is a narrow suppression-count control, and broader definition integrity is DISCLOSED as outside the contract. |
| B5 | AMEND (`:13`) | Add an explicit RED row for unsuccessful generator EXECUTION (`codex_t1p1.txt:189`), beside the compile-failure and missing-table rows. |
| B7 | AMEND (`:15`, `:32-34`) | v1-v4 are CLAUSE (d) (R4 admits re-introduction under a different predicate and excludes only widening the original); "partial (b)" is not a disqualifier.  One measured representative plus the endianness leg is defensible -- the rules enumerate rows and cells, not one receipt per predicate axis.  L5 = Grok's v2 at `grok_t1p1.txt:76` (first difference 416) ONLY; `codex_t1p1.txt:100` names a DIFFERENT variant (first difference 256 overall).  v3/v4's "one" cell is unspecified (`codex_t1p1.txt:121`); 168/224 are the class-wide first differences. |
| B8 | AMEND (`:16`, `:28-30`) -- the principal substantive error | ALL 24 cells are the generator-output FLOOR: R7's reachability is through the fix's own repair-path data flow, and `main()` enumerates all 24 through its loops and surviving exclusions (`generate_m88k_loadstore.c:221-262`); eight cells lacking a guest consumer today does not make their generator paths unreachable.  "16 floor + 8 clause (e)" (Grok `:84-89`) substitutes the consumer domain for the producer's.  The CONTRACT states 24 floor cells and names 16 as the current guest-consumer subset; an escape at any of the 24 is a floor breach. |
| B9 | AMEND (`:17`) | Keep the callee boundary, worded "not an ADDITIONAL DEPENDS-ON axis"; the R12 accept row remains mandatory. |
| B12 | AMEND (`:20`, `:56`) | "~40 equality rows" is replaced by the enumerated count: 54 distinct name pins per artifact (24 repairs + 24 counterparts + 6 accepts; 57 if the three accept indices that are also counterparts are emitted twice), plus the structural and status rows.  Boundedness stands. |
| C1 | AMEND (`:21`, `:65`) | Keep the separate MED correctness finding; DELETE "not a stop": the recomputed address can enter generic handling and its fault paths (`cpu_m88k_instr_loadstore.c:279-290`, `:234-239`).  Record: wrong-address access with possible secondary fault behaviour; unmeasured. |
| C2 | AMEND (`:22`, `:67-69`) | Grok's chain omits a state transfer: the generic handler writes the staged `dmt[]`, `ldcr` reads `cr[]`, and DATA_ACCESS handling copies between them (`cpu_m88k_instr_loadstore.c:88-112`; `cpu_m88k.c:432`, `:908-918`) -- a successful generic access alone does not reach the `ldcr` stop.  The more direct source-established stop: exception delivery calls `m88k_stcr` with the existing PSR and its byte-order mismatch check clears `running` (`cpu_m88k.c:827-832`, `:523-532`); and "BO is set only at initialisation" is too broad -- `m88k_stcr` writes the whole PSR (`:553`).  File as CPU-STOP / MED, source-established, unmeasured, outside T1.  Citations re-verified by the main loop before filing (CHECKS #12). |
| C3 | UPHOLD as a LANDING obligation, not as evidence anything was updated. | -- |
| DeepSeek | its ordinary-immediate acceptance request (`ollama_deepseek_t1p1_Q12.txt:76`; also `codex_t1p1.txt:146`) is outside the mandatory adjacent-value set -- the defective scaled cells already follow the immediate-scaled exclusion -- and does not block the repair; DISCLOSED, not rowed. | -- |
| checks | CHECKS #4 wrong ("regardless" contradicts the dependency-driven make rule, #10); #6 is OWED to the builder, not measured; #7 overclaims "not a stop". | corrected in `CHECKS_mainloop.md`. |
| spec | BUILD_SPEC §2, §3, §6, §7, §9 amended (its section 10); §5 (the repair) unchanged. | sent to the builder 2026-10-23 ~10:00. |

## D. What the builder owes (the implementation spec, by pointer)

1. Pre-fix receipts on HEAD, dated before any edit: the generator compiled and run; fresh stdout vs committed table
   agreement at HEAD (CHECKS #6); the new detector RED at the 24 pins on HEAD (clause (a)), preserved at a durable path.
2. `PRETABLE.out` written before table 1 (mandatory: sibling parity, claim -> row, guard field vs body field with the
   body-induced partitions, channel per row -- B4/B7 give the channels).
3. The fix (A1-A5) with a `/* #NNN: */` tag at the deleted arm's position in the generator (the regenerated table
   carries no hand edits), the two files propagated.
4. The detector (B1-B12) and its gate block; the table: HEAD generator (= clause (b) at the generator site), HEAD table
   with the fixed generator (clause (b) at the table site), comment-only generator and comment-only table (clause
   (c), measured), the v2 and endianness re-introductions (B7), v6 (B3) -- every score with its artifact path.
5. Build-tree rebuilds and the two-part clearance recorded as OUTPUT; GATE 2 run once, alone, to `REGRESS`-style
   green; GATE 11 once on the rebuilt `build/gxemul` as the m88k regression check.
6. Records text names findings by id and answer-file:line only.
