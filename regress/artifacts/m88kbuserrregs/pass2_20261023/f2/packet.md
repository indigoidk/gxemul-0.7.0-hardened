# F2 -- the ADJUDICATION PASS of T36 (`m88kbuserrregs`, round `#570`) PASS 2 -- for GPT-6 Astra (adjudicator; owner roster 2026-10-23/24)

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

You adjudicate the pass-2 (diff) review of one regression-testing round in the GXemul hardened fork (a correctness fix to
the m88k memory model -- two CMMU fault-status registers now written on a refused device access -- and its measured 31-row
regression detector).  FIVE reviewing seats answered on the uncommitted diff; the main loop read every answer whole and
wrote its dispositions in `..\PASS2_RULINGS.md` (A1-A3, B1-B5, C1-C6 + D1, D2-D9: twenty-four).  **Your job is to find
which of those dispositions is WRONG**, rule the disputes below by argument and by the source (you may open every file
named here, the working tree -- which carries the round's uncommitted edits and, unrelated, the peer's uncommitted files
named in `..\packet.md` section 0 -- and HEAD `7fca7187` via `git show`), and be HARDER on the positions that adopted YOUR
OWN pass-2 answer than on the others.  Do not build or run anything; do not propose reproduction recipes; dispositions by
id, answer-file:line where you cite a seat.

Paths: `A\` = `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\m88kbuserrregs\`; this pass = `A\pass2_20261023\`;
the build = `A\table1_20261023\` (BUILD_REPORT.md, SCORES.txt, PRETABLE.out, fix570.diff, staged\, gates\, boot_ab\);
pass 1 = `A\pass1_20261023\` (PASS1_RULINGS.md section E is the adjudicated design; BUILD_SPEC.md sections 10-11).

## 1. The seats and where their answers are

| seat | file | verdict | class |
|---|---|---|---|
| GPT-6 Astra (you, as reviewer) | `..\codex_t36p2.txt` | SHIP WITH CHANGES | file-reading |
| Grok 4.7 (xhigh, plan mode) | `..\grok_t36p2.txt` | SHIP WITH CHANGES | file-reading (working tree) |
| GLM 5.3 | `..\ollama_glm_t36p2_Q12.txt`, `..\ollama_glm_t36p2_Q34.txt` | SHIP WITH CHANGES (both) | packet-fed (`..\packet_compact.md`) |
| DeepSeek v4-pro | `..\ollama_deepseek_t36p2_Q12.txt`, `..\ollama_deepseek_t36p2_Q34.txt` | **DO NOT SHIP** (Q1-2: one claimed floor breach, D1) / SHIP WITH CHANGES (Q3-4) | packet-fed |
| Gemini 4 Argon (through agy, `gemini-4-argon-high`) | `..\argon_agy_t36p2.txt` (verdict and body appended in section 6 below) | see section 6 | file-reading (the compact packet + the tree) |
| Fable 5.1 | `..\fable5.HELD.txt` | HELD by the owner, with its question | -- |
| agy (other than as Argon's transport), kimi, minimax, Opus-as-seat | `..\roster_NOT_FIRED.txt` | DELIBERATELY NOT FIRED | -- |

The brief the seats answered: `..\packet.md` (FULL, 268 KB, every diff inlined) / `..\packet_compact.md` (75 KB).  The
drafter's inconsistency list, which seeded the brief's P1-P15: the scratchpad `NOTES.md` is summarised in the brief's
section 6.

## 2. The dispositions under test -- `..\PASS2_RULINGS.md`

* **A1-A3** the executable diff ships as is (five readings agree; no executable defect, no floor breach).
* **B1-B5** five comment sentences IN THE DIFF corrected before commit (L4; comment-only; line counts kept; est/ mirrored;
  object compare redone; clearance re-run): the `:361` citation (B1); the "(the debugger)" parenthetical (B2); the
  `~10^5` count scoped (B3); "writes only PFSR and PFAR" narrowed to the fault paths (B4); the CMMU-less sentence narrowed
  with the no-row disclosure for the instruction label's delivery (B5).
* **C1-C6** the floor discharged on (a)-(d) with the (a) record in the probe-measured form (never the clause-(c)
  by-construction form); the ask-again candidates of all seats graded clause (e), with the main loop's `CACHE_NONE`
  caller census for GLM's third-cache-class candidate.
* **D1** DeepSeek's claimed L2 ("CMMU-owner confusion": a fallback to the bootstrap cpu's CMMU when the faulting cpu has
  none) REJECTED as a breach, graded clause (e) under the DEPENDS-ON bound and the joint-cell rule ("exactly when the
  guarded body's own code distinguishes them"); Astra's own AA6 reached the same grade.
* **D2** the shipped probe's header: ONE docstring-only re-freeze (rev 2b) fixing P3, P10, P6, F15, P13 together, the
  frozen rev-2 artifact untouched, rev 2b re-run on the fixed and the HEAD binaries, both md5s recorded -- AGAINST GLM's
  errata-only position.
* **D3** the gate comment's two missing qualifiers added in the live and staged `gate_arm.sh` (comment-only; the gate ran
  the pre-edit file, recorded; no re-run).
* **D4** `staged/gate_arm.sh` renamed `.sh.txt` (Q19) with a README note; the MANIFEST's "27 of 27 as predicted" qualified
  with L22's prediction location.
* **D5** PRETABLE untouched; a dated note beside it (L22's prediction at BUILDER_QUESTIONS Q18 / BUILD_SPEC §11 Q18; the
  draft-id map; AMENDMENT 1's self-stated time vs mtime); SCORES.txt gains the 60-char truncation pointer.
* **D6-D9** the CHANGELOG, OUTSTANDING_BUGS, ledger and commit-scoping requirements as enumerated.

## 3. The disputes -- each side in its own words

**D1 -- is "CMMU-owner confusion" a floor breach?**
* DeepSeek (`..\ollama_deepseek_t36p2_Q12.txt:39`): "Clause (d) floor breach.  The null-CMMU cell is floor, but no row
  detects a mutant that uses the boot CPU's CMMU when the faulting CPU has no CMMU ... `null route` and `null surv` stay
  green because cpu1 still takes the exception and survives.  The repair's effect for the faulting CPU is nulled, guard
  shape kept.  This is a clause (d) breach, L2."
* Astra (`..\codex_t36p2.txt:142`): "AA6 Wrong-CPU CMMU selection | CPU sample, including LUNA multi-CPU configurations |
  CLAUSE (e); beyond the adjudicated CPU-independent cross-product".  Grok and GLM did not raise the cell.
* Main loop: clause (e) -- the guarded body distinguishes `cmmu == NULL` from not; nothing in it distinguishes which cpu
  owns a CMMU; the variant is an added fallback, not a weakening of a dominating predicate or a body-read operand swap.
  Question: is that reading of the bound right, and does E's "a survival control with a real channel discharges the
  floor obligation" for the NULL cell cover a variant that writes SOMEONE ELSE'S registers while surviving?

**D2 -- re-freeze the shipped probe's docstring, or errata only?**
* Astra (`..\codex_t36p2.txt:157`): "Preserve the exact measured rev-2 artifact and its historical hash.  A corrected
  live header changes file identity: record its new identity and documentation-only relationship to the measured
  instrument."  Grok (`..\grok_t36p2.txt:90`): "Correct the sentence.  The table ran on the frozen bytes.  Keep that
  frozen copy as the instrument, and record the new md5 of the shipped probe and that the row logic did not change."
* GLM (`..\ollama_glm_t36p2_Q12.txt:8`): "a records erratum beside the frozen md5; do not re-freeze the instrument for a
  non-load-bearing sentence (P13's byte-identity is worth more)"; (`..\ollama_glm_t36p2_Q34.txt:6`): "erratum + correct
  CHANGELOG rationale; do not edit the frozen header".
* Main loop: ONE docstring-only re-freeze of the SHIPPED copy, the frozen artifact untouched, rev 2b re-run on both
  binaries, both md5s in the records.  Question: is a committed detector whose header carries a known false sentence
  acceptable with an erratum, or is the re-freeze (seconds of cost) the right call -- and does the re-run on both
  binaries satisfy "the measured instrument" for the gate pin, whose receipt names `d57c12ab`?

**D3 -- grades of two comment items.**  P1 ("(the debugger)"): Astra, Grok, GLM-Q34 and DeepSeek grade it L4 / reword;
GLM-Q12 "not an L4, a one-word fix affordable but not required".  P14 (the gate comment's missing qualifiers): Astra and
Grok "add the qualifiers"; GLM-Q34 "acceptable only with A8 verbatim in the CHANGELOG; better add them"; DeepSeek L4.
Main loop: both edited in place (B2, D3).

**D4 -- the (a) record form (settled unanimous, listed for completeness):** measured at the probe; the gate pins would red
by inspection; never the clause-(c) by-construction form; the gate never ran the block pre-fix (departure 3).

## 4. The questions -- VERDICT LINE FIRST (`VERDICT: UPHOLD | AMEND | REJECT -- <one line>`), then by id

Q1. Of the TWENTY-FOUR dispositions (A1-A3, B1-B5, C1-C6, D1-D9), which are WRONG, and why (file:line)?  Name the ones you
    are least sure of even if you uphold them.
Q2. Rule D1, D2 and D3 in your own words against the source and the quoted rule text (the DEPENDS-ON bound; the
    joint-cell "exactly when the body distinguishes them" rule; E's survival ruling for the NULL cell; the L1-L4 licence
    list; the frozen-instrument rule).  For D1 say explicitly whether a `null owner` row is OWED now (L2), FILED (clause
    (e)), or neither.
Q3. The PRE-COMMIT EDIT LIST, complete and exact: (i) product comments B1-B5 (which words, which files, the line-count
    constraint, the object compare, est/, the clearance); (ii) the probe docstring re-freeze D2 (which sentences); (iii)
    the gate comment D3 (live + staged identical); (iv) the staged rename D4; (v) the notes D5; (vi) the records D6-D9.
    Is anything MISSING from that list, or in it that should not be?  Is any item one that invalidates a measured receipt
    (so that a leg or a gate must be re-run) -- the main loop says none does beyond the rev-2b probe re-run on the two
    binaries and the redone object compare.
Q4. Your own pass-2 positions that the rulings ADOPTED -- the header correction with both identities recorded (your F9),
    AA6's clause-(e) grade, the (a) record form (your F4/P8), the IDR census that made D1's "only" false (your F14), the
    departure disclosures (your F10 item 7) -- scrutinise each MORE than the others; say which you would now weaken or
    withdraw.
Q5. Argon's answer (section 6): does it raise anything the other four did not, and does any of its findings change a
    disposition?  Grade each of its findings by id.

## 5. Seats not in the evidence basis

Fable 5.1 is HELD by the owner (hold question in `..\fable5.HELD.txt`).  agy fired only as Argon's transport; kimi, minimax
and Opus-as-seat are not on the roster (Opus 5.5 built and measured the round).  Say in your verdict line that the basis is
FIVE reviewing seats (or FOUR, if Argon's section is marked absent below).

## 6. Gemini 4 Argon's answer (appended by the main loop when it landed)

**Gemini 4 Argon** (`gemini-4-argon-high` through agy, `--add-dir` on GXEMUL-SEC; it opened the tree and the artifacts;
63,064 b; exit 0): **VERDICT: SHIP WITH CHANGES** -- "Fix L4 stale citation in dev_m8820x.c:361 (and est/), correct/record
probe header line 33's false include-order claim and SCORES.txt's L22 criterion + 60-char SYMPTOM truncation, clean up
staged/gate_arm.sh, and write the bounded #570 records (recording Argon as FIRED on pass 2)."  Its findings F1-F8
(`..\argon_agy_t36p2.txt:8-27`), the ask-again AA1-AA9 (`:154-169`, all graded clause (e), zero L2), Q3 (`:173-225`), Q4
(`:229-253`).  **What it adds beyond the other four:**
* **F1.3 -- TWO MORE shifted citations** (`:11`, `:84`, `:203`): `dev_luna88k.c` also gained +4 net lines, so
  `regress/luna_intmask_probe.py:2` (cites `dev_luna88k.c:816`) and `regress/m8820x_sites_probe.py:23` (cites `:901`)
  shift too -- SEVEN tracked regress citations to file, not five.  Confirmed by the main loop: `case INT_ST_MASK0` is at
  HEAD `:813` and working-tree `:817`.  -> amend B1's filing count.
* **F5.2 -- a PRETABLE sentence vs the probe** (`:20`, `:242`): PRETABLE `R-d` says the null session "pauses cpu 0 before
  cpu 1 runs"; the probe never pauses cpu 0 -- it parks in `H`'s `br .` self-loop.  A records clarification for the
  dated note beside PRETABLE (D5) and the CHANGELOG; PRETABLE itself is not edited.
* **F6 -- the pass-2 brief's section 0 still names `argon.NOT_FIRED.txt`** (`:22`, `:253`), which the main loop removed
  when Argon was fired; the ledger's pass-2 entry must record Argon FIRED (`argon_agy_t36p2.txt`), never NOT FIRED.
  Agreed -- it is in D8 by construction (the brief's text is a dated artifact and is not rewritten).
* **AA8 / AA9** (`:166-167`): `res == -1` instead of `res <= 0` (no m88k device returns below -1 -- clause (e)); the
  writes conditioned on supervisor mode (all sessions supervisor -- clause (e)).  Both new; both (e).
* **P14 / P13 graded ACCEPTABLE** (`:216-217`) against the main loop's D3 (add the qualifiers): Argon reads the two lines
  after the gate comment's opening sentence as supplying them.  The main loop keeps D3 (comment-only, cheap, and the
  opening sentence is what a reader quotes).
**Where the main loop CHECKED Argon and found it WRONG (so the adjudicator does not inherit it):**
* Its **P10 "sharpening"** (`:147`, `:215`, `:247`) -- "with R2 fixed, `ToBeTranslated` passes `NO_EXCEPTIONS` at
  `cpu_dyntrans.c:309-310` and halts via R1 without ever entering the arm" -- is FALSE on the source: the real fetch at
  `src/cpus/cpu_m88k_instr.c:2989-2990` is `cpu->memory_rw(..., MEM_READ, CACHE_INSTRUCTION)` with NO `NO_EXCEPTIONS`,
  and `cpu_dyntrans.c:306-309` (the delay-slot display read) is likewise `CACHE_INSTRUCTION` alone (read 2026-10-24
  ~03:2x).  Grok's reading (`..\grok_t36p2.txt:92`) stands: with R2 fixed the step's own fetch reaches the arm and the
  NULL test runs, then R1's `bad:` tail halts -- a source-derived PREDICTION (P10 stays "predicted", D2).  Argon's
  consequent "both R1 and R2 must be fixed before the arm is reached" is withdrawn with it; the re-root obligation
  (rows go red when R2 alone is fixed, because the halt replaces the handler) is unchanged.
* Its **pre-fix red list** (`:104`: "ust pfsr ... luna pfsr ... ifetch dcmmu") and some leg scores (`:124` L6b "20/31")
  do not match the artifacts: `prefix_HEAD.out` reds are `uld pfsr, uld pfar, ust pfsr, ust pfar, vme pfsr, vme pfar,
  luna route, luna pfar, ifetch pfsr, ifetch pfar` (no `luna pfsr`, no `ifetch dcmmu`; `uld` rows present) and
  `SCORES.txt` has L6b at 19/31.  Its clause verdicts do not rest on those misreads, but its Q2 numbers are not to be
  copied into any record.
* Its **L5 description** (`:117`: an env var `GXEMUL_F570_BIN` and a `check_prereqs()` rejecting a missing binary) is
  not the builder's leg (an exit-1 NON-EMULATOR stub in the binary's place, `L5_stub.out`, 1/31); treat as a misread.
**Question for you (Q5):** grade Argon's F1.3, F5.2, F6, AA8, AA9 and its P13/P14 "acceptable" against the dispositions;
confirm or overturn the main loop's refutation of its P10 mechanism from the two source lines named above.
