# PASS-2 DIFF REVIEW -- round `#569`, ledger row `m88kscaledbyte` (GXemul hardened fork)
**Brief v1, FULL form -- for seats that can read files; every fact a question needs is inlined anyway.**  Drafted 2026-10-23 ~10:50 -0500.
Tree under review: the `GXEMUL-SEC/` WORKING TREE over HEAD `5986c137` -- the round is IN FLIGHT and UNCOMMITTED
(section 4).  Built from `GXEMUL-SEC/tools/BRIEF_TEMPLATE.md` (working tree).  The self-contained packet form is `brief2_COMPACT.md`.

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated
wrongly.  **Check the premises, not just the derivations.**  Where I state something as
fact, ask whether it is true.  A seat that re-derives a premise from something this brief
did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.**  There are THREE pristine-2021-upstream
copies of GXemul under the project root (`./src/` and two under
`_archive/audit-results-*/builds/`).  They are NOT this fork.  If your line numbers
disagree with mine by hundreds you are reading one of them — say so rather than
reconciling.

**If you cannot read files that is expected** — every fact you need is inlined.  Name any
premise you cannot settle from this packet rather than guessing at it.

**Where this brief states an ARITHMETIC claim — an index range, an offset, a count of
reachable addresses — ENUMERATE it rather than reasoning about it.**  Walk the values.
A derivation that skips one masking line reads exactly like a correct one.

**And ENUMERATE THE RIGHT DOMAIN — a domain is itself a premise.**  Ask what the PRODUCER of
these values can actually emit before you walk them.  Walking every member of a set you have
not audited is not enumeration; it is a derivation with more steps, and it reads exactly like
a correct one.

**VERDICT LINE FIRST**, so your answer survives truncation.

---

## 0. What this is, what this pass is for, and how to answer

**The project.**  GXemul is a computer-architecture emulator: a developer tool that runs legacy operating systems
inside a software sandbox.  This fork is a hardening effort -- ordinary software-correctness work on the emulator's own
C code: out-of-bounds accesses, missing checks, crash-on-unusual-input defects, and the regression tests that keep them
fixed.  The *guest* is a program or OS running INSIDE the emulator; the *host* is the emulator process on the developer's
own machine.  A *variant* or *leg* below is a deliberately altered copy of the code, used to measure whether the
regression test notices the alteration (standard mutation testing); a row that notices it goes *red* under that leg.

**This pass.**  PASS 2: a review of the ACTUAL DIFF and of the MEASUREMENTS, before anything is committed.  The fix and
its regression detector were designed on pass 1 and that design was adjudicated (section 3).  The builder implemented
both, measured a 16-run table against the detector, propagated the two source files to the four fork trees, and ran
GATE 2 and GATE 11 once each, alone (section 9).  Review effort is scoped to THIS diff; the settled design is not
re-argued unless you find one of its premises false -- then say so loudly (R21, section 10).

**Hard limits.**  READ-ONLY.  Do not build, run, copy or modify anything in the repository; do not run the generator,
the driver or any gate.  No seat is asked to design or run a guest-path reproduction (section 2 says why).

**Reading scope (seats that can read files).**  `GXEMUL-SEC/src/`, the top-level `GXEMUL-SEC/regress/*.c`, `*.sh` and
`*.py`, and THIS ROUND'S OWN directory `GXEMUL-SEC/regress/artifacts/m88kscaledbyte/` -- every artifact this brief cites
lives there, and the decisive ones are inlined below.  Do not read any other directory under `regress/artifacts/`, and
do not read `tools/pipeline/ledger.json`.  The leg-variant files (`table1_20261022/L*.diff`, `S*.diff`) need not be
opened: each leg is named here by its id, its one-line description and its score.  The MC88100 manual text lives
OUTSIDE the repository at the absolute path `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\mc88100.txt` (its one load-bearing
passage is quoted in S5).

**The working tree is NOT the round alone (section 4, part 6).**  21 tracked files differ from HEAD.  THIS ROUND'S are
`src/cpus/generate_m88k_loadstore.c`, `src/cpus/tmp_m88k_loadstore.c` and ONE hunk of `regress/gate_offline.sh` -- plus the
new, untracked `regress/diff_m88k_loadstore_gen.sh` and the untracked `regress/artifacts/m88kscaledbyte/`.  The other 18
belong to other sessions' in-flight work and are NOT under review:
`regress/diff_wdc_identify.c`, `regress/gate_sh_rounding.sh`, `regress/gdrom_default_probe.py`, `regress/sh4_chcr_probe.py`,
`regress/wdc_addtoinbuf_probe.py`, `src/cpus/cpu_alpha_palcode.c`, `src/devices/dev_lca.c`, `src/devices/dev_pcc2.c`,
`src/devices/dev_sh4.c`, `src/include/thirdparty/mvme_pcctworeg.h`, `tools/BRIEF_TEMPLATE.md`, `tools/CLAUDE.md`,
`tools/PIPELINE.md`, `tools/adjudicate.sh`, `tools/panel.sh`, `tools/pipeline/check_probe_wiring.py`,
`tools/pipeline/ledger.json` (other rows only; this round's row is unchanged), `tools/pipeline/matrix.html`.
`regress/gate_offline.sh` itself carries THREE foreign hunks (at HEAD lines ~1738, ~1832 and ~2273: 58 added lines, 3
removed); the file to commit is the staged copy `table1_20261022/staged/gate_offline.sh`, which is HEAD plus this round's
ONE hunk (section 7.3).  Every other source file this brief cites is byte-identical to HEAD.

**Answer format -- VERDICT LINE FIRST:**
~~~~
VERDICT: <SHIP | SHIP WITH CHANGES | DO NOT SHIP> -- <one sentence>
Q1: <one line>   Q2: <one line>   Q3: <one line>   Q4: <one line>   Q5: <one line>
~~~~
Then one section per question.  Mark EVERY claim READ (you opened the file or artifact), REASONED (from this packet
alone) or NOT CHECKABLE.  A change you ask for names its file and its grep anchor, and says which licence it is under:
L1 pre-ship construction, L2 floor breach, L3 undischarged obligation, L4 wrong record -- or FILE (section 10, R16).

---

## 1. The defect and the fix -- as the records describe them (VERBATIM)

Ledger row `m88kscaledbyte`, its `title` field (HEAD and working tree identical; the row is unchanged by the round so far
-- state `open`, witness `none`, commits empty, and it carries NO `entries` field: section 4, part 2):
~~~~
cpus/generate_m88k_loadstore.c table + cpu_m88k_instr.c:X(xmem_slow) -- the generator emits NULL for every scaled byte-size entry; scaled `xmem.bu rD,rS1[rS2]` calls that NULL pointer (host SIGSEGV), scaled `ld.b/ld.bu/st.b` decode to `ic->f == NULL` (CPU stop) -- HOST-STOP
~~~~

The queue, `OUTSTANDING_BUGS.md` (HEAD == working tree), lines 28-29 and 25260-25263:
~~~~
   28| > 1. `m88kscaledbyte` (HIGH, new) -- m88k scaled byte ld/st/xmem use NULL table slots; a user-mode xmem calls a NULL
   29| >    function in the host.  T1; the fix shape is disputed and pass 1 settles it.
  ...
25260| * **`m88kscaledbyte` (HIGH, open)** -- new.  cpus/generate_m88k_loadstore.c table + cpu_m88k_instr.c:X(xmem_slow) -- the
25261|   generator emits NULL for every scaled byte-size entry; scaled `xmem.bu rD,rS1[rS2]` calls that NULL pointer (host
25262|   SIGSEGV), scaled `ld.b/ld.bu/st.b` decode to `ic->f == NULL` (CPU stop) -- HOST-STOP.  TRIAGE.md T1; report rows
25263|   A7-29, A7-30, A(c)#1; port: yes (ajfa mvme187 4a01173).  Batch 1 of 10 (fix shape disputed; pass 1 settles it).
~~~~

The committed critical-items ruling (`regress/artifacts/research_20261022/crit_20261022/CRIT_RULINGS.md`, committed in
`cb2eba1e`), its T1 row, line 13:
~~~~
 13| | **T1** m88k scaled-byte `xmem` NULL slot | The first adjudication's dispute is SETTLED for Astra: repair the TABLE (alias the scaled-byte slots to the existing unscaled byte handlers in `generate_m88k_loadstore.c:254-257`), keep the generation early-return (`:104-105`, else duplicate definitions), do NOT edit the decoder -- the `op != 3` exemption is not in this tree (it is the unported ajfa recipe) and changing a decoder-local `scaled` cannot reach `xmem_slow`'s own rebuild of it. Scaled `ld.b`/`st.b` share the slots (a CPU-stop, same change). N1/N2 stay separate rounds. | Astra Q1; Grok Q1 (24 repaired table entries; floor (a)-(d); accept rows; rung-3 on unmodified `testm88k`) | READY -- round 1 |
~~~~

**Evidence level.**  The defect is established by READING the source (section 5, S3; section 8.2) and by the pre-fix
red of the offline detector (section 9.6).  It has NOT been measured on a guest path (section 2).  The queue lines and the
ledger row still say "fix shape disputed; pass 1 settles it" and "witness: none" -- the landing records owe their
correction (Q5).

---

## 2. The witness disposition -- rung-3 attempt BLOCKED; detector-only by owner ruling (VERBATIM)

`regress/artifacts/m88kscaledbyte/witness_attempt_20261022/WITNESS_ATTEMPT.md`, inlined whole.  **It is UNTRACKED at
HEAD** (section 4, part 3), and the new driver's header cites it.
~~~~
  1| # m88kscaledbyte -- the rung-3 witness ATTEMPT, 2026-10-22: BLOCKED (recorded so `none` never means "did not think to")
  2| 
  3| Round T1 of the external-fixes batch (`regress/artifacts/research_20261022/`).  The carrier's lifecycle step 2 asks for
  4| a rung-3 witness attempt before the fix; the 2026-08-27 owner ruling asks one seat to try it; the 2026-08-27 `detector:`
  5| term requires the attempt to be RECORDED.
  6| 
  7| **What was attempted.**  A measuring seat was briefed (Agent tool, Opus) to make a cold-debugger probe through real
  8| instruction decode and real `memory_rw` on the unmodified in-tree `testm88k` machine, with the liveness and
  9| device-signature controls the witness ladder requires, built from HEAD 13233723 in a scratch clone -- the probe SHAPE both
 10| design seats specified in `research_20261022/crit_20261022/codex_rescrit.txt` and `grok_crit.txt` (their Q1 sections).
 11| The brief named no instruction words or decode paths; it pointed at the row id and those two answers.
 12| 
 13| **What happened.**  The coordinator's response was stopped by the harness safety classifier while the brief was being
 14| written (the seventh such stop that day; the class is recorded in the project memory `gxemul-panel-benign-framing`).
 15| The agent launched with a truncated brief and was killed at once; it had written nothing.  Per the standing rule for
 16| that class, the brief was not re-issued in any form.
 17| 
 18| **Owner ruling (2026-10-22, by question):** "Detector-only, attempt recorded" -- ship the agreed fix with an offline
 19| regression detector under the ledger's `detector:` witness term, record this attempt as BLOCKED, and leave a guest-path
 20| witness to the owner (or a session they drive) by another route if one is wanted.  The probe shape for that later run
 21| is the one the two seat answers specify; nothing here restates it.
 22| 
 23| **Status:** rung-3 attempt BLOCKED (classifier), not "not tried".  Witness term for the round: `detector:<path>`.
~~~~
**So, for this pass:** do NOT design, sketch or run a guest-path reproduction.  The round ships under the ledger's
`detector:<path>` witness term (R18) with an OFFLINE regression detector; the guest-path channels (the exchanged byte,
neighbour preservation, zero extension) are listed in the driver's own NOT-OBSERVED paragraph (section 7.4, lines 66-74).

---

## 3. The settled design and its adjudication (VERBATIM)

The pass-1 panel answered the pass-1 brief (`pass1_20261022/packet.md`); the main loop wrote the rulings; GPT-6 Astra then
ADJUDICATED them (verdict AMEND, the repair UPHELD) and its amendments, section E, SUPERSEDE the rows they name.  The Fable
stage is HELD by the owner (`pass1_20261022/fable5.HELD.txt`), so every ruling below is provisional on its face.

### 3.1 `pass1_20261022/PASS1_RULINGS.md` -- the header, and sections A, B, C, E, D, in file order

~~~~
  1| # T1 (`m88kscaledbyte`) -- pass-1 design review: rulings (main loop, 2026-10-22; HEAD cb2eba1e at firing)
  2| 
  3| **Evidence basis: 3 of 4 rostered seats** (owner roster 2026-10-20/21: GLM 5.3 + Grok + Astra + Fable).
  4| GPT-6 Astra `ultra` (`codex_t1p1.txt`, 19,643 b, rc 0, header model verified) -- READY WITH CHANGES.
  5| Grok 4.7 xhigh plan-mode (`grok_t1p1.txt`, 21,832 b, rc 0) -- READY WITH CHANGES.
  6| GLM 5.3 cloud, packet-fed, TWO firings of one seat per the one-question-per-packet rule (`ollama_glm_t1p1_Q12.txt`
  7| 17,369 b; `ollama_glm_t1p1_Q34.txt` 9,008 b; both plain text, verdict first, finished tails) -- READY WITH CHANGES.
  8| Fable 5.1: DELIBERATELY NOT FIRED (`fable5.HELD.txt`, owner holds of 10-21/10-22; hold question carried there).
  9| NOT FIRED by owner roster: agy, kimi, deepseek, minimax, opus5.  Every seat answered; no seat failure.
 10| Provisional on its face until the Fable hold lifts; the build proceeds because all three answering seats agree on
 11| every design point and the Fable stage is HELD with its question.
 12| 
 13| Dispositions are by seat answer file : line.  The main loop's own checks are in `CHECKS_mainloop.md` (11 items).
 14| 
 15| ## A. The repair -- SETTLED, all three seats agree
 16| 
 17| | # | ruling | Astra | Grok | GLM |
 18| |---|---|---|---|---|
 19| | A1 | Remove the WHOLE arm `generate_m88k_loadstore.c:254-257` (condition, `printf("\tNULL")`, `continue`, brace).  Deleting only the `continue` emits two initializer tokens (the drafter's P5 upheld). | :46 | :45 | Q12:31 |
 20| | A2 | Keep `:104-105` (the generation early return): without it `loadstore()` emits duplicate `LS_N`/`LS_GENERIC_N` definitions under the unscaled byte names; the generated-definition count stays 198. | :46, :57 | :41 | Q12:29 |
 21| | A3 | The decoder is NOT edited (S4/S5; the ajfa `op != 3` recipe is not in this tree and cannot reach `xmem_slow`'s own `scaled`). | :85 | :59 | Q12:37 |
 22| | A4 | All 24 slots alias to the 12 unscaled byte handler names (the counterpart at index-32); the 8 slots with no producer today are aliased too -- a partial repair would ADD a predicate, which is the clause-(d) shape. | :11-44 | :10-39 | Q12:10-27 |
 23| | A5 | The committed generated table `src/cpus/tmp_m88k_loadstore.c` is REGENERATED IN THE SAME COMMIT (24 lines `NULL` -> name; 296 -> 272 NULLs; 512 entries).  Both files land byte-identical in `est/` (precommit section A; neither is on `tools/est_divergence.txt`) and are propagated to the three build trees with the two-part clearance.  `Makefile.skel:134-135` is dependency-driven, so both artifacts are live fixed sites. | :59-61 | :47 | Q12:33 |
 24| | A6 | P1 ("`cpu_m88k.c:130` forces big-endian") is FALSE: the loader (`emul.c:651-652`, `file_elf.c:693-694`) and a config `byte_order` (`emul.c:737-738`) set little-endian later; 16 of the 24 cells have a producer today (12 sync both endians + 4 nosync plain), 4 gain one after N2, 4 have none.  P2/P3 confirmed. | :63-74 | :51-55 | Q12:35 |
 25| 
 26| ## B. The detector -- SETTLED on shape and pins
 27| 
 28| | # | ruling | Astra | Grok | GLM |
 29| |---|---|---|---|---|
 30| | B1 | TWO LEGS, both required by clause (b)'s "every fixed site": (i) compile and run the REAL generator (it has its own `main`; no `#include` harness) and pin its stdout; (ii) read the COMMITTED table with a reader parametrized by file and array size (`[512]`; the `#375` `ls_entry` hard-codes `[32]` and `$MIPSLS` -- CHECKS #2); plus (iii) full fresh-vs-committed equality.  Either leg alone is green under the other site's reversion (both seats' revert matrices). | :168-180 | :120-122 | Q34:7-17 |
 31| | B2 | Primary pins: ABSOLUTE handler names BY EQUALITY at all 24 indices (both endian halves; the expected names come from the design, never from the committed file), in BOTH artifacts.  The relative `slot[i] == slot[i-32]` row is NOT a pin (anchor rule R11): it holds under a joint rename and under `NULL == NULL`. | :150 | :101 | Q12:56 |
 32| | B3 | Accept pins by equality: scaled HALFWORD 161 (`m88k_instr_ld_u_2_le_scaled_regofs`) and 177 (`..._2_be_scaled_regofs`) -- rule D2's B+1 edge of `:80`'s `size > 0`, and the kill for v6's only silent form (`size > 0` -> `size > 1`, first difference 161, which a word-only row cannot see); scaled WORD xmem 434/438 (BE) and 418/422 (LE); unscaled byte 144, 400, 404; the 24 counterparts as supplementary. | :146-148 | :91-99 | Q12:54 |
 33| | B4 | Structural rows: exactly one 512-entry initializer per artifact; NULL count == 272 by equality as a SUPPLEMENTARY row (Grok :124: not the floor carrier -- a moved NULL keeps the count; the absolute pins are the carriers); generator stderr `generated_functions = 198` and 198 `#define LS_N` blocks as the control on the kept early return (deleting `:104-105` keeps every name pin green and shows up only there and at link time). | :152-162, :187 | :114-116 | Q34:23-26 |
 34| | B5 | A missing or non-compiling product is an EXPLICIT RED `check` row, never `need_file` (which `gate_skip`s, `lib.sh:147-151`) and never `check_min`. | :192 | :124 | Q34:26 |
 35| | B6 | Clause (c) medium, by instrument kind (offline): a COMMENT-ONLY generator source -> the compile row reds; a COMMENT-ONLY committed table -> every reader row reds.  The identity `xmem` body (the crit packet's framing) is the medium of a runtime handler instrument and does not apply.  Record form: both legs are RUN ONCE by the builder and recorded `(c): measured at <artifact>`, the stronger of the two permitted forms. | :102-108, :194 | :69, :126 | Q12:47, Q34:30 |
 36| | B7 | Clause (d): the repair adds no predicate (pure deletion), so the (d) form is the arm re-introduced under a DIFFERENT predicate -- the seats' v1-v4 (first differences 160 / 416 / 168 / 224), all killed by the absolute pins.  Astra files v1-v4 as "partial (b)", Grok and GLM as (d): a classification difference with NO row consequence (same pins kill them); recorded, not settled by vote.  The table builds ONE representative (v2, Grok :76 / Astra :100 -- the `no_pc_sync` predicate, first difference 416) plus the endianness narrowing GLM Q12:52 names (one half left `NULL`), since that is the shape a BE-only pin set would miss. | :98-100, :110-123 | :71-79 | Q12:48-50 |
 37| | B8 | Floor enumeration: Astra :138-144 and GLM Q12:52 -- all 24 cells are the OUTPUT CONTRACT; Grok :84-89 -- the FLOOR (R7, producible cells) is 16, the 8 no-producer cells clause (e) "pinned in the same equality list".  All three pin all 24, so no row differs.  CONTRACT HEADER states Grok's split: an escape at one of the 16 is a floor breach, at one of the 8 is coverage debt. | :138-144 | :84-89 | Q12:52 |
 38| | B9 | DEPENDS-ON bound: the edited lines are in `main()`; `print_function_name`'s `:74`/`:80` tests are callee compares -- clause (e), not floor (R5).  The halfword pin is still OWED as the accept side of the deleted predicate (B3), not as a floor cell. | :141, :148 | :82, :99 | Q12:52-54 |
 39| | B10 | Home: GATE 2 (`regress/gate_offline.sh`), a new driver `regress/diff_m88k_loadstore_gen.sh` on the committed `diff_autodev_gen.sh` pattern (#406: derive the expectation from the generator's INPUTS, never from the committed output; scratch copy, never run the generator in-tree), wired in a block placed away from the foreign uncommitted hunks (CHECKS #11).  Presence pins name each floor row (deleting one is a red row). | :170 | :124 | Q34:17 |
 40| | B11 | No floor cell is observable only on a guest path; the exchanged-byte / neighbour-preservation / zero-extension channels are the BLOCKED rung-3 witness's and stay with the owner's record (`WITNESS_ATTEMPT.md`); the contract header says so instead of claiming them. | :196 | :128 | Q34:34 |
 41| | B12 | Bounded: one deleted arm, 24 indices, the accept pairs, the structural rows; ~40 equality rows per artifact, no runtime matrix, no open-ended follow-up (not the #392 shape). | :152 | :103 | Q12:58 |
 42| 
 43| ## C. Findings outside T1 -- FILED as rows in T1's landing
 44| 
 45| | # | finding | seat | disposition |
 46| |---|---|---|---|
 47| | C1 | `xmem` address-operand overlap: the load half writes `r[d]` (`cpu_m88k_instr.c:2385`, `:2395`); the store half reuses `arg[1]`/`arg[2]` (`:2421`) and the handler recomputes the effective address from `r[s1]`/`r[s2]` (`cpu_m88k_instr_loadstore.c:248-256`), so with `d == s1` or `d == s2` the write goes to an address computed from the loaded value; the manual requires the write "to that address" (`mc88100.txt:8184-8187`).  Confirmed in source (CHECKS #7). | Astra :200-202 | NEW ROW `m88kxmemaddrovl` (MED; guest-visible wrong result; witness none, source-established).  Not T1's contract. |
 48| | C2 | `M88K_PSR_BO` is set only at `cpu_m88k.c:182-183` right after `:130` assigns big-endian, so it stays clear when the loader/config later sets little-endian; the generic load/store path sets `DMT_BO` from `cpu->byte_order` (`cpu_m88k_instr_loadstore.c:111-112`) and `ldcr` of a DMT stops the CPU when that bit disagrees with the PSR (`cpu_m88k.c:472-477`). | Grok :132 | NEW ROW `m88klepsrbo` (MED-LOW; a little-endian m88k guest's generic-path access can stop the CPU on the DMT/PSR disagreement; witness none).  Line numbers to be re-read at HEAD before filing. |
 49| | C3 | The ledger row's `state_note` and `OUTSTANDING_BUGS.md` still say "fix shape DISPUTED; pass 1 settles it" and "witness: none -- not yet reproduced"; `WITNESS_ATTEMPT.md` is untracked. | drafter NOTES item 4 | Corrected in T1's landing records (row state_note, witness `detector:<path>` with the BLOCKED attempt named, the witness file tracked). |
 50| | C4 | The clause-(c)-by-instrument and D2 rules exist only in the working-tree carrier/template. | drafter NOTES item 5 | Owner's files (never committed by this session); the brief quoted the working-tree text and said so.  No action here. |
 51| 
 52| ## E. ADJUDICATED by GPT-6 Astra, 2026-10-23 ~09:55 (`adj/codex_t1p1adj.txt`, 10,134 b): VERDICT AMEND -- the repair
 53| ## (A1-A6) UPHELD; the amendments below SUPERSEDE the rows they name.  Evidence basis: FOUR reviewing seats (Astra-as-
 54| ## reviewer, Grok, GLM 5.3, DeepSeek); Argon a SEAT FAILURE (`argon_t1p1.DROPPED.txt`); Fable HELD.  Neither absence
 55| ## is agreement, and the "all three agree" wording of sections A-C above is the PRE-adjudication record.
 56| 
 57| | item | ruling | amendment (quoting what it refutes) |
 58| |---|---|---|
 59| | B3 | AMEND (`:11`, `:36-38`) | "the kill for v6's only silent form" is WRONG: the same name printer names the generated DEFINITIONS, so that form also yields duplicate definition names (`generate_m88k_loadstore.c:118-125`); the driver does not compile the definitions, so the table-token difference at 161 is the observable, not silence.  The halfword pins stay; their warrant is R12 (adjacent modelled size), NOT rule D2 (a callee compare is outside the DEPENDS-ON walk). |
 60| | B4 | AMEND (`:12`, `:40`) | The NULL count stays supplementary (Grok objected to it as the PRIMARY carrier, `grok_t1p1.txt:124`).  But "198 `#define LS_N` blocks as the control" must not be read as a definition-integrity check -- Astra said 198 blocks alone do NOT establish correct unique definitions and valid references (`codex_t1p1.txt:187`); it is a narrow suppression-count control, and broader definition integrity is DISCLOSED as outside the contract. |
 61| | B5 | AMEND (`:13`) | Add an explicit RED row for unsuccessful generator EXECUTION (`codex_t1p1.txt:189`), beside the compile-failure and missing-table rows. |
 62| | B7 | AMEND (`:15`, `:32-34`) | v1-v4 are CLAUSE (d) (R4 admits re-introduction under a different predicate and excludes only widening the original); "partial (b)" is not a disqualifier.  One measured representative plus the endianness leg is defensible -- the rules enumerate rows and cells, not one receipt per predicate axis.  L5 = Grok's v2 at `grok_t1p1.txt:76` (first difference 416) ONLY; `codex_t1p1.txt:100` names a DIFFERENT variant (first difference 256 overall).  v3/v4's "one" cell is unspecified (`codex_t1p1.txt:121`); 168/224 are the class-wide first differences. |
 63| | B8 | AMEND (`:16`, `:28-30`) -- the principal substantive error | ALL 24 cells are the generator-output FLOOR: R7's reachability is through the fix's own repair-path data flow, and `main()` enumerates all 24 through its loops and surviving exclusions (`generate_m88k_loadstore.c:221-262`); eight cells lacking a guest consumer today does not make their generator paths unreachable.  "16 floor + 8 clause (e)" (Grok `:84-89`) substitutes the consumer domain for the producer's.  The CONTRACT states 24 floor cells and names 16 as the current guest-consumer subset; an escape at any of the 24 is a floor breach. |
 64| | B9 | AMEND (`:17`) | Keep the callee boundary, worded "not an ADDITIONAL DEPENDS-ON axis"; the R12 accept row remains mandatory. |
 65| | B12 | AMEND (`:20`, `:56`) | "~40 equality rows" is replaced by the enumerated count: 54 distinct name pins per artifact (24 repairs + 24 counterparts + 6 accepts; 57 if the three accept indices that are also counterparts are emitted twice), plus the structural and status rows.  Boundedness stands. |
 66| | C1 | AMEND (`:21`, `:65`) | Keep the separate MED correctness finding; DELETE "not a stop": the recomputed address can enter generic handling and its fault paths (`cpu_m88k_instr_loadstore.c:279-290`, `:234-239`).  Record: wrong-address access with possible secondary fault behaviour; unmeasured. |
 67| | C2 | AMEND (`:22`, `:67-69`) | Grok's chain omits a state transfer: the generic handler writes the staged `dmt[]`, `ldcr` reads `cr[]`, and DATA_ACCESS handling copies between them (`cpu_m88k_instr_loadstore.c:88-112`; `cpu_m88k.c:432`, `:908-918`) -- a successful generic access alone does not reach the `ldcr` stop.  The more direct source-established stop: exception delivery calls `m88k_stcr` with the existing PSR and its byte-order mismatch check clears `running` (`cpu_m88k.c:827-832`, `:523-532`); and "BO is set only at initialisation" is too broad -- `m88k_stcr` writes the whole PSR (`:553`).  File as CPU-STOP / MED, source-established, unmeasured, outside T1.  Citations re-verified by the main loop before filing (CHECKS #12). |
 68| | C3 | UPHOLD as a LANDING obligation, not as evidence anything was updated. | -- |
 69| | DeepSeek | its ordinary-immediate acceptance request (`ollama_deepseek_t1p1_Q12.txt:76`; also `codex_t1p1.txt:146`) is outside the mandatory adjacent-value set -- the defective scaled cells already follow the immediate-scaled exclusion -- and does not block the repair; DISCLOSED, not rowed. | -- |
 70| | checks | CHECKS #4 wrong ("regardless" contradicts the dependency-driven make rule, #10); #6 is OWED to the builder, not measured; #7 overclaims "not a stop". | corrected in `CHECKS_mainloop.md`. |
 71| | spec | BUILD_SPEC §2, §3, §6, §7, §9 amended (its section 10); §5 (the repair) unchanged. | sent to the builder 2026-10-23 ~10:00. |
 72| 
 73| ## D. What the builder owes (the implementation spec, by pointer)
 74| 
 75| 1. Pre-fix receipts on HEAD, dated before any edit: the generator compiled and run; fresh stdout vs committed table
 76|    agreement at HEAD (CHECKS #6); the new detector RED at the 24 pins on HEAD (clause (a)), preserved at a durable path.
 77| 2. `PRETABLE.out` written before table 1 (mandatory: sibling parity, claim -> row, guard field vs body field with the
 78|    body-induced partitions, channel per row -- B4/B7 give the channels).
 79| 3. The fix (A1-A5) with a `/* #NNN: */` tag at the deleted arm's position in the generator (the regenerated table
 80|    carries no hand edits), the two files propagated.
 81| 4. The detector (B1-B12) and its gate block; the table: HEAD generator (= clause (b) at the generator site), HEAD table
 82|    with the fixed generator (clause (b) at the table site), comment-only generator and comment-only table (clause
 83|    (c), measured), the v2 and endianness re-introductions (B7), v6 (B3) -- every score with its artifact path.
 84| 5. Build-tree rebuilds and the two-part clearance recorded as OUTPUT; GATE 2 run once, alone, to `REGRESS`-style
 85|    green; GATE 11 once on the rebuilt `build/gxemul` as the m88k regression check.
 86| 6. Records text names findings by id and answer-file:line only.
~~~~

*Lines 3-11 are the PRE-adjudication roster.  Section E's heading says "the 'all three agree' wording of sections A-C
above is the PRE-adjudication record", but lines 3-11 themselves were not corrected in place -- a records item, Q5a.*

### 3.2 GPT-6 Astra's adjudication, `pass1_20261022/adj/codex_t1p1adj.txt` -- the verdict, the item rulings, and the whole Q3 section
~~~~
  1| VERDICT: AMEND -- On the evidence of four reviewing seats (Astra-as-reviewer, Grok, GLM and DeepSeek), uphold the repair but correct the floor classification, acceptance rationale, variant specification and ancillary findings.
  2| 
  3| A1 UPHOLD.  
  4| A2 UPHOLD.  
  5| A3 UPHOLD.  
  6| A4 UPHOLD.  
  7| A5 UPHOLD: `est/` synchronization is a commit-time propagation obligation, not another tracked repair site.  
  8| A6 UPHOLD.  
  9| B1 UPHOLD.  
 10| B2 UPHOLD.  
 11| B3 AMEND: retain the pins; ground halfword acceptance in R12, not D2; remove “only silent form.”  
 12| B4 AMEND: retain the supplementary counts, but explicitly distinguish them from Astra’s requested definition-integrity checks.  
 13| B5 AMEND: require an explicit failure for unsuccessful generator execution, as well as missing inputs and compilation failure.  
 14| B6 UPHOLD: comment-only media are valid; “measured” requires actual durable receipts.  
 15| B7 AMEND: classify the specified predicate narrowings as clause (d), resolve the conflicting L5 references, and qualify underspecified first-difference claims.  
 16| B8 AMEND: all 24 cells belong to the generator-output floor; 16 is the current guest-consumer subset.  
 17| B9 AMEND: retain the callee boundary, but say “not an additional DEPENDS-ON axis”; the R12 accept row remains mandatory.  
 18| B10 UPHOLD: implement the promised individual row-identity pins.  
 19| B11 UPHOLD.  
 20| B12 AMEND: replace “~40” with the actual enumerated count; boundedness stands.  
 21| C1 AMEND: retain the separate MED correctness finding, but remove the unsupported exclusion of secondary faults or stops.  
 22| C2 AMEND: correct the causal chain and file as source-established, unmeasured CPU-STOP/MED, outside T1.  
 23| C3 UPHOLD as a landing obligation, not evidence of completed updates.  
 24| C4 UPHOLD.
  ...
 52| Q3. Changes to **BUILD_SPEC.md**, by section:
 53| 
 54| - **§2:** make `PRETABLE.out` distinguish the 24 generator-output cells from the 16 current guest-consumer cells; use R12 for the halfword acceptance warrant.
 55| - **§3:** correct the contract header’s floor split; explicitly check generator execution success; implement B10’s independently specified row identities, each occurring exactly once. A total and sentinel alone do not establish those identities (`BUILD_SPEC.md:66-76`). State the limited definition-count coverage.
 56| - **§3, with corresponding score denominators in §6:** enumerate the actual row total. The current lists contain **54 distinct name pins per artifact**, or 57 checks if the three overlapping accept/counterpart indices are emitted twice, before structural and status checks. That is 24 repairs + 24 counterparts + six additional accepts (`BUILD_SPEC.md:60-64`).
 57| - **§6:** resolve L5 to `grok_t1p1.txt:76`; correct L7’s characterization without removing its halfword pins. The frozen specification ends at L7, despite the adjudication packet saying an extra L8 was requested. Add that promised all-NULL table leg as supplementary evidence, with its receipt, rather than treating it as a prerequisite for B6.
 58| - **§7:** qualify regeneration as dependency-driven; preserve explicit propagation and byte comparisons (`BUILD_SPEC.md:111`).
 59| - **§9:** report the corrected classifications, actual receipts and C1/C2 dispositions.
 60| 
 61| **§5’s repair does not change.** The baseline agreement prerequisite in §2 and the pre-fix red requirement in §4 remain.
~~~~

### 3.3 `pass1_20261022/BUILD_SPEC.md` -- section 10, the amendments from that adjudication (they override the sections they name)
~~~~
120| ## 10. AMENDMENTS from GPT-6 Astra's adjudication of pass 1 (2026-10-23 ~09:55, `adj/codex_t1p1adj.txt` Q3) -- these
121| ## override the sections they name; §5 (the repair) is unchanged.  Sent to the builder by message at ~10:00.
122| * §2: `PRETABLE.out` distinguishes the 24 generator-output cells (the FLOOR) from the 16 current guest-consumer cells;
123|   the halfword acceptance's warrant is R12 (adjacent modelled size), not D2.
124| * §3: the contract header states the floor as ALL 24 cells (16 = the current consumer subset; the 8 others are NOT
125|   coverage debt); an explicit RED row for unsuccessful generator EXECUTION (non-zero exit / empty stdout) beside the
126|   compile and missing-table rows; every row carries an identity string that occurs exactly once and the gate block pins
127|   each identity's presence (`== 1`) as well as the total and the sentinel; the row total is ENUMERATED in the driver
128|   header and in `SCORES.txt` (54 distinct name pins per artifact = 24 + 24 + 6, or 57 if the three overlapping accept /
129|   counterpart indices are emitted twice -- say which); the `#define LS_N == 198` and `generated_functions == 198` rows
130|   are described as a narrow suppression-count control, NOT a definition-integrity check (which is disclosed as outside
131|   the contract).
132| * §6: L5 is Grok's v2 at `grok_t1p1.txt:76` only (first difference 416; the `codex_t1p1.txt:100` variant first differs
133|   at 256 overall and is NOT L5); L7 keeps the halfword pins but is recorded as also producing duplicate definition NAMES
134|   that the driver does not compile -- the table token at 161 is its observable, not "silence"; L8 (all-NULL table) is
135|   SUPPLEMENTARY evidence with its own receipt, not a prerequisite of clause (c).
136| * §7: regeneration is dependency-driven -- after each rebuild `cmp` the tree's table against GXEMUL-SEC's and record
137|   whether the tree regenerated or kept the copied file.
138| * §9: the report carries the corrected classifications, every receipt by file, the actual row count, and C1/C2 as
139|   "filed outside T1" only.
~~~~

### 3.4 `pass1_20261022/CHECKS_mainloop.md` -- the main loop's checks, with its post-adjudication corrections
~~~~
  1| # T1 pass 1 -- the main loop's CHECKS of the seats' "not checkable" items (2026-10-22, HEAD cb2eba1e)
  2| 
  3| Anything checkable in under two minutes gets CHECKED, not judged.  Each item names the seat finding it settles
  4| (answer file : line) and the command or lines read.  Source line numbers are HEAD's.
  5| 
  6| | # | seat item | checked how | result |
  7| |---|---|---|---|
  8| | 1 | GLM Q34:38 -- "the packet never shows how the fast handler obtains `p`" | `src/cpus/cpu_m88k_instr_loadstore.c:246-291` read | `p = cpu->cd.m88k.host_load[addr >> 12]` (`:266`; `host_store` `:268`; the `_usr` tables `:260/:262`), from the CPU's own page pointers, never from the call's args; a NULL page, a `.usr` in user mode, or (sizes > 1) a misaligned address falls to `LS_GENERIC_N` (`:279-291`).  The aliased byte handlers therefore take the same path word `xmem` already takes today (word slots are non-NULL).  Design premise CONFIRMED. |
  9| | 2 | GLM Q34:39 -- "the `#375` awk matches `arr\[32\]`; the m88k table is `[512]`" | `regress/gate_offline.sh:52-59` read; `src/cpus/tmp_m88k_loadstore.c:3738` | CONFIRMED: `ls_entry` matches `("\\*" arr "\\[32\\]")` and reads `$MIPSLS` only.  The m88k table is `void (*m88k_loadstore[512])(struct cpu *, struct m88k_instr_call *) = {` at `:3738`.  A reader for this round must take the file and the array size as parameters (or match `\[512\]`); copying `ls_entry` verbatim reads nothing and reports every pin as empty -- the pattern-that-selected-nothing class. |
 10| | 3 | GLM Q12:35 -- S10 "exactly four sites index the table" NOT CHECKABLE | `grep -n 'm88k_loadstore\[' src/cpus/*.c` (generated file excluded) | Exactly four: `cpu_m88k_instr.c:2377` (xmem load), `:2411` (xmem store), `:3087` (immediate-form ld/st), `:3622` (register-form ld/st); plus the generator's own `printf` of the declaration at `generate_m88k_loadstore.c:219`.  CONFIRMED. |
 11| | 4 | GLM Q12:33 / Q34:17 -- are `est/` and the build trees' copies of the generated table tracked / gate-enforced? | `tools/est_divergence.txt` (six paths, none under `src/cpus/`); `precommit_check.sh` section A `cmp` idiom | `est/` is the untracked twin: shared files must land byte-identical (section A), so the regenerated table is PROPAGATED to `est/` (and to `build/`, `build-asan/`, WSL `/tmp/gxsec-build`, with the two-part clearance) by the round -- an est copy is not a second "fixed site" in git, it is a propagation obligation.  The build trees regenerate the table at build time regardless (`Makefile.skel:134-135`). |
 12| | 5 | GLM Q12:1 / Q34:23 -- the NULL count to pin | `grep -c NULL src/cpus/tmp_m88k_loadstore.c` at HEAD | 296 at HEAD (24 arm-D + 272 arms A/B/C per the drafter's census, packet section 7); post-fix pin = 272 BY EQUALITY. |
 13| | 6 | GLM Q34:41 -- "whether the committed tmp is byte-identical to generator stdout at HEAD" | not run here (needs a compile) | OWED to the builder as the agreement row's first run on the UNMODIFIED generator, before the fix (it is the pre-fix leg of that row and part of clause (a)'s receipt). |
 14| 
 15| | 7 | Astra Q4 (`codex_t1p1.txt:200-202`) -- a SEPARATE `xmem` address-operand defect | `src/cpus/cpu_m88k_instr.c:2384-2426` read; `_scratchpad/mc88100.txt:8184-8187` | CONFIRMED in source: the load half writes `r[d]` through `call.arg[0] = &r[d]` (`:2385`, `:2395`); the store half reuses `arg[1]`/`arg[2]` -- pointers to `r[s1]`/`r[s2]` (`:2421`, "already set up from xmem_load call") -- and the handler recomputes the effective address from them (`cpu_m88k_instr_loadstore.c:248-256`).  When `d == s1` or `d == s2` the write's address is computed from the just-loaded value, while the manual says the data unit performs "a read transaction from the specified address, immediately followed by a write transaction to that address" (`:8184-8187`).  Not T1's defect and not covered by T1's detector: FILED as a new row in T1's landing (guest-visible wrong result, not a stop; witness none, source-established).  Astra's own disposition: "should not expand T1's regression contract." |
 16| | 8 | Astra Q3(a) (`:170`) -- the closer in-tree exemplar `diff_autodev_gen.sh` + GATE 2 wiring | `git ls-files`; `git show HEAD:regress/gate_offline.sh` | Both TRACKED and in HEAD: `regress/diff_autodev_gen.sh` (#406: compiles nothing, derives the expected table from the generator's INPUTS, never from the committed output -- "a tracked generated file is not evidence about its own generator") and the `#406` block at HEAD `gate_offline.sh:1886` (WT `:1938`).  This is the pattern for T1's driver: scratch copy, run the real generator, compare to an INDEPENDENT expectation (the 24 names from the design), then read the committed table separately. |
 17| | 9 | Astra Q3(b) (`:192`) -- `need_file` SKIPs rather than fails | `regress/lib.sh:147-151` | CONFIRMED: `need_file` calls `gate_skip` on a missing input.  T1's block must red explicitly on a missing generator or table (a `check` row), never rely on `need_file`, or a deleted product reads as SKIP -- silent coverage loss. |
 18| | 10 | Astra Q1(d) (`:61`) -- "the make rule is dependency-driven; not every `make` regenerates" | `src/cpus/Makefile.skel:134-135` | CONFIRMED: `tmp_m88k_loadstore.c: cpu_m88k_instr_loadstore.c generate_m88k_loadstore` -- regenerated only when the template or the generator binary is newer.  A build whose committed table is newer than the generator compiles the COMMITTED copy; one that rebuilds the generator compiles fresh output.  So both artifacts are genuinely live "fixed sites" (clause (b) needs both legs), which is what GLM Q34:9-17 and Astra Q3(a) both concluded. |
 19| | 11 | gate wiring home | `git show HEAD:regress/gate_offline.sh \| diff - regress/gate_offline.sh` | `gate_offline.sh` carries UNCOMMITTED hunks at WT `:1741`, `:1834-1886`, `:2276`, `:2280` that are not this session's -- a T1 block in GATE 2 is inserted away from them (after the `#375` block, HEAD `:72`) and committed as HEAD + that hunk only, with the working tree keeping the foreign hunks.  `regress/gate_m88k_rounding.sh` (GATE 11) is clean (WT == HEAD) but is the runtime m88k probe gate; the offline detector belongs in GATE 2. |
 20| 
 21| | 12 | Astra adjudication (`adj/codex_t1p1adj.txt:67-69`) -- the C2 chain's new citations | `cpu_m88k.c:432`, `:523-532`, `:553`, `:827-832`, `:908-918`; `cpu_m88k_instr_loadstore.c:88-112`, `:234-239` read at HEAD | recorded in the Bash transcript of 2026-10-23 ~10:00; the C2 row is filed with these lines. |
 22| 
 23| **Corrections after the adjudication (2026-10-23, `adj/codex_t1p1adj.txt:44-50`), quoting what they refute:**
 24| * #4 said "The build trees regenerate the table at build time regardless" -- WRONG: the make rule is dependency-driven
 25|   (#10); a tree regenerates only when the generator binary or the template is newer.  The two-fixed-site conclusion
 26|   is unaffected.
 27| * #6 is an OWED measurement (the builder's baseline agreement run), not a check made here.
 28| * #7 said "guest-visible wrong result, not a stop" -- the "not a stop" half is UNSUPPORTED: the recomputed address can
 29|   enter the generic handler and its fault paths (`cpu_m88k_instr_loadstore.c:279-290`, `:234-239`).  The C1 row says
 30|   "wrong-address access with possible secondary fault behaviour; unmeasured".
 31| * The closing text that stood here ("those wait for the Astra and Grok answers") was stale once the seats answered;
 32|   the rulings are in `PASS1_RULINGS.md` sections A-C and the adjudication's amendments in its section E.
~~~~

---

## 4. Section C0 -- has this round already shipped?  PASS-2 form: it is IN FLIGHT (commands and output VERBATIM)

This brief's own `C0_OUTPUT.txt`, inlined.  Git object reads only -- no `git status`, no `git diff`, no index access.
~~~~
# §C0 -- HAS THIS ROUND ALREADY SHIPPED?  PASS-2 form: run 2026-10-23 10:42:20 -0500 against HEAD 5986c137d783b0d7b0104dbc6b652dfab781b7a7 (5986c137)
# repo: C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC   (git object reads only: log / show / ls-files / ls-tree; no status, no diff, no index writes)
# For a pass-2 brief this records that the round is IN FLIGHT: implemented and measured in the working tree, NOT committed.

## 1. git log -1 -- <each file the round touches>
$ git log -1 --format='%h %ad %s' --date=iso HEAD -- src/cpus/generate_m88k_loadstore.c
39748e3c 2026-06-28 23:25:42 -0500 Import GXemul 0.7.0 (unmodified upstream baseline)
$ git log -1 --format='%h %ad %s' --date=iso HEAD -- src/cpus/tmp_m88k_loadstore.c
39748e3c 2026-06-28 23:25:42 -0500 Import GXemul 0.7.0 (unmodified upstream baseline)
$ git log -1 --format='%h %ad %s' --date=iso HEAD -- regress/gate_offline.sh
1329d894 2026-10-02 18:09:15 -0500 #556 hrecord: 154 record corrections placed as 155 notes in the regression harness's comments and docstrings, 65 files; 27 not made, filed as hrecordowed; no test behaviour changes
$ git log -1 --format='%h %ad %s' --date=iso HEAD -- regress/diff_m88k_loadstore_gen.sh
(no output -- no commit has ever touched this path: NEW / UNTRACKED)
$ git log -1 --format='%h %ad %s' --date=iso HEAD -- regress/artifacts/m88kscaledbyte/witness_attempt_20261022/WITNESS_ATTEMPT.md
(no output -- no commit has ever touched this path: NEW / UNTRACKED)

$ git log --oneline -8     (2ca79b90 is HEAD's newest ROUND: #568, landed 'held for Fable')
5986c137 regress: gate_ab.sh header -- the pristine ref's label corrected (39748e3 is not byte-identical to the 0.7.0 release); PRISTINE_REF kept
cb2eba1e records: follow-up to 13233723 -- the critical-items design adjudication preserved; a duplicate-ledger-id harness gap and a dead MIPS page-mask case filed
13233723 records: the external-fixes research filed -- 126 rows from GitHub forks, distro patches and upstream SVN r6522-r6577
de8c7547 records: the OpenFirmware exit family scoped by Argon -- a title corrected, the scoping in three rows, one row filed
7f48ea10 records: two PowerPC shift rows filed with rung-3 witnesses -- slw/srw/sraw shift amounts 32..63 wrap, srd/srad/sradi undecoded
c03949e0 records: vmedefaultkill names its landing commit 2ca79b90 in its commits field; 2ca79b90's pass-2 receipt
2ca79b90 #568 (vmedefaultkill): dev_vme.c's default: no longer ends the emulator -- the 26 header-named registers decline with one announce each, every other offset faults to the guest; a 38-row detector in gate 14; held for Fable
86114a90 records: three late Argon readings adjudicated -- #565's and #566's probe records and the fable-hold records corrected, an assess hold restored, two rows filed

## 2. grep <row id> CHANGELOG.md   (HEAD copy and working-tree copy)
$ git show HEAD:CHANGELOG.md | grep -n -E "m88kscaledbyte|#569"
(exit status 1 -- no match)
$ grep -n -E "m88kscaledbyte|#569" CHANGELOG.md        # working tree (byte-identical to HEAD: md5 4ef01caa)
(exit status 1 -- no match)
$ git show HEAD:CHANGELOG.md | grep -n -m1 -E "^# .#568."      # the newest round block at HEAD
77:# `#568` (vmedefaultkill): the MVME187's VME2 controller model ended the emulator on any offset its switch did not name -- the 26 header-
$ grep -n -E "m88kscaledbyte|m88kxmemaddrovl|m88klepsrbo" OUTSTANDING_BUGS.md     # working tree == HEAD
28:> 1. `m88kscaledbyte` (HIGH, new) -- m88k scaled byte ld/st/xmem use NULL table slots; a user-mode xmem calls a NULL
25260:* **`m88kscaledbyte` (HIGH, open)** -- new.  cpus/generate_m88k_loadstore.c table + cpu_m88k_instr.c:X(xmem_slow) -- the
$ (ledger row, read-only parse of HEAD's and the working tree's tools/pipeline/ledger.json)
== HEAD rows: 1069
   m88kscaledbyte : state=open sev=HIGH witness='none' commits=''
     keys: ['commits', 'id', 'opened', 'sev', 'state', 'state_note', 'title', 'witness']
   m88kxmemaddrovl : ABSENT
   m88klepsrbo : ABSENT
   m88kxmemusr : state=open sev=MED witness='none' commits=''
   m88kxmemr0 : state=open sev=MED witness='none' commits=''
== WT rows: 1069
   m88kscaledbyte : state=open sev=HIGH witness='none' commits=''
     keys: ['commits', 'id', 'opened', 'sev', 'state', 'state_note', 'title', 'witness']
   m88kxmemaddrovl : ABSENT
   m88klepsrbo : ABSENT
   m88kxmemusr : state=open sev=MED witness='none' commits=''
   m88kxmemr0 : state=open sev=MED witness='none' commits=''

## 3. ls <the directory any NEW TOOL lives in>
$ ls -la regress/diff_*.sh ; git ls-files -s "regress/diff_*.sh"
-rwxr-xr-x 1 User00 197121 10201 2026-08-14 03:14 regress/diff_autodev_gen.sh
-rwxr-xr-x 1 User00 197121 14528 2026-10-23 09:59 regress/diff_m88k_loadstore_gen.sh
100755 525ab12d0b1dc9354a47cad07b3cd862cb986c0b 0	regress/diff_autodev_gen.sh
$ git ls-files regress tools | grep -v "^regress/artifacts/" | grep -iE "loadstore|xmem|scaled"
(exit status 1 -- no tracked tool for this class; the new driver is UNTRACKED)
$ git ls-files regress/artifacts/m88kscaledbyte/ | wc -l
0
(0 -- the round's whole artifacts directory, including witness_attempt_20261022/WITNESS_ATTEMPT.md, is UNTRACKED)

## 4. modes and identities of the round's files
$ git ls-tree HEAD regress/gate_offline.sh src/cpus/generate_m88k_loadstore.c src/cpus/tmp_m88k_loadstore.c
100644 blob f84ef64e9c4c8dcb5536313b0cc466fad1c5904b	regress/gate_offline.sh
100644 blob ee302ce80a323c474e40a3da8aa4facdd318059b	src/cpus/generate_m88k_loadstore.c
100644 blob c921937579058e6e487d65af2d7e755b28d92180	src/cpus/tmp_m88k_loadstore.c
$ git config --get core.filemode ; git config --get core.autocrlf
false
false
$ md5 (first 8): HEAD blob vs working tree vs the measured instrument (RUNS.log / fixed.meta)
  generator   HEAD bebaf439  WT 6a1fec41   (RUNS.log "repo generator 6a1fec41")
  table       HEAD 269e6e6f  WT d222e737   (RUNS.log "repo table d222e737")
  driver      HEAD (none)  WT cc2f3cf1   (RUNS.log "want md5 cc2f3cf1")
  gate        HEAD 8161cafe  WT 74d84bc1  staged copy 7a7fd8bc

## 5. the two src files across the four fork trees (md5, first 8; working-tree reads; WSL /tmp/gxsec-build is in CLEARANCE.out)
src/cpus/generate_m88k_loadstore.c  GXEMUL-SEC=6a1fec41 est=6a1fec41 build=6a1fec41 build-asan=6a1fec41
src/cpus/tmp_m88k_loadstore.c  GXEMUL-SEC=d222e737 est=d222e737 build=d222e737 build-asan=d222e737
est: no .MUTANT
build: no .MUTANT
build-asan: no .MUTANT
divergence set (grep -vE '^\s*(#|$)' tools/est_divergence.txt):
  src/devices/.index
  src/devices/Makefile.skel
  src/devices/autodev.c
  src/devices/dev_jazz.c
  src/devices/dev_ne2000.c
  src/machines/machine_arc.c

## 6. the working tree is NOT the round alone: every tracked file (src/ regress/ tools/ CHANGELOG OUTSTANDING_BUGS; regress/artifacts/ excluded) whose content differs from HEAD
##    (deriver: git ls-tree -r HEAD, then the git blob sha1 of each working-tree file computed in python -- no git index access)
tracked files compared (artifacts excluded): 743
differ from HEAD: 21
  M regress/diff_wdc_identify.c
  M regress/gate_offline.sh
  M regress/gate_sh_rounding.sh
  M regress/gdrom_default_probe.py
  M regress/sh4_chcr_probe.py
  M regress/wdc_addtoinbuf_probe.py
  M src/cpus/cpu_alpha_palcode.c
  M src/cpus/generate_m88k_loadstore.c
  M src/cpus/tmp_m88k_loadstore.c
  M src/devices/dev_lca.c
  M src/devices/dev_pcc2.c
  M src/devices/dev_sh4.c
  M src/include/thirdparty/mvme_pcctworeg.h
  M tools/BRIEF_TEMPLATE.md
  M tools/CLAUDE.md
  M tools/PIPELINE.md
  M tools/adjudicate.sh
  M tools/panel.sh
  M tools/pipeline/check_probe_wiring.py
  M tools/pipeline/ledger.json
  M tools/pipeline/matrix.html
missing in WT: 0
  THIS ROUND'S: src/cpus/generate_m88k_loadstore.c, src/cpus/tmp_m88k_loadstore.c, and ONE hunk of regress/gate_offline.sh (+ the untracked regress/diff_m88k_loadstore_gen.sh).
  NOT THIS ROUND'S (other sessions' in-flight work; not under review): every other path above, and gate_offline.sh's other three hunks.

VERDICT OF §C0: IN FLIGHT -- NOT SHIPPED.  No CHANGELOG hit for the row id or #569 at HEAD or in the working tree; both
src files last committed at the upstream import 39748e3c and now modified in the working tree; the driver and the whole
artifacts directory are untracked; the ledger row is unchanged (state open, witness none, commits empty, no entries).
~~~~

---

## 5. SETTLED PREMISES -- re-inlined so nobody spends an answer re-deriving them

Copied forward from the pass-1 brief's section 5 (`pass1_20261022/packet.md`), pruned to what a question here depends on,
and appended with what pass 1 (`PASS1_RULINGS.md` A/B as amended by E; `CHECKS_mainloop.md`) and the build
(`table1_20261022/`) settled.  **Each was RE-READ IN THIS SCOPE** -- the working tree over HEAD `5986c137` -- by the
drafter; line numbers are the working tree's.  `cpu_m88k_instr.c`, `cpu_m88k_instr_loadstore.c`, `cpu_dyntrans.c`,
`cpu_m88k.c`, `Makefile.skel`, `regress/lib.sh` and `regress/run.sh` are byte-identical to HEAD; in the generator every
line before 254 is unchanged and every line after it moved by +4.

* **S1 -- the generation early return is KEPT.**  `loadstore()` still returns on `if (size == 0 && scaledness)`
  (generator :104-105; the diff does not touch it), so no handler is generated for a scaled byte and no name with
  `_scaled` exists for size 0.  (A2.)
* **S2 -- the deleted arm and its three siblings.**  HEAD's table printer had four `NULL` arms: `store && signedness`
  (:239-242), `!registeroffset && usr` (:244-247), `!registeroffset && scaledness` (:249-252) -- all three unchanged -- and
  `size == 0 && scaledness` (HEAD :254-257), which the diff deletes whole.  MEASURED: 296 `NULL` of 512 at HEAD
  (BASELINE.out section 4), split 128 + 96 + 48 + 24 by arm (the pass-1 census, `pass1_20261022/packet.md` section 7;
  PRETABLE.out section 1); 272 after the fix (FIX.out; the drafter's re-parse, S18a).
* **S3 -- the consumers, unchanged by the diff (cpu_m88k_instr.c; section 8.2).**  `X(xmem_slow)` indexes
  `m88k_loadstore[...]` for its load half (:2377-2382) and its store half (:2411-2417), ALWAYS adding
  `M88K_LOADSTORE_NO_PC_SYNC` and NEVER `M88K_LOADSTORE_SIGNEDNESS`, takes `scaled` from `iword & 0x200` (:2357) and
  `user` from `iword & 0x80` (:2359), and calls both slots with no NULL test (:2395, :2426).  The register-form `ld`/`st`
  decoder installs `m88k_loadstore[...]` as `ic->f` (:3622-3629: adds SCALEDNESS and USR, never NO_PC_SYNC), and a NULL
  `ic->f` reaches `fatal("INTERNAL ERROR: ic->f == NULL!\n"); goto bad;` (cpu_dyntrans.c:1906-1908), which stops the
  emulated CPU.  The immediate form (:3087-3091) never adds SCALEDNESS, USR or REGISTEROFFSET.  Exactly these four
  sites index the table (CHECKS #3).
* **S4 -- which of the 24 cells have a guest consumer today (A6; B8 as amended by E).**  16 do: 160 164 168 176 180 184
  224 228 232 240 244 248 (the register-form decoder, both endians, plain and `.usr`) and 416 420 432 436 (`xmem_slow`,
  plain `ld.bu`/`st.b`, both endians).  480 484 496 500 gain `xmem_slow` as a consumer only if `m88kxmemusr` is fixed
  (the register-form decoder sends bit `0x80` to `fatal("wt bit not yet implemented! TODO\n"); goto bad;`, :3606-3614,
  BEFORE `xmem_slow`, and the immediate form forces `user = 0`, :2372).  424 440 488 504 have none (`xmem_slow` never
  adds SIGNEDNESS).  The little-endian half IS reachable (A6: the ELF loader and a configuration `byte_order` override
  the constructor's big-endian).  **ALL 24 ARE THE FLOOR** (E/B8): `main()`'s loops emit every one of them; 16 is the
  current guest-consumer SUBSET, not the floor.
* **S5 -- the alias is the architecture and needs no new function.**  MC88100 User's Manual (local OCR text,
  `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\mc88100.txt:2961-2965`): "When the source 2 operand is scaled, it is shifted by
  0, 1, 2, or 3 bits (multiplied by scale factor 1, 2, 4, or 8) for byte, half-word, word, or double-word accesses,
  respectively. For byte accesses, the 5UBOPCODE [OCR for SUBOPCODE] field is distinctly different from the register
  indirect with index (unscaled) cases but the result is identical."  The handlers compute
  `reg(ic->arg[1]) + LS_SIZE * reg(ic->arg[2])` under `LS_SCALED` (cpu_m88k_instr_loadstore.c:65-70 generic, :248-253
  fast), `LS_SIZE` 1 for a byte.  `print_function_name()` appends `_scaled` only `if (scaledness && size > 0)` (:80-81)
  and prints `_le` for EVERY byte entry whatever its endianness (:74-75), so each repaired slot prints its index-32
  counterpart's existing name (12 distinct names) -- the idiom the table ALREADY uses for big-endian byte slots
  (`loadstore()` :101-102 generates no big-endian byte function).
* **S6 -- two fixed sites, both live.**  `src/cpus/tmp_m88k_loadstore.c` is TRACKED; `src/cpus/Makefile.skel:134-135`
  regenerates it only when the template or the generator binary is newer (CHECKS #10; #4 corrected), so a build compiles
  EITHER the committed copy OR fresh generator output.  (A5; B1.)
* **S7 -- the decoder is not edited;** the external `op != 3` recipe is not in this tree and could not reach
  `xmem_slow`'s own `scaled` (A3).
* **S8 -- the witness:** rung-3 attempt BLOCKED (classifier stop), owner ruling "Detector-only, attempt recorded",
  witness term `detector:<path>` (section 2; R18).
* **S9 -- the detector's shape (B1, B2, B10):** a POSIX `sh` driver on the committed `regress/diff_autodev_gen.sh` (#406)
  pattern that compiles and runs the REAL generator in a scratch copy, reads the COMMITTED table separately, pins BOTH by
  ABSOLUTE name equality against names hard-coded in the driver, and `cmp`s the two; the relative `slot[i] == slot[i-32]`
  comparison is NOT a pin (anchor rule, R11).  Wired in GATE 2 (`regress/gate_offline.sh`).
* **S10 -- clause (c) for an offline instrument (B6):** a comment-only generator and a comment-only table, recorded in
  the form `(c): measured at <artifact>`; the "identity xmem body" medium belongs to runtime handler instruments and does
  not apply (R2).
* **S11 -- clause (d) for a pure deletion (B7 as amended):** the removed behaviour re-introduced under a DIFFERENT
  predicate (R4); L5 = `grok_t1p1.txt:76`'s v2 only (first difference at index 416); `codex_t1p1.txt:100` is a
  different variant (first overall difference 256), kept only as supplementary L5b; L6 = one endian half left as
  before the fix (GLM Q12:52), built as the little-endian half.
* **S12 -- the accept side (B3, B9 as amended):** halfword 161/177 are owed under R12 (the adjacent modelled size), NOT
  under rule D2 (a callee compare is outside the DEPENDS-ON walk, R5); the v6 form (`size > 0` moved by one) is NOT
  silent -- it also yields duplicate generated DEFINITION names, which the driver does not compile.
* **S13 -- the counts are narrow controls (B4 as amended):** `NULL == 272` is SUPPLEMENTARY (a moved NULL keeps the
  count); `#define LS_N == 198` and stderr `generated_functions == 198` are a narrow suppression-count control, NOT a
  definition-integrity check (broader definition integrity is disclosed as outside the contract).
* **S14 -- explicit red, never a skip (B5 as amended):** a compile or link failure, a non-zero exit, an empty stdout, a
  missing generator and a missing table are each an explicit RED row; never `need_file` (which calls `gate_skip`,
  `regress/lib.sh:147-151`).
* **S15 -- the enumerated total (B12 as amended):** 54 DISTINCT name pins per artifact = 24 repairs + 24 counterparts
  (index-32) + 6 further accepts (161 177 418 422 434 438); the three counterparts that are also accepts (144 400 404)
  are emitted ONCE, as accept rows, so 21 rows are "counterpart" rows.  Total 4 + 2 x (5 + 54) + 1 = **123**.
* **S16 -- C1 and C2 are FILED outside T1, in T1's landing,** as `m88kxmemaddrovl` (MED; wrong-address access with
  possible secondary fault behaviour; unmeasured) and `m88klepsrbo` (CPU-STOP / MED; source-established; unmeasured).
  Neither row exists yet in the ledger or in OUTSTANDING_BUGS.md (section 4, part 2).
* **S17 -- propagation:** `tools/precommit_check.sh` section A compares only `src/` paths between GXEMUL-SEC and `est/`
  (its loop skips everything else: `case "$f" in` / `src/*) ;;` / `*) continue ;;`); neither src file is in the derived divergence set
  (`grep -vE '^\s*(#|$)' tools/est_divergence.txt`, section 4 part 5); `est/` has no `regress/` directory.
* **S18 -- the drafter's own derivations (CHECK THEM; each was computed from the files, not copied from a record):**
  (a) parsing the 512-entry initializer in HEAD's and the working tree's table: exactly 24 entries differ, at indices 160
  164 168 176 180 184 224 228 232 240 244 248 416 420 424 432 436 440 480 484 488 496 500 504; all 24 were `NULL` at
  HEAD; each new name equals the entry at index-32 in BOTH trees; 12 distinct names; `NULL` 296 -> 272; declaration at
  line 3738 in both.  (b) All 54 expected names in the driver's spec block equal `print_function_name()`'s naming rule
  applied to their index (0 differ).  (c) The GATE 2 block's three index lists equal the driver's spec classes R+N
  (24), A (9) and C (21), and with its five fixed ids yield exactly 123 identities.  (d) The 54 index->name pairs are
  identical between driver v2 and driver v3 (`driver_v2_to_v3.diff`: only the class letters F/E -> R/N and the
  descriptions changed).  (e) The GATE 2 run's driver log `GATE2_diff_m88k_loadstore_gen.log` is byte-identical to
  `fixed.out` (md5 `5f803a73`).
* **S19 -- modes.**  HEAD's `regress/gate_offline.sh` is mode 100644 and is run by `bash` (`regress/run.sh:85`:
  `bash "$HERE/$g.sh"`); the GATE 2 block EXECUTES the driver directly (`"$HERE/diff_m88k_loadstore_gen.sh"`), so the
  driver needs the executable bit; the precedent `regress/diff_autodev_gen.sh` is committed 100755; this repository has
  `core.fileMode=false` (section 4, part 4).
* **S20 -- coverage outside the GATE 2 block.**  `tools/pipeline/check_probe_wiring.py` (HEAD) governs `.py` files only:
  "`domain()' is `.py'-ONLY BY CONSTRUCTION ... A `.sh' path can therefore NEVER be in the domain" (:1247-1248).  GATE 2's
  self-variant manifest loops over `"$HERE"/diff_*.c` only (HEAD `gate_offline.sh:1155`, the `SM_COVERED` check).  So
  neither covers a `.sh` driver -- the committed `diff_autodev_gen.sh` (#406) included -- and no `.py` exists under
  `regress/artifacts/m88kscaledbyte/`.

---

## 6. PREMISES STATED AS QUESTIONS -- check these; ratification is not wanted

* **P1 -- the `#569` comment's scope (-> Q1c).**  The comment (generator :254-261, section 7.1) says the 24 slots "were
  NULL, and xmem_slow() calls them unguarded while the ld/st decoder installs them as ic->f (both in cpu_m88k_instr.c)".
  S4: 8 of the 24 have no consumer today, and the driver's own header marks them "(no consumer)".  PRETABLE.out section 2
  maps this sentence (C6) to NO ROW, as a guest-path consequence.  Is the sentence true as written, or does it over-state
  -- and is that an L4 matter or acceptable shorthand?
* **P2 -- which tree GATE 2's `PASS (502 checks)` describes (-> Q4d).**  The builder ran GATE 2 on the WORKING TREE
  (BUILD_REPORT D-10).  Its `gate_offline.sh` carries three foreign hunks that add 17 `check` calls (the drafter's count:
  58 added lines; no added line opens a loop; the 17 are named-row presence checks inside the existing WDC IDENTIFY
  block, whose added comment reads "#563: the #473 class, closed.  Seventeen rows" -- another session's in-flight work),
  and GATE 2 also compiles `regress/diff_wdc_identify.c`, which is foreign-modified in the working tree.  The weekly
  battery's GATE 2 counts (quoted in section 9.15 of `brief2_FULL.md`): `offline-differential: PASS (359 checks)` on
  2026-10-04 at HEAD `1329d894`, whose `TREE_DIRTY` list (alphabetical) names neither `regress/gate_offline.sh` nor
  `regress/diff_wdc_identify.c`; `PASS (376 checks)` on 2026-10-11 and 2026-10-18, both verdicts `TREE_DIRTY=YES` WITH
  both files modified.  `1329d894` is the last commit to touch `regress/gate_offline.sh`, `regress/diff_wdc_identify.c`
  or `regress/lib.sh` (`git log 1329d894..HEAD` on those paths is empty).  So I believe HEAD's GATE 2 reports 359,
  376 = 359 + those 17, and the COMMITTED form (the staged copy: HEAD + this round's 126 checks) would report **485**,
  not 502.  That is DERIVED, not measured: the staged copy was never run.  Is the derivation right, and what may the
  record and the commit message claim?
* **P3 -- the block runs BEFORE GATE 2's compiler detection (-> Q4a).**  The block sits after the `#375` block (HEAD :72);
  GATE 2 sets `CC=$(command -v cc || command -v gcc)` only at HEAD :185 (after a `gate_skip "no C compiler on PATH"` at
  :183-184), and `regress/lib.sh` does not export `CC`; the driver uses `CC=${CC:-cc}`.  So I believe that on a host with
  `gcc` but no `cc` the block reds at `gen_compiles` while the gate's own compiled differentials would still run, and that
  on a host with no compiler at all GATE 2 now reports FAIL instead of SKIP (BUILD_REPORT D-9: `gate_skip` prints FAIL
  when any check has already failed, `regress/lib.sh:137-145`).  The `b1w` comment just below the insertion says
  compiler-free checks sit before the compiler check "on purpose".  Is either consequence a defect, and is the placement
  right?
* **P4 -- the `-x` row on this machine (-> Q4a).**  BUILD_REPORT section 2: the driver "must be added with mode 100755
  (the gate tests `-x`; `core.fileMode=false` here, and WSL shows rwx regardless)".  If so, the "driver is executable"
  row cannot go red on this machine, and the committed mode is observable only by `git ls-files -s` after staging or on
  a host that honours file modes.  Is the row sound, and what does the landing owe?
* **P5 -- the pre-fix order (-> Q3d).**  The only pre-edit-DATED red is driver v1's (122 rows; `driver_v1/prefix_HEAD.out`
  09:46:19, run on the unmodified repository; the generator edit is 09:46:58).  The SHIPPED driver v3 (123 rows) was
  measured pre-fix at 10:03:08, AFTER the edit, through `GEN=`/`TABLE=` pointing at byte-exact copies of the HEAD blobs
  (`RUNS.log`, md5 `bebaf439` / `269e6e6f`).  S18(d): the 54 expected pairs are unchanged v1 -> v3; v3 adds the
  `gen_stdout` row (green pre-fix) and the identity column.  Does v1's dated red discharge the order discriminator for
  every v3 row that is red pre-fix, or does the record owe something?
* **P6 -- no per-run self-check (-> Q2e).**  The `#406` driver re-runs its own variant lane on every gate run (the gate
  checks `MUTANT killed: full revert` and `MUTANT killed: noglob only`, section 8.6), and GATE 2 re-runs a self-variant
  for every `diff_*.c` (S20).  The `#569` driver's 16 legs ran ONCE (`table1_20261022/`).  Is the one-time table
  sufficient for a detector of this shape, or is a per-run self-check owed or worth filing?
* **P7 -- the 123 identity pins (-> Q4e).**  PRETABLE_v3 section 5: "checked by construction when the gate block is
  read, and by the green GATE 2 run" -- no leg deletes, renames or duplicates a row.  Is that by-construction reading
  sound (R2's record forms)?  BUILD_REPORT open question 2: 123 individual checks, or one aggregated check that names any
  failing identity?
* **P8 -- the partition outside the 24 (-> Q2d).**  PRETABLE.out section 3 says the guard cell (`size == 0 &&
  scaledness`) is EXHAUSTED by the 24 pins, and lists as SAMPLED or unrowed: halfword kinds other than `ld.hu` sync
  (`ld.h`, `st.h`, `.usr`, no-PC-sync), scaled word with PC-sync, scaled doubleword, and the immediate-form byte cells.
  Is any of those a FLOOR cell under R7 as E amended it (S4: "all 24"), or are they all clause-(e) disclosure?

---

## 7. THE DIFF -- every hunk of the round's four files, INLINED

The numstat was computed WITHOUT touching the git index -- `git show HEAD:<path> | diff -u - <path>`, and for the gate
HEAD's blob against the staged copy.  `git diff` was deliberately not run (another process may hold the index).

    file                                          +     -   form in this brief
    src/cpus/generate_m88k_loadstore.c            8     4   INLINED (7.1) -- the one hunk, whole
    src/cpus/tmp_m88k_loadstore.c                24    24   INLINED (7.2) -- all 8 hunks, whole
    regress/gate_offline.sh   (HEAD -> staged)   45     0   INLINED (7.3) -- the one hunk, whole
    regress/diff_m88k_loadstore_gen.sh          276     0   INLINED (7.4) -- the whole NEW file (untracked), numbered
    -------------------------------------------------------
    regress/gate_offline.sh   (staged -> WT)     58     3   NOT SHOWN -- the three foreign hunks; not this round's and not
                                                            to be committed with it (section 0)
    regress/artifacts/m88kscaledbyte/**          (new)      SUMMARIZED -- section 9 inlines the decisive artifacts; the leg
                                                            variant files L*.diff / S*.diff are NOT SHOWN (each leg is
                                                            named by its id, description and score)

md5 (first 8) of what is shown: generator `bebaf439` -> `6a1fec41`; table `269e6e6f` -> `d222e737`; gate HEAD `8161cafe`
-> staged `7a7fd8bc` (the working-tree file, with the foreign hunks, is `74d84bc1`); driver `cc2f3cf1` -- the instrument
every v3 run used (`RUNS.log`: "want md5 cc2f3cf1575b99459c27f6bdcdaf2abe").

### 7.1 `src/cpus/generate_m88k_loadstore.c` (HEAD -> working tree)
~~~~diff
--- a/src/cpus/generate_m88k_loadstore.c
+++ b/src/cpus/generate_m88k_loadstore.c
@@ -251,10 +251,14 @@
 				continue;
 			}
 
-			if (size == 0 && scaledness) {
-				printf("\tNULL");
-				continue;
-			}
+			/*  #569: no NULL arm for scaled byte accesses.  A
+			    byte's scale factor is 1, so a scaled byte access
+			    is the unscaled one, and print_function_name()
+			    already omits "_scaled" for size 0: these 24 slots
+			    name the unscaled byte handlers.  They were NULL,
+			    and xmem_slow() calls them unguarded while the
+			    ld/st decoder installs them as ic->f (both in
+			    cpu_m88k_instr.c).  */
 
 			printf("\tm88k_instr_");
 			print_function_name(size, store, signedness,
~~~~

### 7.2 `src/cpus/tmp_m88k_loadstore.c` (HEAD -> working tree; regenerated by the fixed generator, never hand-edited -- FIX.out)
The initializer's declaration is at line 3738 in both versions; each hunk changes three entries of one 16-entry
group.  Index of a changed line = (its line number) - 3739.
~~~~diff
--- a/src/cpus/tmp_m88k_loadstore.c
+++ b/src/cpus/tmp_m88k_loadstore.c
@@ -3896,15 +3896,15 @@
 	NULL,
 	NULL,
 	NULL,
-	NULL,
+	m88k_instr_ld_u_1_le_regofs,
 	m88k_instr_ld_u_2_le_scaled_regofs,
 	m88k_instr_ld_u_4_le_scaled_regofs,
 	m88k_instr_ld_u_8_le_scaled_regofs,
-	NULL,
+	m88k_instr_st_1_le_regofs,
 	m88k_instr_st_2_le_scaled_regofs,
 	m88k_instr_st_4_le_scaled_regofs,
 	m88k_instr_st_8_le_scaled_regofs,
-	NULL,
+	m88k_instr_ld_1_le_regofs,
 	m88k_instr_ld_2_le_scaled_regofs,
 	m88k_instr_ld_4_le_scaled_regofs,
 	m88k_instr_ld_8_le_scaled_regofs,
@@ -3912,15 +3912,15 @@
 	NULL,
 	NULL,
 	NULL,
-	NULL,
+	m88k_instr_ld_u_1_le_regofs,
 	m88k_instr_ld_u_2_be_scaled_regofs,
 	m88k_instr_ld_u_4_be_scaled_regofs,
 	m88k_instr_ld_u_8_be_scaled_regofs,
-	NULL,
+	m88k_instr_st_1_le_regofs,
 	m88k_instr_st_2_be_scaled_regofs,
 	m88k_instr_st_4_be_scaled_regofs,
 	m88k_instr_st_8_be_scaled_regofs,
-	NULL,
+	m88k_instr_ld_1_le_regofs,
 	m88k_instr_ld_2_be_scaled_regofs,
 	m88k_instr_ld_4_be_scaled_regofs,
 	m88k_instr_ld_8_be_scaled_regofs,
@@ -3960,15 +3960,15 @@
 	NULL,
 	NULL,
 	NULL,
-	NULL,
+	m88k_instr_ld_u_1_le_usr_regofs,
 	m88k_instr_ld_u_2_le_scaled_usr_regofs,
 	m88k_instr_ld_u_4_le_scaled_usr_regofs,
 	m88k_instr_ld_u_8_le_scaled_usr_regofs,
-	NULL,
+	m88k_instr_st_1_le_usr_regofs,
 	m88k_instr_st_2_le_scaled_usr_regofs,
 	m88k_instr_st_4_le_scaled_usr_regofs,
 	m88k_instr_st_8_le_scaled_usr_regofs,
-	NULL,
+	m88k_instr_ld_1_le_usr_regofs,
 	m88k_instr_ld_2_le_scaled_usr_regofs,
 	m88k_instr_ld_4_le_scaled_usr_regofs,
 	m88k_instr_ld_8_le_scaled_usr_regofs,
@@ -3976,15 +3976,15 @@
 	NULL,
 	NULL,
 	NULL,
-	NULL,
+	m88k_instr_ld_u_1_le_usr_regofs,
 	m88k_instr_ld_u_2_be_scaled_usr_regofs,
 	m88k_instr_ld_u_4_be_scaled_usr_regofs,
 	m88k_instr_ld_u_8_be_scaled_usr_regofs,
-	NULL,
+	m88k_instr_st_1_le_usr_regofs,
 	m88k_instr_st_2_be_scaled_usr_regofs,
 	m88k_instr_st_4_be_scaled_usr_regofs,
 	m88k_instr_st_8_be_scaled_usr_regofs,
-	NULL,
+	m88k_instr_ld_1_le_usr_regofs,
 	m88k_instr_ld_2_be_scaled_usr_regofs,
 	m88k_instr_ld_4_be_scaled_usr_regofs,
 	m88k_instr_ld_8_be_scaled_usr_regofs,
@@ -4152,15 +4152,15 @@
 	NULL,
 	NULL,
 	NULL,
-	NULL,
+	m88k_instr_ld_u_1_le_regofs_nopcsync,
 	m88k_instr_ld_u_2_le_scaled_regofs_nopcsync,
 	m88k_instr_ld_u_4_le_scaled_regofs_nopcsync,
 	m88k_instr_ld_u_8_le_scaled_regofs_nopcsync,
-	NULL,
+	m88k_instr_st_1_le_regofs_nopcsync,
 	m88k_instr_st_2_le_scaled_regofs_nopcsync,
 	m88k_instr_st_4_le_scaled_regofs_nopcsync,
 	m88k_instr_st_8_le_scaled_regofs_nopcsync,
-	NULL,
+	m88k_instr_ld_1_le_regofs_nopcsync,
 	m88k_instr_ld_2_le_scaled_regofs_nopcsync,
 	m88k_instr_ld_4_le_scaled_regofs_nopcsync,
 	m88k_instr_ld_8_le_scaled_regofs_nopcsync,
@@ -4168,15 +4168,15 @@
 	NULL,
 	NULL,
 	NULL,
-	NULL,
+	m88k_instr_ld_u_1_le_regofs_nopcsync,
 	m88k_instr_ld_u_2_be_scaled_regofs_nopcsync,
 	m88k_instr_ld_u_4_be_scaled_regofs_nopcsync,
 	m88k_instr_ld_u_8_be_scaled_regofs_nopcsync,
-	NULL,
+	m88k_instr_st_1_le_regofs_nopcsync,
 	m88k_instr_st_2_be_scaled_regofs_nopcsync,
 	m88k_instr_st_4_be_scaled_regofs_nopcsync,
 	m88k_instr_st_8_be_scaled_regofs_nopcsync,
-	NULL,
+	m88k_instr_ld_1_le_regofs_nopcsync,
 	m88k_instr_ld_2_be_scaled_regofs_nopcsync,
 	m88k_instr_ld_4_be_scaled_regofs_nopcsync,
 	m88k_instr_ld_8_be_scaled_regofs_nopcsync,
@@ -4216,15 +4216,15 @@
 	NULL,
 	NULL,
 	NULL,
-	NULL,
+	m88k_instr_ld_u_1_le_usr_regofs_nopcsync,
 	m88k_instr_ld_u_2_le_scaled_usr_regofs_nopcsync,
 	m88k_instr_ld_u_4_le_scaled_usr_regofs_nopcsync,
 	m88k_instr_ld_u_8_le_scaled_usr_regofs_nopcsync,
-	NULL,
+	m88k_instr_st_1_le_usr_regofs_nopcsync,
 	m88k_instr_st_2_le_scaled_usr_regofs_nopcsync,
 	m88k_instr_st_4_le_scaled_usr_regofs_nopcsync,
 	m88k_instr_st_8_le_scaled_usr_regofs_nopcsync,
-	NULL,
+	m88k_instr_ld_1_le_usr_regofs_nopcsync,
 	m88k_instr_ld_2_le_scaled_usr_regofs_nopcsync,
 	m88k_instr_ld_4_le_scaled_usr_regofs_nopcsync,
 	m88k_instr_ld_8_le_scaled_usr_regofs_nopcsync,
@@ -4232,15 +4232,15 @@
 	NULL,
 	NULL,
 	NULL,
-	NULL,
+	m88k_instr_ld_u_1_le_usr_regofs_nopcsync,
 	m88k_instr_ld_u_2_be_scaled_usr_regofs_nopcsync,
 	m88k_instr_ld_u_4_be_scaled_usr_regofs_nopcsync,
 	m88k_instr_ld_u_8_be_scaled_usr_regofs_nopcsync,
-	NULL,
+	m88k_instr_st_1_le_usr_regofs_nopcsync,
 	m88k_instr_st_2_be_scaled_usr_regofs_nopcsync,
 	m88k_instr_st_4_be_scaled_usr_regofs_nopcsync,
 	m88k_instr_st_8_be_scaled_usr_regofs_nopcsync,
-	NULL,
+	m88k_instr_ld_1_le_usr_regofs_nopcsync,
 	m88k_instr_ld_2_be_scaled_usr_regofs_nopcsync,
 	m88k_instr_ld_4_be_scaled_usr_regofs_nopcsync,
 	m88k_instr_ld_8_be_scaled_usr_regofs_nopcsync,
~~~~

### 7.3 `regress/gate_offline.sh` -- HEAD's blob -> the staged copy `table1_20261022/staged/gate_offline.sh` (the ONE hunk to commit)
The three lines above and below the insertion are HEAD's: the end of the `#375` block (`done`) and the start of the
`b1w` block, whose comment says it is "Placed BEFORE the compiler check on purpose".
~~~~diff
--- a/regress/gate_offline.sh
+++ b/regress/gate_offline.sh
@@ -71,6 +71,51 @@
         "$([ "$(ls_entry $arr 5)" != "$(ls_entry $arr 21)" ] && echo differ || echo same)" "differ"
 done
 
+# ---- #569: the m88k load/store dispatch-table generator --------------------------
+# generate_m88k_loadstore.c printed NULL for the 24 scaled-byte slots of
+# m88k_loadstore[512], which cpu_m88k_instr.c indexes with no NULL check
+# (xmem_slow() calls the slot; the register-form ld/st decoder installs it as
+# ic->f). The fix deletes that NULL arm, so the slots name the unscaled byte
+# handlers. The driver compiles and runs the REAL generator in a scratch copy and
+# reads the COMMITTED table separately -- each alone stays green when only the
+# other is reverted -- against names hard-coded in the driver, never read from
+# either artifact. GEN and TABLE are cleared so this always tests the committed
+# files. A missing or non-compiling generator, one that fails to run, and a
+# missing table are each a red row inside the driver, never a skip.
+MLSLOG=$LOGDIR/diff_m88k_loadstore_gen.log
+if [ ! -x "$HERE/diff_m88k_loadstore_gen.sh" ]; then
+    check "m88k loadstore generator: driver is executable" "no" "yes"
+else
+    GEN= TABLE= "$HERE/diff_m88k_loadstore_gen.sh" > "$MLSLOG" 2>&1
+    sed 's/^/       /' "$MLSLOG"
+    check     "m88k loadstore generator: row failures" \
+              "$(sed -n 's/^ROWS=[0-9]* FAIL=\([0-9]*\)$/\1/p' "$MLSLOG")" "0"
+    check     "m88k loadstore generator: rows run (the denominator is the pin)" \
+              "$(sed -n 's/^ROWS=\([0-9]*\) FAIL=[0-9]*$/\1/p' "$MLSLOG")" "123"
+    check     "m88k loadstore generator: completion sentinel" \
+              "$(grep -c '^M88KLS_DONE$' "$MLSLOG")" "1"
+    #  EVERY ROW BY IDENTITY, each exactly once, from lists held HERE and not read
+    #  from the driver: a deleted, renamed or duplicated row is red by name, which
+    #  the total alone cannot say.  The lists are the driver's contract -- the 24
+    #  repaired slots; the 6 further accepts plus the 3 counterparts that are also
+    #  accepts; the other 21 counterparts -- in both artifacts, plus the generator
+    #  status rows and the cmp row: 4 + 2 x (5 + 24 + 9 + 21) + 1 = 123.
+    _mls_pin="160 164 168 176 180 184 224 228 232 240 244 248 416 420 424 432 436 440 480 484 488 496 500 504"
+    _mls_acc="161 177 418 422 434 438 144 400 404"
+    _mls_cp="128 132 136 148 152 192 196 200 208 212 216 384 388 392 408 448 452 456 464 468 472"
+    _mls_ids="gen_compiles gen_exit gen_stdout gen_count cmp_fresh_committed"
+    for _a in fresh committed; do
+        _mls_ids="$_mls_ids ${_a}_present ${_a}_inits ${_a}_entries ${_a}_nulls ${_a}_lsn"
+        for _i in $_mls_pin; do _mls_ids="$_mls_ids ${_a}_pin$_i"; done
+        for _i in $_mls_acc; do _mls_ids="$_mls_ids ${_a}_acc$_i"; done
+        for _i in $_mls_cp;  do _mls_ids="$_mls_ids ${_a}_cp$_i"; done
+    done
+    for _id in $_mls_ids; do
+        check "m88k loadstore generator: row $_id, exactly once" \
+              "$(grep -ow -- "$_id" "$MLSLOG" | wc -l | tr -d ' ')" "1"
+    done
+fi
+
 #  b1w: the pty record parser's selftest, and a POSITIVE CONTROL that proves the selftest can
 #  still catch something.  Placed BEFORE the compiler check on purpose: it needs only python3,
 #  and a machine without cc must not silently lose parser coverage as well as the
~~~~

### 7.4 `regress/diff_m88k_loadstore_gen.sh` -- the WHOLE new file (276 lines, untracked; md5 `cc2f3cf1`)
~~~~
  1| #!/bin/sh
  2| #
  3| #  #569: does generate_m88k_loadstore.c fill the 24 scaled-byte slots of the
  4| #  m88k_loadstore[512] dispatch table, and does the COMMITTED generated table
  5| #  (src/cpus/tmp_m88k_loadstore.c) carry the same text?
  6| #
  7| #  WHY THIS EXISTS.  The generator printed NULL for every scaled BYTE slot
  8| #  (size 0 with scaledness set), while cpu_m88k_instr.c indexes the table with
  9| #  no NULL check: xmem_slow() calls the slot, and the register-form ld/st
 10| #  decoder installs it as ic->f.  A byte's scale factor is 1, so a scaled byte
 11| #  access is the unscaled one, and print_function_name() already omits
 12| #  "_scaled" for size 0; the fix deletes the NULL arm and the slots name the
 13| #  unscaled byte handlers -- the alias this table already uses for the
 14| #  big-endian byte slots.
 15| #
 16| #  TWO ARTIFACTS, AND EACH IS A FIXED SITE.  The build regenerates the table
 17| #  only when the generator binary or the template is newer (Makefile.skel), so
 18| #  a build compiles EITHER the committed copy or fresh output.  A reader of the
 19| #  committed table alone stays green when only the generator is reverted; a run
 20| #  of the generator alone stays green when only the committed table is.  So
 21| #  this compiles and runs the REAL generator in a scratch copy -- NEVER in the
 22| #  repo: it prints the table to stdout and the table is TRACKED -- reads the
 23| #  committed table separately, pins BOTH with the same rows, and asserts the two
 24| #  are byte-identical.
 25| #
 26| #  THE EXPECTED NAMES ARE HARD-CODED BELOW, never read from either artifact: a
 27| #  tracked generated file is not evidence about its own generator (#406), and
 28| #  slot[i] == slot[i-32] holds under a joint rename and under NULL == NULL.
 29| #
 30| #  CONTRACT -- what this detector is designed to catch:
 31| #    * the deleted arm's 24 cells, by ABSOLUTE name equality in both artifacts.
 32| #      ALL 24 ARE THE FLOOR: main()'s own loops emit every one of them, so an
 33| #      escape at any of the 24 is a floor breach.  16 are today's GUEST-
 34| #      CONSUMER subset, marked "(consumer)": the sync ld/st cells, both
 35| #      endians, plain and .usr (160 164 168 176 180 184 224 228 232 240 244
 36| #      248), and the no-PC-sync plain ld.bu/st.b cells (416 420 432 436).  The
 37| #      other 8 (424 440 480 484 488 496 500 504) are marked "(no consumer)" --
 38| #      a fact about today's callers, not a weaker pin; xmem becomes the
 39| #      consumer of 480 484 496 500 if m88kxmemusr is fixed;
 40| #    * the accept side of the deleted predicate (size == 0 && scaledness), by
 41| #      the de-escalation rule's row per adjacent modelled value: the scaled
 42| #      HALFWORD cells 161/177 (size 1, the adjacent size; with the `size > 0`
 43| #      in print_function_name moved by one they are the name rows that
 44| #      change), scaled word xmem 418 422 434 438, and the unscaled byte cells;
 45| #    * 54 DISTINCT NAME PINS PER ARTIFACT: the 24 repairs, their 24 unscaled
 46| #      counterparts at index-32, and 6 further accepts (161 177 418 422 434
 47| #      438).  Three counterparts are also accept cells (144 400 404); each of
 48| #      those indices is emitted ONCE, as an accept row, so 21 rows are
 49| #      "counterpart" rows;
 50| #    * structure: one 512-entry initializer; 272 NULL entries, SUPPLEMENTARY (a
 51| #      MOVED NULL keeps the count -- the absolute pins carry the floor);
 52| #    * a NARROW SUPPRESSION-COUNT CONTROL, NOT a definition-integrity check: 198
 53| #      `#define LS_N` blocks and the generator's stderr generated_functions ==
 54| #      198 see the deletion of loadstore()'s kept size-0-scaled early return
 55| #      (12 more blocks) and nothing finer -- duplicate or wrong definition
 56| #      NAMES keep both counts;
 57| #    * fresh == committed, byte for byte;
 58| #    * the generator compiles and links, exits 0 and prints something, and the
 59| #      committed table is present and parseable -- each an explicit RED row,
 60| #      never a skip.
 61| #  ROWS: 4 generator status rows + 2 x (5 structural + 54 name pins) + 1 cmp =
 62| #  123, every row emitted on every run.  EVERY ROW CARRIES AN IDENTITY, its
 63| #  first field (gen_*, fresh_*, committed_*, cmp_fresh_committed), which
 64| #  occurs exactly once in the output; gate 2 pins each identity, the total and
 65| #  the sentinel.
 66| #  NOT OBSERVED, deliberately: handler BODIES and the xmem exchange itself (the
 67| #  exchanged byte, neighbour preservation, zero extension) -- guest-path
 68| #  channels that belong to the BLOCKED rung-3 witness record,
 69| #  regress/artifacts/m88kscaledbyte/witness_attempt_20261022/WITNESS_ATTEMPT.md;
 70| #  per-slot positions of the other three NULL arms (held only by the count);
 71| #  scaled doubleword names; the immediate-form byte cells; the size tests in
 72| #  print_function_name beyond the halfword edge; the generated DEFINITIONS
 73| #  beyond their count (unique names, flags, references -- the generated file
 74| #  is not compiled here).
 75| #
 76| #  (c): measured at regress/artifacts/m88kscaledbyte/table1_20261022/L3_commentgen.out
 77| #  (a comment-only generator: the compile row and every fresh-side row red) and
 78| #  .../L4_commenttable.out (a comment-only table: every committed-side row red).
 79| #  .../L8_allnull.out (an all-NULL initializer) is supplementary.  SCORES.txt there.
 80| #
 81| #  Overrides, so a table of variants runs WITHOUT touching the repo:
 82| #  GEN=<generator source>, TABLE=<committed table>, CC=<compiler>.  Gate 2
 83| #  clears GEN and TABLE so it always tests the committed files.
 84| #
 85| #  Offline: a C compiler, no guest, no build tree.  Wired into gate 2.
 86| set -u
 87| 
 88| HERE=$(cd "$(dirname "$0")" && pwd)
 89| SEC=$(cd "$HERE/.." && pwd)
 90| GEN=${GEN:-$SEC/src/cpus/generate_m88k_loadstore.c}
 91| TABLE=${TABLE:-$SEC/src/cpus/tmp_m88k_loadstore.c}
 92| CC=${CC:-cc}
 93| 
 94| WORK=${TMPDIR:-/tmp}/gxsec-m88klsgen.$$
 95| #  A killed run must not reach the sentinel: the signal trap EXITS (and the exit
 96| #  trap cleans up), it does not resume the script.
 97| trap 'rm -rf "$WORK"' 0
 98| trap 'exit 1' 1 2 3 15
 99| rm -rf "$WORK"; mkdir -p "$WORK"
100| 
101| rows=0
102| fails=0
103| row() {   # $1 identity  $2 description  $3 got  $4 want -- equality; every row counts
104|     rows=$((rows + 1))
105|     if [ "$3" = "$4" ]; then
106|         printf '  ok   %-20s %-50s %s\n' "$1" "$2" "$3"
107|     else
108|         fails=$((fails + 1))
109|         printf '  FAIL %-20s %-50s got=%s want=%s\n' "$1" "$2" "$3" "$4"
110|     fi
111| }
112| note() { printf '  --   %s\n' "$1"; }
113| 
114| note "GEN   $GEN"
115| note "TABLE $TABLE"
116| 
117| #  index class expected-name description.  R repair with a guest consumer today,
118| #  N repair with none, A accept, C counterpart (index - 32) of a repair.
119| #  index = 256*no_pc_sync + 128*registeroffset + 64*usr + 32*scaledness +
120| #  16*endianness + 8*signedness + 4*store + size, the generator's loop order.
121| cat > "$WORK/spec" <<'EOF'
122| 160 R m88k_instr_ld_u_1_le_regofs scaled ld.bu le sync
123| 164 R m88k_instr_st_1_le_regofs scaled st.b le sync
124| 168 R m88k_instr_ld_1_le_regofs scaled ld.b le sync
125| 176 R m88k_instr_ld_u_1_le_regofs scaled ld.bu be sync
126| 180 R m88k_instr_st_1_le_regofs scaled st.b be sync
127| 184 R m88k_instr_ld_1_le_regofs scaled ld.b be sync
128| 224 R m88k_instr_ld_u_1_le_usr_regofs scaled ld.bu le usr sync
129| 228 R m88k_instr_st_1_le_usr_regofs scaled st.b le usr sync
130| 232 R m88k_instr_ld_1_le_usr_regofs scaled ld.b le usr sync
131| 240 R m88k_instr_ld_u_1_le_usr_regofs scaled ld.bu be usr sync
132| 244 R m88k_instr_st_1_le_usr_regofs scaled st.b be usr sync
133| 248 R m88k_instr_ld_1_le_usr_regofs scaled ld.b be usr sync
134| 416 R m88k_instr_ld_u_1_le_regofs_nopcsync scaled ld.bu le nosync
135| 420 R m88k_instr_st_1_le_regofs_nopcsync scaled st.b le nosync
136| 424 N m88k_instr_ld_1_le_regofs_nopcsync scaled ld.b le nosync
137| 432 R m88k_instr_ld_u_1_le_regofs_nopcsync scaled ld.bu be nosync
138| 436 R m88k_instr_st_1_le_regofs_nopcsync scaled st.b be nosync
139| 440 N m88k_instr_ld_1_le_regofs_nopcsync scaled ld.b be nosync
140| 480 N m88k_instr_ld_u_1_le_usr_regofs_nopcsync scaled ld.bu le usr nosync
141| 484 N m88k_instr_st_1_le_usr_regofs_nopcsync scaled st.b le usr nosync
142| 488 N m88k_instr_ld_1_le_usr_regofs_nopcsync scaled ld.b le usr nosync
143| 496 N m88k_instr_ld_u_1_le_usr_regofs_nopcsync scaled ld.bu be usr nosync
144| 500 N m88k_instr_st_1_le_usr_regofs_nopcsync scaled st.b be usr nosync
145| 504 N m88k_instr_ld_1_le_usr_regofs_nopcsync scaled ld.b be usr nosync
146| 161 A m88k_instr_ld_u_2_le_scaled_regofs scaled ld.hu le sync (halfword)
147| 177 A m88k_instr_ld_u_2_be_scaled_regofs scaled ld.hu be sync (halfword)
148| 418 A m88k_instr_ld_u_4_le_scaled_regofs_nopcsync scaled word ld le nosync (xmem)
149| 422 A m88k_instr_st_4_le_scaled_regofs_nopcsync scaled word st le nosync (xmem)
150| 434 A m88k_instr_ld_u_4_be_scaled_regofs_nopcsync scaled word ld be nosync (xmem)
151| 438 A m88k_instr_st_4_be_scaled_regofs_nopcsync scaled word st be nosync (xmem)
152| 144 A m88k_instr_ld_u_1_le_regofs unscaled ld.bu be sync
153| 400 A m88k_instr_ld_u_1_le_regofs_nopcsync unscaled ld.bu be nosync
154| 404 A m88k_instr_st_1_le_regofs_nopcsync unscaled st.b be nosync
155| 128 C m88k_instr_ld_u_1_le_regofs unscaled ld.bu le sync
156| 132 C m88k_instr_st_1_le_regofs unscaled st.b le sync
157| 136 C m88k_instr_ld_1_le_regofs unscaled ld.b le sync
158| 148 C m88k_instr_st_1_le_regofs unscaled st.b be sync
159| 152 C m88k_instr_ld_1_le_regofs unscaled ld.b be sync
160| 192 C m88k_instr_ld_u_1_le_usr_regofs unscaled ld.bu le usr sync
161| 196 C m88k_instr_st_1_le_usr_regofs unscaled st.b le usr sync
162| 200 C m88k_instr_ld_1_le_usr_regofs unscaled ld.b le usr sync
163| 208 C m88k_instr_ld_u_1_le_usr_regofs unscaled ld.bu be usr sync
164| 212 C m88k_instr_st_1_le_usr_regofs unscaled st.b be usr sync
165| 216 C m88k_instr_ld_1_le_usr_regofs unscaled ld.b be usr sync
166| 384 C m88k_instr_ld_u_1_le_regofs_nopcsync unscaled ld.bu le nosync
167| 388 C m88k_instr_st_1_le_regofs_nopcsync unscaled st.b le nosync
168| 392 C m88k_instr_ld_1_le_regofs_nopcsync unscaled ld.b le nosync
169| 408 C m88k_instr_ld_1_le_regofs_nopcsync unscaled ld.b be nosync
170| 448 C m88k_instr_ld_u_1_le_usr_regofs_nopcsync unscaled ld.bu le usr nosync
171| 452 C m88k_instr_st_1_le_usr_regofs_nopcsync unscaled st.b le usr nosync
172| 456 C m88k_instr_ld_1_le_usr_regofs_nopcsync unscaled ld.b le usr nosync
173| 464 C m88k_instr_ld_u_1_le_usr_regofs_nopcsync unscaled ld.bu be usr nosync
174| 468 C m88k_instr_st_1_le_usr_regofs_nopcsync unscaled st.b be usr nosync
175| 472 C m88k_instr_ld_1_le_usr_regofs_nopcsync unscaled ld.b be usr nosync
176| EOF
177| 
178| #  The #375 reader (gate_offline.sh's ls_entry), parametrized by file, array
179| #  name and size, and run ONCE per artifact: every entry of the FIRST
180| #  `(*<array>[<size>])(...) = {` initializer, one per line, in index order.
181| #  This table ends `<last entry> };` on the entry's own line, so the end test is
182| #  "the line holds the closing brace" rather than ls_entry's `^};`.
183| #  Prints "<initializers> <entries> <NULL entries>".
184| parse() {   # $1 file  $2 array  $3 size  $4 entries-out
185|     : > "$4"
186|     if [ ! -f "$1" ]; then echo "0 0 0"; return; fi
187|     awk -v arr="$2" -v size="$3" -v out="$4" '
188|         index($0, "(*" arr "[" size "])") && /= *[{]/ {
189|             inits++; if (inits == 1) f = 1; next }
190|         f { last = ($0 ~ /[}]/); gsub(/[ \t,};]/, "")
191|             if ($0 != "") { n++; print > out; if ($0 == "NULL") nul++ }
192|             if (last) f = 0 }
193|         END { printf "%d %d %d\n", inits, n, nul }' "$1"
194| }
195| ent() { sed -n "$(($2 + 1))p" "$1"; }   # $1 entries file  $2 index
196| 
197| #  Every row is emitted on every run -- a missing artifact turns its rows RED,
198| #  it never removes them -- so the row count is constant and gate 2 pins it.
199| artifact_rows() {   # $1 label  $2 file
200|     lbl=$1; file=$2
201|     counts=$(parse "$file" m88k_loadstore 512 "$WORK/$lbl.ent")
202|     #  The trailing zeros keep $1..$3 set (set -u) if the parse printed nothing.
203|     set -- $counts 0 0 0
204|     if [ ! -f "$file" ]; then present=absent
205|     elif [ "$1" -ge 1 ]; then present=yes
206|     else present="no m88k_loadstore[512] initializer"; fi
207|     row "${lbl}_present" "present and parseable" "$present" "yes"
208|     row "${lbl}_inits" "m88k_loadstore[512] initializers" "$1" "1"
209|     row "${lbl}_entries" "initializer entries" "$2" "512"
210|     row "${lbl}_nulls" "NULL entries (supplementary)" "$3" "272"
211|     if [ -f "$file" ]; then nls=$(grep -c '^#define LS_N ' "$file"); else nls=absent; fi
212|     row "${lbl}_lsn" "#define LS_N blocks (suppression count)" "$nls" "198"
213|     while read -r i c name desc; do
214|         case $c in
215|         R) id=${lbl}_pin$i; d="repair $desc (consumer)" ;;
216|         N) id=${lbl}_pin$i; d="repair $desc (no consumer)" ;;
217|         A) id=${lbl}_acc$i; d="accept $desc" ;;
218|         *) id=${lbl}_cp$i;  d="counterpart $desc" ;;
219|         esac
220|         row "$id" "$d" "$(ent "$WORK/$lbl.ent" "$i")" "$name"
221|     done < "$WORK/spec"
222| }
223| 
224| # ------------------------------------------------- the generator, run for real
225| compiled=no
226| if [ ! -f "$GEN" ]; then
227|     gres="no -- source absent"
228| elif ! cp "$GEN" "$WORK/generate_m88k_loadstore.c" 2>/dev/null; then
229|     gres="no -- source unreadable"
230| elif ( cd "$WORK" && $CC -o generate_m88k_loadstore generate_m88k_loadstore.c ) \
231|         > "$WORK/cc.log" 2>&1 && [ -x "$WORK/generate_m88k_loadstore" ]; then
232|     gres=yes; compiled=yes
233| else
234|     gres="no -- the compile or link failed"
235| fi
236| row gen_compiles "generator: compiles and links" "$gres" "yes"
237| if [ "$compiled" != yes ] && [ -s "$WORK/cc.log" ]; then
238|     sed -e "s|$WORK/||g" -e 's/^/  --   cc: /' "$WORK/cc.log" | head -6
239| fi
240| 
241| #  EXECUTION is its own pair of rows: a generator that compiles and then exits
242| #  non-zero, or prints nothing, is red here and not only downstream.
243| if [ "$compiled" = yes ]; then
244|     ( cd "$WORK" && ./generate_m88k_loadstore > fresh.c 2> gen.err ); grc=$?
245| else
246|     grc="not run"
247| fi
248| row gen_exit "generator: exit status" "$grc" "0"
249| if [ "$compiled" != yes ]; then sres="not run"
250| elif [ -s "$WORK/fresh.c" ]; then sres=yes
251| else sres="no -- stdout empty"; fi
252| row gen_stdout "generator: stdout non-empty" "$sres" "yes"
253| if [ -f "$WORK/gen.err" ]; then
254|     gf=$(sed -n 's/^.*: generated_functions = \([0-9][0-9]*\)$/\1/p' "$WORK/gen.err" | head -1)
255|     [ -n "$gf" ] || gf="not reported"
256| else
257|     gf=absent
258| fi
259| row gen_count "generator: stderr generated_functions" "$gf" "198"
260| 
261| # ---------------------------------------------------- both artifacts, same rows
262| artifact_rows fresh "$WORK/fresh.c"
263| artifact_rows committed "$TABLE"
264| 
265| if [ ! -f "$WORK/fresh.c" ]; then cres="fresh output absent"
266| elif [ ! -f "$TABLE" ]; then cres="committed table absent"
267| elif cmp -s "$WORK/fresh.c" "$TABLE"; then cres=identical
268| else cres=differ; fi
269| row cmp_fresh_committed "fresh == committed, byte for byte (cmp)" "$cres" "identical"
270| if [ "$cres" = differ ]; then
271|     diff "$WORK/fresh.c" "$TABLE" | head -8 | sed 's/^/  --   diff: /'
272| fi
273| 
274| printf '\nROWS=%d FAIL=%d\n' "$rows" "$fails"
275| printf 'M88KLS_DONE\n'
276| if [ "$fails" = 0 ]; then exit 0; else exit 1; fi
~~~~

---

## 8. SOURCE CONTEXT -- as read in the working tree (byte-identical to HEAD except the generator)

### 8.1 The FIXED generator, `src/cpus/generate_m88k_loadstore.c` -- the whole program after the licence header (lines 41-275)
`print_function_name()` names both the table entries and the generated definitions; `loadstore()` holds the generation
early returns (:98-111); `main()` holds the table printer and its three surviving `NULL` arms (:239-252), then the `#569`
comment where the fourth arm was (:254-261).
~~~~
 41| 
 42| #include <stdio.h>
 43| #include <string.h>
 44| 
 45| 
 46| #define	M88K_LOADSTORE_STORE		4
 47| #define	M88K_LOADSTORE_SIGNEDNESS	8
 48| #define	M88K_LOADSTORE_ENDIANNESS	16
 49| #define	M88K_LOADSTORE_SCALEDNESS	32
 50| #define	M88K_LOADSTORE_USR		64
 51| #define	M88K_LOADSTORE_REGISTEROFFSET	128
 52| #define	M88K_LOADSTORE_NO_PC_SYNC	256
 53| 
 54| 
 55| int generated_functions = 0;
 56| 
 57| 
 58| void print_function_name(int size, int store, int signedness,
 59| 	int endianness, int scaledness, int usr, int registeroffset,
 60| 	int no_pc_sync)
 61| {
 62| 	if (store)
 63| 		printf("st");
 64| 	else {
 65| 		printf("ld");
 66| 		if (!signedness)
 67| 			printf("_u");
 68| 	}
 69| 	printf("_%i", 1 << size);
 70| 
 71| 	if (endianness >= 0) {
 72| 		/*  Special case so that Byte loads/stores are only
 73| 		    included ones (for little endian):  */
 74| 		if (size == 0 && endianness)
 75| 			printf("_le");
 76| 		else
 77| 			printf(endianness? "_be" : "_le");
 78| 	}
 79| 
 80| 	if (scaledness && size > 0)
 81| 		printf("_scaled");
 82| 
 83| 	if (usr)
 84| 		printf("_usr");
 85| 
 86| 	if (registeroffset)
 87| 		printf("_regofs");
 88| 
 89| 	if (no_pc_sync)
 90| 		printf("_nopcsync");
 91| }
 92| 
 93| 
 94| void loadstore(int size, int store, int signedness,
 95| 	int endianness, int scaledness, int usr, int registeroffset,
 96| 	int no_pc_sync)
 97| {
 98| 	if (store && signedness)
 99| 		return;
100| 
101| 	if (size == 0 && endianness)
102| 		return;
103| 
104| 	if (size == 0 && scaledness)
105| 		return;
106| 
107| 	if (!registeroffset && usr)
108| 		return;
109| 
110| 	if (!registeroffset && scaledness)
111| 		return;
112| 
113| 	if (store)
114| 		printf("#define LS_STORE\n");
115| 	else
116| 		printf("#define LS_LOAD\n");
117| 
118| 	printf("#define LS_N m88k_instr_");
119| 	print_function_name(size, store, signedness, endianness,
120| 	    scaledness, usr, registeroffset, no_pc_sync);
121| 	printf("\n");
122| 
123| 	printf("#define LS_GENERIC_N m88k_generic_");
124| 	print_function_name(size, store, signedness, -1,
125| 	    scaledness, usr, registeroffset, no_pc_sync);
126| 	printf("\n");
127| 
128| 	printf("#define LS_%i\n", 1 << size);
129| 	printf("#define LS_SIZE %i\n", 1 << size);
130| 
131| 	if (signedness && !store)
132| 		printf("#define LS_SIGNED\n");
133| 
134| 	if (endianness)
135| 		printf("#define LS_BE\n");
136| 	else
137| 		printf("#define LS_LE\n");
138| 
139| 	if (endianness == 0)
140| 		printf("#define LS_INCLUDE_GENERIC\n");
141| 
142| 	if (scaledness)
143| 		printf("#define LS_SCALED\n");
144| 
145| 	if (usr)
146| 		printf("#define LS_USR\n");
147| 
148| 	if (registeroffset)
149| 		printf("#define LS_REGOFS\n");
150| 
151| 	if (no_pc_sync)
152| 		printf("#define LS_NO_PC_SYNC\n");
153| 
154| 	printf("#include \"cpu_m88k_instr_loadstore.c\"\n");
155| 	generated_functions ++;
156| 
157| 	if (no_pc_sync)
158| 		printf("#undef LS_NO_PC_SYNC\n");
159| 
160| 	if (registeroffset)
161| 		printf("#undef LS_REGOFS\n");
162| 
163| 	if (usr)
164| 		printf("#undef LS_USR\n");
165| 
166| 	if (scaledness)
167| 		printf("#undef LS_SCALED\n");
168| 
169| 	if (endianness == 0)
170| 		printf("#undef LS_INCLUDE_GENERIC\n");
171| 
172| 	if (endianness)
173| 		printf("#undef LS_BE\n");
174| 	else
175| 		printf("#undef LS_LE\n");
176| 
177| 	if (signedness && !store)
178| 		printf("#undef LS_SIGNED\n");
179| 
180| 	printf("#undef LS_SIZE\n");
181| 	printf("#undef LS_%i\n", 1 << size);
182| 
183| 	printf("#undef LS_GENERIC_N\n");
184| 	printf("#undef LS_N\n");
185| 
186| 	if (store)
187| 		printf("#undef LS_STORE\n");
188| 	else
189| 		printf("#undef LS_LOAD\n");
190| }
191| 
192| 
193| int main(int argc, char *argv[])
194| {
195| 	int size, store, signedness, endianness, scaledness, usr,
196| 	    registeroffset, no_pc_sync;
197| 
198| 	printf("\n/*  AUTOMATICALLY GENERATED! Do not edit.  */\n\n");
199| 
200| 	for (no_pc_sync=0; no_pc_sync<=M88K_LOADSTORE_NO_PC_SYNC;
201| 		      no_pc_sync+=M88K_LOADSTORE_NO_PC_SYNC)
202| 	 for (registeroffset=0; registeroffset<=M88K_LOADSTORE_REGISTEROFFSET;
203| 		      registeroffset+=M88K_LOADSTORE_REGISTEROFFSET)
204| 	  for (usr=0; usr<=M88K_LOADSTORE_USR; usr+=M88K_LOADSTORE_USR)
205| 	   for (scaledness=0; scaledness<=M88K_LOADSTORE_SCALEDNESS;
206| 			scaledness+=M88K_LOADSTORE_SCALEDNESS)
207| 	    for (endianness=0; endianness<=M88K_LOADSTORE_ENDIANNESS;
208| 			  endianness+=M88K_LOADSTORE_ENDIANNESS)
209| 	      for (signedness=0; signedness<=M88K_LOADSTORE_SIGNEDNESS;
210| 			    signedness+=M88K_LOADSTORE_SIGNEDNESS)
211| 	        for (store=0; store<=M88K_LOADSTORE_STORE;
212| 			      store+=M88K_LOADSTORE_STORE)
213| 		  for (size=0; size<=3; size++)
214| 			loadstore(size, store, signedness,
215| 			    endianness, scaledness, usr, registeroffset,
216| 			    no_pc_sync);
217| 
218| 	/*  Array of pointers to fast load/store functions:  */
219| 	printf("\n\nvoid (*m88k_loadstore[512])(struct cpu *, struct "
220| 	    "m88k_instr_call *) = {\n");
221| 	for (no_pc_sync=0; no_pc_sync<=M88K_LOADSTORE_NO_PC_SYNC;
222| 		      no_pc_sync+=M88K_LOADSTORE_NO_PC_SYNC)
223| 	 for (registeroffset=0; registeroffset<=M88K_LOADSTORE_REGISTEROFFSET;
224| 		      registeroffset+=M88K_LOADSTORE_REGISTEROFFSET)
225| 	  for (usr=0; usr<=M88K_LOADSTORE_USR; usr+=M88K_LOADSTORE_USR)
226| 	   for (scaledness=0; scaledness<=M88K_LOADSTORE_SCALEDNESS;
227| 			scaledness+=M88K_LOADSTORE_SCALEDNESS)
228| 	    for (endianness=0; endianness<=M88K_LOADSTORE_ENDIANNESS;
229| 			  endianness+=M88K_LOADSTORE_ENDIANNESS)
230| 	      for (signedness=0; signedness<=M88K_LOADSTORE_SIGNEDNESS;
231| 			    signedness+=M88K_LOADSTORE_SIGNEDNESS)
232| 	        for (store=0; store<=M88K_LOADSTORE_STORE;
233| 			      store+=M88K_LOADSTORE_STORE)
234| 		  for (size=0; size<=3; size++) {
235| 			if (store || size || signedness || endianness
236| 			    || scaledness || usr || registeroffset || no_pc_sync)
237| 				printf(",\n");
238| 
239| 			if (store && signedness) {
240| 				printf("\tNULL");
241| 				continue;
242| 			}
243| 
244| 			if (!registeroffset && usr) {
245| 				printf("\tNULL");
246| 				continue;
247| 			}
248| 
249| 			if (!registeroffset && scaledness) {
250| 				printf("\tNULL");
251| 				continue;
252| 			}
253| 
254| 			/*  #569: no NULL arm for scaled byte accesses.  A
255| 			    byte's scale factor is 1, so a scaled byte access
256| 			    is the unscaled one, and print_function_name()
257| 			    already omits "_scaled" for size 0: these 24 slots
258| 			    name the unscaled byte handlers.  They were NULL,
259| 			    and xmem_slow() calls them unguarded while the
260| 			    ld/st decoder installs them as ic->f (both in
261| 			    cpu_m88k_instr.c).  */
262| 
263| 			printf("\tm88k_instr_");
264| 			print_function_name(size, store, signedness,
265| 			    endianness, scaledness, usr, registeroffset,
266| 			    no_pc_sync);
267| 		}
268| 	printf(" };\n");
269| 
270| 	fprintf(stderr, "%s: generated_functions = %i\n",
271| 	    argv[0], generated_functions);
272| 
273| 	return 0;
274| }
275| 
~~~~

### 8.2 The consumers, `src/cpus/cpu_m88k_instr.c` (NOT edited; byte-identical to HEAD) and the NULL-`ic->f` check in `src/cpus/cpu_dyntrans.c`
`X(xmem_slow)` -- the field extraction, the immediate-form overrides, both table indexings and both unguarded calls:
~~~~
2348| X(xmem_slow)
2349| {
2350| 	uint32_t iword = ic->arg[0];
2351| 	uint32_t tmp;
2352| 	int d      = (iword >> 21) & 0x1f;
2353| 	int s1     = (iword >> 16) & 0x1f;
2354| 	int s2     =  iword        & 0x1f;
2355| 	int imm16  =  iword        & 0xffff;
2356| 	int regofs = (iword & 0xf0000000) != 0;
2357| 	int scaled = iword & 0x200;
2358| 	int size   = iword & 0x400;
2359| 	int user   = iword & 0x80;
  ...
2365| 	SYNCH_PC;
2366| 	pc_before_memory_access = (uint32_t)cpu->pc;
2367| 
2368| 	if (!regofs) {
2369| 		/*  immediate offset:  */
2370| 		scaled = 0;
2371| 		size = (iword >> 26) & 1;
2372| 		user = 0;
2373| 	}
  ...
2375| 	tmp = cpu->cd.m88k.r[d];
2376| 
2377| 	xmem_load = m88k_loadstore[ (size? 2 : 0)
2378| 	    + (cpu->byte_order == EMUL_BIG_ENDIAN? M88K_LOADSTORE_ENDIANNESS : 0)
2379| 	    + (scaled? M88K_LOADSTORE_SCALEDNESS : 0)
2380| 	    + (user? M88K_LOADSTORE_USR : 0)
2381| 	    + (regofs? M88K_LOADSTORE_REGISTEROFFSET : 0)
2382| 	    + M88K_LOADSTORE_NO_PC_SYNC ];
2383| 
2384| 	call.f = xmem_load;
2385| 	call.arg[0] = (size_t) &cpu->cd.m88k.r[d];
2386| 	call.arg[1] = (size_t) &cpu->cd.m88k.r[s1];
2387| 	if (regofs)
2388| 		call.arg[2] = (size_t) &cpu->cd.m88k.r[s2];
2389| 	else
2390| 		call.arg[2] = imm16;
2391| 
2392| 	if (d == M88K_ZERO_REG)
2393| 		call.arg[0] = (size_t)&cpu->cd.m88k.zero_scratch;
2394| 
2395| 	xmem_load(cpu, &call);
  ...
2411| 	xmem_store = m88k_loadstore[ (size? 2 : 0)
2412| 	    + M88K_LOADSTORE_STORE
2413| 	    + (cpu->byte_order == EMUL_BIG_ENDIAN? M88K_LOADSTORE_ENDIANNESS : 0)
2414| 	    + (scaled? M88K_LOADSTORE_SCALEDNESS : 0)
2415| 	    + (user? M88K_LOADSTORE_USR : 0)
2416| 	    + (regofs? M88K_LOADSTORE_REGISTEROFFSET : 0)
2417| 	    + M88K_LOADSTORE_NO_PC_SYNC ];
2418| 
2419| 	call.f = xmem_store;
2420| 	call.arg[0] = (size_t) &tmp;
2421| 	// arg[1] and arg[2] are already set up from xmem_load call.
2422| 
2423| 	if (d == M88K_ZERO_REG)
2424| 		tmp = 0;
2425| 
2426| 	xmem_store(cpu, &call);
~~~~
The register-form `ld`/`st`/`xmem`/`lda` decoder (opcode 0x3d) -- the `.usr`/`.wt`/scaled bits, the `ld`/`st` table index, the `xmem` dispatch:
~~~~
3604| 			if (iword & 0x100)
3605| 				user = 1;
3606| 			if (iword & 0x80)
3607| 				wt = 1;
3608| 			if (iword & 0x200)
3609| 				scaled = 1;
3610| 
3611| 			if (wt) {
3612| 				fatal("wt bit not yet implemented! TODO\n");
3613| 				goto bad;
3614| 			}
  ...
3620| 			if (op == 0 || op == 1) {
3621| 				/*  ld or st:  */
3622| 				ic->f = m88k_loadstore[ opsize
3623| 				    + (op==1? M88K_LOADSTORE_STORE : 0)
3624| 				    + (signedness? M88K_LOADSTORE_SIGNEDNESS:0)
3625| 				    + (cpu->byte_order == EMUL_BIG_ENDIAN?
3626| 				       M88K_LOADSTORE_ENDIANNESS : 0)
3627| 				    + (scaled? M88K_LOADSTORE_SCALEDNESS : 0)
3628| 				    + (user? M88K_LOADSTORE_USR : 0)
3629| 				    + M88K_LOADSTORE_REGISTEROFFSET ];
  ...
3653| 			} else {
3654| 				/*  xmem:  */
3655| 				ic->f = instr(xmem_slow);
3656| 				ic->arg[0] = iword;
3657| 				if (d == M88K_ZERO_REG)
3658| 					ic->f = instr(nop);
~~~~
The immediate-form `ld`/`st` index (never adds SCALEDNESS, USR or REGISTEROFFSET):
~~~~
3087| 			ic->f = m88k_loadstore[ opsize
3088| 			    + (store? M88K_LOADSTORE_STORE : 0)
3089| 			    + (signedness? M88K_LOADSTORE_SIGNEDNESS:0)
3090| 			    + (cpu->byte_order == EMUL_BIG_ENDIAN?
3091| 			       M88K_LOADSTORE_ENDIANNESS : 0) ];
~~~~
`src/cpus/cpu_dyntrans.c` -- a NULL `ic->f` (the decoder path) goes to `bad:`, which stops the CPU:
~~~~
1906| 	if (ic->f == NULL) {
1907| 		fatal("INTERNAL ERROR: ic->f == NULL!\n");
1908| 		goto bad;
~~~~

### 8.3 `src/cpus/Makefile.skel` -- the dependency-driven regeneration rule (S6)
~~~~
128| cpu_m88k.o: cpu_m88k.c cpu_m88k_instr.c cpu_dyntrans.c memory_rw.c \
129| 	tmp_m88k_loadstore.c tmp_m88k_head.c tmp_m88k_tail.c tmp_m88k_bcnd.c
130| 
131| tmp_m88k_bcnd.c: generate_m88k_bcnd
132| 	./generate_m88k_bcnd > tmp_m88k_bcnd.c
133| 
134| tmp_m88k_loadstore.c: cpu_m88k_instr_loadstore.c generate_m88k_loadstore
135| 	./generate_m88k_loadstore > tmp_m88k_loadstore.c
~~~~

### 8.4 `src/cpus/cpu_m88k_instr_loadstore.c` -- the scaled address computation (S5; generic handler, then fast handler)
~~~~
 65| 	uint32_t addr = reg(ic->arg[1]) +
 66| #ifdef LS_REGOFS
 67| #ifdef LS_SCALED
 68| 	    LS_SIZE *
 69| #endif
 70| 	    reg(ic->arg[2]);
 71| #else
 72| 	    ic->arg[2];
 73| #endif
  ...
248| 	uint32_t addr = reg(ic->arg[1]) +
249| #ifdef LS_REGOFS
250| #ifdef LS_SCALED
251| 	    LS_SIZE *
252| #endif
253| 	    reg(ic->arg[2]);
254| #else
255| 	    ic->arg[2];
256| #endif
~~~~

### 8.5 GATE 2's frame (HEAD): the header, the compiler detection, and `regress/lib.sh`'s `check`, `gate_skip`, `need_file`
`regress/gate_offline.sh` (HEAD):
~~~~
  17| set -u
  18| HERE=$(cd "$(dirname "$0")" && pwd)
  19| . "$HERE/lib.sh"
  20| 
  21| SEC=$ROOT/GXEMUL-SEC
  22| SRC=core/float_emul.c
  23| 
  24| gate_begin "offline-differential"
  ...
 183| command -v cc >/dev/null 2>&1 || command -v gcc >/dev/null 2>&1 || \
 184|     gate_skip "no C compiler on PATH"
 185| CC=$(command -v cc || command -v gcc)
~~~~
`regress/lib.sh` (HEAD):
~~~~
 80| check() {
 81|     _checks=$((_checks+1))
 82|     if [ "$2" = "$3" ]; then
 83|         printf "  ${C_OK}ok${C_OFF}   %-52s %s\n" "$1" "$2"
 84|     else
 85|         printf "  ${C_BAD}FAIL${C_OFF} %-52s got=%s want=%s\n" "$1" "$2" "$3"
 86|         _fails=$((_fails+1))
 87|     fi
 88| }
  ...
137| gate_skip() {
138|     echo
139|     if [ "${_fails:-0}" != 0 ]; then
140|         echo "${C_BAD}$GATE_NAME: FAIL${C_OFF} ($_fails of $_checks checks failed" \
141|              "before this section could not run: $*)"
142|         exit 1
143|     fi
144|     echo "${C_SKIP}$GATE_NAME: SKIP${C_OFF} -- $*"; exit $EXIT_SKIP
145| }
146| 
147| need_file() {
148|     for f in "$@"; do
149|         [ -e "$f" ] || gate_skip "missing required input: $f"
150|     done
151| }
~~~~
`regress/run.sh` (HEAD), how each gate is started:
~~~~
 85|     bash "$HERE/$g.sh"
~~~~

### 8.6 The precedent: HEAD's `#406` block in `regress/gate_offline.sh`, which wires `regress/diff_autodev_gen.sh` (mode 100755)
~~~~
1886| # ---- #406: the autodev.c generator ----------------------------------------------
1887| # A prose mention of "DEVINIT" in a comment used to reach the generated C. It cost
1888| # 358 compiler errors, no binary, gate 1 red and eleven gates skipped -- from one
1889| # comment line, which is still in the tree DELIBERATELY (rewording it would have
1890| # made the hardening deletable in silence).
1891| #
1892| # The driver runs the REAL generator in a scratch copy, so it cannot drift from
1893| # what ships, and it carries its own mutant lane. The load-bearing row is the
1894| # ORDERED NAME LIST, not a character check: measured, the half-fix that keeps
1895| # noglob but drops the anchor emits 27 extra names of which 26 are DOTLESS --
1896| # valid C identifiers that a "no bad characters" row waves straight through, and
1897| # that fail at link time instead of parse time.
1898| AGLOG=$LOGDIR/diff_autodev_gen.log
1899| if [ ! -x "$HERE/diff_autodev_gen.sh" ]; then
1900|     check "autodev generator: driver is executable" "no" "yes"
1901| else
1902|     "$HERE/diff_autodev_gen.sh" > "$AGLOG" 2>&1
1903|     sed 's/^/       /' "$AGLOG"
1904|     check     "autodev generator: row failures" \
1905|               "$(grep -oE '[0-9]+ failures' "$AGLOG" | grep -oE '^[0-9]+')" "0"
1906|     check_min "autodev generator: rows actually run" \
1907|               "$(grep -oE '^[0-9]+ rows' "$AGLOG" | grep -oE '^[0-9]+')" 8
1908|     check     "autodev generator: offline verdict" \
1909|               "$(grep -c 'AUTODEV_GEN_PASS' "$AGLOG")" "1"
1910|     #  Named rows. The two mutants are what make the ordered-list assertion
1911|     #  load-bearing rather than decorative, so deleting either must be loud.
1912|     check     "autodev generator: the ordered devinit list is asserted" \
1913|               "$(grep -c 'devinit names == the .DEVINIT( declarations, in order' "$AGLOG")" "1"
1914|     check     "autodev generator: the full-revert mutant is present" \
1915|               "$(grep -c 'MUTANT killed: full revert' "$AGLOG")" "1"
1916|     check     "autodev generator: the HALF-FIX mutant is present" \
1917|               "$(grep -c 'MUTANT killed: noglob only' "$AGLOG")" "1"
1918|     #  If somebody rewords dev_rs5c313.c:144 the mutant lane stops proving
1919|     #  anything, so the driver asserts that live input still exists and this row
1920|     #  makes that assertion visible at gate level too.
1921|     check     "autodev generator: a live off-anchor mention still exists" \
1922|               "$(grep -c 'a live off-anchor DEVINIT mention still exists' "$AGLOG")" "1"
1923|     #  No mutant may SURVIVE. Named separately from the failure count because a
1924|     #  survivor is a statement about the DETECTOR, not about the generator.
1925|     check     "autodev generator: no mutant survives" \
1926|               "$(grep -c 'SURVIVES' "$AGLOG")" "0"
1927| fi
~~~~

### 8.7 What else covers a regress driver (S20): GATE 2's self-variant manifest loop (HEAD) and `check_probe_wiring.py`'s domain note (HEAD)
~~~~
1153| SM_EXEMPT="ieee_store:2099-01-01"   # #537: fbpending_bound moved to SM_COVERED
1154| sm_missing=""
1155| for f in "$HERE"/diff_*.c; do
1156|     stem=$(basename "$f" .c); stem=${stem#diff_}
1157|     #  Match the STEM, not the whole token: exemptions now carry ":date" suffixes, and a
1158|     #  substring match against the raw string would silently accept a stem that is merely a
1159|     #  prefix of another one.
1160|     _found=no
1161|     for _c in $SM_COVERED; do [ "$_c" = "$stem" ] && _found=yes; done
1162|     for _e in $SM_EXEMPT; do [ "${_e%%:*}" = "$stem" ] && _found=yes; done
1163|     [ "$_found" = yes ] || sm_missing="$sm_missing $stem"
1164| done
1165| check "selfmutant manifest: every differential is covered or dated-exempt" \
1166|       "${sm_missing:-none}" "none"
~~~~
~~~~
1247|     #  `domain()' is `.py'-ONLY BY CONSTRUCTION: it runs `git ls-files -- "*.py"' and filters
1248|     #  `f.endswith(".py")' twice more.  A `.sh' path can therefore NEVER be in the domain, so a
1249|     #  `.sh' manifest entry is reported GHOST *no matter what* -- staging does not clear it and
1250|     #  committing does not clear it.  Measured: all three were `git add'ed, `git ls-files' lists
~~~~

---

## 9. THE MEASUREMENTS -- VERBATIM, each with its artifact path (`regress/artifacts/m88kscaledbyte/table1_20261022/` unless stated)

Every `.out` cited below ends with its completion sentinel (`M88KLS_DONE`, `..._DONE`), checked by the drafter with
`tail -1` (R19).

### 9.1 `BUILD_REPORT.md` -- the builder's report
~~~~
  1| # T1 (`m88kscaledbyte`), round `#569` -- builder's report (resumed 2026-10-23; HEAD `5986c137`, unchanged throughout)
  2| 
  3| Spec: `pass1_20261022/BUILD_SPEC.md` sections 3-9, plus three mid-task additions from the coordinator: L8
  4| (`ollama_deepseek_t1p1_Q34.txt:20-21`) and the GPT-6 Astra pass-1 adjudication (`pass1_20261022/adj/codex_t1p1adj.txt`,
  5| verdict AMEND, the repair UPHELD).  No git write of any kind was made; nothing under `tools/` was edited; the peer's
  6| files were not touched.  Pass 2 is the main loop's.  Every number below names the file that holds it.
  7| 
  8| ## 1. What was done, in order
  9| | when (10-23) | step | receipt |
 10| |---|---|---|
 11| | 10-22 23:40-23:45 | steps 2.1-2.3 by the previous builder, REUSED unchanged after checking them against the source and the packet: HEAD md5s in five trees, fresh `generate_m88k_loadstore` output == committed table at HEAD (CHECKS #6 discharged), 296 NULL / 512 / 198 | `BASELINE.out`, `PRETABLE.out` |
 12| | 09:40 | L8 prediction written before any table run | `PRETABLE_L8.out` |
 13| | 09:4x | driver v1 + GATE 2 block v1 (identical insertion into the working-tree file and a staged HEAD copy); a shake-down against scratch HEAD copies (construction, not recorded) | `driver_v1/` |
 14| | 09:46:19 | step 4, pre-fix RED: v1 on unmodified HEAD (repo defaults), `ROWS=122 FAIL=50`: the 24 name pins in both artifacts (all `NULL`) and both NULL counts (296); the rest green, `cmp` identical | `driver_v1/prefix_HEAD.out` (+ `.meta`) |
 15| | 09:46:58, 09:47:51 | step 5: the generator fix (`#569`); the table regenerated from it in `/tmp/gxt1/fix` and copied over the repo's -- exactly 24 changed lines, each `NULL` -> the design name at a pinned index, 512 entries, 272 NULL, LF | `FIX.out` |
 16| | 09:47-09:51 | v1: `fixed.out` 122/0; legs L1-L8, L5b, S1, all equal to PRETABLE's predicted red sets row by row; v2 = v1 + the clause-(c) record comment (5 lines), every v1 run reproduced byte-identically by v2 | `driver_v1/SCORES.txt`, `driver_v1/RERUN_v2.txt`, `driver_v1/driver_v1_to_v2.diff` |
 17| | 09:53-09:54 | step 7 begun: `est/` propagated; `build/` rebuilt | `CLEARANCE.out` |
 18| | 09:55-10:02 | the adjudication applied: v1 receipts moved to `driver_v1/` (mtimes kept); driver v3; GATE 2 block v3; `PRETABLE_v3.out` written at 10:02:21, before any v3 run | `driver_v2_to_v3.diff`, `PRETABLE_v3.out`, `staged/` |
 19| | 10:03 | the v3 table, 16 runs, ONE instrument (driver md5 `cc2f3cf1...` checked before every run); every measured red set == its predicted set, row by row, and every output carries all 123 identities exactly once | `RUNS.log`, `SCORES.txt` |
 20| | 10:03 | L7's duplicate definition names, measured outside the driver | `DUPNAMES.out` |
 21| | 10:04-10:07 | `build-asan/` and `/tmp/gxsec-build` rebuilt; the two-part clearance re-run over all four trees | `CLEARANCE.out` |
 22| | 10:09-10:12 | GATE 2 alone (`run.sh 2`): PASS (502 checks), REGRESS_PASS | `GATE2_tail.out`, `GATE2_diff_m88k_loadstore_gen.log` |
 23| | 10:12-10:17 | GATE 11 alone (`run.sh 11`) on the rebuilt `build/gxemul`: PASS (111 checks), REGRESS_PASS | `GATE11_tail.out` |
 24| 
 25| ## 2. Diff stat -- the four repo files (plain `diff` against `git show HEAD:<file>`; all LF)
 26| | file | + | - | |
 27| |---|---|---|---|
 28| | `src/cpus/generate_m88k_loadstore.c` | 8 | 4 | the whole arm at HEAD `:254-257` removed, the `#569` comment in its place; `:104-105` untouched |
 29| | `src/cpus/tmp_m88k_loadstore.c` | 24 | 24 | regenerated, never hand-edited (`FIX.out`) |
 30| | `regress/diff_m88k_loadstore_gen.sh` | 276 | 0 | NEW, untracked -- **must be added with mode 100755** (the gate tests `-x`; `core.fileMode=false` here, and WSL shows rwx regardless) |
 31| | `regress/gate_offline.sh` | 45 | 0 | the block after the `#375` block; commit `staged/gate_offline.sh` (= HEAD + this hunk). The working-tree file = the same hunk + the foreign hunks untouched (`staged/insert_HEAD.diff` and `staged/insert_WT.diff` add identical lines at the same position, nothing removed) |
 32| 
 33| `est/` holds byte-identical copies of the two `src/` files (precommit section A).
 34| 
 35| ## 3. The detector as built (driver v3, the file to commit)
 36| * **The 24 output cells vs the 16 consumer cells.**  All 24 repaired cells are the FLOOR (adjudication B8: `main()`'s
 37|   loops emit all 24), pinned by absolute name in both artifacts.  16 are today's guest-consumer subset, marked
 38|   `(consumer)` (160 164 168 176 180 184 224 228 232 240 244 248 416 420 432 436); the 8 others are marked
 39|   `(no consumer)`, which is a fact about today's callers, not a weaker pin.
 40| * **Rows: 123** = 4 generator status rows (`gen_compiles`, `gen_exit`, `gen_stdout` -- new, B5 --, `gen_count`) + 2
 41|   artifacts x (5 structural + **54 distinct name pins**) + 1 `cmp`.  54 = 24 repairs + 24 counterparts + 6 further
 42|   accepts; the three counterparts that are also accepts (144 400 404) are emitted ONCE, as accept rows.
 43| * Every row's first field is an identity that occurs exactly once in the output; GATE 2 pins each of the 123 from its
 44|   OWN index lists (`== 1`), plus `ROWS == 123`, `FAIL == 0` and the `M88KLS_DONE` sentinel.
 45| * Halfword accept 161/177 warranted by R12 (B3); `LS_N`/`generated_functions == 198` stated as a narrow suppression-
 46|   count control, not definition integrity (B4); the header's NOT-OBSERVED list names handler bodies and the xmem
 47|   exchange (the BLOCKED witness record) and the generated definitions beyond their count.
 48| 
 49| ## 4. Scores (every one from its artifact; v3, 123 rows; `SCORES.txt` compares each red set row by row)
 50| | run | red/rows | artifact | what it is |
 51| |---|---|---|---|
 52| | PRE | 50/123 | `prefix_HEAD_v3.out` | clause (a) on the HEAD blobs through the overrides (see D-4) |
 53| | FIX | 0/123 | `fixed.out` | the fixed repo files, repo defaults |
 54| | L1 | 26/123 | `L1_headgen.out` | clause (b) at the generator site |
 55| | L2 | 26/123 | `L2_headtable.out` | clause (b) at the table site |
 56| | L3 | 64/123 | `L3_commentgen.out` | clause (c), measured: comment-only generator |
 57| | L4 | 60/123 | `L4_commenttable.out` | clause (c), measured: comment-only table |
 58| | L5 | 14/123 | `L5_v2nopcsync.out` | clause (d): `grok_t1p1.txt:76`'s v2, first difference 416 |
 59| | L6 | 14/123 | `L6_lehalf.out` | clause (d): the little-endian half left as before the fix |
 60| | L7 | 3/123 | `L7_v6halfword.out` | accept edge: 161/177 red, word pins green; NOT silent -- 24 duplicated `#define LS_N` names (`DUPNAMES.out`) |
 61| | L8 | 56/123 | `L8_allnull.out` | SUPPLEMENTARY: all-NULL initializer (the coordinator's 24 pins + accepts + NULL count, and also the 21 committed counterparts) |
 62| | L5b | 30/123 | `L5b_codexnopcsync.out` | SUPPLEMENTARY only: `codex_t1p1.txt:100`'s different predicate (first overall difference 256) -- not L5 |
 63| | S1 | 3/123 | `S1_noearlyreturn.out` | SUPPLEMENTARY (B4 control): `:104-105` deleted, `gen_count` and `fresh_lsn` 210 |
 64| | S2 | 1/123 | `S2_exit1.out` | SUPPLEMENTARY (B5): exit 1 -> `gen_exit` only |
 65| | S3 | 62/123 | `S3_emptyout.out` | SUPPLEMENTARY (B5): exit 0, empty stdout -> `gen_stdout` and every fresh row |
 66| | S4 | 60/123 | `S4_notable.out` | SUPPLEMENTARY (B5): table absent -> red, not a skip |
 67| | S5 | 64/123 | `S5_nogen.out` | SUPPLEMENTARY (B5): generator absent -> red, not a skip |
 68| 
 69| The variant of each leg is a file only: `L<n>.diff` / `S<n>.diff` (S4/S5 are absent paths, no diff).  The v1 table
 70| (122 rows: PRE 50, FIX 0, L1 26, L2 26, L3 63, L4 60, L5 14, L6 14, L7 3, L8 56, L5b 30, S1 3) is in `driver_v1/`.
 71| **(c): measured at** `L3_commentgen.out` and `L4_commenttable.out` (first by v1: `driver_v1/L3_commentgen.out`
 72| 63/122, `driver_v1/L4_commenttable.out` 60/122); L8 is supplementary, not a prerequisite.
 73| 
 74| ## 5. Clearance (`CLEARANCE.out`, run 10:07:46 over all four trees; neither file is in the derived divergence set)
 75| ```
 76| est         part 1 CLEAN, CLEAN      part 2  est/: source tree, part 2 N/A (no binary exists)
 77| build       part 1 CLEAN, CLEAN      part 2  [ gxemul -nt generator ] yes, [ gxemul -nt table ] yes   (gxemul 09:54:12)
 78| build-asan  part 1 CLEAN, CLEAN      part 2  yes, yes                                                 (gxemul 10:06:40)
 79| gxsec-build part 1 CLEAN, CLEAN      part 2  yes, yes                                                 (gxemul 10:07:16)
 80| ```
 81| In each build tree make itself re-ran `./generate_m88k_loadstore > tmp_m88k_loadstore.c` (once, shown by its log
 82| line) and the in-tree table then `cmp`s CLEAN against GXEMUL-SEC's: the agreement row, measured in a real build.
 83| `rm src/cpus/*.o; make -j8`, rc 0, no `.MUTANT` anywhere, no concurrent job.
 84| 
 85| ## 6. Gates (each once, alone, `bash regress/run.sh <n>`, LOGDIR = lib.sh default `/tmp/gxregress`)
 86| * **GATE 2** `offline-differential: PASS (502 checks)`, `REGRESS_PASS`, rc 0, 171 s.  The #569 block's 126 checks all
 87|   ok; 0 gate-level FAIL rows; 502 = the last battery's 376 + 126.  The gate-side driver log is byte-identical to
 88|   `fixed.out`.
 89| * **GATE 11** `gate 11: m88k rounding mode (#298): PASS (111 checks)`, `REGRESS_PASS`, rc 0, 247 s, binary
 90|   `build/gxemul` (09:54:12).  111 = the last battery's count.
 91| Both measured the WORKING TREE (see D-10).
 92| 
 93| ## 7. What disagreed with the spec or a ruling (by id), and deviations
 94| * **D-1 (BUILD_SPEC section 6, L5; B7).**  The spec's L5 pointer named `grok_t1p1.txt:76` and `codex_t1p1.txt:100`,
 95|   which are two different predicates (first differences 416 and 256).  The adjudication (B7) resolved L5 to Grok's;
 96|   Codex's is kept only as the labelled supplementary L5b.
 97| * **D-2 (B8; PRETABLE.out section 0).**  The 16-floor / 8-clause-(e) split is superseded: all 24 are floor; 16 is the
 98|   consumer subset.  PRETABLE.out is left as written; `PRETABLE_v3.out` records the change.
 99| * **D-3 (B3, B4, B5, B10, B12).**  Applied as the adjudication amended them (section 3).  B10's per-identity pins raise
100|   GATE 2 from 376 to 502 checks; nothing in `tools/` or `regress/` pins that count (searched).
101| * **D-4 (BUILD_SPEC section 4).**  v3's pre-fix run (`prefix_HEAD_v3.out`) went through the GEN/TABLE overrides on the
102|   byte-exact HEAD blobs AFTER the step-5 edit, because the adjudication arrived after the fix.  The authentic
103|   pre-edit-dated receipt is `driver_v1/prefix_HEAD.out` (09:46:19, before the 09:46:58 generator edit).  The repo
104|   was not reverted to re-date it.
105| * **D-5 (PRETABLE.out, two small inaccuracies, not rewritten).**  Section 5 predicted `0` for L3's fresh LS_N row and the
106|   driver reports `absent` (red either way).  Section 1 says "four sites index unguarded" while listing three; the
107|   fourth, the immediate form at `cpu_m88k_instr.c:3087`, cannot form a scaled index.
108| * **D-6 (supplementary legs beyond the spec).**  L5b and S1 (from PRETABLE.out), S2-S5 (added for the B5 rows).
109| * **D-7 (section 7).**  `make -j8`, one make job, instead of a plain `make`.
110| * **D-8 (coordinator's L8 expectation).**  The measured red set also includes the 21 committed-side counterpart rows
111|   (all NULL by construction): 56, as `PRETABLE_L8.out` predicted.
112| * **D-9 (placement, observation).**  The block sits before `gate_offline.sh`'s compiler check, as specified.  On a host
113|   with no C compiler it reds via `gen_compiles` (B5's explicit red), and the gate's later "no C compiler" `gate_skip`
114|   then reports FAIL, not SKIP (`lib.sh`: a skip after failures is a FAIL).
115| * **D-10 (trees).**  The five peer files are uncommitted in GXEMUL-SEC and byte-identical in every build tree (already
116|   compiled into the old binaries); `rm src/cpus/*.o` recompiled `cpu_alpha` with the peer's `cpu_alpha_palcode.c` as it
117|   stands.  Both gates therefore measured the working tree, `gate_offline.sh`'s foreign hunks included.
118| * **C1 / C2:** filed outside T1 only (adjudication C1/C2); nothing here touches them.  The adjudication's corrections
119|   to PASS1_RULINGS (roster line) and CHECKS #4/#6/#7 are records work for the main loop.  CHECKS #6 is discharged by
120|   `BASELINE.out` section 3.
121| 
122| ## 8. Open questions for the main loop
123| 1. Is the post-edit v3 pre-fix run (D-4) acceptable beside the v1 pre-edit receipt?
124| 2. 123 individual identity checks (as amended) or one aggregated check that names any failing identity?  (Each adds
125|    one gate line; GATE 2 now prints 123 more.)
126| 3. The helper scripts (variant builder, runners, scorer) live only in the session scratchpad
127|    `t1/build/`.  Any `.py` copied under `regress/artifacts/` needs a `check_probe_wiring.py` MANIFEST line.  The diff
128|    files already specify every variant.
129| 4. The Fable stage is HELD (`fable5.HELD.txt`), so the rulings this build follows are provisional on their face.
130| 
131| BUILD_REPORT_DONE
~~~~

### 9.2 `SCORES.txt` -- each run's MEASURED red set against PRETABLE_v3's prediction
~~~~
  1| # SCORES.txt -- T1 / #569, the driver-v3 table (2026-10-23).  Each run's MEASURED red set against the set
  2| # PRETABLE_v3.out predicted (written 10:02:21, before any v3 run), row by row, by row IDENTITY; and the gate-2
  3| # identity check replayed on each output.  Generated by scratchpad t1/build/score3.py from the .out files below;
  4| # the runs (driver md5, GEN/TABLE path + md5, rc, last line) are in RUNS.log.  The v1 table (122 rows) and its
  5| # scores are kept in driver_v1/ -- including the authentic pre-edit receipt driver_v1/prefix_HEAD.out.
  6| #
  7| # ROW TOTAL 123 = 4 generator status rows (gen_compiles gen_exit gen_stdout gen_count) + 2 artifacts x (5
  8| # structural + 54 DISTINCT NAME PINS) + 1 cmp.  54 = 24 repairs + 24 counterparts + 6 further accepts; the three
  9| # counterparts that are also accepts (144 400 404) are emitted ONCE, as accept rows (so 21 counterpart rows).
 10| # The 24 repairs are ALL floor; 16 are the current guest-consumer subset (160 164 168 176 180 184 224 228 232 240 244 248 416 420 432 436).
 11| 
 12| run  red/rows artifact                pred  match   ids once  role -- reason the red is the reason under test
 13| PRE   50/123  prefix_HEAD_v3.out      50    YES     123/123   (a) -- the HEAD blobs: the 24 repaired slots are NULL in BOTH artifacts (296 NULLs); fresh == committed holds
 14| FIX    0/123  fixed.out               0     YES     123/123   -- -- the fixed generator and the regenerated table (repo defaults, as gate 2 runs it): every row green
 15| L1    26/123  L1_headgen.out          26    YES     123/123   (b) gen site -- HEAD's generator re-emits NULL at the 24 slots; the committed (fixed) table stays green; cmp differs
 16| L2    26/123  L2_headtable.out        26    YES     123/123   (b) table site -- HEAD's table carries NULL at the 24 slots; the fresh (fixed) output stays green; cmp differs
 17| L3    64/123  L3_commentgen.out       64    YES     123/123   (c) measured -- comment-only generator source: no main(), the link fails -> compile, exit, stdout, count rows and every fresh row red
 18| L4    60/123  L4_commenttable.out     60    YES     123/123   (c) measured -- comment-only table: no initializer -> every committed-side row red; the generator side green
 19| L5    14/123  L5_v2nopcsync.out       14    YES     123/123   (d) -- grok_t1p1.txt:76's v2 -- the arm re-introduced under `&& no_pc_sync`: the 12 no-PC-sync repairs NULL, first at 416
 20| L6    14/123  L6_lehalf.out           14    YES     123/123   (d) -- the arm re-introduced on the LITTLE-endian half only (glm Q12:52): the 12 LE repairs NULL, BE repairs green
 21| L7     3/123  L7_v6halfword.out       3     YES     123/123   accept (R12) -- the `size > 0` in print_function_name -> `size > 1` (grok :80 / codex :130): 161/177 lose `_scaled`; word pins green; NOT silent -- see DUPNAMES.out
 22| L8    56/123  L8_allnull.out          56    YES     123/123   suppl. medium -- all-NULL initializer, structure kept (deepseek Q34:20): every committed NAME row and the count red, structure green
 23| L5b   30/123  L5b_codexnopcsync.out   30    YES     123/123   suppl. only -- NOT L5: codex_t1p1.txt:100's predicate (no_pc_sync alone, after the exclusions), first overall difference 256
 24| S1     3/123  S1_noearlyreturn.out    3     YES     123/123   suppl. B4 -- loadstore()'s kept early return deleted: 12 more blocks -> gen_count and fresh_lsn 210; every name pin green
 25| S2     1/123  S2_exit1.out            1     YES     123/123   suppl. B5 -- the generator exits 1 after printing the whole table: gen_exit red, nothing else
 26| S3    62/123  S3_emptyout.out         62    YES     123/123   suppl. B5 -- the generator returns before printing anything (exit 0): gen_stdout red, and every fresh row
 27| S4    60/123  S4_notable.out          60    YES     123/123   suppl. B5 -- TABLE names an absent file: committed_present 'absent' and every committed row red -- not a skip
 28| S5    64/123  S5_nogen.out            64    YES     123/123   suppl. B5 -- GEN names an absent file: gen_compiles 'no -- source absent', every generator and fresh row red -- not a skip
 29| 
 30| ALL RUNS: measured red set == predicted, the same 123 identities, each once, sentinel present: YES
 31| 
 32| ## clause (c), in the record form the carrier allows (adjudication B6: comment-only media; measured)
 33| (c): measured at regress/artifacts/m88kscaledbyte/table1_20261022/L3_commentgen.out (a comment-only generator
 34|      source: the compile row reds, and with it every generator-status and fresh-side row -- 64/123) and
 35|      .../L4_commenttable.out (a comment-only table: every committed-side row reds -- 60/123).  First measured by
 36|      driver v1 (driver_v1/L3_commentgen.out 63/122, driver_v1/L4_commenttable.out 60/122).  L8_allnull.out
 37|      (56/123) is SUPPLEMENTARY evidence with its own receipt, not a prerequisite for (c).
 38| 
 39| ## L7 is not silent (adjudication B3/B7): DUPNAMES.out -- its generator output carries 24 duplicated
 40| ## `#define LS_N` names (the 24 scaled-halfword definitions lose `_scaled`), S1's 12, HEAD and the fix 0.  The driver
 41| ## does not compile the generated file, so the table-token difference at 161/177 is this detector's observable.
 42| 
 43| ## per run: the measured red set, and the got= values of the status, structural and edge rows that went red
 44| PRE  prefix_HEAD_v3.out  sentinel present  ROWS=123 FAIL=50
 45|     measured red: committed_nulls; committed_pin[24: 160 164 168 176 180 184 224 228 232 240 244 248 416 420 424 432 436 440 480 484 488 496 500 504]; fresh_nulls; fresh_pin[24: 160 164 168 176 180 184 224 228 232 240 244 248 416 420 424 432 436 440 480 484 488 496 500 504]
 46|     fresh_nulls          got=296
 47|     committed_nulls      got=296
 48|     fresh_pin160         got=NULL
 49|     fresh_pin416         got=NULL
 50|     committed_pin160     got=NULL
 51| FIX  fixed.out  sentinel present  ROWS=123 FAIL=0
 52|     measured red: (none)
 53| L1  L1_headgen.out  sentinel present  ROWS=123 FAIL=26
 54|     measured red: cmp_fresh_committed; fresh_nulls; fresh_pin[24: 160 164 168 176 180 184 224 228 232 240 244 248 416 420 424 432 436 440 480 484 488 496 500 504]
 55|     fresh_nulls          got=296
 56|     cmp_fresh_committed  got=differ
 57|     fresh_pin160         got=NULL
 58|     fresh_pin416         got=NULL
 59| L2  L2_headtable.out  sentinel present  ROWS=123 FAIL=26
 60|     measured red: cmp_fresh_committed; committed_nulls; committed_pin[24: 160 164 168 176 180 184 224 228 232 240 244 248 416 420 424 432 436 440 480 484 488 496 500 504]
 61|     committed_nulls      got=296
 62|     cmp_fresh_committed  got=differ
 63|     committed_pin160     got=NULL
 64| L3  L3_commentgen.out  sentinel present  ROWS=123 FAIL=64
 65|     measured red: cmp_fresh_committed; fresh_acc[9: 144 161 177 400 404 418 422 434 438]; fresh_cp[21: 128 132 136 148 152 192 196 200 208 212 216 384 388 392 408 448 452 456 464 468 472]; fresh_entries; fresh_inits; fresh_lsn; fresh_nulls; fresh_pin[24: 160 164 168 176 180 184 224 228 232 240 244 248 416 420 424 432 436 440 480 484 488 496 500 504]; fresh_present; gen_compiles; gen_count; gen_exit; gen_stdout
 66|     gen_compiles         got=no -- the compile or link failed
 67|     gen_exit             got=not run
 68|     gen_stdout           got=not run
 69|     gen_count            got=absent
 70|     fresh_present        got=absent
 71|     fresh_entries        got=0
 72|     fresh_nulls          got=0
 73|     fresh_lsn            got=absent
 74|     cmp_fresh_committed  got=fresh output absent
 75|     fresh_acc161         got=
 76|     fresh_acc177         got=
 77|     fresh_pin160         got=
 78|     fresh_pin416         got=
 79| L4  L4_commenttable.out  sentinel present  ROWS=123 FAIL=60
 80|     measured red: cmp_fresh_committed; committed_acc[9: 144 161 177 400 404 418 422 434 438]; committed_cp[21: 128 132 136 148 152 192 196 200 208 212 216 384 388 392 408 448 452 456 464 468 472]; committed_entries; committed_inits; committed_lsn; committed_nulls; committed_pin[24: 160 164 168 176 180 184 224 228 232 240 244 248 416 420 424 432 436 440 480 484 488 496 500 504]; committed_present
 81|     committed_present    got=no m88k_loadstore[512] initializer
 82|     committed_entries    got=0
 83|     committed_nulls      got=0
 84|     committed_lsn        got=0
 85|     cmp_fresh_committed  got=differ
 86|     committed_pin160     got=
 87| L5  L5_v2nopcsync.out  sentinel present  ROWS=123 FAIL=14
 88|     measured red: cmp_fresh_committed; fresh_nulls; fresh_pin[12: 416 420 424 432 436 440 480 484 488 496 500 504]
 89|     fresh_nulls          got=284
 90|     cmp_fresh_committed  got=differ
 91|     fresh_pin416         got=NULL
 92| L6  L6_lehalf.out  sentinel present  ROWS=123 FAIL=14
 93|     measured red: cmp_fresh_committed; fresh_nulls; fresh_pin[12: 160 164 168 224 228 232 416 420 424 480 484 488]
 94|     fresh_nulls          got=284
 95|     cmp_fresh_committed  got=differ
 96|     fresh_pin160         got=NULL
 97|     fresh_pin416         got=NULL
 98| L7  L7_v6halfword.out  sentinel present  ROWS=123 FAIL=3
 99|     measured red: cmp_fresh_committed; fresh_acc[2: 161 177]
100|     cmp_fresh_committed  got=differ
101|     fresh_acc161         got=m88k_instr_ld_u_2_le_regofs
102|     fresh_acc177         got=m88k_instr_ld_u_2_be_regofs
103| L8  L8_allnull.out  sentinel present  ROWS=123 FAIL=56
104|     measured red: cmp_fresh_committed; committed_acc[9: 144 161 177 400 404 418 422 434 438]; committed_cp[21: 128 132 136 148 152 192 196 200 208 212 216 384 388 392 408 448 452 456 464 468 472]; committed_nulls; committed_pin[24: 160 164 168 176 180 184 224 228 232 240 244 248 416 420 424 432 436 440 480 484 488 496 500 504]
105|     committed_nulls      got=512
106|     cmp_fresh_committed  got=differ
107|     committed_pin160     got=NULL
108| L5b  L5b_codexnopcsync.out  sentinel present  ROWS=123 FAIL=30
109|     measured red: cmp_fresh_committed; fresh_acc[6: 400 404 418 422 434 438]; fresh_cp[10: 384 388 392 408 448 452 456 464 468 472]; fresh_nulls; fresh_pin[12: 416 420 424 432 436 440 480 484 488 496 500 504]
110|     fresh_nulls          got=392
111|     cmp_fresh_committed  got=differ
112|     fresh_pin416         got=NULL
113| S1  S1_noearlyreturn.out  sentinel present  ROWS=123 FAIL=3
114|     measured red: cmp_fresh_committed; fresh_lsn; gen_count
115|     gen_count            got=210
116|     fresh_lsn            got=210
117|     cmp_fresh_committed  got=differ
118| S2  S2_exit1.out  sentinel present  ROWS=123 FAIL=1
119|     measured red: gen_exit
120|     gen_exit             got=1
121| S3  S3_emptyout.out  sentinel present  ROWS=123 FAIL=62
122|     measured red: cmp_fresh_committed; fresh_acc[9: 144 161 177 400 404 418 422 434 438]; fresh_cp[21: 128 132 136 148 152 192 196 200 208 212 216 384 388 392 408 448 452 456 464 468 472]; fresh_entries; fresh_inits; fresh_lsn; fresh_nulls; fresh_pin[24: 160 164 168 176 180 184 224 228 232 240 244 248 416 420 424 432 436 440 480 484 488 496 500 504]; fresh_present; gen_count; gen_stdout
123|     gen_stdout           got=no -- stdout empty
124|     gen_count            got=not reported
125|     fresh_present        got=no m88k_loadstore[512] initializer
126|     fresh_entries        got=0
127|     fresh_nulls          got=0
128|     fresh_lsn            got=0
129|     cmp_fresh_committed  got=differ
130|     fresh_acc161         got=
131|     fresh_acc177         got=
132|     fresh_pin160         got=
133|     fresh_pin416         got=
134| S4  S4_notable.out  sentinel present  ROWS=123 FAIL=60
135|     measured red: cmp_fresh_committed; committed_acc[9: 144 161 177 400 404 418 422 434 438]; committed_cp[21: 128 132 136 148 152 192 196 200 208 212 216 384 388 392 408 448 452 456 464 468 472]; committed_entries; committed_inits; committed_lsn; committed_nulls; committed_pin[24: 160 164 168 176 180 184 224 228 232 240 244 248 416 420 424 432 436 440 480 484 488 496 500 504]; committed_present
136|     committed_present    got=absent
137|     committed_entries    got=0
138|     committed_nulls      got=0
139|     committed_lsn        got=absent
140|     cmp_fresh_committed  got=committed table absent
141|     committed_pin160     got=
142| S5  S5_nogen.out  sentinel present  ROWS=123 FAIL=64
143|     measured red: cmp_fresh_committed; fresh_acc[9: 144 161 177 400 404 418 422 434 438]; fresh_cp[21: 128 132 136 148 152 192 196 200 208 212 216 384 388 392 408 448 452 456 464 468 472]; fresh_entries; fresh_inits; fresh_lsn; fresh_nulls; fresh_pin[24: 160 164 168 176 180 184 224 228 232 240 244 248 416 420 424 432 436 440 480 484 488 496 500 504]; fresh_present; gen_compiles; gen_count; gen_exit; gen_stdout
144|     gen_compiles         got=no -- source absent
145|     gen_exit             got=not run
146|     gen_stdout           got=not run
147|     gen_count            got=absent
148|     fresh_present        got=absent
149|     fresh_entries        got=0
150|     fresh_nulls          got=0
151|     fresh_lsn            got=absent
152|     cmp_fresh_committed  got=fresh output absent
153|     fresh_acc161         got=
154|     fresh_acc177         got=
155|     fresh_pin160         got=
156|     fresh_pin416         got=
157| 
158| SCORES_DONE
~~~~

### 9.3 `PRETABLE_v3.out` -- the v3 row set and predictions, written at 10:02:21, before any v3 run
~~~~
  1| # PRETABLE_v3.out -- T1 / #569, ADDENDUM 2 to PRETABLE.out: the row set and the predictions for driver v3.
  2| # Written 2026-10-23 by the resuming builder BEFORE any run of driver v3 (no shake-down either): this file's mtime
  3| # is the order discriminator for every v3 prediction below.  PRETABLE.out and PRETABLE_L8.out stand unchanged.
  4| # Cause: the pass-1 adjudication, pass1_20261022/adj/codex_t1p1adj.txt (GPT-6 Astra, verdict AMEND; the repair is
  5| # UPHELD -- A1-A6), relayed by the coordinator.  The v1 table (122 rows) is preserved in driver_v1/, including the
  6| # authentic pre-edit prefix_HEAD.out (09:46:19, before the generator edit at 09:47).
  7| # Everything below about a leg's outcome is a PREDICTION; SCORES.txt compares the measured sets against it.
  8| 
  9| ## 1. The v3 row list against PRETABLE.out section 0's PRESCRIBED rows (the diff the carrier requires when a row
 10| ##    list is rewritten from a panel's findings: nothing prescribed may silently vanish)
 11|   PRETABLE.out                              driver v3 identity (first field of each row)
 12|   G1 generator compiles                 ->  gen_compiles
 13|   G2 generator runs (exit 0)            ->  gen_exit
 14|   (new, adjudication B5)                ->  gen_stdout          stdout non-empty: execution success is explicit
 15|   G3 stderr generated_functions == 198  ->  gen_count
 16|   A1 present and parseable              ->  <a>_present         <a> = fresh | committed
 17|   A2 m88k_loadstore[512] initializers   ->  <a>_inits
 18|   A3 initializer entries == 512         ->  <a>_entries
 19|   A4 NULL entries == 272                ->  <a>_nulls           supplementary, unchanged
 20|   A5 #define LS_N blocks == 198         ->  <a>_lsn             relabelled "(suppression count)" (adjudication B4)
 21|   A6 pin <i> F / E  x24                 ->  <a>_pin<i>          F -> "(consumer)", E -> "(no consumer)": ALL 24 FLOOR
 22|   A7 accept <i>  x9                     ->  <a>_acc<i>          same 9 indices, same names
 23|   A8 cpart <i>  x21                     ->  <a>_cp<i>           same 21 indices, same names
 24|   X1 fresh == committed (cmp)           ->  cmp_fresh_committed
 25|   Prescribed rows DROPPED: none.  Rows ADDED: gen_stdout.  Expected names: the 54 index->name pairs are
 26|   byte-identical to v1/v2's spec block (checked mechanically before this file was written).
 27|   TOTAL = 4 + 2 x (5 + 54) + 1 = 123 (v1: 122).  54 = 24 repairs + 24 counterparts + 6 further accepts; the three
 28|   counterparts that are also accepts (144 400 404) are emitted ONCE, as accept rows.
 29|   Every row carries an identity that occurs exactly once; gate 2 holds its OWN list of the 123 identities and pins
 30|   each at == 1, beside ROWS == 123, FAIL == 0 and the M88KLS_DONE sentinel.
 31| 
 32| ## 2. Reclassifications the adjudication made, as they now read in the contract header
 33|   * FLOOR = all 24 generator-output cells (B8): main()'s loops emit all 24, so an escape at any is a floor breach.
 34|     16 are the current GUEST-CONSUMER subset (160 164 168 176 180 184 224 228 232 240 244 248 416 420 432 436); the
 35|     8 others (424 440 480 484 488 496 500 504) are NOT coverage debt.  PRETABLE.out section 0's F/E split and its
 36|     "(e)" wording for the 8 are superseded by this.
 37|   * Halfword accept 161/177: warranted by R12 (the de-escalation rule's adjacent modelled size), not by D2 (B3).
 38|   * LS_N == 198 / generated_functions == 198: a narrow suppression-count control, NOT a definition-integrity check.
 39|   * L5 = grok_t1p1.txt:76 exactly (first difference 416).  codex_t1p1.txt:100's predicate (first overall difference
 40|     256) is NOT L5; it stays in the table only as the separately labelled supplementary leg L5b.
 41|   * L7 is not "silent": the same printer names the generated definitions, so it also produces duplicate definition
 42|     NAMES, which this driver does not compile; its table-token difference is the observable.  PREDICTED here, to be
 43|     measured outside the driver: L7's own generator output carries 24 duplicated `#define LS_N` names (the 24
 44|     scaled-halfword definitions lose `_scaled` and collide with the unscaled ones); the fixed generator 0; S1's 12.
 45|   * L8 (all-NULL table) is SUPPLEMENTARY evidence with its own receipt, not a prerequisite for clause (c).
 46| 
 47| ## 3. Supplementary legs added for the B5 rows (execution success, missing inputs), by id only
 48|   S2  GEN = the fixed generator with main()'s final `return 0;` -> `return 1;`        exit status non-zero
 49|   S3  GEN = the fixed generator with `return 0;` before main()'s first printf          exit 0, stdout empty
 50|   S4  TABLE = a path that does not exist                                               missing committed table
 51|   S5  GEN = a path that does not exist                                                 missing generator source
 52| 
 53| ## 4. Predicted red sets for driver v3 (rows red of 123)
 54|   PRE  (HEAD blobs via GEN/TABLE)  50   fresh_pin x24, committed_pin x24, fresh_nulls, committed_nulls
 55|   FIX  (repo defaults)              0
 56|   L1   26   fresh_pin x24, fresh_nulls, cmp_fresh_committed
 57|   L2   26   committed_pin x24, committed_nulls, cmp_fresh_committed
 58|   L3   64   gen_compiles gen_exit gen_stdout gen_count, all 59 fresh_* rows, cmp_fresh_committed
 59|   L4   60   all 59 committed_* rows, cmp_fresh_committed
 60|   L5   14   fresh_pin{416 420 424 432 436 440 480 484 488 496 500 504}, fresh_nulls (284), cmp
 61|   L6   14   fresh_pin{160 164 168 224 228 232 416 420 424 480 484 488}, fresh_nulls (284), cmp
 62|   L7    3   fresh_acc161, fresh_acc177, cmp
 63|   L8   56   committed_pin x24, committed_acc x9, committed_cp x21, committed_nulls (512), cmp
 64|   L5b  30   fresh_pin (the 12 no-PC-sync), fresh_acc{400 404 418 422 434 438}, fresh_cp{384 388 392 408 448 452 456
 65|             464 468 472}, fresh_nulls (392), cmp
 66|   S1    3   gen_count (210), fresh_lsn (210), cmp
 67|   S2    1   gen_exit (1)
 68|   S3   62   gen_stdout ("no -- stdout empty"), gen_count ("not reported"), all 59 fresh_* rows, cmp
 69|   S4   60   all 59 committed_* rows (committed_present "absent"), cmp ("committed table absent")
 70|   S5   64   as L3, with gen_compiles reading "no -- source absent"
 71| 
 72| ## 5. CHANNEL for the changed rows (the rest as PRETABLE.out section 5)
 73|   gen_exit     S2 (1); L3/S5 ("not run")            -- the exit status
 74|   gen_stdout   S3 ("no -- stdout empty"); L3/S5 ("not run")   -- stdout emptiness
 75|   identities   any deleted or renamed row: its identity's count 0 at the gate; a duplicated row: 2.  Not a table leg
 76|                (the gate pins it); checked by construction when the gate block is read, and by the green GATE 2 run.
 77| 
 78| PRETABLE_V3_DONE
~~~~

### 9.4 `PRETABLE.out` -- the original pre-table check (written 2026-10-22 23:45, before the driver existed); PRETABLE_v3 is its addendum (EXCERPTS: the header, section 2 CLAIM -> ROW, section 3 GUARD vs BODY, section 5 CHANNEL; its sections 0, 1 and 4 -- the 122 prescribed rows, sibling parity, the leg list -- are carried forward by PRETABLE_v3 section 1 and SCORES; open the file for them)
~~~~
  1| # PRETABLE.out -- T1 / #569 (row m88kscaledbyte), the pre-table check (D2; carrier "THE PRE-TABLE CHECK", mandatory)
  2| # Written by the builder BEFORE the driver exists and BEFORE any table run (prefix_HEAD, fixed, L1-L7): this file's
  3| # mtime is the order discriminator.  HEAD 5986c137 (cb2eba1e + a gate_ab.sh-only commit; none of the in-scope files
  4| # changed -- BASELINE.out section 1).  Line numbers are HEAD's.  Everything below about a leg's outcome is a
  5| # PREDICTION; the measured outcome lands in SCORES.txt and is compared against this file there.
  ...
 60| ## 2. CLAIM -> ROW, for every sentence the #569 comment in the generator will assert
 61| (the comment replaces :254-257; its sentences, as they will be written:)
 62|   C1 "no NULL arm for scaled byte accesses"                 -> A6 (24 pins, both artifacts) and A4 (NULL == 272)
 63|   C2 "A byte's scale factor is 1, so a scaled byte access   -> NO ROW: an architecture statement the offline detector
 64|       is the unscaled one"                                     cannot observe; its warrant is mc88100.txt:2960-2965 and
 65|                                                                :6458-6460 (scale factor one for byte), cited in the
 66|                                                                CHANGELOG/report, not in product code
 67|   C3 "print_function_name() already omits "_scaled" for     -> A6: every expected pin name lacks "_scaled" (a size-0
 68|       size 0"                                                  "_scaled" name reds all 24); A7 161/177: the size-1 EDGE
 69|                                                                keeps "_scaled" (L7 moves that edge)
 70|   C4 "these 24 slots name the unscaled byte handlers"       -> A6 by absolute equality; A7/A8 pin the same 12 names
 71|                                                                independently at index-32 (relative row NOT used, B2)
 72|   C5 "They were NULL"                                       -> historical; its rows are the clause-(a) reds:
 73|                                                                prefix_HEAD.out (A6 x48 and A4 x2 red) and BASELINE.out
 74|                                                                section 5 (24 of 24 NULL at HEAD)
 75|   C6 "which xmem_slow() calls unguarded and the ld/st       -> NO ROW in this detector: a guest-path consequence (B11);
 76|       decoder installs as ic->f (cpu_m88k_instr.c)"            source-established (CHECKS #3, cpu_m88k_instr.c :2395,
 77|                                                                :2426, :3622; cpu_dyntrans.c :1906); the rung-3 witness
 78|                                                                is BLOCKED (witness_attempt_20261022/WITNESS_ATTEMPT.md)
 79| The driver header's contract sentences map to rows in the same way (section 5 below gives each row's mutant and channel);
 80| its "does NOT observe" sentences are deliberate no-row sentences (B11).
 81| 
 82| ## 3. GUARD FIELD vs BODY FIELD, with the partition the body induces on each lvalue (7n-5)
 83| 
 84| Guard (the deleted predicate) reads:  size, scaledness.
 85| Body (what the 24 cells run after the deletion: main :259-262 printf + print_function_name(size, store, signedness,
 86| endianness, scaledness, usr, registeroffset, no_pc_sync)) reads all eight loop variables.  Partitions it induces:
 87|   size          tested == 0 (with endianness, :74) and > 0 (with scaledness, :80); otherwise only PRINTED (1 << size,
 88|                 :69).  Body-tested partition {0} | {1,2,3}; the printed width distinguishes every value.
 89|   scaledness    truthy at :80                      {0} | {32}
 90|   store         truthy at :62                      {0} | {4}
 91|   signedness    truthy at :66, only when !store    {0} | {8}
 92|   endianness    :71 (>= 0, always true from main), :74 (with size == 0), :77 truthy   {0} | {16}, collapsed for size 0
 93|   usr           truthy at :83                      {0} | {64}
 94|   registeroffset truthy at :86                     {0} | {128}
 95|   no_pc_sync    truthy at :89                      {0} | {256}
 96| Body-only fields: store, signedness, endianness, usr, registeroffset, no_pc_sync.  All eight are written ONLY by the
 97| nested for-loop headers of main() (:221-234), independently, and the loops enumerate the whole product -- so every
 98| state where a body-only field "disagrees" with the guard occurs.  Inside the guard cell (size == 0 && scaledness) the
 99| dominating arms fix registeroffset = 128 (arm C) and exclude store && signedness (arm A), leaving
100| {ld.bu, ld.b, st.b} x endianness{0,16} x usr{0,64} x no_pc_sync{0,256} = 24 cells -- EXHAUSTED by A6's 24 pins.
101| No disagreeing-state row is owed beyond them.
102| Which pins hold which cell outside the guard (the accept side, B3):
103|   size 1, scaled     161 (LE), 177 (BE): ld.hu regofs sync -- the D2 B+1 edge of :80 (B-1 is size -1, outside the
104|                      domain; codex :148).  EXHAUSTED for the edge compare (its two endian cells); other halfword kinds
105|                      SAMPLED (ld.h/st.h, .usr, nopcsync not rowed).
106|   size 2, scaled     418/422 (LE), 434/438 (BE): xmem word ld/st, nopcsync -- SAMPLED.
107|   size 3, scaled     NOT ROWED (doubleword; Grok :91 "the far value") -- clause (e), disclosed.
108|   size 0, unscaled   144, 400, 404 + the 21 cparts = all 24 regofs unscaled byte cells -- EXHAUSTED for the guard's
109|                      scaledness = 0 region at size 0, registeroffset 128.  The unscaled byte cells with
110|                      registeroffset 0 (the immediate forms, indices 0..127 / 256..383) are NOT rowed -- SAMPLED none,
111|                      clause (e).
  ...
131| ## 5. CHANNEL -- per row group: the mutant it kills (by leg id) and the observable that differs.  PREDICTED.
132|   G1 compiles            L3                            compile status (a comment-only source has no main(): link fails)
133|   G2 runs exit 0         L3                            exit status (no binary to run)
134|   G3 generated_functions L3 (absent), S1 (210)         the count on stderr
135|   fresh A1/A2/A3         L3                            presence / initializer count / entry count
136|   fresh A4 NULL == 272   PRE 296, L1 296, L3 0, L5 284, L6 284, L5b 392   the NULL count (blind to a MOVED NULL, Grok :124)
137|   fresh A5 LS_N == 198   L3 0, S1 210                  the #define LS_N count
138|   fresh A6 pins          PRE/L1/L3 all 24; L5 and L5b the 12 no-PC-sync pins (416..504); L6 the 12 LE pins
139|                          (160 164 168 224 228 232 416 420 424 480 484 488)      the symbol text at that index (NULL)
140|   fresh A7 161/177       L3, L7                        the symbol text (L7: "_scaled" dropped from the halfword name)
141|   fresh A7 418/422/434/438 L3, L5b                     the symbol text (L5b: NULL)
142|   fresh A7 144           L3                            the symbol text
143|   fresh A7 400/404       L3, L5b                       the symbol text
144|   fresh A8 cparts        L3; L5b the 10 no-PC-sync cparts (384 388 392 408 448 452 456 464 468 472)
145|   committed A1/A2/A3/A5  L4                            presence / initializer count / entry count / LS_N count
146|   committed A4           PRE 296, L2 296, L4 0         the NULL count
147|   committed A6 pins      PRE, L2, L4 (all 24)          the symbol text
148|   committed A7/A8        L4                            the symbol text
149|   X1 cmp                 L1 L2 L3 L4 L5 L6 L7 L5b S1   byte equality of the two artifacts (green under PRE and FIX:
150|                                                        both artifacts are HEAD's, or both fixed)
151| Predicted red counts (of 122): PRE 50, FIX 0, L1 26, L2 26, L3 63, L4 60, L5 14, L6 14, L7 3, L5b 30, S1 3.
152| Rows with NO red leg in this table other than a null medium: committed A5 (the committed copy's LS_N count has no
153| single-site mutant here -- S1 changes the generator only), A1/A2/A3 on both sides (their non-null mutants -- a dropped
154| or duplicated initializer entry -- are not in the table).  Those are disclosed, not vacuous: each varies under its
155| null medium, which is its measured channel.
156| CHANNEL CHECK: every row above names a mutant under which its observable varies; none is survive-only.  SCORES.txt
157| will diff the measured red set of every leg against these predictions, row by row.
158| 
159| PRETABLE_DONE
~~~~

### 9.5 `RUNS.log` -- one instrument: what each v3 run ran against
~~~~
  1| # RUNS.log -- driver v3 table: one block per run -- what ran, against what, and what it printed last
  2| # started 2026-10-23 10:03:08 -0500; driver /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/diff_m88k_loadstore_gen.sh; want md5 cc2f3cf1575b99459c27f6bdcdaf2abe
  3| # repo generator 6a1fec41d0364fc77f33879f06d9f75b  repo table d222e737a0644e3b633fc1bffdb8e974  (checked again at the end)
  4| PRE prefix_HEAD_v3  10:03:08  driver cc2f3cf1575b99459c27f6bdcdaf2abe  rc 1  -> prefix_HEAD_v3.out
  5|     GEN   /tmp/gxt1/legs/headgen.c  bebaf43992929256de4f187e6b7c27b3
  6|     TABLE /tmp/gxt1/legs/headtable.c  269e6e6f7b5ba4849202b61443bfb9af
  7|     ROWS=123 FAIL=50  last line: M88KLS_DONE
  8| FIX fixed  10:03:09  driver cc2f3cf1575b99459c27f6bdcdaf2abe  rc 0  -> fixed.out
  9|     GEN   (repo default) 6a1fec41d0364fc77f33879f06d9f75b
 10|     TABLE (repo default) d222e737a0644e3b633fc1bffdb8e974
 11|     ROWS=123 FAIL=0  last line: M88KLS_DONE
 12| L1 headgen  10:03:09  driver cc2f3cf1575b99459c27f6bdcdaf2abe  rc 1  -> L1_headgen.out
 13|     GEN   /tmp/gxt1/legs/headgen.c  bebaf43992929256de4f187e6b7c27b3
 14|     TABLE /tmp/gxt1/legs/fixtable.c  d222e737a0644e3b633fc1bffdb8e974
 15|     ROWS=123 FAIL=26  last line: M88KLS_DONE
 16| L2 headtable  10:03:09  driver cc2f3cf1575b99459c27f6bdcdaf2abe  rc 1  -> L2_headtable.out
 17|     GEN   /tmp/gxt1/legs/fixgen.c  6a1fec41d0364fc77f33879f06d9f75b
 18|     TABLE /tmp/gxt1/legs/headtable.c  269e6e6f7b5ba4849202b61443bfb9af
 19|     ROWS=123 FAIL=26  last line: M88KLS_DONE
 20| L3 commentgen  10:03:10  driver cc2f3cf1575b99459c27f6bdcdaf2abe  rc 1  -> L3_commentgen.out
 21|     GEN   /tmp/gxt1/legs/commentgen.c  baa53bc05d730081a6536c7767f6c90a
 22|     TABLE /tmp/gxt1/legs/fixtable.c  d222e737a0644e3b633fc1bffdb8e974
 23|     ROWS=123 FAIL=64  last line: M88KLS_DONE
 24| L4 commenttable  10:03:10  driver cc2f3cf1575b99459c27f6bdcdaf2abe  rc 1  -> L4_commenttable.out
 25|     GEN   /tmp/gxt1/legs/fixgen.c  6a1fec41d0364fc77f33879f06d9f75b
 26|     TABLE /tmp/gxt1/legs/commenttable.c  5010163a7bcf2a80c572552520aa292a
 27|     ROWS=123 FAIL=60  last line: M88KLS_DONE
 28| L5 v2nopcsync  10:03:10  driver cc2f3cf1575b99459c27f6bdcdaf2abe  rc 1  -> L5_v2nopcsync.out
 29|     GEN   /tmp/gxt1/legs/v2nopcsync.c  0aad2d6ce087811e7329f0efcd509d72
 30|     TABLE /tmp/gxt1/legs/fixtable.c  d222e737a0644e3b633fc1bffdb8e974
 31|     ROWS=123 FAIL=14  last line: M88KLS_DONE
 32| L6 lehalf  10:03:11  driver cc2f3cf1575b99459c27f6bdcdaf2abe  rc 1  -> L6_lehalf.out
 33|     GEN   /tmp/gxt1/legs/lehalf.c  188e7812523ca8f4b16bc30b34b78ff9
 34|     TABLE /tmp/gxt1/legs/fixtable.c  d222e737a0644e3b633fc1bffdb8e974
 35|     ROWS=123 FAIL=14  last line: M88KLS_DONE
 36| L7 v6halfword  10:03:11  driver cc2f3cf1575b99459c27f6bdcdaf2abe  rc 1  -> L7_v6halfword.out
 37|     GEN   /tmp/gxt1/legs/v6halfword.c  5b6054821b2ea8aad60a6ffaab91fac5
 38|     TABLE /tmp/gxt1/legs/fixtable.c  d222e737a0644e3b633fc1bffdb8e974
 39|     ROWS=123 FAIL=3  last line: M88KLS_DONE
 40| L8 allnull  10:03:11  driver cc2f3cf1575b99459c27f6bdcdaf2abe  rc 1  -> L8_allnull.out
 41|     GEN   /tmp/gxt1/legs/fixgen.c  6a1fec41d0364fc77f33879f06d9f75b
 42|     TABLE /tmp/gxt1/legs/allnull.c  30e4344056b9b5feffc8f038058b244b
 43|     ROWS=123 FAIL=56  last line: M88KLS_DONE
 44| L5b codexnopcsync  10:03:12  driver cc2f3cf1575b99459c27f6bdcdaf2abe  rc 1  -> L5b_codexnopcsync.out
 45|     GEN   /tmp/gxt1/legs/codexnopcsync.c  4511c183d6784c01e3d43a2bc91b3811
 46|     TABLE /tmp/gxt1/legs/fixtable.c  d222e737a0644e3b633fc1bffdb8e974
 47|     ROWS=123 FAIL=30  last line: M88KLS_DONE
 48| S1 noearlyreturn  10:03:12  driver cc2f3cf1575b99459c27f6bdcdaf2abe  rc 1  -> S1_noearlyreturn.out
 49|     GEN   /tmp/gxt1/legs/noearlyreturn.c  96fa6babded0f8754bf25223e3908bf5
 50|     TABLE /tmp/gxt1/legs/fixtable.c  d222e737a0644e3b633fc1bffdb8e974
 51|     ROWS=123 FAIL=3  last line: M88KLS_DONE
 52| S2 exit1  10:03:12  driver cc2f3cf1575b99459c27f6bdcdaf2abe  rc 1  -> S2_exit1.out
 53|     GEN   /tmp/gxt1/legs/s2exit1.c  5af6d6a7f37e800228d3f711fb518187
 54|     TABLE /tmp/gxt1/legs/fixtable.c  d222e737a0644e3b633fc1bffdb8e974
 55|     ROWS=123 FAIL=1  last line: M88KLS_DONE
 56| S3 emptyout  10:03:13  driver cc2f3cf1575b99459c27f6bdcdaf2abe  rc 1  -> S3_emptyout.out
 57|     GEN   /tmp/gxt1/legs/s3emptyout.c  13f7e92004983d391081444857c4702b
 58|     TABLE /tmp/gxt1/legs/fixtable.c  d222e737a0644e3b633fc1bffdb8e974
 59|     ROWS=123 FAIL=62  last line: M88KLS_DONE
 60| S4 notable  10:03:13  driver cc2f3cf1575b99459c27f6bdcdaf2abe  rc 1  -> S4_notable.out
 61|     GEN   /tmp/gxt1/legs/fixgen.c  6a1fec41d0364fc77f33879f06d9f75b
 62|     TABLE /tmp/gxt1/legs/absent_table.c  (absent)
 63|     ROWS=123 FAIL=60  last line: M88KLS_DONE
 64| S5 nogen  10:03:13  driver cc2f3cf1575b99459c27f6bdcdaf2abe  rc 1  -> S5_nogen.out
 65|     GEN   /tmp/gxt1/legs/absent_gen.c  (absent)
 66|     TABLE /tmp/gxt1/legs/fixtable.c  d222e737a0644e3b633fc1bffdb8e974
 67|     ROWS=123 FAIL=64  last line: M88KLS_DONE
 68| # finished 2026-10-23 10:03:13 -0500; repo generator 6a1fec41d0364fc77f33879f06d9f75b  repo table d222e737a0644e3b633fc1bffdb8e974
 69| # repo files UNCHANGED by the table
 70| RUNS_DONE
~~~~

### 9.6 The pre-fix and fixed receipts, and the timeline (mtimes are the files' own, read by the drafter)
`driver_v1/prefix_HEAD.meta` and `driver_v1/fixed.meta`, whole:
~~~~
## prefix_HEAD run 2026-10-23 09:46:18 -0500  HEAD 5986c137d783b0d7b0104dbc6b652dfab781b7a7
driver    47086d1981f81ef1afcf2a9e01932e3c  (frozen copy: scratchpad t1/build/driver_v1.sh 47086d1981f81ef1afcf2a9e01932e3c)
generator bebaf43992929256de4f187e6b7c27b3  HEAD-blob bebaf43992929256de4f187e6b7c27b3
table     269e6e6f7b5ba4849202b61443bfb9af  HEAD-blob 269e6e6f7b5ba4849202b61443bfb9af
command   GEN= TABLE= /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/diff_m88k_loadstore_gen.sh > prefix_HEAD.out 2>&1
rc        1
summary   ROWS=122 FAIL=50  last line: M88KLS_DONE


## fixed run 2026-10-23 09:47:51 -0500
driver    47086d1981f81ef1afcf2a9e01932e3c  (v1 frozen copy 47086d1981f81ef1afcf2a9e01932e3c)
generator 6a1fec41d0364fc77f33879f06d9f75b
table     d222e737a0644e3b633fc1bffdb8e974
command   GEN= TABLE= /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/diff_m88k_loadstore_gen.sh > fixed.out 2>&1
rc        0
summary   ROWS=122 FAIL=0  last line: M88KLS_DONE

~~~~
`driver_v1/prefix_HEAD.out` (mtime 2026-10-23 09:46:19.436; 127 lines) -- head and tail:
~~~~
  1|   --   GEN   /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/cpus/generate_m88k_loadstore.c
  2|   --   TABLE /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/cpus/tmp_m88k_loadstore.c
  3|   ok   generator: compiles and links                                yes
  4|   ok   generator: exit status                                       0
  5|   ok   generator: stderr generated_functions                        198
  6|   ok   fresh: present and parseable                                 yes
  7|   ok   fresh: m88k_loadstore[512] initializers                      1
  8|   ok   fresh: initializer entries                                   512
  9|   FAIL fresh: NULL entries (supplementary)                          got=296 want=272
 10|   ok   fresh: #define LS_N blocks                                   198
 11|   FAIL fresh: pin [160] F scaled ld.bu le sync                      got=NULL want=m88k_instr_ld_u_1_le_regofs
 12|   FAIL fresh: pin [164] F scaled st.b le sync                       got=NULL want=m88k_instr_st_1_le_regofs
  ...
124|   ok   fresh == committed, byte for byte (cmp)                      identical
125| 
126| ROWS=122 FAIL=50
127| M88KLS_DONE
~~~~
`prefix_HEAD_v3.out` (mtime 2026-10-23 10:03:08.950) -- head and tail:
~~~~
  1|   --   GEN   /tmp/gxt1/legs/headgen.c
  2|   --   TABLE /tmp/gxt1/legs/headtable.c
  3|   ok   gen_compiles         generator: compiles and links                      yes
  4|   ok   gen_exit             generator: exit status                             0
  5|   ok   gen_stdout           generator: stdout non-empty                        yes
  6|   ok   gen_count            generator: stderr generated_functions              198
  7|   ok   fresh_present        present and parseable                              yes
  8|   ok   fresh_inits          m88k_loadstore[512] initializers                   1
  9|   ok   fresh_entries        initializer entries                                512
 10|   FAIL fresh_nulls          NULL entries (supplementary)                       got=296 want=272
 11|   ok   fresh_lsn            #define LS_N blocks (suppression count)            198
 12|   FAIL fresh_pin160         repair scaled ld.bu le sync (consumer)             got=NULL want=m88k_instr_ld_u_1_le_regofs
 13|   FAIL fresh_pin164         repair scaled st.b le sync (consumer)              got=NULL want=m88k_instr_st_1_le_regofs
 14|   FAIL fresh_pin168         repair scaled ld.b le sync (consumer)              got=NULL want=m88k_instr_ld_1_le_regofs
 15|   FAIL fresh_pin176         repair scaled ld.bu be sync (consumer)             got=NULL want=m88k_instr_ld_u_1_le_regofs
 16|   FAIL fresh_pin180         repair scaled st.b be sync (consumer)              got=NULL want=m88k_instr_st_1_le_regofs
  ...
125|   ok   cmp_fresh_committed  fresh == committed, byte for byte (cmp)            identical
126| 
127| ROWS=123 FAIL=50
128| M88KLS_DONE
~~~~
`fixed.out` (mtime 2026-10-23 10:03:09.295; byte-identical to GATE 2's driver log, S18e) -- head and tail:
~~~~
  1|   --   GEN   /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/cpus/generate_m88k_loadstore.c
  2|   --   TABLE /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/cpus/tmp_m88k_loadstore.c
  3|   ok   gen_compiles         generator: compiles and links                      yes
  4|   ok   gen_exit             generator: exit status                             0
  5|   ok   gen_stdout           generator: stdout non-empty                        yes
  6|   ok   gen_count            generator: stderr generated_functions              198
  7|   ok   fresh_present        present and parseable                              yes
  8|   ok   fresh_inits          m88k_loadstore[512] initializers                   1
  9|   ok   fresh_entries        initializer entries                                512
 10|   ok   fresh_nulls          NULL entries (supplementary)                       272
 11|   ok   fresh_lsn            #define LS_N blocks (suppression count)            198
 12|   ok   fresh_pin160         repair scaled ld.bu le sync (consumer)             m88k_instr_ld_u_1_le_regofs
 13|   ok   fresh_pin164         repair scaled st.b le sync (consumer)              m88k_instr_st_1_le_regofs
 14|   ok   fresh_pin168         repair scaled ld.b le sync (consumer)              m88k_instr_ld_1_le_regofs
  ...
125|   ok   cmp_fresh_committed  fresh == committed, byte for byte (cmp)            identical
126| 
127| ROWS=123 FAIL=0
128| M88KLS_DONE
~~~~
The timeline, sorted by each file's own mtime:
~~~~
2026-10-22 23:42:00.990  BASELINE.out: the HEAD generator compiled and run in a scratch dir; fresh == committed (md5 269e6e6f)
2026-10-22 23:45:16.960  PRETABLE.out: the pre-table check, before any driver existed (122 rows prescribed)
2026-10-23 09:40:22.282  PRETABLE_L8.out: the L8 prediction
2026-10-23 09:46:19.436  driver_v1/prefix_HEAD.out: driver v1 (md5 47086d19) on the UNMODIFIED repo (repo defaults): ROWS=122 FAIL=50
2026-10-23 09:46:58.650  src/cpus/generate_m88k_loadstore.c EDITED (md5 6a1fec41)
2026-10-23 09:47:51.562  src/cpus/tmp_m88k_loadstore.c REGENERATED from the fixed generator (md5 d222e737)
2026-10-23 09:47:52.112  driver_v1/fixed.out: ROWS=122 FAIL=0
2026-10-23 09:51:43.119  driver_v1/RERUN_v2.txt: v2 (= v1 + 5 comment lines) reproduces every v1 run
2026-10-23 09:59:58.756  regress/diff_m88k_loadstore_gen.sh = driver v3 (md5 cc2f3cf1), the file to commit
2026-10-23 10:01:39.464  the GATE 2 block v3: working-tree file and staged copy written
2026-10-23 10:02:21.316  PRETABLE_v3.out: the v3 predictions, before any v3 run
2026-10-23 10:03:08.950  prefix_HEAD_v3.out: v3 on byte-exact HEAD blob copies via GEN=/TABLE=: ROWS=123 FAIL=50
2026-10-23 10:03:13.525  the last of the 16 v3 runs (RUNS.log: started 10:03:08, finished 10:03:13)
2026-10-23 10:04:24.977  SCORES.txt
2026-10-23 10:07:46.505  CLEARANCE.out (build/ rebuilt 09:54:12, build-asan/ 10:06:40, /tmp/gxsec-build 10:07:16)
2026-10-23 10:12:03.644  GATE 2's driver log (the gate ran 10:09:00-10:11:51)
2026-10-23 10:17:17.180  GATE11_tail.out (the gate ran 10:12:46-10:16:53)
2026-10-23 10:17:59.560  FIX.out
2026-10-23 10:20:09.934  BUILD_REPORT.md
~~~~

### 9.7 How the shipped driver (v3) differs from the one that made the pre-edit-dated receipt (v1)
`driver_v1/driver_v1_to_v2.diff` (whole) and `driver_v1/RERUN_v2.txt` (lines 1-6):
~~~~
--- driver_v1/diff_m88k_loadstore_gen.sh
+++ driver_v2/diff_m88k_loadstore_gen.sh
@@ -58,6 +58,11 @@
 #  size tests beyond the halfword edge; uniqueness of the generated definition
 #  names (a collision fails the emulator's own compile, loudly).
 #
+#  (c): measured at regress/artifacts/m88kscaledbyte/table1_20261022/L3_commentgen.out
+#  (a comment-only generator: the compile row and every fresh-side row red) and
+#  .../L4_commenttable.out (a comment-only table: every committed-side row red);
+#  .../L8_allnull.out is a second table-side medium.  Scores: SCORES.txt there.
+#
 #  Overrides, so a table of variants runs WITHOUT touching the repo:
 #  GEN=<generator source>, TABLE=<committed table>, CC=<compiler>.  Gate 2
 #  clears GEN and TABLE so it always tests the committed files.
  1| # RERUN_v2.txt -- 2026-10-23 09:51:39 -0500
  2| # driver v1 md5 47086d1981f81ef1afcf2a9e01932e3c (every artifact in this dir)   driver v2 md5 302e6259dca9981362c50eec3caaed18 (the file to be committed)
  3| # v1 -> v2 diff: driver_v1_to_v2.diff -- 5 added line(s), 0 removed;
  4| #   added lines that are not comments: 0
  5| # repo files UNCHANGED by the table
  6| RUNS_DONE
~~~~
`driver_v2_to_v3.diff` (14 KB) is NOT inlined (open it: `table1_20261022/driver_v2_to_v3.diff`).  What it changes, by the drafter's reading and the
mechanical check S18(d): the header's CONTRACT paragraph is rewritten (all 24 floor; the consumer subset; the 54-pin
enumeration; the narrow-count wording; the NOT-OBSERVED list adds "the generated DEFINITIONS beyond their count");
`row()` gains a first IDENTITY argument and a fixed-width identity column; the spec block's class letters change F/E ->
R/N and four accept descriptions change -- the 54 index -> expected-name pairs are UNCHANGED; the `gen_stdout` row
(execution: stdout non-empty) is added; every literal row label becomes an identity (`gen_compiles`, `gen_exit`,
`gen_count`, `cmp_fresh_committed`, `<a>_present/_inits/_entries/_nulls/_lsn`, `<a>_pin<i>/_acc<i>/_cp<i>`).

### 9.8 Every v3 run's score line, sentinel, mtime and md5 (read by the drafter from the `.out` files themselves)
~~~~
run      artifact                          score line           sentinel      mtime                md5
PRE      prefix_HEAD_v3.out                ROWS=123 FAIL=50     M88KLS_DONE   2026-10-23 10:03:08  435acd93
FIX      fixed.out                         ROWS=123 FAIL=0      M88KLS_DONE   2026-10-23 10:03:09  5f803a73
L1       L1_headgen.out                    ROWS=123 FAIL=26     M88KLS_DONE   2026-10-23 10:03:09  cd4bc9fe
L2       L2_headtable.out                  ROWS=123 FAIL=26     M88KLS_DONE   2026-10-23 10:03:09  4c85a352
L3       L3_commentgen.out                 ROWS=123 FAIL=64     M88KLS_DONE   2026-10-23 10:03:10  a01850e7
L4       L4_commenttable.out               ROWS=123 FAIL=60     M88KLS_DONE   2026-10-23 10:03:10  22d2892f
L5       L5_v2nopcsync.out                 ROWS=123 FAIL=14     M88KLS_DONE   2026-10-23 10:03:10  8d8fbd2f
L6       L6_lehalf.out                     ROWS=123 FAIL=14     M88KLS_DONE   2026-10-23 10:03:11  7ccf186b
L7       L7_v6halfword.out                 ROWS=123 FAIL=3      M88KLS_DONE   2026-10-23 10:03:11  0486301d
L8       L8_allnull.out                    ROWS=123 FAIL=56     M88KLS_DONE   2026-10-23 10:03:11  39e082fb
L5b      L5b_codexnopcsync.out             ROWS=123 FAIL=30     M88KLS_DONE   2026-10-23 10:03:12  f20c6b37
S1       S1_noearlyreturn.out              ROWS=123 FAIL=3      M88KLS_DONE   2026-10-23 10:03:12  444eb602
S2       S2_exit1.out                      ROWS=123 FAIL=1      M88KLS_DONE   2026-10-23 10:03:12  bbdbc83b
S3       S3_emptyout.out                   ROWS=123 FAIL=62     M88KLS_DONE   2026-10-23 10:03:13  e44f8dc9
S4       S4_notable.out                    ROWS=123 FAIL=60     M88KLS_DONE   2026-10-23 10:03:13  a7b3dbc3
S5       S5_nogen.out                      ROWS=123 FAIL=64     M88KLS_DONE   2026-10-23 10:03:13  8256642f
v1 PRE   driver_v1/prefix_HEAD.out         ROWS=122 FAIL=50     M88KLS_DONE   2026-10-23 09:46:19  112ad303
v1 FIX   driver_v1/fixed.out               ROWS=122 FAIL=0      M88KLS_DONE   2026-10-23 09:47:52  5e113bd0
~~~~

### 9.9 `DUPNAMES.out` -- L7's duplicate definition NAMES, measured outside the driver
~~~~
  1| # DUPNAMES.out -- T1 / #569: duplicate generated-definition NAMES per generator (2026-10-23 10:03:36 -0500)
  2| # method: cc -o g <gen>.c; ./g > out.c; grep '^#define LS_N ' / '^#define LS_GENERIC_N ' | sort | uniq -d
  3| # (the driver does not compile the generated file; this is the observable it leaves to the emulator's compile)
  4| generator          md5                                    LS_N   LS_N dup    GENERIC_N  GENERIC dup
  5| headgen            bebaf43992929256de4f187e6b7c27b3        198          0          198           90
  6| fixgen             6a1fec41d0364fc77f33879f06d9f75b        198          0          198           90
  7| v6halfword         5b6054821b2ea8aad60a6ffaab91fac5        198         24          198           78
  8| noearlyreturn      96fa6babded0f8754bf25223e3908bf5        210         12          210          102
  9| 
 10| ## the duplicated LS_N names, per variant (each listed once; every one occurs twice)
 11| -- v6halfword
 12|    m88k_instr_ld_2_be_regofs
 13|    m88k_instr_ld_2_be_regofs_nopcsync
 14|    m88k_instr_ld_2_be_usr_regofs
 15|    m88k_instr_ld_2_be_usr_regofs_nopcsync
 16|    m88k_instr_ld_2_le_regofs
 17|    m88k_instr_ld_2_le_regofs_nopcsync
 18|    m88k_instr_ld_2_le_usr_regofs
 19|    m88k_instr_ld_2_le_usr_regofs_nopcsync
 20|    m88k_instr_ld_u_2_be_regofs
 21|    m88k_instr_ld_u_2_be_regofs_nopcsync
 22|    m88k_instr_ld_u_2_be_usr_regofs
 23|    m88k_instr_ld_u_2_be_usr_regofs_nopcsync
 24|    m88k_instr_ld_u_2_le_regofs
 25|    m88k_instr_ld_u_2_le_regofs_nopcsync
 26|    m88k_instr_ld_u_2_le_usr_regofs
 27|    m88k_instr_ld_u_2_le_usr_regofs_nopcsync
 28|    m88k_instr_st_2_be_regofs
 29|    m88k_instr_st_2_be_regofs_nopcsync
 30|    m88k_instr_st_2_be_usr_regofs
 31|    m88k_instr_st_2_be_usr_regofs_nopcsync
 32|    m88k_instr_st_2_le_regofs
 33|    m88k_instr_st_2_le_regofs_nopcsync
 34|    m88k_instr_st_2_le_usr_regofs
 35|    m88k_instr_st_2_le_usr_regofs_nopcsync
 36| -- noearlyreturn
 37|    m88k_instr_ld_1_le_regofs
 38|    m88k_instr_ld_1_le_regofs_nopcsync
 39|    m88k_instr_ld_1_le_usr_regofs
 40|    m88k_instr_ld_1_le_usr_regofs_nopcsync
 41|    m88k_instr_ld_u_1_le_regofs
 42|    m88k_instr_ld_u_1_le_regofs_nopcsync
 43|    m88k_instr_ld_u_1_le_usr_regofs
 44|    m88k_instr_ld_u_1_le_usr_regofs_nopcsync
 45|    m88k_instr_st_1_le_regofs
 46|    m88k_instr_st_1_le_regofs_nopcsync
 47|    m88k_instr_st_1_le_usr_regofs
 48|    m88k_instr_st_1_le_usr_regofs_nopcsync
 49| 
 50| DUPNAMES_DONE
~~~~

### 9.10 `FIX.out` -- the regenerated table verified line by line (section 2 of the file)
~~~~
 31| ## 2. the table, HEAD -> fixed, line by line (scratchpad t1/build/verify_table.py)
 32| CR bytes: head 0 new 0
 33| lines: head 4251 new 4251
 34| declaration line(s) (1-based): [3738]
 35| differing lines: 24
 36| changes that are exactly NULL -> the design name at a pinned index: 24 of 24 (pins 24)
 37| indices changed == the 24 pins: True
 38| new table: entries 512, NULL 272
 39| diff line ranges (normal format): 3899c3899 3903c3903 3907c3907 3915c3915 3919c3919 3923c3923 3963c3963 3967c3967 3971c3971 3979c3979 3983c3983 3987c3987 4155c4155 4159c4159 4163c4163 4171c4171 4175c4175 4179c4179 4219c4219 4223c4223 4227c4227 4235c4235 4239c4239 4243c4243 
~~~~

### 9.11 `CLEARANCE.out` -- propagation and the two-part clearance, run 10:07:46
~~~~
  1| # CLEARANCE.out -- T1 / #569, step 7 (D5): propagation and the two-part clearance, RUN 2026-10-23 10:07:46 -0500
  2| # part 1: cmp <tree>/<file> GXEMUL-SEC/<file>; part 2: [ <tree>/gxemul -nt <tree>/<file> ] (build trees only).
  3| # repo: generator 6a1fec41d0364fc77f33879f06d9f75b  table d222e737a0644e3b633fc1bffdb8e974
  4| 
  5| ## the divergence set, DERIVED (grep -vE '^\s*(#|$)' tools/est_divergence.txt) -- neither file is in it:
  6|    src/devices/.index
  7|    src/devices/Makefile.skel
  8|    src/devices/autodev.c
  9|    src/devices/dev_jazz.c
 10|    src/devices/dev_ne2000.c
 11|    src/machines/machine_arc.c
 12|    src/cpus/generate_m88k_loadstore.c: shared (not listed) -> the clearance applies
 13|    src/cpus/tmp_m88k_loadstore.c: shared (not listed) -> the clearance applies
 14| 
 15| ## sentinels
 16|    /mnt/c/DocumentNoSnc/cc/GXEMUL/est: no .MUTANT
 17|    /mnt/c/DocumentNoSnc/cc/GXEMUL/build: no .MUTANT
 18|    /mnt/c/DocumentNoSnc/cc/GXEMUL/build-asan: no .MUTANT
 19|    /tmp/gxsec-build: no .MUTANT
 20| 
 21| ## the clearance
 22|    est         part 1  cmp src/cpus/generate_m88k_loadstore.c   : CLEAN
 23|    est         part 1  cmp src/cpus/tmp_m88k_loadstore.c        : CLEAN
 24|    est         part 2  est/: source tree, part 2 N/A (no binary exists)
 25|    build       part 1  cmp src/cpus/generate_m88k_loadstore.c   : CLEAN
 26|    build       part 1  cmp src/cpus/tmp_m88k_loadstore.c        : CLEAN
 27|    build       part 2  [ gxemul -nt src/cpus/generate_m88k_loadstore.c ] : yes   (gxemul 2026-10-23 09:54:12.016, file 2026-10-23 09:53:36.707)
 28|    build       part 2  [ gxemul -nt src/cpus/tmp_m88k_loadstore.c ] : yes   (gxemul 2026-10-23 09:54:12.016, file 2026-10-23 09:53:53.585)
 29|    build-asan  part 1  cmp src/cpus/generate_m88k_loadstore.c   : CLEAN
 30|    build-asan  part 1  cmp src/cpus/tmp_m88k_loadstore.c        : CLEAN
 31|    build-asan  part 2  [ gxemul -nt src/cpus/generate_m88k_loadstore.c ] : yes   (gxemul 2026-10-23 10:06:40.775, file 2026-10-23 10:04:41.557)
 32|    build-asan  part 2  [ gxemul -nt src/cpus/tmp_m88k_loadstore.c ] : yes   (gxemul 2026-10-23 10:06:40.775, file 2026-10-23 10:05:37.884)
 33|    gxsec-build part 1  cmp src/cpus/generate_m88k_loadstore.c   : CLEAN
 34|    gxsec-build part 1  cmp src/cpus/tmp_m88k_loadstore.c        : CLEAN
 35|    gxsec-build part 2  [ gxemul -nt src/cpus/generate_m88k_loadstore.c ] : yes   (gxemul 2026-10-23 10:07:16.286, file 2026-10-23 10:06:47.242)
 36|    gxsec-build part 2  [ gxemul -nt src/cpus/tmp_m88k_loadstore.c ] : yes   (gxemul 2026-10-23 10:07:16.286, file 2026-10-23 10:07:02.262)
 37| 
 38| ## did make regenerate the table IN-TREE? (dependency-driven: only when the generator binary or the template is
 39| ## newer -- here the generator source was newer, so its binary was rebuilt and the rule fired; shown, not assumed)
 40|    build       rule ran: 1 time(s) (log line 113)   generator stderr: ./generate_m88k_loadstore: generated_functions = 198
 41|    build-asan  rule ran: 1 time(s) (log line 113)   generator stderr: ./generate_m88k_loadstore: generated_functions = 198
 42|    gxsec-build rule ran: 1 time(s) (log line 112)   generator stderr: ./generate_m88k_loadstore: generated_functions = 198
 43| 
 44| ## the per-tree build records (copy time, make rc/wall, mtimes after make), as printed by build_tree.sh
 45|    == est (/mnt/c/DocumentNoSnc/cc/GXEMUL/est, source tree)  start 2026-10-23 09:53:28
 46|    copied   src/cpus/generate_m88k_loadstore.c 2026-10-23 09:53:28.562   src/cpus/tmp_m88k_loadstore.c 2026-10-23 09:53:28.580
 47|    -- clearance (part 1: source cmp against GXEMUL-SEC; part 2: [ binary -nt source ])
 48|       part 1  cmp est/src/cpus/generate_m88k_loadstore.c  GXEMUL-SEC/src/cpus/generate_m88k_loadstore.c : CLEAN
 49|       part 1  cmp est/src/cpus/tmp_m88k_loadstore.c  GXEMUL-SEC/src/cpus/tmp_m88k_loadstore.c : CLEAN
 50|       part 2  est: source tree, part 2 N/A (no binary exists)
 51|    == est done 09:53:28
 52| 
 53|    == build (/mnt/c/DocumentNoSnc/cc/GXEMUL/build, build tree)  start 2026-10-23 09:53:36
 54|    copied   src/cpus/generate_m88k_loadstore.c 2026-10-23 09:53:36.707   src/cpus/tmp_m88k_loadstore.c 2026-10-23 09:53:36.721
 55|    make     rc=0  wall=36s  log lines 128  (log: scratchpad t1/build/build_build.log)
 56|             lines matching 'error' (case-insensitive): 0
 57|             log: 39:cc -Wshadow -Wcast-align -Wstrict-aliasing -Wall  -Wextra -Wno-unused-parameter -Wno-cast-align -fstrict-aliasing -fomit-frame-pointer -fpeephole -fgnu89-inline -O3 -DNDEBUG  -I../include/    generate_m88k_loadstore.c   -o generate_m88k_loadstore
 58|             log: 113:./generate_m88k_loadstore > tmp_m88k_loadstore.c
 59|             log: 115:./generate_m88k_loadstore: generated_functions = 198
 60|    after    gen-bin 2026-10-23 09:53:37.336   src/cpus/tmp_m88k_loadstore.c 2026-10-23 09:53:53.585   gxemul 2026-10-23 09:54:12.016
 61|             cpu_m88k.o 2026-10-23 09:54:04.186
 62|    -- clearance (part 1: source cmp against GXEMUL-SEC; part 2: [ binary -nt source ])
 63|       part 1  cmp build/src/cpus/generate_m88k_loadstore.c  GXEMUL-SEC/src/cpus/generate_m88k_loadstore.c : CLEAN
 64|       part 1  cmp build/src/cpus/tmp_m88k_loadstore.c  GXEMUL-SEC/src/cpus/tmp_m88k_loadstore.c : CLEAN
 65|       part 2  [ build/gxemul -nt build/src/cpus/generate_m88k_loadstore.c ] : yes
 66|       part 2  [ build/gxemul -nt build/src/cpus/tmp_m88k_loadstore.c ] : yes
 67|    == build done 09:54:12
 68| 
 69|    == build-asan (/mnt/c/DocumentNoSnc/cc/GXEMUL/build-asan, build tree)  start 2026-10-23 10:04:41
 70|    copied   src/cpus/generate_m88k_loadstore.c 2026-10-23 10:04:41.557   src/cpus/tmp_m88k_loadstore.c 2026-10-23 10:04:41.577
 71|    make     rc=0  wall=119s  log lines 128  (log: scratchpad t1/build/build_build-asan.log)
 72|             lines matching 'error' (case-insensitive): 0
 73|             log: 39:cc -Wshadow -Wcast-align -Wstrict-aliasing -Wall  -Wextra -Wno-unused-parameter -Wno-cast-align -fstrict-aliasing -fomit-frame-pointer -fpeephole -fgnu89-inline -O3 -DNDEBUG -fsanitize=address,undefined -fno-omit-frame-pointer -g -I../include/    generate_m88k_loadstore.c   -o generate_m88k_loadstore
 74|             log: 113:./generate_m88k_loadstore > tmp_m88k_loadstore.c
 75|             log: 115:./generate_m88k_loadstore: generated_functions = 198
 76|    after    gen-bin 2026-10-23 10:04:42.456   src/cpus/tmp_m88k_loadstore.c 2026-10-23 10:05:37.884   gxemul 2026-10-23 10:06:40.775
 77|             cpu_m88k.o 2026-10-23 10:06:27.817
 78|    -- clearance (part 1: source cmp against GXEMUL-SEC; part 2: [ binary -nt source ])
 79|       part 1  cmp build-asan/src/cpus/generate_m88k_loadstore.c  GXEMUL-SEC/src/cpus/generate_m88k_loadstore.c : CLEAN
 80|       part 1  cmp build-asan/src/cpus/tmp_m88k_loadstore.c  GXEMUL-SEC/src/cpus/tmp_m88k_loadstore.c : CLEAN
 81|       part 2  [ build-asan/gxemul -nt build-asan/src/cpus/generate_m88k_loadstore.c ] : yes
 82|       part 2  [ build-asan/gxemul -nt build-asan/src/cpus/tmp_m88k_loadstore.c ] : yes
 83|    == build-asan done 10:06:40
 84| 
 85|    == gxsec-build (/tmp/gxsec-build, build tree)  start 2026-10-23 10:06:47
 86|    copied   src/cpus/generate_m88k_loadstore.c 2026-10-23 10:06:47.242   src/cpus/tmp_m88k_loadstore.c 2026-10-23 10:06:47.248
 87|    make     rc=0  wall=29s  log lines 127  (log: scratchpad t1/build/build_gxsec-build.log)
 88|             lines matching 'error' (case-insensitive): 0
 89|             log: 19:cc -Wshadow -Wcast-align -Wstrict-aliasing -Wall  -Wextra -Wno-unused-parameter -Wno-cast-align -fstrict-aliasing -fomit-frame-pointer -fpeephole -fgnu89-inline -O3 -DNDEBUG  -I../include/    generate_m88k_loadstore.c   -o generate_m88k_loadstore
 90|             log: 112:./generate_m88k_loadstore > tmp_m88k_loadstore.c
 91|             log: 113:./generate_m88k_loadstore: generated_functions = 198
 92|    after    gen-bin 2026-10-23 10:06:47.562   src/cpus/tmp_m88k_loadstore.c 2026-10-23 10:07:02.262   gxemul 2026-10-23 10:07:16.286
 93|             cpu_m88k.o 2026-10-23 10:07:11.970
 94|    -- clearance (part 1: source cmp against GXEMUL-SEC; part 2: [ binary -nt source ])
 95|       part 1  cmp gxsec-build/src/cpus/generate_m88k_loadstore.c  GXEMUL-SEC/src/cpus/generate_m88k_loadstore.c : CLEAN
 96|       part 1  cmp gxsec-build/src/cpus/tmp_m88k_loadstore.c  GXEMUL-SEC/src/cpus/tmp_m88k_loadstore.c : CLEAN
 97|       part 2  [ gxsec-build/gxemul -nt gxsec-build/src/cpus/generate_m88k_loadstore.c ] : yes
 98|       part 2  [ gxsec-build/gxemul -nt gxsec-build/src/cpus/tmp_m88k_loadstore.c ] : yes
 99|    == gxsec-build done 10:07:16
100| 
101| CLEARANCE_DONE
~~~~

### 9.12 `GATE2_tail.out` -- GATE 2 run once, alone (EXCERPT: the header and run record, the start and end of the driver log as the gate printed it, the block's three aggregate checks and its first identity checks, and the closing lines)
~~~~
  1| # GATE2_tail.out -- T1 / #569, step 8: GATE 2 (gate_offline.sh) run ONCE, alone, as `bash regress/run.sh 2`
  2| # (LOGDIR = lib.sh default /tmp/gxregress).  Full output: 2596 lines, kept in the builder's scratchpad
  3| # (t1/build/gate2_run.log); this file preserves the run record, the #569 block's section VERBATIM (lines 16-269
  4| # of the full output: the driver log as the gate prints it, then the block's 126 checks) and the closing lines.
  5| # The driver's own log is GATE2_diff_m88k_loadstore_gen.log beside it.  The gate ran on the WORKING TREE:
  6| # gate_offline.sh carries the foreign uncommitted hunks (CHECKS #11) plus the #569 block.  Gate-level 'FAIL'
  7| # rows (lines beginning '  FAIL ') in the whole output: 0.
  8| 
  9| ## run record
 10| gate 2: start 2026-10-23 10:09:00 -0500; HEAD ref: refs/heads/main; LOGDIR=/tmp/gxregress (lib.sh default)
 11| concurrent jobs at start: 0
 12| gate 2: rc=0  end 2026-10-23 10:11:51 -0500  wall=171s  lines 2596
 13| 
 14| ## the #569 block's section, verbatim
 15|          --   GEN   /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/cpus/generate_m88k_loadstore.c
 16|          --   TABLE /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/cpus/tmp_m88k_loadstore.c
 17|          ok   gen_compiles         generator: compiles and links                      yes
 18|          ok   gen_exit             generator: exit status                             0
 19|          ok   gen_stdout           generator: stdout non-empty                        yes
 20|          ok   gen_count            generator: stderr generated_functions              198
  ...
136|          ok   committed_cp464      counterpart unscaled ld.bu be usr nosync           m88k_instr_ld_u_1_le_usr_regofs_nopcsync
137|          ok   committed_cp468      counterpart unscaled st.b be usr nosync            m88k_instr_st_1_le_usr_regofs_nopcsync
138|          ok   committed_cp472      counterpart unscaled ld.b be usr nosync            m88k_instr_ld_1_le_usr_regofs_nopcsync
139|          ok   cmp_fresh_committed  fresh == committed, byte for byte (cmp)            identical
140|        
141|        ROWS=123 FAIL=0
142|        M88KLS_DONE
143|   ok   m88k loadstore generator: row failures               0
144|   ok   m88k loadstore generator: rows run (the denominator is the pin) 123
145|   ok   m88k loadstore generator: completion sentinel        1
146|   ok   m88k loadstore generator: row gen_compiles, exactly once 1
147|   ok   m88k loadstore generator: row gen_exit, exactly once 1
148|   ok   m88k loadstore generator: row gen_stdout, exactly once 1
149|   ok   m88k loadstore generator: row gen_count, exactly once 1
150|   ok   m88k loadstore generator: row cmp_fresh_committed, exactly once 1
  ...
266|   ok   m88k loadstore generator: row committed_cp464, exactly once 1
267|   ok   m88k loadstore generator: row committed_cp468, exactly once 1
268|   ok   m88k loadstore generator: row committed_cp472, exactly once 1
269| 
270| ## the closing lines (completion line, summary, verdict)
271| 
272| offline-differential: PASS (502 checks)
273| 
274| ############################################################
275| ## SUMMARY
276| ############################################################
277|   PASS 2. gate_offline
278| 
279|   passed 1   failed 0   skipped 0
280|   GATE_COVERAGE=1/16 (SUBSET: 2)
281| 
282| REGRESS_PASS
283| 
284| GATE2_TAIL_DONE
~~~~

### 9.13 `GATE11_tail.out` -- GATE 11 run once, alone, on the rebuilt `build/gxemul` (EXCERPT: header, run record, closing lines)
~~~~
  1| # GATE11_tail.out -- T1 / #569, step 8: GATE 11 (gate_m88k_rounding.sh) run ONCE, alone, as `bash regress/run.sh 11`,
  2| # on the rebuilt build/gxemul (CLEARANCE.out: rebuilt 2026-10-23 09:54:12 over the fixed generator and table).
  3| # Full output: 359 lines, kept in the builder's scratchpad (t1/build/gate11_run.log).  The m88k regression
  4| # check the spec asks for; it does not exercise the 24 slots (no guest witness -- WITNESS_ATTEMPT.md).
  5| # build/gxemul at report time: 2026-10-23 09:54:12.016853000 -0500 6159736
  6| # Gate-level 'FAIL' rows (lines beginning '  FAIL ') in the whole output: 0.
  7| 
  8| ## run record
  9| gate 11: start 2026-10-23 10:12:46 -0500; HEAD ref: refs/heads/main; LOGDIR=/tmp/gxregress (lib.sh default)
 10| concurrent jobs at start: 0
 11| gate 11: rc=0  end 2026-10-23 10:16:53 -0500  wall=247s  lines 359
 12| 
 13| ## the binary and image lines the gate printed
 14| 4:  --   binary : /mnt/c/DocumentNoSnc/CC/GXEMUL/build/gxemul
 15| 5:  --   image  : /mnt/c/DocumentNoSnc/CC/GXEMUL/_images/liveimage-luna88k-raw-20250518.img (R: throwaway overlay; never written)
 16| 
 17| ## every check row the gate itself emitted (lines beginning '  ok   ' / '  FAIL ')
 18|   ok   rows run                                             80
 19|   ok   rows correct                                         80
 20|   ok     asymmetric: fadd-neg toward+Inf                    1
  ...
128|   ok   luna absentcpu: no row reported a halted machine (the pre-fix symptom is the process ending mid-row) 0
129| 
130| ## the closing lines (completion line, summary, verdict)
131| 
132| gate 11: m88k rounding mode (#298): PASS (111 checks)
133| 
134| ############################################################
135| ## SUMMARY
136| ############################################################
137|   PASS 11. gate_m88k_rounding
138| 
139|   passed 1   failed 0   skipped 0
140|   GATE_COVERAGE=1/16 (SUBSET: 11)
141| 
142| REGRESS_PASS
143| 
144| GATE11_TAIL_DONE
~~~~

### 9.14 `BASELINE.out` -- the HEAD agreement receipt (sections 3-4: fresh generator output == the committed table at HEAD)
~~~~
 34| ## 3. the HEAD generator, compiled and run in /tmp/gxt1/base (a scratch dir; never in the repo)
 35| copied: md5 bebaf43992929256de4f187e6b7c27b3
 36| compile: rc=0  (cc -o gen generate_m88k_loadstore.c; log lines: 0)
 37| run: rc=0
 38| stderr: ./gen: generated_functions = 198
 39| fresh_HEAD.c: 89277 bytes, 4250 lines, md5 269e6e6f7b5ba4849202b61443bfb9af
 40| committed  : 89277 bytes, 4250 lines, md5 269e6e6f7b5ba4849202b61443bfb9af
 41| CMP fresh_HEAD.c vs committed GXEMUL-SEC/src/cpus/tmp_m88k_loadstore.c: IDENTICAL (CHECKS #6 agreement at HEAD)
 42| 
 43| ## 4. counts, two methods each (a denominator for every count)
 44| fresh_HEAD.c: initializers matching *m88k_loadstore[512] = 1; entries in it = 512; NULL entries in it = 296
 45| fresh_HEAD.c: grep -c NULL (whole file, CHECKS #5 method) = 296
 46| fresh_HEAD.c: grep -c '^#define LS_N ' (trailing space) = 198
 47| fresh_HEAD.c: grep -c '^#define LS_N'  (no space; also matches LS_NO_PC_SYNC -- the calibration) = 297
 48| fresh_HEAD.c: grep -c '^#define LS_NO_PC_SYNC' = 99
 49| committed: initializers matching *m88k_loadstore[512] = 1; entries in it = 512; NULL entries in it = 296
 50| committed: grep -c NULL (whole file, CHECKS #5 method) = 296
 51| committed: grep -c '^#define LS_N ' (trailing space) = 198
 52| committed: grep -c '^#define LS_N'  (no space; also matches LS_NO_PC_SYNC -- the calibration) = 297
 53| committed: grep -c '^#define LS_NO_PC_SYNC' = 99
~~~~

### 9.15 For P2: GATE 2's recorded check counts in the weekly battery (outside the repository, `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\nightly\`), read by the drafter
~~~~
battery_20261004_180001.log:2325: offline-differential: PASS (359 checks)
battery_20261011_180002.log:2360: offline-differential: PASS (376 checks)
battery_20261018_231924.log:2360: offline-differential: PASS (376 checks)

verdict_20261004_180001.txt, lines 1-7 (the TREE_DIRTY list is printed in path order):
  1| HEAD=1329d894
  2| TREE_DIRTY=YES  *** VERDICT DOES NOT DESCRIBE A COMMIT ***
  3|      M regress/artifacts/recordfix_20261002/chk_hrec.py.txt
  4|      M regress/gate_sh_rounding.sh
  5|      M regress/gdrom_default_probe.py
  6|      M regress/ppc_rldicl_probe.py
  7|      M regress/sh4_chcr_probe.py

verdict_20261011_180002.txt, lines 1-7 (the TREE_DIRTY list is printed in path order):
  1| HEAD=e483d931
  2| TREE_DIRTY=YES  *** VERDICT DOES NOT DESCRIBE A COMMIT ***
  3|      M regress/artifacts/recordfix_20261002/chk_hrec.py.txt
  4|      M regress/diff_wdc_identify.c
  5|      M regress/gate_offline.sh
  6|      M regress/gate_sh_rounding.sh
  7|      M regress/gdrom_default_probe.py

verdict_20261018_231924.txt, lines 1-7 (the TREE_DIRTY list is printed in path order):
  1| HEAD=6c2840d7
  2| TREE_DIRTY=YES  *** VERDICT DOES NOT DESCRIBE A COMMIT ***
  3|      M regress/artifacts/recordfix_20261002/chk_hrec.py.txt
  4|      M regress/diff_wdc_identify.c
  5|      M regress/gate_hygiene.sh
  6|      M regress/gate_mips_folds.sh
  7|      M regress/gate_offline.sh

$ git log --format=%h 1329d894..HEAD -- regress/gate_offline.sh regress/diff_wdc_identify.c regress/lib.sh | wc -l
0

The 17 `check` labels the foreign hunk (staged -> working tree, at staged line 1879) adds -- members of P2's "17":
   1. wdc IDENTIFY: the re-arm 32769 length row is present
   2. wdc IDENTIFY: the re-arm 32769 push row is present
   3. wdc IDENTIFY: the arm 32769 row is present
   4. wdc IDENTIFY: the re-arm 32767 length row is present
   5. wdc IDENTIFY: the re-arm 32767 push row is present
   6. wdc IDENTIFY: the arm 32767 row is present
   7. wdc IDENTIFY: the re-arm whole-chunk row is present
   8. wdc IDENTIFY: the arm chunk-body row is present
   9. wdc IDENTIFY: the long-transfer last-chunk row is present
  10. wdc IDENTIFY: the 2-byte write-route row is present
  11. wdc IDENTIFY: the 4-byte write-route row is present
  12. wdc IDENTIFY: the little-endian write-route row is present
  13. wdc IDENTIFY: the COMPLETED write-route row is present
  14. wdc IDENTIFY: the 1-byte write-route row is present
  15. wdc IDENTIFY: the completion ireason row is present
  16. wdc IDENTIFY: the completion STATUS row is present
  17. wdc IDENTIFY: the stray-read row is present
~~~~

---

## 10. The project rules the questions apply -- quoted VERBATIM with their bounds

**Provenance, plainly:** quoted from the WORKING-TREE carrier `GXEMUL-SEC/tools/CLAUDE.md` (byte-identical to the root
`CLAUDE.md` every session loads, and unchanged since 2026-10-22 10:10, so the line numbers match the pass-1 brief's).
`tools/CLAUDE.md` differs from HEAD's copy: R2 and R8 (adopted by owner ruling 2026-10-09) are NOT committed at HEAD
`5986c137`.  They are the rules this round is held to, and they travel here WITH their bounds.  R6 (joint cells) is not
quoted: no question here depends on it.

**R1 -- THE FLOOR** -- `tools/CLAUDE.md` (working tree) lines 1328-1333, VERBATIM:
~~~~
1328| > **THE FLOOR.** A detector is VACUOUS — replace it IN-ROUND — unless it (a) fails on the
1329| > pre-fix build, (b) fails on a **VERBATIM REINSTATEMENT of the removed defect at EVERY fixed
1330| > site**, and (c) fails on a **NULL MEDIUM** -- a product medium carrying none of the behaviour under
1331| > test (the clause-(c) block below says what that is per instrument kind). Below the floor, the
1332| > round's own claim to have "shipped a detector with the fix" is a WRONG RECORD, which the
1333| > stopping rule already fixes in-round.
~~~~

**R2 -- clause (c): the null medium by instrument kind, the pre-fix build, the two record forms** -- `tools/CLAUDE.md` (working tree) lines 1340-1367, VERBATIM:
~~~~
1340| > **ONE criterion -- a product medium carrying none of the behaviour under test -- and its object
1341| > differs by instrument kind:**
1342| > * an offline differential that `#include`s the product: a COMMENT-ONLY product source, which must
1343| >   fail to COMPILE, with a gate that reds on the compile failure (measured for `#488`:
1344| >   `regress/artifacts/shortread/nullmedium_20261009/RECEIPT.txt`);
1345| > * a runtime probe: an ABSENT or NON-EMULATOR binary (every session dies), or a build WITHOUT the
1346| >   device for a device round;
1347| > * an instruction-handler round: an IDENTITY BODY (decode and retire, write nothing) -- the
1348| >   recommended default, two measured legs at `#527`.
1349| >
1350| > **THE PRE-FIX BUILD IS CLAUSE (a)'S MEDIUM AND NEVER CLAUSE (c)'S.**  It carries every behaviour of the
1351| > product, one of them wrong, so a detector can red on it and still pass a comment-only file -- `#446`,
1352| > the instance that created this clause.  A table that wrote "null medium" over a pre-fix leg carries a
1353| > WRONG RECORD (L4: correct it in place, quoting what it refutes, as
1354| > `ppcrldimimask/killtable_20260911/SCORES.txt` does), NOT a floor breach: clause (c) is then
1355| > UNMEASURED there.  **A breach is a genuine null medium coming back GREEN, and nothing else** -- "a
1356| > sharper medium was available" is not a floor criterion (at most clause-(e) debt).
1357| >
1358| > **RECORD CLAUSE (c) IN ONE OF EXACTLY TWO FORMS, never as a bare clause letter beside a row name:**
1359| > * `(c): measured at <artifact>` -- the leg was run and its receipt is durable;
1360| > * `(c): by construction via <row/pin>, leg not run` -- e.g. the gate pins the row count by EQUALITY
1361| >   and a named row reds on a dead run, or the differential `#include`s the product and its gate reds
1362| >   on a compile failure.  **A by-construction claim is checked by READING that shape; where the reading
1363| >   fails -- no runtime gate wiring, no pin, `check_min`, a control computed over the row list
1364| >   (`all([])` is True) -- the leg is OWED** (7n-1's two: the unwired `ppc_rldicl_probe.py` and
1365| >   `alpha_tbi_probe.py`).  Predict a dead run's score from the source, not from the row count (Astra
1366| >   measured luna's at 0/14 with four gate checks red, and SGI's at 6/46 because six rows test only
1367| >   exit status).
~~~~

**R3 -- clause (d)** -- `tools/CLAUDE.md` (working tree) lines 1376-1377, VERBATIM:
~~~~
1376| > **(d) The detector must also fail when the fix is PRESENT but its REPAIR IS NULLED —
1377| > the guard kept, its effect removed.**
~~~~

**R4 -- the two (d) shapes, including the pure-deletion form** -- `tools/CLAUDE.md` (working tree) lines 1428-1433, VERBATIM:
~~~~
1428| > **The two shapes, once the enumeration is right:**
1429| > * **fix ADDS a predicate** -> weaken the added one (unchanged; the original rule).
1430| > * **fix adds none** -> the (d) mutant reroutes an EXISTING guard's repair. For a
1431| >   de-fatalisation: **swap the guard's operand for a field the guarded BODY reads.**
1432| >   For a pure deletion: **re-introduce the removed behaviour under a DIFFERENT predicate**
1433| >   -- not the same one widened, which is (b) wearing (d)'s clothes.
~~~~

**R5 -- the DEPENDS-ON bound** -- `tools/CLAUDE.md` (working tree) lines 1448-1451, VERBATIM:
~~~~
1448| > > **DEPENDS ON enumerates exactly two things: (1) the predicates DOMINATING the diff's
1449| > > edited lines, walked up only to the ENCLOSING FUNCTION BOUNDARY -- never into callees
1450| > > or callers; and (2) for operand-swap forms, swaps drawn ONLY from fields the guarded
1451| > > BODY reads (the guard-field/body-field grep the pre-table check already mandates).**
~~~~

**R7 -- the floor (cells a row is OWED for) versus clause-(e) disclosure** -- `tools/CLAUDE.md` (working tree) lines 1517-1522, VERBATIM:
~~~~
1517| > > **The rule ENUMERATES joint cells wherever the body distinguishes them; the FLOOR -- the cells a row
1518| > > is OWED for -- is the cross-product of the guard's dominating predicates with the device-STATE lvalues
1519| > > the fix's own repair path reads that are JOINTLY REACHABLE through its own data flow.**  The bits of
1520| > > the single value being written are single-operand MARGINALS, not floor; joint cells outside the floor
1521| > > are clause-(e) coverage debt, subject to the one ask-again.  A filter may reject or discharge a cell
1522| > > but may demand a new row only for a floor cell -- so it cannot grow unbounded.
~~~~

**R8 -- rule D2: a relational compare is pinned at its edges** -- `tools/CLAUDE.md` (working tree) lines 1557-1566, VERBATIM:
~~~~
1557| > > For a relational compare against a constant bound B that a fix DEPENDS ON (`X > B`, `e < 96`), each region of its
1558| > > generating set is discharged by the row that varies under the LEAST-OBSERVABLE non-equivalent move of B: **X = B+1
1559| > > for the region past the bound and X = B-1 for the region below it** (the "at" member is dead where the branch maps B
1560| > > to itself).  **A far row proves the branch EXISTS and discharges the BRANCH partition; it never pins the BOUND.**
1561| > > Measured on `#473`'s shipped WDC detector: its rows at 68928 and 4998 let `> 32769` and `> 32766` at each clamp --
1562| > > one-token bound moves -- pass all 128 rows, while rows at 32769 and 32767 red each one
1563| > > (`regress/artifacts/wdc473floor/pass1_20261009/fable5_meas/`).  **Bound: at most two rows per compare the fix
1564| > > depends on -- the compare's own two edges.**  It adds no axis; it moves the rows a region already owes to where the
1565| > > bound is observable, so it cannot become `#392`.  It is the accept-row finding -- *a single accept row pins exactly
1566| > > ONE bound, the one it is near* -- stated for compares.
~~~~

**R9 -- the pre-table check's four rows: SIBLING PARITY, CLAIM -> ROW, GUARD FIELD vs BODY FIELD, CHANNEL** -- `tools/CLAUDE.md` (working tree) lines 1724-1725, lines 1740-1741, VERBATIM:
~~~~
1724| > | **SIBLING PARITY** | for each arm the diff de-fatalises, compare its observable channels against its nearest sibling arm. An asymmetry is a row you owe or a sentence you owe | a de-fatalised arm with NO completion-event row while its sibling had one |
1725| > | **CLAIM -> ROW** | every ADDED comment sentence asserting an OBSERVABLE CONSEQUENCE owes a row or an explicit no-row sentence. Claim verbs (*observes, controls, pins, proves, the X control*) are EXAMPLES, not the test | a "device-signature control" claimed in prose and implemented by nothing |
  ...
1740| > | **GUARD FIELD vs BODY FIELD** | list fields the PREDICATE reads and fields the guarded BODY reads; where they differ, grep whether they are written at the same sites. If not, the detector owes a state where they DISAGREE.  **Also record, per lvalue, the PARTITION THE BODY INDUCES on it** (its tested masks and compare regions) -- EXHAUSTED / SAMPLED is read off this column, never asserted (7n-5, 2026-10-09) | the guard's operand swapped for a field whose third state no row built |
1741| > | **CHANNEL** | for each row, name **the mutant it kills** and **the observable that differs under that mutant**. A row whose named channel cannot vary under its named mutant is VACUOUS BY CONSTRUCTION, and that is knowable at writing time, before any table runs | a survival oracle at a REFUSAL-EFFECT site: guarded and unguarded code both survive |
~~~~

**R10 -- clause (e): the contract** -- `tools/CLAUDE.md` (working tree) lines 1801-1805, VERBATIM:
~~~~
1801| > **(e) THE CONTRACT.** The probe header names which edits this detector is designed
1802| > to catch. *A detector that says so is falsifiable; one claiming completeness is
1803| > not* -- and a later escape becomes "outside the contract" or "a breach of it",
1804| > which are different dispositions, rather than an argument about overclaiming.
1805| > Two lines in a header.
~~~~

**R11 -- clause (f): the anchor rule** -- `tools/CLAUDE.md` (working tree) lines 1814-1817, VERBATIM:
~~~~
1814| > **Rows that assert only PAIRWISE DISTINCTNESS, or a same-path round-trip, test the decode
1815| > against ITSELF.** They are therefore invariant under any edit that re-maps addresses
1816| > INJECTIVELY over the probed set -- translations first among them -- and they catch a re-map
1817| > only where it COLLIDES on that set.
~~~~

**R12 -- the de-escalation clause** -- `tools/CLAUDE.md` (working tree) lines 2406-2415, VERBATIM:
~~~~
2406| > **A fatal→survive fix DELETES THE ACCIDENTAL TRIPWIRE that made guard-mask growth
2407| > self-announcing.** Before #447, adding `| TCR_UNIE` to a guard mask meant `exit(1)` on the
2408| > first legal write — unmissable. After it, the same edit means a **silently refused write** and
2409| > nothing anywhere notices.
2410| >
2411| > So: **when a fix removes a host-fatal guard, enumerate from the diff every predicate that used
2412| > to gate death, and the detector shipping with that fix must pin the ACCEPT SIDE of each** — a
2413| > row per adjacent modelled bit or value, proving legal writes still land. Those rows are part
2414| > of the FIX'S COST, not future strengthening, because the fix itself destroyed the old
2415| > (accidental) detector for that class.
~~~~

**R13 -- accept-row failability, by its discriminator** -- `tools/CLAUDE.md` (working tree) lines 2452-2458, VERBATIM:
~~~~
2452| > **THE RULE, BY ITS DISCRIMINATOR:** the accept row must redden under the **least-observable
2453| > growth form that is measured NON-EQUIVALENT at that site**. Find it by the reading the rule
2454| > already mandates — read the latch/store arm and cite its line. Where the latch operand CAN
2455| > mask the guard, guard-only is equivalent and JOINT is that form. Where the latch operand is a
2456| > constant the guard cannot feed, guard-only is non-equivalent AND quieter, so it is that form.
2457| > **"Build the form the latch operand does not mask"** is the generalisation, and it is not a
2458| > new rule — it is this rule's own reason made explicit.
~~~~

**R14 -- a row list rewritten from a panel's findings is diffed against the pre-table block** -- `tools/CLAUDE.md` (working tree) lines 1670-1673, VERBATIM:
~~~~
1670| > > > **A ROW LIST REWRITTEN FROM A PANEL'S FINDINGS IS DIFFED AGAINST THE PRE-TABLE BLOCK'S
1671| > > > OWN PRESCRIBED ROWS, NOT MERELY EXTENDED WITH THE NEW ONES.** The block PRESCRIBES rows;
1672| > > > a later list that does not contain them has dropped an obligation, and the diff is the
1673| > > > only thing that says so.
~~~~

**R15 -- the ask-again: capped at ONE ask, and the cap counts asks, not findings** -- `tools/CLAUDE.md` (working tree) lines 2471-2475, lines 2481-2483, VERBATIM:
~~~~
2471| > **CAPPED AT ONE ASK-AGAIN PER DETECTOR PER ROUND.** This is not the #392 chain — #392 was
2472| > unbounded fix-of-fix passes with no stop condition; this is a single extra adversarial query
2473| > against a clean table with a measured stop: nothing found, done; something found, row added
2474| > under L1, done. **The cap IS the anti-#392 clause.** A second ask-again after an empty first
2475| > is exactly where the chain starts, and anything found past the cap is FILED, never fixed.
  ...
2481| > > Everything ONE ask returns is disposed of INDIVIDUALLY under L1–L4 and the floor — and **a
2482| > > floor breach among the findings is L2, repaired in-round however late it is found.** A
2483| > > second ASK is where the #392 chain starts; the number of rows one ask yields is not.
~~~~

**R16 -- the four licences for an in-round fix of detector material (everything else is FILED)** -- `tools/CLAUDE.md` (working tree) lines 2608-2618, VERBATIM:
~~~~
2608| > Everything else is FILED. Named so no round has to re-argue it:
2609| >
2610| > * **L1 — pre-ship construction.** The row is part of the deliverable still being built. A row
2611| >   measured vacuous before commit is unfinished, not a reopening. **The stopping rule governs
2612| >   findings against SHIPPED material only.**
2613| > * **L2 — floor breach.** The shipped detector fails vacuity-floor clause (a), (b) or (c) —
2614| >   replace in-round however late it is found.
2615| > * **L3 — undischarged obligation.** The row is the sole carrier of something the round OWES
2616| >   (a de-escalation accept row; the "shipped a detector" claim itself). A vacuous sole carrier
2617| >   makes the round's record false.
2618| > * **L4 — wrong record.** Prose or comments claiming coverage a measurement refutes.
~~~~

**R17 -- the oracle-order discriminator, and its "the code does not move" clause** -- `tools/CLAUDE.md` (working tree) lines 2511-2513, lines 2518-2523, VERBATIM:
~~~~
2511| > > **Re-pin the oracle FIRST. Measure the COMMITTED build RED under the new expectations.
2512| > > THEN change the code.** Same scripts, opposite colour. If you cannot show that red, you
2513| > > do not have test-first, and the re-pin collapses into laundering.
  ...
2518| > > While the defect is still open, the committed build IS the pre-fix build: re-pin the oracle, measure
2519| > > HEAD RED at one input in the corrected region, and keep that receipt at a durable path dated before
2520| > > any handler edit -- it is the order discriminator AND the row's witness.  A divergence argument or a
2521| > > documentary provenance record (a CHANGELOG passage, a commit message) is CORROBORATION, never a
2522| > > substitute for that red, and a retrospective run against a reconstructed pre-fix tree supplies a red
2523| > > but not an authentic pre-edit DATE.  **Bound: one measured red per oracle a ROW CONSUMES**; a helper no
~~~~

**R18 -- the bound on the `detector:` witness term** -- `tools/CLAUDE.md` (working tree) lines 2963-2967, VERBATIM:
~~~~
2963| > **THE BOUND: `detector:` IS NOT A RUNG.** It records that a fix shipped with a MEASURED
2964| > DETECTOR and no guest-path witness. It ranks BELOW every access witness, and it does NOT
2965| > satisfy the reproduce-before-you-edit step: **a round using it still owes the rung-3 ATTEMPT**
2966| > the 2026-08-27 lifecycle ruling requires, and must record that the attempt was made and what
2967| > it found. The one thing it may never mean is *we did not think to ask*.
~~~~

**R19 -- a preserved log is verified by its completion sentinel** -- `tools/CLAUDE.md` (working tree) lines 3507-3509, VERBATIM:
~~~~
3507| > > **THE RULE, and it costs one line: A PRESERVED LOG IS VERIFIED BY ITS COMPLETION SENTINEL,
3508| > > NOT BY ITS EXISTENCE.** Every probe in this tree emits one (`TPROBE2_DONE`, `TARGETED_DONE`,
3509| > > `FREEZE_DONE`, `REGRESS_PASS`). `tail -1` before citing, and re-copy if it is absent.
~~~~

**R20 -- the repair chain: a closing pass must be a VALID pass** -- `tools/CLAUDE.md` (working tree) lines 2670-2674, VERBATIM:
~~~~
2670| > > **A closing pass must be a VALID pass: the diff actually delivered; the roster complete or
2671| > > its misses named per the seat ledger; and the zero carried WITH ITS DENOMINATOR -- which
2672| > > cells, which mutant shapes, were swept.** *"Zero found"* and *"zero looked for"* must not
2673| > > render the same, which is this project's oldest rule about blanks turned on its own stop
2674| > > condition.
~~~~

**R21 -- the repair chain: effort on the diff, the floor question on the composite** -- `tools/CLAUDE.md` (working tree) lines 2686-2688, VERBATIM:
~~~~
2686| > > **Review EFFORT is scoped to the repair diff, so settled design is not re-litigated. The
2687| > > FLOOR QUESTION -- does a clean-sweep mutant exist in the (d) enumeration -- is asked of the
2688| > > SHIPPED COMPOSITE on every pass.**
~~~~

---

## 11. QUESTIONS -- VERDICT LINE FIRST (format in section 0)

**Q1 -- THE FIX: exactly the agreed repair, and nothing else?**

(a) Is the generator diff (7.1) exactly the agreed repair -- the WHOLE arm removed (A1: the condition, its
`printf("\tNULL")`, the `continue`, the brace), `loadstore()`'s early return kept (A2, S1), the decoder untouched (A3;
`cpu_m88k_instr.c` is byte-identical to HEAD) -- and nothing else?  Walk the 4 removed and the 8 added lines.

(b) Is the regenerated table (7.2) exactly the 24 `NULL` -> name lines and nothing else -- 24 of 24 changed lines, 272
`NULL`, 512 entries?  WALK THE 24: for each index decode (kind, endianness, `.usr`, PC-sync) from the index formula in
the driver's header (7.4, lines 117-120), and say whether the new name is the handler the architecture requires for that
cell (S5).  Every big-endian slot carries an `_le` name -- confirm that this is the existing byte idiom (S5), not an error.

(c) CLAIM -> ROW (R9): for each sentence of the `#569` comment (generator :254-261) -- "no NULL arm for scaled byte
accesses"; "A byte's scale factor is 1, so a scaled byte access is the unscaled one"; "print_function_name() already omits
"_scaled" for size 0"; "these 24 slots name the unscaled byte handlers"; "They were NULL"; "xmem_slow() calls them
unguarded while the ld/st decoder installs them as ic->f (both in cpu_m88k_instr.c)" -- does a row observe it, or does it
carry an explicit no-row basis (PRETABLE.out section 2, C1-C6)?  Answer P1.  Then the same for the GATE 2 block's
comment (7.3) and for the driver header's CONTRACT sentences (7.4, lines 30-74).

(d) Does deleting the arm change any OTHER generated output -- the separator logic (generator :235-237), the stderr
`generated_functions` count, the other three `NULL` arms?  The measured facts are `gen_count` 198 and `fresh_lsn` 198
green in `fixed.out`, and, in each build tree, make regenerated the table and it `cmp`s clean against GXEMUL-SEC's
(CLEARANCE.out).

**Q2 -- THE DETECTOR AS SHIPPED: do the 123 rows discharge what pass 1 ruled, and is any of them vacuous?**

(a) Do the 123 rows discharge B1-B12 AS AMENDED BY E?  Walk them: the absolute per-index pins at all 24 cells in BOTH
artifacts (B2); the accept pins 161 177 434 438 418 422 144 400 404 (B3); the 21 counterpart rows; the structural rows
(B4); the generator compile AND execution status rows `gen_compiles`, `gen_exit`, `gen_stdout`, `gen_count` (B5); fresh
== committed (B1 iii); one identity per row, each pinned by the gate (B10); the enumerated total 123 (B12; S15).

(b) VACUOUS BY CONSTRUCTION (R9, the CHANNEL line): is any row's named observable unable to vary under its named leg?
PRETABLE.out section 5 names the channel per row group; PRETABLE_v3 section 5 the changed rows.  PRETABLE.out says
`committed_lsn` and both sides' `_present` / `_inits` / `_entries` rows have no red leg except a null medium -- disclosed,
or vacuous?

(c) THE CONTRACT (R10): does the header (7.4, lines 30-79) state the floor (all 24), the guest-consumer subset (16) and
what the detector does NOT observe?  Does it claim anything no row observes (an L4 candidate)?

(d) Answer P8.

(e) Answer P6.

(f) **THE ONE ASK-AGAIN** (R15: the project allows exactly one after a clean table; everything it returns is disposed of
individually, and a floor breach among the findings is L2).  Is there a change to the generator or to the committed
table under which all 123 rows stay green while a cell the CONTRACT claims dispatches differently?  Say whether one
exists.  If it does, name WHERE it acts (the generator line, or the table index), the row you expect to stay green, and
why that row's observable cannot vary under it -- describe it; do not write patch text.  If none exists inside the
contract, say so and give the partition argument (which inputs the repair changes the answer for, and which rows see
each).

**Q3 -- THE LEGS: do the measurements say what the records say they say?**

(a) Do the measured red sets equal PRETABLE_v3 section 4's predictions ROW BY ROW?  SCORES.txt's per-run "measured red"
lines are the measured side.  Walk all 16 runs.

(b) Is each red for the reason under test (SCORES.txt's got= values -- e.g. L3's `gen_compiles` reads "no -- the compile
or link failed", L5's `fresh_pin416` reads `NULL`)?

(c) The floor, clause by clause, each with its named receipt (R1-R4): (a) pre-fix red -- PRE; (b) verbatim
reinstatement at BOTH fixed sites -- L1 (generator), L2 (table); (c) null media -- L3, L4, recorded in R2's
"(c): measured at" form; (d) the nulled repair -- L5, L6.  Is each discharged?  Does any clause rest on a SUPPLEMENTARY
leg (L8, L5b, S1-S5)?

(d) Answer P5 against R17 -- note its sentence "a retrospective run against a reconstructed pre-fix tree supplies a red
but not an authentic pre-edit DATE", and its bound "one measured red per oracle a ROW CONSUMES".

**Q4 -- WIRING, CLEARANCE, GATES**

(a) The GATE 2 block (7.3): its placement (after `#375`, before `b1w`), the `-x` check, `row failures == 0` and
`rows run == 123` by EQUALITY, the sentinel, the 123 identity pins -- is anything wrong or unsupported?  Answer P3 and
P4.  The new file must be committed mode 100755 (S19): what, at landing, verifies that it was?

(b) Does the staged `gate_offline.sh` carry ONLY this round's hunk?  (7.3: one hunk, +45 -0; the builder's
`staged/insert_HEAD.diff` and `staged/insert_WT.diff` differ only in their two `---`/`+++` header lines.)

(c) The four-tree clearance (9.11): part 1 on all four trees, part 2 on the three build trees, `est/: source tree, part 2
N/A`; the in-tree regeneration fired once per build tree.  Sound?

(d) GATE 2 `PASS (502 checks)` and GATE 11 `PASS (111 checks)` (9.12, 9.13): answer P2 -- which tree do these results
describe, and what may the record and the commit message claim?  (BUILD_REPORT D-10.)

(e) Answer P7.  And S20: is anything owed, or worth FILING, because nothing outside the GATE 2 block notices if that
block, or the driver's execution, goes away?

**Q5 -- RECORDS, AND ANYTHING ELSE**

(a) What must the CHANGELOG `#569` block, OUTSTANDING_BUGS.md (lines 28-29 and 25260-25263) and the ledger row say at
landing?  At least: the witness term `detector:regress/diff_m88k_loadstore_gen.sh` with the BLOCKED rung-3 attempt named
(R18); the two filed rows `m88kxmemaddrovl` and `m88klepsrbo` (S16); a state_note no longer saying "DISPUTED"; the
witness record and the round's artifacts directory TRACKED.  Check also what this packet shows: the ledger row has NO
`entries` field yet (the pass-1 seats, the adjudication and their directories are unrecorded); the Fable stage is HELD
(`fable5.HELD.txt` carries its hold question), and HEAD's newest round `#568` landed "held for Fable" (section 4, part 1,
`2ca79b90`); `PASS1_RULINGS.md` lines 3-11 still carry the pre-adjudication roster -- "3 of 4 rostered seats", "NOT FIRED
by owner roster: agy, kimi, deepseek, minimax, opus5", "Every seat answered; no seat failure" -- although DeepSeek
answered on 2026-10-23 and Argon was a seat failure (section 3.1; the adjudication asked for that replacement at
`adj/codex_t1p1adj.txt:73`).  What else does the landing owe?

(b) The builder's disagreements D-1..D-10 and open questions 1-4 (BUILD_REPORT sections 7-8, inlined in 9.1): which need
a disposition, and what should it be?

(c) **The standing licence.**  If, while verifying a claim, you found something ELSE -- say so, with the file and the
grep anchor (or line) that settles it.

---

## 12. Every path this brief names -- checked with `ls` at drafting time (`LS_PERMITTED.txt`)
~~~~
# Every path the T1 / #569 pass-2 brief names, checked 2026-10-23 11:08:40 -0500.  HEAD 5986c137.
# Repo paths are relative to C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC; 'tracked' = in git ls-files (an index READ).

tracked        7970  2026-10-23 09:46  src/cpus/generate_m88k_loadstore.c
tracked       89953  2026-10-23 09:47  src/cpus/tmp_m88k_loadstore.c
tracked      112887  2026-09-05 14:13  src/cpus/cpu_m88k_instr.c
tracked       11307  2021-04-22 13:04  src/cpus/cpu_m88k_instr_loadstore.c
tracked       58158  2026-07-17 14:59  src/cpus/cpu_dyntrans.c
tracked       48146  2026-09-06 08:58  src/cpus/cpu_m88k.c
tracked        6776  2021-04-22 13:04  src/cpus/Makefile.skel
tracked      178729  2026-10-23 10:01  regress/gate_offline.sh
UNTRACKED     14528  2026-10-23 09:59  regress/diff_m88k_loadstore_gen.sh
tracked       10201  2026-08-14 03:14  regress/diff_autodev_gen.sh
tracked       17714  2026-08-15 18:39  regress/lib.sh
tracked        6138  2026-08-13 22:49  regress/run.sh
tracked       30535  2026-10-16 21:48  regress/gate_m88k_rounding.sh
tracked      247563  2026-10-09 19:44  regress/diff_wdc_identify.c
tracked       57333  2026-10-09 19:43  tools/BRIEF_TEMPLATE.md
tracked      309189  2026-10-22 10:10  tools/CLAUDE.md
tracked       79586  2026-10-21 07:30  tools/precommit_check.sh
tracked         986  2026-08-27 14:53  tools/est_divergence.txt
tracked      367900  2026-10-22 23:35  tools/pipeline/check_probe_wiring.py
tracked     9774241  2026-10-22 22:37  tools/pipeline/ledger.json
tracked     2714461  2026-10-22 15:42  CHANGELOG.md
tracked     1927897  2026-10-22 22:15  OUTSTANDING_BUGS.md
tracked        6883  2026-10-22 15:42  regress/artifacts/research_20261022/crit_20261022/CRIT_RULINGS.md
UNTRACKED      1917  2026-10-22 22:38  regress/artifacts/m88kscaledbyte/witness_attempt_20261022/WITNESS_ATTEMPT.md
UNTRACKED    109037  2026-10-22 23:12  regress/artifacts/m88kscaledbyte/pass1_20261022/packet.md
UNTRACKED     15963  2026-10-23 09:53  regress/artifacts/m88kscaledbyte/pass1_20261022/PASS1_RULINGS.md
UNTRACKED      7402  2026-10-23 09:54  regress/artifacts/m88kscaledbyte/pass1_20261022/CHECKS_mainloop.md
UNTRACKED     13229  2026-10-23 09:54  regress/artifacts/m88kscaledbyte/pass1_20261022/BUILD_SPEC.md
UNTRACKED       907  2026-10-22 23:12  regress/artifacts/m88kscaledbyte/pass1_20261022/fable5.HELD.txt
UNTRACKED       805  2026-10-23 09:44  regress/artifacts/m88kscaledbyte/pass1_20261022/argon_t1p1.DROPPED.txt
UNTRACKED     10134  2026-10-23 09:52  regress/artifacts/m88kscaledbyte/pass1_20261022/adj/codex_t1p1adj.txt
UNTRACKED     19643  2026-10-22 23:23  regress/artifacts/m88kscaledbyte/pass1_20261022/codex_t1p1.txt
UNTRACKED     21832  2026-10-22 23:28  regress/artifacts/m88kscaledbyte/pass1_20261022/grok_t1p1.txt
UNTRACKED     17585  2026-10-22 23:19  regress/artifacts/m88kscaledbyte/pass1_20261022/ollama_glm_t1p1_Q12.txt
UNTRACKED     10345  2026-10-23 09:34  regress/artifacts/m88kscaledbyte/pass1_20261022/ollama_deepseek_t1p1_Q12.txt
UNTRACKED      1468  2026-10-23 09:54  regress/artifacts/m88kscaledbyte/pass1_20261022/MANIFEST.md5
UNTRACKED     12461  2026-10-23 10:20  regress/artifacts/m88kscaledbyte/table1_20261022/BUILD_REPORT.md
UNTRACKED     12583  2026-10-23 10:04  regress/artifacts/m88kscaledbyte/table1_20261022/SCORES.txt
UNTRACKED     14400  2026-10-22 23:45  regress/artifacts/m88kscaledbyte/table1_20261022/PRETABLE.out
UNTRACKED      6492  2026-10-23 10:02  regress/artifacts/m88kscaledbyte/table1_20261022/PRETABLE_v3.out
UNTRACKED      2312  2026-10-23 09:40  regress/artifacts/m88kscaledbyte/table1_20261022/PRETABLE_L8.out
UNTRACKED      4913  2026-10-23 10:03  regress/artifacts/m88kscaledbyte/table1_20261022/RUNS.log
UNTRACKED      8249  2026-10-23 10:07  regress/artifacts/m88kscaledbyte/table1_20261022/CLEARANCE.out
UNTRACKED      2259  2026-10-23 10:03  regress/artifacts/m88kscaledbyte/table1_20261022/DUPNAMES.out
UNTRACKED      1966  2026-10-23 10:17  regress/artifacts/m88kscaledbyte/table1_20261022/FIX.out
UNTRACKED      9907  2026-10-22 23:42  regress/artifacts/m88kscaledbyte/table1_20261022/BASELINE.out
UNTRACKED     24368  2026-10-23 10:12  regress/artifacts/m88kscaledbyte/table1_20261022/GATE2_tail.out
UNTRACKED     13649  2026-10-23 10:12  regress/artifacts/m88kscaledbyte/table1_20261022/GATE2_diff_m88k_loadstore_gen.log
UNTRACKED     10482  2026-10-23 10:17  regress/artifacts/m88kscaledbyte/table1_20261022/GATE11_tail.out
UNTRACKED     13649  2026-10-23 10:03  regress/artifacts/m88kscaledbyte/table1_20261022/fixed.out
UNTRACKED     14251  2026-10-23 10:03  regress/artifacts/m88kscaledbyte/table1_20261022/prefix_HEAD_v3.out
UNTRACKED     12923  2026-10-23 09:46  regress/artifacts/m88kscaledbyte/table1_20261022/driver_v1/prefix_HEAD.out
UNTRACKED       577  2026-10-23 09:58  regress/artifacts/m88kscaledbyte/table1_20261022/driver_v1/prefix_HEAD.meta
UNTRACKED     12224  2026-10-23 09:47  regress/artifacts/m88kscaledbyte/table1_20261022/driver_v1/fixed.out
UNTRACKED       398  2026-10-23 09:58  regress/artifacts/m88kscaledbyte/table1_20261022/driver_v1/fixed.meta
UNTRACKED      1801  2026-10-23 09:51  regress/artifacts/m88kscaledbyte/table1_20261022/driver_v1/RERUN_v2.txt
UNTRACKED       796  2026-10-23 09:51  regress/artifacts/m88kscaledbyte/table1_20261022/driver_v1/driver_v1_to_v2.diff
UNTRACKED     14122  2026-10-23 10:18  regress/artifacts/m88kscaledbyte/table1_20261022/driver_v2_to_v3.diff
UNTRACKED    174494  2026-10-23 10:01  regress/artifacts/m88kscaledbyte/table1_20261022/staged/gate_offline.sh
UNTRACKED      3412  2026-10-23 10:01  regress/artifacts/m88kscaledbyte/table1_20261022/staged/insert_HEAD.diff
UNTRACKED      3419  2026-10-23 10:01  regress/artifacts/m88kscaledbyte/table1_20261022/staged/insert_WT.diff
UNTRACKED     14129  2026-10-23 10:03  regress/artifacts/m88kscaledbyte/table1_20261022/L1_headgen.out
UNTRACKED     14129  2026-10-23 10:03  regress/artifacts/m88kscaledbyte/table1_20261022/L2_headtable.out
UNTRACKED     14535  2026-10-23 10:03  regress/artifacts/m88kscaledbyte/table1_20261022/L3_commentgen.out
UNTRACKED     14463  2026-10-23 10:03  regress/artifacts/m88kscaledbyte/table1_20261022/L4_commenttable.out
UNTRACKED     13982  2026-10-23 10:03  regress/artifacts/m88kscaledbyte/table1_20261022/L5_v2nopcsync.out
UNTRACKED     13960  2026-10-23 10:03  regress/artifacts/m88kscaledbyte/table1_20261022/L6_lehalf.out
UNTRACKED     14025  2026-10-23 10:03  regress/artifacts/m88kscaledbyte/table1_20261022/L7_v6halfword.out
UNTRACKED     14623  2026-10-23 10:03  regress/artifacts/m88kscaledbyte/table1_20261022/L8_allnull.out
UNTRACKED     14330  2026-10-23 10:03  regress/artifacts/m88kscaledbyte/table1_20261022/L5b_codexnopcsync.out
UNTRACKED     13908  2026-10-23 10:03  regress/artifacts/m88kscaledbyte/table1_20261022/S1_noearlyreturn.out
UNTRACKED     13562  2026-10-23 10:03  regress/artifacts/m88kscaledbyte/table1_20261022/S2_exit1.out
UNTRACKED     14528  2026-10-23 10:03  regress/artifacts/m88kscaledbyte/table1_20261022/S3_emptyout.out
UNTRACKED     14192  2026-10-23 10:03  regress/artifacts/m88kscaledbyte/table1_20261022/S4_notable.out
UNTRACKED     14268  2026-10-23 10:03  regress/artifacts/m88kscaledbyte/table1_20261022/S5_nogen.out

# outside the repository (paths relative to C:/DocumentNoSnc/cc/GXEMUL)
present      775987  2026-07-30 02:14  _scratchpad/mc88100.txt
present        1464  2026-10-04 21:44  _scratchpad/nightly/verdict_20261004_180001.txt
present        1462  2026-10-11 22:02  _scratchpad/nightly/verdict_20261011_180002.txt
present        1454  2026-10-19 03:51  _scratchpad/nightly/verdict_20261018_231924.txt
present      495537  2026-10-19 03:51  _scratchpad/nightly/battery_20261018_231924.log
present      474446  2026-10-11 22:02  _scratchpad/nightly/battery_20261011_180002.log
present      471758  2026-10-04 21:44  _scratchpad/nightly/battery_20261004_180001.log
present        7970  2026-10-23 09:53  est/src/cpus/generate_m88k_loadstore.c
present       89953  2026-10-23 09:53  est/src/cpus/tmp_m88k_loadstore.c
present        7970  2026-10-23 09:53  build/src/cpus/generate_m88k_loadstore.c
present       89953  2026-10-23 09:53  build/src/cpus/tmp_m88k_loadstore.c
present     6159736  2026-10-23 09:54  build/gxemul
present        7970  2026-10-23 10:04  build-asan/src/cpus/generate_m88k_loadstore.c
present       89953  2026-10-23 10:05  build-asan/src/cpus/tmp_m88k_loadstore.c
present   107506096  2026-10-23 10:06  build-asan/gxemul
present      309189  2026-10-22 10:10  CLAUDE.md

MISSING count: 0
UNTRACKED count: 53 (the new driver and the whole round artifacts directory; nothing else)
NOTE: tools/CLAUDE.md and tools/BRIEF_TEMPLATE.md are quoted from the WORKING TREE; both differ from HEAD.
      regress/gate_offline.sh and regress/diff_wdc_identify.c carry other sessions' uncommitted edits (section 0).
~~~~

BRIEF2_FULL_DONE
